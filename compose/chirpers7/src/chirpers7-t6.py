#!/usr/bin/env python3
"""Chirpers - The Endless Stair (Chirpers VII), track 6: NOBODY PLAYS THE BASS (chirper-three).

DEEP, HEAVY HOUSE, F# minor (11A), 120 -> 120.5 bpm inside the track (the tape's tempo path). Featured illusion:
THE MISSING FUNDAMENTAL. The bass line is played by nobody: only its 2nd-6th harmonics sound (the `phantom-bass`
patch) and the ear supplies the low note that isn't on the speaker.
- THE SEAM IS THE ILLUSION: t6 enters under t5's outro, where t5's real 808 holds F#1, with its phantom bass on the same
  F#; as the crossfade takes t5's sub away, the bass goes on being heard.
- Lower than possible (bars 57-80): the phantom line drops an octave, to notes (C#1, A0) no speaker in a club plays.
- THE BASS TAKEN APART (the break): five pure partials (exactly 2..6 x F#1) enter one by one, staggered and spread
  across the field, and are heard as separate tones (a bright chord); then they gather to the centre and start playing
  in one rhythm together - common onset fuses them - and the low F# they imply appears in the ear.
- The drop brings THE REAL SUB (the floor appearing); the outro takes it away again and the bass is still there,
  settling on C# for t7's C# minor.
THE STAIR (F# G# A C#) is climbed by the bass nobody plays, at the end of the groove and of the drop.

FORM (176 bars, ~5:50):
  intro   1-16    the seam in: kick, hats, the phantom bass holding F# (under t5's real 808 on F#1)
  groove  17-48   the rolling phantom line (F#m D Bm C#), claps from 25, stabs from 33, the stair at 45-48
  deeper  49-80   stabs and rims; from 57 the phantom line an octave lower (lower than the speakers play)
  break   81-96   no drums: the bass taken apart into its partials, then put back together
  drop    97-144  everything, THE REAL SUB under the phantom line; it vanishes for bars 127-128 (and the bass stays)
  outro   145-176 the real sub gone, the phantom line thinning; from 161 the phantom holds C# (t7's C#m)
"""
import json
import os
import random

OUT = os.environ.get("C7T6_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers7-t6.yaml")
BAR = 4.0
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
SECTIONS = [("intro", 1, 16), ("groove", 17, 48), ("deeper", 49, 80), ("break", 81, 96), ("drop", 97, 120),
            ("drop2", 121, 144), ("outro", 145, 176)]
DROPS = ("drop", "drop2")
HOLE = (65, 68)
HALFTIME = (121, 136)                        # v9: the second drop's drums in half-time; the four returns for the stair
BARS = SECTIONS[-1][2]
TOTAL = BARS * BAR
FS1 = 30                                    # F#1, 46.25 Hz


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def b0(bar):
    return (bar - 1) * BAR


def sec_of(bar):
    for name, a, z in SECTIONS:
        if a <= bar <= z:
            return name
    return "outro"


class Part:
    def __init__(self):
        self.ev = []

    def add(self, at, ln, head, vel):
        self.ev.append((at, ln, head, int(max(1, min(127, vel)))))

    def score(self, total=TOTAL):
        ev = sorted(self.ev, key=lambda e: (e[0], -e[3]))
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
        return " ".join(toks)


P = {}


def part(n):
    return P.setdefault(n, Part())


# the rolling line, per bar: (beat, length, semitones over the bar's root, velocity)
ROLL = [(0.0, 0.7, 0, 112), (1.0, 0.25, 0, 84), (1.5, 0.45, 3, 96), (2.5, 0.25, 0, 82), (3.0, 0.45, -2, 98),
        (3.5, 0.25, 7, 88)]
# v2: the line keeps changing: the roll, pushed sixteenths, an octave leap, a half-time figure
PUSHED = [(0.0, 0.45, 0, 112), (0.75, 0.25, 0, 86), (1.5, 0.45, 3, 96), (2.25, 0.25, 7, 84), (2.75, 0.45, 0, 98),
          (3.5, 0.25, -2, 90)]
LEAP = [(0.0, 0.7, 0, 112), (1.0, 0.25, 12, 90), (1.5, 0.45, 0, 96), (2.5, 0.25, 12, 86), (3.0, 0.45, 3, 98),
        (3.5, 0.25, -2, 88)]
HALF = [(0.0, 1.4, 0, 112), (2.0, 0.7, -2, 100), (3.0, 0.45, 3, 92)]


def roll_for(bar, sec):
    if sec == "drop2":
        return HALF if bar < 129 else LEAP
    return [ROLL, PUSHED, ROLL, LEAP][((bar - 17) // 8) % 4]
ROOTS = [FS1, FS1 + 1, FS1 - 2, FS1 - 5]    # v10, darker (F# Phrygian): F#m9 | Gmaj7#11 (bII) | Em9 | C#7b9
STAIR = [0, 2, 3, 7]                        # F# G# A C#
ROOTS2 = [FS1 - 4, FS1 - 7, FS1 + 1, FS1 - 5]  # v10: the second drop's walk: Dmaj7#11 | Bm11 | Gmaj7 | C#7b9
DEEP_END = (69, 80)                          # v5: after the hole: no stabs, no congas, the line at its most nasal


M9, M11, MM9 = (0, 3, 7, 10, 14), (0, 3, 7, 10, 17), (0, 3, 7, 11, 14)
MAJ7S11, SIX9S11, D7B9, D7S9 = (0, 4, 7, 11, 18), (0, 4, 9, 14, 18), (0, 4, 7, 10, 13), (0, 4, 7, 10, 15)
# v15 (Harry's third steer: 'very simple progressions... formulaic'): THE GROOVE THROUGH-COMPOSED, 6 + 9 + 7 + 6 bars
# instead of the one-bar loop: a PEDAL (the phantom holds F# while the chords move above it: F#m9, F#m11, Gmaj7#11
# over F#); the loop MUTATING (each pass new extensions); the bass SPIRALLING (32-38: the phantom line as a
# Shepard-Risset loop - the bass nobody plays climbs forever); CHROMATIC MEDIANTS (F#m9, Dmaj7#11, Bbmaj7#11, C#7b9)
GROOVE_CHORD = {}
for _b, _c in zip(range(17, 23), [(0, M9)] * 2 + [(0, M11)] * 2 + [(1, MAJ7S11)] * 2):
    GROOVE_CHORD[_b] = _c
_MUT = {0: [M9, M11, MM9], 1: [MAJ7S11, SIX9S11, MAJ7S11], 10: [M9, M11, M11], 7: [D7B9, D7S9, D7B9]}
for _b in range(23, 32):
    _r = (FS1 + [0, 1, -2, -5][(_b - 1) % 4] - FS1) % 12
    GROOVE_CHORD[_b] = (_r, _MUT[_r][(_b - 23) // 4])
for _b in range(32, 39):
    GROOVE_CHORD[_b] = (0, M9 if _b < 36 else M11)
for _b, _c in zip(range(39, 45), [(0, M9), (0, M9), (8, MAJ7S11), (4, MAJ7S11), (4, MAJ7S11), (7, D7B9)]):
    GROOVE_CHORD[_b] = _c
PEDAL = (17, 22)
SPIRAL = (32, 38)
# v16: THE FIRST DROP THROUGH-COMPOSED, 9 + 7 + 8, in place of the one-bar loop: the floor arrives on a PEDAL (97-105:
# the bass holds F# under the real sub while F#m9, F#m11, Gmaj7#11 move above); THE STAIR COMES DOWN (106-112: a chord
# a bar down the dark descent F#m9 Em9 Dmaj7#11 C#7b9, again with m11/m11); the harmony SLOWS (113-120: two-bar chords
# mutating as they hold - F#m11, Gmaj7#11 > G6/9#11, Em11, C#7#9 - into the half-time)
PEDALS = [PEDAL, (97, 105)]
for _b, _c in zip(range(97, 106), [(0, M9)] * 3 + [(0, M11)] * 3 + [(1, MAJ7S11)] * 3):
    GROOVE_CHORD[_b] = _c
for _b, _c in zip(range(106, 113), [(0, M9), (10, M9), (8, MAJ7S11), (7, D7B9), (0, M11), (10, M11), (8, MAJ7S11)]):
    GROOVE_CHORD[_b] = _c
for _b, _c in zip(range(113, 121), [(0, M11)] * 2 + [(1, MAJ7S11), (1, SIX9S11), (10, M11), (10, M11), (7, D7S9), (7, D7S9)]):
    GROOVE_CHORD[_b] = _c


# v17: THE DEEPER SECTION'S HARMONY, 9 + 7 + 4 + 12 instead of the one-bar loop: DORIAN (49-57: F#m9 and B9, the
# Dorian IV with its D# natural, F#m11, B7, Dmaj7#11); CHROMATIC MEDIANTS as the line drops an octave (58-64: F#m9,
# Am9 - C natural - Cmaj7#11, a tritone from F#, C#7b9); the HOLE on F#m11; THE DEEP END slow (69-80: F#m11,
# Gmaj7#11, C#7#9, four bars each)
DOM9, DOM7 = (0, 4, 7, 10, 14), (0, 4, 7, 10)
for _b, _c in zip(range(49, 58), [(0, M9)] * 2 + [(5, DOM9)] * 2 + [(0, M11)] * 2 + [(5, DOM7), (8, MAJ7S11), (8, MAJ7S11)]):
    GROOVE_CHORD[_b] = _c
for _b, _c in zip(range(58, 65), [(0, M9)] * 2 + [(3, M9)] * 2 + [(6, MAJ7S11), (7, D7B9), (7, D7B9)]):
    GROOVE_CHORD[_b] = _c
for _b in range(65, 69):
    GROOVE_CHORD[_b] = (0, M11)
for _b, _c in zip(range(69, 81), [(0, M11)] * 4 + [(1, MAJ7S11)] * 4 + [(7, D7S9)] * 4):
    GROOVE_CHORD[_b] = _c


# v18: THE SECOND DROP'S HARMONY, 9 + 7 + 4 + 4 instead of the one-bar loop: FALLING THIRDS under the climbing stair
# (121-129: Dmaj7#11, Bm11, Gmaj7#11, three bars each - the chords sink while the stair nobody plays rises); a darker
# turn (130-136: Em9, C#7b9, Dmaj9, C#7#9); HOME IN NOIR under the stair's last climb (137-140: F#m(maj9), its E#
# rubbing on the F#); the REVEAL plain home (141-144: F#m11). B now sits at B1, not B0 (31 Hz).
MAJ9 = (0, 4, 7, 11, 14)
for _b, _c in zip(range(121, 145), [(8, MAJ7S11)] * 3 + [(5, M11)] * 3 + [(1, MAJ7S11)] * 3
                  + [(10, M9)] * 2 + [(7, D7B9)] * 2 + [(8, MAJ9)] + [(7, D7S9)] * 2
                  + [(0, MM9)] * 4 + [(0, M11)] * 4):
    GROOVE_CHORD[_b] = _c


def in_pedal(bar):
    return any(a <= bar <= z for a, z in PEDALS)


def root_of(bar):
    if bar in GROOVE_CHORD and not in_pedal(bar):
        pc = GROOVE_CHORD[bar][0]
        return FS1 + (pc if pc <= 6 else pc - 12)         # F#1 .. C2 up (v17: B, C), the rest below
    if in_pedal(bar):
        return FS1
    return (ROOTS2 if sec_of(bar) == "drop2" else ROOTS)[(bar - 1) % 4]


def chord_of(bar):
    """v15: the chord above the bass (MIDI notes, two octaves up): the groove's plan, else the old voicing."""
    if bar in GROOVE_CHORD:
        pc, ivs = GROOVE_CHORD[bar]
        r = FS1 + 24 + (pc if pc <= 6 else pc - 12)
        return [r + i for i in ivs]
    return voicing(root_of(bar) + 24)


def voicing(r):
    """v10: the chord on root r (MIDI, two octaves up): minor 9ths on F#/E, m11 on B, maj7#11 on G/D, 7b9 on C#."""
    pc = (r - FS1) % 12
    if pc in (0, 10):                          # F#, E: m9
        return [r, r + 3, r + 7, r + 10, r + 14]
    if pc == 5:                                # B: m11
        return [r, r + 3, r + 7, r + 10, r + 17]
    if pc in (1, 8):                           # G, D: maj7#11
        return [r, r + 4, r + 7, r + 11, r + 18]
    return [r, r + 4, r + 7, r + 10, r + 13]   # C#: 7b9


def major_of(bar):
    r = root_of(bar)
    return r != FS1 and r != FS1 - 7


def bass_line():
    for bar in range(1, BARS + 1):
        sec = sec_of(bar)
        root = root_of(bar)
        if sec == "intro":
            part("phantom").add(b0(bar), BAR - 0.1, nm(FS1), 100)
            continue
        if sec == "break":
            continue
        if SPIRAL[0] <= bar <= SPIRAL[1]:                      # v15: the spiral plays the line here
            continue
        if sec == "outro" and bar >= 161:
            part("phantom").add(b0(bar), BAR - 0.1, nm(FS1 - 5), 98)             # C#1: t7's tonic
            continue
        if (sec == "groove" and bar >= 45) or (sec == "drop2" and bar >= 141):     # THE STAIR, climbed by nobody
            st = STAIR[(bar - 1) % 4]
            for b in range(4):
                part("stair").add(b0(bar) + b, 0.9, nm(FS1 + 36 + STAIR[b]), 70 + 6 * b)   # c2-stair counts on
                part("phantom").add(b0(bar) + b, 0.7 if b % 2 == 0 else 0.45, nm(FS1 + st), 108 if b == 0 else 92)
            continue
        low = -12 if (sec == "deeper" and bar >= 57) else 0                     # lower than the speakers play
        roll = roll_for(bar, sec) if sec != "outro" else (ROLL if bar % 2 else ROLL[:2])
        if sec == "outro" and bar <= 152:
            # v5: THE LINE REBUILT FROM ITS PARTIALS: the five pure sines of the break (2..6 x each note), centred now,
            # play the roll - each sounds its harmonic of every note, and together they make the moving bass nobody plays
            for beat, ln, iv, v in ROLL:
                for h in range(2, 7):
                    part(f"h{h}").add(b0(bar) + beat, ln, nm(root + iv), v - 10 - 3 * (h - 2))
            continue
        maj = (root - FS1) % 12 in (1, 8, 7, 4, 5, 6)   # v17: + Bb (a clash in v15: Db over Bbmaj7), B, C       # G, D, C#: the line's third is major over them
        for beat, ln, iv, v in roll:
            iv = 4 if (iv == 3 and maj) else iv
            # v10: the line below what speakers play gets its own track, 6 dB hotter, so it stays in front
            trk = "phantomlow" if low else ("phantompole" if sec == "drop" else "phantom")   # v12: the drop's pole
            part(trk).add(b0(bar) + beat, ln, nm(root + low + iv), v)
            # v3: THE GHOST of the bass: in the drops its accented notes, three octaves up, a sixteenth late, into the dub
            if sec in DROPS and v >= 96:
                part("ghost").add(b0(bar) + beat + 0.25, 0.3, nm(root + iv + 36), v - 30)
        # THE REAL SUB: the floor arrives with the drop (and goes missing for two bars)
        if sec in DROPS and not 127 <= bar <= 128 and bar < 141:
            part("sub").add(b0(bar), 1.6, nm(root), 104)
            part("sub").add(b0(bar) + 2.0, 1.4, nm(root), 96)


def spiral_score():
    """v15: one bar of the roll on F#1, written out with its rests, for the Risset spiral."""
    out, cur = [], 0.0
    for beat, ln, iv, v in ROLL:
        if beat > cur + 1e-6:
            out.append(f"R/{beat - cur:g}b")
        out.append(f"{nm(FS1 + iv)}/{ln:g}b@{v}")
        cur = beat + ln
    if cur < 4.0 - 1e-6:
        out.append(f"R/{4.0 - cur:g}b")
    return " ".join(out)


def riser():
    """v12: an endless Shepard riser over the break's fusion (89-96), stopping dead as the real sub arrives at 97."""
    part("riser").add(b0(89), 32.0, "F#3", 90)


def taken_apart():
    """The break: partials 2..6 of F#1, enter staggered and spread (heard apart), then gather and pulse together (heard as
    one low F#)."""
    for k, h in enumerate(range(2, 7)):
        a = b0(81 + 2 * k)
        part(f"h{h}").add(a, b0(91) - a - 0.05, nm(FS1), 76)
        for bar in range(91, 97):                                                # one rhythm: common onset fuses
            for b in range(4):
                part(f"h{h}").add(b0(bar) + b, 0.7 if b % 2 == 0 else 0.4, nm(FS1), 92 if b == 0 else 80)
    # v14: THE PROOF (teach the ear, chirp-eco's lesson): in bars 92 and 94 the REAL fundamental joins the fused
    # partials, in their rhythm; in 91, 93, 95, 96 it is gone. The floor comes and goes; the pitch never moves.
    for bar in (92, 94):
        for b in range(4):
            part("h1").add(b0(bar) + b, 0.7 if b % 2 == 0 else 0.4, nm(FS1), 100 if b == 0 else 88)


def stair_nobody_plays():
    """v7: THE STAIR NOBODY PLAYS: in the second drop the pure partials 3..6 play the stair (F#3 G#3 A3 C#4) as half-note
    pulses - for F#3 that is 555, 740, 925, 1110 Hz, nothing at 185 - and the ear hears the melody where nothing sounds;
    no single partial even moves by step, only the note they imply does."""
    # v8: THE REVEAL (chirper-one's suggestion): at bar 141, once, the fundamentals themselves - F#3 G#3 A3 C#4, pure
    # sines, one a beat - the melody the room has been imagining, actually played for one bar, then gone
    for b, st in enumerate(STAIR):
        part("h1").add(b0(141) + b, 0.9, nm(54 + st), 92)
    for bar in range(121, 141):
        m = 54 + STAIR[(bar - 121) % 4]                  # F#3 G#3 A3 C#4 (MIDI 54 = F#3)
        for b in (0, 2):
            for h in range(3, 7):
                part(f"h{h}").add(b0(bar) + b, 1.7, nm(m), 84 - 4 * (h - 3) - (6 if b else 0))


def drums():
    hand = random.Random(6)
    for bar in range(1, BARS + 1):
        sec = sec_of(bar)
        if sec == "break":                             # v6: to the last bar (the seam into t7)
            continue
        if HOLE[0] <= bar <= HOLE[1]:                  # v2: THE HOLE: the drums gone, the bass nobody plays alone
            if bar == HOLE[1]:
                for k in range(8):
                    part("hats").add(b0(bar) + 2 + k * 0.25, 0.1, "h", 50 + 7 * k)
            continue
        half = HALFTIME[0] <= bar <= HALFTIME[1]
        if half:                                       # v9: THE SECOND DROP IN HALF-TIME: one, the 'a' of two, the 'and' of three
            for at, v in ((0.0, 116), (1.75, 92), (2.5, 106)):
                part("kick").add(b0(bar) + at, 0.5, "k", v)
        for b in range(4):
            if not half:
                part("kick").add(b0(bar) + b, 0.5, "k", 114 if b == 0 else 106)
            part("hats").add(b0(bar) + b + 0.5, 0.25, "oh", 70 + hand.randint(-6, 6))     # v3: from bar 1 (t5's tail)
            if sec == "intro":
                part("hats").add(b0(bar) + b + 0.75, 0.1, "h", 44 + hand.randint(-6, 6))
            if sec in ("deeper",) + DROPS or (sec == "groove" and bar >= 33):
                for s in (1, 3):
                    if hand.random() < 0.8:
                        part("hats").add(b0(bar) + b + s / 4, 0.1, "h", 56 + hand.randint(-8, 8))
        if (sec in ("groove", "deeper") + DROPS and bar >= 25) or (sec == "outro" and bar < 161):
            for b in ((2,) if half else (1, 3)):               # half-time: one clap, on three
                part("clap").add(b0(bar) + b + 0.012, 0.5, "cp", 94 + hand.randint(-4, 4))
        if sec in ("deeper",) + DROPS:
            for s in (3, 6, 11, 14):                                             # a rim figure, 3-3-2 against the four
                part("rim").add(b0(bar) + s / 4, 0.2, "rs", 70 + hand.randint(-8, 8))


def stabs():
    """A dark minor-ninth stab on the 'e' of one and the 'a' of three (offbeat against t5's 'and's), into a 3/8 delay."""
    for bar in range(33, 161):
        sec = sec_of(bar)
        if sec == "break":
            continue
        if DEEP_END[0] <= bar <= DEEP_END[1]:
            continue
        v = chord_of(bar)
        for b in ((0.5, 1.5, 2.5, 3.5) if sec == "drop2" else (0.75, 2.75)):     # v4: on the 'a's; drop2 every off-beat
            part("stab").add(b0(bar) + b, 0.3 if sec == "drop2" else 0.45, ",".join(nm(m) for m in v), 74 if sec == "drop2" else 80)
        # the dark pad: the chord held through the bar (v2: an octave up, out of the bass's harmonics), deeper + drop
        if sec in ("deeper", "drop"):
            part("pad").add(b0(bar), BAR - 0.1, ",".join(nm(m) for m in v[1:]), 64 if sec == "deeper" else 72)
    for bar in range(17, 45):                                   # v15: the pad carries the groove's new harmony
        part("pad").add(b0(bar), BAR - 0.1, ",".join(nm(m) for m in chord_of(bar)[1:]), 56)


def shaker():
    """v4: a shaker on a DOTTED-EIGHTH cycle (every three sixteenths, running across the bar lines) against the four."""
    hand = random.Random(26)
    cyc = 0
    for bar in range(49, 145):
        sec = sec_of(bar)
        if sec == "break" or HOLE[0] <= bar <= HOLE[1]:
            cyc = (cyc + 16) % 3
            continue
        for s in range(16):
            if (cyc + s) % 3 == 0:
                part("shaker").add(b0(bar) + s / 4, 0.15, "sh", 78 + hand.randint(-8, 8))
        cyc = (cyc + 16) % 3


def congas():
    """Hand percussion from bar 33: open tones and slaps in a two-bar figure, muted ghosts between."""
    hand = random.Random(16)
    fig = [(0.5, "o", 90), (1.25, "mu", 60), (1.75, "o", 84), (2.5, "sl", 96), (3.25, "lo", 88),
           (4.5, "o", 90), (5.0, "mu", 58), (5.75, "lo", 86), (6.5, "sl", 100), (7.25, "o", 82), (7.75, "mu", 56)]
    for bar in range(33, 161, 2):
        if sec_of(bar) in ("break", "drop2") or HOLE[0] <= bar <= DEEP_END[1]:
            continue
        for at, pc, v in fig:
            if hand.random() < 0.9:
                part("conga").add(b0(bar) + at, 0.25, pc, v + hand.randint(-8, 8))


LEVEL = {"intro": -8, "groove": -6, "deeper": -3, "break": -9, "drop": 0, "drop2": -1, "outro": -5}
STEPS = {"groove": [(33, -4)], "deeper": [(65, -6), (69, -2)], "outro": [(161, -7)]}


def lanes():
    dyn = []
    for name, a, z in SECTIONS:
        if dyn:
            dyn.append([f"{b0(a) - 0.25:.2f}b", dyn[-1][1]])
        dyn.append([f"{b0(a):.2f}b", float(LEVEL[name])])
        for at, lv in STEPS.get(name, []):                                       # v2: steps inside long sections
            dyn.append([f"{b0(at) - 0.25:.2f}b", dyn[-1][1]])
            dyn.append([f"{b0(at):.2f}b", float(lv)])
    return dyn


def main():
    bass_line()
    taken_apart()
    riser()
    stair_nobody_plays()
    drums()
    stabs()
    congas()
    shaker()
    tempo = [{"at": "0b", "bpm": 120}, {"at": f"{b0(17):.0f}b", "bpm": 120},
             {"at": f"{b0(145):.0f}b", "bpm": 120.5, "ramp": True}]
    pump = {"type": "pump", "on": "kick", "depth": "-7dB", "attack": "3ms", "release": "330ms", "curve": 0.7}
    tr = lambda n, patch, **kw: dict({"name": n, "patch": patch, "score": part(n).score()}, **kw)
    # the partials: exact harmonics (ratio n on F#1), each from its own place, gathering to the centre by bar 93
    PAN = {2: -0.8, 3: 0.8, 4: -0.45, 5: 0.45, 6: 0.0}
    partials = []
    for h in range(2, 7):
        pts = [["0b", 1.0], [f"{b0(90)}b", 1.0], [f"{b0(93)}b", 0.0], [f"{TOTAL}b", 0.0]]
        partials.append(tr(f"h{h}", {"extends": "partial", "synth": {"layers": [f"sine ratio={h}"]}},
                           gain="-12dB", auto={"pn": {"points": pts}},
                           pan={"value": 0, "mod": [{"src": "auto.pn", "amount": PAN[h]}]},
                           sends={"hall": "-14dB"}))
    song = {
        "about": "Chirpers - The Endless Stair (Chirpers VII), track 6 by chirper-three: NOBODY PLAYS THE BASS. Deep, heavy "
                 "house in F# minor; the missing-fundamental illusion: a bass line of harmonics only, heard where nothing "
                 "plays; taken apart into its partials in the break and put back together; the real sub only in the drop. "
                 "Generated by compose/chirpers7/src/chirpers7-t6.py.",
        "tempo": tempo,
        "patches": {"c2-stair": {"about": "borrowed from chirper-two's t1 (THE STAIR's voice): a Shepard tone, octave-spaced "
                                          "partials under a fixed bell near 600 Hz.",
                                 "synth": {"layers": [{"type": "shepard", "shepard": {"octaves": 8, "center": "600hz",
                                                                                      "width": 1.1}}],
                                           "amp": {"a": "4ms", "d": "700ms", "s": 0.25, "r": "400ms", "curve": 2}},
                                 "play": {"vel_sens": 0.6}}},
        "tail": "0.1s",                          # end on the last bar: the DJ mixes out of it (chirper-one's finding)
        "loudness": -11,
        "buses": {"room": {"fx": ["reverb kind=room decay=1.2s mix=1 predelay=12ms", "hp cutoff=250"]},
                  "hall": {"fx": ["reverb kind=hall decay=3s mix=1 predelay=25ms", "hp cutoff=200"]},
                  "dub": {"fx": ["delay time=3/8 mix=1 feedback=0.5", "hp cutoff=500", "lp cutoff=2800",
                                 "reverb kind=hall decay=2.5s mix=0.3"]}},
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=25", "lowshelf cutoff=220 gain=-6dB", "peak cutoff=160 q=0.8 gain=-2dB",
                                                    "highshelf cutoff=4000 gain=3dB"]},   # tilt: the bass's shape kept
                          {"type": "compressor", "threshold": "-20dB", "ratio": 2.5, "attack": "15ms", "release": "150ms",
                           "makeup": "0dB"},
                          {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                          {"type": "gain", "gain": "+8dB"},
                          {"type": "compressor", "threshold": "-12dB", "ratio": 8, "attack": "0.3ms", "release": "60ms",
                           "makeup": "0dB"}],    # chirper-zero's recipe: catch the kick before the loudness stage
                   "auto": {"dyn": {"points": lanes()}}},
        "tracks": [
            tr("kick", "machine-kit", gain="-11dB"),
            tr("hats", "machine-kit play.humanize.drunk=5ms play.humanize.swing_drift=0.04 play.humanize.accent=0.4", gain="+3dB", pan=0.1, lfo={"hh": {"wave": "sine", "rate": "20b"}},
               fx=[{"type": "filter", "kind": "hp", "cutoff": {"value": 2500, "mod": [{"src": "lfo.hh", "amount": 0.7}]}}]),
            tr("clap", "machine-kit play.humanize.nudge.cp=10ms", gain="-2dB", sends={"room": "-8dB"}),
            tr("rim", "machine-kit", gain="-8dB", pan=-0.3, sends={"dub": "-12dB"}),
            # v12: THE COLOUR CLIMBS FOR EVER, THE PITCH STANDS STILL: in the first drop the phantom line runs through a
            # barber pole (bands an octave apart climbing on the song's clock) - the emphasis glides up through its
            # harmonics endlessly while the pitch the ear rebuilds never moves
            tr("phantompole", "phantom-bass", gain="-5dB", fx=["barberpole cycle=4bar low=60", pump]),
            tr("riser", "fx-riser-endless amp.a=32b", gain="-13dB"),
            {"name": "phantomspiral", "patch": "phantom-bass", "gain": "-7dB", "at": f"{b0(SPIRAL[0]):.0f}b",
             "risset": {"cycle": "4bar", "layers": 3, "length": f"{SPIRAL[1] - SPIRAL[0] + 1}bar", "pitch": True},
             "score": spiral_score()},                     # v15: the bass nobody plays, climbing forever
            tr("phantom", "phantom-bass", gain="-7dB", lfo={"tb": {"wave": "sine", "rate": "44b"}},
               auto={"nz": {"points": [["0b", 0.0], [f"{b0(DEEP_END[0]) - 0.5}b", 0.0], [f"{b0(DEEP_END[0])}b", 1.0],
                                       [f"{b0(DEEP_END[1] + 1) - 0.5}b", 1.0], [f"{b0(DEEP_END[1] + 1)}b", 0.0],
                                       [f"{TOTAL}b", 0.0]]}},
               fx=[{"type": "filter", "kind": "bp", "q": 0.7,          # v2: the colour moves, the pitch doesn't: a
                    "cutoff": {"value": 170, "mod": [{"src": "lfo.tb", "amount": 0.8},     # band-pass over h2..h6;
                                                     {"src": "auto.nz", "amount": 1.0}]}}, pump]),
            tr("phantomlow", "phantom-bass", gain="-1dB",
               # v11: THE BASS NOBODY PLAYS DRIFTS: through the deep end its own clock slides a sixteenth behind the kick
               # over six bars, then eases back onto the grid by bar 80 (re-locked long before any seam)
               warp=[{"over": "68bar", "to": 0}, {"over": "6bar", "to": 0.25}, {"over": "6bar", "to": 0, "curve": "smooth"}], lfo={"tb": {"wave": "sine", "rate": "44b"}},
               auto={"nz": {"points": [["0b", 0.0], [f"{b0(DEEP_END[0]) - 0.5}b", 0.0], [f"{b0(DEEP_END[0])}b", 1.0],
                                       [f"{b0(DEEP_END[1] + 1) - 0.5}b", 1.0], [f"{b0(DEEP_END[1] + 1)}b", 0.0],
                                       [f"{TOTAL}b", 0.0]]}},
               fx=[{"type": "filter", "kind": "bp", "q": 0.7,          # v2: the colour moves, the pitch doesn't: a
                    "cutoff": {"value": 170, "mod": [{"src": "lfo.tb", "amount": 0.8},     # band-pass over h2..h6;
                                                     {"src": "auto.nz", "amount": 1.0}]}}, pump]),   # v5: the deep end nasal
            tr("sub", "808", gain="-16dB", fx=[{"type": "filter", "kind": "lp", "cutoff": 90}, pump]),
            tr("stab", "juno-pad", gain="-5dB", pan=0.2, sends={"dub": "-5dB"}, lfo={"sl": {"wave": "sine", "rate": "28b"}},
               fx=[{"type": "filter", "kind": "lp", "q": 1.2,
                    "cutoff": {"value": 1800, "mod": [{"src": "lfo.sl", "amount": 0.9}]}}, pump]),
            tr("pad", "juno-pad", gain="-9dB", pan=-0.15, sends={"hall": "-8dB"}, lfo={"pd": {"wave": "sine", "rate": "28b"}},
               fx=["tape wow=12 wow_rate=0.3 drift=1 tone=7kHz",   # v13: a slow warble on ONE element, the pad
                   {"type": "filter", "kind": "lp", "q": 0.8,
                    "cutoff": {"value": 1600, "mod": [{"src": "lfo.pd", "amount": 0.8}]}}, pump]),
            tr("conga", "congas play.humanize.time=8ms play.humanize.vel=0.15", gain="-6dB", pan=-0.35, sends={"room": "-10dB"}),
            # v11: under the half-time drop a Risset bed speeding up AND slowing down at once (both: true)
            {"name": "both", "patch": "machine-kit", "gain": "-8dB", "pan": 0.3, "at": f"{b0(HALFTIME[0]):.0f}b",
             "risset": {"cycle": "4bar", "both": True, "layers": 3, "length": f"{HALFTIME[1] - HALFTIME[0] + 1}bar"},
             "sends": {"dub": "-14dB"},
             "score": "rs/0.75b@92 h/0.25b@60 rs/0.5b@84 h/0.5b@58 rs/0.75b@90 h/0.25b@56 cb/0.5b@78 h/0.5b@54"},
            tr("shaker", "djembe", gain="-10dB", pan=0.35, sends={"room": "-12dB"}, fx=["lp cutoff=7000"]),
            tr("ghost", "celesta", gain="-9dB", pan=0.3, sends={"dub": "-3dB"}),
            tr("stair", "c2-stair", gain="-10dB", pan=-0.2, sends={"hall": "-6dB"}),
            tr("h1", "partial", gain="-8dB", sends={"hall": "-10dB"}),    # v8: the reveal's fundamentals
        ] + partials,
    }
    with open(OUT, "w") as f:
        json.dump(song, f, indent=1)
        f.write("\n")
    print(f"wrote {OUT}: {BARS} bars")


if __name__ == "__main__":
    main()
