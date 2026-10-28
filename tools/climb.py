#!/usr/bin/env python3
"""Hill-climb queue: the songs being reproduced, how many rounds each has had and what was tried — and,
for any climbing agent's next pass, one climb to work on, weighted towards the fewest rounds.

  climb.py add "Artist - Title" ["Artist - Title" …] [--url URL] [--genre G] [--note TEXT]
               [--priority P] [--by NAME]           request songs (a YouTube URL alone works too)
               [--ref FILE|HOST:/PATH] [--album A --track N --artist A --year Y]
                                                    … with our own copy of a reference file (its tags fill
                                                    the metadata), converted to ref/ID.wav
  climb.py add-album SOURCE [--album A --artist A --year Y] [--genre G] [--note TEXT] [--priority P]
                                                    request every track of an album, in order: SOURCE is a
                                                    folder of audio files (local, or HOST:/PATH via scp) or a
                                                    playlist URL; copies the originals to ref/albums/ALBUM/ and
                                                    each reference to ref/ID.wav (one master for the album)
  climb.py art ALBUM [--url URL | --file F] [--px 32] [--colors 16]
                                                    the album's cover as pixel art (art/SLUG.json: a
                                                    palette and pixel indices; players draw it as blocks,
                                                    as a TUI would): from the iTunes search unless given;
                                                    the original is kept in ref/albums/SLUG/
  climb.py refs ALBUM SOURCE                        replace an album's references (matched by track number),
                                                    e.g. with better files; notes each climb to re-measure
  climb.py next [--as NAME] [--peek] [--take ID] [--include-owned] [--json] [--seed N]
                                                    pick this pass's climb (and say what to do); skips climbs
                                                    another agent owns (--include-owned draws them too);
                                                    --peek records no start, --take ID starts exactly that one
  climb.py done ID --note TEXT [--score S --version vN] [--next TEXT] [--engine SHA]
               [--with FILE …] [--render WAV] [--as NAME] [--force]
                                                    record the round (kept or not), hand off; --with refuses
                                                    files changed after another agent started this climb
                                                    (unless --force); --render records a kept album
                                                    version's edges (tools/albumedges.py)
  climb.py status [--json]                          every climb: status, rounds, best, last round, odds
  climb.py log ID [-n N]                            a climb's rounds
  climb.py set ID KEY=VALUE …                       edit a climb's fields (source, genre, metric, …)
  climb.py note ID TEXT [--next TEXT] [--fresh]     steer: a note in its history (not a round; `next` shows it);
                                                    --fresh: `next` shows nothing older (a fresh start;
                                                    the full history stays in `climb.py log`)
  climb.py pause|resume|drop ID [--note TEXT]       take a climb out of (or back into) the queue
  climb.py tui                                      the queue as a TUI: toggle climbable/playlist, focus, notes
  climb.py focus ALBUM | --ids ID,ID… | --off       climb only that album (or those climbs): pause every other
                                                    queued climb; --off resumes what a focus paused
                                                    (marked, so --off resumes exactly those); the playlist
                                                    is unchanged
  climb.py commit -m MSG PATH …                     commit those paths only and publish (below)
  climb.py publish                                  push this tree's local commits (a retry: records nothing)
Out of band: `add --oob` (or `set ID oob=true`) makes a test climb that `next` never picks and that never
joins the playlist; agents can still climb it (and any paused climb) directly when asked.

Sampling: weight = priority / (1 + rounds); a climb another agent started in the last 90 min without
recording a round since is held (skipped while anything else is queued; halved otherwise; a soft hold, not a lock), ×0.3 for the climb you did last and
×0.6 for its genre (switch it up). Requested songs have no rounds, so they come up first — but a
song's setup is one agent's job: one with no rounds that another agent started in the last 2 h is
skipped (it writes shared unversioned paths) until that first round is done.

Publishing (bd-d30a90): the tree is shared, so nothing ever stashes another agent's uncommitted work. Commits take
only their own paths; when origin is ahead, a clean tree rebases, a tree with others' edits replays the commits in a
scratch worktree, pushes from there and moves this tree over only the upstream-changed paths (refusing if one of them
is edited here; every other index entry, a foreign staged edit included, stays as it was). If the push cannot happen the receipt says so — the record is committed locally; retry with
`climb.py publish`, never by re-running the command (that would record the round twice).

State, in this repo (the tool commits its own files and pushes; --no-git to skip):
  climbs.json          the registry — the groove's playlist plays its `enabled` entries
  climbs/ID.jsonl      one line per round: round, at, who, score, version, kept, note, next
Runtime (not in git): $XDG_STATE_HOME/chirp/climb-starts.jsonl — who started what, when.
Who you are: --as NAME, else $CLIMB_AS, else the herdr pane, else the pi session."""
import fcntl
import calendar
import json
import os
import random
import re
import shutil
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
# How long a started round holds its climb against other agents (until its `done`, a note-free round record, or
# this long): rounds got slower and more careful; in 3 days 26% of 513 ran past 30 min (median 17, p90 46, 5% over
# an hour), and a queue handing the climb on mid-round made two agents work one song (We Are the Music Makers).
ROUND_HOLD = 90 * 60
# A song's setup (its first round) writes unversioned shared paths — ref/ID.wav, stems, songs/ID.yaml,
# tools/ID-sections.txt — so one agent sets it up: `next` skips a song with no rounds that another agent
# started within this long (it expires on its own and ends with that round's `done`).
SETUP_HOLD = 2 * 3600
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


def tracked_dirty():
    """Tracked paths with uncommitted changes (index or working tree): another agent's active work."""
    out = git("status", "--porcelain=v1", "-z", "--untracked-files=no").stdout.split("\0")
    paths, i = [], 0
    while i < len(out):
        e = out[i]
        if e:
            paths.append(e[3:])
            if e[0] in "RC":   # a rename or copy: the next field is its source
                i += 1
        i += 1
    return paths


def _advance(old, new):
    """Move this tree from `old` to `new` touching only the paths that differ between them (index and file), and
    only when none of those carries uncommitted work; every other index entry - a foreign staged edit included - is
    left exactly as it was (`reset --keep` would reset the whole index). → None, or why it did not move."""
    changed = [p for p in git("diff", "--name-only", "--no-renames", "-z", old, new).stdout.split("\0") if p]
    busy = sorted(set(changed) & set(tracked_dirty()))
    if busy:
        return f"{', '.join(busy[:3])} {'is' if len(busy) == 1 else 'are'} edited here and changed upstream"
    u = git("update-ref", "-m", "climb publish: advance to the published commit", "HEAD", new, old)
    if u.returncode:
        return f"HEAD moved meanwhile: {u.stderr.strip()[:120]}"
    keep = [p for p in changed if git("cat-file", "-e", f"{new}:{p}").returncode == 0]
    gone = [p for p in changed if p not in keep]
    if keep:
        git("checkout", new, "--", *keep)
    if gone:
        git("rm", "-q", "--ignore-unmatch", "--", *gone)
    return None


def _replay_elsewhere(ahead):
    """Origin is ahead and the tree holds others' edits: replay `ahead` (oldest first) on origin/main in a scratch
    worktree and push from there, then move this tree to it with _advance (no stash). → (pushed, receipt)."""
    import tempfile
    tmp = tempfile.mkdtemp(prefix="climb-publish-")
    wt = lambda *a: subprocess.run(["git", *a], cwd=tmp, capture_output=True, text=True)   # noqa: E731
    try:
        w = git("worktree", "add", "-q", "--detach", tmp, "origin/main")
        if w.returncode:
            return False, f"scratch worktree failed: {w.stderr.strip()[:160]}"
        for c in ahead:
            cp = wt("cherry-pick", "--allow-empty", c)
            if cp.returncode:
                wt("cherry-pick", "--abort")
                return False, f"{c[:7]} conflicts with origin/main: {(cp.stdout + cp.stderr).strip()[:160]}"
        if wt("push", "-q", "origin", "HEAD:main").returncode:
            return False, "race"
        new = wt("rev-parse", "HEAD").stdout.strip()
        stuck = _advance(git("rev-parse", "HEAD").stdout.strip(), new)
        if stuck:
            return True, (f"pushed {new[:7]}, but this tree stays where it was: {stuck} (`climb.py publish` again once "
                          "that is committed)")
        return True, f"pushed {new[:7]} (replayed beside others' uncommitted edits, none stashed)"
    finally:
        git("worktree", "remove", "--force", tmp)
        shutil.rmtree(tmp, ignore_errors=True)


def publish(attempts=5):
    """Push this tree's local commits to origin main without stashing anyone's work (bd-d30a90).
    → (True, receipt) when origin has them, (False, why) when they stay local."""
    for attempt in range(attempts):
        # one named ref, no FETCH_HEAD (others' fetches in this tree can leave it naming several branches)
        f = git("fetch", "-q", "--no-write-fetch-head", "origin", "refs/heads/main:refs/remotes/origin/main")
        if f.returncode:
            return False, f"fetch failed: {f.stderr.strip()[:160]}"
        # commits whose change is not upstream yet (an equivalent replay already pushed does not count)
        ahead = git("rev-list", "--reverse", "--cherry-pick", "--right-only", "--no-merges", "origin/main...HEAD").stdout.split()
        behind = git("rev-list", "HEAD..origin/main").stdout.split()
        if not ahead:
            if behind and git("merge", "-q", "--ff-only", "--no-autostash", "origin/main").returncode:
                return True, "nothing to push (this tree is behind origin and could not fast-forward past local edits)"
            return True, "nothing to push"
        if behind:
            if tracked_dirty():
                ok, why = _replay_elsewhere(ahead)
                if why == "race" and attempt < attempts - 1:
                    continue
                return ok, ("push lost every race" if why == "race" else why)
            r = git("rebase", "-q", "--no-autostash", "origin/main")   # a clean tree; never autostash, whatever the config
            if r.returncode:
                git("rebase", "--abort")
                return False, f"rebase onto origin/main conflicts: {(r.stdout + r.stderr).strip()[:160]}"
        if git("push", "-q", "origin", "HEAD:main").returncode == 0:
            return True, f"pushed {git('rev-parse', '--short', 'HEAD').stdout.strip()}"
        time.sleep(1 + attempt)
    return False, "push lost every race"


def commit(paths, msg, args):
    """True when the change is in a commit (pushed, or local with an honest receipt and `climb.py publish` to retry);
    False when nothing was committed - callers must then fail loudly, or the registry edit can be lost to the next
    agent's sync. Never stashes another agent's uncommitted work (bd-d30a90)."""
    if "--no-git" in args or not os.path.isdir(os.path.join(ROOT, ".git")):
        return True
    rel = [os.path.relpath(os.path.join(ROOT, p) if not os.path.isabs(p) else p, ROOT) for p in paths]
    with locked("climb-git.lock"):
        for attempt in range(6):
            git("add", "--", *rel)
            c = git("commit", "-q", "-m", msg, "--", *rel)
            if c.returncode == 0:
                break
            out = c.stdout + c.stderr
            if "nothing" in out:
                return True
            # another agent's git op in the shared tree (sync, status, pull) can hold .git/index.lock for a moment
            if "index.lock" in out and attempt < 5:
                time.sleep(1 + attempt)
                continue
            print(f"climb: not committed: {out.strip()[:200]}", file=sys.stderr)
            return False
        ok, why = publish()
        if not ok:
            sha = git("rev-parse", "--short", "HEAD").stdout.strip()
            print(f"climb: committed locally as {sha} but NOT pushed: {why}. The record is safe in git; retry with "
                  "`python3 tools/climb.py publish` - do not re-run this command (it would record it twice)", file=sys.stderr)
        return True


def commit_or_die(paths, msg, args):
    if not commit(paths, msg, args):
        die("NOT recorded in git (see 'not committed' above): the registry edit is only in the working tree "
            "and the next sync can drop it - fix the git state and re-run (with --force for done)", 4)


# ── sampling ───────────────────────────────────────────────────────────────────────────────

def weights(reg, me):
    """Draw weights. A climb another agent started under ROUND_HOLD ago and has not recorded a round on since is HELD:
    it is skipped while anything unheld is queued (two agents on one climb duplicate the round - chirper-two drew
    entrapment and imprint while chirper-three held them); when every candidate is held, held ones are drawn at
    half weight as before."""
    t = time.time()
    st = starts()
    mine = [s for s in st if s.get("who") == me]
    last = mine[-1] if mine else None
    out, held = {}, set()
    for c in reg["climbs"]:
        if c["status"] not in QUEUED or c.get("oob"):
            continue
        if c["rounds"] == 0 and any(s["id"] == c["id"] and s.get("who") != me and t - s.get("t", 0) < SETUP_HOLD
                                    for s in st):
            continue  # someone is setting it up
        w = float(c.get("priority", 1)) / (1 + c["rounds"])
        others = [s for s in st if s["id"] == c["id"] and s.get("who") != me and t - s.get("t", 0) < ROUND_HOLD]
        lr = c.get("last") or {}
        try:
            lr_t = calendar.timegm(time.strptime(lr.get("at", ""), "%Y-%m-%dT%H:%M:%SZ"))
        except ValueError:
            lr_t = 0
        if any(not (lr.get("who") == s.get("who") and lr_t >= s.get("t", 0) - 1) for s in others):
            held.add(c["id"])
        if others:
            w *= 0.5
        if last and last["id"] == c["id"]:
            w *= 0.3
        elif last and c.get("genre") and c.get("genre") == last.get("genre"):
            w *= 0.6
        out[c["id"]] = w
    free = {k: v for k, v in out.items() if k not in held}
    return free if free else out


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


# ── references: our own copies (never rely on a share or a URL staying up) ──────────────────

AUDIO = (".flac", ".mp3", ".m4a", ".ogg", ".opus", ".wav", ".aiff", ".aif", ".wma", ".webm")
REMOTE = re.compile(r"^[\w.@-]+:/")


def ytdlp(*args, timeout=900):
    for cmd in (["yt-dlp"], ["uv", "tool", "run", "yt-dlp"]):
        try:
            return subprocess.run([*cmd, *args], capture_output=True, text=True, timeout=timeout, env={
                **os.environ, "SSL_CERT_FILE": os.environ.get("SSL_CERT_FILE", "/etc/ssl/certs/ca-certificates.crt")})
        except FileNotFoundError:
            continue
    die("yt-dlp not found (nor uv)")


def tags(path):
    """Artist, album, title, track and year from a file's tags (ffprobe), lower-cased keys."""
    r = subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", path],
                       capture_output=True, text=True, stdin=subprocess.DEVNULL)
    try:
        d = json.loads(r.stdout)
    except ValueError:
        return {}
    t = {k.lower(): v for k, v in (d.get("format", {}).get("tags") or {}).items()}
    for st in d.get("streams", []):  # ogg/opus keep tags on the stream
        t.update({k.lower(): v for k, v in (st.get("tags") or {}).items() if k.lower() not in t})
    track = re.match(r"\d+", str(t.get("track") or t.get("tracknumber") or ""))
    year = re.match(r"\d{4}", str(t.get("date") or t.get("year") or t.get("originaldate") or ""))
    return {k: v for k, v in {
        "artist": t.get("album_artist") or t.get("albumartist") or t.get("artist"),
        "album": t.get("album"), "title": t.get("title"),
        "track": int(track.group()) if track else None, "year": int(year.group()) if year else None,
    }.items() if v}


def copy_in(src, dest_dir):
    """Our own copy of SRC (a local path, or HOST:/PATH over scp) in DEST_DIR; returns its path."""
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, os.path.basename(src.split(":", 1)[1] if REMOTE.match(src) else src))
    if REMOTE.match(src):
        r = subprocess.run(["scp", "-q", "-o", "BatchMode=yes", src, dest], capture_output=True, text=True, stdin=subprocess.DEVNULL)
        if r.returncode:
            die(f"scp {src}: {r.stderr.strip()[:200]}")
    else:
        shutil.copy2(src, dest)
    return dest


def to_wav(src, cid):
    """ref/ID.wav at the metric's format (48 kHz, 16-bit stereo) from any audio file."""
    out = os.path.join(ROOT, "ref", f"{cid}.wav")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-vn", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", out],
                       capture_output=True, text=True, stdin=subprocess.DEVNULL)
    if r.returncode:
        die(f"ffmpeg {src}: {r.stderr.strip()[:200]}")
    return out


def album_files(source, album_dir, meta):
    """[(path, tags)] for an album SOURCE, copied into ALBUM_DIR, in track order."""
    out = []
    if source.startswith("http"):
        d = ytdlp("--flat-playlist", "-J", source, timeout=300)
        try:
            pl = json.loads(d.stdout)
        except ValueError:
            die(f"not a playlist: {source}: {d.stderr.strip()[-200:]}")
        meta.setdefault("album", re.sub(r"^Album - ", "", pl.get("title") or "") or None)
        for i, e in enumerate(pl.get("entries") or [], 1):
            url = e.get("url") or f"https://www.youtube.com/watch?v={e['id']}"
            base = os.path.join(album_dir, f"{i:02d} {slug(e.get('title') or e['id'])}")
            r = ytdlp("-f", "bestaudio", "-o", base + ".%(ext)s", "--no-playlist", url)
            got = [f for f in os.listdir(album_dir) if f.startswith(os.path.basename(base) + ".")]
            if r.returncode or not got:
                die(f"download {url}: {r.stderr.strip()[-200:]}")
            t = tags(os.path.join(album_dir, got[0]))
            t.setdefault("title", e.get("title"))
            t.setdefault("artist", e.get("channel") or e.get("uploader"))
            t["track"] = t.get("track") or i
            t["source"] = url
            out.append((os.path.join(album_dir, got[0]), t))
        return out
    if REMOTE.match(source):
        host, path = source.split(":", 1)
        r = subprocess.run(["ssh", "-o", "BatchMode=yes", host, "find", path, "-maxdepth", "2", "-type", "f"],
                           capture_output=True, text=True)
        if r.returncode:
            die(f"ssh {host}: {r.stderr.strip()[:200]}")
        files = [f"{host}:{f}" for f in r.stdout.splitlines() if f.lower().endswith(AUDIO)]
    else:
        files = [os.path.join(dp, f) for dp, _, fs in os.walk(source) for f in fs if f.lower().endswith(AUDIO)]
    for f in sorted(files):
        local = copy_in(f, album_dir)
        t = tags(local)
        t["source"] = f
        out.append((local, t))
    out.sort(key=lambda x: (x[1].get("track") or 999, x[0]))
    for i, (_, t) in enumerate(out, 1):
        t["track"] = t.get("track") or i
    return out


def new_climb(cid, ref, url, a, meta=None):
    return {
        "id": cid,
        "song": f"songs/{cid}.yaml",
        "reference": ref,
        "source": url,
        "owner": None,
        "metric": f"python3 tools/likeness.py sections ref/{cid}.wav OUT.wav $(cat tools/{cid}-sections.txt)",
        "best": None,
        "passes": 1,
        "enabled": False,
        "status": "requested",
        "rounds": 0,
        "priority": float(opt(a, "--priority", 1)),
        "genre": opt(a, "--genre"),
        **({"meta": meta} if meta else {}),
        "requested": {"by": opt(a, "--by") or os.environ.get("CLIMB_AS") or os.environ.get("USER", "?"),
                      "at": now_iso(), "note": opt(a, "--note")},
    }


def cmd_add_album(a):
    pos = positional(a, ("--album", "--artist", "--year", "--genre", "--note", "--priority", "--by"))
    if not pos:
        die("add-album SOURCE (a folder, HOST:/PATH or a playlist URL) [--album A --artist A --year Y] [--genre G]")
    meta = {k: v for k, v in {"album": opt(a, "--album"), "artist": opt(a, "--artist"),
                              "year": int(opt(a, "--year")) if opt(a, "--year") else None}.items() if v}
    staging = os.path.join(ROOT, "ref", "albums", ".incoming-" + str(os.getpid()))
    files = album_files(pos[0], staging, meta)
    if not files:
        die(f"no audio files in {pos[0]}")
    album = meta.get("album") or files[0][1].get("album") or "album"
    album_dir = os.path.join(ROOT, "ref", "albums", slug(album))
    os.makedirs(album_dir, exist_ok=True)
    added = []
    with registry() as reg:
        have = {c["id"] for c in reg["climbs"]}
        for path, t in files:
            m = {"artist": meta.get("artist") or t.get("artist"), "album": album, "title": t.get("title"),
                 "track": t.get("track"), "year": meta.get("year") or t.get("year")}
            m = {k: v for k, v in m.items() if v}
            cid = slug(m["title"])
            if cid in have:
                cid = slug(f"{album} {m['title']}")
            if cid in have:
                print(f"climb: `{cid}` is already a climb — skipped", file=sys.stderr)
                continue
            kept = os.path.join(album_dir, os.path.basename(path))
            os.replace(path, kept)
            to_wav(kept, cid)
            c = new_climb(cid, f"{m.get('artist', '')} — {m['title']}".strip(" —"), t.get("source"), a, m)
            c["ref_file"] = os.path.relpath(kept, ROOT)
            reg["climbs"].append(c)
            have.add(cid)
            added.append(cid)
    shutil.rmtree(staging, ignore_errors=True)
    for cid in added:
        print(f"requested {cid}")
    if added:
        commit_or_die(["climbs.json"], f"climbs: request the album {album} ({len(added)} tracks)", a)


def cmd_refs(a):
    pos = positional(a, ())
    if len(pos) < 2:
        die("refs ALBUM SOURCE — replace the album's references, matched by track number")
    album, source = pos[0], pos[1]
    reg = load()
    mine = {c["meta"]["track"]: c for c in reg["climbs"]
            if (c.get("meta") or {}).get("album", "").lower() == album.lower() and c["meta"].get("track")}
    if not mine:
        die(f"no climbs on the album `{album}`")
    album_dir = os.path.join(ROOT, "ref", "albums", slug(album))
    files = album_files(source, album_dir, {"album": album})
    done = []
    for path, t in files:
        c = mine.get(t.get("track"))
        if not c:
            print(f"climb: track {t.get('track')} ({os.path.basename(path)}) is not a climb — skipped", file=sys.stderr)
            continue
        to_wav(path, c["id"])
        done.append((c["id"], os.path.relpath(path, ROOT), t.get("source")))
    with registry() as reg:
        for cid, rel, src in done:
            c = find(reg, cid)
            c["ref_file"], c["source"] = rel, src
            h = {"round": c["rounds"], "at": now_iso(), "who": whoami(a), "steer": True,
                 "note": f"reference replaced from {source}: re-measure the best version before comparing rounds"}
            with open(os.path.join(HIST, f"{cid}.jsonl"), "a") as f:
                f.write(json.dumps(h, ensure_ascii=False) + "\n")
    print(f"{len(done)} references replaced: {', '.join(c for c, _, _ in done)}")
    if done:
        commit_or_die(["climbs.json", *[f"climbs/{c}.jsonl" for c, _, _ in done]],
                      f"climbs: {album} references from {source}", a)


def itunes_art(artist, album, year=None):
    """The album's cover URL (600 px) from the iTunes search (the edition from `year` first)."""
    import urllib.parse
    import urllib.request
    q = urllib.parse.urlencode({"term": f"{artist} {album}".strip(), "entity": "album", "limit": 10})
    with urllib.request.urlopen(f"https://itunes.apple.com/search?{q}", timeout=30) as r:
        res = json.load(r).get("results", [])
    norm = lambda x: re.sub(r"[^a-z0-9]", "", (x or "").lower())
    want = norm(album)
    hits = [x for x in res if norm(x.get("collectionName")).startswith(want) or want.startswith(norm(x.get("collectionName")))]
    if not hits:
        die(f"no cover for {artist} — {album} in the iTunes search (give --url or --file)")
    hits.sort(key=lambda x: (str(year or "") != str(x.get("releaseDate", ""))[:4], len(x.get("collectionName", ""))))
    return hits[0]["artworkUrl100"].replace("100x100bb", "600x600bb")


def pixel_art(path, px, colors):
    """(palette as #rrggbb, pixel indices) of an image scaled to px×px with at most `colors`."""
    vf = (f"scale={px}:{px}:flags=area,split[a][b];[a]palettegen=max_colors={colors}:stats_mode=full[p];"
          f"[b][p]paletteuse=dither=none")
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-filter_complex", vf, "-frames:v", "1",
                        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    if r.returncode or len(r.stdout) != px * px * 3:
        die(f"ffmpeg {path}: {r.stderr.decode(errors='replace').strip()[:200]}")
    rgb = [r.stdout[i:i + 3] for i in range(0, len(r.stdout), 3)]
    pal = sorted(set(rgb), key=lambda c: 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2])
    index = {c: i for i, c in enumerate(pal)}
    width = 1 if len(pal) <= 16 else 2
    pixels = "".join(format(index[c], "x").rjust(width, "0") for c in rgb)
    return ["#" + c.hex() for c in pal], pixels


def cmd_art(a):
    pos = positional(a, ("--url", "--file", "--px", "--colors", "--artist"))
    if not pos:
        die("art ALBUM [--url URL | --file F] [--px 32] [--colors 16]")
    album = pos[0]
    reg = load()
    mine = [c for c in reg["climbs"] if ((c.get("meta") or {}).get("album") or "").lower() == album.lower()]
    meta = (mine[0].get("meta") or {}) if mine else {}
    album = meta.get("album") or album
    artist = opt(a, "--artist") or meta.get("artist") or ""
    keep = os.path.join(ROOT, "ref", "albums", slug(album))
    os.makedirs(keep, exist_ok=True)
    if opt(a, "--file"):
        cover = copy_in(opt(a, "--file"), keep)
    else:
        import urllib.request
        url = opt(a, "--url") or itunes_art(artist, album, meta.get("year"))
        cover = os.path.join(keep, "cover" + os.path.splitext(url.split("?")[0])[1] or ".jpg")
        with urllib.request.urlopen(url, timeout=60) as r, open(cover, "wb") as f:
            f.write(r.read())
    px, colors = int(opt(a, "--px", 32)), int(opt(a, "--colors", 16))
    palette, pixels = pixel_art(cover, px, colors)
    out = os.path.join("art", f"{slug(album)}.json")
    os.makedirs(os.path.join(ROOT, "art"), exist_ok=True)
    with open(os.path.join(ROOT, out), "w") as f:
        json.dump({"album": album, "artist": artist, "year": meta.get("year"), "w": px, "h": px,
                   "palette": palette, "pixels": pixels}, f)
        f.write("\n")
    print(f"{out}: {px}×{px}, {len(palette)} colours (from {os.path.relpath(cover, ROOT)})")
    commit_or_die([out], f"art: {album} ({px}×{px}, {len(palette)} colours)", a)


def cmd_add(a):
    titles = positional(a, ("--url", "--genre", "--note", "--priority", "--by", "--ref", "--album", "--track",
                            "--artist", "--year"))
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
            meta = {"artist": opt(a, "--artist") or artist or None, "title": title,
                    "album": opt(a, "--album"), "track": int(opt(a, "--track")) if opt(a, "--track") else None,
                    "year": int(opt(a, "--year")) if opt(a, "--year") else None}
            ref_file = None
            if opt(a, "--ref"):
                # our own copy of the reference: tags fill what the flags leave out
                kept = copy_in(opt(a, "--ref"), os.path.join(ROOT, "ref", "albums", slug(meta["album"] or "singles")))
                for k, v in tags(kept).items():
                    if not meta.get(k) or (k == "title" and not title):
                        meta[k] = v
                to_wav(kept, cid)
                ref_file = os.path.relpath(kept, ROOT)
            meta = {k: v for k, v in meta.items() if v}
            c = new_climb(cid, f"{artist} — {title}" if artist else title, url_ or opt(a, "--ref"), a,
                          meta if (meta.keys() - {"title", "artist"}) or ref_file else None)
            if "--oob" in a:
                c["oob"] = True
            if ref_file:
                c["ref_file"] = ref_file
            reg["climbs"].append(c)
            have.add(cid)
            added.append(cid)
    for cid in added:
        print(f"requested {cid}")
    if added:
        commit_or_die(["climbs.json"], f"climbs: request {', '.join(added)}", a)


NOTE_CHARS = 500   # `next` shows a handoff, not a receipt; `climb.py log` has every word


def visible(hist):
    """The history `next` shows: everything from the last fresh-start note on (`note --fresh`), else all of it."""
    i = max((k for k, h in enumerate(hist) if h.get("fresh")), default=0)
    return hist[i:]


def compose_brief(c):
    """A composition climb's brief (compose/README.md): its slot, the album, its neighbours and the latest ratings."""
    out = []
    try:
        with open(os.path.join(ROOT, "compose", c["album"], "album.json")) as f:
            album = json.load(f)
    except (OSError, ValueError, KeyError):
        return [f"  COMPOSITION (album spec compose/{c.get('album')}/album.json missing)"]
    slot = next((t for t in album.get("tracks", []) if t.get("id") == c["id"]), {})
    n, total = slot.get("n"), len(album.get("tracks", []))
    lo, hi = slot.get("length", ["?", "?"])
    out.append(f"  COMPOSITION — an ORIGINAL song for '{album['album']}' by {album['artist']} ({album.get('genre', '')}), "
               f"track {n}/{total}: {slot.get('role', 'song')}, {lo}-{hi} s. Read compose/README.md and the skill's "
               f"§Composition mode; the album brief and palette are in compose/{album['id']}/album.json, its motif bank "
               f"in compose/{album['id']}/motifs.md. Never copy or closely imitate an existing song.")
    if slot.get("brief"):
        out.append(f"  slot: {slot['brief']}")
    if album.get("brief"):
        out.append(f"  album: {album['brief']}")
    reg = load()
    nbs = []
    for nb in (n - 1 if n else None, n + 1 if n else None):
        t = next((t for t in album.get("tracks", []) if t.get("n") == nb), None)
        if t:
            o = next((x for x in reg["climbs"] if x["id"] == t["id"]), {})
            done = os.path.exists(os.path.join(ROOT, o.get("song", "") or "-"))
            nbs.append(f"{t['n']} {t['id']} '{(o.get('meta') or {}).get('title', '?')}' "
                       f"({'composed' if done else 'empty'}{', ' + o['owner'] if o.get('owner') else ''})")
    if nbs:
        out.append(f"  neighbours: {'; '.join(nbs)}" + (" — the songs bleed into one another: shape your first and last "
                                                       "seconds to meet theirs (compscore's flow term)" if album.get("bleed") else ""))
    if not album.get("named"):
        out.append(f"  the album has no name yet: the first agent to get here names it — "
                   f"`tools/chirpers.py name {album['id']} \"…\"` (then `chirpers.py art {album['id']}`)")
    if c["status"] == "requested":
        out.append(f"  FIRST ROUND — compose it from scratch: write songs/{c['id']}.yaml with the library's patches, fx and "
                   f"mix tools (tempo, form, motifs, parts, arrangement, master with a ceiling), title it "
                   f"(`tools/chirpers.py title {c['id']} \"…\"`), add its motifs to the album's bank, render it, score it "
                   f"(`python3 tools/compscore.py {c['id']} OUT.wav --text`), LISTEN, then `climb.py done {c['id']} --version v1 "
                   f"--score S --note … --next … --with songs/{c['id']}.yaml compose/{album['id']}/motifs.md` (it joins "
                   f"the playlist); save its features with compscore --save on the kept render.")
    else:
        out.append(f"  this round: listen to it in the album's order, read the ratings and notes below and compscore's "
                   f"weakest terms (--text), then make the one musical change you believe improves it most (a section, "
                   f"a motif's development, an arrangement, a sound, the mix, a transition); keep it if it wins on paired "
                   f"seeds and stays itself (variety over convergence); `climb.py done {c['id']} …` and compscore --save.")
    rp = os.path.join(ROOT, "compose", album["id"], "ratings.jsonl")
    if os.path.exists(rp):
        with open(rp) as f:
            rs = [json.loads(ln) for ln in f if ln.strip()]
        mine = [r for r in rs if r.get("id") == c["id"]][-4:]
        for r in mine:
            out.append(f"  RATING {r['at'][:16]} {r.get('who')} {r.get('score', '')}{'/10' if 'score' in r else 'note'}"
                       f" ({r.get('version') or '-'}){': ' + r['note'] if r.get('note') else ''}")
    return out


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
    meta = c.get("meta") or {}
    if c.get("mode") == "compose":
        lines += compose_brief(c)
    elif meta.get("album"):
        lines.append(f"  album {meta['album']} track {meta.get('track', '?')} ({meta.get('artist', '')}, {meta.get('year', '')}) — "
                     f"the registry holds its meta (the playlist shows it); songs/{c['id']}.yaml carries `meta:` "
                     f"once the groove's pinned binary supports it (main 8c95a3d+; until then put it in `about:`); the album "
                     f"plays end to end, so match the record's level at the song's first and last seconds: "
                     f"`tools/albumedges.py check {c['id']} RENDER.wav` shows your edges against the record and "
                     f"both transitions; pass `--render RENDER.wav` to done so a kept version's edges are recorded")
    if c.get("mode") == "compose":
        pass
    elif c["status"] == "requested" and c.get("ref_file"):
        lines.append(f"  the reference is ready: ref/{c['id']}.wav (from {c['ref_file']}, one master for the album — "
                     f"do not replace it with a download)")
    if c.get("mode") == "compose":
        pass
    elif c["status"] == "requested":
        lines.append(
            f"  FIRST ROUND — set it up ({SKILL}, §Setup): find the official upload (record it: "
            f"`climb.py set {c['id']} source=URL genre=…`), reference audio to ref/{c['id']}.wav, stems, a tab if "
            f"there is one, tools/{c['id']}-sections.txt, a first songs/{c['id']}.yaml that plans with the groove's "
            f"binary; measure it, then `climb.py done {c['id']} --version v1 --score S --note … --next … "
            f"--with songs/{c['id']}.yaml tools/{c['id']}-sections.txt` (it joins the playlist).")
    else:
        lines.append(f"  this round: listen and measure, then make the BOLD change you believe will move it most — rebuild an "
                     f"instrument (sound design: layers, FM, filters, envelopes, LFO/automation), rewrite note patterns or "
                     f"sections, or rewrite the whole song; a candidate every round, aiming for a big gain ({SKILL}, "
                     f"§Climbing charter). Keep it if it wins on full-length scores and held seeds; then `climb.py done "
                     f"{c['id']} --note … --next … [--score S --version vN --with {c.get('song')}]`.")
    view = visible(hist)
    for h in view[-3:]:
        sc = f" {h['score']}" if h.get("score") is not None else ""
        tag = ("FRESH START" if h.get("fresh") else "NOTE") if h.get("steer") else f"r{h['round']}"
        note = h["note"] if len(h["note"]) <= NOTE_CHARS else h["note"][:NOTE_CHARS] + f" … (climb.py log {c['id']})"
        lines.append(f"  {tag} {age(h['at'])} ago by {h['who']}{sc}{' kept' if h.get('kept') else ''}: {note}")
    nxt = next((h["next"] for h in reversed(view) if h.get("next")), None)
    if nxt and len(nxt) > NOTE_CHARS:
        nxt = nxt[:NOTE_CHARS] + " …"
    if nxt:
        lines.append(f"  suggested next: {nxt}")
    return "\n".join(lines)


NUMWORDS = "zero one two three four five six seven eight nine".split()


def agent_names(s):
    """The names an owner or agent string stands for: 'chirper-one (chirp-climb1)' -> {chirper-one, chirp-climb1};
    a worktree chirp-climbN and the agent chirper-<N in words> are the same climber."""
    out = set()
    for tok in re.findall(r"[a-z0-9][a-z0-9_.@-]*", (s or "").lower()):
        out.add(tok)
        m = re.fullmatch(r"chirp-climb(\d)", tok)
        if m:
            out.add(f"chirper-{NUMWORDS[int(m.group(1))]}")
        m = re.fullmatch(r"chirper-([a-z]+)", tok)
        if m and m.group(1) in NUMWORDS:
            out.add(f"chirp-climb{NUMWORDS.index(m.group(1))}")
    return out


def owned_by_other(c, me):
    o = c.get("owner")
    return bool(o) and not (agent_names(o) & agent_names(me))


def untracked_setup(cid):
    """[(path, HH:MM)] of a climb's setup files that exist but are not in git: someone mid-setup without claiming it
    (chirper-one drew `one` on 25 Oct while chirper-zero's untracked map, sections and stems sat in the tree)."""
    out = []
    for rel in (f"tools/maps/{cid}.json", f"tools/{cid}-sections.txt", f"songs/{cid}.yaml"):
        full = os.path.join(ROOT, rel)
        if not os.path.exists(full):
            continue
        r = subprocess.run(["git", "-C", ROOT, "ls-files", "--error-unmatch", rel], capture_output=True)
        if r.returncode:
            out.append((rel, time.strftime("%H:%M", time.localtime(os.path.getmtime(full)))))
    return out


def cmd_next(a):
    me = whoami(a)
    reg = load()
    w = weights(reg, me)
    skipped = []
    take = opt(a, "--take")
    if take:
        c = find(reg, take)
        if owned_by_other(c, me) and "--force" not in a:
            die(f"`{take}` is owned by {c['owner']}: coordinate first (or --force to take it anyway)", 3)
        cid = take
    else:
        if not w:
            die("nothing queued (every climb is paused, dropped or done)", 1)
        if "--include-owned" not in a:
            # (chirper-zero/chirper-one, 23 Oct: draws of another agent's climb recorded a start that later forced
            # `done --force` on the owner)
            skipped = sorted(i for i in w if owned_by_other(find(reg, i), me))
            w = {i: v for i, v in w.items() if i not in skipped}
            if not w:
                die(f"every queued climb is owned by another agent ({', '.join(skipped)}): `next --take ID` after "
                    f"coordinating, or --include-owned", 1)
        rng = random.Random(int(opt(a, "--seed"))) if opt(a, "--seed") else random.Random()
        ids = list(w)
        cid = rng.choices(ids, weights=[w[i] for i in ids])[0]
    c = find(reg, cid)
    total = sum(w.values())
    odds = w[cid] / total if cid in w and total else None
    if "--peek" not in a:
        os.makedirs(os.path.dirname(STARTS), exist_ok=True)
        with locked("climb-starts.lock"), open(STARTS, "a") as f:
            f.write(json.dumps({"id": cid, "who": me, "t": time.time(), "at": now_iso(), "genre": c.get("genre")}) + "\n")
    pending = untracked_setup(cid) if c.get("status") == "requested" and not c.get("owner") else []
    if "--json" in a:
        out = {"climb": c, "history": visible(history(cid))[-5:],
               "odds": round(odds, 3) if odds is not None else None, "skipped_owned": skipped}
        if pending:
            out["untracked_setup"] = [p for p, _ in pending]
        print(json.dumps(out))
    else:
        how = f"odds {odds:.0%}" if odds is not None else "taken by id"
        skip = f"; skipped {len(skipped)} owned by others" if skipped else ""
        print(f"next for {me} ({how}{skip}):\n{brief(c, history(cid))}")
    if pending:
        print(f"climb: `{cid}` looks mid-setup by someone (untracked: "
              f"{', '.join(f'{p} {t}' for p, t in pending)}): ask before building it", file=sys.stderr)


def cmd_done(a):
    pos = positional(a, ("--note", "--score", "--version", "--next", "--engine", "--as", "--with", "--render"))
    if not pos:
        die("done ID --note TEXT [--score S --version vN] [--next TEXT] [--with FILE …]")
    cid, note = pos[0], opt(a, "--note")
    if not note:
        die("done needs --note (what you tried and what happened — the next agent reads it)")
    me = whoami(a)
    score = float(opt(a, "--score")) if opt(a, "--score") else None
    version = opt(a, "--version")
    # Files others may have written: another agent on this climb since (or shortly before) you started it.
    withs = multi(a, "--with")
    if withs and "--force" not in a:
        st = starts()
        mine = [s["t"] for s in st if s["id"] == cid and s.get("who") == me]
        since = (mine[-1] if mine else time.time()) - SPREAD
        others = [s for s in st if s["id"] == cid and s.get("who") != me and s.get("t", 0) >= since]
        if others:
            first = min(s["t"] for s in others)
            touched = [p for p in withs if os.path.exists(os.path.join(ROOT, p)) and os.path.getmtime(os.path.join(ROOT, p)) > first]
            if touched:
                die(f"{', '.join(sorted({s['who'] for s in others}))} also started {cid} while you were on it, and "
                    f"{', '.join(touched)} changed since: check they hold your version (git diff), coordinate, then "
                    f"re-run with --force (or drop --with and commit yourself)", 3)
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
            c["status"] = "active"
            c["enabled"] = not c.get("oob")  # out-of-band climbs never join the playlist
        c["last"] = {"at": h["at"], "who": me}
        if kept and opt(a, "--render") and (c.get("meta") or {}).get("album") and c.get("mode") != "compose":
            # the album plays gaplessly: compare this version's two joins with the kept version's (a warning, not a
            # gate — chirper-zero found Hedphelym v2 and Ageispolis v2 each lost one)
            try:
                joins, warns = _albumedges().join_regressions(cid, opt(a, "--render"))
                if joins:
                    h["joins"] = {k: {kk: v[kk] for kk in ("with", "score", "was") if kk in v} for k, v in joins.items()}
                for w in warns:
                    print(f"climb: WARNING {w}", file=sys.stderr)
            except (OSError, SystemExit, ValueError, KeyError) as e:
                print(f"climb: joins not checked ({e})", file=sys.stderr)
        os.makedirs(HIST, exist_ok=True)
        with open(os.path.join(HIST, f"{cid}.jsonl"), "a") as f:
            f.write(json.dumps({k: v for k, v in h.items() if v is not None}, ensure_ascii=False) + "\n")
    edges = []
    if kept and opt(a, "--render") and (c.get("meta") or {}).get("album") and c.get("mode") != "compose":
        # An album song's kept render: its edges, for the album's transitions (albumedges.py score).
        ae = _albumedges()
        try:
            edges = [ae.cmd_record([cid, opt(a, "--render")], version=version)]
        except (OSError, SystemExit, ValueError) as e:
            print(f"climb: edges not recorded ({e}); run tools/albumedges.py record {cid} RENDER.wav", file=sys.stderr)
    near = best.get("score")
    if score is not None and not kept and near is not None and abs(score - float(near)) <= 0.05:
        print(f"climb: {score} is within rounding of best {near}: if either was rounded, re-measure both "
              f"unrounded (likeness.py prints 3 decimals) and `climb.py set {cid} best=…` if this one is higher",
              file=sys.stderr)
    # commit FIRST, then print the status line LAST: a failed commit must not end in a success line (agents read
    # `| tail -1`), and it exits non-zero
    commit_or_die(["climbs.json", f"climbs/{cid}.jsonl", *multi(a, "--with"), *edges],
                  f"climbs: {cid} round {h['round']}{f' — {version} {score}' if kept else ''}: {note[:60]}", a)
    print(f"{cid} round {h['round']}{f' — best {score} ({version})' if kept else ''}"
          f"{' — joins the playlist' if c.get('enabled') and h['round'] == 1 else ''}")


def _albumedges():
    import importlib.util
    spec = importlib.util.spec_from_file_location("albumedges", os.path.join(HERE, "albumedges.py"))
    ae = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ae)
    return ae


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
        on = sorted({s["who"] for s in st if s["id"] == c["id"] and t - s.get("t", 0) < ROUND_HOLD})
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
    pos = [p for p in pos if p != "--fresh"]
    if len(pos) < 2:
        die("note ID TEXT [--next TEXT] [--fresh]")
    cid, text = pos[0], " ".join(pos[1:])
    with registry() as reg:
        c = find(reg, cid)
        h = {"round": c["rounds"], "at": now_iso(), "who": whoami(a), "note": text, "next": opt(a, "--next"), "steer": True,
             "fresh": True if "--fresh" in a else None}
        os.makedirs(HIST, exist_ok=True)
        with open(os.path.join(HIST, f"{cid}.jsonl"), "a") as f:
            f.write(json.dumps({k: v for k, v in h.items() if v is not None}, ensure_ascii=False) + "\n")
    print(f"{cid}: noted")
    commit_or_die(["climbs.json", f"climbs/{cid}.jsonl"], f"climbs: {cid} note: {text[:60]}", a)


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
                val = json.loads(v)
            except ValueError:
                val = v
            if k == "best" and isinstance(val, (int, float)):
                # `set ID best=61.03` (a re-measure, e.g. after a library change) updates only the score: the
                # version/commit/engine record stays, so status/next/done keep working
                val = {**(c.get("best") if isinstance(c.get("best"), dict) else {}), "score": val}
            c[k] = val
    commit_or_die(["climbs.json"], f"climbs: {pos[0]} {' '.join(pos[1:])[:60]}", a)


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
    commit_or_die(["climbs.json"], f"climbs: {pos[0]} {status}", a)


def album_of(c):
    return (c.get("meta") or {}).get("album")


def cmd_focus(a):
    pos = positional(a, ("--ids",))
    off = "--off" in a
    ids = [x.strip() for x in (opt(a, "--ids") or "").split(",") if x.strip()]
    if not pos and not off and not ids:
        die("focus ALBUM | focus --ids ID,ID… | focus --off")
    changed = []
    with registry() as reg:
        if off:
            for c in reg["climbs"]:
                if c.get("paused_by") == "focus":
                    c["status"] = "active" if c["rounds"] else "requested"
                    c.pop("paused_by", None)
                    changed.append(c["id"])
            reg.pop("focus", None)
        elif ids:
            have = {c["id"] for c in reg["climbs"]}
            missing = [x for x in ids if x not in have]
            if missing:
                die(f"no such climb(s): {', '.join(missing)}")
            for c in reg["climbs"]:
                on = c["id"] in ids
                if on and c.get("paused_by") == "focus":
                    c["status"] = "active" if c["rounds"] else "requested"
                    c.pop("paused_by", None)
                    changed.append(c["id"])
                elif not on and c["status"] in QUEUED:
                    c["status"], c["paused_by"] = "paused", "focus"
                    changed.append(c["id"])
            reg["focus"] = "climbs: " + ", ".join(ids)
        else:
            album = pos[0]
            mine = [c for c in reg["climbs"] if (album_of(c) or "").lower() == album.lower()]
            if not mine:
                die(f"no climbs on the album `{album}` (albums: {', '.join(sorted({album_of(c) for c in reg['climbs'] if album_of(c)}))})")
            for c in reg["climbs"]:
                on = (album_of(c) or "").lower() == album.lower()
                if on and c.get("paused_by") == "focus":
                    c["status"] = "active" if c["rounds"] else "requested"
                    c.pop("paused_by", None)
                    changed.append(c["id"])
                elif not on and c["status"] in QUEUED:
                    c["status"], c["paused_by"] = "paused", "focus"
                    changed.append(c["id"])
            reg["focus"] = album_of(mine[0])
    print(f"focus {'off' if off else reg.get('focus')}: {len(changed)} climbs changed")
    if changed:
        commit_or_die(["climbs.json"], f"climbs: focus {'off' if off else (pos[0] if pos else reg.get('focus'))} "
                                       f"({len(changed)} changed)", a)


def cmd_commit(a):
    """climb.py commit -m MSG PATH …: commit exactly those paths and publish them (no stash, honest receipt)."""
    if "-m" not in a or a.index("-m") + 1 >= len(a):
        die("usage: climb.py commit -m MSG PATH …")
    i = a.index("-m")
    msg, paths = a[i + 1], [p for p in a[:i] + a[i + 2:] if p != "--no-git"]
    if not paths:
        die("climb.py commit: name the paths to commit")
    commit_or_die(paths, msg, a)


def cmd_publish(a):
    """climb.py publish: push local commits (after a 'NOT pushed' receipt). Records nothing."""
    with locked("climb-git.lock"):
        ok, why = publish()
    print(f"climb: {why}" if ok else f"climb: NOT pushed: {why}", file=sys.stderr if not ok else sys.stdout)
    sys.exit(0 if ok else 1)


def cmd_tui(a):
    import runpy
    sys.argv = [os.path.join(HERE, "climbtui.py"), *a]
    runpy.run_path(sys.argv[0], run_name="__main__")


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("status", "ls", "list"):
        return cmd_status(a[1:] if a else [])
    cmd, rest = a[0], a[1:]
    table = {"add": cmd_add, "request": cmd_add, "add-album": cmd_add_album, "refs": cmd_refs, "art": cmd_art, "next": cmd_next, "done": cmd_done, "log": cmd_log, "set": cmd_set,
             "note": cmd_note,
             "pause": lambda r: cmd_state(r, "paused"), "resume": lambda r: cmd_state(r, "active"),
             "drop": lambda r: cmd_state(r, "dropped"), "focus": cmd_focus, "tui": cmd_tui,
             "commit": cmd_commit, "publish": cmd_publish}
    if cmd in ("-h", "--help", "help"):
        print(__doc__)
        return
    if cmd not in table:
        die(f"unknown command `{cmd}` — {', '.join(table)} or status")
    if cmd in ("next", "done"):
        janitor()
    table[cmd](rest)


def janitor():
    """Every round sweeps the agents' temp audio (tmpclean.py: at most every 10 minutes, detached)."""
    try:
        subprocess.Popen([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmpclean.py"),
                          "--every", "10", "--quiet"], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL, start_new_session=True)
    except OSError:
        pass


if __name__ == "__main__":
    main()
