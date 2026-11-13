#!/usr/bin/env python3
"""gspec: third-octave spectra side by side, each against its own 80 Hz-8 kHz total, for a part heard alone on a
record against ours rendered alone. (chirper-zero, Common Time v30.)

  gspec.py NAME=FILE[:START:DUR] ... [--diff] [--band LO-HI ...]

Each file (16- or 32-bit WAV), or START seconds for DUR seconds of it, is read in third-octaves from 63 Hz to
12.5 kHz; both channels' power is summed, so a panned guitar counts whole. Every row is relative to that file's own
80 Hz-8 kHz total, so level does not matter, only shape. With --diff the first row is the yardstick and the rest
are printed as differences from it. Find where a guitar is alone on a record with galone.py.
--band LO-HI (hertz; may be given more than once) adds a second table: each file's share in that band, against the
same total. USE IT BEFORE QUOTING ONE THIRD-OCTAVE: a strong harmonic on a band's edge moves that band alone by many
dB. The 80 Hz band read "13 dB less than the record" on rigs whose low F's second harmonic (87 Hz) sits on its
upper edge; across 71-112 Hz the shortfall was 5 dB (Common Time v32).
What it showed (obZen 3:03, Bleed 6:27, read from the records): our three heavy rigs alone were within 2-3 dB of the
record's guitar from 1.6 to 5 kHz, had 2-4.5 dB MORE at 500 Hz-1.25 kHz, 5 dB LESS at 71-112 Hz and nothing above
6.3 kHz (-18 dB at 8 kHz, -23 at 10 kHz; the record rolls off about 18 dB an octave). So a separated guitar stem's
"fizz" is the separator's. Read-only. Tests: tools/tests/test_gspec.py.
"""
import sys
import wave

import numpy as np

CS = [63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500]


def power(p, t0=None, dur=None):
    """(power spectrum of both channels together, its frequencies, the 80 Hz-8 kHz total)."""
    with wave.open(p) as w:
        sr = w.getframerate()
        sw = w.getsampwidth()
        if t0 is not None:
            w.setpos(int(t0 * sr))
        n = int(dur * sr) if dur else w.getnframes()
        x = np.frombuffer(w.readframes(n), "<i%d" % sw).astype(float).reshape(-1, w.getnchannels()) / 2 ** (8 * sw - 1)
    P = 0
    for ch in range(x.shape[1]):
        P = P + np.abs(np.fft.rfft(x[:, ch])) ** 2      # power of both channels (a panned guitar counts whole)
    f = np.fft.rfftfreq(len(x), 1 / sr)
    tot = P[(f >= 80) & (f < 8000)].sum()
    return P, f, tot


def spec(p, t0=None, dur=None):
    P, f, tot = power(p, t0, dur)
    return np.array([10 * np.log10(P[(f >= c / 2 ** (1 / 6)) & (f < c * 2 ** (1 / 6))].sum() / tot + 1e-12) for c in CS])


def shares(p, t0, dur, bands):
    """The file's share in each (lo, hi) band, dB against its 80 Hz-8 kHz total."""
    P, f, tot = power(p, t0, dur)
    return np.array([10 * np.log10(P[(f >= lo) & (f < hi)].sum() / tot + 1e-12) for lo, hi in bands])


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    bands, files = [], []
    it = iter(argv)
    for a in it:
        if a == "--band":
            lo, _, hi = next(it, "").partition("-")
            try:
                bands.append((float(lo), float(hi)))
            except ValueError:
                raise SystemExit("gspec: --band LO-HI in hertz, as in --band 71-112") from None
        elif not a.startswith("--"):
            files.append(a)
    if not files or "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0 if ("-h" in argv or "--help" in argv) else 2
    diff = "--diff" in argv
    rows, custom = [], []
    for a in files:
        name, rest = a.split("=", 1)
        parts = rest.split(":")
        at = (parts[0], float(parts[1]) if len(parts) > 1 else None, float(parts[2]) if len(parts) > 2 else None)
        rows.append((name, spec(*at)))
        if bands:
            custom.append((name, shares(*at, bands)))
    print("%-22s" % "Hz" + "".join("%6s" % (c if c < 1000 else "%gk" % (c / 1000)) for c in CS))
    for i, (name, s) in enumerate(rows):
        v = s - rows[0][1] if diff and i else s
        print("%-22s" % (name + (" -1st" if diff and i else "")) + "".join("%6.1f" % x for x in v))
    if bands:
        print("%-22s" % "band, Hz" + "".join("%12s" % ("%g-%g" % b) for b in bands))
        for i, (name, s) in enumerate(custom):
            v = s - custom[0][1] if diff and i else s
            print("%-22s" % (name + (" -1st" if diff and i else "")) + "".join("%12.1f" % x for x in v))
    return 0


if __name__ == "__main__":
    sys.exit(main())
