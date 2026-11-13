#!/usr/bin/env python3
"""tools/bfit.py: the partials of a held string note and the inharmonicity that fits them (chirper-zero, for `inharm`).

Hermetic: synthetic strings whose partials follow f_n = n f1 sqrt(1 + B n^2) for a known B.

  python3 tools/tests/test_bfit.py      (from ~/.config/chirp; a few seconds)
"""
import contextlib
import io
import math
import os
import shutil
import sys
import tempfile
import unittest
import wave

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import bfit as B  # noqa: E402

SR = 48000


def string(f1, b, seconds=1.5):
    t = np.arange(int(seconds * SR)) / SR
    x = np.zeros(len(t))
    for n in range(1, int(min(50, 5000 / f1)) + 1):
        x += np.sin(2 * np.pi * n * f1 * math.sqrt(1 + b * n * n) * t) / n
    return x / np.abs(x).max() * 0.8


class Fit(unittest.TestCase):
    def test_a_stiff_string_reads_its_own_B(self):
        for f1, b in ((77.78, 1e-4), (43.65, 3e-4), (164.81, 5e-5)):
            got_f1, fs = B.partials(string(f1, b), SR, f1)
            cents, fitted = B.fit(got_f1, fs)
            self.assertAlmostEqual(got_f1, f1 * math.sqrt(1 + b), delta=0.05)
            self.assertAlmostEqual(fitted / b, 1.0, delta=0.08, msg=f"{f1} {b}")
        _, fs = B.partials(string(77.78, 1e-4), SR, 77.78)
        cents, _ = B.fit(fs[1], fs)
        self.assertAlmostEqual(cents[19], 1200 * math.log2(math.sqrt(1 + 1e-4 * 400)), delta=2.0)   # partial 20: 34 cents
        self.assertAlmostEqual(cents[39], 128.0, delta=4.0)                                         # partial 40

    def test_a_harmonic_string_reads_none(self):
        f1, fs = B.partials(string(77.78, 0.0), SR, 77.78)
        cents, fitted = B.fit(f1, fs)
        self.assertLess(abs(fitted), 2e-7)
        self.assertLess(float(np.abs(cents).max()), 1.0)

    def test_the_fundamental_is_found_a_little_off_the_asked_pitch(self):
        f1, _ = B.partials(string(78.5, 0.0), SR, 77.78)              # 16 cents sharp of the asked F0
        self.assertAlmostEqual(f1, 78.5, delta=0.05)


class Tool(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="bfit-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self.wav = os.path.join(self.root, "eb2.wav")
        x = string(77.78, 1e-4)
        with wave.open(self.wav, "wb") as w:
            w.setnchannels(2)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes(np.repeat((x * 32767).astype("<i2"), 2).tobytes())

    def run_tool(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            B.main([self.wav, *argv])
        return out.getvalue()

    def test_the_line_with_and_without_the_law(self):
        plain = self.run_tool("77.78")
        self.assertRegex(plain, r"^f1 77\.7\d\d Hz \([+-]0\.\d cents\) \| n5 2  n10 9  n20 3[345]  n30 7[456]  n40 1[23]\d  \| ")
        self.assertRegex(plain, r"\| B fitted (9\.[5-9]\de-05|1\.0\de-04)\n$")
        law = self.run_tool("77.78", "1e-4")
        self.assertRegex(law, r"n5 2/2  n10 9/9  n20 3[345]/34  n30 7[456]/75  n40 1[23]\d/128")
        self.assertRegex(law, r"\(asked 1e-04: [+-]\d%\)\n$")

    def test_no_arguments_prints_the_help(self):
        with self.assertRaises(SystemExit) as e:
            B.main([])
        self.assertIn("bfit.py WAV F0 [B]", str(e.exception))


if __name__ == "__main__":
    unittest.main()
