#!/usr/bin/env python3
"""tempoclock: one clock for a number or a tempo map, held to compscore's and drumpunch's (bd-10e881).

  python3 tools/tests/test_tempoclock.py      (from ~/.config/chirp; ~1 s)
"""
import os
import sys
import tempfile
import unittest

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import compscore as CS  # noqa: E402
import drumpunch as D  # noqa: E402
import tempoclock as T  # noqa: E402

GEAR = [{"at": 0, "bpm": 122.7756}, {"at": "268b", "bpm": 130.9606}]                    # Slow Enough to Count v18's map
RAMP = [{"at": "0b", "bpm": 90}, {"at": "32b", "bpm": 150, "ramp": True}, {"at": "64b"}, {"at": 96, "bpm": 60}]
LATE = [{"at": "16b", "bpm": 100}, {"at": "48b", "bpm": 140}]                             # no point at beat 0


class Clock(unittest.TestCase):
    def test_one_tempo_is_the_old_arithmetic(self):
        for t in (144, "144", 144.0):
            c = T.of(t)
            self.assertFalse(c.mapped)
            self.assertAlmostEqual(c.secs(36), 36 * 60 / 144)
            self.assertAlmostEqual(c.beats(15.0), 15.0 * 144 / 60)
            self.assertEqual(c.bpm, 144.0)
        self.assertEqual(T.of(None).bpm, 120.0)
        self.assertEqual(T.of([]).bpm, 120.0)
        self.assertEqual(T.of(None, default=96).bpm, 96.0)
        flat = T.of([{"at": 0, "bpm": 88}, {"at": "64b", "bpm": 88}])                   # a map that never changes
        self.assertFalse(flat.mapped)
        self.assertAlmostEqual(flat.secs(88), 60.0)
        self.assertEqual(T.of(144).secs([0, 12]), [0.0, 5.0])

    def test_a_change_of_gear_is_followed_and_comes_back(self):
        c = T.of(GEAR)
        self.assertTrue(c.mapped)
        at = 268 * 60 / 122.7756
        self.assertAlmostEqual(c.secs(268), at, places=9)
        self.assertAlmostEqual(c.secs(300), at + 32 * 60 / 130.9606, places=9)           # the faster count after the change
        self.assertAlmostEqual(c.bpm_at(100), 122.7756)
        self.assertAlmostEqual(c.bpm_at(268), 130.9606)
        for b in (0, 1.5, 267.99, 268, 268.01, 400):
            self.assertAlmostEqual(c.beats(c.secs(b)), b, places=7)
        one = T.of(122.7756)                                                             # what a one-tempo tool would say
        self.assertGreater(one.secs(400) - c.secs(400), 3.9)                             # four seconds late by the end

    def test_it_is_compscores_clock_and_drumpunchs(self):
        beats = [0, 3.25, 16, 31.9, 32, 40, 63.99, 64, 80, 96, 96.5, 200]
        for m in (GEAR, RAMP, LATE):
            c = T.of(m)
            with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
                f.write("tempo: " + repr(m).replace("'", '"').replace("True", "true") + "\ntracks: []\n")
            self.addCleanup(os.remove, f.name)
            pts = CS.tempo_points(f.name)
            self.assertEqual(pts, T.points(m))                                           # the same points
            segs = CS.tempo_segments(pts)
            want = CS.map_secs(segs, np.array(beats, float))
            for b, w in zip(beats, want):
                self.assertAlmostEqual(c.secs(b), float(w), places=9)
                self.assertAlmostEqual(c.beats(float(w)), CS.map_beats(segs, float(w)), places=7)
            self.assertEqual([round(x, 9) for x in T.of_song(f.name).secs(beats)], [round(x, 9) for x in c.secs(beats)])
            if m is not LATE:                                                            # drumpunch wants a point at 0
                to_s = D.beats_to_seconds([dict(p, at=str(p["at"])) for p in m if p.get("bpm") is not None])
                tol = 0.02 if m is RAMP else 1e-6                                        # its ramp is a 1/64-beat staircase
                for b in beats[:9]:
                    self.assertAlmostEqual(c.secs(b), to_s(b), delta=tol)
        r = T.of(RAMP)
        self.assertAlmostEqual(r.bpm_at(16), 120.0)                                      # half way up the ramp
        self.assertAlmostEqual(r.bpm_at(70), 150.0)                                      # the point with no bpm holds it
        self.assertAlmostEqual(r.bpm_at(100), 60.0)

    def test_a_written_position_is_placed_on_the_map(self):
        import warp
        one, gear = T.of(96), T.of(GEAR)
        for v in (12, 12.5, "96b", "8bar", "8bars", "1.5s", "200ms", "40"):
            self.assertAlmostEqual(one.at(v), warp.beats(v, 96), places=9)               # one tempo: warp's arithmetic
        self.assertEqual(gear.at("300b"), 300.0)
        self.assertEqual(gear.at("75bar"), 300.0)
        self.assertAlmostEqual(gear.at(f"{gear.secs(300)}s"), 300.0, places=6)           # seconds go through the map
        self.assertLess(warp.beats(f"{gear.secs(300)}s", 122.7756), 298.1)               # ... where one tempo would be two beats out
        with self.assertRaises(ValueError):
            one.at(True)

    def test_what_it_cannot_place_it_says(self):
        for bad in ([{"at": "4bars", "bpm": 100}, {"at": "8bars", "bpm": 120}], [{"at": 0, "bpm": 0}, {"at": 4, "bpm": 9}],
                    [100, 120], [{"at": 0}, {"at": 8, "bpm": 100}]):
            with self.assertRaises(ValueError):
                T.of(bad)
        with self.assertRaises(ValueError):
            T.of("fast")


if __name__ == "__main__":
    unittest.main()
