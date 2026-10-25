#!/usr/bin/env python3
"""microscore: how closely a short clip (1-10 s) reproduces the record LOCALLY, by signal measures only (Harry, 25 Oct:
a micro benchmark that sees sound, not song shape: where our songs lean on global metrics to hide bad local sound).

  microscore.py REF.wav CAND.wav [--ref-from S --ref-to S] [--cand-from S --cand-to S] [--json]
  microscore.py --clip ID CAND.wav | --clip ID --song SONG.yaml        (a clip from micro/clips.json)
  microscore.py --mask [--clips a,b] [-j 3]          each clip's song's current render over the same window
  microscore.py --clip ID --song micro/songs/ID.yaml [--seeds 0,3,7,11] --record NOTE [--as WHO]   (ledger)
  microscore.py --board                              the best recorded total per clip (holdouts marked)

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


LEDGER = os.path.join(ROOT, "micro", "ledger.jsonl")


def ledger():
    if not os.path.exists(LEDGER):
        return []
    with open(LEDGER) as f:
        return [json.loads(x) for x in f if x.strip()]


def clips():
    p = os.path.join(ROOT, "micro", "clips.json")
    return json.load(open(p))["clips"] if os.path.exists(p) else []


def clip_ref(cl):
    return cut(L.load(os.path.join(ROOT, "ref", f"{cl['song']}.wav")), cl["from"], cl["to"])


def render_window(song, t0, t1, seed=None):
    import chirpbin
    with tempfile.TemporaryDirectory(dir="/tmp/lt" if os.path.isdir("/tmp/lt") else None) as d:
        out = os.path.join(d, "r.wav")
        sd = ["--seed", str(seed)] if seed is not None else []
        r = subprocess.run(["nice", "-n", "15", chirpbin.resolve("chirp"), "render", "-f", os.path.abspath(song), *sd, "-o", out],
                           capture_output=True, text=True, stdin=subprocess.DEVNULL, cwd=os.path.dirname(os.path.abspath(song)),
                           env={**os.environ, "RAYON_NUM_THREADS": "2"})
        if r.returncode:
            raise SystemExit(f"microscore: render failed: {r.stderr.strip()[-300:]}")
        return cut(L.load(out), t0, t1)


def row(name, s):
    dims = " ".join(f"{k[:5]} {('  -' if s[k] is None else f'{s[k]:5.1f}')}" for k in WEIGHTS)
    return f"{name:34s} total {s['total']:6.2f} | {dims}"


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
    ap.add_argument("--seeds", help="with --song: render these seeds (e.g. 0,3,7,11) and score their mean "
                    "(piano/guitar totals swing +-1-3 between seeds)")
    ap.add_argument("--record", metavar="NOTE")
    ap.add_argument("--as", dest="who", default=os.environ.get("CLIMB_AS") or os.environ.get("USER", "?"))
    ap.add_argument("--board", action="store_true")
    a = ap.parse_args(argv)
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
