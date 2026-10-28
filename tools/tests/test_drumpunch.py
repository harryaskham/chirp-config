#!/usr/bin/env python3
"""drumpunch's pure parts: tempo maps to seconds, clean-hit selection, the per-hit attack measure on synthetic
hits (a fast attack reads faster than a slow one; a tight decay shorter than a ringing one), and paired scoring.

  python3 tools/tests/test_drumpunch.py      (from ~/.config/chirp; ~2 s)
"""
import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import drumpunch as D  # noqa: E402

SR = D.SR


def hit(att_ms, decay_s, f=200.0, n=0.4):
    t = np.arange(int(n * SR)) / SR
    return np.sin(2 * np.pi * f * t) * (1 - np.exp(-t / (att_ms / 1000))) * np.exp(-t / decay_s)


class Tempo(unittest.TestCase):
    def test_constant_and_mapped(self):
        self.assertAlmostEqual(D.beats_to_seconds(120)(8), 4.0)
        f = D.beats_to_seconds([{"at": "0b", "bpm": 120, "ramp": False}, {"at": "4b", "bpm": 60, "ramp": False}])
        self.assertAlmostEqual(f(4), 2.0, places=2)
        self.assertAlmostEqual(f(6), 4.0, places=2)                  # 2 beats at 60 BPM after 4 at 120
        r = D.beats_to_seconds([{"at": "0b", "bpm": 60, "ramp": False}, {"at": "4b", "bpm": 120, "ramp": True}])
        self.assertAlmostEqual(r(4), 4 * np.log(2), places=2)         # ramp glides FROM the previous point (spec.rs):
                                                                      # 60 -> 120 over 4 beats = (60/15) ln 2 s


class Clean(unittest.TestCase):
    def test_only_lone_hits_of_the_class(self):
        evs = [(1.0, {"kick"}, 1), (1.01, {"snare"}, 1), (2.0, {"kick"}, 1), (3.0, {"kick", "snare"}, 1), (4.0, {"snare"}, 1)]
        self.assertEqual(D.clean(evs, "kick"), [2.0])
        self.assertEqual(D.clean(evs, "snare"), [4.0])


class Measure(unittest.TestCase):
    def test_attack_and_decay(self):
        fast, slow = hit(0.5, 0.03), hit(12.0, 0.03)
        ring = hit(0.5, 0.2)
        y = np.zeros(2 * SR)
        mf = D.measure(y, np.concatenate([np.zeros(SR // 10), fast, np.zeros(SR)]), 0.1, 0.5)
        ms = D.measure(y, np.concatenate([np.zeros(SR // 10), slow, np.zeros(SR)]), 0.1, 0.5)
        mr = D.measure(y, np.concatenate([np.zeros(SR // 10), ring, np.zeros(SR)]), 0.1, 0.5)
        self.assertLess(mf["rise_ms"] + 3, ms["rise_ms"])
        self.assertLess(mf["decay_ms"] + 50, mr["decay_ms"])
        self.assertGreater(mf["punch_db"], mr["punch_db"])


class Compare(unittest.TestCase):
    def test_identical_is_100_and_diffs_cost(self):
        r = {"rise_ms": 4.0, "punch_db": 12.0, "decay_ms": 40.0, "sub_click_db": 5.0}
        self.assertEqual(D.compare({"kick": [(r, dict(r))] * 5})["total"], 100.0)
        worse = dict(r, decay_ms=140.0)
        self.assertLess(D.compare({"kick": [(r, worse)] * 5})["total"], 80.0)   # one 100 ms decay error: 73


if __name__ == "__main__":
    unittest.main()
