#!/usr/bin/env python3
"""riffpunch's pure parts: clean-onset selection, grain (spectral flatness) separating a noisy rig from a clean
harmonic series, and the paired comparison on identical sides.

  python3 tools/tests/test_riffpunch.py      (from ~/.config/chirp; ~2 s)
"""
import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import riffpunch as R  # noqa: E402

SR = R.SR


class Parts(unittest.TestCase):
    def test_clean_onsets(self):
        self.assertEqual(R.clean([1.0, 1.02, 2.0, 2.5, 2.55]), [2.0, 2.55])   # 2.55: 50 ms after 2.5, nothing after

    def test_grain_sees_noise_between_harmonics(self):
        t = np.arange(int(0.1 * SR)) / SR
        harm = sum(np.sin(2 * np.pi * 110 * k * t) / k for k in range(1, 40))
        noisy = harm + 0.3 * np.random.default_rng(0).standard_normal(len(t))
        self.assertGreater(R.flatness(noisy), R.flatness(harm) + 0.1)

    def test_identical_sides_score_100(self):
        rng = np.random.default_rng(1)
        y = np.zeros(4 * SR)
        ts = [0.5, 1.0, 1.5, 2.0, 2.5]
        for t in ts:
            n = int(0.2 * SR)
            seg = rng.standard_normal(n) * np.exp(-np.arange(n) / (0.05 * SR))
            y[int(t * SR):int(t * SR) + n] += seg
        r = R.compare(y, y, ts, 0.0)
        self.assertEqual(r["total"], 100.0)
        self.assertEqual(r["offset_ms"]["median"], 0.0)

    def burst(self, y, t, lo, hi, rng):
        n = int(0.2 * SR)
        seg = rng.standard_normal(n) * np.exp(-np.arange(n) / (0.05 * SR))
        y[int(t * SR):int(t * SR) + n] += R.D.bandpass(seg, lo, hi)

    def test_strokes_read_a_songs_own_strokes(self):
        """--strokes (chirper-zero's bench, Extreme and Mean v23): an original song's strokes by the same measures."""
        rng = np.random.default_rng(2)
        ts = [10.5, 11.0, 11.01, 11.5, 12.0, 12.5, 13.9, 14.5]          # 11.0 and 11.01 are not clean; 13.9 is too late
        dull, bright = np.zeros(5 * SR), np.zeros(5 * SR)
        for t in ts[:-1]:
            self.burst(dull, t - 10.0, 400, 1000, rng)
            self.burst(bright, t - 10.0, 1000, 4000, rng)
        a, b = R.strokes_read(dull, ts, 10.0, 14.0), R.strokes_read(bright, ts, 10.0, 14.0)
        self.assertEqual((a["n"], a["of"]), (4, 7))                     # 10.5, 11.5, 12.0, 12.5 read; 14.5 is outside
        self.assertEqual(sorted(a["ours"]), sorted(R.TOL))
        self.assertGreater(a["ours"]["scoop_db"], 10)                   # all of it under 1 kHz: no teeth
        self.assertLess(b["ours"]["scoop_db"], -10)                     # all of it at 1-4 kHz
        self.assertEqual(R.strokes_read(dull, [20.0], 10.0, 14.0), {"n": 0, "of": 0, "ours": dict.fromkeys(R.TOL)})

    def test_the_records_table(self):
        recs = R.records_table()
        self.assertEqual(len(recs), 6)
        st = R.records_stats(recs)
        self.assertAlmostEqual(st["scoop_db"][0], -11.31, delta=0.01)   # chirper-zero's figure: -11.3 (-12.7 to -6.5)
        self.assertAlmostEqual(st["scoop_db"][1], -12.749)
        self.assertAlmostEqual(st["scoop_db"][2], -6.541)
        self.assertAlmostEqual(st["rise_ms"][0], 19.75)
        res = {"n": 4, "of": 7, "ours": {k: st[k][0] + 1 for k in R.TOL}}
        text = "\n".join(R.strokes_lines(res, st, len(recs)))
        self.assertIn("ours - records", text)
        self.assertIn("+1.00", text)
        self.assertIn("median of 6 records' guitar stems", text)

    def test_a_guitar_by_its_chain_only_when_asked(self):
        twin = {"synth": {"layers": [{"type": "pluck"}]}, "fx": [{"type": "amp"}, {"type": "cab"}]}
        can = {"tempo": 120, "patches": {"ct-twin": twin, "ct-bass": twin, "juno": {"synth": {"layers": [{"type": "saw"}]}, "fx": []}},
               "tracks": [{"name": "gl", "patch": "ct-twin", "notes": [{"at": 0}, {"at": 2}]},
                          {"name": "low", "patch": "ct-bass", "notes": [{"at": 1}]},
                          {"name": "pad", "patch": "juno", "notes": [{"at": 3}]},
                          {"name": "lead", "patch": "m8-lead-guitar", "notes": [{"at": 4}]}]}
        self.assertEqual(R.events_from(can), ([2.0], ["lead"]))                     # a reproduction's tracks: as they were
        self.assertEqual(R.events_from(can, by_chain=True), ([0.0, 1.0, 2.0], ["gl", "lead"]))
        self.assertEqual(R.events_from(can, ["low"], by_chain=True), ([0.5], ["low"]))   # named: whatever it is


if __name__ == "__main__":
    unittest.main()
