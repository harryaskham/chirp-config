#!/usr/bin/env python3
"""tools/velramp.py: crescendos written in velocity, and whether they sound.

Hermetic: made note lists, and a stand-in engine that plans the song it is given and renders a soloed track bar by
bar: a "clean" track as loud as its notes' velocity, a "saturated" one at one level whatever is written.

  python3 tools/tests/test_velramp.py      (from ~/.config/chirp; a second or two)
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
import velramp as V  # noqa: E402

ENGINE = r'''#!/usr/bin/env python3
import json, sys, wave
import numpy as np
a = sys.argv[1:]
song = json.load(open(a[a.index("-f") + 1]))
if a[0] == "plan":
    print(json.dumps({"data": {"canonical": song}}))
    sys.exit(0)
name = a[a.index("--solo") + 1]
t = next(t for t in song["tracks"] if t["name"] == name)
beats = float(a[a.index("--to") + 1].rstrip("b"))
spb = 60.0 / song.get("tempo", 120)
x = np.zeros(int(beats * spb * 48000))
for n in t["notes"]:
    i = int(n["at"] * spb * 48000); k = int(n["len"] * spb * 48000)
    amp = 0.3 if t.get("saturated") else 0.5 * n["vel"]
    x[i:i + k] = amp * np.sin(2 * np.pi * 220 * np.arange(len(x[i:i + k])) / 48000)
with wave.open(a[a.index("-o") + 1], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(48000)
    w.writeframes((np.repeat(x[:, None], 2, 1) * 32767).astype("<i2").tobytes())
'''


def bars(vels, start=0, per=4):
    """Notes: `per` to a bar, each bar at one velocity (an accent pattern of +-4% inside it)."""
    out = []
    for b, v in enumerate(vels):
        for k in range(per):
            out.append({"at": (start + b) * 4 + k * 4 / per, "len": 4 / per, "pitch": "F1", "vel": round(v * (1.0 if k == 0 else 0.96), 4)})
    return out


APPROACH = [0.45] * 4 + [0.45, 0.54, 0.63, 0.72, 0.81, 0.9] + [0.9] * 6          # level, a six-bar ramp, level


class Finding(unittest.TestCase):
    def test_a_ramp_is_found_without_the_level_bars_round_it(self):
        self.assertEqual(V.ramps(V.bar_tops(bars(APPROACH))), [(4, 9, 0.45, 0.9)])
        self.assertEqual(V.ramps(V.bar_tops(bars(APPROACH[::-1]))), [(6, 11, 0.9, 0.45)])          # a fall is a ramp too
        up_down = V.ramps(V.bar_tops(bars([0.5, 0.6, 0.7, 0.8, 0.8, 0.7, 0.6, 0.5])))
        self.assertEqual(up_down, [(0, 3, 0.5, 0.8), (4, 7, 0.8, 0.5)])

    def test_what_is_not_a_ramp(self):
        self.assertEqual(V.ramps(V.bar_tops(bars([0.6, 0.6, 0.9, 0.9, 0.9]))), [])                # a step between sections
        self.assertEqual(V.ramps(V.bar_tops(bars([0.6, 0.9])), bars=2), [(0, 1, 0.6, 0.9)])       # unless two bars are asked for
        self.assertEqual(V.ramps(V.bar_tops(bars([0.7, 0.74, 0.78, 0.82, 0.86]))), [])            # 23%: under the 30
        self.assertEqual(len(V.ramps(V.bar_tops(bars([0.7, 0.74, 0.78, 0.82, 0.86])), least=0.2)), 1)
        gap = bars([0.4, 0.5, 0.6]) + bars([0.7, 0.8, 0.9], start=5)                              # two bars' rest between
        self.assertEqual(V.ramps(V.bar_tops(gap)), [(0, 2, 0.4, 0.6)])
        wobble = [0.5, 0.52, 0.49, 0.51, 0.5, 0.52, 0.5]
        self.assertEqual(V.ramps(V.bar_tops(bars(wobble))), [])

    def test_ghost_strokes_are_not_a_fall(self):
        # a backbeat at 0.9 in every bar; from the third bar six ghost strokes at 0.3 join it: the bar gets LOUDER
        notes = []
        for b in range(6):
            notes += [{"at": b * 4 + 1, "len": 0.5, "vel": 0.9}, {"at": b * 4 + 3, "len": 0.5, "vel": 0.9}]
            if b >= 2:
                notes += [{"at": b * 4 + k * 0.5 + 0.25, "len": 0.2, "vel": 0.3} for k in range(6)]
        self.assertEqual(V.ramps(V.bar_tops(notes)), [])
        self.assertEqual(V.bar_tops([{"at": 0, "len": 1}, {"at": 4.0, "len": 1, "vel": 0.5}], default=0.7), [(0, 0.7), (1, 0.5)])

    def test_the_song_is_read_track_by_track(self):
        song = {"tempo": 126, "tracks": [
            {"name": "gl", "notes": bars(APPROACH, start=26)},
            {"name": "kit", "tracks": [{"name": "snare", "vel": 0.6, "notes": bars([0.3, 0.5, 0.7, 0.9], start=71)}]},
            {"name": "pad", "notes": bars([0.5] * 8)}, {"name": "empty", "notes": []}]}
        rows = V.find(song)
        self.assertEqual([(r["track"], r["from"], r["to"], r["vel_from"], r["vel_to"], r["written_db"]) for r in rows],
                         [("gl", 31, 36, 0.45, 0.9, 6.0), ("snare", 72, 75, 0.3, 0.9, 9.5)])      # bars as chirp render takes them
        self.assertEqual([r["track"] for r in V.find(song, only={"snare"})], ["snare"])


class WholeRun(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="velramp-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self.engine = os.path.join(self.root, "fake-chirp")
        with open(self.engine, "w") as f:
            f.write(ENGINE)
        os.chmod(self.engine, os.stat(self.engine).st_mode | stat.S_IXUSR)
        self.song = os.path.join(self.root, "song.json")
        with open(self.song, "w") as f:
            json.dump({"tempo": 240, "tracks": [
                {"name": "tight", "saturated": True, "notes": bars(APPROACH, start=2)},
                {"name": "clean", "notes": bars(APPROACH, start=2)},
                {"name": "fade", "notes": bars([0.8, 0.6, 0.4, 0.2], start=20)},
                {"name": "pad", "notes": bars([0.5] * 8)}]}, f)

    def run_tool(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = V.main([self.song, *argv, "--pin", self.engine])
        return code, out.getvalue()

    def test_as_written(self):
        code, text = self.run_tool()
        lines = text.splitlines()
        self.assertEqual(lines[0], "song.json: 3 velocity ramps (as written; --measure says which sound)")
        self.assertRegex(lines[2], r"^  tight +7-12  0\.45 to 0\.90 +\+6\.0 dB$")
        self.assertRegex(lines[4], r"^  fade +21-24  0\.80 to 0\.20 +-12\.0 dB$")
        _, text = self.run_tool("--track", "pad")
        self.assertEqual(text.strip(), "song.json: no velocity ramp of 30% or more over 3 bars or more")

    def test_measured_the_saturated_part_does_not_sound(self):
        code, text = self.run_tool("--measure")
        lines = text.splitlines()
        self.assertEqual(lines[0], "song.json: 3 velocity ramps, 1 that does not sound")
        self.assertRegex(lines[2], r"^  tight .*\+6\.0 dB +[+-]0\.0 dB   NOT THERE$")
        self.assertRegex(lines[3], r"^  clean .*\+6\.0 dB +\+6\.0 dB$")
        self.assertRegex(lines[4], r"^  fade .*-12\.0 dB +-12\.0 dB$")
        _, text = self.run_tool("--measure", "--json", "--track", "tight,clean")
        got = {r["track"]: (r["sounds_db"], r["there"]) for r in json.loads(text)["ramps"]}
        self.assertEqual(got, {"tight": (0.0, False), "clean": (6.0, True)})

    def test_what_cannot_be_read_is_said(self):
        for song, said in (({"tempo": [[0, 120], [8, 90]], "tracks": []}, "the song's tempo changes"),
                           ({"meter": "7/8", "tracks": []}, "not in 4/4")):
            with open(self.song, "w") as f:
                json.dump(song, f)
            with self.assertRaises(SystemExit) as e:
                self.run_tool()
            self.assertIn(said, str(e.exception))
        with self.assertRaises(SystemExit) as e:
            V.main(["no-such-song", "--pin", self.engine])
        self.assertIn("no song no-such-song", str(e.exception))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(V.main([]), 2)
        self.assertIn("velramp.py SONG", out.getvalue())


if __name__ == "__main__":
    unittest.main()
