#!/usr/bin/env python3
"""microscore: how closely a short clip (1-10 s) reproduces the record LOCALLY, by signal measures only (Harry, 25 Oct:
a micro benchmark that sees sound, not song shape: where our songs lean on global metrics to hide bad local sound).

  microscore.py REF.wav CAND.wav [--ref-from S --ref-to S] [--cand-from S --cand-to S] [--json]
  microscore.py --clip ID CAND.wav | --clip ID --song SONG.yaml        (a clip from micro/clips.json)
  microscore.py --mask [--clips a,b] [-j 3]          each clip's song's current render over the same window
  microscore.py --clip ID --song micro/songs/ID.yaml [--seeds 0,3,7,11] --record NOTE [--as WHO]   (ledger)
  microscore.py --board                              the best recorded total per clip (holdouts marked)
  microscore.py --clip ID --context TRACKS [--set tracks.N.patch=P …] [--seeds …] [--record NOTE]
  microscore.py --section SONG:A-B [--context TRACKS] [--stem FAMILY|PATH] [--song-file F] [--set …] [--seeds …]
               [--try 'LABEL: PATH=V PATH=V' …] [--mono] [--explain]
        any window of an album song, not only benchmark clips (section micro-climbs; never written to the ledger):
        the song rendered with --from/--to (bit-identical to the full render; cost runs to the window's end, far less
        with TRACKS soloed) and scored against the record's mix over A-B, or with --stem the separated stem (FAMILY:
        ref/stems/htdemucs_6s/SONG/FAMILY.wav, STEM+STEM summed, or a WAV path) where the part isn't exposed. --try scores variants on
        the same seeds and prints each one's delta to the baseline.
        the clip's album song rendered with TRACKS soloed (its master, buses and lanes kept): patches judged in the
        record's own master context. masteraudit across 111 songs found no common master tilt (median correction
        within +-2 dB, quartiles +-2-3 dB both ways), so a standard harness master would not remove the bias; each
        record's master corrects toward its own colour (Mind's Mirrors' harness 31.0, in context 49.2).

The candidate is level-matched to the reference (RMS) and aligned within +-50 ms before anything is measured, so
loudness and placement are not scored. Seven dimensions, each 0-100 (100 = the reference against itself):
  spectral    multi-resolution STFT (256/1024/4096): spectral convergence + log-magnitude distance
  timbre      mel-cepstral distance (40 mel bands, cepstra 1-13), frame by frame
  tone        long-term 1/6-octave spectrum shape (dB), over the reference's audible bands
  transients  correlation of the onset (spectral flux) envelopes
  pitch       monophonic clips only (most reference frames voiced): cents error and voicing agreement (SHS f0)
  modulation  the modulation spectra (0.5-20 Hz) of four band envelopes: tremolo, beating, vibrato, room motion
  stereo      per-band inter-channel correlation and level difference
total = their weighted mean (spectral .25, timbre .2, tone .15, transients .15, pitch .1, modulation .1, stereo .05;
pitch's weight is shared out when the clip is not monophonic). Read-only.
"""
import argparse
import contextlib
import json
import os
import subprocess
import sys
import tempfile

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import likeness as L  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = L.SR
WEIGHTS = {"spectral": .25, "timbre": .2, "tone": .15, "transients": .15, "pitch": .1, "modulation": .1, "stereo": .05}
# calibrated on the 25 Oct masking report (37 clips, our best song renders vs the records): the median reproduction
# scores ~45 on each dimension (pitch stricter: a semitone ~43), so a climber gets a gradient both ways
SCALES = {"spectral": 1.3, "timbre": 40.0, "tone": 8.0, "pitch": 120.0, "modulation": 0.45, "stereo": 0.7}
BANDS4 = ((60, 250), (250, 1000), (1000, 4000), (4000, 12000))


def stereo2(x):
    return np.stack([x, x], 1) if x.ndim == 1 else x[:, :2]


def cut(x, t0=None, t1=None):
    a = int((t0 or 0) * SR)
    b = len(x) if t1 is None else int(t1 * SR)
    return x[a:b]


def stft_mag(x, n):
    from scipy import signal
    _, _, z = signal.stft(x, SR, nperseg=n, noverlap=n - n // 4, boundary=None, padded=False)
    return np.abs(z)


def align(ref, cand, max_ms=50.0):
    """CAND shifted (zero-filled) to the lag maximising its correlation with REF (mono, |lag| <= max_ms)."""
    r, c = ref.mean(1), cand.mean(1)
    m = int(max_ms / 1000 * SR)
    n = min(len(r), len(c))
    if n < 4 * m:
        return cand
    best, lag = -np.inf, 0
    seg = r[m:n - m]
    for g in range(-m, m + 1, 8):
        v = float(seg @ c[m + g:n - m + g])
        if v > best:
            best, lag = v, g
    for g in range(lag - 8, lag + 9):
        if -m <= g <= m:
            v = float(seg @ c[m + g:n - m + g])
            if v > best:
                best, lag = v, g
    out = np.zeros_like(cand)
    if lag >= 0:
        out[:len(cand) - lag] = cand[lag:]
    else:
        out[-lag:] = cand[:len(cand) + lag]
    return out


def level_match(ref, cand):
    rr, rc = np.sqrt(np.mean(ref ** 2)), np.sqrt(np.mean(cand ** 2))
    return cand * (rr / rc) if rc > 1e-9 else cand


def d_spectral(r, c):
    out = []
    for n in (256, 1024, 4096):
        a, b = stft_mag(r, n), stft_mag(c, n)
        k = min(a.shape[1], b.shape[1])
        a, b = a[:, :k], b[:, :k]
        sc = np.linalg.norm(a - b) / (np.linalg.norm(a) + 1e-9)
        lm = np.mean(np.abs(np.log(a + 1e-5) - np.log(b + 1e-5)))
        out.append(sc + 0.25 * lm)
    return float(np.mean(out))


def mel_fb(n_fft, n_mels=40, fmin=40.0, fmax=16000.0):
    mel = lambda f: 2595 * np.log10(1 + f / 700)  # noqa: E731
    imel = lambda m: 700 * (10 ** (m / 2595) - 1)  # noqa: E731
    pts = imel(np.linspace(mel(fmin), mel(fmax), n_mels + 2))
    f = np.fft.rfftfreq(n_fft, 1 / SR)
    fb = np.zeros((n_mels, len(f)))
    for i in range(n_mels):
        lo, ce, hi = pts[i:i + 3]
        fb[i] = np.clip(np.minimum((f - lo) / (ce - lo + 1e-9), (hi - f) / (hi - ce + 1e-9)), 0, None)
    return fb


def cepstra(x, n=2048):
    from scipy.fft import dct
    p = stft_mag(x, n) ** 2
    m = np.log10(mel_fb(n) @ p + 1e-10)
    return dct(m, axis=0, norm="ortho")[1:14]


def d_timbre(r, c):
    a, b = cepstra(r), cepstra(c)
    k = min(a.shape[1], b.shape[1])
    e = np.sqrt(2 * np.sum((a[:, :k] - b[:, :k]) ** 2, 0)) * 10 / np.log(10)
    w = np.sum(a[:, :k] ** 2, 0) > 0
    return float(np.mean(e[w])) if w.any() else float(np.mean(e))


def sixth_octave(x):
    p = np.mean(stft_mag(x, 8192) ** 2, 1)
    f = np.fft.rfftfreq(8192, 1 / SR)
    edges = 40 * 2 ** (np.arange(0, 8.7, 1 / 6))
    return np.array([10 * np.log10(np.mean(p[(f >= a) & (f < b)]) + 1e-14) for a, b in zip(edges[:-1], edges[1:])])


def d_tone(r, c):
    a, b = sixth_octave(r), sixth_octave(c)
    on = a > a.max() - 50
    a, b = a - a[on].mean(), b - b[on].mean()
    return float(np.sqrt(np.mean((a[on] - b[on]) ** 2)))


def onset_env(x):
    """Linear-magnitude spectral flux on 256-sample frames (1.3 ms hop), smoothed over 30 ms: log flux jumps at any
    onset and cannot tell an 80 ms swell from a 3 ms pluck (r 0.993); linear flux at 1.3 ms punished ordinary 10-30 ms
    note timing (most real clips read ~0). Bin 0 (DC-93 Hz) is left out, so a bass's sub-octave can't swamp the attacks
    (chirper-three's genesis-bass-4: a 23 Hz sub dragged transients); its harmonics carry the attack."""
    m = stft_mag(x, 256)[1:]                             # bin 0 (DC-93 Hz at 256 points) dropped: a sub can't swamp it
    flux = np.maximum(0, np.diff(m, axis=1)).sum(0)
    return np.convolve(flux, np.ones(23) / 23, "same")   # 30 ms: a player's 20 ms timing 0.81, an 80 ms swell 0.61


def s_transients(r, c):
    a, b = onset_env(r), onset_env(c)
    k = min(len(a), len(b))
    a, b = a[:k] - a[:k].mean(), b[:k] - b[:k].mean()
    den = np.linalg.norm(a) * np.linalg.norm(b)
    return float(max(0.0, (a @ b) / den)) * 100 if den > 0 else 0.0


def f0_frames(x):
    import voxtrans
    f0, lev, _ = voxtrans.f0_track(x, lo=40.0, hi=1600.0, floor=30.0, prom=2.0)
    return f0


def d_pitch(r, c, min_share=0.5):
    """(cents-equivalent distance, voiced share of the reference) or (None, share) when under MIN_SHARE is voiced."""
    a, b = f0_frames(r), f0_frames(c)
    k = min(len(a), len(b))
    a, b = a[:k], b[:k]
    va, vb = ~np.isnan(a), ~np.isnan(b)
    share = float(va.mean()) if k else 0.0
    if share < min_share:
        return None, share
    both = va & vb
    if not both.any():
        return 1200.0, share
    cents = np.abs(1200 * np.log2(b[both] / a[both]))
    cents = np.minimum(cents, 1200)
    agree = (va == vb).mean()
    return float(np.median(cents) + 300 * (1 - agree)), share


def band_envs(x):
    m = stft_mag(x, 1024) ** 2
    f = np.fft.rfftfreq(1024, 1 / SR)
    return [np.sqrt(m[(f >= a) & (f < b)].sum(0)) for a, b in BANDS4]


def d_modulation(r, c):
    fps = SR / 256
    out = []
    for a, b in zip(band_envs(r), band_envs(c)):
        k = min(len(a), len(b))
        if k < fps:
            continue
        spec = []
        for e in (a[:k], b[:k]):
            e = e / (e.mean() + 1e-12) - 1
            s = np.abs(np.fft.rfft(e * np.hanning(k)))
            fq = np.fft.rfftfreq(k, 1 / fps)
            spec.append(s[(fq >= 0.5) & (fq <= 20)])
        sa, sb = spec
        out.append(np.mean(np.abs(sa - sb)) / (np.mean(sa) + np.mean(sb) + 1e-9))
    return float(np.mean(out)) if out else 0.0


def d_stereo(r, c):
    from scipy import signal
    out = []
    for lo, hi in BANDS4:
        sos = signal.butter(4, [lo, hi], btype="band", fs=SR, output="sos")
        feats = []
        for x in (r, c):
            y = signal.sosfilt(sos, x, axis=0)
            left, right = y[:, 0], y[:, 1]
            raw_ild = 10 * np.log10((left @ left + 1e-12) / (right @ right + 1e-12))
            ild = float(np.clip(raw_ild, -20, 20))   # lateralisation saturates by ~20 dB; pan +-1 zeroes a side (-230 dB)
            # one source panned hard is fully correlated; a near-silent side leaves the correlation undefined
            icc = 1.0 if abs(raw_ild) >= 30 else (left @ right) / (np.linalg.norm(left) * np.linalg.norm(right) + 1e-12)
            feats.append((icc, ild))
        (ia, la), (ib, lb) = feats
        out.append(abs(ia - ib) + abs(la - lb) / 6)
    return float(np.mean(out))


MONO_FAMILIES = ("bass", "vocals")


def score(ref, cand, mono=None):
    """{dimension: 0-100 (pitch None when the clip is not monophonic), 'total': weighted mean, 'raw': distances}.
    MONO: True/False forces whether pitch counts (a clip's family: bass and vocals); None decides by the share of
    voiced reference frames (pitch tracking a mixture is meaningless: the masking report read 0 on most clips)."""
    ref, cand = stereo2(ref), stereo2(cand)
    if len(ref) < SR // 2:
        raise ValueError("reference clip shorter than 0.5 s")
    if len(cand) < len(ref):                  # a render that stops early is scored as silence there, not trimmed away
        cand = np.concatenate([cand, np.zeros((len(ref) - len(cand), 2))])
    cand = cand[:len(ref)]
    cand = level_match(ref, align(ref, cand))
    rm, cm = ref.mean(1), cand.mean(1)
    raw = {"spectral": d_spectral(rm, cm), "timbre": d_timbre(rm, cm), "tone": d_tone(rm, cm),
           "modulation": d_modulation(rm, cm), "stereo": d_stereo(ref, cand)}
    dims = {k: 100 * np.exp(-v / SCALES[k]) for k, v in raw.items()}
    dims["transients"] = s_transients(rm, cm)
    dp, share = d_pitch(rm, cm, 0.1 if mono else 0.5) if mono is not False else (None, 0.0)
    raw["pitch"] = dp
    dims["pitch"] = None if dp is None else 100 * np.exp(-dp / SCALES["pitch"])
    w = {k: v for k, v in WEIGHTS.items() if dims[k] is not None}
    tot = sum(w[k] * dims[k] for k in w) / sum(w.values())
    out = {k: (round(float(v), 1) if v is not None else None) for k, v in dims.items()}
    out["total"] = round(float(tot), 2)
    out["voiced"] = round(share, 2)
    out["raw"] = {k: (round(float(v), 4) if v is not None else None) for k, v in raw.items()}
    return out


EXPLAIN_EDGES = (40, 80, 160, 320, 640, 1280, 2560, 5120, 10240, 16000)


def explain(ref, cand):
    """Where a clip's sound differs, per octave region (40 Hz-16 kHz), on the same aligned, level-matched pair score()
    uses: the reference's level (dB re its loudest region), our level difference, each band's level swing over time
    (std of its 46 ms frame level, dB: staccato chugs swing, a sustained wall doesn't) for both, and how well our band
    envelope follows the record's (correlation). Points timbre/tone work at a band (chirper-three, the riff screen)."""
    ref, cand = stereo2(ref), stereo2(cand)
    if len(cand) < len(ref):
        cand = np.concatenate([cand, np.zeros((len(ref) - len(cand), 2))])
    cand = level_match(ref, align(ref, cand[:len(ref)]))
    n = 2048
    R, C = stft_mag(ref.mean(1), n) ** 2, stft_mag(cand.mean(1), n) ** 2
    f = np.fft.rfftfreq(n, 1 / SR)
    rows = []
    for lo, hi in zip(EXPLAIN_EDGES[:-1], EXPLAIN_EDGES[1:]):
        k = (f >= lo) & (f < hi)
        er, ec = R[k].sum(0) + 1e-14, C[k].sum(0) + 1e-14                 # stft_mag: (bins, frames)
        lr, lc = 10 * np.log10(er), 10 * np.log10(ec)
        corr = float(np.corrcoef(lr, lc)[0, 1]) if lr.std() > 1e-6 and lc.std() > 1e-6 else 0.0
        rows.append({"band": f"{lo}-{hi}", "ref_db": float(10 * np.log10(er.mean())),
                     "diff_db": float(10 * np.log10(ec.mean() / er.mean())),
                     "ref_swing": float(lr.std()), "our_swing": float(lc.std()), "corr": corr})
    top = max(r["ref_db"] for r in rows)
    for r in rows:
        r["ref_db"] -= top

    def silent(x):                            # share of 20 ms frames more than 50 dB under the clip's loudest
        h = int(0.02 * SR)
        m = len(x) // h
        lv = 10 * np.log10((x[:m * h].mean(1).reshape(m, h) ** 2).mean(1) + 1e-14)
        return float(np.mean(lv < lv.max() - 50)) if m else 0.0
    return {"bands": rows, "silent_record": silent(ref), "silent_ours": silent(cand)}


def explain_text(ex):
    out = []
    if ex["silent_ours"] - ex["silent_record"] >= 0.2:
        out.append(f"    NOTES MISSING: ours is silent in {ex['silent_ours']:.0%} of 20 ms frames where the record is silent in "
                   f"{ex['silent_record']:.0%}; the score measures absent notes, not sound (check bandend.py / the map here)")
    out.append("    band Hz      record  ours-rec  swing rec/ours  env corr")
    for r in ex["bands"]:
        flag = "  <" if abs(r["diff_db"]) >= 6 or r["corr"] < 0.3 else ""
        out.append(f"    {r['band']:>11s} {r['ref_db']:6.1f}   {r['diff_db']:+6.1f}    {r['ref_swing']:5.1f}/{r['our_swing']:<5.1f}   "
                   f"{r['corr']:5.2f}{flag}")
    return "\n".join(out)


LEDGER = os.path.join(ROOT, "micro", "ledger.jsonl")


def ledger():
    if not os.path.exists(LEDGER):
        return []
    with open(LEDGER) as f:
        return [json.loads(x) for x in f if x.strip()]


def clips():
    p = os.path.join(ROOT, "micro", "clips.json")
    return json.load(open(p))["clips"] if os.path.exists(p) else []


def stem_audio(cid, spec):
    """A song's separated stem: FAMILY (ref/stems/htdemucs_6s/SONG/FAMILY.wav), STEM+STEM summed (a riff clip: the
    8-string's low register lands in demucs' bass stem), or a WAV path."""
    if spec.endswith(".wav"):
        if not os.path.exists(spec):
            raise SystemExit(f"microscore: no stem {spec}")
        return L.load(spec)
    xs = []
    for part in spec.split("+"):
        path = os.path.join(ROOT, "ref", "stems", "htdemucs_6s", cid, f"{part}.wav")
        if not os.path.exists(path):
            raise SystemExit(f"microscore: no stem {path}")
        xs.append(L.load(path))
    n = min(len(x) for x in xs)
    return sum(x[:n] for x in xs)


def clip_ref(cl):
    if str(cl.get("ref", "")).startswith("stems:"):        # a clip scored against summed stems, not the mix
        return cut(stem_audio(cl["song"], cl["ref"][len("stems:"):]), cl["from"], cl["to"])
    return cut(L.load(os.path.join(ROOT, "ref", f"{cl['song']}.wav")), cl["from"], cl["to"])


def render_window(song, t0, t1, seed=None, extra=()):
    import chirpbin
    with tempfile.TemporaryDirectory(dir="/tmp/lt" if os.path.isdir("/tmp/lt") else None) as d:
        out = os.path.join(d, "r.wav")
        sd = ["--seed", str(seed)] if seed is not None else []
        r = subprocess.run(["nice", "-n", "15", chirpbin.resolve("chirp"), "render", "-f", os.path.abspath(song), *sd, *extra,
                            "-o", out],
                           capture_output=True, text=True, stdin=subprocess.DEVNULL, cwd=os.path.dirname(os.path.abspath(song)),
                           env={**os.environ, "RAYON_NUM_THREADS": "2"})
        if r.returncode:
            raise SystemExit(f"microscore: render failed: {r.stderr.strip()[-300:]}")
        return cut(L.load(out), t0, t1)


def row(name, s):
    dims = " ".join(f"{k[:5]} {('  -' if s[k] is None else f'{s[k]:5.1f}')}" for k in WEIGHTS)
    return f"{name:34s} total {s['total']:6.2f} | {dims}"


def parse_section(spec):
    """'SONG:A-B' (seconds) -> (song, a, b)."""
    song, _, rng = spec.rpartition(":")
    a, _, b = rng.partition("-")
    if not song or not a or not b or float(b) <= float(a):
        raise SystemExit(f"microscore: --section wants SONG:A-B in seconds (got {spec!r})")
    return song, float(a), float(b)


def parse_try(spec):
    """'LABEL: PATH=V PATH=V' -> (label, [PATH=V, …])."""
    label, _, rest = spec.partition(":")
    sets = rest.split()
    if not label.strip() or not sets or any("=" not in x for x in sets):
        raise SystemExit(f"microscore: --try wants 'LABEL: PATH=V [PATH=V …]' (got {spec!r})")
    return label.strip(), sets


def render_range(song, t0, t1, seed=None, extra=()):
    """The song's t0..t1 s via chirp render --from/--to (bit-identical to cutting the full render)."""
    return render_window(song, None, None, seed, [*extra, "--from", f"{t0:g}s", "--to", f"{t1:g}s"])


@contextlib.contextmanager
def snapshot(song):
    """A private copy of SONG beside it (relative includes still resolve), deleted afterwards."""
    snap = tempfile.NamedTemporaryFile("w", dir=os.path.dirname(os.path.abspath(song)), prefix=".microscore-",
                                       suffix=".yaml", delete=False)
    with snap, open(song) as f:
        snap.write(f.read())
    try:
        yield snap.name
    finally:
        os.unlink(snap.name)


def section(a):
    cid, t0, t1 = parse_section(a.section)
    song = a.song_file or os.path.join(ROOT, "songs", f"{cid}.yaml")
    if a.stem:
        ref = cut(stem_audio(cid, a.stem), t0, t1)
    else:
        ref = cut(L.load(os.path.join(ROOT, "ref", f"{cid}.wav")), t0, t1)
    mono = a.mono or (a.stem in MONO_FAMILIES)
    solo = [x for t in (a.context or "").split(",") if t for x in ("--solo", t)]
    seeds = [int(x) for x in a.seeds.split(",") if x] if a.seeds else [None]
    variants = [("baseline", [])] + [parse_try(t) for t in a.tries]
    # one snapshot of the song for every variant and seed: the config checkout is shared, and a climber's commit
    # mid-run would otherwise split the comparison across versions (the-faultless v4 -> v5 landed during one, 26 Oct)
    with snapshot(song) as snap:
        out = section_runs(snap, variants, solo, a, ref, t0, t1, seeds, mono)
    report_section(a, cid, t0, t1, seeds, out)


def section_runs(song, variants, solo, a, ref, t0, t1, seeds, mono):
    out = []
    for label, sets in variants:
        extra = solo + [x for v in a.set + sets for x in ("--set", v)]
        renders = [render_range(song, t0, t1, k, extra) for k in seeds]
        per = [score(ref, x, mono=mono) for x in renders]
        r = mean_scores(per) if len(per) > 1 else per[0]
        if len(per) > 1:
            r["seeds"] = {str(k): x["total"] for k, x in zip(seeds, per)}
        if a.explain:
            r["explain"] = explain(ref, renders[0])
        out.append((label, sets, r))
    return out


def report_section(a, cid, t0, t1, seeds, out):
    if a.json:
        print(json.dumps({"section": a.section, "stem": a.stem, "context": a.context, "seeds": seeds,
                          "variants": [{"label": lb, "set": st, **r} for lb, st, r in out]}, indent=1))
        return
    base = out[0][2]["total"]
    what = f"{cid} {t0:g}-{t1:g} s" + (f", {a.context} soloed" if a.context else "") + \
        (f", against the {a.stem} stem" if a.stem else ", against the record's mix")
    print(f"{what}; seeds {','.join('-' if k is None else str(k) for k in seeds)}")
    for label, sets, r in out:
        delta = "" if label == "baseline" else f"  ({r['total'] - base:+.2f})"
        print(row(label[:34], r) + delta)
        if a.explain:
            print(explain_text(r["explain"]))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("files", nargs="*")
    ap.add_argument("--ref-from", type=float)
    ap.add_argument("--ref-to", type=float)
    ap.add_argument("--cand-from", type=float)
    ap.add_argument("--cand-to", type=float)
    ap.add_argument("--clip")
    ap.add_argument("--song")
    ap.add_argument("--mask", action="store_true")
    ap.add_argument("--clips")
    ap.add_argument("-j", type=int, default=3)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--context", metavar="TRACKS", help="with --clip: render the clip's ALBUM song (its master, buses and "
                    "lanes) with these tracks soloed (comma-separated) and score the clip window: patches judged in the "
                    "record's own master context")
    ap.add_argument("--set", action="append", default=[], metavar="PATH=V", help="--context: chirp render --set overrides "
                    "(e.g. tracks.3.patch=analog-bass)")
    ap.add_argument("--seeds", help="with --song: render these seeds (e.g. 0,3,7,11) and score their mean "
                    "(piano/guitar totals swing +-1-3 between seeds)")
    ap.add_argument("--record", metavar="NOTE")
    ap.add_argument("--as", dest="who", default=os.environ.get("CLIMB_AS") or os.environ.get("USER", "?"))
    ap.add_argument("--board", action="store_true")
    ap.add_argument("--section", metavar="SONG:A-B", help="any window of an album song (seconds); see the usage above")
    ap.add_argument("--stem", metavar="FAMILY|PATH", help="--section: score against this separated stem, not the mix")
    ap.add_argument("--song-file", help="--section: render this song file (a variant) instead of songs/SONG.yaml")
    ap.add_argument("--try", dest="tries", action="append", default=[], metavar="'LABEL: PATH=V …'",
                    help="--section: a variant's --set overrides, scored on the same seeds against the baseline")
    ap.add_argument("--mono", action="store_true", help="--section: score pitch (monophonic part)")
    ap.add_argument("--explain", action="store_true", help="--section / --clip --context: per octave region, our level "
                    "difference, level swing and envelope correlation against the record (the first seed's render)")
    a = ap.parse_args(argv)
    if a.section:
        if a.record is not None:
            raise SystemExit("microscore: --section is never recorded (the ledger is the benchmark's)")
        return section(a)
    if a.board:
        best = {}
        for e in ledger():
            if e["clip"] not in best or e["total"] > best[e["clip"]]["total"]:
                best[e["clip"]] = e
        for cl in clips():
            e = best.get(cl["id"])
            tag = "HOLDOUT " if cl.get("holdout") else ""
            print(f"{cl['id']:44s} {cl['family']:7s} {tag:8s}" + (f"best {e['total']:6.2f} by {e['who']} ({e['at'][:16]}): {e['note'][:60]}"
                                                                    if e else "—"))
        return
    if a.mask:
        from concurrent.futures import ThreadPoolExecutor
        want = {x for x in (a.clips or "").split(",") if x}
        cs = [c for c in clips() if not want or c["id"] in want]
        reg = {c["id"]: c for c in json.load(open(os.path.join(ROOT, "climbs.json")))["climbs"]}

        def one(cl):
            song = os.path.join(ROOT, "songs", f"{cl['song']}.yaml")
            if not os.path.exists(song):
                return cl, None
            try:
                return cl, score(clip_ref(cl), render_window(song, cl["from"], cl["to"]), mono=cl["family"] in MONO_FAMILIES)
            except (ValueError, SystemExit) as e:
                return cl, {"error": str(e)[:160]}
        with ThreadPoolExecutor(max(1, a.j)) as ex:
            res = list(ex.map(one, cs))
        if a.json:
            print(json.dumps({cl["id"]: s for cl, s in res}, indent=1))
            return
        for cl, s in res:
            g = (reg.get(cl["song"], {}).get("best") or {}).get("score")
            if not s or "error" in s:
                print(f"{cl['id']}: {s['error'] if s else 'no song'}")
                continue
            print(row(f"{cl['id']} ({cl['family']})", s) + f" | song best {g}")
        return
    if a.clip:
        cl = next((c for c in clips() if c["id"] == a.clip), None)
        if not cl:
            raise SystemExit(f"microscore: no clip {a.clip} in micro/clips.json")
        ref = clip_ref(cl)
        if a.context:
            song = os.path.join(ROOT, "songs", f"{cl['song']}.yaml")
            extra = [x for t in a.context.split(",") if t for x in ("--solo", t)] + [x for v in a.set for x in ("--set", v)]
            mono = cl["family"] in MONO_FAMILIES
            seeds = [int(x) for x in a.seeds.split(",") if x] if a.seeds else [None]
            with snapshot(song) as snap:                 # one version for every seed (the checkout is shared)
                renders = [(k, render_window(snap, cl["from"], cl["to"], k, extra)) for k in seeds]
            per = [(k, score(ref, x, mono=mono)) for k, x in renders]
            s = mean_scores([r for _, r in per]) if len(per) > 1 else per[0][1]
            if len(per) > 1:
                s["seeds"] = {str(k): r["total"] for k, r in per}
            a.song = f"context:{cl['song']}:{a.context}" + (f" {' '.join(a.set)}" if a.set else "")
            print(json.dumps(s) if a.json else row(f"{a.clip} (in context)", s))
            if a.explain and not a.json:
                print(explain_text(explain(ref, renders[0][1])))
            record(a, cl, s)
            return
        if a.song and a.seeds:
            mono = cl["family"] in MONO_FAMILIES
            per = [(int(x), score(ref, render_window(a.song, None, None, int(x)), mono=mono)) for x in a.seeds.split(",") if x]
            s = mean_scores([r for _, r in per])
            s["seeds"] = {str(k): r["total"] for k, r in per}
            if not a.json:
                for k, r in per:
                    print(row(f"  seed {k}", r))
            print(json.dumps(s) if a.json else row(f"{a.clip} (mean of {len(per)})", s))
            record(a, cl, s)
            return
        cand = render_window(a.song, None, None) if a.song else cut(L.load(a.files[0]), a.cand_from, a.cand_to)
    else:
        if len(a.files) != 2:
            ap.error("REF.wav CAND.wav, or --clip ID")
        ref = cut(L.load(a.files[0]), a.ref_from, a.ref_to)
        cand = cut(L.load(a.files[1]), a.cand_from, a.cand_to)
    s = score(ref, cand, mono=(cl["family"] in MONO_FAMILIES) if a.clip else None)
    print(json.dumps(s) if a.json else row(a.clip or os.path.basename(a.files[1]), s))
    if a.record is not None:
        if not a.clip:
            raise SystemExit("microscore: --record needs --clip")
        record(a, cl, s)


def mean_scores(rs):
    """The per-dimension mean of several score() results (pitch None when any is None)."""
    out = {}
    for k in list(WEIGHTS) + ["total", "voiced"]:
        vals = [r[k] for r in rs]
        out[k] = None if any(v is None for v in vals) else round(float(np.mean(vals)), 2)
    return out


def record(a, cl, s):
    if a.record is None:
        return
    prev = max((e["total"] for e in ledger() if e["clip"] == a.clip), default=None)
    import time
    e = {"clip": a.clip, "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "who": a.who, "note": a.record,
         "song": a.song, **{k: v for k, v in s.items() if k != "raw"}}
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    with open(LEDGER, "a") as f:
        f.write(json.dumps(e) + "\n")
    print(f"recorded: {s['total']:.2f}" + (f" (best was {prev:.2f}: {'NEW BEST' if s['total'] > prev else 'no gain'})"
                                           if prev is not None else " (first)"))


if __name__ == "__main__":
    main()
