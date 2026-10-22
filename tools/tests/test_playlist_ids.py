#!/usr/bin/env python3
"""playlist.py tools/playlist-ids: the groove plays only the listed climbs that have songs (Harry, 2026-10-22: the
four vocal climbs), falling back to the album/rotation until one has a song.

  python3 tools/tests/test_playlist_ids.py      (from ~/.config/chirp; instant; temp registry, no groove)
"""
import json
import os
import shutil
import sys
import tempfile
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import playlist as P  # noqa: E402


class Ids(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="playlist-ids-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self.tools = os.path.join(self.root, "tools")
        os.makedirs(os.path.join(self.root, "songs"))
        os.makedirs(self.tools)
        climbs = [{"id": "a1", "song": "songs/a1.yaml", "meta": {"album": "A", "track": 1}},
                  {"id": "a2", "song": "songs/a2.yaml", "meta": {"album": "A", "track": 2}},
                  {"id": "v1", "song": "songs/v1.yaml"}, {"id": "v2", "song": "songs/v2.yaml"},
                  {"id": "v3", "song": "songs/v3.yaml"}]
        with open(os.path.join(self.root, "climbs.json"), "w") as f:
            json.dump({"climbs": climbs}, f)
        for s in ("a1", "a2"):
            open(os.path.join(self.root, "songs", s + ".yaml"), "w").close()
        self.old = (P.HERE, P.ROOT, P.log)
        P.HERE, P.ROOT, P.log = self.tools, self.root, lambda *a: None
        self.addCleanup(lambda: setattr(P, "HERE", self.old[0]) or setattr(P, "ROOT", self.old[1]) or setattr(P, "log", self.old[2]))
        P.IDS_MODE[0] = P.ALBUM_MODE[0] = None

    def put(self, name, text):
        with open(os.path.join(self.tools, name), "w") as f:
            f.write(text)

    def ids(self):
        return [c["id"] for c in P.climbs()]

    def test_no_file_keeps_the_rotation(self):
        self.assertEqual(self.ids(), ["a1", "a2", "v1", "v2", "v3"])

    def test_until_a_listed_climb_has_a_song_the_album_plays(self):
        self.put("playlist-album", "A\n")
        self.put("playlist-ids", "v3, v1\nv2\n")
        self.assertEqual(self.ids(), ["a1", "a2"])

    def test_listed_climbs_with_songs_play_in_the_listed_order(self):
        self.put("playlist-album", "A\n")
        self.put("playlist-ids", "v3 v1 v2")
        for s in ("v1", "v3"):
            open(os.path.join(self.root, "songs", s + ".yaml"), "w").close()
        self.assertEqual(self.ids(), ["v3", "v1"])


if __name__ == "__main__":
    unittest.main()
