#!/usr/bin/env python3
"""Vocal stem → rhythmic syllable notation (for harsh/shouted vocals, where the rhythm and dynamics matter and
the pitch is noise): syllables are runs of vocal-band energy above a floor, split at internal dips, quantised to
a grid on the tab's own measure timeline (so odd-length bars stay exact), with velocity from loudness.

  stemvox.py STEM --tab DIR --d0 SECONDS --bars B0-B1 [--note Eb3|auto] [--grid 0.125] [--range 30] [--dip 6] [--min 0.25]
  stemvox.py STEM --map MAP.json --bars B0-B1 [...]   bar times from a tab2song map's corrected timeline
           (its offset, skipped measures and beatgrid/scorealign `bpm` overrides) instead of the raw tab

  --note   one pitch for every syllable, or `auto`: each syllable's pitch from the stem (harmonic summation,
           G3..F5; a shout's pitch moves from phrase to phrase)
  --range  dB below the passage's loudest frame that still counts as voice (default 30)
  --dip    a fall of this many dB inside a run, then a rise, starts a new syllable (default 6)
  --min    shortest syllable in beats after quantising (default 0.25)
  --onsets runs (default: energy runs split at dips) | flux (syllable starts at vocal-band flux peaks — the
           perceived attack; with --grid 0.03125 --min 0.0625 this tracks barked delivery far better)
  --shift  ms added to every syllable time (latency calibration against the target patch's attack)
  --phones per syllable, ^on=/^off= consonant codes (voice layer table) and ^vow= (u 0 … i 1) from acoustic cues
           (stems are noisy: a sketch of the syllables' shape, for voice patches binding expr.on/off/vow)
Prints one line per bar: `bar N  tokens` (R for rests), like stemnotes.py."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import likeness as L  # noqa: E402
import tabtime as T  # noqa: E402

SR = 48000


def band_env(x, hop=0.005, win=0.02, lo=250, hi=5000):
    n, h = int(win * SR), int(hop * SR)
    f = np.fft.rfftfreq(n, 1 / SR); sel = (f >= lo) & (f < hi); w = np.hanning(n)
    out = [10 * np.log10((np.abs(np.fft.rfft(x[i:i + n] * w))[sel] ** 2).sum() + 1e-12) for i in range(0, len(x) - n, h)]
    e = np.array(out)
    k = 3
    return np.convolve(e, np.ones(k) / k, "same"), hop


def syllables(env, hop, rng, dip):
    top = np.percentile(env, 99.5); on = env > top - rng
    segs, i = [], 0
    while i < len(env):
        if not on[i]:
            i += 1; continue
        j = i
        while j < len(env) and on[j]:
            j += 1
        # split [i, j) at dips: local minimum ≥ dip below the running peak, followed by a rise of ≥ dip
        start, peak = i, env[i]
        k = i + 1
        while k < j - 1:
            peak = max(peak, env[k])
            if env[k] < peak - dip and env[k] <= env[k - 1] and env[k] <= env[k + 1]:
                nxt = env[k:j].max() if k < j else env[k]
                if nxt > env[k] + dip:
                    segs.append((start, k, peak)); start, peak = k, env[k]
            k += 1
        segs.append((start, j, max(peak, env[start:j].max())))
        i = j
    return [(a * hop, b * hop, p - top) for a, b, p in segs]


def syllables_flux(env, hop, rng, height=96, gap=0.09, min_len=0.06):
    """Syllables from onsets: vocal-band flux peaks (the perceived attack, not the quiet rising edge), each
    lasting until the next onset or until the voice falls below the passage's top − rng dB."""
    from scipy import signal as sg
    top = np.percentile(env, 99.5); live = env > top - rng
    fl = np.maximum(np.diff(env, prepend=env[0]), 0)
    fl = np.convolve(fl, np.ones(3), "same")
    pk, _ = sg.find_peaks(fl, height=np.percentile(fl, height), distance=max(1, int(gap / hop)))
    pk = [p for p in pk if live[min(p + int(0.03 / hop), len(env) - 1)]]
    segs = []
    for i, p in enumerate(pk):
        nxt = pk[i + 1] if i + 1 < len(pk) else len(env)
        e = p
        while e < nxt and (live[e] or e - p < int(min_len / hop)):
            e += 1
        segs.append((p * hop, e * hop, float(env[p:max(e, p + 1)].max() - top)))
    return segs


VOWEL_F = [(300, 870), (460, 840), (730, 1090), (530, 1840), (270, 2290)]   # u o a e i (the voice layer's table)


def vowel_of(seg):
    """Position on the voice layer's u (0) – o – a – e – i (1) axis from LPC F1/F2 (log distance to the
    five targets, interpolating between the nearest pair along the axis)."""
    import voxprofile as VP
    f1, f2 = VP.lpc_formants(seg)
    if not f1 or not f2:
        return None
    d = [np.hypot(np.log(f1 / a), np.log(f2 / b)) for a, b in VOWEL_F]
    i = int(np.argmin(d))
    j = i + 1 if i == 0 else i - 1 if i == 4 else (i + 1 if d[i + 1] < d[i - 1] else i - 1)
    w = d[i] / (d[i] + d[j] + 1e-9)
    return round((i * (1 - w) + j * w) / 4, 2)


def band_ratio(seg, lo, hi):
    if len(seg) < 256:
        return 0.0
    f = np.fft.rfftfreq(len(seg), 1 / SR); p = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))) ** 2
    tot = p[(f >= 80) & (f < 12000)].sum() + 1e-20
    return float(p[(f >= lo) & (f < hi)].sum() / tot)


def centroid(seg):
    f = np.fft.rfftfreq(len(seg), 1 / SR); p = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))) ** 2
    return float((f * p)[(f >= 80) & (f < 12000)].sum() / (p[(f >= 80) & (f < 12000)].sum() + 1e-20))


def level(seg):
    return 20 * np.log10(np.sqrt((seg ** 2).mean()) + 1e-9) if len(seg) else -200.0


def consonant_at(x, t, peak_db, coda=False):
    """Consonant class around a syllable edge (t, s) as a voice-layer code, from simple acoustic cues: noise
    above 4 kHz → /s/ (11), 2.5-4 kHz → /sh/ (13), a gap then a burst → a stop (place by the burst's centroid:
    low b, mid g, high d; long noise before voicing → unvoiced p/k/t), energy under 400 Hz → a nasal (m / n),
    else none. Separation bleed makes this a sketch, not a phonetic transcription."""
    w = lambda a, b: x[max(0, int((t + a) * SR)):max(0, int((t + b) * SR))]
    edge = w(-0.01, 0.05) if not coda else w(-0.06, 0.0)
    if len(edge) < 512 or level(edge) < peak_db - 35:
        return 0
    hf, mhf, lo = band_ratio(edge, 4000, 9000), band_ratio(edge, 2500, 4000), band_ratio(edge, 80, 400)
    if hf > 0.35:
        return 11
    if mhf > 0.35:
        return 13
    if not coda:
        gap = w(-0.06, -0.015)
        if len(gap) and level(gap) < peak_db - 22:
            burst = w(-0.005, 0.015); c = centroid(burst) if len(burst) > 256 else 2000
            noisy = band_ratio(w(0.0, 0.04), 2000, 9000) > 0.4
            if c < 1500:
                return 1 if noisy else 2
            if c < 3000:
                return 5 if noisy else 6
            return 3 if noisy else 4
        if lo > 0.6:
            return 16
    else:
        after = w(0.0, 0.05)
        if len(after) and level(after) < peak_db - 22:
            return 4
        if lo > 0.6:
            return 17
    return 0


def syllable_pitch(x, a, b, lo=55, hi=77, default="A4"):
    """Pitch of one syllable (MIDI lo..hi): harmonic summation over 5 harmonics of the segment's spectrum.
    Shouted vocals are noisy but strongly pitched; the estimate is the most salient harmonic series."""
    seg = x[int(a * SR):int(b * SR)]
    if len(seg) < int(0.04 * SR):
        return default
    n = 1 << int(np.ceil(np.log2(max(len(seg), 8192))))
    spec = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), n))
    f = np.fft.rfftfreq(n, 1 / SR)
    mag = np.log1p(spec / (spec.max() + 1e-12) * 1000)
    best, bm = -1.0, None
    for m in range(lo, hi + 1):
        f0 = 440 * 2 ** ((m - 69) / 12)
        s = sum(mag[min(len(mag) - 1, int(round(h * f0 * n / SR)))] / h for h in range(1, 6))
        if s > best:
            best, bm = s, m
    names = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
    return f"{names[bm % 12]}{bm // 12 - 1}"


def main():
    a = sys.argv[1:]
    stem = a[0]
    opt = lambda k, d: a[a.index(k) + 1] if k in a else d
    tab, d0 = opt("--tab", None), float(opt("--d0", "0"))
    b0, b1 = (int(v) for v in opt("--bars", "1-1").split("-"))
    note, grid = opt("--note", "Eb3"), float(opt("--grid", "0.125"))
    rng, dip, mn = float(opt("--range", "30")), float(opt("--dip", "6")), float(opt("--min", "0.25"))
    mode, shift = opt("--onsets", "runs"), float(opt("--shift", "0")) / 1000
    phones = "--phones" in a
    tl = T.timeline(tab) if tab else None
    if opt("--map", None):
        import importlib.util
        import json
        here = os.path.dirname(os.path.abspath(__file__))
        spec = importlib.util.spec_from_file_location("t2s", os.path.join(here, "tab2song.py"))
        t2s = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(t2s)
        mp = json.load(open(opt("--map", None)))
        cache = mp["cache"] if os.path.isabs(mp["cache"]) else os.path.join(os.path.dirname(here), mp["cache"])
        tl, t = [], mp.get("offset", 0.0)
        for m in t2s.corrected_timeline(cache, mp):   # skipped measures keep a zero-length slot
            tl.append({"m": m["m"], "start": t, "beats": 0.0 if m["skip"] else m["beats"], "bpm": m["bpm"]})
            if not m["skip"]:
                t += m["beats"] * 60 / m["bpm"]
        d0 = 0.0
    t_start = d0 + tl[b0 - 1]["start"]
    last = tl[b1 - 1]; t_end = d0 + last["start"] + last["beats"] * 60 / last["bpm"]
    x = L.load(stem).mean(1)[int(t_start * SR):int(t_end * SR)]
    env, hop = band_env(x)
    segs = syllables_flux(env, hop, rng) if mode == "flux" else syllables(env, hop, rng, dip)
    segs = [(s + shift, e + shift, lvl) for s, e, lvl in segs]
    # time → (bar, beat-in-bar) on the tab timeline, quantised
    bars = {m: [] for m in range(b0, b1 + 1)}
    for s, e, lvl in segs:
        ts, te = t_start + s, t_start + e
        for m in range(b0, b1 + 1):
            ms = d0 + tl[m - 1]["start"]; spb = 60 / tl[m - 1]["bpm"]; me = ms + tl[m - 1]["beats"] * spb
            if ms <= ts < me:
                qs = round((ts - ms) / spb / grid) * grid
                ql = max(mn, round((te - ts) / spb / grid) * grid)
                vel = int(np.clip(120 + 3 * lvl, 50, 124))
                pitch = syllable_pitch(x, s, e) if note == "auto" else note
                suffix = ""
                if phones:
                    seg = x[int((s - shift) * SR):int((e - shift) * SR)]
                    pk = max((level(seg[i:i + 960]) for i in range(0, max(1, len(seg) - 960), 480)), default=-200.0)
                    on, off = consonant_at(x, s - shift, pk), consonant_at(x, e - shift, pk, coda=True)
                    mid = seg[int(len(seg) * 0.2):int(len(seg) * 0.8)]
                    vw = (vowel_of(mid) if len(mid) > 2048 else None) or 0.62   # an open a/e when unmeasurable
                    suffix = (f"^on={on}" if on else "") + (f"^vow={vw}" if vw is not None else "") + (f"^off={off}" if off else "")
                bars[m].append([qs, ql, vel, pitch, suffix])
                break
    for m in range(b0, b1 + 1):
        nb = tl[m - 1]["beats"]; ev = sorted(bars[m]); toks, pos = [], 0.0
        for qs, ql, vel, pitch, suffix in ev:
            if qs < pos - 1e-9 or qs >= nb:
                continue
            if qs > pos + 1e-9:
                toks.append(f"R/{qs - pos:g}b")
            ql = min(ql, nb - qs)
            toks.append(f"{pitch}/{ql:g}b@{vel}{suffix}"); pos = qs + ql
        if pos < nb - 1e-9:
            toks.append(f"R/{nb - pos:g}b")
        print(f"bar {m:3d}  {' '.join(toks)}")


if __name__ == "__main__":
    main()
