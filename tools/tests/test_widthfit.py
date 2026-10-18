#!/usr/bin/env python3
"""widthfit reads width lanes by time and rewrites only the sections it fits (bd-3a56c6): custom knots (Imprint
v10's 32.15/63.85 s ramps) shift the old points[2*i] read and were erased in unselected sections.

  python3 tools/tests/test_widthfit.py                 (from ~/.config/chirp; ~20 s)
  WIDTHFIT_OLD=… python3 tools/tests/test_widthfit.py  (regular grids: identical to a previous widthfit.py)
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
import wave

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(TOOLS)
SR = 48000
CUTS = [0, 10, 20, 30, 40]
ENV = {k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"}   # this host's LAPACK (see the skill)
spec = importlib.util.spec_from_file_location("wf", os.path.join(TOOLS, "widthfit.py"))
WF = importlib.util.module_from_spec(spec)
spec.loader.exec_module(WF)


def stereo(widths, seed):
    """40 s of noise whose side/mid ratio is widths[i] in section i (broadband)."""
    rng = np.random.default_rng(seed)
    out = []
    for w in widths:
        n = (CUTS[1] - CUTS[0]) * SR
        m, s = rng.normal(0, 0.1, n), rng.normal(0, 0.1, n) * w
        out.append(np.stack([m + s, m - s], 1))
    return np.concatenate(out)


def write(path, x):
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


def knots(doc):
    return {k: [(float(str(t)[:-1]), float(v)) for t, v in doc["head"]["master"]["auto"][k]["points"]]
            for k in doc["head"]["master"]["auto"]}


class Widthfit(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        self.dir = tempfile.mkdtemp(prefix="widthfit-")
        self.addCleanup(shutil.rmtree, self.dir, True)
        self.ref, self.render = os.path.join(self.dir, "ref.wav"), os.path.join(self.dir, "render.wav")
        write(self.ref, stereo([0.5, 0.9, 0.3, 0.7], 1))
        write(self.render, stereo([0.8, 0.6, 0.6, 0.4], 2))
        self.secs = os.path.join(self.dir, "sections.txt")
        with open(self.secs, "w") as f:
            f.write(",".join(map(str, CUTS)))
        # a first pass: the regular grid
        self.empty = os.path.join(self.dir, "empty.json")
        with open(self.empty, "w") as f:
            json.dump({"head": {"master": {"fx": []}}}, f)
        self.grid = os.path.join(self.dir, "grid.json")
        self.run_fit(self.empty, self.grid)

    def run_fit(self, src, dst, *args, tool=None, renders=None):
        r = subprocess.run([sys.executable, tool or os.path.join(TOOLS, "widthfit.py"), src, dst, renders or self.render,
                            self.ref, self.secs, *args], capture_output=True, text=True, cwd=ROOT, env=ENV)
        return r

    def custom(self):
        """The regular grid plus an Imprint-style protected ramp inside section 3 (20-30 s) on wb4."""
        with open(self.grid) as f:
            doc = json.load(f)
        pts = doc["head"]["master"]["auto"]["wb4"]["points"]
        v = pts[4][1]   # section 3's value (knots 4, 5: 20.050 and 29.950 s)
        pts[4:6] = [["20.050s", round(v * 0.8, 3)], ["20.15s", v], ["29.85s", v], ["29.950s", round(v * 0.8, 3)]]
        path = os.path.join(self.dir, "custom.json")
        with open(path, "w") as f:
            json.dump(doc, f)
        return path, doc

    def test_lanes_are_read_by_time(self):
        pts = [["0s", 1.0], ["9.950s", 1.0], ["10.050s", 0.5], ["10.15s", 0.7], ["19.85s", 0.7], ["19.950s", 0.5],
               ["20.050s", 1.2]]
        # over the interior 10.05-19.95 s: the 0.5 -> 0.7 ramps at both ends, 0.7 between (the old read: 0.5)
        self.assertAlmostEqual(WF.section_mean(pts, 10, 20), (0.06 + 0.7 * 9.7 + 0.06) / 9.9, places=6)
        self.assertEqual(WF.section_mean(pts, 0, 10), 1.0)

    def test_zero_step_is_an_identity_and_unselected_knots_survive(self):
        path, before = self.custom()
        for mode in ([], ["--joint"]):
            out = os.path.join(self.dir, "out.json")
            r = self.run_fit(path, out, "--only", "1", "--clip", "1,1", "--strength", "0", *mode)
            self.assertEqual(r.returncode, 0, r.stderr)
            with open(out) as f:
                self.assertEqual(knots(json.load(f)), knots(before), f"mode {mode}")

    def test_only_rewrites_only_its_section_and_keeps_shapes(self):
        path, before = self.custom()
        for mode in ([], ["--joint"]):
            out = os.path.join(self.dir, "out.json")
            r = self.run_fit(path, out, "--only", "3", *mode)
            self.assertEqual(r.returncode, 0, r.stderr)
            with open(out) as f:
                after = knots(json.load(f))
            b = knots(before)
            for lane in after:
                outside = lambda pts: [p for p in pts if not 20 <= p[0] < 30]  # noqa: E731
                self.assertEqual(outside(after[lane]), outside(b[lane]), f"{lane} changed outside section 3 ({mode})")
            # the ramp's knots are all still there, scaled together
            inner = [p for p in after["wb4"] if 20 <= p[0] < 30]
            self.assertEqual([p[0] for p in inner], [20.05, 20.15, 29.85, 29.95])
            self.assertAlmostEqual(inner[0][1] / inner[1][1], 0.8, delta=0.01)

    def test_a_varying_section_is_refused_before_writing(self):
        with open(self.grid) as f:
            doc = json.load(f)
        pts = doc["head"]["master"]["auto"]["wb2"]["points"]
        pts.insert(3, ["15s", 3.0])   # a peak in the middle of section 2
        path, out = os.path.join(self.dir, "peak.json"), os.path.join(self.dir, "out.json")
        with open(path, "w") as f:
            json.dump(doc, f)
        r = self.run_fit(path, out, "--only", "2")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("vary within the section", r.stderr)
        self.assertFalse(os.path.exists(out), "nothing written")
        self.assertEqual(self.run_fit(path, out, "--only", "2", "--scale-shapes").returncode, 0)

    def test_multiple_renders_preserve_power_not_waveform_phase(self):
        # Opposite PCM would cancel if the tool averaged waveforms. Its PSD is unchanged.
        neg = os.path.join(self.dir, "negative.wav")
        with wave.open(self.render, "rb") as inp:
            params = inp.getparams()
            pcm = np.frombuffer(inp.readframes(inp.getnframes()), dtype="<i2")
        with wave.open(neg, "wb") as out:
            out.setparams(params)
            out.writeframes((-pcm).astype("<i2").tobytes())
        for mode in ([], ["--joint"]):
            single = os.path.join(self.dir, "single.json")
            self.assertEqual(self.run_fit(self.grid, single, *mode).returncode, 0)
            with open(single) as f:
                expected = knots(json.load(f))
            for renders in (self.render + "," + self.render, self.render + "," + neg):
                with self.subTest(mode=mode, renders=renders):
                    multi = os.path.join(self.dir, "multi.json")
                    r = self.run_fit(self.grid, multi, *mode, renders=renders)
                    self.assertEqual(r.returncode, 0, r.stderr)
                    with open(multi) as f:
                        self.assertEqual(knots(json.load(f)), expected)

    def test_multiple_renders_zero_step_preserves_custom_knots(self):
        path, before = self.custom()
        for mode in ([], ["--joint"]):
            out = os.path.join(self.dir, "multi-zero.json")
            r = self.run_fit(path, out, "--only", "1", "--clip", "1,1", "--strength", "0", *mode,
                             renders=self.render + "," + self.render)
            self.assertEqual(r.returncode, 0, r.stderr)
            with open(out) as f:
                self.assertEqual(knots(json.load(f)), knots(before))

    def test_literal_comma_filename_keeps_single_input_behavior(self):
        comma = os.path.join(self.dir, "literal,render.wav")
        shutil.copyfile(self.render, comma)
        one, two = os.path.join(self.dir, "one.json"), os.path.join(self.dir, "two.json")
        self.assertEqual(self.run_fit(self.grid, one).returncode, 0)
        self.assertEqual(self.run_fit(self.grid, two, renders=comma).returncode, 0)
        with open(one) as a, open(two) as b:
            self.assertEqual(knots(json.load(a)), knots(json.load(b)))

    @unittest.skipUnless(os.environ.get("WIDTHFIT_OLD"), "set WIDTHFIT_OLD to the previous widthfit.py")
    def test_regular_grids_match_the_previous_widthfit(self):
        for args in ([], ["--only", "2,4"], ["--joint"], ["--strength", "0.5", "--clip", "0.5,4"]):
            new, old = os.path.join(self.dir, "new.json"), os.path.join(self.dir, "old.json")
            self.assertEqual(self.run_fit(self.grid, new, *args).returncode, 0)
            self.assertEqual(self.run_fit(self.grid, old, *args, tool=os.environ["WIDTHFIT_OLD"]).returncode, 0)
            with open(new) as a, open(old) as b:
                self.assertEqual(knots(json.load(a)), knots(json.load(b)), args)


if __name__ == "__main__":
    unittest.main(verbosity=2)
