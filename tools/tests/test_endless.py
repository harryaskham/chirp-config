#!/usr/bin/env python3
"""tools/endless.py: does the endless thing hold?

Hermetic: made songs and a stand-in engine that plays a track by its "fake" kind, so each answer is known:
  shepard  octave-spaced sines under a fixed bell, gliding an octave a bar for ever (a true Shepard glide)
  riser    one sine that climbs an octave a bar and starts again (the saw-tooth the illusion hides)
  climb    one sine that really climbs, a quarter octave a bar
  turns    the shepard, 1.5 dB louder on every third bar (parts taking turns: a longer cycle)
  speeds   a Shepard glide that SPEEDS UP: an octave every two bars for four bars, an octave in the fifth bar, then two
           octaves a bar; speeds-loud is 6 dB louder from the fifth bar (speeds-odd: only on an odd --seed); speeds-saw
           is the riser at those speeds

  python3 tools/tests/test_endless.py      (from ~/.config/chirp; a few seconds)
"""
import contextlib
import io
import json
import os
import shutil
import stat
import sys
import tempfile
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import endless as E  # noqa: E402

ENGINE = r'''#!/usr/bin/env python3
import json, sys, wave
import numpy as np
a = sys.argv[1:]
import os
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "calls.log"), "a") as f:
    f.write(" ".join(a) + "\n")
song = json.load(open(a[a.index("-f") + 1]))
solo = [a[i + 1] for i, v in enumerate(a) if v == "--solo"]
bar = 4 * 60.0 / song.get("tempo", 120)
def pos(tok):
    return float(tok[:-1]) if tok.endswith("s") else float(tok[:-1]) * bar / 4 if tok.endswith("b") else (float(tok) - 1) * bar
t0, t1 = pos(a[a.index("--from") + 1]), pos(a[a.index("--to") + 1])
sr = 24000
t = t0 + np.arange(int(round((t1 - t0) * sr))) / sr
out = np.zeros(len(t))
for tr in song["tracks"]:
    if solo and tr["name"] not in solo:
        continue
    kind, u = tr.get("fake"), t / bar
    if kind in ("shepard", "turns"):
        y = np.zeros(len(t))
        for j in range(-40, 6):
            p = j + u                                        # this component's place in six octaves
            w = np.where((p >= 0) & (p < 6), 0.5 - 0.5 * np.cos(2 * np.pi * p / 6), 0.0)
            y += w * np.sin(2 * np.pi * 55 * 2.0 ** j * bar / np.log(2) * (2.0 ** u - 1))
        if kind == "turns":
            y *= np.where(np.floor(u) % 3 == 2, 10 ** (1.5 / 20), 1.0)
        out += 0.1 * y
    elif kind == "riser":
        f = 220 * 2.0 ** (u % 1)
        out += 0.3 * np.sin(2 * np.pi * np.cumsum(f) / sr)
    elif kind == "climb":
        out += 0.3 * np.sin(2 * np.pi * 110 * bar * 4 / np.log(2) * (2.0 ** (u / 4) - 1))
    elif kind in ("speeds", "speeds-loud", "speeds-odd", "speeds-saw"):
        uu = np.where(u < 4, u / 2, np.where(u < 5, 2 + (u - 4), 3 + 2 * (u - 5)))       # octaves so far
        if kind == "speeds-saw":
            out += 0.3 * np.sin(2 * np.pi * np.cumsum(220 * 2.0 ** (uu % 1)) / sr)
        else:
            y = np.zeros(len(t))
            for j in range(-12, 6):
                p = j + uu
                w = np.where((p >= 0) & (p < 6), 0.5 - 0.5 * np.cos(2 * np.pi * p / 6), 0.0)
                y += w * np.sin(2 * np.pi * np.cumsum(55 * 2.0 ** np.clip(p, 0, 6)) / sr)
            loud = kind == "speeds-loud" or (kind == "speeds-odd" and int(a[a.index("--seed") + 1]) % 2 == 1)
            out += 0.1 * y * (np.where(u >= 4, 2.0, 1.0) if loud else 1.0)
with wave.open(a[a.index("-o") + 1], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes((np.repeat(np.clip(out, -1, 1)[:, None], 2, axis=1) * 32767).astype("<i2").tobytes())
'''


def notes(bars, places=((0, "F2"), (1, "G2"), (2.5, "C3"))):
    return [{"at": 4 * b + at, "pitch": p, "dur": 0.5} for b in range(bars) for at, p in places]


SONG = {"tempo": 120, "tracks": [
    {"name": "stair", "fake": "shepard", "notes": notes(8)},
    {"name": "riser", "fake": "riser", "notes": notes(8)},
    {"name": "climb", "fake": "climb", "notes": notes(8)},
    {"name": "turns", "fake": "turns", "notes": notes(12)},
    {"name": "kit", "fake": None, "notes": []},
    {"name": "speeds", "fake": "speeds", "notes": [{"at": at, "pitch": "F2", "dur": 0.5} for at in (0, 8, 16, 20, 22, 24, 26)]},
    {"name": "louder", "fake": "speeds-loud", "notes": []},
    {"name": "again", "fake": "speeds-saw", "notes": []},
    {"name": "moody", "fake": "speeds-odd", "notes": []},
]}
SPEEDS = ("1-8", "--cycles", "2x2bars,1bar,4x2b", "--steps", "8")


class Endless(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="endless-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        os.makedirs(os.path.join(self.root, "songs"))
        self.engine = os.path.join(self.root, "fake-chirp")
        with open(self.engine, "w") as f:
            f.write(ENGINE)
        os.chmod(self.engine, os.stat(self.engine).st_mode | stat.S_IXUSR)
        self.song = os.path.join(self.root, "songs", "x.yaml")
        self.write(SONG)
        old = E.ROOT
        E.ROOT = self.root
        self.addCleanup(setattr, E, "ROOT", old)

    def write(self, doc):
        with open(self.song, "w") as f:
            json.dump(doc, f)

    def run_tool(self, *args):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = E.main([*args, "--pin", self.engine])
        return code, buf.getvalue()

    def read(self, track, span="1-9", cycle="1bar"):
        return json.loads(self.run_tool(self.song, track, span, "--cycle", cycle, "--json")[1])

    def test_a_true_stair_holds(self):
        got = self.read("stair")
        self.assertEqual((got["cycles"], got["marks"]), (8, []))
        self.assertLess(got["level_spread"], 0.5)
        self.assertLess(abs(got["centroid_drift"]), 0.02)
        self.assertLess(abs(got["runs"]["centroid"]), E.SAW_OCT)
        self.assertEqual(got["plan"], {"cycles": 8, "notes": 3, "differ": []})
        code, text = self.run_tool(self.song, "stair", "1-9", "--cycle", "1bar")
        self.assertEqual(code, 0)
        self.assertIn("x.yaml stair: 1-9, 8 cycles of 1bar (2.000 s), alone through their own effects, bus and master", text)
        self.assertIn("the song    8 cycles of 3 notes, the same notes at the same places in every one", text)
        self.assertIn("IT HOLDS: one cycle later it is the same, and nothing starts again at the wrap.", text)

    def test_a_riser_that_starts_again_is_a_saw_tooth(self):
        got = self.read("riser")
        self.assertEqual([m for m, _ in got["marks"]], ["SAW-TOOTH"])
        self.assertAlmostEqual(got["runs"]["centroid"], 1.0, delta=0.1)       # an octave through the cycle
        self.assertAlmostEqual(got["wraps"]["centroid"], -0.94, delta=0.1)    # and back down at the wrap
        self.assertLess(abs(got["centroid_drift"]), 0.02)                     # one cycle later it IS the same
        _, text = self.run_tool(self.song, "riser", "1-9", "--cycle", "1bar")
        self.assertIn("SAW-TOOTH: the brightness runs +1.0", text)
        self.assertNotIn("IT HOLDS", text)

    def test_a_real_climb_is_a_drift(self):
        got = self.read("climb")
        self.assertEqual([m for m, _ in got["marks"]], ["DRIFT"])
        self.assertAlmostEqual(got["centroid_drift"], 0.25, delta=0.02)
        self.assertAlmostEqual(got["centroid_all"], 1.75, delta=0.1)
        self.assertIn("it is going somewhere (a real octave a cycle would read 1.00)", got["marks"][0][1])

    def test_few_cycles_cannot_show_a_small_drift(self):
        """Two cycles 0.10 octaves apart are inside what neighbouring cycles of a passage that holds differ by: not marked,
        and said so. The same over seven cycles is a drift; a real climb is one on two."""
        self.assertEqual([round(E.drift_floor(n), 3) for n in (2, 3, 4, 7, 40)], [0.127, 0.064, 0.05, 0.05, 0.05])
        got = self.read("climb", "1-3")
        self.assertEqual((got["cycles"], "DRIFT" in [m for m, _ in got["marks"]], round(got["drift_floor"], 3)), (2, True, 0.127))
        small = {**got, "centroid_drift": 0.10, "centroid_all": 0.10, "level_spread": 0.2, "worst_band": None}
        self.assertEqual(E.marks(small), [])
        self.assertEqual([m for m, _ in E.marks({**small, "cycles": 7})], ["DRIFT"])
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            E.report("head", small, None, None)
        self.assertIn("IT HOLDS", buf.getvalue())
        self.assertIn("(the centroid's +0.10 octaves a cycle is not marked: from 2 cycles a drift under 0.13 is inside", buf.getvalue())
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            E.report("head", {**small, "centroid_drift": 0.01, "centroid_all": 0.01}, None, None)
        self.assertNotIn("is not marked", buf.getvalue())

    def test_another_seed_and_the_band_by_cycle(self):
        """--seed reaches the engine; the band that moves most is printed cycle by cycle; a SPREAD says to read another seed."""
        code, text = self.run_tool(self.song, "turns", "1-13", "--cycle", "1bar", "--seed", "3")
        self.assertEqual(code, 0)
        self.assertIn("that band by cycle, against their mean: ", text)
        with open(os.path.join(self.root, "calls.log")) as f:
            self.assertIn("--seed 3", f.read().splitlines()[-1])
        got = json.loads(self.run_tool(self.song, "turns", "1-13", "--cycle", "1bar", "--seed", "3", "--json")[1])
        self.assertEqual((got["seed"], len(got["worst_by_cycle"])), (3, 12))
        self.assertAlmostEqual(sum(got["worst_by_cycle"]), 0.0, delta=1e-6)
        spread = {**got, "level_spread": 4.0}
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            E.report("head", spread, None, None)
        self.assertIn("(a SPREAD is read on one seed, 3: read it on another, --seed 4.", buf.getvalue())
        with self.assertRaises(SystemExit):
            self.run_tool(self.song, "turns", "1-13", "--cycle", "1bar", "--seed", "x")

    def test_parts_taking_turns_make_a_longer_cycle(self):
        got = self.read("turns", "1-13")
        self.assertEqual(got["longer"]["every"], 3)
        self.assertEqual([round(v, 1) for v in got["longer"]["places"]], [-0.5, -0.5, 1.0])
        self.assertIn("A LONGER CYCLE", [m for m, _ in got["marks"]])
        self.assertIsNone(self.read("stair")["longer"])
        self.assertIsNone(self.read("turns", "1-7")["longer"])                # seen twice only: not said

    def test_the_songs_notes_cycle_by_cycle(self):
        doc = json.loads(json.dumps(SONG))
        doc["tracks"][0]["notes"] = [n for n in notes(8) if not (n["at"] == 4 * 5 + 1)] + [{"at": 4 * 5 + 1.5, "pitch": "A2", "dur": 0.5}]
        doc["tracks"].append({"name": "stair2", "fake": None, "notes": notes(8, ((3, "F3"),))})
        self.write(doc)
        got = self.read("stair,stair2")
        self.assertEqual(got["plan"], {"cycles": 8, "notes": 4, "differ": [[6, 2]]})
        self.assertIn(["ANOTHER PATTERN", "the song writes other notes in cycle 6 (2 notes)"], got["marks"])
        self.assertEqual(self.read("stair,stair2", "1-9", "2bars")["plan"]["cycles"], 4)
        d = E.songfmt.load(self.song)
        self.assertEqual(E.plan_cycles(d, ["stair2"], 8.0, 24.0, 4.0), (4, 1, []))     # a window that starts later

    def test_a_glide_that_speeds_up_holds_through_its_changes(self):
        code, text = self.run_tool(self.song, "speeds", *SPEEDS)
        self.assertEqual(code, 0)
        self.assertIn("x.yaml speeds: 1-8, 7 cycles of 3 lengths (2 x 2bars, 1 x 1bar, 4 x 2b; 14.000 s), alone through", text)
        self.assertIn("IT HOLDS THROUGH ITS CHANGES OF SPEED", text)
        self.assertIn("    1 x 1bar   (cycle 3): ", text)
        self.assertIn("ONE cycle: no wrap of its own, and its run is one reading, not a mean", text)
        self.assertIn("the song: 4 cycles of 1 notes, the same notes at the same places in every one", text)
        self.assertIn("(a speed with ONE cycle is marked SAW-TOOTH only past 0.30 octaves or 2.0 dB through the cycle", text)
        self.assertIn("(read on ONE seed, 0. ", text)
        self.assertIn("--seeds 0,11)", text)
        got = json.loads(self.run_tool(self.song, "speeds", *SPEEDS, "--json")[1])
        self.assertEqual((got["cycles"], got["lengths"], got["marks"]), (7, ["2bars", "2bars", "1bar", "2b", "2b", "2b", "2b"], []))
        self.assertEqual([(sp["length"], sp["first"], sp["cycles"], sp["wraps"] is None) for sp in got["speeds"]],
                         [("2bars", 0, 2, False), ("1bar", 2, 1, True), ("2b", 3, 4, False)])
        self.assertEqual([(ch["from"], ch["to"], ch["into"]) for ch in got["changes"]], [("2bars", "1bar", 2), ("1bar", "2b", 3)])
        self.assertLess(max(abs(v - got["level"]) for v in got["levels"]), 0.5)            # every cycle as loud, whatever its length
        self.assertLess(max(abs(v) for v in got["centroids"]), 0.1)
        self.assertEqual(got["plans"][2], {"cycles": 4, "notes": 1, "differ": []})
        self.assertEqual((got["shape"]["readings"], got["shape"]["places"], len(got["shape"]["centroid"])), (7, [], 8))
        self.assertIn("  THE CYCLE'S SHAPE, ALL 7 CYCLES TOGETHER (7 cycles, every speed; ", text)
        self.assertIn("and no place in the cycle stands out.", text)
        doc = json.loads(json.dumps(SONG))
        doc["tracks"][5]["notes"].append({"at": 22.5, "pitch": "C3", "dur": 0.5})           # one more note in the second short cycle
        self.write(doc)
        code, text = self.run_tool(self.song, "speeds", *SPEEDS)
        self.assertIn("ANOTHER PATTERN: 4 x 2b: the song writes other notes in its cycle 2 (1 notes)", text)
        self.assertNotIn("IT HOLDS", text)

    def test_a_step_at_a_change_of_speed_and_a_lone_cycle_that_starts_again(self):
        got = json.loads(self.run_tool(self.song, "louder", *SPEEDS, "--json")[1])
        self.assertEqual([m for m, _ in got["marks"]], ["A STEP AT THE CHANGE"])
        self.assertIn("2bars -> 1bar (into cycle 3): the cycles after are +6.0 dB", got["marks"][0][1])
        self.assertAlmostEqual(got["changes"][1]["level"], 0.0, delta=0.5)                 # as loud after the second change
        got = json.loads(self.run_tool(self.song, "again", *SPEEDS, "--json")[1])
        saws = [what for m, what in got["marks"] if m == "SAW-TOOTH" and "the brightness" in what]
        self.assertEqual([w.split(":")[0] for w in saws], ["2 x 2bars", "1 x 1bar", "4 x 2b"])
        self.assertIn("at the join", saws[1])                                              # the lone cycle: its wrap is the join
        places = [what for m, what in got["marks"] if m == "A PLACE IN THE CYCLE"]         # a riser's octave is heard coming round:
        self.assertTrue(places and all("at every speed" in w for w in places))             # its first slice dark, its last bright
        self.assertIn("slice 1 of 8 is", places[0])
        self.assertIn("darker than its cycle", places[0])
        self.assertIn("at the wrap", saws[0])
        one = self.read("again", "1-5", "2bars")                                           # the first speed alone, as --cycle reads it
        self.assertAlmostEqual(one["runs"]["centroid"], got["speeds"][0]["runs"]["centroid"], delta=0.02)
        self.assertTrue(any(m == "SAW-TOOTH" for m, _ in one["marks"]))

    def test_a_mark_is_given_only_when_every_seed_has_it(self):
        where = os.path.join(self.root, "keep3")
        code, text = self.run_tool(self.song, "moody", *SPEEDS, "--seeds", "0,1", "--keep", where)
        self.assertEqual(sorted(os.listdir(where)), ["endless-s0.wav", "endless-s1.wav"])    # one render a seed
        self.assertEqual([ln for ln in text.splitlines() if ln.startswith("  == SEED")], ["  == SEED 0", "  == SEED 1"])
        self.assertEqual(text.count("  CYCLE BY CYCLE, IN ORDER"), 2)                        # the tables for each
        self.assertIn("  ON EVERY SEED (0, 1; the figures are seed 0's): nothing is marked.\n", text)
        self.assertIn("  ON SOME SEEDS ONLY (more likely the players' own variation than the song", text)
        self.assertIn("    seed 1: A STEP AT THE CHANGE: 2bars -> 1bar (into cycle 3): the cycles after are +6.0 dB", text)
        self.assertNotIn("IT HOLDS", text)
        self.assertNotIn("read on ONE seed", text)
        got = json.loads(self.run_tool(self.song, "moody", *SPEEDS, "--seeds", "0,1", "--json")[1])
        self.assertEqual((got["seeds"], got["marks"], [len(g["marks"]) for g in got["by_seed"]]), ([0, 1], [], [0, 1]))
        code, text = self.run_tool(self.song, "louder", *SPEEDS, "--seeds", "0,1")           # louder on both: the song's
        self.assertIn("  ON EVERY SEED (0, 1; the figures are seed 0's):\n  A STEP AT THE CHANGE: 2bars -> 1bar (into cycle 3)", text)
        self.assertNotIn("ON SOME SEEDS ONLY", text)
        got = json.loads(self.run_tool(self.song, "louder", *SPEEDS, "--seeds", "0,1", "--json")[1])
        self.assertEqual([m for m, _ in got["marks"]], ["A STEP AT THE CHANGE"])
        code, text = self.run_tool(self.song, "speeds", *SPEEDS, "--seeds", "0,1")           # nothing on either: it holds
        self.assertIn("nothing is marked.\n  IT HOLDS THROUGH ITS CHANGES OF SPEED", text)
        with self.assertRaises(SystemExit) as e:
            self.run_tool(self.song, "speeds", *SPEEDS, "--seeds", "0,x")
        self.assertIn("--seeds takes whole numbers", str(e.exception))

    def test_the_cycles_shape_is_every_cycle_of_every_seed_together(self):
        def reading(rows):                               # two speeds: the first two cycles, then the rest
            n = len(rows)
            return {"cycles": n, "speeds": [{"first": 0, "cycles": 2}, {"first": 2, "cycles": n - 2}],
                    "inside": {"level": [[0.0] * 4 for _ in rows], "centroid": rows}}
        wobble = [0.05, -0.05, 0.02, -0.02, 0.04, -0.04, 0.0]
        a = reading([[-0.1 + w, 0.3 + w, -0.1 - w, -0.1] for w in wobble])                 # slice 2 bright in every cycle
        b = reading([[-0.1 - w, 0.3 - w, -0.1 + w, None] for w in wobble])                 # ... on a second seed; a silent slice
        got = E.cycle_shape([a, b])
        self.assertEqual(got["readings"], 14)
        self.assertEqual([(sl, key) for sl, key, *_ in got["places"]], [(2, "centroid")])
        sl, key, mean, se, speeds = got["places"][0]
        self.assertAlmostEqual(mean, 0.3, places=6)
        self.assertLess(se, 0.02)
        self.assertEqual(len(speeds), 2)
        lines = E.shape_lines(got, [a, b])
        self.assertIn("ALL 14 CYCLES TOGETHER (7 cycles x 2 seeds, every speed;", lines[0])
        self.assertIn("  A PLACE IN THE CYCLE: slice 2 of 4 is 0.30 octaves brighter than its cycle (give or take 0.01 over 14 cycles; "
                      "at every speed: ", lines[-1])
        noisy = reading([[0.0, s, 0.0, 0.0] for s in (0.9, -0.5, 0.8, -0.4, 0.7, -0.3, 0.5)])   # a mean of 0.24, but not clear of
        self.assertEqual(E.cycle_shape([noisy])["places"], [])                             # its own scatter
        few = reading([[0.0, 0.3, 0.0, 0.0]] * 3)                                           # three readings are too few
        self.assertEqual(E.cycle_shape([few])["places"], [])
        one_speed = reading([[0.0, -0.05, 0.0, 0.05]] * 2 + [[-0.1, 0.3, -0.1, -0.1]] * 8)   # the first speed does not have it
        self.assertIn("NOT at every speed", E.shape_lines(E.cycle_shape([one_speed]), [one_speed])[-1])

    def test_cycle_lists_and_what_is_refused_of_them(self):
        self.assertEqual([round(s, 3) for _, s in E.cycle_list("2x6bars,2x3bars,2bars,2x1bar", 100)], [14.4, 14.4, 7.2, 7.2, 4.8, 2.4, 2.4])
        self.assertEqual([E.cycle_list(t, 100) for t in ("0x1bar", "x", "2x", "1bar,,2bars")], [None] * 4)
        self.assertIsNone(E.cycle_list("2bars"))                                            # bars need a tempo
        self.assertEqual((E.saw_floor(2, 0.15, 0.15), E.saw_floor(1, 0.15, 0.15), E.saw_floor(1, 1.5, 1.0)), (0.15, 0.30, 2.0))
        self.assertEqual(E.run_valid([float("nan"), 1.0, float("nan")]), 0.0)
        self.assertAlmostEqual(E.run_valid([0.0, float("nan"), 1.0, 1.5]), 2.0, places=6)
        for args, word in ((("x", "speeds", "1-8", "--cycles", "soon"), "--cycles takes lengths in order"),
                           (("x", "speeds", "1-8", "--cycles", "2bars"), "two cycles or more"),
                           (("x", "speeds", "1-8", "--cycles", "5x2bars"), "the cycles add up to 20.00 s and the passage is 14.00 s"),
                           (("x", "nobody", "1-8", "--cycles", "2x2bars"), "has no track nobody")):
            with self.assertRaises(SystemExit) as e:
                self.run_tool(*args)
            self.assertIn(word, str(e.exception))
        self.assertEqual(self.run_tool("x", "speeds", "1-8", "--cycle", "1bar", "--cycles", "2x2bars")[0], 2)   # one or the other
        where = os.path.join(self.root, "keep2")
        self.run_tool(self.song, "speeds", "1-8", "--cycles", "2x2bars,1bar,4x2b", "--keep", where)
        code, text = self.run_tool("--wav", os.path.join(where, "endless.wav"), "--tempo", "120", "--cycles", "2x2bars,1bar,4x2b")
        self.assertIn("endless.wav, 7 cycles of 3 lengths (2 x 2bars, 1 x 1bar, 4 x 2b; 14.000 s)\n", text)
        self.assertNotIn("the song:", text)
        with self.assertRaises(SystemExit) as e:
            self.run_tool("--wav", os.path.join(where, "endless.wav"), "--cycles", "2x2bars,1bar")
        self.assertIn("bars and beats need --tempo", str(e.exception))

    def test_cycles_and_what_is_refused(self):
        self.assertEqual([E.cycle_seconds(t, 100) for t in ("1bar", "4bars", "16b", "2.4s", "0bar", "x")], [2.4, 9.6, 9.6, 2.4, None, None])
        self.assertIsNone(E.cycle_seconds("1bar"))
        self.assertTrue(E.saw(1.0, -0.9, 0.15) and not E.saw(1.0, 0.2, 0.15) and not E.saw(0.1, -0.1, 0.15) and not E.saw(1.0, -0.2, 0.15))
        for args, word in ((("x", "stair", "1-2", "--cycle", "1bar"), "two or more are needed"),
                           (("x", "nobody", "1-9", "--cycle", "1bar"), "has no track nobody"),
                           (("x", "stair", "9-1", "--cycle", "1bar"), "FROM-TO takes two positions"),
                           (("x", "stair", "1-9", "--cycle", "soon"), "--cycle takes"),
                           (("x", "stair", "1-9", "--cycle", "1bar", "--steps", "1"), "--steps takes"),
                           (("nosuch", "stair", "1-9", "--cycle", "1bar"), "no song nosuch")):
            with self.assertRaises(SystemExit) as e:
                self.run_tool(*args)
            self.assertIn(word, str(e.exception))
        self.assertEqual(self.run_tool("x", "stair", "1-9")[0], 2)            # no --cycle: the usage

    def test_a_render_in_hand(self):
        where = os.path.join(self.root, "keep")
        self.run_tool(self.song, "riser", "1-9", "--cycle", "1bar", "--keep", where)
        wav = os.path.join(where, "endless.wav")
        code, text = self.run_tool("--wav", wav, "--cycle", "2s")
        self.assertEqual(code, 0)
        self.assertIn("endless.wav: 8 cycles of 2s (2.000 s)", text)
        self.assertIn("SAW-TOOTH", text)
        self.assertNotIn("the song ", text)
        again = json.loads(self.run_tool("--wav", wav, "--cycle", "1bar", "--tempo", "120", "--json")[1])
        self.assertEqual((again["cycles"], again["plan"]), (8, None))
        x, sr = E.load(wav)
        self.assertEqual((sr, len(x)), (24000, 16 * 24000))


if __name__ == "__main__":
    unittest.main()
