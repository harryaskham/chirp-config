#!/usr/bin/env python3
"""Per-window transposition of a raw part against a reference stem's chroma — the pitch-tracker slips (a fifth from a
subharmonic, an octave-equivalent class error) and a tab line in the wrong key or mode for a passage.

  stemtranspose.py SONG.yaml RAW.json#key STEM.wav OURS.wav OUT.json [--win 2] [--shifts -7..7] [--margin 0.12]
                   [--min 0.5] [--only 1,-1,7,-7]

SONG.yaml gives the tempo map (the song the raw part plays in); OURS.wav is a solo render of that part (`chirp render
--solo NAME`). Every note gets its time from the tempo map; in each --win-second window the stem's chroma
(100 Hz-2 kHz) is compared with ours rolled by every shift; when a non-zero shift beats no shift by --margin and
reaches --min cosine, the window's notes move by it (--only restricts the allowed shifts). Prints the shift histogram
and writes OUT.json with the same key. Chroma has no octave: check octaves separately (spectral centroid).
Check the histogram before trusting a result: a few dominant shifts (e.g. +7 in a run of windows) are real slips;
shifts scattered over -7..+7 mean the stem's chroma is too noisy per window (a gritty, vibrato-heavy vocal: 2 Minutes
to Midnight's Bruce Dickinson line) — then restrict --only or widen --win, and judge by the song score.
"""
import json
import re
import sys

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import likeness as L  # noqa: E402

NAMES = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
SHARP = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
NOTE = re.compile(r"([A-G])(#|b)?(-?\d)")


def tempo_map(song_text):
    m = re.search(r"^tempo: (.*)$", song_text, re.M)
    t = json.loads(m.group(1))
    if isinstance(t, (int, float)):
        return [(0.0, float(t))]
    return [(float(str(e["at"]).rstrip("b")), float(e["bpm"])) for e in t]


def beat_to_s(tm, b):
    s = 0.0
    for i, (at, bpm) in enumerate(tm):
        nxt = tm[i + 1][0] if i + 1 < len(tm) else float("inf")
        if b <= at:
            break
        s += (min(b, nxt) - at) * 60.0 / bpm
    return s


def shift_note(tok, k):
    def rep(m):
        midi = 12 * (int(m.group(3)) + 1) + NAMES[m.group(1)] + {"#": 1, "b": -1, None: 0}[m.group(2)] + k
        return f"{SHARP[midi % 12]}{midi // 12 - 1}"
    head, _, rest = tok.partition("/")
    return NOTE.sub(rep, head) + "/" + rest


def chroma(x, a, b):
    s = x[int(a * 48000):int(b * 48000)]
    if len(s) < 4800:
        return None
    X = np.abs(np.fft.rfft(s * np.hanning(len(s)))) ** 2
    f = np.fft.rfftfreq(len(s), 1 / 48000)
    sel = (f > 100) & (f < 2000)
    c = np.bincount(np.round(69 + 12 * np.log2(f[sel] / 440)).astype(int) % 12, weights=X[sel], minlength=12)
    return c / (np.linalg.norm(c) + 1e-12)


def main(a):
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    song, raw, stem, ours, out = a[:5]
    path, _, key = raw.partition("#")
    data = json.load(open(path)); toks = data[key]["score"].split()
    tm = tempo_map(open(song).read())
    win, margin, floor = opt("--win", 2.0), opt("--margin", 0.12), opt("--min", 0.5)
    allowed = [int(v) for v in opt("--only", "").split(",")] if "--only" in a else [k for k in range(-7, 8) if k]
    # note times
    pos, notes = 0.0, []
    for i, t in enumerate(toks):
        m = re.search(r"/([0-9.]+)b", t)
        if not m:
            continue
        d = float(m.group(1))
        if not t.startswith("R/") and NOTE.match(t):
            notes.append((i, beat_to_s(tm, pos)))
        pos += d
    S = L.load(stem).mean(1); O = L.load(ours).mean(1)
    hist = {}; moved = 0
    if notes:
        t0, t1 = notes[0][1], notes[-1][1] + win
        for a0 in np.arange(t0, t1, win):
            cs, co = chroma(S, a0, a0 + win), chroma(O, a0, a0 + win)
            if cs is None or co is None or co.sum() == 0:
                continue
            base = float(cs @ co)
            best = max(allowed, key=lambda k: float(cs @ np.roll(co, k)))
            bv = float(cs @ np.roll(co, best))
            k = best if (bv - base > margin and bv >= floor) else 0
            hist[k] = hist.get(k, 0) + 1
            if k:
                for i, ts in notes:
                    if a0 <= ts < a0 + win:
                        toks[i] = shift_note(toks[i], k); moved += 1
    data[key]["score"] = " ".join(toks)
    json.dump(data, open(out, "w"), ensure_ascii=False)
    print(f"{len(notes)} notes; window shifts {dict(sorted(hist.items()))}; {moved} notes moved → {out}")


if __name__ == "__main__":
    main(sys.argv[1:])
