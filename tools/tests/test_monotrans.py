#!/usr/bin/env python3
"""monotrans: a monophonic line from a stem (chirper-zero's request; its prototype, identical on Green Calx's vocals).

  python3 tools/tests/test_monotrans.py      (from ~/.config/chirp; seconds)
"""
import json
import os
import shutil
import sys
import tempfile
import unittest
import wave

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import chirpbin  # noqa: E402
import monotrans as M  # noqa: E402

SR = 48000
LINE = [(0.0, 0.5, 60), (0.5, 0.5, 62), (1.0, 0.5, 64), (1.5, 0.5, None), (2.0, 1.0, 67), (3.0, 0.06, 72), (3.06, 0.94, 65)]
HAVE_CHIRP = os.path.exists(chirpbin.resolve("chirp"))


def line():
    x = np.zeros(int(4.5 * SR))
    for at, ln, m in LINE:
        if m is None:
            continue
        t = np.arange(int(ln * SR)) / SR
        f = 440 * 2 ** ((m - 69) / 12)
        x[int(at * SR):int(at * SR) + len(t)] += 0.1 * sum(np.sin(2 * np.pi * h * f * t) / h for h in range(1, 6))
    return x


class Mono(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dir = tempfile.mkdtemp(prefix="monotrans-test-")
        cls.x = line()
        cls.stem = os.path.join(cls.dir, "line.wav")
        pcm = (np.clip(cls.x, -1, 1) * 32767).astype("<i2")
        with wave.open(cls.stem, "wb") as f:
            f.setnchannels(2), f.setsampwidth(2), f.setframerate(SR)
            f.writeframes(np.repeat(pcm[:, None], 2, axis=1).tobytes())

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.dir, ignore_errors=True)

    def notes(self):
        return M.notes_of(M.frames(self.x, 0, 4.5), 4.5)

    def test_the_line_comes_back_and_the_rest_stays_silent(self):
        got = [(n["pitch"], float(n["at"].rstrip("s"))) for n in self.notes()]
        self.assertEqual([p for p, _ in got], [60, 62, 64, 67, 65])
        for (p, at), want in zip(got, [0.0, 0.5, 1.0, 2.0, 3.06]):
            self.assertAlmostEqual(at, want, delta=0.06, msg=p)

    def test_runs_shorter_than_min_len_are_dropped(self):
        self.assertNotIn(72, [n["pitch"] for n in self.notes()])      # the 60 ms blip

    def test_a_gate_above_the_line_makes_silence(self):
        self.assertEqual(M.notes_of(M.frames(self.x, 0, 4.5, gate=0), 4.5), [])

    @unittest.skipUnless(HAVE_CHIRP, "needs the groove pin")
    def test_into_writes_a_notes_track_and_refuses_a_score_track(self):
        src = os.path.join(self.dir, "s.json")
        with open(src, "w") as f:
            json.dump({"tempo": 120, "tracks": [{"name": "keys", "patch": "piano", "score": "C4/1b"}]}, f)
        out = os.path.join(self.dir, "o.json")
        M.main([self.stem, "--from", "0", "--to", "4", "--into", src, "--track", "vox", "--patch", "piano", "-o", out])
        self.assertEqual([n["pitch"] for n in json.load(open(out))["tracks"][1]["notes"]], [60, 62, 64, 67, 65])
        with self.assertRaises(SystemExit):
            M.main([self.stem, "--from", "0", "--to", "4", "--into", src, "--track", "keys", "-o", out])


if __name__ == "__main__":
    unittest.main()
