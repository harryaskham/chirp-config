#!/usr/bin/env python3
"""endlane: match a song's ending to the record's level with one master gain lane (chirper-zero's tool, promoted).

  endlane.py SONG.yaml OUT.yaml REF.wav OURS.wav FROM [--step 0.2] [--lo -25] [--hi 20] [--lane cut]

OURS.wav is a render of SONG (seed 0). From FROM seconds on, the lane is the record's level minus ours per STEP
seconds (median of 3, clipped LO..HI dB), applied by a gain stage appended after the master chain. Ride lanes lift
tails, so a lane fitted on the real render beats a designed fade. Results: I Am That Thirst v13 +0.31 every seed
(last section 60 -> 67), Lethargica v9 +0.25, obZen v3 (last section 59 -> 64, the join into This Spiteful Snake
34.6 -> 42.1). The record's band stop is a good FROM (albumedges / the record's level curve).
"""
import argparse
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def lane_points(ref, ours, sr, start, step=0.2, lo=-25.0, hi=20.0):
    """(points, per-step dB) for mono REF and OURS: the record's level minus ours per STEP from START, median of 3,
    clipped LO..HI; points hold 0 dB until just before START and the last value past the end."""
    from scipy.signal import medfilt
    end = min(len(ref), len(ours)) / sr

    def lv(x, t):
        return 20 * np.log10(np.sqrt(np.mean(x[int(t * sr):int((t + step) * sr)] ** 2)) + 1e-9)
    ts = np.arange(start, end - step / 2, step)
    d = np.clip(medfilt(np.array([lv(ref, t) - lv(ours, t) for t in ts]), 3), lo, hi)
    pts = ([["0s", 0], [f"{start - 0.1:.2f}s", 0]] + [[f"{t + step / 2:.2f}s", round(float(v), 1)] for t, v in zip(ts, d)]
           + [[f"{end + 0.5:.2f}s", round(float(d[-1]), 1)]])
    return pts, d


def apply_lane(song, lane, pts):
    """Append a master gain stage driven by auto.LANE (refused if the lane exists)."""
    if lane in (song["master"].get("auto") or {}):
        raise SystemExit(f"endlane: master lane {lane!r} exists; pass --lane NAME")
    song["master"]["fx"].append({"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto." + lane, "amount": 1}]}})
    song["master"].setdefault("auto", {})[lane] = {"points": pts}
    return song


def main(argv=None):
    import likeness as L
    import songfmt
    import tab2song as T
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("song")
    ap.add_argument("out")
    ap.add_argument("ref")
    ap.add_argument("ours")
    ap.add_argument("start", type=float)
    ap.add_argument("--step", type=float, default=0.2)
    ap.add_argument("--lane", default="cut")
    ap.add_argument("--lo", type=float, default=-25)
    ap.add_argument("--hi", type=float, default=20)
    a = ap.parse_args(argv)
    r = L.load(a.ref).astype(float).mean(1)
    o = L.load(a.ours).astype(float).mean(1)
    pts, d = lane_points(r, o, L.SR, a.start, a.step, a.lo, a.hi)
    s = apply_lane(songfmt.load(a.song), a.lane, pts)
    open(a.out, "w").write(T.dump(s))
    print("lane", [round(float(v), 1) for v in d])


if __name__ == "__main__":
    main()
