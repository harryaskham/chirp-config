#!/usr/bin/env python3
"""voicefit: measure a synthesised voice against the record's vocal and say which voice-layer settings to move.

  voicefit.py SONG TRACK [--ref VOCALS.wav] [--from S --to S] [--set PATH=VALUE …] [--seed N] [--keep DIR] [--json]
  voicefit.py --wav OURS.wav --ref VOCALS.wav [--from S --to S] [--json]          # analysis only

SONG TRACK renders the track solo (`chirp render --solo`, the adopted groove pin) and compares it with the record's
separated vocal (default ref/stems/htdemucs_6s/<song>/vocals.wav) over the same window. Both are measured on their
voiced frames only (YIN pitch, 20 ms hop):

  pitch            median and p10-p90 (an octave apart from the record = the part sits in the wrong register)
  effort           H1-H2, dB: the first harmonic over the second. High = soft, open, breathy phonation; low =
                   pressed. Ours lower than the record -> lower `effort`.
  breathiness      harmonics-to-noise ratio, dB, below 4 kHz. Ours higher (cleaner) -> raise `breath`; lower
                   (noisier) -> lower `breath` / `scream`.
  growl            subharmonic ratio, dB: energy at (k+1/2)*f0 over the harmonics (period doubling, false folds,
                   jitter). Ours above the record -> lower `rasp`, `fold`, `scream`, `vary`.
  singer's formant 2.4-3.4 kHz over 0-2 kHz, dB. Ours above -> lower `ring` / `cluster`; below -> raise them.
  tract            mean formant spacing (F1..F4 of a cepstrally smoothed envelope); `tract` divides every formant,
                   so the suggestion is tract x (ours / record).
  vibrato          rate and depth (cents) on sustained notes (>= 0.5 s within +-80 cents); a patch's vibrato is
                   an LFO on `pitch` whose amount is in semitones (depth/100).

The record's stem holds every vocal (backing included) and the separator's residue, so treat the deltas as
directions, not targets; formant spacing is unreliable on high voices (wide-spaced harmonics). Guidance only,
like vocalscore and noteacc: it never edits a song. CHIRP picks the binary.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import wave

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chirpbin  # noqa: E402  (the adopted groove pin when CHIRP is unset)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 24000
HOP = 480          # 20 ms
WIN = 2048
NOTE = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def load(path, t0=None, t1=None):
    """Mono float at SR (ffmpeg resamples), cropped to [t0, t1) seconds."""
    d = tempfile.mkdtemp(prefix="voicefit-")
    try:
        out = os.path.join(d, "m.wav")
        cmd = ["ffmpeg", "-v", "error", "-y"]
        if t0 is not None:
            cmd += ["-ss", str(t0)]
        if t1 is not None:
            cmd += ["-t", str(t1 - (t0 or 0))]
        cmd += ["-i", path, "-ac", "1", "-ar", str(SR), "-sample_fmt", "s16", out]
        subprocess.run(cmd, check=True, stdin=subprocess.DEVNULL)
        with wave.open(out) as f:
            x = np.frombuffer(f.readframes(f.getnframes()), dtype="<i2").astype(float) / 32768
        return x
    finally:
        shutil.rmtree(d, ignore_errors=True)


def yin(frame, fmin=70.0, fmax=1000.0, thresh=0.15):
    """f0 (Hz) and aperiodicity (CMNDF at the chosen lag; lower = more periodic), or (None, 1)."""
    n = len(frame)
    lo, hi = int(SR / fmax), min(int(SR / fmin), n // 2)
    f = np.fft.rfft(frame, 2 * n)
    r = np.fft.irfft(f * np.conj(f))[:hi + 1]
    e = np.cumsum(frame ** 2)
    # d(tau) = sum_{j<n-tau} (x_j - x_{j+tau})^2 = E[0:n-tau] + E[tau:n] - 2 r(tau)
    taus = np.arange(hi + 1)
    e0 = e[n - 1 - taus]
    e1 = e[n - 1] - np.concatenate(([0.0], e[:hi]))
    d = e0 + e1 - 2 * r
    d[0] = 0
    cm = np.ones_like(d)
    cs = np.cumsum(d[1:])
    cm[1:] = d[1:] * np.arange(1, hi + 1) / np.maximum(cs, 1e-12)
    cand = np.where(cm[lo:hi] < thresh)[0]
    if len(cand):
        t = lo + cand[0]
        while t + 1 < hi and cm[t + 1] < cm[t]:
            t += 1
    else:
        t = lo + int(np.argmin(cm[lo:hi]))
    if cm[t] > 0.45:
        return None, float(cm[t])
    # parabolic refinement
    if 1 <= t < hi:
        a, b, c = cm[t - 1], cm[t], cm[t + 1]
        den = a - 2 * b + c
        off = 0.5 * (a - c) / den if abs(den) > 1e-12 else 0.0
        t = t + float(np.clip(off, -0.5, 0.5))      # a flat parabola must not throw the lag out of range
    return SR / t, float(cm[min(int(round(t)), hi)])


def band_power(spec, freqs, f, half):
    m = (freqs >= f - half) & (freqs <= f + half)
    return float(spec[m].max()) if m.any() else 0.0


def frame_measures(frame, f0):
    w = frame * np.hanning(len(frame))
    nfft = 8192
    spec = np.abs(np.fft.rfft(w, nfft)) ** 2
    freqs = np.arange(len(spec)) * SR / nfft
    half = min(0.1 * f0, 40.0)
    kmax = max(2, min(20, int(4000 / f0)))
    harm = [band_power(spec, freqs, k * f0, half) for k in range(1, kmax + 1)]
    # subharmonic peaks at (k+1/2)*f0, counted only above the noise beside them (the same max statistic over
    # equal-width bands at (k+1/4) and (k+3/4)*f0), so breathiness alone does not read as growl
    sub = []
    for k in range(1, min(kmax, 8)):
        s = band_power(spec, freqs, (k + 0.5) * f0, half)
        flank = 0.5 * (band_power(spec, freqs, (k + 0.25) * f0, half) + band_power(spec, freqs, (k + 0.75) * f0, half))
        sub.append(s - flank if s > 4 * flank else 0.0)    # a peak 6 dB over its flanks, not a noise maximum
    noise = []
    for k in range(1, kmax):
        for a, b in ((0.15, 0.35), (0.65, 0.85)):     # clear of harmonic and half-harmonic main lobes
            m = (freqs >= (k + a) * f0) & (freqs <= (k + b) * f0)
            if m.any():
                noise.append(float(np.median(spec[m])))
    eps = 1e-20
    h1h2 = 10 * np.log10((harm[0] + eps) / (harm[1] + eps))
    shr = max(-60.0, 10 * np.log10((sum(sub) + eps) / (sum(harm[:len(sub)]) + eps))) if sub else None
    # harmonic peak power vs the median inter-harmonic bin power, both per bin (same units)
    hnr = 10 * np.log10((np.mean(harm[:kmax - 1]) + eps) / (np.mean(noise) + eps)) if noise else None
    lo = spec[(freqs > 60) & (freqs < 2000)].sum()
    ring = 10 * np.log10((spec[(freqs >= 2400) & (freqs <= 3400)].sum() + eps) / (lo + eps))
    # cepstrally smoothed envelope: keep quefrencies below ~0.7 of the pitch period
    logs = np.log(spec + 1e-12)
    cep = np.fft.irfft(logs)
    qc = max(8, int(0.7 * SR / f0))
    cep[qc:len(cep) - qc] = 0
    env = np.fft.rfft(cep).real
    peaks = [i for i in range(1, len(env) - 1) if env[i] > env[i - 1] and env[i] >= env[i + 1]]
    pf = [freqs[i] for i in peaks if 200 <= freqs[i] <= 4500]
    fm = []
    for lo_f, hi_f in ((200, 1000), (700, 2700), (2000, 3500), (3000, 4500)):
        c = [p for p in pf if lo_f <= p <= hi_f and (not fm or p > fm[-1] + 150)]
        if c:
            fm.append(c[0])
    spacing = (fm[-1] - fm[0]) / (len(fm) - 1) if len(fm) >= 3 else None
    return dict(h1h2=h1h2, shr=shr, hnr=hnr, ring=ring, spacing=spacing)


def vibrato(f0s, voiced):
    """Median (rate Hz, depth cents) over sustained runs, or (None, None)."""
    fs = SR / HOP
    rates, depths = [], []
    i, n = 0, len(f0s)
    while i < n:
        if not voiced[i]:
            i += 1
            continue
        j = i
        while j < n and voiced[j]:
            j += 1
        seg = np.array(f0s[i:j])
        k = i
        # split the voiced run into note-steady stretches
        start = 0
        cents = 1200 * np.log2(seg / seg[0])
        for t in range(1, len(seg) + 1):
            if t == len(seg) or abs(cents[t] - np.median(cents[start:t])) > 80:
                run = cents[start:t]
                if len(run) >= int(0.5 * fs):
                    x = np.arange(len(run), dtype=float)
                    xm, ym = x.mean(), run.mean()
                    slope = ((x - xm) * (run - ym)).sum() / ((x - xm) ** 2).sum()
                    y = run - (ym + slope * (x - xm))
                    best = (0.0, None)
                    for rate in np.arange(3.0, 9.01, 0.1):
                        ph = 2 * np.pi * rate * x / fs
                        amp = 2 * abs(np.mean(y * np.exp(-1j * ph)))
                        if amp > best[0]:
                            best = (amp, rate)
                    if best[1] is not None and best[0] > 5:
                        rates.append(best[1])
                        depths.append(best[0])
                start = t
        i = j if j > k else i + 1
    if not rates:
        return None, None
    return float(np.median(rates)), float(np.median(depths))


def analyse(x):
    if len(x) < WIN:
        return None
    rms = np.array([np.sqrt(np.mean(x[i:i + WIN] ** 2)) for i in range(0, len(x) - WIN, HOP)])
    floor = np.percentile(rms[rms > 0], 95) * 10 ** (-35 / 20) if (rms > 0).any() else 1.0
    f0s, voiced, ms = [], [], []
    for k, i in enumerate(range(0, len(x) - WIN, HOP)):
        fr = x[i:i + WIN]
        f0 = None
        if rms[k] >= floor:
            f0, _ = yin(fr[:1200])
        f0s.append(f0 or 0.0)
        voiced.append(f0 is not None)
        if f0 is not None:
            ms.append(frame_measures(fr, f0))
    if not ms:
        return None
    f = np.array([v for v in f0s if v > 0])
    med = lambda key: (float(np.median([m[key] for m in ms if m[key] is not None]))  # noqa: E731
                       if any(m[key] is not None for m in ms) else None)
    rate, depth = vibrato(f0s, voiced)
    # period doubling: voiced frames an octave (+-1 st) under the running median pitch of the 1 s around them
    # (the pitch tracker then counts the subharmonics as harmonics, so `shr` misses it)
    fa = np.array(f0s)
    low = tot = 0
    half = int(0.5 * SR / HOP)
    for i in np.where(fa > 0)[0]:
        ctx = fa[max(0, i - half):i + half + 1]
        ctx = ctx[ctx > 0]
        if len(ctx) >= 10:
            tot += 1
            low += abs(12 * np.log2(fa[i] / np.median(ctx)) + 12) < 1
    return dict(octave_low=round(100.0 * low / tot, 1) if tot else None, voiced_s=round(len(ms) * HOP / SR, 1),
                f0_median=float(np.median(f)),
                f0_p10=float(np.percentile(f, 10)), f0_p90=float(np.percentile(f, 90)),
                h1h2=med("h1h2"), hnr=med("hnr"), shr=med("shr"), ring=med("ring"), spacing=med("spacing"),
                vib_rate=rate, vib_depth=depth)


def note(hz):
    m = 69 + 12 * np.log2(hz / 440)
    r = int(round(m))
    return f"{NOTE[r % 12]}{r // 12 - 1}"


def advice(ref, ours):
    """[(measure, suggestion)] for differences past a threshold."""
    out = []
    st = 12 * np.log2(ours["f0_median"] / ref["f0_median"])
    if abs(st) >= 9:
        out.append(("pitch", f"ours sits {st:+.1f} semitones from the record: check the part's octave"))
    if ref["h1h2"] is not None and ours["h1h2"] is not None:
        d = ours["h1h2"] - ref["h1h2"]
        if d <= -3:
            out.append(("effort", f"ours {-d:.1f} dB more pressed (H1-H2): lower `effort`"))
        elif d >= 3:
            out.append(("effort", f"ours {d:.1f} dB softer (H1-H2): raise `effort`"))
    if ref["hnr"] is not None and ours["hnr"] is not None:
        d = ours["hnr"] - ref["hnr"]
        if d >= 3:
            out.append(("breathiness", f"ours {d:.1f} dB cleaner (HNR): raise `breath`"))
        elif d <= -3:
            out.append(("breathiness", f"ours {-d:.1f} dB noisier (HNR): lower `breath`, `vary` (jitter/shimmer) "
                                       f"or `scream`"))
    if ref["shr"] is not None and ours["shr"] is not None:
        d = ours["shr"] - ref["shr"]
        if d >= 3:
            out.append(("growl", f"ours {d:.1f} dB more subharmonic energy: lower `rasp`, `fold`, `scream`, `vary`"))
    if ref.get("octave_low") is not None and ours.get("octave_low") is not None:
        d = ours["octave_low"] - ref["octave_low"]
        if d >= 2:
            out.append(("growl", f"{ours['octave_low']:.1f}% of our voiced frames read an octave low (record "
                                 f"{ref['octave_low']:.1f}%): period doubling, lower `vary`, `pulse_vary`, `rasp`, `fold`"))
    if ref["ring"] is not None and ours["ring"] is not None:
        d = ours["ring"] - ref["ring"]
        if d >= 3:
            out.append(("singer's formant", f"ours {d:.1f} dB stronger at 2.4-3.4 kHz: lower `ring` / `cluster`"))
        elif d <= -3:
            out.append(("singer's formant", f"ours {-d:.1f} dB weaker at 2.4-3.4 kHz: raise `ring` / `cluster`"))
    if ref["spacing"] and ours["spacing"]:
        r = ours["spacing"] / ref["spacing"]
        if abs(r - 1) >= 0.04:
            out.append(("tract", f"formant spacing ours/record {r:.3f}: `tract` x {r:.2f} "
                                 f"({'longer, darker' if r > 1 else 'shorter, brighter'})"))
    if ref["vib_rate"] and ours["vib_rate"]:
        if abs(ours["vib_rate"] - ref["vib_rate"]) >= 0.5 or abs(ours["vib_depth"] - ref["vib_depth"]) >= 10:
            out.append(("vibrato", f"record {ref['vib_rate']:.1f} Hz / {ref['vib_depth']:.0f} cents, ours "
                                   f"{ours['vib_rate']:.1f} Hz / {ours['vib_depth']:.0f} cents: LFO rate "
                                   f"{ref['vib_rate']:.1f}hz, pitch mod amount {ref['vib_depth'] / 100:.2f}"))
    elif ref["vib_rate"] and not ours["vib_rate"]:
        out.append(("vibrato", f"record has {ref['vib_rate']:.1f} Hz / {ref['vib_depth']:.0f} cents, ours none: "
                               f"LFO on `pitch`, rate {ref['vib_rate']:.1f}hz, amount {ref['vib_depth'] / 100:.2f}"))
    return out


def table(ref, ours):
    def f(v, fmt):
        return format(v, fmt) if v is not None else "-"
    rows = [("voiced seconds", f(ref["voiced_s"], ".1f"), f(ours["voiced_s"], ".1f")),
            ("pitch median", f"{note(ref['f0_median'])} {ref['f0_median']:.0f} Hz",
             f"{note(ours['f0_median'])} {ours['f0_median']:.0f} Hz"),
            ("pitch p10-p90", f"{note(ref['f0_p10'])}-{note(ref['f0_p90'])}", f"{note(ours['f0_p10'])}-{note(ours['f0_p90'])}"),
            ("effort H1-H2 dB", f(ref["h1h2"], ".1f"), f(ours["h1h2"], ".1f")),
            ("breathiness HNR dB", f(ref["hnr"], ".1f"), f(ours["hnr"], ".1f")),
            ("growl subharm dB", f(ref["shr"], ".1f"), f(ours["shr"], ".1f")),
            ("growl octave-low %", f(ref.get("octave_low"), ".1f"), f(ours.get("octave_low"), ".1f")),
            ("singer's formant dB", f(ref["ring"], ".1f"), f(ours["ring"], ".1f")),
            ("formant spacing Hz", f(ref["spacing"], ".0f"), f(ours["spacing"], ".0f")),
            ("vibrato", f"{f(ref['vib_rate'], '.1f')} Hz / {f(ref['vib_depth'], '.0f')} c",
             f"{f(ours['vib_rate'], '.1f')} Hz / {f(ours['vib_depth'], '.0f')} c")]
    lines = [f"  {'':22s} {'record':>16s} {'ours':>16s}"]
    lines += [f"  {a:22s} {b:>16s} {c:>16s}" for a, b, c in rows]
    return "\n".join(lines)


def main(a):
    js = "--json" in a
    value_flags = ("--ref", "--from", "--to", "--set", "--wav", "--seed", "--keep")

    def opt(k, default=None):
        if k not in a:
            return default
        i = a.index(k) + 1
        if i >= len(a) or a[i].startswith("--"):
            raise SystemExit(f"{k} needs a value")
        return a[i]

    t0 = float(opt("--from").rstrip("s")) if "--from" in a else None
    t1 = float(opt("--to").rstrip("s")) if "--to" in a else None
    work = tempfile.mkdtemp(prefix="voicefit-")
    try:
        if "--wav" in a:
            ours_wav, ref_wav, label = opt("--wav"), opt("--ref"), os.path.basename(opt("--wav"))
            if not ref_wav:
                raise SystemExit("--wav needs --ref")
            ours = analyse(load(ours_wav, t0, t1))
        else:
            pos = [x for i, x in enumerate(a) if not x.startswith("--") and (i == 0 or a[i - 1] not in value_flags)]
            if len(pos) < 2:
                raise SystemExit(__doc__)
            song, track = pos[:2]
            sid = os.path.splitext(os.path.basename(song))[0]
            ref_wav = opt("--ref") or os.path.join(ROOT, "ref", "stems", "htdemucs_6s", sid, "vocals.wav")
            if not os.path.exists(ref_wav):
                raise SystemExit(f"no record vocal at {ref_wav}: give --ref")
            label = f"{sid} track {track}"
            keep = opt("--keep")
            if keep:
                os.makedirs(keep, exist_ok=True)
            ours_wav = os.path.join(keep or work, f"{sid}-{track}.wav")   # --keep DIR keeps the solo render
            cmd = ["nice", "-n", "15", chirpbin.resolve("chirp"), "render", "-f", song, "--solo", track, "-o", ours_wav]
            if "--seed" in a:
                cmd += ["--seed", opt("--seed")]
            for i, x in enumerate(a):
                if x == "--set":
                    cmd += ["--set", a[i + 1]]
            r = subprocess.run(cmd, capture_output=True, text=True, stdin=subprocess.DEVNULL)
            if r.returncode:
                raise SystemExit(f"render failed: {r.stderr[-600:]}")
            ours = analyse(load(ours_wav, t0, t1))
        ref = analyse(load(ref_wav, t0, t1))
        if not ref or not ours:
            raise SystemExit("no voiced frames in " + ("the record" if not ref else "ours"))
        adv = advice(ref, ours)
        if js:
            print(json.dumps({"record": ref, "ours": ours, "advice": [{"measure": m, "suggestion": s} for m, s in adv]},
                             indent=1))
            return
        win = f"{t0 or 0:g}-{t1:g} s" if t1 else (f"from {t0:g} s" if t0 else "whole song")
        print(f"voicefit {label} ({win}; record {os.path.relpath(ref_wav, ROOT) if ref_wav.startswith(ROOT) else ref_wav})")
        print(table(ref, ours))
        print("\n".join(f"  -> {m}: {s}" for m, s in adv) if adv else "  -> no setting differs past its threshold")
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main(sys.argv[1:])
