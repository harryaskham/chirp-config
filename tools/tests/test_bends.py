#!/usr/bin/env python3
"""Tab bend curves (bd-954470): a bend-and-release (0 -> 3 -> 0) written as "curve" steps over holds, so the note's
time-averaged pitch is the curve's mean, not its peak; "peak" (the default) and "mean" as controls; ties carry the
curve; a chord follows its widest curve; tab2song chooses per part.

  python3 tools/tests/test_bends.py              (from ~/.config/chirp; the render test needs $CHIRP or the
                                                  climb build /tmp/lt/chirp-main/…/chirp, else it is skipped)
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import warnings

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)
import songsterr as S  # noqa: E402

CHIRP = os.environ.get("CHIRP", "/tmp/lt/chirp-main/cli/chirp/target/release/chirp")
RELEASE = {"points": [{"position": 0, "tone": 0}, {"position": 30, "tone": 75}, {"position": 60, "tone": 0}]}


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(TOOLS, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


B = load("barchroma")


def note(fret, string=0, bend=None, tie=False):
    n = {"string": string, "fret": fret}
    if bend:
        n["bend"] = bend
    if tie:
        n["tie"] = True
    return n


def beat(dur, *notes):
    return {"duration": dur, "notes": list(notes)} if notes else {"duration": dur, "rest": True}


MEASURES = [
    # E2 bend-and-release for 2 beats, then F#2 plain
    [beat([1, 2], note(0, bend=RELEASE)), beat([1, 2], note(2))],
    # a bend up over one beat, released over its tied continuation, then a rest
    [beat([1, 4], note(0, bend={"points": [{"position": 0, "tone": 0}, {"position": 60, "tone": 50}]})),
     beat([1, 4], note(0, tie=True, bend={"points": [{"position": 0, "tone": 50}, {"position": 60, "tone": 0}]})),
     beat([1, 2])],
    # a chord: the low string bends and releases, the upper does not
    [beat([1, 1], note(0, 0, bend=RELEASE), note(0, 1))],
]


def dump(obj, path):
    with open(path, "w") as f:
        json.dump(obj, f)


def mean_bend(line):
    """The time-averaged bend (semitones above the written pitch) of a line's first note and its holds."""
    segs = B.bar_segments(line)[0]
    base = segs[0][0] - (float(line.split()[0][5:]) if line.startswith("bend=") and line.split()[0][5:] else 0)
    n = sum(d for _, d in segs if True)
    return sum((p - base) * d for p, d in segs) / n, max(p - base for p, _ in segs)


class Bends(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        self.dir = tempfile.mkdtemp(prefix="bends-")
        self.addCleanup(shutil.rmtree, self.dir, True)
        self.cache = os.path.join(self.dir, "cache")
        os.makedirs(self.cache)
        dump({"tracks": [{"name": "gtr"}]}, f"{self.cache}/songsterr-meta.json")
        dump({"name": "gtr", "tuning": [40, 45, 50, 55, 59, 64],
              "measures": [{"signature": [4, 4], "voices": [{"beats": m}]} for m in MEASURES],
              "automations": {"tempo": [{"measure": 0, "bpm": 120}]}}, f"{self.cache}/songsterr-0.json")

    def lines(self, mode, step=0.125):
        return S.score(self.cache, 0, mode, step)[2]

    def test_peak_is_the_default_and_unchanged(self):
        self.assertEqual(self.lines("peak"), S.score(self.cache, 0)[2])
        self.assertEqual(self.lines("peak")[0], "bend=3 E2/2b bend= F#2/2b")

    def test_mean_holds_the_time_average(self):
        self.assertEqual(self.lines("mean")[0], "bend=1.5 E2/2b bend= F#2/2b")

    def test_curve_steps_through_the_bend_and_release(self):
        line = self.lines("curve")[0]
        first = line[:line.index("bend= F#2")]
        self.assertTrue(first.startswith("bend=0.19 E2/0.125b bend=0.56 _/0.125b"), line)
        self.assertTrue(line.endswith("bend= F#2/2b"), "the release ends at 0 before the next note")
        avg, peak = mean_bend(first)
        self.assertAlmostEqual(avg, 1.5, delta=0.05)
        self.assertLessEqual(peak, 3.0)
        total = sum(float(t.split("/")[1].rstrip("b")) for t in line.split() if "/" in t)
        self.assertAlmostEqual(total, 4.0, places=6, msg="the bar keeps its length")
        # bend_step: coarser steps, same mean
        coarse = self.lines("curve", 0.5)[0]
        self.assertLess(coarse.count("_/"), first.count("_/"))
        self.assertAlmostEqual(mean_bend(coarse[:coarse.index("bend= F#2")])[0], 1.5, delta=0.1)

    def test_a_tie_carries_the_curve(self):
        line = self.lines("curve")[1]
        vals = [float(t[5:] or 0) for t in line.split() if t.startswith("bend=")]
        top = vals.index(max(vals))
        self.assertTrue(0 < top < len(vals) - 1, f"rises then falls: {line}")
        self.assertAlmostEqual(max(vals), 2.0, delta=0.15)
        self.assertTrue(line.endswith("R/2b bend="), line)

    def test_a_chord_follows_its_widest_curve(self):
        line = self.lines("curve")[2]
        self.assertTrue(line.startswith("bend=0.09 E2,A2/0.125b"), line)

    def test_tab2song_chooses_per_part(self):
        T2S = load("tab2song")
        mp = {"cache": self.cache, "offset": 0.0, "bends": "curve", "parts": [
            {"name": "curve", "track": 0, "patch": "x", "bars": [[1, 3]]},
            {"name": "peak", "track": 0, "patch": "x", "bars": [[1, 3]], "bends": "peak"}]}
        song = T2S.build(mp)
        by = {t["name"]: t["score"] for t in song["tracks"]}
        self.assertIn("bend=0.19 E2/0.125b", by["curve"])
        self.assertIn("bend=3 E2/2b", by["peak"])

    @unittest.skipUnless(os.access(CHIRP, os.X_OK), "no chirp build ($CHIRP)")
    def test_the_render_follows_the_curve(self):
        sys.path.insert(0, TOOLS)
        import likeness as L

        def mean_semis(line):
            song = {"tempo": 60, "patches": {"p": {"synth": {"layers": ["sine"], "amp": "1ms 0 1 5ms"}}},
                    "tracks": [{"name": "t", "patch": "p", "score": "gate=1 " + line}]}
            path, wav = os.path.join(self.dir, "s.yaml"), os.path.join(self.dir, "s.wav")
            dump(song, path)
            subprocess.run([CHIRP, "render", "-f", path, "-o", wav], capture_output=True, check=True)
            x = L.load(wav).mean(1)[int(0.02 * 48000):int(1.98 * 48000)]
            return np.sum((x[:-1] <= 0) & (x[1:] > 0)) / 1.96   # crossings/s of a sine = its mean frequency

        ref = mean_semis("A3/2b")
        # tempo 60: the bar's 2-beat bend-and-release note is 2 s
        first = self.lines("curve")[0]
        first = first[:first.index("bend= F#2")].replace("E2", "A3") + " bend="
        got = {m: 12 * np.log2(mean_semis(ln) / ref) for m, ln in
               (("curve", first), ("peak", "bend=3 A3/2b bend="), ("mean", "bend=1.5 A3/2b bend="))}
        self.assertAlmostEqual(got["curve"], 1.5, delta=0.25, msg=str(got))   # the curve's mean, a quarter tone
        self.assertAlmostEqual(got["peak"], 3.0, delta=0.25, msg=str(got))
        self.assertAlmostEqual(got["mean"], 1.5, delta=0.25, msg=str(got))


if __name__ == "__main__":
    unittest.main(verbosity=2)
