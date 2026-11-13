#!/usr/bin/env python3
"""lanes: a song's `auto` lanes, and which of their FALLS are not the line they were drawn as (chirp-eco, 13 Nov;
chirper-zero measured it on Common Time v24 and read it in the engine: plan.rs, points_at).

An `auto` lane is an envelope. Between two points a RISE is a straight line, but a FALL takes the envelope's `curve`
(default 3: exponential), so a fade-out, a duck or a sweep down written as two points is a quick drop and a plateau:
with the default, half the fall is done in the first 21% of the time and 82% by the middle. `"curve": 0` in the lane's
dict makes falls the line as written. Common Time's ending was drawn as a straight fade and played as a drop within two
bars.

  lanes.py ID [--all] [--pin BIN] [--json]
  lanes.py --song FILE ...                          (any song file; default songs/ID.yaml)

Reads the lanes from `chirp plan` (tracks at any depth, buses, the master) and prints each with what it drives, its
points, its rises and falls and its curve; then every fall of a lane whose curve is not 0: where, from what to what,
over how long, and where half of it is done. --all lists the falls of straight lanes too. Nothing is rendered; whether
a fall should be a line is the composer's call (a tape stop wants its curve). Read-only.
"""
import argparse
import json
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DEFAULT_CURVE = 3.0


def shape(x, k):
    """The engine's dsp::curve: how much of a fall is done at fraction x of its time."""
    return x if abs(k) < 1e-3 else (1 - math.exp(-k * x)) / (1 - math.exp(-k))


def half_point(k):
    """The fraction of a fall's time at which half of it is done."""
    return 0.5 if abs(k) < 1e-3 else -math.log(1 - 0.5 * (1 - math.exp(-k))) / k


def beats(tok, tempo):
    """A lane point's position in beats ("12b", "30s"), or None in another form."""
    tok = str(tok).strip()
    try:
        if tok.endswith("b"):
            return float(tok[:-1])
        if tok.endswith("s") and tempo:
            return float(tok[:-1]) * tempo / 60.0
    except ValueError:
        pass
    return None


def drives(owner, name):
    """The parameters of this track, bus or master that follow auto.NAME, as paths."""
    out = []

    def walk(o, path):
        if isinstance(o, dict):
            if any(isinstance(m, dict) and m.get("src") == f"auto.{name}" for m in o.get("mod") or []):
                out.append(path)
            for k, v in o.items():
                if k not in ("auto", "notes", "tracks", "mod"):
                    walk(v, f"{path}.{k}" if path else k)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, f"{path}.{o[i].get('type', i) if isinstance(o[i], dict) else i}")
    walk(owner, "")
    return out


def lanes_of(canon):
    """[{where, name, drives, curve, points, falls}] for every lane of the song."""
    tempo = canon.get("tempo", 120.0)          # the plan leaves out a tempo of 120, the engine's default
    tempo = tempo if isinstance(tempo, (int, float)) and tempo > 0 else None
    patches = canon.get("patches") if isinstance(canon.get("patches"), dict) else {}
    out = []

    def add(where, owner):
        for name, lane in (owner.get("auto") or {}).items():
            if not isinstance(lane, dict):
                continue
            pts = [p for p in lane.get("points") or [] if isinstance(p, (list, tuple)) and len(p) == 2]
            curve = float(lane.get("curve", DEFAULT_CURVE))
            dr = drives(owner, name)
            patch = str(owner.get("patch", "")).split(" ")[0]
            if not dr and isinstance(patches.get(patch), dict):
                dr = [f"patch {patch}: {p}" for p in drives(patches[patch], name)]
            falls = []
            for (t0, v0), (t1, v1) in zip(pts, pts[1:]):
                if isinstance(v0, (int, float)) and isinstance(v1, (int, float)) and v1 < v0:
                    b0, b1 = beats(t0, tempo), beats(t1, tempo)
                    falls.append({"from": t0, "to": t1, "v0": v0, "v1": v1, "beat": b0,
                                  "beats": None if b0 is None or b1 is None else round(b1 - b0, 3),
                                  "seconds": None if b0 is None or not tempo else round(b0 * 60.0 / tempo, 1)})
            out.append({"where": where, "name": name, "drives": dr, "curve": curve, "explicit": "curve" in lane, "points": len(pts),
                        "rises": sum(1 for (_, a), (_, b) in zip(pts, pts[1:])
                                     if isinstance(a, (int, float)) and isinstance(b, (int, float)) and b > a),
                        "falls": falls})

    def tracks(ts):
        for t in ts or []:
            if isinstance(t, dict):
                add(f"track {t.get('name')}", t)
                tracks(t.get("tracks"))

    tracks(canon.get("tracks"))
    buses = canon.get("buses")
    for name, b in (buses.items() if isinstance(buses, dict) else []):
        if isinstance(b, dict):
            add(f"bus {name}", b)
    if isinstance(canon.get("master"), dict):
        add("master", canon["master"])
    return out


def clock(sec):
    return f"{int(sec // 60)}:{sec % 60:04.1f}"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("id", nargs="?")
    ap.add_argument("--song")
    ap.add_argument("--all", action="store_true", help="list the falls of straight (curve 0) lanes too")
    ap.add_argument("--pin")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    song = a.song or (os.path.join(ROOT, "songs", f"{a.id}.yaml") if a.id else None)
    if not song or not os.path.exists(song):
        raise SystemExit("lanes: give a climb ID (songs/ID.yaml) or --song FILE")
    pin = a.pin or open(os.path.join(HERE, "groove-pin")).read().strip()
    env = dict(os.environ)
    env.pop("LD_LIBRARY_PATH", None)
    r = subprocess.run([pin, "plan", "-f", song, "--json"], capture_output=True, text=True, env=env)
    try:
        d = json.loads(r.stdout)
        canon = (d.get("data") or d).get("canonical") or {}
    except ValueError:
        raise SystemExit(f"lanes: chirp plan failed: {r.stderr.strip()[-300:]}")
    rows = lanes_of(canon)
    if a.json:
        print(json.dumps({"song": song, "default_curve": DEFAULT_CURVE, "lanes": rows}))
        return
    bent = [r for r in rows if r["falls"] and abs(r["curve"]) >= 1e-3]
    print(f"{os.path.basename(song)}: {len(rows)} auto lanes; {len(bent)} have falls that are not lines"
          f" ({sum(len(r['falls']) for r in bent)} falls)")
    print(f"  {'where':14s} {'lane':10s} {'points':>6s} {'rises':>5s} {'falls':>5s}  {'curve':9s} drives")
    for r in rows:
        cur = "0 (line)" if abs(r["curve"]) < 1e-3 else f"{r['curve']:g}" + ("" if r["explicit"] else " (dflt)")
        print(f"  {r['where'][:14]:14s} {r['name'][:10]:10s} {r['points']:6d} {r['rises']:5d} {len(r['falls']):5d}  {cur:9s} "
              + (", ".join(r["drives"]) or "?"))
    for r in rows:
        if not r["falls"] or (abs(r["curve"]) < 1e-3 and not a.all):
            continue
        half = half_point(r["curve"])
        print(f"  {r['where']}, {r['name']}" + (f" -> {', '.join(r['drives'])}" if r["drives"] else "")
              + (f": curve {r['curve']:g}, half of each fall is done in its first {half * 100:.0f}%,"
                 f" {shape(0.5, r['curve']) * 100:.0f}% by its middle" if abs(r["curve"]) >= 1e-3 else ": curve 0, lines"))
        for f in r["falls"]:
            at = f"{clock(f['seconds']):>7s}  bar {int(f['beat'] // 4) + 1:<4d}" if f["seconds"] is not None and f["beat"] is not None \
                else f"{str(f['from']):>7s}"
            over = f"over {f['beats']:g} beats" if f["beats"] is not None else f"to {f['to']}"
            print(f"      {at}  {f['v0']:g} -> {f['v1']:g}  {over}")
    if bent:
        print('  A fall meant as a line needs "curve": 0 in its lane (it changes every fall of that lane; rises are lines'
              " either way). Bars are counted in four.")


if __name__ == "__main__":
    sys.exit(main())
