#!/usr/bin/env python3
"""Per-bar tempo outliers in a tab2song map (DTW passes can leave implausible jumps), and a time-preserving flatten.
  bpmcheck.py MAP.json [--dev 0.06] [--win 9]                 list bars whose bpm deviates > dev from the local median
  bpmcheck.py MAP.json --flatten A-B[,C-D] -o OUT.json        set each range to its time-preserving mean bpm
A song on a steady groove should not swing 121 -> 138 -> 102 BPM bar to bar (Dreams' first chorus after a coarse
dtwgrid pass, rhythm 21). Flattening a run to the bpm that keeps its total duration leaves every later bar where
it was; then refine the run with dtwgrid --bars A-B --block 2 --window 0.15 --feature metric --around-zero
--minconf 0.3 --keep-below --median 3 (Dreams: rhythm 21 -> 35 and 26 -> 40, +0.64 held-out). Beats per bar come
from the map's tab (via barchroma's timeline), so meters other than 4/4 are handled."""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import barchroma as B  # noqa: E402


def timeline(mp):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cache = mp["cache"] if os.path.isabs(mp["cache"]) else os.path.join(root, mp["cache"])
    return [m for m in B.T.corrected_timeline(cache, mp) if not m["skip"]]


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    mp = json.load(open(a[0]))
    tl = timeline(mp)
    if "--flatten" in a:
        bpm = mp.setdefault("bpm", {})
        beats = {m["m"]: m["beats"] for m in tl}; cur = {m["m"]: m["bpm"] for m in tl}
        for rg in opt("--flatten", "").split(","):
            lo, hi = (int(v) for v in rg.split("-"))
            ms = [k for k in range(lo, hi + 1) if k in beats]
            nb = sum(beats[k] for k in ms); secs = sum(beats[k] * 60 / cur[k] for k in ms)
            v = round(nb / secs * 60, 3)
            for k in ms:
                bpm[str(k)] = v
            print(f"bars {lo}-{hi}: {nb:g} beats in {secs:.3f} s -> {v} BPM")
        raw = open(a[0]).read(); ind = (len(raw.splitlines()[1]) - len(raw.splitlines()[1].lstrip())) if raw.count("\n") > 1 else 2
        open(opt("-o", ""), "w").write(json.dumps(mp, indent=ind or 2, ensure_ascii=False) + "\n")
        return
    dev, win = opt("--dev", 0.06), opt("--win", 9)
    vals = np.array([m["bpm"] for m in tl]); t = mp.get("offset", 0.0); times = []
    for m in tl:
        times.append(t); t += m["beats"] * 60 / m["bpm"]
    flagged = []
    for i, m in enumerate(tl):
        lo, hi = max(0, i - win // 2), min(len(tl), i + win // 2 + 1)
        med = float(np.median(vals[lo:hi]))
        if abs(m["bpm"] - med) / med > dev:
            flagged.append((m["m"], round(times[i], 1), round(m["bpm"], 1), round(med, 1)))
    print(f"{len(flagged)} of {len(tl)} bars deviate > {dev * 100:.0f}% from the local median (bar, time s, bpm, median):")
    for f in flagged:
        print("  m%d %7.1fs  %6.1f vs %6.1f" % f)


if __name__ == "__main__":
    main()
