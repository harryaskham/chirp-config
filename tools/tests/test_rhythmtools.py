#!/usr/bin/env python3
"""tools/warpgrid.py and tools/gapscan.py (wM's obZen rhythm tools): the beat clock follows a tempo map, a window's
lag comes from confident drums unless a confident mix disagrees, weak or alias lags read as 0, and gaps need the
stem playing while ours is silent for at least 1 s.

  python3 tools/tests/test_rhythmtools.py      (from ~/.config/chirp; instant)
"""
import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import gapscan as G  # noqa: E402
import warpgrid as W  # noqa: E402


class Warpgrid(unittest.TestCase):
    def test_beat_clock(self):
        self.assertAlmostEqual(W.beat_clock(120)(8), 4.0)
        f = W.beat_clock([{"at": "0b", "bpm": 120}, {"at": "8b", "bpm": 60}])
        self.assertAlmostEqual(f(8), 4.0)
        self.assertAlmostEqual(f(10), 6.0)                # two beats at 60 bpm after the knot

    def test_pick(self):
        # (lag ms, best r, r at lag 0)
        self.assertEqual(W.pick((40.0, 0.7, 0.5), (None, 0.0, 0.0)), (40.0, "d"))      # confident drums
        self.assertEqual(W.pick((40.0, 0.7, 0.68), (None, 0.0, 0.0)), (0.0, "d"))      # gains < 0.05 over lag 0: no drift
        self.assertEqual(W.pick((140.0, 0.7, 0.4), (0.0, 0.8, 0.7))[1], "m")           # a confident mix disagrees > 60 ms
        self.assertEqual(W.pick((10.0, 0.3, 0.2), (None, 0.0, 0.0)), (None, "-"))      # nothing confident


class Gapscan(unittest.TestCase):
    def test_gaps(self):
        ref = np.full(10, -20.0)
        ours = np.array([-10, -60, -60, -60, -10, -60, -10, -10, -10, -10], float)
        self.assertEqual(G.gaps(ref, ours), [(0.5, 2.0, -20.0)])      # 3 frames kept; the 1-frame dip at 5 dropped
        self.assertEqual(G.gaps(np.full(10, -40.0), ours), [])        # the stem itself is quiet: no gap

    def test_families_any_key_order(self):
        t = [{"name": "gtr-l", "patch": "m8-emg-l"}, {"name": "bass8", "patch": "bass-fat"},
             {"name": "drums", "patch": "metal-kit-dry"}, {"name": "vox", "patch": "kidman"},
             {"patch": "metal-kit-dry kit.t2.pitch=114.3hz", "name": "drumsr"}]          # patch before name (rngsafe)
        self.assertEqual(G.families(t), {"drums": ["drums", "drumsr"], "guitar+bass": ["gtr-l", "bass8"]})


if __name__ == "__main__":
    unittest.main()
