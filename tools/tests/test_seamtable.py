#!/usr/bin/env python3
"""chirpers.seam_table: GFM escaped pipes stay inside a cell; a row with more cells than the header warns (chirper-two's
t6>t7 overlap read as 4 bars for four minutes on 6 Nov, silently).

  python3 tools/tests/test_seamtable.py      (from ~/.config/chirp; instant)
"""
import contextlib
import io
import os
import sys
import tempfile
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import chirpers as CH  # noqa: E402

HEAD = "| seam | overlap (bars) | swap | notes |\n|---|---|---|---|\n"


def table(rows):
    d = tempfile.mkdtemp()
    os.makedirs(os.path.join(d, "compose", "alb"))
    with open(os.path.join(d, "compose", "alb", "mixplan.md"), "w") as f:
        f.write("# mix\n\n" + HEAD + "".join(rows))
    return d


def parse(root):
    CH._WARNED.clear()
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        bars, default = CH.seam_overlaps("alb", root=root)
    return bars, err.getvalue()


class SeamTable(unittest.TestCase):
    def test_well_formed_rows_parse_silently(self):
        bars, err = parse(table(["| t1 -> t2 | 16 | mid | calm |\n", "| t2 -> t3 | 8 | no | storm |\n"]))
        self.assertEqual(bars, {(1, 2): 16.0, (2, 3): 8.0})
        self.assertEqual(err, "")

    def test_escaped_pipe_stays_in_its_cell(self):
        root = table(["| t6 -> t7 | 16 | no | D \\| Bb \\| C under the seam |\n"])
        bars, err = parse(root)
        self.assertEqual(bars, {(6, 7): 16.0})
        self.assertEqual(err, "")
        self.assertEqual(CH.seam_table("alb", root)[(6, 7)]["notes"], "D | Bb | C under the seam")

    def test_bare_pipe_in_a_cell_warns_once(self):
        root = table(["| t6 -> t7 | 4 | 16 | no | D | Bb |\n"])          # the overlap cell got split off
        bars, err = parse(root)
        self.assertIn("seam t6 -> t7 has 6 cells but the header has 4", err)
        CH.seam_overlaps("alb", root=root)                            # same process: no repeat
        self.assertEqual(err.count("t6 -> t7"), 1)


if __name__ == "__main__":
    unittest.main()
