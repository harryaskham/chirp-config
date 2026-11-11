#!/usr/bin/env python3
"""Engine pins that outlive /tmp.

  pinstore.py keep PIN...    copy each pin binary into the store (once), with its sha256 beside it
  pinstore.py restore PIN    if PIN is missing, bring it back from the store, checked; exit 0 when PIN is there
  pinstore.py seal           record the sha256 of stored pins that have none yet
  pinstore.py list           what the store holds

Pins live in /tmp/lt/pins (shared, pruned), and the system deletes anything in /tmp that nobody has used for ten
days. Two kinds of pin must survive that: the groove's (tools/groove-pin: restart-groove.sh refuses to start
without it) and every release's (an album is re-cut bit for bit only by its own engine).

The store is $CHIRP_PIN_STORE, else ~/.local/state/chirp-eco/pins. A stored pin is found by file name
(chirp-<commit>) and checked against the sha256 written when it was kept. A pin never changes: keeping a different
binary under a stored name is refused, and the stored one stays.
"""
import hashlib
import os
import shutil
import sys


def store_dir():
    state = os.environ.get("XDG_STATE_HOME") or os.path.expanduser("~/.local/state")
    return os.environ.get("CHIRP_PIN_STORE") or os.path.join(state, "chirp-eco", "pins")


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def recorded(stored):
    try:
        with open(stored + ".sha256") as f:
            return f.read().split()[0]
    except (OSError, IndexError):
        return None


def put(src, dst, mode=0o555):
    """Copy src to dst through a temporary name in dst's directory, so dst is never half a file."""
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    tmp = f"{dst}.part-{os.getpid()}"
    shutil.copyfile(src, tmp)
    os.chmod(tmp, mode)
    os.replace(tmp, dst)


def keep(pin, store=None):
    """-> (ok, message). Copies PIN into the store unless it is already there."""
    store = store or store_dir()
    name = os.path.basename(pin)
    if not os.path.isfile(pin):
        return False, f"{name}: no such pin at {pin}"
    stored = os.path.join(store, name)
    digest = sha(pin)
    if os.path.isfile(stored):
        have = recorded(stored) or sha(stored)
        if have != digest:
            return False, f"{name}: differs from the stored copy ({digest[:12]} against {have[:12]}); the stored one stays"
        if not recorded(stored):
            with open(stored + ".sha256", "w") as f:
                f.write(digest + "\n")
        return True, f"{name}: already stored"
    put(pin, stored)
    with open(stored + ".sha256", "w") as f:
        f.write(digest + "\n")
    return True, f"{name}: stored ({digest[:12]})"


def restore(pin, store=None):
    """-> (ok, message). ok means PIN is there and executable afterwards."""
    store = store or store_dir()
    name = os.path.basename(pin)
    if os.path.isfile(pin) and os.access(pin, os.X_OK):
        return True, f"{name}: present"
    stored = os.path.join(store, name)
    if not os.path.isfile(stored):
        return False, f"{name}: missing, and no stored copy in {store}"
    want = recorded(stored)
    if want and sha(stored) != want:
        return False, f"{name}: missing, and the stored copy no longer matches its sha256; not restored"
    put(stored, pin)
    return True, f"{name}: restored to {pin} from {store}" + ("" if want else " (no sha256 was recorded for it)")


def seal(store=None):
    store = store or store_dir()
    out = []
    for name in sorted(os.listdir(store)) if os.path.isdir(store) else []:
        stored = os.path.join(store, name)
        if name.endswith(".sha256") or ".part-" in name or not os.path.isfile(stored) or recorded(stored):
            continue
        digest = sha(stored)
        with open(stored + ".sha256", "w") as f:
            f.write(digest + "\n")
        out.append(f"{name}: sealed ({digest[:12]})")
    return out


def listing(store=None):
    store = store or store_dir()
    out = []
    for name in sorted(os.listdir(store)) if os.path.isdir(store) else []:
        stored = os.path.join(store, name)
        if name.endswith(".sha256") or ".part-" in name or not os.path.isfile(stored):
            continue
        want = recorded(stored)
        state = "no sha256" if not want else ("ok" if sha(stored) == want else "DOES NOT MATCH its sha256")
        out.append(f"{name}  {os.path.getsize(stored) / 1e6:.1f} MB  {state}")
    return out


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__.strip())
        return 0 if len(argv) > 1 else 2
    cmd, args = argv[1], argv[2:]
    if cmd == "keep" and args:
        results = [keep(p) for p in args]
        for _, msg in results:
            print("pinstore:", msg)
        return 0 if all(ok for ok, _ in results) else 1
    if cmd == "restore" and len(args) == 1:
        ok, msg = restore(args[0])
        print("pinstore:", msg)
        return 0 if ok else 1
    if cmd == "seal" and not args:
        for line in seal():
            print("pinstore:", line)
        return 0
    if cmd == "list" and not args:
        lines = listing()
        print("\n".join(lines) if lines else f"(nothing stored in {store_dir()})")
        return 1 if any("DOES NOT MATCH" in line for line in lines) else 0
    print(__doc__.strip(), file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
