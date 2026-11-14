#!/usr/bin/env python3
"""tools/hitpoke.py: does a part's hit get through the whole mix (chirper-zero's, Common Time v36).

Hermetic: a stand-in engine that answers `plan` (tempo 120: a beat is half a second), and mixes made of a steady
bed of noise with a burst at 4 kHz on each kick.

  python3 tools/tests/test_hitpoke.py      (from ~/.config/chirp; a second; needs scipy, as the tool does)
"""
import contextlib
import io
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
import hitpoke as H  # noqa: E402

SR = 48000
BEATS = [0, 2, 4, 6, 8, 10, 12, 12.06, 14, 16, 18, 20, 22]        # a hit a second; one double (30 ms on) at six seconds
ENGINE = r'''#!/usr/bin/env python3
import json, sys
print(json.dumps({"data": {"canonical": {"tracks": [
    {"name": "kick", "notes": [{"at": b} for b in %r]},
    {"name": "kit", "tracks": [{"name": "snare", "notes": [{"at": 2}, {"at": 6}]}]},
    {"name": "pad", "notes": []}]}}}))
''' % (BEATS,)


def mix(click=0.0, seconds=12.0):
    """A bed of noise, and on every kick a 10 ms burst of 4 kHz at `click` times full scale."""
    x = np.random.default_rng(6).standard_normal(int(seconds * SR)) * 0.01
    n = int(0.010 * SR)
    burst = np.sin(2 * np.pi * 4000 * np.arange(n) / SR)
    for b in BEATS:
        i = int(b * 0.5 * SR)
        if i + n <= len(x):
            x[i:i + n] += click * burst
    return x


def save(path, x):
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())
    return path


class Hitpoke(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="hitpoke-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self.engine = os.path.join(self.root, "fake-chirp")
        with open(self.engine, "w") as f:
            f.write(ENGINE)
        os.chmod(self.engine, os.stat(self.engine).st_mode | stat.S_IXUSR)
        self.song = os.path.join(self.root, "song.yaml")
        open(self.song, "w").close()
        self.flat = save(os.path.join(self.root, "flat.wav"), mix(0.0))
        self.poke = save(os.path.join(self.root, "poke.wav"), mix(0.05))

    def run_tool(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = H.main([*argv, "--pin", self.engine])
        return code, out.getvalue()

    def test_a_click_on_the_hits_reads_as_a_rise_and_a_mix_without_one_as_nothing(self):
        code, text = self.run_tool(self.song, "kick", "3000-6000", "1-7:all", "--", self.flat, self.poke)
        self.assertEqual(code, 0)
        lines = text.splitlines()
        self.assertEqual(lines[0], "%-22s" % "kick in 3000-6000 Hz" + "%16s" % "all")
        flat, poke = lines[1].split(), lines[2].split()
        self.assertEqual(flat[0], "flat.wav")
        self.assertAlmostEqual(float(flat[1]), 0.0, delta=1.5)             # the bed alone: nothing happens at the hits
        self.assertGreater(float(poke[1]), 12.0)                           # the burst stands far out of the bed's 3-6 kHz
        self.assertEqual(lines[2][-5:], "( 11)")                           # twelve seconds of hits, less the first (no room
        #                                                                    before it) and the double's second

    def test_windows_are_what_chirp_render_takes_and_the_band_matters(self):
        code, text = self.run_tool(self.song, "kick", "3000-6000", "3-5:bars", "8b-16b:beats", "4s-8s", "--", self.poke)
        self.assertEqual(text.splitlines()[0].split()[-3:], ["bars", "beats", "4s-8s"])
        row = text.splitlines()[1]
        self.assertEqual([row[22 + 16 * i:38 + 16 * i][-5:] for i in range(3)], ["(  4)", "(  4)", "(  4)"])   # four seconds each
        _, low = self.run_tool(self.song, "kick", "100-300", "1-7", "--", self.poke)
        self.assertAlmostEqual(float(low.splitlines()[1].split()[1]), 0.0, delta=1.5)   # a 4 kHz click does not show at 200 Hz

    def test_a_window_with_no_hit_prints_a_dash_and_a_nested_track_is_found(self):
        _, text = self.run_tool(self.song, "snare", "3000-6000", "0s-0.9s:early", "0.9s-4s:late", "--", self.poke)
        row = text.splitlines()[1]
        self.assertEqual(row[22:38].strip(), "-")                          # the snare (inside the kit) first hits at one second
        self.assertEqual(row[38:54][-5:], "(  2)")                         # ... and again at three

    def test_what_cannot_be_read_is_said(self):
        with self.assertRaises(SystemExit) as e:
            self.run_tool(self.song, "pad", "3000-6000", "1-7", "--", self.poke)
        self.assertEqual(str(e.exception), "no notes for pad")
        with self.assertRaises(SystemExit) as e:
            self.run_tool(self.song, "kick", "3000-6000", "seven", "--", self.poke)
        self.assertIn("a window is not FROM-TO", str(e.exception))
        with self.assertRaises(SystemExit) as e:
            self.run_tool(self.song, "kick", "high", "1-7", "--", self.poke)
        self.assertIn("is not LO-HI in hertz", str(e.exception))
        with self.assertRaises(SystemExit) as e:
            self.run_tool(os.path.join(self.root, "nosuch"), "kick", "3000-6000", "1-7", "--", self.poke)
        self.assertIn("no song", str(e.exception))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(H.main([self.song, "kick", "3000-6000", "1-7"]), 2)   # no "--": the help
        self.assertIn("hitpoke.py SONG TRACK LO-HI FROM-TO[:label]", out.getvalue())


if __name__ == "__main__":
    unittest.main()
