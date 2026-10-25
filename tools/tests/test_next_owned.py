#!/usr/bin/env python3
"""climb.py next: skips climbs another agent owns (chirper-zero/chirper-one, 23 Oct: drawing them recorded a start
that later forced `done --force` on the owner), knows chirp-climbN = chirper-<N>, and --take ID starts exactly one.

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

    def test_draws_skip_other_agents_climbs(self):
        for seed in range(30):
            r = self.next_("--seed", str(seed), "--peek")
            self.assertEqual(r.returncode, 0, r.stderr)
            out = json.loads(r.stdout)
            self.assertNotEqual(out["climb"]["id"], "theirs")
            self.assertEqual(out["skipped_owned"], ["theirs"])

    def test_aliases_are_the_same_agent(self):
        self.assertTrue(climb.agent_names("chirp-climb0") & climb.agent_names("chirper-zero"))
        self.assertTrue(climb.agent_names("chirper-one (chirp-climb1)") & climb.agent_names("chirper-one"))
        self.assertFalse(climb.agent_names("chirper-one") & climb.agent_names("chirper-zero"))
        self.assertFalse(climb.owned_by_other({"owner": "chirp-climb0"}, "chirper-zero"))
        self.assertTrue(climb.owned_by_other({"owner": "chirper-one"}, "chirper-zero"))
        self.assertFalse(climb.owned_by_other({}, "anyone"))

    def test_include_owned_can_draw_them(self):
        got = {json.loads(self.next_("--seed", str(s), "--peek", "--include-owned").stdout)["climb"]["id"]
               for s in range(60)}
        self.assertIn("theirs", got)

    def test_take_starts_exactly_that_climb(self):
        r = self.next_("--take", "free")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout)["climb"]["id"], "free")
        self.assertEqual(self.started(), ["free"])

    def test_take_refuses_another_agents_climb_without_force(self):
        r = self.next_("--take", "theirs")
        self.assertEqual(r.returncode, 3)
        self.assertIn("owned by chirper-one", r.stderr)
        self.assertEqual(self.started(), [])
        self.assertEqual(self.next_("--take", "theirs", "--force").returncode, 0)
        self.assertEqual(self.started(), ["theirs"])

    def test_peek_records_no_start(self):
        self.next_("--peek", "--seed", "1")
        self.assertEqual(self.started(), [])

    def test_all_owned_by_others_explains(self):
        r = self.next_(who="chirper-two")
        self.assertEqual(r.returncode, 0, r.stderr)            # 'free' is still drawable
        with open(os.path.join(self.root, "climbs.json")) as f:
            reg = json.load(f)
        for c in reg["climbs"]:
            c["owner"] = c.get("owner") or "chirper-one"
        with open(os.path.join(self.root, "climbs.json"), "w") as f:
            json.dump(reg, f)
        r = self.next_(who="chirper-two")
        self.assertEqual(r.returncode, 1)
        self.assertIn("every queued climb is owned by another agent", r.stderr)


if __name__ == "__main__":
    unittest.main()
