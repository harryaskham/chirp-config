#!/usr/bin/env python3
"""Map bar clocks with repeats (bd-8e945f): a synthetic tab, map and vocal stem with bursts before, inside (both
passes, at different places) and after a middle repeat. stemvox --map must find each burst at its performed time,
and tab2song must put it back there; maps without repeats keep plain `bar N` output.

  python3 tools/tests/test_maptime.py            (from ~/.config/chirp; deterministic, ~10 s)
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
BPM = 120.0          # 0.5 s a beat, 2 s a 4/4 bar
OFFSET = 0.5         # = 1 beat of lead-in
# (performed bar label, beat in that bar): before, inside both passes (different beats), the 2nd pass only, after
BURSTS = [("2", 1.0), ("3.1", 0.5), ("3.2", 2.0), ("4.2", 3.0), ("6", 1.5), ("8", 0.5)]
PERFORMED = ["1", "2", "3.1", "4.1", "3.2", "4.2", "5", "6", "7", "8"]   # repeat [3, 4, 1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(TOOLS, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


T2S = load("tab2song")


def tool(*args):
    r = subprocess.run([sys.executable, *args], capture_output=True, text=True, cwd=ROOT)
    return r


def dump(obj, path):
    with open(path, "w") as f:
        json.dump(obj, f)


def score_onsets(score):
    """Note onsets (beats from the song start) in a tab2song part score: `|` bar lines, `[bar]xN` repeats, R rests."""
    toks = []
    for item in score.split(" | "):
        item = item.strip()
        if item.startswith("[") and "]x" in item:
            inner, n = item[1:].rsplit("]x", 1)
            toks += inner.split() * int(n)
        else:
            toks += item.split()
    t, out = 0.0, []
    for tok in toks:
        if "/" not in tok:
            continue
        d = float(tok.split("/")[1].split("b")[0])
        if not tok.startswith("R"):
            out.append(round(t, 4))
        t += d
    return out


class Fixture:
    def __init__(self, repeat=True, marks=False):
        self.dir = tempfile.mkdtemp(prefix="maptime-")
        cache = os.path.join(self.dir, "cache")
        os.makedirs(cache)
        dump({"tracks": [{"name": "voice"}]}, f"{cache}/songsterr-meta.json")
        rest = {"voices": [{"beats": [{"duration": [1, 1], "rest": True}]}]}
        measures = [{"signature": [4, 4], **rest} for _ in range(8)]
        if marks:   # the tab's own repeat signs over measures 3-4
            measures[2]["repeatStart"] = True
            measures[3]["repeat"] = 2
        dump({"name": "voice", "measures": measures, "automations": {"tempo": [{"measure": 0, "bpm": BPM}]}},
             f"{cache}/songsterr-0.json")
        self.cache = cache
        self.map = {"cache": cache, "offset": OFFSET, "name": "fixture",
                    "parts": [{"name": "vox", "patch": "voice", "score_file": os.path.join(self.dir, "vox.txt")}]}
        if repeat:
            self.map["repeat"] = [[3, 4, 1]]
        self.map_path = os.path.join(self.dir, "map.json")
        dump(self.map, self.map_path)
        self.perf = T2S.performed_timeline(cache, self.map)
        starts = {p["label"]: p["start"] for p in self.perf}
        self.times = [starts[lb] + beat * 60 / BPM for lb, beat in (BURSTS if repeat else [])]
        # the stem: a quiet floor and a 0.3 s vocal-band burst (tone + noise) at each time
        n = int((self.perf[-1]["start"] + 2.5) * SR)
        rng = np.random.default_rng(7)
        x = rng.normal(0, 1e-4, n)
        k = int(0.3 * SR)
        env = np.minimum(1, np.minimum(np.arange(k), np.arange(k)[::-1]) / (0.01 * SR))
        for t in self.times:
            i = int(t * SR)
            burst = 0.5 * np.sin(2 * np.pi * 800 * np.arange(k) / SR) + 0.1 * rng.normal(0, 1, k)
            x[i:i + k] += burst * env
        pcm = (np.clip(np.repeat(x[:, None], 2, 1), -1, 1) * 32767).astype("<i2")
        self.stem = os.path.join(self.dir, "vocals.wav")
        with wave.open(self.stem, "wb") as w:
            w.setnchannels(2)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes(pcm.tobytes())


class MapTime(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)   # the tools' own quick open()s

    def fixture(self, **kw):
        f = Fixture(**kw)
        self.addCleanup(shutil.rmtree, f.dir, True)   # synthetic audio does not outlive the test
        return f

    def test_performed_timeline_expands_the_repeat(self):
        f = self.fixture()
        self.assertEqual([p["label"] for p in f.perf], PERFORMED)
        starts = {p["label"]: p["start"] for p in f.perf}
        self.assertAlmostEqual(starts["3.2"], OFFSET + 4 * 2.0)
        # after the repeat: two more bars than the tab's own clock (the bug: 4 s early here)
        self.assertAlmostEqual(starts["5"], OFFSET + 6 * 2.0)
        self.assertEqual([p["occ"] for p in f.perf if p["m"] == 3], [1, 2])

    def test_stemvox_and_tab2song_keep_every_burst_at_its_performed_time(self):
        f = self.fixture()
        r = tool(os.path.join(TOOLS, "stemvox.py"), f.stem, "--map", f.map_path, "--bars", "1-8")
        self.assertEqual(r.returncode, 0, r.stderr)
        labels = [ln.split()[1] for ln in r.stdout.splitlines() if ln.startswith("bar")]
        self.assertEqual(sorted(labels), sorted(PERFORMED), r.stdout)
        with open(os.path.join(f.dir, "vox.txt"), "w") as out:
            out.write(r.stdout)
        song = T2S.build(f.map)
        got = score_onsets(song["tracks"][0]["score"])
        want = [t * BPM / 60 for t in f.times]   # beats from the song start (the offset is in the score)
        self.assertEqual(len(got), len(want), f"onsets {got} vs {want}\n{r.stdout}")
        for g, w in zip(got, want):
            self.assertLessEqual(abs(g - w), 0.25, f"onsets {got} vs {want}")

    def test_score_files_take_each_pass_or_every_pass(self):
        f = self.fixture()
        with open(os.path.join(f.dir, "vox.txt"), "w") as out:
            out.write("bar 3  C4/4b\nbar 3.2  D4/4b\nbar 4  E4/4b\nbar 7.2  F4/4b\n")
        r = subprocess.run([sys.executable, "-c", f"""
import importlib.util, json, sys
spec = importlib.util.spec_from_file_location('t', {os.path.join(TOOLS, 'tab2song.py')!r})
t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
print(t.build(json.load(open({f.map_path!r})))['tracks'][0]['score'])"""], capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(r.returncode, 0, r.stderr)
        bars = r.stdout.strip().split(" | ")
        # lead-in + bars 1-2 rest, then 3.1 C4, 4.1 E4, 3.2 D4, 4.2 E4
        self.assertEqual(bars[1:5], ["C4/4b", "E4/4b", "D4/4b", "E4/4b"], r.stdout)
        self.assertIn("does not play bar(s) 7.2", r.stderr)

    def test_without_repeats_bars_stay_plain(self):
        f = self.fixture(repeat=False)
        self.assertEqual([p["label"] for p in f.perf], [str(m) for m in range(1, 9)])
        r = tool(os.path.join(TOOLS, "stemvox.py"), f.stem, "--map", f.map_path, "--bars", "2-5")
        self.assertEqual([ln.split()[1] for ln in r.stdout.splitlines()], ["2", "3", "4", "5"], r.stderr)

    def test_stemnotes_labels_each_pass(self):
        f = self.fixture()
        r = tool(os.path.join(TOOLS, "stemnotes.py"), f.stem, "--map", f.map_path, "2", "5")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual([ln.split()[1] for ln in r.stdout.splitlines()], ["2", "3.1", "4.1", "3.2", "4.2", "5"])

    def test_a_tab_with_repeat_signs_is_refused_without_a_map(self):
        f = self.fixture(repeat=False, marks=True)
        r = tool(os.path.join(TOOLS, "stemvox.py"), f.stem, "--tab", f.cache, "--bars", "1-5")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("repeat signs at measure(s) 3, 4", r.stderr)
        r = tool(os.path.join(TOOLS, "stemvox.py"), f.stem, "--tab", f.cache, "--bars", "1-5", "--ignore-repeats")
        self.assertEqual(r.returncode, 0, r.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
