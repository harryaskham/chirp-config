#!/usr/bin/env python3
"""padtrans: chord-pad transcription from a stem (chirper-zero's request; its prototype, identical on Ptolemy).

  python3 tools/tests/test_padtrans.py      (from ~/.config/chirp; seconds)
"""
import json
import os
import shutil
import sys
import tempfile
import unittest
import wave

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import chirpbin  # noqa: E402
import padtrans as P  # noqa: E402

SR = 48000
CHORDS = [(57, 60, 64), (53, 57, 60), None, (55, 59, 62), (52, 55, 59)]       # Am, F, (silence), G, Em — 2 s each
HAVE_CHIRP = os.path.exists(chirpbin.resolve("chirp"))


def pad():
    x = np.zeros(int(2 * len(CHORDS) * SR))
    t = np.arange(2 * SR) / SR
    for i, ch in enumerate(CHORDS):
        if ch:
            for m in ch:
                f = 440 * 2 ** ((m - 69) / 12)
                x[i * 2 * SR:(i + 1) * 2 * SR] += 0.05 * sum(np.sin(2 * np.pi * h * f * t) / h ** 2 for h in range(1, 4))
    return x


class Transcribe(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dir = tempfile.mkdtemp(prefix="padtrans-test-")
        cls.stem = os.path.join(cls.dir, "pad.wav")
        x = pad()
        pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
        with wave.open(cls.stem, "wb") as f:
            f.setnchannels(2), f.setsampwidth(2), f.setframerate(SR)
            f.writeframes(np.repeat(pcm[:, None], 2, axis=1).tobytes())
        cls.x = x

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.dir, ignore_errors=True)

    def test_each_chord_and_the_gap_come_back(self):
        notes = P.runs(P.chords(self.x, 0, 10, win=0.5), 10, 0.5)
        got = {}
        for n in notes:
            got.setdefault((n["at"], n["len"]), set()).add(n["pitch"])
        want = {(f"{2.0 * i:.3f}s", "2.000s"): set(ch) for i, ch in enumerate(CHORDS) if ch}
        self.assertEqual(got, want)
        self.assertTrue(all(0.2 <= n["vel"] <= 1.0 for n in notes))

    def test_voices_limits_the_chord(self):
        notes = P.runs(P.chords(self.x, 0, 2, win=0.5, voices=2), 2, 0.5)
        self.assertEqual(len({n["pitch"] for n in notes}), 2)

    def song(self, track):
        p = os.path.join(self.dir, "s.json")
        with open(p, "w") as f:
            json.dump({"tempo": 120, "tracks": [track]}, f, indent=2)
        return p

    @unittest.skipUnless(HAVE_CHIRP, "needs the groove pin")
    def test_into_adds_a_track_or_replaces_notes_in_the_range(self):
        out = os.path.join(self.dir, "o.json")
        src = self.song({"name": "keys", "patch": "piano", "notes": [{"at": "1s", "len": "1s", "pitch": 40, "vel": 0.5},
                                                                     {"at": "9s", "len": "1s", "pitch": 41, "vel": 0.5}]})
        P.main([self.stem, "--from", "2", "--to", "8", "--into", src, "--track", "keys", "-o", out])
        notes = json.load(open(out))["tracks"][0]["notes"]
        self.assertEqual([n["pitch"] for n in notes if n["at"] in ("1s", "9s")], [40, 41], "notes outside the range kept")
        self.assertEqual({n["pitch"] for n in notes if n["at"] == "2.000s"}, {53, 57, 60})
        P.main([self.stem, "--from", "0", "--to", "4", "--into", src, "--track", "pad", "--patch", "piano", "-o", out])
        self.assertEqual([t["name"] for t in json.load(open(out))["tracks"]], ["keys", "pad"])

    def test_a_score_track_is_refused(self):
        src = self.song({"name": "keys", "patch": "piano", "score": "C4/1b"})
        with self.assertRaises(SystemExit) as e:
            P.main([self.stem, "--from", "0", "--to", "4", "--into", src, "--track", "keys", "-o", os.path.join(self.dir, "x.json")])
        self.assertIn("songfmt.py notes", str(e.exception))


if __name__ == "__main__":
    unittest.main()
