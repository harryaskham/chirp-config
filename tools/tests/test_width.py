#!/usr/bin/env python3
"""width.py: side/mid by band (10 Nov, after chirper-three's finding that Accretion's top end was mono).

  python3 tools/tests/test_width.py      (from ~/.config/chirp; instant, synthetic signals, no ffmpeg)
"""
import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import width as W  # noqa: E402

N = W.SR * 4


def noise(seed, lo=None, hi=None):
    """White noise, optionally band-limited by zeroing FFT bins."""
    x = np.random.default_rng(seed).standard_normal(N)
    if lo is not None:
        X = np.fft.rfft(x)
        f = np.fft.rfftfreq(N, 1 / W.SR)
        X[(f < lo) | (f >= hi)] = 0
        x = np.fft.irfft(X, N)
    return x.astype(np.float32)


class Width(unittest.TestCase):
    def test_identical_channels_are_mono(self):
        x = noise(1)
        w = W.measure(np.stack([x, x], axis=1))
        self.assertTrue(all(v == W.MONO for v in w.values()))
        self.assertEqual(W.fmt(w["top"]), "mono")

    def test_a_one_channel_file_is_mono(self):
        self.assertEqual(W.measure(noise(1).reshape(-1, 1))["top"], W.MONO)

    def test_unrelated_channels_read_zero(self):
        """chirper-three's hat recipe: two independent noise layers hard left and right give 0 dB."""
        w = W.measure(np.stack([noise(1), noise(2)], axis=1))
        for band in ("mid", "high", "air", "top"):
            self.assertLess(abs(w[band]), 0.7, band)

    def test_opposite_channels_are_all_side(self):
        x = noise(1)
        self.assertGreater(W.measure(np.stack([x, -x], axis=1))["top"], 60)

    def test_width_is_read_band_by_band(self):
        """A mono body with independent air (6-16 kHz) left and right: wide in the air band only."""
        body = noise(1, 100, 6000)
        left, right = body + noise(2, 6000, 16000), body + noise(3, 6000, 16000)
        w = W.measure(np.stack([left, right], axis=1))
        self.assertLess(abs(w["air"]), 1.0)
        self.assertLess(w["mid"], -30)
        self.assertLess(w["high"], -30)
        self.assertLess(w["top"], w["air"])                    # the headline is the 2-16 kHz power ratio

    def test_a_panned_mono_source_is_not_wide_by_much(self):
        """A mono hat panned 30% reads narrow (what a pan alone gives): L = 0.65 x, R = 0.35 x -> about -10.5 dB."""
        x = noise(1)
        w = W.measure(np.stack([0.65 * x, 0.35 * x], axis=1))
        self.assertLess(abs(w["top"] - 20 * np.log10(0.15 / 0.5)), 0.2)

    def test_line(self):
        s = W.line("t8", {"low": -16.1, "mid": -3.9, "high": -9.0, "air": -14.2, "top": -10.5})
        self.assertIn("top (2-16 kHz) -10.5 dB", s)
        self.assertIn("air 6-16k -14.2", s)


if __name__ == "__main__":
    unittest.main()
