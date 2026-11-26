#!/usr/bin/env python3
"""Escapement (Chirpers 11), track 7 (chirper-zero): OUT OF STEP. The slot's word is PHASE.

ONE PATTERN AGAINST ITSELF. Two clicks, the same sound, play the same half-bar pattern (PATTERN: x x . x . x x .).
A is on the grid and never moves. B is the same loop a hair shorter: its phase, phi, is how many sixteenths it is
ahead of A, and every B stroke sounds when t + phi(t) reaches it. Nothing else is written for B.

THE ESCAPEMENT. In "slips" the phase goes up by one sixteenth a row: for the first SLIDE bars of each row B creeps
ahead, slowly at first and then faster (phi = k + u^2), and CATCHES on the next sixteenth, where it stays locked for
the rest of the row: a tooth of the wheel. Each lock is a different pattern made of the same two (the eight
rotations), and after eight rows B is a whole half-bar ahead, which is where it started: "home".

THREE KINDS OF PHASE, ONE ARITHMETIC. (1) The rhythm: the locks. (2) The sound: as B leaves a lock, strokes that
were together are a millisecond apart, then two, then five, and two copies of one click that close cancel at the
frequencies whose half-wave is the gap: a comb that sweeps down as the gap opens. There is no phaser on the record;
this is one. (3) The bass: pairs of sines, each pair DELTA Hz apart (G2 and G2 + DELTA, and the same on its harmonics), where
DELTA is one cycle a beat. Struck on the off-beat they agree there and cancel on every beat, exactly where the bass drum is: the pump of
a side-chain, with no compressor and no envelope, only two tones out of step.

THE LONG ARC. Both clicks pass one low-pass whose opening IS the phase: dull at 4 kHz while they are together,
a step brighter at every catch, wide open at home; and it closes again as B drifts back.

In "drifts" B lets go: its phase runs back from eight to nothing at one steady speed (a sixteenth every four
bars, Piano Phase's way), through every lock without stopping, and is one click again at the end.

THE FORM IS ARITHMETIC: a row is ROW bars; SECTIONS lists each section's rows, its parts (a part may be given the
bars of the section it plays) and what the phase does. Every note comes from those.

v1 is the SKELETON (26 Nov): the process, stated whole, with few sounds.

v2 (26 Nov): THE MOULD (C11T7_COMP=0 takes it out: v1). The pattern has three holes in its eight sixteenths
(2, 4 and 7). From "home" a third click, C, small and bright and on the grid, plays the holes and nothing else:
the pattern's complement. When A and B are together the two patterns interlock and every sixteenth of the bar
sounds exactly once: that is what home is, and it is why the wheel was turned eight times to get back. In "drifts",
as B lets go, its strokes fall into the holes C is filling: B and C strike together where they never could at home
(on one, two or all three of C's strokes, by how far ahead B is: all three at four ahead), and the bar goes lumpy;
when B is home again it is smooth again. Home is the only phase at which B and C never meet.
"""
import json
import math
import os

OUT = os.environ.get("C11T7_OUT", os.path.join(os.path.dirname(__file__), "..", "..", "..", "songs", "chirpers11-t7.yaml"))
BPM = 126
BEATS = 4
ROW = 8
STEP = 0.25
BAR = 16                       # sixteenths

PATTERN = (0, 1, 3, 5, 6)      # of eight sixteenths: x x . x . x x .
LOOP = 8
SLIDE = 2                      # bars B takes to slip from one lock to the next
NOTE = "G3"
F0 = 97.9989                   # G2
DULL = 4000                    # Hz: the clicks' low-pass when B is with A
OCTAVES = 1.7                  # ... and how far it opens when B is a whole loop ahead
DELTA = BPM / 60               # Hz: one cycle a beat

COMP_ON = os.environ.get("C11T7_COMP", "1") != "0"    # v2: the complement, C
COMP = tuple(s for s in range(LOOP) if s not in PATTERN)   # the holes: 2, 4, 7
C = {"c": None} if COMP_ON else {}
ALL = None
# name, rows, {part: None, or the (from bar, to bar) stretches of the section it plays}, the phase: ("lock", k) | ("slips", k0) | ("drift", from, to)
SECTIONS = [
    ("one click", 3, {"a": ALL, "b": [(8, 24)], "kick": [(16, 24)]},                                                          ("lock", 0)),
    # the bass drum stands back while B slips to its last lock (8, which is home), and for the whole of the fifth row,
    # where the bass is heard pumping with no drum to pump it
    ("slips",     8, {"a": ALL, "b": ALL, "kick": [(0, 32), (40, 56), (58, 64)], "bass": [(16, 64)], "clap": [(40, 56), (58, 64)], "hat": [(32, 56), (58, 64)]}, ("slips", 0)),
    ("home",      2, {"a": ALL, "b": ALL, "kick": ALL, "bass": ALL, "clap": ALL, "hat": ALL, **C},                            ("lock", 8)),
    ("drifts",    4, {"a": ALL, "b": ALL, "kick": [(0, 16), (24, 32)], "bass": ALL, "clap": [(0, 16), (24, 32)], "hat": ALL, **C},  ("drift", 8, 0)),
    ("one again", 3, {"a": ALL, "b": [(0, 20)], "kick": [(0, 8)], "bass": [(0, 16)], "clap": [(0, 8)], "hat": [(0, 8)], **({"c": [(0, 16)]} if COMP_ON else {})}, ("lock", 0)),
]


def starts():
    out, b = [], 0
    for name, rows, parts, phase in SECTIONS:
        out.append((name, b, rows * ROW, parts, phase)); b += rows * ROW
    return out, b


SECS, BARS = starts()
TOTAL = BARS * BEATS


def plays(part, bar):
    for name, b0, n, parts, phase in SECS:
        if b0 <= bar < b0 + n:
            if part not in parts:
                return False
            w = parts[part]
            return w is None or any(lo <= bar - b0 < hi for lo, hi in w)
    return False


def phi(t):
    """B's phase at time t (sixteenths from the start): how many sixteenths it is ahead of A."""
    bar = t / BAR
    for name, b0, n, parts, phase in SECS:
        if b0 <= bar < b0 + n or (name == SECS[-1][0] and bar >= b0):
            u = bar - b0
            if phase[0] == "lock":
                return float(phase[1])
            if phase[0] == "slips":
                k, v = int(u // ROW), (u % ROW) / SLIDE
                return phase[1] + k + (v * v if v < 1 else 1.0)
            if phase[0] == "drift":
                return phase[1] + (phase[2] - phase[1]) * u / n
    return 0.0


def when(b):
    """The time (sixteenths) at which B, running ahead by phi, reaches its own sixteenth b: t + phi(t) = b."""
    lo, hi = b - 10.0, b + 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if mid + phi(mid) < b:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def note(at, pitch, length, vel):
    return {"at": round(at, 5), "len": round(length, 4), "pitch": pitch, "vel": round(vel, 3)}


def part(name, steps):
    out = []
    for bar in range(BARS):
        if plays(name, bar):
            out += [note(bar * BEATS + s * STEP, p, n * STEP, v) for s, p, n, v in steps(bar)]
    return out


VEL = lambda s: 0.9 if s % LOOP == 0 else 0.76


def open_lane():
    """How bright both clicks are: the phase itself, as a share of the loop (0 together, 1 a whole loop ahead)."""
    pts, last = [], None
    for h in range(BARS * 2 + 1):
        v = round(phi(min(h * BAR / 2, BARS * BAR - 0.001)) / LOOP, 4)
        if v != last or h == BARS * 2:
            if last is not None and pts and pts[-1][0] != f"{(h - 1) * 2:g}b":
                pts.append([f"{(h - 1) * 2:g}b", last])
            pts.append([f"{h * 2:g}b", v])
        last = v
    return pts


def a_notes():
    return [note(s * STEP, NOTE, 0.5 * STEP, VEL(s)) for s in range(BARS * BAR) if s % LOOP in PATTERN and plays("a", s // BAR)]


def c_notes():
    """The complement: C strikes the pattern's holes, on the grid."""
    return [note(s * STEP, "G5", 0.25 * STEP, 0.85 if s % LOOP == COMP[0] else 0.72) for s in range(BARS * BAR) if s % LOOP in COMP and plays("c", s // BAR)]


def b_notes():
    out = []
    for b in range(int(BARS * BAR + 9)):
        if b % LOOP in PATTERN:
            t = when(b)
            if 0 <= t < BARS * BAR and plays("b", int(t // BAR)):
                out.append(note(t * STEP, NOTE, 0.5 * STEP, VEL(b)))
    return out


KICK = lambda bar: [(s, "G1", 1, 0.95 if s == 0 else 0.9) for s in (0, 4, 8, 12)]
CLAP = lambda bar: [(4, "C4", 1, 0.8), (12, "C4", 1, 0.86)]
HAT = lambda bar: [(s, "A#4", 1, 0.8) for s in (2, 6, 10, 14)]
BASS = lambda bar: [(2, "G2", 15.6, 0.9)]      # struck on the off-beat, held for the bar: its two tones agree on the off-beats

R = 1 + DELTA / F0             # the second tone of each pair, as a ratio of the note
PATCHES = {
    "os-click": {"about": "Out of Step's click (chirper-zero, 26 Nov): five cycles of a saw on G3 dying in 22 ms, lifted 9 dB round 9 kHz, started at the same point of its wave every time, through a low-pass that both clicks share (it opens with the phase): nothing in it is random, so two of them struck together are one click, and two struck a millisecond apart are a comb. (The machine's rim was tried first: two rims differ by 22 dB under one, and its note stood 16 to 25 dB over the album's envelope.)",
                 "play": {"vel_sens": 0.5},
                 "synth": {"layers": ["saw phase=0"], "filters": ["hp cutoff=500", "peak cutoff=9000 q=0.7 gain=9dB", {"kind": "lp", "cutoff": {"value": DULL, "mod": [{"src": "auto.open", "amount": OCTAVES}]}, "q": 0.7}], "amp": {"a": "0.1ms", "d": "22ms", "s": 0, "r": "10ms", "curve": 3}}},
    "os-comp": {"about": "Out of Step's third click (chirper-zero, 26 Nov, v2): the complement's. Two cycles of a saw on G5 dying in 12 ms, above 3 kHz, lifted 8 dB round 10 kHz: small and bright, so that it is heard as the holes being filled and not as a third pattern.",
                "play": {"vel_sens": 0.5},
                "synth": {"layers": ["saw phase=0"], "filters": ["hp cutoff=3000", "peak cutoff=10000 q=0.7 gain=8dB"], "amp": {"a": "0.1ms", "d": "12ms", "s": 0, "r": "8ms", "curve": 3}}},
    "os-kick": {"about": "Out of Step's bass drum (chirper-zero, 26 Nov): the engine's machine kick, short and dry, on G1.",
                "play": {"vel_sens": 0.3},
                "synth": {"layers": [{"type": "machine", "machine": {"part": "kick", "decay": "260ms", "click": 0.6, "drive": 0.35, "punch": 22, "punch_time": "32ms"}}],
                          "filters": ["hp cutoff=28"], "amp": {"a": "0.1ms", "d": "0s", "s": 1, "r": "1s"}}},
    "os-hat": {"about": "Out of Step's hat (chirper-zero, 26 Nov): the machine's hat, 45 ms, on the off-beats once the two clicks are home.",
               "play": {"vel_sens": 0.4},
               "synth": {"layers": [{"type": "machine", "machine": {"part": "hat", "decay": "45ms"}}], "filters": ["hp cutoff=6000"], "amp": {"a": "0.1ms", "d": "0s", "s": 1, "r": "150ms"}}},
    "os-clap": {"about": "Out of Step's clap (chirper-zero, 26 Nov): the machine's clap, three bursts, short, dry.",
                "play": {"vel_sens": 0.4},
                "synth": {"layers": [{"type": "machine", "machine": {"part": "clap", "bursts": 3, "decay": "140ms"}}], "amp": {"a": "0.1ms", "d": "0s", "s": 1, "r": "400ms"}}},
    "os-bass": {"about": f"Out of Step's bass (chirper-zero, 26 Nov): three pairs of sines, at G2 and its second and third harmonics, each pair {DELTA:g} Hz apart (one cycle a beat at {BPM}; ratio {R:.6f} for G2 ONLY: another note needs its own ratio). They start together, so struck on the off-beat they cancel on every beat: a pump with no compressor.",
                "play": {"mono": True, "vel_sens": 0.2},
                "synth": {"layers": [x for h, lv in ((1, -3), (2, -9), (3, -15)) for x in (f"sine phase=0 ratio={h} level={lv}dB", f"sine phase=0 ratio={h + DELTA / F0:.6f} level={lv - 1.5}dB")],
                          "amp": {"a": "4ms", "d": "0s", "s": 1, "r": "30ms"}}},
}


def song():
    doc = {
        "about": "Chirpers - Escapement, track 7 by chirper-zero: OUT OF STEP. Two clicks, the same sound and the same half-bar pattern; one is on the grid, the other slips a sixteenth ahead every eight bars and catches there (eight locks, then home), and later drifts back without stopping. Where they part they make a comb; the bass is two sines one cycle a beat apart that cancel on every beat. Generated by compose/chirpers11/src/chirpers11-t7.py.",
        "tempo": BPM,
        "ceiling": "-1dB",
        "loudness": -11.0,
        "seed": 1,
        "tail": "2s",
        "length": f"{TOTAL}b",
        "event_stable": True,
        "patches": PATCHES,
        "buses": {"room": {"fx": ["reverb kind=room decay=0.5s mix=1", "hp cutoff=400"]}},
        "master": {"fx": [{"type": "eq", "bands": ["hp cutoff=30"]}, {"type": "compressor", "threshold": "-18dB", "ratio": 2, "attack": "20ms", "release": "160ms", "makeup": "0dB"}]},
        "tracks": [
            {"name": "kick", "patch": "os-kick", "gain": "-8dB", "pan": 0.0, "notes": part("kick", KICK)},
            {"name": "a", "patch": "os-click", "gain": "-2dB", "pan": -0.35, "sends": {"room": "-16dB"}, "auto": {"open": {"points": open_lane()}}, "notes": a_notes()},
            {"name": "b", "patch": "os-click", "gain": "-2dB", "pan": 0.35, "sends": {"room": "-16dB"}, "auto": {"open": {"points": open_lane()}}, "notes": b_notes()},
            {"name": "bass", "patch": "os-bass", "gain": "-23dB", "pan": 0.0, "notes": part("bass", BASS)},
            {"name": "hat", "patch": "os-hat", "gain": "-1dB", "pan": 0.0, "sends": {"room": "-16dB"}, "notes": part("hat", HAT)},
            {"name": "clap", "patch": "os-clap", "gain": "-5dB", "pan": 0.0, "sends": {"room": "-10dB"}, "notes": part("clap", CLAP)},
        ],
    }
    if COMP_ON:
        doc["tracks"].append({"name": "c", "patch": "os-comp", "gain": "-6dB", "pan": 0.0, "sends": {"room": "-16dB"}, "notes": c_notes()})
        doc["about"] = doc["about"].replace(" Generated by", " From v2 a third click plays the pattern's three holes once the two are home: together they sound every sixteenth exactly once, and apart they collide. Generated by")
    else:
        del PATCHES["os-comp"]
    return doc


def dump(doc):
    lines = []
    for k, v in doc.items():
        if k == "tracks":
            lines.append("tracks:")
            lines += ["  - " + json.dumps(t) for t in v]
        else:
            lines.append(f"{k}: {json.dumps(v)}")
    return "\n".join(lines) + "\n"


def lock(k):
    """What they make when B is k sixteenths ahead: one half-bar, X A and B, a or b one of them, . neither; with C: c C alone, * B and C together."""
    b = {(p - k) % LOOP for p in PATTERN}
    def cell(s):
        if s in PATTERN:
            return "X" if s in b else "a"
        if COMP_ON:
            return "*" if s in b else "c"
        return "b" if s in b else "."
    return " ".join(cell(s) for s in range(LOOP))


if __name__ == "__main__":
    if os.environ.get("C11T7_SHOW"):
        sec = 60 / BPM * BEATS
        for name, b0, n, parts, phase in SECS:
            print(f"{name:10s} bars {b0:3d}-{b0 + n:3d}  {int(b0 * sec) // 60}:{b0 * sec % 60:04.1f}-{int((b0 + n) * sec) // 60}:{(b0 + n) * sec % 60:04.1f}  phase {phase}  " + ", ".join(p if w is None else p + " " + "+".join(f"{lo}-{hi}" for lo, hi in w) for p, w in parts.items()))
        for k in range(LOOP + 1):
            print(f"   B {k} ahead:  {lock(k)}")
        ms = 60 / BPM / 4 * 1000
        print("   the first slip (bars 24-26): the gap between A's stroke and B's, ms: " + " ".join(f"{(n['at'] / STEP - round(n['at'] / STEP + phi(n['at'] / STEP)) + 0) * -ms:.1f}" for n in b_notes() if 24 * BEATS <= n["at"] < 25.5 * BEATS))
        print(f"{BARS} bars, {TOTAL} beats, {BARS * sec:.1f} s; the bass: {F0} and {F0 * R:.4f} Hz")
    else:
        open(OUT, "w").write(dump(song()))
