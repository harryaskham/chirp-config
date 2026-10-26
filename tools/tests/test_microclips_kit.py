#!/usr/bin/env python3
"""tools/microclips.py --kit-std: a struck kit swings in level between hits; a sustained roll does not.

  python3 tools/tests/test_microclips_kit.py      (from ~/.config/chirp; instant)
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

SR = M.L.SR


def write(root, cid, x):
    d = os.path.join(root, "ref", "stems", "htdemucs_6s", cid)
    os.makedirs(d)
    with wave.open(os.path.join(d, "drums.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


class Kit(unittest.TestCase):
    def test_kit_swings_roll_does_not(self):
        rng = np.random.default_rng(0)
        t = np.arange(8 * SR) / SR
        kit = 0.5 * rng.normal(size=len(t)) * np.exp(-((t % 0.25) / 0.03))          # a hit every 250 ms, 30 ms decay
        roll = 0.3 * rng.normal(size=len(t)) * (1 + 0.2 * np.sin(2 * np.pi * 2.5 * t))   # sustained, slow strokes
        with tempfile.TemporaryDirectory() as root:
            write(root, "kit", kit)
            write(root, "roll", roll)
            old, M.ROOT = M.ROOT, root
            try:
                self.assertGreater(M.envelope_std("kit", 0, 8), 6)
                self.assertLess(M.envelope_std("roll", 0, 8), 6)
            finally:
                M.ROOT = old


if __name__ == "__main__":
    unittest.main()
