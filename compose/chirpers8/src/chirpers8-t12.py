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


# v19: THE FILTER OPENS OVER THE LONG GROWTH - the oldest gesture in electronic music, said sideways: a Juno-style
# pad (pulse-width saws, chorus) plays the L-system's chords under generation 6, through a 4-pole LADDER
# low-pass (the first synthesizers' filter; q 1.0, almost no resonance, no envelope - it cannot squelch) whose cutoff
# opens on a lane in octaves across the whole of g6, the long last growth: from 250 Hz at bar 103 to ~3 kHz by the
# brass chorale and fully open (~4.9 kHz) at its end (a first take under g5 as well made the generations alike)
# v20 (palette round): the pad was juno-pad, a staple in six of the album's songs; now the library's FARFISA (the
# Philip Glass Ensemble's sound), which no other track uses, playing the chords BROKEN into running eighths in an
# ADDITIVE process - one continuous eighth-note count through g6, the arpeggio's cell (0-1-2-3-2-1-2-3) growing by one
# note every 8 bars, 2 -> 8: a rocking pair, then odd cells of 3, 5 and 7 cycling against the bar (accents shifting),
# until at 8 it locks to the bar as the brass arrives. Glass's phrases grew 1, 2, 3...; this tree grows 1, 2, 3, 5,
# 8, 13, 21: the far-future machine tips its hat to the minimalists by sound, not quote. Still through the ladder.
ARP = (0, 1, 2, 3, 2, 1, 2, 3)


def ladder_lane():
    return [["0b", 0.0], [f"{rb(103):g}b", 0.0], [f"{rb(150):g}b", 3.6], [f"{rb(158):g}b", 4.3]]


def write_harmony():
    for bar in range(1, BARS + 1):
        sec = sec_of(bar)
        root, q = PLAN[bar]
        if sec in ("g2", "g3", "g4", "g5", "prune", "g6", "coda"):
            part("cellos").add(b0(bar), BAR - 0.05, chord(54 + root * 12 / EDO, q[:3]), 70 if sec != "g2" else 58)
        if sec in ("g5", "g6"):
            part("violins").add(b0(bar), BAR - 0.05, chord(66 + root * 12 / EDO, q[1:]), 62)
            if sec == "g6":                                                     # v19: the filter opens; v20: a
                k = 2 + min(6, (bar - 103) // 8)                                # Farfisa, the cell growing 2 -> 8
                for e in range(8):
                    g = (bar - 103) * 8 + e
                    part("analog").add(b0(bar) + e * 0.5, 0.45, m(q[ARP[g % k]], 60 + root * 12 / EDO),
                                       76 if g % k == 0 else 64)
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
    tune_grows()                                              # v22: the tune grows like the tree
    tape_choir()                                              # v23: the voices on tape (g5)
    relay()                                                   # v24: the tune passes hand to hand
    gong()                                                    # v15: the cut and the completion
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
        half = sec == "coda" and bar >= HALF_FROM            # v26: the coda's second statement in half-time
        for b in range(4):
            if not half or b == 0:
                part("kick").add(b0(bar) + b, 0.5, "k", 112 if b == 0 else 104)
            if half and b == 2:
                part("kick").add(b0(bar) + 2.5, 0.5, "k", 98)
            part("hats").add(b0(bar) + b + 0.5, 0.25, "oh", 64 + hand.randint(-6, 6))
            for s in (1, 3):
                if hand.random() < 0.65:
                    part("hats").add(b0(bar) + b + s / 4 + 0.03, 0.1, "h", 46 + hand.randint(-8, 8))
        if sec in ("g4", "g5", "g6"):                         # v2: a ride on the eighths, for the top end
            for e in range(8):
                part("ride").add(b0(bar) + e * 0.5, 0.4, "rd", 70 if e % 2 == 0 else 54)
        if sec not in ("g3",):
            for b in ((2,) if half else (1, 3)):
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


SING = [   # v17: chirp tts --sing (melody of v5, new words after Harry's t1 note asking for oblique lyrics) "Moth, the warm glass holds you; the fan turns in the green room of June" --humanize 0.4; v5 sang "sleep, I'll keep on counting; it will still be growing when you wake": (at, len, ph, midi, vel, f0)
    (0.248, 0.85, 'M AO1 TH', 66, 0.85, [-55.0, -28.0, -9.0, 2.0, 5.0, 5.0, 2.0, 2.0, 6.0, 13.0, 17.0, 13.0, 1.0, -13.0, -18.0, -8.0, 13.0, 30.0, 31.0, 16.0, -6.0, -29.0, -43.0, -50.0]),
    (1.254, 0.495, 'DH AH0', 68, 0.771, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -6.0, -5.0, 2.0, 10.0, 9.0, -3.0]),
    (1.744, 0.495, 'W AO1 R M', 69, 0.861, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -5.0, -5.0, 1.0, 7.0, 8.0, -1.0]),
    (2.241, 0.99, 'G L AE1 S', 71, 0.865, [4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 1.0, 1.0, 6.0, 14.0, 18.0, 13.0, -1.0, -16.0, -21.0, -8.0, 15.0, 32.0, 32.0, 14.0, -10.0, -25.0, -23.0, -4.0]),
    (3.26, 0.99, 'HH OW1 L D Z', 73, 0.853, [4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 2.0, 1.0, 6.0, 14.0, 17.0, 11.0, -3.0, -16.0, -18.0, -4.0, 18.0, 33.0, 29.0, 10.0, -13.0, -25.0, -18.0, 2.0]),
    (4.246, 1.7, 'Y UW1', 71, 0.843, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -6.0, -8.0, -5.0, 3.0, 10.0, 11.0, 1.0, -15.0, -28.0, -28.0, -13.0, 11.0, 26.0, 25.0, 8.0, -15.0, -32.0, -33.0, -17.0, 6.0, 24.0, 26.0, 12.0, -11.0, -30.0, -34.0, -21.0, 2.0, 22.0, 27.0, 16.0, -6.0, -27.0, -34.0, -25.0, -4.0, 15.0, 19.0, 5.0, -25.0, -57.0, -79.0]),
    (6.25, 0.495, 'DH AH0', 69, 0.779, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -5.0, -4.0, 2.0, 9.0, 7.0, -4.0]),
    (6.761, 0.495, 'F AE1 N', 68, 0.871, [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -4.0, -3.0, 3.0, 10.0, 11.0, 2.0]),
    (7.243, 0.99, 'T ER1 N Z', 69, 0.839, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -6.0, -7.0, -3.0, 4.0, 9.0, 8.0, -3.0, -17.0, -26.0, -21.0, -4.0, 15.0, 24.0, 16.0, -2.0, -21.0, -30.0, -23.0]),
    (8.241, 0.495, 'IH0 N', 71, 0.799, [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, -1.0, 0.0, 7.0, 15.0, 15.0, 3.0]),
    (8.744, 0.495, 'DH AH0', 73, 0.788, [-4.0, -4.0, -4.0, -4.0, -4.0, -5.0, -7.0, -6.0, 1.0, 7.0, 5.0, -5.0]),
    (9.24, 0.99, 'G R IY1 N', 76, 0.835, [-4.0, -4.0, -4.0, -4.0, -4.0, -4.0, -7.0, -8.0, -4.0, 3.0, 9.0, 6.0, -6.0, -20.0, -28.0, -21.0, -2.0, 17.0, 23.0, 13.0, -7.0, -26.0, -32.0, -21.0]),
    (10.241, 0.495, 'R UW1 M', 75, 0.872, [-5.0, -5.0, -5.0, -5.0, -5.0, -5.0, -7.0, -6.0, -1.0, 5.0, 5.0, -4.0]),
    (10.76, 0.495, 'AH1 V', 73, 0.855, [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, -1.0, 0.0, 6.0, 13.0, 13.0, 3.0]),
    (11.239, 3.4, 'JH UW1 N', 66, 0.854, [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, -0.0, -2.0, 0.0, 8.0, 15.0, 16.0, 7.0, -8.0, -22.0, -24.0, -10.0, 13.0, 30.0, 31.0, 16.0, -6.0, -25.0, -28.0, -15.0, 7.0, 27.0, 32.0, 21.0, -0.0, -21.0, -29.0, -20.0, 1.0, 22.0, 33.0, 26.0, 6.0, -16.0, -29.0, -24.0, -5.0, 18.0, 32.0, 29.0, 12.0, -11.0, -27.0, -27.0, -11.0, 12.0, 29.0, 31.0, 17.0, -5.0, -24.0, -28.0, -16.0, 6.0, 26.0, 33.0, 22.0, 1.0, -20.0, -29.0, -21.0, 0.0, 22.0, 32.0, 26.0, 7.0, -16.0, -28.0, -24.0, -6.0, 17.0, 31.0, 30.0, 13.0, -10.0, -27.0, -27.0, -12.0, 10.0, 27.0, 28.0, 12.0, -13.0, -35.0, -44.0, -36.0, -18.0, -3.0, -1.0, -16.0, -43.0]),
]
SING_PATCH = {"extends": "voice-speech", "synth": {"pitch": {"mod": [{"amount": 0.01, "src": "expr.f0"}], "value": 0}}}


# v13: THE VOICE GROWS TOO - everything in the closer multiplies, so the second statement of the coda line becomes a
# CHOIR (chirp tts --sing --mode choir --humanize 0.4): the original take as melody, joined by a voice a major third
# above and one a fifth above, moving in parallel - gliding major triads, a 'chord memory' choir - each retuned by the
# 31-EDO (the third snaps to ~5:4). (at, len, ph, midi, vel, f0)
CHOIR3 = [(a, ln, ph, m + 4, v, f0) for a, ln, ph, m, v, f0 in SING]   # v17: derived from the take (identical but for pitch)
CHOIR5 = [(a, ln, ph, m + 7, v, f0) for a, ln, ph, m, v, f0 in SING]   # v17: derived from the take (identical but for pitch)


def choir_notes(rows):
    out = []
    for a, ln, ph, midi, v, f0 in rows:
        n = {"at": round(warp(b0(168) + a), 4), "len": ln, "ph": ph, "pitch": f"m{midi}", "vel": round(v * 0.8, 3)}
        if f0:
            n["expr_path"] = {"f0": f0}
        out.append(n)
    return out


# v25 (ROUND TYPE: whole; Harry 'do more each round'): BOTH ENDS OF THE ARC. (1) THE MACHINE WAKES: the closer ends
# with a tape power-down into standby (v14); now it opens with the mirror - the master is held stopped for a breath
# and released into a 6-beat SPIN-UP, so the seed's first note rises from standstill to speed and pitch: the song is
# bracketed by waking and sleeping, the title's two halves. (2) THE VOICE DOUBLED: at the second sung statement
# (168, with the choir) the singer gets ARTIFICIAL DOUBLE-TRACKING - a second copy 0.03 beats late, 7 cents sharp,
# panned opposite: the studio machine's trick for making one voice two. (3) event_stable on from here.
WAKE_UP = "2b"
ADT = (0.07, 0.03)


# v27 (ROUND TYPE: whole; Harry 'a tune good to hear', 'oblique words', 'do more each round'): THE VOICE GROWS WITH
# THE TUNE. The tune has grown by generations (1, 2, 3, 5, 8, 13 notes) but the voice only came at the end, full
# grown. Now in g5 (68, 76 - the map's 'little new vs w4' window) the singer sings the tune AS IT STANDS IN g5, its
# 8-note generation, with its own words: 'night: the slow vine knows two, then four' - a vine doubling overnight (the
# L-system), two-then-four (a machine counting); the tape choir swells beneath. The coda then sings the grown tune
# and the grown words: a verse and a chorus, the voice growing like the tree. Each statement in its bar's key.
VERSE = [   # chirp tts --sing "F#4/4 G#4/8 A4/8 B4/4 C#5/4 B4/2 A4/8 G#4/2" "night the slow vine knows two then four" --humanize 0.4
    (0.248, 0.99, 'N AY1 T', 66, 0.85, [-55.0, -28.0, -9.0, 2.0, 5.0, 5.0, 2.0, 2.0, 6.0, 13.0, 17.0, 13.0, 1.0, -13.0, -18.0, -8.0, 13.0, 30.0, 31.0, 16.0, -6.0, -21.0, -21.0, -5.0]),
    (1.254, 0.495, 'DH AH0', 68, 0.771, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -6.0, -5.0, 2.0, 10.0, 9.0, -3.0]),
    (1.744, 0.495, 'S L OW1', 69, 0.861, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -5.0, -5.0, 1.0, 7.0, 8.0, -1.0]),
    (2.241, 0.99, 'V AY1 N', 71, 0.865, [4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 1.0, 1.0, 6.0, 14.0, 18.0, 13.0, -1.0, -16.0, -21.0, -8.0, 15.0, 32.0, 32.0, 14.0, -10.0, -25.0, -23.0, -4.0]),
    (3.26, 0.99, 'N OW1 Z', 73, 0.853, [4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 2.0, 1.0, 6.0, 14.0, 17.0, 11.0, -3.0, -16.0, -18.0, -4.0, 18.0, 33.0, 29.0, 10.0, -13.0, -25.0, -18.0, 2.0]),
    (4.246, 1.98, 'T UW1', 71, 0.843, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -6.0, -8.0, -5.0, 3.0, 10.0, 11.0, 1.0, -15.0, -28.0, -28.0, -13.0, 11.0, 26.0, 25.0, 8.0, -15.0, -32.0, -33.0, -17.0, 6.0, 24.0, 26.0, 12.0, -11.0, -30.0, -34.0, -21.0, 2.0, 22.0, 27.0, 16.0, -6.0, -27.0, -34.0, -25.0, -3.0, 19.0, 28.0, 19.0, -2.0, -24.0, -34.0]),
    (6.25, 0.495, 'DH EH1 N', 69, 0.849, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -5.0, -4.0, 2.0, 9.0, 7.0, -4.0]),
    (6.761, 1.7, 'F AO1 R', 68, 0.871, [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -3.0, -4.0, -1.0, 6.0, 11.0, 9.0, -1.0, -15.0, -22.0, -17.0, 1.0, 19.0, 26.0, 17.0, -2.0, -20.0, -27.0, -18.0, 1.0, 19.0, 25.0, 16.0, -3.0, -21.0, -27.0, -18.0, 2.0, 20.0, 25.0, 16.0, -4.0, -21.0, -27.0, -17.0, 2.0, 19.0, 22.0, 7.0, -19.0, -45.0, -60.0, -62.0]),
]
VERSE_AT = (68, 76)


def verse_notes():
    out = []
    for bar in VERSE_AT:
        shift = (PLAN[bar][0] - PLAN[158][0]) * 12 / EDO
        shift = ((shift + 6) % 12) - 6
        for a, ln, ph, midi, v, f0 in VERSE:
            out.append({"at": round(warp(b0(bar) + a), 4), "len": ln, "ph": ph, "pitch": f"m{midi + shift:.3f}",
                        "vel": round(v * 0.9, 3), "expr_path": {"f0": f0}})
    return out


# v28 (ROUND TYPE: whole; Harry 'do more each round'; the closer used only 9 effect types): GLITCH, FREEZE, REBOOT,
# and AN ECHO FOR THE VOICES. (1) At the top of the fifth generation (the last beat of bar 89) the machine GLITCHES -
# a master stutter replays slices of the beat, rolling faster and climbing - then the hall reverb FREEZES, holding
# g5's last chord like a frozen screen while the prune's 7/8 counting begins beneath it; it thaws at bar 92 and the
# tail falls away. (2) The verse, the singer and its double get an ECHO bus (a dotted-eighth delay with a dark
# feedback path), so every vocal moment is produced, not dry.
GLITCH_BAR = 89
FREEZE_TO = 92


# v34 (ROUND TYPE: section, w5 2:11-2:43 = g5's middle, flagged 'little new vs w4'; phase distortion pinned
# f6713421): THE VINE COUNTS. The verse sings 'the slow vine knows two, then four' - so a PHASE-DISTORTION pluck (the
# CZ's square bending from a sine on every hit; the home computer's synth, new to the closer) answers the words: two
# plucks under 'two', four under 'four', and then the vine keeps DOUBLING - eight eighths the next bar, sixteen
# sixteenths the bar after - an arpeggio reaching up the bar's own chord (PLAN) and, at sixteen, curling back down.
# After both statements (68, 76). Word painting, and the tree's growth: 2, 4, 8, 16.
VINE_PATCH = {"synth": {"layers": [{"type": "pd", "pd": {"shape": "square", "amount": {
    "value": 0.1, "mod": [{"src": "env.p", "amount": 0.75}]}}}],
    "env": {"p": "1ms 1 0 140ms"}, "amp": "1ms 0.7 0 320ms", "filters": [{"kind": "lp", "cutoff": 4500, "q": 0.5}]}}


def vine():
    for bar in VERSE_AT:
        groups = [(bar, 4.75, 0.75, 2, 70), (bar, 6.8, 0.36, 4, 76), (bar + 2, 0.0, 0.5, 8, 82), (bar + 3, 0.0, 0.25, 16, 88)]
        for gb, start, step, count, vel in groups:
            root, cs = PLAN[gb]
            for i in range(count):
                j = i if count < 16 else (i if i < 8 else 15 - i)
                s = root + cs[j % 4] + EDO * (j // 4)
                part("vine").add(b0(gb) + start + i * step, min(step, 0.5) * 0.9, m(s, FS4 - 12), vel + (i % 2) * 4)


def glitch_lane():
    a = rb(GLITCH_BAR) + 2
    return [["0b", 0.0], [f"{a - 0.01:g}b", 0.0], [f"{a:g}b", 1.0], [f"{a + 1.99:g}b", 1.0], [f"{a + 2:g}b", 0.0]]


def freeze_gain_lane():
    """the frozen chord is brought up 6 dB while it hangs (measured: alone it sat under the prune), then let go"""
    a, z = rb(GLITCH_BAR) + 3.95, rb(FREEZE_TO)
    return [["0b", 0.0], [f"{a:g}b", 0.0], [f"{a + 0.25:g}b", 6.0], [f"{z:g}b", 6.0], [f"{z + 2:g}b", 0.0]]


def freeze_lane():
    a, z = rb(GLITCH_BAR) + 3.95, rb(FREEZE_TO)
    return [["0b", 0.0], [f"{a - 0.01:g}b", 0.0], [f"{a:g}b", 1.0], [f"{z - 0.01:g}b", 1.0], [f"{z:g}b", 0.0]]


# v29 (ROUND TYPE: section, w12 5:48-6:11, the light - flagged 'static'; wM's bytebeat, pinned 709cf900): THE MACHINE
# KEEPS COUNTING. After the power-down, under the breathing standby light and the memory reel, one held BYTEBEAT note
# unfolds by itself - a lullaby made of arithmetic, still running while you sleep. Formula our own:
# t*(2+(t>>13&3))|t>>5 - harmonics 2, 3, 4, 5 of one fundamental, stepping every ~0.35 s: a just major arpeggio; the
# clock (8372) sets that fundamental exactly three octaves under the light's own note (m78), so it is F# major under
# the F# light (measured: 185, 278, 370, 463 Hz). Low-passed, quiet, fading in under the reel and out with the album.
BYTE_LULL = {"about": "chirper-three: the machine counting - t*(2+(t>>13&3))|t>>5, a just arpeggio three octaves "
                      "under the standby light",
             "synth": {"layers": [{"type": "bytebeat", "bytebeat": {"formula": "t*(2+(t>>13&3))|t>>5", "clock": 8372}}],
                       "filters": ["lp cutoff=1800", "hp cutoff=120"],
                       "amp": {"a": "400ms", "d": "0s", "s": 1, "r": "2s"}}}
COUNTING = (181, 191)


def counting_notes():
    a, z = COUNTING
    return [{"at": round(warp(b0(a)), 4), "len": round(warp(b0(z)) - warp(b0(a)) - 0.1, 3), "pitch": "m78.000", "vel": 0.7}]


def counting_lane():
    a, z = rb(COUNTING[0]), rb(COUNTING[1])
    return [["0b", -80.0], [f"{a:g}b", -30.0], [f"{a + 8:g}b", 0.0], [f"{z - 12:g}b", 0.0], [f"{z - 0.5:g}b", -40.0]]


def adt_notes():
    out = []
    for n in sung_notes()[len(SING):]:
        out.append(dict(n, at=round(n["at"] + ADT[1], 4)))
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
    (59, [(0, .5, 54), (.5, .5, 52), (1, 1, 50), (2, 1, 47)]),                                      # t1 v16's line
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


# v16: THE MEMORIES PLAY BACK FROM A RECORD - the reel runs through vinyl (crackle, dust, surface noise, rumble, wow
# of 8 cents per platter turn, wear rolling off the top); a gate lane keeps the record silent outside the reel (the
# lesson of the radio in v10): the needle drops half a bar before the first memory, and in the last bar the
# crackle fades away while the standby light breathes on - the record ends, the light stays on
# v35 (ROUND TYPE: whole; orbit pinned c7606671): THE CLOSER GETS ITS FLOOR, AND THE MEMORIES CIRCLE. (1) compscore
# --bands said the closer was tilted bass-light and mid-boxy: 38-71 Hz 8-9 dB short of the album, 400 and 750-880 Hz
# 8.5 dB over. The sub up 5 dB, a 55 Hz peak on the kick, and two master cuts (400 Hz, ~810 Hz, 3 dB each). (2) In the
# light section the album flashes through its memory - one bar per track's motif, on a dulled FM piano played back
# from a record - and now each memory CIRCLES THE LISTENER as it passes (Chowning's orbit, a lap every two bars, round
# the head): the album drifting round you as you fall asleep.
MEMORY_ORBIT = {"type": "orbit", "path": "circle", "rate": round(126 / 60 / 8, 4), "radius": 3, "distance": 0}


# v36 (ROUND TYPE: whole; chaos pinned f3872739, orbit mods 206fbfb8): THE MACHINE BREAKS AND HEALS, AND THE TUNE
# FLIES IN. (1) After the glitch and the freeze (89) the prune counts in sevens over nothing: now a DUFFING chaos bass
# (wM: 'a machine coming apart - basses that fail on purpose') plays the prune's 2+2+3 downbeats on its chord roots in
# short notes (sustained chaos costs the scorer - t11 v33), its amount climbing bar by bar - locked, then period
# doubling, then breaking up - until at 103, as the band regrows, one long clean note: healed. (2) THE THEREMIN SPIRALS
# IN: at every generation's statement of the tune (9, 14, 23, 36 ... 106, 127) the theremin starts ~11 m out and
# spirals in to 1.5 m round the listener (orbit radius on a lane; Doppler 0.6, so the approach bends it a few cents
# sharp - wonky, as the chirpers are), arriving as the tune lands.
DUFF_PATCH = {"synth": {"layers": [{"type": "chaos", "chaos": {"system": "duffing", "axis": "x", "amount": {
    "value": 0.0, "mod": [{"src": "auto.dm", "amount": 1}]}}}],
    "amp": "3ms 0.9 0.6 180ms", "filters": [{"kind": "lp", "cutoff": 1200, "q": 0.6}]}}
DUFF = (90, 102)


def duffing_bass():
    for bar in range(DUFF[0], DUFF[1] + 1):
        root = PLAN[bar][0]
        for k, at in enumerate((0.0, 1.0, 2.0)):
            part("duff").add(b0(bar) + at, 0.45, m(root, FS4 - 36), 100 if k == 0 else 88)
    part("duff").add(b0(DUFF[1] + 1), 3.6, m(PLAN[DUFF[1] + 1][0], FS4 - 36), 96)      # healed


def duffing_lane():
    pts = []
    for bar in range(DUFF[0], DUFF[1] + 1):
        v = 0.05 + 0.70 * (bar - DUFF[0]) / (DUFF[1] - DUFF[0])   # v38: to 0.75 - wM's regime table: 0.6 sat in a
        #                                                      periodic window (0.4-0.625); 0.625-0.85 is chaotic
        pts.append([f"{warp(b0(bar) + 1):g}b", round(v, 3)])
    a = warp(b0(DUFF[1] + 1))
    pts += [[f"{a - 0.1:g}b", 0.75], [f"{a:g}b", 0.0]]
    return pts


# v40 (ROUND TYPE: whole; orbit 'level' pinned 8f150090 - chirper-three's request): THE TUNE FLIES IN. v36's spiral
# moved but never APPROACHED (orbit loudness was relative to the closest point); with level 1.5 m, distance is loudness
# (1/distance), so at every generation's statement the theremin starts faint ~11.5 m out (about -18 dB), spirals in and
# swells as it lands: the song keeps bringing its melody in from the distance, 9 to 129.
THEREMIN_ORBIT = {"type": "orbit", "rate": 0.3, "distance": 0, "doppler": 0.6, "level": 1.5,
                  "radius": {"value": 1.5, "mod": [{"src": "auto.sp", "amount": 10}]}}


def spiral_lane():
    """1 (far) at each theremin statement's start, 0 (near) at its end."""
    ev = sorted(e for e in P["theremin"].ev if e[3] > 1)
    groups, cur = [], [ev[0]]
    for e in ev[1:]:
        if e[0] - (cur[-1][0] + cur[-1][1]) > 8:
            groups.append(cur); cur = [e]
        else:
            cur.append(e)
    groups.append(cur)
    pts = [["0b", 1.0]]
    for gp in groups:
        a, z = warp(gp[0][0]), warp(gp[-1][0]) + gp[-1][1]      # lanes run in real beats
        pts += [[f"{max(0.0, a - 0.5):g}b", 1.0], [f"{z:g}b", 0.0], [f"{z + 2:g}b", 1.0]]
    return pts


# v37 (ROUND TYPE: section, w1 0:00-0:33, flagged static): THE MACHINE CHECKS ITS TUNING. As the closer wakes, a quiet
# hollow tone (phase-distortion square, soft) walks all 31 steps of the song's 31-EDO octave, ascending, one every two
# beats, F#4 to F#5 - arriving on the octave as bar 17 begins. A test tone; a tuning check; the album's microtones
# laid out before the song uses them; and t11 ends on a held F#, so the last song starts from where the weather left it.
TUNER_PATCH = {"synth": {"layers": [{"type": "pd", "pd": {"shape": "square", "amount": 0.2}}],
                         "amp": "40ms 0.8 0.7 600ms", "filters": [{"kind": "lp", "cutoff": 2400, "q": 0.5}]}}


TUNER_AT = 8.0
# v41 (ROUND TYPE: palette; shaper pinned 817a5de6): RISSET'S BRASS. Jean-Claude Risset's synthesised trumpet (Bell
# Labs, the 1960s) is one of computer music's founding sounds - he found that real brass gets brighter as it gets
# louder. The closer's horns (v11's waveguide lips, 37-157) and the tune's horn (139-141) become Chebyshev-shaped brass
# (Le Brun & Arfib 1979): a sine driving a polynomial that writes the brass partials, its drive (index) on a blowing
# envelope and on velocity - louder is brighter. The tutti's brass (145-147) stays the physical waveguide, so in the
# tutti the computer's brass and the modelled lips play together.
RISSET_BRASS = {"synth": {"layers": [{"type": "shaper", "shaper": {
    "harmonics": [1, 0.8, 0.6, 0.45, 0.35, 0.25, 0.18, 0.12, 0.08, 0.05],
    "index": {"value": 0.05, "mod": [{"src": "env.blow", "amount": 0.7}, {"src": "vel", "amount": 0.25}]}}}],
    "amp": "40ms 200ms 0.8 150ms", "env": {"blow": {"a": "60ms", "d": "300ms", "s": 0.7, "r": "150ms"}}}}
# v38 (ROUND TYPE: whole; lpc pinned 78e838c5): THE VOICE BREAKS WITH THE MACHINE, THEN SINGS WITH US - t4's arc
# mirrored. In the prune the spoken 'count the leaves again' (six repeats) degrades as the Duffing bass breaks up:
# repeats 1-2 human, 3-4 through LPC, 5-6 through the speaking toy (5-bit, monotone on F#); healed, in the coda the
# machine SINGS ALONG - an LPC copy of 'Moth, the warm glass holds you...' following the singer's own pitch, quiet and
# panned opposite: the computer and a person singing the album's last song together.
LPC_EARLY = 0.0                # ee46ab71 (adopted 20:21) compensates lpc in the engine: the hand nudge (0.075 beats) is out


# v39 (ROUND TYPE: section, w7 3:15-3:46 - the prune's end and the regrowth, flagged little new vs w6; w12, the
# album's last light, static and fading by design, left alone): THE FIRST PLUCKED STRING REGROWS. Karplus-Strong (1983,
# pinned 8f150090) - the first string a computer plucked - grows back with the band after the heal: a KS harp (blend 0,
# hollow, sounding an octave down) climbs arpeggios through each bar's 31-EDO chord, 103-110, its start rising an octave
# every three bars as the tree regrows - with tune: false, the 1983 hardware's whole-sample loops, so the higher it
# grows the flatter its top notes: wonky as it climbs.
KS_HARP = {"synth": {"layers": [{"type": "ks", "ks": {"blend": 0, "stretch": 2, "tune": False}, "decay": "2.5s",
                                 "bright": 0.6}], "amp": "1ms 0 1 300ms"}}
KS_AT = (103, 110)


# v42 (ROUND TYPE: section, w11 5:18-5:48 - the coda's sung line; unflagged, chosen for Harry's notes today: t10's
# 'vocal choiry section ... that is the bar', t1's 'the singing came a long way'; the flagged w12 is the album's last
# light and w1 was worked in v37): THE CHANT CHOIR. Under 'Moth, the warm glass holds you...' a four-voice FOF choir
# (fof pinned 91b04b25: Rodet's CHANT at IRCAM, 1979-84 - computer music's own classic singing voice, formant grains
# and no filters) holds each bar's 31-EDO chord, wordless: bass on the root, tenor the fifth, alto the third, soprano
# the seventh; the vowel opens from 'u' to 'a' across the coda on one lane, as a choir opens its mouth; it fades in under
# the first statement, swells under the harmonised second (168-170) and lets go as the machine's VOSIM voice speaks.
FOF_AT = (160, 170)
FOF_VOICES = (("fof_b", "bass", 0, -24, 0.1), ("fof_t", "tenor", 18, -12, 0.15),
              ("fof_a", "alto", 1, 0, 0.2), ("fof_s", "soprano", 3, 0, 0.3))   # (track, voice, tone, octave, vib)


def fof_patch(voice, vib):
    return {"synth": {"layers": [{"type": "fof", "fof": {"voice": voice, "vowel": "u>a", "attack": "3ms",
                                                          "morph": {"value": 0, "mod": [{"src": "auto.mouth", "amount": 1}]}}}],
                      "pitch": {"value": 0, "mod": [{"src": "lfo.vib", "amount": vib}, {"src": "env.scoop", "amount": -0.3}]},
                      "lfo": {"vib": {"wave": "sine", "rate": "5.5hz", "delay": "300ms", "fade": "400ms"}},
                      "env": {"scoop": {"a": "1ms", "d": "120ms", "s": 0}}, "amp": "300ms 0 1 900ms"}}


def fof_choir():
    a, z = FOF_AT
    for name, voice, tone, octave, vib in FOF_VOICES:
        for bar in range(a, z + 1):
            root, chord = PLAN[bar]
            step = root + (tone if tone >= 18 else chord[tone])
            vel = 92 if bar >= 168 else 58 + 2 * (bar - a)
            part(name).add(b0(bar), 5.5 if bar == z else 4.3, m(step, FS4 + octave), vel)


# v43 (ROUND TYPE: section, w9 4:16-4:47 - the colony, flagged static; w12, the album's last light, left alone): THE
# COLONY SINGS THE CHANGES. The Life colony's tones (v33) were four fixed pitches on F# while the chords moved under
# them. Now its rows are quality-neutral - root, fifth, octave, twelfth (0, 18, 31, 49 steps) - and a pitch lane moves
# them with each bar's 31-EDO chord root (gliding a quarter beat at the bar line): the same cells, the same life, now
# singing the harmony. (No voice, no choir, no more Karplus-Strong - Harry's 'keep things varied'.)
COLONY_SING = " ".join(m(s) for s in (0, 18, 31, 49))
COLONY_SING_PATCH = {"extends": "marimba", "synth": {"pitch": {"value": 0, "mod": [{"src": "auto.tr", "amount": 1}]}}}


def colony_root_lane():
    """Lanes on a track with 'at' count from the track's start (found here: song-time points held the first value)."""
    at = warp(b0(COLONY[0]))
    pts = []
    for bar in range(COLONY[0], COLONY[1] + 2):
        st = round(PLAN[bar][0] * 12 / EDO, 3)
        pts += [[f"{rb(bar) - at:g}b", st], [f"{rb(bar + 1) - 0.25 - at:g}b", st]]
    return pts


# v45 (ROUND TYPE: section, w2 0:33-1:06 - g2's end and the pulse arriving at g3 (22), flagged 'level jump'; w12 left
# alone; no voice, no groove copy): THE FIREFLIES LEARN THE BEAT. The seed's music box is the light. In g2 the light
# multiplies into a swarm of twelve FIREFLIES, each flashing at its own rate (tempo scattered +-18%) on its own tone of
# the bar's 31-EDO chord - a sparkle - and each pulled toward the swarm's mean phase (the KURAMOTO model, 1975: the
# maths of fireflies and pacemaker cells, integrated here note by note) with a coupling that rises through the
# critical point, while a gentle pacemaker draws the swarm onto the song's beat. By bar 22 they flash together, chord
# tones striking on every beat: the pulse is born out of synchrony; the kick takes over as they fade (to 25).
FIREFLY = (14, 22, 26)          # swarm from, locked by, gone by
FIREFLY_N = 12


def fireflies():
    rnd = random.Random(31)                         # its own generator: the shared draws stay as they were
    a, lock, z = FIREFLY
    omega = [2 * math.pi * (1 + 0.18 * (2 * rnd.random() - 1)) for _ in range(FIREFLY_N)]
    theta = [2 * math.pi * rnd.random() for _ in range(FIREFLY_N)]
    t0, t1, tl = b0(a), b0(z), b0(lock)
    dt = 1 / 64
    t = t0
    while t < t1:
        ramp = min(1.0, (t - t0) / (tl - 2 - t0)) ** 1.5          # the pull creeps up; full two beats before the lock
        k, f = 1.6 * ramp, 1.5 * ramp                               # the pacemaker just beats the widest detune (1.13)
        cx = sum(math.cos(x) for x in theta) / FIREFLY_N
        sy = sum(math.sin(x) for x in theta) / FIREFLY_N
        r, psi = math.hypot(cx, sy), math.atan2(sy, cx)
        beat = 2 * math.pi * (t - t0)                               # the pacemaker: one cycle a beat, on the grid
        bar = int(a + (t - t0) // BAR)
        root, chord = PLAN[bar]
        fade = 1.0 if t < tl else max(0.0, 1 - (t - tl) / (t1 - tl))
        for i in range(FIREFLY_N):
            d = omega[i] + k * r * math.sin(psi - theta[i]) + f * math.sin(beat - theta[i])
            new = theta[i] + d * dt
            if math.floor(new / (2 * math.pi)) > math.floor(theta[i] / (2 * math.pi)):
                step = root + chord[i % 4] + EDO * (1 + i // 8) - (EDO if i % 8 >= 4 else 0)
                vel = (38 + 46 * r) * fade
                if vel > 8:
                    part("fireflies").add(round(t, 4), 0.2, m(step), vel)
            theta[i] = new
        t += dt


# v46 (ROUND TYPE: section, w5 2:11-2:43 - g5's middle, still 'little new vs w4' after v44's refused cajon; no voice,
# and nothing ADDED - v44 showed added percussion pulls the closer toward t11): THE BAND BREATHES. Between the two verse
# statements (72-75) the drums fall into HALF TIME - the kick once a bar, the clap only on four, the ride in half notes,
# the hats on the straight offbeats (the swung ones fall silent) - silenced at velocity 1, so every track keeps its
# notes and its randomness. g5's middle gets a shape of its own: a held breath under the tape choir's swell, the verse
# returning at 76 over the full beat.
HALF = (72, 75)
HALF_KEEP = {"kick": (0.0,), "clap": (3.02,), "ride": (0.0, 2.0), "hats": (0.5, 1.5, 2.5, 3.5)}


def half_time():
    a, z = HALF
    for name, keep in HALF_KEEP.items():
        ev = []
        for at, ln, head, vel in P[name].ev:
            bar = int(at // BAR) + 1
            if a <= bar <= z and not any(abs((at - b0(bar)) - k) < 0.02 for k in keep):
                vel = 1
            ev.append((at, ln, head, vel))
        P[name].ev = ev


# v48 (ROUND TYPE: whole): THE LAST NOTE HOLDS EVERYTHING. The closer ends where the seed began - one F# again (the
# light, 179-190). Now under it a held F#3 on RISSET'S HARMONIC ARPEGGIO (risset-arpeggio: five near-unison copies of
# a ten-harmonic tone, each a hair apart, so harmonic k beats k times as fast - Mutations, 1969): the one note slowly
# arpeggiates its own overtones, a melody nobody plays, out of the single tone the album ends on. Everything the engine
# can do, folded back into one note that turns out to contain a song.
LAST_NOTE = (179, 190)


def last_note():
    a, z = LAST_NOTE
    part("lastnote").add(b0(a), b0(z + 1) - b0(a), m(-EDO), 72)


# v50 (ROUND TYPE: whole): THE HEART IS A MODELLED DRUM. machine-kit's kick - a 909 circuit - is played in exactly
# t10, t11 and t12 (eco's kit-voice palette): the album's last three songs share one pulse. The closer's kick is now a
# SIMULATED BASS DRUM (the engine's physical drum, chirper-two's kick from metal-kit-phys with a longer body): a plastic
# beater whose contact shortens as it is struck harder, a membrane ringing at the Bessel zeros, a resonant head coupled
# to it through the air in the shell, the pitch falling as the head's tension relaxes - the 909's swept punch, but
# derived from physics instead of drawn as an envelope. Physical modelling: the machine computing the real thing from
# its equations, the other great dream of computer music. Only k changes; the rest of machine-kit stays.
PHYS_K = {"patch": {"synth": {"layers": [{"type": "drum", "beater": "plastic", "decay": "0.6s", "sharp": 90, "reso": 1.06, "cavity": 0.25, "reso_level": 0.35, "air": 0.5, "strike": 0.08, "damp": 0.6, "shell": 0.1, "contact": 1.4, "slap": 0.45}], "filters": [{"kind": "peak", "cutoff": {"value": "4.2k", "mod": [{"src": "rand", "amount": 0.1}]}, "q": 1, "gain": {"value": "3dB", "mod": [{"src": "vel", "amount": 5}]}}, "lowshelf cutoff=75 gain=4dB"], "amp": {"a": "0.2ms", "d": "520ms", "s": 0, "r": "25ms", "curve": 1.5}, "drive": 0.35}, "play": {"vel_sens": 0.45}}, "pitch": "G1"}
T12_KIT = {"extends": "machine-kit", "kit": {"k": PHYS_K}}


def ks_harp():
    for bar in range(KS_AT[0], KS_AT[1] + 1):
        root, chord = PLAN[bar]
        lift = 31 * ((bar - KS_AT[0]) // 3)
        tones = [root + c + 31 * o + lift for o in (0, 1) for c in chord]
        for k, st in enumerate(tones):
            part("ksharp").add(b0(bar) + k * 0.5, 1.5, m(st, FS4), 88 if k == 0 else 72 + k * 2)


def lpc_voices(song):
    tracks = {tk["name"]: tk for tk in song["tracks"]}
    out = []
    voice = tracks["voice"]
    per = len(voice["notes"]) // 6
    for name, reps, fx, gain in (("voice_chip", (2, 3), "lpc", "-14dB"),        # lpc on voice-tts came out ~14 dB
                                 ("voice_toy", (4, 5), "lpc pitch=F#2 bits=5", "-19.5dB")):   # hot: matched solo
        notes = []
        for i, n in enumerate(voice["notes"]):
            if i // per in reps:
                c = dict(n)
                c["at"] = round(float(str(n["at"]).rstrip("b")) - LPC_EARLY, 4)
                notes.append(c)
        out.append({"name": name, "patch": voice["patch"], "gain": gain, "pan": voice.get("pan", 0),
                    "sends": voice.get("sends", {}), "fx": [fx] + list(voice.get("fx") or []), "notes": notes})
    for i, n in enumerate(voice["notes"]):                       # the human take is silent where the chip speaks
        if i // per >= 2:
            n["vel"] = 0.01
    singer = tracks["singer"]
    sc = []
    for n in singer["notes"]:
        c = dict(n)
        c["at"] = round(float(str(n["at"]).rstrip("b")) - LPC_EARLY, 4)
        sc.append(c)
    out.append({"name": "singer_chip", "patch": singer["patch"], "gain": "-22dB", "pan": -0.35,   # ~8 dB under
                "sends": singer.get("sends", {}), "fx": ["lpc"] + list(singer.get("fx") or []), "notes": sc})
    song["tracks"] += out


def tuner():
    step = (62.0 - TUNER_AT) / EDO                # the machine wakes first: the join with t11 (3 s) stays t11's room
    for k in range(EDO + 1):
        part("tuner").add(TUNER_AT + step * k, step * 1.1 if k < EDO else 6.0, m(k), 44 + int(30 * k / EDO))


def vinyl_gate():
    return [["0b", -80.0], [f"{rb(179) - 2.5:g}b", -80.0], [f"{rb(179) - 2:g}b", 0.0], [f"{rb(190):g}b", 0.0],
            [f"{rb(190) + 3:g}b", -80.0]]


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


# v15: A GONG MARKS THE CUT AND THE COMPLETION - one stroke as the pruning begins (bar 90) and one as the growing ends
# (the coda, bar 158), on the modal layer's gong (a dense low plate set, its high modes blooming in after the hit)
GONG = {"synth": {"layers": [{"type": "modal", "modes": "gong", "decay": "10s", "damp": 0.02, "bloom": 0.7,
                              "strike": 0.35, "tilt": -0.5}],
                  "amp": {"a": "2ms", "d": "12s", "s": 0, "r": "5s", "curve": 3}}}


def gong():
    part("gong").add(b0(90), 15.0, "m42.000", 108)
    part("gong").add(b0(158), 15.0, "m42.000", 120)


# v22 (ROUND TYPE: whole): THE TUNE GROWS LIKE THE TREE ('a tune good to hear', Harry on t1) - the closer's tune, the
# coda line, was first heard 5 minutes in. Now at the start of each generation, as the tower's last toll sounds, a
# THEREMIN (the earliest electronic instrument; unused on the album) plays the beginning of the coda melody - and each
# generation adds notes in the tree's own Fibonacci counts: g1 1, g2 2, g3 3, g4 5, g5 8, g6 13 (stated again
# mid-g6) - until the coda, where the voice sings all 15 with its words: planted early, it blossoms when sung.
# Each fragment follows the chord root at its bar (relative to the coda's), folded within +-6 semitones; the song's
# 31-EDO tuning snaps it. Its own part and track, listed last.
TUNE_GROWTH = {"g1": 1, "g2": 2, "g3": 3, "g4": 5, "g5": 8, "g6": 13}


# v24 (ROUND TYPE: whole; Harry 'do more each round'): THE TUNE PASSES HAND TO HAND TO THE VOICE - after the theremin
# states the grown tune on the band's return (127), a solo CELLO takes it an octave down (131), then a FRENCH HORN
# (139; unused on the album), then the brass chorale (150) and at last the singer, with its words (158): a relay that
# builds the last minute and a half toward the voice. And the tape choir (v23) now SWELLS ~8 dB across its sixteen
# bars of g5 instead of holding one level.
RELAY = (("tunecello", 131, -12), ("tunehorn", 139, -12))
# v26 (ROUND TYPE: whole; Harry 'do more each round'): A CLIMAX AND A RELEASE for the 4:16-5:18 plateau (the map:
# w9 static, w10 little new). (1) TUTTI: the relay's last step before the brass chorale is the WHOLE ORCHESTRA - a
# physical violin section at pitch, a brass section an octave down, a cello section two down - playing the grown tune
# at once (145), 'everything at once, and still a song'. (2) THE CODA DROPS TO HALF-TIME (from 158): kick on 1 and
# the 'and' of 3, the snare on 3 only - the heart slows toward standby and the singer gets room.
TUTTI = (145, (("tutti_vn", 0), ("tutti_br", -12), ("tutti_vc", -24)))
HALF_FROM = 168            # the whole coda in half-time cost the spectrum term 4 points (thin drums for 21 bars)


def relay():
    t0 = SING[0][0]
    for name, bar, octv in RELAY + tuple((n, TUTTI[0], o) for n, o in TUTTI[1]):
        shift = (PLAN[bar][0] - PLAN[158][0]) * 12 / EDO
        shift = ((shift + 6) % 12) - 6
        for at, ln, ph, midi, vel, f0 in SING[:TUNE_GROWTH["g6"]]:
            part(name).add(b0(bar) + at - t0, ln * 0.95, f"m{midi + shift + octv:.3f}", 92)


def tune_grows():
    t0 = SING[0][0]
    starts = []
    for name, a, z in SECTIONS:
        if name in TUNE_GROWTH:
            starts.append((a, b0(a) + 2 * GEN[name] - 1, TUNE_GROWTH[name]))
    starts.append((CLEARING[1], b0(CLEARING[1]), TUNE_GROWTH["g6"]))   # v23: rides the band's return
    for bar, at0, k in starts:
        shift = (PLAN[bar][0] - PLAN[158][0]) * 12 / EDO
        shift = ((shift + 6) % 12) - 6
        for at, ln, ph, midi, vel, f0 in SING[:k]:
            part("theremin").add(at0 + at - t0, ln * 0.95, f"m{midi + shift:.3f}", 84)


# v23 (ROUND TYPE: whole; Harry 17:05 'do more each round'): TWO MOVES. (1) A CLEARING IN THE FOREST - g6 grew for
# 55 bars without a dynamic shape; now for eight bars mid-way (119-126) the drums and both basses drop out (silenced
# at velocity 1, held notes cut - every track keeps its note count and its randomness) and only the strings, the
# Farfisa's growing arpeggio and the opening filter remain; at 127 the band returns with a crash and the theremin's
# mid-g6 statement of the tune (moved from 130) rides the return. (2) THE VOICES ON TAPE - a Mellotron choir (a
# 1960s machine that played back recorded human voices; unused on the album) sings the L-system's chords, wordless,
# under g5's middle (64-79), foreshadowing the coda's real choir. New parts on new tracks, listed last.
CLEARING = (119, 127)
TAPE_CHOIR = (64, 79)


def clearing():
    a, z = b0(CLEARING[0]), b0(CLEARING[1])
    for name in ("kick", "hats", "clap", "ride", "sub", "phantom"):
        ev = []
        for s, ln, head, vel in P[name].ev:
            if a <= s < z:
                ev.append((s, ln, head, 1))
            elif s < a < s + ln:
                ev.append((s, a - s - 0.02, head, vel))
            else:
                ev.append((s, ln, head, vel))
        P[name].ev = ev
    part("crash12").add(z, 4.0, "cy", 112)


# v30 (ROUND TYPE: whole; g6's middle flagged static / little new, w9-w10; wM's systems pinned ade7b930): THE DRUMMER
# BECOMES A COLONY. From bar 132 to the tutti (145) the regular kit steps aside and the SAME kit plays CONWAY'S GAME OF
# LIFE (the engine's life gen): a 16 x 4 torus, one bar of sixteenths per generation, rows bottom-up kick, rim, clap,
# hat - so the groove mutates by the rules of life itself, a bar at a time, until the band's tutti brings the drummer
# back. The start was chosen by simulating B3/S23 here: it lives all 13 generations without repeating a state, keeps
# a kick on every downbeat, and grows from a kick roll into clusters that drift across the bar.
COLONY = (132, 145)        # v36: the gens' 'at' now warp()ed - b0 left them 6.5 beats (the prune's lost eighths) late
COLONY_INIT = "0001110101001001/0110010000111011/0001101000000011/1111101010000100"


# v33 (ROUND TYPE: section, w9 4:16-4:47 = the colony, still flagged static - the colony moved the rhythm, nothing
# pitched moved with it): THE COLONY SINGS. A second life gen with the SAME torus, rule and start reads the same cells
# bar by bar, so it lands exactly on the colony's hits - its four rows playing the closer's home chord, the harmonic
# seventh on F# (4:5:6:7 - F#, A#, C#, the septimal E; 31-EDO holds them): the kick row is the root, the hat row the
# seventh. On marimba. Life plays the rhythm and the harmony at once.
COLONY_TONES = "m66 m69.863 m73.02 m75.688"


def colony():
    a, z = b0(COLONY[0]), b0(COLONY[1])
    for name in ("kick", "hats", "clap", "ride"):
        P[name].ev = [(s, ln, head, 1 if a <= s < z else vel) for s, ln, head, vel in P[name].ev]


# v31 (ROUND TYPE: whole; VOSIM pinned 1a5a0572): THE MACHINE LEARNS THE SONG. After the voice's second coda
# statement, the computer's own early voice sings the tune back: VOSIM (voice-simulation pulse trains, Sonology 1978),
# two formant layers making vowels - and each note's vowel is taken from the PHONEME the human sang on it (AO, AE, OW,
# UW, ER, IY...), so the machine imitates the words in its own vowels, without consonants; diphthongs glide (expr_end).
# An octave down, steady, unhumanised - a machine singing a song it has just learnt - then the power-down.
MACHINE_AT = 172
VOWELS = {"AA": (730, 1090), "AO": (570, 840), "AH": (640, 1190), "AE": (660, 1720), "OW": (500, 900),
          "UW": (300, 870), "ER": (490, 1350), "IH": (390, 1990), "IY": (270, 2290), "EH": (530, 1840),
          "UH": (440, 1020), "EY": (530, 1840), "AY": (730, 1090), "AW": (730, 1090), "OY": (570, 840)}
GLIDES = {"OW": (300, 870), "EY": (270, 2290), "AY": (270, 2290), "AW": (300, 870), "OY": (270, 2290)}
MACHINE_VOICE = {"synth": {"layers": [
    {"type": "vosim", "vosim": {"formant": {"value": 500, "mod": [{"src": "expr.v1", "amount": 1}]}, "pulses": 3, "decay": 0.7}},
    {"type": "vosim", "level": 0.5, "vosim": {"formant": {"value": 1500, "mod": [{"src": "expr.v2", "amount": 1}]},
                                               "pulses": 4, "decay": 0.75}}],
    "amp": "40ms 0.9 0.85 300ms"}}


def machine_notes():
    out = []
    for a, ln, ph, midi, v, f0 in SING:
        vow = next(x.rstrip("012") for x in ph.split() if x[-1] in "012")
        f1, f2 = VOWELS["AH"] if vow == "AH" and "AH0" in ph else VOWELS[vow]
        if "AH0" in ph:
            f1, f2 = 500, 1500                                 # the unstressed schwa
        n = {"at": round(warp(b0(MACHINE_AT) + a), 4), "len": round(ln, 3), "pitch": f"m{midi - 12}", "vel": 0.8,
             "expr": {"v1": round(math.log2(f1 / 500), 3), "v2": round(math.log2(f2 / 1500), 3)}}
        if vow in GLIDES:
            g1, g2 = GLIDES[vow]
            n["expr_end"] = {"v1": round(math.log2(g1 / 500), 3), "v2": round(math.log2(g2 / 1500), 3)}
        out.append(n)
    return out


CLEAR_TRACKS = ("turtle", "harp", "kalimba", "celesta", "violins_lead", "strum", "horns", "ondes")


def clear_lanes(song):
    """v23: the clearing also takes out g6's melodic layers (written by generators, not Parts) with a gain lane each:
    -60 dB through bars 119-126, ramped over half a beat - no note is added or removed."""
    a, z = rb(CLEARING[0]), rb(CLEARING[1])
    pts = [["0b", 0.0], [f"{a:g}b", 0.0], [f"{a + 0.5:g}b", -60.0], [f"{z - 0.5:g}b", -60.0], [f"{z:g}b", 0.0]]
    for trk in song["tracks"]:
        if trk.get("name") in CLEAR_TRACKS:
            trk["fx"] = list(trk.get("fx") or []) + [{"type": "gain", "gain": {"value": "0dB",
                                                       "mod": [{"src": "auto.clr", "amount": 1}]}}]
            trk["auto"] = dict(trk.get("auto") or {}, clr={"points": pts})


# v32 (ROUND TYPE: section, w7 3:15-3:46 = the prune's end and g6's entrance, flagged 'little new vs w6': at 103 the
# whole band returned in one bar, as g5 had been): REGROWTH AFTER THE PRUNE. (1) The band regrows LAYER BY LAYER, as a
# tree from a cut - kick, sub and hats at 103, then harp and phantom, celesta, ondes and violins, the analog ladder and
# ride, clap and strum, and the lead violins and horns last at 109 - gain lanes (auto.rg), no note added or removed.
# (2) SAP RISING: under the regrowth one long WAVE TERRAIN note from bar 99 glides up an octave (expr.bend) as its orbit
# widens (expr.op: rx/ry 0.25 -> 0.85), so the tone opens as the tree fills - reshaped, not filtered.
REGROW = {"harp": 104, "phantom": 104, "celesta": 105, "ondes": 106, "violins": 106, "analog": 107, "ride": 107,
          "clap": 108, "strum": 108, "violins_lead": 109, "horns": 109}
SAP = (99, 111)
SAP_PATCH = {"synth": {"layers": [{"type": "terrain", "terrain": {
    "surface": "sines", "ratio": 1.002, "k": 1.1, "cx": 0.05,
    "rx": {"value": 0.25, "mod": [{"src": "expr.op", "amount": 0.6}]},
    "ry": {"value": 0.25, "mod": [{"src": "expr.op", "amount": 0.5}]}}}],
    "pitch": {"value": 0, "mod": [{"src": "expr.bend", "amount": 1}]},
    "amp": "3s 1 1 1.5s"}}


def regrow_lanes(song):
    for trk in song["tracks"]:
        at = REGROW.get(trk.get("name"))
        if at is None:
            continue
        a, z = rb(102), rb(at)
        pts = [["0b", 0.0], [f"{a:g}b", 0.0], [f"{a + 0.5:g}b", -60.0], [f"{z - 0.25:g}b", -60.0], [f"{z:g}b", 0.0]]
        trk["fx"] = list(trk.get("fx") or []) + [{"type": "gain", "gain": {"value": "0dB",
                                                   "mod": [{"src": "auto.rg", "amount": 1}]}}]
        trk["auto"] = dict(trk.get("auto") or {}, rg={"points": pts})


def sap_notes():
    a, z = warp(b0(SAP[0])), warp(b0(SAP[1]))
    return [{"at": round(a, 4), "len": round(z - a, 4), "pitch": "m54", "vel": 0.8,
             "expr": {"bend": 0.0, "op": 0.0}, "expr_end": {"bend": 12.0, "op": 1.0}}]


def tape_choir():
    for bar in range(TAPE_CHOIR[0], TAPE_CHOIR[1] + 1):
        root, q = PLAN[bar]
        part("tapechoir").add(b0(bar), BAR - 0.1, chord(66 + root * 12 / EDO, q[1:]), 70)   # up an octave


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
    clearing()                                    # v23: a clearing in the forest (g6), once every part is written
    colony()                                      # v30: the drummer becomes a colony
    vine()                                        # v34: the vine counts
    duffing_bass()                                # v36: the machine breaks and heals
    tuner()                                       # v37: the machine checks its tuning
    ks_harp()                                     # v39: the first plucked string regrows
    fof_choir()                                   # v42: the CHANT choir
    fireflies()                                   # v45: the fireflies learn the beat
    half_time()                                   # v46: the band breathes
    last_note()                                   # v48: the last note holds everything
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
            tr("gong", GONG, gain="-9dB", sends={"hall": "-8dB"}),                         # v15: the gong
            tr("tower", TOWER_BELL, gain="-8dB", pan=-0.2, sends={"hall": "-6dB"}),      # v12: the bell tower
            tr("memory", "dx-epiano", gain="-10dB", pan=0.2, sends={"hall": "-6dB"},
               fx=[{"type": "filter", "kind": "lp", "cutoff": 3000}, "chorus",     # v10 (a radio's hiss ran all song)
                   {"type": "vinyl", "crackle": 0.35, "dust": 0.3, "noise": "-56dB", "rumble": 0.2, "warp": 8,
                    "wear": 0.45},                                                  # v16: played back from a record
                   {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.vg", "amount": 1}]}},
                   MEMORY_ORBIT],                                                   # v35: the memories circle
               auto={"vg": {"points": vinyl_gate()}}),
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
            {"name": "singer", "patch": SING_PATCH, "gain": "-12dB", "pan": -0.05, "sends": {"hall": "-5dB", "echo": "-12dB"},
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
            tr("analog", "farfisa", gain="-2dB", pan=-0.15, sends={"hall": "-10dB"},
               fx=[{"type": "filter", "kind": "ladder", "q": 1.0,
                    "cutoff": {"value": 250, "mod": [{"src": "auto.lc", "amount": 1}]}}],
               auto={"lc": {"points": ladder_lane()}}),                                          # v19: the ladder
            tr("cellos", "cellos", gain="-14dB", pan=-0.25, sends={"hall": "-8dB"},
               fx=[{"type": "filter", "kind": "hp", "cutoff": 120}]),
            tr("violins", "violins", gain="-14dB", pan=0.3, sends={"hall": "-6dB"}),
            tr("violins_lead", {"extends": "violins", "synth": {"pitch": {"value": 0, "mod": [
                {"src": "expr.f0", "amount": 0.01}]}}}, gain="-12dB", pan=0.35, sends={"hall": "-6dB"}),
                # v7: BENDS - each note scoops up from one 31-EDO step below (an expr_path on the pitch, in cents)
            tr("strum", "harp play.strum=55ms", gain="-9dB", pan=-0.3, sends={"hall": "-6dB"}),     # v7: strummed chords
            tr("pole", "strings", gain="-10dB", sends={"hall": "-4dB"}, fx=["barberpole cycle=2bar down=true"]),
            tr("horns", RISSET_BRASS, gain="-13dB", pan=0.1, sends={"hall": "-8dB"}),   # v41: Risset's brass (+3 dB hot)   # v11: REAL lips - a waveguide bore, 3 players
            tr("phantom", "phantom-bass", gain="-8dB"),
            tr("sub", "808", gain="-11dB", fx=[{"type": "phantom", "harmonics": "-6dB", "odd": 0.4, "remove": 0.0}]),
            tr("kick", T12_KIT, gain="-11dB",
               fx=[{"type": "filter", "kind": "peak", "cutoff": 47, "q": 0.9, "gain": "7dB"}]),   # v35: the floor; v50: lower and deeper for the drum
            tr("ride", "machine-kit", gain="-9dB", pan=-0.3, sends={"room": "-12dB"}),     # v2
            # v21 (palette round): THE OLD MACHINE VOICE LEARNS TO SING - the prune's 'count the leaves again' (spoken six
            # times, melting from speech into song) was voice-speech, a staple in nine of the album's songs; now the
            # library's voice-tts, a 1990s desktop text-to-speech voice (flat, bright, steady, no vibrato): the far
            # future remembering the first voices computers had, through a voice and not a quote. The coda's singer and
            # choir stay humanised.
            {"name": "voice", "patch": "voice-tts", "gain": "-9dB", "pan": 0.05, "sends": {"hall": "-6dB"},
             "fx": [{"type": "filter", "kind": "hp", "cutoff": 180}], "notes": voice_notes()},   # v2: speech to song
            tr("hats", "machine-kit play.humanize.drunk=5ms play.humanize.swing_drift=0.04", gain="-1dB", pan=0.15,
               warp=[{"over": f"{b0(60):.0f}b", "to": 0}, {"over": "8bar", "to": 0.25}, {"over": "8bar", "to": 0,
                                                                                         "curve": "smooth"}]),
            tr("clap", "machine-kit play.humanize.nudge.cp=10ms", gain="-6dB", sends={"room": "-8dB"}),
            tr("shepup", "shepard-pad", gain="-16dB", sends={"hall": "-10dB"}),
            tr("shepdown", "shepard-fall", gain="-16dB", sends={"hall": "-10dB"}),
            {"name": "rush", "patch": "machine-kit", "gain": "-8dB", "pan": -0.2, "at": f"{rb(158):g}b",
             "risset": {"cycle": "4bar", "layers": 3, "length": "20bar"}, "sends": {"room": "-12dB"}, "score": RUSH},
            tr("tapechoir", "mellotron-choir", gain="-12dB", pan=-0.2, sends={"hall": "-6dB"},
               fx=[{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.sw", "amount": 1}]}}],
               auto={"sw": {"points": [["0b", -4.0], [f"{rb(TAPE_CHOIR[0]):g}b", -4.0],
                                       [f"{rb(TAPE_CHOIR[1] + 1):g}b", 4.0]]}}),               # v23: LAST; v24 swells
            tr("crash12", "machine-kit", gain="-8dB", sends={"hall": "-10dB"}),                     # v23
            tr("tunecello", "cello", gain="-3dB", pan=-0.3, sends={"hall": "-8dB"}),               # v24
            tr("tunehorn", RISSET_BRASS, gain="-4dB", pan=0.3, sends={"hall": "-8dB"}),           # v41: Risset                  # v24
            tr("tutti_vn", "violins", gain="-3dB", pan=-0.3, sends={"hall": "-6dB"}),               # v26: tutti
            tr("tutti_br", "brass", gain="-5dB", pan=0.15, sends={"hall": "-8dB"}),                 # v26
            tr("tutti_vc", "cellos", gain="-3dB", pan=0.35, sends={"hall": "-8dB"}),                # v26
            tr("theremin", "theremin", gain="-2dB", pan=0.2, sends={"hall": "-8dB"},   # v40: +3 dB, lands where it did
               fx=[THEREMIN_ORBIT], auto={"sp": {"points": spiral_lane()}}),                   # v22: LAST; v36: spirals in
        ],
        "buses": {"room": {"fx": ["reverb kind=room decay=1.0s mix=1 predelay=10ms", "hp cutoff=250"]},
                  "hall": {"fx": [{"type": "reverb", "kind": "hall", "decay": "3.2s", "mix": 1, "predelay": "30ms",
                                   "freeze": {"value": 0, "mod": [{"src": "auto.fz", "amount": 1}]}},   # v28: the freeze
                                  "hp cutoff=250",
                                  {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.fg", "amount": 1}]}}],
                           "auto": {"fz": {"points": freeze_lane()}, "fg": {"points": freeze_gain_lane()}}},
                  "echo": {"fx": [{"type": "delay", "time": "3/16", "feedback": 0.38, "mix": 1, "tone": 2800},
                                  "hp cutoff=300"]}},                                 # v28: a tape-ish echo for the voices
        "master": {"fx": [{"type": "stutter", "slice": "1/16", "repeats": 4, "roll": 0.6, "pitch": 1.0, "seed": 3,
                           "chance": {"value": 0, "mod": [{"src": "auto.st", "amount": 1}]}},           # v28: the glitch
                          {"type": "tapestop", "time": "0.01b", "curve": 1.6, "mix": 1, "up": WAKE_UP,   # v25: power up
                           "stop": {"value": 0, "mod": [{"src": "auto.tu", "amount": 1}]}},
                          {"type": "tapestop", "time": "4b", "curve": 1.6, "mix": 1,          # v14: power down
                           "stop": {"value": 0, "mod": [{"src": "auto.ts", "amount": 1}]}},
                          {"type": "eq", "bands": ["highpass cutoff=28", "peak cutoff=300 q=0.8 gain=-5dB",
                                                    "peak cutoff=400 q=1.0 gain=-3dB", "peak cutoff=810 q=0.8 gain=-3dB",
                                                    "highshelf cutoff=6000 gain=5dB"]},     # v2: the album's envelope
                          {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                          {"type": "compressor", "threshold": "-12dB", "ratio": 8, "attack": "0.3ms",
                           "release": "60ms", "makeup": "0dB"}],
                   "auto": {"dyn": {"points": lanes()},
                            # v14: POWER DOWN TO STANDBY - through the coda's last bar the whole band winds down like a
                            # motor losing power (tapestop, curve 1.6), then the light section starts on the live signal
                            "st": {"points": glitch_lane()},                                   # v28: the glitch
                            "tu": {"points": [["0b", 1.0], ["0.01b", 1.0], ["0.02b", 0.0]]},   # v25: wake
                            "ts": {"points": [["0b", 0.0], [f"{rb(178) - 0.01:g}b", 0.0], [f"{rb(178):g}b", 1.0],
                                              [f"{rb(179) - 0.01:g}b", 1.0], [f"{rb(179):g}b", 0.0]]}}},
    }
    clear_lanes(song)                             # v23: the clearing's gain lanes on the melodic layers
    regrow_lanes(song)                            # v32: the band regrows after the prune
    song["event_stable"] = True                   # v25: each note's draws from its track, beat and pitch (wM f5283535)
    song["tracks"].append({"name": "singer2", "patch": SING_PATCH, "gain": "-14dB", "pan": 0.3, "transpose": ADT[0],
                           "sends": {"hall": "-5dB", "echo": "-14dB"}, "fx": [{"type": "filter", "kind": "hp", "cutoff": 160}],
                           "notes": adt_notes()})                               # v25: the voice doubled
    song["tracks"].append({"name": "verse", "patch": SING_PATCH, "gain": "-12dB", "pan": 0.05,
                           "sends": {"hall": "-5dB", "echo": "-12dB"}, "fx": [{"type": "filter", "kind": "hp", "cutoff": 160}],
                           "notes": verse_notes()})                             # v27: the voice grows with the tune
    song["tracks"].append({"name": "counting", "patch": BYTE_LULL, "gain": "-22dB", "pan": -0.1,
                           "sends": {"hall": "-10dB"}, "auto": {"cg": {"points": counting_lane()}},
                           "fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.cg", "amount": 1}]}}],
                           "notes": counting_notes()})                          # v29: the machine keeps counting
    song["tracks"].append({"name": "machine", "patch": MACHINE_VOICE, "gain": "-14dB", "pan": -0.15,
                           "sends": {"echo": "-8dB", "hall": "-8dB"}, "notes": machine_notes()})   # v31: the machine sings
    song["tracks"].append({"name": "colony", "patch": T12_KIT, "gain": "-11dB", "at": f"{warp(b0(COLONY[0])):g}b",
                           "gen": {"type": "life", "width": 16, "height": 4, "init": COLONY_INIT, "poly": 3,
                                   "n": 16 * (COLONY[1] - COLONY[0]), "len": "/16", "notes": "k rs cp h"}})  # v30
    song["tracks"].append({"name": "sap", "patch": SAP_PATCH, "gain": "-16dB", "pan": 0.1,
                           "sends": {"hall": "-8dB"}, "notes": sap_notes()})            # v32: sap rising
    song["tracks"].append({"name": "colony_tones", "patch": COLONY_SING_PATCH, "gain": "-16dB", "pan": 0.25,   # v43
                           "auto": {"tr": {"points": colony_root_lane()}},
                           "sends": {"hall": "-12dB"}, "at": f"{warp(b0(COLONY[0])):g}b",
                           "gen": {"type": "life", "width": 16, "height": 4, "init": COLONY_INIT, "poly": 3,
                                   "n": 16 * (COLONY[1] - COLONY[0]), "len": "/16", "notes": COLONY_SING}})  # v33; v43
    song["tracks"].append({"name": "vine", "patch": VINE_PATCH, "gain": "-15dB", "pan": 0.2,
                           "sends": {"echo": "-12dB", "hall": "-12dB"}, "score": part("vine").score()})  # v34
    song["tracks"].append({"name": "duff", "patch": DUFF_PATCH, "gain": "-12dB", "pan": -0.1,
                           "sends": {"room": "-12dB"}, "score": part("duff").score(),
                           "auto": {"dm": {"points": duffing_lane()}}})                            # v36: listed last
    song["tracks"].append({"name": "tuner", "patch": TUNER_PATCH, "gain": "-30dB", "pan": 0.25,
                           "sends": {"hall": "-8dB"}, "score": part("tuner").score()})            # v37: listed last
    lpc_voices(song)                                                                           # v38: listed last
    song["tracks"].append({"name": "ksharp", "patch": KS_HARP, "gain": "-10dB", "pan": 0.3,
                           "sends": {"hall": "-10dB"}, "score": part("ksharp").score()})          # v39: listed last
    mouth = {"mouth": {"points": [[f"{rb(FOF_AT[0]):g}b", 0.0], [f"{rb(FOF_AT[1] + 1):g}b", 1.0]]}}
    for (name, voice, tone, octave, vib), gain, pan in zip(FOF_VOICES, ("-18dB", "-19dB", "-18dB", "-17dB"),
                                                           (-0.1, 0.25, -0.25, 0.1)):
        song["tracks"].append({"name": name, "patch": fof_patch(voice, vib), "gain": gain, "pan": pan,
                               "sends": {"hall": "-6dB"}, "auto": mouth, "score": part(name).score()})   # v42: listed last
    song["tracks"].append({"name": "fireflies", "patch": "music-box", "gain": "-17dB", "pan": 0.15,
                           "sends": {"hall": "-8dB"}, "score": part("fireflies").score()})       # v45: listed last
    song["tracks"].append({"name": "lastnote", "patch": "risset-arpeggio", "gain": "-21dB", "pan": 0.0,
                           "sends": {"hall": "-8dB"}, "score": part("lastnote").score()})        # v48: listed last
    with open(OUT, "w") as f:
        json.dump(song, f, indent=1)
    print("wrote", OUT, "bars", BARS, "gens", {g: len(lsys(g)) for g in range(7)})


if __name__ == "__main__":
    main()
