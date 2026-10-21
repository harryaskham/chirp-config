#!/usr/bin/env python3
"""albumedges: a kept album version's joins compared with the previous kept version's (chirper-zero: Hedphelym v2
and Ageispolis v2 each lost a join unnoticed; climb.py done now warns).

  python3 tools/tests/test_albumjoins.py      (from ~/.config/chirp; seconds)
"""
import importlib.util
import io
import json
import os
import shutil
import tempfile
import unittest
import wave
from contextlib import redirect_stdout

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000


def tone(path, head_db, tail_db, seconds=8.0, seed=0):
    rng = np.random.default_rng(seed)
    n = int(seconds * SR)
    x = rng.normal(size=(n, 2)) * 0.05
    gain = np.interp(np.arange(n), [0, n - 1], [10 ** (head_db / 20), 10 ** (tail_db / 20)])
    pcm = (np.clip(x * gain[:, None], -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as f:
        f.setnchannels(2), f.setsampwidth(2), f.setframerate(SR)
        f.writeframes(pcm.tobytes())


class Joins(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="albumjoins-")
        self.addCleanup(shutil.rmtree, self.root, True)
        os.makedirs(os.path.join(self.root, "ref"))
        os.makedirs(os.path.join(self.root, "climbs", "edges"))
        climbs = [{"id": c, "meta": {"album": "X", "track": i + 1}} for i, c in enumerate("abc")]
        with open(os.path.join(self.root, "climbs.json"), "w") as f:
            json.dump({"climbs": climbs}, f)
        for i, c in enumerate("abc"):
            tone(os.path.join(self.root, "ref", f"{c}.wav"), -6 - 2 * i, -12 - 2 * i, seed=i)
        os.environ["CLIMB_ROOT"] = self.root
        self.addCleanup(os.environ.pop, "CLIMB_ROOT", None)
        spec = importlib.util.spec_from_file_location("albumedges_t", os.path.join(TOOLS, "albumedges.py"))
        self.A = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.A)
        # kept versions of the neighbours, and b's kept v1 rendered like its record
        for c in "ac":
            self.A.cmd_record([c, os.path.join(self.root, "ref", f"{c}.wav")], version="v1")
        self.b1 = os.path.join(self.root, "b1.wav")
        tone(self.b1, -8, -14, seed=11)
        self.A.cmd_record(["b", self.b1], version="v1")

    def test_join_scores_match_what_check_prints(self):
        out = io.StringIO()
        with redirect_stdout(out):
            self.A.cmd_check(["b", self.b1])
        printed = [float(line.split("score ")[1]) for line in out.getvalue().splitlines() if "score " in line]
        ours, ref, _ = self.A.render_edges("b", self.b1, 3.0)
        j = self.A.join_scores("b", ours, ref)
        self.assertEqual([j["from"]["score"], j["into"]["score"]], [round(v, 1) for v in printed])
        self.assertEqual((j["from"]["with"], j["into"]["with"]), ("a", "c"))

    def test_the_same_render_raises_no_warning(self):
        joins, warns = self.A.join_regressions("b", self.b1)
        self.assertEqual(warns, [])
        self.assertEqual(joins["into"]["was"], joins["into"]["score"])

    def test_a_louder_tail_warns_about_the_join_into_the_next_song(self):
        b2 = os.path.join(self.root, "b2.wav")
        with wave.open(self.b1) as f:
            x = np.frombuffer(f.readframes(f.getnframes()), "<i2").reshape(-1, 2).astype(float)
        x[-3 * SR:] *= 10                               # only the last 3 s, 20 dB hotter than the kept version's
        with wave.open(b2, "wb") as f:
            f.setnchannels(2), f.setsampwidth(2), f.setframerate(SR)
            f.writeframes(np.clip(x, -32768, 32767).astype("<i2").tobytes())
        joins, warns = self.A.join_regressions("b", b2)
        self.assertEqual(len(warns), 1, warns)
        self.assertIn("join into c gets worse", warns[0])
        self.assertIn("level-match this song's tail", warns[0])
        self.assertLess(joins["into"]["score"], joins["into"]["was"] - 0.5)

    def test_no_recorded_version_means_no_comparison(self):
        os.remove(os.path.join(self.root, "climbs", "edges", "b.json"))
        joins, warns = self.A.join_regressions("b", self.b1)
        self.assertEqual(warns, [])
        self.assertNotIn("was", joins["into"])


if __name__ == "__main__":
    unittest.main()
