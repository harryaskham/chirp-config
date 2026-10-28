#!/usr/bin/env python3
"""tools/rngsafe.py: the replacement map keeps only PARTS (renamed <part>r, bars A..B, extra subst) and the splice
mutes the originals over the span, appends the replacements LAST and copies their sound settings.

  python3 tools/tests/test_rngsafe.py      (from ~/.config/chirp; instant)
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import rngsafe as R  # noqa: E402


class Rngsafe(unittest.TestCase):
    def test_replacement_map(self):
        m = {"parts": [{"name": "gtr-l", "bars": [[1, 99]], "subst": [[1, 2, "C2", "D2"]]}, {"name": "bass", "bars": [[1, 99]]}]}
        mm = R.replacement_map(m, ["gtr-l"], 41, 46, [["Bb1", "F#1"]])
        self.assertEqual(len(mm["parts"]), 1)
        p = mm["parts"][0]
        self.assertEqual((p["name"], p["bars"]), ("gtr-lr", [[41, 46]]))
        self.assertEqual(p["subst"], [[1, 2, "C2", "D2"], [41, 46, "Bb1", "F#1"]])
        self.assertEqual(len(m["parts"]), 2)                       # the input map is untouched

    def test_splice_mutes_appends_last_and_copies_settings(self):
        gain = {"value": "-3dB", "mod": [{"src": "auto.envl", "amount": 1}]}
        cur = {"tracks": [{"name": "gtr-l", "patch": "m8-emg-l", "pan": -1, "gain": gain, "fx": ["eq"],
                           "auto": {"envl": {"points": [["0s", 0], ["5s", -6]]}}},
                          {"name": "bass", "patch": "bass-fat"}]}
        rep = {"tracks": [{"name": "gtr-lr", "patch": "x", "score": "F1/4"}]}
        d = R.splice(cur, rep, ["gtr-l"], 10.0, 20.0)
        self.assertEqual([t["name"] for t in d["tracks"]], ["gtr-l", "bass", "gtr-lr"])
        g = d["tracks"][0]
        self.assertEqual(g["auto"]["mx"]["points"][2], ["10.000s", -60])
        self.assertEqual(g["fx"][-1]["gain"]["mod"][0]["src"], "auto.mx")
        n = d["tracks"][2]
        self.assertEqual((n["patch"], n["pan"], n["gain"], n["fx"], n["score"]), ("m8-emg-l", -1, gain, ["eq"], "F1/4"))
        # the replacement keeps the source's own lanes (its gain mod reads auto.envl) but not the mute lane (9c6183ad)
        self.assertEqual(sorted(n["auto"]), ["envl"])
        self.assertNotIn("mx", cur["tracks"][0].get("auto", {}))   # the input song is untouched


if __name__ == "__main__":
    unittest.main()
