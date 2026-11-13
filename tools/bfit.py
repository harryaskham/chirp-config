#!/usr/bin/env python3
"""bfit: the partials of a held string note and the inharmonicity that fits them (chirper-zero, 13 Nov, for the pluck
layer's `inharm`: it showed that `stiff` 0.32 gives a low Eb a B of 2e-7 where a real wound string has about 1e-4).

  bfit.py WAV F0 [B]

WAV is a held note, DI (no amp), a second or more; F0 its fundamental in Hz. Prints the fundamental found (and its cents
from F0), the cents each of partials 5, 10, 20, 30 and 40 stands above n times the fundamental, and the B that fits
f_n = n f1 sqrt(1 + B n^2) over the partials up to 5 kHz (at most 50). With B given, the law's own cents beside each
partial and how far the fit is from it. Reads 0.1-1.1 s of the file, both channels summed. Read-only.
(Promoted to tools/ by chirp-eco as written; tests: tools/tests/test_bfit.py.)
"""
import sys
import wave

import numpy as np


def partials(x, sr, f0):
    """(f1, {n: Hz}) of a held note: each partial is looked for where the last spacing predicts it."""
    y = x[int(0.1 * sr):int(1.1 * sr)]
    y = y * np.hanning(len(y))
    n = 1 << 21
    X = np.abs(np.fft.rfft(y, n))
    fr = np.fft.rfftfreq(n, 1 / sr)

    def peak(f, rel):
        m = (fr > f * (1 - rel)) & (fr < f * (1 + rel))
        return fr[np.argmax(X * m)]

    f1 = peak(f0, 0.03)
    fs = {1: f1}
    prev = f1
    top = int(min(50, 5000 / f0))
    for k in range(2, top + 1):
        step = (prev - fs.get(k - 2, 0)) if k > 2 else f1          # the last spacing predicts the next partial
        pk = peak(prev + step, 0.4 * f1 / (prev + step))
        fs[k] = pk
        prev = pk
    return f1, fs


def fit(f1, fs):
    """(the partials' cents above n f1, the fitted B)."""
    ks = np.array(sorted(fs))
    f = np.array([fs[k] for k in ks])
    c = 1200 * np.log2(f / (ks * f1))
    b = np.sum(((f / (ks * f1)) ** 2 - 1) * (ks ** 2 - 1)) / np.sum((ks ** 2 - 1) ** 2)
    return c, float(b)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) < 2:
        raise SystemExit(__doc__)
    p, f0 = argv[0], float(argv[1])
    B = float(argv[2]) if len(argv) > 2 else None
    with wave.open(p) as w:
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(float).reshape(-1, w.getnchannels()).mean(1) / 32768
    f1, fs = partials(x, sr, f0)
    c, b = fit(f1, fs)
    top = max(fs)
    s = "f1 %.3f Hz (%+.1f cents) | " % (f1, 1200 * np.log2(f1 / f0))
    for k in (5, 10, 20, 30, 40):
        if k <= top:
            s += "n%d %.0f" % (k, c[k - 1]) + ("/%.0f  " % (1200 * np.log2(np.sqrt(1 + B * k * k))) if B else "  ")
    print(s + "| B fitted %.2e" % b + (" (asked %.0e: %+.0f%%)" % (B, 100 * (b / B - 1)) if B else ""))


if __name__ == "__main__":
    sys.exit(main())
