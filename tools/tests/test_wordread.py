#!/usr/bin/env python3
"""tools/wordread.py: a recogniser as the ear for words, and its control on reference records (chirper-zero's barktest
and refread, Common Time v17-v18, made general).

Hermetic: the recogniser is stood in for (what it "wrote" is given), so the counting is what is tested: words found in
order, a looped sentence scoring few different words, the control printing counts and never the records' words.

  python3 tools/tests/test_wordread.py      (from ~/.config/chirp; a second or two; needs ffmpeg for `control`)
"""
import contextlib
import io
import json
import math
import os
import re
import shutil
import struct
import sys
import tempfile
import unittest
import wave

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import wordread as W  # noqa: E402

LYRIC = "wait not yet each one keeps its own count none of them wrong"


def tone(path, loud_from=None, seconds=6, sr=8000):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(b"".join(struct.pack("<h", int((6000 if loud_from is not None and loud_from <= i / sr < loud_from + 2 else 60)
                                                     * math.sin(2 * math.pi * 440 * i / sr))) for i in range(sr * seconds)))


class WordRead(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="wordread-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        old = (W.ROOT, W.recognise)
        self.addCleanup(lambda: (setattr(W, "ROOT", old[0]), setattr(W, "recognise", old[1])))
        W.ROOT = self.root
        self.wrote = {}
        self.asked = []

        def recognise(path, model, t0=None, t1=None):
            self.asked.append((os.path.basename(path), model, t0, t1))
            return self.wrote[(os.path.basename(path), model)]
        W.recognise = recognise

    def run_tool(self, *argv):
        out, old = io.StringIO(), sys.argv
        sys.argv = ["wordread.py", *argv]
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
                W.main()
        finally:
            sys.argv = old
        return out.getvalue()

    def voice(self, name):
        p = os.path.join(self.root, name)
        tone(p)
        return p

    def test_words_are_counted_in_order(self):
        self.assertEqual(W.in_order(W.words("wait not yet"), W.words("Wait! Not... yet.")), 3)
        self.assertEqual(W.in_order(W.words("wait not yet"), W.words("yet not wait")), 1)        # the order matters
        self.assertEqual(W.in_order(W.words("keep count keep count"), W.words("keep count")), 2)

    def test_read_scores_each_voice_and_model(self):
        clear, bark = self.voice("clear.wav"), self.voice("bark.wav")
        self.wrote = {("clear.wav", "small.en"): "Wait, not yet. Each one keeps its own count. None of them wrong.",
                      ("clear.wav", "base.en"): "Wait, not yet. Each one keeps it sound. None of them wrong.",
                      ("bark.wav", "small.en"): "I'm going to go. I'm going to go. I'm going to go.",
                      ("bark.wav", "base.en"): "Wait."}
        d = json.loads(self.run_tool("read", clear, bark, "--lyric", LYRIC, "--models", "small.en,base.en", "--json"))
        self.assertEqual([r["lyric_words"] for r in d], [13, 13])
        self.assertEqual(d[0]["models"]["small.en"]["read"], 13)
        self.assertEqual(d[0]["models"]["base.en"]["read"], 10)              # "its own count" was not written
        self.assertEqual((d[1]["models"]["small.en"]["read"], d[1]["models"]["small.en"]["different"]), (0, 4))   # a loop
        text = self.run_tool("read", clear, "--lyric", LYRIC)
        self.assertIn("13 / 13 /  13", text)
        self.assertIn("small.en: Wait, not yet.", text)
        self.assertEqual(self.asked[-1], ("clear.wav", "small.en", None, None))   # small.en is the default judge

    def test_the_lyric_can_come_from_a_file_and_is_required(self):
        clear = self.voice("clear.wav")
        self.wrote = {("clear.wav", "small.en"): "wait not yet"}
        f = os.path.join(self.root, "lyric.txt")
        with open(f, "w") as fh:
            fh.write("Wait.\nNot yet.\n")
        self.assertEqual(json.loads(self.run_tool("read", clear, "--lyric-file", f, "--json"))[0]["models"]["small.en"]["read"], 3)
        with self.assertRaises(SystemExit) as e:
            self.run_tool("read", clear)
        self.assertIn("--lyric", str(e.exception))

    @unittest.skipUnless(shutil.which("ffmpeg"), "ffmpeg")
    def test_control_counts_and_never_prints_the_records_words(self):
        tone(os.path.join(self.root, "ref", "stems", "bs_roformer_sw", "rec", "vocals.wav"), loud_from=3)
        tone(os.path.join(self.root, "ref", "rec.wav"))
        tone(os.path.join(self.root, "ref", "nostem.wav"))
        self.wrote = {("vocals.wav", "small.en"): "the line that's right dead face turning away",
                      ("rec.wav", "small.en"): "the line dead face and nothing more"}
        text = self.run_tool("control", "rec", "nostem", "--secs", "2")
        self.assertEqual(self.asked, [("vocals.wav", "small.en", 3.0, 5.0), ("rec.wav", "small.en", 3.0, 5.0)])   # the busiest 2 s
        row = text.splitlines()[1]
        self.assertTrue(row.startswith("rec "))
        self.assertEqual([int(x) for x in re.findall(r"\d+", row)], [3, 8, 8, 7, 7, 4])   # from 3 s; stem 8 words, mix 7, 4 in common
        self.assertNotIn("dead", text)
        self.assertNotIn("nostem", text)                                            # skipped, said on stderr
        self.asked.clear()
        d = json.loads(self.run_tool("control", "rec:1", "--secs", "2", "--json"))
        self.assertEqual((d[0]["from"], d[0]["in_common"]), (1.0, 4))
        self.assertEqual(self.asked[0][2:], (1.0, 3.0))
        with self.assertRaises(SystemExit):
            self.run_tool("control", "nostem")


if __name__ == "__main__":
    unittest.main()
