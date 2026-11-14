#!/usr/bin/env python3
"""tools/keybench.py: the same bars of a part moved to other grounds, alone through its own rig.

Hermetic: a made song and the stand-in engine of test_pitchbench.py (each note as partials 2 to 6 of its pitch), so
the bench song, the window and the band table are all run and the answer is known.

  python3 tools/tests/test_keybench.py      (from ~/.config/chirp; a second or two)
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
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import keybench as K  # noqa: E402
from test_pitchbench import ENGINE  # noqa: E402

SONG = {"tempo": 120, "length": "64b", "tracks": [
    {"name": "gl", "out": "gtrs", "warp": [{"over": "8b", "to": 0}],
     "notes": [{"at": 0, "len": 2, "pitch": "E2"}] + [{"at": 8 + i, "len": 0.9, "pitch": "A2", "vel": 0.8} for i in range(8)]
     + [{"at": 16, "len": 2, "pitch": "E2"}]},
    {"name": "gr", "out": "gtrs", "notes": [{"at": 8 + i, "len": 0.9, "pitch": "A2,E3"} for i in range(8)], "risset": {"cycle": "8b"}},
    {"name": "drums", "tracks": [{"name": "kick", "notes": [{"at": 8 + i, "len": 0.2, "pitch": "A1"} for i in range(8)]}]},
    {"name": "lead", "score": "A4/4 B4/4", "mute": True}],
    "buses": [{"name": "gtrs"}]}


class Moving(unittest.TestCase):
    def test_a_pitch_moves_and_a_kit_piece_stays(self):
        self.assertEqual(K.moved("F1", 7), "C2")
        self.assertEqual(K.moved("C2", -7), "F1")
        self.assertEqual(K.moved("F#2", 5), "B2")
        self.assertEqual(K.moved("B3", 1), "C4")
        self.assertEqual(K.moved("F1,C2,F2", -1), "E1,B1,E2")
        self.assertEqual(K.moved(54, 2), 56)
        self.assertEqual(K.moved("54", 2), "56")
        self.assertEqual(K.moved("k", 5), "k")
        self.assertEqual(K.moved("rde", -3), "rde")

    def test_the_bench_keeps_the_parts_bars_and_nothing_else(self):
        made = K.bench(SONG, ["gl", "gr"], 8.0, 16.0, -4)
        gl, gr, drums, lead = made["tracks"]
        self.assertEqual([n["pitch"] for n in gl["notes"]], ["F2"] * 8)                  # the E2s before and after are out
        self.assertEqual(gl["notes"][0], {"at": 8, "len": 0.9, "pitch": "F2", "vel": 0.8})
        self.assertEqual(gl["warp"], SONG["tracks"][0]["warp"])                           # its own clock stays
        self.assertEqual([n["pitch"] for n in gr["notes"]], ["F2,C3"] * 8)
        self.assertNotIn("risset", gr)
        self.assertEqual(drums["tracks"][0]["notes"], [])
        self.assertNotIn("score", lead)
        self.assertEqual(made["buses"], SONG["buses"])
        self.assertEqual(SONG["tracks"][0]["notes"][1]["pitch"], "A2")                    # the song given is not touched
        self.assertEqual(K.bench(SONG, ["kick"], 8.0, 16.0, 0)["tracks"][2]["tracks"][0]["notes"][0]["pitch"], "A1")
        for tracks, said in ((["nosuch"], "nosuch"), (["gl"], "gl (no notes there)")):
            with self.assertRaises(KeyError) as e:
                K.bench(SONG, tracks, 40.0, 48.0, 0)
            self.assertEqual(e.exception.args[0], said)


class WholeRun(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="keybench-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self.engine = os.path.join(self.root, "fake-chirp")
        with open(self.engine, "w") as f:
            f.write(ENGINE)
        os.chmod(self.engine, os.stat(self.engine).st_mode | stat.S_IXUSR)
        self.song = os.path.join(self.root, "song.json")
        with open(self.song, "w") as f:
            json.dump(SONG, f)

    def run_tool(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = K.main([self.song, *argv, "--pin", self.engine])
        return code, out.getvalue()

    def test_a_move_shows_in_the_bands_it_leaves_and_enters(self):
        # A2 as the stand-in plays it: partials at 220, 330, 440, 550, 660 Hz. Up an octave: 440 to 1320 Hz.
        code, text = self.run_tool("gl", "3-5", "12", "0", "--json")
        self.assertEqual(code, 0)
        got = json.loads(text)
        self.assertEqual(got["bands"], K.LABELS)
        self.assertEqual([r["shift"] for r in got["rows"]], [0, 12])                      # as written once, and first
        written, up = got["rows"]
        i = {name: n for n, name in enumerate(K.LABELS)}
        self.assertAlmostEqual(sum(10 ** (v / 10) for v in written["bands"]), 1.0, delta=0.02)   # shares of its own total
        self.assertGreater(written["bands"][i["120-250"]], -6)                            # 220 Hz, the strongest
        self.assertLess(written["bands"][i["1-2k"]], -25)                                 # only the notes' edges are up there
        self.assertLess(up["bands"][i["120-250"]], -20)                                   # nothing is left under 440 Hz
        self.assertGreater(up["bands"][i["1-2k"]], 20)                                    # 1100 and 1320 Hz arrive
        self.assertAlmostEqual(up["all"], 0.0, delta=0.3)                                 # the stand-in is as loud on any note

    def test_the_table_and_what_is_kept(self):
        keep = os.path.join(self.root, "kept")
        code, text = self.run_tool("gl,gr", "8b-16b", "-7", "5", "--keep", keep)
        lines = text.splitlines()
        self.assertIn("gl, gr at 8b-16b: the same notes moved, alone", lines[0])
        self.assertEqual(lines[1].split(), ["semitones"] + K.LABELS + ["all"])
        self.assertEqual([ln.split()[0] for ln in lines[2:5]], ["as", "-7", "+5"])
        self.assertEqual(len(lines[3].split()), 11)
        self.assertEqual(sorted(os.listdir(keep)),
                         ["bench+5.json", "bench+5.wav", "bench-7.json", "bench-7.wav", "bench.json", "bench.wav"])
        with open(os.path.join(keep, "bench-7.json")) as f:
            made = json.load(f)
        self.assertEqual({n["pitch"] for n in made["tracks"][1]["notes"]}, {"D2,A2"})

    def test_what_cannot_be_benched_is_said(self):
        for argv, said in ((("nosuch", "3-5", "5"), "has no track nosuch"), (("gl", "11-13", "5"), "has no track gl (no notes there)"),
                           (("gl", "3-5", "up"), "each SHIFT is a whole number of semitones"),
                           (("gl", "5-3", "5"), "5-3: FROM-TO as chirp render takes positions"),
                           (("gl", "soon", "5"), "soon: FROM-TO")):
            with self.assertRaises(SystemExit) as e:
                self.run_tool(*argv)
            self.assertIn(said, str(e.exception))
        code, text = self.run_tool("gl", "3-5")
        self.assertEqual(code, 2)
        self.assertIn("keybench.py SONG TRACK[,TRACK...] FROM-TO SHIFT", text)
        with open(self.song, "w") as f:
            json.dump(dict(SONG, tempo=[[0, 120], [8, 90]]), f)
        with self.assertRaises(SystemExit) as e:
            self.run_tool("gl", "3-5", "5")
        self.assertIn("only fixed-tempo songs", str(e.exception))


if __name__ == "__main__":
    unittest.main()
