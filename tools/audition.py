#!/usr/bin/env python3
"""audition: one part, soloed over a time range, against its stem — the quick loop for patch and part design.

  audition.py SONG TRACK[,TRACK…] STEM.wav --from A --to B [--seed S] [--set PATH=VALUE …] [--keep OUT.wav] [--json]
  audition.py --wav OURS.wav STEM.wav --from A --to B [--json]     (compare a render you already have)

Renders SONG with `chirp render --solo TRACK --from As --to Bs` (state-exact: notes started before A sound as in the
full render; ~5 s for a 10 s window) and compares it with the stem over the same span:

  level     RMS dB of each (ours - stem)
  envelope  third-octave band levels 40 Hz-16 kHz as shares of each signal's total, and the bands that differ most
            (positive = ours has more there: EQ, filter, brightness)
  centroid  median spectral centroid (brightness)
  width     side/mid energy ratio in dB (stereo spread)
  onsets    onsets per second, and the median decay to -20 dB after each onset (ms; notes cut by the next onset
            are left out) — articulation and envelope
  notes     noteacc's local pitch and timing on the excerpt (0 = chance, 100 = identical): wrong notes, late notes

Stems are full-length and aligned with the reference (ref/stems/htdemucs_6s/ID/{drums,bass,guitar,vocals,piano,
other}.wav); a separated stem carries some bleed, so read small differences loosely. Uses the groove pin
(tools/groove-pin) unless $CHIRP is set.
"""
import json
import os
import subprocess
import sys
import tempfile

import numpy as np
from scipy import signal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chirpbin  # noqa: E402
import noteacc  # noqa: E402
from likeness import SR, load  # noqa: E402

CENTRES = 1000 * 2 ** (np.arange(-14, 13) / 3)        # third octaves 62.5 Hz … 16 kHz (around 1 kHz)
CENTRES = CENTRES[(CENTRES >= 40) & (CENTRES <= 16000)]


def bands_db(x):
    """Third-octave band levels (dB) of mono x from a Welch spectrum (exact bins, no filter leakage)."""
    f, p = signal.welch(x, SR, nperseg=8192)
    out = []
    for c in CENTRES:
        sel = (f >= c / 2 ** (1 / 6)) & (f < c * 2 ** (1 / 6))
        out.append(10 * np.log10(p[sel].sum() + 1e-20))
    return np.array(out)


def centroid(x):
    f, _, Z = signal.stft(x, SR, nperseg=2048, noverlap=1536)
    m = np.abs(Z)
    e = m.sum(0)
    c = (f[:, None] * m).sum(0) / np.maximum(e, 1e-12)
    loud = e > np.percentile(e, 50) if e.size else e
    return float(np.median(c[loud])) if loud.any() else float("nan")


def width_db(st):
    mid, side = (st[:, 0] + st[:, 1]) / 2, (st[:, 0] - st[:, 1]) / 2
    return float(10 * np.log10((side ** 2).sum() / max((mid ** 2).sum(), 1e-20) + 1e-12))


def articulation(x):
    """(onsets per second, median ms to fall 20 dB after an onset, onsets measured)."""
    fl = noteacc.flux(x.astype(np.float32)).sum(0)
    on = noteacc.onsets(fl)
    hop = 0.005
    n = int(hop * SR)
    env = np.sqrt(np.convolve(x.astype(np.float64) ** 2, np.ones(n) / n, mode="same")[::n] + 1e-20)
    env_db = 20 * np.log10(env)
    decays = []
    for i, t in enumerate(on):
        a = int(t / hop)
        nxt = int(on[i + 1] / hop) if i + 1 < len(on) else len(env_db)
        if a >= len(env_db) - 2:
            continue
        pk = a + int(np.argmax(env_db[a:min(a + int(0.05 / hop), nxt)])) if nxt > a else a
        below = np.nonzero(env_db[pk:nxt] < env_db[pk] - 20)[0]
        if len(below):
            decays.append(below[0] * hop * 1000)
    dur = len(x) / SR
    return len(on) / dur if dur else 0.0, (float(np.median(decays)) if decays else None), len(decays)


def compare(stem, ours):
    """Stereo arrays over the same span → the report dict (pure: no rendering)."""
    n = min(len(stem), len(ours))
    stem, ours = stem[:n], ours[:n]
    xs, xo = stem.mean(1), ours.mean(1)
    rms = lambda x: 20 * np.log10(np.sqrt((x.astype(np.float64) ** 2).mean()) + 1e-12)  # noqa: E731
    bs, bo = bands_db(xs), bands_db(xo)
    share = lambda b: b - 10 * np.log10((10 ** (b / 10)).sum())   # each band's share of the total, dB  # noqa: E731
    rel = share(bo) - share(bs)
    audible = (bs > bs.max() - 50) | (bo > bo.max() - 50)
    order = [i for i in np.argsort(-np.abs(rel)) if audible[i]][:5]
    rs, ds, ns = articulation(xs)
    ro, do, no_ = articulation(xo)
    P = noteacc.Pair(stem, ours)
    p, t = P.pitch(), P.timing()
    return {
        "seconds": round(n / SR, 3),
        "level_db": {"stem": round(rms(xs), 2), "ours": round(rms(xo), 2), "diff": round(rms(xo) - rms(xs), 2)},
        "envelope": {"bands_hz": [round(float(c)) for c in CENTRES], "diff_db": [round(float(v), 1) for v in rel],
                     "largest": [{"hz": round(float(CENTRES[i])), "diff_db": round(float(rel[i]), 1)} for i in order]},
        "centroid_hz": {"stem": round(centroid(xs)), "ours": round(centroid(xo))},
        "width_db": {"stem": round(width_db(stem), 1), "ours": round(width_db(ours), 1)},
        "onsets_per_s": {"stem": round(rs, 2), "ours": round(ro, 2)},
        "decay20_ms": {"stem": ds and round(ds), "ours": do and round(do), "measured": [ns, no_]},
        "notes": {"pitch": p.get("score"), "timing": t.get("score"), "offset_ms": t.get("offset_ms_median")},
    }


def render(song, tracks, a, b, seed, sets, out):
    cmd = [chirpbin.resolve("chirp"), "render", "-f", song, "--from", f"{a}s", "--to", f"{b}s", "-o", out]
    for tr in tracks:
        cmd += ["--solo", tr]
    if seed is not None:
        cmd += ["--seed", str(seed)]
    for s in sets:
        cmd += ["--set", s]
    r = subprocess.run(["nice", "-n", "12", *cmd], capture_output=True, text=True, stdin=subprocess.DEVNULL)
    if r.returncode or not os.path.exists(out):
        raise SystemExit(f"audition: render failed: {r.stderr.strip()[-400:]}")


def report(r):
    L, E = r["level_db"], r["envelope"]
    print(f"{r['seconds']} s   level ours {L['ours']} dB vs stem {L['stem']} dB ({L['diff']:+} dB)")
    print("envelope (ours - stem, each band's share of its total): "
          + ", ".join(f"{e['hz']} Hz {e['diff_db']:+}" for e in E["largest"]))
    print(f"centroid ours {r['centroid_hz']['ours']} Hz vs stem {r['centroid_hz']['stem']} Hz   "
          f"width ours {r['width_db']['ours']} dB vs stem {r['width_db']['stem']} dB (side/mid)")
    print(f"onsets/s ours {r['onsets_per_s']['ours']} vs stem {r['onsets_per_s']['stem']}   decay to -20 dB ours "
          f"{r['decay20_ms']['ours']} ms vs stem {r['decay20_ms']['stem']} ms")
    n = r["notes"]
    print(f"notes: pitch {n['pitch']}  timing {n['timing']}  (0 = chance, 100 = identical; offset {n['offset_ms']} ms)")


def main(argv):
    a = list(argv)

    def opt(flag, default=None, many=False):
        vals = []
        while flag in a:
            i = a.index(flag)
            vals.append(a[i + 1])
            del a[i:i + 2]
        return vals if many else (vals[-1] if vals else default)

    as_json = "--json" in a
    a = [x for x in a if x != "--json"]
    ours_wav, keep = opt("--wav"), opt("--keep")
    t0, t1 = opt("--from"), opt("--to")
    seed, sets = opt("--seed"), opt("--set", many=True)
    if t0 is None or t1 is None:
        raise SystemExit(__doc__.strip().splitlines()[2])
    t0, t1 = float(t0.rstrip("s")), float(t1.rstrip("s"))
    if ours_wav:
        stem_path = a[0]
        ours = load(ours_wav)
        ours = ours[int(t0 * SR):int(t1 * SR)] if len(ours) / SR > (t1 - t0) + 0.5 else ours
    else:
        if len(a) < 3:
            raise SystemExit(__doc__.strip().splitlines()[2])
        song, tracks, stem_path = a[0], a[1].split(","), a[2]
        out = keep or tempfile.mktemp(suffix=".wav", prefix="audition-", dir="/tmp/lt" if os.path.isdir("/tmp/lt") else None)
        try:
            render(song, tracks, t0, t1, seed, sets, out)
            ours = load(out)
        finally:
            if not keep and os.path.exists(out):
                os.remove(out)
    stem = load(stem_path)[int(t0 * SR):int(t1 * SR)]
    res = compare(stem, ours)
    if as_json:
        print(json.dumps(res))
    else:
        report(res)


if __name__ == "__main__":
    main(sys.argv[1:])
