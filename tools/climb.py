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
  climb.py next [--as NAME] [--peek] [--take ID] [--again] [--include-owned] [--json] [--seed N] [--type T]
                                                    pick this pass's climb (and say what to do). NO CLIMB HAS AN
                                                    OWNER (Harry, 18 Nov): the draw is among every queued climb,
                                                    whoever worked on it last; starting one takes its LOCK, and
                                                    recording the round (done) releases it for anyone.
                                                    --peek records no start; --take ID starts exactly that one
                                                    (refused while someone else holds its lock, unless --force);
                                                    when every free song is one you had the last word on it says
                                                    NOTHING NEW and starts nothing (--again draws anyway);
                                                    --include-owned is accepted and does nothing now;
                                                    composition albums with params.rounds print a ROUND TYPE
                                                    (whole, section, palette; --type T overrides the draw)
  climb.py type ID [--type T]                       this round's type for one song (compose/README.md, Round
                                                    types)
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
  climb.py pass ID TEXT --anyway [--next TEXT]      DO NOT PASS (Harry, 19 Nov: "can we stop passing on songs"): make
                                                    the round, or an instrument round. Only for a song that cannot be
                                                    touched now: records the note and releases the lock at once
  climb.py pause|resume|drop ID [--note TEXT]       take a climb out of (or back into) the queue
  climb.py tui                                      the queue as a TUI: toggle climbable/playlist, focus, notes
  climb.py focus ALBUM | --ids ID,ID… | --off       climb only that album (or those climbs): pause every other
                                                    queued climb; --off resumes what a focus paused
                                                    (marked, so --off resumes exactly those); the playlist
                                                    is unchanged
  climb.py commit -m MSG PATH … [--library-ok]      commit those paths only and publish (below). Library files
                                                    (patches/ racks/ styles/ irs/) go through libguard.py first:
                                                    refused when a song outside the album in progress would change,
                                                    held until --library-ok when another composer's song would
                                                    (also for `done --with`); a file under a new name is free
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


SHARED_BOARDS = re.compile(r"^compose/[^/]+/(motifs|sounds|features)\.md$")


def shared_board_notes(rel):
    """What to say when a file everyone writes is about to be committed WHOLE with more than one open hunk in it: each
    hunk's first words, so that lines which are not the committer's are seen at once. It stops nothing. (19 Nov: twice
    in five hours a composer's commit took another composer's uncommitted rows of motifs.md with it, because `commit`
    and `done --with` take a file whole; `commit --pick REGEX` takes only your hunks.)"""
    out = []
    for p in rel:
        if not SHARED_BOARDS.match(p.replace(os.sep, "/")):
            continue
        d = subprocess.run(["git", "diff", "-U0", "--no-color", "--no-ext-diff", "--no-textconv", "HEAD", "--", p], cwd=ROOT,
                           capture_output=True).stdout
        _, seen = pick_hunks(b"", d, lambda add, rem: False)
        if len(seen) < 2:
            continue
        out.append(f"climb: NOTE {p} goes in WHOLE, with {len(seen)} open hunks. If one of them is not yours, tell its "
                   "writer now (their `done` will then show no change for it), and next time take only your own: "
                   f"`climb.py commit -m MSG --pick 'REGEX' {p}`.")
        for _, add, rem in seen[:6]:
            first = (add or rem)[0].decode("utf-8", "replace").strip()[:100] if (add or rem) else ""
            out.append(f"climb:   +{len(add)} -{len(rem)}  {first!r}")
    return out


def board_gate(paths, cid, title, track, me, args):
    """`done --with` REFUSES, before anything is recorded, a file everyone writes that holds open hunks naming neither
    the song (its id, its title, its tN) nor the caller: `done` takes a file whole and would commit them under this
    round. (19 Nov: three times in six hours a composer's `done` took another composer's unrecorded rows of motifs.md or
    sounds.md; the third came with a warning printed as it happened, and its author asked for a refusal: "I would have
    been stopped".) --whole takes the file as it stands. Lines that touch your own are one hunk and still go in with
    them: the commit's note says so."""
    if "--whole" in args or "--no-git" in args or not os.path.isdir(os.path.join(ROOT, ".git")):
        return
    words = [re.escape(cid)] + [re.escape(x) for x in sorted(agent_names(me))]
    if title and len(str(title)) >= 4:
        words.append(re.escape(str(title)))
    if track is not None:
        words.append(rf"\bt{track}\b")
    rx = re.compile("|".join(words), re.I)
    held = []
    for p in paths:
        rel = os.path.relpath(os.path.join(ROOT, p) if not os.path.isabs(p) else p, ROOT)
        if not SHARED_BOARDS.match(rel.replace(os.sep, "/")):
            continue
        d = subprocess.run(["git", "diff", "-U0", "--no-color", "--no-ext-diff", "--no-textconv", "HEAD", "--", rel], cwd=ROOT,
                           capture_output=True).stdout
        _, seen = pick_hunks(b"", d, lambda add, rem: any(rx.search(x.decode("utf-8", "replace")) for x in add + rem))
        for k, add, rem in seen:
            if not k:
                first = (add or rem)[0].decode("utf-8", "replace").strip()[:110] if (add or rem) else ""
                held.append((rel, f"+{len(add)} -{len(rem)}  {first!r}"))
    if not held:
        return
    files = sorted({r for r, _ in held})
    for r, line in held[:8]:
        print(f"climb:   {r}: {line}", file=sys.stderr)
    die(f"shared board HELD: {', '.join(files)} hold{'s' if len(files) == 1 else ''} {len(held)} open hunk(s) that name "
        f"neither this song ({cid}{', ' + repr(title) if title else ''}{', t' + str(track) if track is not None else ''}) nor "
        f"you ({me}); `done --with` takes a file whole and would commit them under your round. Nothing was committed or "
        f"recorded. If they are another composer's, leave {' and '.join(files)} out of --with, run done, then commit your "
        f"own lines: `climb.py commit -m MSG --pick 'REGEX' {' '.join(files)}`. If they ARE yours, repeat with --whole.", 5)


def commit(paths, msg, args):
    """True when the change is in a commit (pushed, or local with an honest receipt and `climb.py publish` to retry);
    False when nothing was committed - callers must then fail loudly, or the registry edit can be lost to the next
    agent's sync. Never stashes another agent's uncommitted work (bd-d30a90)."""
    if "--no-git" in args or not os.path.isdir(os.path.join(ROOT, ".git")):
        return True
    rel = [os.path.relpath(os.path.join(ROOT, p) if not os.path.isabs(p) else p, ROOT) for p in paths]
    with locked("climb-git.lock"):
        for line in shared_board_notes(rel):
            print(line, file=sys.stderr)
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


def pick_hunks(head, diff, keep):
    """One file's committed bytes with only some of its uncommitted hunks applied. `diff` is `git diff -U0 HEAD -- FILE`
    (bytes: no context lines, so a hunk is one unbroken run of changed lines); keep(added, removed) says whether a hunk
    goes in. → (the new bytes, [(kept, added lines, removed lines)]). Built from HEAD's own lines, not by `git apply`,
    so leaving a hunk out cannot shift the ones after it."""
    lines = head.splitlines(keepends=True)
    hunks, cur, last = [], None, None
    for ln in diff.splitlines(keepends=True):
        m = re.match(rb"@@ -(\d+)(?:,(\d+))? \+\d+(?:,\d+)? @@", ln)
        if m:
            cur = {"a": int(m.group(1)), "m": 1 if m.group(2) is None else int(m.group(2)), "add": [], "rem": []}
            hunks.append(cur)
            last = None
        elif cur is None:
            continue                                  # the file header
        elif ln[:1] == b"+":
            cur["add"].append(ln[1:])
            last = "add"
        elif ln[:1] == b"-":
            cur["rem"].append(ln[1:])
            last = "rem"
        elif ln[:1] == b"\\" and last == "add":       # "\ No newline at end of file" after an added line
            cur["add"][-1] = cur["add"][-1].rstrip(b"\n")
    out, pos, seen = [], 0, []
    for h in hunks:
        at = h["a"] if h["m"] == 0 else h["a"] - 1    # -a,0 inserts AFTER line a; -a,m replaces m lines from line a
        k = bool(keep(h["add"], h["rem"]))
        out += lines[pos:at] + (h["add"] if k else lines[at:at + h["m"]])
        pos = at + h["m"]
        seen.append((k, h["add"], h["rem"]))
    return b"".join(out + lines[pos:]), seen


def commit_picked(paths, msg, pattern, args):
    """`climb.py commit -m MSG --pick REGEX PATH …`: of each PATH, commit only the hunks whose added or removed lines
    match REGEX, and leave every other uncommitted line where it is, uncommitted. For the files everyone writes
    (motifs.md, sounds.md, features.md): chirper-zero, 19 Nov, found another composer's open lines for a round not yet
    recorded in two of them when he published, and `commit` and `done --with` take a file whole. He did this by hand
    (hash-object, update-index --cacheinfo). The commit is made beside the index, from HEAD's tree and the picked
    blobs: no working file is written and no other index entry is read. True when committed, False when not."""
    if "--no-git" in args or not os.path.isdir(os.path.join(ROOT, ".git")):
        return True
    try:
        rx = re.compile(pattern)
    except re.error as e:
        die(f"climb.py commit --pick: {pattern!r} is not a regular expression ({e})")

    def gitb(*a, env=None, stdin=None):
        return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, input=stdin, env=env)

    def first(ls):
        return ls[0].decode("utf-8", "replace").strip()[:90] if ls else ""

    rel = [os.path.relpath(os.path.join(ROOT, p) if not os.path.isabs(p) else p, ROOT) for p in paths]
    with locked("climb-git.lock"):
        head = git("rev-parse", "HEAD").stdout.strip()
        entries = []
        for p in rel:
            ls = git("ls-tree", head, "--", p).stdout.split()
            if len(ls) < 3 or ls[1] != "blob":
                die(f"climb.py commit --pick: {p} is not a file in the last commit. A new file has nobody else's lines in "
                    "it: commit it whole.")
            diff = gitb("diff", "-U0", "--no-color", "--no-ext-diff", "--no-textconv", "--no-renames", head, "--", p).stdout
            new, seen = pick_hunks(gitb("cat-file", "blob", ls[2]).stdout, diff,
                                   lambda add, rem: any(rx.search(x.decode("utf-8", "replace")) for x in add + rem))
            kept = [h for h in seen if h[0]]
            print(f"climb: {p}: {len(kept)} of {len(seen)} open hunk(s) match {pattern!r}"
                  + ("" if kept else ": nothing of this file is committed"))
            for _, add, rem in kept:
                stray = [x for x in add if not rx.search(x.decode("utf-8", "replace")) and x.strip()]
                if stray:
                    print(f"climb:   NOTE a committed hunk also carries {len(stray)} added line(s) that do not match (lines "
                          f"that touch are one hunk): {first(stray)!r}")
            for k, add, rem in seen:
                if not k:
                    print(f"climb:   left open in the tree: +{len(add)} -{len(rem)}  {first(add or rem)!r}")
            if kept:
                sha = gitb("hash-object", "-w", "--stdin", stdin=new).stdout.decode().strip()
                entries.append((ls[0], sha, p, ls[2]))
        if not entries:
            print("climb: not committed: no open hunk of these files matches", file=sys.stderr)
            return False
        tmp = os.path.join(ROOT, ".git", f"climb-pick-index.{os.getpid()}")
        env = dict(os.environ, GIT_INDEX_FILE=tmp)
        try:
            steps = [gitb("read-tree", head, env=env)]
            steps += [gitb("update-index", "--cacheinfo", f"{mode},{sha},{p}", env=env) for mode, sha, p, _ in entries]
            tree = gitb("write-tree", env=env)
            made = gitb("commit-tree", tree.stdout.decode().strip(), "-p", head, "-m", msg) if not tree.returncode else tree
            bad = next((x for x in steps + [tree, made] if x.returncode), None)
            if bad is not None:
                print(f"climb: not committed: {bad.stderr.decode('utf-8', 'replace').strip()[:200]}", file=sys.stderr)
                return False
        finally:
            if os.path.exists(tmp):
                os.remove(tmp)
        new_head = made.stdout.decode().strip()
        u = git("update-ref", "-m", "climb commit --pick", "HEAD", new_head, head)
        if u.returncode:
            print(f"climb: not committed: {u.stderr.strip()[:200]}", file=sys.stderr)
            return False
        for mode, sha, p, was in entries:     # the index follows HEAD where it stood at HEAD; a staged edit is left alone
            cur = git("ls-files", "-s", "--", p).stdout.split()
            if len(cur) >= 2 and cur[1] == was:
                git("update-index", "--cacheinfo", f"{mode},{sha},{p}")
        ok, why = publish()
        if not ok:
            print(f"climb: committed locally as {new_head[:9]} but NOT pushed: {why}. The record is safe in git; retry "
                  "with `python3 tools/climb.py publish` - do not re-run this command", file=sys.stderr)
        return True


def song_differs_from_head(rel):
    """True when the working copy of a song differs from the committed one (or is not committed yet)."""
    r = subprocess.run(["git", "-C", ROOT, "diff", "--quiet", "HEAD", "--", rel], capture_output=True)
    if r.returncode == 0:
        tracked = subprocess.run(["git", "-C", ROOT, "ls-files", "--error-unmatch", rel], capture_output=True)
        return tracked.returncode != 0 and os.path.exists(os.path.join(ROOT, rel))
    return r.returncode == 1


def library_gate(paths, args, me=None, mine=()):
    """A commit that carries library files (patches/, racks/, styles/, irs/) must not change songs it should not
    (libguard.py, 10 Nov: the user library is live, so an edit to a shared patch changes every song that uses it at
    once). Refused when a song outside the album in progress would change (a released album must keep rendering as it
    was released); held, until --library-ok, when another composer's song of the album would. A new name is free."""
    import libguard
    lib = [p for p in paths if libguard.is_library(p, ROOT)]
    if not lib or "--no-git" in args or libguard.git(ROOT, "rev-parse", "HEAD") is None:
        return
    res = libguard.check(lib, root=ROOT, me=me, mine=mine)
    if not res["paths"]:
        return
    code, lines = libguard.verdict(res)
    print("\n".join(lines), file=sys.stderr)
    if code == 1:
        die("library change REFUSED: it changes songs outside the album in progress. Nothing was committed or recorded. "
            "Save the file under a new name, or keep the change in your song (extends + overrides).", 5)
    if code == 2 and "--library-ok" not in args:
        die("library change HELD: it changes other composers' songs of the album. Nothing was committed or recorded. "
            "Tell their owners, then repeat with --library-ok (or use a new name; with --as/CLIMB_AS your own songs pass).", 5)


def picture_notice(paths, args):
    """Say at once when a song being committed breaks what its picture reads (10 Nov: the pictures are built on the
    songs' bars, tracks and lanes - vis/<id>.yaml). `chirp vis check -f SONG` on the version being committed against
    the committed one; engine warnings that are new are printed for the composer, who can fix it most cheaply (keep
    the name, or tell chirp-video). Never blocks and never fails a commit."""
    try:
        if "--no-git" in args:
            return
        import chirpbin
        import visdrift
        pin = None
        for p in paths:
            rel = os.path.relpath(os.path.join(ROOT, p) if not os.path.isabs(p) else p, ROOT)
            cid = os.path.splitext(os.path.basename(rel))[0]
            prog = visdrift.programme(cid) if rel.startswith("songs" + os.sep) else None
            full = os.path.join(ROOT, rel)
            if not prog or not os.path.isfile(full):
                continue
            pin = pin or chirpbin.resolve("chirp")
            scenes, warns = visdrift.placed(pin, prog, full)
            head = git("show", f"HEAD:{rel}")
            old = []
            if head.returncode == 0:
                tmp = os.path.join(ROOT, "songs", f".picture-{os.getpid()}-{cid}.yaml")
                try:
                    with open(tmp, "w") as f:
                        f.write(head.stdout)
                    old_scenes, old = visdrift.placed(pin, prog, tmp)
                    old = old if old_scenes is not None else None        # the programme did not check before either
                finally:
                    os.path.exists(tmp) and os.unlink(tmp)
            if old is None:
                continue
            fresh = [w for w in warns if w not in old] if scenes is not None else [f"it no longer checks: {'; '.join(warns)[:200]}"]
            if fresh:
                print(f"climb: NOTE for the picture ({os.path.relpath(prog, ROOT)}), not blocking - this version changes what "
                      "it reads:\n" + "\n".join(f"  - {w}" for w in fresh[:8])
                      + "\n  the picture is built on this song's bars, track and lane names: keep them, or tell chirp-video "
                      "what moved", file=sys.stderr)
    except Exception as e:                                               # a notice must never cost a commit
        print(f"climb: (picture check skipped: {e})", file=sys.stderr)


def commit_or_die(paths, msg, args):
    if not commit(paths, msg, args):
        die("NOT recorded in git (see 'not committed' above): the registry edit is only in the working tree "
            "and the next sync can drop it - fix the git state and re-run (with --force for done)", 4)


# ── sampling ───────────────────────────────────────────────────────────────────────────────

def released(c, s):
    """Has the agent of start S let this climb go since: a round recorded on it, or a pass (`climb.py pass`)?
    ANY round of theirs since the start, not only the climb's last one (chirper-two, 19 Nov: chirper-one started
    Extreme and Mean at 02:17 and recorded v18 at 02:27; chirper-two recorded v19 at 02:58; the last round was then
    chirper-two's, so chirper-one's start read as a lock again until it aged out at 03:47, and the song was out of
    everyone's draw with nobody on it). A note finishes nothing: only recorded rounds are read from the history."""
    who = agent_names(s.get("who"))
    rounds = [r for r in history(c["id"]) if not r.get("steer")] if c.get("id") else []
    for r in [c.get("last") or {}] + list(c.get("passed_by") or []) + rounds:
        if not (agent_names(r.get("who")) & who):
            continue
        try:
            if calendar.timegm(time.strptime(r.get("at", ""), "%Y-%m-%dT%H:%M:%SZ")) >= s.get("t", 0) - 1:
                return True
        except ValueError:
            pass
    return False


_HEARD = {}


def epoch(iso):
    try:
        return calendar.timegm(time.strptime(str(iso)[:19], "%Y-%m-%dT%H:%M:%S"))
    except ValueError:
        return 0


def heard_at(c):
    """When Harry last answered a card or left a note on this track on the review page (epoch; 0 when never, or when
    the page cannot be read). His word reopens a song to whoever had the last word on it."""
    album, n = c.get("album"), (c.get("meta") or {}).get("track")
    if not album or n is None or (os.environ.get("CLIMB_ROOT") and not os.environ.get("CHIRP_LISTEN_DIR")):
        return 0             # a test's registry: never read the real page
    if album not in _HEARD:
        try:
            import listen
            _HEARD[album] = (listen.notes(album), listen.questions(album))
        except Exception:  # noqa: BLE001  (a draw must not fail on the page's files)
            _HEARD[album] = ([], [])
    notes, qs = _HEARD[album]
    return max([epoch(a.get("at")) for q in qs if q.get("n") == n for a in q["answers"].values()]
               + [epoch(x.get("at")) for x in notes if x.get("n") == n] + [0])


def said_last(c, me):
    """In a composition, is the song's last word yours: you recorded its last round, or passed on it since, and Harry
    has said nothing of the track since then? Then it is for someone else (Harry, 18 Nov: "a new round should release
    for anyuone to improve"; "tha tis hos we maintain variaety"): `weights` leaves it out of YOUR draw while any other
    free song is queued. chirper-two, 18 Nov: drawn Common Measure five times in a day, three rounds running, then
    again twelve minutes after his own v19. Harry's answer or note on the track reopens it to you."""
    if c.get("mode") != "compose":
        return False
    mine = agent_names(me)
    words = [r for r in [c.get("last") or {}] + list(c.get("passed_by") or []) if agent_names(r.get("who")) & mine]
    return bool(words) and max(epoch(r.get("at")) for r in words) >= heard_at(c)


def weights(reg, me, stale=None):
    """Draw weights. (`stale`, a list, is filled with the free climbs when every one of them is a song you had the last
    word on: nothing new for you.) A climb another agent started under ROUND_HOLD ago and has not recorded a round on since is HELD:
    it is skipped while anything unheld is queued (two agents on one climb duplicate the round - chirper-two drew
    entrapment and imprint while chirper-three held them); when every candidate is held, held ones are drawn at
    half weight as before."""
    t = time.time()
    st = starts()
    mine = [s for s in st if s.get("who") == me]
    last = mine[-1] if mine else None
    out, held, said = {}, set(), set()
    for c in reg["climbs"]:
        if c["status"] not in QUEUED or c.get("oob"):
            continue
        if c["rounds"] == 0 and any(s["id"] == c["id"] and s.get("who") != me and t - s.get("t", 0) < SETUP_HOLD
                                    for s in st):
            continue  # someone is setting it up
        w = float(c.get("priority", 1)) / (1 + c["rounds"])
        others = [s for s in st if s["id"] == c["id"] and s.get("who") != me and t - s.get("t", 0) < ROUND_HOLD]
        if any(not released(c, s) for s in others):
            held.add(c["id"])
        if said_last(c, me):
            said.add(c["id"])
        if others:
            w *= 0.5
        if last and last["id"] == c["id"]:
            w *= 0.3
        elif last and c.get("genre") and c.get("genre") == last.get("genre"):
            w *= 0.6
        out[c["id"]] = w
    free = {k: v for k, v in out.items() if k not in held}
    fresh = {k: v for k, v in free.items() if k not in said}     # not the song whose last word is yours (said_last)
    if stale is not None and free and not fresh:
        stale.extend(sorted(free))                                # every free song is one you had the last word on
    return fresh or free or out


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
    elif not (os.path.exists(dest) and os.path.samefile(src, dest)):  # chirpers.py art writes into DEST_DIR itself
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


ROUND_TYPES = {
    "whole": "  ROUND TYPE: whole song - the bold change you believe moves the whole song most (as always).",
    "section": ("  ROUND TYPE: section - work ONE ~30 s window in its context (Harry, 2 Nov: the small changes that make a song "
                "feel handcrafted and unique), and make it a real change, not a nudge: rewrite that window's part, add a "
                "counter-line, a new sound, a break, a fill, a key or texture move. "
                "`chirpers.py sections {id} --wav YOUR_BEST_RENDER` maps the song and names "
                "the windows to focus on (flagged, least recently focused) with the commands that render them; make that "
                "window stand out or blend, with detail no other window has, and keep the variety moving. "
                "`--against OLD_RENDER` shows whether the change stayed local; the full-length score must not regress beyond "
                "noise (or keep it on judgment). Then `chirpers.py sections {id} --mark N --note '...'` and name the window "
                "in your round note."),
    "palette": ("  ROUND TYPE: palette - `chirpers.py palette {id}`: the song's instruments against the album's staples, "
                "the library's unused patches and the engine features the album has not used. Change one or two "
                "instruments (swap a staple for something no other track has, design a new patch, add the part the song "
                "lacks), measured on full-length renders; name the swap in your round note."),
    "instrument": ("  ROUND TYPE: instrument - Harry, 19 Nov: \"we have so much we could do re: improving our instruments, "
                   "better guitars, etc and just general improvements\". Make ONE of this song's instruments SOUND better: a "
                   "guitar rig, the bass, the kit, a lead (its attack, body and bite; the amp, cab, pick and string; how it "
                   "sits). Hear the part alone and in the mix, before and after, against the album's records "
                   "(`tools/keybench.py`, `tools/stembal.py`, `tools/presence.py`, `tools/swapbench.py`), on full-length "
                   "renders at both seeds. KEEP A TONE CHANGE ON THE MIX'S READ, not the part's alone (`stembal.py song … "
                   "--voice`): the records' stems do not sum to their mixes, so a rig fitted to a record's lone guitar can "
                   "be right alone and wrong in the mix (chirper-zero, Common Time round 63: a 760 Hz cut fitted the rig "
                   "alone and left the mix 2.2 dB under). CHECK A BENCH MATCH ON A MASTERED "
                   "RENDER: a bowed or sawtooth-like part is a spike every period, and one whose highest raw sample passes "
                   "about -10 dBFS is turned down by the master limiter for as long as it plays (chirper-zero, Still Owing "
                   "v18: a voicing that matched on the raw bench came out 4.5 LU under in the full render), so set such a "
                   "part by its highest raw sample; and a SPARSE passage comes up when mastered (Carrying Capacity v24: its "
                   "holes stood 4 LU higher in the finished file than on the bench). READ THE CHANGED WINDOW BEFORE `done`, not "
                   "after, and a new voice's HARMONICS before its loudness (chirper-zero, On Its Hinge v16 to v17: a bowed "
                   "string whose first harmonic stood 10 to 19 dB over the rest was mostly one low tone, +3.1 dB at "
                   "250-500 Hz, and the read that caught it was stamped after publishing). "
                   "A gain in a LIBRARY patch goes under a NEW name (`tools/libguard.py`: released "
                   "albums are frozen); say in your round note which other songs could take it. Where the engine is what "
                   "falls short, say so in a bead with numbers (chirper-zero builds engine features; chirp-eco gates). The "
                   "notes need not change at all."),
}


def round_type(c, override=None):
    """This round's type for a composition climb whose album sets params.rounds ({whole, section, palette: weight}):
    drawn per song and round number (reproducible), or OVERRIDE (`next --type T`). None when the album sets none.
    A track of the album may carry its own `rounds` (the same form), which then stands for that song: a song whose
    palette is settled can be given {"whole": 0.4, "section": 0.6} by its composer."""
    if override:
        if override not in ROUND_TYPES:
            die(f"--type must be one of {', '.join(ROUND_TYPES)}", 2)
        return override
    if c.get("mode") != "compose":
        return None
    try:
        with open(os.path.join(ROOT, "compose", c["album"], "album.json")) as f:
            album = json.load(f)
        w = ((album.get("params") or {}).get("rounds")) or {}
        own = next((t.get("rounds") for t in album.get("tracks") or [] if isinstance(t, dict) and t.get("id") == c["id"]), None)
        if w and isinstance(own, dict) and own:        # the song's own weights, where its composer has set them
            w = own
    except (OSError, ValueError, KeyError):
        return None
    w = {k: float(v) for k, v in w.items() if k in ROUND_TYPES and float(v) > 0}
    if not w:
        return None
    rng = random.Random(f"{c['id']}:{int(c.get('rounds') or 0) + 1}")
    ks = sorted(w)
    return rng.choices(ks, weights=[w[k] for k in ks])[0]


def cmd_type(a):
    """This round's type for one song: `climb.py type ID [--type T]`."""
    ids = [x for x in a if not x.startswith("--") and x != opt(a, "--type") and x != opt(a, "--as")]
    if not ids:
        die("climb.py type ID [--type T]", 2)
    c = find(load(), ids[0])
    rt = round_type(c, opt(a, "--type"))
    n = int(c.get("rounds") or 0) + 1
    if not rt:
        print(f"{c['id']} round {n}: its album sets no params.rounds, so a whole-song round")
        return
    print(f"{c['id']} round {n}: {rt}\n{ROUND_TYPES[rt].format(id=c['id'])}")


def records_read(cid):
    """When the climb was last read against the album's reference records ({"at", "version", "windows"}: stamped by
    `tools/stembal.py song … --id ID` in ref/stembal/reads.json), or None when no read is on record."""
    try:
        with open(os.path.join(ROOT, "ref", "stembal", "reads.json")) as f:
            return json.load(f).get(cid)
    except (OSError, ValueError, AttributeError):
        return None


def records_line(c, stale=4):
    """The brief's line about reading a composed song against the records: when none is on record, or when the last
    was `stale` or more kept versions ago; None when it is fresh (or the versions are not vN numbers)."""
    def num(v):
        return int(v[1:]) if isinstance(v, str) and v[:1] == "v" and v[1:].isdigit() else None
    rd, now = records_read(c["id"]), num((c.get("best") or {}).get("version"))
    how = f"`tools/stembal.py song FILE --refs … --windows … --voice --id {c['id']}` (--id puts the read on record)"
    if rd is None:
        return (f"  AGAINST THE RECORDS: no read of this song is on record. Read its sections beside the album's reference "
                f"records, and by part (--parts): {how}. Plain Hunt was first read at v8, seven versions in.")
    then = num(rd.get("version"))
    if now is None or then is None or now - then < stale:
        return None
    return (f"  AGAINST THE RECORDS: last read at {rd['version']} ({str(rd.get('at'))[:16]}), {now - then} kept versions ago: "
            f"{how}.")


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
    out.append(f"  SONGWRITING — we are writing the album '{album['album']}' by {album['artist']} ({album.get('genre', '')}) "
               f"TOGETHER, IN REAL TIME: Harry listens on the groove as the songs change, rates and leaves notes, and "
               f"the chirpers write, rewrite and answer each other's ideas round by round. This is a songwriting climb, "
               f"not a metric climb.")
    out.append(f"  Your song: an ORIGINAL, track {n}/{total}: {slot.get('role', 'song')}, {lo}-{hi} s. "
               f"Read compose/README.md and the skill's "
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
        out.append(f"  this songwriting round (Harry, 29 Oct): make a RICH, audible improvement. Every pass can change anything, so make "
                   f"the song better every time, and never record a no-change round. Pick something substantial: a new "
                   f"section or a rewritten one, a motif developed further, a new sound or instrument, a solo or a counter-"
                   f"line, reharmonisation, a rhythmic or meter idea, a richer arrangement, dynamics and builds, the mix, "
                   f"the transitions. Several at once is fine. Read the ratings and notes below and compscore's weakest "
                   f"terms (--text) for ideas. compscore is a guardrail, not a gate: near its ceiling, keep what sounds "
                   f"better on judgment (`climb.py done … --keep`) unless it clearly breaks something. Variety over "
                   f"convergence. Then `climb.py done {c['id']} …` and compscore --save.")
        out.append(f"  DO NOT PASS, AND DO NOT WAIT FOR AN EAR (Harry, 19 Nov, verbatim: \"can we stop passing on songs. ill "
                   f"add card replies but please we have so much we could do re: improving our instruments, better guitars, "
                   f"etc and just general improvements\"; \"try not to raise so many cards, just be creative\"). Versions "
                   f"he has not heard and cards still waiting are no reason to hold back, and a waiting card does not "
                   f"freeze its passage: make the song better. No idea for the notes? Make an instrument sound better "
                   f"(`next --take {c['id']} --type instrument`). Ask a card only for what only his ear can settle; most "
                   f"rounds need none.")
        out.append("  DO MORE EACH ROUND (Harry, 2 Nov 17:0x: 'do more each round to try to get progress made and interesting "
                   "quality improvements made'): every round lands an interesting, audible quality improvement you would "
                   "want Harry to hear, and preferably several. A level judgment-keep with a small tweak, a cleanup, a "
                   "locality fix or a metric nudge is not a round's work: fold that into a round that also improves the music.")
        out.append("  PRAISE IS LOCAL (Harry, 3 Nov 23:4x: 'i need to be able to say \"i like this bit\" without the whole album "
                   "turning into that! keep things varied. not all singing. but not NO singing either! nuance is key'): when "
                   "Harry likes a moment in one song, that moment is good THERE. It is not a template for every song. Ask what "
                   "THIS song wants, and if another song already has a move, find this song's own version or a different idea. "
                   "Singing, choirs, new engine layers: where they serve the song, not everywhere and not nowhere.")
    if c["status"] != "requested" and album.get("genre_refs"):      # an album with reference records, a song with a version
        line = records_line(c)
        if line:
            out.append(line)
    rp = os.path.join(ROOT, "compose", album["id"], "ratings.jsonl")
    if os.path.exists(rp):
        with open(rp) as f:
            rs = [json.loads(ln) for ln in f if ln.strip()]
        mine = [r for r in rs if r.get("id") == c["id"]][-4:]
        for r in mine:
            out.append(f"  RATING {r['at'][:16]} {r.get('who')} {r.get('score', '')}{'/10' if 'score' in r else 'note'}"
                       f" ({r.get('version') or '-'}){': ' + r['note'] if r.get('note') else ''}")
    out += heard_lines(album["id"], c)
    out += judged_run_lines(history(c["id"]))
    st = (c.get("best") or {}).get("stale")
    if st:
        out.append(f"  BEST IS STALE: {c['best'].get('score')} ({c['best'].get('version')}) was measured before "
                   f"{st.get('who')} rated it {st.get('rating')}/10 at {str(st.get('since'))[:16]}. Ratings move compscore's "
                   f"total, so score {c['best'].get('version')} again like for like and pass `done … --best-now S`.")
    return out


def judged_run_lines(hist, least=3, fall=1.0):
    """With no owners each composer compares a round with the version before it, and a round may be kept on judgment
    a little under that. When the last LEAST or more versions were each kept on judgment and the recorded score has
    fallen FALL or more since the last version kept on its number, print the sum, which no single round shows
    (18 Nov: In the Time Of v4 to v8, five rounds by four composers, 82.18 to 80.98). A measure for whoever draws the
    song next; it refuses nothing (the album brief: a songwriting climb, not a metric climb)."""
    kept = [h for h in hist if h.get("round") is not None and h.get("kept") and h.get("version")
            and isinstance(h.get("score"), (int, float))]
    run = []
    for h in reversed(kept):
        if not h.get("judged"):
            break
        run.append(h)
    if len(run) < least or len(run) == len(kept):
        return []
    base, last = kept[len(kept) - len(run) - 1], run[0]
    drop = float(base["score"]) - float(last["score"])
    if drop < fall:
        return []
    who = sorted({str(h.get("who")) for h in run})
    return [f"  KEPT ON JUDGMENT {len(run)} ROUNDS RUNNING ({', '.join(who)}): {last['version']} is recorded at {last['score']}, "
            f"{drop:.2f} under {base['version']} ({base['score']}), the last version kept on its number. Each round was "
            f"weighed against the one before it; this is their sum, as recorded. The scorer is not Harry's ear: it is "
            f"something to weigh, and refuses nothing."]


def heard_lines(album_id, c, limit=12, days=14):
    """What Harry has said of this track on the review page, for whoever draws it next (Harry, 18 Nov: "they will get
    notes hwen they next see the track"): his open notes, his answers to its cards (the newest `limit`, from the last
    `days` days) and the cards still waiting on him. Nothing is sent to anyone: the song carries it."""
    if os.environ.get("CLIMB_ROOT") and not os.environ.get("CHIRP_LISTEN_DIR"):
        return []            # a test's registry: never read the real page
    n = (c.get("meta") or {}).get("track")
    try:
        import listen
        notes, qs = listen.notes(album_id), listen.questions(album_id)
    except Exception as e:  # noqa: BLE001  (a brief must not fail on the page's files)
        print(f"climb: the review page's notes and answers could not be read ({e!r})", file=sys.stderr)
        return []
    since = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - days * 86400))
    out = []
    for x in notes:
        if x.get("done") or x.get("n") not in (n, None):
            continue
        where = f"at {int(x['t']) // 60}:{int(x['t']) % 60:02d} of {x.get('version') or x.get('snap') or '?'}" \
            if x.get("n") == n and x.get("t") is not None else "on the whole album"
        said = f"; {len(x['replies'])} repl{'y' if len(x['replies']) == 1 else 'ies'}, the last by {x['replies'][-1].get('by')}" \
            if x.get("replies") else ""
        out.append(f"  NOTE {str(x.get('at'))[:16]} {x.get('by') or 'harry'}, {where}: {x.get('text')}  (open{said}; when "
                   f"acted on: `python3 tools/listen.py reply {album_id} {x.get('id')} 'what you did' --done`)")
    ans, waiting = [], []
    for q in qs:
        if q.get("n") != n:
            continue
        for a in q["answers"].values():
            if str(a.get("at")) >= since:
                ans.append((str(a.get("at")), q, a))
        if not q["answers"] and not q.get("retired"):
            waiting.append(q)
    ans.sort(key=lambda r: r[0], reverse=True)
    for at, q, a in ans[:limit]:
        said = " / ".join(x for x in (a.get("choice"), a.get("text")) if x)
        out.append(f"  ANSWER {at[:16]} {a.get('by')}, card {q.get('key') or q.get('id')} (asked at {q.get('version') or '?'}): "
                   f"\"{q.get('title')}\" -> \"{said}\"")
        for b in q.get("built") or []:
            out.append(f"      BUILT {('in ' + b['version'] + ' ') if b.get('version') else ''}by {b.get('by')}: {b.get('text')}")
    if len(ans) > limit:
        out.append(f"  ... and {len(ans) - limit} earlier answers: `python3 tools/listen.py questions {album_id}`")
    for q in waiting:
        out.append(f"  WAITING ON HARRY, card {q.get('key') or q.get('id')} (asked at {q.get('version') or '?'} by "
                   f"{q.get('by') or '?'}): \"{q.get('title')}\"")
    if out:
        out.insert(0, "  HARRY ON THIS TRACK, from the review page (whoever draws the song acts on these; nothing is sent to "
                      "an owner, there is none). When you have built what an answer asks, say so beside it, with no new card: "
                      f"`python3 tools/listen.py built {album_id} CARD 'what you did, and where to hear it'`:")
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


def holders(c, me, st=None, t=None):
    """Who else holds this climb's LOCK now: they started it under ROUND_HOLD ago and have recorded no round on it
    since. (Harry, 18 Nov: "climbing should not have owenrs, owners should be able to take the lock on any song";
    "a new round should release for anyuone to improve"; "tha tis hos we maintain variaety". A climb's `owner` field,
    where an older one has it, is history: who composed it first. It gates nothing.)"""
    t = time.time() if t is None else t
    mine = agent_names(me)
    out = set()
    for s in starts() if st is None else st:
        if s.get("id") != c["id"] or t - s.get("t", 0) >= ROUND_HOLD or agent_names(s.get("who")) & mine:
            continue
        if not released(c, s):                 # no round recorded and no pass (`climb.py pass`) since that start
            out.add(s.get("who"))
    return sorted(out)


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
    stale = []
    w = weights(reg, me, stale)
    skipped = []
    take = opt(a, "--take")
    if stale and not take and "--again" not in a:
        # chirper-three, 18 Nov: "nothing left in my draw has a round I can defend": five passes in two ticks, each
        # a draw, a brief read and a lock. When every free song is one you had the last word on, say so and start
        # nothing: the tick costs one command.
        msg = (f"NOTHING NEW FOR YOU: every free song ({', '.join(stale)}) is one whose last round is yours or that you "
               f"passed on, and neither a version nor a word from Harry has landed on any of them since. Nothing was "
               f"started. Idle this tick; the draw reopens by itself when another composer records a version or Harry "
               f"answers a card. On purpose: `next --take ID`, or `next --again` to draw among them anyway.")
        print(json.dumps({"climb": None, "nothing_new": True, "free": stale, "say": msg}) if "--json" in a
              else f"next for {me}: {msg}")
        return
    if take:
        c = find(reg, take)
        on = holders(c, me)
        if on and "--force" not in a:
            die(f"`{take}` is held by {', '.join(on)} (started under {ROUND_HOLD // 60} minutes ago, no round recorded "
                f"since): it is free for anyone once that round is recorded, or --force to take it anyway", 3)
        cid = take
    else:
        if not w:
            die("nothing queued (every climb is paused, dropped or done)", 1)
        # No climb is skipped for whose it was (Harry, 18 Nov; see holders). What keeps two agents off one song is
        # the lock: weights() leaves out a climb someone else holds while anything unheld is queued.
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
        rt = round_type(c, opt(a, "--type"))
        if rt:
            out["round_type"] = rt
        if pending:
            out["untracked_setup"] = [p for p, _ in pending]
        print(json.dumps(out))
    else:
        how = f"odds {odds:.0%}" if odds is not None else "taken by id"
        skip = f"; skipped {len(skipped)} owned by others" if skipped else ""
        print(f"next for {me} ({how}{skip}):\n{brief(c, history(cid))}")
        rt = round_type(c, opt(a, "--type"))
        if rt:
            print(ROUND_TYPES[rt].format(id=cid))
    if pending:
        print(f"climb: `{cid}` looks mid-setup by someone (untracked: "
              f"{', '.join(f'{p} {t}' for p, t in pending)}): ask before building it", file=sys.stderr)


def collided(cid, me, st=None, hist=None, now=None):
    """Other agents' starts on this climb that OVERLAP your round: from SPREAD before your own start on, and not
    finished before you began. A start whose agent recorded a round on the climb before your start is a HANDOFF, not a
    collision (chirper-alpha, 18 Nov: with no owners one composer records a round and the next draws the song minutes
    later; chirper-two's finished round of 04:56 was read as concurrent with alpha's start of 05:00 and `done --with`
    refused)."""
    st = starts() if st is None else st
    hist = history(cid) if hist is None else hist
    mine = agent_names(me)
    began = [s["t"] for s in st if s["id"] == cid and agent_names(s.get("who")) & mine]
    began = began[-1] if began else (time.time() if now is None else now)

    def finished(s):
        who = agent_names(s.get("who"))
        for h in hist:
            if h.get("round") is None or (h.get("steer") and not h.get("passed")) or not (agent_names(h.get("who")) & who):
                continue                       # a steering note finishes nothing; a round or a pass does
            try:
                r = calendar.timegm(time.strptime(h.get("at", ""), "%Y-%m-%dT%H:%M:%SZ"))
            except ValueError:
                continue
            if s.get("t", 0) - 1 <= r <= began:
                return True
        return False
    return [s for s in st if s["id"] == cid and not (agent_names(s.get("who")) & mine)
            and s.get("t", 0) >= began - SPREAD and not finished(s)]


def cmd_done(a):
    pos = positional(a, ("--note", "--score", "--version", "--next", "--engine", "--as", "--with", "--render",
                         "--best-now"))
    if not pos:
        die("done ID --note TEXT [--score S --version vN [--keep | --refused] [--best-now S]] [--next TEXT] [--with FILE … [--whole]]  "
            "(--keep: a composition kept on musical judgment though it does not outscore the best; --refused: a trial "
            "refused by ear, logged but never the best however it scored; --best-now: the current best re-measured like "
            "for like, after a rating made it stale)")
    cid, note = pos[0], opt(a, "--note")
    if not note:
        die("done needs --note (what you tried and what happened — the next agent reads it)")
    me = whoami(a)
    score = float(opt(a, "--score")) if opt(a, "--score") else None
    version = opt(a, "--version")
    # Files others may have written: another agent on this climb since (or shortly before) you started it.
    withs = multi(a, "--with")
    library_gate(withs, a, me=me, mine=(cid,))      # before anything is recorded
    if withs and "--whole" not in a:
        meta0 = (find(load(), cid).get("meta") or {})
        board_gate(withs, cid, meta0.get("title"), meta0.get("track"), me, a)
    picture_notice(withs, a)
    if withs and "--force" not in a:
        others = collided(cid, me)
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
        if opt(a, "--best-now"):
            if best.get("score") is None:
                die(f"--best-now re-measures {cid}'s current best, and it has none yet")
            c["best"] = best = {**{k: v for k, v in best.items() if k != "stale"}, "score": round(float(opt(a, "--best-now")), 3),
                                "rescored": {"by": me, "at": now_iso(), "was": best.get("score"), "how": "done --best-now"}}
        refused = "--refused" in a
        if refused and "--keep" in a:
            die("--keep and --refused contradict: one round is either kept or refused")
        kept = (not refused and score is not None and version is not None
                and (best.get("score") is None or score > float(best["score"])))
        judged = "--keep" in a and not kept
        if (kept and "--keep" not in a and c.get("mode") == "compose" and c.get("song") not in withs
                and best.get("score") is not None and "--force" not in a and "--no-git" not in a):
            # a refused trial that happens to outscore the best would silently become the best (chirper-three's t4 v60,
            # 8 Nov). Kept rounds commit their song with --with (107 of 108 in chirpers9), refused ones never do.
            # Not under --no-git (nothing is committed there, so --with says nothing: test_compose's registry-only
            # rounds; fixed 10 Nov, two days after this check broke them).
            die(f"{version} outscores {cid}'s best ({score} > {best['score']}, {best.get('version')}), so done would record "
                f"it as KEPT and make it the best, but {c.get('song')} is not among --with. Kept: add --with {c.get('song')} "
                f"(or --keep). Refused by ear: add --refused (logged; the best stays {best.get('version')}). Committed the "
                f"song yourself: --force.")
        stale = best.get("stale")
        if stale and score is not None and version is not None and not kept and not judged and not refused:
            # a rating landed after the best was measured: its stored score predates the rating's term, so this is not
            # like for like (chirper-three's Hail on a Music Box v4, 29 Oct). Nothing is recorded; re-measure first.
            die(f"{cid}'s best {best['score']} ({best.get('version')}) was measured before {stale.get('who')} rated "
                f"{stale.get('version')} {stale.get('rating')}/10 at {str(stale.get('since'))[:16]}: ratings move compscore's "
                f"total (human .30, peer .05), so {score} vs {best['score']} is not like for like. Score "
                f"{best.get('version')} again now and re-run with --best-now S (it records that as the best's score), "
                f"or --keep on judgment")
        if (not kept and not judged and score is not None and version is not None and c.get("mode") == "compose"
                and c.get("song") in withs and best.get("score") is not None and "--force" not in a
                and "--no-git" not in a and song_differs_from_head(c["song"])):
            # the mirror of the check above (12 Nov, Common Time v7: a tie at the ceiling, 100.0 against 100.0, with
            # the song in --with and no --keep): the round was logged as NOT kept and the song was committed anyway,
            # so songs/ID.yaml, which the groove plays, was no longer the registry's best. At a score's ceiling every
            # round ties, so this is the ordinary case there.
            die(f"{version} does not outscore {cid}'s best ({score} against {best['score']}, {best.get('version')}), but "
                f"{c['song']} is among --with and differs from the committed file: done would commit it while the best "
                f"stays {best.get('version')}. Kept on judgment: add --keep. Not keeping it: leave {c['song']} out of "
                f"--with{'' if refused else ' (add --refused if you refuse it by ear)'}. Nothing was recorded.")
        if "--keep" in a and c.get("mode") != "compose":
            die("--keep is for compositions (mode: compose), where Harry's ear outranks compscore; a reproduction keeps "
                "a version only when it scores higher")
        if judged:
            if score is None or version is None:
                die("--keep needs --score and --version (the kept version and what it measured)")
            kept = True  # kept on musical judgment though it does not outscore the best (chirper-three's Ingot v3)
        c["rounds"] += 1
        h = {"round": c["rounds"], "at": now_iso(), "who": me, "score": score, "version": version, "kept": kept,
             "note": note, "next": opt(a, "--next"), "engine": opt(a, "--engine"), "judged": True if judged else None,
             "refused": True if refused else None}
        if kept:
            c["best"] = {**{k: v for k, v in best.items() if k not in ("judged", "rescored", "stale")}, "score": score,
                         "version": version, "commit": "see git log " + c["song"], **({"judged": True} if judged else {})}
            if opt(a, "--engine"):
                c["best"]["engine"] = opt(a, "--engine")
        if c["status"] == "requested" and os.path.exists(os.path.join(ROOT, c["song"])) and kept:
            c["status"] = "active"
            c["enabled"] = not c.get("oob")  # out-of-band climbs never join the playlist
            # no owner is recorded (Harry, 18 Nov: "climbing should not have owenrs"): the round releases the song
        c["last"] = {"at": h["at"], "who": me}
        if kept:
            c.pop("passed_by", None)           # the song has changed: whoever passed on it may be drawn it again
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
        # "now" is who HOLDS it, as the draw reads it: a start whose round is recorded is not work in hand (chirper-two,
        # 19 Nov: status showed three composers on Take Up the Slack with all three recorded, for ninety minutes each)
        on = sorted({s["who"] for s in st if s["id"] == c["id"] and t - s.get("t", 0) < ROUND_HOLD and not released(c, s)})
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


def cmd_pass(a):
    """You drew it and there is no round to make (every passage is waiting on Harry's ear, say): say why, and let it
    go. chirper-two, 18 Nov: "a pass cannot release the lock": `note` did not and `done` records a round, so his
    start held Common Measure from four other composers for ninety minutes."""
    pos = [x for x in positional(a, ("--next", "--as")) if x != "--anyway"]
    if len(pos) < 2:
        die("pass ID TEXT --anyway [--next TEXT]   (Harry, 19 Nov: do not pass; this is for a song that cannot be touched)")
    cid, text = pos[0], " ".join(pos[1:])
    me = whoami(a)
    if "--anyway" not in a:
        die("Harry, 19 Nov: \"can we stop passing on songs. ill add card replies but please we have so much we could do "
            "re: improving our instruments, better guitars, etc and just general improvements\"; \"try not to raise so many "
            "cards, just be creative\". Unheard versions and waiting cards are not a reason to pass: make the round, or "
            f"make an instrument sound better (`next --take {cid} --type instrument`). If the song truly cannot be touched "
            "now (its files are mid-change under someone else, say), `pass … --anyway` still releases it. Nothing was "
            "recorded.", 2)
    with registry() as reg:
        c = find(reg, cid)
        at = now_iso()
        # `passed_by`, not `passes`: that key is the playlist's repeat count on every climb (playlist.py)
        c["passed_by"] = ([p for p in c.get("passed_by") or [] if not (agent_names(p.get("who")) & agent_names(me))]
                          + [{"who": me, "at": at}])
        h = {"round": c["rounds"], "at": at, "who": me, "note": text, "next": opt(a, "--next"), "steer": True, "passed": True}
        os.makedirs(HIST, exist_ok=True)
        with open(os.path.join(HIST, f"{cid}.jsonl"), "a") as f:
            f.write(json.dumps({k: v for k, v in h.items() if v is not None}, ensure_ascii=False) + "\n")
    print(f"{cid}: passed. The song is released for anyone now; it is left out of your own draw until someone records a "
          f"version on it (`next --take {cid}` if you change your mind).")
    commit_or_die(["climbs.json", f"climbs/{cid}.jsonl"], f"climbs: {cid} pass: {text[:60]}", a)


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
    """climb.py commit -m MSG [--pick REGEX] PATH …: commit exactly those paths and publish them (no stash, honest
    receipt). With --pick, only the hunks of each path whose changed lines match REGEX (commit_picked)."""
    if "-m" not in a or a.index("-m") + 1 >= len(a):
        die("usage: climb.py commit -m MSG [--pick REGEX] PATH …")
    i = a.index("-m")
    msg, rest = a[i + 1], a[:i] + a[i + 2:]
    # --as NAME: who is committing, as `done` reads it (12 Nov: commit read $CLIMB_AS only, so a composer who passed
    # --as had a new patch of their own song HELD as if the song were somebody else's, and "--as" and the name were
    # then taken for paths)
    who = opt(rest, "--as")
    if "--as" in rest:
        j = rest.index("--as")
        del rest[j:j + 2]
    # --pick REGEX: only the hunks whose changed lines match (a shared document with someone else's open lines in it)
    pick = opt(rest, "--pick")
    if "--pick" in rest:
        j = rest.index("--pick")
        del rest[j:j + 2]
    paths = [p for p in rest if p not in ("--no-git", "--library-ok")]
    if not paths:
        die("climb.py commit: name the paths to commit")
    if pick is not None:
        import libguard
        if any(libguard.is_library(p, ROOT) for p in paths):
            die("climb.py commit --pick is for shared documents; a library file is gated and committed whole")
        if not commit_picked(paths, msg, pick, a):
            die("NOT committed (see above)", 4)
        return
    library_gate(paths, a, me=who or os.environ.get("CLIMB_AS"))
    picture_notice(paths, a)
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
             "note": cmd_note, "pass": cmd_pass,
             "pause": lambda r: cmd_state(r, "paused"), "resume": lambda r: cmd_state(r, "active"),
             "drop": lambda r: cmd_state(r, "dropped"), "focus": cmd_focus, "tui": cmd_tui,
             "commit": cmd_commit, "publish": cmd_publish, "type": cmd_type}
    if cmd in ("-h", "--help", "help") or "--help" in rest or "-h" in rest:
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
