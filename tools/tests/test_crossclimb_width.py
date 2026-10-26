#!/usr/bin/env python3
"""tools/crossclimb.py --refit-width: one widthfit --joint pass per side after the EQ refit, scored at the best of
raw/refit/width; the default (no flag) rows and print format are unchanged.

  python3 tools/tests/test_crossclimb_width.py      (from ~/.config/chirp; instant, no renders)
"""
import json
import os
import sys
import tempfile
import unittest
from unittest import mock

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import crossclimb as X  # noqa: E402

CLIMB = {"id": "t", "song": "songs/t.yaml",
         "metric": "python3 tools/likeness.py sections ref/t.wav OUT.wav $(cat tools/t-sections.txt)"}


class Proc:
    def __init__(self, stdout="", rc=0):
        self.stdout, self.stderr, self.returncode = stdout, "", rc


def fake_run(calls, width_rc=0):
    ok = json.dumps({"status": "success", "data": {"duration": 10, "timings": {"cpu_ms": 2000}}})

    def run(cmd, **kw):
        calls.append(cmd)
        if cmd[1:2] == ["plan"]:
            return Proc(json.dumps({"data": {"canonical": {"master": {"fx": []}, "tracks": []}}}))
        if any(str(c).endswith("mastereq.py") for c in cmd):
            return Proc(json.dumps({"eq": {"type": "eq", "bands": []}}))
        if any(str(c).endswith("widthfit.py") for c in cmd):
            if not width_rc:
                open(cmd[3], "w").write("{}")
            return Proc("", width_rc)
        return Proc(ok)
    return run


class Width(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.out = mock.patch.object(X, "OUT", self.tmp.name)
        self.out.start()

    def tearDown(self):
        self.out.stop()
        self.tmp.cleanup()

    def test_default_side_has_no_width(self):
        s = X.side("a", "chirp", None, "", 1, refit=True)
        self.assertNotIn("width", s)
        w = X.side("a", "chirp", None, "", 1, width=True)
        self.assertTrue(w["refit"] and w["width"])

    def test_refit_rows_unchanged_without_width(self):
        calls, scores = [], iter([60.0, 61.0])
        with mock.patch.object(X.subprocess, "run", fake_run(calls)), \
                mock.patch.object(X, "score", lambda c, w: next(scores)):
            r = X.run_one(CLIMB, X.side("a", "chirp", None, "", 1, refit=True), keep=True)
        self.assertEqual(set(r), {"score", "raw", "refit", "rt", "short"})
        self.assertEqual((r["score"], r["raw"], r["refit"]), (61.0, 60.0, 61.0))
        self.assertFalse(any(str(c).endswith("widthfit.py") for cmd in calls for c in cmd))
        self.assertEqual(X.fmt_rf(r), " (raw 60.00, refit 61.00)")

    def test_width_pass_joint_and_best(self):
        calls, scores = [], iter([60.0, 61.0, 62.5])
        with mock.patch.object(X.subprocess, "run", fake_run(calls)), \
                mock.patch.object(X, "score", lambda c, w: next(scores)):
            r = X.run_one(CLIMB, X.side("b", "chirp", None, "", 1, width=True), keep=True)
        wf = [cmd for cmd in calls if any(str(c).endswith("widthfit.py") for c in cmd)]
        self.assertEqual(len(wf), 1)
        self.assertEqual(wf[0][2:], [os.path.join(self.tmp.name, "t-b-refit.json"), os.path.join(self.tmp.name, "t-b-width.json"),
                                     os.path.join(self.tmp.name, "t-b.wav"), "ref/t.wav", "tools/t-sections.txt",
                                     "--joint", "--clip", "0.5,2"])
        self.assertEqual((r["score"], r["width"]), (62.5, 62.5))
        self.assertEqual(X.fmt_rf(r), " (raw 60.00, refit 61.00, width 62.50)")

    def test_width_failure_keeps_best_of_rest(self):
        calls, scores = [], iter([60.0, 61.0])
        with mock.patch.object(X.subprocess, "run", fake_run(calls, width_rc=1)), \
                mock.patch.object(X, "score", lambda c, w: next(scores)):
            r = X.run_one(CLIMB, X.side("b", "chirp", None, "", 1, width=True), keep=True)
        self.assertEqual((r["score"], r["width"]), (61.0, None))
        self.assertIn("width_error", r)
        self.assertEqual(X.fmt_rf(r), " (raw 60.00, refit 61.00, width ERR)")


if __name__ == "__main__":
    unittest.main()
