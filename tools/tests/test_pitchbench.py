#!/usr/bin/env python3
"""tools/pitchbench.py: the pitch a note really sounds at through a track's own rig, one held note at a time.

Hermetic: made waves whose pitch is known, a made song, and a stand-in engine that plays the bench it is given
(each note as partials 2 to 6 of its pitch, no fundamental, moved by the track's `transpose`), so the whole path is
run: the bench song, the render's window, the reading. One more test benches a real track on the groove's pin when
it is at hand.

  python3 tools/tests/test_pitchbench.py      (from ~/.config/chirp; a few seconds)
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
import pitchbench as P  # noqa: E402

SR = 48000
ENGINE = r'''#!/usr/bin/env python3
import json, sys, wave
import numpy as np
a = sys.argv[1:]
song = json.load(open(a[a.index("-f") + 1]))
beat = 60.0 / song["tempo"]
start = float(a[a.index("--from") + 1].rstrip("b")) if "--from" in a else 0.0
end = float(a[a.index("--to") + 1].rstrip("b"))
x = np.zeros(int((end - start) * beat * 48000))
names = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def hz(p, up):
    n, i = names[p[0]], 1
    while p[i] in "#b":
        n += 1 if p[i] == "#" else -1
        i += 1
    return 440.0 * 2 ** ((n + 12 * (int(p[i:]) + 1) + up - 69) / 12)
def walk(ts):
    for t in ts:
        for n in t.get("notes", []):
            i = int((n["at"] - start) * beat * 48000)
            k = int(n["len"] * beat * 48000)
            tt = np.arange(k) / 48000
            for p in n["pitch"].split(","):
                f = hz(p, t.get("transpose", 0))
                x[i:i + k] += sum(0.1 / h * np.sin(2 * np.pi * f * h * tt) for h in range(2, 7))
        walk(t.get("tracks", []))
walk(song["tracks"])
with wave.open(a[a.index("-o") + 1], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(48000)
    w.writeframes((np.repeat(np.clip(x, -1, 1)[:, None], 2, 1) * 32767).astype("<i2").tobytes())
'''


def tone(f0, partials, seconds=1.4, detune=None):
    t = np.arange(int(seconds * SR)) / SR
    return sum(a * np.sin(2 * np.pi * f0 * h * (1 + (detune or {}).get(h, 0.0)) * t) for h, a in partials.items())


class Reading(unittest.TestCase):
    def test_pitch_names(self):
        self.assertEqual(P.midi("C4"), 60)
        self.assertEqual(P.midi("Gb3"), 54)
        self.assertEqual(P.midi("F#3"), 54)
        self.assertEqual(P.midi("54"), 54)
        self.assertAlmostEqual(P.hz(P.midi("A4")), 440.0)
        self.assertAlmostEqual(P.hz(P.midi("Gb3")), 185.0, places=1)
        self.assertEqual(P.name(261.63)[0], "C4")
        self.assertAlmostEqual(P.name(440.0 * 2 ** (30 / 1200))[1], 30.0, places=3)
        for bad in ("H3", "C", "", "Cx4"):
            with self.assertRaises(ValueError):
                P.midi(bad)

    def test_the_wave_gives_the_pitch_where_the_partials_mislead(self):
        f0 = P.hz(P.midi("F1"))                                                  # 43.7 Hz
        # no fundamental and a cabinet's hump on partial sixteen: the strongest partial is nowhere near the note
        x = tone(f0, {2: 0.5, 3: 0.6, 16: 1.0, 23: 0.5})
        self.assertAlmostEqual(1200 * np.log2(P.sounds_as(x, SR) / f0), 0.0, delta=5)
        self.assertAlmostEqual(P.peaks(x, SR, top=1)[0][0], 16 * f0, delta=1.0)
        # the same note an octave up shares every partial with the lower one; the wave still tells them apart
        up = tone(2 * f0, {1: 0.3, 2: 1.0, 3: 0.5, 8: 0.7})
        self.assertAlmostEqual(1200 * np.log2(P.sounds_as(up, SR) / (2 * f0)), 0.0, delta=5)
        # one partial a few hertz off its place (an amp's sum-and-difference cluster) does not move the note
        off = tone(92.5, {1: 0.6, 2: 0.5, 3: 0.5, 4: 0.4, 5: 1.0}, detune={1: -0.016})
        self.assertAlmostEqual(1200 * np.log2(P.sounds_as(off, SR) / 92.5), 0.0, delta=12)
        self.assertAlmostEqual(1200 * np.log2(P.sounds_as(tone(261.63, {1: 1.0, 2: 0.5}), SR) / 261.63), 0.0, delta=2)
        # where the reading stops: a fundamental 20 dB under its even partials, and nothing else odd, is read an octave up
        self.assertAlmostEqual(1200 * np.log2(P.sounds_as(tone(100.0, {1: 0.1, 2: 1.0, 4: 0.5}), SR) / 100.0), 1200.0, delta=5)
        self.assertAlmostEqual(1200 * np.log2(P.sounds_as(tone(100.0, {1: 0.5, 2: 1.0, 4: 0.5}), SR) / 100.0), 0.0, delta=5)
        # a quieter tone a fifth under it ringing on (the note before, in a reverb) does not move the note
        both = tone(784.0, {1: 1.0, 2: 0.3, 3: 0.2}) + tone(523.25, {1: 0.3, 2: 0.25})
        self.assertAlmostEqual(1200 * np.log2(P.sounds_as(both, SR) / 784.0), 0.0, delta=10)

    def test_nothing_is_read_from_noise_or_silence(self):
        self.assertIsNone(P.sounds_as(np.random.default_rng(3).standard_normal(SR), SR))
        self.assertIsNone(P.sounds_as(np.zeros(SR), SR))
        self.assertIsNone(P.sounds_as(np.ones(100), SR))
        self.assertEqual(P.peaks(np.zeros(SR), SR), [])

    def test_partials_are_listed_low_to_high_with_their_levels(self):
        x = tone(200.0, {1: 0.5, 2: 1.0, 3: 0.25, 30: 1.0})                      # the 6 kHz one is over the reading's top
        pk = P.peaks(x, SR, top=6)
        self.assertEqual([round(f) for f, _ in pk], [200, 400, 600])
        self.assertEqual([round(db) for _, db in pk], [-6, 0, -12])
        self.assertEqual(len(P.peaks(x, SR, top=2)), 2)


class Bench(unittest.TestCase):
    SONG = {"tempo": 120, "length": "400b", "tail": "4s", "tracks": [
        {"name": "gl", "patch": "p", "out": "gtrs", "notes": [{"at": 0, "len": 1, "pitch": "F1"}], "warp": [{"over": "8b", "to": -1}],
         "risset": {"cycle": "8b"}, "at": 16, "repeat": 2, "stretch": 2.0, "transpose": 12, "mute": True, "auto": {"sec": {"points": []}}},
        {"name": "drums", "score": "k s k s", "tracks": [{"name": "tick", "notes": [{"at": 0, "pitch": "k"}], "risset": {"cycle": "8b"}}]},
        {"name": "sys", "gen": {"type": "ca"}}, {"name": "sub", "song": "other"}, {"name": "in", "input": "mic"}],
        "buses": [{"name": "gtrs", "fx": [{"type": "pump", "on": "drums"}]}]}

    def test_the_bench_is_the_song_with_one_tracks_notes(self):
        made, starts = P.bench(self.SONG, "gl", ["Gb3", "C4"], 3.2, 2.0, 8.0)
        self.assertEqual(starts, [8.0, 13.2])
        gl = made["tracks"][0]
        self.assertEqual(gl["notes"], [{"at": 8.0, "len": 3.2, "pitch": "Gb3", "vel": 0.85},
                                       {"at": 13.2, "len": 3.2, "pitch": "C4", "vel": 0.85}])
        self.assertEqual(sorted(gl), ["auto", "name", "notes", "out", "patch", "transpose"])     # its own clock and its mute are gone
        drums = made["tracks"][1]
        self.assertNotIn("score", drums)
        self.assertEqual(drums["tracks"][0], {"name": "tick", "notes": []})                    # a risset with no notes does not plan
        self.assertEqual(made["tracks"][2], {"name": "sys"})
        self.assertEqual(made["tracks"][3], {"name": "sub"})
        self.assertEqual(made["tracks"][4], {"name": "in", "input": "mic"})
        self.assertEqual(made["buses"], self.SONG["buses"])                                    # the rig's bus is the song's own
        self.assertEqual(self.SONG["tracks"][0]["notes"][0]["pitch"], "F1")                    # the song given is not touched
        nested, _ = P.bench(self.SONG, "tick", ["k"], 1, 1)
        self.assertEqual(nested["tracks"][1]["tracks"][0]["notes"][0]["pitch"], "k")
        with self.assertRaises(KeyError):
            P.bench(self.SONG, "nosuch", ["C4"], 1, 1)


class WholeRun(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="pitchbench-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self.engine = os.path.join(self.root, "fake-chirp")
        with open(self.engine, "w") as f:
            f.write(ENGINE)
        os.chmod(self.engine, os.stat(self.engine).st_mode | stat.S_IXUSR)
        self.song = os.path.join(self.root, "song.json")
        with open(self.song, "w") as f:
            json.dump({"tempo": 126, "length": "1636b", "tracks": [
                {"name": "wl", "notes": [{"at": 0, "len": 400, "pitch": "F1"}], "warp": [{"over": "8b", "to": -1}]},
                {"name": "up", "transpose": 12, "notes": []},
                {"name": "bass", "notes": [{"at": 0, "len": 400, "pitch": "F0"}]}]}, f)

    def run_tool(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = P.main([self.song, *argv, "--pin", self.engine])
        return code, out.getvalue()

    def test_each_note_is_read_alone_through_the_track(self):
        code, text = self.run_tool("wl", "Gb1", "Gb3", "C4", "F1,C2")
        self.assertEqual(code, 0)
        lines = text.splitlines()
        self.assertIn("track wl: each note held 1.6 s alone", lines[0])
        rows = [ln.split() for ln in lines[2:]]
        self.assertEqual([r[0] for r in rows], ["Gb1", "Gb3", "C4", "F1,C2"])
        self.assertEqual([r[2] for r in rows[:3]], ["Gb1", "Gb3", "C4"])                        # no fundamental in any of them
        self.assertTrue(all(abs(float(r[3])) <= 5 and r[4] == "cents" for r in rows[:3]))
        self.assertIn("(a chord: no one pitch)", lines[5])
        self.assertIn("x2.00)", lines[3])                                                      # the lowest partial there is the second
        self.assertNotIn("NOT AS WRITTEN", text)

    def test_a_note_that_sounds_elsewhere_is_marked(self):
        code, text = self.run_tool("up", "C3", "--json")
        row = json.loads(text)["rows"][0]
        self.assertEqual((row["note"], row["sounds"]), ("C3", "C4"))
        self.assertAlmostEqual(row["cents"], 1200.0, delta=5)
        self.assertEqual(row["partials"][0]["multiple"], 4.0)
        _, text = self.run_tool("up", "C3")
        self.assertIn("C4  NOT AS WRITTEN", text)

    def test_the_bench_can_be_put_where_a_lane_has_its_value_and_kept(self):
        keep = os.path.join(self.root, "kept")
        code, text = self.run_tool("wl", "Gb3", "C4", "--at", "137", "--hold", "1.2", "--top", "3", "--keep", keep)
        self.assertEqual(code, 0)
        self.assertIn("held 1.2 s", text)
        self.assertIn(", at 137", text)
        rows = [ln.split() for ln in text.splitlines()[2:]]
        self.assertEqual([r[2] for r in rows], ["Gb3", "C4"])
        with open(os.path.join(keep, "bench.json")) as f:
            made = json.load(f)
        self.assertEqual(made["tracks"][0]["notes"][0]["at"], 544.0)                           # bar 137 in 4/4
        self.assertNotIn("warp", made["tracks"][0])
        self.assertEqual(made["tracks"][2]["notes"], [])
        self.assertTrue(os.path.exists(os.path.join(keep, "bench.wav")))

    def test_a_note_that_still_rings_is_said(self):
        x = np.zeros(int(6.0 * SR))
        x[:int(2.6 * SR)] += tone(523.25, {1: 0.5, 2: 0.4}, seconds=2.6)                       # the first note rings through the gap
        x[int(2.6 * SR):int(4.2 * SR)] += tone(784.0, {1: 1.0, 2: 0.3}, seconds=1.6) + tone(523.25, {1: 0.25}, seconds=1.6)
        rows = P.measure(x, SR, [0.0, 2.6], 1.6, ["C5", "G5"])
        self.assertIsNone(rows[0]["rings_db"])
        self.assertAlmostEqual(rows[1]["rings_db"], -4.2, delta=1.0)
        self.assertEqual(rows[1]["sounds"], "G5")
        _, text = self.run_tool("wl", "Gb3", "C4", "--gap", "2.5")
        self.assertNotIn("still rings", text)                                                  # the stand-in engine has no tail

    def test_what_cannot_be_benched_is_said(self):
        for argv, said in ((("nosuch", "C4"), "has no track nosuch"), (("wl", "H3"), "'H3' is not a pitch"),
                           (("wl", "C4", "--at", "soon"), "--at soon: a bar (41), beats (160b) or seconds (30s)")):
            with self.assertRaises(SystemExit) as e:
                self.run_tool(*argv)
            self.assertIn(said, str(e.exception))
        with open(self.song, "w") as f:
            json.dump({"tempo": [[0, 120], [8, 90]], "tracks": [{"name": "wl", "notes": []}]}, f)
        with self.assertRaises(SystemExit) as e:
            self.run_tool("wl", "C4")
        self.assertIn("only fixed-tempo songs", str(e.exception))
        code, text = self.run_tool("wl")
        self.assertEqual(code, 2)
        self.assertIn("pitchbench.py SONG TRACK NOTE", text)


class OnThePin(unittest.TestCase):
    def test_a_real_track_plays_what_is_written(self):
        try:
            with open(os.path.join(TOOLS, "groove-pin")) as f:
                pin = f.read().strip()
        except OSError:
            pin = ""
        root = tempfile.mkdtemp(prefix="pitchbench-test-")
        self.addCleanup(shutil.rmtree, root, True)
        if not pin or not os.access(pin, os.X_OK):
            self.skipTest("no groove pin on this machine")
        song = os.path.join(root, "s.json")
        with open(song, "w") as f:
            plain = {"synth": {"layers": [{"level": "0dB"}, {"ratio": 2.0, "level": "-6dB"}],
                               "amp": {"a": "2ms", "d": "50ms", "s": 1, "r": "50ms"}}}
            json.dump({"tempo": 120, "patches": {"plain": plain}, "tracks": [
                {"name": "a", "patch": "plain", "notes": [{"at": 0, "len": 1, "pitch": "C3"}]},
                {"name": "b", "patch": "plain", "transpose": -12, "notes": []},
                {"name": "c", "notes": []}]}, f)                    # the default patch: an FM bell, modulator at 3.5
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            P.main([song, "a", "A2", "E4", "--pin", pin, "--json"])
            P.main([song, "b", "A3", "--pin", pin, "--json"])
            P.main([song, "c", "A3", "--pin", pin, "--json"])
        first, second, third = [json.loads(ln)["rows"] for ln in out.getvalue().splitlines()]
        self.assertEqual([(r["sounds"], abs(r["cents"]) < 15) for r in first], [("A2", True), ("E4", True)])
        self.assertEqual(second[0]["sounds"], "A2")                                            # the track's transpose is the rig's
        self.assertEqual(third[0]["sounds"], "A2")                 # half multiples: the bell's wave repeats an octave under


if __name__ == "__main__":
    unittest.main()
