import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import ytpub as Y  # noqa: E402


def test_chapters_start_at_zero_and_merge_short_ones():
    lines = Y.chapters([(0.4, "1. A"), (95.0, "2. B"), (99.0, "3. tiny"), (200.0, "4. C"), (3725.0, "5. D")])
    assert lines == ["00:00 1. A", "01:35 2. B", "03:20 4. C", "1:02:05 5. D"]


def test_chapters_need_three():
    assert Y.chapters([(0, "1. A"), (60, "2. B")]) == []


def test_only_originals_resolve():
    aid, meta, rdir = Y.resolve("chirpers5")
    assert aid == "chirpers5" and meta["album"] == "Soft Concrete" and rdir.endswith("Soft Concrete")
    assert Y.resolve("soft concrete")[0] == "chirpers5"
    with pytest.raises(SystemExit):
        Y.resolve("money")
    with pytest.raises(SystemExit):
        Y.resolve("obzen-t1")


def test_title_description_and_tags():
    meta = {"album": "The Endless Stair", "genre": "deep / heavy minimal house (mixtape)", "year": 2026}
    assert Y.video_title(meta, True) == "chirpers - The Endless Stair (continuous DJ mix)"   # lowercase in public
    assert len(Y.video_title({"album": "x" * 200}, False)) == 100
    d = Y.description(meta, {"target_lufs": -13.8}, ["00:00 1. A", "04:00 2. B", "08:00 3. C"], True)
    assert d.startswith("The Endless Stair by chirpers: an original deep / heavy minimal house (mixtape) album as one")
    assert "Written in Rust, note by note" in d and "no samples" in d and "AI" not in d and "Harry" not in d
    assert "\n00:00 1. A\n04:00 2. B\n08:00 3. C\n" in d and "-13.8 LUFS" in d and "\n\n\n" not in d
    t = Y.tags(meta)
    assert t[:2] == ["chirpers", "The Endless Stair"] and "deep" in t and "AI music" not in t and sum(len(x) + 2 for x in t) <= 480


def test_parse_code_url_and_next_offset():
    assert Y.parse_code_url("http://127.0.0.1:5555/?state=s1&code=4/abc&scope=x") == ("4/abc", "s1")
    assert Y.parse_code_url("  4/bare-code ") == ("4/bare-code", None)
    with pytest.raises(SystemExit):
        Y.parse_code_url("http://127.0.0.1:5555/?error=access_denied")
    assert Y.next_offset({"Range": "bytes=0-33554431"}) == 33554432
    assert Y.next_offset({}) == 0


def test_private_files_are_0600(tmp_path):
    p = tmp_path / "sub" / "token.json"
    Y.write_private(str(p), {"refresh_token": "x"})
    assert oct(os.stat(p).st_mode & 0o777) == "0o600" and json.load(open(p)) == {"refresh_token": "x"}


def test_upload_dry_run_is_private_and_labelled(tmp_path, monkeypatch, capsys):
    rdir = tmp_path / "Soft Concrete"
    (rdir / "youtube").mkdir(parents=True)
    (rdir / "youtube" / "meta.json").write_text(json.dumps({"title": "T", "tags": ["a"], "video": "video.mov", "thumbnail": "thumb.jpg"}))
    (rdir / "youtube" / "description.txt").write_text("D\n")
    monkeypatch.setattr(Y, "MUSIC", str(tmp_path))
    Y.main(["upload", "chirpers5", "--dry-run"])
    body = json.loads(capsys.readouterr().out)
    assert body["status"]["privacyStatus"] == "private" and body["status"]["containsSyntheticMedia"] is True
    assert body["status"]["selfDeclaredMadeForKids"] is False and body["snippet"]["categoryId"] == "10"


def test_video_type_and_peak(tmp_path):
    import subprocess
    assert Y.video_type("a/video.mov") == "video/quicktime" and Y.video_type("v.mp4") == "video/mp4"
    w = tmp_path / "tone.wav"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-f", "lavfi", "-i", "sine=frequency=440:duration=1",
                    "-af", "volume=-6dB", str(w)], check=True)
    assert -24.5 < Y.sample_peak_db(str(w)) < -23.5      # lavfi's sine is at 1/8 (-18 dBFS), then -6 dB


def test_peak_guard():
    assert Y.peak_ok(-0.36, -0.36) and Y.peak_ok(-0.9, -0.93) and Y.peak_ok(-1.5, -1.62)
    assert not Y.peak_ok(2.47, -1.62)        # the AAC overshoot this guard exists for
    assert not Y.peak_ok(-0.1, -0.6) and not Y.peak_ok(0.0, 0.2)


def test_banner_jpeg_is_16_9_and_small(tmp_path):
    from PIL import Image
    src = tmp_path / "b.png"
    Image.new("RGB", (3840, 2400), (10, 20, 40)).save(src)
    out = Y.banner_jpeg(str(src), str(tmp_path / "b.jpg"))
    im = Image.open(out)
    assert im.size == (2560, 1440) and os.path.getsize(out) < 6 * 1024 * 1024


def test_artist_is_lowercase_and_channel_match_ignores_case():
    assert Y.artist({"artist": "Chirpers"}) == "chirpers" and Y.artist({}) == "chirpers"
    assert Y.same_channel("Chirpers") and Y.same_channel(" chirpers ") and not Y.same_channel("Harry Askham")


def test_sync_problem_bounds():
    assert Y.sync_problem({"video": 0.0, "audio": 0.0, "fps": 30.0}) is None
    assert Y.sync_problem({"video": 0.016, "audio": 0.0, "fps": 30.0}) is None          # under half a frame
    assert "+20.0 ms" in Y.sync_problem({"video": 0.02, "audio": 0.0, "fps": 30.0})     # over half a frame at 30 fps
    assert "lacks" in Y.sync_problem({"video": 0.0})


def test_stream_starts_catches_an_offset_picture(tmp_path):
    import subprocess

    def mux(name, offset):
        p = tmp_path / name
        subprocess.run(["ffmpeg", "-loglevel", "error", "-itsoffset", str(offset), "-f", "lavfi", "-i",
                        "testsrc=size=64x64:rate=30:duration=1", "-f", "lavfi", "-i", "sine=frequency=440:duration=1",
                        "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le",
                        str(p)], check=True)
        return str(p)

    ok = Y.stream_starts(mux("ok.mov", 0))
    assert ok["fps"] == 30.0 and Y.sync_problem(ok) is None
    late = Y.stream_starts(mux("late.mov", 0.2))
    assert "+200.0 ms" in Y.sync_problem(late)


def test_concat_filter_joins_mp3s_sample_exactly_from_zero(tmp_path):
    """The kit's --video audio: each mp3 decoded alone and joined by the concat filter, restamped from 0, carries
    exactly the per-file decoded samples (the concat demuxer kept a 23 ms priming start and lost samples, 4 Nov)."""
    import subprocess
    files = []
    for i, secs in enumerate((1.3, 0.7, 1.1)):
        p = tmp_path / f"{i}.mp3"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-f", "lavfi", "-i", f"sine=frequency={300 + 100 * i}:duration={secs}",
                        "-ar", "48000", "-c:a", "libmp3lame", "-b:a", "192k", str(p)], check=True)
        files.append(str(p))
    each = sum(Y.ffprobe_dur(f) for f in files)
    out = tmp_path / "k.mov"
    cmd = ["ffmpeg", "-loglevel", "error", "-f", "lavfi", "-i", "testsrc=size=64x64:rate=30:duration=3.1"]
    for f in files:
        cmd += ["-i", f]
    graph = "".join(f"[{i + 1}:a]" for i in range(len(files))) + f"concat=n={len(files)}:v=0:a=1,asetpts=N/SR/TB[a]"
    cmd += ["-filter_complex", graph, "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-c:a", "pcm_s24le", "-ar", "48000", str(out)]
    subprocess.run(cmd, check=True)
    assert abs(Y.audio_seconds(str(out)) - each) < 0.001
    assert Y.stream_starts(str(out))["audio"] == 0.0


# ---------- uploads that last hours (11 Nov: a 4K60 album) ----------

class FakeYouTube:
    """A resumable session: POST opens it, PUT takes bytes (or a status query), with scripted trouble on the way."""

    def __init__(self, size, trouble=()):
        self.size, self.got, self.trouble = size, 0, list(trouble)
        self.posts, self.tokens, self.puts = 0, [], 0

    def __call__(self, method, url, token, body=None, ctype="application/json", headers=None):
        self.tokens.append(token)
        if method == "POST":
            self.posts += 1
            return 200, {"Location": "https://upload.example/session-1"}, {}
        rng = headers["Content-Range"]
        if rng.startswith("bytes */"):                       # how far did you get?
            if url != "https://upload.example/session-1":
                return 404, {}, {}
            return (200, {}, {"id": "VID"}) if self.got == self.size else (308, self._range(), b"")
        self.puts += 1
        if self.trouble:
            what = self.trouble.pop(0)
            if what == "net":
                raise OSError("connection reset")
            if what == "half":                               # the chunk arrived, the answer did not
                self.got += len(body)
                raise OSError("timed out")
            if what:
                return what, {}, {"error": what}
        start = int(rng.split()[1].split("-")[0])
        assert start == self.got, f"chunk starts at {start}, the session has {self.got}"
        self.got += len(body)
        return (200, {}, {"id": "VID"}) if self.got == self.size else (308, self._range(), b"")

    def _range(self):
        return {"Range": f"bytes=0-{self.got - 1}"} if self.got else {}


def _upload(tmp_path, monkeypatch, yt, size=1000, **kw):
    f = tmp_path / "video.mov"
    f.write_bytes(bytes(range(256)) * 4 if size == 1024 else b"x" * size)
    monkeypatch.setattr(Y, "CHUNK", 256)
    monkeypatch.setattr(Y, "call", yt)
    monkeypatch.setattr(Y.time, "sleep", lambda s: None)
    return Y.resumable_upload("tok0", str(f), {"snippet": {}}, log=lambda m: None, **kw)


def test_upload_goes_through_in_chunks(tmp_path, monkeypatch):
    yt = FakeYouTube(1000)
    assert _upload(tmp_path, monkeypatch, yt) == {"id": "VID"}
    assert (yt.posts, yt.puts, yt.got) == (1, 4, 1000)


def test_upload_survives_network_errors_and_5xx(tmp_path, monkeypatch):
    yt = FakeYouTube(1000, trouble=[None, "net", 503, "half", None])
    assert _upload(tmp_path, monkeypatch, yt) == {"id": "VID"}
    assert yt.got == 1000 and yt.posts == 1, "the same session, every byte once"


def test_upload_renews_the_token_on_401_and_by_age(tmp_path, monkeypatch):
    n = {"i": 0}

    def fresh():
        n["i"] += 1
        return f"tok{n['i']}"

    yt = FakeYouTube(1000, trouble=[None, 401])
    assert _upload(tmp_path, monkeypatch, yt, fresh=fresh) == {"id": "VID"}
    assert n["i"] == 1 and yt.tokens[-1] == "tok1" and yt.got == 1000
    yt = FakeYouTube(1000)
    monkeypatch.setattr(Y, "TOKEN_LIFE", -1)                 # every request is "an hour later"
    assert _upload(tmp_path, monkeypatch, yt, fresh=fresh) == {"id": "VID"}
    assert "tok0" not in yt.tokens


def test_upload_gives_up_after_many_failures_in_a_row(tmp_path, monkeypatch):
    yt = FakeYouTube(1000, trouble=[503] * 40)
    with pytest.raises(SystemExit) as e:
        _upload(tmp_path, monkeypatch, yt)
    assert "run the upload again to resume" in str(e.value)


def test_a_second_run_resumes_the_saved_session(tmp_path, monkeypatch):
    seen = {}
    yt = FakeYouTube(1000, trouble=[None, None] + [503] * 40)
    with pytest.raises(SystemExit):
        _upload(tmp_path, monkeypatch, yt, on_session=seen.update)
    assert seen == {"location": "https://upload.example/session-1", "size": 1000} and yt.got == 512
    yt.trouble = []
    assert _upload(tmp_path, monkeypatch, yt, session=seen) == {"id": "VID"}
    assert yt.posts == 1 and yt.got == 1000, "no new session, only the missing bytes"


def test_a_session_for_another_size_or_a_dead_one_starts_again(tmp_path, monkeypatch):
    yt = FakeYouTube(1000)
    assert _upload(tmp_path, monkeypatch, yt, session={"location": "https://upload.example/session-1", "size": 999}) == {"id": "VID"}
    assert yt.posts == 1
    yt = FakeYouTube(1000)
    assert _upload(tmp_path, monkeypatch, yt, session={"location": "https://upload.example/gone", "size": 1000}) == {"id": "VID"}
    assert yt.posts == 1 and yt.got == 1000


def test_a_ready_made_thumbnail_must_be_wide_and_becomes_1280x720(tmp_path):
    from PIL import Image
    Image.new("RGB", (3000, 3000)).save(tmp_path / "sq.png")
    Image.new("RGB", (2560, 1440), (9, 40, 90)).save(tmp_path / "wide.png")
    out = Y.ready_thumb(str(tmp_path / "wide.png"), str(tmp_path / "thumb.jpg"))
    assert Image.open(out).size == (1280, 720) and os.path.getsize(out) < 2_000_000
    with pytest.raises(SystemExit) as e:
        Y.ready_thumb(str(tmp_path / "sq.png"), str(tmp_path / "t2.jpg"))
    assert "not 16:9" in str(e.value)
