#!/usr/bin/env python3
"""chirpbin.resolve: $CHIRP, else the adopted groove pin, else the tool's old default with a warning.

  python3 tools/tests/test_chirpbin.py      (from ~/.config/chirp; instant)
"""
import contextlib
import importlib.util
import io
import os
import shutil
import stat
import tempfile
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(tools_dir):
    spec = importlib.util.spec_from_file_location("chirpbin_test", os.path.join(tools_dir, "chirpbin.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


class Resolve(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="chirpbin-")
        self.addCleanup(shutil.rmtree, self.dir, True)
        shutil.copy(os.path.join(TOOLS, "chirpbin.py"), self.dir)
        self.pin = os.path.join(self.dir, "chirp-pin")
        with open(self.pin, "w") as f:
            f.write("#!/bin/sh\n")
        os.chmod(self.pin, os.stat(self.pin).st_mode | stat.S_IXUSR)
        self.saved = os.environ.pop("CHIRP", None)
        self.addCleanup(lambda: os.environ.__setitem__("CHIRP", self.saved) if self.saved else os.environ.pop("CHIRP", None))
        self.m = load(self.dir)

    def write_pin(self, text):
        with open(os.path.join(self.dir, "groove-pin"), "w") as f:
            f.write(text)

    def test_chirp_env_wins(self):
        self.write_pin(self.pin + "\n")
        os.environ["CHIRP"] = "/explicit/chirp"
        self.assertEqual(self.m.resolve("/old/default"), "/explicit/chirp")

    def test_the_adopted_groove_pin_is_the_default(self):
        self.write_pin(self.pin + "\n")
        self.assertEqual(self.m.resolve("/old/default"), self.pin)

    def test_no_usable_pin_keeps_the_old_default_and_says_so(self):
        for text in (None, "/no/such/binary\n"):
            if text is not None:
                self.write_pin(text)
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                self.assertEqual(self.m.resolve("/old/default"), "/old/default")
            self.assertIn("set CHIRP", err.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
