#!/usr/bin/env python3
"""tools/bedlevel.py: the bed's level under the music over the body and per window, and the S&M rule's verdict.

  python3 tools/tests/test_bedlevel.py      (from ~/.config/chirp; instant)
"""
import os
import sys
import unittest

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import bedlevel as B  # noqa: E402

SR = B.L.SR


class BedLevel(unittest.TestCase):
    def test_levels_and_verdict(self):
        n = 60 * SR
        rng = np.random.default_rng(0)
        music = 0.3 * rng.normal(size=n)
        music[25 * SR:35 * SR] *= 0.01                   # a quiet passage (one whole window): the bed shows through
        bed = 0.03 * rng.normal(size=n)                  # -20 dB under the loud music
        body, med, worst = B.levels(bed, music, body=5, win=10)
        self.assertAlmostEqual(med, -20.0, delta=0.5)
        self.assertGreater(worst, 15.0)                  # 10 s where the bed is 20 dB over the quiet music
        self.assertEqual(B.verdict(body, worst), "TOO LOUD")
        self.assertEqual(B.verdict(-24.0, -14.0), "ok")
        self.assertEqual(B.verdict(-21.0, -8.0), "TOO LOUD")


if __name__ == "__main__":
    unittest.main()
