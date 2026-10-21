#!/usr/bin/env python3
"""tmpclean: a .tmpclean-keep marker keeps a directory's renders like stems (chirper-zero lost comparison renders
to the 6 h sweep); unmarked renders still go at --age.

  python3 tools/tests/test_tmpclean.py      (from ~/.config/chirp; instant)
"""
import os
import sys
import tempfile
import time
import unittest
from unittest import mock

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import tmpclean as T  # noqa: E402


class Keep(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="tmpclean-test-")
        self.files = {}
        for name, hours, marker in (("plain/a.wav", 8, False), ("kept/jobs/b.wav", 8, True), ("kept/jobs/c.wav", 80, True)):
            p = os.path.join(self.root, name)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "wb") as f:
                f.write(b"\0" * 1000)
            t = time.time() - hours * 3600
            os.utime(p, (t, t))
            self.files[name] = p
        open(os.path.join(self.root, "kept", T.KEEP), "w").close()
        real = T.candidates
        self.only_mine = lambda roots: [f for f in real(roots) if f[0].startswith(self.root + "/")]

    def tearDown(self):
        import shutil
        shutil.rmtree(self.root, ignore_errors=True)

    def test_marker_classifies_its_subtree_like_stems(self):
        flags = {os.path.relpath(f[0], self.root): f[3] for f in self.only_mine([self.root])}
        self.assertEqual(flags, {"plain/a.wav": False, "kept/jobs/b.wav": True, "kept/jobs/c.wav": True})

    def test_age_sweep_spares_marked_renders_until_the_stems_age(self):
        with mock.patch.object(T, "candidates", self.only_mine):
            T.run([self.root], age=6, stems_age=72, cap=1000, min_free=0, min_age=30, dry=False)
        self.assertFalse(os.path.exists(self.files["plain/a.wav"]), "an unmarked 8 h render goes")
        self.assertTrue(os.path.exists(self.files["kept/jobs/b.wav"]), "a marked 8 h render stays")
        self.assertFalse(os.path.exists(self.files["kept/jobs/c.wav"]), "a marked render past 72 h goes")


if __name__ == "__main__":
    unittest.main()
