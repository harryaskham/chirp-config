#!/usr/bin/env python3
"""ctgen: Common Time's film, written from the songs themselves.

    ctgen.py                 write ../film/chirpers10-tN.yaml for every song of the album
    ctgen.py 3 7             only those tracks
    ctgen.py --plan 3        print what it found in the song and what it chose, write nothing
    ctgen.py --out=DIR …     write the programmes to DIR instead of ../film/
    ctgen.py --reel=N:A:B[:E]  a sampler: song N from bar A to bar B with a scene every E bars
                             (4), each a different study; writes chirpers10-tN-reel.yaml

The songs are still being written, so nothing here is fixed to a bar by hand. For each song the
generator reads the notes (tools/songmap.py: `chirp plan` and a MIDI render), and works out:
  - what each track is (a riff, the bass, a drum, a tune, a voice), from its notes alone;
  - each track's CELL bar by bar (the length of its repeating riff in sixteenths: the same
    reading the engine gives the picture as `track.T.cell`);
  - where the music runs a long cycle right round (parts of different lengths together for as
    long as they take to come round): such a round is one scene, to the sixteenth, and the
    longest are tied as knots;
  - where else the song changes (who plays, and which cells), which is where the scenes change;
  - which study fits each stretch (studies.py), never the same one twice running.
Run it again whenever a song changes: the programme follows.
"""
import collections
import hashlib
import itertools
import json
import math
import os
import pickle
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(CFG, "tools"))
sys.path.insert(0, HERE)
import songmap  # noqa: E402
import studies as S  # noqa: E402

ALBUM = json.load(open(os.path.join(HERE, "..", "album.json")))
CACHE = os.path.expanduser("~/.cache/chirp/ctgen")
# Where the programmes go. Not vis/ yet: they use engine features (cells, plates) that are on
# the chirp-video branch only, and vis/ is read by every released binary. --out=DIR overrides.
OUT = os.path.join(HERE, "..", "film")

# One spot colour a song: signal lamps, never two neighbours alike.
SPOTS = ["#ff5a2a", "#ffb000", "#39c5ff", "#ff3d6e", "#7dff6a", "#ff7a00", "#b28cff", "#00d6a8", "#ffd23c",
         "#ff4040", "#4aa8ff", "#ff9ec4", "#c8ff3c", "#ff6a3d", "#5ce0ff", "#ffb86a", "#ff5a2a"]

# Which songs are printed as negatives (black figures on the pale wall): never three alike in a row.
# The longest riff a picket fence can hold at draft size (720p: a strip is two pixels). At 4K
# the strips are three times finer on the horse: raise this to 16.
FENCE_MAX = 9
WHITE = {2, 5, 7, 10, 12, 14, 17}

DRUM_WORDS = ("kick", "snare", "tom", "cym", "hat", "ride", "foot", "skin", "metal", "rim", "chest", "tabla", "clave", "shaker",
              "block", "knock", "wood", "tick", "palmas", "drum", "kettle", "log", "gourd", "struck", "feet", "china", "crash")


# The engine that will draw the film: asked for each track's cells (`chirp vis cells`), so the
# generator deals by what the picture will find. $CHIRP, else the chirp-video build.
CHIRP = os.environ.get("CHIRP") or next((p for p in (
    os.path.expanduser("~/.local/state/pi-daemon/worktrees/tools/chirp-video/cli/chirp/target/release/chirp"),
    "/tmp/cv/ct/bin/chirp") if os.path.exists(p)), "chirp")


def engine_cells(song):
    """Each track's cells as the engine reads them: {track: [(from, to, cell)]} in sixteenths
    from the song's start. None if this engine cannot say (then the reading below is used: the
    same method, but on the written notes, where the engine has the played ones)."""
    path = os.path.join(CFG, "songs", song + ".yaml")
    os.makedirs(CACHE, exist_ok=True)
    try:
        stamp = f"{os.path.getmtime(CHIRP):.0f}"
    except OSError:
        stamp = "path"
    key = hashlib.sha1(open(path, "rb").read() + stamp.encode()).hexdigest()[:16]
    c = os.path.join(CACHE, f"{song}-cells-{key}.json")
    if os.path.exists(c):
        return json.load(open(c))
    try:
        r = subprocess.run([CHIRP, "--json", "vis", "cells", "-f", path], capture_output=True, text=True, timeout=600, cwd=os.path.join(CFG, "songs"))
        data = json.loads(r.stdout)["data"]["tracks"]
    except (OSError, ValueError, KeyError, subprocess.TimeoutExpired):
        return None
    out = {t["name"]: [(sp["from"], sp["to"], sp["cell"]) for sp in t["spans"]] for t in data}
    for old in os.listdir(CACHE):
        if old.startswith(song + "-cells-") and old != os.path.basename(c):
            os.remove(os.path.join(CACHE, old))
    json.dump(out, open(c, "w"))
    return out


def load(song):
    """The song's notes: {track: [(start beat, end beat, key)]}, seconds, beats a bar, tempo."""
    path = os.path.join(CFG, "songs", song + ".yaml")
    os.makedirs(CACHE, exist_ok=True)
    key = hashlib.sha1(open(path, "rb").read()).hexdigest()[:16]
    c = os.path.join(CACHE, f"{song}-{key}.pkl")
    if os.path.exists(c):
        return pickle.load(open(c, "rb"))
    data, ppq, tempo, metre, notes = songmap.load(song)
    clk = songmap.Clock(ppq, tempo, metre)
    canon = {t.get("name"): t for t in (data["canonical"].get("tracks") or []) if isinstance(t, dict)}
    out = {
        "seconds": data["seconds"], "bar_beats": clk.bar_beats, "bpm": 60 / clk.pts[0][2],
        "notes": {name: [(n[0] / ppq, n[1] / ppq, n[2]) for n in ns] for name, ns in notes.items()},
        "sung": {name for name, t in canon.items() if any(isinstance(n, dict) and n.get("ph") for n in (t.get("notes") or []))},
    }
    for old in os.listdir(CACHE):
        if old.startswith(song + "-") and old != os.path.basename(c):
            os.remove(os.path.join(CACHE, old))
    pickle.dump(out, open(c, "wb"))
    return out


def cell_of(grid, lo, hi, longest=48):
    """As the engine's cells.rs: the shortest shift under which the pattern lands on itself."""
    if sum(1 for s in range(lo, hi) if s in grid) < 6:
        return None
    sc = {}
    for p in range(2, longest + 1):
        if hi - lo < 2 * p:
            break
        m = n = 0
        for s in range(lo, hi - p):
            a, b = grid.get(s), grid.get(s + p)
            if a is None and b is None:
                continue
            n += 1
            if a is not None and a == b:
                m += 1
        if n:
            sc[p] = m / n
    if not sc:
        return None
    top = max(sc.values())
    if top < 0.5:
        return None
    clear = max(0.62, top - 0.25)
    for p in sorted(sc):
        if sc[p] >= clear:
            return p, sc[p]
    for p in sorted(sc):
        if sc[p] >= top - 0.04:
            return p, sc[p]


class Track:
    def __init__(self, name, notes, sung, bars, bar_steps, spans=None):
        self.name, self.notes, self.sung = name, notes, sung
        self.spans = sorted(spans or [])
        keys = [n[2] for n in notes]
        self.lo, self.hi = min(keys), max(keys)
        self.med = sorted(keys)[len(keys) // 2]
        self.distinct = len(set(keys))
        # Notes in each bar, and the grid of sixteenths.
        self.per_bar = [0] * bars
        self.grid = {}
        self.steps_in_bar = collections.defaultdict(set)
        for a, _, k in notes:
            b = int(a * 4 // bar_steps)
            if 0 <= b < bars:
                self.per_bar[b] += 1
            x = a * 4
            s = round(x)
            if abs(x - s) <= 0.2:
                self.grid[s] = min(self.grid.get(s, 999), k)
                self.steps_in_bar[int(s // bar_steps)].add(s)
        # The cell bar by bar (16 steps at a time, as the engine reads it).
        self.cells = [None] * bars
        if spans is not None:
            # The engine's own reading: the cell it has through most of each bar.
            for b in range(bars):
                lo, got = b * bar_steps, collections.Counter()
                for a, z, c in spans:
                    got[c] += max(0, min(z, lo + bar_steps) - max(a, lo))
                if got and got.most_common(1)[0][1] >= bar_steps / 2:
                    self.cells[b] = got.most_common(1)[0][0]
        for b in range(bars):
            if spans is not None or not self.per_bar[b]:
                continue
            lo = b * 16
            best = cell_of(self.grid, lo - 64, lo + 64)
            for c in (cell_of(self.grid, lo, lo + 128), cell_of(self.grid, lo + 16 - 128, lo + 16)):
                if c and (best is None or c[1] > best[1] + 0.05):
                    best = c
            self.cells[b] = best[0] if best else None
        low = name.lower()
        drumish = any(w in low for w in DRUM_WORDS) or (self.distinct <= 2 and len(notes) >= 24)
        if sung:
            self.role = "voice"
        elif drumish:
            self.role = "drum"
        elif "bass" in low:
            self.role = "bass"
        elif self.lo <= 45 and self.med <= 52 and len(notes) >= 48:
            self.role = "riff"
        elif self.med >= 55 and len(notes) >= 10:
            self.role = "tune"
        else:
            self.role = "other"

    def count(self, a, b):
        return sum(self.per_bar[a:b])

    def cover(self, a, b):
        """The share of bars a..b it plays in."""
        return sum(1 for n in self.per_bar[a:b] if n) / max(b - a, 1)

    def cell(self, a, b):
        """The cell it mostly has over bars a..b (None: none), and for how much of its playing."""
        got = collections.Counter(c for c, n in zip(self.cells[a:b], self.per_bar[a:b]) if n)
        if not got:
            return None, 0.0
        c, n = got.most_common(1)[0]
        return c, n / sum(got.values())

    def hold(self, cell, lo, hi):
        """The longest stretch within sixteenths lo..hi through which it keeps this cell (the
        engine's spans of it, joined where less than a bar apart), or None."""
        runs = []
        for a, z, c in self.spans:
            if c != cell or z <= lo or a >= hi:
                continue
            a, z = max(a, lo), min(z, hi)
            if runs and a - runs[-1][1] <= 16:
                runs[-1][1] = z
            else:
                runs.append([a, z])
        return max(runs, key=lambda r: r[1] - r[0], default=None)

    def sig(self, a, b):
        return frozenset(s for bar in range(a, b) for s in self.steps_in_bar.get(bar, ()))


def analyse(song):
    d = load(song)
    bar_steps = int(round(d["bar_beats"] * 4))
    last = max(n[1] for ns in d["notes"].values() for n in ns)
    bars = int(last // d["bar_beats"]) + 1
    found = engine_cells(song)
    tracks = [Track(name, ns, name in d["sung"], bars, bar_steps, None if found is None else found.get(name, []))
              for name, ns in d["notes"].items() if ns]
    d["engine"] = found is not None
    return d, bars, tracks


def sections(bars, tracks, short=8, long=28):
    """Where the scenes change: where who plays changes, or a leading riff's cell does."""
    main = [t for t in tracks if len(t.notes) >= 12]

    def state(b):
        who = frozenset(t.name for t in main if t.per_bar[b])
        cells = frozenset((t.name, t.cells[b]) for t in main if t.role in ("riff", "bass") and t.per_bar[b] and t.cells[b])
        return who, cells

    def dist(a, b):
        (wa, ca), (wb, cb) = a, b
        u = len(wa | wb) or 1
        d = len(wa ^ wb) / u
        if ca != cb and (ca or cb):
            d += 0.35
        return d

    states = [state(b) for b in range(bars)]
    # A bar is a boundary when the two bars after it differ enough from the two before.
    score = [0.0] * bars
    for b in range(2, bars - 1):
        before = (states[b - 1][0] | states[b - 2][0], states[b - 1][1] | states[b - 2][1])
        after = (states[b][0] | states[b + 1][0], states[b][1] | states[b + 1][1])
        score[b] = dist(before, after)
    cuts = [0]
    order = sorted(range(bars), key=lambda b: -score[b])
    chosen = set()
    for b in order:
        if score[b] < 0.3:
            break
        if all(abs(b - c) >= short for c in chosen | {0, bars}):
            chosen.add(b)
    cuts += sorted(chosen)
    if long is None:        # the music's own sections, uncut
        return list(zip(cuts, cuts[1:] + [bars]))
    out = []
    for a, b in zip(cuts, cuts[1:] + [bars]):
        out += [x for x, _ in recut(a * 16, b * 16, long)]
    out = sorted(set(x // 16 for x in out))
    return list(zip(out, out[1:] + [bars]))


def recut(a, b, long):
    """A long stretch (sixteenths a..b) cut again every `long` bars or so, on four-bar lines
    from its start, so the picture keeps changing."""
    n = max(1, round((b - a) / 16 / long))
    step = (b - a) / n
    at = sorted({a} | {a + int(round(i * step / 64)) * 64 for i in range(1, n)})
    at = [x for x in at if x < b]
    return list(zip(at, at[1:] + [b]))


COMMON = (2, 4, 8, 16, 32)

# How long before its cut each study's camera is started (needs chirp-video 7c0e1799; an
# engine without `lead` refuses the programme). The strip of a photo-finish is two bars long.
# The knot, the lamp, the gears and the daylight track keep nothing: they need none.
LEAD = {"finish": "2bar", "sheet": "2bar", "fence": "1bar", "wheels": "1bar", "discs": "2b", "walkers": "1bar",
        "pendulums": "1bar", "balls": "1bar", "flight": "1bar"}


def find_cycles(tracks, bars, bar_s):
    """Where the music runs a long cycle right round: two or three parts, each keeping a cell
    of a different length (at most one of them plain common time), together for at least as
    long as those lengths take to come round together: their least common multiple, where
    that is a real wait (nine seconds to about a minute) and longer than any one of them.

    Returns rounds that do not overlap, the longest waits first chosen:
    [(first sixteenth, last, sixteenths a round, how many rounds, tracks, cells)], in order."""
    rank = {"riff": 0, "bass": 1, "tune": 2, "other": 2, "voice": 3, "drum": 4}
    # Each part's stretches of one cell (a bar or less apart joined), where it plays a note a
    # bar at least; doubles (the same cell over the same bars) are one part, the foremost.
    best = {}
    for t in tracks:
        runs = []
        for a, z, c in t.spans:
            if c < 3:
                continue
            if runs and runs[-1][2] == c and a - runs[-1][1] <= 16:
                runs[-1][1] = z
            else:
                runs.append([a, z, c])
        for a, z, c in runs:
            if z - a < 64 or t.count(a // 16, -(-z // 16)) < (z - a) / 16:
                continue
            # Ends within two sixteenths of a bar line are the bar line.
            a, z = (round(x / 16) * 16 if abs(x - round(x / 16) * 16) <= 2 else x for x in (a, z))
            key = (c, a // 16, z // 16)
            mine = (rank.get(t.role, 3), -len(t.notes))
            if key not in best or mine < best[key][0]:
                best[key] = (mine, t, a, z, c)
    held = sorted((a, z, c, t) for _, t, a, z, c in best.values())
    found = []

    def consider(combo):
        cells = [c for _, _, c, _ in combo]
        if len(set(cells)) < len(cells) or sum(1 for c in cells if c in COMMON) > 1 or len({t.name for *_, t in combo}) < len(combo):
            return
        round_ = math.lcm(*cells)
        if round_ in cells or not 9 <= round_ / 16 * bar_s <= 64:
            return
        s0, s1 = max(x[0] for x in combo), min(x[1] for x in combo)
        if s1 - s0 < 0.92 * round_:
            return
        if s1 - s0 >= round_:
            n = int((s1 - s0) / round_ + 0.02)
        else:           # not quite a round together: it is timed to close as they stop
            s0, n = max(0, s1 - round_), 1
        drums = sum(1 for *_, t in combo if t.role == "drum")
        found.append(((round_, -drums, len(combo)), s0, s0 + n * round_, round_, n, [t for *_, t in combo], cells))

    for i, x in enumerate(held):
        for j in range(i + 1, len(held)):
            y = held[j]
            if y[0] >= x[1] - 64:
                break
            if min(x[1], y[1]) - y[0] < 64:
                continue
            consider((x, y))
            for z in held[j + 1:]:
                if z[0] >= min(x[1], y[1]) - 64:
                    break
                if min(x[1], y[1], z[1]) - z[0] >= 64:
                    consider((x, y, z))
    taken = []
    for _, a, z, round_, n, ts, cells in sorted(found, key=lambda f: f[0], reverse=True):
        if all(z <= p[0] or a >= p[1] for p in taken):
            taken.append((a, z, round_, n, ts, cells))
    return sorted(taken)


def distinct(tracks, a, b):
    """Drop doubles: tracks that play the same rhythm as one already kept."""
    kept = []
    for t in tracks:
        s = t.sig(a, b)
        if not s:
            continue
        if any(len(s & k.sig(a, b)) >= 0.85 * max(len(s), len(k.sig(a, b))) for k in kept):
            continue
        kept.append(t)
    return kept


def choose(n, title, song, reel=None):
    d, bars, tracks = analyse(song)
    spot = SPOTS[(n - 1) % len(SPOTS)]
    # A scene lasts about 26 seconds: so many bars at this song's tempo, in fours.
    bar_s = d["bar_beats"] * 60 / d["bpm"]
    long = int(min(16, max(8, round(26 / bar_s / 4) * 4)))
    common = lambda c: c in COMMON  # noqa: E731

    def cast(a, b):
        """Who plays in bars a..b: (by_notes, riffs, drums, tunes, others, cand), `cand` being
        those that carry a cell, best first."""
        # In most of its bars, and from near its start (a plate should not stand empty while
        # its subject waits to come in).
        act = [t for t in tracks if t.count(a, b) >= 4 and t.cover(a, b) >= 0.5 and t.count(a, min(a + 3, b))]
        if not act:
            act = [t for t in tracks if t.count(a, b) >= 4]
        by_notes = sorted(act, key=lambda t: -t.count(a, b))
        riffs = distinct([t for t in by_notes if t.role in ("riff", "bass")], a, b)
        drums = [t for t in by_notes if t.role == "drum"]
        tunes = distinct([t for t in by_notes if t.role in ("tune", "voice")], a, b)
        others = distinct([t for t in by_notes if t.role == "other"], a, b)
        # A part has a cell here if it keeps one through most of its playing, plays it in
        # about half the bars at least, and plays a note a bar or more (a plate built on a
        # part that is hardly there stands empty).
        held = lambda t: sum(1 for k in range(a, b) if t.per_bar[k] and t.cells[k] == t.cell(a, b)[0]) / (b - a)  # noqa: E731
        celled = lambda t: (t.cell(a, b)[0] is not None and t.cell(a, b)[1] >= 0.5 and held(t) >= 0.45 and t.count(a, b) >= b - a)  # noqa: E731
        # Who carries a cell: the riffs first, then any other part with an odd one (a clean
        # tick, a harp), then the kick and the kit.
        oddones = [t for t in distinct(tunes + others, a, b) if celled(t) and not common(t.cell(a, b)[0])]
        cand = [t for t in riffs if celled(t)] + oddones + [t for t in drums if celled(t)]
        return by_notes, riffs, drums, tunes, others, cand

    # Where the scenes are (first and last sixteenth, and the cycle it is one round of).
    # The music's own sections first. Where a section runs a long cycle right round, a scene
    # is that round exactly, to the sixteenth: the plate lasts as long as its cycle, and is
    # changed when everything on it has come round together. The rest is cut every so many
    # bars, so the picture keeps changing.
    lay = []
    if reel:
        # A sampler: a scene every so many bars through one stretch of the song.
        first, end, every = reel
        lay = [[a * 16, min(a + every, end) * 16, None] for a in range(first, min(end, bars), every)]
    else:
        rounds = find_cycles(tracks, bars, bar_s) if d["engine"] else []
        # The longest rounds are tied as knots (see studies.loops): up to a fifth of the song,
        # never two running. Another round is a scene of its own if it is not too long for
        # any study to hold; if it is, that stretch is cut as usual.
        budget, knots = 0.2 * bars * 16, []
        for r in sorted(rounds, key=lambda r: -r[2]):
            i = rounds.index(r)
            near = [rounds[j] for j in (i - 1, i + 1) if 0 <= j < len(rounds) and (rounds[j][1] == r[0] or rounds[j][0] == r[1])]
            # (The same lengths tie the same knot: not again within thirty-two bars.)
            again = any(sorted(x[5]) == sorted(r[5]) and min(abs(x[0] - r[1]), abs(r[0] - x[1])) < 32 * 16 for x in knots)
            if r[2] <= budget and not again and not any(x in knots for x in near):
                knots.append(r)
                budget -= r[2]
        cuts = [a * 16 for a, _ in sections(bars, tracks, short=max(4, long // 2), long=None)] + [bars * 16]
        at = 0

        def fill(x, y):
            """The stretch between rounds: cut at the music's own sections, then every so many bars."""
            edges = [x] + [c for c in cuts if x + 32 <= c <= y - 32] + [y]
            for p, q in zip(edges, edges[1:]):
                lay.extend([u, v, None] for u, v in recut(p, q, long))

        for a, z, round_, n, ts, cells in rounds:
            knot = (a, z, round_, n, ts, cells) in knots and not (lay and lay[-1][2] and lay[-1][2].get("knot") and a - at < 32)
            if not knot and round_ / 16 > 1.6 * long:
                continue
            if a - at >= 32:
                fill(at, a)
            elif lay:
                lay[-1][1] = a          # a sliver before the round belongs to the plate before
            else:
                a = 0
            for i in range(n):
                lay.append([a if i == 0 else lay[-1][1], min(z - (n - 1 - i) * round_, bars * 16), {"tracks": ts, "cells": cells, "round": round_, "knot": knot and i == 0}])
            at = lay[-1][1]
        if bars * 16 - at >= 32:
            fill(at, bars * 16)
        elif lay:
            lay[-1][1] = bars * 16
    scenes, plan, last = [], [], None
    used = collections.Counter()
    shut = False        # the scene before was a round that closed on its last sixteenth
    for k, (a16, b16, cyc) in enumerate(lay):
        a = a16 // 16
        b = min(bars, max(a + 1, -(-b16 // 16)))
        by_notes, riffs, drums, tunes, others, cand = cast(a, b)
        # One wheel per distinct cell; at most one of them plain common time (a cell of 2, 4,
        # 8, 16), for the others to be odd against.
        wheel, seen_cells, had_common = [], set(), False
        for t in cand:
            c = t.cell(a, b)[0]
            if c in seen_cells or (common(c) and had_common):
                continue
            wheel.append(t)
            seen_cells.add(c)
            had_common |= common(c)
        if len(wheel) == 1:   # one riff alone: its nearest double keeps it company
            wheel += [t for t in cand if t not in wheel][:1]
        cells = [t.cell(a, b)[0] for t in wheel]
        if cyc:
            # A round: the plate holds the parts whose round it is, the drums last.
            pairs = sorted(zip(cyc["tracks"], cyc["cells"]), key=lambda tc: tc[0].role == "drum")
            wheel, cells = [t for t, _ in pairs], [c for _, c in pairs]
        cell = dict(zip(wheel, cells))
        S.HELD = {t.name: c for t, c in cell.items() if c}
        S.HOLD = 24 if scenes else 76        # (a song's first plate is seen whole while its title is up)
        S.SIXTEENTH = bar_s / 16
        S.END = b16
        odd = sum(1 for c in set(cells) if not common(c))
        # A tune worth a bird: one that sings at least a note a bar here.
        tune = next((t for t in tunes if t not in wheel and t.count(a, b) >= (b - a)), None)
        # What suits this stretch, best first.
        if not wheel and not tune:
            order = ["finish0", "studio0", "walkers0"]
        elif not wheel:
            order = ["flight", "studio0", "walkers0"]
        elif len(set(cells)) >= 2 and odd:
            order = ["wheels", "loops", "finish", "gears", "fence", "discs", "balls", "pendulums", "walkers", "studio", "sheet"]
        elif len(set(cells)) >= 2:
            order = ["finish", "walkers", "gears", "loops", "balls", "fence", "discs", "pendulums", "studio", "wheels", "sheet"]
        else:
            # One riff alone: bodies and a ring, not counting machines (a lone wheel says nothing).
            order = ["sheet", "walkers", "discs", "fence", "studio", "finish", "balls"]
        # A fence wants short riffs (a long one is too many pictures for the strips to hold
        # at draft size); a train of gears wants two.
        fits = lambda t, top: 3 <= (cell[t] or 0) <= top  # noqa: E731
        whole = (b16 - a16) / 16        # the scene's length in bars, to the sixteenth
        short = sorted((t for t in wheel if fits(t, FENCE_MAX) and not common(cell[t])), key=lambda t: cell[t])[:2]
        if len(short) == 1:     # one odd riff: common time runs beside it
            short += [t for t in wheel if fits(t, 8) and common(cell[t])][:1]
        if not short:
            order = [o for o in order if o != "fence"]
        # A train of gears wants two or three riffs whose lengths are within four times of
        # each other (a gear beside one six times its size is a speck): the longest run of such.
        fit = sorted((t for t in wheel if fits(t, 32)), key=lambda t: cell[t])
        train = max(([t for t in fit[i:] if cell[t] <= 4 * cell[fit[i]]][:3] for i in range(len(fit))), key=len, default=[])
        if len(train) < 2:
            order = [o for o in order if o != "gears"]
        # A knot wants two or three riffs of different lengths, none so long that five bars
        # of wire is a bare arc.
        knot, had = [], set()
        for t in sorted((t for t in wheel if fits(t, 24)), key=lambda t: (common(cell[t]), cell[t])):
            if cell[t] not in had:
                had.add(cell[t]), knot.append(t)
        knot = knot[:3]
        if len(knot) < 2:
            order = [o for o in order if o != "loops"]
        if wheel and max(cells) <= 4:
            # Nothing but short common time here: bodies, not counting machines.
            order = ["sheet", "walkers", "studio", "finish"]
        if tune and "flight" not in order and not cyc:
            order.insert(2, "flight")
        if k == 0 and not reel:
            # A song opens on a plate that comes up well under its name: lines and bodies on
            # black, not the daylight track, steel, or a strip that starts empty.
            order = [o for o in order if o not in ("fence", "studio", "gears", "finish")] or order
        # Each song begins its round of the studies somewhere else, so no two songs go
        # through them in the same order.
        turn = 0 if reel else (n * 3) % len(order)
        order = order[turn:] + order[:turn]
        # The one used least so far in this song (never the same twice running); ties go to
        # what suits best.
        base = lambda o: o.rstrip("0")  # noqa: E731
        if cyc and cyc.get("knot"):
            pick, last = "knot", "loops"
        else:
            pick = min((o for o in order if base(o) != last or len(order) == 1), key=lambda o: (used[base(o)], order.index(o)))
            last = base(pick)
        used[last] += 1
        # Who is on the plate: people and horses in turn, starting somewhere else each song.
        subject = ("walker", "horse", "runner", "pacer")[(n + used[last]) % 4]
        names = [t.name for t in wheel]
        plain = set()
        if pick in ("finish0", "studio0", "walkers0"):
            # Nothing has a cell here: whoever plays, on the bar's own clock.
            names = [t.name for t in distinct(riffs + tunes + drums + others, a, b)[:3]] or [(by_notes[0] if by_notes else tracks[0]).name]
            plain = set(names)
        spot_track = tune.name if tune else (names[-1] if names else None)
        shown = pick
        if pick == "wheels":
            use = names[:4]
            look = S.wheels(use, spot, spot_track if spot_track in use else use[-1])
        elif pick in ("finish", "finish0"):
            use = names[:3]
            look = S.finish_line(use, spot, spot_track if spot_track in use else use[-1], subject={"walker": "runner", "pacer": "horse"}.get(subject, subject), plain=tuple(plain), meet=bool(odd))
        elif pick == "balls":
            use = names[:4]
            look = S.balls(use, spot, spot_track if spot_track in use else use[-1])
        elif pick == "gears":
            use = [t.name for t in train]
            look = S.gears(use, spot, spot_track if spot_track in use else use[-1], white=n in WHITE)
        elif pick == "knot":
            # One whole round: the knot is tied from its first sixteenth to its last.
            use = [t.name for t in wheel][:3]
            look = S.loops(use, spot, spot_track if spot_track in use else use[-1], cells=cells[:3], tie=cyc["round"], start=b16 - cyc["round"])
        elif pick == "loops":
            use = [t.name for t in knot]
            look = S.loops(use, spot, spot_track if spot_track in use else use[-1], cells=[cell[t] for t in knot])
        elif pick == "fence":
            use = [t.name for t in short[:2]]
            look = S.fence(use, spot, spot_track if spot_track in use else use[-1], subject="pacer" if subject in ("walker", "pacer") else "horse")
        elif pick == "discs":
            # Rings of runners, one ring a riff: only riffs with a length of their own (a ring
            # of two or four says nothing), the longest cells left to the other studies.
            # Short riffs first (their figures are bigger); three rings only if all are short.
            fit = sorted((t for t in wheel if 3 <= (cell[t] or 0) <= 16), key=lambda t: cell[t])
            use = [t.name for t in fit][:3 if all(cell[t] <= 8 for t in fit[:3]) else 2] or names[:1]
            look = S.discs(use, spot, spot_track if spot_track in use else use[-1], subject={"walker": "runner", "pacer": "horse"}.get(subject, subject),
                           cells={t.name: cell[t] for t in wheel})
        elif pick == "pendulums":
            use = names[:5]
            look = S.pendulums(use, spot, spot_track if spot_track in use else use[-1])
        elif pick == "sheet":
            look = S.sheet(names[:4], spot, names[1] if len(names) > 1 else None, subject="horse" if subject == "pacer" else subject)
        elif pick in ("walkers", "walkers0"):
            use = names[:2] + ([tune.name] if tune and tune.name not in names[:2] else names[2:3])
            if tune:
                plain.add(tune.name)
            look = S.walkers(use, spot, spot_track if spot_track in use else use[-1], subject=subject, plain=tuple(plain))
        elif pick in ("studio", "studio0"):
            use = names[:3] + ([tune.name] if tune and tune.name not in names[:3] else names[3:4])
            if tune:
                plain.add(tune.name)
            # The fast ones are followed (the camera runs beside them); the slow ones pass.
            place = S.chase if subject in ("horse", "runner") else S.studio
            shown = "chase" if place is S.chase else pick
            look = place(use[:3], spot, spot_track if spot_track in use[:3] else use[:3][-1], subject=subject, plain=tuple(plain), white=n in WHITE, bars=whole, start=a16 / 16)
        else:  # flight
            fl = [tune] + [t for t in tunes if t is not tune and t not in wheel][:2]
            use = [t.name for t in fl]
            rng = {t.name: (max((t.lo - 24) / 84 - 0.01, 0), min((t.hi - 24) / 84 + 0.01, 1)) for t in fl}
            look = S.flight(use, spot, use[0], ranges=rng)
            names = use
            cells = [None] * len(use)
        scene = {"at": 0 if not scenes else f"{a16 // 16}bar" if a16 % 16 == 0 else f"{a16 / 4:g}b", "look": look}
        # A camera that holds time has been running before the cut: its plate, strip or sheet
        # is started early and drawn unseen (the scene's `lead`), so the cut lands on a
        # picture already made and not on an empty plate. A song's first plate develops in
        # view, under its title.
        lead = LEAD.get(last)
        if lead and scenes:
            scene["lead"] = lead
        if shut:
            # The knot before this closed on its last sixteenth: it stands a moment more,
            # border lit, while this plate comes up through it.
            scene["xfade"] = "2b"
        shut = pick == "knot" and b16 - cyc["round"] >= a16 - 1
        scenes.append(scene)
        plan.append((a16 / 16, b16 / 16, shown + ("*" if cyc and pick != "knot" else ""), names[:4], cells[:4], tune.name if tune else "-"))
    return d, bars, tracks, scenes, plan


def main():
    global OUT
    for a in sys.argv[1:]:
        if a.startswith("--out="):
            OUT = a[6:]
    OUT = os.path.abspath(OUT)
    os.makedirs(OUT, exist_ok=True)
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    only = [int(a) for a in args] or [int(t["n"]) for t in ALBUM["tracks"]]
    show = "--plan" in sys.argv
    reel = next((tuple(int(x) for x in a[7:].split(":")) for a in sys.argv[1:] if a.startswith("--reel=")), None)
    if reel:
        only, reel = [reel[0]], (reel[1], reel[2], reel[3] if len(reel) > 3 else 4)
    for t in ALBUM["tracks"]:
        n = int(t["n"])
        if n not in only:
            continue
        song = t["id"]
        d, bars, tracks, scenes, plan = choose(n, t["title"], song, reel)
        if show:
            print(f"{song} \"{t['title']}\": {bars} bars, {d['bpm']:.0f} bpm, {len(tracks)} tracks"
                  + ("" if d.get("engine") else "  (cells read here, not by the engine: build the chirp-video branch or set $CHIRP)"))
            roles = collections.defaultdict(list)
            for tr in tracks:
                roles[tr.role].append(tr.name)
            for r, names in roles.items():
                print(f"  {r:6s} {' '.join(names)}"[:200])
        bar = lambda x: f"{x:g}" if x == int(x) else f"{x:.2f}"  # noqa: E731
        for a, b, pick, names, cells, tune in plan:
            if show:
                print(f"  {bar(a):>6s}-{bar(b):<6s} {pick:9s} {' '.join(f'{x}:{c}' for x, c in zip(names, cells + [None] * 4)):48s} tune {tune}")
        if show:
            continue
        head = (f"# chirpers10 t{n} \"{t['title']}\": written by compose/chirpers10/vis-gen/ctgen.py from the song's own notes\n"
                f"# ({bars} bars; {len(scenes)} scenes). Do not edit: run ctgen.py {n} again when the song changes.\n")
        out = os.path.join(OUT, f"{song}{'-reel' if reel else ''}.yaml")
        figures = [(round(a, 4), round(b - a, 4)) for a, b, *_ in plan]
        white = n in WHITE
        prog = {"fade": [0, 0] if white or reel else ["1bar", "2bar"],
                "master": S.master(n, t["title"], white=white, figures=figures, bars=bars, window=reel[:2] if reel else None), "scenes": scenes}
        open(out, "w").write(head + json.dumps(prog, indent=1) + "\n")
        print(f"{song}: {len(scenes)} scenes: " + " ".join(p[2] for p in plan))
    # (In a plan, `knot` is a round tied as a knot and `name*` another study given a whole round.)


if __name__ == "__main__":
    main()
