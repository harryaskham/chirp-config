#!/usr/bin/env python3
"""tools/lanes.py: a song's `auto` lanes and which of their falls are not lines (Common Time v24: a lane's falling
segments take the envelope's curve, default 3; only rises are straight).

Hermetic: the lane reading on plan dicts, and the tool against a stand-in for `chirp plan`.

  python3 tools/tests/test_lanes.py      (from ~/.config/chirp; under a second)
"""
import contextlib
import io
import json
import os
import shutil
import stat
import sys
import tempfile
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import lanes as N  # noqa: E402

SONG = {
    "tempo": 126.0,
    "patches": {"wahwah": {"fx": [{"type": "wah", "pos": {"value": 0, "mod": [{"src": "auto.wah", "amount": 1}]}}]}},
    "buses": {"gtrs": {"fx": [{"type": "eq"}, {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.ride", "amount": 1}]}}],
                       "auto": {"ride": {"points": [["0b", 0], ["1606b", 0], ["1610b", -1], ["1636b", -30]]},
                                "ring": {"curve": 0, "points": [["0b", 0], ["8b", -20], ["16b", 0]]}}}},
    "master": {"fx": [{"type": "tapestop", "stop": {"value": 0, "mod": [{"src": "auto.stop", "amount": 1}]}}],
               "auto": {"stop": {"points": [["0s", 0], ["10s", 1], ["10.01s", 0]]}}},
    "tracks": [{"name": "leadw", "patch": "wahwah fx.0.mix=1", "auto": {"wah": {"points": [["0b", 1], ["2b", 0.25]]}}, "notes": [{}]},
               {"name": "bus", "tracks": [{"name": "inner", "gain": {"value": "0dB", "mod": [{"src": "auto.up", "amount": 1}]},
                                           "auto": {"up": {"points": [["0b", -6], ["4b", 0]]}}}]}],
}


class Read(unittest.TestCase):
    def setUp(self):
        self.rows = {(r["where"], r["name"]): r for r in N.lanes_of(SONG)}

    def test_every_lane_is_found_with_what_it_drives(self):
        self.assertEqual(sorted(self.rows), [("bus gtrs", "ride"), ("bus gtrs", "ring"), ("master", "stop"),
                                             ("track inner", "up"), ("track leadw", "wah")])
        self.assertEqual(self.rows[("bus gtrs", "ride")]["drives"], ["fx.gain.gain"])
        self.assertEqual(self.rows[("master", "stop")]["drives"], ["fx.tapestop.stop"])
        self.assertEqual(self.rows[("track inner", "up")]["drives"], ["gain"])
        self.assertEqual(self.rows[("track leadw", "wah")]["drives"], ["patch wahwah: fx.wah.pos"])   # inside its patch

    def test_falls_are_listed_with_their_place_and_rises_are_only_counted(self):
        ride = self.rows[("bus gtrs", "ride")]
        self.assertEqual((ride["curve"], ride["explicit"], ride["rises"], len(ride["falls"])), (3.0, False, 0, 2))
        last = ride["falls"][1]
        self.assertEqual((last["v0"], last["v1"], last["beats"], last["beat"]), (-1, -30, 26.0, 1610.0))
        self.assertAlmostEqual(last["seconds"], 1610 * 60 / 126.0, delta=0.06)
        up = self.rows[("track inner", "up")]
        self.assertEqual((up["rises"], up["falls"]), (1, []))
        stop = self.rows[("master", "stop")]["falls"][0]                   # a point in seconds
        self.assertAlmostEqual(stop["beat"], 10 * 126 / 60.0)
        self.assertEqual(self.rows[("bus gtrs", "ring")]["curve"], 0.0)

    def test_the_curve_is_the_engines(self):
        self.assertAlmostEqual(N.shape(0.2, 3.0), 0.4748, places=3)        # (1 - e^-0.6) / (1 - e^-3)
        self.assertAlmostEqual(N.shape(0.5, 3.0), 0.8176, places=3)
        self.assertEqual(N.shape(0.37, 0.0), 0.37)                          # curve 0: the line
        self.assertAlmostEqual(N.shape(N.half_point(3.0), 3.0), 0.5, places=6)
        self.assertAlmostEqual(N.half_point(3.0), 0.215, places=3)
        self.assertEqual(N.half_point(0.0), 0.5)

    def test_a_plan_without_a_tempo_is_at_120(self):
        song = dict(SONG)
        del song["tempo"]
        row = [r for r in N.lanes_of(song) if r["name"] == "ride"][0]
        self.assertEqual(row["falls"][1]["seconds"], 805.0)


class Tool(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="lanes-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self.pin = os.path.join(self.root, "chirp-fake")
        with open(self.pin, "w") as f:
            f.write("#!/usr/bin/env python3\nimport json\nprint(json.dumps({'data': {'canonical': %r}}))\n" % (SONG,))
        os.chmod(self.pin, os.stat(self.pin).st_mode | stat.S_IXUSR)
        self.song = os.path.join(self.root, "song.yaml")
        open(self.song, "w").close()

    def run_tool(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            N.main(["--song", self.song, "--pin", self.pin, *argv])
        return out.getvalue()

    def test_the_table_and_the_falls_that_are_not_lines(self):
        text = self.run_tool()
        self.assertIn("song.yaml: 5 auto lanes; 3 have falls that are not lines (4 falls)", text)
        self.assertIn("bus gtrs, ride -> fx.gain.gain: curve 3, half of each fall is done in its first 21%, 82% by its middle", text)
        self.assertIn("12:46.7  bar 403   -1 -> -30  over 26 beats", text)
        self.assertNotIn("bus gtrs, ring", text)                           # a straight lane's falls are not listed ...
        self.assertIn("0 (line)", text)                                    # ... but the lane is, in the table
        self.assertIn("bus gtrs, ring: curve 0, lines", self.run_tool("--all"))            # drives nothing here: said so by "?"
        self.assertIn('"curve": 0', text)

    def test_json(self):
        d = json.loads(self.run_tool("--json"))
        self.assertEqual((d["default_curve"], len(d["lanes"])), (3.0, 5))


if __name__ == "__main__":
    unittest.main()
