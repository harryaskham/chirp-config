#!/usr/bin/env python3
"""floorfit: the record's noise floor measured per band and matched in the full mix (chirper-zero's request).

  python3 tools/tests/test_floorfit.py      (from ~/.config/chirp; ~15 s: the fit renders three short windows)
"""
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import wave
from contextlib import redirect_stdout

import numpy as np
from scipy import signal

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import chirpbin  # noqa: E402
import floorfit as F  # noqa: E402
from likeness import load  # noqa: E402

SR = 48000
HAVE_CHIRP = os.path.exists(chirpbin.resolve("chirp"))


def band_noise(n, lo, hi, db, seed, mono=False):
    rng = np.random.default_rng(seed)
    sos = signal.butter(6, [lo, hi], "bandpass", fs=SR, output="sos")
    x = signal.sosfilt(sos, rng.normal(size=(n, 1 if mono else 2)), axis=0)
    x = np.repeat(x, 2, axis=1) if mono else x
    return x / np.sqrt((x ** 2).mean()) * 10 ** (db / 20)


def write(path, st):
    pcm = (np.clip(st, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as f:
        f.setnchannels(2), f.setsampwidth(2), f.setframerate(SR)
        f.writeframes(pcm.tobytes())


class Measure(unittest.TestCase):
    def test_a_steady_floor_reads_its_level_and_its_independence(self):
        st = band_noise(10 * SR, 4000, 12000, -50, 1)
        (db, r), = F.floors(st, {"hiss": (3000, 16000)}).values()
        self.assertAlmostEqual(db, -50, delta=1.5)        # per-frame power wobbles a little around the mean
        self.assertLess(abs(r), 0.05)
        (_, r_mono), = F.floors(band_noise(10 * SR, 4000, 12000, -50, 2, mono=True), {"hiss": (3000, 16000)}).values()
        self.assertGreater(r_mono, 0.99)

    def test_the_floor_is_the_quiet_moments_not_the_loud_ones(self):
        st = band_noise(10 * SR, 4000, 12000, -70, 3)
        st[2 * SR:8 * SR] += band_noise(6 * SR, 4000, 12000, -30, 4)       # 60% of the time the band is loud
        (db, _), = F.floors(st, {"hiss": (3000, 16000)}, pct=10).values()
        self.assertLess(db, -65)


@unittest.skipUnless(HAVE_CHIRP, "needs the groove pin")
class Fit(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="floorfit-test-")
        self.addCleanup(shutil.rmtree, self.dir, True)
        self.song = os.path.join(self.dir, "song.json")
        with open(self.song, "w") as f:
            json.dump({"tempo": 120, "length": "8s", "tracks": [{"name": "pad", "patch": "piano", "score": "C3/16b@40"}]}, f, indent=2)
        ours = os.path.join(self.dir, "ours.wav")
        subprocess.run([chirpbin.resolve("chirp"), "render", "-f", self.song, "-o", ours], check=True, capture_output=True)
        st = load(ours)
        self.ref = os.path.join(self.dir, "ref.wav")
        write(self.ref, st + band_noise(len(st), 3500, 14000, -62, 5) + band_noise(len(st), 250, 700, -40, 6))

    def run_fit(self, *extra, bands="hiss=3000-16000"):
        out = os.path.join(self.dir, "out.json")
        buf = io.StringIO()
        with redirect_stdout(buf):
            F.main(["fit", self.song, self.ref, "-o", out, "--bands", bands, *extra])
        return out, buf.getvalue()

    def test_the_fitted_floor_lands_on_the_record_in_the_mix(self):
        out, text = self.run_fit("--from", "1", "--to", "7")
        line = next(x for x in text.splitlines() if x.startswith("hiss:"))
        want = float(line.split("record ")[1].split(" dBFS")[0])
        got = float(line.split("-> ")[1].split(" (")[0])
        self.assertAlmostEqual(got, want, delta=1.0)
        song = json.load(open(out))
        tr = next(t for t in song["tracks"] if t["name"] == "floor-hiss")
        self.assertEqual(tr["notes"][0]["len"], "8.000s")
        pat = song["patches"][tr["patch"]]["synth"]["layers"]
        self.assertEqual([x["pan"] for x in pat], [-1, 1])

    def test_a_window_is_required_and_a_loud_floor_is_skipped(self):
        with self.assertRaises(SystemExit) as e:
            self.run_fit()
        self.assertIn("--from A --to B", str(e.exception))
        out, text = self.run_fit("--from", "1", "--to", "7", bands="hiss=3000-16000,body=200-800")
        self.assertIn("body: the record's floor here is", text)      # -40 dBFS: too loud for a noise floor
        names = [t["name"] for t in json.load(open(out))["tracks"]]
        self.assertIn("floor-hiss", names)
        self.assertNotIn("floor-body", names)


if __name__ == "__main__":
    unittest.main()
