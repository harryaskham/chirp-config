#!/usr/bin/env python3
"""splitpart: one time range of a track onto a second patch, proven note-identical (chirper-zero's request).

  python3 tools/tests/test_splitpart.py      (from ~/.config/chirp; a few seconds: the proofs run chirp plan)
"""
import json
import os
import shutil
import sys
import tempfile
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import chirpbin  # noqa: E402
import splitpart as S  # noqa: E402

HAVE_CHIRP = os.path.exists(chirpbin.resolve("chirp"))


class Units(unittest.TestCase):
    def test_score_split_moves_notes_starting_in_range_with_their_holds(self):
        keep, move, n = S.split_score("C4/1b@90 _/1b | R/1b E4/1b@80 _/0.5b | G4/2b", 2, 4)
        self.assertEqual(keep, "C4/1b@90 _/1b | R/1b R/1b R/0.5b | G4/2b")
        self.assertEqual(move, "R/1b R/1b | R/1b E4/1b@80 _/0.5b | R/2b")
        self.assertEqual(n, 1)

    def test_unsupported_score_tokens_are_refused(self):
        for score in ("C4 D4", "C4/300ms", "(C4 D4)x2/1b"):
            with self.assertRaises(S.Refused, msg=score):
                S.split_score(score, 0, 1)

    def test_tempo_maps_convert_seconds_to_beats(self):
        segs = S.tempo_segments([{"at": "0b", "bpm": 60}, {"at": "4b", "bpm": 120, "meter": "4/4"}])
        self.assertAlmostEqual(S.to_beats("2s", segs), 2.0)
        self.assertAlmostEqual(S.to_beats(5, segs), 6.0)      # 4 beats in 4 s, then 2 beats per second
        self.assertAlmostEqual(S.to_beats("7b", segs), 7.0)
        with self.assertRaises(S.Refused):
            S.tempo_segments([{"at": "0b", "bpm": 60, "ramp": True}])

    def test_notes_split_by_onset_and_track_copy(self):
        doc = {"tempo": 120, "tracks": [{"name": "a", "patch": "p", "gain": "-3dB",
                                         "notes": [{"at": "0.5s", "pitch": 60}, {"at": "2b", "pitch": 62}, {"at": "3s", "pitch": 64}]}]}
        out, n = S.split(doc, "a", "1s", "2s", "q", "b")
        self.assertEqual(n, 1)
        a, b = out["tracks"]
        self.assertEqual([x["pitch"] for x in a["notes"]], [60, 64])
        self.assertEqual(b, {"name": "b", "patch": "q", "gain": "-3dB", "notes": [{"at": "2b", "pitch": 62}]})
        self.assertEqual(len(doc["tracks"][0]["notes"]), 3, "the input is not modified")

    def test_refusals(self):
        doc = {"tempo": 120, "tracks": [{"name": "a", "patch": "p", "score": "C4/1b"}, {"name": "b", "patch": "p", "score": "D4/1b"}]}
        for args in (("x", "0b", "1b", "q", "n"), ("a", "0b", "1b", "q", "b"), ("a", "2b", "3b", "q", "n"), ("a", "1b", "1b", "q", "n")):
            with self.assertRaises(S.Refused, msg=args):
                S.split(doc, *args)


@unittest.skipUnless(HAVE_CHIRP, "needs the groove pin")
class Proof(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="splitpart-test-")
        self.addCleanup(shutil.rmtree, self.dir, True)

    def song(self, score):
        p = os.path.join(self.dir, "song.json")
        with open(p, "w") as f:
            json.dump({"tempo": 120, "tracks": [{"name": "lead", "patch": "piano", "score": score},
                                                {"name": "bass", "patch": "bass", "score": "C2/4b"}]}, f, indent=2)
        return p

    def test_a_clean_split_is_written_with_the_new_patch(self):
        src, out = self.song("C4/1b@90 D4/1b@90 E4/1b@90 F4/1b@90"), os.path.join(self.dir, "out.json")
        S.main([src, "lead", "--from", "1b", "--to", "3b", "--patch", "bell", "-o", out])
        d = json.load(open(out))
        self.assertEqual([(t["name"], t["patch"], t["score"]) for t in d["tracks"]],
                         [("lead", "piano", "C4/1b@90 R/1b R/1b F4/1b@90"), ("lead-alt", "bell", "R/1b D4/1b@90 E4/1b@90 R/1b"),
                          ("bass", "bass", "C2/4b")])

    def test_a_split_that_would_change_a_latched_octave_is_refused(self):
        src, out = self.song("C5/1b@90 D/1b@90"), os.path.join(self.dir, "out.json")   # D is D5 by latching
        with self.assertRaises(SystemExit) as e:
            S.main([src, "lead", "--from", "1b", "--to", "2b", "--patch", "bell", "-o", out])
        self.assertIn("changes the voices", str(e.exception))
        self.assertFalse(os.path.exists(out))
        self.assertEqual([f for f in os.listdir(self.dir) if f.startswith(".splitpart-")], [])


if __name__ == "__main__":
    unittest.main()
