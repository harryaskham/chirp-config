#!/usr/bin/env python3
"""sectioneq: --apply writes the fitted stage into a song (chirper-zero's request), --sections counts from 1, and the
default output is unchanged.

  python3 tools/tests/test_sectioneq.py      (from ~/.config/chirp; seconds; SECTIONEQ_OLD=previous sectioneq.py also
                                              checks the default output byte for byte)
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import wave

import numpy as np
from scipy import signal

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import chirpbin  # noqa: E402
import sectioneq as E  # noqa: E402

HAVE_CHIRP = os.path.exists(chirpbin.resolve("chirp"))
BLOCK = {"auto": {f"eq{j}": {"points": [["0s", 1.0]]} for j in range(7)}, "eq": {"type": "eq", "bands": []}}


def wav(path, x):
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as f:
        f.setnchannels(2), f.setsampwidth(2), f.setframerate(48000)
        f.writeframes(np.repeat(pcm[:, None], 2, axis=1).tobytes())


class Merge(unittest.TestCase):
    def test_after_glue_else_before_clip_else_last(self):
        for fx, at in ((["gain", "glue threshold=-16dB", "clip"], 2), (["gain", {"type": "clip"}], 1), (["gain"], 1), ([], 0)):
            ms = {"fx": list(fx)}
            E.merge(ms, json.loads(json.dumps(BLOCK)))
            self.assertEqual(ms["fx"][at], BLOCK["eq"], fx)
            self.assertEqual(sorted(ms["auto"]), sorted(BLOCK["auto"]))

    def test_a_lane_clash_is_refused_and_names_a_free_prefix(self):
        ms = {"fx": [], "auto": {"eq3": {}, "rq0": {}}}
        with self.assertRaises(SystemExit) as e:
            E.merge(ms, json.loads(json.dumps(BLOCK)))
        self.assertIn("--prefix sq", str(e.exception))
        self.assertEqual(ms["fx"], [], "nothing merged")


class Apply(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="sectioneq-test-")
        self.addCleanup(shutil.rmtree, self.dir, True)

    def path(self, name, text):
        p = os.path.join(self.dir, name)
        with open(p, "w") as f:
            f.write(text)
        return p

    @unittest.skipUnless(HAVE_CHIRP, "needs the groove pin")
    def test_flow_yaml_changes_only_its_master_line(self):
        src = self.path("s.yaml", 'tempo: 120\nmaster: {"fx": ["glue threshold=-16dB ratio=2", "clip"]}\ntracks:\n'
                                  '  - {name: "a", patch: "piano", score: "C4/1b"}\n')
        out = os.path.join(self.dir, "o.yaml")
        E.apply_to(src, json.loads(json.dumps(BLOCK)), out)
        a, b = open(src).read().splitlines(), open(out).read().splitlines()
        self.assertEqual([x for x in a if not x.startswith("master:")], [x for x in b if not x.startswith("master:")])
        ms = json.loads(next(x for x in b if x.startswith("master:"))[7:])
        self.assertEqual([f if isinstance(f, str) else f["type"] for f in ms["fx"]], ["glue threshold=-16dB ratio=2", "eq", "clip"])

    @unittest.skipUnless(HAVE_CHIRP, "needs the groove pin")
    def test_a_native_json_song_keeps_its_formatting(self):
        doc = {"tempo": 120, "tracks": [{"name": "a", "patch": "piano", "score": "C4/1b"}]}
        src = self.path("s.json", json.dumps(doc, indent=2) + "\n")
        out = os.path.join(self.dir, "o.json")
        E.apply_to(src, json.loads(json.dumps(BLOCK)), out)
        got = json.load(open(out))
        self.assertEqual(open(out).read(), json.dumps(got, indent=2) + "\n")
        self.assertEqual(got["master"]["fx"], [BLOCK["eq"]])

    def test_a_tab2song_map_gets_head_master(self):
        src = self.path("m.json", json.dumps({"head": {"tempo": 100}, "parts": []}, indent=2) + "\n")
        out = os.path.join(self.dir, "o.json")
        E.apply_to(src, json.loads(json.dumps(BLOCK)), out)
        self.assertEqual(json.load(open(out))["head"]["master"]["fx"], [BLOCK["eq"]])


class Cli(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dir = tempfile.mkdtemp(prefix="sectioneq-cli-")
        rng = np.random.default_rng(1)
        x = rng.normal(size=20 * 48000) * 0.1
        b, a = signal.butter(2, 3000, fs=48000)
        cls.ref, cls.cand = os.path.join(cls.dir, "r.wav"), os.path.join(cls.dir, "c.wav")
        wav(cls.ref, x), wav(cls.cand, signal.lfilter(b, a, x) * 1.3)
        cls.secs = os.path.join(cls.dir, "s.txt")
        with open(cls.secs, "w") as f:
            f.write("0,10,20\n")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.dir, ignore_errors=True)

    def run_(self, tool, *args):
        r = subprocess.run([sys.executable, tool, self.ref, self.cand, self.secs, *args], capture_output=True, text=True,
                           env={k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"})
        return r.stdout, r.stderr

    def test_sections_counts_from_one(self):
        a, _ = self.run_(os.path.join(TOOLS, "sectioneq.py"), "--only", "1")
        b, err = self.run_(os.path.join(TOOLS, "sectioneq.py"), "--sections", "2")
        self.assertEqual(a, b)
        self.assertIn("section 2 (index 1, 10-20 s)", err)

    @unittest.skipUnless(os.environ.get("SECTIONEQ_OLD"), "SECTIONEQ_OLD=previous sectioneq.py")
    def test_default_output_is_unchanged(self):
        for args in ((), ("--only", "1"), ("--only", "0,1", "--scale", "0.5")):
            self.assertEqual(self.run_(os.environ["SECTIONEQ_OLD"], *args)[0], self.run_(os.path.join(TOOLS, "sectioneq.py"), *args)[0])


if __name__ == "__main__":
    unittest.main()
