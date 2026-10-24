#!/usr/bin/env python3
"""Tab capos: Songsterr writes a capoed track's frets relative to the capo (No Surprises' acoustic capo 3 and
Rickenbacker capo 15). songsterr.score(..., capo=True) sounds them at tuning + capo; the default (capo=False) is
byte-identical to before, so existing maps keep their pitches unless they opt in with "capo": true.

  python3 tools/tests/test_capo.py              (from ~/.config/chirp; under a second)
"""
import json
import os
import shutil
import sys
import tempfile
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import songsterr as S  # noqa: E402

TUNING = [64, 59, 55, 50, 45, 40]


def note(string, fret):
    return {"duration": [1, 4], "notes": [{"string": string, "fret": fret}]}


def track(capo):
    # D shape on the top strings: E4+2 = F#4, G3+2 = A3, B3+3 = D4, a rest-free 4/4 bar
    bar = {"signature": [4, 4], "voices": [{"beats": [note(0, 2), note(2, 2), note(1, 3), note(2, 2)]}]}
    t = {"name": "gtr", "tuning": TUNING, "measures": [bar]}
    if capo is not None:
        t["capo"] = capo
    return t


class CapoTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        for i, c in enumerate((3, 15, None)):
            with open(f"{self.dir}/songsterr-{i}.json", "w") as f:
                json.dump(track(c), f)
        with open(f"{self.dir}/songsterr-meta.json", "w") as f:
            json.dump({"tracks": [{}, {}, {}]}, f)

    def tearDown(self):
        shutil.rmtree(self.dir)

    def line(self, i, capo):
        return S.score(self.dir, i, capo=capo)[2][0]

    def test_default_ignores_capo(self):
        self.assertEqual(self.line(0, False), self.line(2, False))
        self.assertIn("F#4", self.line(0, False))

    def test_capo_3_sounds_a_minor_third_up(self):
        got = self.line(0, True)
        self.assertTrue(got.startswith("A4/"), got)
        self.assertIn("C4/", got)
        self.assertIn("F4/", got)
        self.assertNotIn("F#4", got)

    def test_capo_15(self):
        got = self.line(1, True)
        self.assertTrue(got.startswith("A5/"), got)
        self.assertIn("C5/", got)
        self.assertIn("F5/", got)

    def test_no_capo_unchanged_with_option(self):
        self.assertEqual(self.line(2, True), self.line(2, False))


if __name__ == "__main__":
    unittest.main()
