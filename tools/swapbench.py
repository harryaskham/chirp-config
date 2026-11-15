#!/usr/bin/env python3
"""swapbench: SWAP OR LAYER? The same notes of a part on other patches, alone through the part's own routing.
(chirp-eco, 14 Nov, for chirper-zero's finding on Plain Hunt v3: "swap or layer is a measurement, not a taste". A
fuzz bass, on its own through the bass's bus, had 7 dB less under 60 Hz and 3 dB less at 60-120 Hz than the bass it
would have replaced: as a swap it would have thinned half the song, as a layer it added the teeth. He measured that by
hand with an FFT; this is that as one command.)

  swapbench.py SONG TRACK FROM-TO PATCH[@DB] [PATCH[@DB] ...] [--layer] [--pin CHIRP] [--keep DIR] [--json]
  chirpers.py palette ID --bench TRACK FROM-TO PATCH[@DB] ... [--layer]        (the same, from the palette brief)
  swapbench.py SONG TRACK[,TRACK...] FROM-TO                    (no patch: THE PART ALONE BY BAND, as it is, in seconds)

SONG is an id (songs/ID.yaml) or a file; TRACK the part; FROM-TO the bars it plays, as `chirp render --from/--to`
take positions (63-66, 248b-264b); each PATCH a patch as a song names one (a library name, with overrides if
wanted: "bass-fuzz fx.0.shape=wavefold"; or one of the song's own `patches:`). @DB puts that many dB more of it
into the track's bus (bass-fuzz@+4, pad@-6): a `gain` at the end of the track's own effects.
The bench is the song with every other track's notes out, so the track's own effects, its bus, its sends and the
master are the song's (loudness off, seed 0), and the part's notes in the window as written.
Prints the nine bands tools/stembal.py reads (under 60 Hz to 8-16 kHz) and the whole:
  as it is        the part on its present patch, each band against its own total
  PATCH           that patch IN ITS PLACE, in dB against as it is (same notes, same routing, same fader); and
                  "= LUFS": the dB to add to it (PATCH@+2.5) for the part alone to be AS LOUD as it is now, by a
                  loudness meter. A first figure: through a bus compressor the level does not follow the gain
                  exactly, so run it once more with the @DB and read the column again (it should read 0).
  + PATCH         with --layer: that patch OVER the present one (a second track beside it), against as it is
then EACH PATCH'S OWN SHAPE: every swap's nine bands against its own total, under the present part's, so where a
new sound's weight sits is read off the bench and not found on the full render (chirper-zero, Odd Sympathy v19: a
voice benched by loudness, presence and words, not by band, put its passage 6.3 dB over the records at 250-500 Hz;
"a band table of the voice alone would have said it in ten seconds").
With no PATCH it is that table for the part as it is; several tracks (tc,sl,sr) are read together as one part.
and, when the part has RESTS in the window (60 ms or more between its notes as written), THE PART'S RESTS: for the
part as it is and for each patch, the level in the SECOND HALF of each rest (of its first quarter second at most:
by then a note's own release is over) against the level in the notes. -10 is a stop; 0 is a rig that plays through
its rests (chirper-zero, Running Total v6: the plain wall rig read a riff's sixteenth rests AS LOUD as the chug
before them, its stop form 7 to 8 dB down, and the band table could not show it).
What the rows say:
  LOSES ...       a swap takes 3 dB or more out of a band the part holds (within 15 dB of its own total): what a
                  layer would keep
  NOT THERE       a layer moves no band by 0.5 dB: it is under its own part (raise it, PATCH@+4, and read again)
  FILLS THE RESTS a patch's rests are 3 dB or more nearer its notes than the present part's: less of a stop
A band where neither patch has anything (60 dB under the part's total, and still 45 under with the new patch) is
printed as a dot: its difference is noise. (--json keeps the number.)
What it cannot say: how either sounds; what the rest of the band covers (tools/presence.py against the part it
layers, tools/stembal.py --parts); what a bus compressor keyed by other tracks would do. A layer here goes where
the track goes; a layer on another bus is the song's to try.
--keep DIR keeps each bench song and render. --pin: the chirp binary (else $CHIRP, else the groove's pin).
Read-only. Tests: tools/tests/test_swapbench.py.
"""
import json
import math
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(HERE)
sys.path.insert(0, HERE)
import chirpbin  # noqa: E402
import keybench  # noqa: E402
import levels  # noqa: E402
import likeness  # noqa: E402
import songfmt  # noqa: E402
import wincut  # noqa: E402

LABELS = keybench.LABELS
HOLDS_DB = -15.0      # a band the part "holds": within this of its own total
LOSES_DB = -3.0       # a swap that takes this much out of such a band loses it
THERE_DB = 0.5        # a layer that moves no band by this much is not there
EMPTY_DB = (-60.0, -45.0)   # a band this far under the part's total, and still this far under on the new patch, is empty
REST_S = 0.06         # a written gap this long between the part's notes is a rest (a sixteenth at 240 is 62 ms) ...
REST_READ_S = 0.25    # ... read in the second half of its first quarter second at most: past the note's own release
                      # (a gated rig is still up for 30-40 ms), before the room's tail is all that is left
FILLS_DB = 3.0        # rests this much nearer the notes than the present part's: FILLS THE RESTS
REST_FLOOR_DB = -60.0  # nothing reads deeper than this


def candidate(text):
    """"bass-fuzz fx.0.shape=wavefold@+4" -> ("bass-fuzz fx.0.shape=wavefold", 4.0); no @DB -> 0.0."""
    patch, at, db = text.rpartition("@")
    if at:
        try:
            return patch.strip(), float(db)
        except ValueError:
            pass
    return text.strip(), 0.0


def find(tracks, name):
    """(the list a track called name sits in, its index), at any depth; None when there is none."""
    for i, t in enumerate(tracks or []):
        if isinstance(t, dict):
            if t.get("name") == name:
                return tracks, i
            got = find(t.get("tracks"), name)
            if got:
                return got
    return None


def with_patch(bench, track, patch, db, layer):
    """The bench song with `track` on `patch` (db more of it), in its place or (layer) as a second track beside it."""
    out = json.loads(json.dumps(bench))
    where, i = find(out["tracks"], track)
    t = json.loads(json.dumps(where[i])) if layer else where[i]
    t["patch"] = patch
    if db:
        t["fx"] = list(t.get("fx") or []) + [f"gain gain={db:g}dB"]
    if layer:
        t["name"] = f"{track}+layer"
        where.insert(i + 1, t)
    return out


def empty(own, diff):
    """Is a band empty on both patches (own: the present patch's band against its total; diff: the new one's move)?"""
    return own <= EMPTY_DB[0] and own + diff <= EMPTY_DB[1]


def reading(row, base):
    """What a row says: the bands a swap LOSES, or that a layer is NOT THERE; "" otherwise."""
    if row["how"] == "swap":
        lost = [(lb, d) for lb, d, own in zip(LABELS, row["bands"], base) if own >= HOLDS_DB and d <= LOSES_DB]
        return "LOSES " + ", ".join(f"{lb} ({d:+.1f})" for lb, d in lost) if lost else ""
    return "NOT THERE" if max(abs(d) for d, own in zip(row["bands"], base) if not empty(own, d)) < THERE_DB else ""


def written(bench, tracks, b0, tempo):
    """(notes, rests) of the part in a bench song, each [(start, end)] in seconds from the bench render's start (beat
    b0): when its notes are written to sound (the tracks together), and where each gap of REST_S or more between them
    is read: the second half of its first REST_READ_S at most. (None, None) when a note has no written length: a
    kit's hit has no rest to read."""
    spans = []
    for name in tracks:
        where, i = find(bench["tracks"], name)
        for n in where[i].get("notes") or []:
            ln = n.get("len")
            if isinstance(ln, bool) or not isinstance(ln, (int, float)) or ln <= 0:
                return None, None
            a = (float(n.get("at") or 0) - b0) * 60.0 / tempo
            spans.append((a, a + float(ln) * 60.0 / tempo))
    notes = []
    for a, b in sorted(spans):
        if notes and a <= notes[-1][1] + 1e-9:
            notes[-1][1] = max(notes[-1][1], b)
        else:
            notes.append([a, b])
    rests = [(b + min(nxt - b, REST_READ_S) / 2, b + min(nxt - b, REST_READ_S))
             for (_, b), (nxt, _) in zip(notes, notes[1:]) if nxt - b >= REST_S - 1e-9]
    return [tuple(n) for n in notes], rests


def rest_depth(wav, notes, rests):
    """The level in the part's rests against the level in its notes, in dB (negative: quieter in the rests; never
    under REST_FLOOR_DB). None when there is nothing to read."""
    x = likeness.load(wav).astype(float)

    def power(spans):
        tot, n = 0.0, 0
        for a, b in spans:
            seg = x[max(0, int(round(a * likeness.SR))):max(0, int(round(b * likeness.SR)))]
            tot, n = tot + float((seg ** 2).sum()), n + seg.size
        return tot / n if n else None
    held, gap = power(notes), power(rests)
    if not held or gap is None:
        return None
    return round(max(REST_FLOOR_DB, 10 * math.log10(gap / held + 1e-12)), 1)


def lufs(wav):
    """The loudness of a bench render (K-weighted, gated, as LUFS)."""
    return levels.loudness(likeness.load(wav), likeness.SR)[0]


def table(song, track, b0, b1, cands, layer, pin, where):
    """[{patch, db, how ("as it is" | "swap" | "layer"), bands, all, own, says}] for the track's notes in beats
    b0..b1: `bands` in dB against the part as it is (the first row's against its own total), `own` each row's bands
    against ITS OWN total. `track` may be several ("tc,sl,sr": one part) when there are no candidates. When the
    part has written rests there, every row has `rest_db` (rest_depth) and the first `rests`, how many."""
    doc = songfmt.load(song)
    tracks = track.split(",")
    if len(tracks) > 1 and cands:
        raise SystemExit("swapbench: several tracks are read together only with no PATCH (the part as it is); a swap is one track's")
    try:
        bench = keybench.bench(doc, tracks, b0, b1, 0)
    except KeyError as e:
        raise SystemExit(f"swapbench: {os.path.basename(song)} has no track {e.args[0]}") from None
    now = []
    for t in tracks:
        spot = find(doc.get("tracks"), t)
        p = spot[0][spot[1]].get("patch")
        now.append(p if isinstance(p, str) else "(its own inline patch)")
    now = " + ".join(dict.fromkeys(now))
    wav = keybench.render(bench, pin, where, "", b0, b1)
    base, loud = keybench.band_levels(wav), lufs(wav)
    own = [round(v - base[-1], 1) for v in base[:-1]]
    rows = [{"patch": now, "db": 0.0, "how": "as it is", "bands": own, "all": 0.0, "own": own, "says": ""}]
    notes, gaps = written(bench, tracks, b0, float(doc.get("tempo", 120)))
    depth = rest_depth(wav, notes, gaps) if gaps else None
    if depth is not None:
        rows[0].update(rest_db=depth, rests=len(gaps))
    n = 0
    for patch, db in cands:
        for how in ("swap", "layer") if layer else ("swap",):
            n += 1
            try:
                wav = keybench.render(with_patch(bench, track, patch, db, how == "layer"), pin, where, f"-{n}", b0, b1)
            except SystemExit as e:
                raise SystemExit(str(e).replace("keybench:", f"swapbench: {patch}:")) from None
            got = keybench.band_levels(wav)
            row = {"patch": patch, "db": db, "how": how, "bands": [round(v - b, 1) for v, b in zip(got[:-1], base[:-1])],
                   "all": round(got[-1] - base[-1], 1), "own": [round(v - got[-1], 1) for v in got[:-1]]}
            row["says"] = reading(row, own)
            if how == "swap":                      # the dB more of it that makes the part alone as loud as it is now
                row["match_db"] = round(loud - lufs(wav), 1)
            if depth is not None:
                row["rest_db"] = rest_depth(wav, notes, gaps)
            rows.append(row)
    return rows


def rest_lines(rows, names, width):
    """The lines of THE PART'S RESTS (none when the part has no written rest in the window)."""
    if "rest_db" not in rows[0]:
        return []
    base = rows[0]["rest_db"]
    out = [f"  the part's rests ({rows[0]['rests']} of {REST_S * 1000:.0f} ms or more as written): the level in each one's second "
           f"half (of its first {REST_READ_S * 1000:.0f} ms at most) against the level in its notes, dB"]
    for r, n in zip(rows, names):
        d = r.get("rest_db")
        if d is None:
            continue
        says = "as it is" if r["how"] == "as it is" else (
            f"FILLS THE RESTS: {d - base:.1f} dB less of a stop than as it is" if d - base >= FILLS_DB else "")
        out.append(f"  {n:{width}s}{d:+8.1f}" + ("   " + says if says else ""))
    return out


def label(r, width):
    """A row's name in at most `width` characters: "+ " for a layer, the patch (cut with … when long), and its @DB,
    which is never cut (two rows of one long patch differ only there)."""
    head = "+ " if r["how"] == "layer" else ""
    tail = f"@{r['db']:+g}" if r["db"] else ""
    room = width - len(head) - len(tail)
    patch = r["patch"] if len(r["patch"]) <= room else r["patch"][:max(1, room - 1)] + "…"
    return head + patch + tail


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    opt = {"--pin": None, "--keep": None}
    for k in list(opt):
        if k in a and a.index(k) + 1 < len(a):
            i = a.index(k)
            opt[k] = a[i + 1]
            del a[i:i + 2]
    flags = {k: k in a for k in ("--json", "--layer")}
    a = [x for x in a if x not in flags]
    if len(a) < 3 or "-h" in a or "--help" in a:
        print(__doc__)
        return 0 if ("-h" in a or "--help" in a) else 2
    song, track, window = a[0], a[1], a[2]
    cands = [candidate(x) for x in a[3:]]
    path = song if os.path.exists(song) else os.path.join(ROOT, "songs", song + ".yaml")
    if not os.path.exists(path):
        raise SystemExit(f"swapbench: no song {song}")
    tempo = songfmt.load(path).get("tempo", 120)
    if not isinstance(tempo, (int, float)) or isinstance(tempo, bool) or tempo <= 0:
        raise SystemExit("swapbench: the song's tempo changes: only fixed-tempo songs are benched")
    lo, _, hi = window.partition("-")
    ends = [wincut.position(lo, tempo), wincut.position(hi, tempo) if hi else None]
    if ends[0] is None or ends[1] is None or ends[1] <= ends[0]:
        raise SystemExit(f"swapbench: {window}: FROM-TO as chirp render takes positions, as in 63-66 or 248b-264b")
    b0, b1 = (round(s * tempo / 60.0, 4) for s in ends)
    where = opt["--keep"] or tempfile.mkdtemp(prefix="swapbench-")
    os.makedirs(where, exist_ok=True)
    try:
        rows = table(path, track, b0, b1, cands, flags["--layer"], opt["--pin"] or chirpbin.resolve(), where)
    finally:
        if not opt["--keep"]:
            shutil.rmtree(where, True)
    if flags["--json"]:
        print(json.dumps({"song": os.path.basename(path), "track": track, "window": window, "bands": LABELS, "rows": rows}))
        return 0
    if not cands:
        print(f"{os.path.basename(path)} {track} at {window}: the part alone, as it is, through its own effects, bus and master")
        print(f"  {'':16s}" + "".join(s.rjust(8) for s in LABELS))
        print(f"  {'its own shape':16s}" + "".join(f"{v:+8.1f}" for v in rows[0]["own"]) + f"   {rows[0]['patch']}")
        print("  (each band against the part's own total, in dB)")
        if "rest_db" in rows[0]:
            print(f"  its rests ({rows[0]['rests']} of {REST_S * 1000:.0f} ms or more as written): {rows[0]['rest_db']:+.1f} dB against "
                  f"its notes in each one's second half (of its first {REST_READ_S * 1000:.0f} ms at most)")
        return 0
    print(f"{os.path.basename(path)} {track} at {window}: the same notes on other patches, alone through the track's own effects, "
          "bus and master")
    names = [label(r, 44) for r in rows]
    width = min(44, max(16, max(len(n) for n in names)))
    print(f"  {'patch':{width}s}" + "".join(s.rjust(8) for s in LABELS) + "     all  = LUFS")
    for r, n in zip(rows, names):
        first = r["how"] == "as it is"
        cells = [f"{v:+8.1f}" if first or not empty(own, v) else "       ·" for v, own in zip(r["bands"], rows[0]["bands"])]
        print(f"  {n:{width}s}" + "".join(cells)
              + ("        " if first else f"{r['all']:+8.1f}")
              + (f"{'@' + format(r['match_db'], '+.1f'):>8s}" if "match_db" in r else "        ")
              + ("   as it is" if first else ("   " + r["says"] if r["says"] else "")))
    print("  (as it is: each band against the part's own total; a patch: in its place, dB against as it is; + a patch: "
          "layered over it)")
    print("  each patch's own shape (each band against ITS OWN total: where its weight sits):")
    for r, n in zip(rows, names):
        if r["how"] != "layer":
            print(f"  {n:{width}s}" + "".join(f"{v:+8.1f}" for v in r["own"]))
    for line in rest_lines(rows, names, width):
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
