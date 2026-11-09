#!/usr/bin/env python3
"""listen.py: share hashes, byte ranges, the notes event log, snapshot reuse (an unchanged song file is linked, not
re-rendered) and the server's API (notes, ranged media, the chirp web redirect).

  python3 tools/tests/test_listen.py      (from ~/.config/chirp; a few seconds, renders nothing real)
"""
import json
import os
import struct
import sys
import tempfile
import threading
import unittest
import urllib.request
import wave

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import listen as L  # noqa: E402


def fake_render(pin, song, out):
    with wave.open(out, "w") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(48000)
        w.writeframes(struct.pack("<hh", 0, 0) * 4800)            # 0.1 s of silence
    fake_render.calls += 1


fake_render.calls = 0


class Pure(unittest.TestCase):
    def test_share_hash_roundtrip(self):
        text = json.dumps({"tempo": 100, "tracks": [{"name": "v", "patch": "voice-hook"}]})
        h = L.share_hash(text)
        self.assertTrue(h.startswith("#s=") and "=" not in h[3:] and "+" not in h and "/" not in h)
        self.assertEqual(L.from_hash(h), text)

    def test_byte_range(self):
        self.assertEqual(L.byte_range("bytes=0-99", 1000), (0, 99))
        self.assertEqual(L.byte_range("bytes=900-", 1000), (900, 999))
        self.assertEqual(L.byte_range("bytes=-100", 1000), (900, 999))
        self.assertEqual(L.byte_range("bytes=0-5000", 1000), (0, 999))
        self.assertIsNone(L.byte_range(None, 1000))
        self.assertIsNone(L.byte_range("bytes=2000-", 1000))

    def test_notes_event_log(self):
        ev = [{"op": "add", "id": "a", "at": "1", "n": 8, "t": 3.0, "text": "last chord!"},
              {"op": "add", "id": "b", "at": "2", "n": 1, "t": 9.0, "text": "too dense"},
              {"op": "reply", "id": "a", "at": "3", "by": "chirper-three", "text": "now D", "done": True},
              {"op": "delete", "id": "b", "at": "4"}, {"op": "reply", "id": "zz", "text": "orphan"}]
        ns = L.reduce_notes(ev)
        self.assertEqual([n["id"] for n in ns], ["a"])
        self.assertTrue(ns[0]["done"])
        self.assertEqual(ns[0]["replies"][0]["by"], "chirper-three")


class Who(unittest.TestCase):
    def test_reply_is_signed_by_the_caco_agent_not_the_unix_user(self):
        env = dict(os.environ)
        try:
            for k in ("CHIRP_LISTEN_AUTHOR", "CACOPHONY_ACTOR"):
                os.environ.pop(k, None)
            os.environ["USER"] = "harry"
            os.environ["CACO_AGENT_ID"] = L.AGENTS["chirper-one"]
            self.assertEqual(L.whoami(), "chirper-one")
            os.environ["CACO_AGENT_ID"] = "visiting-unknown"
            self.assertEqual(L.whoami(), "visiting-unknown")
            os.environ["CHIRP_LISTEN_AUTHOR"] = "wM"
            self.assertEqual(L.whoami(), "wM")
        finally:
            os.environ.clear()
            os.environ.update(env)


class Snapshots(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        L.DATA = self.d
        fake_render.calls = 0

    def test_second_cut_links_unchanged_tracks(self):
        a = L.cut("chirpers9", "first", render=fake_render, canonical=lambda p, s: '{"tempo":1}', log=lambda *x: None)
        n = len(a["tracks"])
        self.assertGreater(n, 0)
        self.assertEqual(fake_render.calls, n)
        b = L.cut("chirpers9", "second", render=fake_render, canonical=lambda p, s: '{"tempo":1}', log=lambda *x: None)
        self.assertEqual(fake_render.calls, n)                    # nothing re-rendered
        self.assertEqual(b["changed"], 0)
        self.assertEqual(b["prev"], a["id"])
        p = lambda s: os.path.join(self.d, "chirpers9", "snapshots", s, "t01.mp3")   # noqa: E731
        self.assertEqual(os.stat(p(a["id"])).st_ino, os.stat(p(b["id"])).st_ino)
        self.assertEqual([s["id"] for s in L.snapshots("chirpers9")], [a["id"], b["id"]])
        self.assertEqual(os.stat(p(a["id"])[:-3] + "song").st_ino, os.stat(p(b["id"])[:-3] + "song").st_ino)

    def test_look_args_programme_per_track(self):
        d = tempfile.mkdtemp()
        open(os.path.join(d, "chirpers9-t2.yaml"), "w").write("scenes: []")
        self.assertEqual(L.look_args(None, "chirpers9-t2", d), [])
        self.assertEqual(L.look_args("accretion3d", "chirpers9-t2", d), ["--look", "accretion3d"])   # unchanged
        self.assertEqual(L.look_args("{id}|accretion3d", "chirpers9-t2", d), ["--vis", os.path.join(d, "chirpers9-t2.yaml")])
        self.assertEqual(L.look_args("{id}|accretion3d", "chirpers9-t3", d), ["--look", "accretion3d"])
        self.assertEqual(L.look_args("{id}", "chirpers9-t3", d), [])                                 # engine default

    def test_programme_mtime_follows_kits(self):
        d = tempfile.mkdtemp()
        for name, text, t in (("chirpers9-t2", "scenes: [{use: kit-a}]", 100), ("kit-a", "layers: [{use: 'kit-b'}]", 200),
                              ("kit-b", "layers: []", 300), ("kit-c", "layers: []", 900)):
            p = os.path.join(d, name + ".yaml")
            open(p, "w").write(text)
            os.utime(p, (t, t))
        self.assertEqual(L.programme_mtime("{id}|accretion3d", "chirpers9-t2", d), 300)   # kit-b, not the unused kit-c
        self.assertIsNone(L.programme_mtime("{id}|accretion3d", "chirpers9-t3", d))       # no programme file
        self.assertIsNone(L.programme_mtime("accretion3d", "chirpers9-t2", d))

    def test_stale_redoes_only_previews_older_than_their_programme(self):
        a = L.cut("chirpers9", "", render=fake_render, canonical=lambda p, s: '{"tempo":1}', log=lambda *x: None)
        d = os.path.join(self.d, "chirpers9", "snapshots", a["id"])
        calls = []

        def run(cmd, **kw):
            calls.append(cmd)
            open(cmd[-1], "wb").write(b"mp4")
            return type("R", (), {"returncode": 0, "stderr": ""})()
        quiet = lambda *x: None   # noqa: E731
        L.videos("chirpers9", a["id"], {1}, "{id}|accretion3d", log=quiet, run=run)
        made = os.path.getmtime(os.path.join(d, "t01.mp4"))
        orig = L.programme_mtime
        try:
            L.programme_mtime = lambda look, tid: made - 100                                 # programme older: kept
            L.videos("chirpers9", a["id"], {1}, "{id}|accretion3d", log=quiet, run=run, stale=True)
            self.assertEqual(len(calls), 1)
            L.programme_mtime = lambda look, tid: made + 100                                 # programme newer: redone
            L.videos("chirpers9", a["id"], {1}, "{id}|accretion3d", log=quiet, run=run, stale=True)
            self.assertEqual(len(calls), 2)
            L.programme_mtime = lambda look, tid: None                                       # no programme: kept
            L.videos("chirpers9", a["id"], {1}, "{id}|accretion3d", log=quiet, run=run, stale=True)
            self.assertEqual(len(calls), 2)
        finally:
            L.programme_mtime = orig

    def test_each_track_renders_on_the_pin_of_its_start(self):
        a = L.cut("chirpers9", "", render=fake_render, canonical=lambda p, s: '{"tempo":1}', log=lambda *x: None)
        pins = []

        def run(cmd, **kw):
            pins.append(cmd[3])
            open(cmd[-1], "wb").write(b"mp4")
            return type("R", (), {"returncode": 0, "stderr": ""})()
        orig, n = L.read_text, iter(range(100))
        try:
            L.read_text = lambda p: f"/pins/chirp-{next(n)}" if p.endswith("groove-pin") else orig(p)  # adopted mid-run
            L.videos("chirpers9", a["id"], {1, 2}, "accretion", log=lambda *x: None, run=run)
        finally:
            L.read_text = orig
        self.assertEqual(pins, ["/pins/chirp-0", "/pins/chirp-1"])

    def test_video_renders_the_snapshots_own_song_text(self):
        a = L.cut("chirpers9", "", render=fake_render, canonical=lambda p, s: '{"tempo":1}', log=lambda *x: None)
        d = os.path.join(self.d, "chirpers9", "snapshots", a["id"])
        with open(os.path.join(d, "t01.song"), "w") as f:
            f.write("SNAPSHOT TEXT")                          # differs from songs/ now: the copy must win
        seen = []

        def run(cmd, **kw):
            seen.append(open(cmd[cmd.index("-f") + 1]).read())
            open(cmd[-1], "wb").write(b"mp4")
            return type("R", (), {"returncode": 0, "stderr": ""})()
        L.videos("chirpers9", a["id"], {1}, "accretion", log=lambda *x: None, run=run)
        self.assertEqual(seen, ["SNAPSHOT TEXT"])
        self.assertTrue(os.path.exists(os.path.join(d, "t01.mp4")))
        self.assertTrue(L.snapshots("chirpers9")[-1]["tracks"][0]["video"])
        self.assertFalse([f for f in os.listdir(os.path.join(L.ROOT, "songs")) if f.startswith(f".listen-{os.getpid()}")])
        L.videos("chirpers9", a["id"], {1}, "accretion", log=lambda *x: None, run=run)            # exists: skipped
        self.assertEqual(len(seen), 1)
        L.videos("chirpers9", a["id"], {1}, "accretion", log=lambda *x: None, run=run, redo=True)  # --redo
        self.assertEqual(len(seen), 2)


class Committed(unittest.TestCase):
    def test_cut_snapshots_the_committed_song_not_the_working_file(self):
        L.DATA = tempfile.mkdtemp()
        seen = []

        def render(pin, song, out):
            seen.append((os.path.basename(song), open(song, "rb").read()))
            fake_render(pin, song, out)
        snap = L.cut("chirpers9", "", render=render, canonical=lambda p, s: '{"tempo":1}', log=lambda *x: None)
        head = L.committed_text("songs/chirpers9-t1.yaml")
        self.assertTrue(seen[0][0].startswith(".listen-"))      # a temporary copy beside its includes
        self.assertEqual(seen[0][1], head)
        d = os.path.join(L.DATA, "chirpers9", "snapshots", snap["id"])
        self.assertEqual(open(os.path.join(d, "t01.song"), "rb").read(), head)
        self.assertFalse([f for f in os.listdir(os.path.join(L.ROOT, "songs")) if f.startswith(f".listen-{os.getpid()}")])


class Server(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = tempfile.mkdtemp()
        L.DATA = cls.d
        cls.snap = L.cut("chirpers9", "", render=fake_render, canonical=lambda p, s: '{"tempo":1}', log=lambda *x: None)
        cls.sent = []
        L.CODE = "solofury"
        L.notify = lambda album, note, track: cls.sent.append((note["n"], (track or {}).get("owner")))
        cls.srv = L.http.server.ThreadingHTTPServer(("127.0.0.1", 0), L.Handler)
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()
        cls.base = f"http://127.0.0.1:{cls.srv.server_address[1]}/"

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()
        cls.srv.server_close()

    def get(self, path, headers=None, code=True):
        h = {**({"X-Listen-Code": "solofury"} if code else {}), **(headers or {})}
        return urllib.request.urlopen(urllib.request.Request(self.base + path, headers=h))

    def post(self, path, body):
        req = urllib.request.Request(self.base + path, method="POST", data=json.dumps(body).encode(),
                                     headers={"X-Listen-Code": "solofury"})
        return json.load(urllib.request.urlopen(req))

    def test_app_api_notes_media_web(self):
        self.assertIn(b"chirpers studio", self.get("", code=False).read())          # the page itself needs no code
        albums = json.load(self.get("api/albums"))
        self.assertIn("chirpers9", [a["id"] for a in albums])
        self.assertEqual(len(next(a for a in albums if a["id"] == "chirpers9")["tracks"]), 8)
        t = self.snap["tracks"][-1]
        self.assertTrue(self.post("api/chirpers9/notes", {"snap": self.snap["id"], "n": t["n"], "t": 12.34,
                                                          "text": "the last chord", "by": "alex"})["ok"])
        d = json.load(self.get("api/chirpers9"))
        self.assertEqual([(n["n"], n["t"], n["text"], n["by"]) for n in d["notes"]], [(t["n"], 12.3, "the last chord", "alex")])
        self.assertEqual(self.sent[0], (t["n"], t["owner"]))
        r = self.get(f"media/chirpers9/{self.snap['id']}/t01.mp3", {"Range": "bytes=0-9"})
        self.assertEqual((r.status, len(r.read()), r.headers["Accept-Ranges"]), (206, 10, "bytes"))

        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *a, **k):
                return None
        try:
            urllib.request.build_opener(NoRedirect).open(urllib.request.Request(
                self.base + f"web/chirpers9/{self.snap['id']}/1", headers={"X-Listen-Code": "solofury"}))
            self.fail("expected a redirect")
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 302)
            self.assertEqual(L.from_hash(e.headers["Location"].split("#", 1)[1].join(["#", ""])), '{"tempo":1}')

    def test_access_code(self):
        for path in ("api/albums", "api/chirpers9", f"media/chirpers9/{self.snap['id']}/t01.mp3"):
            with self.assertRaises(urllib.error.HTTPError) as e:
                self.get(path, code=False)
            self.assertEqual(e.exception.code, 401)
        self.assertEqual(self.get("api/albums", {"Cookie": "a=b; listen_code=solofury"}, code=False).status, 200)
        with self.assertRaises(urllib.error.HTTPError):
            self.get("api/albums", {"Cookie": "listen_code=nope"}, code=False)

    def test_general_feedback_and_a_web_reply(self):
        r = self.post("api/chirpers9/notes", {"n": 0, "text": "the album breathes", "by": "Alex <b>"})
        self.post(f"api/chirpers9/notes/{r['id']}/reply", {"text": "thank you", "by": "harry"})
        n = next(x for x in json.load(self.get("api/chirpers9"))["notes"] if x["id"] == r["id"])
        self.assertEqual((n["n"], n["track"], n["by"], [(x["by"], x["text"]) for x in n["replies"]]),
                         (0, None, "Alex b", [("harry", "thank you")]))
        with self.assertRaises(urllib.error.HTTPError):
            self.post("api/chirpers9/notes/nonexistent/reply", {"text": "x"})

    def test_worklog(self):
        w = json.load(self.get("api/chirpers9/log"))
        self.assertEqual(len(w["tracks"]), 8)
        self.assertTrue(all(isinstance(t["log"], list) and isinstance(t["sections"], list) for t in w["tracks"]))
        self.assertTrue(w["features"] and all(f["pin"] for f in w["features"]))
        self.assertEqual([s["id"] for s in w["snapshots"]], [self.snap["id"]])


if __name__ == "__main__":
    unittest.main()
