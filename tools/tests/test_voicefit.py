#!/usr/bin/env python3
"""tools/voicefit.py: each measure moves the right way on synthetic voices, and the advice names the right settings.

  python3 tools/tests/test_voicefit.py      (from ~/.config/chirp; ~1 min)
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
import wave

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import voicefit as V  # noqa: E402

SR = V.SR
T = np.arange(int(SR * 3)) / SR


def voice(f0, sub=0.0, noise=0.0, tilt=1.0, vib=(0, 0), seed=0):
    ph = 2 * np.pi * f0 * T
    if vib[1]:
        ph = 2 * np.pi * np.cumsum(f0 * 2 ** (vib[1] / 1200 * np.sin(2 * np.pi * vib[0] * T))) / SR
    x = sum((1 / k ** tilt) * np.sin(k * ph) for k in range(1, 30) if k * f0 < 11000)
    if sub:
        x = x + sub * sum((1 / k ** tilt) * np.sin((k + 0.5) * ph) for k in range(1, 10))
    x = x + noise * np.random.default_rng(seed).normal(size=len(T))
    return 0.3 * x / np.abs(x).max()


def doubled(f0, alt=0.6):
    """A pulse train whose every other period is weaker in short bursts (0.2 s of every 1 s): intermittent period
    doubling, tracked an octave under the pitch around it. (Doubling throughout moves the median too: the pitch check
    flags that.)"""
    x = np.zeros(len(T))
    period = SR / f0
    k, t = 0, 0.0
    while t < len(T) - 40:
        i = int(t)
        burst = (t / SR) % 1.0 < 0.2
        x[i:i + 40] += (alt if burst and k % 2 else 1.0) * np.hanning(40)
        k += 1
        t += period
    return 0.3 * x / np.abs(x).max()


def write(path, x):
    with wave.open(path, "wb") as f:
        f.setnchannels(1), f.setsampwidth(2), f.setframerate(SR)
        f.writeframes((x * 32767).astype("<i2").tobytes())


class Measures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.clean = V.analyse(voice(220))

    def test_pitch(self):
        for f in (110, 220, 330, 523):
            self.assertAlmostEqual(V.analyse(voice(f))["f0_median"], f, delta=f * 0.01)

    def test_effort_follows_spectral_tilt(self):
        self.assertAlmostEqual(self.clean["h1h2"], 6.0, delta=1.0)          # 1/k: H1/H2 = 2
        self.assertAlmostEqual(V.analyse(voice(220, tilt=2))["h1h2"], 12.0, delta=1.0)

    def test_breathiness_is_not_growl(self):
        b = V.analyse(voice(220, noise=0.3))
        self.assertLess(b["hnr"], self.clean["hnr"] - 10)
        self.assertEqual([m for m, _ in V.advice(self.clean, b)], ["breathiness"])

    def test_subharmonics_are_growl_not_breathiness(self):
        g = V.analyse(voice(220, sub=0.1))
        self.assertGreater(g["shr"], self.clean["shr"] + 20)
        self.assertEqual([m for m, _ in V.advice(self.clean, g)], ["growl"])

    def test_period_doubling_reads_octave_low(self):
        d = V.analyse(doubled(220, alt=0.5))
        c = V.analyse(doubled(220, alt=1.0))
        self.assertGreater(d["octave_low"], c["octave_low"] + 5)
        self.assertIn("growl", [m for m, _ in V.advice(c, d)])

    def test_vibrato(self):
        v = V.analyse(voice(220, vib=(5.5, 40)))
        self.assertAlmostEqual(v["vib_rate"], 5.5, delta=0.3)
        self.assertAlmostEqual(v["vib_depth"], 40, delta=8)
        adv = dict(V.advice(v, self.clean))
        self.assertIn("vibrato", adv)
        self.assertIn("5.5hz", adv["vibrato"])

    def test_tract_suggestion_direction(self):
        ref = dict(self.clean, spacing=1000.0)
        ours = dict(self.clean, spacing=1100.0)
        adv = dict(V.advice(ref, ours))
        self.assertIn("x 1.10", adv["tract"])


class Cli(unittest.TestCase):
    def test_wav_mode_json(self):
        d = tempfile.mkdtemp(prefix="voicefit-test-")
        write(os.path.join(d, "ref.wav"), voice(220))
        write(os.path.join(d, "ours.wav"), voice(220, noise=0.3))
        r = subprocess.run([sys.executable, os.path.join(TOOLS, "voicefit.py"), "--wav", os.path.join(d, "ours.wav"),
                            "--ref", os.path.join(d, "ref.wav"), "--json"], capture_output=True, text=True, timeout=300)
        self.assertEqual(r.returncode, 0, r.stderr)
        out = json.loads(r.stdout)
        self.assertEqual([a["measure"] for a in out["advice"]], ["breathiness"])
        for f in os.listdir(d):
            os.remove(os.path.join(d, f))
        os.rmdir(d)


if __name__ == "__main__":
    unittest.main()
