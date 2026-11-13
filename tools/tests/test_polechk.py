#!/usr/bin/env python3
"""tools/polechk.py: does a moving comb climb or fall, how fast, how deep (chirper-zero's, Common Time v28).

Hermetic: noise as the dry part, and the same noise through a comb an octave wide in log frequency that moves a known
number of twelfths each bar.

  python3 tools/tests/test_polechk.py      (from ~/.config/chirp; a few seconds)
"""
import contextlib
import io
import os
import shutil
import sys
import tempfile
import unittest
import wave

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import polechk as P  # noqa: E402

SR = 48000
BAR = 2.0                # a bar of four at 120


def pole(dry, twelfths_a_bar, depth_db):
    """dry through a comb one octave apart in log frequency, depth_db deep, moved twelfths_a_bar each bar."""
    L = int(BAR * SR)
    out = np.zeros(len(dry))
    f = np.fft.rfftfreq(L, 1 / SR)
    octs = np.log2(np.maximum(f, 1.0) / 100.0)
    for i in range(len(dry) // L):
        gain_db = depth_db / 2 * np.cos(2 * np.pi * (octs - i * twelfths_a_bar / 12.0))
        out[i * L:(i + 1) * L] = np.fft.irfft(np.fft.rfft(dry[i * L:(i + 1) * L]) * 10 ** (gain_db / 20), L)
    return out


def save(path, x):
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


class Pole(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="polechk-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self.dry = np.random.default_rng(3).standard_normal(int(BAR * SR) * 8) * 0.1

    def read(self, wet, seconds=BAR):
        return P.motion(P.frames_of(self.dry, wet, SR, seconds))

    def test_a_rising_pole_rises_and_a_falling_one_falls(self):
        up, depth = self.read(pole(self.dry, 2, 12.0))
        self.assertEqual(float(np.median(up)), 2.0)                        # two twelfths a bar: an octave in six bars
        self.assertAlmostEqual(float(np.median(depth)), 12.0 * 0.95, delta=1.0)   # 10th-90th percentile of a cosine
        down, _ = self.read(pole(self.dry, -3, 12.0))
        self.assertEqual(float(np.median(down)), -3.0)

    def test_a_comb_that_stands_still_and_no_comb_at_all(self):
        still, depth = self.read(pole(self.dry, 0, 12.0))
        self.assertEqual(float(np.median(still)), 0.0)
        self.assertGreater(float(np.median(depth)), 8.0)
        _, none = self.read(self.dry)
        self.assertLess(float(np.median(none)), 0.01)

    def test_the_tool_prints_speed_and_depth_and_tempo_sets_the_bar(self):
        d, w = os.path.join(self.root, "dry.wav"), os.path.join(self.root, "wet.wav")
        save(d, self.dry)
        save(w, pole(self.dry, 2, 12.0))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            P.main([d, w])
        self.assertIn("8 frames of 1 bar: shift per frame (twelfths of an octave) median +2.0", out.getvalue())
        self.assertIn("=> +0.17 octaves a bar (one octave in 6.0 bars); comb depth median", out.getvalue())
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            P.main([d, w, "2", "--tempo", "240"])                          # two bars at 240 are the same two seconds
        self.assertIn("8 frames of 2 bar: shift per frame (twelfths of an octave) median +2.0", out.getvalue())
        with self.assertRaises(SystemExit):
            P.main([d, w, "16"])


if __name__ == "__main__":
    unittest.main()
