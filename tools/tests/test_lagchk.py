#!/usr/bin/env python3
"""tools/lagchk.py: how far the right channel's part leads the left's (chirper-zero's, Odd Sympathy v1).

Hermetic: a one-bar riff of short tones on the left, and the same riff on the right moved earlier by a known number
of sixteenths.

  python3 tools/tests/test_lagchk.py      (from ~/.config/chirp; a second)
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
import lagchk as G  # noqa: E402

SR, BPM = 48000, 120                                           # a bar is two seconds, a sixteenth 125 ms
RIFF = [0, 1, 3, 6, 10, 12, 13, 15]                            # attacks in a bar; its second half is the first's negative


def part(lead16, bars=12, riff=RIFF):
    """The riff every bar as 60 ms tones, early by lead16 sixteenths (it wraps round the bar)."""
    x = np.zeros(bars * 2 * SR)
    n = int(0.06 * SR)
    tone = np.sin(2 * np.pi * 220 * np.arange(n) / SR) * np.linspace(1, 0.2, n)
    for b in range(bars):
        for k in riff:
            i = int(((b * 16 + k - lead16) % (bars * 16)) * 0.125 * SR)
            x[i:i + n] += tone[:len(x) - i]
    return x


def save(path, left, right=None):
    data = np.stack([left, right], 1) if right is not None else left[:, None]
    with wave.open(path, "wb") as w:
        w.setnchannels(data.shape[1])
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(data, -1, 1) * 30000).astype("<i2").tobytes())
    return path


class Lagchk(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="lagchk-test-")
        self.addCleanup(shutil.rmtree, self.root, True)

    def run_tool(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = G.main(list(argv))
        return code, out.getvalue()

    def lead(self, text, row=0):
        return float(text.splitlines()[row].split("right leads by ")[1].split()[0])

    def test_a_part_moved_early_reads_as_a_lead_in_sixteenths(self):
        for k in (0, 1, 3, 4):
            wav = save(os.path.join(self.root, f"lead{k}.wav"), part(0), part(k))
            code, text = self.run_tool(wav, str(BPM), "3")
            self.assertEqual(code, 0)
            self.assertAlmostEqual(self.lead(text), k, delta=0.05)
        late = save(os.path.join(self.root, "late.wav"), part(0), part(-2))
        self.assertAlmostEqual(self.lead(self.run_tool(late, str(BPM), "3")[1]), -2, delta=0.05)   # minus: the right is late

    def test_half_a_bar_reads_plus_and_minus_eight_alike(self):
        wav = save(os.path.join(self.root, "against.wav"), part(0), part(8))
        _, text = self.run_tool(wav, str(BPM), "3")
        line = text.splitlines()[0]
        self.assertEqual(line[:11], "         3:")
        both = sorted(float(p.split()[0]) for p in line.split("right leads by ")[1].split(", then "))
        self.assertAlmostEqual(both[0], -8, delta=0.05)
        self.assertAlmostEqual(both[1], 8, delta=0.05)

    def test_positions_as_chirp_render_takes_them_and_the_window(self):
        # in step for six bars, then the right part a sixteenth early
        left = part(0)
        right = np.concatenate([part(0)[:6 * 2 * SR], part(1)[6 * 2 * SR:]])
        wav = save(os.path.join(self.root, "slip.wav"), left, right)
        _, text = self.run_tool(wav, str(BPM), "2", "8", "28b", "14s", "40", "--bars", "2")
        rows = text.splitlines()
        self.assertAlmostEqual(self.lead(text, 0), 0, delta=0.05)          # bar 2: in step
        for row in (1, 2, 3):                                              # bar 8 = beat 28 = 14 s: after the slip
            self.assertAlmostEqual(self.lead(text, row), 1, delta=0.05)
        self.assertEqual(rows[4], "        40: outside the file")
        _, near = self.run_tool(wav, str(BPM), "8", "--reach", "0.5")      # a reach too short to see a whole sixteenth
        self.assertLess(abs(self.lead(near)), 0.51)

    def test_one_channel_and_no_arguments(self):
        mono = save(os.path.join(self.root, "mono.wav"), part(0))
        with self.assertRaises(SystemExit) as e:
            self.run_tool(mono, str(BPM), "3")
        self.assertIn("one channel", str(e.exception))
        code, text = self.run_tool(mono)
        self.assertEqual(code, 2)
        self.assertIn("lagchk.py WAV BPM POS [POS ...]", text)


if __name__ == "__main__":
    unittest.main()
