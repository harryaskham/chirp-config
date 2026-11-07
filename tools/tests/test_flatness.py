#!/usr/bin/env python3
"""flatness.py: a steady loop is flat end to end; music that changes every block is not; runs are placed right."""
import os
import subprocess
import sys
import tempfile
import unittest
import wave

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import flatness as FL  # noqa: E402

SR = FL.SR


def tone(freqs, secs, amp=0.2):
    t = np.arange(int(SR * secs)) / SR
    return sum(amp * np.sin(2 * np.pi * f * t) for f in freqs).astype(np.float32)


def write(x):
    fd, p = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    with wave.open(p, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
    return p


CHORDS = [(261.6, 329.6, 392.0), (220.0, 261.6, 329.6), (174.6, 220.0, 261.6, 1046.5), (196.0, 246.9, 293.7, 3136.0)]


class Flatness(unittest.TestCase):
    def test_a_steady_loop_is_all_flat(self):
        p = write(tone(CHORDS[0], 64))
        pct, best, found = FL.runs(FL.changes(FL.features(FL.load(p))))
        os.unlink(p)
        self.assertEqual(pct, 100.0)
        self.assertEqual(best, 64)
        self.assertEqual(found, [(0, 64)])

    def test_a_change_every_block_is_not_flat(self):
        x = np.concatenate([tone(CHORDS[i % 4], 8, amp=0.05 + 0.1 * (i % 3)) for i in range(8)])
        p = write(x)
        pct, best, found = FL.runs(FL.changes(FL.features(FL.load(p))))
        os.unlink(p)
        self.assertEqual(pct, 0.0)
        self.assertEqual(found, [])

    def test_the_flat_run_is_placed(self):
        moving = [tone(CHORDS[i % 4], 8, amp=0.05 + 0.1 * (i % 3)) for i in range(4)]
        x = np.concatenate(moving + [tone(CHORDS[1], 40)] + moving)
        p = write(x)
        _, best, found = FL.runs(FL.changes(FL.features(FL.load(p))))
        os.unlink(p)
        self.assertEqual(found, [(32, 72)])      # exactly the 40 s hold: the jump into it is a change
        self.assertEqual(best, 40)

    def test_cli_prints_runs(self):
        p = write(tone(CHORDS[0], 40))
        out = subprocess.run([sys.executable, os.path.join(os.path.dirname(FL.__file__), "flatness.py"), p],
                             capture_output=True, text=True, check=True).stdout
        os.unlink(p)
        self.assertIn("100% flat", out)
        self.assertIn("flat 0:00-0:40 (40 s)", out)


class Mix(unittest.TestCase):
    def test_tracks_join_at_the_seam_and_spans_are_their_own(self):
        import json
        import shutil
        import chirpers as CH
        d = tempfile.mkdtemp()
        try:
            for n in (1, 2):
                x = tone(CHORDS[0], 40) if n == 1 else np.concatenate([tone(CHORDS[i % 4], 8, 0.05 + 0.1 * (i % 3))
                                                                      for i in range(5)])
                p = write(x)
                shutil.move(p, os.path.join(d, f"t{n:02d}.wav"))
                os.rename(os.path.join(d, f"t{n:02d}.wav"), os.path.join(d, f"t{n:02d}.mp3"))   # ffmpeg sniffs content
                open(os.path.join(d, f"t{n:02d}.song"), "w").write("tempo: 120\n")
            json.dump({"album": "x", "pin": "/bin/true", "tracks": [{"n": 1, "title": "a"}, {"n": 2, "title": "b"}]},
                      open(os.path.join(d, "snapshot.json"), "w"))
            saved = CH.song_timeline, CH.seam_overlaps, CH.seam_start
            CH.song_timeline = lambda pin, song: {"secs": 36.0, "times": [0.5 * i for i in range(80)], "end_beat": 72}
            CH.seam_overlaps = lambda album, default=16: ({(1, 2): 4}, 16)
            CH.seam_start = lambda tl, bars: 28.0                    # t2 enters 8 s before t1's musical end
            try:
                x, spans = FL.album_mix(d)
            finally:
                CH.song_timeline, CH.seam_overlaps, CH.seam_start = saved
            self.assertEqual([s[0] for s in spans], [1, 2])
            self.assertAlmostEqual(spans[1][2], 28.0, places=1)      # t2's entry
            self.assertAlmostEqual(len(x) / FL.SR, 28.0 + 40.0, places=1)
            self.assertAlmostEqual(spans[0][3], 28.0, places=1)      # t1's own span ends where t2 enters
        finally:
            shutil.rmtree(d)


if __name__ == "__main__":
    unittest.main()
