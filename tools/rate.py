#!/usr/bin/env python3
"""rate: Harry's (and agents') ratings and notes for composed songs (composition mode, compose/README.md).

  rate.py ID SCORE [--note TEXT] [--who NAME]     a 0-10 rating (decimals fine) of the song's current version
  rate.py now SCORE [--note TEXT]                 rate whatever the groove is playing right now
  rate.py note ID TEXT                            a note without a rating
  rate.py list [ID | ALBUM_ID]                    the ratings and notes so far

Ratings go to compose/ALBUM/ratings.jsonl (committed), stamped with the song's current best version. compscore's
`human` term is Harry's latest rating x10 (an older version's counts half); its `peer` term is other agents' latest
ratings (never the song's own composer's). WHO defaults to harry from a plain shell and to the agent's climb name
inside an agent session (PI_SESSION_ID / CLIMB_AS), so agent ratings never count as Harry's. Climbers see the latest
ratings and notes in `climb.py next`.
"""
import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(HERE)
sys.path.insert(0, HERE)
import chirpers as CH  # noqa: E402

C = CH.C


def default_who(argv):
    if os.environ.get("PI_SESSION_ID") or os.environ.get("CLIMB_AS") or "--as" in argv:
        return C.whoami(argv)
    return "harry"


def resolve_now(status, ids):
    """The climb id a live status is playing: its label when that is a climb, else the playlist's current entry.
    Raises SystemExit with a usable message otherwise (after a groove restart the first song plays unlabelled: its
    label is its opening notes, e.g. 'F2,C3/1+1+…')."""
    label = status.get("label")
    if label in ids:
        return label
    pl = status.get("playlist") or {}
    cur, entries = pl.get("current"), pl.get("entries") or []
    if isinstance(cur, int) and 0 <= cur < len(entries):
        cur = entries[cur]
    if isinstance(cur, dict) and cur.get("label") in ids:
        return cur["label"]
    raise SystemExit(f"rate: the groove is playing {str(label)[:40]!r}, which is not a climb (after a restart the first "
                     f"song plays unlabelled until the playlist takes over); rate it by id: rate.py ID SCORE")


def playing_now():
    """The climb id the groove is playing, or None when the groove is unreachable."""
    groove = os.path.join(os.environ.get("XDG_RUNTIME_DIR", f"/run/user/{os.getuid()}"), "chirp-groove")
    try:
        r = subprocess.run([groove, "--json", "live", "status"], capture_output=True, text=True, timeout=10)
        status = json.loads(r.stdout).get("data") or {}
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return None
    return resolve_now(status, {c["id"] for c in C.load()["climbs"]})


def ratings_path(album_id):
    return os.path.join(ROOT, "compose", album_id, "ratings.jsonl")


def record(cid, score, note, who, argv):
    reg = C.load()
    c = C.find(reg, cid)
    if c.get("mode") != "compose":
        raise SystemExit(f"rate: {cid} is not a composition (only composed songs are rated)")
    if score is not None and not 0 <= score <= 10:
        raise SystemExit("rate: SCORE is 0-10")
    e = {"id": cid, "who": who, "at": C.now_iso(), "version": (c.get("best") or {}).get("version")}
    if score is not None:
        e["score"] = score
    if note:
        e["note"] = note
    p = ratings_path(c["album"])
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "a") as f:
        f.write(json.dumps(e, ensure_ascii=False) + "\n")
    paths = [os.path.relpath(p, ROOT)]
    if score is not None and who != c.get("owner") and (c.get("best") or {}).get("score") is not None:
        # A rating moves compscore's total (human .30, peer .05) but not the stored best, so `done` would compare a
        # new round against a pre-rating number (chirper-three: Hail on a Music Box v3 98.15 -> 92.50 like for like
        # after Harry's 8.0, and v4 92.58 logged as not kept, 29 Oct). Mark the best stale until it is re-measured.
        with C.registry() as reg2:
            b = C.find(reg2, cid).get("best") or {}
            if b.get("score") is not None:
                b["stale"] = {**b.get("stale", {"score": b["score"]}), "since": e["at"], "who": who, "rating": score,
                              "version": e["version"]}
        paths.append("climbs.json")
    what = f"{score}/10" if score is not None else "note"
    C.commit_or_die(paths, f"compose: {who} rates {cid} {what}"
                    + (f": {note[:60]}" if note else ""), argv)
    return e


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    clean, skip = [], False
    for x in argv:
        if skip:
            skip = False
            continue
        if x == "--as":
            skip = True
            continue
        if x != "--no-git":
            clean.append(x)
    if clean and clean[0] == "list":
        target = clean[1] if len(clean) > 1 else None
        reg = C.load()
        albums = sorted({c["album"] for c in reg["climbs"] if c.get("mode") == "compose"})
        for aid in albums:
            p = ratings_path(aid)
            if not os.path.exists(p):
                continue
            with open(p) as f:
                for ln in f:
                    r = json.loads(ln)
                    if target in (None, aid, r["id"]):
                        print(f"{r['at'][:16]} {r['id']:14s} {r['who']:12s} {r.get('version') or '-':5s} "
                              f"{r.get('score', '  ')!s:>4} {r.get('note', '')}")
        return
    if clean and clean[0] == "note":
        if len(clean) < 3:
            raise SystemExit("rate.py note ID TEXT")
        e = record(clean[1], None, " ".join(clean[2:]), default_who(argv), argv)
        print(f"{e['id']}: note recorded ({e['who']})")
        return
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("id", help="a climb id, or 'now' for the track the groove is playing")
    ap.add_argument("score", type=float)
    ap.add_argument("--note")
    ap.add_argument("--who")
    a = ap.parse_args(clean)
    cid = playing_now() if a.id == "now" else a.id
    if not cid:
        raise SystemExit("rate: nothing is playing (or the groove is unreachable)")
    e = record(cid, a.score, a.note, a.who or default_who(argv), argv)
    print(f"{e['id']} ({e.get('version') or 'no version yet'}): {e['score']}/10 by {e['who']}"
          + (f" — {e['note']}" if e.get("note") else ""))


if __name__ == "__main__":
    main()
