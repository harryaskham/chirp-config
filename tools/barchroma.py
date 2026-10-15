#!/usr/bin/env python3
"""Per-bar pitch audit of a tab2song part against a stem: for every kept measure, the stem's chroma over that bar's
real time span is compared with the pitch classes the tab's part plays there. Bars where the recording's dominant
pitch classes are not what the tab plays are listed worst-first — candidates for a part's "replace" corrections
(tab2song.py), which Pneuma's hold (tab: D5 held; record: A/E voicings, then A) and Shadows' transitions needed.

  barchroma.py MAP.json PART STEM.wav [--bars A-B] [--top 20] [--min-level -45] [--emit OUT.json --min-gain 0.25]

Per bar: the stem's chroma (30 Hz-2 kHz, 0.7 Hz bins) against the chroma the tab's notes should produce with
their harmonics (1-8 at 1/h, so a low note's fifth-up 3rd harmonic is expected), and against the same notes
transposed by 1..11 semitones; bars where a transposition fits clearly better are listed first with the
suggested shift. Bars where the stem is near-silent (below --min-level dB) or the tab rests are skipped."""
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


def note_midis(line):
    out = []
    for tok in line.split():
        head = tok.split("/")[0]
        for n in head.split(","):
            m = re.match(r"^([A-G](?:#|b)?)(-?\d+)$", n)
            if m:
                out.append(12 * (int(m.group(2)) + 1) + PC[m.group(1)])
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


SUG = {}   # bar -> (fit gain, best shift, tab line)


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
    tl = T.corrected_timeline(cache, mp)
    lines = S.score(cache, part["track"])[2]
    rep = {int(k): v for k, v in part.get("replace", {}).items()}
    lo, hi = (int(v) for v in opt("--bars", "1-100000").split("-"))
    t, rows = mp.get("offset", 0.0), []
    for m in tl:
        if m["skip"]:
            continue
        dur = m["beats"] * 60 / m["bpm"]
        if lo <= m["m"] <= hi:
            line = rep.get(m["m"], lines[m["m"] - 1])
            pcs = note_pcs(line)
            seg = x[int(t * 48000):int((t + dur) * 48000)]
            lvl = 10 * np.log10(np.mean(seg ** 2) + 1e-12) if len(seg) else -120
            if pcs and lvl > opt("--min-level", -45.0):
                c = chroma(seg); cn = c / (np.linalg.norm(c) + 1e-12)
                mids = note_midis(line)
                fit = [float(cn @ predicted(mids, k)) for k in range(12)]
                best = int(np.argmax(fit)); gain = fit[best] - fit[0]
                top = " ".join(f"{NAMES[k]}{100 * c[k]:.0f}" for k in np.argsort(c)[::-1][:4])
                sug = f"try {best:+d} st ({fit[0]:.2f} → {fit[best]:.2f})" if best else f"fits ({fit[0]:.2f})"
                rows.append((gain, m["m"], t, top, sug, line[:56]))
                SUG[m["m"]] = (gain, best, line)
        t += dur
    rows.sort(reverse=True)
    for gain, mm, tt, top, sug, line in rows[:opt("--top", 20)]:
        print(f"m{mm:<4} {tt:7.1f}s  stem: {top:24} {sug:28} | {line}")
    if rows:
        print(f"{sum(1 for r in rows if r[0] > 0.15)} of {len(rows)} bars fit a transposition better by > 0.15")
    if "--emit" in a:
        # replace entries for tab2song: each flagged bar transposed by its suggested shift, taken as the smallest
        # equivalent interval (+7 -> -5) that keeps the bar inside the part's range (chroma does not know octaves)
        mg = opt("--min-gain", 0.25)
        floor_note = min((n for _, _, ln in SUG.values() for n in note_midis(ln)), default=0)   # the part's range

        def shift(k, line):
            low = min(note_midis(line))
            ok = [c for c in (k, k - 12) if low + c >= floor_note]     # never below the instrument's lowest note
            return min(ok, key=abs) if ok else k
        out = {str(m): transpose(line, shift(k, line)) for m, (g, k, line) in sorted(SUG.items()) if k and g > mg}
        json.dump(out, open(opt("--emit", ""), "w"), indent=1)
        print(f"emitted {len(out)} bar corrections (gain > {mg})")


if __name__ == "__main__":
    main(sys.argv[1:])
