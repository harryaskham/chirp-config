#!/usr/bin/env python3
"""chirpers.py upload sheets: per-track lyrics from compose/ALBUM/lyrics/tN.txt (chirp-eco, 5 Nov). Without lyrics the
sheet is byte-identical to before; with them, a per-track section (language and words, or instrumental).

  python3 tools/tests/test_uploadsheet.py      (from ~/.config/chirp; under a second)
"""
import os
import sys
import tempfile
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import chirpers as CH  # noqa: E402

META = {"artist": "chirpers", "album": "Test Album", "year": 2026, "cover": "cover-3000.jpg", "songwriter": "S",
        "ai_disclosure": "D", "genres": ["Electronic", "Experimental"], "explicit": False,
        "tracks": [{"n": 1, "title": "One", "file": "01 - One.wav", "seconds": 61.0, "sha256": "ab" * 32,
                    "verified": True, "source": "verified: identical to the released MP3"},
                   {"n": 2, "title": "Two", "file": "02 - Two.wav", "seconds": 125.4, "sha256": "cd" * 32,
                    "verified": True, "source": "verified: identical to the released MP3"}]}
PUB = {"distributor": "DistroKid", "language": "instrumental (no lyrics), unless a track has words"}

# The sheet as upload_sheet wrote it before lyrics existed (byte-identity of the default).
OLD = """# Test Album: upload sheet (DistroKid)

Fill the form in this order; every file named here is in this folder.

- Artist name: **chirpers** (lowercase; create a NEW artist profile if the store offers an existing 'Chirpers', which is someone else)
- Album title: **Test Album**
- Release year: 2026
- Primary genre: Electronic; secondary: Experimental
- Cover: `cover-3000.jpg` (3000x3000 JPEG, no text)
- Songwriter / composer (every track): **S**
- AI disclosure: D
- Explicit: no; language: instrumental (no lyrics), unless a track has words
- ISRC / UPC: leave blank (the distributor assigns them); record them in metadata.json afterwards
- Release date: the earliest the distributor allows unless Harry picks one; no pre-save needed

| # | title | file | length | sha256 (first 12) | verified | source |
|---|---|---|---|---|---|---|
| 1 | One | `01 - One.wav` | 1:01 | abababababab | yes | verified: identical to the released MP3 |
| 2 | Two | `02 - Two.wav` | 2:05 | cdcdcdcdcdcd | yes | verified: identical to the released MP3 |
"""


class Sheet(unittest.TestCase):
    def test_default_unchanged(self):
        self.assertEqual(CH.upload_sheet(META, PUB), OLD)
        self.assertEqual(CH.upload_sheet(META, PUB, {}), OLD)
        self.assertEqual(CH.upload_sheet(META, PUB, None), OLD)

    def test_lyrics_section(self):
        ly = {1: {"words": True, "language": "English", "text": "keep it there (x2)\nthere."}}
        s = CH.upload_sheet(META, PUB, ly)
        self.assertTrue(s.startswith(OLD))
        tail = s[len(OLD):]
        self.assertIn("## Lyrics (per track)", tail)
        self.assertIn("### 1. One (English)\n\n```\nkeep it there (x2)\nthere.\n```", tail)
        self.assertIn("### 2. Two (instrumental)", tail)
        self.assertTrue(s.endswith("\n") and not s.endswith("\n\n"))


class Parse(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="uploadsheet-test-")
        self.d = os.path.join(self.root, "compose", "alb", "lyrics")
        os.makedirs(self.d)

    def write(self, name, text):
        with open(os.path.join(self.d, name), "w") as f:
            f.write(text)

    def test_header_and_words(self):
        self.write("t1.txt", "WORDS: yes  LANGUAGE: English\nslow down a touch.\nthere.\n")
        self.write("t2.txt", "WORDS: no  LANGUAGE: English\n")
        self.write("t3.txt", "WORDS: yes  LANGUAGE: Japanese\nhi\n")
        self.write("notes.md", "ignored\n")
        ly = CH.album_lyrics("alb", root=self.root)
        self.assertEqual(sorted(ly), [1, 2, 3])
        self.assertEqual(ly[1], {"words": True, "language": "English", "text": "slow down a touch.\nthere."})
        self.assertFalse(ly[2]["words"])
        self.assertEqual(ly[3]["language"], "Japanese")

    def test_no_header(self):
        self.write("t4.txt", "just words\n")
        self.assertEqual(CH.album_lyrics("alb", root=self.root)[4], {"words": True, "language": "English", "text": "just words"})

    def test_none(self):
        self.assertEqual(CH.album_lyrics("nope", root=self.root), {})


if __name__ == "__main__":
    unittest.main()
