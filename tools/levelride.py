#!/usr/bin/env python3
"""Fader ride for a tab2song map: follow the reference's macro-dynamics. Short-term loudness of the reference and of
a render of the map are compared (high-passed RMS, smoothed over --win seconds); the difference becomes a master gain
automation lane (auto.ride, after the master EQ, before the song ceiling), clamped to ±--max dB and median-filtered so
it moves like a hand on a fader, not a compressor. Re-run after arrangement or mix changes (it follows the render).

  levelride.py MAP.json REF.wav RENDER.wav[,RENDER2,...] [--win 4] [--step 2] [--max 9] [--amount 1.0] [--contour --sections F] [--slew 8] [--only-in T0-T1,…] [--fade-out T0-T1] [-o OUT.json]

--amount scales the correction (0.5 = halfway). --only-in T0-T1,… applies the (absolute, not contour) correction only inside
those ranges with 0.5 s ramps — an outro's decay or a trailing tail past the record's end (Hajnal, Raining Blood: +0.3..0.5). --slew caps how fast the lane moves (dB/s; 8 keeps 0.25 s rides fader-like). --contour --sections F removes each section's mean correction, so the
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


def fade_out(t, d, spec):
    """Append a linear fade on the ride lane: 0 dB at T0 down to -60 dB at T1 (and held after) — a tail that must end
    where the record ends (the loudness measure gates near-silence, so a ride cannot ask for it)."""
    a0, a1 = (float(v) for v in spec.split("-"))
    f = np.interp(t, [a0, a1], [0.0, -60.0], left=0.0, right=-60.0)
    if t[-1] < a1:
        t = np.append(t, [a1, a1 + 2.0]); d = np.append(d, [d[-1], d[-1]]); f = np.append(f, [-60.0, -60.0])
    return t, d + f


def only_in_mask(t, spec, ramp=0.5):
    """1 inside the ranges ("T0-T1,T0-T1"), 0 outside, with linear ramps of `ramp` s at the edges."""
    w = np.zeros(len(t))
    for r in spec.split(","):
        a0, a1 = (float(v) for v in r.split("-"))
        w = np.maximum(w, np.clip(np.minimum((t - a0) / ramp + 1, (a1 - t) / ramp + 1), 0, 1))
    return w


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
    if "--only-in" in a:   # correct only inside these ranges (e.g. an outro's level curve); the lane elsewhere is untouched
        d = d * only_in_mask(t, a[a.index("--only-in") + 1])
    if "--accumulate" in a and "ride" in lanes:
        old_t = np.array([float(p[0].rstrip("s")) for p in lanes["ride"]["points"]])
        old_v = np.array([p[1] for p in lanes["ride"]["points"]])
        d = np.clip(d + np.interp(t, old_t, old_v), -opt("--max", 9.0), opt("--max", 9.0))
    if "--slew" in a:   # limit how fast the ride may move (dB/s, both directions): fine rides stay fader-like, not pumping
        lim = float(a[a.index("--slew") + 1])
        d = d.copy()
        for i in range(1, len(d)):
            d[i] = np.clip(d[i], d[i - 1] - lim * (t[i] - t[i - 1]), d[i - 1] + lim * (t[i] - t[i - 1]))
        for i in range(len(d) - 2, -1, -1):
            d[i] = np.clip(d[i], d[i + 1] - lim * (t[i + 1] - t[i]), d[i + 1] + lim * (t[i + 1] - t[i]))
    if "--fade-out" in a:   # an explicit tail fade (after the slew, so it is not slowed)
        t, d = fade_out(t, d, a[a.index("--fade-out") + 1])
    lanes["ride"] = {"points": [["0s", round(float(d[0]), 2)]] + [[f"{x:.2f}s", round(float(v), 2)] for x, v in zip(t, d)]}
    json.dump(mp, open(opt("-o", a[0]), "w"), indent=1)
    print(f"ride: {len(t)} points, range {d.min():+.1f}..{d.max():+.1f} dB, mean |d| {np.abs(d).mean():.1f} dB")
