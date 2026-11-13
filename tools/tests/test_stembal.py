#!/usr/bin/env python3
"""tools/stembal.py: a mix's nine bands beside reference records' separated stems (chirper-zero, Common Time).

Hermetic: synthetic stems (one sine each), and a stand-in engine that "renders" a sine per soloed track, so the numbers
are known: three parts of equal level, one in each of three bands.

  python3 tools/tests/test_stembal.py      (from ~/.config/chirp; a few seconds; needs ffmpeg, as the tool does)
"""
import contextlib
import io
import math
import os
import shutil
import stat
import struct
import sys
import tempfile
import unittest
import wave

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import stembal as S  # noqa: E402

FREQ = {"kick": 50.0, "bass": 100.0, "gl": 1500.0, "pad": 6000.0}     # bands 0 (<60), 1 (-120), 5 (-2k), 7 (-8k)
ENGINE = r'''#!/usr/bin/env python3
import json, math, struct, sys, wave
FREQ = %r
a = sys.argv[1:]
if "plan" in a:
    print(json.dumps({"data": {"canonical": {"tracks": [{"name": "kick", "patch": "metal-kit"}, {"name": "bass", "patch": "ct-bass"},
                                                       {"name": "gl", "patch": "ct-chug-l"}, {"name": "pad", "patch": "juno"}]}}}))
    sys.exit(0)
solo = [a[i + 1] for i, x in enumerate(a) if x == "--solo"]
for t in solo:
    if t not in FREQ:
        print(json.dumps({"status": "error", "error": "no track named " + t}))
        sys.exit(2)
parts = solo or ["kick", "bass", "gl"]
n = 44100 * 2
with wave.open(a[a.index("-o") + 1], "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(44100)
    w.writeframes(b"".join(struct.pack("<h", int(8000 * sum(math.sin(2 * math.pi * FREQ[p] * i / 44100) for p in parts)))
                           for i in range(n)))
''' % (FREQ,)


# A second stand-in that keeps time: tempo 120 in 4/4, --from/--to honoured (bars, beats, seconds), a bass that changes
# band at six seconds and a level that rises, so windows differ; every sample depends only on its place in the song, as
# the engine's do, so a window render and a cut from a longer render are the same samples. It logs every render.
TIMED = r'''#!/usr/bin/env python3
import json, math, os, struct, sys, wave
a = sys.argv[1:]
META = %s
if "plan" in a:
    print(json.dumps({"data": {"canonical": dict(META, tracks=[{"name": "kick", "patch": "metal-kit"},
                                                                {"name": "bass", "patch": "ct-bass"},
                                                                {"name": "gl", "patch": "ct-chug-l"}])}}))
    sys.exit(0)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "calls.log"), "a") as f:
    f.write(" ".join(a) + "\n")
def secs(tok):
    if tok.endswith("s"): return float(tok[:-1])
    if tok.endswith("b"): return float(tok[:-1]) * 0.5
    return (float(tok) - 1) * 4 * 0.5
sr = 48000
f0 = round(secs(a[a.index("--from") + 1]) * sr) if "--from" in a else 0
f1 = round(secs(a[a.index("--to") + 1]) * sr)
solo = [a[i + 1] for i, x in enumerate(a) if x == "--solo"] or ["kick", "bass", "gl"]
def freq(p, t):
    return {"kick": 50.0, "gl": 1500.0, "bass": 100.0 if t < 6 else 200.0}[p]
with wave.open(a[a.index("-o") + 1], "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(b"".join(struct.pack("<h", int(3000 * (1 + i / sr / 10) * sum(math.sin(2 * math.pi * freq(p, i / sr) * i / sr)
                                                                                  for p in solo))) for i in range(f0, f1)))
'''


def sine(path, freq, seconds=3.0, amp=8000):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(44100)
        w.writeframes(b"".join(struct.pack("<h", int(amp * math.sin(2 * math.pi * freq * i / 44100)))
                               for i in range(int(44100 * seconds))))


@unittest.skipUnless(shutil.which("ffmpeg"), "ffmpeg")
class Stembal(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="stembal-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self.old = S.ROOT
        S.ROOT = self.root
        self.addCleanup(lambda: setattr(S, "ROOT", self.old))
        for rec in ("recA", "recB"):
            for stem, f in (("drums", 50.0), ("bass", 100.0), ("guitar", 1500.0)):
                sine(os.path.join(self.root, "ref", "stems", "bs_roformer_sw", rec, stem + ".wav"), f)
        os.makedirs(os.path.join(self.root, "tools"))
        self.engine = os.path.join(self.root, "fake-chirp")
        with open(self.engine, "w") as f:
            f.write(ENGINE)
        os.chmod(self.engine, os.stat(self.engine).st_mode | stat.S_IXUSR)
        with open(os.path.join(self.root, "tools", "groove-pin"), "w") as f:
            f.write(self.engine + "\n")
        self.song = os.path.join(self.root, "song.yaml")
        open(self.song, "w").close()

    def run_tool(self, *argv):
        out = io.StringIO()
        old = sys.argv
        sys.argv = ["stembal.py", *argv]
        try:
            with contextlib.redirect_stdout(out):
                S.main()
        finally:
            sys.argv = old
        return out.getvalue()

    def row(self, text, name):
        line = next(ln for ln in text.splitlines() if ln.startswith(name))
        return [float(x) for x in line[22:].split()[:9]]

    def test_a_sine_lands_in_its_band(self):
        for freq, band in ((50.0, 0), (100.0, 1), (1500.0, 5), (3000.0, 6)):
            p = os.path.join(self.root, f"s{int(freq)}.wav")
            sine(p, freq)
            v = S.bands(S.load(p))
            self.assertEqual(int(v.argmax()), band, freq)
            self.assertGreater(v[band] / v.sum(), 0.99)

    def test_the_references_whole_mix_is_the_sum_of_their_stems(self):
        text = self.run_tool("refs", "--refs", "recA,recB", "--from", "0", "--dur", "2")
        med = self.row(text, "median")
        for band in (0, 1, 5):                                   # three stems of equal level: a third each, -4.8 dB
            self.assertAlmostEqual(med[band], 10 * math.log10(1 / 3), delta=0.3)
        self.assertLess(max(med[b] for b in (2, 3, 4, 6, 7, 8)), -40)
        cache = os.listdir(os.path.join(self.root, "ref", "stembal"))
        self.assertEqual(len(cache), 1)
        shutil.rmtree(os.path.join(self.root, "ref", "stems", "bs_roformer_sw", "recB"))
        with self.assertRaises(SystemExit):                      # the record list is checked before the cache is read
            self.run_tool("refs", "--refs", "recA,recB", "--from", "0", "--dur", "2")

    def test_refs_are_named_or_listed(self):
        with self.assertRaises(SystemExit) as e:
            self.run_tool("refs")
        self.assertIn("recA, recB", str(e.exception))
        with self.assertRaises(SystemExit) as e:
            self.run_tool("refs", "--refs", "recA,nope")
        self.assertIn("no stems for nope", str(e.exception))
        text = self.run_tool("refs", "--refs", "all", "--from", "0", "--dur", "2")
        self.assertIn("recA", text)
        self.assertIn("recB", text)

    def test_groups_are_guessed_from_track_and_patch_names(self):
        self.assertEqual(S.guess_groups(self.engine, self.song, dict(os.environ)),
                         {"drums": ["kick"], "bass": ["bass"], "guitar": ["gl"]})

    def test_a_song_like_the_references_reads_level_with_them(self):
        text = self.run_tool("song", self.song, "--refs", "recA,recB", "--from", "0", "--dur", "2", "--windows", "1-4:all",
                             "--out", self.root)
        self.assertIn("groups: drums = kick; bass = bass; guitar = gl", text)
        diff = self.row(text, "OURS - REFS (mean)")
        for band in (0, 1, 5):
            self.assertAlmostEqual(diff[band], 0.0, delta=0.5)
        bass = [ln for ln in text.splitlines() if ln.startswith("bass")][0]
        v = [float(x) for x in bass[22:].split()]
        self.assertEqual(max(range(9), key=lambda i: v[i]), 1)   # the bass group's energy is in 60-120 Hz
        self.assertAlmostEqual(v[9], 10 * math.log10(1 / 3), delta=0.5)   # ... and it is a third of the mix
        self.assertEqual([f for f in os.listdir(self.root) if f.startswith("sb-")], [])   # the short renders are removed

    def test_mix_only_renders_once_a_window_and_a_heavier_bass_shows(self):
        text = self.run_tool("song", self.song, "--refs", "recA,recB", "--from", "0", "--dur", "2", "--windows", "1-4",
                             "--groups", "bass=bass", "--mix-only", "--out", self.root)
        self.assertNotIn("groups:", text)
        self.assertIn("OURS - REFS (mean)", text)

    def test_a_group_naming_no_track_stops_with_the_engines_words(self):
        with self.assertRaises(SystemExit) as e:
            self.run_tool("song", self.song, "--refs", "recA", "--from", "0", "--dur", "2", "--windows", "1-4",
                          "--groups", "bass=nosuch", "--out", self.root)
        self.assertIn("render failed for bass", str(e.exception))
        self.assertIn("no track named nosuch", str(e.exception))

    def record(self, name, parts):
        """ref/NAME.wav: one second a part, each a list of (frequency, amplitude)."""
        path = os.path.join(self.root, "ref", name + ".wav")
        with wave.open(path, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(44100)
            for part in parts:
                w.writeframes(b"".join(struct.pack("<h", int(sum(a * math.sin(2 * math.pi * f * i / 44100) for f, a in part)))
                                       for i in range(44100)))

    def test_spread_is_what_a_record_moves_between_its_own_loud_passages(self):
        """Two loud seconds, the second with its 1.5 kHz part at half the amplitude, then a quiet one that does not count:
        60-120 Hz moves between -3.0 and -1.0 dB of the whole (std 1.0), 1-2 kHz between -3.0 and -7.0 (std 2.0)."""
        loud, thin, quiet = [(100, 8000), (1500, 8000)], [(100, 8000), (1500, 4000)], [(100, 80), (1500, 80)]
        for rec in ("recA", "recB"):
            self.record(rec, [loud, thin, quiet])
        text = self.run_tool("refs", "--refs", "recA,recB", "--from", "0", "--dur", "2", "--spread", "--win", "1")
        sd = self.row(text, "MEDIAN spread (std)")
        self.assertAlmostEqual(sd[1], 1.0, delta=0.1)
        self.assertAlmostEqual(sd[5], 2.0, delta=0.1)
        rng = self.row(text, "MEDIAN 10-90% range")
        self.assertAlmostEqual(rng[5], 0.8 * 4.0, delta=0.2)
        self.assertIn("recA n=2", text)                              # the quiet second is not a loud passage
        plain = self.run_tool("refs", "--refs", "recA,recB", "--from", "0", "--dur", "2")
        self.assertNotIn("spread", plain)                            # only when asked for
        self.assertTrue(text.startswith(plain))                      # ... and it only adds to the table
        song = self.run_tool("song", self.song, "--refs", "recA,recB", "--from", "0", "--dur", "2", "--windows", "1-4",
                             "--mix-only", "--spread", "--win", "1", "--out", self.root)
        self.assertAlmostEqual(self.row(song, "refs own spread (std)")[5], 2.0, delta=0.1)
        self.assertLess(song.index("OURS - REFS (mean)"), song.index("refs own spread (std)"))

    def test_spread_without_the_record_reads_the_sum_of_its_stems(self):
        text = self.run_tool("refs", "--refs", "recA,recB", "--from", "0", "--dur", "2", "--spread", "--win", "1")
        sd = self.row(text, "MEDIAN spread (std)")                   # steady sines: nothing moves
        self.assertLess(max(sd[b] for b in (0, 1, 5)), 0.05)
        with self.assertRaises(SystemExit) as e:                     # three seconds of stems hold no two 20 s windows
            self.run_tool("refs", "--refs", "recA,recB", "--from", "0", "--dur", "2", "--spread")
        self.assertIn("shorter --win", str(e.exception))

    def timed(self, meta='{"tempo": 120.0}'):
        with open(self.engine, "w") as f:
            f.write(TIMED % meta)
        log = os.path.join(self.root, "calls.log")
        if os.path.exists(log):
            os.remove(log)
        return log

    def test_one_render_a_group_gives_the_same_numbers_as_a_render_a_window(self):
        log = self.timed()
        args = ("song", self.song, "--refs", "recA,recB", "--from", "0", "--dur", "2", "--windows", "1-3:early", "5b-11b",
                "7s-10.5s:late", "--out", self.root)
        once = self.run_tool(*args)
        with open(log) as f:
            calls = f.read().splitlines()
        self.assertEqual(len(calls), 4)                                    # three groups and the mix, once each
        self.assertTrue(all("--from" not in c and "--to 10.5s" in c for c in calls))   # to the end of the last window
        os.remove(log)
        each = self.run_tool(*args, "--per-window")
        with open(log) as f:
            self.assertEqual(len(f.read().splitlines()), 12)               # as before: every window, every group
        self.assertEqual(once, each)                                       # the same text, digit for digit
        self.assertIn("== ours, late (7s-10.5s; dB re the whole mix)", once)
        early = [ln for ln in once.splitlines() if ln.startswith("bass")][0]
        late = [ln for ln in once.splitlines() if ln.startswith("bass")][2]
        self.assertNotEqual(early, late)                                   # the bass moved band: the windows are not one
        self.assertEqual([f for f in os.listdir(self.root) if f.startswith("sb-")], [])

    def test_a_song_the_cutter_cannot_place_is_rendered_window_by_window(self):
        for meta in ('{"tempo": [[0, 120], [8, 90]]}', '{"tempo": 120.0, "meter": "7/8"}', '{"tempo": 120.0, "songs": {"a": {}}}'):
            log = self.timed(meta)
            self.run_tool("song", self.song, "--refs", "recA", "--from", "0", "--dur", "2", "--windows", "1-3", "3-5",
                          "--mix-only", "--out", self.root)
            with open(log) as f:
                calls = f.read().splitlines()
            self.assertEqual(len(calls), 2, meta)
            self.assertTrue(all("--from" in c for c in calls), meta)

    def test_positions_as_the_engine_reads_them(self):
        self.assertAlmostEqual(S.position("41", 126.0), 40 * 4 * 60 / 126.0)       # a bar, 1-indexed, in four
        self.assertAlmostEqual(S.position("12b", 120.0), 6.0)
        self.assertEqual(S.position("30s", 97.0), 30.0)
        self.assertEqual(S.position("1", 120.0), 0.0)
        for bad in ("0", "1:30", "riffA", "-4", "", "12bars"):
            self.assertIsNone(S.position(bad, 120.0), bad)
        self.assertEqual(S.window_seconds({"tracks": [], "tempo": 120.0}, ["1-3:a", "5b-11b"]), [(0.0, 4.0), (2.5, 5.5)])
        self.assertIsNone(S.window_seconds({"tracks": [], "tempo": 120.0}, ["3-1"]))   # backwards
        self.assertIsNone(S.window_seconds({}, ["1-3"]))                           # no plan read: do not guess
        self.assertEqual(S.window_seconds({"tracks": []}, ["1-3"]), [(0.0, 4.0)])  # the plan leaves out a tempo of 120
        self.assertIsNone(S.window_seconds({"tracks": [], "tempo": [[0, 120]]}, ["1-3"]))

    def test_a_cut_is_the_frames_a_window_render_gives(self):
        src, dst = os.path.join(self.root, "ramp.wav"), os.path.join(self.root, "cut.wav")
        with wave.open(src, "wb") as w:
            w.setnchannels(2)
            w.setsampwidth(2)
            w.setframerate(48000)
            w.writeframes(b"".join(struct.pack("<hh", i % 30000, -(i % 30000)) for i in range(48000 * 3)))
        s0, s1 = 40 * 4 * 60 / 126.0 / 100, 55 * 4 * 60 / 126.0 / 100              # 0.7619... to 1.0476... s: between frames
        S.cut(src, dst, s0, s1)
        with wave.open(dst, "rb") as w:
            self.assertEqual((w.getnchannels(), w.getsampwidth(), w.getframerate()), (2, 2, 48000))
            self.assertEqual(w.getnframes(), round(s1 * 48000) - round(s0 * 48000))
            first = struct.unpack("<hh", w.readframes(1))
        self.assertEqual(first, (round(s0 * 48000) % 30000, -(round(s0 * 48000) % 30000)))

    def test_windows_are_required(self):
        with self.assertRaises(SystemExit) as e:
            self.run_tool("song", self.song, "--refs", "recA", "--from", "0", "--dur", "2")
        self.assertIn("--windows", str(e.exception))


if __name__ == "__main__":
    unittest.main()
