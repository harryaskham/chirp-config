#!/usr/bin/env python3
"""warp: where a track's notes really sound when the track has a `warp` (its own clock against the song's), and a
table of how far it has slipped. (chirp-eco, 14 Nov, for Common Time's second song, whose right-hand guitars run on
a warped clock: the tools that read a part's notes from the plan put every one of them on the song's grid.)

  warp.py SONG [TRACK ...] [--at POS ...] [--pin CHIRP]
  warp.py SONG TRACK ... --bars 55-56          (the notes that SOUND in those bars, and where each is WRITTEN)

SONG is a climb ID (songs/ID.yaml) or a song file. For each warped track (or the ones named): every stretch of its
warp, the bars it runs over, and the shift it ends on, in beats, in sixteenths and in milliseconds (minus = ahead of
the song). Tracks with the same warp share one table. --at POS (a bar, 41; beats, 160b; seconds, 76.2s; repeatable):
the shift of each warped track for a note written there.

--bars FROM-TO (as `chirp render --from/--to` takes positions: 55-56 is bar 55): A WARPED PART'S BAR IS NOT WRITTEN
IN THAT BAR. For each warped track, every note that sounds in the range, with where it sounds and where it is
written (bar:sixteenth, both counted from 1 and 0 as the song does), its pitch and the shift; a note written
OUTSIDE the range is marked, and the notes written inside it that sound elsewhere are listed after. To change what
a warped part plays "in bar 55", choose its notes from this table, not by the bar they are written in (chirper-zero,
Odd Sympathy v20: the right guitar's last stab of bar 55 is written in bar 56, in the next section and its key).

As a module, for tools that read notes from `chirp plan`'s canonical song:
  segments(warp, tempo)   the stretches as (start, end, shift at start, shift at end, curve), in beats
  shift(segs, beat)       the shift in beats for a note written at `beat` (from the track's start)
  moved(notes, warp, tempo)   the notes with `at` and `len` as they sound (copies; the same list when there is no warp)
  sounding(notes, warp, tempo, b0, b1)   (the notes that sound in beats b0..b1 with their written place, those written
                              there that sound elsewhere)
It follows the engine (crates/chirp-core/src/lower.rs, `Warp`): stretches run in turn from the track's start; each
moves the shift to `to` (beats, `1bar`, seconds) or holds a `tempo` ratio, over `over`, along `curve` (linear,
smooth, in, out); after the last the shift holds; a note written at b sounds at b + shift(b) and ends at
(b + len) + shift(b + len). Notes move; the track's automation stays on the song's clock.
Limits: fixed-tempo songs in 4/4, tracks that start at the song's top (no embedded songs). notechk.py, hitpoke.py and
holds.py use it. Read-only. Tests: tools/tests/test_warp.py.
"""
import json
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CURVES = {
    "linear": lambda x: x,
    "smooth": lambda x: 0.5 - 0.5 * math.cos(math.pi * x),
    "in": lambda x: x * x,
    "out": lambda x: 1.0 - (1.0 - x) * (1.0 - x),
}


def beats(value, tempo):
    """A length or a shift in beats: a number (beats), "96b", "8bar", "1.5s", "200ms" (4/4, one tempo)."""
    if isinstance(value, bool):
        raise ValueError(f"not a length: {value!r}")
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).strip()
    for suffix, scale in (("bars", 4.0), ("bar", 4.0), ("ms", tempo / 60000.0), ("s", tempo / 60.0), ("b", 1.0)):
        if s.endswith(suffix):
            return float(s[:-len(suffix)]) * scale
    return float(s)


def ratio(value):
    """A tempo ratio: 1.03, or "3:4"."""
    if isinstance(value, str) and ":" in value:
        a, b = value.split(":", 1)
        return float(a) / float(b)
    return float(value)


def segments(warp, tempo):
    """[(start beat, end beat, shift at start, shift at end, curve name)] for a track's `warp` list."""
    b = d = 0.0
    out = []
    for i, s in enumerate(warp or []):
        over = beats(s.get("over", "4bar"), tempo)
        if not (math.isfinite(over) and over > 0):
            raise ValueError(f"warp[{i}].over must be positive")
        curve = s.get("curve") or "linear"
        if curve not in CURVES:
            raise ValueError(f"warp[{i}].curve {curve!r}: linear, smooth, in or out")
        if s.get("to") is not None:
            to = beats(s["to"], tempo)
        elif s.get("tempo") is not None:
            to = d + over * (1.0 / ratio(s["tempo"]) - 1.0)      # a track at r times the tempo plays `over` beats in over / r
        else:
            to = d
        out.append((b, b + over, d, to, curve))
        b += over
        d = to
    return out


def shift(segs, x):
    """The shift in beats for a note written at beat x from the track's start: 0 before the first stretch, held after
    the last."""
    if not segs:
        return 0.0
    if x >= segs[-1][1]:
        return segs[-1][3]
    for b0, b1, d0, d1, curve in segs:
        if x < b1:
            if x <= b0:
                return d0
            return d0 + (d1 - d0) * CURVES[curve]((x - b0) / (b1 - b0))
    return segs[-1][3]


def moved(notes, warp, tempo):
    """The notes as they sound: copies with `at` and `len` (beats) moved by the track's warp; `notes` itself when the
    track has none. A note's end moves by the shift where it ends, so a note across a slip is a little shorter or longer."""
    if not warp:
        return notes
    segs = segments(warp, tempo)
    out = []
    for n in notes:
        at = float(n.get("at") or 0)
        end = at + float(n.get("len") or 0)
        at2 = at + shift(segs, at)
        out.append(dict(n, at=at2, len=end + shift(segs, end) - at2))
    return out


def sounding(notes, warp, tempo, b0, b1):
    """(inside, strays) for the beats b0..b1: `inside` the notes that SOUND there, in the order they sound, each
    {"sounds", "written" (beats), "shift" (beats), "pitch", "out" (True when it is written outside b0..b1)}; `strays`
    the notes written there that sound elsewhere, in the same form."""
    segs = segments(warp, tempo) if warp else []
    rows = []
    for n in notes:
        at = float(n.get("at") or 0)
        d = shift(segs, at) if segs else 0.0
        rows.append({"sounds": at + d, "written": at, "shift": d, "pitch": n.get("pitch")})
    eps = 1e-6
    inside = sorted((dict(r, out=not b0 - eps <= r["written"] < b1 - eps) for r in rows if b0 - eps <= r["sounds"] < b1 - eps),
                    key=lambda r: (r["sounds"], str(r["pitch"])))
    strays = sorted((r for r in rows if b0 - eps <= r["written"] < b1 - eps and not b0 - eps <= r["sounds"] < b1 - eps),
                    key=lambda r: (r["sounds"], str(r["pitch"])))
    return inside, strays


def place(beat):
    """A beat as bar:sixteenth, "55:13.00" (bars from 1, sixteenths from 0, in 4/4)."""
    beat = round(beat, 6)
    return f"{int(beat // 4) + 1}:{(beat % 4) * 4:05.2f}"


def notes_of(canon, name):
    """A track's notes as written, at any depth ([] when it has none)."""
    def walk(ts):
        for t in ts or []:
            if isinstance(t, dict):
                if t.get("name") == name:
                    return [n for n in t.get("notes") or [] if isinstance(n, dict)]
                got = walk(t.get("tracks"))
                if got is not None:
                    return got
        return None
    return walk(canon.get("tracks")) or []


def warped_tracks(canon):
    """[(name, warp)] for every track that has one, at any depth."""
    out = []

    def walk(ts):
        for t in ts or []:
            if isinstance(t, dict):
                if t.get("warp") and t.get("name"):
                    out.append((t["name"], t["warp"]))
                walk(t.get("tracks"))
    walk(canon.get("tracks"))
    return out


def position(tok, tempo):
    """A `chirp render --from` position in beats: a bar (49, 1-indexed, in 4/4), beats (12b) or seconds (30s)."""
    s = tok.strip()
    if s.endswith("s"):
        return float(s[:-1]) * tempo / 60.0
    if s.endswith("b"):
        return float(s[:-1])
    return (float(s) - 1) * 4


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    if not a or "-h" in a or "--help" in a:
        print(__doc__)
        return 0 if a else 2
    pin, ats, bars = None, [], None
    if "--bars" in a:
        i = a.index("--bars")
        bars = a[i + 1] if i + 1 < len(a) else ""
        del a[i:i + 2]
    while "--pin" in a:
        i = a.index("--pin")
        pin = a[i + 1]
        del a[i:i + 2]
    while "--at" in a:
        i = a.index("--at")
        ats.append(a[i + 1])
        del a[i:i + 2]
    song, names = a[0], a[1:]
    path = song if os.path.exists(song) else os.path.join(ROOT, "songs", f"{song}.yaml")
    if not os.path.exists(path):
        raise SystemExit(f"warp: no song {song!r} (a climb ID or a file)")
    if not pin:
        with open(os.path.join(HERE, "groove-pin")) as f:
            pin = f.read().strip()
    env = dict(os.environ)
    env.pop("LD_LIBRARY_PATH", None)
    r = subprocess.run([pin, "plan", "-f", path, "--json"], capture_output=True, text=True, env=env)
    try:
        d = json.loads(r.stdout)
        canon = (d.get("data") or d).get("canonical") or {}
    except ValueError:
        raise SystemExit(f"warp: chirp plan failed: {r.stderr.strip()[-300:]}") from None
    tempo = canon.get("tempo", 120.0)                        # the plan leaves out a tempo of 120, the engine's default
    if not isinstance(tempo, (int, float)) or isinstance(tempo, bool) or tempo <= 0:
        raise SystemExit("warp: this song's tempo changes; warp.py reads fixed-tempo songs only")
    tracks = warped_tracks(canon)
    if names:
        missing = [n for n in names if n not in dict(tracks)]
        if missing:
            raise SystemExit(f"warp: no warped track {', '.join(missing)} (warped: {', '.join(n for n, _ in tracks) or 'none'})")
        tracks = [(n, w) for n, w in tracks if n in names]
    if not tracks:
        print("no track has a warp")
        return 0
    ms = 60000.0 / tempo
    if bars is not None:                                      # the notes that sound in a range, and where each is written
        lo, _, hi = bars.partition("-")
        try:
            b0, b1 = position(lo, tempo), position(hi, tempo)
        except ValueError:
            b0 = b1 = 0.0
        if not hi or b1 <= b0:
            raise SystemExit(f"warp: --bars {bars}: FROM-TO as chirp render takes positions (55-56 is bar 55)")
        for name, w in tracks:
            inside, strays = sounding(notes_of(canon, name), w, tempo, b0, b1)
            out = sum(1 for r in inside if r["out"])
            print(f"{name}: {len(inside)} note(s) SOUND in {bars} (bar:sixteenth); {out} of them written outside it")
            print(f"  {'sounds':>10s}  {'written':>10s}  {'pitch':10s} {'shift':>12s}")
            for r in inside:
                print(f"  {place(r['sounds']):>10s}  {place(r['written']):>10s}  {str(r['pitch']):10s} {r['shift'] * 4:+7.2f} 16ths"
                      + (f"   WRITTEN IN BAR {int(r['written'] // 4) + 1}" if r["out"] else ""))
            if strays:
                print(f"  written in {bars} but sounding elsewhere: "
                      + ", ".join(f"{r['pitch']} written {place(r['written'])} sounds {place(r['sounds'])}" for r in strays))
        return 0
    groups = {}
    for name, w in tracks:
        groups.setdefault(json.dumps(w, sort_keys=True), (w, []))[1].append(name)
    for w, group in groups.values():
        segs = segments(w, tempo)
        print(f"{', '.join(group)}  (tempo {tempo:g}; minus = ahead of the song)")
        print(f"  {'bars':>15s}  {'curve':6s}  {'ends':>8s} {'16ths':>7s} {'ms':>8s}")
        for b0, b1, d0, d1, curve in segs:
            how = "hold" if d1 == d0 else curve
            print(f"  {b0 / 4 + 1:7.2f}-{b1 / 4 + 1:7.2f}  {how:6s}  {d1:+8.3f} {d1 * 4:+7.2f} {d1 * ms:+8.1f}")
        for tok in ats:
            x = position(tok, tempo)
            s = shift(segs, x)
            print(f"  at {tok}: {s:+.3f} beats, {s * 4:+.2f} sixteenths, {s * ms:+.1f} ms")
    return 0


if __name__ == "__main__":
    sys.exit(main())
