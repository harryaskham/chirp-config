#!/usr/bin/env python3
"""wildgen: Common Time's second film, dealt from wild.py's idioms over each song as found.

    wildgen.py               write ../film/chirpers10-tN.yaml for every song
    wildgen.py 3 7           only those songs
    wildgen.py --plan 3      print the scenes and what was dealt; write nothing
    wildgen.py --out=DIR …   write to DIR

It reads the songs exactly as ctgen.py does (the engine's cells, the notes), then cuts each
into short scenes on the music's own joints and gives every scene an idiom, a variant, a
treatment and a colourway so that no two scenes of the album are the same picture.
"""
import collections
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ctgen as C  # noqa: E402
import wild as W  # noqa: E402

# Each song's colours: ground, ink, dim ink, and three lamps.
PALS = {
    1: ("#050506", "#f2efe6", "#77746c", "#ff5a2a", "#19c3b1", "#ffd23c"),
    2: ("#06080a", "#e9f1f2", "#6c7a80", "#39c5ff", "#ff7a59", "#b8ff6a"),
    3: ("#080604", "#f6ead2", "#857660", "#ffb000", "#4ad1c4", "#ff4f6e"),
    4: ("#050507", "#eeeaf6", "#77738a", "#ff3d6e", "#6ab0ff", "#ffe066"),
    5: ("#040705", "#e8f3e4", "#6f8068", "#7dff6a", "#ff8a3d", "#5cc8ff"),
    6: ("#070504", "#f7ebe0", "#8a7566", "#ff7a00", "#00c9a7", "#f9f871"),
    7: ("#060509", "#ece6fa", "#7c7396", "#b28cff", "#ffc75f", "#ff6f91"),
    8: ("#030707", "#e2f5f1", "#64817b", "#00d6a8", "#ff5e78", "#ffe45e"),
    9: ("#070602", "#faf3d6", "#8a8260", "#ffd23c", "#5c7cfa", "#ff6b6b"),
    10: ("#080404", "#f8e6e4", "#8b6c69", "#ff4040", "#3ddbd9", "#ffd166"),
    11: ("#04060a", "#e4eefc", "#677893", "#4aa8ff", "#ffa94d", "#f783ac"),
    12: ("#080507", "#fae8f1", "#8d6f7f", "#ff9ec4", "#63e6be", "#ffd43b"),
    13: ("#060802", "#f1f8dc", "#7c875f", "#c8ff3c", "#ff6b9d", "#74c0fc"),
    14: ("#080503", "#fbeadf", "#8d7464", "#ff6a3d", "#38d9a9", "#e599f7"),
    15: ("#03070a", "#dff4fb", "#62808c", "#5ce0ff", "#ffb347", "#ff6b81"),
    16: ("#080603", "#fbf0dc", "#8e7c60", "#ffb86a", "#66d9e8", "#f06595"),
    17: ("#070404", "#f5ece6", "#857069", "#ff5a2a", "#19c3b1", "#ffd23c"),
}
PAPER = "#e9e4d6"
PAPER_INK = "#141312"


class Song:
    """A song read once: its tracks, bars and tempo, and scene contexts on request."""
    def __init__(self, num):
        self.n = num
        self.meta = next(t for t in C.ALBUM["tracks"] if int(t["n"]) == num)
        self.id, self.title = self.meta["id"], self.meta["title"]
        self.d, self.bars, self.tracks = C.analyse(self.id)
        self.bar_s = self.d["bar_beats"] * 60 / self.d["bpm"]
        self.by = {t.name: t for t in self.tracks}
        # How full each bar is: notes sounding in it, against a full bar of this song.
        per = [sum(t.per_bar[b] for t in self.tracks) for b in range(self.bars)]
        top = sorted(per)[int(0.85 * (len(per) - 1))] or 1
        self.full = [min(1.0, n / top) for n in per]

    def cast(self, a, b):
        """Who plays in bars a..b, as ctgen has it: (by_notes, riffs, drums, tunes, others, cand)."""
        tracks, bar_s = self.tracks, self.bar_s
        soon = 3 if a == 0 else max(1, min(3, int(4.0 / bar_s + 0.5)))
        act = [t for t in tracks if t.count(a, b) >= max(2, b - a) and t.cover(a, b) >= 0.5 and t.count(a, min(a + soon, b))]
        if not act:
            act = [t for t in tracks if t.count(a, b) >= 2]
        by_notes = sorted(act, key=lambda t: -t.count(a, b)) or sorted(tracks, key=lambda t: -len(t.notes))[:1]
        riffs = C.distinct([t for t in by_notes if t.role in ("riff", "bass")], a, b)
        drums = [t for t in by_notes if t.role == "drum"]
        tunes = C.distinct([t for t in by_notes if t.role in ("tune", "voice")], a, b)
        others = C.distinct([t for t in by_notes if t.role == "other"], a, b)
        held = lambda t: sum(1 for k in range(a, b) if t.per_bar[k] and t.cells[k] == t.cell(a, b)[0]) / (b - a)  # noqa: E731
        celled = lambda t: (t.cell(a, b)[0] is not None and t.cell(a, b)[1] >= 0.5 and held(t) >= 0.45 and t.count(a, b) >= b - a)  # noqa: E731
        oddones = [t for t in C.distinct(tunes + others, a, b) if celled(t) and t.cell(a, b)[0] not in C.COMMON]
        cand = [t for t in riffs if celled(t)] + oddones + [t for t in drums if celled(t)]
        return by_notes, riffs, drums, tunes, others, cand

    def part(self, t, a16, b16, cell=None):
        a, b = a16 // 16, max(a16 // 16 + 1, -(-b16 // 16))
        keys = [k for s, _, k in t.notes if a16 / 4 <= s < b16 / 4] or [t.med]
        anchor = t.anchor(a16, b16, cell) if cell else None
        return W.P(t.name, cell, a16 if anchor is None else anchor, t.role, min(keys), max(keys), t.count(a, b) / max(b - a, 1), n=sum(1 for s, *_ in t.notes if a16 / 4 <= s < b16 / 4))

    def cx(self, a16, b16, k=0, variant=0, paper=False, cyc=None):
        a = a16 // 16
        b = min(self.bars, max(a + 1, -(-b16 // 16)))
        by_notes, riffs, drums, tunes, others, cand = self.cast(a, b)
        # One part per distinct cell, at most one of them plain common time.
        wheel, seen, had_common = [], set(), False
        for t in cand:
            c = t.cell(a, b)[0]
            if c in seen or (c in C.COMMON and had_common):
                continue
            wheel.append(t)
            seen.add(c)
            had_common |= c in C.COMMON
        cells = [t.cell(a, b)[0] for t in wheel]
        if cyc:
            pairs = sorted(zip(cyc["tracks"], cyc["cells"]), key=lambda tc: tc[0].role == "drum")
            wheel, cells = [t for t, _ in pairs], [c for _, c in pairs]
        riffs_p = [self.part(t, a16, b16, c) for t, c in zip(wheel, cells)]
        # Doubles of the celled parts as well (same cell): more bodies for the same riff.
        every = [self.part(t, a16, b16, t.cell(a, b)[0]) for t in cand]
        drum_p = [self.part(t, a16, b16, t.cell(a, b)[0]) for t in drums]
        for p in drum_p:        # a drum with no cell of its own keeps the bar
            if not p.cell:
                p.cell, p.anchor = 16, a16 - a16 % 16
        tune_p = [self.part(t, a16, b16, None) for t in tunes if t not in wheel and t.count(a, b) >= (b - a)]
        low = lambda w: next((p for p in drum_p if w in p.name.lower()), None)  # noqa: E731
        pal = PALS[self.n]
        bg, ink, dim = (PAPER, PAPER_INK, "#8a8578") if paper else pal[:3]
        return W.Cx(n=self.n, title=self.title, song=self.id, a16=a16, b16=b16, bars=(b16 - a16) / 16, bar_s=self.bar_s, six=self.bar_s / 16, bpm=self.d["bpm"],
                    riffs=riffs_p, every=every, drums=drum_p, tunes=tune_p, parts=[self.part(t, a16, b16, t.cell(a, b)[0]) for t in by_notes],
                    kick=low("kick"), snare=low("snare"), hat=low("hat") or low("cym") or low("ride"),
                    bg=bg, ink=ink, dim=dim, a=pal[3], b=pal[4], c=pal[5], paper=paper, seed=self.n * 1000 + k, k=k, variant=variant, cyc=cyc,
                    odd=sum(1 for c in set(cells) if c not in C.COMMON), lcm=(__import__("math").lcm(*cells) if cells else 16),
                    full=sum(self.full[a:b]) / max(b - a, 1))


# What each song leans on: idioms that suit its name, dealt there first (and still once only
# in each guise).
FEATURE = {
    1: ("loom", "remainder", "crystal", "helix", "billiard", "riley"), 2: ("sympathy", "pendwave", "strings", "cradle", "seesaw", "ink", "strobe"), 3: ("changes", "maypole", "chorus", "stringart", "drill", "vasarely"),
    4: ("dominoes", "automaton", "tally", "abacus", "odometer", "hanoi"), 5: ("stairs", "ridges", "escalator", "flight", "lifts", "trampoline", "suprematist", "barber"), 6: ("colony", "bifurcate", "automaton", "anemone", "lava", "marbling"),
    7: ("golden", "spiral", "sunflower", "mandala", "star", "kandinsky", "courses"), 8: ("loom", "tartan", "solkattu", "musicbox", "specimen", "breakout", "measure"), 9: ("henge", "orrery", "moons", "grove", "snow", "sundial"),
    10: ("balance", "coins", "tape", "galton", "duel", "hourglass"), 11: ("doors", "blinds", "press", "hammers", "tesla", "albers"), 12: ("hands", "juggle", "semaphore", "chorus", "fan", "shadowplay"),
    13: ("eclipse", "pond", "spiral", "lanterns", "rink", "zen"), 14: ("numerals", "tally", "zoetrope", "seismo", "leader", "hourglass", "strobe"), 15: ("slack", "ropes", "wires", "swings", "switchboard", "rothko"),
    16: ("moire", "chladni", "eclipse", "lighthouse", "billiard", "candles"), 17: ("railway", "highway", "gates", "constellation", "searchlights", "sundial", "hailstone"),
}
# Each song's house: the guises and the ways of sharing the frame it leans to, so the songs
# differ from one another as well as from bar to bar. (The first song, the album's argument, has none.)
HOUSE = {
    2: "echo water blown mirror stop slices ball double lighten diptych satellite cutout smoked delayed",
    3: "lines engraved hatched typed sheet blueprint leaded strips bands intercut triptych stencil woven",
    4: "typed onebit newsprint dots blocks combed poster board corner card strips tracking",
    5: "relief planet hole tunnel falling blown duotone sweep window nest bands cutout infra screen",
    6: "overgrown wound warp solar leaded kaleido flood difference lighten iris rings glass dripping",
    7: "coiled falling kaleido spin wall wound ball nest rings wedges satellite glass woven",
    8: "leaded engraved newsprint poster flood duotone mirror triptych diptych window board infra woven",
    9: "stop slices echo fringe roll relief drawn double iris sweep corner cutout smoked delayed",
    10: "onebit dots torn combed typed poster negative difference card bands corner stencil dripping",
    11: "mirror roll spin sheet blocks torn wall diptych sweep card intercut tracking screen",
    12: "mirror drawn blueprint hatched ball echo water diptych intercut lighten satellite cutout screen",
    13: "echo stop slices fringe water overgrown hole double window iris difference glass smoked negative stencil",
    14: "typed dots lines blocks sheet onebit stop strips board wedges triptych stencil delayed",
    15: "warp wound blown torn water combed tunnel sweep bands double satellite dripping woven",
    16: "fringe duotone solar relief falling planet leaded lighten difference nest window glass tracking delayed",
    17: "tunnel falling planet roll blown ball flood wedges rings nest card stencil infra screen",
}
HOUSE = {n_: set(v.split()) for n_, v in HOUSE.items()}
TRANSITIONS = ("melt", "luma", "push", "strips", "burn", "blocks", "zoom", "weave", "spiral", "rings", "checker", "split", "wipe", "iris", "blinds", "clock", "diamond", "rise", "dissolve",
               "flip", "squeeze", "shred", "stretch", "whip", "fall", "whirl", "ripple", "glitch", "pixel", "tiles", "doors", "spin", "scan", "diagonal", "slats", "interlace", "star", "dither", "corners", "wave",
               "fan", "shutter")
NO_PAIR = ("room", "sheet", "plate", "travel")      # families that are not put in a frame with another


def rnd(*key):
    """A fixed random number 0..1 for a key."""
    import hashlib
    return int(hashlib.sha1(repr(key).encode()).hexdigest()[:8], 16) / 0xffffffff


def landings(S):
    """The great round's end: the sixteenths (on a bar line) at which every length of riff
    that the song keeps to, each from where it began, comes round at once, where that happens
    only once or twice in the whole song. [(sixteenth, {cell: where its turns begin})]."""
    end = S.bars * 16
    cover, anc = collections.Counter(), collections.defaultdict(collections.Counter)
    for t in (S.tracks.values() if isinstance(S.tracks, dict) else S.tracks):
        for sp in t.anchors:
            a, z, cell, anchor = sp[:4]
            if 32 % cell:
                cover[cell] += z - a
                anc[cell][anchor % cell] += z - a
    # A length the song keeps to: played (by all its parts together) for at least half the
    # song's length, and seven times in ten from the same place.
    need = {cell: anc[cell].most_common(1)[0][0] for cell, n in cover.items() if n >= 0.5 * end and anc[cell].most_common(1)[0][1] >= 0.7 * n}
    if len(need) < 2:
        return []
    hits = [t for t in range(16 * 8, end - 16, 16) if all((t - r) % cell == 0 for cell, r in need.items())]
    # (It is a landing only after a long wait: once or twice in the song, and past its middle.)
    return [(t, need) for t in hits if t >= end / 2] if 1 <= len(hits) <= 2 else []


def cut(S):
    """Where a song's scenes change: [(first sixteenth, last, round or None)].

    The music's own joints first (who plays changes, a riff's length changes) and the ends
    of its long rounds, to the sixteenth. Between them a scene lasts some six to ten seconds:
    whole rounds of its own riffs where they come round that quickly, so that the cut falls
    where they meet and not on the bar; whole bars otherwise."""
    end = S.bars * 16
    six = S.bar_s / 16
    least = max(2, round(5.0 / S.bar_s))        # bars: no scene much under five seconds
    joints = {a * 16 for a, _ in C.sections(S.bars, S.tracks, short=least, long=None)} | {0, end}
    rounds = C.find_cycles(S.tracks, S.bars, S.bar_s) if S.d["engine"] else []
    S.rounds = rounds
    edges = set()
    for a, z, *_ in rounds:
        edges |= {a, min(z, end)}
    S.landings = landings(S)
    edges |= {t for t, _ in S.landings}
    gap = max(24, int(4.0 / six))               # no stretch shorter than this (about four seconds)
    head = max(64, int(8.5 / six))              # the first scene stands under the song's name
    marks = sorted(m for m in edges | {j for j in joints if all(abs(j - e) >= gap for e in edges)} if m == 0 or m >= head)
    kept = [marks[0]]
    for m in marks[1:]:
        if m - kept[-1] >= gap:
            kept.append(m)
        elif m == end or (m in edges and kept[-1] not in edges and kept[-1] != 0):
            kept[-1] = m            # the nearer joint gives way to a round's end (or the song's)
        # (otherwise this joint is dropped)
    if kept[-1] != end:
        kept.append(end)
    kept = sorted(set(kept))
    out = []
    for x, y in zip(kept, kept[1:]):
        cyc = next(({"tracks": ts, "cells": cells, "round": r} for a, z, r, _, ts, cells in rounds if a <= x and y <= z), None)
        p = x
        while p < y:
            k = len(out)
            # A full passage is cut faster than a thin one (four to eight seconds against six to eleven).
            full = S.full[min(p // 16, S.bars - 1)]
            secs = (6.2 - 2.2 * full) + (5.0 - 1.2 * full) * rnd(S.n, "len", k) if k else max(9.0, 3.6 * S.bar_s)
            want = secs / six
            c = S.cx(p, int(min(y, p + want)), cyc=cyc)
            L = c.lcm if (len(c.riffs) >= 2 and c.odd) else 16
            unit = L if 16 < L <= want * 1.25 and k else 16
            q = p + max(1, round(want / unit)) * unit
            if q >= y or y - q < 3.6 / six:
                q = y
            out.append((p, q, cyc, None))
            p = q
    out = flurries(S, dynamics(S, out), gap)
    for t, _ in S.landings:
        for i, (p, q, cyc, kind) in enumerate(out):
            if p == t:
                out[i] = (p, q, cyc, "landing")
    return out


def dynamics(S, scenes):
    """Where the band comes in (a bar far fuller than the one before) the film cuts on it, to
    the sixteenth; and the thin bar before it, where there is one, stands alone and hushed."""
    f = S.full
    S.drops = [b for b in range(2, S.bars - 2) if f[b] > 0.5 and f[b - 1] < 0.5 * f[b] and f[b] - f[b - 1] > 0.35]
    S.stops = [b for b in range(2, S.bars - 2) if f[b] < 0.5 * min(f[b - 1], f[b + 1]) and f[b - 1] > 0.4]
    for d in S.drops:
        x = d * 16
        i = next((i for i, (p, q, *_) in enumerate(scenes) if p <= x < q), None)
        if i is None or i == 0:
            continue
        p, q, cyc, _ = scenes[i]
        if p == x:
            scenes[i] = (p, q, cyc, "drop")
        elif x - p >= 16 and q - x >= 32:
            scenes[i:i + 1] = [(p, x, cyc, None), (x, q, cyc, "drop")]
        elif x - p < 16 and i > 1:
            # A joint just before the drop: the drop takes the cut instead.
            scenes[i - 1] = (scenes[i - 1][0], x, scenes[i - 1][2], scenes[i - 1][3])
            scenes[i] = (x, q, cyc, "drop")
    for s_ in S.stops:
        x, y = s_ * 16, (s_ + 1) * 16
        i = next((i for i, (p, q, *_) in enumerate(scenes) if p <= x and y <= q), None)
        if i is None or i == 0 or scenes[i][3]:
            continue
        p, q, cyc, _ = scenes[i]
        new = ([(p, x, cyc, None)] if x - p >= 24 else []) + [(x if x - p >= 24 else p, y, cyc, "hush")] + ([(y, q, cyc, None)] if q > y else [])
        if q > y and q - y < 24:
            continue
        scenes[i:i + 1] = new
    return scenes


def fills(S):
    """Bars where the drums break out of their pattern: far more strokes than the bars around."""
    dr = [t for t in S.tracks if t.role == "drum"]
    tot = [sum(t.per_bar[b] for t in dr) for b in range(S.bars)]
    out = []
    for b in range(4, S.bars - 1):
        near = sorted(tot[x] for x in range(max(0, b - 4), min(S.bars, b + 5)) if x != b)
        m = near[len(near) // 2] if near else 0
        if m > 0 and tot[b] >= 1.35 * m and tot[b] - m >= 6:
            out.append((tot[b] / m, b))
    # The strongest first, and none within twelve bars of one already taken.
    kept = []
    for _, b in sorted(out, reverse=True):
        if all(abs(b - x) >= 12 for x in kept):
            kept.append(b)
    return sorted(kept)


def flurries(S, scenes, gap):
    """Where the drums break into a fill the film does too: that bar goes by in flashes, a
    beat each (two at a fast tempo), each a different picture."""
    six = S.bar_s / 16
    unit = 4 if 4 * six >= 0.42 else 8
    S.fills = fills(S)
    for b in S.fills:
        x, y = b * 16, (b + 1) * 16
        i = next((i for i, (p, q, *_) in enumerate(scenes) if p <= x and y <= q), None)
        if i is None or i == 0 or scenes[i][3]:
            continue
        p, q, cyc, _ = scenes[i]
        if x - p < 0.6 * gap:
            x = p           # too little before it to stand alone: the flurry takes it
        if q - y < 0.6 * gap:
            y = q
        if y - x > 40:
            continue        # (that would be flashes for too long)
        new = [(p, x, cyc, None)] if x > p else []
        new += [(e, min(e + unit, y), cyc, "flash") for e in range(x, y, unit) if y - e >= unit // 2]
        new[-1] = (new[-1][0], y, cyc, new[-1][3])
        if y < q:
            new.append((y, q, cyc, None))
        scenes[i:i + 1] = new
    return scenes


class Deal:
    """What has been dealt so far, album-wide: so no picture comes twice."""
    def __init__(self):
        self.used = collections.Counter()       # idiom → times
        self.treats = collections.Counter()
        self.combos = set()                     # (idiom, treatment)
        self.recent = []                        # idioms, newest last
        self.count = 0
        self.log = {}                           # song → ["idiom/treatment", …]
        self.kinds = collections.Counter()      # combinations → times
        self.trans = collections.Counter()
        self.arrivals = 0
        self.moves = collections.Counter()
        self.flashes = 0
        self.motif = {}
        self.dyn = collections.Counter()
        self.last = None
        self.chains = 0
        self.grown = collections.Counter()
        self.stacks = collections.Counter()
        self.trios = 0
        self.odd = 0
        self.landings = 0
        self.ruled = 0
        self.album_first = None

    @staticmethod
    def motif_key(c):
        return tuple((p.name, p.cell) for p in c.riffs[:2])

    def choose(self, S, c, k, first, flash=False, prefer=None, kind=None, ahead=None, final=False):
        in_song = self.song_used
        fams = [W.REG[i]["fam"] for i in self.recent[-3:]]
        cands = []
        secs = (c.b16 - c.a16) * c.six
        busiest = max([p.n for p in c.riffs[:2] + c.tunes[:1]] or [0])
        # Chains: a picture is joined by a second, and then the second stands alone.
        last = self.last if not flash else None
        hand_on = last["partner"] if last and last.get("partner") and not prefer and kind != "hush" and rnd(S.n, k, "hand?") < 0.7 else None
        if hand_on:
            fams = fams[:-1]        # (its family was the last one seen: that is the point)
        for name, info in W.REG.items():
            if info["needs"] > len(c.riffs) or (info["tune"] and not c.tunes):
                continue
            if first and (info["cost"] >= 3 or info["fam"] in ("plate", "room", "travel")):
                continue
            if name == "numerals" and S.n != 14:
                continue        # figures only where the song is about counting
            if flash and (info["cost"] >= 3 or info["fam"] in ("plate", "travel", "sheet", "trace", "grow") or name in W.PLATES or name in W.SLOW):
                continue        # a flash has no time to draw anything out
            if name in W.FED and (final or busiest < max(5, 1.4 * secs)):
                continue        # it is made of notes, and here there are too few (or the song is ringing out)
            score = 4.0 * self.used[name] + 1.5 * (info["cost"] - 1) - 2.0 * min(info["needs"], 3) + 3.0 * rnd(S.n, k, name)
            if name == prefer:
                score -= 60         # the song ends on the picture it began with, changed
            elif name == hand_on:
                score -= 45         # the picture that came in beside the last one now stands alone
            elif name in self.recent[-(9 if flash else 12):]:
                score += 100
            if flash and in_song[name] and name not in self.recent[-9:]:
                score -= 6          # a flash looks back at what the song has shown, in another guise
            if fams and info["fam"] == fams[-1]:
                score += 50
            elif info["fam"] in fams:
                score += 8
            if name in FEATURE.get(S.n, ()) and in_song[name] < 2:
                score -= 7
            if info["fam"] == "plate":
                score += 3          # the first film's studies: now and then
            if not any((name, t) not in self.combos and ok(c, info) for t, (_, ok) in W.TREAT.items()) or (info["fam"] == "plate" and self.used[name]):
                score += 40         # it has been seen every way it can be
            mood = info.get("mood", 0)
            if (mood < 0 and c.full > 0.7) or (mood > 0 and c.full < 0.35):
                score += 9          # a calm picture for a thin passage, a full one for a full one
            if kind == "hush":
                score += -10 * (mood < 0) + 20 * (mood > 0) + 30 * (info["cost"] >= 3)
            if kind == "drop":
                score += -10 * (mood > 0) + 14 * (mood < 0)
            if name == self.motif.get(self.motif_key(c)) and name not in self.recent[-5:] and rnd(S.n, k, "motif?") < 0.4:
                score -= 14         # the riff that had this picture has come back: so does the picture, changed
            cands.append((score, name))
        import copy
        base = copy.copy(c)

        def make(name, sub=None, keep=False, ctx=None):
            """The idiom's look for this scene (as part `sub` sees it), or None if it does not fit.
            `keep`: as it was last time (the same camera and colours), for a picture that carries on."""
            d = copy.copy(ctx or base) if sub is None else base.sub(sub, 2)
            d.variant = max(self.used[name] - keep, 0)
            rot = d.variant % 3
            d.a, d.b, d.c = (d.a, d.b, d.c)[rot:] + (d.a, d.b, d.c)[:rot]
            try:
                return d, W.bolder(name, W.REG[name]["f"](d))
            except (ValueError, IndexError, ZeroDivisionError, TypeError):
                return None

        def note(name, treat, label, partner=None, raw=0, ending=None):
            if not flash:
                self.last = {"name": name, "partner": partner, "ending": ending, "riffs": frozenset((p.name, p.cell) for p in c.riffs), "size": raw}
            if not flash and c.riffs:
                self.motif.setdefault(self.motif_key(c), name)
            self.used[name] += 1
            self.combos.add((name, treat))
            self.recent.append(name)
            in_song[name] += 1
            self.count += 1
            self.log.setdefault(str(S.n), []).append(label)

        grows = set()
        if ahead is not None and not flash and not first:
            # The band is about to gain or lose a part: favour a picture that can do the same.
            for _, name in sorted(cands)[:36]:
                if W.REG[name]["fam"] == "plate" or name in W.PLATES or W.REG[name]["cost"] >= 3:
                    continue
                one, two = make(name), make(name, ctx=ahead)
                if one and two:
                    n1, n2 = len(json.dumps(one[1])), len(json.dumps(two[1]))
                    if abs(n1 - n2) > 0.03 * n1:
                        grows.add(name)
            cands = [(score - 16 * (name in grows), name) for score, name in cands]
        ranked = [name for _, name in sorted(cands)]
        # The band gains a part, or loses one, and nothing else changes: so does the picture.
        now = frozenset((p.name, p.cell) for p in c.riffs)
        if last and not flash and not prefer and kind != "hush" and not last.get("partner") and last.get("ending") and last.get("riffs") and now \
                and (last["riffs"] < now or now < last["riffs"]) and rnd(S.n, k, "grow?") < 0.75:
            name = last["name"]
            way = "more" if last["riffs"] < now else "less"
            key = next((w_ for w_ in (way, way + "2", way + "3") if (name, w_) not in self.combos), None)
            got = make(name, keep=True) if key and W.REG[name]["fam"] != "plate" and name not in W.PLATES else None
            if got and W.TREAT[last["ending"]][1](got[0], W.REG[name]):
                d, look = got
                raw = len(json.dumps(look))
                if abs(raw - last["size"]) > 0.03 * last["size"]:
                    d.arrive = "1"
                    look = W.TREAT[last["ending"]][0](d, look)
                    c.__dict__.update(d.__dict__)
                    self.grown[way] += 1
                    note(name, key, f"{name}/{way}", raw=raw, ending=last["ending"])
                    return name, way, look
        # Now and then two pictures share the frame.
        if not first and not flash and not prefer and not grows and rnd(S.n, k, "pair?") < 0.12 + 0.34 * c.full:
            pair = [n_ for n_ in ranked if W.REG[n_]["fam"] not in NO_PAIR and W.REG[n_]["cost"] <= 2 and n_ not in self.recent[-12:]]
            # The picture before, if it stood alone, carries on and is joined by a new one.
            carry = last["name"] if last and not last.get("partner") and W.REG[last["name"]]["fam"] not in NO_PAIR and W.REG[last["name"]]["cost"] <= 2 else None
            for A in ([carry] if carry else []) + pair[:6]:
                got = make(A, keep=(A == carry or A == hand_on))
                if not got:
                    continue
                for B in pair:
                    kinds = sorted((kd for kd in W.COMBOS if (A, f"{kd}+{B}") not in self.combos and (B, f"{kd}+{A}") not in self.combos), key=lambda kd: self.kinds[kd] + 2 * rnd(S.n, k, kd) - 5 * (kd in HOUSE.get(S.n, ())))
                    if B == A or W.REG[B]["fam"] == W.REG[A]["fam"] or not kinds:
                        continue
                    other = make(B, sub=1 if len(c.riffs) > 1 else 0)
                    if not other:
                        continue
                    # Where three riffs run and the band is full, now and then three pictures.
                    if len(c.riffs) >= 3 and c.full >= 0.5 and rnd(S.n, k, "trio?") < 0.45:
                        for C in pair:
                            if C in (A, B) or W.REG[C]["fam"] in (W.REG[A]["fam"], W.REG[B]["fam"]):
                                continue
                            third = make(C, sub=2)
                            if not third:
                                continue
                            kind = min(W.TRIOS, key=lambda kd: self.kinds[kd] + 2 * rnd(S.n, k, kd))
                            if (A, f"{kind}+{B}+{C}") in self.combos:
                                continue
                            look = W.TRIOS[kind](got[0], got[1], other[1], third[1])
                            self.kinds[kind] += 1
                            self.treats[kind] += 1
                            self.trios += 1
                            note(A, f"{kind}+{B}+{C}", f"{A}+{B}+{C}/{kind}", partner=B)
                            self.chains += A == carry
                            self.used[B] += 1
                            self.used[C] += 1
                            return A, f"{kind}+{B}+{C}", look
                    kind = kinds[0]
                    look = W.COMBOS[kind](got[0], got[1], other[1])
                    self.kinds[kind] += 1
                    self.treats[kind] += 1
                    note(A, f"{kind}+{B}", f"{A}+{B}/{kind}", partner=B)
                    self.chains += A == carry
                    self.used[B] += 1
                    self.count -= 0
                    return A, f"{kind}+{B}", look
        for name in ranked:
            info = W.REG[name]
            got = make(name)
            if not got:
                continue
            if name == hand_on:
                got = make(name, keep=True) or got
            d, look = got
            c.__dict__.update(d.__dict__)
            # Its first time it is seen plain; after that, through something it has not been seen through.
            order = sorted((t for t, (_, ok) in W.TREAT.items() if t != "plain" and (name, t) not in self.combos and ok(c, info)),
                           key=lambda t: self.treats[t] + 2 * rnd(S.n, k, t) - 6 * (t in HOUSE.get(S.n, ())))
            if info["fam"] == "plate":
                order = []          # the first film's studies come as they were, and once
            if name in W.BOLD:
                # Pictures made of lines and points keep to guises that add to them: a print of a hair line is nothing.
                order = [t for t in order if t in W.FILLS]
            if first:
                # A song opens on its picture as it is, or in a guise that leaves it whole.
                order = [t for t in order if t in ("fringe", "relief", "solar", "leaded", "echo", "water", "blown", "ball", "falling", "mirror", "kaleido", "smoked", "infra", "tracking")]
            plain_ok = (name, "plain") not in self.combos
            treat = "plain" if (plain_ok and (self.used[name] == 0 or first or name == hand_on or rnd(S.n, k, "plain?") < 0.25)) or not order else order[0]
            if treat == "plain" and not plain_ok:
                continue            # it has been seen every way it can be
            if flash:
                # Nothing that needs time to build.
                order = [t for t in order if t in ("kaleido", "mirror", "duotone", "dots", "newsprint", "engraved", "hatched", "onebit", "drawn", "blueprint", "typed", "negative", "lines", "fringe", "wall", "planet",
                                                   "solar", "relief", "poster", "flood")]
                treat = order[0] if order and (self.used[name] or not plain_ok) else "plain" if plain_ok else None
                if treat is None:
                    continue
            c.arrive = "1"
            raw = len(json.dumps(look))
            if treat in W.ARRIVES and not flash and (c.b16 - c.a16) * c.six >= 5.5 and rnd(S.n, k, "arrive?") < 0.45:
                # It begins as itself, and the treatment comes on where the riff comes round
                # part way through (or it begins treated and comes out of it).
                lead = W._lead(c)
                cell = lead.cell or 16
                at = c.a16 + (0.4 + 0.2 * rnd(S.n, k, "when")) * (c.b16 - c.a16)
                m = (lead.anchor + round((at - lead.anchor) / cell) * cell) / 4
                on = f"smooth({m - 0.12:g}, {m + 0.12:g}, time.beat)"
                c.arrive = on if self.arrivals % 2 == 0 else f"(1 - {on})"
                self.arrivals += 1
            # Where the music is full a picture may wear two guises at once.
            second = None
            if treat in W.STACK and not flash and not first and name != hand_on and c.full >= 0.55 and rnd(S.n, k, "stack?") < 0.5:
                more = sorted((t for t in W.STACK if W.STACK[t] != W.STACK[treat] and (name, t) not in self.combos and W.TREAT[t][1](c, info) and (name not in W.BOLD or t in W.FILLS)
                               and (treat, t) not in W.STACK_BAD and (t, treat) not in W.STACK_BAD),
                              key=lambda t: self.stacks[t] + 2 * rnd(S.n, k, "st" + t))
                if more:
                    second = more[0]
            if second:
                first_, last_ = sorted((treat, second), key=lambda t: W.STACK[t])
                look = W.TREAT[last_][0](c, W.TREAT[first_][0](c, look))
                self.treats[treat] += 1
                self.stacks[second] += 1
                self.combos.add((name, second))
                both = f"{first_},{last_}"
                note(name, treat, f"{name}/{both}", raw=raw, ending=None)
                return name, both, look
            look = W.TREAT[treat][0](c, look)
            self.treats[treat] += 1
            note(name, treat, name if treat == "plain" else f"{name}/{treat}", raw=raw, ending="plain" if c.arrive.startswith("(1 -") else treat)
            return name, treat, look
        raise RuntimeError(f"nothing fits t{S.n} scene {k}")


def ruled(S, rnd_, look):
    """The frame keeps count of a long round. While the round lasts, whatever the pictures
    do, a line is ruled round the edge of the frame a sixteenth at a time, and each of the
    round's riffs leaves a mark on it wherever it begins a turn: one riff's marks outside
    the line, the next one's inside. The corner where the line began is where the riffs
    meet: the only place where their marks fall together."""
    a, z, per, _, tracks, cells = rnd_
    anchors = [t.anchor(a, z, c) for t, c in zip(tracks, cells)]
    if any(x is None for x in anchors):
        return look
    # The sixteenth at which the most of them begin a turn together (all, if they ever do).
    m = max(range(a, a + per), key=lambda x: (sum((x - an) % c == 0 for an, c in zip(anchors, cells)), -x))
    Wd, Hd = 1.71, 0.93

    def at(u, d=0.0):
        w, h = Wd + d, Hd + d
        s = f"(fract({u})*{4 * w + 4 * h:g})"
        return (f"0 - {w:g} + clamp({s}, 0, {2 * w:g}) - clamp({s} - {2 * w + 2 * h:g}, 0, {2 * w:g})",
                f"{h:g} - clamp({s} - {2 * w:g}, 0, {2 * h:g}) + clamp({s} - {4 * w + 2 * h:g}, 0, {2 * h:g})")
    now = "time.beat*4"
    gone = f"(1 - smooth({z / 4:g}, {z / 4 + 1:g}, time.beat))"
    n_ = min(z - a, per)
    x, y = at(f"({a - m} + inst.i)/{per}")
    over = [{"type": "shape", "repeat": n_, "sides": 1, "radius": 0.006, "fill": 1, "width": 0, "color": "#f2efe6", "x": x, "y": y, "opacity": f"0.85*step({a} + inst.i, {now})*{gone}"}]
    pal = PALS[S.n]
    for i, (t, c, an) in enumerate(zip(tracks, cells, anchors)):
        first = an + -(-(a - an) // c) * c
        count = min((z - 1 - first) // c + 1, per // c)
        if count < 1:
            continue
        when = f"({first} + inst.i*{c})"
        x, y = at(f"({first - m} + inst.i*{c})/{per}", (0.034, -0.034, -0.068)[i % 3])
        size = f"*(1 + 1.4*exp(0 - 0.6*max({now} - {when}, 0)))"
        seen = f"step({when}, {now})*{gone}"
        over.append({"type": "shape", "repeat": count, "sides": 4, "rotate": 0.125, "radius": f"0.023{size}", "fill": 1, "width": 0, "color": "#000000", "blend": "normal", "x": x, "y": y, "opacity": seen})
        over.append({"type": "shape", "repeat": count, "sides": 4, "rotate": 0.125, "radius": f"0.017{size}", "fill": 1, "width": 0, "color": pal[3 + i % 3], "blend": "normal", "x": x, "y": y, "opacity": seen})
    return {"background": "#000000", "layers": [W._act(look, blend="normal")] + over, "filters": []}


def odd_turns(S, c):
    """Where the scene's first riff is played differently for a turn or two among many that
    are alike: the sixteenths at which those turns begin."""
    if not c.riffs:
        return []
    p = c.riffs[0]
    T = next((t for t in S.tracks if t.name == p.name), None) if not isinstance(S.tracks, dict) else S.tracks.get(p.name)
    if T is None or not p.cell or p.cell * c.six < 0.45:
        return []           # a turn too short to see
    pats, t = {}, math.ceil((c.a16 - p.anchor) / p.cell)
    while p.anchor + (t + 1) * p.cell <= c.b16:
        lo = p.anchor + t * p.cell
        pats[lo] = frozenset(int(s - lo) for s in T.grid if lo <= s < lo + p.cell)
        t += 1
    if len(pats) < 4:
        return []
    base = collections.Counter(pats.values()).most_common(1)[0][0]
    odd = [lo for lo, q in pats.items() if q != base and q]
    return odd if 1 <= len(odd) <= max(1, len(pats) // 5) and len(odd) <= 2 else []


def white(look, amount):
    """Light over the whole picture (a burn-out, a flash), whatever it is made of."""
    look.setdefault("layers", []).append({"type": "shape", "sides": 4, "rotate": 0.125, "radius": 2.7, "width": 0, "fill": 1, "color": "#ffffff", "blend": "add", "x": 0, "y": 0, "opacity": amount})


def gathering(look, t, need):
    """A look with the hands of the great round over it: one ring for each length of riff and
    one for the bar, a mark going round each once a turn; they stand in a line at the top only
    at the sixteenth `t`. They come up over the eight bars before."""
    cells = sorted(need) + [16]
    up = f"smooth({t / 4 - 44:g}, {t / 4 - 30:g}, time.beat)"
    over = []
    for i, cell in enumerate(cells):
        r = 0.34 + 0.13 * i
        ph = f"(0.25 - (time.beat*4 - {t})/{cell})"
        near = f"exp(0 - 6*abs(fract((time.beat*4 - {t})/{cell} + 0.5) - 0.5))"
        over.append({"type": "shape", "sides": 0, "radius": r, "width": 0.003, "fill": 0, "color": "#ffffff", "blend": "add", "opacity": f"0.35*{up}"})
        over.append({"type": "shape", "sides": 1, "radius": f"0.022 + 0.02*{near}", "width": 0, "fill": 1, "color": "#ffffff", "blend": "add", "x": f"{r}*cos({ph})", "y": f"{r}*sin({ph})", "opacity": f"{up}"})
    over.append({"type": "shape", "repeat": 12, "sides": 1, "radius": 0.005, "width": 0, "fill": 1, "color": "#ffffff", "blend": "add", "x": 0, "y": f"0.3 + inst.i*{(0.34 + 0.13 * (len(cells) - 1) - 0.26) / 11:g}", "opacity": f"0.5*{up}"})
    return {"background": "#000000", "layers": [W._act(look, blend="normal")] + over, "filters": []}


def plan(S, deal):
    """A song's scenes: [(a16, b16, idiom, treatment, scene dict, context)]."""
    deal.song_used = collections.Counter()
    deal.motif = {}
    deal.last = None
    out = []
    was_flash = False
    last_shift = 0
    cuts = cut(S)
    shifts = {}
    for k, (a16, b16, cyc, kind) in enumerate(cuts):
        flash = kind == "flash"
        c = S.cx(a16, b16, k=k, cyc=cyc)
        # The next scene that is not a flash: does the band only gain or lose a part there?
        ahead = None
        j = next((j for j in range(k + 1, len(cuts)) if cuts[j][3] != "flash"), None)
        if j is not None and not flash and cuts[j][3] != "hush" and j < len(cuts) - 1:
            c2 = S.cx(cuts[j][0], cuts[j][1], k=j, cyc=cuts[j][2])
            r1, r2 = frozenset((p.name, p.cell) for p in c.riffs), frozenset((p.name, p.cell) for p in c2.riffs)
            if r1 and r2 and (r1 < r2 or r2 < r1):
                ahead = c2
        landed = None
        if kind == "landing" and out:
            # The great round is over: everything is where it was when the song began, and so is the picture.
            try:
                c0 = S.cx(a16, b16, k=0, cyc=cyc)
                c0.riffs = out[0][5].riffs      # (the wheels as they were, though they have stopped sounding)
                landed = (out[0][2], "landing", W.bolder(out[0][2], W.REG[out[0][2]]["f"](c0)))
                deal.used[out[0][2]] += 1
                deal.recent.append(out[0][2])
                deal.last = None
                deal.log.setdefault(str(S.n), []).append(f"{out[0][2]}/landing")
                deal.landings += 1
            except (ValueError, IndexError, ZeroDivisionError, TypeError):
                landed = None
        name, treat, look = landed or deal.choose(S, c, k, first=(k == 0), flash=flash, prefer=(deal.album_first if S.n == 17 else out[0][2]) if k and k == len(cuts) - 1 and len(cuts) > 12 else None, kind=kind, ahead=ahead,
                                       final=(k == len(cuts) - 1))
        if deal.album_first is None:
            deal.album_first = name     # the album ends on the picture it began with, changed
        deal.dyn[kind] += 1
        # Each length of riff has its own cast of colour in a song: the first as the song's
        # colours are, each new length a step round from them, and back when a length returns.
        cell = c.riffs[0].cell if c.riffs else 16
        shift = shifts.setdefault(cell, (0, 0.07, -0.07, 0.14, -0.14, 0.21, -0.21, 0.28)[len(shifts) % 8])
        if treat in ("more", "less"):
            shift = last_shift      # the same picture with a part more or less: in the same colours
        if not flash:
            last_shift = shift
        if shift and not flash and not any(L.get("type") == "sky" for L in look.get("layers", [])) and W.REG[name]["fam"] not in ("plate", "ground"):
            look.setdefault("filters", []).append({"type": "hue", "shift": shift})
        deal.flashes += flash
        scene = {"at": 0 if k == 0 else f"{a16 // 16}bar" if a16 % 16 == 0 else f"{a16 / 4:g}b", "look": look}
        still = any(t in ("roll", "spin", "hole", "sheet", "kaleido", "mirror", "tunnel", "slices", "wall", "planet", "wound") for t in treat.split(",")) or name in W.PLATES or W.REG[name]["fam"] in ("plate", "sheet", "sign")
        if k and not flash and not still and treat not in ("more", "less") and (b16 - a16) * c.six >= 4.5 and rnd(S.n, k, "move?") < 0.5:
            # The camera over the picture does one thing in the scene, each kind in its turn.
            bars_ = S.full[a16 // 16:max(a16 // 16 + 1, b16 // 16)]
            after = S.full[min(b16 // 16, S.bars - 1):min(b16 // 16 + 2, S.bars)] or bars_
            slope = sum(after) / len(after) - sum(bars_) / len(bars_)
            way = 1 if slope > 0.1 else -1 if slope < -0.1 else 0
            mv = min(W.MOVES_FOR[way], key=lambda m_: deal.moves[m_] + 1.5 * rnd(S.n, k, m_))
            deal.moves[mv] += 1
            look = W.rostrum(c, look, mv)
        if not flash and "+" not in treat and len(c.riffs) >= 2 and c.riffs[0].cell != c.riffs[1].cell and 40 <= math.lcm(c.riffs[0].cell, c.riffs[1].cell) and name not in W.PLATES:
            # Whenever the scene's first two riffs come round together the picture catches the light.
            A, B = c.riffs[0], c.riffs[1]
            meet = f"exp(0 - 2.5*fract({A.turn})*{A.cell})*exp(0 - 2.5*fract({B.turn})*{B.cell})"
            look.setdefault("filters", []).append({"type": "color", "exposure": f"1 + 1.6*{meet}"})
        odd = odd_turns(S, c) if not flash and kind != "hush" else []
        if odd:
            # The riff is played differently once (or twice) in the scene: for that turn the picture is its negative.
            p = c.riffs[0]
            when = " + ".join(f"step({lo / 4:g}, time.beat)*step(time.beat, {(lo + p.cell) / 4 - 0.02:g})" for lo in odd)
            look.setdefault("filters", []).append({"type": "invert", "amount": f"min({when}, 1)" if len(odd) > 1 else when})
            deal.odd += len(odd)
        if cyc and b16 == min(S.bars * 16, a16 + ((b16 - a16) // cyc["round"] or 1) * cyc["round"]) and any(z == b16 for _, z, *_ in S.rounds):
            # The scene ends where a long round does: the picture burns out on the meeting.
            look.setdefault("filters", []).append({"type": "color", "exposure": f"1 + 5*pow(smooth({b16 / 4 - 1:g}, {b16 / 4:g}, time.beat), 3)"})
            white(look, f"0.7*pow(smooth({b16 / 4 - 1:g}, {b16 / 4:g}, time.beat), 3)")
        for t, need in S.landings:
            if a16 < t <= a16 + 16 * 12 and not flash and b16 <= t:
                # The great round is nearly over: a hand for each length of riff comes up over the
                # picture, each going round once in its own turn, and all of them reach the top
                # together only at the landing.
                look = scene["look"] = gathering(look, t, need)
                if b16 == t:
                    white(look, f"pow(smooth({t / 4 - 3:g}, {t / 4:g}, time.beat), 2.5)")
        if kind == "landing":
            since = f"max(time.beat - {a16 / 4:g}, 0)"
            white(look, f"exp(0 - 0.9*{since})")
        if kind == "hush":
            # The band has stopped: the picture is drained and dim until it comes back in.
            look.setdefault("filters", []).append({"type": "color", "saturation": 0.1, "exposure": 0.5})
        if kind == "drop":
            # The band comes in: the picture is struck with light and comes forward, then settles.
            since = f"max(time.beat - {a16 / 4:g}, 0)"
            look.setdefault("filters", []).extend([{"type": "camera", "zoom": f"1 + 0.22*exp(0 - 2.5*{since})"}, {"type": "color", "exposure": f"1 + 3.5*exp(0 - 4*{since})"}])
            white(look, f"0.45*exp(0 - 5*{since})")
        if k and name in W.PLATES and "+" not in treat:
            scene["lead"] = "2bar" if name == "photofinish" else "1bar"
        elif k and not kind and not was_flash and treat not in ("more", "less") and rnd(S.n, k, "x") < 0.34:
            # One picture turns into the next: each way in its turn, over a beat or two.
            tr = min(TRANSITIONS, key=lambda t_: deal.trans[t_] + 1.5 * rnd(S.n, k, t_))
            deal.trans[tr] += 1
            scene["xfade"] = "1b" if tr in ("push", "strips", "blocks", "split", "weave", "checker", "flip", "squeeze", "whip", "fall", "glitch", "pixel", "doors", "scan", "slats", "interlace", "shutter") else "2b"
            scene["transition"] = tr
        if cyc:
            # The scene lies in a long round: the frame keeps count of it across the cuts.
            whole = next((r for r in S.rounds if r[0] <= a16 and b16 <= r[1]), None)
            if whole:
                scene["look"] = ruled(S, whole, look)
                deal.ruled += 1
        out.append((a16, b16, name, treat, scene, c))
        was_flash = bool(kind)
    return out


def main():
    out_dir = os.path.join(HERE, "..", "film")
    for a in sys.argv[1:]:
        if a.startswith("--out="):
            out_dir = a[6:]
    out_dir = os.path.abspath(out_dir)
    args = [int(a) for a in sys.argv[1:] if not a.startswith("--")]
    show = "--plan" in sys.argv
    deal = Deal()
    total = collections.Counter()
    for t in C.ALBUM["tracks"]:
        num = int(t["n"])
        if "--solo" in sys.argv and args and num not in args:
            continue
        S = Song(num)
        scenes = plan(S, deal)
        for *_, name, treat, _, _ in scenes:
            total[name] += 1
        if args and num not in args:
            continue
        six = S.bar_s / 16
        if show:
            print(f"{S.id} \"{S.title}\": {S.bars} bars, {S.d['bpm']:.0f} bpm, {len(scenes)} scenes, {sum((b - a) for a, b, *_ in scenes) * six / len(scenes):.1f} s each")
            for a, b, name, treat, _, c in scenes:
                print(f"  {a / 16:7.2f}-{b / 16:<7.2f} {(b - a) * six:5.1f}s  {name:12s} {treat:9s} {' '.join(f'{p.name}:{p.cell}' for p in c.riffs[:4])}"
                      + (f"  tune {c.tunes[0].name}" if c.tunes else "") + ("  paper" if c.paper else ""))
            continue
        os.makedirs(out_dir, exist_ok=True)
        head = (f"# chirpers10 t{num} \"{S.title}\": written by compose/chirpers10/vis-gen/wildgen.py from the song's own notes\n"
                f"# ({S.bars} bars; {len(scenes)} scenes). Do not edit: run wildgen.py {num} again when the song changes.\n")
        prog = {"fade": ["1bar", "2bar"], "master": W.master(S.title, S.n - 1), "scenes": [sc for *_, sc, _ in scenes]}
        open(os.path.join(out_dir, f"{S.id}.yaml"), "w").write(head + json.dumps(prog, indent=1) + "\n")
        print(f"{S.id}: {len(scenes)} scenes: " + " ".join(f"{n_}{'' if t_ == 'plain' else '/' + t_}" for _, _, n_, t_, _, _ in scenes))
    if not show and not args:
        # What was dealt, scene by scene (for the proof sheets).
        json.dump(deal.log, open(os.path.join(out_dir, "plan.json"), "w"))
    if show or "--tally" in sys.argv:
        print(f"album: {deal.count} scenes, {len(total)} idioms, {len(deal.combos)} different pictures")
        print("  " + "  ".join(f"{n_}:{k}" for n_, k in total.most_common()))
        print("  treatments: " + "  ".join(f"{n_}:{k}" for n_, k in deal.treats.most_common()))
        print("  turns into: " + "  ".join(f"{n_}:{k}" for n_, k in deal.trans.most_common()))
        print(f"  the band comes in: {deal.dyn['drop']}  hushed bars: {deal.dyn['hush']}  pictures joined by the next: {deal.chains}  pictures that gain a part with the band: {deal.grown['more']}, lose one: {deal.grown['less']}  scenes in a ruled frame: {deal.ruled}  two guises at once: {sum(deal.stacks.values())}  three pictures at once: {deal.trios}  a turn played differently: {deal.odd}  landings: {deal.landings}")
        print(f"  flashes: {deal.flashes}  treatments that arrive or leave: {deal.arrivals}  camera: " + "  ".join(f"{n_}:{k}" for n_, k in deal.moves.most_common()))


if __name__ == "__main__":
    main()
