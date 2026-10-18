#!/usr/bin/env python3
"""A tab's own repeat signs and alternate endings (bd-11abdc): opt-in `"tab_repeats": true` plays them by Guitar Pro's
rules — a plain repeat, first/second endings, endings 1-3 then 4 (the closing measure three times, the fourth ending
once: The Model's 114 bars, not a naive 116) and a close without a start sign; nested repeats, endings outside a
repeat and endings that never play are errors; every staff, the bar clock and score_file pass labels follow the same
order; without the option every map is unchanged, and it cannot be combined with explicit `repeat` entries.

  python3 tools/tests/test_tabrepeats.py         (from ~/.config/chirp; under a second)
"""
import importlib.util
import io
import json
import os
import re
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(TOOLS)
spec = importlib.util.spec_from_file_location("tab2song_rep", os.path.join(TOOLS, "tab2song.py"))
T = importlib.util.module_from_spec(spec)
spec.loader.exec_module(T)


def tab(n, marks):
    ms = [{} for _ in range(n)]
    for k, v in marks.items():
        ms[k - 1].update(v)
    return ms


def plays(n, marks):
    return [i + 1 for i in T.tab_play_order(tab(n, marks))]


# The Model's structure, scaled down: 1-2 repeat x2; 5-7 x4 with 7 = endings 1-3 and 8 = ending 4; 10-11 x2 with 11 =
# ending 1 and 12 = ending 2
MODEL = {1: {"repeatStart": True}, 2: {"repeat": 2},
         5: {"repeatStart": True}, 7: {"alternateEnding": [1, 2, 3], "repeat": 4}, 8: {"alternateEnding": [4]},
         10: {"repeatStart": True}, 11: {"alternateEnding": [1], "repeat": 2}, 12: {"alternateEnding": [2]}}
MODEL_ORDER = [1, 2, 1, 2, 3, 4, 5, 6, 7, 5, 6, 7, 5, 6, 7, 5, 6, 8, 9, 10, 11, 10, 12, 13]


class Order(unittest.TestCase):
    def test_plain_repeat(self):
        self.assertEqual(plays(6, {1: {"repeatStart": True}, 4: {"repeat": 2}}), [1, 2, 3, 4, 1, 2, 3, 4, 5, 6])
        self.assertEqual(plays(3, {2: {"repeatStart": True}, 3: {"repeat": 3}}), [1, 2, 3, 2, 3, 2, 3])

    def test_first_and_second_endings(self):
        self.assertEqual(plays(7, {2: {"repeatStart": True}, 4: {"alternateEnding": [1], "repeat": 2}, 5: {"alternateEnding": [2]}}),
                         [1, 2, 3, 4, 2, 3, 5, 6, 7])

    def test_endings_one_to_three_then_four(self):
        self.assertEqual(plays(8, {3: {"repeatStart": True}, 5: {"alternateEnding": [1, 2, 3], "repeat": 4},
                                   6: {"alternateEnding": [4]}}),
                         [1, 2, 3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 6, 7, 8])

    def test_a_close_without_a_start_repeats_from_the_last_section(self):
        self.assertEqual(plays(5, {2: {"repeat": 2}}), [1, 2, 1, 2, 3, 4, 5])
        self.assertEqual(plays(6, {1: {"repeatStart": True}, 2: {"repeat": 2}, 4: {"repeat": 2}}),
                         [1, 2, 1, 2, 3, 4, 3, 4, 5, 6])

    def test_the_whole_model_structure(self):
        self.assertEqual(plays(13, MODEL), MODEL_ORDER)

    def test_malformed_tabs_are_errors(self):
        for bad, why in (({1: {"repeatStart": True}, 2: {"repeatStart": True}, 3: {"repeat": 2}}, "nested"),
                         ({3: {"alternateEnding": [1]}}, "outside a repeat"),
                         ({1: {"repeatStart": True}, 2: {"alternateEnding": [1], "repeat": 2}, 3: {"alternateEnding": [3]}},
                          "never play")):
            with self.assertRaisesRegex(ValueError, why):
                T.tab_play_order(tab(5, bad))


class Maps(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="tabrepeats-")
        self.addCleanup(shutil.rmtree, self.dir, True)
        self.cache = os.path.join(self.dir, "cache")
        os.makedirs(self.cache)
        ms = tab(13, MODEL)
        with open(f"{self.cache}/songsterr-meta.json", "w") as f:
            json.dump({"tracks": [{"name": "gtr"}, {"name": "bass"}]}, f)
        for k, (name, low) in enumerate((("gtr", 52), ("bass", 40))):
            tr = {"name": name, "tuning": [low + 5 * s for s in range(4)], "automations": {"tempo": [{"measure": 0, "bpm": 120}]},
                  "measures": [dict(m, signature=[4, 4], voices=[{"beats": [{"duration": [1, 1], "notes": [{"string": 0, "fret": i}]}]}])
                               for i, m in enumerate(ms)]}
            with open(f"{self.cache}/songsterr-{k}.json", "w") as f:
                json.dump(tr, f)

    def mp(self, **kw):
        return {"cache": self.cache, "offset": 0.0, "parts": [
            {"name": "gtr", "track": 0, "patch": "x", "bars": [[1, 13]]},
            {"name": "bass", "track": 1, "patch": "x", "bars": [[1, 13]]}], **kw}

    def test_off_is_the_written_order(self):
        pt = T.performed_timeline(self.cache, self.mp())
        self.assertEqual([p["m"] for p in pt], list(range(1, 14)))

    def test_on_plays_the_signs_with_pass_labels_and_clock(self):
        pt = T.performed_timeline(self.cache, self.mp(tab_repeats=True))
        self.assertEqual([p["m"] for p in pt], MODEL_ORDER)
        labels = [p["label"] for p in pt]
        self.assertEqual([lb for lb in labels if lb.split(".")[0] in ("7", "8")], ["7.1", "7.2", "7.3", "8"])
        self.assertEqual([lb for lb in labels if lb.split(".")[0] in ("11", "12")], ["11", "12"])
        self.assertEqual([p["start"] for p in pt], [2.0 * k for k in range(len(MODEL_ORDER))], "4/4 at 120: two seconds a bar")
        skipped = T.performed_timeline(self.cache, self.mp(tab_repeats=True, skip=[[9, 9]]))
        self.assertEqual([p["m"] for p in skipped], [m for m in MODEL_ORDER if m != 9])

    def test_every_staff_follows_and_score_files_take_passes(self):
        sf = os.path.join(self.dir, "lead.txt")
        with open(sf, "w") as f:
            f.write("bar 7.2  C5/4b\n")
        mp = self.mp(tab_repeats=True)
        mp["parts"].append({"name": "lead", "patch": "x", "score_file": sf})
        with redirect_stderr(io.StringIO()):
            song = T.build(mp)
        by = {t["name"]: t["score"] for t in song["tracks"]}
        for name in ("gtr", "bass"):
            notes = re.findall(r"[A-G][#b]?\d", by[name])
            self.assertEqual(len(notes), len(MODEL_ORDER), f"{name}: one written note per performed bar")
        self.assertEqual(by["lead"].count("C5"), 1, "only the second pass of bar 7")

    def test_explicit_repeats_and_tab_repeats_do_not_mix(self):
        with self.assertRaises(SystemExit), redirect_stderr(io.StringIO()):
            T.performed_timeline(self.cache, self.mp(tab_repeats=True, repeat=[[1, 2, 1]]))

    @unittest.skipUnless(os.path.isdir(os.path.join(ROOT, "ref/songsterr-10792")), "The Model's tab is not cached")
    def test_the_model_is_114_bars(self):
        cache = os.path.join(ROOT, "ref/songsterr-10792")
        self.assertEqual(len(T.performed_timeline(cache, {"cache": cache, "offset": 0.0, "tab_repeats": True})), 114)
        self.assertEqual(len(T.performed_timeline(cache, {"cache": cache, "offset": 0.0})), 96)


if __name__ == "__main__":
    unittest.main(verbosity=2)
