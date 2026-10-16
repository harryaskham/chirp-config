#!/usr/bin/env python3
"""Pick the sections where a change wins on EVERY seed — the --only-in ranges for stemvel/stemretime/levelride/songride.

  sectionpick.py SECTIONS.txt BASE_s7.json,BASE_s13.json VAR_s7.json,VAR_s13.json [--min 0.1] [--merge]

Each JSON is `likeness.py sections REF RENDER $(cat SECTIONS)` output; base and variant lists are paired by position (the
same seeds). Prints the per-section deltas and an --only-in string of the sections whose delta is >= --min on all
seeds (adjacent winners merged with --merge). A full-song transfer that is mixed by section (Flim's bass stemvel,
Thin Thing's drum retime: +1.2 in some sections, -1.6 in others) is usually worth keeping where it wins.
"""
import json
import sys


def main(a):
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    secs = [float(x) for x in open(a[0]).read().strip().split(",")]
    base = [json.load(open(p)) for p in a[1].split(",")]
    var = [json.load(open(p)) for p in a[2].split(",")]
    if len(base) != len(var):
        sys.exit("base and variant lists must pair up (same seeds)")
    lo = opt("--min", 0.1)
    print("totals: base " + " ".join(f"{b['total']:.2f}" for b in base) + " | variant " + " ".join(f"{v['total']:.2f}" for v in var))
    wins = []
    for i in range(len(secs) - 1):
        d = [v["sections"][i]["total"] - b["sections"][i]["total"] for b, v in zip(base, var)]
        ok = all(x >= lo for x in d)
        print(f"{'*' if ok else ' '} section {i + 1:2d} {secs[i]:7.1f}-{secs[i + 1]:7.1f}: Δ " + " ".join(f"{x:+.2f}" for x in d))
        if ok:
            wins.append([secs[i], secs[i + 1]])
    if "--merge" in a:
        merged = []
        for w in wins:
            if merged and abs(merged[-1][1] - w[0]) < 1e-6:
                merged[-1][1] = w[1]
            else:
                merged.append(list(w))
        wins = merged
    print("--only-in " + ",".join(f"{x:g}-{y:g}" for x, y in wins) if wins else "no section wins on every seed")


if __name__ == "__main__":
    main(sys.argv[1:])
