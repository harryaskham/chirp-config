#!/usr/bin/env python3
"""noteacc: local note and timing accuracy (Harry 2026-10-20) on a synthetic melody with known errors.

  python3 tools/tests/test_noteacc.py      (from ~/.config/chirp; about a minute)
"""
import os
import sys
import tempfile
import unittest
import wave

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import noteacc  # noqa: E402

SR = 48000
NOTE = 0.5
N = 60                                     # 30 s
SCALE = [55, 57, 59, 60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79]


def melody(pitches, onsets, length=N * NOTE):
    x = np.zeros(int(length * SR) + SR)
    rng = np.random.default_rng(3)
    for p, t0 in zip(pitches, onsets):
        n = int(NOTE * SR)
        t = np.arange(n) / SR
        f = 440 * 2 ** ((p - 69) / 12)
        tone = sum(np.sin(2 * np.pi * k * f * t) / k for k in range(1, 7))
        env = np.minimum(1, t / 0.01) * np.exp(-t / 0.6)
        click = np.zeros(n)
        click[:240] = rng.normal(size=240) * 0.5 * np.exp(-np.arange(240) / 60)
        a = int(t0 * SR)
        x[a:a + n] += 0.15 * tone * env + click
    return x[:int(length * SR)]


def write(path, x):
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(2), w.setsampwidth(2), w.setframerate(SR)
        w.writeframes(np.repeat(pcm[:, None], 2, axis=1).tobytes())


class NoteAcc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dir = tempfile.mkdtemp(prefix="noteacc-test-")
        rng = np.random.default_rng(11)
        cls.p = [int(v) for v in rng.choice(SCALE, N)]
        cls.on = [i * NOTE for i in range(N)]
        wrong = rng.random(N) < 0.3
        cls.files = {}

        def mk(name, pitches, onsets, length=N * NOTE):
            path = os.path.join(cls.dir, name + ".wav")
            write(path, melody(pitches, onsets, length))
            cls.files[name] = path

        mk("ref", cls.p, cls.on)
        mk("same", cls.p, cls.on)
        mk("keys", [p + (1 if i % 2 else -1) if w else p for i, (p, w) in enumerate(zip(cls.p, wrong))], cls.on)
        mk("late", cls.p, [t + 0.08 if w else t for t, w in zip(cls.on, wrong)])
        mk("keys2nd", [p + 1 if t >= 15 else p for p, t in zip(cls.p, cls.on)], cls.on)
        mk("shift30", cls.p, [t + 0.03 for t in cls.on])
        mk("short", cls.p[:40], cls.on[:40], length=20.0)
        cls.r = {k: noteacc.measure(cls.files["ref"], v, [0, 15, 30] if k == "keys2nd" else None)
                 for k, v in cls.files.items() if k != "ref"}

    def test_identical_scores_full(self):
        r = self.r["same"]
        self.assertGreater(r["pitch"]["score"], 95)
        self.assertGreater(r["timing"]["score"], 95)
        self.assertEqual(r["timing"]["offset_ms_median"], 0.0)

    def test_wrong_notes_cost_pitch_not_timing(self):
        same, keys = self.r["same"], self.r["keys"]
        self.assertLess(keys["pitch"]["score"], same["pitch"]["score"] - 15)
        self.assertGreater(keys["timing"]["score"], same["timing"]["score"] - 10)

    def test_late_notes_cost_timing_not_pitch(self):
        same, late = self.r["same"], self.r["late"]
        self.assertLess(late["timing"]["score"], same["timing"]["score"] - 15)
        self.assertGreater(late["pitch"]["score"], 80)

    def test_errors_are_located(self):
        r = self.r["keys2nd"]
        s1, s2 = r["sections"]
        self.assertLess(s2["pitch"], s1["pitch"] - 20)
        self.assertTrue(all(w["start"] >= 11 for w in r["worst"][:3]), r["worst"][:3])

    def test_systematic_lateness_is_reported(self):
        self.assertAlmostEqual(self.r["shift30"]["timing"]["offset_ms_median"], 30, delta=12)

    def test_short_candidate_is_padded_and_reported(self):
        r = self.r["short"]
        self.assertAlmostEqual(r["candidate_seconds"], 20.0, places=2)
        self.assertGreater(r["pitch"]["ref_only"], 0.2)
        self.assertLess(r["timing"]["score"], self.r["same"]["timing"]["score"] - 15)


if __name__ == "__main__":
    unittest.main()
