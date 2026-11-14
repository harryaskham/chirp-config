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
import time
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


class Questions(unittest.TestCase):
    ASK = {"op": "ask", "id": "q1", "at": "2026-11-14T09:00:00Z", "by": "chirper-zero", "n": 2, "track_title": "Odd Sympathy",
           "version": "v5", "key": "words", "title": "Can you make out the words?", "choices": ["Yes", "Some", "No"], "media": []}

    def test_the_event_log_folds_into_questions(self):
        ev = [self.ASK,
              {"op": "answer", "id": "q1", "at": "2026-11-14T10:00:00Z", "by": "Harry", "choice": "Some", "text": ""},
              {"op": "answer", "id": "q1", "at": "2026-11-14T10:01:00Z", "by": "alex", "choice": "", "text": "only the first line"},
              {"op": "answer", "id": "q1", "at": "2026-11-14T10:02:00Z", "by": "harry", "choice": "No", "text": "the band covers them"},
              {"op": "answer", "id": "nope", "at": "2026-11-14T10:03:00Z", "by": "harry", "choice": "Yes"},
              {"op": "told", "at": "2026-11-14T10:04:00Z", "answers": [["q1", "alex", "2026-11-14T10:01:00Z"],
                                                                         ["q1", "harry", "2026-11-14T10:00:00Z"]]}]
        (q,) = L.reduce_questions(ev)
        self.assertEqual(sorted(q["answers"]), ["alex", "harry"])                     # each person's latest, whatever the case
        self.assertEqual((q["answers"]["harry"]["choice"], q["answers"]["harry"]["text"]), ("No", "the band covers them"))
        self.assertTrue(q["answers"]["alex"]["told"])
        self.assertFalse(q["answers"]["harry"]["told"])                               # he changed it after that one was sent
        self.assertEqual([(x["id"], a["by"]) for x, a in L.untold([q])], [("q1", "harry")])
        self.assertIsNone(q["retired"])

    def test_a_new_version_of_the_same_passage_replaces_the_question(self):
        newer = {**self.ASK, "id": "q2", "at": "2026-11-14T11:00:00Z", "version": "v7"}
        other = {**self.ASK, "id": "q3", "at": "2026-11-14T11:30:00Z", "key": "", "title": "Another"}
        qs = L.reduce_questions([self.ASK, newer, other, {"op": "retire", "id": "q3", "at": "2026-11-14T12:00:00Z", "reason": "moot"}])
        self.assertEqual([(q["id"], (q["retired"] or {}).get("reason")) for q in qs],
                         [("q1", "replaced by q2"), ("q2", None), ("q3", "moot")])

    def test_the_digest_carries_every_answer_verbatim(self):
        q = L.reduce_questions([self.ASK, {"op": "answer", "id": "q1", "at": "2026-11-14T10:00:00Z", "by": "harry", "choice": "Some",
                                           "text": "first line yes; \"between us moves\" is lost"}])[0]
        text = L.digest_text("chirpers10", L.untold([q]), public="http://x/")
        self.assertIn("HARRY ANSWERED 1 QUESTION on the review page (chirpers10)", text)
        self.assertIn("1. [Odd Sympathy v5] Can you make out the words?   (asked by chirper-zero, id q1)", text)
        self.assertIn("   harry chose: Some", text)
        self.assertIn('   harry wrote: first line yes; "between us moves" is lost', text)
        self.assertIn("http://x/#a=chirpers10&v=questions", text)

    def test_where_a_file_of_takes_is_cut(self):
        # two takes of 18.9 s with 0.8 s between; a breath inside the first take is not the boundary
        self.assertEqual(L.split_points([(7.0, 7.4), (18.9, 19.7)], 38.6, 2), [(0.0, 18.9), (19.7, 38.6)])
        self.assertEqual(L.split_points([(6.5, 7.2), (13.7, 14.4)], 20.9, 3), [(0.0, 6.5), (7.2, 13.7), (14.4, 20.9)])
        # the silence a file closes (or opens) with is no take's: "record, then ours" with 0.7 s after each
        self.assertEqual(L.split_points([(6.5, 7.2), (13.7, 14.4)], 14.4, 2), [(0.0, 6.5), (7.2, 13.7)])
        self.assertEqual(L.split_points([(0.0, 1.0), (9.0, 9.8), (17.8, 18.6)], 18.6, 2), [(1.0, 9.0), (9.8, 17.8)])
        self.assertIsNone(L.split_points([(3.0, 4.4), (7.6, 8.6), (30.0, 31.0)], 49.7, 2))    # nothing near the middle
        self.assertIsNone(L.split_points([], 30.0, 2))
        made = []

        def run(cmd, check):
            made.append((cmd[cmd.index("-ss") + 1], cmd[cmd.index("-t") + 1], cmd[-1]))
        lens = L.cut_parts("ab.mp3", ["a.mp3", "b.mp3"], probe=lambda p: (38.6, [(18.9, 19.7)]), run=run)
        self.assertEqual(lens, [18.9, 18.9])
        self.assertEqual(made, [("0.000", "18.900", "a.mp3"), ("19.700", "18.900", "b.mp3")])
        self.assertIsNone(L.cut_parts("x.mp3", ["a.mp3", "b.mp3"], probe=lambda p: (30.0, []), run=run))

    def test_ask_keeps_its_own_copies_of_the_clips(self):
        d = tempfile.mkdtemp()
        old, L.DATA = L.DATA, d
        self.addCleanup(setattr, L, "DATA", old)
        clip = os.path.join(d, "voice alone.mp3")
        with open(clip, "wb") as f:
            f.write(b"ID3clip")

        def cut(path, outs):
            for o in outs:
                with open(o, "wb") as f:
                    f.write(b"part")
            return [18.9, 18.95]
        q = L.ask("chirpers9", 2, " Does it lift? ", "the key change", "v4", "lift", [("v3 | v4", clip)], [("the voice alone", clip)],
                  ["Yes", "", "No"], 61.24, by="chirper-zero", cut=cut)
        self.assertEqual((q["title"], q["n"], q["track"], q["choices"], q["t"], q["by"]),
                         ("Does it lift?", 2, "chirpers9-t2", ["Yes", "No"], 61.2, "chirper-zero"))
        self.assertTrue(q["track_title"])
        pair, single = q["media"]
        self.assertEqual((pair["sync"], [i["label"] for i in pair["items"]], [i["secs"] for i in pair["items"]]),
                         (True, ["v3", "v4"], [18.9, 18.95]))
        self.assertEqual((single["sync"], single["items"][0]["label"]), (False, "the voice alone"))
        for g in q["media"]:
            for it in g["items"]:
                self.assertRegex(it["src"], r"^q[0-9a-f]{7}-\w+\.mp3$")
                self.assertTrue(os.path.exists(os.path.join(d, "chirpers9", "questions", it["src"])))
        self.assertEqual([x["id"] for x in L.questions("chirpers9")], [q["id"]])
        uneven = L.ask("chirpers9", 0, "And the album?", abs_=[("a|b", clip)], cut=lambda p, o: [10.0, 14.0], by="chirp-eco")
        self.assertEqual((uneven["n"], uneven["track"], uneven["media"][0]["sync"]), (0, None, False))
        for kw, said in (({"title": " "}, "needs a title"), ({"n": 99}, "has no track 99"),
                         ({"clips": [("x", "/nonexistent.mp3")]}, "no clip"), ({"abs_": [("only one", clip)]}, "--ab wants"),
                         ({"abs_": [("a|b", clip)], "cut": lambda p, o: None}, "no silence where 2 takes")):
            with self.assertRaises(ValueError) as e:
                L.ask(**{"album": "chirpers9", "n": 1, "title": "t", **kw})
            self.assertIn(said, str(e.exception))

    def test_answers_go_out_once_as_one_message_each(self):
        d = tempfile.mkdtemp()
        old, L.DATA = L.DATA, d
        self.addCleanup(setattr, L, "DATA", old)
        a = L.ask("chirpers9", 1, "First?", by="chirper-zero", choices=["Yes", "No"])
        b = L.ask("chirpers9", 2, "Second?", by="chirper-zero")
        c = L.ask("chirpers9", 3, "Third?", by="chirp-eco")
        for q, choice, text in ((a, "Yes", ""), (b, "", "a hole"), (c, "", "fine")):
            L.question_event("chirpers9", {"op": "answer", "id": q["id"], "at": L.now_iso(), "by": "harry", "choice": choice,
                                           "text": text})
        sent = []

        def send(target, body):
            sent.append((target, body))
            return target != "broken", "ok"
        self.assertEqual(L.send_digest("chirpers9", send), 3)
        zero, eco = L.AGENTS["chirper-zero"], L.AGENTS["chirp-eco"]
        self.assertEqual([t for t, _ in sent], [zero, eco])                           # one each; eco's own question rides in its copy
        self.assertIn("ANSWERED 2 QUESTIONS", sent[0][1])
        self.assertIn("harry wrote: a hole", sent[0][1])
        self.assertNotIn("Third?", sent[0][1])
        self.assertIn("ANSWERED 3 QUESTIONS", sent[1][1])
        self.assertEqual(L.send_digest("chirpers9", send), 0)                         # nothing is sent twice
        self.assertEqual(len(sent), 2)
        L.question_event("chirpers9", {"op": "answer", "id": a["id"], "at": "2026-11-14T23:59:59Z", "by": "harry", "choice": "No",
                                       "text": ""})
        with open(os.path.join(d, "agents.json"), "w") as f:
            json.dump({"chirper-zero": "broken"}, f)
        self.assertEqual(L.send_digest("chirpers9", send), 0)                         # the asker's message failed: it stays owed
        self.assertEqual([(q["id"], x["choice"]) for q, x in L.untold(L.questions("chirpers9"))], [(a["id"], "No")])


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
        t0 = time.time()
        L.videos("chirpers9", a["id"], {1}, "{id}|accretion3d", log=quiet, run=run)
        made = os.path.getmtime(os.path.join(d, "t01.mp4"))
        self.assertLessEqual(made, t0 + 1)                                                    # stamped at its start
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

    def test_lod_is_opt_in_and_probed_on_the_pin(self):
        """chirp-video's batch 49: `chirp video --lod` draws a 480p preview at 480p detail (not the film's look), so
        previews ask for it only with videos(lod=True) / --lod, and only when the pin's help has it."""
        d = tempfile.mkdtemp()
        for name, text in (("old", "Usage: chirp video [OPTIONS]\n      --size <WxH>\n"),
                           ("new", "Usage: chirp video [OPTIONS]\n      --lod   Detail follows the picture's size\n")):
            p = os.path.join(d, name)
            with open(p, "w") as f:
                f.write("#!/bin/sh\ncat <<'X'\n" + text + "X\n")
            os.chmod(p, 0o755)
        L._LOD.clear()
        self.assertEqual(L.lod_args(os.path.join(d, "old")), [])
        self.assertEqual(L.lod_args(os.path.join(d, "new")), ["--lod"])
        self.assertEqual(L.lod_args(os.path.join(d, "missing")), [])
        snap = L.cut("chirpers9", "", render=fake_render, canonical=lambda p, s: '{"tempo":1}', log=lambda *x: None)
        calls = []

        def run(cmd, **kw):
            calls.append(cmd)
            open(cmd[-1], "wb").write(b"mp4")
            return type("R", (), {"returncode": 0, "stderr": ""})()
        orig = L.read_text
        try:
            L.read_text = lambda p: os.path.join(d, "new") if p.endswith("groove-pin") else orig(p)
            L.videos("chirpers9", snap["id"], {1}, "accretion", log=lambda *x: None, run=run)             # the film's detail
            L.videos("chirpers9", snap["id"], {1}, "accretion", log=lambda *x: None, run=run, redo=True, lod=True)
        finally:
            L.read_text = orig
        self.assertEqual(["--lod" in c for c in calls], [False, True])

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


class FirstVersion(unittest.TestCase):
    def test_a_first_version_still_being_written_is_left_out_of_a_cut(self):
        self.assertTrue(L.at_head("songs/chirpers9-t1.yaml"))
        self.assertFalse(L.at_head("songs/no-such-song-in-head.yaml"))
        kept = [{"kept": True, "version": "v1"}]
        self.assertTrue(L.first_version_pending("songs/no-such-song-in-head.yaml", []))      # untracked, never kept
        self.assertFalse(L.first_version_pending("songs/no-such-song-in-head.yaml", kept))   # kept once: its text is cut
        self.assertFalse(L.first_version_pending("songs/chirpers9-t1.yaml", []))             # committed: HEAD's text is cut
        self.assertTrue(L.first_version_pending("x", [], tracked=False))
        self.assertFalse(L.first_version_pending("x", [], tracked=True))


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

    def test_questions_are_asked_answered_and_served(self):
        clip = os.path.join(self.d, "c.mp3")
        with open(clip, "wb") as f:
            f.write(b"0123456789abcdef")
        scheduled = []
        old = L.schedule_digest
        L.schedule_digest = lambda album, quiet=None: scheduled.append(album)
        self.addCleanup(setattr, L, "schedule_digest", old)
        q = L.ask("chirpers9", 1, "A breath or a hole?", clips=[("the break", clip)], choices=["A breath", "A hole"], by="chirper-zero")
        gone = L.ask("chirpers9", 1, "Old one", by="chirper-zero")
        L.question_event("chirpers9", {"op": "retire", "id": gone["id"], "at": L.now_iso(), "reason": "moot"})
        src = q["media"][0]["items"][0]["src"]
        r = self.get(f"media/chirpers9/q/{src}", {"Range": "bytes=4-7"})
        self.assertEqual((r.status, r.read(), r.headers["Content-Type"]), (206, b"4567", "audio/mpeg"))
        with self.assertRaises(urllib.error.HTTPError) as e:
            self.get(f"media/chirpers9/q/{src}", code=False)
        self.assertEqual(e.exception.code, 401)
        self.assertTrue(self.post(f"api/chirpers9/questions/{q['id']}/answer", {"choice": "A breath", "by": "Harry"})["ok"])
        self.assertTrue(self.post(f"api/chirpers9/questions/{q['id']}/answer",
                                  {"choice": "A hole", "text": "it drops out", "by": "Harry"})["ok"])
        self.assertTrue(self.post(f"api/chirpers9/questions/{q['id']}/answer", {"text": "a breath for me", "by": "Alex"})["ok"])
        self.assertEqual(scheduled, ["chirpers9"] * 3)
        got = {x["id"]: x for x in json.load(self.get("api/chirpers9"))["questions"]}
        self.assertEqual({k: (v["choice"], v["text"]) for k, v in got[q["id"]]["answers"].items()},
                         {"harry": ("A hole", "it drops out"), "alex": ("", "a breath for me")})
        self.assertEqual(got[gone["id"]]["retired"]["reason"], "moot")
        for path, body in ((f"api/chirpers9/questions/{q['id']}/answer", {"choice": "Neither"}),
                           (f"api/chirpers9/questions/{q['id']}/answer", {"choice": "", "text": " "}),
                           (f"api/chirpers9/questions/{gone['id']}/answer", {"text": "x"}),
                           ("api/chirpers9/questions/qnone/answer", {"text": "x"})):
            with self.assertRaises(urllib.error.HTTPError) as e:
                self.post(path, body)
            self.assertEqual(e.exception.code, 400)

    def test_the_question_commands(self):
        import contextlib
        import io
        clip = os.path.join(self.d, "k.mp3")
        with open(clip, "wb") as f:
            f.write(b"x")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            L.main(["ask", "chirpers9", "--track", "3", "--title", "Thrill or mistake?", "--version", "v8", "--key", "slip", "--at", "53",
                    "--clip", f"the slip={clip}", "--choice", "A thrill", "--choice", "A mistake", "--by", "chirper-zero"])
        qid = out.getvalue().split("question ")[1].split()[0]
        self.assertIn(f"#a=chirpers9&v=questions&q={qid}", out.getvalue())
        q = next(x for x in L.questions("chirpers9") if x["id"] == qid)
        self.assertEqual((q["n"], q["version"], q["key"], q["t"], q["choices"], q["media"][0]["items"][0]["label"]),
                         (3, "v8", "slip", 53.0, ["A thrill", "A mistake"], "the slip"))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            L.main(["questions", "chirpers9", "--track", "3", "--open"])
        self.assertIn(f"[{qid}] t3 v8 (chirper-zero,", out.getvalue())
        self.assertIn("OPEN\n    Thrill or mistake?", out.getvalue())
        with contextlib.redirect_stdout(io.StringIO()):
            L.main(["retire", "chirpers9", qid, "--reason", "rewritten"])
        self.assertEqual(next(x for x in L.questions("chirpers9") if x["id"] == qid)["retired"]["reason"], "rewritten")
        for argv, said in ((["retire", "chirpers9", qid], "no open question"),
                           (["ask", "chirpers9", "--title", "t", "--clip", "nolabel"], "wants LABEL=FILE"),
                           (["ask", "chirpers9", "--title", "t", "--track", "77"], "has no track 77")):
            with self.assertRaises(SystemExit) as e:
                L.main(argv)
            self.assertIn(said, str(e.exception))

    def test_worklog(self):
        w = json.load(self.get("api/chirpers9/log"))
        self.assertEqual(len(w["tracks"]), 8)
        self.assertTrue(all(isinstance(t["log"], list) and isinstance(t["sections"], list) for t in w["tracks"]))
        self.assertTrue(w["features"] and all(f["pin"] for f in w["features"]))
        self.assertEqual([s["id"] for s in w["snapshots"]], [self.snap["id"]])


if __name__ == "__main__":
    unittest.main()
