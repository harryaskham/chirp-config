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

v3 (26 Nov): THE TUNE THE TWO MAKE (C11T7_TUNE=0 takes it out: v2). Wherever A and B strike on the same sixteenth
the two clicks are one louder click, and those doubles are a different figure at every lock: two of them at one
ahead, three at two, four at three ... A small glass pip now plays exactly the doubles, and each stroke of the
pattern has a note: G, B flat, D, F, A (the record's chord: Give or Take's G minor seventh with Least Common's ninth
on top). So every lock has its own tune, found in the two clicks and not written: G . . . . F . . at one ahead,
. Bb . D . . A . at two, G . . D . F A . at three ..., always a piece of the chord. AT HOME EVERY STROKE IS A
DOUBLE AND THE TUNE IS THE WHOLE CHORD: that is the second thing home is. In "slips" the first four locks are
heard bare, as before; from the fifth (where the drum stands back) each lock is heard bare for two bars and then
with its tune. In "drifts" B does not stop, so each tune is heard only for the two bars in which B passes its lock,
all seven backwards (7, 6, 5 ... 1: four of them for the first time), between bars where there is no tune at all.

v4 (26 Nov): THE PENDULUM (C11T7_PEND=0 takes it out: v3). A fourth kind of phase, and the smallest: under a
millisecond. While the two clicks are one click (the opening and the ending) A is given to the left ear alone and B
to the right, at the same loudness, and B swings ahead of A and behind it by PEND_MS (0.6 ms: the time sound takes
to cross a head), once there and back every two bars. A lead that small is not heard as two clicks, nor as a
rhythm: it is heard as a PLACE. The one click swings from ear to ear like the pendulum of the clock this record is
named after, and nothing is panned: each ear gets its own click at the same level all the way; only which is first
changes. (The two are turned down 3 dB while they stand apart, so that B joining adds no loudness, only a place.) THE DRUM HOLDS THE PENDULUM: it swings only where there is no bass drum. In "one click" it starts still
when B joins (bar 9), is at its full width a swing later, and stops dead on the bar the drum comes in. In "one
again" the drum's last stroke lets it go: it swings its full width at once and comes to rest, half as far every
three bars, and when it is still B stops. On ONE speaker there are no two ears to compare: the same lead is a comb, a hollow that opens
and closes in the click twice a swing (the phaser of the slips, a hundred times slower).

v5 (26 Nov): THE BASS HEARS THE LOCK (C11T7_ROOT=0 takes it out: v4). The bass has held one note, G, for the whole
record. But every lock has a first stroke that the two clicks share (the first note of its tune), and it is one of
two: the pattern's first stroke, G, or its second, B flat. In "drifts", where B does not stop and nothing says
where the locks are, the bass now does: as B passes each lock the bass plays the note the two are agreed on first.
After sixty-six bars on G it moves: B flat for four bars as B passes the seventh lock, G for eight (the sixth and
the fifth), B flat for four (the fourth), G for four (the third), B flat for four (the second), and G from there
home. Nobody wrote the line: G and B flat fall where the pattern's rotations put them, and the bass drum is away
for two of the changes (bars 121 to 128). Under B flat the tune's notes are a B flat major seventh (B flat, D, F, A); under G
they are G minor with its ninth: two chords out of one pattern. The B flat is a second bass, tuned like the first:
pairs of sines one cycle a beat apart from ITS notes, so it pumps on the beat as the G does.
ROOT_IN says in which kinds of phase the bass follows. It was tried in "slips" as well (the bass changing on the
bar B catches): on its own that scored a little under this, and both together made thirteen sections that kept
coming back and cost two points, so "slips" keeps its one note and the bass's first move is an event.
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
TUNE_ON = os.environ.get("C11T7_TUNE", "1") != "0"    # v3: the tune the two make
TUNE = {0: "G4", 1: "Bb4", 3: "D5", 5: "F5", 6: "A5"}  # a note for each stroke of the pattern: G minor ninth
assert set(TUNE) == set(PATTERN)
TUNE_FROM = 4                  # in "slips": the row from which a lock has its tune (the first four locks are heard bare)
TUNE_AFTER = 4                 # ... and the bar of the row from which it is heard (2 slipping, 2 bare)
TUNE_NEAR = 0.26               # sixteenths: a bar plays a lock's tune if B is this near the lock from its first step to its last
T = {"tune": None} if TUNE_ON else {}
ROOT_ON = os.environ.get("C11T7_ROOT", "1") != "0" and TUNE_ON   # v5: the bass hears the lock
F0B = 116.5409                 # B flat 2
ROOT_IN = tuple(os.environ.get("C11T7_ROOT_IN", "drift").split(","))   # the kinds of phase in which the bass follows the lock ("slips", "drift"); elsewhere it is G
PEND_ON = os.environ.get("C11T7_PEND", "1") != "0"    # v4: the pendulum
PEND_MS = 0.6                  # ms: how far B is ahead of A (and then behind) at the end of a swing; sound crosses a head in about this
PEND_BARS = 2                  # bars to swing there and back
PEND_GROW = 2                  # bars it takes to reach its full swing when it is set going ("up")
PEND_HALF = 3                  # bars in which the swing halves when it is left to come to rest ("rest")
PEND_APART = 1.0               # where the two clicks stand while it swings: A at -PEND_APART, B at +PEND_APART (an ear each)
PAN = 0.35                     # ... and everywhere else
PEND_GAIN = -3                 # dB: what both clicks are given while they stand apart: two clicks, an ear each, are then as loud as the one click was
P = (lambda lo, hi, kind: ("pend", lo, hi, kind)) if PEND_ON else (lambda lo, hi, kind: ("lock", 0))
ALL = None
# name, rows, {part: None, or the (from bar, to bar) stretches of the section it plays}, the phase: ("lock", k) | ("slips", k0) | ("drift", from, to) | ("pend", from bar, to bar, "up" or "rest"): locked at 0, swinging
SECTIONS = [
    ("one click", 3, {"a": ALL, "b": [(8, 24)], "kick": [(16, 24)]},                                                          P(8, 16, "up")),
    # the bass drum stands back while B slips to its last lock (8, which is home), and for the whole of the fifth row,
    # where the bass is heard pumping with no drum to pump it
    ("slips",     8, {"a": ALL, "b": ALL, "kick": [(0, 32), (40, 56), (58, 64)], "bass": [(16, 64)], "clap": [(40, 56), (58, 64)], "hat": [(32, 56), (58, 64)], **({"tune": [(r * ROW + TUNE_AFTER, (r + 1) * ROW) for r in range(TUNE_FROM, 8)]} if TUNE_ON else {})}, ("slips", 0)),
    ("home",      2, {"a": ALL, "b": ALL, "kick": ALL, "bass": ALL, "clap": ALL, "hat": ALL, **C, **T},                       ("lock", 8)),
    ("drifts",    4, {"a": ALL, "b": ALL, "kick": [(0, 16), (24, 32)], "bass": ALL, "clap": [(0, 16), (24, 32)], "hat": ALL, **C, **T},  ("drift", 8, 0)),
    ("one again", 3, {"a": ALL, "b": [(0, 20)], "kick": [(0, 8)], "bass": [(0, 16)], "clap": [(0, 8)], "hat": [(0, 8)], **({"c": [(0, 16)]} if COMP_ON else {}), **({"tune": [(0, 16)]} if TUNE_ON else {})}, P(8, 20, "rest")),
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


def swing(x, kind):
    """The pendulum, x bars after it starts: B's lead as a share of PEND_MS (+ ahead: the right ear first)."""
    if kind == "up":       # set going from rest: wider for PEND_GROW bars, then steady
        return min(1.0, x / PEND_GROW) * math.sin(2 * math.pi * x / PEND_BARS)
    return -0.5 ** (x / PEND_HALF) * math.sin(2 * math.pi * x / PEND_BARS)   # "rest": B arrives going backwards, overshoots and dies away


def lead_ms(t):
    """How many ms B is ahead of A at time t (sixteenths) because of the pendulum; 0 where there is none."""
    bar = t / BAR
    for name, b0, n, parts, phase in SECS:
        if b0 <= bar < b0 + n and phase[0] == "pend" and phase[1] <= bar - b0 < phase[2]:
            return PEND_MS * swing(bar - b0 - phase[1], phase[3])
    return 0.0


def phi(t, pend=True):
    """B's phase at time t (sixteenths from the start): how many sixteenths it is ahead of A."""
    bar = t / BAR
    for name, b0, n, parts, phase in SECS:
        if b0 <= bar < b0 + n or (name == SECS[-1][0] and bar >= b0):
            u = bar - b0
            if phase[0] == "pend":
                return lead_ms(t) / (60000 / BPM / 4) if pend else 0.0
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
        v = round(phi(min(h * BAR / 2, BARS * BAR - 0.001), pend=False) / LOOP, 4)
        if v != last or h == BARS * 2:
            if last is not None and pts and pts[-1][0] != f"{(h - 1) * 2:g}b":
                pts.append([f"{(h - 1) * 2:g}b", last])
            pts.append([f"{h * 2:g}b", v])
        last = v
    return pts


def apart_lane():
    """Where the two clicks stand: 0 at their usual PAN, 1 an ear each (while the pendulum swings). They part and
    come back in the last sixteenth of a bar, which is one of the pattern's holes, with B exactly on A."""
    pts = [["0b", 0]]
    for name, b0, n, parts, phase in SECS:
        if phase[0] == "pend":
            lo, hi = (b0 + phase[1]) * BEATS, (b0 + phase[2]) * BEATS
            pts += ([[f"{lo - 0.125:g}b", 0]] if lo > 0 else []) + [[f"{lo:g}b", 1], [f"{hi - 0.125:g}b", 1], [f"{hi:g}b", 0]]
    return pts + [[f"{TOTAL:g}b", 0]]


def click_pan(side):
    return {"value": side * PAN, "mod": [{"src": "auto.apart", "amount": round(side * (PEND_APART - PAN), 4)}]} if PEND_ON else side * PAN


def click_fx():
    return {"fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.apart", "amount": PEND_GAIN}]}}]} if PEND_ON else {}


def click_auto():
    return {"open": {"points": open_lane()}, **({"apart": {"points": apart_lane()}} if PEND_ON else {})}


def a_notes():
    return [note(s * STEP, NOTE, 0.5 * STEP, VEL(s)) for s in range(BARS * BAR) if s % LOOP in PATTERN and plays("a", s // BAR)]


def c_notes():
    """The complement: C strikes the pattern's holes, on the grid."""
    return [note(s * STEP, "G5", 0.25 * STEP, 0.85 if s % LOOP == COMP[0] else 0.72) for s in range(BARS * BAR) if s % LOOP in COMP and plays("c", s // BAR)]


def doubles(k):
    """The sixteenths of the half-bar on which A and B strike together when B is k ahead."""
    return tuple(s for s in PATTERN if (s + k) % LOOP in PATTERN)


def tune_lock(bar):
    """The lock whose tune a bar plays (0 to LOOP), or None: B must be within TUNE_NEAR of it for the whole bar."""
    if not plays("tune", bar):
        return None
    p0, p1 = phi(bar * BAR), phi((bar + 1) * BAR - 0.001)
    k = round((p0 + p1) / 2)
    return k if abs(p0 - k) <= TUNE_NEAR and abs(p1 - k) <= TUNE_NEAR else None


def tune_notes():
    out = []
    for bar in range(BARS):
        k = tune_lock(bar)
        if k is not None:
            d = doubles(k)
            out += [note((bar * BAR + half + s) * STEP, TUNE[s], 1 * STEP, 0.85 if s == d[0] else 0.72) for half in (0, LOOP) for s in d]
    return out


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


def bass_lock(bar):
    """The lock the bass hears in a bar: the one B is in when the bass strikes (in "drifts", the one B is nearest)."""
    t = bar * BAR + 2
    p = phi(t, pend=False) if PEND_ON else phi(t)
    kind = next(ph[0] for name, b0, n, parts, ph in SECS if b0 <= bar < b0 + n)
    return int(round(p)) if kind == "drift" else int(math.floor(p + 1e-9))


def bass_note(bar):
    """The first stroke the two clicks share at that lock, two octaves under its note in the tune: G or B flat."""
    kind = next(ph[0] for name, b0, n, parts, ph in SECS if b0 <= bar < b0 + n)
    return TUNE[doubles(bass_lock(bar))[0]].replace("4", "2") if ROOT_ON and kind in ROOT_IN else "G2"


BASS_G = lambda bar: BASS(bar) if bass_note(bar) == "G2" else []
BASS_B = lambda bar: [(2, "Bb2", 15.6, 0.9)] if bass_note(bar) == "Bb2" else []

R = 1 + DELTA / F0             # the second tone of each pair, as a ratio of the note
PATCHES = {
    "os-click": {"about": "Out of Step's click (chirper-zero, 26 Nov): five cycles of a saw on G3 dying in 22 ms, lifted 9 dB round 9 kHz, started at the same point of its wave every time, through a low-pass that both clicks share (it opens with the phase): nothing in it is random, so two of them struck together are one click, and two struck a millisecond apart are a comb. (The machine's rim was tried first: two rims differ by 22 dB under one, and its note stood 16 to 25 dB over the album's envelope.)",
                 "play": {"vel_sens": 0.5},
                 "synth": {"layers": ["saw phase=0"], "filters": ["hp cutoff=500", "peak cutoff=9000 q=0.7 gain=9dB", {"kind": "lp", "cutoff": {"value": DULL, "mod": [{"src": "auto.open", "amount": OCTAVES}]}, "q": 0.7}], "amp": {"a": "0.1ms", "d": "22ms", "s": 0, "r": "10ms", "curve": 3}}},
    "os-comp": {"about": "Out of Step's third click (chirper-zero, 26 Nov, v2): the complement's. Two cycles of a saw on G5 dying in 12 ms, above 3 kHz, lifted 8 dB round 10 kHz: small and bright, so that it is heard as the holes being filled and not as a third pattern.",
                "play": {"vel_sens": 0.5},
                "synth": {"layers": ["saw phase=0"], "filters": ["hp cutoff=3000", "peak cutoff=10000 q=0.7 gain=8dB"], "amp": {"a": "0.1ms", "d": "12ms", "s": 0, "r": "8ms", "curve": 3}}},
    "os-tune": {"about": "Out of Step's pip (chirper-zero, 26 Nov, v3): a small glass tone (a sine with its twelfth, 140 ms), which plays only the sixteenths on which the two clicks strike together, a note for each stroke of the pattern.",
                "play": {"vel_sens": 0.6},
                "synth": {"layers": ["sine", "sine ratio=3 level=-14dB"], "amp": {"a": "0.3ms", "d": "140ms", "s": 0, "r": "40ms", "curve": 3}}},
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
    "os-bass-b": {"about": f"Out of Step's second bass (chirper-zero, 26 Nov, v5): the same three pairs of sines built on B flat 2 ({F0B} Hz), each pair {DELTA:g} Hz apart (ratio {1 + DELTA / F0B:.6f} for B flat 2 only), so it pumps on the beat as the G does. It sounds at the locks whose first shared stroke is the pattern's second.",
                  "play": {"mono": True, "vel_sens": 0.2},
                  "synth": {"layers": [x for h, lv in ((1, -3), (2, -9), (3, -15)) for x in (f"sine phase=0 ratio={h} level={lv}dB", f"sine phase=0 ratio={h + DELTA / F0B:.6f} level={lv - 1.5}dB")],
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
            {"name": "a", "patch": "os-click", "gain": "-2dB", "pan": click_pan(-1), "sends": {"room": "-16dB"}, **click_fx(), "auto": click_auto(), "notes": a_notes()},
            {"name": "b", "patch": "os-click", "gain": "-2dB", "pan": click_pan(1), "sends": {"room": "-16dB"}, **click_fx(), "auto": click_auto(), "notes": b_notes()},
            {"name": "bass", "patch": "os-bass", "gain": "-23dB", "pan": 0.0, "notes": part("bass", BASS_G if ROOT_ON else BASS)},
            {"name": "hat", "patch": "os-hat", "gain": "-1dB", "pan": 0.0, "sends": {"room": "-16dB"}, "notes": part("hat", HAT)},
            {"name": "clap", "patch": "os-clap", "gain": "-5dB", "pan": 0.0, "sends": {"room": "-10dB"}, "notes": part("clap", CLAP)},
        ],
    }
    if ROOT_ON:
        i = next(k for k, t in enumerate(doc["tracks"]) if t["name"] == "bass")
        doc["tracks"].insert(i + 1, {"name": "bassb", "patch": "os-bass-b", "gain": "-23dB", "pan": 0.0, "notes": part("bass", BASS_B)})
        doc["about"] = doc["about"].replace(" Generated by", " From v5, while B drifts home, the bass plays the first stroke the two clicks share at each lock B passes, G or B flat: it moves for the first time, and says where the locks are. Generated by")
    else:
        del PATCHES["os-bass-b"]
    if PEND_ON:
        doc["about"] = doc["about"].replace(" Generated by", f" From v4, while the two are one click (the opening and the ending) they are given an ear each and one swings {PEND_MS:g} ms ahead of the other and behind it: the click is heard to swing from ear to ear, with nothing panned. Generated by")
    if COMP_ON:
        doc["tracks"].append({"name": "c", "patch": "os-comp", "gain": "-6dB", "pan": 0.0, "sends": {"room": "-16dB"}, "notes": c_notes()})
        doc["about"] = doc["about"].replace(" Generated by", " From v2 a third click plays the pattern's three holes once the two are home: together they sound every sixteenth exactly once, and apart they collide. Generated by")
    else:
        del PATCHES["os-comp"]
    if TUNE_ON:
        doc["tracks"].append({"name": "tune", "patch": "os-tune", "gain": "-18dB", "pan": 0.0, "sends": {"room": "-10dB"}, "notes": tune_notes()})
        doc["about"] = doc["about"].replace(" Generated by", " From v3 a small pip plays the sixteenths on which the two clicks strike together, a note for each stroke of the pattern (G, B flat, D, F, A): every lock has its own tune, and home is the whole chord. Generated by")
    else:
        del PATCHES["os-tune"]
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
            print(f"   B {k} ahead:  {lock(k)}" + (f"   the tune: {' '.join(TUNE[s] if s in doubles(k) else '.' for s in range(LOOP))}" if TUNE_ON else ""))
        if TUNE_ON:
            runs, last = [], None
            for bar in range(BARS):
                k = tune_lock(bar)
                if k != last or not runs:
                    runs.append([bar, bar + 1, k])
                else:
                    runs[-1][1] = bar + 1
                last = k
            print("   the tune by bars: " + " ".join(f"{lo}-{hi}:{k}" for lo, hi, k in runs if k is not None))
        if ROOT_ON:
            runs = []
            for bar in range(BARS):
                if plays("bass", bar):
                    k, p = bass_lock(bar), bass_note(bar)
                    if runs and runs[-1][1] == bar and runs[-1][3] == p:
                        runs[-1][1] = bar + 1; runs[-1][2].append(k)
                    else:
                        runs.append([bar, bar + 1, [k], p])
            print("   the bass by bars (the locks it hears): " + " ".join(f"{lo}-{hi}:{p}({','.join(str(q) for q in sorted(set(ks), key=ks.index))})" for lo, hi, ks, p in runs))
        if PEND_ON:
            for name, b0, n, parts, phase in SECS:
                if phase[0] == "pend":
                    print(f"   the pendulum in \"{name}\" (bars {b0 + phase[1]}-{b0 + phase[2]}, {phase[3]}): B's lead at each quarter of a bar, ms (+ the right ear first): " + " ".join(f"{lead_ms((b0 + phase[1]) * BAR + q * 4):+.2f}" for q in range(0, (phase[2] - phase[1]) * 4 + 1)))
        ms = 60 / BPM / 4 * 1000
        print("   the first slip (bars 24-26): the gap between A's stroke and B's, ms: " + " ".join(f"{(n['at'] / STEP - round(n['at'] / STEP + phi(n['at'] / STEP)) + 0) * -ms:.1f}" for n in b_notes() if 24 * BEATS <= n["at"] < 25.5 * BEATS))
        print(f"{BARS} bars, {TOTAL} beats, {BARS * sec:.1f} s; the bass: {F0} and {F0 * R:.4f} Hz")
    else:
        open(OUT, "w").write(dump(song()))
