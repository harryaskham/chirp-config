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

v12 (26 Nov): THE ROOM CLAPS (C11T3_CROWD=0 takes it out: v11). v11 filled the room with people. Now they clap,
and how a crowd comes to clap as one is a measured thing (Neda and others, 2000, with microphones in concert
halls): applause is everyone clapping fast, each at a rate of his own, and it is noise; it turns into one clap
when people HALVE their rate, because slow clapping is far more even from one person to the next, and then each
is pulled toward what he hears. It is Kuramoto's arithmetic: a phase a person, each with a rate of its own and a
pull toward the beat, and when the pull is stronger than the spread of the rates they lock.
Here: 32 people, each with a place (eight across, four rows back: 2, 4, 6 and 8 m away; a row back is half as
loud again and 6 ms later, which is the speed of sound). The first sixteen are the half house, in by bar 141:
from then, one after another, they clap twice a beat, each up to a tenth off that rate and nobody with anybody
(bars 141 to 144: applause). From bar 145, one by one, each halves his rate and is pulled to the beat, and the
second sixteen, who are coming in, start at the slow rate; the pull grows until the house is full (bar 149).
Bars 149 to 152: one clap on every beat, 32 pairs of hands, the back row 17 ms behind the front. Then the door.
Nothing is random: every person's rate, first clap and moment of halving are taken from the golden ratio.
A hand is a 9 ms burst of noise with nothing under 1.5 kHz: `compscore --bands` said this song has 6 to 13 dB
less than the rest of the record from 8 to 15 kHz, and applause is what that is.

v13 (26 Nov): THE CORRIDOR'S OTHER TWO WALLS (C11T3_FLUT=0 takes it out: v12). The corridor has had two walls
since v1: its ends, a long way off, which send the click back as an echo you can count. It has two more, the
ones beside you, 2.34 m apart, and a click between two close hard walls does not echo: it RATTLES (a flutter
echo), going across and back 73 times a second, which is the note D2. Standing in the middle the click comes
off both walls at once, twice in each crossing: the rattle is an octave up (D3) and in the middle of the head.
Step toward the left wall and the left wall's click comes first and the right wall's later: the rattle drops an
octave, leans left (the first arrival wins), and its colour changes with every step, because two clicks
t apart in every 13.6 ms take out the partials of D2 at odd multiples of 1 / 2t.

ALSO, THE CLICK'S REPAIR (C11T3_TRIM=0 leaves the click as it was): `compscore --bands` said this song has 10 dB
more than the rest of the record at 880 Hz and 12 dB less at 15 kHz. Each part read alone: the click owns both
(a third of its power is at its own note, A5; and it is the only part with anything over 10 kHz). It is turned
down 5 dB at 880 Hz and up 6 dB round 15 kHz, on a lane that is nought in the first four bars and the last
eight (the seams).

v14 (27 Nov): ZENO'S BALL (C11T3_BALL=0 takes it out: v13). A small light ball is let fall, nine times, and each
time it comes to rest EXACTLY on a bar line where the song goes through a door or turns a row. A ball that keeps
the same share of its speed at every bounce (here 2 ** (-1/6): 0.891, about a table-tennis ball's) makes flights
that shrink by that share every time, so the bounces come twice as fast every six, and infinitely many of them
fit into a finite time: the first flight divided by (1 - 0.891). That time is set to seven and a quarter beats,
so the first bounce is on the fourth sixteenth of a bar and the last is the bar line two bars on. Each bounce
is quieter by the same share (1.0 dB), as a real one is. The first flight (376 ms) says how far it fell: 22 cm.
It is SPACE twice over: the ball reaches the walls as the click and the tock do (it is in FIRST), so every room
answers the same ball with its own echoes and its own air, and outside nothing answers; and it rolls from one
side to the other as it bounces.
WHY NOW, said plainly: the album's scorer read this song 0.890 like Least Common (two songs at 126 on D, with
6.44 and 6.39 onsets a second), and I owed chirper-one the move. The ball's bounces fall between the song's
sixteenths, where the scorer can see them. Its note is A6, the fifth: on D6 (the first version) it made the
two songs MORE alike in their notes (0.715 to 0.744), and with a bounce keeping 0.841 it gave fewer bounces
the scorer could see (6.576 a second).

v15 (27 Nov): A BIRD IN THE HANGAR (C11T3_BIRD=0 takes it out: v14). For the hangar's first eight bars the drum
and the bass rest, and there is only the click and what the hangar gives back. Now something small is flying in
there. It goes round in a circle 6 m across the radius whose centre is 4 m in front of you: so it passes 2 m
behind your head and 10 m out in front, once every two bars (four times round in the eight bars), at 9.9 m/s,
which is a swallow's cruising speed. It calls every three sixteenths, two notes, E then A.
Nothing about where it is has been written by hand: there is no pan, no fader move, no detune. The engine's
`orbit` effect (Chowning's moving source, 1971) is given the circle and works out, sample by sample, how long the
sound takes to reach each ear (so the call arrives up to 0.6 ms sooner at the nearer ear, and is flat going away
and sharp coming back: a third of a semitone each way), how much the head shadows it, and how far it is (five
times as far in front as behind: 14 dB).
The calls go to the hangar's air as well, so the hangar answers them.

v16 (27 Nov): A FOURTH, A FIFTH, AN OCTAVE GO BY (C11T3_FLY=0 takes it out: v15). Something that passes you
is heard higher coming than going, and the interval says how fast it went: (c + v) / (c - v) here (the engine
moves the source and lets the time to each ear follow, so the note is f(1 + v/c) coming and f(1 - v/c) going).
A fourth (4/3) is a seventh of the speed of sound, a fifth (3/2) is a fifth of it, an octave (2) is a third of
it: 49, 69 and 114 metres a second. Three things go by in the hangar, left to right, one on each of the bar
lines 87, 88 and 89 (the last two bars the drum rests, and the line it comes back on), each faster than the
last, and each comes on the note the one before left on: A7 to E7, E7 to A6, A6 to A5. The last lands on the
click's own note as the drum comes in. None of them sings any of those notes: the third one's own note is E6.
They pass FLY_DIST metres in front on a line FLY_RADIUS metres out to each side (the engine's orbit, path
"line"); the speed is raised by the little the ends of that line are short of straight ahead.

v17 (27 Nov): THE BUILDING ACROSS THE SQUARE HUMS (C11T3_NEXT=0 takes it out: v16). Through "the door" you
walk away across the square and the click you left falls behind (10 m at bar 153, 163 m at bar 168). You are
walking TOWARDS something: the next building. A building has a sound of its own from outside: its transformers
and its lights hum at twice the mains and at the multiples of that, and a wall lets the bottom of a sound
through and keeps the rest (the mass law: 6 dB more loss for every octave up). So what reaches you is two plain
tones, 120 and 180 Hz (mains at 60 to the second), the upper 3.5 dB under the lower because it is 0.585 of an
octave higher. It is in no key: 120 Hz is half way between B flat and B, 180 half way between F and F sharp.
It grows as you come: as 1 over the distance, from 173.5 m at bar 153 to 10.2 m at the end of bar 168 (as near
to the next door as bar 153 was to this one): 24.6 dB. One held note; the form is the walk.
WHY 60 AND NOT 50 (this country's mains): 100 and 150 Hz fall where the song already has sound; 120 and 180
fall in the two bands the scorer found short (its rows without a drum are empty there). That choice is the
scorer's. AND WHY NOT A NOTE: the first build was the next song's note and its fifth (B flat and F), and it
made this song's chroma like Least Common's (likeness 0.827 to 0.849, the edge is 0.85) at any level.

v18 (27 Nov): THE PIPES WHISTLE (C11T3_WHISTLE=0 takes it out: v17). Clap at the mouth of a long concrete
pipe under a road and what comes back from the far end is not a clap: it is a whistle that falls, "pyeow",
and the second echo is a longer one (Crawford's culvert whistlers, 1971). The reason is in this song
already: the click that goes straight down the pipe and back comes first; the click that glanced once off a
wall has a little farther to go, twice a little farther still: the k-th comes back after hypot(there and
back, k widths) / the speed of sound. So the clicks come thick at first and then thinner, and settle to one
for every width: a note that falls from the top of hearing to the speed of sound over the width, which is
the octave of the note the pipe already sings across itself. In "the pipes" each pipe is now 81.7 m long as
well as its width across: the click comes back from the far end on each of the three beats after it, every
time a slower fall (the n-th echo has n times as far to come), and each pipe's whistles fall towards that
pipe's note: D3, F3, G3, A3, B flat, C4, D4, E4. Nothing is bent: every whistle is clicks (the stairs' tick,
5 ms, on G4), each where the arithmetic puts it, on one dry track (`whistle`). You are stood beside the
pipe's mouth, not in it: each arrival counts as the sine of the angle it comes out at (WHISTLE_SIDE). In the
mouth the first arrivals, a millisecond apart, add up to a tick 25 dB over the whistle that follows it.

v19 (27 Nov): FASTER THAN SOUND (C11T3_SONIC=0 takes it out: v18). Three things go by in the hangar at a
seventh, a fifth and a third of the speed of sound (bar lines 87, 88, 89). The fourth goes by at TWICE the
speed of sound (the line of bar 91), striking a bell every eighth, a note higher each time: the pipes'
scale, going up (it rests for the two strokes nearest its passing). You do not hear it coming: it outruns everything it does. When it has passed, its sound
arrives all at once from where it was nearest and spreads BOTH ways. What it struck last before it passed
is heard first, and then what it struck before that: its whole coming is heard BACKWARDS, the scale
running down, from the left where it came from, each bell swelling to its stroke and stopping. At twice
the speed of sound exactly the past comes back at the tempo it happened at, so the backward bells fall on
the song's sixteenths. And what it strikes when it has gone is heard going away to the right, a third as
fast and a twelfth lower. Every time, note, level and side is worked out from where it was (the same sums
as the things that went by before it; the signs come out the other way). A stroke is as loud as it is near
and as its ring is squeezed (my reasoning from one stroke's energy, not a textbook's formula). No boom is
sounded: only its bells.

v20 (27 Nov): THE HANGAR'S OTHER TWO WALLS (C11T3_FOUR=0 takes them out: v19). Every room in this song has
had two walls, left and right, and a wall is a number of sixteenths there and back. In its last two rows
the hangar gets the wall in front and the wall behind, as far apart as the other two (12 sixteenths there
and back; you stand half way, 6 and 6). An echo that has met both pairs of walls has come back from a
CORNER, and by Pythagoras: across a and deep d, it is sqrt(a * a + d * d) sixteenths late, which is
almost never a whole number. With the click in the middle (6 + 6) the corners answer 6 * sqrt(2) = 8.49,
6 * sqrt(5) = 13.42, 12 * sqrt(2) = 16.97 and 6 * sqrt(10) = 18.97 sixteenths late: the first half way
between two sixteenths, the next nowhere, and the last two within 4 ms of a sixteenth, because 17/12 is
nearly sqrt(2) and 19/6 nearly sqrt(10). When the click steps to 7 + 5 every one of them moves, and one
corner echo lands ON a sixteenth: 5 across and 12 deep is 13. Each echo comes from where its corner is
(across / late, of the way to that side) and every wall it met takes 3 dB, as the room's walls do.

v21 (27 Nov): UNDER THE DOME (C11T3_DOME=0 takes it out: v20). Every wall in this song has been flat,
and a flat wall gives a click back once. The hall of "standing room" has a dome, and a dome like this
one (an ellipse turned round) has a FOCUS: from the click up to ANY part of it and down to that one
place on the floor is the same way round, 7 sixteenths: the curve is the one for which that is so. In
the row before the people come in (bars 129-136, which had nothing of its own) you walk to it. Two
sixteenths of sound away, the twelve parts of the dome answer one after another, those ahead of you
first and those behind you last, from all round: a rattle. With every bar it is shorter. On the focus
(the last three bars) all twelve arrive together: ONE stroke, on step 9 where nothing else in this room
strikes, made of twelve, and not one of them was played any louder: the only thing that changed is
where you stand (the Albert Hall's echo, before the mushrooms were hung in 1969; the whispering place
under any dome).

v22 (27 Nov): THE HALL'S AIR DUCT (C11T3_DUCT=0 takes it out: v21). Every wall in this song gives a
click back as a click. A pipe does not. A sound that crosses the pipe while it goes along it (half a
wave across, or two halves, or three) goes along it more slowly than the speed of sound: by
sqrt(1 - (own / f) squared), where `own` is the note that just fits across. A high note is hardly
slowed. A note near the pipe's own is slowed almost to a stop. So a click that goes down a duct and
back comes back as a note that STARTS HIGH AND FALLS, quickly at first and then more and more slowly,
towards the duct's own note, and never quite arrives (the note back at time t is own / sqrt(1 -
(back / t) squared): a culvert whistler, Crawford 1971). The hall's duct is 1.56 m across (its note
A2, 110 Hz; 220 and 330 with it), to your left, in the row before the dome (bars 121-128), and is 1,
then 3, then 5 sixteenths there and back: from the short one the note is down in a tenth of a
second; from the long one it is still coming down when the next click goes in. How far the sound has
been is how slowly it comes down.

v23 (27 Nov): THE CORRIDOR'S HANDRAIL (C11T3_RAIL=0 takes it out: v22). Sound has two speeds here:
343 m/s in the air and 5100 in steel. Put an ear to a long rail and have somebody knock on it a
long way off: the knock is heard twice, first through the steel and then through the air, and how
far apart is how far off (2.72 ms a metre: Biot measured the speed of sound in iron this way in
1808, on 951 m of water pipe in Paris, and the two knocks were 2.5 s apart). In the third of the
corridor's four rows (bars 33 to 40) somebody knocks on the handrail twice a bar, a mark further
each time (a mark is 20.4 m: what the air crosses in a thirty-second), out to 163 m and back. The
air's knock (D6, on the right) lands on sixteenths 7 and 15 every time, quieter the further off; the
steel's ring (D7, in the left ear, which is on the rail) comes before it: 56 ms before from the
nearest mark, 444 ms before from the furthest, and hardly quieter. The rail has the news first.

v24 (27 Nov): THE WHISPERING GALLERY (C11T3_GAL=0 takes it out: v23). Every wall in the song till now
sent sound back ACROSS a room. A round wall does something else with a sound made close to it: the
sound clings to the wall and goes ROUND, and hardly spreads (Rayleigh worked it out for St Paul's;
in the Gol Gumbaz at Bijapur, 38 m across, a whisper is said to come back seven times). In the
hall's first row (bars 113 to 120) the hall has such a gallery, 39 m across: 122.5 m round, which
is three sixteenths at the speed of sound. Every two bars somebody a third of the way round
whispers at the wall. Straight across (34 m) it is too faint to hear; by the wall it comes from
the LEFT a sixteenth later (the short way) and from the RIGHT a sixteenth after that (the long
way), and each comes round again every three sixteenths, seven times: left, right, nothing; left,
right, nothing: three against the bar's four, and nobody wrote a rhythm: it is where you stand.
The whisper is made half a sixteenth after the bar line, so every arrival falls between the
song's own strokes (on them, the master swallowed it: read).
It is the same 29 ms of hiss every time, sample for sample, falling 3 dB for every doubling of
the way and 1.5 dB a lap.

v25 (27 Nov): THE BASS IS HEARD ROUND THE CORNER (C11T3_BEND=0 takes it out: v24). The bass
comes in at bar 33, half way down the corridor. It was there all along: 3 m down a side passage,
round a corner that is 24 m off when the corridor begins. Sound bends round a corner into the
shadow, and low sound bends best: Maekawa's rule (1968) says the shadow takes
10 log (3 + 20 N) dB, where N counts the half waves by which the way round the corner is longer
than the straight way through the wall. So the bass is heard before it is met, its first
partial 14 dB down and every octave above about 3 dB more, and (by the corridor's own law) 9.5
dB more for the longer way; walking up to the corner the way round gets no longer than the
way through, and in the last metre the shadow lifts to 5 dB for every partial alike. At bar
33 the corner is turned. The six tones are the bass's own first six partials as measured
alone, each with its own shadow written on its fader's lane.

v26 (27 Nov): THE HANGAR'S DOOR SHUTS (C11T3_SLAM=0 takes it out: v25). On the first beat of
the hangar, where the drum and the bass rest for eight bars, the door shuts behind you, and
the row that was empty at the bottom is left with the tail. How long a sound lasts in a room
is Sabine's rule: 0.161 V / A. In a small room A is the walls. In a very big one the air
itself takes sound, and it takes far more of the high than of the low (0.4 dB a kilometre at
125 Hz, 29 at 4 kHz): 0.161 V / (S a + 4 m V). So in the hangar (245 by 245 by 20 m) the
bottom of the slam is still there after eight seconds and the top is gone in two: seven bands
of noise, each on a straight line in dB to its own time. The tail goes dark as it dies, and
that is how the size of the place is heard.

v27 (27 Nov): THE HUSH AFTER THE DOOR (C11T3_HUSH=0 takes it out: v26). v26 shut the hangar's
door and wrote the tail the hangar would leave, band by band; and measured it; and found that
the chord and its echo lay over it. Now the click, the tock, the chord and the bird wait two
bars. For 3.8 seconds there is the door's tail and nothing else: you stand still and hear
how big the place is. In that time the tail's top goes (2 s to fall 60 dB) and its bottom is
still there (9 s): the air, not the walls. Then the click walks on. Nothing is added. The
hangar's echo (its buses' doors) opens when the hush ends and not at the door: it had let in
the echoes of the last click and tock before the door, and they were read over the tail.

v28 (27 Nov): THE FOOT OF THE STAIRS (C11T3_FOOT=0 takes it out: v27). You come into the
stairwell and stop. For its first four bars the drum and the bass wait: there is the click,
the tock, and what the stairwell gives back of them (four sixteenths from one wall, one from
the other), coming up as you come in; Zeno's ball has just come to rest on that bar line.
You hear the place before you climb. In the fifth bar you clap for the first time, the stairs
answer with their falling chirp, and the drum comes back with the clap. Nothing is added.

v29 (27 Nov): WHERE IT BEGAN (C11T3_BEGAN=0 takes it out: v28). In a room that rings, a
plain tone is heard where it began (the Franssen effect). In the hangar's last two rows a
plain tone sounds every two bars, each tone twice. The first time it starts sharply on the
left; 50 ms later it has been handed to the right, where all the rest of it sounds, a bar
long; the two together are one unbroken tone. The second time it is the same without its
start. The hangar's air rings with both, and while a tone is held the two sides are about
as loud as each other: the held tone says little of where it is; the start does. So the
first should be heard on the left, where it began, and the second not: though after their
first 50 ms the two are the same.

v30 (27 Nov): THE WALLS CLOSE IN (C11T3_CLOSE=0 takes it out: v29). A knock between two
walls comes back once for every time across and back. Between walls 18.6 m apart that
is nine echoes a second: you can count them. Halve the width and they come twice as
fast: a rattle, a buzz; at the corridor's own 2.33 m they are its note, D2; at arm's
length, D4. Bar by bar the walls close in and come back out to the corridor's own
(its last row). Rhythm and pitch are one thing: the width of the room says which.

v31 (28 Nov): A DROP DOWN THE STAIRWELL (C11T3_DROP=0 takes it out: v30). On the way up
the stairs something is let go over the rail in every bar (a tap), a flight of eight
steps higher each time. It lands when gravity says and its thud comes back up at the
speed of sound: the wait is the square root of twice the height over g, and the height
over 343. The wait says how high you have climbed, and it grows by less each flight.

v32 (28 Nov): THE STAIRWELL RINGS (C11T3_WELL=0 takes it out: v31). Every thud of v31
rings the column of air between the floor and where you stand. A column one flight high
has one note: 126.1 Hz. A column n flights high has that note over n and every multiple
of it: the lowest way falls as you climb (126, 63, 42, 32 ... Hz), the ways crowd
together, and one flight's own note is among them at every height.

v33 (28 Nov): THE ROOM HOLDS ITS BREATH (C11T3_KEPT=0 takes it out: v32). One clap in a
hall in bar 139. Half a beat after it the hall stops dying: its tail hangs as it was for
six and a half beats, as if time had stopped in the room. On the first beat of bar 141,
where the applause begins, it lets go, and dies as a hall does.

v34 (28 Nov): THE KNOCK GOES AWAY, THE ROOM DOES NOT (C11T3_RECEDE=0 takes it out: v33).
In bars 89 to 96 a low knock twice a bar, each time twice as far off (1.3 m to 163 m) and
then back. Each doubling takes 6 dB off the knock itself and makes it later, a whole beat
at the far end; the room's answer to it is the same wherever it is struck. From 2.5 m on
there is more room than knock: that is how an ear tells how far off a sound is.

v35 (28 Nov): SOONER OR LOUDER (C11T3_EARS=0 takes it out: v34). In bars 145 to 152 the same
plain pip in both ears walks from the left to the right twice. In bars 146 to 148 both ears
get it exactly as loud and one gets it sooner, by the way round a head (up to 551 millionths
of a second). In bars 150 to 152 both get it at the same instant and one gets it louder (up
to 9.4 dB). Rayleigh's two ways of telling where a sound is, one at a time.

v36 (28 Nov): THE HIGHER THE NOTE, THE HIGHER IT HANGS (C11T3_RUNG=0 takes it out: v35).
Outside the door (bars 153 to 160) one plain pip a beat, always in the middle, the same in
both ears and nearly as loud, comes down sixteen notes from D7 to D4 and climbs them again. A note is
said to seem to come from higher up the higher its pitch, wherever it really comes from
(Pratt, 1930; Roffler and Butler, 1968). Nothing but the note changes.

v37 (28 Nov): THE PIPE NARROWS: A CLOUD BECOMES A POINT (C11T3_CLOUD=0 takes it out: v36).
In bars 73 to 79 a short hiss a sixteenth after every beat, written as loud in each ear all the way.
At first each ear has a hiss of its own: a cloud. Bar by bar more of it is one hiss given to
both ears, and in the last two bars it is all one hiss: a point. Nothing is panned.

v38 (28 Nov): HOW FAR BY HOW DULL ALONE (C11T3_DULL=0 takes it out: v37). Outside, in bars 9
to 16, the same low knock twice a bar: the first as it is, the second with its top taken
half an octave lower each bar and written as loud.

v39 (28 Nov): SAID INTO THE ROOM AGAIN AND AGAIN, ONLY THE ROOM IS LEFT (C11T3_LUC=0 takes it
out: v38). After Alvin Lucier's "I am sitting in a room" (1969): he recorded himself speaking,
played the recording into the room and recorded that, over and over, until the words were gone
and only the room's own notes were left. Here: three knocks a bar in the corridor (bars 17 to
24), and every bar they have been through the corridor once more.
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


CROWD = os.environ.get("C11T3_CROWD", "1") != "0" and HOUSE                    # v12: the room claps (applause that halves its rate and locks: Neda 2000, Kuramoto)
CROWD_ROWS = (2.0, 4.0, 6.0, 8.0)                      # m: how far away each row of people is; the first two rows are the half house
CROWD_PANS = (-0.9, -0.64, -0.39, -0.13, 0.13, 0.39, 0.64, 0.9)   # where the eight in a row stand
CROWD_SPREAD = 0.10                                    # a person's own rate is up to this share off the beat's when he claps fast, half that when slow
CROWD_PULL = float(os.environ.get("C11T3_CROWD_PULL", "5"))   # the pull toward the beat when the house is full, in radians a beat for a person a quarter turn out
CROWD_GAIN = os.environ.get("C11T3_CROWD_GAIN", "-14dB")   # every person's fader (a row back is quieter by its distance)
SOUND = 343.0                                          # m/s
GOLD = (math.sqrt(5) - 1) / 2


FLUT = os.environ.get("C11T3_FLUT", "1") != "0" and CROWD                      # v13: the corridor's other two walls (a flutter echo)
FLUT_IN = "the corridor"
FLUT_NOTE, FLUT_HZ = "D2", 73.416                      # the note the two side walls make: they are half a wave of it apart
FLUT_WIDE = SOUND / (2 * FLUT_HZ)                      # m (2.336): a click goes across and back in 1 / 73.4 s
FLUT_STILL = 8                                         # bars standing in the middle of the corridor first
FLUT_TURN = 16                                         # bars to walk to the left wall, back through the middle to the right wall, and back
FLUT_REACH = 0.375                                     # how far from the middle the walk goes, as a share of the width: to an eighth of it from each wall
FLUT_RETURNS = 2                                       # the side walls ring when the click goes by, and again each time it comes back down the corridor
FLUT_BACK = 0.63                                       # ... each time at this much of the time before (-4 dB)
FLUT_RING = 0.7                                        # s a ring's note is held (the patch's own decay ends it sooner)
FLUT_GAIN = os.environ.get("C11T3_FLUT_GAIN", "-14dB")                         # at -6 it was 10 dB over the music in the gap after the click and took 0.76 dB off the music under it (measured): 8 dB down
FLUT_RATE = 48000                                      # samples a second: every start is written on a whole sample (half a sample out moved the notches a third of a line at 8 kHz: measured)
TRIM = os.environ.get("C11T3_TRIM", "1") != "0" and FLUT                        # v13: the click's own note turned down (it was 10 dB over the rest of the record)
TRIM_CUTS = tuple(c for c in ((880.0, float(os.environ.get("C11T3_TRIM_1", "-5")), 3), (15000.0, float(os.environ.get("C11T3_TRIM_AIR", "6")), 0.7)) if c[1])   # (Hz, dB, q): A5 down ; the click's top up (it owns the top of the song, which had 12 dB less than the rest of the record at 15 kHz)
TRIM_IN = (4, 16)                                      # bars over which the cut comes in: the first four bars are the click as it always was (Least Common's end is under them)
TRIM_OUT = (152, 160)                                  # ... and goes out again: the last eight bars are the click as it was (Ring True comes in under them)


BALL = os.environ.get("C11T3_BALL", "1") != "0" and TRIM                        # v14: Zeno's ball
NEXTROOM = os.environ.get("C11T3_NEXT", "1") != "0" and os.environ.get("C11T3_FLY", "1") != "0" and os.environ.get("C11T3_BIRD", "1") != "0" and BALL and SQUARE     # v17: the room next door (heard through its wall as you cross the square)
SONIC = os.environ.get("C11T3_SONIC", "1") != "0" and os.environ.get("C11T3_WHISTLE", "1") != "0" and NEXTROOM and PIPES_ON    # v19: faster than sound
FOUR = os.environ.get("C11T3_FOUR", "1") != "0" and SONIC  # v20: the hangar's other two walls (the echoes from its corners)
FOUR_IN = "the hangar"                                 # the section
FOUR_WALK = ((6, 6), (7, 5))                           # the rows of it, by where the click stands (left + right, sixteenths there and back): its last two
FOUR_DEEP = (6, 6)                                     # sixteenths to the wall in front and back, to the wall behind and back: as deep as it is wide, and you half way
FOUR_WALLS = 4                                         # an echo that has met more walls than this is left out (it would be 13 dB under the click's first)
FOUR_FIRST, FOUR_EACH = -4.0, -3.0                     # dB against the click: the first wall an echo meets, each wall after (what the room's two walls take)
FOUR_PAN = 0.85                                        # an echo from straight left or right is this far over (where the side walls' echoes are)
FOUR_VEL = 0.75                                        # the velocity of an echo at 0 dB (the loudest written, two first echoes together, is +2 dB: 0.944)
FOUR_PANS = 9                                          # tracks, evenly from -0.8 to 0.8: an echo is on the nearest
FOUR_GAIN = os.environ.get("C11T3_FOUR_GAIN", "-20dB") # the tracks' fader. Set in the whole song's master, which holds the click and every echo of it near -18 dBFS: at -2, -8 and -14dB the first corner echo came out as loud as the click itself (-17.6 to -18.1); at -20dB what sounds at its instant is 3.4 dB under the side walls' first echo (the echo by itself about 5 under): a wall's worth and a little more
DOME = os.environ.get("C11T3_DOME", "1") != "0" and FOUR   # v21: the hall has a dome, and the dome has a focus (every wall till now was flat)
DOME_IN = ("standing room", 2)                         # the section and the row of it (from 0): the row before the people come in, which had nothing of its own
DOME_PATH = 7                                          # sixteenths from the click up to the dome and down to its focus: THE SAME BY WAY OF EVERY PART OF THE DOME (an ellipse is the curve for which that is so). The click is on step 2: step 9, where nothing else in this room strikes
DOME_UP = 3                                            # sixteenths from the focus up to the dome (and 4 from the click to it)
DOME_PARTS = 12                                        # the parts of the dome an echo is written from: a ring of it, evenly round you (the first DOME_TURN of a part off straight ahead), DOME_RISE degrees up
DOME_TURN = 0.25
DOME_RISE = 45.0
DOME_WALK = (2.0, 5)                                   # sixteenths of sound from the focus at the row's first bar, and the bars it takes to walk there (in a straight line, evenly): the rest of the row you stand on it. Five, not six: in the row's seventh bar Zeno's ball bounces on step 8.98, with the focus; so the focus is heard alone in the sixth and the eighth
DOME_VEL = 0.75                                        # every part's echo, at every bar: nothing gets louder but by arriving together
DOME_PAN = 0.9                                         # the part straight to your left is this far left
DOME_GAIN = os.environ.get("C11T3_DOME_GAIN", "-24dB") # the tracks' fader, set in the whole song's master between two readings. THE FADER SETS THE RATTLE, NOT THE FOCUS: this master holds the focused stroke at the click's own level whatever the fader (-18.5 dBFS in its 40 ms at -20dB, -19.5 at -28dB; the click is -19.7). At -20dB the parts of the rattle stood 1 to 10 dB over what was in their gaps (their highest samples -6 dBFS: nearly the focus); at -28dB they were level with their gaps or under
DUCT = os.environ.get("C11T3_DUCT", "1") != "0" and DOME   # v22: the hall's air duct (what comes back from a pipe is not a click: every note in it takes its own time)
DUCT_IN = ("standing room", 1)                         # the section and the row of it (from 0): the row before the dome, which had nothing of its own but the ball
DUCT_NOTE = "A2"                                       # the duct's own lowest note across (110 Hz: half a wave fits across it: SOUND / (2 * 110) = 1.56 m wide). Nothing under it can travel along the duct but straight down the middle. Chosen with the scorer's bands in view (110 Hz is the band this song is shortest in): the scorer's reading, and a duct that size is a real one
DUCT_MODES = ((1, 0.0), (2, -6.0), (3, -10.0))         # the ways across that are heard: 1, 2, 3 half waves (110, 220, 330 Hz), dB
DUCT_BACK = (1, 1, 1, 3, 3, 3, 5, 5)                   # sixteenths to the duct's far end and back, bar by bar (and the dome in the next row is 7). The echo begins on step 2 + this: 3, 5, 7
DUCT_TOP = 8.0                                         # times its own note that each way across is first heard at (the higher a note, the sooner it is back: all of them above this come at once, as the click)
DUCT_RING = "1600ms"                                   # how long an echo takes to die (60 dB): at 700 ms the long duct's echo was gone before it was within three semitones of its note
DUCT_POINTS = 48                                       # points of the lane a glide is written with (evenly in the logarithm of time)
DUCT_VEL = 0.8
DUCT_PAN = -0.4                                        # the duct's mouth is to your left
DUCT_GAIN = os.environ.get("C11T3_DUCT_GAIN", "-22dB") # set in the whole song's master between two readings, BEFORE their scores were read. At -20dB the echo's lowest tone began 2 to 13 dB over the music in its own band (median 9) and was level with it 300 ms on; at -28dB it began level and was 8 to 10 dB under at 300 ms: the fall would not be followed. THIS MASTER DUCKS THE ECHO WITH EVERY BASS DRUM (10 dB down at 150 and 600 ms after a start on step 3): it is heard between the drums. The scorer likes it louder (-20dB read 99.646, -28dB 99.633): not the reason
RAIL = os.environ.get("C11T3_RAIL", "1") != "0" and DUCT   # v23: the corridor's handrail: one knock is heard twice, because sound has two speeds (Biot, 1808: a knock on 951 m of iron water pipe in Paris came 2.5 s sooner through the iron than through the air in it)
RAIL_IN = ("the corridor", 2)                          # the section and the row of it (from 0): the third of the corridor's four rows, which had nothing the other three have not
RAIL_SPEED = 5100.0                                    # m/s: sound along a steel bar (in air: SOUND, 343)
RAIL_MARKS = (1, 2, 3, 4, 5, 6, 7, 8, 8, 7, 6, 5, 4, 3, 2, 1)   # where on the rail each knock is struck, in thirty-seconds of AIR from you (20.4 m each at this tempo): out to 163 m and back
RAIL_ON = (7, 15)                                      # the sixteenths of the bar on which the AIR's knock lands: three sixteenths after a bass drum (the master has let go by then); the knock itself is struck that much BEFORE. Read in v22's render, the knock's band is at -47 and -57 dBFS on these two
RAIL_NOTE = "D7"                                       # what the rail brings: its ring (the song is on D)
RAIL_PARTS = ((1, 0), (2.756, -6))                     # a free bar's first two ways of ringing (ratio, dB): 2349 and 6474 Hz: nothing over 10 kHz
RAIL_RING = "70ms"
RAIL_LOSS = 0.5                                        # dB a mark that the steel keeps (it does not spread: a rail is one way only)
RAIL_GAIN = os.environ.get("C11T3_RAIL_GAIN", "-22dB") # the rail's ring: read in the whole song's master at -22dB (13 of 16 rise 6 dB or more; all 16 are 6 to 34 dB over the music in their band) and -28dB (9 of 16 rise): the louder of the two, because at the quieter nearly half did not begin. The three that do not rise at -22dB fall on a bass drum or one of the corridor's echoes
RAIL_PAN = -0.8                                        # your left ear is on the rail
AIR_NOTE = "D6"                                        # what the air brings: the knock, an octave duller than the rail's ring. IT WAS FIRST A THUD ON F3 (174.6 Hz) AND THAT DID NOT WORK, READ TWICE IN THE WHOLE SONG: on sixteenths 7 and 15 the bass's note is still sounding and NOT ONE THUD OF 16 ROSE 6 dB; on 1 and 9 (the band is 40 to 55 dB emptier there) 2 of 16 rose, because the bass drum's tail is what comes before them, and the master delivered the same thud 20 dB apart by place where 9 dB were written. THE LOW BAND IS THE DRUM'S AND THE BASS'S IN THIS ROW. Between 1100 and 1250 Hz the row is at -42 to -60 dBFS on every sixteenth
AIR_PARTS = ((1, 0), (2.756, -10))
AIR_RING = "40ms"
AIR_LAW = 0.5                                          # the air's knock falls as 1 over the distance to this power: 3 dB a doubling (a corridor keeps the sound in; open air would be 1: 6 dB)
AIR_GAIN = os.environ.get("C11T3_AIR_GAIN", "-20dB")   # the air's knock: set in the whole song's master between two readings, BEFORE their scores were read: at -18dB 15 of the 16 rose 6 dB or more (8 to 40 dB over the music in their band), at -24dB 12 of 16 (2 to 35 over): the ones that did not begin were the far ones, and the far ones are the story. THE THREE THAT FALL WITH THE TOCK (bars 33 and 40 on 7, bar 36 on 15) ARE DELIVERED 13 TO 15 dB UNDER THE SAME KNOCK ELSEWHERE
GAL = os.environ.get("C11T3_GAL", "1") != "0" and RAIL    # v24: the hall has a whispering gallery: a whisper at a round wall does not cross the room, it goes ROUND it, both ways, and round again (St Paul's; the Gol Gumbaz at Bijapur, 38 m across, where a whisper is said to come back seven times. Rayleigh 1878, Raman 1921)
GAL_IN = ("standing room", 0)                          # the section and the row of it (from 0): the first row of the hall, which had only the standing wave
GAL_LAP = 3                                            # sixteenths once round: 122.5 m of wall at 343 m/s: a gallery 39 m across (the Gol Gumbaz is 38)
GAL_AT = 1 / 3                                         # where you stand: this much of the way round from the one who whispers, by the short way: the whisper comes from the LEFT after a third of a lap and from the RIGHT after two thirds, and again every lap: left, right, nothing; left, right, nothing: three against the bar's four, by geometry
GAL_TIMES = 7                                          # times round, each way
GAL_EVERY = 2                                          # bars between whispers
GAL_ON = 0.5                                           # the sixteenth of the bar somebody whispers on: HALF A SIXTEENTH AFTER THE BAR LINE, so that every arrival falls BETWEEN the song's sixteenths. Read in the whole song's master with the whisper ON the bar line (two readings, -16 and -24dB): the arrivals that fell with the click, its echoes, the tock or the drum came out 10 to 18 dB under what was written (the second arrival 21.7 dB under the first for 3.5) and the ones on empty sixteenths came out as written, 30 to 39 dB over everything in their band: the gallery's pattern was not delivered. The whisper itself is not heard: straight across the room (34 m, as 1 over the distance) it is too faint: that is the gallery's whole trick
GAL_LAW = 0.5                                          # the wall's wave spreads along the wall only: it falls as 1 over the distance to this power (3 dB a doubling, as the pipes' and the rail's do), where sound in the open falls 6
GAL_LOSS = 1.5                                         # dB the wall takes a lap
GAL_NOTE = "B4"                                        # the note the noise's register is clocked from (45.9 thousand steps a second): EVERY ARRIVAL IS THE SAME BURST, sample for sample: it is one whisper, coming round
GAL_BAND = (3000, 7500)                                # Hz: a whisper is all hiss, and the wall carries the short waves best. Nothing over 10 kHz (asked for by chirper-one)
GAL_LEN = 0.06                                         # beats a whisper lasts (29 ms), and 20 ms to die
GAL_VEL = 0.9
GAL_PAN = 0.8                                          # each way round, out to its side
GAL_GAIN = os.environ.get("C11T3_GAL_GAIN", "-25dB")   # set in the whole song's master between two readings, BEFORE their scores were read: at -22dB 40 of the 56 arrivals stand 6 dB or more over everything else in their band and ear in their own 50 ms (the first -20.3 dBFS there, 39 dB over), at -28dB 31 (the first -26.3). THE MASTER STILL DOES NOT DELIVER THE FALL AS WRITTEN: against the first, the arrivals after a bass drum come 6 to 7 dB under what is written and the rest 1 to 6 under: the first arrival falls in the emptiest place in the bar
BEND = os.environ.get("C11T3_BEND", "1") != "0" and GAL   # v25: the bass is heard ROUND THE CORNER before it is met: sound bends into a shadow, the low notes most (Maekawa, 1968: the shadow takes 10 log (3 + 20 N) dB, where N is how many half waves longer the way round is than the way through)
BEND_BARS = (16, 32)                                   # bars from 0: the corridor's first two rows, before the bass comes in (bar 33 is the corner: you turn it and the bass is in front of you)
BEND_SIDE = 3.0                                        # m: how far round the corner the bass is
BEND_FROM = 24.0                                       # m: how far from the corner you are when the corridor begins (0.8 m/s: a slow walk)
BEND_LAW = 0.5                                         # the corridor's own law (the handrail's, the pipes'): the level falls as 1 over the way to this power
BEND_PARTS = (0.0, -14.2, -15.1, -17.6, -27.4, -24.3)  # dB: the bass's own first six partials against its first, read alone (b/bass.yaml): each is shadowed by its own amount
BEND_TRIM = -5.5                                       # dB: a plain tone at the bass's fader reads this much over the bass's first partial (read alone)
BEND_LIFT = -2.0                                       # dB: taken off for what this song's master adds to a quiet part in these two rows. Read in the whole song's master without it: the six tones came 0.5 to 1.7 dB over what is written against the bass as it is met, 2.4 over in the last bar and 3.4 on the last two notes (the bass itself is held down by the master where it plays with the drum; these rows are 3 dB quieter and are not)
BEND_GAIN = os.environ.get("C11T3_BEND_GAIN", "")      # the first partial's fader; nothing: the bass's own fader, BEND_TRIM and BEND_LIFT, so that with no shadow these six tones are the bass AT THE EAR
SLAM = os.environ.get("C11T3_SLAM", "1") != "0" and BEND   # v26: the hangar's door shuts behind you, and the tail says how big the place is and what its air does: in a very big room the walls set how long the low sound lasts and THE AIR sets how long the high sound lasts (Sabine's rule with the air's own term, 4mV): the tail goes dark as it dies
SLAM_IN = "the hangar"                                 # the section on whose first beat the door shuts (the drum and the bass rest for its first row)
SLAM_HALL = (245.0, 245.0, 20.0)                       # metres: as wide and as deep as the hangar's echoes already say, and 20 m high
SLAM_WALLS = 0.15                                      # what walls, floor and roof take of the sound at every meeting, the same at every pitch
SLAM_EDGES = (95.0, 177.0, 354.0, 707.0, 1414.0, 2828.0, 5657.0, 7500.0)   # Hz: the tail's seven bands (octaves, but the bottom starts at 95 Hz, over the drum's and the bass's own notes, and the top stops at 7500)
SLAM_AIR = (0.44, 1.31, 2.73, 4.66, 9.86, 29.4, 70.0)  # dB a kilometre: what the air takes at each band's middle (ISO 9613-1: 20 degrees, half humid; the last read off between its 4 and 8 kHz)
SLAM_TILT = -3.0                                       # dB an octave from band to band: the door's own sound, heavy at the bottom
SLAM_AWAY = 10.0                                       # metres from you to the door: sets how far the slam itself stands over the tail it starts
SLAM_DIRECT = 0.06                                     # seconds of the slam itself, in the middle; then the tail, wide
SLAM_TURN = 0.02                                       # seconds from the one to the other
SLAM_FLOOR = -90.0                                     # dB: "gone"
SLAM_EDGE = (0.5098, 0.6013, 0.9, 2.5629)              # the q of the four filters at each edge of a band: together a wall of 48 dB an octave, 3 dB down at the edge (Butterworth's eighth order): two bands side by side then add up level, and a slow band does not leak far into a quick one
SLAM_TRIM = (2.4, 0.0, 0.0, 0.0, 0.0, 0.0, 1.1)        # dB on each band's fader, measured alone: the bottom band and the narrow top band came out that much under the door's own slope against the five between
SLAM_PAN = float(os.environ.get("C11T3_SLAM_PAN", "2.3"))   # dB: what the engine's pan gives a sound in the middle over the same sound SLAM_WIDE out, both ears counted (measured alone): taken off the slam, so that it stands over the tail by what is written and no more
SLAM_WIDE = 0.8                                        # the tail's two noises (a band has one for each ear) go this far apart
SLAM_GAIN = os.environ.get("C11T3_SLAM_GAIN", "-6dB")      # the bottom band's fader before its trim; read in the whole song's master at -16, -10 (an earlier build), -12 and -6 dB and set BEFORE the last two's scores were read: at -6 the slam's first 50 ms are -10.2 dBFS (a stroke of the drum is -7 to -8) and the tail's first second -20.1 dBFS, 3 dB under the music that is there (the chord and its echo); at -12 the tail's first second is 9 dB under it and only the slam would be heard
HUSH = os.environ.get("C11T3_HUSH", "1") != "0" and SLAM   # v27: THE HUSH AFTER THE DOOR: when the hangar's door has shut, the click, the tock, the chord and the bird wait: for HUSH_BARS bars there is the door's tail and nothing else. You stand still and hear how big the place is: v26 wrote the tail and measured it, but the chord lay over it
HUSH_BARS = 2                                          # bars of it: 3.81 s: by then the tail's top band has gone and its bottom has fallen 25 dB
HUSH_KEEP = ("slam-",)                                 # the tracks (by the start of their names) that do not wait: the tail itself. The bird was tried staying (read in the whole song's master): from the tail's second second it held the two top bands (2.8 to 7.5 kHz) at -34 to -44 dBFS, where they read -41 to -52 without it: the bird waits too, and flies three times round, not four
FOOT = os.environ.get("C11T3_FOOT", "1") != "0" and HUSH   # v28: THE FOOT OF THE STAIRS: when you come into the stairwell the drum and the bass wait FOOT_BARS bars: you stand at the foot of the stairs and hear the place before you climb: the click and the tock and what the stairwell gives back of them, and nothing else. (Zeno's ball comes to rest on that very bar line.) At the end of them you clap for the first time and the drum comes back with the clap
FOOT_IN = "the stairwell"                              # the section on whose first beat they stop
FOOT_BARS = 4                                          # bars they wait: until the bar of the first clap on the stairs
FOOT_WAIT = ("kick", "bass")                           # the tracks that wait
BEGAN = os.environ.get("C11T3_BEGAN", "1") != "0" and FOOT   # v29: WHERE IT BEGAN (the Franssen effect: Franssen 1960; Hartmann and Rakerd 1989): in a room that rings, a plain tone is heard where it BEGAN. Every tone is played twice. The first time it starts sharply on the left; BEGAN_HOLD and BEGAN_HAND later it has been handed to the right, where all the rest of its straight sound is; the two together are one unbroken tone. The second time it is the same without its start: only what came from the right. While either is held the hangar answers (its air), and the two sides are about as loud as each other: a steady plain tone in a ringing room says little of where it is. The start does: so the first should stay on the left, where it began, and the second not
BEGAN_IN = ("the hangar", 2, 2)                        # the section, the row (from 0) of the first tone, and how many rows: bars 97 to 112, the hangar's last two rows
BEGAN_EVERY = 2                                        # bars from tone to tone: a bar of tone, a bar of the hangar ringing on
BEGAN_AT = 0.25                                        # the beat of the bar it starts on: a sixteenth after the drum, the one sixteenth of the bar with nothing at 300 to 480 Hz (the old music's tops there: -37 dBFS, 12 to 23 dB under every other sixteenth)
BEGAN_LEN = 4.0                                        # beats the tone is held
BEGAN_HOLD = 0.010                                     # s: the start is whole, and all on its own side, for this long: the first wave is what the ear takes the place from
BEGAN_HAND = 0.040                                     # s: the start's side falls to nothing, and the other side rises to the whole tone, in this time, in straight lines: the two add up to the whole tone throughout
BEGAN_FADE = 0.400                                     # s: the tone goes out slowly: an end tells no place
BEGAN_TUNE = ("A4", "C5", "F4", "E4")                  # the tones, each twice (with its start, then without): plain sines (the trick wants a plain tone), of the hangar's chord, 330 to 523 Hz (over the 300 Hz at which the hangar's air begins; the song is short at 342 and 400 Hz)
BEGAN_PAN = 1.0                                        # how far to each side: all the way: the start on the left, the rest on the right (on one speaker the two are one plain tone). WHY NOT LEFT AND RIGHT BY TURNS: the first build did that, and read in the whole song's master this hall answered every one of these tones 7 to 13 dB more on the LEFT, whichever side it was fed from: a tone that went on from the right was level (1 to 4 dB to the right), one that went on from the left stood 8 to 13 dB to the left, and A4 from the left was cancelled by its own air (11 dB under the others)
BEGAN_GAIN = os.environ.get("C11T3_BEGAN_GAIN", "-38dB")   # both tracks: meant: the straight sound -28 dBFS in the master (the old music at these notes is -41 to -46 dBFS in the middle, a sixth of an octave round each; its tops on the start's sixteenth -37)
BEGAN_AIR = os.environ.get("C11T3_BEGAN_AIR", "12dB")      # what of them goes to the hangar's air: so that the air is about as loud as the straight sound while the tone is held: where you would stand 27 m from each (in a room of 1200500 cubic metres that rings 5.5 s the room is as loud as the straight sound at 0.057 * sqrt(V / T) = 26.6 m). Read in the whole song's master at -6dB and +6dB (the first build: sides by turns, pan 0.8, no hold; seed 0) and at +12dB (sides by turns, pan 1, with the hold), BEFORE any score: the air on its louder side came out about 19, 7 and 1 dB under the straight sound. THIS BUILD at +12dB (seed 0; the song less the same with nothing to the air): the straight sound -28.6 dBFS on the right, the air on the left -0.8 dB against it (-1.8 to +0.9), on the right 11.5 dB under in the middle (F4's is as loud on the right)
CLOSE = os.environ.get("C11T3_CLOSE", "1") != "0" and BEGAN   # v30: THE WALLS CLOSE IN: a knock between two walls comes back again and again, once for every time across and back. Far walls: echoes you can count. Halve the width and they come twice as fast; halve it again and again and they are a rattle, a buzz, and then a NOTE: the room's own, an octave up for every halving. The corridor's 2.33 m is D2; arm's length is D4. Rhythm and pitch are one thing, and the width of the room says which
CLOSE_IN = ("the corridor", 3)                         # the section and its row (from 0): bars 41 to 48, the corridor's last row: the walk ends between its walls
CLOSE_RATE = 48000                                     # samples a second: every echo is written a whole number of samples after the one before
CLOSE_NEAR = 163                                       # samples across and back between the nearest walls: 0.582 m apart: 294.5 Hz (D4, 5 cents high)
CLOSE_STEPS = (5, 4, 3, 2, 1, 0, 1, 2)                 # bar by bar, how many times the nearest width is doubled: 18.6 m, 9.3, 4.7, 2.33 (the corridor itself: its flutter is D2), 1.16, 0.58, and out again to the corridor's own
CLOSE_AT = (0.125, 2.125)                              # the beats of each bar a knock is on: an eighth of a beat (60 ms) after the first and third strokes of the drum: the only two beats of the bar, two beats apart, that are 26 ms or more from every stroke of every part in all eight bars (searched on v29's notes). The first build's knocks (beats 0.25, 2.25) fell with the click's echo on sixteenth 9 and came out 7.6 dB under; the second's (0.25, 3.25) fell twice with the tock, which comes round every 14 sixteenths (14 and 13 dB under), and twice more came out 6 and 7 dB under. A train that would not be over when the row ends is left out (bar 49 is the foot of the stairs): with these beats, none
CLOSE_FALL = 75.0                                      # dB a second every train falls, whatever the width: the walls are the same walls
CLOSE_END = 36.0                                       # dB fallen at which a train is let go (0.48 s)
CLOSE_SHARE = 3.0                                      # dB taken from every echo for each halving of the width: twice the echoes a second, half the energy each: every train carries the same energy (a rule of this piece, not of a room: in a room nearer walls are louder)
CLOSE_NOTE = "D3"                                      # what an echo is: one soft thud, about two waves of D3 with its octave as loud (with D3 alone the nearest walls' train, 294 to the second, was 10 dB under the others on the bench: a train only keeps what is in step with it)
CLOSE_LEN = 0.05                                       # beats an echo is written (24 ms; its own fall ends it in 12)
CLOSE_GAIN = os.environ.get("C11T3_CLOSE_GAIN", "-16dB")   # the track. Set from readings in the whole song's master, before any score was opened: with the knocks on beats 0.125 and 2.125 at -22dB (both seeds) a train's first 450 ms was -35.4 to -37.9 dBFS (2.5 dB between the quietest and the loudest of the 16) and stood 17.5 dB under the old music at 100 to 600 Hz in the middle: too far under: 6 dB up. An eighth of a beat after the drum THE MASTER LIFTS A KNOCK 13.1 dB (bench at the same fader -45.3). The first build (D3 alone; knocks on beats 0.25 and 2.25), read in the whole song's master at -20dB and -26dB (seed 0) BEFORE any score: a train's first 100 ms -27.9 dBFS for -47.3 on the bench at the same fader: THE MASTER LIFTS A KNOCK ON SIXTEENTH 1 19.4 dB; the trains on sixteenth 1 stood 11 to 19 dB under the old music at 100 to 600 Hz
DROP = os.environ.get("C11T3_DROP", "1") != "0" and CLOSE   # v31: A DROP DOWN THE STAIRWELL: on the way up the stairs something is let go over the rail in every bar, a flight higher each time. It lands when gravity says (the square root of twice the height over g) and its thud comes back up at the speed of sound: the wait says how high you have climbed, and it grows as the square root, by less each flight
DROP_IN = ("the stairwell", 1)                         # the section and its row (from 0): bars 57 to 64, the first whole row of the stairs
DROP_STEPS = 8                                         # steps in a flight
DROP_RISER = 0.17                                      # metres a step: a flight is 1.36 m
DROP_G = 9.81                                          # metres a second a second
DROP_AT = 0.65625                                      # the beat of the bar it is let go on (a tap): found by a search of v30's notes over flights of 6 to 18 steps and every thirty-second of a beat: the tap and all eight landings are 40 ms or more from every stroke of the drum, the bass, the click, the tock and the clap, and 81 ms or more after a drum
DROP_NOTES = ("Bb2", ((2.0, -3.0),))                   # the thud: the floor at the bottom rings two low tones, Bb2 and its octave 3 dB under (116.5, 233.1 Hz): always the same floor. NOT A2, F3 AND C4, which the first build had: they are harmonics of the bass's own notes (A1, F2, C2), and in their own bands three landings of eight were 11 to 13 dB under the old music. Bb is the one note of the scale no harmonic of the bass in this row comes near
DROP_TAP = ("C5", -4.0)                                # the tap of letting go: its note, and dB under the thud's track
DROP_GAIN = os.environ.get("C11T3_DROP_GAIN", "-26dB")   # the thud's track. THE BENCH FIRST (the two tracks alone, the thud's at -20 dB): the first thud's first 100 ms -35.6 dBFS (15.6 under its fader). The first build (three tones, -30 dB) read the first thud at -28.0 dBFS in the whole song's master (a lift of 17.3 dB): aimed at -24 with that lift; read at -26dB (both seeds) BEFORE any score: the first thud -24.4 dBFS, the others 2.8 to 6.5 dB under it (the master evens them: 9.0 written); the nth landing is 10 log n dB under the first (the blow as the height, the way back as one over the height: a rule of this piece)
WELL = os.environ.get("C11T3_WELL", "1") != "0" and DROP   # v32: THE STAIRWELL RINGS: every thud of v31 rings the column of air between the floor and where you stand. A column one flight high has one note (the speed of sound over twice its height); a column n flights high has that note over n, and every multiple of it: the lowest way falls as you climb and the ways crowd together, and the one flight's own note is among them at every height
WELL_BAND = (100.0, 260.0)                             # Hz: the ways written (the lower ones are under the drum and the higher ones the floor does not give)
WELL_NOTE = ("B2", 123.47082531403103)                 # the note written and its frequency; the patches move it to one flight's own note
WELL_RING = 1.8                                        # seconds a ring takes to die
WELL_GAIN = os.environ.get("C11T3_WELL_GAIN", "-30dB")   # every ring's track. THE BENCH FIRST (the eight tracks alone at -20 dB): a ring's first 100 ms -31.6 to -33.3 dBFS (12 under its fader: it is dying from the start), then -35, -43, -56; all 48 ways have a peak within 1.5 Hz of the written and there is no other peak. Aimed at -25 dBFS for the first 100 ms with the thud's lift (17.2 dB); that bench was of the first build (a ring of 0.9 s: over the old music in its band in 2 landings of 8); with 1.8 s the bench reads -30.8 to -32.6 then -33, -37, -42, and the song (both seeds, read BEFORE any score) -20.3 to -27.3 dBFS in the first 100 ms (this master lifts it 18.8 / 19.1 dB): over the old music in 4 landings of 8; a ring of m ways has each 10 log m dB under it (the same sound in all, however many)
KEPT = os.environ.get("C11T3_KEPT", "1") != "0" and WELL   # v33: THE ROOM HOLDS ITS BREATH: one clap in a hall; half a beat after it the hall stops dying: its tail hangs where it was, neither louder nor softer, for six and a half beats: a room in which time has stopped. Then it lets go, on the bar the applause begins, and dies as a hall does
KEPT_IN = ("standing room", 3)                         # the section and its row (from 0): bars 137 to 144: the people are coming in; the applause begins in bar 141
KEPT_CLAP = (2, 1.0)                                   # the bar of the row (from 0) and the beat of the clap: bar 139, beat 1: with the song's own clap
KEPT_FROM = 0.5                                        # beats after the clap at which the hall stops dying
KEPT_TO = (4, 0.0)                                     # the bar of the row and the beat at which it lets go: bar 141, where the applause begins
KEPT_HALL = {"kind": "hall", "decay": "1.2s", "mix": 0.6, "low_cut": 120, "high_cut": 5000}   # the engine's hall on this one track: 1.2 s to die when it is let
KEPT_GAIN = os.environ.get("C11T3_KEPT_GAIN", "-7dB")   # the track. THE FIRST BUILD (-15 dB) WAS UNDER THE MUSIC: read between the strokes in the whole song (the new less the old), the held tail was -31.9 dBFS against the old music's -20.3 in its own band (120 to 5000 Hz), and over it in 3 of 13 windows; in 700 to 2000 Hz, where the tail is strongest, 8.7 dB under. So 8 dB more: the tail -24.3 / -23.8 dBFS (seeds 0 / 11) against -20.3 / -20.7, over it in 3 of 13 still; in 700 to 2000 Hz -25.0 / -24.6 against -23.9 / -24.3, over it in 5 / 6 of 13: level with the music where it is strongest, under it elsewhere. THE BENCH (alone at -20 dB): the held tail -51.4 to -53.4 dBFS by half beat, 2.0 dB down over the 6.5 beats; let go, 60 dB in 1.07 s
RECEDE = os.environ.get("C11T3_RECEDE", "1") != "0" and KEPT   # v34: THE KNOCK GOES AWAY, THE ROOM DOES NOT (how far off a sound is, told by the room): a knock twice a bar, each time twice as far off, and then back. Each doubling takes 6 dB off the knock itself and makes it later (343 m/s); the room's answer to it is as loud wherever in the room it is struck. So near, the knock is over the room; at one distance (the critical distance) they are equal; beyond it there is more room than knock, and at the far end the room is nearly all there is
RECEDE_IN = ("the hangar", 1)                          # the section and its row (from 0): bars 89 to 96. Read on v33: 160 to 200 Hz is -40 to -58 dBFS between the strokes here (twelfths 1 to 10 of the beat)
RECEDE_AT = (1 / 3, 2 + 1 / 3)                         # the beats of the bar at which it is struck: a third of a beat after beats 0 and 2
RECEDE_NOTE = ("F3", 174.614)                          # the knock: a low thud, a sine and its octave, 90 ms
RECEDE_FAR = SOUND * 60 / BPM                          # metres at the far end: a beat of air (163.3 m): the knock is heard a beat after it is struck
RECEDE_STEPS = 8                                       # distances, each half the next: 1.28, 2.55, 5.1, 10.2, 20.4, 40.8, 81.7, 163.3 m: out in bars 89 to 92, back in bars 93 to 96
RECEDE_CRIT = 1                                        # the step (from 0) at which the knock and the room's whole answer to it carry the same energy (the mean of the two ears): 2.55 m: the critical distance of this room, a church's (my choice: by Sabine's rule the hangar's own would be 21 m, and the room's answer would be under everything)
RECEDE_ROOM = {"kind": "hall", "decay": "1.6s", "mix": 1.0, "low_cut": 120, "high_cut": 3000}   # the room's answer: the engine's hall, all of it (no knock in it), on a track of its own
RECEDE_TRIM = (-4.4, -2.7, -4.6, -2.5, -4.5, -2.0, -4.5, -2.0, -4.5, -2.0, -4.5, -2.0, -4.7, -1.0, -4.3, 0.0)   # dB on each knock in turn (by its velocity). THE FIRST BUILD HAD NONE, and in the finished song the steps were not 6 dB: out -7.8 -4.0 -7.9 -4.2, back -1.8 -9.3 -2.6 -4.7: the master lifts a knock after beat 0 by 21.2 to 21.6 dB and one after beat 2 by 16.9 to 19.6 (bar by bar). These are what the first build read, turned over; for the eight far knocks (under the room: they cannot be read) the place's middle
RECEDE_GAIN = os.environ.get("C11T3_RECEDE_GAIN", "-23.9dB")   # the knock's track. THE BENCH FIRST (one knock alone at -20 dB, velocity 1): highest sample -25.5 dBFS. The first build (-25.5 dB, no trims): the nearest knock -9.7 dBFS going and -14.1 coming back; with the trims and 1.6 dB more both are aimed at -12.5. THE SECOND BUILD READ (both seeds, before any score): -12.5 and -12.5 / -12.2 and -12.4 dBFS; the steps -6.0 -5.9 -5.1 going and -6.1 -6.0 -4.2 coming back; the room after the knock -43.4 to -35.1 dBFS, level with the old music in 160 to 200 Hz and 18 dB under it in 120 to 450
RECEDE_ROOM_GAIN = os.environ.get("C11T3_RECEDE_ROOM_GAIN", "-35.9dB")   # the room's track. THE BENCH (one knock's whole answer alone at the knock's fader): its energy is 4.4 dB over the knock's (the two ears 5.6 and 2.6 dB over: the engine's hall answers more on the left); so 6.0 dB (step RECEDE_CRIT) and 4.4 dB under the knock's fader makes them equal at 2.55 m
EARS = os.environ.get("C11T3_EARS", "1") != "0" and RECEDE   # v35: SOONER OR LOUDER (Rayleigh's two ways of telling where a sound is): the same plain pip in both ears walks from the left to the right twice. The first time both ears get it exactly as loud, and one gets it sooner, by as much as the way round a head takes (Woodworth: the head's radius over the speed of sound, times the angle plus its sine). The second time both get it at the same instant, and one gets it louder. A low tone is placed by the first; the second is what a pan knob does
EARS_IN = ("standing room", 4)                         # the section and its row (from 0): bars 145 to 152. Read on v34 by twelfths of the beat: after beats 0 and 2, 400 to 480 Hz is -53 -61 -60 -64 -54 dBFS in twelfths 1 to 5 (after beats 1 and 3 it is not: -39 -37 -35 in twelfths 3 to 5)
EARS_AT = (1 / 3, 2 + 1 / 3)                           # the beats of the bar a pip begins on (its middle; each ear half the difference to either side)
EARS_NOTE = "A4"                                       # the pip: 440 Hz: a whole wave is 2273 millionths of a second, so the widest difference here (551) is under a quarter of a wave: the ear can tell which wave came first
EARS_MS = 80                                           # ms a pip lasts
EARS_EDGE = 8                                          # ms it takes to come and to go
EARS_ANGLES = (-70, -42, -14, 14, 42, 70)              # degrees from straight ahead (minus: to the left), a pip each. THE FIRST BUILD HAD EIGHT (-70 to 70 by 20), from the first bar of each four: its second pip (beat 2.333 of bars 145 and 149) fell where the old music is -23 and -24 dBFS in 300 to 640 Hz, 4 to 7 dB OVER the pip; from the second bar of each four the old music at the pips is -42 to -55
EARS_WALKS = ("time", "level")                         # the walks, 4 bars each: by which ear gets it sooner; by which gets it louder. A walk's pips are in the LAST bars of its four (three bars here: the first is left to the room)
EARS_HEAD = 0.0875                                     # m: the radius of a head
EARS_LEVEL = 10.0                                      # dB between the ears for a sound straight to one side, in the walk by level; the sine of the angle of it elsewhere. MY CHOICE: a real head shadows a tone as low as this by less
EARS_GAIN = os.environ.get("C11T3_EARS_GAIN", "-32.5dB")   # both tracks. THE BENCH FIRST (the two tracks alone at -20 dB): a pip of the walk by time -34.0 dBFS in each ear (its middle 60 ms); set for -27 in the song with the 19.5 dB the master gave the knock a third of a beat after the drum in bars 89 to 96. THE SECOND BUILD READ (each ear by itself, both seeds, before any score): by time the left ear later by -541 -357 -125 +125 +375 +563 millionths of a second (starts are rounded to the sample) and the ears 0.0 dB apart, -27.3 to -24.1 dBFS; by level 0 millionths and -9.4 -6.7 -2.4 +2.4 +6.7 +9.4 dB; the quieter ear over the old music by 10.5 dB at the least
RUNG = os.environ.get("C11T3_RUNG", "1") != "0" and EARS   # v36: THE HIGHER THE NOTE, THE HIGHER IT HANGS (Pratt, 1930; Roffler and Butler, 1968): a note is said to seem to come from higher up the higher its pitch, wherever it really comes from. Outside the door there is no room and no ceiling: one plain pip a beat, always in the middle, the same in both ears and nearly as loud (within 2 dB), comes down a ladder of 16 notes and climbs it again. Nothing but its note changes. v35 placed a pip left and right by time and by level; this is up and down, and it is not in the sound at all
RUNG_IN = ("the door", 0)                              # the section and its row (from 0): bars 153 to 160. Read on v35 by sixteenth of the beat: 500, 1000 and 2000 Hz are -56, -67 and -79 dBFS a sixteenth after the beat in this row (the emptiest place). THE FIRST BUILD (up then down, every pip a sixteenth after its beat) put the ladder's top on the thing that goes past (closest in bar 157) and the old music under the second pip was -25.6 dBFS: that pip was 2.5 dB UNDER the old music in its band, and six more less than 10 dB over it. b/oldat.py then read the old music at every instant the ladder could use, in the band of the note it would play there, both ways round: DOWN THEN UP, with the pips of beats 1 and 3 three sixteenths after the beat, has nothing louder than -38.5 dBFS under any pip
RUNG_AT = (0.25, 0.75, 0.25, 0.75)                     # how far after each beat of the bar its pip begins: a sixteenth after beats 0 and 2, three after beats 1 and 3 (read: see RUNG_IN)
RUNG_FROM = 62                                         # the lowest rung (MIDI): D4, 293.7 Hz
RUNG_STEPS = (0, 3, 5, 7, 10)                          # semitones over the rung an octave below: D F G A C, the song's own five
RUNG_N = 16                                            # rungs: D4 to D7 (2349.3 Hz), three octaves: down them first, then up
RUNG_MS = 90                                           # ms a pip lasts
RUNG_EDGE = 8                                          # ms it takes to come and to go
RUNG_TRIM = (-1.2,) * 16 + (0.0,) + (-1.2,) * 15       # dB off each pip in turn (by velocity). In the first build every pip a sixteenth after its beat read -28.1 dBFS but the first of bar 157, which read -29.3 (the thing going past is closest there and the master gives way): that one is left whole and the others taken down to it
RUNG_GAIN = os.environ.get("C11T3_RUNG_GAIN", "-40.7dB")   # THE BENCH FIRST (the track alone at -20 dB): every pip -26.0 dBFS, the same in both ears; the first build set for -30 in the song with 20 dB of lift (a pip a third after the beat in bars 146 to 152 got 19.2 to 22.4): -44 dB: it got 21.9 and read -28.1. The second build is set for -26: -40.7 dB with the trims
CLOUD = os.environ.get("C11T3_CLOUD", "1") != "0" and RUNG   # v37: THE PIPE NARROWS: A CLOUD BECOMES A POINT. A short hiss a sixteenth after every beat of the pipes. Each ear gets a hiss as loud as before, bar after bar; the only thing that changes is how alike the two ears' hisses are. Two different hisses, one to an ear, are a cloud that fills the head; the same hiss in both is a point in the middle (the same signal in both ears is one source). In between, part of each: the cloud draws in. Nothing is panned and nothing is turned up or down
CLOUD_IN = ("the pipes", 0)                            # the section and its row (from 0): bars 73 to 80
CLOUD_BARS = 7                                         # bars it lasts: bars 73 to 79 (bar 80 is left empty before the door shuts on bar 81)
CLOUD_AT = (0.25, 1.25, 2.25, 3.25)                    # beats of the bar a hiss begins on: a sixteenth after the beat. Read on v36 FIRST (b/rowband2.py: 2000 to 7000 Hz under a stroke of a quarter of a beat, row by row and sixteenth by sixteenth): of the rows outside the first and the last section the pipes have the least under a stroke a sixteenth after the beat (the middle of its 32 beats -46.4 dBFS, the next row's -43.9; the loudest of the 32 -29.1)
CLOUD_LIKE = (0, 0, 0.25, 0.5, 0.75, 1, 1)             # how alike the two ears' hisses are, bar by bar: the share of each ear's power that is the hiss both ears have
CLOUD_LEN = 0.25                                       # beats a hiss lasts (119 ms)
CLOUD_BAND = (3000, 7000)                              # Hz: v36's bands from 4213 to 7895 Hz read 0.1 to 3.8 dB under the album; the hiss's power over 10 kHz is 37.4 dB under all of it
CLOUD_EDGE = (3, 12)                                   # ms it takes to come and to go
CLOUD_TRIM = (0.0, 0.0, 0.0, 0.0)                      # dB on a hiss, by beat of the bar: none
CLOUD_GAIN = os.environ.get("C11T3_CLOUD_GAIN", "-26.3dB")   # the three tracks. THE BENCH FIRST (the three alone at -20 dB): an ear's level -44.4 to -43.3 dBFS (the middle -43.7: every hiss is a new one); the one build set for -30 in the song with 20 dB of lift: it came out -28.1 / -28.4 (seeds 0 / 11: a lift of 21.9 / 21.6) and was left
DULL = os.environ.get("C11T3_DULL", "1") != "0" and CLOUD   # v38: HOW FAR BY HOW DULL ALONE: outside, where no room answers, the same low knock twice a bar: the first as it is, the second with its top taken as air takes it, half an octave more each bar, and written as loud. If air's loss in dB goes as the square of the frequency (the classical law), half an octave duller is twice as far
DULL_IN = ("outside", 1)                               # the section and its row (from 0): bars 9 to 16
DULL_AT = (1.25, 3.25)                                 # beats of every bar: the knock as it is, then the dulled one; a sixteenth after the drum
DULL_LEN = 0.25                                        # beats a knock is held
DULL_NOTE = "Bb2"                                      # 116.5 Hz: a saw, so it has a top to lose
DULL_TOP = 8000                                        # Hz: the low-pass of the knock as it is
DULL_STEP = 0.5                                        # octaves the low-pass comes down each bar: twice as far by the classical law
DULL_EDGE = (1, 90, 20)                                # ms a knock takes to come, to die and to go
DULL_TRIM = (0.0,) * 16                                # dB on a knock, knock by knock: none
DULL_GAIN = os.environ.get("C11T3_DULL_GAIN", "-25.9dB")   # the eight tracks. THE BENCH FIRST (the eight alone at -20 dB): a knock -40.3 to -40.0 dBFS over its first 110 ms, the second of a bar -0.18 to +0.05 dB against the first with no trims, and 3 dB under it where the low-pass is written (bars 11 to 16: within 2 in a hundred); the first build set for -27 in the song with 19 dB of lift
LUC = os.environ.get("C11T3_LUC", "1") != "0" and DULL   # v39: SAID INTO THE ROOM AGAIN AND AGAIN, ONLY THE ROOM IS LEFT (after Alvin Lucier, "I am sitting in a room", 1969). Three knocks a bar in the corridor; every bar they have been through the corridor once more. What a room gives back it gives back best on its own notes, so each time round the knocks are less and the room's notes more
LUC_IN = ("the corridor", 0)                         # the section and its row (from 0): bars 17 to 24. READ FIRST (v38, seed 0): 250 to 650 Hz reads -38.8 dBFS in the middle window of 100 ms there
LUC_AT = (0.25, 0.75, 1.25)                          # beats of every bar a knock is on
LUC_NOTE = "D2"                                      # the corridor's own note (STAND_ROOT)
LUC_KNOCK = 30                                       # ms the knock (a saw) takes to die
LUC_WAYS = (2, 3, 4, 6, 8)                           # the ways across the corridor that ring (times STAND_ROOT): the five of the standing wave
LUC_UP = 6.0                                         # dB a pass lifts each way (an eq peak); the same 6 dB is taken off the whole after every pass
LUC_TAU = 0.080                                      # s a way's ring takes to fall to 1/e after one pass, the same for every way
LUC_Q = 1.0                                          # 1: the textbook peak. THE ENGINE FIRST (b/again1.yaml, the rate read from 60 to 160 ms after the last knock): one pass died at 119 dB a second where 108.6 is written; with 1.3 here it died at 99. (My first reading, over 300 ms, gave 141: it had run into the floor of a 16-bit file)
LUC_TRIM = (0.0, 5.6, 10.7, 16.0, 21.6, 21.2, 21.4, 21.5)   # dB on a bar's knocks, bar by bar: EVERY SAYING AS LOUD AS THE FIRST. Read on the bench (b/again1.txt) with none: everything's loudest 50 ms fell from -40.7 dBFS in the first bar to -64.7 in the last, the peaks' 6 dB a pass taken off and no more; those (0, 5.4, 10.7, 15.6, 19.7, 22.6, 23.8, 24) put every bar's loudest 50 ms where the first bar's is ON THE BENCH. THE SECOND BUILD: in the song's master the eight bars' loudest 50 ms came out -20.2 -20.3 -20.2 -20.6 -22.2 -18.8 -17.6 -17.6 dBFS on seed 0 and -20.4 -20.6 -20.4 -20.8 -22.0 -18.9 -18.2 -18.0 on seed 11 (the master lifts what is left of the last bars more than it lifts the knocks): each bar turned by the middle of the two seeds' distance from the first bar (-0.00 +0.19 +0.03 +0.44 +1.85 -1.38 -2.38 -2.46 dB)
LUC_GAIN = os.environ.get("C11T3_LUC_GAIN", "-19.3dB")   # the first bar's fader; bar j is LUC_UP * j lower and LUC_TRIM[j] higher. THE BENCH FIRST (the row alone, -20 dB): every bar's loudest 50 ms -40.7 to -40.7 dBFS; the first build set for -22 dBFS in the song with 18 dB of lift, a guess
AIR_PAN = 0.4                                          # the other ear
RAIL_VEL = 0.8
SONIC_AT = tuple(int(x) for x in os.environ.get("C11T3_SONIC_AT", "90").split(","))    # the bar lines (bars from 0) on which it is nearest: two bars after the last of the three that went by
SONIC_MACH = 2.0                                       # its speed, in speeds of sound: at 2 its past is heard at the tempo it happened at
SONIC_AWAY = 2                                         # sixteenths of sound away at its nearest (81.7 m: as far as the pipes are long)
SONIC_EVERY = 0.5                                      # beats between its strokes
SONIC_PHASE = 0.5                                      # of that, from its nearest point to the stroke after: it strikes half an interval before and after, not AT the nearest
SONIC_NOTES = ("D3", "F3", "G3", "A3", "Bb3", "C4", "D4", None, None, "G4", "A4", "Bb4")    # what it strikes, in order: the pipes' scale, going on up; it rests for the two strokes nearest its passing (E4 would be folded over the instant the first sound arrives; F4, 115 m off, came out as loud as the bass drum when the rest were right)
SONIC_BEFORE = 8                                       # of those, how many it strikes before it is nearest
SONIC_RING = 0.12                                      # seconds a stroke rings where it is struck
SONIC_PAN = 0.9                                        # what is far to one side is this far to that side
SONIC_GAIN = os.environ.get("C11T3_SONIC_GAIN", "-12dB")  # set in the whole song's master: at -16dB (and every stroke only as loud as it is near) the far bells came out 12 to 18 dB under the music between 100 and 450 Hz and the ones going away 3 dB over the ones heard backwards
WHISTLE = os.environ.get("C11T3_WHISTLE", "1") != "0" and NEXTROOM and PIPES_ON     # v18: the pipes whistle (culvert whistlers)
WHISTLE_BEATS = 1                                      # beats from the click to the pipe's far end and back: the pipe is 81.7 m long
WHISTLE_ECHOES = 3                                     # times the far end is heard: on the three beats after the click
WHISTLE_END = -2.0                                     # dB the far end takes each time
WHISTLE_WALL = -0.15                                   # dB a glance off the pipe's wall takes (rough concrete: 3 in a hundred)
WHISTLE_SPREAD = 0.5                                   # what comes back falls as 1 over the distance to this power: a half, because the pipe's floor and roof keep the sound in (in the open it would be 1)
WHISTLE_SIDE = 1.0                                     # where you stand: 1 beside the pipe's mouth, where what comes out is heard as the sine of the angle it comes out at (the click that came straight back goes straight past; the steep ways come out sideways); 0 in the mouth, where the echo's own tick was 25 dB over its whistle and as loud as the song's click
WHISTLE_FLOOR = -36.0                                  # dB under the loudest: what comes back quieter is not sounded
WHISTLE_NOTE = os.environ.get("C11T3_WHISTLE_NOTE", "G4")     # every arrival is the stairs' tick, 5 ms of a sine on this note: low, so that the whistle is heard and not the tick's own note (on E6 the tick rang at 1319 Hz through every whistle; on G4 the pitch read from the sound follows the arithmetic from 20 ms in)
WHISTLE_GAIN = os.environ.get("C11T3_WHISTLE_GAIN", "-32dB")  # set in the whole song's master, which reads it 16 dB over a render of it alone in these bars and is linear at this level (at -38 dB nothing else moved by 0.001 dB): the first whistle 12 to 14 dB under the row
NEXTROOM_MAINS = 60.0                                  # the mains, Hz, in the building you are walking to
NEXTROOM_PARTS = (2, 3)                                # the multiples of the mains that reach you: twice (the transformer's own note) and three times
NEXTROOM_NOTE = "A2"                                   # the note the held voice is written on (not what sounds: its tones are tuned from it to the mains)
NEXTROOM_WALL = 6.0                                    # dB a wall keeps back for every octave up (the mass law)
NEXTROOM_NEAR = 0.25                                   # sixteenths of sound from the next door at the end of the last bar: as near as the first bar of the walk is to this one
NEXTROOM_GAIN = os.environ.get("C11T3_NEXT_GAIN", "-62dB")    # at the nearest. Set in the whole song's master, where it reads 12 dB over its fader: -50 dBFS in the last bar. At -40 and -46 dB it was louder than the click it is heard with
NEXTROOM_RELEASE = "60ms"                              # it stops with the song: nothing of it rings into the tail
FLY = os.environ.get("C11T3_FLY", "1") != "0" and os.environ.get("C11T3_BIRD", "1") != "0" and BALL     # v16: a fourth, a fifth, an octave go by (Doppler; the engine's orbit on a line)
FLY_PASSES = ((7, "A7", 86), (5, "E7", 87), (3, "A6", 88))                     # (n: it goes at 1/n of the speed of sound, so comes and goes (n+1)/(n-1) apart; the note it is heard on as it comes; the bar, from 0, on whose first beat it is nearest)
FLY_RADIUS = 20.0                                                              # metres out to each side (the engine's most)
FLY_DIST = float(os.environ.get("C11T3_FLY_DIST", "5"))                        # metres in front at its nearest: at 2 m all but the last tenth of a second is 12 dB or more under the nearest point, and the notes it comes and goes on are hardly heard
FLY_GAIN = os.environ.get("C11T3_FLY_GAIN", "-30dB")                           # set in the WHOLE SONG's master: at its nearest each then peaks 13 dB under the click (at -18 dB they peaked -2 to -3 dBFS, as loud as the click, and the bars were 2 to 4 dB louder; at -24 dB 7 under; at -36 dB 19 under)
BIRD = os.environ.get("C11T3_BIRD", "1") != "0" and BALL                        # v15: a bird in the hangar (the engine's orbit: a source on a circle)
BIRD_IN, BIRD_BARS = "the hangar", (0, 8)              # the section, and the bars of it: while the drum and the bass rest
BIRD_RADIUS, BIRD_AHEAD = 6.0, 4.0                     # m: the circle, and how far in front of you its centre is (so 2 m behind you at the nearest, 10 m in front at the farthest)
BIRD_LAP = 2                                           # bars to go once round
BIRD_PHASE = float(os.environ.get("C11T3_BIRD_PHASE", "0"))   # where on the circle it is at the section's first beat (0..1 of a lap)
BIRD_EVERY = 3                                         # sixteenths between calls
BIRD_CALL = (("E8", 0.0, 0.03, 0.7), ("A8", 0.0625, 0.04, 0.9))   # a call: (note, beats after the call's time, length in beats, velocity)
BIRD_GAIN = os.environ.get("C11T3_BIRD_GAIN", "-22dB")                         # set in the WHOLE SONG's master: at -14 dB the call it makes as it passes behind your head peaked -2.2 dBFS, as loud as the click's strokes (-1.7); 8 dB under that the click leads and the bird is 8 dB under it at its nearest
BIRD_AIR = "-10dB"                                     # what of it goes to the hangar's air
BALL_RESTS = tuple(int(x) for x in os.environ.get("C11T3_BALL_RESTS", "16,32,48,72,80,96,112,128,136").split(",") if x)   # the bar lines (bars from the start) on which it comes to rest: every door but the last, and the turn of a row in the long rooms
BALL_BEATS = 7.25                                                               # beats from its first bounce to rest: the first bounce is on the fourth sixteenth of a bar (not on the bass drum, not on the click)
BALL_E = 2 ** (-1 / float(os.environ.get("C11T3_BALL_HALVES", "6")))            # what a bounce keeps of the speed (0.891; a table-tennis ball's is about 0.9): every flight is this times the last, so the bounces come twice as fast every six
BALL_LAST = 0.010                                                               # s: a bounce is not sounded once the flights are shorter than this
BALL_NOTE = os.environ.get("C11T3_BALL_NOTE", "A6")                              # the fifth: on D6 it made the song more like Least Common in its notes (the scorer's chroma 0.715 to 0.744)
BALL_VEL = 0.9
BALL_GAIN = os.environ.get("C11T3_BALL_GAIN", "-6dB")
BALL_WALL = "-6dB"                                                              # how loud it reaches a wall (as the tock does)
BALL_AIR = "-2dB"                                                               # ... and the far air (as the tock does)
BALL_SIDE = 0.5                                                                 # it rolls from this far to one side to this far to the other, and back the next time
GRAVITY = 9.81
if BALL:
    FIRST = {**FIRST, "ball": BALL_WALL}


def ball_flights():
    """(seconds after the first bounce, the flight that follows in seconds, dB) of every bounce of one fall."""
    t1 = BALL_BEATS * 60 / BPM * (1 - BALL_E)
    out, t, k = [], 0.0, 0
    while t1 * BALL_E ** k >= BALL_LAST:
        out.append((t, t1 * BALL_E ** k, 20 * math.log10(BALL_E) * k)); t += t1 * BALL_E ** k; k += 1
    return out


def ball_height():
    """Metres it fell: a flight of T after a fall from h is T = 2 e sqrt(2 h / g)."""
    t1 = BALL_BEATS * 60 / BPM * (1 - BALL_E)
    return GRAVITY * (t1 / (2 * BALL_E)) ** 2 / 2


def nextroom_span():
    """(first bar, bar after the last), from 0: the walk away across the square (the last section)."""
    return SECS[-1][1], SECS[-1][1] + SECS[-1][2]


def nextroom_metres(x):
    """How far off the next room's wall is at bar x (a fraction is a place in the bar): you walk the square, FAR sixteenths of sound, in the section."""
    b0, b1 = nextroom_span()
    return (NEXTROOM_NEAR + FAR * (b1 - x) / (b1 - b0)) * STEP * 60 / BPM * SOUND


def nextroom_db(x):
    """dB under its level at the nearest: sound falls as 1 over the distance."""
    return -20 * math.log10(nextroom_metres(x) / nextroom_metres(nextroom_span()[1]))


def nextroom_lane():
    """0 at the nearest, 1 at the farthest, a point every half bar."""
    b0, b1 = nextroom_span(); most = -nextroom_db(b0)
    return [pt(0, 1.0)] + [pt(b0 + k / 2, -nextroom_db(b0 + k / 2) / most) for k in range(2 * (b1 - b0) + 1)]


def fly_facts():
    """For each pass: (n, m/s, seconds on the line, the patch's ratio to the written note, Hz it sings, Hz coming, Hz going, seconds of the song at its nearest, lap rate, phase)."""
    out = []; end = FLY_RADIUS / math.hypot(FLY_RADIUS, FLY_DIST)           # how much of its speed is toward you at the ends of the line
    for n, heard, bar in FLY_PASSES:
        v = SOUND / n / end; T = 2 * FLY_RADIUS / v; tc = bar * BEATS * 60 / BPM; f_in = 440.0 * 2 ** ((NOTE_NUM(heard) - 69) / 12)
        ratio = n / (n + 1); f0 = f_in * ratio
        out.append((n, v, T, ratio, f0, f_in, f0 * (n - 1) / n, tc, 1 / T, (-(tc - T / 2) / T) % 1.0))
    return out


def NOTE_NUM(name):
    """MIDI number of a note name such as A7 or Bb3."""
    k = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[name[0]] + name.count("#") - name[1:].count("b")
    return k + 12 * (int(name.lstrip("ABCDEFG#b")) + 1)


def bird_span():
    """(first bar, last bar + 1) in which the bird flies, or None."""
    sec = next((x for x in SECS if x[0] == BIRD_IN), None)
    return (sec[1] + BIRD_BARS[0], sec[1] + BIRD_BARS[1]) if BIRD and sec is not None else None


def bird_rate():
    """Laps a second."""
    return BPM / 60 / BEATS / BIRD_LAP


def bird_notes():
    b0, b1 = bird_span()
    return [note(n * STEP + dt, p, ln, v) for n in range(b0 * 16, b1 * 16, BIRD_EVERY) for p, dt, ln, v in BIRD_CALL]


def bird_facts():
    """Speed m/s, nearest and farthest m, the most the pitch moves in cents, the level between nearest and farthest in dB."""
    v = 2 * math.pi * BIRD_RADIUS * bird_rate(); near, far = abs(BIRD_RADIUS - BIRD_AHEAD), BIRD_RADIUS + BIRD_AHEAD
    vr = v * min(1.0, BIRD_AHEAD / BIRD_RADIUS)        # the most of its speed that is towards or away from you
    return v, near, far, 1200 * math.log2(SOUND / (SOUND - vr)), 20 * math.log10(far / near)


def ball_notes():
    beat = 60 / BPM
    return [{"at": round(r * BEATS - BALL_BEATS + t / beat, 5), "len": 0.05, "pitch": BALL_NOTE, "vel": round(BALL_VEL * 10 ** (db / 40), 4)}
            for r in (BALL_RESTS if BALL else ()) for t, fl, db in ball_flights()]


def ball_lane():
    """Where it is from side to side: across as it bounces, and back the next time."""
    pts, side = [(0.0, -BALL_SIDE)], -BALL_SIDE
    for r in BALL_RESTS:
        pts += [(r * BEATS - BALL_BEATS, side), (r * BEATS, -side)]; side = -side
    return [[f"{x:g}b", y] for x, y in pts + [(TOTAL, side)]]


def flut_span():
    """The bars of the corridor, or None."""
    if not FLUT:
        return None
    sec = next((x for x in SECS if x[0] == FLUT_IN), None)
    return (sec[1], sec[1] + sec[2]) if sec else None


def flut_where(bar):
    """How far from the left wall, as a share of the corridor's width, at a time in bars (0.5 is the middle)."""
    u = bar - flut_span()[0] - FLUT_STILL
    return 0.5 if u <= 0 else 0.5 - FLUT_REACH * math.sin(2 * math.pi * u / FLUT_TURN)


def flut_rings():
    """Every time the side walls ring: (beat, velocity, share of the width from the left wall)."""
    b0, b1 = flut_span()
    out = []
    for room, a, b, p0, p1, opn, shut in places():
        if not b0 <= p0 < b1:
            continue
        for bar in range(int(round(p0)), int(round(p1))):
            for k in range(FLUT_RETURNS + 1):
                at = bar * BEATS + (CLICK(bar)[0][0] + k * (a + b)) * STEP      # the click, and each time it has been to both ends and back
                if at < b1 * BEATS:
                    out.append((at, 0.9 * FLUT_BACK ** (k / 2), flut_where(at / BEATS)))   # the patch's loudness goes as the square of the velocity
    return out


def flut_notes(side):
    """One ear's two trains of clicks, each a saw on the corridor's note (an edge every crossing and back): the one
    that came off the near wall first (twice the distance to it), then the one that has been off both (twice the width)."""
    beat = 60 / BPM
    out = []
    for at, vel, w in flut_rings():
        first = round(at * beat * FLUT_RATE)
        for way in (2 * (w if side == "l" else 1 - w) * FLUT_WIDE, 2 * FLUT_WIDE):
            out.append({"at": round((first + round(way / SOUND * FLUT_RATE) + 0.25) / FLUT_RATE / beat, 7), "len": round(FLUT_RING / beat, 4), "pitch": FLUT_NOTE, "vel": round(vel, 3)})
    return sorted(out, key=lambda n: n["at"])


def crowd_times():
    """(the beat applause begins, the beat the pull begins, the beat the house is full, the beat of the door), or None."""
    st = house_stages() if CROWD else []
    if len(st) < 3:
        return None
    sec = next(x for x in SECS if x[0] == HOUSE_IN)
    return st[1][1], st[1][2], st[2][1], (sec[1] + sec[2]) * BEATS


_CROWD = {}


def crowd_claps():
    """Every clap: (the beat at which the hands meet, the person). A phase a person; a clap each time it comes round."""
    if "ev" in _CROWD:
        return _CROWD["ev"]
    t_app, t_pull, t_full, t_end = crowd_times()
    n = len(CROWD_ROWS) * len(CROWD_PANS)
    fr = lambda x: x - math.floor(x)
    ev, dt = [], 1 / 96
    for i in range(n):
        u1, u2, u3, u4 = fr((i + 1) * GOLD), fr((i + 1) * GOLD * GOLD * 7 + 0.31), fr((i + 1) * 0.754877666), fr((i + 1) * 0.569840291)
        eps = CROWD_SPREAD * (2 * u1 - 1)
        first = i < n // 2                                         # the half house, who are in when applause begins; the rest come in while the pull grows
        t_on = t_app + 0.875 * u2 * (t_pull - t_app) if first else t_pull + (0.0625 + 0.875 * u2) * (t_full - t_pull)
        t_half = t_pull + 0.8 * u3 * (t_full - t_pull) if first else t_on
        th, t = 2 * math.pi * u4, t_on
        while t < t_end - 1e-9:
            fast = t < t_half
            w = 2 * math.pi * (2 if fast else 1) * (1 + (eps if fast else eps / 2))
            k = 0.0 if fast else CROWD_PULL * min(1.0, max(0.0, (t - t_pull) / (t_full - t_pull)))
            dth = (w + k * math.sin(2 * math.pi * t - th)) * dt
            if math.floor((th + dth) / (2 * math.pi)) > math.floor(th / (2 * math.pi)) and t < t_end - 0.5:      # the last clap is on the last beat before the door: nobody claps on the door's own first beat
                ev.append((t + (2 * math.pi * math.ceil(th / (2 * math.pi) - 1e-12) - th) / dth * dt, i))
            th += dth; t += dt
    _CROWD["ev"] = sorted(ev)
    return _CROWD["ev"]


def crowd_notes(j):
    """What is heard of the people in place j of every row: each clap later by its row's distance and quieter by it."""
    out = []
    for t, i in crowd_claps():
        if i % len(CROWD_PANS) == j:
            r = CROWD_ROWS[i // len(CROWD_PANS)]
            out.append({"at": round(t + r / SOUND * BPM / 60, 5), "len": 0.05, "pitch": "C5", "vel": round(CROWD_ROWS[0] / r, 3)})
    return out


def crowd_step(bar):
    """(claps in the bar, how far in step they are (0 nobody, 1 one clap), their spread about the beat in ms)."""
    e = [t for t, i in crowd_claps() if bar * BEATS <= t < (bar + 1) * BEATS]
    if not e:
        return 0, 0.0, 0.0
    r = abs(sum(complex(math.cos(2 * math.pi * t), math.sin(2 * math.pi * t)) for t in e)) / len(e)
    return len(e), r, 1000 * 60 / BPM * math.sqrt(sum((((t + 0.5) % 1) - 0.5) ** 2 for t in e) / len(e))


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


def whistle_far():
    """Metres from the click to the pipe's far end and back."""
    return WHISTLE_BEATS * 60 / BPM * SOUND


def whistle_arrivals(width, n, until):
    """(seconds after the click, level) of what comes back the n-th time from the far end of a pipe `width` metres across, up to `until`
    seconds after the click: the echo itself (k = 0), then the click by way of k glances off the walls (two ways for each k), which has farther to come."""
    far, out, k = whistle_far(), [], 0
    while True:
        r = math.hypot(n * far, k * width)
        if r / SOUND >= until:
            return out
        lv = (far / r) ** WHISTLE_SPREAD * 10 ** ((WHISTLE_END * (n - 1) + WHISTLE_WALL * k) / 20) * (0.5 if k == 0 else 1.0) * (k * width / r) ** WHISTLE_SIDE
        out.append((r / SOUND, lv))
        k += 1


def whistle_heard(width, n, after):
    """Hz heard `after` seconds into the n-th echo: one click for every width, seen from where the sound has got to."""
    t0 = n * whistle_far() / SOUND
    return SOUND / width / math.sqrt(1 - (t0 / (t0 + after)) ** 2)


def whistle_pipes():
    """Every pipe the click stands in: (its note, metres across, the bar)."""
    return [(p, SOUND / (2 * hz(p)), b) for _, p, _, b0, b1 in pipes() for b in range(b0, b1)] if WHISTLE else []


def luc_row():
    """The first bar (from 0) of the row in which a knock is said into the room again and again, or None."""
    sec = next((x for x in SECS if x[0] == LUC_IN[0]), None)
    return sec[1] + ROW * LUC_IN[1] if LUC and sec is not None and LUC_IN[1] * ROW < sec[2] else None


def luc_q(n):
    """The q of the eq peak on way n: a ring that falls to 1/e in LUC_TAU (the textbook peak's pole, times LUC_Q for the engine's)."""
    return math.pi * STAND_ROOT * n * LUC_TAU / 10 ** (LUC_UP / 40) * LUC_Q


def luc_knocks():
    """[(bar of the row from 0 = passes it has been through, beat of the song)]: LUC_AT in every bar of the row."""
    b0 = luc_row() * BEATS; assert len(LUC_TRIM) == ROW
    return [(j, b0 + j * BEATS + q) for j in range(ROW) for q in LUC_AT]


def dull_row():
    """The first bar (from 0) of the row in which a knock is duller and no softer, or None."""
    sec = next((x for x in SECS if x[0] == DULL_IN[0]), None)
    return sec[1] + ROW * DULL_IN[1] if DULL and sec is not None and DULL_IN[1] * ROW < sec[2] else None


def dull_cut(k):
    """Hz: the low-pass of step k."""
    return DULL_TOP / 2 ** (k * DULL_STEP)


def dull_knocks():
    """[(knock from 0, beat of the song, step)]: two a bar for ROW bars; the first of a bar is step 0, the second the bar's step."""
    b0 = dull_row() * BEATS; assert len(DULL_TRIM) == 2 * ROW
    return [(2 * j + q, b0 + j * BEATS + DULL_AT[q], j if q else 0) for j in range(ROW) for q in range(2)]


def cloud_row():
    """The first bar (from 0) of the row in which a cloud becomes a point, or None."""
    sec = next((x for x in SECS if x[0] == CLOUD_IN[0]), None)
    return sec[1] + ROW * CLOUD_IN[1] if CLOUD and sec is not None and CLOUD_IN[1] * ROW < sec[2] else None


def cloud_bursts():
    """[(hiss from 0, beat of the song, how alike the two ears are 0 to 1, beat of the bar's place in CLOUD_AT)]: CLOUD_AT in each of CLOUD_BARS bars."""
    b0 = cloud_row() * BEATS; n = len(CLOUD_AT); assert len(CLOUD_LIKE) == CLOUD_BARS <= ROW
    return [(i, b0 + (i // n) * BEATS + CLOUD_AT[i % n], CLOUD_LIKE[i // n], i % n) for i in range(CLOUD_BARS * n)]


def rung_row():
    """The first bar (from 0) of the row with the ladder, or None."""
    sec = next((x for x in SECS if x[0] == RUNG_IN[0]), None)
    return sec[1] + ROW * RUNG_IN[1] if RUNG and sec is not None and RUNG_IN[1] * ROW < sec[2] else None


def rung_note(k):
    """The kth rung's note by name (0 the lowest)."""
    m = RUNG_FROM + 12 * (k // len(RUNG_STEPS)) + RUNG_STEPS[k % len(RUNG_STEPS)]
    return ("C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B")[m % 12] + str(m // 12 - 1)


def rung_pips():
    """[(the beat it begins on, its rung, its velocity)]: down RUNG_N rungs and up again, one a beat."""
    b0 = rung_row() * BEATS; ks = list(range(RUNG_N - 1, -1, -1)) + list(range(RUNG_N))
    return [(b0 + i + RUNG_AT[i % BEATS], k, round(10 ** ((RUNG_TRIM[i] if RUNG_TRIM else 0.0) / 40), 5)) for i, k in enumerate(ks)]


def ears_row():
    """The first bar (from 0) of the row of the two walks, or None."""
    sec = next((x for x in SECS if x[0] == EARS_IN[0]), None)
    return sec[1] + ROW * EARS_IN[1] if EARS and sec is not None and EARS_IN[1] * ROW < sec[2] else None


def ears_pips():
    """[(walk, degrees, beat of the song, s the left ear gets it later than the right (minus: sooner), dB the right ear gets it louder than the left)]."""
    out = []; per = ROW // len(EARS_WALKS); wait = per - len(EARS_ANGLES) // len(EARS_AT)
    for i, w in enumerate(EARS_WALKS):
        for k, a in enumerate(EARS_ANGLES):
            th = math.radians(a); bar, j = divmod(k, len(EARS_AT))
            out.append((w, a, (ears_row() + i * per + wait + bar) * BEATS + EARS_AT[j], EARS_HEAD / SOUND * (th + math.sin(th)) if w == "time" else 0.0, EARS_LEVEL * math.sin(th) if w == "level" else 0.0))
    return out


def recede_row():
    """The first bar (from 0) of the row in which the knock goes away, or None."""
    sec = next((x for x in SECS if x[0] == RECEDE_IN[0]), None)
    return sec[1] + ROW * RECEDE_IN[1] if RECEDE and sec is not None and RECEDE_IN[1] * ROW < sec[2] else None


def recede_knocks():
    """[(beat struck, beat heard, step (0 the nearest), metres off, the knock's velocity)]: out and back, two a bar."""
    assert 2 * RECEDE_STEPS == len(RECEDE_AT) * ROW == len(RECEDE_TRIM)
    out = []
    for j in range(2 * RECEDE_STEPS):
        k = j if j < RECEDE_STEPS else 2 * RECEDE_STEPS - 1 - j
        m = RECEDE_FAR / 2 ** (RECEDE_STEPS - 1 - k); struck = (recede_row() + j // 2) * BEATS + RECEDE_AT[j % 2]
        out.append((round(struck, 7), round(struck + m / SOUND * BPM / 60, 7), k, m, round(2 ** (-k / 2) * 10 ** (RECEDE_TRIM[j] / 40), 5)))
    return out


def kept_row():
    """The first bar (from 0) of the row in which the room holds its breath, or None."""
    sec = next((x for x in SECS if x[0] == KEPT_IN[0]), None)
    return sec[1] + ROW * KEPT_IN[1] if KEPT and sec is not None and KEPT_IN[1] * ROW < sec[2] else None


def kept_times():
    """(the beat of the clap, the beat the hall stops dying, the beat it lets go)."""
    c = (kept_row() + KEPT_CLAP[0]) * BEATS + KEPT_CLAP[1]
    return c, c + KEPT_FROM, (kept_row() + KEPT_TO[0]) * BEATS + KEPT_TO[1]


def well_ways():
    """[(flights, the column's lowest way in Hz, [(k, Hz)] the ways written: its kth multiples inside WELL_BAND, the beat the ring begins)]: one for every thud."""
    one = SOUND / (2 * DROP_STEPS * DROP_RISER)
    return [(n, one / n, [(k, k * one / n) for k in range(1, 200) if WELL_BAND[0] <= k * one / n <= WELL_BAND[1]], land) for n, _, _, _, _, land, _ in drop_falls()]


def drop_row():
    """The first bar (from 0) of the row in which something is let go down the stairwell, or None."""
    sec = next((x for x in SECS if x[0] == DROP_IN[0]), None)
    return sec[1] + ROW * DROP_IN[1] if DROP and sec is not None and DROP_IN[1] * ROW < sec[2] else None


def drop_falls():
    """[(flights, metres, seconds of fall, seconds of the sound's way up, beat let go, beat heard to land, dB)]: one a bar, a flight higher each bar."""
    import math
    out = []
    for n in range(1, ROW + 1):
        h = n * DROP_STEPS * DROP_RISER; fall = math.sqrt(2 * h / DROP_G); up = h / SOUND; at = (drop_row() + n - 1) * BEATS + DROP_AT
        out.append((n, h, fall, up, at, round(at + (fall + up) * BPM / 60, 7), -10 * math.log10(n)))
    return out


def close_row():
    """The first bar (from 0) of the row in which the walls close in, or None."""
    sec = next((x for x in SECS if x[0] == CLOSE_IN[0]), None)
    return sec[1] + ROW * CLOSE_IN[1] if CLOSE and sec is not None else None


def close_trains():
    """[(bar of the row from 0, doublings, samples across and back, beat of the knock, [(beat, dB), ...])]: a knock and its echoes between two walls, twice a bar."""
    out = []
    for b in range(ROW):
        step = CLOSE_STEPS[b]; per = CLOSE_NEAR * 2 ** step
        for at in CLOSE_AT:
            s0 = (close_row() + b) * BEATS + at; es = []; k = 0
            if s0 + CLOSE_END / CLOSE_FALL * BPM / 60 > (close_row() + ROW) * BEATS:
                continue
            while CLOSE_FALL * k * per / CLOSE_RATE <= CLOSE_END:
                t = k * per / CLOSE_RATE
                es.append((round(s0 + t * BPM / 60, 7), -CLOSE_FALL * t - CLOSE_SHARE * (max(CLOSE_STEPS) - step))); k += 1
            out.append((b, step, per, s0, es))
    return out


def began_row():
    """The bar (from 0) of the first tone that stays where it began, or None."""
    sec = next((x for x in SECS if x[0] == BEGAN_IN[0]), None)
    return sec[1] + ROW * BEGAN_IN[1] if BEGAN and sec is not None else None


def began_tones():
    """[(beat, note, whether it has its start)]: every tone of BEGAN_TUNE twice, first with its start (on the left), then without."""
    n = BEGAN_IN[2] * ROW // BEGAN_EVERY
    assert n == 2 * len(BEGAN_TUNE), (n, len(BEGAN_TUNE))
    return [((began_row() + k * BEGAN_EVERY) * BEATS + BEGAN_AT, BEGAN_TUNE[k // 2], k % 2 == 0) for k in range(n)]


def foot_bar():
    """The bar (from 0) on whose first beat the drum and the bass stop at the foot of the stairs, or None."""
    sec = next((x for x in SECS if x[0] == FOOT_IN), None)
    return sec[1] if FOOT and sec is not None else None


def slam_bar():
    """The bar (from 0) on whose first beat the door shuts, or None."""
    sec = next((x for x in SECS if x[0] == SLAM_IN), None)
    return sec[1] if SLAM and sec is not None else None


def slam_rt(db_km):
    """Seconds for the sound to fall 60 dB in the hangar where the air takes db_km dB a kilometre: Sabine's 0.161 V / (S a + 4 m V)."""
    w, d, h = SLAM_HALL
    vol, surf = w * d * h, 2 * (w * d + w * h + d * h)
    return 0.161 * vol / (surf * SLAM_WALLS + 4 * (db_km / 1000 / (10 / math.log(10))) * vol)


def slam_bands():
    """One tuple a band: (lower edge Hz, upper edge Hz, seconds to fall 60 dB, dB of its fader against SLAM_GAIN)."""
    out = []
    for k, air in enumerate(SLAM_AIR):
        lo, hi = SLAM_EDGES[k], SLAM_EDGES[k + 1]
        mid0, mid = math.sqrt(SLAM_EDGES[0] * SLAM_EDGES[1]), math.sqrt(lo * hi)
        out.append((lo, hi, slam_rt(air), SLAM_TRIM[k] + SLAM_TILT * math.log2(mid / mid0) - 10 * math.log10((hi - lo) / (SLAM_EDGES[1] - SLAM_EDGES[0]))))      # white noise has as much in every hertz: a wider band is turned down by its width
    return out


def slam_direct():
    """dB by which the slam itself stands over the tail it starts, SLAM_AWAY metres from the door: 20 log of the hall's own distance (0.057 root (V / T), with T the middle band's) over yours."""
    w, d, h = SLAM_HALL
    return 20 * math.log10(0.057 * math.sqrt(w * d * h / slam_bands()[len(SLAM_AIR) // 2][2]) / SLAM_AWAY)


def slam_db(k, t):
    """dB written on band k's lane t seconds after the door shuts."""
    if t < 0:
        return SLAM_FLOOR
    if t <= SLAM_DIRECT:
        return slam_direct()
    return max(SLAM_FLOOR, -60 * t / slam_bands()[k][2])


def bend_way(beat):
    """Metres from the corner at this beat (0 at the corner and after it)."""
    b0, b1 = BEND_BARS[0] * BEATS, BEND_BARS[1] * BEATS
    return BEND_FROM * max(0.0, min(1.0, (b1 - beat) / (b1 - b0)))


def bend_shadow(f, way):
    """dB the corner takes from a tone of f Hz heard `way` m short of it (Maekawa): the way round is BEND_SIDE + way, the way through the wall the hypotenuse."""
    longer = BEND_SIDE + way - math.hypot(BEND_SIDE, way)
    return -10 * math.log10(3 + 20 * (2 * longer * f / SOUND))


def bend_spread(way):
    """dB the longer way takes (the corridor's law), against standing at the corner."""
    return -20 * BEND_LAW * math.log10((BEND_SIDE + way) / BEND_SIDE)


def gal_row():
    """The first bar of the row with the whispering gallery, or None."""
    sec = next((x for x in SECS if x[0] == GAL_IN[0]), None)
    return sec[1] + ROW * GAL_IN[1] if GAL and sec is not None and GAL_IN[1] * ROW < sec[2] else None


def gal_arrivals():
    """One tuple an arrival: (the whisper's number, side (-1 left: the short way round; 1 right), times round before it, the beat it is heard on, metres of wall behind it, dB against the first arrival)."""
    b0, lap_m = gal_row(), GAL_LAP * STEP * 60 / BPM * SOUND
    out = []
    for w in range(ROW // GAL_EVERY):
        at = (b0 + w * GAL_EVERY) * BEATS + GAL_ON * STEP
        for k in range(GAL_TIMES):
            for side, frac in ((-1, k + GAL_AT), (1, k + 1 - GAL_AT)):
                out.append((w, side, k, at + frac * GAL_LAP * STEP, frac * lap_m, -20 * GAL_LAW * math.log10(frac / GAL_AT) - GAL_LOSS * (frac - GAL_AT)))
    return sorted(out, key=lambda x: x[3])


def rail_row():
    """The first bar of the row with the rail, or None."""
    sec = next((x for x in SECS if x[0] == RAIL_IN[0]), None)
    return sec[1] + ROW * RAIL_IN[1] if RAIL and sec is not None and RAIL_IN[1] * ROW < sec[2] else None


def rail_knocks():
    """One tuple a knock: (mark, metres off, the beat it is struck on, the beat the steel brings it, the beat the air brings it, the steel's dB, the air's dB).
    The air's knock is ON the grid (RAIL_ON); the knock is struck a thirty-second a mark before; the steel brings it metres / RAIL_SPEED after that."""
    assert len(RAIL_MARKS) == ROW * len(RAIL_ON), len(RAIL_MARKS)
    b0 = rail_row(); beat = 60 / BPM; out = []
    for j, k in enumerate(RAIL_MARKS):
        air = (b0 + j // len(RAIL_ON)) * BEATS + RAIL_ON[j % len(RAIL_ON)] * STEP
        m = k * beat / 8 * SOUND; struck = air - k / 8
        out.append((k, m, struck, struck + m / RAIL_SPEED / beat, air, -RAIL_LOSS * k, -20 * AIR_LAW * math.log10(k)))
    return out


def duct_row():
    """The first bar of the row with the duct, or None."""
    sec = next((x for x in SECS if x[0] == DUCT_IN[0]), None)
    return sec[1] + ROW * DUCT_IN[1] if DUCT and sec is not None and DUCT_IN[1] * ROW < sec[2] else None


def duct_hz():
    semis = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[DUCT_NOTE[0]] + (-1 if "b" in DUCT_NOTE else 0)
    return 440 * 2 ** ((semis + 12 * (int(DUCT_NOTE[-1]) + 1) - 69) / 12)


def duct_over(since, back):
    """How many times its own note a way across is, `since` seconds after the straight sound is back from a duct `back` seconds there and back. A wave going across as well as along goes along more slowly, sqrt(1 - (own / f)^2) of the speed of sound: so the note f is back after back / sqrt(1 - (own / f)^2), and the note that is back at the time t is own / sqrt(1 - (back / t)^2): from above, down to the duct's own note, which never arrives."""
    return 1 / math.sqrt(1 - (back / (back + since)) ** 2)


def duct_first(back):
    """Seconds after the straight sound that a way across is at DUCT_TOP times its note."""
    return back * (1 / math.sqrt(1 - 1 / DUCT_TOP ** 2) - 1)


def duct_echoes():
    """[(the beat it begins, its length in beats, seconds there and back, [(beat, semitones over the duct's note)])]: an echo for each click of the row."""
    b0 = duct_row(); sec = 60 / BPM; out = []
    if b0 is None:
        return out
    starts = [(b0 + j) * BEATS + (CLICK_STEP + p) * STEP + duct_first(p * STEP * sec) / sec for j, p in enumerate(DUCT_BACK)]
    for j, p in enumerate(DUCT_BACK):
        back = p * STEP * sec; at = starts[j]; first = duct_first(back)
        length = (starts[j + 1] - at - 0.1) if j + 1 < len(starts) else (b0 + ROW) * BEATS - at - 0.05
        pts = []
        for q in range(DUCT_POINTS):
            since = first * (length * sec / first) ** (q / (DUCT_POINTS - 1))             # from `first` to the note's end, evenly in the logarithm
            pts.append((at + (since - first) / sec, 12 * math.log2(duct_over(since, back))))
        out.append((at, length, back, pts))
    return out


def dome_row():
    """The first bar of the row under the dome, or None."""
    sec = next((x for x in SECS if x[0] == DOME_IN[0]), None)
    return sec[1] + ROW * DOME_IN[1] if DOME and sec is not None and DOME_IN[1] * ROW < sec[2] else None


def dome_off(j):
    """How far from the focus you are in bar j of the row, in sixteenths of sound."""
    return DOME_WALK[0] * max(0.0, 1 - j / DOME_WALK[1])


def dome_parts():
    """[(which way round from straight ahead, degrees; the pan)] of every part of the dome."""
    return [((i + DOME_TURN) * 360 / DOME_PARTS, round(DOME_PAN * math.sin(math.radians((i + DOME_TURN) * 360 / DOME_PARTS)), 3)) for i in range(DOME_PARTS)]


def dome_late(j, turn):
    """Sixteenths after the click that the echo from the part `turn` degrees round arrives in bar j: up to the dome (DOME_PATH - DOME_UP), and down from it to where you are: sqrt(up^2 - 2 up off cos + off^2), where cos is the cosine of the angle between the way you walk and the way to that part."""
    off = dome_off(j); c = math.cos(math.radians(DOME_RISE)) * math.cos(math.radians(turn))
    return DOME_PATH - DOME_UP + math.sqrt(DOME_UP ** 2 - 2 * DOME_UP * off * c + off ** 2)


def dome_notes():
    """{part: [note]}: the dome's echo of the row's every click, a note from each part."""
    b0 = dome_row()
    return {i: [{"at": round((b0 + j) * BEATS + (CLICK_STEP + dome_late(j, turn)) * STEP, 5), "len": 0.2, "pitch": "A5", "vel": DOME_VEL} for j in range(ROW)] for i, (turn, _) in enumerate(dome_parts())} if b0 is not None else {}


def four_rows():
    """[(first bar, left, right)]: the rows in which the hangar has four walls."""
    sec = next((x for x in SECS if x[0] == FOUR_IN), None)
    if not FOUR or sec is None:
        return []
    return [(sec[1] + ROW * i, a, b) for i, (a, b) in enumerate(WALK["hangar"]) if (a, b) in FOUR_WALK]


def four_images(a, b):
    """Every echo of one click that has met the wall in front or behind, the click standing a sixteenths (there and back) from the left wall and b from the right: [(sixteenths late, of the way over (-1 left, 1 right), walls met, how many arrive together (the front one and the back one), across, deep)], soonest first."""
    f, k = FOUR_DEEP; out = {}
    for n in range(-FOUR_WALLS, FOUR_WALLS + 1):
        for dx, wx in ((n * (a + b), 2 * abs(n)), (n * (a + b) - a, abs(2 * n - 1))):       # across: past both walls n times ; or to the left wall first
            for m in range(-FOUR_WALLS, FOUR_WALLS + 1):
                for dy, wy in ((m * (f + k), 2 * abs(m)), (m * (f + k) - k, abs(2 * m - 1))):   # deep: the same, front and behind
                    if wy == 0 or wx + wy > FOUR_WALLS:
                        continue
                    key = (dx, abs(dy), wx + wy)
                    out[key] = out.get(key, 0) + 1
    return sorted((math.hypot(dx, dy), dx / math.hypot(dx, dy), w, cnt, dx, dy) for (dx, dy, w), cnt in out.items())


def four_notes():
    """{track number: [note]}: every corner echo of every click in those rows, on the track nearest where it comes from. Nothing is written past the hangar's last bar line."""
    out = {i: [] for i in range(FOUR_PANS)}; rows = four_rows()
    if not rows:
        return out
    end = (rows[-1][0] + ROW) * BEATS
    for b0, a, b in rows:
        for bar in range(b0, b0 + ROW):
            t0 = bar * BEATS + CLICK_STEP * STEP
            for late, over, walls, cnt, dx, dy in four_images(a, b):
                at = t0 + late * STEP
                if at >= end:
                    continue
                level = FOUR_FIRST + FOUR_EACH * (walls - 1) + 20 * math.log10(cnt)
                i = min(range(FOUR_PANS), key=lambda j: abs(four_pan(j) - FOUR_PAN * over))
                out[i].append({"at": round(at, 5), "len": 0.2, "pitch": "A5", "vel": round(FOUR_VEL * 10 ** (level / 20), 4)})
    return {i: sorted(v, key=lambda x: x["at"]) for i, v in out.items()}


def four_pan(j):
    return round(-0.8 + 1.6 * j / (FOUR_PANS - 1), 3)


def sonic_strokes():
    """Every stroke of the thing that goes by faster than sound: (seconds struck after its nearest, the note, metres off, seconds HEARD after its nearest, how many times as fast its sound is heard (under nought: backwards), its level against a stroke at the nearest, how far to the side from -1 to 1)."""
    d = SONIC_AWAY * STEP * 60 / BPM * SOUND; v = SONIC_MACH * SOUND; out = []
    made = -d / (SOUND * SONIC_MACH * math.sqrt(SONIC_MACH ** 2 - 1))           # when it made the sound that is heard first
    for i, p in enumerate(SONIC_NOTES):
        te = (i - SONIC_BEFORE + SONIC_PHASE) * SONIC_EVERY * 60 / BPM; x = v * te; r = math.hypot(d, x)
        if p is None or te < made < te + SONIC_RING:
            continue                                                            # a stroke whose ring is folded over that instant (half of it heard backwards, half forwards, in a hundredth of a second) is left out
        fast = 1 / (1 + v * x / (SOUND * r))
        out.append((te, p, r, te + r / SOUND, fast, d / r * math.sqrt(abs(fast)), x / r))       # as loud as it is near, and as its ring is squeezed: the same stroke heard in a third of the time has three times the power, heard three times as slow a third
    return out


def sonic_first():
    """(seconds after its nearest that the first sound of it is heard, seconds before its nearest that sound was made)."""
    d = SONIC_AWAY * STEP * 60 / BPM * SOUND
    return d / SOUND * math.sqrt(SONIC_MACH ** 2 - 1) / SONIC_MACH, -d / (SOUND * SONIC_MACH * math.sqrt(SONIC_MACH ** 2 - 1))


def whistle_notes():
    out, wp = [], whistle_pipes()
    for i, (p, width, b) in enumerate(wp):
        t = b * BEATS + CLICK_STEP * STEP                    # the click, in beats
        until = (BEATS if i + 1 < len(wp) else BEATS - CLICK_STEP * STEP) * 60 / BPM    # a pipe is heard until the click is in the next one (the last, until the pipes end)
        for n in range(1, WHISTLE_ECHOES + 1):
            out += [(t + sec * BPM / 60, lv) for sec, lv in whistle_arrivals(width, n, until)]
    top = max(lv for _, lv in out)                           # the loudest arrival of all is written 1; what is WHISTLE_FLOOR under it or quieter is not sounded
    return [{"at": round(at, 6), "len": CHIRP_LEN, "pitch": WHISTLE_NOTE, "vel": round(lv / top, 4)} for at, lv in sorted(out) if lv / top >= 10 ** (WHISTLE_FLOOR / 20)]


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
                  "returns": [{"from": "click", "gain": "0dB", "time": "6ms"}, {"from": "tock", "gain": "-2dB", "time": "6ms"}] + ([{"from": "ball", "gain": BALL_AIR, "time": "6ms"}] if BALL else []),
                  "auto": {"far": {"points": step_lane(6, CLOSED, glide=4)}}}
    for i, (n, t_in, t_out) in enumerate(house_stages()):
        far = step_lane(6, CLOSED, glide=4)
        if i == 0:
            out["air"] = {**out["air"], "auto": {"far": {"points": house_lane(far, 0)}}}
        else:                                                      # the hall's wash dies 1 + FULL n times as fast; it is sent no less (a click's wash begins as loud in a full room: only what is left of it later is less)
            out[f"air{i}"] = {"fx": [f"reverb kind=hall decay={AIR_DECAY / (1 + HOUSE_FULL * n):.3g}s size=1 mix=1 predelay=40ms", "lp cutoff=6000", "hp cutoff=300",
                                     {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.far", "amount": 1}]}}],
                              "returns": [{"from": "click", "gain": "0dB", "time": "6ms"}, {"from": "tock", "gain": "-2dB", "time": "6ms"}] + ([{"from": "ball", "gain": BALL_AIR, "time": "6ms"}] if BALL else []),
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
    if crowd_times():
        for q, (lo, pk) in enumerate(((1500, 2200), (2200, 3400))):
            PATCHES[f"sr-hand-{'ab'[q]}"] = {"about": f"Standing Room's pair of hands (chirper-zero, 26 Nov, v12): one person's clap, a 9 ms burst of noise with nothing under {lo} Hz and most round {pk} Hz, and everything above left in: many of them at once are applause. Its loudness is its velocity (how far away the person is).",
                                             "play": {"vel_sens": 0.5},
                                             "synth": {"layers": ["white"], "filters": [{"kind": "hp", "cutoff": lo, "q": 0.7}, f"peak cutoff={pk} q=1.2 gain=5dB"], "amp": {"a": "0.1ms", "d": "9ms", "s": 0, "r": "6ms", "curve": 4}}}
        for j, pan in enumerate(CROWD_PANS):
            doc["tracks"].append({"name": f"crowd-{j}", "patch": f"sr-hand-{'ab'[j % 2]}", "gain": CROWD_GAIN, "pan": pan, "notes": crowd_notes(j)})      # dry: the people are what the room is damped by
        doc["about"] = doc["about"].replace(" Generated by", " From v12 the people clap: applause first, everyone twice a beat at a rate of his own, then one by one they halve it and are pulled to the beat, and when the house is full it is one clap on every beat from 32 pairs of hands, the back row a sixtieth of a second behind the front (how a crowd finds one clap: Neda, 2000). Generated by")
        assert "From v12" in doc["about"]
    if flut_span():
        PATCHES["sr-flutter"] = {"about": "Standing Room's flutter echo (chirper-zero, 26 Nov, v13): a click going across a corridor and back: a saw on the corridor's own note with everything under 5 kHz taken off, so that only its edge is left, one every crossing and back, dying over half a second. Two of them a little apart are the two walls.",
                                 "play": {"vel_sens": 1, "gate": 1},
                                 "synth": {"layers": ["saw phase=0.5"], "filters": [{"kind": "hp", "cutoff": 5000, "q": 0.7}, "peak cutoff=13000 q=0.7 gain=6dB"], "amp": {"a": "1ms", "d": "600ms", "s": 0, "r": "30ms", "curve": 2}}}
        for side, pan in (("l", -1), ("r", 1)):
            doc["tracks"].append({"name": f"flut-{side}", "patch": "sr-flutter", "gain": FLUT_GAIN, "pan": pan, "notes": flut_notes(side)})      # dry: an ear each
        doc["about"] = doc["about"].replace(" Generated by", " From v13 the corridor has its other two walls: the ones beside you, 2.34 m apart, between which the click rattles 73 times a second (a flutter echo on D2); in the middle of the corridor the rattle is an octave up and in the middle of the head, and walking to a wall it drops, leans to that wall and changes colour. Generated by")
        assert "From v13" in doc["about"]
    if bird_span():
        b0, b1 = bird_span()
        PATCHES["sr-bird"] = {"about": "Standing Room's bird (chirper-zero, 27 Nov, v15): a very short high sine, two of them to a call (E8 then A8, 30 ms apart). Where it is comes from the track's orbit effect, not from the patch.",
                              "play": {"vel_sens": 0.5, "gate": 1},
                              "synth": {"layers": ["sine", "sine ratio=2 level=-18dB"], "amp": {"a": "1ms", "d": "28ms", "s": 0, "r": "10ms", "curve": 3}}}
        doc["tracks"].append({"name": "bird", "patch": "sr-bird", "gain": BIRD_GAIN, "pan": 0.0, "sends": {"air": BIRD_AIR},
                              "fx": [{"type": "orbit", "path": "circle", "radius": BIRD_RADIUS, "distance": BIRD_AHEAD, "rate": round(bird_rate(), 6), "phase": BIRD_PHASE, "doppler": 1.0, "level": abs(BIRD_RADIUS - BIRD_AHEAD)}],
                              "notes": bird_notes()})
        doc["about"] = doc["about"].replace(" Generated by", f" From v15 a bird flies round in the hangar while the drum rests (bars {b0 + 1} to {b1}): a circle of {BIRD_RADIUS:g} m whose centre is {BIRD_AHEAD:g} m in front of you, once round every {BIRD_LAP} bars, calling every {BIRD_EVERY} sixteenths; where it is heard, how loud and how sharp or flat is worked out from the circle by the engine's orbit effect. Generated by")
        assert "From v15" in doc["about"]
    if ball_notes():
        PATCHES["sr-ball"] = {"about": "Standing Room's ball (chirper-zero, 27 Nov, v14): a small hard ball on a hard floor: a sine on A6 and a breath of noise with everything under 700 Hz taken off, gone in 22 ms. Its loudness goes as the square of the velocity, so a bounce that keeps 0.891 of the speed is written 0.891 ** 0.5 of the velocity.",
                              "play": {"vel_sens": 1, "gate": 1},
                              "synth": {"layers": ["sine", "white level=-8dB"], "filters": ["hp cutoff=700"], "amp": {"a": "0.1ms", "d": "22ms", "s": 0, "r": "8ms", "curve": 3}}}
        doc["tracks"].append({"name": "ball", "patch": "sr-ball", "gain": BALL_GAIN, "pan": {"value": 0, "mod": [{"src": "auto.roll", "amount": 1}]},
                              "auto": {"roll": {"points": ball_lane(), "curve": 0}}, "notes": ball_notes()})
        doc["about"] = doc["about"].replace(" Generated by", f" From v14 a small hard ball is let fall {len(BALL_RESTS)} times and comes to rest exactly on a bar line, at every door but the last and at the turn of a row in the long rooms: each flight is 0.891 of the one before, so the bounces come twice as fast every six and infinitely many fit into seven and a quarter beats; every room answers the same ball with its own echoes. Generated by")
        assert "From v14" in doc["about"]
    if TRIM:
        ck = PATCHES["sr-click"]
        PATCHES["sr-click-t"] = {"about": ck["about"] + " From v13 with its own note (880 Hz) turned down and its top turned up on the lane `trim` (0 the click as it was, 1 the whole repair): the song had 10 dB more than the rest of the record at 880 Hz and 12 dB less at 15 kHz, and the click owns both.",
                                 "play": dict(ck["play"]), "synth": {**ck["synth"], "filters": list(ck["synth"]["filters"]) + [{"kind": "peak", "cutoff": f, "q": q, "gain": {"value": "0dB", "mod": [{"src": "auto.trim", "amount": g}]}} for f, g, q in TRIM_CUTS]}}
        for t in doc["tracks"]:
            if t["name"] == "click":
                t["patch"] = "sr-click-t"
                t["auto"] = {**t.get("auto", {}), "trim": {"points": [[f"{x:g}b", y] for x, y in ((0, 0), (TRIM_IN[0] * BEATS, 0), (TRIM_IN[1] * BEATS, 1), (TRIM_OUT[0] * BEATS, 1), (TRIM_OUT[1] * BEATS, 0), (TOTAL, 0))], "curve": 0}}
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
    if FLY:
        beat = 60 / BPM
        for (n, heard, bar), (_, v, T, ratio, f0, f_in, f_out, tc, rate, ph) in zip(FLY_PASSES, fly_facts()):
            PATCHES[f"sr-fly-{n}"] = {"about": f"Standing Room's passer at 1/{n} of the speed of sound (chirper-zero, 27 Nov, v16): a plain held tone with a little of its octave, sung {ratio:.6f} of the written note ({f0:.1f} Hz for {heard}); moving at {v:.1f} m/s it is heard on the written note coming ({f_in:.1f} Hz) and {(n + 1)}/{(n - 1)} below it going ({f_out:.1f} Hz). Where it is comes from the track's orbit effect.",
                                      "play": {"vel_sens": 0, "gate": 1},
                                      "synth": {"layers": [f"sine phase=0 ratio={ratio:.6f}", f"sine phase=0 ratio={2 * ratio:.6f} level=-14dB"], "amp": {"a": "3ms", "d": "0s", "s": 1, "r": "3ms"}}}
            doc["tracks"].append({"name": f"fly-{n}", "patch": f"sr-fly-{n}", "gain": FLY_GAIN, "pan": 0.0,
                                  "fx": [{"type": "orbit", "path": "line", "radius": FLY_RADIUS, "distance": FLY_DIST, "rate": round(rate, 8), "phase": round(ph, 8), "doppler": 1.0, "level": FLY_DIST}],
                                  "notes": [{"at": round((tc - T / 2) / beat, 5), "len": round(T / beat, 5), "pitch": heard, "vel": 0.8}]})
        doc["about"] = doc["about"].replace(" Generated by", " From v16 three things go by in the hangar, left to right, on the bar lines 87, 88 and 89, at a seventh, a fifth and a third of the speed of sound: each is heard a fourth, a fifth and an octave higher coming than going (A7 to E7, E7 to A6, A6 to A5), and none of them sings either note. Generated by")
        assert "From v16" in doc["about"]
    if NEXTROOM:
        nx_b0, nx_b1 = nextroom_span(); nx_most = -nextroom_db(nx_b0); nx_hz = [NEXTROOM_MAINS * nx_k for nx_k in NEXTROOM_PARTS]; nx_db = [-NEXTROOM_WALL * math.log2(nx_f / nx_hz[0]) for nx_f in nx_hz]
        PATCHES["sr-next"] = {"about": f"Standing Room's building across the square (chirper-zero, 27 Nov, v17): a building's hum heard through its wall: plain held tones at {' and '.join(f'{nx_f:g}' for nx_f in nx_hz)} Hz ({' and '.join(str(nx_k) for nx_k in NEXTROOM_PARTS)} times mains of {NEXTROOM_MAINS:g}), each {NEXTROOM_WALL:g} dB quieter for every octave it is above the lowest. Written on {NEXTROOM_NOTE}, which does not sound.",
                              "play": {"vel_sens": 0, "gate": 1},
                              "synth": {"layers": [f"sine phase=0 ratio={nx_f / hz(NEXTROOM_NOTE):.6f} level={nx_d:.2f}dB" for nx_f, nx_d in zip(nx_hz, nx_db)], "amp": {"a": "1s", "d": "0s", "s": 1, "r": NEXTROOM_RELEASE}}}
        doc["tracks"].append({"name": "next", "patch": "sr-next", "gain": NEXTROOM_GAIN, "pan": 0.0,
                              "fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.near", "amount": round(-nx_most, 3)}]}}],
                              "auto": {"near": {"points": nextroom_lane()}},
                              "notes": [{"at": nx_b0 * BEATS, "len": (nx_b1 - nx_b0) * BEATS, "pitch": NEXTROOM_NOTE, "vel": 0.8}]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v17, as you walk away across the square, the building you are walking to is heard: its hum through its wall, {' and '.join(f'{nx_f:g}' for nx_f in nx_hz)} Hz, in no key, growing as you come ({nx_most:.1f} dB over the sixteen bars). Generated by")
        assert "From v17" in doc["about"]
    if WHISTLE and whistle_pipes():
        doc["tracks"].append({"name": "whistle", "patch": "sr-step", "gain": WHISTLE_GAIN, "pan": 0.0, "notes": whistle_notes()})     # dry: the pipe is the room
        doc["about"] = doc["about"].replace(" Generated by", f" From v18 the pipes are {whistle_far() / 2:.0f} m long as well, and the click comes back from the far end on each of the three beats after it as a falling whistle, a slower fall each time (a culvert whistler: the clicks that glanced off the walls have farther to come), down towards the octave of the note that pipe sings. Generated by")
        assert "From v18" in doc["about"]
    if SONIC:
        so_bell = ["sine", "sine ratio=2 level=-9dB", "sine ratio=3 level=-15dB"]; so_pitch = {"value": 0, "mod": [{"src": "auto.dop", "amount": 1}]}
        PATCHES["sr-sonic-back"] = {"about": f"Standing Room's bell on the thing that goes by faster than sound, heard BACKWARDS (chirper-zero, 27 Nov, v19): the bell of the thing that goes past (a sine with its octave and twelfth), swelling for {SONIC_RING * 1000:g} ms to its stroke and stopping there: what it struck before it passed. Its pitch is given by where it was (auto.dop, semitones). It is in no room.",
                                    "play": {"vel_sens": 0.5, "gate": 1}, "synth": {"layers": so_bell, "pitch": so_pitch, "amp": {"a": f"{SONIC_RING * 1000:g}ms", "d": "0ms", "s": 1, "r": "2ms", "curve": 3}}}
        PATCHES["sr-sonic-on"] = {"about": f"Standing Room's bell on the thing that goes by faster than sound, when it has gone (chirper-zero, 27 Nov, v19): the same bell, ringing {SONIC_RING * 3000:g} ms: three times as long, as it is heard three times as slow and a twelfth lower (auto.dop, semitones). It is in no room.",
                                  "play": {"vel_sens": 0.5}, "synth": {"layers": so_bell, "pitch": so_pitch, "amp": {"a": "1.5ms", "d": f"{SONIC_RING * 3000:g}ms", "s": 0, "r": "120ms", "curve": 3}}}
        so_ring = SONIC_RING * BPM / 60
        for so_nm, so_back in (("sonic-back", True), ("sonic-on", False)):
            so_notes, so_lanes = [], [[["0b", 0.0]], [["0b", 0.0]]]
            for so_bar in SONIC_AT:
                for te, p, r, ta, fast, lev, side in sorted(sonic_strokes(), key=lambda q: q[3]):
                    if (fast < 0) != so_back:
                        continue
                    so_len = round(so_ring / abs(fast), 5); so_at = round(so_bar * BEATS + ta * BPM / 60 - (so_len if so_back else 0), 5)      # a bell heard backwards ends on its stroke; one heard slower rings longer
                    so_notes.append({"at": so_at, "len": so_len, "pitch": p, "vel": round(0.9 * lev, 4)})
                    for so_i, so_v in ((0, round(12 * math.log2(abs(fast)), 3)), (1, round(side, 3))):
                        so_lanes[so_i] += [[f"{so_at - 0.02:.5f}b", so_v], [f"{so_at + so_len + 0.05:.5f}b", so_v]]
            doc["tracks"].append({"name": so_nm, "patch": "sr-sonic-back" if so_back else "sr-sonic-on", "gain": SONIC_GAIN, "pan": {"value": 0, "mod": [{"src": "auto.side", "amount": SONIC_PAN}]}, "notes": so_notes,
                                  "auto": {"dop": {"points": so_lanes[0], "curve": 0}, "side": {"points": so_lanes[1], "curve": 0}}})
        doc["about"] = doc["about"].replace(" Generated by", f" From v19 a fourth thing goes by in the hangar, at {SONIC_MACH:g} times the speed of sound, striking the pipes' scale upwards: it is not heard coming; when it has passed, its coming is heard backwards from the left (the scale running down, each bell swelling to its stroke) and its going a third as fast and a twelfth lower from the right. Generated by")
        assert "From v19" in doc["about"]
    if FOUR and four_rows():
        PATCHES["sr-corner"] = {"about": "Standing Room's click come back from a corner (chirper-zero, 27 Nov, v20): the click (the machine's rim and a breath of white noise, above 500 Hz) as a wall leaves it: no lift at the top, its own note (880 Hz) 5 dB down as the click's repair has it, and as loud as its velocity (an echo's level is written in the velocity).",
                                "play": {"vel_sens": 0.5},
                                "synth": {"layers": [{"type": "machine", "machine": {"part": "rim", "decay": "45ms"}}, "white level=-3dB"], "filters": ["hp cutoff=500", {"kind": "peak", "cutoff": 880, "q": 3, "gain": "-5dB"}], "amp": {"a": "0.1ms", "d": "40ms", "s": 0, "r": "20ms", "curve": 4}}}
        fo_notes = four_notes()
        for fo_i in range(FOUR_PANS):
            if fo_notes[fo_i]:
                doc["tracks"].append({"name": f"corner-{fo_i + 1}", "patch": "sr-corner", "gain": FOUR_GAIN, "pan": four_pan(fo_i),
                                      "fx": [{"type": "eq", "bands": ["hp cutoff=250", "lp cutoff=9000"]}], "notes": fo_notes[fo_i]})     # the walls' own filter
        fo_rows = four_rows()
        doc["about"] = doc["about"].replace(" Generated by", f" From v20 the hangar has its other two walls in its last two rows (bars {fo_rows[0][0] + 1} to {fo_rows[-1][0] + ROW}), in front and behind and as far apart as the side ones: an echo that has met both pairs comes back from a corner, the square root of (across squared plus deep squared) sixteenths late, which is almost never on a sixteenth: 8.49, 13.42, 16.97 and 18.97 with the click in the middle, and when it steps to 7 + 5 one corner lands on the grid, because 5 and 12 make 13. Generated by")
        assert "From v20" in doc["about"]
    if dome_row() is not None:
        if "sr-corner" not in PATCHES:
            raise SystemExit("the dome's echo is the click as a wall leaves it (sr-corner): C11T3_FOUR must be on")
        do_notes = dome_notes()
        for do_i, (do_turn, do_pan) in enumerate(dome_parts()):
            doc["tracks"].append({"name": f"dome-{do_i + 1}", "patch": "sr-corner", "gain": DOME_GAIN, "pan": do_pan,
                                  "fx": [{"type": "eq", "bands": ["hp cutoff=250", "lp cutoff=9000"]}], "notes": do_notes[do_i]})     # the walls' own filter
        doc["about"] = doc["about"].replace(" Generated by", f" From v21 the hall has a dome, the first wall in the song that is not flat, and you walk under it in the row before the people come in (bars {dome_row() + 1} to {dome_row() + ROW}). A dome like this one has a focus: from the click up to any part of it and down to that one place is the same way round, {DOME_PATH} sixteenths. Anywhere else the {DOME_PARTS} parts of it answer one after another, the ones ahead of you first and the ones behind last: a rattle {dome_late(0, 180) - dome_late(0, 0):.1f} sixteenths long in the row's first bar, shorter with every bar as you walk in; on the focus (the last {ROW - DOME_WALK[1]} bars) they arrive together, one stroke on step {CLICK_STEP + DOME_PATH} made of {DOME_PARTS}, and no part of it was played any louder. Generated by")
        assert "From v21" in doc["about"]
    if duct_row() is not None:
        du = duct_echoes(); du_top = 12 * math.log2(DUCT_TOP)
        PATCHES["sr-duct"] = {"about": f"Standing Room's air duct (chirper-zero, 27 Nov, v22): what comes back from a duct {SOUND / (2 * duct_hz()):.2f} m across: plain tones on its {len(DUCT_MODES)} lowest ways across ({', '.join(f'{m * duct_hz():.0f}' for m, _ in DUCT_MODES)} Hz), dying in {DUCT_RING}, whose pitch rides the lane `pew` (semitones over the duct's own note): each echo starts {DUCT_TOP:g} times too high and comes down to its note, quickly from a short duct and slowly from a long one.",
                              "play": {"vel_sens": 0.5, "gate": 1},
                              "synth": {"layers": [f"sine phase=0 ratio={m:g} level={lv:g}dB" for m, lv in DUCT_MODES], "pitch": {"value": 0, "mod": [{"src": "auto.pew", "amount": 1}]},
                                        "amp": {"a": "2ms", "d": DUCT_RING, "s": 0, "r": "30ms", "curve": 3}}}
        du_pts = [["0b", round(du_top, 3)]]
        for du_at, du_len, du_back, du_p in du:
            du_pts += [[f"{round(du_at - 0.03, 5):g}b", round(du_top, 3)]] + [[f"{round(t, 5):g}b", round(v, 3)] for t, v in du_p]
        doc["tracks"].append({"name": "duct", "patch": "sr-duct", "gain": DUCT_GAIN, "pan": DUCT_PAN, "auto": {"pew": {"points": du_pts, "curve": 0}},
                              "notes": [{"at": round(du_at, 5), "len": round(du_len, 5), "pitch": DUCT_NOTE, "vel": DUCT_VEL} for du_at, du_len, _, _ in du]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v22 the hall has an air duct, {SOUND / (2 * duct_hz()):.2f} m across, to your left in the row before the dome (bars {duct_row() + 1} to {duct_row() + ROW}). A wall gives a click back as a click. A duct does not: a sound that crosses it as it goes along it goes along more slowly, and the nearer a note is to the duct's own ({duct_hz():.0f} Hz, half a wave across) the later it is back: so each click comes back as a note that starts high and falls to {DUCT_NOTE}, and never quite arrives. The duct is {', '.join(str(p) for p in sorted(set(DUCT_BACK)))} sixteenths there and back: from the short one the fall is quick, from the long one slow: how far it has been is how slowly it comes down. Generated by")
        assert "From v22" in doc["about"]
    if rail_row() is not None:
        rl = rail_knocks(); rl_gap = [(st - ai) * 60 / BPM * 1000 for _, _, _, st, ai, _, _ in rl]
        PATCHES["sr-rail"] = {"about": f"Standing Room's handrail (chirper-zero, 27 Nov, v23): what the STEEL brings of a knock on a long rail: its ring, a free bar's first {len(RAIL_PARTS)} ways of ringing ({', '.join(f'{r * hz(RAIL_NOTE):.0f}' for r, _ in RAIL_PARTS)} Hz), {RAIL_RING}. It comes at {RAIL_SPEED:g} m/s, before the air's.",
                              "play": {"vel_sens": 0.5}, "synth": {"layers": [f"sine phase=0 ratio={r:g} level={lv:g}dB" for r, lv in RAIL_PARTS], "amp": {"a": "0.3ms", "d": RAIL_RING, "s": 0, "r": "20ms", "curve": 3}}}
        PATCHES["sr-knock"] = {"about": f"Standing Room's handrail (chirper-zero, 27 Nov, v23): what the AIR brings of the same knock, duller and later ({', '.join(f'{r * hz(AIR_NOTE):.0f}' for r, _ in AIR_PARTS)} Hz), {AIR_RING}. It comes at {SOUND:g} m/s, after the steel's.",
                               "play": {"vel_sens": 0.5}, "synth": {"layers": [f"sine phase=0 ratio={r:g} level={lv:g}dB" for r, lv in AIR_PARTS], "amp": {"a": "1ms", "d": AIR_RING, "s": 0, "r": "20ms", "curve": 3}}}
        doc["tracks"].append({"name": "rail", "patch": "sr-rail", "gain": RAIL_GAIN, "pan": RAIL_PAN,
                              "notes": [{"at": round(st, 5), "len": 0.2, "pitch": RAIL_NOTE, "vel": round(RAIL_VEL * 10 ** (sdb / 20), 4)} for _, _, _, st, _, sdb, _ in rl]})
        doc["tracks"].append({"name": "knock", "patch": "sr-knock", "gain": AIR_GAIN, "pan": AIR_PAN,
                              "notes": [{"at": round(ai, 5), "len": 0.2, "pitch": AIR_NOTE, "vel": round(RAIL_VEL * 10 ** (adb / 20), 4)} for _, _, _, _, ai, _, adb in rl]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v23 the corridor has a handrail and your left ear is on it (bars {rail_row() + 1} to {rail_row() + ROW}). Somebody knocks on the rail further and further down the corridor, {rl[0][1]:.1f} m more each time, out to {max(m for _, m, *_ in rl):.0f} m and back. Every knock is heard twice: first through the steel (its ring, on the left: sound goes {RAIL_SPEED:g} m/s in steel), then through the air (an octave duller, on the right: {SOUND:g} m/s). The air's knocks are on the grid; the rings come {-max(rl_gap):.0f} ms before them from the nearest mark and {-min(rl_gap):.0f} ms before from the furthest: the gap is a ruler, {-max(rl_gap) / rl[0][1]:.2f} ms a metre (Biot measured the speed of sound in iron this way in 1808). Generated by")
        assert "From v23" in doc["about"]
    if gal_row() is not None:
        ga = gal_arrivals(); ga_lap = GAL_LAP * STEP * 60 / BPM * SOUND
        PATCHES["sr-whisper"] = {"about": f"Standing Room's whisper (chirper-zero, 27 Nov, v24): {GAL_LEN * 60 / BPM * 1000:.0f} ms of hiss, {GAL_BAND[0]:g} to {GAL_BAND[1]:g} Hz, from the engine's chip noise with no chip's clock: a shift register begun from the same state at every note, so every arrival of it is THE SAME BURST, sample for sample, on every seed: one whisper, coming round the gallery again.",
                                 "play": {"vel_sens": 0.5, "gate": 1}, "synth": {"layers": [{"type": "chip", "chip": {"kind": "noise", "clock": 0}}],
                                 "filters": [f"hp cutoff={GAL_BAND[0]:g}"] + [f"lp cutoff={GAL_BAND[1]:g}"] * 3, "amp": {"a": "2ms", "d": "0s", "s": 1, "r": "20ms"}}}
        for ga_nm, ga_side in (("gal-l", -1), ("gal-r", 1)):
            doc["tracks"].append({"name": ga_nm, "patch": "sr-whisper", "gain": GAL_GAIN, "pan": ga_side * GAL_PAN,
                                  "notes": [{"at": round(at, 5), "len": GAL_LEN, "pitch": GAL_NOTE, "vel": round(GAL_VEL * 10 ** (db / 20), 4)} for _, sd, _, at, _, db in ga if sd == ga_side]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v24 the hall has a whispering gallery (bars {gal_row() + 1} to {gal_row() + ROW}): a round wall {ga_lap / math.pi:.0f} m across, {ga_lap:.1f} m round: {GAL_LAP} sixteenths at the speed of sound. Every {GAL_EVERY} bars somebody a third of the way round whispers at the wall. A whisper at a round wall does not cross the room: it clings to the wall and goes round it, both ways: it reaches you from the left after a third of a lap and from the right after two thirds, and each comes round again every lap, {GAL_TIMES} times: left, right, nothing; left, right, nothing: three against the bar's four. It is the same burst of hiss every time, falling as the square root of the distance and {GAL_LOSS:g} dB a lap: {-min(db for _, _, _, _, _, db in ga):.0f} dB by the last. Generated by")
        assert "From v24" in doc["about"]
    if BEND:
        bd_bass = next(t for t in doc["tracks"] if t["name"] == "bass")
        bd_cell = [n for n in bd_bass["notes"] if BEND_BARS[1] * BEATS <= n["at"] < (BEND_BARS[1] + 2) * BEATS]      # the bass's own first two bars: what it is playing round the corner
        assert len(bd_cell) == 8 and not [n for n in bd_bass["notes"] if n["at"] < BEND_BARS[1] * BEATS]
        bd_notes = [dict(n, at=n["at"] - (BEND_BARS[1] - bar) * BEATS) for bar in range(BEND_BARS[0], BEND_BARS[1], 2) for n in bd_cell]
        bd_pump = [fx for fx in bd_bass.get("fx", []) if fx.get("type") == "pump"]
        bd_gain = float(BEND_GAIN[:-2]) if BEND_GAIN else float(bd_bass["gain"][:-2]) + BEND_TRIM + BEND_LIFT
        PATCHES["sr-bend"] = {"about": "Standing Room's bass round the corner (chirper-zero, 27 Nov, v25): one plain tone; six tracks of it are the bass's first six partials (the track's lane auto.h says which, in semitones over the note), each with its own shadow.",
                              "play": {"vel_sens": 0, "gate": 1}, "synth": {"layers": ["sine phase=0"], "pitch": {"value": 0, "mod": [{"src": "auto.h", "amount": 1}]}, "amp": {"a": "5ms", "d": "0s", "s": 1, "r": "30ms"}}}
        for bd_h, bd_part in enumerate(BEND_PARTS, start=1):
            bd_pts = [[f"{n['at']:g}b", round(bend_shadow(hz(n["pitch"]) * bd_h, bend_way(n["at"])) + bend_spread(bend_way(n["at"])), 2)] for n in bd_notes]
            doc["tracks"].append({"name": f"bend-{bd_h}", "patch": "sr-bend", "gain": f"{bd_gain + bd_part:.1f}dB", "pan": 0.0,
                                  "fx": bd_pump + [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.shadow", "amount": 1}]}}],
                                  "auto": {"h": {"points": [["0b", round(12 * math.log2(bd_h), 4)], [f"{BARS * BEATS}b", round(12 * math.log2(bd_h), 4)]], "curve": 0},
                                           "shadow": {"points": [["0b", bd_pts[0][1]]] + bd_pts + [[f"{BARS * BEATS}b", bd_pts[-1][1]]], "curve": 0}},
                                  "notes": [{"at": n["at"], "len": n["len"], "pitch": n["pitch"], "vel": n["vel"]} for n in bd_notes]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v25 the bass is heard round a corner before it is met (bars {BEND_BARS[0] + 1} to {BEND_BARS[1]}): it is {BEND_SIDE:g} m down a side passage and the corridor begins {BEND_FROM:g} m short of the corner. Sound bends into a shadow, low notes most (Maekawa): each of the bass's first six partials loses 10 log (3 + 20 N) dB, N the half waves by which the way round is longer than the way through: {-bend_shadow(hz('D2'), BEND_FROM):.1f} dB of its first partial and {-bend_shadow(hz('D2') * 4, BEND_FROM):.1f} of its fourth at the start, {-bend_shadow(hz('D2'), 0):.1f} dB of every one at the corner itself; and the longer way takes {-bend_spread(BEND_FROM):.1f} dB more at the start. At bar {BEND_BARS[1] + 1} the corner is turned. Generated by")
        assert "From v25" in doc["about"]
    if slam_bar() is not None:
        sl_at, sl_b = slam_bar() * BEATS, BPM / 60.0             # the beat it is on; beats a second
        for sl_k, (sl_lo, sl_hi, sl_rt, sl_trim) in enumerate(slam_bands()):
            sl_name = f"sr-slam-{sl_k + 1}"
            PATCHES[sl_name] = {"about": f"Standing Room's hangar door, band {sl_k + 1} of {len(SLAM_AIR)} (chirper-zero, 27 Nov, v26): plain noise from {sl_lo:g} to {sl_hi:g} Hz, held; its loudness is its track's `gain` on `auto.tail` (dB) and its place the track's pan on `auto.wide`. In the hangar this band takes {sl_rt:.2f} s to fall 60 dB.",
                                "play": {"vel_sens": 0, "gate": 1}, "synth": {"layers": [{"type": "noise"}], "filters": [{"kind": "hp", "cutoff": sl_lo, "q": sl_q} for sl_q in SLAM_EDGE] + [{"kind": "lp", "cutoff": sl_hi, "q": sl_q} for sl_q in SLAM_EDGE], "amp": {"a": "1ms", "d": "0s", "s": 1, "r": "20ms"}}}
            sl_end = sl_rt * SLAM_FLOOR / -60                    # seconds until it is gone
            sl_tail = [["0b", SLAM_FLOOR], [f"{sl_at - 0.01:g}b", SLAM_FLOOR], [f"{sl_at:g}b", round(slam_direct() - SLAM_PAN, 3)], [f"{sl_at + SLAM_DIRECT * sl_b:.5f}b", round(slam_direct() - SLAM_PAN, 3)],
                       [f"{sl_at + (SLAM_DIRECT + SLAM_TURN) * sl_b:.5f}b", round(-60 * (SLAM_DIRECT + SLAM_TURN) / sl_rt, 3)], [f"{sl_at + sl_end * sl_b:.5f}b", SLAM_FLOOR]]
            sl_wide = [["0b", 0.0], [f"{sl_at + SLAM_DIRECT * sl_b:.5f}b", 0.0], [f"{sl_at + (SLAM_DIRECT + SLAM_TURN) * sl_b:.5f}b", 1.0]]
            for sl_ear, sl_side in (("l", -1), ("r", 1)):
                doc["tracks"].append({"name": f"slam-{sl_k + 1}-{sl_ear}", "patch": sl_name, "gain": f"{float(SLAM_GAIN[:-2]) + sl_trim:.2f}dB",
                                      "pan": {"value": 0, "mod": [{"src": "auto.wide", "amount": sl_side * SLAM_WIDE}]},
                                      "auto": {"tail": {"points": sl_tail, "curve": 0}, "wide": {"points": sl_wide, "curve": 0}},
                                      "fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.tail", "amount": 1}]}}],
                                      "notes": [{"at": sl_at, "len": round(min(sl_end * sl_b, ROW * BEATS - 0.25), 4), "pitch": "A3", "vel": 0.8}]})
        sl_rts = [b[2] for b in slam_bands()]
        doc["about"] = doc["about"].replace(" Generated by", f" From v26 the hangar's door shuts behind you on the first beat of bar {slam_bar() + 1}, where the drum and the bass rest, and the tail is left to die in the empty row. The hangar is {SLAM_HALL[0]:g} m by {SLAM_HALL[1]:g} m and {SLAM_HALL[2]:g} m high; its walls take {SLAM_WALLS:g} of the sound at every meeting, at every pitch alike; the air takes more the higher the sound ({SLAM_AIR[0]:g} dB a kilometre in the bottom band, {SLAM_AIR[-1]:g} in the top). By Sabine's rule with the air's term the bottom band ({SLAM_EDGES[0]:g} to {SLAM_EDGES[1]:g} Hz) takes {sl_rts[0]:.1f} s to fall 60 dB and the top ({SLAM_EDGES[-2]:g} to {SLAM_EDGES[-1]:g} Hz) {sl_rts[-1]:.1f} s: the tail goes dark as it dies. The slam itself is in the middle and {slam_direct():.1f} dB over the tail it starts (you are {SLAM_AWAY:g} m from the door); the tail is wide. Generated by")
        assert "From v26" in doc["about"]
    if HUSH and slam_bar() is not None:
        hu_a, hu_b = slam_bar() * BEATS, (slam_bar() + HUSH_BARS) * BEATS
        hu_gone = {}
        for hu_t in doc["tracks"]:
            if not hu_t["name"].startswith(HUSH_KEEP):
                hu_n = sum(1 for n in hu_t["notes"] if hu_a <= n["at"] < hu_b)
                if hu_n:
                    hu_gone[hu_t["name"]] = hu_n
                    hu_t["notes"] = [n for n in hu_t["notes"] if not hu_a <= n["at"] < hu_b]
        assert hu_gone and all(not (n["at"] < hu_a < n["at"] + n["len"]) for hu_t in doc["tracks"] if not hu_t["name"].startswith(HUSH_KEEP) for n in hu_t["notes"])      # and nothing rings in from before
        hu_doors = []                                           # the hangar's echo (its buses' doors) opened at the door, coming up over the row's first bars: it let in the echoes of the last click and tock BEFORE the door, and they were read in the hush (every fourth sixteenth, -30 to -38 dBFS at 1400 to 2800 Hz, over the tail from its second second). The echo now opens when the hush ends, whole
        for hu_name, hu_bus in doc["buses"].items():
            hu_p = (hu_bus.get("auto") or {}).get("door", {}).get("points")
            hu_i = next((i for i, p in enumerate(hu_p or []) if p[0] == f"{hu_a:g}b" and p[1] > -90 and i and hu_p[i - 1][1] == -90), None)
            if hu_i is not None:
                assert hu_p[hu_i + 1][0] == f"{hu_b:g}b", (hu_name, hu_p[hu_i + 1])
                hu_bus["auto"] = {**hu_bus["auto"], "door": {**hu_bus["auto"]["door"], "points": hu_p[:hu_i - 1] + [[f"{hu_b - (hu_a - float(hu_p[hu_i - 1][0][:-1])):g}b", -90]] + hu_p[hu_i + 1:]}}
                hu_doors.append(hu_name)
        assert hu_doors, "no echo opens at the door"
        doc["about"] = doc["about"].replace(" Generated by", f" From v27 there is a hush after the door: for {HUSH_BARS} bars (bars {slam_bar() + 1} and {slam_bar() + HUSH_BARS}) " + ", ".join(f"the {k} ({v})" for k, v in hu_gone.items()) + f" wait, the hangar's echo opens only when they come back (so that the last click before the door is not heard going round), and there is only the door's tail: you stand still and hear how big the place is and what its air does: in those {HUSH_BARS * BEATS * 60 / BPM:.1f} s the tail's top band dies away and its bottom is still there. Generated by")
        assert "From v27" in doc["about"]
    if foot_bar() is not None:
        ft_a, ft_b = foot_bar() * BEATS, (foot_bar() + FOOT_BARS) * BEATS
        ft_gone = {}
        for ft_t in doc["tracks"]:
            if ft_t["name"] in FOOT_WAIT:
                assert not any(n["at"] < ft_a < n["at"] + n["len"] for n in ft_t["notes"])      # nothing of theirs rings in from before
                ft_gone[ft_t["name"]] = sum(1 for n in ft_t["notes"] if ft_a <= n["at"] < ft_b)
                ft_t["notes"] = [n for n in ft_t["notes"] if not ft_a <= n["at"] < ft_b]
        assert set(ft_gone) == set(FOOT_WAIT) and all(ft_gone.values())
        ft_clap = min(n["at"] for t in doc["tracks"] if t["name"].startswith("clap-at") for n in t["notes"])
        assert ft_b <= ft_clap < ft_b + BEATS, (ft_clap, ft_b)          # the first clap on the stairs is in the bar the drum comes back
        doc["about"] = doc["about"].replace(" Generated by", f" From v28 you stop at the foot of the stairs: for the stairwell's first {FOOT_BARS} bars (bars {foot_bar() + 1} to {foot_bar() + FOOT_BARS}) " + " and ".join(f"the {k} ({v} notes)" for k, v in ft_gone.items()) + f" wait, and there is the click, the tock and what the stairwell gives back of them: you hear the place before you climb. The drum comes back in bar {foot_bar() + FOOT_BARS + 1}, the bar of the first clap on the stairs. Generated by")
        assert "From v28" in doc["about"]
    if began_row() is not None:
        bg = began_tones()
        PATCHES["sr-began"] = {"about": f"Standing Room's tone, its start (chirper-zero, 27 Nov, v29): a plain sine that starts at once, is whole for {1000 * BEGAN_HOLD:g} ms and falls to nothing in the next {1000 * BEGAN_HAND:g} ms, in a straight line. With `sr-went` on the same note at the same instant it is one unbroken tone.",
                               "play": {"vel_sens": 0, "gate": 1}, "synth": {"layers": ["sine phase=0"], "amp": {"a": "0.5ms", "h": f"{1000 * BEGAN_HOLD:g}ms", "d": f"{1000 * BEGAN_HAND:g}ms", "s": 0, "r": "5ms", "curve": 0}}}
        PATCHES["sr-went"] = {"about": f"Standing Room's tone, all the rest of it (chirper-zero, 27 Nov, v29): the same sine, silent for the start's first {1000 * BEGAN_HOLD:g} ms, then rising in {1000 * BEGAN_HAND:g} ms in a straight line, held, and going out in {1000 * BEGAN_FADE:g} ms.",
                              "play": {"vel_sens": 0, "gate": 1}, "synth": {"layers": ["sine phase=0"], "amp": {"delay": f"{1000 * BEGAN_HOLD + 0.5:g}ms", "a": f"{1000 * BEGAN_HAND:g}ms", "d": "0s", "s": 1, "r": f"{1000 * BEGAN_FADE:g}ms", "curve": 0}}}
        doc["tracks"].append({"name": "began-l", "patch": "sr-began", "gain": BEGAN_GAIN, "pan": -BEGAN_PAN, "sends": {"air": BEGAN_AIR},
                              "notes": [{"at": t, "len": 0.25, "pitch": p, "vel": 0.8} for t, p, st in bg if st]})
        doc["tracks"].append({"name": "went-r", "patch": "sr-went", "gain": BEGAN_GAIN, "pan": BEGAN_PAN, "sends": {"air": BEGAN_AIR},
                              "notes": [{"at": t, "len": BEGAN_LEN, "pitch": p, "vel": 0.8} for t, p, st in bg]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v29 a tone stays where it began (bars {began_row() + 1} to {began_row() + BEGAN_IN[2] * ROW}, the hangar's last {BEGAN_IN[2]} rows): every {BEGAN_EVERY} bars a plain tone, a bar long, each of {' '.join(BEGAN_TUNE)} twice. The first time it starts sharply on the left, is all there for {1000 * BEGAN_HOLD:g} ms, and in the next {1000 * BEGAN_HAND:g} ms is handed to the right, where all the rest of it sounds; the two together are one unbroken tone. The second time it is the same without its start. The hangar's air rings with both. In a room that rings a plain tone is heard where it began (Franssen): the first on the left, though after {1000 * (BEGAN_HOLD + BEGAN_HAND):g} ms the two are the same. Generated by")
        assert "From v29" in doc["about"]
    if close_row() is not None:
        cl = close_trains()
        PATCHES["sr-close"] = {"about": "Standing Room's echo between two walls (chirper-zero, 27 Nov, v30): one soft low thud, a plain tone and its octave, gone in 12 ms, with nothing over 600 Hz; how hard it is struck is how loud it is. A train of them is a rattle or a note, by how close they come.",
                               "play": {"vel_sens": 1}, "synth": {"layers": ["sine phase=0", "sine phase=0 ratio=2"], "filters": ["lp cutoff=600"], "amp": {"a": "0.2ms", "d": "12ms", "s": 0, "r": "5ms"}}}
        doc["tracks"].append({"name": "close", "patch": "sr-close", "gain": CLOSE_GAIN, "pan": 0.0, "notes": [{"at": t, "len": CLOSE_LEN, "pitch": CLOSE_NOTE, "vel": round(10 ** (d / 40), 5)} for _, _, _, _, es in cl for t, d in es]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v30 the walls close in (bars {close_row() + 1} to {close_row() + ROW}, the corridor's last row): a knock twice a bar comes back between two walls, once for every time across and back; bar by bar the walls are {', '.join(f'{SOUND * CLOSE_NEAR * 2 ** st / CLOSE_RATE / 2:.2f}' for st in CLOSE_STEPS)} m apart: the echoes come {', '.join(f'{CLOSE_RATE / (CLOSE_NEAR * 2 ** st):.1f}' for st in CLOSE_STEPS)} times a second: far walls are echoes to count, near walls a note ({sum(len(es) for _, _, _, _, es in cl)} thuds in {len(cl)} trains). Generated by")
        assert "From v30" in doc["about"]
    if drop_row() is not None:
        dr = drop_falls(); dr_g = float(DROP_GAIN.replace("dB", ""))
        PATCHES["sr-thud"] = {"about": "Standing Room's thud at the bottom of the stairwell (chirper-zero, 28 Nov, v31): a low plain tone and its octave struck together and gone in a tenth of a second, nothing over 600 Hz; how hard it is struck is how loud it is.",
                              "play": {"vel_sens": 1}, "synth": {"layers": ["sine phase=0"] + [f"sine phase=0 ratio={r:.6f} level={d:g}dB" for r, d in DROP_NOTES[1]], "filters": ["lp cutoff=600"], "amp": {"a": "1ms", "d": "110ms", "s": 0, "r": "30ms"}}}
        PATCHES["sr-tap"] = {"about": "Standing Room's tap of letting go (chirper-zero, 28 Nov, v31): one short plain tone.",
                             "play": {"vel_sens": 0}, "synth": {"layers": ["sine phase=0"], "filters": ["lp cutoff=7000"], "amp": {"a": "0.5ms", "d": "25ms", "s": 0, "r": "10ms"}}}
        doc["tracks"].append({"name": "drop-tap", "patch": "sr-tap", "gain": f"{dr_g + DROP_TAP[1]:g}dB", "pan": 0.0, "notes": [{"at": at, "len": 0.05, "pitch": DROP_TAP[0], "vel": 0.8} for _, _, _, _, at, _, _ in dr]})
        doc["tracks"].append({"name": "drop-thud", "patch": "sr-thud", "gain": DROP_GAIN, "pan": 0.0, "notes": [{"at": land, "len": 0.2, "pitch": DROP_NOTES[0], "vel": round(10 ** (d / 40), 5)} for _, _, _, _, _, land, d in dr]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v31 something is let go down the stairwell (bars {drop_row() + 1} to {drop_row() + ROW}, the first whole row of the stairs): at a tap in every bar, a flight of {DROP_STEPS} steps ({DROP_STEPS * DROP_RISER:g} m) higher each time; its thud is heard after the fall and the sound's way back up: {', '.join(f'{1000 * (f + u):.0f}' for _, _, f, u, _, _, _ in dr)} ms: the wait grows as the square root of the height. Generated by")
        assert "From v31" in doc["about"]
    if WELL and drop_row() is not None:
        import math as wl_math
        wl = well_ways(); wl_one = SOUND / (2 * DROP_STEPS * DROP_RISER)
        for wl_n, _, wl_k, wl_at in wl:
            PATCHES[f"sr-well-{wl_n}"] = {"about": f"Standing Room's stairwell ringing from {wl_n} flight(s) up (chirper-zero, 28 Nov, v32): {len(wl_k)} plain tones, the ways of a column of air {wl_n * DROP_STEPS * DROP_RISER:.2f} m high between {WELL_BAND[0]:g} and {WELL_BAND[1]:g} Hz, each the same; struck and dying in {WELL_RING:g} s; nothing over 600 Hz.",
                                          "play": {"vel_sens": 0}, "synth": {"layers": [f"sine phase=0 ratio={k / wl_n:.6f} level={-10 * wl_math.log10(len(wl_k)):.2f}dB" for k, _ in wl_k], "pitch": {"value": round(12 * wl_math.log2(wl_one / WELL_NOTE[1]), 7)},
                                                                              "filters": ["lp cutoff=600"], "amp": {"a": "5ms", "d": f"{WELL_RING:g}s", "s": 0, "r": "50ms"}}}
            doc["tracks"].append({"name": f"well-{wl_n}", "patch": f"sr-well-{wl_n}", "gain": WELL_GAIN, "pan": 0.0, "notes": [{"at": wl_at, "len": round(WELL_RING * BPM / 60, 5), "pitch": WELL_NOTE[0], "vel": 0.8}]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v32 the stairwell rings (the same bars): every thud rings the column of air between the floor and where you stand: one flight's own note is {wl_one:.1f} Hz; from n flights up the lowest way is that over n ({', '.join(f'{f:.1f}' for _, f, _, _ in wl)} Hz) and every multiple of it rings: {', '.join(str(len(k)) for _, _, k, _ in wl)} ways between {WELL_BAND[0]:g} and {WELL_BAND[1]:g} Hz, {wl_one:.1f} and {2 * wl_one:.1f} Hz among them every time. Generated by")
        assert "From v32" in doc["about"]
    if kept_row() is not None:
        kt_c, kt_f, kt_t = kept_times()
        PATCHES["sr-kept"] = {"about": "Standing Room's one clap that the hall keeps (chirper-zero, 28 Nov, v33): the engine's machine clap, as the song's own, nothing over 7 kHz. Its track has the engine's hall on it, and a lane (auto.keep) that stops the hall dying while it is 1.",
                              "play": {"vel_sens": 0}, "synth": {"layers": [{"type": "machine", "machine": {"part": "clap", "bursts": 3, "decay": "140ms"}}], "filters": ["lp cutoff=7000"], "amp": {"a": "0.1ms", "d": "0s", "s": 1, "r": "400ms"}}}
        doc["tracks"].append({"name": "kept", "patch": "sr-kept", "gain": KEPT_GAIN, "pan": 0.0,
                              "auto": {"keep": {"points": [["0b", 0], [f"{kt_f - 0.001:g}b", 0], [f"{kt_f:g}b", 1], [f"{kt_t - 0.001:g}b", 1], [f"{kt_t:g}b", 0]], "curve": 0}},
                              "fx": [{"type": "reverb", **KEPT_HALL, "freeze": {"value": 0, "mod": [{"src": "auto.keep", "amount": 1}]}}],
                              "notes": [{"at": kt_c, "len": 0.25, "pitch": "C4", "vel": 0.8}]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v33 the room holds its breath (bars {int(kt_c) // BEATS + 1} to {int(kt_t) // BEATS}): one clap in a hall on beat {kt_c % BEATS + 1:g} of bar {int(kt_c) // BEATS + 1}; {KEPT_FROM:g} of a beat after it the hall stops dying and its tail hangs as it was for {kt_t - kt_f:g} beats ({(kt_t - kt_f) * 60 / BPM:.1f} s); on the first beat of bar {int(kt_t) // BEATS + 1}, where the applause begins, it lets go and dies in {KEPT_HALL['decay']}. Generated by")
        assert "From v33" in doc["about"]
    if recede_row() is not None:
        rk = recede_knocks()
        PATCHES["sr-recede"] = {"about": f"Standing Room's knock that goes away (chirper-zero, 28 Nov, v34): a low thud ({RECEDE_NOTE[0]} and its octave), 90 ms, whose loudness is all velocity (the amplitude goes as the velocity squared): half the velocity squared for every doubling of the distance. The same patch on a second track is the room's answer: every knock at one velocity through the engine's hall, all of it.",
                                "play": {"vel_sens": 1, "gate": 1}, "synth": {"layers": ["sine phase=0", "sine phase=0 ratio=2 level=-12dB"], "filters": ["lp cutoff=7000"], "amp": {"a": "1ms", "d": "90ms", "s": 0, "r": "20ms"}}}
        doc["tracks"].append({"name": "recede", "patch": "sr-recede", "gain": RECEDE_GAIN, "pan": 0.0, "notes": [{"at": h, "len": 0.25, "pitch": RECEDE_NOTE[0], "vel": v} for _, h, _, _, v in rk]})
        doc["tracks"].append({"name": "recede-room", "patch": "sr-recede", "gain": RECEDE_ROOM_GAIN, "pan": 0.0, "fx": [{"type": "reverb", **RECEDE_ROOM}], "notes": [{"at": h, "len": 0.25, "pitch": RECEDE_NOTE[0], "vel": 1.0} for _, h, _, _, _ in rk]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v34 the knock goes away and the room does not (bars {recede_row() + 1} to {recede_row() + ROW}): a low knock twice a bar, each time twice as far off ({rk[0][3]:.1f} m to {RECEDE_FAR:.0f} m) and then back; each doubling takes 6 dB off the knock and makes it later (a whole beat at the far end), and the room's answer stays as loud: from {RECEDE_FAR / 2 ** (RECEDE_STEPS - 1 - RECEDE_CRIT):.1f} m on there is more room than knock. Generated by")
        assert "From v34" in doc["about"]
    if ears_row() is not None:
        ep = ears_pips(); e_len = EARS_MS / 1000 * BPM / 60
        PATCHES["sr-ears"] = {"about": f"Standing Room's pip for sooner or louder (chirper-zero, 28 Nov, v35): a plain tone, {EARS_MS} ms, {EARS_EDGE} ms to come and to go; its wave begins afresh with every note, so a note begun later is the same sound later. Its loudness goes as the square of the velocity.",
                              "play": {"vel_sens": 1, "gate": 1}, "synth": {"layers": ["sine phase=0"], "filters": ["lp cutoff=7000"], "amp": {"a": f"{EARS_EDGE}ms", "d": "0s", "s": 1, "r": f"{EARS_EDGE}ms"}}}
        for nm, sg in (("ears-l", -1), ("ears-r", 1)):
            doc["tracks"].append({"name": nm, "patch": "sr-ears", "gain": EARS_GAIN, "pan": float(sg),
                                  "notes": [{"at": round(t - sg * itd / 2 * BPM / 60, 7), "len": round(e_len, 7), "pitch": EARS_NOTE, "vel": round(10 ** ((-EARS_LEVEL / 2 + sg * ild / 2) / 40), 5)} for _, _, t, itd, ild in ep]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v35 sooner or louder (bars {ears_row() + 1} to {ears_row() + ROW}): the same plain pip in both ears walks from the left to the right twice: first both ears get it exactly as loud and one gets it sooner (by up to {max(abs(p[3]) for p in ep) * 1e6:.0f} millionths of a second: the way round a head), then both get it at the same instant and one gets it louder (by up to {max(abs(p[4]) for p in ep):.1f} dB). Generated by")
        assert "From v35" in doc["about"]
    if rung_row() is not None:
        PATCHES["sr-rung"] = {"about": f"Standing Room's pip on the ladder (chirper-zero, 28 Nov, v36): one plain tone, {RUNG_MS} ms, {RUNG_EDGE} ms to come and to go; in the middle, no room.",
                              "play": {"vel_sens": 1, "gate": 1}, "synth": {"layers": ["sine phase=0"], "filters": ["lp cutoff=9000"], "amp": {"a": f"{RUNG_EDGE}ms", "d": "0s", "s": 1, "r": f"{RUNG_EDGE}ms"}}}
        doc["tracks"].append({"name": "rung", "patch": "sr-rung", "gain": RUNG_GAIN, "pan": 0.0, "notes": [{"at": at, "len": round(RUNG_MS / 1000 * BPM / 60, 6), "pitch": rung_note(k), "vel": v} for at, k, v in rung_pips()]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v36 the higher the note, the higher it hangs (bars {rung_row() + 1} to {rung_row() + ROW}): one plain pip a beat, always in the middle and the same in both ears, comes down {RUNG_N} notes from {rung_note(RUNG_N - 1)} to {rung_note(0)} and climbs them again; nothing but its note changes, and a higher note is said to seem to come from higher up (Pratt, 1930). Generated by")
        assert "From v36" in doc["about"]
    if cloud_row() is not None:
        cb_ = cloud_bursts(); c_top = max(CLOUD_TRIM); c_vel = lambda share, q: round(share ** 0.25 * 10 ** ((CLOUD_TRIM[q] - c_top) / 40), 5)
        PATCHES["sr-cloud"] = {"about": f"Standing Room's short hiss for the cloud that becomes a point (chirper-zero, 28 Nov, v37): the engine's white noise from {CLOUD_BAND[0]} to {CLOUD_BAND[1]} Hz, {CLOUD_EDGE[0]} ms to come and {CLOUD_EDGE[1]} to go. Every note of it is a new hiss, and two tracks of it are two different hisses. Its loudness goes as the square of the velocity.",
                               "play": {"vel_sens": 1, "gate": 1}, "synth": {"layers": ["white"], "filters": [f"hp cutoff={CLOUD_BAND[0]}"] * 2 + [f"lp cutoff={CLOUD_BAND[1]}"] * 4, "amp": {"a": f"{CLOUD_EDGE[0]}ms", "d": "0s", "s": 1, "r": f"{CLOUD_EDGE[1]}ms"}}}
        for nm, pan, mid in (("cloud-c", 0.0, True), ("cloud-l", -1.0, False), ("cloud-r", 1.0, False)):
            doc["tracks"].append({"name": nm, "patch": "sr-cloud", "gain": CLOUD_GAIN, "pan": pan, "notes": [{"at": round(t, 6), "len": CLOUD_LEN, "pitch": "A4", "vel": c_vel(like if mid else 1 - like, q)} for _, t, like, q in cb_ if (like if mid else 1 - like) > 0]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v37 the pipe narrows (bars {cloud_row() + 1} to {cloud_row() + CLOUD_BARS}): a short hiss a sixteenth after every beat, written as loud in each ear all the way; first each ear has a hiss of its own (a cloud), then more and more of it is the same hiss in both, and at the end it is one hiss (a point). Generated by")
        assert "From v37" in doc["about"]
    if dull_row() is not None:
        dk_ = dull_knocks(); d_top = max(DULL_TRIM)
        for k in range(ROW):
            PATCHES[f"sr-dull-{k}"] = {"about": f"Standing Room's low knock with its top taken (chirper-zero, 28 Nov, v38): a saw that dies in {DULL_EDGE[1]} ms, through a low-pass at {dull_cut(k):.0f} Hz ({k * DULL_STEP:g} octaves under {DULL_TOP} Hz). Its loudness goes as the square of the velocity.",
                                       "play": {"vel_sens": 1, "gate": 1}, "synth": {"layers": ["saw"], "filters": [f"lp cutoff={dull_cut(k):.0f}"], "amp": {"a": f"{DULL_EDGE[0]}ms", "d": f"{DULL_EDGE[1]}ms", "s": 0, "r": f"{DULL_EDGE[2]}ms"}}}
            doc["tracks"].append({"name": f"dull-{k}", "patch": f"sr-dull-{k}", "gain": DULL_GAIN, "pan": 0.0, "notes": [{"at": round(t, 6), "len": DULL_LEN, "pitch": DULL_NOTE, "vel": round(10 ** ((DULL_TRIM[i] - d_top) / 40), 5)} for i, t, st in dk_ if st == k]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v38 how far by how dull alone (bars {dull_row() + 1} to {dull_row() + ROW}): outside, the same low knock twice a bar, the second with its top taken half an octave lower each bar and written as loud. Generated by")
        assert "From v38" in doc["about"]
    if luc_row() is not None:
        ag_ = luc_knocks(); ag_base = float(LUC_GAIN.replace("dB", ""))
        PATCHES["sr-said"] = {"about": f"Standing Room's knock to be said again (chirper-zero, 28 Nov, v39): a saw that dies in {LUC_KNOCK} ms, under 3 kHz. Its loudness goes as the square of the velocity.",
                              "play": {"vel_sens": 1, "gate": 1}, "synth": {"layers": ["saw"], "filters": ["lp cutoff=3000"], "amp": {"a": "0.5ms", "d": f"{LUC_KNOCK}ms", "s": 0, "r": "5ms"}}}
        PATCHES["sr-keep"] = {"about": "Standing Room's keeper (chirper-zero, 28 Nov, v39): one plain tone, held, played 120 dB down into a chain of eqs so that the engine keeps the chain running after the knock that went into it has ended. It is not there to be heard.",
                              "play": {"gate": 1}, "synth": {"layers": ["sine"], "amp": {"a": "5ms", "d": "0s", "s": 1, "r": "5ms"}}}
        for j in range(ROW):
            ag_t = {"name": f"said-{j}", "patch": "sr-said", "gain": f"{ag_base - LUC_UP * j + LUC_TRIM[j]:.1f}dB", "pan": 0.0, "notes": [{"at": round(t, 6), "len": 0.1, "pitch": LUC_NOTE, "vel": 1} for k, t in ag_ if k == j]}
            if j:
                doc.setdefault("buses", {})[f"again-{j}"] = {"fx": [{"type": "eq", "bands": [f"peak cutoff={STAND_ROOT * n:.3f} q={luc_q(n):.3f} gain={LUC_UP:g}dB" for n in LUC_WAYS]} for _ in range(j)]}
                ag_t["out"] = f"again-{j}"
                doc["tracks"].append({"name": f"said-keep-{j}", "patch": "sr-keep", "gain": "-120dB", "pan": 0.0, "out": f"again-{j}", "notes": [{"at": (luc_row() + j) * BEATS, "len": BEATS, "pitch": LUC_NOTE, "vel": 1}]})
            doc["tracks"].append(ag_t)
        doc["about"] = doc["about"].replace(" Generated by", f" From v39 three knocks are said into the corridor again and again (bars {luc_row() + 1} to {luc_row() + ROW}): every bar they have been through the corridor's five ringing ways once more, and bar by bar the knocks go and the corridor's own notes are left (after Alvin Lucier, I am sitting in a room, 1969). Generated by")
        assert "From v39" in doc["about"]
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
        if luc_row() is not None:
            ag_sec = luc_row() * BEATS * 60 / BPM; ag_base = float(LUC_GAIN.replace("dB", ""))
            print(f"said again and again, only the room is left ({LUC_GAIN}), bars {luc_row() + 1}-{luc_row() + ROW} ({int(ag_sec) // 60}:{ag_sec % 60:04.1f}): {len(LUC_AT)} knocks a bar (a saw on {LUC_NOTE}, {LUC_KNOCK} ms) on beats " + " ".join(f"{q:g}" for q in LUC_AT) + f" ; bar by bar they have been through 0 to {ROW - 1} passes of the corridor's ways " + " ".join(str(n) for n in LUC_WAYS) + " (" + " ".join(f"{STAND_ROOT * n:.1f}" for n in LUC_WAYS) + f" Hz) ; a pass lifts each way {LUC_UP:g} dB (q " + " ".join(f"{luc_q(n):.1f}" for n in LUC_WAYS) + f": a ring that falls to 1/e in {1000 * LUC_TAU:g} ms) and the {LUC_UP:g} dB are taken off the whole again ; the faders bar by bar: " + " ".join(f"{ag_base - LUC_UP * j + LUC_TRIM[j]:.1f}" for j in range(ROW)) + " dB" + (" ; trims " + " ".join(f"{x:+.1f}" for x in LUC_TRIM) + " dB" if any(LUC_TRIM) else " ; no trims"))
        if dull_row() is not None:
            dk_ = dull_knocks(); u_sec = dull_row() * BEATS * 60 / BPM
            print(f"how far by how dull alone ({DULL_GAIN}), bars {dull_row() + 1}-{dull_row() + ROW} ({int(u_sec) // 60}:{u_sec % 60:04.1f}): {len(dk_)} low knocks ({DULL_NOTE}, {hz(DULL_NOTE):.1f} Hz, a saw, {DULL_LEN * 60000 / BPM:.0f} ms) on beats " + " ".join(f"{x:g}" for x in DULL_AT) + f" of every bar ; the first of a bar through a low-pass at {DULL_TOP} Hz ; the second, bar by bar, at " + " ".join(f"{dull_cut(j):.0f}" for j in range(ROW)) + f" Hz: {DULL_STEP:g} of an octave a bar ; by the classical law (the loss in dB as the square of the frequency) " + " ".join(f"{2 ** (2 * j * DULL_STEP):g}" for j in range(ROW)) + " times as far" + (f" ; trims {min(DULL_TRIM):+.1f} to {max(DULL_TRIM):+.1f} dB" if any(DULL_TRIM) else " ; no trims"))
        if cloud_row() is not None:
            cb_ = cloud_bursts(); c_sec = cloud_row() * BEATS * 60 / BPM
            print(f"the pipe narrows: a cloud becomes a point ({CLOUD_GAIN}), bars {cloud_row() + 1}-{cloud_row() + CLOUD_BARS} ({int(c_sec) // 60}:{c_sec % 60:04.1f}): {len(cb_)} hisses of {CLOUD_LEN} of a beat ({CLOUD_LEN * 60000 / BPM:.0f} ms), {CLOUD_BAND[0]} to {CLOUD_BAND[1]} Hz, on beats {' '.join(f'{x:g}' for x in CLOUD_AT)} of every bar ; three tracks of one patch: one in the middle (the same hiss to both ears) and one to each ear alone (two different hisses) ; how alike the two ears are, bar by bar: {' '.join(f'{x:g}' for x in CLOUD_LIKE)} ; each ear's power the same throughout: the middle track's share of it is that number" + (f" ; trims by beat of the bar {' '.join(f'{x:+.1f}' for x in CLOUD_TRIM)} dB" if any(CLOUD_TRIM) else " ; no trims"))
        if rung_row() is not None:
            rp_ = rung_pips(); r_sec = rung_row() * BEATS * 60 / BPM
            print(f"the higher the note, the higher it hangs ({RUNG_GAIN}), bars {rung_row() + 1}-{rung_row() + ROW} ({int(r_sec) // 60}:{r_sec % 60:04.1f}): a plain pip ({RUNG_MS} ms) on beats " + ", ".join(f"{q + x:g}" for q, x in enumerate(RUNG_AT)) + f" of every bar, in the middle, no room ; {RUNG_N} rungs down ({rung_note(RUNG_N - 1)} {hz(rung_note(RUNG_N - 1)):.1f} Hz to {rung_note(0)} {hz(rung_note(0)):.1f} Hz: " + " ".join(rung_note(k) for k in range(RUNG_N - 1, -1, -1)) + f") and the same {RUNG_N} up ; {len(rp_)} pips ; velocities {min(v for _, _, v in rp_):g} to {max(v for _, _, v in rp_):g}" + (f" (trims {min(RUNG_TRIM):g} to {max(RUNG_TRIM):g} dB)" if RUNG_TRIM else " (no trims)"))
        if ears_row() is not None:
            ep = ears_pips(); e_sec = ears_row() * BEATS * 60 / BPM
            print(f"sooner or louder ({EARS_GAIN}), bars {ears_row() + 1}-{ears_row() + ROW} ({int(e_sec) // 60}:{e_sec % 60:04.1f}): the same plain pip ({EARS_NOTE}, {hz(EARS_NOTE):.0f} Hz, {EARS_MS} ms) in each ear on beats " + " and ".join(f"{x:.3f}" for x in EARS_AT) + f" of every bar, from the left to the right ; a head of {100 * EARS_HEAD:g} cm ; " + " ; ".join(f"the walk by {w} (bars {int(min(p[2] for p in ep if p[0] == w)) // BEATS + 1}-{int(max(p[2] for p in ep if p[0] == w)) // BEATS + 1}), degrees and " + ("millionths of a second the left ear gets it later (minus: sooner): " + " ".join(f"{p[1]:+d}:{p[3] * 1e6:+.0f}" for p in ep if p[0] == w) if w == "time" else "dB the right ear gets it louder: " + " ".join(f"{p[1]:+d}:{p[4]:+.1f}" for p in ep if p[0] == w)) for i, w in enumerate(EARS_WALKS)))
        if recede_row() is not None:
            rk = recede_knocks(); rc_sec = recede_row() * BEATS * 60 / BPM
            print(f"the knock goes away, the room does not ({RECEDE_GAIN}; the room {RECEDE_ROOM_GAIN}), bars {recede_row() + 1}-{recede_row() + ROW} ({int(rc_sec) // 60}:{rc_sec % 60:04.1f}): a low knock ({RECEDE_NOTE[0]}, {RECEDE_NOTE[1]:.1f} Hz and its octave, 90 ms) struck on beats {RECEDE_AT[0]:.3f} and {RECEDE_AT[1]:.3f} of every bar ; {RECEDE_STEPS} distances out (bars {recede_row() + 1}-{recede_row() + ROW // 2}) and back ; the room's answer ({RECEDE_ROOM['kind']}, {RECEDE_ROOM['decay']} to die) the same every time ; step: metres off, heard ms after it is struck, the knock dB, the knock against the room's whole answer dB: " + " | ".join(f"{k}: {m:.2f} m, {1000 * m / SOUND:.1f} ms, {-20 * math.log10(2) * k:.1f}, {20 * math.log10(2) * (RECEDE_CRIT - k):+.1f}" for _, _, k, m, _ in rk[:RECEDE_STEPS]) + f" ; {len(rk)} knocks ; trimmed by place for the master (dB, knock by knock): " + " ".join(f"{t:g}" for t in RECEDE_TRIM))
        if kept_row() is not None:
            kt_c, kt_f, kt_t = kept_times(); kt_sec = kt_c * 60 / BPM
            print(f"the room holds its breath ({KEPT_GAIN}), bars {int(kt_c) // BEATS + 1}-{int(kt_t) // BEATS} ({int(kt_sec) // 60}:{kt_sec % 60:04.1f}): one clap in a hall ({KEPT_HALL['kind']}, {KEPT_HALL['decay']} to die, {KEPT_HALL['low_cut']} to {KEPT_HALL['high_cut']} Hz) on beat {kt_c % BEATS:g} of bar {int(kt_c) // BEATS + 1} ; the hall stops dying {KEPT_FROM:g} of a beat ({1000 * KEPT_FROM * 60 / BPM:.0f} ms) after it and holds for {kt_t - kt_f:g} beats ({(kt_t - kt_f) * 60 / BPM:.2f} s) ; it lets go on beat {kt_t % BEATS:g} of bar {int(kt_t) // BEATS + 1}")
        if WELL and drop_row() is not None:
            wl = well_ways()
            print(f"the stairwell rings ({WELL_GAIN}), bars {drop_row() + 1}-{drop_row() + ROW}: every thud rings the column between the floor and you: one flight's own note {SOUND / (2 * DROP_STEPS * DROP_RISER):.2f} Hz ; the ways written are those from {WELL_BAND[0]:g} to {WELL_BAND[1]:g} Hz ; a ring dies in {WELL_RING:g} s ; {sum(len(k) for _, _, k, _ in wl)} tones in all")
            for n, low, ks, at in wl:
                print(f"   {n} flight(s): the lowest way {low:.2f} Hz ; {len(ks)} ways written (each {-10 * __import__('math').log10(len(ks)):.1f} dB): " + " ".join(f"{f:.1f}" for _, f in ks) + f" Hz ; from beat {at - (drop_row() + n - 1) * BEATS:.3f} of bar {drop_row() + n}")
        if drop_row() is not None:
            dr = drop_falls(); dr_sec = BEATS * 60 / BPM
            print(f"a drop down the stairwell ({DROP_GAIN}), bars {drop_row() + 1}-{drop_row() + ROW} ({int(drop_row() * dr_sec) // 60}:{drop_row() * dr_sec % 60:04.1f}): let go on beat {DROP_AT:g} of every bar (a tap, {DROP_TAP[0]}), a flight of {DROP_STEPS} steps ({DROP_STEPS * DROP_RISER:g} m) higher each bar ; the thud {DROP_NOTES[0]} and " + ' and '.join(f"{r:g} times it ({d:g} dB)" for r, d in DROP_NOTES[1]))
            for n, h, fall, up, at, land, d in dr:
                print(f"   bar {drop_row() + n}: {n} flight(s), {h:.2f} m: falls {1000 * fall:.1f} ms, the sound comes up in {1000 * up:.1f} ms: heard {1000 * (fall + up):.1f} ms after the tap, on beat {land - (drop_row() + n - 1) * BEATS:.3f} ; {d:+.1f} dB")
        if close_row() is not None:
            cl = close_trains(); cl_sec = BEATS * 60 / BPM
            print(f"the walls close in ({CLOSE_GAIN}), bars {close_row() + 1}-{close_row() + ROW} ({int(close_row() * cl_sec) // 60}:{close_row() * cl_sec % 60:04.1f}): a knock on beats {' and '.join(f'{x:g}' for x in CLOSE_AT)} of every bar and its echoes between two walls ; every train falls {CLOSE_FALL:g} dB a second and is let go {CLOSE_END:g} dB down ; {CLOSE_SHARE:g} dB off every echo for each halving of the width ; {sum(len(es) for _, _, _, _, es in cl)} thuds in {len(cl)} trains")
            for cl_b, cl_st, cl_per, _, cl_es in cl[::len(CLOSE_AT)]:
                print(f"   bar {close_row() + cl_b + 1}: walls {SOUND * cl_per / CLOSE_RATE / 2:6.2f} m apart: across and back in {cl_per} samples ({1000 * cl_per / CLOSE_RATE:.2f} ms): {CLOSE_RATE / cl_per:6.2f} echoes a second ; {len(cl_es)} thuds a train, the first {cl_es[0][1]:+.1f} dB, the last {cl_es[-1][1]:+.1f}")
        if began_row() is not None:
            bg_sec = BEATS * 60 / BPM
            print(f"where it began ({BEGAN_GAIN}, {BEGAN_AIR} of it to the air), bars {began_row() + 1}-{began_row() + BEGAN_IN[2] * ROW} ({int(began_row() * bg_sec) // 60}:{began_row() * bg_sec % 60:04.1f}): every {BEGAN_EVERY} bars from beat {BEGAN_AT:g} a plain tone (each twice: with its start, then without), {BEGAN_LEN:g} beats ({BEGAN_LEN * 60 / BPM:.2f} s) and {1000 * BEGAN_FADE:g} ms going out ; its start is whole on the left for {1000 * BEGAN_HOLD:g} ms, then falls to nothing in {1000 * BEGAN_HAND:g} ms while the right rises to the whole tone ; pan {BEGAN_PAN:g}")
            print("   " + " ; ".join(f"bar {int(t // BEATS) + 1}: {p} ({hz(p):.0f} Hz) {'starts on the left, goes on from the right' if st else 'the same without its start: from the right only'}" for t, p, st in began_tones()))
        if foot_bar() is not None:
            print(f"the foot of the stairs, bars {foot_bar() + 1}-{foot_bar() + FOOT_BARS} ({int(foot_bar() * BEATS * 60 / BPM) // 60}:{foot_bar() * BEATS * 60 / BPM % 60:04.1f}, {FOOT_BARS * BEATS * 60 / BPM:.2f} s): " + " and ".join(f"the {k}" for k in FOOT_WAIT) + f" wait ; the click, the tock and the stairwell's echo of them go on ; the drum comes back in bar {foot_bar() + FOOT_BARS + 1}, with the first clap on the stairs")
        if HUSH and slam_bar() is not None:
            hu_s = HUSH_BARS * BEATS * 60 / BPM
            print(f"the hush after the door, bars {slam_bar() + 1}-{slam_bar() + HUSH_BARS} ({hu_s:.2f} s): every track waits but those named " + ", ".join(f"{k}..." for k in HUSH_KEEP) + f" (the bird is heard from bar {slam_bar() + HUSH_BARS + 1}, three times round) ; by the hush's end the tail's bands have fallen " + " ".join(f"{min(-SLAM_FLOOR, 60 * hu_s / b[2]):.0f}" for b in slam_bands()) + f" dB (gone at {-SLAM_FLOOR:g})")
        sec = 60 / BPM * BEATS
        if slam_bar() is not None:
            sl_w, sl_d, sl_h = SLAM_HALL
            print(f"the hangar's door shuts ({SLAM_GAIN} the bottom band), bar {slam_bar() + 1} ({int(slam_bar() * sec) // 60}:{slam_bar() * sec % 60:04.1f}): the hangar {sl_w:g} x {sl_d:g} x {sl_h:g} m ({sl_w * sl_d * sl_h:.0f} cubic metres, {2 * (sl_w * sl_d + sl_w * sl_h + sl_d * sl_h):.0f} square metres), its walls take {SLAM_WALLS:g} ; the slam {slam_direct():.1f} dB over the tail for {SLAM_DIRECT * 1000:.0f} ms, in the middle ({SLAM_AWAY:g} m from the door) ; the tail {SLAM_WIDE:g} wide ; the door's sound {SLAM_TILT:g} dB an octave")
            for sl_k, (sl_lo, sl_hi, sl_rt, sl_trim) in enumerate(slam_bands()):
                print(f"   band {sl_k + 1}: {sl_lo:g} to {sl_hi:g} Hz, the air {SLAM_AIR[sl_k]:g} dB a km: 60 dB down in {sl_rt:.2f} s (bar {slam_bar() + 1 + sl_rt / sec:.1f}), gone in {sl_rt * SLAM_FLOOR / -60:.1f} s ; its fader {sl_trim:+.2f} dB against SLAM_GAIN ; after 1, 2, 4, 8 s: " + " ".join(f"{slam_db(sl_k, t):.1f}" for t in (1, 2, 4, 8)) + " dB")
        if BEND:
            print(f"the bass round the corner, bars {BEND_BARS[0] + 1}-{BEND_BARS[1]} ({int(BEND_BARS[0] * sec) // 60}:{BEND_BARS[0] * sec % 60:04.1f}): {BEND_SIDE:g} m down a side passage ; you start {BEND_FROM:g} m short of the corner ({BEND_FROM / ((BEND_BARS[1] - BEND_BARS[0]) * sec):.2f} m/s) ; the shadow 10 log (3 + 20 N) dB ; the way's law {BEND_LAW:g} ; the bass's partials {' '.join(f'{p:g}' for p in BEND_PARTS)} dB")
            for bd_bar in list(range(BEND_BARS[0], BEND_BARS[1], 4)) + [BEND_BARS[1] - 2, BEND_BARS[1] - 1, BEND_BARS[1] - 0.25, BEND_BARS[1]]:
                bd_w = bend_way(bd_bar * BEATS)
                print(f"   bar {bd_bar + 1:g}: {bd_w:5.2f} m short ; the way round {BEND_SIDE + bd_w - math.hypot(BEND_SIDE, bd_w):.2f} m longer ; the shadow takes " + " ".join(f"{-bend_shadow(hz('D2') * h, bd_w):.1f}" for h in (1, 2, 3, 4, 6)) + f" dB of partials 1 2 3 4 6 ; the way {-bend_spread(bd_w):.1f} dB ; the first partial {bend_shadow(hz('D2'), bd_w) + bend_spread(bd_w):+.1f} dB against the bass met")
        if gal_row() is not None:
            ga = gal_arrivals(); ga_lap = GAL_LAP * STEP * 60 / BPM * SOUND
            print(f"the whispering gallery, bars {gal_row() + 1}-{gal_row() + ROW} ({int(gal_row() * sec) // 60}:{gal_row() * sec % 60:04.1f}): {ga_lap / math.pi:.1f} m across, {ga_lap:.1f} m round ({GAL_LAP} sixteenths) ; a whisper every {GAL_EVERY} bars on sixteenth {GAL_ON}, {GAL_TIMES} times round each way ; {GAL_BAND[0]:g} to {GAL_BAND[1]:g} Hz, {GAL_GAIN}, pan {GAL_PAN} ; the first whisper is heard on sixteenths (l left, r right; dB): " + " ".join(f"{(at - gal_row() * BEATS) / STEP:g}{'l' if sd < 0 else 'r'}({db:.1f})" for w, sd, _, at, _, db in ga if w == 0))
        if rail_row() is not None:
            rl = rail_knocks(); rl_b0 = rail_row()
            print(f"the corridor's handrail, bars {rl_b0 + 1}-{rl_b0 + ROW} ({int(rl_b0 * sec) // 60}:{rl_b0 * sec % 60:04.1f}): steel {RAIL_SPEED:g} m/s, air {SOUND:g} m/s ; a mark is {rl[0][1]:.2f} m (a thirty-second of air) ; the ring {RAIL_NOTE} ({RAIL_GAIN}, pan {RAIL_PAN}), the air's knock {AIR_NOTE} ({AIR_GAIN}, pan {AIR_PAN}) ; the steel keeps {RAIL_LOSS} dB a mark, the air falls as 1 over the distance to the power {AIR_LAW}")
            for rl_k, rl_m, rl_s, rl_st, rl_ai, rl_sdb, rl_adb in rl:
                rl_step = lambda t: f"{int(t // BEATS) + 1}:{(t % BEATS) / STEP:.3f}"
                print(f"   {rl_m:5.1f} m: struck {rl_step(rl_s)} ; the steel's ring {rl_step(rl_st)} ({(rl_st - rl_s) * 60 / BPM * 1000:.1f} ms after, {rl_sdb:+.1f} dB) ; the air's knock {rl_step(rl_ai)} ({(rl_ai - rl_s) * 60 / BPM * 1000:.0f} ms after, {rl_adb:+.1f} dB) ; the ring comes {(rl_ai - rl_st) * 60 / BPM * 1000:.0f} ms before it")
        if duct_row() is not None:
            du = duct_echoes(); du_b0 = duct_row(); du_sec = 60 / BPM
            print(f"the hall's air duct, bars {du_b0 + 1}-{du_b0 + ROW} ({int(du_b0 * BEATS * du_sec) // 60}:{du_b0 * BEATS * du_sec % 60:04.1f}): {SOUND / (2 * duct_hz()):.2f} m across, its own note {DUCT_NOTE} ({duct_hz():.1f} Hz) ; the ways across heard: {', '.join(f'{m * duct_hz():.0f} Hz {lv:g} dB' for m, lv in DUCT_MODES)} ; each echo first heard {DUCT_TOP:g} times too high ; {DUCT_GAIN}, pan {DUCT_PAN}")
            for du_j, (du_at, du_len, du_back, du_p) in enumerate(du):
                print(f"   bar {du_b0 + du_j + 1}: {DUCT_BACK[du_j]} sixteenths there and back ({du_back * 1000:.0f} ms, {du_back * SOUND / 2:.0f} m long) ; begins on step {(du_at % BEATS) / STEP:.3f} ({duct_first(du_back) * 1000:.1f} ms after the straight sound) ; semitones over its note after 10 30 100 300 1000 ms: " + " ".join(f"{12 * math.log2(duct_over(duct_first(du_back) + ms / 1000, du_back)):.2f}" for ms in (10, 30, 100, 300, 1000)) + f" ; held {du_len * du_sec * 1000:.0f} ms")
        if dome_row() is not None:
            do_six = STEP * 60 / BPM * 1000; do_b0 = dome_row()
            print(f"under the dome, bars {do_b0 + 1}-{do_b0 + ROW} ({int(do_b0 * BEATS * 60 / BPM) // 60}:{do_b0 * BEATS * 60 / BPM % 60:04.1f}): from the click to the dome and down to the focus {DOME_PATH} sixteenths ({DOME_PATH * do_six / 1000 * SOUND:.0f} m) by way of every part ; {DOME_PARTS} parts, {DOME_RISE:g} degrees up, {DOME_UP} sixteenths from the focus ; you start {DOME_WALK[0]:g} sixteenths ({DOME_WALK[0] * do_six / 1000 * SOUND:.0f} m) from it and are on it after {DOME_WALK[1]} bars ; {DOME_GAIN}")
            print("   the parts (degrees round from straight ahead, pan): " + " ".join(f"{t:.0f}:{p:+.2f}" for t, p in dome_parts()))
            for do_j in range(ROW):
                do_l = sorted(dome_late(do_j, t) for t, _ in dome_parts())
                print(f"   bar {do_b0 + do_j + 1}: {dome_off(do_j):.2f} sixteenths off ; the echoes on steps " + " ".join(f"{CLICK_STEP + v:.2f}" for v in do_l) + f" ; first to last {(do_l[-1] - do_l[0]) * do_six:.1f} ms")
        if FOUR and four_rows():
            fo_six = STEP * 60 / BPM * 1000
            print(f"the hangar's other two walls: in front and behind, {FOUR_DEEP[0]} + {FOUR_DEEP[1]} sixteenths there and back ({(FOUR_DEEP[0] + FOUR_DEEP[1]) / 2 * fo_six / 1000 * SOUND:.0f} m deep, as it is wide) ; every wall takes {-FOUR_EACH:g} dB (the first {-FOUR_FIRST:g}) ; echoes that met more than {FOUR_WALLS} walls are left out ; {sum(len(v) for v in four_notes().values())} echoes on {sum(1 for v in four_notes().values() if v)} tracks ({FOUR_GAIN})")
            for fo_b0, fo_a, fo_b in four_rows():
                print(f"   bars {fo_b0 + 1}-{fo_b0 + ROW} ({int(fo_b0 * sec) // 60}:{fo_b0 * sec % 60:04.1f}), the click {fo_a} + {fo_b}: sixteenths late (the step of the bar it lands on; ms from the nearest sixteenth), across and deep, walls met, how many together, where:")
                for fo_late, fo_over, fo_w, fo_cnt, fo_dx, fo_dy in four_images(fo_a, fo_b):
                    fo_st = CLICK_STEP + fo_late; fo_off = (fo_st - round(fo_st)) * fo_six
                    print(f"      {fo_late:6.3f} (step {fo_st % 16:6.3f}{' of the next bar' if fo_st >= 16 else ''}; {fo_off:+6.1f} ms) ; {fo_dx:+3d} across, {fo_dy:2d} deep ; {fo_w} walls ; {fo_cnt} together ; {'middle' if fo_dx == 0 else ('left ' if fo_dx < 0 else 'right ') + format(abs(fo_over), '.2f')} ; {FOUR_FIRST + FOUR_EACH * (fo_w - 1) + 20 * math.log10(fo_cnt):+.1f} dB")
        if SONIC:
            so_first, so_made = sonic_first(); so_d = SONIC_AWAY * STEP * 60 / BPM * SOUND; so_six = STEP * 60 / BPM
            print(f"faster than sound: on the line of bar " + ", ".join(f"{b + 1} ({int(b * BEATS * 60 / BPM) // 60}:{b * BEATS * 60 / BPM % 60:04.1f})" for b in SONIC_AT) + f" something goes by at {SONIC_MACH:g} times the speed of sound ({SONIC_MACH * SOUND:.0f} m/s), {so_d:.1f} m off at its nearest, left to right, striking every {SONIC_EVERY * 60000 / BPM:.0f} ms ({SONIC_GAIN}) ; nothing of it is heard until {so_first * 1000:.0f} ms after it has passed (the sound it made {-so_made * 1000:.0f} ms before) ; far off, its coming is heard {1 / (SONIC_MACH - 1):g} times as fast, backwards ; its going 1/{SONIC_MACH + 1:g} as fast")
            for te, p, r, ta, fast, lev, side in sorted(sonic_strokes(), key=lambda q: q[3]):
                so_n = round(ta / so_six)
                print(f"   heard {ta * 1000:7.1f} ms after the line (sixteenth {so_n:2d} {(ta - so_n * so_six) * 1000:+5.1f} ms): {p:3s} struck {abs(te) * 1000:6.1f} ms {'before' if te < 0 else 'after '} it passed, {r:6.1f} m off ; {'BACKWARDS' if fast < 0 else 'forwards '} at {abs(fast):.3f} of its speed ({1200 * math.log2(abs(fast)):+7.1f} cents: {hz(p) * abs(fast):6.1f} Hz) ; {20 * math.log10(lev):+5.1f} dB ; {'left ' if side < 0 else 'right'} {abs(side):.2f}")
        if WHISTLE and whistle_pipes():
            wh_p = whistle_pipes(); wh_bar = BEATS * 60 / BPM; wh_n = whistle_notes(); wh_t = [n_ * whistle_far() / SOUND for n_ in range(1, WHISTLE_ECHOES + 1)]
            print(f"the pipes whistle, bars {wh_p[0][2] + 1}-{wh_p[-1][2] + 1} ({int(wh_p[0][2] * wh_bar) // 60}:{wh_p[0][2] * wh_bar % 60:04.1f}-{int((wh_p[-1][2] + 1) * wh_bar) // 60}:{(wh_p[-1][2] + 1) * wh_bar % 60:04.1f}): every pipe {whistle_far() / 2:.1f} m long ; the click (sixteenth {CLICK_STEP}) comes back from the far end after " + ", ".join(f"{1000 * x:.0f}" for x in wh_t) + f" ms (the next {WHISTLE_ECHOES} beats), {-WHISTLE_END:g} dB less each time, and as 1 over the distance to the power {WHISTLE_SPREAD:g} ; heard from beside the mouth (the sine of the angle: {WHISTLE_SIDE:g}) ; and by k glances off the walls after hypot(there and back, k widths) / {SOUND:g} ; a glance takes {-WHISTLE_WALL:g} dB ; {len(wh_n)} arrivals, each the stairs' tick on {WHISTLE_NOTE} ({WHISTLE_GAIN})")
            for wh_note, wh_w, wh_b in wh_p:
                print(f"   bar {wh_b + 1}: the pipe sings {wh_note} across, {wh_w:.3f} m ; its whistles fall towards {SOUND / wh_w:.1f} Hz ; heard 5 / 20 / 50 / 100 / 200 / 400 ms into the first: " + " ".join(f"{whistle_heard(wh_w, 1, x / 1000):.0f}" for x in (5, 20, 50, 100, 200, 400)) + " Hz ; into the third: " + " ".join(f"{whistle_heard(wh_w, 3, x / 1000):.0f}" for x in (5, 20, 50, 100, 200, 400)) + " ; loudest " + " / ".join((lambda arr: f"{1000 * (max(arr, key=lambda z: z[1])[0] - n_ * whistle_far() / SOUND):.0f} ms in at {whistle_heard(wh_w, n_, max(arr, key=lambda z: z[1])[0] - n_ * whistle_far() / SOUND):.0f} Hz")(whistle_arrivals(wh_w, n_, (BEATS if wh_b != wh_p[-1][2] else BEATS - CLICK_STEP * STEP) * 60 / BPM)[1:]) for n_ in range(1, WHISTLE_ECHOES + 1)))
        if NEXTROOM:
            nx_b0, nx_b1 = nextroom_span(); nx_hz = [NEXTROOM_MAINS * nx_k for nx_k in NEXTROOM_PARTS]; nx_bar = BEATS * 60 / BPM
            print(f"the building across the square hums, bars {nx_b0 + 1}-{nx_b1} ({int(nx_b0 * nx_bar) // 60}:{nx_b0 * nx_bar % 60:04.1f}-{int(nx_b1 * nx_bar) // 60}:{nx_b1 * nx_bar % 60:04.1f}): mains of {NEXTROOM_MAINS:g} to the second, heard through its wall at " + " and ".join(f"{nx_f:g} Hz ({-NEXTROOM_WALL * math.log2(nx_f / nx_hz[0]):+.1f} dB)" for nx_f in nx_hz) + f" (a wall keeps {NEXTROOM_WALL:g} dB an octave) ; one held voice, {NEXTROOM_GAIN} at the nearest ; it grows as 1 over the distance")
            print("   bar: metres to the next wall, dB under the nearest: " + " ; ".join(f"{b + 1}: {nextroom_metres(b):.0f} m {nextroom_db(b):+.1f}" for b in range(nx_b0, nx_b1, 2)) + f" ; the end of bar {nx_b1}: {nextroom_metres(nx_b1):.1f} m +0.0")
        if FLY:
            print(f"a fourth, a fifth, an octave go by: left to right, {FLY_DIST:g} m in front at the nearest, {FLY_RADIUS:g} m out to each side ({FLY_GAIN}) ; heard f(1 + v/c) coming and f(1 - v/c) going")
            for (n, heard, bar), (_, v, T, ratio, f0, f_in, f_out, tc, rate, ph) in zip(FLY_PASSES, fly_facts()):
                print(f"   nearest on the line of bar {bar + 1} ({int(tc) // 60}:{tc % 60:04.1f}): 1/{n} of the speed of sound, {v:.1f} m/s ({v * 3.6:.0f} km/h; raised {100 * (v * n / SOUND - 1):.1f}% for the line's ends) ; on the line {T * 1000:.0f} ms ({T * BPM / 60:.2f} beats) ; it sings {f0:.1f} Hz ; heard {f_in:.1f} Hz ({heard}) coming, {f_out:.1f} Hz going ({n + 1}/{n - 1}: {1200 * math.log2(f_in / f_out):.0f} cents)")
        if bird_span():
            b0, b1 = bird_span(); sec = BEATS * 60 / BPM; v, near, far, cents, lv = bird_facts(); ns = bird_notes()
            print(f"a bird in the hangar, bars {b0 + 1}-{b1} ({int(b0 * sec) // 60}:{b0 * sec % 60:04.1f}-{int(b1 * sec) // 60}:{b1 * sec % 60:04.1f}): a circle of {BIRD_RADIUS:g} m, its centre {BIRD_AHEAD:g} m in front ; once round every {BIRD_LAP} bars ({1 / bird_rate():.2f} s, {v:.1f} m/s) ; {near:g} m away at the nearest, {far:g} m at the farthest ({lv:.1f} dB between) ; the pitch moves {cents:.0f} cents each way at the most ; {len(ns) // len(BIRD_CALL)} calls, one every {BIRD_EVERY} sixteenths, " + " then ".join(c[0] for c in BIRD_CALL) + f" ; {BIRD_GAIN}, {BIRD_AIR} of it to the air")
        if ball_notes():
            fl = ball_flights(); beat = 60 / BPM
            print(f"Zeno's ball: let fall {len(BALL_RESTS)} times from {100 * ball_height():.0f} cm ; a bounce keeps {BALL_E:.4f} of the speed ({20 * math.log10(BALL_E):.2f} dB) ; first flight {1000 * fl[0][1]:.1f} ms, {len(fl)} bounces sounded (to flights of {1000 * fl[-1][1]:.1f} ms, {fl[-1][2]:.1f} dB), all the flights together {BALL_BEATS * beat:.3f} s ({BALL_BEATS:g} beats) ; {BALL_NOTE}, {BALL_GAIN}")
            print("   it comes to rest on the line of bar: " + " ".join(f"{r + 1} ({int(r * sec) // 60}:{r * sec % 60:04.1f}, {next(nm for nm, b0, n, *_ in SECS if b0 <= r - 1 < b0 + n)})" for r in BALL_RESTS))
            print("   one fall, each bounce in sixteenths from the bar line two bars before rest: " + " ".join(f"{(2 * BEATS - BALL_BEATS + t / beat) / STEP:.2f}" for t, f, db in fl))
        if flut_span():
            b0, b1 = flut_span(); r = flut_rings(); ms = lambda w: 2000 * w * FLUT_WIDE / SOUND
            print(f"the corridor's other two walls, bars {b0 + 1}-{b1}: {FLUT_WIDE:.3f} m apart ({FLUT_NOTE}, {FLUT_HZ} Hz: across and back in {1000 / FLUT_HZ:.2f} ms) ; {len(r)} rings ; in the middle for bars {b0 + 1}-{b0 + FLUT_STILL}, then to a wall and back every {FLUT_TURN // 2} bars")
            print("   bar: metres from the left wall, the left wall's click after ms, the right wall's after ms (at the click): " + " ; ".join(f"{int(at // BEATS) + 1}: {w * FLUT_WIDE:.2f}, {ms(w):.2f}, {ms(1 - w):.2f}" for at, v, w in r[::FLUT_RETURNS + 1]))
        if TRIM:
            print("the click's repair: " + ", ".join(f"{g:+g} dB at {f:.0f} Hz (q {q:g})" for f, g, q in TRIM_CUTS) + f" ; coming in over bars {TRIM_IN[0] + 1}-{TRIM_IN[1]}, whole in bars {TRIM_IN[1] + 1}-{TRIM_OUT[0]}, going out over bars {TRIM_OUT[0] + 1}-{TRIM_OUT[1]}")
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
        if crowd_times():
            t_app, t_pull, t_full, t_end = crowd_times(); n = len(CROWD_ROWS) * len(CROWD_PANS)
            print(f"the room claps, bars {int(t_app // BEATS) + 1}-{int(t_end // BEATS)}: {n} people, {len(CROWD_PANS)} across and {len(CROWD_ROWS)} rows back ({', '.join(f'{r:g} m: {1000 * r / SOUND:.0f} ms late, {20 * math.log10(CROWD_ROWS[0] / r):+.0f} dB' for r in CROWD_ROWS)}) ; applause from bar {int(t_app // BEATS) + 1}, the pull from bar {int(t_pull // BEATS) + 1}, full from bar {int(t_full // BEATS) + 1} ; {len(crowd_claps())} claps")
            print("   bar: claps, in step (0 nobody, 1 one clap), spread about the beat: " + " ; ".join(f"{b + 1}: {c}, {r:.2f}, {sd:.0f} ms" for b in range(int(t_app // BEATS), int(t_end // BEATS)) for c, r, sd in [crowd_step(b)]))
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
