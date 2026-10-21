#!/usr/bin/env python3
"""griddrums: grid fit, programming and the rhythm-term fold on a synthetic drum stem with a known grid
(chirper-zero's request).

  python3 tools/tests/test_griddrums.py      (from ~/.config/chirp; ~20 s)
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
import griddrums as G  # noqa: E402
import likeness as L  # noqa: E402

SR, BPM, T0, BARS = 48000, 120.0, 0.5, 16
SIX = 60 / BPM / 4


def drums(kick_slots=(0, 8), hat_slots=tuple(range(0, 16, 2)), extra=()):
    rng = np.random.default_rng(4)
    x = np.zeros(int((T0 + BARS * 16 * SIX + 1) * SR))
    t = np.arange(int(0.08 * SR)) / SR
    kick = np.sin(2 * np.pi * 60 * t) * np.exp(-t / 0.03)
    hat = rng.normal(size=len(t)) * np.exp(-t / 0.01)
    hat = np.diff(np.concatenate([[0], hat]))            # bright
    fade = np.minimum(1, (len(t) - np.arange(len(t))) / (0.02 * SR))   # no click where a burst ends
    kick, hat = kick * fade, hat * fade
    for n in range(BARS * 16):
        a = int((T0 + n * SIX) * SR)
        if n % 16 in kick_slots:
            x[a:a + len(t)] += 0.6 * kick
        if n % 16 in hat_slots:
            x[a:a + len(t)] += 0.25 * hat
        if n % 16 in extra:
            x[a:a + len(t)] += 0.5 * kick + 0.2 * hat
    return x


def write(path, x):
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as f:
        f.setnchannels(2), f.setsampwidth(2), f.setframerate(SR)
        f.writeframes(np.repeat(pcm[:, None], 2, axis=1).tobytes())


class Grid(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dir = tempfile.mkdtemp(prefix="griddrums-test-")
        cls.x = drums()
        cls.ref = os.path.join(cls.dir, "ref.wav")
        write(cls.ref, cls.x)
        cls.gallop = os.path.join(cls.dir, "gallop.wav")
        write(cls.gallop, drums(extra=(3, 11)))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.dir, ignore_errors=True)

    def test_fit_recovers_the_tempo_and_the_lattice(self):
        r = G.fit(self.x, 70, 180)
        self.assertAlmostEqual(r["bpm"], BPM, delta=0.05)
        frac = ((r["t0"] - T0) / SIX) % 1
        self.assertLess(min(frac, 1 - frac), 0.1, r)
        self.assertGreater(r["on_grid"], 0.9, r)

    def test_program_plays_the_stem_pattern_per_band(self):
        song = {"tempo": 120, "tracks": [{"name": "drums-kick", "patch": "kit", "notes": []}]}
        cuts = [0.0, T0 + 8 * 16 * SIX, T0 + BARS * 16 * SIX]
        out, counts = G.program(song, self.x, cuts, BPM, T0, [("low", "k", "drums-kick"), ("hi", "h", "drums-hats")], G.BANDS,
                                replace=True, log=lambda *_: None)
        kicks = [round((float(n["at"].rstrip("s")) - T0) / SIX) % 16 for n in out["tracks"][0]["notes"]]
        hats = [round((float(n["at"].rstrip("s")) - T0) / SIX) % 16 for n in out["tracks"][1]["notes"]]
        self.assertEqual(set(kicks), {0, 8})
        self.assertTrue(set(hats) <= set(range(0, 16, 2)) and len(set(hats)) >= 6, sorted(set(hats)))
        self.assertEqual(out["tracks"][1]["name"], "drums-hats")
        self.assertEqual(out["tracks"][1]["patch"], "kit")
        self.assertEqual(song["tracks"][0]["notes"], [], "the input is not modified")

    def test_fold_matches_itself_and_flags_a_gallop(self):
        cuts = [T0, T0 + BARS * 16 * SIX]
        (_, _, a, b, r_same), = G.fold(L.load(self.ref), L.load(self.ref), cuts, BPM, T0)
        self.assertAlmostEqual(r_same, 1.0, places=6)
        (_, _, a, b, r_gal), = G.fold(L.load(self.ref), L.load(self.gallop), cuts, BPM, T0)
        self.assertLess(r_gal, 0.9)
        for k in (3, 11):
            self.assertGreater(b[k] / b.max(), a[k] / a.max() + 0.1, (G.digits(a), G.digits(b)))


if __name__ == "__main__":
    unittest.main()
