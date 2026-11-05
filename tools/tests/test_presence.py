#!/usr/bin/env python3
"""presence.py's measure: a track's level against its mix while it sounds, the near share, and the buried flag.

  python3 tools/tests/test_presence.py      (from ~/.config/chirp; under a second)
"""
import os
import sys
import unittest

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import presence as P  # noqa: E402


class Measure(unittest.TestCase):
    def test_frames_db_of_a_full_scale_sine(self):
        sr = 48000
        t = np.arange(sr * 2) / sr
        x = np.stack([np.sin(2 * np.pi * 440 * t)] * 2, axis=1)
        db = P.frames_db(x, sr)
        self.assertEqual(len(db), 5)                       # 2 s of 0.4 s frames
        self.assertAlmostEqual(float(db.mean()), -3.0, places=1)

    def test_buried_part_judged_while_it_sounds(self):
        mix = np.full(100, -10.0)
        solo = np.full(100, -200.0)
        solo[:10] = -45.0                                  # plays 10% of the time, 35 dB under the mix
        r = P.presence(mix, solo, buried=-25.0)
        self.assertAlmostEqual(r["vs_mix_db"], -35.0, places=1)
        self.assertTrue(r["buried"])
        self.assertAlmostEqual(r["active"], 0.1)
        self.assertEqual(r["near"], 0.0)

    def test_brief_but_present_part_is_not_buried(self):
        mix = np.full(100, -10.0)
        solo = np.full(100, -200.0)
        solo[50:55] = -14.0                                # brief, 4 dB under the mix while it plays
        r = P.presence(mix, solo)
        self.assertAlmostEqual(r["vs_mix_db"], -4.0, places=1)
        self.assertFalse(r["buried"])
        self.assertEqual(r["near"], 1.0)

    def test_silent_track(self):
        r = P.presence(np.full(10, -10.0), np.full(10, -200.0))
        self.assertTrue(r["silent"] and r["buried"])
        self.assertIsNone(r["vs_mix_db"])

    def test_kweighting_tames_the_sub_and_lifts_the_hats(self):
        sr = 48000
        t = np.arange(sr * 2) / sr
        sub = np.stack([0.5 * np.sin(2 * np.pi * 40 * t)] * 2, axis=1)
        hat = np.stack([0.05 * np.sin(2 * np.pi * 8000 * t)] * 2, axis=1)
        mix = sub + hat
        rms = {k: P.presence(P.frames_db(mix, sr), P.frames_db(v, sr))["vs_mix_db"] for k, v in (("sub", sub), ("hat", hat))}
        kw = {k: P.presence(P.frames_db(mix, sr, kweight=True), P.frames_db(v, sr, kweight=True))["vs_mix_db"]
              for k, v in (("sub", sub), ("hat", hat))}
        self.assertGreater(kw["hat"], rms["hat"] + 5)      # hats count for more once weighted as heard
        self.assertLess(kw["sub"], rms["sub"])


if __name__ == "__main__":
    unittest.main()
