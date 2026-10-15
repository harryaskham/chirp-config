#!/usr/bin/env python3
"""Hill-climb queue: the songs being reproduced, how many rounds each has had and what was tried — and,
for any climbing agent's next pass, one climb to work on, weighted towards the fewest rounds.

  climb.py add "Artist - Title" ["Artist - Title" …] [--url URL] [--genre G] [--note TEXT]
               [--priority P] [--by NAME]           request songs (a YouTube URL alone works too)
  climb.py next [--as NAME] [--peek] [--json] [--seed N]
                                                    pick this pass's climb (and say what to do)
  climb.py done ID --note TEXT [--score S --version vN] [--next TEXT] [--engine SHA]
               [--with FILE …] [--as NAME]          record the round (kept or not), hand off
  climb.py status [--json]                          every climb: status, rounds, best, last round, odds
  climb.py log ID [-n N]                            a climb's rounds
  climb.py set ID KEY=VALUE …                       edit a climb's fields (source, genre, metric, …)
  climb.py note ID TEXT [--next TEXT]               steer: a note in its history (not a round; `next` shows it)
  climb.py pause|resume|drop ID [--note TEXT]       take a climb out of (or back into) the queue

Sampling: weight = priority / (1 + rounds), halved for a climb another agent started in the last
30 min (spread, not a lock: two agents on one song is fine), ×0.3 for the climb you did last and
×0.6 for its genre (switch it up). Requested songs have no rounds, so they come up first.

State, in this repo (the tool commits its own files and pushes; --no-git to skip):
  climbs.json          the registry — the groove's playlist plays its `enabled` entries
  climbs/ID.jsonl      one line per round: round, at, who, score, version, kept, note, next
Runtime (not in git): $XDG_STATE_HOME/chirp/climb-starts.jsonl — who started what, when.
Who you are: --as NAME, else $CLIMB_AS, else the herdr pane, else the pi session."""
import fcntl
import json
import os
import random
import re
import subprocess
import sys
import time
from contextlib import contextmanager
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(HERE)
REG = os.path.join(ROOT, "climbs.json")
HIST = os.path.join(ROOT, "climbs")
STATE = os.path.join(os.environ.get("XDG_STATE_HOME") or os.path.expanduser("~/.local/state"), "chirp")
STARTS = os.environ.get("CLIMB_STARTS") or os.path.join(STATE, "climb-starts.jsonl")
SPREAD = 30 * 60
QUEUED = ("requested", "active")
SKILL = "the chirp-song-reproduction skill (tools repo: skills/chirp-song-reproduction/SKILL.md)"


def die(msg, code=2):
    print(f"climb: {msg}", file=sys.stderr)
    sys.exit(code)


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def age(iso):
    try:
        t = datetime.strptime(iso, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp()
    except (TypeError, ValueError):
        return "—"
    s = time.time() - t
    return f"{s / 60:.0f}m" if s < 3600 else f"{s / 3600:.0f}h" if s < 86400 else f"{s / 86400:.0f}d"


def whoami(args):
    return (opt(args, "--as") or os.environ.get("CLIMB_AS") or os.environ.get("HERDR_PANE_ID")
            or (os.environ.get("PI_SESSION_ID") or "")[:13] or f"{os.environ.get('USER', '?')}@{os.uname().nodename}")


def opt(a, k, d=None):
    return a[a.index(k) + 1] if k in a and a.index(k) + 1 < len(a) else d


def multi(a, k):
    """Values after a flag up to the next flag (`--with a b c`)."""
    if k not in a:
        return []
    out = []
    for x in a[a.index(k) + 1:]:
        if x.startswith("--"):
            break
        out.append(x)
    return out


def positional(a, flags_with_values):
    out, skip = [], False
    for i, x in enumerate(a):
        if skip:
            skip = False
            continue
        if x in flags_with_values:
            skip = True
            continue
        if x.startswith("--"):
            continue
        out.append(x)
    return out


# ── the registry ────────────────────────────────────────────────────────────────────────────

@contextmanager
def locked(name):
    """A host-wide lock (agents share this working tree)."""
    gitdir = os.path.join(ROOT, ".git")
    path = os.path.join(gitdir if os.path.isdir(gitdir) else STATE, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def load():
    with open(REG) as f:
        reg = json.load(f)
    for c in reg.get("climbs", []):
        normalise(c)
    return reg


def normalise(c):
    """Queue fields for entries from before the queue: an enabled climb is active; its rounds start
    from its version number (each kept version took at least one round)."""
    c.setdefault("status", "active" if c.get("enabled", True) else "paused")
    if "rounds" not in c:
        m = re.match(r"v(\d+)", str((c.get("best") or {}).get("version", "")))
        c["rounds"] = int(m.group(1)) if m else 0
    c.setdefault("priority", 1)
    return c


def save(reg):
    tmp = REG + ".tmp"
    with open(tmp, "w") as f:
        f.write(json.dumps(reg, indent=2, ensure_ascii=False) + "\n")
    os.replace(tmp, REG)


@contextmanager
def registry():
    """Read-modify-write the registry under the lock."""
    with locked("climbs-registry.lock"):
        reg = load()
        yield reg
        save(reg)


def find(reg, cid):
    for c in reg["climbs"]:
        if c["id"] == cid:
            return c
    die(f"no climb `{cid}` (have: {', '.join(c['id'] for c in reg['climbs'])})", 5)


def history(cid):
    path = os.path.join(HIST, f"{cid}.jsonl")
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]


def starts():
    try:
        with open(STARTS) as f:
            return [json.loads(l) for l in f if l.strip()]
    except OSError:
        return []


# ── git (the tool commits only its own paths) ───────────────────────────────────────────────

def git(*a):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True)


def commit(paths, msg, args):
    if "--no-git" in args or not os.path.isdir(os.path.join(ROOT, ".git")):
        return
    rel = [os.path.relpath(os.path.join(ROOT, p) if not os.path.isabs(p) else p, ROOT) for p in paths]
    with locked("climb-git.lock"):
        git("add", "--", *rel)
        c = git("commit", "-q", "-m", msg, "--", *rel)
        if c.returncode:
            if "nothing" not in (c.stdout + c.stderr):
                print(f"climb: not committed: {(c.stderr or c.stdout).strip()[:200]}", file=sys.stderr)
            return
        for _ in range(3):
            p = git("pull", "-q", "--rebase", "--autostash", "origin", "main")
            if p.returncode:
                git("rebase", "--abort")
                print(f"climb: committed locally; pull failed: {p.stderr.strip()[:200]}", file=sys.stderr)
                return
            if git("push", "-q", "origin", "HEAD:main").returncode == 0:
                return
        print("climb: committed locally; push lost three races (it goes with the next push)", file=sys.stderr)


# ── sampling ───────────────────────────────────────────────────────────────────────────────

def weights(reg, me):
    t = time.time()
    st = starts()
    mine = [s for s in st if s.get("who") == me]
    last = mine[-1] if mine else None
    out = {}
    for c in reg["climbs"]:
        if c["status"] not in QUEUED:
            continue
        w = float(c.get("priority", 1)) / (1 + c["rounds"])
        others = [s for s in st if s["id"] == c["id"] and s.get("who") != me and t - s.get("t", 0) < SPREAD]
        if others:
            w *= 0.5
        if last and last["id"] == c["id"]:
            w *= 0.3
        elif last and c.get("genre") and c.get("genre") == last.get("genre"):
            w *= 0.6
        out[c["id"]] = w
    return out


# ── commands ──────────────────────────────────────────────────────────────────────────────

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:48] or "song"


def youtube_title(url):
    """The video's title (best effort: yt-dlp via uv, as the skill's setup uses)."""
    for cmd in (["yt-dlp"], ["uv", "tool", "run", "yt-dlp"]):
        try:
            r = subprocess.run([*cmd, "--print", "title", "--skip-download", url], capture_output=True, text=True,
                               timeout=120, env={**os.environ, "SSL_CERT_FILE": os.environ.get("SSL_CERT_FILE", "/etc/ssl/certs/ca-certificates.crt")})
            if r.returncode == 0 and r.stdout.strip():
                return r.stdout.strip().splitlines()[-1]
        except (OSError, subprocess.TimeoutExpired):
            pass
    return None


def cmd_add(a):
    titles = positional(a, ("--url", "--genre", "--note", "--priority", "--by"))
    url = opt(a, "--url")
    if not titles and url:
        titles = [youtube_title(url) or url]
    if not titles:
        die('add "Artist - Title" … [--url URL] [--genre G] [--note TEXT] [--priority P]')
    if url and len(titles) > 1:
        die("--url goes with one song")
    added = []
    with registry() as reg:
        have = {c["id"] for c in reg["climbs"]}
        for t in titles:
            if t.startswith("http") and not url:
                url_, t = t, youtube_title(t) or t
            else:
                url_ = url
            artist, _, title = t.partition(" - ")
            if not title:
                artist, title = "", artist
            cid = slug(title) if not title.startswith("http") else "yt-" + slug(title.rsplit("=", 1)[-1])
            same = next((c["id"] for c in reg["climbs"] if slug(title) in slug(c.get("reference", ""))
                         and (not artist or slug(artist) in slug(c.get("reference", "")))), None)
            if same:
                print(f"climb: {t} is already a climb (`{same}`) — skipped", file=sys.stderr)
                continue
            if cid in have:
                cid = slug(f"{artist} {title}") if artist else cid
            if cid in have:
                print(f"climb: `{cid}` is already a climb — skipped", file=sys.stderr)
                continue
            c = {
                "id": cid,
                "song": f"songs/{cid}.yaml",
                "reference": f"{artist} — {title}" if artist else title,
                "source": url_,
                "owner": None,
                "metric": f"python3 tools/likeness.py sections ref/{cid}.wav OUT.wav $(cat tools/{cid}-sections.txt)",
                "best": None,
                "passes": 1,
                "enabled": False,
                "status": "requested",
                "rounds": 0,
                "priority": float(opt(a, "--priority", 1)),
                "genre": opt(a, "--genre"),
                "requested": {"by": opt(a, "--by") or os.environ.get("CLIMB_AS") or os.environ.get("USER", "?"),
                              "at": now_iso(), "note": opt(a, "--note")},
            }
            reg["climbs"].append(c)
            have.add(cid)
            added.append(cid)
    for cid in added:
        print(f"requested {cid}")
    if added:
        commit(["climbs.json"], f"climbs: request {', '.join(added)}", a)


def brief(c, hist):
    best = c.get("best") or {}
    lines = [f"{c['id']} — {c.get('reference', '')}",
             f"  {c['status']} · {c['rounds']} rounds · best {best.get('score', '—')} ({best.get('version', '—')})"
             f" · {c.get('genre') or 'genre unset'}",
             f"  song {c.get('song')}  metric: {c.get('metric') or '—'}"]
    if c.get("source"):
        lines.append(f"  source {c['source']}")
    req = c.get("requested") or {}
    if req.get("note"):
        lines.append(f"  request note: {req['note']}")
    if c["status"] == "requested":
        lines.append(
            f"  FIRST ROUND — set it up ({SKILL}, §Setup): find the official upload (record it: "
            f"`climb.py set {c['id']} source=URL genre=…`), reference audio to ref/{c['id']}.wav, stems, a tab if "
            f"there is one, tools/{c['id']}-sections.txt, a first songs/{c['id']}.yaml that plans with the groove's "
            f"binary; measure it, then `climb.py done {c['id']} --version v1 --score S --note … --next … "
            f"--with songs/{c['id']}.yaml tools/{c['id']}-sections.txt` (it joins the playlist).")
    else:
        lines.append(f"  this round: measure, pick the biggest gap, try a fix (engine/library/song — {SKILL}); commit the "
                     f"song only if it beats best; then `climb.py done {c['id']} --note … --next … [--score S --version vN "
                     f"--with {c.get('song')}]`.")
    for h in hist[-3:]:
        sc = f" {h['score']}" if h.get("score") is not None else ""
        tag = "NOTE" if h.get("steer") else f"r{h['round']}"
        lines.append(f"  {tag} {age(h['at'])} ago by {h['who']}{sc}{' kept' if h.get('kept') else ''}: {h['note']}")
    nxt = next((h["next"] for h in reversed(hist) if h.get("next")), None)
    if nxt:
        lines.append(f"  suggested next: {nxt}")
    return "\n".join(lines)


def cmd_next(a):
    me = whoami(a)
    reg = load()
    w = weights(reg, me)
    if not w:
        die("nothing queued (every climb is paused, dropped or done)", 1)
    rng = random.Random(int(opt(a, "--seed"))) if opt(a, "--seed") else random.Random()
    ids = list(w)
    cid = rng.choices(ids, weights=[w[i] for i in ids])[0]
    c = find(reg, cid)
    if "--peek" not in a:
        os.makedirs(os.path.dirname(STARTS), exist_ok=True)
        with locked("climb-starts.lock"), open(STARTS, "a") as f:
            f.write(json.dumps({"id": cid, "who": me, "t": time.time(), "at": now_iso(), "genre": c.get("genre")}) + "\n")
    if "--json" in a:
        print(json.dumps({"climb": c, "history": history(cid)[-5:], "odds": round(w[cid] / sum(w.values()), 3)}))
    else:
        print(f"next for {me} (odds {w[cid] / sum(w.values()):.0%}):\n{brief(c, history(cid))}")


def cmd_done(a):
    pos = positional(a, ("--note", "--score", "--version", "--next", "--engine", "--as", "--with"))
    if not pos:
        die("done ID --note TEXT [--score S --version vN] [--next TEXT] [--with FILE …]")
    cid, note = pos[0], opt(a, "--note")
    if not note:
        die("done needs --note (what you tried and what happened — the next agent reads it)")
    me = whoami(a)
    score = float(opt(a, "--score")) if opt(a, "--score") else None
    version = opt(a, "--version")
    with registry() as reg:
        c = find(reg, cid)
        best = c.get("best") or {}
        kept = score is not None and version is not None and (best.get("score") is None or score > float(best["score"]))
        c["rounds"] += 1
        h = {"round": c["rounds"], "at": now_iso(), "who": me, "score": score, "version": version, "kept": kept,
             "note": note, "next": opt(a, "--next"), "engine": opt(a, "--engine")}
        if kept:
            c["best"] = {**best, "score": score, "version": version, "commit": "see git log " + c["song"]}
            if opt(a, "--engine"):
                c["best"]["engine"] = opt(a, "--engine")
        if c["status"] == "requested" and os.path.exists(os.path.join(ROOT, c["song"])) and kept:
            c["status"], c["enabled"] = "active", True
        c["last"] = {"at": h["at"], "who": me}
        os.makedirs(HIST, exist_ok=True)
        with open(os.path.join(HIST, f"{cid}.jsonl"), "a") as f:
            f.write(json.dumps({k: v for k, v in h.items() if v is not None}, ensure_ascii=False) + "\n")
    print(f"{cid} round {h['round']}{f' — best {score} ({version})' if kept else ''}"
          f"{' — joins the playlist' if c.get('enabled') and h['round'] == 1 else ''}")
    commit(["climbs.json", f"climbs/{cid}.jsonl", *multi(a, "--with")],
           f"climbs: {cid} round {h['round']}{f' — {version} {score}' if kept else ''}: {note[:60]}", a)


def cmd_status(a):
    reg = load()
    w = weights(reg, whoami(a))
    tot = sum(w.values()) or 1
    st = starts()
    t = time.time()
    rows = []
    for c in reg["climbs"]:
        hist = history(c["id"])
        last = hist[-1] if hist else None
        on = sorted({s["who"] for s in st if s["id"] == c["id"] and t - s.get("t", 0) < SPREAD})
        rows.append({"id": c["id"], "status": c["status"], "rounds": c["rounds"], "best": (c.get("best") or {}).get("score"),
                     "genre": c.get("genre"), "playlist": bool(c.get("enabled")), "odds": round(w.get(c["id"], 0) / tot, 3),
                     "last": f"{age(last['at'])} ago by {last['who']}" if last else None, "now": on})
    if "--json" in a:
        print(json.dumps(rows))
        return
    print(f"{'climb':26} {'status':9} {'rounds':>6} {'best':>6} {'odds':>5}  {'genre':24} last round / working now")
    for r in sorted(rows, key=lambda r: -r["odds"]):
        tail = " · ".join(x for x in [r["last"], ("now: " + ", ".join(r["now"])) if r["now"] else None] if x)
        print(f"{r['id'][:26]:26} {r['status']:9} {r['rounds']:>6} {r['best'] if r['best'] is not None else '—':>6} "
              f"{r['odds']:>5.0%}  {(r['genre'] or '—')[:24]:24} {tail}{'' if r['playlist'] else '  (not in playlist)'}")


def cmd_log(a):
    pos = positional(a, ("-n",))
    if not pos:
        die("log ID [-n N]")
    for h in history(pos[0])[-int(opt(a, "-n", 20)):]:
        sc = f" {h['score']}" if h.get("score") is not None else ""
        print(f"{'NOTE' if h.get('steer') else 'r' + str(h['round'])} {h['at']} {h['who']}{sc}{' (' + h['version'] + ')' if h.get('version') else ''}"
              f"{' kept' if h.get('kept') else ''}: {h['note']}" + (f"\n    next: {h['next']}" if h.get("next") else ""))


def cmd_note(a):
    pos = positional(a, ("--next", "--as"))
    if len(pos) < 2:
        die("note ID TEXT [--next TEXT]")
    cid, text = pos[0], " ".join(pos[1:])
    with registry() as reg:
        c = find(reg, cid)
        h = {"round": c["rounds"], "at": now_iso(), "who": whoami(a), "note": text, "next": opt(a, "--next"), "steer": True}
        os.makedirs(HIST, exist_ok=True)
        with open(os.path.join(HIST, f"{cid}.jsonl"), "a") as f:
            f.write(json.dumps({k: v for k, v in h.items() if v is not None}, ensure_ascii=False) + "\n")
    print(f"{cid}: noted")
    commit(["climbs.json", f"climbs/{cid}.jsonl"], f"climbs: {cid} note: {text[:60]}", a)


def cmd_set(a):
    pos = positional(a, ())
    if len(pos) < 2:
        die("set ID KEY=VALUE … (values are JSON when they parse: priority=2, enabled=false)")
    with registry() as reg:
        c = find(reg, pos[0])
        for kv in pos[1:]:
            k, _, v = kv.partition("=")
            if k in ("id", "rounds"):
                die(f"`{k}` is kept by the tool")
            try:
                c[k] = json.loads(v)
            except ValueError:
                c[k] = v
    commit(["climbs.json"], f"climbs: {pos[0]} {' '.join(pos[1:])[:60]}", a)


def cmd_state(a, status):
    pos = positional(a, ("--note",))
    if not pos:
        die(f"{a[0] if a else 'pause'} ID")
    with registry() as reg:
        c = find(reg, pos[0])
        c["status"] = status
        if status == "dropped":
            c["enabled"] = False
        if opt(a, "--note"):
            c["status_note"] = opt(a, "--note")
    print(f"{pos[0]}: {status}")
    commit(["climbs.json"], f"climbs: {pos[0]} {status}", a)


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("status", "ls", "list"):
        return cmd_status(a[1:] if a else [])
    cmd, rest = a[0], a[1:]
    table = {"add": cmd_add, "request": cmd_add, "next": cmd_next, "done": cmd_done, "log": cmd_log, "set": cmd_set,
             "note": cmd_note,
             "pause": lambda r: cmd_state(r, "paused"), "resume": lambda r: cmd_state(r, "active"),
             "drop": lambda r: cmd_state(r, "dropped")}
    if cmd in ("-h", "--help", "help"):
        print(__doc__)
        return
    if cmd not in table:
        die(f"unknown command `{cmd}` — {', '.join(table)} or status")
    table[cmd](rest)


if __name__ == "__main__":
    main()
