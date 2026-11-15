#!/usr/bin/env python3
"""risset: where a `risset` track's notes really SOUND: every copy's strokes, its speed and its level.
(chirp-eco, 15 Nov, for False Summit, Common Time's fifth song: the tools that read a part's notes from the song
see a risset track's PATTERN, a bar or two written at the track's start, not the copies that play for minutes.)

  risset.py SONG [TRACK ...] [--bars FROM-TO] [--pin CHIRP] [--json]

SONG is a climb ID (songs/ID.yaml) or a song file. For each track with a `risset` (or the ones named): the pattern,
the cycle and the copies; what each copy does over one cycle (its speed against the written tempo, its level:
the slowest enters from silence and the fastest leaves into it); then bar by bar, each copy's strokes, speed and
level. --bars FROM-TO (as `chirp render --from/--to` takes positions: 73-75 is bars 73 and 74): every stroke
that sounds there: where (bar:sixteenth), which copy, its speed, its level in dB, and which note of the pattern.

Levels are each stroke's gain against the note as written, in dB (three copies: -3.5 at a copy's loudest). THE
FADE IS A NOTE GAIN, AHEAD OF THE TRACK'S EFFECTS: on a clean kit it is what you hear; through a saturated amp
it is squashed back up (bd-d08501), and a guitar's copies are better written out on their own tracks with fader
lanes, which this tool then has nothing to say about (tools/endless.py reads those).

As a module, for tools that read notes from the song or from `chirp plan`'s canonical song:
  settings(risset, tempo)   cycle, layers, ratio, total (beats), down, both, pitch, with the engine's defaults
  events(pattern, length, cycle, layers, down, total, ratio)   the engine's own list: (note, beat from the track's
                            start, written length, speed, level, copy)
  sounding(track, tempo)    the track's notes as they sound: copies of the pattern's notes with `at` (the SONG's
                            beat), `len`, `gain` (the written gain times the fade), `copy`, `speed`, `from`
                            (the pattern note's index); the written notes when the track has no risset
It follows the engine (crates/chirp-core/src/lower.rs, `fn risset`, `fn risset_events`): K copies `ratio` of tempo
apart; copy j runs from ratio^(j - K/2) to ratio^(j + 1 - K/2) of the written tempo over each cycle, at level
sin^2(pi (j + u) / K) * 2 / K; at a cycle's end each copy is where the next one starts, so every cycle is the same.
Limits: fixed-tempo songs in 4/4. Read-only. Tests: tools/tests/test_risset.py.
"""
import json
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(HERE)
sys.path.insert(0, HERE)
import warp  # noqa: E402

QUIET = 1e-3           # the engine drops a stroke whose level is under this


def settings(r, tempo):
    """A track's `risset` with the engine's defaults filled in (lengths in beats)."""
    r = r if isinstance(r, dict) else {}
    cycle = warp.beats(r.get("cycle", "4bar"), tempo)
    layers = int(r.get("layers", 3))
    ratio = warp.ratio(r["ratio"]) if r.get("ratio") is not None else 2.0
    if cycle <= 0 or not 2 <= layers <= 6 or not 1.05 <= ratio <= 8:
        raise ValueError("risset: cycle must be positive, layers 2..6, ratio 1.05..8")
    total = warp.beats(r["length"], tempo) if r.get("length") is not None else 4.0 * cycle
    return {"cycle": cycle, "layers": layers, "ratio": ratio, "total": total, "down": bool(r.get("down")),
            "both": bool(r.get("both")), "pitch": bool(r.get("pitch"))}


def pattern(notes, tempo):
    """The written notes as [(at, len)] in beats from the track's start, and the pattern's length."""
    rel = [(warp.beats(n.get("at", 0), tempo), warp.beats(n.get("len", 1), tempo)) for n in notes]
    return rel, max((a + d for a, d in rel), default=0.0)


def events(rel, length, cycle, layers, down, total, ratio):
    """The engine's `risset_events`: [(note index, beat, written length, speed, level, copy)]."""
    k, base = layers, layers / 2.0
    lnr = math.log(ratio)
    scale = [ratio ** (j - base) * cycle / lnr for j in range(k)]
    adv = [a * (ratio - 1.0) for a in scale]
    off = [0.0] * k
    if down:
        for j in range(k - 2, -1, -1):
            off[j] = (off[j + 1] + adv[j + 1]) % length
    else:
        for j in range(1, k):
            off[j] = (off[j - 1] + adv[j - 1]) % length
    out = []
    for cy in range(int(math.ceil(total / cycle - 1e-12))):
        c0 = cy * cycle
        for j in range(k):
            p0, a, sc = off[j], adv[j], scale[j]
            for ni, (at, ln) in enumerate(rel):
                q = at + math.ceil((p0 - at) / length) * length
                while q < p0 + a:
                    x = (q - p0) / sc
                    u = -math.log(1.0 - x / ratio) / lnr if down else math.log(1.0 + x) / lnr
                    q += length
                    t = c0 + u * cycle
                    if u >= 1.0 or t >= total:
                        continue
                    pos = j + 1.0 - u if down else j + u
                    w = math.sin(math.pi * pos / k) ** 2 * 2.0 / k
                    if w < QUIET:
                        continue
                    out.append((ni, t, ln, ratio ** (pos - base), w, j))
    return out


def sounding(track, tempo):
    """A track's notes as they sound (see the module's docstring); the written notes when it has no risset."""
    notes = [n for n in track.get("notes") or [] if isinstance(n, dict)]
    if not track.get("risset"):
        return notes
    s = settings(track["risset"], tempo)
    rel, length = pattern(notes, tempo)
    if length <= 0:
        return []
    origin = warp.beats(track.get("at", 0), tempo)
    out = []
    for down, level in (((False, 0.5), (True, 0.5)) if s["both"] else ((s["down"], 1.0),)):
        for ni, t, ln, f, w, j in events(rel, length, s["cycle"], s["layers"], down, s["total"], s["ratio"]):
            m = dict(notes[ni], at=origin + t, len=max(ln / f, 1e-3), gain=w * level, copy=j, speed=f)
            m["from"] = ni
            if s["pitch"]:
                m["tr"] = float(notes[ni].get("tr", 0) or 0) + 12.0 * math.log2(f)
            out.append(m)
    return sorted(out, key=lambda m: (m["at"], m["copy"]))


def risset_tracks(canon):
    """[track] for every track that has a risset and a name, at any depth."""
    out = []

    def walk(ts):
        for t in ts or []:
            if isinstance(t, dict):
                if t.get("risset") and t.get("name"):
                    out.append(t)
                walk(t.get("tracks"))
    walk(canon.get("tracks"))
    return out


def db(w):
    return 20 * math.log10(max(w, 1e-9))


def table(track, tempo, b0=None, b1=None):
    """Bar by bar: {"bar": n, "copies": {j: {"strokes", "speed": (lo, hi), "level": (lo, hi) dB}}}."""
    rows = {}
    for m in sounding(track, tempo):
        if (b0 is not None and m["at"] < b0) or (b1 is not None and m["at"] >= b1):
            continue
        bar = int(m["at"] // 4) + 1
        c = rows.setdefault(bar, {}).setdefault(m["copy"], {"strokes": 0, "speed": [m["speed"]] * 2, "level": [db(m["gain"])] * 2})
        c["strokes"] += 1
        c["speed"] = [min(c["speed"][0], m["speed"]), max(c["speed"][1], m["speed"])]
        c["level"] = [min(c["level"][0], db(m["gain"])), max(c["level"][1], db(m["gain"]))]
    return [{"bar": b, "copies": rows[b]} for b in sorted(rows)]


def report(track, tempo, span=None):
    s = settings(track["risset"], tempo)
    notes = [n for n in track.get("notes") or [] if isinstance(n, dict)]
    rel, length = pattern(notes, tempo)
    origin = warp.beats(track.get("at", 0), tempo)
    k, r = s["layers"], s["ratio"]
    way = "speeding up and slowing down at once" if s["both"] else "slowing down" if s["down"] else "speeding up"
    print(f"{track['name']}: a Risset rhythm from {warp.place(origin)} for {s['total'] / 4:g} bars: a pattern of {len(notes)} notes in "
          f"{length:g} beats, a cycle of {s['cycle'] / 4:g} bars, {k} copies x{r:g} of tempo apart, {way}"
          + (", pitch moving with speed" if s["pitch"] else ""))
    if length <= 0:
        print("  no pattern: the track has no notes")
        return
    print("  one cycle (every cycle is the same):")
    for j in range(k):
        lo, hi = r ** (j - k / 2.0), r ** (j + 1 - k / 2.0)
        ends = [db(math.sin(math.pi * (j + u) / k) ** 2 * 2.0 / k) for u in (0.02, 0.5, 0.98)]
        if s["down"] and not s["both"]:
            lo, hi, ends = hi, lo, ends[::-1]
        note = "  enters from silence" if ends[0] < -30 else "  leaves into silence" if ends[2] < -30 else ""
        print(f"    copy {j}: x{lo:.2f} -> x{hi:.2f} of the written tempo; "
              f"level {ends[0]:+.1f} -> {ends[1]:+.1f} -> {ends[2]:+.1f} dB{note}")
    rows = table(track, tempo)
    print("  bar by bar (each copy: strokes, speed, level dB):")
    for row in rows:
        cells = []
        for j in range(k):
            c = row["copies"].get(j)
            cells.append("-".ljust(30) if not c else (f"{c['strokes']:3d}  x{c['speed'][0]:.2f}-{c['speed'][1]:.2f}  "
                                                      f"{c['level'][0]:+5.1f}..{c['level'][1]:+5.1f}").ljust(30))
        print(f"    {row['bar']:4d}  " + "  ".join(cells).rstrip())
    if span:
        b0, b1 = span
        hits = [m for m in sounding(track, tempo) if b0 <= m["at"] < b1]
        print(f"  every stroke that sounds in {warp.place(b0)} to {warp.place(b1)} ({len(hits)}):")
        for m in hits:
            print(f"    {warp.place(m['at']):>10s}  copy {m['copy']}  x{m['speed']:.2f}  {db(m['gain']):+6.1f} dB  note {m['from'] + 1} "
                  f"({m.get('pitch', '')})")


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    if not a or "-h" in a or "--help" in a:
        print(__doc__)
        return 0 if a else 2
    pin, bars = None, None
    for flag in ("--pin", "--bars"):
        if flag in a:
            i = a.index(flag)
            if i + 1 >= len(a):
                raise SystemExit(f"risset: {flag} takes a value")
            pin, bars = (a[i + 1], bars) if flag == "--pin" else (pin, a[i + 1])
            del a[i:i + 2]
    as_json = "--json" in a
    if as_json:
        a.remove("--json")
    song, names = a[0], a[1:]
    path = song if os.path.exists(song) else os.path.join(ROOT, "songs", song + ".yaml")
    if not os.path.exists(path):
        raise SystemExit(f"risset: no song {song}")
    if pin is None:
        import chirpbin
        pin = chirpbin.resolve()
    env = {k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"}
    r = subprocess.run([pin, "plan", "-f", path, "--json"], capture_output=True, text=True, env=env)
    try:
        canon = json.loads(r.stdout)["data"]["canonical"]
    except (ValueError, KeyError, TypeError):
        raise SystemExit("risset: the song does not plan: " + (r.stderr or r.stdout).strip()[-300:]) from None
    tempo = canon.get("tempo", 120)
    if not isinstance(tempo, (int, float)) or isinstance(tempo, bool) or tempo <= 0:
        raise SystemExit("risset: the song's tempo changes: only fixed-tempo songs are read")
    tracks = risset_tracks(canon)
    have = [t["name"] for t in tracks]
    for n in names:
        if n not in have:
            raise SystemExit(f"risset: {os.path.basename(path)} has no risset track {n}"
                             + (f" (it has: {', '.join(have)})" if have else ""))
    tracks = [t for t in tracks if not names or t["name"] in names]
    span = None
    if bars is not None:
        ends = bars.split("-")
        try:
            span = [warp.position(t, tempo) for t in ends]
        except ValueError:
            span = []
        if len(span) != 2 or span[1] <= span[0]:
            raise SystemExit("risset: --bars takes FROM-TO as chirp render takes positions (73-75, 288b-296b)")
    if as_json:
        print(json.dumps({"song": os.path.basename(path), "tempo": tempo, "tracks": [
            {"name": t["name"], **settings(t["risset"], tempo), "at": warp.beats(t.get("at", 0), tempo), "bars": table(t, tempo),
             "strokes": [m for m in sounding(t, tempo) if span is None or span[0] <= m["at"] < span[1]]} for t in tracks]}))
        return 0
    if not tracks:
        print(f"{os.path.basename(path)}: no track has a risset (copies written out on their own tracks are read by tools/endless.py)")
        return 0
    print(f"{os.path.basename(path)} ({tempo:g} bpm): where its risset tracks sound")
    for t in tracks:
        report(t, tempo, span)
    return 0


if __name__ == "__main__":
    sys.exit(main())
