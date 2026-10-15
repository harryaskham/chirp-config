#!/usr/bin/env python3
"""Utterance profile of a vocal line: per-syllable features of a vocal stem (or a soloed render), for fitting voice
patches and setting measurable targets for voice-engine work (harsh / extreme vocals in particular).

  voxprofile.py WAV [WAV …] [--from S --to S] [--json]

Syllables: vocal-band flux onsets (stemvox.syllables_flux), each ≥ 80 ms; steady features use the middle 60 %.
Per syllable:
  f0        Hz, harmonic summation (110-900 Hz, quarter-tone steps), and f0 slope over the syllable (semitones/s)
  hnr       harmonic-to-noise ratio, dB: power within ±3 % of the harmonics k·f0 (k ≤ 20, < 5 kHz) vs the rest
  subh      subharmonic ratio, dB: power at (k + ½)·f0 vs at k·f0 — period doubling, false-fold 'scream' voicing
  tilt      spectral tilt, dB/octave, 300 Hz-5 kHz (1/3-octave bands, least-squares slope)
  centroid  Hz, 100 Hz-8 kHz
  rise      onset rise time, ms: from 20 dB below the syllable's peak level to the peak (5 ms frames)
  f1 / f2   Hz, the two lowest peaks of a 12th-order LPC envelope (Levinson-Durbin at 12 kHz; no root finding)
Prints median [25th-75th percentile] per feature and file, so a candidate can be compared with the stem."""
import json
import os
import sys

import numpy as np
from scipy import signal as sg

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import likeness as L  # noqa: E402
import stemvox as V  # noqa: E402

SR = 48000


def f0_of(seg):
    n = 1 << int(np.ceil(np.log2(max(len(seg), 16384))))
    spec = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), n)) ** 2
    mag = np.log1p(spec / (spec.max() + 1e-20) * 1e4)
    best, bf = -1.0, 200.0
    for q in range(0, 4 * 36):                              # 110 Hz … ~900 Hz in quarter tones
        f0 = 110 * 2 ** (q / 48)
        s = sum(mag[min(len(mag) - 1, int(round(h * f0 * n / SR)))] / h for h in range(1, 6))
        if s > best:
            best, bf = s, f0
    return bf, spec, n


def comb_power(spec, n, f0, offset):
    tot = 0.0
    for k in range(1, 21):
        fc = (k + offset) * f0
        if fc >= 5000:
            break
        lo, hi = int(fc * 0.97 * n / SR), int(fc * 1.03 * n / SR) + 1
        tot += spec[lo:hi].sum()
    return tot


def lpc_formants(seg):
    y = sg.resample_poly(seg, 1, 4)                        # 12 kHz
    y = np.append(y[0], y[1:] - 0.95 * y[:-1]) * np.hamming(len(y))
    order = 12
    r = np.array([np.dot(y[:len(y) - k], y[k:]) for k in range(order + 1)])
    if r[0] <= 0:
        return None, None
    a = np.zeros(order + 1); a[0] = 1.0; e = r[0]
    for i in range(1, order + 1):                          # Levinson-Durbin
        k = -(r[i] + np.dot(a[1:i], r[i - 1:0:-1])) / e
        a[1:i] = a[1:i] + k * a[i - 1:0:-1]
        a[i] = k
        e *= (1 - k * k)
        if e <= 0:
            return None, None
    h = 1 / (np.abs(np.fft.rfft(a, 2048)) + 1e-9)
    f = np.fft.rfftfreq(2048, 1 / 12000)
    pk, _ = sg.find_peaks(20 * np.log10(h))
    pk = [p for p in pk if 200 < f[p] < 4000]
    return (float(f[pk[0]]) if pk else None), (float(f[pk[1]]) if len(pk) > 1 else None)


def profile(path, a=None, e=None):
    x = L.load(path).mean(1)
    if a is not None:
        x = x[int(a * SR):int(e * SR)]
    env, hop = V.band_env(x)
    segs = V.syllables_flux(env, hop, 30)
    rows = []
    for s, t, _ in segs:
        if t - s < 0.08:
            continue
        seg = x[int(s * SR):int(t * SR)]
        mid = seg[int(len(seg) * 0.2):int(len(seg) * 0.8)]
        if len(mid) < 1024 or np.sqrt((mid ** 2).mean()) < 1e-4:
            continue
        f0, spec, n = f0_of(mid)
        h, sub = comb_power(spec, n, f0, 0.0), comb_power(spec, n, f0, 0.5)
        f = np.fft.rfftfreq(n, 1 / SR)
        band = spec[(f >= 100) & (f < 5000)].sum()
        hnr = 10 * np.log10(h / max(band - h, 1e-20))
        subh = 10 * np.log10(max(sub, 1e-20) / max(h, 1e-20))
        cen = float((f * spec)[(f >= 100) & (f < 8000)].sum() / (spec[(f >= 100) & (f < 8000)].sum() + 1e-20))
        edges = 300 * 2 ** (np.arange(0, 4.1, 1 / 3)); lv = []
        for lo, hi in zip(edges[:-1], edges[1:]):
            lv.append(10 * np.log10(spec[(f >= lo) & (f < hi)].mean() + 1e-20))
        xo = np.log2(np.sqrt(edges[:-1] * edges[1:])); yo = np.array(lv)
        tilt = float(np.sum((xo - xo.mean()) * (yo - yo.mean())) / np.sum((xo - xo.mean()) ** 2))
        # f0 slope: first vs last third
        q = len(seg) // 3
        slope = 12 * np.log2(f0_of(seg[-q:])[0] / f0_of(seg[:q])[0]) / max((t - s) * 2 / 3, 1e-3) if q > 1024 else 0.0
        fr = int(0.005 * SR); lev = np.array([np.sqrt((seg[i:i + fr] ** 2).mean()) + 1e-9 for i in range(0, min(len(seg), int(0.15 * SR)) - fr, fr)])
        if len(lev) > 2:
            ld = 20 * np.log10(lev); pk = int(np.argmax(ld)); st = np.where(ld[:pk + 1] < ld[pk] - 20)[0]
            rise = (pk - (st[-1] if len(st) else 0)) * 5.0
        else:
            rise = float("nan")
        f1, f2 = lpc_formants(mid)
        rows.append({"f0": f0, "slope": slope, "hnr": hnr, "subh": subh, "tilt": tilt, "centroid": cen, "rise": rise, "f1": f1, "f2": f2})
    return rows


def summary(rows):
    out = {"syllables": len(rows)}
    for k in ("f0", "slope", "hnr", "subh", "tilt", "centroid", "rise", "f1", "f2"):
        v = np.array([r[k] for r in rows if r[k] is not None and np.isfinite(r[k])])
        if len(v):
            out[k] = [round(float(np.percentile(v, p)), 1) for p in (50, 25, 75)]
    return out


def main():
    a = sys.argv[1:]
    opt = lambda k, d: a[a.index(k) + 1] if k in a else d
    t0, t1 = opt("--from", None), opt("--to", None)
    files = [x for i, x in enumerate(a) if not x.startswith("--") and (i == 0 or a[i - 1] not in ("--from", "--to"))]
    res = {f: summary(profile(f, float(t0) if t0 else None, float(t1) if t1 else None)) for f in files}
    if "--json" in a:
        print(json.dumps(res)); return
    keys = ("f0", "slope", "hnr", "subh", "tilt", "centroid", "rise", "f1", "f2")
    print(f"{'file':28s} {'n':>4s} " + " ".join(f"{k:>18s}" for k in keys))
    for f, s in res.items():
        print(f"{os.path.basename(f)[:28]:28s} {s['syllables']:4d} " + " ".join(f"{s[k][0]:7.1f} [{s[k][1]:.0f},{s[k][2]:.0f}]".rjust(18) if k in s else " " * 18 for k in keys))


if __name__ == "__main__":
    main()
