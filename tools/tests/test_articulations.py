#!/usr/bin/env python3
"""Opt-in tab articulation transport (bd-7bf072): a tab's `hp` is the SOURCE of a hammer-on/pull-off, so the next note
on the same string gets `^h` (never the source unless it is also a target); notes on other strings in between do not
break it, a plain bar line does not either, but a rest, a tied target or a repeat/ending boundary does; a target chord is
marked only when all its sounding notes are targets; `tapping` is its own `^tap`, independent of hp; voices are kept;
the default is byte-identical; tab2song takes it per part or map-wide; the CLI matches; unknown names fail.

  python3 tools/tests/test_articulations.py      (from ~/.config/chirp; under a second)
"""
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import warnings
from contextlib import redirect_stderr

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import songsterr as S  # noqa: E402

TUNING = [64, 59, 55, 50, 45, 40]   # strings 0..5 high E .. low E (Songsterr numbering)


def n(string, fret, **kw):
    return {"string": string, "fret": fret, **kw}


def b(*notes, dur=(1, 8), **kw):
    return {"duration": list(dur), "notes": list(notes), **kw} if notes else {"duration": list(dur), "rest": True, **kw}


def bar(*beats, **marks):
    return {"signature": [4, 4], "voices": [{"beats": list(beats)}], **marks}


def toks(line):
    return [t for t in line.split() if "/" in t]


BARS = [
    # 1: hammer 5th fret -> 7th, pull 7th -> 5th on string 5 (low E); an A-string note between; a tapped beat
    bar(b(n(5, 5, hp=True)), b(n(5, 7, hp=True)), b(n(5, 5)), b(n(5, 3, hp=True)), b(n(4, 2)), b(n(5, 5)),
        b(n(0, 12), tapping=True), b(n(0, 15), tapping=True)),
    # 2: a source on the last beat whose target opens bar 3 (a plain bar line)
    bar(b(n(5, 0), dur=(1, 2)), b(n(5, 3), dur=(1, 4)), b(n(5, 5, hp=True), dur=(1, 4))),
    # 3: the target; then a source broken by a rest; then one onto a tie
    bar(b(n(5, 7), dur=(1, 4)), b(n(4, 2, hp=True), dur=(1, 4)), b(dur=(1, 4)), b(n(4, 4), n(3, 2, hp=True), dur=(1, 8)),
        b(n(3, 2, tie=True), dur=(1, 8))),
    # 4: a mixed target chord (string 5 is a target, string 2 is not), then an all-target chord; source at the end
    bar(b(n(5, 2, hp=True), n(4, 2, hp=True), dur=(1, 4)), b(n(5, 4), n(2, 3), dur=(1, 4)),
        b(n(4, 4), dur=(1, 4)), b(n(5, 7, hp=True), dur=(1, 4)), repeat=2),
    # 5: after the repeat close: not a target (written order is not performed order here)
    bar(b(n(5, 9), dur=(1, 1))),
]


class Articulations(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        self.dir = tempfile.mkdtemp(prefix="articulations-")
        self.addCleanup(shutil.rmtree, self.dir, True)
        self.cache = os.path.join(self.dir, "cache")
        os.makedirs(self.cache)
        with open(f"{self.cache}/songsterr-meta.json", "w") as f:
            json.dump({"tracks": [{"name": "gtr"}]}, f)
        with open(f"{self.cache}/songsterr-0.json", "w") as f:
            json.dump({"name": "gtr", "tuning": TUNING, "measures": BARS,
                       "automations": {"tempo": [{"measure": 0, "bpm": 120}]}}, f)

    def score(self, arts=None, voice=0):
        err = io.StringIO()
        with redirect_stderr(err):
            lines = S.score(self.cache, 0, voice=voice, articulations=S.articulations_of(arts))[2]
        return lines, err.getvalue()

    def test_the_default_carries_nothing(self):
        lines, err = self.score()
        self.assertNotIn("^h", " ".join(lines))
        self.assertNotIn("^tap", " ".join(lines))
        self.assertNotIn("articulations", err, "no report without the option")

    def test_hammer_and_pull_mark_their_targets(self):
        t = toks(self.score("hp")[0][0])
        self.assertEqual([x.endswith("^h") for x in t], [False, True, True, False, False, True, False, False])
        # source A2 (5th fret) unmarked, B2 hammered, A2 pulled; G2 is a source whose target comes after an A-string
        # note (another string does not break the edge)

    def test_a_plain_bar_line_carries_but_a_rest_a_tie_and_a_repeat_do_not(self):
        lines, err = self.score("hp")
        self.assertTrue(toks(lines[2])[0].endswith("^h"), "the target opening bar 3")
        self.assertFalse(any(x.endswith("^h") for x in toks(lines[2])[1:]), lines[2])
        self.assertFalse(toks(lines[4])[0].endswith("^h"), "over a repeat close")
        for what in ("1 across a rest", "1 onto a tie", "1 over a repeat boundary"):
            self.assertIn(what, err)

    def test_chords_are_marked_only_when_every_note_is_a_target(self):
        lines, err = self.score("hp")
        t = toks(lines[3])
        self.assertFalse(t[1].endswith("^h"), f"a mixed chord: {t[1]}")
        self.assertTrue(t[2].endswith("^h"), "the D string's own target")
        self.assertIn("1 mixed chords", err)

    def test_tapping_is_its_own_mark(self):
        tap = toks(self.score("tap")[0][0])
        self.assertEqual([x for x in tap if x.endswith("^tap")], tap[-2:])
        self.assertNotIn("^h", " ".join(self.score("tap")[0]))
        self.assertNotIn("^tap", " ".join(self.score("hp")[0]))
        both = self.score("hp,tap")[0]
        self.assertEqual([re.sub(r"\^(h|tap)", "", x) for x in both], self.score()[0], "marks only: notes unchanged")

    def test_tab2song_per_part_and_map_wide_and_the_cli(self):
        spec = importlib.util.spec_from_file_location("tab2song_art", os.path.join(TOOLS, "tab2song.py"))
        T = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(T)
        mp = {"cache": self.cache, "offset": 0.0, "parts": [
            {"name": "plain", "track": 0, "patch": "x", "bars": [[1, 5]]},
            {"name": "legato", "track": 0, "patch": "x", "bars": [[1, 5]], "articulations": ["hp"]}]}
        with redirect_stderr(io.StringIO()):
            by = {t["name"]: t["score"] for t in T.build(mp)["tracks"]}
            wide = T.build(dict(mp, articulations=["hp"], parts=[mp["parts"][0]]))["tracks"][0]["score"]
        self.assertNotIn("^h", by["plain"])
        self.assertIn("^h", by["legato"])
        self.assertEqual(wide, by["legato"])
        r = subprocess.run([sys.executable, os.path.join(TOOLS, "songsterr.py"), "--cached", self.cache, "0",
                            "--articulations", "hp,tap"], capture_output=True, text=True, stdin=subprocess.DEVNULL)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual([ln.split(None, 1)[1] for ln in r.stdout.splitlines()[1:]], self.score("hp,tap")[0])
        with self.assertRaises(ValueError):
            S.articulations_of("hp,legato")
        r = subprocess.run([sys.executable, os.path.join(TOOLS, "songsterr.py"), "--cached", self.cache, "0",
                            "--articulations", "slap"], capture_output=True, text=True, stdin=subprocess.DEVNULL)
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(r.stdout, "")

    def test_a_second_voice_has_its_own_edges(self):
        with open(f"{self.cache}/songsterr-0.json") as f:
            ms = json.load(f)
        ms["measures"][0]["voices"].append({"beats": [b(n(1, 5, hp=True), dur=(1, 2)), b(n(1, 7), dur=(1, 2))]})
        with open(f"{self.cache}/songsterr-0.json", "w") as f:
            json.dump(ms, f)
        self.assertEqual([x.endswith("^h") for x in toks(self.score("hp", voice=1)[0][0])], [False, True])


if __name__ == "__main__":
    unittest.main(verbosity=2)
