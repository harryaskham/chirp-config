#!/usr/bin/env python3
"""tools/stemfile.py: a record's stem in whatever format it is stored, and the tools that read stems through it.

The htdemucs_6s stems were packed to Opus on 5 Nov; riffpunch, drumpunch and stembal asked for PART.wav and said "no
stem" for records whose stems were all there (Pneuma, for Common Time's mid-gain bench, 12 Nov).

  python3 tools/tests/test_stemfile.py      (from ~/.config/chirp; a few seconds; needs ffmpeg with an Opus encoder)
"""
import contextlib
import io
import math
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
import wave

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import stemfile as F  # noqa: E402


def have_opus():
    if not shutil.which("ffmpeg"):
        return False
    r = subprocess.run(["ffmpeg", "-hide_banner", "-encoders"], capture_output=True, text=True)
    return "libopus" in r.stdout


def sine(path, freq=440.0, seconds=2.0, sr=48000):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(b"".join(struct.pack("<hh", *(2 * [int(9000 * math.sin(2 * math.pi * freq * i / sr))]))
                               for i in range(int(sr * seconds))))


def pack(wav, ext=".opus"):
    """What was done to the stems on 5 Nov: the WAV re-encoded, the WAV removed."""
    out = os.path.splitext(wav)[0] + ext
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", wav, "-b:a", "160k", out], check=True)
    os.remove(wav)
    return out


@unittest.skipUnless(have_opus(), "ffmpeg with libopus")
class StemFile(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="stemfile-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        F._said.clear()

    def stem(self, model, song, part, freq=440.0):
        p = os.path.join(self.root, "ref", "stems", model, song, part + ".wav")
        sine(p, freq)
        return p

    def test_a_wav_anywhere_is_read_before_a_packed_stem(self):
        self.assertIsNone(F.find(self.root, "rec", "guitar"))
        six = self.stem("htdemucs_6s", "rec", "guitar")
        sw = pack(self.stem("bs_roformer_sw", "rec", "guitar"))
        self.assertEqual(F.find(self.root, "rec", "guitar"), six)        # the WAV, though the other model comes first
        packed = pack(six)
        self.assertEqual(F.find(self.root, "rec", "guitar"), sw)         # no WAV left: the models' order decides
        os.remove(sw)
        self.assertEqual(F.find(self.root, "rec", "guitar"), packed)
        self.assertTrue(F.has(self.root, "rec", "guitar"))
        self.assertFalse(F.has(self.root, "rec", "bass"))

    def test_a_packed_stem_loads_as_the_wav_did(self):
        import likeness as L
        p = self.stem("htdemucs_6s", "rec", "guitar", 440.0)
        want = L.load(p)
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            got = F.load(pack(p))
            F.load(os.path.splitext(p)[0] + ".opus")
        self.assertEqual((got.dtype, got.shape[1]), (np.float32, 2))
        self.assertLess(abs(len(got) - len(want)), 0.02 * L.SR)
        rms = lambda x: 20 * np.log10(np.sqrt(np.mean(x.astype(float) ** 2)))   # noqa: E731
        self.assertAlmostEqual(rms(got), rms(want), delta=0.3)
        spec = np.abs(np.fft.rfft(got[:L.SR, 0]))
        self.assertAlmostEqual(float(np.argmax(spec)), 440.0, delta=2.0)
        self.assertEqual(err.getvalue().count("packed (lossy) stem"), 1)     # said once a file, on stderr

    def test_a_wav_goes_through_likeness_load_untouched(self):
        import likeness as L
        p = self.stem("htdemucs_6s", "rec", "guitar")
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            got = F.load(p)
        self.assertTrue(np.array_equal(got, L.load(p)))
        self.assertEqual(err.getvalue(), "")

    def test_riffpunch_reads_a_record_whose_stems_are_packed(self):
        import riffpunch as R
        old = R.ROOT
        self.addCleanup(lambda: setattr(R, "ROOT", old))
        R.ROOT = self.root
        pack(self.stem("htdemucs_6s", "rec", "guitar", 440.0))
        pack(self.stem("htdemucs_6s", "rec", "bass", 110.0))
        with contextlib.redirect_stderr(io.StringIO()):
            g = R.ref_audio("rec", "guitar")
            gb = R.ref_audio("rec", "guitar+bass")
        self.assertEqual(g.shape[1], 2)
        self.assertGreater(float(np.mean(gb.astype(float) ** 2)), 1.5 * float(np.mean(g.astype(float) ** 2)))
        with self.assertRaises(SystemExit) as e:
            R.ref_audio("rec", "vocals")
        self.assertIn("no vocals stem for rec", str(e.exception))

    def test_drumpunch_and_stembal_find_packed_stems(self):
        import drumpunch as D
        import stembal as S
        old = (D.ROOT, S.ROOT)
        self.addCleanup(lambda: (setattr(D, "ROOT", old[0]), setattr(S, "ROOT", old[1])))
        D.ROOT = S.ROOT = self.root
        wav = self.stem("htdemucs_6s", "rec", "drums", 60.0)
        self.assertEqual(D.ref_stem("rec"), wav)
        packed = pack(wav)
        self.assertEqual(D.ref_stem("rec"), packed)
        with self.assertRaises(SystemExit):
            D.ref_stem("other")
        self.assertEqual(S.stem_file("htdemucs_6s", "rec", "drums"), packed)
        self.assertIsNone(S.stem_file("htdemucs_6s", "rec", "guitar"))
        a = type("A", (), {"model": "htdemucs_6s", "refs": "all"})()
        self.assertEqual(S.ref_ids(a), ["rec"])


if __name__ == "__main__":
    unittest.main()
