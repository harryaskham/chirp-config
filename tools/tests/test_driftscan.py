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
        clicks(os.path.join(cls.d, "ref2.wav"), 0.37, n_s=60.0, offset=0.1)
        clicks(os.path.join(cls.d, "early2.wav"), 0.37, n_s=60.0, offset=0.057)   # 43 ms early

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

    def test_offset_reads_an_early_part_on_likeness_flux(self):
        m = D.offset(self.p("early2.wav"), self.p("ref2.wav"))
        self.assertAlmostEqual(m["lag_ms"], -43, delta=12)            # one 21.3 ms frame of slack
        self.assertGreater(m["gain"], 0)
        z = D.offset(self.p("ref2.wav"), self.p("ref2.wav"))
        self.assertAlmostEqual(z["lag_ms"], 0, delta=5)
        self.assertIn("EARLY", D.offset_row("x", {"_mix": m}, 15))
        self.assertNotIn("EARLY", D.offset_row("x", {"_mix": z}, 15))

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

    def test_little_percussion_marks_a_weak_flag(self):
        m = {"windows": 20, "median_ms": 0.0, "drift_ms": 150.0, "first_q_ms": -80.0, "last_q_ms": 70.0,
             "span_s": 200.0, "drums_pct": 0.6}
        self.assertIn("drift? (little percussion: 0.6% drums; a lead only)", D.row("x", m, 60))
        self.assertIn("  DRIFT", D.row("x", dict(m, drums_pct=23.0), 60))
        self.assertIn("  DRIFT", D.row("x", dict(m, drums_pct=None), 60))   # no stems: no judgement
        self.assertIn("drift? (whole mix; a lead only)", D.row("x", dict(m, drums_pct=23.0, method="mix"), 60))

    def test_focus_ids(self):
        reg = {"focus": "Amnesiac", "climbs": [
            {"id": "b", "enabled": True, "song": "s", "meta": {"album": "Amnesiac", "track": 2}},
            {"id": "a", "enabled": True, "song": "s", "meta": {"album": "Amnesiac", "track": 1}},
            {"id": "x", "enabled": True, "song": "s", "meta": {"album": "Other"}}]}
        self.assertEqual(D.focus_ids(reg), ["a", "b"])
        reg["focus"] = "climbs: x, b"
        self.assertEqual(D.focus_ids(reg), ["b", "x"])


class ApplyLags(unittest.TestCase):
    def test_flagged_parts_move_by_their_own_lag(self):
        song = {"tracks": [{"name": "vox", "score": "C4/1b"}, {"name": "bass", "at": "0.010s", "score": "C2/1b"},
                           {"name": "pad", "score": "C3/1b"}, {"name": "keys", "at": "2b", "score": "C4/1b"},
                           {"name": "drums", "score": "C4/1b"}, {"name": "gtr", "score": "C4/1b"}]}
        res = {"vox": {"lag_ms": -37.0, "gain": 0.01}, "bass": {"lag_ms": -128.0, "gain": 0.02},
               "pad": {"lag_ms": 10.0, "gain": 0.01},           # under --flag-ms: left
               "keys": {"lag_ms": -40.0, "gain": 0.01},         # `at` in beats: skipped, said so
               "drums": {"lag_ms": -30.0, "gain": 0.001},       # no correlation gain: left
               "gtr": {"lag_ms": 45.0, "gain": 0.01}}           # late: moved earlier
        new, done = D.apply_lags(song, res, 15.0, skip=(), cap=None, max_ms=130.0, fps=100.0)
        at = {t["name"]: t.get("at") for t in new["tracks"]}
        self.assertEqual(at, {"vox": "0.037s", "bass": "0.138s", "pad": None, "keys": "2b", "drums": None, "gtr": "-0.045s"})
        notes = {n: note for n, _, note in done}
        self.assertIn("edge", notes["bass"])
        self.assertIn("not in seconds", notes["keys"])
        self.assertNotIn("at", song["tracks"][0])                   # the input is untouched
        capped, _ = D.apply_lags(song, res, 15.0, skip=("gtr",), cap=60.0, max_ms=130.0, fps=100.0)
        at = {t["name"]: t.get("at") for t in capped["tracks"]}
        self.assertEqual((at["bass"], at["gtr"]), ("0.070s", None))

class SectionLags(unittest.TestCase):
    def test_a_late_section_shows_while_the_rest_reads_zero(self):
        import numpy as np
        import likeness as L
        rng = np.random.default_rng(3)
        fps = L.FPS
        n = int(60 * fps)
        r = np.zeros(n)
        r[rng.choice(n, 400, replace=False)] = 1.0
        r = np.convolve(r, np.ones(5) / 5, "same")
        o = r.copy()
        k = int(round(0.2 * fps))                       # section 20-40 s: ours 200 ms late
        i, j = int(20 * fps), int(40 * fps)
        o[i + k:j] = r[i:j - k]
        o[i:i + k] = 0
        out = D.section_lags(r, o, [0.0, 20.0, 40.0, 60.0, 61.0], 250.0)
        self.assertEqual(len(out), 3)                     # the 1 s tail section is too short: left out
        lags = [round(x[2]["lag_ms"] / 10) * 10 for x in out]
        self.assertEqual(lags[0], 0)
        self.assertAlmostEqual(out[1][2]["lag_ms"], 200, delta=1000 / fps)
        self.assertEqual(lags[2], 0)

if __name__ == "__main__":
    unittest.main()
