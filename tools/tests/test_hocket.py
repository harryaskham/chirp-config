#!/usr/bin/env python3
"""tools/hocket.py: do two hard-panned parts take turns (chirper-zero's, Odd Sympathy v3).

Hermetic: tone bursts on the left and the right of a made file.

  python3 tools/tests/test_hocket.py      (from ~/.config/chirp; under a second)
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
import hocket as K  # noqa: E402

SR = 48000


def bursts(starts, length, seconds=8.0, tail=0.0):
    """A 220 Hz tone on for `length` seconds from each start (seconds); `tail` > 0 lets it ring on, falling 20 dB in
    that long (a rig that does not stop)."""
    t = np.arange(int(seconds * SR)) / SR
    env = np.zeros(len(t))
    for s in starts:
        on = (t >= s) & (t < s + length)
        env[on] = 1.0
        if tail:
            after = t >= s + length
            env[after] = np.maximum(env[after], 10 ** (-(t[after] - s - length) / tail))
    return np.sin(2 * np.pi * 220 * t) * env


def save(path, left, right=None):
    data = np.stack([left, right], 1) if right is not None else left[:, None]
    with wave.open(path, "wb") as w:
        w.setnchannels(data.shape[1])
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(data, -1, 1) * 30000).astype("<i2").tobytes())
    return path


class Hocket(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="hocket-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        even, odd = [float(s) for s in range(0, 8, 2)], [float(s) for s in range(1, 8, 2)]
        self.turns = save(os.path.join(self.root, "turns.wav"), bursts(even, 1.0), bursts(odd, 1.0))      # never together
        self.step = save(os.path.join(self.root, "step.wav"), bursts(even, 1.0), bursts(even, 1.0))       # always together
        self.rings = save(os.path.join(self.root, "rings.wav"), bursts(even, 1.0, tail=2.0), bursts(odd, 1.0, tail=2.0))

    def run_tool(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = K.main(list(argv))
        return code, out.getvalue()

    @staticmethod
    def row(line):
        f = line.split()
        return f[0], float(f[3].rstrip("%")), float(f[5].rstrip("%")), float(f[7].rstrip("%"))

    def test_parts_that_take_turns_read_one_side_and_parts_in_step_read_both(self):
        code, text = self.run_tool("turns=" + self.turns, "step=" + self.step)
        self.assertEqual(code, 0)
        turns, step = [self.row(ln) for ln in text.splitlines()]
        self.assertEqual(turns[0], "turns")
        self.assertGreater(turns[1], 99.0)                       # one side, all the time
        self.assertLess(turns[2], 1.0)
        self.assertAlmostEqual(step[2], 50.0, delta=1.0)         # in step: both half the time ...
        self.assertAlmostEqual(step[3], 50.0, delta=1.0)         # ... and neither in the rests
        self.assertLess(step[1], 1.0)
        self.assertEqual(text.splitlines()[0][:20], "turns      one side ")

    def test_a_rig_that_rings_through_its_rests_fills_the_holes(self):
        _, text = self.run_tool("dry=" + self.turns, "rings=" + self.rings)
        dry, rings = [self.row(ln) for ln in text.splitlines()]
        self.assertGreater(rings[2], 80.0)                       # 20 dB down only after two seconds: both nearly always
        self.assertLess(rings[1], dry[1] - 80.0)
        _, tight = self.run_tool("rings=" + self.rings, "--floor", "3")   # only what is within 3 dB counts as sounding
        self.assertGreater(self.row(tight.splitlines()[0])[1], rings[1] + 50.0)   # the tails drop out: turns again

    def test_a_passage_is_cut_by_start_and_length(self):
        mixed = save(os.path.join(self.root, "mixed.wav"),
                     np.concatenate([bursts([0.0, 2.0], 1.0, 4.0), bursts([0.0, 2.0], 1.0, 4.0)]),
                     np.concatenate([bursts([1.0, 3.0], 1.0, 4.0), bursts([0.0, 2.0], 1.0, 4.0)]))
        _, text = self.run_tool(f"first={mixed}:0:4", f"second={mixed}:4:4", f"tail={mixed}:4")
        first, second, tail = [self.row(ln) for ln in text.splitlines()]
        self.assertGreater(first[1], 99.0)                       # the first four seconds take turns
        self.assertAlmostEqual(second[2], 50.0, delta=1.0)       # the last four are in step
        self.assertEqual(second[1:], tail[1:])                   # no length: to the end

    def test_what_cannot_be_read_is_said(self):
        mono = save(os.path.join(self.root, "mono.wav"), bursts([0.0], 1.0, 2.0))
        with self.assertRaises(SystemExit) as e:
            self.run_tool("m=" + mono)
        self.assertIn("one channel", str(e.exception))
        with self.assertRaises(SystemExit) as e:
            self.run_tool(self.turns)
        self.assertIn("is not NAME=FILE[:START:DUR]", str(e.exception))
        code, text = self.run_tool()
        self.assertEqual(code, 2)
        self.assertIn("hocket.py NAME=FILE[:START:DUR]", text)


if __name__ == "__main__":
    unittest.main()
