#!/usr/bin/env python3
"""tools/secsim.py (chirper-zero's): which of the scorer's sections return, and compscore's ON THE EDGE note.

Hermetic: made sections (a `vec` each, as compscore's section features carry) with known likenesses.

  python3 tools/tests/test_secsim.py      (from ~/.config/chirp; under a second)
"""
import os
import sys
import unittest

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import compscore as cs  # noqa: E402
import secsim as S  # noqa: E402


def sec(a, b, vec):
    return {"a": float(a), "b": float(b), "vec": np.array(vec, float)}


# A B C A' B'' : the fourth is the first again (cosine 1.0), the fifth is B at an angle (cosine 0.6: half a return)
A, B, C = [1, 0, 0], [0, 1, 0], [0, 0, 1]
SECS = [sec(0, 10, A), sec(10, 30, B), sec(30, 45, C), sec(45, 60, A), sec(60, 80, [0, 0.6, 0.8])]


class Returns(unittest.TestCase):
    def test_each_section_and_its_best_earlier_non_adjacent_match(self):
        share, line = S.returns(SECS)
        self.assertEqual(line, ["0[0-10s]", "1[10-30s]", "2[30-45s]~0:0.00", "3[45-60s]~0:1.00", "4[60-80s]~2:0.80"])
        # the fifth's neighbour (the fourth) is not counted; of 0, 1, 2 it is most like C (0.8), not B (0.6)
        self.assertAlmostEqual(share, (0.0 + 1.0 + 1.0) / 3)                    # 0.8 is past 0.75: a full return
        share, line = S.returns(SECS[:4] + [sec(60, 80, [0.8, 0.6, 0])])         # most like A (0.8) again
        self.assertEqual(line[-1], "4[60-80s]~0:0.80")
        half = [sec(0, 1, A), sec(1, 2, B), sec(2, 3, [0.6, 0, 0.8])]            # 0.6 against A: halfway up 0.45..0.75
        self.assertAlmostEqual(S.returns(half)[0], 0.5)

    def test_too_few_sections_have_no_share(self):
        self.assertEqual(S.returns(SECS[:2]), (None, ["0[0-10s]", "1[10-30s]"]))
        self.assertEqual(S.returns([]), (None, []))


class Edge(unittest.TestCase):
    def test_the_band_is_the_albums(self):
        self.assertEqual(cs.recurrence_band({"params": {"recurrence": {"band": [0.25, 0.9]}}}), (0.25, 0.9))
        self.assertEqual(cs.recurrence_band({}), (0.25, 0.7))
        self.assertEqual(cs.recurrence_band(None), (0.25, 0.7))

    def test_a_share_inside_the_band_and_close_to_its_end_is_on_the_edge(self):
        self.assertEqual(cs.on_edge(0.252, 0.25, 0.9), "floor")                  # Plain Hunt v5, seed 0
        self.assertEqual(cs.on_edge(0.27, 0.25, 0.9), "floor")
        self.assertEqual(cs.on_edge(0.288, 0.25, 0.9), "")
        self.assertEqual(cs.on_edge(0.89, 0.25, 0.9), "ceiling")
        self.assertEqual(cs.on_edge(0.224, 0.25, 0.9), "")                       # outside: the term already says so
        self.assertEqual(cs.on_edge(None, 0.25, 0.9), "")

    def test_the_note_names_the_cuts_on_the_edge_and_is_silent_otherwise(self):
        self.assertEqual(cs.edge_note([0.38, 0.318, 0.288], 0.25, 0.9), "")
        note = cs.edge_note([0.38, 0.252, 0.252, 0.288, None], 0.25, 0.9)
        self.assertTrue(note.startswith("ON THE EDGE: recurrence share 0.252 (the floor, 0.25), 0.252 (the floor, 0.25) on 2 of 5 cut(s)"))
        self.assertIn("0.895 (the ceiling, 0.9) on 1 of 1", cs.edge_note([0.895], 0.25, 0.9))


if __name__ == "__main__":
    unittest.main()
