#!/usr/bin/env python3
"""tools/microscore.py: each dimension moves with the change it is meant to see and ignores gain and small offsets.

  python3 tools/tests/test_microscore.py      (from ~/.config/chirp; ~20 s)
"""
import os
import sys
import unittest

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import microscore as M  # noqa: E402

SR = M.SR


def plucks(semis=0.0, attack=0.003, seconds=4.0, seed=0):
    """A monophonic line of plucked harmonic notes (E3 G3 A3 B3 ...), slightly wide stereo."""
    rng = np.random.default_rng(seed)
    line = [52, 55, 57, 59, 57, 55, 52, 50]
    dur = seconds / len(line)
    t = np.arange(int(dur * SR)) / SR
    out = []
    for m in line:
        f = 440 * 2 ** ((m + semis - 69) / 12)
        x = sum(np.sin(2 * np.pi * f * h * t) * (0.7 ** h) for h in range(1, 10))
        env = np.minimum(1, t / attack) * np.exp(-t * 3)
        out.append(0.2 * x * env)
    mono = np.concatenate(out)
    side = 0.15 * np.convolve(rng.normal(size=len(mono)), np.ones(32) / 32, "same") * np.abs(mono).max()
    return np.stack([mono + side, mono - side], 1)


def lowpass(x, fc):
    from scipy import signal
    return signal.sosfilt(signal.butter(6, fc, fs=SR, output="sos"), x, axis=0)


class MicroScore(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ref = plucks()
        cls.self_ = M.score(cls.ref, cls.ref)

    def test_identity_scores_100(self):
        for k, v in self.self_.items():
            if k in ("total", "voiced", "raw") or v is None:
                continue
            self.assertGreater(v, 99.0, k)
        self.assertIsNotNone(self.self_["pitch"])            # a monophonic line is pitch-scored

    def test_gain_and_a_small_offset_are_ignored(self):
        d = int(0.02 * SR)
        moved = np.concatenate([np.zeros((d, 2)), 0.5 * self.ref])[:len(self.ref)]
        s = M.score(self.ref, moved)
        self.assertGreater(s["total"], 95.0, s)

    def test_a_lowpass_drops_tone_not_pitch(self):
        s = M.score(self.ref, lowpass(self.ref, 1500))     # (spectral is energy-weighted: these harmonics are weak)
        self.assertLess(s["tone"], 80.0, s)
        self.assertLess(s["timbre"], 90.0, s)
        self.assertGreater(s["pitch"], 90.0, s)
        self.assertGreater(s["transients"], 95.0, s)

    def test_a_semitone_drops_pitch(self):
        s = M.score(self.ref, plucks(semis=1.0))
        self.assertLess(s["pitch"], 50.0, s)

    def test_soft_attacks_drop_transients(self):
        s = M.score(self.ref, plucks(attack=0.08))
        self.assertLess(s["transients"], self.self_["transients"] - 10, s)

    def test_a_sub_octave_does_not_swamp_transients(self):
        low = plucks(semis=-24)                           # E1.. bass line
        t = np.arange(len(low)) / SR
        sub = 0.5 * np.sin(2 * np.pi * 20.6 * t)[:, None] * np.abs(low).max()   # a sustained sub-octave drone
        s = M.score(low, low + sub)
        self.assertGreater(s["transients"], 80.0, s)

    def test_mono_drops_stereo(self):
        mono = np.repeat(self.ref.mean(1, keepdims=True), 2, 1)
        s = M.score(self.ref, mono)
        self.assertLess(s["stereo"], 85.0, s)

    def test_a_hard_panned_take_keeps_a_sane_stereo_score(self):
        right = np.stack([np.zeros(len(self.ref)), self.ref.mean(1)], 1)          # pan +1: the left channel is silent
        near = np.stack([0.05 * self.ref.mean(1), self.ref.mean(1)], 1)           # pan +0.9: -26 dB on the left
        s = M.score(right, near)
        self.assertGreater(s["stereo"], 50.0, s)                                  # (unclamped ILD read -230 dB: 0)

    def test_noise_scores_low(self):
        noise = np.random.default_rng(1).normal(size=self.ref.shape) * 0.05
        s = M.score(self.ref, noise)
        self.assertLess(s["total"], 35.0, s)


if __name__ == "__main__":
    unittest.main()
