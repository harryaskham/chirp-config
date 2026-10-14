#!/usr/bin/env python3
"""Suggest a mastering EQ: fit a few peak/shelf bands to the long-term spectral difference between a candidate
mix and its reference (1/3-octave, level-normalised), and print a ready-to-paste chirp `eq` stage.

  mastereq.py REF.wav CAND.wav [--from S --to S] [--bands 5] [--max 8] [--scale 1.0] [--json]

Greedy: smooth the (cand − ref) curve, take the largest remaining deviation, place a band there (a low/high shelf
at the edges, otherwise a peak whose q follows the deviation's width), subtract its response, repeat. Bands with
|gain| < 1.5 dB are dropped. `--scale` multiplies every gain (Bleed: 1.0 scored best; 0.5 and 1.4 were worse).
Fix instruments first — this is for the whole-mix balance that is left (the unmastered 'muddy, dull' signature)."""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import likeness as L  # noqa: E402

SR = 48000


def third_octave(path, a, e):
    x = L.load(path).mean(1)
    x = x[int(a * SR):int(e * SR)] if e else x[int(a * SR):]
    N = 16384; f = np.fft.rfftfreq(N, 1 / SR); P = np.zeros(N // 2 + 1)
    for i in range(0, len(x) - N, N):
        P += np.abs(np.fft.rfft(x[i:i + N] * np.hanning(N))) ** 2
    edges = 30 * 2 ** (np.arange(0, 9.5, 1 / 3)); edges = edges[edges <= 18000]
    db = np.array([10 * np.log10(P[(f >= lo) & (f < hi)].mean() + 1e-20) for lo, hi in zip(edges[:-1], edges[1:])])
    return np.sqrt(edges[:-1] * edges[1:]), db - db.mean()


def peak_resp(c, fc, gain, q):
    """Approximate magnitude (dB) of a peaking band on a log-frequency axis: a Gaussian in octaves."""
    bw = 1.0 / q            # ≈ bandwidth in octaves
    return gain * np.exp(-0.5 * (np.log2(c / fc) / (bw / 2.355 * 2)) ** 2)


def shelf_resp(c, fc, gain, high):
    s = 1 / (1 + np.exp(-(np.log2(c / fc)) * 3))
    return gain * (s if high else 1 - s)


def fit(c, dev, n_bands=5, max_gain=8.0):
    resid = np.convolve(dev, np.ones(3) / 3, "same")
    resid[0], resid[-1] = dev[0], dev[-1]
    bands = []
    for _ in range(n_bands):
        i = int(np.argmax(np.abs(resid)))
        d = resid[i]
        if abs(d) < 1.5:
            break
        g = float(np.clip(-d, -max_gain, max_gain))
        # width: span of same-sign deviation above half the peak
        j0 = i
        while j0 > 0 and np.sign(resid[j0 - 1]) == np.sign(d) and abs(resid[j0 - 1]) > abs(d) / 2:
            j0 -= 1
        j1 = i
        while j1 < len(resid) - 1 and np.sign(resid[j1 + 1]) == np.sign(d) and abs(resid[j1 + 1]) > abs(d) / 2:
            j1 += 1
        if j1 == len(resid) - 1 and j0 > len(resid) // 2:
            fc = float(c[j0]); bands.append(("highshelf", fc, g, None)); resid += shelf_resp(c, fc, g, True)
        elif j0 == 0 and j1 < len(resid) // 2:
            fc = float(c[j1]); bands.append(("lowshelf", fc, g, None)); resid += shelf_resp(c, fc, g, False)
        else:
            width_oct = max(1 / 3, (j1 - j0 + 1) / 3)
            q = float(np.clip(1.0 / width_oct, 0.5, 3))
            fc = float(c[i]); bands.append(("peak", fc, g, q)); resid += peak_resp(c, fc, g, q)
    return bands, resid


def fmt(bands, scale):
    out = []
    for kind, fc, g, q in sorted(bands, key=lambda b: b[1]):
        g *= scale
        if abs(g) < 1.5:
            continue
        f = f"{fc / 1000:.1f}k" if fc >= 1000 else f"{fc:.0f}"
        out.append(f"{kind} cutoff={f}" + (f" q={q:.1f}" if q else "") + f" gain={g:.1f}dB")
    return out


def main():
    a = sys.argv[1:]
    opt = lambda k, d: a[a.index(k) + 1] if k in a else d
    t0, t1 = float(opt("--from", 0)), float(opt("--to", 0)) or None
    c, R = third_octave(a[0], t0, t1)
    _, C = third_octave(a[1], t0, t1)
    dev = C - R
    bands, resid = fit(c, dev, int(opt("--bands", 5)), float(opt("--max", 8)))
    eq = {"type": "eq", "bands": fmt(bands, float(opt("--scale", 1.0)))}
    if "--json" in a:
        print(json.dumps({"eq": eq, "deviation_rms_db": float(np.sqrt((dev ** 2).mean())),
                          "residual_rms_db": float(np.sqrt((resid ** 2).mean()))}))
    else:
        print(f"deviation rms {np.sqrt((dev ** 2).mean()):.1f} dB → residual after the bands {np.sqrt((resid ** 2).mean()):.1f} dB")
        print(json.dumps(eq))


if __name__ == "__main__":
    main()
