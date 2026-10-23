#!/usr/bin/env python3
"""tools/floorscan.py: a stretch where our render is silent but the record keeps a floor is a gap (by band); a floor
that matches is not; a record that is silent too is not.

  python3 tools/tests/test_floorscan.py      (from ~/.config/chirp; a few seconds)
"""
import os
import shutil
import sys
import tempfile
import types
import unittest
import wave

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import floorscan as F  # noqa: E402

SR = 48000


def write(path, x):
    x = np.clip(x, -1, 1)
    with wave.open(path, "wb") as f:
        f.setnchannels(2), f.setsampwidth(2), f.setframerate(SR)
        f.writeframes(np.repeat((x * 32767).astype("<i2"), 2).tobytes())


class Floor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = tempfile.mkdtemp(prefix="floorscan-test-")
        n = SR * 20
        t = np.arange(n) / SR
        rng = np.random.default_rng(0)
        tone = 0.3 * np.sin(2 * np.pi * 440 * t) + 0.05 * rng.normal(size=n)   # 'music': broadband outside the break
        tone[SR * 8:SR * 14] = 0                       # a 6 s break, 8-14 s: our render goes digitally silent
        hiss = 0.003 * rng.normal(size=n)              # the record's floor, under the music and through the break
        write(os.path.join(cls.d, "ref.wav"), tone + hiss)
        write(os.path.join(cls.d, "ours.wav"), tone)   # digital silence in the break
        write(os.path.join(cls.d, "floored.wav"), tone + 0.003 * np.random.default_rng(1).normal(size=n))
        silent_ref = tone.copy()
        write(os.path.join(cls.d, "silent-ref.wav"), silent_ref)
        cls.a = types.SimpleNamespace(win=2.0, under=20.0, quiet=-90.0)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.d, ignore_errors=True)

    def p(self, n):
        return os.path.join(self.d, n)

    def test_digital_silence_under_a_floor_is_a_gap(self):
        m = F.measure(self.p("ours.wav"), self.p("ref.wav"), self.a)
        self.assertGreaterEqual(m["windows"], 2)
        r = m["runs"][0]
        self.assertGreaterEqual(r["from"], 8.0)
        self.assertLessEqual(r["to"], 14.0)
        self.assertGreater(r["worst_db"], 20)
        self.assertTrue(any(b.endswith("k") or "k-" in b for b in r["bands"]))   # hiss: the upper bands

    def test_a_matching_floor_is_no_gap(self):
        self.assertEqual(F.measure(self.p("floored.wav"), self.p("ref.wav"), self.a)["windows"], 0)

    def test_a_silent_record_is_no_gap(self):
        self.assertEqual(F.measure(self.p("ours.wav"), self.p("silent-ref.wav"), self.a)["windows"], 0)

    def test_runs_merge_adjacent_windows(self):
        g = [(4, [(8, 30.0)]), (5, [(7, 25.0)]), (9, [(8, 22.0)])]
        self.assertEqual(F.runs(g, 2.0), [(8.0, 12.0, {7, 8}, 30.0), (18.0, 20.0, {8}, 22.0)])


if __name__ == "__main__":
    unittest.main()
