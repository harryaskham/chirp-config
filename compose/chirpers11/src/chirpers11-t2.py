#!/usr/bin/env python3
"""Least Common (chirpers11, track 2). Clicky minimal techno, 126 BPM, G minor, 210 bars (6:40).

THE RULE. Three clicks keep cycles of 3, 5 and 7 sixteenths against a bass drum on every fourth. They are never
told what to do after that: everything else in the song is what happens when they MEET.
  two meet   -> a ping. 3 with 5 (every 15 sixteenths) rings D, 3 with 7 (every 21) B flat, 5 with 7 (every 35) F.
  three meet -> a chord (every 105 sixteenths: six bars and nine sixteenths).
  three meet ON THE BASS DRUM -> the song turns a page (every 420 sixteenths: 26 bars and a beat. So the pages turn
                on beat two, then beat three, then beat four).
  all meet ON THE ONE -> once in 105 bars (1680 sixteenths = 3 x 5 x 7 x 16). That is a HALF of the song.
Between two chords the pings fall on sixteenths 15 21 30 35 42 45 60 63 70 75 84 90: twelve notes, the same forwards
and backwards (gaps 15 6 9 5 7 3 15 3 7 5 9 6 15). Nobody wrote that tune. It comes round every 105 sixteenths, nine
sixteenths later in the bar each time, so it visits every sixteenth of the bar once before it is home.

THE SECOND HALF IS THE FIRST, ONE SIZE UP: cycles of 3, 5 and 7 BEATS against the bar of four. 3 x 5 x 7 x 4 beats is
105 bars again. Each long cycle is filled with the NEXT one's number, spread as evenly as it goes (Euclid): five
strokes in the three beats, seven in the five, three in the seven. Their meetings are the same tune four times
slower, so it is held, not struck: a tone that changes when two cycles begin together. From the seventh page the small
tune comes back over it (pings where cycles of 3, 5 and 7 sixteenths WOULD meet, though nobody is playing them): the
same tune at two sizes at once.

The four's own parts (bass, off-beat hat, clap) come in a page at a time and are the only things placed by page. The
chord is Give or Take's (track 1: G minor seventh) with its ninth on top, so the two songs can be laid over each other.

v2 (26 Nov): WHAT A MEETING DOES. In v1 a meeting was only a note. Six switches, each `--without-…` (all six off
is v1 byte for byte); every one is driven by the same count, how far it is to the next time all three meet:
  PLACE   the three and the five walk apart from the centre and back between two meetings of all three (the three
          to the left, the five to the right, the seven stays), so a chord is also three sounds arriving at one
          place. One size up in the second half: the walk takes a page.
  NEAR    the clicks are loudest where the three meet and NEAR dB quieter half way between.
  DOOR    a far room behind the clicks. Its door is shut when a page turns and opens a step each time the three
          meet (four steps to a page); the page turn shuts it again. In the last stretch of the first half, where the
          four stops, it is wide open: the clicks walk to the one alone in a hall. One size up in the second half:
          a step a page, wide open on the last.
  MEMORY  a click keeps the note of the last meeting it was in. The five's tock is on G after a chord, D after it
          meets the three, F after the seven; the seven's knock on G, B flat (the three), F (the five). Two tunes
          nobody wrote, in place of one note struck 400 times. Both are an octave under the pings.
  ROOTS   the bass keeps its rhythm and takes its note from the last meeting of any two (G2 after a chord, D2,
          B flat 2, F2): a bass line that the cycles write.
  BREAK   what the half does, one size down. Before each page of the first half turns, from the last time the five
          and the seven meet (35 sixteenths: two bars and three), the four stops, and the clicks walk to the page
          turn alone, the far room wide open. The page turns on the drum and the door shuts.

v3 (26 Nov): THE SPRING. The two halves were joined by a stop. Eight switches (`--without-rundown`, `-windup`,
`-through`, `-seven`, `-swing`, `-line`, `-rest`, `-wide`; all eight off is v2 byte for byte):
  RUNDOWN  the clock runs down by halves. In the last stretch of the first half (105 sixteenths, the four already
           stopped) each click loses every other stroke, and then every other one again: cycles of 3, 5 and 7
           sixteenths, then eighths, then beats. It is 3 against 5 against 7 at every size, and the size it
           reaches is the second half's, so the one arrives at the tempo the clicks have already come down to. A
           ping is as loud as the quieter of the two that meet, so the tune thins out with them.
  WINDUP   and is wound up at the end. In the last stretch of the second half the big cycles lose their fillings
           and the small cycles come back the same way backwards: every fourth stroke is already there (it is
           the head of the big cycle), then every second, then every one. The song reaches home at the size it
           began at, 3 against 5 against 7 sixteenths, so that it could begin again.
  THROUGH  the tune goes through the door as well. The pings, the chord and the held tone are sent to the far room
           (the clicks alone moved it 0.6 dB), so what a meeting makes is heard further off as the door opens.
  SEVEN    the seven was the quietest thing in the song (15 to 19 dB under the mix): 1.5 dB up.
  LINE     the bass keeps its line. In the second half it took its note from the big cycles' meetings and so held
           one note for five to nine bars: twenty slow changes that the scorer heard as twenty small sections,
           most of them alike. Now it goes on following the small cycles' meetings, as in the first half (nobody
           is playing them, but the drum's sixteenths still count them): the first half's tune stays in the bass
           under the second half's held tones, the same tune at two sizes from the one on.
  REST     the second half gets the breaks the first has, one size up: before each of its pages turns, from the
           last time the three and the five BEATS meet (60 sixteenths: three bars and three), the four stops
           and the clicks walk to the page turn alone.
  WIDE     the far room 6 dB up, so that the door is heard, and thinner (nothing under 900 Hz comes back from it).
  SWING    the door swings. It stepped open when the three met; now it opens all the way through each stretch,
           to the next step's place, so the tune moves off steadily and the page turn brings it back at once.

v4 (26 Nov): THE CLICKS GO THROUGH THE DOOR. In three rounds the door never moved the song more than 0.7 dB:
it was a room getting louder behind clicks that stayed where they were. Five switches (`--without-away`,
`-home`, `-slow`, `-push`, `-low`; all five off is v3 byte for byte):
  AWAY   the clicks walk off. As the door opens their own sound falls (AWAY dB by the last step) while what the
         far room gives back of them stays as it was: they have their own far room (`gone`), whose fader makes up
         exactly what their faders lose. The same strokes are further off each time the three meet, furthest in
         the break before the page turns, and the page turn puts them back in front of you at once. One size
         up in the second half: a step further a page. While the clock runs down they stand in front (they come
         back on the chord that begins it), so that the slowing is heard at full size.
  HOME   and they come home. Over the last stretch of the song, as the small cycles are wound back up, the clicks
         walk back from the far room to where they began, and the pings swell with them. The big cycles' fillings
         no longer fade as the small strokes come in: they stay whole to the half-way point, where the eighths
         have taken their place (v3's wind-up was 2 to 4 dB thinner above 5 kHz than what it replaced).
  SLOW   the clock runs down over two stretches, not one. In the first the four is still playing, so the clicks
         are heard to go from sixteenths to eighths AGAINST the drum; then the four stops and they go to beats
         alone. Twenty-five seconds in place of twelve.
  PUSH   on the last page of each half the off-beat hat is a sixteenth late: on the sixteenth the bass drum was
         cut short to leave empty, pushing into every beat.
  LOW    the bass 2 dB up (114 Hz stood 9.3 dB under the album's envelope).

v6 (26 Nov): THE DRUM ANSWERS. The second half's cycles of 3, 5 and 7 beats were never new: a click on a cycle of
3 sixteenths lands on the bass drum every 12 sixteenths, which is every 3 beats; the five every 5 beats; the seven
every 7. Those meetings, a click with the drum, were the only ones in the song that did nothing. One switch
(`--without-knock`; off is v5 byte for byte):
  KNOCK  from the first half's last page on, when a click lands on the drum the drum answers with a low knock (a
         small kettledrum head, new patch `lc-knock`): G for the three, B flat for the five, D for the seven. So
         under the last page of sixteenths a slow G minor triad is already turning in 3, 5 and 7 beats, two of its
         notes together every 15, 21 and 35 beats and all three exactly where the page turns; through the run-down
         it is what is left with the drum; and on the one the clicks take up those same three cycles, and the
         knock is now the head of each. It stops four bars before the end (the low end of a seam is the next
         song's). Its notes are 98 to 370 Hz, where this song stood 7 to 11 dB under the album's envelope.

v8 (26 Nov): THE SECOND HALF REMEMBERS THE FIRST. On page 6 the three clicks stood 20 to 22 dB under the mix: the
second half was a low-end piece with the clicks far behind it, on an album of clicks. Two switches
(`--without-ghost`, `-fore`; both off is v7 byte for byte):
  GHOST  in the first half the clicks count 3, 5 and 7 sixteenths; in the second, 3, 5 and 7 beats. Now in the
         second half each click has an echo, and the echo keeps its old cycle: the three's comes back every 3
         sixteenths, the five's every 5, the seven's every 7, each time half as loud, from the other side of
         the room. Nobody plays the small cycles there, and they are heard all the same, under the big ones:
         both sizes of the same three numbers at once. In the last stretch, as the small cycles are wound back
         up and played again, the echoes go.
  FORE   and the clicks are struck FORE dB harder through the second half, until that last stretch.

v7 (26 Nov): THE TRIAD TURNS OVER. The drum's answer (v6) was the same three notes in the same three cycles for
four minutes: every page of 105 beats the same low tune. Three switches (`--without-turn`, `-carry`, `-tame`; all
three off is v6 byte for byte):
  TURN   one size up again. The three notes turn in 3, 5 and 7 beats; now the triad itself turns over once in the
         second half, an inversion a page. On the one it is as it was (G2 B flat 2 D3: the three's note lowest and
         commonest); when the page turns the lowest note goes to the top (B flat 2, D3, G3), and again (D3, G3,
         B flat 3), and on the last page it is home (G2, B flat 2, D3). The note heard every three beats is
         G, then B flat, then D, then G: the song's chord, a page a note, under a song that never changed chord.
  CARRY  in the second half the four stops for fifteen beats before each page turns, and the drum's answer
         stopped with it. Now the answer goes on without the question: the knocks keep their beats through the
         break, CARRY_DB down, with the slow clicks and the held tone, and the page turns on the whole triad.
  TAME   the pings' commonest note, D5 (587 Hz), 3 dB down by an EQ on their track: 547 and 641 Hz have stood
         about 7 dB over the album's envelope since v2, and by solo the pings are half of what the song has from
         250 Hz to 1 kHz on the first half's pages.

v5 (26 Nov): ONLY THE DRUM. Read by solo, v4's slow run-down was a change of rhythm 14 to 19 dB under the four,
and the second half's four pages all stood at one level. Three switches (`--without-bare`, `-small`, `-rise`;
all three off is v4 byte for byte):
  BARE   as the clock begins to run down only the drum is left of the four (as it is in the last stretch of the
         song): the bass, the hat and the clap stop a stretch before the drum does, and the clicks stand at full
         height through the run-down (no ride down between meetings). So the first half of the run-down is three
         clicks going from sixteenths to eighths against a drum and nothing else.
  SMALL  the second half begins as the first did. The first half's first page has no bass (three clicks and a
         drum); one size up, the second half's first page has none either: three slow clicks, the held tones
         and the drum. The bass comes back with the page turn, and the clap with it.
  RISE   the wind-up's sixteenths come in from 12 dB down, not 24 (its third quarter stood 3.6 dB under the page
         before it above 5 kHz).
A fourth was tried and dropped: the drum's body moved from 130 Hz to 110 (114 Hz stands 8.7 dB under the album's
envelope). Read on a page where nothing else had changed it moved 105 to 123 Hz by 0.2 dB: the drum has nothing there.

Form as arithmetic: everything below is computed from CYCLES, BAR and BEAT. Nothing is typed as a bar number.
"""
import argparse
import json
from math import lcm, log10
from pathlib import Path

BPM = 126
BEAT, BAR = 4, 16                       # sixteenths
CYCLES = (3, 5, 7)                      # the three clicks, sixteenths (first half) or beats (second half)
VOICES = ('three', 'five', 'seven')
SUPER = lcm(*CYCLES)                    # 105: the three meet
PAGE = lcm(SUPER, BEAT)                 # 420: the three meet on the bass drum
HALF = lcm(SUPER, BAR)                  # 1680: all meet on the one (105 bars)
TOTAL = 2 * HALF
assert (SUPER, PAGE, HALF) == (105, 420, 1680) and HALF % BAR == 0 and PAGE // BEAT % 4 == 1
KEY = 'G'
PING = {(3, 5): 'D5', (3, 7): 'Bb4', (5, 7): 'F4'}          # the commonest meeting gets the plainest note
TONE = {(3, 5): 'D4', (3, 7): 'Bb3', (5, 7): 'F3'}           # the same three notes an octave down, held
CHORD = ('G3', 'Bb3', 'D4', 'F4', 'A4')
OUT = Path(__file__).resolve().parents[3] / 'songs/chirpers11-t2.yaml'

# ---- v2: the switches and their numbers. Nothing above is changed by them.
ON = {'place': True, 'near': True, 'door': True, 'memory': True, 'roots': True, 'break': True,
      'rundown': True, 'windup': True, 'through': True, 'seven': True, 'swing': True, 'line': True, 'rest': True, 'wide': True,
      'away': True, 'home': True, 'slow': True, 'push': True, 'low': True,
      'bare': True, 'small': True, 'rise': True, 'knock': True, 'turn': True, 'carry': True, 'tame': True, 'ghost': True, 'fore': True}
GHOST = {'feed': '-4dB', 'back': 0.5, 'hp': 300, 'side': {'three': 0.5, 'five': -0.5, 'seven': 0.0}}   # v8: what each click's echo takes of it, what it gives back of itself each pass, its high-pass, where it stands (the three walks left and the five right)
FORE = 4                                # v8: dB on the three clicks through the second half
# Bench, page 6's first sixteen bars, each click alone, by sixteenth (ghost.sh, ghostread.py). The three (struck on sixteenths 1 3 5 8 10 of twelve) read -36 -58 -38 -59 -36 -57 -65 -40 -63 -40 -61 -72 in v7; with its echo
# taking -6 dB of it: -36 -53 -38 -44 -36 -46 -52 -39 -53 -40 -47 -61: new strokes on 4, 6 and 11, 8 to 10 dB under the played ones, and a second echo on 7. The five's stood 10 under, the seven's 7 (it is in the middle: a bus
# to one side loses more). So -4 dB. With the clicks 3 dB harder they stood 20.9, 18.7 and 21.2 dB under the mix (v7 24.4, 22.1, 24.8) and 7.8, 7.3 and 8.8 above 300 Hz (10.1, 9.5, 11.1): so 4
TURNED = ({3: 'G2', 5: 'Bb2', 7: 'D3'}, {3: 'Bb2', 5: 'D3', 7: 'G3'}, {3: 'D3', 5: 'G3', 7: 'Bb3'})   # v7: the triad's three positions, by how many pages of the second half have turned (the fourth is the first again)
TURN_DB = (0, -1, -2)                   # v7: on the knock in each position. Bench, by solo: at one level the second inversion stood 2.7 dB under the mix from 200 to 400 Hz (v6's root position 7.5) and the first 4.6 (7.8): the head is the same size and its notes are higher
CARRY_DB = -6                           # v7: on a knock where the four has stopped. Bench, the break before page 6: with them the break reads -32.1 dB raw for -35.4 (under 250 Hz -34.5 for -43.0) and the groove before it -24.3: still a break, 8 dB down, with a low tune in it
TAME = 'peak cutoff=587 q=3 gain=-3dB'  # v7: on the pings. At q 1.4 it took 2.1 to 3.0 dB off everything from 400 Hz to 1 kHz (2.3 dB off the pings as a whole): a fader, not a note
KNOCK = {3: 'G2', 5: 'Bb2', 7: 'D3'}    # v6: the drum's answer to each click that lands on it
KNOCK_FROM = HALF - PAGE                # from the first half's last page
KNOCK_SEAM = 4 * BAR                    # and not in the last four bars
KNOCK_DB, KNOCK_HOLD = '-2dB', -10     # its fader, and the clip before it. Bench, alone on page 4: at 180 ms the head was a spike (-9.6 dBFS highest sample, 21 dB gone in 50 ms) carrying 13 dB less from 90 to 400 Hz than the bass or the drum. So it rings longer, the spike is clipped off, and the fader brings up what is left: at -4 dB it read 7 to 9 dB under the mix from 90 to 400 Hz and 4.4 under the bass; at -2 see the round's note
LC_KNOCK = {'about': "Least Common: the drum's answer when a click lands on it (v6). A small kettledrum head (modes 1 : 1.5 : 2 : 2.5, so on G2, B flat 2 and D3 everything it has is between 98 and 370 Hz), let ring 800 ms.",
            'synth': {'layers': [{'type': 'modal', 'modes': 'kettle', 'decay': '800ms', 'bright': 0.3, 'strike': 0.3}], 'amp': {'a': '0.5ms', 'd': '0s', 's': 1, 'r': '600ms'}},
            'play': {'event_stable': True, 'vel_sens': 0.4}}
RISE = -12                              # v5: dB the wind-up's strokes come in at
AWAY = 9                                # v4: dB the clicks' own sound has fallen when the door is wide open (their far room makes it up)
SWELL = 3                               # v4 HOME: dB the pings have risen by the end of the last stretch
LOW_DB = 2                              # v4 LOW: on the bass's fader
FLOOR = -24                             # dB a stroke has fallen to when it goes (RUNDOWN), or comes in at (WINDUP)
THROUGH = '-6dB'                        # the tune's send to the far room
THROUGH_DRY = -1.5                      # dB on the pings' own fader with it (547 Hz was 7.8 dB over the envelope already)
SEVEN_DB = 1.5                          # (2.5 put 641 Hz 9 dB over the envelope)
ALL = tuple(CYCLES)
WIDE = 0.8                              # how far from the centre a click stands when it is furthest from a meeting of all three
NEAR = 5                                # dB quieter there
LIFT = 2                                # dB on the clicks' faders with NEAR on (the ride takes 2.5 dB off on average)
DOOR = (-60, -12, -6, 0)                # the far room's fader, by how many times the three have met since the page turned
FAR = '-3dB'                            # each click's send to the far room
# The notes are the pings' own (D, B flat, F; G for the chord), each click an octave under the pings (the tock on the
# pings' own octave stacked with them, 13 dB over the envelope at 547 Hz; an octave over them, 12 over at 1.2 kHz).
MEMORY = {'five': {(3, 5): 'D4', (5, 7): 'F4', ALL: 'G4'}, 'seven': {(3, 7): 'Bb3', (5, 7): 'F3', ALL: 'G3'}}
ROOT = {(3, 5): 'D2', (3, 7): 'Bb2', (5, 7): 'F2', ALL: 'G2'}
ROOTS_DB = -3                           # the bass's fader with ROOTS on, beside v1's (this patch is 14 dB louder than the sine it replaces)
LC_ROOT = {'about': 'Least Common: the bass once the meetings write its line (v2). A sine and its octave, so that a line on 73 to 117 Hz is also heard on 147 to 233.',
           'synth': {'layers': [{'wave': 'sine'}, {'wave': 'sine', 'semi': 12, 'level': '-6dB'}], 'amp': {'a': '4ms', 'd': '0s', 's': 1, 'r': '60ms'}},
           'play': {'event_stable': True, 'vel_sens': 0.3}}
BREAK = lcm(*CYCLES[1:])                # 35: the last meeting of the five and the seven before a page turns
TURNS = [p * PAGE for p in range(1, HALF // PAGE)]   # the page turns of the first half (the half itself has its own, v1's)
REST = lcm(*CYCLES[:2]) * BEAT          # 60: v3, the second half's break. The last meeting of the three and the five BEATS before a page turns (3 bars and 3)
TURNS2 = [HALF + t for t in TURNS]      # the page turns of the second half
WIDE_DB = 6                             # v3: the far room's own fader (at 0 dB it added 0.6 dB to the clicks alone)
WIDE_HP = 900                           # and its high-pass with it (at 500 the wider room put 547 and 641 Hz 9 dB over the envelope and the low end 2 dB down beside them)


def broken(s):
    """Is sixteenth s in a break (the four stopped before a page turn)?"""
    return (ON['break'] and any(t - BREAK <= s < t for t in TURNS)) or (ON['rest'] and any(t - REST <= s < t for t in TURNS2))

TOCK = {'about': 'Least Common: the click that counts five, once it has a tune (v2). The same wooden bar damped twice as fast, so that a note it keeps for twenty strokes is a colour and not a drone.',
        'synth': {'layers': [{'type': 'modal', 'modes': 'bar', 'decay': '28ms', 'bright': 0.8, 'damp': 0.4, 'strike': 0.4}],
                  'amp': {'a': '0.2ms', 'd': '45ms', 's': 0, 'r': '20ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.7}}
TOCK_DB = 0                            # the five's fader with MEMORY on, beside v1's


def order(c, s):
    """2 where the cycle of c beats begins, 1 where the cycle of c eighths does, 0 on its other sixteenth strokes."""
    return 2 if s % (4 * c) == 0 else 1 if s % (2 * c) == 0 else 0


def rundown(c, s):
    """dB on the stroke of cycle c at sixteenth s in the last stretch of the first half (None: not played). The
    strokes of order 0 fall to FLOOR over the first half of the stretch and go; those of order 1 over the second."""
    w = SUPER * (2 if ON['slow'] else 1)                     # v4 SLOW: over two stretches, the first with the four still in
    if not ON['rundown'] or not HALF - w <= s < HALF or order(c, s) == 2:
        return 0
    x = (s - (HALF - w)) / w * 2 - (order(c, s) == 1)
    return None if x >= 1 else round(FLOOR * max(x, 0), 1)


def windup(c, s):
    """The same backwards in the last stretch of the second half: dB on a small-cycle stroke that the big cycle
    does not already play (None: not played). Order 1 comes up over the first half of the stretch, order 0 over the second."""
    if not ON['windup'] or not TOTAL - SUPER <= s < TOTAL or s % c:
        return None
    x = (s - (TOTAL - SUPER)) / SUPER * 2 - (order(c, s) == 0)
    return None if x < 0 else round((RISE if ON['rise'] else FLOOR) * (1 - min(x, 1)), 1)


def stretches():
    """(start, length, which step of four) in sixteenths, for every stretch between two meetings of all three: sixteen
    of 105 sixteenths in the first half (four to a page), four of 105 beats (a page each) in the second."""
    return ([(s, SUPER, s % PAGE // SUPER) for s in range(0, HALF, SUPER)] +
            [(s, PAGE, (s - HALF) // PAGE) for s in range(HALF, TOTAL, PAGE)])


def beats(s16):
    return ('%.4f' % (s16 / BEAT)).rstrip('0').rstrip('.') + 'b'


def running_down(s):
    """Is sixteenth s in the run-down (the last stretch of the first half; with SLOW the last two)?"""
    return ON['rundown'] and HALF - SUPER * (2 if ON['slow'] else 1) <= s < HALF


def bare(s):
    """v5: do the bass, the hat and the clap rest at sixteenth s? From where the clock begins to run down to the one
    (the drum goes on for the first of the two stretches; v1 let the bar that straddles its stopping play out)."""
    return ON['bare'] and ON['slow'] and running_down(s)


def walk(far, stand=False):
    """A lane that is 0 where the three meet and `far` half way to the next meeting, straight lines between. With
    `stand` (v5 BARE, the clicks' level) it stays at 0 through the run-down."""
    pts = []
    for s, n, _ in stretches():
        pts += [[beats(s), 0], [beats(s + n / 2), 0 if stand and ON['bare'] and running_down(s) else far]]
    return {'points': pts + [[beats(TOTAL), 0]], 'curve': 0}


def door():
    """The far room's fader: DOOR[k] through the k-th stretch since the page turned, stepping within a sixteenth."""
    pts = []
    for s, n, k in stretches():
        pts += [[beats(s), DOOR[k]], [beats(s + n - 1), DOOR[min(k + 1, len(DOOR) - 1) if ON['swing'] else k]]]
    return {'points': pts + [[beats(TOTAL), DOOR[-1]], [beats(TOTAL + BAR), DOOR[-1]]], 'curve': 0}

def away():
    """v4: dB on the clicks' own sound. 0 when a page turns and -AWAY when the door is wide open, moving as the door
    moves. With HOME it comes back to 0 over the last stretch of the song."""
    top, pts = len(DOOR) - 1, []
    w = SUPER * (2 if ON['slow'] else 1) * ON['rundown']     # while the clock runs down they stand in front
    for s, n, k in stretches():
        here = HALF - w <= s < HALF
        pts += [[beats(s), 0 if here else -AWAY * k / top], [beats(s + n - 1), 0 if here else -AWAY * (min(k + 1, top) if ON['swing'] else k) / top]]
    end = -AWAY
    if ON['home']:
        pts, end = [q for q in pts if float(q[0][:-1]) * BEAT < TOTAL - SUPER] + [[beats(TOTAL - SUPER), -AWAY]], 0
    return {'points': pts + [[beats(TOTAL), end], [beats(TOTAL + BAR), end]], 'curve': 0}


def at(lane, b):
    """A lane's value at beat b (straight lines between its points)."""
    pts = [(float(q[0][:-1]), q[1]) for q in lane['points']]
    for (b0, v0), (b1, v1) in zip(pts, pts[1:]):
        if b0 <= b <= b1:
            return v0 if b1 == b0 else v0 + (v1 - v0) * (b - b0) / (b1 - b0)
    return pts[-1][1] if b > pts[-1][0] else pts[0][1]


def gone():
    """v4: the fader of the clicks' own far room: the door's, plus what the clicks' faders have lost, at every point of either lane."""
    d, a = door(), away()
    bs = sorted({float(q[0][:-1]) for q in d['points'] + a['points']})
    return {'points': [[('%.4f' % b).rstrip('0').rstrip('.') + 'b', round(at(d, b) - at(a, b), 3)] for b in bs], 'curve': 0}


PATCHES = {
    'lc-kick': {'about': "Least Common: the four. The drum machine's bass drum resting on G, short enough to leave the sixteenth before the next beat empty.",
                'synth': {'layers': [{'type': 'machine', 'machine': {'part': 'kick', 'decay': '240ms', 'click': 0.55, 'drive': 0.2, 'punch': 20}}],
                          'amp': {'a': '0.1ms', 'd': '0s', 's': 1, 'r': '400ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.3}},
    'lc-three': {'about': 'Least Common: the click that counts three. Ten milliseconds of noise above 5 kHz: a tick with no note.',
                 'synth': {'layers': [{'type': 'noise', 'color': 'white'}], 'filters': ['hp cutoff=5000', 'peak cutoff=8500 q=2 gain=8dB'],
                           'amp': {'a': '0.1ms', 'd': '10ms', 's': 0, 'r': '8ms', 'curve': 3}}, 'play': {'event_stable': True, 'vel_sens': 0.7}},
    'lc-five': {'about': 'Least Common: the click that counts five. A small wooden bar (1 : 4 : 10) struck hard and damped at once: a tock on G.',
                'synth': {'layers': [{'type': 'modal', 'modes': 'bar', 'decay': '55ms', 'bright': 0.8, 'damp': 0.4, 'strike': 0.4}],
                          'amp': {'a': '0.2ms', 'd': '80ms', 's': 0, 'r': '30ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.7}},
    'lc-seven': {'about': "Least Common: the click that counts seven. The drum machine's rim, tuned to G: two short pings and a click, a knock.",
                 'synth': {'layers': [{'type': 'machine', 'machine': {'part': 'rim', 'decay': '45ms'}}],
                           'amp': {'a': '0.1ms', 'd': '0s', 's': 1, 'r': '120ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.7}},
    'lc-ping': {'about': 'Least Common: what two clicks make when they meet. A vibraphone bar with no motor, half a second long.',
                'synth': {'layers': [{'type': 'modal', 'modes': 'vibes', 'decay': '650ms', 'bright': 0.55, 'strike': 0.3}],
                          'amp': {'a': '0.3ms', 'd': '900ms', 's': 0, 'r': '200ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.5}},
    'lc-chord': {'about': 'Least Common: what three clicks make when they meet. A short filtered chord for a delay to carry.',
                 'synth': {'layers': [{'wave': 'saw', 'detune': -7}, {'wave': 'saw', 'detune': 7}, {'wave': 'pulse', 'level': '-8dB'}],
                           'filters': [{'kind': 'lp', 'cutoff': {'value': 500, 'mod': [{'src': 'env.f', 'amount': 2.6}]}, 'q': 1.4}],
                           'env': {'f': {'a': '1ms', 'd': '140ms', 's': 0, 'r': '80ms'}},
                           'amp': {'a': '1ms', 'd': '220ms', 's': 0, 'r': '90ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.4}},
    'lc-tone': {'about': 'Least Common: the meetings one size up. A plain held tone, a sine and a little of its octave, that takes a beat to arrive.',
                'synth': {'layers': [{'wave': 'sine'}, {'wave': 'triangle', 'semi': 12, 'level': '-16dB'}],
                          'amp': {'a': '240ms', 'd': '0s', 's': 1, 'r': '900ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.2}},
    'lc-hat': {'about': "Least Common: the off beat. The drum machine's hat, closed.",
               'synth': {'layers': [{'type': 'machine', 'machine': {'part': 'hat', 'decay': '45ms'}}],
                         'amp': {'a': '0.1ms', 'd': '0s', 's': 1, 'r': '120ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.6}},
    'lc-clap': {'about': "Least Common: two and four. The drum machine's clap, short.",
                'synth': {'layers': [{'type': 'machine', 'machine': {'part': 'clap', 'decay': '140ms', 'bursts': 3}}],
                          'amp': {'a': '0.1ms', 'd': '0s', 's': 1, 'r': '300ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.5}},
}


def euclid(k, n):
    """k strokes spread over n steps as evenly as they go, the first on the first step."""
    return [i * n // k for i in range(k)]


def touch(pos):
    """How hard a click lands: hardest where it catches the bass drum, lighter on the off beat, lightest between."""
    return .92 if pos % BEAT == 0 else .74 if pos % BEAT == 2 else .58


def build():
    T = {n: [] for n in ('kick', 'three', 'five', 'seven', 'ping', 'chord', 'tone', 'bass', 'hat', 'clap')}
    marks = []

    def add(tr, s16, len16, pitch, vel, **more):
        T[tr].append({'at': round(s16 / BEAT, 4), 'len': round(len16 / BEAT, 4), 'pitch': pitch, 'vel': round(vel, 3), **more})

    if ON['knock']:
        T['knock'] = []

    def knock(s, db=0):
        """v6: the drum's answer at sixteenth s, a note for each click whose cycle lands on it (every 3, 5 and 7 beats)."""
        if ON['knock'] and KNOCK_FROM <= s < TOTAL - KNOCK_SEAM:
            notes = TURNED[(s - HALF) // PAGE % len(TURNED)] if ON['turn'] and s >= HALF else KNOCK
            for c in CYCLES:
                if s % (c * BEAT) == 0:
                    g = db + (TURN_DB[(s - HALF) // PAGE % len(TURNED)] if ON['turn'] and s >= HALF else 0)
                    add('knock', s, 2, notes[c], .85, **({'gain': f'{g}dB'} if g else {}))

    pitch = {'three': 'C6', 'five': 'G5', 'seven': 'G4'}
    mem = dict(pitch)
    roots = []                                                # the note of the last meeting of any two, at every sixteenth
    # ---- the first half: cycles of 3, 5 and 7 sixteenths. Who is in, by supercycle (the three meet at each one's head).
    supers = HALF // SUPER                                    # 16
    pages = HALF // PAGE                                      # 4
    per_page = PAGE // SUPER                                  # 4
    enters = {'three': 0, 'five': 1, 'seven': 2}              # one more click each time the three would have met
    last = supers - 1                                         # the last supercycle of the half: the four stops, to come back on the one
    for s in range(0, HALF):
        n = s // SUPER
        here = [c for c, v in zip(CYCLES, VOICES) if s % c == 0 and (n >= enters[v] or s == 0)]
        if ON['memory'] and len(here) >= 2:                   # a click keeps the note of the last meeting it was in
            for c, v in zip(CYCLES, VOICES):
                if c in here and v in MEMORY:
                    mem[v] = MEMORY[v][tuple(here)]
        loud = {c: rundown(c, s) for c in here}               # v3: 0 dB everywhere but in the last stretch
        for c, v in zip(CYCLES, VOICES):
            if c in here and loud[c] is not None:
                add(v, s, 1, mem[v], touch(s), **({'gain': f'{loud[c]}dB'} if loud[c] else {}))
        met = tuple(c for c in CYCLES if s % c == 0)
        roots.append(ROOT[met] if len(met) >= 2 else roots[-1])
        if len(here) == 2 and None not in loud.values():     # a meeting is as loud as the quieter of the two
            add('ping', s, 4, PING[tuple(here)], .8, **({'gain': f'{min(loud.values())}dB'} if min(loud.values()) else {}))
        if len(here) == 3:
            add('chord', s, 2, ','.join(CHORD), .85 if s % BEAT == 0 else .7)
        if s % BEAT == 0 and n != last and not broken(s):
            add('kick', s, 2, 'G1', .95 if s % BAR == 0 else .88)
            knock(s)
    marks += [('first half: three, five and seven sixteenths', 0)] + [(f'page {p + 1} (the three meet on beat {p * PAGE // BEAT % 4 + 1})', p * PAGE) for p in range(1, pages)]
    marks += [('the clock begins to run down, ' + ('only the drum left of the four' if ON['bare'] else 'the four still playing'), (last - 1) * SUPER)] * (ON['slow'] and ON['rundown']) + [('the four stops', last * SUPER)]
    # ---- the second half: one size up. Cycles of 3, 5 and 7 beats, each filled with the next one's number.
    fill = {c: euclid(CYCLES[(i + 1) % 3], c * BEAT) for i, c in enumerate(CYCLES)}
    assert [len(fill[c]) for c in CYCLES] == [5, 7, 3]
    held = []                                                  # (sixteenth, the cycles that begin together)
    for s in range(HALF, TOTAL):
        r = s - HALF
        heads = [c for c in CYCLES if r % (c * BEAT) == 0]
        small = tuple(c for c in CYCLES if r % c == 0)       # v3 LINE: the bass keeps the small cycles' meetings
        roots.append((ROOT[small] if len(small) >= 2 else roots[-1]) if ON['line'] else ROOT[tuple(heads)] if len(heads) >= 2 else roots[-1])
        if ON['memory'] and len(heads) >= 2:
            for c, v in zip(CYCLES, VOICES):
                if c in heads and v in MEMORY:
                    mem[v] = MEMORY[v][tuple(heads)]
        for c, v in zip(CYCLES, VOICES):
            filled = r % (c * BEAT) in fill[c]
            if ON['windup'] and s >= TOTAL - SUPER and r % (c * BEAT):       # v3: the fillings go, the small cycles come back
                going = (s - (TOTAL - SUPER)) / SUPER * 2
                both = [g for g in ((0.0 if ON['home'] else round(FLOOR * going, 1)) if filled and going < 1 else None, windup(c, s)) if g is not None]
                if both:
                    add(v, s, 1, mem[v], touch(s), **({'gain': f'{max(both)}dB'} if max(both) else {}))
            elif filled:
                add(v, s, 1, mem[v], touch(s) if r % (c * BEAT) else .95)
        if len(heads) >= 2:
            held.append((s, tuple(heads)))
        if s % BEAT == 0 and not broken(s):
            add('kick', s, 2, 'G1', .95 if s % BAR == 0 else .88)
            knock(s)
        elif s % BEAT == 0 and ON['carry']:                  # v7: the answer goes on through the break
            knock(s, CARRY_DB)
    held.append((TOTAL, tuple(CYCLES)))
    for (s, heads), (nxt, _) in zip(held, held[1:]):
        if len(heads) == 3:
            add('chord', s, 2, ','.join(CHORD), .85)
            continue                                           # after a chord the tone rests until the next two meet
        add('tone', s, nxt - s - 2, TONE[heads], .7)
    # the same tune at both sizes: from the seventh page the pings come back over the held tones, at the small
    # cycles' own places (three, five and seven sixteenths counted from the top of the half, nobody playing them)
    for s in range(HALF + 2 * PAGE, TOTAL):
        small = tuple(c for c in CYCLES if (s - HALF) % c == 0)
        if len(small) == 2:
            up = round(SWELL * (s - (TOTAL - SUPER)) / SUPER, 1) if ON['home'] and s >= TOTAL - SUPER else 0
            add('ping', s, 4, PING[small], .62, **({'gain': f'{up}dB'} if up else {}))
    # home: everything meets on the one, and that is the end
    add('chord', TOTAL, 8, ','.join(CHORD), .9)
    add('kick', TOTAL, 2, 'G1', .95)
    for v in VOICES:
        add(v, TOTAL, 1, MEMORY[v][ALL] if ON['memory'] and v in MEMORY else pitch[v], .95)
    marks += [('the drum answers each click that lands on it: a knock every 3, 5 and 7 beats', KNOCK_FROM)] * ON['knock']
    marks += [('second half: three, five and seven beats', HALF)] + [(f'page {p + 5} (the three meet on beat {p * PAGE // BEAT % 4 + 1})', HALF + p * PAGE) for p in range(1, pages)]
    marks += [(f"the triad turns over: {' '.join(TURNED[p % len(TURNED)][c] for c in CYCLES)}", HALF + p * PAGE) for p in range(1, pages)] * (ON['turn'] and ON['knock'])
    marks += [("each click's echo keeps its old cycle: 3, 5 and 7 sixteenths under 3, 5 and 7 beats", HALF)] * ON['ghost'] + [(f'the clicks are struck {FORE} dB harder', HALF)] * ON['fore']
    marks += [('only the drum is left of the four', HALF + last * SUPER), ('home', TOTAL)]
    if ON['break']:
        marks = sorted(marks + [('the four stops for the page turn', t - BREAK) for t in TURNS], key=lambda m: m[1])
    if ON['rest']:
        marks = sorted(marks + [('the four stops for the page turn', t - REST) for t in TURNS2], key=lambda m: m[1])
    # ---- the four's own parts: a bass that never plays with the drum, an off-beat hat, a clap on two and four.
    # Pages (from 0): the bass from page 1; the hat on pages 2, 3 and 6, 7; the clap on page 3 and pages 5, 6, 7.
    # In the last supercycle of the first half the four stops (the drum too) and comes back on the one; in the last
    # supercycle of the second half only the four is left of its parts (the drum), under the clicks, to the end.
    cell = ((2, 1.5, 'G2'), (7, 1, 'G2'), (10, 1, 'Bb2'), (14, 1.5, 'G2'))
    for s0 in range(0, TOTAL, BAR):
        page = s0 // PAGE
        if last * SUPER <= s0 < HALF or s0 >= HALF + last * SUPER:
            continue
        if page >= 1 and not (ON['small'] and page == pages):   # v5 SMALL: the second half's first page has no bass, as the first half's has none
            for off, ln, p in cell:
                if not broken(s0 + off) and not bare(s0 + off):
                    add('bass', s0 + off, ln, roots[s0 + off] if ON['roots'] else p, .85)
        if page in (2, 3, 6, 7):
            late = 1 if ON['push'] and page % pages == pages - 1 else 0       # v4: the last page of a half, a sixteenth late
            for off in (2, 6, 10, 14):
                if not broken(s0 + off + late) and not bare(s0 + off + late):
                    add('hat', s0 + off + late, 1, 'A#4', .7)
        if page in (3, 5, 6, 7):
            for off in (4, 12):
                if not broken(s0 + off) and not bare(s0 + off):
                    add('clap', s0 + off, 1, 'C4', .7)
    return T, marks


def song():
    T, marks = build()
    def track(name, patch, gain, pan=0, **more):
        return {'name': name, 'patch': patch, 'gain': gain, 'pan': pan, 'notes': sorted(T[name], key=lambda n: n['at']), **more}
    echo = lambda n, mix, fb: {'type': 'delay', 'time': f'{n}/16', 'mix': mix, 'feedback': fb, 'tone': 2600}
    under = {'type': 'pump', 'on': 'kick', 'depth': '-5dB', 'release': '170ms'}
    hold = lambda db: f'clip drive=0dB ceiling={db}dB'          # a click's level is its own, not the limiter's
    doc = {
        'about': "Chirpers, album eleven, track 2: Least Common, by chirper-one. Generated by compose/chirpers11/src/chirpers11-t2.py (its docstring is the rule). Three clicks on cycles of 3, 5 and 7 sixteenths against a bass drum on every fourth; a ping where two meet, a chord where three meet, a new page where three meet on the drum, and all of it on the one once in 105 bars. The second half is the first, one size up.",
        'meta': {'artist': 'chirpers', 'album': 'Escapement', 'title': 'Least Common', 'track': 2, 'year': 2026},
        'tempo': BPM, 'seed': 1, 'event_stable': True, 'length': f'{(TOTAL + BAR) // BEAT}b', 'tail': '3s', 'ceiling': '-1dB', 'true_peak': True, 'loudness': -13,
        'patches': PATCHES,
        'buses': {'room': {'fx': ['reverb kind=room decay=0.5s mix=1 predelay=8ms', 'hp cutoff=400']},
                  'hall': {'fx': ['reverb kind=hall decay=3.2s mix=1 predelay=25ms', 'hp cutoff=350', 'lp cutoff=6000']}},
        'master': {'fx': [{'type': 'eq', 'bands': ['hp cutoff=28']}]},
        'tracks': [
            track('kick', 'lc-kick', '-6dB', fx=[{'type': 'eq', 'bands': ['peak cutoff=47 q=1.2 gain=-3dB', 'peak cutoff=130 q=0.9 gain=3dB']}]),
            track('bass', 'sub-sine', '-11dB', fx=[under]),
            track('three', 'lc-three', '-3dB', pan=-0.45, fx=[hold(-12)], sends={'room': '-14dB'}),
            track('five', 'lc-five', '0dB', pan=0.45, fx=[hold(-14)], sends={'room': '-12dB'}),
            track('seven', 'lc-seven', '-1dB', pan=0.0, fx=[hold(-14)], sends={'room': '-12dB'}),
            track('ping', 'lc-ping', '-10.5dB', pan=0.15, fx=[echo(3, 0.3, 0.45)], sends={'hall': '-10dB'}),
            track('chord', 'lc-chord', '-6dB', pan=-0.1, fx=[hold(-6), echo(3, 0.45, 0.6), under], sends={'hall': '-8dB'}),
            track('tone', 'lc-tone', '-28dB', pan=0.1, fx=[under], sends={'hall': '-6dB'}),
            track('hat', 'lc-hat', '6dB', pan=0.2, sends={'room': '-16dB'}),
            track('clap', 'lc-clap', '-6dB', pan=-0.05, sends={'room': '-10dB'}),
        ]}
    by_name = {t['name']: t for t in doc['tracks']}
    side = {'three': -1, 'five': 1, 'seven': 0}
    if ON['roots']:
        doc['patches'] = {**doc['patches'], 'lc-root': LC_ROOT}
        by_name['bass'].update(patch='lc-root', gain=f"{float(by_name['bass']['gain'][:-2]) + ROOTS_DB:g}dB")
    if ON['low']:
        by_name['bass']['gain'] = f"{float(by_name['bass']['gain'][:-2]) + LOW_DB:g}dB"
    if ON['memory']:
        doc['patches'] = {**doc['patches'], 'lc-tock': TOCK}
        by_name['five'].update(patch='lc-tock', gain=f"{float(by_name['five']['gain'][:-2]) + TOCK_DB:g}dB")
    if ON['seven']:
        by_name['seven']['gain'] = f"{float(by_name['seven']['gain'][:-2]) + SEVEN_DB:g}dB"
    if ON['through'] and ON['door']:
        for name in ('ping', 'chord', 'tone'):
            by_name[name]['sends'] = {**by_name[name]['sends'], 'far': THROUGH}
        by_name['ping']['gain'] = f"{float(by_name['ping']['gain'][:-2]) + THROUGH_DRY:g}dB"
    for v in VOICES:
        t = by_name[v]
        if ON['place'] and side[v]:
            t['pan'] = {'value': 0, 'mod': [{'src': 'auto.place', 'amount': 1}]}
            t.setdefault('auto', {})['place'] = walk(side[v] * WIDE)
        if ON['near']:
            t['gain'] = {'value': f"{float(t['gain'][:-2]) + LIFT:g}dB", 'mod': [{'src': 'auto.near', 'amount': 1}]}
            t.setdefault('auto', {})['near'] = walk(-NEAR, stand=True)
        if ON['door']:
            t['sends'] = {**t['sends'], 'gone' if ON['away'] else 'far': FAR}
        if ON['door'] and ON['away']:
            g = t['gain'] if isinstance(t['gain'], dict) else {'value': t['gain'], 'mod': []}
            t['gain'] = {'value': g['value'], 'mod': g['mod'] + [{'src': 'auto.away', 'amount': 1}]}
            t.setdefault('auto', {})['away'] = away()
    if ON['door']:
        doc['buses'] = {**doc['buses'], 'far': {'fx': ['reverb kind=hall decay=2.6s mix=1 predelay=30ms', f"hp cutoff={WIDE_HP if ON['wide'] else 500}", 'lp cutoff=8000'],
                                                'gain': {'value': f"{WIDE_DB if ON['wide'] else 0}dB", 'mod': [{'src': 'auto.door', 'amount': 1}]}, 'auto': {'door': door()}}}
        if ON['away']:                                        # the clicks' own far room: the same room, its fader making up what theirs lose
            doc['buses']['gone'] = {**doc['buses']['far'], 'auto': {'door': gone()}}
    if ON['tame']:
        by_name['ping']['fx'] = [{'type': 'eq', 'bands': [TAME]}] + by_name['ping']['fx']
    span = lambda v: {'points': [['0b', v[0]], [beats(HALF - 1), v[0]], [beats(HALF), v[1]], [beats(TOTAL - SUPER), v[1]], [beats(TOTAL), v[0]], [beats(TOTAL + BAR), v[0]]], 'curve': 0}   # a lane for the second half, going back over its last stretch
    if ON['fore']:                                            # v8: struck harder through the second half
        for v in VOICES:
            g = by_name[v]['gain'] if isinstance(by_name[v]['gain'], dict) else {'value': by_name[v]['gain'], 'mod': []}
            by_name[v]['gain'] = {'value': g['value'], 'mod': g['mod'] + [{'src': 'auto.fore', 'amount': 1}]}
            by_name[v].setdefault('auto', {})['fore'] = span((0, FORE))
    if ON['ghost']:                                           # v8: each click's echo keeps its first-half cycle
        for c, v in zip(CYCLES, VOICES):
            t = f'{c * 60000 / BPM / BEAT:.2f}ms'
            doc['buses'] = {**doc['buses'], f'ghost-{v}': {'pan': GHOST['side'][v], 'gain': {'value': '0dB', 'mod': [{'src': 'auto.ghost', 'amount': 1}]}, 'auto': {'ghost': span((-60, 0))}, 'fx': [f"hp cutoff={GHOST['hp']}"],
                                                           'returns': [{'from': v, 'gain': GHOST['feed'], 'time': t}, {'from': f'ghost-{v}', 'gain': f"{20 * log10(GHOST['back']):.2f}dB", 'time': t}]}}
    if ON['knock']:
        doc['patches'] = {**doc['patches'], 'lc-knock': LC_KNOCK}
        doc['tracks'].append(track('knock', 'lc-knock', KNOCK_DB, fx=[hold(KNOCK_HOLD)]))
    return doc, marks


def dump(doc):
    lines = []
    for k, v in doc.items():
        if k == 'tracks':
            lines.append('tracks:')
            lines += ['  - ' + json.dumps(t) for t in v]
        else:
            lines.append(f'{k}: {json.dumps(v)}')
    return '\n'.join(lines) + '\n'


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--out', type=Path, default=OUT)
    ap.add_argument('--form', action='store_true', help='print the form and stop')
    for k in ON:
        ap.add_argument(f'--without-{k}', action='store_true', help=f'leave out {k} (the last two off is v7, the last five v6, the last six v5, the last nine v4, the last fourteen v3, the last twenty-two v2, all twenty-eight v1)')
    a = ap.parse_args()
    for k in ON:
        ON[k] = not getattr(a, f'without_{k}')
    doc, marks = song()
    if a.form:
        sec = 60 / BPM / BEAT
        for name, s in marks:
            print(f'{s:5d}  bar {s // BAR + 1:3d} beat {s % BAR / BEAT + 1:4.2f}  {int(s * sec) // 60}:{s * sec % 60:05.2f}  {name}')
        for t in doc['tracks']:
            print(f"   {t['name']:6s} {len(t['notes']):5d} notes")
    else:
        a.out.write_text(dump(doc))
