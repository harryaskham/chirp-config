#!/usr/bin/env python3
"""bandsrc: who carries the chroma-dominant band, and with which pitch classes (chirper-two).

  bandsrc.py ID OUR_MIX.wav --ours NAME=solo.wav ... --ref-stems NAME=stem.wav ... [--lo 100 --hi 200]
             [--sections FILE | --bars A-B] [--min-chroma 100]

Per section (or per bar of the map's performed clock with --bars), prints the likeness-exact section chroma and
the 100-200 Hz content oracle (chromadiag), then for the record's mix and stems and for our mix and group solos:
the share of the band's power (source / mix) and the top pitch classes inside the band. Read it as: which source
dominates the record's band and what it says, versus which of ours dominates and what it says. A source can
own the band while being musically right (the bass in Lethargica 282-347 s); test before removing anything.
Solo renders hit the master chain alone and separated stems leak: shares are evidence, not decompositions.
"""
import argparse
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import chromadiag as CD  # noqa: E402

L = CD.L
CFG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # ~/.config/chirp (promoted from ref/evidence/chirper-two)
sys.path.insert(0, os.path.join(CFG, "tools"))


def prof(x, a, b, lo, hi):
    return CD.raw_pc(CD.mono(x[int(a * L.SR):int(b * L.SR)]), [(lo, hi)])[(lo, hi)].sum(1)


def top(p, k=2):
    s = p.sum()
    return " ".join(f"{CD.NAMES[i]}{int(100 * p[i] / max(s, 1e-20))}" for i in np.argsort(-p)[:k])


def spans_from_bars(cid, a, b):
    import tab2song as T
    m = json.load(open(os.path.join(CFG, "tools", "maps", f"{cid}.json")))
    off = m.get("offset", 0)
    out = []
    for x in T.performed_timeline(m["cache"], m):
        if a <= x["m"] <= b:
            s = x["start"] + off
            out.append((f"bar{x['m']}", s, s + 60 * x["beats"] / x["bpm"]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("id")
    ap.add_argument("mix")
    ap.add_argument("--ours", action="append", default=[])
    ap.add_argument("--ref-stems", action="append", default=[])
    ap.add_argument("--lo", type=float, default=100)
    ap.add_argument("--hi", type=float, default=200)
    ap.add_argument("--sections")
    ap.add_argument("--bars")
    ap.add_argument("--min-chroma", type=float, default=100, help="sections only: print those below this chroma")
    a = ap.parse_args()
    ref = os.path.join(CFG, "ref", f"{a.id}.wav")
    R, M = L.load(ref), L.load(a.mix)
    ours = {k: L.load(v) for k, v in (s.split("=", 1) for s in a.ours)}
    stems = {k: L.load(v) for k, v in (s.split("=", 1) for s in a.ref_stems)}
    lo, hi = a.lo, a.hi
    if a.bars:
        b0, b1 = (int(v) for v in a.bars.split("-"))
        spans = spans_from_bars(a.id, b0, b1)
        rows = None
    else:
        secf = a.sections or os.path.join(CFG, "tools", f"{a.id}-sections.txt")
        bounds = [float(v) for v in open(secf).read().replace(",", " ").split()]
        spans = [(f"{s:.1f}", s, e) for s, e in zip(bounds[:-1], bounds[1:])]
        rows = CD.analyse(ref, a.mix, bounds, {})
    for i, (lab, s, e) in enumerate(spans):
        if rows is not None:
            r = rows[i]
            if r["chroma"] >= a.min_chroma:
                continue
            head = f"{lab:>7}-{e:6.1f} ch {r['chroma']:5.1f} or {r['register_oracle'][f'{int(lo)}-{int(hi)}']['content']:+5.1f}" \
                if f"{int(lo)}-{int(hi)}" in r["register_oracle"] else f"{lab:>7}-{e:6.1f} ch {r['chroma']:5.1f}"
        else:
            head = f"{lab:>7} {s:6.1f}"
        rm, om = prof(R, s, e, lo, hi), prof(M, s, e, lo, hi)
        line = f"{head} | REF mix {top(rm):9s}" + "".join(
            f" {k} {100 * prof(v, s, e, lo, hi).sum() / max(rm.sum(), 1e-20):3.0f}%"
            f" {top(prof(v, s, e, lo, hi)):9s}" for k, v in stems.items())
        line += f" | OUR mix {top(om):9s}" + "".join(
            f" {k} {100 * prof(v, s, e, lo, hi).sum() / max(om.sum(), 1e-20):3.0f}%"
            f" {top(prof(v, s, e, lo, hi)):9s}" for k, v in ours.items())
        print(line, flush=True)


if __name__ == "__main__":
    main()
