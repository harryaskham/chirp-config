#!/usr/bin/env python3
"""tools/seams.py: the song's loudness stretch by stretch, and the step at each seam.

Hermetic: a made plan (who plays which bars) and made audio (noise at a known level a bar), so each step is known.

  python3 tools/tests/test_seams.py      (from ~/.config/chirp; a second or two)
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
import wave

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import likeness as L  # noqa: E402
import seams as S  # noqa: E402

SR = 8000
BAR = 2.0                                                  # tempo 120


def part(name, bars, every=1.0):
    return {"name": name, "notes": [{"at": 4 * (b - 1) + i * every, "len": every, "pitch": "F2"}
                                    for b in bars for i in range(int(4 / every))]}


def song():
    """bass: bars 1-12. gtr: enters at 5. lead: enters at 9. click: one stroke in bar 3. pad: bars 1-2, back at 9."""
    return {"tempo": 120, "tracks": [
        part("bass", range(1, 13)), part("gtr", range(5, 13)), part("lead", range(9, 13)),
        {"name": "click", "notes": [{"at": 8.0, "len": 0.25, "pitch": "k"}]},
        {"name": "kit", "tracks": [part("pad", [1, 2, 9, 10, 11, 12])]},
        {"name": "off", "mute": True, "notes": [{"at": 0, "len": 48, "pitch": "C3"}]}]}


def audio(levels_db, sr=SR):
    """Stereo noise, one level (dB) a bar."""
    rng = np.random.default_rng(7)
    return np.concatenate([rng.standard_normal((int(BAR * sr), 2)) * 10 ** (db / 20) for db in levels_db])


class Seams(unittest.TestCase):
    def test_a_part_plays_through_short_gaps_and_a_stroke_is_not_a_part(self):
        got = S.runs(song(), 16.0, 8.0)
        self.assertEqual(got["bass"], [(0.0, 48.0)])
        self.assertEqual(got["pad"], [(0.0, 8.0), (32.0, 48.0)])           # six bars of silence: it left, and came back
        self.assertNotIn("click", got)                                       # one stroke
        self.assertNotIn("off", got)                                         # muted
        gappy = {"tracks": [part("riff", [1, 2, 5, 6])]}                     # two bars' rest: under --quiet 4, one stretch
        self.assertEqual(S.runs(gappy, 16.0, 8.0)["riff"], [(0.0, 24.0)])
        self.assertEqual(S.runs(gappy, 8.0, 8.0)["riff"], [(0.0, 8.0), (16.0, 24.0)])

    def test_the_seams_are_where_parts_enter_and_leave(self):
        got = S.seams(S.runs(song(), 16.0, 8.0), 8.0)
        self.assertEqual([(b, sorted(i), sorted(o)) for b, i, o in got],
                         [(0.0, ["bass", "pad"], []), (8.0, [], ["pad"]), (16.0, ["gtr"], []), (32.0, ["lead", "pad"], []),
                          (48.0, [], ["bass", "gtr", "lead", "pad"])])
        pickup = {"tracks": [part("bass", range(1, 9)), {"name": "gtr", "notes": [{"at": 15.5, "len": 0.5, "pitch": "F2"}]
                                                         + part("gtr", range(5, 9))["notes"]}]}
        self.assertEqual(S.seams(S.runs(pickup, 16.0, 8.0), 8.0)[1][:2], (16.0, ["gtr"]))     # a pickup belongs to its bar
        close = {"tracks": [part("a", range(1, 9)), part("b", range(3, 9)), part("c", range(4, 9))]}
        self.assertEqual([(b, i) for b, i, _ in S.seams(S.runs(close, 16.0, 8.0), 8.0)][:2], [(0.0, ["a"]), (8.0, ["b", "c"])])

    def test_the_step_at_each_seam_and_an_entry_with_none(self):
        # bars 1-2 at -30, 3-4 -30 (the pad left), 5-8 -30 (the guitar came in: NO step), 9-12 -24 (the lead: +6)
        got = S.read(song(), audio([-30] * 8 + [-24] * 4), SR)
        self.assertEqual([s["bars"] for s in got], [[1.0, 3.0], [3.0, 5.0], [5.0, 9.0], [9.0, 13.0]])
        self.assertEqual([s["time"] for s in got], [[0.0, 4.0], [4.0, 8.0], [8.0, 16.0], [16.0, 24.0]])
        self.assertIsNone(got[0]["step"])                                    # nothing before the first stretch
        self.assertAlmostEqual(got[2]["step"], 0.0, delta=0.3)
        self.assertAlmostEqual(got[3]["step"], 6.0, delta=0.3)
        self.assertEqual([S.flat(s) for s in got], [False, False, True, False])   # the pad LEFT at 3: not an entry
        self.assertEqual((got[2]["enter"], got[1]["leave"], sorted(got[3]["enter"])), (["gtr"], ["pad"], ["lead", "pad"]))
        lines = S.table(got)
        self.assertTrue(lines[3].rstrip().endswith("ENTER gtr   ENTERS, NO STEP"))
        self.assertEqual(lines[1].split()[:3], ["1-3", "0:00-0:04", f"{got[0]['lufs']:.1f}"])
        self.assertEqual(lines[-2], f"  it steps up 1 dB or more at bar 9 ({got[3]['step']:+.1f}); its loudest stretch is 9-13 "
                                    f"({got[3]['lufs']:.1f} LUFS)")
        self.assertTrue(lines[-1].startswith("  ENTERS, NO STEP at bar 5: parts come in and the finished file rises less than 0.5 dB"))
        up = S.read(song(), audio([-30] * 4 + [-27] * 4 + [-24] * 4), SR)     # the guitar brings 3 dB: nothing marked
        self.assertEqual([S.flat(s) for s in up], [False] * 4)
        self.assertNotIn("ENTERS, NO STEP", "\n".join(S.table(up)))
        thin = S.read(song(), audio([-30] * 4 + [-34] * 8), SR)                # it comes in and the level FALLS 4: not marked
        self.assertFalse(S.flat(thin[2]))

    def test_your_own_stretches(self):
        got = S.read(song(), audio([-30] * 8 + [-24] * 4), SR, ["1-5:count", "5-9:whole", "9-13:total", "3-4:alone"])
        self.assertEqual([(s["label"], s["bars"]) for s in got],
                         [("count", [1.0, 5.0]), ("whole", [5.0, 9.0]), ("total", [9.0, 13.0]), ("alone", [3.0, 4.0])])
        self.assertEqual([s["step"] is None for s in got], [True, False, False, True])     # the last does not follow the third
        self.assertAlmostEqual(got[2]["step"], 6.0, delta=0.3)
        self.assertEqual((got[1]["enter"], sorted(got[2]["enter"])), (["gtr"], ["lead", "pad"]))
        self.assertIn("whole: ENTER gtr   ENTERS, NO STEP", S.table(got)[2])
        with self.assertRaises(SystemExit) as e:
            S.read(song(), audio([-30] * 12), SR, ["nine-12"])
        self.assertIn("--windows takes FROM-TO", str(e.exception))
        with self.assertRaises(SystemExit) as e:
            S.read({**song(), "tempo": [[0, 120], [16, 90]]}, audio([-30] * 12), SR)
        self.assertIn("only fixed-tempo songs in 4/4", str(e.exception))

    def test_the_tool_from_a_finished_file(self):
        root = tempfile.mkdtemp(prefix="seams-test-")
        self.addCleanup(shutil.rmtree, root, True)
        pin = os.path.join(root, "fake-chirp")
        with open(pin, "w") as f:
            f.write("#!/usr/bin/env python3\nimport json, sys\na = sys.argv\n"
                    "print(json.dumps({'data': {'canonical': json.load(open(a[a.index('-f') + 1]))}}))\n")
        os.chmod(pin, os.stat(pin).st_mode | stat.S_IXUSR)
        path = os.path.join(root, "song.yaml")
        with open(path, "w") as f:
            json.dump(song(), f)
        wav = os.path.join(root, "n-0.wav")
        x = audio([-30] * 8 + [-24] * 4, L.SR)
        with wave.open(wav, "wb") as w:
            w.setnchannels(2)
            w.setsampwidth(2)
            w.setframerate(L.SR)
            w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = S.main([path, "--wav", wav, "--pin", pin])
        text = out.getvalue()
        self.assertEqual(code, 0)
        self.assertTrue(text.startswith("song.yaml, n-0.wav: 4 stretches between the plan's seams (a part enters or leaves; "
                                        "--least 2 bars, --quiet 4); LUFS of the finished file, and the step into each\n"))
        self.assertIn("ENTERS, NO STEP at bar 5", text)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            S.main([path, "--wav", wav, "--pin", pin, "--windows", "1-9:first", "9-13:total", "--json"])
        got = json.loads(out.getvalue())["stretches"]
        self.assertEqual([s["label"] for s in got], ["first", "total"])
        self.assertAlmostEqual(got[1]["step"], 6.0, delta=0.3)
        with self.assertRaises(SystemExit) as e:
            S.main(["nosuch", "--pin", pin])
        self.assertIn("no song nosuch", str(e.exception))


if __name__ == "__main__":
    unittest.main()
