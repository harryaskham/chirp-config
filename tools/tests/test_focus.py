#!/usr/bin/env python3
"""climb.py focus --ids: climb only a chosen set of songs (Harry, 2026-10-22: four vocal climbs), album focus and
--off unchanged.

  python3 tools/tests/test_focus.py      (from ~/.config/chirp; instant; a temp registry, no git)
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Focus(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="focus-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        climbs = [{"id": "a1", "status": "active", "rounds": 3, "meta": {"album": "A"}},
                  {"id": "a2", "status": "paused", "rounds": 2, "paused_by": "focus", "meta": {"album": "A"}},
                  {"id": "v1", "status": "requested", "rounds": 0},
                  {"id": "v2", "status": "paused", "rounds": 1, "paused_by": "focus"},
                  {"id": "x", "status": "paused", "rounds": 5}]                  # paused by hand: never touched
        with open(os.path.join(self.root, "climbs.json"), "w") as f:
            json.dump({"climbs": climbs, "focus": "A"}, f)

    def run_(self, *args):
        r = subprocess.run([sys.executable, os.path.join(TOOLS, "climb.py"), "focus", *args, "--no-git"],
                           capture_output=True, text=True, env={**os.environ, "CLIMB_ROOT": self.root})
        return r, json.load(open(os.path.join(self.root, "climbs.json")))

    def status(self, reg):
        return {c["id"]: (c["status"], c.get("paused_by")) for c in reg["climbs"]}

    def test_ids_focus_pauses_the_rest_and_resumes_the_chosen(self):
        r, reg = self.run_("--ids", "v1,v2")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.status(reg), {"a1": ("paused", "focus"), "a2": ("paused", "focus"), "v1": ("requested", None),
                                            "v2": ("active", None), "x": ("paused", None)})
        self.assertEqual(reg["focus"], "climbs: v1, v2")

    def test_off_resumes_everything_a_focus_paused(self):
        self.run_("--ids", "v1")
        r, reg = self.run_("--off")
        self.assertEqual(self.status(reg), {"a1": ("active", None), "a2": ("active", None), "v1": ("requested", None),
                                            "v2": ("active", None), "x": ("paused", None)})
        self.assertNotIn("focus", reg)

    def test_an_unknown_id_is_refused_and_nothing_changes(self):
        before = json.load(open(os.path.join(self.root, "climbs.json")))
        r, reg = self.run_("--ids", "v1,nope")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("nope", r.stderr + r.stdout)
        self.assertEqual(reg, before)


if __name__ == "__main__":
    unittest.main()
