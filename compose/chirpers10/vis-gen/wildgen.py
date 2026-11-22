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
        return W.P(t.name, cell, a16 if anchor is None else anchor, t.role, min(keys), max(keys), t.count(a, b) / max(b - a, 1))

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
    1: ("loom", "remainder", "crystal", "helix"), 2: ("sympathy", "pendwave", "strings", "cradle"), 3: ("changes", "maypole", "chorus", "stringart"),
    4: ("dominoes", "automaton", "tally", "abacus"), 5: ("stairs", "ridges", "escalator", "flight"), 6: ("colony", "bifurcate", "automaton", "anemone"),
    7: ("golden", "spiral", "sunflower", "mandala"), 8: ("loom", "tartan", "solkattu", "musicbox"), 9: ("henge", "orrery", "moons", "grove"),
    10: ("balance", "coins", "tape", "galton"), 11: ("doors", "blinds", "press", "hammers"), 12: ("hands", "juggle", "semaphore", "chorus"),
    13: ("eclipse", "pond", "spiral", "lanterns"), 14: ("numerals", "tally", "zoetrope", "seismo"), 15: ("slack", "ropes", "wires", "swings"),
    16: ("moire", "chladni", "eclipse", "lighthouse"), 17: ("railway", "highway", "gates", "constellation"),
}
TRANSITIONS = ("melt", "luma", "push", "strips", "burn", "blocks", "zoom", "weave", "spiral", "rings", "checker", "split", "wipe", "iris", "blinds", "clock", "diamond", "rise", "dissolve")
NO_PAIR = ("room", "sheet", "plate", "travel")      # families that are not put in a frame with another


def rnd(*key):
    """A fixed random number 0..1 for a key."""
    import hashlib
    return int(hashlib.sha1(repr(key).encode()).hexdigest()[:8], 16) / 0xffffffff


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
            out.append((p, q, cyc))
            p = q
    return out


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

    def choose(self, S, c, k, first):
        in_song = self.song_used
        fams = [W.REG[i]["fam"] for i in self.recent[-3:]]
        cands = []
        for name, info in W.REG.items():
            if info["needs"] > len(c.riffs) or (info["tune"] and not c.tunes):
                continue
            if first and (info["cost"] >= 3 or info["fam"] in ("plate", "room", "travel")):
                continue
            score = 4.0 * self.used[name] + 1.5 * (info["cost"] - 1) - 2.0 * min(info["needs"], 3) + 3.0 * rnd(S.n, k, name)
            if name in self.recent[-12:]:
                score += 100
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
            cands.append((score, name))
        import copy
        base = copy.copy(c)

        def make(name, sub=None):
            """The idiom's look for this scene (as part `sub` sees it), or None if it does not fit."""
            d = copy.copy(base) if sub is None else base.sub(sub, 2)
            d.variant = self.used[name]
            rot = self.used[name] % 3
            d.a, d.b, d.c = (d.a, d.b, d.c)[rot:] + (d.a, d.b, d.c)[:rot]
            try:
                return d, W.REG[name]["f"](d)
            except (ValueError, IndexError, ZeroDivisionError, TypeError):
                return None

        def note(name, treat, label):
            self.used[name] += 1
            self.combos.add((name, treat))
            self.recent.append(name)
            in_song[name] += 1
            self.count += 1
            self.log.setdefault(str(S.n), []).append(label)

        ranked = [name for _, name in sorted(cands)]
        # Now and then two pictures share the frame.
        if not first and rnd(S.n, k, "pair?") < 0.24:
            pair = [n_ for n_ in ranked if W.REG[n_]["fam"] not in NO_PAIR and W.REG[n_]["cost"] <= 2 and n_ not in self.recent[-12:]]
            for A in pair[:6]:
                got = make(A)
                if not got:
                    continue
                for B in pair:
                    kinds = sorted((kd for kd in W.COMBOS if (A, f"{kd}+{B}") not in self.combos and (B, f"{kd}+{A}") not in self.combos), key=lambda kd: self.kinds[kd] + 2 * rnd(S.n, k, kd))
                    if B == A or W.REG[B]["fam"] == W.REG[A]["fam"] or not kinds:
                        continue
                    other = make(B, sub=1 if len(c.riffs) > 1 else 0)
                    if not other:
                        continue
                    kind = kinds[0]
                    look = W.COMBOS[kind](got[0], got[1], other[1])
                    self.kinds[kind] += 1
                    self.treats[kind] += 1
                    note(A, f"{kind}+{B}", f"{A}+{B}/{kind}")
                    self.used[B] += 1
                    self.count -= 0
                    return A, f"{kind}+{B}", look
        for name in ranked:
            info = W.REG[name]
            got = make(name)
            if not got:
                continue
            d, look = got
            c.__dict__.update(d.__dict__)
            # Its first time it is seen plain; after that, through something it has not been seen through.
            order = sorted((t for t, (_, ok) in W.TREAT.items() if t != "plain" and (name, t) not in self.combos and ok(c, info)),
                           key=lambda t: self.treats[t] + 2 * rnd(S.n, k, t))
            if info["fam"] == "plate":
                order = []          # the first film's studies come as they were, and once
            plain_ok = (name, "plain") not in self.combos
            treat = "plain" if (plain_ok and (self.used[name] == 0 or rnd(S.n, k, "plain?") < 0.25)) or not order else order[0]
            look = W.TREAT[treat][0](c, look)
            self.treats[treat] += 1
            note(name, treat, name if treat == "plain" else f"{name}/{treat}")
            return name, treat, look
        raise RuntimeError(f"nothing fits t{S.n} scene {k}")


def plan(S, deal):
    """A song's scenes: [(a16, b16, idiom, treatment, scene dict, context)]."""
    deal.song_used = collections.Counter()
    out = []
    for k, (a16, b16, cyc) in enumerate(cut(S)):
        c = S.cx(a16, b16, k=k, cyc=cyc)
        name, treat, look = deal.choose(S, c, k, first=(k == 0))
        scene = {"at": 0 if k == 0 else f"{a16 // 16}bar" if a16 % 16 == 0 else f"{a16 / 4:g}b", "look": look}
        if cyc and b16 == min(S.bars * 16, a16 + ((b16 - a16) // cyc["round"] or 1) * cyc["round"]) and any(z == b16 for _, z, *_ in S.rounds):
            # The scene ends where a long round does: the picture burns out on the meeting.
            look.setdefault("filters", []).append({"type": "color", "exposure": f"1 + 5*pow(smooth({b16 / 4 - 1:g}, {b16 / 4:g}, time.beat), 3)"})
        if k and name in W.PLATES and "+" not in treat:
            scene["lead"] = "2bar" if name == "photofinish" else "1bar"
        elif k and rnd(S.n, k, "x") < 0.34:
            # One picture turns into the next: each way in its turn, over a beat or two.
            tr = min(TRANSITIONS, key=lambda t_: deal.trans[t_] + 1.5 * rnd(S.n, k, t_))
            deal.trans[tr] += 1
            scene["xfade"] = "1b" if tr in ("push", "strips", "blocks", "split", "weave", "checker") else "2b"
            scene["transition"] = tr
        out.append((a16, b16, name, treat, scene, c))
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
        prog = {"fade": ["1bar", "2bar"], "master": W.master(S.title), "scenes": [sc for *_, sc, _ in scenes]}
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


if __name__ == "__main__":
    main()
