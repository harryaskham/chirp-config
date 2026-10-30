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
        self.assertIn("SONGWRITING", text)
        self.assertIn("IN REAL TIME", text)
        self.assertIn("compose it from scratch", text)
        self.assertIn("neighbours: 2 alb-t2", text)


class Done(unittest.TestCase):
    def test_first_kept_version_makes_the_composer_owner(self):
        with open(os.path.join(TMP, "songs", "alb-t3.yaml"), "w") as f:
            f.write("tempo: 120\n")
        quiet(CH.C.cmd_done, ["alb-t3", "--version", "v1", "--score", "70", "--note", "composed", "--no-git",
                              "--as", "chirper-two"])
        c = reg()["alb-t3"]
        self.assertEqual((c["status"], c["owner"], c["enabled"]), ("active", "chirper-two", True))


class Rebaseline(unittest.TestCase):
    def test_apply_rescore_keeps_the_old_score_and_notes_it(self):
        c = {"id": "x", "rounds": 4, "best": {"score": 97.54, "version": "v2"}}
        h = CH.apply_rescore(c, {0: 95.6861, 11: 95.968}, "abc123", "chirp-eco", "2026-10-28T12:40:00Z")
        self.assertEqual(c["best"]["score"], 95.686)
        self.assertEqual(c["best"]["rescored"], {"compscore": "abc123", "seeds": {"0": 95.686, "11": 95.968},
                                                 "at": "2026-10-28T12:40:00Z", "was": 97.54})
        self.assertTrue(h["steer"])
        self.assertIn("v2 (the song file) scores 95.686/95.968 on seeds 0/11", h["note"])


class Keep(unittest.TestCase):
    def test_keep_records_a_judged_version_for_compositions_only(self):
        with open(os.path.join(TMP, "songs", "alb-t1.yaml"), "w") as f:
            f.write("tempo: 80\n")
        quiet(CH.C.cmd_done, ["alb-t1", "--version", "v1", "--score", "90", "--note", "v1", "--no-git", "--as", "c3"])
        quiet(CH.C.cmd_done, ["alb-t1", "--version", "v2", "--score", "89.9", "--note", "by ear", "--keep", "--no-git",
                              "--as", "c3"])
        b = reg()["alb-t1"]["best"]
        self.assertEqual((b["version"], b["score"], b.get("judged")), ("v2", 89.9, True))
        quiet(CH.C.cmd_done, ["alb-t1", "--version", "v3", "--score", "91", "--note", "wins", "--no-git", "--as", "c3"])
        self.assertNotIn("judged", reg()["alb-t1"]["best"])                 # a scored win clears the flag
        with self.assertRaises(SystemExit):
            quiet(CH.C.cmd_done, ["old-song", "--version", "v9", "--score", "1", "--note", "x", "--keep", "--no-git"])


class LatestRatings(unittest.TestCase):
    def test_a_note_after_a_score_keeps_the_score(self):
        # Harry, 30 Oct: "10.0/10" then a note "genuine banger" crashed chirpers.py status (KeyError: 'score')
        d = os.path.join(TMP, "compose", "lr")
        os.makedirs(d, exist_ok=True)
        rows = [{"id": "x", "who": "harry", "score": 10.0}, {"id": "x", "who": "harry", "note": "genuine banger"},
                {"id": "y", "who": "harry", "note": "too busy"}, {"id": "y", "who": "harry", "score": 4.0},
                {"id": "z", "who": "harry", "note": "only a note"}]
        with open(os.path.join(d, "ratings.jsonl"), "w") as f:
            f.write("".join(json.dumps(r) + "\n" for r in rows))
        rt = CH.latest_ratings("lr")
        self.assertEqual((rt["x"]["harry"]["score"], rt["x"]["harry"]["note"]), (10.0, "genuine banger"))
        self.assertEqual((rt["y"]["harry"]["score"], rt["y"]["harry"]["note"]), (4.0, "too busy"))
        self.assertNotIn("score", rt["z"]["harry"])


class RebaselineRace(unittest.TestCase):
    def test_a_round_landing_mid_run_changes_the_snapshot(self):
        before = {"rounds": 12, "best": {"version": "v8", "score": 97.735}}
        self.assertEqual(CH.snapshot(before), (12, "v8"))
        after = {"rounds": 13, "best": {"version": "v9", "score": 98.003}}   # Thirteen Teeth, 28 Oct 23:09
        self.assertNotEqual(CH.snapshot(before), CH.snapshot(after))


class Ratings(unittest.TestCase):
    def test_harry_rating_feeds_human_with_stale_half_weight(self):
        quiet(RT.main, ["alb-t2", "7.5", "--note", "great intro riff", "--no-git"])
        quiet(RT.main, ["alb-t2", "6", "--who", "chirper-two", "--no-git"])
        rs = [r for r in CS.ratings("alb") if r["id"] == "alb-t2"]   # the album file also holds other tracks' ratings
        self.assertEqual([(r["who"], r["score"]) for r in rs], [("harry", 7.5), ("chirper-two", 6.0)])
        ctx = {"id": "alb-t2", "ratings": rs, "version": None, "owner": "chirper-one"}
        s, d = CS.m_human(ctx)
        self.assertEqual((s, d["weight_scale"]), (75.0, 1.0))
        ctx["version"] = "v3"
        rs[0]["version"] = "v1"
        self.assertEqual(CS.m_human(ctx)[1]["weight_scale"], 0.5)          # rated an older version
        self.assertEqual(CS.m_peer(ctx)[0], 60.0)                           # chirper-two, not the owner
        rs += [{"id": "alb-t2", "who": "harry", "note": "a note, no score"}, {"id": "alb-t2", "who": "chirper-zero", "note": "n"}]
        self.assertEqual((CS.m_human(ctx)[0], CS.m_peer(ctx)[0]), (75.0, 60.0))   # note-only entries never crash or count
        with self.assertRaises(SystemExit):
            quiet(RT.main, ["old-song", "5", "--no-git"])                   # only compositions are rated

    def test_a_rating_makes_the_best_stale_until_it_is_re_measured(self):
        # chirper-three, 29 Oct: Harry rated Hail on a Music Box v3 8.0; like for like v3 fell 98.15 -> 92.50, and v4's
        # 92.58 was logged as not kept against the stored pre-rating 98.15
        with open(os.path.join(TMP, "songs", "alb-t3.yaml"), "w") as f:
            f.write("tempo: 86\n")
        quiet(CH.C.cmd_done, ["alb-t3", "--version", "v3", "--score", "98.15", "--note", "v3", "--no-git", "--as", "chirper-two"])
        quiet(RT.main, ["alb-t3", "6", "--who", "chirper-two", "--no-git"])           # the owner's own rating: not a term
        self.assertNotIn("stale", reg()["alb-t3"]["best"])
        quiet(RT.main, ["alb-t3", "8", "--note", "glitch resample", "--no-git"])
        st = reg()["alb-t3"]["best"]["stale"]
        self.assertEqual((st["who"], st["rating"], st["version"], st["score"]), ("harry", 8.0, "v3", 98.15))
        self.assertIn("BEST IS STALE: 98.15 (v3)", "\n".join(CH.C.compose_brief(reg()["alb-t3"])))
        rounds = reg()["alb-t3"]["rounds"]
        with self.assertRaises(SystemExit):                                  # refuses an unfair comparison, records nothing
            quiet(CH.C.cmd_done, ["alb-t3", "--version", "v4", "--score", "92.58", "--note", "v4", "--no-git", "--as", "chirper-two"])
        self.assertEqual(reg()["alb-t3"]["rounds"], rounds)
        quiet(CH.C.cmd_done, ["alb-t3", "--version", "v4", "--score", "92.58", "--best-now", "92.50", "--note", "v4",
                              "--no-git", "--as", "chirper-two"])
        b = reg()["alb-t3"]["best"]
        self.assertEqual((b["version"], b["score"]), ("v4", 92.58))          # kept like for like
        self.assertNotIn("stale", b)
        quiet(CH.C.cmd_done, ["alb-t3", "--version", "v5", "--score", "92.0", "--note", "worse", "--no-git", "--as", "chirper-two"])
        self.assertEqual(reg()["alb-t3"]["best"]["version"], "v4")          # an ordinary loss records as before
        c = {"best": {"score": 92.58, "version": "v4", "stale": {"since": "x"}}, "rounds": 3}
        CH.apply_rescore(c, {0: 92.4}, "r", "eco", "t")
        self.assertNotIn("stale", c["best"])                                # a rebaseline clears it too

    def test_now_resolves_the_playing_climb(self):
        ids = {"alb-t1", "alb-t3"}
        self.assertEqual(RT.resolve_now({"label": "alb-t3"}, ids), "alb-t3")
        entries = [{"label": "alb-t1"}, {"label": "alb-t3"}]
        self.assertEqual(RT.resolve_now({"label": "F2,C3/1+1", "playlist": {"current": 0, "entries": entries}}, ids), "alb-t1")
        self.assertEqual(RT.resolve_now({"label": "x", "playlist": {"current": {"label": "alb-t3"}}}, ids), "alb-t3")
        with self.assertRaises(SystemExit) as e:
            RT.resolve_now({"label": "F2,C3/1+1+1", "playlist": {"current": None, "entries": entries}}, ids)
        self.assertIn("rate it by id", str(e.exception))


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

    def test_fft_autocorr_and_tempo_match_the_direct_forms(self):
        o = np.random.default_rng(3).standard_normal(4000)
        self.assertLess(float(np.abs(CS.autocorr(o, 500) - np.correlate(o, o, "full")[3999:4499]).max()), 1e-9)
        F = L.Feat(piece([(20, 110, 0.4, 1.0)]))
        self.assertAlmostEqual(CS.tempo(F.onset), L.tempo(F.onset), places=6)

    def test_spectrum_tolerates_a_clean_track(self):
        c = ctx_of(piece([(30, 110, 0.5, 1.0), (30, 147, 0.4, 0.5)]))
        c["envelope"] = CS.profile(c["F"]) + np.where(np.arange(40) % 2, 5.0, -5.0)     # 5 dB off in every band
        self.assertEqual(CS.m_spectrum(c)[0], 100.0)                                     # within the 6 dB default
        c["album"] = {"tracks": [], "spectrum_tolerance_db": 3.0}
        self.assertLess(CS.m_spectrum(c)[0], 60.0)

    def test_declared_tempo_sets_the_rhythm_grid(self):
        d = tempfile.mkdtemp(dir=TMP)
        for name, text in (("a.yaml", "about: x\ntempo: 96  # bpm\ntracks:\n  - name: g\n"), ("b.json", '{"tempo": 128}'),
                           ("c.yaml", "about: none\n")):
            with open(os.path.join(d, name), "w") as f:
                f.write(text)
        self.assertEqual([CS.declared_tempo(os.path.join(d, n)) for n in ("a.yaml", "b.json", "c.yaml", "missing")],
                         [96.0, 128.0, None, None])
        c = ctx_of(piece([(30, 110, 0.5, 1.0), (30, 147, 0.375, 0.6)]))
        est = CS.m_rhythm(c)[1]
        self.assertFalse(est["declared"])
        c["bpm"] = 120.0
        dec = CS.m_rhythm(c)[1]
        self.assertEqual((dec["declared"], dec["tempo"], dec["pulse_estimate"]), (True, 120.0, est["pulse_estimate"]))

    def test_recurrence_is_continuous_at_the_old_threshold(self):
        def ctx(sim):
            v0, v1 = np.array([1.0, 0.0]), np.array([0.0, 1.0])
            v3 = np.array([sim, np.sqrt(1 - sim * sim)])
            return {"sections": [{"vec": v} for v in (v0, v1, v1 * -1, v3)]}
        lo, hi = CS.m_recurrence(ctx(0.598))[0], CS.m_recurrence(ctx(0.62))[0]
        self.assertLess(abs(hi - lo), 5.0)                     # was 18.9 vs 57.4 across a hard 0.6 cut

    def test_structure_tolerates_record_like_section_lengths(self):
        def ctx(lens):
            t, secs = 0.0, []
            for n in lens:
                secs.append({"a": t, "b": t + n})
                t += n
            return {"sections": secs, "dur": t}
        a = CS.m_structure(ctx([61, 10, 10, 10, 11, 20, 19, 62, 61, 81, 41, 51, 20, 36]))[0]   # cv .66
        b = CS.m_structure(ctx([61, 10, 10, 10, 11, 20, 19, 123, 81, 41, 51, 20, 36]))[0]      # one merge: cv .86
        self.assertEqual((a, b), (100.0, 100.0))

    def test_flow_grades_large_joins(self):
        def flow(jump):
            me = {"head": {"level": -20.0, "profile": [0.0] * 40}, "tail": {"level": -20.0, "profile": [0.0] * 40}}
            nb = {"head": {"level": -20.0, "profile": [0.0] * 40}, "tail": {"level": -20.0 - jump, "profile": [0.0] * 40}}
            ctx = {"others": {"a": nb}, "slot": {"n": 2}, "album": {"tracks": [{"n": 1, "id": "a"}, {"n": 2, "id": "p"}]},
                   "me": me}
            return CS.m_flow(ctx)[0]
        self.assertEqual(flow(4.0), 100.0)
        wb = CS.worst_bands([0.0] * 39 + [12.0], [0.0] * 39 + [-6.0], n=1)
        self.assertEqual(wb, [(14792, 18.0)])                 # the top band (centre ~14.8 kHz) sticks out by 18 dB
        self.assertGreater(flow(14.0) - flow(23.0), 10.0)     # was 6.8 vs 0.7 of a 50-point half: no gradient

    def test_music_end_ignores_a_dead_stop_s_silence(self):
        # chirper-zero, 29 Oct: a tapestop on the last bar leaves seconds of digital silence that section_bounds read as
        # a section of its own (Window Seat: total 92.25 -> 96.65); sections now end where the music does
        sr = 48000
        t = np.arange(10 * sr) / sr
        x = np.stack([0.3 * np.sin(2 * np.pi * 220 * t)] * 2, 1)
        x[7 * sr:] = 0.0                                                     # the deck stops at 7 s
        x[int(6.9 * sr):7 * sr] *= np.linspace(1, 0.0005, int(0.1 * sr))[:, None]
        self.assertAlmostEqual(CS.music_end(x, sr), 7.0, places=1)
        self.assertAlmostEqual(CS.music_end(x[:7 * sr], sr), 7.0, places=1)   # no tail: unchanged
        x[int(8.5 * sr):int(8.6 * sr)] = 1e-4                                # -80 dBFS hiss is still silence
        self.assertAlmostEqual(CS.music_end(x, sr), 7.0, places=1)
        self.assertEqual(CS.music_end(np.zeros((sr, 2)), sr), 1.0)          # all silent: the whole length

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
