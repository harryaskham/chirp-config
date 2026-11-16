#!/usr/bin/env python3
"""tools/endless.py: does the endless thing hold?

Hermetic: made songs and a stand-in engine that plays a track by its "fake" kind, so each answer is known:
  shepard  octave-spaced sines under a fixed bell, gliding an octave a bar for ever (a true Shepard glide)
  riser    one sine that climbs an octave a bar and starts again (the saw-tooth the illusion hides)
  climb    one sine that really climbs, a quarter octave a bar
  turns    the shepard, 1.5 dB louder on every third bar (parts taking turns: a longer cycle)

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
]}


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
