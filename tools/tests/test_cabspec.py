#!/usr/bin/env python3
"""tools/cabspec.py: a rig alone against the mean of records' guitar-alone passages (chirper-zero's).

Hermetic: two "records" of noise, the second 6 dB up above 1 kHz, in a stand-in ref/ folder.

  python3 tools/tests/test_cabspec.py      (from ~/.config/chirp; a second)
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

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import cabspec as C  # noqa: E402

SR = 44100


def save(path, x):
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


def bright(x):
    f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(np.fft.rfft(x) * np.where(f >= 1000, 2.0, 1.0), len(x))


class Cabspec(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="cabspec-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self.old = C.REF
        C.REF = os.path.join(self.root, "ref", "")
        self.addCleanup(lambda: setattr(C, "REF", self.old))
        os.makedirs(C.REF)
        a = np.random.default_rng(1).standard_normal(SR * 3) * 0.05
        b = bright(np.random.default_rng(2).standard_normal(SR * 3) * 0.05)
        save(C.REF + "recA.wav", a)
        save(C.REF + "recB.wav", b)
        self.recs = "recA:0.5:2,recB:0.5:2"
        self.a = C.REF + "recA.wav:0.5:2"
        self.b = C.REF + "recB.wav:0.5:2"

    def run_tool(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = C.main(list(argv))
        return code, out.getvalue()

    @staticmethod
    def row(line):
        """A row's twenty-four third-octaves (six characters each after the 14-character name) and the rest of the line."""
        return [float(line[14 + 6 * i:20 + 6 * i]) for i in range(len(C.CS))], line[14 + 6 * len(C.CS):]

    def test_the_record_is_the_mean_of_the_passages_and_its_spread_their_difference(self):
        code, text = self.run_tool("--abs", "--recs", self.recs, "a=" + self.a, "b=" + self.b)
        self.assertEqual(code, 0)
        lines = text.splitlines()
        self.assertTrue(lines[0].startswith("%-14s" % "Hz" + "   63    80   100"))
        self.assertTrue(lines[1].startswith("RECORD"))
        self.assertTrue(lines[2].startswith("its spread"))
        rec, spread = self.row(lines[1])[0], self.row(lines[2])[0]
        a, b = self.row(lines[3])[0], self.row(lines[4])[0]
        for i in range(len(C.CS)):
            self.assertAlmostEqual(rec[i], (a[i] + b[i]) / 2, delta=0.11)
            self.assertAlmostEqual(spread[i], abs(a[i] - b[i]), delta=0.11)
        hi, lo = list(C.CS).index(4000), list(C.CS).index(250)
        self.assertAlmostEqual((b[hi] - b[lo]) - (a[hi] - a[lo]), 6.0, delta=2.0)   # the second record is 6 dB brighter above 1 kHz

    def test_a_file_is_printed_as_its_difference_and_both_readings_follow_the_row(self):
        _, text = self.run_tool("--recs", self.recs, "a=" + self.a, "b=" + self.b)
        lines = text.splitlines()
        spread = self.row(lines[2])[0]
        (a, rest_a), (b, _) = self.row(lines[3]), self.row(lines[4])
        i0, i1 = list(C.CS).index(100), list(C.CS).index(10000) + 1
        for i in range(i0, i1):
            self.assertAlmostEqual(a[i], -b[i], delta=0.11)                # each record is half the spread from their mean
            self.assertAlmostEqual(abs(a[i]), spread[i] / 2, delta=0.11)
        first, second = rest_a.split("|")
        worst, at, mean = first.split()
        self.assertAlmostEqual(abs(float(worst)), max(abs(v) for v in a[i0:i1]), delta=0.06)
        self.assertTrue(at.startswith("@"))
        self.assertAlmostEqual(float(mean), sum(abs(v) for v in a[i0:i1]) / (i1 - i0), delta=0.06)
        wide_lo, wide_hi, worst2, mean2 = (float(v) for v in second.split())
        self.assertLess(abs(wide_lo - wide_hi), 1.0)                       # under 1 kHz the two records have one shape
        self.assertLessEqual(abs(worst2), abs(float(worst)) + 0.06)
        j0 = list(C.CS).index(315)
        self.assertAlmostEqual(mean2, (abs(wide_lo) + abs(wide_hi) + sum(abs(v) for v in a[j0:i1])) / (2 + i1 - j0), delta=0.06)

    def test_the_default_records_are_the_three_meshuggah_passages(self):
        self.assertEqual(C.RECS, (("obzen", 183.5, 8), ("combustion", 44.6, 2.5), ("bleed", 386.9, 1.5)))

    def test_recs_must_parse_and_no_arguments_is_the_help(self):
        with self.assertRaises(SystemExit) as e:
            self.run_tool("--recs", "recA", "a=" + self.a)
        self.assertIn("--recs ID:START:DUR", str(e.exception))
        code, text = self.run_tool()
        self.assertEqual(code, 2)
        self.assertIn("cabspec.py [--abs]", text)


if __name__ == "__main__":
    unittest.main()
