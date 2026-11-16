#!/usr/bin/env python3
"""modlint: modulation amounts in the wrong unit (chirp-eco, 6 Nov). A frequency parameter's mod amount is in OCTAVES
(cutoff=800+lfo.a*2 sweeps two octaves), a gain's in dB; an amount written in Hz (-2600 on a cutoff) slams the
filter shut or open the moment the source moves. chirper-three's t8 horizon light sat at -42.6 dB from v1 to v3 that
way; chirpers4 and chirpers5 carry the same slip (300-19000 "octaves").

  modlint.py [ID|FILE …] [--album NAME] [--octaves 15] [--json]   (default: the focus album's songs)

Reads each song through `chirp plan --json` (the canonical, patches resolved; groove pin) and flags a mod on
cutoff/freq/formant/center/rate whose |amount| > --octaves. The default 15 is the engine's whole range (frequencies
clamp to 1..30000 Hz, 14.9 octaves), so a flag is never musical; deliberate full sweeps (10-11 octaves on a library
filter envelope) pass. Gains are not judged: 60-120 dB envelope fades on layer levels are a library idiom.
Read-only; exits 1 when anything is flagged.

KEY LANES (16 Nov, chirper-zero, False Summit v10: "a key lane that jumps more than a tritone"). A lane that moves
an eq's bands a semitone a unit (a mod from auto.LANE of 1/12 octave on a cutoff: the bass bus's `key`, which keeps
an eq fitted to the low F on the ground the song is in) is read against the notes of the part it serves: the
tracks sent to that bus, or the track that carries the lane. Wherever the lane holds a value and the part plays,
the part's lowest note there (one that is a tenth of its notes or more); then each MOVE of the lane beside the
move of that lowest note:
  THE LONG WAY ROUND     they differ by an octave or more exactly: the lane went +10 while the notes went -2. The eq
                         leaps a seventh while the part steps down, and sits an octave from where it was fitted.
                         (False Summit's fall, from the skeleton to v9: ground(beat, lad % 12) gave 0, 10, 7, 6, 3,
                         1; once an octave the notch landed on the fundamental of the bass voice carrying the step,
                         and the second step of every octave was 0.28 octaves brighter. Found by ear-less
                         measurement nine versions later; this reads it from the plan in a second.)
  DOES NOT FOLLOW        they differ otherwise (the lane says +3, the lowest note went +5) AND the part's notes as a
                         whole did not move by the lane's amount either (by pitch class: the move that best carries
                         one stretch's notes onto the next's). A question, not a fault. A part whose notes moved
                         with the lane but whose lowest note did not (a melody, a bell line) is not listed.
These lines are printed after the flags and do NOT change the exit status or the flag count: they are questions.
Not read: a lane that ramps instead of holding; a part whose pitches are not note names; a tempo that changes when
the lane is written in seconds. Checked on Common Time's five songs (six lanes): no line on any; sixteen on v9.
"""
import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(HERE)
sys.path.insert(0, HERE)
FREQ = {"cutoff", "freq", "formant", "center", "rate"}
SEMITONE = 1 / 12.0         # a mod amount of this (octaves a unit) makes a lane a KEY lane: its unit is a semitone
SHARE = 0.1                 # a stretch's lowest note is one that is this share of its notes (and two of them) or more


def semitone_lanes(node, found=None):
    """The names of the auto lanes that move a frequency a semitone a unit somewhere under node."""
    found = set() if found is None else found
    if isinstance(node, dict):
        for k, v in node.items():
            if isinstance(v, dict) and isinstance(v.get("mod"), list) and k in FREQ:
                for m in v["mod"]:
                    a = m.get("amount") if isinstance(m, dict) else None
                    if isinstance(a, (int, float)) and abs(abs(a) - SEMITONE) < 0.002 and str(m.get("src", "")).startswith("auto."):
                        found.add(m["src"][5:])
            semitone_lanes(v, found)
    elif isinstance(node, list):
        for v in node:
            semitone_lanes(v, found)
    return found


def held(points, tempo):
    """[(from beat, to beat, value)]: where a lane HOLDS a value (two points or more on it; the last value to the end)."""
    import warp
    pts = [(warp.beats(p[0], tempo), float(p[1])) for p in points]
    out, i = [], 0
    while i < len(pts):
        j = i
        while j + 1 < len(pts) and pts[j + 1][1] == pts[i][1]:
            j += 1
        end = pts[j][0] if j + 1 < len(pts) else float("inf")
        if end > pts[i][0]:
            out.append((pts[i][0], end, pts[i][1]))
        i = j + 1
    return out


def moved_by(before, after):
    """The moves in semitones (0-11) that best carry one stretch's notes onto the next's by pitch class: every move
    whose overlap is within a tenth of the best (a scale that maps onto itself has several). before, after: {MIDI
    number: how many notes}."""
    a, b = [0.0] * 12, [0.0] * 12
    for m, k in before.items():
        a[int(m) % 12] += k
    for m, k in after.items():
        b[int(m) % 12] += k
    score = [sum(a[pc] * b[(pc + r) % 12] for pc in range(12)) for r in range(12)]
    return {r for r in range(12) if score[r] >= 0.9 * max(score) and max(score) > 0}


def key_moves(canon):
    """(lanes read, [{where, lane, tracks, at, bar, lane_move, note_move, from, to, kind}]): each move of a key lane
    that is not the move of its part's lowest note. kind is "long" (they differ by whole octaves) or "other"."""
    import collections

    import keyshape
    import notechk
    tempo = canon.get("tempo", 120.0)
    fixed = isinstance(tempo, (int, float)) and not isinstance(tempo, bool) and tempo > 0
    tracks = [t for t in canon.get("tracks") or [] if isinstance(t, dict) and t.get("name")]
    homes = [(f"buses.{name}", b, [t["name"] for t in tracks if t.get("out") == name])
             for name, b in (canon.get("buses") or {}).items() if isinstance(b, dict)]
    homes += [(f"tracks.{t['name']}", t, [t["name"]]) for t in tracks]
    read, out = 0, []
    for where, home, part in homes:
        for lane in sorted(semitone_lanes(home.get("fx"))):
            points = ((home.get("auto") or {}).get(lane) or {}).get("points")
            if not points or not part:
                continue
            try:
                stretches = held(points, tempo if fixed else 120.0)
            except (ValueError, TypeError, IndexError):
                continue
            if not fixed and any(not str(p[0]).strip().endswith("b") or str(p[0]).strip().endswith("ms") for p in points):
                continue                                  # seconds on a changing tempo: not placed
            notes = []
            for name in part:
                for n in notechk.track_notes(canon, name) or []:
                    low = keyshape.lowest(n.get("pitch"))
                    if low is not None:
                        notes.append((float(n.get("at") or 0), low))
            read += 1
            segs = []
            for t0, t1, v in stretches:
                inside = collections.Counter(m for at, m in notes if t0 <= at < t1)
                if inside:
                    least = max(2, SHARE * sum(inside.values()))
                    often = [m for m, k in inside.items() if k >= least]
                    segs.append((t0, v, min(often) if often else min(inside), inside))
            for a, b in zip(segs, segs[1:]):
                dv, dn = b[1] - a[1], b[2] - a[2]
                if dv == dn:
                    continue
                if (dv - dn) % 12 == 0:
                    kind = "long"
                elif dv == int(dv) and int(dv) % 12 in moved_by(a[3], b[3]):
                    continue                              # the notes moved as the lane did; the lowest of them is not the ground
                else:
                    kind = "other"
                out.append({"where": where, "lane": lane, "tracks": part, "at": b[0], "bar": int(b[0] // 4) + 1,
                            "lane_move": dv, "note_move": dn, "from": keyshape.note_name(a[2]),
                            "to": keyshape.note_name(b[2]), "kind": kind})
    return read, out


def key_lines(song, moves, most=6):
    """The lines for one song's key-lane moves: the first `most` of each lane, then how many more."""
    out, seen = [], {}
    for m in moves:
        key = (m["where"], m["lane"])
        seen[key] = seen.get(key, 0) + 1
        if seen[key] > most:
            continue
        what = ("THE LONG WAY ROUND (the same key is an octave the other way: the eq leaps while the notes step)" if m["kind"] == "long"
                else "DOES NOT FOLLOW (a question: a riff's lowest note is not always its ground)")
        out.append(f"{song}: {m['where']} lane {m['lane']} ({', '.join(m['tracks'])}): at {m['at']:g}b (bar {m['bar']}) the lane moves "
                   f"{m['lane_move']:+g} and the part's lowest note {m['note_move']:+g} ({m['from']} -> {m['to']}): {what}")
    for (where, lane), n in seen.items():
        if n > most:
            out.append(f"{song}: {where} lane {lane}: and {n - most} more")
    return out


def lint(node, octaves=15.0, path=()):
    """[(path, kind, src, amount)] for frequency mod amounts beyond the engine's whole range (Hz written as octaves)."""
    out = []
    if isinstance(node, dict):
        for k, v in node.items():
            p = path + (str(k),)
            if isinstance(v, dict) and isinstance(v.get("mod"), list) and k in FREQ:
                for m in v["mod"]:
                    a = m.get("amount") if isinstance(m, dict) else None
                    if isinstance(a, (int, float)) and abs(a) > octaves:
                        out.append((".".join(p), "freq", m.get("src"), a))
            out += lint(v, octaves, p)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            out += lint(v, octaves, path + (str(i),))
    return out


def canonical(pin, song):
    r = subprocess.run([pin, "plan", "-f", song, "--json"], capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
    except ValueError:
        return None
    return (d.get("data") or d).get("canonical")


def focus_songs(album=None):
    reg = json.load(open(os.path.join(ROOT, "climbs.json")))
    album = album or reg.get("focus")
    out = []
    for c in reg.get("climbs", []):
        if str((c.get("meta") or {}).get("album", "")).casefold() == str(album).casefold():
            p = os.path.join(ROOT, c.get("song") or f"songs/{c['id']}.yaml")
            if os.path.exists(p):
                out.append(p)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("songs", nargs="*", help="climb ids or song files (default: the focus album)")
    ap.add_argument("--album")
    ap.add_argument("--octaves", type=float, default=15.0)
    ap.add_argument("--pin")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    pin = a.pin or open(os.path.join(HERE, "groove-pin")).read().strip()
    songs = [s if os.path.exists(s) else os.path.join(ROOT, "songs", f"{s}.yaml") for s in a.songs] or focus_songs(a.album)
    found, failed, keys, lanes = {}, [], {}, 0
    for s in songs:
        c = canonical(pin, s)
        if c is None:
            failed.append(s)
            continue
        hits = lint(c, a.octaves)
        if hits:
            found[os.path.relpath(s, ROOT)] = hits
        read, moves = key_moves(c)
        lanes += read
        if moves:
            keys[os.path.relpath(s, ROOT)] = moves
    if a.json:
        print(json.dumps({"flagged": found, "unplannable": failed, "checked": len(songs), "key_lanes": lanes, "key_moves": keys}))
    else:
        for s, hits in found.items():
            for p, _kind, src, amt in hits:
                print(f"{s}: {p}  src {src}  amount {amt:g} octaves (beyond the 14.9-octave range: written in Hz?)")
        print(f"modlint: {len(songs)} song(s), {sum(len(h) for h in found.values())} flag(s)"
              + (f", {len(failed)} did not plan: {', '.join(failed)}" if failed else ""))
        for s, moves in keys.items():
            for ln in key_lines(s, moves):
                print(ln)
        if lanes:
            every = [m for ms in keys.values() for m in ms]
            print(f"modlint: {lanes} key lane(s) read against their parts' lowest notes: "
                  + (f"{sum(m['kind'] == 'long' for m in every)} move(s) the long way round, "
                     f"{sum(m['kind'] != 'long' for m in every)} that do not follow (questions, not flags)" if every
                     else "every move of a lane is its part's move"))
    sys.exit(1 if found else 0)


if __name__ == "__main__":
    main()
