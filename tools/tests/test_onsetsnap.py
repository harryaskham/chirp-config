#!/usr/bin/env python3
"""tools/onsetsnap.py: each drum hit snaps to its own band's stem onset within the window and nowhere else; dry runs
write nothing; JSON sources keep their structure; the clock reads constant, mapped and ramped tempos.

  python3 tools/tests/test_onsetsnap.py      (from ~/.config/chirp; ~10 s; needs the adopted chirp pin for `plan`)
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
import onsetsnap as O  # noqa: E402

SR = 48000


def stem(path):
    """Kick bursts (60 Hz) at 1.00, 2.05, 3.50 s; one hat burst (8 kHz noise) at 2.55 s; 6 s."""
    x = np.zeros(SR * 6)
    t = np.arange(int(0.05 * SR)) / SR
    for at in (1.00, 2.05, 3.50):
        i = int(at * SR)
        x[i:i + len(t)] += np.sin(2 * np.pi * 60 * t) * np.exp(-t / 0.015)
    rng = np.random.default_rng(0)
    i = int(2.55 * SR)
    burst = rng.normal(size=len(t)) * np.exp(-t / 0.01)
    from scipy import signal
    burst = signal.sosfilt(signal.butter(4, [6000, 11000], "bandpass", fs=SR, output="sos"), burst)
    x[i:i + len(t)] += 3 * burst
    x = 0.5 * x / np.abs(x).max()
    with wave.open(path, "wb") as f:
        f.setnchannels(2), f.setsampwidth(2), f.setframerate(SR)
        f.writeframes(np.repeat((x * 32767).astype("<i2"), 2).tobytes())


SONG = {"tempo": 120, "length": "6s", "about": "kept", "tracks": [{"name": "drums", "patch": "rock-kit", "notes": [
    {"at": "2b", "len": "0.25b", "pitch": "k", "vel": 0.8},       # 1.00 s: on the 1.00 kick
    {"at": "4b", "len": "0.25b", "pitch": "k", "vel": 0.8},       # 2.00 s: the stem's kick is 50 ms late
    {"at": "5b", "len": "0.25b", "pitch": "h", "vel": 0.6},       # 2.50 s: the hat is 50 ms late
    {"at": "8b", "len": "0.25b", "pitch": "s,h", "vel": 0.7},     # 4.00 s: no mid onset anywhere
    {"at": "10b", "len": "0.25b", "pitch": "k", "vel": 0.8}]}]}   # 5.00 s: no kick within reach


class Snap(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = tempfile.mkdtemp(prefix="onsetsnap-test-")
        stem(os.path.join(cls.d, "drums.wav"))
        with open(os.path.join(cls.d, "song.json"), "w") as f:
            json.dump(SONG, f)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.d, ignore_errors=True)

    def run_(self, *args):
        return subprocess.run([sys.executable, os.path.join(TOOLS, "onsetsnap.py"), os.path.join(self.d, "song.json"),
                               "--stem", os.path.join(self.d, "drums.wav"), *args], capture_output=True, text=True,
                              timeout=300)

    def test_hits_snap_to_their_band_within_the_window(self):
        out = os.path.join(self.d, "out.json")
        r = self.run_("-o", out, "--window", "160")
        self.assertEqual(r.returncode, 0, r.stderr)
        with open(out) as f:
            got = json.load(f)
        ats = [float(n["at"].rstrip("s")) for n in got["tracks"][0]["notes"]]
        self.assertAlmostEqual(ats[0], 1.00, delta=0.01)
        self.assertAlmostEqual(ats[1], 2.05, delta=0.01)     # snapped late to the stem's kick
        self.assertAlmostEqual(ats[2], 2.55, delta=0.01)     # the hat to the hi-band onset, not the 2.05 kick
        self.assertAlmostEqual(ats[3], 4.00, delta=0.001)    # no mid onset: unchanged
        self.assertAlmostEqual(ats[4], 5.00, delta=0.001)    # no kick in reach: unchanged
        self.assertEqual(got["tracks"][0]["notes"][1]["len"], "0.1250s")   # 0.25 b at 120 BPM
        self.assertEqual(got["about"], "kept")               # the JSON source's own structure
        self.assertIn("3 of 5 hits", r.stdout)

    def test_a_yaml_out_is_one_song_yaml_document_that_renders(self):
        sys.path.insert(0, TOOLS)
        import songfmt
        out = os.path.join(self.d, "out.yaml")
        r = self.run_("-o", out, "--window", "160")
        self.assertEqual(r.returncode, 0, r.stderr)
        with open(out) as f:
            text = f.read()
        self.assertFalse(text.lstrip().startswith("{"), "a .yaml output is YAML, not JSON")
        self.assertNotIn("\n---", text)
        doc = songfmt.load(out)
        self.assertAlmostEqual(float(doc["tracks"][0]["notes"][1]["at"].rstrip("s")), 2.05, delta=0.01)
        p = subprocess.run([O.chirpbin.resolve("chirp"), "plan", "-f", out, "--json"], capture_output=True, text=True)
        self.assertEqual(json.loads(p.stdout)["status"], "success", p.stdout[-300:])

    def test_a_score_string_drum_track_is_resolved_and_snapped(self):
        song = {"tempo": 120, "length": "6s", "tracks": [{"name": "drums", "patch": "rock-kit",
                                                         "score": "R/2b k/1b R/1b [k/1b R/1b]x2"}]}
        src = os.path.join(self.d, "score.json")
        with open(src, "w") as f:
            json.dump(song, f)
        out = os.path.join(self.d, "score-out.json")
        r = subprocess.run([sys.executable, os.path.join(TOOLS, "onsetsnap.py"), src, "--stem",
                            os.path.join(self.d, "drums.wav"), "-o", out, "--window", "160"],
                           capture_output=True, text=True, timeout=300)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("score string resolved to 4 notes", r.stderr)   # 3 kicks + the end marker
        with open(out) as f:
            tr = json.load(f)["tracks"][0]
        self.assertNotIn("score", tr)
        ats = [float(n["at"].rstrip("s")) for n in tr["notes"]]
        self.assertAlmostEqual(ats[0], 1.00, delta=0.01)     # beat 2
        self.assertAlmostEqual(ats[1], 2.05, delta=0.01)     # beat 4 -> the late stem kick
        self.assertAlmostEqual(ats[2], 3.00, delta=0.001)    # beat 6: nothing within 160 ms (3.50 is 500 ms away)
        self.assertAlmostEqual(ats[3], 4.00, delta=0.001)    # the end marker stays put
        self.assertNotIn("pitch", tr["notes"][3])

    def test_kit_tracks_only(self):
        canon = {"patches": {"pp-kickharm": {"synth": {"layers": [{"wave": "sine"}]}},
                             "my-kit": {"kit": {"k": {"patch": "x"}}}},
                 "tracks": [{"name": "drums", "patch": "electro-kit"},       # built-in kit: the drums family
                            {"name": "kharm", "patch": "pp-kickharm"},       # a sine 'kick harmonic': not a kit
                            {"name": "perc", "patch": "my-kit"},             # a song-local kit
                            {"name": "bass", "patch": "808"}]}
        self.assertEqual(O.drum_tracks(canon), ["drums", "perc"])
        none = {"tracks": [{"name": "drum-loop", "patch": "pp-kickharm"}, {"name": "kharm", "patch": "pp-kickharm"}]}
        self.assertEqual(O.drum_tracks(none), ["drum-loop"])                 # no kit: track names only

    def test_canonical_note_times(self):
        self.assertEqual(O.beats(None), 0.0)
        self.assertEqual(O.beats(1.25), 1.25)
        self.assertEqual(O.beats("2b"), 2.0)
        self.assertIsNone(O.beats("0.5s"))
        self.assertAlmostEqual(O.seconds(None, O.Clock(120)), 0.0)

    def test_a_narrow_window_moves_less(self):
        r = self.run_("--dry-run", "--window", "20")
        self.assertIn("1 of 5 hits", r.stdout)               # only the 1.00 s kick is within 20 ms

    def test_dry_run_writes_nothing(self):
        out = os.path.join(self.d, "never.json")
        r = self.run_("--dry-run", "-o", out)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse(os.path.exists(out))

    def test_bands_of_kit_pieces(self):
        self.assertEqual(O.band_of("k", {}), "low")
        self.assertEqual(O.band_of("rb,oh,rd", {}), "hi")
        self.assertEqual(O.band_of("c,oh,rd,s", {}), "mid")
        self.assertEqual(O.band_of("ft", {}), "mid")
        self.assertEqual(O.band_of("k,c", {}), "low")
        self.assertEqual(O.band_of("cb", {"cb": "mid"}), "mid")

    def test_clock(self):
        self.assertAlmostEqual(O.Clock(120)(4), 2.0)
        m = O.Clock([{"at": "0b", "bpm": 120}, {"at": "4b", "bpm": 60}])
        self.assertAlmostEqual(m(6), 2.0 + 2.0)
        ramp = O.Clock([{"at": "0b", "bpm": 60, "ramp": True}, {"at": "4b", "bpm": 120}])
        self.assertAlmostEqual(ramp(4), 60 * 4 / 60 * np.log(2), delta=0.01)   # ∫ 60/bpm: 4 b from 60 to 120 BPM


if __name__ == "__main__":
    unittest.main()
