#!/usr/bin/env python3
"""cymspec: a cymbal's top beside the records' drum stems, and how fast its strokes fall (chirper-zero's bench).

  python3 tools/tests/test_cymspec.py      (from ~/.config/chirp; ~2 s)
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

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import cymspec as Y  # noqa: E402

SR = 44100


def write(path, x):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 20000).astype("<i2").tobytes())


def noise(secs, lo, hi, seed=0):
    """Noise between lo and hi Hz."""
    n = int(secs * SR)
    sp = np.fft.rfft(np.random.default_rng(seed).standard_normal(n))
    f = np.fft.rfftfreq(n, 1 / SR)
    sp[(f < lo) | (f >= hi)] = 0
    x = np.fft.irfft(sp, n)
    return x / np.abs(x).max()


def strokes(x, every=1.0, tau=0.3):
    """x struck once every `every` seconds, each stroke dying with time constant tau."""
    t = (np.arange(len(x)) / SR) % every
    return x * np.exp(-t / tau)


class Cym(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="cymspec-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self.old = Y.B.ROOT
        Y.B.ROOT = self.root
        self.addCleanup(setattr, Y.B, "ROOT", self.old)

    def test_a_ringing_plate_falls_less_than_a_splash(self):
        x = noise(8.0, 2000, 16000)
        ring, splash = strokes(x, tau=0.6), strokes(x, tau=0.05)
        fr, nr = Y.fall(ring, SR, 2000, 8000)
        fs, ns = Y.fall(splash, SR, 2000, 8000)
        self.assertGreaterEqual(nr, 6)
        self.assertGreaterEqual(ns, 6)
        self.assertGreater(fr, -6)                 # 0.3 s on, exp(-0.3 / 0.6): about 4 dB down
        self.assertLess(fs, -20)                   # a splash is gone in a quarter of a second
        self.assertEqual(Y.fall(np.zeros(100), SR, 2000, 8000)[1], 0)

    def test_hiss_reads_over_the_records_at_the_top_and_metal_reads_level(self):
        for i, r in enumerate(Y.REFS[:5]):         # five "records": 9 dB more at 4-8 kHz than at 8-16 kHz
            write(os.path.join(self.root, "ref", "stems", "bs_roformer_sw", r, "drums.wav"),
                  0.6 * noise(152.0, 2000, 8000, seed=i) + 0.2 * noise(152.0, 8000, 16000, seed=i + 50))
        R = Y.records()
        self.assertEqual(len(R), 5)
        self.assertTrue(os.path.exists(os.path.join(self.root, "ref", "cymspec", "records-drums-top.json")))
        hiss, metal = os.path.join(self.root, "hiss.wav"), os.path.join(self.root, "metal.wav")
        write(hiss, strokes(noise(6.0, 8000, 16000, seed=7), tau=0.05))                       # the library's closed hat
        write(metal, strokes(0.6 * noise(6.0, 2000, 8000, seed=8) + 0.2 * noise(6.0, 8000, 16000, seed=9), tau=0.3))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            Y.main([f"hiss={hiss}", f"metal={metal}:0:5"])
        text = out.getvalue()
        self.assertIn("(5 records' drum stems, whole)", text)
        self.assertIn("more at 4-8 kHz than at 8-16 kHz (median 6.1)", text)
        def get(name):
            ln = [x for x in text.splitlines() if x.startswith(name)][0]
            return [float(ln[18 + 6 * i:24 + 6 * i]) for i in range(13)]
        h, m = get("hiss"), get("metal")
        top, mid = Y.LAB.index("12.5k"), Y.LAB.index("5k")
        self.assertGreater(h[top] - h[mid], 30)    # nothing under the hiss: far over at the top against its own middle
        self.assertLess(abs(m[top] - m[mid]), 2)   # the same tilt as the records
        with self.assertRaises(SystemExit), contextlib.redirect_stdout(io.StringIO()):
            Y.main(["nothing"])


if __name__ == "__main__":
    unittest.main()
