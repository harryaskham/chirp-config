#!/usr/bin/env python3
"""tools/partchroma.py: a low note whose 3rd harmonic dominates reads a fourth low (+5), the same note with its root
reads 0, and silence is skipped.

  python3 tools/tests/test_partchroma.py      (from ~/.config/chirp; instant)
"""
import os
import sys
import unittest

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import partchroma as P  # noqa: E402

SR = P.SR
F1 = 43.65


def note(f0, weights, sec=2.0):
    t = np.arange(int(sec * SR)) / SR
    return sum(w * np.sin(2 * np.pi * f0 * h * t) for h, w in weights.items())


class Chroma(unittest.TestCase):
    def test_third_harmonic_dominating_reads_plus_five(self):
        record = note(F1, {1: 1.0, 2: 0.8, 3: 0.3, 4: 0.3})       # the record: F root and octave carry it
        ours = note(F1, {1: 0.02, 2: 0.05, 3: 1.0, 4: 0.3})       # ours: root and octave high-passed away, C dominates
        bars = [(1, 0.0, 2.0)]
        rows = P.audit(record, ours, bars, lo=60, hi=600)     # the default: F1 itself is below it
        self.assertEqual(rows[0]["shift"], 5)
        self.assertGreater(rows[0]["best"] - rows[0]["cos0"], 0.15)
        same = P.audit(record, record.copy(), bars, lo=60, hi=600)
        self.assertEqual(same[0]["shift"], 0)
        self.assertAlmostEqual(same[0]["cos0"], 1.0, places=6)

    def test_silence_skipped_and_summary(self):
        bars = [(1, 0.0, 1.0), (2, 1.0, 2.0)]
        record = np.concatenate([note(110.0, {1: 1.0}, 1.0), np.zeros(SR)])
        ours = record.copy()
        s = P.summary(P.audit(record, ours, bars, 60, 600))
        self.assertEqual(s["bars"], 1)
        self.assertEqual(s["bad"], [])


if __name__ == "__main__":
    unittest.main()
