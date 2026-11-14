#!/usr/bin/env python3
"""listen: Harry's album review app (chirp-eco, 6 Nov). Immutable SNAPSHOTS of an album in progress (each track's kept
song file rendered at seed 0 on the groove pin; a track whose song file is unchanged is hard-linked from the previous
snapshot, not re-rendered), a track-by-track player, NOTES at timestamps that go straight to the track's owner, an
"open live in chirp web" link per track (the canonical song in the URL hash, rendered and drawn in the browser), and
best-effort 480p preview videos.

  listen.py cut ALBUM [--label TEXT]                 cut a snapshot (renders changed tracks at nice 15)
  listen.py video ALBUM [SNAP] [--ids 1,8] [--look accretion | '{id}|accretion3d'] [--redo | --stale]
                                                             480p previews (~1.3x real time each: an idle unit)
  listen.py serve [--host H]... [--port 8791]        the app (notes notify the owner through caco); --host repeats
                                                             (the tailnet address and 127.0.0.1 for a Tailscale funnel)

The site (8 Nov, Harry: for him and a friend): a name and the access code once per browser ($CHIRP_LISTEN_CODE, default
'solofury'; a light gate, not security: the page loads freely, data and media need the code as a cookie or an
X-Listen-Code header); album tabs ($CHIRP_LISTEN_ALBUMS, default chirpers10,chirpers9,chirpers8); views Listen (snapshots, or a
released album's video from DATA/ALBUM/release/album.mp4 + chapters.txt), Feedback (every note and reply, signed with
the visitor's name, plus general album feedback), Worklog (every climb round and section note with the pinned engine
features and snapshots, from climbs/ID.jsonl, compose/ALBUM/sections/ and features.md) and History (a track's
renders across snapshots, an A-B segment played version by version, what changed between them).
  listen.py notes ALBUM [--track N] [--open]         read Harry's notes (composers)
  listen.py reply ALBUM NOTE_ID TEXT [--done]        answer a note; it shows under the note in the app

The page is tools/listen.html (read per request). Data: $CHIRP_LISTEN_DIR or ~/.local/state/chirp-eco/listen/ALBUM/
{snapshots/ID/snapshot.json + tNN.mp3/.mp4/.web,
notes.jsonl}. notes.jsonl is an append-only event log (add / reply / delete), so concurrent writers never clobber.
"""
import argparse
import base64
import hashlib
import http.server
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
import time
import urllib.parse
import uuid
import wave
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(HERE)
DATA = os.environ.get("CHIRP_LISTEN_DIR") or os.path.expanduser("~/.local/state/chirp-eco/listen")
WEB = "https://a.skh.am/tools/chirp/"
PUBLIC = os.environ.get("CHIRP_LISTEN_URL", "http://pocket4:8791/")
# owner -> caco agent id (notes go to the owner, cc chirp-eco); DATA/agents.json overrides
AGENTS = {"chirper-zero": "visiting-e308691bf15d", "chirper-one": "visiting-f54b7932ca1d",
          "chirper-two": "visiting-7acbd99f0240", "chirper-three": "visiting-007cc2b5b6eb",
          "wM": "visiting-9506062ca1f8", "chirp-video": "visiting-522210c1ed13", "chirp-eco": "visiting-c82ac9645a31"}


# ── pure helpers (tested) ──────────────────────────────────────────────────────────────────

def share_hash(text):
    """chirp web's share hash (web/library.js shareHash): '#s=' + base64url(deflate-raw(text)), no padding."""
    c = zlib.compressobj(9, zlib.DEFLATED, -15)
    z = c.compress(text.encode()) + c.flush()
    return "#s=" + base64.urlsafe_b64encode(z).decode().rstrip("=")


def from_hash(h):
    m = re.search(r"[#&]s=([A-Za-z0-9_-]+)", h)
    raw = base64.urlsafe_b64decode(m.group(1) + "=" * (-len(m.group(1)) % 4))
    return zlib.decompress(raw, -15).decode()


def byte_range(header, size):
    """(start, end) inclusive for a single 'bytes=' Range header, or None (whole file / unsatisfiable)."""
    m = re.fullmatch(r"\s*bytes=(\d*)-(\d*)\s*", header or "")
    if not m or (m.group(1) == "" and m.group(2) == ""):
        return None
    if m.group(1) == "":
        n = int(m.group(2))
        return (max(0, size - n), size - 1) if n else None
    a = int(m.group(1))
    b = min(int(m.group(2)), size - 1) if m.group(2) else size - 1
    return (a, b) if a <= b < size else None


def reduce_notes(events):
    """Fold the notes.jsonl event log into notes (oldest first): add creates, reply appends (and may mark done),
    delete hides."""
    notes = {}
    for e in events:
        op, nid = e.get("op"), e.get("id")
        if op == "add":
            notes[nid] = {**{k: v for k, v in e.items() if k != "op"}, "replies": [], "done": False}
        elif nid in notes and op == "reply":
            notes[nid]["replies"].append({k: e.get(k) for k in ("by", "at", "text")})
            notes[nid]["done"] = notes[nid]["done"] or bool(e.get("done"))
        elif nid in notes and op == "delete":
            notes.pop(nid)
    return sorted(notes.values(), key=lambda n: n.get("at", ""))


def mmss(t):
    t = float(t or 0)
    return f"{int(t // 60)}:{int(t % 60):02d}"


# ── storage ────────────────────────────────────────────────────────────────────────────────

def album_dir(album):
    return os.path.join(DATA, album)


def snapshots(album):
    d = os.path.join(album_dir(album), "snapshots")
    out = []
    for s in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        p = os.path.join(d, s, "snapshot.json")
        if not s.startswith(".") and os.path.exists(p):
            out.append(read_json(p))
    return out


_LOCK = threading.Lock()


def append_event(album, ev):
    os.makedirs(album_dir(album), exist_ok=True)
    line = json.dumps(ev, ensure_ascii=False) + "\n"
    with _LOCK, open(os.path.join(album_dir(album), "notes.jsonl"), "a") as f:
        f.write(line)                                           # one write per line: O_APPEND keeps lines whole


def notes(album):
    p = os.path.join(album_dir(album), "notes.jsonl")
    if not os.path.exists(p):
        return []
    with open(p) as f:
        return reduce_notes(json.loads(ln) for ln in f if ln.strip())


def now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


# ── cutting snapshots ──────────────────────────────────────────────────────────────────────

def sha_file(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]


def read_json(p):
    with open(p) as f:
        return json.load(f)


def read_text(p):
    with open(p) as f:
        return f.read()


def committed_text(rel):
    """A song's committed text (git HEAD), so a snapshot never catches a composer's uncommitted experiment; the
    working file when it is not tracked."""
    r = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=ROOT, capture_output=True)
    if r.returncode == 0 and r.stdout:
        return r.stdout
    with open(os.path.join(ROOT, rel), "rb") as f:
        return f.read()


def at_head(rel):
    """Whether git HEAD holds this path."""
    return subprocess.run(["git", "cat-file", "-e", f"HEAD:{rel}"], cwd=ROOT, capture_output=True).returncode == 0


def first_version_pending(rel, kept, tracked=None):
    """A track whose FIRST version is still being written: no kept round yet and its song file not in git HEAD. A cut
    leaves it out: committed_text would take the working file, half written (14 Nov: Common Time's second song was
    opened while snapshots of the first were being cut on every kept version)."""
    return not kept and not (at_head(rel) if tracked is None else tracked)


def default_render(pin, song, wav_out):
    sys.path.insert(0, HERE)
    import chirpers as CH
    return CH.render(pin, song, 0, wav_out, dict(os.environ))


def default_canonical(pin, song):
    r = subprocess.run([pin, "plan", "-f", song, "--json"], capture_output=True, text=True, cwd=os.path.dirname(song))
    try:
        d = json.loads(r.stdout)
        return json.dumps((d.get("data") or d)["canonical"], separators=(",", ":"))
    except (ValueError, KeyError, TypeError):
        return None


def cut(album_id, label="", render=default_render, canonical=default_canonical, log=print):
    sys.path.insert(0, HERE)
    import chirpers as CH
    import climb as C
    album = CH.load_album(album_id)
    reg = read_json(os.path.join(ROOT, "climbs.json"))
    pin = read_text(os.path.join(HERE, "groove-pin")).strip()
    prev = (snapshots(album_id) or [None])[-1]
    prev_by = {t["n"]: t for t in (prev or {}).get("tracks", [])}
    sid = time.strftime("%Y%m%d-%H%M", time.gmtime())
    base = os.path.join(album_dir(album_id), "snapshots")
    while os.path.exists(os.path.join(base, sid)):
        sid += "x"
    tmp = os.path.join(base, f".tmp-{sid}")
    os.makedirs(tmp, exist_ok=True)
    tracks, changed = [], 0
    for t in album["tracks"]:
        n, cid = t["n"], t["id"]
        c = next((c for c in reg["climbs"] if c["id"] == cid), None)
        rel = (c or {}).get("song") or f"songs/{cid}.yaml"
        if not c or not os.path.exists(os.path.join(ROOT, rel)):
            continue
        best = c.get("best") or {}
        kept = [h for h in C.history(cid) if h.get("kept") and h.get("version")]
        if first_version_pending(rel, kept):
            log(f"{cid}: no kept version and its song is not committed (a first version being written): left out")
            continue
        text = committed_text(rel)
        sha = hashlib.sha256(text).hexdigest()[:16]
        stem = f"t{n:02d}"
        old = prev_by.get(n)
        entry = {"n": n, "id": cid, "title": t.get("title") or cid, "owner": c.get("owner"),
                 "version": best.get("version"), "score": best.get("score"), "judged": bool(best.get("judged")),
                 "note": ((kept[-1].get("note") or "") if kept else "")[:4000], "sha": sha}
        olddir = os.path.join(base, prev["id"]) if prev else None
        if old and old.get("sha") == sha and os.path.exists(os.path.join(olddir, f"{stem}.mp3")):
            for ext in ("mp3", "mp4", "web", "song"):
                src = os.path.join(olddir, f"{stem}.{ext}")
                if os.path.exists(src):
                    os.link(src, os.path.join(tmp, f"{stem}.{ext}"))
            entry.update({k: old.get(k) for k in ("pin", "dur", "rendered", "video")}, changed=False)
            log(f"{cid}: {entry['version']} unchanged (linked from {prev['id']})")
        else:
            wav = os.path.join(tmp, f"{stem}.wav")
            t0 = time.time()
            with open(os.path.join(tmp, f"{stem}.song"), "wb") as f:
                f.write(text)
            song = os.path.join(ROOT, os.path.dirname(rel), f".listen-{os.getpid()}-{cid}.yaml")   # beside its includes
            with open(song, "wb") as f:
                f.write(text)
            try:
                err = render(pin, song, wav)
                canon = canonical(pin, song) if not err else None
            finally:
                os.unlink(song)
            if err or not os.path.exists(wav):
                log(f"{cid}: render failed: {err}")
                continue
            with wave.open(wav) as w:
                dur = w.getnframes() / float(w.getframerate())
            subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", wav, "-codec:a", "libmp3lame", "-q:a", "2",
                            os.path.join(tmp, f"{stem}.mp3")], check=True)
            os.unlink(wav)
            if canon:
                with open(os.path.join(tmp, f"{stem}.web"), "w") as f:
                    f.write(share_hash(canon))
            entry.update(pin=os.path.basename(pin), dur=round(dur, 2), rendered=now_iso(), changed=True, video=False)
            changed += 1
            log(f"{cid}: {entry['version']} rendered in {time.time() - t0:.0f} s")
        tracks.append(entry)
    snap = {"id": sid, "album": album_id, "title": album.get("album") or album.get("title") or album_id, "at": now_iso(),
            "label": label,
            "pin": os.path.basename(pin), "prev": (prev or {}).get("id"), "changed": changed, "tracks": tracks}
    with open(os.path.join(tmp, "snapshot.json"), "w") as f:
        json.dump(snap, f, indent=1, ensure_ascii=False)
    os.rename(tmp, os.path.join(base, sid))
    log(f"listen: snapshot {album_id}/{sid}: {len(tracks)} tracks, {changed} rendered")
    return snap


def snapshot_song(d, t):
    """The song text this snapshot rendered: its tNN.song copy, else (snapshots cut before copies were kept) the
    version in git whose sha256 matches, else None."""
    p = os.path.join(d, f"t{t['n']:02d}.song")
    if os.path.exists(p):
        return read_text(p)
    rel = f"songs/{t['id']}.yaml"
    cur = os.path.join(ROOT, rel)
    if os.path.exists(cur) and sha_file(cur) == t["sha"]:
        return read_text(cur)
    hs = subprocess.run(["git", "log", "--format=%H", "-n", "200", "--", rel], cwd=ROOT, capture_output=True,
                        text=True).stdout.split()
    for h in hs:
        b = subprocess.run(["git", "show", f"{h}:{rel}"], cwd=ROOT, capture_output=True).stdout
        if b and hashlib.sha256(b).hexdigest()[:16] == t["sha"]:
            return b.decode()
    return None


def look_args(look, track_id, vis_dir=None):
    """The engine arguments for LOOK on track TRACK_ID. A plain LOOK is passed as `--look LOOK`. A LOOK with `{id}` names
    a programme per track: `{id}|FALLBACK` uses vis/<id>.yaml (or .yml/.json) as `--vis` when it exists, else
    `--look FALLBACK` (none: the engine default), so tracks pick up their directed programmes as they appear
    (chirp-video, 8 Nov, after Harry asked for varied, directed videos)."""
    if not look:
        return []
    if "{id}" not in look:
        return ["--look", look]
    name, _, fallback = look.partition("|")
    name = name.replace("{id}", track_id)
    vis_dir = vis_dir or os.path.join(ROOT, "vis")
    for ext in (".yaml", ".yml", ".json"):
        p = os.path.join(vis_dir, name + ext)
        if os.path.exists(p):
            return ["--vis", p]
    return ["--look", fallback] if fallback else []


_LOD = {}


def lod_args(pin):
    """["--lod"] when PIN's `chirp video` has it (chirp-video's batch 49, 10 Nov: detail follows the picture's size, as
    in the live panes - a 480p preview draws about 480/1080 of each mesh and shadowmap; films stay at full detail),
    else []. Opt-in (videos' LOD): see there for what it saves and costs."""
    if pin not in _LOD:
        try:
            h = subprocess.run([pin, "video", "--help"], capture_output=True, text=True, stdin=subprocess.DEVNULL)
            _LOD[pin] = "--lod" in (h.stdout or "") + (h.stderr or "")
        except OSError:
            _LOD[pin] = False
    return ["--lod"] if _LOD[pin] else []


def programme_mtime(look, track_id, vis_dir=None):
    """The newest mtime of the programme LOOK gives TRACK_ID and of every kit it `use:`s (vis/<kit>.yaml, recursively),
    or None when LOOK names no programme file - so --stale can tell a preview older than its programme."""
    args = look_args(look, track_id, vis_dir)
    if "--vis" not in args:
        return None
    vis_dir = vis_dir or os.path.join(ROOT, "vis")
    seen, todo, newest = set(), [args[args.index("--vis") + 1]], 0.0
    while todo:
        p = todo.pop()
        if p in seen or not os.path.exists(p):
            continue
        seen.add(p)
        newest = max(newest, os.path.getmtime(p))
        for kit in re.findall(r"\buse:\s*[\"']?([A-Za-z0-9_.-]+)", read_text(p) or ""):
            for ext in (".yaml", ".yml", ".json"):
                q = os.path.join(vis_dir, kit + ext)
                if os.path.exists(q):
                    todo.append(q)
                    break
    return newest


def videos(album_id, sid=None, ids=None, look=None, log=print, run=subprocess.run, redo=False, stale=False, lod=False):
    """480p previews (854x480, 24 fps, crf 30; LOOK, else the song's own programme or the engine default); one track
    at a time, at nice 19 (about 1.3x real time on pocket4 under load). LOOK may be `{id}|FALLBACK` (see look_args);
    REDO re-renders previews that already exist (a track's programme changed); STALE re-renders only those older than
    their programme or a kit it uses (programme_mtime), plus missing ones; a preview's mtime is when its render
    started (a programme changed mid-render is newer than it).
    Each track renders on the groove pin AS IT IS WHEN THAT TRACK STARTS (9 Nov: a run that began on 7f9c5782 failed
    t4-t6 on programmes written for batch 44, adopted mid-run). Landings are gated byte-identical on the album, so a
    newer pin draws the snapshot's own audio.
    A preview is THE FILM at 480p (full detail). LOD passes `chirp video --lod` when the pin has it: detail follows
    the picture's size as in the live views, which is not how the film will look (chirp-video, 10 Nov) and saves
    about a quarter of the CPU (measured on fa300974 at 480p, cached audio: t1 bars 41-49 162 -> 119 CPU-s, t6 bars
    65-73 410 -> 296) - for a saturated host only."""
    snaps = snapshots(album_id)
    snap = next((s for s in snaps if s["id"] == sid), None) if sid else (snaps or [None])[-1]
    if not snap:
        raise SystemExit("no snapshot")
    d = os.path.join(album_dir(album_id), "snapshots", snap["id"])
    for t in snap["tracks"]:
        stem = f"t{t['n']:02d}"
        mp4 = os.path.join(d, f"{stem}.mp4")
        if ids and t["n"] not in ids:
            continue
        if os.path.exists(mp4) and not redo:
            pm = programme_mtime(look, t["id"]) if stale else None
            if not (pm and pm > os.path.getmtime(mp4)):
                continue
        pin = read_text(os.path.join(HERE, "groove-pin")).strip()
        text = snapshot_song(d, t)
        if text is None:
            log(f"{t['id']}: this snapshot's song text is not recoverable; skipped")
            continue
        song = os.path.join(ROOT, "songs", f".listen-{os.getpid()}-{t['id']}.yaml")   # beside its includes
        with open(song, "w") as f:
            f.write(text)
        out = os.path.join(d, f".{stem}.tmp.mp4")
        t0 = time.time()
        cmd = ["nice", "-n", "19", pin, "video", "-f", song, "--seed", "0", "--size", "854x480", "--fps", "24",
               "--crf", "30"] + (lod_args(pin) if lod else []) + look_args(look, t["id"]) + ["-o", out]
        try:
            r = run(cmd, capture_output=True, text=True, cwd=os.path.dirname(song))
        finally:
            os.unlink(song)
        if r.returncode or not os.path.exists(out):
            log(f"{t['id']}: video failed: {r.stderr.strip()[-200:]}")
            continue
        os.rename(out, os.path.join(d, f"{stem}.mp4"))
        os.utime(os.path.join(d, f"{stem}.mp4"), (t0, t0))   # stamped when its programme was read, for --stale
        t["video"] = True
        with open(os.path.join(d, "snapshot.json.tmp"), "w") as f:
            json.dump(snap, f, indent=1, ensure_ascii=False)
        os.replace(os.path.join(d, "snapshot.json.tmp"), os.path.join(d, "snapshot.json"))
        log(f"{t['id']}: 480p preview in {time.time() - t0:.0f} s")


# ── notify ─────────────────────────────────────────────────────────────────────────────────

def whoami():
    """Who is replying: $CHIRP_LISTEN_AUTHOR, else the caco agent this shell belongs to (CACO_AGENT_ID or
    CACOPHONY_ACTOR, by name when it is a known agent), else $USER. Every agent runs as Harry's Unix user, so $USER
    alone would sign a composer's reply as 'harry' (chirper-one's first reply, 6 Nov)."""
    if os.environ.get("CHIRP_LISTEN_AUTHOR"):
        return os.environ["CHIRP_LISTEN_AUTHOR"]
    cid = os.environ.get("CACO_AGENT_ID") or os.environ.get("CACOPHONY_ACTOR")
    if cid:
        return {v: k for k, v in agents().items()}.get(cid, cid)
    return os.environ.get("USER", "agent")


def agents():
    p = os.path.join(DATA, "agents.json")
    return {**AGENTS, **(read_json(p) if os.path.exists(p) else {})}


def notify(album, note, track):
    owner = (track or {}).get("owner")
    ids = [i for i in (agents().get(owner), agents().get("chirp-eco")) if i]
    link = f"{PUBLIC}#a={album}&s={note['snap']}&n={note['n']}&t={note['t']:.1f}"
    who = (note.get("by") or "harry").upper()
    where = (f"on t{note['n']} {track.get('title', '')} ({track.get('version')}, snapshot {note['snap']}) at {mmss(note['t'])}"
             if track else f"on the album {album} (general feedback, relay as you see fit)")
    body = (f"{who}'S NOTE {where}:\n\n{note['text']}\n\nListen at that moment: {link}\n"
            f"All notes: python3 ~/.config/chirp/tools/listen.py notes {album} --track {note['n']}\n"
            f"Answer (shows under the note in Harry's app): python3 ~/.config/chirp/tools/listen.py reply {album} "
            f"{note['id']} 'what you did' [--done]")
    env = {k: v for k, v in os.environ.items() if k not in ("CACO_AGENT_ID", "CACOPHONY_AGENT")}
    env["CACOPHONY_ACTOR"] = AGENTS["chirp-eco"]
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        f.write(body)
    with open(os.path.join(album_dir(album), "notify.log"), "a") as logf:
        for i in dict.fromkeys(ids):
            try:
                r = subprocess.run(["caco", "msg", "send", "--project", "tools", "--target", i, "--no-tts", "--body-file",
                                    f.name], env=env, capture_output=True, text=True, timeout=90)
                res = f"rc {r.returncode} {(r.stderr or r.stdout).strip()[-160:]!r}"
            except (OSError, subprocess.SubprocessError) as e:
                res = f"error {e!r}"
            logf.write(f"{now_iso()} note {note['id']} -> {i}: {res}\n")
    os.unlink(f.name)


# ── the review site: albums, worklog, feature checkpoints (8 Nov: Harry, for him and a friend over a funnel) ─────

CODE = os.environ.get("CHIRP_LISTEN_CODE", "solofury")      # a light access code, not security (Harry: "not load bearing")
ALBUMS = [a for a in os.environ.get("CHIRP_LISTEN_ALBUMS", "chirpers10,chirpers9,chirpers8").split(",") if a]
TOOLS_REPO = os.environ.get("CHIRP_TOOLS_REPO", "")              # optional: dates for pins not named in a commit


def clean_name(s, default="harry"):
    s = re.sub(r"[^\w .'-]", "", str(s or "")).strip()[:40]
    return s or default


def climb_tracks(album_id):
    """The album's tracks from climbs.json (n, id, title, owner), in track order."""
    try:
        climbs = read_json(os.path.join(ROOT, "climbs.json"))
    except (OSError, ValueError):
        return []
    items = climbs.get("climbs", []) if isinstance(climbs, dict) else climbs
    out = []
    for c in items:
        if isinstance(c, dict) and c.get("album") == album_id:
            m = c.get("meta") or {}
            out.append({"n": m.get("track"), "id": c.get("id"), "title": m.get("title") or c.get("id"),
                        "owner": c.get("owner"), "version": (c.get("best") or {}).get("version"),
                        "score": (c.get("best") or {}).get("score"), "rounds": c.get("rounds")})
    return sorted(out, key=lambda t: (t["n"] is None, t["n"] or 0))


def release_info(album_id):
    """DATA/ALBUM/release/: album.mp4 (the released continuous video), chapters.txt ('m:ss Title' per line) and an
    optional meta.json ({youtube, note})."""
    d = os.path.join(album_dir(album_id), "release")
    if not os.path.exists(os.path.join(d, "album.mp4")):
        return None
    chapters = []
    if os.path.exists(os.path.join(d, "chapters.txt")):
        for ln in read_text(os.path.join(d, "chapters.txt")).splitlines():
            m = re.match(r"\s*(?:(\d+):)?(\d+):(\d\d)\s+(.*)", ln)
            if m:
                h, mi, s, title = m.groups()
                chapters.append({"t": int(h or 0) * 3600 + int(mi) * 60 + int(s), "title": title.strip()})
    meta = read_json(os.path.join(d, "meta.json")) if os.path.exists(os.path.join(d, "meta.json")) else {}
    return {"video": f"media/{album_id}/release/album.mp4", "chapters": chapters, **meta}


def album_info(album_id):
    p = os.path.join(ROOT, "compose", album_id, "album.json")
    a = read_json(p) if os.path.exists(p) else {}
    snaps = snapshots(album_id)
    rel = release_info(album_id)
    return {"id": album_id, "title": a.get("album") or album_id, "artist": a.get("artist"), "genre": a.get("genre"),
            "brief": a.get("brief"), "direction": [d for d in [a.get("direction"), *(a.get("direction_more") or [])] if d],
            "snapshots": len(snaps),
            "status": "released" if rel else "in progress", "release": rel, "tracks": climb_tracks(album_id)}


def read_jsonl(p):
    out = []
    if os.path.exists(p):
        with open(p) as f:
            for ln in f:
                try:
                    out.append(json.loads(ln))
                except ValueError:
                    pass
    return out


_CHECKPOINTS = {}


def feature_checkpoints(album_id):
    """Engine features pinned on the album's feature board: rows of compose/ALBUM/features.md with 'pin HASH', each
    dated by the commit that first wrote that pin into the board (git log -S), cached on the file's mtime."""
    p = os.path.join(ROOT, "compose", album_id, "features.md")
    if not os.path.exists(p):
        return []
    key = (album_id, os.path.getmtime(p))
    if key in _CHECKPOINTS:
        return _CHECKPOINTS[key]
    out = []
    for ln in read_text(p).splitlines():
        m = re.search(r"pin ([0-9a-f]{8})", ln)
        if not ln.startswith("|") or not m:
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        name = (re.search(r"`([^`]+)`", cells[0]) or re.search(r"(\S+)", cells[0])).group(1)
        who = re.search(r"\(([^;()]*);", cells[0])
        at = subprocess.run(["git", "log", "--reverse", "--format=%cI", f"-Spin {m.group(1)}", "--",
                             os.path.relpath(p, ROOT)], cwd=ROOT, capture_output=True, text=True).stdout.split()
        if not at and TOOLS_REPO:
            at = subprocess.run(["git", "log", "-1", "--format=%cI", m.group(1)], cwd=TOOLS_REPO, capture_output=True,
                                text=True).stdout.split()
        desc = cells[0].split("):", 1)[1].strip() if "):" in cells[0] else cells[0]
        out.append({"name": name, "pin": m.group(1), "who": who.group(1).strip() if who else "",
                    "at": at[0] if at else None, "text": desc[:600], "used_by": cells[1][:300] if len(cells) > 1 else ""})
    out.sort(key=lambda c: c["at"] or "")
    _CHECKPOINTS.clear()
    _CHECKPOINTS[key] = out
    return out


def worklog(album_id):
    """Every climb round (climbs/ID.jsonl: who, version, score, kept, the composer's note) and every section note
    (compose/ALBUM/sections/ID.jsonl) per track, the pinned engine features and the snapshots, for the worklog and
    history views."""
    tracks = []
    for t in climb_tracks(album_id):
        rounds = [{k: r.get(k) for k in ("round", "at", "who", "score", "version", "kept")} | {"note": str(r.get("note") or "")[:6000]}
                  for r in read_jsonl(os.path.join(ROOT, "climbs", f"{t['id']}.jsonl"))]
        sections = [{k: s.get(k) for k in ("window", "at", "who", "version", "note")}
                    for s in read_jsonl(os.path.join(ROOT, "compose", album_id, "sections", f"{t['id']}.jsonl"))]
        tracks.append({**t, "log": rounds, "sections": sections})
    snaps = [{k: s.get(k) for k in ("id", "at", "label", "pin", "changed")} for s in snapshots(album_id)]
    feats = feature_checkpoints(album_id)
    if release_info(album_id):                                  # a released album: only what landed while it was made
        last = max((r["at"] or "" for t in tracks for r in t["log"]), default="")
        feats = [f for f in feats if f["at"] and f["at"] <= last]
    return {"album": album_id, "tracks": tracks, "features": feats, "snapshots": snaps}


# ── server ─────────────────────────────────────────────────────────────────────────────────

class Handler(http.server.BaseHTTPRequestHandler):
    server_version = "chirp-listen"

    def log_message(self, fmt, *args):
        pass

    def send_json(self, obj, code=200):
        b = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(b)

    def authed(self):
        """The access code, from the page's cookie (set once with the visitor's name) or an X-Listen-Code header."""
        if not CODE:
            return True
        if self.headers.get("X-Listen-Code") == CODE:
            return True
        for part in (self.headers.get("Cookie") or "").split(";"):
            k, _, v = part.strip().partition("=")
            if k == "listen_code" and urllib.parse.unquote(v) == CODE:
                return True
        return False

    def do_GET(self):
        path = self.path.split("?")[0]
        parts = [p for p in path.split("/") if p]
        if not parts:
            with open(os.path.join(HERE, "listen.html"), "rb") as f:
                b = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(b)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            return self.wfile.write(b)
        if parts == ["favicon.ico"]:
            return self.send_error(404)
        if not self.authed():
            return self.send_json({"error": "access code"}, 401)
        if parts == ["api", "albums"]:
            return self.send_json([album_info(a) for a in ALBUMS
                                   if os.path.exists(os.path.join(ROOT, "compose", a, "album.json")) or snapshots(a)])
        if len(parts) == 2 and parts[0] == "api":
            return self.send_json({"album": parts[1], "snapshots": snapshots(parts[1]), "notes": notes(parts[1])})
        if len(parts) == 3 and parts[0] == "api" and parts[2] == "log" and re.fullmatch(r"[\w-]+", parts[1]):
            return self.send_json(worklog(parts[1]))
        if len(parts) == 4 and parts[0] == "media" and parts[2] == "release" and parts[3] == "album.mp4":
            return self.send_media(os.path.join(album_dir(parts[1]), "release", "album.mp4"))
        if len(parts) == 4 and parts[0] == "media" and re.fullmatch(r"t\d\d\.(mp3|mp4)", parts[3]):
            return self.send_media(os.path.join(album_dir(parts[1]), "snapshots", parts[2], parts[3]))
        if len(parts) == 4 and parts[0] == "web" and parts[3].isdigit():
            p = os.path.join(album_dir(parts[1]), "snapshots", parts[2], f"t{int(parts[3]):02d}.web")
            if os.path.exists(p) and ".." not in p:
                self.send_response(302)
                self.send_header("Location", WEB + read_text(p).strip())
                return self.end_headers()
        self.send_error(404)

    def send_media(self, p):
        if ".." in p or not os.path.exists(p):
            return self.send_error(404)
        size = os.path.getsize(p)
        rng = byte_range(self.headers.get("Range"), size)
        a, b = rng or (0, size - 1)
        self.send_response(206 if rng else 200)
        self.send_header("Content-Type", "audio/mpeg" if p.endswith(".mp3") else "video/mp4")
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(b - a + 1))
        if rng:
            self.send_header("Content-Range", f"bytes {a}-{b}/{size}")
        self.end_headers()
        with open(p, "rb") as f:
            f.seek(a)
            left = b - a + 1
            while left > 0:
                chunk = f.read(min(1 << 16, left))
                if not chunk:
                    break
                try:
                    self.wfile.write(chunk)
                except (BrokenPipeError, ConnectionResetError):
                    return
                left -= len(chunk)

    def do_POST(self):
        parts = [p for p in self.path.split("?")[0].split("/") if p]
        if not self.authed():
            return self.send_json({"error": "access code"}, 401)
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
        except ValueError:
            return self.send_json({"error": "bad json"}, 400)
        if len(parts) == 3 and parts[0] == "api" and parts[2] == "notes":
            album = parts[1]
            text = str(body.get("text") or "").strip()
            by = clean_name(body.get("by"))
            if not text:
                return self.send_json({"error": "text is required"}, 400)
            if body.get("snap") == "release" or not body.get("n"):
                # a note on a released album's video (snap 'release', n the chapter's track) or general feedback (n 0)
                track = next((t for t in climb_tracks(album) if t["n"] == body.get("n")), None) if body.get("n") else None
                note = {"op": "add", "id": uuid.uuid4().hex[:8], "at": now_iso(), "by": by,
                        "snap": "release" if body.get("snap") == "release" else (body.get("snap") or ""),
                        "n": track["n"] if track else 0, "track": track["id"] if track else None,
                        "version": "release" if body.get("snap") == "release" else None,
                        "t": round(float(body.get("t") or 0), 1), "text": text[:4000]}
                append_event(album, note)
                threading.Thread(target=notify, args=(album, note, track), daemon=True).start()
                return self.send_json({"ok": True, "id": note["id"]})
            snap = next((s for s in snapshots(album) if s["id"] == body.get("snap")), None)
            track = next((t for t in (snap or {}).get("tracks", []) if t["n"] == body.get("n")), None)
            if not track:
                return self.send_json({"error": "snap, n and text are required"}, 400)
            note = {"op": "add", "id": uuid.uuid4().hex[:8], "at": now_iso(), "by": by, "snap": snap["id"],
                    "n": track["n"], "track": track["id"], "version": track.get("version"),
                    "t": round(float(body.get("t") or 0), 1), "text": text[:4000]}
            append_event(album, note)
            threading.Thread(target=notify, args=(album, note, track), daemon=True).start()
            return self.send_json({"ok": True, "id": note["id"]})
        if len(parts) == 5 and parts[0] == "api" and parts[2] == "notes" and parts[4] == "reply":
            text = str(body.get("text") or "").strip()
            if not text or not any(n["id"] == parts[3] for n in notes(parts[1])):
                return self.send_json({"error": "note and text are required"}, 400)
            append_event(parts[1], {"op": "reply", "id": parts[3], "at": now_iso(), "by": clean_name(body.get("by")),
                                    "text": text[:4000], "done": False})
            return self.send_json({"ok": True})
        if len(parts) == 5 and parts[0] == "api" and parts[2] == "notes" and parts[4] == "delete":
            append_event(parts[1], {"op": "delete", "id": parts[3], "at": now_iso()})
            return self.send_json({"ok": True})
        self.send_error(404)


def serve(hosts, port):
    """One server per host (e.g. the tailnet address and 127.0.0.1, which a Tailscale funnel proxies to)."""
    hosts = [hosts] if isinstance(hosts, str) else list(hosts)
    srvs = [http.server.ThreadingHTTPServer((h, port), Handler) for h in hosts]
    for h in hosts:
        print(f"listen: serving {DATA} on http://{h}:{port}/ (albums {','.join(ALBUMS)}; access code {'on' if CODE else 'off'})",
              flush=True)
    for s in srvs[1:]:
        threading.Thread(target=s.serve_forever, daemon=True).start()
    srvs[0].serve_forever()


# ── CLI ────────────────────────────────────────────────────────────────────────────────────

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("cut")
    p.add_argument("album")
    p.add_argument("--label", default="")
    p = sub.add_parser("video")
    p.add_argument("album")
    p.add_argument("snap", nargs="?")
    p.add_argument("--ids")
    p.add_argument("--look", help="a look name, or {id}|FALLBACK: vis/<track id>.yaml when it exists, else FALLBACK")
    p.add_argument("--redo", action="store_true", help="re-render previews that already exist")
    p.add_argument("--stale", action="store_true", help="re-render previews older than their programme or its kits")
    p.add_argument("--lod", action="store_true", help="draw at preview detail (about a quarter less CPU; not the film's look)")
    p = sub.add_parser("serve")
    p.add_argument("--host", action="append", help="listen address (repeatable; default 127.0.0.1)")
    p.add_argument("--port", type=int, default=8791)
    p = sub.add_parser("notes")
    p.add_argument("album")
    p.add_argument("--track", type=int)
    p.add_argument("--open", action="store_true", help="only notes not marked done")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("reply")
    p.add_argument("album")
    p.add_argument("id")
    p.add_argument("text")
    p.add_argument("--done", action="store_true")
    p.add_argument("--by", help="who is replying (default: this shell's caco agent)")
    a = ap.parse_args(argv)
    if a.cmd == "cut":
        cut(a.album, a.label)
    elif a.cmd == "video":
        videos(a.album, a.snap, {int(x) for x in a.ids.split(",")} if a.ids else None, a.look, redo=a.redo, stale=a.stale, lod=a.lod)
    elif a.cmd == "serve":
        serve(a.host or ["127.0.0.1"], a.port)
    elif a.cmd == "notes":
        ns = [n for n in notes(a.album) if (a.track is None or n["n"] == a.track) and not (a.open and n["done"])]
        if a.json:
            return print(json.dumps(ns, ensure_ascii=False, indent=1))
        for n in ns:
            print(f"[{n['id']}] t{n['n']} {n.get('version')} @{mmss(n['t'])} (snapshot {n['snap']}, {n['at']})"
                  f"{'  DONE' if n['done'] else ''}\n    {n['text']}")
            for r in n["replies"]:
                print(f"    -> {r['by']} ({r['at']}): {r['text']}")
        print(f"listen: {len(ns)} note(s)")
    elif a.cmd == "reply":
        if not any(n["id"] == a.id for n in notes(a.album)):
            raise SystemExit(f"no note {a.id}")
        append_event(a.album, {"op": "reply", "id": a.id, "at": now_iso(), "by": a.by or whoami(), "text": a.text,
                               "done": a.done})
        print("listen: reply recorded")



if __name__ == "__main__":
    main()
