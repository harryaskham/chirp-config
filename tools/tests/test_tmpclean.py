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

    def make(self, name, hours, size=1000):
        p = os.path.join(self.root, name)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as f:
            f.write(b"\0" * size)
        t = time.time() - hours * 3600
        os.utime(p, (t, t))
        return p

    def test_marked_audio_holds_at_most_half_the_cap(self):
        """19 Nov: marked directories filled the cap (8.8 of 10 GB, one composer's finished rounds) and every unmarked
        render of everyone else went at thirty minutes idle."""
        import shutil
        shutil.rmtree(os.path.join(self.root, "plain"))
        shutil.rmtree(os.path.join(self.root, "kept"))
        live = self.make("live/base.wav", 1)                       # nobody marked it: a round's base render, an hour idle
        old = self.make("round-a/x.wav", 5)                        # marked, a finished round
        new = self.make("round-b/y.wav", 2)                        # marked, the round before this one
        hot = self.make("round-c/z.wav", 0.1)                      # marked, six minutes idle: in use
        for d in ("round-a", "round-b", "round-c"):
            open(os.path.join(self.root, d, T.KEEP), "w").close()
        marks = {os.path.relpath(f[0], self.root): f[4] for f in self.only_mine([self.root])}
        self.assertEqual(marks, {"live/base.wav": False, "round-a/x.wav": True, "round-b/y.wav": True, "round-c/z.wav": True})
        with mock.patch.object(T, "candidates", self.only_mine):
            # the cap holds 3500 of the 4000 bytes; the marked three are 3000, over half of it (1750)
            line = T.run([self.root], age=6, stems_age=72, cap=3500e-9, min_free=0, min_age=30, dry=False)
        self.assertIn("marked 2", line)
        self.assertFalse(os.path.exists(old), "the least recently used marked audio goes first")
        self.assertFalse(os.path.exists(new), "... until the marked audio is within half the cap")
        self.assertTrue(os.path.exists(hot), "audio used in the last --min-age minutes is never deleted, marked or not")
        self.assertTrue(os.path.exists(live), "the unmarked render stays: before, it was the first to go")
        with mock.patch.object(T, "candidates", self.only_mine):   # --keep-share 1: the rule of before 19 Nov
            self.make("round-d/w.wav", 3)
            self.make("round-e/v.wav", 2)
            for d in ("round-d", "round-e"):
                open(os.path.join(self.root, d, T.KEEP), "w").close()
            T.run([self.root], age=6, stems_age=72, cap=3500e-9, min_free=0, min_age=30, dry=False, keep_share=1.0)
        self.assertFalse(os.path.exists(live), "with the old rule the unmarked render is deleted first")
        self.assertTrue(os.path.exists(os.path.join(self.root, "round-d", "w.wav")))


if __name__ == "__main__":
    unittest.main()
