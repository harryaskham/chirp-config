#!/usr/bin/env python3
"""cymspec: a cymbal alone beside the top of eleven records' drum stems, in thirds of an octave from 1 kHz, as a
shape; and how fast its strokes fall. chirper-zero's bench of 19 Nov (So Far v14, the china), moved into tools/ at
his offer; the bass's twin is tools/bassspec.py.

  cymspec.py NAME=FILE[:FROM:TO] ...

FILE is a raw solo render of the cymbal, hat or metal track (`chirp render --solo TRACK --set loudness=null`), FROM
and TO in seconds. Rows: the records' median, their spread (half the distance between the 2nd and the 10th of the
eleven), then each NAME less the median, its mean distance over 2-16 kHz, and each stroke's FALL: the level 0.2 to
0.4 s after a stroke against its first 0.1 s, at 2-8 kHz and at 8-16 kHz (the strokes are found in the file).

Each spectrum is set level on its own mean, in dB, over 2-8 kHz: SHAPES, not levels.

WHAT THE RECORDS' ROW IS: the WHOLE separated drum stem (ref/stems/bs_roformer_sw/ID/drums.wav, 30-150 s): cymbals,
hats and the snare's wires together. It says where a record's metal has its energy, not what one cymbal sounds like.
HOW FAR TO TRUST IT (chirp-eco, 19 Nov, the eleven records read with no separator): the RECORD ITSELF carries 5.7 to
7.4 dB more at 4-8 kHz than at 8-16 kHz (median 6.1); its drum stem 3.6 to 5.9 (median 4.8). So the tilt is the
records', not the separator's, and the stem is about a dB brighter than the record. But the stems LOSE POWER at the
top: all of a record's stems together carry 60 to 81% of its 8-16 kHz and 44 to 60% of its 4-8 kHz. Trust the shape;
do not set a cymbal's LEVEL against a stem.

What it said on the day it was written: the records' metal has its weight at 4-6 kHz and is 9 dB down by 12.5 kHz;
the kit's china (`modal-china`, bright 1, tilt 3, +3 dB at 8 kHz) read +4.1, +4.9, +8.2 at 10, 12.5 and 16 kHz; the
library's closed hat (`haake-hat`) is noise through an 8 kHz high-pass with nothing under it. On the modal plate
BRIGHT fills the top octave, not TILT; and the kit's DRIVE on the china is its ring (drive 0 leaves a stroke 21 dB
down in a quarter of a second: a splash). The cache is ref/cymspec/records-drums-top.json (local). A read, not a score.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bassspec as B  # noqa: E402

REFS = B.REFS
C = [1000 * 2 ** (i / 3) for i in range(13)]                   # 1 kHz ... 16 kHz
LAB = "1k 1.25k 1.6k 2k 2.5k 3.15k 4k 5k 6.3k 8k 10k 12.5k 16k".split()
NORM = [i for i, c in enumerate(C) if 1990 <= c <= 8100]
RNG = [i for i, c in enumerate(C) if c >= 1990]
RECORD_TILT = (5.7, 6.1, 7.4)       # the records themselves, 4-8 kHz less 8-16 kHz: lowest, median, highest (no separator)


def shape(m, sr):
    """The third-octave spectrum (dB) from 1 kHz of every frame, level on its mean over 2-8 kHz."""
    n = 1 << 13
    acc = np.zeros(n // 2 + 1)
    h = np.hanning(n)
    for i in range(0, len(m) - n, n // 2):
        acc += np.abs(np.fft.rfft(m[i:i + n] * h)) ** 2
    if not acc.any():
        raise SystemExit("cymspec: under a fifth of a second of audio, or silence")
    f = np.fft.rfftfreq(n, 1 / sr)
    e = np.array([10 * np.log10(acc[(f >= c / 2 ** (1 / 6)) & (f < c * 2 ** (1 / 6))].sum() + 1e-20) for c in C])
    return e - e[NORM].mean()


def fall(m, sr, lo, hi):
    """(the median fall in dB from a stroke's first 0.1 s to 0.2-0.4 s after it, how many strokes) in the band lo-hi.
    A stroke is a 10 ms step where the band's level rises 8 dB, the largest rise near it, whose loudest 10 ms (within
    30 ms of the rise) is within 20 dB of the file's loudest; the fall is measured from that loudest 10 ms."""
    n, hop = 512, max(1, int(0.01 * sr))
    f = np.fft.rfftfreq(n, 1 / sr)
    sel = (f >= lo) & (f < min(hi, sr / 2 - 200))
    h = np.hanning(n)
    lv = 10 * np.log10(np.array([(np.abs(np.fft.rfft(m[i:i + n] * h)) ** 2)[sel].sum() for i in range(0, len(m) - n, hop)]) + 1e-20)
    if len(lv) < 50:
        return float("nan"), 0
    d = np.diff(lv, prepend=lv[0])
    v = []
    for i in range(2, len(lv) - 48):
        if d[i] > 8 and d[i] == d[max(0, i - 8):i + 8].max():
            p = i + int(np.argmax(lv[i:i + 4]))                    # the stroke's loudest 10 ms, within 30 ms of the rise
            if lv[p] > lv.max() - 20:
                v.append(lv[p + 20:p + 40].mean() - lv[p:p + 10].mean())
    return (float(np.median(v)), len(v)) if v else (float("nan"), 0)


def records(root=None):
    """{record id: the shape of the top of its drum stem}, cached in ref/cymspec/records-drums-top.json."""
    root = root or B.ROOT
    cache = os.path.join(root, "ref", "cymspec", "records-drums-top.json")
    if os.path.exists(cache):
        with open(cache) as f:
            return json.load(f)
    d = {}
    for r in REFS:
        p = os.path.join(root, "ref", "stems", "bs_roformer_sw", r, "drums.wav")
        if os.path.exists(p):
            sr, m = B.load(p, 30, 150)
            d[r] = [float(x) for x in shape(m, sr)]
    if not d:
        raise SystemExit("cymspec: no drum stems under ref/stems/bs_roformer_sw/")
    os.makedirs(os.path.dirname(cache), exist_ok=True)
    with open(cache + ".new", "w") as f:
        json.dump(d, f)
    os.replace(cache + ".new", cache)
    return d


def row(name, m, sr, med):
    d = shape(m, sr) - med
    f1, n1 = fall(m, sr, 2000, 8000)
    f2, _ = fall(m, sr, 8000, 16000)
    return f"{name[:17]:18s}" + "".join(f"{v:+6.1f}" for v in d) + f"   {np.abs(d[RNG]).mean():.2f}          | {f1:+6.1f} {f2:+6.1f} ({n1})"


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if not argv or "-h" in argv or "--help" in argv:
        print(__doc__)
        return
    R = records()
    med, spread = B.stats(R)
    print(f"{'Hz':18s}" + "".join(f"{x:>6s}" for x in LAB)
          + "   mean|d| 2-16k | fall 0.2-0.4 s after the stroke: 2-8 kHz, 8-16 kHz (strokes)")
    print(f"{'RECORDS (median)':18s}" + "".join(f"{v:6.1f}" for v in med) + f"   ({len(R)} records' drum stems, whole)")
    print(f"{'their spread':18s}" + "".join(f"{v:6.1f}" for v in spread))
    for a in argv:
        if a.startswith("--"):
            continue
        if "=" not in a:
            raise SystemExit("cymspec: NAME=FILE[:FROM:TO]")
        name, rest = a.split("=", 1)
        parts = rest.split(":")
        sr, m = B.load(parts[0], *(float(x) for x in parts[1:3])) if len(parts) == 3 else B.load(parts[0])
        print(row(name, m, sr, med))
    print(f"(shapes, level on 2-8 kHz. The records' row is the whole separated drum stem. With no separator the records "
          f"themselves carry {RECORD_TILT[0]} to {RECORD_TILT[2]} dB more at 4-8 kHz than at 8-16 kHz (median {RECORD_TILT[1]}); "
          "their stems lose a third of the top's POWER: trust the shape, not a level against a stem.)")


if __name__ == "__main__":
    main()
