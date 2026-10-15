#!/usr/bin/env python3
"""Re-pitch a monophonic part from a stem: for every note of a song track (a tab's vocal line, a lead), estimate the
stem's pitch over the note's middle (YIN-style difference function on 40 ms frames, median of the confident
frames) and, where it clearly differs from the written note, replace the note's pitch — keeping its duration,
velocity and articulations (^vow, ^on/^off …). Tabs approximate sung lines; the stem knows what was sung.

  stempitch.py STEM.wav SONG.yaml TRACK OUT.json [--key vox] [--from S] [--to S] [--min-dur 0.15]
              [--lo 70] [--hi 700] [--conf 0.25] [--keep-octave]

A note changes only when ≥60% of its frames are confident (YIN dip < --conf) and the median differs by ≥1
semitone. --keep-octave moves the stem's pitch into the written note's octave when it lies within an octave
(pitch trackers flip octaves; the tab's register is usually right)."""
import json
import os
import re
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import likeness as L  # noqa: E402
import drumtrans as D  # noqa: E402
import stemvowels as V  # noqa: E402

SR = 48000
NAMES = "C C# D D# E F F# G G# A A# B".split()
PC = {n: i for i, n in enumerate(NAMES)}
PC.update({"Db": 1, "Eb": 3, "Gb": 6, "Ab": 8, "Bb": 10})


def midi_of(n):
    m = re.match(r"^([A-G](?:#|b)?)(-?\d+)$", n)
    return 12 * (int(m.group(2)) + 1) + PC[m.group(1)] if m else None


def name_of(mi):
    return f"{NAMES[mi % 12]}{mi // 12 - 1}"


def yin(frame, lo, hi, thr):
    n = len(frame); tmax = int(SR / lo); tmin = int(SR / hi)
    if n < 2 * tmax:
        return None
    x = frame - frame.mean()
    d = np.array([np.sum((x[:n - tmax] - x[t:n - tmax + t]) ** 2) for t in range(tmax + 1)])
    cm = d[1:] * np.arange(1, tmax + 1) / (np.cumsum(d[1:]) + 1e-12)
    cm = np.concatenate([[1.0], cm])
    for t in range(tmin, tmax):
        if cm[t] < thr and cm[t] <= cm[t + 1]:
            return SR / t
    return None


def main(a):
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    x = L.load(a[0]).mean(1)
    t0, t1, mind = opt("--from", 0.0), opt("--to", 1e9), opt("--min-dur", 0.15)
    lo, hi, thr = opt("--lo", 70.0), opt("--hi", 700.0), opt("--conf", 0.25)
    pts = D.tempo_points(a[1]); beats = np.array([b for b, _ in pts]); bpm = np.array([v for _, v in pts])
    secs = np.concatenate([[0.0], np.cumsum(np.diff(beats) * 60 / bpm[:-1])])

    def b2t(b):
        i = max(0, np.searchsorted(beats, b, side="right") - 1)
        return secs[i] + (b - beats[i]) * 60 / bpm[i]

    toks, out, pos, changed, seen = V.track_tokens(a[1], a[2]), [], 0.0, 0, 0
    for t in toks:
        m = re.match(r"^([^/]+)/([0-9.]+)b(.*)$", t)
        if not m:
            out.append(t); continue
        body, ln, rest = m.group(1), float(m.group(2)), m.group(3)
        if body in ("R", "r", "_") or "," in body:
            out.append(t); pos += ln; continue
        s, e = b2t(pos), b2t(pos + ln); pos += ln
        written = midi_of(body)
        if written is None or not (t0 <= s < t1) or e - s < mind:
            out.append(t); continue
        seen += 1
        seg = x[int((s + 0.2 * (e - s)) * SR):int((e - 0.2 * (e - s)) * SR)]
        fr = [seg[i:i + int(0.04 * SR)] for i in range(0, max(0, len(seg) - int(0.04 * SR)), int(0.02 * SR))]
        f0s = [f for f in (yin(f_, lo, hi, thr) for f_ in fr) if f]
        if len(fr) == 0 or len(f0s) < 0.6 * len(fr):
            out.append(t); continue
        sung = int(round(69 + 12 * np.log2(np.median(f0s) / 440)))
        if "--keep-octave" in a:
            while sung - written > 6: sung -= 12
            while written - sung > 6: sung += 12
        if abs(sung - written) >= 1:
            changed += 1
            out.append(f"{name_of(sung)}/{m.group(2)}b{rest}")
        else:
            out.append(t)
    json.dump({opt("--key", "vox"): {"score": " ".join(out)}}, open(a[3], "w"))
    print(f"{seen} notes checked in {t0:.0f}-{min(t1, pos):.0f}; {changed} re-pitched from the stem")


if __name__ == "__main__":
    main(sys.argv[1:])
