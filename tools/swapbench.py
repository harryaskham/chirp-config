#!/usr/bin/env python3
"""swapbench: SWAP OR LAYER? The same notes of a part on other patches, alone through the part's own routing.
(chirp-eco, 14 Nov, for chirper-zero's finding on Plain Hunt v3: "swap or layer is a measurement, not a taste". A
fuzz bass, on its own through the bass's bus, had 7 dB less under 60 Hz and 3 dB less at 60-120 Hz than the bass it
would have replaced: as a swap it would have thinned half the song, as a layer it added the teeth. He measured that by
hand with an FFT; this is that as one command.)

  swapbench.py SONG TRACK FROM-TO PATCH[@DB] [PATCH[@DB] ...] [--layer] [--pin CHIRP] [--keep DIR] [--json]
  chirpers.py palette ID --bench TRACK FROM-TO PATCH[@DB] ... [--layer]        (the same, from the palette brief)

SONG is an id (songs/ID.yaml) or a file; TRACK the part; FROM-TO the bars it plays, as `chirp render --from/--to`
take positions (63-66, 248b-264b); each PATCH a patch as a song names one (a library name, with overrides if
wanted: "bass-fuzz fx.0.shape=wavefold"; or one of the song's own `patches:`). @DB puts that many dB more of it
into the track's bus (bass-fuzz@+4, pad@-6): a `gain` at the end of the track's own effects.
The bench is the song with every other track's notes out, so the track's own effects, its bus, its sends and the
master are the song's (loudness off, seed 0), and the part's notes in the window as written.
Prints the nine bands tools/stembal.py reads (under 60 Hz to 8-16 kHz) and the whole:
  as it is        the part on its present patch, each band against its own total
  PATCH           that patch IN ITS PLACE, in dB against as it is (same notes, same routing, same fader)
  + PATCH         with --layer: that patch OVER the present one (a second track beside it), against as it is
and what the rows say:
  LOSES ...       a swap takes 3 dB or more out of a band the part holds (within 15 dB of its own total): what a
                  layer would keep
  NOT THERE       a layer moves no band by 0.5 dB: it is under its own part (raise it, PATCH@+4, and read again)
A band where neither patch has anything (60 dB under the part's total, and still 45 under with the new patch) is
printed as a dot: its difference is noise. (--json keeps the number.)
What it cannot say: how either sounds; what the rest of the band covers (tools/presence.py against the part it
layers, tools/stembal.py --parts); what a bus compressor keyed by other tracks would do. A layer here goes where
the track goes; a layer on another bus is the song's to try.
--keep DIR keeps each bench song and render. --pin: the chirp binary (else $CHIRP, else the groove's pin).
Read-only. Tests: tools/tests/test_swapbench.py.
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
import songfmt  # noqa: E402
import wincut  # noqa: E402

LABELS = keybench.LABELS
HOLDS_DB = -15.0      # a band the part "holds": within this of its own total
LOSES_DB = -3.0       # a swap that takes this much out of such a band loses it
THERE_DB = 0.5        # a layer that moves no band by this much is not there
EMPTY_DB = (-60.0, -45.0)   # a band this far under the part's total, and still this far under on the new patch, is empty


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


def table(song, track, b0, b1, cands, layer, pin, where):
    """[{patch, db, how ("as it is" | "swap" | "layer"), bands, all, says}] for the track's notes in beats b0..b1."""
    doc = songfmt.load(song)
    try:
        bench = keybench.bench(doc, [track], b0, b1, 0)
    except KeyError as e:
        raise SystemExit(f"swapbench: {os.path.basename(song)} has no track {e.args[0]}") from None
    spot = find(doc.get("tracks"), track)
    now = spot[0][spot[1]].get("patch")
    if not isinstance(now, str):
        now = "(its own inline patch)"
    base = keybench.band_levels(keybench.render(bench, pin, where, "", b0, b1))
    own = [round(v - base[-1], 1) for v in base[:-1]]
    rows = [{"patch": now, "db": 0.0, "how": "as it is", "bands": own, "all": 0.0, "says": ""}]
    n = 0
    for patch, db in cands:
        for how in ("swap", "layer") if layer else ("swap",):
            n += 1
            try:
                got = keybench.band_levels(keybench.render(with_patch(bench, track, patch, db, how == "layer"), pin, where,
                                                           f"-{n}", b0, b1))
            except SystemExit as e:
                raise SystemExit(str(e).replace("keybench:", f"swapbench: {patch}:")) from None
            row = {"patch": patch, "db": db, "how": how, "bands": [round(v - b, 1) for v, b in zip(got[:-1], base[:-1])],
                   "all": round(got[-1] - base[-1], 1)}
            row["says"] = reading(row, own)
            rows.append(row)
    return rows


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
    if len(a) < 4 or "-h" in a or "--help" in a:
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
    print(f"{os.path.basename(path)} {track} at {window}: the same notes on other patches, alone through the track's own effects, "
          "bus and master")
    names = [("+ " if r["how"] == "layer" else "") + r["patch"] + (f"@{r['db']:+g}" if r["db"] else "") for r in rows]
    width = min(44, max(16, max(len(n) for n in names)))
    print(f"  {'patch':{width}s}" + "".join(s.rjust(8) for s in LABELS) + "     all")
    for r, n in zip(rows, names):
        first = r["how"] == "as it is"
        cells = [f"{v:+8.1f}" if first or not empty(own, v) else "       ·" for v, own in zip(r["bands"], rows[0]["bands"])]
        print(f"  {(n if len(n) <= width else n[:width - 1] + '…'):{width}s}" + "".join(cells)
              + ("        " if first else f"{r['all']:+8.1f}")
              + ("   as it is" if first else ("   " + r["says"] if r["says"] else "")))
    print("  (as it is: each band against the part's own total; a patch: in its place, dB against as it is; + a patch: "
          "layered over it)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
