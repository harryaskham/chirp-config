#!/usr/bin/env python3
"""eqfit: fit peaking-eq bands offline, so a part matches a wanted tone without render-and-look rounds.
(chirper-zero, Common Time v29 and v30, where its prediction held to 0.4 dB against renders twice.)

  eqfit.py TARGET.wav SOURCE.wav [--peaks "F:Q:G,F:Q:G,..."] [--lo 63] [--hi 5000]

SOURCE is the part rendered alone WITHOUT the eq; TARGET is the tone wanted (another rig, an earlier version, a
passage of a record). Both must be the same passage at the same gain. The bands are fitted by least squares on
biquad responses applied to SOURCE's spectrum, compared with TARGET in third-octaves from --lo to --hi Hz.
--peaks gives the starting bands, and their count is the eq's size (default two: 100:2:3,250:1.2:-3); each band may
move 1.6x in frequency either way, q 0.5 to 4, gain -9 to +9 dB.
Prints the difference before, the predicted difference after, and the fitted bands as F:Q:G (hertz, q, dB: the
`eq` effect's peaks). Render with them once to confirm. Read-only. Tests: tools/tests/test_eqfit.py.
"""
import sys
import wave

import numpy as np

CENTRES = (50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000)


def load(p):
    with wave.open(p) as w:
        sr = w.getframerate()
        return np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(float).reshape(-1, w.getnchannels()).mean(1) / 32768, sr


def fit(t, s, sr, start="100:2:3,250:1.2:-3", lo=63.0, hi=5000.0):
    """(third-octave centres, source minus target before, the same after the fitted bands, the bands as a flat
    list f, q, gain, f, q, gain, ...)."""
    from scipy.optimize import least_squares
    from scipy.signal import freqz
    n = min(len(t), len(s))
    T = np.abs(np.fft.rfft(t[:n])) ** 2
    S = np.abs(np.fft.rfft(s[:n])) ** 2
    f = np.fft.rfftfreq(n, 1 / sr)
    cs = np.array([c for c in CENTRES if lo <= c <= hi])

    def bands(P):
        return np.array([10 * np.log10(P[(f >= c / 2 ** (1 / 6)) & (f < c * 2 ** (1 / 6))].sum() + 1e-20) for c in cs])

    tb = bands(T)

    def peak(fc, q, g):
        A = 10 ** (g / 40)
        w0 = 2 * np.pi * fc / sr
        al = np.sin(w0) / (2 * q)
        _, h = freqz([1 + al * A, -2 * np.cos(w0), 1 - al * A], [1 + al / A, -2 * np.cos(w0), 1 - al / A], worN=f, fs=sr)
        return np.abs(h) ** 2

    def resp(p):
        H = np.ones_like(f)
        for i in range(0, len(p), 3):
            H = H * peak(p[i], p[i + 1], p[i + 2])
        return H

    p0 = [float(v) for b in start.split(",") for v in b.split(":")]
    lob = [v for i in range(0, len(p0), 3) for v in (p0[i] / 1.6, 0.5, -9.0)]
    hib = [v for i in range(0, len(p0), 3) for v in (p0[i] * 1.6, 4.0, 9.0)]
    r = least_squares(lambda p: bands(S * resp(p)) - tb, p0, bounds=(lob, hib))
    p = r.x
    return cs, bands(S) - tb, bands(S * resp(p)) - tb, p


def main(argv=None):
    a = sys.argv[1:] if argv is None else argv
    start = "100:2:3,250:1.2:-3"
    lo, hi = 63.0, 5000.0
    files = []
    it = iter(a)
    for x in it:
        if x in ("-h", "--help"):
            print(__doc__)
            return 0
        if x == "--peaks":
            start = next(it)
        elif x == "--lo":
            lo = float(next(it))
        elif x == "--hi":
            hi = float(next(it))
        else:
            files.append(x)
    if len(files) != 2:
        print(__doc__)
        return 2
    t, sr = load(files[0])
    s, sr2 = load(files[1])
    if sr != sr2:
        raise SystemExit(f"eqfit: the two files have different sample rates ({sr} and {sr2})")
    cs, before, after, p = fit(t, s, sr, start, lo, hi)
    print("Hz      " + " ".join("%5d" % c for c in cs))
    print("before  " + " ".join("%+5.1f" % v for v in before) + "   mean |d| %.2f" % np.mean(np.abs(before)))
    print("after   " + " ".join("%+5.1f" % v for v in after) + "   mean |d| %.2f" % np.mean(np.abs(after)))
    print("peaks   " + ",".join("%.0f:%.1f:%.1f" % (p[i], p[i + 1], p[i + 2]) for i in range(0, len(p), 3)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
