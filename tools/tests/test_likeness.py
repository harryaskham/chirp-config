#!/usr/bin/env python3
"""likeness.sectioned decodes the reference once per call (bd-167ed8) and scores exactly as before.

  python3 tools/tests/test_likeness.py                     (from ~/.config/chirp)
  LIKENESS=tools/_likeness_new.py LIKENESS_OLD=… python3 tools/tests/test_likeness.py   (a candidate vs a baseline)
"""
import hashlib
import importlib.util
import os
import shutil
import tempfile
import unittest
import warnings
import wave

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


L = module(os.environ.get("LIKENESS", os.path.join(TOOLS, "likeness.py")), "likeness_under_test")
OLD = os.environ.get("LIKENESS_OLD")


def write(path, x):
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


def music(seconds, seed, f0=110.0):
    """A deterministic stereo 'song': a pulse of chords in sections, a little noise, panned layers."""
    rng = np.random.default_rng(seed)
    t = np.arange(int(seconds * SR)) / SR
    x = np.zeros((len(t), 2), np.float32)
    for k, f in enumerate((f0, f0 * 1.25, f0 * 1.5)):
        env = (np.sin(2 * np.pi * (1.5 + 0.5 * k) * t) > 0).astype(np.float32)
        tone = 0.15 * np.sin(2 * np.pi * f * (1 + 0.1 * (t > seconds / 2)) * t) * env
        x[:, 0] += tone * (1 - 0.3 * k)
        x[:, 1] += tone * (0.4 + 0.3 * k)
    x += rng.normal(0, 0.01, x.shape).astype(np.float32)
    return x


class Sectioned(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        self.dir = tempfile.mkdtemp(prefix="likeness-")
        self.addCleanup(shutil.rmtree, self.dir, True)
        self.ref, self.cand = os.path.join(self.dir, "ref.wav"), os.path.join(self.dir, "cand.wav")
        write(self.ref, music(40, 1))
        write(self.cand, music(40, 2, 116.0))
        self.bounds = [0.0, 7.5, 16.0, 29.25, 40.0]

    def test_the_reference_is_decoded_once_and_never_written(self):
        loads, seen = {}, []
        real = L.load

        def counting(path):
            loads[path] = loads.get(path, 0) + 1
            x = real(path)
            if path == self.ref:
                seen.append((x, hashlib.sha256(x.tobytes()).hexdigest()))
            return x

        L.load = counting
        try:
            L.sectioned(self.ref, self.cand, self.bounds)
        finally:
            L.load = real
        self.assertEqual(loads[self.ref], 1, loads)
        self.assertEqual(loads[self.cand], 1, loads)
        x, h = seen[0]
        self.assertEqual(hashlib.sha256(x.tobytes()).hexdigest(), h, "the shared reference array was modified")

    def test_a_section_shorter_than_the_rhythm_window_scores_itself_100(self):
        r = L.sectioned(self.ref, self.ref, [0.0, 36.2, 40.0])   # a 3.8 s last section (Archangel's ending)
        self.assertEqual(r["sections"][-1]["rhythm"], 100.0, r["sections"][-1])
        self.assertGreater(r["total"], 99.9)

    def test_standalone_compare_still_crops(self):
        r = L.compare(self.ref, self.cand, ref_start=7.5, ref_end=16.0)
        self.assertAlmostEqual(r["dur_ref"], 8.5, delta=0.1)

    def test_raw_scores_are_not_rebuilt_from_display_fields(self):
        r = L.sectioned(self.ref, self.cand, self.bounds)
        # bd-fd060e: total_raw comes from compare()'s unrounded terms, not its 1-decimal display fields
        for sec, (a, b) in zip(r["sections"], zip(self.bounds, self.bounds[1:])):
            c = L.compare(self.ref, self.cand, ref_start=a, ref_end=b)
            self.assertNotEqual(c["raw"]["total"], round(c["raw"]["total"], 1), "raw terms are unrounded")
            self.assertAlmostEqual(c["raw"]["total"], c["total"], delta=0.05 + 1e-9)
        w = np.diff(self.bounds)
        self.assertAlmostEqual(r["total_raw"], float(np.dot([s["total_raw"] for s in r["sections"]], w) / w.sum()), places=9)
        self.assertLessEqual(abs(r["total"] - r["total_raw"]), 0.06, "the legacy total differs by rounding only")
        self.assertIn("legacy", r["convention"]["total"])

    def test_describe_keeps_sections_inside_the_audio(self):
        # bd-9e4a85: an automatic boundary at or past the end gave a negative last span and NaN (invalid JSON)
        import json
        real = L.sections
        try:
            L.sections = lambda F: [0.0, 5.0, 5.0, 1e6, 2.5]   # zero, duplicate, past the end, unsorted
            d = L.describe(self.ref)
        finally:
            L.sections = real
        spans = [(x["start"], x["end"]) for x in d["sections"]]
        self.assertEqual(spans[0][0], 0.0)
        self.assertTrue(all(b > a for a, b in spans), spans)
        self.assertEqual([a for a, _ in spans], [0.0, 2.5, 5.0])
        self.assertEqual(spans[-1][1], round(d["duration"], 1))
        json.loads(json.dumps(d), parse_constant=lambda c: self.fail(f"non-finite {c} in describe's JSON"))
        self.assertIsNone(L._finite({"a": [float("nan"), 1.0]})["a"][0])

    @unittest.skipUnless(OLD, "set LIKENESS_OLD to the previous likeness.py to compare scores")
    def test_describe_is_unchanged_for_ordinary_audio(self):
        self.assertEqual(L.describe(self.ref), module(OLD, "likeness_old_d").describe(self.ref))

    @unittest.skipUnless(OLD, "set LIKENESS_OLD to the previous likeness.py to compare scores")
    def test_every_score_field_is_unchanged(self):
        old = module(OLD, "likeness_old")
        added = {"raw", "total_raw", "convention"}   # bd-fd060e: new fields only; every legacy one is identical
        legacy = lambda d: {k: ([{x: y for x, y in s.items() if x not in added} for s in v] if k == "sections" else v)  # noqa: E731
                            for k, v in d.items() if k not in added}
        self.assertEqual(legacy(L.sectioned(self.ref, self.cand, self.bounds)), legacy(old.sectioned(self.ref, self.cand, self.bounds)))
        self.assertEqual(legacy(L.compare(self.ref, self.cand)), legacy(old.compare(self.ref, self.cand)))
        self.assertEqual(legacy(L.compare(self.ref, self.cand, ref_start=7.5, ref_end=16.0)),
                         legacy(old.compare(self.ref, self.cand, ref_start=7.5, ref_end=16.0)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
