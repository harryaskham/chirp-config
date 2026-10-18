#!/usr/bin/env python3
"""Tab voices (bd-72f61a): a staff's independent voices — here a drum staff with cymbals in voice 0 and kick/snare
in voice 1, as in The Woven Web — are read one at a time. The default stays voice 0 (byte-identical to before);
voice 1 has its own kicks, snares and triplets; a bar without the chosen voice rests for its meter's length (6/4,
7/4, 8/4, 9/8, 7/8, 4/4, 3/4 and an inherited 3/4), never falling back to another voice; tab2song chooses per part.

  python3 tools/tests/test_voice.py              (from ~/.config/chirp; under a second)
"""
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import songsterr as S  # noqa: E402

SIGS = [(6, 4), (7, 4), (8, 4), (9, 8), (7, 8), (4, 4), (3, 4), None]   # None: inherits 3/4
BAR = [4 * n / d for n, d in (s or (3, 4) for s in SIGS)]


def hit(*gm, dur=(1, 8), tuplet=None):
    b = {"duration": list(dur), "notes": [{"fret": g, "string": 0} for g in gm]}
    if tuplet:
        b["tuplet"] = tuplet
    return b


def rides(beats):
    return [hit(51) for _ in range(int(round(beats / 0.5)))]


TRIPLET = [hit(36, tuplet=3)] * 3              # three eighth-note triplets: one beat
REDUCED = [hit(36, dur=(1, 12))] * 3           # the same, stored already reduced
K, SN = hit(36, dur=(1, 4)), hit(38, dur=(1, 4))
VOICE1 = {
    0: [K, SN] * 3,                                   # 6/4: 3 kicks, 3 snares
    1: TRIPLET + [SN, K] * 3,                         # 7/4: 6 kicks, 3 snares, a triplet
    3: [hit(36), hit(36), hit(38)] * 3,               # 9/8: 6 kicks, 3 snares
    4: [hit(36), hit(38)] * 3 + [hit(36)],            # 7/8: 4 kicks, 3 snares
    6: REDUCED + [SN, SN],                            # 3/4: 3 kicks, 2 snares, a reduced triplet
}                                                     # bars 3, 6 and 8 (indices 2, 5, 7) have no voice 1
KICKS, SNARES = 22, 14


def measures():
    out = []
    for i, sig in enumerate(SIGS):
        v0 = rides(BAR[i])
        if i == 5:
            v0[0] = hit(36, 51)                       # voice 0 has a stray kick too (the real tab has a few)
        m = {"voices": [{"beats": v0}] + ([{"beats": VOICE1[i]}] if i in VOICE1 else [])}
        if sig:
            m["signature"] = list(sig)
        out.append(m)
    return out


def pieces(line, name):
    return sum(tok.split("/")[0].split(",").count(name) for tok in line.split() if "/" in tok)


def beats(line):
    return sum(float(x) for x in re.findall(r"/([0-9]*\.?[0-9]+)b", line))


class Voices(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="voice-")
        self.addCleanup(shutil.rmtree, self.dir, True)
        self.cache = os.path.join(self.dir, "cache")
        os.makedirs(self.cache)
        with open(f"{self.cache}/songsterr-meta.json", "w") as f:
            json.dump({"tracks": [{"name": "drums"}]}, f)
        with open(f"{self.cache}/songsterr-0.json", "w") as f:
            json.dump({"name": "drums", "measures": measures(), "automations": {"tempo": [{"measure": 0, "bpm": 120}]}}, f)

    def test_the_default_is_voice_0(self):
        name, drums, lines = S.score(self.cache, 0)
        self.assertTrue(drums)
        self.assertEqual(lines, S.score(self.cache, 0, voice=0)[2])
        self.assertEqual(sum(pieces(ln, "k") for ln in lines), 1, "only voice 0's stray kick")
        self.assertEqual(sum(pieces(ln, "rd") for ln in lines), sum(int(round(b / 0.5)) for b in BAR))

    def test_voice_1_has_its_own_kicks_snares_and_triplets(self):
        lines = S.score(self.cache, 0, voice=1)[2]
        self.assertEqual(sum(pieces(ln, "k") for ln in lines), KICKS)
        self.assertEqual(sum(pieces(ln, "s") for ln in lines), SNARES)
        self.assertEqual(sum(pieces(ln, "rd") for ln in lines), 0, "voices are never merged")
        self.assertIn("k/0.3333b", lines[1], "a triplet eighth is a third of a beat")
        self.assertIn("k/0.3333b", lines[6], "so is one stored already reduced")

    def test_every_bar_keeps_its_meter(self):
        for voice in (0, 1):
            for i, line in enumerate(S.score(self.cache, 0, voice=voice)[2]):
                self.assertAlmostEqual(beats(line), BAR[i], delta=1e-3, msg=f"voice {voice} bar {i + 1}: {line}")

    def test_a_bar_without_the_voice_rests_for_its_length(self):
        lines = S.score(self.cache, 0, voice=1)[2]
        self.assertEqual([lines[i] for i in (2, 5, 7)], ["R/8b", "R/4b", "R/3b"])   # 8/4, 4/4, inherited 3/4
        self.assertEqual(S.score(self.cache, 0, voice=5)[2], [f"R{S.fmt_len(b)}" for b in BAR])

    def test_tab2song_chooses_per_part(self):
        spec = importlib.util.spec_from_file_location("tab2song_v", os.path.join(TOOLS, "tab2song.py"))
        T = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(T)
        mp = {"cache": self.cache, "offset": 0.0, "parts": [
            {"name": "cymbals", "track": 0, "patch": "kit", "bars": [[1, 8]]},
            {"name": "kick", "track": 0, "patch": "kit", "bars": [[1, 8]], "voice": 1}]}
        by = {t["name"]: t["score"] for t in T.build(mp)["tracks"]}
        self.assertEqual(pieces(by["kick"], "k"), KICKS)
        self.assertEqual(pieces(by["cymbals"], "k"), 1)
        bars = [b.strip() for b in by["kick"].split("|")]
        self.assertEqual(len(bars), 7, "bar by bar (tab2song drops a part's trailing rest bar)")
        for i, bar in enumerate(bars):
            self.assertAlmostEqual(beats(bar), BAR[i], delta=1e-3, msg=f"bar {i + 1}: {bar}")
        self.assertEqual((bars[2], bars[5]), ("R/8b", "R/4b"), "bars without the voice rest in place")

    def test_the_cli_reads_a_voice(self):
        r = subprocess.run([sys.executable, os.path.join(TOOLS, "songsterr.py"), "--cached", self.cache, "0", "--voice", "1"],
                           capture_output=True, text=True, stdin=subprocess.DEVNULL)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("voice 1", r.stdout.splitlines()[0])
        self.assertEqual(sum(pieces(ln.split(None, 1)[1], "k") for ln in r.stdout.splitlines()[1:] if " " in ln), KICKS)


if __name__ == "__main__":
    unittest.main(verbosity=2)
