#!/usr/bin/env python3
"""ctgen: Common Time's film, written from the songs themselves.

    ctgen.py                 write vis/chirpers10-tN.yaml for every song of the album
    ctgen.py 3 7             only those tracks
    ctgen.py --plan 3        print what it found in the song and what it chose, write nothing
    ctgen.py --out=DIR …     write the programmes to DIR instead of vis/

The songs are still being written, so nothing here is fixed to a bar by hand. For each song the
generator reads the notes (tools/songmap.py: `chirp plan` and a MIDI render), and works out:
  - what each track is (a riff, the bass, a drum, a tune, a voice), from its notes alone;
  - each track's CELL bar by bar (the length of its repeating riff in sixteenths: the same
    reading the engine gives the picture as `track.T.cell`);
  - where the song changes (who plays, and which cells), which is where the scenes change;
  - which study fits each stretch (studies.py), never the same one twice running.
Run it again whenever a song changes: the programme follows.
"""
import collections
import hashlib
import json
import os
import pickle
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
    def __init__(self, name, notes, sung, bars, bar_steps):
        self.name, self.notes, self.sung = name, notes, sung
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
        for b in range(bars):
            if not self.per_bar[b]:
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

    def sig(self, a, b):
        return frozenset(s for bar in range(a, b) for s in self.steps_in_bar.get(bar, ()))


def analyse(song):
    d = load(song)
    bar_steps = int(round(d["bar_beats"] * 4))
    last = max(n[1] for ns in d["notes"].values() for n in ns)
    bars = int(last // d["bar_beats"]) + 1
    tracks = [Track(name, ns, name in d["sung"], bars, bar_steps) for name, ns in d["notes"].items() if ns]
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
            d += 0.25
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
    # Long stretches are cut again, on four-bar lines, so the picture keeps changing.
    out = []
    for a, b in zip(cuts, cuts[1:] + [bars]):
        n = max(1, round((b - a) / long))
        step = (b - a) / n
        for i in range(n):
            out.append(a + int(round(i * step / 4)) * 4 if i else a)
    out = sorted(set(out))
    return list(zip(out, out[1:] + [bars]))


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


def choose(n, title, song):
    d, bars, tracks = analyse(song)
    spot = SPOTS[(n - 1) % len(SPOTS)]
    # A scene lasts about 26 seconds: so many bars at this song's tempo, in fours.
    bar_s = d["bar_beats"] * 60 / d["bpm"]
    long = int(min(16, max(8, round(26 / bar_s / 4) * 4)))
    secs = sections(bars, tracks, short=max(4, long // 2), long=long)
    scenes, plan, last = [], [], None
    used = collections.Counter()
    for k, (a, b) in enumerate(secs):
        # Who is playing here: in most of its bars, and from near its start (a plate should
        # not stand empty while its subject waits to come in).
        act = [t for t in tracks if t.count(a, b) >= 4 and t.cover(a, b) >= 0.5 and t.count(a, min(a + 3, b))]
        if not act:
            act = [t for t in tracks if t.count(a, b) >= 4]
        by_notes = sorted(act, key=lambda t: -t.count(a, b))
        riffs = distinct([t for t in by_notes if t.role in ("riff", "bass")], a, b)
        drums = [t for t in by_notes if t.role == "drum"]
        tunes = distinct([t for t in by_notes if t.role in ("tune", "voice")], a, b)
        others = distinct([t for t in by_notes if t.role == "other"], a, b)
        celled = lambda t: (t.cell(a, b)[0] is not None and t.cell(a, b)[1] >= 0.5)  # noqa: E731
        # Who carries a cell here: the riffs first, then any other part with an odd one (a clean
        # tick, a harp), then the kick and the kit. One wheel per distinct cell; at most one of
        # them plain common time (a cell of 2, 4, 8, 16), for the others to be odd against.
        common = lambda c: c in (2, 4, 8, 16, 32)  # noqa: E731
        oddones = [t for t in distinct(tunes + others, a, b) if celled(t) and not common(t.cell(a, b)[0])]
        cand = [t for t in riffs if celled(t)] + oddones + [t for t in drums if celled(t)]
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
        odd = sum(1 for c in set(cells) if not common(c))
        # A tune worth a bird: one that sings at least a note a bar here.
        tune = next((t for t in tunes if t not in wheel and t.count(a, b) >= (b - a)), None)
        # What suits this stretch, best first.
        if not wheel and not tune:
            order = ["finish0", "studio0", "walkers0"]
        elif not wheel:
            order = ["flight", "studio0", "walkers0"]
        elif len(set(cells)) >= 2 and odd:
            order = ["wheels", "finish", "gears", "fence", "discs", "balls", "pendulums", "walkers", "studio", "sheet"]
        elif len(set(cells)) >= 2:
            order = ["finish", "walkers", "gears", "balls", "fence", "discs", "pendulums", "studio", "wheels", "sheet"]
        else:
            # One riff alone: bodies and a ring, not counting machines (a lone wheel says nothing).
            order = ["sheet", "walkers", "discs", "fence", "studio", "finish", "balls"]
        # A fence wants short riffs (a long one is too many pictures for the strips to hold
        # at draft size); a train of gears wants two.
        fits = lambda t, top: 3 <= (t.cell(a, b)[0] or 0) <= top  # noqa: E731
        short = sorted((t for t in wheel if fits(t, FENCE_MAX) and not common(t.cell(a, b)[0])), key=lambda t: t.cell(a, b)[0])[:2]
        if len(short) == 1:     # one odd riff: common time runs beside it
            short += [t for t in wheel if fits(t, 8) and common(t.cell(a, b)[0])][:1]
        if not short:
            order = [o for o in order if o != "fence"]
        if sum(1 for t in wheel if 3 <= (t.cell(a, b)[0] or 0) <= 32) < 2:
            order = [o for o in order if o != "gears"]
        if wheel and max(cells) <= 4:
            # Nothing but short common time here: bodies, not counting machines.
            order = ["sheet", "walkers", "studio", "finish"]
        if tune and "flight" not in order:
            order.insert(2, "flight")
        # Each song begins its round of the studies somewhere else, so no two songs go
        # through them in the same order.
        turn = (n * 3) % len(order)
        order = order[turn:] + order[:turn]
        # The one used least so far in this song (never the same twice running); ties go to
        # what suits best.
        base = lambda o: o.rstrip("0")  # noqa: E731
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
            # A train of gears: riffs with a length of their own, the shortest first.
            fit = sorted((t for t in wheel if 3 <= (t.cell(a, b)[0] or 0) <= 32), key=lambda t: t.cell(a, b)[0])
            use = [t.name for t in fit][:3] or names[:1]
            look = S.gears(use, spot, spot_track if spot_track in use else use[-1], white=n in WHITE)
        elif pick == "fence":
            use = [t.name for t in short[:2]]
            look = S.fence(use, spot, spot_track if spot_track in use else use[-1], subject="pacer" if subject in ("walker", "pacer") else "horse")
        elif pick == "discs":
            # Rings of runners, one ring a riff: only riffs with a length of their own (a ring
            # of two or four says nothing), the longest cells left to the other studies.
            # Short riffs first (their figures are bigger); three rings only if all are short.
            fit = sorted((t for t in wheel if 3 <= (t.cell(a, b)[0] or 0) <= 16), key=lambda t: t.cell(a, b)[0])
            use = [t.name for t in fit][:3 if all(t.cell(a, b)[0] <= 8 for t in fit[:3]) else 2] or names[:1]
            look = S.discs(use, spot, spot_track if spot_track in use else use[-1], subject={"walker": "runner", "pacer": "horse"}.get(subject, subject),
                           cells={t.name: t.cell(a, b)[0] for t in wheel})
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
            look = place(use, spot, spot_track if spot_track in use else use[-1], subject=subject, plain=tuple(plain), white=n in WHITE)
        else:  # flight
            fl = [tune] + [t for t in tunes if t is not tune and t not in wheel][:2]
            use = [t.name for t in fl]
            rng = {t.name: (max((t.lo - 24) / 84 - 0.01, 0), min((t.hi - 24) / 84 + 0.01, 1)) for t in fl}
            look = S.flight(use, spot, use[0], ranges=rng)
            names = use
            cells = [None] * len(use)
        scenes.append({"at": f"{a}bar" if a else 0, "look": look})
        plan.append((a, b, shown, names[:4], cells[:4], tune.name if tune else "-"))
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
    for t in ALBUM["tracks"]:
        n = int(t["n"])
        if n not in only:
            continue
        song = t["id"]
        d, bars, tracks, scenes, plan = choose(n, t["title"], song)
        if show:
            print(f"{song} \"{t['title']}\": {bars} bars, {d['bpm']:.0f} bpm, {len(tracks)} tracks")
            roles = collections.defaultdict(list)
            for tr in tracks:
                roles[tr.role].append(tr.name)
            for r, names in roles.items():
                print(f"  {r:6s} {' '.join(names)}"[:200])
        for a, b, pick, names, cells, tune in plan:
            if show:
                print(f"  {a:4d}-{b:<4d} {pick:9s} {' '.join(f'{x}:{c}' for x, c in zip(names, cells + [None] * 4)):48s} tune {tune}")
        if show:
            continue
        head = (f"# chirpers10 t{n} \"{t['title']}\": written by compose/chirpers10/vis-gen/ctgen.py from the song's own notes\n"
                f"# ({bars} bars; {len(scenes)} scenes). Do not edit: run ctgen.py {n} again when the song changes.\n")
        out = os.path.join(OUT, f"{song}.yaml")
        figures = [(a, b - a) for a, b, *_ in plan]
        white = n in WHITE
        prog = {"fade": [0, 0] if white else ["1bar", "2bar"], "master": S.master(n, t["title"], white=white, figures=figures, bars=bars), "scenes": scenes}
        open(out, "w").write(head + json.dumps(prog, indent=1) + "\n")
        print(f"{song}: {len(scenes)} scenes: " + " ".join(p[2] for p in plan))


if __name__ == "__main__":
    main()
