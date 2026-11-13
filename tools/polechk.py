#!/usr/bin/env python3
"""polechk: does a barber pole (or any moving comb) climb or fall, how fast, and how deep is it? (chirper-zero, Common
Time v28, where it showed `barberpole` at its default q doing nothing measurable; a tempo argument added by chirp-eco.)

  polechk.py DRY.wav WET.wav [BARS_PER_FRAME] [--tempo 120]

DRY and WET are the same part rendered alone, without and with the effect (the same notes, the same length). The wet
part over the dry one is taken in twelfth-octave bands from 100 to 3200 Hz, frame by frame (default one bar of four
at --tempo; BARS_PER_FRAME may be a fraction). The shift along the frequency axis that best lines each frame up with
the next gives the direction and the speed (octaves a bar; + is rising), and the ripple of a frame's band ratios
(their 10th to 90th percentile spread) says how deep the comb is. An octave-band meter cannot see a barber pole: each
octave always holds exactly one band. Read-only.
"""
import argparse
import sys
import wave

import numpy as np


def load(p):
    with wave.open(p) as w:
        sr = w.getframerate()
        return np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(float).reshape(-1, w.getnchannels()).mean(1) / 32768, sr


def frames_of(a, b, sr, seconds):
    """A row a frame: wet over dry in dB by twelfth-octave band (100-3200 Hz), each row about its own mean."""
    n = min(len(a), len(b))
    L = int(seconds * sr)
    edges = 100 * 2 ** (np.arange(61) / 12)
    out = []
    for i in range(n // L):
        A = np.abs(np.fft.rfft(a[i * L:(i + 1) * L] * np.hanning(L))) ** 2
        B = np.abs(np.fft.rfft(b[i * L:(i + 1) * L] * np.hanning(L))) ** 2
        f = np.fft.rfftfreq(L, 1 / sr)
        r = np.array([10 * np.log10((B[(f >= lo) & (f < hi)].sum() + 1e-18) / (A[(f >= lo) & (f < hi)].sum() + 1e-18))
                      for lo, hi in zip(edges, edges[1:])])
        out.append(r - r.mean())
    return np.array(out)


def motion(frames):
    """(the shift from each frame to the next in twelfths of an octave, each frame's comb depth in dB)."""
    lags = []
    for x, y in zip(frames, frames[1:]):
        best = max(range(-5, 6), key=lambda k: np.sum(x[max(0, -k):len(x) - max(0, k)] * y[max(0, k):len(y) - max(0, -k)]))
        lags.append(best)
    rip = [np.percentile(r, 90) - np.percentile(r, 10) for r in frames]
    return lags, rip


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("dry")
    ap.add_argument("wet")
    ap.add_argument("step", nargs="?", type=float, default=1.0, help="bars a frame (default 1)")
    ap.add_argument("--tempo", type=float, default=120.0, help="quarter-note BPM, for the length of a bar of four")
    a = ap.parse_args(argv)
    x, sr = load(a.dry)
    y, _ = load(a.wet)
    frames = frames_of(x, y, sr, a.step * 60 / a.tempo * 4)
    if len(frames) < 2:
        raise SystemExit("polechk: the files are shorter than two frames; give a smaller BARS_PER_FRAME")
    lags, rip = motion(frames)
    print("%d frames of %.2g bar: shift per frame (twelfths of an octave) median %+.1f, mean %+.2f  => %+.2f octaves a bar "
          "(one octave in %.1f bars); comb depth median %.1f dB"
          % (len(frames), a.step, np.median(lags), np.mean(lags), np.mean(lags) / 12 / a.step,
             abs(12 * a.step / np.mean(lags)) if np.mean(lags) else 0, np.median(rip)))


if __name__ == "__main__":
    sys.exit(main())
