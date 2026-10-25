#!/usr/bin/env python3
"""tools/stemvowels.py --style builtin: the vowel axis maps onto the built-in voice's ^u / ^i marks exactly.

  python3 tools/tests/test_stemvowels_style.py      (from ~/.config/chirp; instant)
"""
import os
import sys
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import stemvowels as S  # noqa: E402


class Style(unittest.TestCase):
    def test_default_is_vow(self):
        self.assertEqual(S.mark(0.3), "^vow=0.3")

    def test_builtin_marks_reach_the_same_axis_value(self):
        # the built-in voice: vowel = 0.5 - 0.5*u + 0.5*i
        for v in (0.0, 0.25, 0.4, 0.6, 0.75, 1.0):
            m = S.mark(v, "builtin")
            u = float(m[3:]) if m.startswith("^u=") else 0.0
            i = float(m[3:]) if m.startswith("^i=") else 0.0
            self.assertAlmostEqual(0.5 - 0.5 * u + 0.5 * i, v, places=3)
        self.assertEqual(S.mark(0.5, "builtin"), "")      # 'ah' is the default: no mark


if __name__ == "__main__":
    unittest.main()
