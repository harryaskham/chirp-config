#!/usr/bin/env python3
"""stemhats: absolute band levels, the quiet-band warning and the opt-in --floor-db (bd-b4a779).

  python3 tools/tests/test_stemhats.py      (from ~/.config/chirp; seconds; STEMHATS_OLD=previous stemhats.py also
                                             checks that the default output is unchanged)
"""
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
SONG = 'tempo: 120\ntracks:\n  - {name: "drums", patch: "obzen-kit", score: "k/0.01b@1 R/9.99b"}\n'
CENTRES = (1.25, 1.75, 2.25, 2.75, 3.25, 3.75)


def write_float(path, x):
    """Mono float32 WAV (a -100 dBFS signal does not survive 16-bit PCM)."""
    data = np.asarray(x, "<f4").tobytes()
    fmt = struct.pack("<HHIIHH", 3, 1, SR, SR * 4, 4, 32)
    with open(path, "wb") as f:
        f.write(b"RIFF" + struct.pack("<I", 4 + 8 + len(fmt) + 8 + len(data)) + b"WAVE")
        f.write(b"fmt " + struct.pack("<I", len(fmt)) + fmt + b"data" + struct.pack("<I", len(data)) + data)


def pulses(peak):
    """chirper-two's repro: 80 ms Hann-shaped 6.5-11.5 kHz noise pulses at the given peak amplitude."""
    rng = np.random.default_rng(7123)
    x = np.zeros(5 * SR)
    n = round(0.08 * SR)
    f = np.fft.rfftfreq(n, 1 / SR)
    for c in CENTRES:
        z = np.fft.irfft(np.fft.rfft(rng.normal(size=n)) * ((f > 6500) & (f < 11500)), n) * np.hanning(n)
        x[round(c * SR):round(c * SR) + n] += z / (np.abs(z).max() + 1e-24) * peak
    return x


class StemHats(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dir = tempfile.mkdtemp(prefix="stemhats-")
        cls.song = os.path.join(cls.dir, "song.yaml")
        with open(cls.song, "w") as f:
            f.write(SONG)
        cls.quiet = os.path.join(cls.dir, "quiet.wav")   # peak -100 dBFS, RMS about -124 dBFS
        write_float(cls.quiet, pulses(1e-5))
        cls.loud = os.path.join(cls.dir, "loud.wav")     # the same pulses at peak -20 dBFS
        write_float(cls.loud, pulses(0.1))
        t = np.arange(int(0.08 * SR)) / SR
        x = np.zeros(5 * SR)
        for c in CENTRES:
            x[int(c * SR):int(c * SR) + len(t)] = 0.1 * np.sin(2 * np.pi * 9000 * t)   # RMS -23.01 dBFS
        cls.sine = os.path.join(cls.dir, "sine.wav")
        write_float(cls.sine, x)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.dir, True)

    def run_(self, stem, *extra, tool=None):
        out = os.path.join(self.dir, f"out-{len(os.listdir(self.dir))}.yaml")
        r = subprocess.run([sys.executable, tool or os.path.join(TOOLS, "stemhats.py"), self.song, stem, out,
                            "--from", "1", "--to", "4", *extra], capture_output=True, text=True, stdin=subprocess.DEVNULL,
                           env={k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"})
        text = None
        if os.path.exists(out):
            with open(out) as f:
                text = f.read()
        r.stdout = r.stdout.replace(out, "OUT")
        return r, text

    def test_levels_are_in_dbfs(self):
        r, _ = self.run_(self.sine)
        line = next(ln for ln in r.stderr.splitlines() if ln.startswith("kept hits' band level"))
        median = float(line.split("median ")[1].split(" dBFS")[0])
        self.assertAlmostEqual(median, 20 * np.log10(0.1 / np.sqrt(2)), delta=0.3)

    def test_a_nearly_silent_band_is_reported_but_kept_by_default(self):
        r, text = self.run_(self.quiet)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("nearly silent", r.stderr)
        self.assertEqual(text.count(" h/"), len(CENTRES), text)

    def test_the_floor_drops_a_silent_band(self):
        r, text = self.run_(self.quiet, "--floor-db", "-70")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("nothing to add", r.stderr)
        self.assertIn(f"dropped {len(CENTRES)} onsets below -70 dBFS", r.stderr)
        self.assertIsNone(text)

    def test_the_floor_keeps_real_hits(self):
        _, default = self.run_(self.loud)
        r, floored = self.run_(self.loud, "--floor-db", "-70")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(floored, default)
        self.assertNotIn("nearly silent", r.stderr)

    @unittest.skipUnless(os.environ.get("STEMHATS_OLD"), "set STEMHATS_OLD to the previous stemhats.py")
    def test_the_default_output_is_unchanged(self):
        for stem in (self.quiet, self.loud, self.sine):
            new, a = self.run_(stem)
            old, b = self.run_(stem, tool=os.environ["STEMHATS_OLD"])
            self.assertEqual(a, b, stem)
            self.assertEqual(new.stdout, old.stdout, stem)
            self.assertEqual(new.returncode, old.returncode)


if __name__ == "__main__":
    unittest.main(verbosity=2)
