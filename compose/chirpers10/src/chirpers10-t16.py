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

(Since v8 the hair is never moved in a step: between these widths the peg is turned, and the band follows the
pair's swell as it quickens or slows. See PEG below.)

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
# v7 (chirper-one, whole song): THE GUITARS TAKE SIDES. v1's first want, open through six versions: "the cell has no
# tune and the guitars say only its twos: one guitar could say the whole cell". Inside each kick is one cell, two
# against three against four; the guitars had the twos (open with the kick, a muted stroke half way), the toms the
# threes, the hat the fours. So through two and a half minutes of band the album's two guitars played the plainest
# part in the song. Now each guitar also says one of the other numbers, on the low string, muted, with the drum
# that has it, and the song's sections differ in who says what:
#   square        the twos, both guitars, as written: the rule stated
#   five          the LEFT guitar takes the threes as well (with the toms): 0, 1/3, 1/2, 2/3 of each pulse
#   seven         and the RIGHT takes the fours (with the hat): 0, 1/4, 1/2, 3/4. Three against four, left against
#                 right, meeting on the kick and half way
#   three         the slow one, on the lowest ground: BOTH say the WHOLE cell together: 0, 1/4, 1/3, 1/2, 2/3, 3/4.
#                 It is the song's one unison riff, at the width where its closest strokes are still a tenth of a
#                 second apart
#   square again  the sides again, now in common time
#   the close     the twos, as written, and then nothing
# No new sound and no new time: every stroke added is on a stroke a drum already plays. The open chord with the
# kick is let go a little sooner, before that guitar's next stroke. The glide of v3 (five's last two bars) carries
# the left guitar's threes with it: they are solved from the same phase as everything else.
# THE PAIR KEEPS ITS LINE. The reeds' note is the fourth harmonic of the guitars' low string, and every added stroke
# is that string, muted: benched, the first take left the pair's own line 1.0 to 1.8 dB less clear of the band at
# its note (a third of an octave round it: +5.1, +5.5, +4.5, +5.2 dB over everything else in five, seven, three and
# square again; then +4.1, +3.9, +2.7, +3.8). The song is about that line. So the added strokes are on tracks of
# their own (the same guitars, rigs, faders and sides) with one narrow cut at the reeds' note, which follows the
# ground as the bass's eq does. The strokes the guitars already had are not touched by it.
# section=left:right (the overtones each guitar says), ... ; the added strokes' velocity ; the loudness target
# ("" = unchanged) ; the cut at the reeds' note on the added strokes, q:dB ("" = none, and they stay on the
# guitars' own tracks). "" = v6 byte for byte.
SIDES = os.environ.get("C10T16_SIDES", "five=23:2,seven=23:24,three=234:234,square again=23:24;0.78;-9.861;3:-6" if CYMBALS else "")
ALSO = "-said" if SIDES and SIDES.split(";")[3] else ""     # where the added strokes go
SAID = {x.split("=")[0]: tuple(x.split("=")[1].split(":")) for x in SIDES.split(";")[0].split(",")} if SIDES else {}
# v8 (chirper-two, whole song): ONE HAND ON THE PEG. v1's second want, and v3's unfinished one: "every change of
# width was a cut at a bar line, and tuning is not done in cuts". v3 turned the peg once, for two bars (five into
# seven). Nine changes of width were still cuts: the opening went in two steps and the close in three, as if the
# tuner let go of the peg and took it up again somewhere else. Now the hair's width is ONE LINE through the whole
# song, with no step in it anywhere:
#   in tune       still (0:00)
#   THE OPENING   one turn, eight bars (0:07.3-0:36.4): the hair opens from nothing to one pulse a beat. The pair is
#                 struck once and its swell quickens under the hand: 7.3 seconds to the first return, then 3.0,
#                 2.3, 1.9 ... 0.92, and the sixteenth swell IS the band's first beat. Kick, great drum, cymbals,
#                 toms and handpan fall where the swell does, so the song begins as one long accelerando that
#                 nobody counts, into a tempo that was there all along (the snare, from 0:21.8, keeps it)
#   square        six bars, then two in which it quickens into five (nine pulses for eight)
#   five          six bars, then v3's two into seven
#   seven         six bars, then two in which it SLOWS into three (ten pulses for fourteen: 0.53 s apart to 1.10)
#   three         six bars, then two in which it quickens back to square (seven pulses for six)
#   square again  eight bars
#   THE CLOSE     one turn, six bars (3:01.8-3:23.6): the hair closes from one pulse a beat to nothing. Twelve
#                 pulses, each further from the last (0.93 s, 0.97 ... 2.0, 2.6, and 6.3 to the last chord), the
#                 toms and snare leaving at 3:09.1 and the hat at 3:16.4 as before. The song ends as tuning ends:
#                 the peg is turned until the wobble slows, and stops
# 22 of the 58 bars are turned now (2 before). Nothing new plays: the strokes are solved from the pair's phase, as
# v3's are (the integral of the hair's width; a stroke where it is whole, the guitars' at halves, the toms' at
# thirds, the hat's at quarters), who plays a pulse is who played the section it begins in, the handpan says and
# listens in v2's order a pulse at a time, and the snare and china keep the bar. The third reed is not touched.
# MEASURED (the pair alone, raw: the swell of its fundamental against the written kicks): the opening's fifteen
# within 11 ms (median 5); into five within 6; into three within 19; out of three within 6; the close's eleven
# within 13 (median 5). v3's own two bars read up to 37 ms and are not touched.
# AND THE PAIR'S ROOM NO LONGER FILLS THE SWELL (AIR). Found while measuring the turns: each reed carried the
# library harmonium's own room (1.3 s, a fifth of the signal), and a room rings on through the moment the two reeds
# cancel. Alone, the swell's depth (how far the pair falls between pulses; overtones 1 to 4, both ears summed) read
# 34, 20, 17, 17 dB in 'square', 16, 23, 27, 19 in 'five' and 19, 21, 17, 19 in 'seven', and in the left ear as
# little as 11; with no room at all it is 30 to 35 everywhere. The same room at a third of the level (0.06) gives
# 35, 26, 27, 28 / 25, 32, 32, 28 / 27, 28, 25, 28 (the left ear 18 to 30), and the reeds' faders come down 0.5 dB,
# which is what the room had taken (the pair alone within 0.1 dB of v7, K). Eleven of the twelve readings are 5 to
# 11 dB deeper (the twelfth, the first overtone in 'square', was 34 already).
# the long turns: sections+sections=width at the start>width at the end, ... ; further two-bar turns, as SLIDE ;
# the loudness target ("" = unchanged). "" = v7.
PEG = os.environ.get("C10T16_PEG", "a hair+wider=0>1,a half+a quarter+an eighth=1>0;square:2,seven:2,three:2;-9.821" if SIDES else "")
RAMPS, RAMPED = {}, {}
if PEG:
    for x in filter(None, PEG.split(";")[0].split(",")):
        RAMPS[x.split("=")[0].split("+")[0]] = (tuple(x.split("=")[0].split("+")), Fr(x.split("=")[1].split(">")[0]), Fr(x.split("=")[1].split(">")[1]))
        RAMPED.update({n: x.split("=")[0].split("+")[0] for n in x.split("=")[0].split("+")})
    SLIDES = {**SLIDES, **{x.split(":")[0]: int(x.split(":")[1]) for x in filter(None, PEG.split(";")[1].split(","))}}
# THE PAIR'S ROOM: how much of the reeds' own room is heard (the library's is 0.2) ; dB on the two reeds' faders,
# which is what the room took from their level. "" = as v7.
AIR = os.environ.get("C10T16_AIR", "0.06;-0.5" if PEG else "")
PAIR = STILL + (f" fx.1.mix={AIR.split(';')[0]}" if AIR else "")
# v9 (chirper-one; instrument round: THE BASS SAYS ITS OWN NOTE). The song is one note, and what the band stands on
# is the bass holding it (here it holds; on the other songs it chugs). Read alone, on low F the bass's loudest
# partial was not the F but the twelfth, the C at 131 Hz: the fundamental 2.6 dB under it and the octave 2.1. On
# the low E flat of 'three' the twelfth (B flat) stood 6.5 dB over both. So where the ground is lowest the bass
# hummed the fifth of its note. That is the album chain's octave lift (7.5 dB at 90 Hz, q 1): at q 1 it lifts the
# twelfth nearly as much as the octave. (Not read on the other songs, where the bass chugs.) Against
# the records the same thing read as the wrong band: the bass 2.7 dB under their basses at 60-120 Hz and 6.7 over
# at 120-250, where it held 44% of a mix that stood 3.2 over, the band the two reeds' own note is in.
# Now the lift is ON the octave and narrow (87.3 Hz on F, q 1.6, 9.5 dB) and the twelfth has a dip of its own (q 2,
# -6 dB); both follow the ground as the chain's other bands do. The fader comes up 1 dB, which is what the bass
# lost on B, where nothing was wrong. The octave is the loudest partial on F and on E flat; on A flat and B the
# fundamental is, as it was. Nothing else in the chain moves and no note changes.
# the octave's lift: Hz on F : q : dB ; the dip on the twelfth: Hz on F : q : dB (both follow the ground) ; the
# bass's fader, dB ; the loudness target (fitted so the opening, which has no bass, is at v8's gain). "" = v8.
BASS = os.environ.get("C10T16_BASS", "87.3:1.6:9.5;131:2:-6;1.5;-9.91" if AIR else "")
# v10 (chirper-zero, palette: the part the song lacked, on an instrument no other song has): THE UNISON BEND.
# The song says what a tuner does: turn the peg until the wobble slows, and stops. Every guitarist does that with
# the left hand too: hold a note on one string, bend the string beside it up to the same note, and listen to the
# two of them wobble slower and slower until they are one. A unison bend is this whole song in one gesture, and the
# band had no lead guitar to make it.
# So there is one now, and its rule is the song's: THE LEAD PLAYS ONLY WHILE THE PEG IS TURNED, and what it plays
# is the pair, an octave up, on two strings through one amplifier. One string holds twice the still reed. The
# other is written as twice the hair, with the hair's own slide, so the two are a hair apart at the octave and
# their wobble is the pair's second overtone exactly: twice to the pulse, the guitars' own number, quickening and
# slowing as the peg turns. Through an amplifier a wobble is less a swell in loudness than a slow wah: the note's
# own line falls 25 to 35 dB twice a pulse and the tone thins to its octave and fills again, while the lead's
# loudness moves 5 dB (K-weighted, the middle 90% of the close).
#   the four turns between sections (two bars each: 0:58.2, 1:27.3, 1:56.4, 2:25.5)   the lead holds the pair's
#       note of that ground while the band quickens or slows under it, and stops at the bar line where the ground
#       changes and the new width begins
#   THE CLOSE (3:01.8-3:23.6)   struck ONCE where the last turn begins, and held: twenty-two seconds of one bend,
#       the wobble coming further apart with the band's strokes
#   the last chord (3:23.6)     the bend has arrived: the lead lets go as the chord is struck, and the chord is the
#       band's, as it was. (Benched with the lead holding the unison through it: the chord's own line at 349 Hz then
#       wobbled 15.5 dB where it wobbles 5.5 without the lead, because the band's strings are not on the reeds' note:
#       the guitars' open strings read 2.6 cents sharp of it and wander 3 either side, stroke by stroke. With the
#       strings put on their notes it was 8.7. So that is the next round's, not this one's: see the round note.)
# It is a new patch of the song's own, `ce-bend`: the library's fluid lead (`m8-lead`, which no song on the record
# uses) as ONE saw: its detuned second oscillator, its vibrato, its echo and its room all wobble or smear and are
# out; then the album's lead amplifier at half gain and the engine's cabinet. A plucked string was benched first
# (the album's lead rig, also with `tune_sounding` and no variation) and cannot do this: the lows of its own line
# fell at 0.50, 0.88, 0.54, 0.82, 0.15, 0.31 of the half pulse, where a steady wobble falls at the same place every
# time, and with BOTH strings on the same note its line still swung 18 to 23 dB (a plucked string's two planes
# beat with each other, so it is never still). The oscillator's lows fall at 0.49 to 0.53 and in tune its line
# moves 0.2 dB. It is on its note (read: within 0.02 cent of the written line through the whole close), provided
# the patch plays each note to its end: at the engine's default gate a note's slide finishes at 95% of its length,
# and the lead reached the unison a second early (read: 0.5 cent flat of the line at 20 s, its wobble a third of
# a turn behind the pair's by 3:13).
# MEASURED (raw, the lead alone against the pair alone): through the close the lead's own line is lowest where
# the pair's second overtone is lowest, within 51 ms (median 8) over the 22 lows; in the turn out of seven, within
# 19 ms (median 12) over 20.
# which turned notes: 'all', or 'close' (the last turn only) ; the lead's fader ; its filter, Hz
# ; the amplifier's gain ; dB before the amplifier ; the cabinet's cone ; attack, ms ; the loudness target ; the
# track's eq, Hz:q:dB,... (a held note at 311 to 494 Hz is mostly its own first line: at -12 dB with no eq the lead
# was 52 to 57% of the mix's whole 250-500 Hz band wherever it played; the eq takes 4 dB off that line, 5 off
# 700 Hz, where the mix already stood 3.7 over the records in the close, and gives 4 back at 2.2 kHz, where a lead
# is heard: 24 to 30% of 250-500 Hz now, 15 to 20% of 2-4 kHz). "" = v9.
BEND = os.environ.get("C10T16_BEND", "all;-11.5dB;1200;0.5;-20;45;60;-9.851;380:0.8:-4,700:1:-5,2200:0.7:4" if BASS else "")
# v11 (chirper-zero; section round: the ending, 2:54-3:31, and one repair of v10): THE NOTE IS LEFT ALONE.
# The song is a tuning, and it ends when the two reeds are one note. That note was never heard by itself: the
# band's last chord lay over it for 6.7 of its 8 beats, 5 dB louder, and a held chord through an amplifier is not
# still (at the reeds' own lines the last bar wobbled 4.0 dB at 349 Hz, 14.4 at 524, 8.7 at 1048; the two reeds
# alone 2.9, 0.5, 0.1). Three things, the first two in the ending only:
#   THE BAND LETS GO AT THE BAR LINE (3:27.3). The last chord is struck by everyone as before, held ONE bar, and
#       let go together; for the last bar (3.6 s) the two reeds are alone, in tune and still. Guitars and bass
#       only; the handpan's four notes and the crash ring as they did.
#   THE BAND IS ON THE REEDS' NOTE. Read against the still reed (the sixteenth harmonic of low F, the 33 open
#       strokes from 0:36 to 1:05), the guitars sounded 2.6 cents sharp and wandered from -0.7 to +5.5 stroke by
#       stroke (the plucked string's own sharpness, and the rig's random pitch); the bass +0.8 (-1.6 to +2.7).
#       Now the strings are on their written notes (the engine's `tune_sounding`) and nothing is random: -0.5
#       (-1.1 to +0.5) and +0.1 (-0.3 to +0.9). And every chord's fifth is the reeds' own twelfth, 3:2 of its root
#       (an equal-tempered fifth is 2 cents flat of it, which is 0.6 Hz at 524 Hz: a wobble nobody wrote, in a
#       song whose wobbles are all written). In the last chord's first bar the mix's line at 349 Hz wobbles 2.1 dB
#       where it wobbled 7.7, at 698 Hz 7.7 where 13.0. This is for the whole song and is small anywhere but
#       there (the pair's swell through 'square' is followed as before, 0.68 > 0.70).
#   THE LEAD NO LONGER CANCELS THE NOTE IT DOUBLES (a repair of my v10). Its still string is the reeds' second
#       overtone, the same frequency, and in this engine both start their cycle on the note's first sample: I
#       read each alone and never the sum. Summed, they were 158 to 173 degrees apart on F and E flat and nearly
#       the same size: the line they share came out 7.7 to 11.1 dB BELOW the reeds' alone (turn 1, turn 4, the
#       close; -1.7 on A flat, +0.7 on B), and through the close the mix followed the pair's swell at 349 Hz
#       WORSE than before there was a lead (r 0.41 at v9, 0.07 at v10). The lead's oscillator now starts half a
#       cycle on, which turns its odd harmonics over and leaves the even ones (its second and the reeds' fourth
#       already added). The shared line is 3.2 to 4.7 dB ABOVE the reeds' alone in all five places; the close
#       reads r 0.52 and the first turn 0.91 (0.26). After ANY change to the lead's chain (its filter, amp,
#       cabinet, eq) run phase.py again.
#       AND ITS OWN NOTE COMES DOWN 5 dB (the cut at 380 Hz, 4 -> 9 dB): two parts that add on one line are louder
#       than either. With the two adding and v10's eq the mix stood 5.5 dB over the records at 250-500 Hz in the
#       close (3.6 at v9, before the lead; the 2.5 I reported at v10 was the cancellation); now 4.6, and the
#       lead's own line is 4 dB under the reeds' overtone it doubles.
# patch overrides for the four guitars ; for the bass ; fifths as 3:2 ('1', or '' = as written) ; how long the
# guitars and bass hold the last chord, beats as written ('' = as it was, 7.6; they sound 0.88 of it) ; the
# lead's oscillator ('' = as v10) ; the lead's eq, Hz:q:dB,... ('' = as v10) ; the loudness target. "" = v10.
ALONE = os.environ.get("C10T16_ALONE", "synth.layers.0.tune_sounding=true synth.pitch.mod.1.amount=0;synth.pitch.mod.1.amount=0;1;4.5;saw phase=0.5;"
                                       "380:0.8:-9,700:1:-5,2200:0.7:4;-9.891" if BEND else "")
# v12 (chirper-two; instrument round: the hi-hat; no note changes): THE HAT HAS A BODY.
#   The closed hat plays 763 strokes here, sixteen to the bar in the squares and twenty-eight in 'seven', and it is
#   the library's `haake-hat`: white noise (and three squares) through an 8 kHz high-pass, 45 ms. Read alone it
#   had nothing under 8 kHz to speak of: its 4-8 kHz stood 2.3 dB UNDER its 8-16 kHz and its 2-4 kHz 11 under
#   that. A hiss, with no metal under it. The eleven records' drum stems all carry 4.7 to 7.4 dB MORE at 4-8 kHz
#   than at 8-16 (median 5.9); this kit carried 2.4 to 2.7 more, and the hat is all but the whole of the kit's
#   top octave. The read by part said the same (the kit against the records' drums: 4-8 kHz -2.1 and -1.8 in
#   'square' and 'seven', 8-16 kHz +1.4), and so did the mix, 1.3 to 1.8 dB short at 4-8 kHz in every band
#   section, which every read of this song since v1 has listed.
#   WHAT CHANGED, the hat only (the crash and china keep the album kit): a kit of the song's own, `ce-hat-kit`,
#   whose closed hat is opened downwards (the high-pass 8 kHz -> 4.5 kHz) and shortened (45 -> 35 ms); on its
#   track a peak at 6 kHz (q 0.8, +4 dB) and a deeper shelf over 9 kHz (-2 -> -4 dB), so the body comes up and
#   the hiss does not; less of the overheads' room (send 4.5 -> 2.5 dB), which is where a tick becomes a wash;
#   the fader 16 -> 17 dB.
#   MEASURED, the hat alone (raw, seed 0, six bars of 'square' and of 'seven'): 4-8 kHz +5.2 dB, 2-4 kHz +9.5,
#   8-16 kHz as it was (0.0 / -0.2); its 4-8 kHz now 3.0 dB OVER its 8-16. As a tick: the share of the time it is
#   within 12 dB of its strokes' peaks 21 -> 16 % and 25 -> 21 %. In the band: a stroke's first 30 ms above 3 kHz
#   against everything else there, -1.7 -> +1.6 dB (soft strokes, 'square') and -5.2 -> -2.8 (accents, which
#   fall with the kick and guitars). The kit's 4-8 kHz over its 8-16: 2.4 -> 4.4 and 2.7 -> 4.7.
#   THE MIX AGAINST THE RECORDS (stembal, the six windows on record), 4-8 kHz: square -1.3 -> -0.2, five -1.4 ->
#   -0.2, seven -1.8 -> -0.5, three -1.6 -> -0.7, square again -1.8 -> -0.5, the close -3.2 -> -2.6; 8-16 kHz
#   reads 0.1 to 0.2 lower and no other band moves more than 0.1. As mastered (three seeds): 4-8 kHz +1.0 to +1.4 dB in the band sections, 8-16 kHz
#   -0.2 to -0.3. The target -9.891 -> -9.861 keeps the stretches with no hat within 0.01 dB of v11.
# overrides on the library's closed hat (haake-hat) ; the hat track's fader ; its send to the overheads' room ;
# its eq, band,band ; the loudness target ("" = unchanged). "" = v11 byte for byte.
HAT = os.environ.get("C10T16_HAT", "filters.0.cutoff.value=4.5k amp.d=35ms;17dB;2.5dB;highshelf cutoff=9000 gain=-4dB,peak cutoff=6000 q=0.8 gain=4dB;-9.861" if ALONE else "")
# v13 (chirper-zero; instrument round: the counting toms, all 609 strokes; no stroke moves): THE TOMS COUNT. They
# play twelve to the bar on the ground's own notes, a stroke every 0.3 s round three drums, and they are the
# album's tom with its 1.3 s head: when the next stroke landed the last had fallen 10 dB, so the three rang as one
# low chord with a ripple on it, and in the band a tom stroke alone on its tick raised the mix by 1.1 dB at
# 100-400 Hz (a quarter of them by nothing). chirper-two's v12 handoff named the round: shorter, and a cut for
# their box.
#   SHORTER AND LOUDER: the head's decay 1.3 -> 0.6 s and the amp's 1.8 -> 0.8 s (a stroke is 24 dB down when the
#       next lands), the fader -3 -> 0 dB: the weight goes into the stroke and not the ring.
#   THE BOX OUT, THE NOTE IN: their cut at 330 Hz 3 -> 6 dB, and 5 dB at 75 Hz, where the heads' own notes are (C2,
#       F2 and their fellows in the other keys): shortened alone, the toms took 0.1 dB from the one band this song
#       is shortest in, 60-120 Hz, which their ring had been helping to hold.
# A tom stroke alone on its tick now raises the mix 2.9 dB at 100-400 Hz, and three in four of them by 1.8 or more.
# By part the kit against the records' kits: 250-500 Hz +4.1 -> +2.7, 60-120 Hz -0.9 -> +0.5. The mix: 60-120 Hz 0.3 to 0.5 nearer in every
# band section, all nine bands 1.522 -> 1.372.
# overrides inside each tom's patch ; the tom tracks' fader ; their eq, band,band ; the loudness target. "" = v12.
STROKE = os.environ.get("C10T16_STROKE", "synth.layers.0.decay=0.6s synth.amp.d=0.8s;0dB;peak cutoff=330 q=1 gain=-6dB,peak cutoff=75 q=0.9 gain=5dB;-9.87" if HAT else "")
# v14 (chirper-one; section round, w6, 2:25-2:54): THE HANDPAN NAMES THE FIVE. The rule gives the band four pulses:
# the kick has the pair's own, the guitars the second overtone's, the toms the third's, the hat the fourth's. The
# handpan says them as notes, the pair's own series: as the hair opens it names one and two, then three, then four
# (F3, F4, C5, F5), and it has been silent since the band came in. The series does not stop at four. The pair's
# FIFTH overtone pulses five times to the pulse, and nobody plays it. When the band comes back to common time
# ('square again': the same eight bars as 'square') the handpan comes back inside the band, for the first time, and
# names the next one: A5, five times the still reed (873.07 Hz), five strokes to the pulse, each where that overtone
# swells. It is the song's first major third on F (the series' own, 14 cents under the piano's), and with it the
# cell inside each kick is two against three against four against FIVE. It comes as it came at the top: said, then
# left to the pair: two bars without it, two with the five on the bar's first pulse, two on the first and third,
# two on every pulse; and when the peg begins to close it is the first to go, as the fours are first in the close.
# Its strokes are high-passed: the handpan's shell (on F2 in this song) would otherwise thump under every one.
# AND THEY ARE STOPPED. The handpan rings five seconds and sits in a three-second hall: at five and a half strokes a
# second on one note the first build was a drone whose level wandered 12 dB from stroke to stroke as the tails
# added and cancelled (read alone), not five strokes. So each stroke is damped by the next finger, as a player
# re-striking one field does: a short decay, a 50 ms release, and a tenth of the hall.
# the section ; for each of its bars the pulses of that bar on which the five is said (digits; 0 = none) ; the
# track's fader ; its pan ; its eq bands (| between) ; the five strokes' velocities ; how long each rings, in
# fifths of a pulse ; the loudness target ('' = unchanged) ; overrides on the handpan's patch for these strokes.
# '' = v13 byte for byte.
FIFTH = os.environ.get("C10T16_FIFTH", "square again;0,0,1,1,13,13,1234,1234;-11dB;0.3;hp cutoff=500;0.85,0.5,0.6,0.5,0.6;1;;"
                                       "synth.amp.d=300ms synth.amp.r=50ms fx.0.mix=0.1" if STROKE else "")
# v15 (chirper-alpha; section round, w5, 1:56-2:25; the change is bar 39, 2:18.2-2:21.8): THE PAIR IS STOPPED AT THE
# FOURTH. Until now the metre changed only by the peg: the hair moves, the note stays. Here the note moves and the
# peg is left alone. Stop both reeds a fourth higher and the hair is the same width in cents and a third wider in
# cycles, so the pulse is a third faster: a fourth is 4:3, and three to the bar becomes FOUR. (A twelve-string's
# wobble quickens up the neck.) For one bar of 'three' the band, which only plays what the pair does, is in common
# time on A flat: each part in the rule plays the pulse it played in three quarters of the time, a fourth higher,
# four times (kick and bass 3 -> 4, guitars 6 -> 8 and 12 -> 16, toms 9 -> 12 on A flat's own drums, hat 12 -> 16);
# the reeds are struck on 207.652 and 208.752 Hz (1.100 Hz apart: 9.15 cents, where on E flat they are 9.16). The
# snare and the crash are outside the rule and stay: the kick lands with the snare on two and four. Then the low
# E flat and three again, and two bars later the peg turns to four the slow way.
# The pair alone in that bar: its four overtones pulse 3.96, 8.00, 11.98, 16.00 to the bar, 23 to 29 dB deep, the
# swells within 0.02 of a pulse of the strokes. Every other bar of the finished file is v14's (null, three seeds).
# the section ; which of its bars (from 1; several with commas) ; the fret, in semitones ; the pulses to the bar
# it gives ; the loudness target ('' = unchanged). '' = v14 byte for byte.
FRET = os.environ.get("C10T16_FRET", "three;5;5;4;" if FIFTH else "")
# v16 (chirper-one; whole-song round): THE PAIR SHOWS THE COUNT. From bar 11 to bar 55 (0:36-3:20) the band played
# without a rest, 45 bars inside 1.8 dB, with the two reeds 9 to 10 dB under it: the song says the band only plays what
# the pair does, and after the opening nobody could hear the pair do it. Now, at each change of the hair, the band
# rests for the first bar of the new count and the pair is heard pulsing it; then the band plays it. Each time one
# drum stays and counts its own overtone beside the reeds, so the rule is laid out one line at a time: at 'five' the
# reeds alone (five swells); at 'seven' the hat (the fourth overtone's 28); at 'three' the toms on the low ground
# (the third's nine); at 'square again' the foot (the first's four). The crash stays on each downbeat.
# section=tracks that stay (commas), ';' between sections | tracks that never rest | the loudness target ('' =
# unchanged). The band rests in the section's first bar. "" = v15 byte for byte.
SHOWN = os.environ.get("C10T16_SHOWN", "five=brass;seven=brass,hat;three=brass,skins-bb1;square again=brass,foot|"
                                       "reed,hair,third,drum,cymbals,pan,pan-out,pan-five,bend|-10.1" if FRET else "")
# v17 (chirper-alpha; instrument round: the four guitars, every muted stroke, 906 of 1264 notes): THE HAND LIGHTENS.
# Read alone beside six records' strokes (riffpunch --strokes, 342 clean muted strokes) the chug had three faults: its
# low end died after the stroke (+2.36; records -1.10), it had no teeth (400 Hz-1 kHz less 1-4 kHz -5.42; records
# -11.31), and by part the guitars stood 3.9 dB over the records' at 500 Hz-1 kHz, on the reeds' fourth overtone.
# (1) The palm's weight was 1.0 on every muted stroke; it is 0.4 on a stroke that says two (half way between two
# kicks), 0.5 on three (the thirds), 0.6 on four (the quarters). The weight is the low end: the album's cure alone
# made it worse (+3.45), one weight of 0.6 gave +0.42, these three -0.64. The three read nearly alike; the ladder is
# the best fit of five tried, not a thing an ear will follow. (2) A full hand closes the string's filter 2 octaves,
# not 3.4. (3) The microphone 0.4 -> 0.5. (4) The +2.5 dB at 700 Hz is -1.5 dB, and +2.5 dB at 185 Hz gives back
# some of the body the lighter hand takes (by part 120-250 Hz -3.4 -> -5.0; without the band -6.8).
# After: teeth -11.70, grain 0.39 (0.40), rise 20.0 ms (19.75); the rig alone against a record's guitar 2.53 -> 1.95;
# the mix against the records 1.58 -> 1.28, six stretches of six nearer; the reeds' fourth overtone 1.5 to 2 dB
# more heard. The cost: leaner guitars, and the band up to 0.4 dB quieter where they lead.
# the palm's reach on the string's filter, octaves ; the hand's weight on a muted stroke that says two, three, four
# (half way between two kicks, on the thirds, on the quarters; anything else takes the last) ; the microphone ; the
# bands on each guitar where the 700 Hz lift was ('|' between them; '' = none) ; the loudness target ('' =
# unchanged). '' = v16 byte for byte.
HAND = os.environ.get("C10T16_HAND", "-2;0.4,0.5,0.6;0.5;peak cutoff=700 q=0.9 gain=-1.5dB|peak cutoff=185 q=1.2 gain=2.5dB;-10.27" if SHOWN else "")
# v18 (chirper-three; section round on w2, 0:29-0:58, which the map flags 'static': 'square', where the band comes in,
# was six bars alike). THE STRING GIVES. A string that has just been brought up to pitch slips, and the hand brings it
# up again. In the third bar of 'square' (0:43.6) the hair narrows from one pulse a beat to a half, which is how
# wide it was half way through the opening (0:21.8), and in the fourth (0:47.3) it is pulled back; so 'square' reads two
# bars in four, two that sag and recover, two in four, two that quicken into five. Nothing is invented: the pair is
# struck at each bar line and the sharp reed glides (v3's two bars, down and then up), and everyone in the rule
# plays where the pair's swell is: six kicks where there were eight, 0.97, 1.16, 1.51, 1.51, 1.16, 0.97 s apart (0.91
# in four), the bass with them, the guitars twice to each, the toms three times, the hat four. The snare and the
# china are not in the rule and keep the bar. THE LEAD COMES WITH IT by its own rule (v10: wherever the peg is
# turned once the band is in): its bent string sags with the reed and comes back, at 0:43.6, where its first note
# had been 0:58.2. 106 notes become 84 in the two bars; every note outside them is v17's on every track.
# MEASURED: the pair alone, the swell of its fundamental against the four written kicks inside the two bars: +3, +4,
# +7, +2 ms (a plain bar's: +6, +7, +6). The lead 12.0 dB under everything else there (K; 12.6 at its turn into five)
# and adding to the reeds' line at 349 Hz as it does there (+3.6 dB; +3.7). The two bars +2.2 to +2.5 dB at 250-500
# Hz against v17 (the lead is +2.1 of it), up to 1.7 dB less at 60-120 Hz (two kicks fewer), within 0.13 dB overall. Everything outside them within 0.007 dB of v17
# on three seeds with the target where it was. The map: w2's bar-to-bar rhythm 0.043 -> 0.078 and no flag.
# the section ; the bar of it in which the string gives (the next brings it back) ; the hair's width at the bottom, in
# pulses to the beat ; dB on the lead's notes in those two bars ("" = as at its other turns, "none" = no lead there) ;
# the loudness target ("" = unchanged). "" = v17 byte for byte.
GIVES = os.environ.get("C10T16_GIVES", "square;3;1/2;;" if HAND else "")
# v19 (chirper-alpha; palette round: the two reeds, the whole song; no note changes): THE REEDS HAVE THEIR TWELFTH.
# The song's rule is that the pair's overtones pulse two, three and four times to its one, and the band plays
# them: guitars the twos, toms the threes, hat the fours. But the pair itself could not say three. The library
# harmonium's reed is a pulse 0.35 of a cycle wide, and a pulse a THIRD of a cycle wide has no third harmonic at
# all: at 0.35 it is 24.7 dB under the first by arithmetic, and on the pair alone it read 20.9 to 21.1 under (the
# second 7.0 to 8.1 under, the fourth 6.2 to 7.3, the fifth 7.7 to 8.4). It swelled as the rule says, nine times
# to the bar in 'three' and twelve in 'square', where nobody could hear it: 10.9 to 11.9 dB under everything else
# in its third-octave with the band in, and 2.8 under even in the bar of 'three' where the band rests and the low
# toms count its nine beside it (v16). So each reed gets what a reed organ gets when a stop is drawn: one more
# rank, at three times its own note (the twelfth; an organ's 2 2/3 foot), a sine, 10.5 dB down in the patch beside
# the reed's own two pulses at 4 and 7 down. Both reeds have it, each on its own note, so the rank beats as the
# pair does, three times as fast; the turned reed (the sharp one while the peg moves) has it too and it follows
# the slide. The third reed (v5), which is in tune with the still one, does not: there it would drown the wobble.
# (Benched, raw, the pair alone and in the mix. The third overtone now stands 7.8 to 8.1 dB under the first, with
# the second and the fourth; it swells 17.4 to 18.7 dB deep, 9.0 and 12.0 to the bar; with the band in it reads
# +1.1 to +2.1 against everything else, and +9.4 in the bar where the toms count it. The other overtones read as
# they did to 0.1 dB; the pair alone is 0.2 to 0.3 dB louder. THE HANDPAN strikes this overtone as a note, C5,
# when it swells (v2): at its 24 strokes in the opening the pair now stands 1.5 dB under it there (it was 14.4
# under), and the two together read 1.0 dB under the two apart (median; -6.6 to +2.6), as on the other three
# overtones (-0.4, +1.4, -0.5; the worst stroke 5.0 to 5.9 under): no stroke-by-stroke lock, nothing to mend. THE
# GUITARS' FIFTH has its eighth harmonic on the same hertz (pure since v11): read summed, the mix gains 3.2 to 3.8
# dB in that third-octave with the band in, which is what a part 1 to 2 dB over the rest adds: no cancelling.
# THE FIRST TAKE was the rank at -9 dB: +2.5 to +3.5 with the band in, but against the eleven records 500 Hz to
# 1 kHz, where this song is already over, rose 0.5 to 1.2 dB; at -10.5 it rises 0.4 to 0.9. The target moves
# -10.27 to -10.235: the reeds are louder, and the band's bars were coming out 0.05 to 0.10 dB lower.
# NOT DONE: re-cutting the reed itself. A pulse 0.15 wide would have the second, third and fourth 1.0, 2.8 and
# 5.6 dB under the first before the filters: every number present, and a much brighter instrument through the
# whole song. One rank changes one partial.)
# the rank's ratio to the reed's note ; its wave ; its level in the reed (beside the reed's own -4 and -7 dB) ;
# dB on the two reeds' faders ("" = as they were) ; the loudness target ("" = unchanged). "" = v18 byte for byte.
TWELFTH = os.environ.get("C10T16_TWELFTH", "3;sine;-10.5dB;;-10.235" if GIVES else "")
# v20 (chirper-three; section round, w3, 0:58-1:27; the change is bars 20-24, 1:12.0-1:24.4): THE BAND LEAVES EVERY
# FOURTH PULSE TO THE PAIR. After the bar in which the pair is shown (v16) 'five' was five bars alike: 25 pulses of
# one cell, the only stretch of the song where the rule was stated and nothing was done with it. Now the band counts
# a four of its own inside the five. It plays three pulses and leaves the fourth to the reeds, five times: the rest
# is the fifth pulse of bar 20, the fourth of bar 21, the third of 22, the second of 23 and the first of 24 (1:12.00,
# 1:14.91, 1:17.82, 1:20.73, 1:23.64; 0.727 s each). Four and five share nothing, so a rest every fourth pulse
# visits each of the bar's five places exactly once, a place earlier each bar; when it reaches the downbeat the
# phrase is done, the band plays the last four pulses whole and the peg turns into seven as it did. In each rest
# the pair is what v16 shows for a bar, a pulse at a time: the reeds, saying the cell the band has just stopped
# saying. The snare and the crash are not in the rule and keep the bar: the snare is alone inside two of the rests
# (1:15.45, 1:20.91) and the crash at the head of the last.
# WRITTEN: 75 strokes taken out, 15 a pulse (the two guitars 2 each, the left guitar's threes 2, bass, kick, three
# toms, four hats). Nothing added, nothing moved; every other note is v19's.
# MEASURED (t16-r20; raw, the song's own seed): over each rest the three reeds stand over everything else by +16.6,
# +0.6, +27.7, -2.0 and +0.1 dB K (they stood -8.8, -6.5, -5.0, -6.9, -7.2 under the band); the second and fourth
# hold a snare stroke and the fifth the crash, and by quarters of the pulse those read +28.8 +47.2 +7.5 -4.8, +24.6
# -8.5 +10.1 +24.4 and -4.0 -0.2 +10.9 +23.4. The mix falls 9.3 dB into the first rest (the pair alone) and 6.3 into
# the third (the third reed is holding by then). Finished files, seeds 0 / 11 / 1: the five rests read -7.7 to -8.3,
# -3.1 to -3.9, -4.9, -2.9 to -4.5 and -3.4 to -3.7 dB against the same pulses of v19, the twenty pulses the band
# plays within 0.02 dB, the five bars -0.61 dB. The target goes -10.235 -> -10.295 (the song is 3.6 s of band
# lighter and the master had raised everything else 0.04 to 0.11 dB): every other stretch within +0.002 to +0.009 dB
# and -68 dB or lower.
# the section ; every how many of its pulses the band leaves one ; the first pulse left, counted from the first the
# band plays there (from 0) ; how many times ; who leaves ; the loudness target ("" = unchanged). "" = v19 byte for byte.
LEAVES = os.environ.get("C10T16_LEAVES", "five;4;4;5;left,right,left-said,right-said,bass,foot,skins-eb2,hat;-10.295" if TWELFTH else "")
# v21 (chirper-two; palette round: the bass drum, the album kit's as it comes, becomes a drum of the song's own; no
# stroke moves): THE FOOT IS ON THE NOTE. The song is one note, and everything in it is on the ground or a hair off
# it on purpose: the reeds, the guitars, the bass, the toms (v13: "on the ground's own notes"), the great drum, the
# handpan. One thing was not. The bass drum was the album kit's on A (55 Hz) whatever the ground: the major third
# over F, a semitone over A flat, a tone under B, the tritone of E flat; and the kit's drum wanders at random, so it
# was never the same A twice (read: 14 cents under to 17 over, stroke to stroke). It plays the pair's slowest
# pulse, 191 strokes, with the bass striking under 171 of them.
#   THE DRUM TAKES THE BASS'S NOTE, stroke by stroke (alone, the ground's): F1 43.7 Hz, A flat 1 51.9, E flat 1
#       38.9; it does not wander. So it is retuned when the peg turns: up a minor third into 'five', down into
#       'three'. ON B IT STANDS A FOURTH LOWER (G flat 1, 46.2 Hz): on B1 itself (61.7 Hz, built) the mix lost 2.4
#       dB under 60 Hz and drum and bass, on one frequency at one level, cancelled by turns (the stroke under 70
#       Hz 2.5 dB down, its spread 1.1 -> 5.2 dB). v13's toms already stand a fourth lower there, for their reason.
#   A CHEST: the kit's drum has nothing at its octave (its drive makes odd harmonics only). A bare sine an octave
#       over the drum, 90 ms, on every stroke, on a track of its own past the drums' bus, -4 dB. (-7 read 0.2 to
#       0.3 dB shorter at 60-120 Hz, the band this song is shortest in.)
#   READ (cents.py, the drum's line 30-110 ms after the stroke): 1 to 9 cents over its note on F, A flat and G
#       flat, 22 over on E flat (the end of the drum's own fall is still in it), 3 cents wide or less on the
#       three notes it takes after the peg has turned.
#   WITH THE BASS (sum.py, drum, chest and bass alone, the 250 ms after each stroke): under 70 Hz +1.4, +2.3, 0.0
#       and +2.9 dB on F, A flat, B and E flat (drum and bass now add where they beat); 70-140 Hz +1.3 to +2.4.
#   THE MIX AGAINST THE RECORDS (seven windows): 1.162 -> 1.127 (their mixes), 1.475 -> 1.314 (their voiceless
#       passages); 60-120 Hz nearer in all seven (-0.5 -0.5 -0.7 -0.3 -0.6 -2.0 -3.0 -> -0.1 -0.2 -0.1 0.0 -0.2
#       -1.5 -2.2); 250-500 Hz 0.1 to 0.6 nearer in six of the seven (the drum's fifth harmonic left it). Under
#       60 Hz the five band sections went from -0.4 -0.1 +0.2 -0.5 -0.7 to +0.5 +0.8 +0.4 +0.7 +0.1: a little
#       further, on the other side.
#   NOT NEARER ALONE: by kickspec the drum is no nearer the records' bass drums (7.76 -> 8.12): theirs sit at 50 Hz.
#   BUILT AND NOT KEPT: the bass ducked under the drum (4, 6, 9 dB; strokes evener, every window worse: six band
#       windows 0.969 -> 1.094); the drum's drive 0.35 -> 0.2 (the mix the same to 0.02, the knock further from
#       the records', -28 -> -34 against -25.9); the bass's sine handed to the drum (not built: the bass HOLDS
#       here, and for three quarters of every beat the floor is the bass's alone).
#   The target -10.295 -> -10.355: a lower drum weighs less on the meter, and the two stretches with no drum in
#       them (0:00-0:07, 3:19 on) had come up 0.05 to 0.07 dB on three seeds.
# overrides inside the kit's bass drum, after its note ; the highest note a foot may take, Hz (a ground over it: the
# drum stands a fourth lower) ; the chest: semitones over the drum : its length, ms : its fader ('' = no chest) ;
# the loudness target ('' = unchanged). "" = v20 byte for byte.
FOOT = os.environ.get("C10T16_FOOT", "kit.k.patch.synth.pitch.mod.1.amount=0;55;12:90:-4dB;-10.355" if LEAVES else "")
# v22 (chirper-alpha; section round, w1, 0:00-0:29; the change is the first two bars, 0:00-0:07.3; one note of
# the turned reed is rewritten and nothing else). THE REEDS ARE TUNED BEFORE THE SONG BEGINS.
#   The song is about a peg, and it is named for what a tuner says when the wobble stops. It ends that way: the
#   hair closes to nothing over six bars (v8) and the two reeds are left alone on one still note (v11). But it BEGAN
#   with the job already done: two bars of the pair in tune, 7.3 seconds of one plain note, and then the peg was
#   turned away so slowly that nothing wobbled until 0:14.6. The first quarter-minute of a song about beating had
#   no beat in it, and the map called the window static in tone.
#   NOW THE FIRST THING HEARD IS THE TUNING. The second reed comes in two pulses a beat sharp (2.2 Hz, 21.7 cents:
#   wider than the song ever turns it afterwards; 'seven' is seven quarters) and is turned down to the first reed
#   in one straight line over the two bars. So the pair's swell SLOWS: 0.47 s to the first return, then 0.50, 0.55,
#   0.61, 0.69, 0.82, 1.07, and 2.57 s to the eighth, WHICH IS THE STROKE AT 0:07.3: the unison arrives on the song's
#   first drum, and from there the peg is turned away as before. Eight swells in, sixteen out; the still point is
#   the stroke itself. The overtones do what they do all song, here alone and slowing: the octave swells sixteen
#   times, the twelfth twenty-four, the double octave thirty-two.
#   NOBODY PLAYS ALONG: no drum, no handpan, no cymbal. Everywhere else in the song a pulse is pointed at; here the
#   pair is heard doing it by itself, faster than a band could follow, before there is a band. And the one place
#   the two reeds are heard still and alone is now the END (v11), which is where the song was going.
#   It is one more turn of v8's peg ('in tune=2>0'), written with v8's own solver: the glide's size is fitted so the
#   two bars hold a whole number of pulses, so the reeds meet in step.
#   MEASURED (the pair alone, raw): the fundamental's swells at 0.46, 0.98, 1.54, 2.14, 2.82, 3.66, 4.70 s (written
#   0.47, 0.97, 1.52, 2.13, 2.82, 3.64, 4.70), its dips 17 to 33 dB under the still note; over the last half second
#   it is the still unison's level to 0.0 dB (the octave 0.6 under). Two reeds apart are 3 dB quieter than two
#   in step: the first two bars read 2.8 dB lower in the finished file (K), rising into the stroke.
# the width the pair begins at, pulses a beat (it is turned to nothing over the two bars of 'in tune') ; the loudness
# target ('' = unchanged). "" = v21 byte for byte.
TUNED = os.environ.get("C10T16_TUNED", "2;-10.373" if FOOT and PEG else "")
if TUNED:
    assert "in tune" not in RAMPED
    RAMPS["in tune"] = (("in tune",), Fr(TUNED.split(";")[0]), Fr(0))
    RAMPED["in tune"] = "in tune"
# v23 (chirper-three; instrument round: THE SNARE, its 84 strokes; none is added, moved or struck harder).
# THE READ. (1) ITS NOTE. The album kit's snare is written on A3 and its head sounds 243.5 Hz: B3, 20 to 28 cents
#   flat, and it wanders stroke to stroke (-23 to +28 cents; the song's whole subject is a hair of 11). Its second
#   mode stood a tritone and 30 cents over that (350 Hz, 7 dB under). So on F it rang a flat tritone over the
#   ground, on A flat a flat minor third, on E flat a flat minor sixth, and on B the ground's own note a quarter of
#   a semitone flat. v13 put the toms on the ground's notes and v21 the bass drum; this was the last drum that was not.
# (2) ITS SHAPE, alone beside six records' snares (tools/snarespec.py; mean distance over 160 Hz-5 kHz): 5.3 to 5.7 in
#   the five stretches, with humps of +5 to +10 dB at 1, 1.25, 2 and 2.5 kHz and 1 to 5 dB short from 4 to 8 kHz; body
#   against crack -3.8 to -6.2 (the records -2.9, never under -4.4), wires against crack -5.1 to -6.7 (+0.4, never
#   under -0.6). (3) WHOSE THE HUMPS ARE: with the snare's send to the kit's overhead room taken away the stroke's
#   first 150 ms lose 10.7 dB, and 15 to 17 dB from 1.25 to 3.15 kHz. Most of what is heard of this snare is that
#   room, whose low cut (5 kHz) is gentle; the bus's clip changes nothing in the shape and its glue about 1 dB of
#   the humps (benched without each).
# WHAT IS WRITTEN. THE HEAD SOUNDS THE GROUND'S NOTE, stroke by stroke: F3 on F (42 strokes), A flat 3 on A flat
#   (14), E flat 3 on E flat (14), and on B a fourth lower, G flat 3 (14), as the toms and the foot stand there. It
#   does not wander (the kit's two moves on the drum's pitch are off: the spread goes from 20 cents either way to
#   3, and the note does not move). The head is written 1.15 semitones under the note
#   it sounds, because the air between the two heads raises the pair; and that air is set (cavity 0.3 -> 0.162) so
#   the second mode is A FIFTH over the note, not a tritone. Read dry, ground by ground: the note within 2 cents on
#   all four, stroke to stroke -3 to +3 cents; the second mode within 4 cents of the fifth, 9.5 to 10.8 dB under.
#   THE DRUM: ten head modes, not 24, and 6 dB out at 900 Hz inside the drum; the wires at 5 kHz and full; its low
#   cut at 110 Hz and its body's lift on the note itself, so the body is the same on every ground. ITS ROOM IS ITS
#   OWN: a copy of the kit's overhead room with 6 dB out at 1.05 kHz, 5 at 2.3 kHz and a shelf of +4 dB from 3.5 kHz
#   after it (the cymbals keep the kit's room). The track's own shelf (-3 dB from 7 kHz) is gone; fader 3.5 -> 3.1.
# AFTER. Alone: 5.48, 5.70, 5.31, 5.46, 5.57 -> 3.06, 3.69, 3.47, 4.55, 3.47 (F, A flat, B, E flat, F again); body
#   against crack 0.0, -2.0, -0.8, -1.4, +0.2 (inside the records' range in all five; four were under it); wires
#   against crack -1.0, -1.2, -1.0, -1.7, -0.8 (0.2 to 1.1 short of the range still). A stroke's first 150 ms is
#   within 0.25 dB of v22's on every ground (K; its peak 0.1 to 0.7 dB higher), and inside the mix the snare stands where it stood (-6.2, -8.0,
#   -7.9, -9.4, -8.3, -8.3 -> -6.1, -8.3, -8.0, -9.4, -8.0, -8.4 dB against everything). THE MIX against the
#   records, six stretches: without a voice 1.106 -> 1.072, all eleven 0.928 -> 0.850, nearer in all six on both.
#   The kit by part: 250-500 Hz +2.7 -> +1.2, 500 Hz-1 kHz +5.5 -> +3.5, 1-2 kHz +2.5 -> -1.0.
# COSTS: the snare's ring after the stroke (0.15 to 0.6 s) is 2.0 to 3.7 dB lower on four of the five stretches (K:
#   the room's cut bands are where the meter listens), so 'wider', where the snare is the loudest thing, is 0.15
#   to 0.23 dB lower ; the kit by part 120-250 Hz +1.1 -> +2.0 (the note is lower) ; on E flat the note (156 Hz) is under
#   where any record's snare sits (4.55, the least gain) ; a dip of 6 dB at 1.6 kHz in the first stretch on F ; the
#   snare's ring is now a
#   pitch you can name, and it steps with the peg: if that is heard as a tom, see the round's next-note.
#   The target is not moved: where no snare plays the file is 0.02 to 0.04 dB over v22, the band within 0.05.
# the head: semitones its written note stands under the note it sounds : the air between its two heads (`cavity`) ;
# the highest note it may take, Hz (a ground over it: the drum stands a fourth lower, as the toms and the foot do) ;
# what every stroke's drum takes besides its note ; the snare's own room: bands after a copy of the kit's overhead
# room ('' = the kit's room, as before) ; what it sends there ; its track eq ('-' = none, '' = as it was) ; its
# fader ; the loudness target ('' = unchanged). "" = v22 byte for byte.
HEAD = os.environ.get("C10T16_HEAD", "1.15:0.162;220;"
                      "kit.s.patch.synth.pitch.mod.0.amount=0 kit.s.patch.synth.pitch.mod.1.amount=0 kit.s.patch.synth.filters.0.cutoff=110 "
                      "kit.s.patch.synth.layers.0.mode_count=10 kit.s.patch.synth.filters.2.kind=peak kit.s.patch.synth.filters.2.cutoff=900 "
                      "kit.s.patch.synth.filters.2.q=1 kit.s.patch.synth.filters.2.gain=-6dB kit.s.patch.synth.layers.0.wire_tone=5000 "
                      "kit.s.patch.synth.layers.0.wires=1;"
                      "peak cutoff=1050 q=1.2 gain=-6dB|peak cutoff=2300 q=1.2 gain=-5dB|highshelf cutoff=3500 gain=4dB;-1.5dB;-;3.1dB;"
                      if TUNED else "")
# v24 (chirper-alpha; section round, w7, 2:54-3:31, flagged static; the change is 3:20.0-3:22.1, between the band's
# last stroke and the last chord: thirteen notes on a new track, `last` (the song's handpan, damped), and one
# stroke of the finger cymbals; nothing else changes). EVERY OVERTONE HAS A LAST SWELL.
#   In the ending the peg is turned down to the unison in one straight line (v8), twelve pulses long. Overtone n of
#   the pair swells n times a pulse, so it swells for the LAST time one n-th of a pulse before the end: the higher
#   the overtone, the later. The band already plays the first two: its last stroke is the fundamental's last swell
#   (3:17.35) and the guitars' last muted stroke is the octave's (3:19.2). Then nobody played, for 4.4 seconds, while
#   the pair went on settling overtone by overtone. Now the handpan, which has named the pair's overtones since v2,
#   names each of the rest as it swells for the last time: 3 (C5, 3:20.0), 4 (F5, 3:20.5), 5 (A5), 6 (C6), 7, 8 (F6),
#   9 ... 15, the gaps closing as a dropped ball's do (0.49 s, 0.33, 0.25 ... 0.06); and the sixteenth is the finger
#   cymbals' own note (chirper-two tuned them to 2793.8 Hz, sixteen times the reed), so they ring it (3:22.1). After
#   that nothing an ear can follow in the pair is still moving: a second and a half of the drone, and the chord
#   (3:23.6). The band slows to a stop and the pair's settling runs UP the harmonic series, faster and faster.
#   READ ON THE PAIR ALONE: the last swell of overtones 5 to 16 falls 0 to 44 ms from where the note is written
#   (median 11 ms; 3 and 4 have flat tops the notes sit on).
#   THE SOUND: the song's handpan with its ring damped (1.5 s; as it rings elsewhere, 5.5 s, thirteen notes stood
#   1.8 dB under the drone through the stillness and there was none), no wander in time, each note 3 dB softer per
#   octave over the first (the patch grows louder as it climbs; with the tilt the notes stand level, -3 to -5 dB
#   against everything else, K). MEASURED (raw, own seed): at its own pitch a note is +4.4 dB over everything else
#   (median; least +0.3); the mix at each note's own line gains +4 to +14 dB (median +8.4), and on the finished
#   files of three seeds +4.3 or more on every note. Two strokes are written a fraction of a millisecond late (the
#   last field): F5 0.72 ms and the fourteenth 0.2 ms, half a cycle each: as first written they fell against lines
#   already sounding (the lead guitar's partials) and TOOK 3 and 6 dB from them.
# the overtones named at their last swell, 'from-to' ; what the handpan's patch takes besides ; its fader ; its pan ;
# the touch a * n ** b + c ; how long a note is held, beats ; dB a note loses for each octave over the first named ;
# the finger cymbals' own overtone:piece:velocity:beats it is left to ring ('' = no stroke) ; the loudness target
# ('' = unchanged) ; overtone:milliseconds a stroke is written later, ',' between (a stroke on a line another part
# holds adds to it or takes from it by where in the cycle it falls). "" = v23 byte for byte. On only while HEAD and
# PEG are.
LAST = os.environ.get("C10T16_LAST", "3-15;synth.amp.d=1.5s synth.amp.r=1.5s synth.env.ring.d=2s synth.env.ring.r=2s play.humanize.time=0ms;"
                      "-9.5dB;0;0.8,-0.28,0.2;2;3;16:o:0.62:1.6;;4:0.72,14:0.2" if HEAD and PEG else "")
# what the handpan says on each pulse of a section the peg is turned through (v2's order, a pulse each)
TURNED_NAMED = {"a hair": NAMED["a hair"], "wider": ((1, 2, 3, 4), ()) * 6,
                "a quarter": ((1, 2, 3, 4), (1, 2, 3, 4), (1, 2, 3), (1, 2, 3)), "an eighth": ((1, 2),)}


def places(said):
    """Where in one pulse a guitar that says these overtones strikes: '2' -> 0, 1/2 ; '23' -> 0, 1/3, 1/2, 2/3 ; ..."""
    return sorted({Fr(i, int(m)) for m in said for i in range(int(m))})


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
    for _ in range(60):                      # the far end that makes the count whole (v8: a peg may be turned down too)
        size = (a + z) / 2
        a, z = (size, z) if (phases(size)[-1] < n) == (r1 > r0) else (a, size)
    table = phases(size)

    def when(p):
        p = float(p)                         # (a Fraction against 4000 floats, a thousand times over, took most of a minute)
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

    def turn(b0, names, r0, r1):
        """v8: one turn of the peg through several sections. The hair goes from r0 to r1 pulses a beat in a straight
        line, the pair is struck once, and every stroke falls where the pair's own swell does (as in v3's two bars).
        Who plays a pulse is who played the section it begins in."""
        secs, at = [], 0
        for name, r, bars, ground, who in FORM:
            if name in names:
                secs.append((at, at + 4 * bars, name, who, ground))
            at += 4 * bars
        assert secs[0][0] == b0 and all(x[1] == y[0] for x, y in zip(secs, secs[1:])), names
        total, f, root = secs[-1][1] - b0, hz(REED + secs[0][4]), 29 + secs[0][4]
        size, n, when = turned(f, r0, r1, total, total - 0.04)
        put("reed", b0, f"{f:.3f}hz", total - 0.04, 0.8)
        put("hair", b0, f"{f + float(r0) * HAIR:.3f}hz", total - 0.04, 0.8)
        ev["hair"][-1].update(patch=GLIDER, expr={"slide": 0.0}, expr_end={"slide": round(size, 6)})
        seen = defaultdict(int)
        for p in range(n):
            t0, t1 = when(Fr(p)), when(Fr(p + 1))
            _, _, name, who, _ = next(x for x in secs if x[0] <= b0 + t0 < x[1])
            i, seen[name] = seen[name], seen[name] + 1               # this section's i-th pulse
            if "k" in who:
                kit("foot", b0 + t0, "k", 0.98 if i == 0 else 0.88)
                if "g" in who:
                    put("bass", b0 + t0, nm(root), t1 - t0 - 0.1, 0.95 if i == 0 else 0.9)
            if "g" in who:
                half = when(Fr(2 * p + 1, 2))
                for tr in ("left", "right"):
                    put(tr, b0 + t0, f"{nm(root)},{nm(root + 7)}", half - t0 - 1 / 12, 0.92)
                    put(tr, b0 + half, nm(root), min(0.3, (t1 - half) * 0.6), 0.82, mute=True)
            if "t" in who:
                for j in range(3):
                    kit("skins", b0 + when(Fr(3 * p + j, 3)), ("ft", "t2", "t1")[j], 0.8 if j == 0 else 0.62)
            if "h" in who:
                for j in range(4):
                    kit("hat", b0 + when(Fr(4 * p + j, 4)), "h", 0.62 if j == 0 else 0.42)
            if PAN and name in TURNED_NAMED and (b0 < 40 or PAN.split(";")[2]):
                for k in TURNED_NAMED[name][i]:                      # overtone k, k times to the pulse
                    for j in range(k):
                        put("pan" if b0 < 40 else "pan-out", b0 + when(Fr(k * p + j, k)), f"{k * f:.3f}hz", min(2, (t1 - t0) / 2),
                            round(TOUCH[k] + (0.2 if name == "an eighth" else 0), 2))
        assert all(seen[x] == len(TURNED_NAMED[x]) for x in seen if x in TURNED_NAMED), dict(seen)

    b = 0                                    # in beats
    for num, (name, r, bars, ground, who) in enumerate(FORM):
        marks.append((name, b, r, bars))
        f = hz(REED + ground)
        if name in RAMPED:                   # v8: the peg is turned through this section (the whole turn is written at its first)
            if name in RAMPS:
                turn(b, *RAMPS[name])
            if "s" in who:                   # the snare is not in the rule
                for bar in range(b, b + 4 * bars, 4):
                    kit("snare", bar + 1, "s", 0.9)
                    kit("snare", bar + 3, "s", 0.95)
            b += 4 * bars
            continue
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
                        for tr, said in zip(("left", "right"), SAID.get(name, ("2", "2"))):
                            if said != "2":  # v7: this guitar says another number too, on the same phase
                                fr, half = places(said), Fr(j % 2, 2)
                                for i, x in enumerate(fr):
                                    if not half <= x < half + Fr(1, 2):
                                        continue
                                    t0 = a + when(j // 2 + x)
                                    g2 = a + when(j // 2 + (fr[i + 1] if i + 1 < len(fr) else 1)) - t0
                                    if x == 0:
                                        put(tr, t0, f"{nm(root)},{nm(root + 7)}" + (f",{nm(root + 12)}" if j == 0 else ""), g2 - min(1 / 12, g2 * 0.3), 0.96 if j == 0 else 0.92)
                                    else:
                                        put(tr if x == Fr(1, 2) else tr + ALSO, t0, nm(root), min(0.3, g2 * 0.6), 0.82 if x == Fr(1, 2) else float(SIDES.split(";")[1]), mute=True)
                            elif j == 0:     # the bar line's open chord, as every bar of the section begins
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
                for tr, said in zip(("left", "right"), SAID.get(name, ("2", "2"))):
                    first = float(places(said)[1] / r) if r and "g" in who and said != "2" else 0   # v7: to this guitar's next stroke
                    put(tr, a, f"{nm(root)},{nm(root + 7)},{nm(root + 12)}", first - min(0.08, first * 0.3) if first else (1 / (2 * float(r)) - 0.08) if r and "g" in who else 7.6, 0.96)
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
                        there = j == 0 and "c" in who and a % 4 == 0      # the chord is there
                        gap = Fr(span, int(count))
                        for tr, said in zip(("left", "right"), SAID.get(name, ("2", "2"))):
                            if said != "2":   # v7: this guitar says another number too
                                fr, half = places(said), Fr(j % 2, 2)
                                for i, x in enumerate(fr):
                                    if not half <= x < half + Fr(1, 2):
                                        continue
                                    g2 = ((fr[i + 1] if i + 1 < len(fr) else 1) - x) * 2 * gap
                                    if x == 0 and not there:
                                        put(tr, at, f"{nm(29 + ground)},{nm(36 + ground)}", g2 - min(Fr(1, 12), g2 * Fr(3, 10)), 0.92)
                                    elif x:
                                        put(tr if x == Fr(1, 2) else tr + ALSO, at + (x - half) * 2 * gap, nm(29 + ground), min(Fr(3, 10), g2 * Fr(3, 5)), 0.82 if x == Fr(1, 2) else float(SIDES.split(";")[1]), mute=True)
                            elif there:
                                continue
                            elif j % 2 == 0:  # with the kick: the low string and its fifth, open, cut before the muted stroke
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
    if GIVES:
        # v18: two bars of a plain section are turned, down and back. Written as v3's two bars are: the pair is struck
        # at each bar line, the sharp reed glides, and every stroke of the rule falls where the pair's swell does. The
        # snare and the brass are not in the rule and stay where they were.
        where, bar, low, _, _ = GIVES.split(";")
        at, sec = 0, None
        for name, r, bars, ground, who in FORM:
            if name == where:
                sec = (at, r, bars, ground, who)
            at += 4 * bars
        b0, r, bars, ground, who = sec
        b0 += 4 * (int(bar) - 1)
        assert 1 <= int(bar) < bars - SLIDES.get(where, 0) and all(x in who for x in "kgth") and SAID.get(where, ("2", "2")) == ("2", "2")
        f, root = hz(REED + ground), 29 + ground
        for tr in ("reed", "hair", "left", "right", "bass", "foot", "skins", "hat"):
            ev[tr] = [e for e in ev[tr] if not b0 <= e["at"] < b0 + 8]
        for a, r0, r1 in ((b0, r, Fr(low)), (b0 + 4, Fr(low), r)):
            size, n, when = turned(f, r0, r1, 4, 4 - 0.04)
            put("reed", a, f"{f:.3f}hz", 4 - 0.04, 0.8)
            put("hair", a, f"{f + float(r0) * HAIR:.3f}hz", 4 - 0.04, 0.8)
            ev["hair"][-1].update(patch=GLIDER, expr={"slide": 0.0}, expr_end={"slide": round(size, 6)})
            for layer, mult in (("k", 1), ("g", 2), ("t", 3), ("h", 4)):
                for j in range(n * mult):
                    t, gap = a + when(Fr(j, mult)), when(Fr(j + 1, mult)) - when(Fr(j, mult))
                    if layer == "k":
                        kit("foot", t, "k", 0.98 if j == 0 else 0.88)
                        put("bass", t, nm(root), gap - 0.1, 0.95 if j == 0 else 0.9)
                    elif layer == "g":
                        for tr in ("left", "right"):
                            if j == 0:
                                put(tr, t, f"{nm(root)},{nm(root + 7)},{nm(root + 12)}", gap - 0.08, 0.96)
                            elif j % 2 == 0:
                                put(tr, t, f"{nm(root)},{nm(root + 7)}", gap - 1 / 12, 0.92)
                            else:
                                put(tr, t, nm(root), min(0.3, gap * 0.6), 0.82, mute=True)
                    elif layer == "t":
                        kit("skins", t, ("ft", "t2", "t1")[j % 3], 0.8 if j % 3 == 0 else 0.62)
                    else:
                        kit("hat", t, "h", 0.62 if j % 4 == 0 else 0.42)
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
        track("reed", PAIR, f"{-9.5 + (float(AIR.split(';')[1]) if AIR else 0):g}dB", -0.12, fx=[{"type": "eq", "bands": ["peak cutoff=300 q=0.8 gain=-6dB"]}]),
        track("hair", PAIR, f"{-9.5 + (float(AIR.split(';')[1]) if AIR else 0):g}dB", 0.12, fx=[{"type": "eq", "bands": ["peak cutoff=300 q=0.8 gain=-6dB"]}]),
        track("left", "ct-twin fx.2.cone=37" + palm, "0.5dB", -0.92, "strings", mid),
        track("right", "ct-twin fx.2.cone=41" + palm, "0.5dB", 0.92, "strings", mid),
        *([{**track(side + ALSO, "ct-twin fx.2.cone=" + cone + palm, "0.5dB", pan, "strings",
                    mid + [{"type": "eq", "bands": [{"kind": "peak", "cutoff": keyed(round(hz(REED), 3)), "q": float(SIDES.split(";")[3].split(":")[0]),
                                                     "gain": SIDES.split(";")[3].split(":")[1] + "dB"}]}]),
            "auto": {"key": {"points": key, "curve": 0}}} for side, cone, pan in (("left", "37", -0.92), ("right", "41", 0.92))] if ALSO else []),
        # the bass holds its notes here (on the other songs it chugs): half of 120-250 Hz was its overtones
        track("bass", "ct-bass", (BASS.split(";")[2] if BASS else "0.5") + "dB", 0, "low", [{"type": "eq", "bands": ["peak cutoff=180 q=1 gain=-3dB"]}]),
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
                                                *([{"kind": "peak", "cutoff": keyed(float(x.split(":")[0])), "q": float(x.split(":")[1]), "gain": x.split(":")[2] + "dB"}
                                                   for x in BASS.split(";")[:2]] if BASS else
                                                  [{"kind": "peak", "cutoff": keyed(90), "q": 1.0, "gain": "7.5dB"}]),
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
                                 "extends": PAIR, "synth": {"pitch": {"value": 0, "mod": [{"src": "expr.slide", "amount": 1}]}}}}} if SLIDES else {}))
    if tuned:
        doc["patches"] = {**doc.get("patches", {}), **tuned}
    if THIRD and THIRD.split(";")[2]:
        doc["loudness"] = float(THIRD.split(";")[2])
    if DRUM:
        great_drum(doc)
    if CYMBALS:
        finger_cymbals(doc)
    if SIDES and SIDES.split(";")[2]:
        doc["loudness"] = float(SIDES.split(";")[2])
    if PEG and PEG.split(";")[2]:
        doc["loudness"] = float(PEG.split(";")[2])
    if BASS and BASS.split(";")[3]:
        doc["loudness"] = float(BASS.split(";")[3])
    if BEND:
        unison_bend(doc)
    if ALONE:
        in_tune(doc, end)
    if HAT:
        a_hat_with_a_body(doc)
    if STROKE:
        the_toms_count(doc)
    if FIFTH:
        the_fifth(doc, marks)
    if FRET:
        fretted(doc, marks)
    if HAND:
        the_hand_says_the_count(doc)        # before the bars of rest are taken out: it reads the kicks as written
    if SHOWN:
        the_pair_shows_the_count(doc, marks)
    if HAND and HAND.split(";")[4]:
        doc["loudness"] = float(HAND.split(";")[4])
    if GIVES:
        the_string_gives(doc)
    if TWELFTH:
        the_reeds_have_their_twelfth(doc)
    if LEAVES:
        the_band_leaves_every_fourth(doc, marks)
    if FOOT:
        the_foot_is_on_the_note(doc)
    if TUNED and TUNED.split(";")[1]:
        doc["loudness"] = float(TUNED.split(";")[1])
    if HEAD:
        the_snare_is_on_the_note(doc)
    if LAST:
        every_overtone_has_a_last_swell(doc, marks)
    return doc, marks, end


def every_overtone_has_a_last_swell(doc, marks):
    """v24: while the peg is turned down to the unison (v8: one straight line, twelve pulses), overtone n of the pair
    swells for the last time one n-th of a pulse before the end. The band already plays the first's (its last stroke)
    and the second's (the guitars' last muted stroke); the handpan names the rest, each at its own last swell, and
    the finger cymbals, which have stood on the sixteenth all song, ring theirs."""
    span, add, fader, pan, law, hold, tilt, cym, target, nudge = LAST.split(";")
    late = {int(x.split(":")[0]): float(x.split(":")[1]) * BPM / 60000.0 for x in filter(None, nudge.split(","))}
    names, r0, r1 = RAMPS["a half"]
    b0 = next(b for name, b, _, _ in marks if name == names[0])
    total = sum(4 * bars for name, _, bars, _, _ in FORM if name in names)
    f = hz(REED + next(ground for name, _, _, ground, _ in FORM if name == names[0]))
    _, pulses, when = turned(f, r0, r1, total, total - 0.04)
    a, b, c = (float(x) for x in law.split(","))
    lo, hi = (int(x) for x in span.split("-"))
    doc["tracks"].append({"name": "last", "patch": PAN.split(";")[0] + (" " + add if add else ""), "gain": fader, "pan": float(pan),
                          "notes": [{"at": round(b0 + when(pulses - 1.0 / k) + late.get(k, 0), 6), "len": float(hold), "pitch": f"{k * f:.3f}hz",
                                     "vel": round(a * k ** b + c, 2),
                                     **({"gain": f"{-float(tilt) * math.log2(k / lo):.2f}dB"} if tilt and float(tilt) and k > lo else {})}
                                    for k in range(lo, hi + 1)]})
    if cym:
        k, piece, vel, ring = cym.split(":")
        tr = next(t for t in doc["tracks"] if t["name"] == "cymbals")
        tr["notes"] = sorted(tr["notes"] + [{"at": round(b0 + when(pulses - 1.0 / int(k)), 5), "len": float(ring), "pitch": piece, "vel": float(vel)}],
                             key=lambda n: n["at"])
    if target:
        doc["loudness"] = float(target)


def the_snare_is_on_the_note(doc):
    """v23: the snare's head sounds the ground's own note (the octave from E flat 3; a ground over the highest it may
    take: a fourth lower), stroke by stroke, and does not wander; its second mode is the fifth over it. Its room is
    its own: a copy of the kit's overhead room with an eq after it. No stroke is added, moved or struck harder."""
    head, top, over, room, send, eq, fader, target = HEAD.split(";")
    under, cavity = head.split(":")
    snare = next(t for t in doc["tracks"] if t["name"] == "snare")
    assert snare["patch"] == "ct-kit" and all(n["pitch"] == "s" and "patch" not in n for n in snare["notes"])
    lane = [(float(b[:-1]), v) for b, v in doc["buses"]["low"]["auto"]["key"]["points"]]
    F3 = 53                                # the key lane counts semitones from F

    def note(at):
        m = F3 + [v for b, v in lane if b <= at + 1e-6][-1]
        return m - 5 if hz(m) > float(top) else m

    P = "kit.s.patch.synth."
    drum = lambda m: (f"ct-kit kit.s.pitch=m{m - float(under):.2f} {P}layers.0.cavity={cavity} {P}filters.1.cutoff={hz(m):.0f}"
                      + (" " + over if over else ""))
    snare["patch"] = drum(F3)
    for n in snare["notes"]:
        if note(n["at"]) != F3:
            n["patch"] = drum(note(n["at"]))
    if room:
        oh = doc["buses"]["oh"]
        doc["buses"]["snare-oh"] = {**oh, "fx": [oh["fx"][0], {"type": "eq", "bands": room.split("|") + list(oh["fx"][1]["bands"])}]}
        snare["sends"] = {"snare-oh": send}
    elif send:
        snare["sends"] = {"oh": send}
    if eq == "-":
        snare.pop("fx", None)
    elif eq:
        snare["fx"] = [{"type": "eq", "bands": eq.split("|")}]
    if fader:
        snare["gain"] = fader
    if target:
        doc["loudness"] = float(target)


def the_foot_is_on_the_note(doc):
    """v21: the bass drum takes the note the band stands on. Each stroke is tuned to the bass's note under it (alone, to
    the ground's: the bass bus's own key lane); where that note is over the highest a foot may take, a fourth lower, as
    v13's toms stand on B. A chest (a bare sine, a tenth of a second) says the drum's octave on every stroke, on a
    track of its own past the drums' bus. No stroke is added, moved or taken out."""
    over, top, chest, target = FOOT.split(";")
    T = {t["name"]: t for t in doc["tracks"]}
    foot, bass = T["foot"], T["bass"]
    assert foot["patch"] == "ct-kit" and all(n["pitch"] == "k" and "patch" not in n for n in foot["notes"])
    lane = [(float(b[:-1]), v) for b, v in doc["buses"]["low"]["auto"]["key"]["points"]]
    midi = {nm(m): m for m in range(12, 60)}
    F1 = midi["F1"]                       # the key lane counts semitones from F

    def note(at):
        m = F1 + [v for b, v in lane if b <= at + 1e-6][-1]
        for b in bass["notes"]:
            if b["at"] - 1e-3 <= at < b["at"] + b["len"]:
                m = midi[b["pitch"]]
        return m - 5 if hz(m) > float(top) else m

    drum = lambda m: f"ct-kit kit.k.pitch={nm(m)}" + (" " + over if over else "")
    foot["patch"] = drum(F1)
    for n in foot["notes"]:
        if note(n["at"]) != F1:
            n["patch"] = drum(note(n["at"]))
    if chest:
        semi, ms, fader = chest.split(":")
        doc["patches"]["ce-chest"] = {"extends": "808", "synth": {"layers": ["sine"], "pitch": {"value": 0, "mod": []}, "drive": 0, "filters": [],
                                                                 "amp": {"a": "2ms", "d": f"{ms}ms", "s": 0, "r": "20ms", "curve": 3}},
                                      "play": {"mono": False, "glide": "0ms", "gate": 1}}
        doc["tracks"].append({"name": "chest", "patch": "ce-chest", "gain": fader, "pan": 0,
                              "notes": [{"at": n["at"], "len": 0.25, "pitch": nm(note(n["at"]) + int(semi)), "vel": n["vel"]} for n in foot["notes"]]})
    if target:
        doc["loudness"] = float(target)


def the_band_leaves_every_fourth(doc, marks):
    """v20: in one section the parts that are in the rule rest for one whole pulse in every so many; the pair, and
    whoever keeps the bar (the snare, the crash), go on."""
    sec, every, first, times, who, target = LEAVES.split(";")
    name, b, r, bars = next(m for m in marks if m[0] == sec)
    pulse = 1 / Fr(r)                                                       # beats
    shown = SHOWN and sec in [e.split("=")[0] for e in SHOWN.split("|")[0].split(";")]
    start = b + (4 if shown else 0)                                          # the first pulse the band plays
    held = b + 4 * (bars - SLIDES.get(sec, 0))                               # where the peg begins to turn
    tracks = {t["name"]: t for t in doc["tracks"]}
    for k in range(int(times)):
        a = start + (int(first) + int(every) * k) * pulse
        z = a + pulse
        assert z <= held, (sec, k, float(a))                                 # never while the peg turns
        gone = 0
        for n in filter(tracks.get, who.split(",")):
            before = len(tracks[n]["notes"])
            tracks[n]["notes"] = [x for x in tracks[n]["notes"] if not float(a) - 1e-6 <= x["at"] < float(z) - 1e-6]
            gone += before - len(tracks[n]["notes"])
        assert gone, (sec, k)
    assert all(t["notes"] for t in doc["tracks"])
    if target:
        doc["loudness"] = float(target)


def the_reeds_have_their_twelfth(doc):
    """v19: each of the two reeds (and the turned reed, which is the sharp one while the peg moves) gets one more rank
    at three times its own note, so the pair's third overtone, the toms' number, sounds and swells as its others do."""
    ratio, wave, level, fader, target = TWELFTH.split(";")
    rank = f" synth.layers.4.wave={wave} synth.layers.4.ratio={ratio} synth.layers.4.level={level}"
    for t in doc["tracks"]:
        if t["name"] in ("reed", "hair"):
            assert t["patch"] == PAIR, t["patch"]
            t["patch"] += rank
            if fader:
                t["gain"] = f"{float(t['gain'][:-2]) + float(fader):g}dB"
    turned_reed = doc.get("patches", {}).get(GLIDER)
    if turned_reed:
        assert turned_reed["extends"] == PAIR
        turned_reed["extends"] += rank
    if target:
        doc["loudness"] = float(target)


def the_string_gives(doc):
    """v18: the lead follows the peg into the two bars by its own rule (v10); here it is told how loudly."""
    where, bar, _, lead, target = GIVES.split(";")
    b0 = 0
    for name, r, bars, ground, who in FORM:
        if name == where:
            break
        b0 += 4 * bars
    b0 += 4 * (int(bar) - 1)
    t = next((t for t in doc["tracks"] if t["name"] == "bend"), None)
    if t and lead == "none":
        t["notes"] = [n for n in t["notes"] if not b0 <= n["at"] < b0 + 8]
    elif t and lead:
        for n in t["notes"]:
            if b0 <= n["at"] < b0 + 8:
                n["gain"] = f"{float(lead):g}dB"
    if target:
        doc["loudness"] = float(target)


def the_fifth(doc, marks):
    """v14: the handpan says the pair's fifth overtone, five strokes to the pulse, in one section of constant width."""
    sec, plan, gain, pan, eq, vels, ring, target, damped = FIFTH.split(";")
    name, b, r, bars = next(m for m in marks if m[0] == sec)
    ground = next(x[3] for x in FORM if x[0] == sec)
    pulse, f = 1 / Fr(r), hz(REED + ground)
    plan, vels = plan.split(","), [float(v) for v in vels.split(",")]
    assert len(plan) == bars and len(vels) == 5 and (4 / pulse).denominator == 1, (len(plan), bars)
    notes = []
    for bar, said in enumerate(plan):
        for d in said:
            if d == "0":
                continue
            at = b + 4 * bar + (int(d) - 1) * pulse
            for j in range(5):
                notes.append({"at": round(float(at + Fr(j, 5) * pulse), 5), "len": round(float(pulse / 5) * float(ring), 5),
                              "pitch": f"{5 * f:.3f}hz", "vel": vels[j]})
    doc["tracks"].append({"name": "pan-five", "patch": PAN.split(";")[0] + (" " + damped if damped else ""), "gain": gain, "pan": float(pan), "notes": notes,
                          **({"fx": [{"type": "eq", "bands": eq.split("|")}]} if eq else {})})
    if target:
        doc["loudness"] = float(target)


def the_hand_says_the_count(doc):
    """v17: the four guitars' palm closes the string's filter less far, and its weight on each muted stroke is the
    count that stroke says: two (half way between two kicks), three (on the thirds), four (on the quarters)."""
    from bisect import bisect_right
    reach, weights, mic, band, _ = HAND.split(";")
    weights = [float(x) for x in weights.split(",")]
    tracks = {t["name"]: t for t in doc["tracks"]}
    kicks = sorted(n["at"] for n in tracks["foot"]["notes"])
    places = [(Fr(1, 2), 0), (Fr(1, 3), 1), (Fr(2, 3), 1), (Fr(1, 4), 2), (Fr(3, 4), 2)]
    for name in ("left", "right", "left" + ALSO, "right" + ALSO):
        t = tracks[name]
        t["patch"] += f" synth.filters.0.cutoff.mod.0.amount={reach} fx.2.mic={mic}"
        assert t["fx"][0] == {"type": "eq", "bands": ["peak cutoff=700 q=0.9 gain=2.5dB"]}, t["fx"][0]
        t["fx"] = ([{"type": "eq", "bands": band.split("|")}] if band else []) + t["fx"][1:]
        if not t["fx"]:
            del t["fx"]
        for n in t["notes"]:
            if n.get("expr", {}).get("pm"):
                i, w = bisect_right(kicks, n["at"] + 1e-6), weights[-1]
                if 0 < i < len(kicks):
                    cell = kicks[i] - kicks[i - 1]
                    if i >= 2 and cell > 1.5 * (kicks[i - 1] - kicks[i - 2]):     # the kick rests next: the pulse it was in
                        cell = kicks[i - 1] - kicks[i - 2]
                    p = (n["at"] - kicks[i - 1]) / cell
                    d, k = min((abs(p - float(q)), k) for q, k in places)
                    if d < 0.045:
                        w = weights[k]
                n["expr"] = {**n["expr"], "pm": w}


def the_pair_shows_the_count(doc, marks):
    """v16: in the first bar of each named section the band rests and the pair is heard pulsing the new count."""
    entries, kept, target = SHOWN.split("|")
    kept = set(kept.split(","))
    start = {name: b for name, b, r, bars in marks}
    for entry in entries.split(";"):
        section, stay = entry.split("=")
        a, stay = start[section], {x for x in stay.split(",") if x}
        for t in doc["tracks"]:
            if t["name"] not in kept and t["name"] not in stay:
                t["notes"] = [n for n in t["notes"] if not a <= n["at"] < a + 4]
    assert all(t["notes"] for t in doc["tracks"])
    if target:
        doc["loudness"] = float(target)


def fretted(doc, marks):
    """v15: for a bar the pair is stopped a fret higher with the peg left alone. The hair keeps its width in cents,
    so it is wider in cycles by the interval, and everything in the rule is that much faster and that much higher."""
    sec, which, fret, n, target = FRET.split(";")
    name, b, r, bars = next(m for m in marks if m[0] == sec)
    ground = next(x[3] for x in FORM if x[0] == sec)
    was, n, fret = Fr(r) * 4, int(n), int(fret)
    assert was.denominator == 1, was
    cell, scale = float(4 / was), float(was / n)
    kits = {int(x.split("=")[0]): x.split("=")[1].split(",")[0].lower() for x in TOMS.split(";")}
    skins = lambda g: "skins" if g == 0 else "skins-" + kits[g]
    tracks = {t["name"]: t for t in doc["tracks"]}

    def up(p):
        return ",".join(f"m{float(q[1:]) + fret:.4f}" if q[0] == "m" else nm(NAMES.index(q[:-1]) + 12 * (int(q[-1]) + 1) + fret) for q in p.split(","))

    for bar in map(int, which.split(",")):
        assert 1 <= bar <= bars - SLIDES.get(sec, 0), bar            # a bar of constant width: not one the peg is turned in
        a = b + 4 * (bar - 1)

        def said(src, pitched):
            """The bar's first pulse, then its second as often as it takes: each in three quarters of its time (a
            kit stroke keeps its length, as at every width)."""
            old = [e for e in tracks[src]["notes"] if a - 1e-6 <= e["at"] < a + 4 - 1e-6]
            cells = [[e for e in old if a + k * cell - 1e-3 <= e["at"] < a + (k + 1) * cell - 1e-3] for k in (0, 1)]
            new = [{**e, "at": round(a + j * 4 / n + (e["at"] - a - min(j, 1) * cell) * scale, 5),
                    **({"len": round(e["len"] * scale, 5), "pitch": up(e["pitch"])} if pitched else {})} for j in range(n) for e in cells[min(j, 1)]]
            assert old and all(cells), src
            return old, new

        for src, dst, pitched in [(t, t, t != "foot" and t != "hat") for t in ("foot", "left", "right", "left" + ALSO, "right" + ALSO, "bass", "hat")] + [(skins(ground), skins(ground + fret), False)]:
            old, new = said(src, pitched)
            tracks[src]["notes"] = [e for e in tracks[src]["notes"] if e not in old]
            tracks[dst]["notes"] = sorted(tracks[dst]["notes"] + new, key=lambda e: e["at"])
        f = hz(REED + ground + fret)
        for tr, p in (("reed", f), ("hair", f + n / 4 * HAIR)):
            held = [e for e in tracks[tr]["notes"] if abs(e["at"] - a) < 1e-6]
            assert len(held) == 1 and set(held[0]) == {"at", "len", "pitch", "vel"} and abs(held[0]["len"] - 3.96) < 1e-6, held
            held[0]["pitch"] = f"{p:.3f}hz"
    if target:
        doc["loudness"] = float(target)


def the_toms_count(doc):
    """v13: the counting toms are shorter and louder; their box cut deeper, their own notes lifted."""
    patch, fader, band, target = STROKE.split(";")
    for t in doc["tracks"]:
        if t["name"].startswith("skins"):
            if patch:
                t["patch"] += "".join(f" kit.{piece}.patch.{o}" for piece in ("ft", "t2", "t1") for o in patch.split())
            if band:
                t["fx"] = [{"type": "eq", "bands": band.split(",")}]
            if fader:
                t["gain"] = fader
    if target:
        doc["loudness"] = float(target)


def in_tune(doc, end):
    """v11: the band's strings on the reeds' note, its fifths pure, the last chord let go after a bar, the lead's oscillator half a cycle on."""
    strings, low, pure, hold, osc, eq, target = ALONE.split(";")
    names = "C Db D Eb E F Gb G Ab A Bb B".split()
    midi = lambda n: names.index(n[:-1]) + 12 * (int(n[-1]) + 1)
    last = end - 8                                       # the last chord's beat
    for t in doc["tracks"]:
        guitar = t["name"] in ("left", "right", "left-said", "right-said")
        if guitar and strings:
            t["patch"] += " " + strings
        if t["name"] == "bass" and low:
            t["patch"] += " " + low
        if guitar and pure:
            for n in t["notes"]:
                ps = str(n["pitch"]).split(",")
                if len(ps) > 1:                          # root first; an octave stays a name, a fifth or twelfth becomes 3:2 or 3:1 of the root
                    root = midi(ps[0])
                    n["pitch"] = ",".join([ps[0]] + [q if (midi(q) - root) % 12 == 0 else "m%.4f" % (root + 12 * math.log2({7: 1.5, 19: 3}[midi(q) - root])) for q in ps[1:]])
        if (guitar or t["name"] == "bass") and hold:
            for n in t["notes"]:
                if n["at"] == last:
                    n["len"] = float(hold)
    if osc and "ce-bend" in doc.get("patches", {}):
        doc["patches"]["ce-bend"]["synth"]["layers"] = [osc]
    if eq:
        next(t for t in doc["tracks"] if t["name"] == "bend")["fx"] = [{"type": "eq", "bands": ["peak cutoff={} q={} gain={}dB".format(*b.split(":")) for b in eq.split(",")]}]
    if target:
        doc["loudness"] = float(target)


def unison_bend(doc):
    """v10: a lead on two strings an octave over the pair, wherever the peg is turned once the band is in; appended LAST."""
    which, gain, cut, drive, pre, cone, attack, target, eq = BEND.split(";")
    band_in = 0
    for name, r, bars, ground, who in FORM:
        if "g" in who:
            break
        band_in += 4 * bars
    by = {t["name"]: t for t in doc["tracks"]}
    still = {n["at"]: n for n in by["reed"]["notes"]}
    twice = lambda pitch: f"{2 * float(pitch[:-2]):.3f}hz"
    turned = [n for n in by["hair"]["notes"] if "expr_end" in n and n["at"] >= band_in]
    if which == "close":
        turned = turned[-1:]
    notes = []
    for n in turned:
        notes.append({"at": n["at"], "len": n["len"], "pitch": twice(still[n["at"]]["pitch"]), "vel": 0.9})
        notes.append({"at": n["at"], "len": n["len"], "pitch": twice(n["pitch"]), "vel": 0.9, "expr": n["expr"], "expr_end": n["expr_end"]})
    doc.setdefault("patches", {})["ce-bend"] = {
        "about": ("chirper-zero: Close Enough's unison bend: a sustaining lead on two strings a hair apart through one amp. The library's m8-lead as one saw "
                  "(no detuned layer, no vibrato, no echo, no room: each of those wobbles or smears), the album's lead amp at half gain and the engine's "
                  "cabinet; its pitch follows a note's `slide`, in semitones, as the turned reed's does, and it plays each note to its end (gate 1: at the "
                  "default a slide finishes at 95% of the note)"),
        "extends": "m8-lead",
        "synth": {"pitch": {"value": 0, "mod": [{"src": "expr.slide", "amount": 1}]}, "layers": ["saw"],
                  "filters": [{"kind": "lp", "cutoff": float(cut), "q": 0.8}], "amp": {"a": attack + "ms", "r": "150ms", "s": 1}},
        "play": {"legato": False, "glide": "0ms", "gate": 1},
        "fx": [{"type": "gain", "gain": pre + "dB"},
               {"type": "amp", "model": "5150", "gain": float(drive), "ts": 0.3, "tight": 140, "boost": "0dB", "bass": 0.5, "mid": 0.68, "treble": 0.58,
                "presence": 0.6, "resonance": 0.55, "sag": 0.3, "bloom": 0.3},
               {"type": "cab", "model": "4x12-modern", "mic": 0.1, "distance": 0.15, "cone": int(cone)}]}
    doc["tracks"].append({"name": "bend", "patch": "ce-bend", "gain": gain, "pan": 0,
                          **({"fx": [{"type": "eq", "bands": ["peak cutoff={} q={} gain={}dB".format(*b.split(":")) for b in eq.split(",")]}]} if eq else {}),
                          "notes": notes})
    if target:
        doc["loudness"] = float(target)


def spans_of(names):
    out, at = [], 0
    for name, r, bars, ground, who in FORM:
        if name in names.split(","):
            out.append((at, at + 4 * bars, ground))
        at += 4 * bars
    return out


def a_hat_with_a_body(doc):
    """v12: the closed hat gets a kit of its own (the crash and china on `brass` keep the album kit), a drier room and an eq."""
    over, fader, room, bands, target = HAT.split(";")
    doc.setdefault("patches", {})["ce-hat-kit"] = {
        "about": ("Close Enough's closed hat (chirper-two, 19 Nov): the album kit with the library's closed hat (haake-hat: white noise "
                  "and three squares through an 8 kHz high-pass, 45 ms) opened downwards and shortened, so it has a body under 8 kHz."),
        "extends": "ct-kit", "kit": {"h": {"patch": "haake-hat " + over, "gain": "-10dB", "choke": "hat"}}}
    hat = next(t for t in doc["tracks"] if t["name"] == "hat")
    assert hat["patch"] == "ct-kit" and all(n["pitch"] == "h" for n in hat["notes"])
    hat["patch"], hat["gain"] = "ce-hat-kit", fader
    hat["sends"] = {"oh": room}                                          # new objects: `brass` shares the old ones
    hat["fx"] = [{"type": "eq", "bands": bands.split(",")}]
    if target:
        doc["loudness"] = float(target)


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
