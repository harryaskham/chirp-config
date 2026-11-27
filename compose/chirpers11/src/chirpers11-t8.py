#!/usr/bin/env python3
"""Wind Down (Escapement, track 8, the closer). Clicky minimal techno, 124 BPM running down to 50, G minor, 200 bars.

THE RULE. Nothing here is new. One thing is taken from each of the other seven songs, gathered a section at a time
on one grid in one key, held together, and then let go one at a time, last in, first out, until the first thing on
the record (a click off the beat) is alone again. Then the spring runs down: over the last eight bars the tempo
falls from 124 to 50, each tick is let ring a little longer than the last, and the final stroke, let go altogether
and an octave down, lands ON the one, where that click has never been.

  from 1 Give or Take      the grid: a bass drum on the four and one click on the off-beats (sixteenths 2 6 10 14)
  from 7 Out of Step       the half-bar pattern x x . x . x x . on a short saw click
  from 5 Hearing Things    the bass with no fundamental (harmonics two to six), its line a tone down, off the beat
  from 4 Ring True         the cell's tune on the wooden bar, stopped; let go once everything is gathered
  from 2 Least Common      the meeting tune: a ping where two of the cycles 3, 5 and 7 meet, a chord where all three do
  from 3 Standing Room     standing room: two walls 3 and 5 sixteenths away, round the click
  from 6 Small Change      one seed every two bars and a pair of coins, 3 and 5, a fifth up and a fourth down
The click itself is Ring True's wooden bar playing Give or Take's grid: a note stopped too soon, until the end.

v2 (26 Nov): WHAT THE SONGS LEARNT SINCE. The seven grew after v1 quoted them, and chirper-zero offered three of
his (06:04): the closer takes one more thing from four of them, and one from the album's name. Six switches, each
`--without-…` (all six off is v1 byte for byte):
  CATCH   the escapement itself. In the last bar before each thing comes the wheel is caught: everything stops but
          the click (in its room, once it has one), and on the one it is let go with the new thing in it. Seven
          catches, the last before all are gathered. Nothing is caught on the way out: that is the winding down.
  COMP    from 7 Out of Step v2: the complement . . x . x . . x, a small bright click in the pattern's three holes.
          It fits only when everything is home, so it plays through the hold and no longer: for those 32 bars every
          sixteenth of the bar is struck.
  HAT     from 5 Hearing Things: its hat, backwards. From the bar the first thing leaves to the bar the drum goes, a
          hat that slows down through every eight bars and starts the next where it started the last: the song has
          been winding down for a minute and a half before the tempo moves.
  LEARNT  from 3 Standing Room v3: when the room goes, what is left of it is in the bass. For the eight bars after
          its door shuts the bass plays the room's three-three-two (D F C D F C on sixteenths 2 5 7 10 13 15).
  STOP    from 1 Give or Take v3: the stop. The spring does not run down in a straight line against the beat (v1): it
          loses speed in a straight line against the clock, as a platter does when the motor goes off: slowly, then
          all at once. Speed sqrt(1 - 2x / W) after x beats, W chosen so that a fifth of it is left on the one
          (v1 kept two fifths): the last ticks are nearly two seconds apart.
  TUCK    the click 3 dB lower while anything else plays (it stood 14 dB over the envelope at its own note), and as
          it was while it is alone.

v3 (26 Nov): EACH LEAVES AS ITSELF. In v2 a thing went by being absent from the next bar, and the scorer heard
bars 114 to 172 as one section. Six switches, each `--without-…` (all six off is v2 byte for byte); five are the
leaving thing's own song's idea, in its last bars, and the sixth is the end:
  SPENT   6 Small Change: the change spends what it has left. In its last four bars a seed every bar, not every
          two, and in the last of them on beats one and three; the coins run on over the bar line after it.
  HELD    2 Least Common: the meetings' last word is a chord that is not let go: on the bar they leave, the chord
          held for a bar and two bars dying. The only held sound in the song.
  TAKEN   4 Ring True: the cell is taken back into the hand. Over its last eight bars its ring goes from let go
          to stopped, so it leaves as the click it came as.
  REAL    5 Hearing Things: the bass with no fundamental is given it. For its last four bars a sine plays the
          notes the ear had been supplying; then both go.
  SLIP    7 Out of Step: the pattern slips. In its last eight bars it starts a sixteenth later each bar: eight
          steps, eight bars, so it has gone all the way round and is in step again in the bar it leaves.
  SINK    1 Give or Take's stop, its other half (chirper-zero's A RECORD SWITCHED OFF): as the spring runs down
          each tick's NOTE sinks with the speed, as a record's does when the motor goes off. A clock's tick does
          not sink, but by then each tick is being let ring into a note. A quarter of the speed is left on the
          one (v2: a fifth), so the note has sunk exactly two octaves: the last stroke is G4, reached, not jumped to.

v4 (26 Nov): THE BODY OF THE SOUND. v3 read 10 and 11 dB over the album's envelope from 1.4 to 1.6 kHz and 11
under at 71 Hz: a song with a waist and no hips. Read by parts, the middle is the click's note and the saw's
eighth harmonic (between them half to nine tenths of 1 to 2 kHz once the cell has gone), and nothing at all lives
between the drum (47 Hz) and the bass's second harmonics (98 up). Three switches (`--without-mid`, `-body`,
`-open`; all three off is v3 byte for byte):
  MID    the click is turned from its note towards its click: 6 dB off round G6 (1568 Hz) and 3 dB on round
         11 kHz, after its clip. While it is alone it is 4.5 dB up, so the lone click stands where it stood.
         As the spring runs down and the note sinks it leaves the cut behind, so the note comes out as it falls
         (and the 4.5 dB is taken off again by the last stroke). The saw's click loses 5 dB round 1.6 kHz.
  BODY   the drum is given the body between its note and the bass: 5 dB round 72 Hz.
  OPEN   the last chord opens as it dies. It was held under a low-pass that never moved; now the filter is shut
         while the chord is held (600 Hz) and opens two octaves in the first two and a half seconds of its
         going, which now takes six, not three (with both at three seconds the chord was 17 dB under the mix
         before the filter had moved a third of the way): the meetings' last word gets brighter as it gets
         quieter, a door opening on something leaving.

v12 (27 Nov): THE CATCH SAYS WHO IS COMING. Two switches (`--without-tell`, `-whole`; both off is v11 byte for
byte):
  TELL   seven times the escapement catches: a bar with only the click, and after it something new. Until now
         all seven were the same bar. Now each says who is coming: the newcomer plays whatever of its OWN
         figure falls in the caught bar's last beat, as if it had come a beat early (3 dB under its stroke):
           bar 16   the pattern: its last two strokes (sixteenths 13 and 14)
           bar 32   the bass with no fundamental: its last note of four bars, F2
           bar 48   the cell: the last stroke of its two-bar tune, C5, before it begins on D5
           bar 64   the meetings: three and five meet on beat 4 of this bar, a D5, and are heard to part
                    over the bar line
           bar 80   the room: nothing new (its door is already opening through this bar)
           bar 96   the change: one seed, three sixteenths before the one, so that its first coin (three
                    sixteenths on) falls ON the one with the first seed proper
           bar 112  the complement: the pattern's holes that fall in the beat (sixteenths 12 and 15)
  WHOLE  v11's lead (the bass's D2 through the last beat of five catches) is a bare sine: the bass's
         fundamental with none of its harmonics, where the bass itself is harmonics with no fundamental. On
         small speakers it is not there at all. Now, ONCE, the bass's own voice plays the same D2 with it,
         under it: the first time the bass comes back before the drum (bar 48) it is whole for that beat, so
         that the four bare fundamentals after it are known for the bass; then it has no fundamental again
         until bar 173 (Ring True v11's SHOW: shown once before). First built in all five catches the lead plays in:
         the scorer's boundary after each fell by 0.03 to 0.06 (one of them, where nothing else was new, from
         0.17 to 0.14) and its sections at the highest cut from 9 to 5: a catch whose last beat has the bass's
         voice in it is three quarters of a catch (v11's finding with two beats of the lead, again).

v11 (27 Nov): WHAT THE SONGS LEARNT AFTER MIDNIGHT. Ring True (v11) and Least Common (v11) each learnt something
in the last hour; the closer takes two things from the one and one from the other, and nothing of its own. Three
switches (`--without-grip`, `-choke`, `-lead`; all three off is v10 byte for byte):
  GRIP   4 Ring True v11: the wood has a hand. There, as the wood closes, the hand comes down on the bar's
         middle: its note goes and its second mode, two octaves up, is what is left. Here the cell IS that bar,
         and the hand takes it back over bars 161 to 168: so bar by bar the cell's tune goes up two octaves as
         it is stopped (the note 12 dB down by the last bar, the second mode at the note's old level). And on
         the cell's last stroke the hand lets go of the stick and of the bar (v8): that one stroke has its
         note again, whole, and bounces on it. A new patch name, wd-grip. Ring True's crossfade was linear in
         dB and dipped 6 dB in the middle; here each layer has its own level on the stroke (expr.note,
         expr.mode) and the two are an equal-power pair: a change of colour, not of level.
  CHOKE  4 Ring True v11: the weight's head tightens under the beater as it is stopped. Here the drum goes at
         bar 193: in its last two bars the beater is held against it and its note rises, B flat then C for G.
         The drum does not just stop: it is stopped.
  LEAD   2 Least Common v11: the bass comes back before the drum. In each caught bar where the bass is already
         in (bars 48, 64, 80, 96, 112) the bass's own fundamental (the sine it is given at the end, v3) holds
         D, the fifth below, through the bar's last beat into the one the drum comes back on. Not the whole
         bar: Least Common found that a break with the bass's band filled is no longer a break. FIRST BUILT
         WITH THE LAST TWO BEATS HELD, and this song found the same thing at half the size: rendered in full,
         the scorer's sections fell from 10 to 8 at its highest cut, and came back with the lead out.

v10 (26 Nov): WHAT THE SONGS LEARNT TONIGHT. Small Change (v9) and Least Common (v10) each learnt something after
the closer last quoted them; it takes one thing from each and nothing of its own. Three switches (`--without-
exchange`, `-rate`, `-given`; all three off is v9 byte for byte):
  EXCHANGE  6 Small Change v9: the same change in another currency. While the change spends what is left (bars
            141 to 144, a seed a bar) the seeds are also paid by a second pair of coins, 3 and 5, of a unit two
            thirds of a sixteenth (three of its units for two sixteenths): the same fifths up on the left and
            fourths down on the right, one and a half times as fast, three against two with the first pair. A
            hand opens it for those four bars and lets it down over the two after, as the first pair's run on.
  RATE      6 Small Change v9: through the hold the complement has filled the pattern's holes, so that every
            sixteenth of the bar is struck. In its last four bars the complement's click also counts what the
            other currency can pay where that falls BETWEEN the sixteenths: 5, 8, 10 and 11 of its units after
            each seed, softer the more coins. The full grid is given its triplet just before it empties.
  GIVEN     2 Least Common v10: the drum rests where the three and the five meet on it, and the beat is given
            to the answer (the knock, which has sounded there since v6). From the bar the first thing leaves to
            the bar the meetings leave (145 to 160) that is three beats, fifteen beats apart (bar 147 beat two,
            151 beat one, 154 beat four), and the fourth fifteen is where all three meet on the drum (bar 158:
            the chord, the triad turning over), with the drum under it: three rests count in the last meeting.

v9 (26 Nov): WITH INTEREST. Three switches (`--without-answer`, `-interest`, `-chest`; all three off is v8 byte for
byte):
  ANSWER    the hand drops the stick on the cell's last stroke (v8), and the strings nobody plays were shut in
            that same half beat: the one stroke of the cell's that is let go altogether was the one they did not
            hear. Now they hear it and its bounces, and are held open through the bar after the cell has gone
            (bar 169), then let down over the next: the cell's last note is answered by the strings that have
            its note in them (C3's fourth partial and F2's sixth are C5), and the answer is what is left of the
            cell when it is not there.
  INTEREST  Small Change's lesson of v7 (a purse that gives back more than it is given, with a hand on its fader,
            builds; shut, it is empty at once). The change's last seed (bar 144, beat 3) went to the smallest
            purse and was a held B flat that ran out. Now the purse pays interest: the note swells for the two
            beats that are left and is shut on the one of bar 145, where the change goes. A clip inside the loop
            is the purse's size: it cannot hold more than that, so the swell comes up to a level and stays.
  CHEST     nothing in this song sounds between 60 and 85 Hz: the drum is on G1 (49 Hz) with its 47 Hz taken
            down, and the bass has no fundamental (that is its illusion). Beside the album the song stood 9.6 dB
            short at 71 Hz, the one band the scorer charged it for, and aimed at as such: a bell of 4 dB at 71 Hz
            on the drum, narrow (its stroke sweeps through there; it has no note there to give the bass).

v8 (26 Nov): WHAT IS LEFT BOUNCING. Two of the seven grew once more after v7, and the closer takes the new thing
from each. Two switches (`--without-drop`, `-part`; both off is v7 byte for byte):
  DROP  4 Ring True v8. There the stick is let go too: a thing's stroke is dropped and bounces, each bounce sooner
        and softer than the last by the same share. Here the hand has taken the cell back (bars 161 to 168); on
        the cell's last stroke it lets go of the stick, and of the bar: the stroke rings as nothing of the cell's
        has for eight bars. The cell goes at bar 169 and its stick is still bouncing on a bar still ringing:
        eight bounces, each gap three quarters of the one before, and the ninth would fall on beat two of the
        bar the cell is not in. Something coming to rest by itself, which is the song.
  PART  2 Least Common v8. There the second half remembers the first: each click's echo keeps its old cycle. Here
        nobody plays the cycles at all; only their meetings are heard, as pings. Now each meeting is heard to
        part: after a ping the two cycles that met go on their way, the three's click 3 sixteenths later on the
        left, the five's 5 later on the right, the seven's 7 later in the middle (where Least Common stands
        them). They are the ping's own echoes with the note taken out (what is left of a vibraphone bar over
        1.2 kHz is its second mode, two octaves up, and its click), so Least Common's cycles are heard in the
        closer for one step each, 342 times, and nobody plays them.

v7 (26 Nov): RING TRUE. Two of the seven grew again after v6, and the closer takes the new things from each. Three
switches (`--without-true`, `-turn`, `-tame`; all off is v6 byte for byte):
  TAME  2 Least Common v7 again: the pings' commonest note, D5, 3 dB down by an EQ on their track. The strings
        sing on the cell's notes, 500 Hz to 1 kHz, where this song already stood 6.4 dB over the album's
        envelope at 547 Hz; with them it stood 6.6.
  TRUE  4 Ring True v7. There the strings nobody plays are let go while the wood closes, and go quiet by themselves
        as it is shut. Here the cell is Ring True's wooden bar; so when the room goes (bar 153) the strings are
        let go beside the cell and are what is left round it: a string answers a note only if it is one of its
        own. Then the hand takes the cell (bar 161) and drags it late, and a thing dragged late is flat: the
        strings stop answering at once, bars before the hand has shut the cell. They ring while it rings true.
        They are stopped when the cell goes, and wait for the last stroke as before.
  TURN  2 Least Common v7. There the drum's low triad turns over a page at a time. Here the drum answers the
        meetings that land on it, two notes at a time; now each time all three meet on the drum (every 105
        beats) the triad turns over: G2 B flat 2 D3, then B flat 2 D3 G3, then D3 G3 B flat 3, and round.

v6 (26 Nov): WHAT THEY LEARNT THIS AFTERNOON. Three of the seven grew again after v5 quoted them, and the closer
takes the new thing from each. Three switches on (`--without-strings`, `-paid`, `-knock`; all off is v5 byte for byte) and one off:
  KNOCK   2 Least Common v6, the drum answers. There the drum answers each click that lands on it. Here nobody
          plays the cycles, only their meetings sound; so the drum answers each MEETING that lands on it, with
          the notes of the two cycles that met (G2 for the three, B flat 2 for the five, D3 for the seven):
          two low notes every 15, 21 and 35 beats, and all three every 105.
  STRINGS 4 Ring True v6, the strings nobody plays. The click is Ring True's wooden bar, and beside it lie that
          song's five open strings (F2, G2, B flat 2, C3, D3: each a loop one period long that returns itself
          and hears only the click). They are stopped for the whole record. The last stroke, on the one, is
          G4, the fourth harmonic of the G string: as it is struck the strings are let go, and when the stroke
          has stopped the string goes on at that note by itself. The last sound on the record is a string
          nobody played.
  EARLY   (OFF, `--with-early`) the strings let go from the top of the run-down instead, answering each tick as
          it slows and sinks. By solo they stood 10 to 15 dB under the lone click there, and the scorer took
          0.4 (99.05 for 99.45): with a new sound through the last 25 seconds its boundary at bar 9, where
          nothing changed, reads 0.16 for 0.18. Off until an ear asks for it.
  PAID    6 Small Change v5, the smallest change. The change's very last seed (bar 144, beat three) is paid in
          coins of 3 and 5 of a unit that is a pitch (B flat 3's period): its change is its own note, held,
          as the change leaves.

v5 (26 Nov): TWO MORE LEAVINGS. In v3 five of the seven left as themselves; the room only had its door shut, and
the cell was damped and nothing else. Three switches (`--without-sing`, `-nudge`, `-ease`; all three off is v4
byte for byte):
  SING   3 Standing Room v6: the walls sing. In the room's last four bars two more walls come in, so near that
         they cannot be counted: a second pair of buses, each returning the click and itself, one after 10.2 ms
         and one after 6.8. An echo every 10.2 ms is not an echo, it is 98 Hz: the room, as it goes, is two
         strings that the click plucks, G on the left and the D above it on the right (the far walls are 3 and
         5 sixteenths away; the near ones 3 and 2 of something a hundred times smaller). They rise through three
         bars, stand for one, and the door shuts on them with the room's.
  NUDGE  1 Give or Take's hand: as the cell is taken back into the hand (TAKEN) the hand is felt. Over its last
         eight bars the cell is dragged late by up to a sixteenth and let catch up, d(x) = reach sin^2(pi x / T),
         and its notes go with its speed, flat while it is dragged and sharp while it catches up
         (-12 log2(1 + d') semitones on each stroke): it is in step again in the bar it leaves.
  EASE   the cell let go is 2 dB lower (7 dB off at ring 1, not 5): let go it carried 91 to 98% of 500 Hz to
         1 kHz, and 547 Hz stood 6.7 dB over the album's envelope.

Form as arithmetic: GATHER lists the things in the order they come; each comes STEP bars after the last, all are
held for HOLD bars, they go in reverse order LEAVE bars apart, and the last WIND bars are the spring running down.
"""
import argparse
import json
from math import log, log10, log2, pi, sin, sqrt
from pathlib import Path

BPM, SLOW = 124, 50
S16 = 60000 / BPM / 4                       # a sixteenth, ms
BAR = 16
STEP, HOLD, LEAVE, WIND = 16, 32, 8, 8      # bars
GATHER = ['grid', 'pattern', 'ghost', 'cell', 'meetings', 'room', 'change']
COMES = {k: i * STEP for i, k in enumerate(GATHER)}
ALL = len(GATHER) * STEP                    # the bar at which everything is in
GOES = {k: ALL + HOLD + (len(GATHER) - 1 - i) * LEAVE for i, k in enumerate(GATHER)}   # last in, first out
GOES['grid'] = GOES['pattern'] + LEAVE      # the drum goes here; the click stays to the end
RUNS_DOWN = GOES['grid']
BARS = RUNS_DOWN + WIND
DRUM_IN = 8                                 # the bass drum comes eight bars after the click (and turns the listener round)
LET_GO = (ALL + HOLD // 2, ALL + HOLD)      # the cell's ring goes from STOPPED to 1 across these bars
STOPPED = 0.15                              # the cell's ring while it is gathered
ALONE = 6                                   # dB the click's fader comes up while it is alone (before the drum; as the spring runs down)
SHUT = -0.25                                # the click's: stopped sooner than Ring True stops anything (5 ms), so it is a tick and not a note
TICK, LAST = 'G6', 'G5'                     # the click's note (an octave over Give or Take's, clear of the cell and the pings); the last stroke's
CYCLES = (3, 5, 7)
PING = {(3, 5): 'D5', (3, 7): 'Bb4', (5, 7): 'F4'}
CHORD = ('G3', 'Bb3', 'D4', 'F4', 'A4')
CELL = [(3, 'D5', .8), (7, 'F5', .7), (11, 'G5', .85), (14, 'F5', .65), (19, 'D5', .8), (23, 'C5', .7), (27, 'Bb4', .85), (29, 'C5', .6)]
PATTERN = (0, 1, 3, 5, 6)                   # of eight sixteenths
GHOST = (('G1', 'G1', 'G1', 'Bb1'), ('G1', 'G1', 'G1', 'G1'), ('G1', 'G1', 'G1', 'C2'), ('G1', 'G1', 'D2', 'F2'))
WALLS = (3, 5)                              # sixteenths there and back
COINS, UP, DOWN, GIVE = (3, 5), 7, -5, 0.62
LAG = {UP: 19.7, DOWN: 23.8}                # ms the pitch effect is late (Small Change's bench)
WOOD = (0.015, 1.0)                         # the bar's ring time, seconds: stopped, let go
OUT = Path(__file__).resolve().parents[3] / 'songs/chirpers11-t8.yaml'

# ---- v2: the switches and their numbers. Nothing above is changed by them.
ON = {'catch': True, 'comp': True, 'hat': True, 'learnt': True, 'stop': True, 'tuck': True,
      'spent': True, 'held': True, 'taken': True, 'real': True, 'slip': True, 'sink': True,
      'mid': True, 'body': True, 'open': True, 'sing': True, 'nudge': True, 'ease': True, 'strings': True, 'paid': True, 'knock': True, 'early': False, 'true': True, 'turn': True, 'tame': True, 'drop': True, 'part': True, 'answer': True, 'interest': True, 'chest': True, 'exchange': True, 'rate': True, 'given': True, 'grip': True, 'choke': True, 'lead': True, 'tell': True, 'whole': True}
TELL = {'from': 12, 'db': -3}           # v12: the sixteenth of a caught bar from which the newcomer's own figure is played; dB on those strokes
WHOLE = {'gain': '-6dB', 'bars': (COMES['cell'] - 1,)}   # v12: dB on the bass's own voice (harmonics two to six) under the lead's fundamental; the caught bars (from 0) it is in (first: all five; see the docstring)
GRIP = {'note': -12, 'semis': 24, 'from': '-40dB', 'patch': 'wd-grip'}   # v11: dB on the cell's note with the hand all the way down; its second mode's place above the note; that layer's level with no hand; the patch
CHOKE = {'notes': ('Bb1', 'C2')}        # v11: the drum's note in each of its last bars
LEAD = {'beats': 1, 'pitch': 'D2', 'gain': '-27dB', 'vel': .8}   # v11: beats before the one that the bass's fundamental holds; its note; its fader.
# Bench (g.sh, gread.py, raw, bar 48 by beat): at the fundamental's own fader (-21 dB) the note alone read -31.3 dBFS where the caught bar's click reads -43.2 and the groove either side -22.3: the bar's second half 12 dB over its first.
# 6 dB less: over the click and 15 under the groove (Least Common's stands 2 dB over its break; a sine at 73 Hz wants more than a click does to be heard at all).
# RENDERED IN FULL WITH TWO BEATS HELD: the scorer's sections fell from 10 to 8 at its highest cut on both seeds (structure 99.33 for 100), and with the lead out they were 10 again (first/: nl11, ng11): half a caught bar with the bass's
# band in it is half a catch. One beat: a pickup into the one, and the catch is a catch for three beats of its four
EXCHANGE = {'per': 1.5, 'back': 0.72, 'feed': '3dB', 'pan': 0.3, 'down': 8}   # v10: Small Change's exchange: how many of its units make a sixteenth; what each loop gives back a pass (the first pair's is 0.62 and its passes are half as often again); what it takes of the seed (the first pair takes 0 dB; see the bench below); how far to each side (the first pair is at 0.5); beats over which it is let down.
# Bench (xc.sh, xcread.py: the song less v9, raw, by unit from the seed of bar 141): taking -2 dB its coins read -33 and -38 on 3 and 5 units where the first pair's read -34 and -32 on 3 and 5 sixteenths, and by bar it stood 1 to 5 dB under the first pair and 18 to 22 under the mix. Taking 0 dB (rendered in full): 3 under to 2 over the first pair, still 16 to 20 under the mix, and in the finished song 0.2 to 0.5 dB on 400 Hz to 3 kHz: these are the fullest bars of the song and the change is a small thing in them. 3 dB more: for four bars the other currency is the one that is heard.
RATE = {'upto': 12, 'gain': '-9dB', 'pan': -0.2}   # v10: the largest amount the click counts (twelve units is two beats); its fader and side (the complement's are -6 dB and 0.2). Bench: at -6 dB its highest sample was -10.4 dBFS beside the complement's -11.0: a second complement, not a count behind it. 3 dB less
GIVEN = {'meet': (3, 5), 'bars': 2 * LEAVE}   # v10: the two cycles whose meeting on the drum the drum rests for; the bars before the meetings go in which it does
ANSWER = {'feed': '-29dB', 'open': 4, 'down': 4}   # v9: what the strings take of the dropped stroke and of its bounces; beats after the cell goes that they are held open; beats over which they are let down.
# Bench (int.sh, intread.py: the song less the song without the answer, raw, by half beat): at -27 dB the answer read -27 -24 -28 -29 -32 -36 -39 from the stroke through bar 169, 7.6 dB under the mix over that bar, and level with
# or over what is between the drum's beats there (-26 to -30) for two beats: 2 dB less
INTEREST = {'back': 0.737, 'feed': '-27dB', 'size': -24}   # v9: what each loop of the smallest purse gives back (0.71 ran out); what it takes of the seed (it was -13: it starts lower and comes up); the clip in the loop, dBFS.
# Bench (the seed and its purse alone by quarter beat): taking -19 dB and clipped at -22 it read -27 -30 -28 -27 -26 -26 -26 -26: up 4 dB in half a beat and then flat at its size, 1.6 dB under the whole mix: a held note, louder; not a swell.
# It comes up 2 dB a quarter beat until it is full: so 8 dB less of the seed, to be full only at the one, and a purse 2 dB smaller
CHEST = 'peak cutoff=71 q=3 gain=4dB'    # v9: on the drum.
# Bench (bars 143 to 146, raw): with q 1.5 the bell reached the drum's own note and its octave: the drum's beats read 3 dB more (-16 for -19 by quarter beat), the whole mix 1.8 dB more, and 60 to 85 Hz 3.7: a louder drum, not a chest. So q 3
DROP = {'share': 0.75, 'bounces': 8, 'rest': 7, 'ring': 1.0, 'db': 3}   # v8: each bounce's gap and level as a share of the one before; how many are heard; sixteenths from the stroke to where the next would fall; the dropped stroke's ring (let go) and dB on it.
# Bench (part.sh, partread.py: the stroke and its bounces alone by 60 ms; the mix with and without). Stopped as the hand had left it (a 28 ms tap) and 6 dB up, the stroke's highest sample was -8.5 dBFS and its bounces moved the mix 1 or 2 dB in two
# sixths of a second: a loud tap and nothing after it. Let go (it rings a second), the same bounces have a note to ring on
PART = {'side': {3: -0.45, 5: 0.45, 7: 0.0}, 'hp': {3: 1200, 5: 1200, 7: 1200}, 'gain': '4dB'}   # v8: where each cycle's click stands (Least Common's places), the high-pass that takes the ping's note out of it, the buses' fader.
# Bench: with the three's high-pass at 5 kHz, the five's at 2 kHz and the seven's at 1.2 kHz and the fader at 0 dB the clicks stood 12.4 dB under the pings and 13 to 16 under the mix from 1 to 5 kHz, and the three's was nearly nothing
# (25 under the mix from 5 to 10 kHz: a vibraphone bar has little up there). So one high-pass for all three, and 4 dB more
TAME = 'peak cutoff=587 q=3 gain=-3dB'  # v7: on the pings (Least Common's)
TRUE = {'feed': '-33dB'}                # v7: what the strings take of the cell.
# Bench, by difference (the song with them less the song without, raw): at Ring True's -30 dB they stood 9 to 11 dB under the mix in bars 153 to 160 and 6 to 7 above 300 Hz, and put 3.6 dB on the song from 500 Hz to 1 kHz there (547 Hz is 6.4 over the album's envelope already): 3 dB less
TURNED = ({3: 'G2', 5: 'Bb2', 7: 'D3'}, {3: 'Bb2', 5: 'D3', 7: 'G3'}, {3: 'D3', 5: 'G3', 7: 'Bb3'})   # v7: the triad's three positions (Least Common's)
TURN_DB = (0, -1, -2)                   # and dB on each (the same head higher stands further forward: Least Common's bench)
PAGE = 105                              # beats between two meetings of all three on the drum
KNOCK = {'notes': {3: 'G2', 5: 'Bb2', 7: 'D3'}, 'gain': '-5dB', 'hold': -10}   # v6: Least Common's knock: each cycle's note; its fader and the clip before it.
# Bench, bars 113 to 128, the 600 ms after each knock: at Least Common's -2 dB two notes at once stood 2.6 dB under this mix from 90 to 123 Hz and level with it from 123 to 200 (this song is thinner there): 3 dB less
WD_KNOCK = {'about': "Wind Down: the drum's answer when a meeting lands on it (v6, after Least Common's lc-knock): a small kettledrum head let ring 800 ms.",
            'synth': {'layers': [{'type': 'modal', 'modes': 'kettle', 'decay': '800ms', 'bright': 0.3, 'strike': 0.3}], 'amp': {'a': '0.5ms', 'd': '0s', 's': 1, 'r': '600ms'}},
            'play': {'event_stable': True, 'vel_sens': 0.4}}
STRINGS = {'strings': (('F2', 87.307, 0.3), ('G2', 97.999, 0.0), ('Bb2', 116.541, -0.3), ('C3', 130.813, 0.15), ('D3', 146.832, -0.15)),   # v6: Ring True's: note, Hz, side
           'feed': '-30dB', 'back': 0.985, 'lp': 5000, 'from': -12}   # what they take of the click; what each gives back a period; the low-pass in the loop; the dB their hand starts from
PAID = {'hz': 233.08, 'coins': (3, 5), 'back': 0.71, 'feed': '-13dB', 'pan': 0.6}   # v6: Small Change's note purse: its unit (B flat 3), its coins, what each loop gives back of itself and the other, what it takes of the seed.
# Giving back 0.70 as it does in Small Change (where it is alone) the note was 9 dB under this mix for half a bar and 22 under by the next: gone before it was heard as held. Giving back 0.71 and taking 6 dB more it is 5, 11 and 18 under by half bar and still 21 to 26 under two bars on
SING = {'walls': (('sing-l', 10.2, '-0.8dB', -0.7), ('sing-r', 6.8, '-0.5dB', 0.7)), 'bars': 4, 'from': -6, 'feed': '18dB', 'fx': ['lp cutoff=4500', 'hp cutoff=200']}   # v5: the near walls: (name, ms away: 1 / 98 Hz and 1 / 147 Hz, what each gives back of itself, side); the room's last bars; the dB their door starts at; what they take of the click.
# The feed is set by solo: a stopped click is so little that at -6 dB the walls stood 33 dB under the mix above 300 Hz in their standing bar; at 14, 10.7; at 18 (and the door from -6, not -12, so that all four bars are heard) see the round's note.
# First try, the two returning EACH OTHER as the far walls do: it did not sing (33 dB gone in 50 ms): a wall on the left hears a wall on the right through its own pan, 6.4 dB lost a pass. So each returns itself
NUDGE = {'reach': 0.25, 'bars': LEAVE}                        # v5: the hand on the cell: beats late at its latest; over its last bars
EASE = -7                                                     # v5: dB on the cell at ring 1 (it was -5)
MID = {'tick': ['peak cutoff=1568 q=1 gain=-6dB', 'peak cutoff=11000 q=0.7 gain=3dB'], 'saw': ['peak cutoff=1600 q=0.8 gain=-5dB']}   # v4
MID_ALONE = 4.5                                               # v4: dB more on the click while it is alone (with its note cut the lone click read 4.6 dB lower: -32.4 for -27.8)
BODY = 'peak cutoff=72 q=1.4 gain=5dB'                        # v4: on the drum
OPEN = {'about': "Wind Down: the meetings' last chord, opening as it dies (v4): wd-held with its low-pass at 600 Hz while the chord is held and opening two octaves over the first two and a half seconds of a six-second release.",
        'synth': {'layers': [{'wave': 'saw', 'detune': -7}, {'wave': 'saw', 'detune': 7}],
                  'filters': [{'kind': 'lp', 'cutoff': {'value': 2400, 'mod': [{'src': 'env.shut', 'amount': -2}]}, 'q': 0.8}],
                  'env': {'shut': {'a': '1ms', 'd': '0s', 's': 1, 'r': '2.5s'}},
                  'amp': {'a': '500ms', 'd': '0s', 's': 1, 'r': '6s'}}, 'play': {'event_stable': True, 'vel_sens': 0.3}}
OPEN_DB = 2                                                   # on its fader: shut at 600 Hz it stood 2 dB lower while held than wd-held did at 900
SUNK = 0.25                                                   # v3 SINK: the share of its speed left on the one: two octaves
SPENT = LEAVE // 2                                            # v3: bars before the change goes in which it spends
HELD = {'len': 4, 'gain': '-28dB', 'vel': .8}                # the last chord: beats held, its fader (at -16 it was the loudest thing in the mix, 1.5 dB under the whole)
REAL = {'bars': LEAVE // 2, 'gain': '-21dB'}                 # the bass's own fundamental: its last bars, its fader (at -13 it was 84% of everything under 60 Hz and the bars 3 dB up)
V3 = {
    'wd-held': {'about': "Wind Down: the meetings' last chord, held (v3): wd-chord's two saws under a low-pass at 900 Hz that does not open, half a second coming and three seconds going.",
                'synth': {'layers': [{'wave': 'saw', 'detune': -7}, {'wave': 'saw', 'detune': 7}], 'filters': [{'kind': 'lp', 'cutoff': 900, 'q': 0.8}],
                          'amp': {'a': '500ms', 'd': '0s', 's': 1, 'r': '3s'}}, 'play': {'event_stable': True, 'vel_sens': 0.3}},
    'wd-under': {'about': "Wind Down: the fundamental the ghost bass never had (v3): a sine at the note.",
                 'synth': {'layers': [{'wave': 'sine'}], 'amp': {'a': '6ms', 'd': '0s', 's': 1, 'r': '50ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.3}},
}
CATCHES = sorted({COMES[k] - 1 for k in GATHER[1:]} | {ALL - 1})   # the bar before each coming, and before all are gathered
LEFT = 0.2                                                    # the share of its speed the spring has left on the one, with STOP
COMP = tuple(s for s in range(8) if s not in PATTERN)        # the pattern's holes: 2, 4, 7
COMP_BARS = (ALL, ALL + HOLD)                                 # home: the hold
HAT_BARS = (ALL + HOLD, RUNS_DOWN)                            # from the first leaving to the drum's
ROW, LAYERS, COUNT, QUIET = 8, 4, 23, 0.04                    # Hearing Things' numbers: bars in a row, layers, the slowest layer's count, the softest stroke kept
LEARNT = ((2, 'D2'), (5, 'F2'), (7, 'C2'), (10, 'D2'), (13, 'F2'), (15, 'C2'))   # Standing Room's bass once it has learnt the room
LEARNT_BARS = (GOES['room'], GOES['room'] + LEAVE)
W_STOP = 2 * WIND * 4 / (1 - LEFT ** 2)                       # beats a platter would take to stop if LEFT of its speed is left after WIND bars
TUCK = 3                                                      # dB
NEW = {
    'wd-comp': {'about': "Wind Down: the complement's click (after Out of Step v2): two cycles of a saw on G5 dying in 12 ms, above 3 kHz, lifted round 10 kHz.",
                'synth': {'layers': ['saw phase=0'], 'filters': ['hp cutoff=3000', 'peak cutoff=10000 q=0.7 gain=8dB'], 'amp': {'a': '0.1ms', 'd': '12ms', 's': 0, 'r': '8ms', 'curve': 3}},
                'play': {'event_stable': True, 'vel_sens': 0.5}},
    'wd-hat': {'about': "Wind Down: the hat (after Hearing Things): the machine's hat, 28 ms, above 5 kHz, whose loudness is all velocity.",
               'synth': {'layers': [{'type': 'machine', 'machine': {'part': 'hat', 'decay': '28ms'}}], 'filters': ['hp cutoff=5000'], 'amp': {'a': '0.1ms', 'd': '0s', 's': 1, 'r': '120ms'}},
               'play': {'event_stable': True, 'vel_sens': 1.0}},
}


def slowing():
    """One row of the hat that slows down for ever (Hearing Things' risset, backwards): (beat in the row, velocity).
    Stroke n of the finest layer falls CYCLE * log2(n / n0) beats before the row's end; it belongs to every layer whose
    count it divides into, and its loudness is the sum of their windows."""
    cycle, n0, out = ROW * 4, COUNT * 2 ** (LAYERS - 1), []
    for n in range(n0, 2 * n0):
        t = cycle * log2(n / n0)
        v = sum(sin(pi * (t / cycle + j) / LAYERS) ** 2 for j in range(LAYERS) if n % 2 ** (LAYERS - 1 - j) == 0) / (LAYERS / 2)
        if v >= QUIET:
            out.append(((cycle - t) % cycle, v))
    return sorted(out)


def w_stop():
    """W_STOP, or with SINK the same for SUNK of its speed left."""
    return 2 * WIND * 4 / (1 - SUNK ** 2) if ON['sink'] else W_STOP


def speed(x):
    """The spring's speed x beats into the wind-down, as a share of full speed."""
    return sqrt(1 - 2 * x / w_stop()) if ON['stop'] else 1 + (SLOW / BPM - 1) * x / (WIND * 4)

open_amp = {'a': '0.2ms', 'd': '0s', 's': 1, 'r': '2.5s', 'curve': 1}
PATCHES = {
    'wd-wood': {'about': "Wind Down: Ring True's wooden bar (1 : 4 : 10), its ring time given by each stroke (expr.ring, seconds over 0.015), with the stick's click on its front (2 ms of noise). It is the click and the cell.",
                'synth': {'layers': [{'type': 'modal', 'modes': 'bar', 'decay': {'value': WOOD[0], 'mod': [{'src': 'expr.ring', 'amount': 1}]}, 'bright': 0.75, 'strike': 0.35},
                                     {'type': 'noise', 'color': 'white', 'level': {'value': '-80dB', 'mod': [{'src': 'env.stick', 'amount': 70}]}}],
                          'env': {'stick': {'a': '0.1ms', 'd': '2ms', 's': 0, 'r': '2ms'}}, 'amp': open_amp},
                'play': {'event_stable': True, 'vel_sens': 0.6}},
    'wd-kick': {'about': "Wind Down: the drum. The machine's bass drum on G, short.",
                'synth': {'layers': [{'type': 'machine', 'machine': {'part': 'kick', 'decay': '240ms', 'click': 0.5, 'drive': 0.2, 'punch': 20}}],
                          'amp': {'a': '0.1ms', 'd': '0s', 's': 1, 'r': '400ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.3}},
    'wd-saw': {'about': 'Wind Down: a click that is five cycles of a saw (after Out of Step): on G3 that is 51 ms.',
               'synth': {'layers': [{'wave': 'saw'}], 'filters': ['lp cutoff=9000'], 'amp': {'a': '0.1ms', 'd': '45ms', 's': 0, 'r': '6ms', 'curve': 0}},
               'play': {'event_stable': True, 'vel_sens': 0.5}},
    'wd-ghost': {'about': 'Wind Down: a bass with no fundamental (after Hearing Things): harmonics two to six of the note and nothing at the note.',
                 'synth': {'layers': [{'type': 'additive', 'partials': [[2, 1], [3, 0.85], [4, 0.6], [5, 0.42], [6, 0.3]]}],
                           'amp': {'a': '4ms', 'd': '0s', 's': 1, 'r': '40ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.3}},
    'wd-ping': {'about': 'Wind Down: what two cycles make when they meet (after Least Common): a vibraphone bar with no motor.',
                'synth': {'layers': [{'type': 'modal', 'modes': 'vibes', 'decay': '650ms', 'bright': 0.55, 'strike': 0.3}],
                          'amp': {'a': '0.3ms', 'd': '900ms', 's': 0, 'r': '200ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.5}},
    'wd-chord': {'about': 'Wind Down: what three cycles make when they meet: a short filtered chord.',
                 'synth': {'layers': [{'wave': 'saw', 'detune': -7}, {'wave': 'saw', 'detune': 7}, {'wave': 'pulse', 'level': '-8dB'}],
                           'filters': [{'kind': 'lp', 'cutoff': {'value': 500, 'mod': [{'src': 'env.f', 'amount': 2.6}]}, 'q': 1.4}],
                           'env': {'f': {'a': '1ms', 'd': '140ms', 's': 0, 'r': '80ms'}},
                           'amp': {'a': '1ms', 'd': '220ms', 's': 0, 'r': '90ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.4}},
    'wd-seed': {'about': 'Wind Down: the seed (after Small Change): a short vibraphone bar with 2 ms of noise on its front.',
                'synth': {'layers': [{'type': 'modal', 'modes': 'vibes', 'decay': '180ms', 'bright': 0.6, 'strike': 0.3},
                                     {'type': 'noise', 'color': 'white', 'level': {'value': '-80dB', 'mod': [{'src': 'env.tick', 'amount': 70}]}}],
                          'env': {'tick': {'a': '0.1ms', 'd': '2ms', 's': 0, 'r': '2ms'}},
                          'amp': {'a': '0.3ms', 'd': '250ms', 's': 0, 'r': '80ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.4}},
}


def ring_s(r):
    return WOOD[0] * (WOOD[1] / WOOD[0]) ** r


def wood(at, pitch, vel, r, ease=-5):
    """One stroke on the bar at ring r (0 stopped .. 1 let go): its ring time, and 5 dB off at ring 1 so that letting go is a swell."""
    return {'at': round(at, 4), 'len': 0.25, 'pitch': pitch, 'vel': vel, 'expr': {'ring': round(ring_s(r) - WOOD[0], 5)}, 'gain': f'{round(ease * max(r, 0), 2)}dB'}


def hand(x):
    """v5 NUDGE: x beats into the cell's last bars, how late the hand has made it (beats) and how fast that is changing (beats a beat)."""
    span = NUDGE['bars'] * 4
    return NUDGE['reach'] * sin(pi * x / span) ** 2, NUDGE['reach'] * pi / span * sin(2 * pi * x / span)


def coins_for(amount, p, q):
    """v10: the fewest coins of p and q that make an amount, or None if it cannot be paid."""
    ways = [i + (amount - i * p) // q for i in range(amount // p + 1) if (amount - i * p) % q == 0]
    return min(ways) if ways else None


def given(beat):
    """v10 GIVEN: whether the drum gives this beat (counted from the top of the song) to the answer."""
    return ON['given'] and ON['knock'] and GOES['meetings'] - GIVEN['bars'] <= beat // 4 < GOES['meetings'] and tuple(c for c in CYCLES if beat * 4 % c == 0) == GIVEN['meet']


def caught(bar):
    return ON['catch'] and bar in CATCHES


def told(bar):
    """v12: what the thing that comes after this caught bar plays of its own figure in the bar's last beat: (track, note) pairs, in time order."""
    b, nxt, last = bar * 4, bar + 1, range(TELL['from'], BAR)
    if nxt == COMES['pattern']:
        return [('saw', {'at': b + (8 + s) / 4, 'len': 0.2, 'pitch': 'G3', 'vel': .62}) for s in PATTERN if 8 + s in last]
    if nxt == COMES['ghost']:
        return [('ghost', {'at': b + s / 4, 'len': 0.45, 'pitch': GHOST[bar % 4][i], 'vel': .85}) for i, s in enumerate((2, 6, 10, 14)) if s in last]
    if nxt == COMES['cell']:
        return [('cell', wood(b + (s % BAR) / 4, pitch, vel, STOPPED, **({'ease': EASE} if ON['ease'] else {}))) for s, pitch, vel in CELL if s // BAR == bar % 2 and s % BAR in last]
    if nxt == COMES['meetings']:
        return [('ping', {'at': s / 4, 'len': 1, 'pitch': PING[m], 'vel': .75}) for s in range(bar * BAR + TELL['from'], (bar + 1) * BAR) for m in [tuple(c for c in CYCLES if s % c == 0)] if len(m) == 2]
    if nxt == COMES['change']:
        return [('seed', {'at': b + 4 - COINS[0] / 4, 'len': 0.25, 'pitch': 'Bb4', 'vel': .9})]
    if nxt == ALL and ON['comp']:
        return [('comp', {'at': b + (8 + s) / 4, 'len': 0.1, 'pitch': 'G5', 'vel': .75}) for s in COMP if 8 + s in last]
    return []


def here(thing, bar):
    return COMES[thing] <= bar < GOES[thing] and not caught(bar)


def build():
    T = {k: [] for k in ('kick', 'tick', 'saw', 'ghost', 'cell', 'ping', 'chord', 'seed', 'comp', 'hat', 'held', 'under')}
    if ON['paid']:
        T['paid'] = []
    if ON['knock']:
        T['knock'] = []
    if ON['rate'] and ON['exchange'] and ON['spent'] and ON['comp']:
        T['rate'] = []
    if ON['lead'] and ON['catch']:
        T['lead'] = []
    for bar in range(BARS):
        b = bar * 4
        down = bar >= RUNS_DOWN
        # from 1: the grid. The click is there from the first bar to the last; in the last WIND bars it is let ring more each bar.
        r = SHUT + (1 - SHUT) * (bar - RUNS_DOWN + 1) / (WIND + 1) if down else SHUT
        for s in (2, 6, 10, 14):
            T['tick'].append(wood(b + s / 4, TICK, .8 if s in (2, 10) else .7, r))
            if ON['sink'] and ON['stop'] and down:            # the note sinks with the speed
                T['tick'][-1]['expr']['sink'] = round(12 * log2(speed((bar - RUNS_DOWN) * 4 + s / 4)), 2)
        if DRUM_IN <= bar < RUNS_DOWN and not caught(bar):
            for beat in range(4):
                if given(b + beat):                             # v10: the beat is the answer's
                    continue
                T['kick'].append({'at': b + beat, 'len': 0.5, 'pitch': CHOKE['notes'][bar - (RUNS_DOWN - len(CHOKE['notes']))] if ON['choke'] and bar >= RUNS_DOWN - len(CHOKE['notes']) else 'G1', 'vel': .95 if beat == 0 else .88})
        if 'lead' in T and caught(bar) and bar > COMES['ghost']:   # v11 LEAD: the bass comes back before the drum
            T['lead'].append({'at': b + 4 - LEAD['beats'], 'len': LEAD['beats'], 'pitch': LEAD['pitch'], 'vel': LEAD['vel']})
            if ON['whole'] and bar in WHOLE['bars']:            # v12 WHOLE: the bass's own voice with it: whole for a beat
                T['ghost'].append({'at': b + 4 - LEAD['beats'], 'len': LEAD['beats'], 'pitch': LEAD['pitch'], 'vel': LEAD['vel'], 'gain': WHOLE['gain']})
        for tr, n in (told(bar) if ON['tell'] and caught(bar) else []):   # v12 TELL: the catch says who is coming
            T[tr].append({**n, 'gain': f"{round(float(n.get('gain', '0dB')[:-2]) + TELL['db'], 2)}dB"})
        if here('pattern', bar):
            slip = (bar - (GOES['pattern'] - LEAVE) + 1) % 8 if ON['slip'] and bar >= GOES['pattern'] - LEAVE else 0
            for half in (0, 8):
                for s in PATTERN:
                    T['saw'].append({'at': b + (half + (s + slip) % 8) / 4, 'len': 0.2, 'pitch': 'G3', 'vel': .8 if s == 0 else .62})
        if here('ghost', bar) and ON['learnt'] and LEARNT_BARS[0] <= bar < LEARNT_BARS[1]:
            for s, pitch in LEARNT:                          # the room has gone: the bass plays what it learnt of it
                T['ghost'].append({'at': b + s / 4, 'len': 0.45, 'pitch': pitch, 'vel': .88 if s == 2 else .8})
        elif here('ghost', bar):
            for i, s in enumerate((2, 6, 10, 14)):
                T['ghost'].append({'at': b + s / 4, 'len': 0.45, 'pitch': GHOST[bar % 4][i], 'vel': .85})
                if ON['real'] and bar >= GOES['ghost'] - REAL['bars']:
                    T['under'].append({'at': b + s / 4, 'len': 0.45, 'pitch': GHOST[bar % 4][i], 'vel': .85})
        if ON['comp'] and COMP_BARS[0] <= bar < COMP_BARS[1]:
            for half in (0, 8):
                for s in COMP:
                    T['comp'].append({'at': b + (half + s) / 4, 'len': 0.1, 'pitch': 'G5', 'vel': .75})
        if ON['hat'] and HAT_BARS[0] <= bar < HAT_BARS[1] and (bar - HAT_BARS[0]) % ROW == 0 and bar + ROW <= HAT_BARS[1]:
            T['hat'] += [{'at': round(b + t, 4), 'len': 0.1, 'pitch': 'A5', 'vel': round(v, 3)} for t, v in slowing()]
        if here('cell', bar):
            lo, hi = LET_GO
            r = STOPPED if bar < lo else 1 if bar >= hi else STOPPED + (1 - STOPPED) * (bar - lo) / (hi - lo)
            if ON['taken'] and bar >= GOES['cell'] - LEAVE:    # taken back into the hand: stopped again by its last bar
                r = 1 - (1 - STOPPED) * (bar - (GOES['cell'] - LEAVE) + 1) / LEAVE
            for s, pitch, vel in CELL:
                if s // BAR == bar % 2:
                    T['cell'].append(wood(b + (s % BAR) / 4, pitch, vel, r, **({'ease': EASE} if ON['ease'] else {})))
                    if ON['grip'] and ON['taken'] and bar >= GOES['cell'] - LEAVE:   # v11 GRIP: the hand on the bar's middle: an equal-power pair
                        x = (bar - (GOES['cell'] - LEAVE) + 1) / LEAVE
                        T['cell'][-1]['expr'].update(note=round(10 * log10(1 - (1 - 10 ** (GRIP['note'] / 10)) * x), 2), mode=round(-float(GRIP['from'][:-2]) + 10 * log10(x), 2))
                    if ON['nudge'] and bar >= GOES['cell'] - NUDGE['bars']:   # the hand: late, and its note with its speed
                        late, rate = hand((bar - (GOES['cell'] - NUDGE['bars'])) * 4 + (s % BAR) / 4)
                        T['cell'][-1]['at'] = round(T['cell'][-1]['at'] + late, 4)
                        T['cell'][-1]['expr']['sink'] = round(-12 * log2(1 + rate), 2)
            if ON['drop'] and bar == GOES['cell'] - 1:         # v8 DROP: the cell's last stroke goes by a track of its own, so that only it bounces
                n = T['cell'].pop()
                let = wood(n['at'], n['pitch'], n['vel'], DROP['ring'], **({'ease': EASE} if ON['ease'] else {}))   # let go, where the hand had it stopped
                T['cell-drop'] = [{**let, 'expr': {**{k: v for k, v in n['expr'].items() if k not in ('note', 'mode')}, 'ring': let['expr']['ring']}, 'gain': f"{round(float(let['gain'][:-2]) + DROP['db'], 2)}dB"}]
        if here('meetings', bar):
            for s in range(bar * BAR, (bar + 1) * BAR):          # the cycles are counted from the top of the song; nobody plays them
                meet = tuple(c for c in CYCLES if s % c == 0)
                if len(meet) == 2:
                    T['ping'].append({'at': s / 4, 'len': 1, 'pitch': PING[meet], 'vel': .75})
                elif len(meet) == 3:
                    T['chord'].append({'at': s / 4, 'len': 0.5, 'pitch': ','.join(CHORD), 'vel': .8})
                if ON['knock'] and len(meet) >= 2 and s % 4 == 0:   # v6 KNOCK: a meeting on the drum
                    pos = (s // 4 // PAGE - COMES['meetings'] * 4 // PAGE) % len(TURNED) if ON['turn'] else 0   # v7 TURN: how many times all three have met on the drum since the meetings came
                    T['knock'].append({'at': s / 4, 'len': 0.5, 'pitch': ','.join((TURNED[pos] if ON['turn'] else KNOCK['notes'])[c] for c in meet), 'vel': .8,
                                       **({'gain': f'{TURN_DB[pos]}dB'} if ON['turn'] and TURN_DB[pos] else {})})
        spending = ON['spent'] and here('change', bar) and bar >= GOES['change'] - SPENT
        if here('change', bar) and ((bar - COMES['change']) % 2 == 0 or spending):
            T['seed'].append({'at': b, 'len': 0.25, 'pitch': 'Bb4', 'vel': .9})
            if spending and 'rate' in T:                        # v10 RATE: what the other currency can pay of this seed, between the sixteenths
                T['rate'] += [{'at': round(b + a / (4 * EXCHANGE['per']), 4), 'len': 0.1, 'pitch': 'G5', 'vel': round(.8 - .13 * (coins_for(a, *COINS) - 1), 2)}
                              for a in range(1, RATE['upto'] + 1) if coins_for(a, *COINS) and (a / EXCHANGE['per']) % 1]
            if spending and bar == GOES['change'] - 1:
                T['paid' if ON['paid'] else 'seed'].append({'at': b + 2, 'len': 0.25, 'pitch': 'Bb4', 'vel': .9})   # v6 PAID: the very last seed goes to the smallest purse
        if ON['held'] and bar == GOES['meetings']:
            T['held'].append({'at': b, 'len': HELD['len'], 'pitch': ','.join(CHORD), 'vel': HELD['vel']})
    # the final stroke: the click, let go altogether, on the one
    T['tick'].append(wood(BARS * 4, LAST, .9, 1))
    T['tick'][-1]['gain'] = '0dB'
    if ON['sink'] and ON['stop']:                             # the last stroke is where the sinking has got to
        T['tick'][-1].update(pitch=TICK)
        T['tick'][-1]['expr']['sink'] = round(12 * log2(SUNK), 2)
    return T


def door(thing):
    """A bus fader that is shut (-60 dB) until its thing comes, open while it is here, and shut again over two bars as it goes."""
    a, z = COMES[thing] * 4, GOES[thing] * 4
    return {'points': [['0b', -60]] + ([[f'{a - 8}b', -60]] if a >= 8 else []) + [[f'{a}b', 0], [f'{z}b', 0], [f'{z + 8}b', -60], [f'{BARS * 4}b', -60]], 'curve': 0}


def near():
    """v5 SING: the near walls' door: shut until the room's last bars, up from SING['from'] dB to 0 by its last bar, and shut with the room's."""
    a, z = (GOES['room'] - SING['bars']) * 4, GOES['room'] * 4
    return {'points': [['0b', -60], [f'{a - 1}b', -60], [f'{a}b', SING['from']], [f'{z - 4}b', 0], [f'{z}b', 0], [f'{z + 8}b', -60], [f'{BARS * 4}b', -60]], 'curve': 0}


def alone():
    """The click's fader ride: ALONE dB before the drum comes, 0 while anything else plays, back up over the first bar of the wind-down."""
    a, z = DRUM_IN * 4, RUNS_DOWN * 4
    low = ALONE + (TUCK if ON['tuck'] else 0)
    up = low + (MID_ALONE if ON['mid'] else 0)                # v4: the lone click stands where it stood before its note was cut
    pts = [['0b', up], [f'{a - 0.5}b', up], [f'{a}b', 0]]
    for bar in (CATCHES if ON['catch'] else []):              # the click is alone in a caught bar too
        pts += [[f'{bar * 4 - 0.25}b', 0], [f'{bar * 4}b', up], [f'{bar * 4 + 3.5}b', up], [f'{bar * 4 + 4}b', 0]]
    # as the spring runs down the note sinks out of the cut, so what was added for it is taken off again by the last stroke
    return {'points': pts + [[f'{z}b', 0], [f'{z + 4}b', up]] + ([[f'{BARS * 4}b', low]] if up != low else []) + [[f'{BARS * 4 + 4}b', low]], 'curve': 0}


def song():
    T = build()
    db = lambda x: f'{20 * log10(x):.2f}dB'
    under = {'type': 'pump', 'on': 'kick', 'depth': '-4dB', 'release': '170ms'}
    hold = lambda d: f'clip drive=0dB ceiling={d}dB'
    buses = {'hall': {'fx': ['reverb kind=hall decay=3.2s mix=1 predelay=25ms', 'hp cutoff=350', 'lp cutoff=6000']}}
    for me, you, n, side in (('wall-l', 'wall-r', WALLS[0], -0.7), ('wall-r', 'wall-l', WALLS[1], 0.7)):
        buses[me] = {'pan': side, 'gain': {'value': '0dB', 'mod': [{'src': 'auto.door', 'amount': 1}]}, 'auto': {'door': door('room')},
                     'fx': ['lp cutoff=4500', 'hp cutoff=300'],
                     'returns': [{'from': 'tick', 'gain': '-4dB', 'time': f'{n}/16'}, {'from': you, 'gain': '-3dB', 'time': f'{n}/16'}]}
    for me, you, n, semi, side in (('coin-up', 'coin-down', COINS[0], UP, -0.5), ('coin-down', 'coin-up', COINS[1], DOWN, 0.5)):
        t = f'{n * S16 - LAG[semi]:.2f}ms'
        buses[me] = {'pan': side, 'fx': [{'type': 'pitch', 'semitones': semi, 'mix': 1}, 'lp cutoff=10000', 'hp cutoff=150'],
                     'returns': [{'from': 'seed', 'gain': '0dB', 'time': t}, {'from': me, 'gain': db(GIVE), 'time': t}, {'from': you, 'gain': db(GIVE), 'time': t}]}
    if ON['exchange'] and ON['spent']:                         # v10: the same seeds in another currency, for the bars the change spends in
        a, z, u = (GOES['change'] - SPENT) * 4, GOES['change'] * 4, S16 / EXCHANGE['per']
        hand = {'points': [['0b', -60], [f'{a - 0.05}b', -60], [f'{a}b', 0], [f'{z}b', 0], [f"{z + EXCHANGE['down']}b", -60], [f'{BARS * 4}b', -60]], 'curve': 0}
        for me, you, n, semi, side in (('xcoin-up', 'xcoin-down', COINS[0], UP, -EXCHANGE['pan']), ('xcoin-down', 'xcoin-up', COINS[1], DOWN, EXCHANGE['pan'])):
            t = f'{n * u - LAG[semi]:.2f}ms'
            buses[me] = {'pan': side, 'gain': {'value': '0dB', 'mod': [{'src': 'auto.hand', 'amount': 1}]}, 'auto': {'hand': hand},
                         'fx': [{'type': 'pitch', 'semitones': semi, 'mix': 1}, 'lp cutoff=10000', 'hp cutoff=150'],
                         'returns': [{'from': 'seed', 'gain': EXCHANGE['feed'], 'time': t}, {'from': me, 'gain': db(EXCHANGE['back']), 'time': t}, {'from': you, 'gain': db(EXCHANGE['back']), 'time': t}]}
    end = BARS * 4
    doc = {
        'about': "Chirpers, Escapement, track 8: Wind Down, by chirper-one. Generated by compose/chirpers11/src/chirpers11-t8.py (its docstring is the rule). The closer: one thing from each of the other seven songs, gathered a section at a time on one grid in G minor, held, and let go one at a time until the click that opened the record is alone; then the tempo runs down from 124 to 50 and the last stroke, let ring, lands on the one.",
        'meta': {'artist': 'chirpers', 'album': 'Escapement', 'title': 'Wind Down', 'track': 8, 'year': 2026},
        'tempo': [{'at': '0b', 'bpm': BPM}, {'at': f'{RUNS_DOWN * 4}b', 'bpm': BPM}] +
                 ([{'at': f'{RUNS_DOWN * 4 + x}b', 'bpm': round(BPM * speed(x), 3), 'ramp': True} for x in range(1, WIND * 4 + 1)] if ON['stop'] else
                  [{'at': f'{end}b', 'bpm': SLOW, 'ramp': True}]),
        'seed': 1, 'event_stable': True, 'length': f'{end + 4}b', 'tail': '4s', 'ceiling': '-1dB', 'true_peak': True, 'loudness': -12,
        'patches': PATCHES, 'buses': buses,
        'master': {'fx': [{'type': 'eq', 'bands': ['hp cutoff=28']}]},
        'tracks': [
            {'name': 'kick', 'patch': 'wd-kick', 'gain': '-9dB', 'notes': T['kick'], 'fx': [{'type': 'eq', 'bands': ['peak cutoff=47 q=1.2 gain=-3dB', 'peak cutoff=130 q=0.9 gain=3dB'] + ([CHEST] if ON['chest'] else [])}]},
            {'name': 'ghost', 'patch': 'wd-ghost', 'gain': '-20dB', 'notes': T['ghost'], 'fx': ['lp cutoff=900', under]},
            {'name': 'tick', 'patch': 'wd-wood', 'gain': {'value': '-7dB', 'mod': [{'src': 'auto.alone', 'amount': 1}]}, 'auto': {'alone': alone()}, 'pan': 0, 'notes': T['tick'], 'fx': [hold(-12)], 'sends': {'hall': '-16dB'}},
            {'name': 'saw', 'patch': 'wd-saw', 'gain': '-12dB', 'pan': -0.25, 'notes': T['saw']},
            {'name': 'cell', 'patch': 'wd-wood', 'gain': '-1dB', 'pan': 0.3, 'notes': T['cell'], 'sends': {'hall': '-12dB'}},
            {'name': 'ping', 'patch': 'wd-ping', 'gain': '-12dB', 'pan': -0.15, 'notes': T['ping'], 'sends': {'hall': '-10dB'}},
            {'name': 'chord', 'patch': 'wd-chord', 'gain': '-8dB', 'pan': 0.1, 'notes': T['chord'], 'fx': [hold(-8), under], 'sends': {'hall': '-8dB'}},
            {'name': 'seed', 'patch': 'wd-seed', 'gain': '-6dB', 'notes': T['seed'], 'fx': [hold(-12)]},
        ],
    }
    by_name = {t['name']: t for t in doc['tracks']}
    if ON['tame']:
        by_name['ping']['fx'] = [{'type': 'eq', 'bands': [TAME]}] + by_name['ping'].get('fx', [])
    if ON['mid']:
        by_name['tick']['fx'] = by_name['tick']['fx'] + [{'type': 'eq', 'bands': MID['tick']}]
        by_name['saw']['fx'] = [{'type': 'eq', 'bands': MID['saw']}]
    if ON['body']:
        by_name['kick']['fx'] = [{'type': 'eq', 'bands': by_name['kick']['fx'][0]['bands'] + [BODY]}]
    if ON['tuck']:
        by_name['tick']['gain']['value'] = f"{float(by_name['tick']['gain']['value'][:-2]) - TUCK:g}dB"
    if ON['comp']:
        doc['patches'] = {**doc['patches'], 'wd-comp': NEW['wd-comp']}
        doc['tracks'].append({'name': 'comp', 'patch': 'wd-comp', 'gain': '-6dB', 'pan': 0.2, 'notes': T['comp']})
        if T.get('rate'):                                      # v10 RATE: the same click on the other side
            doc['tracks'].append({'name': 'rate', 'patch': 'wd-comp', 'gain': RATE['gain'], 'pan': RATE['pan'], 'notes': T['rate']})
    if ON['sink'] and ON['stop']:
        sunk = json.loads(json.dumps(PATCHES['wd-wood']))
        sunk['about'] = "Wind Down: the click whose note can sink (v3): wd-wood with the whole voice's pitch on the stroke (expr.sink, semitones)."
        sunk['synth']['pitch'] = {'value': 0, 'mod': [{'src': 'expr.sink', 'amount': 1}]}
        doc['patches'] = {**doc['patches'], 'wd-sink': sunk}
        by_name['tick']['patch'] = 'wd-sink'
    if ON['nudge']:                                           # the cell's notes move with the hand: the same patch as the sinking click
        if 'wd-sink' not in doc['patches']:
            sunk = json.loads(json.dumps(PATCHES['wd-wood']))
            sunk['about'] = "Wind Down: the bar whose note can move (v3): wd-wood with the whole voice's pitch on the stroke (expr.sink, semitones)."
            sunk['synth']['pitch'] = {'value': 0, 'mod': [{'src': 'expr.sink', 'amount': 1}]}
            doc['patches'] = {**doc['patches'], 'wd-sink': sunk}
        by_name['cell']['patch'] = 'wd-sink'
    if ON['grip'] and ON['taken']:                            # v11: the cell's bar twice, the second two octaves up, each with its own level on the stroke
        held = json.loads(json.dumps(doc['patches'][by_name['cell']['patch']]))
        bar_layer = held['synth']['layers'][0]
        held['about'] = "Wind Down: the bar with a hand on its middle (v11, after Ring True's rt-held): the cell's patch, and its bar a second time two octaves up (a wooden bar's second mode). Each has its level on the stroke: expr.note (dB on the note, 0 with no hand) and expr.mode (dB over -40 on the second mode)."
        held['synth']['layers'] = [{**bar_layer, 'level': {'value': '0dB', 'mod': [{'src': 'expr.note', 'amount': 1}]}}] + held['synth']['layers'][1:] + [{**bar_layer, 'semi': GRIP['semis'], 'level': {'value': GRIP['from'], 'mod': [{'src': 'expr.mode', 'amount': 1}]}}]
        doc['patches'] = {**doc['patches'], GRIP['patch']: held}
        by_name['cell']['patch'] = GRIP['patch']
    if ON['sing']:
        for me, ms, back, side in SING['walls']:
            doc['buses'][me] = {'pan': side, 'gain': {'value': '0dB', 'mod': [{'src': 'auto.near', 'amount': 1}]}, 'auto': {'near': near()}, 'fx': SING['fx'],
                                'returns': [{'from': 'tick', 'gain': SING['feed'], 'time': f'{ms}ms'}, {'from': me, 'gain': back, 'time': f'{ms}ms'}]}
    if ON['strings']:
        hand = {'points': ([['0b', -60], [f'{RUNS_DOWN * 4 - 1}b', -60], [f'{RUNS_DOWN * 4}b', STRINGS['from']], [f'{RUNS_DOWN * 4 + 8}b', 0], [f'{BARS * 4 + 16}b', 0]] if ON['early'] else
                           [['0b', -60], [f'{BARS * 4 - 0.5}b', -60], [f'{BARS * 4}b', 0], [f'{BARS * 4 + 16}b', 0]]), 'curve': 0}
        if ON['true']:                                         # v7: let go beside the cell from where the room goes to where the cell goes
            hand['points'] = hand['points'][:1] + [[f"{GOES['room'] * 4 - 1}b", -60], [f"{GOES['room'] * 4}b", 0], [f"{GOES['cell'] * 4 - 0.5}b", 0], [f"{GOES['cell'] * 4}b", -60]] + hand['points'][1:]
            if ON['answer'] and T.get('cell-drop'):            # v9: held open through the bar after the cell, then let down
                hand['points'][3:5] = [[f"{GOES['cell'] * 4 + ANSWER['open']}b", 0], [f"{GOES['cell'] * 4 + ANSWER['open'] + ANSWER['down']}b", -60]]
        for name, hz, side in STRINGS['strings']:
            me = 'str-' + name.lower()
            t = f"{1000 / hz - 225.1 / STRINGS['lp']:.3f}ms"         # a period, less the low-pass's own delay, so the loop is in tune
            doc['buses'][me] = {'pan': side, 'gain': {'value': '0dB', 'mod': [{'src': 'auto.hand', 'amount': 1}]}, 'auto': {'hand': hand}, 'fx': [f"lp cutoff={STRINGS['lp']}"],
                                'returns': [{'from': 'tick', 'gain': STRINGS['feed'], 'time': t}] + ([{'from': 'cell', 'gain': TRUE['feed'], 'time': t}] if ON['true'] else []) +
                                           ([{'from': x, 'gain': ANSWER['feed'], 'time': t} for x in ('cell-drop', 'cell-bounce')] if ON['true'] and ON['answer'] and T.get('cell-drop') else []) + [{'from': me, 'gain': db(STRINGS['back']), 'time': t}]}
    if T.get('cell-drop'):                                     # v8 DROP: the same track again for the one stroke, and its bounces: echoes of it, each sooner and softer by the same share
        doc['tracks'].append({**{x: y for x, y in by_name['cell'].items() if x != 'notes'}, 'name': 'cell-drop', 'notes': T['cell-drop']})
        gap = DROP['rest'] * 60000 / BPM / 4 * (1 - DROP['share']) / (1 - DROP['share'] ** (DROP['bounces'] + 1))
        doc['buses']['cell-bounce'] = {'pan': by_name['cell']['pan'], 'returns': [{'from': 'cell-drop', 'gain': f"{20 * log10(DROP['share']) * j:.2f}dB", 'time': f"{gap * (1 - DROP['share'] ** j) / (1 - DROP['share']):.1f}ms"} for j in range(1, DROP['bounces'] + 1)]}
    if ON['part'] and T['ping']:                               # v8 PART: the pings by pair, a track each (the same track three times), so that each cycle's bus hears only its own meetings
        base = {x: y for x, y in by_name['ping'].items() if x != 'notes'}
        doc['tracks'] = [t for t in doc['tracks'] if t['name'] != 'ping'] + [{**base, 'name': f'ping-{a}{b}', 'notes': [n for n in T['ping'] if n['pitch'] == PING[(a, b)]]} for a, b in PING]
        for c in CYCLES:
            doc['buses'][f'part-{c}'] = {'pan': PART['side'][c], 'gain': PART['gain'], 'fx': [f"hp cutoff={PART['hp'][c]}"],
                                         'returns': [{'from': f'ping-{a}{b}', 'gain': '0dB', 'time': f'{c * 60000 / BPM / 4:.2f}ms'} for a, b in PING if c in (a, b)]}
    if ON['knock'] and T['knock']:
        doc['patches'] = {**doc['patches'], 'wd-knock': WD_KNOCK}
        doc['tracks'].append({'name': 'knock', 'patch': 'wd-knock', 'gain': KNOCK['gain'], 'notes': T['knock'], 'fx': [hold(KNOCK['hold'])]})
    if ON['paid'] and T['paid']:
        doc['tracks'].append({'name': 'paid', 'patch': 'wd-seed', 'gain': by_name['seed']['gain'], 'notes': T['paid'], 'fx': [hold(-12)]})
        u, (p, q) = 1000 / PAID['hz'], PAID['coins']
        for coin, other, side in ((p, q, -1), (q, p, 1)):
            me, t = f'paid{coin}', f'{coin * u:.3f}ms'
            doc['buses'][me] = {'pan': side * PAID['pan'], 'gain': '0dB', 'fx': ['lp cutoff=6000', 'hp cutoff=40'],
                                'returns': [{'from': 'paid', 'gain': PAID['feed'], 'time': t}, {'from': me, 'gain': db(PAID['back']), 'time': t}, {'from': f'paid{other}', 'gain': db(PAID['back']), 'time': t}]}
            if ON['interest']:                                 # v9: the purse gives back more than it is given, cannot hold more than its size, and is shut on the one
                one = GOES['change'] * 4
                doc['buses'][me] = {'pan': side * PAID['pan'], 'gain': {'value': '0dB', 'mod': [{'src': 'auto.shut', 'amount': 1}]}, 'auto': {'shut': {'points': [['0b', 0], [f'{one - 0.03}b', 0], [f'{one}b', -60], [f'{BARS * 4 + 16}b', -60]], 'curve': 0}},
                                    'fx': ['lp cutoff=6000', 'hp cutoff=40', hold(INTEREST['size'])],
                                    'returns': [{'from': 'paid', 'gain': INTEREST['feed'], 'time': t}, {'from': me, 'gain': db(INTEREST['back']), 'time': t}, {'from': f'paid{other}', 'gain': db(INTEREST['back']), 'time': t}]}
    if ON['held']:
        doc['patches'] = {**doc['patches'], **({'wd-open': OPEN} if ON['open'] else {'wd-held': V3['wd-held']})}
        doc['tracks'].append({'name': 'held', 'patch': 'wd-open' if ON['open'] else 'wd-held', 'gain': f"{float(HELD['gain'][:-2]) + OPEN_DB:g}dB" if ON['open'] else HELD['gain'], 'pan': -0.1, 'notes': T['held'], 'fx': [under], 'sends': {'hall': '-6dB'}})
    if ON['real']:
        doc['patches'] = {**doc['patches'], 'wd-under': V3['wd-under']}
        doc['tracks'].append({'name': 'under', 'patch': 'wd-under', 'gain': REAL['gain'], 'notes': T['under'], 'fx': [under]})
    if T.get('lead'):
        doc['patches'] = {**doc['patches'], 'wd-under': V3['wd-under']}
        doc['tracks'].append({'name': 'lead', 'patch': 'wd-under', 'gain': LEAD['gain'], 'notes': T['lead']})
    if ON['hat']:
        doc['patches'] = {**doc['patches'], 'wd-hat': NEW['wd-hat']}
        doc['tracks'].append({'name': 'hat', 'patch': 'wd-hat', 'gain': '6dB', 'pan': -0.2, 'notes': T['hat'], 'sends': {'hall': '-18dB'}})
    return doc


def dump(doc):
    lines = []
    for k, v in doc.items():
        if k == 'tracks':
            lines.append('tracks:')
            lines += ['  - ' + json.dumps(t) for t in v]
        else:
            lines.append(f'{k}: {json.dumps(v)}')
    return '\n'.join(lines) + '\n'


def clock(bar):
    """Seconds at the top of a bar: steady to RUNS_DOWN, then a tempo falling in a straight line (against beats) to SLOW."""
    t = min(bar, RUNS_DOWN) * 4 * 60 / BPM
    if bar > RUNS_DOWN:
        n, x = WIND * 4, (bar - RUNS_DOWN) * 4
        if ON['stop']:                                        # a platter's: x beats take W - sqrt(W^2 - 2 W x) beats of full speed
            return t + 60 / BPM * (w_stop() - sqrt(w_stop() ** 2 - 2 * w_stop() * x))
        k = (SLOW - BPM) / n
        t += 60 / k * log((BPM + k * x) / BPM)
    return t


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--out', type=Path, default=OUT)
    ap.add_argument('--form', action='store_true', help='print the form and stop')
    for k in [k for k, on in ON.items() if not on]:
        ap.add_argument(f'--with-{k}', action='store_true', help=f'put in {k} (written, and off)')
    for k in [k for k, on in ON.items() if on]:
        ap.add_argument(f'--without-{k}', action='store_true', help=f'leave out {k} (the last two off is v11, the last five v10, the last eight v9, the last eleven v8, the last thirteen v7, the last sixteen v6, the last nineteen v5, the last twenty-two v4, the last twenty-five v3, the last thirty-one v2, all thirty-seven v1)')
    a = ap.parse_args()
    for k in ON:
        ON[k] = getattr(a, f'with_{k}') if not ON[k] else not getattr(a, f'without_{k}')
    if a.form:
        marks = sorted([(COMES[k], f'{k} comes') for k in GATHER] + [(DRUM_IN, 'the drum comes'), (ALL, 'all gathered'), (LET_GO[0], 'the cell is let go')] +
                       [(GOES[k], f'{k} goes' if k != 'grid' else 'the drum goes; the spring runs down') for k in GATHER] + [(BARS, 'the last stroke, on the one')] +
                       ([(b, 'caught') for b in CATCHES] if ON['catch'] else []) +
                       ([(COMP_BARS[0], 'the complement fills the holes'), (COMP_BARS[1], 'the complement goes')] if ON['comp'] else []) +
                       ([(HAT_BARS[0], 'the hat that slows for ever')] if ON['hat'] else []) +
                       ([(LEARNT_BARS[0], "the bass plays the room's figure"), (LEARNT_BARS[1], 'the bass is itself again')] if ON['learnt'] else []) +
                       ([(GOES['change'] - SPENT, 'the change spends what is left')] if ON['spent'] else []) +
                       ([(GOES['change'] - SPENT, 'the change is also paid in another currency: coins of 3 and 5 of a unit two thirds of a sixteenth (three for two)')] if ON['exchange'] and ON['spent'] else []) +
                       ([(GOES['change'] - SPENT, "the complement's click counts what the other currency can pay, between the sixteenths: " + ' '.join(str(a) for a in range(1, RATE['upto'] + 1) if coins_for(a, *COINS) and (a / EXCHANGE['per']) % 1) + ' units after each seed')] if ON['rate'] and ON['exchange'] and ON['spent'] and ON['comp'] else []) +
                       ([(beat // 4, f'the drum gives beat {beat % 4 + 1} to the answer: the three and the five meet on it') for beat in range(BARS * 4) if given(beat)]) +
                       ([(GOES['meetings'], 'the last chord, held')] if ON['held'] else []) +
                       ([(GOES['cell'] - LEAVE, 'the cell is taken back into the hand')] if ON['taken'] else []) +
                       ([(GOES['cell'] - LEAVE, "the hand is on the bar's middle: bar by bar the cell's note goes and its second mode, two octaves up, is what is left; its dropped stroke has the note again")] if ON['grip'] and ON['taken'] else []) +
                       ([(RUNS_DOWN - len(CHOKE['notes']), 'the beater is held against the drum: its note rises, ' + ' then '.join(CHOKE['notes']))] if ON['choke'] else []) +
                       ([(b, f"the bass comes back before the drum: its fundamental holds {LEAD['pitch']} through the last {'beat' if LEAD['beats'] == 1 else str(LEAD['beats']) + ' beats'}") for b in CATCHES if b > COMES['ghost']] if ON['lead'] and ON['catch'] else []) +
                       ([(b, 'the catch says who is coming: ' + ', '.join(f"{tr} {n['pitch']} on sixteenth {round((n['at'] - b * 4) * 4)}" for tr, n in told(b))) for b in CATCHES if told(b)] if ON['tell'] and ON['catch'] else []) +
                       ([(b, f"for that beat the bass is whole: its own voice plays the {LEAD['pitch']} under its fundamental") for b in CATCHES if b > COMES['ghost'] and b in WHOLE['bars']] if ON['whole'] and ON['lead'] and ON['catch'] else []) +
                       ([(GOES['cell'] - 1, "the hand lets go of the stick: the cell's last stroke bounces")] if ON['drop'] else []) +
                       ([(COMES['meetings'], 'each meeting is heard to part: the two cycles that met click once more, 3, 5 or 7 sixteenths on')] if ON['part'] else []) +
                       ([(GOES['ghost'] - REAL['bars'], 'the bass is given its fundamental')] if ON['real'] else []) +
                       ([(GOES['pattern'] - LEAVE, 'the pattern slips a sixteenth a bar')] if ON['slip'] else []) +
                       ([(GOES['room'] - SING['bars'], 'the walls come in until they sing')] if ON['sing'] else []) +
                       ([(RUNS_DOWN if ON['early'] else BARS, "Ring True's strings are let go beside the click")] if ON['strings'] else []) +
                       ([(COMES['meetings'], 'the drum answers each meeting that lands on it')] if ON['knock'] else []) +
                       ([(GOES['room'], "the strings are let go beside the cell, and ring while it rings true")] if ON['true'] and ON['strings'] else []) +
                       ([(b // 4, f"all three meet on the drum: the triad turns over ({' '.join(TURNED[(b // PAGE - COMES['meetings'] * 4 // PAGE) % len(TURNED)][c] for c in CYCLES)})") for b in range(0, GOES['meetings'] * 4, PAGE) if b >= COMES['meetings'] * 4] if ON['turn'] and ON['knock'] else []) +
                       ([(GOES['change'] - 1, "the change's last seed is paid in the smallest coins: a held B flat")] if ON['paid'] else []) +
                       ([(GOES['cell'], "the strings answer the dropped stroke: held open through the bar after the cell, then let down")] if ON['answer'] and ON['true'] and ON['strings'] and ON['drop'] else []) +
                       ([(GOES['change'] - 1, "the last seed is paid with interest: the held B flat swells and is shut on the one")] if ON['interest'] and ON['paid'] else []) +
                       ([(DRUM_IN, 'the drum has a chest: a bell of 4 dB at 71 Hz')] if ON['chest'] else []) +
                       ([(GOES['cell'] - NUDGE['bars'], 'the hand drags the cell a sixteenth late and lets it catch up')] if ON['nudge'] else []))
        for bar, what in marks:
            t = clock(bar)
            print(f'bar {bar + 1:3d}  {int(t) // 60}:{t % 60:05.2f}  {what}')
        T = build()
        print(f'{BARS} bars, {clock(BARS):.1f} s to the last stroke; strokes: ' + ', '.join(f'{k} {len(v)}' for k, v in T.items() if v or k not in ('held', 'under')))
        ticks = [clock(RUNS_DOWN + (bar * 16 + s) / 16) for bar in range(WIND) for s in (2, 6, 10, 14)] + [clock(BARS)]
        print('the spring: the gap between ticks goes ' + ' '.join(f'{(b - a) * 1000:.0f}' for a, b in zip(ticks, ticks[1:]))[:60] + ' ... ' +
              ' '.join(f'{(b - a) * 1000:.0f}' for a, b in zip(ticks[-5:], ticks[-4:])) + ' ms (the last is the half beat to the one)')
    else:
        a.out.write_text(dump(song()))
