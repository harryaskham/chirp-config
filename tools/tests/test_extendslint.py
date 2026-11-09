#!/usr/bin/env python3
"""extendslint: an `extends` override's `mod` list replaces the base's, so routes it does not copy are lost
(chirper-three's t8 v82, 9 Nov).

  python3 tools/tests/test_extendslint.py      (from ~/.config/chirp; instant, no chirp binary)
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import extendslint as X  # noqa: E402

VIB = {"src": "lfo.vib", "amount": 0.2}
TW = {"src": "env.tw", "amount": 0.22}
BASES = {"strings": {"synth": {"pitch": {"value": 0, "mod": [VIB, TW]}, "lfo": {"vib": {"rate": 5}}}}}


def lint(song):
    return X.lint_song(song, lambda n: BASES.get(n))


class ExtendsLint(unittest.TestCase):
    def test_an_override_that_drops_routes_is_named(self):
        song = {"tracks": [{"name": "violins", "patch": {"extends": "strings",
                                                         "synth": {"pitch": {"mod": [{"src": "lfo.b", "amount": 1}]}}}}]}
        f = lint(song)
        self.assertEqual([(x["where"], x["extends"], x["path"], [r["src"] for r in x["lost"]]) for x in f],
                         [("violins", "strings", "synth.pitch.mod", ["lfo.vib", "env.tw"])])

    def test_copying_the_whole_list_and_adding_is_clean(self):
        song = {"tracks": [{"name": "v", "patch": {"extends": "strings",
                                                   "synth": {"pitch": {"mod": [VIB, TW, {"src": "lfo.b", "amount": 1}]}}}}]}
        self.assertEqual(lint(song), [])

    def test_amounts_may_change(self):
        song = {"tracks": [{"name": "v", "patch": {"extends": "strings",
                                                   "synth": {"pitch": {"mod": [{"src": "lfo.vib", "amount": 0.3}, TW]}}}}]}
        self.assertEqual(lint(song), [])

    def test_overrides_without_a_mod_list_are_clean(self):
        song = {"tracks": [{"name": "v", "patch": {"extends": "strings", "synth": {"lfo": {"vib": {"bloom": 0.5}}}}}]}
        self.assertEqual(lint(song), [])

    def test_a_song_local_base_is_used_first(self):
        song = {"patches": {"mine": {"synth": {"pitch": {"mod": [TW]}}},
                            "mine2": {"extends": "mine", "synth": {"pitch": {"mod": []}}}}}
        f = lint(song)
        self.assertEqual([(x["where"], x["extends"], [r["src"] for r in x["lost"]]) for x in f],
                         [("song.patches", "mine", ["env.tw"])])

    def test_unknown_bases_are_skipped(self):
        self.assertEqual(lint({"tracks": [{"name": "v", "patch": {"extends": "nope", "synth": {"pitch": {"mod": []}}}}]}), [])


if __name__ == "__main__":
    unittest.main()
