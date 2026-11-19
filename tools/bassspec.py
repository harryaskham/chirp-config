#!/usr/bin/env python3
"""bassspec: a bass alone beside eleven records' bass stems, in thirds of an octave, as shapes (like cabspec for a
guitar). chirper-zero's bench of 19 Nov (In the Time Of v24), moved into tools/ at his offer.

  bassspec.py NAME=FILE[:FROM:TO] ... [--each]

FILE is a raw solo render of the bass (`chirp render --solo TRACK --set loudness=null`), FROM and TO in seconds.
Rows: the records' median, their spread (half the distance between the 2nd and the 10th of the eleven), then each
NAME less the median, its worst band, its mean distance over 40 Hz-5 kHz, and the same counting only each band's
excess over the records' own spread. --each also prints every record less the median.

Each spectrum is set level on its own mean, in dB, over 50 Hz-2.5 kHz, so the rows are SHAPES, not levels. Only the
frames within 15 dB of the loudest are read (a bass that rests is not averaged with its silence).

The records' basses are SEPARATED STEMS (ref/stems/bs_roformer_sw/ID/bass.wav, 30-150 s of each): trust the low
bands; above 1 kHz the separator may have given the bass's grind to the guitars or the guitars' to the bass (on a
lone guitar it takes up to 5 dB of the top: tools/riffpunch.py). Their shapes are cached in
ref/bassspec/records-bass.json (local; delete it to read the stems again).

What it said of the album's bass (`ct-bass`) on the day it was written: the records have their weight at the OCTAVE
(the 80 Hz band 26 dB over 40 Hz and 30 over 400-630 Hz, a grind peak at 1.25 kHz 9 under); ours was a sub and a box
(+17.9 dB at 40 Hz, -7.6 and -9.8 at 80 and 100, +5.6 to +11.3 at 400-800 Hz). And: the SUB BELONGS TO THE KICK on the
records (their basses sit 16 dB under their drums below 60 Hz; ours were level), and `ct-bass`'s sine sub drives the
bass's two compressors. A read, not a score.
"""
import json
import os
import sys
import wave

import numpy as np

ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFS = ("bleed combustion dancers-to-a-discordant-system electric-red lethargica obzen pineal-gland-optics pravus "
        "the-abysmal-eye the-faultless this-spiteful-snake").split()
C = [31.5 * 2 ** (i / 3) for i in range(25)]                   # 31.5 Hz ... 8 kHz
LAB = "31 40 50 63 80 100 125 160 200 250 315 400 500 630 800 1k 1.25k 1.6k 2k 2.5k 3.15k 4k 5k 6.3k 8k".split()
NORM = [i for i, c in enumerate(C) if 49 <= c <= 2600]
RNG = [i for i, c in enumerate(C) if 39 <= c <= 5100]


def load(f, a=None, b=None):
    """(rate, the mono sum) of a 16-bit WAV, from second a to second b."""
    with wave.open(f) as w:
        sr = w.getframerate()
        if a is not None:
            w.setpos(int(a * sr))
        n = w.getnframes() - w.tell() if b is None else int((b - (a or 0)) * sr)
        x = np.frombuffer(w.readframes(n), dtype="<i2").reshape(-1, w.getnchannels()).astype(np.float64).mean(1) / 32768
    return sr, x


def shape(m, sr, gate=15):
    """The third-octave spectrum (dB) of the frames within `gate` dB of the loudest, level on its mean over 50 Hz-2.5 kHz."""
    n = 1 << 14
    h = np.hanning(n)
    fr = [np.abs(np.fft.rfft(m[i:i + n] * h)) ** 2 for i in range(0, len(m) - n, n // 2)]
    if not fr:
        raise SystemExit("bassspec: under half a second of audio")
    p = np.array([f.sum() for f in fr])
    acc = np.sum([f for f, k in zip(fr, p > p.max() * 10 ** (-gate / 10)) if k], axis=0)
    f = np.fft.rfftfreq(n, 1 / sr)
    e = np.array([10 * np.log10(acc[(f >= c / 2 ** (1 / 6)) & (f < c * 2 ** (1 / 6))].sum() + 1e-20) for c in C])
    return e - e[NORM].mean()


def records(root=None):
    """{record id: its bass stem's shape}, cached in ref/bassspec/records-bass.json."""
    root = root or ROOT
    cache = os.path.join(root, "ref", "bassspec", "records-bass.json")
    if os.path.exists(cache):
        with open(cache) as f:
            return json.load(f)
    d = {}
    for r in REFS:
        p = os.path.join(root, "ref", "stems", "bs_roformer_sw", r, "bass.wav")
        if os.path.exists(p):
            sr, m = load(p, 30, 150)
            d[r] = [float(x) for x in shape(m, sr)]
    if not d:
        raise SystemExit("bassspec: no bass stems under ref/stems/bs_roformer_sw/")
    os.makedirs(os.path.dirname(cache), exist_ok=True)
    with open(cache + ".new", "w") as f:
        json.dump(d, f)
    os.replace(cache + ".new", cache)
    return d


def stats(R):
    """(median, spread) of the records' shapes: the spread is half the distance between the 2nd lowest and 2nd highest."""
    M = np.array(list(R.values()))
    s = np.sort(M, 0)
    return np.median(M, 0), ((s[-2] - s[1]) / 2 if len(M) >= 4 else (s[-1] - s[0]) / 2)


def row(name, e, med, spread):
    """One NAME's line: its shape less the median, the worst band, the mean distance, and the excess over the spread."""
    d = e - med
    w = int(np.argmax(np.abs(d[RNG]))) + RNG[0]
    ex = np.maximum(np.abs(d) - spread, 0)
    return (f"{name[:15]:16s}" + "".join(f"{v:+6.1f}" for v in d)
            + f"   {d[w]:+5.1f} @{LAB[w]:5s}  {np.abs(d[RNG]).mean():.2f}                 {ex[RNG].mean():.2f}")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if not argv or "-h" in argv or "--help" in argv:
        print(__doc__)
        return
    R = records()
    med, spread = stats(R)
    print(f"{'Hz':16s}" + "".join(f"{x:>6s}" for x in LAB)
          + "   worst      mean|d| 40 Hz-5 kHz   and with each band's excess over the records' spread only")
    print(f"{'RECORDS (median)':16s}" + "".join(f"{v:6.1f}" for v in med) + f"   ({len(R)} records' bass stems)")
    print(f"{'their spread':16s}" + "".join(f"{v:6.1f}" for v in spread))
    if "--each" in argv:
        for r, e in R.items():
            print(f"{r[:15]:16s}" + "".join(f"{v:+6.1f}" for v in np.array(e) - med))
    for a in argv:
        if a.startswith("--"):
            continue
        if "=" not in a:
            raise SystemExit("bassspec: NAME=FILE[:FROM:TO]")
        name, rest = a.split("=", 1)
        parts = rest.split(":")
        sr, m = load(parts[0], *(float(x) for x in parts[1:3])) if len(parts) == 3 else load(parts[0])
        print(row(name, shape(m, sr), med, spread))
    print("(shapes, not levels: each row is level on its own mean over 50 Hz-2.5 kHz. The records are separated stems: "
          "trust the low bands; above 1 kHz the grind may be partly the guitars'.)")


if __name__ == "__main__":
    main()
