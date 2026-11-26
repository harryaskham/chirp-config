#!/usr/bin/env python3
"""Escapement (Chirpers 11), track 3 (chirper-zero): STANDING ROOM. The slot's word is SPACE.

THE RHYTHM IS THE ROOM. One click a bar, a wooden tock every other bar, a bass drum on the four: that is all that is
played up top. Everything else you hear the click do is the room: it stands between two walls, and each wall sends it
back. A wall is a distance, and here a distance is a number of sixteenths there and back. With the left wall 3 away
and the right wall 4, the click comes back from the left after 3, from the right after 4, from both after 7, from the
left after 10, the right after 11, both after 14 ... each time softer and duller (the walls take 3 dB and the top).
So a room is a rhythm, and its length is the two walls added: 3 + 4 is a room in seven, 2 + 3 a room in five,
5 + 7 a room in twelve, and none of those divides the bar: the echoes that outlast the bar come back BETWEEN the
next click's echoes, and the bar fills up (in the corridor twelve of its sixteen steps sound). ONE ROOM FITS:
3 + 5 is eight, half the bar, and in it the old echoes fall exactly on the new ones and stand: the click on 2
becomes 2, 5, 7, 10, 13, 15, the three-three-two, and nothing else. Standing room.

THE TOCK KEEPS THE ROOM'S TIME, NOT THE BAR'S. In a room it strikes once for every two crossings (twice the room's
length: every 14 sixteenths in the corridor, 10 in the stairwell, 24 in the hangar), so each stroke lands as its
own echo comes home from both walls, and it walks through the bar: the corridor's bar comes round every 7 bars,
the stairwell's every 5, the hangar's every 3. In standing room twice the room is the bar, and it stops walking.

The click is in ALL the rooms all the time (each room is two buses that hear the click, the tock and each other,
bd-705c25's returns); the song only opens and shuts their DOORS (a fader after each wall), and leaves a door a
little open behind it as it walks on. Nothing but the rooms changes the click's rhythm from the first bar to the last.

THE FORM IS ARITHMETIC: a row is ROW bars; SECTIONS lists, for each section, its rows, its parts, the room whose door
is open, how wide the walls stand apart and how much of the far air is heard. Every lane point comes from those.

v1 is the SKELETON (26 Nov): the rooms standing and the walk through them, with few sounds.

v2 (26 Nov): THE CLICK WALKS ACROSS EACH ROOM (C11T3_WALK=0 stands it still, as in v1). A room's length is its two
walls added, and that does not change when the click moves: only how the length is shared. In the corridor (seven)
the click starts two from the left wall and five from the right, and every row takes a step across: 2 + 5, 3 + 4,
4 + 3, 5 + 2. Every step is a new rhythm (the returns come at a, b, a + b, ...) on the same seven, so the tock,
which keeps the room's time, never notices, and the first echo crosses from the left ear to the right as the click
does. The stairwell is crossed the other way (4 + 1, 3 + 2, 2 + 3); in the hangar the click reaches the middle
(6 + 6: both walls answer at once). IN STANDING ROOM IT STANDS: 3 + 5, forty bars, not a step. Each place is its
own pair of walls with its own door, so in the bar or two of a step both places are heard: the old echoes dying
behind, the new ones building.

v3 (26 Nov): THE BASS LEARNS THE ROOM, AND TAKES IT OUT OF THE DOOR (C11T3_LEARN=0 writes v2). Until now nothing
that is PLAYED has had the room's rhythm: the bass has kept to the off-beats while the walls said three-three-two
over it. From the second row of standing room the bass plays what the room says, a stroke where the click is and
one wherever a wall sends it back in the same bar (steps 2, 5, 7, 10, 13, 15), and each wall has a note: D for the
click and for both walls together, F for the left wall, C for the right (`learnt()`, from the same `echoes()` that
prints the rooms). Then the walk goes out of the door: the walls are gone, the click is one dry click a bar again,
and THE BASS STILL PLAYS THE ROOM, walking away (18 dB down over eight bars), until the drum stops. The room is in
the hands now. The last eight bars are the click alone, as they always were. (CARRY 12, the bass four bars on after
the drum, was tried: the scorer then reads the whole song as five sections with 5.6 dB between them, 90.3.)
And the dry click is heard WHERE IT STANDS: its pan is its place between the walls ((a - b) / (a + b), times PAN),
so as it steps across a room the click itself moves with its first echo, and at 6 + 6 in the hangar it is dead centre.

v4 (26 Nov): THE WALLS CLOSE IN (C11T3_PIPES=0 takes the section out: v3). A room is a rhythm because its echoes
are far enough apart to count. Bring the walls together and they are not: the echoes run into one another and the
room SINGS, at one cycle for every crossing. A new section, "the pipes", between the stairwell and the hangar:
eight rooms too small to count, the click in the middle of each, a bar in each, every one smaller than the
last: 13.6 ms from the click to a wall and back, then 11.5, 10.2, 9.1, 8.6, 7.6, 6.8, 6.1. The same click, once a
bar, now plays D, F, G, A, B flat, C, D, E, a scale going up as the walls come in (the tock rings them too; the
bass stands back: for these eight bars the rooms are the only thing with a note). These
walls are hard (they give back all but a decibel, so a pipe rings for 0.7 s) where the big rooms' walls take three.
6 ms is as close as this engine's walls will stand, so E is the top, and it is the ninth of the chord the hangar
opens with: the walls fly apart, from six milliseconds to twelve sixteenths, on the note the pipes left hanging.

v5 (26 Nov): ACROSS THE SQUARE (C11T3_SQUARE=0 writes v4). The song's unit has always been a sixteenth of sound:
a wall three sixteenths away answers three sixteenths late. A sixteenth at this tempo is 119 ms, and sound goes 41
metres in that. So "outside" is now a place too: when the song begins the click is FAR sixteenths away across a
square (four: 163 m), and THE CLICK IS AS LATE AS IT IS FAR. It is written on the second sixteenth of the bar, as
ever, and heard on the sixth; every bar the listener is a quarter of a sixteenth nearer and it comes 30 ms sooner
(the bass drum, which is here and not there, is the ruler: the click passes through it on the ninth bar), until at
the corridor's door it is where it was written. It is also as quiet as it is far (6 dB for every doubling of the
distance, from one sixteenth: 14 dB down at four) and as dull (the air takes 5 dB of its top for each sixteenth:
20 dB at four). (The first try was late and dull and NOT quiet: this song's master holds every click 20 dB down
at its ceiling, so a click 14 dB down came out as loud as ever. The far click is written LIMIT dB lower still.) Nothing else in the song moves. In "the door" the same walk is taken backwards: the click falls
behind the drum a quarter of a sixteenth a bar, fainter and duller, and the last click of the song is where the
first was, 163 m off and four sixteenths late. The song now fades by walking away.

v6 (26 Nov): THE WALLS SING (C11T3_SING=0 takes it out: v5). In v3 the bass learnt the room: it plays a stroke
where the click is and one wherever a wall sends it back, and each wall has a note (F for the left, C for the
right, D for the click). In v4 a room too small to count was found to sing. v6 puts the two together: IN EACH
WALL OF STANDING ROOM THERE IS A PIPE, tuned to that wall's note, and a third where the click stands. A pipe is
struck by whatever reaches it: the click strikes the D pipe; three sixteenths on its echo comes off the left wall
and strikes the F pipe in that wall; two sixteenths later the right wall's, C; then both, softer; and so on, each
return 3 dB down, as the walls have always done it. So the room plays the bass's line, D F C (F and C) F C, in
the bass's rhythm, the three-three-two, with nobody playing it: F from the left, C from the right, D from where
the click stands. For the fourth row of standing room THE BASS RESTS and the line is still there, sung by the
walls with no bass under it (a pipe struck by a click has almost nothing at its own note: the ear puts the note
there from what is above it). In the fifth row the bass comes back in under its own line, and then, as before,
takes it out of the door: the pipes are shut with the walls.
The pipes hear the click's echoes only, not the tock's (the walls as the click alone finds them: `hear-l`,
`hear-r`, which are not heard themselves), because the bass learnt the click's line.

v7 (26 Nov): IN TIME ALL ALONG (C11T3_PASS=0 takes it out: v6). Six rounds of rooms: walls, pipes, a square the
click walks across. Nothing in the song has MOVED PAST. Now, outside, something does: a small bell on a thing that
goes by on a straight line from the left to the right, a sixteenth of sound (41 m) away at its closest, at one
fifth of the speed of sound. It strikes straight eighths, at the song's tempo, on one note, F: it is in time
and in tune all along. That is not what is heard. Each stroke is heard when its sound has crossed the distance,
and the distance is closing: the strokes pile up. While it is coming, every stroke arrives 4/5 of an eighth
after the last: FIVE STROKES AGAINST THE BEAT'S FOUR, and its note is heard 5/4 too high: A. When it has gone
by, the distance is opening: every stroke arrives 6/5 of an eighth after the last, FIVE AGAINST SIX, and its
note is 5/6 of itself: D. Tempo and pitch are one thing, as they are on a record (Give or Take), and here it is
distance that turns the platter. So what goes past plays a cadence nobody wrote: A, the fifth of the key, falls
through F (its own note, heard only at the instant it is closest: the first beat of bar 11, a sixteenth late,
because it is a sixteenth away) to D, the key note, as the door of the corridor opens. Its loudness is its
distance (1/r) and its side is its bearing. One speed does all of it: c/5 gives 5:4, 5:6, a major third up, a
minor third down, and a fifth between.
(The bell is tuned 15 cents sharp of F so that the A and the D it is heard as are the song's own within 2 cents.)
With the bell goes a CLACK, the click's own rim with its bottom taken off, on every stroke: what carries the bell.
BENCHED (seed 0; v6 that day 96.14): the bell alone at -12 dB 95.51 (it was 7.6 dB over everything else at its
closest, and the scorer heard a new section at 18 s and a duller song); at -20 dB 95.73; twice as far off (82 m)
95.51; a second pass in "the door", the other way, 95.38; the bell at -20 dB with the clack 95.94. The last is
what is here: it costs 0.20 on both seeds, and it is kept because the song had nothing that moved.

v8 (26 Nov): TWICE (C11T3_TWICE=0 takes it out: v7). What went past at the beginning goes past again at the end,
the other way and FASTER: in "the door", as the click walks off across the square, the bell comes from the right
at a THIRD of the speed of sound and is gone to the left. The same arithmetic with one number changed. At c/5
its strokes came five against four and went five against six, and its note fell a fifth (5/4 to 5/6: A to D).
At c/3 they come THREE AGAINST TWO (triplets over the bass drum's eighths) and go THREE AGAINST FOUR, exactly
half as fast as they came; and its note is heard 3/2 of itself coming and 3/4 going: it falls AN OCTAVE, and
the tempo falls an octave with it. The bell is on G this time: D above, then D below, through G for the one
stroke when it is closest (the first beat of bar 157, a sixteenth late). A fourth-and-fifth close where the
first pass made a fifth: plagal, for the way out. Both passes leave on the same D, the tock's.
(c/n always gives n against n - 1 and n against n + 1, and a fall of (n + 1)/(n - 1): a fifth at 5, an octave
at 3, a twelfth at 2.)
ALSO: the three lanes of what goes past (its note, its level, its side) are now drawn STRAIGHT between strokes
("curve": 0). The engine bows a lane where it falls (chirp-eco's bench, 26 Nov): v7's bell was up to 19 cents
flat between strokes where it was closest. And the clack that carries the bell is 6 dB up (-20 dB).

v9 (26 Nov): STANDING ROOM (C11T3_STAND=0 takes it out: v8). The song is named for a room in which there is only
room to stand, and until now it had every kind of room but the one the name means: a room with a STANDING WAVE
in it. Between two walls a note whose half-waves fit holds still: loud at the walls, silent at its nodes, and
how loud it is depends on WHERE YOU STAND and on nothing else. The room is 2.34 m from wall to wall: its own
note is D2, and what is sounded in it is five of its modes (the second, third, fourth, sixth and eighth: D3,
A3, D4, A4, D5; the fifths and octaves of the song's key and no third). For the first three rows of "standing
room" (bars 113 to 136) you walk from the left wall to the right, and mode n is as loud as |cos(n pi x / L)|
where your EAR is: at the wall the whole chord; a sixth of the way across the A3 is gone; a quarter, the D3 and
the A4; a third, the As ring over everything; in the middle A3 is gone again and the Ds stand; then the same
back, mirrored. Nothing is played but five held notes. AND THE TWO EARS ARE NOT IN THE SAME PLACE: they are
17 cm apart along the walk, which is most of the way from one node of the top mode to the next (29 cm), so the
D5 is in one ear while it is out of the other, and passes from ear to ear eight times in the crossing; the A4
six; the low D3 hardly at all (low notes have no side: that is why). The modes are on tracks of their own, an
ear each (`mode-N-l`, `mode-N-r`), dry: they are the room.
(Not made: the wave's SIGN. Either side of a node the air moves the opposite way, so two ears with a node
between them are half a cycle apart; here they differ in loudness only. And the modes are the tempered D and A:
the room's true third mode is 2 cents above A3.)

v10 (26 Nov): A CLAP COMES BACK AS A CHIRP (C11T3_CHIRP=0 takes it out: v9). The stairwell has had walls; now it
has STAIRS. Clap your hands at the foot of a long flight of steps and what comes back is not a clap: every step
sends its own small echo, each a little later than the one below it, and a row of echoes evenly spaced is a
NOTE. But they are not evenly spaced: the low steps are straight ahead (one tread further each: 2 x 29.2 cm of
path, 1/587 s: D5) and the high ones are up the slope (a tread and a riser further each: 2 x 39 cm, 1/440 s:
A4), so the note FALLS as the echo goes up the flight: a click comes back as a chirp, a fourth down in an
eighth of a second. (It is what a handclap does at the foot of the Castillo at Chichen Itza; these treads are
sized for D minor and the Castillo's are not.) Sixty steps; each echo is the same tick as the clap, smaller
by its distance: 1200 echoes are written, each a note.
From the fifth bar of "the stairwell" (bars 53 to 72, 1:39 to 2:17) the hands clap once a bar, on the eleventh
sixteenth, and you WALK TO THE STAIRS: a sixteenth of sound from them and back (20 m), then half (10 m), a
quarter (5 m), an eighth (2.5 m). Two things tell you how far they are and neither is loudness: WHEN the chirp
comes (a sixteenth after the clap, a thirty-second, and then on its heels), and HOW IT FALLS (from far off it
is still falling as it ends, D5 to B flat 4, and its last echo is 9 dB under its first; close to, it drops
at once to A4, stays there, and dies 30 dB).
The clap and its echoes are one patch (`sr-step`: 5 ms of a sine on A5, the note the chirp lands an octave
under) on two tracks (`clap-at` the hands, `stairs` the sixty echoes), dry. The first echo is given the same
level at every distance (from 20 m a real one would be 27 dB weaker than from 2.5): what changes is when and
how, as said.
(Benched first: a clap of under a millisecond, which is what an echo this fine wants, came out a different
size and shape every time: the engine moves its envelopes every 32 samples (0.67 ms). Sixty of them at one
spacing were only 8 dB clear of noise; sixty 5 ms ticks are 17 dB clear. The ticks overlap, as real echoes do.)

v11 (26 Nov): STANDING ROOM ONLY (C11T3_HOUSE=0 takes it out: v10). The record's name, the other way: the room
FILLS WITH PEOPLE, and people are the best absorbers a room ever gets. Sabine's law (1898: he measured a hall's
echo with an organ pipe, a stopwatch and seat cushions): a room's echo lasts T = 0.161 V / A seconds, V its
volume and A everything in it that swallows sound; every person adds the same amount to A. So a room dies
(1 + people's share) times as fast when the people are in, and it does not matter where they stand.
After the standing wave, in the last two rows of "standing room" (bars 137 to 152, 4:19 to 4:49), people come
in twice: over bars 137 to 140, to half a house (held to bar 144), and over bars 145 to 148 to a full one (held
to the door). A full house swallows twice what the empty room does. What that does here, to the two things
the room is made of:
- THE WALLS. A click comes back off the left wall three sixteenths on, off the right five on, and each echo
  goes on to the other wall. A bare wall takes 3 dB each time; with half a house 6 dB, with a full one 9 dB:
  every wall, every time. The echoes' rhythm is the same; the train of them is a third as long.
- THE AIR (the hall's wash behind them). Its decay goes from 5.5 s to 2.75 s to 1.83 s. It is sent no less:
  a click's wash begins as loud as it did and dies sooner, so what is left of the clicks before is less.
Nothing in the engine turns a room's decay while it sounds, so three rooms are built (empty, half, full: the
walls and the air of each) and the click is in all three at once; a lane on each room's door lets one be heard
at a time, and two are mixed only while the people are coming in. No track is changed.
- THE PIPES IN THE WALLS (v6: they sing from bar 137, struck by what reaches each wall). With people in front
  of a wall less reaches it: each room has its own pair of wall pipes, struck by that room's echoes. The pipe
  where the click stands is struck by the click itself and is as it was.
(Made first without that: the walls alone. In the master nothing could be read: where the click's echoes fall
the pipes sing, and they were as loud as ever. A bench said so before it was published.)
"""
import json
import math
import os

OUT = os.environ.get("C11T3_OUT", os.path.join(os.path.dirname(__file__), "..", "..", "..", "songs", "chirpers11-t3.yaml"))
BPM = 126
BEATS = 4
ROW = 8
STEP = 0.25

# a room: the left wall and the right wall, in sixteenths there and back
ROOMS = {"corridor": (3, 4), "stairwell": (2, 3), "hangar": (5, 7), "standing": (3, 5)}
# where the click stands in each room, a row or more at each place (left wall, right wall): the room's length stays
WALK = {"corridor": [(2, 5), (3, 4), (4, 3), (5, 2)], "stairwell": [(4, 1), (3, 2), (2, 3)], "hangar": [(4, 8), (5, 7), (6, 6), (7, 5)], "standing": [(3, 5)]}
if os.environ.get("C11T3_WALK", "1") == "0":
    WALK = {room: [ab] for room, ab in ROOMS.items()}
assert all(a + b == sum(ROOMS[room]) for room, w in WALK.items() for a, b in w)
LEARN = os.environ.get("C11T3_LEARN", "1") != "0"   # v3: the bass learns the room; the dry click is where it stands
LEARN_ROOM = "standing"        # the room the bass learns
LEARN_AFTER = 1                # rows of that room it listens for first
WALL_NOTE = {"click": "D2", "both": "D2", "left": "F2", "right": "C2"}   # the bass's note for the click and for each wall's answer
CARRY = 8                      # bars of "the door" the bass carries the room on for (the drum stops at 8 too)
AWAY = -18                     # dB the bass has fallen by then: it walks away with the room in its hands
PAN = 0.7                      # the dry click's pan when it stands AT a wall (it never does: 4 + 1 is 0.6 of the way)
PIPES_ON = os.environ.get("C11T3_PIPES", "1") != "0"   # v4: the walls close in
PIPES = ("D2", "F2", "G2", "A2", "Bb2", "C3", "D3", "E3")   # the note each pipe sings: one cycle for every crossing (a wall 1000 / Hz ms away)
PIPE_BARS = 1                  # bars the click stands in each
PIPE_RING = 0.7                # seconds a pipe rings (to -60 dB): its walls give back 60 * (the crossing in seconds) / PIPE_RING dB less each time
PIPE_LEVEL = -11               # dB: a pipe's door when it is open
PIPE_TRIM = 0.035              # ms: what a wall's own filter adds to a crossing (measured: the pipes sang 4 to 11 cents flat without it)
PIPE_DAMP = ["hp cutoff=40", "lp cutoff=4500"]   # what a pipe's wall takes
SQUARE = os.environ.get("C11T3_SQUARE", "1") != "0" and PIPES_ON   # v5: across the square
FAR = 4                        # sixteenths of sound the click is away in the song's first bar and in its last (a sixteenth is 60 / BPM / 4 s: 41 m)
NEAR = 1                       # its level is 20 log10(NEAR / (NEAR + its distance)) dB: 6 dB down at one sixteenth, 14 at four
LIMIT = 20                     # dB the master's limiter already holds the click down by when it is here (measured: the song's loudness gain is 19 dB and
                               # the click's own peak is 1 dBFS before it): a click loses this much first, or it is not heard to lose anything
AIR = 5                        # dB of its top (the lift round 11 kHz) the air takes for each sixteenth of distance
SOUND = 343                    # metres a second
SING = os.environ.get("C11T3_SING", "1") != "0" and SQUARE   # v6: the walls sing
SING_FROM = 3                  # rows of standing room before the pipes in its walls are opened
SING_ALONE = 1                 # rows from there for which the bass rests
SING_RING = 0.45               # seconds one of those pipes rings (to -60 dB): a note, not a drone
SING_LEVEL = float(os.environ.get("C11T3_SING_LEVEL", "-6"))   # dB: their door when it is open
SING_PAN = 0.6                 # how far to its side a wall's pipe is heard (the click's is where the click stands)
SING_DAMP = ["hp cutoff=40", "lp cutoff=3000"]   # what a pipe's own wall takes
PASS = os.environ.get("C11T3_PASS", "1") != "0" and SING   # v7: in time all along (what goes past)
PASS_V = 1 / 5                 # its speed, as a part of sound's (69 m/s): 5 strokes against 4 as it comes, 5 against 6 as it goes
PASS_NEAR = float(os.environ.get("C11T3_PASS_NEAR", "1"))   # sixteenths of sound it is away at its closest (41 m)
PASS_EVERY = 2                 # sixteenths between its strokes, where it is: straight eighths
PASS_NOTE = "F5"               # its own note: heard 5/4 of it coming (A5, the click's) and 5/6 of it going (D5, the tock's)
PASS_SHARP = 0.15              # semitones the bell is sharp of that note, so that the two notes it is heard as are in tune
PASS_IN = dict((nm, tuple(float(q) for q in v.split("/"))) for nm, v in (x.split("=") for x in os.environ.get("C11T3_PASS_IN", "outside=10/4/16/1").split(",")))
#                                a section: the bar of it on whose first beat the thing is closest / the bars of it between which it is heard / 1 left to right, -1 right to left
PASS_FADE = 2                  # bars at each end in which it comes out of nothing and goes back into it ...
PASS_FADE_DB = -30             # ... from this far under its level there
PASS_GAIN = os.environ.get("C11T3_PASS_GAIN", "-20dB")   # the bell's level when it is closest
TWICE = os.environ.get("C11T3_TWICE", "1") != "0" and PASS   # v8: twice (the second pass; straight lanes; the clack up)
PASS_AGAIN = os.environ.get("C11T3_PASS_AGAIN", "1") != "0" and TWICE      # the second pass ...
AGAIN = {"sec": "the door", "at": 4, "lo": 0, "hi": 8, "way": -1, "v": 1 / 3, "note": "G5", "sharp": -0.02}   # ... the bar of the section it is closest on, the bars it is heard between, right to left, its speed, its own note
STRAIGHT = os.environ.get("C11T3_STRAIGHT", "1") != "0" and TWICE          # the lanes of what goes past are straight between strokes
PASS_TICK = os.environ.get("C11T3_PASS_TICK", "-20dB" if TWICE else "-26dB")   # ... and the level of the clack that carries the bell ("" for the bell alone)
PASS_PAN = 0.9                 # how far to the side it is heard when it is far along its line
STAND = os.environ.get("C11T3_STAND", "1") != "0" and TWICE                     # v9: standing room (a standing wave, walked across)
STAND_IN = ("standing room", 0, 24)                    # the section, and the bars of it in which you walk from wall to wall
STAND_HOLD = 4.5                                       # beats the held notes are written past the far wall: a note sounds for 95% of its written length (the engine's `play.gate`; CORRECTED 26 Nov 15:50: not "lets go 4.6 beats early"), so these let go half a beat before the wall; `play: {gate: 1}` on the patch is the right way, for a next version
STAND_ROOT = 73.416                                    # Hz: the room's own note (D2): its walls are SOUND / (2 * STAND_ROOT) = 2.34 m apart
STAND_MODES = ((2, "D3"), (3, "A3"), (4, "D4"), (6, "A4"), (8, "D5"))   # the modes that are sounded: fifths and octaves, no third
STAND_EAR = 0.17                                       # m from ear to ear, along the walk
STAND_GAIN = float(os.environ.get("C11T3_STAND_GAIN", "-28"))   # dB: a mode at a wall (benched: at -24 the chord was 5 dB under the music and the loudness stage turned the rest of the song down 0.55 dB; it scored more the louder it was)
STAND_TILT = -3.0                                      # dB an octave: the higher modes are damped more
STAND_FLOOR = -40.0                                    # dB: how deep a node is let be
STEP_OPEN = 1                  # bars the door of the next place takes to open as the click steps
STEP_SHUT = 2                  # bars the door of the place behind takes to shut
WALL = "-3dB"                  # what a wall gives back
FIRST = {"click": "-4dB", "tock": "-6dB"}   # how loud each part reaches a wall
ABSORB = ["hp cutoff=250", "lp cutoff=9000"]

# name, rows, parts, the room whose door is open (None: outside), the walls' width, the far air (dB; None: none)
SECTIONS = [
    ("outside",       2, {"click", "kick", "tock"},                          None,        0.0, None),
    ("the corridor",  4, {"click", "kick", "tock", "bass"},                  "corridor",  0.8, -22),
    ("the stairwell", 3, {"click", "kick", "tock", "bass"},                  "stairwell", 0.5, -26),
] + ([("the pipes",    len(PIPES) * PIPE_BARS // ROW, {"click", "kick", "tock"}, None,              0.0, None)] if PIPES_ON else []) + [
    ("the hangar",    4, {"click", "kick", "tock", "bass", "chord"},         "hangar",    1.2, -8),
    ("standing room", 5, {"click", "kick", "tock", "bass", "chord", "clap"}, "standing",  1.0, -16),
    ("the door",      2, {"click", "kick", "tock"} | ({"bass"} if LEARN else set()), None,   0.0, None),
]
CHIRP = os.environ.get("C11T3_CHIRP", "1") != "0" and STAND                     # v10: a clap comes back as a chirp (the stairs)
CHIRP_IN = "the stairwell"
CHIRP_TREAD = SOUND / (2 * 587.33)                     # m (0.292): at the foot each tread is this much further: echoes 1/587 s apart, D5
CHIRP_RISER = 0.2576                                   # m: far up the flight each step is a tread and a riser further, 0.39 m: echoes 1/440 s apart, A4
CHIRP_STEPS = 60                                       # steps in the flight (17.5 m along, 15.5 m up)
CHIRP_AWAY = ((4, 8, 1.0), (8, 12, 0.5), (12, 16, 0.25), (16, 24, 0.125))   # (from bar, to bar of the section, how far off the foot of the stairs is: sixteenths of sound THERE AND BACK; 1 is 20.4 m)
CHIRP_ON = (10,)                                       # the sixteenths of a bar on which the hands clap (none of the stairwell's own echoes falls there)
CHIRP_FALL = 1.5                                       # a step's echo is (the foot's distance / its own) to this power of the foot's
CHIRP_NOTE = "A5"                                      # the tick: 5 ms of a sine on this note (the chirp ends an octave under it)
CHIRP_LEN = 0.008                                      # beats a tick is held (3.8 ms)
CHIRP_GAIN = float(os.environ.get("C11T3_CHIRP_GAIN", "-2"))    # dB: the clap (benched alone: at -6 the chirp's first 20 ms were 12 dB under the click; at -2 they are 8 under)
CHIRP_BACK = float(os.environ.get("C11T3_CHIRP_BACK", "-6"))    # dB: the echo from the foot of the stairs against the clap, at every distance
OPEN = 2                       # bars a door takes to open (from AJAR)
SHUT = 4                       # bars it takes to shut behind the walk
AJAR = -24                     # dB: where an opening door starts and a shutting one ends before it is closed
CLOSED = -90
ENTER = {"outside": [("kick", 4), ("tock", 8)], "the corridor": [("bass", 2 * ROW)], "the hangar": [("kick", ROW), ("bass", ROW)]}   # the bar of the section from which a part is there
LEAVE = {"the door": [("tock", 8), ("kick", 8)]}                                                                                      # ... and from which it is gone
if LEARN:
    LEAVE["the door"].append(("bass", CARRY))


def starts():
    out, b = [], 0
    for name, rows, parts, room, width, air in SECTIONS:
        out.append((name, b, rows * ROW, parts, room, width, air)); b += rows * ROW
    return out, b


SECS, BARS = starts()
TOTAL = BARS * BEATS


def section_of(bar):
    for s in SECS:
        if s[1] <= bar < s[1] + s[2]:
            return s
    return SECS[-1]


def sing_bars():
    """(first bar, last bar) in which the pipes in standing room's walls are open, and (first, last) in which the bass rests."""
    b0, n = next((s[1], s[2]) for s in SECS if s[4] == LEARN_ROOM)
    return (b0 + SING_FROM * ROW, b0 + n), (b0 + SING_FROM * ROW, b0 + (SING_FROM + SING_ALONE) * ROW)


def plays(part, bar):
    name, b0, n, parts, room, width, air = section_of(bar)
    if SING and part == "bass" and sing_bars()[1][0] <= bar < sing_bars()[1][1]:
        return False
    for p, there in ENTER.get(name, []):
        if p == part and bar < b0 + there:
            return False
    for p, gone in LEAVE.get(name, []):
        if p == part and bar >= b0 + gone:
            return False
    return part in parts


def dist(bar):
    """How far off the click is in a bar, in sixteenths of sound: it comes across the square through the song's
    first section and goes back across it through the last; anywhere else it is here."""
    if not SQUARE:
        return 0.0
    sec = section_of(bar)
    if sec[1] == SECS[0][1]:
        return FAR * (1 - (bar - sec[1]) / sec[2])
    if sec[1] == SECS[-1][1]:
        return FAR * (bar - sec[1] + 1) / sec[2]
    return 0.0


def dist_lane(per):
    """A lane that is per(distance) for the whole of each bar."""
    pts, last = [], None
    for bar in range(BARS):
        v = round(per(dist(bar)), 3)
        if v != last:
            pts += ([pt(bar - 0.01, last)] if last is not None else []) + [pt(bar, v)]
        last = v
    return pts + [pt(BARS, last)]


def stand_span():
    """The beats between which the standing wave is walked across, or None."""
    sec = next((x for x in SECS if x[0] == STAND_IN[0]), None) if STAND else None
    return ((sec[1] + STAND_IN[1]) * BEATS, (sec[1] + STAND_IN[2]) * BEATS) if sec else None


def stand_at(t, side):
    """Where an ear (side -1 left, 1 right) is at beat t, as a share of the way from the left wall to the right."""
    lo, hi = stand_span()
    L = SOUND / (2 * STAND_ROOT)
    u = min(1.0, max(0.0, (t - lo) / (hi - lo)))
    return (STAND_EAR / 2 + (L - STAND_EAR) * u + side * STAND_EAR / 2) / L


def stand_db(n, t, side):
    """dB of mode n at that ear at beat t: |cos(n pi x / L)|, no deeper than STAND_FLOOR."""
    return max(STAND_FLOOR, 20 * math.log10(max(abs(math.cos(n * math.pi * stand_at(t, side))), 1e-9)))


def mode_lane(n, side):
    lo, hi = stand_span()
    k = int(round((hi - lo) / STEP))
    return [["0b", round(stand_db(n, lo, side), 2)]] + [[f"{lo + i * STEP:g}b", round(stand_db(n, lo + i * STEP, side), 2)] for i in range(k + 1)] + [[f"{TOTAL:g}b", round(stand_db(n, hi, side), 2)]]


HOUSE = os.environ.get("C11T3_HOUSE", "1") != "0" and CHIRP                     # v11: standing room only (the house fills: Sabine's law)
HOUSE_IN = "standing room"
HOUSE_STEPS = ((24, 28, 0.5), (32, 36, 1.0))           # (from bar, to bar of the section, the share of a full house there is by then): people come in twice
HOUSE_FULL = float(os.environ.get("C11T3_HOUSE_FULL", "2"))   # what a full house swallows, in what the empty room swallows: the room then dies 1 + HOUSE_FULL times as fast
AIR_DECAY = 5.5                                        # s: the hall's decay, empty (the air bus's own)


def house_stages():
    """(share of a full house, the beat by which it is in, the beat from which the next people come) of every room that is built: the empty one first. [] with no house."""
    sec = next((x for x in SECS if x[0] == HOUSE_IN), None) if HOUSE else None
    if sec is None or sec[4] is None:
        return []
    out = [(0.0, 0.0, (sec[1] + HOUSE_STEPS[0][0]) * BEATS)]
    for i, (b0, b1, n) in enumerate(HOUSE_STEPS):
        out.append((n, (sec[1] + b1) * BEATS, (sec[1] + HOUSE_STEPS[i + 1][0]) * BEATS if i + 1 < len(HOUSE_STEPS) else BARS * BEATS))
    return out


def house_share(i, t):
    """How much of what is heard at beat t is room i's (0 to 1): all of it between its people's coming and the next ones', a mix of two rooms while they come in."""
    st = house_stages()
    n, t_in, t_out = st[i]
    if t_in <= t <= t_out:
        return 1.0
    if i > 0 and st[i - 1][2] < t < t_in:
        return (t - st[i - 1][2]) / (t_in - st[i - 1][2])
    if i + 1 < len(st) and t_out < t < st[i + 1][1]:
        return 1 - (t - t_out) / (st[i + 1][1] - t_out)
    return 0.0


def lane_at(points, t):
    """A lane's value at beat t, straight between its points."""
    xs = [(float(p[0][:-1]), p[1]) for p in points]
    for (t0, v0), (t1, v1) in zip(xs, xs[1:]):
        if t0 <= t <= t1:
            return v0 if t1 == t0 else v0 + (v1 - v0) * (t - t0) / (t1 - t0)
    return xs[-1][1]


def house_lane(points, i, trim=0.0):
    """A door's or the air's lane (dB) as room i has it: the lane itself while that room is the only one heard, shut while it is not heard, and while people come in the lane less the room's share (a point every half beat)."""
    st = house_stages()
    ts = sorted({float(p[0][:-1]) for p in points} | {st[0][2] + k / 2 for k in range(int((st[-1][1] - st[0][2]) * 2) + 1)} | {x for q in st for x in (q[1], q[2])})
    vals = []
    for t in ts:
        w = house_share(i, t)
        vals.append([f"{t:g}b", CLOSED if w <= 1e-6 else round(max(CLOSED, lane_at(points, t) + trim + 20 * math.log10(w)), 3)])
    return [p for k, p in enumerate(vals) if k in (0, len(vals) - 1) or not (vals[k - 1][1] == p[1] == vals[k + 1][1])]


def chirp_away(bar):
    """Metres from the hands to the foot of the stairs in that bar, or None where there is no clap."""
    sec = next((x for x in SECS if x[0] == CHIRP_IN), None) if CHIRP else None
    if sec is None:
        return None
    for b0, b1, away in CHIRP_AWAY:
        if sec[1] + b0 <= bar < sec[1] + b1:
            return away * (60 / BPM / 4) * SOUND / 2
    return None


def stair_echoes(d):
    """(seconds after the clap, level against the foot's echo) of the echo from each step, the foot d metres off."""
    out = []
    for n in range(CHIRP_STEPS):
        r = math.hypot(d + n * CHIRP_TREAD, n * CHIRP_RISER)
        out.append((2 * r / SOUND, (d / r) ** CHIRP_FALL))
    return out


def chirp_notes():
    """The claps, and every step's echo of every clap."""
    claps, back = [], []
    for bar in range(BARS):
        d = chirp_away(bar)
        if d is None:
            continue
        for s in CHIRP_ON:
            t = bar * BEATS + s * STEP
            claps.append({"at": round(t, 6), "len": CHIRP_LEN, "pitch": CHIRP_NOTE, "vel": 1.0})
            back += [{"at": round(t + sec * BPM / 60, 6), "len": CHIRP_LEN, "pitch": CHIRP_NOTE, "vel": round(lv, 4)} for sec, lv in stair_echoes(d)]
    return claps, back


def note(at, pitch, length, vel):
    return {"at": round(at, 4), "len": round(length, 4), "pitch": pitch, "vel": round(vel, 3)}


def part(name, steps):
    out = []
    for bar in range(BARS):
        if plays(name, bar):
            out += [note(bar * BEATS + s * STEP, p, n * STEP, v) for s, p, n, v in steps(bar)]
    return out


def pt(bar, v):
    return [f"{bar * BEATS:g}b", round(v, 3)]


def places():
    """Every place the click stands: (bus name, left wall, right wall, first bar, last bar, bars to open, bars to shut)."""
    out = []
    for name, b0, n, parts, room, width, air in SECS:
        if room is None:
            continue
        walk = WALK[room]
        each = n / len(walk)
        for i, (a, b) in enumerate(walk):
            out.append((room if len(walk) == 1 else f"{room}{a}{b}", a, b, b0 + i * each, b0 + (i + 1) * each, OPEN if i == 0 else STEP_OPEN, SHUT if i == len(walk) - 1 else STEP_SHUT))
    assert len({p[0] for p in out}) == len(out)
    return out


def door_lane(b0, b1, opn, shut):
    """dB on a place's door: open while the click stands there, opening as it comes, shutting behind it."""
    pts = [pt(0, CLOSED), pt(b0 - 0.01, CLOSED), pt(b0, AJAR), pt(b0 + opn, 0), pt(b1, 0), pt(b1 + shut, AJAR), pt(b1 + shut + 0.01, CLOSED), pt(BARS, CLOSED)]
    return [p for i, p in enumerate(pts) if i == 0 or p != pts[i - 1]]


def step_lane(index, default, glide=2):
    """A lane that holds each section's value and glides to the next over the section's first `glide` bars."""
    pts, last = [], None
    for s in SECS:
        v = s[index] if s[index] is not None else default
        if last is None:
            pts.append(pt(0, v))
        elif v != last:
            pts += [pt(s[1], last), pt(s[1] + glide, v)]
        last = v
    pts.append(pt(BARS, last))
    return pts


def breath_lane(depth=0.2, bars=8):
    """The dub delay's feedback, breathing once in `bars` bars."""
    return [pt(b, depth * math.sin(2 * math.pi * b / bars)) for b in range(0, BARS + 1)]


def hz(p):
    semi = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[p[0]] + (-1 if "b" in p[1:] else 1 if "#" in p else 0) + 12 * (int(p[-1]) + 1)
    return 440.0 * 2 ** ((semi - 69) / 12)


def pipes():
    """Every pipe: (bus name, the note, ms from the click to either wall and back, first bar, last bar)."""
    b0 = next((s[1] for s in SECS if s[0] == "the pipes"), None)
    return [] if b0 is None else [(f"pipe{i}", p, 1000 / hz(p), b0 + i * PIPE_BARS, b0 + (i + 1) * PIPE_BARS) for i, p in enumerate(PIPES)]


def pipe_buses():
    """A pipe is two hard walls the same distance from the click, too near to count (the engine wants 6 ms or more)."""
    out = {}
    for name, p, ms, b0, b1 in pipes():
        assert ms - PIPE_TRIM >= 6.0, (p, ms)
        back = f"{-60 * ms / 1000 / PIPE_RING:.2f}dB"
        for side, other in (("l", "r"), ("r", "l")):
            out[f"{name}-{side}"] = {"fx": [{"type": "eq", "bands": PIPE_DAMP}],
                                     "returns": [{"from": part, "gain": g, "time": f"{ms - PIPE_TRIM:.3f}ms"} for part, g in FIRST.items()] + [{"from": f"{name}-{other}", "gain": back, "time": f"{ms - PIPE_TRIM:.3f}ms"}],
                                     "out": f"{name}-door"}
        out[f"{name}-door"] = {"pan": 0.0, "fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.door", "amount": 1}]}}],
                               "auto": {"door": {"points": [pt(0, CLOSED), pt(b0 - 0.02, CLOSED), pt(b0, PIPE_LEVEL), pt(b1 - 0.15, PIPE_LEVEL), pt(b1, CLOSED), pt(BARS, CLOSED)]}}}
    return out


def sing_buses():
    """The pipes in standing room's walls: one in each wall, struck by what that wall sends back of the click, and one where the click stands."""
    a, b = WALK[LEARN_ROOM][0]
    (b0, b1), rest = sing_bars()
    out = {}
    for side, own, other in (("l", a, "r"), ("r", b, "l")):      # the room as the click alone finds it: the pipes hear this, nobody else does
        out[f"hear-{side}"] = {"fx": [{"type": "eq", "bands": ABSORB}],
                               "returns": [{"from": "click", "gain": FIRST["click"], "time": f"{own}/16"}, {"from": f"hear-{other}", "gain": WALL, "time": f"{own}/16"}],
                               "out": "hear-shut"}
    out["hear-shut"] = {"fx": [{"type": "gain", "gain": f"{CLOSED}dB"}]}
    lane = [pt(0, CLOSED), pt(b0 - 0.02, CLOSED), pt(b0, SING_LEVEL), pt(b1, SING_LEVEL), pt(b1 + STEP_SHUT, SING_LEVEL + AJAR), pt(b1 + STEP_SHUT + 0.01, CLOSED), pt(BARS, CLOSED)]
    for name, src, gain, pan in (("click", "click", FIRST["click"], PAN * (a - b) / (a + b)), ("left", "hear-l", "0dB", -SING_PAN), ("right", "hear-r", "0dB", SING_PAN)):
        ms = 1000 / hz(WALL_NOTE[name])
        assert ms - PIPE_TRIM >= 6.0, (name, ms)
        back = f"{-60 * ms / 1000 / SING_RING:.2f}dB"
        for side, other in (("a", "b"), ("b", "a")):
            out[f"sing-{name}-{side}"] = {"fx": [{"type": "eq", "bands": SING_DAMP}],
                                          "returns": [{"from": src, "gain": gain, "time": f"{ms - PIPE_TRIM:.3f}ms"}, {"from": f"sing-{name}-{other}", "gain": back, "time": f"{ms - PIPE_TRIM:.3f}ms"}],
                                          "out": f"sing-{name}-door"}
        out[f"sing-{name}-door"] = {"pan": round(pan, 3), "fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.door", "amount": 1}]}}], "auto": {"door": {"points": lane}}}
    for i, (n, t_in, t_out) in enumerate(house_stages()):          # v11: with people in the room the pipes in its walls are struck by what is left of the echoes
        more = -float(WALL[:-2]) * HOUSE_FULL * n
        if i == 0:
            for name in ("left", "right"):
                out[f"sing-{name}-door"] = {**out[f"sing-{name}-door"], "auto": {"door": {"points": house_lane(lane, 0)}}}
            continue
        for side, own, other in (("l", a, "r"), ("r", b, "l")):
            out[f"hear{i}-{side}"] = {"fx": [{"type": "eq", "bands": ABSORB}],
                                      "returns": [{"from": "click", "gain": f"{float(FIRST['click'][:-2]) - more:g}dB", "time": f"{own}/16"}, {"from": f"hear{i}-{other}", "gain": f"{float(WALL[:-2]) - more:g}dB", "time": f"{own}/16"}],
                                      "out": "hear-shut"}
        for name, src, pan in (("left", f"hear{i}-l", -SING_PAN), ("right", f"hear{i}-r", SING_PAN)):
            ms = 1000 / hz(WALL_NOTE[name])
            back = f"{-60 * ms / 1000 / SING_RING:.2f}dB"
            for side, other in (("a", "b"), ("b", "a")):
                out[f"sing{i}-{name}-{side}"] = {"fx": [{"type": "eq", "bands": SING_DAMP}],
                                                "returns": [{"from": src, "gain": "0dB", "time": f"{ms - PIPE_TRIM:.3f}ms"}, {"from": f"sing{i}-{name}-{other}", "gain": back, "time": f"{ms - PIPE_TRIM:.3f}ms"}],
                                                "out": f"sing{i}-{name}-door"}
            out[f"sing{i}-{name}-door"] = {"pan": round(pan, 3), "fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.door", "amount": 1}]}}], "auto": {"door": {"points": house_lane(lane, i)}}}
    return out


def buses():
    out = {}
    for room, a, b, b0, b1, opn, shut in places():
        door = {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.door", "amount": 1}]}}
        lane = {"door": {"points": door_lane(b0, b1, opn, shut)}}
        for side, own, other, pan in (("l", a, "r", -0.85), ("r", b, "l", 0.85)):
            out[f"{room}-{side}"] = {"fx": [{"type": "eq", "bands": ABSORB}],
                                     "returns": [{"from": p, "gain": g, "time": f"{own}/16"} for p, g in FIRST.items()] + [{"from": f"{room}-{other}", "gain": WALL, "time": f"{own}/16"}],
                                     "out": f"{room}-door-{side}"}
            out[f"{room}-door-{side}"] = {"pan": pan, "fx": [door], "auto": lane, "out": "walls"}
    for i, (n, t_in, t_out) in enumerate(house_stages()):          # v11: the same room with people in it
        room = next(x for x in SECS if x[0] == HOUSE_IN)[4]
        (a, b), = WALK[room]
        more = -float(WALL[:-2]) * HOUSE_FULL * n                 # dB more that every wall takes from every echo
        if i == 0:
            base = out[f"{room}-door-l"]["auto"]["door"]["points"]
            for side in "lr":
                out[f"{room}-door-{side}"] = {**out[f"{room}-door-{side}"], "auto": {"door": {"points": house_lane(base, 0)}}}
            continue
        for side, own, other, pan in (("l", a, "r", -0.85), ("r", b, "l", 0.85)):
            out[f"{room}{i}-{side}"] = {"fx": [{"type": "eq", "bands": ABSORB}],
                                        "returns": [{"from": p, "gain": f"{float(g[:-2]) - more:g}dB", "time": f"{own}/16"} for p, g in FIRST.items()] + [{"from": f"{room}{i}-{other}", "gain": f"{float(WALL[:-2]) - more:g}dB", "time": f"{own}/16"}],
                                        "out": f"{room}{i}-door-{side}"}
            out[f"{room}{i}-door-{side}"] = {"pan": pan, "fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.door", "amount": 1}]}}], "auto": {"door": {"points": house_lane(base, i)}}, "out": "walls"}
    out.update(pipe_buses())
    if SING:
        out.update(sing_buses())
    out["walls"] = {"fx": [{"type": "width", "width": {"value": 0.0, "mod": [{"src": "auto.apart", "amount": 1}]}}], "auto": {"apart": {"points": step_lane(5, 0.0)}}}
    out["air"] = {"fx": ["reverb kind=hall decay=5.5s size=1 mix=1 predelay=40ms", "lp cutoff=6000", "hp cutoff=300",
                         {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.far", "amount": 1}]}}],
                  "returns": [{"from": "click", "gain": "0dB", "time": "6ms"}, {"from": "tock", "gain": "-2dB", "time": "6ms"}],
                  "auto": {"far": {"points": step_lane(6, CLOSED, glide=4)}}}
    for i, (n, t_in, t_out) in enumerate(house_stages()):
        far = step_lane(6, CLOSED, glide=4)
        if i == 0:
            out["air"] = {**out["air"], "auto": {"far": {"points": house_lane(far, 0)}}}
        else:                                                      # the hall's wash dies 1 + FULL n times as fast; it is sent no less (a click's wash begins as loud in a full room: only what is left of it later is less)
            out[f"air{i}"] = {"fx": [f"reverb kind=hall decay={AIR_DECAY / (1 + HOUSE_FULL * n):.3g}s size=1 mix=1 predelay=40ms", "lp cutoff=6000", "hp cutoff=300",
                                     {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.far", "amount": 1}]}}],
                              "returns": [{"from": "click", "gain": "0dB", "time": "6ms"}, {"from": "tock", "gain": "-2dB", "time": "6ms"}],
                              "auto": {"far": {"points": house_lane(far, i)}}}
    out["dub"] = {"fx": [{"type": "delay", "time": "3/16", "feedback": {"value": 0.5, "mod": [{"src": "auto.breath", "amount": 1}]}, "mix": 1, "tone": 2000}, "hp cutoff=300",
                         "reverb kind=hall decay=3s mix=0.3"], "auto": {"breath": {"points": breath_lane()}}}
    return out


KICK = lambda bar: [(s, "A1", 1, 0.95 if s == 0 else 0.9) for s in (0, 4, 8, 12)]
CLICK = lambda bar: [(2 + dist(bar), "A5", 1, 0.9)] if SQUARE else [(2, "A5", 1, 0.9)]             # CLICK_STEP, and as late as it is far
TOCK = lambda bar: [(11, "D5" if bar % 4 == 1 else "F5", 1, 0.8)] if bar % 2 else []   # outside: every other bar
TOCK_STEP = 11                 # in a room: from this step of the section's first bar, every 2 * (a + b) sixteenths


def tock_notes():
    out = []
    for name, b0, n, parts, room, width, air in SECS:
        if "tock" not in parts:
            continue
        if room is None:
            for bar in range(b0, b0 + n):
                if plays("tock", bar):
                    out += [note(bar * BEATS + s * STEP, p, ln * STEP, v) for s, p, ln, v in TOCK(bar)]
            continue
        a, b = ROOMS[room]
        k, at = 0, b0 * 16 + TOCK_STEP
        while at < (b0 + n) * 16:
            out.append(note(at * STEP, "D5" if k % 4 == 3 else "F5", 1 * STEP, 0.8)); k += 1; at += 2 * (a + b)
    return out
BASS = lambda bar: [(2, "D2", 1.5, 0.9), (6, "D2", 1.5, 0.8), (10, "D2", 1.5, 0.9), (14, ("C2", "D2", "F2", "A1")[(bar // 2) % 4] if bar % 2 else "D2", 1.5, 0.8)]
CLAP = lambda bar: [(4, "C4", 1, 0.8), (12, "C4", 1, 0.86)]
CLICK_STEP = 2


def learnt():
    """The bass's bar once it has learnt the room: the click's step, then every step of the same bar on which a wall sends it back."""
    a, b = WALK[LEARN_ROOM][0]
    out = [(CLICK_STEP, WALL_NOTE["click"], 1.5, 0.92)]
    for t, side in echoes(a, b):
        if CLICK_STEP + t < 16:
            out.append((CLICK_STEP + t, WALL_NOTE[side], 1.5, round((0.88 if side == "both" else 0.8) * (1.0 if t <= a + b else 0.9), 3)))
    return out


def has_learnt(bar):
    name, b0, n, parts, room, width, air = section_of(bar)
    if room == LEARN_ROOM:
        return bar >= b0 + LEARN_AFTER * ROW
    return bar >= b0 and room is None and any(s[4] == LEARN_ROOM and s[1] < b0 for s in SECS)


def bass_bar(bar):
    return learnt() if LEARN and has_learnt(bar) else BASS(bar)


def away_lane():
    """dB on the bass: 0 until the walk is out of the door, then falling to AWAY over the CARRY bars it carries the room."""
    b0 = next(s[1] for s in SECS if s[4] is None and any(t[4] == LEARN_ROOM and t[1] < s[1] for t in SECS))
    return [pt(0, 0), pt(b0, 0), pt(b0 + CARRY, AWAY), pt(BARS, AWAY)]


def stand_lane():
    """Where the dry click stands between the walls, -1 at the left wall, +1 at the right, 0 outside: (a - b) / (a + b)."""
    ev = []
    for name, b0, n, parts, room, width, air in SECS:
        if room is None:
            ev.append((b0, 0.0, OPEN))
    ev += [(b0, (a - b) / (a + b), opn) for room, a, b, b0, b1, opn, shut in places()]
    ev.sort()
    pts, last = [pt(0, ev[0][1])], ev[0][1]
    for b0, v, glide in ev[1:]:
        if v != last:
            pts += [pt(b0, last), pt(b0 + glide, v)]
        last = v
    pts.append(pt(BARS, last))
    return pts
CHORDS = [("D3", "F3", "A3", "C4", "E4"), ("Bb2", "D3", "F3", "A3", "C4")]
CHORD = lambda bar: [(6, p, 2, 0.85) for p in CHORDS[(bar // 8) % 2]] if bar % 4 == 0 else []

PATCHES = {
    "sr-kick": {"about": "Standing Room's bass drum (chirper-zero, 26 Nov): the engine's machine kick, short and dry, on A1. It is not in any room.",
                "play": {"vel_sens": 0.3},
                "synth": {"layers": [{"type": "machine", "machine": {"part": "kick", "decay": "260ms", "click": 0.6, "drive": 0.35, "punch": 22, "punch_time": "32ms"}}],
                          "filters": ["hp cutoff=28"], "amp": {"a": "0.1ms", "d": "0s", "s": 1, "r": "1s"}}},
    "sr-click": {"about": "Standing Room's click (chirper-zero, 26 Nov): the machine's rim with a breath of white noise, 40 ms, above 500 Hz and lifted 6 dB round 11 kHz: bright enough that a wall can take its top away.",
                 "play": {"vel_sens": 0.4},
                 "synth": {"layers": [{"type": "machine", "machine": {"part": "rim", "decay": "45ms"}}, "white level=-3dB"], "filters": ["hp cutoff=500", "peak cutoff=11000 q=0.7 gain=6dB"],
                           "amp": {"a": "0.1ms", "d": "40ms", "s": 0, "r": "20ms", "curve": 4}}},
    "sr-tock": {"about": "Standing Room's tock (chirper-zero, 26 Nov): a wooden bar on the modal layer (after Common Measure's clave), an octave or so under the click.",
                "play": {"vel_sens": 0.5},
                "synth": {"layers": [{"type": "modal", "modes": "glock", "bright": 0.9, "damp": 0.25, "decay": "150ms", "strike": 0.5, "tilt": 0.0}],
                          "amp": {"a": "0.2ms", "d": "240ms", "s": 0, "r": "40ms"}}},
    "sr-clap": {"about": "Standing Room's clap (chirper-zero, 26 Nov): the machine's clap, three bursts, short, dry.",
                "play": {"vel_sens": 0.4},
                "synth": {"layers": [{"type": "machine", "machine": {"part": "clap", "bursts": 3, "decay": "140ms"}}], "amp": {"a": "0.1ms", "d": "0s", "s": 1, "r": "400ms"}}},
    "sr-chord": {"about": "Standing Room's dub chord (chirper-zero, 26 Nov): three saws and a square through a short filter envelope, dry; its space is the bus `dub`, a dotted-eighth echo whose feedback breathes.",
                 "synth": {"layers": ["saw unison=3 detune=0.15 spread=0.6", "square level=-8dB"], "env": {"f": {"a": "1ms", "d": "220ms", "s": 0.08, "r": "100ms"}},
                           "filters": [{"kind": "lp", "cutoff": {"value": 600, "mod": [{"src": "env.f", "amount": 2.4}, {"src": "vel", "amount": 1}]}, "q": 1.6}],
                           "amp": {"a": "1ms", "d": "300ms", "s": 0.15, "r": "150ms"}}},
}


def click_far():
    """The click's two lanes of distance: its level (dB) and what the air takes of its top (dB at 11 kHz)."""
    if not SQUARE:
        return {}
    return {"dist": {"points": dist_lane(lambda r: 0.0 if r == 0 else 20 * math.log10(NEAR / (NEAR + r)) - LIMIT)}, "dull": {"points": dist_lane(lambda r: -AIR * r)}}


def song():
    if SQUARE:
        f = PATCHES["sr-click"]["synth"]["filters"]
        i = next(k for k, x in enumerate(f) if isinstance(x, str) and x.startswith("peak cutoff=11000"))
        f[i] = {"kind": "peak", "cutoff": 11000, "q": 0.7, "gain": {"value": "6dB", "mod": [{"src": "auto.dull", "amount": 1}]}}
    pump = {"type": "pump", "on": "kick", "depth": "-5dB", "attack": "2ms", "release": "180ms", "curve": 0.7}
    doc = {
        "about": "Chirpers - Escapement, track 3 by chirper-zero: STANDING ROOM. One click a bar between two walls; a wall is a number of sixteenths there and back, so a room is a rhythm: 3 + 4 a room in seven, 2 + 3 in five, 5 + 7 in twelve, and 3 + 5, which is eight and fits the bar, where the echoes stand. A tock keeps each room's time, not the bar's. The click is in every room all the time; the song opens and shuts their doors." + (" From v2 the click walks across each room a step a row (2 + 5, 3 + 4, 4 + 3, 5 + 2 in the corridor), and in standing room it stands." if any(len(w) > 1 for w in WALK.values()) else "") + (" From v3 the bass learns the room's three-three-two (a note for the click, one for each wall) and carries it out of the door; the dry click is panned to where it stands." if LEARN else "") + (" From v4 the walls close in between the stairwell and the hangar: eight rooms too small to count, which sing a rising scale." if PIPES_ON else "") + (" From v5 the click begins 163 m off across a square and is as late, as quiet and as dull as it is far; it walks in over the first sixteen bars and away over the last sixteen." if SQUARE else "") + " Generated by compose/chirpers11/src/chirpers11-t3.py.",
        "tempo": BPM,
        "ceiling": "-1dB",
        "loudness": -11.0,
        "seed": 1,
        "tail": "3s",
        "length": f"{TOTAL}b",
        "event_stable": True,
        "patches": PATCHES,
        "buses": buses(),
        "master": {"fx": [{"type": "eq", "bands": ["hp cutoff=30"]}, {"type": "compressor", "threshold": "-18dB", "ratio": 2, "attack": "20ms", "release": "160ms", "makeup": "0dB"}]},
        "tracks": [
            {"name": "kick", "patch": "sr-kick", "gain": "-8dB", "pan": 0.0, "notes": part("kick", KICK)},
            {"name": "click", "patch": "sr-click", "gain": "2dB", **({"pan": {"value": 0, "mod": [{"src": "auto.stand", "amount": PAN}]}, "auto": {"stand": {"points": stand_lane()}, **click_far()}} if LEARN else {"pan": 0.0}),
             **({"fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dist", "amount": 1}]}}]} if SQUARE else {}), "notes": part("click", CLICK)},
            {"name": "tock", "patch": "sr-tock", "gain": "-3dB", "pan": 0.0, "notes": tock_notes()},
            {"name": "bass", "patch": "sub-sine params.grit=0.8", "gain": "-14dB", "pan": 0.0, "fx": [pump] + ([{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.away", "amount": 1}]}}] if LEARN else []), **({"auto": {"away": {"points": away_lane()}}} if LEARN else {}), "notes": part("bass", bass_bar)},
            {"name": "clap", "patch": "sr-clap", "gain": "-4dB", "pan": 0.0, "notes": part("clap", CLAP)},
            {"name": "chord", "patch": "sr-chord", "gain": "-22dB", "pan": 0.0, "fx": [pump], "sends": {"dub": "-3dB"}, "notes": part("chord", CHORD)},
        ],
    }
    if PASS and passes():
        PATCHES["sr-pass"] = {"about": "Standing Room's bell on the thing that goes past (chirper-zero, 26 Nov, v7): a small dry bell, a sine with its octave and twelfth, 120 ms, whose pitch is given by how fast the thing is closing (auto.dop, semitones). It is in no room.",
                              "play": {"vel_sens": 0.3},
                              "synth": {"layers": ["sine", "sine ratio=2 level=-9dB", "sine ratio=3 level=-15dB"], "pitch": {"value": 0, "mod": [{"src": "auto.dop", "amount": 1}]},
                                        "amp": {"a": "0.5ms", "d": "120ms", "s": 0, "r": "40ms", "curve": 3}}}
        doc["tracks"].append({"name": "pass", "patch": "sr-pass", "gain": PASS_GAIN, "pan": {"value": 0, "mod": [{"src": "auto.side", "amount": PASS_PAN}]},
                              "auto": {nm: {"points": pass_lane(i), **({"curve": 0} if STRAIGHT else {})} for nm, i in (("dop", 2), ("near", 3), ("side", 4))},
                              "fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.near", "amount": 1}]}}],
                              "notes": [note(q[0] * STEP, q[5], 1 * STEP, 0.8) for q in passes()]})
        if PASS_AGAIN:
            doc["about"] = doc["about"].replace(" Generated by", " From v8 it goes past again in the door, the other way and at a third of the speed of sound: three against two as it comes, three against four when it has gone, and its note falls an octave. Generated by")
            assert "From v8" in doc["about"]
        if PASS_TICK:
            PATCHES["sr-pass-tick"] = {"about": "Standing Room's clack, of the thing that goes past (chirper-zero, 26 Nov, v7): the click's own rim and breath, shorter and with everything under 3 kHz taken off, on every stroke of the bell and at the bell's distance and side.",
                                       "play": {"vel_sens": 0.3},
                                       "synth": {"layers": [{"type": "machine", "machine": {"part": "rim", "decay": "30ms"}}, "white level=-3dB"], "filters": ["hp cutoff=3000", "peak cutoff=11000 q=0.7 gain=6dB"],
                                                 "pitch": {"value": 0, "mod": [{"src": "auto.dop", "amount": 1}]}, "amp": {"a": "0.1ms", "d": "25ms", "s": 0, "r": "15ms", "curve": 4}}}
            doc["tracks"].append({**doc["tracks"][-1], "name": "pass-tick", "patch": "sr-pass-tick", "gain": PASS_TICK})
        doc["about"] = doc["about"].replace(" Generated by", " From v7 something goes past outside, a sixteenth of sound away at a fifth of the speed of sound, striking straight eighths on one note: its strokes are heard five against four and a major third high as it comes, five against six and a minor third low when it has gone (the Doppler effect, of a rhythm and of a pitch at once). Generated by")
        assert "From v7" in doc["about"]
    if house_stages():
        doc["about"] = doc["about"].replace(" Generated by", " From v11 standing room fills with people, twice, in its last two rows, and by Sabine's law every person takes the same bite from every echo: a wall takes 3 dB from an echo in the empty room, 6 with half a house, 9 with a full one, and the hall's wash dies in a half and then a third of the time. Generated by")
        assert "From v11" in doc["about"]
    if CHIRP and chirp_notes()[0]:
        claps, back = chirp_notes()
        PATCHES["sr-step"] = {"about": "Standing Room's tick (chirper-zero, 26 Nov, v10): 5 ms of a sine, started at the same point of its wave every time: a clap, and each step's echo of it. Its loudness is its velocity (vel_sens 0.5 is linear).",
                              "play": {"vel_sens": 0.5, "gate": 1},
                              "synth": {"layers": ["sine phase=0"], "amp": {"a": "0ms", "d": "5ms", "s": 0, "r": "2ms", "curve": 3}}}
        doc["tracks"].append({"name": "clap-at", "patch": "sr-step", "gain": f"{CHIRP_GAIN:g}dB", "pan": 0.0, "notes": claps})                       # dry: the stairs are the room
        doc["tracks"].append({"name": "stairs", "patch": "sr-step", "gain": f"{CHIRP_GAIN + CHIRP_BACK:g}dB", "pan": 0.25, "notes": back})          # ahead and a little to the right
        doc["about"] = doc["about"].replace(" Generated by", " From v10 there are stairs in the stairwell: a clap at their foot comes back as a chirp, because each of sixty steps sends its own echo and the higher ones are further apart in time (D5 falling towards A4 in an eighth of a second); you walk to the stairs, so the chirp comes sooner and falls further. Generated by")
        assert "From v10" in doc["about"]
    if stand_span():
        lo, hi = stand_span()
        PATCHES["sr-mode"] = {"about": "Standing Room's mode (chirper-zero, 26 Nov, v9): one sine, held: a note whose half-waves fit between the walls. Its loudness is where the ear is (auto.at, dB).",
                              "synth": {"layers": ["sine phase=0"], "amp": {"a": "400ms", "d": "0s", "s": 1, "r": "1.5s"}}}
        for n, pitch in STAND_MODES:
            for nm, side in (("l", -1), ("r", 1)):
                doc["tracks"].append({"name": f"mode-{n}-{nm}", "patch": "sr-mode", "gain": f"{STAND_GAIN + STAND_TILT * math.log2(n / STAND_MODES[0][0]):.2f}dB", "pan": side,
                                      "auto": {"at": {"points": mode_lane(n, side), "curve": 0}},
                                      "fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.at", "amount": 1}]}}],
                                      "notes": [note(lo, pitch, hi - lo + STAND_HOLD, 0.8)]})
        doc["about"] = doc["about"].replace(" Generated by", " From v9 there is a standing wave in standing room: five held notes that fit between its walls, each as loud as it is where the ear is, and for three rows you walk from one wall to the other: the chord changes with where you stand and the top notes pass from ear to ear. Generated by")
        assert "From v9" in doc["about"]
    if SING:
        doc["about"] = doc["about"].replace(" Generated by", " From v6 there is a pipe in each wall of standing room, tuned to that wall's note, and one where the click stands: the click and its echoes strike them, so the room sings the bass's line (D, F from the left, C from the right) and for one row the bass rests under it. Generated by")
        assert "From v6" in doc["about"]
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


def passes():
    """Every stroke of what goes past, as it is heard: (the sixteenth it is heard on, the sixteenth it was struck on, semitones it is
    heard sharp by, dB from its level at its closest, its side from -1 to 1)."""
    out = []
    todo = [(name, at, lo, hi, way, PASS_V, PASS_NOTE, PASS_SHARP) for name, (at, lo, hi, way) in PASS_IN.items()] if PASS else []
    if PASS_AGAIN:
        todo.append((AGAIN["sec"], AGAIN["at"], AGAIN["lo"], AGAIN["hi"], AGAIN["way"], AGAIN["v"], AGAIN["note"], AGAIN["sharp"]))
    for name, at, lo, hi, way, vel, pitch, sharp in todo:
        sec = next((x for x in SECS if x[0] == name), None)
        if sec is None:
            continue
        s0, t_lo, t_hi = (sec[1] + at) * 16, (sec[1] + lo) * 16, (sec[1] + hi) * 16
        for k in range(-600, 600):
            s = s0 + k * PASS_EVERY
            x = vel * (s - s0)                   # sixteenths of sound along its line from where it is closest
            r = math.hypot(PASS_NEAR, x)         # ... and from here
            t = s + r                            # a sixteenth of sound takes a sixteenth
            if t_lo <= t < t_hi:
                fade = PASS_FADE_DB * max(0.0, 1 - (t - t_lo) / (PASS_FADE * 16), 1 - (t_hi - t) / (PASS_FADE * 16))
                out.append((t, s, -12 * math.log2(1 + vel * x / r) + sharp, 20 * math.log10(PASS_NEAR / r) + fade, way * x / r, pitch))
    return sorted(out)


def pass_lane(i):
    """A lane through one of those at every stroke: 2 the note, 3 the level, 4 the side. Between strokes it goes straight, as the thing does."""
    p = passes()
    return [["0b", round(p[0][i], 3)]] + [[f"{t * STEP:.4f}b", round(q[i], 3)] for q in p for t in [q[0]]] + [[f"{TOTAL:g}b", round(p[-1][i], 3)]]


def echoes(a, b, n=16):
    """Where one click's returns fall, in sixteenths after it: (step, side)."""
    out, k = [], 1
    while len(out) < n:
        t = (k // 2) * (a + b)
        out += [(t, "both")] if k % 2 == 0 else [(t + a, "left"), (t + b, "right")]
        k += 1
    return sorted(out)[:n]


if __name__ == "__main__":
    if os.environ.get("C11T3_SHOW"):
        sec = 60 / BPM * BEATS
        for name, b0, n, parts, room, width, air in SECS:
            print(f"{name:14s} bars {b0:3d}-{b0 + n:3d}  {int(b0 * sec) // 60}:{b0 * sec % 60:04.1f}-{int((b0 + n) * sec) // 60}:{(b0 + n) * sec % 60:04.1f}  room {room or '-':10s} width {width}  air {air}  {', '.join(sorted(parts))}")
        for room, a, b, b0, b1, opn, shut in places():
            print(f"{room:11s} bars {b0:5.1f}-{b1:5.1f}  {a} + {b} = {a + b}: a click on step 2 comes back on steps " + " ".join(f"{(2 + t) % 16}{'' if s == 'both' else s[0]}" for t, s in echoes(a, b, 12)) + f" ; the tock every {2 * (a + b)} sixteenths, round every {math.lcm(2 * (a + b), 16) // 16} bar(s)")
        for name, p, ms, b0, b1 in pipes():
            print(f"{name:11s} bars {b0:5.1f}-{b1:5.1f}  {p:3s} {hz(p):6.1f} Hz: the walls {ms:.2f} ms away and back; they give back {-60 * ms / 1000 / PIPE_RING:.2f} dB less each time")
        if SQUARE:
            ms = 60000 / BPM / 4
            for nm, sc in (("coming", SECS[0]), ("going", SECS[-1])):
                print(f"   across the square, {nm} (bars {sc[1]}-{sc[1] + sc[2]}): bar: sixteenths away (m), heard on sixteenth, dB, top dB: " + " ; ".join(
                    f"{b + 1}: {dist(b):.2f} ({dist(b) * ms / 1000 * SOUND:.0f} m) {2 + dist(b):.2f} {20 * math.log10(NEAR / (NEAR + dist(b))):+.1f} {-AIR * dist(b):+.1f}" for b in range(sc[1], sc[1] + sc[2], 3)))
        if SING:
            (b0, b1), (r0, r1) = sing_bars()
            print(f"the walls sing from bar {b0} to bar {b1} (the bass rests from {r0} to {r1}): " + " ; ".join(
                f"{nm}: {WALL_NOTE[nm]} {hz(WALL_NOTE[nm]):.1f} Hz, a pipe {1000 / hz(WALL_NOTE[nm]):.2f} ms there and back, giving back {-60 / hz(WALL_NOTE[nm]) / SING_RING:.2f} dB less each time" for nm in ("click", "left", "right")))
            a, b = WALK[LEARN_ROOM][0]
            print("   what strikes them in a bar (step: the pipe, dB at the pipe): " + " ".join(
                [f"{CLICK_STEP}:D {FIRST['click']}"] + [f"{CLICK_STEP + t}:{'F+C' if sd == 'both' else 'F' if sd == 'left' else 'C'} {float(FIRST['click'][:-2]) + float(WALL[:-2]) * (2 * (t // (a + b)) - (1 if sd == 'both' else 0) ):+.0f}" for t, sd in echoes(a, b) if CLICK_STEP + t < 16]))
        if house_stages():
            st = house_stages(); room = next(x for x in SECS if x[0] == HOUSE_IN)[4]; (wa, wb), = WALK[room]; bounce = (wa + wb) / 2 * STEP * 60 / BPM
            print(f"standing room only: people come in " + " and ".join(f"over bars {int(st[i][2] // BEATS) + 1}-{int(st[i + 1][1] // BEATS)} (to {st[i + 1][0]:g} of a house, held from bar {int(st[i + 1][1] // BEATS) + 1})" for i in range(len(st) - 1)) + f" ; a full house swallows {HOUSE_FULL:g} times what the empty room does")
            for i, (n, t_in, t_out) in enumerate(st):
                loss = -float(WALL[:-2]) * (1 + HOUSE_FULL * n)
                print(f"   {n:g} of a house ({'the room as it was' if i == 0 else 'buses ' + room + str(i) + '-l/-r and air' + str(i)}): a wall takes {loss:g} dB from an echo each time: the echoes die 60 dB in {60 / loss * bounce:.2f} s (a wall every {1000 * bounce:.0f} ms on average) ; the first echo {float(FIRST['click'][:-2]) + float(WALL[:-2]) * HOUSE_FULL * n:g} dB ; the air's decay {AIR_DECAY / (1 + HOUSE_FULL * n):.2f} s")
        if CHIRP and chirp_notes()[0]:
            claps, back = chirp_notes(); b0 = next(x for x in SECS if x[0] == CHIRP_IN)[1]
            nt = lambda f: (lambda m: "C C# D Eb E F F# G Ab A Bb B".split()[int(round(m)) % 12] + str(int(round(m)) // 12 - 1) + f"{100 * (m - round(m)):+.0f}c")(69 + 12 * math.log2(f / 440))
            print(f"the stairs, bars {int(claps[0]['at'] // BEATS) + 1}-{int(claps[-1]['at'] // BEATS) + 1}: {CHIRP_STEPS} steps, tread {100 * CHIRP_TREAD:.1f} cm, riser {100 * CHIRP_RISER:.1f} cm ({math.degrees(math.atan2(CHIRP_RISER, CHIRP_TREAD)):.0f} degrees) ; {len(claps)} claps on sixteenth {','.join(str(q) for q in CHIRP_ON)} ; {len(back)} echoes ; at the foot {SOUND / (2 * CHIRP_TREAD):.1f} Hz, far up the slope {SOUND / (2 * math.hypot(CHIRP_TREAD, CHIRP_RISER)):.1f} Hz")
            for c0, c1, away in CHIRP_AWAY:
                d = away * (60 / BPM / 4) * SOUND / 2; e = stair_echoes(d); g = [b[0] - a[0] for a, b in zip(e, e[1:])]
                print(f"   bars {b0 + c0 + 1}-{b0 + c1}: the foot {d:.2f} m off: the chirp begins {1000 * e[0][0]:.1f} ms after the clap ({e[0][0] * BPM / 15:.3f} of a sixteenth) and lasts {1000 * (e[-1][0] - e[0][0]):.1f} ms ; its echoes come {1 / g[0]:.1f} Hz ({nt(1 / g[0])}) at first, {1 / g[len(g) // 2]:.1f} half way ({nt(1 / g[len(g) // 2])}), {1 / g[-1]:.1f} at the last ({nt(1 / g[-1])}): {12 * math.log2(g[-1] / g[0]):.2f} semitones down ; the last echo is {20 * math.log10(e[-1][1]):.1f} dB under the first")
        if stand_span():
            lo, hi = stand_span(); L = SOUND / (2 * STAND_ROOT)
            print(f"the standing wave, bars {lo // BEATS + 1:g}-{hi // BEATS:g}: walls {L:.2f} m apart (the room's note {STAND_ROOT:.1f} Hz), ears {STAND_EAR * 100:.0f} cm apart ; modes " + " ".join(f"{n}:{p}" for n, p in STAND_MODES) + " ; a mode at a wall " + " ".join(f"{STAND_GAIN + STAND_TILT * math.log2(n / STAND_MODES[0][0]):.1f}" for n, p in STAND_MODES) + " dB")
            for q in (0, 1 / 8, 1 / 6, 1 / 4, 1 / 3, 1 / 2, 2 / 3, 3 / 4, 1):
                t = lo + (hi - lo) * q
                print(f"   bar {t / BEATS + 1:6.2f}: the head {100 * (stand_at(t, -1) + stand_at(t, 1)) / 2:5.1f}% of the way across ; left ear / right ear dB: " + " ; ".join(f"{p} {stand_db(n, t, -1):+6.1f} / {stand_db(n, t, 1):+6.1f}" for n, p in STAND_MODES))
        if PASS and passes():
            p, ms = passes(), 60000 / BPM / 4
            for name, (at, lo, hi, way), PASS_V, PASS_NOTE in [(nm, v_, PASS_V, PASS_NOTE) for nm, v_ in PASS_IN.items()] + ([(AGAIN["sec"], (AGAIN["at"], AGAIN["lo"], AGAIN["hi"], AGAIN["way"]), AGAIN["v"], AGAIN["note"])] if PASS_AGAIN else []):
                b0 = next(x[1] for x in SECS if x[0] == name)
                q = [x for x in p if (b0 + lo) * 16 <= x[0] < (b0 + hi) * 16]
                gap = lambda a, b: (b[0] - a[0]) / PASS_EVERY
                print(f"what goes past in {name}: {'left to right' if way > 0 else 'right to left'}, at {PASS_V * SOUND:.1f} m/s, {PASS_NEAR * ms / 1000 * SOUND:.0f} m away at its closest, which is on the first beat of bar {b0 + at + 1:g} "
                      f"and heard on sixteenth {((b0 + at) * 16 + PASS_NEAR) % 16:g} of it ; {len(q)} strokes heard from bar {q[0][0] / 16 + 1:.2f} to bar {q[-1][0] / 16 + 1:.2f}")
                print(f"   its first two strokes are {gap(q[0], q[1]):.4f} of an eighth apart, heard {q[0][2]:+.2f} semitones from {PASS_NOTE} ({q[0][3]:+.1f} dB, side {q[0][4]:+.2f}) ; "
                      f"its last two {gap(q[-2], q[-1]):.4f}, {q[-1][2]:+.2f} ({q[-1][3]:+.1f} dB, side {q[-1][4]:+.2f}) ; closest: " + " ".join(f"[{x[0] / 16 + 1:.3f}: {x[2]:+.2f} st {x[3]:+.1f} dB {x[4]:+.2f}]" for x in q if abs(x[1] - (b0 + at) * 16) <= 2 * PASS_EVERY))
        if LEARN:
            print("the bass once it has learnt the room: " + " ".join(f"{st}:{p}" for st, p, n, v in learnt()) + f" ; from bar {next(b for b in range(BARS) if has_learnt(b))} to bar {max(b for b in range(BARS) if has_learnt(b) and plays('bass', b)) + 1}")
            print("the dry click's pan: " + " ".join(f"{p[0]}={p[1] * PAN:+.2f}" for p in stand_lane()))
        print(f"{BARS} bars, {TOTAL} beats, {BARS * sec:.1f} s")
    else:
        open(OUT, "w").write(dump(song()))
