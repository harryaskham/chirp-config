#!/usr/bin/env python3
"""chugmix: the low end's fall at a stroke, read on any signal (a solo, a mix, a record)."""
import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import chugmix as C  # noqa: E402


def strokes(decay_s, n=8, gap=0.25):
    """n strokes a quarter second apart: 160 Hz, each dying with the time constant decay_s (None: held)."""
    y = np.zeros(int((n * gap + 0.5) * C.SR))
    ts = [0.2 + i * gap for i in range(n)]
    for t in ts:
        k = np.arange(int(0.2 * C.SR))
        env = np.ones(len(k)) if decay_s is None else np.exp(-k / (decay_s * C.SR))
        y[int(t * C.SR):int(t * C.SR) + len(k)] += env * np.sin(2 * np.pi * 160 * k / C.SR)
    return y, ts


class Fall(unittest.TestCase):
    def test_a_held_low_end_reads_level_and_a_dying_one_positive(self):
        y, ts = strokes(None)
        f, _, n = C.fall(y, ts)
        self.assertEqual(n, 8)
        self.assertAlmostEqual(f, 0.0, delta=0.3)
        y, ts = strokes(0.03)                      # 30 ms: by 40-80 ms it is well down
        f, _, _ = C.fall(y, ts)
        self.assertGreater(f, 8.0)

    def test_it_hangs_on_the_onset(self):          # the reason for `records --scan`: read late, a dying stroke reads less
        y, ts = strokes(0.03)
        self.assertLess(C.fall(y, [t - 0.016 for t in ts])[0], C.fall(y, ts)[0] - 2)

    def test_a_stroke_at_the_edge_is_not_read(self):
        y, ts = strokes(None)
        self.assertEqual(C.fall(y, [0.001, len(y) / C.SR - 0.01])[2], 0)

    def test_the_records(self):
        self.assertEqual(len(C.RECORDS), 6)
        rec = sorted(v[5] for v in C.RECORDS.values())
        self.assertAlmostEqual(rec[0], 2.38)
        self.assertAlmostEqual(rec[-1], 4.46)
        self.assertTrue(all(abs(v[1]) < 0.7 for v in C.RECORDS.values()))     # every record's guitar holds, within 0.6 dB
        self.assertTrue(all(v[3] > 7 for v in C.RECORDS.values()))            # and every record's drums die

    def test_the_jump(self):
        y, ts = strokes(0.03)
        yb = C.D.bandpass(y, 150, 8000)
        self.assertGreater(C.jump(yb, ts), 10)
        self.assertLess(C.jump(yb, [t + 0.06 for t in ts]), 0)


if __name__ == "__main__":
    unittest.main()
