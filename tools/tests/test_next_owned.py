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


class Pass(unittest.TestCase):
    """`climb.py pass`: drew it, no round to make. It releases the lock at once (chirper-two, 18 Nov: "a pass cannot
    release the lock") and the song is left out of the passer's own draw; so is the song whose last round is yours."""

    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="pass-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self.starts = os.path.join(self.root, "starts.jsonl")
        self.env = {**os.environ, "CLIMB_ROOT": self.root, "CLIMB_STARTS": self.starts}
        climbs = [{"id": i, "status": "active", "rounds": 3, "mode": "compose", "song": f"songs/{i}.yaml", "passes": 1}
                  for i in ("a", "b", "c")]                       # `passes` is the playlist's repeat count: never touched
        climbs.append({"id": "repro", "status": "active", "rounds": 3, "song": "songs/repro.yaml",
                       "last": {"at": "2026-11-18T10:00:00Z", "who": "chirper-two"}})
        with open(os.path.join(self.root, "climbs.json"), "w") as f:
            json.dump({"climbs": climbs}, f)

    def run_(self, *args, who="chirper-two"):
        return subprocess.run([sys.executable, os.path.join(TOOLS, "climb.py"), *args, "--as", who], capture_output=True,
                              text=True, env=self.env)

    def reg(self):
        with open(os.path.join(self.root, "climbs.json")) as f:
            return {c["id"]: c for c in json.load(f)["climbs"]}

    def test_a_pass_releases_the_lock_and_leaves_the_song_out_of_the_passers_draw(self):
        self.assertEqual(self.run_("next", "--take", "a", "--json").returncode, 0)
        held = self.run_("next", "--take", "a", "--json", who="chirper-one")
        self.assertEqual(held.returncode, 3, held.stderr)                                  # chirper-two holds it
        no = self.run_("pass", "a", "full until it is heard:", "four cards wait", "--no-git")
        self.assertEqual(no.returncode, 2)                                                 # Harry, 19 Nov: do not pass
        self.assertIn("can we stop passing on songs", no.stderr)
        self.assertNotIn("passed_by", self.reg()["a"])
        r = self.run_("pass", "a", "full until it is heard:", "four cards wait", "--anyway", "--no-git")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("released", r.stdout)
        self.assertEqual([p["who"] for p in self.reg()["a"]["passed_by"]], ["chirper-two"])
        self.assertEqual(self.reg()["a"]["passes"], 1)
        with open(os.path.join(self.root, "climbs", "a.jsonl")) as f:
            h = json.loads(f.readlines()[-1])
        self.assertTrue(h["passed"] and h["steer"] and "four cards" in h["note"])
        self.assertEqual(self.run_("next", "--take", "a", "--json", who="chirper-one").returncode, 0)   # free at once
        for seed in range(12):                                                             # never drawn to its passer
            got = json.loads(self.run_("next", "--peek", "--json", "--seed", str(seed)).stdout)["climb"]["id"]
            self.assertNotEqual(got, "a")
        self.assertEqual(self.run_("next", "--take", "a", "--json", "--force").returncode, 0)   # but he may come back
        self.run_("pass", "a", "again", "--anyway", "--no-git")
        self.assertEqual(len(self.reg()["a"]["passed_by"]), 1)                               # one pass a composer

    def test_your_own_last_round_is_for_someone_else_and_a_kept_version_voids_the_passes(self):
        reg = {"climbs": list(self.reg().values())}
        by = {c["id"]: c for c in reg["climbs"]}
        by["b"]["last"] = {"at": "2026-11-18T10:00:00Z", "who": "chirper-two"}
        by["c"]["passed_by"] = [{"who": "chirp-climb2", "at": "2026-11-18T10:00:00Z"}]      # an alias of chirper-two
        self.assertEqual(sorted(climb.weights(reg, "chirper-two")), ["a", "repro"])        # not b (his round), not c
        self.assertEqual(sorted(climb.weights(reg, "chirper-one")), ["a", "b", "c", "repro"])
        self.assertTrue(climb.said_last(by["b"], "chirper-two") and not climb.said_last(by["repro"], "chirper-two"))
        by["a"]["last"] = {"at": "2026-11-18T10:00:00Z", "who": "chirper-two"}
        by["repro"]["status"] = "paused"
        self.assertEqual(sorted(climb.weights(reg, "chirper-two")), ["a", "b", "c"])       # nothing else: all, as before
        with open(os.path.join(self.root, "climbs.json"), "w") as f:
            json.dump(reg, f)
        r = self.run_("done", "c", "--version", "v4", "--score", "90", "--keep", "--note", "n", "--no-git", who="chirper-one")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn("passed_by", self.reg()["c"])                                     # the song changed
        self.assertEqual(self.reg()["c"]["passes"], 1)

    def test_nothing_new_starts_nothing_and_harrys_word_reopens_the_song(self):
        """chirper-three, 18 Nov: five passes in two ticks, each a draw, a brief and a lock."""
        reg = {"climbs": list(self.reg().values())}
        by = {c["id"]: c for c in reg["climbs"]}
        by["a"]["last"] = by["c"]["last"] = {"at": "2026-11-18T10:00:00Z", "who": "chirper-two"}
        by["b"]["passed_by"] = [{"who": "chirper-two", "at": "2026-11-18T10:05:00Z"}]
        by["repro"]["status"] = "paused"
        with open(os.path.join(self.root, "climbs.json"), "w") as f:
            json.dump(reg, f)
        r = self.run_("next")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("NOTHING NEW FOR YOU: every free song (a, b, c)", r.stdout)
        self.assertFalse(os.path.exists(self.starts))                                      # nothing was started
        got = json.loads(self.run_("next", "--json").stdout)
        self.assertEqual((got["climb"], got["nothing_new"], got["free"]), (None, True, ["a", "b", "c"]))
        self.assertIn(json.loads(self.run_("next", "--again", "--json").stdout)["climb"]["id"], ("a", "b", "c"))
        with open(self.starts) as f:
            self.assertEqual(len(f.readlines()), 1)                                        # --again draws, and starts
        self.assertIn(json.loads(self.run_("next", "--json", who="chirper-one").stdout)["climb"]["id"], ("a", "b", "c"))
        old = climb.heard_at
        self.addCleanup(setattr, climb, "heard_at", old)
        climb.heard_at = lambda c: climb.epoch("2026-11-18T11:00:00Z") if c["id"] == "b" else 0   # Harry answered on b
        self.assertFalse(climb.said_last(by["b"], "chirper-two"))                          # his word reopens it
        self.assertTrue(climb.said_last(by["a"], "chirper-two"))
        stale = []
        self.assertEqual(sorted(climb.weights(reg, "chirper-two", stale)), ["b"])
        self.assertEqual(stale, [])
        climb.heard_at = lambda c: climb.epoch("2026-11-18T09:00:00Z")                     # an older answer reopens nothing
        self.assertTrue(climb.said_last(by["b"], "chirper-two"))
        self.assertEqual(climb.epoch("not a time"), 0)

    def test_released_reads_rounds_and_passes_and_a_note_finishes_nothing(self):
        t0 = 1_800_000_000
        iso = lambda t: __import__("time").strftime("%Y-%m-%dT%H:%M:%SZ", __import__("time").gmtime(t))   # noqa: E731
        s = {"id": "a", "who": "chirper-two", "t": t0}
        self.assertFalse(climb.released({"id": "a"}, s))
        self.assertTrue(climb.released({"id": "a", "last": {"who": "chirper-two", "at": iso(t0 + 60)}}, s))
        self.assertFalse(climb.released({"id": "a", "last": {"who": "chirper-one", "at": iso(t0 + 60)}}, s))
        self.assertTrue(climb.released({"id": "a", "passed_by": [{"who": "chirper-two", "at": iso(t0 + 60)}]}, s))
        self.assertFalse(climb.released({"id": "a", "passed_by": [{"who": "chirper-two", "at": iso(t0 - 600)}]}, s))   # older
        self.assertEqual(climb.holders({"id": "a", "passed_by": [{"who": "chirper-two", "at": iso(t0 + 60)}]}, "chirper-one",
                                       st=[s], t=t0 + 120), [])
        self.assertEqual(climb.holders({"id": "a"}, "chirper-one", st=[s], t=t0 + 120), ["chirper-two"])
        st = [s, {"id": "a", "who": "chirper-alpha", "t": t0 + 460}]
        note = [{"round": 3, "who": "chirper-two", "at": iso(t0 + 230), "note": "a steering note", "steer": True}]
        self.assertEqual(len(climb.collided("a", "chirper-alpha", st=st, hist=note)), 1)   # a real note carries `round`
        self.assertEqual(climb.collided("a", "chirper-alpha", st=st, hist=[{**note[0], "passed": True}]), [])


class Handoff(unittest.TestCase):
    """done --with refuses when someone else was on the song WHILE you were; a round finished before you began is a
    handoff (chirper-alpha, 18 Nov: The Other Hand, chirper-two done at 04:56, alpha started at 05:00)."""

    def test_a_round_finished_before_you_began_is_not_a_collision(self):
        t0 = 1_800_000_000
        iso = lambda t: __import__("time").strftime("%Y-%m-%dT%H:%M:%SZ", __import__("time").gmtime(t))   # noqa: E731
        st = [{"id": "s", "who": "chirper-two", "t": t0}, {"id": "s", "who": "chirper-alpha", "t": t0 + 460},
              {"id": "other", "who": "chirper-one", "t": t0 + 400}]
        done = [{"round": 1, "who": "chirper-two", "at": iso(t0 + 230)}]
        self.assertEqual(climb.collided("s", "chirper-alpha", st=st, hist=done), [])                # the handoff
        self.assertEqual([s["who"] for s in climb.collided("s", "chirper-alpha", st=st, hist=[])], ["chirper-two"])
        note = [{"who": "chirper-two", "at": iso(t0 + 230), "note": "a note, not a round"}]
        self.assertEqual(len(climb.collided("s", "chirper-alpha", st=st, hist=note)), 1)           # a note finishes nothing
        late = [{"round": 1, "who": "chirper-two", "at": iso(t0 + 600)}]
        self.assertEqual(len(climb.collided("s", "chirper-alpha", st=st, hist=late)), 1)           # recorded after you began
        again = st + [{"id": "s", "who": "chirper-two", "t": t0 + 500}]
        self.assertEqual([s["t"] for s in climb.collided("s", "chirper-alpha", st=again, hist=done)], [t0 + 500])
        old = [{"id": "s", "who": "chirper-two", "t": t0 - 3 * 3600}, {"id": "s", "who": "chirper-alpha", "t": t0}]
        self.assertEqual(climb.collided("s", "chirper-alpha", st=old, hist=[]), [])                 # long before: as it was
        self.assertEqual(climb.collided("s", "chirp-climb2", st=st[:1], hist=[], now=t0 + 60), [])  # your own alias


class JudgedRun(unittest.TestCase):
    """The brief sums a run of rounds kept on judgment: each composer sees only the version before (18 Nov)."""

    @staticmethod
    def r(n, score, judged=False, who="chirper-zero", kept=True):
        return {"round": n, "version": f"v{n}", "score": score, "kept": kept, "judged": judged or None, "who": who}

    def test_three_judged_rounds_a_point_down_are_summed(self):
        h = [self.r(1, 81.27), self.r(2, 81.42), self.r(3, 82.18, who="chirper-three"), self.r(4, 82.14, True),
             self.r(5, 81.61, True, "chirper-three"), self.r(6, 81.279, True, "chirper-two"), self.r(7, 81.07, True),
             {"note": "a note, not a round", "who": "chirper-one"}, self.r(8, 80.984, True, "chirper-one")]
        out = climb.judged_run_lines(h)
        self.assertEqual(len(out), 1)
        for word in ("5 ROUNDS RUNNING", "v8 is recorded at 80.984", "1.20 under v3 (82.18)", "chirper-one, chirper-three",
                     "refuses nothing"):
            self.assertIn(word, out[0])

    def test_quiet_when_there_is_nothing_to_sum(self):
        r = self.r
        self.assertEqual(climb.judged_run_lines([]), [])
        self.assertEqual(climb.judged_run_lines([r(1, 90.0), r(2, 89.0, True), r(3, 88.0, True)]), [])          # two only
        self.assertEqual(climb.judged_run_lines([r(1, 90.0), r(2, 89.9, True), r(3, 89.8, True), r(4, 89.7, True)]), [])
        self.assertEqual(climb.judged_run_lines([r(1, 90.0, True), r(2, 88.0, True), r(3, 86.0, True)]), [])    # no base
        self.assertEqual(climb.judged_run_lines([r(1, 90.0), r(2, 88.0, True), r(3, 87.0, True), r(4, 86.0, True),
                                                 r(5, 86.5)]), [])                                           # run ended
        up = [r(1, 90.0), r(2, 90.5, True), r(3, 91.0, True), r(4, 91.5, True)]
        self.assertEqual(climb.judged_run_lines(up), [])                                                     # rose
        gone = [r(1, 90.0), r(2, 80.0, True, kept=False), r(3, 89.0, True), r(4, 88.5, True)]
        self.assertEqual(climb.judged_run_lines(gone), [])                               # a round not kept is no version


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
              {"op": "built", "id": "q1", "at": now, "by": "chirper-two", "version": "v3", "text": "the hook is 3 dB up at 1:15"},
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
        self.assertIn("listen.py built alb CARD", text)             # how to say an answer was acted on, with no new card
        self.assertIn("BUILT in v3 by chirper-two: the hook is 3 dB up at 1:15", text)
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
