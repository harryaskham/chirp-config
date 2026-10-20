#!/usr/bin/env python3
"""Per-part chroma lag scan: is a harmonic part early or late against the record, section by section?

  chromalag.py SONG.yaml REF.wav SECTIONS.txt --parts a,b,c [--bpm N] [--range 1.0] [--chirp BIN] [--work DIR]

likeness scores chroma per short window (~0.5 s), so a part that plays the right notes half a beat off loses chroma
as surely as wrong notes do (Harder, Better, Faster, Stronger: the robot vocal and the riff synth both sat half a
beat early; delaying the riff synth gave +0.23..+0.31 on every seed). Each listed part is rendered solo (the song's
own track names), its chroma (80 Hz-2 kHz, 1/16 s hops) correlated with the record MIX's at quarter-beat lags in
[-range, +range] beats per section; prints the best lag (+ = the record is LATER: delay our part by that much) where
it beats lag 0 by > 0.01, '-' where the part is silent. A lag of one SIGN across most of a part's sections is a fix
(flagged with the median lag): delay the track (prepend R/<lag>b) or start it earlier (trim its leading rest; map
parts: make it a raw part). Sporadic lags are noise or content. Archangel: the stemsong vocal was 0.5-0.75 beat late
in 7 of 8 sections; 0.5 beat earlier +0.14 held-out. Complements onsetlag.py --chroma (the MIX's lag per section).
A flag is a CANDIDATE: render and score it. Parts that repeat at the lag alias — Dreams' rhodes-r (off-beat
stabs over a two-chord vamp) leaned -1 beat and advancing it lost on every seed (chirper-zero). Self-similarity at
the lag does not separate the cases (that rhodes 0.72 vs HBFS's true riff-synth 0.77), so no automatic veto.
"""
import os
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import chirpbin  # noqa: E402  (the adopted groove pin when CHIRP is unset)
import re
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import likeness as L  # noqa: E402

SR = 48000
HOP = 0.0625


def frames(x):
    win, hop = 4096, int(HOP * SR)
    f = np.fft.rfftfreq(win, 1 / SR)
    sel = (f > 80) & (f < 2000)
    pc = np.round(69 + 12 * np.log2(f[sel] / 440)).astype(int) % 12
    out = []
    for i in range(0, len(x) - win, hop):
        X = np.abs(np.fft.rfft(x[i:i + win] * np.hanning(win))) ** 2
        c = np.bincount(pc, weights=X[sel], minlength=12)
        out.append(c / (np.linalg.norm(c) + 1e-12))
    return np.array(out)


def main(a):
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    song, ref, secf = a[0], a[1], a[2]
    parts = opt("--parts", "").split(",")
    chirp = opt("--chirp", chirpbin.resolve("chirp"))
    work = opt("--work", "/tmp/lt/chromalag")
    os.makedirs(work, exist_ok=True)
    bpm = opt("--bpm", 0.0)
    if not bpm:
        m = re.search(r"^tempo:\s*\[?\s*\{?[^0-9]*?([0-9.]+)", open(song).read(), re.M)
        m2 = re.search(r'"bpm":\s*([0-9.]+)', open(song).read())
        bpm = float(m.group(1)) if m and not open(song).read().split("tempo:", 1)[1].lstrip().startswith("[") else float(m2.group(1))
    beat = 60.0 / bpm
    rng = opt("--range", 1.0)
    steps = list(range(-int(round(rng * 4)), int(round(rng * 4)) + 1))
    lags = [int(round(k * beat / 4 / HOP)) for k in steps]
    secs = [float(v) for v in open(secf).read().replace("\n", ",").split(",") if v.strip()]
    R = frames(L.load(ref).mean(1))
    print(f"tempo {bpm:.2f} bpm (beat {beat * 1000:.0f} ms); lag in beats, + = the record later (delay ours)")
    for p in parts:
        w = os.path.join(work, f"{p}.wav")
        subprocess.run(["nice", "-n", "15", chirp, "render", "-f", song, "--solo", p, "-o", w],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if not os.path.exists(w):
            print(f"{p:14s} render failed")
            continue
        P = frames(L.load(w).mean(1))
        os.remove(w)
        row, hits = [], {}
        for s0, s1 in zip(secs, secs[1:]):
            i0, i1 = int(s0 / HOP) + 16, int(s1 / HOP) - 16
            if i1 - i0 < 32 or np.mean(np.linalg.norm(P[i0:min(i1, len(P))], axis=1) if i0 < len(P) else [0]) < 0.5:
                row.append("   -  ")
                continue
            sc = []
            for lg in lags:
                pa, ra = P[i0:i1], R[max(0, i0 + lg):i1 + lg]
                n = min(len(pa), len(ra))
                sc.append(float(np.mean(np.sum(pa[:n] * ra[:n], axis=1))) if n else 0.0)
            k = int(np.argmax(sc))
            z = steps.index(0)
            if sc[k] - sc[z] > 0.01:
                lag = steps[k] / 4
                row.append(f"{lag:+.2f}b")
                hits[lag] = hits.get(lag, 0) + 1
            else:
                row.append("  0   ")
        active = sum(1 for r in row if r.strip() != "-")
        flag = ""
        if hits and active:
            # a consistent DIRECTION counts, not one exact value (Archangel's vocal: -0.75 in 4 sections, -0.5 in 3)
            for sign in (1, -1):
                same = [(lag, n) for lag, n in hits.items() if lag * sign > 0]
                n = sum(c for _, c in same)
                if n / active >= 0.6:
                    med = sorted(lag for lag, c in same for _ in range(c))[n // 2]
                    act = f"prepend R/{med}b" if med > 0 else f"start {-med}b earlier (trim the leading rest)"
                    flag = f"  <- {'late' if med < 0 else 'early'} in {n}/{active} sections (median {med:+.2f} beat): {act}"
        print(f"{p:14s} " + " ".join(row) + flag)


if __name__ == "__main__":
    main(sys.argv[1:])
