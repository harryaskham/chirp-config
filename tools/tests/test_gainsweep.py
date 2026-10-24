#!/usr/bin/env python3
"""tools/gainsweep.py: gain forms shift in dB (strings, linear numbers, {value, mod} lanes); the sweep reports deltas;
follow keeps only winners that still gain and extends them while they do (a fake scorer: no rendering).

  python3 tools/tests/test_gainsweep.py      (from ~/.config/chirp; instant)
"""
import math
import os
import shutil
import sys
import tempfile
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import gainsweep as G  # noqa: E402

SONG = {"tempo": 100, "tracks": [
    {"name": "lead", "gain": "-3dB", "score": "C4/1b"},
    {"name": "hats", "gain": 0.5, "score": "C4/1b"},
    {"name": "floor", "gain": {"value": "-50dB", "mod": [{"src": "auto.follow", "amount": 1}]}, "score": "C4/1b"},
    {"name": "bass", "score": "C2/1b"},
    {"name": "muted", "gain": "-inf", "score": "C4/1b"},
]}


def fake(target):
    """Score = 60 - sum over tracks of |dB - target| / 4 (the best mix sits at TARGET per track)."""
    def fn(path):
        import songfmt
        s = songfmt.load(path)
        err = sum(abs(G.gain_db(t.get("gain")) - target[t["name"]]) / 4 for t in s["tracks"] if t["name"] in target)
        return {"mean": 60 - err}
    return fn


class GainSweep(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="gainsweep-test-")
        self.path = os.path.join(self.d, "song.yaml")
        import songfmt
        open(self.path, "w").write(songfmt.dump_yaml(SONG))

    def tearDown(self):
        shutil.rmtree(self.d, ignore_errors=True)

    def test_gain_forms(self):
        self.assertEqual(G.gain_db("-3dB"), -3.0)
        self.assertAlmostEqual(G.gain_db(0.5), -6.02, places=2)        # a bare number is linear
        self.assertAlmostEqual(G.gain_db("50%"), -6.02, places=2)
        self.assertEqual(G.gain_db(None), 0.0)
        self.assertEqual(G.gain_db("-inf"), -math.inf)
        self.assertEqual(G.shifted("-3dB", 4), "+1.0dB")
        self.assertEqual(G.shifted(0.5, 4), "-2.0dB")
        lane = G.shifted({"value": "-50dB", "mod": [1]}, -4)
        self.assertEqual(lane, {"value": "-54.0dB", "mod": [1]})

    def test_groups_skip_silent_and_named(self):
        self.assertEqual([g for g, _ in G.groups_of(SONG, None, set())], ["lead", "hats", "floor", "bass"])
        self.assertEqual(G.groups_of(SONG, "kit:hats+bass,lead", set()), [("kit", ["hats", "bass"]), ("lead", ["lead"])])
        with self.assertRaises(SystemExit):
            G.groups_of(SONG, "nope", set())

    def test_sweep_and_follow(self):
        target = {"lead": -3.0, "hats": 6.0, "bass": -8.0, "floor": -50.0}   # hats want +12, bass -8
        sc = G.Scorer(self.path, "ref", "secs", (0,), score_fn=fake(target))
        groups = G.groups_of(SONG, None, set())
        base, res = G.sweep(SONG, groups, 4.0, sc, jobs=2)
        self.assertGreater(res["hats"]["+"], 0)
        self.assertGreater(res["bass"]["-"], 0)
        self.assertLess(res["lead"]["+"], 0)
        cur, score, kept = G.follow(SONG, groups, res, 4.0, sc, min_gain=0.2, steps=3)
        moves = {k: d for k, d, _ in kept}
        self.assertEqual(moves, {"hats": 12.0, "bass": -8.0})
        self.assertAlmostEqual(score, 60.0, places=1)
        self.assertEqual([f for f in os.listdir(self.d) if f.startswith(".gainsweep-")], [])   # variants cleaned up


if __name__ == "__main__":
    unittest.main()
