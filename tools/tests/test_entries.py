#!/usr/bin/env python3
"""tools/entries.py: what joins, bar by bar, with a kit's pieces read apart.

Hermetic: a made song and a stand-in engine that only plans (the tool renders nothing).

  python3 tools/tests/test_entries.py      (from ~/.config/chirp; under a second)
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
import entries as E  # noqa: E402

ENGINE = r'''#!/usr/bin/env python3
import json, sys
a = sys.argv[1:]
song = json.load(open(a[a.index("-f") + 1]))
if song.get("broken"):
    sys.exit("does not plan")
print(json.dumps({"data": {"canonical": song}}))
'''

# tempo 120, bars of four beats. The riff plays bars 1-16 without a rest. The cymbal track crashes on bars 1 and 9 (two
# entries: they are eight bars apart) and its china starts at bar 5 and plays every beat to bar 8. A lead enters at
# bar 9, beat 2, and stops at the end of bar 12. A pad holds bars 13-16.
SONG = {"tempo": 120, "tracks": [
    {"name": "riff", "notes": [{"at": float(b), "len": 0.9, "pitch": "F1"} for b in range(64)]},
    {"name": "cym", "notes": [{"at": 0.0, "len": 2, "pitch": "c"}, {"at": 32.0, "len": 2, "pitch": "c"}]
     + [{"at": float(b), "len": 0.5, "pitch": "x"} for b in range(16, 32)]},
    {"name": "group", "tracks": [{"name": "lead", "notes": [{"at": 33.0 + 2 * i, "len": 2, "pitch": "C5"} for i in range(8)]}]},
    {"name": "pad", "notes": [{"at": 48.0, "len": 16, "pitch": "F3,C4"}]},
    {"name": "silent", "notes": []}]}


class Pieces(unittest.TestCase):
    def test_a_length_of_silence(self):
        self.assertEqual(E.quiet_beats("2bars", 120), 8.0)
        self.assertEqual(E.quiet_beats("1bar", 120), 4.0)
        self.assertEqual(E.quiet_beats("6b", 120), 6.0)
        self.assertEqual(E.quiet_beats("4s", 120), 8.0)
        self.assertIsNone(E.quiet_beats("two", 120))

    def test_a_kits_pieces_are_parts_of_their_own(self):
        got = dict(E.parts(SONG))
        self.assertEqual(list(got), ["riff", "cym (c)", "cym (x)", "lead", "pad"])
        self.assertEqual(got["cym (c)"], [(0.0, 2.0), (32.0, 34.0)])
        self.assertEqual(got["lead"], [(33.0, 49.0)])                             # notes end to end are one span

    def test_what_enters_and_leaves_in_order(self):
        already, evs = E.events(SONG, 8.0)
        self.assertEqual(already, [])
        self.assertEqual([(b, ins) for b, ins, _ in evs if ins],
                         [(0.0, ["riff", "cym (c)"]), (16.0, ["cym (x)"]), (32.0, ["cym (c)"]), (33.0, ["lead"]), (48.0, ["pad"])])
        self.assertEqual([(b, outs) for b, _, outs in evs if outs],
                         [(2.0, ["cym (c)"]), (31.0, ["cym (x)"]), (34.0, ["cym (c)"]), (49.0, ["lead"]), (63.0, ["riff"]),
                          (64.0, ["pad"])])
        already, evs = E.events(SONG, 8.0, 20.0, 40.0)                            # one stretch: what was already playing
        self.assertEqual(already, ["riff", "cym (x)"])
        self.assertEqual([(b, ins) for b, ins, _ in evs if ins], [(32.0, ["cym (c)"]), (33.0, ["lead"])])
        crashes = [b for b, ins, _ in E.events(SONG, 40.0)[1] if "cym (c)" in ins]
        self.assertEqual(crashes, [0.0])                                          # 40 beats of quiet: the second crash is no entry
        self.assertEqual(E.where(332.0, 126), ("84.1", "2:38"))


class Song(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="entries-test-")
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
            code = E.main([self.song, *argv, "--pin", self.pin])
        return code, out.getvalue()

    def test_the_list_and_a_stretch_of_it(self):
        code, text = self.run_tool()
        self.assertEqual(code, 0)
        lines = text.splitlines()
        self.assertEqual(lines[0], "song.json: what enters, in order (a part silent for 2bars or more before its note; a kit's "
                                   "pieces apart)")
        self.assertEqual([ln.split(None, 2) for ln in lines[1:]],
                         [["1.1", "0:00", "+ riff, cym (c)"], ["5.1", "0:08", "+ cym (x)"], ["9.1", "0:16", "+ cym (c)"],
                          ["9.2", "0:16", "+ lead"], ["13.1", "0:24", "+ pad"]])
        _, text = self.run_tool("--from", "6", "--to", "11", "--leaves")
        lines = text.splitlines()
        self.assertEqual(lines[0], "song.json, 6 to 11: what enters and leaves, in order (a part silent for 2bars or more before its "
                                   "note; a kit's pieces apart)")
        self.assertEqual(lines[1], "  already playing: riff, cym (x)")
        self.assertEqual([ln.split(None, 2) for ln in lines[2:]],
                         [["8.4", "0:15", "- cym (x)"], ["9.1", "0:16", "+ cym (c)"], ["9.2", "0:16", "+ lead"],
                          ["9.3", "0:17", "- cym (c)"]])
        _, none = self.run_tool("--from", "14", "--to", "16")
        self.assertEqual(none.splitlines()[1:], ["  already playing: riff, pad", "  nothing enters"])

    def test_json_and_what_it_refuses(self):
        d = json.loads(self.run_tool("--quiet", "1bar", "--json")[1])
        self.assertEqual((d["quiet_beats"], d["events"][0]), (4.0, {"beat": 0.0, "bar": "1.1", "at": "0:00", "enters": ["riff", "cym (c)"],
                                                                     "leaves": []}))
        for argv, said in ((("--quiet", "soon"), "--quiet takes a length"), (("--from", "x"), "--from x")):
            with self.assertRaises(SystemExit) as e:
                self.run_tool(*argv)
            self.assertIn(said, str(e.exception))
        for cannot in ([[0, 120], [8, 90]], [{"at": 0, "bpm": 120}, {"at": "8b", "bpm": 90, "meter": "3/4"}]):
            self.write(dict(SONG, tempo=cannot))
            with self.assertRaises(SystemExit) as e:
                self.run_tool()
            self.assertIn("one tempo, or a map in beats", str(e.exception))

    def test_a_tempo_map_is_followed(self):
        """bd-10e881: 120 for 32 beats (16 s), then 60: a beat lasts a second from bar 9 on."""
        gear = [{"at": 0, "bpm": 120, "meter": None, "ramp": False}, {"at": "32b", "bpm": 60, "meter": None, "ramp": False}]
        self.assertEqual(E.where(32.0, gear), ("9.1", "0:16"))
        self.assertEqual(E.where(36.0, gear), ("10.1", "0:20"))                   # one tempo would say 0:18
        self.assertEqual(E.where(36.0, 120), ("10.1", "0:18"))
        one = self.run_tool()[1]
        self.write(dict(SONG, tempo=gear))
        mapped = self.run_tool()[1]
        bars = lambda text: [ln.split()[0] for ln in text.splitlines()[1:]]  # noqa: E731
        self.assertEqual(bars(mapped), bars(one))                                 # the same bars
        self.assertNotEqual(mapped, one)                                          # ... at other times
        # a silence in SECONDS is measured on the map: 3 s is 6 beats before the change and 3 beats after it
        song = {"tempo": gear, "tracks": [{"name": "a", "notes": [{"at": b, "len": 1.0, "pitch": "C3"} for b in (0.0, 6.0, 40.0, 45.0)]}]}
        self.write(song)
        d = json.loads(self.run_tool("--quiet", "3s", "--json")[1])
        self.assertEqual([e["beat"] for e in d["events"] if e["enters"]], [0.0, 40.0, 45.0])     # 5 beats at 120 is 2.5 s: no entry at 6
        self.assertEqual([e["at"] for e in d["events"] if e["enters"]], ["0:00", "0:24", "0:29"])
        self.assertIsNone(d["quiet_beats"])
        d = json.loads(self.run_tool("--quiet", "5b", "--from", "20s", "--json")[1])                # 20 s is beat 36 on the map
        self.assertEqual([e["beat"] for e in d["events"] if e["enters"]], [40.0])
        self.write({"broken": True})
        with self.assertRaises(SystemExit) as e:
            self.run_tool()
        self.assertIn("does not plan", str(e.exception))
        with contextlib.redirect_stdout(io.StringIO()) as usage:
            self.assertEqual(E.main([]), 2)
        self.assertIn("entries.py SONG", usage.getvalue())


if __name__ == "__main__":
    unittest.main()
