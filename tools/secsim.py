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

Under each render's lines, THE TERM: the recurrence term is the MEAN of what each cut scores (100 with its share in
the band, falling away outside it), so the line gives each cut's score and names the cuts under 100. A term of 96.4
is usually six cuts at 100 and ONE outside the band, not every cut a little short.
With two renders or more (the kept version, then the candidate): WHAT CHANGED from each to the next, for the cuts
whose score moved: the seams that are GONE (two sections now one: it counts once where it counted twice), NEW or
MOVED (a seam within 3 s of an old one is the same seam; within 12 s it moved), and each section on the same span
whose best match now counts a tenth of a return more or less. (chirper-zero, 16 Nov: four rounds in one night were kept against a lower
recurrence, each explained by reading two blocks of seven lines against each other by hand; on Plain Hunt v15 the
matches that fell, 0.80 -> 0.70, were all still inside the band, and the 3.6 points were one cut where the seam at
206 s was no longer found.)
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


SAME_S, MOVED_S = 3.0, 12.0     # a seam this close to an old one is the same seam; this close, it moved
CREDIT_MOVED = 0.1              # a section whose best match counts this much more or less of a return is said


def seams(old, new):
    """What became of the seams between two sets of sections: {gone: [t], new: [t], moved: [(from, to)]}."""
    a, b = [s["b"] for s in old[:-1]], [s["b"] for s in new[:-1]]
    kept, moved, gone = set(), [], []
    for t in a:
        near = min(b, key=lambda u: abs(u - t), default=None)
        if near is not None and abs(near - t) <= SAME_S:
            kept.add(near)
    for t in a:
        if any(abs(u - t) <= SAME_S for u in b):
            continue
        free = [u for u in b if u not in kept and abs(u - t) <= MOVED_S]
        if free:
            u = min(free, key=lambda v: abs(v - t))
            kept.add(u)
            moved.append((t, u))
        else:
            gone.append(t)
    return {"gone": gone, "new": [u for u in b if u not in kept], "moved": moved}


def changed(old, new, old_line, new_line):
    """The lines saying what changed between one cut's sections in two renders (old_line, new_line: returns()'s items)."""
    def at(secs, t):
        return max(range(len(secs)), key=lambda i: min(secs[i]["b"], t + 1e-6) - max(secs[i]["a"], t - 1e-6))
    got, out = seams(old, new), []
    for t in got["gone"]:
        i = next(k for k, s in enumerate(old[:-1]) if s["b"] == t)
        out.append(f"the seam at {t:.0f} s is GONE: {old_line[i]} and {old_line[i + 1]} are now one section {new_line[at(new, t)]}: "
                   "it counts once where it counted twice")
    for t in got["new"]:
        i = next(k for k, s in enumerate(new[:-1]) if s["b"] == t)
        out.append(f"a NEW seam at {t:.0f} s: {old_line[at(old, t)]} is now {new_line[i]} and {new_line[i + 1]}")
    for t, u in got["moved"]:
        out.append(f"the seam at {t:.0f} s MOVED to {u:.0f} s")
    for j, s in enumerate(new):
        for i, o in enumerate(old):
            if abs(o["a"] - s["a"]) <= MOVED_S and abs(o["b"] - s["b"]) <= MOVED_S and "~" in old_line[i] and "~" in new_line[j]:
                was, now = float(old_line[i].rsplit(":", 1)[1]), float(new_line[j].rsplit(":", 1)[1])
                if abs(cs_credit(now) - cs_credit(was)) >= CREDIT_MOVED:
                    out.append(f"{old_line[i]} -> {new_line[j]}: it returns {'LESS' if now < was else 'MORE'} "
                               f"({cs_credit(was):.2f} -> {cs_credit(now):.2f} of a return)")
    return out


def cs_credit(sim):
    """How much of a return a best match counts as: 0 at RETURN[0], 1 at RETURN[1]."""
    return float(np.clip((sim - cs.RETURN[0]) / (cs.RETURN[1] - cs.RETURN[0]), 0, 1))


def term_line(scores, shares, lo, hi):
    """THE TERM under a render's lines: the mean of the cuts' scores, and which cuts are under 100."""
    if not scores or any(v is None for v in scores):
        return ""
    under = [f"cut {i + 1} at {v:.1f} (share {shares[i]:.3f}, {'under the floor' if shares[i] < lo else 'over the ceiling'} "
             f"{lo if shares[i] < lo else hi:g})" for i, v in enumerate(scores) if v < 99.95 and shares[i] is not None]
    return (f"THE TERM: {float(np.mean(scores)):.1f}, the mean of the cuts' " + " ".join(f"{v:.1f}" for v in scores)
            + ("; under 100: " + "; ".join(under) if under else ""))


def what_changed(a, b):
    """The lines of WHAT CHANGED between two renders' readings ({name, sets, lines, shares, scores})."""
    if len(a["sets"]) != len(b["sets"]) or any(v is None for v in a["scores"] + b["scores"]):
        return []
    out = [f"WHAT CHANGED, {a['name']} -> {b['name']}: the term {float(np.mean(a['scores'])):.1f} -> {float(np.mean(b['scores'])):.1f}"]
    still = []
    for i in range(len(a["sets"])):
        if abs(a["scores"][i] - b["scores"][i]) < 0.05:
            still.append(i)
            continue
        out.append(f"  cut {i + 1} (n={len(a['sets'][i])} -> {len(b['sets'][i])}): {a['scores'][i]:.1f} -> {b['scores'][i]:.1f} "
                   f"(share {a['shares'][i]:.3f} -> {b['shares'][i]:.3f})")
        out += ["      " + ln for ln in changed(a["sets"][i], b["sets"][i], a["lines"][i], b["lines"][i])]
    if still:
        d = [b["shares"][i] - a["shares"][i] for i in still if a["shares"][i] is not None and b["shares"][i] is not None]
        out.append(f"  the {'other ' if len(still) < len(a['sets']) else ''}{len(still)} cut(s) score the same before and after"
                   + (f" (their shares moved {min(d):+.3f} to {max(d):+.3f})" if d else ""))
    return out


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
    read = []
    for wav in wavs:
        ctx = cs.build_ctx(cid, wav, climb, album, song)
        sets = ctx["section_sets"] or [ctx["sections"]]
        print(os.path.basename(wav), " cuts tried:", [len(s) for s in sets])
        shares, lines = [], []
        for secs in sets:
            share, line = returns(secs)
            shares.append(share)
            lines.append(line)
            print(f"  n={len(secs)} share={float('nan') if share is None else share:.3f} | " + " ".join(line))
        note = cs.edge_note(shares, lo, hi)
        if note:
            print(f"  {note} (the album's band is {lo:g}-{hi:g})")
        scores = [cs.m_recurrence({**ctx, "sections": secs})[0] if len(secs) >= 3 else None for secs in sets]
        term = term_line(scores, shares, lo, hi)
        if term:
            print(f"  {term}")
        twice = [os.path.basename(w) for w in wavs].count(os.path.basename(wav)) > 1      # two n-0.wav: say whose
        name = os.path.join(os.path.basename(os.path.dirname(os.path.abspath(wav))), os.path.basename(wav)) if twice \
            else os.path.basename(wav)
        read.append({"name": name, "sets": sets, "lines": lines, "shares": shares, "scores": scores})
    for a, b in zip(read, read[1:]):
        for ln in what_changed(a, b):
            print(ln)
    return 0


if __name__ == "__main__":
    sys.exit(main())
