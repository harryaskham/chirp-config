#!/usr/bin/env python3
"""Transcribe drums from a separated drum stem onto a 16th grid → explicit kit notation.

  stemdrums.py STEM.wav DOWNBEAT_S BAR_S FIRST_BAR LAST_BAR [--th k=1.8,s=1.6,h=1.5,c=1.4]

Each piece is a band envelope (kick 40-100 Hz, snare 180-300 Hz + 1.5-4 kHz, hat 7-12 kHz, crash
3-6 kHz sustained); a step is a hit when the envelope peak just after it exceeds the piece's threshold
× its rolling median floor. Hit strength becomes velocity. Thresholds are calibrated against a known
transcription (`calibrate`). Output: one line per bar of 16th tokens (`k,oh/0.25b@104 R/0.25b …`)."""
import json, os, sys
import numpy as np
from scipy import ndimage, signal
sys.path.insert(0, os.path.dirname(__file__))
import likeness as L

BANDS = {"k": [(40, 100)], "s": [(180, 300), (1500, 4000)], "h": [(7000, 12000)], "c": [(3000, 6000)]}
TH = {"k": 1.8, "s": 1.6, "h": 1.5, "c": 1.4}
NAME = {"k": "k", "s": "s", "h": "oh", "c": "c"}


def envelopes(path):
    x = L.load(path).mean(1)
    env = {}
    for p, bands in BANDS.items():
        e = 0
        for lo, hi in bands:
            sos = signal.butter(4, (lo, hi), btype="band", fs=48000, output="sos")
            e = e + np.abs(signal.sosfiltfilt(sos, x))
        e = ndimage.maximum_filter1d(e, 96)[::96]  # 2 ms resolution
        env[p] = e
    return env


def grid_hits(env, d0, bar, b0, b1, th=TH):
    """→ {piece: array [bars, 16] of strength ratios (0 = no hit)}."""
    out = {}
    s16 = bar / 16
    for p, e in env.items():
        floor = ndimage.median_filter(e, size=int(1.0 / 0.002))  # 1 s rolling median
        res = np.zeros((b1 - b0 + 1, 16))
        for j in range(b0, b1 + 1):
            for k in range(16):
                t = d0 + j * bar + k * s16
                i0, i1 = int((t - 0.015) / 0.002), int((t + 0.035) / 0.002)
                pk = e[i0:i1].max(); fl = floor[int(t / 0.002)] + 1e-9
                if p == "c":  # crash: must still ring 120 ms later
                    if e[int((t + 0.12) / 0.002)] < 0.5 * pk:
                        continue
                r = pk / fl
                if r > th[p]:
                    res[j - b0, k] = r
        out[p] = res
    return out


def to_score(hits):
    bars = next(iter(hits.values())).shape[0]
    lines = []
    for j in range(bars):
        toks = []
        for k in range(16):
            pcs = [NAME[p] for p in ("c", "k", "s", "h") if hits[p][j, k] > 0]
            if not pcs:
                toks.append("R/0.25b"); continue
            strength = max(hits[p][j, k] for p in hits if hits[p][j, k] > 0)
            toks.append(f"{','.join(pcs)}/0.25b@{int(np.clip(70 + 12 * np.log2(strength), 50, 124))}")
        lines.append(" ".join(toks))
    return lines


def truth_grid(score, nbars):
    """Parse an explicit kit score (beats lengths) into {piece: [bars,16] bool}."""
    import re
    g = {p: np.zeros((nbars, 16), bool) for p in BANDS}
    t = 0.0
    for tok in score.split():
        m = re.match(r"([a-z0-9,]+)/([\d.]+)b", tok)
        if not m:
            continue
        step = int(round(t * 4))
        if not tok.startswith("R") and step < nbars * 16:
            pcs = m.group(1).split(",")
            for p, names in (("k", {"k"}), ("s", {"s"}), ("h", {"oh", "h", "h1", "h2", "h3"}), ("c", {"c", "x", "cch"})):
                if names & set(pcs):
                    g[p][step // 16, step % 16] = True
        t += float(m.group(2))
    return g


if __name__ == "__main__":
    a = sys.argv[1:]
    th = dict(TH)
    if "--th" in a:
        for kv in a[a.index("--th") + 1].split(","):
            k, v = kv.split("="); th[k] = float(v)
    env = envelopes(a[0])
    hits = grid_hits(env, float(a[1]), float(a[2]), int(a[3]), int(a[4]), th)
    for j, line in enumerate(to_score(hits)):
        print(f"bar {int(a[3]) + j:3d}  {line}")
