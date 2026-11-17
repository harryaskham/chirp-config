#!/usr/bin/env python3
"""chirpers10-t7 "Extreme and Mean" (chirper-zero): one pattern of longs and shorts, the same at every size.

Euclid cuts a line "in extreme and mean ratio" when the whole is to the longer part as the longer is to the shorter.
A line cut so has no common measure: no unit, however small, goes a whole number of times into both parts. This piece
is that cut made in time, and it is the record's slow song (80 where the other six run 100 to 138).

There are two cells: a LONG of three sixteenths and a SHORT of two. And one rule, applied to every cell at once:

    a long becomes a long and a short;  a short becomes a long.

Start from one long and apply the rule over and over: L, LS, LSL, LSLLS, LSLLSLSL ... Each line is the line before
it followed by the line before that. The pattern never falls into a loop, yet every stretch of it comes back; and it
is the same at every size: group the cells as the rule made them and the groups are again longs and shorts in the
same order, 5 and 3 sixteenths, then 8 and 5, 13 and 8, 21 and 13 ... up to 233 and 144.

So the band plays ONE pattern at many sizes at once:

  cells of 3 and 2          the guitars' muted strokes (a long is two strokes and a rest, a short one stroke and a
                            rest), with the bass and the kick locked to them
  cells of 8 and 5          the string is let ring: an open low note
  cells of 13 and 8         a chord (on the long ones the root; on the short ones, from the third section, a tritone up)
  cells of 34 and 21        a crash
  cells of 55 and 34        the root: home on the long ones, a semitone up on the short ones
  cells of 233 and 144      THE SECTIONS OF THE SONG: the long ones heavy, the short ones quiet. Long, short, long,
                            long, short, long, short, long: the form is the riff, 78 times slower.

The whole song is the fourteenth line of the rule: 1597 sixteenths, and then one chord where the fifteenth would
begin. The kit keeps common time against all of it (the china in quarters, the snare on three) and starts its count
again at each section. A long section is fourteen bars and nine sixteenths; a short one is exactly nine bars.

In the quiet sections the rule is said another way, by the engine itself: a wire harp (Karplus-Strong, the first on
this record) is given no notes, only the rule as an L-system (the first on this record), written so that each short
cell is born one step up the scale from the long cell that made it. Its tune is therefore each phrase followed by
the phrase before it, one step higher. In the last section the harp plays over the band: the two sayings together.

v1 is the SKELETON (Harry, 17 Nov about 03:40: "open up 2 new song slots"; track 2's terms: mine, my title, a
skeleton first): the whole shape standing, bare.
"""
import bisect
import json
import os

OUT = os.environ.get("C10T7_OUT", os.path.join(os.path.dirname(__file__), "..", "..", "..", "songs", "chirpers10-t7.yaml"))
BPM = 80
F1 = 29
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
T = {}
GEN = 14                                  # the song is the rule's fourteenth line
TOP = 9                                   # the cells that are the song's sections
# the harp: gain ; hall send ; gain in the last section, over the band ("" = it does not play there)
HARP = os.environ.get("C10T7_HARP", "-14dB;-10dB;-12.5dB")
PAD = os.environ.get("C10T7_PAD", "7.5dB;-9dB")        # the clean guitar's chords in the quiet sections: gain ; hall send
# the bass in the quiet sections, dB after its bus (its compressor holds a long soft note at the level of a hard short
# one, so a lower velocity does not make it quieter; this does)
QBASS = os.environ.get("C10T7_QBASS", "-4.5")


def nm(n):
    return f"{NAMES[n % 12]}{n // 12 - 1}"


def word(n):
    """Line n of the rule: W1 = L, W2 = LS, Wn = W(n-1) W(n-2)."""
    a, b = "L", "LS"
    for _ in range(n - 2):
        a, b = b, b + a
    return a if n == 1 else b


SIZE = [(3, 2)]                           # SIZE[k] = (a long's sixteenths, a short's) at size k
for _k in range(GEN):
    SIZE.append((SIZE[-1][0] + SIZE[-1][1], SIZE[-1][0]))


def cells(k):
    """The song at size k: (start sixteenth, 'L' or 'S', length)."""
    out, t = [], 0
    for c in word(GEN - k):
        n = SIZE[k][c == "S"]
        out.append((t, c, n))
        t += n
    return out


LEV = [cells(k) for k in range(GEN)]
STARTS = [[c[0] for c in lv] for lv in LEV]
TOTAL = LEV[0][-1][0] + LEV[0][-1][2]
assert TOTAL == 1597 and all(lv[-1][0] + lv[-1][2] == TOTAL for lv in LEV) and SIZE[TOP] == (233, 144)
assert all(set(STARTS[k + 1]) <= set(STARTS[k]) for k in range(GEN - 1))     # every size's cells begin where smaller cells do
RANK = {}
for _k, _s in enumerate(STARTS):
    for _p in _s:
        RANK[_p] = _k                     # the largest size of cell that begins here


def at_size(k, p):
    """The size-k cell that sixteenth p lies in."""
    return LEV[k][bisect.bisect_right(STARTS[k], p) - 1]


SECS = LEV[TOP]                           # eight: L S L L S L S L
KEY = [0, 0, 0, 3, 3, 0, 0, 0]            # home, a minor third up for the middle pair, home (the rule's own grouping: 3 + 2 + 3)
WIDE = {3, 5, 7}                          # four guitars


def add(tr, s16, len16, pitch, vel, **expr):
    n = {"at": round(s16 / 4, 4), "len": round(len16 / 4 * 0.98, 4), "pitch": nm(pitch) if isinstance(pitch, int) else pitch, "vel": round(vel, 3)}
    if expr:
        n["expr"] = {k: float(v) for k, v in expr.items()}
    T.setdefault(tr, []).append(n)


def drum(piece, s16, vel):
    tr = {"k": "kick", "s": "snare", "h": "hat", "c": "cym", "x": "cym", "rde": "cym"}.get(piece, "toms")
    T.setdefault(tr, []).append({"at": round(s16 / 4, 4), "len": 2.0 if piece in ("c", "x") else 1.0 if piece == "rde" else 0.5 if piece == "h" else 0.25,
                                 "pitch": piece, "vel": round(vel, 3)})


ROOTS = []                                # (sixteenth, the bass's root in semitones over F1): the low bus's eq follows it


def heavy(i, s0, n):
    gtrs = ("gl", "gr", "wl", "wr") if i in WIDE else ("gl", "gr")
    for p, kind, ln in LEV[0]:
        if not s0 <= p < s0 + n:
            continue
        r = RANK[p]
        root = KEY[i] + (1 if at_size(6, p)[1] == "S" else 0)
        if not ROOTS or ROOTS[-1][1] != root:
            ROOTS.append((p, root))
        if r >= 3:                        # a chord: the root on a long cell of 13, a tritone up on a short one of 8
            up = 6 if at_size(3, p)[1] == "S" and i >= 2 else 0
            for tr in gtrs:
                add(tr, p, ln, ",".join(nm(F1 + root + up + j) for j in (0, 7, 12)), 1.0)
            add("bass", p, ln, F1 + root + up, 0.95)
            drum("k", p, 0.95)
            if r >= 5:
                drum("c", p, 0.9 if r >= 8 else 0.75)
        elif r == 2:                      # the string let ring
            for tr in gtrs:
                add(tr, p, 2, F1 + root, 1.0)
            add("bass", p, 2, F1 + root, 0.95)
            drum("k", p, 0.95)
            if ln == 3:
                for tr in gtrs:
                    add(tr, p + 2, 1, F1 + root, 0.85, pm=1)
                add("bass", p + 2, 1, F1 + root, 0.85)
                drum("k", p + 2, 0.85)
        else:                             # muted: a long is two strokes and a rest, a short one stroke and a rest
            for j in range(2 if ln == 3 else 1):
                v = (0.95 if r == 1 else 0.88) if j == 0 else 0.8
                for tr in gtrs:
                    add(tr, p + j, 1, F1 + root, v, pm=1)
                add("bass", p + j, 1, F1 + root, v)
                drum("k", p + j, v)
    # the kit keeps common time and starts its count again with the section
    kit_from = SIZE[8][0] if i == 0 else 0            # the first nine bars: no snare or china yet, a hat in quarters
    for q in range(0, n, 4):
        if q < kit_from:
            drum("h", s0 + q, 0.45)
        else:
            drum("x", s0 + q, 0.55 if q % 16 == 0 else 0.5)
    for q in range(8, n - 9, 16):
        if q >= kit_from:
            drum("s", s0 + q, 0.95)
    for j, pc in enumerate(["t1", "t1", "t2", "t2", "ft", "ft", "s", "s"]):      # the nine-sixteenth bar ends in a fill
        drum(pc, s0 + n - 8 + j, 0.6 + 0.045 * j)


def quiet(i, s0, n):
    key = KEY[i]
    for p, kind, ln in LEV[5]:            # cells of 34 and 21: the chord. F minor on the long ones, D flat on the short ones
        if not s0 <= p < s0 + n:
            continue
        ch, low = ((41, 48, 56), 0) if kind == "L" else ((37, 44, 53), 8)
        add("pad", p, ln - 1, ",".join(nm(x + key) for x in ch), 0.8)
        add("bass", p, ln - 2, F1 + key + low, 0.3)
        ROOTS.append((p, key + low))
    for p, kind, ln in LEV[3]:
        if s0 <= p < s0 + n:
            drum("k", p, 0.3)
    for q in range(0, n, 4):
        drum("rde", s0 + q, 0.4)


def compose():
    for i, (s0, kind, n) in enumerate(SECS):
        (heavy if kind == "L" else quiet)(i, s0, n)
    for tr in ("gl", "gr", "wl", "wr"):                   # where the fifteenth line would begin: one chord
        add(tr, TOTAL, 32, ",".join(nm(F1 + j) for j in (0, 7, 12, 19)), 0.95)
    add("bass", TOTAL, 32, F1, 0.95)
    drum("k", TOTAL, 0.95)
    drum("c", TOTAL, 0.95)
    ROOTS.append((TOTAL, 0))


RULES = {"A": "A", "p": "p", "q": "q[+Br]", "B": "A", "r": "pq"}      # Apq is a long, Br a short; the short is born a step up


def harp_gen(depth, n, pool):
    return {"type": "lsystem", "axiom": "Apq", "rules": RULES, "depth": depth, "n": n, "len": "/16", "notes": " ".join(nm(x) for x in pool)}


def harp_tune(depth):
    """What the engine's turtle will play (for the notes and the docs): the pool step of each cell."""
    s = "Apq"
    for _ in range(depth):
        s = "".join(RULES.get(c, c) for c in s)
    pos, stack, out = 0, [], []
    for c in s:
        if c == "+":
            pos += 1
        elif c == "[":
            stack.append(pos)
        elif c == "]":
            pos = stack.pop()
        elif c.isupper():
            out.append(pos)
    return out


POOL = [53, 56, 60, 63, 65, 68, 72, 75]   # F3 Ab3 C4 Eb4 F4 Ab4 C5 Eb5 (F minor seventh, broken): step 0 sounds once, step 1 at cells 1 2 3 5 8 13 21 34


def song():
    compose()
    kit = "ct-kit-here"
    air = [{"type": "eq", "bands": ["highshelf cutoff=9000 gain=-2dB"]}]
    main = "ct-twin fx.1.model=gojira fx.2.mic=0.5 fx.2.cone={}"
    mids = {"fx": [{"type": "eq", "bands": ["peak cutoff=700 q=0.9 gain=2.5dB"]}]}
    wall = {"fx": [{"type": "eq", "bands": ["peak cutoff=380 q=1 gain=-3dB"]}]}
    hg, hh, h8 = HARP.split(";")
    harps = [(i, s0, 8, 144, [x + KEY[i] + (12 if i == 6 else 0) for x in POOL], hg) for i, (s0, kind, n) in enumerate(SECS) if kind == "S"]
    if h8:
        harps.append((7, SECS[7][0], 9, 233, [x + 12 for x in POOL], h8))
    tracks = [
        {"name": "gl", "patch": main.format(50), "gain": "-0.7dB", "pan": -1, "out": "gtrs", **mids},
        {"name": "gr", "patch": main.format(51), "gain": "-0.7dB", "pan": 1, "out": "gtrs", **mids},
        {"name": "wl", "patch": "ct-wall-stop-l", "gain": "-3.5dB", "pan": -0.75, "out": "gtrs", **wall},
        {"name": "wr", "patch": "ct-wall-stop-r", "gain": "-3.5dB", "pan": 0.75, "out": "gtrs", **wall},
        *[{"name": f"harp{i + 1}", "patch": "em-harp", "gain": g, "pan": 0.25, "at": f"{s0 / 4:g}b", "sends": {"hall": hh},
           "gen": [harp_gen(d, n, pool)]} for i, s0, d, n, pool, g in harps],
        {"name": "pad", "patch": "ct-glass", "gain": PAD.split(";")[0], "pan": -0.3, "sends": {"hall": PAD.split(";")[1]}},
        {"name": "bass", "patch": "ct-bass", "gain": "0.5dB", "pan": 0, "out": "low"},
        {"name": "kick", "patch": kit, "gain": "2dB", "out": "drums", "fx": [{"type": "eq", "bands": ["peak cutoff=4500 q=0.8 gain=10dB"]}]},
        {"name": "snare", "patch": kit, "gain": "3.5dB", "out": "drums", "sends": {"oh": "-1.5dB", "snr": "-10dB"},
         "fx": [{"type": "eq", "bands": ["highshelf cutoff=7000 gain=-3dB"]}]},
        {"name": "toms", "patch": kit, "gain": "4dB", "out": "drums", "sends": {"oh": "-1.5dB"}},
        {"name": "cym", "patch": kit, "gain": "-4.5dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air},
        {"name": "hat", "patch": kit, "gain": "14dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air},
    ]
    for t in tracks:
        if "gen" not in t:
            t["notes"] = sorted(T.get(t["name"], []), key=lambda n: n["at"])

    def key_f(hz):
        return {"value": hz, "mod": [{"src": "auto.key", "amount": round(1 / 12, 5)}]}

    pts, prev = [["0b", ROOTS[0][1]]], ROOTS[0][1]
    for p, r in ROOTS[1:]:
        if r != prev:
            pts += [[f"{p / 4 - 0.02:g}b", prev], [f"{p / 4:g}b", r]]
            prev = r
    qpts = [["0b", 0]]
    for s0, kind, n in SECS:
        if kind == "S":
            qpts += [[f"{s0 / 4 - 0.02:g}b", 0], [f"{s0 / 4:g}b", float(QBASS)], [f"{(s0 + n) / 4 - 0.02:g}b", float(QBASS)], [f"{(s0 + n) / 4:g}b", 0]]
    return {
        "about": ("chirpers X (Common Time), track 7 by chirper-zero: Extreme and Mean. Two cells, a long of three sixteenths and a short "
                  "of two, and one rule: a long becomes a long and a short, a short becomes a long. The pattern it makes never loops and "
                  "is the same at every size, so the band plays it at many sizes at once: muted strokes, open notes, chords, crashes, "
                  "the root, and the song's own sections (long ones heavy, short ones quiet). The kit keeps common time against it. In "
                  "the quiet sections a wire harp has no notes, only the rule (the engine's L-system). The slow song: 80. v1 is the skeleton."),
        "tempo": BPM, "ceiling": "-1dB", "loudness": -10, "seed": 1, "tail": "5s", "length": f"{(TOTAL + 32) / 4:g}b", "event_stable": True,
        "patches": {
            "ct-kit-here": {"extends": "ct-kit", "kit": {"x": {"pan": 0.35}, "rde": {"pan": 0.4}, "rb": {"pan": 0.35}, "h": {"pan": -0.45}}},
            "em-harp": {"about": ("Extreme and Mean's wire harp (chirper-zero, 17 Nov): the library's ks-harp (Karplus-Strong, stretch 3) with a "
                                  "release long enough for a sixteenth-long pluck to ring on."),
                        "gain": "-5dB",
                        "synth": {"amp": {"a": "1ms", "d": 0, "s": 1, "r": "2.5s"},
                                  "layers": [{"type": "ks", "bright": 0.8, "decay": "5s", "ks": {"blend": 1, "stretch": 3}}]}},
        },
        "buses": {
            "hall": {"fx": ["reverb kind=hall decay=4.5s mix=1 predelay=30ms low_cut=150"]},
            "drums": {"fx": ["reverb kind=room decay=0.7s mix=0.1 predelay=8ms",
                             {"type": "glue", "threshold": "-24dB", "ratio": 2.5, "attack": "20ms", "release": "140ms", "knee": 6.0},
                             "clip drive=0dB ceiling=-13dB",
                             {"type": "eq", "bands": ["peak cutoff=400 q=0.8 gain=-6dB", "peak cutoff=5500 q=0.9 gain=1dB", "highshelf cutoff=9000 gain=-2dB", "lp cutoff=14250 q=0.8"]}]},
            "oh": {"fx": ["reverb kind=room decay=0.7s mix=1 predelay=4ms low_cut=5000 high_cut=12000 spread=0.6", {"type": "eq", "bands": ["lp cutoff=14250 q=0.8"]}]},
            "snr": {"fx": [{"type": "eq", "bands": ["peak cutoff=300 q=0.7 gain=-12dB"]}]},
            "gtrs": {"fx": [{"type": "eq", "bands": ["peak cutoff=330 q=1.2 gain=-2dB"]}, "reverb kind=room decay=0.35s mix=0.06 predelay=6ms"]},
            "low": {"fx": [{"type": "eq", "bands": [{"kind": "peak", "cutoff": key_f(44), "q": 1.5, "gain": "-7dB"}, {"kind": "peak", "cutoff": key_f(90), "q": 1.0, "gain": "7.5dB"},
                                                    {"kind": "peak", "cutoff": 350, "q": 1.0, "gain": "-8dB"}, {"kind": "peak", "cutoff": 1500, "q": 1.0, "gain": "4dB"}]},
                           {"type": "compressor", "threshold": "-26dB", "ratio": 8.0, "attack": "12ms", "release": "120ms", "makeup": "2.5dB"},
                           {"type": "eq", "bands": [{"kind": "peak", "cutoff": key_f(170), "q": 1.2, "gain": "-3dB"}]},
                           {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.quiet", "amount": 1}]}}],
                    "auto": {"key": {"points": pts, "curve": 0}, "quiet": {"points": qpts, "curve": 0}}},
        },
        "master": {"fx": [{"type": "eq", "bands": ["hp cutoff=24"]}, {"type": "gain", "gain": os.environ.get("C10T7_MASTER", "2.7dB")}]},
        "tracks": tracks,
    }


def dump(doc):
    lines = []
    for k, v in doc.items():
        if k == "tracks":
            lines.append("tracks:")
            lines += ["  - " + json.dumps(t) for t in v]
        else:
            lines.append(f"{k}: {json.dumps(v)}")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    if os.environ.get("C10T7_SHOW"):
        sec = 15 / BPM
        for i, (s0, kind, n) in enumerate(SECS):
            print(f"section {i + 1} {kind} {'heavy' if kind == 'L' else 'quiet'}  sixteenths {s0}-{s0 + n}  bars {s0 / 16 + 1:.2f}-{(s0 + n) / 16 + 1:.2f}  "
                  f"{int(s0 * sec) // 60}:{s0 * sec % 60:04.1f}-{int((s0 + n) * sec) // 60}:{(s0 + n) * sec % 60:04.1f}  key +{KEY[i]}")
        print("the first 34 cells:", "".join(c[1] for c in LEV[0][:34]))
        print("their sizes:       ", "".join(str(min(RANK[c[0]], 9)) for c in LEV[0][:34]))
        print("the harp's steps:  ", "".join(str(x) for x in harp_tune(8)))
    else:
        open(OUT, "w").write(dump(song()))
