#!/usr/bin/env python3
"""climb.py publication never stashes another agent's uncommitted work (bd-d30a90).

Real throwaway git repos under a temp dir (a bare origin, the shared tree, another clone pushing upstream changes);
nothing touches ~/.config/chirp's repository.

  python3 tools/tests/test_publish.py      (from ~/.config/chirp; seconds)
"""
import contextlib
import importlib.util
import io
import os
import shutil
import subprocess
import tempfile
import types
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load():
    spec = importlib.util.spec_from_file_location("climb_publish_test", os.path.join(TOOLS, "climb.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def run(cwd, *a):
    p = subprocess.run(["git", *a], cwd=cwd, capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(f"git {' '.join(a)}: {p.stderr}")
    return p.stdout.strip()


class Publish(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="climb-publish-test-")
        self.addCleanup(shutil.rmtree, self.dir, True)
        self.origin = os.path.join(self.dir, "origin.git")
        run(self.dir, "init", "-q", "--bare", "-b", "main", self.origin)
        seed = os.path.join(self.dir, "seed")
        run(self.dir, "clone", "-q", self.origin, seed)
        self.ident(seed)
        for name in ("ours.txt", "foreign.txt", "upstream.txt"):
            self.write(seed, name, f"{name} v0\n")
        run(seed, "add", "-A")
        run(seed, "commit", "-q", "-m", "seed")
        run(seed, "push", "-q", "origin", "HEAD:main")
        self.tree = os.path.join(self.dir, "shared")    # the agents' one working tree
        self.other = os.path.join(self.dir, "other")    # someone pushing from elsewhere
        for d in (self.tree, self.other):
            run(self.dir, "clone", "-q", self.origin, d)
            self.ident(d)
        self.C = load()
        self.C.ROOT = self.tree

    @staticmethod
    def ident(d):
        run(d, "config", "user.email", "test@example.com")
        run(d, "config", "user.name", "test")

    @staticmethod
    def write(d, name, text):
        with open(os.path.join(d, name), "w") as f:
            f.write(text)

    @staticmethod
    def read(d, name):
        with open(os.path.join(d, name)) as f:
            return f.read()

    def upstream(self, name, text):
        self.write(self.other, name, text)
        run(self.other, "commit", "-q", "-am", f"upstream {name}")
        run(self.other, "push", "-q", "origin", "HEAD:main")

    def origin_file(self, name):
        return run(self.origin, "show", f"main:{name}")

    def commit_ours(self, text="ours v1\n"):
        self.write(self.tree, "ours.txt", text)
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            ok = self.C.commit(["ours.txt"], "ours", [])
        return ok, err.getvalue()

    def assertNothingStashed(self):
        self.assertEqual(run(self.tree, "stash", "list"), "")

    def test_a_foreign_edit_stays_put_when_origin_is_not_ahead(self):
        self.write(self.tree, "foreign.txt", "another agent's draft\n")
        ok, err = self.commit_ours()
        self.assertTrue(ok)
        self.assertEqual(err, "")
        self.assertEqual(self.origin_file("ours.txt"), "ours v1")
        self.assertEqual(self.origin_file("foreign.txt"), "foreign.txt v0", "only our paths are published")
        self.assertEqual(self.read(self.tree, "foreign.txt"), "another agent's draft\n")
        self.assertIn("foreign.txt", self.C.tracked_dirty())
        self.assertNothingStashed()

    def test_a_clean_tree_rebases_onto_origin(self):
        self.upstream("upstream.txt", "upstream v1\n")
        ok, err = self.commit_ours()
        self.assertTrue(ok, err)
        self.assertEqual(err, "")
        self.assertEqual(self.origin_file("upstream.txt"), "upstream v1")
        self.assertEqual(self.origin_file("ours.txt"), "ours v1")
        self.assertEqual(run(self.tree, "rev-parse", "HEAD"), run(self.origin, "rev-parse", "main"))

    def test_others_edits_are_replayed_around_not_stashed(self):
        self.upstream("upstream.txt", "upstream v1\n")
        self.write(self.tree, "foreign.txt", "another agent's draft\n")
        ok, err = self.commit_ours()
        self.assertTrue(ok, err)
        self.assertEqual(self.origin_file("ours.txt"), "ours v1")
        self.assertEqual(self.origin_file("upstream.txt"), "upstream v1")
        self.assertEqual(self.origin_file("foreign.txt"), "foreign.txt v0")
        self.assertEqual(run(self.tree, "rev-parse", "HEAD"), run(self.origin, "rev-parse", "main"), "this tree moved")
        self.assertEqual(self.read(self.tree, "upstream.txt"), "upstream v1\n")
        self.assertEqual(self.read(self.tree, "foreign.txt"), "another agent's draft\n")
        self.assertNothingStashed()
        self.assertEqual(len(run(self.tree, "worktree", "list").splitlines()), 1, "the scratch worktree is gone")

    def test_an_edit_that_also_changed_upstream_is_never_overwritten(self):
        self.upstream("foreign.txt", "foreign changed upstream\n")
        self.write(self.tree, "foreign.txt", "another agent's draft\n")
        ok, err = self.commit_ours()
        self.assertTrue(ok)
        self.assertEqual(self.origin_file("ours.txt"), "ours v1", "ours is published")
        self.assertEqual(self.read(self.tree, "foreign.txt"), "another agent's draft\n")
        self.assertNothingStashed()
        again, why = self.C.publish()
        self.assertTrue(again)
        self.assertIn("nothing to push", why, "the replayed commit is not pushed twice")
        self.assertEqual(run(self.origin, "rev-list", "--count", "main"), "3")

    def test_an_unreachable_origin_leaves_an_honest_receipt_and_publish_retries(self):
        run(self.tree, "remote", "set-url", "origin", os.path.join(self.dir, "missing.git"))
        ok, err = self.commit_ours()
        self.assertTrue(ok, "committed locally")
        self.assertIn("NOT pushed", err)
        self.assertIn("climb.py publish", err)
        self.assertEqual(self.read(self.tree, "ours.txt"), "ours v1\n")
        self.assertEqual(run(self.tree, "log", "-1", "--format=%s"), "ours")
        run(self.tree, "remote", "set-url", "origin", self.origin)
        before = run(self.tree, "rev-list", "--count", "HEAD")
        pushed, why = self.C.publish()
        self.assertTrue(pushed, why)
        self.assertEqual(self.origin_file("ours.txt"), "ours v1")
        self.assertEqual(run(self.tree, "rev-list", "--count", "HEAD"), before, "publish records nothing new")

    def test_the_mocked_control_flow_never_stashes(self):
        # chirper-zero's repro shape: every git call mocked, a foreign tracked draft present
        calls = []

        def fake_git(*a):
            calls.append(list(a))
            out = "M  songs/foreign.yaml\0" if a[:1] == ("status",) else ""
            return types.SimpleNamespace(returncode=0, stdout=out, stderr="")
        self.C.git = fake_git
        self.C.locked = lambda name: contextlib.nullcontext()
        os.makedirs(os.path.join(self.tree, "songs"), exist_ok=True)
        self.assertTrue(self.C.commit(["songs/ours.yaml"], "ours", []))
        self.assertFalse(any("--autostash" in c or c[:1] == ["stash"] for c in calls), calls)
        self.assertFalse(any(c[:1] == ["pull"] for c in calls), calls)


if __name__ == "__main__":
    unittest.main(verbosity=2)
