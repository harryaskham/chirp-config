#!/usr/bin/env python3
"""Composition mode (tools/chirpers.py, compscore.py, rate.py, climb.py's compose brief), against a scratch registry
(CLIMB_ROOT, no git): an album's empty tracks become compose climbs; the first agent names the album once; ratings
feed compscore's human term (a stale version's at half weight); a static loop scores low on structure and variety
while a sectioned piece does better; agents' measure plugins join the total.

  python3 tools/tests/test_compose.py      (from ~/.config/chirp; ~20 s)
"""
import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = tempfile.mkdtemp(prefix="compose-test-")
os.environ["CLIMB_ROOT"] = TMP
os.environ.pop("PI_SESSION_ID", None)
os.environ.pop("CLIMB_AS", None)
sys.path.insert(0, TOOLS)
import chirpers as CH  # noqa: E402
import compscore as CS  # noqa: E402
import likeness as L  # noqa: E402
import rate as RT  # noqa: E402

SPEC = {"artist": "Chirpers", "album": "Test Album (unnamed)", "year": 2026, "genre": "djent", "brief": "b",
        "bleed": True, "genre_refs": [], "weights": {"human": 0.3},
        "tracks": [{"n": 1, "role": "intro", "length": [100, 140], "brief": "open"},
                   {"n": 2, "role": "song", "length": [180, 240], "brief": "hit"},
                   {"n": 3, "role": "outro", "length": [450, 510], "brief": "close"}]}


def quiet(fn, *a):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*a)


def setUpModule():
    os.makedirs(os.path.join(TMP, "songs"), exist_ok=True)
    with open(os.path.join(TMP, "climbs.json"), "w") as f:
        json.dump({"climbs": [{"id": "old-song", "song": "songs/old-song.yaml", "status": "active", "rounds": 3}]}, f)
    spec = os.path.join(TMP, "spec.json")
    with open(spec, "w") as f:
        json.dump(SPEC, f)
    quiet(CH.main, ["new", "alb", "--spec", spec, "--no-git", "--as", "chirp-eco"])


def tearDownModule():
    shutil.rmtree(TMP, ignore_errors=True)


def reg():
    with open(os.path.join(TMP, "climbs.json")) as f:
        return {c["id"]: c for c in json.load(f)["climbs"]}


class Album(unittest.TestCase):
    def test_new_tracks_are_compose_climbs(self):
        r = reg()
        self.assertIn("old-song", r)
        for n in (1, 2, 3):
            c = r[f"alb-t{n}"]
            self.assertEqual((c["mode"], c["album"], c["status"]), ("compose", "alb", "requested"))
            self.assertEqual(c["metric"], f"python3 tools/compscore.py alb-t{n} OUT.wav")
            self.assertEqual(c["meta"]["album"], CH.load_album("alb")["album"])   # tests run in any order
        self.assertTrue(os.path.exists(os.path.join(TMP, "compose", "alb", "motifs.md")))

    def test_name_once_then_title(self):
        quiet(CH.main, ["name", "alb", "Gravity Wells", "--no-git", "--as", "chirper-one"])
        self.assertTrue(all(c["meta"]["album"] == "Gravity Wells" for k, c in reg().items() if k.startswith("alb-")))
        self.assertEqual(CH.load_album("alb")["named_by"], "chirper-one")
        with self.assertRaises(SystemExit):
            quiet(CH.main, ["name", "alb", "Another Name", "--no-git"])
        quiet(CH.main, ["title", "alb-t2", "Lattice", "--no-git"])
        self.assertEqual(reg()["alb-t2"]["meta"]["title"], "Lattice")
        self.assertEqual([t.get("title") for t in CH.load_album("alb")["tracks"] if t["n"] == 2], ["Lattice"])

    def test_compose_brief(self):
        c = CH.C.find(CH.C.load(), "alb-t1")
        text = CH.C.brief(c, [])
        self.assertIn("COMPOSITION", text)
        self.assertIn("compose it from scratch", text)
        self.assertIn("neighbours: 2 alb-t2", text)


class Ratings(unittest.TestCase):
    def test_harry_rating_feeds_human_with_stale_half_weight(self):
        quiet(RT.main, ["alb-t2", "7.5", "--note", "great intro riff", "--no-git"])
        quiet(RT.main, ["alb-t2", "6", "--who", "chirper-two", "--no-git"])
        rs = CS.ratings("alb")
        self.assertEqual([(r["who"], r["score"]) for r in rs], [("harry", 7.5), ("chirper-two", 6.0)])
        ctx = {"id": "alb-t2", "ratings": rs, "version": None, "owner": "chirper-one"}
        s, d = CS.m_human(ctx)
        self.assertEqual((s, d["weight_scale"]), (75.0, 1.0))
        ctx["version"] = "v3"
        rs[0]["version"] = "v1"
        self.assertEqual(CS.m_human(ctx)[1]["weight_scale"], 0.5)          # rated an older version
        self.assertEqual(CS.m_peer(ctx)[0], 60.0)                           # chirper-two, not the owner
        with self.assertRaises(SystemExit):
            quiet(RT.main, ["old-song", "5", "--no-git"])                   # only compositions are rated


def piece(sections, sr=L.SR):
    """Concatenated synthetic sections: (seconds, root Hz, pulse period s, level)."""
    out = []
    rng = np.random.default_rng(0)
    for sec, f0, period, lvl in sections:
        t = np.arange(int(sec * sr)) / sr
        x = lvl * 0.25 * (np.sin(2 * np.pi * f0 * t) + 0.5 * np.sin(2 * np.pi * 1.5 * f0 * t))
        for k in np.arange(0, sec, period):
            i, n = int(k * sr), int(0.05 * sr)
            x[i:i + n] += lvl * 0.6 * rng.standard_normal(min(n, len(x) - i)) * np.exp(-np.arange(min(n, len(x) - i)) / (0.008 * sr))
        out.append(x)
    x = np.concatenate(out)
    return np.stack([x, x], 1).astype(np.float32)


def ctx_of(x, album=None, others=None):
    F = L.Feat(x)
    dur = len(x) / L.SR
    X = CS.frames(F)
    secs = CS.section_feats(F, x, CS.section_bounds(F, dur, X), X)
    me = CS.features(x, F, dur)
    return {"id": "p", "x": x, "F": F, "dur": dur, "album": album or {"tracks": []}, "slot": {"length": [60, 90]},
            "sections": secs, "me": me, "density": me["density"], "others": others or {}, "ratings": [],
            "owner": None, "version": None, "envelope": None}


class Measures(unittest.TestCase):
    def test_loop_scores_below_a_sectioned_piece(self):
        loop = ctx_of(piece([(64, 110, 0.5, 1.0)]))
        song = ctx_of(piece([(16, 110, 0.5, 1.0), (16, 147, 0.375, 0.4), (16, 110, 0.5, 1.0), (16, 98, 0.3, 0.7)]))
        self.assertLess(len(loop["sections"]), len(song["sections"]))
        self.assertLess(CS.m_variety(loop)[0], CS.m_variety(song)[0])
        self.assertLess(CS.score(loop)["total"], CS.score(song)["total"])

    def test_plugin_and_weights(self):
        c = ctx_of(piece([(30, 110, 0.5, 1.0), (30, 147, 0.4, 0.5)]), album={"tracks": [], "weights": {"mine": 0.5}})
        base = CS.score(c)
        with_plugin = CS.score(c, {"mine": lambda ctx: (100.0, {"why": "test"})})
        self.assertIn("mine", with_plugin["terms"])
        self.assertGreater(with_plugin["total"], base["total"])
        self.assertNotIn("human", base["terms"])                          # no rating: the term is skipped, not 0

    def test_flow_and_distinct_need_neighbours(self):
        x = piece([(30, 110, 0.5, 1.0), (30, 147, 0.4, 0.5)])
        c = ctx_of(x)
        self.assertEqual(CS.m_flow(c)[0], None)
        twin = dict(c["me"])
        c2 = ctx_of(x, album={"tracks": [{"n": 1, "id": "a"}, {"n": 2, "id": "p"}]}, others={"a": twin})
        c2["slot"] = {"n": 2, "length": [60, 90]}
        self.assertLess(CS.m_distinct(c2)[0], 10.0)                          # an identical twin is not distinct
        self.assertIsNotNone(CS.m_flow(c2)[0])


if __name__ == "__main__":
    unittest.main()
