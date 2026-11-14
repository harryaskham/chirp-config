#!/usr/bin/env python3
"""presence.py's measure: a track's level against its mix while it sounds, the near share, and the buried flag; and
--windows, where every track is rendered once and the windows cut from it (the same numbers as a render a window).

  python3 tools/tests/test_presence.py      (from ~/.config/chirp; a few seconds)
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

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import presence as P  # noqa: E402

# A stand-in for chirp that keeps time: tempo 120 in 4/4, --from/--to honoured (bars, beats, seconds). Three tracks: a
# pad that holds, a lead that comes in at four seconds, and a ghost 40 dB down. Every sample depends only on its place
# in the song, as the engine's do, so a window render and a cut from a whole render are the same. It logs every render.
ENGINE = r'''#!/usr/bin/env python3
import json, math, os, struct, sys, wave
a = sys.argv[1:]
META = %s
if "plan" in a:
    print(json.dumps({"data": {"canonical": dict(META, tracks=[{"name": "pad"}, {"name": "lead"}, {"name": "ghost"},
                                                                {"name": "off", "mute": True}])}}))
    sys.exit(0)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "calls.log"), "a") as f:
    f.write(" ".join(a) + "\n")
def secs(tok):
    if tok.endswith("s"): return float(tok[:-1])
    if tok.endswith("b"): return float(tok[:-1]) * 0.5
    return (float(tok) - 1) * 4 * 0.5
sr = 48000
f0 = round(secs(a[a.index("--from") + 1]) * sr) if "--from" in a else 0
f1 = round(secs(a[a.index("--to") + 1]) * sr) if "--to" in a else 12 * sr
solo = [a[i + 1] for i, x in enumerate(a) if x == "--solo"] or ["pad", "lead", "ghost"]
def amp(p, t):
    return {"pad": 0.2, "lead": 0.4 if t >= 4 else 0.0, "ghost": 0.002}[p]
FREQ = {"pad": 220.0, "lead": 1000.0, "ghost": 3000.0}
with wave.open(a[a.index("-o") + 1], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(b"".join(struct.pack("<hh", *[int(32767 * sum(amp(p, i / sr) * math.sin(2 * math.pi * FREQ[p] * i / sr)
                                                                for p in solo))] * 2) for i in range(f0, f1)))
'''


class Windows(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="presence-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self.pin = os.path.join(self.root, "chirp-fake")
        self.song = os.path.join(self.root, "song.yaml")
        with open(self.song, "w") as f:
            f.write("tempo: 120\n")
        self.log = os.path.join(self.root, "calls.log")
        self.engine()

    def engine(self, meta='{"tempo": 120.0}'):
        with open(self.pin, "w") as f:
            f.write(ENGINE % meta)
        os.chmod(self.pin, os.stat(self.pin).st_mode | stat.S_IXUSR)
        if os.path.exists(self.log):
            os.remove(self.log)

    def calls(self):
        with open(self.log) as f:
            return f.read().splitlines()

    def run_tool(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            P.main(["--song", self.song, "--pin", self.pin, "-j", "2", *argv])
        return out.getvalue()

    def test_many_windows_in_one_run_read_as_each_does_alone(self):
        many = json.loads(self.run_tool("--windows", "1-2:before", "3-5:lead-in", "13b-21.5b", "--json"))
        self.assertEqual(len(self.calls()), 4)                             # the mix and three live tracks, once each
        self.assertTrue(all("--from" not in c and "--to 21.5b" in c for c in self.calls()))
        self.assertEqual([w["label"] for w in many["windows"]], ["before", "lead-in", ""])
        self.assertEqual(many["muted"], ["off"])
        for w in many["windows"]:
            alone = json.loads(self.run_tool("--from", w["window"][0], "--to", w["window"][1], "--json"))
            self.assertEqual(w["tracks"], alone["tracks"], w["window"])    # the same numbers, to the last digit
        before, lead_in = many["windows"][0]["tracks"], many["windows"][1]["tracks"]
        self.assertTrue(before["lead"]["silent"])                          # the lead is not in the first two seconds
        self.assertFalse(lead_in["lead"]["silent"])
        self.assertTrue(lead_in["ghost"]["buried"])

    def test_the_tables_come_one_a_window_with_their_labels(self):
        text = self.run_tool("--windows", "1-2:before", "3-5")
        heads = [ln for ln in text.splitlines() if ln.startswith("song.yaml")]
        self.assertEqual(len(heads), 2)
        self.assertIn("(before: 1 -> 2; seed 0; unmastered, K-weighted): 3 tracks, 1 muted skipped", heads[0])
        self.assertIn("(3 -> 5; seed 0;", heads[1])
        self.assertIn("silent", text.split(heads[1])[0])                   # the lead, in the first table only
        self.assertNotIn("silent", text.split(heads[1])[1])

    def test_one_window_alone_is_printed_as_it_always_was(self):
        text = self.run_tool("--from", "3", "--to", "5")
        self.assertTrue(text.startswith("song.yaml (3 -> 5; seed 0; unmastered, K-weighted): 3 tracks, 1 muted skipped\n"))
        self.assertEqual(len(self.calls()), 4)
        self.assertTrue(all("--from 3 --to 5" in c for c in self.calls()))

    def test_a_song_wincut_cannot_place_is_rendered_window_by_window(self):
        self.engine('{"tempo": [[0, 120], [8, 90]]}')
        self.run_tool("--windows", "1-2", "3-5")
        self.assertEqual(len(self.calls()), 8)
        self.assertTrue(all("--from" in c for c in self.calls()))

    def test_preroll_starts_before_the_first_window_and_reads_the_same(self):
        plain = json.loads(self.run_tool("--windows", "5-6:late", "3-4:earlier", "--json"))
        os.remove(self.log)
        fast = json.loads(self.run_tool("--windows", "5-6:late", "3-4:earlier", "--preroll", "8", "--json"))
        self.assertEqual(len(self.calls()), 4)                             # still one render a track
        self.assertTrue(all("--from 3 --preroll 8 --to 6" in c for c in self.calls()))   # from the EARLIEST window on
        self.assertEqual(fast["windows"], plain["windows"])               # the same numbers, to the last digit
        os.remove(self.log)
        one = json.loads(self.run_tool("--from", "5", "--to", "6", "--preroll", "2.5", "--json"))
        self.assertTrue(all("--from 5 --preroll 2.5 --to 6" in c for c in self.calls()))
        self.assertEqual(one["tracks"], plain["windows"][0]["tracks"])
        os.remove(self.log)
        self.run_tool("--to", "3", "--preroll", "8")                      # nothing to start before: the top it is
        self.assertTrue(all("--preroll" not in c for c in self.calls()))
        with self.assertRaises(SystemExit):
            self.run_tool("--from", "5", "--to", "6", "--preroll", "0")

    def test_stereo_reads_both_channels_power(self):
        sr = P.L.SR
        t = np.arange(sr) / sr
        tone = 0.5 * np.sin(2 * np.pi * 1000 * t)
        centre = np.stack([tone * np.sqrt(0.5), tone * np.sqrt(0.5)], axis=1)      # constant-power pan: the centre
        hard = np.stack([np.zeros_like(tone), tone], axis=1)                       # ... and hard right: as loud alone
        mono = [float(P.frames_db(x, sr).mean()) for x in (centre, hard)]
        both = [float(P.frames_db(x, sr, stereo=True).mean()) for x in (centre, hard)]
        self.assertAlmostEqual(mono[0] - mono[1], 3.0, delta=0.05)                 # the mono sum reads the hard one 3 dB low
        self.assertAlmostEqual(both[0] - both[1], 0.0, delta=0.01)                 # both channels' power: level
        self.assertAlmostEqual(float(P.frames_db(tone, sr, stereo=True).mean()), float(P.frames_db(tone, sr).mean()), places=6)
        text = self.run_tool("--from", "3", "--to", "5", "--stereo")
        self.assertIn("(3 -> 5; seed 0; unmastered, K-weighted, both channels): 3 tracks", text)

    def test_windows_and_from_do_not_mix_and_a_window_needs_two_ends(self):
        for argv in (("--windows", "1-2", "--from", "3"), ("--windows", "riffA")):
            with self.assertRaises(SystemExit):
                self.run_tool(*argv)


class Measure(unittest.TestCase):
    def test_frames_db_of_a_full_scale_sine(self):
        sr = 48000
        t = np.arange(sr * 2) / sr
        x = np.stack([np.sin(2 * np.pi * 440 * t)] * 2, axis=1)
        db = P.frames_db(x, sr)
        self.assertEqual(len(db), 5)                       # 2 s of 0.4 s frames
        self.assertAlmostEqual(float(db.mean()), -3.0, places=1)

    def test_buried_part_judged_while_it_sounds(self):
        mix = np.full(100, -10.0)
        solo = np.full(100, -200.0)
        solo[:10] = -45.0                                  # plays 10% of the time, 35 dB under the mix
        r = P.presence(mix, solo, buried=-25.0)
        self.assertAlmostEqual(r["vs_mix_db"], -35.0, places=1)
        self.assertTrue(r["buried"])
        self.assertAlmostEqual(r["active"], 0.1)
        self.assertEqual(r["near"], 0.0)

    def test_brief_but_present_part_is_not_buried(self):
        mix = np.full(100, -10.0)
        solo = np.full(100, -200.0)
        solo[50:55] = -14.0                                # brief, 4 dB under the mix while it plays
        r = P.presence(mix, solo)
        self.assertAlmostEqual(r["vs_mix_db"], -4.0, places=1)
        self.assertFalse(r["buried"])
        self.assertEqual(r["near"], 1.0)

    def test_silent_track(self):
        r = P.presence(np.full(10, -10.0), np.full(10, -200.0))
        self.assertTrue(r["silent"] and r["buried"])
        self.assertIsNone(r["vs_mix_db"])

    def test_kweighting_tames_the_sub_and_lifts_the_hats(self):
        sr = 48000
        t = np.arange(sr * 2) / sr
        sub = np.stack([0.5 * np.sin(2 * np.pi * 40 * t)] * 2, axis=1)
        hat = np.stack([0.05 * np.sin(2 * np.pi * 8000 * t)] * 2, axis=1)
        mix = sub + hat
        rms = {k: P.presence(P.frames_db(mix, sr), P.frames_db(v, sr))["vs_mix_db"] for k, v in (("sub", sub), ("hat", hat))}
        kw = {k: P.presence(P.frames_db(mix, sr, kweight=True), P.frames_db(v, sr, kweight=True))["vs_mix_db"]
              for k, v in (("sub", sub), ("hat", hat))}
        self.assertGreater(kw["hat"], rms["hat"] + 5)      # hats count for more once weighted as heard
        self.assertLess(kw["sub"], rms["sub"])


if __name__ == "__main__":
    unittest.main()
