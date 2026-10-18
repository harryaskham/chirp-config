#!/usr/bin/env python3
"""Per-bar pitch audit of a tab2song part against a stem: for every kept measure, the stem's chroma over that bar's
real time span is compared with the pitch classes the tab's part plays there. Bars where the recording's dominant
pitch classes are not what the tab plays are listed worst-first — candidates for a part's "replace" corrections
(tab2song.py), which Pneuma's hold (tab: D5 held; record: A/E voicings, then A) and Shadows' transitions needed.

  barchroma.py MAP.json PART STEM.wav [--bars A-B] [--top 20] [--min-level -45] [--emit OUT.json --min-gain 0.25 [--emit-bent]]

Per bar: the stem's chroma (30 Hz-2 kHz, 0.7 Hz bins) against the chroma the tab's notes should produce with
their harmonics (1-8 at 1/h, so a low note's fifth-up 3rd harmonic is expected), and against the same notes
transposed by 1..11 semitones; bars where a transposition fits clearly better are listed first with the
suggested shift. Bars where the stem is near-silent (below --min-level dB) or the tab rests are skipped.

Bends (bd-0467c9): `bend=X` latches (across notes, holds and bar lines) until `bend=` resets it, so the written
pitch is not the sounding one. A bar a bend touches (a bend= token, or a bend carried in) is predicted from its
sounding pitches — each note and hold at its bent pitch, weighted by its length; a fractional bend splits
between neighbouring classes — and marked `bent`. Bend-free bars keep the written-note signature. A suggested
shift for a bent bar is a shift of the sounding pitch: transpose (which keeps the bend tokens) applies exactly it,
never the bend twice. --emit still leaves bent bars out (listed, not written): a bent bar that does not fit is
usually a bend-shape problem (a tab bend-and-release becomes one held bend at its peak), not a transposition;
--emit-bent writes them too."""
import json
import os
import re
import sys
import importlib.util

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import likeness as L  # noqa: E402

spec = importlib.util.spec_from_file_location("t2s", os.path.join(HERE, "tab2song.py"))
T = importlib.util.module_from_spec(spec); spec.loader.exec_module(T)
import songsterr as S  # noqa: E402

NAMES = "C C# D D# E F F# G G# A A# B".split()
PC = {n: i for i, n in enumerate(NAMES)}
PC.update({"Db": 1, "Eb": 3, "Gb": 6, "Ab": 8, "Bb": 10})


def note_midis(line, sounding=True):
    """Sounding pitches, including the tab's latched semitone bend (``bend=`` resets it).

    Songsterr writes the bend before its note: ignoring it audits the written fret rather than the
    pitch chirp plays, so a correctly bent note can look like a whole-bar transposition error.
    """
    out, bend = [], 0.0
    for tok in line.split():
        if tok.startswith("bend="):
            bend = float(tok.partition("=")[2] or 0)
            continue
        head = tok.split("/")[0]
        for n in head.split(","):
            m = re.match(r"^([A-G](?:#|b)?)(-?\d+)$", n)
            if m:
                out.append(12 * (int(m.group(2)) + 1) + PC[m.group(1)] + (bend if sounding else 0))
    return out


def note_pcs(line):
    return {k % 12 for k in note_midis(line)}


def predicted(midis, shift=0):
    """Chroma a set of notes should produce, harmonics 1-8 at 1/h (a low bass note's 3rd harmonic is a fifth up)."""
    c = np.zeros(12)
    for n in midis:
        for h in range(1, 9):
            c[int(round(n + shift + 12 * np.log2(h))) % 12] += 1.0 / h
    return c / (np.linalg.norm(c) + 1e-12)


def tok_beats(rest):
    """A token's length in beats from what follows its '/': `2b`, `4` (a quarter), `8.` (dotted); None if unknown."""
    body = re.split(r"[@^]", rest, maxsplit=1)[0]
    m = re.match(r"^(\d+(?:\.\d+)?)b", body)
    if m:
        return float(m.group(1))
    m = re.match(r"^(\d+)(\.?)", body)
    if m and int(m.group(1)) > 0:
        return 4 / int(m.group(1)) * (1.5 if m.group(2) else 1)
    return None


def bar_segments(line, bend=0.0, held=()):
    """A bar's sounding pitches: ([(midi + bend, beats)] for each note and hold, the bend after the bar, the notes
    still held, whether a bend touched the bar). `bend=X` latches until `bend=`; `_` holds the previous notes
    (across the bar line too) at the current bend. A token without a length takes the previous one's."""
    segs, held, bent, last = [], list(held), abs(bend) > 1e-9, 1.0
    for tok in line.split():
        if tok.startswith("bend="):
            v = tok[5:]
            bend, bent = (float(v) if v else 0.0), True
            continue
        head, sep, rest = tok.partition("/")
        if "=" in head:   # other settings and controls
            continue
        d = (tok_beats(rest) if sep else None) or last
        last = d
        if head in ("R", "r", "."):
            held = []
            continue
        if head == "_":
            segs += [(m + bend, d) for m in held]
            continue
        mids = []
        for n in head.split(","):
            mm = re.match(r"^([A-G](?:#|b)?)(-?\d+)", n)
            if mm:
                mids.append(12 * (int(mm.group(2)) + 1) + PC[mm.group(1)])
        held = mids
        segs += [(m + bend, d) for m in mids]
    return segs, bend, held, bent


def predicted_segments(segs, shift=0):
    """predicted() for sounding pitches with lengths: each weighted by its beats, a fractional (bent) pitch split
    between its two neighbouring classes; harmonics 1-8 at 1/h as there."""
    c = np.zeros(12)
    for n, w in segs:
        lo = np.floor(n + shift)
        frac = n + shift - lo
        for h in range(1, 9):
            k = int(lo) + int(round(12 * np.log2(h)))
            c[k % 12] += w * (1 - frac) / h
            c[(k + 1) % 12] += w * frac / h
    return c / (np.linalg.norm(c) + 1e-12)


SUG = {}   # bar -> (fit gain, best shift, tab line, bent)


def transpose(line, k):
    """Shift every note of a tab line by k semitones, keeping durations and articulations."""
    def one(tok):
        head, sep, rest = tok.partition("/")
        if not sep or head in ("R", "r", "_"):
            return tok
        out = []
        for n in head.split(","):
            m = re.match(r"^([A-G](?:#|b)?)(-?\d+)$", n)
            if not m:
                return tok
            mi = 12 * (int(m.group(2)) + 1) + PC[m.group(1)] + k
            out.append(f"{NAMES[mi % 12]}{mi // 12 - 1}")
        return ",".join(out) + sep + rest
    return " ".join(one(t) for t in line.split())


def chroma(x):
    n = 32768                       # 0.7 Hz bins: low notes must not smear into their neighbours' classes
    acc = np.zeros(12)
    f = np.fft.rfftfreq(n, 1 / 48000)
    m = (f > 30) & (f < 2000)
    pc = ((np.round(12 * np.log2(f[m] / 440)) + 9) % 12).astype(int)
    for i in range(0, max(1, len(x) - n), n // 2):
        seg = x[i:i + n]
        if len(seg) < n:
            break
        sp = np.abs(np.fft.rfft(seg * np.hanning(n))) ** 2
        acc += np.bincount(pc, weights=sp[m], minlength=12)
    return acc / (acc.sum() + 1e-12)


def main(a):
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    mp = json.load(open(a[0])); part = next(p for p in mp["parts"] if p["name"] == a[1])
    x = L.load(a[2]).mean(1)
    root = os.path.dirname(HERE)
    cache = mp["cache"] if os.path.isabs(mp["cache"]) else os.path.join(root, mp["cache"])
    tl = T.performed_timeline(cache, mp)  # the performed clock: skips and repeats (bd-8e945f)
    lines = S.score(cache, part["track"])[2]
    rep = {int(k): v for k, v in part.get("replace", {}).items()}
    lo, hi = (int(v) for v in opt("--bars", "1-100000").split("-"))
    # the bend state and held notes carry across bars in play order; outside its `bars` the part rests (no bends)
    plays = set()
    for a_, b_ in part.get("bars", [[1, len(lines)]]):
        plays.update(range(a_, b_ + 1))
    bend, held = 0.0, []
    t, rows = mp.get("offset", 0.0), []
    for m in tl:
        if m["skip"]:
            continue
        dur = m["beats"] * 60 / m["bpm"]
        line = rep.get(m["m"], lines[m["m"] - 1])
        if m["m"] in plays:
            segs, bend_after, held_after, bent = bar_segments(line, bend, held)
        else:
            segs, bend_after, held_after, bent = [], bend, [], False
        if lo <= m["m"] <= hi:
            pcs = note_pcs(line)
            seg = x[int(t * 48000):int((t + dur) * 48000)]
            lvl = 10 * np.log10(np.mean(seg ** 2) + 1e-12) if len(seg) else -120
            if (segs if bent else pcs) and lvl > opt("--min-level", -45.0):
                c = chroma(seg); cn = c / (np.linalg.norm(c) + 1e-12)
                if bent:   # the sounding (bent) pitches, by length
                    fit = [float(cn @ predicted_segments(segs, k)) for k in range(12)]
                else:
                    mids = note_midis(line)
                    fit = [float(cn @ predicted(mids, k)) for k in range(12)]
                best = int(np.argmax(fit)); gain = fit[best] - fit[0]
                top = " ".join(f"{NAMES[k]}{100 * c[k]:.0f}" for k in np.argsort(c)[::-1][:4])
                sug = f"try {best:+d} st ({fit[0]:.2f} → {fit[best]:.2f})" if best else f"fits ({fit[0]:.2f})"
                if bent:
                    sug += " bent"
                rows.append((gain, (m["m"], m["occ"]), m["label"], t, top, sug, line[:56]))
                SUG.setdefault(m["m"], (gain, best, line, bent))   # replace is per tab measure: its first play's
        bend, held = bend_after, held_after
        t += dur
    rows.sort(reverse=True)
    for gain, _, mm, tt, top, sug, line in rows[:opt("--top", 20)]:
        print(f"m{mm:<4} {tt:7.1f}s  stem: {top:24} {sug:28} | {line}")
    if rows:
        print(f"{sum(1 for r in rows if r[0] > 0.15)} of {len(rows)} bars fit a transposition better by > 0.15")
    if "--emit" in a:
        # replace entries for tab2song: each flagged bar transposed by its suggested shift, taken as the smallest
        # equivalent interval (+7 -> -5) that keeps the bar inside the part's range (chroma does not know octaves)
        mg = opt("--min-gain", 0.25)
        # Range limits describe written frets, not a note's temporary bend offset.
        floor_note = min((n for _, _, ln, _ in SUG.values() for n in note_midis(ln, sounding=False)), default=0)

        def shift(k, line):
            low = min(note_midis(line, sounding=False))
            ok = [c for c in (k, k - 12) if low + c >= floor_note]     # never below the instrument's lowest note
            return min(ok, key=abs) if ok else k
        bent_too = "--emit-bent" in a
        out = {str(m): transpose(line, shift(k, line)) for m, (g, k, line, bent) in sorted(SUG.items())
               if k and g > mg and (bent_too or not bent)}
        held = [m for m, (g, k, line, bent) in sorted(SUG.items()) if k and g > mg and bent and not bent_too]
        if held:
            print(f"{len(held)} bent bars not emitted (check their bends; --emit-bent writes them): "
                  + ", ".join(map(str, held[:20])) + (" …" if len(held) > 20 else ""))
        json.dump(out, open(opt("--emit", ""), "w"), indent=1)
        print(f"emitted {len(out)} bar corrections (gain > {mg})")


if __name__ == "__main__":
    main(sys.argv[1:])
