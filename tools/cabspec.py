#!/usr/bin/env python3
"""cabspec: a guitar rig alone against the RECORD's guitar alone, third-octave by third-octave: the yardstick for a
cabinet (bd-af781d). (chirper-zero, Common Time v33; a module with --recs, by chirp-eco.)

  cabspec.py [--abs] [--recs ID:START:DUR,...] NAME=FILE[:START:DUR] ...

The RECORD is the mean of guitar-alone passages read from the records themselves (ref/ID.wav; find such passages
with galone.py). Default: obZen 183.5+8 s, Combustion 44.6+2.5 s, Bleed 386.9+1.5 s. Each spectrum is in
third-octaves from 63 Hz to 12.5 kHz against its own 71 Hz-8.9 kHz total (both channels' power summed).
Prints the RECORD, the records' spread (largest minus smallest, a band), then each file as its difference from the
RECORD (--abs: the spectra themselves), and two readings of how far it is:
  worst, mean|d|     over the third-octaves from 100 Hz to 10 kHz
  after the bar      the two wide bands 71-141 and 141-282 Hz, then worst and mean|d| with those two standing in for
                     the third-octaves under 315 Hz. This is the reading to use: under 315 Hz the records differ
                     from each other by up to 11 dB a third-octave, by the notes being played.
A rig fitted to this alone can be wrong in the record's MIX (v33): check stembal --voice and lowwide.py too.
Also importable: spec(), bands(), record(). Read-only. Tests: tools/tests/test_cabspec.py.
"""
import os
import sys
import wave

import numpy as np

CS = np.array([63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000,
               10000, 12500])
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
while not os.path.isdir(os.path.join(ROOT, "ref")) and ROOT != "/":
    ROOT = os.path.dirname(ROOT)
REF = os.path.join(ROOT, "ref", "")
RECS = (("obzen", 183.5, 8), ("combustion", 44.6, 2.5), ("bleed", 386.9, 1.5))


def spec(p, t0=None, dur=None):
    with wave.open(p) as w:
        sr = w.getframerate()
        sw = w.getsampwidth()
        if t0 is not None:
            w.setpos(int(t0 * sr))
        n = int(dur * sr) if dur else w.getnframes() - (int(t0 * sr) if t0 else 0)
        x = np.frombuffer(w.readframes(n), "<i%d" % sw).astype(float).reshape(-1, w.getnchannels()) / 2 ** (8 * sw - 1)
    P = 0
    for ch in range(x.shape[1]):
        P = P + np.abs(np.fft.rfft(x[:, ch])) ** 2
    return P, np.fft.rfftfreq(len(x), 1 / sr)


def bands(P, f, norm=True):
    b = np.array([10 * np.log10(P[(f >= c / 2 ** (1 / 6)) & (f < c * 2 ** (1 / 6))].sum() + 1e-20) for c in CS])
    return b - 10 * np.log10(P[(f >= 71) & (f < 8900)].sum() + 1e-20) if norm else b


def wide(P, f):
    """The two wide bands under 315 Hz (71-141, 141-282 Hz) against the 71 Hz-8.9 kHz total."""
    return np.array([10 * np.log10(P[(f >= lo) & (f < hi)].sum() + 1e-20) for lo, hi in ((71, 141), (141, 282))]) \
        - 10 * np.log10(P[(f >= 71) & (f < 8900)].sum() + 1e-20)


def record(recs=None):
    """(the mean of the records' guitar-alone passages in third-octaves, each record's row)."""
    R = np.array([bands(*spec(REF + n + ".wav", t0, d)) for n, t0, d in (recs or RECS)])
    return R.mean(0), R


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    if not a or "-h" in a or "--help" in a:
        print(__doc__)
        return 0 if a else 2
    ab = "--abs" in a
    a = [x for x in a if x != "--abs"]
    recs = RECS
    if "--recs" in a:
        i = a.index("--recs")
        try:
            recs = tuple((n, float(t0), float(d)) for n, t0, d in (r.split(":") for r in a[i + 1].split(",")))
        except (IndexError, ValueError):
            raise SystemExit("cabspec: --recs ID:START:DUR,ID:START:DUR,... (seconds), as in --recs obzen:183.5:8") from None
        del a[i:i + 2]
    tgt, R = record(recs)
    i0, i1 = list(CS).index(100), list(CS).index(10000) + 1
    WT = np.mean([wide(*spec(REF + n + ".wav", t0, d)) for n, t0, d in recs], 0)
    j0 = list(CS).index(315)
    print("%-14s" % "Hz" + " ".join("%5s" % (c if c < 1000 else "%gk" % (c / 1000)) for c in CS)
          + "   worst  mean|d| (100 Hz-10 kHz) | 71-141 141-282 Hz, and worst, mean|d| with those two for the bands under 315 Hz")
    print("%-14s" % "RECORD" + " ".join("%5.1f" % v for v in tgt))
    print("%-14s" % "its spread" + " ".join("%5.1f" % v for v in np.ptp(R, 0)))
    for x in a:
        name, rest = x.split("=", 1)
        p = rest.split(":")
        Pf = spec(p[0], float(p[1]) if len(p) > 1 else None, float(p[2]) if len(p) > 2 else None)
        b = bands(*Pf)
        d = b - tgt
        k = np.argmax(np.abs(d[i0:i1])) + i0
        w = wide(*Pf) - WT
        dd = np.concatenate([w, d[j0:i1]])
        print("%-14s" % name[:14] + " ".join("%+5.1f" % v for v in (b if ab else d))
              + "   %+5.1f @%s  %.2f" % (d[k], CS[k], np.mean(np.abs(d[i0:i1])))
              + "  | %+5.1f %+5.1f   %+5.1f  %.2f" % (w[0], w[1], dd[np.argmax(np.abs(dd))], np.mean(np.abs(dd))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
