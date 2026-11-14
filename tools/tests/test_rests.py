#!/usr/bin/env python3
"""tools/rests.py: the gaps in a part's notes, and what else sounds in them.

Hermetic: a made song and a stand-in engine that only plans (the tool renders nothing).

  python3 tools/tests/test_rests.py      (from ~/.config/chirp; under a second)
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
import rests as R  # noqa: E402

ENGINE = r'''#!/usr/bin/env python3
import json, sys
a = sys.argv[1:]
song = json.load(open(a[a.index("-f") + 1]))
if song.get("broken"):
    sys.exit("does not plan")
print(json.dumps({"data": {"canonical": song}}))
'''

# tempo 120: a beat is 500 ms, a bar two seconds.
#   wall  sixteenths end to end through bars 1-2: no rest
#   lone  bar 3: a note, a beat's rest, a note, half a beat's rest, a note; then out until bar 9, one last note
#   pad   holds bars 1-4;  kick on every beat of bars 1-3 (0.25 long)
SONG = {"tempo": 120, "tracks": [
    {"name": "wall", "notes": [{"at": i * 0.25, "len": 0.245, "pitch": "F1"} for i in range(32)]},
    {"name": "lone", "notes": [{"at": 8, "len": 0.5, "pitch": "F2"}, {"at": 9.5, "len": 0.5, "pitch": "F2"},
                               {"at": 10.5, "len": 0.5, "pitch": "F2,C3"}, {"at": 10.5, "len": 1.0, "pitch": "A2"},
                               {"at": 32, "len": 1, "pitch": "F2"}]},
    {"name": "group", "tracks": [{"name": "pad", "notes": [{"at": 0, "len": 16, "pitch": "F3"}]}]},
    {"name": "kick", "notes": [{"at": float(b), "len": 0.25, "pitch": "k"} for b in range(12)]},
    {"name": "silent", "notes": []}]}


class Pieces(unittest.TestCase):
    def test_a_length_in_ms_seconds_or_beats(self):
        self.assertEqual(R.span_s("150ms", 120), 0.15)
        self.assertEqual(R.span_s("0.2s", 120), 0.2)
        self.assertEqual(R.span_s("0.5b", 120), 0.25)
        self.assertIsNone(R.span_s("150", 120))

    def test_sounding_merges_a_chord_and_finds_a_nested_track(self):
        self.assertEqual(R.names(SONG), ["wall", "lone", "pad", "kick"])
        self.assertEqual(R.sounding(SONG, "lone"), [(8.0, 8.5), (9.5, 10.0), (10.5, 11.5), (32.0, 33.0)])
        self.assertEqual(R.sounding(SONG, "pad"), [(0.0, 16.0)])

    def test_rests_inside_a_passage_and_at_its_end(self):
        passages, found = R.rests(R.sounding(SONG, "lone"), 0.3)
        self.assertEqual(passages, [(8.0, 11.5), (32.0, 33.0)])
        self.assertEqual(found, [(8.5, 1.0), (10.0, 0.5), (11.5, 20.5), (33.0, None)])
        self.assertEqual(R.rests(R.sounding(SONG, "lone"), 0.75)[1], [(8.5, 1.0), (11.5, 20.5), (33.0, None)])
        passages, found = R.rests(R.sounding(SONG, "wall"), 0.3)
        self.assertEqual((passages, found), ([(0.0, 7.995)], [(7.995, None)]))            # 5 ms between notes is no rest
        passages, found = R.rests(R.sounding(SONG, "lone"), 0.3, 9.0, 12.0)              # one stretch of the song
        self.assertEqual((passages, found), ([(8.0, 11.5)], [(10.0, 0.5), (11.5, 20.5)]))

    def test_what_else_sounds(self):
        spans = {n: R.sounding(SONG, n) for n in R.names(SONG)}
        self.assertEqual(R.others_in(spans, "lone", 8.5, 1.0), ["pad", "kick"])
        self.assertEqual(R.others_in(spans, "lone", 11.5, 2.0), ["pad"])                 # the kick's last hit ended at 11.25
        self.assertEqual(R.others_in(spans, "lone", 33.0, 2.0), [])
        self.assertEqual(R.where(1424.0, 126), ("11:18.1", "357.1"))


class Song(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="rests-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self.pin = os.path.join(self.root, "chirp-fake")
        with open(self.pin, "w") as f:
            f.write(ENGINE)
        os.chmod(self.pin, os.stat(self.pin).st_mode | stat.S_IXUSR)
        self.song = os.path.join(self.root, "song.json")
        self.write(SONG)

    def write(self, doc):
        with open(self.song, "w") as f:
            json.dump(doc, f)

    def run_tool(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = R.main([self.song, *argv, "--pin", self.pin])
        return code, out.getvalue()

    def test_a_part_with_no_rest_is_told_so_and_one_with_rests_gets_its_table(self):
        code, text = self.run_tool("wall", "lone")
        self.assertEqual(code, 0)
        lines = text.splitlines()
        self.assertEqual(lines[0], "song.json wall: plays bars 1-2; 0 rest(s) of 150ms or more between its notes, 1 passage end(s)")
        self.assertTrue(lines[1].lstrip().startswith("NO REST BETWEEN ITS NOTES"))
        i = lines.index("song.json lone: plays bars 3, 9; 2 rest(s) of 150ms or more between its notes, 2 passage end(s)")
        self.assertNotIn("NO REST", "\n".join(lines[i:]))
        rows = [ln.split() for ln in lines[i + 2:i + 6]]
        self.assertEqual(rows[0][:5], ["0:04.2", "3.1", "500", "ms", "(1b)"])
        self.assertEqual(rows[0][5:], ["pad,", "kick"])
        self.assertEqual(rows[1][:5], ["0:05.0", "3.3", "250", "ms", "(0.5b)"])
        self.assertEqual(rows[2][:5], ["0:05.8", "3.4", "out", "5.125", "bars"])
        self.assertIn("(its last note)  NOTHING: it is alone", lines[i + 5])
        self.assertEqual(lines[i + 6].strip(), "longest 500 ms; 0 of 2 with nothing else written under them")

    def test_json_a_stretch_and_the_least_length(self):
        _, text = self.run_tool("lone", "--min", "0.75b", "--tail", "2b", "--json")
        d = json.loads(text)
        self.assertEqual((d["min_s"], d["tail_s"]), (0.375, 1.0))
        t = d["tracks"][0]
        self.assertEqual((t["track"], t["notes"], t["passages"]), ("lone", 5, [[8.0, 11.5], [32.0, 33.0]]))
        self.assertEqual([(r["at_beat"], r["ms"], r["out"]) for r in t["rests"]],
                         [(8.5, 500, False), (11.5, 10250, True), (33.0, None, True)])
        self.assertEqual(t["rests"][1]["with"], ["pad"])
        _, text = self.run_tool("lone", "--from", "5", "--to", "12")
        self.assertIn("song.json lone, 5 to 12: plays bars 9; 0 rest(s)", text)
        _, text = self.run_tool("kick", "--from", "30")
        self.assertIn("song.json kick, 30 to the end: no notes there", text)

    def test_what_it_refuses(self):
        for argv, said in ((("nosuch",), "no track nosuch with notes"), (("silent",), "no track silent with notes"),
                           (("lone", "--min", "150"), "--min and --tail take a length"), (("lone", "--from", "x"), "--from x")):
            with self.assertRaises(SystemExit) as e:
                self.run_tool(*argv)
            self.assertIn(said, str(e.exception))
        self.write(dict(SONG, tempo=[[0, 120], [8, 90]]))
        with self.assertRaises(SystemExit) as e:
            self.run_tool("lone")
        self.assertIn("one tempo", str(e.exception))
        self.write({"broken": True})
        with self.assertRaises(SystemExit) as e:
            self.run_tool("lone")
        self.assertIn("does not plan", str(e.exception))
        with contextlib.redirect_stdout(io.StringIO()) as usage:
            self.assertEqual(R.main(["only"]), 2)
        self.assertIn("rests.py SONG TRACK", usage.getvalue())


if __name__ == "__main__":
    unittest.main()
