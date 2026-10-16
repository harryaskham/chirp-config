#!/usr/bin/env python3
"""A record's tuning offset from A440: the weighted circular mean, in cents, of strong spectral peaks' deviation from
the equal-tempered grid, per file (stems or the mix). Set a song's `a4: 440·2^(c/1200)` to follow a record that is
off concert pitch (tape-era masters drift by tens of cents) — then judge by the score: likeness' chroma uses A440
semitone bins, so offsets well under 50 cents barely register (2 Minutes to Midnight: +20 c, a4 445.1 tied).

  tuning.py FILE.wav [FILE2.wav …] [--lo 80] [--hi 1500] [--from 20] [--to 300]
"""
import sys

import numpy as np
from scipy import signal

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import likeness as L  # noqa: E402


def offset(path, lo, hi, t0, t1, seg=8192):
    x = L.load(path).mean(1); offs, w = [], []
    for s in range(int(48000 * t0), min(len(x), int(48000 * t1)) - seg, 48000):
        X = np.abs(np.fft.rfft(x[s:s + seg] * np.hanning(seg))); f = np.fft.rfftfreq(seg, 1 / 48000)
        pk, _ = signal.find_peaks(X, height=X.max() * 0.2, distance=5)
        for p in pk:
            if lo < f[p] < hi and 0 < p < len(X) - 1:
                a, b, c = np.log(X[p - 1] + 1e-12), np.log(X[p]), np.log(X[p + 1] + 1e-12)
                fp = (p + 0.5 * (a - c) / (a - 2 * b + c + 1e-12)) * 48000 / seg
                m = 69 + 12 * np.log2(fp / 440); offs.append((m - round(m)) * 100); w.append(X[p])
    if not offs:
        return 0.0, 0
    offs, w = np.array(offs), np.array(w)
    return float(np.angle(np.sum(w * np.exp(2j * np.pi * offs / 100))) / (2 * np.pi) * 100), len(offs)


if __name__ == "__main__":
    a = sys.argv[1:]
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    files = [v for i, v in enumerate(a) if not v.startswith("--") and (i == 0 or not a[i - 1].startswith("--"))]
    for f in files:
        c, n = offset(f, opt("--lo", 80.0), opt("--hi", 1500.0), opt("--from", 20.0), opt("--to", 300.0))
        print(f"{f}: {c:+.1f} cents ({n} peaks) → a4 {440 * 2 ** (c / 1200):.2f}")
