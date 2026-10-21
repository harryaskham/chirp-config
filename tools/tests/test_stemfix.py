#!/usr/bin/env python3
"""stemfix: wrong octaves and neighbours found from a stem (synthetic stem from the correct notes), applied only
as reported and proven (chirper-zero's request).

  python3 tools/tests/test_stemfix.py      (from ~/.config/chirp; seconds)
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
import stemfix as F  # noqa: E402

SR = 48000
RIGHT = [45, 48, 52, 57, 55, 52, 50, 48, 45, 47, 48, 52, 50, 48, 47, 45]      # A2 … one note per beat at 120 BPM
WRONG = {3: 69, 9: 46}                                                        # A3 an octave high; B2 a semitone low
HAVE_CHIRP = os.path.exists(chirpbin.resolve("chirp"))


def stem_wav(path, pitches):
    x = np.zeros(int((len(pitches) * 0.5 + 0.5) * SR))
    t = np.arange(int(0.5 * SR)) / SR
    env = np.minimum(1, t / 0.005) * np.exp(-t / 0.4)
    for i, p in enumerate(pitches):
        f = 440 * 2 ** ((p - 69) / 12)
        a = int(i * 0.5 * SR)
        x[a:a + len(t)] += 0.15 * env * sum(np.sin(2 * np.pi * h * f * t) / h for h in range(1, 7))
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(2), w.setsampwidth(2), w.setframerate(SR)
        w.writeframes(np.repeat(pcm[:, None], 2, axis=1).tobytes())


def notes_song(pitches):
    return {"tempo": 120, "tracks": [{"name": "bass", "patch": "bass", "notes": [
        {"at": f"{0.5 * i:.3f}s", "len": "0.45s", "pitch": p, "vel": 0.7} for i, p in enumerate(pitches)]}]}


def score_song(pitches):
    return {"tempo": 120, "tracks": [{"name": "bass", "patch": "bass",
                                      "score": " ".join(f"{F.spell(p, 440)}/1b@90" for p in pitches)}]}


class Find(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dir = tempfile.mkdtemp(prefix="stemfix-test-")
        cls.stem = os.path.join(cls.dir, "bass.wav")
        stem_wav(cls.stem, RIGHT)
        cls.S = F.Stem(cls.stem)
        cls.bad = [WRONG.get(i, p) for i, p in enumerate(RIGHT)]

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.dir, ignore_errors=True)

    def found(self, doc):
        ch, _, n = F.plan_fixes(doc, doc["tracks"][0], self.S, {"octave", "neighbour"}, None, None, None, 9, 15)
        return {(round(c["t"], 2), c["old"], c["new"]) for c in ch}, n

    def test_the_wrong_notes_and_only_they_are_found_in_a_notes_list(self):
        got, n = self.found(notes_song(self.bad))
        self.assertEqual(n, 16)
        self.assertEqual(got, {(1.5, 69, 57), (4.5, 46, 47)})

    def test_a_correct_part_gets_no_suggestions(self):
        got, _ = self.found(notes_song(RIGHT))
        self.assertEqual(got, set())

    def test_score_strings_are_read_and_rewritten_token_by_token(self):
        doc = score_song(self.bad)
        got, _ = self.found(doc)
        self.assertEqual(got, {(1.5, 69, 57), (4.5, 46, 47)})
        ch, _, _ = F.plan_fixes(doc, doc["tracks"][0], self.S, {"octave", "neighbour"}, None, None, None, 9, 15)
        fixed = F.apply(doc, "bass", ch)["tracks"][0]["score"].split()
        orig = doc["tracks"][0]["score"].split()
        self.assertEqual([i for i, (x, y) in enumerate(zip(orig, fixed)) if x != y], [3, 9])
        self.assertEqual((fixed[3], fixed[9]), ("A3/1b@90", "B2/1b@90"))

    def test_spelling_and_parsing_round_trip(self):
        for p in (21, 45, 46, 60, 61.5):
            self.assertAlmostEqual(F.parse_pitch(F.spell(p, 440), 440), p, places=3)
        self.assertEqual(F.parse_pitch("Bb3", 440), 58)
        self.assertIsNone(F.parse_pitch("k", 440))
        self.assertIsNone(F.parse_pitch("C:maj7", 440))


@unittest.skipUnless(HAVE_CHIRP, "needs the groove pin")
class Apply(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="stemfix-apply-")
        self.addCleanup(shutil.rmtree, self.dir, True)
        self.stem = os.path.join(self.dir, "bass.wav")
        stem_wav(self.stem, RIGHT)

    def write(self, doc):
        p = os.path.join(self.dir, "song.json")
        with open(p, "w") as f:
            json.dump(doc, f, indent=2)
        return p

    def test_at_applies_only_the_chosen_change_and_proves_it(self):
        src, out = self.write(notes_song([WRONG.get(i, p) for i, p in enumerate(RIGHT)])), os.path.join(self.dir, "out.json")
        F.main([src, "bass", self.stem, "--at", "4.5", "-o", out])
        got = [n["pitch"] for n in json.load(open(out))["tracks"][0]["notes"]]
        self.assertEqual(got, [47 if i == 9 else WRONG.get(i, p) for i, p in enumerate(RIGHT)])

    def test_a_fix_that_would_move_a_latched_octave_is_refused(self):
        # A3/1b then "C/1b" (C4 by latching after A3 … octave 3: C3). Fixing A3 -> A2 would re-latch C to C2.
        doc = {"tempo": 120, "tracks": [{"name": "bass", "patch": "bass", "score": "A3/1b@90 C/1b@90"}]}
        stem = os.path.join(self.dir, "s.wav")
        stem_wav(stem, [45, 48])
        src, out = self.write(doc), os.path.join(self.dir, "out.json")
        ch, _, _ = F.plan_fixes(doc, doc["tracks"][0], F.Stem(stem), {"octave"}, None, None, None, 9, 15)
        self.assertEqual([(c["old"], c["new"]) for c in ch], [(57, 45)], "C has no explicit octave, so only A3 is a candidate")
        with self.assertRaises(SystemExit) as e:
            F.main([src, "bass", stem, "--fix", "octave", "-o", out])
        self.assertIn("other notes' pitches", str(e.exception))
        self.assertFalse(os.path.exists(out))


if __name__ == "__main__":
    unittest.main()
