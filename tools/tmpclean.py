#!/usr/bin/env python3
"""Temp audio janitor: keep agents' scratch renders from filling the disk.

  tmpclean.py [--dry-run] [--age H] [--stems-age H] [--cap GB] [--min-free GB] [--min-age MIN]
              [--every MIN] [--loop SECONDS] [--quiet] [ROOT...]

Only audio files (wav flac mp3 ogg opus webm m4a aif aiff) are ever deleted: under each ROOT
(default /tmp/lt, recursively) and directly in /tmp. Never: anything used in the last --min-age
minutes (default 30), symlinks, other users' files, git checkouts (a top-level dir with .git,
e.g. /tmp/lt/chirp-main), build dirs (target/, node_modules/, .git/).

"Last used" is the later of mtime and atime. In order:
  1. renders idle past --age hours (default 6) go; stems (a path part naming stems/sep/demucs)
     past --stems-age hours (default 72): separating a reference again is slow;
  2. while the remaining audio under the roots exceeds --cap GB (default 10): oldest renders, then
     oldest stems;
  3. while the disk has less than --min-free GB free (default 25): oldest audio of any kind.

--every MIN: do nothing if the last run was under MIN minutes ago (for hooks: climb.py runs it
on every next/done). --loop S: run every S seconds (a detached janitor). One run at a time
(flock). A line per run goes to /tmp/lt/tmpclean.log.

Keep audio you need beyond a round in ~/.config/chirp/ref/ (git-ignored) or a song's own
evidence folder, not /tmp. For comparison renders you need for a day or two (a long round, a daemon restart),
`touch DIR/.tmpclean-keep`: audio under DIR is then treated like stems (--stems-age, default 72 h since last
use; deleted after ordinary renders when over the cap; disk pressure still applies). Delete the marker when done.
"""
import fcntl
import os
import re
import shutil
import sys
import time

AUDIO = {".wav", ".flac", ".mp3", ".ogg", ".opus", ".webm", ".m4a", ".aif", ".aiff"}
SKIP_DIRS = {".git", "target", "node_modules", "__pycache__"}
STEMS = re.compile(r"(stem|sep|demucs|htdemucs|mdx)", re.I)
KEEP = ".tmpclean-keep"   # a directory holding this file keeps its audio like stems
STATE = "/tmp/lt"
LOG = f"{STATE}/tmpclean.log"
STAMP = f"{STATE}/.tmpclean-stamp"
LOCK = f"{STATE}/.tmpclean.lock"


def opt(a, flag, default, cast=float):
    if flag in a:
        i = a.index(flag)
        v = a[i + 1]
        del a[i:i + 2]
        return cast(v)
    return default


def flag(a, name):
    if name in a:
        a.remove(name)
        return True
    return False


def candidates(roots):
    """(path, size, last_used, is_stem) for each deletable audio file."""
    me = os.getuid()
    out = []
    marked = {}

    def kept(d):
        """Whether d or a parent (below /) holds the keep marker."""
        if d not in marked:
            up = os.path.dirname(d)
            marked[d] = os.path.exists(os.path.join(d, KEEP)) or (up != d and up != "/" and kept(up))
        return marked[d]

    def consider(p, st):
        if st.st_uid != me or os.path.splitext(p)[1].lower() not in AUDIO:
            return
        out.append((p, st.st_size, max(st.st_mtime, st.st_atime), bool(STEMS.search(p)) or kept(os.path.dirname(p))))

    for root in roots:
        if not os.path.isdir(root):
            continue
        for top in os.scandir(root):
            if top.is_symlink():
                continue
            if top.is_file():
                consider(top.path, top.stat())
                continue
            if not top.is_dir() or top.name in SKIP_DIRS or os.path.exists(os.path.join(top.path, ".git")):
                continue
            for d, dirs, files in os.walk(top.path):
                dirs[:] = [x for x in dirs if x not in SKIP_DIRS and not os.path.islink(os.path.join(d, x))]
                for f in files:
                    p = os.path.join(d, f)
                    try:
                        st = os.lstat(p)
                    except OSError:
                        continue
                    if os.path.isfile(p) and not os.path.islink(p):
                        consider(p, st)
    # Loose audio directly in /tmp (agents' one-off renders).
    for e in os.scandir("/tmp"):
        if e.is_file(follow_symlinks=False):
            try:
                consider(e.path, e.stat(follow_symlinks=False))
            except OSError:
                pass
    return out


def free_gb(path="/tmp"):
    return shutil.disk_usage(path).free / 1e9


def run(roots, age, stems_age, cap, min_free, min_age, dry):
    now = time.time()
    files = candidates(roots)
    gone, why = [], {"age": 0, "cap": 0, "disk": 0}
    old_enough = lambda f: now - f[2] > min_age * 60  # noqa: E731

    def drop(f, reason):
        if not dry:
            try:
                os.remove(f[0])
            except OSError:
                return False
            # A directory our deletions emptied goes too (never a root).
            d = os.path.dirname(f[0])
            while d not in roots and d != "/tmp" and d.startswith("/tmp/"):
                try:
                    os.rmdir(d)
                except OSError:
                    break
                d = os.path.dirname(d)
        gone.append(f)
        why[reason] += 1
        return True

    keep = []
    for f in files:
        limit = (stems_age if f[3] else age) * 3600
        if now - f[2] > limit and old_enough(f):
            drop(f, "age")
        else:
            keep.append(f)
    # Over the cap: oldest renders first, then oldest stems.
    under = [f for f in keep if any(f[0].startswith(r.rstrip("/") + "/") for r in roots)]
    total = sum(f[1] for f in under)
    for f in sorted(under, key=lambda f: (f[3], f[2])):
        if total <= cap * 1e9:
            break
        if old_enough(f) and drop(f, "cap"):
            total -= f[1]
            keep.remove(f)
    # Short of disk: oldest audio of any kind.
    freed = sum(f[1] for f in gone) if dry else 0
    for f in sorted(keep, key=lambda f: f[2]):
        if free_gb() + freed / 1e9 >= min_free:
            break
        if old_enough(f) and drop(f, "disk") and dry:
            freed += f[1]
    size = sum(f[1] for f in gone) / 1e9
    kept = [f for f in keep if f not in gone]
    return (
        f"{time.strftime('%F %T')} tmpclean{' (dry run)' if dry else ''}: deleted {len(gone)} files "
        f"({size:.1f} GB: age {why['age']}, cap {why['cap']}, disk {why['disk']}); "
        f"kept {len(kept)} ({sum(f[1] for f in kept) / 1e9:.1f} GB); free {free_gb():.0f} GB"
    )


def main():
    a = sys.argv[1:]
    if flag(a, "-h") or flag(a, "--help"):
        print(__doc__)
        return
    dry = flag(a, "--dry-run")
    quiet = flag(a, "--quiet")
    age = opt(a, "--age", 6.0)
    stems_age = opt(a, "--stems-age", 72.0)
    cap = opt(a, "--cap", 10.0)
    min_free = opt(a, "--min-free", 25.0)
    min_age = opt(a, "--min-age", 30.0)
    every = opt(a, "--every", 0.0)
    loop = opt(a, "--loop", 0.0)
    roots = [os.path.abspath(r) for r in a] or [STATE]
    os.makedirs(STATE, exist_ok=True)
    while True:
        due = not every or not os.path.exists(STAMP) or time.time() - os.path.getmtime(STAMP) > every * 60
        if due:
            with open(LOCK, "w") as lk:
                try:
                    fcntl.flock(lk, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except BlockingIOError:
                    lk = None
                if lk:
                    line = run(roots, age, stems_age, cap, min_free, min_age, dry)
                    if not dry:
                        open(STAMP, "w").close()
                        with open(LOG, "a") as log:
                            log.write(line + "\n")
                    if not quiet:
                        print(line)
        if not loop:
            return
        time.sleep(loop)


if __name__ == "__main__":
    main()
