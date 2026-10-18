#!/usr/bin/env python3
"""tab2song's drum remap/drop (bd-77908e): settings in a bar (swing=, vel=, gate=, bend=, ccN=) pass through untouched,
while pieces are still renamed, deduplicated and dropped (a fully dropped hit becomes a rest of its length).

  python3 tools/tests/test_remap.py              (from ~/.config/chirp; instant)
"""
import importlib.util
import os
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tab2song_remap", os.path.join(TOOLS, "tab2song.py"))
T = importlib.util.module_from_spec(spec)
spec.loader.exec_module(T)


class Remap(unittest.TestCase):
    def test_settings_pass_through(self):
        line = "swing=.666 vel=100 gate=0.5 bend=2 cc64=127 k,h1/0.5b@100 s/0.5b R/1b"
        self.assertEqual(T.remap_drums(line, {"h1": "h"}, set()),
                         "swing=.666 vel=100 gate=0.5 bend=2 cc64=127 k,h/0.5b@100 s/0.5b R/1b")

    def test_pieces_are_renamed_deduplicated_and_dropped(self):
        self.assertEqual(T.remap_drums("h1,h2/0.25b@90 cow/0.25b@80 _/0.5b", {"h1": "h", "h2": "h"}, {"cow"}),
                         "h/0.25b@90 R/0.25b _/0.5b")

    def test_a_line_without_settings_is_unchanged_from_before(self):
        line = "k,s/0.5b@110 h1/0.25b@70 R/0.25b rd/1b@90"
        self.assertEqual(T.remap_drums(line, {"h1": "h", "rd": "r"}, {"x"}), "k,s/0.5b@110 h/0.25b@70 R/0.25b r/1b@90")


if __name__ == "__main__":
    unittest.main(verbosity=2)
