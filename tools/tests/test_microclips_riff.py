#!/usr/bin/env python3
"""tools/microclips.py --sum / --ref-stems and microscore's stems: references: a riff that no single stem dominates
(Immutable's 8-string splits between demucs' guitar and bass stems) is proposed as a summed family, and its clip is
scored against those stems summed.

  python3 tools/tests/test_microclips_riff.py      (from ~/.config/chirp; a second)
"""
import os
import sys
import tempfile
import unittest
import wave

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import microclips as M  # noqa: E402
import microscore as S  # noqa: E402

SR = M.L.SR


def write(path, x):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


class Riff(unittest.TestCase):
    def test_sums_parse(self):
        self.assertEqual(M.parse_sums(["riff=guitar+bass"]), [("riff", ["guitar", "bass"])])
        for bad in (["riff=guitar"], ["=guitar+bass"], ["riff=guitar+tuba"]):
            with self.assertRaises(SystemExit):
                M.parse_sums(bad)

    def test_riff_is_proposed_and_scored_against_summed_stems(self):
        rng = np.random.default_rng(0)
        n = 12 * SR
        stems = {"guitar": 0.3 * rng.normal(size=n), "bass": 0.3 * rng.normal(size=n), "drums": 0.1 * rng.normal(size=n),
                 "vocals": 1e-4 * rng.normal(size=n), "other": 1e-4 * rng.normal(size=n)}
        with tempfile.TemporaryDirectory() as root:
            for s, x in stems.items():
                write(os.path.join(root, "ref", "stems", "htdemucs_6s", "song", f"{s}.wav"), x)
            old_m, old_s, M.ROOT, S.ROOT = M.ROOT, S.ROOT, root, root
            try:
                plain = M.candidates("song")
                self.assertFalse([c for c in plain if c["family"] in ("guitar", "bass")])     # no single stem dominates
                riff = [c for c in M.candidates("song", sums=M.parse_sums(["riff=guitar+bass"])) if c["family"] == "riff"]
                self.assertTrue(riff and riff[0]["share"] > 0.85)
                ref = S.clip_ref({"song": "song", "from": 2.0, "to": 4.0, "ref": "stems:guitar+bass"})
                want = S.cut(S.L.load(os.path.join(root, "ref", "stems", "htdemucs_6s", "song", "guitar.wav")) +
                             S.L.load(os.path.join(root, "ref", "stems", "htdemucs_6s", "song", "bass.wav")), 2.0, 4.0)
                self.assertTrue(np.allclose(ref, want))
            finally:
                M.ROOT, S.ROOT = old_m, old_s


if __name__ == "__main__":
    unittest.main()
