#!/usr/bin/env python3
"""libguard: a library change must not alter songs it should not (10 Nov).

  python3 tools/tests/test_libguard.py      (from ~/.config/chirp; a temp git repo and a stand-in planner: no engine)
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import libguard as G  # noqa: E402


def slurp(path):
    with open(path) as f:
        return f.read()


def planner(cfg, song):
    """Stand-in for `chirp plan`: a song is lines of patch names; its canonical form is its text plus each named
    library file's content under CFG (a name without a file is a built-in). `!broken` does not plan."""
    text = slurp(song)
    if "!broken" in text:
        return None, ""
    out = [text]
    for name in text.split():
        for d in G.LIB_DIRS:
            for ext in (".yaml", ".wav"):
                p = os.path.join(os.path.dirname(cfg + "/"), d, name + ext)
                if os.path.exists(p) and ext == ".yaml":
                    out.append(slurp(p))
    canon = "\n".join(out)
    return str(hash(canon)), canon


class LibGuard(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        g = lambda *a: subprocess.run(["git", "-C", self.d, *a], check=True, capture_output=True)   # noqa: E731
        g("init", "-q")
        g("config", "user.email", "t@t")
        g("config", "user.name", "t")
        for sub in ("patches", "racks", "irs", "songs"):
            os.makedirs(os.path.join(self.d, sub))
        self.w("config.yaml", "x: 1\n")
        self.w("patches/bass.yaml", "bass v1\n")
        self.w("patches/pad.yaml", "pad v1\n")
        self.w("racks/crush.yaml", "crush v1\n")
        self.w("irs/hall.wav", "RIFF1")
        self.w("songs/old-1.yaml", "bass organ\n")           # a released song: bass (user library) + organ (built-in)
        self.w("songs/old-2.yaml", "pad crush hall\n")
        self.w("songs/new-1.yaml", "bass\n")                 # the album in progress
        self.w("songs/new-2.yaml", "pad\n")
        self.w("songs/bad.yaml", "!broken bass\n")
        reg = {"focus": "Now", "climbs": [
            {"id": "old-1", "meta": {"album": "Then"}}, {"id": "old-2", "meta": {"album": "Then"}},
            {"id": "new-1", "meta": {"album": "Now"}, "owner": "ann"}, {"id": "new-2", "meta": {"album": "now"}, "owner": "bob"},
            {"id": "bad", "meta": {"album": "Then"}}, {"id": "gone", "meta": {"album": "Then"}}]}
        self.w("climbs.json", json.dumps(reg))
        g("add", "-A")
        g("commit", "-q", "-m", "init")

    def w(self, relp, text):
        with open(os.path.join(self.d, relp), "w") as f:
            f.write(text)

    def check(self, paths=None, **kw):
        return G.check(paths, root=self.d, planner=planner, **kw)

    def test_is_library(self):
        self.assertTrue(G.is_library("patches/bass.yaml", self.d))
        self.assertTrue(G.is_library(os.path.join(self.d, "irs/hall.wav"), self.d))
        self.assertFalse(G.is_library("songs/old-1.yaml", self.d))
        self.assertFalse(G.is_library("config.yaml", self.d))

    def test_an_edit_to_a_shared_patch_names_every_song_it_changes(self):
        self.w("patches/bass.yaml", "bass v2\n")
        r = self.check(["patches/bass.yaml"])
        self.assertEqual(r["frozen"], ["old-1"])
        self.assertEqual(r["progress"], [{"id": "new-1", "owner": "ann"}])
        self.assertEqual(r["unplannable"], ["bad"])           # broken at HEAD either way: reported, not blamed
        self.assertEqual(r["checked"], 5)                      # `gone` has no song file
        self.assertEqual(G.verdict(r)[0], 1)

    def test_only_the_named_paths_count_not_other_dirty_files(self):
        self.w("patches/bass.yaml", "bass v2\n")               # someone else's uncommitted edit in the shared tree
        self.w("patches/pad.yaml", "pad v2\n")
        r = self.check(["patches/pad.yaml"])
        self.assertEqual((r["frozen"], [p["id"] for p in r["progress"]]), (["old-2"], ["new-2"]))
        self.assertEqual(G.dirty_library(self.d), ["patches/bass.yaml", "patches/pad.yaml"])

    def test_a_new_patch_nothing_uses_is_free(self):
        self.w("patches/bass-2.yaml", "bass v2\n")
        r = self.check(["patches/bass-2.yaml"])
        self.assertEqual((r["frozen"], r["progress"], G.verdict(r)[0]), ([], [], 0))

    def test_a_new_file_that_shadows_a_built_in_is_caught(self):
        self.w("patches/organ.yaml", "my organ\n")             # `organ` was the engine's built-in for old-1
        r = self.check(["patches/organ.yaml"])
        self.assertEqual(r["frozen"], ["old-1"])

    def test_deleting_a_used_patch_is_caught(self):
        os.unlink(os.path.join(self.d, "patches/pad.yaml"))
        r = self.check(["patches/pad.yaml"])
        self.assertEqual(r["frozen"], ["old-2"])

    def test_your_own_songs_may_change(self):
        self.w("songs/new-1.yaml", "bass\n")
        r = self.check(overlay={"patches/solo.yaml": "x"}, me="ann")
        self.assertEqual(G.verdict(r)[0], 0)
        self.w("patches/bass.yaml", "bass v2\n")
        r = G.check(["patches/bass.yaml"], root=self.d, planner=planner, me="ann", only=["new-1", "new-2"])
        self.assertEqual((r["own"], r["progress"], G.verdict(r)[0]), (["new-1"], [], 0))
        r = G.check(["patches/bass.yaml"], root=self.d, planner=planner, me="bob", only=["new-1", "new-2"])
        self.assertEqual((r["own"], [p["id"] for p in r["progress"]], G.verdict(r)[0]), ([], ["new-1"], 2))
        r = G.check(["patches/bass.yaml"], root=self.d, planner=planner, mine=("new-1",), only=["new-1", "new-2"])
        self.assertEqual(r["own"], ["new-1"])                  # `done` passes the round's own climb

    def test_a_changed_asset_is_matched_by_name(self):
        self.w("irs/hall.wav", "RIFF2")
        r = self.check(["irs/hall.wav"])
        self.assertEqual((r["frozen"], r["assets"]), (["old-2"], ["old-2"]))
        self.w("irs/room.wav", "RIFF3")                        # a new asset: free
        self.assertEqual(self.check(["irs/room.wav"])["frozen"], [])

    def test_no_change_no_work(self):
        r = self.check(["patches/bass.yaml", "songs/old-1.yaml"])
        self.assertEqual((r["paths"], r["checked"]), ([], 0))
        self.assertEqual(G.verdict(r), (0, ["libguard: no library file differs from HEAD"]))

    def test_overlay_never_touches_the_working_tree(self):
        r = self.check(overlay={"patches/bass.yaml": "bass v3\n"})
        self.assertEqual(r["frozen"], ["old-1"])
        self.assertEqual(slurp(os.path.join(self.d, "patches/bass.yaml")), "bass v1\n")
        self.assertEqual(subprocess.run(["git", "-C", self.d, "status", "--porcelain"], capture_output=True,
                                        text=True).stdout, "")


if __name__ == "__main__":
    unittest.main()
