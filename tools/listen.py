#!/usr/bin/env python3
"""listen: Harry's album review app (chirp-eco, 6 Nov). Immutable SNAPSHOTS of an album in progress (each track's kept
song file rendered at seed 0 on the groove pin; a track whose song file is unchanged is hard-linked from the previous
snapshot, not re-rendered), a track-by-track player, NOTES at timestamps that stay on the track for whoever draws it, an
"open live in chirp web" link per track (the canonical song in the URL hash, rendered and drawn in the browser), and
best-effort 480p preview videos.

  listen.py cut ALBUM [--label TEXT]                 cut a snapshot (renders changed tracks at nice 15)
  listen.py video ALBUM [SNAP] [--ids 1,8] [--look accretion | '{id}|accretion3d'] [--redo | --stale]
                                                             480p previews (~1.3x real time each: an idle unit)
  listen.py serve [--host H]... [--port 8791]        the app (a note tells chirp-eco through caco); --host repeats
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
            [--parts ride:rb,hat] [--focus 4-11]
      THE PAGE SHOWS ONE QUESTION AT A TIME and plays it by itself, the takes in turn; an answer brings the next
      (Harry, 15 Nov: "questions are very busy and hard to even parse or answer"; "make it easy to respond, like a
      flick thru view w autoplay, maybe with shorter more focused examples"). So: the TITLE is the question and
      only the question, short (the page sets a title's last question large and what stands before it small);
      what changed goes first in --context, the measurements after it (they are folded away); the --ab is 6 to 10
      seconds ON THE CHANGE; one more clip at most; two to four choices of a few words.
      --ab: ONE file holding the versions one after another with a silence between (the usual -ab clip) is cut at
            the silences into its parts, shown side by side; parts of equal length can be switched mid-phrase.
            ANY NUMBER of takes: "first|made|middle=FILE", "1|2|3|4|5=FILE" (one label a take; the row wraps).
      --clip: one file, one player. Both may repeat; a question may have neither.
      --focus START-END: the seconds of the --ab takes the card plays first (the whole take is one press away).
            Without it the page finds them: from a second and a half before the takes first part, for 4 to 7
            seconds (focus_window; takes of 11 s or less are played whole). `ask` prints what it found.
      --parts: the tracks the question is ABOUT (a kit's piece as TRACK:PIECE). When it is answered, the message that
            brings the answer also says where else those parts play in the song as it then stands: an answer about
            one place is often an answer about a device (a ride-bell pendulum turned down in two passages went on
            opening the song for seven hours: chirper-zero, 15 Nov). A new track of a version not yet in songs/
            reads "not in the song now" when you ask; the line is read again when he answers, so the card stands.
      --choice: the answers offered as buttons (he can always write instead). --at: where it is in the song, for an
            "open in Listen" link. --key: a later question with the same key REPLACES this one (a new version of
            the same passage), so the page never asks about a superseded clip.
  listen.py questions ALBUM [--open] [--track N] [--json]     the questions and every answer
  listen.py questions ALBUM --focus      each live question's takes and the seconds the card plays first
  listen.py questions ALBUM --moved      the live ones whose passage of the song has moved since their clips were cut,
      the furthest first. Measured from the snapshots' audio (the same seconds on the question's version and now:
      the mean difference of the band envelopes in dB; under 0.15 it sounds as it did, from 0.6 it has changed),
      at every cut, and shown on the page's cards. Ask again with the same --key to replace a card's clips.
  listen.py retire ALBUM QUESTION_ID [--reason TEXT]          take a question off the page

THE STUDIO (22 Nov, Harry: "one single studio preview app with one persistent login system ... move :8790 content into
it, so i can see all in one place"): /studio/ serves $CHIRP_STUDIO_DIR (default ~/.local/state/chirp-eco/review: the
film's page and drafts, the video prototypes, the composers' clips) behind the same access code, so through the funnel
too. A folder is a page (newest first; a clip, its picture and its note together, with players; ?q= finds, ?p= pages,
?list shows the files of a folder that has its own index.html); a file is served as it is, with ranges. The old
port (--old-port, default 8790) redirects into /studio/, and absolute links to it inside served pages are rewritten.

The page is tools/listen.html (read per request). Data: $CHIRP_LISTEN_DIR or ~/.local/state/chirp-eco/listen/ALBUM/
{snapshots/ID/snapshot.json + tNN.mp3/.mp4/.web,
notes.jsonl, questions.jsonl, questions/*.mp3}. notes.jsonl and questions.jsonl are append-only event logs (add /
reply / delete; ask / answer / retire / told), so concurrent writers never clobber.
"""
import argparse
import base64
import email.utils
import gzip
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
GZIP_LEAST = 1024      # a page or JSON body this long is gzipped for a client that takes it
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
    one off the page; told marks the answers already sent to the asker; built says what was made of an answer, and
    in which version (a list on the question, oldest first; no key when nothing was)."""
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
        elif qid in qs and op == "built":
            # chirper-zero, 19 Nov: Harry said "I can't hear the bow", it was built in the next version, and the page
            # had nowhere to say so (reply is for notes): the answer stood there as if nothing had come of it.
            qs[qid].setdefault("built", []).append({"by": e.get("by") or "", "at": e.get("at"),
                                                    "version": e.get("version") or "", "text": e.get("text") or ""})
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


def digest_text(album, pairs, public=None, also=None):
    """One message for a batch of answers: every answer verbatim under its question. also(question) may give one more
    line for a question (where else its parts play), or None."""
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
        extra = also(q) if also else None
        if extra:
            lines.append(f"   {extra}")
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


def built(album, card, text, version="", by=None, at=None):
    """Say on the page what was made of an ANSWERED question: `card` is its id or its key (the newest answered question
    with that key, retired or not: a card asked again keeps its key). Returns the question. No new card is needed to
    tell Harry that what he asked for is done (his, 19 Nov: "try not to raise so many cards")."""
    qs = questions(album)
    q = next((x for x in qs if x["id"] == card), None) \
        or next((x for x in reversed(qs) if card and x.get("key") == card and x["answers"]), None)
    if q is None:
        raise ValueError(f"no question {card!r} on {album} (an id, or the key of an answered one: `listen.py questions {album}`)")
    if not q["answers"]:
        raise ValueError(f"question {q['id']} has no answer yet: there is nothing of his to have built")
    if not str(text).strip():
        raise ValueError("say what was built, in a line")
    question_event(album, {"op": "built", "id": q["id"], "at": at or now_iso(), "by": by or whoami(),
                           "version": version or current_versions(album).get(q.get("n"), ""), "text": str(text).strip()})
    return q


def questions(album):
    p = os.path.join(album_dir(album), "questions.jsonl")
    if not os.path.exists(p):
        return []
    with open(p) as f:
        return reduce_questions(json.loads(ln) for ln in f if ln.strip())


# ── has the passage a question is about moved since its clips were cut? ──
MOVED_LITTLE, MOVED = 0.15, 0.6      # dB (see envelope_diff): under the first the passage sounds as it did; from the
#                                      second on it has changed. On Common Time and Odd Sympathy (14 Nov): passages no
#                                      later version touched read 0.02-0.07; a snare re-routed or a mix trim 0.3-0.5;
#                                      a part swapped, rested or re-voiced 0.6-2.8.


def envelope_diff(a, b, sr=22050):
    """How differently two takes of the same seconds sound, in dB: the mean difference between their band envelopes
    (eight bands from 60 Hz to 11 kHz, 46 ms steps), the overall level difference taken out, over the steps and
    bands where either take sounds. Robust to the mp3 coder; 0 for the same audio at another gain. Needs numpy."""
    import numpy as np
    m = min(len(a), len(b))
    a, b = np.asarray(a[:m], float), np.asarray(b[:m], float)
    n, hop, edges = 2048, 1024, [60, 120, 250, 500, 1000, 2000, 4000, 8000, 11000]
    if m < n or not a.any() or not b.any():
        return None
    win, fr = np.hanning(n), np.fft.rfftfreq(n, 1 / sr)
    sel = [(fr >= lo) & (fr < hi) for lo, hi in zip(edges[:-1], edges[1:])]

    def env(x):
        rows = []
        for i in range(0, m - n + 1, hop):
            sp = np.abs(np.fft.rfft(x[i:i + n] * win)) ** 2
            rows.append([sp[k].sum() for k in sel])
        e = 10 * np.log10(np.array(rows) + 1e-12)
        return np.maximum(e, e.max() - 50.0), e > e.max() - 40.0
    (ea, la), (eb, lb) = env(a), env(b)
    level = 10 * np.log10(float(np.dot(b, b)) / float(np.dot(a, a)))
    live = la | lb
    return round(float(np.abs(eb - ea - level)[live].mean()), 2) if live.any() else 0.0


FOCUS_S = 7.0          # the longest stretch of an A/B a card plays first (Harry, 15 Nov: "shorter more focused examples")
FOCUS_MIN = 4.0        # and the shortest
FOCUS_LEAD = 1.5       # seconds of the passage before the takes part, so the change is heard arriving
FOCUS_SLACK = 4.0      # takes within this of the focus in length are played whole (an 11 s take is short enough)


def focus_window(takes, sr=22050, length=FOCUS_S, shortest=FOCUS_MIN, lead=FOCUS_LEAD, slack=FOCUS_SLACK):
    """(start, end) in seconds: the few seconds of two or more takes of ONE passage that say what differs, or None
    when the takes are short already (the window would leave under `slack` out) or cannot be compared.
    Band envelopes as envelope_diff (eight bands, 46 ms steps), each take against the first over the bands that
    sound in either, with the overall level difference taken out, smoothed over half a second. The window opens
    `lead` seconds before the takes first part (where the difference first reaches a third of its largest), on an
    attack of the first take when one lies within
    half a second before that, and runs to a second past where they last differ: at most `length`, at least
    `shortest`. It takes in the clip's start or end when it comes within a second of them. Needs numpy."""
    import numpy as np
    m = min((len(t) for t in takes), default=0)
    n, hop, edges = 2048, 1024, [60, 120, 250, 500, 1000, 2000, 4000, 8000, 11000]
    if len(takes) < 2 or m < max(shortest + slack, 2.0) * sr:
        return None
    win, fr = np.hanning(n), np.fft.rfftfreq(n, 1 / sr)
    sel = [(fr >= lo) & (fr < hi) for lo, hi in zip(edges[:-1], edges[1:])]

    def env(x):
        x = np.asarray(x[:m], float)
        rows = [[(np.abs(np.fft.rfft(x[i:i + n] * win)) ** 2)[k].sum() for k in sel] for i in range(0, m - n + 1, hop)]
        return 10 * np.log10(np.array(rows) + 1e-12)
    E = [env(t) for t in takes]
    top = max(float(e.max()) for e in E)                 # one floor for every take: only what sounds is compared
    E = [np.maximum(e, top - 50.0) for e in E]
    d = np.zeros(len(E[0]))
    for e in E[1:]:
        live = (e > top - 40.0) | (E[0] > top - 40.0)
        if not live.any():
            continue
        diff = e - E[0]
        d += np.where(live, np.abs(diff - np.median(diff[live])), 0.0).sum(1) / np.maximum(live.sum(1), 1)
    per = sr / hop                                        # steps a second
    k = max(1, int(round(0.5 * per)))
    d = np.convolve(d, np.ones(k) / k, mode="same")
    if d.max() <= 0:
        return None
    apart = np.nonzero(d >= d.max() / 3.0)[0]
    i = max(0, int(apart[0] - lead * per))
    level = 10 * np.log10((10 ** (E[0] / 10)).sum(1))
    lo = max(1, i - int(0.5 * per))
    if i > lo:                                           # open on an attack, not in the middle of a note
        rises = level[lo:i + 1] - level[lo - 1:i]
        if rises.max() >= 3.0:
            i = lo + int(np.argmax(rises))
    total = m / sr
    start = i / per
    start = 0.0 if start < 1.0 else max(0.0, start - 0.03)
    end = min(start + length, max(start + shortest, apart[-1] / per + 1.0))
    if total - end < 1.0:
        end = total
    if total - (end - start) < slack:
        return None
    return round(start, 2), round(end, 2)


def focus_file(album):
    return os.path.join(album_dir(album), "questions-focus.json")


def read_focus(album):
    try:
        return read_json(focus_file(album))
    except (OSError, ValueError):
        return {}


def refresh_focus(album, decode=None, log=print):
    """For every live question, the stretch of each group of side-by-side takes in which they differ most
    (focus_window), kept in DATA/ALBUM/questions-focus.json as {"QID|GROUP": [start, end] or null} for the server and
    the page. Only what is not measured yet is measured. Run by `ask`, `cut` and `questions --focus`."""
    decode = decode or (lambda path: decode_passage(path, 0.0, 600.0))
    old, new, done = read_focus(album), {}, 0
    for q in questions(album):
        if q["retired"]:
            continue
        for gi, g in enumerate(q.get("media") or []):
            if not g.get("sync") or len(g.get("items") or []) < 2:
                continue
            key = f"{q['id']}|{gi}"
            if key in old:
                new[key] = old[key]
                continue
            files = [os.path.join(album_dir(album), "questions", it["src"]) for it in g["items"]]
            try:
                w = focus_window([decode(f) for f in files]) if all(map(os.path.exists, files)) else None
                new[key] = list(w) if w else None
            except Exception as e:
                log(f"listen: {q['id']}: no focus for its takes ({e})")
                new[key] = None
            done += 1
    if new != old:
        tmp = focus_file(album) + ".tmp"
        with open(tmp, "w") as f:
            json.dump(new, f, indent=0, sort_keys=True)
        os.replace(tmp, focus_file(album))
    return done


def with_focus(qs, focus):
    """The questions with `focus` ([start, end] seconds) on each group of side-by-side takes that has one: the asker's
    own (`ask --focus`, on the first such group) before the measured one."""
    out = []
    for q in qs:
        media, first = [], True
        for gi, g in enumerate(q.get("media") or []):
            f = None
            if g.get("sync") and len(g.get("items") or []) > 1:
                f = (q.get("focus") if first else None) or (focus or {}).get(f"{q['id']}|{gi}")
                first = False
            media.append({**g, "focus": f} if f else g)
        out.append({**q, "media": media})
    return out


def decode_passage(path, t, dur, sr=22050):
    """dur seconds of an audio file from t, mono at sr, as a numpy array."""
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", f"{t:.3f}", "-t", f"{dur:.3f}", "-i", path, "-ac", "1",
                          "-ar", str(sr), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(float)


def passage_window(q):
    """(start, length) in seconds of the stretch of the song a question is about: from its --at, as long as its first
    cut clip (6 to 30 s; 12 when it has none)."""
    secs = next((it.get("secs") for g in q.get("media") or [] for it in g.get("items") or [] if it.get("secs")), None)
    return float(q["t"]), min(max(float(secs or 12.0), 6.0), 30.0)


def moved_key(q, snaps):
    """(cache key, the snapshot of the question's version, the newest snapshot, same song text?) or None when the
    question has no place in the song or its version was never in a snapshot."""
    if q.get("t") is None or not q.get("n") or not q.get("version"):
        return None
    mine = [(s["id"], t) for s in snaps for t in s.get("tracks") or [] if t.get("n") == q["n"]]
    of = [i for i, (_, t) in enumerate(mine) if t.get("version") == q["version"]]
    if not of:
        return None
    # A snapshot cut in the minute a version is recorded can carry the new LABEL over the OLD song (chirper-alpha,
    # 18 Nov: Plain Hunt's first "v22" snapshot had v21's text and audio; the true one came four minutes later, and
    # ph-tower-hunt read CHANGED by 2.51 dB against a song that had moved 0.05). So the version's own snapshot is the
    # first one labelled with it whose song text differs from the snapshot before the label appeared; when none does
    # (a version that changed no text), the first labelled one, as before.
    before = mine[of[0] - 1][1].get("sha") if of[0] else None
    then = next((mine[i] for i in of if before and mine[i][1].get("sha") and mine[i][1]["sha"] != before), mine[of[0]])
    now = mine[-1]
    a, b = then[1].get("sha") or then[0], now[1].get("sha") or now[0]      # by the song's text: a snapshot in which only
    return f"{q['id']}|{a}|{b}", then[0], now[0], a == b                   # another track moved makes nothing due


def moved_file(album):
    return os.path.join(album_dir(album), "questions-moved.json")


def read_moved(album):
    try:
        return read_json(moved_file(album))
    except (OSError, ValueError):
        return {}


def refresh_moved(album, decode=decode_passage, log=print):
    """Measure, for every live question with a place in the song, how far that passage of the song as it is now is
    from the passage as it was on the question's version (envelope_diff of the two snapshots' audio), and keep it in
    DATA/ALBUM/questions-moved.json for the server and the page. Only what is not measured yet is measured (a new
    snapshot of a track makes its questions due). Run by `cut`, `ask` and `questions --moved`; the server only
    reads the file. Returns how many were measured."""
    snaps, old, new, done = snapshots(album), read_moved(album), {}, 0
    for q in questions(album):
        k = None if q["retired"] else moved_key(q, snaps)
        if not k:
            continue
        key, then, now, same = k
        if key in old:
            new[key] = old[key]
            continue
        if same:
            new[key] = 0.0
        else:
            t, dur = passage_window(q)
            f = [os.path.join(album_dir(album), "snapshots", s, f"t{q['n']:02d}.mp3") for s in (then, now)]
            try:
                new[key] = envelope_diff(decode(f[0], t, dur), decode(f[1], t, dur)) if all(map(os.path.exists, f)) else None
            except Exception as e:                      # numpy or ffmpeg missing, a broken file: say so and go on
                log(f"listen: {q['id']}: the passage could not be compared ({e})")
                new[key] = None
        done += 1
    if new != old:
        tmp = moved_file(album) + ".tmp"
        with open(tmp, "w") as f:
            json.dump(new, f, indent=0, sort_keys=True)
        os.replace(tmp, moved_file(album))
    return done


def quiet_refresh_moved(album):
    """refresh_moved (and refresh_focus) for the commands whose own work must never fail or grow a line because of it."""
    try:
        refresh_moved(album, log=lambda *x: None)
        refresh_focus(album, log=lambda *x: None)
    except Exception as e:
        print(f"listen: the questions' passages were not compared ({e})", file=sys.stderr)


def with_now(qs, current, snaps=(), moved=None):
    """The questions, each with `now` (its track's current kept version, from {track number: version}), `behind`
    (how many kept versions on the song is; None when either is not vN) and `moved` (dB, see envelope_diff: how far
    the passage the question is about has moved since its clips were cut; None when not measured). A question's
    clips are its own copies, so it can always be answered; this says whether the song still sounds like them
    (chirper-zero's ask, 14 Nov: so Harry "could see that for himself")."""
    def num(v):
        m = re.fullmatch(r"v(\d+)", str(v or "").strip())
        return int(m.group(1)) if m else None
    out = []
    for q in qs:
        now = current.get(q.get("n"))
        a, b = num(q.get("version")), num(now)
        k = moved_key(q, snaps) if moved else None
        out.append({**q, "now": now, "behind": None if a is None or b is None else max(0, b - a),
                    "moved": (moved or {}).get(k[0]) if k else None})
    return out


def current_versions(album):
    """{track number: its current kept version} for an album, from climbs.json."""
    return {t["n"]: t["version"] for t in climb_tracks(album) if t.get("n") is not None and t.get("version")}


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


def parts_play(q, canon=None):
    """{part: [(first bar, last bar, True when the question's own place is in it)]} for the parts a question names
    (`parts`: tracks, or a kit's pieces as TRACK:PIECE), in the song as it stands now; {} when it names none, and
    None for a part with no notes. Bars are counted as chirp render counts them. Raises when the song cannot be read."""
    parts = [p for p in q.get("parts") or [] if p]
    if not parts or not q.get("track"):
        return {}
    import chirpbin
    import rests
    if canon is None:
        env = {k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"}
        r = subprocess.run([chirpbin.resolve(), "plan", "-f", os.path.join(ROOT, "songs", f"{q['track']}.yaml"), "--json"],
                           capture_output=True, text=True, env=env, cwd=ROOT, timeout=120)
        canon = json.loads(r.stdout)["data"]["canonical"]
    here = None
    if q.get("t") is not None:                       # the stretch the question's clip covers, in beats (a tempo map
        import tempoclock                            # is followed: bd-10e881; before, a mapped song had no line)
        clock = tempoclock.of(canon.get("tempo"))
        t, dur = passage_window(q)
        here = (clock.beats(t), clock.beats(t + dur))
    out = {}
    for p in parts:
        spans = rests.sounding(canon, p) if rests.notes_of(canon, p) else []
        runs = rests.rests(spans, 0.5)[0]
        out[p] = [(int(a // 4) + 1, int((b - 1e-6) // 4) + 1, here is not None and a < here[1] and b > here[0])
                  for a, b in runs] or None
    return out


def parts_line(q, play=parts_play):
    """The digest's line for a question that names its parts: where each plays now, the question's own place starred.
    None when it names none or the song cannot be read (the answer still goes)."""
    try:
        got = play(q)
    except Exception:                                # never hold an answer back for this
        return None
    if not got:
        return None
    said = []
    for p, runs in got.items():
        if not runs:
            said.append(f"{p}: not in the song now")
            continue
        said.append(f"{p}: bars " + ", ".join((f"{a}" if a == b else f"{a}-{b}") + ("*" if mine else "") for a, b, mine in runs))
    star = "; * = where this question is" if any(mine for runs in got.values() for _, _, mine in runs or []) else ""
    return f"WHERE ITS PARTS PLAY NOW ({'; '.join(said)}{star}). An answer about one place may be an answer about the device."


TITLE_LONG = 110       # characters: past this a card's title is more than its question


def card_notes(q):
    """What `ask` says about a new card as the page will show it: the seconds each group of takes opens on, and a
    title that is long. [] when there is nothing to say."""
    out = []
    for g in q.get("media") or []:
        secs = [it.get("secs") for it in g.get("items") or [] if it.get("secs")]
        if g.get("sync") and len(secs) > 1:
            f = g.get("focus")
            if not f:
                out.append(f"the takes ({max(secs):.0f} s) play whole")
            elif q.get("focus") == f:
                out.append(f"the takes ({max(secs):.0f} s) open on {f[0]:g} to {f[1]:g} s (yours)")
            else:
                out.append(f"the takes ({max(secs):.0f} s) open on {f[0]:g} to {f[1]:g} s, where they differ; "
                           "--focus START-END sets it yourself")
    if len(q.get("title") or "") > TITLE_LONG:
        out.append(f"the title is {len(q['title'])} characters. The page sets its last question large and the rest small; "
                   "a title that is only the question reads best, with what changed in --context")
    return out


def parts_hint(line):
    """What `ask` adds when a named part is not in the kept song yet: the card is fine, the line is read again later."""
    if line and "not in the song now" in line:
        return ("a part that is not in songs/ yet (a new track of a version not kept so far) is fine: the line is read "
                "again, on the song as it then stands, when he answers. No need to ask again.")
    return None


def ask(album, n, title, context="", version="", key="", abs_=(), clips=(), choices=(), at=None, by=None, cut=cut_parts,
        parts=(), focus=None):
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
    if [p for p in parts if str(p).strip()]:
        q["parts"] = [str(p).strip() for p in parts if str(p).strip()]
    if focus:                                         # the asker knows where the change is: seconds into the --ab takes
        a, b = float(focus[0]), float(focus[1])
        if not 0 <= a < b:
            raise ValueError("--focus wants START-END in seconds into the takes, as in --focus 4-11")
        q["focus"] = [round(a, 2), round(b, 2)]
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
    # No song has an owner (Harry, 18 Nov: "climbing should not have owenrs"; of notes: "they will get notes hwen they
    # next see the track"): a note is not sent to a composer. It stays open on its track, and `climb.py next` prints it
    # in the brief of whoever draws the song (climb.heard_lines). chirp-eco is told, as before.
    ids = [i for i in (agents().get("chirp-eco"),) if i]
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
            ok, res = (send(target, digest_text(album, group, also=parts_line))
                       if target and target != known.get("chirp-eco") else (True, "no agent"))
            logf.write(f"{now_iso()} answers x{len(group)} -> {asker or '?'}: {'ok' if ok else 'FAILED'} {res}\n")
            if ok:
                told += [[q["id"], a["by"], a["at"]] for q, a in group]
        if known.get("chirp-eco"):
            ok, res = send(known["chirp-eco"], digest_text(album, pairs, also=parts_line))
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


def album_links(album_id):
    """The album's own links for the page's bar: compose/ALBUM/links.json, a list of {"title", "url"[, "by"]}. A
    composer's page that is not this app's (a digest of a night's rounds, a listening order) is found where the
    questions are. Only http(s) URLs and titles of 60 characters or fewer are passed on; a file that does not parse
    gives none. (chirper-zero, 16 Nov: "what changed while you were away", generated from the climb files.)"""
    try:
        rows = read_json(os.path.join(ROOT, "compose", album_id, "links.json"))
    except (OSError, ValueError):
        return []
    out = []
    for r in rows if isinstance(rows, list) else []:
        if isinstance(r, dict) and isinstance(r.get("title"), str) and isinstance(r.get("url"), str) \
                and r["title"].strip() and len(r["title"]) <= 60 and re.fullmatch(r"https?://[^\s\"'<>]+", r["url"]):
            out.append({"title": r["title"].strip(), "url": r["url"], "by": re.sub(r"[^\w .-]", "", str(r.get("by") or ""))[:40]})
    return out[:6]


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


# ── the studio: the file server that was on :8790, inside this app (22 Nov) ─────────────────────────────────────────
# Harry, 22 Nov: "We have :8790 and :8791 - can we actually just merge these two things? just one single studio preview
# app with one persistent login system (the any-user / solofury one) behind the funnel and just move :8790 content into
# it, so i can see all in one place". :8790 was a bare file server (caddy) over ~/.local/state/chirp-eco/review: the
# film's page and drafts, the video prototypes, every composer's clips and notes; tailnet only, no login. The files
# stay where their writers put them; this app serves them under /studio/ behind its own gate, so they are also behind
# the funnel. A folder is shown as a page: newest first, a clip beside its note, with players. The old port answers
# with a redirect to here, and old absolute links inside pages are pointed here as they are served.

STUDIO = os.environ.get("CHIRP_STUDIO_DIR") or os.path.expanduser("~/.local/state/chirp-eco/review")
STUDIO_FILMS = os.path.expanduser("~/.local/state/chirp-video/film")   # the finished films: review.mp4 is a link into it
STUDIO_OLD_PORT = 8790
STUDIO_PER_PAGE = 60
STUDIO_NAMES = {"common-time": ("The film", "Common Time: the latest draft, scene by scene"),
                "proto": ("Video prototypes", "every draft, reel, sheet and study, with its note"),
                "clips": ("Clips", "the composers' before-and-after clips and their notes"),
                "accretion": ("Accretion", "the released film's page"),
                "tracks": ("Standby Amber: tracks", ""), "thumbs": ("Standby Amber: thumbnails", ""),
                "index.html": ("Standby Amber: the review page", "the old front page of :8790"),
                "review.mp4": ("Standby Amber: the film at 720p", "")}
STUDIO_KINDS = {".html": "text/html; charset=utf-8", ".txt": "text/plain; charset=utf-8", ".md": "text/plain; charset=utf-8",
                ".yaml": "text/plain; charset=utf-8", ".yml": "text/plain; charset=utf-8", ".json": "application/json; charset=utf-8",
                ".mp3": "audio/mpeg", ".opus": "audio/ogg", ".ogg": "audio/ogg", ".wav": "audio/wav", ".flac": "audio/flac",
                ".mp4": "video/mp4", ".webm": "video/webm", ".mov": "video/quicktime",
                ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp", ".gif": "image/gif"}
_OLD_URL = re.compile(rb"https?://(?:pocket4(?:\.miku-owl\.ts\.net)?|100\.104\.0\.14):8790/")
_APP_URL = re.compile(rb"https?://(?:pocket4(?:\.miku-owl\.ts\.net)?|100\.104\.0\.14):8791/")
STUDIO_IMG_INLINE = 1_500_000        # a picture this size or smaller is shown in the list; a larger one is a link


def studio_rewrite(body):
    """A page's absolute links to the old file server, and to this app by its tailnet name, as paths of this app: they
    then work from anywhere the page is read (the tailnet, the funnel)."""
    return _APP_URL.sub(b"/", _OLD_URL.sub(b"/studio/", body))


def studio_href(url):
    """One link (an album's links.json) the same way."""
    return studio_rewrite(url.encode()).decode()


def studio_roots(root=None, also=None):
    """Where a studio path may end: the tree itself, and what a link in it may lead to (this app's own data: the
    snapshots' joins; the video agent's finished films; $CHIRP_STUDIO_ALSO, colon-separated)."""
    more = [DATA, STUDIO_FILMS, *[x for x in os.environ.get("CHIRP_STUDIO_ALSO", "").split(":") if x]] if also is None else also
    return [os.path.realpath(x) for x in (root or STUDIO, *more)]


def studio_inside(p, roots):
    p = os.path.realpath(p)
    return os.path.exists(p) and any(p == base or p.startswith(base + os.sep) for base in roots)


def studio_path(parts, root=None, also=None):
    """The file or folder for /studio/PARTS, or None. Every part is a plain name (no '..', no hidden file, no
    separator); a link inside the tree is followed only to where studio_roots allows."""
    roots = studio_roots(root, also)
    names = [urllib.parse.unquote(x) for x in parts]
    if any(not n or n.startswith(".") or "/" in n or "\\" in n or "\0" in n for n in names):
        return None
    p = os.path.join(roots[0], *names)
    return os.path.realpath(p) if studio_inside(p, roots) else None


def studio_entries(d, roots=None):
    """[{name, dir, size, mtime}] for a folder: no hidden files, no dead links, no link to where it may not lead."""
    roots = roots or studio_roots()
    out = []
    try:
        names = os.listdir(d)
    except OSError:
        return out
    for name in names:
        if name.startswith("."):
            continue
        try:
            st = os.stat(os.path.join(d, name))
        except OSError:
            continue
        if os.path.islink(os.path.join(d, name)) and not studio_inside(os.path.join(d, name), roots):
            continue
        is_dir = os.path.isdir(os.path.join(d, name))
        out.append({"name": name, "dir": is_dir, "size": 0 if is_dir else st.st_size, "mtime": st.st_mtime})
    return out


def studio_groups(entries, d=None, q="", order="new"):
    """A folder as its page shows it: folders first, then files GROUPED BY NAME WITHOUT EXTENSION (a clip, its picture
    and its note are one thing), newest first (order 'name': by name). Each group: {stem, mtime, size, files,
    note}; the note is the group's .txt (its first 1500 characters). q keeps groups whose name or note has it."""
    dirs = sorted((e for e in entries if e["dir"]), key=lambda e: e["name"])
    groups = {}
    for e in entries:
        if e["dir"]:
            continue
        stem = os.path.splitext(e["name"])[0]
        g = groups.setdefault(stem, {"stem": stem, "mtime": 0, "size": 0, "files": [], "note": ""})
        g["files"].append(e)
        g["mtime"] = max(g["mtime"], e["mtime"])
        g["size"] += e["size"]
    for g in groups.values():
        g["files"].sort(key=lambda e: e["name"])
        txt = next((e for e in g["files"] if e["name"].endswith(".txt")), None)
        if txt and d and len(g["files"]) > 1:
            try:
                with open(os.path.join(d, txt["name"]), errors="replace") as f:
                    g["note"] = f.read(1500).strip()
            except OSError:
                pass
    out = list(groups.values())
    if q:
        ql = q.lower()
        out = [g for g in out if ql in g["stem"].lower() or ql in g["note"].lower()]
        dirs = [e for e in dirs if ql in e["name"].lower()]
    out.sort(key=(lambda g: g["stem"]) if order == "name" else (lambda g: (-g["mtime"], g["stem"])))
    return dirs, out


def human_size(n):
    for unit, k in (("GB", 1 << 30), ("MB", 1 << 20), ("kB", 1 << 10)):
        if n >= k:
            return f"{n / k:.1f} {unit}" if n < 10 * k else f"{n / k:.0f} {unit}"
    return f"{n} B"


def _h(text):
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _u(name):
    return urllib.parse.quote(name)


def studio_links(text):
    """A note's text for a page: escaped, its links live, and those to the old port or to this app made paths here."""
    def link(m):
        url = m.group(0).replace("&amp;", "&")
        return f'<a href="{_h(studio_href(url))}">{m.group(0)}</a>'
    return re.sub(r"https?://[^\s<>\"')]+[^\s<>\"').,;:]", link, _h(text))


STUDIO_CSS = """:root{--bg:#0b0d12;--panel:#12151d;--line:#262b38;--amber:#e8c27a;--hi:#ffd58a;--dim:#8f98aa;--text:#d6dbe6}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font:14px/1.45 system-ui,sans-serif}
a{color:var(--hi)}
header{
display:flex;gap:6px 14px;align-items:center;flex-wrap:wrap;padding:8px 14px;border-bottom:1px solid var(--line);
position:sticky;top:0;background:var(--bg);z-index:5}
header b{color:var(--hi);font-size:16px}
header a{text-decoration:none;white-space:nowrap}
header a.on{color:var(--bg);background:var(--amber);border-radius:5px;padding:2px 8px}
header form{margin-left:auto;display:flex;gap:6px}
input,select,button{
background:var(--panel);color:var(--amber);border:1px solid var(--line);border-radius:5px;font:inherit;padding:4px 8px}
main{padding:12px 16px;max-width:1100px}
.m{color:var(--dim);font-size:12px}
h2{font-size:16px;color:var(--hi);margin:0 0 4px}
.g{background:var(--panel);border:1px solid var(--line);border-radius:7px;padding:9px 12px;margin:8px 0}
.g .hd{display:flex;gap:10px;flex-wrap:wrap;align-items:baseline}
.g .hd b{color:var(--amber);font:13px ui-monospace,Menlo,Consolas,monospace;overflow-wrap:anywhere}
.g .note{white-space:pre-wrap;margin:6px 0;overflow-wrap:anywhere}
.g audio,.g video{width:100%;max-width:900px;display:block;margin:6px 0;background:#000;border-radius:4px}
.g img{max-width:100%;max-height:340px;display:block;margin:6px 0;border-radius:4px}
.g .fs a{margin-right:12px;font-size:12px;white-space:nowrap}
.hub{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:10px;margin:10px 0}
.hub a{display:block;text-decoration:none;background:var(--panel);border:1px solid var(--line);border-radius:7px;padding:12px 14px}
.hub a:hover{border-color:var(--amber)}
.hub a b{display:block;font-size:16px}
.hub a span{display:block;color:var(--text)}
.pg{display:flex;gap:14px;margin:14px 0;align-items:center}"""


def studio_bar(rel):
    top = rel.split("/")[0] if rel else ""
    links = [("/", "Review", None), ("/studio/common-time/", "Film", "common-time"), ("/studio/proto/", "Prototypes", "proto"),
             ("/studio/clips/", "Clips", "clips"), ("/studio/", "All", "")]
    return ("<header><b>chirpers</b>"
            + "".join(f'<a href="{href}"{" class=on" if key is not None and key == top else ""}>{label}</a>' for href, label, key in links))


def studio_page(rel, d, query, roots=None):
    """The page for a folder of the studio (rel: its path under /studio/, '' for the top)."""
    q = (query.get("q") or [""])[0].strip()[:80]
    order = "name" if (query.get("s") or [""])[0] == "name" else "new"
    try:
        page = max(1, int((query.get("p") or ["1"])[0]))
    except ValueError:
        page = 1
    dirs, groups = studio_groups(studio_entries(d, roots), d, q, order)
    here = "/studio/" + (rel + "/" if rel else "")
    out = [f'<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
           f"<title>chirpers - studio{': ' + _h(rel) if rel else ''}</title><style>{STUDIO_CSS}</style>", studio_bar(rel),
           f'<form method=get action="{_h(here)}"><input name=q value="{_h(q)}" placeholder="find in this folder" size=18>'
           f'<select name=s onchange="this.form.submit()"><option value=new>newest first</option>'
           f'<option value=name{" selected" if order == "name" else ""}>by name</option></select></form></header><main>']
    crumbs, path = ['<a href="/studio/">studio</a>'], "/studio/"
    for part in [x for x in rel.split("/") if x]:
        path += _u(part) + "/"
        crumbs.append(f'<a href="{path}">{_h(part)}</a>')
    out.append(f'<div class=m>{" / ".join(crumbs)}</div>')
    if not rel and not q:                                       # the top: what is here, by name
        out.append("<h2>Studio</h2><div class=m>Everything that was on :8790, in one place and behind the same sign-in: "
                   "the film, the video prototypes, the composers' clips. Old links to :8790 come here.</div><div class=hub>")
        known = list(STUDIO_NAMES)
        for e in sorted(studio_entries(d, roots), key=lambda e: (known.index(e["name"]) if e["name"] in known else 99, e["name"])):
            title, what = STUDIO_NAMES.get(e["name"], (e["name"], ""))
            inside = studio_entries(os.path.join(d, e["name"]), roots) if e["dir"] else []
            newest = max((x["mtime"] for x in inside), default=e["mtime"])
            count = f"{len(inside)} files, " if e["dir"] else ""
            out.append(f'<a href="{here}{_u(e["name"])}{"/" if e["dir"] else ""}"><b>{_h(title)}</b><span>{_h(what)}</span>'
                       f'<span class=m>{count}newest {time.strftime("%d %b %H:%M", time.localtime(newest))}</span></a>')
        out.append("</div></main>")
        return "".join(out)
    total = len(groups)
    groups = groups[(page - 1) * STUDIO_PER_PAGE:page * STUDIO_PER_PAGE]
    index = os.path.exists(os.path.join(d, "index.html"))
    pages = max(1, -(-total // STUDIO_PER_PAGE))
    out.append(f'<h2>{_h(STUDIO_NAMES.get(rel, (rel or "studio", ""))[0])}</h2><div class=m>{total} item{"s" if total != 1 else ""}'
               + (f' matching "{_h(q)}"' if q else "") + (f", page {page} of {pages}" if pages > 1 else "")
               + (f' &middot; <a href="{_h(here)}">this folder&#39;s own page</a>' if index else "") + "</div>")
    for e in dirs:
        out.append(f'<div class=g><div class=hd><b><a href="{here}{_u(e["name"])}/">{_h(e["name"])}/</a></b></div></div>')
    for g in groups:
        when = time.strftime("%a %d %b %H:%M", time.localtime(g["mtime"]))
        out.append(f'<div class=g><div class=hd><b>{_h(g["stem"])}</b><span class=m>{when} &middot; {human_size(g["size"])}</span></div>')
        if g["note"]:
            out.append(f'<div class=note>{studio_links(g["note"])}</div>')
        names = [e["name"] for e in g["files"]]
        poster = next((n for n in names if os.path.splitext(n)[1].lower() in (".jpg", ".jpeg", ".png", ".webp")), None)
        for e in g["files"]:
            ext, href = os.path.splitext(e["name"])[1].lower(), here + _u(e["name"])
            if STUDIO_KINDS.get(ext, "").startswith("audio/"):
                out.append(f'<audio controls preload=none src="{href}"></audio>')
            elif STUDIO_KINDS.get(ext, "").startswith("video/"):
                small = poster and next(x["size"] for x in g["files"] if x["name"] == poster) <= STUDIO_IMG_INLINE
                still = f' poster="{here}{_u(poster)}"' if small else ""
                out.append(f'<video controls preload=none{still} src="{href}"></video>')
            elif STUDIO_KINDS.get(ext, "").startswith("image/") and e["size"] <= STUDIO_IMG_INLINE:
                out.append(f'<a href="{href}"><img loading=lazy decoding=async src="{href}" alt=""></a>')
        files = "".join(f'<a href="{here}{_u(e["name"])}">{_h(e["name"])} <span class=m>{human_size(e["size"])}</span></a>'
                        for e in g["files"])
        out.append(f"<div class=fs>{files}</div></div>")
    if total > STUDIO_PER_PAGE:
        keep = "".join(f"&{k}={_u(v)}" for k, v in (("q", q), ("s", "name" if order == "name" else "")) if v)
        out.append("<div class=pg>" + (f'<a href="?p={page - 1}{keep}">&larr; newer</a>' if page > 1 else "")
                   + (f'<a href="?p={page + 1}{keep}">older &rarr;</a>' if page * STUDIO_PER_PAGE < total else "") + "</div>")
    out.append("</main>")
    return "".join(out)


STUDIO_BACK = (b'<a href="/studio/" style="position:fixed;right:10px;bottom:10px;z-index:99;background:#12151d;color:#ffd58a;'
               b'border:1px solid #262b38;border-radius:14px;padding:4px 10px;font:12px system-ui;text-decoration:none">'
               b"chirpers studio</a>")


class OldPort(http.server.BaseHTTPRequestHandler):
    """The old file server's port: every address there is now under /studio/ of the app."""
    app_port = 8791

    def log_message(self, fmt, *args):
        pass

    def do_GET(self):
        host = (self.headers.get("Host") or self.server.server_address[0]).rsplit(":", 1)[0]
        self.send_response(302)
        self.send_header("Location", f"http://{host}:{self.app_port}/studio{self.path if self.path.startswith('/') else '/'}")
        self.send_header("Content-Length", "0")
        self.end_headers()

    do_HEAD = do_GET


# ── server ─────────────────────────────────────────────────────────────────────────────────

class Handler(http.server.BaseHTTPRequestHandler):
    server_version = "chirp-listen"

    def log_message(self, fmt, *args):
        pass

    def send_body(self, b, kind, code=200):
        """A whole text body (the page, JSON), gzipped when the client takes it and it is worth it: the album's data is
        880 kB as JSON and 134 kB gzipped, and the page fetches it again after every answer; over a relay or a phone
        that is the wait (16 Nov: a client on a relayed link gave up on the worklog mid-body). A client that has gone
        away is not an error."""
        zipped = len(b) >= GZIP_LEAST and "gzip" in (self.headers.get("Accept-Encoding") or "").lower()
        if zipped:
            b = gzip.compress(b, 5)
        try:
            self.send_response(code)
            self.send_header("Content-Type", kind)
            if zipped:
                self.send_header("Content-Encoding", "gzip")
            self.send_header("Vary", "Accept-Encoding")
            self.send_header("Content-Length", str(len(b)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(b)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def send_json(self, obj, code=200):
        self.send_body(json.dumps(obj, ensure_ascii=False).encode(), "application/json; charset=utf-8", code)

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
                return self.send_body(f.read(), "text/html; charset=utf-8")
        if parts == ["favicon.ico"]:
            return self.send_error(404)
        if not self.authed():
            if parts[0] == "studio" and "text/html" in (self.headers.get("Accept") or ""):
                self.send_response(302)                         # a page of the studio: sign in on the app's page, then come back
                self.send_header("Location", "/#next=" + urllib.parse.quote(self.path, safe=""))
                self.send_header("Content-Length", "0")
                return self.end_headers()
            return self.send_json({"error": "access code"}, 401)
        if parts[0] == "studio":
            return self.studio(parts[1:], path, urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query, keep_blank_values=True))
        if parts == ["api", "albums"]:
            return self.send_json([album_info(a) for a in ALBUMS
                                   if os.path.exists(os.path.join(ROOT, "compose", a, "album.json")) or snapshots(a)])
        if len(parts) == 2 and parts[0] == "api":
            snaps = snapshots(parts[1])
            links = [dict(x, url=studio_href(x["url"])) for x in album_links(parts[1])]
            return self.send_json({"album": parts[1], "snapshots": snaps, "notes": notes(parts[1]), "links": links,
                                   "questions": with_focus(with_now(questions(parts[1]), current_versions(parts[1]),
                                                                    snaps, read_moved(parts[1])), read_focus(parts[1]))})
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

    def studio(self, parts, path, query):
        """/studio/…: a folder as a page (its own index.html when it has one, unless ?list or a search), a file as it is."""
        p = studio_path(parts)
        if p is None:
            return self.send_error(404)
        rel = "/".join(urllib.parse.unquote(x) for x in parts)
        if os.path.isdir(p):
            if not path.endswith("/"):                          # so that a page's relative links resolve inside it
                self.send_response(301)
                self.send_header("Location", path + "/")
                self.send_header("Content-Length", "0")
                return self.end_headers()
            index = os.path.join(p, "index.html")
            if rel and os.path.exists(index) and not any(k in query for k in ("list", "q", "p", "s")):
                p = index
            else:
                return self.send_body(studio_page(rel, p, query).encode(), "text/html; charset=utf-8")
        kind = STUDIO_KINDS.get(os.path.splitext(p)[1].lower(), "application/octet-stream")
        if kind.startswith(("text/", "application/json")) and os.path.getsize(p) <= 8 << 20:
            with open(p, "rb") as f:
                body = f.read()
            if kind.startswith("text/html"):
                body = studio_rewrite(body) + STUDIO_BACK
            return self.send_body(body, kind)
        return self.send_media(p, kind, True)

    def send_media(self, p, kind=None, cache=False):
        if ".." in p or not os.path.exists(p):
            return self.send_error(404)
        size = os.path.getsize(p)
        stamp = email.utils.formatdate(os.path.getmtime(p), usegmt=True)
        if cache and self.headers.get("If-Modified-Since") == stamp and not self.headers.get("Range"):
            self.send_response(304)
            return self.end_headers()
        rng = byte_range(self.headers.get("Range"), size)
        a, b = rng or (0, size - 1)
        self.send_response(206 if rng else 200)
        kinds = {".mp3": "audio/mpeg", ".opus": "audio/ogg", ".ogg": "audio/ogg", ".wav": "audio/wav"}
        self.send_header("Content-Type", kind or kinds.get(os.path.splitext(p)[1], "video/mp4"))
        if cache:
            self.send_header("Last-Modified", stamp)
            self.send_header("Cache-Control", "private, max-age=60")
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


def serve(hosts, port, old_port=0):
    """One server per host (e.g. the tailnet address and 127.0.0.1, which a Tailscale funnel proxies to). old_port: the
    file server's old port (8790), answered on every host but the loopback with a redirect into /studio/; if something
    still holds it, the app starts without it and says so."""
    hosts = [hosts] if isinstance(hosts, str) else list(hosts)
    srvs = [http.server.ThreadingHTTPServer((h, port), Handler) for h in hosts]
    for h in hosts if old_port else []:
        if h.startswith("127.") or h == "localhost":
            continue
        try:
            old = http.server.ThreadingHTTPServer((h, old_port), type("OldPortFor", (OldPort,), {"app_port": port}))
        except OSError as e:
            print(f"listen: the old port {h}:{old_port} is not free ({e}); no redirect from it", flush=True)
            continue
        threading.Thread(target=old.serve_forever, daemon=True).start()
        print(f"listen: http://{h}:{old_port}/… redirects to http://{h}:{port}/studio/…", flush=True)
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
    p.add_argument("--old-port", type=int, default=STUDIO_OLD_PORT,
                   help="the old file server's port, redirected into /studio/ (default 8790; 0: none)")
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
    p.add_argument("--ab", action="append", default=[], metavar="'A|B[|C...]=FILE'",
                   help="one file of takes end to end (two or more, a label each), cut at its silences")
    p.add_argument("--clip", action="append", default=[], metavar="'LABEL=FILE'", help="one clip")
    p.add_argument("--choice", action="append", default=[], help="an answer offered as a button (repeatable)")
    p.add_argument("--at", type=float, help="where it is in the song, in seconds (an 'open in Listen' link)")
    p.add_argument("--parts", default="", metavar="TRACK[:PIECE],...",
                   help="the tracks the question is about: its answer's message says where else they play")
    p.add_argument("--focus", metavar="START-END", help="the seconds of the --ab takes the card plays first")
    p.add_argument("--by", help="who is asking (default: this shell's caco agent)")
    p = sub.add_parser("questions", help="the questions and every answer")
    p.add_argument("album")
    p.add_argument("--open", action="store_true", help="only questions nobody has answered")
    p.add_argument("--track", type=int)
    p.add_argument("--json", action="store_true")
    p.add_argument("--moved", action="store_true",
                   help="only live questions whose passage of the song has moved since their clips were cut, the furthest first")
    p.add_argument("--focus", action="store_true", help="each live question's takes and the seconds the card plays first")
    p = sub.add_parser("built", help="say beside an answer what was made of it, and in which version (no new card)")
    p.add_argument("album")
    p.add_argument("card", help="the question's id, or its key")
    p.add_argument("text", help="what you did, in a line, with where to hear it")
    p.add_argument("--version", default="", help="the version it is in (default: the track's kept version now)")
    p.add_argument("--by", help="who built it (default: this shell's caco agent)")
    p = sub.add_parser("retire", help="take a question off the page")
    p.add_argument("album")
    p.add_argument("id")
    p.add_argument("--reason", default="")
    a = ap.parse_args(argv)
    if a.cmd == "cut":
        cut(a.album, a.label)
        quiet_refresh_moved(a.album)
    elif a.cmd == "video":
        videos(a.album, a.snap, {int(x) for x in a.ids.split(",")} if a.ids else None, a.look, redo=a.redo, stale=a.stale, lod=a.lod)
    elif a.cmd == "serve":
        serve(a.host or ["127.0.0.1"], a.port, a.old_port)
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
            focus = None
            if a.focus:
                m = re.fullmatch(r"\s*([0-9.]+)\s*-\s*([0-9.]+)\s*", a.focus)
                if not m:
                    raise ValueError("--focus wants START-END in seconds into the takes, as in --focus 4-11")
                focus = (float(m.group(1)), float(m.group(2)))
            q = ask(a.album, a.track, a.title, a.context, a.version, a.key, [pair(t, "--ab") for t in a.ab],
                    [pair(t, "--clip") for t in a.clip], a.choice, a.at, a.by, parts=a.parts.split(","), focus=focus)
        except ValueError as e:
            raise SystemExit(f"listen: {e}") from None
        quiet_refresh_moved(a.album)
        print(f"listen: question {q['id']} is on the page: {PUBLIC}#a={a.album}&v=questions&q={q['id']}")
        for line in card_notes(with_focus([q], read_focus(a.album))[0]):
            print("listen: " + line)
        if q.get("parts"):                           # say now what the answer's message will say, so a wrong name shows
            line = parts_line(q)
            print("listen: " + (line or "its parts could not be read in the song (check --parts and --track)"))
            if parts_hint(line):
                print("listen: " + parts_hint(line))
    elif a.cmd == "questions":
        qs = [q for q in questions(a.album) if (a.track is None or q["n"] == a.track) and not (a.open and (q["answers"] or q["retired"]))]
        if a.focus:
            refresh_focus(a.album)
            for q in with_focus([q for q in qs if not q["retired"]], read_focus(a.album)):
                for line in card_notes(q):
                    if line.startswith("the takes"):
                        print(f"[{q['id']}] t{q['n']} {q.get('version') or '':>4s}  key {q.get('key') or '-':16s} {line.split(',')[0]}")
            return
        if a.moved:
            refresh_moved(a.album)
            qs = [q for q in with_now(qs, current_versions(a.album), snapshots(a.album), read_moved(a.album))
                  if not q["retired"] and (q["moved"] or 0) >= MOVED_LITTLE]
            qs.sort(key=lambda q: (q["n"] or 0, -q["moved"]))
            if a.json:
                return print(json.dumps(qs, ensure_ascii=False, indent=1))
            for q in qs:
                how = "CHANGED" if q["moved"] >= MOVED else "the mix moved a little"
                print(f"[{q['id']}] t{q['n']} {q['version']} -> now {q['now']}  {q['moved']:.2f} dB  {how}  key {q.get('key') or '-'}"
                      f"  {'answered' if q['answers'] else 'OPEN'}\n    {q['title']}")
            return print(f"listen: {len(qs)} live question(s) whose passage has moved since their clips were cut "
                         f"({sum(1 for q in qs if q['moved'] >= MOVED)} changed; ask again with the same --key to replace a card's clips)")
        if a.json:
            return print(json.dumps(qs, ensure_ascii=False, indent=1))
        for q in qs:
            state = "RETIRED " + q["retired"]["reason"] if q["retired"] else ("answered" if q["answers"] else "OPEN")
            print(f"[{q['id']}] t{q['n']} {q.get('version') or ''} ({q['by']}, {q['at']})  {state}\n    {q['title']}")
            for ans in q["answers"].values():
                said = " | ".join(x for x in (ans["choice"], ans["text"]) if x)
                print(f"    -> {ans['by']} ({ans['at']}): {said}")
            for b in q.get("built") or []:
                print(f"    => BUILT {('in ' + b['version'] + ' ') if b['version'] else ''}by {b['by']} ({b['at']}): {b['text']}")
        print(f"listen: {len(qs)} question(s), {sum(1 for q in qs if not q['answers'] and not q['retired'])} open")
    elif a.cmd == "built":
        try:
            q = built(a.album, a.card, a.text, a.version, a.by)
        except ValueError as e:
            raise SystemExit(f"listen: {e}") from None
        print(f"listen: the page now says so beside his answer: {PUBLIC}#a={a.album}&v=questions&q={q['id']}")
    elif a.cmd == "retire":
        if not any(q["id"] == a.id and not q["retired"] for q in questions(a.album)):
            raise SystemExit(f"no open question {a.id}")
        question_event(a.album, {"op": "retire", "id": a.id, "at": now_iso(), "reason": a.reason})
        print("listen: question retired")



if __name__ == "__main__":
    main()
