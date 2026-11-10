#!/usr/bin/env python3
"""bandprof: where a render's ENERGY sits, per octave, and its low end against its tunes (chirper-two, 10 Nov).

  bandprof.py FILE[@START+SECONDS] ...        any audio ffmpeg reads; @211+18 = 18 s from 3:31

Per file (or window): the share of the total power in each octave band from 20 Hz to 16 kHz, dB, from averaged POWER
spectra - the way a loudness stage counts, not the way compscore's spectrum term does (that averages frames in dB, so
a bass that hits and rests reads low and a held floor reads high) - and one figure:

  <90 vs 355-5k6   power below 90 Hz against power from 355 Hz to 5.6 kHz, dB

Why: loudness normalisation spends a song's level wherever its power is. Accretion at snapshot 0903 read +3.8 to
+5.8 dB on six tracks and +12.0 / +9.9 on t3 / t7 (the genre anchors -4.6 to +13.4, median +6.6): at the same -11 LUFS
those two songs' tunes played about 6 dB under their neighbours'. By section it shows which part of a song is all
sub (t3's storms +14.5 / +16.8 against its lock's +9.7). Read-only; a flashlight, not a score.
"""
import subprocess
import sys

import numpy as np

EDGES = [20, 45, 90, 180, 355, 710, 1400, 2800, 5600, 11000, 16000]


def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "48000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def profile(mono, sr=48000, n=8192):
    """Each octave band's share of the total power, dB."""
    win, acc, count = np.hanning(n), np.zeros(n // 2 + 1), 0
    for i in range(0, len(mono) - n, n):
        acc += np.abs(np.fft.rfft(mono[i:i + n] * win)) ** 2
        count += 1
    acc /= max(count, 1)
    f = np.fft.rfftfreq(n, 1 / sr)
    v = [10 * np.log10(acc[(f >= lo) & (f < hi)].sum() + 1e-20) for lo, hi in zip(EDGES[:-1], EDGES[1:])]
    total = 10 * np.log10(sum(10 ** (x / 10) for x in v))
    return [x - total for x in v]


def low_over_tunes(v):
    low = 10 * np.log10(10 ** (v[0] / 10) + 10 ** (v[1] / 10))
    mid = 10 * np.log10(sum(10 ** (x / 10) for x in v[4:8]))
    return low - mid


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    print(" " * 25 + " ".join(f"{e:>6}" for e in EDGES[:-1]) + "   <90 vs 355-5k6")
    for arg in argv:
        name, _, rng = arg.partition("@")
        mono = load(name)
        if rng:
            a, b = rng.split("+")
            mono = mono[int(float(a) * 48000):int((float(a) + float(b)) * 48000)]
        v = profile(mono)
        label = (name.split("/")[-1] + ("@" + rng if rng else ""))[:24]
        print(f"{label:24s} " + " ".join(f"{x:6.1f}" for x in v) + f"   {low_over_tunes(v):+6.1f}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
