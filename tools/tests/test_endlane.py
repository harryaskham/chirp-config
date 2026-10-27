#!/usr/bin/env python3
"""tools/endlane.py: the lane is the record's level minus ours per step from FROM (clipped), and an existing lane is
refused.

  python3 tools/tests/test_endlane.py      (from ~/.config/chirp; instant)
"""
import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import endlane as E  # noqa: E402

SR = 48000


class Lane(unittest.TestCase):
    def test_level_difference_becomes_the_lane(self):
        t = np.arange(4 * SR) / SR
        ref = 0.2 * np.sin(2 * np.pi * 220 * t)
        ours = ref * 0.5                                         # 6.02 dB quieter throughout
        pts, d = E.lane_points(ref, ours, SR, start=2.0)
        self.assertTrue(np.allclose(d, 6.02, atol=0.05))
        self.assertEqual(pts[:2], [["0s", 0], ["1.90s", 0]])
        self.assertEqual(pts[-1][1], 6.0)

    def test_clipped(self):
        t = np.arange(3 * SR) / SR
        ref = 0.2 * np.sin(2 * np.pi * 220 * t)
        pts, d = E.lane_points(ref, ref * 1e-3, SR, start=1.0, hi=20)  # 60 dB quieter -> clipped at +20
        self.assertTrue(np.all(d == 20))

    def test_existing_lane_refused(self):
        song = {"master": {"fx": [], "auto": {"cut": {"points": []}}}}
        with self.assertRaises(SystemExit):
            E.apply_lane(song, "cut", [["0s", 0]])
        s = E.apply_lane({"master": {"fx": []}}, "end2", [["0s", 0]])
        self.assertEqual(s["master"]["fx"][-1]["gain"]["mod"][0]["src"], "auto.end2")


if __name__ == "__main__":
    unittest.main()
