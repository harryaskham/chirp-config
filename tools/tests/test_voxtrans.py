#!/usr/bin/env python3
"""tools/voxtrans.py: a sung line whose 3rd harmonic dominates (Hetfield's ~930 Hz formant) transcribes to its
fundamentals with SHS; silence gives no notes.

  python3 tools/tests/test_voxtrans.py      (from ~/.config/chirp; a few seconds)
"""
import os
import sys
import unittest

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import voxtrans as V  # noqa: E402


def sung(midis, dur=0.6, gap=0.15):
    """Notes with harmonics 1..8, the 3rd 4x louder than the fundamental (a strong formant), short gaps."""
    out = []
    t = np.arange(int(dur * V.SR)) / V.SR
    for m in midis:
        f = 440 * 2 ** ((m - 69) / 12)
        x = sum((4.0 if h == 3 else 1.0 / h) * np.sin(2 * np.pi * f * h * t) for h in range(1, 9))
        env = np.minimum(1, np.minimum(t, dur - t) * 30)
        out += [0.05 * x * env, np.zeros(int(gap * V.SR))]
    return np.concatenate(out)


class VoxTrans(unittest.TestCase):
    def test_shs_names_the_fundamentals_despite_a_loud_third_harmonic(self):
        line = [52, 55, 57, 59, 55]                       # E3 G3 A3 B3 G3 (165-247 Hz)
        x = sung(line)
        f0, lev, loud = V.f0_track(x)
        notes = V.notes_of(f0, lev, loud)
        self.assertEqual([n["pitch"] for n in notes], line)
        self.assertTrue(all(0.4 < n["len"] < 0.7 for n in notes))

    def test_silence_gives_no_notes(self):
        f0, lev, loud = V.f0_track(np.zeros(V.SR * 2))
        self.assertEqual(V.notes_of(f0, lev, loud), [])


if __name__ == "__main__":
    unittest.main()
