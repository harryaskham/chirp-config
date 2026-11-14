#!/usr/bin/env python3
"""chirpers10-t2 "Odd Sympathy" (chirper-zero): one riff and two clocks.

In 1665 Huygens hung two pendulum clocks from one beam and found that, however he started them, within half an hour they
swung exactly against each other; he called it "an odd kind of sympathy". This is that, for two guitars.

Common Time (track 1) keeps one pulse and turns three cells of different lengths under it. This piece is the other way
round: ONE cell, one bar long, on two guitars, left and right, each with its own clock. They start in step. The right
guitar's clock runs a hair fast: it slips ahead of the left by a sixteenth, holds there, slips again, and so on, each
hold a canon of the riff with itself at a new distance, until it is half a bar ahead: exactly against the left. The riff
is written so that there, and only there, the two halves fit: every sixteenth of the bar has one guitar on it and never
both (the riff's second half is the negative of its first). What was a riff with holes is a machine with none.

The slips are the engine's track `warp` (the right-hand tracks' own clock against the song's); nothing is shifted by hand.

v1 is the SKELETON (Harry, 14 Nov: "should skeleton it and then climb both"): the whole shape standing, bare.
"""
import json
import os

OUT = os.environ.get("C10T2_OUT", os.path.join(os.path.dirname(__file__), "..", "..", "..", "songs", "chirpers10-t2.yaml"))
BPM = 108
F1 = 29
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]


def nm(n):
    return f"{NAMES[n % 12]}{n // 12 - 1}"


# THE RIFF: sixteen sixteenths. (position, length, kind): c a palm-muted chug on the open low string, o the string open,
# h a hook note. Its attacks are 0 1 3 6 | 10 12 13 15: of every pair of sixteenths half a bar apart exactly one is struck.
# Every note is short and the gaps are real rests (a riff with holes): the piece is about what fills them.
RIFF = [(0, 1, "c"), (1, 1, "c"), (3, 2, "o"), (6, 2, "h0"), (10, 1.5, "h1"), (12, 1, "c"), (13, 1, "c"), (15, 1, "h2")]
ATTACKS = [p for p, _, _ in RIFF]
assert all((p in ATTACKS) != ((p + 8) % 16 in ATTACKS) for p in range(16)), "the two halves must be each other's negative"
# the hook's notes are three of Common Time's four (Ab Gb B C over F): the tritone, the minor third, the fifth
HOOK = [F1 + 6, F1 + 3, F1 + 7]
CHUGS = [p for p, _, k in RIFF if k == "c"]

# THE FORM, in bars (4/4). The right guitar's lead over the left, in sixteenths, at each station.
FORM = [
    ("one clock", 0, 8, 0),          # the left guitar alone and a pendulum; the bass and kick join
    ("in step", 8, 24, 0),           # both, together
    ("slip", 24, 28, None),
    ("a sixteenth", 28, 32, 1),
    ("slip", 32, 36, None),
    ("an eighth", 36, 48, 2),
    ("slip", 48, 50, None),
    ("three", 50, 56, 3),
    ("slip", 56, 58, None),
    ("a quarter", 58, 74, 4),
    ("let go", 74, 98, None),        # no beam: clean guitars, the right one drifting all the way to half a bar
    ("against", 98, 122, 8),         # exactly against each other: the bar is full
    ("two clocks", 122, 130, 8),     # the guitars alone, then the ticks
]
NB = 130
# the right-hand clock (track `warp`): stretches in turn from the start; `to` is its shift in beats, negative = ahead
WARP = [
    {"over": "96b", "to": 0},
    {"over": "16b", "to": -0.25, "curve": "smooth"}, {"over": "16b", "to": -0.25},
    {"over": "16b", "to": -0.5, "curve": "smooth"}, {"over": "48b", "to": -0.5},
    {"over": "8b", "to": -0.75, "curve": "smooth"}, {"over": "24b", "to": -0.75},
    {"over": "8b", "to": -1.0, "curve": "smooth"}, {"over": "64b", "to": -1.0},
    {"over": "88b", "to": -2.0, "curve": "linear"},          # bars 74-96: the long drift, a little over 1% fast
]

T = {}


def add(tr, s16, len16, pitch, vel, **expr):
    n = {"at": round(s16 / 4, 4), "len": round(len16 / 4 * 0.98, 4), "pitch": nm(pitch) if isinstance(pitch, int) else pitch, "vel": round(vel, 3)}
    if expr:
        n["expr"] = {k: float(v) for k, v in expr.items()}
    T.setdefault(tr, []).append(n)


def riff(tr, b0, b1, vel=0.85, up=0, clean=False, ramp=None):
    """The riff on a track, bars b0..b1. Heavy: chugs muted. Clean (`up` semitones higher): every note a short tick."""
    for b in range(b0, b1):
        v = vel * (ramp[0] + (ramp[1] - ramp[0]) * (b - b0) / max(1, b1 - b0 - 1)) if ramp else vel
        for p, ln, kind in RIFF:
            t = b * 16 + p
            if kind == "c":
                if clean:
                    add(tr, t, 1, F1 + up, v * 0.8)
                else:
                    add(tr, t, ln, F1, v * (1.0 if p in (0, 12) else 0.9), pm=1)
            elif kind == "o":
                add(tr, t, 1 if clean else ln, F1 + up + (12 if clean else 0), v)
            else:
                add(tr, t, 2 if clean else ln, HOOK[int(kind[1])] + up, v * 1.05)


def bass(b0, b1, lead=0, vel=0.9):
    """The bass keeps the LEFT clock; where the right guitar is locked `lead` sixteenths ahead it takes its chugs too."""
    for b in range(b0, b1):
        seen = set()
        for p, ln, kind in RIFF:
            add("bass", b * 16 + p, ln, F1 if kind in "co" else HOOK[int(kind[1])], vel)
            seen.add(p)
        if lead:
            for p in CHUGS:
                q = (p - lead) % 16
                if q not in seen:
                    add("bass", b * 16 + q, 1, F1, vel * 0.85)


def drum(piece, s16, vel):
    tr = {"k": "kick", "s": "snare", "g": "snare", "h": "hat", "c": "cym", "x": "cym", "cch": "cym", "rb": "ride", "rd": "ride"}.get(piece, "toms")
    T.setdefault(tr, []).append({"at": round(s16 / 4, 4), "len": 2.0 if piece in ("c", "x") else 0.5 if piece in ("h", "rb", "rd") else 0.25, "pitch": piece, "vel": round(vel, 3)})


def groove(b0, b1, lead, snare, cym, kvel=0.92):
    """A station's beat: the kick on every chug of either guitar (and the left's open string), the snare on `snare`,
    a cymbal on the quarter."""
    kicks = sorted(set(CHUGS + [3]) | {(p - lead) % 16 for p in CHUGS})
    for b in range(b0, b1):
        for p in kicks:
            drum("k", b * 16 + p, kvel * (1.0 if p % 4 == 0 else 0.9))
        for p in snare:
            drum("s", b * 16 + p, 0.95)
        for p in range(0, 16, 4):
            drum(cym, b * 16 + p, 0.6 if p == 0 else 0.5)
    drum("c", b0 * 16, 0.9)


def fill(b, kind="toms"):
    """The last half bar before bar `b`."""
    if kind == "toms":
        for i, pc in enumerate(["t1", "t1", "t2", "t2", "ft", "ft", "s", "s"]):
            drum(pc, b * 16 - 8 + i, 0.6 + 0.045 * i)
    else:
        for i in range(8):
            drum("s", b * 16 - 8 + i, 0.5 + 0.06 * i)


def pendulum(b0, b1, vel=0.42):
    for b in range(b0, b1):
        drum("rb", b * 16, vel * 1.12)       # tick
        drum("rb", b * 16 + 8, vel)          # tock


def compose():
    # one clock: no introduction (Common Time has the long wait; this starts). The left guitar alone with the riff and a
    # pendulum; then the bass and the kick under it
    pendulum(0, 8)
    T.setdefault("home", []).append({"at": 0, "len": 32.2, "pitch": "F1", "vel": 0.55})
    riff("gl", 0, 8, vel=0.85)
    bass(4, 8)
    for b in range(4, 8):
        for p in CHUGS:
            drum("k", b * 16 + p, 0.85)
        for p in range(0, 16, 4):
            drum("h", b * 16 + p, 0.45)
    fill(8)
    # in step
    riff("gl", 8, 24)
    riff("gr", 8, 24)
    bass(8, 24)
    groove(8, 24, 0, snare=(8,), cym="x")
    for name, b0, b1, lead in FORM[2:10]:
        riff("gl", b0, b1)
        riff("gr", b0, b1)
        bass(b0, b1, lead or 0)
        if lead is None:                 # a slip: the beat thins to a kick on the bar line and a hat, so the slip is heard
            for b in range(b0, b1):
                drum("k", b * 16, 0.85)
                for p in range(0, 16, 4):
                    drum("h", b * 16 + p, 0.45)
            fill(b1, "snare" if b1 - b0 < 4 else "toms")
        else:
            groove(b0, b1, lead, snare=(4, 12) if lead in (2, 4) else (8,), cym="h" if lead == 2 else "rd" if lead == 4 else "x")
    # let go: the heavy guitars stop; two clean guitars tick the riff, the right one drifting from a quarter to half a bar
    # ahead; the swarm (sixteen oscillators finding a common phase) locks as they arrive
    for tr in ("cl", "cr"):
        riff(tr, 74, 98, vel=0.5, up=24, clean=True, ramp=(0.8, 1.1))
    pendulum(74, 98)
    for b in range(86, 98):
        drum("k", b * 16, 0.4 + 0.03 * (b - 86))
    T.setdefault("home", []).append({"at": 74 * 4, "len": 96.2, "pitch": "F1", "vel": 0.55})
    for n in ("F2", "C3"):
        T.setdefault("air", []).append({"at": 74 * 4, "len": 96.2, "pitch": n, "vel": 0.45})
    for n in ("F3", "C4"):
        T.setdefault("swarm", []).append({"at": 74 * 4, "len": 96.0, "pitch": n, "vel": 0.7})
    fill(98)
    # against: half a bar apart. Every sixteenth has one guitar on it
    riff("gl", 98, 122, vel=0.9)
    riff("gr", 98, 122, vel=0.9)
    bass(98, 122, 8, vel=0.95)
    groove(98, 122, 8, snare=(4, 12), cym="x")
    for b in range(102, 122, 4):
        drum("c", b * 16, 0.85)
    # two clocks: the guitars alone, still against each other; then only the ticks
    riff("gl", 122, 126, vel=0.85)
    riff("gr", 122, 126, vel=0.85)
    drum("c", 122 * 16, 0.9)
    pendulum(122, 130)
    for tr in ("cl", "cr"):
        riff(tr, 126, 130, vel=0.45, up=24, clean=True, ramp=(1.0, 0.6))
    T.setdefault("home", []).append({"at": 126 * 4, "len": 16.0, "pitch": "F1", "vel": 0.5})


# the heavy rig: Common Time's tight rig on the engine's own cabinet (sounds.md), one a side
HEAVY = (" fx.0.mix=0 synth.layers.0.soft=expr.pm fx.2.tight=220 fx.3.mix=0"
         + "".join(f" fx.4.bands.{i}.gain=0dB" for i in range(7)))
CLEAN = "ct-clean synth.layers.0.inharm=0.00008"
DRIP = {"type": "reverb", "kind": "spring", "drip": 1, "decay": "1.8s", "mix": 0.22}     # the spring that drips (engine feature 5)
# the swarm, as in Common Time: sixteen saws to a note pulled toward a common phase by a coupling the `sync` lane sets
SWARM = {"about": "chirper-zero: the swarm - sixteen saws to a note, each at its own pitch (60 cents' spread), pulled toward their common phase by a coupling the track's `sync` lane sets (0 a crowd, 1 the critical point, 3 locked); a low-pass opens as they agree. As in Common Time (track 1).",
         "synth": {"layers": [{"type": "kuramoto", "kuramoto": {"count": 16, "spread": 60, "coupling": {"value": 0, "mod": [{"src": "auto.sync", "amount": 1}]}}}],
                   "filters": [{"kind": "lp", "cutoff": {"value": 350, "mod": [{"src": "sync", "amount": 2.6}]}}], "amp": {"a": "1.5s", "d": 0, "s": 1, "r": "3s"}}, "gain": "-9.5dB"}


def song():
    compose()
    cab = lambda cone: [{"type": "cab", "model": "4x12-modern", "mic": 0.25, "distance": 0.15, "cone": cone}]
    kit = "ct-kit-here"
    air = [{"type": "eq", "bands": ["highshelf cutoff=9000 gain=-2dB"]}]
    b = lambda bar: f"{bar * 4}b"
    spec = [
        {"name": "gl", "patch": "ct-chug-l" + HEAVY, "gain": "3.3dB", "pan": -1, "out": "gtrs", "fx": cab(12)},
        {"name": "gr", "patch": "ct-chug-r" + HEAVY, "gain": "3.3dB", "pan": 1, "out": "gtrs", "fx": cab(13), "warp": WARP},
        {"name": "cl", "patch": CLEAN, "gain": "1dB", "pan": -0.7, "sends": {"hall": "-9dB"}, "fx": [DRIP]},
        {"name": "cr", "patch": CLEAN, "gain": "1dB", "pan": 0.7, "sends": {"hall": "-9dB"}, "fx": [DRIP], "warp": WARP},
        {"name": "bass", "patch": "ct-bass", "gain": "0.5dB", "pan": 0, "out": "low"},
        {"name": "kick", "patch": kit, "gain": "2dB", "out": "drums", "fx": [{"type": "eq", "bands": ["peak cutoff=4500 q=0.8 gain=10dB"]}]},
        {"name": "snare", "patch": kit, "gain": "8dB", "out": "drums", "sends": {"oh": "-1.5dB"}},
        {"name": "toms", "patch": kit, "gain": "4dB", "out": "drums", "sends": {"oh": "-1.5dB"}},
        {"name": "cym", "patch": kit, "gain": "-3dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air},
        {"name": "hat", "patch": kit, "gain": "14dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air},
        {"name": "ride", "patch": kit, "gain": "6dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air},
        {"name": "home", "patch": "contrabass-tight", "gain": "-9dB", "pan": 0.3, "sends": {"hall": "-12dB"}},
        {"name": "air", "patch": "juno-pad", "gain": "-13dB", "pan": 0.15, "sends": {"hall": "-8dB"}},
        {"name": "swarm", "patch": "ot-swarm", "gain": {"value": "-14dB", "mod": [{"src": "auto.lvl", "amount": 1}]}, "pan": 0, "sends": {"hall": "-8dB"},
         "auto": {"sync": {"points": [["0b", 0.3], [b(74), 0.3], [b(90), 1.0], [b(95), 1.4], [b(96), 3], [b(NB), 3]]},
                  "lvl": {"points": [["0b", 0], [b(74), -6], [b(80), 2], [b(96), 4], [b(98), -6], [b(NB), -6]]}}},
    ]
    tracks = []
    for t in spec:
        if t["name"] in T:
            tracks.append({**t, "notes": sorted(T[t["name"]], key=lambda n: n["at"])})
    return {
        "about": ("chirpers X (Common Time), track 2 by chirper-zero: \"Odd Sympathy\". One riff, one bar long, on two guitars, left "
                  "and right, each with its own clock. They start in step; the right one slips ahead a sixteenth at a time (the "
                  "engine's track warp), holding at each distance, until it is half a bar ahead, exactly against the left, and "
                  "there the riff's two halves fit: every sixteenth has one guitar on it and never both. After Huygens's two "
                  "pendulum clocks on one beam (1665), which always ended swinging against each other. v1: the skeleton."),
        "tempo": BPM, "ceiling": "-1dB", "loudness": -10, "seed": 1, "tail": "4s", "length": f"{NB * 4}b", "event_stable": True,
        "patches": {"ct-kit-here": {"extends": "ct-kit", "kit": {"x": {"pan": 0.35}, "rde": {"pan": 0.4}, "rb": {"pan": 0.35}, "h": {"pan": -0.45}}},
                    "ot-swarm": SWARM},
        "buses": {
            "hall": {"fx": ["reverb kind=hall decay=4.5s mix=1 predelay=30ms low_cut=150"]},
            "drums": {"fx": ["reverb kind=room decay=0.7s mix=0.1 predelay=8ms",
                             {"type": "glue", "threshold": "-24dB", "ratio": 2.5, "attack": "20ms", "release": "140ms", "knee": 6.0},
                             "clip drive=0dB ceiling=-13dB",
                             {"type": "eq", "bands": ["peak cutoff=400 q=0.8 gain=-6dB", "peak cutoff=5500 q=0.9 gain=1dB", "highshelf cutoff=9000 gain=-2dB"]}]},
            "oh": {"fx": ["reverb kind=room decay=0.7s mix=1 predelay=4ms low_cut=5000 high_cut=12000 spread=0.6"]},
            "gtrs": {"fx": [{"type": "gain", "gain": "0dB"}]},
            "low": {"fx": [{"type": "eq", "bands": ["peak cutoff=44 q=1.5 gain=-7dB", "peak cutoff=90 q=1 gain=7.5dB", "peak cutoff=350 q=1 gain=-8dB", "peak cutoff=1500 q=1 gain=4dB"]},
                           {"type": "compressor", "threshold": "-26dB", "ratio": 8.0, "attack": "12ms", "release": "120ms", "makeup": "2.5dB"},
                           {"type": "eq", "bands": ["peak cutoff=170 q=1.2 gain=-3dB"]}]},
        },
        "master": {"fx": [{"type": "eq", "bands": ["hp cutoff=24"]}, {"type": "gain", "gain": "1.6dB"}]},
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
    open(OUT, "w").write(dump(song()))
