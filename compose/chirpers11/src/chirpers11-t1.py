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

v17 (27 Nov): THE CLOCK WAS RUNNING ALL ALONG (C11T1_CLOCK_END=0 takes it out: v16). The wall clock of "no ruler"
did not stop when the music came back; it was only covered. In the song's last four bars, when the hat has gone
and deck B's record has run down and stopped, it is there again: a tick at every whole second from 271 to 278,
eight of them, on the pallet it would be on had it never stopped (the odd seconds tick, the even ones tock, as
at 93). The record's time ran down; the wall's did not. In the album these four bars lie under the first four
of Least Common (chirper-one agreed, 06:03 and 06:32): at 126 to the minute the eight ticks fall on its beats
0.06 2.16 4.26 6.36 8.46 10.56 12.66 14.76, the last 0.59 s before its bar 5: a clock that takes no notice of
three, five and seven either. It has its own two tracks and its own fader: an ending is bare, and the master
lifts whatever is left in it.

v18 (27 Nov): THE CLOCK STRIKES THE MINUTES (C11T1_CHIME=0 takes it out: v17). The clock on the wall has a
bell. At one minute into the song it strikes once; at two minutes twice; at three, three times; at four,
four: ten strokes in all, a second apart, as a clock strikes. The arithmetic is the song's: at 124 to the
minute a minute is 124 beats, thirty-one bars exactly, so every minute of this song begins on a bar line
(bars 32, 63, 94 and 125) and the first stroke of each hour, so to say, is on the one. But the clock counts
seconds, and a second is two beats and a fifteenth: every next stroke is a thirty-first of a second (32 ms)
further behind the beat it follows: 32, 65, 97 ms: the record gains on the clock as it always has. A
listener with a watch can check it: the song tells its own time. One bell (`gt-chime`: a struck bar's three
partials on F6), on the wall where the clock is (to the right, a little of the room).

v19 (27 Nov): THE PIPS (C11T1_PIPS=0 takes them out: v18). The clock strikes the minutes; now it counts
them in, as the time signal on the radio does: a short pip of 1000 Hz on each of the five seconds before
a whole minute and a long one that BEGINS on the minute. A second is two beats and a fifteenth, so the
pips are not on the beat: they fall 161, 129, 97, 65 and 32 ms BEFORE every other beat, closing on it,
and the long one is on the bar line exactly, with the bell's first stroke. Then the bell's strokes fall
behind the beat again, 32 ms more each time. The clock and the beat agree once a minute, for an instant,
and the pips are heard arriving at it. 1000 Hz is a standard and in no key (21 cents over B5).

v20 (27 Nov): A SCRATCH ACROSS DECK B'S RECORD (C11T1_SCAR=0 takes it out: v19). The song has a clock on
the wall, which ticks once a second whatever the decks do. Now the record has one too: a scratch straight
across it, from the edge to the label, which the needle meets once in every turn: a small tick every 15
sixteenths OF THE RECORD. It is written on the record like deck B's other parts, so it goes through
everything the record goes through and tells it: 15 against deck A's 16 when the hand is off (a sixteenth
earlier every bar), early and late with the hand, twice over and eight times over in the stretch, once
more going backwards in the spin back, every 11 1/4 sixteenths at the other speed. Two things it does
NOT do are as true: while the needle is stuck everything else on the record comes round again and the
tick alone goes on as it did (it was once a turn already); and in the loop the needle never gets to it.
The scratch is half a sixteenth after where the needle is on the first beat of "locked": between two of
deck B's sixteenths, where nothing else on the record is. When the motor is switched off the needle meets it once more, 44 ms late and a little low, and
never again: the platter stops three and a half sixteenths of the record short of it.

v21 (27 Nov): THE CLOCK CHIMES THE QUARTERS (C11T1_QUART=0 takes it out: v20). The clock on the wall
ticks the seconds, strikes the minutes and gives the pips. A clock that strikes has a tune for the
quarters: the Westminster quarters, FIVE CHANGES ON FOUR BELLS (here D C B flat F: all four are in the
song's G minor, and the bell that strikes the minutes is the lowest of them an octave up), taken in
order: one change at a quarter past, two at the half, three at a quarter to. The whole minute's four
are not rung: the minute belongs to the pips and the strokes. So every fifteen seconds of the song,
which is seven and three quarter bars and never the same place in a bar twice, the clock rings 4, 8 or
12 notes, half a second apart: its own time, a beat and a thirtieth of the decks'. The tune is nearly
in time with the music and never is, and falls a little further behind it with every note. How far
through a minute the song is can now be told from how many changes are rung, as the minute can from the
strokes. Nothing is rung in the last four bars: there the clock only ticks.

v22 (27 Nov): TWO DECKS CROSS (C11T1_CANON=0 takes it out: v21). The song has had one record at five
speeds, each fixed (v12: a canon by proportion). Here the speed itself is what moves. For four bars of
"both" (82 to 85, the row that had nothing of its own) two more decks have deck B's record. One starts
at half speed, an octave down, on the left, and is wound up steadily (a straight line in pitch: its
speed doubles every two bars) to double speed, an octave up, on the right. The other does exactly the
reverse. So one accelerates as the other slows, one rises as the other falls, one walks right as the
other walks left; and because the needles are set so, they are on the SAME beat of the record at the
moment their speeds are the same: the first beat of bar 84, where both are at the record's own speed
and pitch, in the middle, and on the grid. Before it and after it they are never together: the same
beat of the record is 46 ms apart on the two decks a beat either side of the crossing, and 204 ms (a
sixteenth and two thirds) two beats either side. It is Nancarrow's Canon X (Study 21),
done as a record does it: pitch and tempo are one thing.

v23 (27 Nov): THE HOLE IS OFF CENTRE (C11T1_WOW=0 takes it out: v22). A record whose hole is not in
the middle of its grooves goes under the needle faster on one side of every turn and slower on the
other: its pitch goes up and down once a turn (wow). Deck B's hole is 1 mm off, with the needle
80 mm out: 1.25% each way, 21.5 cents sharp and then as flat. On the record's ticks and stabs nobody
would know; so in the first row of "locked" (bars 113 to 120), where no hand is on the record, a
chord is HELD on it (an organ of plain tones: the stab's chords, a bar of the record each), and the
record's pitch lane, which every part of deck B follows, is given the wow. It is sharpest when the
scratch (v20) comes under the needle: the tick marks the turn. For four bars a turn is 1.81 s; at
bar 117 the switch goes to the other speed, the chord jumps a fourth with everything else on the
record, and the wow goes four turns for three (1.36 s). The record's strokes are NOT moved in time
(the wow is 3.6 ms each way there: not written).

v24 (27 Nov): THE RECORD IS STARTED (C11T1_UP=0 takes it out: v23). The song ends with deck B's
motor switched off and its platter running down for two bars. It now begins the other way: half
a sixteenth after the first bass drum the motor goes ON, in the headphone (the left ear, where the
cue is heard from bar 3), and the platter takes the same two bars to come up. Its speed rises in
a straight line, so the record has turned t squared over 16 beats after t beats, and its
sixteenth clicks come by at t = 2 times the square root of 1, 2, 3 ... 15: each sooner after the
last, and the sixteenth is the cue's first stroke. Every click is the same click (the same steps
of a shift register) played at the speed the platter has at that instant: at a quarter speed two
octaves down and four times as long, and quieter in proportion (a cartridge's voltage follows the
groove's speed). The headphone does not slow down: its small speaker passes nothing under
1.8 kHz at any speed, so the slowest clicks are thin.

v25 (27 Nov): THE TWO RECORDS BEAT (C11T1_BEAT=0 takes it out: v24). Two copies of one record on
two decks, and on both a held tone. Deck A's is steady; deck B's turns with its platter, so
when the hand pushes deck B ahead its tone runs sharp and gets ahead of deck A's wave by wave.
A whole number of waves apart the two tones add; half a wave off they cancel. So the sum throbs
once for every wave of drift, and the throbs can be counted: the tone is 64 waves to the beat
(132.27 Hz), so each throb is a 64th of a beat, 7.56 ms. In the first row of "the nudge" (bars
97 to 104) the hand pushes deck B a quarter of a beat ahead and lets it come back, twice: 16
throbs out and 16 back each time: slow as the push begins, quickest as the record runs fastest,
and STILL at the top, where the decks are furthest apart and for a moment at one speed. It is
the song's drift made into something you can count; no click is added.

v26 (27 Nov): GIVE OR TAKE A SECOND (C11T1_LEAP=0 takes it out: v25). The song has a clock on
the wall that strikes the minutes, chimes the quarters and gives the pips, all in seconds
against the record's beats. Now and then the world's clocks are given a second, because the
Earth is not as good a clock as an atom: the last minute of that day has 61 seconds, the clock
reads 23:59:60, and the time signal has SEVEN pips where it always has six. Here the third
minute is given a second (seven pips, in "the stretch", where the drum rests and they can be
counted), and for a minute the clock's strokes and quarters are a second late against the
record; the fourth minute has a second taken (59 seconds, five pips: the signal that has been
laid down for it and never yet sent), and the clock is right again for the end. One pip more,
one pip fewer, and a minute of the clock moved by a second. Nothing else is touched.

v27 (27 Nov): THE GRID IS FOUND (C11T1_SWING=0 takes it out: v26). The first section is
called the grid, and until now the grid was simply there. Now the record's hat comes in (bar 9)
swung hard, and is set straight a step at a time, two bars a step: in every pair of its
sixteenths the long one stands to the short one as 3 to 1, then 2 to 1, then 3 to 2, then
1 to 1. Those are the ratios of a twelfth, an octave, a fifth and a unison: a rhythm is an
interval slowed down, and the swing is tuned down to the unison. The off stroke is late by an
eighth, a twelfth, a twentieth of a beat (60.5, 40.3, 24.2 ms) and then by nothing; when it is
straight the record's tock comes in (bar 17) and the song is about two decks. Nothing is added;
no stroke on a beat or an off beat moves.

v28 (27 Nov): THE STROBE (C11T1_STROBE=0 takes it out: v27). A turntable has a ring of dots
round the platter and a lamp beside it that flashes in time. When the record runs true the
dots stand still; when it gains they creep forward; when it loses they creep back: you read
the speed with your eye. Here you read it with your ear. In the first row of "take" a lamp
flashes on every beat of the grid, and the dots are notes: the note under the lamp is how far
deck B's record is from the grid at that instant, a note of the scale (G Bb C D F) for every
fiftieth of a beat (9.7 ms). G3 is the dot on its mark. The hand's breath in "take" (a bar
ahead, a bar behind, 0.08 of a beat at the furthest) is heard as a broken chord: up to F4 and
back while the record gains, down to Bb2 and back while it loses, and home on every bar line.
In the next row deck B's own bass drum comes in and the same drift is heard as a flam.

v29 (27 Nov): GIVE OR TAKE A NOTE (C11T1_GIVE=0 takes it out: v28). A tune of eight notes
is given a note at a time: its first note; its first two; its first three; until it is
whole. Then it is taken a note at a time from the front: without its first; without its
first two; until only its last note is left. That is 36 notes and 28: 64, eight squared:
one row of eighths, to the note (the second row of "both"). The tune's first note comes
round later and later (on the triangular numbers: 1, 2, 3 ... 7 eighths apart) and its
last note sooner and sooner (7, 6, 5 ... 1 apart): time given, and time taken. The
process is Rzewski's "Les Moutons de Panurge" (1969).

v30 (28 Nov): HALF-LIFE (C11T1_LIFE=0 takes it out: v29). A low string (D2) is struck
every two bars in the second row of "the nudge". Its first tone is half as loud a bar
later; its second after half a bar; its third after a third of a bar; its fourth after
a quarter: the nth tone halves n times as fast. Nothing ticks and nothing counts: every
tone is a clock that runs down, and the string's colour says how long ago it was
struck.

v31 (28 Nov): TIME'S ARROW (C11T1_ARROW=0 takes it out: v30). The string of HALF-LIFE
is heard before it is struck: bars 93 to 96 are the film of bars 105 to 108 run
backwards about the first beat of bar 101. It grows out of nothing, the low tone
first and slowly, the upper ones later and faster, and stops dead where the stroke
was: an eighth of a beat before the drum comes back.

v32 (28 Nov): A BEAT BECOMES A NOTE (C11T1_FUSE=0 takes it out: v31). In bars 89 to 92
one wave of a low tone sounds once a beat; then twice, 4, 8, 16 and 32 times a beat.
At 32 a beat the waves stand end to end and are one held note: 66.13 Hz, the tempo
times 32. Then it comes apart the same way. Nothing changes but how often.

v33 (28 Nov): THE TUNE AND ITS RHYTHM GO ROUND AT DIFFERENT SPEEDS (C11T1_TALEA=0 takes it
out: v32). In bars 9 to 16 the song's tune of eight notes is played to a rhythm of five
notes a bar (3 3 4 3 3 sixteenths). The rhythm goes round 8 times and the tune 5 times in
40 notes; they begin together only at the row's two ends. No bar is like another; every
note of the tune is heard once in each of the bar's five places.

v34 (28 Nov): ONE RHYTHM AT THREE SPEEDS, AND THEY NEVER DISAGREE (C11T1_FAIR=0 takes it
out: v33). The fair way to take turns (give, take, take, give, take, give, give, take: Thue
and Morse's sequence) as a rhythm on the sixteenths of bars 113 to 120. Every second place
of it is the same rhythm at half the speed, every fourth at a quarter: three voices play it
at the three speeds, the slower the lower, and a slower one never strikes where a faster
one rests.

v35 (28 Nov): THE BEAT THAT SPEEDS UP FOR EVER (C11T1_FASTER=0 takes it out: v34). In bars
121 to 128 a pip is struck faster and faster: twice as fast after every two bars, and after
every two bars exactly where it began. Four beats at once, each twice as fast as the one
below, all speeding up alike; the fastest fades out and a new slowest fades in under it
(Risset's rhythm: the stair without end, made of time).

v36 (28 Nov): THE BEAT THAT SLOWS FOR EVER (C11T1_SLOWER=0 takes it out: v35). In bars 129
to 136 every pip of bars 121 to 128 is played again, turned round about the line between the
two rows: as far after it as it was before it. What sped up for ever slows for ever. It is
the row in which the record is switched off and runs down: the record stops; this does not.

v37 (28 Nov): GIVE OR TAKE THIRTY MILLISECONDS (C11T1_SHRINK=0 takes it out: v36). In bars 49 to
56, where there is no ruler, three clicks, twice a bar. The first and the last are always the
same time apart; the middle one is in the middle, then 30 ms early, then 30 ms late, then
early and late side by side.

v38 (28 Nov): CHANCE COMES IN CLUMPS (C11T1_CHANCE=0 takes it out: v37). In bars 57 to 64
eight pips to two bars, on the sixteenths, four times: spread by the golden ratio, thrown
by chance, spread, thrown. The throw's seed was written before the throw was seen.

v39 (28 Nov): FIVE AGAINST SEVEN (C11T1_POLY=0 takes it out: v38). In bars 17 to 24 a wooden
stroke five times a bar, evenly, and another seven times a bar, evenly: the five alone for two
bars, both for four, the seven alone for two. They agree on the first beat and nowhere else;
twice a bar they are a thirty-fifth of a bar apart; and a bar's strokes read the same
backwards. The song's own five, the tock's, is on the grid: it is this five rounded down.
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


def arrow_mirror():
    """The beat about which time is turned: ARROW_GAP bars before the string's row; or None."""
    return (life_row() - ARROW_GAP) * BEATS if ARROW and life_row() is not None else None


def arrow_ends():
    """The beats at which the turned string stops dead: each of the string's first ARROW_STROKES strokes, as far before the mirror as the stroke is after it; the earliest first."""
    return sorted(2 * arrow_mirror() - t for t in life_strokes()[:ARROW_STROKES])


def arrow_lane(n):
    """The nth tone's level by time, as a lane in dB: the string's lane (life_lane) turned round about the mirror: 6.0206 n dB MORE for every LIFE_HALF beats, in a straight line, to nothing off where it stops."""
    low = round(-6.0206 * n * (LIFE_EVERY - 0.001) / LIFE_HALF, 4); pts = [["0b", low]]
    for e in arrow_ends():
        pts += [[f"{e - LIFE_EVERY + 0.001:g}b", low], [f"{e:g}b", 0.0]]
    return {"points": pts + [[f"{BARS * BEATS}b", 0.0]], "curve": 0}


def faster_row():
    """The first bar (from 0) of the row in which a beat speeds up for ever, or None."""
    sec = next((x for x in SECS if x[0] == FASTER_IN[0]), None)
    return sec[1] + ROW * FASTER_IN[1] if FASTER and sec is not None and FASTER_IN[1] * ROW < sec[2] else None


def faster_strokes():
    """[(turn, stroke of the fastest beat (from 0), beat of the song, loudness 0 to 1, the beats it is a stroke of (0 the slowest))].
    Through a turn of T beats the kth beat's speed is r 2^(k + t/T) strokes a beat, with r T = FASTER_N ln 2, so its jth stroke falls at T log2(1 + j / (FASTER_N 2^k)).
    A beat's loudness is half of 1 less the cosine of a whole turn over all the beats: nothing at the slowest speed of the slowest and the fastest of the fastest, and they add to the same at every moment."""
    out = []; M = FASTER_N * 2 ** (FASTER_LAYERS - 1)
    for turn in range(ROW * BEATS // FASTER_TURN):
        for j in range(M):
            x = math.log2(1 + j / M); ks = tuple(k for k in range(FASTER_LAYERS) if j % 2 ** (FASTER_LAYERS - 1 - k) == 0)
            amp = sum(0.5 * (1 - math.cos(2 * math.pi * (k + x) / FASTER_LAYERS)) for k in ks) / (FASTER_LAYERS / 2)
            if amp > 0 and 20 * math.log10(amp) >= FASTER_FLOOR:
                out.append((turn, j, faster_row() * BEATS + FASTER_FROM + (turn + x) * FASTER_TURN, amp, ks))
    return out


def poly_row():
    """The first bar (from 0) of the row of five against seven, or None."""
    sec = next((x for x in SECS if x[0] == POLY_IN[0]), None)
    return sec[1] + ROW * POLY_IN[1] if POLY and sec is not None and POLY_IN[1] * ROW < sec[2] else None


def poly_hz(p):
    """Hz of a note name (A4 = 440)."""
    n = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[p[0]] + (1 if "#" in p else -1 if "b" in p[1:] else 0)
    return 440.0 * 2 ** ((n + 12 * (int(p[-1]) + 1) - 69) / 12)


def poly_strokes():
    """[(voice 0 the five / 1 the seven, bar of the row from 0, place in the bar from 0, beat of the song, dB it is turned down)]."""
    from fractions import Fraction as Fr
    b0 = poly_row() * BEATS; both = {Fr(k, POLY_N[0]) for k in range(POLY_N[0])} | {Fr(k, POLY_N[1]) for k in range(POLY_N[1])}
    assert {(1 - t) % 1 for t in both} == both and len(both) == sum(POLY_N) - 1          # read backwards from the next bar line the bar is the same; they agree once
    assert [16 * k // POLY_N[0] for k in range(POLY_N[0])] == FIVE and all(len(POLY_TRIM[v]) == POLY_N[v] for v in (0, 1))   # the song's five is the even five rounded down to the grid
    return [(v, j, k, b0 + j * BEATS + k * BEATS / POLY_N[v], POLY_FALL * k if j == ROW - 1 else 0.0) for v in (0, 1) for j in range(*POLY_BARS[v]) for k in range(POLY_N[v])]


def chance_row():
    """The first bar (from 0) of the row in which chance comes in clumps, or None."""
    sec = next((x for x in SECS if x[0] == CHANCE_IN[0]), None)
    return sec[1] + ROW * CHANCE_IN[1] if CHANCE and sec is not None and CHANCE_IN[1] * ROW < sec[2] else None


def chance_phrases():
    """[(kind, sorted sixteenths)] for the phrases of CHANCE_ORDER. Spread: sixteenth floor(SLOTS frac(n g)), g the golden ratio less one, n going on from phrase to phrase. Chance: a shuffle by the generator of CHANCE_SEED, going on from phrase to phrase."""
    g = (5 ** 0.5 - 1) / 2; x = CHANCE_SEED; n = 0; out = []
    for kind in CHANCE_ORDER:
        if kind == "spread":
            sl = [int(CHANCE_SLOTS * ((k * g) % 1)) for k in range(n, n + CHANCE_N)]; n += CHANCE_N
        else:
            pool = list(range(CHANCE_SLOTS)); sl = []
            for i in range(CHANCE_N):
                x = (1664525 * x + 1013904223) % 2 ** 32; j = i + (x >> 16) % (CHANCE_SLOTS - i); pool[i], pool[j] = pool[j], pool[i]; sl.append(pool[i])
        assert len(set(sl)) == CHANCE_N, sl
        out.append((kind, sorted(sl)))
    return out


def chance_pips():
    """[(pip from 0 in time, beat of the song, phrase from 0)]."""
    b0 = chance_row() * BEATS; per = CHANCE_SLOTS / 4; assert per * len(CHANCE_ORDER) == ROW * BEATS and len(CHANCE_TRIM) == CHANCE_N * len(CHANCE_ORDER)
    return [(p * CHANCE_N + q, b0 + p * per + sl / 4, p) for p, (_, sls) in enumerate(chance_phrases()) for q, sl in enumerate(sls)]


def chance_hz():
    """Hz of CHANCE_NOTE (a letter, an optional b, an octave; A4 is 440)."""
    semi = {"C": -9, "D": -7, "E": -5, "F": -4, "G": -2, "A": 0, "B": 2}[CHANCE_NOTE[0]] - (1 if "b" in CHANCE_NOTE[1:] else 0)
    return 440 * 2 ** ((semi + 12 * (int(CHANCE_NOTE[-1]) - 4)) / 12)


def chance_stats(sls):
    """(pairs side by side, the longest silence in sixteenths from one pip to the next) of a phrase's sorted sixteenths."""
    gaps = [b - a for a, b in zip(sls, sls[1:])]; return sum(1 for d in gaps if d == 1), max(gaps)


def shrink_row():
    """The first bar (from 0) of the row with the three clicks, or None."""
    sec = next((x for x in SECS if x[0] == SHRINK_IN[0]), None)
    return sec[1] + ROW * SHRINK_IN[1] if SHRINK and sec is not None and SHRINK_IN[1] * ROW < sec[2] else None


def shrink_clicks():
    """[(click from 0, beat of the song, triple from 0, place in the triple 0 1 2, the triple's kind)]: len(SHRINK_AT) triples a bar for ROW bars."""
    b0 = shrink_row() * BEATS; n = len(SHRINK_AT); assert len(SHRINK_ORDER) == ROW * n and len(SHRINK_TRIM) == 3 * ROW * n; out = []
    for j, kind in enumerate(SHRINK_ORDER):
        t0 = b0 + (j // n) * BEATS + SHRINK_AT[j % n]
        for q, dt in enumerate((0, SHRINK_MID[kind], SHRINK_SPAN)): out.append((3 * j + q, t0 + dt, j, q, kind))
    return out


def slower_row():
    """The first bar (from 0) of the row in which the beat slows for ever (the row after the one in which it speeds up), or None."""
    return faster_row() + ROW if SLOWER and faster_row() is not None and faster_row() + 2 * ROW <= BARS else None


def slower_strokes():
    """faster_strokes() turned round about the line between the two rows, in the order they are played: [(turn (0 the first played), stroke of the fastest beat, beat of the song the pip BEGINS on, loudness 0 to 1, the beats it is a stroke of)].
    A pip that began t beats before the line and lasted L ends t beats after it: it begins on line + t - L."""
    line = slower_row() * BEATS; ln = FASTER_MS / 1000 * BPM / 60; nt = ROW * BEATS // FASTER_TURN
    return sorted(((nt - 1 - turn, j, 2 * line - t - ln, amp, ks) for turn, j, t, amp, ks in faster_strokes()), key=lambda r: r[2])


def fair_row():
    """The first bar (from 0) of the row in which one rhythm goes at three speeds, or None."""
    sec = next((x for x in SECS if x[0] == FAIR_IN[0]), None)
    return sec[1] + ROW * FAIR_IN[1] if FAIR and sec is not None and FAIR_IN[1] * ROW < sec[2] else None


def fair_struck(n):
    """Is place n struck: has n, written in twos, an even number of ones?"""
    return bin(n).count("1") % 2 == 0


def fair_strokes():
    """[(beat, voice (from 0), the voice's place n, the sixteenth of the bar)]: every voice plays the one rhythm at its own speed through the row."""
    return [(fair_row() * BEATS + n * st / 4, j, n, n * st % (4 * BEATS)) for j, st in enumerate(FAIR_STEPS) for n in range(ROW * BEATS * 4 // st) if fair_struck(n)]


def talea_row():
    """The first bar (from 0) of the row in which the tune and its rhythm go round, or None."""
    sec = next((x for x in SECS if x[0] == TALEA_IN[0]), None)
    return sec[1] + ROW * TALEA_IN[1] if TALEA and sec is not None and TALEA_IN[1] * ROW < sec[2] else None


def talea_notes():
    """[(beat it begins, beats to the next, note, place in the rhythm (from 0), place in the tune (from 0))]: ROW bars of the rhythm."""
    assert sum(TALEA_STEPS) == 4 * BEATS
    out = []; at = 0
    for k in range(ROW * len(TALEA_STEPS)):
        st = TALEA_STEPS[k % len(TALEA_STEPS)]
        out.append((talea_row() * BEATS + at / 4, st / 4, TALEA_TUNE[k % len(TALEA_TUNE)], k % len(TALEA_STEPS), k % len(TALEA_TUNE))); at += st
    return out


def fuse_row():
    """The first bar (from 0) of the bars in which a beat becomes a note, or None."""
    sec = next((x for x in SECS if x[0] == FUSE_IN[0]), None)
    return sec[1] + ROW * FUSE_IN[1] if FUSE and sec is not None and FUSE_IN[1] * ROW < sec[2] else None


def fuse_waves():
    """[(the beat a wave begins, how many a beat there are just then)]: every wave, in order."""
    out = []; t = fuse_row() * BEATS
    for rate, beats in FUSE_STEPS:
        out += [(t + k / rate, rate) for k in range(rate * beats)]; t += beats
    return out


def life_row():
    """The first bar (from 0) of the row with the string that runs down, or None."""
    sec = next((x for x in SECS if x[0] == LIFE_IN[0]), None)
    return sec[1] + ROW * LIFE_IN[1] if LIFE and sec is not None and LIFE_IN[1] * ROW < sec[2] else None


def life_strokes():
    """The beats of the strokes: every LIFE_EVERY beats from LIFE_AT of the row."""
    return [life_row() * BEATS + LIFE_AT + k * LIFE_EVERY for k in range(ROW * BEATS // LIFE_EVERY)]


def life_lane(n):
    """The nth tone's level by time, as a lane in dB: nothing off at a stroke, then 6.0206 n dB less for every LIFE_HALF beats, in a straight line (dB by time: a half-life), back to nothing off at the next stroke."""
    pts = [["0b", 0.0]]
    for t in life_strokes():
        pts += [[f"{t:g}b", 0.0], [f"{t + LIFE_EVERY - 0.001:g}b", round(-6.0206 * n * (LIFE_EVERY - 0.001) / LIFE_HALF, 4)]]
    return {"points": pts + [[f"{BARS * BEATS}b", 0.0]], "curve": 0}


def give_row():
    """The first bar (from 0) of the row in which a tune is given and taken a note at a time, or None."""
    sec = next((x for x in SECS if x[0] == GIVE_IN[0]), None)
    return sec[1] + ROW * GIVE_IN[1] if GIVE and sec is not None and GIVE_IN[1] * ROW < sec[2] else None


def give_passes():
    """The passes, each a list of places in the tune (from 0): first 1 note, then 2, ... then all n (the giving); then all but the first, all but the first two, ... the last alone (the taking)."""
    n = len(GIVE_TUNE)
    out = [list(range(k)) for k in range(1, n + 1)] + [list(range(j, n)) for j in range(1, n)]
    assert sum(len(p) for p in out) == n * n and n * n * GIVE_STEP == ROW * BEATS, (n, GIVE_STEP)
    return out


def give_notes():
    """[(beat, note, place in the tune, pass, whether the pass is of the giving)], one every GIVE_STEP beats from GIVE_AT of the row."""
    out, k = [], 0
    for q, ps in enumerate(give_passes()):
        for j in ps:
            out.append((give_row() * BEATS + GIVE_AT + k * GIVE_STEP, GIVE_TUNE[j], j, q, q < len(GIVE_TUNE))); k += 1
    return out


def strobe_row():
    """The first bar (from 0) of the row with the strobe, or None."""
    sec = next((x for x in SECS if x[0] == STROBE_IN[0]), None)
    return sec[1] + ROW * STROBE_IN[1] if STROBE and sec is not None and STROBE_IN[1] * ROW < sec[2] else None


def strobe_pitch(dots):
    """The note of the dot that is `dots` dots ahead of the mark (behind, if negative)."""
    m = STROBE_HOME + 12 * (dots // len(STROBE_SCALE)) + STROBE_SCALE[dots % len(STROBE_SCALE)]
    return ("C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B")[m % 12] + str(m // 12 - 1)


def strobe_notes():
    """[(grid beat, dots, note)]: a flash on every beat of the row; the dots are how far deck B's record is ahead of the grid at the flash (d), to the nearest dot."""
    out = []
    for j in range(ROW * BEATS):
        t = strobe_row() * BEATS + j + STROBE_AT
        dots = int(round(d(t) * STROBE_DOTS))
        assert abs(d(t) * STROBE_DOTS - dots) < 0.49, (t, d(t) * STROBE_DOTS)       # no flash falls just half way between two dots
        out.append((t, dots, strobe_pitch(dots)))
    return out


def swing_bar():
    """The bar (from 0) where the hat's swing begins, or None."""
    at = 0
    for name, rows, _, _ in SECTIONS:
        if name == SWING_IN[0]:
            return at + SWING_IN[1] * ROW if SWING else None
        at += rows * ROW
    return None


def swing_off(long, short):
    """Beats from an eighth's start to its off sixteenth when the pair stands long to short: the half of a beat shared out."""
    return 0.5 * long / (long + short)


def beat_row():
    """The first bar of the row in which the two records beat, or None."""
    sec = next((x for x in SECS if x[0] == BEAT_IN[0]), None)
    return sec[1] + ROW * BEAT_IN[1] if BEAT and sec is not None and BEAT_IN[1] * ROW < sec[2] else None


def beat_hz():
    return BEAT_WAVES * BPM / 60


def beat_off():
    """Semitones from the written note to the tone."""
    semi = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[BEAT_NOTE[0]] + (-1 if "b" in BEAT_NOTE[1:] else 0) + 12 * (int(BEAT_NOTE[-1]) + 1)
    return 12 * math.log2(beat_hz() / (440.0 * 2 ** ((semi - 69) / 12)))


def beat_apart(t):
    """Waves by which deck B's copy of the tone is ahead of deck A's at grid time t (beats): the decks' distance in waves, from the row's start."""
    return BEAT_WAVES * (d(t) - d(beat_row() * BEATS))


def beat_nulls(fine=512):
    """The grid times (beats) in the row at which the two tones are half a wave apart (they cancel), and the whole waves between them there."""
    b0 = beat_row() * BEATS
    out, last = [], math.cos(math.pi * beat_apart(b0))
    for i in range(1, ROW * BEATS * fine + 1):
        t = b0 + i / fine
        now = math.cos(math.pi * beat_apart(t))
        if (now > 0) != (last > 0):
            out.append((t - 0.5 / fine, math.floor(beat_apart(t - 0.5 / fine))))
        last = now
    return out


def up_span():
    """(the beat deck B's motor goes on, the beats its platter takes to come up), or None: it comes up into the cue's first stroke."""
    if not UP:
        return None
    w = UP_BARS * BEATS
    on = CUE_BARS[0] * BEATS + cue_err(0.0) - w
    return (on, w) if on >= 0 else None


def up_ticks():
    """One tuple a click of the record as it comes up: (its number from standstill, the beat it is heard on, the platter's speed then (1 = full), semitones, its length in beats, its velocity).
    The platter's speed rises in a straight line, as it falls in the stop: after t beats it is t / w and the record has turned t * t / (2 w) beats: its k-th sixteenth comes by at t = sqrt(2 w k / 4)."""
    on, w = up_span()
    out = []
    for k in range(1, int(round(w / 2 / STEP))):                # the last one is the cue's own first stroke
        t = math.sqrt(2 * w * k * STEP); sp = t / w
        out.append((k, on + t, sp, 12 * math.log2(sp), UP_LEN / sp, UP_VEL[k % len(UP_VEL)] * sp))
    return out


def wow_row():
    """The first bar of the row in which the hole is off centre, or None."""
    sec = next((x for x in SECS if x[0] == WOW_IN[0]), None)
    return sec[1] + ROW * WOW_IN[1] if WOW and sec is not None and WOW_IN[1] * ROW < sec[2] else None


def wow_rec(t):
    """The sixteenth of deck B's record under the needle at grid time t (beats), in and after 'locked' (the hand is off: the record is with the grid until the switch, then FAST_BY as fast)."""
    fw = fast_window()
    return t / STEP if not fw or t < fw[0] else (fw[0] + (min(t, fw[1]) - fw[0]) * FAST_BY + max(0.0, t - fw[1])) / STEP


def wow_turns(t):
    """Turns of the record since the scratch was under the needle (whole numbers: the scratch's tick)."""
    return (wow_rec(t) - scar_phase() - SCAR_OFF) / SCAR_TURN


def wow_st(t):
    """Semitones the off-centre hole makes the record sharp by at grid time t: 0.0 outside its row."""
    b0 = wow_row()
    if b0 is None or not b0 * BEATS <= t < (b0 + ROW) * BEATS:
        return 0.0
    return 12 * math.log2(1 + WOW_OFF / WOW_RADIUS * math.cos(2 * math.pi * wow_turns(t)))


def wow_notes():
    """The held chord on deck B's record in the wow's row: each bar OF THE RECORD its chord (the stab's), held for that bar; the record's bars are FAST_BY as short from the switch."""
    b0, fw, out = wow_row(), fast_window(), []
    t0, t1 = b0 * BEATS, (b0 + ROW) * BEATS
    cut = min(fw[0], t1) if fw else t1
    for bar in range(b0, int(cut // BEATS)):
        out += [note(bar * BEATS, p, BEATS, WOW_VEL) for p in CHORDS[(bar // 2) % len(CHORDS)]]
    if fw and fw[0] < t1:
        for i in range(int(math.ceil((t1 - fw[0]) / BEATS * FAST_BY - 1e-9))):
            at = fw[0] + i * BEATS / FAST_BY
            out += [note(at, p, min(BEATS / FAST_BY, t1 - at), WOW_VEL) for p in CHORDS[((int(fw[0] // BEATS) + i) // 2) % len(CHORDS)]]
    return out


def spd_lane():
    """Semitones a record on deck B is sharp or flat by, from its speed: one point a sixteenth, only where it moves."""
    pts, last, fine = [["0b", 0]], 0.0, False
    for i in range(int(TOTAL / STEP) + 1):
        t = i * STEP
        back = forced(t)                                     # a record's pitch is its speed, whichever way it turns, and whatever turns it
        v = round(12 * math.log2(max(speed(t) if back is None else back, 0.03)) + wow_st(t), 3)   # a stopped record has no pitch: the lane rests five octaves down (v23: + the wow, 0.0 everywhere but in its row)
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
CLOCK_END = os.environ.get("C11T1_CLOCK_END", "1") != "0" and CLOCK     # v17: the clock was running all along (it is heard again in the last bars)
CHIME = os.environ.get("C11T1_CHIME", "1") != "0" and CLOCK_END     # v18: the clock strikes the minutes
PIPS = os.environ.get("C11T1_PIPS", "1") != "0" and os.environ.get("C11T1_CHIME", "1") != "0" and CLOCK_END      # v19: the pips
SCAR = os.environ.get("C11T1_SCAR", "1") != "0" and PIPS  # v20: a scratch across deck B's record (the record's own clock: one tick a turn)
SCAR_TURN = STICK_TURN                                 # sixteenths of the record from one tick to the next: one turn of the platter (15: the turn that sticks)
SCAR_ON = "locked"                                     # the scratch is just after where the needle is on the first beat of this section
SCAR_OFF = 0.5                                         # sixteenths after that: BETWEEN two of deck B's sixteenths, where nothing else on the record is (on a sixteenth every tick fell with deck B's own click and was 2 to 5 dB under the music in its own 8 ms: an accent on the click, not a tick)
SCAR_WITH = "tock"                                     # it is heard wherever this part of deck B's is (the record in the room)
SCAR_NOTE = "C6"                                       # the tick: 1047 Hz and 3244 Hz, where this song has room (1 kHz +0.5, 3.1 kHz -2.3; 2.2 kHz is at the edge and is left alone)
SCAR_VEL = 0.9
SCAR_PAN = 0.1                                         # where the record's chord and its pop are
SCAR_GAIN = os.environ.get("C11T1_SCAR_GAIN", "-16dB") # set in the whole song's master, between two readings: here a tick is -20 to -33 dBFS in its own 8 ms (the song's own clicks are -14 to -26) and over what was in its gap by 4 to 15 dB in the middle of each section; at -20dB it was level with its gap
QUART = os.environ.get("C11T1_QUART", "1") != "0" and SCAR     # v21: the clock chimes the quarters
QUART_EVERY = 15                                       # seconds: a quarter of a minute
QUART_BELLS = {3: "D6", 2: "C6", 1: "Bb5", 5: "F5"}    # four more bells, by their place in the scale of B flat (the song's G minor has all four): the bell that strikes the minutes (F6) is the lowest of them an octave up
QUART_CHANGES = ((3, 2, 1, 5), (1, 3, 2, 5), (1, 2, 3, 1), (3, 1, 2, 5), (5, 2, 3, 1))   # the Westminster quarters: five changes on four bells
QUART_ORDER = {1: (0,), 2: (1, 2), 3: (3, 4, 0)}       # the changes rung at the first, second and third quarter: taken in order, round and round (the whole minute's four are not rung: the minute belongs to the pips and the strokes)
QUART_APART = 0.5                                      # seconds from note to note: the clock's own time, a beat and a thirtieth of the decks'
QUART_CHANGE = 3.0                                     # seconds from a change's first note to the next change's first: its fourth note is three times as long
QUART_HELD = (1.0, 2.0)                                # beats a note is held: the first three of a change, and its last
QUART_TRIM = {(1, 3): -3.0}                            # dB by (minute, quarter): set in the whole song's master, chime by chime. Twelve of the thirteen came out within 3 dB of one another untrimmed (their notes' medians -25.0 to -28.5 dBFS at -22dB); the one at 1:45 is in "no ruler", where the kick is out, and was -22.5
QUART_GAIN = os.environ.get("C11T1_QUART_GAIN", "-25dB")  # set in the whole song's master between two readings: at -22dB every note stood 5 to 43 dB (median 13) over the music in a band 12% wide round its own tone and the music under a chime was 0.05 to 0.12 dB down; at -28dB the median was 7 and two notes of the hundred were level with the music or under it. A tune needs every note. Written 9 dB under the strokes of the minute
CANON = os.environ.get("C11T1_CANON", "1") != "0" and QUART   # v22: two more decks with deck B's record, one winding up and one running down: they cross (a canon by acceleration: Nancarrow's Canon X)
CANON_IN = ("both", 2, 1, 5)                           # the section, the row of it (from 0), and the bars of that row (from 0) it runs from and to: the row had nothing of its own, and these four bars are the ones between the clock's half-past and its quarter-to (the bells are where the slow deck's notes are)
CANON_OCT = 1.0                                        # octaves each deck is from the record's speed at the ends: one starts at half speed and ends at double, the other the reverse; in the middle both are at the record's own speed, at the same place on it, on a bar line
CANON_PART = "tock"                                    # what is on the record (deck B's tock: TOCK), heard on deck B's own patch for it (its pitch already follows a lane named spd)
CANON_PAN = 0.8                                        # each deck goes from one side to the other as it goes: they cross in the middle of the room as they cross in speed and in pitch
CANON_POINTS = 4                                       # points of each lane to a beat
CANON_ROOM = "-10dB"                                   # the tock's own send to the room
CANON_GAIN = os.environ.get("C11T1_CANON_GAIN", "-16dB")  # set in the whole song's master between two readings, BEFORE their scores were read: at -14dB a stroke stood 6 under to 31 dB over the music in its own band (median 11 and 13 for the two decks; 39 of 44 level with it or over); at -20dB 12 under to 25 over (median 5 and 7; 31 of 44): a deck that loses a stroke in three is not heard to accelerate. The slower decks of v12 are at -13. THIS MASTER DELIVERS THESE TICKS AS WRITTEN (6 dB of fader was 6 dB of every stroke). At the crossing the two strike as one, 6 dB up: about the tock's own level (-8.5)
WOW = os.environ.get("C11T1_WOW", "1") != "0" and CANON and SCAR and FAST   # v23: the hole in deck B's record is off centre: its speed goes up and down once a turn (wow), and a held chord on the record shows it
WOW_IN = ("locked", 0)                                 # the section and the row of it (from 0): the first row in which nothing else moves deck B's speed (the hand is off; the switch goes to the other speed half way through, and the wow goes with it)
WOW_OFF = 1.0                                          # mm the hole is off centre
WOW_RADIUS = 80.0                                      # mm from the centre to the needle: the speed under it goes WOW_OFF / WOW_RADIUS up and down (1.25%: 21.5 cents each way), once a turn, FASTEST WHEN THE SCRATCH (v20) IS UNDER THE NEEDLE
WOW_ORGAN = os.environ.get("C11T1_WOW_ORGAN", "1") != "0"   # the held chord (off: the wow is on the record's strokes only: the reference the organ is read against)
WOW_PARTS = ((1, 0), (2, -12))                         # the organ: plain tones (ratio, dB): nothing in it moves but the record
WOW_VEL = 0.7
WOW_PAN = 0.1                                          # where the record's chord is
WOW_GAIN = os.environ.get("C11T1_WOW_GAIN", "-31dB")   # set in the whole song's master between two readings, BEFORE their scores were read (each read against the same song with WOW_ORGAN off, fitted out): at -28dB the organ is -23.8 dBFS, 12.7 dB under the row and LEVEL with the music between 180 and 500 Hz (the stab's own band); at -34dB 6 dB less. Between: a held chord under the stabs, not over them. THE MASTER PUMPS IT 5 dB WITH EVERY BEAT
PIPS_BEFORE = 5                                        # short pips: one on each of the five seconds before the minute
PIPS_SHORT = 0.1                                       # seconds a short pip lasts
PIPS_LONG = 0.5                                        # the sixth, which BEGINS on the minute
PIPS_HZ = 1000.0                                       # the time signal's tone: a standard, in no key
PIPS_NOTE = "B5"                                       # the note it is written on (987.77 Hz): the patch's one layer is 1000 / 987.77 times it
PIPS_GAIN = os.environ.get("C11T1_PIPS_GAIN", "-24dB")
PIPS_TRIM = {1: (-5.0, -7.0, -3.5, -5.0, -0.5, -1.5), 2: (-5.0, -7.0, -1.0, -3.0, -1.5, -4.5), 3: (-6.0, -5.0, -4.5, -5.0, -6.0, -6.5), 4: (-3.5, -5.0, -2.0, -3.5, 0.0, -1.5)}    # dB, pip by pip (the five short ones and the long one of each minute), set in the whole song's master so that every pip is delivered alike: written at one level they came out 7 dB apart (-24.0 to -31.0 dBFS in the right ear), the ones nearest a beat the smallest, because the master ducks with the drum
CHIME_EVERY = 60                                       # seconds: it strikes at every whole minute of the song (124 beats: 31 bars: a minute begins on a bar line)
CHIME_APART = 1                                        # seconds between the strokes of one minute: the clock's own time (2 beats and a fifteenth)
CHIME_NOTE = os.environ.get("C11T1_CHIME_NOTE", "F6")  # the bell
CHIME_PARTS = ((1.0, 0.0), (2.756, -9.0), (5.404, -18.0))    # a struck bar's partials: times the note, dB
CHIME_RING = "1200ms"                                  # how long a stroke rings
CHIME_HELD = 2.0                                       # beats a stroke is held: just under the time to the next
CHIME_GAIN = os.environ.get("C11T1_CHIME_GAIN", "-16dB")
CHIME_TRIM = {1: 0.0, 2: 0.0, 3: -10.0, 4: -4.0}        # dB, minute by minute, set in the whole song's master so that every stroke is delivered alike: written at one level the strokes of 3:00 (in "the stretch", where little else sounds) came out 10 dB over those of 1:00 and 2:00, at -4 dBFS, and those of 4:00 4 dB over
CLOCK_END_BARS = 4                                     # the song's last bars: the hat has gone, the record stops
CLOCK_END_GAIN = os.environ.get("C11T1_CLOCK_END_GAIN", "-44dB")    # set in the whole song's master: a tick peaks 7.8 dB over this figure there: -36 dBFS, the level agreed with chirper-one for Least Common's first four bars
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
UP = os.environ.get("C11T1_UP", "1") != "0" and CUE and STOP and os.environ.get("C11T1_WOW", "1") != "0"   # v24: the record is started: the stop's mirror. The song ends with deck B's motor switched off; it now begins with it switched on, in the headphone, before the cue
UP_BARS = STOP_BARS                                    # the bars the platter takes to come up to speed: the bars it takes to stop. The motor goes on this long before the cue's first stroke: at the song's first instant (and half a sixteenth)
UP_NOTE = "D3"                                         # the note the click's noise is clocked from at full speed: 93 steps of the register to a turn: 13.7 thousand steps a second: a click up to about 7 kHz, as the cue's is
UP_LEN = 0.0207                                        # beats a click lasts at full speed (10 ms): at speed s it lasts 1/s as long and its register runs s as fast: EVERY CLICK IS THE SAME STEPS OF THE REGISTER, as a record's click slowed down is the same groove
UP_VEL = (0.55, 0.34, 0.62, 0.4)                       # the record's sixteenths (the hat's and the cue's own accents), times the speed: a cartridge gives a voltage in proportion to the groove's speed under it: 6 dB less at half speed
UP_TRIM = -16.1                                        # dB on the track so that a click at full speed has the energy of the cue's own click at the same accent. READ ALONE at the cue's fader: the register's click (8.7 ms of full-scale steps) came out 16.1 dB over the cue's (4.4 ms of dying noise) through the same three filters (16.8 without the headphone's top)
UP_GAIN = os.environ.get("C11T1_UP_GAIN", "")          # the track's fader: the cue's own (with the trim) unless given. READ IN THE WHOLE SONG'S MASTER (left ear, 1.5 to 8 kHz): with the trim the last four clicks come within 3.3 dB of the cue's first four strokes of the same accents (-3.3 +1.8 -2.6 -1.7): the hand-over is level; 6 dB lower they are 4 to 9 dB under and the cue steps up. THE CLICKS WHOSE NUMBER IS A SQUARE (1, 4, 9) FALL HALF A SIXTEENTH AFTER A BASS DRUM (2 times the root of a square is a whole beat) and the master ducks them 8 to 12 dB; 6 and 12 fall within 30 ms of one and go the same way
BEAT = os.environ.get("C11T1_BEAT", "1") != "0" and UP   # v25: the two records beat: the same held tone is on both decks, deck A's steady and deck B's turning with its record: where they are in step they add, half a wave apart they cancel: one throb for every wave the decks drift apart
BEAT_IN = ("the nudge", 0)                             # the section and the row of it (from 0): its first row, which had nothing of its own: the hand pushes deck B a quarter of a beat ahead and lets it come back, twice
BEAT_WAVES = 64                                        # waves of the tone to a beat of the grid: 132.27 Hz at 124 to the minute (C3 and 19 cents: a note the loop at the end of this section goes through): a quarter of a beat apart is 16 waves exactly, so each throb is a 64th of a beat (7.56 ms) of drift
BEAT_NOTE = "C3"                                       # the note it is written on; the lane carries the 19 cents
BEAT_VEL = 0.8
BEAT_PAN = 0.0                                         # both in the middle: two tones beat in the air only if they come from one place (an ear each and the beat is made in the head: Hearing Things has that)
BEAT_GAIN = os.environ.get("C11T1_BEAT_GAIN", "-31dB")   # each tone. Set in the whole song's master between two readings, BEFORE their scores were read: at -34dB the swells are 2.1 dB over the rest of the music in the tone's band (its median), at -28dB 8.1 dB over it and the row's other music is pushed 0.17 dB down. At both, all 64 silences are where they are written (3 ms, median)
LEAP = os.environ.get("C11T1_LEAP", "1") != "0" and BEAT   # v26: GIVE OR TAKE A SECOND: the wall clock is given a leap second and has one taken back. The minute that ends at LEAP_GIVE has 61 seconds: the time signal has SEVEN pips (as it does on the night of a leap second: 23:59:60), and from then the clock's strokes and quarters are a second late against the record. The minute that ends at LEAP_TAKE has 59: FIVE pips (the signal laid down for a second taken out, which has never yet been sent), and the clock is right again
LEAP_GIVE = 3                                          # the minute given a second: its pips are in "the stretch", where the drum rests
LEAP_TAKE = 4                                          # the minute that has one taken: so the clock ends the song where it always did (the last four bars are not touched)
LEAP_TRIM = {"long": -4.5}                             # dB: the long pip of the given minute stands a second later than it did: its velocity there, set in the whole song's master (every other pip keeps the trim of the second of the song it stands on): at -6.5 (the trim it had on 3:00) it arrived at -28.6 dBFS, the quietest of the seven, where the song's other long pips are -25.4 to -26.3: 2 dB up
SWING = os.environ.get("C11T1_SWING", "1") != "0" and LEAP   # v27: THE GRID IS FOUND: the record's hat comes in swung hard and is set straight a step at a time. In every pair of its sixteenths the long one stands to the short one as SWING_WALK says: 3 to 1, 2 to 1, 3 to 2, 1 to 1: a twelfth, an octave, a fifth, a unison: the ratios of the first intervals, heard as time. Nothing is added and no stroke on a beat or an off beat moves: only the hat's second and fourth sixteenths
SWING_IN = ("the grid", 1)                             # the section and its row (from 0): bars 9 to 16, where the hat comes in and nothing drifts yet
SWING_PART = "hat"                                     # the track whose off sixteenths move
SWING_WALK = ((3, 1), (2, 1), (3, 2), (1, 1))          # long to short, SWING_BARS bars each: the off stroke stands on the last quarter, the last third, the last two fifths and the half of its eighth: late by 1/8, 1/12, 1/20 of a beat and nothing (60.5, 40.3, 24.2 ms at 124)
SWING_BARS = 2                                         # bars a step
STROBE = os.environ.get("C11T1_STROBE", "1") != "0" and SWING   # v28: THE STROBE: a turntable has a ring of dots round its platter and a lamp that flashes in time: when the record runs true the dots stand still; when it gains they creep forward, when it loses they creep back. Here the lamp flashes on every beat of the grid and the dots are notes: the note that is under the lamp says how far deck B's record is from the grid at that instant. The dot that is on its mark is STROBE_HOME; a dot is 1 / STROBE_DOTS of a beat
STROBE_IN = ("take", 0)                                # the section and its row (from 0): bars 33 to 40: the row had nothing of its own, and deck B's own bass drum (which lets you hear the drift as a flam) comes in the row after
STROBE_DOTS = 50                                       # dots round one beat of the record: a dot is 9.68 ms at 124 to the minute; the hand's reach in "take" (0.08 of a beat) is 4 dots
STROBE_AT = 0.0                                        # where in each beat of the grid the lamp flashes
STROBE_SCALE = (0, 3, 5, 7, 10)                        # the dots' notes, semitones over the home note, round and round (an octave every five dots): G Bb C D F
STROBE_HOME = 55                                       # the dot on its mark: G3 (MIDI 55)
STROBE_LEN = 0.75                                      # beats a flash's note is held
STROBE_GAIN = os.environ.get("C11T1_STROBE_GAIN", "-22dB")   # set in the whole song's master BEFORE any score was read. The bench (a note alone at -20 dB): its body (60 to 300 ms) -35.9 dBFS. Read at -28dB in the song: the bodies -33.1 dBFS: the master lifts it 10.8 dB there and not the 18.5 of a part between the drums (the notes are ON the bass drum, which ducks them); the old music at 170 to 370 Hz in the same windows is -27.9 in the middle: meant to stand about level with it, so 6 dB up
GIVE = os.environ.get("C11T1_GIVE", "1") != "0" and STROBE   # v29: GIVE OR TAKE A NOTE (the process of Rzewski's "Les Moutons de Panurge", 1969): a tune is GIVEN a note at a time (1 ; 1 2 ; 1 2 3 ; ... ; all of it) and then TAKEN a note at a time from the front (2 to the end ; 3 to the end ; ... ; the last note alone). A tune of n notes takes n(n+1)/2 notes to give and n(n-1)/2 to take: n squared in all: 8 notes are 64: one row of eighths, to the note. The first note comes round on the triangular numbers, later and later; the last note sooner and sooner
GIVE_IN = ("both", 1)                                  # the section and its row (from 0): bars 73 to 80: both decks, and the row does both
GIVE_TUNE = ("G3", "Bb3", "D4", "C4", "F4", "G4", "Bb4", "D5")   # the tune: the song's five notes (G Bb C D F), rising with one turn back so that it is a tune and not a scale; under the clock's chimes (F5 to D6)
GIVE_STEP = 0.5                                        # beats from note to note: eighths
GIVE_AT = 0.25                                         # the beat of the row its first note is on: a sixteenth after the drum, and so every note a sixteenth after a stroke (on the eighths themselves the bass drum and the sub have the band: the old music's tops at 180 to 620 Hz are -8 to -12 dBFS there, -13 to -23 a sixteenth after the beat)
GIVE_LEN = 0.45                                        # beats a note is written
GIVE_PAN = 0.25                                        # the giving a little to the left, the taking as far to the right
GIVE_GAIN = os.environ.get("C11T1_GIVE_GAIN", "-24dB")   # both tracks. The bench (the row alone at -20 dB): a note's first 100 ms -35.1 dBFS. Read in the whole song's master at -30dB and -36dB (seed 0), BEFORE any score: -34.5 and -40.5 dBFS (this master lifts it 10.6 dB in this row, no more than a note on the drum: both decks are playing), nine in ten within 1.5 dB, the two places in the beat 0.2 dB apart: no trims. The old music in a sixth of an octave round each note is -37 to -42 dBFS in the middle: at -30dB the tune was level with it. -24dB is meant to bring it to -28.5 dBFS, as loud as the strobe
LIFE = os.environ.get("C11T1_LIFE", "1") != "0" and GIVE   # v30: HALF-LIFE: a low string is struck every two bars. Its first tone is half as loud a bar later; its second half as loud after half a bar; its third after a third; its fourth after a quarter: the nth tone halves n times as fast. Every tone of the string is a clock that runs down, and the string's colour says how long ago it was struck: no tick, no count: time told by what is left
LIFE_IN = ("the nudge", 1)                             # the section and its row (from 0): bars 105 to 112, the row after the two records beat; nothing held is in it
LIFE_NOTES = ("D2", "D3", "A3", "D4")                  # the string's first four tones: 73.4 Hz and two, three, four times it (A3 is two cents under three times): D is the fifth of the song's G; 71 Hz is the one band the song is short in
LIFE_EVERY = 8                                         # beats from stroke to stroke: two bars
LIFE_AT = 0.125                                        # the beat of the bar a stroke is on: an eighth of a beat after the drum: 26 ms or more from every stroke of every part in bars 105, 107, 109 and 111 (searched on v29's notes)
LIFE_HALF = 4.0                                        # beats in which the first tone halves (6.02 dB): one bar; the nth tone's half-life is this over n
LIFE_TILT = 6.0206                                     # dB the nth tone is under the first at the stroke, for each doubling of n: as 1 over n (a plucked string's)
LIFE_GAIN = os.environ.get("C11T1_LIFE_GAIN", "-26dB")   # the first tone's track; the others are under it by the tilt. The bench (the row alone, the first tone at -20 dB): its first beat -30.0 dBFS. Read in the whole song's master at -36dB (both seeds), BEFORE any score: -35.4 / -35.3 dBFS: THE MASTER LIFTS IT 10.6 dB (a full row: the same 10.6 the tune of v29 had), not the 17 a held tone had in other songs: the first tone was 9 to 17 dB under the old music in its own sixth of an octave: 10 dB up, for -25.4
ARROW = os.environ.get("C11T1_ARROW", "1") != "0" and LIFE   # v31: TIME'S ARROW: the string of HALF-LIFE is heard BEFORE it is struck: the film of its first two strokes run backwards. It grows out of nothing, the low tone first and slowly, the upper ones later and faster, and stops dead where the stroke was. Every instant of it is as far before the mirror as the string's is after
ARROW_GAP = 4                                          # bars before the string's row at which the mirror stands: the first beat of bar 101, the middle of the row between (the two records beat)
ARROW_STROKES = 2                                      # how many of the string's strokes are turned round: the first two, which fall in bars 93 to 96. The other two would fall in bars 89 to 92, where deck B's bass plays the string's own D2 (read on v30: the old music in 73 Hz is -22 dBFS on its strokes there and -40 to -72 in bars 93 to 96)
ARROW_COME = 0.040                                     # seconds the turned string takes to come: the string's 40 ms to go, turned round
ARROW_GO = 0.004                                       # seconds it takes to stop: the string's 4 ms to come, turned round
ARROW_GAIN = os.environ.get("C11T1_ARROW_GAIN", "-32dB")   # the first tone's track; the others are under it by the string's tilt. THE BENCH (the turned string and the string alone, first tones at -20 dB): the last beat -30.0 dBFS; before the mirror and after it within 0.07 dB in the middle. Read in the whole song's master at -32dB (both seeds) BEFORE any score: the last beat -29.6 (bar 94, under the knock's roll) and -26.9 / -27.1 dBFS (bar 96): this master lifts it 12.4 and 15.1 dB
FUSE = os.environ.get("C11T1_FUSE", "1") != "0" and ARROW   # v32: A BEAT BECOMES A NOTE: one wave of a low tone, once a beat; then 2, 4, 8, 16 and 32 times a beat: at 32 the waves stand end to end and are one held note, whose pitch is the tempo (32 times it). Then it comes apart the same way. Nothing changes but how often
FUSE_IN = ("the stretch", 0)                           # the section and its row (from 0): its first four bars (89 to 92), before the turned string; the kick is not in them
FUSE_WAVES = 32                                        # waves of the tone to the beat: 124 / 60 * 32 = 66.13 Hz (the tone of the two records beat, bars 97 to 104, is 64 to the beat: the octave over)
FUSE_STEPS = ((1, 1), (2, 1), (4, 1), (8, 1), (16, 2), (32, 4), (16, 2), (8, 1), (4, 1), (2, 1), (1, 1))   # (waves a beat, for how many beats): 16 beats, 222 waves
FUSE_NOTE = ("C2", 65.40639132514966)                  # the note written and its frequency; the patch moves it to the tone
FUSE_GAIN = os.environ.get("C11T1_FUSE_GAIN", "-30dB")   # the track. THE BENCH FIRST (the track alone at -20 dB): every wave's top -26.0 dBFS; the note -29.0 dBFS; each halving of how many 3.0 dB less. Aimed at -24 to -27 dBFS for the note (the lifts read in bars 94 to 96: 12.4 to 15.1 dB). Read in the whole song's master (both seeds) BEFORE any score: the note -24.7 dBFS (lifted 14.3 dB), the waves' tops -20.4 to -21.1 on most beats
TALEA = os.environ.get("C11T1_TALEA", "1") != "0" and FUSE   # v33: THE TUNE AND ITS RHYTHM GO ROUND AT DIFFERENT SPEEDS (isorhythm: the talea and the color of the old motets): a rhythm of five notes to the bar and the song's tune of eight notes, each going round and round: the rhythm 8 times and the tune 5 times in the row's 40 notes, and only at the row's two ends do they begin together. No bar is like another, and every note of the tune is heard once in each of the bar's five places
TALEA_IN = ("the grid", 1)                             # the section and its row (from 0): bars 9 to 16: the drum, the hat and the tick alone. Read on v32 by twelfths of the beat: between the beats 196 to 588 Hz is -32 to -55 dBFS and 98 to 294 Hz -30 to -69
TALEA_STEPS = (3, 3, 4, 3, 3)                          # the rhythm, in sixteenths from each note to the next: five notes spread as evenly as sixteen sixteenths allow; one bar
TALEA_TUNE = ("G3", "Bb3", "D4", "C4", "F4", "G4", "Bb4", "D5")   # the tune of give or take a note (bars 73 to 80), whole, before it is given and taken
TALEA_GAIN = os.environ.get("C11T1_TALEA_GAIN", "-32dB")   # the track, before the trims. THE BENCH FIRST (the track alone at -20 dB, no trims): all 40 tops -26.3 to -25.8 dBFS
TALEA_EVEN = (8.3, -1.2, 5.8, 6.3, 2.7)                # dB each of the bar's five places is raised, so that the tune comes out at one height. THE FIRST BUILD HAD NONE AND THE MASTER GAVE THE RHYTHM AN ACCENT OF ITS OWN: read in the whole song (the new less the old) the tops were -33.3 dBFS on the beat (under the drum), -23.8 at beat 0.75, -30.8 and -31.3 on the two half beats (under the tick) and -27.7 at beat 3.25: 9.5 dB between the places, so every note of the tune came out at five heights. These bring each to -25 dBFS: read in the whole song's master BEFORE any score (seeds 0 / 11): -25.0, -25.0, -24.9, -25.0, -25.0 / -24.9, -25.0, -24.7, -25.1, -25.0 by place; all 40 tops -26.4 to -22.4 / -26.2 to -23.7
FAIR = os.environ.get("C11T1_FAIR", "1") != "0" and TALEA   # v34: ONE RHYTHM AT THREE SPEEDS, AND THEY NEVER DISAGREE (Thue and Morse's sequence: the fair way to take turns: give, take, take, give, take, give, give, take ...). Number the sixteenths of the row from 0; strike number n if n written in twos has an even number of ones. Take every second stroke-place of that rhythm and you have the same rhythm at half the speed; every fourth, at a quarter. So three voices play it on the sixteenths, the eighths and the beats, and a slower voice never strikes where a faster one rests. The bars go by the same rule: a bar is the pattern or its opposite
FAIR_IN = ("locked", 0)                                # the section and its row (from 0): bars 113 to 120: the two decks are locked. Read on v33 by twelfths of the beat: 1400 to 1750 Hz is -34 to -52 dBFS here, 1050 to 1300 Hz -36 to -48
FAIR_STEPS = (1, 2, 4)                                 # sixteenths from one place of a voice to its next: the three speeds
FAIR_NOTES = ("G6", "D6", "G5")                        # each voice's note: 1568, 1175, 784 Hz: the slower, the lower
FAIR_MS = 45                                           # ms a stroke is held: a plain pip
FAIR_TRIM = (-0.3, -5.9, -3.6, -4.7, -0.5, -5.9, -5.8, -8.9, -0.5, -6.0, -3.4, -5.4, 0.0, -5.8, -4.7, -8.3)   # dB (0 or less) on a stroke by the sixteenth of the bar it falls on, by its velocity. THE FIRST BUILD HAD NONE (-32.3 dB): in the finished song G6's strokes came out, by sixteenth of the bar (the middle of four), -33.6 -28.0 -30.3 -29.2 -33.4 -28.0 -28.1 -25.0 -33.4 -27.9 -30.5 -28.5 -33.9 -28.1 -29.2 -25.6 dBFS: 8.9 dB between the beat and the sixteenth before the next. These are that reading turned over, for -27 everywhere
FAIR_GAIN = os.environ.get("C11T1_FAIR_GAIN", "-25.4dB")   # every voice's track. THE BENCH FIRST (the three tracks alone at -20 dB, no trims): G6's tops -25.7 dBFS (the middle); the first build was set for -38 on the bench (-32.3 dB); the second is 6.9 dB up with the trims. THE SECOND BUILD READ (both seeds, before any score): G6 by sixteenth of the bar -27.1 to -27.0 / -27.5 to -26.4 dBFS; D6 -27.6 to -26.8 / -27.9 to -26.3; G5 -28.5 to -27.4 / -28.5 to -27.6
FASTER = os.environ.get("C11T1_FASTER", "1") != "0" and FAIR   # v35: THE BEAT THAT SPEEDS UP FOR EVER (Risset's rhythm: the stair without end, made of time): a pip is struck faster and faster, twice as fast after every two bars, and two bars later it is exactly where it began. It is several beats at once, each twice as fast as the one below and every one of them speeding up alike; the fastest fades out as it goes and a new slowest fades in under it, so that after a turn each has become the next and the whole is what it was
FASTER_IN = ("locked", 1)                              # the section and its row (from 0): bars 121 to 128: everything else is on the grid here. Read on v34: 1000 and 1300 Hz are -39 to -50 dBFS through the beat in this row
FASTER_TURN = 8                                        # beats in a turn: every beat of it doubles its speed in this time (2 bars)
FASTER_N = 4                                           # strokes of the slowest beat in a turn; the next has twice as many, and so on
FASTER_LAYERS = 4                                      # beats at once: 4, 8, 16 and 32 strokes a turn. A stroke of a slower beat is always a stroke of every faster one
FASTER_FROM = 0.25                                     # the beat of the bar a turn begins on: a sixteenth after the line, off the drum
FASTER_NOTE = "D6"                                     # the pip (1174.7 Hz)
FASTER_MS = 25                                         # ms a pip lasts
FASTER_EDGE = 3                                        # ms it takes to come and to go
FASTER_FLOOR = -30.0                                   # dB under the loudest: a stroke written lower than this is left out
FASTER_GAIN = os.environ.get("C11T1_FASTER_GAIN", "-28.3dB")   # the track. THE BENCH FIRST (the track alone at -20 dB): a stroke of all the beats -25.7 dBFS at its top; set for -24 in the song with the 10 dB the master gave a pip a sixteenth after the beat in bars 113 to 120. THE BUILD READ (both seeds, before any score): the strokes of all the beats -27.4 to -22.9 dBFS (the middle -24.4); a stroke written -6 dB or more is off what is written by -3.0 to +4.4 dB: the master, stroke by stroke (not by where in the beat it falls: by sixteenth the middles are within 1.0 dB). LEFT AS IT IS: a table of 104 trims would mend it
SLOWER = os.environ.get("C11T1_SLOWER", "1") != "0" and FASTER   # v36: THE BEAT THAT SLOWS FOR EVER: the strokes of the beat that speeds up for ever (v35, bars 121 to 128) TURNED ROUND about the line between the two rows: every pip of v35 is played again as far after that line as it was before it. What sped up for ever slows for ever: each beat halves its speed in two bars, a new fastest one fades in over it and the slowest fades out under it, and after every two bars it is exactly where it began. It is the row in which the record itself is switched off and runs down to a stop: the record stops; this never does
SLOWER_NOTE = FASTER_NOTE                              # the same pip
SLOWER_TRIM = {(0, 0): -6, (0, 1): -3.2, (0, 2): 2.7, (0, 3): -5.6, (0, 4): -3.5, (0, 5): 8, (0, 6): -5.8, (0, 7): -5.1, (0, 8): 1.7, (0, 9): -5.7, (0, 10): -3, (0, 11): -2, (0, 12): 9.5, (0, 13): -6.2, (0, 14): -1, (0, 15): -1.8, (0, 16): 9.1, (0, 17): -6.2, (0, 18): -2.6, (0, 19): -3.1, (0, 20): 2.9, (0, 22): -5.3, (0, 24): -1.7, (0, 26): -5.9, (0, 28): -4.8, (0, 30): 5.5, (1, 0): -6, (1, 1): -3.1, (1, 2): 2.8, (1, 3): -5.4, (1, 4): -3.5, (1, 5): 8.1, (1, 6): -5.8, (1, 7): -5.1, (1, 8): 1.7, (1, 9): -6.2, (1, 10): -3.4, (1, 11): -2.2, (1, 12): 9.6, (1, 13): -6.2, (1, 14): -1.3, (1, 15): -1.8, (1, 16): 8.7, (1, 17): -6.3, (1, 18): -3.1, (1, 19): -3.2, (1, 20): 2.8, (1, 22): -5.4, (1, 24): -1.7, (1, 26): -5.7, (1, 28): -4.9, (1, 30): 6.1, (2, 0): -5.9, (2, 1): -3.3, (2, 2): 2.7, (2, 3): -5.6, (2, 4): -3.4, (2, 5): 8.3, (2, 6): -5.6, (2, 7): -5.1, (2, 8): 1.7, (2, 9): -5.8, (2, 10): -3.3, (2, 11): -2, (2, 12): 9.7, (2, 13): -6.2, (2, 14): -1.3, (2, 15): -1.8, (2, 16): 9, (2, 17): -6.3, (2, 18): -3.1, (2, 19): -2.9, (2, 20): 2.9, (2, 22): -5.2, (2, 24): -1.7, (2, 26): -5.6, (2, 28): -4.9, (2, 30): 6.1, (3, 0): -5.8, (3, 1): -3.3, (3, 2): 3.4, (3, 3): -5.6, (3, 4): -3.5, (3, 5): 8.2, (3, 6): -5.4, (3, 7): -5.1, (3, 8): 1.6, (3, 9): -5.9, (3, 10): -3.5, (3, 11): -2.3, (3, 12): 9.5, (3, 13): -6.3, (3, 14): -2.4, (3, 15): -1.9, (3, 16): 9, (3, 17): -6.3, (3, 18): -2.9, (3, 19): -3, (3, 20): 3, (3, 22): -5.2, (3, 24): -1.6, (3, 26): -6, (3, 28): -4.9, (3, 30): 6}   # dB on a stroke, by (turn as played, stroke of the fastest beat): THE FIRST BUILD READ TURNED OVER. With no trims (-27.3 dB) the master put the four strokes of all the beats in a turn at -19.5, -26.2, -32.9 and -23.2 dBFS, the same in every turn within 1.2 dB and on both seeds: a stroke was off the law by -8.5 to +5.5 dB, by where it falls in this row (the record is running down under it). Each stroke's own miss (the two seeds' mean), turned over and written 1.15 times as deep; the largest is taken off all of them and given to the fader
SLOWER_GAIN = os.environ.get("C11T1_SLOWER_GAIN", "-17.3dB")   # THE BENCH FIRST (the track alone at -20 dB): a stroke of all the beats -25.7 dBFS at its top; the first build set for -22 in the song with 11 dB of lift (v35 got 9.6 in the row before): -27.3 dB: the middle one read -24.7. The second build is set for -24.4 (v35's own middle) with the trims: -17.3 dB
SHRINK = os.environ.get("C11T1_SHRINK", "1") != "0" and SLOWER   # v37: GIVE OR TAKE THIRTY MILLISECONDS: TAKEN, IT IS NOT MISSED; GIVEN, IT IS. Three clicks. The first and the last are always the same time apart (0.625 of a beat); only the middle one moves: in the middle (two even gaps), a sixteenth of a beat early (a short gap, then a long one) or a sixteenth of a beat late (long, then short). A short gap is said to shrink the gap after it towards itself, so short-long is said to sound even; long-short is said to sound as uneven as it is (time-shrinking: Nakajima, ten Hoopen and van der Wilk, 1991)
SHRINK_IN = ("no ruler", 0)                            # the section and its row (from 0): bars 49 to 56: there is no kick and no tick here and deck B wanders half a beat (the hat, the knock and the tock go on). Read on v36 first (b/oldat2.py): the old music in D5's band under a triple from beat 0 is -45.7 dBFS at the most (seed 0), from beat 2 -35.3
SHRINK_AT = (0, 2)                                     # beats of the bar a triple begins on
SHRINK_SPAN = 0.625                                    # beats from the first click to the last
SHRINK_MID = {"even": 0.3125, "short-long": 0.25, "long-short": 0.375}   # beats from the first click to the middle one
SHRINK_ORDER = ("even",) * 4 + ("short-long",) * 4 + ("long-short",) * 4 + ("short-long", "long-short") * 2   # triple by triple: two bars of each, then two bars of the two side by side
SHRINK_NOTE = "D5"                                     # the click's tone
SHRINK_MS = 15                                         # ms a click is held
SHRINK_EDGE = (1, 5)                                   # ms it takes to come and to go
SHRINK_TRIM = (10.4, 0.5, -2.3, 9.2, -0.4, -2.4, 6, -2, -0.4, 4.5, -2, -2.5, 11.6, 1.4, -1.9, -2.3, 7.6, -0.9, -2.1, -2.5, 1.6, -1.5, -2, -0.1, 11.8, -0.7, -0.1, 0.5, -2.6, 9.6, -0.7, -2, 5.5, -1.2, -2.5, -2.6, 10.6, 1, -1.8, -1.5, -2.2, 1.7, -1.4, -2.5, 5.3, -1.1, 8.2, 0.4)   # dB on a click, click by click. MEASURED, NOT REASONED: with no trims (-25.7 dB) the master gave the 48 clicks -34.2 to -21.7 dBFS (up to 12.4 dB apart within a triple; the two seeds within 1.93 dB): each click's level less -24, turned over and written 1.15 times as deep
SHRINK_GAIN = os.environ.get("C11T1_SHRINK_GAIN", "-13.9dB")   # THE BENCH FIRST (the track alone at -20 dB): every click -30.3 dBFS (root mean square over 20 ms), every gap within 0.04 ms of what is written; the first build set for -24 in the song with 12 dB of lift; the second build: the trims' top (11.8) added to the first build's -25.7 dB
CHANCE = os.environ.get("C11T1_CHANCE", "1") != "0" and SHRINK   # v38: CHANCE COMES IN CLUMPS: eight pips to two bars, on the sixteenths, four times: spread by the golden ratio (never two side by side), thrown by chance, spread, thrown. Of all the ways to draw 8 sixteenths of 32, nine in ten have two side by side
CHANCE_IN = ("no ruler", 1)                            # the section and its row (from 0): bars 57 to 64
CHANCE_SLOTS = 32                                      # sixteenths to a phrase (two bars)
CHANCE_N = 8                                           # pips to a phrase
CHANCE_ORDER = ("spread", "chance", "spread", "chance")   # the four phrases
CHANCE_SEED = 111                                      # the throw: x -> (1664525 x + 1013904223) mod 2^32 from this, its top 16 bits; the first CHANCE_N of a shuffle of the sixteenths. Written before the throw was seen, and not changed after
CHANCE_NOTE = "G4"                                     # a plain pip
CHANCE_LEN = 0.125                                     # beats a pip is held (60 ms)
CHANCE_EDGE = (3, 15)                                  # ms a pip takes to come and to go
CHANCE_TRIM = (7.8, -5, 3.5, -3, -1.9, -2.1, -4, 2.7, -2.5, -5.1, -2.9, -4.4, 5.8, 6.9, 2.5, -5.1, 1.3, -0.1, 6.2, -0.9, -0.8, 6.3, -0.8, -4.5, 10.4, -4, -0.9, 7.2, -0.4, 7.7, -0.6, -5.1)   # dB on a pip, pip by pip in time. MEASURED, NOT REASONED: with no trims (-24.7 dB) the master gave the 32 pips -33.0 to -19.5 dBFS by place (the two seeds within 0.84 dB): each pip's level less -24, turned over and written 1.15 times as deep
CHANCE_GAIN = os.environ.get("C11T1_CHANCE_GAIN", "-14.3dB")   # THE BENCH FIRST (the track alone at -20 dB): every pip -29.3 dBFS over its 60 ms, read on the sixteenth it is written on; the first build set for -24 in the song with 10 dB of lift; the second build: the trims' top (10.4) added to the first build's -24.7 dB
POLY = os.environ.get("C11T1_POLY", "1") != "0" and CHANCE   # v39: FIVE AGAINST SEVEN. A wooden stroke five times a bar, evenly, and another seven times a bar, evenly: neither is on the grid's sixteenths after the first beat, they agree once a bar and nowhere else, and the bar's strokes read the same backwards. The song's own five (the tock's, on the grid) is this five rounded down
POLY_IN = ("give", 0)                                  # the section and its row (from 0): bars 17 to 24: the first row with no part of its own that is not kept out
POLY_N = (5, 7)                                        # strokes to the bar, each evenly spread
POLY_NOTE = ("F4", "C4")                               # the five's wood and the seven's, a fourth apart. THE FIRST BUILD HAD THE FIVE ON F3: on the first beat of the bar the old music in F3's band (the drum and the sub) was 8.6 to 13.4 dB over the stroke (seed 0), and I had not read the old music at the strokes' own instants before building. Read then (oldat.txt, v38, both seeds, eight notes from F3 to Bb4): F4 has 1 of the five's 6 first-beat strokes and 1 of its 24 others with old music over -22 dBFS in its band; F3 had 6 of 6
POLY_PAN = (-0.4, 0.4)
POLY_BARS = ((0, 6), (2, 8))                           # bars of the row (from, up to) each plays: the five alone for 2 bars, both for 4, the seven alone for 2
POLY_FALL = 2.0                                        # dB each stroke of the row's last bar is under the one before it: the seven thins out
POLY_LEN = 40                                          # ms a stroke takes to die
POLY_TRIM = ((11.6, 0.9, -3.2, -2.6, 1.0), (8.2, 1.5, 3.2, -4.3, -0.1, -0.2, -2.7))   # dB by place in the bar, the five's and the seven's. THE SECOND BUILD: in the song's master the strokes of the first build (no trims, both voices at -8 dB) stood by place, against their voice's middle, -9.35 -0.05 +3.49 +3.00 -0.15 dB (the five) and -7.17 -1.32 -2.81 +3.71 +0.10 +0.20 +2.31 dB (the seven), the middle of the two seeds: the master holds the stroke on the first beat down (the drum is on it). Each place is turned 1.15 times that the other way; the five is 0.8 dB up as well (on the bench F4 is -42.8 dBFS where C4 is -41.9: the filter)
POLY_GAIN = os.environ.get("C11T1_POLY_GAIN", "3.6dB")   # both tracks. THE BENCH FIRST (the two alone at -20 dB; the five then on F3): a stroke -42.0 (the five) and -41.9 dBFS (the seven) in its own band in its loudest 20 ms, begun 2.0 ms after it is written; the first build set for -20 dBFS in the song with 10 dB of lift, a guess, at -8 dB: the strokes' middle came out -19.2 and -19.0 dBFS on seed 0 (the lift 10.8 and 10.9 dB). The fader is that plus the highest trim (11.6 dB), for the loudness goes with the velocity under the highest
assert sum(fu_b for _, fu_b in FUSE_STEPS) % BEATS == 0
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


def scar_phase():
    """The sixteenth of the record (from its start) the scratch is first met on: every SCAR_TURN after it, the needle meets it again."""
    b0 = next((x[1] for x in SECS if x[0] == SCAR_ON), 0)
    return (b0 * 16) % SCAR_TURN


def scar_steps(bar):
    """Deck B's record, bar by bar, as its other parts are written: the sixteenths of this bar on which the needle meets the scratch."""
    return [(s + SCAR_OFF, SCAR_NOTE, 0.5 - SCAR_OFF / 2, SCAR_VEL) for s in range(16) if (bar * 16 + s - scar_phase()) % SCAR_TURN == 0]


def scar_notes():
    return deck_b(SCAR_WITH, scar_steps) if SCAR else []


def leap_real(sec):
    """The second of the SONG on which the wall clock shows second `sec`: between the minute that was given a second and the minute that had one taken the clock is a second late."""
    return sec + (1 if LEAP and LEAP_GIVE * CHIME_EVERY <= sec < LEAP_TAKE * CHIME_EVERY else 0)


def pips_seconds():
    """(the minute, [(the second of the song a pip begins on, how many seconds it lasts)]): five short ones before each minute the clock strikes and a long one on it; with the leap second (LEAP) six short ones before the minute that was given a second and four before the one that had one taken."""
    if not LEAP:
        return [(k, [(k * CHIME_EVERY - j, PIPS_SHORT) for j in range(PIPS_BEFORE, 0, -1)] + [(k * CHIME_EVERY, PIPS_LONG)]) for k, _ in chime_strikes()]
    out = []
    for k, _ in chime_strikes():
        m = k * CHIME_EVERY
        shorts = [m - j for j in range(PIPS_BEFORE, 0, -1)]            # the clock's seconds 55 to 59
        if k == LEAP_TAKE:
            shorts = shorts[:-1]                                       # that minute has no second 59
        ps = [(leap_real(c), PIPS_SHORT) for c in shorts]
        if k == LEAP_GIVE:
            ps.append((m, PIPS_SHORT))                                 # the leap second itself, 59:60: the song's second on which the minute used to begin
        out.append((k, ps + [(leap_real(m), PIPS_LONG)]))
    return out


def pips_trim(k, i, sec):
    """dB on pip i of minute k, which begins on second `sec` of the song: PIPS_TRIM was set pip by pip in the whole song's master, so with the leap second a pip takes the trim of the song's second it stands on."""
    if not LEAP:
        return PIPS_TRIM[k][i]
    was = dict(zip([k * CHIME_EVERY - j for j in range(PIPS_BEFORE, 0, -1)] + [k * CHIME_EVERY], PIPS_TRIM[k]))
    return was[sec] if sec in was else LEAP_TRIM["long"]


def pips_note_hz():
    semis = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}[PIPS_NOTE[:-1]]
    return 440 * 2 ** ((semis + 12 * (int(PIPS_NOTE[-1]) + 1) - 69) / 12)


def pips_notes():
    return [{"at": round(sec * BPM / 60, 5), "len": round(ln * BPM / 60, 5), "pitch": PIPS_NOTE, "vel": round(0.9 * 10 ** (pips_trim(k, i, sec) / 20), 4)} for k, ps in pips_seconds() for i, (sec, ln) in enumerate(ps)]   # a pip's loudness is its velocity (vel_sens 0.5)


def canon_span():
    """(the beat the two decks start, the beat they cross, the beat they stop), or None."""
    sec = next((x for x in SECS if x[0] == CANON_IN[0]), None) if CANON else None
    if sec is None or CANON_IN[1] * ROW >= sec[2]:
        return None
    b0 = sec[1] + CANON_IN[1] * ROW
    t0, t1 = (b0 + CANON_IN[2]) * BEATS, (b0 + CANON_IN[3]) * BEATS
    return t0, (t0 + t1) / 2, t1


def canon_speed(t, up):
    """The speed of the deck that winds up (or the one that runs down) at grid beat t: 2 ** (octaves from the crossing), a straight line in pitch."""
    t0, tc, t1 = canon_span()
    return 2 ** ((1 if up else -1) * CANON_OCT * (t - tc) / (tc - t0))


def canon_place(t, up):
    """The beat of the record under that deck's needle at grid beat t: the speed added up from the crossing, where both are at the record's beat tc."""
    t0, tc, t1 = canon_span(); k = (tc - t0) / (CANON_OCT * math.log(2))
    return tc + (1 if up else -1) * k * (canon_speed(t, up) - 1)


def canon_when(b, up):
    """The grid beat at which that deck's needle is at the record's beat b (the other way round), or None if it never is."""
    t0, tc, t1 = canon_span(); k = (tc - t0) / (CANON_OCT * math.log(2)); x = 1 + (1 if up else -1) * (b - tc) / k
    return tc + (1 if up else -1) * (tc - t0) / CANON_OCT * math.log2(x) if x > 0 else None


def canon_notes(up, steps):
    """Every stroke the record holds between where that deck starts and where it stops, when its needle gets there."""
    t0, tc, t1 = canon_span(); out = []
    p0, p1 = canon_place(t0, up), canon_place(t1, up)
    for bar in range(int(p0 // BEATS), int(p1 // BEATS) + 1):
        for st, p, n, v in steps(bar):
            b = bar * BEATS + st * STEP
            if p0 <= b < p1:
                t = canon_when(b, up); end = canon_when(min(b + n * STEP, p1), up)
                out.append({"at": round(t, 5), "len": round(end - t, 5), "pitch": p, "vel": round(v, 3)})
    return out


def canon_lanes(up):
    """(the deck's pitch against the record, semitones; where it is, -1 left to 1 right): a point CANON_POINTS times a beat."""
    t0, tc, t1 = canon_span(); n = int((t1 - t0) * CANON_POINTS); side = 1 if up else -1
    ts = [t0 + j / CANON_POINTS for j in range(n + 1)]
    spd = [["0b", round(12 * math.log2(canon_speed(t0, up)), 3)]] + [[f"{t:g}b", round(12 * math.log2(canon_speed(t, up)), 3)] for t in ts]
    pan = [["0b", round(-side * CANON_PAN, 3)]] + [[f"{t:g}b", round(side * CANON_PAN * (t - tc) / (tc - t0), 3)] for t in ts]
    return spd, pan


def quart_chimes():
    """[(seconds, minute, quarter, [(seconds, bell, is it the change's last note?)])]: a chime at every quarter of a minute but the whole ones, left out if any of it would sound in the last four bars (the seam: the ticking alone)."""
    end = (BARS - 4) * BEATS * 60 / BPM
    out, k = [], 1
    while k * QUART_EVERY < end:
        if k % 4:
            ns = [(k * QUART_EVERY + i * QUART_CHANGE + j * QUART_APART, QUART_BELLS[d], j == len(QUART_CHANGES[c]) - 1) for i, c in enumerate(QUART_ORDER[k % 4]) for j, d in enumerate(QUART_CHANGES[c])]
            if ns[-1][0] + 1.5 < end:
                late = leap_real(k * QUART_EVERY) - k * QUART_EVERY          # v26: a second, between the given minute and the taken one
                out.append((k * QUART_EVERY + late, k // 4, k % 4, [(sec + late, bell, last) for sec, bell, last in ns] if late else ns))
        k += 1
    return out


def quart_notes():
    return [{"at": round(sec * BPM / 60, 5), "len": QUART_HELD[1 if last else 0], "pitch": bell, "vel": round(0.9 * 10 ** (QUART_TRIM.get((m, q), 0.0) / 20), 4)} for _, m, q, ns in quart_chimes() for sec, bell, last in ns]


def chime_strikes():
    """(the minute, the seconds of its strokes): at the k-th whole minute of the song the clock strikes k times, CHIME_APART seconds apart."""
    end = BARS * BEATS * 60 / BPM
    return [(k, [leap_real(k * CHIME_EVERY) + j * CHIME_APART for j in range(k)]) for k in range(1, int(end // CHIME_EVERY) + 1) if k * CHIME_EVERY + (k - 1) * CHIME_APART < end]


def chime_hz():
    """Hz of the bell's note."""
    semis = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}[CHIME_NOTE[:-1]]
    return 440 * 2 ** ((semis + 12 * (int(CHIME_NOTE[-1]) + 1) - 69) / 12)


def chime_notes():
    return [{"at": round(sec * BPM / 60, 5), "len": CHIME_HELD, "pitch": CHIME_NOTE, "vel": round(0.9 * 10 ** (CHIME_TRIM.get(k, 0.0) / 20), 4)} for k, secs in chime_strikes() for sec in secs]   # the bell's loudness is its velocity (vel_sens 0.5)


def clock_span():
    """(first bar, bar after the last) of the section the clock is heard in, from 0."""
    return next((b0, b0 + n) for name, b0, n, parts, hand in SECS if name == CLOCK_IN)


def clock_seconds():
    """The whole seconds of the song (multiples of CLOCK_EVERY) that fall inside the span."""
    b0, b1 = clock_span(); bar_s = BEATS * 60 / BPM
    return [k * CLOCK_EVERY for k in range(int(b0 * bar_s / CLOCK_EVERY) + 1, int(math.ceil(b1 * bar_s / CLOCK_EVERY))) if b0 * bar_s <= k * CLOCK_EVERY < b1 * bar_s]


def clock_end_seconds():
    """The whole seconds (multiples of CLOCK_EVERY) in the song's last CLOCK_END_BARS bars."""
    bar_s = BEATS * 60 / BPM; t0, t1 = (BARS - CLOCK_END_BARS) * bar_s, BARS * bar_s
    return [k * CLOCK_EVERY for k in range(int(t0 / CLOCK_EVERY), int(t1 / CLOCK_EVERY) + 1) if t0 <= k * CLOCK_EVERY < t1]


def clock_end_notes(pallet):
    """The ticks (pallet 0) or tocks (pallet 1) of the last bars: each second on the pallet it would be on had the clock never stopped."""
    first = clock_seconds()[0]
    return [{"at": round((sec - early) * BPM / 60, 5), "len": 0.05, "pitch": "C6", "vel": vel} for sec in clock_end_seconds() if round((sec - first) / CLOCK_EVERY) % 2 == pallet for early, vel in CLOCK_PARTS]


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
    if CLOCK_END:
        for ce_i, ce_nm in enumerate(("tick", "tock")):
            doc["tracks"].append({"name": f"clock-{ce_nm}-end", "patch": f"gt-clock-{ce_nm}", "gain": CLOCK_END_GAIN, "pan": CLOCK_PAN, "sends": {"room": CLOCK_ROOM}, "notes": clock_end_notes(ce_i)})
        doc["about"] = doc["about"].replace(" Generated by", f" From v17 the clock is heard again in the last {CLOCK_END_BARS} bars, when the record has stopped: it was running all along. Generated by")
        assert "From v17" in doc["about"]
    if CHIME and chime_strikes():
        PATCHES["gt-chime"] = {"about": f"Give or Take's clock's bell (chirper-zero, 27 Nov, v18): a small struck bar: plain tones at {', '.join(f'{r:g}' for r, _ in CHIME_PARTS)} times its note, ringing {CHIME_RING}: what the clock on the wall strikes the minutes on.",
                               "play": {"vel_sens": 0.5, "gate": 1},
                               "synth": {"layers": [f"sine phase=0 ratio={ch_r:g} level={ch_d:g}dB" for ch_r, ch_d in CHIME_PARTS], "amp": {"a": "0.3ms", "d": CHIME_RING, "s": 0, "r": "300ms", "curve": 3}}}
        doc["tracks"].append({"name": "chime", "patch": "gt-chime", "gain": CHIME_GAIN, "pan": CLOCK_PAN, "sends": {"room": CLOCK_ROOM}, "notes": chime_notes()})
        doc["about"] = doc["about"].replace(" Generated by", " From v18 the clock strikes the minutes: once at 1:00, twice at 2:00, three times at 3:00, four at 4:00, a second apart. A minute of this song is thirty-one bars exactly, so the first stroke of each is on a bar line, and every next one is a thirty-first of a second further behind the beat. Generated by")
        assert "From v18" in doc["about"]
    if PIPS and pips_seconds():
        PATCHES["gt-pip"] = {"about": f"Give or Take's pips (chirper-zero, 27 Nov, v19): the time signal's tone: one plain sine at {PIPS_HZ:g} Hz (written on {PIPS_NOTE}, {PIPS_HZ / pips_note_hz():.6f} times it), on at once and off at once (2 ms each way), as long as its note. In no key and in no room.",
                             "play": {"vel_sens": 0.5, "gate": 1},
                             "synth": {"layers": [f"sine phase=0 ratio={PIPS_HZ / pips_note_hz():.6f}"], "amp": {"a": "2ms", "d": "0ms", "s": 1, "r": "2ms"}}}
        doc["tracks"].append({"name": "pips", "patch": "gt-pip", "gain": PIPS_GAIN, "pan": CLOCK_PAN, "notes": pips_notes()})
        doc["about"] = doc["about"].replace(" Generated by", f" From v19 the clock counts each minute in with the pips: a short pip of {PIPS_HZ:g} Hz on each of the {PIPS_BEFORE} seconds before it and a long one that begins on it; a second is two beats and a fifteenth, so they close on every other beat (161, 129, 97, 65, 32 ms early) and the long one is on the bar line, with the bell. Generated by")
        assert "From v19" in doc["about"]
    if SCAR and scar_notes():
        PATCHES["gt-scar"] = {"about": "Give or Take's scratch (chirper-zero, 27 Nov, v20): the tick of a scratch across deck B's record as the needle meets it, once a turn: two plain tones (the note and 3.1 times it) gone in 6 ms; its pitch follows deck B's speed (auto.spd, semitones), so it falls with the platter.",
                              "play": {"vel_sens": 0.5},
                              "synth": {"layers": ["sine phase=0", "sine phase=0 ratio=3.1 level=-6dB"], "pitch": {"value": 0, "mod": [{"src": "auto.spd", "amount": 1}]}, "amp": {"a": "0.1ms", "d": "6ms", "s": 0, "r": "4ms", "curve": 3}}}
        doc["tracks"].append({"name": "scar", "patch": "gt-scar", "gain": SCAR_GAIN, "pan": SCAR_PAN, "auto": {"spd": {"points": lane}}, "notes": scar_notes()})      # dry, as the pop is
        doc["about"] = doc["about"].replace(" Generated by", f" From v20 there is a scratch across deck B's record, which the needle meets once a turn: a small tick every {SCAR_TURN} sixteenths of the record, so {SCAR_TURN} against sixteen when the hand is off, and through everything the record goes through: early and late with the hand, twice and eight times over in the stretch, once more going backwards in the spin back, closer at the other speed; it alone is not changed when the needle sticks (it was once a turn already); and when the motor is switched off the needle meets it once more, late, and never again. Generated by")
        assert "From v20" in doc["about"]
    if QUART and quart_chimes():
        if "gt-chime" not in PATCHES:
            raise SystemExit("the quarters are rung on the clock's bell (gt-chime): C11T1_CHIME must be on")
        qu = quart_chimes()
        doc["tracks"].append({"name": "quarters", "patch": "gt-chime", "gain": QUART_GAIN, "pan": CLOCK_PAN, "sends": {"room": CLOCK_ROOM}, "notes": quart_notes()})
        doc["about"] = doc["about"].replace(" Generated by", f" From v21 the clock chimes the quarters of every minute, as a clock in a hall does: the Westminster quarters, five changes on four bells ({', '.join(QUART_BELLS[d] for d in (3, 2, 1, 5))}), taken in order: one change at a quarter past the minute, two at the half, three at a quarter to; the minute itself is left to the pips and the strokes. {len(qu)} chimes, {sum(len(c[3]) for c in qu)} notes, {QUART_APART:g} s apart: the clock's own time, which is a beat and a thirtieth of the decks', so the tune is nearly in time with them and never is; and how far through a minute the song is can be told from how many changes are rung. Generated by")
        assert "From v21" in doc["about"]
    if canon_span() is not None:
        ca_t0, ca_tc, ca_t1 = canon_span(); ca_steps = {"tock": TOCK}[CANON_PART]
        for ca_up in (True, False):
            ca_spd, ca_pan = canon_lanes(ca_up)
            doc["tracks"].append({"name": "canon-up" if ca_up else "canon-down", "patch": "gt-" + CANON_PART, "gain": CANON_GAIN, "pan": {"value": 0, "mod": [{"src": "auto.walk", "amount": 1}]}, "sends": {"room": CANON_ROOM},
                                  "auto": {"spd": {"points": ca_spd, "curve": 0}, "walk": {"points": ca_pan, "curve": 0}}, "notes": canon_notes(ca_up, ca_steps)})
        doc["about"] = doc["about"].replace(" Generated by", f" From v22 two more decks have deck B's record, for four bars of 'both' (bars {int(ca_t0 // BEATS) + 1} to {int(ca_t1 // BEATS)}): one starts at half speed, an octave down, on the left, and winds up to double speed, an octave up, on the right; the other does the reverse. Each is the other backwards in speed, in pitch and in place, and they cross once, on the first beat of bar {int(ca_tc // BEATS) + 1}: for that one stroke both are at the record's own speed, on the same beat of it, in the middle, with the grid (a canon by acceleration: Nancarrow's Canon X, on turntables). Generated by")
        assert "From v22" in doc["about"]
    if wow_row() is not None:
        wo_b0 = wow_row(); wo_e = WOW_OFF / WOW_RADIUS; wo_c = 1200 * math.log2(1 + wo_e); wo_fw = fast_window(); wo_turn = SCAR_TURN * STEP * 60 / BPM
        if WOW_ORGAN:
            PATCHES["gt-organ"] = {"about": f"Give or Take's held chord (chirper-zero, 27 Nov, v23): an organ on deck B's record: {len(WOW_PARTS)} plain tones a note, held, so that nothing in it moves but the record. Its pitch follows deck B's speed (auto.spd), and in its row the record's hole is {WOW_OFF:g} mm off centre.",
                                   "play": {"vel_sens": 0.5, "gate": 1},
                                   "synth": {"layers": [f"sine phase=0 ratio={r:g} level={lv:g}dB" for r, lv in WOW_PARTS], "pitch": {"value": 0, "mod": [{"src": "auto.spd", "amount": 1}]}, "amp": {"a": "40ms", "d": "0s", "s": 1, "r": "120ms"}}}
            doc["tracks"].append({"name": "organ", "patch": "gt-organ", "gain": WOW_GAIN, "pan": WOW_PAN, "auto": {"spd": {"points": lane}}, "notes": wow_notes()})      # dry
        doc["about"] = doc["about"].replace(" Generated by", f" From v23 the hole in deck B's record is {WOW_OFF:g} mm off centre, and in the first row of 'locked' (bars {wo_b0 + 1} to {wo_b0 + ROW}) it can be heard: the record's speed goes {100 * wo_e:.2f}% up and down once a turn, so everything on it is {wo_c:.1f} cents sharp and then as flat, fastest when the scratch comes under the needle (its tick)." + (" A chord is held on the record there, an organ, to show it." if WOW_ORGAN else "") + f" A turn is {wo_turn:.2f} s; when the switch goes to the other speed (bar {int(wo_fw[0] // BEATS) + 1}) the chord goes up a fourth and the wow goes {FAST_BY:.3f} times as fast with it ({wo_turn / FAST_BY:.2f} s): it is the record that is going round, not the note that is shaking. Generated by")
        assert "From v23" in doc["about"]
    if up_span() is not None:
        up = up_ticks(); up_on, up_w = up_span(); up_pts = [["0b", round(up[0][3], 4)]]
        for _, up_at, _, up_st, up_ln, _ in up:                 # the lane holds each click's speed from just before it to just after
            up_pts += [[f"{up_at - 0.03:.5f}b", round(up_st, 4)], [f"{up_at + up_ln + 0.03:.5f}b", round(up_st, 4)]]
        up_pts.append([f"{TOTAL:g}b", round(up[-1][3], 4)])
        PATCHES["gt-up"] = {"about": f"Give or Take's record coming up to speed (chirper-zero, 27 Nov, v24): deck B's sixteenth click as the groove holds it, played at whatever speed the platter has: the engine's chip noise with no chip's clock, a shift register begun from the same state at every note and clocked from the note played ({UP_NOTE} at full speed) and the track's lane (auto.spd, semitones): every click is the same steps of the register, slower and longer the slower the platter. Then the headphone: the cue's own small speaker (nothing under 1.8 kHz, a ring at 3.2 kHz, little over 7 kHz), which does not slow down with the record.",
                            "play": {"vel_sens": 0.5, "gate": 1}, "synth": {"layers": [{"type": "chip", "chip": {"kind": "noise", "clock": 0}}], "pitch": {"value": 0, "mod": [{"src": "auto.spd", "amount": 1}]},
                            "filters": [{"kind": "hp", "cutoff": 1800, "q": 0.8}, "peak cutoff=3200 q=2 gain=6dB", "lp cutoff=7000"], "amp": {"a": "1ms", "d": "0s", "s": 1, "r": "3ms"}}}      # the cue's three filters: the same headphone. (The first whole-song pair was rendered without its top, lp 7000: the register's steps then put 0.1 dB more into the scorer's 9.2 and 14.8 kHz bands: put back)
        doc["tracks"].append({"name": "start", "patch": "gt-up", "gain": UP_GAIN or f"{float(CUE_GAIN[:-2]) + UP_TRIM:g}dB", "pan": CUE_PAN, "auto": {"spd": {"points": up_pts, "curve": 0}},
                              "notes": [{"at": round(at, 5), "len": round(ln, 5), "pitch": UP_NOTE, "vel": round(vel, 4)} for _, at, _, _, ln, vel in up]})      # dry: a headphone
        doc["about"] = doc["about"].replace(" Generated by", f" From v24 the song begins with deck B's motor switched on, as it ends with it switched off: in the headphone (the left ear), half a sixteenth after the first bass drum, the platter starts to turn, and takes {UP_BARS} bars to come up to speed, the {UP_BARS} bars it takes to stop. The record's sixteenth clicks come by at 2 times the square root of 1, 2, 3 ... beats: {len(up)} clicks, each sooner after the last, each the same click played at the speed the platter has: longer, lower and quieter the slower it is: the first at a quarter speed, two octaves down and four times as long. The sixteenth is the cue's first stroke, on bar {CUE_BARS[0] + 1}. Generated by")
        assert "From v24" in doc["about"]
    if beat_row() is not None:
        bt_b0 = beat_row() * BEATS; bt_off = round(beat_off(), 4); bt_far = max(abs(beat_apart(bt_b0 + i / 16)) for i in range(ROW * BEATS * 16 + 1))
        PATCHES["gt-beat"] = {"about": "Give or Take's beating tone (chirper-zero, 27 Nov, v25): one plain held tone whose pitch follows its track's lane (auto.spd, semitones): on deck A's track the lane is flat, on deck B's it is the record's speed. Two of them a wave apart are one; half a wave apart, nothing.",
                              "play": {"vel_sens": 0.5, "gate": 1}, "synth": {"layers": ["sine phase=0"], "pitch": {"value": 0, "mod": [{"src": "auto.spd", "amount": 1}]}, "amp": {"a": "40ms", "d": "0s", "s": 1, "r": "120ms"}}}
        bt_note = [{"at": bt_b0, "len": ROW * BEATS, "pitch": BEAT_NOTE, "vel": BEAT_VEL}]      # ONE note a deck for the whole row: a new note would start its wave again and the two would forget how far apart they are
        doc["tracks"].append({"name": "beat-a", "patch": "gt-beat", "gain": BEAT_GAIN, "pan": BEAT_PAN, "auto": {"spd": {"points": [["0b", bt_off], [f"{TOTAL:g}b", bt_off]], "curve": 0}}, "notes": bt_note})
        doc["tracks"].append({"name": "beat-b", "patch": "gt-beat", "gain": BEAT_GAIN, "pan": BEAT_PAN, "auto": {"spd": {"points": [[p[0], round(p[1] + bt_off, 4)] for p in lane], "curve": 0}}, "notes": [dict(n) for n in bt_note]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v25 the two records beat (bars {beat_row() + 1} to {beat_row() + ROW}): the same held tone is on both decks, {BEAT_WAVES} waves to the beat ({beat_hz():.2f} Hz), deck A's steady and deck B's turning with its record. Where the decks are a whole number of waves apart the two add; half a wave off they cancel: a throb for every 64th of a beat ({60000 / BPM / BEAT_WAVES:.2f} ms) the hand pushes deck B ahead: {bt_far:.0f} throbs out to a quarter of a beat and {bt_far:.0f} back, quickest when the record is moving fastest against the grid and still when it is furthest away. {len(beat_nulls())} silences in the row. Generated by")
        assert "From v25" in doc["about"]
    if LEAP and PIPS and CHIME and QUART:
        lp_pips = dict(pips_seconds())
        assert len(lp_pips[LEAP_GIVE]) == PIPS_BEFORE + 2 and len(lp_pips[LEAP_TAKE]) == PIPS_BEFORE
        assert lp_pips[LEAP_TAKE][-1][0] == LEAP_TAKE * CHIME_EVERY       # the clock is right again
        doc["about"] = doc["about"].replace(" Generated by", f" From v26 the clock is given a second and has one taken (the song's name). The minute that ends at {LEAP_GIVE}:00 has 61 seconds: the time signal has SEVEN pips, six short ones and the long one, which begins on {LEAP_GIVE}:01 of the song (a leap second: the clock reads 59:60). For the next minute the clock's {LEAP_GIVE} strokes and its three quarters are a second late against the record. The minute that ends at {LEAP_TAKE}:00 has 59 seconds: FIVE pips (the signal for a second taken out, which has never yet been sent), and the clock strikes {LEAP_TAKE} on {LEAP_TAKE}:00 of the song as it always did. Generated by")
        assert "From v26" in doc["about"]
    if SWING and swing_bar() is not None:
        sw_t = next(t for t in doc["tracks"] if t["name"] == SWING_PART)
        sw_n = 0
        for sw_k, (sw_long, sw_short) in enumerate(SWING_WALK):
            sw_a = (swing_bar() + sw_k * SWING_BARS) * BEATS
            for n in sw_t["notes"]:
                if sw_a <= n["at"] < sw_a + SWING_BARS * BEATS:
                    sw_pos = round(n["at"] % 0.5, 6)
                    assert sw_pos in (0.0, 0.25), (n["at"], "the hat is not on its sixteenths here")
                    if sw_pos == 0.25 and sw_long != sw_short:
                        n["at"] = round(n["at"] - 0.25 + swing_off(sw_long, sw_short), 5); sw_n += 1
        assert sw_n == sum(8 * SWING_BARS for a, b in SWING_WALK if a != b)      # eight off sixteenths a bar
        doc["about"] = doc["about"].replace(" Generated by", f" From v27 the grid is found: the hat comes in (bar {swing_bar() + 1}) swung, and is set straight a step at a time: in every pair of its sixteenths the long one stands to the short one as " + ", ".join(f"{a} to {b}" for a, b in SWING_WALK) + f", {SWING_BARS} bars each (a twelfth, an octave, a fifth and a unison, as time): {sw_n} strokes are late by " + ", ".join(f"{(swing_off(a, b) - 0.25) * 60000 / BPM:.1f}" for a, b in SWING_WALK if a != b) + " ms; no stroke on a beat or an off beat moves, and nothing is added. Generated by")
        assert "From v27" in doc["about"]
    if strobe_row() is not None:
        sb_ns = strobe_notes()
        PATCHES["gt-strobe"] = {"about": "Give or Take's strobe (chirper-zero, 27 Nov, v28): the lamp at the platter's edge: a plain tone with a little of its second and third over it, swelling for 15 ms and falling to a third in a quarter of a second; one note a flash.",
                                "play": {"vel_sens": 0}, "synth": {"layers": ["sine phase=0", "sine phase=0 ratio=2 level=-9dB", "sine phase=0 ratio=3 level=-15dB"], "filters": ["lp cutoff=7000"], "amp": {"a": "15ms", "d": "250ms", "s": 0.3, "r": "60ms"}}}
        doc["tracks"].append({"name": "strobe", "patch": "gt-strobe", "gain": STROBE_GAIN, "pan": 0.0, "notes": [{"at": round(t, 5), "len": STROBE_LEN, "pitch": p, "vel": 0.8} for t, _, p in sb_ns]})
        sb_far = max(abs(k) for _, k, _ in sb_ns)
        doc["about"] = doc["about"].replace(" Generated by", f" From v28 the strobe (bars {strobe_row() + 1} to {strobe_row() + ROW}, the first row of 'take'): a lamp flashes on every beat of the grid and the note under it says how far deck B's record is from the grid: {strobe_pitch(0)} when they are together, a note of the scale higher for every {1000 * 60 / BPM / STROBE_DOTS:.1f} ms the record is ahead, a note lower for every {1000 * 60 / BPM / STROBE_DOTS:.1f} ms behind ({len(sb_ns)} notes, {strobe_pitch(-sb_far)} to {strobe_pitch(sb_far)}). Generated by")
        assert "From v28" in doc["about"]
    if give_row() is not None:
        gv = give_notes(); gv_n = len(GIVE_TUNE)
        PATCHES["gt-give"] = {"about": "Give or Take's counting tune (chirper-zero, 27 Nov, v29): a soft hollow pluck: a plain tone with a little of its third and fifth harmonics, struck and gone in a fifth of a second; every note as loud as every other.",
                              "play": {"vel_sens": 0}, "synth": {"layers": ["sine phase=0", "sine phase=0 ratio=3 level=-12dB", "sine phase=0 ratio=5 level=-20dB"], "filters": ["lp cutoff=7000"], "amp": {"a": "1ms", "d": "200ms", "s": 0, "r": "60ms", "curve": 3}}}
        for gv_name, gv_giving, gv_pan in (("give", True, -GIVE_PAN), ("take", False, GIVE_PAN)):
            doc["tracks"].append({"name": gv_name, "patch": "gt-give", "gain": GIVE_GAIN, "pan": gv_pan, "notes": [{"at": round(t, 5), "len": GIVE_LEN, "pitch": p, "vel": 0.8} for t, p, _, _, g in gv if g == gv_giving]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v29 a tune is given and taken a note at a time (bars {give_row() + 1} to {give_row() + ROW}, the second row of 'both'): {' '.join(GIVE_TUNE)}: first its first note, then its first two, then three, until it is whole ({gv_n * (gv_n + 1) // 2} notes); then without its first note, without its first two, until only the last is left ({gv_n * (gv_n - 1) // 2} notes): {gv_n * gv_n} notes, {gv_n} squared, an eighth each: the row to the note. Generated by")
        assert "From v29" in doc["about"]
    if life_row() is not None:
        import math as lf_math
        lf_g = float(LIFE_GAIN.replace("dB", ""))
        PATCHES["gt-life"] = {"about": "Give or Take's string that runs down (chirper-zero, 28 Nov, v30): one plain held tone, 4 ms to come and 40 ms to go; its track's lane (auto.life, dB) is its whole shape: a straight line in dB by time, which is a half-life.",
                              "play": {"vel_sens": 0, "gate": 1}, "synth": {"layers": ["sine phase=0"], "filters": ["lp cutoff=7000"], "amp": {"a": "4ms", "d": "0s", "s": 1, "r": "40ms"}}}
        for lf_n, lf_p in enumerate(LIFE_NOTES, 1):
            doc["tracks"].append({"name": f"life-{lf_n}", "patch": "gt-life", "gain": f"{round(lf_g - LIFE_TILT * lf_math.log2(lf_n), 2):g}dB", "pan": 0.0, "auto": {"life": life_lane(lf_n)},
                                  "fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.life", "amount": 1}]}}],
                                  "notes": [{"at": t, "len": LIFE_EVERY - 0.2, "pitch": lf_p, "vel": 0.8} for t in life_strokes()]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v30 a string runs down (bars {life_row() + 1} to {life_row() + ROW}, the second row of 'the nudge'): struck every {LIFE_EVERY // BEATS} bars on {LIFE_NOTES[0]}, its first tone is half as loud after {LIFE_HALF / BEATS:g} bar, its second after a half of that, its third after a third, its fourth after a quarter ({', '.join(f'{6.0206 * n * BEATS / LIFE_HALF:.2f}' for n in range(1, len(LIFE_NOTES) + 1))} dB a bar): every tone is a clock that runs down and the string's colour says how long ago it was struck. Generated by")
        assert "From v30" in doc["about"]
    if arrow_mirror() is not None:
        import math as ar_math
        ar_g = float(ARROW_GAIN.replace("dB", "")); ar_b = BPM / 60; ar_e = arrow_ends()
        PATCHES["gt-arrow"] = {"about": "Give or Take's string heard before it is struck (chirper-zero, 28 Nov, v31): gt-life turned round: one plain held tone, 40 ms to come and 4 ms to go; its track's lane (auto.arrow, dB) is its whole shape: the string's line run backwards.",
                               "play": {"vel_sens": 0, "gate": 1}, "synth": {"layers": ["sine phase=0"], "filters": ["lp cutoff=7000"], "amp": {"a": f"{1000 * ARROW_COME:g}ms", "d": "0s", "s": 1, "r": f"{1000 * ARROW_GO:g}ms"}}}
        for ar_n, ar_p in enumerate(LIFE_NOTES, 1):
            doc["tracks"].append({"name": f"arrow-{ar_n}", "patch": "gt-arrow", "gain": f"{round(ar_g - LIFE_TILT * ar_math.log2(ar_n), 2):g}dB", "pan": 0.0, "auto": {"arrow": arrow_lane(ar_n)},
                                  "fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.arrow", "amount": 1}]}}],
                                  "notes": [{"at": round(e - (LIFE_EVERY - 0.2) - ARROW_COME * ar_b, 5), "len": round(LIFE_EVERY - 0.2 + (ARROW_COME - ARROW_GO) * ar_b, 5), "pitch": ar_p, "vel": 0.8} for e in ar_e]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v31 the string is heard before it is struck (bars {int(ar_e[0] - (LIFE_EVERY - 0.2)) // BEATS + 1} to {int(ar_e[-1]) // BEATS + 1}): the string of bars {life_row() + 1} to {life_row() + ARROW_STROKES * LIFE_EVERY // BEATS} run backwards about the first beat of bar {arrow_mirror() // BEATS + 1}: it grows out of nothing, the low tone first and the upper ones later and faster ({', '.join(f'{6.0206 * n * BEATS / LIFE_HALF:.1f}' for n in range(1, len(LIFE_NOTES) + 1))} dB a bar), and stops dead {BEATS - ar_e[0] % BEATS:g} of a beat before bars {' and '.join(str(int(e) // BEATS + 2) for e in ar_e)}. Generated by")
        assert "From v31" in doc["about"]
    if fuse_row() is not None:
        fu_hz = BPM / 60 * FUSE_WAVES; fu = fuse_waves(); fu_n = sum(b for _, b in FUSE_STEPS); fu_h = next(b for r, b in FUSE_STEPS if r == FUSE_WAVES)
        PATCHES["gt-fuse"] = {"about": f"Give or Take's beat that becomes a note (chirper-zero, 28 Nov, v32): one wave of a plain tone of {FUSE_WAVES} waves to the beat ({fu_hz:.2f} Hz), begun and ended where it crosses nothing: no time to come or to go. {FUSE_WAVES} of them a beat are one held note.",
                              "play": {"vel_sens": 0, "gate": 1}, "synth": {"layers": ["sine phase=0"], "pitch": {"value": round(12 * math.log2(fu_hz / FUSE_NOTE[1]), 7)}, "filters": ["lp cutoff=7000"], "amp": {"a": "0ms", "d": "0s", "s": 1, "r": "0ms"}}}
        doc["tracks"].append({"name": "fuse", "patch": "gt-fuse", "gain": FUSE_GAIN, "pan": 0.0, "notes": [{"at": round(t, 7), "len": round(1 / FUSE_WAVES, 7), "pitch": FUSE_NOTE[0], "vel": 0.8} for t, _ in fu]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v32 a beat becomes a note (bars {fuse_row() + 1} to {fuse_row() + fu_n // BEATS}): one wave of a low tone ({fu_hz:.1f} Hz: {FUSE_WAVES} waves to the beat) once a beat, then {', '.join(str(r) for r, _ in FUSE_STEPS[1:[r for r, _ in FUSE_STEPS].index(FUSE_WAVES)])} and {FUSE_WAVES} times a beat: at {FUSE_WAVES} the waves stand end to end and are one held note of {fu_h} beats, whose pitch is the tempo; then it comes apart the same way. {len(fu)} waves, all alike. Generated by")
        assert "From v32" in doc["about"]
    if talea_row() is not None:
        tn = talea_notes()
        PATCHES["gt-talea"] = {"about": "Give or Take's tune on a soft hammer (chirper-zero, 28 Nov, v33): a plain tone with its octave (-9 dB) and its twelfth (-15 dB), struck and gone in 200 ms; nothing over 7 kHz. Its loudness goes as the square of the velocity.",
                               "play": {"vel_sens": 1}, "synth": {"layers": ["sine phase=0", "sine phase=0 ratio=2 level=-9dB", "sine phase=0 ratio=3 level=-15dB"], "filters": ["lp cutoff=7000"], "amp": {"a": "1ms", "d": "200ms", "s": 0, "r": "60ms", "curve": 3}}}
        doc["tracks"].append({"name": "talea", "patch": "gt-talea", "gain": f"{float(TALEA_GAIN[:-2]) + max(TALEA_EVEN):g}dB", "pan": 0.0, "notes": [note(at, p, ln, 10 ** ((TALEA_EVEN[pl] - max(TALEA_EVEN)) / 40)) for at, ln, p, pl, _ in tn]})   # the patch's loudness goes as the square of the velocity: 40 dB for ten times
        doc["about"] = doc["about"].replace(" Generated by", f" From v33 the tune and its rhythm go round at different speeds (bars {talea_row() + 1} to {talea_row() + ROW}): a rhythm of {len(TALEA_STEPS)} notes to the bar ({' '.join(str(x) for x in TALEA_STEPS)} sixteenths) and the tune of {len(TALEA_TUNE)} notes ({' '.join(TALEA_TUNE)}): in {len(tn)} notes the rhythm goes round {len(tn) // len(TALEA_STEPS)} times and the tune {len(tn) // len(TALEA_TUNE)}; they begin together only at the row's two ends. Generated by")
        assert "From v33" in doc["about"]
    if fair_row() is not None:
        fs = fair_strokes(); f_len = round(FAIR_MS / 1000 * BPM / 60, 7)
        PATCHES["gt-fair"] = {"about": f"Give or Take's pip for the rhythm at three speeds (chirper-zero, 28 Nov, v34): a plain tone, {FAIR_MS} ms; nothing over 2 kHz is played on it. Its loudness goes as the square of the velocity.",
                              "play": {"vel_sens": 1, "gate": 1}, "synth": {"layers": ["sine phase=0"], "filters": ["lp cutoff=7000"], "amp": {"a": "3ms", "d": "0s", "s": 1, "r": "15ms"}}}
        for j, st in enumerate(FAIR_STEPS):
            doc["tracks"].append({"name": f"fair-{st}", "patch": "gt-fair", "gain": FAIR_GAIN, "pan": 0.0, "notes": [{"at": round(at, 7), "len": f_len, "pitch": FAIR_NOTES[j], "vel": round(10 ** (FAIR_TRIM[pl] / 40), 5)} for at, v, _, pl in fs if v == j]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v34 one rhythm goes at three speeds and they never disagree (bars {fair_row() + 1} to {fair_row() + ROW}): the fair way to take turns (strike place n if n written in twos has an even number of ones) played on the sixteenths, on the eighths and on the beats at once, each speed on its own note; every second place of the rhythm is the same rhythm at half the speed, so a slower voice never strikes where a faster one rests. Generated by")
        assert "From v34" in doc["about"]
    if faster_row() is not None:
        fs_ = faster_strokes()
        PATCHES["gt-faster"] = {"about": f"Give or Take's pip for the beat that speeds up for ever (chirper-zero, 28 Nov, v35): a plain tone, {FASTER_MS} ms, {FASTER_EDGE} ms to come and to go. Its loudness goes as the square of the velocity.",
                                "play": {"vel_sens": 1, "gate": 1}, "synth": {"layers": ["sine phase=0"], "filters": ["lp cutoff=7000"], "amp": {"a": f"{FASTER_EDGE}ms", "d": "0s", "s": 1, "r": f"{FASTER_EDGE}ms"}}}
        doc["tracks"].append({"name": "faster", "patch": "gt-faster", "gain": FASTER_GAIN, "pan": 0.0, "notes": [{"at": round(t, 6), "len": round(FASTER_MS / 1000 * BPM / 60, 6), "pitch": FASTER_NOTE, "vel": round(amp ** 0.5, 5)} for _, _, t, amp, _ in fs_]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v35 a beat speeds up for ever (bars {faster_row() + 1} to {faster_row() + ROW}): a pip struck faster and faster, twice as fast after every {FASTER_TURN // BEATS} bars, and after every {FASTER_TURN // BEATS} bars exactly where it began: {FASTER_LAYERS} beats at once, each twice as fast as the one below, all speeding up alike, the fastest fading out and a new slowest fading in (Risset's rhythm). Generated by")
        assert "From v35" in doc["about"]
    if slower_row() is not None:
        doc["tracks"].append({"name": "slower", "patch": "gt-faster", "gain": SLOWER_GAIN, "pan": 0.0, "notes": [{"at": round(t, 6), "len": round(FASTER_MS / 1000 * BPM / 60, 6), "pitch": SLOWER_NOTE, "vel": round(amp ** 0.5 * 10 ** ((SLOWER_TRIM.get((turn, j), 0.0) - max(SLOWER_TRIM.values(), default=0.0)) / 40), 5)} for turn, j, t, amp, _ in slower_strokes()]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v36 the beat slows for ever (bars {slower_row() + 1} to {slower_row() + ROW}): the strokes of bars {faster_row() + 1} to {faster_row() + ROW} turned round about the line between the two rows: what sped up for ever slows for ever, while the record itself runs down to a stop. Generated by")
        assert "From v36" in doc["about"]
    if shrink_row() is not None:
        sc_ = shrink_clicks(); s_top = max(SHRINK_TRIM); s_ms = 60000 / BPM
        PATCHES["gt-shrink"] = {"about": f"Give or Take's click for the three clicks (chirper-zero, 28 Nov, v37): a plain tone held {SHRINK_MS} ms, {SHRINK_EDGE[0]} ms to come and {SHRINK_EDGE[1]} to go. Its loudness goes as the square of the velocity.",
                                "play": {"vel_sens": 1, "gate": 1}, "synth": {"layers": ["sine phase=0"], "filters": ["lp cutoff=6000"], "amp": {"a": f"{SHRINK_EDGE[0]}ms", "d": "0s", "s": 1, "r": f"{SHRINK_EDGE[1]}ms"}}}
        doc["tracks"].append({"name": "shrink", "patch": "gt-shrink", "gain": SHRINK_GAIN, "pan": 0.0, "notes": [{"at": round(t, 6), "len": round(SHRINK_MS / s_ms, 6), "pitch": SHRINK_NOTE, "vel": round(10 ** ((SHRINK_TRIM[i] - s_top) / 40), 5)} for i, t, _, _, _ in sc_]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v37 give or take thirty milliseconds (bars {shrink_row() + 1} to {shrink_row() + ROW}): three clicks, the first and the last always {SHRINK_SPAN * s_ms:.0f} ms apart; the middle one in the middle, then {(SHRINK_MID['even'] - SHRINK_MID['short-long']) * s_ms:.0f} ms early (short, long: said to sound even), then {(SHRINK_MID['long-short'] - SHRINK_MID['even']) * s_ms:.0f} ms late (long, short: said to sound uneven), then the two side by side. Generated by")
        assert "From v37" in doc["about"]
    if chance_row() is not None:
        cp_ = chance_pips(); h_top = max(CHANCE_TRIM)
        PATCHES["gt-chance"] = {"about": f"Give or Take's plain pip for chance and for the spread (chirper-zero, 28 Nov, v38): one sine, {CHANCE_EDGE[0]} ms to come and {CHANCE_EDGE[1]} to go. Its loudness goes as the square of the velocity.",
                                "play": {"vel_sens": 1, "gate": 1}, "synth": {"layers": ["sine phase=0"], "filters": ["lp cutoff=2000"], "amp": {"a": f"{CHANCE_EDGE[0]}ms", "d": "0s", "s": 1, "r": f"{CHANCE_EDGE[1]}ms"}}}
        doc["tracks"].append({"name": "chance", "patch": "gt-chance", "gain": CHANCE_GAIN, "pan": 0.0, "notes": [{"at": round(t, 6), "len": CHANCE_LEN, "pitch": CHANCE_NOTE, "vel": round(10 ** ((CHANCE_TRIM[i] - h_top) / 40), 5)} for i, t, _ in cp_]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v38 chance comes in clumps (bars {chance_row() + 1} to {chance_row() + ROW}): eight pips to two bars, on the sixteenths, four times: spread by the golden ratio, thrown by chance, spread, thrown. Generated by")
        assert "From v38" in doc["about"]
    if poly_row() is not None:
        ps_ = poly_strokes(); p_top = max(POLY_TRIM[v][k] - dn for v, j, k, t, dn in ps_)
        PATCHES["gt-wood"] = {"about": f"Give or Take's wooden stroke for five against seven (chirper-zero, 28 Nov, v39): a saw under 520 Hz that dies in {POLY_LEN} ms. Its loudness goes as the square of the velocity.",
                              "play": {"vel_sens": 1, "gate": 1}, "synth": {"layers": ["saw"], "filters": ["lp cutoff=520", "lp cutoff=520"], "amp": {"a": "0.5ms", "d": f"{POLY_LEN}ms", "s": 0, "r": "5ms"}}}
        for p_v in (0, 1):
            doc["tracks"].append({"name": f"even-{POLY_N[p_v]}", "patch": "gt-wood", "gain": POLY_GAIN, "pan": POLY_PAN[p_v], "notes": [{"at": round(t, 6), "len": 0.1, "pitch": POLY_NOTE[p_v], "vel": round(10 ** ((POLY_TRIM[v][k] - dn - p_top) / 40), 5)} for v, j, k, t, dn in ps_ if v == p_v]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v39 five against seven (bars {poly_row() + 1} to {poly_row() + ROW}): a wooden stroke five times a bar, evenly, and another seven times a bar; the five alone for two bars, both for four, the seven alone for two. They agree once a bar, and a bar's strokes read the same backwards. Generated by")
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


if __name__ == "__main__":
    if os.environ.get("C11T1_SHOW"):
        if poly_row() is not None:
            from fractions import Fraction as Fr
            ps_ = poly_strokes(); p_sec = poly_row() * BEATS * 60 / BPM; p_bar = BEATS * 60000 / BPM; p_near = sorted((abs(Fr(a_, POLY_N[0]) - Fr(b_, POLY_N[1])), a_, b_) for a_ in range(1, POLY_N[0]) for b_ in range(1, POLY_N[1])); p_min = p_near[0][0]
            print(f"five against seven ({POLY_GAIN}), bars {poly_row() + 1}-{poly_row() + ROW} ({int(p_sec) // 60}:{p_sec % 60:04.1f}): a wooden stroke (a saw under 520 Hz, {POLY_LEN} ms) ; " + " ; ".join(f"{POLY_NOTE[v]} ({poly_hz(POLY_NOTE[v]):.1f} Hz) {POLY_N[v]} times a bar, every {BEATS / POLY_N[v]:.4f} of a beat ({p_bar / POLY_N[v]:.1f} ms), pan {POLY_PAN[v]:g}, bars {poly_row() + 1 + POLY_BARS[v][0]}-{poly_row() + POLY_BARS[v][1]}" for v in (0, 1)) + f" ; {len(ps_)} strokes ; they agree on the first beat of the bar and nowhere else ; nearest after that {p_min} of a bar ({float(p_min) * p_bar:.1f} ms): " + ", ".join(f"the five's stroke {a_ + 1} {'before' if Fr(a_, POLY_N[0]) < Fr(b_, POLY_N[1]) else 'after'} the seven's stroke {b_ + 1}" for d_, a_, b_ in p_near if d_ == p_min) + " ; read backwards from the next bar line a bar's strokes are the same ; the song's five (sixteenths " + " ".join(str(x) for x in FIVE) + ") is the even five rounded down to the grid: " + " ".join(f"{(16 * k / POLY_N[0] - FIVE[k]) * p_bar / 16:.1f}" for k in range(POLY_N[0])) + f" ms early ; the last bar's strokes each {POLY_FALL:g} dB under the one before" + (" ; trims by place: the five " + " ".join(f"{x:+.1f}" for x in POLY_TRIM[0]) + ", the seven " + " ".join(f"{x:+.1f}" for x in POLY_TRIM[1]) + " dB" if any(POLY_TRIM[0]) or any(POLY_TRIM[1]) else " ; no trims"))
        if chance_row() is not None:
            import math as _m
            h_sec = chance_row() * BEATS * 60 / BPM; ways = _m.comb(CHANCE_SLOTS, CHANCE_N); apart = _m.comb(CHANCE_SLOTS - CHANCE_N + 1, CHANCE_N)
            print(f"chance comes in clumps ({CHANCE_GAIN}), bars {chance_row() + 1}-{chance_row() + ROW} ({int(h_sec) // 60}:{h_sec % 60:04.1f}): {CHANCE_N} pips ({CHANCE_NOTE}, {chance_hz():.1f} Hz, {CHANCE_LEN * 60000 / BPM:.0f} ms) to {CHANCE_SLOTS} sixteenths, {len(CHANCE_ORDER)} times ; " + " ; ".join(f"bars {chance_row() + 1 + p * CHANCE_SLOTS // 16}-{chance_row() + (p + 1) * CHANCE_SLOTS // 16} {kind}: sixteenths " + " ".join(str(v) for v in sls) + f" ({chance_stats(sls)[0]} side by side, the longest silence {chance_stats(sls)[1]})" for p, (kind, sls) in enumerate(chance_phrases())) + f" ; of the {ways} ways to draw {CHANCE_N} of {CHANCE_SLOTS}, {apart} ({100 * apart / ways:.1f} in a hundred) have no two side by side" + (f" ; trims {min(CHANCE_TRIM):+.1f} to {max(CHANCE_TRIM):+.1f} dB" if any(CHANCE_TRIM) else " ; no trims"))
        if shrink_row() is not None:
            sc_ = shrink_clicks(); k_sec = shrink_row() * BEATS * 60 / BPM; k_ms = 60000 / BPM
            print(f"give or take thirty milliseconds ({SHRINK_GAIN}), bars {shrink_row() + 1}-{shrink_row() + ROW} ({int(k_sec) // 60}:{k_sec % 60:04.1f}): {len(sc_)} clicks ({SHRINK_NOTE}, {SHRINK_MS} ms) in {len(SHRINK_ORDER)} triples on beats {' '.join(f'{x:g}' for x in SHRINK_AT)} of every bar ; the first and the last click {SHRINK_SPAN:g} of a beat apart ({SHRINK_SPAN * k_ms:.1f} ms) ; the middle click after " + " ; ".join(f"{k}: {v:g} of a beat (gaps {v * k_ms:.1f} and {(SHRINK_SPAN - v) * k_ms:.1f} ms)" for k, v in SHRINK_MID.items()) + " ; triple by triple (e even, s short-long, l long-short): " + " ".join(k[0] for k in SHRINK_ORDER) + (f" ; trims {min(SHRINK_TRIM):+.1f} to {max(SHRINK_TRIM):+.1f} dB" if any(SHRINK_TRIM) else " ; no trims"))
        if slower_row() is not None:
            sl_ = slower_strokes(); s_sec = slower_row() * BEATS * 60 / BPM; s_ms = 60000 / BPM; s_g = lambda k: [t for _, _, t, _, ks in sl_ if k in ks]
            print(f"the beat that slows for ever ({SLOWER_GAIN}), bars {slower_row() + 1}-{slower_row() + ROW} ({int(s_sec) // 60}:{s_sec % 60:04.1f}): the {len(sl_)} strokes of bars {faster_row() + 1}-{faster_row() + ROW} turned round about beat {slower_row() * BEATS} (the line of bar {slower_row() + 1}): a pip ({SLOWER_NOTE}, {FASTER_MS} ms) that began t beats before the line ends t beats after it ; the first begins on beat {sl_[0][2] - slower_row() * BEATS:.4f} of the row, the last on {sl_[-1][2] - slower_row() * BEATS:.4f} ; each beat's first gap and last gap in the row (ms): " + " ; ".join(f"{(s_g(k)[1] - s_g(k)[0]) * s_ms:.0f} to {(s_g(k)[-1] - s_g(k)[-2]) * s_ms:.0f}" for k in range(FASTER_LAYERS)) + (f" ; trims {min(SLOWER_TRIM.values()):+.1f} to {max(SLOWER_TRIM.values()):+.1f} dB on {len(SLOWER_TRIM)} strokes" if SLOWER_TRIM else " ; no trims"))
        if faster_row() is not None:
            fs_ = faster_strokes(); f_sec = faster_row() * BEATS * 60 / BPM; f_ms = 60000 / BPM; f_t = [q for q in fs_ if q[0] == 0]
            print(f"the beat that speeds up for ever ({FASTER_GAIN}), bars {faster_row() + 1}-{faster_row() + ROW} ({int(f_sec) // 60}:{f_sec % 60:04.1f}): a pip ({FASTER_NOTE}, {FASTER_MS} ms) ; a turn is {FASTER_TURN} beats, from beat {FASTER_FROM:g} of every {FASTER_TURN // BEATS} bars ; {FASTER_LAYERS} beats at once of {', '.join(str(FASTER_N * 2 ** k) for k in range(FASTER_LAYERS))} strokes a turn ; each one's first gap and last gap in a turn (ms): " + " ; ".join(f"{FASTER_TURN * math.log2(1 + 1 / (FASTER_N * 2 ** k)) * f_ms:.0f} to {FASTER_TURN * (1 - math.log2(2 - 1 / (FASTER_N * 2 ** k))) * f_ms:.0f}" for k in range(FASTER_LAYERS)) + f" ; {len(f_t)} strokes a turn, {len(fs_)} in all (those under {FASTER_FLOOR:g} dB left out) ; a stroke of all {FASTER_LAYERS} beats is written 0.0 dB, one of the fastest alone " + " to ".join(f"{20 * math.log10(q[3]):.1f}" for q in (min((q for q in f_t if len(q[4]) == 1), key=lambda q: q[1]), max((q for q in f_t if len(q[4]) == 1), key=lambda q: q[1]))) + " dB")
        if fair_row() is not None:
            fs = fair_strokes(); f_sec = fair_row() * BEATS * 60 / BPM; f_set = [{round(at, 6) for at, v, _, _ in fs if v == j} for j in range(len(FAIR_STEPS))]
            print(f"one rhythm at three speeds, and they never disagree ({FAIR_GAIN}), bars {fair_row() + 1}-{fair_row() + ROW} ({int(f_sec) // 60}:{f_sec % 60:04.1f}): place n is struck if n written in twos has an even number of ones: " + " ".join("".join("x" if fair_struck(4 * q + r) else "." for r in range(4)) for q in range(8)) + " ... ; " + " ; ".join(f"every {st} sixteenth(s) on {FAIR_NOTES[j]}: {len(f_set[j])} strokes of {ROW * BEATS * 4 // st} places" for j, st in enumerate(FAIR_STEPS)) + " ; " + " ; ".join(f"{len(f_set[j] & f_set[j - 1])} of the {len(f_set[j])} strokes on {FAIR_NOTES[j]} fall on a stroke on {FAIR_NOTES[j - 1]}" for j in range(1, len(FAIR_STEPS))) + f" ; the bars that begin with a stroke: {' '.join(str(fair_row() + b + 1) for b in range(ROW) if fair_struck(b))} (the same rule) ; {FAIR_MS} ms a stroke ; trims by sixteenth of the bar (dB): " + " ".join(f"{t:g}" for t in FAIR_TRIM))
        if talea_row() is not None:
            tn = talea_notes(); tl_sec = talea_row() * BEATS * 60 / BPM
            print(f"the tune and its rhythm go round ({TALEA_GAIN}), bars {talea_row() + 1}-{talea_row() + ROW} ({int(tl_sec) // 60}:{tl_sec % 60:04.1f}): the rhythm {' '.join(str(x) for x in TALEA_STEPS)} sixteenths ({len(TALEA_STEPS)} notes a bar, on beats {' '.join(f'{(t[0] - talea_row() * BEATS):g}' for t in tn[:len(TALEA_STEPS)])}) ; the tune {' '.join(TALEA_TUNE)} ({len(TALEA_TUNE)} notes) ; {len(tn)} notes: the rhythm {len(tn) // len(TALEA_STEPS)} times, the tune {len(tn) // len(TALEA_TUNE)} times ; bar by bar: " + " | ".join(" ".join(t[2] for t in tn[b * len(TALEA_STEPS):(b + 1) * len(TALEA_STEPS)]) for b in range(ROW)) + f" ; raised by place (dB): {' '.join(f'{x:+g}' for x in TALEA_EVEN)} ; each note of the tune in each place of the bar once: {sorted({(t[3], t[4]) for t in tn}) == [(i, j) for i in range(len(TALEA_STEPS)) for j in range(len(TALEA_TUNE))]}")
        if fuse_row() is not None:
            fu = fuse_waves(); fu_n = sum(b for _, b in FUSE_STEPS); fu_hz = BPM / 60 * FUSE_WAVES; fu_h = next(b for r, b in FUSE_STEPS if r == FUSE_WAVES)
            print(f"a beat becomes a note ({FUSE_GAIN}), bars {fuse_row() + 1}-{fuse_row() + fu_n // BEATS} ({int(fuse_row() * BEATS * 60 / BPM) // 60}:{fuse_row() * BEATS * 60 / BPM % 60:04.1f}): one wave of {fu_hz:.2f} Hz ({FUSE_WAVES} waves to the beat: {FUSE_NOTE[0]} {1200 * math.log2(fu_hz / FUSE_NOTE[1]):+.0f} cents ; {1000 / fu_hz:.2f} ms), all alike ; waves a beat, beat by beat: " + " ".join(str(r) for r, b in FUSE_STEPS for _ in range(b)) + f" ; {len(fu)} waves ; at {FUSE_WAVES} a beat they stand end to end: one held note of {fu_h} beats ({fu_h * 60 / BPM:.2f} s)")
        if arrow_mirror() is not None:
            ar_e = arrow_ends(); ar_b = int(ar_e[0] - (LIFE_EVERY - 0.2)) // BEATS
            print(f"time's arrow ({ARROW_GAIN}), bars {ar_b + 1}-{int(ar_e[-1]) // BEATS + 1} ({int(ar_b * BEATS * 60 / BPM) // 60}:{ar_b * BEATS * 60 / BPM % 60:04.1f}): the string of bars {life_row() + 1}-{life_row() + ARROW_STROKES * LIFE_EVERY // BEATS} turned round about beat {arrow_mirror()} (the first beat of bar {arrow_mirror() // BEATS + 1}) ; its tones {' '.join(LIFE_NOTES)} ; the nth rises {6.0206 * BEATS / LIFE_HALF:.2f} n dB a bar ; it comes in {1000 * ARROW_COME:g} ms and stops in {1000 * ARROW_GO:g} ms")
            for e in ar_e:
                print(f"   from beat {(e - (LIFE_EVERY - 0.2)) % BEATS:.3f} of bar {int(e - (LIFE_EVERY - 0.2)) // BEATS + 1} to beat {e % BEATS:.3f} of bar {int(e) // BEATS + 1}, where it stops dead: the stroke it is the film of is on beat {(2 * arrow_mirror() - e) % BEATS:.3f} of bar {int(2 * arrow_mirror() - e) // BEATS + 1}")
        if life_row() is not None:
            lf_b = life_row()
            print(f"half-life ({LIFE_GAIN}), bars {lf_b + 1}-{lf_b + ROW} ({int(lf_b * BEATS * 60 / BPM) // 60}:{lf_b * BEATS * 60 / BPM % 60:04.1f}): a string struck on beat {LIFE_AT:g} of every {LIFE_EVERY // BEATS} bars ({len(life_strokes())} strokes) ; its tones {' '.join(LIFE_NOTES)} ; the nth is {LIFE_TILT:g} dB under the first for each doubling of n at the stroke and halves every {LIFE_HALF:g}/n beats: " + ' ; '.join(f"{p}: {6.0206 * n * BEATS / LIFE_HALF:.2f} dB a bar, {-6.0206 * n * (LIFE_EVERY - 0.2) / LIFE_HALF:.1f} dB when it is let go" for n, p in enumerate(LIFE_NOTES, 1)))
        if give_row() is not None:
            gv = give_notes(); gv_b = give_row(); gv_n = len(GIVE_TUNE)
            print(f"give or take a note ({GIVE_GAIN}), bars {gv_b + 1}-{gv_b + ROW} ({int(gv_b * BEATS * 60 / BPM) // 60}:{gv_b * BEATS * 60 / BPM % 60:04.1f}): the tune {' '.join(GIVE_TUNE)} ; given a note at a time ({gv_n * (gv_n + 1) // 2} notes, pan {-GIVE_PAN:g}), then taken a note at a time from the front ({gv_n * (gv_n - 1) // 2} notes, pan {GIVE_PAN:g}): {len(gv)} notes = {gv_n} squared ; one every {GIVE_STEP:g} beat from beat {GIVE_AT:g}")
            print("   the passes: " + " | ".join(" ".join(GIVE_TUNE[j] for j in ps) for ps in give_passes()))
            print("   the first note of the tune falls on eighths " + " ".join(str(k) for k, (_, _, j, _, _) in enumerate(gv) if j == 0) + " of the row (apart by " + " ".join(str(b - a) for a, b in zip([k for k, x in enumerate(gv) if x[2] == 0], [k for k, x in enumerate(gv) if x[2] == 0][1:])) + ") ; the last note on eighths " + " ".join(str(k) for k, (_, _, j, _, _) in enumerate(gv) if j == gv_n - 1) + " (apart by " + " ".join(str(b - a) for a, b in zip([k for k, x in enumerate(gv) if x[2] == gv_n - 1], [k for k, x in enumerate(gv) if x[2] == gv_n - 1][1:])) + ")")
        if strobe_row() is not None:
            sb_ns = strobe_notes(); sb_b = strobe_row()
            print(f"the strobe ({STROBE_GAIN}), bars {sb_b + 1}-{sb_b + ROW} ({int(sb_b * BEATS * 60 / BPM) // 60}:{sb_b * BEATS * 60 / BPM % 60:04.1f}): a flash on every beat of the grid ; a dot is 1/{STROBE_DOTS} of a beat ({1000 * 60 / BPM / STROBE_DOTS:.2f} ms) ; the dot on its mark is {strobe_pitch(0)} ; {len(sb_ns)} notes, held {STROBE_LEN} of a beat")
            for sb_k in range(ROW):
                print(f"   bar {sb_b + sb_k + 1}: " + " ; ".join(f"{p} ({k:+d} dots: the record {1000 * 60 / BPM * d(t):+.1f} ms)" for t, k, p in sb_ns[sb_k * BEATS:(sb_k + 1) * BEATS]))
        if SWING and swing_bar() is not None:
            print(f"the grid is found (the {SWING_PART}'s swing), bars {swing_bar() + 1}-{swing_bar() + len(SWING_WALK) * SWING_BARS} ({int(swing_bar() * BEATS * 60 / BPM) // 60}:{swing_bar() * BEATS * 60 / BPM % 60:04.1f}): long to short, {SWING_BARS} bars each: " + " ; ".join(
                f"{a}:{b} (bars {swing_bar() + k * SWING_BARS + 1}-{swing_bar() + (k + 1) * SWING_BARS}: the off sixteenth at {swing_off(a, b):.4f} of a beat, {(swing_off(a, b) - 0.25) * 60000 / BPM:.1f} ms late)" for k, (a, b) in enumerate(SWING_WALK)))
        if LEAP and PIPS and CHIME and QUART:
            print(f"give or take a second: the minute that ends at {LEAP_GIVE}:00 has 61 seconds, the minute that ends at {LEAP_TAKE}:00 has 59 ; pips (seconds of the song): " + " ; ".join(f"minute {lp_k}: {len(lp_ps)} pips at " + " ".join(f"{lp_s // 60}:{lp_s % 60:02d}" for lp_s, _ in lp_ps) for lp_k, lp_ps in pips_seconds()) + " ; strokes: " + " ; ".join(f"{lp_k}: " + " ".join(f"{lp_s // 60}:{lp_s % 60:02d}" for lp_s in lp_ss) for lp_k, lp_ss in chime_strikes()) + " ; quarters a second late: " + " ".join(f"{int(lp_q[0]) // 60}:{int(lp_q[0]) % 60:02d}" for lp_q in quart_chimes() if lp_q[0] % QUART_EVERY))
        if beat_row() is not None:
            bt_n = beat_nulls(); bt_sec = 60 / BPM
            print(f"the two records beat, bars {beat_row() + 1}-{beat_row() + ROW} ({int(beat_row() * BEATS * bt_sec) // 60}:{beat_row() * BEATS * bt_sec % 60:04.1f}): a tone of {BEAT_WAVES} waves to the beat ({beat_hz():.2f} Hz: {BEAT_NOTE} {beat_off() * 100:+.0f} cents) on both decks, {BEAT_GAIN} each, pan {BEAT_PAN:g} ; a throb is {60000 / BPM / BEAT_WAVES:.2f} ms of drift ; {len(bt_n)} silences")
            for bt_bar in range(beat_row(), beat_row() + ROW):
                bt_in = [x for x in bt_n if bt_bar * BEATS <= x[0] < (bt_bar + 1) * BEATS]
                print(f"   bar {bt_bar + 1}: the decks {beat_apart(bt_bar * BEATS):+.2f} waves apart at its start ({1000 * d(bt_bar * BEATS) * bt_sec:+.1f} ms), deck B {speed_st(bt_bar * BEATS + 2):+.2f} semitones at its middle ({beat_hz() * (speed(bt_bar * BEATS + 2) - 1):+.2f} throbs a second) ; {len(bt_in)} silences, on sixteenths " + " ".join(f"{(x[0] - bt_bar * BEATS) / STEP:.2f}" for x in bt_in))
        if up_span() is not None:
            up_on, up_w = up_span()
            print(f"the record is started (the stop's mirror): the motor goes on at beat {up_on:g} and the platter takes {up_w:g} beats ({up_w * 60 / BPM:.2f} s) ; {len(up_ticks())} clicks in the left ear before the cue's first stroke (beat {up_on + up_w:g}) ; click: beat, speed, semitones, ms long, vel: " + " ; ".join(f"{k}: {at:.3f} {sp:.3f} {st:+.1f} {ln * 60 / BPM * 1000:.0f} {vel:.2f}" for k, at, sp, st, ln, vel in up_ticks()))
        if wow_row() is not None:
            wo_b0 = wow_row(); wo_sec = 60 / BPM; wo_fw = fast_window(); wo_e = WOW_OFF / WOW_RADIUS
            print(f"the hole is off centre (wow), bars {wo_b0 + 1}-{wo_b0 + ROW} ({int(wo_b0 * BEATS * wo_sec) // 60}:{wo_b0 * BEATS * wo_sec % 60:04.1f}): {WOW_OFF:g} mm off at {WOW_RADIUS:g} mm: the speed {100 * wo_e:.2f}% up and down, {1200 * math.log2(1 + wo_e):+.1f} to {1200 * math.log2(1 - wo_e):+.1f} cents, once a turn ; a turn is {SCAR_TURN} sixteenths of the record: {SCAR_TURN * STEP:g} beats ({SCAR_TURN * STEP * wo_sec:.3f} s) until bar {int(wo_fw[0] // BEATS) + 1}, then {SCAR_TURN * STEP / FAST_BY:g} beats ({SCAR_TURN * STEP * wo_sec / FAST_BY:.3f} s) ; {(wow_turns((wo_b0 + ROW) * BEATS) - wow_turns(wo_b0 * BEATS)):.2f} turns in the row ; the organ {'(' + WOW_GAIN + ', pan ' + str(WOW_PAN) + ')' if WOW_ORGAN else 'OFF'}")
            print("   sharpest (the scratch under the needle) at bar:sixteenth " + " ".join(f"{int(t // BEATS) + 1}:{(t % BEATS) / STEP:.2f}" for t in [x / 256 for x in range(wo_b0 * BEATS * 256, (wo_b0 + ROW) * BEATS * 256)] if math.floor(wow_turns(t)) != math.floor(wow_turns(t - 1 / 256))))
            if WOW_ORGAN:
                print("   the organ: " + " ; ".join(f"{int(n['at'] // BEATS) + 1}:{(n['at'] % BEATS) / STEP:g} {n['len']:g} beats " + "".join(m['pitch'] + " " for m in wow_notes() if m['at'] == n['at']).strip() for n in wow_notes()[::4]))
        if canon_span() is not None:
            ca_t0, ca_tc, ca_t1 = canon_span(); ca_sec = 60 / BPM
            print(f"two decks cross (a canon by acceleration), bars {int(ca_t0 // BEATS) + 1}-{int(ca_t1 // BEATS)} ({int(ca_t0 * ca_sec) // 60}:{ca_t0 * ca_sec % 60:04.1f} to {int(ca_t1 * ca_sec) // 60}:{ca_t1 * ca_sec % 60:04.1f}), crossing on bar {int(ca_tc // BEATS) + 1} beat {ca_tc % BEATS + 1:g} ({int(ca_tc * ca_sec) // 60}:{ca_tc * ca_sec % 60:04.1f}): the record's {CANON_PART}, {CANON_OCT:g} octave(s) each way ; {CANON_GAIN}, pan {-CANON_PAN:g} to {CANON_PAN:g}")
            for ca_up in (True, False):
                ca_n = canon_notes(ca_up, {"tock": TOCK}[CANON_PART])
                print(f"   the deck that {'winds up' if ca_up else 'runs down'}: speed {canon_speed(ca_t0, ca_up):.2f} to {canon_speed(ca_t1, ca_up):.2f} ; the record's beats {canon_place(ca_t0, ca_up) - ca_tc:+.2f} to {canon_place(ca_t1, ca_up) - ca_tc:+.2f} from the crossing ; {len(ca_n)} strokes ; by bar: " + " | ".join(" ".join(f"{(x['at'] % BEATS) / STEP:.2f}" for x in ca_n if int(x['at'] // BEATS) == b) for b in range(int(ca_t0 // BEATS), int(ca_t1 // BEATS))))
            ca_u, ca_d = canon_notes(True, {"tock": TOCK}[CANON_PART]), canon_notes(False, {"tock": TOCK}[CANON_PART])
            print("   apart (ms) at the strokes nearest the crossing: " + " ".join(f"{(x['at'] - ca_tc) / STEP:+.2f}:{min(abs(x['at'] - y['at']) for y in ca_d) * ca_sec * 1000:.0f}" for x in ca_u if abs(x['at'] - ca_tc) <= 2.5))
        if QUART and quart_chimes():
            qu = quart_chimes()
            print(f"the clock chimes the quarters ({QUART_GAIN}): {len(qu)} chimes, {sum(len(c[3]) for c in qu)} notes on {' '.join(QUART_BELLS[d] for d in (3, 2, 1, 5))}, {QUART_APART:g} s apart ({QUART_APART * BPM / 60:.4f} beats), a change every {QUART_CHANGE:g} s")
            for qu_t, qu_m, qu_q, qu_ns in qu:
                qu_b = qu_t * BPM / 60
                print(f"   {qu_m}:{qu_q * QUART_EVERY:02d} (bar {int(qu_b // BEATS) + 1} beat {qu_b % BEATS + 1:.2f}, {section_at(qu_b)[0]}): {len(qu_ns) // 4} change(s): " + " | ".join(" ".join(b for _, b, _ in qu_ns[i:i + 4]) for i in range(0, len(qu_ns), 4)) + f" ; to {qu_ns[-1][0] - qu_t:g} s after ; trim {QUART_TRIM.get((qu_m, qu_q), 0.0):+g} dB")
        if SCAR and scar_notes():
            sc = scar_notes(); sc_ms = 60000 / BPM
            print(f"a scratch across deck B's record: a tick every {SCAR_TURN} sixteenths of the record (from its sixteenth {scar_phase() + SCAR_OFF:g}: {SCAR_OFF:g} of a sixteenth after the first beat of {SCAR_ON}) ; {len(sc)} ticks, bars {int(sc[0]['at'] // BEATS) + 1}-{int(sc[-1]['at'] // BEATS) + 1} ; {SCAR_GAIN}, pan {SCAR_PAN}")
            for sc_name, sc_b0, sc_n, sc_parts, sc_hand in SECS:
                sc_in = [q for q in sc if sc_b0 * BEATS <= q["at"] < (sc_b0 + sc_n) * BEATS]
                if sc_in:
                    sc_gaps = [(b["at"] - a["at"]) / STEP for a, b in zip(sc_in, sc_in[1:])]
                    print(f"   {sc_name:12s} {len(sc_in):3d} ticks ; from one to the next, sixteenths of the grid: {min(sc_gaps):.2f} to {max(sc_gaps):.2f}" + f" ; the first five at bar.sixteenth " + " ".join(f"{int(q['at'] // BEATS) + 1}.{(q['at'] % BEATS) / STEP:.2f}" for q in sc_in[:5]))
            sc_last = sc[-6:]
            print("   its last six (seconds ; ms since the one before): " + " ; ".join(f"{q['at'] * sc_ms / 1000:.2f} s" + (f" +{(q['at'] - p['at']) * sc_ms:.0f}" if p else "") for p, q in zip([None] + sc_last[:-1], sc_last)))
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
        if CHIME and chime_strikes():
            def ch_where(sec):
                ch_b = sec * BPM / 60; ch_f = int(ch_b + 1e-9)
                return f"{sec // 60}:{sec % 60:02d} bar {ch_f // BEATS + 1} beat {ch_f % BEATS + 1} +{(ch_b - ch_f) * 60000 / BPM:.0f} ms"
            print(f"   the clock strikes the minutes ({CHIME_GAIN}, on {CHIME_NOTE}, partials " + " ".join(f"{chime_hz() * r:.0f}" for r, _ in CHIME_PARTS) + f" Hz, ringing {CHIME_RING}): a minute is {60 * BPM // 60} beats, {60 * BPM / 60 / BEATS:g} bars ; a second is {BPM / 60:.4f} beats, so each stroke is {1000 * (BPM / 60 - int(BPM / 60)) * 60 / BPM:.1f} ms further behind the beat than the last")
            for ch_k, ch_secs in chime_strikes():
                print(f"      {ch_k} stroke(s) ({CHIME_TRIM.get(ch_k, 0.0):+g} dB): " + " ; ".join(ch_where(x) for x in ch_secs))
        if PIPS and pips_seconds():
            print(f"   the pips ({PIPS_GAIN}, {PIPS_HZ:g} Hz, {PIPS_SHORT * 1000:g} ms and the last {PIPS_LONG * 1000:g} ms): on the {PIPS_BEFORE} seconds before each minute and on it ; a second is {BPM / 60:.4f} beats")
            for pp_k, pp in pips_seconds():
                pp_out = []
                for pp_i, (pp_sec, pp_ln) in enumerate(pp):
                    pp_b = pp_sec * BPM / 60; pp_n = round(pp_b)
                    pp_out.append(f"{pp_sec // 60}:{pp_sec % 60:02d} bar {pp_n // BEATS + 1} beat {pp_n % BEATS + 1} {(pp_b - pp_n) * 60000 / BPM:+.0f} ms ({pips_trim(pp_k, pp_i, pp_sec):+g} dB)")
                print(f"      the minute {pp_k}: " + " ; ".join(pp_out))
        if CLOCK_END:
            ce_secs = clock_end_seconds(); ce_first = clock_seconds()[0]; ce_bar = BEATS * 60 / BPM; ce_t0 = (BARS - CLOCK_END_BARS) * ce_bar
            print(f"   the clock was running all along: in the last {CLOCK_END_BARS} bars ({BARS - CLOCK_END_BARS + 1}-{BARS}, from {ce_t0:.2f} s) it ticks at the whole seconds {ce_secs[0]} to {ce_secs[-1]} ({len(ce_secs)} of them, {CLOCK_END_GAIN}): " + " ".join(f"{x}:{'tick' if round((x - ce_first) / CLOCK_EVERY) % 2 == 0 else 'tock'}" for x in ce_secs) + " ; beats from the first of those bars: " + " ".join(f"{(x - ce_t0) * BPM / 60:.3f}" for x in ce_secs) + f" ; the last one {BARS * ce_bar - ce_secs[-1]:.2f} s before the song ends")
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
