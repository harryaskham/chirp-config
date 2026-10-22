#!/usr/bin/env python3
"""vocalscore: vocal-stem terms (activity, cadence, pitch, vowels) on a synthetic sung line with known faults, and the
word similarity behind --asr (Whisper itself is not run here).

  python3 tools/tests/test_vocalscore.py      (from ~/.config/chirp; seconds)
"""
import os
import sys
import unittest

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import vocalscore as V  # noqa: E402

SR = 48000
RNG = np.random.default_rng(9)
LINE = [(0.4 + 0.45 * i, 0.32, 55 + int(RNG.integers(0, 12)), float(RNG.uniform(0.5, 1.5))) for i in range(40)]


def sing(shift=0.0, semis=0, silent=False):
    x = np.zeros(int(20 * SR))
    if silent:
        return x
    for at, ln, m, tilt in LINE:
        t = np.arange(int(ln * SR)) / SR
        f = 440 * 2 ** ((m + semis - 69) / 12)
        env = np.minimum(1, t / 0.02) * np.minimum(1, (ln - t) / 0.04)
        tone = sum(np.sin(2 * np.pi * h * f * t) / h ** tilt for h in range(1, 12) if h * f < 8000)
        a = int((at + shift) * SR)
        x[a:a + len(t)] += 0.1 * env * tone
    return x


class Terms(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ref = sing()

    def test_identical_scores_100(self):
        w = V.score(self.ref, self.ref.copy())
        for k in ("activity", "cadence", "pitch", "vowels"):
            self.assertAlmostEqual(w[k], 100.0, places=1, msg=k)

    def test_late_keeps_phrasing_but_loses_cadence_and_pitch(self):
        w = V.score(self.ref, sing(shift=0.25))
        self.assertGreater(w["activity"], 60)
        self.assertLess(w["cadence"], 40)
        self.assertLess(w["pitch"], 60)

    def test_transposed_keeps_cadence_but_loses_pitch(self):
        w = V.score(self.ref, sing(semis=2))
        self.assertGreater(w["cadence"], 80)
        self.assertLess(w["pitch"], 10)

    def test_silence_does_not_sing(self):
        w = V.score(self.ref, sing(silent=True) + 1e-6 * RNG.normal(size=len(self.ref)))
        self.assertLess(w["activity"], 20)

    def test_word_similarity(self):
        a = "you can't hurry love".split()
        self.assertEqual(V.word_similarity(a, a), 1.0)
        self.assertEqual(V.word_similarity(a, "you can't hurry dove".split()), 0.75)
        self.assertEqual(V.word_similarity(a, []), 0.0)
        self.assertIsNone(V.word_similarity([], a))


if __name__ == "__main__":
    unittest.main()
