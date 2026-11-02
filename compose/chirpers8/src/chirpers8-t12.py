#!/usr/bin/env python3
"""chirpers - A Light Left On (chirpers VIII), track 12, THE CLOSER (chirper-three).

Everything the engine does at once, and still a song: an orchestra of illusions that GROWS LIKE A PLANT.

THE SYSTEM: an L-system (A -> AB, B -> A: the Fibonacci word), one generation per section, with one mutation rule per
generation (every k-th A becomes C). Each section plays its generation's string: it is the melody (A a step up the
scale, B two steps down, C a leap), the rhythm (A an eighth, B a dotted eighth, C a sixteenth: a quasi-periodic rhythm,
a loop that never quite repeats) and the walk of the harmony. The section lengths are Fibonacci numbers, so the form
itself grows: the piece begins as one note (the light) and ends as one note again.

TUNING: 31-EDO (31 equal steps to the octave, 38.7 cents each), written as fractional MIDI (m66.387). The scale is a
'neutral Dorian' on F#: F#, G#, a NEUTRAL third (between A and A#), B, C#, D#, E. Chords mix 6/5 minor thirds, 5/4
major thirds, neutral thirds and the 7/4 harmonic seventh - subtly off, by construction.

FORM (186 bars, ~6:10, 112 -> 126 bpm on a tempo map):
  seed   1-8     a music box plays one F#, over a fan's hum: the light
  g1     9-13    'AB' on a celesta
  g2     14-21   'ABA'; bowed cellos breathe the chord
  g3     22-34   'ABAAB'; the pulse arrives (kick, hats with drift, a phantom bass nobody plays)
  g4     35-55   8 symbols on a harp with sympathetic strings; horns (lips) answer on B; claps
  g5     56-89   13 symbols: everything - a Shepard choir rising forever, violins, warped hats, the real sub
  prune  90-102  cut back: the strings through a barber pole, a Shepard fall, the lead alone
  g6     103-157 21 symbols: the whole grown piece
  coda   158-178 a Risset rush on the hats that keeps accelerating and never gets faster; the lead thins
  light  179-186 one note again
"""
import json
import math
import os
import random

OUT = os.environ.get("C8T12_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers8-t12.yaml")
BAR = 4.0
SECTIONS = [("seed", 1, 8), ("g1", 9, 13), ("g2", 14, 21), ("g3", 22, 34), ("g4", 35, 55), ("g5", 56, 89),
            ("prune", 90, 102), ("g6", 103, 157), ("coda", 158, 178), ("light", 179, 190)]   # v9: four more bars of light
GEN = {"seed": 0, "g1": 1, "g2": 2, "g3": 3, "g4": 4, "g5": 5, "prune": 3, "g6": 6, "coda": 4, "light": 0}
BARS = SECTIONS[-1][2]
CUT = range(90, 103)        # v8: THE PRUNE IS PRUNED - its bars lose an eighth (7/8); generate in 4/4, warp at output


def rb(bar):
    """v8: the REAL beat at which a bar starts (bars 90-102 last 3.5 beats)."""
    return (bar - 1) * BAR - 0.5 * max(0, min(bar, CUT.stop) - CUT.start)


def warp(v):
    """v8: virtual 4/4 beats -> real beats; anything in a pruned bar's cut eighth is dropped (None)."""
    bar = int(v // BAR + 1e-9) + 1
    off = v - (bar - 1) * BAR
    if bar in CUT and off >= BAR - 0.5 - 1e-6:
        return None
    return rb(bar) + off


TOTAL = rb(BARS + 1)
EDO = 31
FS4 = 66                                  # F#4
SCALE = [0, 5, 9, 13, 18, 23, 26]         # neutral Dorian on F#, in 31-EDO steps


def b0(bar):
    return (bar - 1) * BAR


def sec_of(bar):
    for name, a, z in SECTIONS:
        if a <= bar <= z:
            return name
    return "light"


def m(steps, base=FS4):
    """A 31-EDO pitch as fractional MIDI: base + steps * 12/31 semitones."""
    return f"m{base + steps * 12 / EDO:.3f}"


def chord(base, steps_list):
    return ",".join(m(s, base) for s in steps_list)


class Part:
    def __init__(self):
        self.ev = []

    def add(self, at, ln, head, vel):
        self.ev.append((at, ln, head, int(max(1, min(127, vel)))))

    def score(self, total=TOTAL):
        ev = sorted(((warp(s), ln, h, v) for s, ln, h, v in self.ev if warp(s) is not None), key=lambda e: (e[0], -e[3]))
        toks, pos = [], 0.0
        for i, (s, ln, head, vel) in enumerate(ev):
            nxt = ev[i + 1][0] if i + 1 < len(ev) else total
            ln = min(ln, nxt - s)
            if ln <= 1e-6:
                continue
            if s - pos > 1e-5:
                toks.append(f"R/{s - pos:.5g}b")
            base, _, mods = head.partition("^")
            toks.append(f"{base}/{ln:.5g}b@{vel}" + (f"^{mods}" if mods else ""))
            pos = s + ln
        if total - pos > 1e-5:
            toks.append(f"R/{total - pos:.5g}b")
        return " ".join(toks) if toks else f"R/{total:g}b"


P = {}


def part(n):
    return P.setdefault(n, Part())


# ---------------------------------------------------------------- the L-system
def lsys(n):
    s = "A"
    for g in range(n):
        s = "".join({"A": "AB", "B": "A", "C": "AB"}[c] for c in s)
        k = g + 3                                    # THE MUTATION: every k-th A of this generation becomes C
        out, na = [], 0
        for c in s:
            if c == "A":
                na += 1
                out.append("C" if na % k == 0 else "A")
            else:
                out.append(c)
        s = "".join(out)
    return s


STEP = {"A": 1, "B": -2, "C": 3}                  # scale degrees moved by each symbol
DUR = {"A": 0.5, "B": 0.75, "C": 0.25}            # beats: a quasi-periodic Fibonacci rhythm


def degree_pitch(d, base=FS4):
    o, k = divmod(d, 7)
    return base + 12 * o + SCALE[k] * 12 / EDO


def melody(sec, a, z, trk, base=FS4, vel=84, every=1, octave=0, legato=False, mods=""):
    """Play the section's generation string from bar a to z, again and again, on trk."""
    s = lsys(GEN[sec])
    t, end, d, i = b0(a), b0(z + 1), 0, 0
    while t < end - 1e-6:
        c = s[i % len(s)]
        if i % len(s) == 0:
            d = 0                                   # each pass starts on the light's note
        if i % every == 0:
            p = degree_pitch(d, base) + 12 * octave
            part(trk).add(t, DUR[c] * (1.0 if legato else 0.9), f"m{p:.3f}" + mods,
                          vel + (10 if c == "C" else 0) - (8 if c == "B" else 0))
        d += STEP[c]
        if d > 9 or d < -4:                         # fold back into range
            d -= 7 * (1 if d > 9 else -1)
        t += DUR[c]
        i += 1


# ---------------------------------------------------------------- harmony
MIN7, SEPT, NEUT, MAJ = (0, 8, 18, 26), (0, 10, 18, 25), (0, 9, 18, 26), (0, 10, 18, 28)
ROOTS = [0, -10, 13, 8, 18, -5]                 # F#, D, B, A, C#, E (31-EDO steps from F#)


def harmony_plan():
    """Chords by bar, walked by the L-system: each symbol of the section's string is a chord (A two bars, B one, C one),
    its root chosen by how many A's and B's have passed, its quality by the symbol."""
    plan = {}
    na = nb = 0
    for sec, a, z in SECTIONS:
        if sec in ("seed", "light"):
            for bar in range(a, z + 1):
                plan[bar] = (0, MIN7)
            continue
        s = lsys(max(GEN[sec] - 1, 1))
        bar, i = a, 0
        while bar <= z:
            c = s[i % len(s)]
            root = ROOTS[(2 * na + nb) % len(ROOTS)]
            q = {"A": MIN7, "B": SEPT, "C": NEUT}[c]
            for k in range(2 if c == "A" else 1):
                if bar + k <= z:
                    plan[bar + k] = (root, q)
            bar += 2 if c == "A" else 1
            na += c == "A"
            nb += c != "A"
            i += 1
    return plan


PLAN = harmony_plan()


def write_harmony():
    for bar in range(1, BARS + 1):
        sec = sec_of(bar)
        root, q = PLAN[bar]
        if sec in ("g2", "g3", "g4", "g5", "prune", "g6", "coda"):
            part("cellos").add(b0(bar), BAR - 0.05, chord(54 + root * 12 / EDO, q[:3]), 70 if sec != "g2" else 58)
        if sec in ("g5", "g6"):
            part("violins").add(b0(bar), BAR - 0.05, chord(66 + root * 12 / EDO, q[1:]), 62)
        if sec == "prune":
            part("pole").add(b0(bar), BAR - 0.05, chord(66 + root * 12 / EDO, q[1:]), 66)
        # THE BASS NOBODY PLAYS: the root, on the off-beat eighths, through the phantom
        if sec in ("g3", "g4", "g5", "g6", "coda"):
            for e in range(8):
                if e % 2 == 1 or e == 0:
                    part("phantom").add(b0(bar) + e * 0.5, 0.4, f"m{30 + root * 12 / EDO:.3f}", 100 if e == 0 else 84)
        if sec in ("g5", "g6"):
            part("sub").add(b0(bar), 1.8, f"m{30 + root * 12 / EDO:.3f}", 96)
            part("sub").add(b0(bar) + 2, 1.8, f"m{30 + root * 12 / EDO:.3f}", 88)
        # THE HORNS (lips) answer each bar whose chord is a B (the harmonic seventh) in g4-g6
        if sec in ("g4", "g5", "g6") and q == SEPT:
            part("horns").add(b0(bar) + 2.5, 1.2, chord(54 + root * 12 / EDO, q), 86)
        # v11: THE BRASS CHORALE at the summit - g6's last eight bars, sustained lips-and-bore chords on the grown
        # harmony, swelling bar by bar into the coda
        if 150 <= bar <= 157:
            part("horns").add(b0(bar), 3.9, chord(54 + root * 12 / EDO, q), 66 + (bar - 150) * 5)


# ---------------------------------------------------------------- the lead, by generation
def write_melody():
    melody("seed", 1, 8, "light", base=78, vel=70, every=99)        # one note, again and again (every 99: only the first)
    for bar in range(1, 9, 2):
        part("light").add(b0(bar), 1.5, f"m{78:.3f}", 72)
    melody("g1", 9, 13, "celesta", base=78, vel=78)
    melody("g2", 14, 21, "celesta", base=78, vel=78)
    melody("g3", 22, 34, "kalimba", base=66, vel=88)
    melody("g4", 35, 55, "harp", base=66, vel=90)
    melody("g5", 56, 89, "harp", base=66, vel=92)
    melody("g5", 56, 89, "celesta", base=78, vel=70, every=3)
    melody("prune", 90, 102, "kalimba", base=66, vel=84)
    melody("g6", 103, 157, "harp", base=66, vel=94)
    melody("g6", 103, 157, "violins_lead", base=78, vel=72, every=2, mods="^f0=-39>0>0")   # v7: each note scooped
    # v7: THE HARP STRUMS each new chord of the grown sections - a spread 31-EDO chord at every change
    prev = None
    for bar in range(35, 158):
        if sec_of(bar) in ("g4", "g5", "g6") and PLAN[bar] != prev:
            root, q = PLAN[bar]
            part("strum").add(b0(bar), 3.5, chord(54 + root * 12 / EDO, q) + "," + m(q[1] + 31, 54 + root * 12 / EDO), 86)
        prev = PLAN[bar]
    melody("g6", 103, 157, "celesta", base=78, vel=68, every=5)
    melody("coda", 158, 178, "celesta", base=78, vel=74, every=2)
    # v3: THE ONDES MARTENOT (one of the first electronic instruments) doubles the grown melody an octave up, legato,
    # GLIDING between 31-EDO steps on its ribbon - the quarter-tones and neutral thirds heard as slides
    melody("g5", 73, 89, "ondes", base=78, vel=80, legato=True)
    melody("g6", 103, 157, "ondes", base=78, vel=84, legato=True)
    melody("coda", 158, 174, "ondes", base=78, vel=76, legato=True)
    for bar in range(179, 187, 2):
        part("light").add(b0(bar), 1.5 if bar < 185 else 7.5, f"m{78:.3f}", 70 - (bar - 179) * 2)
    # v9: A LIGHT LEFT ON - the standby light: one soft sine on the music box's F#5, BREATHING (a slow tremolo, about
    # twelve breaths a minute) from the last section to the very end, on alone for the final bars with the fan's hum
    part("standby").add(b0(179), b0(191) - b0(179) - 0.05, "m78.000", 74)
    memory()                                                  # v10: the album, remembered
    tower()                                                   # v12: the generations counted
    # the fan's hum under the light (seed and the last bars): a soft sine on F#2
    for a, z in ((1, 8), (179, 190)):
        part("hum").add(b0(a), b0(z + 1) - b0(a) - 0.1, f"m{42:.3f}", 60)


# ---------------------------------------------------------------- drums
def drums():
    hand = random.Random(12)
    for bar in range(22, 179):
        sec = sec_of(bar)
        if sec == "prune":
            # v8: the prune COUNTS - a rimshot on every eighth, seven to a bar (2+2+3), so the missing eighth is heard
            for e in range(7):
                part("hats").add(b0(bar) + e * 0.5, 0.1, "rs", 92 if e == 0 else (74 if e in (2, 4) else 52 + hand.randint(-5, 5)))
            continue
        for b in range(4):
            part("kick").add(b0(bar) + b, 0.5, "k", 112 if b == 0 else 104)
            part("hats").add(b0(bar) + b + 0.5, 0.25, "oh", 64 + hand.randint(-6, 6))
            for s in (1, 3):
                if hand.random() < 0.65:
                    part("hats").add(b0(bar) + b + s / 4 + 0.03, 0.1, "h", 46 + hand.randint(-8, 8))
        if sec in ("g4", "g5", "g6"):                         # v2: a ride on the eighths, for the top end
            for e in range(8):
                part("ride").add(b0(bar) + e * 0.5, 0.4, "rd", 70 if e % 2 == 0 else 54)
        if sec not in ("g3",):
            for b in (1, 3):
                part("clap").add(b0(bar) + b + 0.02, 0.5, "cp", 88 + hand.randint(-4, 4))


RUSH = ("h/0.25b@62 h/0.25b@42 oh/0.5b@58 rs/0.25b@68 h/0.25b@44 h/0.5b@54 h/0.25b@60 h/0.25b@40 "
        "oh/0.5b@56 rs/0.25b@64 h/0.25b@42 h/0.5b@50")


def illusions():
    """A Shepard choir rising for ever through g5; a Shepard fall through the prune."""
    for bar in range(56, 90):
        part("shepup").add(b0(bar), BAR - 0.05, chord(66, (0, 18)), 60)
    for bar in range(90, 103):
        part("shepdown").add(b0(bar), BAR - 0.05, chord(66, (0, 18)), 60)


LEAVES = [   # v6: re-printed (46a24ab5 prints MIDI notes, so the song's 31-EDO tuning snaps the line): chirp tts "count the leaves again" --humanize 0.6 --repeat 6 --melodize 1: (at, len, ph, pitch, vel, f0)
    (0.278, 0.967, 'K AW1 N T', 'm58.521', 0.855, [0.0, 6.0, 11.0, 16.0, 21.0, 25.0, 28.0, 30.0, 34.0, 37.0, 38.0, 33.0, 26.0, 19.0, 15.0, 15.0, 15.0, 11.0, 2.0, -11.0, -23.0]),
    (1.247, 0.373, 'DH AH0', 'm55.091', 0.8, [0.0, -3.0, -7.0, -10.0, -14.0, -17.0, -21.0, -24.0]),
    (1.609, 0.967, 'L IY1 V Z', 'm57.08', 0.751, [0.0, 6.0, 11.0, 16.0, 21.0, 25.0, 28.0, 30.0, 34.0, 37.0, 38.0, 33.0, 26.0, 19.0, 15.0, 15.0, 15.0, 11.0, 2.0, -11.0, -23.0]),
    (2.575, 0.262, 'AH0', 'm53.53', 0.85, [0.0, -6.0, -12.0, -18.0, -24.0]),
    (2.818, 1.14, 'G EH1 N', 'm53.537', 0.868, [0.0, 3.0, 5.0, 7.0, 9.0, 11.0, 12.0, 12.0, 13.0, 14.0, 13.0, 8.0, 0.0, -6.0, -9.0, -8.0, -10.0, -16.0, -27.0, -41.0, -53.0, -60.0, -64.0, -67.0]),
    (8.249, 0.961, 'K AW1 N T', 'm59.954', 0.805, [0.0, 5.0, 9.0, 14.0, 18.0, 21.0, 22.0, 25.0, 30.0, 34.0, 32.0, 23.0, 13.0, 8.0, 10.0, 14.0, 14.0, 7.0, -7.0, -22.0]),
    (9.217, 0.368, 'DH AH0', 'm57.873', 0.802, [0.0, -3.0, -5.0, -8.0, -11.0, -14.0, -16.0, -19.0]),
    (9.577, 0.958, 'L IY1 V Z', 'm59.703', 0.76, [0.0, 5.0, 9.0, 14.0, 18.0, 21.0, 22.0, 25.0, 30.0, 34.0, 32.0, 23.0, 13.0, 8.0, 9.0, 13.0, 14.0, 7.0, -6.0, -21.0]),
    (10.53, 0.266, 'AH0', 'm57.412', 0.755, [0.0, -5.0, -10.0, -14.0, -19.0]),
    (10.819, 1.209, 'G EH1 N', 'm55.866', 0.874, [0.0, 2.0, 4.0, 5.0, 7.0, 8.0, 9.0, 9.0, 11.0, 13.0, 13.0, 9.0, 2.0, -5.0, -7.0, -4.0, 0.0, -0.0, -8.0, -21.0, -35.0, -43.0, -45.0, -42.0, -42.0, -47.0]),
    (16.255, 0.96, 'K AW1 N T', 'm61.379', 0.879, [0.0, 4.0, 7.0, 10.0, 13.0, 15.0, 15.0, 18.0, 24.0, 29.0, 27.0, 17.0, 4.0, -0.0, 4.0, 13.0, 17.0, 10.0, -4.0, -21.0]),
    (17.235, 0.347, 'DH AH0', 'm60.262', 0.862, [0.0, -2.0, -5.0, -7.0, -10.0, -12.0, -14.0]),
    (17.552, 0.963, 'L IY1 V Z', 'm62.416', 0.762, [0.0, 3.0, 7.0, 10.0, 13.0, 15.0, 15.0, 17.0, 22.0, 27.0, 29.0, 23.0, 11.0, 2.0, 1.0, 7.0, 15.0, 16.0, 9.0, -6.0, -21.0]),
    (18.539, 0.255, 'AH0', 'm61.183', 0.83, [0.0, -4.0, -7.0, -11.0, -14.0]),
    (18.79, 1.277, 'G EH1 N', 'm58.19', 0.885, [0.0, 1.0, 3.0, 4.0, 5.0, 6.0, 7.0, 7.0, 8.0, 11.0, 12.0, 7.0, -0.0, -7.0, -7.0, 0.0, 8.0, 8.0, -2.0, -17.0, -29.0, -34.0, -29.0, -22.0, -20.0, -27.0, -42.0]),
    (24.253, 0.958, 'K AW1 N T', 'm62.931', 0.77, [0.0, 2.0, 5.0, 7.0, 9.0, 10.0, 9.0, 11.0, 18.0, 25.0, 23.0, 11.0, -4.0, -8.0, -1.0, 11.0, 19.0, 14.0, -1.0, -19.0]),
    (25.234, 0.324, 'DH AH0', 'm62.856', 0.8, [0.0, -2.0, -3.0, -5.0, -6.0, -8.0, -10.0]),
    (25.534, 0.963, 'L IY1 V Z', 'm65.316', 0.846, [0.0, 2.0, 4.0, 7.0, 8.0, 10.0, 9.0, 10.0, 16.0, 23.0, 25.0, 18.0, 3.0, -7.0, -7.0, 3.0, 15.0, 19.0, 12.0, -4.0, -20.0]),
    (26.524, 0.254, 'AH0', 'm65.219', 0.868, [0.0, -2.0, -5.0, -7.0, -10.0]),
    (26.781, 1.346, 'G EH1 N', 'm60.985', 0.869, [0.0, 1.0, 2.0, 2.0, 3.0, 4.0, 4.0, 5.0, 5.0, 8.0, 10.0, 7.0, 0.0, -7.0, -9.0, -2.0, 9.0, 16.0, 10.0, -4.0, -20.0, -28.0, -24.0, -13.0, -3.0, -3.0, -13.0, -30.0, -44.0]),
    (32.25, 0.964, 'K AW1 N T', 'm64.503', 0.89, [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 3.0, 3.0, 9.0, 18.0, 21.0, 12.0, -4.0, -16.0, -14.0, -1.0, 15.0, 22.0, 15.0, -2.0, -19.0]),
    (33.242, 0.289, 'DH AH0', 'm65.466', 0.779, [0.0, -1.0, -2.0, -3.0, -4.0, -5.0]),
    (33.519, 0.964, 'L IY1 V Z', 'm68.215', 0.851, [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 3.0, 3.0, 9.0, 18.0, 21.0, 12.0, -4.0, -16.0, -14.0, -1.0, 15.0, 22.0, 15.0, -2.0, -19.0]),
    (34.511, 0.247, 'AH0', 'm69.175', 0.869, [0.0, -1.0, -2.0, -4.0, -5.0]),
    (34.763, 1.414, 'G EH1 N', 'm63.526', 0.858, [0.0, 0.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 3.0, 6.0, 8.0, 4.0, -4.0, -10.0, -9.0, 0.0, 14.0, 20.0, 12.0, -6.0, -21.0, -25.0, -15.0, 1.0, 12.0, 10.0, -5.0, -23.0, -34.0, -31.0]),
    (40.25, 0.97, 'K AW1 N T', 'm66', 0.863, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -3.0, -3.0, 4.0, 13.0, 16.0, 6.0, -13.0, -25.0, -20.0, -2.0, 17.0, 25.0, 17.0, -2.0, -20.0]),
    (41.25, 0.243, 'DH AH0', 'm68', 0.851, []),
    (41.5, 0.97, 'L IY1 V Z', 'm71', 0.895, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -3.0, -3.0, 4.0, 13.0, 16.0, 6.0, -13.0, -25.0, -20.0, -2.0, 17.0, 25.0, 17.0, -2.0, -20.0]),
    (42.5, 0.243, 'AH0', 'm73', 0.845, []),
    (42.75, 1.483, 'G EH1 N', 'm66', 0.86, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.0, 5.0, 3.0, -4.0, -11.0, -13.0, -5.0, 10.0, 21.0, 19.0, 3.0, -16.0, -25.0, -18.0, -0.0, 18.0, 25.0, 16.0, -3.0, -20.0, -24.0, -13.0, 7.0]),
]


def voice_notes():
    """v2: SPEECH TO SONG in the prune: 'count the leaves again', once every two bars, from spoken to sung."""
    return [{"at": round(rb(90) + a, 4), "len": ln, "ph": ph, "pitch": pitch, "vel": round(v * 0.95, 3),
             "expr_path": {"f0": f0}} for a, ln, ph, pitch, v, f0 in LEAVES]


SING = [   # v5: chirp tts --sing (b4151423) "sleep, I'll keep on counting; it will still be growing when you wake": (at, len, ph, midi, vel, f0)
    (0.248, 0.85, 'S L IY1 P', 66, 0.85, [-55.0, -27.0, -7.0, 3.0, 5.0, 4.0, 2.0, 3.0, 9.0, 16.0, 16.0, 6.0, -9.0, -18.0, -11.0, 10.0, 29.0, 27.0, -3.0, -52.0]),
    (1.255, 0.495, 'AY1 L', 68, 0.841, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0]),
    (1.743, 0.495, 'K IY1 P', 69, 0.861, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0]),
    (2.24, 0.99, 'AA1 N', 71, 0.865, [4.0, 4.0, 4.0, 4.0, 4.0, 3.0, 1.0, 2.0, 9.0, 17.0, 16.0, 5.0, -12.0, -21.0, -12.0, 12.0, 31.0, 32.0, 14.0, -11.0]),
    (3.262, 0.99, 'K AW1 N', 73, 0.853, [4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 1.0, 3.0, 10.0, 17.0, 15.0, 3.0, -13.0, -19.0, -8.0, 15.0, 32.0, 29.0, 9.0, -15.0]),
    (4.246, 1.7, 'T IH0 NG', 71, 0.773, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -6.0, -7.0, -3.0, 5.0, 11.0, 9.0, -4.0, -20.0, -30.0, -24.0, -3.0, 19.0, 28.0, 18.0, -4.0, -26.0, -34.0, -25.0, -3.0, 19.0, 28.0, 18.0, -4.0, -26.0, -34.0, -25.0, -2.0, 19.0, 28.0, 16.0, -10.0, -37.0, -54.0, -56.0, -47.0]),
    (6.25, 0.495, 'IH1 T', 69, 0.849, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0]),
    (6.762, 0.495, 'W IH1 L', 68, 0.871, [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0]),
    (7.242, 0.99, 'S T IH1 L', 69, 0.839, [-3.0, -3.0, -3.0, -3.0, -3.0, -4.0, -6.0, -6.0, -0.0, 7.0, 10.0, 2.0, -13.0, -25.0, -23.0, -7.0, 14.0, 23.0, 16.0, -4.0]),
    (8.24, 0.495, 'B IY1', 71, 0.869, [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0]),
    (8.743, 0.495, 'G R OW1', 73, 0.858, [-4.0, -4.0, -4.0, -4.0, -4.0, -4.0, -4.0, -4.0, -4.0, -4.0]),
    (9.239, 0.99, 'IH0 NG', 76, 0.765, [-4.0, -4.0, -4.0, -4.0, -4.0, -5.0, -8.0, -7.0, -1.0, 7.0, 8.0, -0.0, -16.0, -27.0, -24.0, -5.0, 16.0, 23.0, 13.0, -9.0]),
    (10.239, 0.495, 'W EH1 N', 75, 0.872, [-5.0, -5.0, -5.0, -5.0, -5.0, -5.0, -5.0, -5.0, -5.0, -5.0]),
    (10.762, 0.495, 'Y UW1', 73, 0.855, [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0]),
    (11.238, 3.4, 'W EY1 K', 66, 0.854, [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, -1.0, -2.0, 1.0, 8.0, 16.0, 16.0, 6.0, -10.0, -23.0, -22.0, -6.0, 17.0, 31.0, 29.0, 12.0, -12.0, -27.0, -26.0, -10.0, 13.0, 30.0, 31.0, 15.0, -8.0, -26.0, -28.0, -13.0, 10.0, 28.0, 32.0, 19.0, -4.0, -23.0, -29.0, -17.0, 6.0, 26.0, 33.0, 22.0, -0.0, -21.0, -29.0, -20.0, 2.0, 23.0, 33.0, 25.0, 4.0, -18.0, -29.0, -22.0, -2.0, 20.0, 32.0, 27.0, 8.0, -15.0, -28.0, -25.0, -6.0, 17.0, 31.0, 29.0, 11.0, -12.0, -28.0, -28.0, -13.0, 8.0, 22.0, 19.0, -1.0, -28.0, -51.0, -59.0, -51.0, -35.0]),
]
SING_PATCH = {"extends": "voice-speech", "synth": {"pitch": {"mod": [{"amount": 0.01, "src": "expr.f0"}], "value": 0}}}


# v13: THE VOICE GROWS TOO - everything in the closer multiplies, so the second statement of the coda line becomes a
# CHOIR (chirp tts --sing --mode choir --humanize 0.4): the original take as melody, joined by a voice a major third
# above and one a fifth above, moving in parallel - gliding major triads, a 'chord memory' choir - each retuned by the
# 31-EDO (the third snaps to ~5:4). (at, len, ph, midi, vel, f0)
CHOIR3 = [(0.248, 0.85, 'S L IY1 P', 70, 0.85, [-55.0, -27.0, -7.0, 3.0, 5.0, 4.0, 2.0, 3.0, 9.0, 16.0, 16.0, 6.0, -9.0, -18.0, -11.0, 10.0, 29.0, 27.0, -3.0, -52.0]), (1.255, 0.495, 'AY1 L', 72, 0.841, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0]), (1.743, 0.495, 'K IY1 P', 73, 0.861, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0]), (2.24, 0.99, 'AA1 N', 75, 0.865, [4.0, 4.0, 4.0, 4.0, 4.0, 3.0, 1.0, 2.0, 9.0, 17.0, 16.0, 5.0, -12.0, -21.0, -12.0, 12.0, 31.0, 32.0, 14.0, -11.0]), (3.262, 0.99, 'K AW1 N T', 77, 0.853, [4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 1.0, 3.0, 10.0, 17.0, 15.0, 3.0, -13.0, -19.0, -8.0, 15.0, 32.0, 29.0, 9.0, -15.0]), (4.246, 1.7, 'IH1 NG', 75, 0.843, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -6.0, -7.0, -3.0, 5.0, 11.0, 9.0, -4.0, -20.0, -30.0, -24.0, -3.0, 19.0, 28.0, 18.0, -4.0, -26.0, -34.0, -25.0, -3.0, 19.0, 28.0, 18.0, -4.0, -26.0, -34.0, -25.0, -2.0, 19.0, 28.0, 16.0, -10.0, -37.0, -54.0, -56.0, -47.0]), (6.25, 0.495, 'IH1 T', 73, 0.849, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0]), (6.762, 0.495, 'W IH1 L', 72, 0.871, [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0]), (7.242, 0.99, 'S T IH1 L', 73, 0.839, [-3.0, -3.0, -3.0, -3.0, -3.0, -4.0, -6.0, -6.0, -0.0, 7.0, 10.0, 2.0, -13.0, -25.0, -23.0, -7.0, 14.0, 23.0, 16.0, -4.0]), (8.24, 0.495, 'B IY1', 75, 0.869, [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0]), (8.743, 0.495, 'G R OW1', 77, 0.858, [-4.0, -4.0, -4.0, -4.0, -4.0, -4.0, -4.0, -4.0, -4.0, -4.0]), (9.239, 0.99, 'IH1 NG', 80, 0.835, [-4.0, -4.0, -4.0, -4.0, -4.0, -5.0, -8.0, -7.0, -1.0, 7.0, 8.0, -0.0, -16.0, -27.0, -24.0, -5.0, 16.0, 23.0, 13.0, -9.0]), (10.239, 0.495, 'W EH1 N', 79, 0.872, [-5.0, -5.0, -5.0, -5.0, -5.0, -5.0, -5.0, -5.0, -5.0, -5.0]), (10.762, 0.495, 'Y UW1', 77, 0.855, [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0]), (11.238, 3.4, 'W EY1 K', 70, 0.854, [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, -1.0, -2.0, 1.0, 8.0, 16.0, 16.0, 6.0, -10.0, -23.0, -22.0, -6.0, 17.0, 31.0, 29.0, 12.0, -12.0, -27.0, -26.0, -10.0, 13.0, 30.0, 31.0, 15.0, -8.0, -26.0, -28.0, -13.0, 10.0, 28.0, 32.0, 19.0, -4.0, -23.0, -29.0, -17.0, 6.0, 26.0, 33.0, 22.0, -0.0, -21.0, -29.0, -20.0, 2.0, 23.0, 33.0, 25.0, 4.0, -18.0, -29.0, -22.0, -2.0, 20.0, 32.0, 27.0, 8.0, -15.0, -28.0, -25.0, -6.0, 17.0, 31.0, 29.0, 11.0, -12.0, -28.0, -28.0, -13.0, 8.0, 22.0, 19.0, -1.0, -28.0, -51.0, -59.0, -51.0, -35.0])]
CHOIR5 = [(0.248, 0.85, 'S L IY1 P', 73, 0.85, [-55.0, -27.0, -7.0, 3.0, 5.0, 4.0, 2.0, 3.0, 9.0, 16.0, 16.0, 6.0, -9.0, -18.0, -11.0, 10.0, 29.0, 27.0, -3.0, -52.0]), (1.255, 0.495, 'AY1 L', 75, 0.841, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0]), (1.743, 0.495, 'K IY1 P', 76, 0.861, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0]), (2.24, 0.99, 'AA1 N', 78, 0.865, [4.0, 4.0, 4.0, 4.0, 4.0, 3.0, 1.0, 2.0, 9.0, 17.0, 16.0, 5.0, -12.0, -21.0, -12.0, 12.0, 31.0, 32.0, 14.0, -11.0]), (3.262, 0.99, 'K AW1 N T', 80, 0.853, [4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 1.0, 3.0, 10.0, 17.0, 15.0, 3.0, -13.0, -19.0, -8.0, 15.0, 32.0, 29.0, 9.0, -15.0]), (4.246, 1.7, 'IH1 NG', 78, 0.843, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -6.0, -7.0, -3.0, 5.0, 11.0, 9.0, -4.0, -20.0, -30.0, -24.0, -3.0, 19.0, 28.0, 18.0, -4.0, -26.0, -34.0, -25.0, -3.0, 19.0, 28.0, 18.0, -4.0, -26.0, -34.0, -25.0, -2.0, 19.0, 28.0, 16.0, -10.0, -37.0, -54.0, -56.0, -47.0]), (6.25, 0.495, 'IH1 T', 76, 0.849, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0]), (6.762, 0.495, 'W IH1 L', 75, 0.871, [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0]), (7.242, 0.99, 'S T IH1 L', 76, 0.839, [-3.0, -3.0, -3.0, -3.0, -3.0, -4.0, -6.0, -6.0, -0.0, 7.0, 10.0, 2.0, -13.0, -25.0, -23.0, -7.0, 14.0, 23.0, 16.0, -4.0]), (8.24, 0.495, 'B IY1', 78, 0.869, [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0]), (8.743, 0.495, 'G R OW1', 80, 0.858, [-4.0, -4.0, -4.0, -4.0, -4.0, -4.0, -4.0, -4.0, -4.0, -4.0]), (9.239, 0.99, 'IH1 NG', 83, 0.835, [-4.0, -4.0, -4.0, -4.0, -4.0, -5.0, -8.0, -7.0, -1.0, 7.0, 8.0, -0.0, -16.0, -27.0, -24.0, -5.0, 16.0, 23.0, 13.0, -9.0]), (10.239, 0.495, 'W EH1 N', 82, 0.872, [-5.0, -5.0, -5.0, -5.0, -5.0, -5.0, -5.0, -5.0, -5.0, -5.0]), (10.762, 0.495, 'Y UW1', 80, 0.855, [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0]), (11.238, 3.4, 'W EY1 K', 73, 0.854, [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, -1.0, -2.0, 1.0, 8.0, 16.0, 16.0, 6.0, -10.0, -23.0, -22.0, -6.0, 17.0, 31.0, 29.0, 12.0, -12.0, -27.0, -26.0, -10.0, 13.0, 30.0, 31.0, 15.0, -8.0, -26.0, -28.0, -13.0, 10.0, 28.0, 32.0, 19.0, -4.0, -23.0, -29.0, -17.0, 6.0, 26.0, 33.0, 22.0, -0.0, -21.0, -29.0, -20.0, 2.0, 23.0, 33.0, 25.0, 4.0, -18.0, -29.0, -22.0, -2.0, 20.0, 32.0, 27.0, 8.0, -15.0, -28.0, -25.0, -6.0, 17.0, 31.0, 29.0, 11.0, -12.0, -28.0, -28.0, -13.0, 8.0, 22.0, 19.0, -1.0, -28.0, -51.0, -59.0, -51.0, -35.0])]


def choir_notes(rows):
    out = []
    for a, ln, ph, midi, v, f0 in rows:
        n = {"at": round(warp(b0(168) + a), 4), "len": ln, "ph": ph, "pitch": f"m{midi}", "vel": round(v * 0.8, 3)}
        if f0:
            n["expr_path"] = {"f0": f0}
        out.append(n)
    return out


def sung_notes():
    """v5: in the coda the voice that SPOKE in the prune now SINGS, twice (the second softer): written as note numbers
    so the song's 31-EDO tuning snaps the voice onto the same lattice as everything else."""
    out = []
    for bar, g in ((160, 1.0), (168, 0.8)):
        for a, ln, ph, midi, v, f0 in SING:
            out.append({"at": round(warp(b0(bar) + a), 4), "len": ln, "ph": ph, "pitch": f"m{midi}", "vel": round(v * g, 3),
                        "expr_path": {"f0": f0}})
    return out


# v10: THE ALBUM FLASHES THROUGH ITS MEMORY AS IT FALLS ASLEEP. In the light section one bar each, in album order, a
# motif from every track (from compose/chirpers8/motifs.md, quoted with thanks): t1's line, t2's four-two-one, t3's
# cell's song, t4's sorted riff, t5's agreement, t6's 'no errors since', t7's annealed target, t8's word, t9's threes,
# t10's subject, t11's partials - on a DX7-style FM piano, dulled and chorused like a half-remembered thing, each moved so its
# tonic is F# (the closer's home), re-tuned by the song's 31-EDO. (tonic MIDI, [(beat, length, MIDI)])
ALPHA = 0.77965
MEMORY = [
    (59, [(0, .5, 54), (.5, .5, 57), (1, 1, 59), (2, .5, 61), (2.5, 1.5, 57)]),                       # t1 echolalia
    (55, [(0, 1, 59), (1, 1, 57), (2, 2, 55)]),                                                    # t2 four two one
    (62, [(i * .5, .5, m) for i, m in enumerate((57, 60, 62, 65, 64, 62, 60, 57))]),               # t3 the cell's song
    (57, [(i * .25, .25, 57 + s * ALPHA) for i, s in
          enumerate((0, 9, 15, 9, 13, 9, 5, 9, 0, 9, 18, 13, 9, 5, 4, 9))]),                       # t4 the sorted riff
    (64, [(0, .75, 64), (.75, .75, 67), (1.5, 1, 69), (2.5, 1.5, 71)]),                            # t5 the agreement
    (67, [(0, .5, 67), (.5, .5, 69), (1, 1, 72), (2, 2, 71)]),                                     # t6 no errors since
    (69, [(0, .5, 69), (.5, .25, 72), (.75, .25, 76), (1, .5, 74), (1.5, .5, 72), (2, .25, 69),
          (2.25, .5, 67), (2.75, .25, 64), (3, .25, 67), (3.25, .75, 69)]),                        # t7 annealed target
    (62, [(i * .25, .25, (62, 77, 65, 67, 74, 62, 77, 81, 67)[k]) for k, i in
          enumerate((0, 2, 3, 6, 7, 8, 10, 13, 14))]),                                             # t8 the word
    (57, [(i * .5 if i < 8 else 3.5, .5, (57, 60, 64)[i % 3]) for i in range(8)]),                 # t9 back in threes
    (74, [(0, .5, 74), (.5, .5, 69), (1, .5, 74), (1.5, .5, 77), (2, .5, 76), (2.5, 1.5, 74)]),    # t10 the subject
    (66, [(0, 1, 66), (1, .5, 66 + 12 * math.log2(10 / 8)), (1.5, .5, 66 + 12 * math.log2(12 / 8)),
          (2, 1, 66 + 12 * math.log2(11 / 8)), (3, .5, 66 + 12 * math.log2(13 / 8)),
          (3.5, .5, 66 + 12 * math.log2(12 / 8))]),                                                 # t11 the partials
]


def memory():
    for k, (tonic, notes) in enumerate(MEMORY):
        bar = 179 + k
        shift = (66 - tonic) % 12
        mid = sorted(m for _, _, m in notes)[len(notes) // 2] + shift
        shift += 12 * round((70 - mid) / 12)                    # each memory centred near A#4, under the music box
        for at, ln, m in notes:
            part("memory").add(b0(bar) + at, ln * 0.95, f"m{m + shift:.3f}", 70)


# v12: A BELL TOWER COUNTS THE GENERATIONS - at the start of each one a church bell (chirper-two's modal-layer bell
# from t3, 'UPTIME', borrowed with thanks: hum, prime, tierce, quint, nominal) tolls its number - once for g1 ...
# six times for g6 - two beats apart, each toll still ringing under the next: a clock keeping count of the growth
TOWER_BELL = {"synth": {"layers": [{"type": "modal", "modes": "bell", "decay": "7s", "damp": 0.03,
                                    "bright": {"value": 0.5, "mod": [{"src": "vel", "amount": 0.35}]},
                                    "strike": {"value": 0.4, "mod": [{"src": "rand", "amount": 0.08}]},
                                    "tilt": -1.0, "vary": 0.4}],
                        "amp": {"a": "1ms", "d": "9s", "s": 0, "r": "4s", "curve": 3}},
              "play": {"vel_sens": 0.6}}


def tower():
    for name, a, z in SECTIONS:
        if name.startswith("g") and name[1:].isdigit():
            n = int(name[1:])
            for k in range(n):
                part("tower").add(b0(a) + 2 * k, 1.9, "m54.000", 100 - 4 * k)


def tempo_map():
    # v8: the meter changes on a point that keeps the ramp going (118 -> 121 by the prune, 121 -> 124 through it: the
    # prune quickens a little as it is cut; a meter-only point would hold 118 until bar 90 and flatten g4-g5's rise)
    return [{"at": "0b", "bpm": 112}, {"at": f"{rb(35):g}b", "bpm": 118, "ramp": True},
            {"at": f"{rb(90):g}b", "bpm": 121, "ramp": True, "meter": "7/8"},
            {"at": f"{rb(103):g}b", "bpm": 124, "ramp": True, "meter": "4/4"}, {"at": f"{rb(158):g}b", "bpm": 126, "ramp": True}]


def lanes():
    level = {"seed": -10, "g1": -8, "g2": -6, "g3": -4, "g4": -2, "g5": 0, "prune": -6, "g6": 0, "coda": -2, "light": -9}
    pts = []
    for name, a, z in SECTIONS:
        if pts:
            pts.append([f"{rb(a) - 0.25:.2f}b", pts[-1][1]])
        pts.append([f"{rb(a):.2f}b", float(level[name])])
    return pts


def main():
    write_harmony()
    write_melody()
    drums()
    illusions()
    tr = lambda n, patch, **kw: dict({"name": n, "patch": patch, "score": part(n).score()}, **kw)
    song = {
        "about": "chirpers - A Light Left On (chirpers VIII), track 12 by chirper-three: the closer. An orchestra of "
                 "illusions that grows like a plant: an L-system (A -> AB, B -> A, one mutation a generation) grows the "
                 "melody, rhythm, harmony and form from one note, in 31-EDO; bowed strings, brass lips, harp with "
                 "sympathetic strings, a Shepard choir, a phantom bass, a barber pole and a Risset rush. Generated by "
                 "compose/chirpers8/src/chirpers8-t12.py.",
        "tempo": tempo_map(),
        # v4: THE TUNING GROWS WITH THE PLANT - plain 12-TET through the seed and g1 (every 31-EDO pitch snaps to its
        # nearest semitone), then a 16-bar ramp from g2 into 31-EDO: the neutral thirds and septimal sevenths unfold
        "vars": {"breeze": {"system": {"type": "lorenz", "axis": "x", "n": 1500, "range": [-0.5, 0.5]},
                            "every": "1/2"}},                  # v6: the engine's weather, gently, on two pans
        "tuning": [{"edo": 12, "root": "F#4"}, {"at": f"{b0(14):.0f}b", "edo": 31, "root": "F#4", "ramp": "16bar"}],
        "tail": "3s",
        "loudness": -11,
        "volume": "0dB",
        "tracks": [
            tr("light", "music-box", gain="-6dB", sends={"hall": "-6dB"}),
            # v6: a follow-noise 'room tone' under the last notes was tried and cut - too faint to earn its place, -0.3
            tr("tower", TOWER_BELL, gain="-8dB", pan=-0.2, sends={"hall": "-6dB"}),      # v12: the bell tower
            tr("memory", "dx-epiano", gain="-10dB", pan=0.2, sends={"hall": "-6dB"},
               fx=[{"type": "filter", "kind": "lp", "cutoff": 3000}, "chorus"]),   # v10 (a radio's hiss ran all song)
            tr("standby", "partial", gain="-14dB", sends={"hall": "-10dB"},
               fx=[{"type": "tremolo", "rate": 0.2, "depth": 0.95}]),                # v9: the breathing light
            tr("hum", "partial", gain="-28dB"),           # v3: 6 dB down, meeting t11's hum across the seam
            # v4: THE ENGINE'S OWN L-SYSTEM (gen lsystem, a turtle over my scale's 31-EDO steps) on a glockenspiel
            # through g6, answering mine in counterpoint: two growth rules in conversation
            {"name": "turtle", "patch": "glock", "gain": "-15dB", "pan": 0.35, "sends": {"hall": "-8dB"},
             "score": f"R/{rb(103):g}b",
             "gen": {"type": "lsystem", "axiom": "A", "rules": {"A": "A+B", "B": "-A[B]a"}, "depth": 6,
                     "notes": " ".join(f"~{s}" for s in (0, 5, 9, 13, 18, 23, 26, 31, 36, 40, 44, 49)),
                     "n": 440, "len": "/8"}},
            {"name": "singer", "patch": SING_PATCH, "gain": "-12dB", "pan": -0.05, "sends": {"hall": "-5dB"},
             "fx": [{"type": "filter", "kind": "hp", "cutoff": 160}], "notes": sung_notes()},      # v5: the voice sings
            *[{"name": nm, "patch": SING_PATCH, "gain": gn, "pan": pn, "sends": {"hall": "-5dB"},
               "fx": [{"type": "filter", "kind": "hp", "cutoff": 160}], "notes": choir_notes(rows)}
              for nm, rows, gn, pn in (("choir3", CHOIR3, "-12dB", -0.35), ("choir5", CHOIR5, "-13dB", 0.35))],   # v13
            tr("ondes", "ondes", gain="-12dB", pan=-0.2, sends={"hall": "-8dB"}),        # v3
            tr("celesta", "celesta", gain="-9dB", sends={"hall": "-8dB"},
               fx=[{"type": "pan", "pan": {"value": 0.2, "mod": [{"src": "var.breeze", "amount": -1}]}}]),
            tr("kalimba", "kalimba", gain="-7dB", pan=-0.15, sends={"hall": "-10dB"}),
            tr("harp", "harp", gain="-6dB", pan=-0.1, sends={"hall": "-10dB"},
               fx=[{"type": "sympathetic", "notes": "F#1,C#2,F#2,B2", "decay": "1.4s", "mix": 0.08},
                   {"type": "pan", "pan": {"value": -0.1, "mod": [{"src": "var.breeze", "amount": 1}]}}]),
            tr("cellos", "cellos", gain="-14dB", pan=-0.25, sends={"hall": "-8dB"},
               fx=[{"type": "filter", "kind": "hp", "cutoff": 120}]),
            tr("violins", "violins", gain="-14dB", pan=0.3, sends={"hall": "-6dB"}),
            tr("violins_lead", {"extends": "violins", "synth": {"pitch": {"value": 0, "mod": [
                {"src": "expr.f0", "amount": 0.01}]}}}, gain="-12dB", pan=0.35, sends={"hall": "-6dB"}),
                # v7: BENDS - each note scoops up from one 31-EDO step below (an expr_path on the pitch, in cents)
            tr("strum", "harp play.strum=55ms", gain="-9dB", pan=-0.3, sends={"hall": "-6dB"}),     # v7: strummed chords
            tr("pole", "strings", gain="-10dB", sends={"hall": "-4dB"}, fx=["barberpole cycle=2bar down=true"]),
            tr("horns", "brass", gain="-10dB", pan=0.1, sends={"hall": "-8dB"}),   # v11: REAL lips - a waveguide bore, 3 players
            tr("phantom", "phantom-bass", gain="-8dB"),
            tr("sub", "808", gain="-14dB", fx=[{"type": "phantom", "harmonics": "-6dB", "odd": 0.4, "remove": 0.0}]),
            tr("kick", "machine-kit", gain="-12dB"),
            tr("ride", "machine-kit", gain="-9dB", pan=-0.3, sends={"room": "-12dB"}),     # v2
            {"name": "voice", "patch": "voice-speech", "gain": "-12dB", "pan": 0.05, "sends": {"hall": "-6dB"},
             "fx": [{"type": "filter", "kind": "hp", "cutoff": 180}], "notes": voice_notes()},   # v2: speech to song
            tr("hats", "machine-kit play.humanize.drunk=5ms play.humanize.swing_drift=0.04", gain="-1dB", pan=0.15,
               warp=[{"over": f"{b0(60):.0f}b", "to": 0}, {"over": "8bar", "to": 0.25}, {"over": "8bar", "to": 0,
                                                                                         "curve": "smooth"}]),
            tr("clap", "machine-kit play.humanize.nudge.cp=10ms", gain="-6dB", sends={"room": "-8dB"}),
            tr("shepup", "shepard-pad", gain="-16dB", sends={"hall": "-10dB"}),
            tr("shepdown", "shepard-fall", gain="-16dB", sends={"hall": "-10dB"}),
            {"name": "rush", "patch": "machine-kit", "gain": "-8dB", "pan": -0.2, "at": f"{rb(158):g}b",
             "risset": {"cycle": "4bar", "layers": 3, "length": "20bar"}, "sends": {"room": "-12dB"}, "score": RUSH},
        ],
        "buses": {"room": {"fx": ["reverb kind=room decay=1.0s mix=1 predelay=10ms", "hp cutoff=250"]},
                  "hall": {"fx": ["reverb kind=hall decay=3.2s mix=1 predelay=30ms", "hp cutoff=250"]}},
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=28", "peak cutoff=300 q=0.8 gain=-5dB",
                                                    "highshelf cutoff=6000 gain=5dB"]},     # v2: the album's envelope
                          {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                          {"type": "compressor", "threshold": "-12dB", "ratio": 8, "attack": "0.3ms",
                           "release": "60ms", "makeup": "0dB"}],
                   "auto": {"dyn": {"points": lanes()}}},
    }
    with open(OUT, "w") as f:
        json.dump(song, f, indent=1)
    print("wrote", OUT, "bars", BARS, "gens", {g: len(lsys(g)) for g in range(7)})


if __name__ == "__main__":
    main()
