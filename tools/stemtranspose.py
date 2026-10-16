#!/usr/bin/env python3
"""Per-window transposition of a raw part against a reference stem's chroma — the pitch-tracker slips (a fifth from a
subharmonic, an octave-equivalent class error) and a tab line in the wrong key or mode for a passage.

  stemtranspose.py SONG.yaml RAW.json#key STEM.wav OURS.wav OUT.json [--win 2] [--shifts -7..7] [--margin 0.12]
                   [--min 0.5] [--only 1,-1,7,-7]
                   [--per-note [--max-shift 2] [--yin 0.15]]

SONG.yaml gives the tempo map (the song the raw part plays in); OURS.wav is a solo render of that part (`chirp render
--solo NAME`). Every note gets its time from the tempo map; in each --win-second window the stem's chroma
(100 Hz-2 kHz) is compared with ours rolled by every shift; when a non-zero shift beats no shift by --margin and
reaches --min cosine, the window's notes move by it (--only restricts the allowed shifts). Prints the shift histogram
and writes OUT.json with the same key. Chroma has no octave: check octaves separately (spectral centroid).
--per-note: instead of windows, each note's own span (middle 60%) gets a YIN pitch from the stem; a confident stem
pitch 1..--max-shift semitones away moves the note's pitch class (octave kept). Less noisy than windows on a
vibrato-heavy vocal; the histogram lists every note's offset (and 'unvoiced').
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


def yin(x, thr=0.15, fmin=80.0, fmax=1100.0, sr=48000):
    """f0 (Hz) of a voiced segment by YIN's cumulative-mean-normalised difference, or None if aperiodic."""
    if len(x) > 9600:
        c = len(x) // 2; x = x[c - 4800:c + 4800]
    x = x - x.mean(); n = len(x); lo, hi = int(sr / fmax), min(int(sr / fmin), n // 2)
    if hi <= lo + 2 or np.sqrt(np.mean(x ** 2)) < 1e-4:
        return None
    d = np.array([np.sum((x[:n - t] - x[t:]) ** 2) for t in range(hi)])
    cm = d[1:] * np.arange(1, hi) / (np.cumsum(d[1:]) + 1e-12); cm = np.concatenate([[1.0], cm])
    below = np.where(cm[lo:hi] < thr)[0]
    if not len(below):
        return None
    t = lo + below[0]
    while t + 1 < hi and cm[t + 1] < cm[t]:
        t += 1
    if 0 < t < hi - 1:   # parabolic refinement
        a_, b_, c_ = cm[t - 1], cm[t], cm[t + 1]; t = t + 0.5 * (a_ - c_) / (a_ - 2 * b_ + c_ + 1e-12)
    return sr / t


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
            notes.append((i, beat_to_s(tm, pos), beat_to_s(tm, pos + d)))
        pos += d
    S = L.load(stem).mean(1); O = L.load(ours).mean(1)
    hist = {}; moved = 0
    if notes and "--per-note" not in a:
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
                for i, ts, _ in notes:
                    if a0 <= ts < a0 + win:
                        toks[i] = shift_note(toks[i], k); moved += 1
    if "--per-note" in a:
        # each note's own span: YIN f0 of the stem over its middle 60%; move the note's pitch class to the stem's
        # nearest semitone when the stem is confident and 1-2 semitones away (octave kept: YIN's octave is unreliable)
        lim = opt("--max-shift", 2); thr = opt("--yin", 0.15)
        for i, ts, te in notes:
            a0, a1 = ts + 0.2 * (te - ts), te - 0.2 * (te - ts)
            if a1 - a0 < 0.06:
                continue
            f0 = yin(S[int(a0 * 48000):int(a1 * 48000)], thr)
            if not f0:
                hist["unvoiced"] = hist.get("unvoiced", 0) + 1; continue
            mn = NOTE.match(toks[i]); midi = 12 * (int(mn.group(3)) + 1) + NAMES[mn.group(1)] + {"#": 1, "b": -1, None: 0}[mn.group(2)]
            d = (round(69 + 12 * np.log2(f0 / 440)) - midi) % 12
            d = d - 12 if d > 6 else d
            hist[d] = hist.get(d, 0) + 1
            if 0 < abs(d) <= lim:
                toks[i] = shift_note(toks[i], d); moved += 1
    data[key]["score"] = " ".join(toks)
    json.dump(data, open(out, "w"), ensure_ascii=False)
    print(f"{len(notes)} notes; shifts {dict(sorted(hist.items(), key=lambda kv: (isinstance(kv[0], str), kv[0] if not isinstance(kv[0], str) else 0)))}; {moved} notes moved → {out}")


if __name__ == "__main__":
    main(sys.argv[1:])
