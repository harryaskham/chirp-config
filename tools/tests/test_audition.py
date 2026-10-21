#!/usr/bin/env python3
"""audition.compare: a soloed part vs its stem (chirper-zero's request) on synthetic parts with known differences.

  python3 tools/tests/test_audition.py      (from ~/.config/chirp; seconds)
"""
import os
import sys
import unittest

import numpy as np
from scipy import signal

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import audition as A  # noqa: E402

SR = 48000


def part(decay=0.08, notes=(57, 60, 64, 67, 69, 72, 64, 60) * 2, step=0.5):
    """Plucked harmonic notes every `step` s with an exponential decay; mono."""
    x = np.zeros(int(len(notes) * step * SR) + SR)
    t = np.arange(int(step * SR)) / SR
    for i, p in enumerate(notes):
        f = 440 * 2 ** ((p - 69) / 12)
        tone = sum(np.sin(2 * np.pi * k * f * t) / k for k in range(1, 9)) * np.exp(-t / decay)
        a = int(i * step * SR)
        x[a:a + len(t)] += 0.2 * tone
    return x[:int(len(notes) * step * SR)]


def stereo(x, side=0.0):
    rng = np.random.default_rng(5)
    s = side * signal.lfilter([1], [1, -0.5], rng.normal(size=len(x))) * np.abs(x).max() * 0.2
    return np.stack([x + s, x - s], axis=1).astype(np.float32)


class Compare(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stem = stereo(part())
        cls.same = A.compare(cls.stem, cls.stem.copy())

    def test_identical_part_matches(self):
        r = self.same
        self.assertEqual(r["level_db"]["diff"], 0.0)
        self.assertLess(max(abs(v) for v in r["envelope"]["diff_db"]), 0.01)
        self.assertGreater(r["notes"]["pitch"], 95)
        self.assertGreater(r["notes"]["timing"], 95)
        self.assertEqual(r["decay20_ms"]["stem"], r["decay20_ms"]["ours"])

    def test_a_darker_part_shows_negative_highs_and_a_lower_centroid(self):
        b, a = signal.butter(4, 1200, fs=SR)
        dark = signal.lfilter(b, a, self.stem, axis=0).astype(np.float32)
        r = A.compare(self.stem, dark)
        top = r["envelope"]["largest"][0]
        self.assertGreater(top["hz"], 1500)
        self.assertLess(top["diff_db"], -10)
        self.assertLess(r["centroid_hz"]["ours"], r["centroid_hz"]["stem"] * 0.8)

    def test_a_wider_part_measures_wider(self):
        r = A.compare(stereo(part(), side=0.0), stereo(part(), side=1.0))
        self.assertGreater(r["width_db"]["ours"], r["width_db"]["stem"] + 10)

    def test_a_longer_decay_measures_longer(self):
        r = A.compare(self.stem, stereo(part(decay=0.15)))   # -20 dB at ~345 ms, before the next note (500 ms)
        self.assertGreater(r["decay20_ms"]["ours"], 1.5 * r["decay20_ms"]["stem"])
        self.assertAlmostEqual(r["onsets_per_s"]["ours"], r["onsets_per_s"]["stem"], delta=0.5)

    def test_decays_cut_by_the_next_note_are_not_measured(self):
        r = A.compare(self.stem, stereo(part(decay=0.25)))   # -20 dB only at ~576 ms: every note is cut first
        self.assertIsNone(r["decay20_ms"]["ours"])
        self.assertEqual(r["decay20_ms"]["measured"][1], 0)

    def test_level_difference_is_reported_in_db(self):
        r = A.compare(self.stem, self.stem * 0.5)
        self.assertAlmostEqual(r["level_db"]["diff"], -6.02, delta=0.05)


if __name__ == "__main__":
    unittest.main()
