#!/usr/bin/env python3
"""climb.py commit / done --with: a song version that breaks what its picture reads is said at once, and never blocks
(10 Nov: the pictures are built on the songs' bars, track and lane names).

  python3 tools/tests/test_picture_notice.py     (from ~/.config/chirp; a temp registry and git repo, a stand-in engine)
"""
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENGINE = '''#!/usr/bin/env python3
# stand-in for `chirp vis check PROG -f SONG --json`: a programme line "reads NAME" needs the word NAME in the song
import json, sys
if sys.argv[1:3] != ["vis", "check"]:
    sys.exit(3)
prog, song = sys.argv[3], sys.argv[sys.argv.index("-f") + 1]
words = open(song).read().split()
if "!broken" in words:
    print("chirp: the song does not plan", file=sys.stderr)
    sys.exit(1)
warn = [f"track {ln.split()[1]} is not in the song" for ln in open(prog).read().splitlines()
        if ln.startswith("reads ") and ln.split()[1] not in words]
print(json.dumps({"status": "success", "data": {"ok": True, "scenes": [[0.0, "a"], [10.0, "b"]], "song_seconds": 60.0,
                                                "warnings": warn}}))
'''


class PictureNotice(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="picture-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        for d in ("songs", "vis"):
            os.makedirs(os.path.join(self.root, d))
        self.w("songs/a.yaml", "kick lights choir\n")
        self.w("songs/b.yaml", "kick\n")                      # no programme
        self.w("vis/a.yaml", "reads lights\nreads choir\nreads ghost\n")   # `ghost` was never there: an old warning
        c = lambda i: {"id": i, "status": "active", "rounds": 3, "owner": "ann", "song": f"songs/{i}.yaml",   # noqa: E731
                       "mode": "compose", "best": {"score": 90.0, "version": "v3"}}
        self.w("climbs.json", json.dumps({"climbs": [c("a"), c("b")]}))
        self.engine = os.path.join(self.root, "fake-chirp")
        self.w("fake-chirp", ENGINE)
        os.chmod(self.engine, os.stat(self.engine).st_mode | stat.S_IXUSR)
        self.git("init", "-q")
        self.git("add", "-A")
        self.git("commit", "-qm", "init")

    def w(self, rel, text):
        with open(os.path.join(self.root, rel), "w") as f:
            f.write(text)

    def git(self, *a):
        return subprocess.run(["git", "-C", self.root, "-c", "user.name=t", "-c", "user.email=t@t", *a], check=True,
                              capture_output=True, text=True).stdout

    def climb(self, *args):
        env = {**os.environ, "CLIMB_ROOT": self.root, "CLIMB_STARTS": os.path.join(self.root, "starts.jsonl"),
               "CHIRP": self.engine, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
               "GIT_COMMITTER_EMAIL": "t@t"}
        return subprocess.run([sys.executable, os.path.join(TOOLS, "climb.py"), *args], capture_output=True, text=True,
                              env=env)

    def commits(self):
        return int(self.git("rev-list", "--count", "HEAD").strip())

    def test_a_renamed_track_the_picture_reads_is_said_and_the_commit_goes_through(self):
        self.w("songs/a.yaml", "kick lights2 choir\n")
        r = self.climb("done", "a", "--as", "ann", "--note", "split the lights", "--score", "91", "--version", "v4",
                       "--with", "songs/a.yaml")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("NOTE for the picture (vis/a.yaml)", r.stderr)
        self.assertIn("track lights is not in the song", r.stderr)
        self.assertNotIn("ghost", r.stderr)                    # a warning that was there before is not news
        self.assertEqual(self.commits(), 2)

    def test_a_version_that_keeps_the_names_is_silent(self):
        self.w("songs/a.yaml", "kick lights choir bass\n")
        r = self.climb("commit", "-m", "a bass", "songs/a.yaml")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn("NOTE for the picture", r.stderr)

    def test_songs_without_a_programme_are_not_checked(self):
        os.chmod(self.engine, 0)                               # an engine that cannot run
        self.w("songs/b.yaml", "kick snare\n")
        r = self.climb("commit", "-m", "b", "songs/b.yaml")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn("picture", r.stderr)

    def test_a_broken_engine_never_costs_the_commit(self):
        os.chmod(self.engine, 0)
        self.w("songs/a.yaml", "kick lights2 choir\n")
        r = self.climb("commit", "-m", "a", "songs/a.yaml")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.commits(), 2)

    def test_a_version_the_programme_cannot_check_is_said(self):
        self.w("songs/a.yaml", "!broken\n")
        r = self.climb("commit", "-m", "a", "songs/a.yaml")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("it no longer checks", r.stderr)


if __name__ == "__main__":
    unittest.main()
