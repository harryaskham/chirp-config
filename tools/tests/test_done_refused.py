#!/usr/bin/env python3
"""climb.py done in compose mode: a refused trial that happens to outscore the best must not silently become the best
(chirper-three's t4 v60, 8 Nov). Kept rounds commit their song with --with; a would-be auto-keep without it stops and
asks; --refused logs the round and leaves the best alone; --keep and --refused contradict.

  python3 tools/tests/test_done_refused.py      (from ~/.config/chirp; a few seconds; a temp registry and git repo)
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DoneRefused(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="done-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        os.makedirs(os.path.join(self.root, "songs"))
        with open(os.path.join(self.root, "songs", "a.yaml"), "w") as f:
            f.write("tempo: 100\n")
        c = {"id": "a", "status": "active", "rounds": 3, "owner": "chirper-three", "song": "songs/a.yaml",
             "mode": "compose", "best": {"score": 99.5, "version": "v3"}}
        with open(os.path.join(self.root, "climbs.json"), "w") as f:
            json.dump({"climbs": [c]}, f)
        g = ["git", "-C", self.root]
        subprocess.run([*g, "init", "-q"], check=True)
        subprocess.run([*g, "-c", "user.name=t", "-c", "user.email=t@t", "add", "-A"], check=True)
        subprocess.run([*g, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "init"], check=True)

    def done(self, *args):
        env = {**os.environ, "CLIMB_ROOT": self.root, "CLIMB_STARTS": os.path.join(self.root, "starts.jsonl"),
               "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
        return subprocess.run([sys.executable, os.path.join(TOOLS, "climb.py"), "done", "a", "--as", "chirper-three",
                               "--note", "trial", *args], capture_output=True, text=True, env=env)

    def best(self):
        with open(os.path.join(self.root, "climbs.json")) as f:
            return json.load(f)["climbs"][0]["best"]

    def log(self):
        p = os.path.join(self.root, "climbs", "a.jsonl")
        return [json.loads(x) for x in open(p)] if os.path.exists(p) else []

    def test_a_higher_score_without_the_song_stops_and_records_nothing(self):
        r = self.done("--score", "99.6", "--version", "v4")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("--refused", r.stderr)
        self.assertEqual((self.best()["version"], self.log()), ("v3", []))

    def test_refused_logs_the_round_and_keeps_the_best(self):
        r = self.done("--score", "99.6", "--version", "v4", "--refused")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.best()["version"], "v3")
        self.assertEqual([(x["version"], x["kept"], x.get("refused")) for x in self.log()], [("v4", False, True)])

    def test_kept_with_the_song_becomes_the_best_as_before(self):
        with open(os.path.join(self.root, "songs", "a.yaml"), "a") as f:
            f.write("# v4\n")
        r = self.done("--score", "99.6", "--version", "v4", "--with", "songs/a.yaml")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual((self.best()["version"], self.best()["score"]), ("v4", 99.6))
        self.assertEqual([(x["version"], x["kept"]) for x in self.log()], [("v4", True)])

    def test_a_lower_score_is_refused_as_before(self):
        r = self.done("--score", "99.4", "--version", "v4")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.best()["version"], "v3")
        self.assertEqual([x["kept"] for x in self.log()], [False])

    def test_keep_and_refused_contradict(self):
        r = self.done("--score", "99.6", "--version", "v4", "--keep", "--refused")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("contradict", r.stderr)


if __name__ == "__main__":
    unittest.main()
