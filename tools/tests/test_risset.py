#!/usr/bin/env python3
"""tools/risset.py: where a risset track's notes sound.

Hermetic: the arithmetic is the engine's (lower.rs `risset_events`), and the literal figures pinned here are the
ones that were checked against the engine's own audio on 15 Nov (False Summit v2's `tick`, rendered alone: 134 of
135 strokes over -16 dB had an onset within 30 ms, and no onset was without a stroke). The stand-in engine only
answers `plan` with the song.

  python3 tools/tests/test_risset.py      (from ~/.config/chirp; under a second)
"""
import contextlib
import io
import json
import math
import os
import shutil
import stat
import sys
import tempfile
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import endless as E  # noqa: E402
import risset as R  # noqa: E402

ENGINE = r'''#!/usr/bin/env python3
import json, sys
a = sys.argv[1:]
song = json.load(open(a[a.index("-f") + 1]))
print(json.dumps({"data": {"canonical": song}}) if not song.get("broken") else "no")
'''
TICK = {"name": "tick", "patch": "kit", "at": "288b", "risset": {"length": "10bar"},      # as `chirp plan` prints it:
        "notes": [{"len": 0.5, "pitch": "h", "vel": 0.9}, {"at": 0.5, "len": 0.5, "pitch": "h"}, {"at": 1, "pitch": "h"}]}
SONG = {"tempo": 100, "tracks": [TICK, {"name": "gl", "notes": [{"at": 0, "pitch": "F1"}]}]}


class Arithmetic(unittest.TestCase):
    def test_the_engines_defaults_and_what_it_refuses(self):
        self.assertEqual(R.settings({}, 100), {"cycle": 16.0, "layers": 3, "ratio": 2.0, "total": 64.0, "down": False,
                                               "both": False, "pitch": False})
        s = R.settings({"cycle": "2bar", "layers": 4, "ratio": "3:2", "length": "6s", "down": True}, 120)
        self.assertEqual((s["cycle"], s["layers"], s["ratio"], s["total"], s["down"]), (8.0, 4, 1.5, 12.0, True))
        for bad in ({"layers": 7}, {"layers": 1}, {"ratio": 1.0}, {"cycle": "0bar"}):
            with self.assertRaises(ValueError):
                R.settings(bad, 100)
        self.assertEqual(R.pattern(TICK["notes"], 100), ([(0.0, 0.5), (0.5, 0.5), (1.0, 1.0)], 2.0))

    def test_the_ticks_strokes_as_the_engine_plays_them(self):
        got = R.sounding(TICK, 100)
        self.assertEqual(len(got), 202)
        first = got[0]
        self.assertEqual((round(first["at"], 4), first["copy"], first["from"], round(first["speed"], 2), round(R.db(first["gain"]), 1)),
                         (288.0118, 2, 1, 1.41, -6.0))
        self.assertEqual(R.warp.place(first["at"]), "73:00.05")
        rows = R.table(TICK, 100)
        self.assertEqual([r["bar"] for r in rows], list(range(73, 83)))
        self.assertEqual([[r["copies"][j]["strokes"] for j in range(3)] for r in rows[:4]],
                         [[2, 5, 10], [3, 5, 11], [3, 7, 13], [4, 7, 13]])
        self.assertEqual(rows[4]["copies"], rows[0]["copies"])                    # the second cycle is the first
        self.assertEqual([round(v, 1) for v in rows[0]["copies"][0]["level"]], [-45.4, -33.9])   # the slow copy enters from silence
        self.assertEqual([round(v, 1) for v in rows[3]["copies"][2]["level"]], [-55.6, -27.5])   # the fast one leaves into it
        self.assertTrue(all(288 <= m["at"] < 328 for m in got))                    # 10 bars from beat 288
        self.assertEqual(len(R.table(TICK, 100, 288.0, 292.0)), 1)

    def test_every_cycle_is_the_same_and_each_stroke_follows_the_rule(self):
        rel, length = [(0.0, 0.25), (0.75, 0.25)], 1.0
        ev = R.events(rel, length, 8.0, 3, False, 24.0, 2.0)
        one = [(ni, round(t, 9), round(f, 9), round(w, 9), j) for ni, t, _, f, w, j in ev if t < 8]
        two = [(ni, round(t - 8, 9), round(f, 9), round(w, 9), j) for ni, t, _, f, w, j in ev if 8 <= t < 16]
        self.assertEqual(one, two)
        for ni, t, ln, f, w, j in ev:
            u = (t % 8.0) / 8.0
            self.assertAlmostEqual(f, 2.0 ** (j - 1.5 + u), places=9)             # copy j: 2^(j - K/2) .. twice that
            self.assertAlmostEqual(w, math.sin(math.pi * (j + u) / 3) ** 2 * 2 / 3, places=9)
            self.assertGreaterEqual(w, R.QUIET)
        for j in range(3):                                                         # a copy's strokes close up as it speeds
            ts = [t for ni, t, _, f, w, c in ev if c == j and ni == 0 and t < 8]
            gaps = [b - a for a, b in zip(ts, ts[1:])]
            self.assertTrue(all(b < a for a, b in zip(gaps, gaps[1:])), gaps)
        down = R.events(rel, length, 8.0, 3, True, 8.0, 2.0)
        for ni, t, ln, f, w, j in down:
            u = t / 8.0
            self.assertAlmostEqual(f, 2.0 ** (j - 0.5 - u), places=9)             # slowing: from twice down
            self.assertAlmostEqual(w, math.sin(math.pi * (j + 1 - u) / 3) ** 2 * 2 / 3, places=9)
        self.assertEqual(R.events(rel, length, 8.0, 3, False, 4.0, 2.0), [e for e in ev if e[1] < 4.0])    # `length` cuts it

    def test_both_ways_pitch_and_a_track_without_one(self):
        t = {"name": "x", "risset": {"cycle": "2bar", "both": True, "pitch": True, "ratio": "3:2"},
             "notes": [{"at": 0, "len": 0.25, "pitch": "C4"}, {"at": 0.5, "len": 0.25, "pitch": "E4", "tr": 12}]}
        got = R.sounding(t, 120)
        up = R.events([(0.0, 0.25), (0.5, 0.25)], 0.75, 8.0, 3, False, 32.0, 1.5)
        dn = R.events([(0.0, 0.25), (0.5, 0.25)], 0.75, 8.0, 3, True, 32.0, 1.5)
        self.assertEqual(len(got), len(up) + len(dn))
        self.assertAlmostEqual(max(m["gain"] for m in got), 0.5 * max(e[4] for e in up + dn), places=9)       # each way at half level
        for m in got:
            self.assertAlmostEqual(m["tr"], (12 if m["from"] == 1 else 0) + 12 * math.log2(m["speed"]), places=9)
            self.assertTrue(1.5 ** -1.5 - 1e-9 <= m["speed"] <= 1.5 ** 1.5 + 1e-9)
            self.assertAlmostEqual(m["len"], 0.25 / m["speed"], places=9)
        plain = {"name": "gl", "notes": [{"at": 3, "pitch": "F1"}]}
        self.assertEqual(R.sounding(plain, 120), plain["notes"])
        self.assertEqual(R.sounding({"name": "e", "risset": {}, "notes": []}, 120), [])


class Readers(unittest.TestCase):
    """tools/notechk.py's track_notes is what entries.py, rests.py, velramp.py, hitpoke.py and palette.py read."""

    def test_the_note_tools_read_the_copies_and_a_late_track_from_the_top(self):
        import notechk
        got = notechk.track_notes(SONG, "tick")
        self.assertEqual((len(got), R.warp.place(got[0]["at"]), R.warp.place(got[-1]["at"])[:2]), (202, "73:00.05", "82"))
        self.assertEqual(notechk.track_notes(SONG, "gl"), SONG["tracks"][1]["notes"])               # untouched: the same list
        late = {"tempo": 120, "tracks": [{"name": "late", "at": "2bar",
                                          "notes": [{"at": 0, "pitch": "C2"}, {"at": 4, "pitch": "D2"}]}]}
        self.assertEqual([(n["at"], n["pitch"]) for n in notechk.track_notes(late, "late")], [(8.0, "C2"), (12.0, "D2")])
        changing = {"tempo": [[0, 100], [8, 120]], "tracks": [dict(TICK)]}
        self.assertEqual(notechk.track_notes(changing, "tick"), TICK["notes"])                       # left as written
        self.assertIsNone(notechk.track_notes(SONG, "nobody"))

    def test_a_notes_own_gain_rides_under_the_fade(self):
        t = {"name": "x", "risset": {"cycle": "2bar"},
             "notes": [{"at": 0, "len": 0.5, "pitch": "h", "gain": "-6dB"}, {"at": 1, "pitch": "h"}]}
        got = R.sounding(t, 120)
        a = max(m["gain"] for m in got if m["from"] == 0)
        b = max(m["gain"] for m in got if m["from"] == 1)
        self.assertAlmostEqual(a / b, 10 ** (-6 / 20), delta=0.03)
        gains = ({}, {"gain": 0.5}, {"gain": "-20dB"}, {"gain": "2"}, {"gain": "loud"}, {"gain": True})
        self.assertEqual([R.written_gain(n) for n in gains], [1.0, 0.5, 0.1, 2.0, 1.0, 1.0])


class Tool(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="risset-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        os.makedirs(os.path.join(self.root, "songs"))
        self.engine = os.path.join(self.root, "fake-chirp")
        with open(self.engine, "w") as f:
            f.write(ENGINE)
        os.chmod(self.engine, os.stat(self.engine).st_mode | stat.S_IXUSR)
        self.song = os.path.join(self.root, "songs", "x.yaml")
        self.write(SONG)
        old = R.ROOT
        R.ROOT = self.root
        self.addCleanup(setattr, R, "ROOT", old)

    def write(self, doc):
        with open(self.song, "w") as f:
            json.dump(doc, f)

    def run_tool(self, *args):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = R.main([*args, "--pin", self.engine])
        return code, buf.getvalue()

    def test_the_report(self):
        code, text = self.run_tool("x", "--bars", "73-74")
        self.assertEqual(code, 0)
        self.assertIn("x.yaml (100 bpm): where its risset tracks sound", text)
        self.assertIn("tick: a Risset rhythm from 73:00.00 for 10 bars: a pattern of 3 notes in 2 beats, a cycle of 4 bars, "
                      "3 copies x2 of tempo apart, speeding up", text)
        self.assertIn("copy 0: x0.35 -> x0.71 of the written tempo; level -70.7 -> -15.6 -> -6.2 dB  enters from silence", text)
        self.assertIn("copy 2: x1.41 -> x2.83 of the written tempo; level -6.2 -> -15.6 -> -70.7 dB  leaves into silence", text)
        self.assertIn("      73    2  x0.38-0.40  -45.4..-33.9     5  x0.72-0.83   -5.7.. -4.2    10  x1.41-1.67   -9.4.. -6.0", text)
        self.assertIn("every stroke that sounds in 73:00.00 to 74:00.00 (17):", text)
        self.assertIn("  73:00.05  copy 2  x1.41    -6.0 dB  note 2 (h)", text)
        got = json.loads(self.run_tool(self.song, "tick", "--bars", "288b-292b", "--json")[1])
        t = got["tracks"][0]
        self.assertEqual((got["tempo"], t["name"], t["at"], len(t["strokes"])), (100, "tick", 288.0, 17))
        self.assertEqual(len(got["tracks"][0]["bars"]), 10)

    def test_what_it_says_when_there_is_nothing_to_read(self):
        with self.assertRaises(SystemExit) as e:
            self.run_tool("x", "gl")
        self.assertIn("has no risset track gl (it has: tick)", str(e.exception))
        for args, word in ((("nosuch",), "no song nosuch"), (("x", "--bars", "9"), "--bars takes FROM-TO"),
                           (("x", "--bars"), "takes a value")):
            with self.assertRaises(SystemExit) as e:
                self.run_tool(*args)
            self.assertIn(word, str(e.exception))
        self.write({"tempo": 100, "tracks": [SONG["tracks"][1]]})
        self.assertIn("no track has a risset (copies written out on their own tracks are read by tools/endless.py)", self.run_tool("x")[1])
        self.write({"broken": True})
        with self.assertRaises(SystemExit) as e:
            self.run_tool("x")
        self.assertIn("does not plan", str(e.exception))

    def test_endless_reads_the_copies_not_the_pattern(self):
        self.assertEqual(E.plan_cycles(SONG, ["tick"], 288.0, 328.0, 16.0, 100), (2, 83, []))       # 73-83: two whole cycles
        self.assertEqual(E.plan_cycles(SONG, ["tick"], 288.0, 328.0, 16.0), (2, 0, []))             # no tempo: as written, nothing there
        late = {"tempo": 120, "tracks": [{"name": "late", "at": "8b", "notes": [{"at": 0, "pitch": "C2"}, {"at": 4, "pitch": "C2"}]}]}
        self.assertEqual(E.plan_cycles(late, ["late"], 8.0, 16.0, 4.0, 120), (2, 1, []))            # a late track from its own start
        self.assertEqual(E.notes_sounding(late, "nobody", 120), [])
        warped = {"tempo": 120, "tracks": [{"name": "w", "warp": [{"over": "8bar", "to": 0.25}], "notes": [{"at": 32, "pitch": "C2"}]}]}
        self.assertEqual([round(n["at"], 3) for n in E.notes_sounding(warped, "w", 120)], [32.25])


if __name__ == "__main__":
    unittest.main()
