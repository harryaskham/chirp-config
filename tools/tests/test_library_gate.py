#!/usr/bin/env python3
"""climb.py commit / done --with carrying library files go through libguard (10 Nov): refused when a song outside the
album in progress would change, held until --library-ok when another composer's song would, free under a new name.

  python3 tools/tests/test_library_gate.py     (from ~/.config/chirp; a temp registry and git repo, a stand-in engine)
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
# stand-in for `chirp plan -f SONG --json`: canonical = the song's words and the library files they name
import json, os, sys
song = sys.argv[sys.argv.index("-f") + 1]
cfg = os.path.dirname(os.environ["CHIRP_CONFIG"])
words = open(song).read().split()
lib = {}
for w in words:
    p = os.path.join(cfg, "patches", w + ".yaml")
    if os.path.exists(p):
        lib[w] = open(p).read()
print(json.dumps({"data": {"canonical": {"words": words, "lib": lib}}}))
'''


class LibraryGate(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="libgate-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        for d in ("songs", "patches"):
            os.makedirs(os.path.join(self.root, d))
        self.w("patches/bass.yaml", "bass v1\n")
        self.w("patches/lead.yaml", "lead v1\n")
        self.w("songs/old.yaml", "bass\n")                    # a released album's song
        self.w("songs/a.yaml", "lead\n")                      # the album in progress: ann's
        self.w("songs/b.yaml", "lead\n")                      # ... and bob's
        mk = lambda i, album, owner=None: {"id": i, "status": "active", "rounds": 3, "owner": owner,   # noqa: E731
                                           "song": f"songs/{i}.yaml", "mode": "compose", "meta": {"album": album},
                                           "best": {"score": 90.0, "version": "v3"}}
        self.w("climbs.json", json.dumps({"focus": "Now", "climbs": [mk("old", "Then"), mk("a", "Now", "ann"),
                                                                     mk("b", "Now", "bob")]}))
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

    def climb(self, *args, who=None):
        env = {**os.environ, "CLIMB_ROOT": self.root, "CLIMB_STARTS": os.path.join(self.root, "starts.jsonl"),
               "CHIRP": self.engine, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
               "GIT_COMMITTER_EMAIL": "t@t"}
        env.pop("CLIMB_AS", None)
        if who:
            env["CLIMB_AS"] = who
        return subprocess.run([sys.executable, os.path.join(TOOLS, "climb.py"), *args], capture_output=True, text=True,
                              env=env)

    def registry(self):
        with open(os.path.join(self.root, "climbs.json")) as f:
            return json.load(f)

    def commits(self):
        return int(self.git("rev-list", "--count", "HEAD").strip())

    def test_an_edit_that_changes_a_released_song_is_refused(self):
        self.w("patches/bass.yaml", "bass v2\n")
        r = self.climb("commit", "-m", "louder bass", "patches/bass.yaml", "--library-ok")
        self.assertEqual(r.returncode, 5, r.stderr)
        self.assertIn("REFUSED", r.stderr)
        self.assertIn("old", r.stderr)
        self.assertEqual(self.commits(), 1)                    # nothing committed, even with --library-ok

    def test_the_same_change_under_a_new_name_is_free(self):
        self.w("patches/bass-2.yaml", "bass v2\n")
        r = self.climb("commit", "-m", "bass-2", "patches/bass-2.yaml")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.commits(), 2)

    def test_another_composers_song_holds_until_library_ok(self):
        self.w("patches/lead.yaml", "lead v2\n")
        r = self.climb("commit", "-m", "brighter lead", "patches/lead.yaml", who="ann")
        self.assertEqual(r.returncode, 5, r.stderr)
        self.assertIn("HELD", r.stderr)
        self.assertIn("b (bob)", r.stderr)
        self.assertNotIn("a (ann)", r.stderr)                  # her own song may change
        self.assertEqual(self.commits(), 1)
        r = self.climb("commit", "-m", "brighter lead", "patches/lead.yaml", "--library-ok", who="ann")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.commits(), 2)
        self.assertEqual(self.git("show", "--name-only", "--format=", "HEAD").split(), ["patches/lead.yaml"])

    def test_done_with_a_library_file_is_gated_before_the_round_is_recorded(self):
        self.w("patches/bass.yaml", "bass v2\n")
        self.w("songs/a.yaml", "lead bass\n")
        r = self.climb("done", "a", "--as", "ann", "--note", "new bass", "--score", "91", "--version", "v4",
                       "--with", "songs/a.yaml", "patches/bass.yaml")
        self.assertEqual(r.returncode, 5, r.stderr)
        self.assertIn("REFUSED", r.stderr)
        reg = self.registry()
        self.assertEqual(reg["climbs"][1]["rounds"], 3)        # no round recorded
        self.assertEqual(self.commits(), 1)

    def test_done_with_only_your_own_song_changing_passes(self):
        self.w("patches/solo.yaml", "solo v1\n")
        self.w("songs/a.yaml", "lead solo\n")
        r = self.climb("done", "a", "--as", "ann", "--note", "a solo", "--score", "91", "--version", "v4",
                       "--with", "songs/a.yaml", "patches/solo.yaml")
        self.assertEqual(r.returncode, 0, r.stderr)
        reg = self.registry()
        self.assertEqual(reg["climbs"][1]["rounds"], 4)

    def test_paths_without_library_files_never_run_the_guard(self):
        self.w("songs/a.yaml", "lead lead\n")
        os.chmod(self.engine, 0)                               # an engine that cannot run: the guard is not consulted
        r = self.climb("commit", "-m", "song only", "songs/a.yaml")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.commits(), 2)


if __name__ == "__main__":
    unittest.main()
