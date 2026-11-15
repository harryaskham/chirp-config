#!/usr/bin/env python3
"""tools/swapbench.py: the same notes of a part on other patches, alone through its own routing (swap or layer?).

Hermetic: a made song and a stand-in engine in which a patch IS a set of partials ("deep": the fundamental;
"teeth": partials 8 to 12; "thin": the fundamental 12 dB down and nothing else) and a track's `gain gain=NdB` effect is
honoured, so what a swap loses and whether a layer is there are known.

  python3 tools/tests/test_swapbench.py      (from ~/.config/chirp; a few seconds)
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
import palette  # noqa: E402
import swapbench as S  # noqa: E402

ENGINE = r'''#!/usr/bin/env python3
import json, os, sys, wave
import numpy as np
a = sys.argv[1:]
song = json.load(open(a[a.index("-f") + 1]))
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "calls.log"), "a") as f:
    f.write(json.dumps([[t["name"], t.get("patch"), len(t.get("notes") or []), t.get("fx")] for t in song["tracks"]]) + "\n")
beat = 60.0 / song["tempo"]
start, end = (float(a[a.index(k) + 1].rstrip("b")) for k in ("--from", "--to"))
x = np.zeros(int((end - start) * beat * 48000))
PARTIALS = {"deep": {1: 0.2}, "teeth": {h: 0.05 for h in range(8, 13)}, "thin": {1: 0.05}, "wash": {1: 0.2}}
RINGS = {"wash": 0.5}                      # a patch that plays on past its notes' written ends, as loud, for half a beat
if any(t.get("patch") == "broken" for t in song["tracks"]):
    sys.exit("unknown patch `broken`")
for t in song["tracks"]:
    gain = 1.0
    for fx in t.get("fx") or []:
        if isinstance(fx, str) and fx.startswith("gain gain="):
            gain *= 10 ** (float(fx[len("gain gain="):-2]) / 20)
    for n in t.get("notes") or []:
        i = int((n["at"] - start) * beat * 48000)
        k = min(int((n.get("len", 0.1) + RINGS.get(t["patch"].split()[0], 0)) * beat * 48000), len(x) - i)
        tt = np.arange(k) / 48000
        f0 = 43.65 * (2 if n["pitch"] == "F2" else 1)
        x[i:i + k] += gain * sum(amp * np.sin(2 * np.pi * f0 * h * tt) for h, amp in PARTIALS[t["patch"].split()[0]].items())
with wave.open(a[a.index("-o") + 1], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(48000)
    w.writeframes((np.repeat(np.clip(x, -1, 1)[:, None], 2, 1) * 32767).astype("<i2").tobytes())
'''

SONG = {"tempo": 120, "tracks": [
    {"name": "bass", "patch": "deep", "out": "low", "fx": ["eq bands=[]"],
     "notes": [{"at": 0, "len": 4, "pitch": "F2"}] + [{"at": 8 + 2 * i, "len": 1.9, "pitch": "F1"} for i in range(4)]},
    {"name": "group", "tracks": [{"name": "pad", "patch": "thin", "notes": [{"at": 8, "len": 8, "pitch": "F1"}]}]},
    {"name": "lead", "patch": "teeth", "notes": [{"at": 8, "len": 8, "pitch": "F2"}]}],
    "buses": [{"name": "low"}]}


class Pieces(unittest.TestCase):
    def test_a_candidate_is_a_patch_and_how_much_more_of_it(self):
        self.assertEqual(S.candidate("bass-fuzz fx.0.shape=wavefold@+4"), ("bass-fuzz fx.0.shape=wavefold", 4.0))
        self.assertEqual(S.candidate("pad@-6"), ("pad", -6.0))
        self.assertEqual(S.candidate("modal-bell"), ("modal-bell", 0.0))
        self.assertEqual(S.candidate("odd@name"), ("odd@name", 0.0))             # not a number: the whole of it is the patch

    def test_in_its_place_or_beside_it(self):
        swap = S.with_patch(SONG, "bass", "teeth", 0.0, False)
        self.assertEqual([t["name"] for t in swap["tracks"]], ["bass", "group", "lead"])
        self.assertEqual((swap["tracks"][0]["patch"], swap["tracks"][0]["fx"], swap["tracks"][0]["out"]), ("teeth", ["eq bands=[]"], "low"))
        layer = S.with_patch(SONG, "bass", "teeth", 4.0, True)
        self.assertEqual([t["name"] for t in layer["tracks"]], ["bass", "bass+layer", "group", "lead"])
        self.assertEqual(layer["tracks"][0], SONG["tracks"][0])                   # the part itself as it was
        beside = layer["tracks"][1]
        self.assertEqual((beside["patch"], beside["out"], beside["notes"]), ("teeth", "low", SONG["tracks"][0]["notes"]))
        self.assertEqual(beside["fx"], ["eq bands=[]", "gain gain=4dB"])          # more of it, after its own effects
        nested = S.with_patch(SONG, "pad", "deep", -6.0, True)
        self.assertEqual([t["name"] for t in nested["tracks"][1]["tracks"]], ["pad", "pad+layer"])
        self.assertEqual(SONG["tracks"][0]["patch"], "deep")                      # the song given is not touched

    def test_a_long_patch_keeps_its_gain_in_the_label(self):
        long = "ct-twin fx.1.model=gojira fx.2.model=1x12 fx.2.mic=0.5 fx.2.cone=16"
        self.assertEqual(S.label({"how": "swap", "patch": "teeth", "db": 0.0}, 44), "teeth")
        self.assertEqual(S.label({"how": "layer", "patch": "teeth", "db": 4.0}, 44), "+ teeth@+4")
        a, b = S.label({"how": "swap", "patch": long, "db": 0.0}, 44), S.label({"how": "swap", "patch": long, "db": 2.5}, 44)
        self.assertEqual((len(a), len(b)), (44, 44))
        self.assertTrue(a.endswith("…") and b.endswith("…@+2.5"))
        self.assertTrue(S.label({"how": "layer", "patch": long, "db": -6.0}, 44).startswith("+ ct-twin fx.1.model=gojira"))

    def test_what_a_row_says(self):
        own = [-0.1, -20.0, -30.0, -70.0, -70.0, -70.0, -70.0, -70.0, -70.0]
        swap = {"how": "swap", "bands": [-7.3, -4.0, -9.0, +30.0, 0, 0, 0, 0, 0]}
        self.assertEqual(S.reading(swap, own), "LOSES <60 (-7.3)")               # 60-120 is not a band the part holds
        self.assertEqual(S.reading(dict(swap, bands=[-2.9] + [0.0] * 8), own), "")
        self.assertEqual(S.reading({"how": "layer", "bands": [0.2, -0.4, 0.1, 9.0, 0, 0, 0, 0, 0]}, own), "NOT THERE")   # 9 dB of nothing
        self.assertEqual(S.reading({"how": "layer", "bands": [0.2, -0.4, 0.1, 30.0, 0, 0, 0, 0, 0]}, own), "")
        self.assertTrue(S.empty(-70.0, 9.0) and not S.empty(-70.0, 30.0) and not S.empty(-20.0, 0.0))


class Bench(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="swapbench-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self.pin = os.path.join(self.root, "chirp-fake")
        with open(self.pin, "w") as f:
            f.write(ENGINE)
        os.chmod(self.pin, os.stat(self.pin).st_mode | stat.S_IXUSR)
        self.song = os.path.join(self.root, "song.json")
        with open(self.song, "w") as f:
            json.dump(SONG, f)

    def run_tool(self, *argv, tool=S):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = tool.main([self.song, *argv, "--pin", self.pin])
        return code, out.getvalue()

    def calls(self):
        with open(os.path.join(self.root, "calls.log")) as f:
            return [json.loads(ln) for ln in f]

    def test_a_swap_loses_the_floor_and_a_layer_keeps_it(self):
        code, text = self.run_tool("bass", "3-5", "teeth", "thin", "teeth@-60", "--layer", "--json")
        self.assertEqual(code, 0)
        d = json.loads(text)
        rows = {(r["patch"], r["db"], r["how"]): r for r in d["rows"]}
        self.assertEqual(d["rows"][0]["how"], "as it is")
        self.assertEqual(d["rows"][0]["patch"], "deep")
        self.assertAlmostEqual(d["rows"][0]["bands"][0], 0.0, delta=0.1)          # F1's fundamental: all of it under 60 Hz
        swap, layer = rows[("teeth", 0.0, "swap")], rows[("teeth", 0.0, "layer")]
        self.assertLess(swap["bands"][0], -40)                                    # the teeth have no floor
        self.assertTrue(swap["says"].startswith("LOSES <60 ("))
        self.assertAlmostEqual(layer["bands"][0], 0.0, delta=0.1)                 # layered, the floor is as it was
        self.assertGreater(layer["bands"][3], 30)                                 # ... and 250-500 Hz has something in it
        self.assertEqual(layer["says"], "")
        self.assertAlmostEqual(rows[("thin", 0.0, "swap")]["all"], -12.0, delta=0.2)
        self.assertTrue(rows[("thin", 0.0, "swap")]["says"].startswith("LOSES <60 (-12."))
        self.assertEqual(rows[("teeth", -60.0, "layer")]["says"], "NOT THERE")
        first = self.calls()[0]                                                   # the bench: the part's notes in the window alone
        self.assertEqual(first, [["bass", "deep", 4, ["eq bands=[]"]], ["group", None, 0, None], ["lead", "teeth", 0, None]])
        beside = self.calls()[2]
        self.assertEqual(beside[:2], [["bass", "deep", 4, ["eq bands=[]"]], ["bass+layer", "teeth", 4, ["eq bands=[]"]]])
        self.assertEqual(self.calls()[-1][1], ["bass+layer", "teeth", 4, ["eq bands=[]", "gain gain=-60dB"]])

    def test_the_gain_for_equal_loudness(self):
        d = json.loads(self.run_tool("bass", "3-5", "thin", "thin@+12", "teeth", "--layer", "--json")[1])
        rows = {(r["patch"], r["db"], r["how"]): r for r in d["rows"]}
        self.assertAlmostEqual(rows[("thin", 0.0, "swap")]["match_db"], 12.0, delta=0.2)     # the same sound 12 dB down
        self.assertAlmostEqual(rows[("thin", 12.0, "swap")]["match_db"], 0.0, delta=0.2)     # ... and with it: level
        self.assertNotIn("match_db", rows[("thin", 0.0, "layer")])                            # a layer is not levelled
        self.assertNotIn("match_db", d["rows"][0])
        self.assertIn("match_db", rows[("teeth", 0.0, "swap")])
        _, text = self.run_tool("bass", "3-5", "thin")
        self.assertTrue(text.splitlines()[1].rstrip().endswith("all  = LUFS"))
        self.assertRegex(text.splitlines()[3], r"-12\.\d +@\+1[12]\.\d")                     # all, then the gain to add

    def test_the_table_and_the_palette_door(self):
        code, text = self.run_tool("bass", "3-5", "teeth@+6", "--layer")
        lines = text.splitlines()
        self.assertTrue(lines[0].startswith("song.json bass at 3-5: the same notes on other patches, alone through the track's own"))
        self.assertIn("   as it is", lines[2])
        self.assertTrue(lines[2].lstrip().startswith("deep "))
        self.assertTrue(lines[3].lstrip().startswith("teeth@+6 ") and "LOSES <60" in lines[3])
        self.assertTrue(lines[4].lstrip().startswith("+ teeth@+6 "))
        self.assertIn("·", lines[4])                                              # bands neither patch has anything in
        _, by_palette = self.run_tool("--bench", "bass", "3-5", "teeth@+6", "--layer", tool=palette)
        self.assertEqual(by_palette, text)

    def test_each_patchs_own_shape_and_the_part_alone(self):
        code, text = self.run_tool("bass", "3-5", "teeth", "--layer")
        lines = text.splitlines()
        i = lines.index("  each patch's own shape (each band against ITS OWN total: where its weight sits):")
        own = [ln.split() for ln in lines[i + 1:]]
        self.assertEqual([r[0] for r in own], ["deep", "teeth"])                  # the swaps, not the layers
        self.assertAlmostEqual(float(own[0][1]), 0.0, delta=0.1)                  # deep: all of it under 60 Hz
        self.assertLess(float(own[1][1]), -30)                                    # teeth: nothing there ...
        self.assertGreater(max(float(own[1][4]), float(own[1][5])), -4)           # ... its weight at 250 Hz-1 kHz
        d = json.loads(self.run_tool("bass", "3-5", "teeth", "--json")[1])
        self.assertEqual([len(r["own"]) for r in d["rows"]], [9, 9])
        self.assertEqual(d["rows"][0]["own"], d["rows"][0]["bands"])
        os.remove(os.path.join(self.root, "calls.log"))
        code, alone = self.run_tool("bass", "3-5")                                # no patch: the part as it is, by band
        self.assertEqual(code, 0)
        self.assertEqual(alone.splitlines()[0], "song.json bass at 3-5: the part alone, as it is, through its own effects, bus and master")
        self.assertTrue(alone.splitlines()[2].lstrip().startswith("its own shape"))
        self.assertTrue(alone.splitlines()[2].rstrip().endswith("deep"))
        self.assertEqual(len(self.calls()), 1)                                    # one render
        _, both = self.run_tool("bass,lead", "3-5")                               # two tracks read as one part
        self.assertTrue(both.splitlines()[2].rstrip().endswith("deep + teeth"))
        self.assertEqual([t[2] for t in self.calls()[-1]], [4, 0, 1])             # bass's four notes and the lead's one; the pad out
        with self.assertRaises(SystemExit) as e:
            self.run_tool("bass,lead", "3-5", "teeth")
        self.assertIn("several tracks are read together only with no PATCH", str(e.exception))

    def test_the_parts_rests(self):
        """A part of eighth notes with eighth rests (250 ms at 120): the engine's patches stop dead with the note; `wash`
        plays on as loud for half a beat, so it FILLS THE RESTS."""
        song = {"tempo": 120, "tracks": [
            {"name": "chug", "patch": "deep", "notes": [{"at": i, "len": 0.5, "pitch": "F1"} for i in range(8)]},
            {"name": "kit", "patch": "deep", "notes": [{"at": i, "pitch": "F1"} for i in range(8)]}]}
        bench = S.keybench.bench(song, ["chug"], 0.0, 8.0, 0)
        notes, rests = S.written(bench, ["chug"], 0.0, 120.0)
        self.assertEqual((len(notes), len(rests), notes[1]), (8, 7, (0.5, 0.75)))
        self.assertEqual([round(v, 4) for v in rests[0]], [0.375, 0.5])           # the second half of the rest at 0.25-0.5 s
        self.assertEqual(S.written(S.keybench.bench(song, ["kit"], 0.0, 8.0, 0), ["kit"], 0.0, 120.0), (None, None))
        path = os.path.join(self.root, "chug.json")
        with open(path, "w") as f:
            json.dump(song, f)
        rows = S.table(path, "chug", 0.0, 8.0, [("thin", 0.0), ("wash", 0.0)], True, self.pin, self.root)
        got = {(r["patch"], r["how"]): r["rest_db"] for r in rows}
        self.assertEqual((got[("deep", "as it is")], got[("thin", "swap")], rows[0]["rests"]), (S.REST_FLOOR_DB, S.REST_FLOOR_DB, 7))
        self.assertAlmostEqual(got[("wash", "swap")], 0.0, delta=0.3)             # as loud in its rests as in its notes
        self.assertAlmostEqual(got[("wash", "layer")], -6.0, delta=0.5)           # two in the notes, one in the rests
        lines = S.rest_lines(rows, [S.label(r, 44) for r in rows], 16)
        self.assertIn("the part's rests (7 of 60 ms or more as written)", lines[0])
        self.assertEqual(len(lines), 6)
        self.assertTrue(lines[1].rstrip().endswith("-60.0   as it is"), lines[1])
        self.assertEqual([("FILLS THE RESTS" in ln) for ln in lines[1:]], [False, False, False, True, True])
        self.assertIn("60.0 dB less of a stop than as it is", lines[4])
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            S.main([path, "chug", "0b-8b", "--pin", self.pin])
        self.assertIn("its rests (7 of 60 ms or more as written): -60.0 dB against its notes", out.getvalue())
        code, text = self.run_tool("bass", "3-5", "thin")                         # no rest in the window: nothing is added
        self.assertEqual((code, "rests" in text), (0, False))

    def test_what_it_refuses(self):
        for argv, said in ((("nosuch", "3-5", "teeth"), "no track nosuch"), (("bass", "20-22", "teeth"), "no notes there"),
                           (("bass", "5-3", "teeth"), "FROM-TO"), (("bass", "3-5", "broken"), "swapbench: broken:")):
            with self.assertRaises(SystemExit) as e:
                self.run_tool(*argv)
            self.assertIn(said, str(e.exception))
        with open(self.song, "w") as f:
            json.dump(dict(SONG, tempo=[[0, 120], [8, 90]]), f)
        with self.assertRaises(SystemExit) as e:
            self.run_tool("bass", "3-5", "teeth")
        self.assertIn("tempo changes", str(e.exception))
        with contextlib.redirect_stdout(io.StringIO()) as usage:
            self.assertEqual(S.main(["only", "two"]), 2)
        self.assertIn("swapbench.py SONG TRACK FROM-TO PATCH", usage.getvalue())


if __name__ == "__main__":
    unittest.main()
