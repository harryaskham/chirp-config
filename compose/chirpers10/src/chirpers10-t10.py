#!/usr/bin/env python3
"""Still Owing (Common Time t10). Two bars to spend, never a tick more.

Each half has a recognisable touch: a low open E-flat and two palm strokes
on the call; a higher chord and a four-note falling answer on the reply.
With debt d, the two halves take 16+d and 16-d sixteenths. The players really
stretch their figures; it is not just a shifted downbeat. The kit never follows
that private tempo. A dry piano marks the middle of the pair; a struck key on
a wave terrain marks where the reply actually arrives. They part, then meet.
"""
import argparse
import json
import os
from collections import defaultdict
from pathlib import Path

BPM, SUB, BAR, HOME = 112, 4, 16, 27  # E-flat 1
MAX_DEBT = 6
FORM = [('at par', [0]*3), ('in hand', [0]*5), ('on account', list(range(MAX_DEBT+1))),
        ('still owing', [MAX_DEBT]*6), ('two clocks', [6, 4, 2, 0]),
        ('called in', list(range(MAX_DEBT, -MAX_DEBT-1, -2))),
        ('across the line', [d for width in (6, 5, 4, 2) for d in (width, -width)]),
        ('square', [0]*5), ('the receipt', [0])]
NOTES = 'C Db D Eb E F Gb G Ab A Bb B'.split()
OUT = Path(__file__).resolve().parents[3] / 'songs/chirpers10-t10.yaml'
# v2: the length of the reply picks its player in 'across the line' alone.
# Bowed lyre on the left, picked guitar on the right. As the two clocks
# converge the guitars rejoin from the end of the phrase. Empty = v1 exactly.
TRADE = os.environ.get('C10T10_TRADE', '-5')
# v3: on the repeat of each crest root, spend the six borrowed sixteenths
# on a reverse pickup made from the following answer. Empty = published v2.
ADVANCE = os.environ.get('C10T10_ADVANCE', '7.5')
# v4: after the players return to straight time, one more note of the answer
# can ring each time around. Track gain in dB; empty reproduces v3 exactly.
COURSES = os.environ.get('C10T10_COURSES', '-11')
# v5: 'called in' puts the straight clock into the right guitarist's hands.
# Semitones above the low part; the left joins that register at par. Empty = v4.
STRAIGHT = os.environ.get('C10T10_STRAIGHT', '12' if COURSES else '')
# v6: repay each clock gap as the length of a note. Empty restores v5;
# omitting STRAIGHT still gives the pre-crossing arrangement.
PAYBACK = os.environ.get('C10T10_PAYBACK', '1' if STRAIGHT else '')
# v7: breath and pick are the two halves before anybody borrows a tick.
# Empty gives v6 exactly; PAYBACK empty still gives the pre-fill version.
BREATH = os.environ.get('C10T10_BREATH', '-15' if PAYBACK else '')
# v8: count the first debts on damped bronze keys. Track gain; empty = v7.
CHANGE = os.environ.get('C10T10_CHANGE', '-11.5' if BREATH else '')
# v9: once the answer arrives early in 'called in', a pressure drum takes the
# terrain key's stroke and bends to the pitch of the square guitar. Empty = v8.
PRESS = os.environ.get('C10T10_PRESS', '-13' if CHANGE else '')
# v10: the distance between the two markers becomes the bassist's step.
# Fraction of the step held; empty restores v9 and earlier switches.
STRIDE = os.environ.get('C10T10_STRIDE', '.80' if PRESS else '')
# Before a downbeat moves, the brush borrows *duration*. Empty restores v10.
BRUSH = os.environ.get('C10T10_BRUSH', '-7' if STRIDE else '')
# v12: at the crest the baritone still plays the call in the bar it was given.
# First time on each ground only (the second time has the backwards pickup).
# Semitones over the guitars' call ; its lift over the opening, dB ; 1 = the
# third guitar gives its call chord to the reed. Empty restores v11.
# Benched an octave lower (its opening register): 10 dB under the mix and the
# short third note 13-14 under. Up here it is a line, so it needs less lift,
# and the third guitar keeps its chord where each new ground arrives.
RECALL = os.environ.get('C10T10_RECALL', '24;3;0' if BRUSH and BREATH else '')
# v13: what the mallet buys is kept on account. The bronze count is damped,
# so each new note of the answer was gone as soon as it was struck. Now the
# newest key is left sounding (a bow on the bar's edge, so it holds under the
# band) until the next one is bought: G flat, F, C, then E flat, the answer
# at a thirty-third of its speed over the riff that will not leave E flat.
# Each lasts one pair and the sixteenth just borrowed; the last is damped a
# sixteenth before the plain late pairs. Its shimmer is the drummer's clock:
# one beat of the paired tuning for every straight sixteenth.
# Track gain in dB ; depth of the shimmer. Benched at -17: 7.5 dB under the
# raw mix and four fifths of everything at 500-1000 Hz, a test tone. At -24:
# 14 under, but the passage read 2.3 dB over the records at 500-1000 Hz
# (0.4 without it). So -27, and the two lower keys 2 dB less again: the band
# leaves less in their semitones, and they stood 5 dB further out of it.
# Empty restores v12; it is on only
# while every older switch is, so each of those still gives what it gave.
KEPT = os.environ.get('C10T10_KEPT', '-27;0.55' if all((
    RECALL, BRUSH, STRIDE, PRESS, CHANGE, BREATH, PAYBACK, STRAIGHT, COURSES, ADVANCE, TRADE)) else '')
# v14, whole song: THE GROUND RISES WITH THE CREDIT. From the pocket at 1:30 to
# the line at 2:17 the riff sat on E flat for seven pairs running, and the
# line's first low chord, A flat, arrived from nowhere. Once the answer starts
# to come EARLY, the whole band now climbs to meet that chord: the pair four
# ticks in credit is on F, the pair six in credit on G flat, and the line's
# A flat is the next step. The song's first minute borrows on a ground that
# will not move and climbs only at full debt (E flat, G flat, A flat); its
# second half now climbs as the debt turns to credit, by step, to the same A
# flat. Guitars, bass, the straight guitar and the pressure drum all move
# together (the drum bends to the answer's first note on each new ground).
# And the third guitar, the wall chord that carries the crest and the line,
# strikes each new ground and its answer: the three climbs share one voice.
# Semitones over E flat for the pairs two, four and six ticks in credit ;
# 1 = the wall chord on each raised ground. Empty restores v13; it is on only
# while KEPT is.
LADDER = os.environ.get('C10T10_LADDER', '0,2,3;1' if KEPT else '')
# v15 (palette): THE QUIET ROOM HAS ITS OWN BASS AND ITS OWN FOOT. The song is played by two bands: the loud one, and a
# small quiet one that is heard before it at 0:00 and inside it at 1:30: a baritone sax, a clean guitar, a piano, a
# brush on the snare (0:26). The quiet band had no bass of its own: in both of its rooms the eight-string band's bass
# guitar played for it, and at 0:04 and 0:08 the metal kit's kick. Now the quiet band has an UPRIGHT BASS, plucked
# (the library's `upright-bass`; no other song on the record has one): the two low E flats under the sax, the four
# pedals of the pocket (A flat, G flat, E flat, E flat) and the three notes that pay the pocket's debts back (G flat,
# F, C, with the toms). And its foot is the brush kit's feathered bass drum, on the brush's own track. So the first
# stroke of the bass guitar and of the metal kick drum is the loud band's entrance at 0:12.9 (its hat, snare and one
# muted guitar still steal in at 0:08.6, as they did), and after the pocket the bass guitar comes back on the
# downbeat of 1:47.1. No note is added, moved or removed. In v14 the metal kick at 0:08.6 was the introduction's
# loudest instant, 5 dB over full scale before the limiter, which turned everything down 6 dB to pass it.
# patch (with overrides) ; track gain dB ; semitones against the bass guitar's written notes ; the feathered kick's
# gain over the brush track (dB ; empty leaves the metal kick in the introduction). Empty restores v14; it is on only
# while LADDER is.
# Benched raw, seed 0. The library patch as it is, at 0 dB: 2 to 10 dB over the bass guitar's notes (K), and its
# pedal 24 dB down before the end of its ten sixteenths (the bass guitar's is held). So: the string's decay doubled
# (1.7 s to 3.4 s: 10 to 12 dB down at the end), the note's whole written length (gate 1), and a track gain at which
# the pocket reads as loud as it did (at -4 it was 0.15 LU over v14 finished, at -5 0.27 under).
ROOM = os.environ.get('C10T10_ROOM', 'upright-bass play.gate=1 play.humanize.time=0ms play.humanize.vel=0 '
                      'synth.layers.0.decay.value=3.4s;-4.5;0;0' if LADDER and BRUSH else '')
# A plucked pedal dies away where the bass guitar's was held, so a few of the pocket's quietest moments fall under
# the loudness meter's gate and the file read 0.024 dB louder: every other bar came out that much quieter. This target
# gives those bars the gain they had in v14.
ROOM_LUFS = -9.976
# v16 (section, 0:00-0:34): THE LOUD BAND'S FIRST WORD IS AN ANSWER. The song is played by two bands, and the pair is
# two halves: a call and its answer. In the introduction the quiet band has both (the sax calls, the pick answers),
# three times. The loud band then took both at once, on the call, at 0:12.9. Now the sax calls a FOURTH time, exactly
# as it called the third (the reed closed for the muted strokes, the upright, the soft foot, the hat and the backbeat
# stealing in), and where the pick has answered three times the loud band answers instead: its first stroke is the
# higher chord at 0:15.0, the crash and the kick with it, and the four falling notes are its way in to the riff. Its
# first low E flat is then the downbeat of 0:17.1, the straight pair the so-debt card plays, which keeps every note.
# So before anyone borrows a tick the two halves have changed hands one at a time, and the half that will owe is
# the one the loud band took first.
# (Benched the other way round and not kept: the loud band calls at 0:12.9 and the pick answers once more. The song
# then stops two seconds after it starts, the scorer hears the loud band arrive at 0:17 and reads the first eighteen
# seconds as one section, 95.9/94.1 -> 93.6/91.1; and the card's first chord follows a silence instead of a bar.)
# Empty restores v15; it is on only while ROOM is.
ANSWER = os.environ.get('C10T10_ANSWER', '1' if ROOM else '')
# v17 (chirper-one; palette): WHAT IS STILL OWED IS THE LENGTH OF THE BOOM. 'Called in' is the song's half-time
# section, and since v10 the bassist's step there is the debt itself: a note every six sixteenths while six are owed,
# every four while four are, every two while two are, and at par he stops counting. It was the staple bass guitar,
# each step held four fifths of its length: a line that got busier. THE SWAP: those thirty steps (1:47.1-2:00.0) go
# from the bass guitar to an 808 (the library's `808-dist`, a long sub with a pitch-drop punch, driven so it speaks on
# small speakers; no other song on the record has one), which is one voice: each boom rings until the next cuts it.
# So what is still owed is how long the boom lasts: six sixteenths, then four, then two, and on the downbeat of
# 2:00.0, where nothing is owed, the last one is cut and the bass guitar comes back on its held E flat, as before.
# The bass guitar rests for those three pairs (its first rest inside a loud section); the notes, their places and
# their pitches are the bassist's own, unmoved. The 808 plays nowhere else.
# Benched raw, seed 0, each alone on the same thirty steps. At -15 dB the 808 was 2.5 dB over the bass guitar it
# replaces (1.9 K), the raw mix +0.6 dB and +2.9 at 20-60 Hz. At -17 it is level with it (+0.5 dB, 0.0 K) and the
# mix within 0.1 dB; a boom falls 0.3 to 0.7 dB over its own length, so it is the next one that ends it. Against the
# bass guitar it has 2 to 3 dB more under 60 Hz and 3 to 5 less at 60-120 Hz.
# What it gave up was 60-120 Hz, where this song is already short (the scorer's worst band on every seed is 97 Hz):
# finished, the three pairs went from 2.0 to 3.7 dB short of the eleven records there. So one eq band on the 808's
# own track, 5 dB at 95 Hz, and the fader 1.5 dB down to hold its level: it gets about 2 dB of that band back, and
# note by note it then follows the bass guitar's own balance more closely (the spread across the five pitches of
# the steps goes from 2.2 dB to 1.0). Raising the patch's octave-up triangle layer instead did nothing (benched).
# patch ; track gain dB ; semitones against the written steps ; the song's loudness target (every bar outside the
# three pairs keeps v16's mastering gain: at v16's target they came out 0.004 dB louder) ; one eq band on its track
# (leave the field out for none). Empty restores v16; it is on only while ANSWER and STRIDE are.
BOOM = os.environ.get('C10T10_BOOM', '808-dist;-18.5;0;-9.98;peak cutoff=95 q=1.2 gain=5dB' if ANSWER and STRIDE else '')
# v18: THE BOW GETS A STRING AND A BODY (instrument round, chirper-zero, 19 Nov). Harry on the card so-bow, "Does
# trading the answer between pick and bow work?": "bow instr sounds not great, improve".
# THE INSTRUMENT: the bow of 'across the line' (2:22-2:52: sixteen notes, the answer Gb-F-C-Eb four times, alone on the
# left over a held bass and a quarter-note hat). It was the library's body-less tagelharpa string, which its own
# description calls experimental ("short notes barely speak").
# WHAT WAS WRONG, read alone on its first two phrases: (1) IT COULD NOT HOLD ITS OCTAVE. On the long notes the string
# sat in its second mode: at F3 the first harmonic stood 17 dB UNDER the second the first time and 3 over it the
# second; Gb3 -6 then +2; C3 0 then -12. The same four notes came out in a different register each phrase.
# (2) THE SHORT NOTES WERE A QUARTER SCRATCH: on the C and the E flat (0.5 and 0.3 s) only 76 to 78% of the power was
# on the note's harmonics. (3) THE TOP WAS NEARLY AS LOUD AS THE NOTE: above 2 kHz it stood 3 to 8 dB under everything
# below. In the mix the first phrase read +8.1 dB over the records at 250-500 Hz (the octave-up tone) and +4.3 at
# 8-16 kHz (the scratch).
# NOW: a bowed string on a body (the engine's bowed waveguide with the cello's string and box: this register is the
# cello's own), song-local patch `owing-bow`. The first harmonic leads the second by 4 to 5 dB on all eight notes
# read; 96 to 99% of the power is on the harmonics; harmonics 2 to 6 fall -5 -10 -12 -13 -14, a bowed string's
# sawtooth. Each stroke swells 5 dB in 200 ms and eases; vibrato (15 cents each way, 5.3 Hz) only from 200 ms in, so
# only the two long notes have it. The body alone gave too much first harmonic (2 to 6: -9 -14 -17 -18 -19), so a
# low shelf in the patch holds it back 6 dB below 300 Hz.
# ITS LEVEL IS SET BY THE MASTER'S LIMITER, a thing I learned the hard way: a bowed string's wave is a spike every
# period, and this song's limiter turns down anything whose spikes pass about -10 dBFS before the loudness gain. A
# brighter voicing I tried (shelves of -9 and +5 dB; crest 19.7 dB) matched the old bow's loudness on the bench and came
# out 4.5 LU under it in the full render; this voicing at the old bow's loudness came out 2 under. So the fader puts
# the bow's highest sample at -10.5 dBFS raw (crest 15.9 dB): the limiter leaves it alone, and the bow answers about
# 2 LU softer than the old one did. (A short room ahead of the hall smears the spikes, crest 14.9, but colours each
# note differently; tape drive does little: both benched, neither kept.)
# track gain dB ; the low shelf's corner Hz ; its gain dB. '' = v17 (the tagelharpa at TRADE's gain).
BOW = os.environ.get('C10T10_BOW', '-0.7;300;-6' if BOOM and TRADE else '')
# v19 (chirper-two, whole song): THE LOUD BAND MOVES INTO THE RECORD'S ROOM. This song was stood up before the
# record's band staging settled, and it still had its first one: guitars and bass straight to the master, a kit bus
# with a shallow cut. Read against the eleven records at v18, every loud section said the same three things: 2.5 to
# 4.3 dB too much at 250-500 Hz, 1.0 to 2.0 too much under 60 Hz, 0.8 to 1.6 too little at 60-120 Hz (the scorer's
# worst band on every seed is 97 Hz). By part: the bass guitar stood 13.7 dB over the records' basses under 60 Hz,
# 3.7 under them at 60-120 and 9.0 over at 250-500; the kit 5.7 and 6.0 over the records' kits at 250-500 Hz and
# 500 Hz-1 kHz. So:
#   the bass guitar goes through the record's low bus (as In the Time Of and Close Enough carry it): an eq that
#     follows the ground under each pair (less at the ground's own octave, more an octave up, a cut at 350 Hz, a
#     little growl at 1.5 kHz) and a compressor;
#   the two riff guitars and the wall get the record's guitar bus (a cut at 330 Hz, a short room) and the riff
#     guitars its 700 Hz lift;
#   the kit's bus cut is deeper and wider (450 Hz, -7 dB, was 390 Hz, -4) with 0.8 dB given back after it (the kit
#     had fallen 0.9 dB under the records' kits' share of the mix), and the kick loses 3.5 dB at 42 Hz.
# Tried on the way and not kept (each read against the records): the record's kit clip (4-8 kHz fell to 0.6 to 2.5
# dB under the records; it was within 1.0), its kick click (4.5 kHz +10 dB: 4-8 kHz up to 2.9 over), and the low
# bus's third band (-3 dB at 170 Hz) with a kit cut centred at 400 Hz (120-250 Hz fell 1.0 to 1.5 short).
# AFTER (the six loud sections, ours minus the records): under 60 Hz +1.0..+2.0 -> -0.3..+1.1; 60-120 Hz
# -0.8..-1.6 -> +0.7..-0.6; 250-500 Hz +2.5..+4.3 -> +1.0..+3.3 (what is left is 'called in', where the right
# guitar plays an octave up, and 'across the line', the bow's own octave). The scorer's 97 Hz: 8.7 -> 6.7 under.
# THE QUIET BAND IS NOT TOUCHED: the brush kit keeps the old kit bus under its own name; the upright, the sax, the
# clean guitar, the piano, the keys, the bow, the twelve-string and the 808 are where they were.
# the guitar bus's cut dB ; the riff guitars' 700 Hz lift dB ; the kit bus's cut ('cutoff q gain') ; the kick's sub
# cut (an eq band, or nothing) ; the low bus's makeup dB ; the loudness target (the quiet band keeps the gain it had) ;
# dB given back to the kit after its cut. '' = v18.
STAGE = os.environ.get('C10T10_STAGE', '-3;2.5;450 0.8 -7;peak cutoff=42 q=1.2 gain=-3.5dB;2.5;-9.941;0.8' if BOW and BOOM else '')
# v20 (chirper-zero, instrument round): THE RIFF GUITARS GET A CHEST. Read alone against a record's guitar heard
# alone (cabspec, 'on account'), the two riff guitars stood 8.0 dB under it from 141 to 282 Hz and 4.5 to 6.5 over
# it from 400 to 800 Hz: no chest, all nose. The records' guitar stems said the same (120-250 Hz 6.2 under, their
# middle half 1.5 wide), and the band the guitars did not hold was held by the bass (3.4 over the records' basses
# there). With no voice in this song the mix itself stood 0.3 to 2.0 over the records at 500 Hz-1 kHz (mean 1.1).
# (v19's read by part had left the left guitar out of the guitars, so they looked short and got 2.5 dB at 700 Hz.)
# So, after each riff guitar's cabinet: a chest (6.5 dB near 195 Hz) and 1.5 dB off near 560 Hz in place of the
# 700 Hz lift; and the bass makes room with one more band on its bus (6 dB off at 185 Hz, before its compressor;
# v19 had tried that band alone and the mix fell short there: the guitars were not yet in it). Nothing before the
# cabinet is touched: the amp is as tight as it was. A deeper cut (3.5 dB) read better alone and by part and took
# the mix to 0.5 UNDER at 500 Hz-1 kHz ('in hand' 2.0 under): the mix decided.
# AFTER: alone, mean distance from the record's guitar 3.03 -> 1.79 dB, 141-282 Hz -8.0 -> -3.0; by part the
# guitars at 120-250 Hz -6.2 -> -1.8 and the bass +3.4 -> -0.1; the mix at 500 Hz-1 kHz, six sections, mean +1.1
# -> 0.0 (120-250 Hz +0.8 -> +1.0, 1-2 kHz 0.0 -> -0.4).
# the riff guitars' eq bands 'Hz:q:dB,...' ; one more band on the low bus 'Hz:q:dB' (or nothing) ; the loudness
# target (what plays without the riff guitars and the bass guitar keeps the gain it had: the song reads 0.3 LU
# lower, because the 700 Hz lift was loudness). '' = v19.
CHEST = os.environ.get('C10T10_CHEST', '195:1.3:6.5,560:1:-1.5;185:1:-6;-10.239' if STAGE else '')
# v21 (chirper-one, whole song): THE DRUMMER KEEPS THE ACCOUNT, AND THE BAND BUILDS AS IT BORROWS. The drummer never
# follows the guitars' private tempo (the song's first rule), and until now he did not show the debt at all: the same
# closed hat, tip of the stick, at par and at six owed, 31 dB under the band. And the loud band played one level:
# 'in hand', 'on account' and 'still owing' read -13.4, -13.5 and -13.1 (K) in the finished file.
# (1) HIS HAT IS AS FAR OPEN AS THE DEBT in 'on account' (0:34-1:04), where the debt grows a sixteenth a pair: tip,
# tip, shank, a quarter open, half, three-quarters, open, for none to six sixteenths owed; the ride's edge takes
# over at the crest as it always has. An opened hat rings until the next stroke closes it. He still plays every
# stroke where he played it.
# (2) THE BAND BUILDS. Its three buses (guitars, bass, kit) ease down 2 dB through the two brush pairs that end 'in
# hand', and come back a sixth of the way with each sixteenth borrowed: full again on the pair that owes six. The
# quiet band's instruments (brush, piano, the keys) are not on those buses, so they stand a little clearer while
# little is owed.
# Benched raw, each alone: the hat goes from -57.9 dB (K) at one owed to -45.1 at six, 31 under the band to 20 under,
# and from 19 dB under everything else's own 4-16 kHz to 8 under. The master takes back more than half of the
# band's 2 dB: finished, the build is about 1.2 dB.
# BUILT, RENDERED AND NOT KEPT: the same hat through 'called in' (1:47-2:17, half-time: open at six, closing to the
# tip at par, opening again on credit). That section's dry closed hat is part of what sets it apart: with the hat
# opened there the scorer cut five sections where it cut six on both seeds read (96.7 / 96.8 -> 95.6 / 95.6), while
# the hat in 'on account' alone read 97.4 / 98.3. The third field takes it back ('on account,called in').
# the hat's stroke by sixteenths owed, 0 to 6, comma between (the kit's h tip, hs shank, h1/h2/h3 quarter, half and
# three-quarter open, oh open) ; dB on each of those strokes ; the sections it is kept in ; dB the loud band's three
# buses come down by where the borrowing starts (0 = no build) ; the loudness target ('' = unchanged). '' = v20; it
# is on only while CHEST is.
LEDGER = os.environ.get('C10T10_LEDGER', 'h,h,hs,h1,h2,h3,oh;0,0,0,0,0,0,0;on account;2;' if CHEST else '')
# v22 (chirper-alpha; whole song: its ending, 3:17.1-3:21.4): THE LAST CALL GETS NO ANSWER. The song is called Still
# Owing and nothing in it ever is: every pair pays inside two bars, 'square' squares it and 'the receipt' closes the
# account. It begins with a call that is answered (the reed's E flat, B flat, F at 0:00; the pick's four notes; the
# piano and the struck key on the bar line where the answer comes) and every call since has had its answer. So it
# ends on the one that does not: after the receipt's chord is damped the reed calls once more, the piano marks the
# bar line where the answer is due, the struck key (which marks where the answer arrives) does not strike, and the
# reed holds its last note through the bar the answer would have filled, falling away. Four notes; nothing before
# 3:17.1 changes. The call is 3 dB over the first one's: it follows the loudest chord in the song.
# dB on the last call against the first ; sixteenths the reed holds its last note past the bar line where the answer
# is due (0 = it stops short of it, as at 0:00) ; dB that note has fallen by when it lets go ; the piano's mark on
# that bar line, velocity ('' = none) ; sixteenths the song runs past that bar line ; the loudness target ('' =
# unchanged). '' = v21.
OUTSTANDING = os.environ.get('C10T10_OUTSTANDING', '3;16;-20;0.72;18;' if LEDGER and BREATH else '')
# v23 (chirper-zero; instrument round: the hi-hat, all 175 of its strokes, the whole song): THE HAT CAN BE HEARD, AND
# THE TOP IS THE CYMBALS'. No stroke moves. v21 made the drummer keep the account: in 'on account' the hat opens a
# notch with every sixteenth borrowed. But this song's hat sat on the cymbals' track at the cymbals' fader, as Where
# It Was's did until its v19: each closed stroke read 25 to 27 dB under the mix in its own tenth of a second, where
# the album's other hats read 12 to 15 under. The ladder began under the floor: its first three rungs (-25, -22, -21)
# were not there to be heard, and the hat of 'in hand', 'called in' and 'square' was not there at all.
#   THE HAT COMES UP TO THE ALBUM'S: the closed tip 10 dB (16 under the mix in 'in hand', 15 in 'square', 17 in the
#       half-time). THE LADDER STANDS ON IT, every rung louder than the last in its first tenth and ringing longer
#       (-15.0, -14.5, -13.6, -13.2, -12.4, -12.0 where -24.8, -22.4, -21.0, -17.6, -15.3, -16.9): the open hat at
#       the top comes up 5 dB, not 10, so it is a cymbal opening and not hiss arriving.
#   THE TOP CHANGES HANDS. Raised alone, the hat put the mix 0.7 to 2.2 dB further over the records at 8-16 kHz in
#       five stretches, because that band was already full and nothing in it was metal: the snare's wires held 56% of it and the
#       kick's click 21% (39% in 'square'), the cymbals 10%. So the kick is low-passed at 9 kHz, above its click (its
#       share of 4-8 kHz is where it was), and the snare gives 2 dB above 9 kHz (its wires stood 2.9 dB over its
#       crack where six records' snares stand level; 2.3 now). The cymbals hold 40 to 52% of the band now and the mix
#       is where it was against the records (mean distance at 8-16 kHz 1.21 > 1.19: nearer in four stretches,
#       further in three; the half-time 'called in' goes 1.0 under).
# kit overrides on the cymbals' track ; the kick's low-pass, Hz ('' = none) ; the snare's shelf, Hz:dB ('' = none) ;
# the loudness target ('' = unchanged). "" = v22 byte for byte.
TOP = os.environ.get('C10T10_TOP', 'kit.h.gain=0dB kit.hs.gain=-1dB kit.h1.gain=-1.5dB kit.h2.gain=-5.5dB kit.h3.gain=-7dB kit.oh.gain=-5dB kit.hp.gain=-4dB;'
                                   '9000;9000:-2;-10.229' if OUTSTANDING else '')
# v24 (chirper-three; the draw was a palette round, taken as ONE instrument changed: the snare, all 98 strokes; no
# stroke moves): THE SNARE IS FITTED TO THIS SONG. Three songs had the album's physical snare fitted to them (On Its
# Hinge v19, The Other Hand v20, Plain Hunt v33); this one had it as it comes, and louder than any of them.
#   ALONE at its 42 clean strokes in 0:10-1:35 (tools/drumpunch.py's measures; six records' snares in brackets): the
#       body (150-300 Hz) stood 5.0 dB OVER the crack (1.5-5 kHz) where the records' stand 3.2 under; the wires
#       2.4 over the crack (level); the stroke fell 16.4 dB in its first 50 ms (13.8) and rose in 2.0 ms (2.5 to 12).
#   IN THE BAND (raw, 0:13-1:30): the kit held 38% of everything at 250-500 Hz, the snare alone 23% (the kick 17%);
#       by part the kit read 4.8 dB over the records' kits at 250-500 Hz and 4.2 at 500 Hz-1 kHz. A stroke's first
#       30 ms stood 8.3 dB over everything else (K); The Other Hand's stood 4.2 over at its v19.
#   THE FIT: the +5 dB at 200 Hz the kit gives its snare becomes -5; the wires' buzz is centred at 5 kHz, not 7; a
#       slightly softer stick (contact 0.6 -> 0.9) and a head that rings a little longer (0.18 -> 0.24 s under a
#       200 ms envelope, was 140), which is what brings the fall after the stroke to the records'; a broad cut at
#       700 Hz on the track; the fader 1 dB down.
#   AFTER: alone, the body 3.5 dB under the crack, the wires 1.0 over, the fall 14.4 dB, the rise 2.5 ms: all five
#       measures inside the records' ranges (two were). By part the kit reads 2.5 over at 250-500 Hz and 2.9 at
#       500 Hz-1 kHz; a stroke stands 6.0 dB over everything else; the master pulls the band down 3.1 dB under a
#       stroke where it pulled 4.5. The mix against the records' voiceless passages: 0.772 -> 0.711, nearer in all
#       six stretches. COST: against the records' mixes with voices the top (8-16 kHz) reads 0.1 to 0.4 dB further
#       off in all six. No loudness target moved: the bars no stroke touches are within 0.014 dB on three seeds.
# kit overrides on the snare's track ; eq bands added to the track's eq (comma between bands) ; the fader, dB ;
# the loudness target ('' = unchanged). "" = v23 byte for byte.
SNARE = os.environ.get('C10T10_SNARE', 'kit.s.patch.synth.filters.1.gain=-5dB kit.s.patch.synth.layers.0.wire_tone=5000 '
                                       'kit.s.patch.synth.layers.0.contact=0.9 kit.s.patch.synth.amp.d=200ms '
                                       'kit.s.patch.synth.layers.0.decay=0.24s;'
                                       'peak cutoff=700 q=0.6 gain=-5dB;2;' if TOP else '')


def bow_patch():
    lo, lo_gain = (float(v) for v in BOW.split(';')[1:3])
    return {'about':'chirper-zero: the bow of Still Owing: a bowed string on a body (the engine\'s bowed waveguide, the cello\'s string and box), in place of the '
                    'body-less tagelharpa string. Each stroke swells a little and eases; vibrato only on notes long enough to have it; a low shelf keeps the '
                    'first harmonic from leading too far. Not a library patch.',
            'synth':{'filters':['lowshelf cutoff=%g gain=%gdB'%(lo,lo_gain)],
                     'layers':[{'type':'bowed','body':0.8,'body_size':2.2,'bow_attack':'50ms','bow_pos':0.1,'bow_speed':0.55,'bright':0.6,'pressure':0.78,'rosin':0.2,'speak':0.7,
                                'level':{'value':'0dB','mod':[{'src':'env.swell','amount':5.0}]}}],
                     'env':{'swell':{'a':'200ms','d':'800ms','s':0.6,'r':'150ms'}},
                     'lfo':{'vib':{'wave':'sine','rate':'5.3hz','delay':'200ms','fade':'300ms','retrig':True}},
                     'pitch':{'value':0,'mod':[{'src':'lfo.vib','amount':0.15}]},
                     'amp':{'a':'25ms','d':'0s','s':1,'r':'160ms'}},
            'fx':['reverb kind=hall decay=1.8s mix=0.1'],'gain':'0dB'}


# Offset in an ordinary bar, gate, semitones, open / palm / single note.
CALL = [(0,2.50,0,'o'), (3,.64,0,'m'), (4,.78,0,'m'), (6,2.25,7,'n'),
        (9,.62,0,'m'), (10,.78,0,'m'), (13,2.12,2,'n')]
# Four answer pitches Gb, F, C, Eb, from the album hook in a new order. The
# mutes between are pedal Eb. With six on credit this whole bar lasts ten ticks.
REPLY = [(0,3.35,15,'o'), (4,.74,0,'m'), (5,2.32,14,'n'), (8,.7,0,'m'),
         (9,.7,0,'m'), (11,1.76,9,'n'), (14,1.55,12,'n')]


def nm(p):
    return NOTES[p % 12] + str(p//12 - 1)


def chord(*p):
    return ','.join(map(nm,p))


def pressure_skin():
    # The short, inharmonic skin sound dies before the pitched bend. Only one
    # fingertip attack: the wrist moves the remaining modes up to the reply.
    layers = [
        {'type':'additive','partials':[[1,.85],[2,.88],[3,.55],[4.02,.38],[5.01,.21],[6.02,.13]],'damp':.38},
        {'type':'additive','partials':[[1.54,1],[2.43,.68],[3.14,.33],[5.16,.22]],
         'level':{'value':'-65dB','mod':[{'src':'env.skin','amount':56}]}},
        {'wave':'sine','ratio':.67,'level':{'value':'-65dB','mod':[{'src':'env.thud','amount':56}]}},
        {'type':'noise','color':'pink','level':{'value':'-66dB','mod':[{'src':'env.tap','amount':58}]}}
    ]
    return {
        'about':'Tuned pressure drum: a fingertip strike, a lower thud and a ringing head. The wrist moves the head pitch without a second attack.',
        'play':{'gate':1,'vel_sens':.6},
        'synth':{
            'layers':layers,
            'env':{'tap':{'a':'0.3ms','d':'17ms','s':0},'thud':{'a':'1ms','d':'95ms','s':0},
                   'skin':{'a':'0.4ms','d':'85ms','s':0}},
            'pitch':{'value':0,'mod':[{'src':'expr.press','amount':1}]},
            'filters':['hp cutoff=95','lp cutoff=6000'],
            'amp':{'a':'1ms','d':'2.4s','s':.24,'r':'45ms','curve':2}
        }
    }


def kept_key():
    # One key of the same bronze, bowed instead of struck: the bar's own pitch
    # with a little of its second and third modes, slow to speak, level while
    # the bow is on it. The song's track adds the shimmer, locked to the tempo.
    return {
        'about':'Still Owing: the bronze key the mallet has just struck, kept sounding with a bow on the edge of the bar. No attack of its own; the damped mallet stroke is its attack.',
        'play':{'gate':1,'vel_sens':.3,'humanize':{'time':'0ms','vel':0}},
        'synth':{
            'layers':[{'type':'additive','partials':[[1,1],[2.52,.085],[4.95,.022]]}],
            'filters':['hp cutoff=150','lp cutoff=5200'],
            'amp':{'a':'170ms','d':'1.2s','s':.82,'r':'120ms','curve':2}
        }
    }


def build():
    voices = defaultdict(list)
    sections = []
    fold_sources, fold_patches = {}, {}
    air_points = [[0,0]]
    call_heads = [p for p,_,_,how in CALL if how!='m']
    change_pitches = [semi for _,_,semi,how in REPLY if how!='m']
    def shade_breath(at, phrase):
        # The bore needs time to speak at Eb2. Articulate an already sounding
        # note rather than restarting it for two 90 ms strokes of mere air.
        for start,end in zip(call_heads,call_heads[1:]+[BAR]):
            taps=[p for p,_,_,h in CALL if start<p<end and h=='m']
            if not taps or phrase==0 or (phrase==1 and start!=0): continue
            pts=[(taps[0]-.65,0),(taps[0]-.25,-30)]
            if phrase==1:  # two short openings of the same low Eb
                for p in taps:
                    pts.extend([(p-.08,-30),(p+.06,0),(p+.51,0),(p+.68,-30)])
            pts.extend([(end-.26,-30),(end-.04,0)])
            air_points.extend([[f'{(at+p)/SUB:g}b',db] for p,db in pts])

    def note(track, tick, gate, pitch, vel, **expr):
        assert tick >= 0 and gate > 0 and 0 < vel <= 1
        n = {'at':round(tick/SUB,6), 'len':round(gate/SUB,6),
             'pitch':nm(pitch) if isinstance(pitch,int) else pitch, 'vel':round(vel,3)}
        if expr:
            n['expr'] = {k:round(v,5) for k,v in expr.items()}
        voices[track].append(n)

    def kit(piece, at, vel):
        tr = {'k':'kick','s':'snare','t1':'skins','t2':'skins','ft':'skins'}.get(piece,'metal')
        note(tr, at, 4 if piece in ('c','x','rde') else 1, piece, vel)

    def tally(at, p, d, length=3.0, vel=.83):
        note('tally', at, length, p, vel, owing=abs(d)/MAX_DEBT)

    def borrow(root, debt, midpoint):
        # Record this ground's first `debt` ticks of the COMPRESSED answer on
        # the introduction's clean guitar; no external samples or helper songs.
        ratio = (BAR-debt)/BAR
        name = f'owing-advance-{root}'
        src = name+'-source'
        heads = [{'at':round(pos*ratio/SUB,6), 'len':round(min(gate*ratio,debt-pos*ratio)/SUB,6),
                  'pitch':nm(root+semi+24), 'vel':.90 if pos==0 else .83}
                 for pos,gate,semi,how in REPLY if how!='m' and pos*ratio<debt]
        fold_sources[src] = {'tempo':BPM,'length':f'{debt/SUB:g}b','tail':'0s','seed':1,
                             'tracks':[{'name':'source','patch':'ct-clean synth.layers.0.inharm=0.00008 play.gate=1 play.humanize.time=0ms play.humanize.vel=0',
                                        'notes':heads}]}
        fold_patches[name] = {'play':{'gate':1},'synth':{'amp':{'a':'3ms','s':1,'r':'6ms'},
                              'layers':[{'type':'sample','song':src,'root':'C4','reverse':True}]}}
        note(name,midpoint,debt,'C4',1)

    def straight_gate(pattern, pos):
        # Lift the pick before the next pitched attack. No repeated pedal notes
        # between: this line has three strokes in the call and four in the answer.
        end = next((p for p,_,_,how in pattern if p>pos and how!='m'), BAR)
        return .72*(end-pos)

    pair = 2*BAR
    crest_roots = (0,0,3,3,5,5)
    t = 0
    pair_start = {}
    for s, debts in FORM:
        sections.append((s,t))
        for j,d in enumerate(debts):
            pair_start[s,j] = t
            width = BAR+d
            turn = t+width
            assert width+(BAR-d)==pair and 0<width<pair
            # The sustained middle climbs Eb -> Gb -> Ab. The following pocket
            # strips this to two strokes and lets the bass settle home on Eb.
            root = HOME
            if s == 'still owing': root += crest_roots[j]
            if s == 'two clocks': root += (5,3,0,0)[j]
            if s == 'square': root += (0,-2,-4,-2,0)[j]
            if LADDER and s == 'called in' and d < 0:
                rungs = [int(x) for x in LADDER.split(';')[0].split(',')]
                credit = sorted((-v for v in debts if v < 0))
                assert len(rungs) == len(credit)
                root += rungs[credit.index(-d)]
            if s == 'the receipt':
                # One straight low chord; the two middle markers coincide for
                # the last time, over the fifth returning to E-flat.
                for g in ('left','right'):
                    note(g,t,10,chord(HOME,HOME+7),.97)
                    note(g,turn,15.4,chord(HOME,HOME+7,HOME+12),1)
                for at,dur in ((t,10),(turn,15.4)):
                    note('bass',at,dur,HOME,.95); kit('k',at,1)
                note('rule',turn,7,HOME+36,.75); tally(turn,HOME+36,0,10,.88)
                kit('c',turn,.85); t+=pair; continue

            # What stays at home is a different sound from what moves. The
            # piano sometimes sits out, so the pair's end is not another click.
            early = change_pitches[:d] if CHANGE and s=='on account' and 0 < d <= len(change_pitches) else ()
            if early:
                # The mallet strikes the straight midpoint, always on Gb. Each
                # borrowed tick buys one more note before the full answer.
                for slot, semi in enumerate(early):
                    note('change',t+BAR+slot,.84,root+36+semi,.79 if slot==0 else .70)
                    if slot == 0:
                        voices['change'][-1]['gain'] = '3.5dB'  # keep the piano's downbeat accent
                if KEPT:
                    # The key bought this time rings until the next is bought,
                    # one sixteenth later in the following pair. After the
                    # whole answer there is nothing left to buy: lift it one
                    # sixteenth before the bar line.
                    bought = t+BAR+d-1
                    until = bought+pair+1 if d < len(change_pitches) else t+pair-1
                    note('kept',bought,until-bought,root+36+early[-1],.80)
                    if early[-1] < change_pitches[1]:
                        voices['kept'][-1]['gain'] = '-2dB'  # C and E flat, under the two keys that began the answer
            elif s in ('at par','in hand','on account','two clocks','across the line','square'):
                note('rule',t+BAR,2.2,HOME+31,.72 if s!='two clocks' else .89)
            if PRESS and s=='called in' and d<0:
                # The three early answers leave two, four and six ticks to the
                # straight reply. Start on its other three pitches, nearest
                # first (F3, Eb3, C3); squeeze the head up to Gb3 at the beat.
                target = root + change_pitches[0] + 12
                starts = sorted({root+p+12 for p in change_pitches if root+p+12<target}, reverse=True)
                gaps = sorted(-v for v in debts if v<0)
                assert len(starts)==len(gaps) and turn-d==t+BAR
                base = starts[gaps.index(-d)]
                ticks = -d
                note('pressure',turn,ticks+1,base,.86)
                # The note lasts one more tick at the destination. Half-tick
                # knots keep the bend on time even on the shortest stroke.
                path = []
                for half in range(2*(ticks+1)+1):
                    u = min(1., half/(2*ticks))
                    path.append(round((target-base)*u*u*(3-2*u),5))
                voices['pressure'][-1]['expr_path']={'press':path}
            else:
                tally(turn,root+39,d,4.2 if s=='two clocks' else 2.7)

            if s == 'two clocks':
                # A bass pedal to stand on; listen for the distance between
                # piano and tally contracting 6,4,2,0. No guitar or kit marks
                # their entrances, and they really do become one attack.
                note('bass',t,10,root,.82)
                note('clean',t,12,chord(root+24,root+31),.82)
                if PAYBACK:
                    # No attack between the markers. In the spare air at the end
                    # of each pair the clean string spends exactly its debt on
                    # ONE of the reply notes. At par, string lengths become a
                    # descending bass/tom fill; the next pair supplies the Eb.
                    amounts = [delta for delta in debts if delta>0]
                    pitches = [HOME+semi for _,_,semi,how in REPLY if how!='m']
                    if d:
                        pickup = t + pair-d
                        assert pickup > turn
                        note('clean',pickup,d-.24,pitches[j]+12,.92)
                    else:
                        pickup = t + pair-sum(amounts)
                        assert pickup >= turn+SUB and len(amounts)==len(pitches)-1
                        for dur,p,piece in zip(amounts,pitches[:-1],('t1','t2','ft'),strict=True):
                            note('bass',pickup,dur-.24,p,.90)
                            # Lighten the stick as the notes shorten: the last
                            # floor tom should not cover the bass player's C.
                            kit(piece,pickup,.35+.30*dur/max(amounts))
                            pickup += dur
                        assert pickup == t+pair
                else:
                    note('clean',turn+3,4,root+26,.75)
                    if j == len(debts)-1:
                        for i,piece in enumerate(('ft','t2','t1','s')):
                            kit(piece,t+pair-4+i,.53+i*.10)
                t+=pair; continue

            # One lick becomes an open chord. On the final Eb, the upper four
            # courses of a twelve-string tuned down a semitone take frets
            # 2/0/2/2 (Eb3/Gb3/C4/F4). Pick in melody order, not string order.
            repay = {}
            dry_from = 0
            if COURSES and s == 'square':
                positions = [pos for pos,_,_,how in REPLY if how != 'm']
                octaves = (12,24,24,12)
                assert len(positions) == len(octaves)
                count = len(positions) if len(debts)==1 else j*len(positions)//(len(debts)-1)
                repay = dict(zip(positions[:count], octaves[:count]))
                dry_from = positions[count] if count < len(positions) else BAR
            advance = bool(ADVANCE) and s == 'still owing' and j%2==1
            if advance:
                borrow(root, d, t+BAR)
            straight_call = bool(RECALL) and s == 'still owing' and j%2==0
            if straight_call:
                # The guitars take 22 sixteenths over Eb-Bb-F. The reed takes
                # the 16 it took at 0:00, so each note of its call comes a
                # little further ahead of theirs, and it stops on the bar line.
                register,lift,_ = RECALL.split(';')
                for p0,_,semi,how in CALL:
                    if how=='m': continue
                    following = next((pos for pos in call_heads if pos>p0), BAR)
                    note('breath',t+p0,following-p0-.25,root+semi+int(register),.90 if p0==0 else .83,sub=.12)
                    voices['breath'][-1]['gain'] = f'{float(lift):g}dB'
            crossing = bool(STRAIGHT) and s == 'called in'
            if crossing:
                for half,shape in enumerate((CALL,REPLY)):
                    for pos,_,semi,how in shape:
                        if how=='m': continue
                        p = root+semi+int(STRAIGHT)
                        # One player stays on 16+16 while the other's answer
                        # moves from six ticks behind to six ticks ahead.
                        note('right',t+half*BAR+pos,straight_gate(shape,pos),
                             chord(p,p+7) if how=='o' else p,.99 if pos==0 else .92)
            trade = bool(TRADE) and s == 'across the line'
            # Each smaller swing starts on a new low chord. The answer stays
            # Gb-F-C-Eb against them all; the call comes home as the hands meet.
            call_root = root + (5,3,-2,0)[j//2] if trade else root
            # Four swings on either side of the midpoint. With each swing let
            # another note at the END of the answer belong to the whole band.
            heads = [(pos,semi) for pos,_,semi,how in REPLY if how!='m'] if trade else []
            reunited = {pos for pos,_ in heads[len(heads)-j//2:]} if trade else set()
            # Keep a quarter-note hat under the early bow. The china and snare
            # return with the reunited tail, sooner each time.
            lay_out_until = turn + min(reunited, default=BAR)*(pair-width)/BAR
            if trade and d < 0:
                # Time for a bass note to ring: Bb, Db, Ab, home to Eb under
                # successive long answers, instead of doubling their four pitches.
                note('bass',turn,pair-width-.55,root+(7,10,5,0)[j//2],.91)
                # Bow through the spaces where the guitars palm-mute. The four
                # pitches and their stretched onsets are the SAME reply; the
                # duration changes from a pick stroke to a breath of the bow.
                for i,(pos,semi) in enumerate(heads):
                    end = heads[i+1][0] if i+1 < len(heads) else BAR
                    pitch = root+semi+12
                    if i==len(heads)-1 and j==len(debts)-1:
                        pitch = chord(pitch,pitch+7)  # let the fifth lead home
                    note('bow',turn+pos*(pair-width)/BAR,(end-pos)*(pair-width)/BAR-.32,
                         pitch, (.92,.87,.82,.90)[i])
            if BREATH and s=='at par':
                shade_breath(t,j)
            for back, (pattern,at,w) in enumerate(((CALL,t,width),(REPLY,turn,pair-width))):
                for ix,(p0,gate,semi,how) in enumerate(pattern):
                    hit = at+p0*w/BAR
                    dur = gate*w/BAR
                    pitch = (root if back else call_root)+semi
                    mute = how=='m'
                    vel = (.76 if mute else .92) if p0 else .99
                    if s=='at par':
                        # Give the answer a face before its first displacement.
                        if BREATH and not back:
                            # The baritone calls an octave below the original
                            # clean guitar. First connect the three pitches.
                            # Second, tongue the first double stroke on Eb;
                            # third, leave BOTH short pairs to the left guitar.
                            if not mute:
                                following = next((pos for pos in call_heads if pos>p0), BAR)
                                note('breath',hit,following-p0-.25,pitch+12,vel-.09,sub=.12)
                        elif not mute:
                            note('clean',hit,dur,pitch+24,vel-.09)
                        if j>=1 and not back and not p0:
                            note('bass',hit,dur,root,.83); kit('k',hit,.86)
                        if j==2 and mute: note('left',hit,dur,pitch,.70,pm=1)
                        continue
                    # Low Eb call, high Gb answer. In the first crest the right
                    # hand lets its reply ring instead of adding more mutes.
                    for side in ('left','right'):
                        if crossing:
                            if side=='right': continue  # already played the square version
                            if back and d==0 and mute: continue
                        if repay and back and side == 'right' and p0 < dry_from:
                            continue  # no right-hand chugs between the notes given to the open courses
                        if (advance or early) and side=='right' and not back and hit>=t+BAR:
                            continue  # the left guitar keeps the tail of the call; the right makes room
                        if trade and back and p0 not in reunited:
                            if mute and (side=='right' or (d<0 and hit<lay_out_until)): continue
                            if not mute and (d<0 or side=='left'): continue
                        if s=='called in' and j<3 and side=='right' and not back: continue
                        if s=='still owing' and side=='right' and back and mute: continue
                        meeting = crossing and back and d==0
                        gp = pitch+int(STRAIGHT) if meeting else pitch
                        voiced = chord(gp,gp+7) if how=='o' else gp
                        if s=='square' and back and not mute and side=='right':
                            voiced=chord(pitch,pitch+7)
                        guitar_gate = straight_gate(pattern,p0) if meeting else dur
                        if early and side=='right' and not back:
                            guitar_gate = min(guitar_gate, t+BAR-hit)
                        note(side,hit,guitar_gate,voiced,vel,**({'pm':1} if mute else {}))
                    # Bass keeps the hook's accents clear, not a second fast solo.
                    long_answer = trade and back and d<0
                    if not mute and not long_answer:
                        bp = pitch-12 if back and semi>=12 else pitch
                        note('bass',hit,dur,bp,vel-.05)
                    elif not back and s not in ('called in','square'):
                        note('bass',hit,dur*.84,call_root,.78)
                    if (not back and (not mute or ix in (1,2))) or (back and (p0==0 or (s in ('still owing','across the line') and not mute))):
                        if not long_answer or p0 in (0,REPLY[-1][0]):
                            kit('k',hit,vel)
                    if s in ('still owing','across the line') and how=='o' and not (trade and back and j<6) and not (
                            straight_call and not back and RECALL.split(';')[2]=='1'):
                        note('weight',hit,dur,chord(pitch,pitch+7),.93)
                    if LADDER and LADDER.split(';')[1]=='1' and s=='called in' and root!=HOME and how=='o':
                        note('weight',hit,dur,chord(pitch,pitch+7),.93)
                    if s=='square' and back and not mute:
                        if p0 in repay:
                            # Lift together before the next low call. The last
                            # reply outlasts the receipt's first low chord by a
                            # beat. For that beat the chord can ring on its own;
                            # leave two ticks of breath before the last Eb.
                            damp = t + pair + (BAR-2 if j == len(debts)-1 else 0)
                            note('courses',hit,damp-hit-.12,pitch+repay[p0],.90 if p0==0 else .84)
                        else:
                            note('clean',hit,dur,pitch+24,.90)
            # No borrowing in this part: the drummer's quarters and backbeat
            # can be followed across both displaced halves of the guitar riff.
            # Three still-square pairs just before the first unequal one. The
            # two strokes always start on beat two, and always share eight ticks.
            spread = (j-(len(debts)-2) if s=='in hand' and j>=len(debts)-2 else
                      2 if s=='on account' and j==0 else None)
            if BRUSH and spread is not None: assert d==0
            for i in range(pair//SUB):
                q = t+i*SUB
                if s=='at par' and j<2: continue
                if s in ('called in','at par') and i%2: continue
                if trade and d<0 and turn<=q<lay_out_until:
                    kit('h',q,.56 if i%4==0 else .44)
                    continue
                if BRUSH and spread is not None and i%4==1:
                    # 4+4, 5+3, 6+2 sixteenths of wire on the head. Nothing
                    # new strikes as the longer sweep passes the backbeat.
                    note('sweep',q,SUB+(spread if i<4 else -spread),'sw',.88)
                elif BRUSH and spread is not None and i%4==2:
                    kit('hp',q,.64)  # the foot counts three while the hands brush and strike
                elif LEDGER and s in LEDGER.split(';')[2].split(',') and LEDGER.split(';')[0].split(',')[abs(d)] != 'h':
                    # v21: the hat is as far open as the debt; an opened hat rings until the next stroke closes it
                    note('metal',q,2*SUB if s=='called in' else SUB,LEDGER.split(';')[0].split(',')[abs(d)],.57 if i%4==0 else .47)
                    trim = float(LEDGER.split(';')[1].split(',')[abs(d)])
                    if trim: voices['metal'][-1]['gain'] = f'{trim:g}dB'
                else:
                    kit('x' if s=='across the line' else 'rde' if s=='still owing' else 'h',q,.57 if i%4==0 else .47)
                snare_beats = (1,3) if s in ('still owing','across the line') else (2,)
                if i%4 in snare_beats:
                    kit('s',q,.96 if i%4!=1 else .83)
            if j==0 and s not in ('at par','called in'): kit('c',t,.83)
            if s in ('on account','across the line') and j==len(debts)-1:
                for off,pc in ((4,'t1'),(2,'t2'),(1,'ft')): kit(pc,t+pair-off,.76)
            t+=pair

    if STRIDE:
        hold = float(STRIDE)
        assert 0 < hold <= 1, 'C10T10_STRIDE must be a fraction of a step'
        # Read the last *pitched* stroke of the original riff on the bassist's
        # clock. A short palm stroke is not another note of the melody.
        def bass_pitch(pos, d, root):
            width = BAR+d
            back = pos>=width
            pat = REPLY if back else CALL
            local = (pos-width if back else pos)*BAR/(pair-width if back else width)
            semi = next(s for p,_,s,h in reversed(pat) if h!='m' and p<=local)
            return root+semi-(12 if back and semi>=12 else 0)

        marks = dict(sections)
        debts = dict(FORM)
        def clear(a,b):
            voices['bass'] = [n for n in voices['bass'] if not a/SUB <= n['at'] < b/SUB]

        # Three pairs on the maximum debt. Six does not divide 32, but it
        # divides 96: don't restart on each bar. Where a step would cover the
        # backwards guitar, let the breath last until the compressed reply.
        start = marks['still owing'] + 2*pair
        stop = start + 3*pair
        clear(start,stop)
        for at in range(start,stop,MAX_DEBT):
            j,pos = divmod(at-marks['still owing'],pair)
            d = debts['still owing'][j]
            if ADVANCE and j%2 and BAR<=pos<BAR+d: continue
            root = HOME+crest_roots[j]
            note('bass',at,MAX_DEBT*hold,bass_pitch(pos,d,root),.92)

        # On the way down each positive debt names a new stride: 6, 4, 2.
        # Let the previous step go before the pair ends. At zero stop counting;
        # the old bass part returns on the two guitarists' shared reply.
        repayment = debts['called in']
        for j,d in enumerate(repayment):
            base = marks['called in']+pair*j
            if d==0:
                # No gap left to count. Hold Eb, lift for one last two-tick
                # stride, then strike Gb with both players on the same beat.
                clear(base,base+BAR)
                note('bass',base,BAR-repayment[j-1],HOME,.93)
                break
            if d<0: break
            clear(base,base+pair)
            for pos in range(0,pair,d):
                if BOOM:    # v17: the step is an 808's; it rings its whole length, and the next one cuts it
                    note('boom',base+pos,min(d,pair-pos),bass_pitch(pos,d,HOME)+int(BOOM.split(';')[2]),.92)
                else:
                    note('bass',base+pos,min(d,pair-pos)*hold,bass_pitch(pos,d,HOME),.92)

    if ROOM:
        _,_,shift,foot = ROOM.split(';')
        where = dict(sections)
        quiet = lambda n: n['at']*SUB < where['in hand'] or where['two clocks'] <= n['at']*SUB < where['called in']
        midi = lambda name: NOTES.index(name[:-1])+12*(int(name[-1])+1)
        # Level-matched note by note to the bass guitar's own notes (K-weighted, each alone, raw): a plucked string
        # speaks hardest when it is short and when it is high. In dB: the two E flats under the sax; the pedals
        # A flat, G flat, E flat, E flat; the three notes of the fill (the last, on C, stays under its floor tom).
        trims = (-5,-5, -2.5,-1,0,0, -1.5,-4.5,-10)
        moved = sorted((n for n in voices['bass'] if quiet(n)), key=lambda n: n['at'])
        assert len(moved) == len(trims)
        for n,trim in zip(moved,trims):
            voices['room'].append({**n,'pitch':nm(midi(n['pitch'])+int(shift)),**({'gain':f'{trim:g}dB'} if trim else {})})
        voices['bass'] = [n for n in voices['bass'] if not quiet(n)]
        assert len(voices['room']) == 2+4+3
        if foot:
            early = [n for n in voices['kick'] if n['at']*SUB < where['in hand']]
            assert len(early) == 2
            voices['kick'] = [n for n in voices['kick'] if n not in early]
            voices['sweep'].extend({**n,'gain':f'{float(foot):g}dB'} for n in early)

    if ANSWER:
        # The first bar of what was the loud band's first pair is the first bar of the quiet band's last pair, note
        # for note, with the reed's tonguing; the crash moves to the loud band's first stroke.
        first, pair = dict(sections)['in hand'], 2*BAR
        first_bar = lambda n, start: start <= round(n['at']*SUB, 4) < start+BAR
        for tr in ('left', 'right', 'bass', 'kick', 'snare', 'metal', 'breath', 'room', 'sweep'):
            again = [{**n, 'at': round(n['at']+pair/SUB, 6)} for n in voices[tr] if first_bar(n, first-pair)]
            voices[tr] = [n for n in voices[tr] if not first_bar(n, first)] + again
        kit('c', first+BAR, .83)
        lo, hi = (first-pair)/SUB, (first-pair+BAR)/SUB
        air_points.extend([[f'{float(at[:-1])+pair/SUB:g}b', db] for at, db in list(air_points)
                           if isinstance(at, str) and lo <= float(at[:-1]) < hi])

    if OUTSTANDING:
        # v22: after the receipt the reed calls once more, as at 0:00. The piano marks the bar line where the answer
        # is due, and nobody answers: the one call in the song that is never paid.
        lift, wait, fall, mark, run = OUTSTANDING.split(';')[:5]
        sections.append(('outstanding', t))
        for p0,_,semi,how in CALL:
            if how=='m': continue
            following = next((pos for pos in call_heads if pos>p0), BAR+float(wait))
            note('breath',t+p0,following-p0-.25,HOME+semi+12,(.99 if p0==0 else .92)-.09,sub=.12)
            if float(lift): voices['breath'][-1]['gain'] = f'{float(lift):g}dB'
        if float(wait) and float(fall):
            air_points.extend([[f'{(t+BAR)/SUB:g}b',0],[f'{(t+BAR+float(wait)-.25)/SUB:g}b',float(fall)]])
        if mark:
            note('rule',t+BAR,2.2,HOME+31,float(mark))
        t += BAR+int(run)

    def track(tr,patch,db,pan=0,**more):
        ns=sorted(voices.pop(tr),key=lambda e:e['at']); assert ns
        assert all(0<=n['at']<t/SUB and n['at']+n['len']<=t/SUB+.00001 for n in ns)
        return {'name':tr,'patch':patch,'gain':f'{db}dB','pan':pan,'notes':ns,**more}
    palm=' synth.layers.0.mute=expr.pm*0.6 synth.layers.0.mute_width=0.1'
    stage = STAGE.split(';') if STAGE else None
    chest = CHEST.split(';') if CHEST and stage else None
    band = lambda b: 'peak cutoff=%s q=%s gain=%sdB' % tuple(b.split(':'))
    room = chest[1].split(':') if chest and chest[1] else None      # the bass makes room for the chest
    riff = dict(out='gtrs', fx=[{'type':'eq','bands':[band(b) for b in chest[0].split(',')] if chest else
                                 [f'peak cutoff=700 q=0.9 gain={stage[1]}dB']}]) if stage else {}
    tracks=[track('left','ct-twin fx.2.cone=81'+palm,1,-.93,**riff),
            track('right','ct-twin fx.1.model=gojira fx.2.cone=84'+palm,1,.93,**riff),
            track('weight','ct-wall-stop-l',-5,.05,fx=['hp cutoff=130']+([{'type':'eq','bands':['peak cutoff=380 q=1 gain=-3dB']}] if stage else []),
                  **({'out':'gtrs'} if stage else {})),
            track('clean','ct-clean synth.layers.0.inharm=0.00008',-2,-.26,sends={'spring':'-15dB'}),
            track('bass','ct-bass',-.8,out='low') if stage else
            track('bass','ct-bass',-.8,fx=[{'type':'eq','bands':['hp cutoff=27','peak cutoff=330 q=1 gain=-4dB']}]),
            track('rule','piano-additive',-9,-.35), track('tally','owing-key',-9,.38,sends={'spring':'-15dB'}),
            track('kick','ct-kit',2,out='drums',fx=[{'type':'eq','bands':['peak cutoff=4100 q=0.85 gain=6dB']+([stage[3]] if stage[3] else [])}])
            if stage else track('kick','ct-kit',2,out='drums',fx=['peak cutoff=4100 q=0.85 gain=6dB']),
            track('snare','ct-kit',3,out='drums'), track('metal','ct-kit',2,out='drums'),track('skins','ct-kit',2,out='drums')]
    if BRUSH:
        tracks.append(track('sweep','brush-kit kit.sw.patch.synth.amp.a=28ms kit.sw.patch.synth.amp.r=32ms '
                            'play.humanize.time=0ms play.humanize.vel=0 fx.3.mix=0',
                            float(BRUSH),-.18,out='brush' if stage else 'drums'))
    if ROOM:
        tracks.append(track('room',ROOM.split(';')[0],float(ROOM.split(';')[1]),.08))
    if BREATH:
        tracks.append(track('breath','bari-sax synth.amp.r=65ms fx.0.mix=0.075',float(BREATH),-.16,
                            auto={'tongue':{'points':air_points,'curve':0}},
                            fx=[{'type':'gain','gain':{'value':'0dB','mod':[{'src':'auto.tongue','amount':1}]}}]))
    if TRADE:
        if BOW:
            tracks.append(track('bow','owing-bow',float(BOW.split(';')[0]),-.66,fx=['hp cutoff=120']))
        else:
            tracks.append(track('bow','tagelharpa-bass-bowed synth.amp.r=80ms fx.0.mix=0.035',
                                float(TRADE),-.66,fx=['hp cutoff=120']))
    for name in fold_patches:
        tracks.append(track(name,name,float(ADVANCE),.66))
    if CHANGE:
        bronze = ('gamelan play.gate=1 play.humanize.time=0ms play.humanize.vel=0 '
                  'synth.amp.r=14ms synth.env.ring.r=16ms fx.0.mix=0')
        tracks.append(track('change',bronze,float(CHANGE),-.35))
    if PRESS:
        tracks.append(track('pressure','owing-skin',float(PRESS),.38,sends={'spring':'-20dB'}))
    if KEPT:
        level,shimmer = KEPT.split(';')
        # A sixteenth is a quarter of a beat: the tremolo is loudest on every
        # straight sixteenth from the top of the song, where each key starts.
        tracks.append(track('kept','owing-kept',float(level),-.35,
                            fx=[f'tremolo rate=0.25b depth={float(shimmer):g}']))
    if COURSES:
        # The written gates only lift the dampers. Lengthen the strings' own
        # decays too, or the first courses are already dead when the last rings.
        acoustic = ("twelve-string play.tuning='Eb2 Ab2 Db3 Gb3 Bb3 Eb4' play.gate=1 "
                    "synth.layers.0.decay.value=12s synth.layers.1.decay.value=9s "
                    "synth.amp.r=90ms fx.3.mix=0.05")
        tracks.append(track('courses',acoustic,float(COURSES),.42,fx=['hp cutoff=130']))
    if BOOM:
        tracks.append(track('boom',BOOM.split(';')[0],float(BOOM.split(';')[1]),
                            **({'fx':[{'type':'eq','bands':[BOOM.split(';')[4]]}]} if BOOM.split(';')[4:] else {})))
    assert not voices
    key_patch={'about':'Still Owing: the reply marker. Its orbit opens in proportion to the sixteenths borrowed in this pair.',
      'synth':{'amp':{'a':'2ms','d':'450ms','s':.2,'r':'95ms'},'layers':[{'type':'terrain','terrain':{
          'surface':'sines','k':1.7,'cx':.13,'cy':-.18,'rx':{'value':.16,'mod':[{'src':'expr.owing','amount':.46}]},
          'ry':{'value':.12,'mod':[{'src':'expr.owing','amount':.34}]}}}]},'fx':['hp cutoff=185']}
    old_kit_bus = {'fx':['reverb kind=room decay=0.48s mix=0.08','glue threshold=-23dB ratio=2.2 attack=18ms release=130ms',
                         {'type':'eq','bands':['peak cutoff=390 q=0.9 gain=-4dB','lp cutoff=14900']}]}
    staged = {}
    if stage:
        # The ground under each pair, for the low bus's eq: the bass guitar's lowest note there (where it rests, the
        # 808's or the upright's; else the pair before), as semitones from F1, where the record's low bus is centred.
        pair_beats = 2*BAR/SUB
        low_of = lambda n: min(12*(int(p[-1])+1)+NOTES.index(p[:-1]) for p in n['pitch'].split(','))
        ground = {}
        for name in ('room', 'boom', 'bass'):                      # the bass guitar has the last word
            seen = {}
            for tr in tracks:
                if tr['name'] == name:
                    for n in tr['notes']:
                        i = int(n['at']//pair_beats); seen[i] = min(seen.get(i, 999), low_of(n))
            ground.update(seen)
        points, was, here = [], None, HOME
        for i in range(int(t/SUB/pair_beats)):
            here = ground.get(i, here)
            semis = (here-29+6)%12-6
            if semis != was:
                if was is not None: points.append([f'{i*pair_beats-.02:g}b', was])
                points.append([f'{i*pair_beats:g}b', semis]); was = semis
        keyed = lambda hz: {'value':hz,'mod':[{'src':'auto.key','amount':0.08333}]}
        cutoff, q, cut = stage[2].split()
        staged = {
            'gtrs':{'fx':[{'type':'eq','bands':[f'peak cutoff=330 q=1.2 gain={stage[0]}dB']},'reverb kind=room decay=0.35s mix=0.06 predelay=6ms']},
            'low':{'fx':[{'type':'eq','bands':[{'kind':'peak','cutoff':keyed(44),'q':1.5,'gain':'-7dB'},
                                               {'kind':'peak','cutoff':keyed(90),'q':1.0,'gain':'7.5dB'},
                                               {'kind':'peak','cutoff':350,'q':1.0,'gain':'-8dB'},
                                               {'kind':'peak','cutoff':1500,'q':1.0,'gain':'4dB'}]+
                                              ([{'kind':'peak','cutoff':float(room[0]),'q':float(room[1]),'gain':room[2]+'dB'}] if room else [])},
                         {'type':'compressor','threshold':'-26dB','ratio':8.0,'attack':'12ms','release':'120ms','makeup':f'{stage[4]}dB'}],
                   'auto':{'key':{'points':points,'curve':0}}},
            'brush':old_kit_bus,
            'drums':{'fx':old_kit_bus['fx'][:2]+[{'type':'eq','bands':[f'peak cutoff={cutoff} q={q} gain={cut}dB','lp cutoff=14900']},
                                                {'type':'gain','gain':f'{stage[6]}dB'}]},
        }
    if LEDGER and staged and float(LEDGER.split(';')[3]):
        # v21: the loud band comes down through the two brush pairs and builds with the debt, a sixth of the way for
        # each sixteenth borrowed; full again on the pair that owes six. One lane on each of its three buses.
        depth = float(LEDGER.split(';')[3])
        lean = [['0b',0],[f"{pair_start['in hand',3]/SUB:g}b",0],[f"{pair_start['on account',0]/SUB:g}b",-depth],[f"{pair_start['on account',MAX_DEBT]/SUB:g}b",0]]
        for name in ('gtrs','low','drums'):
            staged[name]['fx'] = staged[name]['fx']+[{'type':'gain','gain':{'value':'0dB','mod':[{'src':'auto.lean','amount':1}]}}]
            staged[name].setdefault('auto',{})['lean'] = {'points':lean,'curve':0}
    return {'about':'Still Owing, Common Time track 10: a low call borrows time from a higher answer and pays it back within each two-bar phrase.',
        'tempo':BPM,'seed':1,'event_stable':True,'length':f'{t//SUB}b','tail':'3s','loudness':float(LEDGER.split(';')[4]) if LEDGER and LEDGER.split(';')[4] else float(chest[2]) if chest else float(stage[5]) if stage else float(BOOM.split(';')[3]) if BOOM else ROOM_LUFS if ROOM else -10,'ceiling':'-1dB','true_peak':True,
        **({'songs':fold_sources} if fold_sources else {}),
        'patches':{'owing-key':key_patch,**fold_patches,**({'owing-skin':pressure_skin()} if PRESS else {}),
                   **({'owing-kept':kept_key()} if KEPT else {}),**({'owing-bow':bow_patch()} if BOW and TRADE else {})},
        'buses':{'spring':{'fx':['reverb kind=spring drip=0.65 mix=1 decay=1.2s low_cut=350 predelay=18ms']},
        'drums':old_kit_bus, **staged},
        'master':{'fx':['hp cutoff=25']},'tracks':tracks}, sections


def the_top_changes_hands(song):
    """v23: the hat at the album's level with its ladder on it; the kick and the snare give the cymbals the top."""
    kit, kick_lp, shelf, target = TOP.split(';')
    for t in song['tracks']:
        if t['name'] == 'metal' and kit:
            t['patch'] += ' ' + kit
        if t['name'] == 'kick' and kick_lp:
            t['fx'] = (t.get('fx') or []) + [f'lp cutoff={kick_lp}']
        if t['name'] == 'snare' and shelf:
            t['fx'] = (t.get('fx') or []) + [{'type': 'eq', 'bands': ['highshelf cutoff={} gain={}dB'.format(*shelf.split(':'))]}]
    if target:
        song['loudness'] = float(target)


def the_snare_is_fitted(song):
    """v24: the album's snare fitted to this song: its body under its crack, as on the records; 1 dB down."""
    over, bands, fader, target = SNARE.split(';')
    for t in song['tracks']:
        if t['name'] == 'snare':
            if over:
                t['patch'] += ' ' + over
            if bands:
                eq = next((f for f in t.get('fx') or [] if isinstance(f, dict) and f.get('type') == 'eq'), None)
                if eq is None:
                    t['fx'] = (t.get('fx') or []) + [{'type': 'eq', 'bands': []}]
                    eq = t['fx'][-1]
                eq['bands'] = eq['bands'] + [b.strip() for b in bands.split(',')]
            if fader:
                t['gain'] = f'{float(fader):g}dB'
    if target:
        song['loudness'] = float(target)


def dump(song):
    return '\n'.join('tracks:\n'+'\n'.join('  - '+json.dumps(x) for x in v) if k=='tracks' else k+': '+json.dumps(v) for k,v in song.items())+'\n'


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=OUT); parser.add_argument('--form',action='store_true')
    args=parser.parse_args(); song, marks=build()
    if TOP: the_top_changes_hands(song)
    if SNARE: the_snare_is_fitted(song)
    if args.form:
        for n,t in marks: print(f'{n:18} {t/BAR+1:5.0f}  {t/SUB*60/BPM:6.2f}s')
    else: args.out.write_text(dump(song))
