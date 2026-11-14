#!/usr/bin/env python3
"""tools/sendpaths.py: sends that go round a clip or a limiter.

Hermetic: made plans, and a stand-in engine that plans the song it is given and renders a soloed track as loud as
its paths make it (0.2 through the clipped bus, plus its send to the room at its level), so --measure's tell is known.

  python3 tools/tests/test_sendpaths.py      (from ~/.config/chirp; a second or two)
"""
import contextlib
import io
import json
import os
import re
import shutil
import stat
import sys
import tempfile
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import sendpaths as S  # noqa: E402

ENGINE = r'''#!/usr/bin/env python3
import json, sys, wave
import numpy as np
a = sys.argv[1:]
song = json.load(open(a[a.index("-f") + 1]))
if a[0] == "plan":
    print(json.dumps({"data": {"canonical": song}}))
    sys.exit(0)
name = a[a.index("--solo") + 1]
def find(ts):
    for t in ts:
        if t.get("name") == name:
            return t
        got = find(t.get("tracks", []))
        if got:
            return got
t = find(song["tracks"])
def db(g):
    return float(str(g["value"] if isinstance(g, dict) else g).rstrip("dB"))
amp = 0.0 if t.get("silent") else 0.2 + sum(0.2 * 10 ** (db(g) / 20) for b, g in (t.get("sends") or {}).items() if b == "oh")
x = amp * np.sin(2 * np.pi * 220 * np.arange(48000) / 48000)
with wave.open(a[a.index("-o") + 1], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(48000)
    w.writeframes((np.repeat(x[:, None], 2, 1) * 32767).astype("<i2").tobytes())
'''
SONG = {"tempo": 120, "buses": {
    "drums": {"fx": ["reverb mix=0.1", "glue", "clip drive=0dB ceiling=-13dB", "eq"]},
    "oh": {"fx": ["reverb kind=room", "eq"]},
    "par": {"fx": [{"type": "compressor"}], "out": "drums"},
    "low": {"fx": [{"type": "eq"}, {"type": "compressor"}]},
    "sub": {"fx": ["eq"], "out": "limited"},
    "limited": {"fx": [{"type": "limiter", "ceiling": "-3dB"}]},
    "hall": {"fx": ["reverb"]}},
    "tracks": [
        {"name": "snare", "out": "drums", "sends": {"oh": "-1.5dB", "par": "0dB", "drums": "-3dB"}},
        {"name": "cym", "out": "drums", "sends": {"oh": {"value": "4.5dB", "mod": [{"src": "auto.x", "amount": 1}]}, "hall": "-18dB"}},
        {"name": "hat", "out": "drums", "silent": True, "sends": {"oh": "4.5dB"}},
        {"name": "bass", "out": "low", "sends": {"hall": 0.5}},
        {"name": "lead", "sends": {"hall": "-10dB"}},
        {"name": "pad", "out": "sub", "sends": {"hall": "-6dB"}},
        {"name": "kit", "fx": ["clip"], "tracks": [{"name": "tom", "sends": {"oh": "-2dB"}}, {"name": "ghost"}]}]}


class Paths(unittest.TestCase):
    def test_what_goes_round_and_what_does_not(self):
        got = {(p["track"], p["send"]): p for p in S.paths(SONG)}
        self.assertEqual(sorted(got),
                         [("cym", "hall"), ("cym", "oh"), ("hat", "oh"), ("pad", "hall"), ("snare", "oh"), ("tom", "oh")])
        self.assertNotIn(("snare", "par"), got)                    # that bus leads back into the clipped one
        self.assertNotIn(("snare", "drums"), got)                  # a send into the clipped bus itself
        self.assertNotIn(("lead", "hall"), got)                    # nothing on its way out to go round
        self.assertNotIn(("bass", "hall"), got)                    # a compressor is not a clip (without --soft)
        snare = got[("snare", "oh")]
        self.assertEqual((snare["where"], snare["by"], snare["db"], snare["loud"], snare["moves"]),
                         ("drums", ["clip"], -1.5, True, False))
        self.assertEqual((got[("cym", "oh")]["db"], got[("cym", "oh")]["moves"]), (4.5, True))     # read at its written value
        self.assertFalse(got[("cym", "hall")]["loud"])             # -18 dB: listed, not marked
        self.assertEqual((got[("pad", "hall")]["where"], got[("pad", "hall")]["by"]), ("limited", ["limiter"]))   # its bus's bus
        self.assertEqual(got[("tom", "oh")]["where"], "track kit")                                       # a parent's strip
        self.assertTrue(S.paths(SONG, over=-20)[1]["loud"] and got[("cym", "hall")]["db"] == -18.0)

    def test_soft_counts_compressors(self):
        soft = {(p["track"], p["send"]): p for p in S.paths(SONG, soft=True)}
        bass = soft[("bass", "hall")]
        self.assertEqual((bass["by"], bass["db"], bass["loud"]), (["compressor"], -6.0, True))
        self.assertEqual(soft[("snare", "oh")]["by"], ["glue", "clip"])

    def test_levels_and_buses_as_a_list(self):
        self.assertEqual([round(S.decibels(g), 1) for g in ("-1.5dB", "0dB", 0.5, "2", {"value": "3dB"}, 0)],
                         [-1.5, 0.0, -6.0, 6.0, 3.0, -200.0])
        as_list = dict(SONG, buses=[dict(v, name=k) for k, v in SONG["buses"].items()])
        self.assertEqual(len(S.paths(as_list)), 6)
        self.assertEqual(S.paths({"tracks": [{"name": "a", "out": "nowhere", "sends": {"x": "0dB"}}]}), [])

    def test_a_send_is_taken_off_one_track_only(self):
        cut = S.without_send(SONG, "tom", "oh")
        self.assertEqual(cut["tracks"][6]["tracks"][0]["sends"], {})
        self.assertEqual(cut["tracks"][0]["sends"], SONG["tracks"][0]["sends"])
        self.assertEqual(SONG["tracks"][6]["tracks"][0]["sends"], {"oh": "-2dB"})
        self.assertIsNone(S.without_send(SONG, "tom", "hall"))
        self.assertIsNone(S.without_send(SONG, "nosuch", "oh"))


class WholeRun(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="sendpaths-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self.engine = os.path.join(self.root, "fake-chirp")
        with open(self.engine, "w") as f:
            f.write(ENGINE)
        os.chmod(self.engine, os.stat(self.engine).st_mode | stat.S_IXUSR)
        self.song = os.path.join(self.root, "song.json")
        with open(self.song, "w") as f:
            json.dump(SONG, f)
        self.clean = os.path.join(self.root, "clean.json")
        with open(self.clean, "w") as f:
            json.dump({"buses": {"hall": {"fx": ["reverb"]}}, "tracks": [{"name": "lead", "sends": {"hall": "-10dB"}}]}, f)

    def run_tool(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = S.main([*argv, "--pin", self.engine])
        return code, out.getvalue()

    def test_the_report(self):
        code, text = self.run_tool(self.song, self.clean)
        self.assertEqual(code, 0)
        lines = text.splitlines()
        self.assertEqual(lines[0], "song.json: 6 sends go round a clip or a limiter, 5 over -10 dB")
        self.assertRegex(lines[2], r"^  snare +drums \(clip\) +oh +-1\.5 dB +LOUD$")
        self.assertRegex(lines[3], r"^  cym +drums \(clip\) +oh +\+4\.5 dB \*  LOUD$")
        self.assertRegex(lines[4], r"^  cym +drums \(clip\) +hall +-18\.0 dB *$")
        self.assertIn("* the level is modulated: read at its written value", text)
        self.assertEqual(lines[-1], "clean.json: no send goes round a clip or a limiter")
        _, soft = self.run_tool(self.clean, "--soft")
        self.assertIn("no send goes round a clip, a limiter or a compressor", soft)
        _, text = self.run_tool(self.song, "--over", "0", "--json")
        self.assertEqual([p["track"] for p in json.loads(text)[0]["paths"] if p["loud"]], ["cym", "hat"])

    def test_the_tell_is_measured(self):
        code, text = self.run_tool(self.song, "--measure", "41-49", "--over", "-5")
        row = {}
        for ln in text.splitlines()[2:]:
            m = re.match(r"^  (\S+) +.*?\) +(\S+) +[-+][0-9.]+ dB", ln)
            if m:
                row[m.group(1) + ">" + m.group(2)] = ln
        # the snare alone: 0.2 through the clip and 0.2 x -1.5 dB by the send: 5.3 dB higher with the send than without
        self.assertRegex(row["snare>oh"], r"alone: peak -8\.7 with, -14\.0 without \(\+5\.3 dB\); loudness \+5\.3 LU with")
        self.assertIn("silent in the window", row["hat>oh"])
        self.assertNotIn("alone", row["cym>hall"])                 # not LOUD: not measured
        self.assertRegex(row["tom>oh"], r"\(\+5\.1 dB\)")
        _, text = self.run_tool(self.song, "--measure", "41-49", "--json")
        snare = next(p for p in json.loads(text)[0]["paths"] if (p["track"], p["send"]) == ("snare", "oh"))
        self.assertAlmostEqual(snare["with"][0] - snare["without"][0], 5.3, delta=0.05)

    def test_what_cannot_be_read_is_said(self):
        with self.assertRaises(SystemExit) as e:
            self.run_tool("no-such-song")
        self.assertIn("no song no-such-song", str(e.exception))
        bad = os.path.join(self.root, "bad.json")
        with open(bad, "w") as f:
            f.write("not a song")
        with self.assertRaises(SystemExit) as e:
            self.run_tool(bad)
        self.assertIn("bad.json does not plan", str(e.exception))
        code, text = self.run_tool()
        self.assertEqual(code, 2)
        self.assertIn("sendpaths.py SONG [SONG ...]", text)


if __name__ == "__main__":
    unittest.main()
