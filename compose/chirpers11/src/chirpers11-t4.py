#!/usr/bin/env python3
"""Ring True (Escapement, track 4). Clicky minimal techno, 125 BPM, B flat (five notes: B flat C D F G), 184 bars (5:53).

THE RULE. Six struck things, every one a physical model or noise, play ONE two-bar cell from the first bar to the
last. Not a stroke is added, moved or taken away once a thing has come in. What changes is how long each thing is
allowed to RING, and nothing else: a number from 0 (damped at once: a click) to 1 (let go: a note).
  the weight   a bass drum: a felt beater on a skin (the `drum` layer)             B flat 1
  the wood     a small bar (the `modal` layer, the marimba's modes)                the tune
  the metal    a steel bar (`modal`, the glockenspiel's modes), the off-beats      the tune's top
  the skin     a kettledrum head (`modal`, the kettle's modes)                     three low notes
  the string   a plucked string under a palm (`pluck`)                             the bass
  the air      a burst of noise in a resonator tuned to the note                   two and four
Every click is a note that was stopped too soon to be heard as one. The form lets them go one at a time, so the tune
that was in the clicks from bar 1 is heard, and then stops them again; the last sixteen bars are the first cell
once more, and the question for the ear is whether the tune can still be heard in it. In the very last bar
everything is let go at once (LAST): the answer, ringing into the silence.
A thing is LET GO slowly (over a section, bar by bar) and STOPPED quickly (over QUICK bars: a hand laid on it).

v2 (26 Nov), five switches, each `--without-…` (all five off is v1 byte for byte):
  PLATE  a seventh thing, and the one that RINGS FALSE: a small plate (`modal`, the plate's dense inharmonic modes) on
         the second sixteenth of every beat, so that with the weight on the beat, the metal on the off-beat and the
         wood on the fourth sixteenth the cell runs in sixteenths across four materials. Stopped it is the bright
         tick this family lacked; it comes in with the air, last of the family. It is the last to be let go
         (through the section with no weight), and let go it is a wash, never a note; it is choked in two bars
         with the string and the weight.
  BOOM   the weight becomes a thing that can ring true: the felt thud as it was, and under it a kettle's head on
         the same B flat whose ring time the stroke gives. Stopped: a thud. Let go: a drum that holds its note.
  ROOM   a stopped thing is dry; a thing let go is heard in a hall, in proportion to its ring (a second copy of
         each ringing stroke sent to the hall only, 20 log10(ring) dB under ROOM_DEPTH).
  TOLL   in the last bar before each new thing is let go, the weight itself is let go for that one bar: four
         strokes that hold their note, then a thud again. Nothing is added: it is the same four strokes.
  HUSH   in the last bar before the weight is lifted, a hand is laid on everything else: one bar of the whole
         family stopped dead under the weight's toll, and on the next one they are all let go.

v9 (26 Nov), THE HAND IS EMPTY. Three more switches (`--without-empty`, `-blow`, `-long`; with them off it is v8
byte for byte):
  EMPTY  since v8 each struck thing drops its stick on the last stroke of its listening, and the stick bounces to
         the one. But the hand went on playing: the thing's later strokes of that bar were struck through its own
         bounces (the wood's sixteenth 14, the metal's 15, the string's 15, the skin's 14 and 16), by a stick that
         was on the floor. They are left out now: once dropped, nothing more of that thing in the bar, and the
         bounces are heard to the one alone.
  BLOW   the air could not be dropped (v8: it is blown, not struck). Its own way of being let go too much: on the
         last stroke of its listening (bar 84, D5) the breath is not taken off and the pipe overblows up its own
         harmonics, a sixteenth each, to the one: D5, then D6, A6, D7 (the second, third and fourth), each a
         little softer. In the same bar the skin's stick is bouncing: the two things let go in that section fall
         and rise into the one together.
  LONG   everything else rings a second or more when it is let go; the air's breath was 0.4 s at any ring. A
         second, slower breath behind the first (it comes up with the ring as the first does, and is nothing
         while the air is stopped) makes a let-go stroke of the air a breath that trails off over most of a
         second (new patch `rt-sigh`: `rt-flue` and the second breath). Longer, not louder: 1.4 dB off its fader.

v8 (26 Nov), two more switches (`--without-drop`, `-skin`; with them off it is v7 byte for byte):
  DROP   until now a thing was stopped or let go. Now the stick is let go too. In the last bar of its listening
         (the four bars each thing is heard alone at the top of its turn) a thing's last stroke that is at least a
         beat before the one is dropped: it bounces. Each bounce comes sooner than the last by the same share
         (three quarters) and is that much softer, as a dropped stick's do, and the last of them would fall on the
         one, where the others come back and play it. The cell does not change: the stroke is the one that was
         always there, and nobody plays the bounces. Five drops: the wood (bar 36), the metal (52), the string
         (68), the skin (84), and the weight (116), a drum bouncing into the bar where everything is let go.
         Not the air: it is blown, and a breath has no stick to drop.
  SKIN   of the five strings nobody plays (v6), C3 and D3 never sounded: the string plays each of those notes
         once a cell, cut short (v7: 26 and 30 dB under the B flat). The skin is a drum tuned to the strings'
         notes (B flat 2, F2, D3); now the two top strings hear the skin as well, and only they do: the three low
         ones are as they were.

v7 (26 Nov), three more switches (`--without-own`, `-close`, `-soft`; with them off it is v6 byte for byte):
  OWN    the strings nobody plays are tuned to the five notes the STRING plays (F2, G2, B flat 2, C3, D3), and
         they could not hear it: they heard only the wood and the air, two and three octaves over them, and so
         sang the wood's notes and nothing under 500 Hz. Now they hear the string as well. When it is let go
         beside them each one sounds its own note, the note that was just plucked, and holds it after the pluck
         has gone: the string has a sustain pedal.
  CLOSE  the wood's closing (bars 153 to 168) was the one stopping with no mark. The strings are let go again for
         it. Nobody stops them: the wood closes, they hear less and less of it, and they go quiet by themselves.
  SOFT   1.4 kHz has stood 7 dB over the album's envelope since v3: the metal let go is 2 dB lower and its
         remembered hall 3 dB lower.

v6 (26 Nov), one more switch that is on (`--without-sympathy`; with it off it is v5 byte for byte) and one that is
off (`--with-wash`):
  SYMPATHY the strings nobody plays. Beside the seven things lie five open strings, tuned to the five notes two
           and three octaves under the wood's (F2, G2, B flat 2, C3, D3). Nothing strikes them, so the rule stands: not a
           stroke is added. They sound only because something near them is ringing at one of their own notes
           (each is a loop one period long that returns itself, and it is fed the wood and the air). They are
           things like the others, with a hand on them: let go across the section with no weight, open while the
           weight is let go, stopped in two bars with the skin and the air, and let go again in the last bar.
           When the weight is listened to alone (bars 113 to 116) what is heard round it is the strings dying.
  WASH     (OFF) the weight's listening was the only one nobody answered. The plate, the thing that rings false,
           answers it in its last two bars: a wash behind the toll. It does what it says (by solo the plate is
           all there is above 2 kHz in bars 115 and 116, 18 dB under the weight). Off because with it the scorer
           no longer hears the weight's four bars as something that returns (2 sections of 8 return for 3, under
           its band) and takes 2.2 points, for a sound that faint.

v5 (26 Nov), three more switches (`--without-flue`, `-remember`, `-lift`; with them off it is v4 byte for byte):
  FLUE     the air is blown, not struck. It was three milliseconds of noise in a resonator: let go, the resonator
           sang, which is a struck thing again and the least like its name of the seven. Now there is breath
           behind the puff (new patch `rt-flue`): a second noise that lasts nearly half a second and comes up
           only as the thing is let go, into a resonator a third as sharp. Stopped it is the same puff; let go
           it is a pipe that is blown: the note lasts as long as the breath does, not as long as the pipe rings.
  REMEMBER the room remembers. When a thing is stopped by the hand (the skin and the air, then the string and
           the plate, then the metal) it is a click again, but for the rest of that section the hall it rang in
           is still open round it: the stopped strokes go on being sent there (tracks `-kept`, each at a level
           set by solo, since a click is too short to fill a hall at a note's send). At the next stopping it is dry.
  LIFT     the metal's aftertaste, its one ringing stroke four bars after it is stopped, stood 9.4 dB under the
           mix: 4 dB up.

v4 (26 Nov), three more switches (`--without-answer`, `-even`, `-after`; with them off it is v3 byte for byte):
  ANSWER the listenings were all alike: four bars, a thing alone. Now the things already let go ANSWER the new one
         in the last two of its four bars, let go altogether as it is and 7 dB behind it: the wood is alone (nobody is before it); the metal is answered by the
         wood; the string by the metal and the wood; the skin and the air by all three. Each break is fuller than
         the last, and the fifth is the whole family without the weight (bars 97 to 112), which they have been
         gathering towards. The weight is not answered: it is what the others stand on.
  AFTER  an aftertaste, the foretaste's mirror. Four bars after it has been stopped, each thing gives ONE more
         stroke let go altogether (the last of its bar): the ring remembered, among clicks.
  EVEN   each thing alone at its own level. One number (3 dB down) left the wood alone 1.1 dB OVER the groove
         that came back after it and the others 1.1 to 2.2 under: the wood is now 5.5 down.

v3 (26 Nov), four more switches (`--without-listen`, `-off`, `-fore`, `-note`; with v2's five also off it is v1 byte for byte):
  LISTEN the others stop to listen. For the first four bars of its turn a thing is heard ALONE and let go altogether:
         the wood at bar 33, the metal at 49, the string at 65, the skin and the air together at 81, and at 113,
         after sixteen bars without it, the weight by itself, ringing B flat. Then everything comes back in, and the
         thing goes on being let go among the others. Until now a thing's turn was a slow change under six others.
         Alone it is 3 dB down, so that the others coming back is a step up.
  OFF    the hand comes off. A thing's turn no longer begins stopped and creeps: on the one of its section it is
         let go half way at once (ring 0.5: the wood goes from a 15 ms click to a 120 ms note in one bar), and the
         rest of the way over the sixteen bars. Every section now begins with something heard to change.
  FORE   a foretaste. Eight bars before its turn, each thing gives ONE stroke let go altogether (the last of its
         bar), in the middle of a section where it is otherwise stopped: one ring of a second among clicks, on a count.
  NOTE   the weight's note. In v2 the kettle under the thud rang for 1.2 s at most, so it was 17 dB gone by the
         next beat and 25 dB under its own thud. Let go, it now rings three seconds, the thud gives way (6 dB)
         and the head comes up (6 dB): each stroke lands on the last one's note, and the drum holds B flat.

Form as arithmetic: the sections are a list of lengths (LENGTHS, bars); each thing has a list of (section, ring)
points, a point `(n, r)` meaning ring r at the top of section n and `(n, r, QUICK)` ring r QUICK bars into it; its
ring at any bar is the straight line between them (`ring_at`). A ring r is a ring time `t0 * (t1 / t0) ** r` seconds
(equal steps of r are equal ratios of time), handed to the stroke as `expr.ring`.
"""
import argparse
import json
from math import log10, log2
from pathlib import Path

BPM = 125
BAR, CELL = 16, 32                          # sixteenths in a bar and in the cell
SEC, QUICK, LAST = 16, 2, 1                 # bars: a section in which something is let go; how fast a thing is stopped; let go at the end
LENGTHS = [SEC] * 8 + [SEC // 2] * 3 + [SEC] * 2   # sections 1-8 let go, 9-11 stop (half as long: nothing in them is turning), 12-13
TOP = [sum(LENGTHS[:i]) for i in range(len(LENGTHS) + 1)]   # the bar each section starts on (and the end)
SECTIONS = len(LENGTHS)
BARS = TOP[-1]
OUT = Path(__file__).resolve().parents[3] / 'songs/chirpers11-t4.yaml'

# The cell: (sixteenth of 32, pitch, how hard). It never changes.
STROKES = {
    'weight': [(s, 'Bb1', .95 if s % BAR == 0 else .88) for s in range(0, CELL, 4)],
    'wood':   [(3, 'D5', .8), (7, 'F5', .7), (11, 'G5', .85), (14, 'F5', .65), (19, 'D5', .8), (23, 'C5', .7), (27, 'Bb4', .85), (29, 'C5', .6)],
    'metal':  [(2, 'F6', .7), (6, 'F6', .55), (10, 'G6', .7), (14, 'F6', .55), (18, 'D6', .7), (22, 'F6', .55), (26, 'G6', .7), (30, 'Bb6', .6)],
    'skin':   [(10, 'Bb2', .8), (15, 'F2', .65), (26, 'Bb2', .8), (29, 'D3', .6), (31, 'F2', .7)],
    'string': [(2, 'Bb2', .85), (7, 'Bb2', .7), (11, 'F2', .8), (14, 'G2', .7), (18, 'Bb2', .85), (23, 'Bb2', .7), (27, 'D3', .8), (30, 'C3', .7)],
    'air':    [(4, 'F5', .8), (12, 'F5', .75), (20, 'F5', .8), (28, 'D5', .75)],
}
# Ring time, seconds: (shut, let go).
RING = {'weight': (0.25, 1.10), 'wood': (0.015, 1.00), 'metal': (0.012, 1.20), 'skin': (0.030, 1.20), 'string': (0.030, 1.00), 'air': (0.004, 0.60)}
# Who is in from which bar, and each one's ring at section boundaries (a point per boundary named; straight lines between).
ENTERS = {'weight': 0, 'wood': 0, 'metal': 8, 'string': TOP[1], 'skin': TOP[1], 'air': TOP[1] + 8}
OUT_OF = {'weight': (TOP[6], TOP[7])}       # the seventh section: the weight is lifted
Q = QUICK
SHAPE = {                                    # (section counted from 0, ring[, bars into it])
    'wood':   [(2, 0), (3, 1), (3, .45, Q), (6, .45), (6, 1, Q), (11, 1), (12, 0)],
    'metal':  [(3, 0), (4, 1), (4, .5, Q), (6, .5), (6, 1, Q), (10, 1), (10, 0, Q)],
    'string': [(4, 0), (5, 1), (5, .7, Q), (6, .7), (6, 1, Q), (9, 1), (9, 0, Q)],
    'skin':   [(5, 0), (6, 1), (8, 1), (8, 0, Q)],
    'air':    [(5, 0), (6, .6), (6, 1, Q), (8, 1), (8, 0, Q)],
    'weight': [(7, 0), (8, 1), (9, 1), (9, 0, Q)],
}
NAMES = ['taps', 'the family', 'the wood is let go', 'the metal is let go', 'the string is let go', 'the skin and the air are let go', 'no weight: all let go',
         'the weight is let go', 'the skin and the air are stopped', 'the string and the weight are stopped', 'the metal is stopped', 'the wood closes', 'taps again']
assert len(NAMES) == SECTIONS

long_ring = {'a': '0.2ms', 'd': '0s', 's': 1, 'r': '2.5s', 'curve': 1}
ring = lambda t0: {'value': t0, 'mod': [{'src': 'expr.ring', 'amount': 1}]}
PATCHES = {
    'rt-weight': {'about': 'Ring True: the weight. A bass drum as a thing: a felt beater on a skin, its ring time from the stroke (expr.ring, seconds over 0.25).',
                  'synth': {'layers': [{'type': 'drum', 'beater': 'felt', 'decay': ring(0.25), 'strike': 0.15, 'slap': 0.4, 'sharp': 60}], 'amp': long_ring},
                  'play': {'event_stable': True, 'vel_sens': 0.3}},
    'rt-wood': {'about': 'Ring True: the wood. A small bar (1 : 4 : 10) struck near its middle; its ring time from the stroke (expr.ring, seconds over 0.015).',
                'synth': {'layers': [{'type': 'modal', 'modes': 'bar', 'decay': ring(0.015), 'bright': 0.75, 'strike': 0.35}], 'amp': long_ring},
                'play': {'event_stable': True, 'vel_sens': 0.6}},
    'rt-metal': {'about': 'Ring True: the metal. A steel bar (1 : 2.76 : 5.40 : 8.93); its ring time from the stroke (expr.ring, seconds over 0.012).',
                 'synth': {'layers': [{'type': 'modal', 'modes': 'glock', 'decay': ring(0.012), 'bright': 1.0, 'strike': 0.6}], 'amp': long_ring},
                 'play': {'event_stable': True, 'vel_sens': 0.6}},
    'rt-skin': {'about': 'Ring True: the skin. A kettledrum head (the air in the kettle pulls its modes to 1 : 1.5 : 2 : 2.5, so it sings its note); its ring time from the stroke (expr.ring, seconds over 0.03).',
                'synth': {'layers': [{'type': 'modal', 'modes': 'kettle', 'decay': ring(0.03), 'bright': 0.6, 'strike': 0.4}], 'amp': long_ring},
                'play': {'event_stable': True, 'vel_sens': 0.6}},
    'rt-string': {'about': 'Ring True: the string. A plucked string whose ring time comes from the stroke (expr.ring, seconds over 0.03): a palm on it, lifted.',
                  'synth': {'layers': [{'type': 'pluck', 'decay': ring(0.03), 'bright': 0.5, 'pick': 0.18, 'soft': 0.3}], 'amp': long_ring},
                  'play': {'event_stable': True, 'vel_sens': 0.5}},
    'rt-air': {'gain': '24dB', 'about': 'Ring True: the air. Three milliseconds of noise into a resonator tuned to the note (a band-pass); how long it sings comes from the stroke (expr.ring, on its q).',
               'synth': {'layers': [{'type': 'noise', 'color': 'white', 'level': {'value': '-70dB', 'mod': [{'src': 'env.burst', 'amount': 70}]}}],
                         'env': {'burst': {'a': '0.1ms', 'd': '3ms', 's': 0, 'r': '3ms'}},
                         'filters': [{'kind': 'bp', 'cutoff': 261.63, 'keytrack': 1, 'q': {'value': 0.7, 'mod': [{'src': 'expr.ring', 'amount': 1}]}}],
                         'amp': long_ring},
               'play': {'event_stable': True, 'vel_sens': 0.5}},
}
PATCH = {k: 'rt-' + k for k in STROKES}

# ---- v2: the switches, and what each adds. Nothing above is changed by them.
ON = {'plate': True, 'boom': True, 'room': True, 'toll': True, 'hush': True, 'listen': True, 'off': True, 'fore': True, 'note': True,
      'answer': True, 'even': True, 'after': True, 'flue': True, 'remember': True, 'lift': True, 'sympathy': True, 'wash': False, 'own': True, 'close': True, 'soft': True, 'drop': True, 'skin': True, 'empty': True, 'blow': True, 'long': True}
BLOW = {'harmonics': (2, 3, 4), 'db': -4}   # v9: the harmonics of its pipe the air overblows through, a sixteenth each, after the last stroke of its listening; dB on each beside the one before.
# Bench (blow.sh, blowread.py: the air alone from that stroke by sixteenth): at -2 dB a step the four read -18 -19 -18 -20 (the resonator gives a higher note more: its band is wider) and the bar's last beat stood 2 to 3 dB
# OVER the one it runs into (-21): a rise that tops what it leads to. So -4 a step
LONG = {'env': {'a': '120ms', 'd': '2s', 's': 0, 'r': '3s'}, 'db': -6, 'fader': -1.4}   # v9: the second breath: it is still coming up when the stroke ends (a sixteenth is 120 ms) and trails off after it; dB beside the first breath; dB on the air's fader.
# Longer, not louder: with the second breath the air alone read 1.4 dB more where everything is let go (bars 121 to 124: -24.0 for -25.4) and put 0.9 dB on the mix from 450 to 900 Hz, where the air is all but the mix (2 dB under it) and
# the song is already 5 dB over the album. So 1.4 dB off its fader.
# Bench, one let-go stroke alone by 120 ms: with 900 ms to let go it read -15 -27 -45 -55 where v8 reads -15 -37 -57 -59: a quarter of a second, not a second (the level hangs from the envelope by 70 dB, so its first tenth is 7 dB). So 3 s
DROP = {'share': 0.75, 'bounces': 8, 'room': 4, 'not': ('air',)}   # v8: each bounce's gap, and its level, as a share of the one before; how many are heard (the next would be the one); sixteenths before the one that the dropped stroke must leave; what is not struck.
# Bench (drop.sh, dropread.py: the stroke alone with its bounces, by 60 ms to the one): the wood -27 -32 -34 -36 -37 -36 -40 -36 -34 -35; the weight -22 -29 -26 -31 -29 -32 -33 -34: each bounce is softer and they come faster: the wood's buzzes back up towards the one and the others' run out (v8's note said the level holds; it does not).
# The air was dropped too at first, and its stroke by a track of its own read 5 dB under the same stroke on its own track (-23 for -18: the flue's pipe is still sounding from the stroke before, and a second track's pipe is cold): so not the air
SKIN = {'feeds': ('skin',), 'feed': '-28dB', 'strings': ('C3', 'D3')}   # v8: what else two of the strings hear, and how much of it.
# Bench (own.sh, ownread.py: the song with it less the song without, bars 117 and 118): with all five hearing the skin at -32 dB it woke B flat 2 most, then F2 (3 dB under), G2 (4), C3 (8), D3 (20): mostly more of the three that
# sounded already, 15 and 16 dB under the mix from 60 to 250 Hz on top of the 12 and 13 the string wakes. So only the two that did not sound, and 4 dB more of it
OWN = {'feeds': ('string',), 'feed': '-29dB'}   # v7: what else the strings hear, and how much of it.
# Bench (the song with it less the song without, bars 117 and 118): at -36 dB what the string wakes stood 18.1 and 19.8 dB under the mix from 60 to 120 and 120 to 250 Hz (B flat 2 strongest, then G2, F2): there, and nothing. 7 dB more
SOFT = {'ease': {'metal': -2}, 'kept': {'metal': -3}}   # v7: dB on the metal let go, and on its remembered hall
SYMPATHY = {'strings': (('F2', 87.307, 0.3), ('G2', 97.999, 0.0), ('Bb2', 116.541, -0.3), ('C3', 130.813, 0.15), ('D3', 146.832, -0.15)),   # v6: each string's note, Hz and side (a return cannot be shorter than 6 ms, so F and G are an octave under the others)
            'feeds': ('wood', 'air'), 'feed': '-30dB', 'back': 0.985, 'lp': 5000, 'let': -24}   # what they hear and how much of it; what each gives back of itself a period; the low-pass in the loop; the dB their hand starts from.
# Bench (the song with them less the song without): hearing the wood and the air at -20 dB they stood 3.7 and 2.5 dB under the whole mix once the wood was let go beside them (a string that gives back 0.985 answers a held note at its own pitch 36 dB up): 10 dB less
FLUE = {'q': 40, 'breath': {'a': '30ms', 'd': '450ms', 's': 0, 'r': '300ms'}, 'top': -24, 'ease': 0}   # v5: the resonator's q let go (it was 120); the breath; the breath's level let go, dB beside the puff's; dB on the stroke at ring 1
# The breath's level is set under the track's clip. Bench, the stroke let go, level over two seconds and its third harmonic beside its note: top 0 -25.8 (and 10 dB off the stroke took only 1.9 off: it was all clip);
# -12 -28.2, -26.0; -24 -33.1, -32.4; -36 -41.6, -31.9. At -24 it is clean and climbs with the ring: -51.5 -53.6 -43.3 -43.7 -37.6 -33.1 at rings 0, 0.2 … 1 (rt-air: -47.8 -54.8 -40.8 -42.0 -33.7 -44.1).
CAL_FLUE = [0, 0, 0, 0, 0, 0]                # v5: nothing is given back: the flue's highest sample is the clip's at every ring
KEPT = {'air': 7, 'string': 2.5, 'metal': 4, 'skin': 7, 'plate': 11}   # v5: dB over its dry fader at which a stopped thing is still sent to the hall (a track of its own, `-kept`). Set by solo: sent as a let-go stroke is (10 dB under the dry), the halls stood 23 to 38 dB under the mix above 300 Hz, which is nothing; a click is too short to fill a hall.
# At these each hall stands 2.5 to 4 dB over the click it remembers and 11 to 17 dB under the mix (K-weighted, by parts). At 10 and 17 the skin's and the plate's stood 7 and 10 dB over their own clicks: a hall with a tick in it, not a tick with a hall round it
LIFT = {'metal': 4}                          # v5: dB on a thing's aftertaste
ANSWER = 2                                   # v4: the last bars of a listening in which the things already let go answer
ANSWER_DB = -10                              # dB on the answering things: behind the thing they answer (at -6 the answered bars stood 0.6 to 1.4 dB OVER the groove that came back; at -10 level with it, so the weight's return is still the step)
AFTER = SEC // 4                             # v4: bars after it is stopped that a thing gives one more stroke let go
ALONE_OF = {'wood': -5.5}                    # v4 EVEN: dB on a thing alone where ALONE's one number left it over the return
LISTEN = 4                                   # bars at the top of its turn that a thing is heard alone, let go altogether
ALONE = -3                                   # dB on its strokes while it is alone (unhushed the wood alone read 2.4 dB OVER the groove it broke off, and the others' return was a step down)
OFF = 0.5                                    # the share of its ring a thing is given at once, on the one of its turn
FORE = SEC // 2                              # bars before its turn that a thing gives one stroke let go
NOTE = {'ring': (0.04, 3.0), 'thud': -2, 'note': 2, 'from': '-6dB', 'ease': -3.5}   # the head's ring time, seconds (v2: to 1.2: 17 dB gone by the next beat); dB a second of ring on the felt layer and on the head; the head's level stopped; dB at ring 1
PLATE = {'strokes': [(1, 'F7', .6), (5, 'F7', .5), (9, 'F7', .6), (13, 'F7', .5), (17, 'F7', .6), (21, 'F7', .5), (25, 'F7', .6)],
         'ring': (0.010, 1.5), 'enters': ENTERS['air'], 'shape': [(6, 0), (7, 1), (9, 1), (9, 0, Q)], 'ease': -8, 'gain': '-9dB', 'pan': -0.5}
BOOM = {'ring': (0.04, 1.2), 'gain': '-3dB'}
ROOM_DEPTH = -16                             # dB under its dry fader that a thing let go altogether is sent to the hall
TOLLS = [TOP[i] - 1 for i in range(2, 7)]    # the bar before each of sections 3 to 7: the weight is let go for it
HUSH = TOP[6] - 1                            # the bar before the weight is lifted: everything else is stopped for it
ROOM_FROM = 0.05                             # strokes with less ring than this are not sent at all
ROOM_THINGS = ('wood', 'metal', 'skin', 'string', 'air', 'plate')
NEW = {
    'rt-plate': {'about': 'Ring True: the plate, the thing that rings false. A small thin plate (dense inharmonic modes) struck near its edge; its ring time from the stroke (expr.ring, seconds over 0.010). Stopped, a bright tick; let go, a wash and never a note.',
                 'synth': {'layers': [{'type': 'modal', 'modes': 'plate', 'decay': ring(0.010), 'bright': 1.0, 'strike': 0.7}], 'amp': long_ring},
                 'play': {'event_stable': True, 'vel_sens': 0.6}},
    'rt-boom': {'about': "Ring True: the weight as a thing that can ring true. The felt beater's thud on a skin (fixed), and under it a kettledrum head on the same note whose ring time comes from the stroke (expr.ring, seconds over 0.04).",
                'synth': {'layers': [{'type': 'drum', 'beater': 'felt', 'decay': 0.35, 'strike': 0.15, 'slap': 0.4, 'sharp': 60},
                                     {'type': 'modal', 'modes': 'kettle', 'decay': ring(0.04), 'bright': 0.4, 'strike': 0.2, 'level': '-3dB'}], 'amp': long_ring},
                'play': {'event_stable': True, 'vel_sens': 0.3}},
}


def things():
    """The cell's things in order, with the plate when it is on."""
    return list(STROKES) + (['plate'] if ON['plate'] else [])


def drum_patch():
    """rt-boom with the stroke's ring on the two layers' levels as well: the thud gives way to the note."""
    felt, kettle = (dict(x) for x in NEW['rt-boom']['synth']['layers'])
    felt['level'] = {'value': '0dB', 'mod': [{'src': 'expr.ring', 'amount': NOTE['thud']}]}
    kettle['level'] = {'value': NOTE['from'], 'mod': [{'src': 'expr.ring', 'amount': NOTE['note']}]}
    return {'about': "Ring True: the weight whose thud gives way to its note (v3). rt-boom's two layers, a felt thud and a kettledrum head on the same note; the stroke's ring (expr.ring, seconds) sets the head's ring time and also takes the thud down and brings the head up.",
            'synth': {'layers': [felt, kettle], 'amp': NEW['rt-boom']['synth']['amp']}, 'play': NEW['rt-boom']['play']}


def strokes_of(thing):
    return PLATE['strokes'] if thing == 'plate' else STROKES[thing]


def ring_range(thing):
    return PLATE['ring'] if thing == 'plate' else (NOTE['ring'] if ON['note'] else BOOM['ring']) if thing == 'weight' and ON['boom'] else RING[thing]


def enters(thing):
    return PLATE['enters'] if thing == 'plate' else ENTERS[thing]


def up(pitch, semis):
    """A note name some semitones higher."""
    names = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
    n = names.index(pitch[:-1]) + 12 * int(pitch[-1]) + semis
    return f'{names[n % 12]}{n // 12}'


def blown():
    """v9: (bar, sixteenth of the bar) of the stroke after which the air overblows: its last stroke in the last bar of its listening. None if it has none."""
    pts = SHAPE['air']
    if not (ON['blow'] and ON['listen'] and pts[0][1] == 0):
        return None
    bar = TOP[pts[0][0]] + LISTEN - 1
    mine = [s % BAR for s, _, _ in strokes_of('air') if s // BAR == bar % 2 and s % BAR + len(BLOW['harmonics']) < BAR]
    return (bar, mine[-1]) if mine else None


def flue_patch():
    """rt-air with breath behind the puff: a second noise, half a second long, whose level the stroke's ring brings up."""
    air = PATCHES['rt-air']
    breath = {'type': 'noise', 'color': 'white', 'level': {'value': f"{-130 + FLUE['top']}dB", 'mod': [{'src': 'env.breath', 'amount': 70}, {'src': 'expr.ring', 'amount': round(60 / (FLUE['q'] - 0.7), 3)}]}}
    if ON['long']:                                               # v9: the same breath again, slower: it trails off after the stroke
        sigh = {'type': 'noise', 'color': 'white', 'level': {'value': f"{-130 + FLUE['top'] + LONG['db']}dB", 'mod': [{'src': 'env.sigh', 'amount': 70}, {'src': 'expr.ring', 'amount': round(60 / (FLUE['q'] - 0.7), 3)}]}}
        return {'gain': air['gain'], 'about': "Ring True: the air, blown (v5), and its breath trailing off (v9). rt-air's puff of noise in a resonator tuned to the note; behind it a breath nearly half a second long, and behind that a slower one that goes on for a second after the stroke. The stroke's ring brings both up (60 dB from stopped to let go). The resonator's q goes to 40, not 120, so let go it is breath with a note in it and not a ping.",
                'synth': {**air['synth'], 'layers': air['synth']['layers'] + [breath, sigh], 'env': {**air['synth']['env'], 'breath': FLUE['breath'], 'sigh': LONG['env']}}, 'play': air['play']}
    return {'gain': air['gain'], 'about': "Ring True: the air, blown (v5). rt-air's puff of noise in a resonator tuned to the note, and behind it a breath: a second noise nearly half a second long whose level the stroke's ring brings up (60 dB from stopped to let go). The resonator's q goes to 40, not 120, so let go it is breath with a note in it and not a ping.",
            'synth': {**air['synth'], 'layers': air['synth']['layers'] + [breath], 'env': {**air['synth']['env'], 'breath': FLUE['breath']}}, 'play': air['play']}


def remembered(thing, bar):
    """v5: is the thing, stopped by the hand, still heard in its hall? From the bar it is stopped to the end of that section."""
    last = (PLATE['shape'] if thing == 'plate' else SHAPE[thing])[-1]
    return ON['remember'] and len(last) > 2 and last[1] == 0 and TOP[last[0]] + last[2] <= bar < TOP[last[0] + 1]


def patch_of(thing):
    if thing == 'air' and ON['flue']:
        return 'rt-sigh' if ON['long'] else 'rt-flue'            # v9: with its second breath it is another sound, under another name
    return 'rt-plate' if thing == 'plate' else ('rt-drum' if ON['note'] else 'rt-boom') if thing == 'weight' and ON['boom'] else PATCH[thing]


def ring_at(thing, bar):
    """The thing's ring (0..1) at a bar: the straight line between its points; flat before the first and after the last."""
    if bar >= BARS - LAST:
        return 1.0
    if thing == 'weight' and ON['toll'] and bar in TOLLS:
        return 1.0
    if thing != 'weight' and ON['hush'] and bar == HUSH:
        return 0.0
    pts = [(TOP[p[0]] + (p[2] if len(p) > 2 else 0), p[1]) for p in (PLATE['shape'] if thing == 'plate' else SHAPE[thing])]
    if ON['off'] and pts[0][1] == 0 and pts[0][0] <= bar < pts[1][0]:      # its turn: half at once, the rest across the section
        (b0, _), (b1, r1) = pts[0], pts[1]
        return r1 * (OFF + (1 - OFF) * (bar - b0) / (b1 - b0))
    if bar <= pts[0][0]:
        return pts[0][1]
    for (b0, r0), (b1, r1) in zip(pts, pts[1:]):
        if b0 <= bar < b1:
            return r0 + (r1 - r0) * (bar - b0) / (b1 - b0)
    return pts[-1][1]


def dropped(thing):
    """v8: (bar, sixteenth of the bar) of the stroke a thing drops: in the last bar of its listening, its last stroke that leaves DROP['room'] sixteenths before the one. None if it has no listening."""
    pts = SHAPE.get(thing)
    if not (ON['drop'] and ON['listen'] and pts and pts[0][1] == 0) or thing in DROP['not']:
        return None
    bar = TOP[pts[0][0]] + LISTEN - 1
    late = [s % BAR for s, _, _ in strokes_of(thing) if s // BAR == bar % 2 and s % BAR <= BAR - DROP['room']]
    return (bar, late[-1]) if late else None


def listened(bar):
    """The things whose turn began within the last LISTEN bars (they are heard alone); empty when nothing is listened to."""
    if not ON['listen']:
        return set()
    return {k for k, pts in SHAPE.items() if pts[0][1] == 0 and TOP[pts[0][0]] <= bar < TOP[pts[0][0]] + LISTEN}


def answering(bar):
    """v4: the things that answer in this bar: in the last ANSWER bars of a listening (never the weight's), every
    thing whose own turn began before it. Empty when nobody answers."""
    out = set()
    if ON['answer']:
        for k in listened(bar):
            top = TOP[SHAPE[k][0][0]]
            if k == 'weight' and ON['wash'] and ON['plate'] and bar >= top + LISTEN - ANSWER:
                out |= {'plate'}                                # v6: the plate answers the toll
            if k != 'weight' and bar >= top + LISTEN - ANSWER:
                out |= {j for j, pts in SHAPE.items() if j != 'weight' and pts[0][1] == 0 and TOP[pts[0][0]] < top}
    return out


def aftertaste(thing):
    """v4: the bar in which a thing, stopped, gives one more let-go stroke (None for the weight, and for a thing that is never stopped)."""
    if thing == 'weight' or not ON['after']:
        return None
    last = (PLATE['shape'] if thing == 'plate' else SHAPE[thing])[-1]
    return TOP[last[0]] + (last[2] if len(last) > 2 else 0) + AFTER if last[1] == 0 else None


def foretaste(thing):
    """The bar in which a thing gives its one let-go stroke before its turn (None for the weight: it has its tolls)."""
    if thing == 'weight':
        return None
    first = (PLATE['shape'] if thing == 'plate' else SHAPE[thing])[0]
    return TOP[first[0]] - FORE


def seconds(thing, r):
    t0, t1 = ring_range(thing)
    return t0 * (t1 / t0) ** r


def air_q(r):
    """The air's resonator: a band-pass's q from a ring, 0.7 (a puff) to 120 (it sings); with FLUE to 40 (the breath sings, not the pipe)."""
    return 0.7 * ((FLUE['q'] if ON['flue'] else 120) / 0.7) ** r


# What the bench reads (--bench, then bread.py): a thing's highest sample at rings 0, 0.2 … 1. A shut string or a
# singing resonator is far quieter than the same stroke let go, so each stroke is given back the difference.
CAL = {'string': [-26.8, -17.3, -13.8, -11.4, -10.0, -10.3], 'air': [-41.2, -34.1, -37.3, -34.5, -36.8, -35.9]}
# And the other way: a bar that rings for a second carries far more than the same bar stopped, at the same highest
# sample. dB taken from a stroke at ring 1 (in proportion below it), so that letting go is a swell and not a flood.
EASE = {'wood': -5, 'metal': -5, 'skin': -3}


def level(thing, r):
    """dB to add to a stroke at ring r so that the thing's highest sample is the same at every ring."""
    db = (PLATE['ease'] if thing == 'plate' else NOTE['ease'] if thing == 'weight' and ON['boom'] and ON['note'] and NOTE['ease'] else FLUE['ease'] if thing == 'air' and ON['flue'] else EASE.get(thing, 0) + (SOFT['ease'].get(thing, 0) if ON['soft'] else 0)) * r
    if thing in CAL:
        cal = CAL_FLUE if thing == 'air' and ON['flue'] else CAL[thing]
        c = [cal[-1] - v for v in cal]
        x = min(r * 5, 4.999)
        i = int(x)
        db += c[i] + (c[i + 1] - c[i]) * (x - i)
    return round(db, 2) if thing in CAL or thing in EASE or thing == 'plate' or (thing == 'weight' and ON['boom'] and ON['note'] and NOTE['ease']) else None


def expr(thing, r):
    return {'ring': round(air_q(r) - 0.7, 4)} if thing == 'air' else {'ring': round(seconds(thing, r) - ring_range(thing)[0], 5)}


def stroke(thing, at, pitch, vel, r):
    n = {'at': at, 'len': 0.25, 'pitch': pitch, 'vel': vel, 'expr': expr(thing, r)}
    if level(thing, r) is not None:
        n['gain'] = f'{level(thing, r)}dB'
    return n


def build():
    T = {k: [] for k in things()}
    if ON['room']:
        T.update({k + '-room': [] for k in ROOM_THINGS if k in T})
        if ON['remember']:
            T.update({k + '-kept': [] for k in ROOM_THINGS if k in T and k in KEPT})
    T.update({k + '-drop': [] for k in things() if dropped(k)})
    for bar in range(BARS):
        for thing in things():
            if bar < enters(thing) or any(a <= bar < b for a, b in [OUT_OF.get(thing, (0, 0))]):
                continue
            alone = listened(bar)
            if alone and thing not in alone and thing not in answering(bar):
                continue
            r_bar = 1.0 if alone else ring_at(thing, bar)        # whatever sounds in a listening is let go altogether
            mine = [x for x in strokes_of(thing) if x[0] // BAR == bar % 2]
            for s, pitch, vel in strokes_of(thing):
                if ON['empty'] and dropped(thing) and bar == dropped(thing)[0] and s // BAR == bar % 2 and s % BAR > dropped(thing)[1]:
                    continue                                    # v9 EMPTY: its stick is on the floor
                if s // BAR == bar % 2:
                    r = 1.0 if ((ON['fore'] and bar == foretaste(thing)) or bar == aftertaste(thing)) and s == mine[-1][0] else r_bar
                    n = stroke(thing, bar * 4 + (s % BAR) / 4, pitch, vel, r)
                    if alone and ALONE:
                        down = ANSWER_DB if thing not in alone else ALONE_OF.get(thing, ALONE) if ON['even'] else ALONE
                        n['gain'] = f"{round(float(n.get('gain', '0dB')[:-2]) + down, 2)}dB"
                    if ON['lift'] and thing in LIFT and bar == aftertaste(thing) and r == 1.0 and not alone:
                        n['gain'] = f"{round(float(n.get('gain', '0dB')[:-2]) + LIFT[thing], 2)}dB"
                    T[thing + '-drop' if dropped(thing) == (bar, s % BAR) else thing].append(n)   # v8: the dropped stroke goes by a track of its own, so that only it bounces
                    if thing + '-room' in T and r >= ROOM_FROM:      # the room hears a thing as far as it is let go
                        own = float(n.get('gain', '0dB')[:-2])
                        T[thing + '-room'].append({**n, 'gain': f'{round(own + 20 * log10(r), 2)}dB'})
                    elif thing + '-kept' in T and remembered(thing, bar):   # v5: stopped, and its hall still open
                        T[thing + '-kept'].append(dict(n))
                    if thing == 'air' and blown() == (bar, s % BAR):        # v9 BLOW: the breath is not taken off: up the pipe's harmonics to the one
                        for j, h in enumerate(BLOW['harmonics'], 1):
                            m = {**n, 'at': n['at'] + j / 4, 'pitch': up(pitch, round(12 * log2(h))), 'gain': f"{round(float(n.get('gain', '0dB')[:-2]) + BLOW['db'] * j, 2)}dB"}
                            T[thing].append(m)
                            if thing + '-room' in T:
                                T[thing + '-room'].append(dict(m))
    return T


def song(T, bars=BARS):
    track = lambda name, gain, pan=0, **more: {'name': name, 'patch': patch_of(name), 'gain': gain, 'pan': pan, 'notes': T[name], **more}
    hold = lambda db: f'clip drive=0dB ceiling={db}dB'          # a stroke's highest sample is its own, not the limiter's
    doc = {
        'about': "Chirpers, Escapement, track 4: Ring True, by chirper-one. Generated by compose/chirpers11/src/chirpers11-t4.py (its docstring is the rule). " + ('Seven' if ON['plate'] else 'Six') + " struck things, each a physical model or noise, play one two-bar cell from the first bar to the last; the only thing that changes is how long each is allowed to ring. Every click is a note stopped too soon to be heard as one: the form lets them go one at a time, then shuts them again.",
        'meta': {'artist': 'chirpers', 'album': 'Escapement', 'title': 'Ring True', 'track': 4, 'year': 2026},
        'tempo': BPM, 'seed': 1, 'event_stable': True, 'length': f'{bars * 4}b', 'tail': '4s', 'ceiling': '-1dB', 'true_peak': True, 'loudness': -12,
        'patches': PATCHES,
        'buses': {'room': {'fx': ['reverb kind=room decay=0.4s mix=1 predelay=6ms', 'hp cutoff=300']}},
        'master': {'fx': [{'type': 'eq', 'bands': ['hp cutoff=28']}]},
        'tracks': [track('weight', '-3dB'), track('wood', '-3dB', pan=-0.3, sends={'room': '-14dB'}), track('metal', '-5dB', pan=0.35, sends={'room': '-14dB'}),
                   track('skin', '0dB', pan=0.15, fx=[hold(-10)], sends={'room': '-14dB'}), track('string', '-3dB', pan=-0.1), track('air', f"{2 + LONG['fader']:g}dB" if ON['long'] and ON['flue'] else '2dB', pan=0.05, fx=[hold(-9)], sends={'room': '-12dB'})],
    }
    by_name = {t['name']: t for t in doc['tracks']}
    if ON['boom'] and ON['note']:
        doc['patches'] = {**doc['patches'], 'rt-drum': drum_patch()}
    elif ON['boom']:
        doc['patches'] = {**doc['patches'], 'rt-boom': NEW['rt-boom']}
        by_name['weight']['gain'] = BOOM['gain']
    if ON['flue']:
        doc['patches'] = {**doc['patches'], patch_of('air'): flue_patch()}
    if ON['plate'] and 'plate' in T:
        doc['patches'] = {**doc['patches'], 'rt-plate': NEW['rt-plate']}
        doc['tracks'].append(track('plate', PLATE['gain'], pan=PLATE['pan'], sends={'room': '-16dB'}))
        by_name['plate'] = doc['tracks'][-1]
    if ON['room']:
        doc['buses'] = {**doc['buses'], 'hall': {'fx': ['reverb kind=hall decay=2.4s mix=1 predelay=20ms', 'hp cutoff=300', 'lp cutoff=7000']}}
        for k in ROOM_THINGS:
            if k + '-room' in T:
                dry = by_name[k]
                doc['tracks'].append({'name': k + '-room', 'patch': dry['patch'], 'gain': f"{float(dry['gain'][:-2]) + ROOM_DEPTH}dB", 'pan': dry['pan'],
                                      'notes': T[k + '-room'], 'out': 'hall', **({'fx': dry['fx']} if 'fx' in dry else {})})
        for k in ROOM_THINGS:
            if T.get(k + '-kept'):
                dry = by_name[k]
                doc['tracks'].append({'name': k + '-kept', 'patch': dry['patch'], 'gain': f"{float(dry['gain'][:-2]) + KEPT[k] + (SOFT['kept'].get(k, 0) if ON['soft'] else 0)}dB", 'pan': dry['pan'],
                                      'notes': T[k + '-kept'], 'out': 'hall', **({'fx': dry['fx']} if 'fx' in dry else {})})
    for k in [k for k in by_name if T.get(k + '-drop')]:        # v8 DROP: the same track again for the one stroke, and its bounces: echoes of it, each sooner and softer by the same share
        doc['tracks'].append({**{x: y for x, y in by_name[k].items() if x != 'notes'}, 'name': k + '-drop', 'notes': T[k + '-drop']})
        rest = (BAR - dropped(k)[1]) * 60000 / BPM / 4            # ms from the stroke to the one
        gap = rest * (1 - DROP['share']) / (1 - DROP['share'] ** (DROP['bounces'] + 1))
        doc['buses'][k + '-bounce'] = {'pan': by_name[k]['pan'], 'returns': [{'from': k + '-drop', 'gain': f"{20 * log10(DROP['share']) * j:.2f}dB", 'time': f"{gap * (1 - DROP['share'] ** j) / (1 - DROP['share']):.1f}ms"} for j in range(1, DROP['bounces'] + 1)]}
    if ON['sympathy'] and bars == BARS:
        hand = {'points': [['0b', -60], [f'{TOP[6] * 4 - 1}b', -60], [f'{TOP[6] * 4}b', SYMPATHY['let']], [f'{TOP[7] * 4}b', 0], [f'{TOP[8] * 4}b', 0], [f'{(TOP[8] + QUICK) * 4}b', -60]] +
                          ([[f'{TOP[11] * 4 - 1}b', -60], [f'{TOP[11] * 4}b', 0], [f'{TOP[12] * 4 - 1}b', 0], [f'{TOP[12] * 4}b', -60]] if ON['close'] else []) +   # v7: let go while the wood closes; shut again for the taps
                          [[f'{(BARS - LAST) * 4 - 0.5}b', -60], [f'{(BARS - LAST) * 4}b', 0], [f'{BARS * 4 + 16}b', 0]], 'curve': 0}
        for name, hz, side in SYMPATHY['strings']:
            me = 'sym-' + name.lower()
            t = f"{1000 / hz - 225.1 / SYMPATHY['lp']:.3f}ms"         # a period, less the low-pass's own delay (0.2251 / its cutoff), so the loop is in tune
            doc['buses'][me] = {'pan': side, 'gain': {'value': '0dB', 'mod': [{'src': 'auto.hand', 'amount': 1}]}, 'auto': {'hand': hand}, 'fx': [f"lp cutoff={SYMPATHY['lp']}"],
                                'returns': [{'from': k, 'gain': SYMPATHY['feed'], 'time': t} for k in SYMPATHY['feeds']] + ([{'from': k, 'gain': OWN['feed'], 'time': t} for k in OWN['feeds']] if ON['own'] else []) + ([{'from': k, 'gain': SKIN['feed'], 'time': t} for k in SKIN['feeds']] if ON['skin'] and name in SKIN['strings'] else []) + [{'from': me, 'gain': f"{20 * log10(SYMPATHY['back']):.2f}dB", 'time': t}]}
    return doc


def bench():
    """Each thing alone, one stroke every two seconds at rings 0, 0.2 … 1 (60 BPM, a stroke every two beats)."""
    was = ON['room']
    ON['room'] = False                                           # the bench reads the things dry
    T = {k: [stroke(k, 2 * i, strokes_of(k)[0][1], .8, i / 5) for i in range(6)] for k in things()}
    doc = song(T, bars=3)
    ON['room'] = was
    doc.update(tempo=60, length='12b', tail='2s', loudness=None)
    for t in doc['tracks']:
        t.update(gain='0dB', pan=0, sends={})
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


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--out', type=Path, default=OUT)
    ap.add_argument('--form', action='store_true', help='print the form and stop')
    ap.add_argument('--bench', action='store_true', help='write the bench song (each thing at six rings) instead')
    for k, on in ON.items():
        ap.add_argument(f"--{'without' if on else 'with'}-{k}", action='store_true', help=f"{'leave out' if on else 'put in'} {k} (of the twenty-four that are on: all off is v1; the last nineteen off is v2; the last fifteen off is v3; the last twelve off is v4; the last nine off is v5; the last eight off is v6; the last five off is v7; the last three off is v8)")
    a = ap.parse_args()
    for k, on in list(ON.items()):
        ON[k] = on != getattr(a, f"{'without' if on else 'with'}_{k}")
    if a.form:
        sec = 60 / BPM * 4
        for i, name in enumerate(NAMES):
            b, e = TOP[i], TOP[i + 1]
            print(f'{i + 1:2d}  bars {b + 1:3d}-{e:3d}  {int(b * sec) // 60}:{b * sec % 60:05.2f}  {name:38s} ' +
                  ' '.join(f'{k} {ring_at(k, b):.2f}>{ring_at(k, e - 1):.2f}' for k in list(SHAPE) + (['plate'] if ON['plate'] else []) if e > enters(k) and not any(x <= b < y for x, y in [OUT_OF.get(k, (0, 0))])))
        if ON['sympathy']:
            print(f"    the strings nobody plays ({' '.join(n for n, _, _ in SYMPATHY['strings'])}): let go across bars {TOP[6] + 1}-{TOP[7]}, open to bar {TOP[8]}, stopped by bar {TOP[8] + QUICK}, let go in bar {BARS}" + (f"; let go again while the wood closes, bars {TOP[11] + 1}-{TOP[12]}" if ON['close'] else '') + ('; they hear the string as well as the wood and the air' if ON['own'] else '') + (f"; {' and '.join(SKIN['strings'])} hear the skin too" if ON['skin'] else ''))
        if ON['drop']:
            print('    the stick is let go too: ' + ', '.join(f'the {k} in bar {dropped(k)[0] + 1} on sixteenth {dropped(k)[1] + 1} ({(BAR - dropped(k)[1]) * 60000 / BPM / 4:.0f} ms to the one)' for k in things() if dropped(k)) + f"; {DROP['bounces']} bounces, each {DROP['share']} of the one before")
        if ON['empty'] and ON['drop']:
            print('    the hand is empty: once its stick is dropped a thing plays nothing more in that bar')
        if blown():
            print(f"    the air overblows: after its stroke in bar {blown()[0] + 1} on sixteenth {blown()[1] + 1}, harmonics {' '.join(str(h) for h in BLOW['harmonics'])} of its pipe, a sixteenth each, to the one")
        if ON['long'] and ON['flue']:
            print("    the air's breath trails off: a second, slower breath behind the first")
        print(f'{BARS} bars, {BARS * sec:.1f} s; strokes: ' + ', '.join(f'{k} {len(v)}' for k, v in build().items()))
    else:
        a.out.write_text(dump(bench() if a.bench else song(build())))
