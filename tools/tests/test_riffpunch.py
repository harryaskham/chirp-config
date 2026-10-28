#!/usr/bin/env python3
"""riffpunch's pure parts: clean-onset selection, grain (spectral flatness) separating a noisy rig from a clean
harmonic series, and the paired comparison on identical sides.

  python3 tools/tests/test_riffpunch.py      (from ~/.config/chirp; ~2 s)
"""
import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import riffpunch as R  # noqa: E402

SR = R.SR


class Parts(unittest.TestCase):
    def test_clean_onsets(self):
        self.assertEqual(R.clean([1.0, 1.02, 2.0, 2.5, 2.55]), [2.0, 2.55])   # 2.55: 50 ms after 2.5, nothing after

    def test_grain_sees_noise_between_harmonics(self):
        t = np.arange(int(0.1 * SR)) / SR
        harm = sum(np.sin(2 * np.pi * 110 * k * t) / k for k in range(1, 40))
        noisy = harm + 0.3 * np.random.default_rng(0).standard_normal(len(t))
        self.assertGreater(R.flatness(noisy), R.flatness(harm) + 0.1)

    def test_identical_sides_score_100(self):
        rng = np.random.default_rng(1)
        y = np.zeros(4 * SR)
        ts = [0.5, 1.0, 1.5, 2.0, 2.5]
        for t in ts:
            n = int(0.2 * SR)
            seg = rng.standard_normal(n) * np.exp(-np.arange(n) / (0.05 * SR))
            y[int(t * SR):int(t * SR) + n] += seg
        r = R.compare(y, y, ts, 0.0)
        self.assertEqual(r["total"], 100.0)
        self.assertEqual(r["offset_ms"]["median"], 0.0)


if __name__ == "__main__":
    unittest.main()
