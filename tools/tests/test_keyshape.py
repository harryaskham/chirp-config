#!/usr/bin/env python3
"""tools/keyshape.py: a part's own shape in each key it plays.

Hermetic: a made song and a stand-in engine whose "rig" is fitted to one ground, as the bass bus this tool was
written for was: a low note whose fundamental is over 58 Hz has everything above 150 Hz turned down (a compressor
clamping on a lifted fundamental). So the answer is known: the same notes lose their top on B, and a stretch that
plays other notes as well loses bands for another reason.

  python3 tools/tests/test_keyshape.py      (from ~/.config/chirp; a few seconds)
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
import keyshape as K  # noqa: E402

ENGINE = r'''#!/usr/bin/env python3
import json, sys, wave
import numpy as np
a = sys.argv[1:]
song = json.load(open(a[a.index("-f") + 1]))
if song.get("broken"):
    sys.exit("no")
beat = 60.0 / song["tempo"]
start = float(a[a.index("--from") + 1].rstrip("b"))
end = float(a[a.index("--to") + 1].rstrip("b"))
x = np.zeros(int((end - start) * beat * 48000))
names = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def hz(p):
    n, i = names[p[0]], 1
    while p[i] in "#b":
        n += 1 if p[i] == "#" else -1
        i += 1
    return 440.0 * 2 ** ((n + 12 * (int(p[i:]) + 1) - 69) / 12)
def walk(ts):
    for t in ts:
        for n in t.get("notes", []):
            i = int((n["at"] - start) * beat * 48000)
            k = int(n["len"] * beat * 48000)
            if i < 0 or i + k > len(x) or str(n["pitch"])[0] not in names:
                continue
            tt = np.arange(k) / 48000
            lift = 58.0 * 2 ** (t.get("lane_at", {}).get(str(int(n["at"] // 4)), 0) / 12)
            for p in n["pitch"].split(","):
                f = hz(p)
                for h in range(1, 9):
                    g = 0.25 if (lift < f < 100 and f * h > 150) else 1.0     # the rig: fitted to grounds under the lift
                    x[i:i + k] += g * 0.03 / h * np.sin(2 * np.pi * f * h * tt)
        walk(t.get("tracks", []))
walk(song["tracks"])
with wave.open(a[a.index("-o") + 1], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(48000)
    w.writeframes((np.repeat(np.clip(x, -1, 1)[:, None], 2, 1) * 32767).astype("<i2").tobytes())
'''


def bars(first, last, pitches):
    """Four notes a bar over bars first..last (from 0), cycling through `pitches`."""
    return [{"at": float(b * 4 + i), "len": 0.9, "pitch": pitches[i % len(pitches)]} for b in range(first, last + 1) for i in range(4)]


# home is A1 (55 Hz, bars 1-8 and 21-22). Bars 9-12 are the same figure on B1 (61.7 Hz: over the rig's lift). Bars
# 13-16 are on G1 with two high notes struck over each low one. Bar 17 is one bar on D2. The kit plays throughout.
SONG = {"tempo": 120, "tracks": [
    {"name": "bass", "notes": bars(0, 7, ["A1"]) + bars(8, 11, ["B1"]) + bars(12, 15, ["G1,G5,D6"]) + bars(16, 16, ["D2"])
     + bars(20, 21, ["A1"])},
    {"name": "kit", "tracks": [{"name": "kick", "notes": bars(0, 21, ["k"])}]},
    {"name": "pad", "notes": bars(0, 21, ["A3"])}]}


class Grounds(unittest.TestCase):
    def test_the_lowest_note_of_a_pitch(self):
        self.assertEqual(K.lowest("F1"), 29)
        self.assertEqual(K.lowest("F3,C4,F2"), 41)
        self.assertEqual(K.lowest(41), 41)
        self.assertIsNone(K.lowest("k"))
        self.assertEqual((K.note_name(29), K.note_name(44), K.note_name(36)), ("F1", "Ab2", "C2"))

    def test_runs_of_bars_that_share_their_lowest_note(self):
        got = K.runs(SONG, ["bass"])
        self.assertEqual(got, [(0, 7, 33), (8, 11, 35), (12, 15, 31), (16, 16, 38), (20, 21, 33)])
        self.assertEqual(K.runs(SONG, ["kick"]), [])                              # a kit names no pitch
        self.assertEqual(K.runs(SONG, ["bass", "pad"])[0], (0, 7, 33))            # two tracks are one part: the lowest of both
        with self.assertRaises(KeyError):
            K.runs(SONG, ["nosuch"])

    def test_home_is_the_ground_with_the_most_bars_and_a_passing_bar_is_left_out(self):
        gs = K.grounds(K.runs(SONG, ["bass"]), least=2, most=3)
        self.assertEqual([(g["name"], g["bars"], g["runs"], g["read"]) for g in gs],
                         [("A1", 10, 2, (0, 2)), ("G1", 4, 1, (12, 14)), ("B1", 4, 1, (8, 10))])
        self.assertEqual([g["name"] for g in K.grounds(K.runs(SONG, ["bass"]), least=1)], ["A1", "G1", "B1", "D2"])
        self.assertEqual(K.grounds([]), [])

    def test_bands_under_a_fundamental_are_not_read(self):
        self.assertEqual([K.band_of(f) for f in (43.7, 59.9, 61.7, 119.0, 130.8, 260.0)], [0, 0, 1, 1, 2, 3])
        home = [-10.0, -1.0, -11.0, -23.0, -19.0, -30.0, -27.0, -48.0, -79.0]
        diff = [-6.0, +0.8, -6.5, -7.1, -2.9, -7.5, -3.0, -7.4, -0.8]
        self.assertEqual(K.loses(diff, home, 2), [("120-250", -6.5), ("250-500", -7.1)])     # 1-2k and up: not held at home
        self.assertEqual(K.loses(diff, home, 3), [("250-500", -7.1)])

    def test_what_two_rows_say_together(self):
        a, b = ("120-250", -6.5), ("1-2k", -7.5)
        self.assertEqual(K.verdict([], []), "")
        self.assertEqual(K.verdict([], [a]), "it holds as written; home's own notes would lose 120-250 there (the rig, hidden by "
                                             "the notes the song plays)")
        self.assertEqual(K.verdict([a], [b]), "the notes the song plays there AND the rig: home's own notes keep 120-250 but lose 1-2k")
        self.assertEqual(K.verdict([a], [a, b]), "THE RIG: home's own notes lose it there too")
        self.assertEqual(K.verdict([a, b], [b, a]), "THE RIG: home's own notes lose them there too")
        self.assertEqual(K.verdict([a], []), "the notes: home's own notes, moved there, keep it")
        self.assertTrue(K.verdict([a, b], [b]).startswith("THE RIG at 1-2k (home's own notes lose that there too); the rest"))
        self.assertEqual((K.far_note(7), K.far_note(-8)), ("", ""))
        self.assertTrue(K.far_note(12).startswith(" (12 semitones from home: the harmonics themselves move most of a band"))
        self.assertTrue(K.far_note(-9).startswith(" (9 semitones from home"))


class WholeRun(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="keyshape-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self.engine = os.path.join(self.root, "fake-chirp")
        with open(self.engine, "w") as f:
            f.write(ENGINE)
        os.chmod(self.engine, os.stat(self.engine).st_mode | stat.S_IXUSR)
        self.song = os.path.join(self.root, "song.json")
        self.write(SONG)

    def write(self, doc):
        with open(self.song, "w") as f:
            json.dump(doc, f)

    def run_tool(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = K.main([self.song, *argv, "--pin", self.engine])
        return code, out.getvalue()

    def test_a_rig_fitted_to_one_ground_and_a_stretch_of_other_notes(self):
        code, text = self.run_tool("bass", "--bars", "4", "--json")
        self.assertEqual(code, 0)
        got = json.loads(text)
        self.assertEqual((got["home"], [g["name"] for g in got["grounds"]]), ("A1", ["A1", "G1", "B1"]))
        home, g1, b1 = got["grounds"]
        self.assertAlmostEqual(sum(10 ** (v / 10) for v in home["own"]), 1.0, delta=0.02)      # shares of its own total
        self.assertEqual((b1["semis"], g1["semis"]), (2, -2))
        lost = dict(b1["loses"])
        self.assertEqual(list(lost), ["250-500"])                                 # the same figure, over the rig's lift;
        self.assertLess(lost["250-500"], -6)                                      # the fundamental's own bands are not read
        self.assertEqual([lb for lb, _ in b1["moved_loses"]], ["250-500"])        # home's notes lose it there too
        self.assertEqual(b1["says"], "THE RIG: home's own notes lose it there too")
        self.assertTrue({"60-120", "120-250"} <= {lb for lb, _ in g1["loses"]}, g1["loses"])   # other notes carry the total
        self.assertEqual(g1["moved_loses"], [])
        self.assertEqual(g1["says"], "the notes: home's own notes, moved there, keep it")

    def test_the_control_is_played_where_the_ground_is(self):
        # the rig's lift follows a lane at bars 9-12 (two semitones up there): the song is mended, and the control,
        # played at THAT place, says so too; played at home's place it would still lose
        doc = json.loads(json.dumps(SONG))
        doc["tracks"][0]["lane_at"] = {str(b): 2.5 for b in range(8, 12)}
        self.write(doc)
        b1 = json.loads(self.run_tool("bass", "--bars", "4", "--json")[1])["grounds"][2]
        self.assertEqual((b1["name"], b1["loses"], b1["moved_loses"], b1["says"]), ("B1", [], [], ""))

    def test_a_part_of_two_tracks_where_one_rests(self):
        doc = json.loads(json.dumps(SONG))
        doc["tracks"].append({"name": "bass2", "notes": bars(0, 7, ["A1"])})       # the second take plays the home bars only
        self.write(doc)
        got = json.loads(self.run_tool("bass,bass2", "--bars", "4", "--json")[1])
        self.assertEqual([g["name"] for g in got["grounds"]], ["A1", "G1", "B1"])
        self.assertEqual([lb for lb, _ in got["grounds"][2]["loses"]], ["250-500"])    # B is read from the one that plays it

    def test_the_table_and_what_it_refuses(self):
        code, text = self.run_tool("bass", "--bars", "4")
        lines = text.splitlines()
        self.assertTrue(lines[0].startswith("song.json bass: its own shape in each key it plays"))
        self.assertEqual(lines[2].split()[:3], ["A1", "55.0", "1-5"])
        self.assertTrue(lines[2].endswith("10 bars in 2 runs: HOME"))
        self.assertEqual(lines[4].split()[:3], ["B1", "61.7", "9-13"])
        self.assertTrue(any(ln.strip().startswith("B1 as written") and "LOSES 250-500" in ln for ln in lines))
        self.assertTrue(any(ln.strip().startswith("home +2") for ln in lines))
        self.assertTrue(any(ln.strip() == "the notes: home's own notes, moved there, keep it" for ln in lines))
        _, one = self.run_tool("pad")
        self.assertIn("it plays on A3 only: no other key to read it in", one)
        for argv, said in ((("nosuch",), "has no track nosuch"), (("kick",), "plays no pitched notes"),
                           (("bass", "--bars", "0"), "whole numbers of bars")):
            with self.assertRaises(SystemExit) as e:
                self.run_tool(*argv)
            self.assertIn(said, str(e.exception))
        self.write(dict(SONG, tempo=[[0, 120], [8, 90]]))
        with self.assertRaises(SystemExit) as e:
            self.run_tool("bass")
        self.assertIn("tempo changes", str(e.exception))
        with contextlib.redirect_stdout(io.StringIO()) as usage:
            self.assertEqual(K.main([]), 2)
        self.assertIn("keyshape.py SONG TRACK", usage.getvalue())


if __name__ == "__main__":
    unittest.main()
