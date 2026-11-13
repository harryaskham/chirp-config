#!/usr/bin/env python3
"""tools/cabbench.py: a song's rigs with another cabinet stage and no eq after the amp (chirper-zero's).

Hermetic: a stand-in engine that answers `patch show --resolved --json` with a rig of the djent family's shape and
logs every render; a base.yaml in the generator's form.

  python3 tools/tests/test_cabbench.py      (from ~/.config/chirp; a second)
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
import cabbench as B  # noqa: E402

ENGINE = r'''#!/usr/bin/env python3
import json, os, sys
a = sys.argv[1:]
here = os.path.dirname(os.path.abspath(__file__))
if a[:2] == ["patch", "show"]:
    fx = [{"type": "sympathetic"}, {"type": "compressor"}, {"type": "amp", "model": "mark"},
          {"type": "ir", "file": "some/cab"}, {"type": "eq", "bands": ["peak cutoff=5000 gain=-10dB"]}, {"type": "gate"}]
    if a[2] == "odd":
        fx = fx[:2] + fx[3:]
    print(json.dumps({"data": {"patch": {"about": "a rig", "extends": "m8", "fx": fx}}}))
    sys.exit(0)
with open(os.path.join(here, "calls.log"), "a") as f:
    f.write(json.dumps(a) + "\n")
if "fail-wall" in a[a.index("-f") + 1] and "wl" in a:
    sys.stderr.write("chirp: no such riff\n")
    sys.exit(3)
open(a[a.index("-o") + 1], "wb").write(b"RIFF")
'''
BASE = '''tempo: 126
patches: {"mine": {"extends": "pad"}}
tracks:
  - {"name": "gl", "patch": "rig-l fx.0.mix=0 fx.4.bands.3.gain=0dB fx.2.tight=220", "fx": ["eq peaks"], "pan": -1}
  - {"name": "gr", "patch": "rig-r", "pan": 1}
  - {"name": "gr2", "patch": "rig-r fx.4.bands.6.gain=0dB", "pan": 0.8}
  - {"name": "wl", "patch": "rig-w", "pan": -1}
  - {"name": "bass", "patch": "ct-bass fx.4.bands.0.gain=1dB", "fx": ["eq low"]}
'''


class Cabbench(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="cabbench-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self.engine = os.path.join(self.root, "fake-chirp")
        with open(self.engine, "w") as f:
            f.write(ENGINE)
        os.chmod(self.engine, os.stat(self.engine).st_mode | stat.S_IXUSR)
        self.w = os.path.join(self.root, "w")
        os.makedirs(self.w)
        with open(os.path.join(self.w, "base.yaml"), "w") as f:
            f.write(BASE)
        self.rigs = ["--rigs", "chug=gl,gr,gr2:42-48", "wall=wl:113-119"]

    def run_tool(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = B.main([self.w, *argv, "--pin", self.engine])
        return code, out.getvalue()

    def song(self, name):
        with open(os.path.join(self.w, name + ".yaml")) as f:
            lines = f.read().split("\n")
        tracks = {t["name"]: t for t in (json.loads(ln[4:]) for ln in lines if ln.startswith("  - {"))}
        patches = json.loads(next(ln for ln in lines if ln.startswith("patches:"))[len("patches:"):])
        return tracks, patches

    def calls(self):
        with open(os.path.join(self.root, "calls.log")) as f:
            return [json.loads(ln) for ln in f]

    def test_the_cabinet_is_replaced_the_eq_goes_and_the_other_overrides_stay(self):
        code, text = self.run_tool("eng=cab:4x12-modern:0.3:0.15:0,1", *self.rigs)
        self.assertEqual((code, text), (0, "done eng\n"))
        tracks, patches = self.song("eng")
        self.assertEqual(tracks["gl"]["patch"], "cb-rig-l fx.0.mix=0 fx.2.tight=220")     # fx.4.* went with the eq
        self.assertNotIn("fx", tracks["gl"])                                               # ... and so did the track's eq
        self.assertEqual(tracks["gr2"]["patch"], "cb-rig-r")
        self.assertEqual(tracks["bass"]["patch"], "ct-bass fx.4.bands.0.gain=1dB")         # not a rig's track: as it was
        self.assertEqual(tracks["bass"]["fx"], ["eq low"])
        self.assertEqual(patches["mine"], {"extends": "pad"})
        left, right = patches["cb-rig-l"]["fx"], patches["cb-rig-r"]["fx"]
        self.assertEqual([e["type"] for e in left], ["sympathetic", "compressor", "amp", "cab", "gate"])
        self.assertEqual(left[3], {"type": "cab", "model": "4x12-modern", "mic": 0.3, "distance": 0.15})   # cone 0: no key
        self.assertEqual(right[3]["cone"], 1)                                              # gr and gr2 are right tracks
        self.assertEqual(patches["cb-rig-l"]["about"], "cabbench eng")

    def test_amp_files_eq_and_json_specs(self):
        with open(os.path.join(self.root, "stage.json"), "w") as f:
            json.dump([{"type": "cab", "model": "2x12"}, {"type": "eq", "bands": ["lp cutoff=9000"]}], f)
        code, text = self.run_tool("amp", "files", "e1=eq:hp cutoff=70 q=0.9|lp cutoff=5600 q=0.7",
                                   "two=json:" + os.path.join(self.root, "stage.json"), *self.rigs)
        self.assertEqual(text.split(), ["done", "amp", "done", "files", "done", "e1", "done", "two"])
        self.assertEqual(self.song("amp")[1]["cb-rig-l"]["fx"][3], {"type": "gain", "gain": "0dB"})
        self.assertEqual(self.song("files")[1]["cb-rig-l"]["fx"][3], {"type": "ir", "file": "some/cab"})
        self.assertEqual(self.song("e1")[1]["cb-rig-l"]["fx"][3], {"type": "eq", "bands": ["hp cutoff=70 q=0.9", "lp cutoff=5600 q=0.7"]})
        two = [e["type"] for e in self.song("two")[1]["cb-rig-l"]["fx"]]
        self.assertEqual(two, ["sympathetic", "compressor", "amp", "cab", "eq", "gate"])
        with self.assertRaises(SystemExit) as e:
            self.run_tool("x=tube:screamer", *self.rigs)
        self.assertIn("unknown spec", str(e.exception))

    def test_each_rig_is_rendered_alone_on_its_own_bars_raw(self):
        self.run_tool("amp", *self.rigs)
        calls = self.calls()
        self.assertEqual(len(calls), 2)
        chug = next(c for c in calls if c[c.index("-o") + 1].endswith("amp-chug.wav"))
        self.assertEqual(chug[chug.index("--from") + 1:chug.index("--from") + 4], ["42", "--to", "48"])
        self.assertEqual([chug[i + 1] for i, x in enumerate(chug) if x == "--solo"], ["gl", "gr", "gr2"])
        self.assertEqual(chug[chug.index("--set") + 1], "loudness=null")
        self.assertEqual(chug[chug.index("--seed") + 1], "0")
        self.assertTrue(os.path.exists(os.path.join(self.w, "amp-wall.wav")))

    def test_a_failed_render_is_said_and_the_rest_go_on(self):
        code, text = self.run_tool("fail-wall=amp", *self.rigs)
        self.assertEqual(code, 0)
        self.assertIn("fail-wall wall FAILED chirp: no such riff", text)
        self.assertIn("done fail-wall", text)
        self.assertTrue(os.path.exists(os.path.join(self.w, "fail-wall-chug.wav")))

    def test_a_patch_of_another_shape_is_refused_and_bad_arguments_are_said(self):
        with open(os.path.join(self.w, "base.yaml"), "w") as f:
            f.write(BASE.replace('"rig-l fx.0.mix=0', '"odd fx.0.mix=0'))
        with self.assertRaises(SystemExit) as e:
            self.run_tool("amp", *self.rigs)
        self.assertIn("odd is not amp, cabinet, eq at effects 2, 3, 4", str(e.exception))
        with self.assertRaises(SystemExit) as e:
            self.run_tool("amp", "--rigs", "chug=gl:42")
        self.assertIn("--rigs RIG=TRACK,TRACK:FROM-TO", str(e.exception))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(B.main([self.w]), 2)
        self.assertIn("cabbench.py W NAME[=SPEC]", out.getvalue())

    def test_the_default_rigs_are_common_times(self):
        self.assertEqual(B.RIGS, {"chug": (("gl", "gr"), 42, 48), "bite": (("sl", "sr"), 80, 86), "wall": (("wl", "wr"), 113, 119)})


if __name__ == "__main__":
    unittest.main()
