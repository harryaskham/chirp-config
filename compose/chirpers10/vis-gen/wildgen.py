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
    1: ("loom", "remainder", "crystal", "helix", "billiard", "riley", "reels", "torusknot"), 2: ("sympathy", "pendwave", "strings", "cradle", "seesaw", "ink", "strobe", "worldlines"), 3: ("changes", "maypole", "chorus", "stringart", "drill", "vasarely"),
    4: ("abacus", "tally", "dominoes", "automaton", "odometer", "hanoi", "barcode", "dice", "hilbert", "sandpile"), 5: ("stairs", "ridges", "escalator", "flight", "lifts", "trampoline", "suprematist", "barber"), 6: ("colony", "bifurcate", "automaton", "anemone", "lava", "marbling", "ripplebath", "mycelium"),
    7: ("rabbits", "golden", "spiral", "sunflower", "mandala", "star", "kandinsky", "courses"), 8: ("loom", "tartan", "solkattu", "musicbox", "specimen", "breakout", "measure", "reels", "hilbert"), 9: ("henge", "orrery", "moons", "grove", "snow", "sundial", "dice", "torusknot", "clockfield"),
    10: ("balance", "coins", "tape", "galton", "duel", "hourglass", "barcode", "sandpile"), 11: ("doors", "blinds", "press", "hammers", "tesla", "albers", "portals"), 12: ("hands", "juggle", "semaphore", "chorus", "fan", "shadowplay", "braille"),
    13: ("eclipse", "pond", "spiral", "lanterns", "rink", "zen", "braille", "ripplebath", "worldlines"), 14: ("numerals", "tally", "zoetrope", "seismo", "leader", "hourglass", "strobe", "dice", "clockfield"), 15: ("slack", "ropes", "wires", "swings", "switchboard", "rothko", "mycelium"),
    16: ("beats", "moire", "chladni", "eclipse", "lighthouse", "billiard", "candles", "ripplebath"), 17: ("hailstone", "railway", "highway", "gates", "constellation", "searchlights", "sundial", "phasecorridor", "kaleidohall"),
}
# Each song's house: the guises and the ways of sharing the frame it leans to, so the songs
# differ from one another as well as from bar to bar. (The first song, the album's argument, has none.)
HOUSE = {
    2: "echo water blown mirror stop slices ball double lighten diptych satellite cutout smoked delayed puzzle warpby timemap standing scanfold prismby spiralcut duochrono metered recoil boomerang receding exposed ringed janus",
    3: "lines engraved hatched typed sheet blueprint leaded strips bands intercut triptych stencil woven sampler knitted itself diagonal woodcut etched cathedral",
    4: "typed onebit newsprint dots blocks combed poster board corner card strips tracking puzzle beaded bricks halves louvers riso hexcut",
    5: "relief planet hole tunnel falling blown duotone sweep window nest bands cutout infra screen ridged papercut embossed stagepass anamorph spiralcut conformal metered receding",
    6: "overgrown wound warp solar leaded kaleido flood difference lighten iris rings glass dripping beaded halves warpby hyperbolic anamorph prismby spiralcut conformal cathedral",
    7: "coiled falling kaleido spin wall wound ball nest rings wedges satellite glass woven bricks papercut itself diamond hyperbolic anamorph hexcut conformal cathedral",
    8: "leaded engraved newsprint poster flood duotone mirror triptych diptych window board infra woven puzzle bricks halves louvers woodcut riso etched cathedral",
    9: "stop slices echo fringe roll relief drawn double iris sweep corner cutout smoked delayed papercut reeded timemap scanfold hexcut duochrono metered looped boomerang filmclock ringed",
    10: "onebit dots torn combed typed poster negative difference card bands corner stencil dripping sampler beaded carried negmask woodcut riso etched recoil looped",
    11: "mirror roll spin sheet blocks torn wall diptych sweep card intercut tracking screen papercut puzzle louvers stagepass prismby hexcut mirrorby metered filmclock",
    12: "mirror drawn blueprint hatched ball echo water diptych intercut lighten satellite cutout screen papercut diagonal negmask timemap woodcut scanfold etched mirrorby janus",
    13: "echo stop slices fringe water overgrown hole double window iris difference glass smoked negative stencil ridged carried embossed timemap scanfold spiralcut duochrono cathedral metered boomerang exposed janus",
    14: "typed dots lines blocks sheet onebit stop strips board wedges triptych stencil delayed beaded bricks louvers reeded standing scanfold hexcut duochrono metered looped recoil filmclock exposed ringed",
    15: "warp wound blown torn water combed tunnel sweep bands double satellite dripping woven knitted sampler carried warpby standing spiralcut duochrono exposed",
    16: "fringe duotone solar relief falling planet leaded lighten difference nest window glass tracking delayed ridged reeded embossed standing anamorph prismby conformal cathedral metered filmclock",
    17: "tunnel falling planet roll blown ball flood wedges rings nest card stencil infra screen puzzle ridged itself diamond hyperbolic stagepass anamorph hexcut conformal metered receding",
}
HOUSE = {n_: set(v.split()) for n_, v in HOUSE.items()}
OPEN = {1: "stringart"}     # the picture a song opens on, where it is not the first of its featured ones (the album's first picture, and the one the landing brings back)
TRANSITIONS = ("melt", "luma", "push", "strips", "burn", "blocks", "zoom", "weave", "spiral", "rings", "checker", "split", "wipe", "iris", "blinds", "clock", "diamond", "rise", "dissolve",
               "flip", "squeeze", "shred", "stretch", "whip", "fall", "whirl", "ripple", "glitch", "pixel", "tiles", "doors", "spin", "scan", "diagonal", "slats", "interlace", "star", "dither", "corners", "wave",
               "fan", "shutter", "mosh", "smoke", "overgrow", "echo", "drip", "inkbleed",
               "phase", "canon", "rung", "sum", "barber", "halving", "golden", "euclid", "dealt", "owed", "leaf", "negative", "ritard", "haul", "beats", "stairs",
               "displace", "prism", "aperture", "accordion", "pendulum", "gear", "orbit", "chromatic",
               "cube", "shatter", "kaleido", "polar", "fold", "louver",
               "vortex", "carousel", "ribbon", "shockwave", "facet", "slitcurtain", "spiralwipe", "mosaicflip", "helixwipe", "parallax", "rhombus", "gravity", "tube", "nodal",
               "rewind", "stutter", "flipbook", "timewipe", "timeiris")
# Ways that suit the music coming up over the cut (the next bars fuller than the last: a roll, a blow, a rush in)
# and ways that suit it falling away (a wind-down, a letting go). A cut where the band neither gains nor loses takes any.
TR_UP = set("stutter zoom whip shockwave burn shatter aperture tube spin whirl star prism chromatic glitch push rise iris vortex timeiris".split())
TR_DOWN = set("melt fall drip smoke ritard rewind gravity dissolve inkbleed overgrow fold accordion squeeze stretch blinds halving owed leaf".split())
# Ways that keep something of the old picture from frame to frame: they take longer (about two seconds).
CARRIED = ("mosh", "smoke", "overgrow", "echo", "drip", "inkbleed")
# Ways that record the old picture as the change begins and play the recording (a tape wound back; a roll into the cut).
TAPED = {"rewind": 2.4, "stutter": 1.9, "flipbook": 1.9, "timewipe": 1.9, "timeiris": 1.9}
# Ways that count or move mechanically (counted.rs): the dense ones need about two seconds to be read, the rest a second and a half.
COUNTED = {"rung": 1.9, "sum": 1.9, "euclid": 1.9, "dealt": 1.9, "golden": 1.9, "halving": 1.9, "ritard": 1.9, "stairs": 1.9,
           "phase": 1.4, "canon": 1.4, "barber": 1.4, "owed": 1.4, "leaf": 1.4, "negative": 1.4, "haul": 1.4, "beats": 1.4,
           "displace": 1.6, "prism": 1.6, "aperture": 1.6, "accordion": 1.7, "pendulum": 1.4, "gear": 1.7, "orbit": 1.8, "chromatic": 1.5,
           "cube": 1.5, "shatter": 1.6, "kaleido": 1.6, "polar": 1.6, "fold": 1.6, "louver": 1.6,
           "vortex": 1.6, "carousel": 1.7, "ribbon": 1.6, "shockwave": 1.5, "facet": 1.7, "slitcurtain": 1.6, "spiralwipe": 1.5, "mosaicflip": 1.7,
           "helixwipe": 1.6, "parallax": 1.5, "rhombus": 1.6, "gravity": 1.6, "tube": 1.5, "nodal": 1.8}
# How each song passes into the next: its own idea, counted out over its last two bars
# (the wheels going round at their own rates; the row rung; the oblong cut into its squares).
# After the last song the walk comes up in black.
SEAMS = {1: "phase", 2: "canon", 3: "rung", 4: "sum", 5: "barber", 6: "halving", 7: "golden", 8: "euclid", 9: "dealt", 10: "owed", 11: "leaf",
         12: "flip", 13: "negative", 14: "ritard", 15: "haul", 16: "beats", 17: "stairs"}
NO_PAIR = ("room", "sheet", "plate", "travel", "space")      # families that are not put in a frame with another


def rnd(*key):
    """A fixed random number 0..1 for a key."""
    import hashlib
    return int(hashlib.sha1(repr(key).encode()).hexdigest()[:8], 16) / 0xffffffff


def reprises(S):
    """Where a song plays its opening again: the bar lines (as sixteenths), past the song's
    middle, at which three parts or more play their own first two bars once more, note for
    note, after having played other things. The first such place only."""
    tracks = [t for t in (S.tracks.values() if isinstance(S.tracks, dict) else S.tracks) if t.role != "drum"]
    early = max(12, int(0.15 * S.bars))
    votes = collections.Counter()
    for t in tracks:
        bars = [frozenset((j, t.grid.get(b * 16 + j)) for j in range(16) if t.grid.get(b * 16 + j) is not None) for b in range(S.bars)]
        o = next((b for b in range(min(early, S.bars - 2)) if len(bars[b]) >= 2 and len(bars[b + 1]) >= 2), None)
        if o is None:
            continue
        other = next((b for b in range(o + 2, S.bars - 1) if bars[b] != bars[o + (b - o) % 2]), None)
        if other is None:
            continue
        for b in range(max(other + 8, int(0.6 * S.bars)), S.bars - 1):
            if bars[b] == bars[o] and bars[b + 1] == bars[o + 1] and not (bars[b - 2] == bars[o] and bars[b - 1] == bars[o + 1]):
                votes[b] += 1
    best = [b for b, v in sorted(votes.items()) if v >= 3]
    return [best[0] * 16] if best else []


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
    S.reprises = [t for t in reprises(S) if not any(abs(t - x) < 64 for x, _ in S.landings)]
    edges |= set(S.reprises)
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
    for t in S.reprises:
        for i, (p, q, cyc, kind) in enumerate(out):
            if p == t and kind in (None, "drop"):
                out[i] = (p, q, cyc, "reprise")
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
        self.reprises = 0
        self.canons = 0
        self.joins = collections.Counter()
        self.canon_own = {}
        self.canon_far = collections.defaultdict(set)
        self.dealt = collections.defaultdict(set)
        self.sums = 0
        self.walks = 0
        self.rings = 0
        self.measures = 0
        self.rolled = 0
        self.grounds = collections.Counter()
        self.grounds_last = collections.defaultdict(list)
        self.ledgers = 0
        self.owed = collections.defaultdict(set)
        self.rolls_in = collections.Counter()
        self.sized = collections.Counter()
        self.tuned = collections.Counter()
        self.hauls = collections.defaultdict(set)
        self.spires = collections.defaultdict(set)
        self.gears = collections.defaultdict(set)
        self.rules = collections.defaultdict(set)
        self.overtones = collections.defaultdict(set)
        self.septs = collections.defaultdict(set)
        self.recounts = collections.defaultdict(set)
        self.palins = collections.defaultdict(set)
        self.measured = collections.defaultdict(set)
        self.rung = collections.defaultdict(set)
        self.walked = collections.defaultdict(set)
        self.hinges = 0
        self.period = {}
        self.fits = 0
        self.hands = 0
        self.deals = 0
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
            if info["max_cell"] < 64 and any((p_.cell or 0) > info["max_cell"] for p_ in c.riffs[:max(info["needs"], 1)]):
                continue        # it was made for a shorter riff than this (a candle a sixteenth: not thirty-four)
            if first and (info["cost"] >= 3 or info["fam"] in ("plate", "room", "travel")):
                continue
            if name in FIGURES and S.n not in FIGURES[name]:
                continue        # figures only where the song is about counting
            if flash and (info["cost"] >= 3 or info["fam"] in ("plate", "travel", "sheet", "trace", "grow") or name in W.PLATES or name in W.SLOW):
                continue        # a flash has no time to draw anything out
            if not flash and (name in W.SLOW and secs < 3.8 or name in W.LONG and secs < 5.5):
                continue        # it takes longer than this to become anything
            if name in W.FED and (first or final or busiest < max(5, 1.4 * secs)):
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
                if first:
                    score -= 70 - 6 * FEATURE[S.n].index(name)     # a song opens on a picture of what it is about: the first of these that can be drawn here
            if first and name == OPEN.get(S.n):
                score -= 80
            if name in W.WANTS and in_song[name] < 3 and W.WANTS[name](c) and (name != "beats" or name in FEATURE.get(S.n, ())):
                score -= 18         # it is at its best here
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
            d.idiom = name
            rot = d.variant % 3
            d.a, d.b, d.c = (d.a, d.b, d.c)[rot:] + (d.a, d.b, d.c)[:rot]
            try:
                return d, W.bolder(name, W.REG[name]["f"](d))
            except (ValueError, IndexError, ZeroDivisionError, TypeError):
                return None

        def note(name, treat, label, partner=None, raw=0, ending=None):
            if not flash:
                self.last = {"name": name, "partner": partner, "ending": ending, "riffs": frozenset((p.name, p.cell) for p in c.riffs), "size": raw,
                             "lead": next((p.cell for p in c.riffs if p.role != "drum"), None), "drum": next((p.cell for p in c.riffs if p.role == "drum"), None)}
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
        # The hinge: the riff carries on unchanged while the drummer changes step between twos and
        # threes (six quick steps for four broad ones). The picture carries on too, and swings
        # round: it is seen from its other side.
        lead_now = next((p.cell for p in c.riffs if p.role != "drum"), None)
        drum_now = next((p.cell for p in c.riffs if p.role == "drum"), None)
        if last and not flash and not prefer and kind != "hush" and not last.get("partner") and last.get("ending") and lead_now and drum_now \
                and last.get("lead") == lead_now and last.get("drum") and (last["drum"] % 3 == 0) != (drum_now % 3 == 0):
            name = last["name"]
            key = next((w_ for w_ in ("hinge", "hinge2", "hinge3") if (name, w_) not in self.combos), None)
            got = make(name, keep=True) if key and W.REG[name]["fam"] != "plate" and name not in W.PLATES else None
            if got and W.TREAT[last["ending"]][1](got[0], W.REG[name]):
                d, look = got
                d.arrive = "1"
                look = W.TREAT[last["ending"]][0](d, W.ground(d, look, last.get("ground")))
                side = not last.get("flipped")
                if side:
                    look = W.flipped(look)
                c.__dict__.update(d.__dict__)
                c.talk = f"the drums change step from {last['drum']} to {drum_now} under the same riff"
                self.hinges += 1
                note(name, key, f"{name}/hinge", raw=len(json.dumps(look)), ending=last["ending"])
                self.last["flipped"] = side
                self.last["ground"] = last.get("ground")
                return name, "hinge", look
        # The song's own canon (the first it is dealt, one of its featured pictures if it can
        # be) is shown whole once while the parts are still in step, and comes back each time
        # they are a whole sixteenth further apart than it has been seen.
        pair2, own = None, self.canon_own.get(S.n)
        ms_ = measuring(S, c) if not flash and not prefer and not first and kind != "hush" and (c.b16 - c.a16) * c.six >= 3.5 else None
        unmeasured = bool(ms_) and ms_[0] not in self.measured[S.n]
        if not flash and not prefer and kind != "hush" and not unmeasured:
            pair2 = stereo(S, c)
            if not pair2 and not own and not first:
                pair2 = stereo(S, c, whole=True)
        if pair2 and (pair2[2] == 0 or rnd(S.n, k, "canon?") < 0.7) and not (last and last.get("canon") and rnd(S.n, k, "canon again?") < 0.35):
            behind, ahead_, far = pair2
            rest = [p for p in c.riffs if p.name[:-1] != behind.name[:-1]]
            how = "half" if far == 0 else min(W.JOINS, key=lambda j: (self.joins[(S.n, j)], self.joins[j], rnd(S.n, k, j)))
            again = own and far == int(far) and far not in self.canon_far[S.n] and own not in self.recent[-2:]
            featured = [] if own else [f for f in ranked if f in W.STRONG][:2]
            for name in ([own] if again else featured) + ranked:
                tag = f"canon{far:g}" if name == own and again or far == 0 else "canon"
                if name not in W.CANON or (name, tag) in self.combos or (first and W.REG[name]["cost"] >= 3):
                    continue
                cl, cr = copy.copy(base), copy.copy(base)
                cl.riffs, cr.riffs = [behind] + rest, [ahead_] + rest
                one, two = make(name, ctx=cl, keep=(tag != "canon")), make(name, ctx=cr, keep=(tag != "canon"))
                if not one or not two:
                    continue
                c.__dict__.update(one[0].__dict__)
                c.canon = f"{behind.name} and {ahead_.name} {far:g} apart, joined in {how}"
                look = W.canon(c, one[1], two[1], how)
                self.canons += 1
                self.joins[(S.n, how)] += 1
                self.joins[how] += 1
                self.canon_own.setdefault(S.n, name)
                self.canon_far[S.n].add(far)
                self.treats["canon"] += 1
                note(name, tag, f"{name}/canon {how} {far:g}")
                self.last["canon"] = True
                return name, "canon", look
        # The other hand: a right part plays the left's riff backwards. First (and once per
        # section), show the explicit counter-running palindrome tape where mirrored strokes
        # meet at the central reading head; elsewhere, draw the picture for each and join them.
        pair3 = hands(S, c) if not flash and not prefer and not first and kind != "hush" else None
        if pair3 and pair3[0].cell >= 12 and (S.n, c.a16 // 16 // 24) not in self.palins[S.n] and "palindrome" not in self.recent[-2:] and (c.b16 - c.a16) * c.six >= 3.5:
            cd = copy.copy(base)
            cd.palin = pair3
            got = make("palindrome", ctx=cd, keep=True)
            t = next((t for t in PALIN_GUISES if ("palindrome", t) not in self.combos and W.TREAT[t][1](cd, W.REG["palindrome"])), None)
            if got and t:
                c.__dict__.update(got[0].__dict__)
                c.arrive = "1"
                c.talk = f"{pair3[0].name} forward against {pair3[1].name} reversed, cell {pair3[0].cell}"
                gk = min((x for x in ("halo", "footlights", "plasma", "smoke", "horizon", "stars") if x not in self.grounds_last[S.n][-2:]), key=lambda x: self.grounds[x] + 2 * rnd(S.n, k, "g" + x))
                self.grounds[gk] += 1
                self.grounds_last[S.n].append(gk)
                look = W.TREAT[t][0](c, W.ground(c, got[1], gk) if t in W.GROUND_OK else got[1])
                self.treats[t] += 1
                self.palins[S.n].add((S.n, c.a16 // 16 // 24))
                note("palindrome", t, "palindrome/mirror" + ("" if t == "plain" else f" {t}"), raw=len(json.dumps(got[1])), ending=None)
                return "palindrome", t, look
        if pair3 and rnd(S.n, k, "hands?") < 0.75:
            pl, pr = pair3
            rest = [p for p in c.riffs if p.name not in (pl.name, pr.name)]
            how = min(W.JOINS, key=lambda j: (self.joins[(S.n, j)], self.joins[j], rnd(S.n, k, j)))
            for name in sorted(W.HANDS, key=lambda n_: (self.used[n_] + 3 * (n_ in self.recent[-6:]), W.HANDS.index(n_))):
                if name not in W.HANDS or (name, "hands") in self.combos:
                    continue
                cl, cr = copy.copy(base), copy.copy(base)
                cl.riffs, cr.riffs = [pl] + rest, [pr] + rest
                one, two = make(name, ctx=cl), make(name, ctx=cr)
                if not one or not two:
                    continue
                c.__dict__.update(one[0].__dict__)
                c.canon = f"{pr.name} plays {pl.name} backwards, joined in {how}"
                look = W.canon(c, one[1], W.flipped(two[1]), how)
                self.hands += 1
                self.joins[(S.n, how)] += 1
                self.joins[how] += 1
                self.treats["hands"] += 1
                note(name, "hands", f"{name}/hands {how}")
                self.last["canon"] = True
                return name, "hands", look
        # Time borrowed and paid back: the phrase written out row by row, each half ruled off
        # as long as it was given, and what is owed lit between the middle and where the
        # second half begins. Once for each amount owed.
        ow = owing_here(S, c) if not flash and not prefer and not first and kind != "hush" and (c.b16 - c.a16) * c.six >= 3.5 else None
        if ow and ow[3:5] not in self.owed[S.n] and (ow[3] or self.owed[S.n]) and "ledger" not in self.recent[-1:]:
            cd = copy.copy(base)
            cd.owing = ow[:3]
            got = make("ledger", ctx=cd, keep=True)
            t = next((t for t in LEDGER_GUISES if ("ledger", t) not in self.combos and W.TREAT[t][1](cd, W.REG["ledger"])), None)
            if got and t:
                c.__dict__.update(got[0].__dict__)
                c.arrive = "1"
                c.talk = (f"{ow[0]}: the first half owes the second {ow[3]:g}" if ow[3] > 0 else f"{ow[0]}: the second half owes the first {-ow[3]:g}" if ow[3] < 0 else f"{ow[0]}: paid back")
                c.talk += ", and borrows" if ow[3] * ow[4] > 0 else ", and pays back" if ow[3] * ow[4] < 0 else ""
                gk = min((x for x in ("halo", "footlights", "plasma", "smoke", "horizon", "stars") if x not in self.grounds_last[S.n][-2:]), key=lambda x: self.grounds[x] + 2 * rnd(S.n, k, "g" + x))
                self.grounds[gk] += 1
                self.grounds_last[S.n].append(gk)
                look = W.TREAT[t][0](c, W.ground(c, got[1], gk) if t in W.GROUND_OK else got[1])
                self.treats[t] += 1
                self.ledgers += 1
                self.owed[S.n].add(ow[3:5])
                note("ledger", t, "ledger/owing" + ("" if t == "plain" else f" {t}"), raw=len(json.dumps(got[1])), ending=None)
                return "ledger", t, look
        # One rule played at several sizes at once: the parts that play only a long and a short
        # are courses of one wall, the biggest size at the top. Twice in each such passage,
        # not twice running, in another guise each time.
        sz = sizes_here(S, c) if not flash and not prefer and not first and kind != "hush" and (c.b16 - c.a16) * c.six >= 3.5 else None
        # (A passage at one size is shown once for each size and length; at several, twice.)
        szk = (S.n, sz[0]) if sz and len(sz[2]) > 1 else (S.n,) + tuple(sz[2][0][1:3]) + (len(sz[2][0][3]) // 30,) if sz else None
        if sz and self.sized[szk] < (2 if len(sz[2]) > 1 else 1) and "sizes" not in self.recent[-1:]:
            cd = copy.copy(base)
            cd.sizes = sz
            got = make("sizes", ctx=cd, keep=True)
            t = next((t for t in SIZE_GUISES if ("sizes", t) not in self.combos and W.TREAT[t][1](cd, W.REG["sizes"])), None)
            if got and t:
                c.__dict__.update(got[0].__dict__)
                c.arrive = "1"
                c.talk = "one rule at " + ", ".join(f"{L}:{S_} ({name})" for name, L, S_, _ in sz[2])
                gk = min((x for x in ("halo", "footlights", "plasma", "smoke", "horizon", "stars") if x not in self.grounds_last[S.n][-2:]), key=lambda x: self.grounds[x] + 2 * rnd(S.n, k, "g" + x))
                self.grounds[gk] += 1
                self.grounds_last[S.n].append(gk)
                look = W.TREAT[t][0](c, W.ground(c, got[1], gk) if t in W.GROUND_OK else got[1])
                self.treats[t] += 1
                self.sized[szk] += 1
                note("sizes", t, "sizes/rule" + ("" if t == "plain" else f" {t}"), raw=len(json.dumps(got[1])), ending=None)
                return "sizes", t, look
        # A tune in which every note lasts as long as its period: each note is one wave, as long
        # as it lasts, on a ruler that counts it. A few times while the tune is played, not
        # twice running, in another guise each time.
        tn = tune_here(S, c) if not flash and not prefer and not first and kind != "hush" and (c.b16 - c.a16) * c.six >= 3.5 else None
        if tn and self.tuned[(S.n, tn[0], tn[1])] < (3 if tn[2] - tn[1] > 24 * 16 else 2) and not any(x == "periods" for x in self.recent[-3:]):
            cd = copy.copy(base)
            cd.periods = tn
            got = make("periods", ctx=cd, keep=True)
            t = next((t for t in PERIOD_GUISES if ("periods", t) not in self.combos and W.TREAT[t][1](cd, W.REG["periods"])), None)
            if got and t:
                c.__dict__.update(got[0].__dict__)
                c.arrive = "1"
                c.talk = f"{tn[0]}: every note lasts as long as its period (" + ", ".join(f"{n_ / 2:g}" for n_ in sorted({x[3] for x in tn[4]}, reverse=True)) + f" counts of {tn[3]:.3g})"
                gk = min((x for x in ("halo", "footlights", "plasma", "smoke", "horizon", "stars") if x not in self.grounds_last[S.n][-2:]), key=lambda x: self.grounds[x] + 2 * rnd(S.n, k, "g" + x))
                self.grounds[gk] += 1
                self.grounds_last[S.n].append(gk)
                look = W.TREAT[t][0](c, W.ground(c, got[1], gk) if t in W.GROUND_OK else got[1])
                self.treats[t] += 1
                self.tuned[(S.n, tn[0], tn[1])] += 1
                note("periods", t, "periods/tune" + ("" if t == "plain" else f" {t}"), raw=len(json.dumps(got[1])), ending=None)
                return "periods", t, look
        # A tune made by a rule: each note against the next, and the web between them. Once
        # for every ten bars of it; never twice running; another guise each time.
        rl = rule_here(S, c) if not flash and not prefer and not first and kind != "hush" and (c.b16 - c.a16) * c.six >= 4.5 else None
        rkey = (rl[0], rl[1], (c.a16 - rl[1]) // 160) if rl else None
        if rl and rkey not in self.rules[S.n] and "cobweb" not in self.recent[-2:]:
            cd = copy.copy(base)
            # (The plot is as wide as the tune has ranged lately: a tune that has settled is seen close to.)
            near = [k_ for t_ in S.tracks if t_.name == rl[0] for s_, _, k_ in t_.notes if c.a16 - 128 <= s_ * 4 < c.b16 + rl[5]]
            lo, hi = min(near), max(near)
            pad = max(0, 7 - (hi - lo)) / 2
            cd.rule = (rl[0], lo - pad, hi + pad, rl[5])
            got = make("cobweb", ctx=cd, keep=True)
            t = next((t for t in RULE_GUISES if ("cobweb", t) not in self.combos and W.TREAT[t][1](cd, W.REG["cobweb"])), None)
            if got and t:
                c.__dict__.update(got[0].__dict__)
                c.arrive = "1"
                c.talk = f"{rl[0]} made by a rule: each note against the next"
                gk = min((x for x in ("halo", "footlights", "plasma", "smoke", "horizon", "stars") if x not in self.grounds_last[S.n][-2:]), key=lambda x: self.grounds[x] + 2 * rnd(S.n, k, "g" + x))
                self.grounds[gk] += 1
                self.grounds_last[S.n].append(gk)
                look = W.TREAT[t][0](c, W.ground(c, got[1], gk) if t in W.GROUND_OK else got[1])
                self.treats[t] += 1
                self.rules[S.n].add(rkey)
                note("cobweb", t, "cobweb/rule" + ("" if t == "plain" else f" {t}"), raw=len(json.dumps(got[1])), ending=None)
                return "cobweb", t, look
        # Harmonic partials beating together (overtones of a tuned/drifting pulse): resonant
        # standing waves for each harmonic partial with a combined interference trace below.
        ov = partials_here(S, c) if not flash and not prefer and not first and kind != "hush" and (c.b16 - c.a16) * c.six >= 4.0 else None
        ovk = (ov[0], (c.a16 // 16 - ov[0]) // 8) if ov else None
        if ov and ovk not in self.overtones[S.n] and "overtones" not in self.recent[-2:]:
            cd = copy.copy(base)
            cd.partials = ov[2:]
            got = make("overtones", ctx=cd, keep=True)
            t = next((t for t in OVERTONE_GUISES if ("overtones", t) not in self.combos and W.TREAT[t][1](cd, W.REG["overtones"])), None)
            if got and t:
                c.__dict__.update(got[0].__dict__)
                c.arrive = "1"
                c.talk = "partials " + ", ".join(f"{m}x ({nm})" for m, nm, _ in ov[3])
                gk = min((x for x in ("halo", "footlights", "plasma", "smoke", "horizon", "stars") if x not in self.grounds_last[S.n][-2:]), key=lambda x: self.grounds[x] + 2 * rnd(S.n, k, "g" + x))
                self.grounds[gk] += 1
                self.grounds_last[S.n].append(gk)
                look = W.TREAT[t][0](c, W.ground(c, got[1], gk) if t in W.GROUND_OK else got[1])
                self.treats[t] += 1
                self.overtones[S.n].add(ovk)
                note("overtones", t, "overtones/beat" + ("" if t == "plain" else f" {t}"), raw=len(json.dumps(got[1])), ending=None)
                return "overtones", t, look
        # Seven-to-the-beat lock: where a seven-note riff speeds up to seven notes per beat and
        # locks onto the quarter note, show the seven-toothed wheel locking against the bar.
        sp = sept_here(S, c) if not flash and not prefer and not first and kind != "hush" and (c.b16 - c.a16) * c.six >= 3.5 else None
        spk = (c.a16 // 16 // 7) if sp else None
        if sp and spk not in self.septs[S.n] and "septlock" not in self.recent[-2:]:
            cd = copy.copy(base)
            cd.sept = sp
            got = make("septlock", ctx=cd, keep=True)
            t = next((t for t in SEPT_GUISES if ("septlock", t) not in self.combos and W.TREAT[t][1](cd, W.REG["septlock"])), None)
            if got and t:
                c.__dict__.update(got[0].__dict__)
                c.arrive = "1"
                c.talk = f"{', '.join(sp[:3])} locked at seven to the beat"
                gk = min((x for x in ("halo", "footlights", "plasma", "smoke", "horizon", "stars") if x not in self.grounds_last[S.n][-2:]), key=lambda x: self.grounds[x] + 2 * rnd(S.n, k, "g" + x))
                self.grounds[gk] += 1
                self.grounds_last[S.n].append(gk)
                look = W.TREAT[t][0](c, W.ground(c, got[1], gk) if t in W.GROUND_OK else got[1])
                self.treats[t] += 1
                self.septs[S.n].add(spk)
                note("septlock", t, "septlock/lock" + ("" if t == "plain" else f" {t}"), raw=len(json.dumps(got[1])), ending=None)
                return "septlock", t, look
        # Grid recount (16:15 without changing tempo): twin dials and vernier ruler showing the
        # band recounting faster against the old bar line.
        rc_ = recount_here(S, c) if not flash and not prefer and not first and kind != "hush" and (c.b16 - c.a16) * c.six >= 4.0 else None
        rck = (c.a16 // 16 // 10) if rc_ else None
        if rc_ and rck not in self.recounts[S.n] and "recount" not in self.recent[-2:]:
            cd = copy.copy(base)
            cd.recount = rc_
            got = make("recount", ctx=cd, keep=True)
            t = next((t for t in RECOUNT_GUISES if ("recount", t) not in self.combos and W.TREAT[t][1](cd, W.REG["recount"])), None)
            if got and t:
                c.__dict__.update(got[0].__dict__)
                c.arrive = "1"
                c.talk = f"recounting at {1 / rc_[1]:.4g}:1 ({', '.join(rc_[2][:3])})"
                gk = min((x for x in ("halo", "footlights", "plasma", "smoke", "horizon", "stars") if x not in self.grounds_last[S.n][-2:]), key=lambda x: self.grounds[x] + 2 * rnd(S.n, k, "g" + x))
                self.grounds[gk] += 1
                self.grounds_last[S.n].append(gk)
                look = W.TREAT[t][0](c, W.ground(c, got[1], gk) if t in W.GROUND_OK else got[1])
                self.treats[t] += 1
                self.recounts[S.n].add(rck)
                note("recount", t, "recount/shift" + ("" if t == "plain" else f" {t}"), raw=len(json.dumps(got[1])), ending=None)
                return "recount", t, look
        # A riff a place off the bar: a wheel of its places rolling in the ring of the bar's.
        # Once for every twelve bars, and whenever the wheels change (a second riff, the
        # other way off the bar); never twice running; another guise each time. And riffs
        # of odd lengths together (five, seven, eleven), a wheel each, once in forty-five
        # bars: the album's first song is told the time by them.
        gr = gear_here(S, c) if not flash and not prefer and not first and kind != "hush" and (c.b16 - c.a16) * c.six >= 4.5 else None
        gkey = ((tuple(w[0] for w in gr[2]), c.a16 // 16 // 12) if any(abs(w[0] - gr[1]) == 1 for w in gr[2]) else ("odd", c.a16 // 16 // 45)) if gr else None
        if gr and gkey not in self.gears[S.n] and "pinion" not in self.recent[-2:]:
            cd = copy.copy(base)
            cd.gear = gr
            got = make("pinion", ctx=cd, keep=True)
            t = next((t for t in GEAR_GUISES if ("pinion", t) not in self.combos and W.TREAT[t][1](cd, W.REG["pinion"])), None)
            if got and t:
                c.__dict__.update(got[0].__dict__)
                c.arrive = "1"
                c.talk = " and ".join(f"{', '.join(w[2][:2])} in {w[0]} against the bar's {gr[1]}" + (f", counted in {w[3]}" if len(w) > 3 else "") for w in gr[2])
                gk = min((x for x in ("halo", "footlights", "plasma", "smoke", "horizon", "stars") if x not in self.grounds_last[S.n][-2:]), key=lambda x: self.grounds[x] + 2 * rnd(S.n, k, "g" + x))
                self.grounds[gk] += 1
                self.grounds_last[S.n].append(gk)
                look = W.TREAT[t][0](c, W.ground(c, got[1], gk) if t in W.GROUND_OK else got[1])
                self.treats[t] += 1
                self.gears[S.n].add(gkey)
                note("pinion", t, "pinion/wheel" + ("" if t == "plain" else f" {t}"), raw=len(json.dumps(got[1])), ending=None)
                return "pinion", t, look
        # Voices an octave apart, climbing for ever (or parts an octave of speed apart, gaining
        # for ever): the stair seen from the side and from above; the rows of ticks and
        # their dial. Once for each passage of the first, once for every eight bars of the
        # second; never twice running; another guise each time.
        for name, here, bag in (("quicken", quick_here, "quick"), ("spire", climb_here, "climb")):
            ps = here(S, c) if not flash and not prefer and not first and kind != "hush" and (c.b16 - c.a16) * c.six >= 3.5 else None
            key = (name, ps[0], (c.a16 // 16 - ps[0]) // 8 if name == "quicken" else 0) if ps else None
            if not ps or key in self.spires[S.n] or self.recent[-1:] in (["spire"], ["quicken"]):
                continue
            cd = copy.copy(base)
            setattr(cd, bag, ps[2:])
            got = make(name, ctx=cd, keep=True)
            t = next((t for t in SPIRE_GUISES if (name, t) not in self.combos and W.TREAT[t][1](cd, W.REG[name])), None)
            if got and t:
                c.__dict__.update(got[0].__dict__)
                c.arrive = "1"
                c.talk = (f"{', '.join(ps[2])} an octave apart on one note, {ps[3]} to {ps[4]}" if name == "spire" else
                          f"{', '.join(ps[2])} an octave of speed apart, a stroke every {ps[4]:.2g} to {ps[3]:.2g} sixteenths")
                gk = min((x for x in ("halo", "footlights", "plasma", "smoke", "horizon", "stars") if x not in self.grounds_last[S.n][-2:]), key=lambda x: self.grounds[x] + 2 * rnd(S.n, k, "g" + x))
                self.grounds[gk] += 1
                self.grounds_last[S.n].append(gk)
                look = W.TREAT[t][0](c, W.ground(c, got[1], gk) if t in W.GROUND_OK else got[1])
                self.treats[t] += 1
                self.spires[S.n].add(key)
                note(name, t, f"{name}/{'climb' if name == 'spire' else 'gain'}" + ("" if t == "plain" else f" {t}"), raw=len(json.dumps(got[1])), ending=None)
                return name, t, look
        # Slack taken up: one part answers another's pull late (or early), by less each time,
        # until they fall together. A rope for each answer, hanging by as much as it was
        # late. Once for each pull, as it comes; not twice running; another guise each time.
        hl = haul_here(S, c) if not flash and not prefer and not first and kind != "hush" and (c.b16 - c.a16) * c.six >= 3.5 else None
        seen = sum(min(r[0], r[1]) <= c.b16 for r in hl[0]) if hl else 0
        # (The pull is in the scene; or it was the last, the taut one, and its rope still hums.)
        newest = max((r for r in hl[0] if min(r[0], r[1]) <= c.b16), key=lambda r: min(r[0], r[1])) if seen else None
        here = newest and (max(newest[0], newest[1]) >= c.a16 - 1 or (abs(newest[2]) < 0.5 and min(newest[0], newest[1]) >= c.a16 - 40))
        if hl and seen and here and (hl[1], seen) not in self.hauls[S.n] and "haul" not in self.recent[-1:]:
            cd = copy.copy(base)
            cd.haul = hl
            got = make("haul", ctx=cd, keep=True)
            t = next((t for t in HAUL_GUISES if ("haul", t) not in self.combos and W.TREAT[t][1](cd, W.REG["haul"])), None)
            if got and t:
                c.__dict__.update(got[0].__dict__)
                c.arrive = "1"
                c.talk = "the slack taken up: " + ", ".join(f"{who} {abs(sl):g} {'late' if sl > 0 else 'early' if sl < 0 else 'on it'}".replace(" 0 on", " on") for _, _, sl, who in hl[0])
                gk = min((x for x in ("halo", "footlights", "plasma", "smoke", "horizon", "stars") if x not in self.grounds_last[S.n][-2:]), key=lambda x: self.grounds[x] + 2 * rnd(S.n, k, "g" + x))
                self.grounds[gk] += 1
                self.grounds_last[S.n].append(gk)
                look = W.TREAT[t][0](c, W.ground(c, got[1], gk) if t in W.GROUND_OK else got[1])
                self.treats[t] += 1
                self.hauls[S.n].add((hl[1], seen))
                note("haul", t, "haul/slack" + ("" if t == "plain" else f" {t}"), raw=len(json.dumps(got[1])), ending=None)
                return "haul", t, look
        # A roll slowed until it can be counted, or wound up until it cannot: a ring for each
        # drum, every stroke a dot at its place in the beat. Through the whole of the slowing,
        # scene after scene in another guise (also on a song's first scene: it is what the
        # song sets out from).
        rl = rolling_here(S, c) if not flash and not prefer and kind != "hush" else None
        if rl and self.rolls_in[(S.n, rl[0])] < 2:
            cd = copy.copy(base)
            cd.roll = rl
            got = make("rolls", ctx=cd, keep=True)
            t = next((t for t in ROLL_GUISES if ("rolls", t) not in self.combos and W.TREAT[t][1](cd, W.REG["rolls"])), None)
            if got and t:
                c.__dict__.update(got[0].__dict__)
                c.arrive = "1"
                c.talk = f"{rl[0]} is rolled, and slows or winds up"
                gk = min((x for x in W.GROUNDS if x not in self.grounds_last[S.n][-3:] and x not in ("ripples", "scope")), key=lambda x: self.grounds[x] + 2 * rnd(S.n, k, "g" + x))
                self.grounds[gk] += 1
                self.grounds_last[S.n].append(gk)
                look = W.TREAT[t][0](c, W.ground(c, got[1], gk))
                self.treats[t] += 1
                self.rolled += 1
                self.rolls_in[(S.n, rl[0])] += 1
                note("rolls", t, "rolls/roll" + ("" if t == "plain" else f" {t}"), raw=len(json.dumps(got[1])), ending=None)
                return "rolls", t, look
        # The common measure: in a song that cuts the longer of two riffs down by the other,
        # section by section, the oblong of the two lengths stands whole, the squares taken so
        # far are lit, and the lamp goes over what is left. Once for each step.
        ms = measuring(S, c) if not flash and not prefer and not first and kind != "hush" and (c.b16 - c.a16) * c.six >= 3.5 else None
        if ms and ms[0] not in self.measured[S.n]:          # (a new step, even straight after the last: that is the song)
            cd = copy.copy(base)
            cd.euclid = (ms[1], ms[2], ms[0], ms[3], ms[4])
            cd.riffs = [ms[3], ms[4]]
            got = make("measure", ctx=cd, keep=True)
            t = next((t for t in MEASURE_GUISES if ("measure", t) not in self.combos and W.TREAT[t][1](cd, W.REG["measure"])), None)
            if got and t:
                c.__dict__.update(got[0].__dict__)
                c.arrive = "1"
                c.talk = f"{ms[3].name} is {ms[5]} long and {ms[4].name} {ms[6]}: the less from the greater"
                look = W.TREAT[t][0](c, got[1])
                self.treats[t] += 1
                self.measures += 1
                self.measured[S.n].add(ms[0])
                note("measure", t, f"measure/less {ms[5]}:{ms[6]}" + ("" if t == "plain" else f" {t}"), raw=len(json.dumps(got[1])), ending=None)
                return "measure", t, look
        # Rows rung in changes: the rows as they are rung, every note's line running down
        # through its places. It comes back once in each run of rows and when the run ends
        # (when the notes come round to the order they set out in).
        rg = rows_here(S, c) if not flash and not prefer and not first and kind != "hush" and (c.b16 - c.a16) * c.six >= 3.5 else None
        if rg and ((rg[2], rg[3]) not in self.rung[S.n]) and "ringing" not in self.recent[-2:]:
            cd = copy.copy(base)
            cd.rows = (rg[1], rg[0])
            got = make("ringing", ctx=cd, keep=True)
            t = next((t for t in ROW_GUISES if ("ringing", t) not in self.combos and W.TREAT[t][1](cd, W.REG["ringing"])), None)
            if got and t:
                c.__dict__.update(got[0].__dict__)
                c.arrive = "1"
                c.talk = f"{rg[0]} rings rows of {rg[1][0][1]}" + (", and the run ends" if rg[3] else "")
                under = got[1]
                if t in W.GROUND_OK:
                    # (a quiet ground: the diagram begins as a few lines on an empty frame)
                    gk = min((x for x in ("halo", "footlights", "horizon", "smoke", "plasma", "stars") if x not in self.grounds_last[S.n][-2:]), key=lambda x: rnd(S.n, k, "rg" + x))
                    under = W.ground(c, under, gk)
                look = W.TREAT[t][0](c, under)
                if rg[3] and rg[4] <= c.b16:
                    # The last row of the run: the notes have come round, and the picture is struck with light.
                    white(look, f"0.75*step({rg[4] / 4:g}, time.beat)*exp(0 - 1.6*max(time.beat - {rg[4] / 4:g}, 0))")
                self.treats[t] += 1
                self.rings += 1
                self.rung[S.n].add((rg[2], rg[3]))
                note("ringing", t, "ringing/rows" + ("" if t == "plain" else f" {t}"), raw=len(json.dumps(got[1])), ending=None)
                return "ringing", t, look
        # The walk: in a song that goes from number to number by a rule, each number lasting as
        # long as it is, the numbers are squares on a line; the picture comes back once in
        # each long walk, in another guise.
        wk = walk_here(S, c) if not flash and not prefer and not first and kind != "hush" and (c.b16 - c.a16) * c.six >= 3.5 else None
        if wk and wk[2] not in self.walked[S.n] and "squares" not in self.recent[-2:]:
            cd = copy.copy(base)
            cd.walk = (wk[1], wk[0])
            got = make("squares", ctx=cd, keep=True)
            t = next((t for t in WALK_GUISES if ("squares", t) not in self.combos and W.TREAT[t][1](cd, W.REG["squares"])), None)
            if got and t:
                c.__dict__.update(got[0].__dict__)
                c.arrive = "1"
                c.talk = f"the walk from {wk[2]}"
                look = W.TREAT[t][0](c, got[1])
                self.treats[t] += 1
                self.walks += 1
                self.walked[S.n].add(wk[2])
                note("squares", t, "squares/walk" + ("" if t == "plain" else f" {t}"), raw=len(json.dumps(got[1])), ending=None)
                return "squares", t, look
        # Two parts fit into one another (one plays the other's negative): a zip is closed, one
        # part's notes the teeth of one side and the other's the teeth of the other.
        fit = fitting(S, c) if not flash and not prefer and not first and kind != "hush" and (c.b16 - c.a16) * c.six >= 3.5 else None
        if fit and "zipper" not in self.recent[-2:] and rnd(S.n, k, "zip?") < 0.8:
            cd = copy.copy(base)
            cd.fit = fit
            got = make("zipper", ctx=cd)
            t = next((t for t in ZIP_GUISES if ("zipper", t) not in self.combos and W.TREAT[t][1](cd, W.REG["zipper"])), None)
            if got and t:
                c.__dict__.update(got[0].__dict__)
                c.arrive = "1"
                c.talk = f"{fit[0].name} and {fit[1].name} fit into one another, {1 / fit[2]:.3g} to the beat"
                look = W.TREAT[t][0](c, got[1])
                self.treats[t] += 1
                self.fits += 1
                note("zipper", t, "zipper/fit" + ("" if t == "plain" else f" {t}"), raw=len(json.dumps(got[1])), ending=None)
                return "zipper", t, look
        # The sum: while a riff is being added up, a place at a time, its triangle keeps coming
        # back, a few rows further on each time, and is there when the sum closes.
        add = summing(S, c) if not flash and not prefer and not first and kind != "hush" else None
        if add and (add[1] or "total" not in self.recent[-2:]):
            cd = copy.copy(base)
            cd.adding = add[0]
            got = make("total", ctx=cd, keep=True)
            t = next((t for t in TOTAL_GUISES if ("total", t) not in self.combos and W.TREAT[t][1](cd, W.REG["total"])), None)
            if got and t:
                c.__dict__.update(got[0].__dict__)
                c.arrive = "1"
                rows = (math.sqrt(8 * max(c.b16 - add[0][1], 0) + 1) - 1) / 2
                c.talk = f"the sum is at {min(int(rows), add[0][3])} of {add[0][3]}" + (", and closes" if add[1] else "")
                look = W.TREAT[t][0](c, got[1])
                self.treats[t] += 1
                self.sums += 1
                note("total", t, "total/sum" + ("" if t == "plain" else f" {t}"), raw=len(json.dumps(got[1])), ending=None)
                return "total", t, look
        # The deal: in a song that gives a part one more note to the beat, time after time,
        # the dice come back at each new number and show it (a die for each beat of the bar).
        rate = dealing(S, c) if not flash and not prefer and not first and kind != "hush" else None
        if rate and rate[0] >= 2 and rate[0] not in self.dealt[S.n] and "dice" not in self.recent[-1:]:
            cd = copy.copy(base)
            cd.riffs, cd.every, cd.drums, cd.tunes, cd.parts = [rate[1]], [], [], [], []
            got = make("dice", ctx=cd)
            t = next((t for t in DEAL_GUISES if ("dice", t) not in self.combos and W.TREAT[t][1](cd, W.REG["dice"])), None)
            if got and t:
                c.__dict__.update(got[0].__dict__)
                c.arrive = "1"
                c.talk = f"{rate[1].name} is given {rate[0]} to the beat"
                look = W.TREAT[t][0](c, got[1])
                self.dealt[S.n].add(rate[0])
                self.treats[t] += 1
                self.deals += 1
                note("dice", t, f"dice/deal {rate[0]}" + ("" if t == "plain" else f" {t}"), raw=len(json.dumps(got[1])), ending=None)
                return "dice", t, look
        # Two parts answer one another: a picture each, and the line between them goes to and fro as they do.
        talk = talkers(S, c) if not flash and not prefer and not first and kind != "hush" and (c.b16 - c.a16) * c.six >= 4.0 else None
        if talk and rnd(S.n, k, "tug?") < 0.65 and not (last and last.get("tug")):
            pa, pb = talk
            both = [n_ for n_ in ranked if W.REG[n_]["fam"] not in NO_PAIR and W.REG[n_]["cost"] <= 2 and n_ not in self.recent[-12:] and n_ not in W.FED]
            done = False
            for A in both[:8]:
                ca = copy.copy(base)
                ca.riffs, ca.tunes = [pa] + [p for p in c.riffs if p.name != pa.name], [pa] + list(c.tunes)
                one = make(A, ctx=ca)
                if not one:
                    continue
                for B in both:
                    if B == A or W.REG[B]["fam"] == W.REG[A]["fam"] or (A, f"tug+{B}") in self.combos or (B, f"tug+{A}") in self.combos or (A in W.THIN and B in W.THIN):
                        continue
                    cb = copy.copy(base)
                    cb.riffs, cb.tunes = [pb] + [p for p in c.riffs if p.name != pb.name], [pb] + list(c.tunes)
                    cb.a, cb.b, cb.c = cb.b, cb.c, cb.a
                    two = make(B, ctx=cb)
                    if not two:
                        continue
                    c.talk = f"{pa.name} and {pb.name} answer one another"
                    look = W.tug(c, one[1], two[1], pa, pb)
                    self.kinds["tug"] += 1
                    self.treats["tug"] += 1
                    note(A, f"tug+{B}", f"{A}+{B}/tug", partner=B)
                    self.last["tug"] = True
                    self.used[B] += 1
                    return A, f"tug+{B}", look
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
                    look = W.TREAT[last["ending"]][0](d, W.ground(d, look, last.get("ground")))
                    c.__dict__.update(d.__dict__)
                    self.grown[way] += 1
                    note(name, key, f"{name}/{way}", raw=raw, ending=last["ending"])
                    self.last["ground"] = last.get("ground")
                    return name, way, look
        # Two parts play one riff, one ahead of the other: the picture is drawn for each and
        # joined down the middle. In step it is one picture; out of step it is broken there,
        # by exactly as much as they are.
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
                    kinds = sorted((kd for kd in W.COMBOS if (A, f"{kd}+{B}") not in self.combos and (B, f"{kd}+{A}") not in self.combos and fits(kd, A, B)), key=lambda kd: self.kinds[kd] + 2 * rnd(S.n, k, kd) - 5 * (kd in HOUSE.get(S.n, ())))
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
        passed = 0
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
            order = sorted((t for t, (_, ok) in W.TREAT.items() if t != "plain" and (name, t) not in self.combos and ok(c, info) and not (name in W.THIN and t in W.SHRINKS)),
                           key=lambda t: self.treats[t] + 2 * rnd(S.n, k, t) - 6 * (t in HOUSE.get(S.n, ())))
            if info["fam"] == "plate":
                order = []          # the first film's studies come as they were, and once
            if name in W.BOLD or name in W.THIN:
                # Pictures made of lines and points keep to guises that add to them: a print of a hair line is nothing.
                order = [t for t in order if t in W.FILLS]
            if first:
                # A song opens on its picture as it is, or in a guise that leaves it whole.
                # (not on a ball or falling away: before anything has been played those are a dark frame)
                order = [t for t in order if t in ("fringe", "relief", "solar", "leaded", "echo", "water", "blown", "mirror", "kaleido", "smoked", "infra", "tracking")]
            plain_ok = (name, "plain") not in self.combos
            treat = "plain" if (plain_ok and (self.used[name] == 0 or first or name == hand_on or rnd(S.n, k, "plain?") < 0.25)) or not order else order[0]
            # A song whose riff keeps changing its length in half bars (two, four, five, three):
            # each new length is seen on a sheet of that many pictures, one taken each half bar.
            per = period(S, c) if not flash and not first else None
            if per and per != self.period.get(S.n) and "halves" not in order and name != hand_on and passed < 10:
                passed += 1
                continue            # (one that can be put on such a sheet, if there is one near the top)
            if per and per != self.period.get(S.n) and "halves" in order and name != hand_on:
                treat = "halves"
                self.period[S.n] = per
                c.talk = f"the riff is {per} half bars long"
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
                more = sorted((t for t in W.STACK if W.STACK[t] != W.STACK[treat] and (name, t) not in self.combos and W.TREAT[t][1](c, info) and ((name not in W.BOLD and name not in W.THIN) or t in W.FILLS) and not (name in W.THIN and t in W.SHRINKS)
                               and (treat, t) not in W.STACK_BAD and (t, treat) not in W.STACK_BAD),
                              key=lambda t: self.stacks[t] + 2 * rnd(S.n, k, "st" + t))
                if more:
                    second = more[0]
            # A picture that leaves most of the frame dark stands on a ground: the rest of the
            # band, dimly (a kind of ground the song has not just had).
            gk = None
            if name in W.GROUNDED and treat in W.GROUND_OK and (second is None or second in W.GROUND_OK) and "layers" in look \
                    and not any(f.get("type") in ("feedback", "expose", "slit", "fence", "panels", "timeslice", "step") for f in look.get("filters", [])):
                # (A song's first picture stands on a ground that is lit before anything has sounded:
                # the frame the seam lands on is not a dark one.)
                kinds = [x for x in W.GROUNDS if x not in self.grounds_last[S.n][-3:] and (not first or x in ("halo", "footlights", "plasma", "smoke", "horizon", "floor"))]
                gk = min(kinds, key=lambda x: self.grounds[x] + 2 * rnd(S.n, k, "g" + x))
                look = W.ground(c, look, gk)
                self.grounds[gk] += 1
                self.grounds_last[S.n].append(gk)
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
            if not flash:
                self.last["ground"] = gk
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


def slips(S, L, R):
    """How far part R plays ahead of part L, bar by bar, in sixteenths (to a quarter), where
    they play the same thing; None where they do not, or are silent. Kept on the song."""
    if not hasattr(S, "_slips"):
        S._slips = {}
    if (L, R) in S._slips:
        return S._slips[(L, R)]
    import bisect
    T = {t.name: t for t in (S.tracks.values() if isinstance(S.tracks, dict) else S.tracks)}
    ol, orr = sorted(a * 4 for a, *_ in T[L].notes), sorted(a * 4 for a, *_ in T[R].notes)
    out = []
    for bar in range(S.bars):
        a, b = bar * 16, bar * 16 + 16
        nl, xr = bisect.bisect_left(ol, b) - bisect.bisect_left(ol, a), orr[bisect.bisect_left(orr, a):bisect.bisect_left(orr, b)]
        best = None
        if nl >= 3 and len(xr) >= 3:
            for q in range(0, 37):
                hit = 0
                for x in xr:
                    i = bisect.bisect_left(ol, x + q * 0.25 - 0.13)
                    hit += i < len(ol) and ol[i] <= x + q * 0.25 + 0.13
                score = hit / max(nl, len(xr))
                if best is None or score > best[0] + 1e-9:
                    best = (score, q * 0.25)
        out.append(best[1] if best and best[0] > 0.8 else None)
    S._slips[(L, R)] = out
    return out


def stereo(S, c, whole=False):
    """Two parts of the scene that play one riff, one of them ahead of the other (a left and
    a right: gl and gr), where they are out of step: (the part behind, the part ahead with
    its `lag`, how far ahead at most here); or None. `whole`: where they are still in step
    and will go out of it within twenty-four bars."""
    import copy
    T = {t.name: t for t in (S.tracks.values() if isinstance(S.tracks, dict) else S.tracks)}
    a, b = c.a16 // 16, min(S.bars, max(c.a16 // 16 + 1, -(-c.b16 // 16)))
    best = None
    for left in sorted(T):
        right = left[:-1] + "r"
        if not left.endswith("l") or right not in T or T[left].role == "drum" or any(T[n_].count(a, b) < 3 * (b - a) for n_ in (left, right)):
            continue
        lags = slips(S, left, right)
        here = lags[a:b]
        if sum(v is not None for v in here) * 2 < len(here):
            continue
        far = max(v for v in here if v is not None)
        if whole:
            if far or any(v is None for v in here) or not any(v and v >= 0.75 for v in lags[b:b + 24]):
                continue
        elif far < 0.75:
            continue
        cell = T[left].cell(a, b)[0] or 16      # (a line that does not repeat is taken a bar at a time)
        first = next(v for v in here if v is not None)
        expr, cur = [f"{first:g}"], first
        for i, v in enumerate(here):
            if v is not None and v != cur and i:
                expr.append(f"{v - cur:g}*step({(a + i) * 4}, time.beat)")
                cur = v
        behind = S.part(T[left], c.a16, c.b16, cell)
        ahead = copy.copy(behind)
        ahead.name, ahead.lag = right, "(" + " + ".join(expr) + ")"
        if best is None or T[left].count(a, b) > best[3]:
            best = (behind, ahead, far, T[left].count(a, b))
    return best[:3] if best else None


def hands(S, c):
    """Two parts of the scene, a left and a right, of which the right plays the left's riff
    backwards (the same strip of attacks read from the other end): (the left, the right with
    its turns begun where its strip is the left's reversed); or None."""
    T = {t.name: t for t in (S.tracks.values() if isinstance(S.tracks, dict) else S.tracks)}
    a, b = c.a16 // 16, min(S.bars, max(c.a16 // 16 + 1, -(-c.b16 // 16)))
    pairs = [(n_, n_[:-1] + "r") for n_ in T if n_.endswith("l")] + [("left", "right")]
    for left, right in pairs:
        if left not in T or right not in T or T[left].role == "drum" or any(T[n_].count(a, b) < 3 * (b - a) for n_ in (left, right)):
            continue
        cell = T[left].cell(a, b)[0]
        if not cell or cell < 6 or T[right].cell(a, b)[0] != cell:
            continue
        pl = S.part(T[left], c.a16, c.b16, cell)

        def strip(t, anchor):
            hits = [0] * cell
            turns = 0
            x = anchor + -(-(a * 16 - anchor) // cell) * cell
            while x + cell <= b * 16:
                for j in range(cell):
                    hits[j] += t.grid.get(x + j) is not None
                turns, x = turns + 1, x + cell
            return [h * 2 > turns for h in hits] if turns else None
        sl = strip(T[left], pl.anchor)
        if not sl or sum(sl) < 3 or sl == sl[::-1]:
            continue
        turned = [strip(T[right], pl.anchor + shift) for shift in range(cell)]
        if any(sr == sl for sr in turned):
            continue        # the right plays the left's riff as it is (in step or out of it): a riff that reads the same both ways proves nothing
        for shift, sr in enumerate(turned):
            if sr and sr[::-1] == sl:
                pr = S.part(T[right], c.a16, c.b16, cell)
                pr.anchor = pl.anchor + shift
                return pl, pr
    return None


def fitting(S, c):
    """Two parts of the scene that fit into one another: they never play together, and
    together they make an unbroken pulse of at least two to the beat that neither makes
    alone (one plays the other's negative). (The one that plays more, the other, the pulse
    in beats); or None."""
    a, b = c.a16 / 4, c.b16 / 4

    def onsets(t):
        out = []
        for s_, *_ in sorted(t.notes):
            if a - 0.02 <= s_ < b - 0.02 and (not out or s_ - out[-1] > 0.05):
                out.append(s_)
        return out
    tracks = [(t, onsets(t)) for t in (S.tracks.values() if isinstance(S.tracks, dict) else S.tracks)]
    tracks = [(t, o) for t, o in tracks if len(o) >= max(4, (b - a) * 0.5)]
    best = None
    for i, (x, ox) in enumerate(tracks):
        for y, oy in tracks[i + 1:]:
            if x.role == "drum" and y.role == "drum":
                continue
            both = sorted(ox + oy)
            gaps = [q - p for p, q in zip(both, both[1:])]
            med = sorted(gaps)[len(gaps) // 2]
            if min(gaps) < 0.08 or med > 0.51 or sum(1 for g_ in gaps if abs(g_ - med) < 0.15 * med) < 0.85 * len(gaps):
                continue
            broken = True
            for o in (ox, oy):
                own = [q - p for p, q in zip(o, o[1:])]
                kinds = collections.Counter(round(g_ / med) for g_ in own)
                if len(kinds) < 2 or kinds.most_common(1)[0][1] > 0.8 * len(own):
                    broken = False      # it only takes every other place (or every third): no riff to it
            if broken and (best is None or len(both) > best[0]):
                first, second = (x, y) if len(ox) >= len(oy) else (y, x)
                best = (len(both), first, second, med)
    if not best:
        return None
    _, x, y, med = best
    ab = (c.a16 // 16, min(S.bars, max(c.a16 // 16 + 1, -(-c.b16 // 16))))
    return S.part(x, c.a16, c.b16, x.cell(*ab)[0]), S.part(y, c.a16, c.b16, y.cell(*ab)[0]), med


LEDGER_GUISES = ("plain", "relief", "infra", "fringe", "papercut", "duotone", "echo", "delayed", "blueprint", "solar", "tracking", "onebit", "water")
# (not papercut or onebit: they lose the bricks still to be played)
RULE_GUISES = ("plain", "fringe", "echo", "infra", "delayed", "solar", "duotone", "blueprint", "tracking", "relief", "water", "papercut")
GEAR_GUISES = ("plain", "echo", "fringe", "infra", "delayed", "solar", "duotone", "blueprint", "tracking", "relief", "water", "papercut", "onebit",
               "negative", "drawn", "hatched", "dots", "screen", "blown", "smoked", "dripping", "lines", "stop", "coiled", "engraved", "torn", "woven")
SPIRE_GUISES = ("plain", "fringe", "echo", "delayed", "infra", "solar", "duotone", "tracking", "blueprint", "relief", "water", "papercut", "onebit")
HAUL_GUISES = ("plain", "fringe", "echo", "delayed", "infra", "solar", "water", "duotone", "tracking", "blueprint", "relief", "papercut")
PERIOD_GUISES = ("plain", "fringe", "echo", "delayed", "solar", "infra", "duotone", "blueprint", "water", "tracking", "relief")
SIZE_GUISES = ("plain", "relief", "fringe", "echo", "infra", "duotone", "delayed", "solar", "blueprint", "tracking", "water", "bricks")
ROLL_GUISES = ("plain", "fringe", "echo", "delayed", "infra", "solar", "water", "tracking", "relief", "kaleido", "smoked")
MEASURE_GUISES = ("plain", "relief", "papercut", "fringe", "bricks", "duotone", "echo", "delayed", "solar", "blueprint", "onebit")
# Pictures with figures in them, and the songs that count (Running Total adds up, Slow Enough
# to Count counts, So Far says its numbers): nowhere else is a number written.
FIGURES = {"numerals": (14,), "leader": (14,), "odometer": (4, 14, 17)}
ROW_GUISES = ("plain", "relief", "infra", "fringe", "echo", "delayed", "duotone", "solar", "blueprint", "tracking", "water", "papercut", "onebit", "drawn")
WALK_GUISES = ("plain", "relief", "papercut", "itself", "fringe", "duotone", "echo", "delayed", "solar", "blueprint", "tracking", "water", "onebit")
ZIP_GUISES = ("plain", "relief", "papercut", "infra", "fringe", "duotone", "echo", "delayed", "solar", "tracking", "blown", "water")


def period(S, c):
    """In a song whose riffs keep changing their length in half bars, how many this scene's
    riff has (2..6); or None."""
    if not hasattr(S, "_periods"):
        seen = set()
        for bar in range(0, S.bars - 1, 2):
            for t in (S.tracks.values() if isinstance(S.tracks, dict) else S.tracks):
                if t.role in ("riff", "bass") and t.count(bar, bar + 2) >= 4:
                    cell = t.cell(bar, bar + 2)[0]
                    if cell and cell % 8 == 0 and 1 <= cell // 8 <= 6:
                        seen.add(cell // 8)
        S._periods = seen
    if len(S._periods - {1}) < 4 or not c.riffs or not c.riffs[0].cell:
        return None
    cell = c.riffs[0].cell
    return cell // 8 if cell % 8 == 0 and 2 <= cell // 8 <= 6 else None


def borrowing(S, L=32):
    """A phrase whose first half borrows time from its second (or the other way) and pays it
    back: a part that plays one phrase of two bars over and over, the same notes in the same
    order, but with the note that belongs on the half coming late or early and every other
    note stretched or squeezed to fit. Found from the notes. Returns (the part,
    [(sixteenth, where the second half begins, [(onset, length, key, second half?)])]),
    or None."""
    if hasattr(S, "_owing"):
        return S._owing
    import statistics
    best = None
    for t in (S.tracks.values() if isinstance(S.tracks, dict) else S.tracks):
        if t.role == "drum" or len(t.notes) < 150:
            continue
        wins = collections.defaultdict(list)
        for a, b, k in sorted(t.notes):
            w = int((a * 4 + 0.3) // L)             # (a note a hair early belongs to the phrase it leads)
            wins[w].append((a * 4 - w * L, (b - a) * 4, k))
        # The phrase as written: the commonest window whose notes all fall on sixteenths.
        shapes = collections.Counter()
        for w, ns in wins.items():
            if (len(ns) >= 8 and all(abs(o - round(o)) < 0.12 for o, _, _ in ns) and sum(1 for o, _, _ in ns if o < L / 2 - 0.5) >= 3
                    and sum(1 for o, _, _ in ns if o > L / 2 - 0.5) >= 3):
                low = min(k for _, _, k in ns)
                shapes[tuple((round(o), k - low) for o, _, k in ns)] += 1
        if not shapes:
            continue
        ref, seen = shapes.most_common(1)[0]
        if seen < 3 or not any(o == L // 2 for o, _ in ref):
            continue
        out = []
        for w in sorted(wins):
            ns = wins[w]
            low = min(k for _, _, k in ns)
            pairs = []
            if len(ns) == len(ref) and [k - low for _, _, k in ns] == [k for _, k in ref]:
                pairs = list(zip(ns, ref))
            else:                                   # the first half alone, or the second
                for cand in (ref[:len(ns)], ref[len(ref) - len(ns):]):
                    if len(cand) == len(ns) and len({k - low - r for (_, _, k), (_, r) in zip(ns, cand)}) == 1:
                        pairs = list(zip(ns, cand))
                        break
            if not pairs:
                continue
            f1 = [o / r for (o, _, _), (r, _) in pairs if 0 < r < L // 2]
            f2 = [(L - o) / (L - r) for (o, _, _), (r, _) in pairs if L // 2 <= r < L]
            B1 = L / 2 * statistics.median(f1) if len(f1) >= 3 else None
            B2 = L - L / 2 * statistics.median(f2) if len(f2) >= 3 else None
            if B1 is not None and B2 is not None and abs(B1 - B2) > 0.6:
                continue
            B = B2 if B2 is not None else B1
            if B is None or not L / 4 <= B <= 3 * L / 4:
                continue
            if max(abs(o - (r * B / (L / 2) if r < L // 2 else B + (r - L / 2) * (L - B) / (L / 2))) for (o, _, _), (r, _) in pairs) > 0.5:
                continue
            out.append((w * L, round(B * 2) / 2, [(max(o, 0), ln, k, r >= L // 2) for (o, ln, k), (r, _) in pairs]))
        moved = sum(1 for _, B, _ in out if abs(B - L / 2) >= 0.75)
        if moved >= 6 and len({B for _, B, _ in out}) >= 4 and (best is None or moved > best[0]):
            best = (moved, t.name, out)
    S._owing = (best[1], best[2], L) if best else None
    return S._owing


def owing_here(S, c):
    """(the part, the phrases about the scene, the phrase's length, how much is owed at the
    scene's end) where the scene lies among phrases that owe, or just after one; or None."""
    bw = borrowing(S)
    if not bw:
        return None
    name, rows, L = bw
    here = [r for r in rows if c.a16 - L < r[0] < c.b16]
    if len(here) < max(1, (c.b16 - c.a16) // L - 1):
        return None
    near = [r for r in rows if r[0] < c.b16][-8:]      # (the ledger keeps what was written before a rest)
    before = [r for r in rows if r[0] < here[0][0]]
    was = before[-1][1] if before else L / 2
    owed = here[-1][1] - L / 2
    return name, near, L, owed, ((here[-1][1] > was) - (here[-1][1] < was)) if owed else 0


def _rule_ok(word, depth=2):
    """True if a word of longs and shorts could have been made by the rule long -> long
    short, short -> long: no two shorts together, no three longs, and the same of the word
    it was made from (a long and its short taken back to a long, a long alone to a short)."""
    for _ in range(depth + 1):
        s = "".join(word)
        if "SS" in s or "LLL" in s:
            return False
        was, i = [], 1 if word[:1] == ["S"] else 0
        while i < len(word):
            if word[i] != "L":
                return False
            if i + 1 < len(word) and word[i + 1] == "S":
                was.append("L")
                i += 2
            elif i + 1 == len(word):
                break               # (the last long may have lost its short)
            else:
                was.append("S")
                i += 1
        word = was
        if len(word) < 4:
            break
    return True


def sizing(S):
    """One rule played at several sizes: a part whose notes are only ever a long or a short
    apart (the long less than twice the short: three and two, five and three, eight and
    five), on the sixteenth, for a dozen notes or more. Found from the notes. Returns the
    passages [(from, to, [(part, long, short, [(sixteenth, gap, key)…])…])]: the parts of a
    passage are those that play through the same stretch, the biggest size first. The longs
    and shorts must be in an order the rule long -> long short, short -> long can make."""
    if hasattr(S, "_sizing"):
        return S._sizing
    runs = []
    for t in S.tracks:
        ons = {}
        for s, z, key in t.notes:
            q = round(s * 4)
            if abs(s * 4 - q) < 0.06:
                ons.setdefault(q, (key, max(1, round((z - s) * 4))))
        if len(ons) < 12 or len(ons) < 0.9 * len({round(s * 4, 1) for s, _, _ in t.notes}):
            continue
        seq = sorted(ons)
        run = [seq[0]]
        for x in seq[1:] + [None]:
            if x is not None and x - run[-1] <= 13:
                run.append(x)
                continue
            gaps = [q - p for p, q in zip(run, run[1:])]
            kinds = sorted(set(gaps))
            if len(run) >= 12 and len(kinds) == 2 and kinds[0] < kinds[1] < 2 * kinds[0] and 1.4 < kinds[1] / kinds[0] < 1.8 \
                    and _rule_ok(["L" if x_ == kinds[1] else "S" for x_ in gaps]):
                S_, L_ = kinds
                last = min(L_, max(S_, ons[run[-1]][1]))
                runs.append((run[0], run[-1] + last, t.name, L_, S_, [(p, gp, ons[p][0]) for p, gp in zip(run, gaps + [last])]))
            run = [x] if x is not None else []
    out = []
    for r in sorted(runs):
        for p in out:
            both = min(p[1], r[1]) - max(p[0], r[0])
            if both >= 0.6 * min(p[1] - p[0], r[1] - r[0]):
                p[0], p[1] = min(p[0], r[0]), max(p[1], r[1])
                p[2].append(r[2:])
                break
        else:
            out.append([r[0], r[1], [r[2:]]])
    S._sizing = [(a, b, sorted(rows, key=lambda x: -x[1])) for a, b, rows in out]
    return S._sizing


def climbing(S):
    """Voices an octave apart: three parts or more that sound one note in three octaves or
    more, and go on doing so as the note moves. Found from the notes, bar by bar: the parts
    that share a pitch class in at least three octaves for most of the bar. Returns the
    passages [(from bar, to bar, parts, lowest key, highest key)]; of parts that play the
    same thing (one a side) the first is kept."""
    if hasattr(S, "_climbing"):
        return S._climbing
    cand = [t for t in S.tracks if t.role != "drum" and len(t.notes) >= 24]
    sound = {}
    for t in cand:
        m = {}
        for s, z, k in sorted(t.notes):
            a = round(s * 4)
            for q in range(a, min(a + 8, round(z * 4) + 1) if z > s else a + 1):
                m[q] = k
            m[a] = k
        sound[t.name] = m
    per = []
    for b in range(S.bars):
        votes, live = collections.Counter(), 0
        for q in range(b * 16, b * 16 + 16):
            by = collections.defaultdict(list)
            for t in cand:
                k = sound[t.name].get(q)
                if k is not None:
                    by[k % 12].append((t.name, k))
            best = max(by.values(), key=lambda v: len({k // 12 for _, k in v}), default=[])
            if len({k // 12 for _, k in best}) >= 3:
                live += 1
                votes.update(nm for nm, _ in best)
        names = [nm for nm, v in votes.items() if live >= 8 and v >= 0.6 * live]
        seen, keep = set(), []
        for nm in sorted(names):
            sig = tuple(sound[nm].get(q) for q in range(b * 16, b * 16 + 16))
            if sig not in seen:
                seen.add(sig), keep.append(nm)
        per.append(keep if len(keep) >= 3 else [])
    out = []
    for b, names in enumerate(per):
        if not names:
            continue
        if out and out[-1][1] == b and len(set(out[-1][2]) & set(names)) >= 2:
            out[-1][1] = b + 1
            out[-1][2] = sorted(set(out[-1][2]) | set(names))
        else:
            out.append([b, b + 1, names])
    # One way only: parts that step up and down are a riff played in octaves, not this. The
    # passage is cut where the way turns (a leap the other way of a fifth or more is a part
    # coming round again, and no turn).
    def steps(nm, a16, b16):
        ks = [k for q, k in sorted(sound[nm].items()) if a16 <= q < b16 + 1]
        return [y - x for x, y in zip(ks, ks[1:]) if y != x and abs(y - x) < 7]

    res = []
    for a, b, names in out:
        ways = []
        for bar in range(a, b):
            st = [d for nm in names for d in steps(nm, bar * 16, bar * 16 + 16)]
            up = sum(d > 0 for d in st)
            ways.append(0 if not st else 1 if up >= 0.85 * len(st) else -1 if up <= 0.15 * len(st) else None)
        runs, at = [], None
        for i, w in enumerate(ways + [None]):
            if at is not None and (w is None or (w and runs[-1][2] and w != runs[-1][2])):
                runs[-1][1] = a + i
                at = None
            if w is not None and at is None:
                at = a + i
                runs.append([at, None, w])
            elif w and at is not None and not runs[-1][2]:
                runs[-1][2] = w
        for ra, rb, w in runs:
            if rb - ra < 2 or not w:
                continue
            keep = [nm for nm in names if sum(abs(d) for d in steps(nm, ra * 16, rb * 16)) >= 5 and any(ra * 16 <= q < rb * 16 for q in sound[nm])]
            if len(keep) < 3:
                continue
            keep.sort(key=lambda nm: min(k for q, k in sound[nm].items() if ra * 16 <= q < rb * 16))
            ks = [k for nm in keep for q, k in sound[nm].items() if ra * 16 <= q < rb * 16]
            res.append((ra, rb, keep, min(ks), max(ks)))
    S._climbing = res
    return res


def quickening(S):
    """Parts an octave of speed apart: three or more whose strokes come twice as often from
    one to the next, all of them gaining (or all losing). Found from the notes, bar by bar.
    Returns the passages [(from bar, to bar, parts, shortest gap, longest gap)] (gaps in
    sixteenths)."""
    if hasattr(S, "_quickening"):
        return S._quickening
    cand = [t for t in S.tracks if t.role != "drum" and len(t.notes) >= 24]
    starts = {t.name: sorted(s * 4 for s, _, _ in t.notes) for t in cand}
    med = {}
    for t in cand:
        st = starts[t.name]
        for b in range(S.bars):
            g = [st[i + 1] - st[i] for i in range(len(st) - 1) if b * 16 <= st[i] < b * 16 + 16 and st[i + 1] - st[i] < 12]
            if len(g) >= 2:
                med[t.name, b] = (sorted(g)[len(g) // 2], g[0], g[-1])
    per = []
    for b in range(S.bars):
        gain = [(med[t.name, b][0], t.name) for t in cand if (t.name, b) in med and med[t.name, b][2] < med[t.name, b][1] * 0.985]
        seen, rows = set(), []
        for m, nm in sorted(gain, key=lambda r: r[1]):      # (of two at one speed, one a side, the first by name)
            if not any(abs(m - x) < 0.04 * x for x in seen):
                seen.add(m), rows.append((m, nm))
        rows.sort()
        chain = [rows[0]] if rows else []
        for m, nm in rows[1:]:
            if 1.6 <= m / chain[-1][0] <= 2.5:
                chain.append((m, nm))
        per.append(chain if len(chain) >= 3 else [])
    out = []
    for b, chain in enumerate(per):
        if not chain:
            continue
        names = [nm for _, nm in chain]
        if out and out[-1][1] == b:
            out[-1][1] = b + 1
            out[-1][2] += names
        else:
            out.append([b, b + 1, list(names)])
    res = []
    for a, b, names in out:
        if b - a < 2:
            continue
        names = sorted(nm for nm in set(names) if names.count(nm) >= 0.4 * (b - a))       # (those that are in it for a good part of it)
        if len(names) < 3:
            continue
        gs = [med[nm, q][0] for nm in names for q in range(a, b) if (nm, q) in med]
        res.append((a, b, names, min(gs), max(gs)))
    S._quickening = res
    return res


def climb_here(S, c):
    """The passage of voices climbing an octave apart that the scene lies in (most of it), or None."""
    for a, b, names, lo, hi in climbing(S):
        if min(b * 16, c.b16) - max(a * 16, c.a16) >= 0.7 * (c.b16 - c.a16):
            return a, b, names, lo, hi
    return None


def quick_here(S, c):
    """The passage of parts gaining an octave of speed apart that the scene lies in (most of it), or None."""
    for a, b, names, g0, g1 in quickening(S):
        if min(b * 16, c.b16) - max(a * 16, c.a16) >= 0.7 * (c.b16 - c.a16):
            return a, b, names, g0, g1
    return None


def gearing(S):
    """A riff one place longer or shorter than the bar. Found from the notes: a part whose
    strokes lie on the bar's grid (sixteenths, or triplet eighths: whichever its notes
    keep to) and repeat after one place more or fewer than the bar has, and not with the
    bar. Returns the passages [(from bar, to bar, places to the beat, places to the bar,
    places to the riff, first place, parts)], the parts in order of how much they play;
    the first place is where the riff begins, counted in places from the song's start."""
    if hasattr(S, "_gearing"):
        return S._gearing
    runs = collections.defaultdict(list)
    for t in S.tracks:
        if len(t.notes) < 24:
            continue
        sub = next((d for d in (4, 3) if sum(abs(s * d - round(s * d)) < 0.12 for s, _, _ in t.notes) >= 0.92 * len(t.notes)), None)
        if not sub:
            continue
        g = 4 * sub
        on = {round(s * sub) for s, _, _ in t.notes}
        for P in (g - 1, g + 1):
            bars = []
            for b in range(S.bars - 1):
                win = [q for q in on if b * g <= q < b * g + 2 * g - P]
                allq = [q for q in on if b * g <= q < b * g + 2 * g]
                if len(win) >= 2 and len(allq) <= 2 * (P - 2) and sum(q + P in on for q in win) >= 0.85 * len(win) and sum(q + g in on for q in win) < 0.75 * len(win):
                    # (and not sooner: a riff of five comes round after fifteen too, and is no wheel of fifteen)
                    if not any(P % d == 0 and sum(q + d in on for q in allq[:-1]) >= 0.85 * (len(allq) - 1) for d in range(2, P)):
                        bars.append(b)
            for b in bars:
                r = runs[sub, P]
                r.append((b, b + 2, t.name))
    out = []
    for (sub, P), rr in runs.items():
        g = 4 * sub
        cover = collections.defaultdict(set)
        for a, b, nm in rr:
            for x in range(a, b):
                cover[x].add(nm)
        a = None
        for x in sorted(cover) + [None]:
            if a is not None and (x is None or x != last + 1):
                names = collections.Counter(nm for y in range(a, last + 1) for nm in sorted(cover[y]))     # (sorted: a set's order is not the same from run to run)
                if last + 1 - a >= 4 or (last + 1 - a >= 3 and len(names) >= 2):
                    parts = [nm for nm, _ in names.most_common()]
                    lead = next(t for t in S.tracks if t.name == parts[0])
                    q0 = min(round(s * sub) for s, _, _ in lead.notes if a * 4 <= s < (last + 1) * 4)
                    out.append((a, last + 1, sub, g, P, q0, parts))
                a = None
            if x is not None and a is None:
                a = x
            last = x
    S._gearing = sorted(out)
    return S._gearing


def gear_here(S, c):
    """The riffs a place off the bar that the scene lies in (most of it): (places to the
    beat, places to the bar, [(places to the riff, first place, parts)]), the shorter riff
    first if there are two; or None."""
    got = {}
    for a, b, sub, g, P, q0, parts in gearing(S):
        if min(b * 16, c.b16) - max(a * 16, c.a16) >= 0.7 * (c.b16 - c.a16) and (sub, g, P) not in got:
            got[sub, g, P] = (P, q0, parts)
    rc = recounting(S)
    if not got and rc and c.a16 >= rc[0] - 4:
        # A band that has begun to count faster: its bar is a wheel shorter round than the
        # old bar's ring, but with as many teeth (sixteen on a wheel fifteen round).
        fit = [p for p in c.riffs + c.drums if p.cell and p.cell != 16 and abs(p.cell / rc[1] - 16) < 0.02 and p.n >= 4]
        if fit:
            fit.sort(key=lambda p: (p.role == "drum", -p.n))
            return 4, 16, [(fit[0].cell, fit[0].anchor, [fit[0].name] + [p.name for p in fit[1:] if p.name[:2] != fit[0].name[:2]][:1], 16)]
    if not got:
        # Or two riffs or three of odd lengths shorter than the bar (five, seven, eleven):
        # a wheel each, one inside another, all touching the ring where the music is.
        # (Only in a song that runs on three such lengths or more: there they are its clock.)
        if not hasattr(S, "_odd"):
            bars = collections.Counter()
            for t in S.tracks:
                for a, z, cell in t.spans:
                    if t.role != "drum" and cell and 5 <= cell < 16 and cell % 2:
                        bars[cell] += z - a
            S._odd = {cell for cell, n_ in bars.items() if n_ >= 0.1 * S.bars}
        cells = {}
        for p in c.riffs:
            if p.cell in S._odd and p.cell not in cells:
                cells[p.cell] = (p.cell, p.anchor, [p.name])
        return (4, 16, sorted(cells.values())[:3]) if len(S._odd) >= 3 and len(cells) >= 2 else None
    sub, g = max(((sub, g) for sub, g, _ in got), key=lambda k: sum(1 for x in got if x[:2] == k))
    # Of a wheel's parts, the one that plays most here, and with it the one that least
    # plays what it plays (its negative, if there is one: a part that doubles it adds nothing).
    T = {t.name: t for t in S.tracks}
    on = lambda nm: {round(s_ * sub) for s_, _, _ in T[nm].notes if c.a16 / 4 <= s_ < c.b16 / 4}       # noqa: E731
    wheels = []
    for P, q0, parts in sorted(v for k, v in got.items() if k[:2] == (sub, g)):
        turns = lambda o: len(o) >= 3 and sum(q + P in o or q - P in o for q in o) >= 0.8 * len(o)      # noqa: E731  (it comes round with the wheel here)
        live = sorted((nm for nm in parts if turns(on(nm))), key=lambda nm: (T[nm].role == "drum", -len(on(nm))))
        if not live:
            continue
        a = on(live[0])
        rest = sorted(((len(a & on(nm)) / len(a | on(nm)), nm) for nm in live[1:]), key=lambda r: r[0])
        wheels.append((P, q0, live[:1] + [nm for sh, nm in rest[:1] if sh < 0.5]))
    return (sub, g, wheels) if wheels else None


def _arch(x, y):
    """The curve a*x*x + b*x + c nearest the points (least squares), or None."""
    m = sum(x) / len(x)
    u = [p_ - m for p_ in x]                               # (about the middle: the sums stay small)
    S_ = lambda k: sum(p_ ** k for p_ in u)               # noqa: E731
    T_ = lambda k: sum(p_ ** k * q for p_, q in zip(u, y))    # noqa: E731
    A = [[S_(4), S_(3), S_(2), T_(2)], [S_(3), S_(2), S_(1), T_(1)], [S_(2), S_(1), len(u), T_(0)]]
    for i in range(3):
        piv = max(range(i, 3), key=lambda r: abs(A[r][i]))
        if abs(A[piv][i]) < 1e-9:
            return None
        A[i], A[piv] = A[piv], A[i]
        for r in range(3):
            if r != i:
                f = A[r][i] / A[i][i]
                A[r] = [p_ - f * q for p_, q in zip(A[r], A[i])]
    a, b, c_ = (A[i][3] / A[i][i] for i in range(3))
    return a, b - 2 * a * m, a * m * m - b * m + c_


def ruling(S):
    """A tune made by a rule: every note's pitch decides the next one's. Found from the
    notes: a part that plays one note at a time at even spacing, whose pairs (a note's
    pitch, the next note's) lie on one arched curve wherever enough different pitches
    come to tell (a tune that only repeats lies on any curve one likes, and is not this).
    Returns [(part, from 16th, to 16th, lowest key, highest key, sixteenths between notes)]."""
    if hasattr(S, "_ruling"):
        return S._ruling
    out = []
    for t in S.tracks:
        ns = sorted(t.notes)
        if t.role == "drum" or len(ns) < 40:
            continue
        gaps = [round((b[0] - a[0]) * 4) for a, b in zip(ns, ns[1:])]
        step = collections.Counter(gaps).most_common(1)[0][0]
        if step < 4 or sum(g == step for g in gaps) < 0.8 * len(gaps):
            continue
        # runs of evenly spaced notes
        runs, at = [], 0
        for i, g in enumerate(gaps + [None]):
            if g != step:
                if i - at >= 8:
                    runs.append((at, i))
                at = i + 1
        arched = False
        for a, z in runs:
            ks = [k for _, _, k in ns[a:z + 1]]
            for w in range(0, len(ks) - 24, 8):
                x, y = ks[w:w + 24], ks[w + 1:w + 25]
                if len(set(x)) < 6:
                    continue
                co = _arch(x, y)
                if not co:
                    continue
                dev = lambda v: (sum((q - sum(v) / len(v)) ** 2 for q in v) / len(v)) ** 0.5       # noqa: E731
                res = [q - (co[0] * p_ * p_ + co[1] * p_ + co[2]) for p_, q in zip(x, y)]
                apex = -co[1] / (2 * co[0]) if co[0] else 1e9
                if co[0] < 0 and min(x) < apex < max(x) and dev(res) < 0.35 * dev(y):
                    arched = True
        if arched:
            for a, z in runs:
                ks = [k for _, _, k in ns[a:z + 1]]
                out.append((t.name, round(ns[a][0] * 4), round(ns[z][0] * 4) + step, min(ks), max(ks), step))
    S._ruling = out
    return out


def rule_here(S, c):
    """The tune made by a rule that the scene lies in (most of it): (part, lowest key, highest, sixteenths between notes), or None."""
    for nm, a, b, lo, hi, step in ruling(S):
        if min(b, c.b16) - max(a, c.a16) >= 0.7 * (c.b16 - c.a16):
            return nm, a, b, lo, hi, step
    return None


def recounting(S):
    """A band that starts to count faster (or slower) without the tempo changing: from some
    bar on its strokes keep to a grid a little finer than the sixteenths they kept to
    before (sixteen places where there were fifteen). Found from the notes: the unit that
    the strokes of each few bars fit best, and where it changes. Returns (the sixteenth of
    the change, the new unit in sixteenths), or None."""
    if hasattr(S, "_recount"):
        return S._recount
    S._recount = None
    units = (15 / 16, 16 / 15, 8 / 9, 9 / 8, 14 / 15, 15 / 14)

    def off(on, u):
        """How far a part's strokes lie from a grid of unit u, at its best phase (0 to 0.25)."""
        return min(sum(abs(((q - on[0] - ph * u / 24) / u + 0.5) % 1 - 0.5) for q in on) / len(on) for ph in range(24))

    last = None
    for b in range(0, S.bars - 3):
        got = [on for on in ([s * 4 for s, _, _ in t.notes if b * 16 <= s * 4 < b * 16 + 64] for t in S.tracks) if 6 <= len(on) <= 48]
        if len(got) < 3:
            continue
        err = {u: sum(off(on, u) for on in got) / len(got) for u in (1.0,) + units}
        u = min(err, key=err.get)
        if u == 1.0 and err[u] < 0.08:
            last = b
        elif u != 1.0 and err[u] < 0.06 and err[1.0] > 0.15 and last is not None and b - last <= 8:
            S._recount = (min(min(on) for on in got if off(on, u) < 0.06 and off(on, 1.0) > 0.15), u)
            break
    return S._recount


def partials(S):
    """Harmonic partials beating together: passages where 3+ parts lock into integer multiples
    (1x, 2x, 3x, 4x, 5x...) of a fundamental pulse rate, including at least one odd partial
    (3x or 5x) and either an off-grid fundamental or 4+ simultaneous harmonics. Excludes songs
    driven by quickening (t5) so it highlights genuine overtone/beating structures (t16)."""
    if not hasattr(S, "_partials"):
        S._partials = None
    if S._partials is not None:
        return S._partials
    if quickening(S):
        S._partials = []
        return S._partials
    cand = [t for t in S.tracks if len(t.notes) >= 24]
    import bisect
    bar_rate = {}
    for t in cand:
        st = sorted(s for s, _, _ in t.notes)
        u = [st[0]]
        for x in st[1:]:
            if x - u[-1] > 0.025:
                u.append(x)
        for b in range(S.bars):
            lo = bisect.bisect_left(u, b * 4)
            hi = bisect.bisect_left(u, (b + 2) * 4)
            if hi - lo < 4:
                continue
            xs = u[lo:hi]
            gaps = [xs[i + 1] - xs[i] for i in range(len(xs) - 1) if xs[i + 1] - xs[i] < 1.3]
            if len(gaps) < 3:
                continue
            med = sorted(gaps)[len(gaps) // 2]
            if med < 0.09 or med > 1.1:
                continue
            steady = sum(1 for g in gaps if abs(g - med) < 0.14 * med or abs(g - 2 * med) < 0.14 * 2 * med)
            if steady >= 0.65 * len(gaps):
                bar_rate[(t.name, b)] = 1.0 / med
    bars = []
    for b in range(S.bars):
        here = sorted((r, nm) for (nm, bb), r in bar_rate.items() if bb == b)
        if len(here) < 3:
            continue
        best = None
        for r0, _ in here:
            if r0 < 0.7 or r0 > 2.4:
                continue
            harms = {}
            for r, nm in here:
                k = round(r / r0)
                if 1 <= k <= 6 and abs(r / r0 - k) < 0.06 * k and k not in harms:
                    harms[k] = (nm, r)
            has_odd = any(k in (3, 5) for k in harms)
            off_grid = abs(r0 - round(r0)) > 0.06
            if has_odd and (len(harms) >= 4 or (len(harms) >= 3 and off_grid)):
                score = len(harms) + (1 if off_grid else 0)
                if best is None or score > best[0]:
                    best = (score, r0, sorted((k, nm, r) for k, (nm, r) in harms.items()))
        if best:
            bars.append((b, best[1], best[2]))
    runs = []
    for b, r0, h in bars:
        if runs and b <= runs[-1][1] + 2:
            runs[-1][1] = b + 1
            runs[-1][2].append((b, r0, h))
        else:
            runs.append([b, b + 1, [(b, r0, h)]])
    S._partials = [(a, b, xs[len(xs) // 2][1], xs[len(xs) // 2][2]) for a, b, xs in runs if b - a >= 4]
    return S._partials


def partials_here(S, c):
    """The harmonic-partials passage the scene lies in (at least half), or None."""
    for a, b, r0, harms in partials(S):
        if min(b * 16, c.b16) - max(a * 16, c.a16) >= 0.5 * (c.b16 - c.a16):
            return a, b, r0, harms
    return None


def sept_here(S, c):
    """Where a ramping song reaches seven notes to the beat and locks onto the quarter note:
    returns the non-drum parts running at 7/beat in this scene, or None."""
    if quickening(S):
        return None
    dl = dealing(S, c)
    if not dl or dl[0] != 7:
        return None
    a, b = c.a16 / 4, c.b16 / 4
    parts = []
    for t in S.tracks:
        if t.role == "drum":
            continue
        st = sorted(s for s, _, _ in t.notes if a <= s < b)
        if len(st) < 12:
            continue
        # dedup chords within 0.03 beat
        u = [st[0]]
        for x in st[1:]:
            if x - u[-1] > 0.03:
                u.append(x)
        gaps = [u[i + 1] - u[i] for i in range(len(u) - 1) if u[i + 1] - u[i] < 0.5]
        if len(gaps) >= 8:
            med = sorted(gaps)[len(gaps) // 2]
            if 0.125 <= med <= 0.165:  # ~1/7 beat
                parts.append((len(u), t.name))
    # Keep distinct voices (skip l/r duplicates so 3 rings show gl, dl, wl)
    out, seen = [], set()
    for _, nm in sorted(parts, reverse=True):
        stem = nm[:-1] if nm.endswith(("l", "r")) else nm
        if stem not in seen:
            seen.add(stem)
            out.append(nm)
    return out[:3] if out else None


def recount_here(S, c):
    """Where a band has switched to recounting on a finer/coarser grid without tempo change
    (e.g. 16:15 in t14): returns (change_s16, unit, active_parts), or None."""
    rc = recounting(S)
    if not rc or c.a16 < rc[0] - 4:
        return None
    at16, unit = rc
    a, b = c.a16 / 4, c.b16 / 4
    # Find tracks active here whose notes fit the new unit grid better than standard sixteenths.
    active = []
    for t in S.tracks:
        ns = [s * 4 for s, _, _ in t.notes if a <= s < b]
        if len(ns) < 6:
            continue
        err_new = sum(abs(((q - at16) / unit + 0.5) % 1 - 0.5) for q in ns) / len(ns)
        err_old = sum(abs((q + 0.5) % 1 - 0.5) for q in ns) / len(ns)
        if err_new < 0.16 and err_new < err_old * 0.85:
            active.append((t.role == "drum", -len(ns), t.name))
    if not active:
        return None
    out, seen = [], set()
    for _, _, nm in sorted(active):
        stem = nm[:-2] if nm.endswith(("-l", "-r")) else (nm[:-4] if nm.endswith(("l-up", "r-up")) else nm)
        if stem not in seen:
            seen.add(stem)
            out.append(nm)
    return (at16, unit, out[:3]) if out else None


def hauling(S):
    """Slack taken up: one part answers another's pull late (or early), by less each time,
    until they fall together. Found from the notes. The pull is a part of few notes that
    falls on bar lines; the answer a part of few notes, each within a bar of a pull, three
    or more running that come nearer every time and end on it (or two, in a song that has
    such a three). Returns the passages [(rows, from, to)], rows (pull, answer, slack, part)
    in sixteenths: the slack is how late the answer was (early, if less than nothing),
    measured from where it falls when they are together (a singer's breath before the line
    is not slack)."""
    if hasattr(S, "_hauling"):
        return S._hauling
    refs = []
    for t in S.tracks:
        on = sorted({16 * round(s / 4) for s, _, _ in t.notes if abs(s * 4 - 16 * round(s / 4)) < 0.6})
        if 3 <= len(on) and len(t.notes) <= 60:
            refs.append((t.name, on))
    runs = {}
    for t in S.tracks:
        ns = sorted(t.notes)
        if t.role == "drum" or not 4 <= len(ns) <= 40:
            continue
        for rname, pulls in refs:
            if rname == t.name:
                continue
            run = []
            for s, _, _ in ns + [(None, 0, 0)]:
                near = min(pulls, key=lambda p_: abs(s * 4 - p_)) if s is not None else None
                off = s * 4 - near if s is not None and abs(s * 4 - near) <= 14 else None
                if off is not None and (not run or (near > run[-1][0] and abs(off) < abs(run[-1][2]) - 0.75 and (off * run[-1][2] > 0 or abs(off) < 1))):
                    run.append((near, s * 4, off))
                    continue
                if len(run) >= 2 and abs(run[0][2]) >= 2 and abs(run[-1][2]) < 1:
                    runs.setdefault((t.name, tuple(r[0] for r in run)), [(pl, h, round((off_ - run[-1][2]) * 2) / 2, t.name) for pl, h, off_ in run])
                run = [(near, s * 4, off)] if off is not None else []
    long = {name for (name, pulls), rows in runs.items() if len(rows) >= 3}
    rows = sorted(r for (name, _), rr in runs.items() if name in long for r in rr)
    out = []
    for r in rows:
        if out and min(r[0], r[1]) - 80 <= max(max(x[0], x[1]) for x in out[-1]):       # (a verse apart, or less)
            out[-1].append(r)
        else:
            out.append([r])
    S._hauling = [(rr, min(min(x[0], x[1]) for x in rr) - 16, max(max(x[0], x[1]) for x in rr) + 40) for rr in out]
    return S._hauling


def haul_here(S, c):
    """The passage in which slack is taken up that the scene lies in (at least half of it), or None."""
    for rows, a, b in hauling(S):
        if min(b, c.b16) - max(a, c.a16) >= 0.5 * (c.b16 - c.a16):
            return rows, a, b
    return None


def tuned(S):
    """A tune in which every note lasts as long as its period: the lower the note, the longer
    it is held, in the proportion of the pitches (a fifth up lasts two thirds as long, an
    octave up half). Found from the notes: a part of twenty notes or more at four pitches or
    more whose lengths times their frequencies all come to the same. Returns the passages
    [(part, from, to, count, [(sixteenth, length, key, units)…])], sixteenths as floats;
    `count` is the song's count as the tune keeps it (a sixteenth, or what the song has made
    of the sixteenth by then), and `units` a note's length in halves of it."""
    if hasattr(S, "_tuned"):
        return S._tuned
    out = []
    for t in S.tracks:
        ns = sorted(t.notes)
        if t.role == "drum" or len(ns) < 20 or len({k_ for _, _, k_ in ns}) < 4:
            continue
        # A note lasts until the next begins; before a rest, as long as its pitch says.
        near = [(ns[i + 1][0] - a) * 4 * 2 ** (key / 12) for i, (a, z, key) in enumerate(ns[:-1]) if ns[i + 1][0] - a <= 1.45 * (z - a)]
        if len(near) < 0.6 * len(ns) or min(near) <= 0:
            continue            # (chords, or too many rests to tell)
        K = sorted(near)[len(near) // 2]
        if sum(abs(x / K - 1) < 0.06 for x in near) < 0.9 * len(near):
            continue
        rows = []
        for i, (a, z, key) in enumerate(ns):
            gap = (ns[i + 1][0] - a) * 4 if i + 1 < len(ns) else 999
            rows.append((a * 4, gap if gap <= 1.45 * (z - a) * 4 else K / 2 ** (key / 12), key))
        if len({round(w, 1) for _, w, _ in rows}) < 4:
            continue
        # The passages: the tune as far as it goes without a rest of four bars.
        runs, run = [], [rows[0]]
        for r in rows[1:]:
            if r[0] - (run[-1][0] + run[-1][1]) > 64:
                runs.append(run)
                run = []
            run.append(r)
        runs.append(run)
        for run in runs:
            if len(run) < 12:
                continue
            # The unit: the longest all the lengths are whole numbers of (each pitch's usual length).
            by = {}
            for _, w, key in run:
                by.setdefault(key, []).append(w)
            usual = [sorted(v)[len(v) // 2] for v in by.values()]
            unit = min(usual) / 8
            for m in range(1, 9):
                u0 = min(usual) / m
                n_ = [max(1, round(w / u0)) for w in usual]
                u1 = sum(w * q for w, q in zip(usual, n_)) / sum(q * q for q in n_)
                if all(abs(w / u1 - round(w / u1)) < 0.16 for w in usual):
                    unit = u1
                    break
            count = unit * max(1, round(1 / unit))
            out.append((t.name, run[0][0], run[-1][0] + run[-1][1], count, [(on, w, key, max(1, round(w / unit))) for on, w, key in run]))
    S._tuned = out
    return out


def tune_here(S, c):
    """The tune of periods the scene lies in (at least half of it, eight of its notes or more), or None."""
    for part, a, b, unit, rows in tuned(S):
        if min(b, c.b16) - max(a, c.a16) >= 0.5 * (c.b16 - c.a16) and sum(c.a16 <= r[0] < c.b16 for r in rows) >= 6:
            return part, a, b, unit, rows
    return None


def sizes_here(S, c):
    """The passage played at several sizes that the scene lies in (at least half of it), or None."""
    for a, b, rows in sizing(S):
        if min(b, c.b16) - max(a, c.a16) >= 0.5 * (c.b16 - c.a16):
            return a, b, rows
    return None


def rolling(S):
    """Rolls that slow until they can be counted, or wind up until they cannot: a part one of
    whose notes is struck about half as often (or twice as often) bar after bar, for at least
    three bars, from or to more than 64 strokes a bar. Found from the notes. Returns
    [(the part, its lowest and highest note, from bar, to bar)], with a few bars after a
    slowing and before a winding up in which the strokes can be counted."""
    if hasattr(S, "_rolling"):
        return S._rolling
    out = {}
    for t in (S.tracks.values() if isinstance(S.tracks, dict) else S.tracks):
        keys = collections.Counter(k for _, _, k in t.notes)
        for key, cnt in keys.items():
            if cnt < 100:
                continue
            per = [0] * (S.bars + 1)
            for a, _, k in t.notes:
                if k == key and int(a // 4) < S.bars:
                    per[int(a // 4)] += 1
            b = 0
            while b < S.bars - 1:
                for way in (1, -1):
                    e = b
                    while e + 1 < S.bars and per[e] > 0 and per[e + 1] > 0 and (per[e] / per[e + 1] if way == 1 else per[e + 1] / per[e]) >= 1.5:
                        e += 1
                    if e - b >= 3 and max(per[b], per[e]) >= 64:
                        a0, b0 = (max(0, b - 1), min(S.bars, e + 5)) if way == 1 else (max(0, b - 4), min(S.bars, e + 2))
                        lo, hi, x, y = out.get(t.name, (key, key, a0, b0))
                        out[t.name] = (min(lo, key), max(hi, key), min(x, a0), max(y, b0))
                        b = e
                        break
                b += 1
    S._rolling = [(name, lo, hi, a, b) for name, (lo, hi, a, b) in out.items()]
    return S._rolling


def rolling_here(S, c):
    """(the part, its lowest note, its highest) where at least half the scene lies in a roll
    that is slowing or winding up; or None."""
    for name, lo, hi, a, b in rolling(S):
        if min(b * 16, c.b16) - max(a * 16, c.a16) >= 0.5 * (c.b16 - c.a16):
            return name, lo, hi
    return None


def euclid(S):
    """A song that finds the common measure of two riffs' lengths the old way: section by
    section the longer of two parts' riffs is cut down by the length of the other (52 against
    32, 20 against 32, 20 against 12, 8 against 12, 8 against 4). Found from the notes.
    Returns (one part, the other, [(from sixteenth, to sixteenth, one's length, the
    other's)]) for the pair with the longest such chain (at least three steps), or None."""
    if hasattr(S, "_euclid"):
        return S._euclid
    S._euclid = None
    tracks = [t for t in (S.tracks.values() if isinstance(S.tracks, dict) else S.tracks) if t.role == "riff"]

    def period(t, a16, b16, L):
        same = tot = 0
        for q in range(a16, b16 - L):
            x, y = t.grid.get(q), t.grid.get(q + L)
            if x is not None or y is not None:
                tot += 1
                same += x == y
        return same / tot if tot >= 40 else 0

    best = None
    for X in tracks:
        for Y in tracks:
            if X is Y:
                continue
            spans = []                              # [bar, bar, X's cell, Y's]
            for bar in range(0, S.bars - 1):
                if X.count(bar, bar + 1) < 2 or Y.count(bar, bar + 1) < 2:
                    continue
                cx, cy = X.cell(bar, bar + 1)[0], Y.cell(bar, bar + 1)[0]
                if not cx or not cy:
                    continue
                if spans and spans[-1][2:] == [cx, cy] and spans[-1][1] >= bar - 1:
                    spans[-1][1] = bar + 1
                else:
                    spans.append([bar, bar + 1, cx, cy])
            spans = [sp for sp in spans if sp[1] - sp[0] >= 3]
            # The longest run of spans each one step on from the last (the greater less the less).
            for i in range(len(spans)):
                chain = [spans[i]]
                for sp in spans[i + 1:]:
                    a, b = chain[-1][2], chain[-1][3]
                    if a != b and (sp[2], sp[3]) == ((a - b, b) if a > b else (a, b - a)):
                        chain.append(sp)
                    elif (sp[2], sp[3]) != (a, b) and sp[1] - sp[0] >= 8:
                        break                       # (a short stretch read otherwise is passed over)
                if len(chain) >= 4 and (best is None or len(chain) > len(best[2])):
                    best = (X, Y, chain)
    if best:
        X, Y, chain = best
        stages = [(sp[0] * 16, sp[1] * 16, sp[2], sp[3]) for sp in chain]
        # The step before, where one riff was too long for its length to be read at a glance:
        # the first stage's two lengths added together.
        a0, b0, cx, cy = stages[0]
        for T, L, pair in ((X, cx + cy, (cx + cy, cy)), (Y, cx + cy, (cx, cx + cy))):
            for start in range(0, a0 // 16):
                if period(T, start * 16, a0, L) >= 0.95 and period(T, start * 16, a0, pair[0] if T is Y else pair[1]) < 0.9:
                    stages.insert(0, (start * 16, a0, pair[0], pair[1]))
                    break
            if stages[0][1] == a0 and stages[0][0] != a0:
                break
        S._euclid = (X, Y, stages)
    return S._euclid


def measuring(S, c):
    """(which step of the measuring the scene is in, the oblong's sides, the two parts as they
    are here) where at least 60 % of the scene lies in one step; or None."""
    e = euclid(S)
    if not e:
        return None
    X, Y, stages = e
    for i, (a, b, cx, cy) in enumerate(stages):
        if min(b, c.b16) - max(a, c.a16) >= 0.6 * (c.b16 - c.a16):
            px, py = S.part(X, max(a, c.a16), c.b16, cx if cx <= 48 else None), S.part(Y, max(a, c.a16), c.b16, cy if cy <= 48 else None)
            for p_, cell_ in ((px, cx), (py, cy)):
                if p_.cell is None:
                    p_.cell, p_.anchor = cell_, a       # (too long for the engine to read: it began with the section)
            return i, stages[0][2], stages[0][3], px, py, cx, cy
    return None


def ringing(S):
    """Rows rung in changes: a part that plays the same few notes over and over, each time in
    a new order, no note moving more than one place from one row to the next. Found from the
    notes. Returns (the part's name, [run]) with a run a list of rows
    (sixteenth, length, ((sixteenth, key), ...)), or None. A run is in one key and at one
    length of row; it is at least 24 rows, at least 20 of them different."""
    if hasattr(S, "_rows"):
        return S._rows
    import bisect
    best = None
    for t in (S.tracks.values() if isinstance(S.tracks, dict) else S.tracks):
        if t.role == "drum" or len(t.notes) < 150:
            continue
        seq = []                                    # (sixteenth, key), repeats of a note dropped
        for b0, _, key in sorted(t.notes):
            if not seq or seq[-1][1] != key:
                seq.append((round(b0 * 4), key))
        ons = [x for x, _ in seq]

        def row(s0, L):
            i, j = bisect.bisect_left(ons, s0), bisect.bisect_left(ons, s0 + L)
            keys = [k_ for _, k_ in seq[i:j]]
            return tuple(seq[i:j]) if 4 <= len(keys) <= 8 and len(set(keys)) == len(keys) else None

        def run_from(s0, L):
            out = []
            while True:
                r = row(s0, L)
                if not r or (out and {k_ for _, k_ in r} != {k_ for _, k_ in out[-1][2]}):
                    return out
                out.append((s0, L, r))
                s0 += L

        runs, s0, end = [], ons[0], ons[-1]
        while s0 < end:
            cands = []
            for L in range(5, 17):
                for d in range(L):                  # (a row may be cut anywhere: prefer one that starts on a bar line, then a beat)
                    r = run_from(s0 + d, L)
                    if len(r) >= 24:
                        cands.append((len(r), r))
                if cands:
                    break
            if not cands:
                s0 += 1
                continue
            most = max(n_ for n_, _ in cands)
            run = min((r for n_, r in cands if n_ >= most - 2), key=lambda r: (r[0][0] % 16 != 0, r[0][0] % 4 != 0, r[0][0]))
            runs.append(run)
            s0 = run[-1][0] + run[-1][1]
        good = []
        for run in runs:
            orders = [tuple(k_ for _, k_ in r[2]) for r in run]
            moved = sum(1 for a, b in zip(orders, orders[1:]) if all(abs(a.index(p) - b.index(p)) <= 1 for p in a))
            if len(set(orders)) >= 20 and moved >= 0.9 * (len(run) - 1):
                good.append(run)
        total = sum(len(r) for r in good)
        if total >= 60 and (best is None or total > best[0]):
            best = (total, t.name, good)
    S._rows = (best[1], best[2]) if best else None
    return S._rows


def rows_here(S, c):
    """(the part, the rows about the scene, which run, whether the run ends in the scene)
    where at least half the scene lies in a run of rows; or None."""
    rg = ringing(S)
    if not rg:
        return None
    name, runs = rg
    for i, run in enumerate(runs):
        a, b = run[0][0], run[-1][0] + run[-1][1]
        if min(b, c.b16) - max(a, c.a16) >= 0.5 * (c.b16 - c.a16):
            L = run[0][1]
            near = [r for r in run if c.a16 - 13 * L <= r[0] < c.b16]
            if sum(1 for r in near if r[0] < (c.a16 + c.b16) / 2) < 6:
                return None                         # (the run has only just begun: there is little to see yet)
            return name, near, i, c.a16 < b <= c.b16 + L, b
    return None


def walking(S):
    """A part that walks from number to number by one rule (halve it if it is even; treble it
    and add one if it is odd), each number lasting as many sixteenths as it is: found from
    the gaps between its notes (the one that is added is a note of its own, a sixteenth into
    the number). Returns (the part's name, [(sixteenth, number, trebled)]) or None."""
    if not hasattr(S, "_walk"):
        S._walk = None
        for t in (S.tracks.values() if isinstance(S.tracks, dict) else S.tracks):
            on = sorted({round(nt[0] * 4) for nt in t.notes})
            gaps = [b - a for a, b in zip(on, on[1:])]
            steps, i, prev = [], 0, None
            while i < len(gaps):
                gap = gaps[i]
                if prev and prev % 2 == 1 and prev > 1 and i + 1 < len(gaps) and gap + gaps[i + 1] == 3 * prev + 1:
                    steps.append((on[i], gap + gaps[i + 1], True))
                    i += 2
                else:
                    steps.append((on[i], gap, False))
                    i += 1
                prev = steps[-1][1]
            pairs = [(a[1], b[1]) for a, b in zip(steps, steps[1:]) if a[1] >= 5]
            kept = sum(1 for a, b in pairs if (a % 2 == 0 and b == a // 2) or (a % 2 == 1 and b == 3 * a + 1))
            if len(pairs) >= 24 and kept >= 0.9 * len(pairs):
                S._walk = (t.name, steps)
                break
    return S._walk


def walk_here(S, c):
    """(the part, the steps about the scene, the number the walk here set out from) where the
    scene lies in a walk of at least six numbers; or None."""
    w = walking(S)
    if not w:
        return None
    name, steps = w
    mid = (c.a16 + c.b16) / 2
    k = next((i for i, (s0, m, _) in enumerate(steps) if s0 <= mid < s0 + m), None)
    if k is None:
        return None
    a = k
    while a > 0 and steps[a - 1][1] != 1:
        a -= 1
    b = k
    while b < len(steps) - 1 and steps[b][1] != 1:
        b += 1
    if b - a + 1 < 6:
        return None
    near = [st for st in steps if st[0] + st[1] >= c.a16 - 170 and st[0] <= c.b16 + 330]
    return name, near, steps[a][1]


def even(notes, a, b):
    """The whole number of notes to the beat that a part plays, evenly, over beats a..b; or None."""
    st = sorted(s for s, *_ in notes if a - 0.02 <= s < b - 0.02)
    gaps = [y - x for x, y in zip(st, st[1:]) if y - x > 0.05]
    if len(gaps) < max(2, (b - a) * 0.6):
        return None
    med = sorted(gaps)[len(gaps) // 2]
    n_ = round(1 / med)
    if not 1 <= n_ <= 9 or abs(med - 1 / n_) > 0.012 + 0.05 / n_:
        return None
    if sum(1 for g_ in gaps if abs(g_ - med) < 0.2 * med) < 0.65 * len(gaps):
        return None
    return n_


def dealing(S, c):
    """In a song that gives its parts one more note to the beat time after time (two to the
    beat, then three, then four), what this scene is being given: (how many to the beat, the
    part); or None. Bar by bar the fastest part that plays evenly counts."""
    if not hasattr(S, "_deal"):
        S._deal = []
        for bar in range(S.bars):
            best = None
            for t in (S.tracks.values() if isinstance(S.tracks, dict) else S.tracks):
                n_ = even(t.notes, bar * 4, bar * 4 + 4) if t.role != "drum" else None
                if n_ and (best is None or n_ > best[0]):
                    best = (n_, t)
            S._deal.append(best)
        runs = []
        for b_ in S._deal:
            if b_ and (not runs or runs[-1] != b_[0]):
                runs.append(b_[0])
        S._ramp = any(x + 1 == y and y + 1 == z for x, y, z in zip(runs, runs[1:], runs[2:]))
    if not S._ramp:
        return None
    a, b = c.a16 // 16, min(S.bars, max(c.a16 // 16 + 1, -(-c.b16 // 16)))
    here = [x for x in S._deal[a:b] if x]
    if len(here) * 2 < b - a:
        return None
    n_ = max(x[0] for x in here)

    def carries(t):
        """In how many of the scene's bars this part plays that many to the beat, and how many notes."""
        return (sum(1 for bar in range(a, b) if even(t.notes, bar * 4, bar * 4 + 4) == n_), sum(1 for s, _, _ in t.notes if a * 4 <= s < b * 4))
    # The part that carries the count through most of the scene (not merely in its first bar:
    # the count is often handed from one part to another).
    t = max((t for t in (S.tracks.values() if isinstance(S.tracks, dict) else S.tracks) if t.role != "drum"), key=carries)
    return n_, S.part(t, c.a16, c.b16, t.cell(a, b)[0])


def adding(S):
    """Passages in which a riff is added up: statement after statement of one line, each
    from the top (or to the tail) and one place longer than the last, with no gap between,
    so that statement k begins k(k-1)/2 sixteenths after the sum began. Found from the
    notes: [(head | tail, the sixteenth the sum began, the first statement played, the last
    (the riff's length), the riff's keys place by place)]."""
    if hasattr(S, "_adding"):
        return S._adding
    T = lambda k: k * (k + 1) // 2      # noqa: E731
    end = S.bars * 16
    tracks = [t for t in (S.tracks.values() if isinstance(S.tracks, dict) else S.tracks) if t.role != "drum" and len(t.notes) >= 40]

    def pat(t, s0, k):
        return [t.grid.get(s0 + T(k - 1) + j) is not None for j in range(k)]

    def grows(A, B, kind):
        return (B[:len(A)] == A) if kind == "head" else (B[2:] == A[1:])      # (a statement to the tail may begin on a note where the riff rests)
    seeds = []
    for t in tracks:
        for kind in ("head", "tail"):
            for s0 in range(0, end, 16):
                k, run, best = 4, None, None
                while s0 + T(k + 1) <= end and k < 70:
                    A, B = pat(t, s0, k), pat(t, s0, k + 1)
                    if grows(A, B, kind) and sum(A) >= max(2, k // 3) and sum(B) > sum(A) - 1 + 0 * k and (k < 8 or k - sum(A) >= 1):
                        run = run or k
                        if best is None or k + 1 - run > best[1] - best[0]:
                            best = (run, k + 1)
                    else:
                        run = None
                    k += 1
                if best and best[1] - best[0] >= 8:
                    seeds.append((best[1] - best[0], kind, s0, best[0], best[1], t))
    out, taken = [], []
    for _, kind, s0, k0, k1, t in sorted(seeds, key=lambda x: (-x[0], x[2])):
        if any(not (s0 + T(k1) <= x or s0 + T(k0 - 1) >= y) for x, y in taken):
            continue
        # Other parts may carry the sum on, or have begun it.
        cur, last = pat(t, s0, k1), t
        while s0 + T(k1 + 1) <= end:
            nxt = next((u for u in tracks if grows(cur, pat(u, s0, k1 + 1), kind) and sum(pat(u, s0, k1 + 1)) >= sum(cur)), None)
            if not nxt:
                break
            k1, cur, last = k1 + 1, pat(nxt, s0, k1 + 1), nxt
        cur = pat(t, s0, k0)
        while k0 > 2:
            prev = next((u for u in tracks if grows(pat(u, s0, k0 - 1), cur, kind) and sum(pat(u, s0, k0 - 1)) >= 1), None)
            if not prev:
                break
            k0, cur = k0 - 1, pat(prev, s0, k0 - 1)
        # It ends where the sum closes on a bar line, if it does near its end (after that the riff is only repeated).
        close = next((k for k in range(k1, max(k1 - 3, k0), -1) if (s0 + T(k)) % 16 == 0), k1)
        if close != k1:
            k1, last = close, next((u for u in tracks if sum(pat(u, s0, close)) >= 2), last)
        keys = [last.grid.get(s0 + T(k1 - 1) + j) for j in range(k1)]
        taken.append((s0 + T(k0 - 1), s0 + T(k1)))
        out.append((kind, s0, k0, k1, keys))
    S._adding = sorted(out, key=lambda x: x[1])
    return S._adding


def summing(S, c):
    """The sum this scene is in the middle of, and whether it closes here: (the passage, closes); or None."""
    for A in adding(S):
        kind, s0, k0, k1, _ = A
        a, b = s0 + k0 * (k0 - 1) // 2, s0 + k1 * (k1 + 1) // 2
        closes = c.a16 <= b - 12 and b <= c.b16 + 8
        if closes or min(c.b16, b) - max(c.a16, a) >= 0.6 * (c.b16 - c.a16):
            return A, closes
    return None


TOTAL_GUISES = ("plain", "relief", "infra", "papercut", "duotone", "fringe", "solar", "delayed", "echo", "tracking", "blueprint", "onebit", "water", "reeded")
DEAL_GUISES = ("plain", "relief", "papercut", "infra", "duotone", "solar", "fringe", "echo", "delayed", "tracking", "water", "reeded")     # guises that leave the pips to be counted
OVERTONE_GUISES = ("plain", "fringe", "reeded", "relief", "echo", "delayed", "solar", "duotone", "water", "infra")
SEPT_GUISES = ("plain", "fringe", "echo", "reeded", "relief", "delayed", "solar", "duotone", "tracking")
RECOUNT_GUISES = ("plain", "fringe", "reeded", "delayed", "echo", "relief", "duotone", "blueprint")
PALIN_GUISES = ("plain", "fringe", "reeded", "relief", "echo", "delayed", "duotone", "blueprint", "solar")


def talkers(S, c):
    """Two parts of the scene that answer one another (each plays where the other rests, and
    they change over at least twice): the two as parts, the one that plays more first; or None."""
    a, b = c.a16 // 16, min(S.bars, max(c.a16 // 16 + 1, -(-c.b16 // 16)))
    slots = (c.b16 - c.a16) // 2          # eighths
    if slots < 12:
        return None
    sound = {}
    for t in S.tracks:
        if t.role == "drum":
            continue
        on = [0] * slots
        k = 0
        for s, e, _ in t.notes:
            if s * 4 < c.b16 and e * 4 > c.a16:
                k += c.a16 <= s * 4 < c.b16
                for i in range(max(0, int((s * 4 - c.a16) // 2)), min(slots, int((max(e, s + 0.5) * 4 - c.a16 + 1.999) // 2))):
                    on[i] = 1
        if k >= 3:
            sound[t.name] = on
    best = None
    names = sorted(sound)
    for i, x in enumerate(names):
        for y in names[i + 1:]:
            if x[:-1] == y[:-1]:
                continue
            ox = sum(p and not q for p, q in zip(sound[x], sound[y]))
            oy = sum(q and not p for p, q in zip(sound[x], sound[y]))
            both = sum(p and q for p, q in zip(sound[x], sound[y]))
            turns, who = 0, None
            for p, q in zip(sound[x], sound[y]):
                now = x if p and not q else y if q and not p else None
                if now and now != who:
                    turns += who is not None
                    who = now
            if (turns >= 2 and min(ox, oy) >= max(3, slots // 8) or turns >= 1 and min(ox, oy) >= max(4, slots // 5)) and both <= 0.3 * min(ox + both, oy + both):
                score = turns * min(ox, oy)
                if best is None or score > best[0]:
                    best = (score, x if ox >= oy else y, y if ox >= oy else x)
    if not best:
        return None
    T = {t.name: t for t in S.tracks}
    out = []
    for name in best[1:]:
        cell = T[name].cell(a, b)[0] or 16
        out.append(S.part(T[name], c.a16, c.b16, cell))
    return out


def fits(kind, A, B):
    """Whether two pictures can share the frame this way: one picture works on the other in
    several of them, and that needs something to work on and something to work with."""
    if A in W.THIN and B in W.THIN:
        return False            # two pictures that are mostly dark make a dark frame
    if kind in ("cutout", "negmask", "mirrorby"):        # B's lights act as mask/invert/mirror over A
        return A in W.BROAD and B not in W.FULL
    if kind == "ringed":        # A is seen small, in a ring of frames round B
        return A in W.BROAD and W.REG[A]["fam"] not in ("type", "sign", "plate") and B not in W.THIN
    if kind == "stencil":       # A shows only through B's lights
        return A in W.BROAD and B in W.BROAD
    if kind == "timemap":         # B's lightness pulls A back in time; works best when A is broad and B is not thin
        return A in W.BROAD and B not in W.THIN
    if kind in ("glass", "warpby", "embossed", "prismby"):         # A is refracted/displaced/shaded/dispersed by B
        return A in W.BROAD and W.REG[A]["fam"] != "type" and (kind != "warpby" or B in W.BROAD)
    if kind == "stagepass":
        return A not in W.THIN and B not in W.THIN
    if kind in ("lighten", "double"):      # both pictures on the one plate
        return A not in W.WHITE and B not in W.WHITE
    return True


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
    close = f"smooth({t / 4 - 20:g}, {t / 4 - 2:g}, time.beat)"        # the last five bars
    tints = ["#ff7a59", "#45d9c5", "#ffd65a", "#c59bff", "#8fd0ff"]
    over = []
    for i, cell in enumerate(cells):
        r = 0.34 + 0.13 * i
        tint = "#ffffff" if i == len(cells) - 1 else tints[i % len(tints)]
        ph = f"(0.25 - (time.beat*4 - {t})/{cell})"
        near = f"exp(0 - 6*abs(fract((time.beat*4 - {t})/{cell} + 0.5) - 0.5))"
        over.append({"type": "shape", "sides": 0, "radius": r, "width": f"0.004 + 0.004*{close}", "fill": 0, "color": tint, "blend": "add", "opacity": f"(0.3 + 0.4*{close})*{up}"})
        over.append({"type": "shape", "sides": 1, "radius": f"0.03 + 0.012*{close} + 0.028*{near}", "width": 0, "fill": 1, "color": tint, "blend": "add", "x": f"{r}*cos({ph})", "y": f"{r}*sin({ph})", "opacity": f"{up}"})
        # (Each mark draws a short tail behind it, so its going round is seen in a still.)
        over.append({"type": "shape", "repeat": 7, "sides": 1, "radius": "0.016 - 0.0018*inst.i", "width": 0, "fill": 1, "color": tint, "blend": "add",
                     "x": f"{r}*cos({ph} + 0.012*(inst.i + 1))", "y": f"{r}*sin({ph} + 0.012*(inst.i + 1))", "opacity": f"(0.6 - 0.07*inst.i)*{up}"})
    top = 0.34 + 0.13 * (len(cells) - 1)
    over.append({"type": "shape", "repeat": 24, "sides": 1, "radius": f"0.005 + 0.004*{close}", "width": 0, "fill": 1, "color": "#ffffff", "blend": "add", "x": 0, "y": f"0.28 + inst.i*{(top - 0.22) / 23:g}", "opacity": f"(0.45 + 0.5*{close})*{up}"})
    return {"background": "#000000", "layers": [W._act(look, blend="normal", fade=f"1 - 0.3*{close}")] + over, "filters": []}


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
        if k and k == len(cuts) - 1 and not c.riffs and not flash:
            # The song rings out with nobody playing a riff: the picture has the parts the song
            # began with, still turning though they have stopped sounding.
            c.riffs = next((list(o[5].riffs) for o in out if o[5].riffs), [])
        landed = None
        if kind in ("landing", "reprise") and out:
            # The great round is over: everything is where it was when the song began, and so is the picture.
            # (Or the song plays its opening again, note for note: its first picture is there again, as it was.)
            try:
                c0 = S.cx(a16, b16, k=0, cyc=cyc)
                if kind == "landing":
                    c0.riffs = out[0][5].riffs      # (the wheels as they were, though they have stopped sounding)
                else:
                    c0.__dict__.update({k_: v_ for k_, v_ in out[0][5].__dict__.items() if k_ in ("a", "b", "c", "bg", "ink", "dim", "variant", "seed")})
                back = W.bolder(out[0][2], W.REG[out[0][2]]["f"](c0))
                if kind == "reprise" and out[0][3] in W.TREAT and out[0][3] != "plain":
                    c0.arrive = "1"
                    back = W.TREAT[out[0][3]][0](c0, back)      # in the guise it wore
                landed = (out[0][2], kind, back)
                deal.used[out[0][2]] += 1
                deal.recent.append(out[0][2])
                deal.last = None
                deal.log.setdefault(str(S.n), []).append(f"{out[0][2]}/{kind}")
                deal.landings += kind == "landing"
                deal.reprises += kind == "reprise"
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
        if treat in ("more", "less", "hinge"):
            shift = last_shift      # the same picture with a part more or less: in the same colours
        if not flash:
            last_shift = shift
        if shift and not flash and not any(L.get("type") == "sky" for L in look.get("layers", [])) and W.REG[name]["fam"] not in ("plate", "ground") and name not in W.TRUE:
            look.setdefault("filters", []).append({"type": "hue", "shift": shift})
        deal.flashes += flash
        scene = {"at": 0 if k == 0 else f"{a16 // 16}bar" if a16 % 16 == 0 else f"{a16 / 4:g}b", "look": look}
        still = any(t in ("roll", "spin", "hole", "sheet", "kaleido", "mirror", "tunnel", "slices", "wall", "planet", "wound", "filmclock", "ringed", "exposed", "receding", "janus") for t in treat.replace("+", ",").split(",")) or name in W.PLATES or W.REG[name]["fam"] in ("plate", "sheet", "sign")
        # A picture that is there to be read (a sum, a ledger, rows, an oblong cut into squares) is not moved about.
        still = still or name in ("overtones", "septlock", "recount", "palindrome", "cobweb", "pinion", "spire", "quicken", "haul", "periods", "sizes", "measure", "ledger", "ringing", "total", "squares", "rolls", "zipper", "dice", "rabbits", "barcode", "braille")
        if k and not flash and not still and treat not in ("more", "less", "hinge") and (b16 - a16) * c.six >= 4.5 and rnd(S.n, k, "move?") < 0.5:
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
        if kind == "reprise":
            since = f"max(time.beat - {a16 / 4:g}, 0)"
            white(look, f"0.6*exp(0 - 2.5*{since})")
        if kind == "hush":
            # The band has stopped: drained and hushed, but never crushed into pitch black.
            look.setdefault("filters", []).append({"type": "color", "saturation": 0.16, "exposure": 0.68})
        if kind == "drop":
            # The band comes in: the picture is struck with light and comes forward, then settles.
            since = f"max(time.beat - {a16 / 4:g}, 0)"
            look.setdefault("filters", []).extend([{"type": "camera", "zoom": f"1 + 0.22*exp(0 - 2.5*{since})"}, {"type": "color", "exposure": f"1 + 3.5*exp(0 - 4*{since})"}])
            white(look, f"0.45*exp(0 - 5*{since})")
        if treat == "hinge":
            scene["xfade"], scene["transition"] = "1b", "flip"      # it swings round
        elif k and name in W.PLATES and "+" not in treat:
            scene["lead"] = "2bar" if name == "photofinish" else "1bar"
        elif k and not kind and not was_flash and treat not in ("more", "less") and rnd(S.n, k, "x") < 0.42:
            # One picture turns into the next: each way in its turn, over a beat or two.
            # (How the band's fullness goes over the cut: the way of changing leans with it.)
            was_ = S.full[max(a16 // 16 - 2, 0):a16 // 16] or [0.0]
            next_ = S.full[a16 // 16:min(a16 // 16 + 2, S.bars)] or was_
            lift = sum(next_) / len(next_) - sum(was_) / len(was_)
            up, down = (TR_UP, TR_DOWN) if lift > 0.1 else (TR_DOWN, TR_UP) if lift < -0.1 else ((), ())
            tr = min(TRANSITIONS, key=lambda t_: deal.trans[t_] + 1.5 * rnd(S.n, k, t_) + (-1.2 if t_ in up else 0.6 if t_ in down else 0))
            deal.trans[tr] += 1
            scene["xfade"] = "1b" if tr in ("push", "strips", "blocks", "split", "weave", "checker", "flip", "squeeze", "whip", "fall", "glitch", "pixel", "doors", "scan", "slats", "interlace", "shutter", "pendulum") else "2b"
            scene["transition"] = tr
            if tr in CARRIED or tr in COUNTED or tr in TAPED:
                beats = max(2, min(4 if tr in CARRIED else 6, round(COUNTED.get(tr, TAPED.get(tr, 1.9)) / (c.six * 4))))
                while beats > 2 and beats * 4 * 2.5 > b16 - a16:
                    beats -= 1
                if tr in ("stutter", "flipbook"):
                    beats = 4 if beats >= 4 else 2      # it rolls in halves of its length (it turns eight pages): a whole number of them to the beat
                scene["xfade"] = f"{beats}b"
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
    bar_s, titles = {}, {}
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
        bar_s[num], titles[num] = S.bar_s, S.title
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
                      + (f"  [{getattr(c, 'canon', '')}]" if getattr(c, "canon", "") else "")
                      + (f"  [{getattr(c, 'talk', '')}]" if getattr(c, "talk", "") else "")
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
        # The film as an album file's `songs:` and `transitions:` (how the songs pass into
        # one another: each over the last two bars of the song it leaves, between 3.2 and
        # 4.4 seconds). Whoever draws it adds where the songs and their recordings are.
        json.dump({"songs": [{"n": n_, "title": titles[n_], "vis": f"chirpers10-t{n_}.yaml"} for n_ in sorted(bar_s)],
                   "transitions": [{"after": n_, "kind": SEAMS[n_], "dur": f"{min(4.4, max(3.2, 2 * bar_s[n_])):.2f}s"} for n_ in sorted(bar_s) if n_ in SEAMS]},
                  open(os.path.join(out_dir, "film.json"), "w"), indent=1)
    if show or "--tally" in sys.argv:
        print(f"album: {deal.count} scenes, {len(total)} idioms, {len(deal.combos)} different pictures")
        print("  " + "  ".join(f"{n_}:{k}" for n_, k in total.most_common()))
        print("  treatments: " + "  ".join(f"{n_}:{k}" for n_, k in deal.treats.most_common()))
        print("  turns into: " + "  ".join(f"{n_}:{k}" for n_, k in deal.trans.most_common()))
        print(f"  the band comes in: {deal.dyn['drop']}  hushed bars: {deal.dyn['hush']}  pictures joined by the next: {deal.chains}  pictures that gain a part with the band: {deal.grown['more']}, lose one: {deal.grown['less']}  scenes in a ruled frame: {deal.ruled}  two guises at once: {sum(deal.stacks.values())}  three pictures at once: {deal.trios}  a turn played differently: {deal.odd}  landings: {deal.landings}  canons: {deal.canons}  deals: {deal.deals}  sums: {deal.sums}  the other hand: {deal.hands}  parts that fit: {deal.fits}  hinges: {deal.hinges}  reprises: {deal.reprises}  walks: {deal.walks}  rows rung: {deal.rings}  measures: {deal.measures}  rolls: {deal.rolled}  owing: {deal.ledgers}")
        print("  grounds: " + "  ".join(f"{k}:{v}" for k, v in deal.grounds.most_common()))
        print(f"  flashes: {deal.flashes}  treatments that arrive or leave: {deal.arrivals}  camera: " + "  ".join(f"{n_}:{k}" for n_, k in deal.moves.most_common()))


if __name__ == "__main__":
    main()
