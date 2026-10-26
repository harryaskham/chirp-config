#!/usr/bin/env python3
"""tools/microscore.py --section / --try: window and variant specs parse, bad ones are refused, and a section is
never written to the benchmark ledger.

  python3 tools/tests/test_microscore_section.py      (from ~/.config/chirp; instant)
"""
import os
import sys
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import microscore as M  # noqa: E402


class Section(unittest.TestCase):
    def test_section_spec(self):
        self.assertEqual(M.parse_section("black-cathedral:30-38"), ("black-cathedral", 30.0, 38.0))
        self.assertEqual(M.parse_section("fuel:12.5-20"), ("fuel", 12.5, 20.0))
        for bad in ("fuel", "fuel:20-12", ":1-2", "fuel:1-"):
            with self.assertRaises(SystemExit):
                M.parse_section(bad)

    def test_try_spec(self):
        self.assertEqual(M.parse_try("m8 pair: tracks.0.patch=m8-emg-l tracks.1.patch=m8-emg-r"),
                         ("m8 pair", ["tracks.0.patch=m8-emg-l", "tracks.1.patch=m8-emg-r"]))
        for bad in ("no colon", "label:", ": tracks.0.gain=1", "x: notaset"):
            with self.assertRaises(SystemExit):
                M.parse_try(bad)

    def test_never_recorded(self):
        with self.assertRaises(SystemExit) as e:
            M.main(["--section", "fuel:1-2", "--record", "x"])
        self.assertIn("never recorded", str(e.exception))


class Explain(unittest.TestCase):
    def test_missing_notes_are_named_and_bands_listed(self):
        import numpy as np
        rng = np.random.default_rng(0)
        n = 4 * M.SR
        ref = 0.3 * rng.normal(size=(n, 2))                       # a continuous wall
        cand = ref.copy()
        cand[n // 3:] = 0.0                                       # ours stops a third of the way in
        ex = M.explain(ref, cand)
        self.assertEqual(len(ex["bands"]), len(M.EXPLAIN_EDGES) - 1)
        self.assertLess(ex["silent_record"], 0.05)
        self.assertGreater(ex["silent_ours"], 0.5)
        self.assertIn("NOTES MISSING", M.explain_text(ex))
        same = M.explain(ref, ref.copy())
        self.assertNotIn("NOTES MISSING", M.explain_text(same))
        self.assertTrue(all(abs(b["diff_db"]) < 0.5 and b["corr"] > 0.99 for b in same["bands"]))


if __name__ == "__main__":
    unittest.main()
