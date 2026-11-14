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
PARTIALS = {"deep": {1: 0.2}, "teeth": {h: 0.05 for h in range(8, 13)}, "thin": {1: 0.05}}
if any(t.get("patch") == "broken" for t in song["tracks"]):
    sys.exit("unknown patch `broken`")
for t in song["tracks"]:
    gain = 1.0
    for fx in t.get("fx") or []:
        if isinstance(fx, str) and fx.startswith("gain gain="):
            gain *= 10 ** (float(fx[len("gain gain="):-2]) / 20)
    for n in t.get("notes") or []:
        i, k = int((n["at"] - start) * beat * 48000), int(n["len"] * beat * 48000)
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
            self.assertEqual(S.main(["only", "three", "args"]), 2)
        self.assertIn("swapbench.py SONG TRACK FROM-TO PATCH", usage.getvalue())


if __name__ == "__main__":
    unittest.main()
