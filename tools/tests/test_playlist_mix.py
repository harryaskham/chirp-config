#!/usr/bin/env python3
"""playlist.py DJ-mix seams: entries overlap their album neighbour by the bars the album's mix plan gives (Harry,
31 Oct: The Endless Stair, an 18-track mixtape), and a playing entry is never removed for a seam change.

  python3 tools/tests/test_playlist_mix.py      (from ~/.config/chirp; instant; temp registry, no groove)
"""
import json
import os
import shutil
import sys
import tempfile
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import playlist as P  # noqa: E402

PLAN = ("| seam | out | in | tempo at seam | key | overlap (bars) | handover | agree | swap |\n"
        "|---|---|---|---|---|---|---|---|---|\n"
        "| t1 -> t2 | a | b | 118 | 8A | 16 | hats | | mid |\n| t2 -> t3 | | | | | 8 bars | | | 4 |\n| t3 -> t4 | | | | | 16 | | | |\n")


class Mix(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="playlist-mix-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self.tools = os.path.join(self.root, "tools")
        for d in ("songs", "tools", "compose/alb9"):
            os.makedirs(os.path.join(self.root, d))
        ids = ["alb9-t1", "alb9-t2", "alb9-t4"]
        with open(os.path.join(self.root, "climbs.json"), "w") as f:
            json.dump({"climbs": [{"id": i, "song": f"songs/{i}.yaml"} for i in ids]}, f)
        for i in ids:
            open(os.path.join(self.root, "songs", i + ".yaml"), "w").close()
        with open(os.path.join(self.root, "compose/alb9/mixplan.md"), "w") as f:
            f.write(PLAN)
        self.old = (P.HERE, P.ROOT, P.log, P.request)
        self.calls = []
        P.HERE, P.ROOT, P.log, P.request = self.tools, self.root, (lambda *a: None), self.calls.append
        self.addCleanup(lambda: (setattr(P, "HERE", self.old[0]), setattr(P, "ROOT", self.old[1]),
                                 setattr(P, "log", self.old[2]), setattr(P, "request", self.old[3])))
        P.IDS_MODE[0] = P.ALBUM_MODE[0] = None

    def want(self, field="overlap"):
        cs = P.climbs()
        return {e["label"]: e.get(field) for e in P.with_seams(cs, [P.entry(c) for c in cs])}

    def status(self, overlaps, current):
        es = [{"label": i, "source": P.path({"id": i, "song": f"songs/{i}.yaml"}), "overlap": o[0] if isinstance(o, tuple) else o,
               "swap": o[1] if isinstance(o, tuple) else None} for i, o in overlaps]
        return {"playlist": {"entries": es, "current": current, "repeat": True}}

    def test_only_album_neighbours_overlap(self):
        # t1 -> t2 is a seam (16); t2 -> t4 skips a track and t4 -> t1 is the loop: back to back
        self.assertEqual(self.want(), {"alb9-t1": 16.0, "alb9-t2": None, "alb9-t4": None})

    def test_no_mix_plan_no_seams(self):
        os.remove(os.path.join(self.root, "compose/alb9/mixplan.md"))
        self.assertEqual(self.want(), {"alb9-t1": None, "alb9-t2": None, "alb9-t4": None})

    def test_a_playing_entry_is_never_removed_for_its_seam(self):
        P.sync(self.status([("alb9-t1", None), ("alb9-t2", None), ("alb9-t4", None)], current=0))
        self.assertEqual(self.calls, [])                                   # t1 plays: its new seam waits
        P.sync(self.status([("alb9-t1", None), ("alb9-t2", None), ("alb9-t4", None)], current=1))
        ops = [(c["op"], c.get("index", c.get("at"))) for c in self.calls]
        self.assertEqual(ops, [("playlist-remove", 0), ("playlist-add", 0)])   # once it has played: updated in place
        self.assertEqual(self.calls[1]["entries"][0]["overlap"], 16.0)

    def test_a_matching_playlist_is_left_alone(self):
        P.sync(self.status([("alb9-t1", (16.0, True)), ("alb9-t2", None), ("alb9-t4", None)], current=2))
        self.assertEqual(self.calls, [])

    def test_the_mix_plans_swap_cells_ride_on_the_seams(self):
        # t1 -> t2 'mid' -> true; t2 -> t3 is not a playlist seam here (t3 is missing), so its '4' is unused
        self.assertEqual(self.want("swap"), {"alb9-t1": True, "alb9-t2": None, "alb9-t4": None})

    def test_a_swap_change_reaches_a_waiting_entry(self):
        P.sync(self.status([("alb9-t1", (16.0, None)), ("alb9-t2", None), ("alb9-t4", None)], current=1))
        self.assertEqual([c["op"] for c in self.calls], ["playlist-remove", "playlist-add"])
        self.assertIs(self.calls[1]["entries"][0]["swap"], True)


if __name__ == "__main__":
    unittest.main()
