#!/usr/bin/env python3
"""tools/warp.py: where a warped track's notes sound, and that notechk, hitpoke and holds read them there.

Hermetic: the figures of the engine's own test (lower.rs, warp_drifts_a_track_and_relocks_it_on_the_beat), and a
stand-in engine that answers `plan`. (Checked once against renders on pin e8830ba0: 340 clicks over two warps with
every unit and curve, the largest difference 1.6 ms, which is the click detector's own lag; unwarped they were up to
1.9 s away.)

  python3 tools/tests/test_warp.py      (from ~/.config/chirp; under a second)
"""
import contextlib
import io
import math
import os
import shutil
import stat
import sys
import tempfile
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import holds as H  # noqa: E402
import notechk as N  # noqa: E402
import warp as W  # noqa: E402

SLIP = [{"over": "4b", "to": 0.5}, {"over": "4b", "to": 0, "curve": "smooth"}]


def starts(warp, tempo=60, n=14):
    """When a note on every beat sounds, in seconds."""
    return [m["at"] * 60 / tempo for m in W.moved([{"at": float(b), "len": 0.25} for b in range(n)], warp, tempo)]


class Shift(unittest.TestCase):
    def test_the_engines_own_figures(self):
        w = starts(SLIP)                                          # half a beat behind over four, smoothly back over four
        want = [0.0, 1.125, 2.25, 3.375, 4.5, 5.0 + 0.5 * (0.5 + 0.5 * math.cos(math.pi / 4)), 6.25]
        for got, exp in zip(w, want):
            self.assertAlmostEqual(got, exp, places=6)
        for i in range(8, 14):
            self.assertAlmostEqual(w[i], float(i), places=9)      # locked to the grid again
        r = starts([{"over": "8b", "tempo": 1.25}])               # 8 of its own beats in 6.4 of the song's; the lead holds
        self.assertAlmostEqual(r[4], 3.2)
        self.assertAlmostEqual(r[8], 6.4)
        self.assertAlmostEqual(r[12], 10.4)
        self.assertAlmostEqual(starts([{"over": "2bar", "to": "-1bar"}])[8], 4.0)

    def test_units_curves_and_ratios(self):
        self.assertEqual(W.beats("96b", 120), 96.0)
        self.assertEqual(W.beats("2bar", 120), 8.0)
        self.assertEqual(W.beats("1.5s", 120), 3.0)
        self.assertEqual(W.beats("500ms", 120), 1.0)
        self.assertEqual(W.beats(-0.25, 120), -0.25)
        self.assertEqual(W.ratio("3:4"), 0.75)
        segs = W.segments([{"over": "8b", "to": -1, "curve": "in"}, {"over": "8b", "to": 0, "curve": "out"}, {"over": "4b"}], 100)
        self.assertEqual([(a, b) for a, b, *_ in segs], [(0.0, 8.0), (8.0, 16.0), (16.0, 20.0)])
        self.assertAlmostEqual(W.shift(segs, 4), -0.25)           # in: the square
        self.assertAlmostEqual(W.shift(segs, 12), -0.25)          # out: 1 - (1 - x)^2 of the way back
        self.assertEqual(W.shift(segs, 18), 0.0)                  # a stretch with neither `to` nor `tempo` holds
        self.assertEqual(W.shift(segs, 400), 0.0)
        self.assertEqual(W.shift([], 3), 0.0)
        with self.assertRaises(ValueError):
            W.segments([{"over": "4b", "to": 1, "curve": "wobbly"}], 120)
        with self.assertRaises(ValueError):
            W.segments([{"over": "0b", "to": 1}], 120)

    def test_a_note_across_a_slip_changes_length_and_no_warp_is_the_same_list(self):
        notes = [{"at": 2.0, "len": 2.0, "pitch": "E2"}]
        self.assertIs(W.moved(notes, None, 120), notes)
        self.assertIs(W.moved(notes, [], 120), notes)
        m = W.moved(notes, [{"over": "4b", "to": -1}], 120)[0]   # ahead by a beat over four: it runs a quarter fast
        self.assertAlmostEqual(m["at"], 1.5)
        self.assertAlmostEqual(m["len"], 1.5)                     # ends at 4 - 1 = 3
        self.assertEqual(m["pitch"], "E2")
        self.assertEqual(notes[0]["at"], 2.0)                     # the plan's notes are not touched


class Readers(unittest.TestCase):
    CANON = {"tempo": 60, "tracks": [{"name": "left", "notes": [{"at": float(b), "len": 0.25} for b in range(10)]},
                                     {"name": "kit", "tracks": [{"name": "right", "warp": SLIP,
                                                                 "notes": [{"at": float(b), "len": 0.25} for b in range(10)]}]}]}

    def test_notechk_reads_a_warped_track_where_it_sounds(self):
        self.assertEqual([n["at"] for n in N.track_notes(self.CANON, "left")], [float(b) for b in range(10)])
        right = [n["at"] for n in N.track_notes(self.CANON, "right")]
        self.assertAlmostEqual(right[4], 4.5)
        self.assertAlmostEqual(right[9], 9.0)
        on, allon = N.onsets(N.track_notes(self.CANON, "right"), 0.0, 60, "all")
        self.assertEqual(on[:5], [0.0, 1.125, 2.25, 3.375, 4.5])
        with self.assertRaises(SystemExit) as e:
            N.track_notes(dict(self.CANON, tempo=[{"at": "0b", "bpm": 60}]), "right")
        self.assertIn("has a warp and the song's tempo changes", str(e.exception))
        self.assertIsNotNone(N.track_notes(dict(self.CANON, tempo=[{"at": "0b", "bpm": 60}]), "left"))   # unwarped: as before

    def test_holds_reads_a_warped_hold_where_it_sounds(self):
        plain = {"name": "pad", "notes": [{"at": 4.0, "len": 8.0, "pitch": "C3"}]}
        self.assertEqual([(h["at"], h["len"]) for h in H.holds_of(plain, 4)], [(4.0, 8.0)])
        late = dict(plain, warp=[{"over": "4b", "to": 1}])
        self.assertEqual([(h["at"], h["len"]) for h in H.holds_of(late, 4, 60)], [(5.0, 8.0)])


ENGINE = r'''#!/usr/bin/env python3
import json, sys
slip = [{"over": "96b", "to": 0}, {"curve": "smooth", "over": "16b", "to": -0.25}, {"over": "16b", "to": -0.25},
        {"over": "2bar", "tempo": 1.03}]
tracks = [{"name": "gl", "notes": [{"at": 0}]}, {"name": "gr", "warp": slip, "notes": [{"at": 0}]},
          {"name": "cr", "warp": slip, "notes": [{"at": 0}]}, {"name": "pad", "warp": [{"over": "1bar", "to": "1bar"}], "notes": []}]
if "bare" in open(sys.argv[sys.argv.index("-f") + 1]).read():
    tracks = tracks[:1]
print(json.dumps({"data": {"canonical": {"tempo": 108, "tracks": tracks}}}))
'''


class Table(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="warp-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self.engine = os.path.join(self.root, "fake-chirp")
        with open(self.engine, "w") as f:
            f.write(ENGINE)
        os.chmod(self.engine, os.stat(self.engine).st_mode | stat.S_IXUSR)
        self.song = os.path.join(self.root, "song.yaml")
        open(self.song, "w").close()

    def run_tool(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = W.main([*argv, "--pin", self.engine])
        return code, out.getvalue()

    def test_the_table_groups_tracks_with_one_warp_and_prints_each_stretch(self):
        code, text = self.run_tool(self.song)
        self.assertEqual(code, 0)
        lines = text.splitlines()
        self.assertEqual(lines[0], "gr, cr  (tempo 108; minus = ahead of the song)")
        self.assertEqual(lines[2].split(), ["1.00-", "25.00", "hold", "+0.000", "+0.00", "+0.0"])
        self.assertEqual(lines[3].split(), ["25.00-", "29.00", "smooth", "-0.250", "-1.00", "-138.9"])   # a sixteenth ahead
        self.assertEqual(lines[4].split()[2], "hold")
        last = lines[5].split()                                                                          # 3% fast for two bars
        self.assertEqual(last[2], "linear")
        self.assertAlmostEqual(float(last[3]), -0.25 + 8 * (1 / 1.03 - 1), places=3)
        self.assertEqual(lines[6], "pad  (tempo 108; minus = ahead of the song)")

    def test_at_and_named_tracks(self):
        code, text = self.run_tool(self.song, "gr", "--at", "27", "--at", "112b", "--at", "200s")
        lines = text.splitlines()
        self.assertEqual(lines[0], "gr  (tempo 108; minus = ahead of the song)")
        self.assertEqual(lines[-3], "  at 27: -0.125 beats, -0.50 sixteenths, -69.4 ms")           # half way through the smooth slip
        self.assertEqual(lines[-2], "  at 112b: -0.250 beats, -1.00 sixteenths, -138.9 ms")
        self.assertTrue(lines[-1].startswith("  at 200s: -0.483 beats"))                           # after the last stretch: held
        with self.assertRaises(SystemExit) as e:
            self.run_tool(self.song, "gl")
        self.assertEqual(str(e.exception), "warp: no warped track gl (warped: gr, cr, pad)")

    def test_a_song_with_no_warp_says_so(self):
        with open(self.song, "w") as f:
            f.write("bare\n")
        self.assertEqual(self.run_tool(self.song), (0, "no track has a warp\n"))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(W.main([]), 2)
        self.assertIn("warp.py SONG [TRACK ...]", out.getvalue())


if __name__ == "__main__":
    unittest.main()
