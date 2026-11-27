#!/usr/bin/env python3
"""Escapement (Chirpers 11), track 1 (chirper-zero): GIVE OR TAKE. The opener; the slot's word is TIME.

TWO DECKS. Deck A is the grid and never moves: a bass drum on the four, one click on the off-beats, a bass, later a clap. Deck B is
everything else (a sixteenth-note noise click, two wooden tocks in a Euclidean five, a dub chord), and a hand is on it:
it is pushed ahead of the grid and dragged back behind it, the way a DJ rides one record against another. Nothing on
deck B is ever placed by hand: every event has a place on its own record, and the record's position against the grid
is one function of time, d(t), in beats. Where d rises the deck runs fast, and what has a pitch on it goes sharp, as a
record does (12 log2(1 + d') semitones, written as a lane from the same function). So the tempo you hear moving is
real on one deck and false on the other, and the bass drum says which.

THE FORM IS ARITHMETIC: a row is ROW bars; SECTIONS lists, for each section, its rows, which parts play, and the hand:
its kind, its reach in beats and its period in bars. Every start, every event and every lane point comes from those.

  the grid      nothing moves: the kick, the click, deck B's sixteenths straight
  give          the hand begins: deck B breathes against the grid (the reach grows)
  take          the chord comes in on deck B and goes sharp and flat with it
  no ruler      deck A stops. Now deck B's tempo is the only tempo, and it is moving. The kick comes back where it always was.
  both          both decks; the hand's period is a bar and a half, so the push walks through the bar
  the nudge     deck B is taken a whole sixteenth ahead and let back: at the far point it fits again, one step out
  locked        the hand comes off: one tempo, the fullest groove
  out           the parts leave; deck A's click is last

v1 is the SKELETON (26 Nov; the brief: "any version at all opens the groove to it; then keep finessing"): the whole
shape standing, with few sounds.

v2 (26 Nov): DECK B IS A RECORD, AND A RECORD HAS ITS OWN BASS DRUM (C11T1_KNOCK=0 takes it out). From the second
row of "take" deck B plays a bass drum of its own on its own four, with its bass taken out (a high-pass at 315 Hz
on the lane `low`: the incoming record with the low EQ killed, as it is mixed), so the two drums are heard against
each other: one drum when the hand is off, a flam when it leans, a gallop when it pushes. Before "no ruler" the grid
click stops, and in the last bar the BASS IS SWAPPED: deck B's drum gets its lows as deck A's drum stops. For twelve
bars the only bass drum on the record is deck B's, and its tempo is the one that moves. Then deck A's drum comes
back where it always was, the two gallop, and deck B's bass is taken out again over two bars.

v3 (26 Nov): THE STOP (C11T1_STOP=0 writes v2). The record ENDS: in "out" deck B plays on (its chord and its
drum with it), deck A's drum leaves, and at the eleventh bar DECK B IS SWITCHED OFF. Its speed falls in a straight line to nothing over two bars, the same d(t)
as every push before it (d' = -u), so its strokes come further and further apart and everything with a pitch on it
sinks, as a platter does with the motor off. One bar of record takes those two bars, and the next never comes.
The grid click, which never moved, counts four more bars alone.
(Tried in this round and taken out: letting deck B's drum's bass back in for "locked", so the two strike as one big
drum. The two drums' lows are not in step: with it the master had 6 dB LESS under 70 Hz in "locked", not more.)

v4 (26 Nov): WHAT THE TWO DECKS MAKE WHEN THEY MEET (C11T1_MEET=0 writes v3). "Locked" has its reward, and it is
the next song's. Least Common (t2, chirper-one) is three clicks in cycles of 3, 5 and 7 sixteenths, and where two
of them meet there is a ping: 3 with 5 a D, 3 with 7 a B flat, 5 with 7 an F. Between two meetings of all three
(105 sixteenths) the pings make a tune of twelve notes, the same forwards and backwards, that nobody wrote. Here,
from the bar the two decks lock, that tune is heard on Least Common's own vibraphone bar, with nobody playing the
three clicks: the meetings without the clicks. All three meet on the first beat of "locked" (the three notes at
once: F, B flat, D, the top of this song's chord), and the tune goes round four times, through "out", and plays
its last note half a bar before deck B's motor goes off: 26 bars, which is four sixteenths short of one of
Least Common's pages (420). So the first song ends on the tune the second is made of, a track early.

v5 (26 Nov): THE LOOP, AND ZENO'S BAR (C11T1_ROLL=0 writes v4). The hand's last trick before the decks lock, and
the oldest one a DJ has for it: the last four bars of "the nudge" deck B is put in a LOOP, and the loop is cut in
half, and in half again. A bar of its first beat over and over (four times); a bar of its first half beat (eight);
a bar of its first quarter (sixteen: every sixteenth is now the record's first instant, its drum, its click and its
tock). Nothing is placed by hand: the record's position is still one function of time, now a sawtooth, and deck A
plays straight on under it. THE LAST BAR IS ZENO'S: each loop gets sixteen turns and is half as long as the one
before, so the sixteen take two beats, then one, then a half, a quarter ... and the bar line is reached only in the
limit. The loop is now shorter than a sixteenth and holds one thing, the first instant of deck B's drum, and
in the bar's last beat it stops being a rhythm: sixty-six strokes a second is a NOTE. It is the tempo's own note
(124 to the minute is 2.07 Hz; thirty-two, sixty-four, a hundred and twenty-eight times that ...: a C, 19 cents
sharp), and it goes up an octave every time the loop is halved, five octaves in that one beat, faster and faster,
with deck A's drum taken out from under it.
It never arrives. The loop is let go on the first beat of "locked", and the record is where it would have been.

v6 (26 Nov): ZENO'S RECORD (C11T1_STRETCH=0 takes it out: v5). The song has slowed deck B three ways: the hand
(its pitch sags), the stop (its pitch falls five octaves), and now a fourth thing a hand cannot do: the STRETCH.
In a new row, "the stretch" (after "both"), deck B's record goes at half speed and ITS PITCH DOES NOT MOVE. It is
done the way a machine does it: the record is cut into grains a sixteenth long, and each grain is played whole,
at full speed, but the next grain starts only half a sixteenth further into the record. So everything on the
record is played twice: every stroke becomes two strokes, half a sixteenth apart, and the second is where the
stroke would be on a record going at half speed. Two bars on, the record goes at a quarter of its speed: four
strokes for each, three quarters of a sixteenth apart, a ratchet that runs up to the place and lands on it. Then
an eighth: eight strokes, seven eighths apart. Then a sixteenth: sixteen strokes, fifteen sixteenths apart, which
is very nearly deck A's grid: a click that starts a sixteenth late and is 8 ms less late every stroke until it
is ON the grid, and the dub chord with it, a sliver that grows into a chord.
The record gets through a bar, then half a bar, then a quarter, then an eighth: in eight bars it has gone a bar
and seven eighths, and going on like this it would never reach the end of its second bar. That is Zeno's other
paradox (the runner who must first go half the way). The loop in "the nudge" is where it ends
up: a record stretched for ever is one grain, repeated. The hand lets go on the first beat of "the nudge" and
the record is where it would have been.
Deck A's drum, bass and clap stand back for these eight bars (the song's one breakdown): only its click stays,
the ruler the stretched record is read against. With deck A's drum under it the stretch was hard to find, and
the scorer's form stood on one cut at the very end of the song (STRETCH_OVER says what plays under it).

v7 (26 Nov): THE REWIND (C11T1_REWIND=0 takes it out: v6). Deck B has been pushed, dragged, looped, stretched
and stopped; it has never gone BACKWARDS. In the last bar of "both" a hand spins the record back: it starts at
two and a third times its speed, the wrong way, and the platter's drag slows it (its speed falls by e every two
beats) until, a bar later, it has gone back over exactly the bar just heard and is at a bar line, turning at a
third of its speed. Everything on that bar is heard again, last stroke first: crowded and more than an octave
high at the start (a record's pitch is its speed, whichever way it turns), then thinning and falling, through
the right pitch before the bar is half over, to a sixth and an octave below it. Deck A plays straight through.
AND THEN THE STRETCH BEGINS FROM WHERE THE RECORD STOPPED. Until now "the stretch" took up the record's next two
bars. It now starts on the bar the rewind went back over: time goes backwards for a bar, and then Zeno's record
crawls forward over the same ground, a bar, half a bar, a quarter, an eighth, and never gets to the end of the
bar the rewind took the place of. The hand lets go on the first beat of "the nudge" and the record is where it
would have been. (REWIND_BACK 2, two bars back in one, was tried: the stretch then falls on an odd bar and an
even one, loses the dub chord that grows from a sliver at its end, and the song scored less: refused.)

v8 (26 Nov): THE OTHER SPEED (C11T1_FAST=0 takes it out: v7). A deck has a switch as well as a hand. Deck B has
been pushed, dragged, looped, stretched, spun back and stopped, always from the speed it was cut at. For the
last FAST_BARS bars of "locked" (the two decks have just agreed, for four bars) the switch is flipped to the
other speed, and deck B plays FOUR BARS FOR EVERY THREE of deck A's. A record's pitch is its speed: four to three
is a perfect fourth, so everything on deck B is a fourth up: its G minor is C minor, over deck A's G. And its bar
is three beats long by deck A's clock: its bar lines fall on the grid's beats 1, 4, 3, 2 of four bars running
and are back on a bar line every third bar: four against three, bar against bar, with nothing written but one
number. Twelve bars of the grid: the record plays sixteen (its eight-bar round of chords twice), and they meet
four times. Then the switch goes back as "out" begins, and the hand puts the record where it would have been.
(A real deck's two speeds are 33 1/3 and 45, twenty-seven to twenty: a fourth and a fifth of a tone, meeting
every twenty bars. This one's are four to three, so that the two are in tune and meet.)
BENCHED (seed 0; v7 that day 96.55): six bars of it 96.45, nine 96.30, twelve 96.27. What it costs is the scorer's
rhythm term, which counts strokes off the sixteenths as loose (66.3 to 63.2), and an edge of its last cut; its
own polymeter reading, which carries no weight, goes from 30 to 70 at twelve bars and to 40 at six. Twelve is
kept: four against three needs its four meetings. C11T1_FAST_BARS=6 is the short one.

v9 (26 Nov): THE ECHO IS ON THE RECORD (C11T1_ECHO=0 takes it out: v8). The dub chord's echo was the one thing
of deck B's that the hand could not move: it is a delay on a bus, a dotted eighth of the GRID's, so in "no
ruler", where deck A is gone and the record swings from 100 to 148 to the minute, the chord's echoes went on
ticking at 124: a ruler. From v9, in "no ruler", the echo is pressed into the record: each chord's four echoes
are notes on deck B's own clock, a dotted eighth of the RECORD's beats apart, so they crowd together as the
hand pushes and string out as it drags, and each is as sharp or as flat as the record is when it SOUNDS (the
bus's echoes kept the pitch the chord was struck at). The chords there are on a track of their own with no
send (`stab-b`); the echoes are `echo-1` to `echo-4`, each at the level and the dullness the bus's echo had
(fitted on a bench of one chord: within 0.5 dB; the bus's fifth echo is 26 dB under its first and is not made).
ALSO: the spin back's pitch lane has a point every sixty-fourth of a beat (it had one a sixteenth): the engine
bows a lane where it falls (chirp-eco's bench), and v7's spun-back tock read up to 64 cents flat.

v10 (26 Nov): THE NEEDLE STICKS (C11T1_STICK=0 takes it out: v9). Every way deck B has left the grid so far has
been a HAND or a SWITCH: a push, a drag, a stop, a spin, a speed. This one is an accident, and it is the one
everybody who has owned a record knows. One turn of a platter at 33 is 1.81 seconds, and at this tempo that is
FIFTEEN sixteenths: a turn of the groove holds a bar less its last sixteenth. In the second row of "both" (bars
73 to 80, 2:19 to 2:35) the needle does not cross into the next turn: it jumps back and plays the same turn
again, with a pop, eight times. Deck A does not know. So against the grid the record's bar is a sixteenth short
and arrives a sixteenth EARLIER every time round: 15 against 16, by accident.
What that does, with no note changed: the wooden tock's five strokes (0 3 6 9 12 of sixteen) lose their long
last gap and become dead even, every three sixteenths, for seven and a half bars (three against the beat's
four); deck B's drum goes round deck A's, a sixteenth earlier a turn: with it, just before it, half way
between (so the two drums are eighths), just after, with it again, and round once more; the dub chord creeps
back from the sixth sixteenth to the last of the bar before. Half a bar from the end of the row a hand puts the
needle on (the eighth pop) and the record is where the grid is.
The turn is in the RECORD's beats, not the grid's: the platter is still being pushed and dragged (the hand of
"both" is on it), so each time round takes as long as the platter takes, and the tock and chord are as sharp
or flat as they were going to be. Only what the needle reads has changed.
The pop is its own track and patch (`pop`, `gt-pop`: 16 ms of dull noise): one at every jump.

v11 (26 Nov): THE HAND ON THE RECORD (C11T1_SCRATCH=0 takes it out: v10). Until now the hand has pushed the
platter and dragged it. Now it takes hold of the record and RUBS it: a scratch. Under the needle is deck B's dub
chord. The hand goes round like a crank: the record goes forward over the chord's first tenth of a second and
back again, there and back in a beat, then in half a beat, then in a quarter. TIME GOES FORWARD AND BACKWARD
UNDER THE NEEDLE, and a record's sound is its speed: its pitch is the speed, and so is its loudness (a
pickup gives the groove's speed, not its place). So nothing here is a sample: the chord is held, and three
lanes are the physics. The pitch is the hand's speed (12 log2 of it). The loudness is the hand's speed times
what the record holds at the place under the needle (the chord, loud at its start and dying). The brightness is
what the record holds there too (the chord's filter, open at its start and closing).
So each rub is two sounds. FORWARD: the chord's start goes under the needle on the sixteenth, at exactly the
record's own speed (the chord at its own pitch), the hand quickens (the chord bends up a tritone: the crank's
fastest is root two times the record's speed) and slows to a stop inside the chord: silence. BACKWARD: the
same tenth of a second the other way: quiet and dull first, swelling and brightening up to the chord's START,
where it is cut off dead: a sound that ends with its own attack. Then the hand turns round in the silence
before the chord and brings the start under the needle again on the next beat.
Deck B plays nothing else in that bar: the hand has it. Two bars: the last bar of "take" (bar 48, 1:31, into
"no ruler") and the bar before the needle sticks (bar 72, 2:17): two rubs a beat long, two of half a beat,
four of a quarter. Track `hand`, patch `gt-rub` (the dub chord's own saws and filter, held), dry.

v12 (26 Nov): ONE RECORD AT FIVE SPEEDS (C11T1_SPEEDS=0 takes it out: v11). The law of this song is the law of a
record: slow it and everything on it is lower and longer by the same ratio. Deck B's tock has been pushed,
dragged, looped, stretched, spun back, switched to the other speed, stuck and rubbed: always one deck. Now the
same record is on FIVE decks at once, each at half the speed of the one before: 1, 1/2, 1/4, 1/8, 1/16. Half the
speed is an octave down and twice as long, so the tock's five strokes a bar are also five strokes in two bars an
octave down, in four bars two octaves down, in eight bars three, and in sixteen bars four octaves down, where
the wooden pip is a low bar on G2 that takes sixteen times as long to die. All five start together on the first beat of
"give" (bar 17, 0:31) and the slowest gets through its one bar of the record as the section ends (bar 32).
That is a canon by proportion (a mensuration canon: Ockeghem's, and Part's Cantus is this with bells), and here
the record law writes it: nothing is composed for the four slower decks. Each is deck B's own motor geared down,
so it gives and takes with deck B, and its pitch bends with deck B's (the same lane).

v13 (26 Nov): THE OTHER RECORD HAS A BASSLINE TOO (C11T1_BASSB=0 takes it out: v12). Deck B's record has had a
click, tocks, a chord and a drum; it has never had a bass, and a record without a bass is not a record. Now it
has one: four strokes a bar on the sixteenth BEFORE each beat (the "a" of the beat), D2 D2 C3 and a turn (Bb2 or
D2): the other record is in D minor, a fifth from deck A's G minor, which is the nearest key there is and the one
a DJ mixes into. It is cut into deck B's record, so everything that has happened to that record happens to it:
it gives and takes, goes sharp and flat with the platter, is stretched, looped, stuck, rubbed past, and sinks
with the motor at the end.

v14 (27 Nov): THE CUE (C11T1_CUE=0 takes it out: v13). Before a DJ lets a record into the room they hear it alone,
in ONE ear, in a headphone held against the head, and get it into step by hand. Until now deck B simply arrived
at bar 9, in step, as no record ever has. Now it is CUED: from bar 3 its sixteenths are in the LEFT ear only, small
and thin and dry (a headphone, not a room), and they are OUT: half a sixteenth late, the worst there is, every
stroke falling between two of the grid's. The hand corrects, and over-corrects, half as far every half bar: late
by 60 ms, early by 30, late by 15, early by 8, 4, 2, 1 (the error is D0 cos(pi u / 2) 2 ** (-u / 2), u in beats).
Two bars to find it; from bar 5 it is within 4 ms and stays, four bars held in one ear against the grid in both.
At bar 9 the fader opens and the same sixteenths are in the room, where they have always come in.
It is TIME (two tempos becoming one, heard before it is allowed to be heard) and it is SPACE (the only thing in
this song that is in one ear). On one speaker it is a small tick that flams against the click and then does not.

v15 (27 Nov): THE RECORD IS HEARD A TURN BEFORE IT PLAYS (C11T1_PRE=0 takes it out: v14). On a real record a
loud stroke presses on the wall of the groove next to it, so the needle finds a faint print of that stroke one
turn of the platter BEFORE it reaches the stroke itself (pre-echo: on many LPs the first loud bar can be heard,
very quietly, in the silence a turn before it starts). This song has said since v8 that one turn of deck A's
record is 15 sixteenths (33 turns a minute at 124). So every stroke of deck A's bass drum, the loudest thing on
it, is now heard twice: once small and dull, 15 sixteenths early, and then itself.
The arithmetic: 15 sixteenths early is one sixteenth LATE in the bar before. So while the drum plays four to
the bar the print falls a sixteenth after each stroke and cannot be told from an echo. It gives itself away
only where the drum starts or stops, and there it is plainly a bar early:
  - the drum rests in "no ruler" and comes back at bar 61: its four prints are heard in bar 60, alone;
  - the same before bar 97 (in bar 96) and before bar 113 (in bar 112);
  - and the prints STOP a bar before the drum does: bars 48, 88, 111 and 136 have the drum and no print.
Nothing new is played: the same patch, the same strokes, moved a turn and kept between 250 Hz and 3 kHz (what
is left of a drum a groove away is its knock, not its weight).

v16 (27 Nov): THE CLOCK ON THE WALL (C11T1_CLOCK=0 takes it out: v15). In "no ruler" deck A's drum and click
are gone and deck B wanders from 100 to 148 to the minute: nothing in the room keeps time. Except the clock.
It ticks once a second, at every whole second of the song (93 to 123: thirty-one ticks), tick and tock by
turns, and it takes no notice of the music: at 124 to the minute fifteen seconds are thirty-one beats, so
against the grid each tick is a fifteenth of a beat later than two beats after the last one. It is exactly on
a beat once every fifteen seconds: at 1:45.0 (bar 55, the second beat, where there is no drum to meet) and at
2:00.0, which is the first beat of bar 63, where deck A's drum has just come back: the clock and the drum
agree once, for one stroke, and the clock goes on being right about something else.
A tick is three sounds, as a watchmaker's timing machine reads them: the tooth unlocks, gives its push, and
drops on the other pallet (14, 8 and 0 ms before the second; the drop is the loud one). Tick and tock are the
two pallets: the same grain of noise at 3.6 and 3.0 kHz. The album is called Escapement: this is one.
"""
import json
import math
import os

OUT = os.environ.get("C11T1_OUT", os.path.join(os.path.dirname(__file__), "..", "..", "..", "songs", "chirpers11-t1.yaml"))
BPM = 124
BEATS = 4                      # beats in a bar
ROW = 8                        # bars in a row
STEP = 0.25                    # a sixteenth, in beats
ROOT = "G"

KNOCK_ON = {"knock"} if os.environ.get("C11T1_KNOCK", "1") != "0" else set()   # v2: deck B's own bass drum
STOP = os.environ.get("C11T1_STOP", "1") != "0" and bool(KNOCK_ON)               # v3: the record switched off in "out"
MEET = os.environ.get("C11T1_MEET", "1") != "0" and STOP                        # v4: Least Common's meeting tune from "locked" to the stop
MEET_CYCLES = (3, 5, 7)        # Least Common's three clicks, in sixteenths
MEET_NOTE = {(3, 5): "D5", (3, 7): "Bb4", (5, 7): "F4"}   # the ping two of them make when they meet (t2's own notes)
ROLL = os.environ.get("C11T1_ROLL", "1") != "0" and MEET                        # v5: the loop, and Zeno's bar
STRETCH = os.environ.get("C11T1_STRETCH", "1") != "0" and ROLL                   # v6: Zeno's record
STRETCH_BY = (2, 4, 8, 16)     # how many times slower deck B's record goes in "the stretch" ...
STRETCH_BARS = 2               # ... for this many bars each
GRAIN = 1                      # sixteenths: the piece of record that is played whole each time
STRETCH_OVER = set(os.environ.get("C11T1_STRETCH_OVER", "tick").split(",")) - {""}   # what of deck A plays under it: its click, the ruler, and nothing else
REWIND = os.environ.get("C11T1_REWIND", "1") != "0" and STRETCH                  # v7: the rewind
REWIND_BARS = 1                # the bars before "the stretch" in which deck B is spun back ...
REWIND_BACK = int(os.environ.get("C11T1_REWIND_BACK", "1"))   # ... and the bars of record it goes back over: it stops on a bar line, and the stretch starts from there
REWIND_TAU = 2.0               # beats in which its speed falls by e: the hand's pull, then the platter's drag
FAST = os.environ.get("C11T1_FAST", "1") != "0" and REWIND                      # v8: the other speed
FAST_BY = 4 / 3                # deck B's speed with its switch at the other speed: four bars for three, and a perfect fourth
FAST_BARS = int(os.environ.get("C11T1_FAST_BARS", "12"))   # the last bars of "locked" for which the switch is there (threes: they meet every third bar)
ECHO = os.environ.get("C11T1_ECHO", "1") != "0" and FAST                         # v9: the echo is on the record
ECHO_IN = os.environ.get("C11T1_ECHO_IN", "no ruler")   # the section in which it is
ECHO_BEATS = 0.75              # the echo's time: a dotted eighth, of the record's own beats
ECHO_GAINS = (-35.6, -40.9, -48.2, -55.6)   # dB: each echo's level, fitted to the bus's (send -7 dB after the chord's -23, feedback 0.45): within 0.5 dB on a bench of one chord
ECHO_TONES = (4000, 2800, 2000, 1500)       # Hz: ... and its low-pass (the bus's echoes lose a little more top each time round)
ECHO_HALL = "-7.36dB"          # ... and its share of the hall (the bus's is mix 0.3: 0.3 to 0.7)
FINE = 16 if ECHO else 1       # lane points to a sixteenth while the record is spun back
STICK = os.environ.get("C11T1_STICK", "1") != "0" and ECHO                       # v10: the needle sticks
STICK_IN = ("both", 8)         # the section, and the bar of it on whose first beat the turn that sticks begins
STICK_TURN = 15                # sixteenths of the record in one turn of the platter: 33 turns a minute is 1.81 s, which at 124 is 3.75 beats
STICK_TURNS = 8                # times that turn is heard: once as the record plays it, then with a pop each time the needle jumps back; after the last a hand puts the needle on
STICK_POP = os.environ.get("C11T1_STICK_POP", "4dB")     # the pop's level: alone it is then 6 dB under deck A's click (at -14 dB it was 27 under: dull noise this short has little in it)
ROLL_AT = 12                   # the bar of "the nudge" at which deck B is put in a loop (it is let go on the first beat of "locked")
ROLL_WHOLE = 3                 # the first loops (a beat, a half, a quarter) get a bar each
ROLL_TURNS = 16                # ... and every loop after them this many turns, each half as long as the last: Zeno's bar
ROLL_TOP = 4000                # Hz: the last loop is the last whose turns come slower than this
ROLL_BARE = 1                  # bars before "locked" in which deck A's bass drum stands back
ROLL_VEL = 0.9                 # the velocity of every turn in Zeno's bar
STOP_AT = 10                   # the bar of "out" at which deck B's motor goes off
STOP_BARS = 2                  # the bars its platter takes to stop
# name, rows, the parts that play, the hand: (kind, reach in beats, period in bars, bars over which it comes on and off)
SECTIONS = [
    ("the grid",  2, {"kick", "tick", "hat"},                         ("none", 0.0, 1, 2)),   # the hat from the second row (ENTER)
    ("give",      2, {"kick", "tick", "hat", "tock", "sub"},          ("breathe", 0.05, 2, 2)),
    ("take",      2, {"kick", "tick", "hat", "tock", "sub", "stab"} | KNOCK_ON,  ("breathe", 0.08, 2, 2)),   # deck B's drum from the second row; the click gone for the last four bars
    ("no ruler",  2, {"hat", "tock", "stab"} | KNOCK_ON,                         ("breathe", 0.5, 4, 4)),
    ("both",      3, {"kick", "tick", "hat", "tock", "sub", "stab", "clap"} | KNOCK_ON,  ("breathe", 0.08, 1.5, 2)),
]
if STRETCH:
    SECTIONS.append(("the stretch", len(STRETCH_BY) * STRETCH_BARS // ROW, STRETCH_OVER | {"hat", "tock", "stab"} | KNOCK_ON, ("stretch", 0.0, 1, 2)))
SECTIONS += [
    ("the nudge", 2, {"kick", "tick", "hat", "tock", "sub", "stab", "clap"} | KNOCK_ON,  ("nudge", 0.25, 4, 2)),
    ("locked",    2, {"kick", "tick", "hat", "tock", "sub", "stab", "clap"} | KNOCK_ON,  ("none", 0.0, 1, 2)),
    ("out",       2, {"kick", "tick", "hat", "tock"} | ({"stab", "knock"} if STOP else set()), ("stop", 0.0, STOP_AT, STOP_BARS) if STOP else ("none", 0.0, 1, 2)),
]
RETURN = 4                     # in "no ruler", the kick alone comes back for the last RETURN bars
LEAVE = {"out": [("kick", 8), ("hat", 12), ("tock", 14)]}   # the bar (of the section) from which each part is gone
ENTER = {"the grid": [("hat", ROW)]}                         # ... and from which each part is there
if KNOCK_ON:
    LEAVE["take"] = [("tick", 12)]                           # the ruler's marks go first, then (at "no ruler") the ruler
    ENTER["take"] = [("knock", ROW)]
if STOP:
    LEAVE["out"] = [("kick", 8)]                             # deck B is not taken out: it stops
if ROLL and ROLL_BARE:
    LEAVE["the nudge"] = [("kick", 2 * ROW - ROLL_BARE)]     # Zeno's bar has no bass drum under it
SWAP = 1                       # bars before "no ruler" over which deck B's drum gets its bass
BACK = 2                       # bars after deck A's drum returns over which it loses it again
KILL = 3.3                     # octaves above 32 Hz at which deck B's drum is cut when its bass is out (315 Hz)
LIFT = 7                       # dB by which what is left of it is turned up while its bass is out (it was 14 dB under the mix without)


def starts():
    out, b = [], 0
    for name, rows, parts, hand in SECTIONS:
        out.append((name, b, rows * ROW, parts, hand)); b += rows * ROW
    return out, b


SECS, BARS = starts()
TOTAL = BARS * BEATS           # the song's length in beats


def section_at(t):
    bar = t / BEATS
    for name, b0, n, parts, hand in SECS:
        if b0 <= bar < b0 + n:
            return name, b0, n, parts, hand
    return SECS[-1]


def d(t):
    """Deck B's position against the grid at grid time t (beats): how far ahead of the grid its record is."""
    if t < 0 or t >= TOTAL:
        return 0.0
    name, b0, n, parts, (kind, reach, period, ramp) = section_at(t)
    if kind in ("none", "stretch"):                            # a stretched record is slow and not flat: its speed against the grid is not the hand's
        return 0.0
    u = t / BEATS - b0                                         # bars into the section
    env = max(0.0, min(1.0, u / ramp, (n - u) / ramp))          # the hand comes on and comes off
    if kind == "breathe":
        return reach * env * math.sin(2 * math.pi * u / period)
    if kind == "nudge":
        if ROLL:                                               # the hand is off by the bar the loop starts
            env = max(0.0, min(1.0, u / ramp, (ROLL_AT - u) / ramp))
        return reach * env * (1 - math.cos(2 * math.pi * u / period)) / 2
    if kind == "stop":                                         # period = the bar the motor goes off, ramp = the bars the platter takes
        x, w = (u - period) * BEATS, ramp * BEATS              # beats since the motor went off; the platter's time in beats
        return 0.0 if x <= 0 else -x * x / (2 * w) if x < w else -w / 2 - (x - w)
    raise ValueError(kind)


def stop_at():
    """(the beat at which deck B's motor goes off, the platter's time in beats), or None."""
    for name, b0, n, parts, (kind, reach, period, ramp) in SECS:
        if kind == "stop":
            return (b0 + period) * BEATS, ramp * BEATS
    return None


def when(b):
    """The grid time at which deck B's record reaches its own beat b: t + d(t) = b. None if it never does."""
    st = stop_at()
    if st and b > st[0]:
        ts, w = st
        if b - ts >= w / 2:                                    # the record stops w / 2 beats after the motor does
            return None
        return ts + w - math.sqrt(w * w - 2 * w * (b - ts))    # x - x^2 / 2w = b - ts
    t = b
    for _ in range(40):
        t = b - d(t)
    return t


def speed(t, h=1 / 64):
    """Deck B's speed against the grid at grid time t (1 = the same tempo)."""
    return 1 + (d(t + h) - d(t - h)) / (2 * h)


def rewind():
    """The spin back: (the grid beat it starts on, the beats it lasts, where the record is when it starts, its speed then, backwards), or None."""
    b1 = next((sec[1] for sec in SECS if sec[0] == "the stretch"), None)
    if not REWIND or b1 is None:
        return None
    t0, T = (b1 - REWIND_BARS) * BEATS, REWIND_BARS * BEATS
    p0 = t0 + d(t0)
    back = p0 - (b1 - REWIND_BARS - REWIND_BACK) * BEATS
    return t0, T, p0, back / (REWIND_TAU * (1 - math.exp(-T / REWIND_TAU)))


def rewind_speed(t):
    """How fast deck B is turning backwards at grid time t (1 = its own tempo), or None when it is not."""
    rw = rewind()
    if rw is None or not rw[0] <= t < rw[0] + rw[1]:
        return None
    return rw[3] * math.exp(-(t - rw[0]) / REWIND_TAU)


def rewound(part, steps):
    """What the record holds between where the spin back starts and where it stops, each stroke when the record passes it going back."""
    t0, T, p0, s0 = rewind()
    lo = p0 - s0 * REWIND_TAU * (1 - math.exp(-T / REWIND_TAU))
    out = []
    for bar in range(int(lo // BEATS), int(p0 // BEATS) + 1):
        if plays(part, bar):
            for s, p, n, v in steps(bar):
                b = bar * BEATS + s * STEP
                if lo + 1e-6 < b <= p0:
                    x = -REWIND_TAU * math.log(1 - (p0 - b) / (s0 * REWIND_TAU))
                    out.append(note(t0 + x, p, min(n * STEP / (s0 * math.exp(-x / REWIND_TAU)), 2.0), v))
    return sorted(out, key=lambda q: q["at"])


def fast_window():
    """The grid beats between which deck B's switch is at the other speed, or None."""
    sec = next((x for x in SECS if x[0] == "locked"), None)
    if not FAST or sec is None or FAST_BARS <= 0:
        return None
    return (sec[1] + sec[2] - FAST_BARS) * BEATS, (sec[1] + sec[2]) * BEATS


def forced(t):
    """Deck B's speed at grid time t when a hand or the switch has it (the spin back, the other speed), or None."""
    back = rewind_speed(t)
    if back is not None:
        return back
    fw = fast_window()
    return FAST_BY if fw and fw[0] <= t < fw[1] else None


def sped(steps):
    """What the record plays with the switch at the other speed: from the bar it is on, FAST_BY bars for every bar of the grid."""
    t0, t1 = fast_window()
    b0, out = int(t0 // BEATS), []
    for i in range(int(math.ceil((t1 - t0) / BEATS * FAST_BY - 1e-9))):
        for s, p, n, v in steps(b0 + i):
            x = (i * BEATS + s * STEP) / FAST_BY
            if x < t1 - t0 - 1e-9:
                out.append(note(t0 + x, p, min(n * STEP / FAST_BY, t1 - t0 - x), v))
    return out


def speed_st(t):
    """Semitones deck B is sharp by at grid time t."""
    return 12 * math.log2(max(speed(t), 0.03))


def spd_lane():
    """Semitones a record on deck B is sharp or flat by, from its speed: one point a sixteenth, only where it moves."""
    pts, last, fine = [["0b", 0]], 0.0, False
    for i in range(int(TOTAL / STEP) + 1):
        t = i * STEP
        back = forced(t)                                     # a record's pitch is its speed, whichever way it turns, and whatever turns it
        v = round(12 * math.log2(max(speed(t) if back is None else back, 0.03)), 3)   # a stopped record has no pitch: the lane rests five octaves down
        if v != last or (pts and i and pts[-1][1] != v):
            if pts[-1][0] != f"{(i - 1) * STEP:g}b" and i and not fine:
                pts.append([f"{(i - 1) * STEP:g}b", last])
            edge = forced(t - STEP) if i else None
            if back is not None and edge is None and i:          # the hand takes the record on the beat, not over the sixteenth before it
                pts.append([f"{t - 0.01:g}b", last])
            if back is None and edge is not None:                # ... and lets it go on the beat
                pts.append([f"{t - 0.01:g}b", round(12 * math.log2(max(forced(t - 0.01), 0.03)), 3)])
            pts.append([f"{t:g}b", v])
        fine = False
        if FINE > 1 and rewind_speed(t) is not None:             # between sixteenths a falling lane is bowed: give the spin back points enough to be straight
            for j in range(1, FINE):
                if rewind_speed(t + j * STEP / FINE) is not None:
                    pts.append([f"{t + j * STEP / FINE:g}b", round(12 * math.log2(max(rewind_speed(t + j * STEP / FINE), 0.03)), 3)])
                    fine = True
        last = v
    pts.append([f"{TOTAL:g}b", 0])
    return pts


def echo_span():
    """The grid beats between which the dub chord's echo is on the record, or None."""
    sec = next((x for x in SECS if x[0] == ECHO_IN), None) if ECHO else None
    return (sec[1] * BEATS, (sec[1] + sec[2]) * BEATS) if sec else None


def echo_notes(k):
    """The k-th echo of every chord struck in that section: on deck B's clock, k * ECHO_BEATS of the record's beats after the chord."""
    lo, hi = echo_span()
    out = []
    for bar in range(int(lo // BEATS), int(hi // BEATS)):
        if plays("stab", bar):
            for s, p, n, v in STAB(bar):
                b = bar * BEATS + s * STEP + k * ECHO_BEATS
                t, end = when(b), when(b + n * STEP)
                if t is not None and t < TOTAL:
                    out.append(note(t, p, (end if end is not None else t + n * STEP) - t, v))
    return out


SCRATCH = os.environ.get("C11T1_SCRATCH", "1") != "0" and STICK                   # v11: the hand on the record (a scratch)
SCR_AT = tuple((x.split("/")[0], int(x.split("/")[1])) for x in os.environ.get("C11T1_SCR_AT", "take/15,both/7").split(",") if x)   # the section, and the bar of it for which the hand has the record
SCR_PHRASE = ((0, 1.0, 2), (2, 0.5, 2), (3, 0.25, 4))   # (the beat of the bar a run of rubs begins on, the beats one rub takes there and back, how many)
SCR_PHI = math.pi / 4          # how far round the crank is when the chord's start goes under the needle: a rub sounds for (1 - PHI/pi) of its time
SCR_PEAK = math.sqrt(2)        # the record's fastest under the hand, in its own speed: with PHI an eighth of a turn the chord's start goes under the needle at exactly the record's speed
SCR_AMP = (0.15, 0.28 / 3)     # what the record holds: the chord's loudness dies to this share of its start, with this time constant (s of record): gt-stab's d 280ms, s 0.15
SCR_FLT = (0.08, 0.2 / 3)      # ... and its filter's envelope the same way: gt-stab's d 200ms, s 0.08
SCR_OFF = -80.0                # dB: the lane where the needle is before the chord, and where the hand is off
SCR_GAIN = os.environ.get("C11T1_SCR_GAIN", "-26dB")   # the held chord's fader (the dub chord's own is -23: benched alone at that, a rub was 3 to 7 dB over the chord's own stroke and 6 dB over it in peak)


SPEEDS = os.environ.get("C11T1_SPEEDS", "1") != "0" and SCRATCH                 # v12: one record at five speeds (a canon by proportion)
SPEEDS_IN = ("give", 0, 16)                            # the section, and the bars of it over which the slower decks play: the slowest gets through one bar of the record in them
SPEEDS_K = (1, 2, 3, 4)                                # deck k is at 1 / 2^k of deck B's speed: k octaves down, 2^k times as long
SPEEDS_GAIN = tuple(float(x) for x in os.environ.get("C11T1_SPEEDS_GAIN", "-13,-13,-4,-5").split(","))   # dB: each slower deck's fader (the tock's own is -8.5). At -13 all four give the same power (the record's law), and in the master the two lowest could not be read apart from the sub and the drum, which are on their notes: they are lifted 9 and 8 dB
SPEEDS_PAN = (-0.225, -0.15, -0.075, 0.0)              # the tock is at -0.3: each slower deck a step nearer the middle


BASSB = os.environ.get("C11T1_BASSB", "1") != "0" and SPEEDS                    # v13: deck B's record has a bassline
CUE = os.environ.get("C11T1_CUE", "1") != "0" and BASSB                         # v14: the cue (deck B in one ear before it is let into the room)
CLOCK = os.environ.get("C11T1_CLOCK", "1") != "0" and os.environ.get("C11T1_PRE", "1") != "0" and CUE    # v16: the clock on the wall (one tick a second, in "no ruler")
CLOCK_IN = "no ruler"                                  # the section it is heard in: the one with nothing else that keeps time
CLOCK_EVERY = 1                                        # seconds between ticks; a tick at every whole multiple of it, counted from the start of the song
CLOCK_PARTS = ((0.014, 0.35), (0.008, 0.5), (0.0, 1.0))    # a tick's three sounds (seconds before the second, velocity): unlock, impulse, drop
CLOCK_HZ = (3600, 3000)                                # the two pallets: tick, tock (out of the 2.2 kHz band, where this song is already 6 dB over the album)
CLOCK_PAN = 0.5                                        # on the wall to the right (the cue was in the left ear)
CLOCK_ROOM = "-10dB"
CLOCK_GAIN = os.environ.get("C11T1_CLOCK_GAIN", "-20dB")
PRE = os.environ.get("C11T1_PRE", "1") != "0" and CUE                           # v15: the record is heard a turn before it plays (pre-echo)
PRE_OF = "kick"                                        # the part that prints through: the loudest thing on deck A's record
PRE_TURN = STICK_TURN                                  # sixteenths in one turn of deck A's platter (15: the turn that sticks in "both")
PRE_BAND = (250, 3000)                                 # Hz: what is left of the stroke a groove away
PRE_GAIN = os.environ.get("C11T1_PRE_GAIN", "-18.5dB")
CUE_BARS = (2, 8)                                                              # the bars (0-based) in which it is heard: from bar 3 to the bar before the hat comes in
CUE_OUT = 0.125                                                                # beats it starts late by: half a sixteenth (60.5 ms), the furthest a sixteenth-note part can be from the grid
CUE_HALF = 2.0                                                                 # beats in which the hand's error halves and changes side
CUE_PAN = -1.0                                                                 # one ear
CUE_GAIN = os.environ.get("C11T1_CUE_GAIN", "-5dB")                             # set in the whole song's master: at -9 dB a stroke read 8 dB under the room's hat in the same ear and only 7 dB over what the music leaves between its strokes (over 1.5 kHz)
BASSB_MODE = os.environ.get("C11T1_BASSB_MODE", "swap")                        # swap: it is heard where deck A's bass is out ; full: wherever deck B's record plays from "no ruler" on
BASSB_IN = {"swap": ("no ruler", "the stretch", "out"), "full": ("no ruler", "both", "the stretch", "the nudge", "locked", "out")}[BASSB_MODE]
BASSB_GAIN = os.environ.get("C11T1_BASSB_GAIN", "-15dB")                       # at -10 it was louder than everything else in "no ruler" put together (measured): 5 dB down
BASSB_STEPS = lambda bar: [(3, "D2", 2, 0.9), (7, "D2", 2, 0.8), (11, "C3", 2, 0.85), (15, "Bb2" if bar % 2 else "D2", 1, 0.75)]   # the sixteenth before each beat
if BASSB:
    for _s in SECS:
        if _s[0] in BASSB_IN:
            _s[3].add("bassb")                                                     # it is on deck B's record in these sections
    LEAVE.setdefault("out", []).append(("bassb", 12))                              # ... and not in the last four bars
    if BASSB_MODE == "swap" and rewind() and "the stretch" in BASSB_IN:            # the stretch begins with the spin back, which is the last bar of "both": the bass is on the record there too
        _b = next(x for x in SECS if x[0] == "both")
        _b[3].add("bassb"); ENTER.setdefault("both", []).append(("bassb", _b[2] - REWIND_BARS))


def speeds_span():
    """The bars between which the slower decks play, or None."""
    sec = next((x for x in SECS if x[0] == SPEEDS_IN[0]), None) if SPEEDS else None
    return (sec[1] + SPEEDS_IN[1], sec[1] + SPEEDS_IN[2]) if sec else None


def speeds_notes(k):
    """Deck k's strokes: the record's own (TOCK), from the span's first bar, each sounding when deck B's record is 2^k times as far into the span."""
    b0, b1 = speeds_span()
    out = []
    for bar in range(b0, b1):
        for st, p, n, v in TOCK(bar):
            x = (bar - b0) * BEATS + st * STEP                   # beats into the span, on the record
            if x * 2 ** k >= (b1 - b0) * BEATS:
                continue
            t, end = when(b0 * BEATS + x * 2 ** k), when(b0 * BEATS + min((x + n * STEP) * 2 ** k, (b1 - b0) * BEATS))
            out.append({"at": round(t, 5), "len": round(end - t, 4), "pitch": p[:-1] + str(int(p[-1]) - k), "vel": v})
    return out


def scratch_spans():
    """The beats at which the hand takes deck B's record, for a bar each."""
    if not SCRATCH:
        return []
    return [(sec[1] + bar) * BEATS for nm, bar in SCR_AT for sec in SECS if sec[0] == nm]


def rubs():
    """(the beat a rub begins on, the beats it takes there and back) of every rub."""
    return [(s0 + b + i * T, T) for s0 in scratch_spans() for b, T, n in SCR_PHRASE for i in range(n)]


def hand_at(t):
    """(the record's speed under the hand, in its own speed; seconds of record the needle is past the chord's start) at beat t; None where the hand is off."""
    for t0, T in rubs():
        if t0 - 1e-9 <= t < t0 + T - 1e-9:
            th = 2 * math.pi * (t - t0) / T + SCR_PHI                  # the crank
            a = SCR_PEAK * T * 60 / BPM / (2 * math.pi)                # its arm, in seconds of record
            return SCR_PEAK * math.sin(th), a * (math.cos(SCR_PHI) - math.cos(th))
    return None


def hand_lanes():
    """The three lanes of the scratch: the pitch (semitones: the speed), the loudness (dB: the speed times what the record holds there), the brightness (the chord's filter envelope there)."""
    def val(t):
        h = hand_at(t)
        if h is None:
            return 0.0, SCR_OFF, 0.0
        v, p = h
        st = round(12 * math.log2(max(abs(v), 0.03)), 3)
        if p < -1e-9:
            return st, SCR_OFF, 0.0                                    # the needle is in the silence before the chord
        p = max(p, 0.0)
        amp = SCR_AMP[0] + (1 - SCR_AMP[0]) * math.exp(-p / SCR_AMP[1])
        return st, round(max(SCR_OFF, 20 * math.log10(max(abs(v) * amp, 1e-6))), 2), round(SCR_FLT[0] + (1 - SCR_FLT[0]) * math.exp(-p / SCR_FLT[1]), 4)
    ts = set()
    for s0 in scratch_spans():
        ts |= {round(s0 + i / 64, 6) for i in range(BEATS * 64 + 1)}
    for t0, T in rubs():
        ts |= {round(t0 - 0.002, 6), round(t0 + T * (1 - SCR_PHI / math.pi) + 0.002, 6)}   # the start goes under the needle at once, and the cut is dead
    lanes = ([["0b", 0.0]], [["0b", SCR_OFF]], [["0b", 0.0]])
    for t in sorted(ts):
        for lane, v in zip(lanes, val(t)):
            lane.append([f"{t:.6f}".rstrip("0").rstrip(".") + "b", v])
    for lane, v in zip(lanes, (0.0, SCR_OFF, 0.0)):
        lane.append([f"{TOTAL:g}b", v])
    return lanes


def stick():
    """(the record's beat at which the turn that sticks begins, the turn in beats, the times it is heard), or None."""
    sec = next((x for x in SECS if x[0] == STICK_IN[0]), None) if STICK else None
    return ((sec[1] + STICK_IN[1]) * BEATS, STICK_TURN * STEP, STICK_TURNS) if sec else None


def stuck(steps):
    """What the needle reads while it is stuck: the same turn of the record, STICK_TURNS times; each stroke sounds when the platter gets it there."""
    p0, turn, n = stick()
    out = []
    for j in range(n):
        for s, p, ln, v in steps(int(p0 // BEATS)):
            if s * STEP < turn:
                q = p0 + j * turn + s * STEP
                out.append(note(when(q), p, when(q + min(ln * STEP, turn - s * STEP)) - when(q), v))
    return out


def pops():
    """The pop each time the needle jumps back, and when the hand puts it on."""
    p0, turn, n = stick()
    return [note(when(p0 + j * turn), "C4", STEP / 2, 0.9) for j in range(1, n + 1)]


def plays(part, bar):
    name, b0, n, parts, hand = section_at(bar * BEATS)
    if name == "no ruler" and part == "kick" and bar >= b0 + n - RETURN:
        return True
    for p, gone in LEAVE.get(name, []):
        if p == part and bar >= b0 + gone:
            return False
    for p, there in ENTER.get(name, []):
        if p == part and bar < b0 + there:
            return False
    return part in parts


def low_lane():
    """How much of deck B's drum's bass is cut (1 all, 0 none): in for "no ruler" until deck A's drum is back."""
    pts = [["0b", 1]]
    for name, b0, n, parts, hand in SECS:
        if name == "no ruler":
            pts += [[f"{(b0 - SWAP) * BEATS:g}b", 1], [f"{b0 * BEATS:g}b", 0], [f"{(b0 + n - RETURN) * BEATS:g}b", 0], [f"{(b0 + n - RETURN + BACK) * BEATS:g}b", 1]]
    pts.append([f"{TOTAL:g}b", 1])
    return pts


def note(at, pitch, length, vel):
    return {"at": round(at, 4), "len": round(length, 4), "pitch": pitch, "vel": round(vel, 3)}


def deck_a(part, steps):
    """steps: (step in the bar, pitch, length in steps, velocity). On the grid."""
    out = []
    for bar in range(BARS):
        if plays(part, bar):
            out += [note(bar * BEATS + s * STEP, p, n * STEP, v) for s, p, n, v in steps(bar)]
    return out


def roll_stages():
    """Every loop of the roll: (the grid beat it starts on, its length in beats, its turns)."""
    if not ROLL:
        return []
    t = (next(s[1] for s in SECS if s[0] == "the nudge") + ROLL_AT) * BEATS
    out, loop = [], 1.0
    for i in range(ROLL_WHOLE):
        out.append((t, loop, int(round(BEATS / loop)))); t += BEATS; loop /= 2
    while BPM / 60 / loop <= ROLL_TOP:
        out.append((t, loop, ROLL_TURNS)); t += ROLL_TURNS * loop; loop /= 2
    return out


def roll_window():
    """The grid beats between which deck B is in a loop, or None."""
    st = roll_stages()
    return (st[0][0], next(s[1] for s in SECS if s[0] == "locked") * BEATS) if st else None


def grains():
    """The stretch: (the grid beat a grain starts on, where in the record it starts, in sixteenths from the section's first)."""
    b0 = next((s[1] for s in SECS if s[0] == "the stretch"), None)
    if b0 is None:
        return []
    out, t, pos = [], b0 * BEATS, 0.0
    for by in STRETCH_BY:
        for _ in range(int(STRETCH_BARS * BEATS / (GRAIN * STEP))):
            out.append((t, pos)); t += GRAIN * STEP; pos += GRAIN / by
    return out


def stretch_window():
    """The grid beats between which deck B is stretched, or None."""
    g = grains()
    return (g[0][0], g[-1][0] + GRAIN * STEP) if g else None


def stretched(steps):
    """What the grains hold: every stroke whose start is inside a grain, where it is in the grain, cut off at the grain's end."""
    g = grains()
    b0 = int(g[0][0] // BEATS) - (REWIND_BARS + REWIND_BACK if rewind() else 0)   # from v7: from where the spin back left the record
    far = int(math.ceil((g[-1][1] + GRAIN) / 16))
    record = [(16 * i + s, p, n, v) for i in range(far) for s, p, n, v in steps(b0 + i)]
    return [note(t + (s - pos) * STEP, p, min(n, GRAIN - (s - pos)) * STEP, v)
            for t, pos in g for s, p, n, v in record if -1e-9 <= s - pos < GRAIN - 1e-9]


def deck_b(part, steps):
    """The same, on deck B's record: each event sounds when the record gets to it."""
    out, win, sw = [], roll_window(), stretch_window()
    fw = fast_window()
    sk = stick()
    rw = rewind()
    if rw:
        sw = (rw[0], sw[1])                                    # the record is not going forward from the spin back to the end of the stretch
    for bar in range(BARS):
        if plays(part, bar):
            for s, p, n, v in steps(bar):
                b = bar * BEATS + s * STEP
                t = when(b)
                if sk and sk[0] <= b < sk[0] + sk[1] * sk[2]:               # the needle never reads these: it is stuck in the turn before them
                    continue
                if t is not None and any(s0 <= t < s0 + BEATS for s0 in scratch_spans()):   # the hand has the record
                    continue
                if t is not None and 0 <= t < TOTAL and not (win and win[0] <= t < win[1]) and not (sw and sw[0] <= t < sw[1]) and not (fw and fw[0] <= t < fw[1]):   # the record never gets to what the loop skips
                    end = when(b + n * STEP)
                    out.append(note(t, p, (end if end is not None else t + 4 * n * STEP) - t, v))
    if win and plays(part, int(win[0] // BEATS)):
        # in the loop: what the record holds between the loop's start and its end, once a turn, cut off where the loop ends
        for t0, loop, turns in roll_stages():
            if loop >= STEP:
                out += [note(t0 + r * loop + s * STEP, p, min(n * STEP, loop - s * STEP), v)
                        for r in range(turns) for s, p, n, v in steps(int(win[0] // BEATS)) if s * STEP < loop]
        out.sort(key=lambda x: x["at"])
    if sk and plays(part, int(sk[0] // BEATS)):
        out += stuck(steps)
        out.sort(key=lambda x: x["at"])
    if rw and plays(part, int(rw[0] // BEATS)):
        out += rewound(part, steps)
    if sw and plays(part, int(sw[0] // BEATS)):
        out += stretched(steps)
        out.sort(key=lambda x: x["at"])
    if fw and plays(part, int(fw[0] // BEATS)):
        out += sped(steps)
        out.sort(key=lambda x: x["at"])
    return out


def roll_notes():
    """Zeno's bar: the loops shorter than a sixteenth hold the first instant of deck B's drum and nothing else."""
    return [{"at": round(t0 + r * loop, 6), "len": round(loop, 6), "pitch": ROOT + "1", "vel": ROLL_VEL}
            for t0, loop, turns in roll_stages() if loop < STEP for r in range(turns)]


def euclid(k, n, rot=0):
    """k strokes spread as evenly as they will go over n steps."""
    return sorted({(i * n // k + rot) % n for i in range(k)})


KICK = lambda bar: [(s, ROOT + "1", 1, 0.95 if s == 0 else 0.9) for s in (0, 4, 8, 12)]
TICK = lambda bar: [(s, "G5", 1, 0.72 if s in (2, 10) else 0.62) for s in (2, 6, 10, 14)]
HAT = lambda bar: [(s, "C6", 0.5, (0.55, 0.34, 0.62, 0.4)[s % 4] + (0.06 if (s * 5 + bar * 3) % 7 == 0 else 0)) for s in range(16)]
FIVE = euclid(5, 16)
TOCK = lambda bar: [(s, ("G6", "Bb6", "G6", "D7", "Bb6")[i] if bar % 4 != 3 else ("G6", "Bb6", "D7", "F7", "D7")[i], 1, 0.8 if i in (0, 3) else 0.62) for i, s in enumerate(FIVE)]
SUB = lambda bar: [(2, "G2", 1.6, 0.9), (7, "G2", 1, 0.8), (10, "Bb2" if bar % 2 else "G2", 1.6, 0.9)] + ([(14, "F2", 1.6, 0.85)] if bar % ROW == ROW - 1 else [(14, "D3", 1, 0.75)] if bar % 2 else [])
CLAP = lambda bar: [(4, "C4", 1, 0.8), (12, "C4", 1, 0.86)]
KNOCK = lambda bar: [(s, ROOT + "1", 1, 0.92 if s == 0 else 0.86) for s in (0, 4, 8, 12)]   # deck B's four
CHORDS = [("G3", "Bb3", "D4", "F4"), ("G3", "Bb3", "D4", "F4"), ("G3", "A3", "D4", "F4"), ("Eb3", "G3", "Bb3", "D4")]


def STAB(bar):
    ch = CHORDS[(bar // 2) % len(CHORDS)]
    out = [(6, p, 1.5, 0.85) for p in ch]
    if bar % 2:
        out += [(13, p, 1, 0.7) for p in ch]
    return out


def meet_notes():
    """Least Common's meetings, counted from the bar the decks lock to the bar deck B's motor goes off: a ping where
    two of the three cycles meet, the three notes at once where all three do. Nobody plays the cycles."""
    b0 = next(s[1] for s in SECS if s[0] == "locked")
    b1 = next(s[1] for s in SECS if s[0] == "out") + STOP_AT
    out = []
    for s in range((b1 - b0) * 16):
        hit = tuple(c for c in MEET_CYCLES if s % c == 0)
        if len(hit) == 3:
            out += [note((b0 * 16 + s) * STEP, p, 2 * STEP, 0.85) for p in ("F4", "Bb4", "D5")]
        elif len(hit) == 2:
            out.append(note((b0 * 16 + s) * STEP, MEET_NOTE[hit], 2 * STEP, 0.75))
    return out


PATCHES = {
    "gt-kick": {"about": "Give or Take's bass drum (chirper-zero, 26 Nov): the engine's machine kick, short and dry, resting on the song's G; deck A.",
                "play": {"vel_sens": 0.3},
                "synth": {"layers": [{"type": "machine", "machine": {"part": "kick", "decay": "280ms", "click": 0.65, "drive": 0.35, "punch": 22, "punch_time": "34ms"}}],
                          "filters": ["hp cutoff=28"], "amp": {"a": "0.1ms", "d": "0s", "s": 1, "r": "1s"}}},
    "gt-meet": {"about": "Give or Take's ping (chirper-zero, 26 Nov, v4): Least Common's `lc-ping` (chirper-one) rebuilt here under this song's name: a vibraphone bar with no motor, half a second long. It plays t2's meeting tune once the two decks are locked.",
                "play": {"event_stable": True, "vel_sens": 0.5},
                "synth": {"layers": [{"type": "modal", "modes": "vibes", "decay": "650ms", "bright": 0.55, "strike": 0.3}], "amp": {"a": "0.3ms", "d": "900ms", "s": 0, "r": "200ms"}}},
    "gt-knock": {"about": "Give or Take's second bass drum (chirper-zero, 26 Nov, v2): deck B's own, a little shorter and clickier than deck A's, through a high-pass on the lane `low` (32 Hz to 315 Hz: the low EQ of the incoming record, killed until the bass is swapped); its pitch follows deck B's speed.",
                 "play": {"vel_sens": 0.3},
                 "synth": {"layers": [{"type": "machine", "machine": {"part": "kick", "decay": "220ms", "click": 0.8, "drive": 0.3, "punch": 20, "punch_time": "30ms"}}],
                           "pitch": {"value": 0, "mod": [{"src": "auto.spd", "amount": 1}]},
                           "filters": [{"kind": "hp", "cutoff": {"value": 32, "mod": [{"src": "auto.low", "amount": KILL}]}, "q": 0.7}], "amp": {"a": "0.1ms", "d": "0s", "s": 1, "r": "1s"}}},
    "gt-roll": {"about": f"Give or Take's loop (chirper-zero, 26 Nov, v5): deck B's bass drum as it is in \"the nudge\" (its bass out: a high-pass at {32 * 2 ** KILL:.0f} Hz), let go the instant its note ends, so that a note as long as the loop is the loop: the first instant of the drum, over and over. Zeno's bar.",
                "play": {"vel_sens": 0.3},
                "synth": {"layers": [{"type": "machine", "machine": {"part": "kick", "decay": "220ms", "click": 0.8, "drive": 0.3, "punch": 20, "punch_time": "30ms"}}],
                          "filters": [{"kind": "hp", "cutoff": round(32 * 2 ** KILL), "q": 0.7}], "amp": {"a": "0.1ms", "d": "0s", "s": 1, "r": "1ms"}}},
    "gt-tick": {"about": "Give or Take's grid click (chirper-zero, 26 Nov): the machine's rim, one voice, high and dry; deck A's ruler marks.",
                "play": {"vel_sens": 0.5},
                "synth": {"layers": [{"type": "machine", "machine": {"part": "rim", "decay": "35ms"}}], "amp": {"a": "0.1ms", "d": "0s", "s": 1, "r": "300ms"}}},
    "gt-hat": {"about": "Give or Take's sixteenth click (chirper-zero, 26 Nov): a 14 ms burst of white noise between 6 and 12.5 kHz; deck B.",
               "play": {"vel_sens": 0.7},
               "synth": {"layers": ["white"], "filters": [{"kind": "hp", "cutoff": 6000, "q": 0.8}, "peak cutoff=8500 q=2 gain=4dB", "lp cutoff=12500"],
                         "amp": {"a": "0.1ms", "d": "14ms", "s": 0, "r": "8ms", "curve": 5}}},
    "gt-clap": {"about": "Give or Take's clap (chirper-zero, 26 Nov): the machine's clap, three bursts, short; deck A.",
                "play": {"vel_sens": 0.4},
                "synth": {"layers": [{"type": "machine", "machine": {"part": "clap", "bursts": 3, "decay": "140ms"}}], "amp": {"a": "0.1ms", "d": "0s", "s": 1, "r": "400ms"}}},
    "gt-tock": {"about": "Give or Take's tock (chirper-zero, 26 Nov): a wooden bar on the modal layer (after Common Measure's clave), whose pitch follows deck B's speed (auto.spd, semitones).",
                "play": {"vel_sens": 0.5},
                "synth": {"layers": [{"type": "modal", "modes": "glock", "bright": 0.9, "damp": 0.25, "decay": "160ms", "strike": 0.5, "tilt": 0.0}],
                          "pitch": {"value": 0, "mod": [{"src": "auto.spd", "amount": 1}]}, "amp": {"a": "0.2ms", "d": "260ms", "s": 0, "r": "40ms"}}},
    "gt-stab": {"about": "Give or Take's dub chord (chirper-zero, 26 Nov): three saws and a square through a short filter envelope, dry (the echo is a bus); its pitch follows deck B's speed (auto.spd, semitones), as a chord on a nudged record does.",
                "synth": {"layers": ["saw unison=3 detune=0.15 spread=0.6", "square level=-8dB"], "env": {"f": {"a": "1ms", "d": "200ms", "s": 0.08, "r": "100ms"}},
                          "pitch": {"value": 0, "mod": [{"src": "auto.spd", "amount": 1}]},
                          "filters": [{"kind": "lp", "cutoff": {"value": 600, "mod": [{"src": "env.f", "amount": 2.4}, {"src": "vel", "amount": 1}]}, "q": 1.6}],
                          "amp": {"a": "1ms", "d": "280ms", "s": 0.15, "r": "150ms"}}},
}


def cue_err(u):
    """Beats the cued record is LATE by, u beats after the hand takes it: it over-corrects, half as far every CUE_HALF beats."""
    return CUE_OUT * math.cos(math.pi * u / CUE_HALF) * 2 ** (-u / CUE_HALF)


def clock_span():
    """(first bar, bar after the last) of the section the clock is heard in, from 0."""
    return next((b0, b0 + n) for name, b0, n, parts, hand in SECS if name == CLOCK_IN)


def clock_seconds():
    """The whole seconds of the song (multiples of CLOCK_EVERY) that fall inside the span."""
    b0, b1 = clock_span(); bar_s = BEATS * 60 / BPM
    return [k * CLOCK_EVERY for k in range(int(b0 * bar_s / CLOCK_EVERY) + 1, int(math.ceil(b1 * bar_s / CLOCK_EVERY))) if b0 * bar_s <= k * CLOCK_EVERY < b1 * bar_s]


def clock_notes(pallet):
    """The ticks (pallet 0) or the tocks (pallet 1): every other second, three sounds each."""
    return [{"at": round((sec - early) * BPM / 60, 5), "len": 0.05, "pitch": "C6", "vel": vel} for sec in clock_seconds()[pallet::2] for early, vel in CLOCK_PARTS]


def pre_notes(src):
    """The source's strokes one turn of the platter early (those that would fall before the record starts are not there)."""
    d = PRE_TURN * STEP
    return [{**n, "at": round(n["at"] - d, 4)} for n in src if n["at"] - d >= 0]


def pre_bars(src):
    """(bars, from 1, that have a print and no stroke; bars that have a stroke and no print)."""
    has = {int(n["at"] // BEATS) for n in src}; pr = {int(n["at"] // BEATS) for n in pre_notes(src)}
    return sorted(b + 1 for b in pr - has), sorted(b + 1 for b in has - pr)


def cue_notes():
    """Deck B's sixteenths (the hat's own strokes) as the DJ hears them before the fader opens."""
    out = []
    for bar in range(*CUE_BARS):
        for st, pitch, ln, vel in HAT(bar):
            r = bar * BEATS + st * STEP
            out.append({"at": round(r + cue_err(r - CUE_BARS[0] * BEATS), 5), "len": 0.125, "pitch": pitch, "vel": round(vel, 3)})
    return out


def song():
    lane = spd_lane()
    pump = {"type": "pump", "on": "kick", "depth": "-5dB", "attack": "2ms", "release": "180ms", "curve": 0.7}
    doc = {
        "about": "Chirpers - Escapement, track 1 by chirper-zero: GIVE OR TAKE. Two decks. Deck A (the bass drum, one click, the sub) is the grid and never moves. Deck B (the sixteenth click, the tocks, the dub chord) has a hand on it: pushed ahead of the grid and dragged back, and what has a pitch on it goes sharp and flat with its speed, as a record does. Generated by compose/chirpers11/src/chirpers11-t1.py.",
        "tempo": BPM,
        "ceiling": "-1dB",
        "loudness": -10.5,
        "seed": 1,
        "tail": "2s",
        "length": f"{TOTAL}b",
        "event_stable": True,
        "patches": PATCHES,
        "buses": {
            "room": {"fx": ["reverb kind=room decay=0.5s mix=1 predelay=6ms", "hp cutoff=400"]},
            "dub": {"fx": [{"type": "delay", "time": "3/16", "feedback": 0.45, "mix": 1, "tone": 2200}, "hp cutoff=350", "reverb kind=hall decay=2.4s mix=0.3"]},
        },
        "master": {"fx": [{"type": "eq", "bands": ["hp cutoff=30", "peak cutoff=120 q=0.7 gain=3dB"]}, {"type": "compressor", "threshold": "-18dB", "ratio": 2, "attack": "20ms", "release": "160ms", "makeup": "0dB"}]},
        "tracks": [
            {"name": "kick", "patch": "gt-kick", "gain": "-4.5dB", "pan": 0.0, "notes": deck_a("kick", KICK)},
            {"name": "tick", "patch": "gt-tick", "gain": "-3dB", "pan": 0.0, "sends": {"room": "-12dB"}, "notes": deck_a("tick", TICK)},
            {"name": "sub", "patch": "sub-sine params.grit=0.8", "gain": "-5dB", "pan": 0.0, "fx": [pump], "notes": deck_a("sub", SUB)},
            {"name": "clap", "patch": "gt-clap", "gain": "-5dB", "pan": 0.0, "sends": {"room": "-9dB"}, "notes": deck_a("clap", CLAP)},
            {"name": "hat", "patch": "gt-hat", "gain": "0dB", "pan": 0.25, "sends": {"room": "-16dB"}, "notes": deck_b("hat", HAT)},
            {"name": "tock", "patch": "gt-tock", "gain": "-8.5dB", "pan": -0.3, "sends": {"room": "-10dB", "dub": "-18dB"}, "auto": {"spd": {"points": lane}}, "notes": deck_b("tock", TOCK)},
            {"name": "stab", "patch": "gt-stab", "gain": "-23dB", "pan": 0.1, "fx": [pump], "sends": {"dub": "-7dB"}, "auto": {"spd": {"points": lane}}, "notes": deck_b("stab", STAB)},
        ],
    }
    if KNOCK_ON:
        doc["tracks"].append({"name": "knock", "patch": "gt-knock", "gain": "-5dB", "pan": 0.0, "fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.low", "amount": LIFT}]}}],
                              "auto": {"spd": {"points": lane}, "low": {"points": low_lane()}}, "notes": deck_b("knock", KNOCK)})
        doc["about"] = doc["about"].replace("Deck B (the sixteenth click, the tocks, the dub chord) has a hand on it", "Deck B (the sixteenth click, the tocks, the dub chord, and from v2 a bass drum of its own with its bass taken out) has a hand on it")
    else:
        del PATCHES["gt-knock"]
    if ROLL:
        doc["tracks"].append({"name": "roll", "patch": "gt-roll", "gain": "3dB", "pan": 0.0, "sends": {"room": "-14dB"}, "notes": roll_notes()})
        doc["about"] = doc["about"].replace(" Generated by", " From v5 the last four bars before the decks lock are a loop of deck B cut in half and in half again, and the last bar is Zeno's: sixteen turns of each loop, each half as long, until the rhythm is a note going up an octave at a time. Generated by")
    else:
        del PATCHES["gt-roll"]
    if STRETCH:
        doc["about"] = doc["about"].replace(" Generated by", " From v6, in \"the stretch\", deck B goes at a half, a quarter, an eighth and a sixteenth of its speed and its pitch does not move: it is cut into grains a sixteenth long, each played whole, so every stroke is heard two, four, eight, sixteen times. Generated by")
    if echo_span():
        lo, hi = echo_span()
        k0 = next(i for i, t in enumerate(doc["tracks"]) if t["name"] == "stab")
        st = doc["tracks"][k0]
        inside = [n for n in st["notes"] if lo <= n["at"] < hi]
        st["notes"] = [n for n in st["notes"] if not lo <= n["at"] < hi]
        doc["tracks"].append({"name": "stab-b", "patch": "gt-stab", "gain": st["gain"], "pan": st["pan"], "fx": st["fx"], "auto": {"spd": {"points": lane}}, "notes": inside})   # the chord there: no send to the grid's echo
        doc["buses"]["tape"] = {"fx": ["reverb kind=hall decay=2.4s mix=1"]}
        for k, (g, f) in enumerate(zip(ECHO_GAINS, ECHO_TONES), 1):
            doc["tracks"].append({"name": f"echo-{k}", "patch": "gt-stab", "gain": f"{g:g}dB", "pan": st["pan"], "fx": [f"lp cutoff={f:g}", "hp cutoff=350"], "sends": {"tape": ECHO_HALL},
                                  "auto": {"spd": {"points": lane}}, "notes": echo_notes(k)})
        doc["about"] = doc["about"].replace(" Generated by", " From v9, in no ruler, the dub chord's echo is on the record and not on the grid: its echoes are a dotted eighth of the record's own beats apart, so they crowd and string out with the hand, and each is as sharp or flat as the record is when it sounds. Generated by")
        assert "From v9" in doc["about"]
    if scratch_spans():
        hand, loud, bright = hand_lanes()
        rub = json.loads(json.dumps(PATCHES["gt-stab"]))
        rub["about"] = "Give or Take's dub chord under the hand (chirper-zero, 26 Nov, v11): the chord's own saws and filter, HELD: its pitch is the hand's speed (auto.hand, semitones), its filter is opened by what the record holds under the needle (auto.bright), and the track's gain (auto.loud) is the speed times the chord's loudness there."
        rub["play"] = {**rub.get("play", {}), "gate": 1}
        rub["synth"].pop("env", None)
        rub["synth"]["pitch"] = {"value": 0, "mod": [{"src": "auto.hand", "amount": 1}]}
        rub["synth"]["filters"][0]["cutoff"]["mod"] = [{"src": "auto.bright", "amount": 2.4}, {"src": "vel", "amount": 1}]
        rub["synth"]["amp"] = {"a": "1ms", "d": "10ms", "s": 1, "r": "10ms"}
        PATCHES["gt-rub"] = rub
        doc["tracks"].append({"name": "hand", "patch": "gt-rub", "gain": SCR_GAIN, "pan": 0.1,
                              "fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.loud", "amount": 1}]}}],
                              "auto": {"hand": {"points": hand, "curve": 0}, "loud": {"points": loud, "curve": 0}, "bright": {"points": bright, "curve": 0}},
                              "notes": [note(s0, p, BEATS, 0.85) for s0 in scratch_spans() for p in CHORDS[(int(s0 // BEATS) // 2) % len(CHORDS)]]})   # dry
        doc["about"] = doc["about"].replace(" Generated by", " From v11 the hand takes hold of deck B's record and rubs it, twice, a bar each: the dub chord goes forward under the needle and back, there and back in a beat, half a beat, a quarter; its pitch and its loudness are the hand's speed, and the backward half swells up to the chord's start and is cut off there. Generated by")
        assert "From v11" in doc["about"]
    if BASSB:
        PATCHES["gt-bass-b"] = {"about": "Give or Take's second bass (chirper-zero, 26 Nov, v13): deck B's record's own: a plain tone with a little saw over it, plucked (the filter opens for a moment at each stroke); its pitch follows deck B's speed.",
                                "play": {"vel_sens": 0.5},
                                "synth": {"layers": ["sine", "saw level=-10dB"], "env": {"f": {"a": "1ms", "d": "140ms", "s": 0.1, "r": "60ms"}},
                                          "pitch": {"value": 0, "mod": [{"src": "auto.spd", "amount": 1}]},
                                          "filters": [{"kind": "lp", "cutoff": {"value": 220, "mod": [{"src": "env.f", "amount": 2.2}]}, "q": 1.0}],
                                          "amp": {"a": "2ms", "d": "160ms", "s": 0.6, "r": "50ms"}}}
        doc["tracks"].append({"name": "bass-b", "patch": "gt-bass-b", "gain": BASSB_GAIN, "pan": 0.0, "auto": {"spd": {"points": lane}}, "notes": deck_b("bassb", BASSB_STEPS)})      # dry
        doc["about"] = doc["about"].replace(" Generated by", " From v13 deck B's record has a bassline of its own (D2 D2 C3 and a turn, on the sixteenth before each beat; a fifth from deck A's key), heard where deck A's bass is out: alone with its record in no ruler, stretched with it, and sinking with the platter at the end. Generated by")
        assert "From v13" in doc["about"]
    if speeds_span():
        ms = lambda x, k: f"{float(x[:-2]) * 2 ** k:g}ms"
        for i, k in enumerate(SPEEDS_K):
            tk = PATCHES["gt-tock"]
            PATCHES[f"gt-tock-{2 ** k}"] = {"about": f"Give or Take's tock at 1/{2 ** k} of its speed (chirper-zero, 26 Nov, v12): the same wooden bar as a record gives it back slowed: played {k} octave(s) down, and every time in it (the bar's ring, the stroke's rise, fall and release) {2 ** k} times as long. Its pitch follows deck B's speed as the tock's does.",
                                            "play": dict(tk["play"]),
                                            "synth": {**tk["synth"], "layers": [{**tk["synth"]["layers"][0], "decay": ms(tk["synth"]["layers"][0]["decay"], k)}],
                                                      "amp": {**tk["synth"]["amp"], **{q: ms(tk["synth"]["amp"][q], k) for q in ("a", "d", "r")}}}}
            doc["tracks"].append({"name": f"tock-{2 ** k}", "patch": f"gt-tock-{2 ** k}", "gain": f"{SPEEDS_GAIN[i]:g}dB", "pan": SPEEDS_PAN[i], "sends": {"room": "-10dB"},
                                  "auto": {"spd": {"points": lane}}, "notes": speeds_notes(k)})
        doc["about"] = doc["about"].replace(" Generated by", " From v12 the same record is on five decks in give, each at half the speed of the one before: the tock's five strokes a bar are also five in two bars an octave down, in four bars two octaves down, in eight three and in sixteen four, where it is a slow bell on G2: a canon by proportion that the record's own law writes. Generated by")
        assert "From v12" in doc["about"]
    if stick():
        PATCHES["gt-pop"] = {"about": "Give or Take's pop (chirper-zero, 26 Nov, v10): the needle jumping a groove wall: 16 ms of dull noise, 150 Hz to 1.8 kHz; deck B.",
                             "play": {"vel_sens": 0.3},
                             "synth": {"layers": ["white"], "filters": ["hp cutoff=150", "lp cutoff=1800"], "amp": {"a": "0.1ms", "d": "16ms", "s": 0, "r": "5ms", "curve": 4}}}
        doc["tracks"].append({"name": "pop", "patch": "gt-pop", "gain": STICK_POP, "pan": 0.1, "notes": pops()})      # dry, where the record's chord is
        doc["about"] = doc["about"].replace(" Generated by", " From v10, in the second row of both, the needle sticks: one turn of the platter is fifteen sixteenths of the record, and deck B plays that turn eight times with a pop at each jump, so its bar comes a sixteenth earlier each time against deck A (15 against 16): the tock goes dead even, deck B's drum goes round deck A's, and half a bar before the row ends a hand puts the needle on. Generated by")
        assert "From v10" in doc["about"]
    if fast_window():
        doc["about"] = doc["about"].replace(" Generated by", " From v8 deck B's switch is flipped to the other speed for the last twelve bars of locked: it plays four bars for every three of deck A's, a perfect fourth up, and the two meet every third bar. Generated by")
        assert "From v8" in doc["about"]
    if REWIND:
        doc["about"] = doc["about"].replace(" Generated by", " From v7 the last bar before the stretch is a spin back: deck B goes backwards over the bar just heard, more than twice too fast and slowing, last stroke first, its pitch falling with its speed; the stretch then crawls forward from where it stopped. Generated by")
        assert "From v7" in doc["about"]
    if CUE:
        PATCHES["gt-cue"] = {"about": "Give or Take's cue (chirper-zero, 27 Nov, v14): deck B's sixteenth click as a headphone held to one ear lets it out: the same 14 ms burst of noise, but between 1.8 and 7 kHz with a small speaker's ring at 3.2 kHz; dry, in one ear.",
                             "play": {"vel_sens": 0.7},
                             "synth": {"layers": ["white"], "filters": [{"kind": "hp", "cutoff": 1800, "q": 0.8}, "peak cutoff=3200 q=2 gain=6dB", "lp cutoff=7000"], "amp": {"a": "0.1ms", "d": "14ms", "s": 0, "r": "8ms", "curve": 5}}}
        doc["tracks"].append({"name": "cue", "patch": "gt-cue", "gain": CUE_GAIN, "pan": CUE_PAN, "notes": cue_notes()})      # dry: a headphone, not a room
        doc["about"] = doc["about"].replace(" Generated by", " From v14 deck B is cued before it is let in: from bar 3 its sixteenths are in the left ear only, small and dry, half a sixteenth late, and the hand corrects and over-corrects, half as far every half bar, until from bar 5 they are in step; at bar 9 the fader opens. Generated by")
        assert "From v14" in doc["about"]
    if MEET:
        doc["tracks"].append({"name": "meet", "patch": "gt-meet", "gain": "-14dB", "pan": 0.0, "sends": {"room": "-10dB"}, "notes": meet_notes()})
        doc["about"] = doc["about"].replace(" Generated by", " From v4, when the two decks lock, Least Common's meeting tune (the next song's: pings where cycles of 3, 5 and 7 sixteenths meet) goes round four times and ends half a bar before deck B is switched off. Generated by")
    else:
        del PATCHES["gt-meet"]
    if PRE:
        src = next(t for t in doc["tracks"] if t["name"] == PRE_OF)
        doc["tracks"].append({"name": "pre", "patch": src["patch"], "gain": PRE_GAIN, "pan": 0.0, "fx": [{"type": "eq", "bands": [f"hp cutoff={PRE_BAND[0]}", f"lp cutoff={PRE_BAND[1]}"]}], "notes": pre_notes(src["notes"])})      # dry and in the middle, as the drum is
        doc["about"] = doc["about"].replace(" Generated by", f" From v15 every stroke of deck A's bass drum is heard twice: a small dull print of it {PRE_TURN} sixteenths (one turn of the platter) early, as a real record's loud strokes print through to the groove before, and then itself; where the drum comes back after a rest the prints are heard alone a bar before it. Generated by")
        assert "From v15" in doc["about"]
    if CLOCK:
        for ck_i, ck_nm in enumerate(("tick", "tock")):
            PATCHES[f"gt-clock-{ck_nm}"] = {"about": f"Give or Take's wall clock, the {ck_nm} (chirper-zero, 27 Nov, v16): a 9 ms grain of noise through a narrow band at {CLOCK_HZ[ck_i]} Hz: one pallet of an escapement. Three of them make a tick (unlock, impulse, drop).",
                                           "play": {"vel_sens": 0.7},
                                           "synth": {"layers": ["white"], "filters": [{"kind": "bp", "cutoff": CLOCK_HZ[ck_i], "q": 5}, "hp cutoff=1200"], "amp": {"a": "0.1ms", "d": "9ms", "s": 0, "r": "5ms", "curve": 3}}}
            doc["tracks"].append({"name": f"clock-{ck_nm}", "patch": f"gt-clock-{ck_nm}", "gain": CLOCK_GAIN, "pan": CLOCK_PAN, "sends": {"room": CLOCK_ROOM}, "notes": clock_notes(ck_i)})
        doc["about"] = doc["about"].replace(" Generated by", f" From v16 a clock ticks on the wall through \"{CLOCK_IN}\", once a second at every whole second of the song, tick and tock by turns: fifteen seconds are thirty-one beats, so it slides through the beat and is exactly on one once in fifteen seconds. Generated by")
        assert "From v16" in doc["about"]
    return doc


def dump(doc):
    lines = []
    for k, v in doc.items():
        if k == "tracks":
            lines.append("tracks:")
            lines += ["  - " + json.dumps(t) for t in v]
        else:
            lines.append(f"{k}: {json.dumps(v)}")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    if os.environ.get("C11T1_SHOW"):
        sec = 60 / BPM * BEATS
        for name, b0, n, parts, (kind, reach, period, ramp) in SECS:
            far = max(abs(d(t / 16)) for t in range(b0 * BEATS * 16, (b0 + n) * BEATS * 16))
            fast = max(speed(t / 16) for t in range(b0 * BEATS * 16, (b0 + n) * BEATS * 16)); slow = min(speed(t / 16) for t in range(b0 * BEATS * 16, (b0 + n) * BEATS * 16))
            print(f"{name:10s} bars {b0:3d}-{b0 + n:3d}  {int(b0 * sec) // 60}:{b0 * sec % 60:04.1f}-{int((b0 + n) * sec) // 60}:{(b0 + n) * sec % 60:04.1f}  {kind:8s} furthest {far:.3f} beats ; "
                  f"deck B's tempo {BPM * slow:.1f}-{BPM * fast:.1f} ; {12 * math.log2(max(slow, 0.03)):+.2f} to {12 * math.log2(fast):+.2f} semitones ; {', '.join(sorted(parts))}")
        for t0, loop, turns in roll_stages():
            f = BPM / 60 / loop; semi = 12 * math.log2(f / 440) + 69
            print(f"   the loop from beat {t0:9.4f} (bar {t0 / BEATS + 1:7.3f}): {loop:.6g} of a beat, {loop * 60000 / BPM:8.3f} ms, {turns:2d} turns" + (f" ; {f:7.1f} a second: {'C C# D Eb E F F# G Ab A Bb B'.split()[int(round(semi)) % 12]}{int(round(semi)) // 12 - 1} {100 * (semi - round(semi)):+.0f} cents" if loop < STEP else " ; deck B's own parts"))
        if echo_span():
            lo, hi = echo_span(); ms = 60000 / BPM; e1 = echo_notes(1); st = [n for n in deck_b("stab", STAB) if lo <= n["at"] < hi][::4]; gaps = [(q["at"] - c["at"]) for c, q in zip(st, e1[::4])]
            print(f"   the echo on the record, bars {lo // BEATS + 1:g}-{hi // BEATS:g}: {len(st)} chords, {len(ECHO_GAINS)} echoes each ; chord to first echo {min(gaps) * ms:.0f} to {max(gaps) * ms:.0f} ms ({min(gaps):.3f} to {max(gaps):.3f} grid beats; the bus's is {ECHO_BEATS * ms:.0f} ms) ; "
                  f"the first echo's pitch against its chord's, semitones: {min(speed_st(q['at']) - speed_st(c['at']) for c, q in zip(st, e1[::4])):+.2f} to {max(speed_st(q['at']) - speed_st(c['at']) for c, q in zip(st, e1[::4])):+.2f}")
        if fast_window():
            t0, t1 = fast_window()
            print(f"   the other speed from bar {t0 / BEATS + 1:g} to bar {t1 / BEATS + 1:g}: deck B at {FAST_BY:.4f} of its speed ({12 * math.log2(FAST_BY):+.2f} semitones, {BPM * FAST_BY:.1f} to the minute) ; the record plays {(t1 - t0) / BEATS * FAST_BY:g} bars in {(t1 - t0) / BEATS:g} ; "
                  f"its bar lines fall on the grid's bar.beat " + " ".join(f"{int((t0 + k * BEATS / FAST_BY) // BEATS) + 1}.{(k * BEATS / FAST_BY) % BEATS + 1:g}" for k in range(9)) + " ... ; " + ", ".join(
                  f"{nm} {len(sped(st))}" for nm, st in (("hat", HAT), ("tock", TOCK), ("stab", STAB), ("knock", KNOCK))) + " strokes")
        if rewind():
            t0, T, p0, s0 = rewind(); s1 = s0 * math.exp(-T / REWIND_TAU)
            print(f"   the spin back from bar {t0 / BEATS + 1:g}: deck B backwards at {s0:.2f} times its speed ({12 * math.log2(s0):+.1f} semitones), slowing to {s1:.2f} ({12 * math.log2(s1):+.1f}) ; "
                  f"the record goes from bar {p0 / BEATS + 1:.3f} back to bar {(p0 - s0 * REWIND_TAU * (1 - math.exp(-T / REWIND_TAU))) / BEATS + 1:.3f} ; " + ", ".join(
                  f"{nm} {len(rewound(nm, st))}" for nm, st in (("hat", HAT), ("tock", TOCK), ("stab", STAB), ("knock", KNOCK))) + " strokes")
        g = grains()
        for i, by in enumerate(STRETCH_BY if g else ()):
            n = int(STRETCH_BARS * BEATS / (GRAIN * STEP)); t0, p0 = g[i * n]
            print(f"   the stretch from bar {t0 / BEATS + 1:g}: deck B at 1/{by} of its speed for {STRETCH_BARS} bars; the record goes from {p0:g} to {p0 + n * GRAIN / by:g} sixteenths ; "
                  f"every stroke is heard {by} times, {GRAIN * (1 - 1 / by):g} of a sixteenth apart ({GRAIN * (1 - 1 / by) * STEP * 60000 / BPM:.1f} ms)")
        if CLOCK:
            ck_b0, ck_b1 = clock_span(); ck_secs = clock_seconds(); ck_on = [x for x in ck_secs if abs(x * BPM / 60 - round(x * BPM / 60)) < 1e-9]
            print(f"   the clock on the wall, bars {ck_b0 + 1}-{ck_b1}: {len(ck_secs)} ticks, one at every whole second of the song from {ck_secs[0]} to {ck_secs[-1]} ({ck_secs[0] // 60}:{ck_secs[0] % 60:02d}-{ck_secs[-1] // 60}:{ck_secs[-1] % 60:02d}), tick and tock by turns ({CLOCK_HZ[0]} and {CLOCK_HZ[1]} Hz), {CLOCK_GAIN}, pan {CLOCK_PAN:g} ; a second is {BPM / 60:.4f} beats: each tick {BPM / 60 - 2:.4f} of a beat later than two beats after the last ; a tick's three sounds " + " ".join(f"{1000 * e:g}" for e, v in CLOCK_PARTS) + " ms before the second")
            print("      the first five at bar.beat " + " ".join(f"{int(x * BPM / 60 // BEATS) + 1}.{x * BPM / 60 % BEATS + 1:.3f}" for x in ck_secs[:5]) + " ; exactly on a beat at " + " ; ".join(f"{x // 60}:{x % 60:02d}.0 (bar {int(round(x * BPM / 60)) // BEATS + 1}, beat {int(round(x * BPM / 60)) % BEATS + 1})" for x in ck_on))
        if PRE:
            trs = {t["name"]: t for t in song()["tracks"]}; src = trs[PRE_OF]["notes"]; alone, none = pre_bars(src); beat = 60 / BPM
            print(f"   the record is heard a turn early: {len(trs['pre']['notes'])} prints of the {PRE_OF}, each {PRE_TURN} sixteenths ({PRE_TURN * STEP * beat * 1000:.0f} ms) before its stroke: on sixteenth {(16 - PRE_TURN) % 4} of the beat, a bar early ; {PRE_GAIN}, kept between {PRE_BAND[0]} and {PRE_BAND[1]} Hz ; bars with the print and no stroke: " + " ".join(str(b) for b in alone) + " ; bars with the stroke and no print: " + " ".join(str(b) for b in none))
        if CUE:
            ns = cue_notes(); beat = 60 / BPM
            print(f"   the cue, bars {CUE_BARS[0] + 1}-{CUE_BARS[1]} ({CUE_BARS[0] * BEATS * beat:.1f}-{CUE_BARS[1] * BEATS * beat:.1f} s): {len(ns)} strokes in one ear (pan {CUE_PAN:g}, {CUE_GAIN}) ; late by (ms) at the start of each half bar: " + " ".join(f"{cue_err(h * 2.0) * beat * 1000:+.2f}" for h in range(0, 2 * (CUE_BARS[1] - CUE_BARS[0]))))
            print(f"      its first eight strokes (bar.sixteenth): " + " ".join(f"{int(n['at'] // BEATS) + 1}.{(n['at'] % BEATS) / STEP:.3f}" for n in ns[:8]) + f" ; its fastest and slowest against the grid: {100 * max((ns[i + 1]['at'] - ns[i]['at']) / STEP for i in range(len(ns) - 1)) - 100:+.1f}% and {100 * min((ns[i + 1]['at'] - ns[i]['at']) / STEP for i in range(len(ns) - 1)) - 100:+.1f}% between strokes")
        if BASSB:
            ns = deck_b("bassb", BASSB_STEPS); beat = 60 / BPM; bars = sorted({int(n["at"] // BEATS) for n in ns}); runs = [b for b in bars if b - 1 not in bars]; ends = [b + 1 for b in bars if b + 1 not in bars]
            print(f"   deck B's bassline ({BASSB_MODE}): {len(ns)} strokes in bars " + ", ".join(f"{a + 1}-{b}" for a, b in zip(runs, ends)) + " ; by section: " + " ; ".join(f"{nm} {sum(1 for n in ns if b0 * BEATS <= n['at'] < (b0 + n_) * BEATS)}" for nm, b0, n_, parts, hand in SECS if "bassb" in parts))
            print("      its last six strokes (bar.sixteenth, held ms): " + " ".join(f"{int(n['at'] // BEATS) + 1}.{(n['at'] % BEATS) / STEP:.2f}/{n['len'] * beat * 1000:.0f}" for n in ns[-6:]))
        if speeds_span():
            b0, b1 = speeds_span(); beat = 60 / BPM
            print(f"   one record at five speeds, bars {b0 + 1}-{b1} ({int(b0 * BEATS * beat) // 60}:{b0 * BEATS * beat % 60:04.1f}-{int(b1 * BEATS * beat) // 60}:{b1 * BEATS * beat % 60:04.1f}): deck B's tock and four more decks, each at half the speed of the one before")
            for i, k in enumerate(SPEEDS_K):
                ns = speeds_notes(k)
                print(f"      1/{2 ** k} of the speed ({k} octave(s) down, {SPEEDS_GAIN[i]:g} dB): {len(ns)} strokes, {(b1 - b0) // 2 ** k} bar(s) of the record ; the first five at bar.sixteenth " + " ".join(f"{int(n['at'] // BEATS) + 1}.{(n['at'] % BEATS) / STEP:.2f}" for n in ns[:5]) + " ; " + " ".join(n["pitch"] for n in ns[:5]) + f" ; a stroke is held {ns[0]['len'] * beat * 1000:.0f} ms")
        if scratch_spans():
            beat = 60 / BPM
            print(f"   the hand on the record: " + " ; ".join(f"bar {int(s0 // BEATS) + 1} ({int(s0 * beat) // 60}:{s0 * beat % 60:04.1f}), the chord {' '.join(CHORDS[(int(s0 // BEATS) // 2) % len(CHORDS)])}" for s0 in scratch_spans()) + f" ; {len(rubs()) // len(scratch_spans())} rubs a bar ; the record's fastest {SCR_PEAK:.3f} of its own speed (+{12 * math.log2(SCR_PEAK):.2f} semitones) ; the chord's start goes under the needle at {SCR_PEAK * math.sin(SCR_PHI):.3f} of it ({12 * math.log2(SCR_PEAK * math.sin(SCR_PHI)):+.2f})")
            for b, T, n in SCR_PHRASE:
                a = SCR_PEAK * T * beat / (2 * math.pi); far = a * (math.cos(SCR_PHI) + 1)
                print(f"      from beat {b + 1:g}: {n} rubs of {T:g} of a beat ({1000 * T * beat:.1f} ms): forward {1000 * T * beat * (math.pi - SCR_PHI) / (2 * math.pi):.1f} ms, backward the same, then {1000 * T * beat * SCR_PHI / math.pi:.1f} ms in the silence before the chord ; the needle goes {1000 * far:.1f} ms into the chord, where the chord is {20 * math.log10(SCR_AMP[0] + (1 - SCR_AMP[0]) * math.exp(-far / SCR_AMP[1])):.1f} dB of its start")
        if stick():
            p0, turn, n = stick(); ms = 60000 / BPM
            ts = [when(p0 + j * turn) for j in range(n + 1)]
            print(f"   the needle sticks from bar {p0 / BEATS + 1:g} ({int(ts[0] * 60 / BPM) // 60}:{ts[0] * 60 / BPM % 60:04.1f}): one turn is {turn / STEP:g} sixteenths of the record ({turn * ms:.0f} ms at the grid's tempo: {60000 / (turn * ms):.2f} turns a minute) ; heard {n} times, {n - 1} jumps and the hand: pops at bar.sixteenth " + " ".join(f"{int(t // BEATS) + 1}.{(t % BEATS) / STEP:.2f}" for t in ts[1:]) + f" ; the turns take {min(b - a for a, b in zip(ts, ts[1:])) * ms:.0f} to {max(b - a for a, b in zip(ts, ts[1:])) * ms:.0f} ms (the platter is still pushed and dragged)")
            print("      turn: how many sixteenths early the record's bar is against the grid's, and where deck B's drum falls in deck A's beat: " + " ; ".join(f"{j + 1}: {j} {('with it', 'a sixteenth before', 'half way', 'a sixteenth after')[j % 4]}" for j in range(n)))
            print("      in one turn: " + " ; ".join(f"{nm} " + " ".join(f"{st:g}" for st, p, ln, v in (steps(int(p0 // BEATS))) if st * STEP < turn and (nm != "stab" or p == steps(int(p0 // BEATS))[0][1])) for nm, steps in (("tock", TOCK), ("knock", KNOCK), ("stab", STAB))) + f" ; hat every sixteenth ({sum(1 for st, p, ln, v in HAT(int(p0 // BEATS)) if st * STEP < turn)})")
        print(f"{BARS} bars, {TOTAL} beats, {BARS * sec:.1f} s ; the five: {FIVE}")
    else:
        open(OUT, "w").write(dump(song()))
