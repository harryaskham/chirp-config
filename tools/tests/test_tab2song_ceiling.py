#!/usr/bin/env python3
"""tools/tab2song.py: a map head without a top-level ceiling gets a stderr reminder (the engine limiter otherwise
holds -1 dBFS); one with a ceiling gets none.

  python3 tools/tests/test_tab2song_ceiling.py      (from ~/.config/chirp; instant)
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tab2song as T  # noqa: E402


class Ceiling(unittest.TestCase):
    def test_missing_ceiling_is_flagged(self):
        self.assertIn("ceiling", T.ceiling_note({"master": {"fx": []}}))
        self.assertIn("ceiling", T.ceiling_note(None))

    def test_set_ceiling_is_quiet(self):
        self.assertIsNone(T.ceiling_note({"ceiling": "-0.3dB"}))


if __name__ == "__main__":
    unittest.main()
