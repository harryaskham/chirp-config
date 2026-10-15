#!/usr/bin/env python3
"""Pad part transcribed from a stem, bar by bar: for an instrument the tab does not have (atmospheres, drones,
effects guitars, pads living in Demucs' "other"), write a sustained part that follows the stem — each bar's
dominant pitch class (chroma, 30 Hz-2 kHz) in the octave of its strongest spectral peak, plus the second pitch
class when it is strong, velocity from the bar's level, rests where the stem is quiet or unpitched (noisy), and
repeated bars merged into held notes. Output is a raw part for tab2song (`"raw": "FILE.json#KEY"`).

  stempad.py MAP.json STEM.wav OUT.json [--key pad] [--bars 37-228,285-400] [--floor -55] [--min-share 0.3]
            [--lo 36] [--hi 84] [--second 0.5]

No audio is copied: only pitch, level and timing are measured."""
import json
import os
import sys
import importlib.util

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import likeness as L  # noqa: E402

spec = importlib.util.spec_from_file_location("bc", os.path.join(HERE, "barchroma.py"))
B = importlib.util.module_from_spec(spec); spec.loader.exec_module(B)
NAMES = B.NAMES


def fmt(x):
    return f"{round(x, 4):.4f}".rstrip("0").rstrip(".")


def ranges(spec_):
    out = []
    for r in spec_.split(","):
        a, _, b = r.partition("-")
        out.append((int(a), int(b or a)))
    return out


def main(a):
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    mp = json.load(open(a[0])); x = L.load(a[1]).mean(1)
    root = os.path.dirname(HERE)
    cache = mp["cache"] if os.path.isabs(mp["cache"]) else os.path.join(root, mp["cache"])
    tl = [m for m in B.T.corrected_timeline(cache, mp) if not m["skip"]]
    want = ranges(opt("--bars", "1-100000"))
    on = lambda m: any(lo <= m <= hi for lo, hi in want)
    floor, share_min, second = opt("--floor", -55.0), opt("--min-share", 0.3), opt("--second", 0.5)
    lo_m, hi_m = opt("--lo", 36), opt("--hi", 84)
    t = mp.get("offset", 0.0)
    bars = []
    for m in tl:
        dur = m["beats"] * 60 / m["bpm"]
        seg = x[int(t * 48000):int((t + dur) * 48000)]
        notes, lvl = None, -120.0
        if on(m["m"]) and len(seg) > 8192:
            lvl = 10 * np.log10(np.mean(seg ** 2) + 1e-12)
            if lvl > floor:
                c = B.chroma(seg); order = np.argsort(c)[::-1]
                if c[order[0]] >= share_min:
                    sp = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))); f = np.fft.rfftfreq(len(seg), 1 / 48000)
                    def place(pc):
                        # the strongest spectral peak of this pitch class inside the allowed range
                        best, bm = -1.0, None
                        for mi in range(lo_m, hi_m + 1):
                            if mi % 12 != pc:
                                continue
                            fr = 440 * 2 ** ((mi - 69) / 12); sel = (f > fr * 0.985) & (f < fr * 1.015)
                            v = sp[sel].max() if sel.any() else 0.0
                            if v > best:
                                best, bm = v, mi
                        return bm
                    notes = [place(order[0])]
                    if c[order[1]] >= second * c[order[0]]:
                        n2 = place(order[1])
                        if n2 is not None and n2 != notes[0]:
                            notes.append(n2)
                    notes = sorted(n for n in notes if n is not None)
        bars.append((m["beats"], notes, lvl))
        t += dur
    loud = [l for _, n, l in bars if n]
    ref = np.percentile(loud, 90) if loud else 0.0
    vel = lambda l: int(np.clip(110 + 2.3 * (l - ref), 30, 120))
    name = lambda mi: f"{NAMES[mi % 12]}{mi // 12 - 1}"
    off_beats = mp.get("offset", 0.0) * tl[0]["bpm"] / 60
    toks, rest, cur = [], off_beats, None          # cur = [notes, beats, vel]
    def flush():
        nonlocal cur, rest
        if cur:
            toks.append(f"{','.join(name(n) for n in cur[0])}/{fmt(cur[1])}b@{cur[2]}")
            cur = None
    for beats, notes, lvl in bars:
        if not notes:
            flush(); rest += beats; continue
        if rest > 1e-9:
            toks.append(f"R/{fmt(rest)}b"); rest = 0.0
        if cur and cur[0] == notes:
            cur[1] += beats
        else:
            flush(); cur = [notes, beats, vel(lvl)]
    flush()
    key = opt("--key", "pad")
    json.dump({key: {"score": " ".join(toks)}}, open(a[2], "w"))
    held = sum(1 for _, n, _ in bars if n)
    print(f"{held} of {len(bars)} bars pitched; {len([t_ for t_ in toks if not t_.startswith('R/')])} notes")


if __name__ == "__main__":
    main(sys.argv[1:])
