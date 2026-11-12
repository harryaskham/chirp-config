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
EIGHT = [(0, 2, "c"), (2, 1, "c"), (3, 1, "c"), (4, 2, "h"), (6, 2, "c")]   # the coda: a cell that fits the bar

# the hook: the notes the wheels turn through, in semitones above the root (F: Ab Gb B C)
H1 = [3, 1, 6, 7]
H2 = [6, 5, 3, 1]
H3 = [1, 3, 1, 8]


def strikes(p, cell, s0, s1):
    """The strikes of global wheel `p` that fall in [s0, s1): (s16, length, kind, instance, hook index)."""
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


def gtr(trs, p, cell, b0, b1, root=F1, hook=H1, vel=0.85, ramp=None):
    s0, s1 = b0 * 16, b1 * 16
    for t, ln, kind, j, hi in strikes(p, cell, s0, s1):
        v = vel * (1.0 if j == 0 else 0.9)
        if ramp:
            v *= ramp[0] + (ramp[1] - ramp[0]) * (t - s0) / max(1, s1 - s0)
        for tr in trs:
            if kind == "c":
                add(tr, t, ln, root, v, pm=1)
            elif kind == "o":
                add(tr, t, ln, root, v)
            elif kind == "h":
                add(tr, t, ln, root + hook[hi % len(hook)], v * 1.05)
            elif kind == "x":
                add(tr, t, ln, root, v * 0.8, dead=1)
            elif kind == "p":
                add(tr, t, ln, ",".join(nm(root + i) for i in (0, 7, 12)), v)
            elif kind == "P":
                add(tr, t, ln, ",".join(nm(root + i) for i in (0, 7, 12, 19)), v)
            elif kind == "d":
                add(tr, t, ln, ",".join(nm(root + i) for i in (24, 37, 42)), v)


def bass(p, cell, b0, b1, root=F1, hook=H1, vel=0.85, ramp=None):
    s0, s1 = b0 * 16, b1 * 16
    for t, ln, kind, j, hi in strikes(p, cell, s0, s1):
        v = vel * (1.0 if j == 0 else 0.9)
        if ramp:
            v *= ramp[0] + (ramp[1] - ramp[0]) * (t - s0) / max(1, s1 - s0)
        if kind == "h":
            add("bass", t, ln, root + hook[hi % len(hook)], v)
        elif kind == "x":
            add("bass", t, ln * 0.5, root, v * 0.7)
        else:
            add("bass", t, ln if kind in ("o", "P") else ln * 0.9, root, v)


def kick(p, cell, b0, b1, vel=0.9, only_first=False, fill16=False):
    s0, s1 = b0 * 16, b1 * 16
    hit = set()
    for t, ln, kind, j, hi in strikes(p, cell, s0, s1):
        if only_first and j:
            continue
        if t not in hit:
            add("kick", t, 1, "k", vel * (1.0 if j == 0 else 0.86))
            hit.add(t)
    if fill16:   # double kick: the sixteenths between the wheel's strikes, softer
        for t in range(s0, s1):
            if t not in hit:
                add("kick", t, 1, "k", vel * 0.62)


def cym(piece, b0, b1, step=4, vel=0.62, skip_last=0):
    for t in range(b0 * 16, b1 * 16 - skip_last, step):
        add("cym", t, step, piece, vel * (1.12 if t % 16 == 0 else 1.0 if t % 8 == 0 else 0.9))


def snare(mode, b0, b1, vel=0.9, skip_last=0):
    offs = {"half": [8], "back": [4, 12], "none": []}[mode]
    for b in range(b0, b1):
        for o in offs:
            t = b * 16 + o
            if t < b1 * 16 - skip_last:
                add("snare", t, 2, "s", vel)


def crash(s16, vel=0.85, piece="c"):
    add("cym", s16, 8, piece, vel)


def fill(b1, n=8, vel=0.8):
    """A run into bar line b1 over its last n sixteenths: snare, then down the toms."""
    seq = ["s", "s", "t1", "t1", "t2", "t2", "ft", "ft"]
    for i in range(n):
        t = b1 * 16 - n + i
        piece = seq[(len(seq) - n + i) % len(seq)] if n <= len(seq) else seq[i * len(seq) // n]
        add("snare" if piece == "s" else "toms", t, 1, piece, vel * (0.7 + 0.3 * i / max(1, n - 1)))


def tick(tr, p, cell, pitches, b0, b1, vel=0.42, ramp=None):
    s0, s1 = b0 * 16, b1 * 16
    for t, ln, kind, j, hi in strikes(p, cell, s0, s1):
        v = vel + (0.18 if j == 0 else 0)
        if ramp:
            v *= ramp[0] + (ramp[1] - ramp[0]) * (t - s0) / max(1, s1 - s0)
        add(tr, t, 1.8, pitches[j % len(pitches)], v)


C5 = 72
LONG_WAIT = [(C5, 1), (C5 - 1, 1), (C5 - 4, 1), (C5 - 7, 2), (C5 - 6, 1), (C5 - 4, 1), (C5 - 1, 1), (C5, 2),
             (C5 + 1, 1), (C5, 1), (C5 - 4, 1), (C5 - 6, 2), (C5 - 7, 1), (C5 - 4, 1), (C5 - 6, 1), (C5 - 7, 3)]


def long_wait(b0, b1, vel=0.75, up=0):
    """The lead's tune: one note to each turn of the eleven wheel (some held for two or three turns)."""
    s0, s1 = b0 * 16, b1 * 16
    t = s0 + (-s0) % 11
    i = 0
    while t < s1:
        pitch, turns = LONG_WAIT[i % len(LONG_WAIT)]
        ln = min(turns * 11, s1 - t)
        add("lead", t, ln, pitch + up, vel)
        t += turns * 11
        i += 1


def solo(b0, b1, seed=9, vel=0.82):
    """A run on the seven wheel's strikes: a walk through the mode with leaps."""
    rng = random.Random(seed)
    scale = [0, 1, 3, 5, 6, 7, 8, 10]
    deg = 10
    for t, ln, kind, j, hi in strikes(7, [(0, 1, "c"), (1, 1, "c"), (2, 1, "c"), (3, 1, "c"), (4, 1, "c"), (5, 2, "h")], b0 * 16, b1 * 16):
        step = rng.choice([-2, -1, -1, 1, 1, 2, 3, -3]) if kind == "c" else rng.choice([4, -4, 5])
        deg = max(4, min(22, deg + step))
        add("lead", t, ln, 53 + 12 * (deg // 8) + scale[deg % 8], vel * (1.0 if kind == "h" else 0.88))


def drone(b0, b1, vel=0.6, fifth=True):
    for b in range(b0, b1, 4):
        ln = min(4, b1 - b) * 16 + 0.8
        add("home", b * 16, ln, "F1", vel)
        if fifth:
            for p in ("C2", "F2"):
                add("fifth", b * 16, ln, p, vel * 0.8)


def pad(b0, b1, vel=0.5):
    for b in range(b0, b1, 8):
        ln = min(8, b1 - b) * 16 + 0.8
        for p in ("F2", "C3", "G3", "C4"):
            add("air", b * 16, ln, p, vel)


def hit(s16, ln=32, vel=1.0):
    for tr in ("gl", "gr", "gl2", "gr2"):
        add(tr, s16, ln, "F1,C2,F2,C3", vel)
    add("bass", s16, ln, "F1", vel)
    add("kick", s16, 1, "k", 1.0)
    crash(s16, 1.0)
    crash(s16, 0.9, "x")


G = ("gl", "gr")
G2 = ("gl2", "gr2")
CL5 = ["F3", "C4", "F4"]
CL7 = ["C4", "G4", "F4", "Bb4"]
CL11 = ["F4", "C5", "Ab4", "Eb5", "Db5"]
TICK5 = [(0, 1, "c"), (2, 1, "c"), (3, 1, "c")]
TICK7 = [(0, 1, "c"), (2, 1, "c"), (4, 1, "c"), (5, 1, "c")]
TICK11 = [(0, 1, "c"), (3, 1, "c"), (5, 1, "c"), (8, 1, "c"), (9, 1, "c")]


def compose():
    B = BOUNDS
    # 1. 0-35  THE WAIT BEGINS: everything strikes once, together; then only the wheels, ticking, one by one
    hit(0)
    drone(0, 35)
    pad(4, 35)
    tick("cl5", 5, TICK5, CL5, 2, 35)
    tick("cl7", 7, TICK7, CL7, 12, 35)
    tick("cl11", 11, TICK11, CL11, 22, 35, vel=0.36)
    cym("rb", 16, 35, vel=0.3, skip_last=8)
    kick(4, [(0, 1, "c")], 27, 35, vel=0.6)                      # a heartbeat on the quarter
    gtr(G, 5, FIVE_A, 30, 35, vel=0.8, ramp=(0.45, 0.9))           # the machine, approaching
    bass(5, FIVE_A, 30, 35, vel=0.8, ramp=(0.45, 0.9))
    fill(35, 8)

    # 2. 35-55  five and seven have met: RIFF A, the five wheel in full
    a, z = B[1], B[2]
    crash(a * 16)
    gtr(G, 5, FIVE_A, a, z, hook=H1)
    bass(5, FIVE_A, a, z, hook=H1)
    kick(5, FIVE_A, a, z)
    cym("x", a, z, skip_last=8)
    snare("half", a, z, skip_last=8)
    for t in landings(5, a * 16 + 1, z * 16):
        crash(t, 0.8)
    fill(z, 8)

    # 3. 55-70  five meets eleven: the five wheel thickens, and eleven arrives as open chords left to ring
    a, z = B[2], B[3]
    crash(a * 16)
    gtr(G, 5, FIVE_B, a, z, hook=H1)
    gtr(G2, 11, ELEVEN_W, a, z, vel=0.9)
    bass(5, FIVE_A, a, z, hook=H1)
    kick(5, FIVE_B, a, z)
    cym("x", a, z, skip_last=4)
    snare("half", a, z, skip_last=4)
    for t in landings(11, a * 16 + 1, z * 16):
        crash(t, 0.85)
    fill(z, 4)

    # 4. 70-77  five and seven meet: seven bars of the seven wheel, nearly alone (one guitar, bass, kick)
    a, z = B[3], B[4]
    crash(a * 16, 0.7, "sp")
    gtr(("gl",), 7, SEVEN_A, a, z, hook=H2, vel=0.8)
    gtr(("gr",), 7, SEVEN_A, a + 4, z, hook=H2, vel=0.8)
    bass(7, SEVEN_A, a, z, hook=H2)
    kick(7, SEVEN_A, a, z)
    cym("h", a, z, vel=0.55, skip_last=8)
    snare("half", a, z, skip_last=8)
    fill(z, 8)

    # 5. 77-105  seven meets eleven: RIFF B, guitars on seven, the bass on eleven; the lead's tune arrives halfway
    a, z = B[4], B[5]
    crash(a * 16)
    gtr(G, 7, SEVEN_B, a, z, hook=H2)
    bass(11, ELEVEN_A, a, z, hook=H1)
    kick(7, SEVEN_B, a, z)
    cym("rb", a, a + 14, vel=0.6)
    cym("x", a + 14, z, skip_last=8)
    crash((a + 14) * 16)
    snare("half", a, z, skip_last=8)
    long_wait(a + 14, z)
    for t in landings(7, a * 16 + 1, z * 16):
        crash(t, 0.8)
    fill(z, 8)

    # 6. 105-110  five and seven meet: stop-time. Sixteen stabs on the five wheel, silence between
    a, z = B[5], B[6]
    gtr(G + G2, 5, FIVE_S, a, z, vel=0.95)
    bass(5, FIVE_S, a, z, vel=0.95)
    kick(5, FIVE_S, a, z, vel=0.95)
    for t, ln, kind, j, hi in strikes(5, FIVE_S, a * 16, z * 16):
        add("cym", t, 2, "cch", 0.75)

    # 7. 110-140  five meets eleven: RIFF C, the splayed one. Eleven on guitars and bass, slow and wide; five under it in the kick
    a, z = B[6], B[7]
    crash(a * 16)
    for (x, y, root, hook) in ((a, a + 11, F1, H1), (a + 11, a + 22, F1 + 5, H3), (a + 22, z, F1, H1)):
        gtr(G, 11, ELEVEN_A, x, y, root=root, hook=hook)
        gtr(G2, 11, ELEVEN_W, x, y, root=root, vel=0.9)
        bass(11, ELEVEN_A, x, y, root=root, hook=hook)
        crash(x * 16, 0.9)
    kick(5, FIVE_A, a, z)
    cym("x", a, z, step=8, vel=0.7, skip_last=8)
    snare("half", a, z, skip_last=8)
    fill(z, 8)

    # 8. 140-154  five meets seven: both at once. Five in the left guitar, seven in the right; double time
    a, z = B[7], B[8]
    crash(a * 16)
    gtr(("gl",), 5, FIVE_B, a, z, hook=H1)
    gtr(("gr",), 7, SEVEN_B, a, z, hook=H2)
    bass(7, SEVEN_A, a, z, hook=H2)
    kick(5, FIVE_B, a, z)
    cym("h", a, z, step=2, vel=0.5, skip_last=4)
    snare("back", a, z, skip_last=4)
    fill(z, 4)

    # 9. 154-165  seven meets eleven: the lead runs on the seven wheel while the bass turns eleven
    a, z = B[8], B[9]
    crash(a * 16)
    gtr(G, 7, SEVEN_A, a, z, hook=H2)
    bass(11, ELEVEN_A, a, z, hook=H1)
    kick(7, SEVEN_A, a, z)
    cym("rd", a, z, vel=0.6, skip_last=8)
    snare("half", a, z, skip_last=8)
    solo(a, z)
    fill(z, 8)

    # 10. 165-175  five meets eleven: the weight comes off
    a, z = B[9], B[10]
    crash(a * 16)
    gtr(G, 5, FIVE_A, a, z, hook=H1, vel=0.75, ramp=(1.0, 0.4))
    bass(11, ELEVEN_W, a, z, vel=0.8)
    kick(5, FIVE_A, a, a + 5, only_first=True, vel=0.8)
    cym("h", a, z, vel=0.5)
    snare("half", a, a + 5)
    tick("cl5", 5, TICK5, CL5, a + 5, z, ramp=(0.5, 1.0))
    drone(a + 4, z, vel=0.5, fifth=False)

    # 11. 175-210  five and seven meet: THE EYE. The wheels tick as they did at the start; the tune, slowly
    a, z = B[10], B[11]
    drone(a, z)
    pad(a, z)
    tick("cl5", 5, TICK5, CL5, a, z)
    tick("cl7", 7, TICK7, CL7, a, z)
    tick("cl11", 11, TICK11, CL11, a + 12, z, vel=0.36)
    cym("rb", a + 8, z, vel=0.3, skip_last=8)
    long_wait(a + 8, a + 30, vel=0.7, up=-12)
    for t, ln, kind, j, hi in strikes(5, FIVE_A, (z - 10) * 16, z * 16 - 8):
        add("toms", t, 1, ["ft", "t2", "t1"][j], 0.45 + 0.35 * (t - (z - 10) * 16) / 160)
    kick(4, [(0, 1, "c")], z - 6, z, vel=0.6)
    fill(z, 8)

    # 12. 210-220  five and seven meet: the weight comes back. Muted five on the guitars, seven under it
    a, z = B[11], B[12]
    crash(a * 16, 0.7)
    gtr(G, 5, FIVE_B, a, z, hook=H1, vel=0.85, ramp=(0.6, 1.0))
    bass(7, SEVEN_A, a, z, hook=H2)
    kick(7, SEVEN_A, a, z)
    for t, ln, kind, j, hi in strikes(5, FIVE_A, a * 16, (a + 5) * 16):
        add("toms", t, 1, ["ft", "t2", "t1"][j], 0.7)
    cym("x", a + 5, z, skip_last=8)
    snare("half", a + 4, z, skip_last=8)
    fill(z, 8)

    # 13. 220-231  five meets eleven: the splayed riff again, filled in
    a, z = B[12], B[13]
    crash(a * 16)
    gtr(G, 11, ELEVEN_B, a, z, hook=H1)
    gtr(G2, 11, ELEVEN_W, a, z, vel=0.9)
    bass(11, ELEVEN_A, a, z, hook=H1)
    kick(11, ELEVEN_B, a, z)
    cym("x", a, z, skip_last=8)
    snare("half", a, z, skip_last=8)
    fill(z, 8)

    # 14. 231-245  seven meets eleven: seven on the guitars over eleven's chords; double time
    a, z = B[13], B[14]
    crash(a * 16)
    gtr(G, 7, SEVEN_B, a, z, hook=H3)
    gtr(G2, 11, ELEVEN_W, a, z, vel=0.9)
    bass(7, SEVEN_B, a, z, hook=H3)
    kick(7, SEVEN_B, a, z)
    cym("x", a, z, step=2, vel=0.55, skip_last=4)
    snare("back", a, z, skip_last=4)
    fill(z, 4)

    # 15. 245-275  five meets seven: all three. Five left, seven right, eleven in the bass, and the tune over them
    a, z = B[14], B[15]
    crash(a * 16)
    gtr(("gl",), 5, FIVE_B, a, z, hook=H1)
    gtr(("gr",), 7, SEVEN_B, a, z, hook=H2)
    bass(11, ELEVEN_A, a, z, hook=H1)
    kick(5, FIVE_B, a, z)
    cym("rde", a, z, vel=0.6, skip_last=8)
    snare("half", a, z, skip_last=8)
    long_wait(a, z, vel=0.8)
    for t in landings(5, a * 16 + 1, z * 16):
        crash(t, 0.8)
    fill(z, 8)

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

    # 17. 280-308  five meets seven: the hardest stretch. Seven everywhere, the kick running sixteenths; up a semitone, and back
    a, z = B[16], B[17]
    for (x, y, root) in ((a, a + 14, F1), (a + 14, a + 21, F1 + 1), (a + 21, z, F1)):
        crash(x * 16, 0.9)
        gtr(G + G2, 7, SEVEN_B, x, y, root=root, hook=H2, vel=0.92)
        bass(7, SEVEN_B, x, y, root=root, hook=H2, vel=0.92)
    kick(7, SEVEN_B, a, z, fill16=True)
    cym("x", a, z, step=2, vel=0.58, skip_last=8)
    snare("back", a, z, skip_last=8)
    fill(z, 8)

    # 18. 308-315  seven meets eleven: seven bars for the bass, on eleven, under one held chord
    a, z = B[17], B[18]
    crash(a * 16)
    for tr in G2:
        add(tr, a * 16, 7 * 16 - 8, "F1,C2,F2,C3", 0.9)
    bass(11, ELEVEN_B, a, z, hook=H1, vel=0.95)
    kick(11, ELEVEN_A, a, z)
    cym("h", a, z, vel=0.55, skip_last=8)
    snare("half", a, z, skip_last=8)
    fill(z, 8)

    # 19. 315-330  five meets seven: the two guitars swap wheels
    a, z = B[18], B[19]
    crash(a * 16)
    gtr(("gl",), 7, SEVEN_A, a, z, hook=H2)
    gtr(("gr",), 5, FIVE_A, a, z, hook=H1)
    bass(5, FIVE_A, a, z, hook=H1)
    kick(5, FIVE_A, a, z)
    kick(7, SEVEN_A, a, z, only_first=True)
    cym("x", a, z, skip_last=4)
    snare("half", a, z, skip_last=4)
    fill(z, 4)

    # 20. 330-350  five meets eleven: RIFF A comes home, with eleven's chords and the tune
    a, z = B[19], B[20]
    crash(a * 16)
    gtr(G, 5, FIVE_A, a, z, hook=H1, vel=0.92)
    gtr(G2, 11, ELEVEN_W, a, z, vel=0.92)
    bass(5, FIVE_A, a, z, hook=H1, vel=0.92)
    kick(5, FIVE_B, a, z)
    cym("x", a, z, skip_last=8)
    snare("half", a, z, skip_last=8)
    long_wait(a, z, vel=0.8)
    for t in landings(5, a * 16 + 1, z * 16):
        crash(t, 0.8)
    fill(z, 8)

    # 21. 350-385  five and seven meet for the last time before the landing: THE APPROACH, all three wheels
    a, z = B[20], B[21]
    crash(a * 16)
    gtr(("gl",), 5, FIVE_B, a, z, hook=H1, vel=0.92, ramp=(0.9, 1.05))
    gtr(("gr",), 7, SEVEN_B, a, z, hook=H2, vel=0.92, ramp=(0.9, 1.05))
    gtr(G2, 11, ELEVEN_W, a, z, vel=0.92)
    bass(11, ELEVEN_A, a, z, hook=H1, vel=0.92)
    kick(5, FIVE_B, a, z - 14)
    kick(5, FIVE_B, z - 14, z, fill16=True)
    cym("x", a, z - 14, skip_last=0)
    cym("x", z - 14, z, step=2, vel=0.6, skip_last=16)
    snare("half", a, z - 14)
    snare("back", z - 14, z, skip_last=16)
    long_wait(a + 7, z - 1, vel=0.85)
    for t in landings(7, a * 16 + 1, z * 16):
        crash(t, 0.85)
    fill(z, 16, vel=0.9)

    # THE LANDING, 385-409: all three wheels and the bar line, together for the first time since bar 1.
    # Then common time, plainly: a cell eight sixteenths long, everyone on it
    a = 385
    hit(a * 16, ln=14)
    gtr(G + G2, 8, EIGHT, a + 1, a + 16, hook=H1, vel=0.95)
    bass(8, EIGHT, a + 1, a + 16, hook=H1, vel=0.95)
    kick(8, EIGHT, a + 1, a + 16)
    cym("x", a + 1, a + 16)
    snare("back", a + 1, a + 16)
    for b in range(a + 1, a + 16, 2):
        crash(b * 16, 0.85)
    hit((a + 16) * 16, ln=8 * 16)
    drone(a + 16, NB)
    pad(a + 16, NB)
    tick("cl5", 5, TICK5, CL5, a + 17, NB - 1, ramp=(1.0, 0.4))
    tick("cl7", 7, TICK7, CL7, a + 17, NB - 1, ramp=(1.0, 0.4))


def song():
    compose()
    for v in T.values():
        v.sort(key=lambda x: x["at"])
    spec = [
        ("gl", RIG_L, "0dB", -1, {}), ("gr", RIG_R, "0dB", 1, {}),
        ("gl2", RIG_L, "-3dB", -0.8, {}), ("gr2", RIG_R, "-3dB", 0.8, {}),
        ("bass", BASS, "0.5dB", 0, {}),
        ("kick", KIT, "2dB", None, {"out": "drums"}), ("snare", KIT, "8dB", None, {"out": "drums"}),
        ("cym", KIT, "-3dB", None, {"out": "drums"}), ("toms", KIT, "4dB", None, {"out": "drums"}),
        ("lead", "m8-lead-guitar", {"value": "-3dB", "mod": [{"src": "auto.eye", "amount": 1}]}, 0, {"sends": {"hall": "-10dB"}, "auto": {"eye": {"points": [["0b", 0], [f"{174 * 4}b", 0], [f"{175 * 4}b", -10], [f"{210 * 4}b", -10], [f"{211 * 4}b", 0]]}}}),
        ("cl5", "m8-clean", "-4dB", -0.45, {"sends": {"dly": "-14dB", "hall": "-12dB"}}),
        ("cl7", "m8-clean", "-3dB", 0.45, {"sends": {"dly": "-14dB", "hall": "-12dB"}}),
        ("cl11", "m8-clean", "-3dB", 0, {"sends": {"dly": "-12dB", "hall": "-10dB"}}),
        ("home", "contrabass-tight", "-12dB", 0.3, {"sends": {"hall": "-12dB"}}),
        ("fifth", "cellos", "-15dB", 0.4, {"sends": {"hall": "-8dB"}}),
        ("air", "juno-pad", "-17dB", 0.15, {"sends": {"hall": "-8dB"}}),
    ]
    tracks = []
    for name, patch, gain, pan, extra in spec:
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
        "buses": {"hall": {"fx": ["reverb kind=hall decay=4.5s mix=1 predelay=30ms low_cut=150"]},
                  "dly": {"fx": ["delay time=3/16 feedback=0.35 mix=1 ping_pong=true", "reverb kind=hall decay=3s mix=0.3"]},
                  "drums": {"fx": ["reverb kind=room decay=0.7s mix=0.1 predelay=8ms",
                                   {"type": "glue", "threshold": "-24dB", "ratio": 2.5, "attack": "20ms", "release": "140ms", "knee": 6.0}]
                            + ([f"clip drive=0dB ceiling={DCLIP}dB"] if DCLIP else [])}},
        "master": {"fx": [{"type": "eq", "bands": ["hp cutoff=24"]}]
                   + ([{"type": "gain", "gain": f"{MGAIN.split(':')[0]}dB"}, "limiter ceiling=-1dB", {"type": "gain", "gain": f"-{MGAIN.split(':')[1]}dB"}] if MGAIN else [])},
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
