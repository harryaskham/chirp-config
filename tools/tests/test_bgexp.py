#!/usr/bin/env python3
"""bgexp jobs always end terminal (bd-1a4f0e): whatever fails — a missing sections file after a good render, a
missing binary, a failed render, unusable scorer output — the job records `failed` with its stage and error, keeps
a completed render, and `done` jobs still score and clean up as before. No chirp process runs (subprocess is mocked).

  python3 tools/tests/test_bgexp.py            (from ~/.config/chirp; ~1 s)
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import io
import unittest
from contextlib import redirect_stdout
import wave
from unittest import mock

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("bgexp_under_test", os.environ.get("BGEXP", os.path.join(TOOLS, "bgexp.py")))
B = importlib.util.module_from_spec(spec)
spec.loader.exec_module(B)


def tiny_wav(path):
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(48000)
        w.writeframes(bytes(480 * 4))


class Jobs(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="bgexp-test-")
        self.addCleanup(shutil.rmtree, self.dir, True)
        self.old = (B.ROOT, B.EXP, B.CHIRP)
        self.addCleanup(lambda: setattr(B, "ROOT", self.old[0]) or setattr(B, "EXP", self.old[1]) or setattr(B, "CHIRP", self.old[2]))
        B.ROOT, B.EXP, B.CHIRP = self.dir, os.path.join(self.dir, "jobs"), sys.executable
        self.song = os.path.join(self.dir, "song.yaml")
        with open(self.song, "w") as f:
            f.write('{"tempo": 120, "tracks": []}\n')
        self.ref = os.path.join(self.dir, "ref.wav")
        tiny_wav(self.ref)
        self.secs = os.path.join(self.dir, "sections.txt")
        with open(self.secs, "w") as f:
            f.write("0,0.01\n")

    def run_job(self, render_rc=0, likeness_out=None, sections=None, keep_wav=False):
        lk = likeness_out if likeness_out is not None else json.dumps(
            {"total": 70.5, "total_raw": 70.4987, "sections": [{"start": 0, "end": 0.01, "total": 70.5, "loudness": 80.0}]})

        def fake_run(cmd, **kw):
            if "render" in cmd:
                tiny_wav(cmd[cmd.index("-o") + 1])
                return subprocess.CompletedProcess(cmd, render_rc, "", "")
            if any("likeness.py" in str(c) for c in cmd):
                return subprocess.CompletedProcess(cmd, 0, lk, "")
            if any("mixfeel.py" in str(c) for c in cmd):
                return subprocess.CompletedProcess(cmd, 0, "{}", "")
            return subprocess.CompletedProcess(cmd, 0, "chirp 0.1.0", "")

        with mock.patch.object(B.subprocess, "run", side_effect=fake_run):
            B.job("j", self.song, self.ref, sections or self.secs, 1, [], max_load=1e9, keep_wav=keep_wav)
        with open(os.path.join(B.EXP, "j.json")) as f:
            return json.load(f)

    def wav(self):
        return os.path.exists(os.path.join(B.EXP, "j.wav"))

    def test_missing_sections_after_a_good_render_fails_and_keeps_the_render(self):
        st = self.run_job(sections=os.path.join(self.dir, "MISSING.txt"))
        self.assertEqual((st["state"], st["stage"]), ("failed", "scoring"), st)
        self.assertIn("FileNotFoundError", st["error"])
        self.assertTrue(self.wav(), "the completed render is kept")
        self.assertIn("finished", st)
        with open(os.path.join(B.EXP, "j.log")) as f:
            self.assertIn("Traceback", f.read())

    def test_a_failure_before_rendering_is_terminal(self):
        B.CHIRP = os.path.join(self.dir, "no-such-chirp")
        st = self.run_job()
        self.assertEqual(st["state"], "failed", st)
        self.assertIn("FileNotFoundError", st["error"])

    def test_a_failed_render_fails_without_a_wav(self):
        st = self.run_job(render_rc=1)
        self.assertEqual((st["state"], st["stage"]), ("failed", "rendering"), st)
        self.assertFalse(self.wav())

    def test_unusable_scores_fail_and_keep_the_render(self):
        st = self.run_job(likeness_out="not json")
        self.assertEqual((st["state"], st["stage"]), ("failed", "scoring"), st)
        self.assertTrue(self.wav())

    def test_success_scores_and_cleans_up(self):
        st = self.run_job()
        self.assertEqual(st["state"], "done", st)
        self.assertEqual(st["total"], 70.5)
        self.assertIn("legacy", st["conventions"]["exact"])
        self.assertEqual(st["total_raw"], 70.4987, "the raw total is recorded as given")
        self.assertFalse(self.wav(), "deleted after scoring")
        st = self.run_job(keep_wav=True)
        self.assertEqual(st["state"], "done")
        self.assertTrue(self.wav(), "--keep-wav keeps it")

    def test_a_short_render_is_flagged(self):
        lk = json.dumps({"total": 70.5, "sections": [{"start": 0, "end": 0.01, "total": 70.5}],
                         "coverage": {"complete": False, "candidate_seconds": 9.5, "requested_end": 10.0, "short_sections": [1]}})
        st = self.run_job(likeness_out=lk)
        self.assertEqual(st["state"], "done")
        self.assertFalse(st["coverage"]["complete"])
        out = io.StringIO()
        with redirect_stdout(out):
            B.status()
        self.assertIn("SHORT: render 9.5 s < sections 10.0 s", out.getvalue())

    def test_the_cli_refuses_missing_inputs_before_forking(self):
        r = subprocess.run([sys.executable, os.path.join(TOOLS, "bgexp.py"), "run", "x", self.song,
                            "--sections", "tools/NO-SUCH-sections.txt"], capture_output=True, text=True,
                           env={**os.environ, "BGEXP_DIR": os.path.join(self.dir, "cli")})
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("does not exist", r.stderr)
        self.assertFalse(os.path.exists(os.path.join(self.dir, "cli", "x.json")), "no job was queued")


if __name__ == "__main__":
    unittest.main(verbosity=2)
