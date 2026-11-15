#!/usr/bin/env python3
"""keyshape: A PART'S OWN SHAPE IN EACH KEY IT PLAYS. Does its tone hold when the ground moves?
(chirp-eco, 15 Nov, for chirper-zero's finding on Plain Hunt v11, which reached all four of Common Time's songs:
every song's bass bus carried an eq fitted on the low F. On any other ground the fundamental climbed into the eq's
90 Hz lift, the compressor clamped on it, and the bass ALONE lost 3.6 dB of its 120-250 Hz on A flat and 6.8 on B,
and up to 7.5 dB at 1-2 kHz. In the mix it read as "+1 at 60-120, -2 at 120-250" on those stretches, and once as
Harry's "more bass", which was answered with a fader. He found it by benching the part four times by hand: "a
tool would have found this at the first key change of the first song".)

  keyshape.py SONG TRACK[,TRACK...] [--bars 8] [--min 2] [--pin CHIRP] [--keep DIR] [--json]

SONG is an id (songs/ID.yaml) or a file; the TRACKs are one part (the bass; both guitars of a rig: gl,gr).
The grounds are found from the part's own notes: the lowest note of each bar, and each run of bars that share it
(runs under --min bars are passing notes and left out). For each ground, the first --bars bars of its longest run
are rendered with every other track's notes out, so the part's effects, its bus and the master are the song's
(loudness off, seed 0): a second or two a ground. Printed:
  its own shape    the nine bands tools/stembal.py reads, each against the part's OWN total there, for every ground;
                   HOME is the ground with the most bars
  against home     each other ground's shape minus home's, in dB, twice:
                   as written    the bars the song plays on that ground
                   home moved    HOME's bars played THERE, moved by semitones: the same notes in that key, at that
                                 place in the song, so every lane and fader is as the song has it there
  LOSES ...        3 dB or more out of a band the part has within 25 dB of its total at home. Only bands ABOVE the
                   one that holds either fundamental are read: lower down it is the note that moved, not the tone
then what the two rows say together: when home's own notes lose the band there too, it is THE RIG (an eq, a tight
filter or a compressor fitted to one ground); when they keep it, the notes the song plays there are different ones;
when only home's notes lose something, the rig is at work there and the song's own notes hide it.
What it cannot say: whether the loss is heard (tools/stembal.py on the stretch, by part; an ear), or what mends
it. One mend: the eq bands take their cutoff from a bus lane that follows the ground
({"kind": "peak", "cutoff": {"value": 44, "mod": [{"src": "auto.key", "amount": 0.08333}]}, ...}; a Freq mod is in
octaves, so 1/12 a semitone), as Plain Hunt v11 and Odd Sympathy v23 do.
Limits: fixed-tempo songs in 4/4; notes as written (a part on a `warp` is read by the bars it is written in);
kit pieces and pitches that are not note names are skipped. --keep DIR keeps each bench song and render.
--pin: the chirp binary (else $CHIRP, else the groove's pin). Read-only. Tests: tools/tests/test_keyshape.py.
"""
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(HERE)
sys.path.insert(0, HERE)
import chirpbin  # noqa: E402
import keybench  # noqa: E402
import pitchbench  # noqa: E402
import songfmt  # noqa: E402

LABELS = keybench.LABELS
HOLDS_DB = -25.0      # a band the part "has" at home: within this of its own total
LOSES_DB = -3.0       # a ground that takes this much out of such a band loses it
BEATS = 4.0           # a bar


def note_name(m):
    m = int(round(m))
    return f"{pitchbench.NAMES[m % 12]}{m // 12 - 1}"


def lowest(pitch):
    """The lowest MIDI number in a note's pitch ("F1", "F3,C4", 41), or None when it names no pitch (a kit piece)."""
    got = []
    for part in str(pitch).split(","):
        try:
            got.append(pitchbench.midi(part))
        except ValueError:
            pass
    return min(got) if got else None


def track_notes(doc, name):
    """A track's notes as the song writes them, at any depth; None when there is no such track."""
    def walk(ts):
        for t in ts or []:
            if isinstance(t, dict):
                if t.get("name") == name:
                    return [n for n in t.get("notes") or [] if isinstance(n, dict)]
                got = walk(t.get("tracks"))
                if got is not None:
                    return got
        return None
    return walk(doc.get("tracks"))


def runs(doc, tracks):
    """[(first bar, last bar, ground)] in order: the runs of bars (from 0) in which the part's lowest note is the
    same MIDI number. A bar the part does not play ends a run. KeyError (the name) for a missing track."""
    low = {}
    for name in tracks:
        notes = track_notes(doc, name)
        if notes is None:
            raise KeyError(name)
        for n in notes:
            m = lowest(n.get("pitch"))
            if m is None:
                continue
            bar = int(float(n.get("at") or 0) // BEATS)
            low[bar] = min(low.get(bar, m), m)
    out = []
    for bar in sorted(low):
        if out and out[-1][2] == low[bar] and out[-1][1] == bar - 1:
            out[-1][1] = bar
        else:
            out.append([bar, bar, low[bar]])
    return [tuple(r) for r in out]


def grounds(found, least=2, most=8):
    """[{ground, name, hz, bars, runs, read: (first bar, last bar)}], home first, then by pitch: every ground with a
    run of `least` bars or more; `read` is the first `most` bars of its longest run."""
    by = {}
    for a, b, g in found:
        if b - a + 1 >= least:
            by.setdefault(g, []).append((a, b))
    out = []
    for g, rs in by.items():
        a, b = max(rs, key=lambda r: (r[1] - r[0], -r[0]))
        out.append({"ground": g, "name": note_name(g), "hz": round(pitchbench.hz(g), 1), "bars": sum(y - x + 1 for x, y in rs),
                    "runs": len(rs), "read": (a, min(b, a + most - 1))})
    if not out:
        return out
    home = max(out, key=lambda r: (r["bars"], -r["ground"]))
    return [home] + sorted((r for r in out if r is not home), key=lambda r: r["ground"])


def band_of(hz):
    """The index of the band a frequency falls in (0 for anything under the first edge)."""
    return max(0, sum(1 for e in keybench.EDGES[1:-1] if hz >= e))


def loses(diff, home_own, first):
    """[(band label, dB)] a ground loses: bands from index `first` up that home has, down by 3 dB or more."""
    return [(LABELS[i], d) for i, (d, own) in enumerate(zip(diff, home_own)) if i >= first and own >= HOLDS_DB and d <= LOSES_DB]


def verdict(written, moved):
    """What a ground's two rows say together ("" when neither loses anything)."""
    names = [lb for lb, _ in moved]
    both = [lb for lb, _ in written if lb in names]
    if not written:
        return (f"it holds as written; home's own notes would lose {', '.join(names)} there (the rig, hidden by the notes "
                "the song plays)") if moved else ""
    if len(both) == len(written):
        return "THE RIG: home's own notes lose " + ("it" if len(both) == 1 else "them") + " there too"
    if both:
        return f"THE RIG at {', '.join(both)} (home's own notes lose that there too); the rest is the notes the song plays there"
    if moved:
        return (f"the notes the song plays there AND the rig: home's own notes keep {', '.join(lb for lb, _ in written)} "
                f"but lose {', '.join(names)}")
    return "the notes: home's own notes, moved there, keep it"


def read(song, tracks, pin, where, least=2, most=8):
    """The table: {"home": name, "grounds": [{name, hz, bars, runs, read, own, vs_home, moved, loses, moved_loses, says}]}.
    `own` is each band against the part's own total on that ground; vs_home / moved are in dB against home's own."""
    doc = songfmt.load(song)
    tempo = doc.get("tempo", 120)
    if not isinstance(tempo, (int, float)) or isinstance(tempo, bool) or tempo <= 0:
        raise SystemExit("keyshape: the song's tempo changes: only fixed-tempo songs are benched")
    try:
        gs = grounds(runs(doc, tracks), least, most)
    except KeyError as e:
        raise SystemExit(f"keyshape: {os.path.basename(song)} has no track {e.args[0]}") from None
    if not gs:
        raise SystemExit(f"keyshape: {', '.join(tracks)} plays no pitched notes for {least} bars together")

    def shape(b0, b1, semis, tag, at=None):
        """The part's bars b0..b1 (beats) alone, moved by semis and, with `at`, played from that beat instead."""
        try:
            made = keybench.bench(doc, tracks, b0, b1, semis)
        except KeyError as e:
            raise SystemExit(f"keyshape: {os.path.basename(song)} has no track {e.args[0]}") from None
        if at is not None and at != b0:
            stack = list(made.get("tracks") or [])
            while stack:
                t = stack.pop()
                if isinstance(t, dict):
                    stack.extend(t.get("tracks") or [])
                    for n in t.get("notes") or []:
                        n["at"] = float(n.get("at") or 0) + at - b0
            b0, b1 = at, at + b1 - b0
        got = keybench.band_levels(keybench.render(made, pin, where, tag, b0, b1))
        return [round(v - got[-1], 1) for v in got[:-1]]
    home = gs[0]
    hb0 = home["read"][0] * BEATS
    for i, g in enumerate(gs):
        gb0, gb1 = g["read"][0] * BEATS, (g["read"][1] + 1) * BEATS
        g["own"] = shape(gb0, gb1, 0, f"-{g['name']}")
        if i == 0:
            continue
        semis = int(round(g["ground"] - home["ground"]))
        first = max(band_of(g["hz"]), band_of(home["hz"])) + 1
        bars = min(g["read"][1] - g["read"][0], home["read"][1] - home["read"][0]) + 1
        g["vs_home"] = [round(a - b, 1) for a, b in zip(g["own"], home["own"])]
        g["moved"] = [round(a - b, 1) for a, b in
                      zip(shape(hb0, hb0 + bars * BEATS, semis, f"-{g['name']}-moved", at=gb0), home["own"])]
        g["semis"] = semis
        g["loses"], g["moved_loses"] = loses(g["vs_home"], home["own"], first), loses(g["moved"], home["own"], first)
        g["says"] = verdict(g["loses"], g["moved_loses"])
    return {"home": home["name"], "grounds": gs}


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    opt = {"--pin": None, "--keep": None, "--bars": "8", "--min": "2"}
    for k in list(opt):
        if k in a and a.index(k) + 1 < len(a):
            i = a.index(k)
            opt[k] = a[i + 1]
            del a[i:i + 2]
    as_json = "--json" in a
    if as_json:
        a.remove("--json")
    if len(a) != 2 or "-h" in a or "--help" in a:
        print(__doc__)
        return 0 if ("-h" in a or "--help" in a) else 2
    try:
        most, least = int(opt["--bars"]), int(opt["--min"])
    except ValueError:
        most = least = 0
    if most < 1 or least < 1:
        raise SystemExit("keyshape: --bars and --min take whole numbers of bars, 1 or more")
    song, tracks = a[0], a[1].split(",")
    path = song if os.path.exists(song) else os.path.join(ROOT, "songs", song + ".yaml")
    if not os.path.exists(path):
        raise SystemExit(f"keyshape: no song {song}")
    where = opt["--keep"] or tempfile.mkdtemp(prefix="keyshape-")
    os.makedirs(where, exist_ok=True)
    try:
        got = read(path, tracks, opt["--pin"] or chirpbin.resolve(), where, least, most)
    finally:
        if not opt["--keep"]:
            shutil.rmtree(where, True)
    gs = got["grounds"]
    if as_json:
        print(json.dumps({"song": os.path.basename(path), "tracks": tracks, "bands": LABELS, **got}))
        return 0
    print(f"{os.path.basename(path)} {', '.join(tracks)}: its own shape in each key it plays (alone through its own effects, "
          "bus and master; each band against the part's OWN total, dB)")
    print(f"  {'ground':7s}{'Hz':>6s}  {'bars read':12s}" + "".join(s.rjust(8) for s in LABELS))
    for i, g in enumerate(gs):
        a0, a1 = g["read"]
        print(f"  {g['name']:7s}{g['hz']:6.1f}  {f'{a0 + 1}-{a1 + 2}':12s}" + "".join(f"{v:+8.1f}" for v in g["own"])
              + f"   {g['bars']} bars in {g['runs']} run{'s' if g['runs'] != 1 else ''}" + (": HOME" if i == 0 else ""))
    if len(gs) == 1:
        print(f"  it plays on {gs[0]['name']} only: no other key to read it in")
        return 0
    print(f"  against {got['home']} (dB; as written = the song's bars on that ground; home moved = {got['home']}'s bars played "
          "there, in that key):")
    for g in gs[1:]:
        for label, row, lost in ((f"{g['name']} as written", g["vs_home"], g["loses"]),
                                 (f"   home {g['semis']:+d}", g["moved"], g["moved_loses"])):
            print(f"  {label:27s}" + "".join(f"{v:+8.1f}" for v in row)
                  + ("   LOSES " + ", ".join(f"{lb} ({d:+.1f})" for lb, d in lost) if lost else ""))
        if g["says"]:
            print(f"  {'':27s}{g['says']}")
    if not any(g["loses"] or g["moved_loses"] for g in gs[1:]):
        print("  the part keeps its shape on every ground (no band it has at home falls 3 dB above the fundamentals)")
    print("  (bands at or under the one holding a fundamental are not read: there it is the note that moved. The bars are as "
          "`chirp render --from/--to` take them.)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
