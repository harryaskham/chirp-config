#!/usr/bin/env python3
"""ripple: how much FINE STRUCTURE a part's spectrum has: what makes a speaker cabinet sound like one, and what no
third-octave meter sees. (chirper-zero, Common Time v33: "a smooth response is not a cabinet".)

  ripple.py NAME=FILE[:START:DUR] ... [--over DRY.wav[:START:DUR]]

For each file (16- or 32-bit WAV; both channels' power summed), or START seconds for DUR seconds of it: the spectrum
in twelfth-octave bands, less its own running average over nine of them (about two thirds of an octave), as an rms
in dB, in three ranges: 400 Hz-1.6 kHz, 1.6-3.2 kHz and 3.2-6.4 kHz. A smooth response reads under 1 dB; a miked
speaker's cone break-up reads 1.5-3.
Guitars heard alone on three Meshuggah records (obZen 183.5+8 s, Combustion 44.6+2.5 s, Bleed 386.9+1.5 s) read
1.6-2.9 | 1.1-1.8 | 2.4-3.1 (the header repeats it). An amp with no cabinet 0.7 | 0.3 | 0.3; a smooth eq standing in
for a cabinet 0.9 | 0.6 | 0.9; the engine's `cab` 2x12 1.1 | 0.5 | 1.2 and 4x12 2.1 | 1.0 | 1.4; rigs on captured
cabinet files 2.4 | 1.6 | 1.8 and 4.0 | 1.2 | 2.6. Compare the same passage, or passages of about the same length:
a longer file averages more and reads a little lower.

--over DRY (chirp-eco): read each file's bands LESS the dry file's (the same passage before the stage being judged:
a rig's amp output with no cabinet, say), so the reading is the stage's own and not the notes'. WITHOUT IT THE LOW
RANGE READS THE RIFF: the amp alone, no cabinet, reads 0.68, 1.11 and 2.06 at 400 Hz-1.6 kHz on Common Time's three
riffs (the harmonics of the notes played), and every engine cabinet leaves that figure where it was. A record has
no dry signal, so its low-range figure holds its notes too: judge a cabinet's low-range detail with --over, and
against records only from 1.6 kHz up. Read-only. Tests: tools/tests/test_ripple.py.
"""
import sys
import wave

import numpy as np

RANGES = ((400, 1600), (1600, 3200), (3200, 6400))


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


def fine(P, f, lo, hi, n=12):
    """The spectrum's level in dB in n-th-octave bands from lo to hi."""
    E = lo * 2 ** (np.arange(0, int(np.log2(hi / lo) * n) + 1) / n)
    idx = np.searchsorted(f, E)
    return np.array([10 * np.log10(P[idx[i]:idx[i + 1]].sum() + 1e-20) for i in range(len(E) - 1)])


def ripple(P, f, lo, hi, n=12, dry=None):
    """The rms, in dB, of the n-th-octave bands from lo to hi about their own running average (two thirds of an octave);
    dry = (P, f) of the same passage before the stage being judged: its bands are taken off first."""
    b = fine(P, f, lo, hi, n)
    if dry is not None:
        b = b - fine(dry[0], dry[1], lo, hi, n)
    k = n // 3 * 2 + 1
    sm = np.convolve(np.pad(b, (k // 2, k // 2), mode="edge"), np.ones(k) / k, "valid")
    return np.sqrt(np.mean((b - sm) ** 2))


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if not argv or "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0 if argv else 2
    argv = list(argv)
    dry = None
    if "--over" in argv:
        i = argv.index("--over")
        if i + 1 >= len(argv):
            raise SystemExit("ripple: --over DRY.wav[:START:DUR]")
        parts = argv[i + 1].split(":")
        dry = spec(parts[0], float(parts[1]) if len(parts) > 1 else None, float(parts[2]) if len(parts) > 2 else None)
        del argv[i:i + 2]
    if dry is None:
        print("%-26s %8s %8s %8s   (records 1.6-2.9 | 1.1-1.8 | 2.4-3.1)" % ("ripple, dB", "0.4-1.6k", "1.6-3.2k", "3.2-6.4k"))
    else:
        print("%-26s %8s %8s %8s   (each file less the dry one: the stage's own)" % ("ripple, dB", "0.4-1.6k", "1.6-3.2k", "3.2-6.4k"))
    for a in argv:
        n, rest = a.split("=", 1)
        parts = rest.split(":")
        P, f = spec(parts[0], float(parts[1]) if len(parts) > 1 else None, float(parts[2]) if len(parts) > 2 else None)
        print("%-26s %8.2f %8.2f %8.2f" % ((n,) + tuple(ripple(P, f, lo, hi, dry=dry) for lo, hi in RANGES)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
