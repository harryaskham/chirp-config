#!/usr/bin/env python3
"""tools/driftscan.py: a steady tempo error reads as drift, a constant offset as a median lag with no drift; and
onsetlag.windowed_lags is what onsetlag.py prints (its refactor kept the output byte-identical).

  python3 tools/tests/test_driftscan.py      (from ~/.config/chirp; ~1 min)
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import wave

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import driftscan as D  # noqa: E402
import onsetlag  # noqa: E402

SR = 48000


def clicks(path, period, n_s=120.0, offset=0.0):
    """A stereo 16-bit click track: a 5 ms decaying burst every `period` s from `offset`."""
    x = np.zeros(int(SR * n_s))
    burst = np.random.default_rng(0).normal(size=240) * np.exp(-np.arange(240) / 60)
    t = offset
    while t < n_s - 0.01:
        i = int(t * SR)
        x[i:i + 240] += burst[:len(x[i:i + 240])]
        t += period
    x = 0.5 * x / np.abs(x).max()
    with wave.open(path, "wb") as f:
        f.setnchannels(2), f.setsampwidth(2), f.setframerate(SR)
        f.writeframes(np.repeat((x * 32767).astype("<i2"), 2).tobytes())


class Drift(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = tempfile.mkdtemp(prefix="driftscan-test-")
        # a 0.37 s pulse (no common divisor with the windows), the record's
        clicks(os.path.join(cls.d, "ref.wav"), 0.37)
        clicks(os.path.join(cls.d, "fast.wav"), 0.37 * (1 - 0.0008))   # ours 0.08% fast: early by ~93 ms at 116 s
        clicks(os.path.join(cls.d, "late.wav"), 0.37, offset=0.04)      # ours 40 ms late throughout

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.d, ignore_errors=True)

    def p(self, name):
        return os.path.join(self.d, name)

    def test_a_tempo_error_is_drift(self):
        m = D.measure(self.p("fast.wav"), self.p("ref.wav"))
        self.assertLess(m["drift_ms"], -60)
        self.assertGreater(m["drift_ms"], -130)
        self.assertLess(m["last_q_ms"], m["first_q_ms"])

    def test_an_offset_is_not_drift(self):
        m = D.measure(self.p("late.wav"), self.p("ref.wav"))
        self.assertAlmostEqual(m["median_ms"], 40, delta=10)
        self.assertLess(abs(m["drift_ms"]), 20)

    def test_theil_sen_ignores_an_alias(self):
        ts = list(range(10))
        ys = [2.0 * t for t in ts]
        ys[4] = 500.0                                   # a half-beat alias in one window
        self.assertAlmostEqual(D.theil_sen(ts, ys), 2.0, delta=0.01)

    def test_cli_wav_mode(self):
        r = subprocess.run([sys.executable, os.path.join(TOOLS, "driftscan.py"), "--wav", self.p("fast.wav"),
                            "--ref", self.p("ref.wav"), "--json"], capture_output=True, text=True, timeout=300)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertLess(json.loads(r.stdout)["drift_ms"], -60)

    def test_onsetlag_prints_its_windowed_lags(self):
        r = subprocess.run([sys.executable, os.path.join(TOOLS, "onsetlag.py"), self.p("late.wav"), self.p("ref.wav")],
                           capture_output=True, text=True, timeout=300)
        lines = [x for x in r.stdout.splitlines() if " lag " in x and "median" not in x]
        w = onsetlag.windowed_lags(self.p("late.wav"), self.p("ref.wav"))
        self.assertEqual(len(lines), len(w))
        self.assertIn(f"lag {w[0][1]:+5d} ms", lines[0])

    def test_focus_ids(self):
        reg = {"focus": "Amnesiac", "climbs": [
            {"id": "b", "enabled": True, "song": "s", "meta": {"album": "Amnesiac", "track": 2}},
            {"id": "a", "enabled": True, "song": "s", "meta": {"album": "Amnesiac", "track": 1}},
            {"id": "x", "enabled": True, "song": "s", "meta": {"album": "Other"}}]}
        self.assertEqual(D.focus_ids(reg), ["a", "b"])
        reg["focus"] = "climbs: x, b"
        self.assertEqual(D.focus_ids(reg), ["b", "x"])


if __name__ == "__main__":
    unittest.main()
