#!/usr/bin/env python3
"""drumshare: per section, the drums' share of the chroma-dominant 100-200 Hz power, ours vs the record's
(chirper-two). Our share = drum-solo power / mix power; the record's = drum-stem power / mix power (a separated
stem; read it as a level of evidence, not truth). Prints each section's chroma (likeness-exact) and flags sections
where our drums own the band far more than the record's do: in TSS (0-46 s) and Pravus (242-277 s) such tom
passages were worth +0.25..+0.9 once the toms were retuned to the record's onset-synchronous peak.

  drumshare.py REF.wav REF_DRUM_STEM.wav OUR_MIX.wav OUR_DRUM_SOLO.wav SECTIONS.txt [--lo 100 --hi 200]
"""
import argparse
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chromadiag as CD  # noqa: E402

L = CD.L


def band(x, a, b, lo, hi):
    return CD.raw_pc(CD.mono(x[int(a * L.SR):int(b * L.SR)]), [(lo, hi)])[(lo, hi)].sum(1)


def main():
    ap = argparse.ArgumentParser()
    for k in ("ref", "ref_drums", "mix", "drums", "sections"):
        ap.add_argument(k)
    ap.add_argument("--lo", type=float, default=100)
    ap.add_argument("--hi", type=float, default=200)
    a = ap.parse_args()
    R, RD, M, D = (L.load(p) for p in (a.ref, a.ref_drums, a.mix, a.drums))
    bounds = [float(v) for v in open(a.sections).read().replace(",", " ").split()]
    rows = CD.analyse(a.ref, a.mix, bounds, {})
    N = CD.NAMES
    print(f"{'section':>15} chroma | drums share of {a.lo:.0f}-{a.hi:.0f} Hz: record / ours | top pcs: record mix / our drums")
    for (s, e), r in zip(zip(bounds[:-1], bounds[1:]), rows):
        rm, rd, om, od = (band(x, s, e, a.lo, a.hi) for x in (R, RD, M, D))
        rs, os_ = 100 * rd.sum() / max(rm.sum(), 1e-20), 100 * od.sum() / max(om.sum(), 1e-20)
        flag = "  <== drums own the band" if os_ > 50 and os_ > 2 * rs else ""
        top = lambda p: " ".join(N[i] for i in np.argsort(-p)[:3])  # noqa: E731
        print(f"{s:7.1f}-{e:7.1f} {r['chroma']:5.1f} | {rs:5.0f}% / {os_:5.0f}% | {top(rm):8s} / {top(od):8s}{flag}")


if __name__ == "__main__":
    main()
