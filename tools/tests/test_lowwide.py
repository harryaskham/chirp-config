#!/usr/bin/env python3
"""tools/lowwide.py: who carries the low end, the wide guitars or the centred bass (chirper-zero's, Common Time v32).

Hermetic: noise in stereo, the same on both sides (a bass), different on each (double-tracked guitars), or flipped.

  python3 tools/tests/test_lowwide.py      (from ~/.config/chirp; a second; needs scipy, as the tool does)
"""
import contextlib
import io
import os
import shutil
import sys
import tempfile
import unittest
import wave

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import lowwide as W  # noqa: E402

SR = 8000


def noise(seed, seconds=8.0, amp=0.1):
    return np.random.default_rng(seed).standard_normal(int(seconds * SR)) * amp


def save(path, left, right=None):
    x = np.stack([left] if right is None else [left, right], 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(x.shape[1])
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


class Lowwide(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="lowwide-test-")
        self.addCleanup(shutil.rmtree, self.root, True)

    def path(self, name):
        return os.path.join(self.root, name)

    def run_tool(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = W.main(list(argv))
        return code, out.getvalue()

    def test_a_bass_is_all_mid_and_two_guitars_are_as_much_side_as_mid(self):
        a, b = noise(1), noise(2)
        bass, _ = W.measure(np.stack([a, a], 1).astype(np.float32), SR)[0], None
        self.assertLess(bass[0], -60.0)
        self.assertAlmostEqual(bass[1], 1.0, delta=0.01)
        for sm, corr in W.measure(np.stack([a, b], 1).astype(np.float32), SR):
            self.assertAlmostEqual(sm, 0.0, delta=1.5)
            self.assertAlmostEqual(corr, 0.0, delta=0.15)
        flipped = W.measure(np.stack([a, -a], 1).astype(np.float32), SR)[0]
        self.assertGreater(flipped[0], 60.0)
        self.assertAlmostEqual(flipped[1], -1.0, delta=0.01)

    def test_a_bass_under_two_guitars_reads_between(self):
        """A centred part at the guitars' own level: the mid holds the bass and half the guitars, the side the other half:
        a third as much side as mid, -4.8 dB."""
        a, b, c = noise(1), noise(2), noise(3)
        mixed = W.measure(np.stack([a + c, b + c], 1).astype(np.float32), SR)
        self.assertAlmostEqual(mixed[0][0], -4.8, delta=1.5)
        self.assertAlmostEqual(mixed[0][1], 0.5, delta=0.15)

    def test_only_the_loud_frames_count(self):
        """Four seconds wide and loud, then four seconds centred and 20 dB down: the reading is the loud frame's."""
        a, b, c = noise(1, 4.0), noise(2, 4.0), noise(3, 4.0, amp=0.01)
        x = np.stack([np.concatenate([a, c]), np.concatenate([b, c])], 1).astype(np.float32)
        self.assertAlmostEqual(W.measure(x, SR)[0][0], 0.0, delta=2.0)

    def test_the_table_a_passage_and_the_median_of_the_others(self):
        a, b, c = noise(1), noise(2), noise(3)
        save(self.path("recA.wav"), a + c, b + c)
        save(self.path("recB.wav"), a, b)
        save(self.path("ours.wav"), np.concatenate([c, a]), np.concatenate([c, b]))   # centred for 8 s, then wide
        code, text = self.run_tool("recA=" + self.path("recA.wav"), "recB=" + self.path("recB.wav"),
                                   "OURS-wide=" + self.path("ours.wav") + ":8:8", "ours-mono=" + self.path("ours.wav") + ":0:8")
        self.assertEqual(code, 0)
        lines = text.splitlines()
        self.assertEqual(lines[0], "%-34s" % "side - mid dB (corr)" + "".join("%16s" % ("%d-%d Hz" % b) for b in W.B))
        self.assertEqual([ln[:34].strip() for ln in lines[1:]], ["recA", "recB", "OURS-wide", "ours-mono", "MEDIAN of the others"])
        first = [float(ln[34:43]) for ln in lines[1:]]
        self.assertAlmostEqual(first[2], 0.0, delta=1.5)                   # the passage from 8 s is the wide half
        self.assertLess(first[3], -60.0)                                   # ... and the first 8 s the centred one
        self.assertAlmostEqual(first[4], (first[0] + first[1]) / 2, delta=0.06)   # ours are left out of the median
        _, one = self.run_tool("recA=" + self.path("recA.wav"), "ours=" + self.path("ours.wav"))
        self.assertNotIn("MEDIAN", one)                                    # one record has no median

    def test_a_mono_file_has_no_sides_and_no_arguments_is_the_help(self):
        save(self.path("mono.wav"), noise(1))
        with self.assertRaises(SystemExit) as e:
            self.run_tool("m=" + self.path("mono.wav"))
        self.assertIn("is not stereo", str(e.exception))
        code, text = self.run_tool()
        self.assertEqual(code, 2)
        self.assertIn("lowwide.py NAME=FILE[:START:DUR]", text)


if __name__ == "__main__":
    unittest.main()
