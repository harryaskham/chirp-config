#!/usr/bin/env python3
"""Per-note dynamics from a stem: every note of a song track gets the velocity of the reference performance — the
stem's level over the note's middle, relative to the track's median sung level — written as `@V` (replacing any
existing velocity; other articulations kept). A tab or a transcription gives notes at one velocity; the record's
singer or player swells and recedes, and the level contour is a large share of a part's likeness.

  stemvel.py STEM.wav SONG.yaml TRACK OUT.json [--key vox] [--range 40-120] [--mid V] [--slope 2.5]

--mid: velocity at the median level (default the range's middle; chirp's unmarked notes play at 100).

slope: velocity units per dB around the median (so ±16 dB spans 40-120 at 2.5). Notes where the stem is silent
keep the median velocity."""
import json
import os
import re
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stemvowels as V  # noqa: E402
import drumtrans as D  # noqa: E402
import likeness as L  # noqa: E402

SR = 48000


def run(stem, song, track, key="vox", lo=40, hi=120, slope=2.5, mid=None):
    x = L.load(stem).mean(1)
    pts = D.tempo_points(song)
    beats = np.array([b for b, _ in pts]); bpm = np.array([v for _, v in pts])
    secs = np.concatenate([[0.0], np.cumsum(np.diff(beats) * 60 / bpm[:-1])])

    def b2t(b):
        i = max(0, np.searchsorted(beats, b, side="right") - 1)
        return secs[i] + (b - beats[i]) * 60 / bpm[i]

    toks, notes, pos = V.track_tokens(song, track), [], 0.0
    for t in toks:
        m = re.match(r"^([^/]+)/([0-9.]+)b(.*)$", t)
        if not m:
            notes.append((t, None)); continue
        body, ln, rest = m.group(1), float(m.group(2)), m.group(3)
        if body in ("R", "r", "_"):
            notes.append((t, None)); pos += ln; continue
        a, e = b2t(pos), b2t(pos + ln)
        d = e - a
        seg = x[int((a + 0.15 * d) * SR):int((e - 0.15 * d) * SR)]
        lvl = 10 * np.log10(np.mean(seg ** 2) + 1e-12) if len(seg) > 64 else None
        notes.append(((body, m.group(2), rest), lvl))
        pos += ln
    sung = [l for _, l in notes if l is not None and l > -70]
    med = float(np.median(sung)) if sung else -30.0
    mid = (lo + hi) / 2 if mid is None else mid
    out = []
    for tok, lvl in notes:
        if lvl is None and isinstance(tok, str):
            out.append(tok); continue
        body, ln, rest = tok
        v = int(np.clip(mid + slope * ((lvl if lvl is not None and lvl > -70 else med) - med), lo, hi))
        rest = re.sub(r"@\d+", "", rest)
        out.append(f"{body}/{ln}b@{v}{rest}")
    return {key: {"score": " ".join(out)}}, med, len(sung)


if __name__ == "__main__":
    a = sys.argv[1:]
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    lo, hi = (int(v) for v in opt("--range", "40-120").split("-"))
    res, med, n = run(a[0], a[1], a[2], opt("--key", "vox"), lo, hi, opt("--slope", 2.5), opt("--mid", 100.0) if "--mid" in a else None)
    json.dump(res, open(a[3], "w"))
    print(f"{n} sung notes; median stem level {med:.1f} dB")
