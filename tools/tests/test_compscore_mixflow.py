#!/usr/bin/env python3
"""compscore flow on mixtape albums (chirp-eco, 5 Nov): with compose/ALBUM/mixplan.md, a seam is judged on the bodies
either side of its crossfade (mix_head / mix_tail, placed like the groove and release --mix), not the faded ends.
Albums without a mix plan are unchanged.

  python3 tools/tests/test_compscore_mixflow.py      (from ~/.config/chirp; a second)
"""
import os
import sys
import tempfile
import unittest
from unittest import mock

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import chirpers as CH  # noqa: E402
import compscore as CS  # noqa: E402

FLAT = [0.0] * 8


def feat(level, profile=FLAT, **kw):
    return dict({"level": level, "profile": list(profile)}, **kw)


def ctx(me, others, n=2):
    album = {"id": "alb", "tracks": [{"n": 1, "id": "t1"}, {"n": 2, "id": "t2"}, {"n": 3, "id": "t3"}]}
    return {"me": me, "others": others, "slot": {"n": n, "id": f"t{n}"}, "album": album}


class Flow(unittest.TestCase):
    def test_no_mix_keys_is_the_old_measure(self):
        me = {"head": feat(-20), "tail": feat(-30)}
        oth = {"t1": {"head": feat(-10), "tail": feat(-14)}, "t3": {"head": feat(-30), "tail": feat(-12)}}
        s, d = CS.m_flow(ctx(me, oth))
        self.assertAlmostEqual(d["in"]["level_jump_db"], 6.0)    # my head -20 vs t1's tail -14
        self.assertAlmostEqual(d["out"]["level_jump_db"], 0.0)   # my tail -30 vs t3's head -30
        self.assertNotIn("measured", d["in"])
        self.assertNotIn("measured", d["out"])

    def test_mix_windows_used_when_both_sides_have_them(self):
        me = {"head": feat(-40), "tail": feat(-40), "mix_head": feat(-12, bars=16), "mix_tail": feat(-11, bars=16)}
        oth = {"t1": {"head": feat(-10), "tail": feat(-45), "mix_tail": feat(-11, bars=16)},
               "t3": {"head": feat(-45), "tail": feat(-10), "mix_head": feat(-11, bars=16)}}
        s, d = CS.m_flow(ctx(me, oth))
        self.assertAlmostEqual(d["in"]["level_jump_db"], 1.0)
        self.assertAlmostEqual(d["out"]["level_jump_db"], 0.0)
        self.assertTrue(d["in"]["measured"].startswith("mix:"))
        self.assertGreater(s, 90)

    def test_neighbour_without_mix_windows_falls_back_with_a_note(self):
        me = {"head": feat(-20), "tail": feat(-30), "mix_head": feat(-12, bars=16)}
        oth = {"t1": {"head": feat(-10), "tail": feat(-14)}}
        s, d = CS.m_flow(ctx(me, oth))
        self.assertAlmostEqual(d["in"]["level_jump_db"], 6.0)
        self.assertIn("predate the mix windows", d["in"]["measured"])


class Windows(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="mixflow-test-")
        os.makedirs(os.path.join(self.root, "compose", "alb"))
        self.song = os.path.join(self.root, "song.yaml")
        open(self.song, "w").write("tempo: 120\n")
        sr = CS.L.SR
        t = np.arange(int(20 * sr)) / sr
        amp = np.where(t < 8, 0.01, 0.5)[:, None]          # quiet for the first 8 s, loud after
        self.x = (amp * np.sin(2 * np.pi * 220 * t)[:, None] * np.ones((1, 2))).astype(np.float32)
        self.F = CS.L.Feat(self.x)
        self.album = {"id": "alb", "tracks": [{"n": 1}, {"n": 2}, {"n": 3}]}
        # 120 bpm: a beat every 0.5 s; last bar line at beat 36 (18 s)
        self.tl = {"bpm": lambda b: 120.0, "secs": 18.2, "times": [0.5 * i for i in range(40)], "end_beat": 36,
                   "dead": 0.2}

    def run_windows(self, mixplan=True, bars=None):
        if mixplan:
            open(os.path.join(self.root, "compose", "alb", "mixplan.md"), "w").write("# plan\n")
        me = {}
        with mock.patch.object(CS, "ROOT", self.root), \
                mock.patch.object(CH, "song_timeline", return_value=self.tl), \
                mock.patch.object(CH, "seam_overlaps", return_value=(bars or {}, 4)):
            CS.mix_windows(me, self.x, self.F, self.album, {"n": 2}, self.song, secs=2.0)
        return me

    def test_no_mixplan_adds_nothing(self):
        self.assertEqual(self.run_windows(mixplan=False), {})

    def test_windows_placed_like_the_mix(self):
        me = self.run_windows(bars={(1, 2): 4, (2, 3): 2})
        self.assertAlmostEqual(me["mix_head"]["at"], 8.0)    # bar 4 at 120 bpm = beat 16 = 8 s: after the in-crossfade
        self.assertAlmostEqual(me["mix_tail"]["at"], 12.0)   # seam_start: beat 36 - 8 = beat 28 = 14 s; minus 2 s
        self.assertEqual(me["mix_tail"]["bars"], 2)
        self.assertGreater(me["mix_head"]["level"], -10)      # the loud body, not the quiet intro


if __name__ == "__main__":
    unittest.main()
