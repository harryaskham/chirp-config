#!/usr/bin/env python3
"""tools/eqcuts.py: a song's EQ cuts, the version each dates from, and what has stopped playing with it since.

Hermetic: plans are built here, and the stand-in engine prints the file it is given as that file's plan; the history
test makes its own small git repository.

  python3 tools/tests/test_eqcuts.py      (from ~/.config/chirp; a second or two)
"""
import contextlib
import io
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import eqcuts as E  # noqa: E402

ENGINE = '''#!/usr/bin/env python3
import json, sys
a = sys.argv[1:]
text = open(a[a.index("-f") + 1]).read()
if "BAD" in text:
    print(json.dumps({"status": "error", "error": "no"}))
    sys.exit(2)
print(json.dumps({"data": {"canonical": json.loads(text)}}))
'''


def notes(first, last, pitch="E2"):
    return [{"at": float(b), "len": 1.0, "pitch": pitch} for b in range(first, last)]


def song(tone_lane=0.0, tone_notes=True, hz=700, gain="-2.5dB", cut=True, extra=()):
    """Two guitars with one cut each over 32 beats, a tone under their first 16, a hat, a bass through a bus."""
    eq = [{"type": "eq", "bands": [{"kind": "peak", "cutoff": hz, "q": 1, "gain": gain}, {"kind": "hp", "cutoff": 30}]}] if cut else []
    tracks = [
        {"name": "gl", "patch": "rig fx.1.model=mark", "out": "gtrs", "fx": eq, "notes": notes(0, 32)},
        {"name": "gr", "patch": "rig fx.1.model=mark", "out": "gtrs", "fx": eq, "notes": notes(0, 32)},
        {"name": "tone", "patch": "sine", "notes": notes(0, 16, "F4") if tone_notes else [],
         "gain": {"value": "-19dB", "mod": [{"src": "auto.lvl", "amount": 1.0}]},
         "auto": {"lvl": {"points": [["0b", 5.0], ["3.99b", 5.0], ["4b", tone_lane], ["16b", tone_lane]]}}},
        {"name": "hat", "patch": "kit", "notes": [{"at": float(b), "len": 0.25, "pitch": "h"} for b in range(0, 32)]},
        {"name": "bass", "patch": "ct-bass", "out": "low", "notes": notes(0, 32, "E1")},
        *extra,
    ]
    return {"tempo": 120, "tracks": tracks,
            "buses": {"gtrs": {"fx": [{"type": "eq", "bands": [{"kind": "peak", "cutoff": 200, "q": 1.2, "gain": "-2dB"}]}]},
                      "low": {"fx": ["peak cutoff=350 q=1 gain=-8dB", "hp cutoff=30"], "out": "gtrs"}},
            "patches": {"ct-bass": {"fx": [{"type": "eq", "bands": [{"kind": "highshelf", "cutoff": 1500, "gain": "-10dB"},
                                                                     {"kind": "peak", "cutoff": 900, "gain": "5dB"}]}]},
                        "ct-bass.x": {"fx": [{"type": "eq", "bands": [{"kind": "peak", "cutoff": 100, "gain": "-9dB"}]}]}},
            "master": {"fx": [{"type": "eq", "bands": [{"kind": "hp", "cutoff": 24}]}, {"type": "gain", "gain": "2dB"}]}}


def versions(*songs):
    return [(f"v{i + 1}", E.digest(s)) for i, s in enumerate(songs)]


class Parts(unittest.TestCase):
    def test_what_a_cut_is(self):
        self.assertEqual(E.db("-2.5dB"), (-2.5, []))
        self.assertEqual(E.db({"value": 700, "mod": [{"src": "auto.veq", "amount": 1}]}), (700.0, ["auto.veq"]))
        self.assertEqual(E.db(None), (None, []))
        self.assertEqual(E.band("peak cutoff=350 q=1 gain=-8dB"), {"kind": "peak", "cutoff": "350", "q": "1", "gain": "-8dB"})
        moved = {"kind": "peak", "cutoff": {"value": 700, "mod": [{"src": "auto.veq"}]}, "gain": "-2.5dB"}
        got = E.fx_cuts([{"type": "eq", "bands": [moved,
                                                  {"kind": "peak", "cutoff": 900, "gain": "5dB"}, {"kind": "hp", "cutoff": 30},
                                                  {"cutoff": 250, "gain": -3}]},
                         "peak cutoff=350 q=1 gain=-8dB", "hp cutoff=30", {"type": "gain", "gain": "-6dB"}])
        self.assertEqual(got, [(0, 0, "peak", 700.0, None, -2.5, ["auto.veq"]), (0, 3, "peak", 250.0, None, -3.0, []),
                               (1, 0, "peak", 350.0, 1.0, -8.0, [])])           # a boost, a high-pass and a gain are not cuts

    def test_a_part_turned_down_by_a_lane_does_not_sound_there(self):
        d = E.digest(song(tone_lane=0.0))
        self.assertEqual(d["tracks"]["tone"]["beats"], [[0, 16]])
        self.assertEqual(d["tracks"]["tone"]["low"], 65)                            # F4
        self.assertIsNone(d["tracks"]["hat"]["low"])                               # a kit piece has no pitch
        d = E.digest(song(tone_lane=-60.0))                                        # the same notes, the lane to -60 dB from beat 4
        self.assertEqual(d["tracks"]["tone"]["beats"], [[0, 4]])
        self.assertEqual(d["tracks"]["gl"], {"out": "gtrs", "patch": "rig", "low": 40, "beats": [[0, 32]]})
        muted = song()
        muted["tracks"][2]["mute"] = True
        self.assertEqual(E.digest(muted)["tracks"]["tone"]["beats"], [])
        late = song()
        late["tracks"][2]["at"] = "8b"                                             # a track that starts late: its notes from there
        self.assertEqual(E.digest(late)["tracks"]["tone"]["beats"], [[8, 24]])
        self.assertEqual(sorted((c["on"], c["name"], c["hz"]) for c in d["cuts"]),
                         [("bus", "gtrs", 200.0), ("bus", "low", 350.0), ("patch", "ct-bass", 1500.0),
                          ("track", "gl", 700.0), ("track", "gr", 700.0)])         # not the piece ct-bass.x, not the master's hp

    def test_whose_tracks_a_cut_sits_over(self):
        d = E.digest(song())
        self.assertEqual(E.members(d, {"on": "track", "name": "gl"}), ["gl"])
        self.assertEqual(E.members(d, {"on": "patch", "name": "rig"}), ["gl", "gr"])
        self.assertEqual(E.members(d, {"on": "bus", "name": "gtrs"}), ["gl", "gr", "bass"])   # the low bus runs into it
        self.assertEqual(E.members(d, {"on": "bus", "name": "low"}), ["bass"])
        self.assertEqual(len(E.members(d, {"on": "master", "name": "master"})), 5)


class Read(unittest.TestCase):
    def rows(self, *songs, **kw):
        return {(r["on"], tuple(r["names"]), r["hz"]): r for r in E.read(versions(*songs), **kw)}

    def test_the_tone_left_by_its_lane_and_the_cut_stayed(self):
        """False Summit: the cut made at v2 against a tone; at v4 the tone's lane goes to -60 dB, its notes unchanged."""
        rows = self.rows(song(cut=False), song(), song(), song(tone_lane=-60.0), song(tone_lane=-60.0))
        r = rows[("track", ("gl", "gr"), 700.0)]                                   # the same band on a left and a right: one row
        self.assertEqual((r["since"], r["first"], r["new"], r["was"]), ("v2", False, False, None))
        self.assertEqual([(x["track"], round(x["then"], 2), round(x["now"], 3), x["from"], x["reaches"]) for x in r["left"]],
                         [("tone", 0.5, 0.125, "v4", True)])                       # F4 is under 700 Hz: it reached the band
        self.assertEqual(r["joined"], [])
        bus = rows[("bus", ("gtrs",), 200.0)]
        self.assertEqual((bus["since"], bus["first"]), ("v1", True))
        self.assertEqual([(x["track"], x["from"], x["reaches"]) for x in bus["left"]], [("tone", "v4", False)])   # F4 is above 200 Hz
        shelf = rows[("patch", ("ct-bass",), 1500.0)]
        self.assertEqual([(x["track"], x["reaches"]) for x in shelf["left"]], [("tone", None)])   # a high shelf: notes cannot say
        text = "\n".join(E.lines("x", versions(song(cut=False), song(), song(), song(tone_lane=-60.0), song(tone_lane=-60.0)),
                                 list(rows.values()), 1.5))
        self.assertIn("x at v5 (5 versions read): 4 EQ cuts of 1.5 dB or more", text)
        self.assertIn("  LEFT SINCE: tone (F4, 349 Hz), from v4: 2 cuts made while it was there, the newest first:\n"
                      "      peak 700 Hz -2.5 dB q 1 on tracks gl, gr (since v2): 50% of its beats then, 12% now\n"
                      "      peak 350 Hz -8 dB q 1 on bus low (since v1, the first read): 50% of its beats then, 12% now", text)
        self.assertIn("left, pitched above the cut (not in that band by its notes): tone from v4 (200 Hz)", text)
        self.assertIn("a render does: tone from v4 (1.5 kHz)", text)
        self.assertTrue(text.splitlines()[-1].startswith("1 LEFT SINCE mark: a question, not a fault."))

    def test_notes_taken_out_leave_too_and_a_kit_piece_cannot_say(self):
        rows = self.rows(song(), song(tone_notes=False))
        r = rows[("track", ("gl", "gr"), 700.0)]
        self.assertEqual([(x["track"], x["now"], x["from"]) for x in r["left"]], [("tone", 0.0, "v2")])
        gone = song()
        gone["tracks"][3]["notes"] = []                                            # the hat goes
        r = self.rows(song(), gone)[("track", ("gl", "gr"), 700.0)]
        self.assertEqual([(x["track"], x["reaches"]) for x in r["left"]], [("hat", None)])

    def test_a_cut_retuned_keeps_its_date_and_a_new_one_says_so(self):
        rows = self.rows(song(hz=700, gain="-2.5dB"), song(hz=800, gain="-4dB"))    # a fifth of an octave up, and deeper
        r = rows[("track", ("gl", "gr"), 800.0)]
        self.assertEqual((r["since"], r["was"]), ("v1", {"hz": 700.0, "gain": -2.5}))
        rows = self.rows(song(hz=700), song(hz=1400))                              # an octave away: another cut
        r = rows[("track", ("gl", "gr"), 1400.0)]
        self.assertEqual((r["since"], r["new"], r["left"]), ("v2", True, []))
        self.assertIn("new in this version", "\n".join(E.lines("x", versions(song(hz=700), song(hz=1400)), [r], 1.5)))

    def test_company_that_joined_and_the_filters(self):
        pad = {"name": "pad", "patch": "juno", "notes": notes(0, 32, "C3")}
        rows = self.rows(song(), song(extra=[pad]))
        r = rows[("track", ("gl", "gr"), 700.0)]
        self.assertEqual([(x["track"], x["then"], x["now"]) for x in r["joined"]], [("pad", 0.0, 1.0)])
        text = "\n".join(E.lines("x", versions(song(), song(extra=[pad])), list(rows.values()), 1.5))
        self.assertIn("JOINED SINCE (the cut was not made against them):\n  pad: under ", text)
        self.assertTrue(text.splitlines()[-1].startswith("0 LEFT SINCE marks"))
        self.assertEqual(sorted(k[2] for k in self.rows(song(), least=3.0)), [350.0, 1500.0])
        self.assertEqual(sorted(k[2] for k in self.rows(song(), lo=300, hi=800)), [350.0, 700.0])
        self.assertEqual(E.lines("x", versions(song(cut=False)), [], 20.0), ["x at v1 (1 version read): 0 EQ cuts of 20 dB or more"])


class Tool(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="eqcuts-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self.engine = os.path.join(self.root, "fake-chirp")
        with open(self.engine, "w") as f:
            f.write(ENGINE)
        os.chmod(self.engine, os.stat(self.engine).st_mode | stat.S_IXUSR)
        old = os.environ.get("XDG_CACHE_HOME")
        os.environ["XDG_CACHE_HOME"] = os.path.join(self.root, "cache")
        self.addCleanup(lambda: os.environ.pop("XDG_CACHE_HOME") if old is None else os.environ.__setitem__("XDG_CACHE_HOME", old))
        old_root, E.ROOT = E.ROOT, self.root
        self.addCleanup(setattr, E, "ROOT", old_root)

    def file(self, name, doc):
        p = os.path.join(self.root, name)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as f:
            f.write(doc if isinstance(doc, str) else json.dumps(doc))
        return p

    def run_tool(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = E.main([*argv, "--pin", self.engine])
        return code, out.getvalue()

    def test_your_own_files_oldest_first(self):
        a, b = self.file("a.yaml", song()), self.file("b.yaml", song(tone_lane=-60.0))
        code, text = self.run_tool("x", "--versions", f"v10={a}", f"cand={b}", "--from", "300", "--to", "1500")
        self.assertEqual(code, 0)                                                  # a mark is a question: never a failure
        self.assertIn("x at cand (2 versions read): 3 EQ cuts of 1.5 dB or more", text)
        self.assertIn("LEFT SINCE: tone (F4, 349 Hz), from cand: 2 cuts made while it was there", text)
        self.assertTrue(os.listdir(os.path.join(self.root, "cache", "chirp", "eqcuts")))          # plans are cached by content
        code, again = self.run_tool("x", "--versions", f"v10={a}", f"cand={b}", "--from", "300", "--to", "1500")
        self.assertEqual(again, text)
        code, data = self.run_tool("x", "--versions", f"v10={a}", f"cand={b}", "--json")
        data = json.loads(data)
        self.assertEqual((data["at"], data["versions"], data["skipped"]), ("cand", ["v10", "cand"], []))
        self.assertEqual(len(data["cuts"]), 4)

    def test_a_version_that_does_not_plan_is_skipped_and_said(self):
        a, bad, b = self.file("a.yaml", song()), self.file("bad.yaml", "BAD"), self.file("b.yaml", song(tone_lane=-60.0))
        _, text = self.run_tool("x", "--versions", f"v1={a}", f"v2={bad}", f"v3={b}")
        self.assertIn("(2 versions read; 1 did not plan and are skipped: v2)", text)
        with self.assertRaises(SystemExit) as e:
            self.run_tool("x", "--versions", f"v1={a}", f"v2={bad}")
        self.assertIn("the newest version (v2) does not plan", str(e.exception))

    def test_the_songs_history_is_its_commits_then_the_file_as_it_stands(self):
        if not shutil.which("git"):
            self.skipTest("git")

        def git(*args):
            subprocess.run(["git", "-C", self.root, "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false",
                            *args], check=True, capture_output=True)

        git("init", "-q")
        self.file("songs/x.yaml", song(cut=False))
        git("add", "songs/x.yaml")
        git("commit", "-q", "-m", "climbs: x round 1 — v1 90.0: v1, the skeleton")
        self.file("songs/x.yaml", song())
        git("commit", "-q", "-am", "climbs: x round 2 — v2 91.0: v2, a cut")
        self.file("songs/x.yaml", song(tone_lane=-20.0))                           # quieter, and still there
        git("commit", "-q", "-am", "a fix with no version in its subject")
        self.assertEqual([lb for lb, _ in E.history("x")][:2], ["v1", "v2"])
        self.assertEqual(len(E.history("x")), 3)                                   # the third is named by its hash
        self.file("songs/x.yaml", song(tone_lane=-60.0))                           # not committed
        self.assertEqual(E.history("x")[-1][0], "the file now")
        _, text = self.run_tool("x")
        self.assertIn("x at the file now (4 versions read)", text)
        self.assertIn("LEFT SINCE: tone (F4, 349 Hz), from the file now: 2 cuts made while it was there", text)
        self.assertIn("on tracks gl, gr (since v2)", text)
        cand = self.file("cand.yaml", song(tone_notes=False))
        _, text = self.run_tool("x", "--song", cand)                               # a candidate in the file's place
        self.assertIn("x at cand.yaml (4 versions read)", text)
        with self.assertRaises(SystemExit):
            self.run_tool("nosuch")


if __name__ == "__main__":
    unittest.main()
