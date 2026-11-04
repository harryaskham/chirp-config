#!/usr/bin/env python3
"""Publish released original Chirpers albums to the Chirpers YouTube channel (Harry, 1 Nov: "let's do YouTube").

Only ORIGINAL albums (compose/chirpersN, released by `chirpers.py release`) are publishable; reproductions of other
artists' songs never are. One video per album: the cover on a blurred field over the whole album (or its continuous
DJ mix when the release has one), with YouTube chapters for the tracks, an honest AI/synthesis note, and a thumbnail.

    ytpub.py auth [--finish URL]     one-time consent; choose the CHIRPERS channel in Google's account chooser
    ytpub.py whoami                  the authorised channel
    ytpub.py list                    original albums, release and upload state
    ytpub.py kit ALBUM [--tracks]    build ~/Music/Chirpers/<album>/youtube/ (video.mp4, description.txt, thumb.jpg)
    ytpub.py kit ALBUM --video FILE  the same with a ready-made album video (chirp video) in place of the cover still
    ytpub.py upload ALBUM [--privacy private|unlisted|public] [--dry-run]
    ytpub.py publish ALBUM [--privacy public]
    ytpub.py update ALBUM [--dry-run]  re-push an uploaded video's title, description and tags
    ytpub.py channel [--description-file F] [--keywords K] [--banner IMG]   the channel's About text, keywords, banner

ALBUM is an album id (chirpers5) or its name. Uploads default to PRIVATE so Harry reviews before anything is public.
Credentials live outside the config repo in ~/.config/chirp-youtube/ (client_secret.json from gws's OAuth client,
token.json written by `auth`, both mode 600); only plain HTTPS is used, no Google client libraries.
"""
import argparse
import base64
import hashlib
import http.server
import json
import os
import re
import secrets
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CRED_DIR = os.path.expanduser(os.environ.get("CHIRP_YOUTUBE_DIR", "~/.config/chirp-youtube"))
MUSIC = os.path.expanduser(os.environ.get("CHIRP_RELEASE_DIR", "~/Music/Chirpers"))
SCOPES = ["https://www.googleapis.com/auth/youtube"]       # upload, thumbnails and the later privacy change
CHANNEL_TITLE = os.environ.get("CHIRP_YOUTUBE_CHANNEL", "chirpers")   # styled lowercase in public (Harry, 1 Nov)
API = "https://www.googleapis.com/youtube/v3"
UPLOAD = "https://www.googleapis.com/upload/youtube/v3"
CHUNK = 32 * 1024 * 1024                                   # a multiple of 256 KiB, as resumable uploads require
ORIGINAL = re.compile(r"^chirpers\d+$")


# ---------- albums ----------

def album_ids():
    d = os.path.join(ROOT, "compose")
    return sorted((x for x in os.listdir(d) if ORIGINAL.match(x) and os.path.exists(os.path.join(d, x, "album.json"))),
                  key=lambda x: int(x[8:]))


def safe_name(name):
    return "".join(ch for ch in name if ch not in '/\\:*?"<>|')


def resolve(album):
    """(album id, album.json, release dir) for an original album id or name; exits for anything else."""
    for aid in album_ids():
        meta = json.load(open(os.path.join(ROOT, "compose", aid, "album.json")))
        if album in (aid, meta.get("album")) or album.lower() == str(meta.get("album", "")).lower():
            return aid, meta, os.path.join(MUSIC, safe_name(meta["album"]))
    sys.exit(f"ytpub: {album!r} is not an original Chirpers album (compose/chirpersN); only originals are published")


def release_of(rdir):
    p = os.path.join(rdir, "release.json")
    return json.load(open(p)) if os.path.exists(p) else None


def stamp(t):
    t = int(t)
    h, m, s = t // 3600, t // 60 % 60, t % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def chapters(starts):
    """YouTube chapter lines from [(start seconds, label)]: the first must be 00:00, there must be at least three and
    each at least 10 s long, so a too-short one is merged into the one before it."""
    out = []
    for t, label in sorted(starts):
        if out and t - out[-1][0] < 10:
            continue
        out.append((0.0 if not out else t, label))
    return [f"{stamp(t)} {label}" for t, label in out] if len(out) >= 3 else []


def artist(meta):
    """The band name as styled in public: lowercase chirpers (Harry, 1 Nov), whatever album.json says."""
    return str(meta.get("artist") or "chirpers").lower()


def same_channel(title):
    return str(title or "").strip().lower() == CHANNEL_TITLE.strip().lower()


def video_title(meta, mix):
    t = f"{artist(meta)} - {meta['album']} ({'continuous DJ mix' if mix else 'full album'})"
    return t[:100]


def description(meta, rel, chaps, mix):
    genre = meta.get("genre", "electronic")
    lines = [f"{meta['album']} by {artist(meta)}: an original {genre} album{' as one continuous DJ mix' if mix else ''}"
             f" ({meta.get('year', '')}).".replace(" ()", ""), "",
             # Harry, 1 Nov: the tracks are composed, not prompted; no need to lead with "AI" everywhere, and it is
             # fairer (technically) to say they are written in Rust. No personal names in public text.
             "Written in Rust, note by note, and synthesized from scratch: no samples, no loops, no recordings.",
             ""]
    lines += chaps
    lines += ["", f"Mastered to {rel.get('target_lufs')} LUFS." if rel.get("target_lufs") is not None else "",
              "#chirpers #electronicmusic #" + re.sub(r"[^a-z0-9]", "", genre.split("/")[0].lower() or "electronic")]
    return "\n".join(x for i, x in enumerate(lines) if x or (i and lines[i - 1])).strip()[:4900]


def tags(meta):
    words = [artist(meta), meta["album"], "electronic music", "synthesized", "written in Rust"]
    words += [g.strip() for g in re.split(r"[/,]", meta.get("genre", "")) if g.strip()]
    out, n = [], 0
    for w in words:
        if n + len(w) + 2 > 480:
            break
        out.append(w)
        n += len(w) + 2
    return out


# ---------- the kit ----------

def ffprobe_dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


# A ready-made album video must last as long as the release program to within ~3 frames (Harry, 4 Nov: "make sure
# the video is in perfect sync"); the still-cover kit needs no such bound.
VIDEO_SYNC_S = 0.1


def stream_starts(path):
    """{'video': start s, 'audio': start s, 'fps': frame rate} of a file's first video and audio streams."""
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,start_time,r_frame_rate",
                        "-of", "json", path], capture_output=True, text=True)
    out = {}
    for s in json.loads(r.stdout or "{}").get("streams", []):
        kind = s.get("codec_type")
        if kind not in ("video", "audio") or kind in out:
            continue
        st = s.get("start_time")
        out[kind] = float(st) if st not in (None, "N/A") else 0.0
        if kind == "video":
            num, _, den = (s.get("r_frame_rate") or "30/1").partition("/")
            out["fps"] = float(num) / float(den) if den and float(den) else 30.0
    return out


def sync_problem(starts):
    """None when the picture and the audio start within half a frame of each other, else why not."""
    if "video" not in starts or "audio" not in starts:
        return "it lacks a video or an audio stream"
    off = starts["video"] - starts["audio"]
    if abs(off) > 0.5 / (starts.get("fps") or 30.0):
        return f"its picture starts {off * 1000:+.1f} ms from its audio (more than half a frame)"
    return None


def sample_peak_db(path):
    """The decoded audio's sample peak in dBFS (streamed, so long mixes stay small in memory)."""
    import numpy as np
    p = subprocess.Popen(["ffmpeg", "-nostats", "-loglevel", "error", "-i", path, "-map", "0:a", "-f", "f32le", "-"],
                         stdout=subprocess.PIPE)
    peak = 0.0
    while True:
        b = p.stdout.read(1 << 22)
        if not b:
            break
        peak = max(peak, float(np.abs(np.frombuffer(b[:len(b) // 4 * 4], dtype="<f4")).max(initial=0.0)))
    p.wait()
    return 20 * np.log10(max(peak, 1e-9))


def peak_ok(peak, source_peak):
    """The video may not clip, nor add more than 0.3 dB of overshoot to the release files it carries (MP3 decoding
    already overshoots a little: Phantom Downbeat's track 3 peaks at -0.36 dBFS; ffmpeg's AAC added ~4 dB)."""
    return peak < 0.0 and peak <= source_peak + 0.3


def video_type(path):
    return "video/quicktime" if path.endswith(".mov") else "video/mp4"


def frame_and_thumb(cover, out_dir):
    """A 1920x1080 frame (the cover at its own size over a blurred, darkened copy) and a 1280x720 JPEG thumbnail."""
    from PIL import Image, ImageFilter, ImageEnhance
    im = Image.open(cover).convert("RGB")
    paths = []
    for (w, h), name in (((1920, 1080), "frame.png"), ((1280, 720), "thumb.jpg")):
        side = min(h, im.width)
        scale = max(w / im.width, h / im.height)
        bg = im.resize((int(im.width * scale) + 1, int(im.height * scale) + 1), Image.LANCZOS)
        bg = bg.crop(((bg.width - w) // 2, (bg.height - h) // 2, (bg.width - w) // 2 + w, (bg.height - h) // 2 + h))
        bg = ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(40))).enhance(0.45)
        fg = im.resize((side, side), Image.LANCZOS) if side != im.width else im
        if fg.height > h:
            fg = fg.resize((h, h), Image.LANCZOS)
        bg.paste(fg, ((w - fg.width) // 2, (h - fg.height) // 2))
        p = os.path.join(out_dir, name)
        bg.save(p, quality=90) if name.endswith(".jpg") else bg.save(p)
        paths.append(p)
    return paths


def program(rel, rdir, force_tracks=False):
    """(audio files, chapter lines, is_mix) for a release: its continuous mix when it has one, else the tracks back to
    back. Shared by kit (the video) and update (the text of an uploaded video), so the chapters always agree."""
    mix = (rel.get("mix") or {}) if not force_tracks else {}
    if mix.get("file") and os.path.exists(os.path.join(rdir, mix["file"])):
        return ([os.path.join(rdir, mix["file"])], chapters([(x["start"], f"{x['n']}. {x['title']}") for x in mix["tracklist"]]),
                True)
    audio, starts, t = [], [], 0.0
    for tr in sorted(rel["tracks"], key=lambda x: x["n"]):
        if not tr.get("file"):
            continue
        p = os.path.join(rdir, tr["file"])
        audio.append(p)
        starts.append((t, f"{tr['n']}. {tr['title']}"))
        t += ffprobe_dur(p)
    return audio, chapters(starts), False


def build_kit(aid, meta, rdir, force_tracks=False, video_file=None):
    rel = release_of(rdir)
    if not rel:
        sys.exit(f"ytpub: {meta['album']} has no release in {rdir}; run chirpers.py release {aid} first")
    out = os.path.join(rdir, "youtube")
    os.makedirs(out, exist_ok=True)
    cover = os.path.join(ROOT, (meta.get("art") or {}).get("file", ""))
    if not os.path.isfile(cover):
        sys.exit(f"ytpub: {aid} has no cover art (album.json art.file)")
    frame, thumb = frame_and_thumb(cover, out)
    audio, chaps, is_mix = program(rel, rdir, force_tracks)
    video = os.path.join(out, "video.mov")
    listfile = os.path.join(out, "audio.txt")
    with open(listfile, "w") as f:
        f.write("".join("file '" + p.replace("'", "'\\''") + "'\n" for p in audio))
    cmd = ["nice", "-n", "15", "ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", "24", "-i", frame,
           "-f", "concat", "-safe", "0", "-i", listfile, "-map", "0:v", "-map", "1:a", "-c:v", "libx264",
           "-preset", "veryfast", "-tune", "stillimage", "-crf", "20", "-pix_fmt", "yuv420p", "-threads", "2",
           "-c:a", "pcm_s24le", "-ar", "48000", "-shortest", video]
    if video_file:
        # a ready-made album video (`chirp video --album`, 4 Nov) in place of the cover still: its picture is copied as
        # is and the release's own audio laid under it, as for the still, so the upload carries exactly the release
        # audio and the chapters land. It must last as long as the program.
        vd, ad = ffprobe_dur(video_file), sum(ffprobe_dur(p) for p in audio)
        if abs(vd - ad) > VIDEO_SYNC_S:
            os.remove(listfile)
            sys.exit(f"ytpub: {video_file} lasts {vd:.3f} s but the release program {ad:.3f} s ({vd - ad:+.3f} s, over "
                     f"{VIDEO_SYNC_S} s); render it from this release")
        cmd = ["nice", "-n", "15", "ffmpeg", "-y", "-loglevel", "error"]
        # chirp video's mp4 starts its picture 21.4 ms late (AAC's 1025-sample priming shifts the mux, 4 Nov); its
        # frames are drawn on the audio's own timeline, so frame 0 belongs at 0 under the release audio: shift it back.
        vstart = stream_starts(video_file).get("video", 0.0)
        if vstart:
            cmd += ["-itsoffset", f"{-vstart:.6f}"]
        cmd += ["-i", video_file, "-f", "concat", "-safe", "0",
                "-i", listfile, "-map", "0:v:0", "-map", "1:a", "-c:v", "copy", "-c:a", "pcm_s24le", "-ar", "48000",
                "-shortest", video]
    # Lossless audio: ffmpeg's AAC encoder overshot these limited masters by ~4 dB (Soft Concrete: -1.6 -> +2.5 dBFS),
    # and YouTube transcodes anyway, so the upload carries PCM and gets exactly one lossy encode, YouTube's.
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True)
    os.remove(listfile)
    if r.returncode:
        sys.exit(f"ytpub: video encode failed: {r.stderr[-400:]}")
    if video_file:
        why = sync_problem(stream_starts(video))
        if why:
            sys.exit(f"ytpub: {video} is out of sync: {why}; not using it")
    peak, src = sample_peak_db(video), max(sample_peak_db(p) for p in audio)
    if not peak_ok(peak, src):
        sys.exit(f"ytpub: the video's audio peaks at {peak:+.2f} dBFS against the release files' {src:+.2f}; not using it")
    for old in ("video.mp4",):
        if os.path.exists(os.path.join(out, old)):
            os.remove(os.path.join(out, old))
    desc = description(meta, rel, chaps, is_mix)
    with open(os.path.join(out, "description.txt"), "w") as f:
        f.write(desc + "\n")
    state_p = os.path.join(out, "meta.json")
    state = json.load(open(state_p)) if os.path.exists(state_p) else {}
    state.pop("video_source", None)
    state.update({"album_id": aid, "album": meta["album"], "title": video_title(meta, is_mix), "mix": is_mix,
                  "tags": tags(meta), "video": "video.mov", "thumbnail": "thumb.jpg", "duration": round(ffprobe_dur(video), 2),
                  **({"video_source": os.path.abspath(video_file)} if video_file else {}),
                  "audio_peak_dbfs": round(peak, 2), "release_peak_dbfs": round(src, 2),
                  "built_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    json.dump(state, open(state_p, "w"), indent=1)
    os.remove(frame)
    print(f"{meta['album']}: {stamp(state['duration'])} {'mix' if is_mix else 'album'} video, {len(chaps)} chapters, "
          f"{os.path.getsize(video) / 1e6:.0f} MB in {time.time() - t0:.0f} s -> {out}")
    return out


# ---------- OAuth (installed app, loopback + PKCE) ----------

def client():
    p = os.path.join(CRED_DIR, "client_secret.json")
    if not os.path.exists(p):
        sys.exit(f"ytpub: no OAuth client at {p} (copy gws's client_secret.json there, mode 600)")
    d = json.load(open(p))
    return d.get("installed") or d.get("web") or d


def write_private(path, obj):
    os.makedirs(os.path.dirname(path), mode=0o700, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump(obj, f)


def parse_code_url(url):
    """The authorisation code and state from the redirect URL (or a bare code)."""
    q = urllib.parse.parse_qs(urllib.parse.urlparse(url.strip()).query)
    if "error" in q:
        sys.exit(f"ytpub: consent refused: {q['error'][0]}")
    if "code" in q:
        return q["code"][0], (q.get("state") or [None])[0]
    return url.strip(), None


def post_form(url, fields):
    data = urllib.parse.urlencode(fields).encode()
    try:
        return json.load(urllib.request.urlopen(url, data, timeout=60))
    except urllib.error.HTTPError as e:
        sys.exit(f"ytpub: token endpoint {e.code}: {e.read().decode()[:300]}")


def exchange(code, pending):
    c = client()
    tok = post_form(c.get("token_uri", "https://oauth2.googleapis.com/token"), {
        "code": code, "client_id": c["client_id"], "client_secret": c["client_secret"],
        "redirect_uri": pending["redirect"], "grant_type": "authorization_code", "code_verifier": pending["verifier"]})
    if "refresh_token" not in tok:
        sys.exit("ytpub: no refresh token returned; run auth again (it asks with prompt=consent)")
    write_private(os.path.join(CRED_DIR, "token.json"), {"refresh_token": tok["refresh_token"], "scope": tok.get("scope"),
                                                       "created": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    try:
        os.remove(os.path.join(CRED_DIR, "pending.json"))
    except FileNotFoundError:
        pass


def cmd_auth(a):
    pend_p = os.path.join(CRED_DIR, "pending.json")
    if a.finish:
        pending = json.load(open(pend_p))
        code, state = parse_code_url(a.finish)
        if state and state != pending["state"]:
            sys.exit("ytpub: state mismatch; start auth again")
        exchange(code, pending)
        return cmd_whoami(a)
    c = client()
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(48)).rstrip(b"=").decode()
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    state = secrets.token_urlsafe(16)
    got = {}

    class H(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            got["url"] = self.path
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"Chirpers YouTube authorised. You can close this tab.")

        def log_message(self, *args):
            pass

    srv = http.server.HTTPServer(("127.0.0.1", a.port), H)
    redirect = f"http://127.0.0.1:{srv.server_port}"
    pending = {"verifier": verifier, "state": state, "redirect": redirect}
    write_private(pend_p, pending)
    url = c.get("auth_uri", "https://accounts.google.com/o/oauth2/auth") + "?" + urllib.parse.urlencode({
        "client_id": c["client_id"], "redirect_uri": redirect, "response_type": "code", "scope": " ".join(SCOPES),
        "access_type": "offline", "prompt": "consent select_account", "state": state,
        "code_challenge": challenge, "code_challenge_method": "S256"})
    print("Open this URL and, in Google's chooser, pick the CHIRPERS channel (not your personal one):\n\n" + url + "\n")
    print(f"Waiting up to {a.wait} s on {redirect}. Consenting from another device? Its browser will fail to load "
          f"127.0.0.1; copy that address and run: ytpub.py auth --finish 'URL'", flush=True)
    srv.timeout = 5
    deadline = time.time() + a.wait
    while "url" not in got and time.time() < deadline:
        srv.handle_request()
    srv.server_close()
    if "url" not in got:
        sys.exit("ytpub: no redirect yet; finish with: ytpub.py auth --finish 'URL'")
    code, st = parse_code_url(got["url"])
    if st != state:
        sys.exit("ytpub: state mismatch; start auth again")
    exchange(code, pending)
    return cmd_whoami(a)


def access_token():
    p = os.path.join(CRED_DIR, "token.json")
    if not os.path.exists(p):
        sys.exit("ytpub: not authorised; run ytpub.py auth")
    c = client()
    tok = post_form(c.get("token_uri", "https://oauth2.googleapis.com/token"), {
        "client_id": c["client_id"], "client_secret": c["client_secret"],
        "refresh_token": json.load(open(p))["refresh_token"], "grant_type": "refresh_token"})
    return tok["access_token"]


def call(method, url, token, body=None, ctype="application/json", headers=None):
    data = json.dumps(body).encode() if isinstance(body, (dict, list)) else body
    h = {"Authorization": "Bearer " + token, **({"Content-Type": ctype} if data is not None else {}), **(headers or {})}
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            raw = r.read()
            return r.status, dict(r.headers), (json.loads(raw) if raw[:1] in (b"{", b"[") else raw)
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            payload = json.loads(raw)
        except ValueError:
            payload = raw.decode(errors="replace")[:500]
        return e.code, dict(e.headers), payload


def channel(token):
    st, _, d = call("GET", f"{API}/channels?part=snippet&mine=true", token)
    if st != 200:
        sys.exit(f"ytpub: channels.list {st}: {json.dumps(d)[:400]}")
    items = d.get("items") or []
    if not items:
        sys.exit("ytpub: the authorised account has no channel; create Chirpers in YouTube first")
    s = items[0]["snippet"]
    return {"id": items[0]["id"], "title": s.get("title"), "handle": s.get("customUrl")}


def cmd_whoami(a):
    ch = channel(access_token())
    print(f"channel: {ch['title']} {ch['handle'] or ''} ({ch['id']})")
    if not same_channel(ch["title"]):
        print(f"WARNING: not the {CHANNEL_TITLE} channel; uploads will refuse. Run auth again and pick {CHANNEL_TITLE}.")
    return ch


# ---------- upload ----------

def next_offset(headers):
    """Bytes already received by a resumable session, from a 308's Range header ('bytes=0-N')."""
    rng = {k.lower(): v for k, v in headers.items()}.get("range")
    return int(rng.rsplit("-", 1)[1]) + 1 if rng else 0


def resumable_upload(token, path, body, log=print):
    size = os.path.getsize(path)
    st, h, d = call("POST", f"{UPLOAD}/videos?uploadType=resumable&part=snippet,status", token, body,
                    ctype="application/json; charset=UTF-8",
                    headers={"X-Upload-Content-Type": video_type(path), "X-Upload-Content-Length": str(size)})
    loc = {k.lower(): v for k, v in h.items()}.get("location")
    if st != 200 or not loc:
        sys.exit(f"ytpub: upload session {st}: {json.dumps(d)[:500]}")
    off, tries = 0, 0
    with open(path, "rb") as f:
        while True:
            f.seek(off)
            chunk = f.read(CHUNK)
            end = off + len(chunk) - 1
            st, h, d = call("PUT", loc, token, chunk, ctype=video_type(path), headers={"Content-Range": f"bytes {off}-{end}/{size}"})
            if st in (200, 201):
                return d
            if st == 308:
                off, tries = next_offset(h), 0
                log(f"  {off / size:6.1%} of {size / 1e6:.0f} MB")
                continue
            if st >= 500 and tries < 6:
                tries += 1
                time.sleep(2 ** tries)
                st, h, d = call("PUT", loc, token, b"", ctype=video_type(path), headers={"Content-Range": f"bytes */{size}"})
                if st in (200, 201):
                    return d
                off = next_offset(h) if st == 308 else off
                continue
            sys.exit(f"ytpub: upload failed {st}: {json.dumps(d)[:500] if not isinstance(d, bytes) else d[:300]}")


def cmd_upload(a):
    aid, meta, rdir = resolve(a.album)
    out = os.path.join(rdir, "youtube")
    state_p = os.path.join(out, "meta.json")
    if not os.path.exists(state_p):
        sys.exit(f"ytpub: no kit for {meta['album']}; run ytpub.py kit {aid}")
    state = json.load(open(state_p))
    if state.get("video_id") and not a.again:
        sys.exit(f"ytpub: already uploaded as https://youtu.be/{state['video_id']} ({state.get('privacy')}); --again to upload another")
    body = {"snippet": {"title": state["title"], "description": open(os.path.join(out, "description.txt")).read().strip(),
                        "tags": state["tags"], "categoryId": "10", "defaultLanguage": "en"},
            "status": {"privacyStatus": a.privacy, "selfDeclaredMadeForKids": False, "embeddable": True,
                       "license": "youtube", "containsSyntheticMedia": not a.no_synthetic_label}}
    if a.dry_run:
        print(json.dumps(body, indent=1))
        return
    token = access_token()
    ch = channel(token)
    if not same_channel(ch["title"]):
        sys.exit(f"ytpub: authorised channel is {ch['title']!r}, not {CHANNEL_TITLE!r}; refusing to upload")
    print(f"uploading {state['title']} to {ch['title']} {ch['handle'] or ''} as {a.privacy}")
    v = resumable_upload(token, os.path.join(out, state["video"]), body)
    state.update({"video_id": v["id"], "channel_id": ch["id"], "privacy": a.privacy,
                  "uploaded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    json.dump(state, open(state_p, "w"), indent=1)
    st, _, d = call("POST", f"{UPLOAD}/thumbnails/set?videoId={v['id']}", access_token(),
                    open(os.path.join(out, state["thumbnail"]), "rb").read(), ctype="image/jpeg")
    print(f"https://youtu.be/{v['id']} ({a.privacy})" + ("" if st == 200 else
          f"; thumbnail not set ({st}: custom thumbnails need the channel phone-verified)"))


def cmd_publish(a):
    aid, meta, rdir = resolve(a.album)
    state_p = os.path.join(rdir, "youtube", "meta.json")
    state = json.load(open(state_p)) if os.path.exists(state_p) else {}
    if not state.get("video_id"):
        sys.exit(f"ytpub: {meta['album']} is not uploaded yet")
    token = access_token()
    st, _, d = call("GET", f"{API}/videos?part=status&id={state['video_id']}", token)
    items = (d or {}).get("items") if isinstance(d, dict) else None
    if st != 200 or not items:
        sys.exit(f"ytpub: videos.list {st}: {json.dumps(d)[:300]}")
    status = items[0]["status"]
    status["privacyStatus"] = a.privacy
    status.pop("uploadStatus", None), status.pop("failureReason", None), status.pop("rejectionReason", None)
    st, _, d = call("PUT", f"{API}/videos?part=status", token, {"id": state["video_id"], "status": status})
    if st != 200:
        sys.exit(f"ytpub: videos.update {st}: {json.dumps(d)[:300]}")
    state["privacy"] = a.privacy
    json.dump(state, open(state_p, "w"), indent=1)
    print(f"https://youtu.be/{state['video_id']} is now {a.privacy}")


def banner_jpeg(path, out):
    """A 2560x1440 JPEG under YouTube's 6 MB banner limit (16:9, centre crop)."""
    from PIL import Image
    im = Image.open(path).convert("RGB")
    w, h = im.size
    if w / h > 16 / 9:
        nw = int(h * 16 / 9)
        im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = int(w * 9 / 16)
        im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    im.resize((2560, 1440), Image.LANCZOS).save(out, quality=90)
    return out


def cmd_channel(a):
    token = access_token()
    ch = channel(token)
    if not same_channel(ch["title"]):
        sys.exit(f"ytpub: authorised channel is {ch['title']!r}, not {CHANNEL_TITLE!r}; refusing")
    st, _, d = call("GET", f"{API}/channels?part=brandingSettings&id={ch['id']}", token)
    if st != 200:
        sys.exit(f"ytpub: channels.list {st}: {json.dumps(d)[:300]}")
    branding = d["items"][0].get("brandingSettings") or {}
    c = branding.setdefault("channel", {})
    if a.description_file:
        c["description"] = open(a.description_file).read().strip()[:1000]
    if a.keywords:
        c["keywords"] = a.keywords
    if a.country:
        c["country"] = a.country
    c.setdefault("defaultLanguage", "en")
    if a.banner:
        import tempfile
        jpg = banner_jpeg(a.banner, os.path.join(tempfile.mkdtemp(), "banner.jpg"))
        st, _, b = call("POST", f"{UPLOAD}/channelBanners/insert", token, open(jpg, "rb").read(), ctype="image/jpeg")
        if st != 200:
            sys.exit(f"ytpub: channelBanners.insert {st}: {json.dumps(b)[:300]}")
        branding.setdefault("image", {})["bannerExternalUrl"] = b["url"]
    st, _, d = call("PUT", f"{API}/channels?part=brandingSettings", token, {"id": ch["id"], "brandingSettings": branding})
    if st != 200:
        sys.exit(f"ytpub: channels.update {st}: {json.dumps(d)[:400]}")
    print(f"{ch['title']} {ch['handle']}: " + ", ".join(k for k in ("description", "keywords", "country") if c.get(k))
          + (", banner" if a.banner else ""))


def cmd_update(a):
    """Re-push an uploaded video's title, description (with chapters) and tags from the album's current metadata,
    without re-encoding or re-uploading (videos.update, 50 quota units)."""
    aid, meta, rdir = resolve(a.album)
    rel = release_of(rdir)
    state_p = os.path.join(rdir, "youtube", "meta.json")
    state = json.load(open(state_p)) if os.path.exists(state_p) else {}
    if not (rel and state.get("video_id")):
        sys.exit(f"ytpub: {meta['album']} is not uploaded yet")
    _, chaps, is_mix = program(rel, rdir, force_tracks=not state.get("mix"))
    title, desc, tg = video_title(meta, is_mix), description(meta, rel, chaps, is_mix), tags(meta)
    if a.dry_run:
        print(f"{state['video_id']}: {title}\ntags: {tg}\n{desc}")
        return
    token = access_token()
    st, _, d = call("GET", f"{API}/videos?part=snippet&id={state['video_id']}", token)
    items = (d or {}).get("items") if isinstance(d, dict) else None
    if st != 200 or not items:
        sys.exit(f"ytpub: videos.list {st}: {json.dumps(d)[:300]}")
    sn = items[0]["snippet"]
    body = {"id": state["video_id"], "snippet": {"title": title, "description": desc, "tags": tg,
                                                 "categoryId": sn.get("categoryId", "10"),
                                                 "defaultLanguage": sn.get("defaultLanguage", "en")}}
    st, _, d = call("PUT", f"{API}/videos?part=snippet", token, body)
    if st != 200:
        sys.exit(f"ytpub: videos.update {st}: {json.dumps(d)[:300]}")
    with open(os.path.join(rdir, "youtube", "description.txt"), "w") as f:
        f.write(desc + "\n")
    state.update({"title": title, "tags": tg, "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    json.dump(state, open(state_p, "w"), indent=1)
    print(f"https://youtu.be/{state['video_id']}: {title}")


def cmd_list(a):
    for aid in album_ids():
        meta = json.load(open(os.path.join(ROOT, "compose", aid, "album.json")))
        rdir = os.path.join(MUSIC, safe_name(meta.get("album", aid)))
        rel = release_of(rdir)
        sp = os.path.join(rdir, "youtube", "meta.json")
        st = json.load(open(sp)) if os.path.exists(sp) else {}
        up = f"https://youtu.be/{st['video_id']} ({st.get('privacy')})" if st.get("video_id") else ("kit built" if st else "")
        print(f"{aid:10s} {meta.get('album', '?')[:28]:28s} {'released' if rel else 'unreleased':10s} {up}")


def cmd_kit(a):
    aid, meta, rdir = resolve(a.album)
    build_kit(aid, meta, rdir, force_tracks=a.tracks, video_file=a.video)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("auth")
    s.add_argument("--finish", metavar="URL", help="the redirect URL (or code) from a consent done on another device")
    s.add_argument("--port", type=int, default=0)
    s.add_argument("--wait", type=int, default=600)
    s.set_defaults(fn=cmd_auth)
    sub.add_parser("whoami").set_defaults(fn=cmd_whoami)
    sub.add_parser("list").set_defaults(fn=cmd_list)
    s = sub.add_parser("kit")
    s.add_argument("album")
    s.add_argument("--tracks", action="store_true", help="the album's tracks back to back even when it has a mix")
    s.add_argument("--video", metavar="FILE", help="a ready-made album video (chirp video --album) instead of the cover "
                   "still: its picture is kept, the release audio laid under it; it must last as long as the album")
    s.set_defaults(fn=cmd_kit)
    s = sub.add_parser("upload")
    s.add_argument("album")
    s.add_argument("--privacy", choices=["private", "unlisted", "public"], default="private")
    s.add_argument("--no-synthetic-label", action="store_true", help="do not set YouTube's altered/synthetic content flag")
    s.add_argument("--again", action="store_true")
    s.add_argument("--dry-run", action="store_true")
    s.set_defaults(fn=cmd_upload)
    s = sub.add_parser("publish")
    s.add_argument("album")
    s.add_argument("--privacy", choices=["private", "unlisted", "public"], default="public")
    s.set_defaults(fn=cmd_publish)
    s = sub.add_parser("update")
    s.add_argument("album")
    s.add_argument("--dry-run", action="store_true")
    s.set_defaults(fn=cmd_update)
    s = sub.add_parser("channel")
    s.add_argument("--description-file")
    s.add_argument("--keywords", help="space-separated; quote multi-word ones")
    s.add_argument("--country", default="GB")
    s.add_argument("--banner", help="an image; cropped to 16:9 and sent as a 2560x1440 JPEG")
    s.set_defaults(fn=cmd_channel)
    a = p.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
