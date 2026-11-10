#!/usr/bin/env python3
"""limwork: how much of a song's mastering is the final limiter doing, and where (chirper-one, 10 Nov).

  limwork.py RAW.wav FINAL.wav [name:sec,name:sec,…] [--strip SEC] [--json]
  limwork.py --song songs/ID.yaml [--seed 0] [--threads 4] [name:sec,…]      renders both itself (two full renders)

RAW is the song rendered with `--set loudness=null` (the mix as the master chain leaves it); FINAL is the normal
render (loudness normalised, then held under the ceiling). A song's master fx run BEFORE the loudness stage, so a
master compressor with its threshold at -18 dB never moves on a mix that sits at -25 dBFS RMS, the loudness stage
then adds 12-15 dB, and the final limiter is left to do everything a mastering chain should - in a few ms, on the
loudest section only. This tool measures that: the gain from RAW to FINAL in 5 ms windows; its 97th percentile is
the static (loudness) gain, and whatever sits below it is gain reduction by the limiter.

It prints, for the whole song and for each named section (name:start-seconds, in order; the last runs to the
end): the mean reduction, its median, 10th and 1st percentiles and its deepest point, and the share of the time the
limiter is pulling more than 1, 3 and 6 dB. --strip SEC draws four seconds of the reduction from SEC (one character
per 20 ms, one step per dB), which shows whether it is single hits or a held squeeze.

Reading it: a mean under 0.5 dB with a few percent over 3 dB is a limiter catching peaks, as it should. A section
with a mean of 2-3 dB and a third or more of its time over 3 dB is being mastered by the limiter: its drums are
ducking the whole mix on every hit, and its loudness against the quiet sections is smaller than the lanes say. The
remedies are upstream: tame the peakiest tracks at their source (solo renders show which; a gong, a snare and a
choir's consonants are usual), give the master compressor a threshold the mix actually reaches (or a pre-gain
ahead of it), and let the climax be loud by density and width rather than by peak level.

Measured when written (t6 Spring Tide v107, seed 0): static gain +14.4 dB; the crest held down 2.9 dB on average,
over 3 dB for 45% of the time, 10.3 dB at its deepest; the torn 2.0 dB; the in-seam, the tide and the cross 0.0-0.1.

Use whole-song renders: a window rendered with --from/--to is normalised to its own loudness, so its static gain
and its reduction are not the song's (t6's crest alone reads +9.9 dB and 0.5 dB; in the whole song +14.4 and 2.9).

Not a score and not an ear. Read-only on the song. The two renders must be the same seed and length.
"""
import json
import os
import subprocess
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
WIN = 0.005


def rd(path, sr=44100):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-f", "f32le", "-ac", "2", "-ar", str(sr), "-"],
                         capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64).reshape(-1, 2), sr


def render_pair(song, seed, threads):
    pin = open(os.path.join(HERE, "groove-pin")).read().strip()
    d = tempfile.mkdtemp(prefix="limwork-")
    env = {k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"}
    out = []
    for name, extra in (("raw", ["--set", "loudness=null"]), ("final", [])):
        w = os.path.join(d, f"{name}.wav")
        r = subprocess.run([pin, "render", "-f", song, "-o", w, "--seed", str(seed), "--threads", str(threads)] + extra,
                           capture_output=True, env=env)
        if r.returncode != 0 or not os.path.exists(w):
            sys.exit(f"limwork: the {name} render failed: {r.stderr.decode()[-300:]}")
        out.append(w)
    return out


def measure(raw, fin, secs):
    a, sr = rd(raw)
    b, _ = rd(fin)
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    w = int(WIN * sr)
    k = n // w
    ra = np.sqrt((a[:k * w].reshape(k, w, 2) ** 2).mean((1, 2)) + 1e-14)
    rb = np.sqrt((b[:k * w].reshape(k, w, 2) ** 2).mean((1, 2)) + 1e-14)
    ok = ra > ra.max() * 10 ** (-45 / 20)          # windows with signal: silence has no gain to read
    g = 20 * np.log10(rb / ra)
    g0 = float(np.percentile(g[ok], 97))

    def row(name, i0, i1):
        gg = g[i0:i1][ok[i0:i1]] - g0
        if len(gg) < 10:
            return None
        return {"name": name, "mean_db": round(float(gg.mean()), 2), "p50_db": round(float(np.percentile(gg, 50)), 2),
                "p10_db": round(float(np.percentile(gg, 10)), 2), "p1_db": round(float(np.percentile(gg, 1)), 2),
                "min_db": round(float(gg.min()), 2), "over_1db": round(float((gg < -1).mean()), 3),
                "over_3db": round(float((gg < -3).mean()), 3), "over_6db": round(float((gg < -6).mean()), 3)}

    rows = [row("whole", 0, k)]
    for i, (name, t0) in enumerate(secs):
        t1 = secs[i + 1][1] if i + 1 < len(secs) else n / sr
        rows.append(row(name, int(t0 / WIN), int(t1 / WIN)))
    db = lambda v: round(float(20 * np.log10(v + 1e-14)), 1)
    return {"static_gain_db": round(g0, 2),
            "raw": {"rms_db": db(np.sqrt((a ** 2).mean())), "peak_db": db(np.abs(a).max())},
            "final": {"rms_db": db(np.sqrt((b ** 2).mean())), "peak_db": db(np.abs(b).max())},
            "rows": [r for r in rows if r]}, g - g0


def main(argv):
    opt = {"--strip": None, "--song": None, "--seed": "0", "--threads": "4"}
    pos, as_json, i = [], False, 0
    while i < len(argv):
        if argv[i] in opt:
            opt[argv[i]] = argv[i + 1]
            i += 2
        elif argv[i] == "--json":
            as_json = True
            i += 1
        elif argv[i] in ("-h", "--help"):
            print(__doc__)
            return 0
        else:
            pos.append(argv[i])
            i += 1
    if opt["--song"]:
        raw, fin = render_pair(opt["--song"], opt["--seed"], opt["--threads"])
    elif len(pos) >= 2:
        raw, fin, pos = pos[0], pos[1], pos[2:]
    else:
        print(__doc__)
        return 2
    secs = [(s.split(":")[0], float(s.split(":")[1])) for s in pos[0].split(",")] if pos else []
    res, red = measure(raw, fin, secs)
    if as_json:
        print(json.dumps(res))
        return 0
    print(f"static gain (P97) {res['static_gain_db']:+.1f} dB; raw rms {res['raw']['rms_db']} peak {res['raw']['peak_db']} dBFS; "
          f"final rms {res['final']['rms_db']} peak {res['final']['peak_db']} dBFS")
    print(f"  {'section':10s} {'mean':>6s} {'P50':>6s} {'P10':>6s} {'P1':>6s} {'min':>6s}   time over 1 / 3 / 6 dB")
    for r in res["rows"]:
        print(f"  {r['name']:10s} {r['mean_db']:6.1f} {r['p50_db']:6.1f} {r['p10_db']:6.1f} {r['p1_db']:6.1f} {r['min_db']:6.1f}"
              f"   {100 * r['over_1db']:3.0f}% {100 * r['over_3db']:3.0f}% {100 * r['over_6db']:3.0f}%")
    if opt["--strip"] is not None:
        t0 = float(opt["--strip"])
        seg = red[int(t0 / WIN):int((t0 + 4) / WIN)]
        print(f"gain reduction {t0:g}-{t0 + 4:g} s (one step per dB, 20 ms per character):")
        print("".join(" .:-=+*#%@"[min(9, int(-min(0.0, seg[j:j + 4].min())))] for j in range(0, len(seg), 4)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
