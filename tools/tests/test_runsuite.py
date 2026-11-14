#!/usr/bin/env python3
"""tools/tests/run.py: every test file in its own process, and what failed.

Hermetic: a scratch folder of four small test files, one of which fails and two of which only pass apart.

  python3 tools/tests/test_runsuite.py      (from ~/.config/chirp; a few seconds)
"""
import contextlib
import io
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run as R  # noqa: E402

FILES = {
    "test_a_sets.py": "import os\nos.environ['RUN_TEST_LEAK'] = '1'\ndef test_set():\n    assert os.environ['RUN_TEST_LEAK'] == '1'\n",
    "test_b_clean.py": "import os\ndef test_clean():\n    assert 'RUN_TEST_LEAK' not in os.environ\n",   # fails in one process with a
    "test_c_class.py": ("import unittest\nclass T(unittest.TestCase):\n    def test_one(self):\n        self.assertEqual(1, 1)\n"
                        "    @unittest.skip('later')\n    def test_two(self):\n        pass\n"),
    "test_d_bad.py": "def test_wrong():\n    assert 1 + 1 == 3\n",
    "helper.py": "raise SystemExit('not a test file')\n",
}


class Suite(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="runsuite-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        for name, text in FILES.items():
            with open(os.path.join(self.root, name), "w") as f:
                f.write(text)

    def run_tool(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = R.main(["--dir", self.root, *argv])
        return code, out.getvalue()

    def test_each_file_runs_apart_and_the_failure_is_named(self):
        code, text = self.run_tool("-j", "3")
        self.assertEqual(code, 1)
        lines = text.splitlines()
        self.assertEqual(lines[0], "FAILED test_d_bad.py (exit 1)")
        self.assertTrue(any("test_d_bad.py::test_wrong" in ln for ln in lines[1:-1]))
        self.assertNotIn("test_b_clean", text)                 # it passes: test_a's environment did not reach it
        self.assertTrue(lines[-1].startswith("4 file(s), each in its own process: 3 passed, 1 failed; tests 3 passed, 1 failed, "
                                             "1 skipped; "))

    def test_words_pick_files_and_a_clean_run_exits_zero(self):
        code, text = self.run_tool("clean", "class")
        self.assertEqual(code, 0)
        self.assertTrue(text.startswith("2 file(s), each in its own process: 2 passed, 0 failed; tests 2 passed, 1 skipped; "))
        code, text = self.run_tool("--list")
        self.assertEqual((code, text.split()), (0, ["test_a_sets.py", "test_b_clean.py", "test_c_class.py", "test_d_bad.py"]))
        code, text = self.run_tool("nosuch")
        self.assertEqual((code, text.strip()), (1, "run: no test files matching nosuch"))

    def test_the_summary_line_is_read(self):
        self.assertEqual(R.counts("...\n12 passed, 2 skipped, 3 subtests passed in 1.20s\n"), {"passed": 12, "skipped": 2})
        self.assertEqual(R.counts("FAILED x\n1 failed, 4 passed, 2 errors in 0.5s"), {"failed": 1, "passed": 4, "error": 2})
        self.assertEqual(R.counts("no summary here"), {})
        self.assertEqual(R.files(self.root, ["bad"]), ["test_d_bad.py"])


if __name__ == "__main__":
    unittest.main()
