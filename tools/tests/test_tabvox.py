#!/usr/bin/env python3
"""tools/tabvox.py: the tab's syllable timeline is fitted to the vocal stem (tempo and offset), each syllable's
CMUdict phonemes land on the first stem note in its span, dictionary misses stay on marks, dry runs write nothing.

  python3 tools/tests/test_tabvox.py      (from ~/.config/chirp; ~20 s; needs the adopted chirp pin for `plan`)
"""
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
import tabvox as T  # noqa: E402

SR = 48000
BPM, T0 = 120.0, 1.5
# 8 sung quarter notes over two 4/4 bars (beats 0..7), then a bar's rest
TAB = {"newLyrics": [{"text": "hel-lo world zorbly go now"}],
       "measures": [{"signature": [4, 4], "voices": [{"beats": [
           {"duration": [1, 4], "notes": [{"fret": 60, "string": 0}]} for _ in range(4)]}]},
           {"voices": [{"beats": [{"duration": [1, 4], "notes": [{"fret": 60, "string": 0}]} for _ in range(2)]
                        + [{"duration": [1, 2], "rest": True, "notes": [{"rest": True}]}]}]}]}
CMU = "HELLO  HH AH0 L OW1\nWORLD  W ER1 L D\nGO  G OW1\nNOW  N AW1\n"


def stem(path, n_s=12.0):
    x = np.zeros(int(SR * n_s))
    t = np.arange(int(0.12 * SR)) / SR
    for b in range(6):
        i = int((T0 + b * 60 / BPM) * SR)
        x[i:i + len(t)] += np.sin(2 * np.pi * 220 * t) * np.exp(-t / 0.04)
    x = 0.5 * x / np.abs(x).max()
    with wave.open(path, "wb") as f:
        f.setnchannels(2), f.setsampwidth(2), f.setframerate(SR)
        f.writeframes(np.repeat((x * 32767).astype("<i2"), 2).tobytes())


class TabVox(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = tempfile.mkdtemp(prefix="tabvox-test-")
        stem(os.path.join(cls.d, "vocals.wav"))
        with open(os.path.join(cls.d, "tab.json"), "w") as f:
            json.dump(TAB, f)
        with open(os.path.join(cls.d, "cmu.dict"), "w") as f:
            f.write(CMU)
        # stem notes: one on each syllable, plus a melisma note inside 'world' (it must not get phonemes)
        times = [T0 + b * 0.5 for b in range(6)]
        notes = [{"at": f"{t + 0.02:.3f}s", "len": "0.3s", "pitch": 60, "vel": 0.7} for t in times]
        notes.insert(3, {"at": f"{times[2] + 0.30:.3f}s", "len": "0.1s", "pitch": 62, "vel": 0.7})
        song = {"tempo": 120, "length": "12s", "tracks": [{"name": "vox", "patch": "lead", "notes": notes}]}
        with open(os.path.join(cls.d, "song.json"), "w") as f:
            json.dump(song, f)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.d, ignore_errors=True)

    def run_(self, *args):
        return subprocess.run([sys.executable, os.path.join(TOOLS, "tabvox.py"), os.path.join(self.d, "song.json"), "vox",
                               "0", "0", "--tab", os.path.join(self.d, "tab.json"), "--stem",
                               os.path.join(self.d, "vocals.wav"), "--cmu", os.path.join(self.d, "cmu.dict"),
                               "--bpm", "110-130", *args], capture_output=True, text=True, timeout=300)

    def test_lyric_conventions_and_held_beats(self):
        toks = T.lyric_tokens("pret-ty pret- ty pret... ..ty spee... ... ...ches [Chorus] Cuc... _ ...koo")
        pieces = [x.get("piece", "_") for x in toks]
        self.assertEqual(pieces, ["pret", "ty", "pret", "ty", "pret", "ty", "spee", "_", "ches", "Cuc", "_", "koo"])
        wids = [x.get("wid") for x in toks if x["kind"] == "syl"]
        self.assertEqual(wids, [0, 0, 1, 1, 2, 2, 3, 3, 4, 4])          # each split word is one word
        cmu = {"pretty": ["P", "R", "IH1", "T", "IY0"], "speeches": ["S", "P", "IY1", "CH", "AH0", "Z"]}
        ph, miss = T.syllable_ph(toks, cmu)
        self.assertEqual(ph[:2], ["P R IH1", "T IY0"])
        self.assertIsNone(ph[7])                                         # the held beat
        self.assertEqual(miss, {"Cuckoo"})

    def test_a_held_beat_extends_its_syllable(self):
        times = [0.0, 0.5, 1.0]                     # syllable, hold, syllable
        notes = [{"at": "0.02s", "pitch": 60}, {"at": "0.52s", "pitch": 62}, {"at": "1.02s", "pitch": 60}]
        got = T.assign(notes, times, ["A", None, "B"], ["syl", "hold", "syl"])
        self.assertEqual(got, {0: (0, "A"), 2: (2, "B")})                # the held note gets nothing

    def test_onsets_skip_rests_and_carry_the_signature(self):
        self.assertEqual(T.tab_onsets(TAB), [0, 1, 2, 3, 4, 5])

    def test_fit_and_phonemes_on_the_first_note_per_syllable(self):
        out = os.path.join(self.d, "out.json")
        r = self.run_("-o", out)
        self.assertEqual(r.returncode, 0, r.stderr)
        import re
        m = re.search(r"fit ([\d.]+) BPM, ([+-][\d.]+) s", r.stdout)
        self.assertAlmostEqual(float(m.group(1)), BPM, delta=1.0)     # six onsets on 21 ms frames: within a BPM
        self.assertAlmostEqual(float(m.group(2)), T0, delta=0.05)
        self.assertIn("not in the dictionary (left on marks): zorbly", r.stdout)
        with open(out) as f:
            notes = json.load(f)["tracks"][0]["notes"]
        self.assertEqual([n.get("ph") for n in notes],
                         ["HH AH0", "L OW1", "W ER1 L D", None, None, "G OW1", "N AW1"])

    def test_dry_run_writes_nothing(self):
        out = os.path.join(self.d, "never.json")
        r = self.run_("--dry-run", "-o", out)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse(os.path.exists(out))


if __name__ == "__main__":
    unittest.main()
