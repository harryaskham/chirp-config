#!/usr/bin/env python3
"""Which tab bar is the record playing? Per-bar onset-pattern matching of a reference stem against our own render of
the same part, on the map's bar timeline — for sections where our part correlates with nothing at any lag (the
record's arrangement differs from the tab: other bars, a different order, a repeat or a cut).

  barmatch.py MAP.json STEM.wav OURS.wav [--from S --to S] [--bars A-B] [--top 3] [--margin 0.25] [--min 0.45]

OURS.wav is a solo render of the matching part of the song the map generates (e.g. `chirp render -f SONG --solo kit`),
so each tab bar's window of it IS that bar's predicted pattern. Features per bar: onset flux in a low band (kick,
30-150 Hz) and a high band (snare/hats, 1-8 kHz), each resampled to 48 points across the bar and z-scored. For every
record bar in range it prints the correlation with the bar we play there (own), the best-matching tab measures
anywhere in the song, and flags bars where a different measure beats ours by --margin and reaches --min — the arrangement candidates to
remap with tab2song's replace / repeat / skip. In a repetitive song some other bar always wins by a little (138
candidates); trust a flag only when consecutive record bars point at consecutive tab bars. Low own correlation
with best matches scattered across the tab means the record plays something the tab lacks (or the bar grid is out
of phase there), not a different arrangement of the tab's bars.
"""
import importlib.util
import json
import os
import sys

import numpy as np
from scipy import signal

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import likeness as L  # noqa: E402

spec = importlib.util.spec_from_file_location("t2s", os.path.join(HERE, "tab2song.py"))
T2S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(T2S)


def bars(mp):
    """[(tab measure, start s, duration s)] for the bars the map plays, in order (skips and repeats applied)."""
    full = T2S.corrected_timeline(mp["cache"], mp)
    keep = [i for i, m in enumerate(full) if not m["skip"]]
    for a, b, n in mp.get("repeat", []):
        idx = [i for i in keep if a <= full[i]["m"] <= b]
        at = max((k for k, i in enumerate(keep) if full[i]["m"] <= b), default=len(keep) - 1) + 1
        keep[at:at] = idx * int(n)
    t = float(mp.get("offset", 0.0)); out = []
    for i in keep:
        d = full[i]["beats"] * 60.0 / full[i]["bpm"]
        out.append((full[i]["m"], t, d)); t += d
    return out


def flux(x, lo, hi, hop=240):
    f, _, Z = signal.stft(x, 48000, nperseg=1024, noverlap=1024 - hop)
    m = np.log1p(np.abs(Z[(f >= lo) & (f < hi)]) * 10)
    return np.maximum(np.diff(m, axis=1), 0).sum(0), hop / 48000


def features(path, bl, n=48):
    x = L.load(path).mean(1)
    out = []
    for lo, hi in ((30, 150), (1000, 8000)):
        e, fr = flux(x, lo, hi)
        rows = []
        for _, t, d in bl:
            grid = t + d * (np.arange(n) + 0.5) / n
            v = np.interp(grid / fr, np.arange(len(e)), e, left=0, right=0)
            rows.append(v)
        out.append(np.array(rows))
    F = np.concatenate(out, axis=1)
    F = F - F.mean(1, keepdims=True)
    return F / (np.linalg.norm(F, axis=1, keepdims=True) + 1e-9)


def main(a):
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    mp = json.load(open(a[0])); stem, ours = a[1], a[2]
    bl = bars(mp)
    R = features(stem, bl); O = features(ours, bl)
    M = R @ O.T          # record bar j vs our bar k (cosine of z-scored patterns)
    lo_t, hi_t = opt("--from", -1.0), opt("--to", 1e9)
    if "--bars" in a:
        b0, b1 = (int(v) for v in opt("--bars", "").split("-"))
    else:
        b0, b1 = 0, len(bl) - 1
    top, margin, floor = opt("--top", 3), opt("--margin", 0.25), opt("--min", 0.45)
    print(f"{len(bl)} bars; record bar → own corr | best tab measures (corr)")
    flagged = 0
    for j, (m, t, d) in enumerate(bl):
        if not (b0 <= j <= b1 and lo_t <= t <= hi_t):
            continue
        order = np.argsort(M[j])[::-1]
        best = []
        for k in order:
            if bl[k][0] not in [b[0] for b in best]:
                best.append((bl[k][0], M[j, k]))
            if len(best) >= top:
                break
        flag = best[0][1] - M[j, j] > margin and best[0][1] >= floor and best[0][0] != m
        flagged += flag
        print(f"{'*' if flag else ' '} #{j:3d} m{m:<4d} {t:7.2f}s own {M[j, j]:+.2f} | "
              + "  ".join(f"m{bm} {bc:+.2f}" for bm, bc in best))
    print(f"{flagged} bars where another tab measure beats ours by > {margin} (and reaches {floor})")


if __name__ == "__main__":
    main(sys.argv[1:])
