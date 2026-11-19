#!/usr/bin/env python3
"""snarespec: a snare's strokes found in a solo file, its shape beside the records', its ratios and its fall
(chirper-zero's bench, Extreme and Mean v26).

  python3 tools/tests/test_snarespec.py      (from ~/.config/chirp; ~2 s)
"""
import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
import wave

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import snarespec as S  # noqa: E402

SR = S.SR


def snare(note, secs=4.0, every=0.5, tau=0.03, crack=0.3, seed=0, sr=SR):
    """Strokes every `every` s: a drum on `note` Hz and a burst of crack (1.5-5 kHz noise), each dying with tau."""
    n = int(secs * sr)
    t = np.arange(n) / sr
    ph = t % every
    rng = np.random.default_rng(seed)
    sp = np.fft.rfft(rng.standard_normal(n))
    f = np.fft.rfftfreq(n, 1 / sr)
    sp[(f < 1500) | (f > 5000)] = 0
    nz = np.fft.irfft(sp, n)
    x = (np.sin(2 * np.pi * note * ph) + crack * nz / np.abs(nz).max()) * np.exp(-ph / tau)
    x[t < 0.25] = 0                                # a quarter second of nothing first: the first stroke has a rise
    return x / np.abs(x).max()


def write(path, x, sr=SR):
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((x * 20000).astype("<i2").tobytes())


class Snare(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="snarespec-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self.old = S.ROOT
        S.ROOT = self.root
        self.addCleanup(setattr, S, "ROOT", self.old)

    def test_strokes_are_found_and_the_note_falls_in_its_band(self):
        y = snare(200.0)
        ts = S.strokes_in(y)
        self.assertEqual(len(ts), 7)                                         # 0.5, 1.0 ... 3.5 s
        self.assertAlmostEqual(ts[0], 0.5, delta=0.02)
        s, body, wires, dec, n = S.read(y, ts)
        self.assertEqual(n, 7)
        self.assertEqual(S.LAB[int(np.argmax(s))], "200")                    # the drum's note
        self.assertAlmostEqual(float(s[S.NORM].mean()), 0.0, places=6)
        self.assertGreater(body, 0)                                          # more drum than crack
        s2, body2, _, dec2, _ = S.read(snare(250.0, tau=0.08, crack=1.5), S.strokes_in(snare(250.0, tau=0.08, crack=1.5)))
        self.assertEqual(S.LAB[int(np.argmax(s2[:8]))], "250")               # a snare a third higher: the next band
        self.assertLess(body2, body)                                         # ... with more crack
        self.assertGreater(dec2, dec)                                        # ... and a longer ring
        with self.assertRaises(SystemExit):
            S.read(y, [])

    def test_a_snare_is_set_beside_the_records_and_another_rate_is_resampled(self):
        recs = {}
        for i, r in enumerate(S.REFS[:3]):                                   # three "records" with their note at 200 Hz
            y = snare(200.0, seed=i)
            s, body, wires, dec, n = S.read(y, S.strokes_in(y))
            recs[r] = {"shape": [float(v) for v in s], "body": body, "wires": wires, "decay": dec, "n": n, "lag_ms": 0.0}
        os.makedirs(os.path.join(self.root, "ref", "snarespec"))
        with open(os.path.join(self.root, "ref", "snarespec", "records-snare.json"), "w") as f:
            json.dump(recs, f)
        ours, theirs = os.path.join(self.root, "ours.wav"), os.path.join(self.root, "theirs.wav")
        write(ours, snare(250.0, seed=9))                                    # the album's: its note a band too high
        write(theirs, snare(200.0, seed=8, sr=44100), sr=44100)              # like the records, at another sample rate
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            S.main([f"ours={ours}", f"theirs={theirs}:0:3.5", "--each"])
        text = out.getvalue()
        self.assertIn("(3 records)", text)

        def get(name):
            ln = [x for x in text.splitlines() if x.startswith(name)][0]
            return [float(ln[16 + 6 * i:22 + 6 * i]) for i in range(len(S.LAB))], ln
        o, line = get("ours")
        self.assertLess(o[S.LAB.index("200")], -10)                          # short where the records' note is
        self.assertGreater(o[S.LAB.index("250")], 10)                        # ... and over a band higher
        self.assertIn("(7)", line)
        t, line = get("theirs")
        for band in ("200", "3.15k"):                                        # the records' shape where anything sounds,
            self.assertLess(abs(t[S.LAB.index(band)] - t[S.LAB.index("2k")]), 2.0)   # ... resampled from 44.1 kHz
        self.assertIn("(6)", line)                                           # the first 3.5 s: six strokes
        self.assertIn(S.REFS[0][:15], text)                                  # --each
        with self.assertRaises(SystemExit), contextlib.redirect_stdout(io.StringIO()):
            S.main(["nothing"])


if __name__ == "__main__":
    unittest.main()
