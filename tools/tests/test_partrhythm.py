#!/usr/bin/env python3
"""tools/partrhythm.py: a click train matches itself (corr ~1, 0 dB), a pattern shifted by half a beat reads low,
a missing part reads far quieter, and a one-frame offset is forgiven (as likeness's rhythm term does).

  python3 tools/tests/test_partrhythm.py      (from ~/.config/chirp; a few seconds)
"""
import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import partrhythm as P  # noqa: E402

SR = 48000


def clicks(times, dur, gain=1.0):
    x = np.zeros(int(dur * SR))
    rng = np.random.default_rng(0)
    for t in times:
        i = int(t * SR)
        burst = rng.standard_normal(int(0.02 * SR)) * np.exp(-np.arange(int(0.02 * SR)) / (0.004 * SR))
        x[i:i + len(burst)] += gain * 0.5 * burst[:len(x) - i]
    return np.stack([x, x], 1)


class Rhythm(unittest.TestCase):
    def setUp(self):
        self.fps = P.MS.L.FPS
        self.bars = [(1, 0.0, 2.0), (2, 2.0, 4.0)]
        self.beats = [0.25 * k for k in range(16)]

    def test_identical_and_offbeat(self):
        ref = P.onset_env(clicks(self.beats, 4.0))
        same = P.audit(ref, P.onset_env(clicks(self.beats, 4.0)), self.bars, self.fps)
        self.assertGreater(min(r["corr"] for r in same), 0.95)
        off = P.audit(ref, P.onset_env(clicks([t + 0.125 for t in self.beats], 4.0)), self.bars, self.fps)
        self.assertLess(max(r["corr"] for r in off), 0.3)

    def test_missing_part_reads_thin(self):
        ra, oa = clicks(self.beats, 4.0), clicks(self.beats, 4.0)
        oa[int(2.0 * SR):] *= 0.03                                 # bar 2 of ours nearly silent: a part missing
        rows = P.audit(P.onset_env(ra), P.onset_env(oa), self.bars, self.fps, ref_audio=ra, ours_audio=oa, sr=SR)
        lv = {r["bar"]: r["level_db"] for r in rows}
        self.assertLess(lv[2] - lv[1], -25)
        self.assertEqual(P.summary(rows)["thin"], [2])

    def test_one_frame_forgiven(self):
        a = np.zeros(200)
        a[::20] = 1.0
        b = np.roll(a, 1)
        self.assertGreater(P.corr(a, b), 0.99)
        self.assertIsNone(P.corr(np.zeros(10), a[:10]))


if __name__ == "__main__":
    unittest.main()
