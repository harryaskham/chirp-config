#!/usr/bin/env python3
"""tools/stemconsonants.py --plosives: a closure then a burst before a vowel reads as its stop (place by the burst's
centroid, voiced with a voice bar); a vowel straight after a vowel does not.

  python3 tools/tests/test_stemconsonants_plosive.py      (from ~/.config/chirp; instant)
"""
import os
import sys
import unittest

import numpy as np
from scipy import signal

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import stemconsonants as C  # noqa: E402

SR = C.SR
rng = np.random.default_rng(0)


def vowel(sec):
    t = np.arange(int(sec * SR)) / SR
    return 0.3 * sum(np.sin(2 * np.pi * 150 * h * t) / h for h in range(1, 20))


def burst(lo, hi, sec=0.008):
    sos = signal.butter(4, [lo, hi], btype="band", fs=SR, output="sos")
    return 0.3 * signal.sosfilt(sos, rng.normal(size=int(sec * SR))) * 3


def syllable(b, voicebar=False):
    """100 ms of preceding vowel, a 40 ms closure (optionally a 120 Hz voice bar), the burst, then the vowel.
    Returns (window from 120 ms before the vowel's onset to 20 ms after, the vowel 60-160 ms in)."""
    t = np.arange(int(0.04 * SR)) / SR
    closure = 0.02 * np.sin(2 * np.pi * 120 * t) if voicebar else 1e-5 * rng.normal(size=len(t))   # a voice bar ~24 dB under
    x = np.concatenate([vowel(0.1), closure, b, vowel(0.3)])
    on = int((0.1 + 0.04 + len(b) / SR) * SR)
    return x[on - int(0.12 * SR):on + int(0.02 * SR)], x[on + int(0.06 * SR):on + int(0.16 * SR)]


class Plosives(unittest.TestCase):
    def test_place_by_burst_centroid(self):
        self.assertEqual(C.plosive(*syllable(burst(3500, 9000))), 3)     # t
        self.assertEqual(C.plosive(*syllable(burst(300, 1000))), 1)      # p
        self.assertEqual(C.plosive(*syllable(burst(1500, 2600))), 5)     # k

    def test_voice_bar_makes_it_voiced(self):
        self.assertEqual(C.plosive(*syllable(burst(3500, 9000), voicebar=True)), 4)   # d

    def test_vowel_to_vowel_is_no_plosive(self):
        x = vowel(0.5)
        on = int(0.25 * SR)
        self.assertEqual(C.plosive(x[on - int(0.12 * SR):on + int(0.02 * SR)], x[on + int(0.06 * SR):on + int(0.16 * SR)]), 0)


if __name__ == "__main__":
    unittest.main()
