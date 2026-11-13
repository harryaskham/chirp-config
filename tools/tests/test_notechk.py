#!/usr/bin/env python3
"""tools/notechk.py: how one track's notes are struck, note by note, in a render of our own song (chirper-zero's,
Common Time v25; made general by chirp-eco).

Hermetic: synthetic notes whose attack, low end and noise are known, and the tool against a stand-in for `chirp plan`.

  python3 tools/tests/test_notechk.py      (from ~/.config/chirp; a few seconds)
"""
import contextlib
import io
import json
import os
import shutil
import stat
import sys
import tempfile
import unittest
import wave

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import notechk as N  # noqa: E402

SR = 48000
NOTES = [{"at": 8 + i, "len": 0.5, "pitch": "F1", "expr": {"pm": 1.0}} for i in range(8)] \
    + [{"at": 16 + i, "len": 0.5, "pitch": "Ab1"} for i in range(4)] \
    + [{"at": 20, "len": 0.25, "pitch": "F1", "expr": {"pm": 1.0}}, {"at": 20.06, "len": 0.25, "pitch": "C2", "expr": {"pm": 1.0}}]
SONG = {"tempo": 120.0, "tracks": [{"name": "bus", "tracks": [{"name": "gl", "patch": "rig", "notes": NOTES}]},
                                   {"name": "empty", "patch": "rig", "notes": []}]}


def render(times, attack_ms, low_decay, noise, seconds=8.0):
    """Notes at `times`: a tone at 500 Hz that rises over attack_ms, a 150 Hz part that dies at low_decay (1/s), and
    noise at 1-4 kHz of the given level."""
    rng = np.random.default_rng(1)
    x = np.zeros(int(seconds * SR))
    n = int(0.4 * SR)
    t = np.arange(n) / SR
    env = np.minimum(1.0, t / (attack_ms / 1000.0)) * np.exp(-6 * t)
    hiss = np.convolve(rng.standard_normal(n), np.ones(6) / 6, "same")
    note = env * (0.5 * np.sin(2 * np.pi * 500 * t) + 0.5 * np.sin(2 * np.pi * 150 * t) * np.exp(-low_decay * t)
                  + 0.25 * np.sin(2 * np.pi * 1700 * t) + noise * hiss)
    for at in times:
        i = int(at * SR)
        x[i:i + n] += note[:len(x) - i]
    return x * 0.5


class Notes(unittest.TestCase):
    def test_a_track_is_found_at_any_depth(self):
        self.assertEqual(len(N.track_notes(SONG, "gl")), 14)
        self.assertEqual(N.track_notes(SONG, "empty"), [])
        self.assertIsNone(N.track_notes(SONG, "nosuch"))

    def test_where_the_render_starts(self):
        self.assertEqual(N.start_beats("3", 120.0), 8.0)                   # bar 3, 1-indexed, in four
        self.assertEqual(N.start_beats("8b", 126.0), 8.0)
        self.assertAlmostEqual(N.start_beats("4s", 120.0), 8.0)
        self.assertIsNone(N.start_beats("riffA", 120.0))

    def test_muted_open_and_all(self):
        muted, every = N.onsets(NOTES, 8.0, 120.0, "muted")
        self.assertEqual(muted[:3], [0.0, 0.5, 1.0])
        self.assertEqual((len(muted), len(every)), (10, 14))
        self.assertEqual(N.onsets(NOTES, 8.0, 120.0, "open")[0], [4.0, 4.5, 5.0, 5.5])
        self.assertEqual(len(N.onsets(NOTES, 8.0, 120.0, "all")[0]), 14)


class Measure(unittest.TestCase):
    def setUp(self):
        self.on = [0.5 + 0.5 * i for i in range(8)]

    def test_a_slower_attack_a_ringing_low_end_and_noise_each_show(self):
        fast = N.measure(render(self.on, 2, 60, 0.0), SR, self.on, self.on)
        slow = N.measure(render(self.on, 20, 60, 0.0), SR, self.on, self.on)
        ring = N.measure(render(self.on, 2, 2, 0.0), SR, self.on, self.on)
        hiss = N.measure(render(self.on, 2, 60, 0.5), SR, self.on, self.on)
        self.assertEqual(fast["n"], 8)
        self.assertGreater(slow["rise"], fast["rise"] + 6)                 # ms
        self.assertGreater(fast["tight"], ring["tight"] + 6)               # dB: the low end that dies fast is tight
        self.assertGreater(hiss["grain"], fast["grain"] * 3)               # noise between the partials
        self.assertGreater(fast["punch"], 0)

    def test_crowded_onsets_and_the_files_edges_are_left_out(self):
        on = sorted(self.on + [2.03])                                      # 30 ms after the note at 2.0: both are crowded
        m = N.measure(render(on, 2, 60, 0.0), SR, on, on)
        self.assertEqual(m["n"], 7)
        self.assertEqual(N.measure(render([0.01, 7.9], 2, 60, 0.0), SR, [0.01, 7.9], [0.01, 7.9])["n"], 0)

    def test_no_clean_onsets_gives_none_not_nan(self):
        m = N.measure(np.zeros(SR * 2), SR, [], [])
        self.assertEqual((m["n"], m["rise"], m["grain"]), (0, None, None))


class Tool(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="notechk-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self.song = os.path.join(self.root, "song.yaml")
        open(self.song, "w").close()
        self.engine(SONG)
        on = [0.5 * i for i in range(8)]                                   # the muted notes, from bar 3 (beat 8)
        self.wav = os.path.join(self.root, "cand.wav")
        left, right = render(on, 2, 60, 0.0), render(on, 20, 60, 0.0)
        with wave.open(self.wav, "wb") as w:
            w.setnchannels(2)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes(np.stack([left, right], axis=1).clip(-1, 1).__mul__(32767).astype("<i2").tobytes())

    def engine(self, song):
        self.pin = os.path.join(self.root, "chirp-fake")
        with open(self.pin, "w") as f:
            f.write("#!/usr/bin/env python3\nimport json\nprint(json.dumps({'data': {'canonical': %r}}))\n" % (song,))
        os.chmod(self.pin, os.stat(self.pin).st_mode | stat.S_IXUSR)

    def run_tool(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            N.main([self.song, *argv, "--pin", self.pin])
        return out.getvalue()

    def test_a_row_a_file_and_the_channel_matters(self):
        left = self.run_tool("gl", "--from", "3", self.wav)
        self.assertRegex(left, r"^cand\.wav +n +7 \| rise +\d+\.\d ms  punch +\d+\.\d dB  tight +-?\d+\.\d dB  grain 0\.\d\d\n$")
        d = json.loads(self.run_tool("gl", "--from", "8b", self.wav, self.wav, "--json"))
        self.assertEqual((len(d["rows"]), d["which"], d["channel"]), (2, "muted", "left"))
        right = json.loads(self.run_tool("gl", "--from", "4s", self.wav, "--channel", "right", "--json"))["rows"][0]
        self.assertGreater(right["rise"], d["rows"][0]["rise"] + 6)        # the right channel's notes rise slower

    def test_no_onsets_is_said_and_a_wrong_track_or_position_stops(self):
        self.assertIn("no clean open onsets of gl in this render", self.run_tool("gl", "--from", "40", "--which", "open", self.wav))
        for argv in (("nosuch", self.wav), ("gl", "--from", "riffA", self.wav)):
            with self.assertRaises(SystemExit):
                self.run_tool(*argv)

    def test_a_plan_without_a_tempo_is_at_120_and_a_changing_tempo_is_refused(self):
        self.engine({k: v for k, v in SONG.items() if k != "tempo"})
        self.assertIn("n   7", self.run_tool("gl", "--from", "3", self.wav))
        self.engine(dict(SONG, tempo=[[0, 120], [8, 90]]))
        with self.assertRaises(SystemExit) as e:
            self.run_tool("gl", self.wav)
        self.assertIn("fixed-tempo", str(e.exception))


if __name__ == "__main__":
    unittest.main()
