#!/usr/bin/env python3
"""tools/gspec.py: third-octave spectra side by side, each against its own 80 Hz-8 kHz total (chirper-zero's).

Hermetic: sines, so every band is known.

  python3 tools/tests/test_gspec.py      (from ~/.config/chirp; a second)
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
import gspec as G  # noqa: E402

SR = 48000


def save(path, chans, width=2):
    """chans: one array a channel, floats in -1..1."""
    x = np.stack(chans, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(x.shape[1])
        w.setsampwidth(width)
        w.setframerate(SR)
        w.writeframes((x * (2 ** (8 * width - 1) - 1)).astype("<i%d" % width).tobytes())


def sine(freq, seconds=1.0, amp=0.5):
    return amp * np.sin(2 * np.pi * freq * np.arange(int(seconds * SR)) / SR)


class Gspec(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="gspec-test-")
        self.addCleanup(shutil.rmtree, self.root, True)

    def path(self, name):
        return os.path.join(self.root, name)

    def run_tool(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = G.main(list(argv))
        return code, out.getvalue()

    def band(self, hz):
        return G.CS.index(hz)

    @staticmethod
    def values(line):
        """A row's numbers: six characters each after the 22-character name (an empty band prints -120.0, which fills its field)."""
        return [float(line[22 + 6 * i:28 + 6 * i]) for i in range(len(G.CS))]

    def test_two_equal_sines_are_half_the_total_each_whatever_the_level(self):
        for name, amp in (("loud.wav", 0.4), ("quiet.wav", 0.004)):
            save(self.path(name), [sine(200, amp=amp) + sine(2000, amp=amp)])
        loud, quiet = G.spec(self.path("loud.wav")), G.spec(self.path("quiet.wav"))
        for hz in (200, 2000):
            self.assertAlmostEqual(loud[self.band(hz)], -3.01, delta=0.05)
            self.assertAlmostEqual(quiet[self.band(hz)], -3.01, delta=0.1)
        self.assertLess(loud[self.band(1000)], -40.0)

    def test_a_part_panned_hard_counts_whole_and_32_bit_files_are_read(self):
        save(self.path("pan.wav"), [sine(200), np.zeros(SR)])              # all of it on the left
        save(self.path("mid.wav"), [sine(200) * 0.7, sine(200) * 0.7], width=4)
        self.assertAlmostEqual(G.spec(self.path("pan.wav"))[self.band(200)], 0.0, delta=0.01)
        self.assertAlmostEqual(G.spec(self.path("mid.wav"))[self.band(200)], 0.0, delta=0.01)

    def test_a_passage_of_a_file_and_the_difference_from_the_first(self):
        save(self.path("rec.wav"), [np.concatenate([sine(200), sine(2000), sine(200)])])    # 2 kHz only in its second second
        save(self.path("ours.wav"), [sine(2000) + sine(500)])
        code, text = self.run_tool("rec=" + self.path("rec.wav") + ":1:1", "ours=" + self.path("ours.wav"), "--diff")
        self.assertEqual(code, 0)
        lines = text.splitlines()
        self.assertEqual(lines[0].split(), ["Hz"] + [str(c) if c < 1000 else "%gk" % (c / 1000) for c in G.CS])
        self.assertTrue(lines[1].startswith("rec  "))
        self.assertTrue(lines[2].startswith("ours -1st  "))
        rec = self.values(lines[1])
        ours = self.values(lines[2])
        self.assertAlmostEqual(rec[self.band(2000)], 0.0, delta=0.1)       # the passage is the 2 kHz second alone
        self.assertLess(rec[self.band(200)], -40.0)
        self.assertAlmostEqual(ours[self.band(2000)], -3.0, delta=0.1)     # ours has half its power there: 3 dB less
        self.assertGreater(ours[self.band(500)], 40.0)
        _, plain = self.run_tool("rec=" + self.path("rec.wav") + ":1:1", "ours=" + self.path("ours.wav"))
        self.assertTrue(plain.splitlines()[2].startswith("ours  "))
        self.assertAlmostEqual(self.values(plain.splitlines()[2])[self.band(2000)], -3.0, delta=0.1)

    def test_no_file_is_the_help(self):
        code, text = self.run_tool("--diff")
        self.assertEqual(code, 2)
        self.assertIn("gspec.py NAME=FILE[:START:DUR]", text)


if __name__ == "__main__":
    unittest.main()
