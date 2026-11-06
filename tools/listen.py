#!/usr/bin/env python3
"""listen: Harry's album review app (chirp-eco, 6 Nov). Immutable SNAPSHOTS of an album in progress (each track's kept
song file rendered at seed 0 on the groove pin; a track whose song file is unchanged is hard-linked from the previous
snapshot, not re-rendered), a track-by-track player, NOTES at timestamps that go straight to the track's owner, an
"open live in chirp web" link per track (the canonical song in the URL hash, rendered and drawn in the browser), and
best-effort 480p preview videos.

  listen.py cut ALBUM [--label TEXT]                 cut a snapshot (renders changed tracks at nice 15)
  listen.py video ALBUM [SNAP] [--ids 1,8] [--look accretion]   480p previews (~1.3x real time each: an idle unit)
  listen.py serve [--host H] [--port 8791]           the app (notes notify the owner through caco)
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
        song = os.path.join(ROOT, (c or {}).get("song") or f"songs/{cid}.yaml")
        if not c or not os.path.exists(song):
            continue
        best = c.get("best") or {}
        kept = [h for h in C.history(cid) if h.get("kept") and h.get("version")]
        sha = sha_file(song)
        stem = f"t{n:02d}"
        old = prev_by.get(n)
        entry = {"n": n, "id": cid, "title": t.get("title") or cid, "owner": c.get("owner"),
                 "version": best.get("version"), "score": best.get("score"), "judged": bool(best.get("judged")),
                 "note": ((kept[-1].get("note") or "") if kept else "")[:4000], "sha": sha}
        olddir = os.path.join(base, prev["id"]) if prev else None
        if old and old.get("sha") == sha and os.path.exists(os.path.join(olddir, f"{stem}.mp3")):
            for ext in ("mp3", "mp4", "web"):
                src = os.path.join(olddir, f"{stem}.{ext}")
                if os.path.exists(src):
                    os.link(src, os.path.join(tmp, f"{stem}.{ext}"))
            entry.update({k: old.get(k) for k in ("pin", "dur", "rendered", "video")}, changed=False)
            log(f"{cid}: {entry['version']} unchanged (linked from {prev['id']})")
        else:
            wav = os.path.join(tmp, f"{stem}.wav")
            t0 = time.time()
            err = render(pin, song, wav)
            if err or not os.path.exists(wav):
                log(f"{cid}: render failed: {err}")
                continue
            with wave.open(wav) as w:
                dur = w.getnframes() / float(w.getframerate())
            subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", wav, "-codec:a", "libmp3lame", "-q:a", "2",
                            os.path.join(tmp, f"{stem}.mp3")], check=True)
            os.unlink(wav)
            canon = canonical(pin, song)
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


def videos(album_id, sid=None, ids=None, look=None, log=print):
    """480p previews (854x480, 24 fps, crf 30; LOOK, else the song's own programme or the engine default); one track
    at a time, at nice 19 (about 1.3x real time on pocket4 under load)."""
    snaps = snapshots(album_id)
    snap = next((s for s in snaps if s["id"] == sid), None) if sid else (snaps or [None])[-1]
    if not snap:
        raise SystemExit("no snapshot")
    d = os.path.join(album_dir(album_id), "snapshots", snap["id"])
    pin = read_text(os.path.join(HERE, "groove-pin")).strip()
    for t in snap["tracks"]:
        stem = f"t{t['n']:02d}"
        if (ids and t["n"] not in ids) or os.path.exists(os.path.join(d, f"{stem}.mp4")):
            continue
        song = os.path.join(ROOT, "songs", f"{t['id']}.yaml")
        if not os.path.exists(song) or sha_file(song) != t["sha"]:
            log(f"{t['id']}: song file moved on since this snapshot; skipped")
            continue
        out = os.path.join(d, f".{stem}.tmp.mp4")
        t0 = time.time()
        cmd = ["nice", "-n", "19", pin, "video", "-f", song, "--seed", "0", "--size", "854x480", "--fps", "24",
               "--crf", "30"] + (["--look", look] if look else []) + ["-o", out]
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(song))
        if r.returncode or not os.path.exists(out):
            log(f"{t['id']}: video failed: {r.stderr.strip()[-200:]}")
            continue
        os.rename(out, os.path.join(d, f"{stem}.mp4"))
        t["video"] = True
        with open(os.path.join(d, "snapshot.json.tmp"), "w") as f:
            json.dump(snap, f, indent=1, ensure_ascii=False)
        os.replace(os.path.join(d, "snapshot.json.tmp"), os.path.join(d, "snapshot.json"))
        log(f"{t['id']}: 480p preview in {time.time() - t0:.0f} s")


# ── notify ─────────────────────────────────────────────────────────────────────────────────

def agents():
    p = os.path.join(DATA, "agents.json")
    return {**AGENTS, **(read_json(p) if os.path.exists(p) else {})}


def notify(album, note, track):
    owner = (track or {}).get("owner")
    ids = [i for i in (agents().get(owner), agents().get("chirp-eco")) if i]
    link = f"{PUBLIC}#a={album}&s={note['snap']}&n={note['n']}&t={note['t']:.1f}"
    body = (f"HARRY'S NOTE on t{note['n']} {track.get('title', '')} ({track.get('version')}, snapshot {note['snap']}) "
            f"at {mmss(note['t'])}:\n\n{note['text']}\n\nListen at that moment: {link}\n"
            f"All notes: python3 ~/.config/chirp/tools/listen.py notes {album} --track {note['n']}\n"
            f"Answer (shows under the note in Harry's app): python3 ~/.config/chirp/tools/listen.py reply {album} "
            f"{note['id']} 'what you did' [--done]")
    env = {k: v for k, v in os.environ.items() if k not in ("CACO_AGENT_ID", "CACOPHONY_AGENT")}
    env["CACOPHONY_ACTOR"] = AGENTS["chirp-eco"]
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        f.write(body)
    for i in dict.fromkeys(ids):
        subprocess.run(["caco", "msg", "send", "--project", "tools", "--target", i, "--no-tts", "--body-file", f.name],
                       env=env, capture_output=True, timeout=90)
    os.unlink(f.name)


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

    def do_GET(self):
        path = self.path.split("?")[0]
        parts = [p for p in path.split("/") if p]
        if not parts:
            with open(os.path.join(HERE, "listen.html"), "rb") as f:
                b = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(b)))
            self.end_headers()
            return self.wfile.write(b)
        if parts == ["api", "albums"]:
            d = DATA if os.path.isdir(DATA) else None
            return self.send_json([a for a in sorted(os.listdir(d)) if snapshots(a)] if d else [])
        if len(parts) == 2 and parts[0] == "api":
            return self.send_json({"album": parts[1], "snapshots": snapshots(parts[1]), "notes": notes(parts[1])})
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
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
        except ValueError:
            return self.send_json({"error": "bad json"}, 400)
        if len(parts) == 3 and parts[0] == "api" and parts[2] == "notes":
            album = parts[1]
            snap = next((s for s in snapshots(album) if s["id"] == body.get("snap")), None)
            track = next((t for t in (snap or {}).get("tracks", []) if t["n"] == body.get("n")), None)
            text = str(body.get("text") or "").strip()
            if not track or not text:
                return self.send_json({"error": "snap, n and text are required"}, 400)
            note = {"op": "add", "id": uuid.uuid4().hex[:8], "at": now_iso(), "by": "harry", "snap": snap["id"],
                    "n": track["n"], "track": track["id"], "version": track.get("version"),
                    "t": round(float(body.get("t") or 0), 1), "text": text[:4000]}
            append_event(album, note)
            threading.Thread(target=notify, args=(album, note, track), daemon=True).start()
            return self.send_json({"ok": True, "id": note["id"]})
        if len(parts) == 5 and parts[0] == "api" and parts[2] == "notes" and parts[4] == "delete":
            append_event(parts[1], {"op": "delete", "id": parts[3], "at": now_iso()})
            return self.send_json({"ok": True})
        self.send_error(404)


def serve(host, port):
    srv = http.server.ThreadingHTTPServer((host, port), Handler)
    print(f"listen: serving {DATA} on http://{host}:{port}/", flush=True)
    srv.serve_forever()


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
    p.add_argument("--look")
    p = sub.add_parser("serve")
    p.add_argument("--host", default="127.0.0.1")
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
    p.add_argument("--by", default=os.environ.get("CHIRP_LISTEN_AUTHOR") or os.environ.get("USER", "agent"))
    a = ap.parse_args(argv)
    if a.cmd == "cut":
        cut(a.album, a.label)
    elif a.cmd == "video":
        videos(a.album, a.snap, {int(x) for x in a.ids.split(",")} if a.ids else None, a.look)
    elif a.cmd == "serve":
        serve(a.host, a.port)
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
        append_event(a.album, {"op": "reply", "id": a.id, "at": now_iso(), "by": a.by, "text": a.text, "done": a.done})
        print("listen: reply recorded")



if __name__ == "__main__":
    main()
