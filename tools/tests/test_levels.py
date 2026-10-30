"""levels.py: BS.1770 loudness, true peak and flat-top detection on signals with known answers."""
import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import levels as LV  # noqa: E402

SR = 48000
T = np.arange(10 * SR) / SR


class Loudness(unittest.TestCase):
    def test_997hz_stereo_sine_reads_its_peak_level(self):
        for db in (-20, -10):
            x = np.stack([10 ** (db / 20) * np.sin(2 * np.pi * 997 * T)] * 2, 1)
            self.assertAlmostEqual(LV.loudness(x, SR)[0], db, delta=0.05)

    def test_one_channel_is_3db_quieter(self):
        x = np.stack([0.1 * np.sin(2 * np.pi * 997 * T), 0 * T], 1)
        self.assertAlmostEqual(LV.loudness(x, SR)[0], -23.0, delta=0.05)


class Peaks(unittest.TestCase):
    def test_true_peak_sees_the_inter_sample_over(self):
        y = np.sin(2 * np.pi * (SR / 4) * T[:SR] + np.pi / 4)        # samples land at 0.707 of the true peak
        self.assertAlmostEqual(20 * np.log10(np.abs(y).max()), -3.01, delta=0.02)
        self.assertGreater(20 * np.log10(LV.true_peak(y[:, None])), -0.2)

    def test_flat_top_run(self):
        z = np.zeros(1000)
        z[100:110] = 1.0
        self.assertEqual(LV.longest_run(np.abs(z) >= 1.0), 10)


if __name__ == "__main__":
    unittest.main()


class Plugin(unittest.TestCase):
    """compose/measures/levels.py: a clean master scores 100, a flat-topped one loses 5 a pinned sample beyond 3, and it
    stays detail-only unless the album weights it."""

    def setUp(self):
        import importlib.util
        root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        spec = importlib.util.spec_from_file_location("levels_plugin", os.path.join(root, "compose", "measures", "levels.py"))
        self.P = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.P)

    def test_clean_and_flat_topped(self):
        x = np.stack([0.5 * np.sin(2 * np.pi * 997 * T[:SR])] * 2, 1)        # peak -6 dBFS, no pinned runs
        self.assertEqual(self.P.analyse(x, SR)["score"], 100.0)
        y = np.clip(2 * x, -0.8, 0.8)                                           # hard-clipped: long flat tops
        d = self.P.analyse(y, SR)
        self.assertGreaterEqual(d["longest_pinned_run"], 4)
        self.assertLess(d["score"], 100.0)

    def test_detail_only_without_an_album_weight(self):
        x = np.stack([0.5 * np.sin(2 * np.pi * 997 * T[:SR])] * 2, 1)
        _, d = self.P.measure({"x": x, "album": {"weights": {}}})
        self.assertEqual(d["weight_scale"], 0.0)
        _, d = self.P.measure({"x": x, "album": {"weights": {"levels": 0.05}}})
        self.assertNotIn("weight_scale", d)
