#!/usr/bin/env python3
"""Fader ride for a tab2song map: follow the reference's macro-dynamics. Short-term loudness of the reference and of
a render of the map are compared (high-passed RMS, smoothed over --win seconds); the difference becomes a master gain
automation lane (auto.ride, after the master EQ, before the song ceiling), clamped to ±--max dB and median-filtered so
it moves like a hand on a fader, not a compressor. Re-run after arrangement or mix changes (it follows the render).

  levelride.py MAP.json REF.wav RENDER.wav[,RENDER2,...] [--win 4] [--step 2] [--max 9] [--amount 1.0] [-o OUT.json]

--amount scales the correction (0.5 = halfway). --contour --sections F removes each section's mean correction, so the
ride only shapes loudness within sections (set section levels separately, e.g. a master envelope). Existing auto.ride is replaced; the render should have been made
without it (or pass --accumulate to add to the existing lane). Several renders (comma-separated: the same
song at different seeds) average their loudness, so the ride doesn't learn one seed's draws (a 0.5 s ride fitted
to the default seed was ~0.7 of Laid to Rest's seed-overfit)."""
import json
import sys
import os

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import likeness as L  # noqa: E402

SR = 48000


def loud(x, win, step):
    x = x.mean(1) if x.ndim > 1 else x
    # one-pole high-pass at ~60 Hz so sub energy doesn't dominate the ride
    a = np.exp(-2 * np.pi * 60 / SR)
    from scipy.signal import lfilter
    y = lfilter([1, -1], [1, -a], x)
    hop = int(step * SR); w = int(win * SR)
    t, v = [], []
    for c in range(0, max(1, len(y) - w), hop):
        seg = y[c:c + w]
        t.append((c + w / 2) / SR); v.append(10 * np.log10((seg ** 2).mean() + 1e-12))
    return np.array(t), np.array(v)


def ride(ref, out, win=4.0, step=2.0, mx=9.0, amount=1.0):
    tr, lr = loud(L.load(ref), win, step)
    # several renders (comma-separated, e.g. the same song at different seeds): average their short-term loudness,
    # so the ride follows the arrangement's level contour, not one seed's random fluctuations
    curves = [loud(L.load(o), win, step) for o in out.split(",")]
    m = min(len(c[1]) for c in curves)
    to, lo = curves[0][0][:m], np.mean([c[1][:m] for c in curves], axis=0)
    n = min(len(tr), len(to))
    d = (lr[:n] - lo[:n])
    d = d - np.median(d)            # the ride shapes the contour; the overall level is the ceiling's job
    # silence on either side says nothing about level
    d[(lr[:n] < -60) | (lo[:n] < -60)] = 0.0
    k = 2
    d = np.array([np.median(d[max(0, i - k):i + k + 1]) for i in range(n)])
    d = np.clip(d * amount, -mx, mx)
    return tr[:n], d


def contour_only(t, d, sections):
    """Remove each section's mean correction: the ride then shapes loudness *within* sections and leaves the section
    levels (the mastering term's job, set elsewhere) untouched. On Bleed this was +0.49 over a ride that also moved
    section levels (a section the record has quieter than ours kept being pushed up, and lost)."""
    d = d.copy()
    for a0, b0 in zip(sections, sections[1:]):
        sel = (t >= a0) & (t < b0)
        if sel.any():
            d[sel] -= d[sel].mean()
    return d


if __name__ == "__main__":
    a = sys.argv[1:]
    opt = lambda k, dflt: type(dflt)(a[a.index(k) + 1]) if k in a else dflt
    mp = json.load(open(a[0]))
    t, d = ride(a[1], a[2], opt("--win", 4.0), opt("--step", 2.0), opt("--max", 9.0), opt("--amount", 1.0))
    master = mp.setdefault("head", {}).setdefault("master", {})
    fx = master.setdefault("fx", [])
    if not any(isinstance(f, dict) and f.get("type") == "gain" and "auto.ride" in json.dumps(f) for f in fx):
        fx.append({"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.ride", "amount": 1}]}})
    lanes = master.setdefault("auto", {})
    if "--sections" in a:   # with --contour: per-section mean removed (sections file: comma-separated boundaries, seconds)
        secs = [float(v) for v in open(a[a.index("--sections") + 1]).read().strip().split(",")]
        if "--contour" in a:
            d = contour_only(t, d, secs)
    if "--accumulate" in a and "ride" in lanes:
        old_t = np.array([float(p[0].rstrip("s")) for p in lanes["ride"]["points"]])
        old_v = np.array([p[1] for p in lanes["ride"]["points"]])
        d = np.clip(d + np.interp(t, old_t, old_v), -opt("--max", 9.0), opt("--max", 9.0))
    lanes["ride"] = {"points": [["0s", round(float(d[0]), 2)]] + [[f"{x:.2f}s", round(float(v), 2)] for x, v in zip(t, d)]}
    json.dump(mp, open(opt("-o", a[0]), "w"), indent=1)
    print(f"ride: {len(t)} points, range {d.min():+.1f}..{d.max():+.1f} dB, mean |d| {np.abs(d).mean():.1f} dB")
