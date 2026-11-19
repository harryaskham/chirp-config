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
import sys
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
        # the worst user config: git would autostash on its own (bd-d30a90 acceptance 1)
        run(self.tree, "config", "rebase.autoStash", "true")
        run(self.tree, "config", "merge.autoStash", "true")
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

    def test_a_staged_foreign_edit_keeps_its_index_and_bytes(self):
        self.upstream("upstream.txt", "upstream v1\n")
        self.write(self.tree, "foreign.txt", "staged draft\n")
        run(self.tree, "add", "foreign.txt")
        self.write(self.tree, "foreign.txt", "staged draft, then edited\n")
        staged = run(self.tree, "diff", "--cached", "--", "foreign.txt")
        ok, err = self.commit_ours()
        self.assertTrue(ok, err)
        self.assertEqual(self.origin_file("ours.txt"), "ours v1")
        self.assertEqual(self.origin_file("foreign.txt"), "foreign.txt v0", "the staged draft is not published")
        self.assertEqual(run(self.tree, "diff", "--cached", "--", "foreign.txt"), staged, "the index entry is kept")
        self.assertEqual(self.read(self.tree, "foreign.txt"), "staged draft, then edited\n")
        self.assertNothingStashed()

    def test_a_fast_forward_beside_a_foreign_edit(self):
        self.upstream("upstream.txt", "upstream v1\n")
        self.write(self.tree, "foreign.txt", "another agent's draft\n")
        ok, why = self.C.publish()
        self.assertTrue(ok, why)
        self.assertEqual(self.read(self.tree, "upstream.txt"), "upstream v1\n", "fast-forwarded")
        self.assertEqual(self.read(self.tree, "foreign.txt"), "another agent's draft\n")
        self.assertNothingStashed()

    def test_a_push_race_is_retried_once_more(self):
        real, calls, raced = self.C.git, [], []

        def racing(*a):
            calls.append(list(a))
            if a[:1] == ("push",) and not raced:   # someone else pushes first
                raced.append(1)
                self.upstream("upstream.txt", "raced in\n")
            return real(*a)
        self.C.git = racing
        ok, err = self.commit_ours()
        self.assertTrue(ok, err)
        self.assertEqual(err, "")
        self.assertEqual(self.origin_file("upstream.txt"), "raced in")
        self.assertEqual(self.origin_file("ours.txt"), "ours v1")
        self.assertEqual(run(self.origin, "log", "--format=%s", "main").split("\n").count("ours"), 1, "one record")
        for c in calls:
            if c[:1] in (["merge"], ["rebase"]):
                self.assertIn("--no-autostash", c, c)
            self.assertNotIn("--autostash", c)
        self.assertNothingStashed()

    # ── commit --pick: only your hunks of a file everyone writes (chirper-zero, 19 Nov) ──
    DOC = "# motifs\n\n## Track 7\nold seven\n\n## Track 11\nold eleven\n\n## Track 12\nold twelve\n"
    OPEN = ("# motifs\n\n## Track 7\nold seven\nt7 v19: the stroke stops (another composer's, round not recorded)\n\n"
            "## Track 11\nold eleven\noih v16: the bow is a bow\n\n## Track 12\nold twelve, see oih v16\n")

    def seed_doc(self):
        self.write(self.tree, "doc.md", self.DOC)
        run(self.tree, "add", "doc.md")
        run(self.tree, "commit", "-q", "-m", "doc")
        run(self.tree, "push", "-q", "origin", "HEAD:main")

    def pick(self, pattern, *paths):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            ok = self.C.commit_picked(list(paths), "picked", pattern, [])
        return ok, out.getvalue(), err.getvalue()

    def test_pick_commits_only_the_matching_hunks_and_leaves_the_rest_open(self):
        self.seed_doc()
        run(self.other, "pull", "-q", "origin", "main")
        self.upstream("upstream.txt", "upstream v1\n")                 # origin moved meanwhile: the pick is replayed onto it
        self.write(self.tree, "foreign.txt", "staged draft\n")
        run(self.tree, "add", "foreign.txt")
        staged = run(self.tree, "diff", "--cached", "--", "foreign.txt")
        self.write(self.tree, "doc.md", self.OPEN)
        ok, out, err = self.pick("oih", "doc.md")
        self.assertTrue(ok, err)
        self.assertIn("doc.md: 2 of 3 open hunk(s) match 'oih'", out)
        self.assertIn("left open in the tree: +1 -0  \"t7 v19: the stroke stops", out)
        want = self.DOC.replace("old eleven\n", "old eleven\noih v16: the bow is a bow\n").replace("old twelve", "old twelve, see oih v16")
        self.assertEqual(self.origin_file("doc.md"), want.strip())
        self.assertEqual(run(self.tree, "show", "HEAD:doc.md"), want.strip())
        self.assertEqual(self.read(self.tree, "doc.md"), self.OPEN)                 # the working file is not written
        left = run(self.tree, "diff", "HEAD", "--", "doc.md")
        self.assertIn("+t7 v19: the stroke stops", left)
        self.assertNotIn("oih", "".join(ln for ln in left.splitlines() if ln[:1] in "+-" and ln[:3] not in ("+++", "---")))
        self.assertEqual(run(self.tree, "diff", "--cached", "--name-only"), "foreign.txt")   # doc.md's index entry follows HEAD
        self.assertEqual(run(self.tree, "diff", "--cached", "--", "foreign.txt"), staged, "a staged edit is not read or moved")
        self.assertEqual(self.origin_file("foreign.txt"), "foreign.txt v0")
        self.assertEqual(self.origin_file("upstream.txt"), "upstream v1")
        self.assertEqual(run(self.tree, "log", "-1", "--format=%s"), "picked")
        self.assertEqual(os.listdir(os.path.join(self.tree, ".git")).count("climb-pick-index.%d" % os.getpid()), 0)
        self.assertNothingStashed()

    def test_pick_commits_nothing_when_nothing_matches(self):
        self.seed_doc()
        self.write(self.tree, "doc.md", self.OPEN)
        head = run(self.tree, "rev-parse", "HEAD")
        ok, out, err = self.pick("no such words", "doc.md")
        self.assertFalse(ok)
        self.assertIn("0 of 3 open hunk(s) match", out)
        self.assertIn("not committed", err)
        self.assertEqual(run(self.tree, "rev-parse", "HEAD"), head)
        self.assertEqual(self.read(self.tree, "doc.md"), self.OPEN)
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            self.C.commit_picked(["doc.md"], "m", "(", [])                          # not a regular expression
        self.write(self.tree, "new.md", "oih\n")
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            self.C.commit_picked(["new.md"], "m", "oih", [])                        # a new file is committed whole

    def test_pick_says_when_lines_that_touch_go_in_together(self):
        self.seed_doc()
        self.write(self.tree, "doc.md", self.DOC.replace("old eleven\n", "old eleven\nt7 v19: someone else's\noih v16: mine\n"))
        ok, out, err = self.pick("oih", "doc.md")
        self.assertTrue(ok, err)
        self.assertIn("NOTE a committed hunk also carries 1 added line(s) that do not match", out)
        self.assertIn("t7 v19: someone else's", out)
        self.assertIn("t7 v19: someone else's", self.origin_file("doc.md"))         # one hunk: it cannot be split by this tool

    def test_pick_through_the_command_line_and_never_on_the_library(self):
        self.seed_doc()
        self.write(self.tree, "doc.md", self.OPEN)
        sys.path.insert(0, TOOLS)                                                   # cmd_commit imports libguard, as the script does
        self.addCleanup(sys.path.remove, TOOLS)
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.C.cmd_commit(["-m", "from the command line", "--pick", "t7 v19", "doc.md"])
            self.assertIn("t7 v19", self.origin_file("doc.md"))
            self.assertNotIn("oih", self.origin_file("doc.md"))
            with self.assertRaises(SystemExit):
                self.C.cmd_commit(["-m", "m", "--pick", "x", "patches/a.yaml"])

    def test_a_shared_board_committed_whole_says_what_went_in(self):
        """19 Nov, twice in five hours: a commit took another composer's uncommitted rows of motifs.md with it. It is
        not stopped (a composer may have two places of their own), but each open hunk's first words are printed."""
        os.makedirs(os.path.join(self.tree, "compose", "alb"))
        self.write(self.tree, "compose/alb/motifs.md", self.DOC)
        run(self.tree, "add", "compose/alb/motifs.md")
        run(self.tree, "commit", "-q", "-m", "board")
        run(self.tree, "push", "-q", "origin", "HEAD:main")
        self.write(self.tree, "compose/alb/motifs.md", self.DOC.replace("old seven\n", "old seven\nmine\n"))
        self.assertEqual(self.C.shared_board_notes(["compose/alb/motifs.md"]), [])           # one open hunk: nothing to say
        self.write(self.tree, "compose/alb/motifs.md", self.OPEN)
        notes = self.C.shared_board_notes(["compose/alb/motifs.md", "ours.txt"])
        self.assertIn("compose/alb/motifs.md goes in WHOLE, with 3 open hunks", notes[0])
        self.assertIn("--pick 'REGEX' compose/alb/motifs.md", notes[0])
        self.assertEqual(len(notes), 4)
        self.assertIn("t7 v19: the stroke stops", notes[1])
        self.write(self.tree, "doc.md", self.OPEN)                                             # not a board: never noted
        self.assertEqual(self.C.shared_board_notes(["doc.md"]), [])
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertTrue(self.C.commit(["compose/alb/motifs.md"], "whole", []))            # and the commit goes ahead
        self.assertIn("goes in WHOLE, with 3 open hunks", err.getvalue())
        self.assertIn("t7 v19", self.origin_file("compose/alb/motifs.md"))

    def test_done_refuses_a_board_that_holds_someone_elses_open_hunks(self):
        """19 Nov: three times in six hours `done --with motifs.md` took another composer's unrecorded rows with it."""
        os.makedirs(os.path.join(self.tree, "compose", "alb"))
        self.write(self.tree, "compose/alb/motifs.md", self.DOC)
        run(self.tree, "add", "compose/alb/motifs.md")
        run(self.tree, "commit", "-q", "-m", "board")
        board = lambda text: self.write(self.tree, "compose/alb/motifs.md", text)                                   # noqa: E731
        gate = lambda *x, args=(): self.C.board_gate(["compose/alb/motifs.md", "ours.txt"], *x, list(args))   # noqa: E731
        zero, one = ("alb-t11", "On Its Hinge", 11, "chirper-zero"), ("alb-t7", "Extreme and Mean", 7, "chirper-one")
        self.assertIsNone(gate(*zero))                                                       # nothing open: nothing held
        seven, eleven = "old seven\nt7 v19: the stroke stops\n", "old eleven\nt11 v16: the bow is a bow\n"
        board(self.DOC.replace("old seven\n", seven).replace("old eleven\n", eleven))        # one row each, both open
        for who, theirs in ((zero, "t7 v19: the stroke stops"), (one, "t11 v16: the bow is a bow")):
            err = io.StringIO()
            with self.assertRaises(SystemExit) as e, contextlib.redirect_stderr(err):
                gate(*who)
            self.assertEqual(e.exception.code, 5)
            self.assertIn("shared board HELD: compose/alb/motifs.md holds 1 open hunk(s)", err.getvalue())
            self.assertIn(theirs, err.getvalue())
            self.assertIn("Nothing was committed or recorded", err.getvalue())
            self.assertIn("--pick 'REGEX' compose/alb/motifs.md", err.getvalue())
            self.assertIsNone(gate(*who, args=["--whole"]))                                  # --whole: as it stands
        board(self.DOC.replace("old eleven\n", eleven))                                      # only t11's row is open
        self.assertIsNone(gate(*zero))
        board(self.DOC.replace("old eleven\n", "old eleven\na line that names nobody\n"))
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            gate(*zero)                                                                      # it could be anyone's: held
        board(self.DOC.replace("old eleven\n", "old eleven\nthe hinge turns (chirper-one)\n"))
        self.assertIsNone(gate(*one))                                                        # his name is on it
        board(self.DOC.replace("old eleven\n", "old eleven\nOn its hinge, again\n"))
        self.assertIsNone(gate(*zero))                                                       # the title, whatever the case
        board(self.DOC.replace("old eleven\n", "old eleven\nfor ALB-T11 only\n"))
        self.assertIsNone(gate(*zero))                                                       # the id
        self.write(self.tree, "ours.txt", "anything\n")                                      # not a board: never held
        self.assertIsNone(self.C.board_gate(["ours.txt"], *zero, []))

    def test_pick_hunks_builds_from_heads_own_lines(self):
        head = b"a\nb\nc\nd\n"
        diff = (b"diff --git a/f b/f\n--- a/f\n+++ b/f\n@@ -0,0 +1 @@\n+TOP\n@@ -2 +3 @@\n-b\n+B\n@@ -3 +3,0 @@\n-c\n"
                b"@@ -4,0 +5 @@\n+END\n\\ No newline at end of file\n")
        every, seen = self.C.pick_hunks(head, diff, lambda add, rem: True)
        self.assertEqual(every, b"TOP\na\nB\nd\nEND")
        self.assertEqual([(k, len(a), len(r)) for k, a, r in seen], [(True, 1, 0), (True, 1, 1), (True, 0, 1), (True, 1, 0)])
        self.assertEqual(self.C.pick_hunks(head, diff, lambda add, rem: False)[0], head)
        self.assertEqual(self.C.pick_hunks(head, diff, lambda add, rem: rem == [b"c\n"])[0], b"a\nb\nd\n")       # a deletion alone
        self.assertEqual(self.C.pick_hunks(head, diff, lambda add, rem: add == [b"END"])[0], b"a\nb\nc\nd\nEND")  # the last alone
        self.assertEqual(self.C.pick_hunks(head, diff, lambda add, rem: add == [b"B\n"])[0], b"a\nB\nc\nd\n")     # the middle alone
        self.assertEqual(self.C.pick_hunks(head, b"", lambda add, rem: True), (head, []))

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
