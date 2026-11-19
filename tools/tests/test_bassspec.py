#!/usr/bin/env python3
"""bassspec: a bass's third-octave shape beside the records' bass stems (chirper-zero's bench, In the Time Of v24).

  python3 tools/tests/test_bassspec.py      (from ~/.config/chirp; ~1 s)
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
import bassspec as B  # noqa: E402


def tone(path, parts, secs=4.0, sr=44100, quiet_tail=0.0):
    """A WAV of sines (freq, amplitude); the last quiet_tail seconds are near silence."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    t = np.arange(int(secs * sr)) / sr
    x = 12000 * sum(a * np.sin(2 * np.pi * f * t) for f, a in parts)
    if quiet_tail:
        x[t > secs - quiet_tail] *= 0.001
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(x.astype("<i2").tobytes())


class Shape(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="bassspec-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self.old = B.ROOT
        B.ROOT = self.root
        self.addCleanup(setattr, B, "ROOT", self.old)

    def test_a_shape_is_level_on_its_mean_and_reads_the_loud_frames(self):
        p = os.path.join(self.root, "a.wav")
        tone(p, [(80, 1.0), (640, 0.1)], quiet_tail=2.0)
        sr, m = B.load(p)
        e = B.shape(m, sr)
        self.assertEqual(B.LAB[int(np.argmax(e))], "80")
        self.assertAlmostEqual(e[B.LAB.index("80")] - e[B.LAB.index("630")], 20.0, delta=1.0)   # 1.0 against 0.1
        self.assertAlmostEqual(float(e[B.NORM].mean()), 0.0, places=6)
        q = os.path.join(self.root, "b.wav")
        tone(q, [(80, 0.25), (640, 0.025)])                                  # the same shape, 12 dB down, no silence
        sq, mq = B.load(q)
        eq = B.shape(mq, sq)
        self.assertAlmostEqual(eq[B.LAB.index("80")] - eq[B.LAB.index("630")], e[B.LAB.index("80")] - e[B.LAB.index("630")], delta=0.5)
        sr2, half = B.load(p, 0.0, 1.0)
        self.assertEqual(len(half), sr2)

    def test_the_records_are_read_once_and_a_bass_is_set_beside_them(self):
        ids = B.REFS[:5]
        for i, r in enumerate(ids):                                          # five "records": the octave, 80 Hz, leads
            tone(os.path.join(self.root, "ref", "stems", "bs_roformer_sw", r, "bass.wav"),
                 [(80, 1.0), (40, 0.05 + 0.01 * i), (500, 0.03)], secs=152.0, sr=22050)
        R = B.records()
        self.assertEqual(sorted(R), sorted(ids))
        self.assertTrue(os.path.exists(os.path.join(self.root, "ref", "bassspec", "records-bass.json")))
        shutil.rmtree(os.path.join(self.root, "ref", "stems"))
        self.assertEqual(B.records(), R)                                     # from the cache: the stems are not read again
        med, spread = B.stats(R)
        self.assertEqual(B.LAB[int(np.argmax(med))], "80")
        ours = os.path.join(self.root, "ours.wav")
        tone(ours, [(40, 1.0), (80, 0.3), (500, 0.3)])                       # a sub and a box
        out = io.StringIO()
        same = os.path.join(self.root, "same.wav")
        tone(same, [(80, 1.0), (40, 0.07), (500, 0.03)])                     # a bass like theirs
        with contextlib.redirect_stdout(out):
            B.main([f"ours={ours}", f"same={same}:0:3"])
        text = out.getvalue()
        self.assertIn("RECORDS (median)", text)
        self.assertIn("(5 records' bass stems)", text)
        line = [ln for ln in text.splitlines() if ln.startswith("ours")][0]
        d = [float(line[16 + 6 * i:22 + 6 * i]) for i in range(25)]
        self.assertGreater(d[B.LAB.index("40")], 15)                         # far over the records at 40 Hz
        self.assertLess(d[B.LAB.index("80")], -5)                            # ... and short at the octave
        self.assertGreater(d[B.LAB.index("500")], 10)
        self.assertRegex(line, r"@(40|50) ")                                 # the worst band is named: the sub
        line = [ln for ln in text.splitlines() if ln.startswith("same")][0]
        d = [float(line[16 + 6 * i:22 + 6 * i]) for i in range(25)]
        for band in ("40", "500"):                                           # the same shape as theirs where anything sounds
            self.assertLess(abs(d[B.LAB.index("80")] - d[B.LAB.index(band)]), 1.5)
        with self.assertRaises(SystemExit):
            B.main(["nothing"])


if __name__ == "__main__":
    unittest.main()
