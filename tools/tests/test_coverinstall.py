"""chirpers.py cover: a cover chosen after the cut goes into the existing release without touching its audio."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import chirpers as CH  # noqa: E402

HAVE = shutil.which("ffmpeg") and shutil.which("ffprobe")
try:
    from PIL import Image
except ImportError:
    Image = None


def packets_md5(path):
    return subprocess.run(["ffmpeg", "-nostats", "-loglevel", "error", "-i", path, "-map", "0:a", "-c", "copy", "-f", "md5", "-"],
                          capture_output=True, text=True).stdout.strip()


def picture(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries",
                        "stream=width,height:stream_disposition=attached_pic", "-of", "json", path], capture_output=True, text=True)
    st = (json.loads(r.stdout or "{}").get("streams") or [])
    return [(s.get("width"), s.get("height"), (s.get("disposition") or {}).get("attached_pic")) for s in st]


def tags(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format_tags=title,artist,album,track", "-of", "json", path],
                       capture_output=True, text=True)
    return {k.lower(): v for k, v in (json.loads(r.stdout).get("format", {}).get("tags") or {}).items()}


@unittest.skipUnless(HAVE and Image, "needs ffmpeg, ffprobe and Pillow")
class CoverInstall(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="covertest-")
        self.rdir = os.path.join(self.d, "Some Album")
        os.makedirs(os.path.join(self.rdir, "master"))
        for n, f in ((1, 330), (2, 440)):
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", f"sine=frequency={f}:duration=1.5:sample_rate=48000",
                            "-ac", "2", "-c:a", "libmp3lame", "-q:a", "0", "-id3v2_version", "3", "-metadata", f"title=Song {n}",
                            "-metadata", "artist=chirpers", "-metadata", "album=Some Album", "-metadata", f"track={n}/2",
                            os.path.join(self.rdir, f"{n:02d} - Song {n}.mp3")], check=True)
        self.meta = {"artist": "chirpers", "album": "Some Album", "year": 2026, "genre": "x", "release": "Some Album", "pin": "chirp-x",
                     "seed": 0, "target_lufs": -11.0, "cover": None, "songwriter": None, "ai_disclosure": None, "genres": None,
                     "explicit": False, "tracks": [{"n": 1, "title": "Song 1", "file": "01 - Song 1.wav", "seconds": 1.5, "explicit": False,
                                                    "isrc": None, "sha256": "0" * 64, "verified": True, "source": "working copy"}]}
        with open(os.path.join(self.rdir, "master", "metadata.json"), "w") as f:
            json.dump(self.meta, f, indent=1)
        self.art = os.path.join(self.d, "art.png")
        Image.new("RGB", (3000, 3000), (20, 10, 60)).save(self.art)

    def tearDown(self):
        shutil.rmtree(self.d, ignore_errors=True)

    def test_mp3s_gain_the_picture_and_keep_their_audio_and_tags(self):
        mp3s = sorted(os.path.join(self.rdir, f) for f in os.listdir(self.rdir) if f.endswith(".mp3"))
        before = {m: (packets_md5(m), tags(m)) for m in mp3s}
        self.assertTrue(all(not picture(m) for m in mp3s))
        res = CH.install_cover(self.art, self.rdir, {}, None)
        self.assertEqual((res["mp3"], res["failed"], res["master"]), (2, [], True))
        for m in mp3s:
            self.assertEqual(packets_md5(m), before[m][0], "the audio packets must be the same")
            self.assertEqual(tags(m), before[m][1], "title, artist, album and track survive")
            self.assertEqual(picture(m), [(1024, 1024, 1)], "one attached picture, 1024 wide")

    def test_master_gets_the_store_cover_and_the_sheet_names_it(self):
        CH.install_cover(self.art, self.rdir, {}, None)
        m = os.path.join(self.rdir, "master")
        self.assertEqual(Image.open(os.path.join(m, "cover-3000.jpg")).size, (3000, 3000))
        with open(os.path.join(m, "metadata.json")) as f:
            meta = json.load(f)
        self.assertEqual(meta["cover"], "cover-3000.jpg")
        self.assertEqual({k: v for k, v in meta.items() if k != "cover"}, {k: v for k, v in self.meta.items() if k != "cover"})
        with open(os.path.join(m, "UPLOAD.md")) as f:
            self.assertIn("cover-3000.jpg", f.read())

    def test_running_it_twice_leaves_one_picture(self):
        CH.install_cover(self.art, self.rdir, {}, None)
        m = os.path.join(self.rdir, "01 - Song 1.mp3")
        md5 = packets_md5(m)
        CH.install_cover(self.art, self.rdir, {}, None)
        self.assertEqual(picture(m), [(1024, 1024, 1)])
        self.assertEqual(packets_md5(m), md5)

    def test_an_unmastered_release_only_gets_tags(self):
        shutil.rmtree(os.path.join(self.rdir, "master"))
        res = CH.install_cover(self.art, self.rdir, {}, None)
        self.assertEqual((res["mp3"], res["master"]), (2, False))
        self.assertFalse(os.path.exists(os.path.join(self.rdir, "master")))


if __name__ == "__main__":
    unittest.main()
