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

QUESTIONS (14 Nov, Harry: "hard to answer qs in chat - if you put them on the review site as side by side comparisons
with a way to give feedback as an answer I can review in batch"). A composer puts a by-ear question on the page with
its clips; Harry answers there (a choice, a line of text, or both), many in one sitting; the answers come back to the
asker verbatim as ONE caco message once he has been quiet for two minutes (cc chirp-eco).
  listen.py ask ALBUM --track N --title "the question" [--context TEXT] [--version v7] [--key NAME]
            [--ab "v6|v7=CLIP-ab.mp3"]... [--clip "the voice alone=CLIP.mp3"]... [--choice TEXT]... [--at SECONDS]
      --ab: ONE file holding the versions one after another with a silence between (the usual -ab clip) is cut at
            the silences into its parts, shown side by side; parts of equal length can be switched mid-phrase.
      --clip: one file, one player. Both may repeat; a question may have neither.
      --choice: the answers offered as buttons (he can always write instead). --at: where it is in the song, for an
            "open in Listen" link. --key: a later question with the same key REPLACES this one (a new version of
            the same passage), so the page never asks about a superseded clip.
  listen.py questions ALBUM [--open] [--track N] [--json]     the questions and every answer
  listen.py retire ALBUM QUESTION_ID [--reason TEXT]          take a question off the page

The page is tools/listen.html (read per request). Data: $CHIRP_LISTEN_DIR or ~/.local/state/chirp-eco/listen/ALBUM/
{snapshots/ID/snapshot.json + tNN.mp3/.mp4/.web,
notes.jsonl, questions.jsonl, questions/*.mp3}. notes.jsonl and questions.jsonl are append-only event logs (add /
reply / delete; ask / answer / retire / told), so concurrent writers never clobber.
"""
import argparse
import base64
import hashlib
import http.server
import json
import os
import re
import shutil
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


def reduce_questions(events):
    """Fold the questions.jsonl event log into questions (oldest first). ask creates (and retires an earlier open
    question with the same key: a new version of the same passage); answer keeps each person's latest; retire takes
    one off the page; told marks the answers already sent to the asker."""
    qs = {}
    for e in events:
        op, qid = e.get("op"), e.get("id")
        if op == "ask":
            if e.get("key"):
                for old in qs.values():
                    if old.get("key") == e["key"] and not old["retired"]:
                        old["retired"] = {"at": e.get("at"), "reason": f"replaced by {qid}"}
            qs[qid] = {**{k: v for k, v in e.items() if k != "op"}, "answers": {}, "retired": None}
        elif qid in qs and op == "answer":
            who = str(e.get("by") or "harry")
            qs[qid]["answers"][who.lower()] = {"by": who, "at": e.get("at"), "choice": e.get("choice") or "",
                                               "text": e.get("text") or "", "told": False}
        elif qid in qs and op == "retire":
            qs[qid]["retired"] = {"at": e.get("at"), "reason": e.get("reason") or ""}
        elif op == "told":
            for qid2, who, at in e.get("answers") or []:
                a = (qs.get(qid2) or {"answers": {}})["answers"].get(str(who).lower())
                if a and a["at"] == at:
                    a["told"] = True
    return sorted(qs.values(), key=lambda q: q.get("at", ""))


def untold(qs):
    """[(question, answer)] not yet sent to the asker, oldest answer first (retired questions' answers still go)."""
    out = [(q, a) for q in qs for a in q["answers"].values() if not a["told"]]
    return sorted(out, key=lambda qa: qa[1]["at"] or "")


def digest_text(album, pairs, public=None):
    """One message for a batch of answers: every answer verbatim under its question."""
    who = sorted({a["by"] for _, a in pairs})
    lines = [f"{' and '.join(w.upper() for w in who)} ANSWERED {len(pairs)} QUESTION{'S' if len(pairs) != 1 else ''} "
             f"on the review page ({album}). Verbatim:", ""]
    for i, (q, a) in enumerate(pairs, 1):
        where = " ".join(x for x in (q.get("track_title") or "", q.get("version") or "") if x)
        lines.append(f"{i}. [{where or album}] {q.get('title')}   (asked by {q.get('by')}, id {q['id']})")
        if a["choice"]:
            lines.append(f"   {a['by']} chose: {a['choice']}")
        if a["text"]:
            lines.append(f"   {a['by']} wrote: {a['text']}")
        lines.append("")
    lines.append(f"The page: {public or PUBLIC}#a={album}&v=questions")
    lines.append(f"All of them: python3 ~/.config/chirp/tools/listen.py questions {album}")
    return "\n".join(lines)


def split_points(silences, duration, parts):
    """Where to cut a file of `parts` takes laid end to end, as [(start, end)] of each take, or None. The silence the
    file opens or closes with is left off; for each inner boundary k/parts of the way through what remains, the
    silence whose middle is nearest it (and within a sixth of a take) is the gap between two takes."""
    lead = max([e for s, e in silences if s <= 0.05], default=0.0)
    tail = min([s for s, e in silences if e >= duration - 0.05 and s > lead], default=duration)
    inner = [(s, e) for s, e in silences if s > lead and e < tail]
    take = (tail - lead) / parts
    edges = [lead]
    for k in range(1, parts):
        want = lead + take * k
        near = [g for g in inner if abs((g[0] + g[1]) / 2 - want) <= take / 6 and g[0] >= edges[-1]]
        if not near:
            return None
        edges += min(near, key=lambda g: abs((g[0] + g[1]) / 2 - want))
    edges.append(tail)
    return [(edges[2 * i], edges[2 * i + 1]) for i in range(parts)]


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


def question_event(album, ev):
    os.makedirs(album_dir(album), exist_ok=True)
    line = json.dumps(ev, ensure_ascii=False) + "\n"
    with _LOCK, open(os.path.join(album_dir(album), "questions.jsonl"), "a") as f:
        f.write(line)


def questions(album):
    p = os.path.join(album_dir(album), "questions.jsonl")
    if not os.path.exists(p):
        return []
    with open(p) as f:
        return reduce_questions(json.loads(ln) for ln in f if ln.strip())


def probe_silences(path):
    """(duration, [(start, end)]) of an audio file: its silences of a quarter second or more (ffmpeg)."""
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                               capture_output=True, text=True, check=True).stdout.strip())
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "silencedetect=noise=-50dB:d=0.25",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: (-?[0-9.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", err)]
    return dur, list(zip(starts, ends + [dur] * (len(starts) - len(ends))))


def cut_parts(path, outs, probe=probe_silences, run=subprocess.run):
    """Cut a file of len(outs) takes laid end to end (silence between) into outs. Returns each part's length in
    seconds, or None when the silences are not where takes of equal length would leave them."""
    dur, sil = probe(path)
    spans = split_points(sil, dur, len(outs))
    if spans is None:
        return None
    for (a, b), out in zip(spans, outs):
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{a:.3f}", "-i", path, "-t", f"{b - a:.3f}",
             "-c:a", "libmp3lame", "-q:a", "2", out], check=True)
    return [round(b - a, 2) for a, b in spans]


def ask(album, n, title, context="", version="", key="", abs_=(), clips=(), choices=(), at=None, by=None, cut=cut_parts):
    """Put a question on the page. abs_: [("v6|v7", FILE)] cut into side-by-side parts; clips: [(label, FILE)].
    The media is copied into DATA/ALBUM/questions/ (the clips folder is cleared after a week). Returns the question."""
    title = str(title or "").strip()
    if not title:
        raise ValueError("a question needs a title")
    track = next((t for t in climb_tracks(album) if t["n"] == n), None) if n else None
    if n and not track:
        raise ValueError(f"{album} has no track {n}")
    qid = "q" + uuid.uuid4().hex[:7]
    d = os.path.join(album_dir(album), "questions")
    os.makedirs(d, exist_ok=True)
    media = []
    for gi, (labels, path) in enumerate(abs_):
        names = [x.strip() for x in labels.split("|") if x.strip()]
        if len(names) < 2 or not os.path.exists(path):
            raise ValueError(f"--ab wants 'A|B=FILE' with a file that exists: {labels}={path}")
        outs = [os.path.join(d, f"{qid}-{gi}{chr(97 + i)}.mp3") for i in range(len(names))]
        lens = cut(path, outs)
        if lens is None:
            raise ValueError(f"{os.path.basename(path)}: no silence where {len(names)} takes of equal length would meet; "
                             "give the takes as separate files with --clip")
        media.append({"sync": max(lens) - min(lens) <= 0.25,
                      "items": [{"label": nm, "src": os.path.basename(o), "secs": ln} for nm, o, ln in zip(names, outs, lens)]})
    for ci, (label, path) in enumerate(clips):
        if not os.path.exists(path):
            raise ValueError(f"no clip {path}")
        out = os.path.join(d, f"{qid}-c{ci}{os.path.splitext(path)[1].lower() or '.mp3'}")
        shutil.copyfile(path, out)
        media.append({"sync": False, "items": [{"label": label.strip(), "src": os.path.basename(out)}]})
    q = {"op": "ask", "id": qid, "at": now_iso(), "by": by or whoami(), "n": track["n"] if track else 0,
         "track": track["id"] if track else None, "track_title": track["title"] if track else "",
         "version": str(version or ""), "key": str(key or ""), "title": title[:400], "context": str(context or "")[:4000],
         "media": media, "choices": [str(c)[:200] for c in choices if str(c).strip()],
         "t": None if at is None else round(float(at), 1)}
    question_event(album, q)
    return q


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


def caco_send(target, body):
    env = {k: v for k, v in os.environ.items() if k not in ("CACO_AGENT_ID", "CACOPHONY_AGENT")}
    env["CACOPHONY_ACTOR"] = AGENTS["chirp-eco"]
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        f.write(body)
    try:
        r = subprocess.run(["caco", "msg", "send", "--project", "tools", "--target", target, "--no-tts", "--body-file", f.name],
                           env=env, capture_output=True, text=True, timeout=90)
        return r.returncode == 0, (r.stderr or r.stdout).strip()[-160:]
    except (OSError, subprocess.SubprocessError) as e:
        return False, repr(e)
    finally:
        os.unlink(f.name)


DIGEST_QUIET = float(os.environ.get("CHIRP_LISTEN_DIGEST_S", "120"))
_TIMERS = {}


def send_digest(album, send=None):
    """Send every answer not yet sent: one message to each asker with the answers to their questions, one to
    chirp-eco with all of them. An answer is marked told only when its asker's message went (or has no agent)."""
    send = send or caco_send
    pairs = untold(questions(album))
    if not pairs:
        return 0
    known = agents()
    by_asker = {}
    for q, a in pairs:
        by_asker.setdefault(q.get("by") or "", []).append((q, a))
    told = []
    with open(os.path.join(album_dir(album), "notify.log"), "a") as logf:
        for asker, group in by_asker.items():
            target = known.get(asker)
            ok, res = send(target, digest_text(album, group)) if target and target != known.get("chirp-eco") else (True, "no agent")
            logf.write(f"{now_iso()} answers x{len(group)} -> {asker or '?'}: {'ok' if ok else 'FAILED'} {res}\n")
            if ok:
                told += [[q["id"], a["by"], a["at"]] for q, a in group]
        if known.get("chirp-eco"):
            ok, res = send(known["chirp-eco"], digest_text(album, pairs))
            logf.write(f"{now_iso()} answers x{len(pairs)} -> chirp-eco: {'ok' if ok else 'FAILED'} {res}\n")
    if told:
        question_event(album, {"op": "told", "at": now_iso(), "answers": told})
    return len(told)


def schedule_digest(album, quiet=None):
    """(Re)start the album's quiet timer: the answers go as one message once nobody has answered for `quiet` s."""
    with _LOCK:
        t = _TIMERS.pop(album, None)
        if t:
            t.cancel()
        t = threading.Timer(DIGEST_QUIET if quiet is None else quiet, send_digest, [album])
        t.daemon = True
        _TIMERS[album] = t
        t.start()


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
            return self.send_json({"album": parts[1], "snapshots": snapshots(parts[1]), "notes": notes(parts[1]),
                                   "questions": questions(parts[1])})
        if len(parts) == 3 and parts[0] == "api" and parts[2] == "log" and re.fullmatch(r"[\w-]+", parts[1]):
            return self.send_json(worklog(parts[1]))
        if len(parts) == 4 and parts[0] == "media" and parts[2] == "release" and parts[3] == "album.mp4":
            return self.send_media(os.path.join(album_dir(parts[1]), "release", "album.mp4"))
        if len(parts) == 4 and parts[0] == "media" and parts[2] == "q" and re.fullmatch(r"q[0-9a-f]+-[\w]+\.(mp3|opus|ogg|wav)", parts[3]):
            return self.send_media(os.path.join(album_dir(parts[1]), "questions", parts[3]))
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
        kinds = {".mp3": "audio/mpeg", ".opus": "audio/ogg", ".ogg": "audio/ogg", ".wav": "audio/wav"}
        self.send_header("Content-Type", kinds.get(os.path.splitext(p)[1], "video/mp4"))
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
        if len(parts) == 5 and parts[0] == "api" and parts[2] == "questions" and parts[4] == "answer":
            q = next((x for x in questions(parts[1]) if x["id"] == parts[3]), None)
            choice, text = str(body.get("choice") or "").strip(), str(body.get("text") or "").strip()
            if not q or q["retired"]:
                return self.send_json({"error": "no such open question"}, 400)
            if choice and choice not in q["choices"]:
                return self.send_json({"error": "that is not one of the choices"}, 400)
            if not choice and not text:
                return self.send_json({"error": "a choice or some text is required"}, 400)
            question_event(parts[1], {"op": "answer", "id": q["id"], "at": now_iso(), "by": clean_name(body.get("by")),
                                      "choice": choice, "text": text[:4000]})
            schedule_digest(parts[1])
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
    for a in ALBUMS:                                  # answers given just before a restart still go to their askers
        if untold(questions(a)):
            schedule_digest(a)
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
    p = sub.add_parser("ask", help="put a by-ear question on the page, with its clips side by side")
    p.add_argument("album")
    p.add_argument("--track", type=int, default=0, help="the track's number on the album (0: the album)")
    p.add_argument("--title", required=True, help="the question, one line")
    p.add_argument("--context", default="", help="what changed, what to listen for (a few lines)")
    p.add_argument("--version", default="", help="the version it is about, as in v7")
    p.add_argument("--key", default="", help="a later question with the same key replaces this one")
    p.add_argument("--ab", action="append", default=[], metavar="'A|B=FILE'", help="one file of takes end to end, cut at its silences")
    p.add_argument("--clip", action="append", default=[], metavar="'LABEL=FILE'", help="one clip")
    p.add_argument("--choice", action="append", default=[], help="an answer offered as a button (repeatable)")
    p.add_argument("--at", type=float, help="where it is in the song, in seconds (an 'open in Listen' link)")
    p.add_argument("--by", help="who is asking (default: this shell's caco agent)")
    p = sub.add_parser("questions", help="the questions and every answer")
    p.add_argument("album")
    p.add_argument("--open", action="store_true", help="only questions nobody has answered")
    p.add_argument("--track", type=int)
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("retire", help="take a question off the page")
    p.add_argument("album")
    p.add_argument("id")
    p.add_argument("--reason", default="")
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
    elif a.cmd == "ask":
        def pair(tok, flag):
            label, sep, path = tok.rpartition("=")
            if not sep or not label.strip():
                raise SystemExit(f"listen: {flag} wants LABEL=FILE, as in {flag} 'v6|v7=clip-ab.mp3'")
            return label, os.path.expanduser(path)
        try:
            q = ask(a.album, a.track, a.title, a.context, a.version, a.key, [pair(t, "--ab") for t in a.ab],
                    [pair(t, "--clip") for t in a.clip], a.choice, a.at, a.by)
        except ValueError as e:
            raise SystemExit(f"listen: {e}") from None
        print(f"listen: question {q['id']} is on the page: {PUBLIC}#a={a.album}&v=questions&q={q['id']}")
    elif a.cmd == "questions":
        qs = [q for q in questions(a.album) if (a.track is None or q["n"] == a.track) and not (a.open and (q["answers"] or q["retired"]))]
        if a.json:
            return print(json.dumps(qs, ensure_ascii=False, indent=1))
        for q in qs:
            state = "RETIRED " + q["retired"]["reason"] if q["retired"] else ("answered" if q["answers"] else "OPEN")
            print(f"[{q['id']}] t{q['n']} {q.get('version') or ''} ({q['by']}, {q['at']})  {state}\n    {q['title']}")
            for ans in q["answers"].values():
                said = " | ".join(x for x in (ans["choice"], ans["text"]) if x)
                print(f"    -> {ans['by']} ({ans['at']}): {said}")
        print(f"listen: {len(qs)} question(s), {sum(1 for q in qs if not q['answers'] and not q['retired'])} open")
    elif a.cmd == "retire":
        if not any(q["id"] == a.id and not q["retired"] for q in questions(a.album)):
            raise SystemExit(f"no open question {a.id}")
        question_event(a.album, {"op": "retire", "id": a.id, "at": now_iso(), "reason": a.reason})
        print("listen: question retired")



if __name__ == "__main__":
    main()
