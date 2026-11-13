#!/usr/bin/env python3
"""tools/galone.py: where a guitar plays alone on a record (chirper-zero's, Common Time v30).

Hermetic: stems made of noise; the drums stop for three seconds, the bass only drops 10 dB there.

  python3 tools/tests/test_galone.py      (from ~/.config/chirp; a second)
"""
import contextlib
import io
import os
import shutil
import sys
import tempfile
import unittest
import wave

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import galone as G  # noqa: E402

SR = 8000


def stem(root, rec, name, gains, seed):
    """One second a gain (linear), of noise at -20 dBFS times that gain."""
    path = os.path.join(root, "ref", "stems", "bs_roformer_sw", rec, name + ".wav")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    x = np.concatenate([np.random.default_rng(seed + i).standard_normal(SR) * 0.1 * g for i, g in enumerate(gains)])
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


class Galone(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="galone-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self.old = G.ROOT
        G.ROOT = self.root
        self.addCleanup(lambda: setattr(G, "ROOT", self.old))

    def run_tool(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = G.main(list(argv))
        return code, out.getvalue()

    def test_a_passage_where_everything_else_stops(self):
        stem(self.root, "rec", "guitar", [1] * 10, 1)
        stem(self.root, "rec", "drums", [1, 1, 1, 1, 0, 0, 0, 1, 1, 1], 100)        # silent from 4 s to 7 s
        stem(self.root, "rec", "bass", [1, 1, 1, 1, 0.001, 0.001, 0.001, 1, 1, 1], 200)   # 60 dB down there
        code, text = self.run_tool("rec")
        self.assertEqual(code, 0)
        self.assertRegex(text, r"^rec +guitar's loud level -(19|20)\.\d dBFS; 1 passage\(s\): 4\.0 s for 3\.0 s "
                               r"\(others (59|6\d) dB under; guitar [+-]0 re loud\)\n$")

    def test_clear_and_min_decide_what_counts(self):
        stem(self.root, "rec", "guitar", [1] * 10, 1)
        stem(self.root, "rec", "drums", [1, 1, 1, 1, 0.3, 0.3, 0.3, 1, 1, 1], 100)   # only 10 dB under from 4 s to 7 s
        _, text = self.run_tool("rec")
        self.assertIn("0 passage(s)", text)
        _, text = self.run_tool("rec", "--clear", "8")
        self.assertIn("1 passage(s): 4.0 s for 3.0 s (others 10 dB under", text)
        _, text = self.run_tool("rec", "--clear", "8", "--min", "4")
        self.assertIn("0 passage(s)", text)

    def test_a_quiet_guitar_alone_does_not_count(self):
        """The guitar is alone from 4 s to 7 s but 20 dB under its loud level: not a passage to read a tone from."""
        stem(self.root, "rec", "guitar", [1, 1, 1, 1, 0.1, 0.1, 0.1, 1, 1, 1], 1)
        stem(self.root, "rec", "drums", [1, 1, 1, 1, 0, 0, 0, 1, 1, 1], 100)
        _, text = self.run_tool("rec")
        self.assertIn("0 passage(s)", text)

    def test_records_without_a_guitar_stem_are_said_and_no_arguments_is_the_help(self):
        stem(self.root, "nog", "drums", [1] * 4, 1)
        stem(self.root, "solo", "guitar", [1] * 4, 1)
        _, text = self.run_tool("nog", "nosuch", "solo")
        self.assertEqual(text.splitlines(), ["nog no guitar stem", "nosuch no guitar stem", "solo no other stem to be alone from"])
        code, text = self.run_tool()
        self.assertEqual(code, 2)
        self.assertIn("galone.py ID...", text)


if __name__ == "__main__":
    unittest.main()
