#!/usr/bin/env python3
"""tools/stereoscan.py: a band our render plays mono under a wide record is NARROW and MONO; a matching image is
not; the master width lanes pinned at the stage's maximum (or at the floor) are found with their spans.

  python3 tools/tests/test_stereoscan.py      (from ~/.config/chirp; a few seconds)
"""
import os
import shutil
import sys
import tempfile
import types
import unittest
import wave

import numpy as np
from scipy import signal

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import stereoscan as S  # noqa: E402

SR = 48000


def write(path, st):
    st = np.clip(st, -1, 1)
    with wave.open(path, "wb") as f:
        f.setnchannels(2), f.setsampwidth(2), f.setframerate(SR)
        f.writeframes((st * 32767).astype("<i2").tobytes())


def band(x, lo, hi):
    sos = signal.butter(4, [lo, hi], "bandpass", fs=SR, output="sos")
    return signal.sosfilt(sos, x)


class Stereo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = tempfile.mkdtemp(prefix="stereoscan-test-")
        n = SR * 30
        rng = np.random.default_rng(0)
        # The body (400 Hz-3.5 kHz): the same moderately wide image in both.
        body_l, body_r = band(rng.normal(size=n), 400, 3500), band(rng.normal(size=n), 400, 3500)
        mid = band(rng.normal(size=n), 400, 3500)
        body = np.stack([0.2 * mid + 0.05 * body_l, 0.2 * mid + 0.05 * body_r], 1)
        # The record's low bed (30-140 Hz): independent L/R, wide. Ours: the same bed mono.
        lo_l, lo_r = band(rng.normal(size=n), 30, 140), band(rng.normal(size=n), 30, 140)
        wide = np.stack([0.3 * lo_l, 0.3 * lo_r], 1)
        mono = np.stack([0.3 * lo_l, 0.3 * lo_l], 1)
        write(os.path.join(cls.d, "ref.wav"), body + wide)
        write(os.path.join(cls.d, "ours.wav"), body + mono)
        write(os.path.join(cls.d, "match.wav"), body + wide)
        with open(os.path.join(cls.d, "song.yaml"), "w") as f:
            f.write('tempo: 120\nmaster: {"chain": ["width"], "auto": {'
                    '"wb0": {"points": [["0s", 6.0], ["11.95s", 6.0], ["12.05s", 1.2], ["30s", 1.2]]}, '
                    '"wb1": {"points": [["0s", 6.0], ["30s", 6.0]]}, '
                    '"wb3": {"points": [["0s", 1.0], ["30s", 1.0]]}, '
                    '"wb6": {"points": [["0s", 0.3], ["30s", 0.3]]}}}\ntracks: []\n')
        cls.a = types.SimpleNamespace(win=10.0, under=10.0, mono=-40.0, lane_floor=0.5, min_pinned=10.0)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.d, ignore_errors=True)

    def p(self, n):
        return os.path.join(self.d, n)

    def test_a_mono_band_under_a_wide_record_is_narrow_and_mono(self):
        m = S.measure(self.p("ours.wav"), self.p("ref.wav"), self.a)
        by = {b["band"]: b for b in m["bands"]}
        for name in ("20-60", "60-150"):
            self.assertTrue(by[name]["narrow"], by[name])
            self.assertTrue(by[name]["mono"], by[name])
            self.assertGreater(by[name]["deficit_db"], 20)
            self.assertEqual(by[name]["narrow_share"], 1.0)
        for name in ("400-1.2k", "1.2k-3.5k"):
            self.assertFalse(by[name]["narrow"], by[name])

    def test_a_matching_image_has_no_narrow_band(self):
        m = S.measure(self.p("match.wav"), self.p("ref.wav"), self.a)
        self.assertFalse(any(b["narrow"] for b in m["bands"]), m["bands"])

    def test_width_lanes_pinned_at_the_maximum_or_the_floor(self):
        with open(self.p("song.yaml")) as f:
            lanes = S.width_lanes(f.read())
        self.assertEqual(sorted(lanes), [0, 1, 3, 6])
        p = S.pinned(lanes, end=30.0, floor=0.5)
        self.assertAlmostEqual(p[0]["at_max_s"], 12.0, delta=0.2)
        (a, b), = p[0]["max_spans"]
        self.assertEqual(a, 0.0)
        self.assertAlmostEqual(b, 12.0, delta=0.1)
        self.assertAlmostEqual(p[1]["at_max_s"], 30.0, delta=0.1)
        self.assertNotIn(3, p)                      # a lane at 1.0 is neither
        self.assertAlmostEqual(p[6]["at_floor_s"], 30.0, delta=0.1)
        self.assertEqual(p[6]["at_max_s"], 0)

    def test_the_report_names_the_mono_bands_the_maxed_lanes_and_the_fix(self):
        m = S.measure(self.p("ours.wav"), self.p("ref.wav"), self.a, self.p("song.yaml"))
        text = S.report("ours", m, self.a)
        self.assertIn("MONO", text)
        self.assertIn("width lanes maxed: 20-60, 60-150", text)
        self.assertRegex(text, r"lane wb0 \(20-60 Hz\): at max 6 for 12 s 0-12\b")
        self.assertIn("masterstack width:0.1,8", text)
        self.assertIn("image matches", S.report("match", S.measure(self.p("match.wav"), self.p("ref.wav"), self.a), self.a))


if __name__ == "__main__":
    unittest.main()
