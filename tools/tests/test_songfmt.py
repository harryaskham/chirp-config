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



@unittest.skipUnless(HAVE_CHIRP, "needs the groove pin")
class Notes(unittest.TestCase):
    """songfmt notes: a score-string track as a notes list (chirper-zero's request), proven against chirp's plan."""

    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="songfmt-notes-")
        self.addCleanup(shutil.rmtree, self.dir, True)

    def song(self, score, patch="g", tempo=120):
        p = os.path.join(self.dir, "s.json")
        doc = {"tempo": tempo, "patches": {"g": {"synth": {"layers": [{"wave": "saw"}]}, "play": {"strum": "4ms"}}},
               "tracks": [{"name": "lead", "patch": patch, "gain": "-3dB", "score": score},
                          {"name": "kit", "patch": "tight-kit", "score": "k/1b@100 h/1b@60 s/2b@90"}]}
        with open(p, "w") as f:
            json.dump(doc, f, indent=2)
        return p

    def convert(self, src, track="lead"):
        out = os.path.join(self.dir, "o.json")
        self.assertEqual(F.main(["notes", src, track, "-o", out]), 0)
        return next(t for t in json.load(open(out))["tracks"] if t["name"] == track)

    def test_chords_holds_marks_hz_and_latched_velocity_convert_exactly(self):
        t = self.convert(self.song("C4,E4,G4/1b@100 _/1b | R/1b 440hz/0.5b@64 A4/0.5b B4/1b@90^vow=0.2>0.8^pm | E5/1b^gate=0.5"))
        self.assertNotIn("score", t)
        self.assertEqual(t["gain"], "-3dB")
        n = t["notes"]
        self.assertEqual([(x["at"], x["len"], x["pitch"]) for x in n],
                         [("0.0b", "2.0b", "C4,E4,G4"), ("3.0b", "0.5b", 69), ("3.5b", "0.5b", 69), ("4.0b", "1.0b", 71),
                          ("5.0b", "1.0b", 76)])
        self.assertAlmostEqual(n[0]["vel"], 100 / 127)
        self.assertAlmostEqual(n[2]["vel"], 0.8, places=5)      # no @V: the velocity chirp plays (its default; @V does not latch)
        self.assertEqual((n[3]["expr"], n[3]["expr_end"]), ({"vow": 0.2, "pm": 1.0}, {"vow": 0.8}))
        self.assertEqual(n[4]["gate"], 0.5)

    def test_kit_pieces_convert(self):
        t = self.convert(self.song("C4/1b@90"), "kit")
        self.assertEqual([x["pitch"] for x in t["notes"]], ["k", "h", "s"])

    def test_ratchets_chord_symbols_and_latched_octaves_are_refused(self):
        for score in ("h/1b@80^r=3", "C:maj7/2b@90", "C5/1b@90 D/1b@90"):
            with self.assertRaises(SystemExit, msg=score):
                self.convert(self.song(score))
        self.assertFalse(os.path.exists(os.path.join(self.dir, "o.json")))


if __name__ == "__main__":
    unittest.main()
