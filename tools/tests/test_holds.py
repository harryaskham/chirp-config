#!/usr/bin/env python3
"""tools/holds.py: a song's long notes, and whether each dies away or sits flat until it stops (Common Time v23: a held
note through a saturated amp has no decay).

Hermetic: the measures on synthetic audio, and the whole tool against a stand-in for the chirp binary that answers
`plan --json` and writes each solo "render" itself.

  python3 tools/tests/test_holds.py      (from ~/.config/chirp; a few seconds)
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

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import holds as H  # noqa: E402

SR = 48000

FAKE_PIN = r'''#!/usr/bin/env python3
"""A stand-in for chirp: `plan --json` prints a canned song; `render --solo NAME --to Nb -o OUT` writes that track."""
import json, math, struct, sys, wave
a = sys.argv[1:]
SONG = {"tempo": 120.0, "tracks": [
    {"name": "wall", "patch": "rig-high-gain", "out": "gtrs", "notes": [
        {"at": 8, "len": 16, "pitch": "F1"}, {"at": 8, "len": 16, "pitch": "C2"},     # one chord: one hold
        {"at": 40, "len": 0.5, "pitch": "F1"}]},
    {"name": "clean", "patch": "rig-clean", "notes": [{"at": 8, "len": 16, "pitch": "F3"}]},
    {"name": "short", "patch": "rig-high-gain", "notes": [{"at": 0, "len": 1, "pitch": "F1"}]},
    {"name": "bus", "tracks": [{"name": "inner", "patch": "pad", "notes": [
        {"at": 0, "len": 8, "pitch": "A2"}, {"at": 8, "len": 8, "pitch": "A2"}]}]},
    {"name": "off", "mute": True, "patch": "pad", "notes": [{"at": 0, "len": 32, "pitch": "A2"}]},
]}
if a[0] == "plan":
    print(json.dumps({"status": "ok", "data": {"canonical": SONG}}))
    sys.exit(0)
solo, out, to = a[a.index("--solo") + 1], a[a.index("-o") + 1], a[a.index("--to") + 1]
assert to.endswith("b") and "--from" not in a and "loudness=null" in a, a
sr, spb = 48000, 0.5
n = int(float(to[:-1]) * spb * sr)
def amp(t):
    b = t / spb
    if solo == "wall":                       # written 8..24, played nine tenths of it, flat, then nothing
        return 0.5 if 8 <= b < 8 + 16 * 0.9 else 0.0
    if solo == "clean":                      # dies away: 6 dB a second
        return 0.5 * 10 ** (-6 * (t - 8 * spb) / 20) if 8 <= b < 24 else 0.0
    if solo == "inner":                      # a pad: flat, and plays on
        return 0.3 if b < 16 else 0.0
    return 0.0
with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(b"".join(struct.pack("<hh", *[int(32767 * amp(i / sr) * math.sin(2 * math.pi * 220 * i / sr))] * 2)
                           for i in range(n)))
print("chirp: wrote", out, file=sys.stderr)
'''


def tone(seconds, env):
    t = np.arange(int(seconds * SR)) / SR
    return np.sin(2 * np.pi * 220 * t) * env(t)


class Notes(unittest.TestCase):
    def test_a_chord_is_one_hold_and_short_notes_are_not_holds(self):
        t = {"notes": [{"at": 8, "len": 16, "pitch": "F1"}, {"at": 8, "len": 16, "pitch": "C2"}, {"len": 2, "pitch": "F1"},
                       {"at": 40, "len": 8, "pitch": "F1"}, "not a note"]}
        hs = H.holds_of(t, 8)
        self.assertEqual([(h["at"], h["len"], h["voices"], h["pitch"]) for h in hs], [(8.0, 16.0, 2, "F1,C2"), (40.0, 8.0, 1, "F1")])
        self.assertEqual([h["next"] for h in hs], [False, False])

    def test_a_hold_the_track_plays_on_from_is_marked(self):
        t = {"notes": [{"at": 0, "len": 8, "pitch": "A2"}, {"at": 8, "len": 8, "pitch": "A2"}, {"at": 16.4, "len": 1, "pitch": "A2"}]}
        self.assertEqual([h["next"] for h in H.holds_of(t, 8)], [True, True])

    def test_overlapping_pad_notes_run_on_and_the_last_does_not(self):
        t = {"notes": [{"at": 0, "len": 16.2, "pitch": "A2"}, {"at": 16, "len": 16.2, "pitch": "A2"},
                       {"at": 32, "len": 16.2, "pitch": "A2"}, {"at": 4, "len": 0.5, "pitch": "E3"}]}
        self.assertEqual([h["next"] for h in H.holds_of(t, 8)], [True, True, False])    # a short note inside is not "on"

    def test_tracks_at_any_depth_and_not_the_muted(self):
        ts = [{"name": "a", "notes": [{}]}, {"name": "bus", "tracks": [{"name": "b", "notes": [{}]}]},
              {"name": "m", "mute": True, "notes": [{}]}, {"name": "empty"}]
        self.assertEqual([t["name"] for t in H.walk(ts)], ["a", "b"])


class Measure(unittest.TestCase):
    def test_a_flat_hold_played_short_reads_flat_and_then_gone(self):
        x = np.concatenate([tone(7.2, lambda t: 0.5 + 0 * t), np.zeros(SR * 2)])       # written 8 s, sounds 7.2
        m = H.measure(x, SR, 0.0, 8.0, 0.5)
        self.assertAlmostEqual(m["fall"], 0.0, delta=0.3)
        self.assertLess(m["then"], -60)
        self.assertAlmostEqual(m["sounds"], 7.2, delta=0.1)

    def test_a_note_that_dies_away_is_read_to_where_it_stops(self):
        x = np.concatenate([tone(8.0, lambda t: 0.5 * 10 ** (-8 * t / 20)), np.zeros(SR)])   # 8 dB a second: 64 dB down
        m = H.measure(x, SR, 0.0, 8.0, 0.5)
        self.assertLess(m["fall"], -25)
        self.assertAlmostEqual(m["sounds"], 5.5, delta=0.3)                             # 40 dB under its first second

    def test_a_hold_in_the_middle_of_the_file(self):
        x = np.concatenate([np.zeros(SR * 3), tone(4.0, lambda t: 0.5 * 10 ** (-3 * t / 20)), tone(1.0, lambda t: 0.5 + 0 * t)])
        m = H.measure(x, SR, 3.0, 4.0, 0.5)
        self.assertAlmostEqual(m["fall"], -3 * 3.0, delta=1.5)                          # first second against the last
        self.assertGreater(m["then"], 5)                                                # the track plays on, louder

    def test_silence_and_a_scrap_are_silent(self):
        self.assertTrue(H.measure(np.zeros(SR * 4), SR, 0.0, 4.0, 0.5)["silent"])
        self.assertTrue(H.measure(tone(0.2, lambda t: 1 + 0 * t), SR, 0.0, 0.2, 0.5)["silent"])


class Tool(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="holds-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self.pin = os.path.join(self.root, "chirp-fake")
        with open(self.pin, "w") as f:
            f.write(FAKE_PIN)
        os.chmod(self.pin, os.stat(self.pin).st_mode | stat.S_IXUSR)
        self.song = os.path.join(self.root, "song.yaml")
        with open(self.song, "w") as f:
            f.write("tempo: 120\n")

    def run_tool(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            H.main(["--song", self.song, "--pin", self.pin, *argv])
        return out.getvalue()

    def test_the_wall_is_flat_and_cuts_the_clean_guitar_dies_the_pad_plays_on(self):
        d = json.loads(self.run_tool("--json"))
        rows = {r["track"]: r["holds"] for r in d["tracks"]}
        self.assertEqual(sorted(rows), ["clean", "inner", "wall"])                      # no short notes, no muted track
        (wall,), (clean,) = rows["wall"], rows["clean"]
        self.assertEqual((wall["voices"], wall["seconds"], wall["flat"], wall["cut"]), (2, 4.0, True, True))
        self.assertAlmostEqual(wall["fall"], 0.0, delta=0.3)
        self.assertEqual((clean["flat"], clean["cut"]), (False, False))
        self.assertLess(clean["fall"], -25)
        self.assertEqual([(h["flat"], h["cut"], h["next"]) for h in rows["inner"]], [(True, False, True), (True, True, False)])

    def test_the_table_lists_the_flat_holds_and_all_lists_every_one(self):
        text = self.run_tool()
        self.assertIn("4 notes of 8 beats or more on 3 tracks", text)
        self.assertEqual(text.count("FLAT, cut"), 2)                                    # the wall, and the pad's last chord
        self.assertEqual(text.count("bars  fall"), 2)                                   # the pad's first runs on: not listed
        self.assertIn("3 hold(s) fall less than 6 dB from start to end; 2 have a rest after them, and 2 of those cut", text)
        inner = next(ln for ln in text.splitlines() if ln.strip().startswith("inner"))
        self.assertEqual(inner.split()[-3:], ["2", "2", "1"])                           # holds, flat, run on
        self.assertEqual(self.run_tool("--all").count("bars  fall"), 4)
        self.assertNotIn("clean", self.run_tool("--tracks", "^wall$"))

    def test_min_and_flat_are_settable(self):
        self.assertIn("5 notes of 1 beats or more on 4 tracks", self.run_tool("--min", "1", "--tracks", "wall|clean|short|inner"))
        d = json.loads(self.run_tool("--json", "--flat", "100"))
        self.assertTrue(all(h["flat"] for r in d["tracks"] for h in r["holds"]))

    def test_a_plan_without_a_tempo_is_at_120(self):
        with open(self.pin) as f:
            src = f.read()
        with open(self.pin, "w") as f:
            f.write(src.replace('"tempo": 120.0, ', ''))                    # the plan leaves out a tempo of 120
        d = json.loads(self.run_tool("--json"))
        self.assertEqual(d["tempo"], 120.0)
        self.assertEqual({r["track"]: r["holds"][0]["seconds"] for r in d["tracks"]}["wall"], 4.0)

    def test_a_song_whose_tempo_changes_is_refused(self):
        with open(self.pin) as f:
            src = f.read()
        with open(self.pin, "w") as f:
            f.write(src.replace('"tempo": 120.0', '"tempo": [[0, 120], [64, 90]]'))
        with self.assertRaises(SystemExit) as e:
            self.run_tool()
        self.assertIn("fixed-tempo", str(e.exception))


if __name__ == "__main__":
    unittest.main()
