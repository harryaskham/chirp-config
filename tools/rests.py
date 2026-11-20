#!/usr/bin/env python3
"""rests: the gaps in a part's notes, and what else sounds in them. CAN ITS REVERB BE HEARD?
(chirp-eco, 14 Nov, for chirper-zero's finding on Common Time v47. Harry said of a dripping spring "I cannot hear it in
the piece"; the cause was that the two guitars carrying it had NO gap between notes anywhere in the spring's two
places, so nothing of the spring was ever heard alone. "A reader would have said so in round 38.")

  rests.py SONG TRACK [TRACK ...] [--min 150ms] [--from POS] [--to POS] [--tail 1s] [--pin CHIRP] [--json]
  rests.py SONG ride:rb cym:x                  (ONE PIECE of a kit's track: where that piece plays, and its rests)

SONG is an id (songs/ID.yaml) or a file; each TRACK a part with a spring, an echo, a long reverb or a ring that is
meant to be heard. From the plan's notes alone (nothing is rendered; a track with a `warp` is read where its notes
sound), for each track:
  the passages it plays (runs of notes with no gap of two bars or more)
  every REST of --min or longer (default 150 ms; 0.5b and 0.2s are taken too): where it starts (clock, bar and beat),
  how long it is, and WHAT ELSE SOUNDS in its first --tail (default one second: where a tail lives)
and it says so plainly when a part has no rest at all: then whatever follows its notes is never heard on its own,
at any mix. --from / --to (as `chirp render` takes positions) read one stretch of the song.
A rest is between notes AS WRITTEN: the end of one (its `at` + `len`) and the start of the next on that track. What
it cannot say: how long a note really rings past its written length (tools/stops.py reads that from a render), how
loud the tail is (tools/presence.py, tools/dispersion.py), or whether the parts that sound in the rest cover it
(tools/stembal.py --parts). Kit tracks count as sounding while their hits are written.
WHERE ELSE DOES THIS PART PLAY? TRACK:PIECE reads one piece of a kit's track (the ride bell on the `ride` track,
the china on `cym`), so the first line, "plays bars ...", answers it for a single drum. When an ear turns a device
down in one place, look there for the same piece on the same pattern elsewhere: a ride-bell pendulum was mended in
the two passages Harry was asked about and left opening the song for seven hours (chirper-zero, Odd Sympathy v21).
One tempo, or a tempo map placed in beats: the clock, a rest's milliseconds and a length given in ms or seconds are
then measured where the rest falls; bars are fours. Read-only. Tests: tools/tests/test_rests.py.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(HERE)
sys.path.insert(0, HERE)
import chirpbin  # noqa: E402
import notechk  # noqa: E402
import wincut  # noqa: E402

PASSAGE_BEATS = 8.0          # a gap this long (two bars of four) ends a passage: the part is out, not resting


def span_s(text, tempo):
    """"150ms", "0.2s" or "0.5b" in seconds; None for anything else."""
    m = re.fullmatch(r"([0-9.]+)(ms|s|b)", text.strip())
    if not m:
        return None
    v = float(m.group(1))
    return {"ms": v / 1000.0, "s": v, "b": v * 60.0 / tempo}[m.group(2)]


def names(canon):
    """Every track that has notes, at any depth, in the song's order."""
    out = []

    def walk(ts):
        for t in ts or []:
            if isinstance(t, dict):
                if t.get("name") and t.get("notes"):
                    out.append(t["name"])
                walk(t.get("tracks"))
    walk(canon.get("tracks"))
    return out


def notes_of(canon, name):
    """The notes of a track, or of ONE PIECE of a kit's track when name is "TRACK:PIECE" (ride:rb); None when there is
    no such track."""
    track, _, piece = name.partition(":")
    notes = notechk.track_notes(canon, track)
    if notes is None or not piece:
        return notes
    return [n for n in notes if str(n.get("pitch")) == piece]


def sounding(canon, name):
    """[(start, end)] in beats, merged and in order, of when the track's notes (or one piece's: TRACK:PIECE) are
    written to sound."""
    spans = sorted((float(n.get("at") or 0), float(n.get("at") or 0) + float(n.get("len") or 0))
                   for n in notes_of(canon, name) or [])
    out = []
    for a, b in spans:
        if out and a <= out[-1][1] + 1e-9:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return [(a, b) for a, b in out]


def rests(spans, least, lo=None, hi=None, long=None):
    """(passages, rests) of one track's sounding spans (beats): passages are [(start, end)] runs with no gap of
    PASSAGE_BEATS or more; rests [(start, length)] the gaps of `least` beats or more INSIDE a passage, plus the gap
    after each passage's last note (its length to the next note, or None after the track's last), since that is where
    a tail rings out. lo / hi (beats) keep the passages that reach into them and the rests that start inside them.
    `long(end, next)`, when given, says whether the gap from beat END to beat NEXT is a rest, in place of `least`
    beats (a length in seconds on a tempo map)."""
    passages, found = [], []
    for i, (a, b) in enumerate(spans):
        if not passages or a - passages[-1][1] >= PASSAGE_BEATS:
            passages.append([a, b])
        else:
            passages[-1][1] = b
        nxt = spans[i + 1][0] if i + 1 < len(spans) else None
        gap = None if nxt is None else nxt - b
        if gap is None or (long(b, nxt) if long else gap >= least):
            found.append((b, gap))
    inside = lambda x: (lo is None or x >= lo) and (hi is None or x < hi)  # noqa: E731
    return ([tuple(p) for p in passages if (lo is None or p[1] > lo) and (hi is None or p[0] < hi)],
            [f for f in found if inside(f[0])])


def others_in(all_spans, name, start, length):
    """The other tracks with a note sounding in [start, start + length) beats, in the song's order."""
    end = start + length
    return [n for n, spans in all_spans.items() if n != name and any(a < end and b > start for a, b in spans)]


def where(beat, tempo):
    """(clock "11:19.0", "357.1": bar and beat, both from 1, in 4/4). `tempo`: a number, a tempo map or a tempoclock."""
    s = wincut.clock_of(tempo).secs(beat)
    return f"{int(s) // 60}:{s % 60:04.1f}", f"{int(beat // 4) + 1}.{int(beat % 4) + 1}"


def read(canon, tracks, least_s, tail_s, lo_s=None, hi_s=None, least_b=None, tail_b=None):
    """[{track, passages, rests: [{at_beat, at, bar, beats, ms, out, with}], notes}] for each track asked for.
    A tempo map placed in beats is followed (bd-10e881): a length in seconds is measured where the rest falls;
    least_b / tail_b give a length in BEATS on such a song (then least_s / tail_s is not used for it)."""
    clock = wincut.clock_of(canon.get("tempo", 120.0))
    if clock is None:
        raise ValueError("a tempo map this cannot place")
    tempo = clock.bpm
    if clock.mapped:
        to_b = lambda s: None if s is None else clock.beats(s)  # noqa: E731
        long = None if least_b is not None else (lambda b, nxt: clock.secs(nxt) - clock.secs(b) >= least_s - 1e-9)
        tail_at = lambda start: tail_b if tail_b is not None else clock.beats(clock.secs(start) + tail_s) - start  # noqa: E731
        ms_of = lambda start, gap: round((clock.secs(start + gap) - clock.secs(start)) * 1000.0)  # noqa: E731
        least = least_b
    else:
        to_b = lambda s: None if s is None else s * tempo / 60.0  # noqa: E731
        long = None
        tail_at = lambda start: to_b(tail_s)  # noqa: E731
        ms_of = lambda start, gap: round(gap * 60000.0 / tempo)  # noqa: E731
        least = to_b(least_s)
    lo, hi = to_b(lo_s), to_b(hi_s)
    all_spans = {n: sounding(canon, n) for n in names(canon)}
    out = []
    for name in tracks:
        if name.partition(":")[0] not in all_spans or not (notes_of(canon, name) or []):
            raise KeyError(name)
        mine = all_spans[name] if name in all_spans else sounding(canon, name)       # a kit's piece: its own spans
        passages, found = rests(mine, least, lo, hi, long)
        rows = []
        for start, gap in found:
            ends_passage = gap is None or gap >= PASSAGE_BEATS
            listen = tail_at(start) if ends_passage else min(gap, tail_at(start))
            clock_, bar = where(start, clock)
            rows.append({"at_beat": round(start, 3), "at": clock_, "bar": bar,
                         "beats": None if gap is None else round(gap, 3),
                         "ms": None if gap is None else ms_of(start, gap),
                         "out": ends_passage, "with": others_in(all_spans, name, start, listen)})
        out.append({"track": name, "passages": [[round(a, 3), round(b, 3)] for a, b in passages], "rests": rows,
                    "notes": len(notes_of(canon, name) or [])})
    return out


def bars_of(passages):
    """Passages (beats) as bars counted from 1: "71-77, 361-363, 9"."""
    ends = [(int(a // 4) + 1, int((b - 1e-6) // 4) + 1) for a, b in passages]
    return ", ".join(f"{a}" if a == b else f"{a}-{b}" for a, b in ends)


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    opt = {"--pin": None, "--min": "150ms", "--from": None, "--to": None, "--tail": "1s"}
    for k in list(opt):
        if k in a and a.index(k) + 1 < len(a):
            i = a.index(k)
            opt[k] = a[i + 1]
            del a[i:i + 2]
    as_json = "--json" in a
    a = [x for x in a if x != "--json"]
    if len(a) < 2 or "-h" in a or "--help" in a:
        print(__doc__)
        return 0 if ("-h" in a or "--help" in a) else 2
    song = a[0] if os.path.exists(a[0]) else os.path.join(ROOT, "songs", a[0] + ".yaml")
    if not os.path.exists(song):
        raise SystemExit(f"rests: no song {a[0]}")
    pin = opt["--pin"] or chirpbin.resolve()
    r = subprocess.run([pin, "plan", "-f", song, "--json"], capture_output=True, text=True, cwd=ROOT,
                       env={k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"})
    try:
        canon = json.loads(r.stdout)["data"]["canonical"]
    except (ValueError, KeyError, TypeError):
        raise SystemExit(f"rests: {os.path.basename(song)} does not plan") from None
    tempo = wincut.clock_of(canon.get("tempo", 120.0))     # one tempo, or a tempo map placed in beats (bd-10e881)
    if tempo is None:
        raise SystemExit("rests: this song's tempo map cannot be placed here (a change of meter, or points not in beats): "
                         "only one tempo, or a map in beats, is read")
    least, tail = span_s(opt["--min"], tempo.bpm), span_s(opt["--tail"], tempo.bpm)
    if least is None or tail is None:
        raise SystemExit("rests: --min and --tail take a length, as in 150ms, 0.2s or 0.5b")
    in_beats = {}
    if tempo.mapped:                               # a length in beats stays in beats where the tempo changes
        for k, name in (("--min", "least_b"), ("--tail", "tail_b")):
            if re.fullmatch(r"[0-9.]+b", opt[k].strip()):
                in_beats[name] = float(opt[k].strip()[:-1])
        least = None if "least_b" in in_beats else least
        tail = None if "tail_b" in in_beats else tail
    ends = [wincut.position(opt[k], tempo) if opt[k] else None for k in ("--from", "--to")]
    for k, v in zip(("--from", "--to"), ends):
        if opt[k] and v is None:
            raise SystemExit(f"rests: {k} {opt[k]}: a position as chirp render takes one (357, 1424b, 679s)")
    try:
        table = read(canon, a[1:], least, tail, *ends, **in_beats)
    except KeyError as e:
        raise SystemExit(f"rests: {os.path.basename(song)} has no track {e.args[0]} with notes") from None
    if as_json:
        print(json.dumps({"song": os.path.basename(song), "min_s": least, "tail_s": tail, **in_beats, "tracks": table}))
        return 0
    stretch = (f", {opt['--from'] or 'the top'} to {opt['--to'] or 'the end'}" if opt["--from"] or opt["--to"] else "")
    for t in table:
        inside = [r for r in t["rests"] if not r["out"]]
        ends_ = [r for r in t["rests"] if r["out"]]
        head = f"{os.path.basename(song)} {t['track']}{stretch}: "
        if not t["passages"]:
            print(head + "no notes there")
            continue
        print(head + f"plays bars {bars_of(t['passages'])}; {len(inside)} rest(s) of {opt['--min']} or more between its notes, "
              f"{len(ends_)} passage end(s)")
        if not inside:
            print("  NO REST BETWEEN ITS NOTES: whatever follows a note (a spring, an echo, a ring) is never heard on its own "
                  "there, at any mix; only at a passage's end")
        if t["rests"]:
            print(f"  {'at':>8s} {'bar':>7s} {'length':>16s}  what else sounds in its first {opt['--tail']}")
        for r in t["rests"]:
            length = "(its last note)" if r["ms"] is None else (f"{r['ms']} ms ({r['beats']:g}b)" if not r["out"]
                                                                 else f"out {r['beats'] / 4:g} bars")
            other = ", ".join(r["with"][:8]) + (f" +{len(r['with']) - 8}" if len(r["with"]) > 8 else "") if r["with"] \
                else "NOTHING: it is alone"
            print(f"  {r['at']:>8s} {r['bar']:>7s} {length:>16s}  {other}")
        if inside:
            alone = sum(1 for r in inside if not r["with"])
            print(f"  longest {max(r['ms'] for r in inside)} ms; {alone} of {len(inside)} with nothing else written under them")
    return 0


if __name__ == "__main__":
    sys.exit(main())
