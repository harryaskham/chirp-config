#!/usr/bin/env python3
"""Drum GM overrides before a beat's pieces merge (bd-a725c6): a clap (GM 39) and a snare (38) struck together
merge into one `s` by default (unchanged); with gm_map {"39": "cp"} they stay `cp,s`. A lone snare is unaffected,
voices, tuplets and meters are kept, tab2song takes it per part or map-wide (remap still applies after), the CLI
matches, and a bad map fails before any output.

  python3 tools/tests/test_gmmap.py              (from ~/.config/chirp; under a second)
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
from contextlib import redirect_stderr

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import songsterr as S  # noqa: E402


def hit(*gm, dur=(1, 8), tuplet=None):
    b = {"duration": list(dur), "notes": [{"fret": g, "string": 0} for g in gm]}
    if tuplet:
        b["tuplet"] = tuplet
    return b


# bar 1 (7/8): clap+snare, snare, clap, kick x4 · bar 2 (4/4): a clap+snare triplet, then quarters
V0 = [[hit(38, 39), hit(38), hit(39), hit(36), hit(36), hit(36), hit(36)],
      [hit(38, 39, tuplet=3), hit(38, tuplet=3), hit(39, tuplet=3), hit(36, dur=(1, 4)), hit(38, 39, dur=(1, 4)),
       hit(36, dur=(1, 4))]]
V1 = [[hit(42) for _ in range(7)], [hit(42, dur=(1, 4)) for _ in range(4)]]   # hats in a second voice
SIGS, BAR = [[7, 8], [4, 4]], [3.5, 4.0]


def beats(line):
    return sum(float(x) for x in re.findall(r"/([0-9]*\.?[0-9]+)b", line))


def toks(line):
    return [t.split("/")[0] for t in line.split() if "/" in t]


class GmMap(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="gmmap-")
        self.addCleanup(shutil.rmtree, self.dir, True)
        self.cache = os.path.join(self.dir, "cache")
        os.makedirs(self.cache)
        with open(f"{self.cache}/songsterr-meta.json", "w") as f:
            json.dump({"tracks": [{"name": "drums"}]}, f)
        ms = [{"signature": s, "voices": [{"beats": a}, {"beats": b}]} for s, a, b in zip(SIGS, V0, V1)]
        with open(f"{self.cache}/songsterr-0.json", "w") as f:
            json.dump({"name": "drums", "measures": ms, "automations": {"tempo": [{"measure": 0, "bpm": 120}]}}, f)

    def test_default_merges_and_override_keeps_the_clap(self):
        legacy = S.score(self.cache, 0)[2]
        self.assertEqual(toks(legacy[0])[:3], ["s", "s", "s"], "39 and 38 are both s by default; together, one s")
        self.assertEqual(legacy, S.score(self.cache, 0, gm_map=None)[2])
        self.assertEqual(legacy, S.score(self.cache, 0, gm_map=S.gm_map_of({}))[2])
        opted = S.score(self.cache, 0, gm_map=S.gm_map_of({"39": "cp"}))[2]
        self.assertEqual(toks(opted[0])[:4], ["cp,s", "s", "cp", "k"])
        self.assertEqual(toks(opted[1])[:3], ["cp,s", "s", "cp"])
        self.assertEqual(toks(opted[1])[4], "cp,s")

    def test_meters_tuplets_and_voices_are_kept(self):
        gm = S.gm_map_of("39=cp")
        for voice in (0, 1):
            for i, line in enumerate(S.score(self.cache, 0, voice=voice, gm_map=gm)[2]):
                self.assertAlmostEqual(beats(line), BAR[i], delta=1e-3, msg=f"voice {voice} bar {i + 1}: {line}")
        self.assertIn("cp,s/0.3333b", S.score(self.cache, 0, gm_map=gm)[2][1])
        self.assertEqual(S.score(self.cache, 0, voice=1, gm_map=gm)[2], S.score(self.cache, 0, voice=1)[2],
                         "a voice without claps is unchanged")

    def test_tab2song_per_part_and_map_wide(self):
        spec = importlib.util.spec_from_file_location("tab2song_gm", os.path.join(TOOLS, "tab2song.py"))
        T = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(T)
        mp = {"cache": self.cache, "offset": 0.0, "parts": [
            {"name": "legacy", "track": 0, "patch": "kit", "bars": [[1, 2]]},
            {"name": "clap", "track": 0, "patch": "kit", "bars": [[1, 2]], "gm_map": {"39": "cp"}},
            {"name": "renamed", "track": 0, "patch": "kit", "bars": [[1, 2]], "gm_map": {"39": "cp"}, "remap": {"cp": "clap"}}]}
        by = {t["name"]: t["score"] for t in T.build(mp)["tracks"]}
        self.assertNotIn("cp", by["legacy"])
        self.assertIn("cp,s", by["clap"])
        self.assertIn("clap", by["renamed"])
        self.assertNotIn("cp", by["renamed"].replace("clap", ""))
        wide = dict(mp, gm_map={"39": "cp"}, parts=[dict(mp["parts"][0])])
        self.assertEqual(T.build(wide)["tracks"][0]["score"], by["clap"], "map-wide applies to every part")

    def test_the_cli_matches(self):
        r = subprocess.run([sys.executable, os.path.join(TOOLS, "songsterr.py"), "--cached", self.cache, "0", "--gm-map", "39=cp"],
                           capture_output=True, text=True, stdin=subprocess.DEVNULL)
        self.assertEqual(r.returncode, 0, r.stderr)
        lines = [ln.split(None, 1)[1] for ln in r.stdout.splitlines()[1:]]
        self.assertEqual(lines, S.score(self.cache, 0, gm_map=S.gm_map_of("39=cp"))[2])

    def test_bad_maps_fail_before_output(self):
        for bad in ({"x": "cp"}, {"200": "cp"}, {"39": "c p"}, {"39": "s/1"}, {"39": ""}, "39"):
            with self.assertRaises(ValueError, msg=bad):
                S.gm_map_of(bad)
        r = subprocess.run([sys.executable, os.path.join(TOOLS, "songsterr.py"), "--cached", self.cache, "0", "--gm-map", "39=C P"],
                           capture_output=True, text=True, stdin=subprocess.DEVNULL)
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(r.stdout, "")
        spec = importlib.util.spec_from_file_location("tab2song_gm2", os.path.join(TOOLS, "tab2song.py"))
        T = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(T)
        with self.assertRaises(SystemExit), redirect_stderr(io.StringIO()):
            T.build({"cache": self.cache, "offset": 0.0,
                     "parts": [{"name": "bad", "track": 0, "patch": "kit", "bars": [[1, 2]], "gm_map": {"39": "C P"}}]})


if __name__ == "__main__":
    unittest.main(verbosity=2)
