#!/usr/bin/env python3
"""stempitch frames fit --lo (bd-f5d514): a 50 Hz bass note is found at --lo 35 (the fixed 40 ms frame rejected
every frame below ~50 Hz), short notes are kept and counted, octaves follow --keep-octave, and the default
--lo 70 analysis (40 ms frames) is unchanged.

  python3 tools/tests/test_stempitch.py            (from ~/.config/chirp; deterministic, ~15 s)
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import warnings
import wave

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(TOOLS)
SR = 48000
TOOL = os.environ.get("STEMPITCH", os.path.join(TOOLS, "stempitch.py"))   # the CLI under test
sys.path.insert(0, TOOLS)
import stempitch as P  # noqa: E402


def hz(midi):
    return 440 * 2 ** ((midi - 69) / 12)


def tone(f0, n, harmonics=6):
    t = np.arange(n) / SR
    return sum(0.3 / h * np.sin(2 * np.pi * f0 * h * t) for h in range(1, harmonics + 1))


class Stempitch(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        self.dir = tempfile.mkdtemp(prefix="stempitch-")
        self.addCleanup(shutil.rmtree, self.dir, True)

    def test_frames_fit_the_lowest_pitch(self):
        self.assertEqual(P.frame_len(70), int(0.04 * SR), "the default keeps its 40 ms frames")
        self.assertEqual(P.frame_len(35), int(0.08 * SR))
        x = tone(50.0, SR // 4)
        self.assertIsNone(P.yin(x[:int(0.04 * SR)], 35, 220, 0.15), "a 40 ms frame cannot hold two 35 Hz periods")
        f = P.yin(x[:P.frame_len(35)], 35, 220, 0.15)
        self.assertAlmostEqual(f, 50.0, delta=0.5)
        # harmonic-rich low notes: the fundamental, not an octave up or down
        for midi in (31, 35, 40):   # G1 49 Hz, B1 62 Hz, E2 82 Hz
            f = P.yin(tone(hz(midi), SR // 4)[:P.frame_len(35)], 35, 220, 0.15)
            self.assertAlmostEqual(12 * np.log2(f / hz(midi)), 0, delta=0.3, msg=f"midi {midi}: {f}")

    def song(self, notes, stem_notes):
        """A song with one track `bass` (notes: [(name, beats)]) at 120 BPM, and a stem playing stem_notes
        ([(midi or None, beats)])."""
        path = os.path.join(self.dir, "song.yaml")
        score = " ".join(f"{n}/{b:g}b" for n, b in notes)
        with open(path, "w") as f:
            f.write(f'tempo: 120\ntracks:\n  - {{name: bass, patch: x, score: "{score}"}}\n')
        x = np.zeros(int((sum(b for _, b in stem_notes) * 0.5 + 1) * SR))
        t = 0
        for midi, beats in stem_notes:
            n = int(beats * 0.5 * SR)
            if midi is not None:
                x[t:t + n] += tone(hz(midi), n)
            t += n
        stem = os.path.join(self.dir, "stem.wav")
        with wave.open(stem, "wb") as w:
            w.setnchannels(2)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((np.clip(np.repeat(x[:, None], 2, 1), -1, 1) * 32767).astype("<i2").tobytes())
        return stem, path

    def run_tool(self, stem, song, *args, tool=TOOL):
        out = os.path.join(self.dir, "out.json")
        r = subprocess.run([sys.executable, tool, stem, song, "bass", out, *args],
                           capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(r.returncode, 0, r.stderr)
        with open(out) as f:
            return json.load(f)["vox"]["score"].split(), r.stdout

    def test_low_bass_is_repitched_at_lo35(self):
        # written E1 (41 Hz) x2, the stem plays G1 (49 Hz) then E1; a 0.25-beat note is too short for 80 ms frames
        stem, song = self.song([("E1", 2), ("E1", 2), ("A1", 0.25), ("R", 1.75)],
                               [(31, 2), (28, 2), (33, 0.25), (None, 1.75)])
        toks, said = self.run_tool(stem, song, "--lo", "35", "--hi", "220", "--conf", "0.15", "--min-dur", "0.1")
        self.assertEqual(toks, ["G1/2b", "E1/2b", "A1/0.25b", "R/1.75b"], said)
        self.assertIn("1 too short for a 80 ms frame at --lo 35", said)
        # the old fixed frames found nothing at all down here
        toks, _ = self.run_tool(stem, song, "--lo", "35", "--hi", "220", "--conf", "0.15")
        self.assertEqual(toks[0], "G1/2b")

    def test_octaves(self):
        # written E2, the stem plays E1: an octave apart; --keep-octave keeps the tab's register
        stem, song = self.song([("E2", 2), ("G2", 2)], [(28, 2), (33, 2)])
        toks, _ = self.run_tool(stem, song, "--lo", "35", "--hi", "220", "--conf", "0.15")
        self.assertEqual(toks, ["E1/2b", "A1/2b"])
        toks, _ = self.run_tool(stem, song, "--lo", "35", "--hi", "220", "--conf", "0.15", "--keep-octave")
        self.assertEqual(toks, ["E2/2b", "A2/2b"])

    def test_the_default_analysis_is_unchanged(self):
        old = os.environ.get("STEMPITCH_OLD")
        if not old:
            self.skipTest("set STEMPITCH_OLD to a copy of the previous stempitch.py to compare")
        # a vocal-range line (the default --lo 70 / --hi 700), some notes off, one short
        stem, song = self.song([("A3", 1), ("C4", 1), ("E4", 0.5), ("G4", 1.5), ("A3", 0.25), ("R", 0.75)],
                               [(57, 1), (62, 1), (64, 0.5), (66, 1.5), (59, 0.25), (None, 0.75)])
        self.assertEqual(self.run_tool(stem, song), self.run_tool(stem, song, tool=old))


if __name__ == "__main__":
    unittest.main(verbosity=2)
