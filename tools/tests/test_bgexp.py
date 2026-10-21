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

    def _cli(self, *args):
        return subprocess.run([sys.executable, os.path.join(TOOLS, "bgexp.py"), "run", "x", *args], capture_output=True,
                              text=True, env={**os.environ, "BGEXP_DIR": os.path.join(self.dir, "cli")})

    def test_a_missing_song_is_named_without_blaming_explicit_defaults(self):
        r = self._cli(os.path.join(self.dir, "no-such-cand.yaml"), "--ref", "ref/shadows.wav",
                      "--sections", "tools/shadows-sections.txt")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("bgexp: song ", r.stderr)
        self.assertNotIn("default", r.stderr)

    def test_defaulted_reference_warns_for_another_song(self):
        r = self._cli(self.song, "--sections", "tools/NO-SUCH-sections.txt")
        self.assertIn("no --ref: " + os.path.basename(self.song) + " will be scored against the shadows climb's", r.stderr)
        self.assertNotIn("(the default", r.stderr, "explicit --sections is not blamed on the default")
        self.assertFalse(os.path.exists(os.path.join(self.dir, "cli", "x.json")), "no job was queued")


class CompareAndSeeds(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="bgexp-cmp-")
        self.addCleanup(shutil.rmtree, self.dir, True)
        self.old = B.EXP
        self.addCleanup(lambda: setattr(B, "EXP", self.old))
        B.EXP = self.dir

    def put(self, name, total, secs, state="done"):
        sections = [{"start": 10.0 * i, "end": 10.0 * (i + 1), "total": v, "stereo": v / 2, "chroma": 50.0}
                    for i, v in enumerate(secs)]
        with open(os.path.join(self.dir, name + ".json"), "w") as f:
            json.dump({"name": name, "state": state, "total": total, "total_raw": total, "sections": sections}, f)

    def test_compare_averages_seed_families_over_common_seeds(self):
        self.put("a-0", 50.0, [40.0, 60.0])
        self.put("a-11", 52.0, [42.0, 62.0])
        self.put("a-7", 99.0, [99.0, 99.0])          # B has no seed 7: left out
        self.put("b-0", 51.0, [44.0, 58.0])
        self.put("b-11", 55.0, [46.0, 64.0])
        self.put("b-13", 10.0, [10.0, 10.0], "failed")
        out = io.StringIO()
        with redirect_stdout(out):
            B.compare("a", "b")
        text = out.getvalue()
        self.assertIn("b vs a (seeds 0,11): total 51.000 -> 53.000  +2.000", text)
        self.assertIn("41.0 ->  45.0   +4.0", text)
        self.assertIn("stereo +2.0", text)
        self.assertIn("61.0 ->  61.0   +0.0", text)

    def test_compare_refuses_without_common_finished_jobs(self):
        self.put("a-0", 50.0, [40.0])
        self.put("b-11", 51.0, [44.0])
        with self.assertRaises(SystemExit):
            B.compare("a", "b")

    def test_run_seeds_queues_one_job_per_seed(self):
        root = tempfile.mkdtemp(prefix="bgexp-root-")
        self.addCleanup(shutil.rmtree, root, True)
        song = os.path.join(root, "cand.yaml")
        for path in (song, os.path.join(root, "ref.wav"), os.path.join(root, "secs.txt")):
            open(path, "w").close()
        out = io.StringIO()
        old_root = B.ROOT
        self.addCleanup(lambda: setattr(B, "ROOT", old_root))
        B.ROOT = root
        argv = ["bgexp.py", "run", "c7", song, "--ref", "ref.wav", "--sections", "secs.txt", "--seeds", "0,11", "--",
                "--set", "x=1"]
        with mock.patch.object(sys, "argv", argv), mock.patch.object(B.os, "fork", return_value=1) as fork, \
                mock.patch.object(B, "job") as job, redirect_stdout(out):
            B.main()
        self.assertEqual(out.getvalue().split(), ["queued", "c7-0", "queued", "c7-11"])
        self.assertEqual(fork.call_count, 2)
        job.assert_not_called()   # the parent only forks; the (mocked) children would run the jobs


if __name__ == "__main__":
    unittest.main(verbosity=2)
