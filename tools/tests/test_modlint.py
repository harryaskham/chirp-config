#!/usr/bin/env python3
"""modlint.lint: implausible mod amounts (Hz written where octaves are meant, linear where dB is meant).

  python3 tools/tests/test_modlint.py      (from ~/.config/chirp; instant)
"""
import os
import sys
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import modlint as M  # noqa: E402


class Lint(unittest.TestCase):
    def test_hz_amount_on_a_cutoff_is_flagged(self):
        song = {"tracks": [{"filters": [{"kind": "lp", "cutoff": {"value": 3000, "mod": [{"src": "auto.cl", "amount": -2600}]}}]}]}
        self.assertEqual(M.lint(song), [("tracks.0.filters.0.cutoff", "freq", "auto.cl", -2600)])

    def test_octave_amounts_and_full_sweeps_pass(self):
        song = {"fx": [{"cutoff": {"value": 800, "mod": [{"src": "lfo.a", "amount": 2}, {"src": "env.f", "amount": -3}]}},
                       {"cutoff": {"value": 20, "mod": [{"src": "env.sfz", "amount": 11}]}},      # a library sweep
                       {"freq": {"value": 1000, "mod": [{"src": "lfo.b", "amount": 6.5}]}}]}
        self.assertEqual(M.lint(song), [])

    def test_gains_and_other_params_ignored(self):
        song = {"level": {"value": 1, "mod": [{"src": "env.ring", "amount": 90}]},       # the envelope-fade idiom
                "pan": {"value": 0, "mod": [{"src": "lfo.p", "amount": 500}]}}
        self.assertEqual(M.lint(song), [])

    def test_threshold_is_settable(self):
        song = {"cutoff": {"value": 800, "mod": [{"src": "lfo.a", "amount": 10}]}}
        self.assertEqual(M.lint(song), [])
        self.assertEqual(len(M.lint(song, octaves=8)), 1)


if __name__ == "__main__":
    unittest.main()
