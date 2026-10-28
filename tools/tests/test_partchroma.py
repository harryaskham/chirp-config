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


class Detail(unittest.TestCase):
    def test_top_pitch_classes(self):
        prof = np.zeros(12)
        prof[5], prof[4], prof[3] = 0.5, 0.3, 0.2              # F, E, D#
        self.assertEqual(P.top(prof), [("F", 0.5), ("E", 0.3), ("D#", 0.2)])
        self.assertEqual(P.fmt_top(P.top(prof)), "F 0.50 E 0.30 D# 0.20")


class Centred(unittest.TestCase):
    def test_centred_is_likeness_scale(self):
        a = np.zeros(12)
        a[5] = 1.0                                               # all F
        b = np.full(12, 1 / 12)                                  # flat: no pitch content
        raw = P.match(a / a.sum(), b)
        self.assertGreater(raw[0], 0.25)                         # the raw cosine of 'F' vs 'nothing' still reads ~0.29
        self.assertIsNone(P.match(a / a.sum(), b, centred=True))  # centred, a flat profile has no direction
        c = np.zeros(12)
        c[0] = 1.0                                               # all C: unrelated to F
        self.assertLess(P.match(a, c, centred=True)[0], 0.0)    # centred: unrelated pitch reads below zero


if __name__ == "__main__":
    unittest.main()
