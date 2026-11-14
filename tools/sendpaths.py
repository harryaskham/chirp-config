#!/usr/bin/env python3
"""sendpaths: sends that go ROUND a clip or a limiter (chirper-zero's finding, Common Time v41; the check he asked for).

  sendpaths.py SONG [SONG ...] [--over -10] [--soft] [--measure FROM-TO] [--pin CHIRP] [--json]

A track whose bus has a `clip` or a `limiter`, and which also SENDS to a bus that does not pass through it, has a
path round the clip. Its peaks reach the mix by the send, its level lives in the send, and its fader mostly drives
the clip. Common Time's snare stood so from v10 to v40: on a drums bus clipped at -13 dB and sent at -1.5 dB to the
cymbals' room, which is not clipped. Alone, its peak was 6.3 dB higher with the send than without and half its
loudness came through a bright 0.7 s room; a transient shaper on the track changed nothing.
From the plan alone (`chirp plan`), for each SONG (an id, or a file): every send of a track whose own way out (its
bus, that bus's bus, a parent track's strip) holds a clip or a limiter, to a bus that does not lead back through it,
with the send's level. Sends over --over dB (default -10) are marked LOUD: those are the ones to look at. A room
that cymbals are meant to live in will be listed too; whether a path is a fault is for the ear and --measure.
--soft counts compressors and their kin (compressor, glue, ott, autolevel) as well as clip and limiter.
--measure FROM-TO (positions as `chirp render` takes them: 41-49) is the tell: each LOUD track is rendered alone with
the send and without it, and the peak and loudness of each are printed with the difference. A few seconds a track.
What it cannot see: a send whose level is modulated is read at its written value; an `input` track; what a bus's
own sends do. Exit status 0 always: it reports, it does not judge. Read-only. Tests: tools/tests/test_sendpaths.py.
"""
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(HERE)
sys.path.insert(0, HERE)
import chirpbin  # noqa: E402

HARD = ("clip", "limiter")
SOFT = ("compressor", "glue", "ott", "autolevel")


def fx_type(fx):
    if isinstance(fx, str):
        return fx.split()[0] if fx.split() else ""
    return str((fx or {}).get("type") or "")


def decibels(g):
    """A send's level in dB: "-1.5dB", a bare number (a linear factor), or {"value": ...} (read at its written value)."""
    if isinstance(g, dict):
        return decibels(g.get("value", 1.0))
    if isinstance(g, (int, float)) and not isinstance(g, bool):
        return 20 * math.log10(g) if g > 0 else -200.0
    s = str(g).strip().lower()
    if s.endswith("db"):
        return float(s[:-2])
    v = float(s)
    return 20 * math.log10(v) if v > 0 else -200.0


def limits(fxs, kinds):
    return [t for t in (fx_type(f) for f in fxs or []) if t in kinds]


def bus_chain(buses, name):
    """The buses a signal passes on its way out from bus `name`: itself, its `out`, that bus's `out` ..."""
    seen = []
    while name and name in buses and name not in seen:
        seen.append(name)
        name = (buses[name] or {}).get("out")
    return seen


def paths(canon, over=-10.0, soft=False):
    """[{track, out, by (the limiting effects), where (the bus or strip that holds them), send, db, loud}] for every
    send of a track that goes round a clip or limiter on the track's own way out."""
    kinds = HARD + (SOFT if soft else ())
    buses = canon.get("buses") or {}
    if isinstance(buses, list):
        buses = {b.get("name"): b for b in buses if isinstance(b, dict)}
    found = []

    def walk(tracks, parents):
        for t in tracks or []:
            if not isinstance(t, dict):
                continue
            # what limits this track on its way out: a parent's strip, then its bus and the buses after it
            limited = [(f"track {p.get('name')}", limits(p.get("fx"), kinds)) for p in parents]
            out = t.get("out") or next((p.get("out") for p in reversed(parents) if p.get("out")), None)
            limited += [(b, limits((buses[b] or {}).get("fx"), kinds)) for b in bus_chain(buses, out)]
            limited = [(w, k) for w, k in limited if k]
            through = {w for w, _ in limited}
            for send, gain in (t.get("sends") or {}).items():
                if not limited or through & set(bus_chain(buses, send)):
                    continue                                   # nothing to go round, or the send leads back through it
                try:
                    db = decibels(gain)
                except (TypeError, ValueError):
                    db = float("nan")
                found.append({"track": t.get("name"), "out": out, "where": limited[0][0], "by": limited[0][1], "send": send,
                              "db": round(db, 1), "loud": bool(db > over), "moves": isinstance(gain, dict)})
            walk(t.get("tracks"), parents + [t])
    walk(canon.get("tracks"), [])
    return found


def plan(pin, song):
    r = subprocess.run([pin, "plan", "-f", song, "--json"], capture_output=True, text=True, cwd=ROOT,
                       env={k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"})
    try:
        d = json.loads(r.stdout)
    except ValueError:
        raise SystemExit(f"sendpaths: {os.path.basename(song)} does not plan: {(r.stderr or r.stdout).strip()[-300:]}") from None
    return (d.get("data") or d).get("canonical") or {}


def without_send(doc, track, send):
    """A copy of the song with that one send taken off the track; None when the track or the send is not in it."""
    out = json.loads(json.dumps(doc))

    def walk(ts):
        for t in ts or []:
            if isinstance(t, dict):
                if t.get("name") == track and send in (t.get("sends") or {}):
                    del t["sends"][send]
                    return True
                if walk(t.get("tracks")):
                    return True
        return False
    return out if walk(out.get("tracks")) else None


def read(path):
    with wave.open(path) as w:
        sr, ch, sw = w.getframerate(), w.getnchannels(), w.getsampwidth()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype={2: np.int16, 4: np.int32}[sw]).reshape(-1, ch).astype(float)
    return x / float(1 << (8 * sw - 1)), sr


def level(x, sr):
    """(peak dBFS, loudness LUFS) of a render; (None, None) when it is silent."""
    import levels
    peak = float(np.abs(x).max()) if len(x) else 0.0
    if peak <= 1e-6:
        return None, None
    return 20 * math.log10(peak), float(levels.loudness(x, sr)[0])


def measure(doc, found, window, pin, where):
    """For each LOUD path: the track alone with the send and without it. Adds "with" and "without" (peak, LUFS)."""
    lo, _, hi = window.partition("-")
    base = os.path.join(where, "with.json")
    with open(base, "w") as f:
        json.dump(doc, f)
    env = {k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"}

    def solo(song, track, out):
        r = subprocess.run(["nice", "-n", "12", pin, "render", "-f", song, "--seed", "0", "--set", "loudness=null", "--threads", "2",
                            "--solo", track, "--from", lo, "--to", hi, "-o", out], capture_output=True, text=True, cwd=ROOT, env=env)
        if r.returncode:
            raise SystemExit("sendpaths: the track did not render: " + (r.stderr or r.stdout).strip()[-300:])
        return level(*read(out))
    cache = {}
    for p in found:
        if not p["loud"]:
            continue
        cut = without_send(doc, p["track"], p["send"])
        if cut is None:
            p["with"] = p["without"] = None                    # a track the plan made (a `double`): not in the file by that name
            continue
        if p["track"] not in cache:
            cache[p["track"]] = solo(base, p["track"], os.path.join(where, "with.wav"))
        other = os.path.join(where, "without.json")
        with open(other, "w") as f:
            json.dump(cut, f)
        p["with"], p["without"] = cache[p["track"]], solo(other, p["track"], os.path.join(where, "without.wav"))
    return found


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    opt = {"--over": "-10", "--measure": None, "--pin": None}
    for k in list(opt):
        if k in a and a.index(k) + 1 < len(a):
            i = a.index(k)
            opt[k] = a[i + 1]
            del a[i:i + 2]
    flags = {k: k in a for k in ("--soft", "--json")}
    a = [x for x in a if x not in flags]
    if not a or "-h" in a or "--help" in a:
        print(__doc__)
        return 0 if ("-h" in a or "--help" in a) else 2
    pin = opt["--pin"] or chirpbin.resolve()
    over = float(opt["--over"])
    report = []
    for song in a:
        path = song if os.path.exists(song) else os.path.join(ROOT, "songs", song + ".yaml")
        if not os.path.exists(path):
            raise SystemExit(f"sendpaths: no song {song}")
        found = paths(plan(pin, path), over, flags["--soft"])
        if opt["--measure"] and any(p["loud"] for p in found):
            import songfmt
            where = tempfile.mkdtemp(prefix="sendpaths-")
            try:
                measure(songfmt.load(path), found, opt["--measure"], pin, where)
            finally:
                shutil.rmtree(where, True)
        report.append({"song": os.path.basename(path), "paths": found})
    if flags["--json"]:
        print(json.dumps(report))
        return 0
    what = "a clip, a limiter or a compressor" if flags["--soft"] else "a clip or a limiter"
    for r in report:
        found = r["paths"]
        loud = sum(p["loud"] for p in found)
        if not found:
            print(f"{r['song']}: no send goes round {what}")
            continue
        print(f"{r['song']}: {len(found)} send{'s' if len(found) != 1 else ''} go{'es' if len(found) == 1 else ''} round {what}, "
              f"{loud} over {over:g} dB")
        print(f"  {'track':14s} {'held by':26s} {'sent to':10s} {'level':>9s}")
        for p in found:
            held = f"{p['where']} ({', '.join(p['by'])})"
            line = (f"  {str(p['track']):14s} {held:26s} {p['send']:10s} {p['db']:+7.1f} dB{' *' if p['moves'] else '  '}"
                    f"{'  LOUD' if p['loud'] else ''}")
            if p.get("with") is not None or p.get("without") is not None:
                (pw, lw), (po, lo) = p["with"], p["without"]
                if pw is None:
                    line += "   silent in the window"
                elif po is None:
                    line += f"   alone: peak {pw:+.1f} dBFS with the send, silent without it"
                else:
                    line += f"   alone: peak {pw:+.1f} with, {po:+.1f} without ({pw - po:+.1f} dB); loudness {lw - lo:+.1f} LU with"
            elif "with" in p:
                line += "   (a track the plan makes: not measured)"
            print(line)
        if any(p["moves"] for p in found):
            print("  * the level is modulated: read at its written value")
    return 0


if __name__ == "__main__":
    sys.exit(main())
