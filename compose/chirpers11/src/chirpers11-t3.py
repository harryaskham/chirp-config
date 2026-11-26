#!/usr/bin/env python3
"""Escapement (Chirpers 11), track 3 (chirper-zero): STANDING ROOM. The slot's word is SPACE.

THE RHYTHM IS THE ROOM. One click a bar, a wooden tock every other bar, a bass drum on the four: that is all that is
played up top. Everything else you hear the click do is the room: it stands between two walls, and each wall sends it
back. A wall is a distance, and here a distance is a number of sixteenths there and back. With the left wall 3 away
and the right wall 4, the click comes back from the left after 3, from the right after 4, from both after 7, from the
left after 10, the right after 11, both after 14 ... each time softer and duller (the walls take 3 dB and the top).
So a room is a rhythm, and its length is the two walls added: 3 + 4 is a room in seven, 2 + 3 a room in five,
5 + 7 a room in twelve, and none of those divides the bar: the echoes that outlast the bar come back BETWEEN the
next click's echoes, and the bar fills up (in the corridor twelve of its sixteen steps sound). ONE ROOM FITS:
3 + 5 is eight, half the bar, and in it the old echoes fall exactly on the new ones and stand: the click on 2
becomes 2, 5, 7, 10, 13, 15, the three-three-two, and nothing else. Standing room.

THE TOCK KEEPS THE ROOM'S TIME, NOT THE BAR'S. In a room it strikes once for every two crossings (twice the room's
length: every 14 sixteenths in the corridor, 10 in the stairwell, 24 in the hangar), so each stroke lands as its
own echo comes home from both walls, and it walks through the bar: the corridor's bar comes round every 7 bars,
the stairwell's every 5, the hangar's every 3. In standing room twice the room is the bar, and it stops walking.

The click is in ALL the rooms all the time (each room is two buses that hear the click, the tock and each other,
bd-705c25's returns); the song only opens and shuts their DOORS (a fader after each wall), and leaves a door a
little open behind it as it walks on. Nothing but the rooms changes the click's rhythm from the first bar to the last.

THE FORM IS ARITHMETIC: a row is ROW bars; SECTIONS lists, for each section, its rows, its parts, the room whose door
is open, how wide the walls stand apart and how much of the far air is heard. Every lane point comes from those.

v1 is the SKELETON (26 Nov): the rooms standing and the walk through them, with few sounds.

v2 (26 Nov): THE CLICK WALKS ACROSS EACH ROOM (C11T3_WALK=0 stands it still, as in v1). A room's length is its two
walls added, and that does not change when the click moves: only how the length is shared. In the corridor (seven)
the click starts two from the left wall and five from the right, and every row takes a step across: 2 + 5, 3 + 4,
4 + 3, 5 + 2. Every step is a new rhythm (the returns come at a, b, a + b, ...) on the same seven, so the tock,
which keeps the room's time, never notices, and the first echo crosses from the left ear to the right as the click
does. The stairwell is crossed the other way (4 + 1, 3 + 2, 2 + 3); in the hangar the click reaches the middle
(6 + 6: both walls answer at once). IN STANDING ROOM IT STANDS: 3 + 5, forty bars, not a step. Each place is its
own pair of walls with its own door, so in the bar or two of a step both places are heard: the old echoes dying
behind, the new ones building.

v3 (26 Nov): THE BASS LEARNS THE ROOM, AND TAKES IT OUT OF THE DOOR (C11T3_LEARN=0 writes v2). Until now nothing
that is PLAYED has had the room's rhythm: the bass has kept to the off-beats while the walls said three-three-two
over it. From the second row of standing room the bass plays what the room says, a stroke where the click is and
one wherever a wall sends it back in the same bar (steps 2, 5, 7, 10, 13, 15), and each wall has a note: D for the
click and for both walls together, F for the left wall, C for the right (`learnt()`, from the same `echoes()` that
prints the rooms). Then the walk goes out of the door: the walls are gone, the click is one dry click a bar again,
and THE BASS STILL PLAYS THE ROOM, walking away (18 dB down over eight bars), until the drum stops. The room is in
the hands now. The last eight bars are the click alone, as they always were. (CARRY 12, the bass four bars on after
the drum, was tried: the scorer then reads the whole song as five sections with 5.6 dB between them, 90.3.)
And the dry click is heard WHERE IT STANDS: its pan is its place between the walls ((a - b) / (a + b), times PAN),
so as it steps across a room the click itself moves with its first echo, and at 6 + 6 in the hangar it is dead centre.

v4 (26 Nov): THE WALLS CLOSE IN (C11T3_PIPES=0 takes the section out: v3). A room is a rhythm because its echoes
are far enough apart to count. Bring the walls together and they are not: the echoes run into one another and the
room SINGS, at one cycle for every crossing. A new section, "the pipes", between the stairwell and the hangar:
eight rooms too small to count, the click in the middle of each, a bar in each, every one smaller than the
last: 13.6 ms from the click to a wall and back, then 11.5, 10.2, 9.1, 8.6, 7.6, 6.8, 6.1. The same click, once a
bar, now plays D, F, G, A, B flat, C, D, E, a scale going up as the walls come in (the tock rings them too; the
bass stands back: for these eight bars the rooms are the only thing with a note). These
walls are hard (they give back all but a decibel, so a pipe rings for 0.7 s) where the big rooms' walls take three.
6 ms is as close as this engine's walls will stand, so E is the top, and it is the ninth of the chord the hangar
opens with: the walls fly apart, from six milliseconds to twelve sixteenths, on the note the pipes left hanging.
"""
import json
import math
import os

OUT = os.environ.get("C11T3_OUT", os.path.join(os.path.dirname(__file__), "..", "..", "..", "songs", "chirpers11-t3.yaml"))
BPM = 126
BEATS = 4
ROW = 8
STEP = 0.25

# a room: the left wall and the right wall, in sixteenths there and back
ROOMS = {"corridor": (3, 4), "stairwell": (2, 3), "hangar": (5, 7), "standing": (3, 5)}
# where the click stands in each room, a row or more at each place (left wall, right wall): the room's length stays
WALK = {"corridor": [(2, 5), (3, 4), (4, 3), (5, 2)], "stairwell": [(4, 1), (3, 2), (2, 3)], "hangar": [(4, 8), (5, 7), (6, 6), (7, 5)], "standing": [(3, 5)]}
if os.environ.get("C11T3_WALK", "1") == "0":
    WALK = {room: [ab] for room, ab in ROOMS.items()}
assert all(a + b == sum(ROOMS[room]) for room, w in WALK.items() for a, b in w)
LEARN = os.environ.get("C11T3_LEARN", "1") != "0"   # v3: the bass learns the room; the dry click is where it stands
LEARN_ROOM = "standing"        # the room the bass learns
LEARN_AFTER = 1                # rows of that room it listens for first
WALL_NOTE = {"click": "D2", "both": "D2", "left": "F2", "right": "C2"}   # the bass's note for the click and for each wall's answer
CARRY = 8                      # bars of "the door" the bass carries the room on for (the drum stops at 8 too)
AWAY = -18                     # dB the bass has fallen by then: it walks away with the room in its hands
PAN = 0.7                      # the dry click's pan when it stands AT a wall (it never does: 4 + 1 is 0.6 of the way)
PIPES_ON = os.environ.get("C11T3_PIPES", "1") != "0"   # v4: the walls close in
PIPES = ("D2", "F2", "G2", "A2", "Bb2", "C3", "D3", "E3")   # the note each pipe sings: one cycle for every crossing (a wall 1000 / Hz ms away)
PIPE_BARS = 1                  # bars the click stands in each
PIPE_RING = 0.7                # seconds a pipe rings (to -60 dB): its walls give back 60 * (the crossing in seconds) / PIPE_RING dB less each time
PIPE_LEVEL = -11               # dB: a pipe's door when it is open
PIPE_TRIM = 0.035              # ms: what a wall's own filter adds to a crossing (measured: the pipes sang 4 to 11 cents flat without it)
PIPE_DAMP = ["hp cutoff=40", "lp cutoff=4500"]   # what a pipe's wall takes
STEP_OPEN = 1                  # bars the door of the next place takes to open as the click steps
STEP_SHUT = 2                  # bars the door of the place behind takes to shut
WALL = "-3dB"                  # what a wall gives back
FIRST = {"click": "-4dB", "tock": "-6dB"}   # how loud each part reaches a wall
ABSORB = ["hp cutoff=250", "lp cutoff=9000"]

# name, rows, parts, the room whose door is open (None: outside), the walls' width, the far air (dB; None: none)
SECTIONS = [
    ("outside",       2, {"click", "kick", "tock"},                          None,        0.0, None),
    ("the corridor",  4, {"click", "kick", "tock", "bass"},                  "corridor",  0.8, -22),
    ("the stairwell", 3, {"click", "kick", "tock", "bass"},                  "stairwell", 0.5, -26),
] + ([("the pipes",    len(PIPES) * PIPE_BARS // ROW, {"click", "kick", "tock"}, None,              0.0, None)] if PIPES_ON else []) + [
    ("the hangar",    4, {"click", "kick", "tock", "bass", "chord"},         "hangar",    1.2, -8),
    ("standing room", 5, {"click", "kick", "tock", "bass", "chord", "clap"}, "standing",  1.0, -16),
    ("the door",      2, {"click", "kick", "tock"} | ({"bass"} if LEARN else set()), None,   0.0, None),
]
OPEN = 2                       # bars a door takes to open (from AJAR)
SHUT = 4                       # bars it takes to shut behind the walk
AJAR = -24                     # dB: where an opening door starts and a shutting one ends before it is closed
CLOSED = -90
ENTER = {"outside": [("kick", 4), ("tock", 8)], "the corridor": [("bass", 2 * ROW)], "the hangar": [("kick", ROW), ("bass", ROW)]}   # the bar of the section from which a part is there
LEAVE = {"the door": [("tock", 8), ("kick", 8)]}                                                                                      # ... and from which it is gone
if LEARN:
    LEAVE["the door"].append(("bass", CARRY))


def starts():
    out, b = [], 0
    for name, rows, parts, room, width, air in SECTIONS:
        out.append((name, b, rows * ROW, parts, room, width, air)); b += rows * ROW
    return out, b


SECS, BARS = starts()
TOTAL = BARS * BEATS


def section_of(bar):
    for s in SECS:
        if s[1] <= bar < s[1] + s[2]:
            return s
    return SECS[-1]


def plays(part, bar):
    name, b0, n, parts, room, width, air = section_of(bar)
    for p, there in ENTER.get(name, []):
        if p == part and bar < b0 + there:
            return False
    for p, gone in LEAVE.get(name, []):
        if p == part and bar >= b0 + gone:
            return False
    return part in parts


def note(at, pitch, length, vel):
    return {"at": round(at, 4), "len": round(length, 4), "pitch": pitch, "vel": round(vel, 3)}


def part(name, steps):
    out = []
    for bar in range(BARS):
        if plays(name, bar):
            out += [note(bar * BEATS + s * STEP, p, n * STEP, v) for s, p, n, v in steps(bar)]
    return out


def pt(bar, v):
    return [f"{bar * BEATS:g}b", round(v, 3)]


def places():
    """Every place the click stands: (bus name, left wall, right wall, first bar, last bar, bars to open, bars to shut)."""
    out = []
    for name, b0, n, parts, room, width, air in SECS:
        if room is None:
            continue
        walk = WALK[room]
        each = n / len(walk)
        for i, (a, b) in enumerate(walk):
            out.append((room if len(walk) == 1 else f"{room}{a}{b}", a, b, b0 + i * each, b0 + (i + 1) * each, OPEN if i == 0 else STEP_OPEN, SHUT if i == len(walk) - 1 else STEP_SHUT))
    assert len({p[0] for p in out}) == len(out)
    return out


def door_lane(b0, b1, opn, shut):
    """dB on a place's door: open while the click stands there, opening as it comes, shutting behind it."""
    pts = [pt(0, CLOSED), pt(b0 - 0.01, CLOSED), pt(b0, AJAR), pt(b0 + opn, 0), pt(b1, 0), pt(b1 + shut, AJAR), pt(b1 + shut + 0.01, CLOSED), pt(BARS, CLOSED)]
    return [p for i, p in enumerate(pts) if i == 0 or p != pts[i - 1]]


def step_lane(index, default, glide=2):
    """A lane that holds each section's value and glides to the next over the section's first `glide` bars."""
    pts, last = [], None
    for s in SECS:
        v = s[index] if s[index] is not None else default
        if last is None:
            pts.append(pt(0, v))
        elif v != last:
            pts += [pt(s[1], last), pt(s[1] + glide, v)]
        last = v
    pts.append(pt(BARS, last))
    return pts


def breath_lane(depth=0.2, bars=8):
    """The dub delay's feedback, breathing once in `bars` bars."""
    return [pt(b, depth * math.sin(2 * math.pi * b / bars)) for b in range(0, BARS + 1)]


def hz(p):
    semi = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[p[0]] + (-1 if "b" in p[1:] else 1 if "#" in p else 0) + 12 * (int(p[-1]) + 1)
    return 440.0 * 2 ** ((semi - 69) / 12)


def pipes():
    """Every pipe: (bus name, the note, ms from the click to either wall and back, first bar, last bar)."""
    b0 = next((s[1] for s in SECS if s[0] == "the pipes"), None)
    return [] if b0 is None else [(f"pipe{i}", p, 1000 / hz(p), b0 + i * PIPE_BARS, b0 + (i + 1) * PIPE_BARS) for i, p in enumerate(PIPES)]


def pipe_buses():
    """A pipe is two hard walls the same distance from the click, too near to count (the engine wants 6 ms or more)."""
    out = {}
    for name, p, ms, b0, b1 in pipes():
        assert ms - PIPE_TRIM >= 6.0, (p, ms)
        back = f"{-60 * ms / 1000 / PIPE_RING:.2f}dB"
        for side, other in (("l", "r"), ("r", "l")):
            out[f"{name}-{side}"] = {"fx": [{"type": "eq", "bands": PIPE_DAMP}],
                                     "returns": [{"from": part, "gain": g, "time": f"{ms - PIPE_TRIM:.3f}ms"} for part, g in FIRST.items()] + [{"from": f"{name}-{other}", "gain": back, "time": f"{ms - PIPE_TRIM:.3f}ms"}],
                                     "out": f"{name}-door"}
        out[f"{name}-door"] = {"pan": 0.0, "fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.door", "amount": 1}]}}],
                               "auto": {"door": {"points": [pt(0, CLOSED), pt(b0 - 0.02, CLOSED), pt(b0, PIPE_LEVEL), pt(b1 - 0.15, PIPE_LEVEL), pt(b1, CLOSED), pt(BARS, CLOSED)]}}}
    return out


def buses():
    out = {}
    for room, a, b, b0, b1, opn, shut in places():
        door = {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.door", "amount": 1}]}}
        lane = {"door": {"points": door_lane(b0, b1, opn, shut)}}
        for side, own, other, pan in (("l", a, "r", -0.85), ("r", b, "l", 0.85)):
            out[f"{room}-{side}"] = {"fx": [{"type": "eq", "bands": ABSORB}],
                                     "returns": [{"from": p, "gain": g, "time": f"{own}/16"} for p, g in FIRST.items()] + [{"from": f"{room}-{other}", "gain": WALL, "time": f"{own}/16"}],
                                     "out": f"{room}-door-{side}"}
            out[f"{room}-door-{side}"] = {"pan": pan, "fx": [door], "auto": lane, "out": "walls"}
    out.update(pipe_buses())
    out["walls"] = {"fx": [{"type": "width", "width": {"value": 0.0, "mod": [{"src": "auto.apart", "amount": 1}]}}], "auto": {"apart": {"points": step_lane(5, 0.0)}}}
    out["air"] = {"fx": ["reverb kind=hall decay=5.5s size=1 mix=1 predelay=40ms", "lp cutoff=6000", "hp cutoff=300",
                         {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.far", "amount": 1}]}}],
                  "returns": [{"from": "click", "gain": "0dB", "time": "6ms"}, {"from": "tock", "gain": "-2dB", "time": "6ms"}],
                  "auto": {"far": {"points": step_lane(6, CLOSED, glide=4)}}}
    out["dub"] = {"fx": [{"type": "delay", "time": "3/16", "feedback": {"value": 0.5, "mod": [{"src": "auto.breath", "amount": 1}]}, "mix": 1, "tone": 2000}, "hp cutoff=300",
                         "reverb kind=hall decay=3s mix=0.3"], "auto": {"breath": {"points": breath_lane()}}}
    return out


KICK = lambda bar: [(s, "A1", 1, 0.95 if s == 0 else 0.9) for s in (0, 4, 8, 12)]
CLICK = lambda bar: [(2, "A5", 1, 0.9)]             # CLICK_STEP
TOCK = lambda bar: [(11, "D5" if bar % 4 == 1 else "F5", 1, 0.8)] if bar % 2 else []   # outside: every other bar
TOCK_STEP = 11                 # in a room: from this step of the section's first bar, every 2 * (a + b) sixteenths


def tock_notes():
    out = []
    for name, b0, n, parts, room, width, air in SECS:
        if "tock" not in parts:
            continue
        if room is None:
            for bar in range(b0, b0 + n):
                if plays("tock", bar):
                    out += [note(bar * BEATS + s * STEP, p, ln * STEP, v) for s, p, ln, v in TOCK(bar)]
            continue
        a, b = ROOMS[room]
        k, at = 0, b0 * 16 + TOCK_STEP
        while at < (b0 + n) * 16:
            out.append(note(at * STEP, "D5" if k % 4 == 3 else "F5", 1 * STEP, 0.8)); k += 1; at += 2 * (a + b)
    return out
BASS = lambda bar: [(2, "D2", 1.5, 0.9), (6, "D2", 1.5, 0.8), (10, "D2", 1.5, 0.9), (14, ("C2", "D2", "F2", "A1")[(bar // 2) % 4] if bar % 2 else "D2", 1.5, 0.8)]
CLAP = lambda bar: [(4, "C4", 1, 0.8), (12, "C4", 1, 0.86)]
CLICK_STEP = 2


def learnt():
    """The bass's bar once it has learnt the room: the click's step, then every step of the same bar on which a wall sends it back."""
    a, b = WALK[LEARN_ROOM][0]
    out = [(CLICK_STEP, WALL_NOTE["click"], 1.5, 0.92)]
    for t, side in echoes(a, b):
        if CLICK_STEP + t < 16:
            out.append((CLICK_STEP + t, WALL_NOTE[side], 1.5, round((0.88 if side == "both" else 0.8) * (1.0 if t <= a + b else 0.9), 3)))
    return out


def has_learnt(bar):
    name, b0, n, parts, room, width, air = section_of(bar)
    if room == LEARN_ROOM:
        return bar >= b0 + LEARN_AFTER * ROW
    return bar >= b0 and room is None and any(s[4] == LEARN_ROOM and s[1] < b0 for s in SECS)


def bass_bar(bar):
    return learnt() if LEARN and has_learnt(bar) else BASS(bar)


def away_lane():
    """dB on the bass: 0 until the walk is out of the door, then falling to AWAY over the CARRY bars it carries the room."""
    b0 = next(s[1] for s in SECS if s[4] is None and any(t[4] == LEARN_ROOM and t[1] < s[1] for t in SECS))
    return [pt(0, 0), pt(b0, 0), pt(b0 + CARRY, AWAY), pt(BARS, AWAY)]


def stand_lane():
    """Where the dry click stands between the walls, -1 at the left wall, +1 at the right, 0 outside: (a - b) / (a + b)."""
    ev = []
    for name, b0, n, parts, room, width, air in SECS:
        if room is None:
            ev.append((b0, 0.0, OPEN))
    ev += [(b0, (a - b) / (a + b), opn) for room, a, b, b0, b1, opn, shut in places()]
    ev.sort()
    pts, last = [pt(0, ev[0][1])], ev[0][1]
    for b0, v, glide in ev[1:]:
        if v != last:
            pts += [pt(b0, last), pt(b0 + glide, v)]
        last = v
    pts.append(pt(BARS, last))
    return pts
CHORDS = [("D3", "F3", "A3", "C4", "E4"), ("Bb2", "D3", "F3", "A3", "C4")]
CHORD = lambda bar: [(6, p, 2, 0.85) for p in CHORDS[(bar // 8) % 2]] if bar % 4 == 0 else []

PATCHES = {
    "sr-kick": {"about": "Standing Room's bass drum (chirper-zero, 26 Nov): the engine's machine kick, short and dry, on A1. It is not in any room.",
                "play": {"vel_sens": 0.3},
                "synth": {"layers": [{"type": "machine", "machine": {"part": "kick", "decay": "260ms", "click": 0.6, "drive": 0.35, "punch": 22, "punch_time": "32ms"}}],
                          "filters": ["hp cutoff=28"], "amp": {"a": "0.1ms", "d": "0s", "s": 1, "r": "1s"}}},
    "sr-click": {"about": "Standing Room's click (chirper-zero, 26 Nov): the machine's rim with a breath of white noise, 40 ms, above 500 Hz and lifted 6 dB round 11 kHz: bright enough that a wall can take its top away.",
                 "play": {"vel_sens": 0.4},
                 "synth": {"layers": [{"type": "machine", "machine": {"part": "rim", "decay": "45ms"}}, "white level=-3dB"], "filters": ["hp cutoff=500", "peak cutoff=11000 q=0.7 gain=6dB"],
                           "amp": {"a": "0.1ms", "d": "40ms", "s": 0, "r": "20ms", "curve": 4}}},
    "sr-tock": {"about": "Standing Room's tock (chirper-zero, 26 Nov): a wooden bar on the modal layer (after Common Measure's clave), an octave or so under the click.",
                "play": {"vel_sens": 0.5},
                "synth": {"layers": [{"type": "modal", "modes": "glock", "bright": 0.9, "damp": 0.25, "decay": "150ms", "strike": 0.5, "tilt": 0.0}],
                          "amp": {"a": "0.2ms", "d": "240ms", "s": 0, "r": "40ms"}}},
    "sr-clap": {"about": "Standing Room's clap (chirper-zero, 26 Nov): the machine's clap, three bursts, short, dry.",
                "play": {"vel_sens": 0.4},
                "synth": {"layers": [{"type": "machine", "machine": {"part": "clap", "bursts": 3, "decay": "140ms"}}], "amp": {"a": "0.1ms", "d": "0s", "s": 1, "r": "400ms"}}},
    "sr-chord": {"about": "Standing Room's dub chord (chirper-zero, 26 Nov): three saws and a square through a short filter envelope, dry; its space is the bus `dub`, a dotted-eighth echo whose feedback breathes.",
                 "synth": {"layers": ["saw unison=3 detune=0.15 spread=0.6", "square level=-8dB"], "env": {"f": {"a": "1ms", "d": "220ms", "s": 0.08, "r": "100ms"}},
                           "filters": [{"kind": "lp", "cutoff": {"value": 600, "mod": [{"src": "env.f", "amount": 2.4}, {"src": "vel", "amount": 1}]}, "q": 1.6}],
                           "amp": {"a": "1ms", "d": "300ms", "s": 0.15, "r": "150ms"}}},
}


def song():
    pump = {"type": "pump", "on": "kick", "depth": "-5dB", "attack": "2ms", "release": "180ms", "curve": 0.7}
    return {
        "about": "Chirpers - Escapement, track 3 by chirper-zero: STANDING ROOM. One click a bar between two walls; a wall is a number of sixteenths there and back, so a room is a rhythm: 3 + 4 a room in seven, 2 + 3 in five, 5 + 7 in twelve, and 3 + 5, which is eight and fits the bar, where the echoes stand. A tock keeps each room's time, not the bar's. The click is in every room all the time; the song opens and shuts their doors." + (" From v2 the click walks across each room a step a row (2 + 5, 3 + 4, 4 + 3, 5 + 2 in the corridor), and in standing room it stands." if any(len(w) > 1 for w in WALK.values()) else "") + (" From v3 the bass learns the room's three-three-two (a note for the click, one for each wall) and carries it out of the door; the dry click is panned to where it stands." if LEARN else "") + (" From v4 the walls close in between the stairwell and the hangar: eight rooms too small to count, which sing a rising scale." if PIPES_ON else "") + " Generated by compose/chirpers11/src/chirpers11-t3.py.",
        "tempo": BPM,
        "ceiling": "-1dB",
        "loudness": -11.0,
        "seed": 1,
        "tail": "3s",
        "length": f"{TOTAL}b",
        "event_stable": True,
        "patches": PATCHES,
        "buses": buses(),
        "master": {"fx": [{"type": "eq", "bands": ["hp cutoff=30"]}, {"type": "compressor", "threshold": "-18dB", "ratio": 2, "attack": "20ms", "release": "160ms", "makeup": "0dB"}]},
        "tracks": [
            {"name": "kick", "patch": "sr-kick", "gain": "-8dB", "pan": 0.0, "notes": part("kick", KICK)},
            {"name": "click", "patch": "sr-click", "gain": "2dB", **({"pan": {"value": 0, "mod": [{"src": "auto.stand", "amount": PAN}]}, "auto": {"stand": {"points": stand_lane()}}} if LEARN else {"pan": 0.0}), "notes": part("click", CLICK)},
            {"name": "tock", "patch": "sr-tock", "gain": "-3dB", "pan": 0.0, "notes": tock_notes()},
            {"name": "bass", "patch": "sub-sine params.grit=0.8", "gain": "-14dB", "pan": 0.0, "fx": [pump] + ([{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.away", "amount": 1}]}}] if LEARN else []), **({"auto": {"away": {"points": away_lane()}}} if LEARN else {}), "notes": part("bass", bass_bar)},
            {"name": "clap", "patch": "sr-clap", "gain": "-4dB", "pan": 0.0, "notes": part("clap", CLAP)},
            {"name": "chord", "patch": "sr-chord", "gain": "-22dB", "pan": 0.0, "fx": [pump], "sends": {"dub": "-3dB"}, "notes": part("chord", CHORD)},
        ],
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


def echoes(a, b, n=16):
    """Where one click's returns fall, in sixteenths after it: (step, side)."""
    out, k = [], 1
    while len(out) < n:
        t = (k // 2) * (a + b)
        out += [(t, "both")] if k % 2 == 0 else [(t + a, "left"), (t + b, "right")]
        k += 1
    return sorted(out)[:n]


if __name__ == "__main__":
    if os.environ.get("C11T3_SHOW"):
        sec = 60 / BPM * BEATS
        for name, b0, n, parts, room, width, air in SECS:
            print(f"{name:14s} bars {b0:3d}-{b0 + n:3d}  {int(b0 * sec) // 60}:{b0 * sec % 60:04.1f}-{int((b0 + n) * sec) // 60}:{(b0 + n) * sec % 60:04.1f}  room {room or '-':10s} width {width}  air {air}  {', '.join(sorted(parts))}")
        for room, a, b, b0, b1, opn, shut in places():
            print(f"{room:11s} bars {b0:5.1f}-{b1:5.1f}  {a} + {b} = {a + b}: a click on step 2 comes back on steps " + " ".join(f"{(2 + t) % 16}{'' if s == 'both' else s[0]}" for t, s in echoes(a, b, 12)) + f" ; the tock every {2 * (a + b)} sixteenths, round every {math.lcm(2 * (a + b), 16) // 16} bar(s)")
        for name, p, ms, b0, b1 in pipes():
            print(f"{name:11s} bars {b0:5.1f}-{b1:5.1f}  {p:3s} {hz(p):6.1f} Hz: the walls {ms:.2f} ms away and back; they give back {-60 * ms / 1000 / PIPE_RING:.2f} dB less each time")
        if LEARN:
            print("the bass once it has learnt the room: " + " ".join(f"{st}:{p}" for st, p, n, v in learnt()) + f" ; from bar {next(b for b in range(BARS) if has_learnt(b))} to bar {max(b for b in range(BARS) if has_learnt(b) and plays('bass', b)) + 1}")
            print("the dry click's pan: " + " ".join(f"{p[0]}={p[1] * PAN:+.2f}" for p in stand_lane()))
        print(f"{BARS} bars, {TOTAL} beats, {BARS * sec:.1f} s")
    else:
        open(OUT, "w").write(dump(song()))
