#!/usr/bin/env python3
"""tools/bandend.py: the band's end is the last frame near the loud level, not the tail of a fade or of silence.

  python3 tools/tests/test_bandend.py      (from ~/.config/chirp; instant)
"""
import os
import sys
import unittest

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import bandend as B  # noqa: E402

SR = B.L.SR


class BandEnd(unittest.TestCase):
    def test_end_of_the_band_not_of_the_file(self):
        rng = np.random.default_rng(0)
        x = np.concatenate([0.3 * rng.normal(size=20 * SR), 1e-4 * rng.normal(size=10 * SR)])   # band 20 s, then near-silence
        self.assertAlmostEqual(B.band_end(x), 20.0, delta=0.3)

    def test_a_long_fade_ends_where_it_falls_below_the_floor(self):
        t = np.arange(30 * SR) / SR
        env = np.where(t < 20, 1.0, 10 ** (-(t - 20) * 6 / 20))      # -6 dB per second after 20 s
        x = 0.3 * np.random.default_rng(1).normal(size=len(t)) * env
        self.assertAlmostEqual(B.band_end(x, floor=40), 20 + 40 / 6, delta=0.5)

    def test_silence_has_no_end(self):
        self.assertIsNone(B.band_end(np.zeros(0)))


if __name__ == "__main__":
    unittest.main()
