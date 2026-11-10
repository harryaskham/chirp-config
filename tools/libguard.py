#!/usr/bin/env python3
"""libguard: does a library change alter songs it should not? (chirp-eco, 10 Nov)

The user library (patches/, racks/, styles/, irs/ here) is LIVE: every pin reads it at render time, so an edit to a
patch another song uses changes that song at once - a released album no longer renders as it was released, or another
composer's song moves under them. Until now nothing checked this (the engine gate compares two binaries under the SAME
library). Harry, 10 Nov: "don't be afraid to make changes from engine through library to song structure" - so library
work is welcome; this keeps it additive where it must be.

  libguard.py [PATH ...] [--json] [--me NAME] [--only ID ...]
      PATH: library files as they are in the working tree (added, modified or deleted against HEAD).
            Default: every library file that differs from HEAD.

How: the engine's own answer. `chirp plan` prints a song's canonical, self-contained form (every patch, rack and style
resolved), so a song whose canonical plan is unchanged cannot render differently. Each registered song (climbs.json),
at its COMMITTED text, is planned twice - against HEAD's library and against HEAD's library with PATHs applied (both
exported to a temp dir, CHIRP_CONFIG pointing at them; the working tree is never touched) - and the two are compared.
That also catches a new file that shadows a built-in patch of the same name, and a deleted file.
An asset the plan only names (an impulse response under irs/) is matched by name instead: a changed or deleted asset
flags every song whose plan mentions it.

Reported, and the exit code:
  1  songs outside the album in progress change (released albums, the playlist's reproductions): never do this - save
     the file under a new name, or keep the change in your song (`extends: NAME` plus overrides, see extendslint.py)
  2  only songs of the album in progress change, and some are not yours (--me NAME: the climbs you own): tell their
     owners first, or use a new name
  0  nothing else changes (a new patch nothing uses yet, or only your own songs)
Read-only. About 0.3 s a song and side (a minute for the whole registry on a quiet host).
"""
import argparse
import concurrent.futures
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(HERE)
LIB_DIRS = ("patches", "racks", "styles", "irs")
TEXT_EXT = (".yaml", ".yml", ".json")


def rel(path, root=None):
    root = root or ROOT
    p = path if os.path.isabs(path) else os.path.join(root, path)
    return os.path.relpath(os.path.abspath(p), os.path.abspath(root))


def is_library(path, root=None):
    """True for a path under one of the library directories of the config repo."""
    r = rel(path, root)
    return any(r.startswith(d + os.sep) for d in LIB_DIRS)


def read_bytes(path):
    with open(path, "rb") as f:
        return f.read()


def git(root, *args, binary=False):
    r = subprocess.run(["git", "-C", root, *args], capture_output=True, text=not binary)
    return r.stdout if r.returncode == 0 else None


def dirty_library(root=None):
    """Library paths that differ from HEAD in the working tree (added, modified, deleted)."""
    root = root or ROOT
    out = git(root, "status", "--porcelain", "--untracked-files=all", "--", *LIB_DIRS) or ""
    return sorted({ln[3:].split(" -> ")[-1].strip().strip('"') for ln in out.splitlines() if ln[3:].strip()})


def export_head(root, dst):
    """HEAD's library, config and songs under DST/before (+ DST/songs); returns the names exported."""
    have = [d for d in (*LIB_DIRS, "config.yaml", "songs") if git(root, "cat-file", "-e", f"HEAD:{d}") is not None]
    before = os.path.join(dst, "before")
    os.makedirs(before)
    with subprocess.Popen(["git", "-C", root, "archive", "HEAD", *have], stdout=subprocess.PIPE) as ar:
        subprocess.run(["tar", "-x", "-C", before], stdin=ar.stdout, check=True)
    if os.path.isdir(os.path.join(before, "songs")):
        os.rename(os.path.join(before, "songs"), os.path.join(dst, "songs"))
    else:
        os.makedirs(os.path.join(dst, "songs"))
    os.symlink(os.path.join(dst, "songs"), os.path.join(before, "songs"))
    if not os.path.exists(os.path.join(before, "config.yaml")):
        open(os.path.join(before, "config.yaml"), "w").close()
    return have


def build_after(root, dst, changes):
    """DST/after: HEAD's library with CHANGES {relpath: bytes | None (deleted)} applied. Untouched directories are
    shared with DST/before."""
    before, after = os.path.join(dst, "before"), os.path.join(dst, "after")
    os.makedirs(after)
    touched = {p.split(os.sep)[0] for p in changes}
    for name in os.listdir(before):
        src = os.path.join(before, name)
        if name in touched and os.path.isdir(src) and not os.path.islink(src):
            shutil.copytree(src, os.path.join(after, name))
        elif os.path.isfile(src) and not os.path.islink(src):
            shutil.copy(src, os.path.join(after, name))      # config.yaml: a real file, so its directory is AFTER's
        else:
            os.symlink(os.path.realpath(src), os.path.join(after, name))
    for d in touched:
        os.makedirs(os.path.join(after, d), exist_ok=True)
    for p, data in changes.items():
        t = os.path.join(after, p)
        if data is None:
            os.path.exists(t) and os.unlink(t)
        else:
            os.makedirs(os.path.dirname(t), exist_ok=True)
            with open(t, "wb") as f:
                f.write(data)
    return after


def engine_planner(pin):
    """(config dir, song path) -> (sha of the canonical plan, its text) or (None, '') when the song does not plan."""
    def plan(cfg, song):
        env = dict(os.environ, CHIRP_CONFIG=os.path.join(cfg, "config.yaml"))
        env.pop("LD_LIBRARY_PATH", None)
        r = subprocess.run([pin, "plan", "-f", song, "--json"], capture_output=True, text=True, env=env,
                           cwd=os.path.dirname(song), stdin=subprocess.DEVNULL)
        try:
            text = json.dumps(json.loads(r.stdout)["data"]["canonical"], sort_keys=True)
        except (ValueError, KeyError, TypeError):
            return None, ""
        return hashlib.sha256(text.encode()).hexdigest()[:16], text
    return plan


def registry(root):
    """[(id, song relpath, owner, album)] of every registered climb, and the album in progress."""
    try:
        with open(os.path.join(root, "climbs.json")) as f:
            reg = json.load(f)
    except (OSError, ValueError):
        return [], None
    rows = [(c["id"], c.get("song") or f"songs/{c['id']}.yaml", c.get("owner"),
             str((c.get("meta") or {}).get("album") or "")) for c in reg.get("climbs", [])]
    return rows, reg.get("focus")


def check(paths=None, root=None, pin=None, planner=None, overlay=None, me=None, only=None, mine=(), jobs=4):
    """Compare every registered song's canonical plan under HEAD's library and under HEAD's library with the changes.
    PATHS are read from the working tree; OVERLAY {relpath: bytes | str | None} gives contents directly (tests, what-if).
    Returns {paths, checked, frozen: [ids], progress: [{id, owner}], own: [ids], assets: [ids], unplannable: [ids]}."""
    root = root or ROOT
    changes = {}
    for p in paths or []:
        r = rel(p, root)
        if not is_library(r, root):
            continue
        full = os.path.join(root, r)
        changes[r] = read_bytes(full) if os.path.isfile(full) else None
    for p, data in (overlay or {}).items():
        changes[rel(p, root)] = data.encode() if isinstance(data, str) else data
    # a path identical to HEAD is no change
    for p in list(changes):
        head = git(root, "show", f"HEAD:{p}", binary=True)
        if head == changes[p] or (head is None and changes[p] is None):
            del changes[p]
    res = {"paths": sorted(changes), "checked": 0, "frozen": [], "progress": [], "own": [], "assets": [],
           "unplannable": []}
    if not changes:
        return res
    if planner is None:
        if pin is None:
            sys.path.insert(0, HERE)
            import chirpbin
            pin = chirpbin.resolve("chirp")
        planner = engine_planner(pin)
    rows, focus = registry(root)
    if only:
        rows = [r for r in rows if r[0] in set(only)]
    # an asset: a non-text library file that existed at HEAD and now differs or is gone (the plan only names it)
    assets = [os.path.splitext(os.path.basename(p))[0] for p in changes
              if not p.endswith(TEXT_EXT) and git(root, "cat-file", "-e", f"HEAD:{p}") is not None]
    dst = tempfile.mkdtemp(prefix="libguard-")
    try:
        export_head(root, dst)
        before, after = os.path.join(dst, "before"), build_after(root, dst, changes)

        def one(row):
            cid, song, owner, album = row
            sp = os.path.join(dst, song)
            if not os.path.isfile(sp):
                return row, "missing", ""
            (a, text), (b, _) = planner(before, sp), planner(after, sp)
            if a is None and b is None:
                return row, "unplannable", ""
            return row, ("same" if a == b else "changed"), text

        with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as ex:
            done = list(ex.map(one, rows))
    finally:
        shutil.rmtree(dst, ignore_errors=True)
    for (cid, song, owner, album), state, text in done:
        if state == "missing":
            continue
        res["checked"] += 1
        if state == "unplannable":
            res["unplannable"].append(cid)
            continue
        hit = state == "changed"
        if not hit and assets and any(re.search(rf"(?<![A-Za-z0-9_-]){re.escape(n)}(?![A-Za-z0-9_-])", text) for n in assets):
            hit = True
            res["assets"].append(cid)
        if not hit:
            continue
        in_progress = bool(focus) and album.casefold() == str(focus).casefold()
        if not in_progress:
            res["frozen"].append(cid)
        elif cid in mine or (me and owner == me):
            res["own"].append(cid)
        else:
            res["progress"].append({"id": cid, "owner": owner})
    return res


def verdict(res):
    """(exit code, lines) for a check() result."""
    if not res["paths"]:
        return 0, ["libguard: no library file differs from HEAD"]
    lines = [f"libguard: {len(res['paths'])} library file(s) ({', '.join(res['paths'][:6])}"
             f"{', ...' if len(res['paths']) > 6 else ''}) against {res['checked']} registered songs"]
    code = 0
    if res["frozen"]:
        code = 1
        lines.append(f"  CHANGES {len(res['frozen'])} song(s) outside the album in progress: {', '.join(res['frozen'][:12])}"
                     f"{', ...' if len(res['frozen']) > 12 else ''}")
        lines.append("  a released album must keep rendering as it was released: save the file under a NEW name, or keep "
                     "the change in your song (`extends: NAME` plus overrides)")
    if res["progress"]:
        code = code or 2
        lines.append("  changes songs of the album in progress that are not yours: "
                     + ", ".join(f"{p['id']} ({p['owner'] or 'no owner'})" for p in res["progress"]))
        lines.append("  tell their owners before it lands (their scores and seams move), or use a new name")
    if res["own"]:
        lines.append(f"  changes your own: {', '.join(res['own'])}")
    if res["assets"]:
        lines.append(f"  (matched by asset name, not by plan: {', '.join(res['assets'][:8])})")
    if res["unplannable"]:
        lines.append(f"  not checked (do not plan on this pin at HEAD): {', '.join(res['unplannable'][:8])}"
                     f"{', ...' if len(res['unplannable']) > 8 else ''}")
    if code == 0:
        lines.append("  no other song changes")
    return code, lines


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--me", help="your climbs' owner name: your own songs of the album in progress may change")
    ap.add_argument("--only", nargs="+", metavar="ID", help="check only these climbs (quick what-if)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    paths = a.paths or dirty_library()
    res = check(paths, me=a.me, only=a.only)
    code, lines = verdict(res)
    print(json.dumps(res, indent=1) if a.json else "\n".join(lines))
    return code


if __name__ == "__main__":
    sys.exit(main())
