#!/usr/bin/env python3
"""entries: WHAT JOINS, BAR BY BAR. Every part that enters (and, if asked, leaves) over a stretch of a song, in order.
(chirp-eco, 15 Nov, for chirper-zero's finding on Common Time v49. One riff's rule was "at every landing something
joins"; the next riff's landings read riff, NOTHING, tune, octave. The gap was found from a section map's line; a
list of what enters at each bar shows a missing step as a gap in the list.)

  entries.py SONG [--from POS] [--to POS] [--quiet 2bars] [--leaves] [--pin CHIRP] [--json]

SONG is an id (songs/ID.yaml) or a file. From the plan's notes alone (nothing is rendered; a track with a `warp` is
read where its notes sound), in the order they happen:
  bar.beat   clock   + the parts that ENTER there: a note of a part that had been silent for --quiet or more
                       (default two bars; 8b, 4s and 1bar are taken too), or its first note in the song
                     - with --leaves, the parts that STOP there: their last note before such a silence (or their last)
A KIT'S TRACK IS READ PIECE BY PIECE: a china that starts on a cymbal track that was already crashing is an entry,
and reads "cym (x)". --from / --to (as `chirp render` takes positions) keep it to one stretch; what was already
playing when the stretch starts is listed first, so the entries are read against it.
What it cannot say: whether an entry is HEARD (tools/presence.py over the bars it enters in; tools/sectionmap.py
prints that command for a static window), or what a "landing" is: a wheel's meetings are in the song's generator,
not in its plan. Entries within the same beat are one line.
Only songs in one tempo. Read-only. Tests: tools/tests/test_entries.py.
"""
import json
import math
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(HERE)
sys.path.insert(0, HERE)
import chirpbin  # noqa: E402
import notechk  # noqa: E402
import velramp  # noqa: E402
import wincut  # noqa: E402


def quiet_beats(text, tempo):
    """"2bars", "1bar", "8b" or "4s" in beats; None for anything else."""
    m = re.fullmatch(r"([0-9.]+)(bars?|b|s)", text.strip())
    if not m:
        return None
    v = float(m.group(1))
    return v * 4 if m.group(2).startswith("bar") else (v if m.group(2) == "b" else v * tempo / 60.0)


def parts(canon):
    """[(label, [(start, end)])] for every part with notes, in the song's order: a pitched track or a one-piece kit
    track under its name, each piece of a kit's track as "track (piece)"; spans in beats, merged and in order."""
    names = []

    def walk(ts):
        for t in ts or []:
            if isinstance(t, dict):
                if t.get("name") and t.get("notes"):
                    names.append(t["name"])
                walk(t.get("tracks"))
    walk(canon.get("tracks"))
    out = []
    for name in names:
        notes = notechk.track_notes(canon, name) or []
        for piece, mine in velramp.pieces(notes).items():
            spans = []
            for a, b in sorted((float(n.get("at") or 0), float(n.get("at") or 0) + float(n.get("len") or 0)) for n in mine):
                if spans and a <= spans[-1][1] + 1e-9:
                    spans[-1][1] = max(spans[-1][1], b)
                else:
                    spans.append([a, b])
            out.append((name if piece is None else f"{name} ({piece})", [(a, b) for a, b in spans]))
    return out


def events(canon, quiet, lo=None, hi=None):
    """(already, [(beat, entering labels, leaving labels)]) in order. A part ENTERS on a note that follows `quiet`
    beats of its own silence (or is its first) and LEAVES at the end of its last note before one (or its last).
    lo / hi (beats) keep the events inside them; `already` is what entered before lo and has not left by it."""
    marks, already = {}, []
    for label, spans in parts(canon):
        runs = []                                   # the part's passages: spans joined across gaps shorter than quiet
        for a, b in spans:
            if runs and a - runs[-1][1] < quiet:
                runs[-1][1] = b
            else:
                runs.append([a, b])
        for a, b in runs:
            if lo is not None and a < lo < b:
                already.append(label)
            if (lo is None or a >= lo) and (hi is None or a < hi):
                marks.setdefault(float(math.floor(a + 1e-6)), ([], []))[0].append(label)
            if (lo is None or b >= lo) and (hi is None or b < hi):
                marks.setdefault(float(math.floor(b + 1e-6)), ([], []))[1].append(label)
    return already, [(beat, ins, outs) for beat, (ins, outs) in sorted(marks.items())]


def where(beat, tempo):
    """("84.1": bar and beat from 1 in 4/4, "2:40")."""
    s = beat * 60.0 / tempo
    return f"{int(beat // 4) + 1}.{int(beat % 4) + 1}", f"{int(s) // 60}:{int(s) % 60:02d}"


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    opt = {"--pin": None, "--quiet": "2bars", "--from": None, "--to": None}
    for k in list(opt):
        if k in a and a.index(k) + 1 < len(a):
            i = a.index(k)
            opt[k] = a[i + 1]
            del a[i:i + 2]
    flags = {k: k in a for k in ("--json", "--leaves")}
    a = [x for x in a if x not in flags]
    if len(a) != 1 or "-h" in a or "--help" in a:
        print(__doc__)
        return 0 if ("-h" in a or "--help" in a) else 2
    song = a[0] if os.path.exists(a[0]) else os.path.join(ROOT, "songs", a[0] + ".yaml")
    if not os.path.exists(song):
        raise SystemExit(f"entries: no song {a[0]}")
    pin = opt["--pin"] or chirpbin.resolve()
    r = subprocess.run([pin, "plan", "-f", song, "--json"], capture_output=True, text=True, cwd=ROOT,
                       env={k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"})
    try:
        canon = json.loads(r.stdout)["data"]["canonical"]
    except (ValueError, KeyError, TypeError):
        raise SystemExit(f"entries: {os.path.basename(song)} does not plan") from None
    tempo = canon.get("tempo", 120.0)
    if not isinstance(tempo, (int, float)) or isinstance(tempo, bool) or tempo <= 0:
        raise SystemExit("entries: the song's tempo changes: only songs in one tempo are read")
    quiet = quiet_beats(opt["--quiet"], tempo)
    if quiet is None or quiet <= 0:
        raise SystemExit("entries: --quiet takes a length, as in 2bars, 8b or 4s")
    ends = []
    for k in ("--from", "--to"):
        s = wincut.position(opt[k], tempo) if opt[k] else None
        if opt[k] and s is None:
            raise SystemExit(f"entries: {k} {opt[k]}: a position as chirp render takes one (77, 304b, 146s)")
        ends.append(None if s is None else s * tempo / 60.0)
    already, evs = events(canon, quiet, *ends)
    if not flags["--leaves"]:
        evs = [(b, ins, []) for b, ins, _ in evs if ins]
    if flags["--json"]:
        print(json.dumps({"song": os.path.basename(song), "quiet_beats": quiet, "already": already,
                          "events": [{"beat": b, "bar": where(b, tempo)[0], "at": where(b, tempo)[1], "enters": ins, "leaves": outs}
                                     for b, ins, outs in evs]}))
        return 0
    stretch = f", {opt['--from'] or 'the top'} to {opt['--to'] or 'the end'}" if opt["--from"] or opt["--to"] else ""
    print(f"{os.path.basename(song)}{stretch}: what enters" + (" and leaves" if flags["--leaves"] else "")
          + f", in order (a part silent for {opt['--quiet']} or more before its note; a kit's pieces apart)")
    if already:
        print(f"  already playing: {', '.join(already)}")
    if not evs:
        print("  nothing enters")
    for b, ins, outs in evs:
        bar, clock = where(b, tempo)
        said = ("+ " + ", ".join(ins) if ins else "") + ("   " if ins and outs else "") + ("- " + ", ".join(outs) if outs else "")
        print(f"  {bar:>7s} {clock:>6s}  {said}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
