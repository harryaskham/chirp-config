#!/usr/bin/env python3
"""tools/vocsplit.py: the records' band shares in their loud passages with the voice and without it (chirper-zero's).

Hermetic: records made of sines, one a stem (50, 100 and 1500 Hz, and a "voice" at 700 Hz that sings for the first
twelve seconds of twenty-four), so every share is known: three equal parts are -4.8 dB each, four are -6.0.

  python3 tools/tests/test_vocsplit.py      (from ~/.config/chirp; a few seconds)
"""
import contextlib
import io
import os
import shutil
import sys
import tempfile
import unittest
import wave

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import vocsplit as V  # noqa: E402

SR = 44100


def stem(path, freq, seconds=24.0, on=(0.0, 1e9), amp=6000, quiet_after=None):
    """A sine that sounds between on[0] and on[1] seconds; quiet_after: 40 dB down from that second on."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    t = np.arange(int(seconds * SR)) / SR
    x = amp * np.sin(2 * np.pi * freq * t) * ((t >= on[0]) & (t < on[1]))
    if quiet_after is not None:
        x = np.where(t >= quiet_after, x * 0.01, x)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(x.astype("<i2").tobytes())


def record(root, name, voice=(0.0, 12.0), seconds=24.0, quiet_after=None, model="bs_roformer_sw"):
    d = os.path.join(root, "ref", "stems", model, name)
    for part, f in (("drums", 50.0), ("bass", 100.0), ("guitar", 1500.0)):
        stem(os.path.join(d, part + ".wav"), f, seconds, quiet_after=quiet_after)
    if voice:
        stem(os.path.join(d, "vocals.wav"), 700.0, seconds, on=voice, quiet_after=quiet_after)


class Vocsplit(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="vocsplit-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self.old = V.ROOT
        V.ROOT = self.root
        self.addCleanup(lambda: setattr(V, "ROOT", self.old))

    def run_tool(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = V.main(list(argv))
        return code, out.getvalue()

    def test_frames_are_sorted_by_the_voice_and_the_shares_are_the_mixes(self):
        record(self.root, "recA")
        record(self.root, "recB")
        rows = V.split(["recA", "recB"])
        m = V.medians(rows)
        for band in (0, 1, 5):                                            # 50, 100 and 1500 Hz
            self.assertAlmostEqual(m["without"][band], -4.77, delta=0.05)   # a third each where nobody sings
            self.assertAlmostEqual(m["with"][band], -6.02, delta=0.05)      # a quarter each where the voice is the fourth
            self.assertAlmostEqual(m["all"][band], -5.56, delta=0.05)       # three voiced frames of five: 5/18
        self.assertAlmostEqual(m["with"][4], -6.02, delta=0.05)            # the voice's own band, 500 Hz-1 kHz
        self.assertAlmostEqual(m["all"][4], -7.78, delta=0.05)             # 3/18
        self.assertLess(m["without"][4], -60.0)
        self.assertEqual([len(rows[c]) for c in V.CLASSES], [2, 2, 2])

    def test_the_table_as_it_is_printed(self):
        record(self.root, "recA")
        code, text = self.run_tool("recA")
        self.assertEqual(code, 0)
        lines = text.splitlines()
        self.assertTrue(lines[0].startswith("%-32s %-8s %3d frames  " % ("recA", "with", 3) + "  -6.0   -6.0 "), lines[0])
        self.assertTrue(lines[1].startswith("%-32s %-8s %3d frames  " % ("recA", "without", 2)))
        self.assertTrue(lines[2].startswith("%-32s %-8s %3d frames  " % ("recA", "all", 5)))
        self.assertEqual(lines[3].rstrip(), "bands: <60 -120 -250 -500 -1k -2k -4k -8k -16k")
        self.assertTrue(lines[4].startswith("%-32s %-8s %3d records " % ("MEDIAN", "with", 1)))
        self.assertRegex(lines[8], r"^WITHOUT minus ALL +\+0\.8   \+0\.8 ")
        self.assertRegex(lines[9], r"^WITH minus ALL +-0\.5   -0\.5 +\S+ +\S+ +\+1\.8 ")

    def test_quiet_passages_do_not_count_and_one_frame_is_too_few(self):
        """The voice sings only in the quiet tail: no loud frame has it, so 'with' has too few frames and no median."""
        record(self.root, "recQ", voice=(16.0, 24.0), quiet_after=16.0)
        code, text = self.run_tool("recQ")
        self.assertIn("%-32s %-8s too few frames" % ("recQ", "with"), text)
        self.assertIn("%-32s %-8s %3d frames" % ("recQ", "without", 4), text)
        self.assertNotIn("WITHOUT minus WITH", text)
        self.assertNotIn("MEDIAN                           with ", text)

    def test_shorter_frames_and_other_thresholds(self):
        record(self.root, "recA")
        _, text = self.run_tool("recA", "--frame", "2")
        self.assertIn("%-32s %-8s %3d frames" % ("recA", "with", 6), text)
        self.assertIn("%-32s %-8s %3d frames" % ("recA", "without", 5), text)
        _, text = self.run_tool("recA", "--with", "3")                    # the voice is 6 dB under the mix: not "with" at 3
        self.assertIn("%-32s %-8s too few frames" % ("recA", "with"), text)

    def test_the_medians_are_stored_for_stembal_and_read_back_without_the_stems(self):
        record(self.root, "recA")
        first = V.cached(["recA"])
        self.assertEqual(first["n"], {"with": 1, "without": 1, "all": 1})
        self.assertTrue(os.path.exists(V.cache_file(["recA"], 4.0, 12.0, 25.0, "bs_roformer_sw")))
        shutil.rmtree(os.path.join(self.root, "ref", "stems"))
        self.assertEqual(V.cached(["recA"]), first)

    def test_a_record_without_a_vocals_stem_is_named_and_no_arguments_is_the_help(self):
        record(self.root, "recN", voice=None)
        with self.assertRaises(SystemExit) as e:
            V.split(["recN"])
        self.assertIn("no vocals stem (WAV) for recN", str(e.exception))
        code, text = self.run_tool()
        self.assertEqual(code, 2)
        self.assertIn("vocsplit.py ID...", text)


if __name__ == "__main__":
    unittest.main()
