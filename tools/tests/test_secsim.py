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

    def test_what_changed_names_the_seam_that_went(self):
        # before: A B C A B (both the fourth and the fifth return). After: the last seam is gone, and A+B together is
        # like neither as it was (cosine 0.71 with A: 0.86 of a return)
        before = [sec(0, 10, A), sec(10, 30, B), sec(30, 45, C), sec(45, 60, A), sec(60, 80, B)]
        after = [sec(0, 10, A), sec(10, 30, B), sec(30, 44, C), sec(44, 80, [1, 1, 0])]
        self.assertEqual(S.seams(before, after), {"gone": [60.0], "new": [], "moved": []})       # 45 -> 44 is the same seam
        self.assertEqual(S.seams(before, [sec(0, 10, A), sec(10, 38, B), sec(38, 60, C), sec(60, 70, A), sec(70, 80, B)]),
                         {"gone": [45.0], "new": [70.0], "moved": [(30.0, 38.0)]})             # 38 is the seam from 30; 45 has no
        lines = S.changed(before, after, S.returns(before)[1], S.returns(after)[1])              # other within 12 s that is free
        self.assertEqual(lines, ["the seam at 60 s is GONE: 3[45-60s]~0:1.00 and 4[60-80s]~1:1.00 are now one section "
                                 "3[44-80s]~0:0.71: it counts once where it counted twice"])
        split = S.changed(after, before, S.returns(after)[1], S.returns(before)[1])
        self.assertEqual(split, ["a NEW seam at 60 s: 3[44-80s]~0:0.71 is now 3[45-60s]~0:1.00 and 4[60-80s]~1:1.00"])
        less = before[:4] + [sec(60, 80, [0, 0.6, 0.8])]                                      # the fifth now half like B
        self.assertEqual(S.changed(before, less, S.returns(before)[1], S.returns(less)[1]), [])   # 0.8 still counts whole
        half = before[:4] + [sec(60, 80, [0, 0.6, 0.8])]
        half[2] = sec(30, 45, [0, 0, -1])                                                     # ... and now 0.6 is its best: half
        self.assertEqual(S.changed(before, half, S.returns(before)[1], S.returns(half)[1]),
                         ["4[60-80s]~1:1.00 -> 4[60-80s]~1:0.60: it returns LESS (1.00 -> 0.50 of a return)"])

    def test_the_term_is_the_mean_of_the_cuts_and_says_which_is_short(self):
        self.assertEqual(S.term_line([100.0, 100.0], [0.3, 0.4], 0.25, 0.45), "THE TERM: 100.0, the mean of the cuts' 100.0 100.0")
        self.assertEqual(S.term_line([100.0, 74.5, 100.0], [0.3, 0.206, 0.4], 0.25, 0.45),
                         "THE TERM: 91.5, the mean of the cuts' 100.0 74.5 100.0; under 100: cut 2 at 74.5 (share 0.206, under the "
                         "floor 0.25)")
        self.assertIn("over the ceiling 0.45", S.term_line([80.0], [0.5], 0.25, 0.45))
        self.assertEqual(S.term_line([None, 100.0], [None, 0.3], 0.25, 0.45), "")
        before = [sec(0, 10, A), sec(10, 30, B), sec(30, 45, C), sec(45, 60, A), sec(60, 80, B)]
        after = [sec(0, 10, A), sec(10, 30, B), sec(30, 44, C), sec(44, 80, [1, 1, 0])]

        def reading(name, sets, scores):
            got = [S.returns(x) for x in sets]
            return {"name": name, "sets": sets, "lines": [g[1] for g in got], "shares": [g[0] for g in got], "scores": scores}
        a, b = reading("v1.wav", [before, before], [100.0, 100.0]), reading("v2.wav", [before, after], [100.0, 74.5])
        lines = S.what_changed(a, b)
        self.assertEqual(lines[0], "WHAT CHANGED, v1.wav -> v2.wav: the term 100.0 -> 87.2")
        self.assertEqual(lines[1], "  cut 2 (n=5 -> 4): 100.0 -> 74.5 (share 0.667 -> 0.429)")
        self.assertTrue(lines[2].startswith("      the seam at 60 s is GONE: "))
        self.assertEqual(lines[-1], "  the other 1 cut(s) score the same before and after (their shares moved +0.000 to +0.000)")
        same = S.what_changed(a, a)
        self.assertEqual(same, ["WHAT CHANGED, v1.wav -> v1.wav: the term 100.0 -> 100.0",
                                "  the 2 cut(s) score the same before and after (their shares moved +0.000 to +0.000)"])
        self.assertEqual(S.what_changed(a, reading("v3.wav", [before], [100.0])), [])            # not the same cuts: nothing said

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
