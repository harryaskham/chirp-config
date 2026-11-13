#!/usr/bin/env python3
"""tools/voxref.py: a voice against the voices on reference records, its tone by band and its level under the mix
(chirper-zero, Common Time v18).

Hermetic: synthetic records whose "voice" is one sine at a known level under a known "band", so both tables are known.

  python3 tools/tests/test_voxref.py      (from ~/.config/chirp; a few seconds; needs ffmpeg, as the tool does)
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
import voxref as V  # noqa: E402


def tones(path, parts, seconds=4.0, sr=32000, gate=None):
    """A WAV of summed sines [(freq, amplitude)]; gate=(a, b) silences everything outside those seconds."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        out = []
        for i in range(int(sr * seconds)):
            on = gate is None or gate[0] <= i / sr < gate[1]
            out.append(struct.pack("<h", int(sum(a * math.sin(2 * math.pi * f * i / sr) for f, a in parts)) if on else 0))
        w.writeframes(b"".join(out))


@unittest.skipUnless(shutil.which("ffmpeg"), "ffmpeg")
class VoxRef(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="voxref-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        old = V.ROOT
        self.addCleanup(lambda: setattr(V, "ROOT", old))
        V.ROOT = self.root
        # two records: the voice is a 1.5 kHz sine (the 1-2 kHz band) for seconds 1-3, the band a 300 Hz sine 10 dB up
        for rec in ("recA", "recB"):
            tones(os.path.join(self.root, "ref", "stems", "bs_roformer_sw", rec, "vocals.wav"), [(1500, 3000)], gate=(1, 3))
            tones(os.path.join(self.root, "ref", rec + ".wav"), [(1500, 3000), (300, 9487)])
        self.solo = os.path.join(self.root, "solo.wav")
        self.mix = os.path.join(self.root, "mix.wav")

    def run_tool(self, *argv):
        out, old = io.StringIO(), sys.argv
        sys.argv = ["voxref.py", "--refs", "recA,recB", "--secs", "3", *argv]
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
                V.main()
        finally:
            sys.argv = old
        return out.getvalue()

    def row(self, text, name, n):
        line = next(ln for ln in text.splitlines() if ln.startswith(name))
        return [float(x.rstrip("%")) for x in line[34:].split()[:n]]

    def test_the_records_tone_and_level_are_what_was_put_in(self):
        tones(self.solo, [(1500, 3000)], gate=(1, 3))
        tones(self.mix, [(1500, 3000), (300, 9487)])
        text = self.run_tool("--ours", self.solo, self.mix)
        med = self.row(text, "records' voices, median of 2", 7)
        self.assertEqual(max(range(7), key=lambda i: med[i]), 3)            # all of the voice is in 1-2 kHz
        self.assertGreater(med[3], -0.5)
        whole, band = self.row(text, "records, median", 2)
        self.assertAlmostEqual(whole, -10.4, delta=0.5)                     # 3000 against 3000 + 9487: 10.4 dB under
        self.assertAlmostEqual(band, 0.0, delta=0.5)                        # ... and alone in 1-4 kHz
        ours = self.row(text, "OURS solo.wav", 3)
        self.assertAlmostEqual(ours[0], whole, delta=0.3)                   # the same voice in the same band: level
        diff = self.row(text, "  minus the records", 7)
        self.assertLess(abs(diff[3]), 0.5)

    def test_a_darker_louder_voice_reads_darker_and_louder(self):
        tones(self.solo, [(1500, 3000), (400, 6000)], gate=(1, 3))          # 6 dB more at 400 Hz than at 1.5 kHz
        tones(self.mix, [(1500, 3000), (400, 6000), (300, 9487)])
        text = self.run_tool("--ours", self.solo, self.mix)
        diff = self.row(text, "  minus the records", 7)
        self.assertGreater(diff[1], 20)                                     # 250-500 Hz: the records' voices have none
        self.assertLess(diff[3], -5)                                        # so 1-2 kHz is a smaller share of this voice
        self.assertGreater(self.row(text, "OURS solo.wav", 1)[0], self.row(text, "records, median", 1)[0] + 3)

    def test_only_the_frames_where_the_voice_sings_count(self):
        tones(self.solo, [(1500, 3000)], gate=(1.0, 1.5))                   # a sparse line: half a second of four
        tones(self.mix, [(1500, 3000), (300, 9487)])
        text = self.run_tool("--ours", self.solo, self.mix)
        whole, _, singing = self.row(text, "OURS solo.wav", 3)
        self.assertAlmostEqual(whole, -10.4, delta=0.7)                     # the same level as the dense line
        self.assertLess(singing, 20)

    def test_a_record_without_a_stem_is_skipped_and_none_at_all_stops(self):
        shutil.rmtree(os.path.join(self.root, "ref", "stems", "bs_roformer_sw", "recB"))
        tones(self.solo, [(1500, 3000)], gate=(1, 3))
        tones(self.mix, [(1500, 3000), (300, 9487)])
        self.assertIn("median of 1", self.run_tool("--ours", self.solo, self.mix))
        shutil.rmtree(os.path.join(self.root, "ref", "stems", "bs_roformer_sw", "recA"))
        with self.assertRaises(SystemExit) as e:
            self.run_tool("--ours", self.solo, self.mix)
        self.assertIn("vocal stem", str(e.exception))


if __name__ == "__main__":
    unittest.main()
