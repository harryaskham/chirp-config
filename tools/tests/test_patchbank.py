#!/usr/bin/env python3
"""Tests for tools/patchbank.py (hermetic: a fake planner; no engine, no audio)."""
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import patchbank as B  # noqa: E402


def kit(**pieces):
    return {"about": "a kit", "gain": "-9dB", "kit": {k: {"patch": {"synth": v}, "pitch": "C2"} for k, v in pieces.items()}}


def track(name, patch, pieces=(), fx=None):
    t = {"name": name, "patch": patch, "notes": [{"at": i, "pitch": p} for i, p in enumerate(pieces)]}
    if fx:
        t["fx"] = fx
    return t


def row(n, title, tracks, patches, own=(), ext=None):
    return {"n": n, "title": title, "version": "v3", "canon": {"tracks": tracks, "patches": patches},
            "own": set(own), "ext": ext or {}}


class Words(unittest.TestCase):
    def test_fields_and_base(self):
        self.assertEqual(B.base_of("ct-twin fx.1.tight=150"), "ct-twin")
        self.assertEqual(B.fields("ct-twin fx.1.tight=150 synth.layers.0.soft=expr.pm*0.5"),
                         {"fx.1.tight": "150", "synth.layers.0.soft": "expr.pm*0.5"})
        self.assertEqual(B.fields("twelve play.tuning='Eb2 Ab2' play.gate=1"), {"play.tuning": "Eb2 Ab2", "play.gate": "1"})

    def test_a_patch_that_plays_a_song_is_not_an_instrument(self):
        self.assertTrue(B.plays_a_song({"synth": {"layers": [{"song": "inner"}]}}))
        self.assertFalse(B.plays_a_song({"synth": {"layers": [{"wave": "saw"}]}}))

    def test_the_same_patch_but_for_its_about(self):
        self.assertTrue(B.same_patch({"about": "a", "gain": 1}, {"about": "b", "gain": 1}))
        self.assertFalse(B.same_patch({"gain": 1}, {"gain": 2}))

    def test_a_kits_pieces_are_written_into_it(self):
        pats = {"k1": {"kit": {"s": {"patch": "k1.s", "pitch": "A3"}, "x": {"patch": "noise", "pitch": "C5"}}},
                "k1.s": {"synth": "snare"}}
        out = B.inline_kit(pats["k1"], pats)
        self.assertEqual(out["kit"]["s"], {"patch": {"synth": "snare"}, "pitch": "A3"})
        self.assertEqual(out["kit"]["x"]["patch"], "noise")                                 # the library's own: by name
        self.assertEqual(pats["k1"]["kit"]["s"]["patch"], "k1.s")                           # the plan is not edited
        self.assertEqual(B.inline_kit({"synth": 1}, pats), {"synth": 1})

    def test_the_lanes_a_patch_reads(self):
        p = {"about": "not auto.this", "fx": [{"pos": {"mod": [{"src": "auto.wah"}]}}], "synth": {"pitch": "auto.fall*2+auto.wah"}}
        self.assertEqual(B.lanes_of(p), ["fall", "wah"])
        self.assertIn("IT READS THE TRACK'S AUTOMATION (`fall`, `wah`)", B.banked_about(p, "w", "d"))
        self.assertNotIn("AUTOMATION", B.banked_about({"synth": 1}, "w", "d"))

    def test_track_effects_are_fields_by_type(self):
        t = track("wl", "x", fx=[{"type": "cab", "model": "4x12", "mic": 0.5}, {"type": "eq", "bands": [{"gain": "1dB"}]},
                                 {"type": "cab", "model": "other"}])
        self.assertEqual(B.track_fx_fields(t), {"+cab.model": "4x12", "+cab.mic": "0.5"})


class Census(unittest.TestCase):
    def songs(self):
        out = []
        for n in range(1, 5):
            tracks = [track("l", "twin a=1 cone=%d" % n), track("r", "twin a=1 cone=%d" % (n + 10))]
            if n == 4:
                tracks = [track("l", "twin a=2"), track("r", "twin")]
            out.append((n, {"tracks": tracks}, set(), {}))
        return out

    def test_agreed_is_more_than_half_the_tracks_in_three_songs(self):
        cen = B.census(self.songs())
        r = cen["twin"]
        self.assertEqual((r["tracks"], r["songs"], r["plain"]), (8, [1, 2, 3, 4], [4]))
        self.assertEqual([(k, v, t) for k, v, t, _ in B.agreed(r)], [("a", "1", 6)])       # cone never agrees

    def test_half_is_not_agreed(self):
        songs = [(n, {"tracks": [track("l", "twin a=1"), track("r", "twin")]}, set(), {}) for n in (1, 2, 3)]
        self.assertEqual(B.agreed(B.census(songs)["twin"]), [])

    def test_a_band_is_one_decision(self):
        songs = [(n, {"tracks": [track("b", "bass fx.2.bands.3.cutoff=1150 fx.2.bands.3.gain=%ddB" % n)]}, set(), {})
                 for n in (1, 2, 3)]
        self.assertEqual(B.agreed(B.census(songs)["bass"]), [])                              # the cutoff agrees, the gain does not
        songs = [(n, {"tracks": [track("b", "bass fx.2.bands.3.cutoff=1150 fx.2.bands.3.gain=6dB")]}, set(), {})
                 for n in (1, 2, 3)]
        self.assertEqual(len(B.agreed(B.census(songs)["bass"])), 2)

    def test_a_songs_own_patch_counts_under_what_it_extends(self):
        songs = [(1, {"tracks": [track("k", "mine x=2")]}, {"mine"}, {"mine": "base y=1"})]
        r = B.census(songs)["base"]
        self.assertEqual(r["rows"], [(1, "k", {"y": "1", "x": "2"})])

    def test_the_document_marks_what_is_agreed(self):
        md = B.census_md(B.census(self.songs()), "album")
        self.assertIn("| `a` | 7 | 4 |", md)
        self.assertIn("AGREED", md)
        self.assertEqual(md.count("AGREED |"), 1)


class Kits(unittest.TestCase):
    def test_each_piece_from_the_track_that_plays_it(self):
        base = kit(k="kick", s="snare", h="hat")
        snare = kit(k="kick", s="SNARE2", h="hat")
        hat = kit(k="kickX", s="snare", h="HAT2")                     # its kick differs, and it does not play it
        out, merged, left = B.merge_kit([("kick", base, {"k"}), ("snare", snare, {"s"}), ("hat", hat, {"h"})])
        self.assertEqual((merged, left), (["kick", "snare", "hat"], []))
        self.assertEqual({p: d["patch"]["synth"] for p, d in out["kit"].items()}, {"k": "kick", "s": "SNARE2", "h": "HAT2"})

    def test_the_same_piece_with_another_sound_is_left_out(self):
        a, b = kit(k="kick", t="tom"), kit(k="kick", t="TOM-UP")
        out, merged, left = B.merge_kit([("toms", a, {"t"}), ("toms-up", b, {"t"})])
        self.assertEqual((merged, left), (["toms"], [1]))
        self.assertEqual(out["kit"]["t"]["patch"]["synth"], "tom")

    def test_a_track_that_differs_outside_the_pieces_is_left_out(self):
        a = kit(k="kick")
        b = dict(kit(k="kick", s="snare"), gain="-3dB")
        self.assertEqual(B.merge_kit([("kick", a, {"k"}), ("snare", b, {"s"})])[2], [1])

    def test_root(self):
        self.assertEqual(B.root_of("hat-kit", {"hat-kit", "here"}, {"hat-kit": "here x=1", "here": "ct-kit"}), "ct-kit")
        self.assertEqual(B.root_of("deck", {"deck"}, {}), "deck")


class Instruments(unittest.TestCase):
    def rows(self):
        lib, here = kit(k="kick", s="snare", h="hat", t="tom"), kit(k="KICK-HERE", s="snare", h="hat", t="tom")
        snare = kit(k="kick", s="SNARE-G3", h="hat", t="tom")
        up = kit(k="KICK-UP", s="snare", h="hat", t="TOM-UP")
        one = row(1, "So Far", [track("kick", "ct-kit-here", "k"), track("snare", "ct-kit kit.s.pitch=G3", "s"),
                                track("toms", "ct-kit", "t"), track("kick-up", "ct-kit-here-up", "k"),
                                track("toms-up", "ct-kit-here-up", "t"), track("bow", "sf-bow"),
                                track("tape", "sf-tape"), track("lead", "sf-lead cutoff=2"), track("pencil", "pencil.patch")],
                  {"ct-kit-here": here, "ct-kit kit.s.pitch=G3": snare, "ct-kit": lib, "ct-kit-here-up": up,
                   "sf-bow": {"about": "a bow", "synth": 1}, "sf-tape": {"synth": {"layers": [{"song": "inner"}]}},
                   "sf-lead cutoff=2": {"synth": 2}, "pencil.patch": {"synth": 3}},
                  own={"ct-kit-here", "ct-kit-here-up", "sf-bow", "sf-tape", "sf-lead"},
                  ext={"ct-kit-here": "ct-kit", "ct-kit-here-up": "ct-kit-here"})
        two = row(2, "Plain Hunt", [track("kit", "ct-kit", "ks"), track("deck", "deck", "x")],
                  {"ct-kit": lib, "deck": kit(x="deck")}, own={"deck"})
        return [one, two]

    def test_what_is_banked_and_under_what_name(self):
        items, skipped = B.instruments(self.rows(), taken={"ct-kit", "piano"})
        names = {name: patch for name, patch, _ in items}
        self.assertEqual(sorted(names), ["ct-kit-so-far", "ct-kit-so-far-up", "deck", "sf-bow", "sf-lead", "so-far-pencil"])
        k = names["ct-kit-so-far"]["kit"]
        self.assertEqual({p: d["patch"]["synth"] for p, d in k.items()},
                         {"k": "KICK-HERE", "s": "SNARE-G3", "h": "hat", "t": "tom"})
        up = names["ct-kit-so-far-up"]["kit"]
        self.assertEqual((up["k"]["patch"]["synth"], up["t"]["patch"]["synth"]), ("KICK-UP", "TOM-UP"))
        self.assertEqual(names["sf-lead"], {"synth": 2})                                     # as played, with its override
        self.assertEqual(skipped, [(1, "sf-tape", "plays a song inside the song")])
        where = {name: w for name, _, w in items}
        self.assertEqual(where["ct-kit-so-far"], "So Far v3 (tracks kick, snare, toms)")

    def test_the_librarys_kit_as_it_comes_is_not_banked(self):
        items, _ = B.instruments(self.rows()[1:], taken=set())
        self.assertEqual([name for name, _, _ in items], ["deck"])

    def test_a_name_something_else_has_gains_the_title(self):
        rows = [row(1, "So Far", [track("p", "piano")], {"piano": {"synth": 9}}, own={"piano"})]
        d = tempfile.mkdtemp()
        self.assertEqual([n for n, _, _ in B.instruments(rows, {"piano"}, d)[0]], ["piano-so-far"])

    def test_a_name_this_tool_banked_before_is_kept(self):
        rows = [row(1, "So Far", [track("p", "sf-bow")], {"sf-bow": {"synth": 9}}, own={"sf-bow"})]
        d = tempfile.mkdtemp()
        with open(os.path.join(d, "sf-bow.yaml"), "w") as f:
            json.dump({"about": B.MARK + " (d) from x", "synth": 8}, f)
        self.assertEqual([n for n, _, _ in B.instruments(rows, {"sf-bow"}, d)[0]], ["sf-bow"])
        with open(os.path.join(d, "sf-bow.yaml"), "w") as f:
            json.dump({"about": "a composer's own", "synth": 8}, f)
        self.assertEqual([n for n, _, _ in B.instruments(rows, {"sf-bow"}, d)[0]], ["sf-bow-so-far"])

    def test_the_same_instrument_in_two_songs_is_one_file(self):
        rows = [row(n, t, [track("b", "bell")], {"bell": {"synth": 9}}, own={"bell"}) for n, t in ((1, "One"), (2, "Two"))]
        self.assertEqual([n for n, _, _ in B.instruments(rows, taken=set())[0]], ["bell"])
        rows[1]["canon"]["patches"]["bell"] = {"synth": 8}
        self.assertEqual([n for n, _, _ in B.instruments(rows, taken=set())[0]], ["bell-one", "bell-two"])


class Bank(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def plan(self, wrong=()):
        def plan(path):
            with open(path) as f:
                doc = json.load(f)
            out = {}
            for t in doc["tracks"]:
                with open(os.path.join(self.dir, t["patch"] + ".yaml")) as f:
                    out[t["patch"]] = json.load(f)
                if t["patch"] in wrong:
                    out[t["patch"]]["gain"] = "moved"
            return {"patches": out}
        return plan

    def test_new_same_changed(self):
        items = [("a", {"synth": 1}, "So Far v3 (track a)")]
        res = B.bank(items, self.plan(), set(), "22 Nov 2026", dirpath=self.dir)
        self.assertEqual((res["new"], res["same"], res["changed"]), (["a"], [], []))
        with open(os.path.join(self.dir, "a.yaml")) as f:
            about = json.load(f)["about"]
        self.assertIn(B.MARK, about)
        self.assertIn("So Far v3 (track a)", about)
        res = B.bank([("a", {"synth": 1}, "So Far v9 (track a)")], self.plan(), {"a"}, "23 Nov 2026", dirpath=self.dir)
        self.assertEqual((res["new"], res["same"]), ([], ["a"]))                             # unchanged: not rewritten
        with open(os.path.join(self.dir, "a.yaml")) as f:
            self.assertEqual(json.load(f)["about"], about)
        res = B.bank([("a", {"synth": 2}, "w")], self.plan(), {"a"}, "23 Nov 2026", dirpath=self.dir, guard=lambda t: True)
        self.assertEqual(res["changed"], ["a"])

    def test_a_changed_file_a_song_uses_is_held(self):
        B.bank([("a", {"synth": 1}, "w")], self.plan(), set(), "d", dirpath=self.dir)
        seen = {}
        res = B.bank([("a", {"synth": 2}, "w"), ("b", {"synth": 3}, "w")], self.plan(), {"a"}, "d", dirpath=self.dir,
                     guard=lambda texts: seen.update(texts) or False)
        self.assertEqual((res["held"], res["changed"], res["new"]), (["a"], [], ["b"]))
        self.assertEqual(list(seen), [os.path.join("patches", "a.yaml")])
        with open(os.path.join(self.dir, "a.yaml")) as f:
            self.assertEqual(json.load(f)["synth"], 1)

    def test_a_taken_name_is_refused_and_another_tools_file_is_never_overwritten(self):
        with open(os.path.join(self.dir, "theirs.yaml"), "w") as f:
            json.dump({"about": "a composer's", "synth": 0}, f)
        res = B.bank([("theirs", {"synth": 1}, "w"), ("piano", {"synth": 1}, "w")], self.plan(), {"piano", "theirs"}, "d",
                     dirpath=self.dir)
        self.assertEqual(sorted(res["refused"]), ["piano", "theirs"])
        with open(os.path.join(self.dir, "theirs.yaml")) as f:
            self.assertEqual(json.load(f)["synth"], 0)

    def test_one_that_does_not_come_back_the_same_is_removed(self):
        res = B.bank([("a", {"synth": 1}, "w"), ("b", {"synth": 1}, "w")], self.plan(wrong={"b"}), set(), "d", dirpath=self.dir)
        self.assertEqual((res["new"], res["wrong"]), (["a"], ["b"]))
        self.assertFalse(os.path.exists(os.path.join(self.dir, "b.yaml")))

    def test_one_that_does_not_plan_does_not_hide_the_others(self):
        inner = self.plan()

        def plan(path):
            with open(path) as f:
                if any(t["patch"] == "bad" for t in json.load(f)["tracks"]):
                    raise SystemExit("does not plan")
            return inner(path)
        res = B.bank([("a", {"synth": 1}, "w"), ("bad", {"synth": 1}, "w")], plan, set(), "d", dirpath=self.dir)
        self.assertEqual((res["new"], res["wrong"]), (["a"], ["bad"]))
        self.assertEqual(os.listdir(self.dir), ["a.yaml"])

    def test_dry_writes_nothing(self):
        res = B.bank([("a", {"synth": 1}, "w")], self.plan(), set(), "d", dirpath=self.dir, dry=True)
        self.assertEqual(res["new"], ["a"])
        self.assertEqual(os.listdir(self.dir), [])

    def test_the_about_keeps_the_patchs_own_words_once(self):
        a = B.banked_about({"about": "the bow of Still Owing."}, "Still Owing v35 (track bow)", "22 Nov 2026")
        self.assertTrue(a.startswith("the bow of Still Owing. " + B.MARK))
        again = B.banked_about({"about": a}, "Still Owing v36 (track bow)", "23 Nov 2026")
        self.assertEqual(again.count(B.MARK), 1)
        self.assertIn("v36", again)

    def test_track_effects_go_after_the_patchs(self):
        out = B.with_track_fx({"fx": [{"type": "amp"}]}, {"fx": [{"type": "cab"}]})
        self.assertEqual([e["type"] for e in out["fx"]], ["amp", "cab"])


class Successors(unittest.TestCase):
    def test_the_agreed_settings_and_the_agreed_effect(self):
        rows, songs = [], []
        for n in (1, 2, 3):
            cab = {"type": "cab", "model": "4x12", "cone": 50 + n}
            tr = [track("wl", "wall fx.3.mix=0 thump=%d" % n, fx=[cab, {"type": "eq", "bands": []}])]
            r = row(n, "Song %d" % n, tr, {})
            rows.append(r)
            songs.append((n, r["canon"], set(), {}))
        cen = B.census(songs)

        def plan(path):
            with open(path) as f:
                ref = json.load(f)["tracks"][0]["patch"]
            return {"patches": {ref: {"about": "the wall", "fx": [{"type": "amp"}], "resolved": ref}}}
        items, left = B.successors(cen, rows, plan, set())
        self.assertEqual(left, [])
        (name, patch, where), = items
        self.assertEqual(name, "wall-2")
        self.assertEqual(patch["resolved"], "wall fx.3.mix=0")                              # thump is each song's
        self.assertEqual(patch["fx"], [{"type": "amp"}, {"type": "cab", "model": "4x12", "cone": 51}])
        self.assertIn("`fx.3.mix=0` (3 of 3 tracks, 3 songs)", where)
        self.assertIn("NOT HEARD", where)

    def test_a_kit_is_left_to_promote(self):
        songs = [(n, {"tracks": [track("s", "ct-kit kit.s.pitch=G3")]}, set(), {}) for n in (1, 2, 3)]
        items, left = B.successors(B.census(songs), [], lambda p: {}, set(), kits={"ct-kit"})
        self.assertEqual((items, left[0][0]), ([], "ct-kit"))


class Index(unittest.TestCase):
    def test_the_index(self):
        md = B.index_md([("b", {"about": "a bow. " + B.MARK + " (d) from x"}, "So Far v3 (track bow)"),
                         ("a", kit(k="kick"), "So Far v3 (tracks kick)")], "album", "promote")
        self.assertLess(md.index("| `a` |"), md.index("| `b` |"))
        d = tempfile.mkdtemp()                                   # the file's own word for where it came from wins
        B.write_patch("b", {"about": B.banked_about({"about": "a bow."}, "So Far v2 (track bow)", "d"), "synth": 1}, d)
        md2 = B.index_md([("b", {"about": "a bow."}, "So Far v3 (track bow)")], "album", "promote", d)
        self.assertIn("| `b` | So Far v2 (track bow) | a bow. |", md2)
        self.assertIn("| `b` | So Far v3 (track bow) | a bow. |", md)
        self.assertIn("a kit of 1 pieces.", md)

    def test_notes_are_stripped_for_the_archive(self):
        self.assertEqual(B.strip_notes({"tracks": [{"name": "a", "notes": [1], "tracks": [{"notes": [2], "gain": 1}]}]}),
                         {"tracks": [{"name": "a", "tracks": [{"gain": 1}]}]})


if __name__ == "__main__":
    unittest.main()
