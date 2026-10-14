#!/usr/bin/env python3
"""Per-section master EQ for songs that are not built from section tracks: one master `eq` with a fixed set of
bands whose gains step at the section boundaries, driven by master automation lanes (`auto.eqN`). Each section's
gains are a least-squares fit (exact biquad responses, a little ridge) of the 1/3-octave long-term difference
between the candidate and the reference over that section — the dense sections stop dictating the quiet ones'
EQ (chirper-two's mastereq.py fits one stage for the whole mix; chirper-zero found per-section fits worth more).

  sectioneq.py REF.wav CAND.wav SECTIONS.txt [--scale 1.0] [--max 9] [--only 0,2,5] [--ramp 0.05]

Prints a `master:` JSON block (auto lanes + eq stage) to merge into a song's master (append the eq after the glue).
--only fits just those sections (others stay flat): check each section separately — a fit can chase content
the arrangement lacks."""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import likeness as L  # noqa: E402

SR = 48000
BANDS = [("lowshelf", 45, 0.7), ("peak", 90, 1.0), ("peak", 250, 1.0), ("peak", 700, 1.0), ("peak", 1800, 1.0),
         ("peak", 4000, 1.0), ("highshelf", 10000, 0.7)]
CENTERS = 1000 * 2 ** (np.arange(-14, 14) / 3)          # 1/3-octave centres ~40 Hz – 16 kHz
CENTERS = CENTERS[(CENTERS >= 40) & (CENTERS <= 16000)]


def biquad_db(kind, f0, q, gain_db, f):
    """RBJ cookbook magnitude response (dB) at frequencies f."""
    A = 10 ** (gain_db / 40); w0 = 2 * np.pi * f0 / SR; al = np.sin(w0) / (2 * q); c = np.cos(w0)
    if kind == "peak":
        b = [1 + al * A, -2 * c, 1 - al * A]; a = [1 + al / A, -2 * c, 1 - al / A]
    elif kind == "lowshelf":
        s = 2 * np.sqrt(A) * al
        b = [A * ((A + 1) - (A - 1) * c + s), 2 * A * ((A - 1) - (A + 1) * c), A * ((A + 1) - (A - 1) * c - s)]
        a = [(A + 1) + (A - 1) * c + s, -2 * ((A - 1) + (A + 1) * c), (A + 1) + (A - 1) * c - s]
    else:
        s = 2 * np.sqrt(A) * al
        b = [A * ((A + 1) + (A - 1) * c + s), -2 * A * ((A - 1) + (A + 1) * c), A * ((A + 1) + (A - 1) * c - s)]
        a = [(A + 1) - (A - 1) * c + s, 2 * ((A - 1) - (A + 1) * c), (A + 1) - (A - 1) * c - s]
    z = np.exp(-1j * 2 * np.pi * f / SR)
    h = (b[0] + b[1] * z + b[2] * z * z) / (a[0] + a[1] * z + a[2] * z * z)
    return 20 * np.log10(np.abs(h) + 1e-12)


def third_octave(x):
    from scipy import signal as sg
    f, P = sg.welch(x, SR, nperseg=8192)
    out = []
    for c in CENTERS:
        sel = (f >= c / 2 ** (1 / 6)) & (f < c * 2 ** (1 / 6))
        out.append(10 * np.log10(P[sel].sum() + 1e-20))
    return np.array(out)


def solve(A, b):
    """Gaussian elimination with partial pivoting (tiny systems; numpy.linalg crashes against some system
    LAPACK builds)."""
    A = np.array(A, dtype=float); b = np.array(b, dtype=float); n = len(b)
    for i in range(n):
        p = i + int(np.argmax(np.abs(A[i:, i])))
        A[[i, p]], b[[i, p]] = A[[p, i]], b[[p, i]]
        for j in range(i + 1, n):
            f = A[j, i] / A[i, i]
            A[j, i:] -= f * A[i, i:]; b[j] -= f * b[i]
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - A[i, i + 1:] @ x[i + 1:]) / A[i, i]
    return x


def fit(dev, mx=9.0, ridge=0.15):
    """Gains g (dB) for BANDS so that their summed response ≈ −dev (6 dB unit responses, linearised)."""
    M = np.stack([biquad_db(k, f0, q, 6.0, CENTERS) / 6.0 for k, f0, q in BANDS], axis=1)
    A = M.T @ M + ridge * np.eye(len(BANDS))
    g = solve(A, M.T @ (-dev))
    return np.clip(g, -mx, mx)


if __name__ == "__main__":
    a = sys.argv[1:]
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    scale, mx, ramp = opt("--scale", 1.0), opt("--max", 9.0), opt("--ramp", 0.05)
    bounds = [float(v) for v in open(a[2]).read().split(",")]
    only = {int(v) for v in opt("--only", "").split(",") if v != ""} if "--only" in a else None
    R, Cd = L.load(a[0]).mean(1), L.load(a[1]).mean(1)
    gains = []
    for k, (s0, s1) in enumerate(zip(bounds, bounds[1:])):
        if only is not None and k not in only:
            gains.append(np.zeros(len(BANDS))); continue
        r = third_octave(R[int(s0 * SR):int(s1 * SR)]); c = third_octave(Cd[int(s0 * SR):int(min(s1, len(Cd) / SR) * SR)])
        dev = (c - c.mean()) - (r - r.mean())
        g = fit(dev, mx) * scale
        gains.append(g)
        print(f"section {k} {s0:7.1f}-{s1:7.1f}: deviation rms {np.sqrt((dev ** 2).mean()):.1f} dB → gains " +
              " ".join(f"{b[1]}:{v:+.1f}" for b, v in zip(BANDS, g)), file=sys.stderr)
    auto, bands = {}, []
    for j, (kind, f0, q) in enumerate(BANDS):
        pts = []
        for k, (s0, s1) in enumerate(zip(bounds, bounds[1:])):
            v = round(float(gains[k][j]), 2)
            pts += [[f"{round(s0 if k == 0 else s0 + ramp, 3)}s", v], [f"{round(s1, 3)}s", v]]
        pts = [[ "0s", pts[0][1]]] + pts
        auto[f"eq{j}"] = {"points": pts}
        bands.append({"kind": kind, "cutoff": f0, "q": q, "gain": {"value": "0dB", "mod": [{"src": f"auto.eq{j}", "amount": 1}]}})
    print(json.dumps({"auto": auto, "eq": {"type": "eq", "bands": bands}}))
