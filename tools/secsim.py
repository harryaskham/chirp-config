#!/usr/bin/env python3
"""secsim: WHICH SECTIONS RETURN. The scorer's own sections of a render, and for each one from the third on the
earlier, non-adjacent section it best matches and how well: the recurrence term's input, laid out.
(chirper-zero's, Plain Hunt v6, 14 Nov; promoted by chirp-eco. The recurrence term fell on one seed and a guessed
cure made it worse; printing the scorer's sections and each one's best earlier match showed the cause at once: a bare
passage had changed the first cycle's middle section, so the second cycle's matched it less, 0.70 -> 0.63. The same
passage at the same place in BOTH cycles: 100 on both seeds.)

  secsim.py ID WAV [WAV ...] [--song YAML]

ID is the climb (its album gives the novelty cuts and the recurrence band); each WAV a render of it (--song when the
render came from a candidate file). For each render, one line for each of the album's novelty cuts:
  n=11 share=0.341 | 0[0-16s] 1[16-34s] 2[34-71s]~0:0.08 3[71-108s]~1:0.99 ...
n is how many sections that cut finds; each section is its number and its seconds; from the third on, "~j:sim" is the
earlier section (not the one just before) it is most like, and the likeness (the cosine of the two sections' mean
frames: spectral shape, chroma and level). A likeness of 0.45 counts nothing as a return and 0.75 counts fully
(compscore.RETURN); `share` is the mean of that over the sections, and the term is 100 while the share is inside
the album's band. A share within 0.02 of the band's end is marked ON THE EDGE: there the term reads 100 and says
nothing until the next change tips it (Plain Hunt v5 sat at 0.252 against a floor of 0.25).
Read-only. Tests: tools/tests/test_secsim.py.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import compscore as cs  # noqa: E402

def returns(secs):
    """(share, the line's items) for one cut's sections: each section "i[a-bs]", from the third on with "~j:sim", the
    earlier non-adjacent section it best matches. share is None with fewer than three sections."""
    fr, line = [], []
    for i, s in enumerate(secs):
        if i >= 2:
            sims = [cs._sim(s, secs[j]) for j in range(0, i - 1)]
            j = int(np.argmax(sims))
            b = sims[j]
            fr.append(float(np.clip((b - cs.RETURN[0]) / (cs.RETURN[1] - cs.RETURN[0]), 0, 1)))
            line.append(f"{i}[{s['a']:.0f}-{s['b']:.0f}s]~{j}:{b:.2f}")
        else:
            line.append(f"{i}[{s['a']:.0f}-{s['b']:.0f}s]")
    return (float(np.mean(fr)) if fr else None), line


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    song = None
    if "--song" in args:
        i = args.index("--song")
        song = args[i + 1]
        del args[i:i + 2]
    if len(args) < 2 or "-h" in args or "--help" in args:
        print(__doc__)
        return 0 if ("-h" in args or "--help" in args) else 2
    cid, wavs = args[0], args[1:]
    reg = cs.registry()
    climb = cs.climb_of(cid, reg)
    album = cs.load_album(climb["album"])
    lo, hi = cs.recurrence_band(album)
    for wav in wavs:
        ctx = cs.build_ctx(cid, wav, climb, album, song)
        sets = ctx["section_sets"] or [ctx["sections"]]
        print(os.path.basename(wav), " cuts tried:", [len(s) for s in sets])
        shares = []
        for secs in sets:
            share, line = returns(secs)
            shares.append(share)
            print(f"  n={len(secs)} share={float('nan') if share is None else share:.3f} | " + " ".join(line))
        note = cs.edge_note(shares, lo, hi)
        if note:
            print(f"  {note} (the album's band is {lo:g}-{hi:g})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
