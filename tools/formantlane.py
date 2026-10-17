#!/usr/bin/env python3
"""A talk-box vowel lane: per-note vowels read from a vocal stem drive the `formant` fx (vowel 0..4 = a e i o u).

  formantlane.py STEM.wav SONG.yaml TRACK OUT.json [--min 0.12] [--gate 1e-3] [--lead 0.005] [--default 2]

For every note of TRACK (SUB/TRACK allowed) at least --min s long, the stem's middle 60% is LPC-analysed (order 12 at
16 kHz); F1/F2 come from the LPC envelope's peaks (no polynomial roots: numpy's eigen-solver is broken in some envs)
and the nearest of a/e/i/o/u (log-distance to textbook F1/F2) becomes a lane step --lead s before the note. Writes
{"points": [[time, vowel], …]} — put it on the track as `auto: {vw: <points>}` with fx `formant vowel=auto.vw q=4`
(map parts: extra.fx / extra.auto). Harder, Better, Faster, Stronger: a static vowel=2 q=8 → this lane at q=4,
+1.05 on all three seeds (chroma 35 → 38.8); q=8 only +0.27. A stand-in until a keyed vocoder exists (bd-b0410a).
"""
import json
import re
import sys
import importlib.util

import numpy as np
from scipy.signal import resample_poly

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import likeness as L          # noqa: E402
import stemvowels as V        # noqa: E402

_spec = importlib.util.spec_from_file_location("st", __file__.rsplit("/", 1)[0] + "/stemtranspose.py")
ST = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ST)

SR = 16000
VOWELS = {0: (750, 1250), 1: (500, 1900), 2: (300, 2300), 3: (500, 900), 4: (330, 800)}   # a e i o u (F1, F2)
F = np.arange(150, 3500, 10.0)
Z = np.exp(-1j * 2 * np.pi * np.outer(F, np.arange(13)) / SR)


def formants(seg, p=12):
    s = np.append(seg[0], seg[1:] - 0.97 * seg[:-1]) * np.hamming(len(seg))
    r = np.array([np.dot(s[:len(s) - k], s[k:]) for k in range(p + 1)])
    if r[0] <= 0:
        return []
    a = np.zeros(p + 1)
    a[0], e = 1.0, r[0]
    for i in range(1, p + 1):
        k = -(r[i] + np.dot(a[1:i], r[i - 1:0:-1])) / e
        prev = a.copy()
        a[1:i] = prev[1:i] + k * prev[i - 1:0:-1]
        a[i] = k
        e *= 1 - k * k
        if e <= 0:
            return []
    env = -20 * np.log10(np.abs(Z @ a) + 1e-12)
    return [F[i] for i in range(1, len(env) - 1) if env[i] > env[i - 1] and env[i] >= env[i + 1]]


def vowel(seg):
    fr = formants(seg)
    f1 = next((f for f in fr if 200 < f < 1000), None)
    f2 = next((f for f in fr if f1 and f1 + 250 < f < 3000), None)
    if not (f1 and f2):
        return None
    return min(VOWELS, key=lambda k: np.log(f1 / VOWELS[k][0]) ** 2 + np.log(f2 / VOWELS[k][1]) ** 2)


def main(a):
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    stem, song, track, out = a[:4]
    x = resample_poly(L.load(stem).mean(1).astype(np.float64), 1, 3)
    tm = ST.tempo_map(open(song).read())
    pos, pts, hist = V.track_offset(song, track), [["0s", float(opt("--default", 2))]], [0] * 5
    for t in V.track_tokens(song, track):
        m = re.match(r"^([^/]+)/([0-9.]+)b", t)
        if not m:
            continue
        ln = float(m.group(2))
        if m.group(1) not in ("R", "r", "_"):
            t0, t1 = ST.beat_to_s(tm, pos), ST.beat_to_s(tm, pos + ln)
            if t1 - t0 >= opt("--min", 0.12):
                seg = x[int((t0 + 0.2 * (t1 - t0)) * SR):int((t1 - 0.2 * (t1 - t0)) * SR)]
                if len(seg) > 512 and np.sqrt(np.mean(seg ** 2)) > opt("--gate", 1e-3):
                    v = vowel(seg)
                    if v is not None:
                        pts.append([f"{max(0.0, t0 - opt('--lead', 0.005)):.3f}s", float(v)])
                        hist[v] += 1
        pos += ln
    json.dump({"points": pts}, open(out, "w"))
    print(f"{sum(hist)} notes with a vowel — a/e/i/o/u {hist} → {out}")


if __name__ == "__main__":
    main(sys.argv[1:])
