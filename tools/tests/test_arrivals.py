#!/usr/bin/env python3
"""tools/arrivals.py: each section's level beside the one before it, and an arrival quieter than its approach.

Hermetic: a stand-in engine whose song is a list of levels, one a bar (tempo 120: a bar is two seconds), played as a
tone; "mastered" it plays every bar at one level, as a limiter would. So every level, step and flag is known.

  python3 tools/tests/test_arrivals.py      (from ~/.config/chirp; a few seconds)
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

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import arrivals as A  # noqa: E402

ENGINE = r'''#!/usr/bin/env python3
import json, os, sys, wave
import numpy as np
a = sys.argv[1:]
song = json.load(open(a[a.index("-f") + 1]))
if "plan" in a:
    print(json.dumps({"data": {"canonical": {"tempo": song["tempo"], "tracks": []}}}))
    sys.exit(0)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "calls.log"), "a") as f:
    f.write(" ".join(a) + "\n")
raw = "loudness=null" in a
bars = song["bars"][: int(a[a.index("--to") + 1]) - 1] if "--to" in a else song["bars"]
t = np.arange(2 * 48000) / 48000
x = np.concatenate([10 ** ((db if raw else -20.0) / 20) * np.sin(2 * np.pi * 1000 * t) for db in bars])
with wave.open(a[a.index("-o") + 1], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(48000)
    w.writeframes((np.repeat(x[:, None], 2, 1) * 32767).astype("<i2").tobytes())
'''

# bars 1-4 quiet, 5-12 a verse, 13-16 a climb that swells (its last two bars 3 dB up), 17-24 the landing 1 dB UNDER the
# verse, 25-28 a break 6 dB down, 29-32 home, 2 dB over the verse
BARS = [-30.0] * 4 + [-20.0] * 8 + [-20.0, -20.0, -17.0, -17.0] + [-21.0] * 8 + [-26.0] * 4 + [-18.0] * 4
MARKS = ["1:quiet", "5!:verse", "13:climb", "17!:landing", "25:break", "29!:home"]


class Pieces(unittest.TestCase):
    def test_a_mark_is_a_position_a_bang_and_a_label(self):
        self.assertEqual(A.mark("17!:landing", 120), {"pos": "17", "at": 32.0, "arrival": True, "label": "landing"})
        self.assertEqual(A.mark("64b", 120), {"pos": "64b", "at": 32.0, "arrival": False, "label": ""})
        self.assertEqual(A.mark("32s!", 120)["arrival"], True)
        self.assertEqual(A.mark("1:a: b", 96)["label"], "a: b")
        self.assertIsNone(A.mark("landing", 120))

    def test_sections_read_levels_edges_and_steps(self):
        sr = 48000
        t = np.arange(4 * sr) / sr
        tone = np.sin(2 * np.pi * 1000 * t)[:, None].repeat(2, 1)
        x = np.concatenate([0.1 * tone, 0.2 * tone, 0.05 * tone])                 # 4 s each: +6 dB, then -12 dB
        marks = [{"pos": "a", "at": 0.0, "arrival": False, "label": "a"}, {"pos": "b", "at": 4.0, "arrival": True, "label": "b"},
                 {"pos": "c", "at": 8.0, "arrival": True, "label": ""}]
        rows = A.sections(x, sr, marks, 12.0, 2.0)
        self.assertEqual([(r["at"], r["to"]) for r in rows], [(0.0, 4.0), (4.0, 8.0), (8.0, 12.0)])
        self.assertIsNone(rows[0]["step"])
        self.assertAlmostEqual(rows[1]["step"], 6.0, delta=0.1)
        self.assertAlmostEqual(rows[1]["vs_before"], 6.0, delta=0.1)
        self.assertAlmostEqual(rows[2]["step"], -12.0, delta=0.1)
        self.assertEqual(A.flagged(rows[1], 0.5), "")
        self.assertTrue(A.flagged(rows[2], 0.5).startswith("QUIETER THAN ITS APPROACH: it opens 12.0 dB under the close before it and"))
        self.assertEqual(len(A.sections(x, sr, marks, 6.0, 2.0)), 2)              # a mark past the end has no section
        self.assertAlmostEqual(A.sections(x, sr, marks, 12.0, 9.0)[1]["opens"], rows[1]["level"])   # an edge longer than it

    def test_only_an_arrival_is_flagged_and_by_either_measure(self):
        r = {"arrival": True, "step": -0.2, "vs_before": -0.7}
        self.assertEqual(A.flagged(r, 0.5), "QUIETER THAN ITS APPROACH: it sits 0.7 dB under the section before it")
        self.assertEqual(A.flagged(dict(r, arrival=False), 0.5), "")
        self.assertEqual(A.flagged(dict(r, vs_before=-0.4), 0.5), "")
        self.assertEqual(A.flagged(dict(r, vs_before=-0.4), 0.2), "QUIETER THAN ITS APPROACH: it opens 0.2 dB under the close before it "
                                                                  "and it sits 0.4 dB under the section before it")
        self.assertEqual(A.flagged({"arrival": True, "step": None, "vs_before": None}, 0.5), "")


class Song(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="arrivals-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self.pin = os.path.join(self.root, "chirp-fake")
        with open(self.pin, "w") as f:
            f.write(ENGINE)
        os.chmod(self.pin, os.stat(self.pin).st_mode | stat.S_IXUSR)
        self.song = os.path.join(self.root, "song.json")
        self.write(120)

    def write(self, tempo):
        with open(self.song, "w") as f:
            json.dump({"tempo": tempo, "bars": BARS}, f)

    def run_tool(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = A.main([self.song, *argv, "--pin", self.pin])
        return code, out.getvalue()

    def calls(self):
        with open(os.path.join(self.root, "calls.log")) as f:
            return f.read().splitlines()

    def test_the_arrival_under_its_approach_is_flagged_and_the_break_is_not(self):
        code, text = self.run_tool(*MARKS, "--edge", "2", "--json")
        self.assertEqual(code, 0)
        d = json.loads(text)
        self.assertEqual(d["what"], "raw")
        rows = {r["label"]: r for r in d["sections"]}
        self.assertAlmostEqual(rows["verse"]["step"], 10.0, delta=0.1)
        self.assertEqual(rows["verse"]["flag"], "")
        self.assertAlmostEqual(rows["climb"]["closes"] - rows["climb"]["opens"], 3.0, delta=0.1)
        self.assertAlmostEqual(rows["landing"]["step"], -4.0, delta=0.1)          # under the climb's last two bars
        self.assertTrue(rows["landing"]["flag"].startswith("QUIETER THAN ITS APPROACH: it opens 4.0 dB under"))
        self.assertAlmostEqual(rows["break"]["step"], -5.0, delta=0.1)
        self.assertEqual(rows["break"]["flag"], "")                               # a break is meant to fall
        self.assertEqual(rows["home"]["flag"], "")
        self.assertEqual(rows["home"]["to"], 64.0)                                # the last section runs to the end
        self.assertEqual(len(self.calls()), 1)                                    # one render
        self.assertIn("--set loudness=null", self.calls()[0])

    def test_the_table_and_what_a_master_does_to_it(self):
        _, text = self.run_tool(*MARKS, "--edge", "2")
        lines = text.splitlines()
        self.assertEqual(lines[0], "song.json (raw; seed 0; edges of 2 bars): each section beside the one before it")
        landing = next(ln for ln in lines if ln.lstrip().startswith("landing!"))
        self.assertIn("0:32", landing)
        self.assertIn("QUIETER THAN ITS APPROACH", landing)
        self.assertTrue(lines[-1].lstrip().startswith("1 of 3 arrival(s) quieter than the approach (by 0.5 dB or more)"))
        _, flat = self.run_tool(*MARKS, "--edge", "2", "--mastered")
        self.assertTrue(flat.startswith("song.json (mastered;"))
        self.assertNotIn("QUIETER", flat)                                         # the limiter flattened the step
        self.assertTrue(flat.splitlines()[-1].lstrip().startswith("3 arrival(s), none quieter"))
        self.assertNotIn("loudness=null", self.calls()[-1])
        _, none = self.run_tool("1:quiet", "5:verse", "17:landing")
        self.assertIn("no mark has a `!`", none.splitlines()[-1])

    def test_a_render_given_a_stop_and_what_it_refuses(self):
        raw = os.path.join(self.root, "raw.wav")
        A.render(self.pin, self.song, raw, False)
        os.remove(os.path.join(self.root, "calls.log"))
        _, text = self.run_tool(*MARKS, "--edge", "2", "--wav", raw)
        self.assertTrue(text.startswith("song.json (a render given;"))
        self.assertIn("QUIETER THAN ITS APPROACH", text)
        self.assertFalse(os.path.exists(os.path.join(self.root, "calls.log")))    # nothing rendered
        _, short = self.run_tool(*MARKS, "--to", "25", "--json")
        self.assertEqual([r["label"] for r in json.loads(short)["sections"]], ["quiet", "verse", "climb", "landing"])
        self.assertIn("--to 25", self.calls()[-1])
        for argv, said in ((("landing",), "a MARK is POS[!][:label]"), (("1", "--edge", "x"), "--edge takes bars")):
            with self.assertRaises(SystemExit) as e:
                self.run_tool(*argv)
            self.assertIn(said, str(e.exception))
        self.write([[0, 120], [8, 90]])
        with self.assertRaises(SystemExit) as e:
            self.run_tool(*MARKS)
        self.assertIn("one tempo and 4/4", str(e.exception))
        with contextlib.redirect_stdout(io.StringIO()) as usage:
            self.assertEqual(A.main(["only"]), 2)
        self.assertIn("arrivals.py SONG MARK", usage.getvalue())


if __name__ == "__main__":
    unittest.main()
