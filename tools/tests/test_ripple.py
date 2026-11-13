#!/usr/bin/env python3
"""tools/ripple.py: a spectrum's fine structure, twelfth-octave bands about their own average (chirper-zero's).

Hermetic: noise, noise through a comb that alternates +4 / -4 dB a twelfth-octave from 400 Hz to 1.6 kHz, and a
"riff" of a few harmonic series, whose lines read as ripple with no cabinet at all.

  python3 tools/tests/test_ripple.py      (from ~/.config/chirp; a second)
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
import ripple as R  # noqa: E402

SR = 32000


def shaped(x, gain_db):
    """x with gain_db(frequencies) applied in the frequency domain."""
    f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(np.fft.rfft(x) * 10 ** (gain_db(f) / 20), len(x))


def comb(f):
    """+4 / -4 dB by twelfth-octave from 400 Hz to 1.6 kHz, nothing elsewhere."""
    band = np.floor(12 * np.log2(np.maximum(f, 1.0) / 400.0))
    return np.where((f >= 400) & (f < 1600), np.where(band % 2 == 0, 4.0, -4.0), 0.0)


def save(path, x):
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


class Ripple(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="ripple-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self.noise = np.random.default_rng(4).standard_normal(SR * 4) * 0.05
        t = np.arange(SR * 4) / SR
        self.riff = sum(0.02 / h * np.sin(2 * np.pi * f0 * h * t) for f0 in (82.4, 110.0, 146.8) for h in range(1, 40))

    def path(self, name, x):
        p = os.path.join(self.root, name)
        save(p, x)
        return p

    def run_tool(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = R.main(list(argv))
        return code, out.getvalue()

    @staticmethod
    def row(text, name):
        return [float(v) for v in next(ln for ln in text.splitlines() if ln.startswith(name))[26:].split()]

    def test_a_comb_reads_as_ripple_where_it_is_and_smooth_noise_does_not(self):
        _, text = self.run_tool("smooth=" + self.path("n.wav", self.noise), "combed=" + self.path("c.wav", shaped(self.noise, comb)))
        self.assertEqual(text.splitlines()[0],
                         "%-26s %8s %8s %8s   (records 1.6-2.9 | 1.1-1.8 | 2.4-3.1)" % ("ripple, dB", "0.4-1.6k", "1.6-3.2k", "3.2-6.4k"))
        smooth, combed = self.row(text, "smooth"), self.row(text, "combed")
        for v in smooth:
            self.assertLess(v, 0.8)
        self.assertGreater(combed[0], 3.0)                                 # +4 / -4 about a nine-band average
        self.assertLess(combed[0], 5.0)
        self.assertAlmostEqual(combed[1], smooth[1], delta=0.05)           # the comb stops at 1.6 kHz
        self.assertAlmostEqual(combed[2], smooth[2], delta=0.05)

    def test_a_riff_reads_as_ripple_with_no_cabinet_and_over_takes_the_notes_out(self):
        dry = self.path("dry.wav", self.riff)
        quiet = self.path("quiet.wav", self.riff * 0.5)                    # a stage with no detail at all
        cab = self.path("cab.wav", shaped(self.riff, comb))
        _, plain = self.run_tool("dry=" + dry, "quiet=" + quiet)
        self.assertGreater(self.row(plain, "dry")[0], 2.0)                 # the harmonics of the notes, not a speaker
        self.assertAlmostEqual(self.row(plain, "quiet")[0], self.row(plain, "dry")[0], delta=0.05)
        code, text = self.run_tool("quiet=" + quiet, "cab=" + cab, "--over", dry)
        self.assertEqual(code, 0)
        self.assertIn("(each file less the dry one: the stage's own)", text.splitlines()[0])
        for v in self.row(text, "quiet"):
            self.assertLess(v, 0.05)                                       # ... and with the notes taken out it has none
        self.assertGreater(self.row(text, "cab")[0], 3.0)
        self.assertLess(self.row(text, "cab")[1], 0.05)

    def test_a_passage_of_a_file(self):
        both = self.path("both.wav", np.concatenate([self.noise, shaped(self.noise, comb)]))
        _, text = self.run_tool("first=" + both + ":0:4", "second=" + both + ":4:4", "whole=" + both)
        self.assertLess(self.row(text, "first")[0], 0.8)
        self.assertGreater(self.row(text, "second")[0], 3.0)
        self.assertGreater(self.row(text, "whole")[0], 1.0)

    def test_no_arguments_is_the_help_and_over_needs_a_file(self):
        code, text = self.run_tool()
        self.assertEqual(code, 2)
        self.assertIn("ripple.py NAME=FILE[:START:DUR]", text)
        with self.assertRaises(SystemExit):
            self.run_tool("a=" + self.path("n.wav", self.noise), "--over")


if __name__ == "__main__":
    unittest.main()
