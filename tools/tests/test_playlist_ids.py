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
import unittest.mock

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


    def test_the_rotation_follows_its_own_playlist_to_a_wholly_different_one(self):
        """12 Nov: the album A was playing as the rotation's own repeating playlist; then playlist-ids named one new
        climb whose first version had just been kept. Nothing of the old playlist is wanted any more, and the driver
        took its own entries for somebody else's album and waited for ever. It must drop them and add the new song."""
        self.put("playlist-album", "A\n")
        self.put("playlist-ids", "v1\n")
        open(os.path.join(self.root, "songs", "v1.yaml"), "w").close()
        sent = []
        entries = [{"label": i, "source": os.path.join(self.root, "songs", i + ".yaml"), "passes": 1} for i in ("a1", "a2")]
        st = {"label": "a2", "queue": [], "playlist": {"entries": entries, "current": 1, "repeat": True, "finished": False}}
        P.YIELDED["on"] = False
        with unittest.mock.patch.object(P, "request", lambda msg: sent.append(msg)), unittest.mock.patch.object(P, "MIX", False):
            P.sync(st)
        self.assertFalse(P.YIELDED["on"], "the driver yielded to its own playlist")
        self.assertEqual([m["op"] for m in sent], ["playlist-remove", "playlist-remove", "playlist-add"])
        self.assertEqual([e["label"] for e in sent[-1]["entries"]], ["v1"])

    def test_somebody_elses_album_is_still_left_alone(self):
        self.put("playlist-ids", "v1\n")
        open(os.path.join(self.root, "songs", "v1.yaml"), "w").close()
        sent = []
        entries = [{"label": "x" + str(i), "source": "/elsewhere/x%d.yaml" % i, "passes": 1} for i in range(3)]
        st = {"label": "x0", "queue": [], "playlist": {"entries": entries, "current": 0, "repeat": False, "finished": False}}
        P.YIELDED["on"] = False
        with unittest.mock.patch.object(P, "request", lambda msg: sent.append(msg)), unittest.mock.patch.object(P, "MIX", False):
            P.sync(st)
        self.assertTrue(P.YIELDED["on"])
        self.assertEqual(sent, [])
        P.YIELDED["on"] = False



class Socket(unittest.TestCase):
    """The driver finds the groove's socket where chirp does, even without XDG_RUNTIME_DIR (the watchdog started one
    without it, and every playlist change failed: [Errno 2])."""

    def test_falls_back_to_the_dir_that_holds_the_socket(self):
        d = tempfile.mkdtemp(prefix="playlist-sock-")
        self.addCleanup(shutil.rmtree, d, True)
        run = os.path.join(d, "run")
        os.makedirs(os.path.join(run, "chirp"))
        open(os.path.join(run, "chirp", P.ID + ".sock"), "w").close()
        env = {k: v for k, v in os.environ.items() if k not in ("XDG_RUNTIME_DIR", "PLAYLIST_SOCKET")}
        with unittest.mock.patch.dict(os.environ, env, clear=True), \
                unittest.mock.patch.object(P.os, "getuid", return_value=424242):
            self.assertTrue(P.sock_path().startswith("/run/user/424242/") or P.sock_path().startswith("/tmp/chirp-"))
            os.environ["XDG_RUNTIME_DIR"] = run
            self.assertEqual(P.sock_path(), os.path.join(run, "chirp", P.ID + ".sock"))
        real = f"/run/user/{os.getuid()}/chirp/{P.ID}.sock"
        if os.path.exists(real):
            with unittest.mock.patch.dict(os.environ, env, clear=True):
                self.assertEqual(P.sock_path(), real)


if __name__ == "__main__":
    unittest.main()
