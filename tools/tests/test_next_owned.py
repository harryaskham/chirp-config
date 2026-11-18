#!/usr/bin/env python3
"""climb.py next: NO CLIMB HAS AN OWNER (Harry, 18 Nov: "climbing should not have owenrs, owners should be able to take
the lock on any song"; "a new round should release for anyuone to improve"; "tha tis hos we maintain variaety"). The draw
is among every queued climb, whoever worked on it last; what keeps two agents off one song is the LOCK (a start under
90 minutes old with no round recorded since), and --take ID respects it. It knows chirp-climbN = chirper-<N>. And the
brief carries what Harry said of the track on the review page ("they will get notes hwen they next see the track").
(Until 18 Nov the draw skipped climbs another agent owned; the `owner` field older climbs carry is history.)

  python3 tools/tests/test_next_owned.py      (from ~/.config/chirp; a few seconds; a temp registry, no git)
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import climb  # noqa: E402


class NextOwned(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="next-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self.starts = os.path.join(self.root, "starts.jsonl")
        climbs = [{"id": "mine", "status": "active", "rounds": 2, "owner": "chirper-zero", "song": "songs/mine.yaml"},
                  {"id": "theirs", "status": "active", "rounds": 0, "owner": "chirper-one", "song": "songs/theirs.yaml"},
                  {"id": "free", "status": "requested", "rounds": 0, "song": "songs/free.yaml"},
                  {"id": "alias", "status": "active", "rounds": 1, "owner": "chirp-climb0", "song": "songs/alias.yaml"}]
        with open(os.path.join(self.root, "climbs.json"), "w") as f:
            json.dump({"climbs": climbs}, f)

    def next_(self, *args, who="chirper-zero"):
        r = subprocess.run([sys.executable, os.path.join(TOOLS, "climb.py"), "next", "--as", who, "--json", *args],
                           capture_output=True, text=True,
                           env={**os.environ, "CLIMB_ROOT": self.root, "CLIMB_STARTS": self.starts})
        return r

    def started(self):
        if not os.path.exists(self.starts):
            return []
        with open(self.starts) as f:
            return [json.loads(x)["id"] for x in f]

    def test_an_unclaimed_setup_in_progress_is_flagged(self):
        os.makedirs(os.path.join(self.root, "tools", "maps"))
        with open(os.path.join(self.root, "tools", "maps", "free.json"), "w") as f:
            f.write("{}")
        r = self.next_("--take", "free", who="chirper-one")
        self.assertEqual(json.loads(r.stdout).get("untracked_setup"), ["tools/maps/free.json"])
        self.assertIn("looks mid-setup", r.stderr)
        r = self.next_("--take", "mine", who="chirper-zero")       # an active climb: no warning, key absent
        self.assertNotIn("untracked_setup", json.loads(r.stdout))

    def test_draws_include_other_agents_climbs(self):
        got = set()
        for seed in range(60):
            r = self.next_("--seed", str(seed), "--peek")
            self.assertEqual(r.returncode, 0, r.stderr)
            out = json.loads(r.stdout)
            got.add(out["climb"]["id"])
            self.assertEqual(out["skipped_owned"], [])
        self.assertIn("theirs", got)                               # composed first by chirper-one: drawn all the same
        self.assertIn("mine", got)

    def test_aliases_are_the_same_agent(self):
        self.assertTrue(climb.agent_names("chirp-climb0") & climb.agent_names("chirper-zero"))
        self.assertTrue(climb.agent_names("chirper-one (chirp-climb1)") & climb.agent_names("chirper-one"))
        self.assertFalse(climb.agent_names("chirper-one") & climb.agent_names("chirper-zero"))
        self.assertFalse(hasattr(climb, "owned_by_other"))

    def test_include_owned_is_still_accepted(self):
        self.assertEqual(self.next_("--seed", "1", "--peek", "--include-owned").returncode, 0)

    def test_take_starts_exactly_that_climb(self):
        r = self.next_("--take", "free")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout)["climb"]["id"], "free")
        self.assertEqual(self.started(), ["free"])

    def test_anyone_takes_a_song_nobody_holds(self):
        r = self.next_("--take", "theirs")                         # chirper-zero takes what chirper-one composed
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.started(), ["theirs"])

    def test_take_respects_the_lock_and_a_recorded_round_releases_it(self):
        self.assertEqual(self.next_("--take", "mine", who="chirper-one").returncode, 0)      # chirper-one holds `mine`
        r = self.next_("--take", "mine")
        self.assertEqual(r.returncode, 3)
        self.assertIn("is held by chirper-one", r.stderr)
        self.assertEqual(self.started(), ["mine"])
        self.assertEqual(self.next_("--take", "mine", who="chirp-climb1").returncode, 0)     # the same climber: its own lock
        for seed in range(30):                                     # and the draw leaves a held song out while others are free
            self.assertNotEqual(json.loads(self.next_("--seed", str(seed), "--peek").stdout)["climb"]["id"], "mine")
        with open(os.path.join(self.root, "climbs.json")) as f:
            reg = json.load(f)
        for c in reg["climbs"]:
            if c["id"] == "mine":                                  # chirper-one records the round: the song is released
                c["last"] = {"at": climb.now_iso(), "who": "chirper-one"}
        with open(os.path.join(self.root, "climbs.json"), "w") as f:
            json.dump(reg, f)
        self.assertEqual(climb.holders({"id": "mine", "last": {"at": climb.now_iso(), "who": "chirper-one"}}, "chirper-zero",
                                       st=[{"id": "mine", "who": "chirper-one", "t": __import__("time").time() - 60}]), [])
        self.assertEqual(self.next_("--take", "mine").returncode, 0)
        self.assertEqual(self.next_("--take", "theirs", who="chirper-two", ).returncode, 0)
        self.assertEqual(self.next_("--take", "theirs", "--force").returncode, 0)             # --force takes a held one

    def test_peek_records_no_start(self):
        self.next_("--peek", "--seed", "1")
        self.assertEqual(self.started(), [])

    def test_a_registry_owned_by_one_agent_is_open_to_all(self):
        with open(os.path.join(self.root, "climbs.json")) as f:
            reg = json.load(f)
        for c in reg["climbs"]:
            c["owner"] = "chirper-one"
        with open(os.path.join(self.root, "climbs.json"), "w") as f:
            json.dump(reg, f)
        r = self.next_(who="chirper-two")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn("owned by", r.stderr)


class Heard(unittest.TestCase):
    """The brief carries Harry's open notes, his answers and the cards waiting on him, for whoever draws the track."""

    def setUp(self):
        import listen
        self.root = tempfile.mkdtemp(prefix="heard-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        os.makedirs(os.path.join(self.root, "alb"))
        old = (listen.DATA, os.environ.get("CHIRP_LISTEN_DIR"))
        listen.DATA = self.root
        os.environ["CHIRP_LISTEN_DIR"] = self.root

        def back():
            listen.DATA = old[0]
            if old[1] is None:
                os.environ.pop("CHIRP_LISTEN_DIR", None)
            else:
                os.environ["CHIRP_LISTEN_DIR"] = old[1]
        self.addCleanup(back)
        now = climb.now_iso()
        notes = [{"op": "add", "id": "n1", "at": now, "by": "harry", "snap": "s1", "n": 2, "version": "v3", "t": 75.0,
                  "text": "the bass is lost here"},
                 {"op": "add", "id": "n2", "at": now, "by": "harry", "snap": "s1", "n": 2, "version": "v3", "t": 10.0,
                  "text": "done already"},
                 {"op": "reply", "id": "n2", "at": now, "by": "chirper-one", "text": "mended", "done": True},
                 {"op": "add", "id": "n3", "at": now, "by": "harry", "snap": "s1", "n": 5, "version": "v1", "t": 1.0,
                  "text": "another track"},
                 {"op": "add", "id": "n4", "at": now, "by": "harry", "snap": "s1", "n": None, "text": "more variety"}]
        qs = [{"op": "ask", "id": "q1", "at": now, "by": "chirper-zero", "n": 2, "version": "v2", "key": "riff",
               "title": "A hook, or an exercise?", "choices": ["A hook", "An exercise"]},
              {"op": "answer", "id": "q1", "at": now, "by": "harry", "choice": "A hook", "text": "louder though"},
              {"op": "ask", "id": "q2", "at": now, "by": "chirper-one", "n": 2, "version": "v3", "key": "wall",
               "title": "Bigger, or muddier?", "choices": ["Bigger", "Muddier"]},
              {"op": "ask", "id": "q3", "at": "2020-01-01T00:00:00Z", "by": "chirper-zero", "n": 2, "version": "v1",
               "key": "old", "title": "Long ago?", "choices": ["Yes"]},
              {"op": "answer", "id": "q3", "at": "2020-01-02T00:00:00Z", "by": "harry", "choice": "Yes"},
              {"op": "ask", "id": "q4", "at": now, "by": "chirper-zero", "n": 5, "version": "v1", "key": "other",
               "title": "Another track's card?", "choices": ["Yes"]}]
        for name, rows in (("notes.jsonl", notes), ("questions.jsonl", qs)):
            with open(os.path.join(self.root, "alb", name), "w") as f:
                f.write("".join(json.dumps(r) + "\n" for r in rows))

    def test_the_brief_carries_what_harry_said_of_the_track(self):
        text = "\n".join(climb.heard_lines("alb", {"id": "alb-t2", "meta": {"track": 2}}))
        self.assertIn("HARRY ON THIS TRACK", text)
        self.assertIn("NOTE ", text)
        self.assertIn("at 1:15 of v3: the bass is lost here", text)
        self.assertIn("listen.py reply alb n1 'what you did' --done", text)
        self.assertNotIn("done already", text)                     # a note marked done is not carried
        self.assertNotIn("another track", text)
        self.assertIn("on the whole album: more variety", text)    # a note on no track reaches every track
        self.assertIn('card riff (asked at v2): "A hook, or an exercise?" -> "A hook / louder though"', text)
        self.assertNotIn("Long ago?", text)                        # an answer older than the window
        self.assertIn('WAITING ON HARRY, card wall (asked at v3 by chirper-one): "Bigger, or muddier?"', text)
        self.assertNotIn("Another track's card?", text)
        self.assertEqual(climb.heard_lines("alb", {"id": "alb-t9", "meta": {"track": 9}}),
                         climb.heard_lines("alb", {"id": "alb-t8", "meta": {"track": 8}}))   # only the album's note
        self.assertEqual(climb.heard_lines("nosuch", {"id": "x", "meta": {"track": 1}}), [])

    def test_a_tests_registry_never_reads_the_real_page(self):
        os.environ.pop("CHIRP_LISTEN_DIR")
        old = os.environ.get("CLIMB_ROOT")
        os.environ["CLIMB_ROOT"] = self.root
        try:
            self.assertEqual(climb.heard_lines("alb", {"id": "alb-t2", "meta": {"track": 2}}), [])
        finally:
            os.environ["CHIRP_LISTEN_DIR"] = self.root
            if old is None:
                os.environ.pop("CLIMB_ROOT")
            else:
                os.environ["CLIMB_ROOT"] = old


if __name__ == "__main__":
    unittest.main()
