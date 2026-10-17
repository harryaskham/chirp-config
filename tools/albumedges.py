#!/usr/bin/env python3
"""Album edges: how a song's first and last seconds meet its neighbours' — the transitions an album
plays without a gap — measured cheaply from each song's own render (never a whole-album render).

  albumedges.py check ID RENDER.wav [--edge S]   this render's edges against the record's, and the
                                                 transitions to its neighbours (their recorded edges,
                                                 else the record's)
  albumedges.py record ID RENDER.wav [--version vN]
                                                 keep this render's edges in climbs/edges/ID.json
                                                 (`climb.py done … --render RENDER.wav` does it for a
                                                 kept album version)
  albumedges.py score [ALBUM] [--json]           every transition of an album: the record's jump,
                                                 ours, the error, and the album's edge score

An edge is the first or last EDGE seconds (default 3): overall level and six band levels (RMS dB).
The record's are read from ref/ID.wav. A render's tail ends at the record's length (climbs are timed
to the record; anything after is the tail that rings into the next song). A transition's jump is
head(k+1) − tail(k); its error is the mean distance between our jump and the record's (dB, over the
level and the bands), scored 100·exp(−err/6). A song's own edge error (its head and tail against
the record's) says which side of a transition to fix: level-match it in the song (master ride or
section levels at the start and end), not with a fade the record does not have."""
import json
import math
import os
import sys
from datetime import datetime, timezone

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(HERE)
sys.path.insert(0, HERE)
from likeness import SR, load  # noqa: E402

EDGES = os.path.join(ROOT, "climbs", "edges")
BANDS = [(20, 120), (120, 400), (400, 1200), (1200, 3500), (3500, 8000), (8000, 20000)]
NAMES = ["level", "sub-120", "120-400", "400-1k2", "1k2-3k5", "3k5-8k", "8k+"]


def db(x):
    return float(10 * math.log10(max(x, 1e-12)))


def stats(seg):
    """Level and band levels (dB) of a stereo segment."""
    x = seg.mean(axis=1)
    out = {"level": db(float(np.mean(x * x)))}
    spec = np.abs(np.fft.rfft(x * np.hanning(len(x)))) ** 2
    f = np.fft.rfftfreq(len(x), 1 / SR)
    tot = spec.sum() + 1e-20
    p = float(np.mean(x * x))
    for (a, b), name in zip(BANDS, NAMES[1:]):
        out[name] = db(p * spec[(f >= a) & (f < b)].sum() / tot)
    return out


def edges(stereo, end=None, edge=3.0):
    """Head and tail stats; the tail ends at `end` seconds (default: the audio's end)."""
    n = len(stereo)
    stop = min(n, int(round(end * SR))) if end else n
    k = max(1, int(edge * SR))
    return {"head": stats(stereo[: min(k, stop)]), "tail": stats(stereo[max(0, stop - k): stop])}


def vec(e):
    return np.array([e[name] for name in NAMES])


def ref_edges(cid, edge):
    ref = load(os.path.join(ROOT, "ref", f"{cid}.wav"))
    return edges(ref, None, edge), len(ref) / SR


def render_edges(cid, path, edge):
    ref, ref_len = ref_edges(cid, edge)
    ours = edges(load(path), ref_len, edge)
    return ours, ref, ref_len


def registry():
    with open(os.path.join(ROOT, "climbs.json")) as f:
        return json.load(f)


def album_of(c):
    return (c.get("meta") or {}).get("album")


def neighbours(cid):
    """(previous, next) climbs on the same album, by track."""
    cs = registry()["climbs"]
    me = next((c for c in cs if c["id"] == cid), None)
    if not me or not album_of(me):
        return None, None, None
    album = sorted([c for c in cs if album_of(c) == album_of(me)], key=lambda c: c["meta"].get("track") or 999)
    i = [c["id"] for c in album].index(cid)
    return me, (album[i - 1] if i > 0 else None), (album[i + 1] if i + 1 < len(album) else None)


def recorded(cid):
    try:
        with open(os.path.join(EDGES, f"{cid}.json")) as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def err(jump_ours, jump_ref):
    e = float(np.mean(np.abs(jump_ours - jump_ref)))
    return e, 100 * math.exp(-e / 6)


def fmt(v):
    return " ".join(f"{x:+5.1f}" for x in v)


def opt(a, k, d=None):
    return a[a.index(k) + 1] if k in a and a.index(k) + 1 < len(a) else d


def cmd_check(a):
    cid, path = a[0], a[1]
    edge = float(opt(a, "--edge", 3))
    ours, ref, _ = render_edges(cid, path, edge)
    print(f"{cid}: edges of {path} against the record ({edge:g} s; dB: {' '.join(NAMES)})")
    for side in ("head", "tail"):
        d = vec(ours[side]) - vec(ref[side])
        print(f"  {side} ours − record: {fmt(d)}   (mean |Δ| {np.mean(np.abs(d)):.1f} dB)")
    _, prev, nxt = neighbours(cid)
    for other, mine, theirs, label in ((prev, "head", "tail", "from"), (nxt, "tail", "head", "into")):
        if not other:
            continue
        rec = recorded(other["id"])
        o_ours = rec["edges"][theirs] if rec else None
        o_ref = (rec or {}).get("ref", {}).get(theirs) or ref_edges(other["id"], edge)[0][theirs]
        basis = f"its kept {rec['version']}" if rec else "its record (no kept render yet)"
        o_ours = o_ours or o_ref
        if label == "from":
            jo, jr = vec(ours["head"]) - vec(o_ours), vec(ref["head"]) - vec(o_ref)
        else:
            jo, jr = vec(o_ours) - vec(ours["tail"]), vec(o_ref) - vec(ref["tail"])
        e, sc = err(jo, jr)
        print(f"  transition {label} {other['id']} ({basis}): record jump {fmt(jr)}")
        print(f"  {' ' * (len(label) + len(other['id']) + len(basis) + 16)}our jump    {fmt(jo)}   error {e:.1f} dB, score {sc:.1f}")


def cmd_record(a, version=None):
    cid, path = a[0], a[1]
    edge = float(opt(a, "--edge", 3))
    ours, ref, ref_len = render_edges(cid, path, edge)
    os.makedirs(EDGES, exist_ok=True)
    doc = {"id": cid, "version": version or opt(a, "--version"), "edge": edge, "ref_seconds": round(ref_len, 3),
           "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "edges": ours, "ref": ref}
    out = os.path.join(EDGES, f"{cid}.json")
    with open(out, "w") as f:
        json.dump(doc, f, indent=1)
        f.write("\n")
    print(f"recorded {os.path.relpath(out, ROOT)}")
    return os.path.relpath(out, ROOT)


def cmd_score(a):
    reg = registry()["climbs"]
    albums = sorted({album_of(c) for c in reg if album_of(c)})
    name = next((x for x in a if not x.startswith("--")), None) or (registry().get("focus") or (albums[0] if albums else None))
    if not name:
        sys.exit("no albums")
    album = sorted([c for c in reg if album_of(c) == name], key=lambda c: c["meta"].get("track") or 999)
    rows = []
    for x, y in zip(album, album[1:]):
        rx, ry = recorded(x["id"]), recorded(y["id"])
        row = {"from": x["id"], "to": y["id"]}
        if rx and ry:
            jr = vec(ry["ref"]["head"]) - vec(rx["ref"]["tail"])
            jo = vec(ry["edges"]["head"]) - vec(rx["edges"]["tail"])
            e, sc = err(jo, jr)
            row |= {"record_jump": round(float(jr[0]), 1), "our_jump": round(float(jo[0]), 1),
                    "error_db": round(e, 2), "score": round(sc, 1)}
        else:
            row["missing"] = [c["id"] for c, r in ((x, rx), (y, ry)) if not r]
        rows.append(row)
    scored = [r["score"] for r in rows if "score" in r]
    total = round(float(np.mean(scored)), 1) if scored else None
    if "--json" in a:
        print(json.dumps({"album": name, "score": total, "transitions": rows}))
        return
    print(f"{name}: album edge score {total if total is not None else '—'} ({len(scored)}/{len(rows)} transitions measured)")
    for r in rows:
        if "score" in r:
            print(f"  {r['from']:>26} → {r['to']:<26} level jump record {r['record_jump']:+5.1f} ours {r['our_jump']:+5.1f}"
                  f"  error {r['error_db']:4.1f} dB  score {r['score']:5.1f}")
        else:
            print(f"  {r['from']:>26} → {r['to']:<26} (no kept render edges yet: {', '.join(r['missing'])})")


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help", "help"):
        print(__doc__)
        return
    cmd, rest = a[0], a[1:]
    if cmd == "check" and len(rest) >= 2:
        return cmd_check(rest)
    if cmd == "record" and len(rest) >= 2:
        return cmd_record(rest)
    if cmd == "score":
        return cmd_score(rest)
    sys.exit(__doc__)


if __name__ == "__main__":
    main()
