#!/usr/bin/env python3
"""chirpers10-t16 "Close Enough" (chirper-two): two reeds a hair apart, and a band that plays the difference.

Tune one string to another and you do not listen to the notes: you listen to the wobble between them, and you turn
the peg until it slows, and stops. Two notes a hair apart make a third thing that is not a note at all but a pulse,
as many times a second as the hair is wide in cycles. And every overtone of the pair is twice, three times, four
times as far apart as the notes themselves: so the second harmonic pulses twice for each pulse of the first, the
third three times, the fourth four. One mistuned unison is a polyrhythm, 1 : 2 : 3 : 4, with nobody playing it.

This piece is that, taken as the whole rhythm section. Two harmoniums hold one note. The second is sharp of the
first by a width chosen in cycles a second, so that the wobble of the pair is IN TEMPO: at 66 to the minute a hair
of 1.1 Hz (eleven cents at F3) pulses once a beat. Then, with no further choice, the band plays what the pair is
already doing:

  the kick      the pulse of the notes themselves       (the first harmonic's beats; the bass holds a note to each)
  the guitars   twice as fast: the second harmonic's    (the low note open with the kick, muted between)
  the toms      three times: the third's
  the hat       four times: the fourth's
  the snare     is not in the rule: two and four of every bar. The drummer's left hand keeps common time

So the METRE IS A TUNING. Widen the hair by a quarter and the whole band is in five against the snare's four; by
three quarters, in seven; narrow it and they are in three; halve it and they play half as often. Nothing is
counted: the form below is a list of widths. And the song ends the way tuning ends: the hair is halved, and halved
again, the strokes come further and further apart (each rings until the next), and when the two reeds are one note
the band has one chord left.

  in tune      the pair on one note: still
  a hair       a quarter of a pulse to the beat: one kick to the bar, four taps of the hat
  wider        half a pulse to the beat
  square       ONE pulse to the beat: common time, from a tuning. The band comes in
  five         a hair and a quarter: five against four
  seven        a hair and three quarters: seven against four
  three        three quarters of a hair: three against four, the slow one, on the lowest ground
  square       one again, as long as the first time
  close enough a half, a quarter, an eighth, and in tune: the last chord

Inside each kick, then, there is one cell: two against three against four (guitar, toms, hat). It is the same cell at
every width; only how many of them fit the snare's bar changes.

v1 is the SKELETON: the whole shape standing, bare (Harry, 19 Nov: "each climber can go crazy and make the song they
want to mkae"). The pair's pitches are written in hertz, so that the hair is a number of cycles and not of cents.

The first thing built for this slot was a Collatz song (halve the even, treble the odd and add one, as lengths and as
harmonics of F). chirper-one recorded So Far on the same rule in track seventeen while it was on the bench, so this
is the other song.
"""
import json
import math
import os
from collections import defaultdict
from fractions import Fraction as Fr

OUT = os.environ.get("C10T16_OUT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../songs/chirpers10-t16.yaml"))
BPM = 66
HAIR = BPM / 60.0                            # Hz: the width that pulses once a beat
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


# THE FORM: name ; the hair's width, in pulses to the beat ; bars ; the ground (semitones over F) ; who plays
#   k = the kick (the notes' own pulse), g = guitars and bass (twice), t = toms (three times), h = hat (four times),
#   s = the snare on three, c = an open chord on each bar line
FORM = [
    ("in tune", Fr(0), 2, 0, ""),
    ("a hair", Fr(1, 4), 4, 0, "kh"),
    ("wider", Fr(1, 2), 4, 0, "khts"),
    ("square", Fr(1), 8, 0, "kgthsc"),
    ("five", Fr(5, 4), 8, 3, "kgthsc"),
    ("seven", Fr(7, 4), 8, 6, "kgthsc"),
    ("three", Fr(3, 4), 8, -2, "kgthsc"),
    ("square again", Fr(1), 8, 0, "kgthsc"),
    ("a half", Fr(1, 2), 2, 0, "kgths"),
    ("a quarter", Fr(1, 4), 2, 0, "kgh"),
    ("an eighth", Fr(1, 8), 2, 0, "kg"),
    ("close enough", Fr(0), 2, 0, "c"),
]
REED = 53                                    # the pair's note on F: F3
# v2, palette: THE PULSES ARE NAMED. The pair's overtones pulse two, three and four times to its one, and the kit
# says so in strokes that have no pitch. A handpan (no other song on the record has one; its note fields are tuned
# fundamental, octave and twelfth, the first three of the pair's own series) strikes each overtone AS A NOTE every
# time that overtone swells: the reed's own F once to the pulse, the octave twice, the twelfth (C) three times, the
# double octave four times. All four swell together on the pulse, so the pulse is a chord; between pulses it is
# two against three against four: high F, C, the two Fs, C, high F. The cell is a tune, and it is the tune the
# two reeds are already singing. Its notes are written in hertz, at whole multiples of the still reed.
# It frames the song, and it SAYS, THEN LISTENS. As the hair opens (0:07.3) it names the overtones in order, a bar
# each: one and two; then three; then four; and leaves the fourth bar to the pair alone. When the hair is twice as
# wide (0:21.8) it says the whole cell on the first pulse of each bar and leaves the second to the pair, until the
# band takes the cell over at 0:36.4. As the hair closes it comes back where the toms have gone (3:09.1) and
# leaves as it came, the fours first, then the threes; the last pulse (3:16.4, two bars long) has only one and
# two; then one chord, in tune.
# Empty restores v1.  The song's own handpan ; the track gain as the hair opens ; as it closes (the band is in;
# leave this field empty and it does not come back at the end: re-fit the target) ; the loudness target (every bar
# without it keeps v1's mastering gain).
# (The library handpan beats with itself: a split partner 3 cents up on the fundamental, the octave 2 cents sharp,
# the twelfth 3 flat; and its shell answers at 92 Hz, a semitone over F. In this song the only wobble may be the
# hair: the partner is silenced, the partials are exact, the shell is on F2.)
PAN = os.environ.get("C10T16_PAN", "handpan synth.layers.0.partials.1.1=0 synth.layers.1.cents=0 synth.layers.2.cents=0 synth.layers.3.fixed=87.307;-17dB;-11dB;-9.981")
NAMED = {"a hair": ((1, 2), (1, 2, 3), (1, 2, 3, 4), ()), "wider": ((1, 2, 3, 4), ()) * 4,
         "a quarter": ((1, 2, 3, 4), (1, 2, 3)), "an eighth": ((1, 2),)}
TOUCH = {1: 0.8, 2: 0.68, 3: 0.6, 4: 0.54}
STILL = "harmonium fx.0.depth=0 synth.layers.1.cents=0"       # see the tracks
# v3 (chirper-three; section round, w4: bars 25-26, 1:27.3-1:34.5): THE PEG IS TURNED. v1's second want: every change
# of width was a cut at a bar line, and tuning is not done in cuts. For the last two bars of 'five' the sharp reed
# is no longer struck at one width and held: it is struck once and GLIDES, from a hair and a quarter to a hair and
# three quarters (1.375 to 1.925 Hz over A flat), as a peg is turned. The pair's pulse quickens under the hand, five
# to the bar becoming seven, and the band does what it always does: it plays the pulse. So the kick, the bass, the
# guitars, the toms and the hat ACCELERATE together over two bars (twelve pulses where there were ten; the guitars
# twenty-four strokes, the toms thirty-six, the hat forty-eight), each stroke where the pair's own swell falls,
# and arrive at 'seven' already at its speed: the key changes at 1:34.5 and the pulse does not. The snare and the
# china are not in the rule: they stay on two and four and on the bar line, so for seven seconds the band pulls
# away from a backbeat that does not move.
# The stroke times are not counted, they are solved: the phase of the pair's beat is the integral of the hair's
# width, and a stroke falls where that phase is a whole number (the guitars' at halves, the toms' at thirds, the
# hat's at quarters). The glide's far end is fitted so that the two bars hold a whole number of pulses.
# which section's last bars slide to the next section's width : how many bars (several: "five:2,seven:1"; a slide
# must hold a whole number of pulses). "" = v2.
SLIDE = os.environ.get("C10T16_SLIDE", "five:2" if PAN else "")
SLIDES = {s.split(":")[0]: int(s.split(":")[1]) for s in SLIDE.split(",")} if SLIDE else {}
# v4 (chirper-alpha, instrument: THE TOMS). The three drums that say the threes were the album kit's as it comes:
# a floor tom on F2, a rack tom on C3 and one on F3, in every section. Two things were wrong with that, and neither
# is a matter of level. (1) THEY DID NOT FOLLOW THE GROUND. The song moves to A flat, to B and to the low E flat,
# and the guitars, the bass and the pair move with it; the drums went on saying F, C, F: over the B of 'seven'
# that is a tritone and a minor ninth, 168 pitched strokes of it in the song's busiest section. (2) THE TOP DRUM
# SAT ON THE REED'S OWN NOTE: F3, 174.6 Hz, is the pair's note on F, the very line whose slow swell is the song's
# subject, and a drum rang there three times a pulse.
# Now the three drums are tuned to the ground's root and fifth, the three lowest of them a drum can hold (from B flat 1,
# 58 Hz, up): on F they are C2, F2, C3; on A flat E flat 2, A flat 2, E flat 3; on B B1, G flat 2, B2; on the low
# E flat B flat 1, E flat 2, B flat 2. No drum is on the pair's note in any section, and the drums as a set sit a fourth to
# an octave lower: big slow drums for the slowest song on the record, under the pair and not in it. No stroke moves.
# (The kit's pieces cannot change pitch in mid-song, so each ground has the same three drums on its own track.)
# Drums in tune with the band add to its own lines instead of lying between them: benched raw in 'seven', the retuned
# drums alone held LESS of 250-500 Hz than before (26% of the band for 33%), yet the mix there rose 0.7 dB, where it
# was already the song's furthest band over the records. So the drums' tracks take 3 dB off at 330 Hz (TOMS_EQ).
# ground in semitones over F = floor tom, middle, top ; ... "" = v3.
TOMS = os.environ.get("C10T16_TOMS", "0=C2,F2,C3;3=Eb2,Ab2,Eb3;6=B1,Gb2,B2;-2=Bb1,Eb2,Bb2") if SLIDE else ""
TOMS_EQ = [{"type": "eq", "bands": ["peak cutoff=330 q=1 gain=-3dB"]}]
# v5 (chirper-three; whole song): THE NUMBERS STAY IN THE AIR. For two and a half minutes the band counted and
# nothing sang: each section was one bare fifth. The pair's own note is the FOURTH harmonic of the guitars' low
# string, and in 'square' the band plays four to the bar. So when the band plays five to the bar a third reed
# sings the low string's FIFTH harmonic, and when it plays seven, the SEVENTH: the song's own still harmonium, in
# the middle, struck once and held, exactly in tune with the still reed (whole-number ratios: 14 cents under the
# piano's major third, 31 under its seventh), each note brought by octaves into the octave from A4 up. With the
# pair's four and the guitars' fifth that is 4:5:6:7, the low string's own overtones.
#   bar 21 (1:12.7)  the fifth over A flat (C5), four bars; it rests while the peg is turned
#   bar 27 (1:34.5)  the fifth over B (D sharp 5)
#   bar 31 (1:49.1)  the seventh joins under it (A4): four bars of the whole chord
#   bar 35 (2:03.6)  on the low E flat both stay (D flat 5 and G5); bar 37 the seventh has gone; bar 39 the fifth
# ONLY FIVE AND SEVEN. A reed in tune with the still reed puts its overtones exactly on the still reed's wherever
# they meet, and drowns the hair's wobble there. The third harmonic and the sixth both land on the pair's third
# overtone, the toms' pulse (benched: with the third harmonic sounding that pulse fell from 25 dB deep to 4). Five
# and seven meet nothing below the pair's fifth overtone: with them the pair's four pulses read as they do alone.
# So 'three' cannot have its own number sung, and the chord leaves there instead.
# the third reed's gain ; its pan ; the loudness target ("" = unchanged) ; its eq bands ; dB on each note, in the
# order they are struck ("" = none). "" = v4.
THIRD = os.environ.get("C10T16_THIRD", "-11dB;0;-9.898;peak cutoff=330 q=0.8 gain=-9dB;-1,0.5,-3,0.5,-6,-4,-4" if TOMS else "")
# section: (bar of the section, bars held, the harmonic of the ground's low string), ... The pair's own note is 4.
WALK = {"five": ((2, 4, 10),), "seven": ((0, 4, 10), (4, 4, 7), (4, 4, 10)), "three": ((0, 2, 14), (0, 2, 20), (2, 2, 20))}
# v6 (chirper-two; palette: two instruments of the song's own, where the band is not): BEFORE THE BAND AND AFTER IT.
# For the first 36 seconds and the last 14 there is no band, or hardly any: two harmoniums, a handpan, and the pulse
# pointed at by the metal kit's kick and hi-hat alone, the album's two most-used sounds standing bare beside reeds.
# Those bars now have their own two players. A GREAT DRUM under each stroke of the foot: a low drum that takes a
# pitch, on the low F (43.65 Hz), struck every 3.6 s as the hair opens and every 1.8 s as it widens, and left to
# ring (20 dB down in 0.9 s). And A PAIR OF FINGER CYMBALS on the hat's strokes (the fours): the small brass pair
# that keeps time beside a harmonium, tuned to the reed's own F four octaves up, struck and left to ring on the
# pulse, struck and held shut between. When the band comes in (0:36.4) the kick and the hat take the strokes as
# before; when it has thinned to nothing (3:09.1, where the handpan comes back) the drum and the cymbals return.
# No stroke is added or moved: 15 strokes of the foot gain a drum; 56 strokes move from the hat to the cymbals.
# MEASURED (the opening, raw, seed 0): the drum's line is within 1.1 cents of the low F; under 60 Hz the opening
# reads 4.8 dB more (the drum alone stands 2.5 dB under what the whole band carries there in 'square'). A cymbal
# left to ring falls 20 dB in 0.32 s, one held shut in 33 ms; on the pulse it stands 6.3 dB over what the hat's
# stroke had from 2 to 16 kHz, between pulses 0.7 under. THE HAIR IS NOT TOUCHED: the strongest slow pulse of each of
# the pair's first four overtones, read in the MIX, is where it was and as deep (within 0.3 dB) with the two new
# instruments sounding: the drum has nothing above 130 Hz and the cymbals nothing below 1.4 kHz.
# NOT KEPT, benched first: the drum under the band too. On the bass's own note its sine adds or cancels by phase
# (under 60 Hz: 'five' 1.5 dB LESS, 'square' 0.0, 'three' +0.7) and the eleven records leave 1 to 2 dB of room.
# THE GREAT DRUM: gain ; the sections it plays in ; ms it rings and the fall's curve (ms curve) ; the note's own sine
# and the head's level, dB (sine:head) ; the head's damping ; brightness ; low-pass (Hz q) ; semitones the stroke
# starts sharp ; the beater's noise, dB ; the share of the gap to the next stroke it is held for ; loudness target
# ("" = unchanged) ; eq bands.
OUTSIDE = "a hair,wider,a quarter,an eighth"
DRUM = os.environ.get("C10T16_DRUM", f"-18dB;{OUTSIDE};1400 1.5;-4:4;0.15;0.6;130 0.7;5;-6;0.92;;hp cutoff=28" if THIRD else "")
# THE FINGER CYMBALS: gain ; pan ; their note, Hz ; the modes of the body and of the shimmer over it, and the
# shimmer's level (body shimmer dB) ; ms an open stroke rings ; a closed one ; brightness ; damping ; the sections ;
# high-pass, Hz ; send to the overheads' room ("" = none) ; dB on the closed stroke. "" = the hat keeps those strokes.
CYMBALS = os.environ.get("C10T16_CYMBALS", f"-13dB;-0.3;2793.82;bell cymbal -12;1500;150;0.8;0.1;{OUTSIDE};1500;;4" if DRUM else "")
GLIDER = "ce-turned-reed"                    # the still reed with a pitch that follows a note's `slide`, in semitones


def turned(f, r0, r1, beats, held):
    """The pair's beat while the sharp reed glides from f + r0 to f + r1 hairs over a note `held` beats long (a
    straight line in semitones, as the engine draws a note's expression): the glide's size in semitones, fitted so
    that `beats` beats hold a whole number of pulses, and a function from a phase in pulses to a time in beats."""
    n = (r0 + r1) / 2 * beats
    assert n.denominator == 1, (r0, r1, beats, n)
    lo, sec, steps = f + float(r0) * HAIR, 60.0 / BPM, 4000

    def phases(size):                        # the beat's phase (pulses) at each of `steps` + 1 points along `beats`
        out, total = [0.0], 0.0
        for i in range(steps):
            mid = (i + 0.5) * beats / steps
            total += (lo * 2 ** (size * min(1.0, mid / held) / 12) - f) * sec * beats / steps
            out.append(total)
        return out

    a, z = 0.0, 2 * 12 * math.log2((f + float(r1) * HAIR) / lo)
    for _ in range(60):                      # the far end that makes the count whole
        size = (a + z) / 2
        a, z = (size, z) if phases(size)[-1] < n else (a, size)
    table = phases(size)

    def when(p):
        if p >= table[-1]:
            return float(beats)
        i = max(j for j in range(steps) if table[j] <= p)
        return (i + (p - table[i]) / (table[i + 1] - table[i])) * beats / steps

    return size, int(n), when


def build():
    ev = defaultdict(list)
    marks = []

    def put(tr, at, pitch, dur, vel, mute=False):
        e = {"at": round(float(at), 5), "len": round(float(dur), 5), "pitch": pitch, "vel": vel}
        if mute:
            e["expr"] = {"pm": 1}
        ev[tr].append(e)

    def kit(tr, at, piece, vel):
        put(tr, at, piece, 0.95 if piece in ("c", "x") else 0.29, vel)

    b = 0                                    # in beats
    for num, (name, r, bars, ground, who) in enumerate(FORM):
        marks.append((name, b, r, bars))
        f = hz(REED + ground)
        # how often the pair is struck again: a bar (two when the pulse is that slow; once when there is no pulse at all)
        span = 4 * bars if not r else 8 if r == Fr(1, 8) else 4
        tail = 4 * SLIDES.get(name, 0)       # v3: beats at the section's end in which the hair glides to the next width
        if tail:
            a = b + 4 * bars - tail
            size, n, when = turned(f, r, FORM[num + 1][1], tail, tail - 0.04)
            put("reed", a, f"{f:.3f}hz", tail - 0.04, 0.8)
            put("hair", a, f"{f + float(r) * HAIR:.3f}hz", tail - 0.04, 0.8)
            ev["hair"][-1].update(patch=GLIDER, expr={"slide": 0.0}, expr_end={"slide": round(size, 6)})
            root = 29 + ground
            for layer, mult in (("k", 1), ("g", 2), ("t", 3), ("h", 4)):
                for j in range(n * mult):
                    at, gap = a + when(Fr(j, mult)), when(Fr(j + 1, mult)) - when(Fr(j, mult))
                    if layer == "k":
                        kit("foot", at, "k", 0.98 if j == 0 else 0.88)
                        put("bass", at, nm(root), gap - 0.1, 0.95 if j == 0 else 0.9)
                    elif layer == "g":
                        for tr in ("left", "right"):
                            if j == 0:       # the bar line's open chord, as every bar of the section begins
                                put(tr, at, f"{nm(root)},{nm(root + 7)},{nm(root + 12)}", gap - 0.08, 0.96)
                            elif j % 2 == 0:
                                put(tr, at, f"{nm(root)},{nm(root + 7)}", gap - 1 / 12, 0.92)
                            else:
                                put(tr, at, nm(root), min(0.3, gap * 0.6), 0.82, mute=True)
                    elif layer == "t":
                        kit("skins", at, ("ft", "t2", "t1")[j % 3], 0.8 if j % 3 == 0 else 0.62)
                    else:
                        kit("hat", at, "h", 0.62 if j % 4 == 0 else 0.42)
            for bar in range(a, a + tail, 4):  # what is not in the rule keeps the bar: the china on its line, the snare on two and four
                kit("brass", bar, "c" if (bar - b) % 16 == 0 else "x", 0.72)
                kit("snare", bar + 1, "s", 0.9)
                kit("snare", bar + 3, "s", 0.95)
        for a in range(b, b + 4 * bars - tail, span):
            put("reed", a, f"{f:.3f}hz", span - 0.04, 0.8)
            put("hair", a, f"{f + float(r) * HAIR:.3f}hz", span - 0.04, 0.8)
            n = r * span                     # pulses of the notes themselves in this span
            if "c" in who and a % 4 == 0:    # the open chord on the bar line
                root = 29 + ground
                for tr in ("left", "right"):
                    put(tr, a, f"{nm(root)},{nm(root + 7)},{nm(root + 12)}", (1 / (2 * float(r)) - 0.08) if r and "g" in who else 7.6, 0.96)
                if not r:
                    put("bass", a, nm(root), 7.6, 0.95)
                kit("brass", a, "c" if a == b or (a - b) % 16 == 0 else "x", 0.86 if a == b else 0.72)
            if not r:
                continue
            for layer, mult in (("k", 1), ("g", 2), ("t", 3), ("h", 4)):
                if layer not in who:
                    continue
                count = n * mult
                assert count.denominator == 1, (name, layer, count)
                for j in range(int(count)):
                    at = a + Fr(span * j, int(count))
                    if layer == "k":
                        kit("foot", at, "k", 0.98 if j == 0 else 0.88)
                        if "g" in who:        # the bass is the notes' own pulse too: it holds from one kick to the next
                            put("bass", at, nm(29 + ground), Fr(span, int(count)) - Fr(1, 10), 0.95 if j == 0 else 0.9)
                    elif layer == "g":
                        if j == 0 and "c" in who and a % 4 == 0:
                            continue          # the chord is there
                        gap = Fr(span, int(count))
                        for tr in ("left", "right"):
                            if j % 2 == 0:    # with the kick: the low string and its fifth, open, cut before the muted stroke
                                put(tr, at, f"{nm(29 + ground)},{nm(36 + ground)}", gap - Fr(1, 12), 0.92)
                            else:
                                put(tr, at, nm(29 + ground), min(Fr(3, 10), gap * Fr(3, 5)), 0.82, mute=True)
                    elif layer == "t":
                        kit("skins", at, ("ft", "t2", "t1")[j % 3], 0.8 if j % 3 == 0 else 0.62)
                    else:
                        kit("hat", at, "h", 0.62 if j % 4 == 0 else 0.42)
            if "s" in who:
                for bar in range(a, a + span, 4):
                    kit("snare", bar + 1, "s", 0.9)
                    kit("snare", bar + 3, "s", 0.95)
        if PAN and name in NAMED and (b < 40 or PAN.split(";")[2]):
            pulse = 1 / r                    # beats
            assert len(NAMED[name]) == r * 4 * bars, name
            for i, which in enumerate(NAMED[name]):
                tr = "pan" if b < 40 else "pan-out"
                for k in which:              # overtone k, k times to the pulse
                    for j in range(k):
                        put(tr, b + i * pulse + Fr(j, k) * pulse, f"{k * f:.3f}hz", min(2, float(pulse) / 2),
                            round(TOUCH[k] + (0.2 if name == "an eighth" else 0), 2))   # three strokes in two bars: firmer
        if PAN and PAN.split(";")[2] and name == "close enough":   # in tune: all four at once
            for k in (1, 2, 3, 4):
                put("pan-out", b, f"{k * f:.3f}hz", 6, round(1.06 - 0.06 * k, 2))
        if THIRD and name in WALK:
            for bar0, held, n in WALK[name]:
                put("third", b + 4 * bar0, f"{f * n / 4:.3f}hz", 4 * held - 0.04, 0.8)
                trims = [float(x) for x in THIRD.split(";")[4].split(",")] if THIRD.split(";")[4] else []
                if len(ev["third"]) <= len(trims) and trims[len(ev["third"]) - 1]:
                    ev["third"][-1]["gain"] = f"{trims[len(ev['third']) - 1]:g}dB"
        b += 4 * bars
    end = b
    # the bass bus's eq follows the ground, as the album's does (its notch and lift sit on the note's first two harmonics)
    key, at, last = [["0b", 0]], 0, 0
    for name, r, bars, ground, who in FORM:
        if ground != last:
            key += [[f"{at - 0.02:g}b", last], [f"{at}b", ground]]
            last = ground
        at += 4 * bars
    keyed = lambda hz_: {"value": hz_, "mod": [{"src": "auto.key", "amount": 0.08333}]}

    def track(name, patch, gain, pan=0, out=None, fx=None, sends=None):
        tr = dict(name=name, patch=patch, gain=gain, pan=pan, notes=sorted(ev[name], key=lambda e: (e["at"], str(e["pitch"]))))
        if out:
            tr["out"] = out
        if sends:
            tr["sends"] = sends
        if fx:
            tr["fx"] = fx
        return tr

    # THE BAND IS THE ALBUM'S (Common Time's kit staging, bass bus and guitar bus, as In the Time Of carries them).
    # What is this song's own is the pair: two harmoniums, close together in the middle so that they beat in the
    # air of one place and not between two ears.
    palm = " synth.layers.0.mute=expr.pm*0.56 synth.layers.0.mute_width=0.10"
    toms, tuned = [], {}
    if TOMS:
        # each ground's strokes go to that ground's drums: the same three pieces, the same fader, the same bus
        spans, at = [], 0
        for name, r, bars, ground, who in FORM:
            spans.append((at, at + 4 * bars, ground))
            at += 4 * bars
        sets = {int(k): v.split(",") for k, v in (x.split("=") for x in TOMS.split(";"))}
        strokes = ev.pop("skins")
        for ground, (low, middle, top) in sets.items():
            tr = "skins" if ground == 0 else "skins-" + low.lower()
            ev[tr] = [e for e in strokes if any(a <= e["at"] < z and g == ground for a, z, g in spans)]
            tuned["ce-toms-" + low.lower()] = {"about": f"chirper-alpha: the album kit with its three counting toms on {low}, {middle} and {top}",
                                               "extends": "ct-kit", "kit": {"ft": {"pitch": low}, "t2": {"pitch": middle}, "t1": {"pitch": top}}}
            toms.append(track(tr, "ce-toms-" + low.lower(), "-3dB", 0, "drums", TOMS_EQ))
        assert sum(len(t["notes"]) for t in toms) == len(strokes) and all(t["notes"] for t in toms)
    mid = [{"type": "eq", "bands": ["peak cutoff=700 q=0.9 gain=2.5dB"]}]
    air = [{"type": "eq", "bands": ["highshelf cutoff=9000 gain=-2dB"]}]
    tracks = [
        # (their body cut 6 dB at 300 Hz: against the eleven records the band with the pair read 3 to 4 dB over at 120-500 Hz,
        # and of 250-500 Hz the pair was the largest part)
        # ONE STILL REED EACH. The library harmonium beats with itself (a second reed 7 cents sharp: 0.7 times a second
        # at F3, twice that an octave up) and its bellows tremble at 1.3 Hz: three slow pulses that are not in tempo,
        # under the one that is. Here the second reed is in unison and the bellows are steady, so the only wobble in
        # the song is the hair.
        track("reed", STILL, "-9.5dB", -0.12, fx=[{"type": "eq", "bands": ["peak cutoff=300 q=0.8 gain=-6dB"]}]),
        track("hair", STILL, "-9.5dB", 0.12, fx=[{"type": "eq", "bands": ["peak cutoff=300 q=0.8 gain=-6dB"]}]),
        track("left", "ct-twin fx.2.cone=37" + palm, "0.5dB", -0.92, "strings", mid),
        track("right", "ct-twin fx.2.cone=41" + palm, "0.5dB", 0.92, "strings", mid),
        # the bass holds its notes here (on the other songs it chugs): half of 120-250 Hz was its overtones
        track("bass", "ct-bass", "0.5dB", 0, "low", [{"type": "eq", "bands": ["peak cutoff=180 q=1 gain=-3dB"]}]),
        track("foot", "ct-kit", "3.5dB", 0, "drums", [{"type": "eq", "bands": ["peak cutoff=4500 q=0.8 gain=10dB"]}]),
        track("snare", "ct-kit", "3.5dB", 0, "drums", [{"type": "eq", "bands": ["highshelf cutoff=7000 gain=-3dB"]}], {"oh": "-1.5dB"}),
        *(toms if TOMS else [track("skins", "ct-kit", "-3dB", 0, "drums")]),      # at 1.5 dB they were half of everything from 60 to 500 Hz
        track("hat", "ct-kit", "16dB", -0.3, "drums", air, {"oh": "4.5dB"}),
        track("brass", "ct-kit", "-2.5dB", 0.2, "drums", air, {"oh": "4.5dB"}),
    ]
    if PAN:
        patch, opens, closes, _ = PAN.split(";")
        tracks += [track("pan", patch, opens, 0.0)] + ([track("pan-out", patch, closes, 0.0)] if closes else [])
    if THIRD:
        tracks += [track("third", STILL, THIRD.split(";")[0], float(THIRD.split(";")[1]), fx=[{"type": "eq", "bands": THIRD.split(";")[3].split("|")}])]
    buses = {
        "strings": {"fx": [{"type": "eq", "bands": ["peak cutoff=330 q=1.2 gain=-2dB"]}, "reverb kind=room decay=0.35s mix=0.06 predelay=6ms"]},
        "drums": {"fx": ["reverb kind=room decay=0.7s mix=0.1 predelay=8ms",
                         {"type": "glue", "threshold": "-24dB", "ratio": 2.5, "attack": "20ms", "release": "140ms", "knee": 6.0},
                         "clip drive=0dB ceiling=-13dB",
                         {"type": "eq", "bands": ["peak cutoff=400 q=0.8 gain=-6dB", "peak cutoff=5500 q=0.9 gain=1dB",
                                                  "highshelf cutoff=9000 gain=-2dB", "lp cutoff=14250 q=0.8"]}]},
        "oh": {"fx": ["reverb kind=room decay=0.7s mix=1 predelay=4ms low_cut=5000 high_cut=12000 spread=0.6",
                      {"type": "eq", "bands": ["lp cutoff=14250 q=0.8"]}]},
        "low": {"fx": [{"type": "eq", "bands": [{"kind": "peak", "cutoff": keyed(44), "q": 1.5, "gain": "-7dB"},
                                                {"kind": "peak", "cutoff": keyed(90), "q": 1.0, "gain": "7.5dB"},
                                                {"kind": "peak", "cutoff": 350, "q": 1.0, "gain": "-8dB"},
                                                {"kind": "peak", "cutoff": 1500, "q": 1.0, "gain": "4dB"}]},
                       {"type": "compressor", "threshold": "-26dB", "ratio": 8.0, "attack": "12ms", "release": "120ms", "makeup": "2.5dB"},
                       {"type": "eq", "bands": [{"kind": "peak", "cutoff": keyed(170), "q": 1.2, "gain": "-3dB"}]}],
                "auto": {"key": {"points": key, "curve": 0}}},
    }
    doc = dict(
        about=("Close Enough: chirpers, Common Time, track sixteen (chirper-two). Two harmoniums hold one note a hair apart; "
               "the hair is as wide in cycles as the tempo is in beats, so the pair pulses in time, and each overtone pulses twice, "
               "three times, four times as fast. The band plays those pulses. The metre is a tuning; the snare keeps four."),
        tempo=BPM, seed=1, length=f"{end:g}b", tail="5s", ceiling="-1dB", loudness=float(PAN.split(";")[3]) if PAN else -10, event_stable=True,
        buses=buses, master={"fx": [{"type": "eq", "bands": ["hp cutoff=24"]}]}, tracks=tracks,
        **({"patches": {GLIDER: {"about": "chirper-three: Close Enough's still reed (one harmonium reed, steady bellows) with a pitch that follows a note's `slide`, in semitones: the peg being turned",
                                 "extends": STILL, "synth": {"pitch": {"value": 0, "mod": [{"src": "expr.slide", "amount": 1}]}}}}} if SLIDES else {}))
    if tuned:
        doc["patches"] = {**doc.get("patches", {}), **tuned}
    if THIRD and THIRD.split(";")[2]:
        doc["loudness"] = float(THIRD.split(";")[2])
    if DRUM:
        great_drum(doc)
    if CYMBALS:
        finger_cymbals(doc)
    return doc, marks, end


def spans_of(names):
    out, at = [], 0
    for name, r, bars, ground, who in FORM:
        if name in names.split(","):
            out.append((at, at + 4 * bars, ground))
        at += 4 * bars
    return out


def great_drum(doc):
    """Under every stroke of the foot where the band is not playing: a big drum on the ground's own note, rung until
    just before the next stroke."""
    gain, where, ring, levels, damp, bright, lp, drop, beater, share, target, eq = DRUM.split(";")
    sine, head = levels.split(":")
    spans = spans_of(where)
    foot = sorted((n for n in next(t for t in doc["tracks"] if t["name"] == "foot")["notes"] if n["pitch"] == "k"), key=lambda n: n["at"])
    notes = []
    for n, nxt in zip(foot, foot[1:] + [None]):
        ground = next((g for a, z, g in spans if a <= n["at"] < z), None)
        if ground is None:
            continue
        gap = (nxt["at"] - n["at"]) if nxt else 4.0
        notes.append({"at": n["at"], "len": round(min(gap, 4.0) * float(share), 5), "pitch": nm(29 + ground), "vel": n["vel"]})
    doc.setdefault("patches", {})["ce-great-drum"] = {
        "about": ("Close Enough's great drum (chirper-two, 19 Nov): a bass drum that takes a pitch. A sine on the note, starting sharp and "
                  "settling as the head gives; a damped membrane over it; a soft beater. Nothing above the low-pass: it stays under the reeds."),
        "synth": {
            "amp": {"a": "1ms", "d": f"{ring.split()[0]}ms", "s": 0, "r": "70ms", "curve": float(ring.split()[1])},
            "env": {"p": {"a": "0.3ms", "d": "50ms", "s": 0}, "s": {"a": "0.3ms", "d": "12ms", "s": 0}},
            "layers": [{"wave": "sine", "level": f"{sine}dB"},
                       {"type": "modal", "modes": "membrane", "decay": f"{float(ring.split()[0]) / 1000:g}s", "damp": float(damp), "bright": float(bright),
                        "strike": 0.4, "level": f"{head}dB"},
                       {"type": "noise", "color": "pink", "level": {"value": "-60dB", "mod": [{"src": "env.s", "amount": 60 + float(beater)}]}}],
            "filters": [f"lp cutoff={lp.split()[0]} q={lp.split()[1]}"],
            "pitch": {"value": 0, "mod": [{"src": "env.p", "amount": float(drop)}]}},
        "play": {"vel_sens": 0.5}}
    doc["tracks"].append({"name": "drum", "patch": "ce-great-drum", "gain": gain, "pan": 0, "notes": notes,
                          **({"fx": [{"type": "eq", "bands": eq.split("|")}]} if eq else {})})
    if target:
        doc["loudness"] = float(target)


def finger_cymbals(doc):
    """Where the band is not playing, the hat's strokes (the fours) are a pair of finger cymbals: open on the pulse,
    closed between. No stroke is added or moved."""
    gain, pan, note, modes, ring, shut, bright, damp, where, hp, oh, lift = CYMBALS.split(";")
    spans = spans_of(where)
    hat = next(t for t in doc["tracks"] if t["name"] == "hat")
    inside = lambda n: any(a <= n["at"] < z for a, z, g in spans)
    moved = [n for n in hat["notes"] if inside(n)]
    assert moved and all(n["pitch"] == "h" for n in moved)
    hat["notes"] = [n for n in hat["notes"] if not inside(n)]
    loud = max(n["vel"] for n in moved)                      # the hat's stroke on the pulse is its loudest
    piece = lambda ms, db=0: {"gain": f"{db:g}dB", "pitch": f"{float(note):.3f}hz", "patch": {"synth": {
        "amp": {"a": "0.2ms", "d": f"{ms}ms", "s": 0, "r": "40ms"},
        "layers": [{"type": "modal", "modes": modes.split()[0], "decay": f"{float(ms) / 1000:g}s", "damp": float(damp), "bright": float(bright), "strike": 0.7},
                   {"type": "modal", "modes": modes.split()[1], "decay": f"{float(ms) / 2000:g}s", "damp": float(damp), "bright": 1.0, "strike": 0.9,
                    "level": f"{modes.split()[2]}dB"}],
        "filters": [f"hp cutoff={hp}"]}}}
    doc.setdefault("patches", {})["ce-finger-cymbals"] = {
        "about": ("Close Enough's finger cymbals (chirper-two, 19 Nov): the small brass pair that keeps time beside a harmonium. "
                  "`o` struck and left to ring, `c` struck and held shut."),
        "kit": {"o": piece(ring), "c": piece(shut, float(lift))}, "play": {"humanize": {"time": "4ms", "vel": 0.06}, "vel_sens": 0.6}}
    doc["tracks"].append({"name": "cymbals", "patch": "ce-finger-cymbals", "gain": gain, "pan": float(pan),
                          **({"sends": {"oh": oh}} if oh else {}),
                          "notes": [{**n, "pitch": "o" if n["vel"] == loud else "c"} for n in moved]})


def dump(doc):
    return "\n".join("tracks:\n" + "\n".join("  - " + json.dumps(tr) for tr in v) if k == "tracks" else k + ": " + json.dumps(v)
                     for k, v in doc.items()) + "\n"


if __name__ == "__main__":
    doc, marks, end = build()
    if os.environ.get("C10T16_SHOW"):
        sec = lambda t: f"{int(t * 60 / BPM // 60)}:{t * 60 / BPM % 60:04.1f}"
        for name, b, r, bars in marks:
            print(f"{name:14s} bar {b // 4 + 1:3d}  {sec(b)}  the hair {float(r) * HAIR:5.3f} Hz ({r} of a pulse to the beat), {bars} bars: "
                  f"to the bar, kick {r * 4}, guitars {r * 8}, toms {r * 12}, hat {r * 16}")
        print(f"end {sec(end)}  ({end // 4} bars)")
    else:
        with open(OUT, "w") as f:
            f.write(dump(doc))
