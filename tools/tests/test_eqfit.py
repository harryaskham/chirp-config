#!/usr/bin/env python3
"""tools/eqfit.py: fit peaking-eq bands offline (chirper-zero's, Common Time v29).

Hermetic: noise as the part without the eq, and the same noise through two known peaking biquads as the tone
wanted; the fit must find them.

  python3 tools/tests/test_eqfit.py      (from ~/.config/chirp; a few seconds; needs scipy, as the tool does)
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
from scipy.signal import lfilter

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import eqfit as E  # noqa: E402

SR = 48000


def peaking(x, fc, q, g):
    A = 10 ** (g / 40)
    w0 = 2 * np.pi * fc / SR
    al = np.sin(w0) / (2 * q)
    b = np.array([1 + al * A, -2 * np.cos(w0), 1 - al * A])
    a = np.array([1 + al / A, -2 * np.cos(w0), 1 - al / A])
    return lfilter(b / a[0], a / a[0], x)


def save(path, x, rate=SR):
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


class Eqfit(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="eqfit-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self.src = np.random.default_rng(5).standard_normal(SR * 4) * 0.05
        self.tgt = peaking(peaking(self.src, 120.0, 2.0, 5.0), 400.0, 1.5, -4.0)

    def test_two_known_bands_are_found(self):
        cs, before, after, p = E.fit(self.tgt, self.src, SR)               # from the default start, 100:2:3,250:1.2:-3
        self.assertGreater(float(np.mean(np.abs(before))), 0.8)
        self.assertLess(float(np.mean(np.abs(after))), 0.15)
        self.assertAlmostEqual(p[0], 120.0, delta=8.0)
        self.assertAlmostEqual(p[2], 5.0, delta=0.6)
        self.assertAlmostEqual(p[3], 400.0, delta=30.0)
        self.assertAlmostEqual(p[5], -4.0, delta=0.6)
        self.assertEqual(list(cs[:3]), [63, 80, 100])
        self.assertEqual(int(cs[-1]), 5000)

    def test_a_part_that_already_matches_needs_no_eq(self):
        _, before, after, p = E.fit(self.src, self.src, SR)
        self.assertLess(float(np.max(np.abs(before))), 1e-6)
        self.assertLess(abs(p[2]) + abs(p[5]), 0.05)

    def test_the_tool_prints_before_after_and_the_bands(self):
        t, s = os.path.join(self.root, "t.wav"), os.path.join(self.root, "s.wav")
        save(t, self.tgt)
        save(s, self.src)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = E.main([t, s, "--peaks", "110:2:3,380:1.2:-3,2000:1:0", "--lo", "80", "--hi", "4000"])
        self.assertEqual(code, 0)
        lines = out.getvalue().splitlines()
        self.assertEqual(lines[0].split(), ["Hz"] + [str(c) for c in E.CENTRES if 80 <= c <= 4000])
        self.assertRegex(lines[1], r"^before  .* mean \|d\| [1-9]\.\d\d$")
        self.assertRegex(lines[2], r"^after   .* mean \|d\| 0\.[01]\d$")
        self.assertRegex(lines[3], r"^peaks   \d+:\d\.\d:[+-]?\d\.\d,\d+:\d\.\d:-\d\.\d,\d+:\d\.\d:-?\d\.\d$")   # three in, three out

    def test_two_files_are_needed_and_at_one_rate(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(E.main([]), 2)
        self.assertIn("eqfit.py TARGET.wav SOURCE.wav", out.getvalue())
        t, s = os.path.join(self.root, "t.wav"), os.path.join(self.root, "s.wav")
        save(t, self.tgt)
        save(s, self.src, rate=44100)
        with self.assertRaises(SystemExit) as e:
            E.main([t, s])
        self.assertIn("different sample rates", str(e.exception))


if __name__ == "__main__":
    unittest.main()
