#!/usr/bin/env python3
"""hocket: do two hard-panned parts take turns? (chirper-zero, Odd Sympathy v3: two guitars half a bar apart, written
so that only one plays at a time; a rig that rings through its rests fills the holes. A module by chirp-eco.)

  hocket.py NAME=FILE[:START:DUR] ... [--floor 20]

Each FILE is a render of the two parts ALONE, one hard left and one hard right (`chirp render --solo L --solo R`);
START and DUR in seconds cut a passage. In 5 ms frames each channel's level is read against its own 95th percentile,
and a side is SOUNDING when it is within --floor dB of that (default 20). Prints the share of the time with ONE side
sounding, BOTH, or NEITHER. Two parts that take turns read mostly "one side"; a rig that holds through its rests
reads "both" (Odd Sympathy's guitars against each other: one side 18% on the first rig, 43% on a dry one); the same
riff in step reads "both" and "neither" (its rests). Compare two rigs over the same notes by giving both renders.
tools/lagchk.py says how far apart the two parts are; this says whether there is air between them.
Read-only. Tests: tools/tests/test_hocket.py.
"""
import sys
import wave

import numpy as np


def load(spec):
    """(samples as frames x channels, rate) of FILE[:START:DUR]."""
    p = spec.split(":")
    with wave.open(p[0]) as w:
        sr, ch, sw = w.getframerate(), w.getnchannels(), w.getsampwidth()
        if len(p) > 1:
            w.setpos(int(float(p[1]) * sr))
        n = int(float(p[2]) * sr) if len(p) > 2 else w.getnframes() - w.tell()
        x = np.frombuffer(w.readframes(n), dtype={2: np.int16, 4: np.int32}[sw]).reshape(-1, ch).astype(float)
    return x, sr


def shares(x, sr, floor=20.0):
    """(one side, both, neither) as fractions of the time, from the first two channels."""
    h = int(0.005 * sr)
    m = len(x) // h * h
    e = np.sqrt((x[:m].reshape(-1, h, x.shape[1]) ** 2).mean(1)) + 1e-9
    on = 20 * np.log10(e / np.percentile(e, 95, axis=0)) > -floor
    lft, rgt = on[:, 0], on[:, 1]
    return float(np.mean(lft ^ rgt)), float(np.mean(lft & rgt)), float(np.mean(~lft & ~rgt))


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    if not a or "-h" in a or "--help" in a:
        print(__doc__)
        return 0 if a else 2
    floor = 20.0
    if "--floor" in a:
        i = a.index("--floor")
        floor = float(a[i + 1])
        del a[i:i + 2]
    for arg in a:
        if "=" not in arg:
            raise SystemExit(f"hocket: {arg!r} is not NAME=FILE[:START:DUR]")
        name, spec = arg.split("=", 1)
        x, sr = load(spec)
        if x.shape[1] < 2:
            raise SystemExit(f"hocket: {name} has one channel; it reads a part hard left against a part hard right")
        one, both, neither = shares(x, sr, floor)
        print(f"{name:10s} one side {100 * one:5.1f}%   both {100 * both:5.1f}%   neither {100 * neither:5.1f}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
