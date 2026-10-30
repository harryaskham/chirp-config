#!/usr/bin/env python3
"""levels: clipping and loudness for a render (chirp-eco; compscore plugin, compose/measures/).

Harry, 30 Oct: "some of our bass hits sound clipped". compscore's master term only checks the sample peak, which the
master limiter caps, so flat-topped kicks and inter-sample overs went unseen. This measures them with tools/levels.py
(ITU-R BS.1770-4 loudness, 4x oversampled true peak, flat-topped runs):

  score = 100 - 15 per dB of true peak above -1 dBTP - 5 per pinned sample beyond 3 in the longest flat run (>= 0)

so a clean master (TP <= -1 dBTP, no run of 4+ samples within 0.01 dB of the peak) scores 100, and No Floor v5
(TP -0.02, run 53) scores 0. Detail: true peak, longest pinned run, integrated LUFS, PLR.

Detail-only until the album sets a weight (the metric is the composers', Harry 30 Oct): with no `levels` key in
album.json weights the result carries weight_scale 0 (shown in --text, not counted in the total).

  python3 compose/measures/levels.py WAV        measure one render
"""
import os
import sys

import numpy as np

ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import levels as LV  # noqa: E402


def analyse(x, sr):
    x = x.astype(np.float64)
    a = np.abs(x)
    peak = float(a.max()) or 1e-12
    pinned = a >= peak * 10 ** (-0.01 / 20)
    run = max(LV.longest_run(pinned[:, c]) for c in range(x.shape[1])) if x.ndim > 1 else LV.longest_run(pinned)
    tp = 20 * np.log10(LV.true_peak(x) or 1e-12)
    lufs, _ = LV.loudness(x, sr)
    score = max(0.0, 100.0 - 15.0 * max(0.0, tp + 1.0) - 5.0 * max(0, run - 3))
    return {"true_peak_dbtp": round(tp, 2), "longest_pinned_run": int(run), "lufs": round(lufs, 1),
            "plr": round(tp - lufs, 1), "score": round(score, 1)}


def measure(ctx):
    import likeness as L
    d = analyse(ctx["x"], L.SR)
    if "levels" not in ((ctx.get("album") or {}).get("weights") or {}):
        d["weight_scale"] = 0.0  # detail-only until the album gives it a weight
    return d["score"], d


if __name__ == "__main__":
    import likeness as L
    for w in sys.argv[1:]:
        print(w, analyse(L.load(w), L.SR))
