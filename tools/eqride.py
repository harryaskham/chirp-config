#!/usr/bin/env python3
"""EQ ride: the spectral counterpart of levelride.py. The section EQ (sectioneq.py lanes auto.eq0..6) fixes each
section's average balance; the record's balance still moves within sections (parts entering, a build opening up,
transitions), and the metric compares 2 s windows. Per window, the residual difference between a render of the
map and the reference (1/3-octave, level-normalised) is fitted to the master EQ's bands (sectioneq.py's exact
biquad responses), median-smoothed, scaled and clamped, and added to the existing lanes as time-varying points.

  eqride.py MAP.json REF.wav RENDER.wav [--win 4] [--scale 0.6] [--max 4] [--from S] [--to S] [--skip A-B,C-D]
           [-o OUT.json]

Skip sections where the arrangement still differs from the record (Pneuma's hold and intro lost with the ride:
an EQ chasing content we do not play).

RENDER.wav must be a render of MAP.json (its lanes are the base the residual is added to). Re-run after mix
changes; compare with the same protocol as other mastering changes."""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import likeness as L  # noqa: E402
import sectioneq as Q  # noqa: E402


def lane_at(points, t):
    ts = np.array([float(p[0].rstrip("s")) for p in points]); vs = np.array([p[1] for p in points], dtype=float)
    return float(np.interp(t, ts, vs))


def main(a):
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    mp = json.load(open(a[0])); ref = L.load(a[1]).mean(1); cand = L.load(a[2]).mean(1)
    win, scale, mx = opt("--win", 4.0), opt("--scale", 0.6), opt("--max", 4.0)
    t_lo, t_hi = opt("--from", 0.0), opt("--to", 1e9)
    skips = [tuple(float(v) for v in r.split("-")) for r in opt("--skip", "").split(",") if r]
    lanes = mp["head"]["master"]["auto"]
    names = [f"eq{k}" for k in range(len(Q.BANDS))]
    n = int(min(len(ref), len(cand)) / Q.SR / win)
    centers, G = [], []
    for k in range(n):
        s0 = k * win; c = s0 + win / 2
        r, x = ref[int(s0 * Q.SR):int((s0 + win) * Q.SR)], cand[int(s0 * Q.SR):int((s0 + win) * Q.SR)]
        g = np.zeros(len(Q.BANDS))
        if t_lo <= c <= t_hi and not any(a_ <= c <= b_ for a_, b_ in skips) and 10 * np.log10(np.mean(r ** 2) + 1e-12) > -50 and 10 * np.log10(np.mean(x ** 2) + 1e-12) > -50:
            dev = Q.third_octave(x) - Q.third_octave(r)
            dev = dev - dev.mean()
            g = Q.fit(dev, mx=9.0)
        centers.append(c); G.append(g)
    G = np.array(G)
    Gs = np.array([np.median(G[max(0, k - 1):k + 2], axis=0) for k in range(len(G))])
    Gs = np.clip(Gs * scale, -mx, mx)
    for j, nm in enumerate(names):
        if nm not in lanes:
            continue
        base = lanes[nm]["points"]
        pts = [["0s", round(lane_at(base, 0.0) + float(Gs[0, j]), 2)]]
        pts += [[f"{c:.2f}s", round(lane_at(base, c) + float(Gs[k, j]), 2)] for k, c in enumerate(centers)]
        end = float(base[-1][0].rstrip("s"))
        if end > centers[-1]:
            pts.append([f"{end:.2f}s", round(lane_at(base, end) + float(Gs[-1, j]), 2)])
        lanes[nm]["points"] = pts
    json.dump(mp, open(opt("-o", a[0]), "w"), indent=1)
    print(f"{len(centers)} windows of {win:.0f} s; residual |g| mean {np.abs(Gs).mean():.2f} dB, max {np.abs(Gs).max():.1f} dB")


if __name__ == "__main__":
    main(sys.argv[1:])
