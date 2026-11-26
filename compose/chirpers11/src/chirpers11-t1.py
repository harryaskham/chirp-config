#!/usr/bin/env python3
"""Escapement (Chirpers 11), track 1 (chirper-zero): GIVE OR TAKE. The opener; the slot's word is TIME.

TWO DECKS. Deck A is the grid and never moves: a bass drum on the four, one click on the off-beats, a bass, later a clap. Deck B is
everything else (a sixteenth-note noise click, two wooden tocks in a Euclidean five, a dub chord), and a hand is on it:
it is pushed ahead of the grid and dragged back behind it, the way a DJ rides one record against another. Nothing on
deck B is ever placed by hand: every event has a place on its own record, and the record's position against the grid
is one function of time, d(t), in beats. Where d rises the deck runs fast, and what has a pitch on it goes sharp, as a
record does (12 log2(1 + d') semitones, written as a lane from the same function). So the tempo you hear moving is
real on one deck and false on the other, and the bass drum says which.

THE FORM IS ARITHMETIC: a row is ROW bars; SECTIONS lists, for each section, its rows, which parts play, and the hand:
its kind, its reach in beats and its period in bars. Every start, every event and every lane point comes from those.

  the grid      nothing moves: the kick, the click, deck B's sixteenths straight
  give          the hand begins: deck B breathes against the grid (the reach grows)
  take          the chord comes in on deck B and goes sharp and flat with it
  no ruler      deck A stops. Now deck B's tempo is the only tempo, and it is moving. The kick comes back where it always was.
  both          both decks; the hand's period is a bar and a half, so the push walks through the bar
  the nudge     deck B is taken a whole sixteenth ahead and let back: at the far point it fits again, one step out
  locked        the hand comes off: one tempo, the fullest groove
  out           the parts leave; deck A's click is last

v1 is the SKELETON (26 Nov; the brief: "any version at all opens the groove to it; then keep finessing"): the whole
shape standing, with few sounds.

v2 (26 Nov): DECK B IS A RECORD, AND A RECORD HAS ITS OWN BASS DRUM (C11T1_KNOCK=0 takes it out). From the second
row of "take" deck B plays a bass drum of its own on its own four, with its bass taken out (a high-pass at 315 Hz
on the lane `low`: the incoming record with the low EQ killed, as it is mixed), so the two drums are heard against
each other: one drum when the hand is off, a flam when it leans, a gallop when it pushes. Before "no ruler" the grid
click stops, and in the last bar the BASS IS SWAPPED: deck B's drum gets its lows as deck A's drum stops. For twelve
bars the only bass drum on the record is deck B's, and its tempo is the one that moves. Then deck A's drum comes
back where it always was, the two gallop, and deck B's bass is taken out again over two bars.

v3 (26 Nov): THE STOP (C11T1_STOP=0 writes v2). The record ENDS: in "out" deck B plays on (its chord and its
drum with it), deck A's drum leaves, and at the eleventh bar DECK B IS SWITCHED OFF. Its speed falls in a straight line to nothing over two bars, the same d(t)
as every push before it (d' = -u), so its strokes come further and further apart and everything with a pitch on it
sinks, as a platter does with the motor off. One bar of record takes those two bars, and the next never comes.
The grid click, which never moved, counts four more bars alone.
(Tried in this round and taken out: letting deck B's drum's bass back in for "locked", so the two strike as one big
drum. The two drums' lows are not in step: with it the master had 6 dB LESS under 70 Hz in "locked", not more.)

v4 (26 Nov): WHAT THE TWO DECKS MAKE WHEN THEY MEET (C11T1_MEET=0 writes v3). "Locked" has its reward, and it is
the next song's. Least Common (t2, chirper-one) is three clicks in cycles of 3, 5 and 7 sixteenths, and where two
of them meet there is a ping: 3 with 5 a D, 3 with 7 a B flat, 5 with 7 an F. Between two meetings of all three
(105 sixteenths) the pings make a tune of twelve notes, the same forwards and backwards, that nobody wrote. Here,
from the bar the two decks lock, that tune is heard on Least Common's own vibraphone bar, with nobody playing the
three clicks: the meetings without the clicks. All three meet on the first beat of "locked" (the three notes at
once: F, B flat, D, the top of this song's chord), and the tune goes round four times, through "out", and plays
its last note half a bar before deck B's motor goes off: 26 bars, which is four sixteenths short of one of
Least Common's pages (420). So the first song ends on the tune the second is made of, a track early.
"""
import json
import math
import os

OUT = os.environ.get("C11T1_OUT", os.path.join(os.path.dirname(__file__), "..", "..", "..", "songs", "chirpers11-t1.yaml"))
BPM = 124
BEATS = 4                      # beats in a bar
ROW = 8                        # bars in a row
STEP = 0.25                    # a sixteenth, in beats
ROOT = "G"

KNOCK_ON = {"knock"} if os.environ.get("C11T1_KNOCK", "1") != "0" else set()   # v2: deck B's own bass drum
STOP = os.environ.get("C11T1_STOP", "1") != "0" and bool(KNOCK_ON)               # v3: the record switched off in "out"
MEET = os.environ.get("C11T1_MEET", "1") != "0" and STOP                        # v4: Least Common's meeting tune from "locked" to the stop
MEET_CYCLES = (3, 5, 7)        # Least Common's three clicks, in sixteenths
MEET_NOTE = {(3, 5): "D5", (3, 7): "Bb4", (5, 7): "F4"}   # the ping two of them make when they meet (t2's own notes)
STOP_AT = 10                   # the bar of "out" at which deck B's motor goes off
STOP_BARS = 2                  # the bars its platter takes to stop
# name, rows, the parts that play, the hand: (kind, reach in beats, period in bars, bars over which it comes on and off)
SECTIONS = [
    ("the grid",  2, {"kick", "tick", "hat"},                         ("none", 0.0, 1, 2)),   # the hat from the second row (ENTER)
    ("give",      2, {"kick", "tick", "hat", "tock", "sub"},          ("breathe", 0.05, 2, 2)),
    ("take",      2, {"kick", "tick", "hat", "tock", "sub", "stab"} | KNOCK_ON,  ("breathe", 0.08, 2, 2)),   # deck B's drum from the second row; the click gone for the last four bars
    ("no ruler",  2, {"hat", "tock", "stab"} | KNOCK_ON,                         ("breathe", 0.5, 4, 4)),
    ("both",      3, {"kick", "tick", "hat", "tock", "sub", "stab", "clap"} | KNOCK_ON,  ("breathe", 0.08, 1.5, 2)),
    ("the nudge", 2, {"kick", "tick", "hat", "tock", "sub", "stab", "clap"} | KNOCK_ON,  ("nudge", 0.25, 4, 2)),
    ("locked",    2, {"kick", "tick", "hat", "tock", "sub", "stab", "clap"} | KNOCK_ON,  ("none", 0.0, 1, 2)),
    ("out",       2, {"kick", "tick", "hat", "tock"} | ({"stab", "knock"} if STOP else set()), ("stop", 0.0, STOP_AT, STOP_BARS) if STOP else ("none", 0.0, 1, 2)),
]
RETURN = 4                     # in "no ruler", the kick alone comes back for the last RETURN bars
LEAVE = {"out": [("kick", 8), ("hat", 12), ("tock", 14)]}   # the bar (of the section) from which each part is gone
ENTER = {"the grid": [("hat", ROW)]}                         # ... and from which each part is there
if KNOCK_ON:
    LEAVE["take"] = [("tick", 12)]                           # the ruler's marks go first, then (at "no ruler") the ruler
    ENTER["take"] = [("knock", ROW)]
if STOP:
    LEAVE["out"] = [("kick", 8)]                             # deck B is not taken out: it stops
SWAP = 1                       # bars before "no ruler" over which deck B's drum gets its bass
BACK = 2                       # bars after deck A's drum returns over which it loses it again
KILL = 3.3                     # octaves above 32 Hz at which deck B's drum is cut when its bass is out (315 Hz)
LIFT = 7                       # dB by which what is left of it is turned up while its bass is out (it was 14 dB under the mix without)


def starts():
    out, b = [], 0
    for name, rows, parts, hand in SECTIONS:
        out.append((name, b, rows * ROW, parts, hand)); b += rows * ROW
    return out, b


SECS, BARS = starts()
TOTAL = BARS * BEATS           # the song's length in beats


def section_at(t):
    bar = t / BEATS
    for name, b0, n, parts, hand in SECS:
        if b0 <= bar < b0 + n:
            return name, b0, n, parts, hand
    return SECS[-1]


def d(t):
    """Deck B's position against the grid at grid time t (beats): how far ahead of the grid its record is."""
    if t < 0 or t >= TOTAL:
        return 0.0
    name, b0, n, parts, (kind, reach, period, ramp) = section_at(t)
    if kind == "none":
        return 0.0
    u = t / BEATS - b0                                         # bars into the section
    env = max(0.0, min(1.0, u / ramp, (n - u) / ramp))          # the hand comes on and comes off
    if kind == "breathe":
        return reach * env * math.sin(2 * math.pi * u / period)
    if kind == "nudge":
        return reach * env * (1 - math.cos(2 * math.pi * u / period)) / 2
    if kind == "stop":                                         # period = the bar the motor goes off, ramp = the bars the platter takes
        x, w = (u - period) * BEATS, ramp * BEATS              # beats since the motor went off; the platter's time in beats
        return 0.0 if x <= 0 else -x * x / (2 * w) if x < w else -w / 2 - (x - w)
    raise ValueError(kind)


def stop_at():
    """(the beat at which deck B's motor goes off, the platter's time in beats), or None."""
    for name, b0, n, parts, (kind, reach, period, ramp) in SECS:
        if kind == "stop":
            return (b0 + period) * BEATS, ramp * BEATS
    return None


def when(b):
    """The grid time at which deck B's record reaches its own beat b: t + d(t) = b. None if it never does."""
    st = stop_at()
    if st and b > st[0]:
        ts, w = st
        if b - ts >= w / 2:                                    # the record stops w / 2 beats after the motor does
            return None
        return ts + w - math.sqrt(w * w - 2 * w * (b - ts))    # x - x^2 / 2w = b - ts
    t = b
    for _ in range(40):
        t = b - d(t)
    return t


def speed(t, h=1 / 64):
    """Deck B's speed against the grid at grid time t (1 = the same tempo)."""
    return 1 + (d(t + h) - d(t - h)) / (2 * h)


def spd_lane():
    """Semitones a record on deck B is sharp or flat by, from its speed: one point a sixteenth, only where it moves."""
    pts, last = [["0b", 0]], 0.0
    for i in range(int(TOTAL / STEP) + 1):
        t = i * STEP
        v = round(12 * math.log2(max(speed(t), 0.03)), 3)   # a stopped record has no pitch: the lane rests five octaves down
        if v != last or (pts and i and pts[-1][1] != v):
            if pts[-1][0] != f"{(i - 1) * STEP:g}b" and i:
                pts.append([f"{(i - 1) * STEP:g}b", last])
            pts.append([f"{t:g}b", v])
        last = v
    pts.append([f"{TOTAL:g}b", 0])
    return pts


def plays(part, bar):
    name, b0, n, parts, hand = section_at(bar * BEATS)
    if name == "no ruler" and part == "kick" and bar >= b0 + n - RETURN:
        return True
    for p, gone in LEAVE.get(name, []):
        if p == part and bar >= b0 + gone:
            return False
    for p, there in ENTER.get(name, []):
        if p == part and bar < b0 + there:
            return False
    return part in parts


def low_lane():
    """How much of deck B's drum's bass is cut (1 all, 0 none): in for "no ruler" until deck A's drum is back."""
    pts = [["0b", 1]]
    for name, b0, n, parts, hand in SECS:
        if name == "no ruler":
            pts += [[f"{(b0 - SWAP) * BEATS:g}b", 1], [f"{b0 * BEATS:g}b", 0], [f"{(b0 + n - RETURN) * BEATS:g}b", 0], [f"{(b0 + n - RETURN + BACK) * BEATS:g}b", 1]]
    pts.append([f"{TOTAL:g}b", 1])
    return pts


def note(at, pitch, length, vel):
    return {"at": round(at, 4), "len": round(length, 4), "pitch": pitch, "vel": round(vel, 3)}


def deck_a(part, steps):
    """steps: (step in the bar, pitch, length in steps, velocity). On the grid."""
    out = []
    for bar in range(BARS):
        if plays(part, bar):
            out += [note(bar * BEATS + s * STEP, p, n * STEP, v) for s, p, n, v in steps(bar)]
    return out


def deck_b(part, steps):
    """The same, on deck B's record: each event sounds when the record gets to it."""
    out = []
    for bar in range(BARS):
        if plays(part, bar):
            for s, p, n, v in steps(bar):
                b = bar * BEATS + s * STEP
                t = when(b)
                if t is not None and 0 <= t < TOTAL:
                    end = when(b + n * STEP)
                    out.append(note(t, p, (end if end is not None else t + 4 * n * STEP) - t, v))
    return out


def euclid(k, n, rot=0):
    """k strokes spread as evenly as they will go over n steps."""
    return sorted({(i * n // k + rot) % n for i in range(k)})


KICK = lambda bar: [(s, ROOT + "1", 1, 0.95 if s == 0 else 0.9) for s in (0, 4, 8, 12)]
TICK = lambda bar: [(s, "G5", 1, 0.72 if s in (2, 10) else 0.62) for s in (2, 6, 10, 14)]
HAT = lambda bar: [(s, "C6", 0.5, (0.55, 0.34, 0.62, 0.4)[s % 4] + (0.06 if (s * 5 + bar * 3) % 7 == 0 else 0)) for s in range(16)]
FIVE = euclid(5, 16)
TOCK = lambda bar: [(s, ("G6", "Bb6", "G6", "D7", "Bb6")[i] if bar % 4 != 3 else ("G6", "Bb6", "D7", "F7", "D7")[i], 1, 0.8 if i in (0, 3) else 0.62) for i, s in enumerate(FIVE)]
SUB = lambda bar: [(2, "G2", 1.6, 0.9), (7, "G2", 1, 0.8), (10, "Bb2" if bar % 2 else "G2", 1.6, 0.9)] + ([(14, "F2", 1.6, 0.85)] if bar % ROW == ROW - 1 else [(14, "D3", 1, 0.75)] if bar % 2 else [])
CLAP = lambda bar: [(4, "C4", 1, 0.8), (12, "C4", 1, 0.86)]
KNOCK = lambda bar: [(s, ROOT + "1", 1, 0.92 if s == 0 else 0.86) for s in (0, 4, 8, 12)]   # deck B's four
CHORDS = [("G3", "Bb3", "D4", "F4"), ("G3", "Bb3", "D4", "F4"), ("G3", "A3", "D4", "F4"), ("Eb3", "G3", "Bb3", "D4")]


def STAB(bar):
    ch = CHORDS[(bar // 2) % len(CHORDS)]
    out = [(6, p, 1.5, 0.85) for p in ch]
    if bar % 2:
        out += [(13, p, 1, 0.7) for p in ch]
    return out


def meet_notes():
    """Least Common's meetings, counted from the bar the decks lock to the bar deck B's motor goes off: a ping where
    two of the three cycles meet, the three notes at once where all three do. Nobody plays the cycles."""
    b0 = next(s[1] for s in SECS if s[0] == "locked")
    b1 = next(s[1] for s in SECS if s[0] == "out") + STOP_AT
    out = []
    for s in range((b1 - b0) * 16):
        hit = tuple(c for c in MEET_CYCLES if s % c == 0)
        if len(hit) == 3:
            out += [note((b0 * 16 + s) * STEP, p, 2 * STEP, 0.85) for p in ("F4", "Bb4", "D5")]
        elif len(hit) == 2:
            out.append(note((b0 * 16 + s) * STEP, MEET_NOTE[hit], 2 * STEP, 0.75))
    return out


PATCHES = {
    "gt-kick": {"about": "Give or Take's bass drum (chirper-zero, 26 Nov): the engine's machine kick, short and dry, resting on the song's G; deck A.",
                "play": {"vel_sens": 0.3},
                "synth": {"layers": [{"type": "machine", "machine": {"part": "kick", "decay": "280ms", "click": 0.65, "drive": 0.35, "punch": 22, "punch_time": "34ms"}}],
                          "filters": ["hp cutoff=28"], "amp": {"a": "0.1ms", "d": "0s", "s": 1, "r": "1s"}}},
    "gt-meet": {"about": "Give or Take's ping (chirper-zero, 26 Nov, v4): Least Common's `lc-ping` (chirper-one) rebuilt here under this song's name: a vibraphone bar with no motor, half a second long. It plays t2's meeting tune once the two decks are locked.",
                "play": {"event_stable": True, "vel_sens": 0.5},
                "synth": {"layers": [{"type": "modal", "modes": "vibes", "decay": "650ms", "bright": 0.55, "strike": 0.3}], "amp": {"a": "0.3ms", "d": "900ms", "s": 0, "r": "200ms"}}},
    "gt-knock": {"about": "Give or Take's second bass drum (chirper-zero, 26 Nov, v2): deck B's own, a little shorter and clickier than deck A's, through a high-pass on the lane `low` (32 Hz to 315 Hz: the low EQ of the incoming record, killed until the bass is swapped); its pitch follows deck B's speed.",
                 "play": {"vel_sens": 0.3},
                 "synth": {"layers": [{"type": "machine", "machine": {"part": "kick", "decay": "220ms", "click": 0.8, "drive": 0.3, "punch": 20, "punch_time": "30ms"}}],
                           "pitch": {"value": 0, "mod": [{"src": "auto.spd", "amount": 1}]},
                           "filters": [{"kind": "hp", "cutoff": {"value": 32, "mod": [{"src": "auto.low", "amount": KILL}]}, "q": 0.7}], "amp": {"a": "0.1ms", "d": "0s", "s": 1, "r": "1s"}}},
    "gt-tick": {"about": "Give or Take's grid click (chirper-zero, 26 Nov): the machine's rim, one voice, high and dry; deck A's ruler marks.",
                "play": {"vel_sens": 0.5},
                "synth": {"layers": [{"type": "machine", "machine": {"part": "rim", "decay": "35ms"}}], "amp": {"a": "0.1ms", "d": "0s", "s": 1, "r": "300ms"}}},
    "gt-hat": {"about": "Give or Take's sixteenth click (chirper-zero, 26 Nov): a 14 ms burst of white noise between 6 and 12.5 kHz; deck B.",
               "play": {"vel_sens": 0.7},
               "synth": {"layers": ["white"], "filters": [{"kind": "hp", "cutoff": 6000, "q": 0.8}, "peak cutoff=8500 q=2 gain=4dB", "lp cutoff=12500"],
                         "amp": {"a": "0.1ms", "d": "14ms", "s": 0, "r": "8ms", "curve": 5}}},
    "gt-clap": {"about": "Give or Take's clap (chirper-zero, 26 Nov): the machine's clap, three bursts, short; deck A.",
                "play": {"vel_sens": 0.4},
                "synth": {"layers": [{"type": "machine", "machine": {"part": "clap", "bursts": 3, "decay": "140ms"}}], "amp": {"a": "0.1ms", "d": "0s", "s": 1, "r": "400ms"}}},
    "gt-tock": {"about": "Give or Take's tock (chirper-zero, 26 Nov): a wooden bar on the modal layer (after Common Measure's clave), whose pitch follows deck B's speed (auto.spd, semitones).",
                "play": {"vel_sens": 0.5},
                "synth": {"layers": [{"type": "modal", "modes": "glock", "bright": 0.9, "damp": 0.25, "decay": "160ms", "strike": 0.5, "tilt": 0.0}],
                          "pitch": {"value": 0, "mod": [{"src": "auto.spd", "amount": 1}]}, "amp": {"a": "0.2ms", "d": "260ms", "s": 0, "r": "40ms"}}},
    "gt-stab": {"about": "Give or Take's dub chord (chirper-zero, 26 Nov): three saws and a square through a short filter envelope, dry (the echo is a bus); its pitch follows deck B's speed (auto.spd, semitones), as a chord on a nudged record does.",
                "synth": {"layers": ["saw unison=3 detune=0.15 spread=0.6", "square level=-8dB"], "env": {"f": {"a": "1ms", "d": "200ms", "s": 0.08, "r": "100ms"}},
                          "pitch": {"value": 0, "mod": [{"src": "auto.spd", "amount": 1}]},
                          "filters": [{"kind": "lp", "cutoff": {"value": 600, "mod": [{"src": "env.f", "amount": 2.4}, {"src": "vel", "amount": 1}]}, "q": 1.6}],
                          "amp": {"a": "1ms", "d": "280ms", "s": 0.15, "r": "150ms"}}},
}


def song():
    lane = spd_lane()
    pump = {"type": "pump", "on": "kick", "depth": "-5dB", "attack": "2ms", "release": "180ms", "curve": 0.7}
    doc = {
        "about": "Chirpers - Escapement, track 1 by chirper-zero: GIVE OR TAKE. Two decks. Deck A (the bass drum, one click, the sub) is the grid and never moves. Deck B (the sixteenth click, the tocks, the dub chord) has a hand on it: pushed ahead of the grid and dragged back, and what has a pitch on it goes sharp and flat with its speed, as a record does. Generated by compose/chirpers11/src/chirpers11-t1.py.",
        "tempo": BPM,
        "ceiling": "-1dB",
        "loudness": -10.5,
        "seed": 1,
        "tail": "2s",
        "length": f"{TOTAL}b",
        "event_stable": True,
        "patches": PATCHES,
        "buses": {
            "room": {"fx": ["reverb kind=room decay=0.5s mix=1 predelay=6ms", "hp cutoff=400"]},
            "dub": {"fx": [{"type": "delay", "time": "3/16", "feedback": 0.45, "mix": 1, "tone": 2200}, "hp cutoff=350", "reverb kind=hall decay=2.4s mix=0.3"]},
        },
        "master": {"fx": [{"type": "eq", "bands": ["hp cutoff=30", "peak cutoff=120 q=0.7 gain=3dB"]}, {"type": "compressor", "threshold": "-18dB", "ratio": 2, "attack": "20ms", "release": "160ms", "makeup": "0dB"}]},
        "tracks": [
            {"name": "kick", "patch": "gt-kick", "gain": "-4.5dB", "pan": 0.0, "notes": deck_a("kick", KICK)},
            {"name": "tick", "patch": "gt-tick", "gain": "-3dB", "pan": 0.0, "sends": {"room": "-12dB"}, "notes": deck_a("tick", TICK)},
            {"name": "sub", "patch": "sub-sine params.grit=0.8", "gain": "-5dB", "pan": 0.0, "fx": [pump], "notes": deck_a("sub", SUB)},
            {"name": "clap", "patch": "gt-clap", "gain": "-5dB", "pan": 0.0, "sends": {"room": "-9dB"}, "notes": deck_a("clap", CLAP)},
            {"name": "hat", "patch": "gt-hat", "gain": "0dB", "pan": 0.25, "sends": {"room": "-16dB"}, "notes": deck_b("hat", HAT)},
            {"name": "tock", "patch": "gt-tock", "gain": "-8.5dB", "pan": -0.3, "sends": {"room": "-10dB", "dub": "-18dB"}, "auto": {"spd": {"points": lane}}, "notes": deck_b("tock", TOCK)},
            {"name": "stab", "patch": "gt-stab", "gain": "-23dB", "pan": 0.1, "fx": [pump], "sends": {"dub": "-7dB"}, "auto": {"spd": {"points": lane}}, "notes": deck_b("stab", STAB)},
        ],
    }
    if KNOCK_ON:
        doc["tracks"].append({"name": "knock", "patch": "gt-knock", "gain": "-5dB", "pan": 0.0, "fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.low", "amount": LIFT}]}}],
                              "auto": {"spd": {"points": lane}, "low": {"points": low_lane()}}, "notes": deck_b("knock", KNOCK)})
        doc["about"] = doc["about"].replace("Deck B (the sixteenth click, the tocks, the dub chord) has a hand on it", "Deck B (the sixteenth click, the tocks, the dub chord, and from v2 a bass drum of its own with its bass taken out) has a hand on it")
    else:
        del PATCHES["gt-knock"]
    if MEET:
        doc["tracks"].append({"name": "meet", "patch": "gt-meet", "gain": "-14dB", "pan": 0.0, "sends": {"room": "-10dB"}, "notes": meet_notes()})
        doc["about"] = doc["about"].replace(" Generated by", " From v4, when the two decks lock, Least Common's meeting tune (the next song's: pings where cycles of 3, 5 and 7 sixteenths meet) goes round four times and ends half a bar before deck B is switched off. Generated by")
    else:
        del PATCHES["gt-meet"]
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


if __name__ == "__main__":
    if os.environ.get("C11T1_SHOW"):
        sec = 60 / BPM * BEATS
        for name, b0, n, parts, (kind, reach, period, ramp) in SECS:
            far = max(abs(d(t / 16)) for t in range(b0 * BEATS * 16, (b0 + n) * BEATS * 16))
            fast = max(speed(t / 16) for t in range(b0 * BEATS * 16, (b0 + n) * BEATS * 16)); slow = min(speed(t / 16) for t in range(b0 * BEATS * 16, (b0 + n) * BEATS * 16))
            print(f"{name:10s} bars {b0:3d}-{b0 + n:3d}  {int(b0 * sec) // 60}:{b0 * sec % 60:04.1f}-{int((b0 + n) * sec) // 60}:{(b0 + n) * sec % 60:04.1f}  {kind:8s} furthest {far:.3f} beats ; "
                  f"deck B's tempo {BPM * slow:.1f}-{BPM * fast:.1f} ; {12 * math.log2(max(slow, 0.03)):+.2f} to {12 * math.log2(fast):+.2f} semitones ; {', '.join(sorted(parts))}")
        print(f"{BARS} bars, {TOTAL} beats, {BARS * sec:.1f} s ; the five: {FIVE}")
    else:
        open(OUT, "w").write(dump(song()))
