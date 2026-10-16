#!/usr/bin/env python3
"""Stem transcription as a RAW part on a tab2song map's real bar sequence — skips and repeats applied, so every
played copy of a repeated tab measure gets its own transcription (stemnotes --map keys bars by tab measure number,
which a score_file cannot tell apart).

  stemraw.py MAP.json STEM.wav OUT.json [--key k] [--from S] [--to S] [--lo MIDI] [--hi MIDI] [--th 0.25]
             [--merge 0.6] [--floor D]

Transcribes the bars that start inside --from..--to (seconds; default the whole song) with stemnotes.transcribe on
the map's bar times (barmatch.bars), and writes {key: {score}} with the leading rest (the map's offset at the
opening tempo plus every earlier bar's beats) — ready for a map part {"raw": "OUT.json#k", "patch": …}; mute the
tab part over the same measures (its "bars") so the two do not double.
"""
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


BM, SN, T2S = load("barmatch"), load("stemnotes"), load("tab2song")


def main(a):
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    mp = json.load(open(a[0])); stem, out = a[1], a[2]
    bl = BM.bars(mp)
    beats_of = {m["m"]: m["beats"] for m in T2S.corrected_timeline(mp["cache"], mp)}
    t0, t1 = opt("--from", -1.0), opt("--to", 1e9)
    idx = [j for j, (_, t, _) in enumerate(bl) if t0 <= t < t1]
    if not idx:
        sys.exit("no bars start in that range")
    j0, j1 = idx[0], idx[-1]
    spans = {j: (bl[j][1], bl[j][2], beats_of[bl[j][0]]) for j in range(j0, j1 + 1)}
    full = T2S.corrected_timeline(mp["cache"], mp)
    first_bpm = next(m["bpm"] for m in full if not m["skip"])
    lead = round(mp.get("offset", 0.0) * first_bpm / 60, 4) + sum(beats_of[bl[j][0]] for j in range(j0))
    fl = opt("--floor", 0.0) if "--floor" in a else None
    lines = [line for _, line in SN.transcribe(stem, 0.0, 0.0, j0, j1, opt("--lo", 23), opt("--hi", 52),
                                               opt("--th", 0.25), opt("--merge", 0.6), fl, spans)]
    score = f"R/{lead:g}b " + " ".join(lines)
    json.dump({opt("--key", "k"): {"score": score}}, open(out, "w"))
    notes = sum(1 for t in score.split() if "/" in t and not t.startswith("R/"))
    print(f"bars #{j0}-#{j1} (m{bl[j0][0]}-m{bl[j1][0]}, {bl[j0][1]:.2f}-{bl[j1][1] + bl[j1][2]:.2f} s): {notes} notes, "
          f"lead rest {lead:g} beats → {out}")


if __name__ == "__main__":
    main(sys.argv[1:])
