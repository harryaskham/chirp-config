#!/usr/bin/env python3
"""songfmt: the flow YAML the tools write <-> a song's JSON source, exactly (chirper-zero's request).

  python3 tools/tests/test_songfmt.py      (from ~/.config/chirp; a few seconds: the round trips run chirp plan)
"""
import json
import os
import shutil
import sys
import tempfile
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)
import chirpbin  # noqa: E402
import songfmt as F  # noqa: E402

HAVE_CHIRP = os.path.exists(chirpbin.resolve("chirp")) and os.path.exists(os.path.join(TOOLS, "tha-source.json"))


class Parse(unittest.TestCase):
    def test_flow_yaml_with_bare_scalars_nested_flow_and_quoted_keys(self):
        doc = F.parse_yaml('\n'.join([
            'about: "a, b"',
            'seed: 0',
            'tempo: 134.766',
            'tail: 0s',
            'live: true',
            'master: {fx: [{type: "filter", cutoff: 120, "q value": .7}, gain], auto: {}}',
            'tracks:',
            '  - {name: "a", gain: -3dB, score: "C4/1b D4/1b"}',
            '  - {"name": "b", "patch": "x"}',
            '']))
        self.assertEqual(list(doc), ["about", "seed", "tempo", "tail", "live", "master", "tracks"])
        self.assertEqual(doc["tail"], "0s")
        self.assertIs(doc["live"], True)
        self.assertEqual(doc["master"], {"fx": [{"type": "filter", "cutoff": 120, "q value": 0.7}, "gain"], "auto": {}})
        self.assertEqual(doc["tracks"], [{"name": "a", "gain": "-3dB", "score": "C4/1b D4/1b"}, {"name": "b", "patch": "x"}])

    def test_block_yaml_anchors_and_duplicates_are_refused(self):
        for text in ("master:\n  fx: []\n", "a: &x 1\n", "a: 1\na: 2\n", "tracks:\n  - name: a\n",
                     "tracks:\n  - {name: a, name: b}\n"):
            with self.assertRaises(F.Unsupported, msg=text):
                F.parse_yaml(text)

    def test_order_follows_like_and_new_keys_go_last(self):
        self.assertEqual(list(F.ordered({"tracks": 1, "new": 2, "master": 3, "tempo": 4}, {"tempo": 0, "master": 0, "tracks": 0})),
                         ["tempo", "master", "tracks", "new"])

    def test_json_style_reproduces_a_file(self):
        d = tempfile.mkdtemp(prefix="songfmt-test-")
        self.addCleanup(shutil.rmtree, d, True)
        for kw, nl in (({"indent": 2, "ensure_ascii": False}, "\n"), ({"separators": (",", ":")}, "")):
            p = os.path.join(d, "x.json")
            with open(p, "w", encoding="utf-8") as f:
                f.write(json.dumps({"a": [1, {"b": "é"}]}, **kw) + nl)
            style, got_nl = F.json_style(p)
            self.assertEqual(json.dumps({"a": [1, {"b": "é"}]}, **style) + got_nl, F.read(p))


@unittest.skipUnless(HAVE_CHIRP, "needs the groove pin and tools/tha-source.json")
class RoundTrip(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="songfmt-rt-")
        self.addCleanup(shutil.rmtree, self.dir, True)
        self.src = os.path.join(TOOLS, "tha-source.json")
        self.song = os.path.join(ROOT, "songs", "tha.yaml")

    def test_a_tool_reordered_yaml_converts_back_to_the_exact_source(self):
        lines = F.read(self.song).rstrip("\n").split("\n")
        master = next(i for i, line in enumerate(lines) if line.startswith("master:"))
        moved = lines[:master] + lines[master + 1:] + [lines[master]]      # what songride leaves behind
        edited = os.path.join(self.dir, "tha.yaml")
        with open(edited, "w", encoding="utf-8") as f:
            f.write("\n".join(moved) + "\n")
        out = os.path.join(self.dir, "tha-source.json")
        self.assertEqual(F.main(["json", edited, "-o", out, "--like", self.src]), 0)
        self.assertEqual(F.read(out), F.read(self.src))

    def test_a_conversion_that_changes_the_song_is_refused_and_writes_nothing(self):
        doc = F.load(self.src)
        doc["tempo"] = doc["tempo"] + 1
        out = os.path.join(self.dir, "bad.json")
        with self.assertRaises(SystemExit):
            F.write_checked(self.src, json.dumps(doc), out, True, ".json")
        self.assertFalse(os.path.exists(out))
        self.assertEqual([f for f in os.listdir(self.dir) if f.startswith(".songfmt-")], [], "no temp file left")


if __name__ == "__main__":
    unittest.main()
