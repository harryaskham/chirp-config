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
      'mid': True, 'body': True, 'open': True, 'sing': True, 'nudge': True, 'ease': True, 'strings': True, 'paid': True, 'knock': True, 'early': False, 'true': True, 'turn': True, 'tame': True}
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


def caught(bar):
    return ON['catch'] and bar in CATCHES


def here(thing, bar):
    return COMES[thing] <= bar < GOES[thing] and not caught(bar)


def build():
    T = {k: [] for k in ('kick', 'tick', 'saw', 'ghost', 'cell', 'ping', 'chord', 'seed', 'comp', 'hat', 'held', 'under')}
    if ON['paid']:
        T['paid'] = []
    if ON['knock']:
        T['knock'] = []
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
                T['kick'].append({'at': b + beat, 'len': 0.5, 'pitch': 'G1', 'vel': .95 if beat == 0 else .88})
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
                    if ON['nudge'] and bar >= GOES['cell'] - NUDGE['bars']:   # the hand: late, and its note with its speed
                        late, rate = hand((bar - (GOES['cell'] - NUDGE['bars'])) * 4 + (s % BAR) / 4)
                        T['cell'][-1]['at'] = round(T['cell'][-1]['at'] + late, 4)
                        T['cell'][-1]['expr']['sink'] = round(-12 * log2(1 + rate), 2)
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
            {'name': 'kick', 'patch': 'wd-kick', 'gain': '-9dB', 'notes': T['kick'], 'fx': [{'type': 'eq', 'bands': ['peak cutoff=47 q=1.2 gain=-3dB', 'peak cutoff=130 q=0.9 gain=3dB']}]},
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
    if ON['sing']:
        for me, ms, back, side in SING['walls']:
            doc['buses'][me] = {'pan': side, 'gain': {'value': '0dB', 'mod': [{'src': 'auto.near', 'amount': 1}]}, 'auto': {'near': near()}, 'fx': SING['fx'],
                                'returns': [{'from': 'tick', 'gain': SING['feed'], 'time': f'{ms}ms'}, {'from': me, 'gain': back, 'time': f'{ms}ms'}]}
    if ON['strings']:
        hand = {'points': ([['0b', -60], [f'{RUNS_DOWN * 4 - 1}b', -60], [f'{RUNS_DOWN * 4}b', STRINGS['from']], [f'{RUNS_DOWN * 4 + 8}b', 0], [f'{BARS * 4 + 16}b', 0]] if ON['early'] else
                           [['0b', -60], [f'{BARS * 4 - 0.5}b', -60], [f'{BARS * 4}b', 0], [f'{BARS * 4 + 16}b', 0]]), 'curve': 0}
        if ON['true']:                                         # v7: let go beside the cell from where the room goes to where the cell goes
            hand['points'] = hand['points'][:1] + [[f"{GOES['room'] * 4 - 1}b", -60], [f"{GOES['room'] * 4}b", 0], [f"{GOES['cell'] * 4 - 0.5}b", 0], [f"{GOES['cell'] * 4}b", -60]] + hand['points'][1:]
        for name, hz, side in STRINGS['strings']:
            me = 'str-' + name.lower()
            t = f"{1000 / hz - 225.1 / STRINGS['lp']:.3f}ms"         # a period, less the low-pass's own delay, so the loop is in tune
            doc['buses'][me] = {'pan': side, 'gain': {'value': '0dB', 'mod': [{'src': 'auto.hand', 'amount': 1}]}, 'auto': {'hand': hand}, 'fx': [f"lp cutoff={STRINGS['lp']}"],
                                'returns': [{'from': 'tick', 'gain': STRINGS['feed'], 'time': t}] + ([{'from': 'cell', 'gain': TRUE['feed'], 'time': t}] if ON['true'] else []) + [{'from': me, 'gain': db(STRINGS['back']), 'time': t}]}
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
    if ON['held']:
        doc['patches'] = {**doc['patches'], **({'wd-open': OPEN} if ON['open'] else {'wd-held': V3['wd-held']})}
        doc['tracks'].append({'name': 'held', 'patch': 'wd-open' if ON['open'] else 'wd-held', 'gain': f"{float(HELD['gain'][:-2]) + OPEN_DB:g}dB" if ON['open'] else HELD['gain'], 'pan': -0.1, 'notes': T['held'], 'fx': [under], 'sends': {'hall': '-6dB'}})
    if ON['real']:
        doc['patches'] = {**doc['patches'], 'wd-under': V3['wd-under']}
        doc['tracks'].append({'name': 'under', 'patch': 'wd-under', 'gain': REAL['gain'], 'notes': T['under'], 'fx': [under]})
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
        ap.add_argument(f'--without-{k}', action='store_true', help=f'leave out {k} (the last three off is v6, the last six v5, the last nine v4, the last twelve v3, the last eighteen v2, all twenty-four v1)')
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
                       ([(GOES['meetings'], 'the last chord, held')] if ON['held'] else []) +
                       ([(GOES['cell'] - LEAVE, 'the cell is taken back into the hand')] if ON['taken'] else []) +
                       ([(GOES['ghost'] - REAL['bars'], 'the bass is given its fundamental')] if ON['real'] else []) +
                       ([(GOES['pattern'] - LEAVE, 'the pattern slips a sixteenth a bar')] if ON['slip'] else []) +
                       ([(GOES['room'] - SING['bars'], 'the walls come in until they sing')] if ON['sing'] else []) +
                       ([(RUNS_DOWN if ON['early'] else BARS, "Ring True's strings are let go beside the click")] if ON['strings'] else []) +
                       ([(COMES['meetings'], 'the drum answers each meeting that lands on it')] if ON['knock'] else []) +
                       ([(GOES['room'], "the strings are let go beside the cell, and ring while it rings true")] if ON['true'] and ON['strings'] else []) +
                       ([(b // 4, f"all three meet on the drum: the triad turns over ({' '.join(TURNED[(b // PAGE - COMES['meetings'] * 4 // PAGE) % len(TURNED)][c] for c in CYCLES)})") for b in range(0, GOES['meetings'] * 4, PAGE) if b >= COMES['meetings'] * 4] if ON['turn'] and ON['knock'] else []) +
                       ([(GOES['change'] - 1, "the change's last seed is paid in the smallest coins: a held B flat")] if ON['paid'] else []) +
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
