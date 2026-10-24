#!/usr/bin/env python3
"""tools/keyshift.py: a render a semitone sharp reads best shift -1 in every window; one in key reads 0.

  python3 tools/tests/test_keyshift.py      (from ~/.config/chirp; a few seconds)
"""
import os
import shutil
import sys
import tempfile
import unittest
import wave

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import keyshift as K  # noqa: E402

SR = 48000


def chords(semis=0, seconds=30):
    """A I-IV-V-vi progression in E (2 s each), harmonic tones, shifted by SEMIS."""
    prog = [[64, 68, 71], [69, 73, 76], [71, 75, 78], [61, 64, 68]]
    out = []
    t = np.arange(2 * SR) / SR
    for i in range(seconds // 2):
        x = np.zeros_like(t)
        for m in prog[i % 4]:
            f = 440 * 2 ** ((m + semis - 69) / 12)
            for h in (1, 2, 3):
                x += np.sin(2 * np.pi * f * h * t) / h
        out.append(0.1 * x * np.minimum(1, t * 50))
    return np.concatenate(out)


def write(path, x):
    with wave.open(path, "wb") as f:
        f.setnchannels(2), f.setsampwidth(2), f.setframerate(SR)
        f.writeframes(np.repeat((np.clip(x, -1, 1) * 32767).astype("<i2"), 2).tobytes())


class KeyShift(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = tempfile.mkdtemp(prefix="keyshift-test-")
        write(os.path.join(cls.d, "ref.wav"), chords(-1))       # the record: E-flat
        write(os.path.join(cls.d, "sharp.wav"), chords(0))      # ours from an E-standard tab
        write(os.path.join(cls.d, "right.wav"), chords(-1))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.d, ignore_errors=True)

    def test_a_semitone_sharp_render_reads_minus_one_everywhere(self):
        m = K.measure(K.chroma(os.path.join(self.d, "sharp.wav")), K.chroma(os.path.join(self.d, "ref.wav")))
        self.assertEqual(m["best"], -1)
        self.assertGreater(m["gain"], 0.05)
        self.assertEqual(m["agree"], m["windows"])

    def test_a_render_in_key_reads_zero(self):
        m = K.measure(K.chroma(os.path.join(self.d, "right.wav")), K.chroma(os.path.join(self.d, "ref.wav")))
        self.assertEqual(m["best"], 0)
        self.assertEqual(m["gain"], 0.0)


if __name__ == "__main__":
    unittest.main()
