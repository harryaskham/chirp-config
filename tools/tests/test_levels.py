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

    def test_clean_low_bass_is_not_flat_but_a_clamp_is(self):
        # wM, 30 Oct: a 40 Hz sine at the ceiling stayed within 0.01 dB of its crest for ~18 samples, so the old FLAT
        # flag fired on clean bass; identical samples are the clipping signature
        x = 0.89 * np.sin(2 * np.pi * 40 * T[:SR])
        self.assertLessEqual(LV.pinned_run(x[:, None]), 2)
        self.assertGreaterEqual(LV.pinned_run(np.clip(1.5 * x, -0.89, 0.89)[:, None]), 4)

    def test_flat_top_run(self):
        z = np.zeros(1000)
        z[100:110] = 1.0
        self.assertEqual(LV.longest_run(np.abs(z) >= 1.0), 10)


class Picture(unittest.TestCase):
    def test_right_against_left_correlation_and_dc(self):
        rng = np.random.default_rng(5)
        mid, side = rng.standard_normal(SR) * 0.1, rng.standard_normal(SR) * 0.05
        x = np.stack([mid + side, (mid - side) * 10 ** (1.0 / 20)], 1)          # the right 1 dB up
        bal, corr, dc = LV.stereo(x)
        self.assertAlmostEqual(bal, 1.0, delta=0.15)                             # (mid and side are a second of noise)
        self.assertGreater(corr, 0.5)
        self.assertLess(dc, 0.005)                                              # noise has no offset to speak of
        self.assertAlmostEqual(LV.stereo(np.stack([mid, -mid], 1))[1], -1.0, places=6)      # out of phase
        self.assertAlmostEqual(LV.stereo(np.stack([mid + 0.01, mid], 1))[2], 0.01, delta=0.001)
        self.assertEqual(LV.stereo(mid[:, None])[:2], (None, None))                         # one channel
        self.assertEqual(LV.stereo(np.stack([mid, 0 * mid], 1))[:2], (None, None))          # a silent side

    def test_a_file_that_leans_is_flagged_and_listed(self):
        import contextlib
        import io
        import tempfile
        import wave
        import likeness as L
        rng = np.random.default_rng(6)
        mid = rng.standard_normal(2 * L.SR) * 0.1
        with tempfile.TemporaryDirectory() as d:
            paths = []
            for name, x in (("level.wav", np.stack([mid, mid * 0.99], 1)), ("leans.wav", np.stack([mid, mid * 10 ** (-0.6 / 20)], 1)),
                            ("anti.wav", np.stack([mid, -mid], 1))):
                paths.append(os.path.join(d, name))
                with wave.open(paths[-1], "wb") as w:
                    w.setnchannels(2)
                    w.setsampwidth(2)
                    w.setframerate(L.SR)
                    w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())
            rows = [LV.measure(p) for p in paths]
            self.assertEqual([[f for f in r["flags"] if f in ("LEAN", "ANTI", "DC")] for r in rows], [[], ["LEAN"], ["ANTI"]])
            self.assertAlmostEqual(rows[1]["balance_db"], -0.6, delta=0.02)
            self.assertEqual(rows[2]["lr_corr"], -1.0)
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                LV.main(paths)
            text = out.getvalue()
            self.assertIn("the picture       R-L dB  L/R corr       DC   (right minus left over the whole file; LEAN at 0.5 dB;", text)
            self.assertIn("leans.wav          -0.60      1.00   0.0000", text)


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
