#!/usr/bin/env python3
"""keyshape: A PART'S OWN SHAPE IN EACH KEY IT PLAYS. Does its tone hold when the ground moves?
(chirp-eco, 15 Nov, for chirper-zero's finding on Plain Hunt v11, which reached all four of Common Time's songs:
every song's bass bus carried an eq fitted on the low F. On any other ground the fundamental climbed into the eq's
90 Hz lift, the compressor clamped on it, and the bass ALONE lost 3.6 dB of its 120-250 Hz on A flat and 6.8 on B,
and up to 7.5 dB at 1-2 kHz. In the mix it read as "+1 at 60-120, -2 at 120-250" on those stretches, and once as
Harry's "more bass", which was answered with a fader. He found it by benching the part four times by hand: "a
tool would have found this at the first key change of the first song".)

  keyshape.py SONG TRACK[,TRACK...] [--bars 8] [--min 2] [--pool] [--no-mix] [--pin CHIRP] [--keep DIR] [--json]

SONG is an id (songs/ID.yaml) or a file; the TRACKs are one part (the bass; both guitars of a rig: gl,gr; where
one of them rests, the ground is read from the other).
The grounds are found from the part's own notes: the lowest note of each bar, and each run of bars that share it
(runs under --min bars are passing notes and left out). For each ground, the first --bars bars of its longest run
are rendered with every other track's notes out, so the part's effects, its bus and the master are the song's
(loudness off, seed 0): a second or two a ground. --pool reads a ground from as many of its runs as it takes
to make --bars bars (longest first; their power summed), for a part that changes ground every bar or two: with
--min 1 a pedal of one bar a ground is read from eight of its bars, not one ("12-13 +7" = that bar and seven more
stretches). Printed:
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
  IN THE MIX       for a ground that loses something: the WHOLE song over the first four bars read there, and for
                   each band lost how far the part alone sits against the mix (-17.1: that far under it) and what
                   the loss is WORTH: the dB the mix's band would rise were it mended (powers added; a first
                   figure). COVERED when no band is worth 0.5 dB: the rest of the band holds those bands there, and
                   a mend will not be heard as level (chirper-zero, Common Time v51: a 7 dB mend of the bass alone
                   moved the mix 1 dB at 120-250 Hz and nothing above; "a line under the table would have said it
                   before the first full render"). It costs one render of the whole song's bars for each ground that
                   loses: on a full song about 40 s each, however few the bars (the engine's start is most of it).
                   --no-mix leaves it out: use that while fitting a mend, and read the mix once at the end.
A ground nine semitones or more from home is marked: the bands are an octave wide, so that far the harmonics
themselves change bands and a few dB of any loss is the note.
What it cannot say: whether the loss is heard as TONE where the part is exposed (an ear; tools/stembal.py on the
stretch, by part), or what mends it. One mend: the eq bands take their cutoff from a bus lane that follows the ground
({"kind": "peak", "cutoff": {"value": 44, "mod": [{"src": "auto.key", "amount": 0.08333}]}, ...}; a Freq mod is in
octaves, so 1/12 a semitone), as Plain Hunt v11 and Odd Sympathy v23 do.
Limits: fixed-tempo songs in 4/4; notes as written (a part on a `warp` is read by the bars it is written in);
kit pieces and pitches that are not note names are skipped. --keep DIR keeps each bench song and render.
--pin: the chirp binary (else $CHIRP, else the groove's pin). Read-only. Tests: tools/tests/test_keyshape.py.
"""
import json
import math
import os
import shutil
import sys
import tempfile

import numpy as np

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
MIX_BARS = 4          # IN THE MIX reads the whole song over this many bars of a ground's first stretch ...
MIX_PREROLL_S = 3.0   # ... with the engine warmed this long before them (`chirp render --preroll`). On Common Time a
#                       render costs 38 s whether it is two bars or four, warmed 0.5 s or 6 (the engine's start), two
#                       bars read within 1 dB of four, and three renders at once were no faster than one after another
COVERED_DB = 0.5      # no lost band worth this much of the mix: COVERED


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


def grounds(found, least=2, most=8, pool=False):
    """[{ground, name, hz, bars, runs, read: (first bar, last bar), reads: [(first, last)]}], home first, then by
    pitch: every ground with a run of `least` bars or more; `read` is the first `most` bars of its longest run, and
    `reads` is that alone, or with `pool` as many of its runs (longest first) as it takes to make `most` bars."""
    by = {}
    for a, b, g in found:
        if b - a + 1 >= least:
            by.setdefault(g, []).append((a, b))
    out = []
    for g, rs in by.items():
        order = sorted(rs, key=lambda r: (-(r[1] - r[0]), r[0]))
        a, b = order[0]
        reads, have = [], 0
        for x, y in order if pool else order[:1]:
            if have >= most:
                break
            y = min(y, x + most - have - 1)
            reads.append((x, y))
            have += y - x + 1
        out.append({"ground": g, "name": note_name(g), "hz": round(pitchbench.hz(g), 1), "bars": sum(y - x + 1 for x, y in rs),
                    "runs": len(rs), "read": (a, min(b, a + most - 1)), "reads": sorted(reads)})
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


FAR = 9               # semitones: from here a move carries the harmonics most of a band up by itself


def far_note(semis):
    """A caution for a ground far from home ("" within FAR semitones): the bands are an octave wide."""
    if abs(semis) < FAR:
        return ""
    return (f" ({abs(semis)} semitones from home: the harmonics themselves move most of a band, so a few dB of this is the "
            "note, not the rig)")


def worth(under, loss):
    """The dB a mix's band would rise were a part's loss in it mended: the part sits `under` dB against the mix there
    (negative: under it) having lost `loss` dB (negative). Powers added: a first figure."""
    return 10 * math.log10(1 + 10 ** (under / 10.0) * (10 ** (-loss / 10.0) - 1))


def read(song, tracks, pin, where, least=2, most=8, pool=False, mix=True):
    """The table: {"home": name, "grounds": [{name, hz, bars, runs, read, own, vs_home, moved, loses, moved_loses, says,
    in_mix}]}. `own` is each band against the part's own total on that ground; vs_home / moved are in dB against
    home's own; in_mix (a ground that loses, with `mix`): {bars, bands: [{band, loss, under, worth}], covered}."""
    doc = songfmt.load(song)
    tempo = doc.get("tempo", 120)
    if not isinstance(tempo, (int, float)) or isinstance(tempo, bool) or tempo <= 0:
        raise SystemExit("keyshape: the song's tempo changes: only fixed-tempo songs are benched")
    try:
        gs = grounds(runs(doc, tracks), least, most, pool)
    except KeyError as e:
        raise SystemExit(f"keyshape: {os.path.basename(song)} has no track {e.args[0]}") from None
    if not gs:
        raise SystemExit(f"keyshape: {', '.join(tracks)} plays no pitched notes for {least} bars together")

    def shape(b0, b1, semis, tag, at=None):
        """The part's bars b0..b1 (beats) alone, moved by semis and, with `at`, played from that beat instead. Of
        several tracks, those that play in those bars (a second guitar may rest where the first carries the ground)."""
        here = [t for t in tracks if any(b0 <= float(n.get("at") or 0) < b1 for n in track_notes(doc, t) or [])]
        try:
            made = keybench.bench(doc, here, b0, b1, semis)
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
        return keybench.band_levels(keybench.render(made, pin, where, tag, b0, b1))

    def summed(levels):
        """Several stretches' bands (and the whole, last) as one: their power summed."""
        return 10 * np.log10(np.sum(10 ** (np.array(levels) / 10.0), axis=0))

    def own(levels):
        """Several stretches' bands as one: their power summed, each band against the total (one stretch: itself)."""
        total = summed(levels)
        return [round(float(v - total[-1]), 1) for v in total[:-1]]
    home = gs[0]
    for i, g in enumerate(gs):
        alone = [shape(a * BEATS, (b + 1) * BEATS, 0, f"-{g['name']}-{k}") for k, (a, b) in enumerate(g["reads"])]
        g["own"] = own(alone)
        if i == 0:
            continue
        semis = int(round(g["ground"] - home["ground"]))
        first = max(band_of(g["hz"]), band_of(home["hz"])) + 1
        g["vs_home"] = [round(a - b, 1) for a, b in zip(g["own"], home["own"])]
        moved = []
        for k, (a, b) in enumerate(g["reads"]):          # home's own bars, played at each of this ground's stretches
            ha, hb = home["reads"][k % len(home["reads"])]
            bars = min(b - a, hb - ha) + 1
            moved.append(shape(ha * BEATS, (ha + bars) * BEATS, semis, f"-{g['name']}-moved-{k}", at=a * BEATS))
        g["moved"] = [round(a - b, 1) for a, b in zip(own(moved), home["own"])]
        g["semis"] = semis
        g["loses"], g["moved_loses"] = loses(g["vs_home"], home["own"], first), loses(g["moved"], home["own"], first)
        g["says"] = verdict(g["loses"], g["moved_loses"])
        if g["says"]:
            g["says"] += far_note(semis)

    def in_mix(g):
        """The WHOLE song over the ground's first bars: what is each lost band worth there?"""
        lost = {**dict(g["moved_loses"]), **dict(g["loses"])}          # a band both rows lose: the song's own figure
        a = g["reads"][0][0]
        b0, b1 = a * BEATS, (a + min(g["reads"][0][1] - a + 1, MIX_BARS)) * BEATS
        part = shape(b0, b1, 0, f"-{g['name']}-part")
        whole = keybench.band_levels(keybench.render(doc, pin, where, f"-{g['name']}-mix", b0, b1, preroll=MIX_PREROLL_S))
        bands = [{"band": lb, "loss": lost[lb], "under": round(float(part[k] - whole[k]), 1)}
                 for k, lb in enumerate(LABELS) if lb in lost]
        for m in bands:
            m["worth"] = round(worth(m["under"], m["loss"]), 1)
        return {"bars": [a, int(b1 / BEATS) - 1], "bands": bands, "covered": all(m["worth"] < COVERED_DB for m in bands)}
    for g in gs[1:] if mix else []:
        if g["loses"] or g["moved_loses"]:
            g["in_mix"] = in_mix(g)
    return {"home": home["name"], "grounds": gs}


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    opt = {"--pin": None, "--keep": None, "--bars": "8", "--min": "2"}
    pool = "--pool" in a
    if pool:
        a.remove("--pool")
    mix = "--no-mix" not in a
    if not mix:
        a.remove("--no-mix")
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
        got = read(path, tracks, opt["--pin"] or chirpbin.resolve(), where, least, most, pool, mix)
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
        if len(g["reads"]) > 1:
            a0, a1 = g["reads"][0]
        many = f" +{len(g['reads']) - 1}" if len(g["reads"]) > 1 else ""
        print(f"  {g['name']:7s}{g['hz']:6.1f}  {f'{a0 + 1}-{a1 + 2}{many}':12s}" + "".join(f"{v:+8.1f}" for v in g["own"])
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
        if g.get("in_mix"):
            im = g["in_mix"]
            print(f"  {'':27s}IN THE MIX there (the whole song, bars {im['bars'][0] + 1}-{im['bars'][1] + 2}; the part alone against "
                  "the mix, and what its loss is worth of the mix, dB): "
                  + "; ".join(f"{m['band']} {m['under']:+.1f}, {-m['loss']:.1f} worth {m['worth']:.1f}" for m in im["bands"]))
            if im["covered"]:
                print(f"  {'':27s}COVERED: mended, no band of the mix would rise {COVERED_DB:g} dB on these bars: it will not be "
                      "heard as level (as the part's own tone where it is exposed: an ear)")
    if not any(g["loses"] or g["moved_loses"] for g in gs[1:]):
        print("  the part keeps its shape on every ground (no band it has at home falls 3 dB above the fundamentals)")
    print("  (bands at or under the one holding a fundamental are not read: there it is the note that moved. The bars are as "
          "`chirp render --from/--to` take them.)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
