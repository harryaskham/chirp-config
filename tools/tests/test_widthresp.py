#!/usr/bin/env python3
"""Width-stage response model and joint fitting (bd-33c6c3): the model is exact for the engine's stage, the bands
are coupled (lower-edge semantics, 12 dB/oct overlapping crossovers), and fitting all seven widths together on the
model reaches a target the per-band ratio rule cannot.

  python3 tools/tests/test_widthresp.py           (from ~/.config/chirp; engine tests need $CHIRP or the pinned
                                                   /tmp/lt/pins/chirp-a931418, else they are skipped)
"""
import os
import sys
import unittest
import warnings

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import likeness as L  # noqa: E402
import widthresp as WR  # noqa: E402

MM = [6, 0.364, 1.533, 1.251, 1.951, 4.215, 4.493]   # Mind's Mirrors v14 tail (chirper-three, mm-r16)
CHIRP = WR.CHIRP


class Model(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        self.f = np.linspace(1, WR.SR / 2, 8193)
        self.white = np.ones_like(self.f)

    def test_unity_is_exactly_neutral(self):
        self.assertLess(np.abs(WR.response(self.f, [1] * 7) - 1).max(), 1e-12)
        self.assertLess(np.abs(WR.response(self.f, [1] * 7, mono_below=0) - 1).max(), 1e-12)

    def test_lower_edge_semantics_and_their_ripple(self):
        # wb6 (8 kHz) scales the side from 8 kHz up — but the cascade's pieces are not phase-aligned, so a band's
        # change ripples two octaves down: wb6 = 2 dips 2 kHz to x0.70 (-3.1 dB) and overshoots to x2.28 at 8-12 kHz
        f = np.array([200.0, 500.0, 2000.0, 6000.0, 10000.0, 20000.0])
        h = np.abs(WR.response(f, [1, 1, 1, 1, 1, 1, 2]))
        self.assertLess(np.abs(h[:2] - 1).max(), 0.01, "the bass is untouched")
        self.assertLess(h[2], 0.75, "the dip below the crossover")
        self.assertTrue((h[3:] > 1.9).all(), h)

    def test_bands_are_coupled_at_the_mm_tail(self):
        g = WR.band_ratios(self.f, self.white * np.abs(WR.response(self.f, MM)) ** 2, self.white)
        # measured 1.2-3.5k answers wb5 more than its own wb4; 400-1.2k reads x1.57 though wb3 is 1.25
        J = WR.jacobian(self.f, self.white, self.white, MM)
        self.assertGreater(J[4, 5], J[4, 4])
        self.assertAlmostEqual(g[4], 4.0, delta=0.05)

    def test_the_small_solver_needs_no_lapack(self):
        A = np.array([[4.0, 1, 0], [1, 3, 1], [0, 1, 2]])
        x = WR._solve(A, np.array([1.0, 2, 3]))
        self.assertTrue(np.allclose(A @ x, [1, 2, 3]))

    def test_joint_fit_reaches_what_per_band_ratios_miss(self):
        # the record's S/M: the MM widths applied to a white side; the render: unity widths
        target = WR.band_ratios(self.f, self.white * np.abs(WR.response(self.f, MM)) ** 2, self.white)
        now = WR.band_ratios(self.f, self.white, self.white)
        per_band = np.clip(np.ones(7) * target / now, 0.1, 8)
        joint = WR.fit_joint(self.f, self.white, self.white, np.ones(7), target, lo=0.1, hi=8, cap=8)
        term = lambda w: WR.stereo_term(WR.predict_ratios(self.f, self.white, self.white, np.ones(7), w), target)  # noqa: E731
        self.assertGreater(term(joint), 99.0)
        self.assertGreater(term(joint), term(per_band) + 2, f"joint {term(joint):.1f} vs per-band {term(per_band):.1f}")


@unittest.skipUnless(os.access(CHIRP, os.X_OK), "no chirp build")
class Engine(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)

    def test_probe_matches_the_model(self):
        (peak, rms), meas, model = WR.probe(CHIRP, MM)
        self.assertLessEqual(peak, 1.0, "unity stage vs no stage: at most one 16-bit step")
        self.assertLess(rms, 0.05)
        err = np.abs(20 * np.log10(model / meas))
        self.assertLess(err[2:].max(), 0.01, err)   # 150 Hz up; the 20/60 Hz bands are within Welch resolution
        self.assertLess(err.max(), 0.25, err)

    def test_multisine_tones_match_the_model(self):
        rows = WR.tone_probe(CHIRP, MM, [40, 250, 1500, 4500, 11000])
        for t, m_, h in rows:
            self.assertAlmostEqual(20 * np.log10(h / m_), 0, delta=0.01, msg=f"{t} Hz")


if __name__ == "__main__":
    unittest.main(verbosity=2)
