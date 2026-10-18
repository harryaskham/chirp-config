#!/usr/bin/env python3
"""stemvox --note-range (bd-2df192): the register `--note auto` chooses from. Omitted, it is G3..F5 (MIDI 55..77) and
every output is byte-identical to before (auto, --phones, a repeated-bar --map with --carry); a C3 voice is forced an
octave up there but transcribes as C3 with --note-range C2..C5; malformed or reversed ranges fail before any analysis;
a fixed --note ignores the range; onsets, durations, velocities, phones, repeat passes and holds do not depend on it.

  python3 tools/tests/test_stemvox_range.py     (from ~/.config/chirp; STEMVOX_OLD=previous stemvox.py also compares
                                                 the default output with it)
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import wave

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(TOOLS, "stemvox.py")
OLD = os.environ.get("STEMVOX_OLD")
SR = 48000
BARS, BPM = 4, 120          # 4/4 at 120: two seconds a bar
C3 = 130.8128


def write_wav(path, x):
    y = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(np.repeat(y[:, None], 2, axis=1).tobytes())


def voice(seconds, f0, harsh=False, seed=1):
    """Syllables on every beat (0.3 s, faded): a harmonic voice at f0, or a noisier shout over it."""
    rng = np.random.default_rng(seed)
    n = int(seconds * SR)
    x = rng.normal(0, 1e-4, n)
    t = np.arange(int(0.3 * SR)) / SR
    env = np.minimum(1, np.minimum(t, t[::-1]) / 0.01)
    for k, start in enumerate(np.arange(0.05, seconds - 0.4, 0.5)):
        f = f0 * (1.0 if not harsh else 2 ** ((k % 3) / 12))
        syl = sum(np.sin(2 * np.pi * h * f * t) / h for h in range(1, 9))
        if harsh:
            syl = syl + rng.normal(0, 0.6, len(t))
        i = int(start * SR)
        x[i:i + len(t)] += 0.2 * env * syl * (0.6 + 0.4 * (k % 2))
    return x


def run(*args):
    return subprocess.run([sys.executable, *args], capture_output=True, text=True, stdin=subprocess.DEVNULL)


def pitches(out):
    return re.findall(r"(?:^|\s)([A-G][#b]?-?\d)/", out)


class NoteRange(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dir = tempfile.mkdtemp(prefix="stemvox-range-")
        cls.tab = os.path.join(cls.dir, "tab")
        os.makedirs(cls.tab)
        with open(f"{cls.tab}/songsterr-meta.json", "w") as f:
            json.dump({"tracks": [{"name": "vox"}]}, f)
        with open(f"{cls.tab}/songsterr-0.json", "w") as f:
            json.dump({"name": "vox", "automations": {"tempo": [{"measure": 0, "bpm": BPM}]},
                       "measures": [{"signature": [4, 4], "voices": [{"beats": [{"duration": [1, 1], "rest": True}]}]}
                                    for _ in range(BARS)]}, f)
        cls.map = os.path.join(cls.dir, "map.json")
        with open(cls.map, "w") as f:   # bars 1-2 play twice: 1, 2, 1.2, 2.2, 3, 4
            json.dump({"cache": cls.tab, "offset": 0.0, "repeat": [[1, 2, 1]], "parts": []}, f)
        cls.low = os.path.join(cls.dir, "low.wav")
        write_wav(cls.low, voice(12.0, C3))
        cls.shout = os.path.join(cls.dir, "shout.wav")
        write_wav(cls.shout, voice(12.0, 220.0, harsh=True))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.dir, True)

    def vox(self, stem, *extra, tool=TOOL, by_map=False):
        where = ["--map", self.map, "--bars", "1-4"] if by_map else ["--tab", self.tab, "--d0", "0", "--bars", f"1-{BARS}"]
        r = run(tool, stem, *where, *extra)
        self.assertEqual(r.returncode, 0, r.stderr)
        return r.stdout

    def default_cases(self):
        return [((self.shout, "--note", "auto"), False), ((self.shout, "--note", "auto", "--phones"), False),
                ((self.low, "--note", "auto"), False),
                ((self.shout, "--note", "auto", "--phones", "--carry"), True)]

    def test_omitted_is_the_old_register(self):
        for args, by_map in self.default_cases():
            self.assertEqual(self.vox(*args, by_map=by_map), self.vox(*args, "--note-range", "G3..F5", by_map=by_map), args)

    @unittest.skipUnless(OLD, "set STEMVOX_OLD to the previous stemvox.py to compare the default output")
    def test_omitted_is_byte_identical_to_before(self):
        for args, by_map in self.default_cases():
            self.assertEqual(self.vox(*args, by_map=by_map), self.vox(*args, tool=OLD, by_map=by_map), args)

    def test_a_low_voice_transcribes_in_a_lower_register(self):
        default = pitches(self.vox(self.low, "--note", "auto"))
        low = pitches(self.vox(self.low, "--note", "auto", "--note-range", "C2..C5"))
        self.assertGreaterEqual(len(low), 12)
        self.assertEqual(set(low), {"C3"}, low)
        self.assertNotIn("C3", default, "the default register cannot reach C3")

    def test_malformed_and_reversed_ranges_fail_first(self):
        for bad in ("C5..C3", "C3", "x..y", "C3..", "36..200"):
            r = run(TOOL, self.low, "--tab", self.tab, "--bars", "1-2", "--note", "auto", "--note-range", bad)
            self.assertNotEqual(r.returncode, 0, bad)
            self.assertIn("--note-range", r.stderr)
            self.assertEqual(r.stdout, "", bad)

    def test_a_fixed_note_ignores_the_range(self):
        r = run(TOOL, self.low, "--tab", self.tab, "--d0", "0", "--bars", f"1-{BARS}", "--note", "Eb3", "--note-range", "C2..C5")
        self.assertEqual(r.stdout, self.vox(self.low, "--note", "Eb3"))
        self.assertIn("ignored", r.stderr)

    def test_phones_repeats_and_carry_do_not_depend_on_it(self):
        args = (self.shout, "--note", "auto", "--phones", "--carry")
        a = self.vox(*args, by_map=True)
        b = self.vox(*args, "--note-range", "C2..C6", by_map=True)
        self.assertIn("bar 1.2", a, "the repeat's second pass is transcribed")
        unpitched = lambda s: re.sub(r"(^|\s)[A-G][#b]?-?\d/", r"\1P/", s)  # noqa: E731
        self.assertEqual(unpitched(a), unpitched(b))


if __name__ == "__main__":
    unittest.main(verbosity=2)
