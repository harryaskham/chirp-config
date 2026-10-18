#!/usr/bin/env python3
"""barchroma with bends (bd-0467c9): a bent note is judged by its sounding pitch, so a G3 under bend=2 that the
record plays as A3 fits as written — no +2 correction that transpose (which keeps the bend) would turn into B3.
Bends latch across bar lines until `bend=`; bend-free bars keep their old signature.

  python3 tools/tests/test_barchroma.py            (from ~/.config/chirp; deterministic, a few seconds)
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import warnings
import wave

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(TOOLS)
SR = 48000
TOOL = os.environ.get("BARCHROMA", os.path.join(TOOLS, "barchroma.py"))   # the CLI under test
spec = importlib.util.spec_from_file_location("bc", os.path.join(TOOLS, "barchroma.py"))
B = importlib.util.module_from_spec(spec)
spec.loader.exec_module(B)

# bar: (tab line, what the record plays: [(midi, beats)])
BARS = {
    1: ("bend=2 G3/4b", [(57, 4)]),                 # bent, no reset: the bend crosses the bar line
    2: ("_/4b bend=", [(57, 4)]),                   # the held note, still bent, then reset
    3: ("G3/4b", [(55, 4)]),                        # after the reset: as written
    4: ("bend=2 G3/2b bend= _/2b", [(57, 2), (55, 2)]),   # bent, then released mid-note
    5: ("C4/4b", [(62, 4)]),                        # bend-free control: the record plays D4 (+2)
    6: ("bend=2 G3/4b bend=", [(57, 4)]),           # the bead's case: written G3, sounding A3
    7: ("bend=2 G3/4b bend=", [(59, 4)]),           # bent, and the record is higher still (B3): a real +2
}


def dump(obj, path):
    with open(path, "w") as f:
        json.dump(obj, f)


class Barchroma(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        self.dir = tempfile.mkdtemp(prefix="barchroma-")
        self.addCleanup(shutil.rmtree, self.dir, True)

    def test_bar_segments_latch_bends_across_bars(self):
        segs, bend, held, bent = B.bar_segments("bend=2 G3/4b")
        self.assertEqual((segs, bend, held, bent), ([(57.0, 4.0)], 2.0, [55], True))
        segs, bend, held, bent = B.bar_segments("_/4b bend=", bend, held)
        self.assertEqual((segs, bend, bent), ([(57.0, 4.0)], 0.0, True))
        self.assertEqual(B.bar_segments("G3/4b", bend, held)[3], False, "after the reset the next bar is bend-free")
        # a held dive: bends between holds, lengths carried to tokens without one
        segs = B.bar_segments("Gb2/32 _ bend=-1 _ bend=-3 _ bend=")[0]
        self.assertEqual(segs, [(42.0, 0.125), (42.0, 0.125), (41.0, 0.125), (39.0, 0.125)])
        # the written-pitch signature of a bent G3 is G3's; the sounding one is A3's
        self.assertTrue(np.allclose(B.predicted_segments(B.bar_segments("bend=2 G3/4b bend=")[0]),
                                    B.predicted([57])))

    def test_a_bent_note_is_not_corrected_again(self):
        cache = os.path.join(self.dir, "cache")
        os.makedirs(cache)
        dump({"tracks": [{"name": "gtr"}]}, f"{cache}/songsterr-meta.json")
        rest = {"signature": [4, 4], "voices": [{"beats": [{"duration": [1, 1], "rest": True}]}]}
        dump({"name": "gtr", "tuning": [64, 59, 55, 50, 45, 40], "measures": [dict(rest) for _ in BARS],
              "automations": {"tempo": [{"measure": 0, "bpm": 120}]}}, f"{cache}/songsterr-0.json")
        mp = {"cache": cache, "offset": 0.0, "parts": [
            {"name": "gtr", "track": 0, "patch": "x", "bars": [[1, len(BARS)]],
             "replace": {str(b): line for b, (line, _) in BARS.items()}}]}
        dump(mp, os.path.join(self.dir, "map.json"))
        # the record: each bar's notes (harmonics 1-6 at 1/h), 2 s a bar at 120 BPM
        x = np.zeros(int(2.0 * len(BARS) * SR) + SR)
        for b, (_, notes) in BARS.items():
            t = (b - 1) * 2.0
            for midi, beats in notes:
                n = int(beats * 0.5 * SR)
                tt = np.arange(n) / SR
                f0 = 440 * 2 ** ((midi - 69) / 12)
                x[int(t * SR):int(t * SR) + n] += sum(0.2 / h * np.sin(2 * np.pi * f0 * h * tt) for h in range(1, 7))
                t += beats * 0.5
        stem = os.path.join(self.dir, "gtr.wav")
        with wave.open(stem, "wb") as w:
            w.setnchannels(2)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((np.clip(np.repeat(x[:, None], 2, 1), -1, 1) * 32767).astype("<i2").tobytes())
        out = os.path.join(self.dir, "fix.json")
        run = lambda *extra: subprocess.run([sys.executable, TOOL, os.path.join(self.dir, "map.json"), "gtr", stem,
                                             "--emit", out, "--min-gain", "0.25", *extra],
                                            capture_output=True, text=True, cwd=ROOT)
        r = run()
        self.assertEqual(r.returncode, 0, r.stderr)
        rows = {ln.split()[0][1:]: ln for ln in r.stdout.splitlines() if ln.startswith("m")}
        for b in (1, 2, 3, 4, 6):
            self.assertIn("fits", rows[str(b)], r.stdout)
        for b in (1, 2, 4, 6):
            self.assertIn("bent", rows[str(b)], r.stdout)
        self.assertNotIn("bent", rows["3"])
        self.assertIn("try +2 st", rows["5"], r.stdout)
        self.assertIn("try +2 st", rows["7"], r.stdout)
        with open(out) as f:
            self.assertEqual(json.load(f), {"5": "D4/4b"}, "bent bars are listed, not emitted")
        self.assertIn("1 bent bars not emitted", r.stdout)
        # --emit-bent: the sounding pitch moves by exactly the suggestion (A3 -> B3), the bend kept, never twice
        r = run("--emit-bent")
        with open(out) as f:
            self.assertEqual(json.load(f), {"5": "D4/4b", "7": "bend=2 A3/4b bend="}, r.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
