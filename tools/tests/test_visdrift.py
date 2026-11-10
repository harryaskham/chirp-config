#!/usr/bin/env python3
"""visdrift: a programme's scene cuts against a song whose structure moved (10 Nov).

  python3 tools/tests/test_visdrift.py      (from ~/.config/chirp; instant, no engine or audio)
"""
import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import visdrift as V  # noqa: E402


def clock(bpm, bars, per=4.0):
    """A constant-tempo song of BARS bars: the shape visdrift.clock returns."""
    times = np.arange(0, bars * per + 8) * 60.0 / bpm
    return {"secs": bars * per * 60.0 / bpm, "times": times, "per": per, "bars": float(bars)}


class Compare(unittest.TestCase):
    def test_an_unchanged_song_is_in_step(self):
        r = V.compare(clock(120, 100), clock(120, 100), [60.0, 120.0])
        self.assertFalse(r["drift"])
        self.assertEqual([(c["bar"], c["shift"]) for c in r["cuts"]], [(31.0, 0.0), (61.0, 0.0)])

    def test_a_tempo_change_moves_every_cut(self):
        r = V.compare(clock(120, 100), clock(100, 100), [60.0])
        self.assertTrue(r["drift"])
        self.assertEqual((r["cuts"][0]["bar"], r["cuts"][0]["now"], r["cuts"][0]["shift"]), (31.0, 72.0, 12.0))
        self.assertEqual(r["length"], [200.0, 240.0])

    def test_bars_added_at_the_end_drift_by_length_alone(self):
        r = V.compare(clock(120, 100), clock(120, 108), [60.0])
        self.assertTrue(r["drift"])                              # the cut's bar has not moved, the song grew
        self.assertEqual((r["cuts"][0]["shift"], r["bars"]), (0.0, [100.0, 108.0]))

    def test_a_meter_change_moves_the_bar(self):
        r = V.compare(clock(120, 100, per=4.0), clock(120, 100, per=3.0), [60.0])
        self.assertEqual((r["cuts"][0]["bar"], r["cuts"][0]["now"]), (31.0, 45.0))
        self.assertTrue(r["drift"])

    def test_a_scene_placed_on_bars_moves_with_the_song(self):
        """The engine starts a bar-placed scene where its bar now is: in step however the tempo moved."""
        r = V.compare(clock(120, 100), clock(100, 100), [60.0], now_times=[72.0])
        self.assertEqual((r["cuts"][0]["now"], r["cuts"][0]["starts"], r["cuts"][0]["shift"]), (72.0, 72.0, 0.0))
        r = V.compare(clock(120, 100), clock(120, 100), [60.0], now_times=[60.0])
        self.assertFalse(r["drift"])

    def test_small_wobble_is_not_drift(self):
        now = clock(120, 100)
        now["secs"] += 0.4                                       # a longer tail, under a second
        self.assertFalse(V.compare(clock(120, 100), now, [60.0])["drift"])


class Lines(unittest.TestCase):
    def test_a_drift_report_names_the_moved_cut_and_the_bars(self):
        r = {"id": "x-t8", "n": 8, "programme": "09 Nov 12:15", "song_then": "abcd1234", "state": "DRIFT",
             "length": [200.0, 216.0], "bars": [100.0, 108.0], "check": [125.0],
             "warnings": ["scene 2 (x) at 300.0 s starts after the song ends (216.0 s)"],
             "cuts": [{"at": 60.0, "bar": 31.0, "now": 60.0, "starts": 60.0, "shift": 0.0},
                      {"at": 125.0, "bar": 63.5, "now": 141.0, "starts": 125.0, "shift": 16.0, "contrast": [1.8, 0.5]}]}
        out = "\n".join(V.lines(r))
        self.assertIn("DRIFT length 3:20.0 -> 3:36.0 (+16.0 s), bars 100 -> 108", out)
        self.assertIn("cut 2:05.0 (bar 63.5 then): that bar is now at 2:21.0, the scene still starts at 2:05.0 (16.0 s early)", out)
        self.assertIn("engine: scene 2 (x) at 300.0 s starts after the song ends", out)
        self.assertIn("weaker (1.8 -> 0.5)", out)
        self.assertNotIn("cut 1:00.0", out)                      # an unmoved cut is not listed
        self.assertIn("re-timing by ear", out)

    def test_an_unchanged_song_is_one_line(self):
        r = {"id": "x-t1", "n": 1, "programme": "09 Nov 06:46", "song_then": "abcd1234", "state": "in step",
             "same_text": True, "cuts": []}
        self.assertEqual(len(V.lines(r)), 1)


if __name__ == "__main__":
    unittest.main()
