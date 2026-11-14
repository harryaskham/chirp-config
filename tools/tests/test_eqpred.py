#!/usr/bin/env python3
"""tools/eqpred.py: what a filter will do to a part, band by band, before a render.

Hermetic: the filter's response against known values, and made files whose spectra are known. (The response was
checked once against renders on pin e8830ba0: pink noise through ten filters and an eq of three bands, 24
third-octaves, within 0.01 dB.) One more test does that check again when the groove's pin is at hand.

  python3 tools/tests/test_eqpred.py      (from ~/.config/chirp; a second or two)
"""
import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import wave

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import eqpred as E  # noqa: E402

SR = 48000


def db(f, hz):
    return float(20 * np.log10(E.response(E.parse(f), [hz], SR)[0]))


def save(path, x, sr=SR):
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((np.clip(x, -1, 1) * 30000).astype("<i2").tobytes())
    return path


class Response(unittest.TestCase):
    def test_the_filters_do_what_their_names_say(self):
        self.assertAlmostEqual(db("lp:1000", 1000), 20 * np.log10(0.707), places=2)       # q is the gain at the cutoff
        self.assertAlmostEqual(db("lp:1000:0.8", 1000), 20 * np.log10(0.8), places=2)
        self.assertAlmostEqual(db("lp:1000", 100), 0.0, delta=0.01)
        self.assertLess(db("lp:1000", 8000), -30)
        self.assertAlmostEqual(db("hp:1000", 1000), 20 * np.log10(0.707), places=2)
        self.assertAlmostEqual(db("hp:1000", 10000), 0.0, delta=0.1)
        self.assertAlmostEqual(db("peak:400:1:-12", 400), -12.0, places=2)                # a peak's gain at its centre
        self.assertAlmostEqual(db("peak:400:1:-12", 20), 0.0, delta=0.05)
        self.assertAlmostEqual(db("highshelf:9000:0.707:-2", 20000), -2.0, delta=0.1)     # a shelf reaches its gain ...
        self.assertAlmostEqual(db("highshelf:9000:0.707:-2", 100), 0.0, delta=0.01)       # ... and leaves the other side
        self.assertAlmostEqual(db("highshelf:9000:0.707:-2", 9000), -1.0, delta=0.15)     # half of it at the corner
        self.assertAlmostEqual(db("lowshelf:120:0.9:4", 20), 4.0, delta=0.1)
        self.assertLess(E.response(E.parse("notch:1000:4"), [1000], SR)[0], 1e-3)        # nothing left at its centre
        self.assertAlmostEqual(db("bp:800:2", 800), 20 * np.log10(2), places=2)           # the band-pass peaks at q
        self.assertAlmostEqual(db("allpass:500", 500), 0.0, places=6)

    def test_slope_24_is_the_filter_twice(self):
        self.assertAlmostEqual(db("lp cutoff=14500 q=0.7 slope=24", 16000), 2 * db("lp cutoff=14500 q=0.7", 16000), places=6)

    def test_the_two_ways_to_write_a_filter(self):
        self.assertEqual(E.parse("lp cutoff=14250 q=0.8"), E.parse("lp:14250:0.8"))
        self.assertEqual(E.parse("highshelf cutoff=9k gain=-2dB"), E.parse("highshelf:9000::-2"))
        self.assertEqual(E.parse("lowpass cutoff=800")["kind"], "lp")
        self.assertAlmostEqual(E.parse("peak cutoff=400 gain=0.5")["gain"], -6.02, places=2)   # a bare gain is a factor
        self.assertEqual(E.parse("peak:400:1:-12dB")["gain"], -12.0)
        for bad in ("ladder:800", "lp q=2", "lp cutoff=800 mix=0.5", "peak cutoff=400 gain=-2"):
            with self.assertRaises(ValueError):
                E.parse(bad)


class OnAFile(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="eqpred-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        t = np.arange(4 * SR) / SR
        self.tone = save(os.path.join(self.root, "tone.wav"), 0.5 * np.sin(2 * np.pi * 3000 * t))
        self.two = save(os.path.join(self.root, "two.wav"), 0.4 * np.sin(2 * np.pi * 6000 * t) + 0.04 * np.sin(2 * np.pi * 10000 * t))

    def run_tool(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = E.main(list(argv))
        return code, out.getvalue()

    def test_a_band_changes_by_the_response_where_the_file_has_its_energy(self):
        code, text = self.run_tool(self.tone, "lp:3000:0.8", "--band", "2000-4000", "--band", "8000-16000")
        self.assertEqual(code, 0)
        head, row = [ln.split() for ln in text.splitlines()]
        self.assertEqual(head[-3:], ["2000-4000", "8000-16000", "all"])
        self.assertAlmostEqual(float(row[1]), 20 * np.log10(0.8), delta=0.1)       # the tone sits on the cutoff
        self.assertAlmostEqual(float(row[3]), 20 * np.log10(0.8), delta=0.1)       # and it is the whole file
        # one band, filled unevenly: 6 kHz at full level and 10 kHz 20 dB under it. A low-pass at 8 kHz takes 7 dB off
        # the upper tone and adds a little at 6 kHz; the band follows the loud one, not the mean of the two
        _, text = self.run_tool(self.two, "lp:8000", "--band", "5000-12000")
        band = float(text.splitlines()[1].split()[1])
        self.assertAlmostEqual(band, db("lp:8000", 6000), delta=0.15)
        self.assertGreater(band, (db("lp:8000", 6000) + db("lp:8000", 10000)) / 2 + 2)

    def test_filters_follow_one_another_and_the_band_sets(self):
        _, both = self.run_tool(self.tone, "peak:3000:1:-6", "highshelf:1000::-2", "--band", "2000-4000")
        self.assertAlmostEqual(float(both.splitlines()[1].split()[1]), -6.0 + db("highshelf:1000::-2", 3000), delta=0.1)
        _, octs = self.run_tool(self.tone, "peak:3000:1:-6")
        self.assertEqual(octs.splitlines()[0].split()[-10:], ["62", "125", "250", "500", "1000", "2k", "4k", "8k", "15k", "all"])
        _, thirds = self.run_tool(self.tone, "peak:3000:1:-6", "--thirds")
        self.assertEqual(len(thirds.splitlines()[0].split()), 2 + len(E.THIRDS) + 1)
        _, cut = self.run_tool(self.tone + ":1:2", "peak:3000:1:-6", "--band", "2000-4000")
        self.assertAlmostEqual(float(cut.splitlines()[1].split()[1]), -6.0, delta=0.1)

    def test_a_hit_counts_the_same_wherever_it_falls_in_a_frame(self):
        # 20 ms bursts of 3 kHz every frame and a half (a beat at 108 bpm), under a steady low tone. In frames that do
        # not overlap, bursts on the frames' edges all but vanished, so a low-pass was predicted to cost nothing.
        size, length = 16384, 960
        t = np.arange(40 * size) / SR
        tone = 0.4 * np.sin(2 * np.pi * 3000 * np.arange(length) / SR)
        got = []
        for offset in (0, size // 2, size // 3):
            x = 0.05 * np.sin(2 * np.pi * 100 * t)
            for k in range(1, 26):
                i = k * (size + size // 2) + offset - length // 2
                x[i:i + length] += tone
            power, freqs, _ = E.spectrum(save(os.path.join(self.root, f"hits{offset}.wav"), x))
            got.append(E.changes(power, freqs, E.response(E.parse("lp:1000"), freqs, SR) ** 2, [])[-1])
        self.assertLess(max(got) - min(got), 0.1)                 # the same file, the same prediction: wherever they fall
        self.assertLess(max(got), -3.0)                           # ... and the bursts are most of the file's power

    def test_what_cannot_be_read_is_said(self):
        with self.assertRaises(SystemExit) as e:
            self.run_tool(self.tone, "ladder:800")
        self.assertIn("the kind is one of lp, hp", str(e.exception))
        with self.assertRaises(SystemExit) as e:
            self.run_tool(self.tone + ":3.9", "lp:800")
        self.assertIn("shorter than", str(e.exception))
        code, text = self.run_tool(self.tone)
        self.assertEqual(code, 2)
        self.assertIn("eqpred.py FILE[:START:DUR] FILTER", text)

    def test_the_engine_agrees_when_the_grooves_pin_is_here(self):
        try:
            with open(os.path.join(TOOLS, "groove-pin")) as f:
                pin = f.read().strip()
        except OSError:
            pin = ""
        if not pin or not os.access(pin, os.X_OK):
            self.skipTest("no groove pin on this machine")
        rng = np.random.default_rng(5)
        noise = rng.standard_normal(6 * SR) * 0.1
        src = save(os.path.join(self.root, "in.wav"), noise)
        env = {k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"}
        got = {}
        for name, fx in (("dry", []), ("wet", ["lp cutoff=6000 q=0.8", {"type": "eq", "bands": [
                {"kind": "peak", "cutoff": 400, "q": 1, "gain": "-12dB"}, {"kind": "highshelf", "cutoff": 2500, "gain": "3dB"}]}])):
            song = os.path.join(self.root, name + ".json")
            with open(song, "w") as f:
                json.dump({"tempo": 120, "length": "12b", "tracks": [{"name": "t", "input": "src", "fx": fx}]}, f)
            out = os.path.join(self.root, name + ".wav")
            r = subprocess.run([pin, "render", "-f", song, "--input", "src=" + src, "--set", "loudness=null", "-o", out],
                               capture_output=True, text=True, env=env)
            self.assertEqual(r.returncode, 0, r.stderr[-300:])
            got[name] = E.spectrum(out + ":1:4")
        p0, freqs, sr = got["dry"]
        p1 = got["wet"][0]
        bands = [(c / 2 ** (1 / 6), c * 2 ** (1 / 6)) for c in E.THIRDS[4:]]
        gain2 = np.ones(len(freqs))
        for t in ("lp:6000:0.8", "peak:400:1:-12", "highshelf:2500::3"):
            gain2 *= E.response(E.parse(t), freqs, sr) ** 2
        pred = E.changes(p0, freqs, gain2, bands)[:-1]
        meas = [10 * np.log10(p1[(freqs >= lo) & (freqs < hi)].sum() / p0[(freqs >= lo) & (freqs < hi)].sum()) for lo, hi in bands]
        self.assertLess(float(np.max(np.abs(np.array(pred) - np.array(meas)))), 0.1)


if __name__ == "__main__":
    unittest.main()
