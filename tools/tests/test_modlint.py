#!/usr/bin/env python3
"""modlint.lint: implausible mod amounts (Hz written where octaves are meant, linear where dB is meant).

  python3 tools/tests/test_modlint.py      (from ~/.config/chirp; instant)
"""
import os
import sys
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import modlint as M  # noqa: E402


class Lint(unittest.TestCase):
    def test_hz_amount_on_a_cutoff_is_flagged(self):
        song = {"tracks": [{"filters": [{"kind": "lp", "cutoff": {"value": 3000, "mod": [{"src": "auto.cl", "amount": -2600}]}}]}]}
        self.assertEqual(M.lint(song), [("tracks.0.filters.0.cutoff", "freq", "auto.cl", -2600)])

    def test_octave_amounts_and_full_sweeps_pass(self):
        song = {"fx": [{"cutoff": {"value": 800, "mod": [{"src": "lfo.a", "amount": 2}, {"src": "env.f", "amount": -3}]}},
                       {"cutoff": {"value": 20, "mod": [{"src": "env.sfz", "amount": 11}]}},      # a library sweep
                       {"freq": {"value": 1000, "mod": [{"src": "lfo.b", "amount": 6.5}]}}]}
        self.assertEqual(M.lint(song), [])

    def test_gains_and_other_params_ignored(self):
        song = {"level": {"value": 1, "mod": [{"src": "env.ring", "amount": 90}]},       # the envelope-fade idiom
                "pan": {"value": 0, "mod": [{"src": "lfo.p", "amount": 500}]}}
        self.assertEqual(M.lint(song), [])

    def test_threshold_is_settable(self):
        song = {"cutoff": {"value": 800, "mod": [{"src": "lfo.a", "amount": 10}]}}
        self.assertEqual(M.lint(song), [])
        self.assertEqual(len(M.lint(song, octaves=8)), 1)


def _song(lane, bass, extra=None):
    """A bass on a bus whose eq follows a `key` lane a semitone a unit. lane: [(beat, value)] steps; bass: [(bar, pitch)]."""
    points = []
    for i, (at, v) in enumerate(lane):
        end = lane[i + 1][0] - 0.02 if i + 1 < len(lane) else at + 16
        points += [[f"{at}b", v], [f"{end}b", v]]
    band = {"kind": "peak", "cutoff": {"value": 44, "mod": [{"src": "auto.key", "amount": 0.08333}]}, "gain": "-7dB"}
    return {"tempo": 120, "buses": {"low": {"auto": {"key": {"curve": 0, "points": points}}, "fx": [{"type": "eq", "bands": [band]}]}},
            "tracks": [{"name": "bass", "out": "low",
                        "notes": [{"at": 4 * b + i, "len": 1, "pitch": p} for b, p in bass for i in range(4)]},
                       {"name": "kick", "out": "drums", "notes": [{"at": 0, "len": 1, "pitch": "k"}]}] + (extra or [])}


class KeyLanes(unittest.TestCase):
    def test_a_lane_that_goes_the_long_way_round(self):
        bass = [(b, "F1") for b in range(4)] + [(b, "Eb1") for b in range(4, 8)] + [(b, "C1") for b in range(8, 12)]
        read, moves = M.key_moves(_song([(0, 0), (16, 10), (32, 7)], bass))            # F -> E flat: the lane UP ten, the notes DOWN two
        self.assertEqual(read, 1)
        self.assertEqual([(m["at"], m["bar"], m["lane_move"], m["note_move"], m["from"], m["to"], m["kind"]) for m in moves],
                         [(16.0, 5, 10.0, -2, "F1", "Eb1", "long")])                   # E flat -> C: -3 and -3, as it should be
        self.assertEqual((moves[0]["where"], moves[0]["lane"], moves[0]["tracks"]), ("buses.low", "key", ["bass"]))
        read, moves = M.key_moves(_song([(0, 0), (16, -2), (32, -5)], bass))            # wrapped: nothing to say
        self.assertEqual((read, moves), (1, []))

    def test_a_lane_that_does_not_follow_and_a_melody_that_does(self):
        bass = [(b, "F1") for b in range(4)] + [(b, "Bb1") for b in range(4, 8)]
        _, moves = M.key_moves(_song([(0, 0), (16, 3)], bass))                         # the lane says +3, the notes went +5
        self.assertEqual([(m["lane_move"], m["note_move"], m["kind"]) for m in moves], [(3.0, 5, "other")])
        tune = {"name": "bell", "fx": [{"cutoff": {"value": 900, "mod": [{"src": "auto.key", "amount": -0.08333}]}}],
                "auto": {"key": {"points": [["0b", 0], ["15.98b", 0], ["16b", 3], ["32b", 3]]}},
                "notes": [{"at": i, "len": 1, "pitch": p} for i, p in enumerate(["C5", "E5", "G5", "C5", "E5", "G5", "E5", "C5"] * 2)]
                + [{"at": 16 + i, "len": 1, "pitch": p} for i, p in enumerate(["G5", "Bb5", "Eb5", "G5", "Bb5", "Eb5", "G5", "Bb5"] * 2)]}
        read, moves = M.key_moves(_song([(0, 0)], [(0, "F1")], [tune]))                # its notes moved +3 (C E G -> Eb G Bb); its
        self.assertEqual((read, moves), (2, []))                                       # lowest note moved +3 too here: C5 -> Eb5
        tune["notes"][16:] = [{"at": 16 + i, "len": 1, "pitch": p} for i, p in enumerate(["G5", "Bb5", "Eb6"] * 5)]
        read, moves = M.key_moves(_song([(0, 0)], [(0, "F1")], [tune]))                # lowest note C5 -> G5 (+7), the notes +3 by
        self.assertEqual(moves, [])                                                    # pitch class: a melody, not listed

    def test_what_makes_a_key_lane_and_where_it_holds(self):
        fx = [{"cutoff": {"value": 44, "mod": [{"src": "auto.key", "amount": 0.08333}, {"src": "lfo.a", "amount": 0.0833}]}},
              {"freq": {"value": 900, "mod": [{"src": "auto.sweep", "amount": 2}]}},
              {"gain": {"mod": [{"src": "auto.g", "amount": 0.0833}]}}]
        self.assertEqual(M.semitone_lanes(fx), {"key"})                                # a semitone a unit, from a lane, on a frequency
        self.assertEqual(M.held([["0b", 0], ["15.98b", 0], ["16b", 3], ["20b", 5], ["24b", 5]], 120),
                         [(0.0, 15.98, 0.0), (20.0, float("inf"), 5.0)])               # the 3 is one point: a ramp passes through it
        self.assertEqual(M.moved_by({41: 8}, {39: 8}), {10})
        self.assertEqual(M.moved_by({60: 4, 62: 4, 64: 4, 66: 4, 68: 4, 70: 4}, {62: 4, 64: 4, 66: 4, 68: 4, 70: 4, 72: 4}),
                         {0, 2, 4, 6, 8, 10})                                          # a whole-tone scale maps onto itself
        self.assertEqual(M.moved_by({}, {41: 1}), set())
        song = _song([(0, 0), (16, 10)], [(b, "F1") for b in range(4)] + [(b, "Eb1") for b in range(4, 8)])
        song["tempo"] = [[0, 120], [16, 90]]                                           # a lane in beats is placed whatever the tempo
        self.assertEqual(len(M.key_moves(song)[1]), 1)
        self.assertEqual(M.key_moves({"tracks": []}), (0, []))

    def test_the_lines_are_questions_after_the_flags(self):
        import contextlib
        import io
        import json
        import stat
        import tempfile
        root = tempfile.mkdtemp(prefix="modlint-test-")
        self.addCleanup(__import__("shutil").rmtree, root, True)
        pin = os.path.join(root, "fake-chirp")
        with open(pin, "w") as f:
            f.write("#!/usr/bin/env python3\nimport json, sys\na = sys.argv\n"
                    "print(json.dumps({'data': {'canonical': json.load(open(a[a.index('-f') + 1]))}}))\n")
        os.chmod(pin, os.stat(pin).st_mode | stat.S_IXUSR)
        bass = [(b, "F1" if (b // 2) % 2 == 0 else "Eb1") for b in range(32)]          # F, E flat, F, E flat ... every two bars
        lane = [(8 * i, 0 if i % 2 == 0 else 10) for i in range(16)]
        song = os.path.join(root, "fall.yaml")
        with open(song, "w") as f:
            json.dump(_song(lane, bass), f)

        def run(*argv):
            out = io.StringIO()
            with contextlib.redirect_stdout(out), self.assertRaises(SystemExit) as e:
                M.main([song, "--pin", pin, *argv])
            return e.exception.code, out.getvalue()
        code, text = run()
        lines = text.splitlines()
        self.assertEqual(code, 0)                                                      # questions do not fail the lint
        self.assertEqual(lines[0], "modlint: 1 song(s), 0 flag(s)")                    # the line that was always there, first
        self.assertEqual(sum("THE LONG WAY ROUND" in ln for ln in lines), 6)           # the first six, then
        self.assertTrue(lines[-2].endswith("buses.low lane key: and 9 more"))
        self.assertEqual(lines[-1], "modlint: 1 key lane(s) read against their parts' lowest notes: 15 move(s) the long way round, "
                                    "0 that do not follow (questions, not flags)")
        self.assertIn("at 8b (bar 3) the lane moves +10 and the part's lowest note -2 (F1 -> Eb1)", lines[1])
        code, text = run("--json")
        got = json.loads(text)
        self.assertEqual((code, got["key_lanes"], len(list(got["key_moves"].values())[0]), got["flagged"]), (0, 1, 15, {}))


if __name__ == "__main__":
    unittest.main()
