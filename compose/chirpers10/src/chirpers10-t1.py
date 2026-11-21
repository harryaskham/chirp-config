#!/usr/bin/env python3
"""chirpers X (Common Time), track 1 "Common Time" - chirper-zero. Generator for songs/chirpers10-t1.yaml.

THE IDEA. One steady pulse (126 bpm, 4/4, never broken) and three WHEELS that turn under it for the whole piece:
cells five, seven and eleven sixteenths long. Each wheel is a global clock: it starts at bar 1 and keeps turning
whether or not anything plays it, and every section only opens windows onto the wheels. All three and the bar line
coincide at bar 1 and then not again for 385 bars (5 x 7 x 11): the piece IS that wait, and the landing at bar 386
is where it finally plays in plain common time. On the way, two wheels at a time meet on a bar line (five and seven
every 35 bars, five and eleven every 55, seven and eleven every 77); those meetings are the section boundaries, so
the form (35 20 15 7 28 5 30 14 11 10 | 35 | 10 11 14 30 5 28 7 15 20 35 bars) is a palindrome nobody chose, and the
two wheels that have just met are the ones the next section is made of.

All positions below are in sixteenths (s16) unless a name says bars.
"""
import json, os, random

OUT = os.environ.get("C10T1_OUT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../songs/chirpers10-t1.yaml"))
RIG_L = os.environ.get("C10T1_RIGL", "ct-chug-l")
RIG_R = os.environ.get("C10T1_RIGR", "ct-chug-r")
BITE_L = os.environ.get("C10T1_BITEL", "ct-bite-l")      # the seven wheel's rig ("" = the seven wheel stays on the tight rig)
BITE_R = os.environ.get("C10T1_BITER", "ct-bite-r")
BITE_DB = os.environ.get("C10T1_BITEDB", "4.3dB")     # as loud as the tight rig on the same riff (LUFS, the pair alone)
CRUNCH_L = os.environ.get("C10T1_CRUNCHL", "ct-crunch-l")    # the low-gain rig that answers the pick: the first break and the approach's first guitars ("" = off)
CRUNCH_R = os.environ.get("C10T1_CRUNCHR", "ct-crunch-r")
CRUNCH_DB = os.environ.get("C10T1_CRUNCHDB", "2dB")
WALL_L = os.environ.get("C10T1_WALLL", "ct-wall-l")
WALL_R = os.environ.get("C10T1_WALLR", "ct-wall-r")
# v20, THE STOPS STOP. Every heavy rig opens with a `sympathetic` effect (the other strings ringing along). Its ring, small as
# it is, keeps a saturated amp at full output through every rest, and the rig's gate sits after the amp where the level never
# falls: a half-beat stab sounded for 0.8 s. C10T1_STOPS names, per rig, what is done about it in a song-local copy of the
# patch: "nosym" (no ring), "gate:-28" (a gate between the compressor and the amp, where a real rig's sits), "decay:0.3s"
# (a shorter ring); several joined with "+". "" = the rigs as they were (v19).
# Kept: no ring on the three heavy rigs (ct-chug, ct-bite, ct-wall). Guitars alone in the stop-times: the quieter quarter of
# the time sat 2 dB under the loud level, now 23 dB, and a third of the time is more than 20 dB down. The riffs hardly change
# (their notes follow each other without rests), and on the Bleed and Faultless benches the attack measures move by 0.5 dB at
# most. The wall rig's chords still ring as long (that is the string); what goes is the second it hung on after a cut, so
# the stop before the landing is a stop. The ring was also 2-3 dB of the guitars' 315-500 Hz: the bus eq gives 1 dB back.
STOPS = dict(x.split("=") for x in os.environ.get("C10T1_STOPS", "chug=nosym,bite=nosym,wall=nosym").split(",") if x)
LIB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "patches")
STOP_PATCHES = {}


def stopped(name, how):
    """A song-local copy of library rig `name` whose rests are rests. Returns the local patch's name."""
    if not how or not name:
        return name
    if how == "nosym":
        return name + " fx.0.mix=0"         # the plain case needs no copy: an override on the library patch
    fx = json.load(open(os.path.join(LIB, name + ".yaml")))["fx"]
    assert fx[0]["type"] == "sympathetic" and fx[1]["type"] == "compressor" and fx[2]["type"] == "amp", name
    fx = [dict(f) if isinstance(f, dict) else f for f in fx]
    gate = None
    for h in how.split("+"):
        if h == "nosym":
            fx[0]["mix"] = 0
        elif h.startswith("decay:"):
            fx[0]["decay"] = h[6:]
        elif h.startswith("gate:"):
            gate = {"type": "gate", "threshold": h[5:] + "dB", "attack": "0.3ms", "hold": "10ms", "release": "30ms"}
    if fx[0].get("mix") == 0:
        fx = fx[1:]
    if gate:
        i = [j for j, f in enumerate(fx) if isinstance(f, dict) and f["type"] == "amp"][0]
        fx.insert(i, gate)
    local = name + "-stop"
    STOP_PATCHES[local] = {"about": f"chirper-zero: {name} with its rests made rests ({how}): see the generator, v20", "extends": name, "fx": fx}
    return local


for _rig, _names in (("chug", ("RIG_L", "RIG_R")), ("bite", ("BITE_L", "BITE_R")), ("wall", ("WALL_L", "WALL_R"))):
    for _n in _names:
        globals()[_n] = stopped(globals()[_n], STOPS.get(_rig, ""))
CLEAN = os.environ.get("C10T1_CLEAN", "ct-clean")
BASS = os.environ.get("C10T1_BASS", "ct-bass")
KIT = os.environ.get("C10T1_KIT", "ct-kit")
DCLIP = os.environ.get("C10T1_DCLIP", "-13")       # drums bus: soft clip ceiling, dBFS ("" = off)
MGAIN = os.environ.get("C10T1_MGAIN", "")       # master: gain into the limiter, then back down ("" = off): the stream gets the release's dynamics
BPM = 126
BOUNDS = [0, 35, 55, 70, 77, 105, 110, 140, 154, 165, 175, 210, 220, 231, 245, 275, 280, 308, 315, 330, 350, 385]
CODA = 24
NB = 385 + CODA

NOTE = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
F1 = 29
AB, BB, DB, EB = 32, 34, 37, 39      # other grounds: Ab1, Bb1 (the seventh string), Db2, Eb2 (the sixth string)
GB = 30


def nm(m):
    return f"{NOTE[m % 12]}{m // 12 - 1}"


T = {}  # track name -> notes


def add(tr, s16, len16, pitch, vel, **expr):
    note = {"at": round(s16 / 4, 4), "len": round(len16 / 4, 4), "pitch": pitch if isinstance(pitch, str) else nm(pitch),
            "vel": round(min(1.0, max(0.05, vel)), 3)}
    if expr:
        note["expr"] = {k: float(v) for k, v in expr.items()}
    T.setdefault(tr, []).append(note)


# ---- the wheels' cells: (offset, length, kind). c = palm-muted chug on the root, o = the root left open,
# h = the next hook note, x = a dead note, p = a short power chord, P = a big open chord left to ring, d = a dissonant stab
FIVE_A = [(0, 2, "c"), (2, 1, "c"), (3, 2, "h")]
FIVE_B = [(0, 1, "c"), (1, 1, "c"), (2, 1, "c"), (3, 2, "h")]
FIVE_S = [(0, 2, "p")]
SEVEN_A = [(0, 2, "c"), (2, 2, "c"), (4, 1, "c"), (5, 2, "h")]
SEVEN_B = [(0, 1, "c"), (1, 1, "c"), (2, 2, "h"), (4, 1, "c"), (5, 2, "h")]
ELEVEN_A = [(0, 3, "o"), (3, 2, "c"), (5, 3, "h"), (8, 1, "c"), (9, 2, "h")]
ELEVEN_B = [(0, 1, "c"), (1, 1, "c"), (2, 1, "c"), (3, 2, "h"), (5, 1, "c"), (6, 2, "h"), (8, 1, "c"), (9, 1, "c"), (10, 1, "x")]
ELEVEN_W = [(0, 8, "P")]
ELEVEN_D = [(0, 11, "P")]                 # one chord to a turn, ringing into the next
EIGHT = [(0, 2, "c"), (2, 1, "c"), (3, 1, "c"), (4, 2, "h"), (6, 2, "c")]   # the coda: a cell that fits the bar

# the hook: the notes the wheels turn through, in semitones above the root (F: Ab Gb B C)
H1 = [3, 1, 6, 7]
H2 = [6, 5, 3, 1]
H3 = [1, 3, 1, 8]
OCT = None
GROW = ([3], [3, 1], [3, 1, 6], H1)      # the hook is learnt a note at a time: Ab; Ab Gb; Ab Gb B; Ab Gb B C
HX = [3, 1, 6, 7, 10, 8, 6]              # and in the last third it has grown to seven: Ab Gb B C Eb Db B
H8 = [3, 1, 6, 7, 10, 8, 6, 1]           # at the landing, eight: two to a bar, a four-bar phrase


def strikes(p, cell, s0, s1):
    """The strikes of global wheel `p` that fall in [s0, s1): (s16, length, kind, index in the cell, hook index)."""
    nh = sum(1 for c in cell if c[2] == "h")
    k = s0 // p
    while k * p < s1:
        jh = 0
        for j, (off, ln, kind) in enumerate(cell):
            t = k * p + off
            if s0 <= t < s1:
                yield t, min(ln, s1 - t), kind, j, k * nh + jh
            if kind == "h":
                jh += 1
        k += 1


def landings(p, s0, s1):
    """Bar lines in [s0, s1) where wheel p begins a turn."""
    return [t for t in range(s0 - s0 % 16 + (16 if s0 % 16 else 0), s1, 16) if t % p == 0]


def s16(b):
    return int(round(b * 16))


SEVEN_RIG = {"gl": "sl", "gr": "sr"}
CRUNCH = {"gl": "kl", "gr": "kr"} if CRUNCH_L else None     # pass as rig=: the part goes to the crunch rig
SOFT = (0.6, 1.25)        # dyn= for the crunch rig, which answers the pick: the chugs soft, the hook notes hard


def gtr(trs, p, cell, b0, b1, root=F1, hook=H1, vel=0.85, ramp=None, rig=None, dyn=(1.0, 1.05), grow=None):
    """`grow`: the riff assembles itself. A list of (turns, the cell's notes that sound for that many turns of the wheel);
    after the list, the whole cell."""
    s0, s1 = s16(b0), s16(b1)
    if DBL_MAP and set(trs) & set(G2) and set(trs) & set(G) and p != 8:
        DBL_EXCL.append((b0, b1))
    for t, ln, kind, j, hi in strikes(p, cell, s0, s1):
        if grow:
            turn, only = (t - cell[j][0]) // p - s0 // p, None
            for n, idx in grow:
                if turn < n:
                    only = idx
                    break
                turn -= n
            if only is not None and j not in only:
                continue
            lone = only is not None and len(only) == 1
        v = vel * (1.0 if j == 0 else 0.9)
        if ramp:
            v *= ramp[0] + (ramp[1] - ramp[0]) * (t - s0) / max(1, s1 - s0)
        if grow and lone:
            v *= LONE                    # a note alone is struck firmly: it is what the spring answers
        for tr in trs:
            if rig:
                tr = rig.get(tr, tr)
            elif p == 7 and BITE_L:
                tr = SEVEN_RIG.get(tr, tr)        # a wheel is known by its rig: five ct-chug, seven ct-bite, eleven ct-wall
            if REAL_FROM is not None and b0 >= REAL_FROM:
                tr = LAND_MAP.get(tr) if p == 8 and tr in LAND_MAP else REAL_MAP.get(tr, tr)   # after the eye the tight rig's string is a real one (v29); the landing riff has a rig of its own (v37)
            if kind == "c":
                add(tr, t, ln, root, v * (dyn[0] if rig else 1.0), pm=1)
            elif kind == "o":
                add(tr, t, ln, root, v)
            elif kind == "h":
                add(tr, t, ln, root + hook[hi % len(hook)], v * (dyn[1] if rig else 1.05))
            elif kind == "x":
                add(tr, t, ln, root, v * 0.8, dead=1)
            elif kind == "p":
                add(tr, t, ln, ",".join(nm(root + i) for i in (0, 7, 12)), v)
            elif kind == "P":
                add(tr, t, ln, ",".join(nm(root + i) for i in (0, 7, 12, 19)), v)
            elif kind == "d":
                add(tr, t, ln, ",".join(nm(root + i) for i in (24, 37, 42)), v)


def layer(tr, p, cell, b0, b1, root=F1, hook=H1, vel=0.8, up=24):
    """A synth doubling a riff: one note to each strike of the wheel, `up` semitones above the guitars (dead notes left out;
    chugs short, the rest full length)."""
    for t, ln, kind, j, hi in strikes(p, cell, s16(b0), s16(b1)):
        if kind == "x":
            continue
        n = root + (hook[hi % len(hook)] if kind == "h" else 0) + up
        add(tr, t, ln * (0.6 if kind == "c" else 0.95), n, vel * (1.0 if j == 0 else 0.9))


def harm(trs, p, cell, b0, b1, interval=12, root=F1, hook=H1, vel=0.8, power=False):
    """A second guitar that plays only the wheel's hook notes, `interval` semitones up (power: each as a power chord)."""
    for t, ln, kind, j, hi in strikes(p, cell, s16(b0), s16(b1)):
        if kind == "h":
            n = root + hook[hi % len(hook)] + interval
            for tr in trs:
                if REAL_FROM is not None and b0 >= REAL_FROM:
                    tr = REAL_MAP.get(tr, tr)     # after the eye the tight rig's string is a real one (v29)
                add(tr, t, ln, ",".join(nm(n + i) for i in (0, 7, 12)) if power else n, vel)


def bass(p, cell, b0, b1, root=F1, hook=H1, vel=0.85, ramp=None):
    """hook=OCT: the bass is on a wheel of its own, under guitars on another, so it keeps to the ground and marks its
    hook strikes with the octave. With the hook's own notes it spent about a third of its time a semitone or a tritone
    from the guitars, down where that is mud (clash.py; v9)."""
    s0, s1 = s16(b0), s16(b1)
    for t, ln, kind, j, hi in strikes(p, cell, s0, s1):
        v = vel * (1.0 if j == 0 else 0.9)
        if ramp:
            v *= ramp[0] + (ramp[1] - ramp[0]) * (t - s0) / max(1, s1 - s0)
        if kind == "h":
            add("bass", t, ln, root + (hook[hi % len(hook)] if hook else 12), v)
        elif kind == "x":
            add("bass", t, ln * 0.5, root, v * 0.7)
        else:
            add("bass", t, ln if kind in ("o", "P") else ln * 0.9, root, v)


def kick(p, cell, b0, b1, vel=0.9, only_first=False, fill16=False):
    s0, s1 = s16(b0), s16(b1)
    hit_at = set()
    for t, ln, kind, j, hi in strikes(p, cell, s0, s1):
        if only_first and j:
            continue
        if t not in hit_at:
            add("kick", t, 1, "k", vel * (1.0 if j == 0 else 0.86))
            hit_at.add(t)
    if fill16:   # double kick: the sixteenths between the wheel's strikes, softer
        for t in range(s0, s1):
            if t not in hit_at:
                add("kick", t, 1, "k", vel * 0.62)


FILL_LEN = {None: 0, "run": 8, "run16": 16, "roll": 8, "roll16": 16, "toms": 12, "kicks": 8, "stop": 8}


def fill(b1, kind="run", vel=0.85):
    """Into bar line b1. run: snare then down the toms; roll: a snare crescendo; toms: the five cell on the toms;
    kicks: thirty-second-note kicks under two snares; stop: nothing but one choked stab."""
    e = b1 * 16
    if kind in ("run", "run16"):
        n = FILL_LEN[kind]
        seq = ["s", "s", "t1", "t1", "t2", "t2", "ft", "ft"]
        for i in range(n):
            piece = seq[i * len(seq) // n]
            add("snare" if piece == "s" else "toms", e - n + i, 1, piece, vel * (0.7 + 0.3 * i / (n - 1)))
    elif kind in ("roll", "roll16"):
        n = FILL_LEN[kind]
        for i in range(n):
            add("snare", e - n + i, 1, "s", vel * (0.45 + 0.55 * i / (n - 1)))
    elif kind == "toms":
        for i, (off, piece) in enumerate([(0, "t1"), (2, "t1"), (3, "t2"), (5, "t2"), (7, "t3"), (8, "ft"), (10, "ft"), (11, "ft2")]):
            add("toms", e - 12 + off, 1, piece, vel * (0.75 + 0.25 * i / 7))
    elif kind == "kicks":
        for i in range(16):
            add("kick", e - 8 + i * 0.5, 0.5, "k", vel * (0.6 + 0.4 * i / 15))
        add("snare", e - 2, 1, "s", vel)
        add("snare", e - 1, 1, "s", vel)
    elif kind == "stop":
        for tr in ("gl", "gr"):
            add(tr, e - 4, 2, "F1,C2,F2", vel)
        add("bass", e - 4, 2, "F1", vel)
        add("kick", e - 4, 1, "k", vel)
        add("cym", e - 4, 2, "cch", vel * 0.9)


def kit(a, z, piece="x", step=4, mode="half", fl="run", cvel=0.62, ghost=False, crash_at_start=True, svel=0.9):
    """A section's pulse: the cymbal on its step, the snare, a crash on the first bar line and a fill into the last."""
    skip = FILL_LEN[fl]
    if crash_at_start:
        crash(a * 16)
    for t in range(a * 16, z * 16 - skip, step):
        add("toms" if piece in ("ft", "ft2", "t1", "t2", "t3") else "cym", t, step, piece, cvel * (1.12 if t % 16 == 0 else 1.0 if t % 8 == 0 else 0.9))
    offs = {"half": [8], "back": [4, 12], "blast": [2, 6, 10, 14], "none": []}[mode]
    for b in range(a, z):
        for o in offs:
            if b * 16 + o < z * 16 - skip:
                add("snare", b * 16 + o, 2, "s", svel)
        if ghost:
            for o in ([5, 7, 11, 14] if mode == "half" else [7, 9, 15]):
                if b * 16 + o < z * 16 - skip:
                    add("snare", b * 16 + o, 1, "s", 0.3)       # the same drum struck softly: 7-10 dB under the backbeat
                    # after the drums bus's clip (at 0.42 it was only 3 dB under). v4 and v5 used the kit's ghost
                    # piece `g`, which is the old kit's snare
    if fl:
        fill(z, fl)


def crash(t, vel=0.85, piece="c"):
    add("cym", t, 8, piece, vel)


def rise(b1, bars=1, vel=0.8):
    """A noise swell into bar line b1, and a low drop on it."""
    add("rise", (b1 - bars) * 16, bars * 16 - 0.3, "C5", vel)
    add("drop", b1 * 16, 12, "F1", vel)


CL5 = [0, 7, 12]            # the ticks' notes, in semitones above the root's F3
CL7 = [7, 14, 12, 17]
CL11 = [12, 19, 15, 22, 20]   # dark: with the minor third, seventh and sixth (the opening)
CL11_OPEN = [12, 19, 14, 24, 21]   # open: second and sixth, no third (the eye)
TICK5 = [(0, 1, "c"), (2, 1, "c"), (3, 1, "c")]
TICK7 = [(0, 1, "c"), (2, 1, "c"), (4, 1, "c"), (5, 1, "c")]
TICK11 = [(0, 1, "c"), (3, 1, "c"), (5, 1, "c"), (8, 1, "c"), (9, 1, "c")]


def tick(tr, p, cell, notes, b0, b1, vel=0.42, ramp=None, harmony=None):
    s0, s1 = s16(b0), s16(b1)
    for t, ln, kind, j, hi in strikes(p, cell, s0, s1):
        v = vel + (0.18 if j == 0 else 0)
        if ramp:
            v *= ramp[0] + (ramp[1] - ramp[0]) * (t - s0) / max(1, s1 - s0)
        root = 53 + (root_at(harmony, t) if harmony else 0)
        add(tr, t, 1.8, root + notes[j % len(notes)] - (12 if tr in ("cl11", "e11") and CLEAN11 else 0), v)   # the bell is played in harmonics: written an octave low


def root_at(harmony, t):
    r = 0
    for start, off in harmony:
        if t >= start:
            r = off
    return r


def bed(harmony, end, vel=0.6, fifth=True, pad_vel=0.5):
    """The drone, its fifth and the open chord over a list of (s16 start, semitones from F), each held to the next."""
    for i, (start, off) in enumerate(harmony):
        stop = harmony[i + 1][0] if i + 1 < len(harmony) else end
        t = start
        while t < stop:
            ln = min(64, stop - t) + 0.8
            low = 29 + off if off <= 3 else 29 + off - 12        # keep the drone between Gb1 and Ab1... or just above
            if low < 29:
                low += 12
            add("home", t, ln, low, vel)
            if fifth:
                add("fifth", t, ln, low + 7, vel * 0.8)
                add("fifth", t, ln, low + 12, vel * 0.8)
            if pad_vel:
                for iv in (0, 7, 14, 19):
                    add("air", t, ln, 41 + off + iv, pad_vel)
            t += 64


C5 = 72
LONG_WAIT = [(C5, 1), (C5 - 1, 1), (C5 - 4, 1), (C5 - 7, 2), (C5 - 6, 1), (C5 - 4, 1), (C5 - 1, 1), (C5, 2),
             (C5 + 1, 1), (C5, 1), (C5 - 4, 1), (C5 - 6, 2), (C5 - 7, 1), (C5 - 4, 1), (C5 - 6, 1), (C5 - 7, 3)]
LONG_WAIT_TURNS = sum(n for _, n in LONG_WAIT)     # 21 turns of eleven = 231 sixteenths


def long_wait(b0, b1, vel=0.75, up=0, start=None, tr="lead", i0=0):
    """The lead's tune: one note to each turn of the eleven wheel (some held for two or three turns)."""
    s0, s1 = s16(b0), s16(b1)
    t = s0 + (-s0) % 11 if start is None else start
    i = i0
    while t < s1:
        pitch, turns = LONG_WAIT[i % len(LONG_WAIT)]
        add(tr, t, min(turns * 11, s1 - t), pitch + up, vel)
        t += turns * 11
        i += 1


# v52: THE TUNE COMES BACK IN HARMONY (section round, 8:15-8:44, in the windows 7:37-8:38 the map called static and
# "little new"). Where all three wheels turn together (7:46) the lead plays the tune twice through, the same notes in
# the same octave both times; the second time the rhythm guitars gain a harmony and the lead did not. Now the lead
# does: on its second pass a SECOND LEAD GUITAR plays the tune a third above it, note for note on the eleven wheel
# (E flat over C and B, C over A flat, A flat over F, B flat over G flat, F over D flat: every one a note of the
# piece's mode). Twin leads: the tune is said once alone and once by two. It is the only place in the piece where
# the tune is harmonised by another guitar (in the eye, three singers double it; in the ending a second voice
# answers it).
# The pair weighs what the one lead did: under the harmony the lead comes down 1.5 dB and the second sits 4 dB under
# it, so the two add up to the lead's old power. (First bench, the lead left alone: the stretch read 0.9 dB up at
# 250-500 Hz and 0.7 at 500 Hz-1 kHz, where it was already 0.6 and 1.0 over the records with the tune alone.)
# the second lead's level against the lead's, dB ; its pan ; its velocity ; both leads' trim while they play together, dB. "" = v51.
TWIN = os.environ.get("C10T1_TWIN", "-4;0.3;0.8;-1.5")
TWIN_AT = []                          # the sixteenth the second lead comes in, and the one it stops
THIRD = {72: 75, 71: 75, 68: 72, 65: 68, 66: 70, 73: 77}


def twin(start, s1):
    """The tune's notes from `start` (a sixteenth) to `s1`, a third above, on the second lead."""
    t, i = start, 0
    while t < s1:
        pitch, turns = LONG_WAIT[i % len(LONG_WAIT)]
        add("lead2", t, min(turns * 11, s1 - t), THIRD[pitch], float(TWIN.split(";")[2]))
        t += turns * 11
        i += 1


MODE = [0, 1, 3, 5, 6, 7, 8, 10]     # F Gb Ab Bb B C Db Eb


def deg(d, base=65):
    return base + 12 * (d // 8) + MODE[d % 8]


SOLO_SCALE = [61, 63, 65, 68, 70, 72]     # Db Eb F Ab Bb C: the ground's major six, no fourth
#  turns of seven, flurry notes, the sixteenths they take, first note (index in the scale), steps between the notes
SOLO = [(2, 5, 4, 2, (2, -1, 2, -1, 2)), (2, 5, 4, 4, (2, -1, 2, -1, 2)), (3, 7, 6, 5, (2, -1, 2, -1, 2, -1, 2)),
        (2, 5, 4, 12, (-2, 1, -2, 1, -2)), (2, 5, 4, 6, (2, -1, 2, -1, 2)), (3, 7, 6, 7, (2, -1, 2, -1, 2, -1, 2)),
        (2, 10, 8, 13, (-1, -1, 2, -1, -1, 2, -1, -1, -1, -1)), (2, 10, 8, 6, (1, 1, -2, 1, 1, -2, 1, 1, 1, 1)),
        (3, 14, 12, 2, (1, 2, -1, 1, 2, -1, 1, 2, -1, 1, 2, -1, 1, 1)),
        (4, 21, 18, 1, (2, 1, -1, 2, 1, -1, 2, 1, -1, 2, 1, -1, 2, 1, -1, 2, -1, 1, -1, 1, -2))]
assert all(len(st) == n for _, n, _, _, st in SOLO)


WAH_PTS = []        # the wah pedal over the lead's run: (sixteenth, position 0 heel .. 1 toe)


def solo(b0, b1, vel=0.82):
    """The lead floats over the riff. Each phrase starts on a turn of the seven wheel: a flurry of five, seven, ten or
    more notes in the time of four, six, eight sixteenths (so off the grid the band is on), joined, landing on one
    long held note. The flurries lengthen; the last climbs for four turns."""
    s0, s1 = s16(b0), s16(b1)
    t = s0 + (-s0) % 7
    tr = "leadw" if WAH else "lead"
    for turns, n, span, i0, steps in SOLO:
        idx = i0
        for k in range(n):
            if t + k * span / n < s1:
                add(tr, t + k * span / n, span / n * 1.05, SOLO_SCALE[idx % 6] + 12 * (idx // 6), vel * 0.86)
                RUN.append((t + k * span / n, span / n * 1.05, SOLO_SCALE[idx % 6] + 12 * (idx // 6), vel * 0.86))
            idx += steps[k]
        if t + span < s1:
            add(tr, t + span, min(turns * 7 - span - 0.3, s1 - t - span), SOLO_SCALE[idx % 6] + 12 * (idx // 6), vel)
            RUN.append((t + span, min(turns * 7 - span - 0.3, s1 - t - span), SOLO_SCALE[idx % 6] + 12 * (idx // 6), vel))
        if t < s1:          # the pedal opens through each flurry and closes slowly over the note it lands on
            WAH_PTS.extend([(t, 0.1), (min(t + span, s1), 1.0), (min(t + turns * 7 - 0.5, s1), 0.25)])
        t += turns * 7


RUN = []            # the run's notes as played (sixteenth, length, pitch, velocity), for its mirror (v45)


def solo_back(b0, src1, shift, vscale):
    """The run again, BACKWARDS, from bar b0: every note keeps its length and takes the place it would have in a mirror
    set at the run's end (so each flurry now falls away from its long note into the next), `shift` semitones away. The
    pedal's moves are mirrored with it."""
    tr = "leadw" if WAH else "lead"
    for t, ln, pitch, v in sorted(RUN, key=lambda q: -(q[0] + q[1])):
        add(tr, s16(b0) + (s16(src1) - (t + ln)), ln, pitch + shift, v * vscale)
    if WAH:
        src0 = min(t for t, _, _, _ in RUN)
        WAH_PTS.extend(sorted((s16(b0) + (s16(src1) - t), v) for t, v in list(WAH_PTS) if src0 <= t <= s16(src1)))


def chimes(b0, b1, pairs=((5, 7), (5, 11), (7, 11)), vel=0.5, motor=False):
    """Coincidences: wherever two wheels begin a turn on the same sixteenth, a struck bar sounds, one pitch to each
    pair (five and seven C, five and eleven Ab, seven and eleven F). All three coincide only at the first bar line
    and at the landing."""
    pitch = {(5, 7): 84, (5, 11): 80, (7, 11): 89}
    s0, s1 = s16(b0), s16(b1)
    for p, q in pairs:
        for t in range(s0 + (-s0) % (p * q), s1, p * q):
            if t % 385:
                if motor:
                    # One struck bar per pair. Its resonator turns with the
                    # wheel that DIDN'T meet, until that wheel comes round twice.
                    third, = {5, 7, 11} - {p, q}
                    release = min(s1 - t, (-t) % third + third)
                    add(f"bar{third}", t, release - .15, pitch[(p,q)] - 12, vel)
                else:
                    add("chime", t, 8, pitch[(p, q)], vel)


# v55: the opening's clean guitars meet again above the split and its swap.
# Gains for the five and seven, in dB. Empty regenerates v54 exactly.
RELAY = os.environ.get("C10T1_RELAY", "8;10")
# v56, eye only: motor-driven bars instead of the glock and its echo. Empty
# restores v55; RELAY='' alone still recovers v54, as the relay card promises.
EYE_BARS = os.environ.get("C10T1_EYE_BARS", "-14.5dB" if RELAY else "")


# v57: both five-bar stop-times have sixteen stabs, four of which land on
# quarters. Those four bear the hook in one direction, then the other.
STOP_HOOK = os.environ.get('C10T1_STOP_HOOK', '1' if EYE_BARS else '')
# The four resting places of the Long Wait, before the tune itself. Cellos'
# note trims in the opening and under the slow chords (dB). Empty restores v57.
RESTING = os.environ.get('C10T1_RESTING', '0;4' if STOP_HOOK else '')
# v59 (palette): the eleven wheel's tick comes back inside the heavy music.
# The ticks are the piece's first sound: three clean guitars, one to a
# wheel, in the wait, the eye and the approach, and nowhere else. In section
# 14 (bars 231-245, 7:20: seven on the guitars in double time) the eleven
# wheel is only held chords. An analog sequencer (the library's moog-seq,
# on no other song of the record) plays the eleven's own five ticks over
# them, the opening's notes on this section's ground, its filter opening as
# the section climbs to where all three wheels sound.
# Track gain ; semitones over the clean tick ; pan ; first and last velocity ;
# high-pass. First bench (-12 dB, high-pass 250): the patch's sub-octave
# square and its body put 0.8 dB on the section at 250-500 Hz and 1.6 at
# 500 Hz-1 kHz, where these guitars are already thick: so the sub is cut
# and the fader is 1.5 dB lower. Empty restores v58.
SEQ = os.environ.get('C10T1_SEQ', '-13.5dB;12;0;0.5;0.8;500' if RESTING else '')
# v60 (palette): HANDS ON THE SEVEN. Every section is made of the two wheels that have just met. Section 18 (bars
# 308-315, 9:46.7: "seven meets eleven", seven bars for the bass on the eleven wheel under one held chord, on A flat
# like the first break) sounded only one of them: the seven was nowhere but in the section's length. Now a pair of
# hands plays it, on congas and bongos (the library's `congas`, on no other song of the record, tuned here to the
# held chord's A flat and E flat): the FIRST BREAK'S OWN CELL (2:13: chug, chug, chug, hook), as tumba, muted tone,
# slap, and then a fourth stroke that steps down four drums in four turns as that break's hook steps down four notes
# (high bongo, low bongo, conga, tumba). Seven bars are sixteen turns of seven; the hands play fourteen and the head
# of the fifteenth, and stop where the toms' fill begins. They take the place of the snare's ghost strokes (the
# drummer's own hand-chatter in this section, 24 soft strokes); the hat, the backbeat, the kick and the bass are as
# they were. So for seven bars three clocks sound alone and can be told apart by what plays them: four on the hat
# and snare, seven on skin, eleven on the bass and the kick.
# (Raw, seed 0. First bench, the library's own balance: the tumba stood 0.7 dB OVER the whole mix in its first 60 ms
# and the slap 19 under, a 20 dB spread, so the cell read as two strokes, not four; the section gained 0.8 LU and
# 4.3 dB at 120-250 Hz. Kept: each drum's own trim, so the strokes sit 5 to 6 dB under the mix on the tumba, the
# conga and the bongos, 9 on the slap and 10 on the muted tone (the ghost strokes they replace stood 12 under); the
# hands as a whole 11.7 dB under the mix, the backbeat still 10 dB over the loudest of them; the section +0.3 LU,
# +1.6 dB at 120-250 Hz and +1.4 at 250-500.)
# track gain ; pan ; the tuning of tumba, muted tone, open conga, slap, low bongo, high bongo ; each one's trim, dB.
# Empty restores v59.
HANDS = os.environ.get('C10T1_HANDS', '-8dB;0.3;Eb3,Gb3,Ab3,Eb4,Eb4,Ab4;-7,0,-4,8,-4,-4' if SEQ else '')


def resting_places():
    """The four phrases end in a held note; their lengths are 5, 5, 5, 6 turns."""
    turns = 0
    for p, n in LONG_WAIT:
        turns += n
        if n > 1:
            yield p, turns
            turns = 0
    assert turns == 0


def bowed_rest(t, duration, pitch, trim):
    add('fifth', t, duration, pitch, .7)
    T['fifth'][-1]['gain'] = trim+'dB'


def quarter_stabs(start_bar, end_bar, returning=False):
    """Revoice just the inner pair. The low takes and all sixteen rests keep their shape."""
    if not STOP_HOOK:
        return
    on_grid = [t for t, *_ in strikes(5, FIVE_S, s16(start_bar), s16(end_bar)) if t % 4 == 0]
    hook = H1[::-1] if returning else H1
    assert len(on_grid) == len(hook)
    tops = dict(zip(on_grid, (F1 + 36 + h for h in hook)))
    for name in G2:
        tr = REAL_MAP.get(name, name) if REAL_FROM is not None and start_bar >= REAL_FROM else name
        for n in T[tr]:
            high = tops.get(round(4*n['at']))
            if high is not None:
                # First time, fret the hook above the open low F. In the
                # mirror, the high cluster briefly clears to that note in octaves.
                low = high - 12 if returning else F1
                n['pitch'] = f'{nm(low)},{nm(high)}'


def relay(b0, b1, returning=False):
    """Two next starts, one hook note: five picks it up, seven carries it."""
    if not RELAY:
        return
    # Leave the stop at the seam (half a bar) intact. At the split the first
    # two meetings go by with just the heavy band; at the swap the longer
    # hook fills all seven meetings and leads straight to riff A's return.
    start, stop = s16(b0), s16(b1 - .5)
    cycle = 5 * 7
    meets = list(range(start + (-start) % cycle, stop - 2 * 7 + 1, cycle))
    tune = HX if returning else H1
    assert len(meets) >= len(tune)
    for t, semis in zip(meets[-len(tune):], tune):
        low = F1 + 36 + semis
        # First pass rises left to right; returning, five is on the right
        # and high, seven on the left and low. No pan moves during a note.
        add("relay5", t + 5, 1.8, low + (12 if returning else 0), .90)
        add("relay7", t + 7, 7, low + (0 if returning else 12), .88)


def hands_on_seven(a, z):
    """v60: the seven wheel on congas through section 18, in the first break's cell; the snare's ghosts make room."""
    stop = z * 16 - FILL_LEN["toms"]
    assert (a * 16) % 7 == 0 and (z * 16) % 7 == 0
    ghosts = [n for n in T["snare"] if a * 4 <= n["at"] < z * 4 and n["vel"] < 0.5]
    T["snare"] = [n for n in T["snare"] if n not in ghosts]
    for t, ln, kind, j, hi in strikes(7, SEVEN_A, a * 16, stop):
        turn = (t - a * 16) // 7
        piece, vel = (("lo", 0.95), ("mu", 0.7), ("sl", 0.85), (("bh", "bl", "o", "lo")[turn % 4], 0.9))[j]
        add("hands", t, 1, piece, vel)
    return len(ghosts)


def chime_all(t, vel=0.7):
    for n in (77, 80, 84, 89):
        add("chime", t, 16, n, vel)


# ---- VOICES (Harry, 12 Nov: "try different options in different parts"). The bark, over the hardest stretch: it keeps
# the bar's own time, eighth-notes from the first beat of every second bar, while the band turns the seven wheel under it.
VOX_LINES = [
    ("W EY1 T", [4]),
    ("N AA1 T|Y EH1 T", [2, 4]),
    ("IY1 CH|W AH1 N|K IY1 P S|IH1 T S|OW1 N|K AW1 N T", [2, 2, 2, 2, 2, 4]),
    ("N AH1 N|AH0 V|DH EH1 M|R AO1 NG", [2, 2, 2, 6]),
    ("W EY1 T", [4]),
    ("N AA1 T|Y EH1 T", [2, 4]),
    ("DH EY1|D UW1|N AA1 T|N OW1|IY1 CH|AH1|DH ER0", [2, 2, 2, 2, 2, 2, 4]),
    ("S AH1 M|W EH1 R|AH0|HH EH1 D", [2, 2, 2, 6]),          # the ground has moved up a semitone
    ("W AH1 N|AW1|ER0", [4, 3, 3]),
    ("HH OW1 L D Z|DH EH1 M|AO1 L", [4, 4, 8]),
    ("K IY1 P|K AW1 N T", [2, 4]),
    ("K IY1 P|K AW1 N T", [2, 4]),
    ("K IY1 P|K AW1 N T", [2, 4]),
]


def say(tr, t, syllables, pitch=45, vel=0.8):
    """Spoken or whispered syllables from sixteenth t: (phonemes, length in sixteenths) each, end to end. The lengths are
    `chirp tts`'s for natural speech (a syllable about 0.4-0.57 s)."""
    for ph, ln in syllables:
        T.setdefault(tr, []).append({"at": round(t / 4, 4), "len": round(ln / 4, 4), "pitch": nm(pitch), "vel": vel, "ph": ph})
        t += ln


# two lines of the bark's text, SPOKEN first, calmly, as the band comes back after the eye (6:42); the bark screams them at 9:01.
# Syllables, lengths and the falling speaking pitch are `chirp tts --voice voice-talk --key F2 --speed 0.9 --print`'s
# (beats at 110 bpm: start, length, phonemes, pitch).
SPOKEN = [(211, [(0.25, 0.612, "IY1 CH", "m45.5"), (0.862, 0.794, "W AH1 N", "m44.9"), (1.657, 0.977, "K IY1 P S", "m44.3"),
                 (2.633, 0.794, "IH1 T S", "m43.7"), (3.428, 0.612, "OW1 N", "m43.1"), (4.04, 1.416, "K AW1 N T", "m40.5")]),     # Each one keeps its own count.
          (213, [(0.25, 0.794, "N AH1 N", "m45.5"), (1.044, 0.612, "AH1 V", "m44.5"), (1.657, 0.794, "DH EH1 M", "m43.5"),
                 (2.451, 1.152, "R AO1 NG", "m40.5")])]                                                                        # None of them wrong.


def speak(tr, lines, vel=0.8):
    k = 126 / 110 * 4          # a beat at 110 bpm, in this piece's sixteenths
    for bar, notes in lines:
        for at, ln, ph, pitch in notes:
            T.setdefault(tr, []).append({"at": round((bar * 16 + (at - 0.25) * k) / 4, 4), "len": round(ln * k / 4, 4), "pitch": pitch, "vel": vel, "ph": ph})


def vox(b0, pitch=65):
    for i, (line, lens) in enumerate(VOX_LINES):
        t = (b0 + 2 * i) * 16
        up = 1 if 14 <= 2 * i < 21 else 0
        for ph, ln in zip(line.split("|"), lens):
            T.setdefault("vox", []).append({"at": round(t / 4, 4), "len": round(ln * 0.9 / 4, 4), "pitch": nm(pitch + up), "vel": 0.9, "ph": ph})
            t += ln


def hit(t, ln=32, vel=1.0):
    for tr in ("gl", "gr", "gl2", "gr2", "wl", "wr") + (("sl", "sr") if BITE_L else ()):
        add(tr, t, ln, "F1,C2,F2,C3", vel)
    add("bass", t, ln, "F1", vel)
    add("kick", t, 1, "k", 1.0)
    crash(t, 1.0)
    crash(t, 0.9, "x")


G = ("gl", "gr")
G2 = ("gl2", "gr2")
WL = ("wl", "wr")      # the wall rig: eleven's open chords, riff C, every chord that is left to ring


# v38: THE BREAK OPENS ON ONE GUITAR. For this many bars at the top of the seven break (2:13) the bass, the kick and the
# snare's backbeat stay out: the low-gain guitar, its hand and its spring, alone with the hat and the snare's ghost
# strokes. Then bass, kick and backbeat; then the second guitar. "" or 0 = v37 (everything from the first bar).
# v46: Harry, on the Questions page: "A hole". The band plays from the break's first bar again (v38-v45: 2).
BREAK_ALONE = int(os.environ.get("C10T1_BREAK", "0") or 0)


# v39: WHEN ELEVEN ARRIVES, THE CYMBAL GOES WITH IT (1:44-2:13). From 1:06 to 2:13 the kit played one pattern for 35 bars
# (china on every quarter, snare on three) while the guitars changed under it. In the section where eleven first arrives
# as chords, the china now strikes WITH each chord, every eleven sixteenths, as a drummer hits a cymbal with a big chord;
# the ride's edge keeps the quarters under it and the snare stays on three. So the kit itself carries three clocks
# there: the kick on five, the china on eleven, the ride and snare on the bar. The ride's edge is the cymbal of this
# section's mirror (the swap, 10:00), so the two now share it. A closed hat was tried first as the pulse (0.55): it read
# 20.6 dB under the mix and never near it, and the one steady pulse must not go missing.
# the pulse's piece : velocity ; the china's velocity on each chord. "" = v38.
ELEVCYM = os.environ.get("C10T1_ELEVCYM", "rde:0.5;0.8")
# Tried in the same round and not taken: the snare on two and four for riff A's last five bars (C10T1_RIFFA=15). It
# spends the piece's first backbeat, which belongs to the split at 4:26.
RIFFA_BACK = int(os.environ.get("C10T1_RIFFA", "") or 0)
# v39: THE KIT'S TOP FALLS AS THE RECORDS' DOES (chirp-eco's reading by thirds on both songs: level with eight records to
# 11.6 kHz, then ours stayed flat where theirs fall, +1.6 dB at 11.6-13.7 kHz, +4.7 at 13.7-16, +7.4 at 16-20; every piece
# of the kit carried it, and the bark's hiss). One second-order low-pass on the drums' bus, the overheads' bus and the
# bark. Fitted by the records read the same way as the piece (gspec, each band against its own 2-8 kHz; eleven records'
# median -15.9 -20.2 -23.1 -27.5 -32.5 for 8-10 / 10-11.6 / 11.6-13.7 / 13.7-16 / 16-20 kHz; v38 -18.0 -22.0 -23.0 -24.4
# -24.2): the wanted change is 0 0 0 -3.1 -8.3 dB. A fourth-order low-pass at 14.5 kHz was too steep (16-20 kHz ended
# 5.8 dB UNDER the records); Odd Sympathy's 14.5 kHz q 0.7 takes 1.4 dB from 11.6-13.7 kHz that is not owed; this one
# (a little resonant) takes 0.6 there. Hz ; q. "" = v38.
DTOP = os.environ.get("C10T1_DTOP", "14250;0.8")
DTOP_BANDS = [f"lp cutoff={DTOP.split(';')[0]} q={DTOP.split(';')[1]}"] if DTOP else []


# v40: RIFF C SPLAYS (4:11-4:26). The brief asks for a motif that gets splayed; riff C is the long one, on eleven. In its
# last eight bars, back on F, the guitars pull its hook apart: for four bars every other note of the hook (Ab Gb B C)
# goes up an octave (Ab, Gb an octave up, B, C an octave up: leaps of a seventh and a ninth where there were steps);
# for the last four every note of it is up, by one octave and two in turn (Ab2, Gb3, B2, C4), over chugs still on the
# low F. The bass and the synth keep the hook as it was, so the guitars are heard leaving the bass and arriving where
# the synth is (its Gb3 and C4); the split that follows is an octave up, and the splay lands there.
# For those last four bars the open chords stop: with them ringing (two more guitars, as loud as the riff's) the leaps
# were an inner detail; without them the riff is alone as it was when it began (3:29), now pulled wide.
# the hook for the first bars ; for the rest ; how many bars the first lasts ; 1 = the open chords stop for the rest. "" = v39.
SPLAY = os.environ.get("C10T1_SPLAY", "3,13,6,19;15,25,18,31;4;1")


# v41: THE SNARE GETS ITS CRACK BACK (whole song). Since v10 the snare went into the overheads' room almost as loud as it
# went to the drums' bus (send -1.5 dB, a bright 0.7 s room). Measured alone through its buses (drumpunch.py, riff A):
# its peak stood only 7.8 dB over its own body 20-50 ms later and it took 125 ms to fall 20 dB; the records' snares
# stand 12.2 (The Faultless) and 17.9 dB (Bleed) over theirs and fall in 12 to 22 ms. The room was the tail: with the
# send at -12 dB the snare stands 12.0 dB over its body and falls in 50 ms. A transient shaper on the track did less
# (10.9 dB with the send cut, nothing without: the tail was not the drum's), a gate the same as no gate.
# BUT THE ROOM WAS ALSO MOST OF THE SNARE'S LEVEL: the drums' bus is clipped at -13 dB and the room is not, so the
# snare's peak reached the mix through the room (alone: -5.1 dBFS with it, -11.4 without; 3.8 LU quieter). Pushing the
# track 4 dB harder into the clip gave half of it back and blunted it (punch 10.1). A room of its own, short (0.15 s),
# kept the level and the blur (punch 8.6). What works is a DRY path beside the clipped bus (bus `snr`, no effect):
# at -12 dB the snare alone is as loud as it was (-23.3 against -22.9 LUFS) with a peak 3 dB LOWER, stands 11.6 dB over
# its body and falls in 55 ms, and has its body back (150-300 Hz against 1.5-5 kHz: -5.6 -> +3.3 dB; the records +13 and -3).
# effects on the snare's track, | between ; its send to the overheads' room, dB ("" = none) ; its gain ;
# its own bus beside the drums' (a room's decay, or "dry") : the send to it, dB. "" = v40.
# In the mix, with its tail gone, the snare then read 0.7 to 1.5 dB LOUDER against the mix while it sounds (presence:
# riff A -6.9 -> -6.2, the hardest stretch -7.5 -> -6.6, the landing -8.4 -> -6.9) and was the loudest track in all
# three; its track comes down 1 dB so that it leads less.
# A shelf on the snare's track (2 dB off above 7 kHz): out of the room its wires stood 1.5 dB over its crack (the
# records -0.8 and +0.9; now +0.6), and the mix's loud frames read 0.4 to 0.8 dB more at 8-16 kHz against the records.
SNARE = os.environ.get("C10T1_SNARE", "shelf:7000:-2;-1.5;5.25dB;dry:-10")        # v41-v45: shelf:7000:-2;-12;7dB;dry:-10
# v42: THE MACHINE APPROACHES (0:57-1:06). The wait's last five bars were written as "the machine, approaching": the
# guitars and the bass play riff A from bar 30 with their velocity rising from 0.45 to 0.9. Through a saturated rig
# velocity does nothing: the guitars alone read -24.5 dB at bar 30 and -24.6 at bar 35, the mix jumped 5.3 dB at bar
# 30 and 0.8 at bar 35, and the whisper's "not yet" (0:56) was answered by the whole riff at full level a second later.
# The landing of the wait was spent five bars early. Now the approach is a fader move: the guitars' and the bass's
# buses rise from far down at the first bar to a little under full at the last, and step up to full on the bar line
# with the crash: the machine comes near, and then the band LANDS at 1:06. Two shapes were tried first: a rise from -18
# dB all the way to full (the mix then rose only 1.7 dB at the landing), and from -20 to -6 dB (a 3.7 dB landing, but
# the guitars sat 16 to 23 dB under the ticks for the first three bars: not an approach anyone would hear).
# first bar : last bar : dB at the start : dB just before the landing. "" = v41.
APPROACH = os.environ.get("C10T1_APPROACH", "30:35:-12:-4")
# v43: THE WEIGHT COMES BACK (6:40-6:59). The rebuild after the eye was written the same way: "the weight comes back",
# the five wheel's velocity rising 0.6 -> 1.0 over its ten bars. It did nothing either: the guitars alone read -24.9 dB
# in the first bar and -24.7 in the last (and 6 dB less under the spoken voice, which is the duck). So the band came
# back at full weight on the first bar line. The form is a palindrome and this section's mirror is the slow chords
# that die away into the eye (5:14); now the rebuild rises out of it: the guitars' and the bass's buses come in this
# many dB down and reach full at the section's end, where eleven lands on Bb. The toms and the kick stay as they
# were, so the rebuild is led by the toms, as its plan always said.
# first bar : last bar : dB at the start. "" = v42.
REBUILD = os.environ.get("C10T1_REBUILD", "210:220:-8")
# v61: THE BAND COMES NEAR (whole-song round, 11:31-12:13). The piece is a wait of 385 bars for one bar line, and the
# bar it waits for was not its largest moment. chirper-one read the finished file by section (18 Nov 23:28): the
# landing's four chords stood 0.2 dB UNDER the double time that leads to them and 0.3 under riff A coming home, and
# every loud section from 1:07 to 12:40 within 0.7 dB of every other. Read raw, the reason is in two places. The
# band that comes in at bar 363 is already whole (eight guitar tracks, the bass, the kit, the lead) and holds one
# level for twenty bars: the mix reads -18.3 dB in its half time and -18.1 in its double time, K-weighted, against
# riff A's -18.0. And the landing's chord, which the mix does put 0.9 dB over that, has the piece's tallest peaks
# (everything strikes at once), so the limiter takes 1.2 dB from it where it takes 0.4 from the approach. Nothing
# can be given back at the landing. So what leads to it is made smaller, with the device this piece already has: at
# 0:57 the machine approaches on the guitars' and the bass's faders (v42), and after the eye the weight comes back
# on them (v43). Now the last approach does what its name says. The band comes in at bar 363 at a distance, under
# the kit and the lead's tune, and comes nearer through the half time and the double time; it is still short of
# full when it stops at bar 383; two bars of ticks; and the landing is the first time since riff A came home that
# the whole band is at full weight. No note changes; the kit, the lead, the ticks and the pads are as they were, so
# for these twenty bars the drummer and the tune lead and the guitars arrive under them.
# first bar : last bar : dB on the guitars' and the bass's buses at the first : dB at the last : the loudness target
# (those twenty bars are quieter, so the whole piece measures a little lower; with the target left at -10 every other
# bar would be turned up into the limiter to make it good. Fitted on the eye, which the limiter does not touch: at
# -10.138 it came out 0.084 dB lower than v60 and at -10.054 0.072 higher; the gain moves 1.86 dB for each dB of
# target, the limiter being inside the loop). "" = v60.
NEARER = os.environ.get("C10T1_NEARER", "363:383:-6:-3:-10.093" if REBUILD and HANDS else "")
# v63 (chirper-one; section round, the map's w16, 7:37-8:07, flagged static and "little new" and never focused; the change
# is 7:46.7-8:15.0): WHERE ALL THREE WHEELS ARE PLAYED, THEIR MEETINGS RING. The glock marks every coincidence of two
# wheels (five and seven C, five and eleven A flat, seven and eleven F) wherever the wheels only TICK: the wait, the
# eye (on the vibraphone since v56), the approach, the ending. Section 15 is the one place the band plays all three at
# once (five in the left guitar, seven in the right, eleven in the bass and the tune), and there the meetings went by
# unmarked: fifteen of them in its first fifteen bars, while the tune is played alone. Now each rings, and rings
# BETWEEN THE TWO THAT MET: five and seven in the middle (the guitars are hard left and right), five and eleven half
# left (the left guitar and the bass), seven and eleven half right. The section's first bar line is itself a meeting
# of five and seven, so the first bell is its downbeat. And the tune is 21 turns of eleven long, which is 33 turns of
# seven: so the seven-and-eleven bell (F) rings on the tune's first note, a third of the way through it, two thirds,
# and on the first note of its second pass (8:15.0), where the second lead joins in thirds (v52) and the bells stop.
# Every A flat and F bell falls where a turn of eleven begins, which is where the tune's notes begin.
# The stroke is the opening's (velocity 0.5); it stands 7 dB over the opening's fader because here it has a band to be
# heard through. Benched raw, the bells alone against everything else, stroke by stroke: the bell's strongest partial
# stands a median 3.1 dB OVER everything else in the third-octave round it (-6.9 to +4.4), and the stroke 7.8 dB UNDER
# the whole band (K, first 100 ms; v59's sequencer, the section before, stands 10.6 to 13.1 under). At the opening's
# fader they read -4.6 and -15.4: at the edge of being heard at all. The A flat bells carry 1.5 dB more: their
# third-octave (830 Hz) is where the guitars are thickest.
# Three new tracks (meet57, meet511, meet711: the glock, one seat each), fifteen strokes; nothing else is changed.
# bars from the section's first ; the bell's velocity ; the bells' fader ; dB on the strokes of each pair (five and seven,
# five and eleven, seven and eleven) ; where each pair's bell stands (pan) ; the loudness target ('' = unchanged).
# "" = v62. It is on only while no older switch of this song is set, so each of those still gives what it gave.
MEET = os.environ.get("C10T1_MEET", "15;0.5;-12dB;0,1.5,0;0,-0.5,0.5;" if not any(k.startswith("C10T1_") and k not in ("C10T1_OUT", "C10T1_SHOW", "C10T1_MEET", "C10T1_TAPE", "C10T1_FINISH", "C10T1_SKIN", "C10T1_HUM", "C10T1_STROKE", "C10T1_FIVE") for k in os.environ) else "")
# v44: THE ENGINE, EXPOSED (9:19, in the hardest stretch). For twenty-eight bars everything runs at once: four guitars
# and the bass on seven, the china on every eighth, the bark, and under it all the kick in unbroken sixteenths. The one
# event inside it is the ground moving up a semitone at 9:20. Now, for the half bar before that, everything stops
# except the kick: eight sixteenths of the kick alone, the machine with its cover off, and then the crash and the lift.
# The pulse is not broken (the kick is the pulse); a rest is a rest.
# the bar : the sixteenth from which everything but the kick rests. "" = v43.
# v47: THE RIFF ASSEMBLES ITSELF, AND THE SPRING IS HEARD (section round, 11:19-11:30). Harry, on the Questions page,
# of the spring's drip on the low-gain guitars: "I cannot hear it in the piece". It could not be: a spring drips after
# a short note with nothing after it, and both places it played were riffs with no rest in them. Now the approach's
# first guitar (the seven wheel's, on the right, at 11:19) does not come in as a riff. It comes in as ONE muted note to
# each turn of its wheel, three times, alone over the ticks and the heartbeat, with two thirds of a second between
# them for the spring to answer; then two notes a turn, then three, then four, then the whole riff. The five wheel's
# guitar on the left does the same from 11:25, faster. The approach was already things arriving one at a time; now
# the riffs themselves arrive a note at a time.
# And they arrive from inside the spring: while a guitar's notes come alone its spring is far wetter (the last field;
# 0.2 everywhere else), and it dries to what it was as the riff fills in: the guitar comes nearer. The bass, which
# came in with the first guitar, waits two bars, so the first lone notes have only the ticks and the heartbeat by them.
# for the seven wheel's guitar: turns : which of its cell's notes sound ; ... (then the whole cell) | the same for the
# five wheel's guitar | the spring's mix while the notes come alone. "" = v46.
# v48: ELEVEN ARRIVES ALONE (section round, 1:44-1:54; the section map called 1:31-2:01 the most static window of the
# song, though a whole new wheel arrives in the middle of it). Eleven came in as open chords UNDER the five wheel's
# riff, which went straight on: nothing got out of its way, so the arrival was a thickening. Now, when eleven's first
# chord lands (1:44), the two guitars of the five wheel REST for five bars. The bass and the kick go on turning five;
# the wall guitars ring eleven's chords over them, the china striking with each chord (which Harry kept: "Harder, and
# I still feel the bar"). So for ten seconds you hear the two wheels against each other with nothing else: five in
# the rhythm section, eleven in the guitars. Then the five wheel's guitars come back where five next meets a bar line
# (1:54), on a crash, and the section is as it was.
# For those bars the wall guitars' faders come up (the third field, dB): alone over the rhythm section they stood under
# the kick and the bass (wl -8.4 by presence, the kick -4.8), and the arrival was 1.9 dB quieter than the riff before it.
# bars the five wheel's guitars rest when eleven arrives (a multiple of five) ; the crash they come back on ; the wall
# guitars' lift in those bars, dB. "" = v47.
ELEVALONE = os.environ.get("C10T1_ELEVALONE", "5;0.85;3")
# v49: IN RIFF B THE CYMBAL FINDS THE BASS'S WHEEL (section round, 2:40-2:53; the map's window 2:32-3:02 had never had
# a round, and it called it static). Riff B is "seven meets eleven": the guitars and the kick turn seven, the bass
# turns eleven under them, and nothing says so: for its first fourteen bars a ride bell counts quarters. Riff A's rule
# was that at every landing something joins; riff B's second landing (bar 84, 2:40) had nothing. Now, from there, the
# CHINA strikes where the bass's eleven begins each turn (every eleven sixteenths), over the ride bell's quarters: the
# move Harry kept at 1:44 ("Harder, and I still feel the bar"), here for a wheel only the bass is playing. Seven bars
# later the lead comes in with its tune, which is one note to each turn of eleven: the cymbal has been marking the
# tune's own clock before the tune arrives, and hands it over (the china goes to the quarters at 2:53, as it did).
# bars into riff B where it starts (a landing of seven) ; the china's velocity. "" = v48.
SEVCYM = os.environ.get("C10T1_SEVCYM", "7;0.58")
ASSEMBLE = os.environ.get("C10T1_ASSEMBLE", "3:0;2:0,2;2:0,1,2;2:0,1,2,4|2:0;2:0,3|0.7")
LONE = float(os.environ.get("C10T1_LONE", "1.8"))        # how much harder a note alone is struck
HOLE = os.environ.get("C10T1_HOLE", "293:8:all")        # v44-v45: 293:8 (the kick went on alone)
# v46: HARRY'S ANSWERS (whole piece). On 14 Nov, 16:12-17:40 GMT, Harry answered the Questions page. Four of his answers
# on this piece say what to do, and each is done (his words in quotes):
#   1. THE SNARE, "Too dry: it lost its air". v41 took the snare out of the cymbals' room (its send to `oh` -1.5 -> -12 dB)
#      because that send is a path round the drums' clip, and read the result against two records' snares. His ear says
#      the path was the snare's air. The send is back at -1.5 dB. The dry path beside it (the crack) stays, and the
#      track comes down 1.75 dB so the snare sits where it sat (C10T1_SNARE's second and third fields). He heard the
#      same mend on Odd Sympathy v17 first: "Now: the air is back".
#   2. THE HOLE AT 9:19, "The kick alone sounds wrong". The half bar before the ground moves up is a rest for the whole
#      band now, the kick too: half a bar of nothing but what is still ringing, then the crash and the lift
#      (C10T1_HOLE's third field, `all`).
#   3. THE LANDING RIFF, "double track em". Each side had one guitar and a second 5.5 dB under it on the same rig. Now
#      each side is TWO guitars at one level: the one it had (the `gojira` amp) and a second take through another amp
#      (`5150`), another microphone place and another cone, a little inside it (C10T1_DOUBLE).
#   4. THE SEVEN BREAK AT 2:13, "A hole". It opened on one guitar alone for two bars (v38); the bass, the kick and the
#      backbeat play from its first bar again (C10T1_BREAK, above).
# the doubles' amp ; microphone , left cone , right cone ; pan ; their trim over the tight rig's, dB, left , right ;
# a trim on all four so the landing riff's guitars are as loud as they were. "" = v45.
# The second amp is thicker at 160-320 Hz (3 dB over the first, alone), where the landing riff already stood over the
# records; one eq band on the second takes puts them level with the first there (the last field: Hz : q : dB).
DOUBLE = os.environ.get("C10T1_DOUBLE", "5150;0.4,8,9;0.75;0.5,1.5;-1.9;230:1.1:-3.5")
# v54: EVERY RIFF IS DOUBLE-TRACKED (Harry, 17 Nov 00:25, asked whether the landing riff's two takes a side through two
# amps were the double-tracking he meant: "Yes: do it to the other riffs too"). Until now only the landing riff had it.
# Every other riff was one guitar a side (the second pair, where it played, played something else: the hook an octave
# up, eleven's chords). Now each guitar of the three heavy rigs has a SECOND TAKE beside it: the same part played again
# (its own track, so its own timing and picking), through the second guitarist's amp, the `5150` the landing's doubles
# use, on another microphone place and another cone, a little inside the first. Where a side plays its own wheel (five
# on the left and seven on the right) each side's wheel is doubled on its own side.
#   - Not doubled: the low-gain rig (the seven break and the approach's first guitars are ONE guitar on purpose), the
#     second pair's harmonies and chords, and the two stretches where the second pair already plays the first pair's
#     notes (the stop-time at 3:20 and the hardest stretch, 8:53): there the four are the double.
#   - THE PAIR WEIGHS WHAT THE ONE DID: each rig's two takes together are trimmed to the loudness of its one before,
#     so no riff is louder for being doubled; it is wider and thicker.
# the doubles' amp ; microphone ; cones left , right for the tight rig ; for seven's rig ; for the wall rig ; pan
# (the wall's are scaled as its first takes are) ; the doubles' trim over their first take, dB, left , right, for the
# tight rig ; seven's ; the wall ; each rig's trim on all its takes where the doubles play, dB (tight ; seven's ;
# wall) ; an eq band on each rig's doubles (Hz : q : dB, as the landing's; tight , seven's , wall; empty = none).
# "" = v53.
DBL = os.environ.get("C10T1_DBL", "5150;0.33;4,5;10,11;16,17;0.75;0.8,0.7;-0.2,-0.4;1.0,0.8;-3;-3;-3;230:1.1:-3.5,230:1.1:-3.5,330:1:-3")
DBL_MAP = {"gl": "dgl", "gr": "dgr", "rl": "drl", "rr": "drr", "sl": "dsl", "sr": "dsr", "wl": "dwl", "wr": "dwr"} if DBL else {}
DBL_EXCL = []          # (bar, bar): where the second pair plays the first pair's notes (filled by gtr)
# v45: THE RUN, BACKWARDS (6:59-7:20). The form is a palindrome: 35 20 15 7 28 5 30 14 11 10 | the eye | 10 11 14 30 ...
# and each section has a mirror. The lead's run (4:53-5:14, eleven bars, on Db) is the one melody of the first half, and
# its mirror, eleven bars on Bb, had no lead at all. Now the run comes back there BACKWARDS, note for note: the same
# notes with the same lengths, set in a mirror, a minor third lower (Db to Bb), with the wah pedal's moves mirrored too.
# Forwards each flurry climbs to a long held note; backwards each long note comes first and the flurry falls away from
# it into the next. It is the one place in the piece where the palindrome is heard in a tune.
# At the run's own level the mirror was a second solo: the lead 3 dB over everything and the section 1.5 dB louder on
# the groove. It sits 3 dB lower than the run (a fader on the lead's track): a thing remembered, not a second solo.
# semitones the mirror is moved by ; its velocity against the run's ; its level against the run's, dB. "" = v44.
RETRO = os.environ.get("C10T1_RETRO", "-3;1.0;-3")
# the dry path's eq. Without one it carried the snare's body past the drums' bus's own 400 Hz cut, and every section read
# 0.5 to 1.4 dB more at 250-500 Hz against the records (the split +1.9 -> +2.8, the landing +1.1 -> +1.9). With this cut
# (and the send 2 dB up) the snare alone carries as much at 250-500 Hz as it did at v40, and 1.1 dB more at 120-250 Hz.
SNARE_EQ = os.environ.get("C10T1_SNAREEQ", "300:0.7:-12")


def compose():
    B = BOUNDS
    F_ONLY = [(0, 0)]

    # 1. 0-35  THE WAIT BEGINS: everything strikes once, together; then only the wheels, ticking, one by one
    hit(0)
    bed(F_ONLY, 35 * 16)
    if RESTING:
        # The lower cello keeps its C. Take two bows out of the sustained
        # upper F and give it the phrase endings, an octave low on the five
        # clock. It comes back to the bed before the first whispered 'wait'.
        ends = tuple(resting_places())
        opening_trim, return_trim = RESTING.split(';')
        t = 5 * 16
        T['fifth'] = [n for n in T['fifth'] if not (4*16 <= n['at']*4 < 12*16 and n['pitch'] == nm(F1+12))]
        for p, turns in ends:
            bowed_rest(t, 5*turns-.6, p-12, opening_trim)
            t += 5*turns
        assert t <= 12*16
    tick("cl5", 5, TICK5, CL5, 2, 35)
    tick("cl7", 7, TICK7, CL7, 14, 35)                              # enters where seven meets a bar line
    tick("cl11", 11, TICK11, CL11, 22, 35, vel=0.36)                # and eleven where it does
    for t in range(16 * 16, 35 * 16 - 8, 4):
        add("cym", t, 4, "rb", 0.3 * (1.12 if t % 16 == 0 else 1.0))
    kick(4, [(0, 1, "c")], 27, 35, vel=0.45)                         # a heartbeat on the quarter
    gtr(G, 5, FIVE_A, 30, 35, hook=GROW[0], vel=0.8, ramp=(0.45, 0.9))   # the machine, approaching, with one note of its hook
    bass(5, FIVE_A, 30, 35, hook=GROW[0], vel=0.8, ramp=(0.45, 0.9))
    if SWARM:                                                       # the swarm: in step at bar 1, then drifting apart
        for n in SWARM_NOTES:
            add("swarm", 0, 30 * 16, n, 0.7)
    if WHISPER:                                                     # a whisper before each new part comes in
        say("whisper", 13 * 16 + 8, [("W EY1 T", 4.75)])
        say("whisper", 21 * 16 + 8, [("W EY1 T", 4.75)])
        say("whisper", 29 * 16 + 6, [("N AA1 T", 3.3), ("Y EH1 T", 4.75)])
    chime_all(0)
    chimes(14, 35, pairs=((5, 7),))                                 # coincidences sound once both wheels are ticking
    chimes(22, 35, pairs=((5, 11), (7, 11)))
    fill(35, "roll")
    rise(35, 2)

    # 2. 35-55  five and seven have met: RIFF A, the five wheel. Every five bars it lands on a bar line, its hook gains a
    #    note (Ab; Ab Gb; Ab Gb B; Ab Gb B C) and something joins
    a, z = B[1], B[2]
    for i, hk in enumerate(GROW):                                    # the hook gains a note at each landing
        gtr(G, 5, FIVE_A, a + 5 * i, a + 5 * i + 5, hook=hk)
        bass(5, FIVE_A, a + 5 * i, a + 5 * i + 5, hook=hk)
    kick(5, FIVE_A, a, z)
    harm(("gl2",), 5, FIVE_A, a + 5, a + 10, 12, hook=GROW[1])       # second landing: the hook an octave up, on the left
    harm(G2, 5, FIVE_A, a + 10, a + 15, 12, hook=GROW[2])            # third: on both sides
    harm(G2, 5, FIVE_A, a + 15, z, 19, hook=H1)                      # fourth: an octave and a fifth up
    if RIFFA_BACK:                                                  # v39: at the fourth landing, the hook complete, the beat opens: snare on two and four
        kit(a, a + RIFFA_BACK, "x", 4, "half", None)
        kit(a + RIFFA_BACK, z, "x", 4, "back", "roll", crash_at_start=False)
    else:
        kit(a, z, "x", 4, "half", "roll")
    for t in landings(5, a * 16 + 1, z * 16):
        crash(t, 0.8)

    # 3. 55-70  five meets eleven: the five wheel thickens, and eleven arrives as open chords left to ring
    a, z = B[2], B[3]
    n5 = int(ELEVALONE.split(";")[0]) if ELEVALONE else 0
    assert n5 % 5 == 0
    gtr(G, 5, FIVE_B, a + n5, z, hook=H1)                              # v48: eleven arrives alone; five's guitars come back on five's next landing
    if n5:
        crash((a + n5) * 16, float(ELEVALONE.split(";")[1]))
    gtr(WL, 11, ELEVEN_W, a, a + 11, vel=0.9)
    gtr(WL, 11, [(0, 8, "P"), (8, 2, "d")], a + 11, z, vel=0.9)       # after eleven lands, each chord is answered by a stab
    bass(5, FIVE_A, a, z, hook=H1)
    kick(5, FIVE_B, a, z)
    if ELEVCYM:                                                       # v39: the china strikes with each of eleven's chords; a hat keeps the quarters
        (piece, pv), cv = ELEVCYM.split(";")[0].split(":"), float(ELEVCYM.split(";")[1])
        kit(a, z, piece, 4, "half", "toms", cvel=float(pv))
        for t, ln, kind, j, hi in strikes(11, ELEVEN_W, s16(a), s16(z) - FILL_LEN["toms"]):
            if t % 16 and t != s16(a):                                # (where a chord meets a bar line the crash below has it)
                add("cym", t, 8, "x", cv)
    else:
        kit(a, z, "x", 4, "half", "toms")
    for t in landings(11, a * 16 + 1, z * 16):
        crash(t, 0.85)

    # 4. 70-77  five and seven meet: seven bars of the seven wheel, nearly alone (one guitar, bass, kick, ghosted snare), up on Ab
    a, z = B[3], B[4]
    gtr(("gl",), 7, SEVEN_A, a, z, root=AB, hook=H2, vel=0.8, rig=CRUNCH, dyn=SOFT)       # on the low-gain rig: the chugs soft, the hook hard
    gtr(("gr",), 7, SEVEN_A, a + 4, z, root=AB, hook=H2, vel=0.8, rig=CRUNCH, dyn=SOFT)
    bass(7, SEVEN_A, a + BREAK_ALONE, z, root=AB, hook=H2)          # v38: the break opens on the guitar and its spring alone (BREAK)
    kick(7, SEVEN_A, a + BREAK_ALONE, z)
    kit(a, z, "h", 2, "half", "kicks", cvel=0.5, ghost=True, crash_at_start=False)
    if BREAK_ALONE:                                                 # ... and the snare only ghosts there: its backbeat comes in with the bass and kick
        T["snare"] = [n for n in T["snare"] if not (a * 4 <= n["at"] < (a + BREAK_ALONE) * 4 and n["vel"] > 0.5)]
    crash(a * 16, 0.7, "sp")

    # 5. 77-105  seven meets eleven: RIFF B, guitars on seven, the bass on eleven; the lead's tune arrives halfway
    a, z = B[4], B[5]
    gtr(G, 7, SEVEN_B, a, z, hook=H2)
    bass(11, ELEVEN_A, a, z, hook=OCT)
    kick(7, SEVEN_B, a, z)
    kit(a, a + 14, "rb", 4, "half", None, cvel=0.6)
    if SEVCYM:                                                        # v49: the china finds the bass's eleven, until the tune takes it over
        for t, ln, kind, j, hi in strikes(11, ELEVEN_A, s16(a + int(SEVCYM.split(";")[0])), s16(a + 14)):
            if j == 0:
                add("cym", t, 8, "x", float(SEVCYM.split(";")[1]))
    kit(a + 14, z, "x", 4, "half", "run")
    long_wait(a + 14, z)
    harm(G2, 7, SEVEN_B, a + 21, z, 12, hook=H2, vel=0.75)            # the last seven bars: the hook doubled an octave up
    for t in landings(7, a * 16 + 1, z * 16):
        crash(t, 0.8)

    # 6. 105-110  five and seven meet: stop-time. Sixteen stabs on the five wheel, silence between
    a, z = B[5], B[6]
    gtr(G + G2, 5, FIVE_S, a, z, vel=0.95)
    quarter_stabs(a, z)
    bass(5, FIVE_S, a, z, vel=0.95)
    kick(5, FIVE_S, a, z, vel=0.95)
    for t, ln, kind, j, hi in strikes(5, FIVE_S, a * 16, z * 16):
        add("cym", t, 2, "cch", 0.75)
    rise(z, 1)

    # 7. 110-140  five meets eleven: RIFF C, the splayed one. Eleven everywhere for eleven bars; then the kick slips onto five
    a, z = B[6], B[7]
    for (x, y, root, hook) in ((a, a + 11, F1, H1), (a + 11, a + 22, F1 + 5, H3), (a + 22, z, F1, H1)):
        if SPLAY and x == a + 22:                                       # v40: in its last eight bars the hook is pulled apart
            h1, h2, nb = [int(v) for v in SPLAY.split(";")[0].split(",")], [int(v) for v in SPLAY.split(";")[1].split(",")], int(SPLAY.split(";")[2])
            gtr(WL, 11, ELEVEN_A, x, x + nb, root=root, hook=h1)
            gtr(WL, 11, ELEVEN_A, x + nb, y, root=root, hook=h2)
        else:
            gtr(WL, 11, ELEVEN_A, x, y, root=root, hook=hook)           # the riff itself on the wall rig, alone at first
        if x > a:
            stop = x + int(SPLAY.split(";")[2]) if SPLAY and x == a + 22 and SPLAY.split(";")[3:] == ["1"] else y
            gtr(G2, 11, ELEVEN_W, x, stop, root=root, vel=0.9)          # the open chords join when the ground moves (v40: and stop where the full splay begins)
        bass(11, ELEVEN_A, x, y, root=root, hook=hook)
        if CZ:
            layer("cz", 11, ELEVEN_A, x, y, root=root, hook=hook)      # a phase-distortion synth doubles riff C two octaves up
        if x > a:
            crash(x * 16, 0.9)
    kick(11, ELEVEN_A, a, a + 11)
    kick(5, FIVE_A, a + 11, z)
    kit(a, z, "x", 8, "half", "run16", cvel=0.7)

    # 8. 140-154  five meets seven: both at once. Five in the left guitar, seven in the right, an octave up; double time
    a, z = B[7], B[8]
    gtr(("gl",), 5, FIVE_B, a, z - 0.5, root=F1 + 12, hook=H1)
    gtr(("gr",), 7, SEVEN_B, a, z - 0.5, root=F1 + 12, hook=H2)
    bass(7, SEVEN_B, a, z - 0.5, hook=H2)                             # with the right guitar, an octave below it
    kick(5, FIVE_B, a, z - 0.5)
    kit(a, z, "h", 2, "back", "stop", cvel=0.5, ghost=True)
    relay(a, z)

    # 9. 154-165  seven meets eleven: the lead runs on the seven wheel while the bass turns eleven; the ground moves to Db
    a, z = B[8], B[9]
    gtr(G, 7, SEVEN_A, a, z, root=DB, hook=H2)
    bass(11, ELEVEN_A, a, z, root=DB, hook=OCT)
    kick(7, SEVEN_A, a, z)
    kit(a, z, "rd", 4, "half", "run", cvel=0.6)
    if ELEVEN9:                          # v51: the eleven wheel gets a body: the toms turn it with the bass
        lo, hi, v0, v1, g = ELEVEN9.split(";")
        snares = {round(n["at"] * 4) for n in T.get("snare", [])}
        for t, ln, kind, j, hi_i in strikes(11, ELEVEN_A, s16(a), s16(z) - FILL_LEN["run"]):
            if t not in snares:          # one hand: where the backbeat falls it plays the snare
                add("toms", t, 1, hi if kind == "h" else lo, float(v0) if j == 0 else float(v1))
                T["toms"][-1]["gain"] = g
    solo(a, z)

    # 10. 165-175  five meets eleven: the weight comes off, slowly. No riff: one chord to each turn of the eleven wheel,
    #     left to ring, on the wall rig, the drums in half time. The chords are the eye's, heard heavy before they are
    #     heard clean: Db (where the lead's run stood), Ab, Gb, home
    a, z = B[9], B[10]
    doom = [(a * 16, DB), (a * 16 + 44, AB), (a * 16 + 88, GB), (a * 16 + 121, F1)]
    for i, (t0, root) in enumerate(doom):
        t1 = doom[i + 1][0] if i + 1 < len(doom) else z * 16
        fade = 1.0 - 0.45 * (t0 - a * 16) / 160
        if RESTING:
            # This time the band supplies the ground: Db, Ab, Gb, F. The
            # cello enters on the *second* stroke of each chord, giving the
            # chord its third or root. The full tune belongs to the eye.
            pitch, _ = ends[i]
            bowed_rest(t0+11, t1-t0-11-1, pitch, return_trim)
        gtr(WL, 11, ELEVEN_D, t0 / 16, t1 / 16, root=root, vel=0.95 * fade)
        bass(11, ELEVEN_D, t0 / 16, t1 / 16, root=root, vel=0.9 * fade)
        crash(t0, 0.9 * fade, "c" if i % 2 == 0 else "x")
    kick(11, [(0, 1, "c")], a, a + 7, vel=0.85)                      # a kick under each chord, for seven bars
    kit(a, a + 5, "x", 8, "half", None, cvel=0.6, crash_at_start=False)
    kit(a + 5, z, "h", 4, "none", None, cvel=0.42, crash_at_start=False)
    tick("cl5", 5, TICK5, CL5, a + 5, z, ramp=(0.5, 1.0))
    bed([(a * 16 + 121, 0)], z * 16, vel=0.5, fifth=False, pad_vel=0)

    # 11. 175-210  five and seven meet: THE EYE. The ticks as at the start, but the ground moves under them, on the eleven
    #     wheel: Db, Ab, Gb and home, one chord to each phrase of the tune; the tune twice, low then high
    a, z = B[10], B[11]
    t0 = 176 * 16                                                    # eleven meets the bar line one bar in
    eye = [(a * 16, 0)]
    for rep in range(2):
        for i, off in enumerate((-4, 3, 1, 0)):
            eye.append((t0 + rep * 231 + [0, 55, 110, 165][i], off))
    bed(eye, z * 16)
    tick(EYE_TR[0], 5, TICK5, CL5, a, z, harmony=eye)                # in the eye each wheel's guitar moves to another wheel's count (EYEFX)
    tick(EYE_TR[1], 7, TICK7, CL7, a, z, harmony=eye)
    tick(EYE_TR[2], 11, TICK11, CL11_OPEN, a + 12, z, vel=0.36, harmony=eye)
    chimes(a, z - 2, pairs=((5, 7),), motor=bool(EYE_BARS))
    chimes(a + 12, z - 2, pairs=((5, 11), (7, 11)), motor=bool(EYE_BARS))
    for t in range((a + 8) * 16, z * 16 - 8, 4):
        add("cym", t, 4, "rb", 0.3 * (1.12 if t % 16 == 0 else 1.0))
    long_wait(a, 176 + 231 / 16, vel=0.7, up=-12, start=t0)
    long_wait(a, 176 + 462 / 16, vel=0.7, up=0, start=t0 + 231)
    if CHOIR:
        long_wait(a, 176 + 462 / 16, vel=0.6, up=0, start=t0 + 231, tr="choir")    # three soft singers on the tune's second pass
    for t, ln, kind, j, hi in strikes(5, FIVE_A, (z - 10) * 16, z * 16 - 12):
        add("toms", t, 1, ["ft", "t2", "t1"][j], 0.32 + 0.33 * (t - (z - 10) * 16) / 160)
    kick(4, [(0, 1, "c")], z - 6, z, vel=0.45)
    fill(z, "toms")
    rise(z, 2)

    # 12. 210-220  five and seven meet: the weight comes back. Muted five on the guitars, seven under it, toms on five
    a, z = B[11], B[12]
    gtr(G, 5, FIVE_B, a, z, hook=H1, vel=0.85, ramp=(0.6, 1.0))
    bass(7, SEVEN_A, a, z, hook=OCT)
    kick(7, SEVEN_A, a, z)
    for t, ln, kind, j, hi in strikes(5, FIVE_A, a * 16, (a + 5) * 16):
        add("toms", t, 1, ["ft", "t2", "t1"][j], 0.7)
    crash(a * 16, 0.7)
    kit(a + 5, z, "x", 4, "half", "roll")
    rise(z, 1)
    if SPEAK:
        speak("speak", SPOKEN)
        for i in range(len(ROBOTS)):                                  # v50: the same line on each machine
            speak(f"rb{i + 1}", SPOKEN)
        if SPEAKS.startswith("cross"):                                # the wall guitars hold the chord through each line, and say it
            speak("spk", SPOKEN)                                      # (the line once more on a muted track: the effect's key, see SPEAKS)
            k = 126 / 110 * 4
            for bar, notes in SPOKEN:
                t0 = bar * 16 + (notes[0][0] - 0.25) * k - 2
                t1 = bar * 16 + (notes[-1][0] - 0.25 + notes[-1][1]) * k + 2
                for tr in ("wsl", "wsr"):
                    add(tr, t0, t1 - t0, SPEAKS.split(";")[1], 0.9)

    # 13. 220-231  five meets eleven: the splayed riff again, filled in, its hook doubled above; on Bb
    a, z = B[12], B[13]
    gtr(WL, 11, ELEVEN_B, a, z, root=BB, hook=H1)
    gtr(G2, 11, ELEVEN_W, a, a + 5, root=BB, vel=0.9)
    harm(G2, 11, ELEVEN_B, a + 5, z, 12, root=BB, hook=H1)
    bass(11, ELEVEN_B, a, z, root=BB, hook=H1)
    kick(11, ELEVEN_B, a, z)
    kit(a, z, "x", 4, "half", "kicks")
    if RETRO:                                                         # v45: the lead's run of 4:53, backwards, in its mirror
        solo_back(a, B[9], int(RETRO.split(";")[0]), float(RETRO.split(";")[1]))

    # 14. 231-245  seven meets eleven: seven on the guitars over eleven's chords; double time; on Eb (F, Bb, Eb: up by fourths, then home)
    a, z = B[13], B[14]
    gtr(G, 7, SEVEN_B, a, z, root=EB, hook=H3)
    gtr(WL, 11, [(0, 8, "P"), (8, 2, "d")], a, z, root=EB, vel=0.9)
    bass(7, SEVEN_B, a, z, root=EB, hook=H3)
    kick(7, SEVEN_B, a, z)
    kit(a, z, "x", 2, "back", "run", cvel=0.55)
    if SEQ:
        up, v0, v1 = int(SEQ.split(';')[1]), float(SEQ.split(';')[3]), float(SEQ.split(';')[4])
        s0, s1 = s16(a), s16(z) - s16(z) % 11            # whole turns of eleven: the last quarter note is the band's
        assert s0 % 11 == 0
        for t, ln, kind, j, hi in strikes(11, TICK11, s0, s1):
            v = v0 + (v1 - v0) * (t - s0) / (s1 - s0) + (0.18 if j == 0 else 0)
            add('seq', t, 1, 53 + EB - F1 - 12 + CL11[j] + up, v)

    # 15. 245-275  five meets seven: all three. Five left, seven right, eleven in the bass, and the tune over them
    a, z = B[14], B[15]
    gtr(("gl",), 5, FIVE_B, a, z, hook=H1)
    gtr(("gr",), 7, SEVEN_B, a, z, hook=H2)
    bass(11, ELEVEN_A, a, z, hook=OCT)
    kick(5, FIVE_B, a, z)
    kit(a, a + 15, "rde", 4, "half", None, cvel=0.6)
    kit(a + 15, z, "x", 4, "half", "run16", crash_at_start=False)
    long_wait(a, z, vel=0.8)
    if TWIN:                                                          # v52: the tune's second pass, in thirds
        twin(s16(a) + (-s16(a)) % 11 + LONG_WAIT_TURNS * 11, s16(z))
        TWIN_AT[:] = [s16(a) + (-s16(a)) % 11 + LONG_WAIT_TURNS * 11, s16(z)]
    harm(G2, 5, FIVE_B, a + 15, z, 12, hook=H1, vel=0.72)
    for t in landings(5, a * 16 + 1, z * 16):
        crash(t, 0.8)
    if MEET:                                                          # v63: where all three wheels are played, their meetings ring
        s0, s1 = s16(a), s16(a + int(MEET.split(";")[0]))
        for k, (p, q) in enumerate(((5, 7), (5, 11), (7, 11))):
            for t in range(s0 + (-s0) % (p * q), s1, p * q):
                add(f"meet{p}{q}", t, 8, {(5, 7): 84, (5, 11): 80, (7, 11): 89}[p, q], float(MEET.split(";")[1]))
                if float(MEET.split(";")[3].split(",")[k]):
                    T[f"meet{p}{q}"][-1]["gain"] = MEET.split(";")[3].split(",")[k] + "dB"

    # 16. 275-280  five meets eleven: stop-time again, with a dissonant chord and the toms in the gaps
    a, z = B[15], B[16]
    gtr(G, 5, FIVE_S, a, z, vel=0.95)
    gtr(G2, 5, [(0, 2, "d")], a, z, vel=0.9)
    quarter_stabs(a, z, returning=True)
    bass(5, FIVE_S, a, z, vel=0.95)
    kick(5, FIVE_S, a, z, vel=0.95)
    for t, ln, kind, j, hi in strikes(5, [(0, 2, "p"), (2, 1, "c"), (3, 1, "c"), (4, 1, "c")], a * 16, z * 16):
        if j == 0:
            add("cym", t, 2, "cch", 0.75)
        else:
            add("toms", t, 1, ["t1", "t2", "ft"][j - 1], 0.7)

    if SQUEAL:      # the stab before the last squeals: two pinched harmonics a fifth apart ring through the gap, and with
        #             the last stab the tape stop drags them down with everything else. They sound Ab5 and Eb6, the hook's
        #             first note and its fifth: F5 and C6 were tried first and vanished into the F chord's own overtones
        add("ql", 279 * 16 + 6, 10, 56, 1.0, ph=1)         # Ab3 touched at its quarter: sounds Ab5
        add("qr", 279 * 16 + 6, 10, 63, 1.0, ph=1)         # Eb4: sounds Eb6

    # 17. 280-308  five meets seven: the hardest stretch. Seven everywhere, the kick running sixteenths; up a semitone
    #     and back; the last seven bars the snare goes to the off-beats
    a, z = B[16], B[17]
    for (x, y, root) in ((a, a + 14, F1), (a + 14, a + 21, F1 + 1), (a + 21, z, F1)):
        if x > a:
            crash(x * 16, 0.9)
        gtr(G + G2, 7, SEVEN_B, x, y, root=root, hook=H2, vel=0.92)
        bass(7, SEVEN_B, x, y, root=root, hook=H2, vel=0.92)
    kick(7, SEVEN_B, a, z, fill16=True)
    kit(a, a + 21, "x", 2, "back", None, cvel=HCYM[0])           # the china on every eighth: the piece's densest cymbal
    kit(a + 21, z, "x", 4, "blast", "roll16", cvel=HCYM[1], crash_at_start=False)
    if HOLE:                              # v44: half a bar of the kick alone before the ground moves up
        hb, h16 = [int(v) for v in HOLE.split(":")[:2]]
        g0, g1 = (hb * 16 + h16) / 4, (hb + 1) * 4
        for tr in list(T):
            if tr == "kick" and HOLE.split(":")[2:] != ["all"]:
                continue
            keep = []
            for n in T[tr]:
                if g0 <= n["at"] < g1:
                    continue
                if hb * 4 <= n["at"] < g0 < n["at"] + n["len"]:      # a note of this bar ringing into the hole stops at its edge
                    n = {**n, "len": round(g0 - n["at"], 4)}
                keep.append(n)
            T[tr] = keep
    if VOX:
        vox(a)

    # 18. 308-315  seven meets eleven: seven bars for the bass, on eleven, under one held chord; on Ab, like the first break
    a, z = B[17], B[18]
    for tr in WL:
        add(tr, a * 16, 7 * 16 - 12, "Ab1,Eb2,Ab2,Eb3", 0.9)
    bass(11, ELEVEN_B, a, z, root=AB, hook=H1, vel=0.95)
    kick(11, ELEVEN_A, a, z)
    kit(a, z, "h", 2, "half", "toms", cvel=0.5, ghost=True)
    if HANDS:
        assert hands_on_seven(a, z) == 24 and len(T["hands"]) == 57

    # 19. 315-330  five meets seven: the two guitars swap wheels (seven left, five right) over a floor-tom pulse
    a, z = B[18], B[19]
    gtr(("gl",), 7, SEVEN_A, a, z - 0.5, hook=H2)
    gtr(("gr",), 5, FIVE_A, a, z - 0.5, hook=H1)
    bass(5, FIVE_A, a, z - 0.5, hook=H1)
    kick(5, FIVE_A, a, z - 0.5)
    kick(7, SEVEN_A, a, z - 0.5, only_first=True)
    kit(a, z, "ft", 4, "half", "stop", cvel=0.58, ghost=True)                 # no cymbals: the pulse is on the floor tom

    relay(a, z, returning=True)

    # 20. 330-350  five meets eleven: RIFF A comes home, with eleven's chords and the tune
    a, z = B[19], B[20]
    gtr(G, 5, FIVE_A, a, z, hook=HX, vel=0.92)                       # the hook has grown to seven notes
    harm(G2, 5, FIVE_A, a, z, 12, hook=HX, vel=0.85, power=True)     # and is struck as power chords above the riff
    gtr(WL, 11, ELEVEN_W, a, z, vel=0.92)
    bass(5, FIVE_A, a, z, hook=HX, vel=0.92)
    kick(5, FIVE_B, a, z)
    kit(a, z, "x", 4, "half", "run")
    long_wait(a, z, vel=0.8)
    for t in landings(5, a * 16 + 1, z * 16):
        crash(t, 0.8)

    # 21. 350-385  five and seven meet for the last time before the landing: THE APPROACH. It starts from nothing, as the
    #     piece did: the ticks, then a heartbeat. Each wheel's guitar comes in where that wheel next meets
    #     a bar line (seven at 357, five at 360, eleven at 363); double time from 371; at 383 the band stops and the
    #     three wheels tick alone into the bar line they have been turning towards since bar 1
    a, z = B[20], B[21]
    crash(a * 16)
    for tr in WL:
        add(tr, a * 16, 60, "F1,C2,F2,C3", 0.9)
    bed([(a * 16, 0)], z * 16, vel=0.55, pad_vel=0.4)
    if SWARM:                                                       # the swarm again: a crowd, pulled into step by the landing
        for n in SWARM_NOTES:
            add("swarm", a * 16, (NB - 2 - a) * 16, n, 0.7)
    tick("cl5", 5, TICK5, CL5, a, z, vel=0.5)
    tick("cl7", 7, TICK7, CL7, a, z, vel=0.5)
    tick("cl11", 11, TICK11, CL11, a, z, vel=0.46)
    chimes(a, 363)
    chimes(383, z)
    for t in range(a * 16, 363 * 16, 4):
        add("cym", t, 4, "rb", 0.34 * (1.12 if t % 16 == 0 else 1.0))
    kick(4, [(0, 1, "c")], 354, 363, vel=0.5)                        # the heartbeat, from the fifth bar
    bass(11, ELEVEN_A, 359 if ASSEMBLE else 357, 363, hook=OCT, vel=0.75)                  # the bass comes in with the first guitar (v47: two bars after it)
    grow7, grow5 = ([[(int(g.split(":")[0]), {int(i) for i in g.split(":")[1].split(",")}) for g in part.split(";")] for part in ASSEMBLE.split("|")[:2]]
                    if ASSEMBLE else (None, None))
    gtr(("gr",), 7, SEVEN_B, 357, 363, hook=H2, vel=0.9, ramp=(0.6, 1.0), rig=CRUNCH, dyn=SOFT, grow=grow7)    # the first guitars back are the low-gain rig;
    gtr(("gl",), 5, FIVE_B, 360, 363, hook=HX, vel=0.9, ramp=(0.7, 1.0), rig=CRUNCH, dyn=SOFT, grow=grow5)     # the high-gain ones come with the band at 363
    fill(363, "toms")
    gtr(("gl",), 5, FIVE_B, 363, 383, hook=HX, vel=0.92, ramp=(0.92, 1.05))
    gtr(("gr",), 7, SEVEN_B, 363, 383, hook=H2, vel=0.92, ramp=(0.92, 1.05))
    gtr(WL, 11, ELEVEN_W, 363, 383, vel=0.92)
    bass(11, ELEVEN_A, 363, 383, hook=OCT, vel=0.92)
    kick(5, FIVE_B, 363, 371)
    kick(5, FIVE_B, 371, 383, fill16=True)
    kit(363, 371, "x", 4, "half", None)
    kit(371, 383, "x", 2, "back", "run16", cvel=0.6, crash_at_start=False)
    long_wait(363, 383, vel=0.85)
    if ATT:        # the tune's ghost: an attractor plays the END of the tune over the approach's ticks, settling from five cycles
        #            to one, and hands it to the lead, who begins it again from the top when the band comes in (bar 363, where
        #            the eleven wheel meets the bar line). So the ghost enters three turns into the tune, on its fourth note
        t_att = 350 * 16 + (-350 * 16) % 11
        assert (363 * 16 - t_att) % 11 == 0 and (363 * 16 - t_att) // 11 == LONG_WAIT_TURNS - 3 and sum(n for _, n in LONG_WAIT[:3]) == 3
        long_wait(350, 363, vel=0.8, tr="att", start=t_att, i0=3)
    for t in landings(7, 363 * 16 + 1, 383 * 16):
        crash(t, 0.85)
    rise(z, 2)

    # THE LANDING, 385-409: all three wheels and the bar line, together for the first time since bar 1. Four bars of one
    # chord on every bar line over the plainest beat there is; then common time as a riff: a cell eight sixteenths long
    a = 385
    hit(a * 16, ln=14)
    for b in range(a + 1, a + 4):
        for tr in G + G2 + WL:
            add(tr, b * 16, 14, "F1,C2,F2,C3", 0.95)
        add("bass", b * 16, 14, "F1", 0.95)
        crash(b * 16, 0.85)
    for b in range(a, a + 4):
        for o in ((0, 10) if b > a else (10,)):
            add("kick", b * 16 + o, 1, "k", 0.92)
    kit(a, a + 4, "x", 4, "back", None, crash_at_start=False)
    gtr(G + G2, 8, EIGHT, a + 4, a + 16, hook=H8, vel=0.95)
    bass(8, EIGHT, a + 4, a + 16, hook=H8, vel=0.95)
    chime_all(a * 16)
    kick(8, EIGHT, a + 4, a + 16)
    kit(a + 4, a + 16, "x", 4, "back", "roll")
    for b in range(a + 6, a + 16, 2):
        crash(b * 16, 0.85)
    hit((a + 16) * 16, ln=8 * 16)
    if FLOOR:                                                       # v53: the four chords' floor
        offs = [int(x) for x in FLOOR.split(";")[1].split(",")]
        T["bass"] = [n for n in T["bass"] if not (a * 4 <= n["at"] < (a + 4) * 4)]
        for b in range(a, a + 4):
            for i, o in enumerate(offs):
                add("bass", b * 16 + o, (offs[i + 1] if i + 1 < len(offs) else 14) - o, "F1", 1.0 if (b == a and o == 0) else 0.95)
            if b > a:
                add("drop", b * 16, 12, "F1", float(FLOOR.split(";")[0]))
    if WORD:                                                        # the answer to "wait" and "not yet": one word, on each of the four chords and on the last
        for b in range(a, a + 4):
            T.setdefault("word", []).append({"at": b * 4, "len": 3.5, "pitch": "F3", "vel": 0.9, "ph": WORD_PH})
        T.setdefault("word", []).append({"at": (a + 16) * 4, "len": 20, "pitch": "F3", "vel": 0.9, "ph": WORD_PH})
    if ENDING:      # all three wheels tick on, as at the start, and are heard: the chord under them dies away (see ENDING)
        bed([((a + 16) * 16, 0)], NB * 16, vel=float(ENDING.split(":")[2]), pad_vel=float(ENDING.split(":")[3]))
        tick("cl5", 5, TICK5, CL5, a + 17, NB - 1, vel=0.5, ramp=(1.0, 0.8))
        tick("cl7", 7, TICK7, CL7, a + 17, NB - 1, vel=0.5, ramp=(1.0, 0.8))
        tick("cl11", 11, TICK11, CL11_OPEN, a + 17, NB - 1, vel=0.44, ramp=(1.0, 0.8))
        chimes(a + 17, NB - 1, vel=0.45)
    else:
        bed([((a + 16) * 16, 0)], NB * 16)
        tick("cl5", 5, TICK5, CL5, a + 17, NB - 1, ramp=(1.0, 0.4))
        tick("cl7", 7, TICK7, CL7, a + 17, NB - 1, ramp=(1.0, 0.4))
        chimes(a + 17, NB - 1, pairs=((5, 7),), vel=0.4)


# synth layers (Harry, 12 Nov: "layered synths / tones ... a showcase of all features"), each its track's gain ("" = off)
# THE SWARM: sixteen oscillators to a note, each at its own pitch, pulled toward their common phase by a coupling that a lane
# rides (the engine's Kuramoto model of synchrony). At bar 1 they are in step; over the wait they drift into a crowd; from
# the approach they are pulled back, and lock as the three wheels land.
# THE MIX BY SECTION (v16). Measured against the eleven records section by section, not only in the three windows of v7
# (tools/stembal.py), and against how far the records themselves move between their own loud passages
# (~/.local/state/chirper-zero/c10/refspread.py: std 0.6-1.0 dB a band, but 2.2 at 500 Hz-1 kHz and 1.3 at 8-16 kHz).
# Track faders by section, (first bar, last bar, dB); "" = off. High-gain rigs are saturated, so velocity cannot do this.
SECMIX = os.environ.get("C10T1_SECMIX", "1")
SECTION_FADERS = {"gl2": [(280, 308, -2.5)], "gr2": [(280, 308, -2.5)]} if SECMIX else {}   # the doubling guitars in the hardest stretch: 2-4 kHz read 1.8 dB over
# v21, a tidy of three things the guard windows showed. (1) Under 60 Hz the eleven-wheel sections read 1.4-2.3 dB over the
# records. It is the KICK, not the bass (the kick is 70-100% of that band everywhere): on the wall rig it stood 2-3 dB over
# the guitars where in riff A it is level with them. So the kick's fader comes down through riff C and the split, and in the
# Bb section, where the mids were also 2-3 dB under, the wall guitars come up. (2) the spoken voice's body, see SPEAK.
TIDY = os.environ.get("C10T1_TIDY", "1")
if TIDY:
    SECTION_FADERS.update({"kick": [(110, 154, -1.0), (220, 231, -1.2)], "wl": [(220, 231, 1.5)], "wr": [(220, 231, 1.5)]})
# v40: where riff C's open chords stop and its hook is pulled wide (bars 136-140) the riff's two guitars come up by this
# much: without the chords the passage fell 1.6 dB (-19.4 LUFS raw, where the riff alone at 3:29 reads -19.5)
SPLAY_LIFT = os.environ.get("C10T1_SPLAYLIFT", "1.5")
if SPLAY and SPLAY.split(";")[3:] == ["1"] and SPLAY_LIFT and SECMIX:
    for _tr in ("wl", "wr"):
        SECTION_FADERS[_tr] = sorted(SECTION_FADERS.get(_tr, []) + [(136, 140, float(SPLAY_LIFT))])
if ELEVALONE and SECMIX and float(ELEVALONE.split(";")[2]):          # v48: eleven's chords, alone over the rhythm section
    for _tr in ("wl", "wr"):
        SECTION_FADERS[_tr] = sorted(SECTION_FADERS.get(_tr, []) + [(55, 55 + int(ELEVALONE.split(";")[0]), float(ELEVALONE.split(";")[2]))])
# the wall rig's tracks: a dip at 350 Hz. It is the thick rig (4-5 dB more than the tight one at 160-315 Hz), and every section
# it plays chords in read over the records at 250-500 Hz (riff C with its chords 2.4, the approach 3.2, section 13 1.3)
WALL_EQ = os.environ.get("C10T1_WALLEQ", "350:1:-2.5") if SECMIX else ""
# the bark's top: without the voice the hardest stretch read 0.8 dB over the records at 8-16 kHz, with it 2.4 (its scream is noise up there)
VOX_SHELF = os.environ.get("C10T1_VOXSHELF", "7000:-6") if SECMIX else ""
# the china's velocity in the hardest stretch (eighths : quarters); it read 2.9 dB over at 8-16 kHz with 0.58:0.66
HCYM = [float(x) for x in os.environ.get("C10T1_HCYM", "0.48:0.58").split(":")]
# effects where the music asks for them (Harry: "a showcase of all features"), each with a switch ("" = off)
WAH = os.environ.get("C10T1_WAH", "1")          # a wah on the lead's run (4:53): the pedal opens through each flurry and closes on the held note
ROTARY = os.environ.get("C10T1_ROTARY", "1")    # a rotary speaker on the slow chords (5:14): it comes in over the first chord and spins up as they fade
# two pinch harmonics over the last two stabs before the tape stop (8:52), on the tight rig. Tried in round 20 they added only
# 1.5-5 dB in their own bands, because the guitars never fell silent between the stabs. Now that they do (v20, STOPS below),
# the squeal stands 5-12 dB clear of the gap from 1.25 to 4 kHz. "" = none
SQUEAL = os.environ.get("C10T1_SQUEAL", "-6dB" if os.environ.get("C10T1_STOPS", "x") else "")
# v21: the first stop-time's last stab STUTTERS into riff C: five sixteenths, each re-read a semitone higher (3:29). The form
# is a palindrome and its two stop-times mirror each other: the second ends in the tape stop (time drags, the pitch falls),
# the first in this (time splinters, the pitch climbs). The stutter's slot is five sixteenths long, the five wheel's own
# turn, so it falls on the wheel's stab by itself. "semitones per repeat : roll : decay"; "" = none
STUTTER = os.environ.get("C10T1_STUTTER", "1:1:0" if os.environ.get("C10T1_TIDY", "1") else "")
# v23, THE ENDING. The last chord was held by eight guitars and the bass at the landing riff's full level for eight bars, and
# then stopped; the ticking guitars and the chimes written over it ("the wheels turn on") sat 24-30 dB down and were never
# heard. A chord that rings out dies away. Now it does: the guitars' and the bass's faders fall from the chord's second bar
# to the end, the choir's held word eases off as a breath does, and all three wheels tick on over it as they did at the
# start (the eleven's bell was missing from the coda). The chord struck at the approach's first bar dies away too.
# "dB the last chord has fallen by the end : dB the approach's chord has fallen by its end : the coda's drone, its
# velocity : and its pad's"; "" = as it was (v22)
ENDING = os.environ.get("C10T1_ENDING", "30:14:0.45:0.35")
# "dB the piece's first chord has fallen by the end of its two bars : dB the bass break's chord has fallen by its end"; "" = held flat (v23)
# A LANE'S FALL IS NOT A STRAIGHT LINE unless it is told to be. A lane is an envelope, and an envelope's falling segments
# take its `curve` (default 3: fast, then slow); rising ones are straight. Measured on a sine, a lane from 0 to -20 dB
# over eight beats reads -3.0 -8.8 -12.6 -15.3 -17.1 -18.3 -19.2 -19.8 at the beats' middles: half the fall in the first
# fifth. With "curve": 0 on the lane it reads -1.2 -3.7 -6.2 -8.7 -11.2 -13.7 -16.2 -18.7, the line as written.
# On a chord that should die away the default gives a quick drop and then a plateau (struck loud, then held soft), so these
# two fades have a lane of their own with "curve": 0. Every earlier fade in the piece (the slow chords at 5:14, the
# approach's chord, the ending) keeps the default: each was measured as it sounds, and is described as measured.
RINGS = os.environ.get("C10T1_RINGS", "13:12")
ENDLINE = os.environ.get("C10T1_ENDLINE", "")      # "1" = the last chord's fade as a straight line too (an alternative, not kept)
# v25, THE PICK. The engine plucks a string with a burst of noise (an even, bright spectrum, its phases at random). A string
# let go by a pick is a triangle that springs back: one kink going round the string, a pulse a period. The engine has that
# shape too (`soft`: 0 the noise, 1 the triangle), described as a finger's. Here it is bound to the palm mute
# (soft = expr.pm) on the five wheel's rig.
# WHAT IT DOES IN THE SONG (riff A, the left guitar alone, 98 muted notes): with the noise pick a muted low F is flat to 1 dB
# from its start to the next note, a hiss held by the amp. With the triangle it pulses at the string's own rate (43.65 Hz,
# every 23 ms): 2 dB in the whole band and 6-7 dB at 100-250 Hz. A growl, not a hiss.
# AGAINST THE RECORD (tools/riffpunch.py, Bleed 0-30 s, 302 muted notes, this exact rig; the record in brackets):
#   rise 20.2 -> 15.5 ms (14.2); low end, first 20 ms against 40-80 ms: 3.7 -> 1.4 dB (1.2); noise between the harmonics at
#   1-4 kHz 0.26 -> 0.40 (0.41); punch 4.1 -> 4.0 (3.6); 400 Hz-1 kHz against 1-4 kHz -11.2 -> -9.9 (-11.9); fizz the same
# On EVERY note it is wrong (The Faultless's open notes: punch 5.8 against the record's 4.0), so it rides the mute only.
# ONE MEASURE READS AGAINST IT: tools/guitarbench.py's low-mid "contrast" (how far the harmonics stand above the valleys
# between them, the 400 Hz octave) 18 dB against the record's 27; v24's rig reads 27. Not the pick noise, the grain, the
# ring or the buzz (each taken out in turn). So this is a judgment for an ear: five measures for, one against.
# THE TONE IS HELD WHERE IT WAS. A muted note's direct signal is now fundamental-heavy (+8 dB at 80 Hz after the amp), so
# the high-pass ahead of the amp (`tight`) goes from 80 to 220 Hz, and
# the tighter amp then leaves the rig 2-3 dB down at 80-125 Hz and 2.5-3.8 up at 250-315 Hz; an eq on the four tracks, after the
# rig, takes that back: riff A's and the landing's guitars are within 0.5 dB of v24 on average over the third-octaves (1.9 at the worst, 630 Hz), and
# no band of any guard window moves more than 0.6 dB against the records.
# ONLY THE FIVE WHEEL'S RIG (ct-chug): it is the rig the bench is built on. Seven's and eleven's keep the noise pick, so
# where five is on the left and seven on the right (4:26, 7:46) the two attacks are side by side.
# "soft's source ; the amp's tight in Hz ; that eq's peaks"; "" = the noise pick (v24)
PICK = os.environ.get("C10T1_PICK", "expr.pm;220;100:1.2:2.2,280:1.5:-3")
PICKED = f" synth.layers.0.soft={PICK.split(';')[0]} fx.2.tight={PICK.split(';')[1]}" if PICK else ""
# v29: AFTER THE EYE the five wheel's string is a real one too (see REAL below). From bar 210 on, the five wheel's riffs go to
# four tracks of their own (rl, rr, rl2, rr2): the same rig with `inharm` (B 5e-5), the white noise that stood in for a real
# string's roughness (`grain`) turned OFF, the pick 0.7 of the way from a noise burst to a released string (v25's is all the way),
# the amp's `tight` at 190 and an eq after it that holds the tone (guitars alone within 0.5 dB of v24's in third-octaves).
# Before the eye the five wheel keeps v25's pick, so the piece has both: riff A at 1:06 on the one, riff A's return at 10:28 on
# the other. B ; the pick ; the amp's tight ; the eq's peaks ; from which bar. "" = v28 (one string throughout).
# v30: the eq after it is refitted so this rig's tone is the FIRST HALF's rig's (within 0.4 dB in third-octaves), not the old
# noise pick's: v29's fit had put 2 dB back at 735 Hz, where our guitars already stand 2-4 dB over a guitar heard alone on the
# records (obZen 3:03, Bleed 6:27; gspec.py), and where the records' passages WITHOUT a voice hold 3.6 dB less than those with
# one (vocsplit.py). The two strings now differ in the string and nothing else. v29's eq: 99:3:5.1,231:1.2:-4.1,735:1.8:2.
REAL5 = os.environ.get("C10T1_REAL5", "0.00005;expr.pm*0.7;190;92:4:3.2,262:1.3:-2.6;210")
REAL_MAP = {"gl": "rl", "gr": "rr", "gl2": "rl2", "gr2": "rr2"} if REAL5 else {}
REAL_FROM = float(REAL5.split(";")[4]) if REAL5 else None
REAL_RIG = (f" synth.layers.0.soft={REAL5.split(';')[1]} fx.2.tight={REAL5.split(';')[2]} synth.layers.0.inharm={REAL5.split(';')[0]}"
            " synth.layers.0.grain.mod.0.amount=0 synth.layers.0.grain.value=0") if REAL5 else ""
# v37: THE LANDING RIFF'S OWN RIG. A wheel is known by its rig (five the tight one, seven ct-bite, eleven ct-wall), and the
# riff at the landing is no wheel: its cell is eight sixteenths long, common time itself, the thing the three wheels were
# all counting towards. Until now it played on the five wheel's rig. It has its own now, heard nowhere else in the piece:
# the real string into the engine's `gojira` amp (its mids forward, `mid` raised), the same cabinet, a cone of its own.
# model : mid ; mic , left cone , right cone ; trim dB over the tight rig's, left , right. "" = v36 (the five wheel's rig).
# The trims make each side as loud (LUFS, alone) as the five wheel's rig was there: with one amp model on both sides the
# right guitar, whose patch sets its own bass and presence, came out 0.9 dB under the left.
# Measured alone (the four guitars, bars 389-395) against the five wheel's rig: 141-282 Hz 2.8 dB less, 282 Hz-2.2 kHz
# about 1 dB more; the landing riff stood furthest from the records in the mix at 120-250 Hz (+2.0 over).
LANDRIG = os.environ.get("C10T1_LANDRIG", "gojira:0.76;0.25,6,7;0.5,1.5")
LAND_MAP = {"gl": "el", "gr": "er", "gl2": "el2", "gr2": "er2"} if LANDRIG and REAL5 else {}
LAND_AMP = (f" fx.2.model={LANDRIG.split(';')[0].split(':')[0]}" + (f" fx.2.mid={LANDRIG.split(';')[0].split(':')[1]}" if LANDRIG.split(';')[0].split(':')[1] else "")) if LAND_MAP else ""
if REAL5 and "gl2" in SECTION_FADERS:      # the hardest stretch's doubling guitars are on the real string now: their fader goes with them
    SECTION_FADERS["rl2"], SECTION_FADERS["rr2"] = list(SECTION_FADERS["gl2"]), list(SECTION_FADERS["gr2"])
# v30: THE MIX READ AGAINST THE RIGHT PASSAGES. The records' loud passages WITHOUT a voice differ from those with one (eleven
# records, vocsplit.py): 2.3 dB less at 500 Hz-1 kHz and 1.4 less at 8-16 kHz than all their loud passages together (the
# yardstick used until now), 0.4 more under 120 Hz. Read that way our instrumental sections are on target at 500 Hz-1 kHz
# (they had read 1-2.5 "under") and 1.4-2.2 dB bright at 8-16 kHz, which the cymbals carry alone. And THE LANDING's riff,
# with four guitars on it, read 1.0-1.4 dB light under 120 Hz and 2.2 over at 120-250 Hz.
# LANDMIX: the landing riff (bars 389-401): bass dB : kick dB : the two doubling guitars dB : cymbals dB.
# CYMINST: the cymbals' fader in the instrumental sections that read 1.4 dB or more over at 8-16 kHz (riff A and the section
# after it, riff C before its chords). "" = v29's faders.
LANDMIX = os.environ.get("C10T1_LANDMIX", "1.5:1:-2.5:-1.5")
# BEQ2: an eq on the bass's bus AFTER its compressor (ahead of it the compressor gives a cut back). Every instrumental section
# read 1.3-1.6 dB over at 120-250 Hz (the landing riff 2.2), and by groups it is the bass: 3.7 dB more there than the
# records' bass stems, where the guitars have 2.3 less and the drums 1.0 more. "" = no second eq (v29).
BEQ2 = os.environ.get("C10T1_BEQ2", "170:1.2:-3")
# v31: THE GUITARS GET THEIR TOP BACK. Where a guitar plays ALONE on the records (obZen 3:03-3:11, Bleed 6:27, This Spiteful
# Snake 4:46; found with galone.py, read from the record itself with gspec.py) its top, against its own 2-3.15 kHz, is
# -3.6 at 4 kHz, -9.9 at 5, -16.4 at 6.3, -22.4 at 8, -26.7 at 10, -34.8 at 12.5 kHz, and three records from two albums agree
# to 0.7-1.6 dB. Our three heavy rigs matched that to 5 kHz and then stopped: 11-17 dB under at 8 kHz, 18-22 under at 10 kHz.
# The cause was mine: a high shelf of -10 to -15 dB at 5 kHz on every rig (and -3 at 7.5 kHz), put there against the bench's
# "fizz +8", which was the stem separator's doing and not the record's. Here the shelves are taken off (overrides at the song;
# no library patch is touched) and two peaks per rig put the top where the record's is, less a third: a cut at the cabinet's
# 5 kHz hump, and for the two rigs on cabinet files a lift into the hole those files have at 8-10 kHz. Predicted against the
# record at 8 / 10 kHz: tight rig -5.4 / -5.0, seven's rig -4.2 / -8.5, wall rig -3.2 / -5.4 (held back because our top
# moves less with the playing than the record's: 6-7 dB against 11-13). Seven's rig also loses 2 dB at 3 kHz: it stood
# 1.5 dB over the record's guitar there, and the hardest stretch, which it leads, has read 1.7 over at 2-4 kHz since v16.
# the tight rig's peaks ; seven's rig's ; the wall rig's. "" = v30.
TOP = os.environ.get("C10T1_TOP", "5300:2:-10,9100:1.8:7.5;3000:1.2:-2,5500:1.6:-6.7,9000:1.2:-4;5272:2.4:-9.7,9613:1.1:5")
TOP_OF = {**{t: 0 for t in ("gl", "gr", "gl2", "gr2", "rl", "rr", "rl2", "rr2", "ql", "qr", "el", "er", "el2", "er2")}, "sl": 1, "sr": 1, "wl": 2, "wr": 2}
if DBL_MAP:
    TOP_OF.update({d: TOP_OF[x] for x, d in DBL_MAP.items()})
CYMINST = os.environ.get("C10T1_CYMINST", "-1.5")
# v35: THE CYMBALS' AIR. Read window by window against the records' passages with as much voice as the window has
# (stembal --voice-tracks), 8-16 kHz was the worst band left: +1.0 to +2.2 dB in the six windows with little or no voice
# (riff A, the section after it, riff C, the split, the hardest stretch, the landing riff), level or under in the three
# with a tune. The cymbals carry that band alone, so: a high shelf on the cymbals', hats' and ride's tracks (Hz:dB), which
# leaves their 4-8 kHz where it is, and the cymbals' fader down in the hardest stretch (bars 280-308), the worst. "" = v34.
CYMAIR = os.environ.get("C10T1_CYMAIR", "9000:-2;-1.5")
if SECMIX and (LANDMIX or CYMINST):
    cymf = [(35, 70, float(CYMINST)), (110, 121, float(CYMINST))] if CYMINST else []
    if LANDMIX:
        lb, lk, ld, lc = [float(x) for x in LANDMIX.split(":")]
        cymf.append((389, 400.5, lc))        # back to the old balance by bar 401: the last chord and its crash are as they were
        SECTION_FADERS["kick"] = SECTION_FADERS.get("kick", []) + [(389, 400.5, lk)]
        for tr in (() if DOUBLE else ("el2", "er2")) if LAND_MAP else ("rl2", "rr2") if REAL5 else ("gl2", "gr2"):
            SECTION_FADERS[tr] = SECTION_FADERS.get(tr, []) + [(389, 400.5, ld)]
    if cymf:
        if CYMAIR and len(CYMAIR.split(";")) > 1 and float(CYMAIR.split(";")[1]):
            cymf = sorted(cymf + [(280, 308, float(CYMAIR.split(";")[1]))])
        SECTION_FADERS["cym"] = cymf
# v26, THE EYE: THE WHEELS LOOK AT EACH OTHER. In the quiet centre (5:33-6:40) each wheel's clean guitar is moved by another
# wheel's count, on the song's clock, so the two stay locked:
#   five's guitar (left) swells and sinks every SEVEN sixteenths (a `tremolo`), loudest where five and seven meet;
#   seven's guitar (right) changes colour every ELEVEN sixteenths (a `phaser`);
#   eleven's bell (middle) circles the listener once every FIVE eighths (an `orbit`).
# The eye's ticks are on tracks of their own (e5, e7, e11: the same guitars, with the effect), so the ticks everywhere else are
# untouched. "the tremolo's depth : dB made up on that guitar : the phaser's mix : its feedback : dB made up : the orbit's radius
# in metres : dB made up"; "" = v25
EYEFX = os.environ.get("C10T1_EYEFX", "0.85:3:0.5:0.6:2.5:2:1.7")
# v27: THE BASS GROWS TEETH. The bass break (bars 308-315, 9:46) was seven bars of the same round bass under a chord that fades:
# nothing in it moved but the fade. Now the bass is also sent to a bus of its own ("grind": a high-pass, the `drive` effect as a
# WAVEFOLDER, a low-pass) whose level and fold depth rise as the chord dies, so the bass turns from round to snarling and takes the
# place the guitars leave; it is cut where the band comes back at bar 315. A send, not a second bass track: the two layers are the
# same performance to the sample (a second track would be humanized apart and comb against the first). Outside the break the bus
# sits at -120 dB. The fold's depth is the level going INTO the folder (a gain ahead of it, on a lane), with the folder's own
# `drive` left at 0: a fold's output is scaled by 1 / |sin(pi k / 2)|, k = 1 + 19 drive + 80 drive^3, which has a pole at every
# even k, so a swept `drive` throws spikes up to 60 dB (measured: the bus peaked at the master's ceiling while adding 0.5 dB).
# high-pass Hz : gain into the folder at the start, dB : at the end : low-pass Hz : the bus's level at full, dB. "" = v26.
GRIND = os.environ.get("C10T1_GRIND", "300:30:50:4500:-26")
# v27: THE HAND. The low-gain rig's muted notes (the first break, 2:13, and the approach's first guitars, 11:20) are muted by a
# HAND on the string, the engine's physical palm mute with a width (`mute` + `mute_width`, live in the groove's engine since 13:19
# on 13 Nov), in place of the filter-and-shorter-decay every other rig uses. A low-gain amp shows it: the muted note is struck
# and then dies under the hand (its level falls 5 dB inside the note; the old one held to 1.7 dB), where a saturated amp would
# hide it. Depth of the mute (times the note's pm) : the hand's width as a fraction of the string. "" = v26.
HAND = os.environ.get("C10T1_HAND", "0.6:0.1")
# v28: THE POLE. The pad under the wait (0:00-1:08) goes through the engine's `barberpole`, a bank of band-passes an octave
# apart that climb for ever (each fades in at the bottom and out at the top): the wait is heard rising and never arriving.
# After the landing, under the ring-out's ticks (12:43), the same pole FALLS. The eye's pad and the approach's are left alone
# (under the approach's first bars the pole measured 0.7 dB deep in the mix: not there to be heard, so it is not there).
# The piece is a palindrome, and on a loop the fall at the end runs straight into the rise at the start.
# q 2 (the effect's default) moved nothing that could be measured on this pad: the bands overlap; at q 8 the comb is 13.5 dB deep.
# bars per octave : q : mix : right-channel offset (width) : the pad's make-up dB under the rising pole : under the falling one
# (the pole costs the pad +3.5 dB, so -3.5 holds its level; the ring-out's pad is struck softer than the wait's and gets 3 dB
# back, to stand beside its ticks as the wait's does). "" = v27.
POLE = os.environ.get("C10T1_POLE", "5:8:1:0.3:-3.5:-0.5")
# v29: THE REAL STRING. A stiff string's overtones are not exact multiples: partial n sounds at n f1 sqrt(1 + B n^2), and on a
# guitar B is about 1e-4 on a wound low string (partial 20 a third of a semitone sharp). The engine's strings had next to none of
# this (B 2e-7 at the heavy rigs' `stiff`, 0 on the clean guitars); `inharm` is B itself (engine feature of this album, bd-783db0,
# live in the groove's engine since 15:03 on 13 Nov). Here: the three clean guitars (the ticks of the wait, the eye, the approach
# and the ring-out), where a string is heard bare. B for the three clean guitars. "" = v28.
REAL = os.environ.get("C10T1_REAL", "0.00008")
REALS = f" synth.layers.0.inharm={REAL}" if REAL else ""
HANDED = (f" synth.layers.0.mute=expr.pm*{HAND.split(':')[0]} synth.layers.0.mute_width={HAND.split(':')[1]}"
          " synth.layers.0.decay.mod.0.amount=0 synth.filters.0.cutoff.mod.0.amount=0 synth.layers.0.bright.mod.0.amount=0") if HAND else ""
# v35: THE SPRING. The low-gain rig (the seven break at 2:13, the approach's first guitars at 11:19) gets what a low-gain
# amp has in its chassis: a spring tank, in place of the patch's plate (`fx.6.kind=spring`): three springs whose high
# frequencies arrive after their low ones, so a muted note leaves a short falling splash behind it. mix : decay : track dB.
# At 0.25 the splash is 3 dB up in the gaps (the quiet quarter of the time -21.2 -> -18.2 dB) and the hand's mute still
# shows (a muted note falls 3.7 dB inside itself; 4.9 before); at 0.35 the mute is washed out (1.9). "" = v34 (the plate).
# MY SLIP, mended in v38: that spring did NOT have highs arriving after lows (chirp-eco's dispersion.py: every band
# together; three short loops, a flutter). The engine's spring now has `drip` (engine feature 5, bd-7becc2), and a fourth
# field here sets it: at drip 1 each echo is a rising chirp (2.8 kHz 3.6 ms and 4 kHz 8.4 ms after 500 Hz). It is denser,
# so the mix comes down to 0.2 to leave the gaps and the mute where they were (quiet quarter -18.9 dB, the mute's fall
# 3.5 dB; at 0.25 with the drip the earlier bench read 2.5). "0.25:1.6s:0.5" = v37 (the flutter).
SPRING = os.environ.get("C10T1_SPRING", "0.2:1.6s:0.5:1")
if SPRING:
    HANDED += (f" fx.6.kind=spring fx.6.mix={'auto.wet' if ASSEMBLE else SPRING.split(':')[0]} fx.6.decay={SPRING.split(':')[1]}"
               + (f" fx.6.drip={SPRING.split(':')[3]}" if len(SPRING.split(':')) > 3 else ""))
    if CRUNCH_DB == "2dB":
        CRUNCH_DB = f"{2 + float(SPRING.split(':')[2]):g}dB"
EYE = [float(x) for x in EYEFX.split(":")] if EYEFX else []
EYE_TR = ("e5", "e7", "e11") if EYEFX else ("cl5", "cl7", "cl11")
TSTOP = os.environ.get("C10T1_TSTOP", "1")      # a tape stop on the last stab before the hardest stretch (8:52): the whole mix winds down, and the band lands on the bar line
SWARM = os.environ.get("C10T1_SWARM", "-18dB")
# its fader (bar, dB): a crowd is about 3 dB quieter than the same swarm in step, and the approach is busier than the opening
SWARM_LVL = [(0, 0), (12, 0), (24, 4), (30, 4), (350, 5), (383, 5), (385, 3), (389, 0), (NB, 0)]
if os.environ.get("C10T1_SECMIX", "1"):      # under the full band (363-383) it cannot be heard and only thickens 250-500 Hz (its notes are F3 and C4): down 11 dB there, back for the stop
    SWARM_LVL = [(0, 0), (12, 0), (24, 4), (30, 4), (350, 5), (362.5, 5), (364, -6), (382.5, -6), (383, 5), (385, 3), (389, 0), (NB, 0)]
SWARM_NOTES = (53, 60)                                  # F3 and C4
SWARM_LANE = [(0, 3), (2, 2), (24, 1), (30, 0.3), (350, 0.3), (363, 1.0), (383, 1.1), (384, 1.4), (385, 3), (NB, 3)]   # (bar, coupling: 0 a crowd, 1 the critical point, 3 locked)
# v22, THE ATTRACTOR (the engine's `chaos` layer, a Roessler system looping at the note's pitch). Its one control walks the
# route to chaos, and on the way the tone's period multiplies: measured on a held C5, at 1.0 it repeats every FIVE cycles
# (partials at 3/5, 4/5, 6/5, 7/5 of the note), at 0.85 every THREE (2/3, 4/3, 5/3: a fifth below), at 0.4 every TWO (an
# octave below), under 0.2 it is one clean tone. Over the approach's ticks it plays the tune and walks that road backwards:
# five cycles, then three, then (as the seven wheel's guitars come in) two, then (with the five's) one: cycles inside
# cycles folding into one as the wheels close on the landing. It stops where the band and the lead take the tune up
# (kept through the band it put 250-500 Hz 5.2 dB over the records: a pure tone has all its energy in one band). "" = none
ATT = os.environ.get("C10T1_ATT", "-20dB")
ATT_STEPS = [(350, 1.0), (353.5, 0.85), (357, 0.46), (360, 0.1)]
ATT_LVL = [["0b", 0], [f"{356 * 4}b", 0], [f"{358 * 4}b", 3], [f"{NB * 4}b", 3]]        # up 3 dB once the first guitars are in
ATT_LANE = [["0b", 1.0]] + [x for i, (b, v) in enumerate(ATT_STEPS) for x in ([[f"{b * 4 - 2}b", ATT_STEPS[i - 1][1]], [f"{b * 4}b", v]] if i else [[f"{b * 4}b", v]])] + [[f"{NB * 4}b", 0.1]]
CZ = os.environ.get("C10T1_CZ", "-14.5dB")               # a phase-distortion synth (the library's cz-bass) doubling riff C
# (v32: 2.5 dB down from -12dB. At -12 it was louder than the guitars at 500 Hz-1 kHz and cost the mix 2.7 dB there, which is
#  the whole of riff C's reading of 2.4 over the records' instrumental passages; now it is level with the guitars in that band.)
CHIME_GAIN = os.environ.get("C10T1_CHIME", "-19dB")
# the mix against eleven records (stembal.py; compose/chirpers10/sounds.md): peaks as hz:q:dB, comma-separated
GEQ = os.environ.get("C10T1_GEQ", "350:1:-4,750:1.2:-1.5" if STOPS else "350:1:-5,750:1.2:-2.5")   # the rhythm guitars' bus (v20: 1 dB back where the ring was)
BEQ = os.environ.get("C10T1_BEQ", "44:1.5:-7,90:1:7.5,350:1:-8,1500:1:4")     # the bass's bus
# v32: THE GUITARS' WEIGHT AND SCOOP, from the same yardstick as v31 (a guitar heard alone on the record) and from the records'
# own stereo (lowwide.py: how much of a band is side, with no stems). Alone, our rigs had the low F's second harmonic (87 Hz)
# 13 dB under its third, where obZen's and Combustion's guitars have the two level; and in the full mix our 70-110 Hz was
# 12.5 dB more mid than side where eleven records' median is 9.3: the bass was carrying what their guitars carry. And at
# 630-800 Hz our rigs stood 3.7-7.8 dB over all three records' guitars.
# BODY: a peak after each rig, like a cabinet's resonance: Hz : q : tight rig dB : seven's rig : wall rig. It sits on the low
# F's second harmonic and still gives 2-3 dB at Eb's and Ab's. The bass is left as it was (taking its 90 Hz down 1.2 dB put
# it 2 dB under the records' bass stems).  SCOOP: the guitars' bus eq's second band (v31: 750:1.2:-1.5).  "" for each = v31.
# The scoop is HALF what the lone guitars asked for (-4 dB put them within 2-3 dB of the records' at 560-900 Hz), because the
# whole mix said otherwise: at -4 the nine guard windows' 500 Hz-1 kHz went from 1.0 dB off the records on average to 1.3
# (the sections with a voice fell under); at -2.75 it is 1.0 again, centred.
BODY = os.environ.get("C10T1_BODY", "87:3.5:5:5:7")
# v33: A CABINET OF CHIRP'S OWN (Harry, 13 Nov 18:06: "we could theoretically build cab IR into the songs / engine so it can
# count as chirp. if we can get a wholly owned better sounding version then even better"; bead bd-af781d).
# The three heavy rigs stop at their amps (the cabinet files and seven's modelled 2x12 are bypassed, fx.3.mix=0; the patches'
# own eq is flattened, every fx.4 band to 0 dB) and ONE response, the same for all three, follows on the track: a low cut,
# seven peaks and two low-passes, the parts the engine's `cab` is made of. Nothing else: v25's, v31's and v32's track peaks,
# the wall's eq and the guitars' bus eq all go.
# How it was voiced (cabbench.py, cabfit.py, cabfit2.py), from each rig's AMP OUTPUT:
#  - A first fit put the amp outputs straight onto the records' guitar alone (obZen 3:03, Combustion 0:44, Bleed 6:27):
#    1.0 / 1.1 / 1.2 dB from it on average with no other eq. In the mix it was wrong: 2.3 dB over the records at 120-250 Hz,
#    1.4 under at 500 Hz-1 kHz and at 4-8 kHz, and the records' stereo said the same of the low end (too much guitar at
#    110-300 Hz, too little at 70-110). Three short passages on other notes cannot place a low end; eleven records' mixes can.
#  - So: under 315 Hz the target is each rig's low end as v32 had it (set by the records' stereo, tools/lowwide.py), 1 dB
#    fuller at 200-250 Hz; from 315 Hz up, HALFWAY from v32's tone to the record's guitar alone; then 0.8 dB less at 183 Hz
#    and a 2 dB lift at 5.6 kHz, which the mix asked for.
# "" = v32 (the files, and every eq back).
OWNCAB = os.environ.get("C10T1_OWNCAB", "hp cutoff=55 q=1.10|peak cutoff=80 q=1.05 gain=5.0dB|peak cutoff=114 q=2.50 gain=8.1dB|peak cutoff=183 q=1.88 gain=3.4dB|peak cutoff=641 q=2.55 gain=-4.8dB|peak cutoff=2203 q=2.90 gain=2.7dB|peak cutoff=3824 q=1.77 gain=3.4dB|peak cutoff=5600 q=1.40 gain=2.2dB|lp cutoff=2800 q=1.09|lp cutoff=16000 q=0.90")
# v34: THE CABINET IN THE ENGINE (bd-af781d, engine commit f977570f): the same voice and a cone of the same kind as a `cab`
# model, `4x12-modern`, so each track carries one effect in place of thirty eq bands.
# model : distance ; then for the tight rig ; seven's ; the wall:  mic , the left side's cone , the right side's.
# The cones were CHOSEN, as a speaker is: of eight pairs tried on each rig, a pair's 4-8 kHz stood anywhere from level with
# v33's to 1.9 dB under it (twenty peaks and dips do not sum to nothing in every band). These three pairs are the nearest to
# v33's cabinet in four bands from 500 Hz to 8 kHz, each rig on a pair of its own; the tight rig's microphone sits a little
# nearer the cone's centre (0.25) to bring its top level.  "" = v33 (the eq bands).
ENGCAB = os.environ.get("C10T1_ENGCAB", "4x12-modern:0.15;0.25,12,13;0.3,2,3;0.3,14,15")
OWNTRIM = os.environ.get("C10T1_OWNTRIM", "1.8:-1.6:0.7" if ENGCAB else "2.2:-1.4:1.4")     # track gain, dB: tight rig : seven's : wall (each as loud alone as it was)
# THE CONE: a smooth response is not a cabinet. In twelfth-octave bands the records' guitar ripples 1.6-2.9 dB about its own
# average at 0.4-1.6 kHz, 1.1-1.8 at 1.6-3.2 kHz and 2.4-3.1 at 3.2-6.4 kHz (a cone breaking up, a microphone near it); the
# rigs on the cabinet files had the same (2.4 / 1.6 / 1.8 and 4.0 / 1.2 / 2.6), the smooth response a third of it
# (0.9 / 0.6 / 0.9). So each rig, and each side of it, gets its own fixed set of narrow peaks and dips on top:
# seed ; then for each stretch of the range  lowest Hz : highest Hz : how many : depth dB : q from : q to.  They alternate up and
# down, one in each slice of its stretch, so they sum to nothing on average. "" = the smooth response alone.
OWNGRIT = os.environ.get("C10T1_OWNGRIT", "7;450:1600:6:5:5:10;1600:3200:4:5:5:10;3200:7000:10:7:8:14")
def grit(kind, right):
    if not OWNGRIT:
        return []
    parts = OWNGRIT.split(";")
    r = random.Random(int(parts[0]) * 100 + kind * 10 + right)
    out = []
    k = 0
    for part in parts[1:]:
        lo, hi, n, depth, q0, q1 = (float(x) for x in part.split(":"))
        for i in range(int(n)):
            f = lo * (hi / lo) ** ((i + 0.15 + 0.7 * r.random()) / n)
            g = depth * (0.55 + 0.45 * r.random()) * (1 if k % 2 == 0 else -1)
            out.append("peak cutoff=%.0f q=%.1f gain=%.1fdB" % (f, q0 + (q1 - q0) * r.random(), g))
            k += 1
    return out
OWNBITE = os.environ.get("C10T1_OWNBITE", "3000:1.2:-2")       # seven's rig keeps v31's cut at 3 kHz (the hardest stretch's 2-4 kHz)
OWNREAL = os.environ.get("C10T1_OWNREAL", "")                  # peaks for the real string's rig: none needed (it is within 0.5 dB of the first half's)
if OWNCAB:
    TOP = BODY = ""
SCOOP = os.environ.get("C10T1_SCOOP", "730:1:-2.75")     # half of what the guitars alone asked for: see the note below
if SCOOP and GEQ == "350:1:-4,750:1.2:-1.5":
    GEQ = "350:1:-4," + SCOOP
DEQ = os.environ.get("C10T1_DEQ", "400:0.8:-6,5500:0.9:1")                             # the drums' bus, after its clip
DSHELF = os.environ.get("C10T1_DSHELF", "9000:-2")
TUNE_DB = float(os.environ.get("C10T1_TUNE", "-2.5"))
DWIDTH = os.environ.get("C10T1_DWIDTH", "")        # the drums bus's side signal scaled by band, hz:scale,hz:scale
# the kit's top octave was nearly mono and 5 dB heavier on the right, where the china is (the records: about as wide as
# -5 dB side to mid at 6-16 kHz, and 2 dB to the right). So: an overheads' room beside the drums bus that every piece but
# the kick is sent to (low_cut hz : the cymbals' send dB : the snare's and toms' send dB : its decay in s), and the
# cymbals re-placed. The drums bus's own top comes down by what the room adds (DEQ, DSHELF above)
DROOM = os.environ.get("C10T1_DROOM", "5000:4.5:-1.5:0.7")
HATPAN = os.environ.get("C10T1_HATPAN", "")
KPANS = os.environ.get("C10T1_KPANS", "x:0.35,rde:0.4,rb:0.35,h:-0.45")          # the kit's cymbals re-placed, piece:pan,piece:pan (a song-local kit over ct-kit)
MASTER_DB = os.environ.get("C10T1_MASTER", "1")                              # the raw mix (what the groove plays) kept where v6's was
# voices, each its track's gain ("" = off): the bark (8:53), three soft singers on the tune in the eye (6:03), a whisper in the opening
DUCK = os.environ.get("C10T1_DUCK", "6:5")        # while the spoken voice speaks, the guitars' bus and the drums' bus give way by this many dB (guitars:drums)
SPEAK = os.environ.get("C10T1_SPEAK", "-3dB")      # a spoken voice in the rebuild (6:42)
# v50: THE GUITARS SPEAK (palette round; an engine effect the album had not used). Harry's main word on this song:
# "the voice needs work is my main takesway, voice is weak". The weak voice is the spoken one at 6:42 ("Each one keeps
# its own count. None of them wrong."): a calm synthetic talker, dry, over a band coming back, and by presence far the
# loudest thing there (1.5 dB under the whole mix; the next part 7.9). Nothing I could measure made it stronger AS A
# VOICE (a larger throat, a second speaker, a whisper under it: benches at v47 and v49). So it is no longer asked to
# pass for one. The two WALL GUITARS (the rig of the eleven wheel and of every chord left to ring) hold the song's
# open chord through each line, and the engine's cross-synthesis (`morph`, mode `cross`) gives that chord the
# talker's moving spectrum: the guitars say the words. They sound only while the voice does (-88 dB between the
# lines, benched alone). The talker stays under them, 9 dB lower than it was, for its consonants. So the lines the
# bark screams at 9:01 are first said by the machine itself.
# Benched alone (/tmp/lt/cz-t1voice3): a recogniser reads 6 of the 10 words from the speaking guitars (two
# recognisers the same; with the talker under them, 6 again); 8 and 7 from the talker alone. Also benched: a
# MACHINE CHOIR (mode `robot` below: three copies of the line through the phase vocoder's robot on F, C and F), 7
# and 6 words: kept as a switch and as a take on the card; a plain vocoder on the same chord, 0 and 2 words; the
# machine choir through an amp, 0.
# THE EFFECT'S KEY IS A MUTED COPY OF THE LINE (track `spk`), NOT `speak`: a track that is both this effect's key and
# a `duck`'s key panics every window render that uses a preroll (engine.rs, the keyed track's pre-fader buffer is
# empty on that path). Found by halving the song; reported to chirp-eco. With the copy every tool renders.
# mode `cross` ; the chord the guitars hold ; their gain ; the talker's gain under them (it was SPEAK) ; their pan
# mode `robot` ; note:pan:gain dB for each machine, comma-separated ; the talker's gain                 "" = v49.
SPEAKS = os.environ.get("C10T1_SPEAKS", "cross;F1,C2,F2,C3;-3.5dB;-12dB;0.8") if SPEAK else ""
ROBOTS = [x.split(":") for x in SPEAKS.split(";")[1].split(",")] if SPEAKS.startswith("robot") else []
if SPEAKS.startswith("cross"):
    TOP_OF.update({"wsl": 2, "wsr": 2})            # the wall rig's cabinet, cones and trim
# v53: THE LANDING HAS A FLOOR (whole-song round: the piece read stretch by stretch against the records for the
# first time since v20). The piece waits 385 bars for four chords, and under those four chords the bottom of the band
# FELL AWAY: against the riff before them the finished file read 5 to 6 dB less under 60 Hz on the second, third and
# fourth chords (the first has a sub drop; the others had none) and 6 to 9 dB less at 60-120 Hz on all four: one
# stroke of the bass and one of the kick, then a held note dying under eight guitars and a choir. The chords landed
# from the waist up. Now each of the four has the first one's sub drop under it, and the bass strikes with the
# kick again inside the bar and does not sit on one dying note. That mends the bottom octave (all four chords now
# read within 2 dB of the riff under 60 Hz). It does NOT mend 60-120 Hz (still 6 to 8 dB under the riff): that band
# is the kick's and the bass's strokes, and held chords over "the plainest beat there is" have few. Benched and not
# taken: the bass in quarters (1 to 2 dB more there, and four strokes a bar is no longer the plainest beat).
# the drop's velocity on chords two to four (the first's is 0.8) ; the sixteenths of the bar the bass strikes. "" = v52.
FLOOR = os.environ.get("C10T1_FLOOR", "0.8;0,10")
WORD = os.environ.get("C10T1_WORD", "-12dB")       # a choir of fifteen on the landing's chords, singing one word
# the word: "yes" (the answer to "not yet", and nearly its sound). "now" was the first choice, but the larger of two speech
# recognisers heard the choir's "now" as "no", the opposite word, in all three renders tried (the smaller heard "now");
# "yes" both read right in all three
WORD_PH = os.environ.get("C10T1_WORDPH", "Y EH1 S")
BARK = os.environ.get("C10T1_BARK", "1")           # v18: the bark's words, tone and level ("" = the bark as it was in v11-v17)
# its level: while it sings, the voice on eleven records is 9.2 dB under the whole record and 7.1 dB under it at 1-4 kHz
# (their vocal stems against the records); ours was 6.8 and 6.9, and with the new tone at 4 dB it is 8.4 and 7.1
VOX = os.environ.get("C10T1_VOX", "4dB" if BARK else "7dB")
# its words: the patch with sung diction and the speaking voice's articulation (the scream and the false folds stay, and
# its noise, roughness and tilt measure the same). A speech recogniser reads 26-28 of the 35 words from the voice alone; 16 before
VOX_WORDS = os.environ.get("C10T1_VOXWORDS", " synth.layers.0.diction=2 synth.layers.0.speech=1" if BARK else "")
# its tone, against the same eleven voices: ours was 3-5 dB heavy at 250-500 Hz, 3.5 dB short at 1-2 kHz (where words are told
# apart) and 4 dB over at 4-8 kHz; with this it is within 1 dB of them in every band from 120 Hz up
VOX_HP = os.environ.get("C10T1_VOXHP", "440" if BARK else "300")
VOX_EQ = os.environ.get("C10T1_VOXEQ", "1400:0.8:4.5,5500:1.2:-4" if BARK else "")
CHOIR = os.environ.get("C10T1_CHOIR", "-27dB")
WHISPER = os.environ.get("C10T1_WHISPER", "-8dB")
BCOMP = os.environ.get("C10T1_BCOMP", "-26:8:2.5")                                    # threshold:ratio:makeup on the bass's bus, after its eq                         # and a high shelf there, hz:dB


# v19: a wheel is known by its guitar in the quiet too. The five's ticks stay on ct-clean (a neck single coil, a studio clean);
# the seven's go to ct-glass (bridge and middle coils together, a small miked amp); the eleven's to ct-bell (ct-clean
# played in harmonics, written an octave low). "" puts a wheel back on ct-clean
CLEAN7 = os.environ.get("C10T1_CLEAN7", "ct-glass")
CLEAN7_DB = os.environ.get("C10T1_CLEAN7DB", "-3dB")
CLEAN11 = os.environ.get("C10T1_CLEAN11", "ct-bell")
CLEAN11_DB = os.environ.get("C10T1_CLEAN11DB", "-4dB")


def peaks(spec):
    return ["peak cutoff=%s q=%s gain=%sdB" % tuple(x.split(":")) for x in spec.split(",") if x]
# v51: THE BASS'S TONE FOLLOWS THE GROUND (whole song; the fault found on Plain Hunt at its v11 and mended since on the
# album's other four songs: owed here). The bass's bus has an eq fitted on the low F: a cut under the fundamental at
# 44 Hz, a lift on its second harmonic at 90, a cut at 170. On any other ground the note climbs into the lift, the
# compressor after it clamps down, and the bass loses its voice. `tools/keyshape.py` on v50, the bass alone, against
# itself on F: on B flat (bars 122-130 and the like, 22 bars) it lost 4.0 dB at 120-250 Hz and about 3 from there up;
# on D flat (155-163) 5 to 7.5 dB of everything from 250 Hz up; on E flat (232-240, the last climb before the
# landing) 10 to 11 dB of everything from 250 Hz up. Those three eq bands now move with the ground (a lane `key` on
# the bus, in semitones over the low F, read from the bass's own lowest note in each bar), so the eq sits on the note
# as it does on F. The two bands that shape its voice (350 Hz, 1.5 kHz) stay where they are: on Running Total moving
# them too was worse.
# NOT ON D FLAT. Read in the MIX (the full band, v50 against the first cut of this), the bass's regained voice above
# 250 Hz moves nothing: the guitars hold those bands. What the moving eq does change is the low end: about 1 dB from
# 60-120 Hz into 120-250. On B flat and E flat that is toward the eleven records (120-250 Hz was 2.1 and 1.6 dB
# short of them; now 0.8 and 0.3). On D flat it was AWAY from them (60-120 Hz -0.9 -> -2.3, 120-250 +0.5 -> +2.5):
# there the bass turns the eleven wheel with octave jumps, and its upper notes (139 Hz) land in the lift that has
# followed the ground. So on D flat the eq stays where it was.
# on ; the grounds (semitones over F) it does not follow. "" = v50.
KEYEQ = os.environ.get("C10T1_KEYEQ", "1;8")
# AND WHERE SEVEN MEETS ELEVEN, THE ELEVEN HAS A BODY (section 9, bars 154-165, 4:53-5:14). The section is the lead's run
# over the guitars and the kick on the seven wheel "while the bass turns eleven": the eleven wheel had ONE voice, the
# bass, and on this ground (D flat) that bass was the one above with 5 to 7 dB of its voice gone. So the meeting the
# section is named for was a riff in seven with something moving underneath. Now the drummer's left hand turns the
# eleven wheel on the toms with the bass, strike for strike: the floor tom where the bass is on the ground, the high
# tom where it jumps the octave (the two toms are an octave apart, as the bass's two notes are), and the snare
# where the backbeat falls. The right hand keeps four on the ride and the foot keeps seven with the guitars: three
# wheels in one kit.
# the tom on the ground's strikes ; on the octave's ; the velocity of a turn's first strike ; of the others ; their
# gain. "" = v50. (At the fill toms' own level they held the section's 250-500 Hz, 2.7 dB under the whole mix, and put
# the section 0.5 dB up: 4 dB came off at the bench.)
ELEVEN9 = os.environ.get("C10T1_ELEVEN9", "ft;t1;0.85;0.7;-4dB")


def key_f(hz):
    return {"value": float(hz), "mod": [{"src": "auto.key", "amount": round(1 / 12, 5)}]}


def kpeaks(spec, follow):
    """`peaks`, with the first `follow` bands' frequencies on the bus's `key` lane."""
    out = []
    for i, x in enumerate(y for y in spec.split(",") if y):
        hz, q, g = x.split(":")
        out.append({"kind": "peak", "cutoff": key_f(hz), "q": float(q), "gain": g + "dB"} if i < follow else "peak cutoff=%s q=%s gain=%sdB" % (hz, q, g))
    return out


def key_lane():
    """The ground under the bass, bar by bar: its lowest note in each bar, in semitones over the low F; a ground of
    one bar is a passing note and is left out; where the bass rests the last ground holds."""
    low = {}
    for n in T.get("bass", []):
        b = int(n["at"] // 4)
        m = min(NOTE.index(x[:-1]) + 12 * (int(x[-1]) + 1) for x in n["pitch"].split(","))
        low[b] = min(low.get(b, 999), m)
    bars = sorted(low)
    runs = []                                          # [first bar, ground, bars]
    for b in bars:
        if runs and runs[-1][1] == low[b]:
            runs[-1][2] += 1
        else:
            runs.append([b, low[b], 1])
    skip = {int(x) for x in (KEYEQ.split(";") + [""])[1].split(",") if x}
    pts, prev = [["0b", 0]], 0
    for b, g, nb in runs:
        k = 0 if g - F1 in skip else g - F1
        if nb < 2 or k == prev:
            continue
        pts += [[f"{b * 4 - 0.02:g}b", prev], [f"{b * 4:g}b", k]]
        prev = k
    return pts
CL_SENDS = {"dly": "-14dB", "hall": "-12dB"} if CLEAN == "m8-clean" else {"dly": "-9dB", "hall": "-7dB"}   # ct-clean is dry: the song gives it its space


def wet_lane(b0, b1, b2):
    """The low-gain guitars' spring: its usual mix, but from bar b0 to b1 the wetter one, drying by bar b2 (v47)."""
    if not (ASSEMBLE and SPRING):
        return {}
    dry, wet = float(SPRING.split(":")[0]), float(ASSEMBLE.split("|")[2])
    return {"auto": {"wet": {"points": [["0b", dry], [f"{b0 * 4 - 0.5:g}b", dry], [f"{b0 * 4:g}b", wet], [f"{b1 * 4:g}b", wet], [f"{b2 * 4:g}b", dry]], "curve": 0}}}


def song():
    compose()
    if DBL_MAP:              # v54: every first take's part again on its double, except where the second pair already plays it
        trims = [float(v) for v in DBL.split(";")[9:12]]
        excl = []
        for a, z in sorted(DBL_EXCL):          # touching stretches are one stretch (a fader lane wants its points in order)
            if excl and a <= excl[-1][1]:
                excl[-1] = (excl[-1][0], max(z, excl[-1][1]))
            else:
                excl.append((a, z))
        DBL_EXCL[:] = excl
        for x, d in DBL_MAP.items():
            kind = TOP_OF[x]
            if x in SECTION_FADERS:
                SECTION_FADERS[d] = list(SECTION_FADERS[x])
            notes = [dict(n) for n in T.get(x, []) if not any(a * 4 <= n["at"] < z * 4 for a, z in DBL_EXCL)]
            if notes:
                T[d] = notes
            for a, z in DBL_EXCL:      # there the first take plays without its double: it keeps the level it had
                if trims[kind] and any(a * 4 <= n["at"] < z * 4 for n in T.get(x, [])):
                    SECTION_FADERS[x] = sorted(SECTION_FADERS.get(x, []) + [(a, z, -trims[kind])])
    # the hats and the ride have their own faders: at the cymbals' level a closed hat read 27-29 dB under the mix
    # and the ride 23 under (tools/presence.py); the bell stays with the cymbals (it is right in the quiet sections)
    for piece_set, name in ((("h", "hs", "oh", "hf", "h1", "h2", "h3"), "hat"), (("rd", "rde", "rds"), "ride")):
        moved = [n for n in T.get("cym", []) if n["pitch"] in piece_set]
        if moved:
            T[name] = moved
            T["cym"] = [n for n in T["cym"] if n["pitch"] not in piece_set]
    for v in T.values():
        v.sort(key=lambda x: x["at"])
    # the lead's fader: full in its run (4:53); the tune over the riffs TUNE_DB lower (it read as the loudest part there,
    # and the mix 2 dB over the records at 500 Hz-1 kHz); 10 dB down in the eye, where it is nearly alone
    LEAD_LANE = [["0b", TUNE_DB]]
    for b0, b1, v in ((154, 165, 0), (175, 210, -10)):
        LEAD_LANE += [[f"{(b0 - 1) * 4}b", TUNE_DB], [f"{b0 * 4}b", v], [f"{b1 * 4}b", v], [f"{(b1 + 1) * 4}b", TUNE_DB]]
    if TWIN and TWIN_AT:              # v52: the two leads together weigh what the one did
        v = round(TUNE_DB + float(TWIN.split(";")[3]), 2)
        LEAD_LANE += [[f"{TWIN_AT[0] / 4 - 0.5:g}b", TUNE_DB], [f"{TWIN_AT[0] / 4:g}b", v], [f"{TWIN_AT[1] / 4:g}b", v], [f"{TWIN_AT[1] / 4 + 0.5:g}b", TUNE_DB]]
    # the bass's fader, after its compressor (which levels every note, so velocity and the track's gain do nothing):
    # down 2.5 dB under the slow chords at 5:14, where its long notes read 1.5-2 dB over the guitars, then dying away
    BASS_RIDE = [["0b", 0], [f"{164.75 * 4}b", 0], [f"{165 * 4}b", -2.5], [f"{170 * 4}b", -2.5], [f"{175 * 4}b", -7.5], [f"{176 * 4}b", 0]]
    GTR_RIDE = [["0b", 0], [f"{170 * 4}b", 0], [f"{175 * 4}b", -5], [f"{176 * 4}b", 0]]      # and the chords die away into the eye
    # the rotary speaker on those chords: in over the first chord, slow (chorale) for two, spinning up to fast as they fade; out after their tails
    ROT_MIX = [["0b", 0], [f"{165 * 4}b", 0], [f"{166 * 4}b", 1], [f"{177 * 4}b", 1], [f"{178 * 4}b", 0]]
    if ROTARY:        # the cabinet's two microphones give 2.7 dB less than the dry guitars: made up on the same fader
        GTR_RIDE = [["0b", 0], [f"{165 * 4}b", 0], [f"{166 * 4}b", 2.7], [f"{170 * 4}b", 2.7], [f"{175 * 4}b", -2.3], [f"{176 * 4}b", 2.7], [f"{177 * 4}b", 2.7], [f"{178 * 4}b", 0]]
    ROT_SPIN = [["0b", 0], [f"{169.5 * 4}b", 0], [f"{170 * 4}b", 1], [f"{178 * 4}b", 1], [f"{178.5 * 4}b", 0]]
    if RINGS:
        # v24: the other two chords that are struck and left. The piece's first (everything strikes once, together, and is held
        # two bars) and the one held under the bass break (bars 308-314): each sat flat at its full level and then cut off
        # They go on a second fader lane of their own with "curve": 0, which falls in a straight line of dB (see RINGS)
        o, k = (float(x) for x in RINGS.split(":"))
        BASS_RING = [["0b", 0], [f"{0.5 * 4}b", 0], [f"{2 * 4}b", -o], [f"{2.5 * 4}b", -o], [f"{3 * 4}b", 0]]
        GTR_RING = BASS_RING + [[f"{308.5 * 4}b", 0], [f"{314.25 * 4}b", -k], [f"{314.6 * 4}b", -k], [f"{314.9 * 4}b", 0]]
    if ENDING:
        # the chord struck where the approach begins (bar 350, the wall rig alone) dies away over its four bars, and the faders
        # are back up before the first guitars of the approach
        GTR_RIDE += [[f"{350.25 * 4}b", 0], [f"{353.75 * 4}b", -float(ENDING.split(":")[1])], [f"{354.5 * 4}b", -float(ENDING.split(":")[1])], [f"{355.5 * 4}b", 0]]
        # the last chord: held a bar, then dying away to the end of the piece, guitars and bass alike
        last = [[f"{401.5 * 4}b", 0], [f"{402.5 * 4}b", -1], [f"{NB * 4}b", -float(ENDING.split(":")[0])]]
        if ENDLINE and RINGS:       # the alternative: the same fade as a straight line (not the kept ending; for a clip to compare)
            GTR_RING += last
            BASS_RING += last
        else:
            GTR_RIDE += last
            if LANDMIX and SECMIX:      # the landing riff's bass (v30), ahead of the last chord's fade
                BASS_RIDE += [[f"{388.5 * 4}b", 0], [f"{389 * 4}b", float(LANDMIX.split(":")[0])], [f"{400.5 * 4}b", float(LANDMIX.split(":")[0])], [f"{401 * 4}b", 0]]
            BASS_RIDE += last
    if APPROACH:      # v42: the machine approaches (see APPROACH): the guitars' and the bass's faders rise over the wait's last bars
        a0, a1, adb, edb = [float(x) for x in APPROACH.split(":")]
        pts = [[f"{(a0 - 1) * 4:g}b", 0], [f"{a0 * 4 - 1:g}b", adb], [f"{a0 * 4:g}b", adb], [f"{a1 * 4 - 0.125:g}b", edb], [f"{a1 * 4:g}b", 0]]
        assert GTR_RIDE[0] == ["0b", 0] and BASS_RIDE[0] == ["0b", 0]
        GTR_RIDE[1:1] = pts
        BASS_RIDE[1:1] = [list(x) for x in pts]
    if REBUILD:       # v43: the weight comes back (see REBUILD): the guitars' and the bass's faders rise through the rebuild
        r0, r1, rdb = [float(x) for x in REBUILD.split(":")]
        pts = [[f"{r0 * 4 - 2:g}b", 0], [f"{r0 * 4 - 0.5:g}b", rdb], [f"{r0 * 4:g}b", rdb], [f"{r1 * 4:g}b", 0]]
        for ride in (GTR_RIDE, BASS_RIDE):
            ride.extend([list(x) for x in pts])
            ride.sort(key=lambda q: float(q[0][:-1]))
    if NEARER:        # v61: the band comes near (see NEARER): down on the bar line where it enters, rising to the stop, full again inside the two bars of ticks
        n0, n1, ndb, edb = [float(x) for x in NEARER.split(":")[:4]]
        pts = [[f"{n0 * 4 - 0.125:g}b", 0], [f"{n0 * 4:g}b", ndb], [f"{n1 * 4:g}b", edb], [f"{(n1 + 1) * 4:g}b", edb], [f"{(n1 + 1.75) * 4:g}b", 0]]
        for ride in (GTR_RIDE, BASS_RIDE):
            assert not any(n0 * 4 - 0.125 <= float(q[0][:-1]) <= (n1 + 1.75) * 4 for q in ride), "another ride already moves in these bars"
            ride.extend([list(x) for x in pts])
            ride.sort(key=lambda q: float(q[0][:-1]))
    # the tape stop: from the last stab of the second stop-time (bar 279, the twelfth sixteenth) to the bar line
    t0 = (279 + 11 / 16) * 4
    TSTOP_LANE = [["0b", 0], [f"{t0 - 0.01}b", 0], [f"{t0}b", 1], [f"{280 * 4 - 0.01}b", 1], [f"{280 * 4}b", 0]]
    # the stutter: the mirror of the tape stop, at the first stop-time's last stab (bar 109, the twelfth sixteenth, to the bar line)
    t1 = (109 + 11 / 16) * 4
    # (the lane is up half a beat before the slot and down half a beat before the next. The effect reads `chance` once a block
    #  of about 5 ms and decides a slot at its first frame, and a lane moves in a straight line between its points: a lane
    #  that rose 5 ms before the slot was read while still near 0, and its fall was read near 1 at the NEXT slot, so riff C's
    #  first note stuttered instead. chirp-eco read this in the engine; I had called it smoothing.)
    STUT_LANE = [["0b", 0], [f"{t1 - 0.6}b", 0], [f"{t1 - 0.5}b", 1], [f"{t1 + 0.6}b", 1], [f"{t1 + 0.7}b", 0]]
    OHC = {"sends": {"oh": DROOM.split(":")[1] + "dB"}} if DROOM else {}
    OHS = {"sends": {"oh": DROOM.split(":")[2] + "dB"}} if DROOM else {}
    # v36: THE KICK'S CLICK. Against two records' drum stems (kbench.py: this kit in the Bleed and The Faultless
    # reproductions, tools/drumpunch.py) the kick was the kit's furthest part from the record: its sub stood 13 and 19 dB over
    # its click (35-120 Hz against 2-6 kHz in the first milliseconds) where the records' stand 0 and 9. A peak on the kick's
    # track (Hz:q:dB): on that bench, dry, +6 dB gives 9 and 11 and +10 dB gives 6 and 7 (the kick's score 46 -> 54, 69 -> 71).
    # IN THIS SONG the drums' bus clips the kick's peak and the click rides on that peak, so less of it survives: measured
    # on the drums alone through their bus (riff A, 53 clean hits; drumpunch against v35) the kick stood at 14.4 dB, and
    # reads 11.9 at +6 dB and 9.3 at +10 dB, The Faultless's own figure, with its rise (11 ms) and its peak level unchanged.
    # (A copy of the click sent round the clip reached 8.7 and 6.2, and raised the drums' peaks 1 and 3 dB: not taken.)
    # The kick is where the wheels are heard in the drums, so its click is what tells one wheel from another under the
    # guitars. "" = v35.
    KCLICK = os.environ.get("C10T1_KCLICK", "4500:0.8:10")
    KCLICK_FX = {"fx": [{"type": "eq", "bands": peaks(KCLICK)}]} if KCLICK else {}
    AIRFX = ({"fx": [{"type": "eq", "bands": ["highshelf cutoff=%s gain=%sdB" % tuple(CYMAIR.split(";")[0].split(":"))]}]}
             if CYMAIR and CYMAIR.split(";")[0] else {})
    GOUT = {"out": "gtrs"} if GEQ else {}
    PICK_FX = {"fx": [{"type": "eq", "bands": peaks(PICK.split(";")[2])}]} if PICK and len(PICK.split(";")) > 2 and PICK.split(";")[2] else {}
    BOUT = {"out": "low"} if BEQ else {}
    REAL_FX = {"fx": [{"type": "eq", "bands": peaks(REAL5.split(";")[3])}]} if REAL5 and REAL5.split(";")[3] else {}
    POLE_FX = {}
    if POLE:
        pc, pq, pm, ps, pmk, pmk2 = [float(x) for x in POLE.split(":")]
        pole = lambda down, lane: {"type": "barberpole", "bands": 5, "low": 100, "spacing": 1.0, "cycle": f"{pc * 4:g}b", "q": pq, "spread": ps, "down": down,
                                   "mix": {"value": 0, "mod": [{"src": f"auto.{lane}", "amount": 1}]}}
        up = [["0b", pm], [f"{36 * 4}b", pm], [f"{37 * 4}b", 0]]
        dn = [["0b", 0], [f"{400 * 4}b", 0], [f"{401 * 4}b", pm], [f"{NB * 4}b", pm]]
        POLE_FX = {"fx": [pole(False, "up"), pole(True, "dn")] + ([{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.up", "amount": pmk / pm}, {"src": "auto.dn", "amount": pmk2 / pm}]}}] if pmk or pmk2 else []),
                   "auto": {"up": {"points": up, "curve": 0}, "dn": {"points": dn, "curve": 0}}}
    if GRIND and BEQ:
        BOUT = {**BOUT, "sends": {"grind": "0dB"}}
        gh, gd0, gd1, glp, gdb = [float(x) for x in GRIND.split(":")]
        GRIND_LVL = [["0b", -120], [f"{308.5 * 4}b", -120], [f"{308.6 * 4}b", gdb - 8], [f"{312.5 * 4}b", gdb], [f"{314.9 * 4}b", gdb], [f"{315 * 4}b", -120]]
        GRIND_TEETH = [["0b", gd0], [f"{308.5 * 4}b", gd0], [f"{314 * 4}b", gd1], [f"{315 * 4}b", gd1], [f"{315.1 * 4}b", gd0]]
    SPEAK_EQ = {"type": "eq", "bands": ["hp cutoff=" + os.environ.get("C10T1_SPEAKHP", "120"), "peak cutoff=300 q=1 gain=" + os.environ.get("C10T1_SPEAKDIP", "-6" if TIDY else "-2.5") + "dB"]}
    DBL_AMP, DBL_PAN = (f" fx.2.model='{DBL.split(';')[0]}'", float(DBL.split(";")[5])) if DBL_MAP else ("", 0.0)
    spec = [
        ("gl", RIG_L + PICKED, "0dB", -1, {**GOUT, **PICK_FX}), ("gr", RIG_R + PICKED, "0dB", 1, {**GOUT, **PICK_FX}),
        ("gl2", RIG_L + PICKED, "-3dB", -0.8, {**GOUT, **PICK_FX}), ("gr2", RIG_R + PICKED, "-3dB", 0.8, {**GOUT, **PICK_FX}),
        *([("rl", RIG_L + REAL_RIG, "0dB", -1, {**GOUT, **REAL_FX}), ("rr", RIG_R + REAL_RIG, "0dB", 1, {**GOUT, **REAL_FX}),
           ("rl2", RIG_L + REAL_RIG, "-3dB", -0.8, {**GOUT, **REAL_FX}), ("rr2", RIG_R + REAL_RIG, "-3dB", 0.8, {**GOUT, **REAL_FX})] if REAL5 else []),
        *([("el", RIG_L + REAL_RIG + LAND_AMP, "0dB", -1, {**GOUT, **REAL_FX}), ("er", RIG_R + REAL_RIG + LAND_AMP, "0dB", 1, {**GOUT, **REAL_FX}),
           *([("el2", RIG_L + REAL_RIG + f" fx.2.model='{DOUBLE.split(';')[0]}'", "0dB", -float(DOUBLE.split(";")[2]), {**GOUT, **REAL_FX}),
              ("er2", RIG_R + REAL_RIG + f" fx.2.model='{DOUBLE.split(';')[0]}'", "0dB", float(DOUBLE.split(";")[2]), {**GOUT, **REAL_FX})] if DOUBLE else
             [("el2", RIG_L + REAL_RIG + LAND_AMP, "-3dB", -0.8, {**GOUT, **REAL_FX}), ("er2", RIG_R + REAL_RIG + LAND_AMP, "-3dB", 0.8, {**GOUT, **REAL_FX})])] if LAND_MAP else []),
        *([("ql", RIG_L + " synth.layers.0.node=4", SQUEAL, -0.5, GOUT), ("qr", RIG_R + " synth.layers.0.node=4", SQUEAL, 0.5, GOUT)] if SQUEAL else []),
        ("sl", BITE_L, BITE_DB, -1, GOUT), ("sr", BITE_R, BITE_DB, 1, GOUT),
        ("kl", CRUNCH_L + HANDED, CRUNCH_DB, -0.8, wet_lane(360, 360.7, 362.5)), ("kr", CRUNCH_R + HANDED, CRUNCH_DB, 0.8, wet_lane(357, 358.4, 361)),          # not through the guitars' bus: its eq scoops the mids this rig is made of
        ("wl", WALL_L, "-2dB", -0.9, {**GOUT, **({"fx": [{"type": "eq", "bands": peaks(WALL_EQ)}]} if WALL_EQ else {})}),
        ("wr", WALL_R, "-2dB", 0.9, {**GOUT, **({"fx": [{"type": "eq", "bands": peaks(WALL_EQ)}]} if WALL_EQ else {})}),
        *([("dgl", RIG_L + PICKED + DBL_AMP, "0dB", -DBL_PAN, {**GOUT, **PICK_FX}), ("dgr", RIG_R + PICKED + DBL_AMP, "0dB", DBL_PAN, {**GOUT, **PICK_FX}),
           *([("drl", RIG_L + REAL_RIG + DBL_AMP, "0dB", -DBL_PAN, {**GOUT, **REAL_FX}), ("drr", RIG_R + REAL_RIG + DBL_AMP, "0dB", DBL_PAN, {**GOUT, **REAL_FX})] if REAL5 else []),
           ("dsl", BITE_L + DBL_AMP, BITE_DB, -DBL_PAN, GOUT), ("dsr", BITE_R + DBL_AMP, BITE_DB, DBL_PAN, GOUT),
           ("dwl", WALL_L + DBL_AMP, "-2dB", -0.9 * DBL_PAN, {**GOUT, **({"fx": [{"type": "eq", "bands": peaks(WALL_EQ)}]} if WALL_EQ else {})}),
           ("dwr", WALL_R + DBL_AMP, "-2dB", 0.9 * DBL_PAN, {**GOUT, **({"fx": [{"type": "eq", "bands": peaks(WALL_EQ)}]} if WALL_EQ else {})})] if DBL_MAP else []),
        *([("wsl", WALL_L, SPEAKS.split(";")[2], -float(SPEAKS.split(";")[4]), {}),       # not through the guitars' bus: its fader is rising there and it ducks under the voice
           ("wsr", WALL_R, SPEAKS.split(";")[2], float(SPEAKS.split(";")[4]), {})] if SPEAKS.startswith("cross") else []),
        *([("spk", "voice-talk", "0dB", 0, {"fx": [SPEAK_EQ], "mute": True})] if SPEAKS.startswith("cross") else []),
        *[(f"rb{i + 1}", "voice-talk", f"{g}dB", float(pan), {"fx": [SPEAK_EQ, f"pvoc mode=robot pitch={note}"]}) for i, (note, pan, g) in enumerate(ROBOTS)],
        ("bass", BASS, "0.5dB", 0, BOUT),
        ("kick", KIT, "2dB", None, {"out": "drums", **KCLICK_FX}), ("snare", KIT, SNARE.split(";")[2] if SNARE else "8dB", None, {"out": "drums", **({"sends": {**({"oh": SNARE.split(";")[1] + "dB"} if SNARE.split(";")[1] and DROOM else {}), **({"snr": SNARE.split(";")[3].split(":")[1] + "dB"} if SNARE.split(";")[3:] and SNARE.split(";")[3] else {})}} if SNARE else OHS), **({"fx": [({"type": "eq", "bands": [f"highshelf cutoff={f.split(':')[1]} gain={f.split(':')[2]}dB"]} if f.startswith("shelf:") else f) for f in SNARE.split(";")[0].split("|") if f]} if SNARE and SNARE.split(";")[0] else {})}),
        ("cym", KIT, "-3dB", None, {"out": "drums", **OHC, **AIRFX}), ("toms", KIT, "4dB", None, {"out": "drums", **OHS}),
        ("hat", KIT, "14dB", float(HATPAN) if HATPAN else None, {"out": "drums", **OHC, **AIRFX}), ("ride", KIT, "6dB", None, {"out": "drums", **OHC, **AIRFX}),
        ("lead", "m8-lead-guitar", {"value": "-3dB", "mod": [{"src": "auto.eye", "amount": 1}]}, 0, {"sends": {"hall": "-10dB"}, "auto": {"eye": {"points": LEAD_LANE}}}),
        *([("lead2", "m8-lead-guitar", {"value": f"{-3 + float(TWIN.split(';')[0]):g}dB", "mod": [{"src": "auto.eye", "amount": 1}]}, float(TWIN.split(";")[1]),
            {"sends": {"hall": "-10dB"}, "auto": {"eye": {"points": LEAD_LANE}}})] if TWIN else []),
        ("leadw", "ct-lead-wah", {"value": "-3dB", "mod": [{"src": "auto.back", "amount": 1}]} if RETRO and float(RETRO.split(";")[2]) else "-3dB", 0,
         {"sends": {"hall": "-10dB"}, "auto": {"wah": {"points": [[f"{round(t / 4, 3)}b", v] for t, v in WAH_PTS]},
                                              **({"back": {"points": [["0b", 0], [f"{BOUNDS[12] * 4 - 1}b", 0], [f"{BOUNDS[12] * 4}b", float(RETRO.split(";")[2])], [f"{BOUNDS[13] * 4}b", float(RETRO.split(";")[2])],
                                                                      [f"{BOUNDS[13] * 4 + 1}b", 0]], "curve": 0}} if RETRO and float(RETRO.split(";")[2]) else {})}}),
        ("cl5", CLEAN + REALS, "-4dB", -0.45, {"sends": CL_SENDS}),
        ("cl7", (CLEAN7 or CLEAN) + REALS, CLEAN7_DB if CLEAN7 else "-3dB", 0.45, {"sends": CL_SENDS}),
        ("cl11", (CLEAN11 or CLEAN) + REALS, CLEAN11_DB if CLEAN11 else "-3dB", 0, {"sends": CL_SENDS}),
        *([("e5", CLEAN + REALS, f"{-4 + EYE[1]}dB", -0.45,
            {"sends": CL_SENDS, "fx": [{"type": "tremolo", "rate": "1.75b", "depth": EYE[0]}]}),
           ("e7", (CLEAN7 or CLEAN) + REALS, f"{float((CLEAN7_DB if CLEAN7 else '-3dB')[:-2]) + EYE[4]}dB", 0.45,
            {"sends": CL_SENDS, "fx": [{"type": "phaser", "rate": "2.75b", "depth": 0.7, "feedback": EYE[3], "stages": 6, "mix": EYE[2]}]}),
           ("e11", (CLEAN11 or CLEAN) + REALS, f"{float((CLEAN11_DB if CLEAN11 else '-3dB')[:-2]) + EYE[6]}dB", 0,
            {"sends": CL_SENDS, "fx": [{"type": "orbit", "rate": "2.5b", "radius": EYE[5]}]})] if EYEFX else []),
        ("home", "contrabass-tight", "-12dB", 0.3, {"sends": {"hall": "-12dB"}}),
        ("fifth", "cellos", "-15dB", 0.4, {"sends": {"hall": "-8dB"}}),
        ("air", "juno-pad", "-17dB", 0.15, {"sends": {"hall": "-8dB"}, **POLE_FX}),
        ("chime", "modal-glock", CHIME_GAIN, -0.2, {"sends": {"hall": "-6dB", "dly": "-14dB"}}),
        ("vox", "kidman" + VOX_WORDS, VOX or "0dB", 0, {"sends": {"hall": "-18dB"}, "fx": [{"type": "eq", "bands": [f"hp cutoff={VOX_HP}"] + peaks(VOX_EQ) + DTOP_BANDS + ([f"highshelf cutoff={VOX_SHELF.split(':')[0]} gain={VOX_SHELF.split(':')[1]}dB"] if VOX_SHELF else [])}]}),
        ("choir", "voice-backing", CHOIR or "0dB", 0, {"sends": {"hall": "-8dB"}}),
        ("speak", "voice-talk", (SPEAKS.split(";")[3 if SPEAKS.startswith("cross") else 2] if SPEAKS else SPEAK) or "0dB", 0, {"fx": [SPEAK_EQ]}),      # dry: with the hall a recogniser lost "its own count"; the dip: it put the rebuild 3.9 dB over the records at 250-500 Hz
        ("word", "ct-word", {"value": WORD or "0dB", "mod": [{"src": "auto.breath", "amount": 1}]} if ENDING else (WORD or "0dB"), 0,
         {"sends": {"hall": "-8dB"}, "fx": [{"type": "eq", "bands": ["hp cutoff=350"]}],
          **({"auto": {"breath": {"points": [["0b", 0], [f"{402.5 * 4}b", 0], [f"{406 * 4}b", -19], [f"{NB * 4}b", -19]]}}} if ENDING else {})}),      # its notes are C3 F3 C4, on top of the guitars' chord: 250-500 Hz read 3.8 dB over with them in
        ("whisper", "ct-whisper", WHISPER or "0dB", 0, {"sends": {"hall": "-8dB"}}),
        ("att", "ct-attractor", {"value": ATT or "0dB", "mod": [{"src": "auto.lvl", "amount": 1}]}, 0, {"sends": {"hall": "-10dB"}, "auto": {"lock": {"points": ATT_LANE}, "lvl": {"points": ATT_LVL}}}),
        ("swarm", "ct-swarm", {"value": SWARM or "0dB", "mod": [{"src": "auto.lvl", "amount": 1}]}, 0,
         {"sends": {"hall": "-8dB"}, "auto": {"sync": {"points": [[f"{b * 4}b", c] for b, c in SWARM_LANE]}, "lvl": {"points": [[f"{b * 4}b", c] for b, c in SWARM_LVL]}}}),
        ("cz", "cz-bass", CZ or "0dB", 0, {"fx": [{"type": "eq", "bands": ["hp cutoff=420"]}]}),     # its sweep, not its body: the wall rig is thick enough at 250-500 Hz
        ("rise", "ct-swell", "-9dB", 0, {"sends": {"hall": "-10dB"}}),
        ("drop", "ct-drop", "-8dB", 0, {}),
    ]
    if EYE_BARS:
        for third, pan in ((5, .3), (7, -.3), (11, 0)):
            spec.append((f"bar{third}", "modal-vibes synth.amp.r=120ms", EYE_BARS, pan,
                         {"fx": [{"type":"tremolo", "rate":f"{third / 4:g}b", "depth":.72}],
                          "sends": {"hall":"-18dB"}}))
    if RELAY:
        g5, g7 = map(float, RELAY.split(";"))
        for name, patch, db, side in (("relay5", CLEAN, g5, -.72), ("relay7", CLEAN7 or CLEAN, g7, .72)):
            # Switch seats in the silence between the passages. No delay or
            # hall send: keep the handoff distinct from its reflections.
            pan = {"value": 0, "mod": [{"src": "auto.seat", "amount": 1}]}
            lane = {"points": [["0b", side], [f"{BOUNDS[8] * 4}b", side], [f"{BOUNDS[18] * 4}b", -side]], "curve": 0}
            spec.append((name, patch + REALS, f"{db:g}dB", pan, {"auto": {"seat": lane}}))
    if MEET:
        for k, name in enumerate(("meet57", "meet511", "meet711")):
            spec.append((name, "modal-glock", MEET.split(";")[2], float(MEET.split(";")[4].split(",")[k]), {"sends": {"hall": "-6dB", "dly": "-14dB"}}))
    if SEQ:
        spec.append(("seq", "moog-seq fx.0.mix=0.1", SEQ.split(';')[0], float(SEQ.split(';')[2]), {"fx": [{"type": "eq", "bands": [f"hp cutoff={SEQ.split(';')[5]}"]}]}))
    if HANDS:
        spec.append(("hands", "ct-hands", HANDS.split(';')[0], float(HANDS.split(';')[1]), {}))
    tracks = []
    for name, patch, gain, pan, extra in spec:
        if KPANS and patch == KIT:
            patch = "ct-kit-here"
        if name not in T:
            continue
        t = {"name": name, "patch": patch, "gain": gain}
        if pan is not None:
            t["pan"] = pan
        t.update(extra)
        if OWNCAB and name in TOP_OF:
            kind = TOP_OF[name]
            t["patch"] = t["patch"] + " fx.3.mix=0" + "".join(f" fx.4.bands.{i}.gain=0dB" for i in range(4 if kind == 2 else 7))
            right = int(name.rstrip("2").endswith("r"))
            if ENGCAB:
                m, dist = ENGCAB.split(";")[0].split(":")
                mic, *cones = ENGCAB.split(";")[1 + kind].split(",")
                if name in LAND_MAP.values():        # the landing riff's rig has its own microphone and cones
                    mic, *cones = (DOUBLE if DOUBLE and name in ("el2", "er2") else LANDRIG).split(";")[1].split(",")
                if name in DBL_MAP.values():         # v54: a double has another microphone place and its own cones
                    mic, cones = DBL.split(";")[1], DBL.split(";")[2 + kind].split(",")
                cab = {"type": "cab", "model": m, "mic": float(mic), "distance": float(dist)}
                if int(cones[right]):
                    cab["cone"] = int(cones[right])
                t["fx"] = [cab] + ([{"type": "eq", "bands": peaks(OWNBITE)}] if kind == 1 and OWNBITE else []) \
                    + ([{"type": "eq", "bands": peaks(DOUBLE.split(";")[5])}] if DOUBLE and name in ("el2", "er2") and DOUBLE.split(";")[5:] else []) \
                    + ([{"type": "eq", "bands": peaks(DBL.split(";")[12].split(",")[kind])}] if name in DBL_MAP.values() and DBL.split(";")[12:] and DBL.split(";")[12].split(",")[kind] else [])
            else:
                t["fx"] = [{"type": "eq", "bands": OWNCAB.split("|") + grit(kind, right) + (peaks(OWNBITE) if kind == 1 else []) + (peaks(OWNREAL) if OWNREAL and name in ("rl", "rr", "rl2", "rr2") else [])}]
            # the squeal (Ab5, 830 Hz) has its own trim, so it is as loud as it was (it sits in the cabinet's scoop and on its cone's detail)
            gain = t["gain"] = f"{float(gain[:-2]) + float(OWNTRIM.split(':')[kind]) + ((-0.6 if ENGCAB else 0.5) if name in ('ql', 'qr') else 0) + (float(LANDRIG.split(';')[2].split(',')[right]) if name in LAND_MAP.values() and not (DOUBLE and name in ('el2', 'er2')) else 0) + ((float(DOUBLE.split(';')[3].split(',')[right]) if name in ('el2', 'er2') else 0) + float(DOUBLE.split(';')[4]) if DOUBLE and name in LAND_MAP.values() else 0) + ((float(DBL.split(';')[6 + kind].split(',')[right]) if name in DBL_MAP.values() else 0) + float(DBL.split(';')[9 + kind]) if name in DBL_MAP or name in DBL_MAP.values() else 0):g}dB"
        if TOP and name in TOP_OF:
            kind = TOP_OF[name]
            t["patch"] = t["patch"] + " fx.4.bands.3.gain=0dB" + ("" if kind == 2 else " fx.4.bands.6.gain=0dB")
            fx = [dict(f) if isinstance(f, dict) else f for f in t.get("fx", [])]
            if fx and isinstance(fx[0], dict) and fx[0].get("type") == "eq":
                fx[0] = {**fx[0], "bands": list(fx[0]["bands"]) + peaks(TOP.split(";")[kind])}
            else:
                fx = [{"type": "eq", "bands": peaks(TOP.split(";")[kind])}] + fx
            if BODY and float(BODY.split(":")[2 + kind]):
                fx[0] = {**fx[0], "bands": list(fx[0]["bands"]) + peaks(":".join(BODY.split(":")[:2] + [BODY.split(":")[2 + kind]]))}
            t["fx"] = fx
        if name in SECTION_FADERS:
            pts = [["0b", 0]]
            for b0, b1, db in SECTION_FADERS[name]:
                pts += [[f"{(b0 - 0.5) * 4}b", 0], [f"{b0 * 4}b", db], [f"{b1 * 4}b", db], [f"{(b1 + 0.5) * 4}b", 0]]
            t["gain"] = {"value": gain, "mod": [{"src": "auto.sec", "amount": 1}]}
            t["auto"] = {**t.get("auto", {}), "sec": {"points": pts}}
        if SPEAKS.startswith("cross") and name in ("wsl", "wsr"):          # (held) after the rig's cabinet, the voice's spectral envelope
            t["fx"] = list(t.get("fx", [])) + [{"type": "morph", "mode": "cross", "key": "spk", "amount": 1}]
        t["notes"] = T[name]
        tracks.append(t)
    return {
        "about": "chirpers X (Common Time), track 1 by chirper-zero: one steady pulse in 4/4 and three wheels (cells five, seven and eleven sixteenths long) that turn under it for the whole piece and meet, all three on a bar line, only at bar 1 and at the landing 385 bars later. Generated by compose/chirpers10/src/chirpers10-t1.py.",
        "tempo": BPM, "ceiling": "-1dB", "loudness": float(MEET.split(";")[5]) if MEET and MEET.split(";")[5] else float(NEARER.split(":")[4]) if NEARER else -10, "seed": 1, "tail": "4s", "length": f"{NB * 4}b", "event_stable": True,
        "patches": {**STOP_PATCHES,
            **({"ct-hands": {"about": "chirper-three: the library's congas and bongos tuned to the held chord of Common Time's bass break (A flat and E flat): see the generator, v60",
                             "extends": "congas", "kit": {pc: {"pitch": n, "gain": f"{float(g):g}dB"} for pc, n, g in zip(("lo", "mu", "o", "sl", "bl", "bh"), HANDS.split(';')[2].split(','), HANDS.split(';')[3].split(','))}}} if HANDS else {}),
            **({"ct-kit-here": {"extends": KIT, "kit": {x.split(":")[0]: {"pan": float(x.split(":")[1])} for x in KPANS.split(",")}}} if KPANS else {}),
            "ct-whisper": {"about": "chirper-zero: a whisper - the speaking voice with nearly all breath and no effort (what `chirp tts --mode whisper` builds)",
                           "extends": "voice-speech", "synth": {"layers": [{"type": "voice", "speech": 1, "breath": 0.95, "effort": 0.05, "ring": 0.2, "vary": 0.5, "vowel": 0.5, "onset": "expr.on", "coda": "expr.off"}]}},
            "ct-swell": {"about": "chirper-zero: a breath in before a landing - band-passed noise that swells for as long as the note is held (a slow attack), its band rising two octaves, cut off on the bar line",
                         "synth": {"layers": [{"type": "noise"}], "filters": [{"kind": "bp", "cutoff": {"value": 500, "mod": [{"src": "env.up", "amount": 2.5}]}, "q": 0.9}, "hp cutoff=250"],
                                   "env": {"up": {"a": "3.6s", "d": "10ms", "s": 1}}, "amp": {"a": "3.6s", "d": "10ms", "s": 1, "r": "40ms", "curve": 3}}},
            "ct-attractor": {"about": "chirper-zero: the tune's shadow in the approach - a Roessler attractor at the note's pitch whose `amount` (lane auto.lock) walks back from chaos: its period goes five, three, two, one",
                             "synth": {"layers": [{"type": "chaos", "chaos": {"system": "rossler", "axis": "x", "amount": {"value": 0, "mod": [{"src": "auto.lock", "amount": 1}]}}}],
                                       "amp": {"a": "40ms", "d": 0, "s": 1, "r": "400ms"}}, "gain": "-5.5dB"},
            "ct-swarm": {"about": "chirper-zero: the swarm - sixteen saws to a note, each at its own pitch (60 cents' spread), pulled toward their common phase by a coupling the track's `sync` lane sets (0 a crowd, 1 the critical point, 3 locked); a low-pass opens as they agree. After the library's kuramoto-choir, with the lane in place of its LFO.",
                         "synth": {"layers": [{"type": "kuramoto", "kuramoto": {"count": 16, "spread": int(os.environ.get("C10T1_SPREAD", "60")), "coupling": {"value": 0, "mod": [{"src": "auto.sync", "amount": 1}]}}}],
                                   "filters": [{"kind": "lp", "cutoff": {"value": 350, "mod": [{"src": "sync", "amount": 2.6}]}}],
                                   "amp": {"a": "1.5s", "d": 0, "s": 1, "r": "3s"}}, "gain": "-9.5dB"},
            "ct-lead-wah": {"about": "chirper-zero: the library's m8-lead-guitar with a wah pedal between its compressor and its amp (the rest of the chain restated as it is there); the pedal follows the track's `wah` lane, and the playing opens it a little further",
                            "extends": "m8-lead-guitar",
                            "fx": [{"type": "compressor", "threshold": "-24dB", "ratio": 4, "attack": "5ms", "release": "120ms", "makeup": "6dB"},
                                   {"type": "wah", "pos": {"value": 0, "mod": [{"src": "auto.wah", "amount": 1}]}, "env": 0.3, "low": 450, "high": 2400, "q": 3.5, "mix": float(os.environ.get("C10T1_WAHMIX", "1"))},
                                   {"type": "amp", "model": "mark", "gain": 0.9, "boost": "6dB", "bass": 0.45, "mid": 0.7, "treble": 0.55, "presence": 0.55, "resonance": 0.6, "sag": 0.3, "bloom": 0.4, "tight": 100},
                                   {"type": "cab", "model": "4x12", "mic": 0.3, "distance": 0.15},
                                   {"type": "eq", "bands": ["peak cutoff=1.7k q=1.2 gain=-2.5dB", "peak cutoff=340 q=1 gain=2dB"]},
                                   "delay time=3/16 mix=0.25 feedback=0.4 ping_pong=true tone=3k", "reverb mix=0.3 size=0.85"]},
            "ct-word": {"about": "chirper-zero: the landing's choir - the library's voice-choir (five singers on a line) as a three-part open stack, a fourth below and a fifth above the note (fifteen voices), with a slightly smaller tract (0.95: a little brighter)",
                       "extends": "voice-choir synth.layers.0.harmony=[-5,7] synth.layers.0.tract=0.95"},
            "ct-drop": {"about": "chirper-zero: the floor dropping on a landing - a sine that falls an octave to the note in 0.35 s and dies in 1.5 s",
                        "synth": {"layers": [{"wave": "sine"}], "pitch": {"value": 0, "mod": [{"src": "env.fall", "amount": 12}]},
                                  "env": {"fall": {"a": "1ms", "d": "350ms", "s": 0}}, "amp": {"a": "3ms", "d": "1.5s", "s": 0, "r": "200ms"}}}},
        "buses": {"hall": {"fx": ["reverb kind=hall decay=4.5s mix=1 predelay=30ms low_cut=150"]},
                  "dly": {"fx": ["delay time=3/16 feedback=0.35 mix=1 ping_pong=true", "reverb kind=hall decay=3s mix=0.3"]},
                  "drums": {"fx": ["reverb kind=room decay=0.7s mix=0.1 predelay=8ms",
                                   {"type": "glue", "threshold": "-24dB", "ratio": 2.5, "attack": "20ms", "release": "140ms", "knee": 6.0}]
                            + ([f"clip drive=0dB ceiling={DCLIP}dB"] if DCLIP else [])
                            + ([{"type": "eq", "bands": peaks(DEQ) + ([f"highshelf cutoff={DSHELF.split(':')[0]} gain={DSHELF.split(':')[1]}dB"] if DSHELF else []) + DTOP_BANDS}] if DEQ or DSHELF else [])
                            + ([{"type": "width", "width": 1, "mono_below": 0, "bands": [[float(x.split(":")[0]), float(x.split(":")[1])] for x in DWIDTH.split(",")]}] if DWIDTH else [])
                            + ([{"type": "duck", "by": "speak", "depth": f"-{DUCK.split(':')[1]}dB", "attack": "20ms", "release": "250ms"}] if DUCK and SPEAK else [])},
                  **({"grind": {"fx": [{"type": "eq", "bands": [f"hp cutoff={gh:g}"]},
                                       {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.teeth", "amount": 1}]}},
                                       {"type": "drive", "shape": "fold", "drive": 0, "mix": 1},
                                       {"type": "eq", "bands": [f"hp cutoff={gh:g}", f"lp cutoff={glp:g}"]},
                                       {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.lvl", "amount": 1}]}}],
                                "auto": {"lvl": {"points": GRIND_LVL, "curve": 0}, "teeth": {"points": GRIND_TEETH, "curve": 0}}}} if GRIND and BEQ else {}),
                  **({"snr": {"fx": [{"type": "eq", "bands": peaks(SNARE_EQ.split(";")[0]) + ([f"highshelf cutoff={SNARE_EQ.split(';')[1].split(':')[0]} gain={SNARE_EQ.split(';')[1].split(':')[1]}dB"] + DTOP_BANDS if SNARE_EQ.split(";")[1:] else [])} if SNARE_EQ else {"type": "gain", "gain": "0dB"}] if SNARE.split(";")[3].split(":")[0] == "dry" else [f"reverb kind=room decay={SNARE.split(';')[3].split(':')[0]} mix=1 predelay=4ms low_cut={DROOM.split(':')[0]} high_cut=12000 spread=0.6"]}} if SNARE and SNARE.split(";")[3:] and SNARE.split(";")[3] and DROOM else {}),
                  **({"oh": {"fx": [f"reverb kind=room decay={(DROOM.split(':') + ['0.4'])[3]}s mix=1 predelay=4ms low_cut={DROOM.split(':')[0]} high_cut=12000 spread=0.6"] + ([{"type": "eq", "bands": DTOP_BANDS}] if DTOP else [])}} if DROOM else {}),
                  **({"gtrs": {"fx": ([] if OWNCAB else [{"type": "eq", "bands": peaks(GEQ)}]) + [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.ride", "amount": 1}] + ([{"src": "auto.ring", "amount": 1}] if RINGS else [])}}]
                               + ([{"type": "rotary", "mix": {"value": 0, "mod": [{"src": "auto.rot", "amount": 1}]}, "speed": {"value": 0, "mod": [{"src": "auto.spin", "amount": 1}]}}] if ROTARY else [])
                               + ([{"type": "duck", "by": "speak", "depth": f"-{DUCK.split(':')[0]}dB", "attack": "20ms", "release": "250ms"}] if DUCK and SPEAK else []),
                               "auto": {"ride": {"points": GTR_RIDE}, **({"ring": {"points": GTR_RING, "curve": 0}} if RINGS else {}), **({"rot": {"points": ROT_MIX}, "spin": {"points": ROT_SPIN}} if ROTARY else {})}}} if GEQ else {}),
                  **({"low": {"fx": [{"type": "eq", "bands": kpeaks(BEQ, 2) if KEYEQ else peaks(BEQ)}]
                              + ([{"type": "compressor", "threshold": BCOMP.split(":")[0] + "dB", "ratio": float(BCOMP.split(":")[1]), "attack": "12ms", "release": "120ms", "makeup": BCOMP.split(":")[2] + "dB"}] if BCOMP else [])
                              + ([{"type": "eq", "bands": kpeaks(BEQ2, 1) if KEYEQ else peaks(BEQ2)}] if BEQ2 else [])
                              + [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.ride", "amount": 1}] + ([{"src": "auto.ring", "amount": 1}] if RINGS else [])}}],
                              "auto": {"ride": {"points": BASS_RIDE}, **({"ring": {"points": BASS_RING, "curve": 0}} if RINGS else {}),
                                       **({"key": {"points": key_lane(), "curve": 0}} if KEYEQ else {})}}} if BEQ else {})},
        "master": {"fx": [{"type": "eq", "bands": ["hp cutoff=24"]}] + ([{"type": "gain", "gain": f"{MASTER_DB}dB"}] if MASTER_DB else [])
                   + ([{"type": "gain", "gain": f"{MGAIN.split(':')[0]}dB"}, "limiter ceiling=-1dB", {"type": "gain", "gain": f"-{MGAIN.split(':')[1]}dB"}] if MGAIN else [])
                   + ([{"type": "tapestop", "stop": {"value": 0, "mod": [{"src": "auto.stop", "amount": 1}]}, "time": "1.25b"}] if TSTOP else [])
                   + ([{"type": "stutter", "slice": "1/16", "repeats": 5, "pitch": float(STUTTER.split(":")[0]), "roll": float(STUTTER.split(":")[1]), "decay": float(STUTTER.split(":")[2]),
                        "chance": {"value": 0, "mod": [{"src": "auto.stut", "amount": 1}]}}] if STUTTER else []),
                   **({"auto": {**({"stop": {"points": TSTOP_LANE}} if TSTOP else {}), **({"stut": {"points": STUT_LANE}} if STUTTER else {})}} if TSTOP or STUTTER else {})},
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


# v62 (chirper-two; whole song, the instrument under all of it): THE RHYTHM GUITARS HOLD STILL.
# Every string in the library's eight-string family grows a vibrato when a note is held: a fifth of a semitone
# either way at 5.3 Hz, beginning 0.38 s after the stroke and full by 0.83 s. On a lead that is a hand on the neck.
# On a rhythm guitar holding a chord it is nobody: and this piece BEGINS with fourteen guitars holding one chord for
# 3.8 s and ENDS with the same fourteen holding it until it dies, lands on four chords of 1.7 s at 12:13, and its
# wall guitars hold 124 chords of about a second or more in all. Every one wavered, every guitar at the same rate.
# Track fourteen's held chords were stood still in its v3 and the same bench says the same here. So the tight rig,
# seven's rig and the walls, with their doubles (16 tracks: every rhythm guitar that holds a note longer than the
# vibrato's delay; 602 held notes), hold without it. Each take is still struck up to 5 cents off (the library's
# random detune, left on: that is what two takes of one part are), so the pairs still shimmer; they no longer wobble.
# NOT TOUCHED: the leads (a lead sings), the spoken guitars at 6:42 and the one harmonic at 8:52 (the third field),
# and every note shorter than 0.38 s, which never had it. No note, fader or fx is changed.
# MEASURED, by how wide a held chord's spectral lines are (cents holding the middle 80% of the energy round each of
# the six strongest lines between 150 Hz and 1.3 kHz; median). The first chord, the wall guitars alone: 42 -> 10.
# All fourteen guitars on it: 44 -> 17. In the finished file: the first chord 27.5 -> 14.2 (its 392 Hz line 45 -> 10.5),
# a landing chord 38 -> 28, the last chord 30 -> 22. On the records' guitar stems the stretches that are plainly a
# held chord read 3 to 13 (The Faultless 3.1, 3.8, 11.0; Lethargica 13.2). The one-second chords barely show it on
# this measure (51 -> 42 where half a second can resolve 17). Every section's level is within 0.06 dB of v61's and
# the passages with no held guitar null against it (-70 dB or lower); the loudness target is not moved.
# the setting ; the shortest note, in seconds, that counts as held (the library vibrato's delay) ; tracks left as they are. "" = v61.
STILL = os.environ.get("C10T1_STILL", "synth.pitch.mod.2.amount=0;0.38;wsl,wsr,ql,qr" if NEARER else "")


def hold_still(doc):
    """Every rhythm guitar that holds a note long enough for the library's vibrato to begin holds it without one."""
    setting, held, spare = STILL.split(";")
    beat = 60 / doc["tempo"]
    done = []
    for t in doc["tracks"]:
        if (t["patch"].split()[0].rsplit("-", 1)[0] in ("ct-chug", "ct-bite", "ct-wall") and t["name"] not in spare.split(",")
                and any(n["len"] * beat > float(held) for n in t.get("notes") or [])):
            t["patch"] += " " + setting
            done.append(t["name"])
    return done


# v64 (chirper-alpha; palette round: one instrument swapped, in the eye, 5:35.2-6:30.2): IN THE EYE THE TUNE IS PLAYED
# FROM TAPE, AT HALF SPEED AND THEN AT SPEED. The tune is the lead guitar's everywhere, and the eye is the one place it
# is played whole, twice: low, then an octave up. There the driven lead was the only amp left in the room, 10 dB down
# so as not to spoil it. Now it rests for the eye and a keyboard of tapes plays the tune: one flute note recorded for
# each of the tune's six keys (the library's blown flute, 4.2 s, dry), a nested song per key and a `sample` patch per
# key. The second pass plays each tape at speed. The FIRST pass plays the same tapes an octave down, which on a tape is
# half speed: the flute's vibrato is 2.6 Hz there and 5 Hz when the tape comes up to speed, and the octave the tune
# rises at 6:02.7 is the deck doubling its speed. In a piece about time kept, the calm is time slowed. One deck turns
# all the tapes (the track's `tape` fx: 4 cents of wow, so every note sits within 10 cents); the fader puts the tape
# where the guitar stood on the loudness meter (-33.7 and -32.9 K raw against -32.7 and -33.5), which for a flute is
# its fundamental 10 dB clear of everything else in its third-octave (the guitar's read -13 and -2: it was heard by
# its harmonics). NB `--solo tape` renders silence (bd-4942f3): bench it as its own little song (the round's bench).
# the bars whose lead notes go to the tape ; the tape's fader ; the passes of the tune the lead guitar still plays as
# well ("" = neither; "2" = the second) ; the flute's velocity when it was recorded ; the deck's wow and flutter in
# cents and its drift (in units of the wow) ; the loudness target ("" = unchanged) ; settings added to the recorded
# flute's patch ("" = the library's flute as it comes). "" = v63. On only while no older switch of this song is set.
TAPE = os.environ.get("C10T1_TAPE", "175:210;-12dB;;0.7;4,1,0.5;;" if not any(k.startswith("C10T1_") and k not in ("C10T1_OUT", "C10T1_SHOW", "C10T1_TAPE", "C10T1_FINISH", "C10T1_SKIN", "C10T1_HUM", "C10T1_STROKE", "C10T1_FIVE") for k in os.environ) else "")


def the_eye_on_tape(doc):
    """In the eye the tune is played from tape: one flute note recorded for each key, at half speed and then at speed."""
    bars, fader, keeps, vel, deck, target, blown = TAPE.split(";")
    b0, b1 = (int(x) for x in bars.split(":"))
    lead = next(t for t in doc["tracks"] if t["name"] == "lead")
    eye = [n for n in lead["notes"] if b0 * 4 <= n["at"] < b1 * 4]
    second = (176 * 16 + LONG_WAIT_TURNS * 11) / 4                    # the beat the tune's second pass begins on
    lead["notes"] = [n for n in lead["notes"] if n not in eye or ("1" if n["at"] < second else "2") in keeps]
    songs, patches, notes = {}, {}, []
    for n in eye:
        m = NOTE.index(n["pitch"][:-1]) + 12 * (int(n["pitch"][-1]) + 1)
        rec = m if n["at"] >= second else m + 12                      # what the flute played: the second pass's octave
        key = NOTE[m % 12]
        songs[f"ct-tape-{nm(rec)}"] = {"tempo": 60, "length": "4.3b", "tail": "0.2s", "seed": 1, "tracks": [
            {"name": "flute", "patch": ("flute fx.0.mix=0 play.humanize.time=0ms play.humanize.vel=0 " + blown).strip(), "gain": "0dB",
             "notes": [{"at": 0, "len": 4.25, "pitch": nm(rec), "vel": float(vel)}]}]}
        patches[f"ct-tape-{key}"] = {"about": f"chirper-alpha: the tape under the {key} keys - one flute note ({nm(rec)}, 4.2 s), played at speed on {nm(rec)} and at half speed an octave below (see the generator, v64)",
                                     "play": {"gate": 1}, "synth": {"amp": {"a": "6ms", "s": 1, "r": "140ms"},
                                     "layers": [{"type": "sample", "song": f"ct-tape-{nm(rec)}", "root": nm(rec)}]}}
        notes.append({**n, "patch": f"ct-tape-{key}"})
    wow, flutter, drift = deck.split(",")
    doc["patches"].update(dict(sorted(patches.items())))
    tracks = doc.pop("tracks")
    doc["songs"] = dict(sorted(songs.items()))
    doc["tracks"] = tracks + [{"name": "tape", "patch": notes[0]["patch"], "gain": fader, "pan": 0, "sends": dict(lead.get("sends") or {}),
                               "fx": [{"type": "eq", "bands": ["hp cutoff=110", "lp cutoff=6500"]}, f"tape wow={wow} flutter={flutter} drift={drift} tone=7kHz"],
                               "notes": notes}]
    if target:
        doc["loudness"] = float(target)
    return notes


# v65 (chirper-two; section round, the landing, 12:13-12:47: the map's w25, flagged 'little new' and never worked on by a
# section round): THE TUNE IS FINISHED, IN COMMON TIME. The lead's tune is sixteen notes on the eleven wheel (a note a turn;
# the fourth, eighth and twelfth held two turns, the last three). Its last pass, in the approach, is cut off by the stop at
# bar 383: the eighth note sounds for one sixteenth. The other eight notes were never played: the landing had the riff, the
# word and no tune. Now the lead comes back over the landing riff's third and last four-bar phrase (12:36.2) and plays the
# eight notes it was owed, D flat, C, A flat, G flat, F, A flat, G flat, F, in the tune's own rhythm with its unit changed
# from eleven sixteenths to EIGHT, the riff's cell: a note on every one and three, the fourth held a bar. Nothing is placed
# by hand: counted back from the last chord, where the tune's last F belongs, the eight notes begin on the phrase's first
# sixteenth (asserted). FOUND, NOT ARRANGED: the riff's hook under those cells is B, C, E flat, D flat, B, G flat, A flat,
# G flat, then the F chord. The tune over it stands a tone, a UNISON, a fourth, a fourth, a fifth, a major seventh, a UNISON,
# a UNISON, and the chord: the tune and the riff end on the same three notes, A flat, G flat, F, cell for cell (the hook
# sounds on the second beat of its cell, a beat after the tune's note begins).
# THE LEVEL (raw, K, the lead against everything else over each note): in riff B, where the tune is first played, -7.0 dB;
# with all three wheels at 7:47, -7.4; over the landing riff at the fader it had, -8.5. So its fader rides 1.5 dB up for these
# eight notes and it stands where it does the first time it is heard.
# the tune's unit at the landing, sixteenths (eleven everywhere else) ; the lead's velocity ; dB on the lead's fader while it
# plays there ; semitones on the notes ; the last note's length in units ('' = the tune's own three) ; the loudness target
# ('' = unchanged). "" = v64 byte for byte.
FINISH = os.environ.get("C10T1_FINISH", "8;0.85;1.5;0;;" if TAPE else "")
# v66 (chirper-one; instrument round: THE SNARE, 568 strokes; no stroke moves): the drum's note ; overrides inside the
# snare's patch (space separated; 'synth…' is the kit's piece s) ; bands added to its track's eq, band|band ; its fader
# ('' = unchanged) ; the loudness target ('' = unchanged). "" = v65 byte for byte. the_snare_s_skin(doc) runs last.
SKIN = os.environ.get("C10T1_SKIN", "G3;synth.layers.0.mode_count=10 synth.layers.0.slap=0.5 synth.layers.0.decay=0.15s synth.layers.0.damp=0.9 "
                                    "synth.layers.0.contact=0.45 synth.amp.d=125ms synth.filters.1.gain=-2.5dB;peak cutoff=2500 q=1.5 gain=-3dB|"
                                    "peak cutoff=5000 q=1 gain=2dB|peak cutoff=700 q=1.2 gain=-3dB|peak cutoff=1250 q=2 gain=-3dB;8.75dB;" if FINISH else "")


def the_snare_s_skin(doc):
    """v66: the album kit's snare refitted on this song's strokes (tools/snarespec.py against six records' snares)."""
    note, over, bands, fader, target = SKIN.split(";")
    tr = next(t for t in doc["tracks"] if t["name"] == "snare")
    extra = ([f"kit.s.pitch={note}"] if note else []) + [("kit.s.patch." + o if o.startswith("synth") else o) for o in over.split()]
    tr["patch"] = " ".join([tr["patch"]] + extra)
    if bands:
        eq = next(f for f in tr["fx"] if isinstance(f, dict) and f.get("type") == "eq")
        eq["bands"] = list(eq["bands"]) + bands.split("|")
    if fader:
        tr["gain"] = fader
    if target:
        doc["loudness"] = float(target)


# v67 (chirper-two; section round, w2, 0:30-1:00, flagged static and never worked on by a section round; the change
# is 0:41.9-0:54.7): SOMEONE HUMS THE TUNE WHILE THEY WAIT. The piece is a wait, and there is a person in it: a
# whisper says "wait" (0:25.7), "wait" (0:41.0), "not yet" (0:56.0), and 385 bars later "yes". The piece has one
# tune, a note to each turn of the eleven wheel, and nobody plays it until 2:53. Now the person waiting hums it under
# their breath: when the eleven wheel starts to tick (bar 22, 0:41.9, straight after the second "wait") a closed-
# mouth voice hums the tune's first eight notes, a note to each turn of that wheel (C B A flat F -, a breath, G flat
# A flat B C -), an octave under the lead's, and stops. "Not yet." Then the machine arrives. They are the same eight
# notes the lead gets out before the stop cuts it off at 12:09; the other eight are the landing's (v65).
# THE VOICE is the engine's hum (`hum`: the mouth shut, the voice through the nose; no song on this album has used
# it) at 0.8, which keeps a little of the open voice's air: at 1 the hum read as a sine (everything over 1 kHz 32 to
# 40 dB under its fundamental; at 0.8, 16 to 23). Each breath is one syllable carried over four notes (`_`).
#   LEVEL (raw bench, the song's seed, K-weighted): at the first guess (-10 dB) it was as loud as everything else
#       put together (+0.6). At -17 dB each note stands 7.9 to 8.5 dB under everything else, and 0.9 to 6.4 dB OVER
#       everything else in the third of an octave round its own note. The eight notes are evened by note gain: as it
#       comes the hum is 5.8 dB stronger on C4 than on F3 (its murmur resonates near 270 Hz).
#   It adds 1.6 dB to the passage's 250-500 Hz and 0.6 dB to its level (raw; finished, 0.62 dB).
#   THE TARGET -10.093 -> -10.15 is chirper-one's handoff from v66, done here: the new snare had brought every quiet
#       passage up 0.11 dB. At -10.15 the four stretches with no snare in them (the wait before the hum, the eye,
#       11:07-11:31, the end) are within 0.002 dB of v65's (seed 1; 76 to 79 dB left after matching).
# the bar the hum starts on (the eleven wheel must land on it) ; how many of the tune's notes ; semitones from the
# lead's octave ; the voice ; its fader ; its pan ; its eq, band|band ; what is sung on each note (phonemes, | between,
# cycled; '' = the patch's own vowel) ; velocity ; each note's fill, comma separated (cycled) ; its send to the hall
# ('' = none) ; dB on each note, comma separated ('' = none) ; the loudness target ('' = unchanged). "" = v66.
HUM = os.environ.get("C10T1_HUM", "22;8;-12;voice-legato fx.0.mix=0 synth.layers.0.inhale=0 synth.layers.0.hum=0.8;-17dB;0.25;hp cutoff=120;AH1|_|_|_|AH1|_|_|_;0.7;"
                                  "0.97,0.97,0.97,0.8,0.97,0.97,0.97,0.9;-8dB;-3,-1.5,1.5,3,0,1,0,-1.5;-10.15" if SKIN else "")


def the_tune_is_hummed(doc):
    """v67: in the wait, from the bar the eleven wheel comes in on, a voice hums the first half of the tune, a note to
    each turn of eleven, and stops: the whisper says 'not yet'. A new last track; no other note changes."""
    bar, count, semis, patch, fader, pan, bands, ph, vel, fills, hall, trims, target = HUM.split(";")
    t = int(bar) * 16
    assert t % 11 == 0, "the eleven wheel does not land on that bar line"
    fills, phs = [float(x) for x in fills.split(",")], ph.split("|")
    trims = [float(x) for x in trims.split(",")] if trims else [0.0]
    notes = []
    for i, (pitch, turns) in enumerate(LONG_WAIT[:int(count)]):
        n = {"at": round(t / 4, 4), "len": round(turns * 11 * fills[i % len(fills)] / 4, 4), "pitch": nm(pitch + int(semis)), "vel": float(vel)}
        if phs[i % len(phs)]:
            n["ph"] = phs[i % len(phs)]
        if trims[i % len(trims)]:
            n["gain"] = f"{trims[i % len(trims)]:g}dB"
        notes.append(n)
        t += turns * 11
    doc["tracks"].append({"name": "hum", "patch": patch, "gain": fader, "pan": float(pan),
                          **({"fx": [{"type": "eq", "bands": bands.split("|")}]} if bands else {}),
                          **({"sends": {"hall": hall}} if hall else {}), "notes": notes})
    if target:
        doc["loudness"] = float(target)


# v68 (chirper-zero; instrument round: the SEVEN wheel's guitar, `ct-bite`, four tracks: sl, sr and their second takes
# dsl, dsr; 2906 palm-muted strokes of 4686 notes; no note changes). THE SEVEN'S CHUG HOLDS.
# Read one track alone beside the records' muted strokes (tools/riffpunch.py --strokes, `sl`, 2:30-3:20) this rig
# stood furthest of the piece's four: its low end was a thump on the front of the stroke that fell away, where the
# records' chug holds its 100-250 Hz through the stroke (tight +4.80; theirs -1.10, from -2.2 to +0.3), and it had
# little front (punch 2.93; theirs 3.63, from 3.5 to 4.2). (The five's rig, `gl`: +3.08 / 3.09. The wall, `wl`:
# +3.38 / 3.37. The eye's pair, `rl`, the five's rig with a harder pick and a tighter amp: +0.40 / 3.21.) Each
# control benched alone first, one track, the same bars:
#   the string's thump out (0.4 -> 0): tight +2.63, punch held (2.94)
#   the amp's tight (80 Hz as it comes) 190: +2.31 ; with the thump out 150: +1.95, 190: +1.78, 260: +1.00, 330: +1.14
#   the stroke rounder under the palm (soft 0 -> pm x 0.4: from a pick's burst of noise part-way to a displaced
#       string): punch 3.30, tight +4.40 ; with the two above: +0.74
#   the palm's filter two octaves instead of 3.4: more teeth (scoop -7.2 -> -9.5) but punch 2.75: NOT taken
#   the compressor's attack 15 ms, the amp's sag 0.5, the compressor's threshold up: nothing that mattered
# THE COST OF THE TIGHT AMP IS THE CHEST: alone beside the records' guitars (tools/cabspec.py) 2.70 -> 3.84, the
# third-octave at 160 Hz 6.3 dB down. A lift at 170 Hz AFTER the cabinet gives it back (2.71), and a transient
# shaper after that gives the stroke its front (punch 3.54, rise 15 ms; theirs 19.75, from 13.5 to 23.5). With a
# tight of 150-220 and a smaller lift, or with a lift of 8 dB, the stroke rose in 8 to 11.5 ms: a click, outside
# the records' range. Not taken.
# the tracks ; what is added to each one's patch ; bands of a new eq after each one's cabinet and eq, band|band ; fx
# after that, fx|fx ; dB on each fader (so the four alone are as loud as before) ; the loudness target ('' =
# unchanged). "" = v67 byte for byte. On only while HUM is.
STROKE = os.environ.get("C10T1_STROKE", "sl,sr,dsl,dsr;synth.layers.0.thump.mod.0.amount=0 fx.2.tight=260 synth.layers.0.soft=expr.pm*0.4;peak cutoff=170 q=0.9 gain=6dB;transient attack=8 sustain=-1;-2;" if HUM else "")


def the_seven_s_chug_holds(doc):
    """v68: the bite rig's muted stroke, on the rig's own controls (see STROKE). No note changes."""
    names, over, bands, after, fader, target = STROKE.split(";")
    for name in names.split(","):
        t = next(t for t in doc["tracks"] if t["name"] == name)
        assert t["patch"].startswith("ct-bite"), (name, t["patch"])
        if over:
            t["patch"] = t["patch"] + " " + over
        fx = list(t.get("fx") or [])
        if bands:
            fx.append({"type": "eq", "bands": bands.split("|")})
        if after:
            fx += after.split("|")
        t["fx"] = fx
        if fader:
            g = t["gain"]
            if isinstance(g, dict):
                g = dict(g)
                g["value"] = f"{float(g['value'][:-2]) + float(fader):g}dB"
            else:
                g = f"{float(g[:-2]) + float(fader):g}dB"
            t["gain"] = g
    if target:
        doc["loudness"] = float(target)


# v69 (chirper-zero; instrument round: the FIVE wheel's guitar before the eye, `ct-chug`, six tracks: gl, gr, their
# second voices gl2, gr2 and their second takes dgl, dgr: the piece's first riff, 1:09-2:15, and its return against
# the seven at 4:29; 2114 notes, 1284 of them palm-muted, none changed). THE FIVE'S CHUG HOLDS.
# v68's survey left this rig second furthest from the records' muted strokes (riffpunch --strokes, `gl` alone,
# 1:09-1:47): its low end was a thump on the front of the stroke that fell away, where the records' chug holds its
# 100-250 Hz through the stroke (tight +3.08; theirs -1.10, from -2.2 to +0.3).
# THE STRING AND THE PICK ARE NOT TOUCHED, AND THAT IS THE POINT. v29 gave the piece two strings on purpose: before
# the eye the five wheel keeps v25's pick and its rough harmonic string, after it (rl, rr ...) the stiff one, 'so
# the piece has both: riff A at 1:06 on the one, riff A's return at 10:28 on the other'. The eye's pair reads
# +0.40, and its fields on this rig read +0.48 to +1.32: benched, and NOT taken, because they would make the two
# halves one. What is taken is in the chain after the string, one track `gl`, the same bars (rise ms / punch / tight):
#   as it was                                                    19.5 / 3.09 / +3.08
#   the string's thump under the palm out (0.4 -> 0)             21.0 / 3.15 / +2.88
#   the compressor's attack 2 -> 15 ms                           18.75 / 3.14 / +1.53   (8 ms: +1.57 with the thump out)
#   BOTH                                                         20.0 / 3.15 / +0.66   <- KEPT (25 ms: +0.98; thump 0.2: +1.17)
# The rig's compressor sat on every stroke 2 ms in and let the low end up again as it fell: at 15 ms the stroke's
# own front goes through and the hold comes after. Tone alone beside the records' guitars (cabspec) 1.86 -> 1.88,
# the six together -19.3 -> -19.4 LUFS (so 0.1 dB on the faders), their raw peak 0.3 dB lower.
# Benched and left: the amp tighter (260: +3.31, worse on this rig); a rounder pick (soft pm x 0.4: +1.49, and 4.4 dB
# of chest gone at 160 Hz); the amp's resonance, bloom and sag (nothing); a transient shaper after the cabinet
# (punch 3.51, in the records' 3.5-4.2, for a raw peak 2 dB higher: waits for an ear on the album's other fronts).
# the tracks ; fields of each one's patch (one already there is replaced) ; bands of a new eq after each one's
# cabinet and eq, band|band ; fx after that, fx|fx ; dB on each fader (the six alone as loud as before) ; the
# loudness target ('' = unchanged). "" = v68 byte for byte. On only while STROKE is. The target: with the strokes'
# fronts through, the master gave the rest of the song 0.006 to 0.016 dB less (the quiet stretches most), so the
# target goes from -10.15 to -10.1392 and every stretch the six do not play in is within 0.005 dB of v68.
FIVE = os.environ.get("C10T1_FIVE", "gl,gr,gl2,gr2,dgl,dgr;fx.1.attack=15ms synth.layers.0.thump.mod.0.amount=0;;;0.1;-10.1392" if STROKE else "")


def the_five_s_chug_holds(doc):
    """v69: the five's rig before the eye: the compressor lets the stroke's front through and the palm's thump is out (see FIVE). No note changes; the string and the pick are v25's."""
    names, over, bands, after, fader, target = FIVE.split(";")
    for name in names.split(","):
        t = next(t for t in doc["tracks"] if t["name"] == name)
        assert t["patch"].startswith("ct-chug"), (name, t["patch"])
        toks = t["patch"].split(" ")
        keys = [x.split("=", 1)[0] for x in toks]
        for f in over.split(" ") if over else []:
            k = f.split("=", 1)[0]
            if k in keys:
                toks[keys.index(k)] = f
            else:
                toks.append(f)
                keys.append(k)
        t["patch"] = " ".join(toks)
        fx = list(t.get("fx") or [])
        if bands:
            fx.append({"type": "eq", "bands": bands.split("|")})
        if after:
            fx += after.split("|")
        if bands or after:
            t["fx"] = fx
        if fader:
            g = t["gain"]
            if isinstance(g, dict):
                g = dict(g)
                g["value"] = f"{float(g['value'][:-2]) + float(fader):g}dB"
            else:
                g = f"{float(g[:-2]) + float(fader):g}dB"
            t["gain"] = g
    if target:
        doc["loudness"] = float(target)


def the_tune_is_finished(doc):
    """The lead's last pass of the tune is cut off at the stop before the landing, eight notes in. The other eight are played
    over the landing riff's last four bars, a note to each cell of EIGHT, and the last one falls on the last chord."""
    unit, vel, db, semis, last, target = FINISH.split(";")
    unit = int(unit)
    lead = next(t for t in doc["tracks"] if t["name"] == "lead")
    cut = lead["notes"][-1]                                           # where it broke off: the eighth note, one sixteenth of it
    assert cut["pitch"] == nm(LONG_WAIT[7][0]) and cut["at"] == (383 * 16 - 1) / 4 and cut["len"] == 0.25, cut
    owed = LONG_WAIT[8:]                                              # D flat, C, A flat, G flat (two units), F, A flat, G flat, F (three)
    chord = (385 + 16) * 16                                           # the last chord
    t = chord - sum(turns for _, turns in owed[:-1]) * unit           # counted back from it: the last note is the chord's
    assert unit != 8 or t == (385 + 12) * 16                          # in units of eight that is the riff's last four-bar phrase, to the sixteenth
    start = t
    for i, (pitch, turns) in enumerate(owed):
        if i == len(owed) - 1 and last:
            turns = float(last)
        lead["notes"].append({"at": round(t / 4, 4), "len": round(turns * unit / 4, 4), "pitch": nm(pitch + int(semis)), "vel": float(vel)})
        t += turns * unit
    if float(db):
        pts = lead["auto"]["eye"]["points"]
        base = pts[-1][1]
        lead["auto"]["eye"]["points"] = pts + [[f"{start / 4 - 0.5:g}b", base], [f"{start / 4:g}b", base + float(db)]]
    if target:
        doc["loudness"] = float(target)


if __name__ == "__main__":
    doc = song()
    if STILL:
        hold_still(doc)
    if TAPE:
        the_eye_on_tape(doc)
    if FINISH:
        the_tune_is_finished(doc)
    if SKIN:
        the_snare_s_skin(doc)
    if HUM:
        the_tune_is_hummed(doc)
    if STROKE:
        the_seven_s_chug_holds(doc)
    if FIVE:
        the_five_s_chug_holds(doc)
    open(OUT, "w").write(dump(doc))
