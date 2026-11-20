#!/usr/bin/env python3
"""kickspec: a bass drum's strokes read by thirds of an octave beside the records' (chirper-one's bench, Where It
Was v27).

  python3 tools/tests/test_kickspec.py      (from ~/.config/chirp; ~2 s)
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
import kickspec as K  # noqa: E402

SR = K.SR
TIMES = [0.5 + 0.4 * i for i in range(8)]          # eight strokes


def kick(times, f0=58.0, chest=0.0, click=0.05, secs=4.0, seed=0):
    """A drum on f0 Hz (with `chest` of its octave) and a burst of click (2-6 kHz noise) at each time, dying in 60 ms."""
    n = int(secs * SR)
    x = np.zeros(n)
    rng = np.random.default_rng(seed)
    m = int(0.3 * SR)
    t = np.arange(m) / SR
    sp = np.fft.rfft(rng.standard_normal(m))
    f = np.fft.rfftfreq(m, 1 / SR)
    sp[(f < 2000) | (f > 6000)] = 0
    nz = np.fft.irfft(sp, m)
    drum = (np.sin(2 * np.pi * f0 * t) + chest * np.sin(2 * np.pi * 2 * f0 * t)) * np.exp(-t / 0.06)
    one = drum + click * nz / np.abs(nz).max() * np.exp(-t / 0.005)
    for at in times:
        a = int(at * SR)
        x[a:a + m] += one[:n - a]
    return x / np.abs(x).max()


def write(path, x):
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 20000).astype("<i2").tobytes())


class Kick(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="kickspec-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self.old = K.S.ROOT
        K.S.ROOT = self.root
        self.addCleanup(setattr, K.S, "ROOT", self.old)

    def test_the_note_the_chest_and_the_click_are_read(self):
        s, knock, click, n = K.read(kick(TIMES), TIMES)
        self.assertEqual(n, 8)
        self.assertEqual(K.LAB[int(np.argmax(s))], "63")                      # a drum on 58 Hz: the 63 Hz band
        self.assertAlmostEqual(float(s[K.NORM].mean()), 0.0, places=6)
        s2, knock2, click2, _ = K.read(kick(TIMES, chest=0.7, click=0.3), TIMES)
        i = K.LAB.index("125")
        self.assertGreater((s2[i] - s2[K.LAB.index("63")]) - (s[i] - s[K.LAB.index("63")]), 15)   # the chest an octave over
        self.assertGreater(click2, click + 8)                                 # more click against the thump
        self.assertLess(knock, -15)                                           # a sine and a click: no middle
        with self.assertRaises(SystemExit):
            K.read(kick(TIMES), [])
        self.assertEqual(K.read(kick(TIMES), TIMES + [3.95])[3], 8)           # a stroke with no 120 ms after it is left out

    def test_a_kick_is_set_beside_the_records_at_its_song_s_own_times(self):
        recs = {}
        for i, r in enumerate(K.REFS[:3]):                                    # three "records": a chest and a click
            s, knock, click, n = K.read(kick(TIMES, chest=0.7, click=0.3, seed=i), TIMES)
            recs[r] = {"shape": [float(v) for v in s], "knock": knock, "click": click, "n": n, "lag_ms": 0.0}
        os.makedirs(os.path.join(self.root, "ref", "kickspec"))
        with open(os.path.join(self.root, "ref", "kickspec", "records-kick.json"), "w") as f:
            json.dump(recs, f)
        ours = os.path.join(self.root, "ours.wav")
        write(ours, kick(TIMES, seed=9)[int(0.2 * SR):])                      # the file begins 10.2 s into the song
        asked = []
        old = K.track_times
        K.track_times = lambda song, track: asked.append((song, track)) or [10.2 + (t - 0.2) for t in TIMES] + [2.0, 99.0]
        self.addCleanup(setattr, K, "track_times", old)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            K.main([f"ours={ours}:song.yaml:10.2:foot", "--each"])
        text = out.getvalue()
        self.assertEqual(asked, [("song.yaml", "foot")])
        self.assertIn("(3 records)", text)
        ln = [x for x in text.splitlines() if x.startswith("ours")][0]
        vals = [float(ln[22 + 6 * i:28 + 6 * i]) for i in range(len(K.LAB))]
        self.assertLess(vals[K.LAB.index("125")], -10)                        # no chest where the records have one
        self.assertTrue(ln.rstrip().endswith(" 8"))                           # the eight strokes inside the file; 2.0 and 99.0 are not
        self.assertIn(K.REFS[0][:22], text)                                   # --each
        with self.assertRaises(SystemExit), contextlib.redirect_stdout(io.StringIO()):
            K.main(["ours=only.wav"])


if __name__ == "__main__":
    unittest.main()
