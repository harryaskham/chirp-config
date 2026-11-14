#!/usr/bin/env python3
"""holds: a song's long notes, and whether each dies away or sits flat until it stops (chirp-eco, 13 Nov; chirper-zero
found it twice on Common Time, at v9 for the slow chords and at v23 for the last chord, fourteen versions late).

A held note through a saturated amp has no decay: the string dies but the amp's output does not, until the string is
30-40 dB down. A chord written to ring out sits flat for its whole length and then cuts. On the bench an 8 s chord
falls 1-2 dB through ct-chug, ct-wall or m8, and 37 dB through the low-gain ct-crunch. A ring-out through a high-gain
rig is a fader move after the amp (an `auto` lane on the bus), not a property of the note.

  holds.py ID [--min 8] [--tracks REGEX] [--flat 3] [--all] [--seed 0] [-j 3] [--pin BIN] [--json]
  holds.py --song FILE ...                          (any song file; default songs/ID.yaml)

Reads the notes from `chirp plan` and takes every one of --min beats or longer (default 8: two bars of four; the notes
of a chord count as one hold). Renders each track that has one solo, unmastered, through its bus and the master, so
a fade on the bus shows; then prints per hold:
  fall    the level at its end against its start (the last quarter of the hold, a second at most, against the first;
          the end is where it stops sounding, since a note is often played shorter than written)
  then    the level just after it stops against its end, or "next" where the track plays on at once
and flags FLAT (fall less than --flat dB, default 6: saturated rigs fall 1-4, a clean or low-gain guitar 30 or more)
and "cut" (20 dB or more gone within half a beat of the end).
Listed: the flat holds with a rest after them, the ones a listener hears stop. A flat hold that runs into the track's
next note is counted ("run on") and not listed: a pad, a drone, a sustained lead. --all lists every hold. The list
says where to look; what should die is the composer's call. Fixed-tempo songs only; a track with a `warp` is read
where its notes sound (tools/warp.py). Read-only.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import likeness as L  # noqa: E402

SILENT = -90.0
CUT = -20.0
SHOWN = 6
FRAME = 0.05


def walk(tracks, out=None):
    """Every track with notes, at any depth."""
    out = [] if out is None else out
    for t in tracks or []:
        if not isinstance(t, dict):
            continue
        if t.get("notes") and t.get("name") and not t.get("mute"):
            out.append(t)
        walk(t.get("tracks"), out)
    return out


def holds_of(track, min_beats, tempo=120.0):
    """[{at, len, pitch, voices, next}] for a track's notes of min_beats or more; a chord's notes are one hold. A track
    with a `warp` is read as it sounds (tools/warp.py; `tempo` matters only for a warp written in seconds)."""
    import warp
    notes = [(float(n.get("at") or 0), float(n.get("len") or 0), str(n.get("pitch", "")))
             for n in warp.moved([n for n in track.get("notes") or [] if isinstance(n, dict)], track.get("warp"), tempo)]
    seen = {}
    for at, ln, pitch in notes:
        if ln < min_beats:
            continue
        h = seen.setdefault((at, ln), {"at": at, "len": ln, "pitch": [], "voices": 0})
        h["pitch"].append(pitch)
        h["voices"] += 1
    out = []
    for (at, ln), h in sorted(seen.items()):
        end = at + ln
        h["pitch"] = ",".join(h["pitch"])
        # the track plays on: another note starts within half a beat of the end, or is still sounding across it
        h["next"] = any((s, n) != (at, ln) and s <= end + 0.5 and s + n > end + 0.01 for s, n, _ in notes)
        out.append(h)
    return out


def db(x):
    return float(10 * np.log10(np.mean(np.square(x)) + 1e-12)) if len(x) else -120.0


def measure(x, sr, start, dur, spb):
    """A hold's fall and what follows it, from the track's solo: x mono, start and dur in seconds, spb seconds a beat.

    A note is often played shorter than written (a hold of 8 bars at nine tenths stops 1.5 s early), so the end is
    where the sound stops: the last 50 ms frame within 40 dB of the start. A note that dies away is read to there.
    """
    a = int(start * sr)
    seg = x[a:int((start + dur) * sr)]
    hop = int(FRAME * sr)
    n = len(seg) // hop
    if n < 8:
        return {"silent": True, "fall": None, "then": None, "sounds": 0.0}
    fr = 10 * np.log10(np.mean(np.square(seg[:n * hop].reshape(n, hop)), axis=1) + 1e-12)
    q = max(1, min(int(1.0 / FRAME), n // 4))                               # a quarter of the hold, a second at most
    first = db(seg[hop:(1 + q) * hop])                                      # past the pick
    if first < SILENT:
        return {"silent": True, "fall": None, "then": None, "sounds": 0.0}
    end = int(np.nonzero(fr > first - 40)[0][-1]) + 1
    e = max(q + 1, end - 2)                                                 # not the release itself
    last = db(seg[max(1, e - q) * hop:e * hop])
    gap = a + end * hop + int(0.1 * sr)
    after = db(x[gap:gap + int(min(0.3, spb / 2) * sr)])
    return {"silent": False, "fall": round(last - first, 1), "then": round(after - last, 1), "sounds": round(end * FRAME, 2)}


def plan(pin, song):
    env = dict(os.environ)
    env.pop("LD_LIBRARY_PATH", None)
    r = subprocess.run([pin, "plan", "-f", song, "--json"], capture_output=True, text=True, env=env)
    if r.returncode:
        raise SystemExit(f"holds: chirp plan failed: {r.stderr.strip()[-300:]}")
    d = json.loads(r.stdout)
    return (d.get("data") or d).get("canonical") or {}


def render(pin, song, out, seed, solo, to):
    """The track solo from the top to `to` beats. From the top on purpose: this is the song's own audio, not an
    approximation, and a late window (--from with --preroll) is not always quicker: an effect that remembers its start
    on the track's bus (a rotary on Common Time's guitars) makes the engine render from the top anyway (bd-e11da9)."""
    cmd = ["nice", "-n", "12", pin, "render", "-f", song, "--seed", str(seed), "--set", "loudness=null", "-o", out,
           "--solo", solo, "--to", f"{to:g}b"]
    env = dict(os.environ, RAYON_NUM_THREADS="2")
    env.pop("LD_LIBRARY_PATH", None)
    r = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if r.returncode:
        raise RuntimeError(f"render failed ({solo}): {r.stderr.strip()[-300:]}")
    return out


def clock(sec):
    return f"{int(sec // 60)}:{sec % 60:04.1f}"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("id", nargs="?")
    ap.add_argument("--song")
    ap.add_argument("--min", type=float, default=8.0, help="beats; a hold is a note this long or longer")
    ap.add_argument("--tracks", help="only tracks whose name matches this regular expression")
    ap.add_argument("--flat", type=float, default=6.0, help="dB; a hold that falls less than this is FLAT")
    ap.add_argument("--all", action="store_true", help="list every hold, not only the flat ones")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("-j", type=int, default=3)
    ap.add_argument("--pin")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    song = a.song or (os.path.join(ROOT, "songs", f"{a.id}.yaml") if a.id else None)
    if not song or not os.path.exists(song):
        raise SystemExit("holds: give a climb ID (songs/ID.yaml) or --song FILE")
    pin = a.pin or open(os.path.join(HERE, "groove-pin")).read().strip()
    canon = plan(pin, song)
    tempo = canon.get("tempo", 120.0)          # the plan leaves out a tempo of 120, the engine's default
    if not isinstance(tempo, (int, float)) or tempo <= 0:
        raise SystemExit("holds: this song's tempo changes; holds.py reads fixed-tempo songs only")
    spb = 60.0 / tempo
    want = re.compile(a.tracks) if a.tracks else None
    jobs = []
    for t in walk(canon.get("tracks")):
        if want and not want.search(t["name"]):
            continue
        hs = holds_of(t, a.min, tempo)
        if hs:
            jobs.append((t, hs))
    work = tempfile.mkdtemp(prefix="holds-", dir="/tmp/lt" if os.path.isdir("/tmp/lt") else None)
    rows = []
    try:
        def one(numbered):
            i, (t, hs) = numbered
            to = max(h["at"] + h["len"] for h in hs) + 2
            wav = render(pin, song, os.path.join(work, f"{i}.wav"), a.seed, t["name"], to)
            x = L.load(wav)
            x = x.mean(axis=1) if x.ndim > 1 else x
            os.remove(wav)
            out = []
            for h in hs:
                m = measure(x, L.SR, h["at"] * spb, h["len"] * spb, spb)
                flat = (not m["silent"]) and m["fall"] > -a.flat
                out.append(dict(h, **m, seconds=round(h["at"] * spb, 1), flat=flat,
                                cut=bool(flat and not h["next"] and m["then"] <= CUT)))
            return {"track": t["name"], "patch": str(t.get("patch", "")), "out": t.get("out"), "holds": out}
        with ThreadPoolExecutor(max(1, a.j)) as ex:
            rows = list(ex.map(one, enumerate(jobs)))
    finally:
        for f in os.listdir(work):
            os.remove(os.path.join(work, f))
        os.rmdir(work)
    if a.json:
        print(json.dumps({"song": song, "tempo": tempo, "min_beats": a.min, "flat_db": a.flat, "tracks": rows}))
        return
    total = sum(len(r["holds"]) for r in rows)
    print(f"{os.path.basename(song)} (seed {a.seed}; each track solo, unmastered, through its bus): {total} notes of "
          f"{a.min:g} beats or more on {len(rows)} tracks")
    print(f"  {'track':10s} {'patch':30s} {'holds':>5s} {'flat':>5s} {'run on':>6s}   bars are counted in four")
    for r in rows:
        hs = r["holds"]
        flat = [h for h in hs if h["flat"]]
        stop = [h for h in flat if not h["next"]]
        print(f"  {r['track']:10s} {r['patch'][:30]:30s} {len(hs):5d} {len(flat):5d} {len(flat) - len(stop):6d}")
        shown = hs if a.all else stop[:SHOWN]
        for h in shown:
            if h["silent"]:
                state = "silent"
            else:
                then = "next" if h["next"] else f"{h['then']:+.0f}"
                state = f"fall {h['fall']:+5.1f} dB  then {then:>4s}  " + ("FLAT" + (", cut" if h["cut"] else "") if h["flat"] else "")
            print(f"      {clock(h['seconds']):>7s}  bar {int(h['at'] // 4) + 1:<4d} {h['len'] / 4:5.1f} bars  {state}")
        if not a.all and len(stop) > SHOWN:
            print(f"      ... and {len(stop) - SHOWN} more (--all, or --tracks '^{re.escape(r['track'])}$' --all)")
    nf = sum(1 for r in rows for h in r["holds"] if h["flat"])
    ns = sum(1 for r in rows for h in r["holds"] if h["flat"] and not h["next"])
    nc = sum(1 for r in rows for h in r["holds"] if h["cut"])
    if nf:
        print(f"  {nf} hold(s) fall less than {a.flat:g} dB from start to end; {ns} have a rest after them, and {nc} of those cut."
              " A chord written to ring out through a saturated amp will not: fade it after the amp (an `auto` lane on its bus).")


if __name__ == "__main__":
    main()
