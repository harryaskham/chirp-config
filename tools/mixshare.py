#!/usr/bin/env python3
"""In-mix balance of an instrument group: per band and section, how far our group's share of our mix is from the
stem's share of the reference mix — (stem − ref mix) − (group solo − our mix), in dB — i.e. the gain the group
needs *in the mix*. A group can look right against its own stem while sitting buried or fizzy in the mix (Pneuma:
the kit 4 dB low with no body; the m8 guitars thin and fizzy; fixing each was +0.4 and +0.9). Emits an EQ for the
group's tracks from the mean over the chosen sections.

  mixshare.py REF.wav STEM.wav OURMIX.wav OURGROUP.wav SECTIONS.txt [--skip 0,5] [--emit-eq] [--max 9]

OURGROUP.wav is a solo render of the group's tracks from the same song as OURMIX.wav (stemscore.py --keep).
Sections where the stem is near-silent are skipped automatically; --skip excludes more (by index)."""
import json
import os
import sys

import numpy as np
from scipy.signal import butter, sosfilt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import likeness as L  # noqa: E402

BANDS = [(40, 100, "lowshelf", 100), (100, 300, "peak", 180), (300, 1500, "peak", 700), (1500, 6000, "peak", 3000),
         (6000, 16000, "highshelf", 7000)]


def lvl(x, lo, hi):
    y = sosfilt(butter(4, [lo, hi], btype="band", fs=48000, output="sos"), x)
    return 10 * np.log10((y ** 2).mean() + 1e-12)


def main(a):
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    ref, st, om, og = (L.load(p).mean(1) for p in a[:4])
    b = [float(v) for v in open(a[4]).read().split(",")]
    skip = {int(v) for v in opt("--skip", "").split(",") if v != ""}
    rows = []
    for i in range(len(b) - 1):
        if i in skip:
            continue
        sl = slice(int(b[i] * 48000), int(min(b[i + 1], len(og) / 48000, len(om) / 48000) * 48000))
        if 10 * np.log10((st[sl] ** 2).mean() + 1e-12) < -50 or 10 * np.log10((og[sl] ** 2).mean() + 1e-12) < -60:
            continue
        need = [(lvl(st[sl], lo, hi) - lvl(ref[sl], lo, hi)) - (lvl(og[sl], lo, hi) - lvl(om[sl], lo, hi)) for lo, hi, _, _ in BANDS]
        rows.append(need)
        print(f"section {i}: " + "  ".join(f"{lo}-{hi}: {v:+5.1f}" for (lo, hi, _, _), v in zip(BANDS, need)))
    if not rows:
        print("no usable sections"); return
    mean = np.mean(rows, 0)
    print("mean:     " + "  ".join(f"{lo}-{hi}: {v:+5.1f}" for (lo, hi, _, _), v in zip(BANDS, mean)))
    if "--emit-eq" in a:
        mx = opt("--max", 9.0)
        bands = [f"{k} cutoff={fc} {'q=0.8 ' if k == 'peak' else ''}gain={max(-mx, min(mx, v)):.1f}dB" for (lo, hi, k, fc), v in zip(BANDS, mean)]
        print(json.dumps({"type": "eq", "bands": bands}))


if __name__ == "__main__":
    main(sys.argv[1:])
