#!/usr/bin/env python3
"""tools/stops.py: how far a part's level falls between its notes, beside the same part on reference records
(chirper-zero, Common Time v19: the library's high-gain rigs never fall silent between notes, bd-42e146).

Hermetic: synthetic "guitars", one that stops between its stabs and one that holds through the rests.

  python3 tools/tests/test_stops.py      (from ~/.config/chirp; a few seconds; needs ffmpeg, as the tool does)
"""
import contextlib
import io
import math
import os
import shutil
import struct
import sys
import tempfile
import unittest
import wave

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import stops as S  # noqa: E402


def stabs(path, rest_level, seconds=6, sr=24000, freq=440.0):
    """Half-second stabs every second; between them the tone stays at rest_level of the stab's amplitude."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(b"".join(struct.pack("<h", int((9000 if (i / sr) % 1.0 < 0.5 else 9000 * rest_level)
                                                     * math.sin(2 * math.pi * freq * i / sr))) for i in range(sr * seconds)))


@unittest.skipUnless(shutil.which("ffmpeg"), "ffmpeg")
class Stops(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="stops-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        old = S.ROOT
        self.addCleanup(lambda: setattr(S, "ROOT", old))
        S.ROOT = self.root
        for rec in ("recA", "recB"):                         # the records' guitars fall 14 dB between stabs
            stabs(os.path.join(self.root, "ref", "stems", "bs_roformer_sw", rec, "guitar.wav"), 0.2)
        self.wall = os.path.join(self.root, "wall.wav")
        self.gated = os.path.join(self.root, "gated.wav")
        stabs(self.wall, 0.9)                                # holds through the rests (-0.9 dB)
        stabs(self.gated, 0.001)                             # falls 60 dB

    def run_tool(self, *argv):
        out, old = io.StringIO(), sys.argv
        sys.argv = ["stops.py", "--refs", "recA,recB,nostem", "--from", "0", "--dur", "6", *argv]
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
                S.main()
        finally:
            sys.argv = old
        return out.getvalue()

    def row(self, text, name):
        line = next(ln for ln in text.splitlines() if ln.startswith(name))
        return [float(x.rstrip("%")) for x in line[36:].split()]

    def test_a_wall_and_a_gated_part_read_as_what_they_are(self):
        text = self.run_tool("--ours", self.wall, self.gated)
        med = self.row(text, "records' guitar, median")
        self.assertAlmostEqual(med[2], -14.0, delta=1.5)                 # the quietest frames: the rests, 14 dB down
        self.assertAlmostEqual(med[3], 50.0, delta=6)                    # half the time is more than 12 dB down
        self.assertLess(med[4], 6)                                       # ... and none of it more than 20
        wall = self.row(text, "OURS wall.wav")
        self.assertGreater(wall[2], -1.5)                                # never falls: p5 within a dB and a half
        self.assertEqual(wall[3:5], [0.0, 0.0])                          # no time in gaps
        gated = self.row(text, "OURS gated.wav")
        self.assertLess(gated[2], -40)
        self.assertAlmostEqual(gated[4], 50.0, delta=6)                  # half the time more than 20 dB down
        self.assertEqual(len([ln for ln in text.splitlines() if ln.startswith("rec")]), 3)   # recA, recB, the median

    def test_a_section_where_the_part_rests_is_not_read_as_a_stop(self):
        p = os.path.join(self.root, "half.wav")
        with wave.open(p, "wb") as w:                                    # three seconds of wall, three of silence
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(24000)
            w.writeframes(b"".join(struct.pack("<h", int(9000 * math.sin(2 * math.pi * 440 * i / 24000)) if i < 72000 else 0)
                                   for i in range(144000)))
        row = self.row(self.run_tool("--ours", p), "OURS half.wav")
        self.assertGreater(row[2], -1.5)
        self.assertEqual(row[3], 0.0)
        self.assertEqual(row[5], 3.0)                                    # only the seconds where it plays count

    def test_silence_is_said_not_measured(self):
        p = os.path.join(self.root, "none.wav")
        stabs(p, 0.0, freq=0.0)
        self.assertIn("silent", self.run_tool("--ours", p))


if __name__ == "__main__":
    unittest.main()
