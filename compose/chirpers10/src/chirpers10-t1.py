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


def gtr(trs, p, cell, b0, b1, root=F1, hook=H1, vel=0.85, ramp=None, rig=None, dyn=(1.0, 1.05)):
    s0, s1 = s16(b0), s16(b1)
    for t, ln, kind, j, hi in strikes(p, cell, s0, s1):
        v = vel * (1.0 if j == 0 else 0.9)
        if ramp:
            v *= ramp[0] + (ramp[1] - ramp[0]) * (t - s0) / max(1, s1 - s0)
        for tr in trs:
            if rig:
                tr = rig.get(tr, tr)
            elif p == 7 and BITE_L:
                tr = SEVEN_RIG.get(tr, tr)        # a wheel is known by its rig: five ct-chug, seven ct-bite, eleven ct-wall
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
        add(tr, t, 1.8, root + notes[j % len(notes)], v)


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


def long_wait(b0, b1, vel=0.75, up=0, start=None, tr="lead"):
    """The lead's tune: one note to each turn of the eleven wheel (some held for two or three turns)."""
    s0, s1 = s16(b0), s16(b1)
    t = s0 + (-s0) % 11 if start is None else start
    i = 0
    while t < s1:
        pitch, turns = LONG_WAIT[i % len(LONG_WAIT)]
        add(tr, t, min(turns * 11, s1 - t), pitch + up, vel)
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
            idx += steps[k]
        if t + span < s1:
            add(tr, t + span, min(turns * 7 - span - 0.3, s1 - t - span), SOLO_SCALE[idx % 6] + 12 * (idx // 6), vel)
        if t < s1:          # the pedal opens through each flurry and closes slowly over the note it lands on
            WAH_PTS.extend([(t, 0.1), (min(t + span, s1), 1.0), (min(t + turns * 7 - 0.5, s1), 0.25)])
        t += turns * 7


def chimes(b0, b1, pairs=((5, 7), (5, 11), (7, 11)), vel=0.5):
    """Coincidences: wherever two wheels begin a turn on the same sixteenth, a struck bar sounds, one pitch to each
    pair (five and seven C, five and eleven Ab, seven and eleven F). All three coincide only at the first bar line
    and at the landing."""
    pitch = {(5, 7): 84, (5, 11): 80, (7, 11): 89}
    s0, s1 = s16(b0), s16(b1)
    for p, q in pairs:
        for t in range(s0 + (-s0) % (p * q), s1, p * q):
            if t % 385:
                add("chime", t, 8, pitch[(p, q)], vel)


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


def compose():
    B = BOUNDS
    F_ONLY = [(0, 0)]

    # 1. 0-35  THE WAIT BEGINS: everything strikes once, together; then only the wheels, ticking, one by one
    hit(0)
    bed(F_ONLY, 35 * 16)
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
    kit(a, z, "x", 4, "half", "roll")
    for t in landings(5, a * 16 + 1, z * 16):
        crash(t, 0.8)

    # 3. 55-70  five meets eleven: the five wheel thickens, and eleven arrives as open chords left to ring
    a, z = B[2], B[3]
    gtr(G, 5, FIVE_B, a, z, hook=H1)
    gtr(WL, 11, ELEVEN_W, a, a + 11, vel=0.9)
    gtr(WL, 11, [(0, 8, "P"), (8, 2, "d")], a + 11, z, vel=0.9)       # after eleven lands, each chord is answered by a stab
    bass(5, FIVE_A, a, z, hook=H1)
    kick(5, FIVE_B, a, z)
    kit(a, z, "x", 4, "half", "toms")
    for t in landings(11, a * 16 + 1, z * 16):
        crash(t, 0.85)

    # 4. 70-77  five and seven meet: seven bars of the seven wheel, nearly alone (one guitar, bass, kick, ghosted snare), up on Ab
    a, z = B[3], B[4]
    gtr(("gl",), 7, SEVEN_A, a, z, root=AB, hook=H2, vel=0.8, rig=CRUNCH, dyn=SOFT)       # on the low-gain rig: the chugs soft, the hook hard
    gtr(("gr",), 7, SEVEN_A, a + 4, z, root=AB, hook=H2, vel=0.8, rig=CRUNCH, dyn=SOFT)
    bass(7, SEVEN_A, a, z, root=AB, hook=H2)
    kick(7, SEVEN_A, a, z)
    kit(a, z, "h", 2, "half", "kicks", cvel=0.5, ghost=True, crash_at_start=False)
    crash(a * 16, 0.7, "sp")

    # 5. 77-105  seven meets eleven: RIFF B, guitars on seven, the bass on eleven; the lead's tune arrives halfway
    a, z = B[4], B[5]
    gtr(G, 7, SEVEN_B, a, z, hook=H2)
    bass(11, ELEVEN_A, a, z, hook=OCT)
    kick(7, SEVEN_B, a, z)
    kit(a, a + 14, "rb", 4, "half", None, cvel=0.6)
    kit(a + 14, z, "x", 4, "half", "run")
    long_wait(a + 14, z)
    harm(G2, 7, SEVEN_B, a + 21, z, 12, hook=H2, vel=0.75)            # the last seven bars: the hook doubled an octave up
    for t in landings(7, a * 16 + 1, z * 16):
        crash(t, 0.8)

    # 6. 105-110  five and seven meet: stop-time. Sixteen stabs on the five wheel, silence between
    a, z = B[5], B[6]
    gtr(G + G2, 5, FIVE_S, a, z, vel=0.95)
    bass(5, FIVE_S, a, z, vel=0.95)
    kick(5, FIVE_S, a, z, vel=0.95)
    for t, ln, kind, j, hi in strikes(5, FIVE_S, a * 16, z * 16):
        add("cym", t, 2, "cch", 0.75)
    rise(z, 1)

    # 7. 110-140  five meets eleven: RIFF C, the splayed one. Eleven everywhere for eleven bars; then the kick slips onto five
    a, z = B[6], B[7]
    for (x, y, root, hook) in ((a, a + 11, F1, H1), (a + 11, a + 22, F1 + 5, H3), (a + 22, z, F1, H1)):
        gtr(WL, 11, ELEVEN_A, x, y, root=root, hook=hook)               # the riff itself on the wall rig, alone at first
        if x > a:
            gtr(G2, 11, ELEVEN_W, x, y, root=root, vel=0.9)             # the open chords join when the ground moves
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

    # 9. 154-165  seven meets eleven: the lead runs on the seven wheel while the bass turns eleven; the ground moves to Db
    a, z = B[8], B[9]
    gtr(G, 7, SEVEN_A, a, z, root=DB, hook=H2)
    bass(11, ELEVEN_A, a, z, root=DB, hook=OCT)
    kick(7, SEVEN_A, a, z)
    kit(a, z, "rd", 4, "half", "run", cvel=0.6)
    solo(a, z)

    # 10. 165-175  five meets eleven: the weight comes off, slowly. No riff: one chord to each turn of the eleven wheel,
    #     left to ring, on the wall rig, the drums in half time. The chords are the eye's, heard heavy before they are
    #     heard clean: Db (where the lead's run stood), Ab, Gb, home
    a, z = B[9], B[10]
    doom = [(a * 16, DB), (a * 16 + 44, AB), (a * 16 + 88, GB), (a * 16 + 121, F1)]
    for i, (t0, root) in enumerate(doom):
        t1 = doom[i + 1][0] if i + 1 < len(doom) else z * 16
        fade = 1.0 - 0.45 * (t0 - a * 16) / 160
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
    tick("cl5", 5, TICK5, CL5, a, z, harmony=eye)
    tick("cl7", 7, TICK7, CL7, a, z, harmony=eye)
    tick("cl11", 11, TICK11, CL11_OPEN, a + 12, z, vel=0.36, harmony=eye)
    chimes(a, z - 2, pairs=((5, 7),))
    chimes(a + 12, z - 2, pairs=((5, 11), (7, 11)))
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

    # 13. 220-231  five meets eleven: the splayed riff again, filled in, its hook doubled above; on Bb
    a, z = B[12], B[13]
    gtr(WL, 11, ELEVEN_B, a, z, root=BB, hook=H1)
    gtr(G2, 11, ELEVEN_W, a, a + 5, root=BB, vel=0.9)
    harm(G2, 11, ELEVEN_B, a + 5, z, 12, root=BB, hook=H1)
    bass(11, ELEVEN_B, a, z, root=BB, hook=H1)
    kick(11, ELEVEN_B, a, z)
    kit(a, z, "x", 4, "half", "kicks")

    # 14. 231-245  seven meets eleven: seven on the guitars over eleven's chords; double time; on Eb (F, Bb, Eb: up by fourths, then home)
    a, z = B[13], B[14]
    gtr(G, 7, SEVEN_B, a, z, root=EB, hook=H3)
    gtr(WL, 11, [(0, 8, "P"), (8, 2, "d")], a, z, root=EB, vel=0.9)
    bass(7, SEVEN_B, a, z, root=EB, hook=H3)
    kick(7, SEVEN_B, a, z)
    kit(a, z, "x", 2, "back", "run", cvel=0.55)

    # 15. 245-275  five meets seven: all three. Five left, seven right, eleven in the bass, and the tune over them
    a, z = B[14], B[15]
    gtr(("gl",), 5, FIVE_B, a, z, hook=H1)
    gtr(("gr",), 7, SEVEN_B, a, z, hook=H2)
    bass(11, ELEVEN_A, a, z, hook=OCT)
    kick(5, FIVE_B, a, z)
    kit(a, a + 15, "rde", 4, "half", None, cvel=0.6)
    kit(a + 15, z, "x", 4, "half", "run16", crash_at_start=False)
    long_wait(a, z, vel=0.8)
    harm(G2, 5, FIVE_B, a + 15, z, 12, hook=H1, vel=0.72)
    for t in landings(5, a * 16 + 1, z * 16):
        crash(t, 0.8)

    # 16. 275-280  five meets eleven: stop-time again, with a dissonant chord and the toms in the gaps
    a, z = B[15], B[16]
    gtr(G, 5, FIVE_S, a, z, vel=0.95)
    gtr(G2, 5, [(0, 2, "d")], a, z, vel=0.9)
    bass(5, FIVE_S, a, z, vel=0.95)
    kick(5, FIVE_S, a, z, vel=0.95)
    for t, ln, kind, j, hi in strikes(5, [(0, 2, "p"), (2, 1, "c"), (3, 1, "c"), (4, 1, "c")], a * 16, z * 16):
        if j == 0:
            add("cym", t, 2, "cch", 0.75)
        else:
            add("toms", t, 1, ["t1", "t2", "ft"][j - 1], 0.7)

    # 17. 280-308  five meets seven: the hardest stretch. Seven everywhere, the kick running sixteenths; up a semitone
    #     and back; the last seven bars the snare goes to the off-beats
    a, z = B[16], B[17]
    for (x, y, root) in ((a, a + 14, F1), (a + 14, a + 21, F1 + 1), (a + 21, z, F1)):
        if x > a:
            crash(x * 16, 0.9)
        gtr(G + G2, 7, SEVEN_B, x, y, root=root, hook=H2, vel=0.92)
        bass(7, SEVEN_B, x, y, root=root, hook=H2, vel=0.92)
    kick(7, SEVEN_B, a, z, fill16=True)
    kit(a, a + 21, "x", 2, "back", None, cvel=0.58)
    kit(a + 21, z, "x", 4, "blast", "roll16", cvel=0.66, crash_at_start=False)
    if VOX:
        vox(a)

    # 18. 308-315  seven meets eleven: seven bars for the bass, on eleven, under one held chord; on Ab, like the first break
    a, z = B[17], B[18]
    for tr in WL:
        add(tr, a * 16, 7 * 16 - 12, "Ab1,Eb2,Ab2,Eb3", 0.9)
    bass(11, ELEVEN_B, a, z, root=AB, hook=H1, vel=0.95)
    kick(11, ELEVEN_A, a, z)
    kit(a, z, "h", 2, "half", "toms", cvel=0.5, ghost=True)

    # 19. 315-330  five meets seven: the two guitars swap wheels (seven left, five right) over a floor-tom pulse
    a, z = B[18], B[19]
    gtr(("gl",), 7, SEVEN_A, a, z - 0.5, hook=H2)
    gtr(("gr",), 5, FIVE_A, a, z - 0.5, hook=H1)
    bass(5, FIVE_A, a, z - 0.5, hook=H1)
    kick(5, FIVE_A, a, z - 0.5)
    kick(7, SEVEN_A, a, z - 0.5, only_first=True)
    kit(a, z, "ft", 4, "half", "stop", cvel=0.58, ghost=True)                 # no cymbals: the pulse is on the floor tom

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
    bass(11, ELEVEN_A, 357, 363, hook=OCT, vel=0.75)                  # the bass comes in with the first guitar
    gtr(("gr",), 7, SEVEN_B, 357, 363, hook=H2, vel=0.9, ramp=(0.6, 1.0), rig=CRUNCH, dyn=SOFT)    # the first guitars back are the low-gain rig;
    gtr(("gl",), 5, FIVE_B, 360, 363, hook=HX, vel=0.9, ramp=(0.7, 1.0), rig=CRUNCH, dyn=SOFT)     # the high-gain ones come with the band at 363
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
    bed([((a + 16) * 16, 0)], NB * 16)
    tick("cl5", 5, TICK5, CL5, a + 17, NB - 1, ramp=(1.0, 0.4))
    tick("cl7", 7, TICK7, CL7, a + 17, NB - 1, ramp=(1.0, 0.4))
    chimes(a + 17, NB - 1, pairs=((5, 7),), vel=0.4)


# synth layers (Harry, 12 Nov: "layered synths / tones ... a showcase of all features"), each its track's gain ("" = off)
# THE SWARM: sixteen oscillators to a note, each at its own pitch, pulled toward their common phase by a coupling that a lane
# rides (the engine's Kuramoto model of synchrony). At bar 1 they are in step; over the wait they drift into a crowd; from
# the approach they are pulled back, and lock as the three wheels land.
# effects where the music asks for them (Harry: "a showcase of all features"), each with a switch ("" = off)
WAH = os.environ.get("C10T1_WAH", "1")          # a wah on the lead's run (4:53): the pedal opens through each flurry and closes on the held note
ROTARY = os.environ.get("C10T1_ROTARY", "1")    # a rotary speaker on the slow chords (5:14): it comes in over the first chord and spins up as they fade
TSTOP = os.environ.get("C10T1_TSTOP", "1")      # a tape stop on the last stab before the hardest stretch (8:52): the whole mix winds down, and the band lands on the bar line
SWARM = os.environ.get("C10T1_SWARM", "-18dB")
# its fader (bar, dB): a crowd is about 3 dB quieter than the same swarm in step, and the approach is busier than the opening
SWARM_LVL = [(0, 0), (12, 0), (24, 4), (30, 4), (350, 5), (383, 5), (385, 3), (389, 0), (NB, 0)]
SWARM_NOTES = (53, 60)                                  # F3 and C4
SWARM_LANE = [(0, 3), (2, 2), (24, 1), (30, 0.3), (350, 0.3), (363, 1.0), (383, 1.1), (384, 1.4), (385, 3), (NB, 3)]   # (bar, coupling: 0 a crowd, 1 the critical point, 3 locked)
CZ = os.environ.get("C10T1_CZ", "-12dB")                 # a phase-distortion synth (the library's cz-bass) doubling riff C
CHIME_GAIN = os.environ.get("C10T1_CHIME", "-19dB")
# the mix against eleven records (stembal.py; compose/chirpers10/sounds.md): peaks as hz:q:dB, comma-separated
GEQ = os.environ.get("C10T1_GEQ", "350:1:-5,750:1.2:-2.5")                  # the rhythm guitars' bus
BEQ = os.environ.get("C10T1_BEQ", "44:1.5:-7,90:1:7.5,350:1:-8,1500:1:4")     # the bass's bus
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
VOX = os.environ.get("C10T1_VOX", "7dB")
CHOIR = os.environ.get("C10T1_CHOIR", "-27dB")
WHISPER = os.environ.get("C10T1_WHISPER", "-8dB")
BCOMP = os.environ.get("C10T1_BCOMP", "-26:8:2.5")                                    # threshold:ratio:makeup on the bass's bus, after its eq                         # and a high shelf there, hz:dB


def peaks(spec):
    return ["peak cutoff=%s q=%s gain=%sdB" % tuple(x.split(":")) for x in spec.split(",") if x]
CL_SENDS = {"dly": "-14dB", "hall": "-12dB"} if CLEAN == "m8-clean" else {"dly": "-9dB", "hall": "-7dB"}   # ct-clean is dry: the song gives it its space


def song():
    compose()
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
    # the bass's fader, after its compressor (which levels every note, so velocity and the track's gain do nothing):
    # down 2.5 dB under the slow chords at 5:14, where its long notes read 1.5-2 dB over the guitars, then dying away
    BASS_RIDE = [["0b", 0], [f"{164.75 * 4}b", 0], [f"{165 * 4}b", -2.5], [f"{170 * 4}b", -2.5], [f"{175 * 4}b", -7.5], [f"{176 * 4}b", 0]]
    GTR_RIDE = [["0b", 0], [f"{170 * 4}b", 0], [f"{175 * 4}b", -5], [f"{176 * 4}b", 0]]      # and the chords die away into the eye
    # the rotary speaker on those chords: in over the first chord, slow (chorale) for two, spinning up to fast as they fade; out after their tails
    ROT_MIX = [["0b", 0], [f"{165 * 4}b", 0], [f"{166 * 4}b", 1], [f"{177 * 4}b", 1], [f"{178 * 4}b", 0]]
    if ROTARY:        # the cabinet's two microphones give 2.7 dB less than the dry guitars: made up on the same fader
        GTR_RIDE = [["0b", 0], [f"{165 * 4}b", 0], [f"{166 * 4}b", 2.7], [f"{170 * 4}b", 2.7], [f"{175 * 4}b", -2.3], [f"{176 * 4}b", 2.7], [f"{177 * 4}b", 2.7], [f"{178 * 4}b", 0]]
    ROT_SPIN = [["0b", 0], [f"{169.5 * 4}b", 0], [f"{170 * 4}b", 1], [f"{178 * 4}b", 1], [f"{178.5 * 4}b", 0]]
    # the tape stop: from the last stab of the second stop-time (bar 279, the twelfth sixteenth) to the bar line
    t0 = (279 + 11 / 16) * 4
    TSTOP_LANE = [["0b", 0], [f"{t0 - 0.01}b", 0], [f"{t0}b", 1], [f"{280 * 4 - 0.01}b", 1], [f"{280 * 4}b", 0]]
    OHC = {"sends": {"oh": DROOM.split(":")[1] + "dB"}} if DROOM else {}
    OHS = {"sends": {"oh": DROOM.split(":")[2] + "dB"}} if DROOM else {}
    GOUT = {"out": "gtrs"} if GEQ else {}
    BOUT = {"out": "low"} if BEQ else {}
    spec = [
        ("gl", RIG_L, "0dB", -1, GOUT), ("gr", RIG_R, "0dB", 1, GOUT),
        ("gl2", RIG_L, "-3dB", -0.8, GOUT), ("gr2", RIG_R, "-3dB", 0.8, GOUT),
        ("sl", BITE_L, BITE_DB, -1, GOUT), ("sr", BITE_R, BITE_DB, 1, GOUT),
        ("kl", CRUNCH_L, CRUNCH_DB, -0.8, {}), ("kr", CRUNCH_R, CRUNCH_DB, 0.8, {}),          # not through the guitars' bus: its eq scoops the mids this rig is made of
        ("wl", WALL_L, "-2dB", -0.9, GOUT), ("wr", WALL_R, "-2dB", 0.9, GOUT),
        ("bass", BASS, "0.5dB", 0, BOUT),
        ("kick", KIT, "2dB", None, {"out": "drums"}), ("snare", KIT, "8dB", None, {"out": "drums", **OHS}),
        ("cym", KIT, "-3dB", None, {"out": "drums", **OHC}), ("toms", KIT, "4dB", None, {"out": "drums", **OHS}),
        ("hat", KIT, "14dB", float(HATPAN) if HATPAN else None, {"out": "drums", **OHC}), ("ride", KIT, "6dB", None, {"out": "drums", **OHC}),
        ("lead", "m8-lead-guitar", {"value": "-3dB", "mod": [{"src": "auto.eye", "amount": 1}]}, 0, {"sends": {"hall": "-10dB"}, "auto": {"eye": {"points": LEAD_LANE}}}),
        ("leadw", "ct-lead-wah", "-3dB", 0, {"sends": {"hall": "-10dB"}, "auto": {"wah": {"points": [[f"{round(t / 4, 3)}b", v] for t, v in WAH_PTS]}}}),
        ("cl5", CLEAN, "-4dB", -0.45, {"sends": CL_SENDS}),
        ("cl7", CLEAN, "-3dB", 0.45, {"sends": CL_SENDS}),
        ("cl11", CLEAN, "-3dB", 0, {"sends": CL_SENDS}),
        ("home", "contrabass-tight", "-12dB", 0.3, {"sends": {"hall": "-12dB"}}),
        ("fifth", "cellos", "-15dB", 0.4, {"sends": {"hall": "-8dB"}}),
        ("air", "juno-pad", "-17dB", 0.15, {"sends": {"hall": "-8dB"}}),
        ("chime", "modal-glock", CHIME_GAIN, -0.2, {"sends": {"hall": "-6dB", "dly": "-14dB"}}),
        ("vox", "kidman", VOX or "0dB", 0, {"sends": {"hall": "-18dB"}, "fx": [{"type": "eq", "bands": ["hp cutoff=300"]}]}),
        ("choir", "voice-backing", CHOIR or "0dB", 0, {"sends": {"hall": "-8dB"}}),
        ("whisper", "ct-whisper", WHISPER or "0dB", 0, {"sends": {"hall": "-8dB"}}),
        ("swarm", "ct-swarm", {"value": SWARM or "0dB", "mod": [{"src": "auto.lvl", "amount": 1}]}, 0,
         {"sends": {"hall": "-8dB"}, "auto": {"sync": {"points": [[f"{b * 4}b", c] for b, c in SWARM_LANE]}, "lvl": {"points": [[f"{b * 4}b", c] for b, c in SWARM_LVL]}}}),
        ("cz", "cz-bass", CZ or "0dB", 0, {"fx": [{"type": "eq", "bands": ["hp cutoff=420"]}]}),     # its sweep, not its body: the wall rig is thick enough at 250-500 Hz
        ("rise", "ct-swell", "-9dB", 0, {"sends": {"hall": "-10dB"}}),
        ("drop", "ct-drop", "-8dB", 0, {}),
    ]
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
        t["notes"] = T[name]
        tracks.append(t)
    return {
        "about": "chirpers X (Common Time), track 1 by chirper-zero: one steady pulse in 4/4 and three wheels (cells five, seven and eleven sixteenths long) that turn under it for the whole piece and meet, all three on a bar line, only at bar 1 and at the landing 385 bars later. Generated by compose/chirpers10/src/chirpers10-t1.py.",
        "tempo": BPM, "ceiling": "-1dB", "loudness": -10, "seed": 1, "tail": "4s", "length": f"{NB * 4}b", "event_stable": True,
        "patches": {
            **({"ct-kit-here": {"extends": KIT, "kit": {x.split(":")[0]: {"pan": float(x.split(":")[1])} for x in KPANS.split(",")}}} if KPANS else {}),
            "ct-whisper": {"about": "chirper-zero: a whisper - the speaking voice with nearly all breath and no effort (what `chirp tts --mode whisper` builds)",
                           "extends": "voice-speech", "synth": {"layers": [{"type": "voice", "speech": 1, "breath": 0.95, "effort": 0.05, "ring": 0.2, "vary": 0.5, "vowel": 0.5, "onset": "expr.on", "coda": "expr.off"}]}},
            "ct-swell": {"about": "chirper-zero: a breath in before a landing - band-passed noise that swells for as long as the note is held (a slow attack), its band rising two octaves, cut off on the bar line",
                         "synth": {"layers": [{"type": "noise"}], "filters": [{"kind": "bp", "cutoff": {"value": 500, "mod": [{"src": "env.up", "amount": 2.5}]}, "q": 0.9}, "hp cutoff=250"],
                                   "env": {"up": {"a": "3.6s", "d": "10ms", "s": 1}}, "amp": {"a": "3.6s", "d": "10ms", "s": 1, "r": "40ms", "curve": 3}}},
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
            "ct-drop": {"about": "chirper-zero: the floor dropping on a landing - a sine that falls an octave to the note in 0.35 s and dies in 1.5 s",
                        "synth": {"layers": [{"wave": "sine"}], "pitch": {"value": 0, "mod": [{"src": "env.fall", "amount": 12}]},
                                  "env": {"fall": {"a": "1ms", "d": "350ms", "s": 0}}, "amp": {"a": "3ms", "d": "1.5s", "s": 0, "r": "200ms"}}}},
        "buses": {"hall": {"fx": ["reverb kind=hall decay=4.5s mix=1 predelay=30ms low_cut=150"]},
                  "dly": {"fx": ["delay time=3/16 feedback=0.35 mix=1 ping_pong=true", "reverb kind=hall decay=3s mix=0.3"]},
                  "drums": {"fx": ["reverb kind=room decay=0.7s mix=0.1 predelay=8ms",
                                   {"type": "glue", "threshold": "-24dB", "ratio": 2.5, "attack": "20ms", "release": "140ms", "knee": 6.0}]
                            + ([f"clip drive=0dB ceiling={DCLIP}dB"] if DCLIP else [])
                            + ([{"type": "eq", "bands": peaks(DEQ) + ([f"highshelf cutoff={DSHELF.split(':')[0]} gain={DSHELF.split(':')[1]}dB"] if DSHELF else [])}] if DEQ or DSHELF else [])
                            + ([{"type": "width", "width": 1, "mono_below": 0, "bands": [[float(x.split(":")[0]), float(x.split(":")[1])] for x in DWIDTH.split(",")]}] if DWIDTH else [])},
                  **({"oh": {"fx": [f"reverb kind=room decay={(DROOM.split(':') + ['0.4'])[3]}s mix=1 predelay=4ms low_cut={DROOM.split(':')[0]} high_cut=12000 spread=0.6"]}} if DROOM else {}),
                  **({"gtrs": {"fx": [{"type": "eq", "bands": peaks(GEQ)}, {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.ride", "amount": 1}]}}]
                               + ([{"type": "rotary", "mix": {"value": 0, "mod": [{"src": "auto.rot", "amount": 1}]}, "speed": {"value": 0, "mod": [{"src": "auto.spin", "amount": 1}]}}] if ROTARY else []),
                               "auto": {"ride": {"points": GTR_RIDE}, **({"rot": {"points": ROT_MIX}, "spin": {"points": ROT_SPIN}} if ROTARY else {})}}} if GEQ else {}),
                  **({"low": {"fx": [{"type": "eq", "bands": peaks(BEQ)}]
                              + ([{"type": "compressor", "threshold": BCOMP.split(":")[0] + "dB", "ratio": float(BCOMP.split(":")[1]), "attack": "12ms", "release": "120ms", "makeup": BCOMP.split(":")[2] + "dB"}] if BCOMP else [])
                              + [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.ride", "amount": 1}]}}],
                              "auto": {"ride": {"points": BASS_RIDE}}}} if BEQ else {})},
        "master": {"fx": [{"type": "eq", "bands": ["hp cutoff=24"]}] + ([{"type": "gain", "gain": f"{MASTER_DB}dB"}] if MASTER_DB else [])
                   + ([{"type": "gain", "gain": f"{MGAIN.split(':')[0]}dB"}, "limiter ceiling=-1dB", {"type": "gain", "gain": f"-{MGAIN.split(':')[1]}dB"}] if MGAIN else [])
                   + ([{"type": "tapestop", "stop": {"value": 0, "mod": [{"src": "auto.stop", "amount": 1}]}, "time": "1.25b"}] if TSTOP else []),
                   **({"auto": {"stop": {"points": TSTOP_LANE}}} if TSTOP else {})},
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
