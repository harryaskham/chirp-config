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
