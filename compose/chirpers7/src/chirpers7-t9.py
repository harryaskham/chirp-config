#!/usr/bin/env python3
"""Chirpers - The Endless Stair (Chirpers VII), track 9: WHERE'S THE ONE (chirper-three).

DEEP MINIMAL TECH-HOUSE, G# minor (1A), 121.5 -> 122 bpm inside the track (the tape's tempo path). Featured illusion:
THE BEAT FLIP (a phantom downbeat). A groove whose stabs and bass accents sit on the off-beats; take the kick away and
the ear re-anchors on them; bring the kick back an eighth LATE, on those off-beats, and the whole groove runs displaced
while sounding perfectly normal; then stop it, leave two bars of doubt, and bring the kick back on the TRUE beat -
which for a few bars sounds like it's on the off-beat, until the claps pull the ear home. In the break a hemiola (the
riff grouped in threes over the four) and a voice saying "one" where the ear thinks the one is: never on the real one.
THE STAIR (G# A# B D#) is a pluck figure that starts on the off-beat, the flip in miniature.

FORM (176 bars, ~5:47):
  intro  1-16    the seam in: kick, hats, the 808 holding G# (t8's C# minor hands a fifth up)
  A      17-40   the groove: kick on the beat, stabs and riff accents on the off-beats, claps 2 and 4
  turn   41-56   41-44 the kick and hats gone (the off-beats become the beat); 45-56 the kick returns DISPLACED, on
                 the off-beats, with the claps on the displaced backbeat: the flipped groove, heard as normal
  back   57-72   57-58 nothing but the stab (doubt); the kick returns on the TRUE beat (heard as the off-beat), the
                 claps on 2 and 4 from 61 pull it home
  break  73-88   no kick: the riff in threes against the four (a hemiola), a pad, the voice counting "one" on the
                 hemiola's accent
  drop   89-136  everything; at 105-112 a quick flip (four bars displaced) and back; the stair on the off-beat
  outro  137-176 the seam out: back on the true beat, thinning; from 161 kick, hats and the 808 on D# (t10's D#m)
"""
import json
import os
import random

OUT = os.environ.get("C7T9_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers7-t9.yaml")
BAR = 4.0
NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
SECTIONS = [("intro", 1, 16), ("A", 17, 40), ("turn", 41, 56), ("back", 57, 72), ("break", 73, 88), ("drop", 89, 136),
            ("outro", 137, 176)]
BARS = SECTIONS[-1][2]
TOTAL = BARS * BAR
GS1 = 32                                     # G#1
FLIP_DISPLACED = [(45, 56), (107, 112), (131, 131)]   # the kick (and claps) an eighth late; v6: bar 131, once, no
# warning - the doubt comes back late and short, and the listener who has learned the trick is caught again (chirper-zero)
KEY_UP = (81, 88)                            # v6: the counted hemiola a fourth up, C# minor: time and key move together
KICKLESS = [(41, 44), (57, 58), (73, 88), (105, 106)]
# v4: THE PHANTOM DOWNBEAT itself: every eighth bar of the groove and the drop, beat one is a hole - no kick, bass, sub,
# stab or hat on the one - and the ear supplies the downbeat that isn't played
# v9: THE FLOOR SLIDES: the flips so far jump; in the drop's second half the kick, claps and hats drift smoothly to an
# eighth behind over eight bars and back over eight (track warp), the riff, stabs and cowbell staying on the grid -
# the downbeat moves continuously; re-locked at bar 129, long before the seam
SLIDE = [{"over": "112bar", "to": 0}, {"over": "8bar", "to": 0.5, "curve": "smooth"},
         {"over": "8bar", "to": 0, "curve": "smooth"}]
GHOST_ONE = {24, 32, 40, 96, 104, 120, 128, 136}


def hole(bar, at):
    return bar in GHOST_ONE and at - b0(bar) < 1.0


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def b0(bar):
    return (bar - 1) * BAR


def sec_of(bar):
    for name, a, z in SECTIONS:
        if a <= bar <= z:
            return name
    return "outro"


def within(bar, spans):
    return any(a <= bar <= z for a, z in spans)


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


# the riff on the sixteenth grid: (position, semitones over the root); its accents fall on the off-beats (2 6 10 14)
RIFF = [(0, 0), (2, 0), (3, 7), (6, 0), (8, -2), (10, 0), (11, 3), (14, 5)]
ROOTS = [GS1, GS1 + 1, GS1 - 4, GS1 - 5]      # v8, darker: G#m9 | Amaj7#11 (Phrygian bII) | Emaj7 | D#7b9
ROOTS_DROP = [GS1, GS1 - 4, GS1 + 5, GS1 - 5]  # v8: the drop: G#m11 | Emaj7#11 | C#m9 | D#7b9


M9, M11, MM9 = (3, 7, 10, 14), (3, 10, 14, 17), (3, 7, 11, 14)
MAJ7S11, MAJ9S11, D7B9, D7S9 = (4, 7, 11, 18), (4, 11, 14, 18), (4, 7, 10, 13), (4, 7, 10, 15)
# v14 (Harry's third steer: 'formulaic'): THE DROP'S FIRST HALF THROUGH-COMPOSED, 10 + 7 + 7 bars instead of the
# one-bar loop: a PEDAL (89-98: the bass holds G# under 'ONE' while chords move above it - G#m11, Amaj7#11 over G#,
# the Phrygian bII grinding on the pedal, G#m(maj9)); the loop MUTATING (99-105: new extensions each pass); and THE
# HARMONIC PENROSE STAIR (106-112: minor chords stepping DOWN by major thirds, G#m9 Em9 Cm9 G#m9 Em9 Cm9 G#m9 - three
# steps down and home again: a staircase that descends forever and goes nowhere, the album's title in harmony)
DROP_PLAN = {}
for _b in range(89, 99):
    DROP_PLAN[_b] = (GS1, GS1, M11) if _b <= 92 else ((GS1, GS1 + 1, MAJ7S11) if _b <= 95 else (GS1, GS1, MM9))
_MUT9 = {0: [M11, M9], 8: [MAJ7S11, MAJ9S11], 5: [M9, M11], 7: [D7B9, D7S9]}
for _b in range(99, 106):
    _r = ROOTS_DROP[(_b - 1) % 4]
    DROP_PLAN[_b] = (_r, _r, _MUT9[(_r - GS1) % 12][(_b - 99) // 4])
for _b, _r in zip(range(106, 113), [GS1, GS1 - 4, GS1 + 4, GS1, GS1 - 4, GS1 + 4, GS1]):
    DROP_PLAN[_b] = (_r, _r, M9)
PENROSE = range(106, 113)


def root_of(bar):
    if bar in DROP_PLAN:
        return DROP_PLAN[bar][0]
    return (ROOTS_DROP if sec_of(bar) == "drop" else ROOTS)[(bar - 1) % 4]


def chord_of(bar):
    """v14: the chord above the bass (MIDI, two octaves up): the drop's plan, else the old voicing."""
    if bar in DROP_PLAN:
        _, cr, ivs = DROP_PLAN[bar]
        return [cr + 24 + i for i in ivs]
    return voicing(root_of(bar) + 24)


def voicing(r):
    """v8: per root, over G#: m9 on G# and C#, maj7#11 on A and E, 7b9 on D# (an unresolved dominant)."""
    pc = (r - GS1) % 12
    if pc in (0, 5):
        return [r + 3, r + 7, r + 10, r + 14]
    if pc in (1, 8):
        return [r + 4, r + 7, r + 11, r + 18]
    return [r + 4, r + 7, r + 10, r + 13]


def riff_iv(root, iv):
    """v8: the riff's minor third turns major (and its flat seventh a major seventh) over A and E; over D# its b7 stays."""
    pc = (root - GS1) % 12
    if pc in (1, 8):
        return {3: 4, -2: -1}.get(iv, iv)
    if pc == 7:
        return {3: 4}.get(iv, iv)
    return iv


def minor_at(bar):
    return root_of(bar) == GS1


def riff():
    for bar in range(17, 161):
        sec = sec_of(bar)
        root = root_of(bar)
        if sec == "break":
            # THE HEMIOLA: the riff's cell (three eighths: root, fifth, root an octave up) over and over against the four
            k0 = (bar - 73) * 8
            for e in range(8):
                k = k0 + e
                note = [0, 7, 12][k % 3] + (5 if KEY_UP[0] <= bar <= KEY_UP[1] else 0)
                part("bass").add(b0(bar) + e * 0.5, 0.4, nm(GS1 + note), 88 if k % 3 == 0 else 58)   # v5: hushed
            continue
        up = 12 if sec == "back" else 0                       # the return comes back changed: an octave up, lighter
        for pos, iv in RIFF:
            acc = pos in (2, 6, 10, 14)
            if sec == "outro" and not acc:                       # the outro thins to the accents
                continue
            if hole(bar, b0(bar) + pos / 4):
                continue
            iv2 = iv if bar in PENROSE else riff_iv(root, iv)       # v14: the Penrose stair's chords are all minor
            part("bass").add(b0(bar) + pos / 4, 0.22, nm(root + iv2 + up), 104 if acc else 80)


def drums():
    hand = random.Random(9)
    for bar in range(1, BARS + 1):
        sec = sec_of(bar)
        disp = within(bar, FLIP_DISPLACED)
        off = 0.5 if disp else 0.0
        if not within(bar, KICKLESS):                            # v2: to the last bar (the seam into t10)
            for b in range(4):
                if hole(bar, b0(bar) + b + off):
                    continue
                part("kick").add(b0(bar) + b + off, 0.5, "k", 114 if b == 0 else 106)
        if sec == "break" or within(bar, [(41, 44), (57, 60), (105, 106)]):
            continue
        for b in range(4):
            if bar >= 5 and not hole(bar, b0(bar) + b + 0.5 - off):
                part("hats").add(b0(bar) + b + 0.5 - off, 0.25, "oh", 68 + hand.randint(-6, 6))   # always opposite the kick
            if sec in ("A", "drop") or (sec == "back" and bar >= 65):
                for s in (1, 3):
                    if hand.random() < 0.7:
                        if not hole(bar, b0(bar) + b + s / 4):
                            part("hats").add(b0(bar) + b + s / 4, 0.1, "h", 52 + hand.randint(-8, 8))
        if (sec in ("A", "turn", "drop") and bar >= 25) or (sec == "back" and bar >= 61) or (sec == "outro" and bar < 161):
            for b in (1, 3):
                part("clap").add(b0(bar) + b + off + 0.012, 0.5, "cp", 94 + hand.randint(-4, 4))
        if sec == "drop" and bar % 4 == 0:
            part("clap").add(b0(bar) + 3.75, 0.25, "rs", 82)


def cowbell_and_ride():
    """v7: in the drop's second half a COWBELL runs a dotted-eighth cycle (every three sixteenths, across the bar lines);
    the cycle's first hit is accented, so its accent meets beat one only every third bar - one more wandering 'one'.
    The outro gets a ride on the off-beats instead of the groove's hats alone: a colour the opening never had."""
    k = 0
    for bar in range(113, 137):
        for s in range(16):
            if (k + s) % 3 == 0:
                first = ((bar - 113) * 16 + s) % 48 == 0
                part("cowbell").add(b0(bar) + s / 4, 0.2, "cb", 100 if first else 66)
        k = (k + 16) % 3
    for bar in range(137, 157):
        for b in range(4):
            part("ride").add(b0(bar) + b + 0.5, 0.4, "rd", 84 if b % 2 else 72)


def fills():
    """v12 (Harry's time-play: accelerating/decelerating fills): bar 88, a snare roll ACCELERATING from eighths to a
    buzz, landing on 'ONE' at 89; bars 44 and 130, fills DECELERATING - the hits spread apart like drums winding
    down - straight into the flips at 45 and 131, so the ear loses the grid just before it is turned over."""
    n = 22
    for i in range(n):                                      # accelerating: quadratic time, intervals shrink to ~0.02 beat
        x = 4.0 * (1 - (1 - i / n) ** 2)
        part("fill").add(b0(88) + x, 0.1, "s", int(48 + 66 * i / n))
    for bar in (44, 130):
        m = 12
        for i in range(m):                                  # decelerating: the mirror image, intervals grow
            x = 3.6 * (i / m) ** 1.8
            part("fill").add(b0(bar) + x, 0.1, "s", int(100 - 40 * i / m))


TTS_ONE_WHERE = [   # v16: chirp tts "one where" --humanize 0.7 --repeat 8 (ce4d6815): (ph, Hz, vel, f0 path in cents)
    ('W AH1 N', 142.85, 0.865, [0.0, 8.0, 16.0, 23.0, 29.0, 33.0, 35.0, 37.0, 41.0, 43.0, 39.0, 28.0, 14.0, 2.0, -5.0, -10.0, -14.0]),
    ('W EH1 R', 105.73, 0.799, [0.0, 3.0, 6.0, 9.0, 11.0, 13.0, 14.0, 14.0, 15.0, 17.0, 15.0, 9.0, 1.0, -7.0, -10.0, -10.0, -11.0, -18.0, -31.0, -47.0, -62.0, -71.0, -75.0, -79.0]),
    ('W AH1 N', 139.05, 0.85, [0.0, 8.0, 16.0, 23.0, 29.0, 33.0, 35.0, 37.0, 41.0, 43.0, 39.0, 28.0, 14.0, 2.0, -5.0, -10.0, -14.0]),
    ('W EH1 R', 106.35, 0.799, [0.0, 3.0, 6.0, 9.0, 11.0, 13.0, 14.0, 14.0, 15.0, 17.0, 15.0, 9.0, 1.0, -7.0, -10.0, -10.0, -11.0, -18.0, -31.0, -47.0, -62.0, -71.0, -75.0, -79.0]),
    ('W AH1 N', 140.46, 0.797, [0.0, 8.0, 16.0, 23.0, 29.0, 33.0, 35.0, 37.0, 41.0, 43.0, 39.0, 28.0, 14.0, 2.0, -5.0, -10.0, -14.0]),
    ('W EH1 R', 105.31, 0.774, [0.0, 3.0, 6.0, 9.0, 11.0, 13.0, 14.0, 14.0, 15.0, 17.0, 15.0, 9.0, 1.0, -7.0, -10.0, -10.0, -11.0, -18.0, -31.0, -47.0, -62.0, -71.0, -75.0, -79.0]),
    ('W AH1 N', 141.76, 0.742, [0.0, 8.0, 16.0, 23.0, 29.0, 33.0, 35.0, 37.0, 41.0, 43.0, 39.0, 28.0, 14.0, 2.0, -5.0, -10.0, -14.0]),
    ('W EH1 R', 104.28, 0.762, [0.0, 3.0, 6.0, 9.0, 11.0, 13.0, 14.0, 14.0, 15.0, 17.0, 15.0, 9.0, 1.0, -7.0, -10.0, -10.0, -11.0, -18.0, -31.0, -47.0, -62.0, -71.0, -75.0, -79.0]),
    ('W AH1 N', 140.1, 0.875, [0.0, 8.0, 16.0, 23.0, 29.0, 33.0, 35.0, 37.0, 41.0, 43.0, 39.0, 28.0, 14.0, 2.0, -5.0, -10.0, -14.0]),
    ('W EH1 R', 106.49, 0.763, [0.0, 3.0, 6.0, 9.0, 11.0, 13.0, 14.0, 14.0, 15.0, 17.0, 15.0, 9.0, 1.0, -7.0, -10.0, -10.0, -11.0, -18.0, -31.0, -47.0, -62.0, -71.0, -75.0, -79.0]),
    ('W AH1 N', 142.61, 0.849, [0.0, 8.0, 16.0, 23.0, 29.0, 33.0, 35.0, 37.0, 41.0, 43.0, 39.0, 28.0, 14.0, 2.0, -5.0, -10.0, -14.0]),
    ('W EH1 R', 104.68, 0.732, [0.0, 3.0, 6.0, 9.0, 11.0, 13.0, 14.0, 14.0, 15.0, 17.0, 15.0, 9.0, 1.0, -7.0, -10.0, -10.0, -11.0, -18.0, -31.0, -47.0, -62.0, -71.0, -75.0, -79.0]),
    ('W AH1 N', 140.66, 0.789, [0.0, 8.0, 16.0, 23.0, 29.0, 33.0, 35.0, 37.0, 41.0, 43.0, 39.0, 28.0, 14.0, 2.0, -5.0, -10.0, -14.0]),
    ('W EH1 R', 107.92, 0.862, [0.0, 3.0, 6.0, 9.0, 11.0, 13.0, 14.0, 14.0, 15.0, 17.0, 15.0, 9.0, 1.0, -7.0, -10.0, -10.0, -11.0, -18.0, -31.0, -47.0, -62.0, -71.0, -75.0, -79.0]),
    ('W AH1 N', 140.97, 0.752, [0.0, 8.0, 16.0, 23.0, 29.0, 33.0, 35.0, 37.0, 41.0, 43.0, 39.0, 28.0, 14.0, 2.0, -5.0, -10.0, -14.0]),
    ('W EH1 R', 104.72, 0.76, [0.0, 3.0, 6.0, 9.0, 11.0, 13.0, 14.0, 14.0, 15.0, 17.0, 15.0, 9.0, 1.0, -7.0, -10.0, -10.0, -11.0, -18.0, -31.0, -47.0, -62.0, -71.0, -75.0, -79.0]),
]


PHN = {"phL": [], "phR": []}


def ph_note(side, at, ln, rep, syl, gain):
    """v16: a native voice note from the humanized tts data: repetition rep (mod 8), syllable syl (0 'one', 1 'where')."""
    ph, hz, vel, f0 = TTS_ONE_WHERE[(rep % 8) * 2 + syl]
    PHN[side].append({"at": round(at, 4), "len": ln, "ph": ph, "pitch": f"{hz}hz", "vel": round(vel * gain, 3),
                      "expr_path": {"f0": f0}})


def radio_fx(seed):
    return [{"type": "radio", "tune": {"value": 0, "mod": [{"src": "auto.dial", "amount": 1}]}, "fade": 0.4,
             "drift": 0.05, "hiss": "-30dB", "whistle": "-30dB", "seed": seed},
            {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.rg", "amount": 1}]}}]


def radio_lanes(side):
    """v15: the dial (0 on the station, 1 off) and the gate (0 dB where the voice speaks, -80 dB elsewhere)."""
    k = 0.08 if side else 0.0                          # the right-hand radio a touch further off, all the way
    dial = [["0b", 0.2 + k], [f"{b0(81):.2f}b", 1.0], [f"{b0(84):.2f}b", k], [f"{b0(87):.2f}b", k],
            [f"{b0(88) + 2:.2f}b", 0.45 + k], [f"{b0(89) - 0.25:.2f}b", 0.0], [f"{b0(90):.2f}b", 0.0]]
    rg = [["0b", -80.0]]
    for a, z in ((b0(24) - 0.5, b0(24) + 2), (b0(32) - 0.5, b0(32) + 2), (b0(81) - 0.25, b0(90) + 2)):
        rg += [[f"{a - 0.05:.2f}b", -80.0], [f"{a:.2f}b", 0.0], [f"{z:.2f}b", 0.0], [f"{z + 0.5:.2f}b", -80.0]]
    return {"dial": {"points": dial}, "rg": {"points": rg}}


def frame_the_holes():
    """v11 (chirp-eco's lesson from t10: a bare hole in a mixed groove reads as a glitch): every empty downbeat is now
    performed. The last stab before it is thrown into a high-feedback dub delay, so its echoes ring through the hole;
    and on the first two the voice softly says 'one' exactly where the beat is missing - the phantom downbeat named."""
    for g in sorted(GHOST_ONE):
        v = chord_of(g - 1)
        part("throw").add(b0(g) - 0.5, 0.25, ",".join(nm(m) for m in v), 92)
        if g in (24, 32):
            for side in ("phL", "phR"):                       # v13: the whisper through the radio band, both sides
                ph_note(side, b0(g), 0.5, 2 + (side == "phR"), 0, 0.55)


def riser():
    """v10: an endless Shepard riser (tinted on C#, the counted bars' key) over the break's second half, stopping dead
    on bar 89 - where the voice says ONE on the true downbeat."""
    part("riser").add(b0(81), 32.0, "C#3", 90)


def stabs():
    """G#m9 on the off-beats: the anchor the ear moves to when the kick goes."""
    for bar in range(17, 145):
        sec = sec_of(bar)
        if sec == "break":
            continue
        v = chord_of(bar)
        hits = (0.75, 1.5, 2.75, 3.5) if (sec == "drop" and bar >= 121) else (0.5, 1.5, 2.5, 3.5)   # the anchor shifts
        for b in hits:
            if hole(bar, b0(bar) + b):
                continue
            part("stabturn" if 41 <= bar <= 56 else "stab").add(b0(bar) + b, 0.18, ",".join(nm(m) for m in v), 84 if b in (0.5, 0.75, 2.5, 2.75) else 72)


def sub_and_pad():
    for bar in range(1, BARS + 1):
        sec = sec_of(bar)
        root = root_of(bar)                            # the 808 on the riff's root
        if sec == "intro" or (sec == "outro" and bar < 161):
            part("sub").add(b0(bar), BAR - 0.1, nm(GS1), 92)
        elif sec == "outro":
            part("sub").add(b0(bar), BAR - 0.1, nm(GS1 - 5), 120)           # D#1: the fifth, t10's D# minor (full: the seam)
        elif sec == "break":
            if bar == 73:
                part("pad").add(b0(bar), 8 * BAR - 0.1, ",".join(nm(m) for m in (56, 59, 63, 66, 70)), 70)
            elif bar == 81:                                  # v6: C#m9 for the counted bars (chirper-one's fourth)
                part("pad").add(b0(bar), 8 * BAR - 0.1, ",".join(nm(m) for m in (61, 64, 68, 71, 75)), 72)
        elif not within(bar, [(41, 44), (57, 58)]):
            if bar in GHOST_ONE:
                part("sub").add(b0(bar) + 1.0, 0.6, nm(root), 100)        # the one left empty
            else:
                part("sub").add(b0(bar), 1.6, nm(root), 100)
            part("sub").add(b0(bar) + 2, 1.6, nm(root), 92)


def stair_and_voice():
    # THE STAIR on a pluck, starting on the off-beat (the flip in miniature)
    for bar in list(range(33, 41, 2)) + list(range(121, 137, 4)):
        for k, iv in enumerate((0, 2, 3, 7)):
            part("stair").add(b0(bar) + 0.5 + k * 0.75, 0.6, nm(GS1 + 36 + iv), 78 + 5 * k)
    # v13 (Harry's third steer: 'our robotic vox is not subtle enough or illusory enough'): the counting voice, the lone
    # 'one's and the shouted ONE are gone. PHANTOM WORDS (Deutsch) through the dark break instead: a two-syllable loop,
    # 'one . where', each syllable a dotted quarter (the loop three beats long: the hemiola, unexplained), on two
    # copies hard left and right through a distant radio band, the right a syllable behind the left - one side says
    # 'one where one where' while the other says 'where one where one', and the ear assembles words that are not
    # there ('wonder', 'nowhere', 'where-one'). The left starts alone at 81; the right joins at 83. At 89 the phantom
    # RESOLVES: both say 'one' together, on the true downbeat, quietly into the dub.
    syl = [("w-ah1-n", "0>-6"), ("w-eh1-r", "0>-4")]
    for side, start, shift in (("phL", 81, 0), ("phR", 83, 1)):
        k = 0
        while True:
            at = b0(start) + k * 1.5
            if at >= b0(89) - 0.75:
                break
            ph, f0 = syl[(k + shift) % 2]
            # v16: each syllable lifted from one repetition of a HUMANIZED 'one where' (pitch, contour, effort)
            ph_note(side, at, 0.7, k // 2 + (3 if side == "phR" else 0), (k + shift) % 2, 0.95)
            k += 1
    for side in ("phL", "phR"):
        ph_note(side, b0(89), 0.8, 0, 0, 1.0)


LEVEL = {"intro": -8, "A": -4, "turn": -3, "back": -3, "break": -8, "drop": 0, "outro": -5}


def lanes():
    dyn = []
    for name, a, z in SECTIONS:
        if dyn:
            dyn.append([f"{b0(a) - 0.25:.2f}b", dyn[-1][1]])
        dyn.append([f"{b0(a):.2f}b", float(LEVEL[name])])
    return dyn


def main():
    riff()
    drums()
    stabs()
    sub_and_pad()
    stair_and_voice()
    cowbell_and_ride()
    riser()
    frame_the_holes()
    fills()
    tempo = [{"at": "0b", "bpm": 121.5}, {"at": f"{b0(17):.0f}b", "bpm": 121.5},
             {"at": f"{b0(137):.0f}b", "bpm": 122, "ramp": True}]
    pump = {"type": "pump", "on": "kick", "depth": "-7dB", "attack": "3ms", "release": "320ms", "curve": 0.7}
    tr = lambda n, patch, **kw: dict({"name": n, "patch": patch, "score": part(n).score()}, **kw)
    song = {
        "about": "Chirpers - The Endless Stair (Chirpers VII), track 9 by chirper-three: WHERE'S THE ONE. Deep minimal "
                 "tech-house in G# minor; the beat-flip illusion (a phantom downbeat): the kick leaves, the ear re-anchors "
                 "on the off-beats, the kick returns an eighth late and sounds normal, then returns on the true beat and "
                 "sounds wrong; a hemiola break with a voice counting 'one' in the wrong place. Generated by "
                 "compose/chirpers7/src/chirpers7-t9.py.",
        "tempo": tempo,
        "tail": "0.1s",                          # end on the last bar: the DJ mixes out of it (chirper-one's finding)
        "loudness": -11,
        "volume": "0dB",
        "buses": {"throwbus": {"fx": ["delay time=3/16 mix=1 feedback=0.62", "hp cutoff=400", "lp cutoff=3000",
                                      "reverb kind=hall decay=2.4s mix=0.35"]},
                  "room": {"fx": ["reverb kind=room decay=1.1s mix=1 predelay=10ms", "hp cutoff=250"]},
                  "dub": {"fx": ["delay time=3/16 mix=1 feedback=0.45", "hp cutoff=500", "lp cutoff=3500",
                                 "reverb kind=hall decay=2.2s mix=0.3"]}},
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=28", "lowshelf cutoff=200 gain=-3dB",
                                                    "highshelf cutoff=5000 gain=4dB"]},
                          {"type": "compressor", "threshold": "-20dB", "ratio": 2.5, "attack": "15ms", "release": "150ms",
                           "makeup": "0dB"},
                          {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                          {"type": "gain", "gain": "+8dB"},
                          {"type": "compressor", "threshold": "-12dB", "ratio": 8, "attack": "0.3ms", "release": "60ms",
                           "makeup": "0dB"}],
                   "auto": {"dyn": {"points": lanes()}}},
        "tracks": [
            tr("kick", "machine-kit", gain="-14dB", warp=SLIDE),
            tr("hats", "machine-kit", gain="3dB", pan=0.1, warp=SLIDE, lfo={"hh": {"wave": "sine", "rate": "20b"}},
               fx=[{"type": "filter", "kind": "hp", "cutoff": {"value": 3000, "mod": [{"src": "lfo.hh", "amount": 0.6}]}}]),
            tr("clap", "machine-kit", gain="-3dB", warp=SLIDE, sends={"room": "-8dB"}),
            tr("fill", "machine-kit", gain="-8dB", pan=-0.1, sends={"room": "-8dB", "dub": "-14dB"}),   # v12: the fills
            tr("bass", "acid", gain="-6dB", lfo={"bc": {"wave": "sine", "rate": "36b"}},
               auto={"dk": {"points": [["0b", 0.0], [f"{b0(73)}b", 0.0], [f"{b0(76)}b", -1.5], [f"{b0(87)}b", -1.5],
                                       [f"{b0(89)}b", 0.0], [f"{TOTAL}b", 0.0]]}},     # v5: the break goes dark
               fx=[{"type": "filter", "kind": "lp", "q": 0.8,
                    "cutoff": {"value": 700, "mod": [{"src": "lfo.bc", "amount": 0.9},
                                                     {"src": "auto.dk", "amount": 1.0}]}}, pump]),
            tr("sub", "808", gain="-23dB", fx=[{"type": "filter", "kind": "lp", "cutoff": 100}, pump]),
            tr("stab", "juno-pad", gain="-4dB", pan=-0.15, sends={"dub": "-6dB"}, lfo={"sl": {"wave": "sine", "rate": "28b"}},
               fx=[{"type": "filter", "kind": "bp", "q": 0.8,
                    "cutoff": {"value": 1400, "mod": [{"src": "lfo.sl", "amount": 0.8}]}}, pump]),
            # v10: in the turn, where the floor flips, the off-beat anchor's colour sinks for ever (a falling barber pole)
            tr("stabturn", "juno-pad", gain="-4dB", pan=-0.15, sends={"dub": "-6dB"}, lfo={"sl": {"wave": "sine", "rate": "28b"}},
               fx=["barberpole cycle=2bar down=true", {"type": "filter", "kind": "bp", "q": 0.8,
                    "cutoff": {"value": 1400, "mod": [{"src": "lfo.sl", "amount": 0.8}]}}, pump]),
            tr("riser", "fx-riser-endless amp.a=32b", gain="-13dB"),
            tr("throw", "juno-pad", gain="-8dB", pan=0.2, sends={"throwbus": "0dB"},
               fx=[{"type": "filter", "kind": "bp", "cutoff": 1400, "q": 0.8}]),     # v11: the dub throw into each hole
            tr("pad", "juno-pad", gain="-8dB", sends={"dub": "-10dB"},
               fx=[{"type": "filter", "kind": "lp", "cutoff": 2200}]),
            # v8: under the break a RISSET ACCELERANDO (rims and a cowbell speeding up for ever, never faster) against
            # the counted hemiola and the bar: three clocks at once
            {"name": "rush", "patch": "machine-kit", "gain": "-5dB", "pan": -0.2, "at": f"{b0(73):.0f}b",
             "risset": {"cycle": "4bar", "down": False, "layers": 3, "length": "16bar"},
             "sends": {"dub": "-14dB", "room": "-10dB"},
             "score": "rs/0.75b@96 rs/0.75b@84 rs/0.5b@90 rs/0.75b@96 cb/0.75b@80 rs/0.5b@88"},
            tr("cowbell", "machine-kit", gain="-10dB", pan=-0.25, sends={"dub": "-12dB"}),
            tr("ride", "machine-kit", gain="-6dB", pan=0.2),
            tr("stair", "celesta", gain="-8dB", pan=0.3, sends={"dub": "-4dB"}),
            # v13: the phantom words - two copies, hard left and right, through a distant radio band (Deutsch played his
            # on two loudspeakers: it reads on speakers and on headphones)
            # v15: each copy through its own RADIO (wM's fx, mono, so one per side keeps the pair): the dial tunes in
            # across the break (off the station at 81 - static, a heterodyne whistle - on it by 84), wanders off before
            # the drop and lands dead on the station for the 'one' at 89; a gate lane keeps the static to where it speaks
            {"name": "phL", "patch": "voice-speech", "gain": "-10dB", "pan": -1.0, "sends": {"dub": "-14dB"},
             "auto": radio_lanes(0), "fx": radio_fx(3), "notes": PHN["phL"]},      # v16: humanized, native notes
            {"name": "phR", "patch": "voice-speech", "gain": "-10dB", "pan": 1.0, "sends": {"dub": "-14dB"},
             "auto": radio_lanes(1), "fx": radio_fx(7), "notes": PHN["phR"]},
        ],
    }
    with open(OUT, "w") as f:
        json.dump(song, f, indent=1)
        f.write("\n")
    print(f"wrote {OUT}: {BARS} bars")


if __name__ == "__main__":
    main()
