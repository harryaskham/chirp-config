#!/usr/bin/env python3
"""Escapement (Chirpers 11), track 7 (chirper-zero): OUT OF STEP. The slot's word is PHASE.

ONE PATTERN AGAINST ITSELF. Two clicks, the same sound, play the same half-bar pattern (PATTERN: x x . x . x x .).
A is on the grid and never moves. B is the same loop a hair shorter: its phase, phi, is how many sixteenths it is
ahead of A, and every B stroke sounds when t + phi(t) reaches it. Nothing else is written for B.

THE ESCAPEMENT. In "slips" the phase goes up by one sixteenth a row: for the first SLIDE bars of each row B creeps
ahead, slowly at first and then faster (phi = k + u^2), and CATCHES on the next sixteenth, where it stays locked for
the rest of the row: a tooth of the wheel. Each lock is a different pattern made of the same two (the eight
rotations), and after eight rows B is a whole half-bar ahead, which is where it started: "home".

THREE KINDS OF PHASE, ONE ARITHMETIC. (1) The rhythm: the locks. (2) The sound: as B leaves a lock, strokes that
were together are a millisecond apart, then two, then five, and two copies of one click that close cancel at the
frequencies whose half-wave is the gap: a comb that sweeps down as the gap opens. There is no phaser on the record;
this is one. (3) The bass: pairs of sines, each pair DELTA Hz apart (G2 and G2 + DELTA, and the same on its harmonics), where
DELTA is one cycle a beat. Struck on the off-beat they agree there and cancel on every beat, exactly where the bass drum is: the pump of
a side-chain, with no compressor and no envelope, only two tones out of step.

THE LONG ARC. Both clicks pass one low-pass whose opening IS the phase: dull at 4 kHz while they are together,
a step brighter at every catch, wide open at home; and it closes again as B drifts back.

In "drifts" B lets go: its phase runs back from eight to nothing at one steady speed (a sixteenth every four
bars, Piano Phase's way), through every lock without stopping, and is one click again at the end.

THE FORM IS ARITHMETIC: a row is ROW bars; SECTIONS lists each section's rows, its parts (a part may be given the
bars of the section it plays) and what the phase does. Every note comes from those.

v1 is the SKELETON (26 Nov): the process, stated whole, with few sounds.

v2 (26 Nov): THE MOULD (C11T7_COMP=0 takes it out: v1). The pattern has three holes in its eight sixteenths
(2, 4 and 7). From "home" a third click, C, small and bright and on the grid, plays the holes and nothing else:
the pattern's complement. When A and B are together the two patterns interlock and every sixteenth of the bar
sounds exactly once: that is what home is, and it is why the wheel was turned eight times to get back. In "drifts",
as B lets go, its strokes fall into the holes C is filling: B and C strike together where they never could at home
(on one, two or all three of C's strokes, by how far ahead B is: all three at four ahead), and the bar goes lumpy;
when B is home again it is smooth again. Home is the only phase at which B and C never meet.

v3 (26 Nov): THE TUNE THE TWO MAKE (C11T7_TUNE=0 takes it out: v2). Wherever A and B strike on the same sixteenth
the two clicks are one louder click, and those doubles are a different figure at every lock: two of them at one
ahead, three at two, four at three ... A small glass pip now plays exactly the doubles, and each stroke of the
pattern has a note: G, B flat, D, F, A (the record's chord: Give or Take's G minor seventh with Least Common's ninth
on top). So every lock has its own tune, found in the two clicks and not written: G . . . . F . . at one ahead,
. Bb . D . . A . at two, G . . D . F A . at three ..., always a piece of the chord. AT HOME EVERY STROKE IS A
DOUBLE AND THE TUNE IS THE WHOLE CHORD: that is the second thing home is. In "slips" the first four locks are
heard bare, as before; from the fifth (where the drum stands back) each lock is heard bare for two bars and then
with its tune. In "drifts" B does not stop, so each tune is heard only for the two bars in which B passes its lock,
all seven backwards (7, 6, 5 ... 1: four of them for the first time), between bars where there is no tune at all.

v4 (26 Nov): THE PENDULUM (C11T7_PEND=0 takes it out: v3). A fourth kind of phase, and the smallest: under a
millisecond. While the two clicks are one click (the opening and the ending) A is given to the left ear alone and B
to the right, at the same loudness, and B swings ahead of A and behind it by PEND_MS (0.6 ms: the time sound takes
to cross a head), once there and back every two bars. A lead that small is not heard as two clicks, nor as a
rhythm: it is heard as a PLACE. The one click swings from ear to ear like the pendulum of the clock this record is
named after, and nothing is panned: each ear gets its own click at the same level all the way; only which is first
changes. (The two are turned down 3 dB while they stand apart, so that B joining adds no loudness, only a place.) THE DRUM HOLDS THE PENDULUM: it swings only where there is no bass drum. In "one click" it starts still
when B joins (bar 9), is at its full width a swing later, and stops dead on the bar the drum comes in. In "one
again" the drum's last stroke lets it go: it swings its full width at once and comes to rest, half as far every
three bars, and when it is still B stops. On ONE speaker there are no two ears to compare: the same lead is a comb, a hollow that opens
and closes in the click twice a swing (the phaser of the slips, a hundred times slower).

v5 (26 Nov): THE BASS HEARS THE LOCK (C11T7_ROOT=0 takes it out: v4). The bass has held one note, G, for the whole
record. But every lock has a first stroke that the two clicks share (the first note of its tune), and it is one of
two: the pattern's first stroke, G, or its second, B flat. In "drifts", where B does not stop and nothing says
where the locks are, the bass now does: as B passes each lock the bass plays the note the two are agreed on first.
After sixty-six bars on G it moves: B flat for four bars as B passes the seventh lock, G for eight (the sixth and
the fifth), B flat for four (the fourth), G for four (the third), B flat for four (the second), and G from there
home. Nobody wrote the line: G and B flat fall where the pattern's rotations put them, and the bass drum is away
for two of the changes (bars 121 to 128). Under B flat the tune's notes are a B flat major seventh (B flat, D, F, A); under G
they are G minor with its ninth: two chords out of one pattern. The B flat is a second bass, tuned like the first:
pairs of sines one cycle a beat apart from ITS notes, so it pumps on the beat as the G does.
ROOT_IN says in which kinds of phase the bass follows. It was tried in "slips" as well (the bass changing on the
bar B catches): on its own that scored a little under this, and both together made thirteen sections that kept
coming back and cost two points, so "slips" keeps its one note and the bass's first move is an event.

v6 (26 Nov): THE TUNE OUT OF STEP WITH ITSELF (C11T7_CANON=0 takes it out: v5). At home the tune is the whole
chord, G B flat . D . F A ., twice a bar, and it has stood still. In home's second row the tune is given a B of
its own: a second pip, an octave lower, playing the same five notes, which does to the tune what B did to the
click. It sets off with the tune, as one, and slips ahead: for half a bar it creeps (slowly, then faster), and
CATCHES a sixteenth ahead, and holds; two bars on it slips again. Four locks in eight bars, and each is a
different piece of music made of the same five notes twice: at one ahead every sixteenth of the bar sounds and
the two run up the chord and back in each other's gaps (G+Bb, Bb, D, D, F, F+A, A, G); at two ahead they meet on
three sixteenths, in thirds by name (Bb+D, D+F) and A over G; at three they meet on four, two fifths (G+D, D+A)
and two seconds (F+G, A+Bb); at four, half a loop, each plays in the other's half and they meet on B flat and F. Where the click's phase made rhythms, the tune's makes harmony, and every note of
it is in the record's chord, so nothing it finds is wrong. (This is Piano Phase's own way: the click's phase is
Clapping Music's.) Then B lets go, "drifts" begins, and the second pip stops.

v7 (26 Nov): THE LOCKS HAVE A SHAPE (C11T7_SHAPE=0 takes it out: v6). For the first four rows of "slips", where
the locks are heard bare, A IS GIVEN THE LEFT EAR AND B THE RIGHT (each keeps a seventh of itself in the other:
SHAPE_APART 0.85). Nothing is moved while the two are together: two copies of one click, one in each ear at
the same instant, ARE one click in the middle, and the levels are set so that the two ears added are exactly
what they were (a click moved to the side is turned up by what its far ear no longer gives: 3.14 dB). So each
lock is now a PICTURE: the strokes the two share stand in the middle, A's own strokes are on the left, B's own
on the right. One ahead: two in the middle and three a side. Two ahead: three and two. Three ahead: four in
the middle and one a side. Four ahead: two and three again, other strokes.
AND EVERY SLIP SHOWS WHAT PHASE IS, FROM THE SMALLEST UP: as B leaves a lock its copy of a shared stroke
reaches the right ear a fraction of a millisecond before A's reaches the left, and the click in the middle
LEANS to the right; at a millisecond it is on the right; by five it is a wide click with an edge; by thirty it
is two clicks; by a sixteenth it is the next lock: a place, a side, a width, a flam, a rhythm, in two bars, and
it is one number growing. (v4's pendulum is the first of those five, held still.)
THEN THE TUNE NAMES WHAT THE PICTURE SHOWED: from the fifth row the two clicks stand where they always stood
and the pip, in the middle, plays the strokes they share: the ones that were in the middle.
ON ONE SPEAKER the two ears are added and the two clicks' sum is what it was.
The two clicks are on tracks of their own for those bars (`a-ear`, `b-ear`); their room sends are as they were
(a send is taken AFTER the track's gain and pan: the turn-up and the pan cancel in it. Corrected 26 Nov: I had written before).
BENCHED AND REFUSED: the picture all the way from the first slip to the end of the drift, an ear each: 94.88 /
94.94; the same at 0.85 with the room as it was: 94.38 / 94.34 (v6 that day 95.05 / 94.98). In both the scorer's
cut at 1:48 (0.182 in v6, 0.002 over its top threshold) slid to 0.167 and the form lost a section on two of
seven cuts; nothing else fell. C11T7_SHAPE_ROWS=8 is the whole of slips.

v8 (26 Nov): HALF A WAVE OUT OF STEP (C11T7_WAVE=0 takes it out: v7). The song is two clicks out of step by
sixteenths, and what changes is the RHYTHM. The click itself is five turns of a wave (a saw on G3: 5.1 ms a
turn). Put B ahead of A by HALF A TURN (2.55 ms) and what changes is the NOTE: every odd harmonic of the one
meets itself upside down in the other and is gone, the even ones are doubled, and what is left is a click on
the G an octave above. Put B a WHOLE turn ahead (5.1 ms) and the two waves are in step again though the clicks
are not: the low G is back, a turn longer. It is the song in small: out of step by half the pattern, the
rhythm turns inside out; by all of it, home. For the last eight bars of "one click" (17 to 24: after the
pendulum, with the bass drum, before the first slip) the two clicks stand in ONE place (the middle: a click
and its copy must reach the same ear to cancel) and B goes ahead by WAVE_STEPS half turns: four bars with A
(as they were), two bars HALF A TURN ahead (bars 21 and 22: the octave), two bars A WHOLE TURN ahead (23 and
24: the low G again), and then the first slip begins. Nothing is played but the same click twice. It is heard
on one speaker: it is the one-speaker half of the pendulum (a lead too small to be a rhythm is a PLACE to
two ears, and a COLOUR or a NOTE to one). The step is made in the pattern's last sixteenth, which is a hole.
The clicks are on their own tracks for those bars (`a-mid`, `b-mid`), turned down 1.67 dB so that on one
speaker they are as loud as they were at their usual places.
BENCHED (seed 0; v7 that day 95.15): the half turn and the whole turn a bar each, alternating, from bar 18
(0,1,2,1,0,1,2,1) scored 94.81 / 94.78: the scorer's cut at the bass drum's entry (31 s) fell from 0.152 to
0.125 and took 1.8 points of variety. The octave for four bars from the drum's entry, then the whole turn for
four (1,1,1,1,2,2,2,2): 95.10. As published (0,0,0,0,1,1,2,2): 95.13: the drum's entry is as it was.

v9 (26 Nov): THE WAVE'S OWN SCALE (C11T7_SCALE=0 takes it out: v8). v8 found that B half a turn of the click's
wave ahead of A is the click an octave up. That is the first step of a ladder. Strike the SAME click n times,
each a n-th of a turn (5.102 ms / n) after the last, and every harmonic that is not a multiple of n meets n - 1
copies of itself spread evenly round the circle and is cancelled; the multiples of n all arrive in step. What is
left is the click on n times its note, AND NO BIGGER (n copies of a saw a n-th of a turn apart ARE a saw n times
as high, of the same height). So one click, with no other sound, no filter and no change of pitch, has a
scale: its wave's own harmonics. 1 G3, 2 G4, 3 D5, 4 G5, 6 D6, 7 F6 (the natural seventh, 31 cents under the
piano's), 8 G6, 9 A6. (5 is a B natural and is left out: the song's tune has B flat.) Every one of the eight
is a note-name of the song's own tune (G, D, F, A); the wave has no B flat to give.
It is played in the second row of "one again" (bars 145 to 152, 4:34 to 4:49), where the drum has gone: a click
on every beat, up the ladder in two bars and down it in two, twice, and the last of them is one click again.
Its own tracks (`wave-1` ... `wave-9`: the k-th copy of each stroke), in the middle, on the song's click patch
and through the same low-pass and room: the only thing that differs from A's click is WHEN.
(Not perfect, and measured: the click dies as it rings (22 ms), so a later copy is a little smaller than the one
it should cancel, and the engine starts a note on a whole sample, 21 millionths of a second: what should cancel
is 12 to 16 dB under what should not. And "no bigger" is the peak, which falls 3 dB from the bottom of the
ladder to the top; the LEVEL rises 6 dB on the way up, because the click's own 500 Hz high-pass takes most of a
single click's two lowest harmonics away and takes nothing from the higher rungs.)

v10 (26 Nov): A NOTE IS A CLICK IN STEP WITH ITS OWN WAVE (C11T7_ROLL=0 takes it out: v9). The record's click is
five turns of a wave (a saw on G3, 5.102 ms a turn). Strike it again before it has died and the second stroke
falls on the first one's tail: in step with it or out, by how far apart they are. A ROLL does that: the click
on its own track, from sixteenths (8.4 strokes a second), faster by the same ratio every beat (1.69 times: the
rate is a straight line on a slide rule), for six beats, until the strokes are ONE TURN OF THE WAVE apart: 196 a
second. There every stroke is in step with the tail of the one before, the tails add, and the row of clicks is
one unbroken note: G3, the saw the click was cut from. It is held for two beats and stops on the bar line.
On the way up the rate is heard first as a rhythm, then as a buzz, then as a pitch that climbs four and a half
octaves; and the strokes go in and out of step with their own tails: in step (bright) when they are a whole
number of turns apart (49 a second: G1; 65: C2; 98: G2), out (hollow) half way between.
Once: in the two bars of "slips" where the drum, the clap and the hat rest (bars 81 and 82, 2:32 to 2:36),
landing on their return. Stockhausen's splice (a note slowed until it is a row of pulses, Kontakte, 1960) the
other way up, made out of the record's own click.
(Made also, and REFUSED: the same roll backwards (a note coming apart into the clicks it is made of) in the
first two bars of the row of "drifts" that has no drum, and up again in that row's last two. With those two
the score fell 0.6: the scorer's sections of "drifts" came out more alike (timbre spread 5.9 to 5.4). They are
still written: C11T7_ROLL_AT="slips/56/up,drifts/16/down,drifts/22/up".)
Each stroke is turned down as the roll quickens, by the square root of the rate, so the roll gives the same
power a second at every speed: what changes is only how the strokes are spaced. Track `roll`, patch `os-click`,
in the middle.
(Made first with the held note as high in peak as one stroke: in the master a held note that high is as loud
as the music, the master turned the music 3 to 5 dB down under it, and the score fell 0.6. Refused.)

v11 (26 Nov): THREE AGAINST TWO, FROM FOUR SINES (C11T7_HEMI=0 takes it out: v10). The bass is two tones a cycle
a beat apart, so it swells once a beat: a pump made of nothing but two tones out of step. Now it has a second
pair under it, on D2 (a fourth below the G), and these two are A CYCLE AND A HALF a beat apart (3.15 Hz): this
pair swells three times in two beats. Both pairs are struck on the off-beat, where each agrees with itself, so
the two pumps agree with each other there once every two beats and nowhere else: the G swells on the "and" of
every beat, the D on the "and" of one and then two thirds of a beat on and two thirds again. Three against two,
and nothing is struck to make it: four sines (eight with their octaves) that never change.
It comes in where the drum rests in "drifts" (bars 121 to 128: nothing else is down there) and stays, the drum
back under it, for as long as the bass does (to bar 152), 6 dB under the bass. The D pair is as sharp as the G pair is (a pair's note is the
mean of its two tones), so the fourth between them is true.
WHY D, AND WHY SO LOW: `compscore --bands` says this song has 9.7 dB less than the rest of the record at 61 and
71 Hz and 7 dB less at 156 Hz. D2 is 73 Hz and its octave 147 Hz.

v12 (26 Nov): TWO CLICKS LESS THAN A WAVE APART (C11T7_COMB=0 takes it out: v11). The song is two clicks going out
of step by sixteenths. This is the same thing a thousand times smaller. A new, small, bright click (all of it over
6.5 kHz) plays on the odd sixteenths wherever the hat plays (bars 57 to 144, less two), and it is TWO clicks, the
same to the sample, in the same place. It follows the song's own form at its own scale. In "slips" and in "drifts",
where click B goes out of step with click A by sixteenths, the second small click falls behind the first by
1, 2, 3 ... up to 12 SAMPLES (a quarter of a millisecond) and comes back, every four bars. In "home", where A and B
lock, the two small clicks are in step to the sample for all sixteen bars: one click, at its brightest. And in
"one again" they are one again. Nobody can hear two clicks a quarter of a millisecond apart as two, or as late. They are heard
as a COLOUR: two copies n samples apart cancel wherever n samples is half a wave (and a wave and a half, and two
and a half): at 24000 / n Hz times 1, 3, 5 ... So the notches walk down the undertones of 24 kHz as the clicks
part (12 kHz, 8, 6, 4.8, 4 ...) and back up as they close: the sweep of a flanger, with no effect on anything:
two notes and a subtraction.
It is also the song's air: `compscore --bands` said first that this song has 14 dB less than the rest of the
record at 15 kHz and 8 dB less at 12.6 kHz, and every part read alone has next to nothing there.

v13 (26 Nov): THE CLICK, HELD, THROUGH A PHASER (C11T7_JET=0 takes it out: v12). In the eight bars of
"drifts" in which the bass drum stands back (121-128) the click's own NOTE is held: a saw on G3 with the
click's own high-pass, which is what the roll (v10) arrives at, a click struck 196 times a second. It goes
through a PHASER, the effect the slot's word is the name of: eight all-pass stages turn the phase of every
harmonic by a different amount, and added back to the note they weaken some harmonics and strengthen others;
which ones sweeps there and back every two bars, four times. It stops on the bar line where the drum comes
back. A held sound under the clicks also does something the scorer reads: the clicks no longer rise out of
nothing, so the break reads as the bare place it is (its onsets a second 8.4 to 5.1).
NOT IN v13, kept here behind a switch (C11T7_LAP=1): ONE MORE TO THE BAR. A wooden click plays seventeen even
strokes to the bar against the song's sixteen in bars 113-114, then eighteen, nineteen and twenty (two bars
each): it laps the song once a bar, then twice, three and four times, which is once a beat, the rate at which
the bass's two tones swell. Two rates that differ by n to the bar beat n times a bar. It renders as written
(the strokes 112.04, 105.81, 100.25, 95.23 ms apart), but it made those eight bars unlike the bars they return
to (the scorer's recurrence 100 to 95.8, on C4 and on D4 alike), and the scorer cannot see its strokes among
sixteen to the bar. A build for another round, on a part the song already has.

v14 (27 Nov): TWO, THREE, FIVE (C11T7_FIVE=0 takes it out: v13). The bass is two tones a cycle a beat apart: it
swells twice in two beats. Under it, since v11, is a pair that swells three times in two beats. Now there is a
third pair OVER it, on C4 (a fourth over the click's own G3), and these two are TWO AND A HALF cycles a beat apart
(5.25 Hz): five swells in two beats. All three pairs are struck on the same off-beat, where each agrees with
itself, so all three agree there, and again two beats on, and nowhere between: two against three against five,
and nothing is struck to make any of it: six plain tones (and their octaves) that never change, out of step with
each other by three different amounts. The pair is as sharp as the bass's own (a pair's note is the mean of its
two tones), so the fourth is true. It sounds wherever the bass does (bars 41 to 152), 14 dB under the music.
In the twelve bars where the bass hears a lock and goes to B flat it is a ninth over the bass.
WHY C4, said plainly: `compscore --bands` says this song has 10.6 dB less than the rest of the record round
250 Hz. The bass's harmonics are at 196 and 294 Hz and the clicks begin at 500: between G3 and D4 the song has
nothing. C4 is 262 Hz.

v15 (27 Nov): THE VERNIER (C11T7_VERN=0 takes it out: v14). A vernier is a second ruler with one mark more
(or less) in the same length: its marks agree with the first ruler's at one place only, and that place tells a
shift far smaller than a mark. Here the first ruler is the bar's sixteen sixteenths and the second is SEVENTEEN
small high ticks in the same bar. Tick k falls k/272 of a bar (k times 7.0 ms) before sixteenth k: with it at
the bar line, a hair early, then a flam, then plainly between two sixteenths, and by the bar's end a whole
sixteenth early, which is with the next one. That is this song's slip (B gains a sixteenth on A in two bars),
done once in every bar, sixteen times in the time B takes to do it once.
It plays through B's first three slips (bars 25-48), where there are only the two clicks, the drum and later
the bass, and stops a row before the hat and the two clicks less than a wave apart come in at bar 57: the top
of the song was empty until then (nothing over 10 kHz for 1:47), and the hat still arrives on a bare top.
"""
import json
import math
import os

OUT = os.environ.get("C11T7_OUT", os.path.join(os.path.dirname(__file__), "..", "..", "..", "songs", "chirpers11-t7.yaml"))
BPM = 126
BEATS = 4
ROW = 8
STEP = 0.25
BAR = 16                       # sixteenths

PATTERN = (0, 1, 3, 5, 6)      # of eight sixteenths: x x . x . x x .
LOOP = 8
SLIDE = 2                      # bars B takes to slip from one lock to the next
NOTE = "G3"
F0 = 97.9989                   # G2
DULL = 4000                    # Hz: the clicks' low-pass when B is with A
OCTAVES = 1.7                  # ... and how far it opens when B is a whole loop ahead
DELTA = BPM / 60               # Hz: one cycle a beat

COMP_ON = os.environ.get("C11T7_COMP", "1") != "0"    # v2: the complement, C
COMP = tuple(s for s in range(LOOP) if s not in PATTERN)   # the holes: 2, 4, 7
C = {"c": None} if COMP_ON else {}
TUNE_ON = os.environ.get("C11T7_TUNE", "1") != "0"    # v3: the tune the two make
TUNE = {0: "G4", 1: "Bb4", 3: "D5", 5: "F5", 6: "A5"}  # a note for each stroke of the pattern: G minor ninth
assert set(TUNE) == set(PATTERN)
TUNE_FROM = 4                  # in "slips": the row from which a lock has its tune (the first four locks are heard bare)
TUNE_AFTER = 4                 # ... and the bar of the row from which it is heard (2 slipping, 2 bare)
TUNE_NEAR = 0.26               # sixteenths: a bar plays a lock's tune if B is this near the lock from its first step to its last
T = {"tune": None} if TUNE_ON else {}
ROOT_ON = os.environ.get("C11T7_ROOT", "1") != "0" and TUNE_ON   # v5: the bass hears the lock
F0B = 116.5409                 # B flat 2
ROOT_IN = tuple(os.environ.get("C11T7_ROOT_IN", "drift").split(","))   # the kinds of phase in which the bass follows the lock ("slips", "drift"); elsewhere it is G
CANON_ON = os.environ.get("C11T7_CANON", "1") != "0" and ROOT_ON   # v6: the tune out of step with itself
CANON_FROM = 8                 # the bar of "home" on which the tune's own B sets off (it stops when "home" does)
CANON_HOLD = 2                 # bars to each lock: it is a sixteenth further ahead every one of these
CANON_SLIDE = 0.5              # ... of which it is slipping for this many (u^2, as B slips), and caught for the rest
CANON_OCT = -1                 # octaves it plays from the tune, so that the two are told apart
CANON_GAIN = os.environ.get("C11T7_CANON_GAIN", "-17dB")
PEND_ON = os.environ.get("C11T7_PEND", "1") != "0"    # v4: the pendulum
SHAPE_ON = os.environ.get("C11T7_SHAPE", "1") != "0" and CANON_ON and PEND_ON   # v7: the locks have a shape
SHAPE_ROWS = int(os.environ.get("C11T7_SHAPE_ROWS", "4"))   # the rows of "slips", from its first, through which A has the left ear and B the right (the locks heard bare)
SHAPE_APART = float(os.environ.get("C11T7_SHAPE_APART", "0.85"))   # how far apart they stand there (1: an ear each)
WAVE_ON = os.environ.get("C11T7_WAVE", "1") != "0" and SHAPE_ON                 # v8: half a wave out of step
WAVE_BARS = (16, 24)           # the bars of "one click" in which B is ahead by half turns of the click's own wave ...
WAVE_STEPS = tuple(int(x) for x in os.environ.get("C11T7_WAVE_STEPS", "0,0,0,0,1,1,2,2").split(","))   # ... and by how many, a bar each
WAVE_PAN = float(os.environ.get("C11T7_WAVE_PAN", "0"))   # where A and B stand meanwhile (-WAVE_PAN and +WAVE_PAN): in one place, so that the one can cancel the other in both ears
WAVE_HZ = 440 * 2 ** ((55 - 69) / 12)                  # the click's note (NOTE, G3): 196.0 Hz, 5.102 ms a turn
SCALE_ON = os.environ.get("C11T7_SCALE", "1") != "0" and WAVE_ON                 # v9: the wave's own scale
SCALE_IN = ("one again", 8, 16)                        # the section, and the bars of it in which one click plays its wave's own notes
SCALE_STEPS = (1, 2, 3, 4, 6, 7, 8, 9)                 # n: the click struck n times, a n-th of a turn apart, is the click on n times its note: G3 G4 D5 G5 D6 F6 G6 A6 (5 is a B natural: the tune has B flat)
SCALE_EVERY = 4                                        # sixteenths from one stroke to the next: on every beat, up the steps and down them
SCALE_GAIN = float(os.environ.get("C11T7_SCALE_GAIN", "-6"))   # dB: every copy (A's own fader is -2: at that the top of the ladder stood 9 dB over the click A and B make together; at -6 the bottom is 1 dB under it and the top 5 over)
SCALE_VEL = 0.9
PEND_MS = 0.6                  # ms: how far B is ahead of A (and then behind) at the end of a swing; sound crosses a head in about this
PEND_BARS = 2                  # bars to swing there and back
PEND_GROW = 2                  # bars it takes to reach its full swing when it is set going ("up")
PEND_HALF = 3                  # bars in which the swing halves when it is left to come to rest ("rest")
PEND_APART = 1.0               # where the two clicks stand while it swings: A at -PEND_APART, B at +PEND_APART (an ear each)
PAN = 0.35                     # ... and everywhere else
PEND_GAIN = -3                 # dB: what both clicks are given while they stand apart: two clicks, an ear each, are then as loud as the one click was
P = (lambda lo, hi, kind: ("pend", lo, hi, kind)) if PEND_ON else (lambda lo, hi, kind: ("lock", 0))
ALL = None
# name, rows, {part: None, or the (from bar, to bar) stretches of the section it plays}, the phase: ("lock", k) | ("slips", k0) | ("drift", from, to) | ("pend", from bar, to bar, "up" or "rest"): locked at 0, swinging
SECTIONS = [
    ("one click", 3, {"a": ALL, "b": [(8, 24)], "kick": [(16, 24)]},                                                          P(8, 16, "up")),
    # the bass drum stands back while B slips to its last lock (8, which is home), and for the whole of the fifth row,
    # where the bass is heard pumping with no drum to pump it
    ("slips",     8, {"a": ALL, "b": ALL, "kick": [(0, 32), (40, 56), (58, 64)], "bass": [(16, 64)], "clap": [(40, 56), (58, 64)], "hat": [(32, 56), (58, 64)], **({"tune": [(r * ROW + TUNE_AFTER, (r + 1) * ROW) for r in range(TUNE_FROM, 8)]} if TUNE_ON else {})}, ("slips", 0)),
    ("home",      2, {"a": ALL, "b": ALL, "kick": ALL, "bass": ALL, "clap": ALL, "hat": ALL, **C, **T, **({"tune2": [(CANON_FROM, 2 * ROW)]} if CANON_ON else {})},   ("lock", 8)),
    ("drifts",    4, {"a": ALL, "b": ALL, "kick": [(0, 16), (24, 32)], "bass": ALL, "clap": [(0, 16), (24, 32)], "hat": ALL, **C, **T},  ("drift", 8, 0)),
    ("one again", 3, {"a": ALL, "b": [(0, 20)], "kick": [(0, 8)], "bass": [(0, 16)], "clap": [(0, 8)], "hat": [(0, 8)], **({"c": [(0, 16)]} if COMP_ON else {}), **({"tune": [(0, 16)]} if TUNE_ON else {})}, P(8, 20, "rest")),
]


def starts():
    out, b = [], 0
    for name, rows, parts, phase in SECTIONS:
        out.append((name, b, rows * ROW, parts, phase)); b += rows * ROW
    return out, b


SECS, BARS = starts()
TOTAL = BARS * BEATS


def plays(part, bar):
    for name, b0, n, parts, phase in SECS:
        if b0 <= bar < b0 + n:
            if part not in parts:
                return False
            w = parts[part]
            return w is None or any(lo <= bar - b0 < hi for lo, hi in w)
    return False


def swing(x, kind):
    """The pendulum, x bars after it starts: B's lead as a share of PEND_MS (+ ahead: the right ear first)."""
    if kind == "up":       # set going from rest: wider for PEND_GROW bars, then steady
        return min(1.0, x / PEND_GROW) * math.sin(2 * math.pi * x / PEND_BARS)
    return -0.5 ** (x / PEND_HALF) * math.sin(2 * math.pi * x / PEND_BARS)   # "rest": B arrives going backwards, overshoots and dies away


def wave_span():
    """The beats between which the two clicks stand in one place and B is half turns of the click's wave ahead, or None."""
    sec = SECS[0] if WAVE_ON and SECS[0][4][0] == "pend" else None
    return ((sec[1] + WAVE_BARS[0]) * BEATS, (sec[1] + WAVE_BARS[1]) * BEATS) if sec else None


def wave_ms(t):
    """How many ms B is ahead of A at time t (sixteenths) because it is half turns ahead; the step is made a sixteenth before the bar line, in the pattern's hole."""
    sp = wave_span()
    if sp is None or not sp[0] <= (t + 1) * STEP < sp[1]:
        return 0.0
    return WAVE_STEPS[int(((t + 1) * STEP - sp[0]) // BEATS) % len(WAVE_STEPS)] * 500 / WAVE_HZ


def wave_gain():
    """dB a click is turned by when it is moved from PAN to WAVE_PAN, so that on one speaker it is as loud as it was."""
    return 20 * math.log10((2 - PAN) / (2 - WAVE_PAN))


def mid(notes, inside):
    """The notes of a click inside (or outside) the bars in which the two stand in one place."""
    sp = wave_span()
    return [n for n in notes if (sp is not None and sp[0] - 0.05 <= n["at"] < sp[1] - 0.05) == inside]


def lead_ms(t):
    """How many ms B is ahead of A at time t (sixteenths) because of the pendulum; 0 where there is none."""
    bar = t / BAR
    for name, b0, n, parts, phase in SECS:
        if b0 <= bar < b0 + n and phase[0] == "pend" and phase[1] <= bar - b0 < phase[2]:
            return PEND_MS * swing(bar - b0 - phase[1], phase[3])
    return wave_ms(t)


def phi(t, pend=True):
    """B's phase at time t (sixteenths from the start): how many sixteenths it is ahead of A."""
    bar = t / BAR
    for name, b0, n, parts, phase in SECS:
        if b0 <= bar < b0 + n or (name == SECS[-1][0] and bar >= b0):
            u = bar - b0
            if phase[0] == "pend":
                return lead_ms(t) / (60000 / BPM / 4) if pend else 0.0
            if phase[0] == "lock":
                return float(phase[1])
            if phase[0] == "slips":
                k, v = int(u // ROW), (u % ROW) / SLIDE
                return phase[1] + k + (v * v if v < 1 else 1.0)
            if phase[0] == "drift":
                return phase[1] + (phase[2] - phase[1]) * u / n
    return 0.0


def when(b):
    """The time (sixteenths) at which B, running ahead by phi, reaches its own sixteenth b: t + phi(t) = b."""
    lo, hi = b - 10.0, b + 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if mid + phi(mid) < b:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


ROLL_ON = os.environ.get("C11T7_ROLL", "1") != "0" and SCALE_ON                 # v10: a note is a click in step with its own wave (the roll)
ROLL_AT = tuple((x.split("/")[0], int(x.split("/")[1]), x.split("/")[2]) for x in os.environ.get("C11T7_ROLL_AT", "slips/56/up").split(",") if x)     # the section, the bar of it at which a roll begins, and which way it goes
ROLL_GLIDE = 6                                         # beats in which the rate goes from sixteenths to a stroke a turn of the click's wave
ROLL_HOLD = 2                                          # beats the note is then held (a roll is ROLL_GLIDE + ROLL_HOLD beats: two bars)
ROLL_FALL = float(os.environ.get("C11T7_ROLL_FALL", "0.5"))    # a stroke is turned down by (the rate / a sixteenth's) to this power: at a half the roll gives the same power a second at every speed
ROLL_VEL = 0.8
ROLL_GAIN = float(os.environ.get("C11T7_ROLL_GAIN", "-8"))     # dB: the roll's fader (A's is -2). REFUSED in the master: fall 0.25 at -6 dB (the held note no higher in peak than a stroke): the note was 2.5 dB under the music, the master turned the music 3 to 5 dB down under it and the score fell 0.6


HEMI_ON = os.environ.get("C11T7_HEMI", "1") != "0" and ROLL_ON                 # v11: three against two, from four sines (a second pump, out of step with the first)
HEMI_IN = tuple((x.split("/")[0], int(x.split("/")[1]), int(x.split("/")[2])) for x in os.environ.get("C11T7_HEMI_IN", "drifts/16/32,one again/0/16").split(",") if x)   # (section, from bar, to bar of it) in which the second pair sounds: from where the drum rests in "drifts" until the bass itself stops
HEMI_NOTE, HEMI_F0 = "D2", 73.4162                     # a fourth under the bass's G
HEMI_RATE = 1.5                                        # cycles a beat between the pair's two tones: it swells three times in two beats (the bass: once a beat)
HEMI_PARTS = ((1, -3.0), (2, -9.0))                    # (harmonic, dB) of each pair: both tones of a pair as loud as each other, so between swells there is nothing
HEMI_GAIN = os.environ.get("C11T7_HEMI_GAIN", "-29dB")  # 6 dB under the bass's fader. REFUSED in the master: the bass's own -23 dB for the 16 bars of "drifts" alone: it was as loud as everything else together where the drum rests, the whole song came down 0.2 dB, and a new cut at its end cost 0.5 (structure and variety), more than the 0.75 it gave (spectrum and cohesion)


COMB = os.environ.get("C11T7_COMB", "1") != "0" and HEMI_ON              # v12: two clicks less than a wave apart (a comb)
COMB_WITH = "hat"                                        # it plays in the bars the hat plays in: the hat has the off-beats, this the odd sixteenths
COMB_APART = ("slips", "drifts")                         # the sections in which the two go apart; in the others ("home", "one again") they are in step to the sample
COMB_STEPS = ((1, 0.55), (3, 0.9), (5, 0.55), (7, 0.9), (9, 0.55), (11, 0.9), (13, 0.55), (15, 0.9))   # (sixteenth, velocity): the odd sixteenths, the one before each beat the louder
COMB_STILL = 4                                           # bars at the start of each such section's playing in which the two are exactly in step
COMB_TURN = 4                                            # bars from in step, to COMB_MAX apart, to in step again
COMB_MAX = int(os.environ.get("C11T7_COMB_MAX", "12"))   # samples apart at the widest: 12 is a quarter of a millisecond
COMB_GAIN = os.environ.get("C11T7_COMB_GAIN", "-6dB")    # each click's fader
RATE = 48000                                             # samples a second: the engine's


def comb_span():
    """The bars in which the two small clicks play, or []."""
    return [bar for bar in range(BARS) if plays(COMB_WITH, bar)] if COMB else []


def comb_apart(x):
    """Samples by which the second click is behind the first at bar position x (bars from the start of the song)."""
    sec = next(q for q in SECS if q[1] <= int(x) < q[1] + q[2])
    if sec[0] not in COMB_APART:
        return 0
    u = x - min(b for b in comb_span() if sec[1] <= b < sec[1] + sec[2])       # bars since it began to play in this section
    return 0 if u < COMB_STILL else int(round(COMB_MAX * (1 - math.cos(2 * math.pi * (u - COMB_STILL) / COMB_TURN)) / 2))


def comb_strokes():
    """(beat, samples the second click is behind, velocity) of every stroke."""
    return [((bar * 16 + st) * STEP, comb_apart(bar + st / 16), v) for bar in comb_span() for st, v in COMB_STEPS]


def comb_notes(second):
    return [{"at": round(t + (n / RATE * BPM / 60 if second else 0.0), 7), "len": 0.03, "pitch": "G5", "vel": v} for t, n, v in comb_strokes()]


LAP = os.environ.get("C11T7_LAP", "0") != "0" and COMB                # NOT IN v13 (off unless C11T7_LAP=1): one more to the bar (two rates)
LAP_PLAN = ((112, 2, 17), (114, 2, 18), (116, 2, 19), (118, 2, 20))   # (first bar, bars, strokes to the bar): the grid has 16, so it laps the song 1, 2, 3, 4 times a bar
LAP_NOTE = os.environ.get("C11T7_LAP_NOTE", "C4")                                                       # 261.6 Hz: the fourth over the bass's G, in the one band of the song with nothing in it (231 to 270 Hz)
LAP_VEL = 0.8
LAP_GAIN = os.environ.get("C11T7_LAP_GAIN", "-10dB")


def lap_strokes():
    """(beat, strokes to the bar, sixteenths from the nearest sixteenth: - before it, + after) of every stroke."""
    out = []
    for b0, n, per in (LAP_PLAN if LAP else ()):
        for bar in range(b0, b0 + n):
            for k in range(per):
                x = k * BAR / per
                out.append(((bar + k / per) * BEATS, per, x - round(x)))
    return out


def lap_notes():
    return [{"at": round(t, 6), "len": 0.05, "pitch": LAP_NOTE, "vel": LAP_VEL} for t, per, off in lap_strokes()]


JET = os.environ.get("C11T7_JET", "1") != "0" and COMB                # v13: the click, held, through a phaser
JET_IN, JET_WITHOUT = "drifts", "kick"                                # it sounds in the bars of this section in which this part stands back
VERN = os.environ.get("C11T7_VERN", "1") != "0" and os.environ.get("C11T7_FIVE", "1") != "0" and JET      # v15: the vernier (seventeen ticks in the bar's sixteen)
VERN_N = int(os.environ.get("C11T7_VERN_N", "17"))                   # ticks in a bar: one more than its sixteenths, so they agree once a bar
VERN_IN = ("slips", 0, int(os.environ.get("C11T7_VERN_BARS", "24")))    # the section, and the bars of it: B's first three slips. It stops a row (8 bars) BEFORE the hat comes in at bar 57:
                                                                     # run to the hat (32 bars) the scorer lost the hat's entry as a cut (8 sections to 7, structure 99.4 to 98.3) and the hat arrived on a top that was already ticking
VERN_NOTE, VERN_LEN, VERN_VEL = "G5", 0.03, 0.7                      # the song's own small high click (`os-air`), every mark alike
VERN_GAIN = os.environ.get("C11T7_VERN_GAIN", "-18dB")               # set in the whole song's master: a tick then peaks 12 dB under the clicks' peaks (at -12 dB it peaked 6 under, and up to -1.6 dBFS: with the click, not under it)
FIVE = os.environ.get("C11T7_FIVE", "1") != "0" and JET              # v14: two, three, five (a third pump, over the bass)
FIVE_NOTE, FIVE_F0 = "C4", 261.6256                                  # a fourth over the click's G3: 262 Hz, between the bass's harmonics at 196 and 294
FIVE_RATE = 2.5                                                      # cycles a beat between the pair's two tones: it swells five times in two beats (the bass twice, the D pair three times)
FIVE_WITH = ("bass", "bassb")                                        # it sounds in every bar in which the bass does, on G or on B flat. RESTING it where the bass goes to B flat (12 bars) was tried: those bars then matched the bars they return to less (0.54 to 0.48) and the scorer's recurrence fell 100 to 87
FIVE_GAIN = os.environ.get("C11T7_FIVE_GAIN", "-34dB")               # NOT SETTLED BY THE MUSIC ALONE, said plainly: in the master it reads 14 dB under the music and 12 dB under the bass's own band, which by the equal-loudness curves (from memory, not measured) is about as loud as the bass. I first chose -40 dB for that reason; at -40 the scorer's recurrence fell 100 to 85 (the song sits 0.024 over that term's floor and the quieter pair tipped it), at -34 it holds. An ear should say which
JET_GAIN = os.environ.get("C11T7_JET_GAIN", "-22dB")
JET_RATE = "8b"                                                       # the phaser's notches go there and back every eight beats (two bars)
JET_STAGES, JET_DEPTH, JET_FEEDBACK, JET_MIX = 8, 0.9, 0.5, 0.5


def jet_span():
    """(first bar, the bar after its last) of the held note, or None."""
    bars = [bar for name, b0, n, parts, phase in SECS if name == JET_IN for bar in range(b0, b0 + n) if not plays(JET_WITHOUT, bar)]
    return (min(bars), max(bars) + 1) if JET and bars else None


def jet_notes():
    lo, hi = jet_span()
    return [{"at": float(lo * BEATS), "len": float((hi - lo) * BEATS), "pitch": NOTE, "vel": 0.8}]


def vern_span():
    """(first bar, bar after the last), from 0."""
    at = 0
    for nm, rows, *_ in SECTIONS:
        if nm == VERN_IN[0]:
            return at + VERN_IN[1], at + VERN_IN[2]
        at += rows * ROW
    raise KeyError(VERN_IN[0])


def vern_notes():
    """VERN_N ticks, evenly, in every bar of the span."""
    b0, b1 = vern_span()
    return [{"at": round(b * BEATS + k * BEATS / VERN_N, 5), "len": VERN_LEN, "pitch": VERN_NOTE, "vel": VERN_VEL} for b in range(b0, b1) for k in range(VERN_N)]


def five_ratios():
    """(ratio of the lower tone, ratio of the upper): FIVE_RATE cycles a beat apart, about a mean as sharp as the bass's own."""
    sharp = 1 + DELTA / 2 / F0
    half = FIVE_RATE * BPM / 60 / 2 / FIVE_F0
    return (sharp - half, sharp + half)


def five_notes(bars):
    """One held note a bar, struck where the bass is (the first off-beat); the last is let go where the pair has just died of itself."""
    dies = (math.floor((BEATS - 0.5) * FIVE_RATE - 0.5) + 0.5) / FIVE_RATE / STEP
    return [note(bar * BEATS + 2 * STEP, FIVE_NOTE, (dies if bar + 1 not in bars else 15.6) * STEP, 0.9) for bar in bars]


def five_swells(beats=2.0):
    return [round(0.5 + n / FIVE_RATE, 3) for n in range(int((beats - 0.5) * FIVE_RATE + 1e-9) + 1)]


def hemi_span():
    """The bars in which the second pump sounds: [(from, to), ...], or []."""
    if not HEMI_ON:
        return []
    out = []
    for nm, lo, hi in HEMI_IN:
        sec = next((x for x in SECS if x[0] == nm), None)
        if sec is not None:
            out.append((sec[1] + lo, sec[1] + hi))
    return out


def hemi_ratios():
    """(ratio of the lower tone, ratio of the upper, dB) for each pair: HEMI_RATE cycles a beat apart, about a mean that is as sharp as the bass's own (half of DELTA over G2)."""
    sharp = 1 + DELTA / 2 / F0
    half = HEMI_RATE * BPM / 60 / 2 / HEMI_F0
    return [(k * sharp - half, k * sharp + half, lv) for k, lv in HEMI_PARTS]


def hemi_notes():
    last = max(b1 for b0, b1 in hemi_span()) - 1
    dies = (math.floor((BEATS - 0.5) * HEMI_RATE - 0.5) + 0.5) / HEMI_RATE / STEP      # sixteenths from the stroke to the last time in the bar that the pair has died of itself
    return [note(bar * BEATS + s * STEP, p, n * STEP, v) for b0, b1 in hemi_span() for bar in range(b0, b1)
            for s, p, n, v in [(2, HEMI_NOTE, dies if bar == last else 15.6, 0.9)]]      # the last one is let go where it has just died (half a beat before the line): nothing of it is in the bars after      # struck where the bass is, on the off-beat, and held for the bar


def hemi_swells(beats=2.0):
    """Beats (from a bar line) at which a pair struck on the first off-beat swells: the second pump's, and the bass's."""
    return [[round(0.5 + n / r, 3) for n in range(int((beats - 0.5) * r + 1e-9) + 1)] for r in (HEMI_RATE, DELTA * 60 / BPM)]


def roll_strokes():
    """One roll going up: (beats after it begins, the rate there in strokes a second) of every stroke."""
    beat = 60 / BPM
    r0, r1, tg = 1 / (STEP * beat), WAVE_HZ, ROLL_GLIDE * beat
    a = math.log(r1 / r0) / tg                                   # the rate is r0 * exp(a t): stroke n is where its integral is n
    out, n = [], 0
    while math.log(1 + n * a / r0) / a < tg:
        t = math.log(1 + n * a / r0) / a
        out.append((t / beat, r0 * math.exp(a * t)))
        n += 1
    t = out[-1][0] * beat
    while t + 1 / r1 < (ROLL_GLIDE + ROLL_HOLD) * beat - 0.5 / r1:   # then a stroke every turn of the wave, to the bar line
        t += 1 / r1
        out.append((t / beat, r1))
    return out


def roll_spans():
    """(the beat a roll begins at, which way it goes) for every roll."""
    if not ROLL_ON:
        return []
    return [(( next(x for x in SECS if x[0] == nm)[1] + bar) * BEATS, way) for nm, bar, way in ROLL_AT if any(x[0] == nm for x in SECS)]


def roll_notes():
    beat = 60 / BPM
    out = []
    for t0, way in roll_spans():
        for t, r in roll_strokes():
            at = t0 + (t if way == "up" else ROLL_GLIDE + ROLL_HOLD - t)
            if way == "down" and t == 0:
                continue                                       # the mirror of the first stroke is the next bar line: A's
            out.append({"at": round(at, 6), "len": 0.05, "pitch": NOTE, "vel": round(ROLL_VEL * (r * STEP * beat) ** -ROLL_FALL, 4)})
    return sorted(out, key=lambda n: n["at"])


def scale_span():
    """The beats between which one click plays its wave's own notes, or None."""
    sec = next((x for x in SECS if x[0] == SCALE_IN[0]), None) if SCALE_ON else None
    return ((sec[1] + SCALE_IN[1]) * BEATS, (sec[1] + SCALE_IN[2]) * BEATS) if sec else None


def scale_strokes():
    """(the beat of a stroke, n): on every SCALE_EVERY sixteenths, up SCALE_STEPS and down them."""
    lo, hi = scale_span()
    cyc = SCALE_STEPS + SCALE_STEPS[::-1]
    return [(lo + i * SCALE_EVERY * STEP, cyc[i % len(cyc)]) for i in range(int(round((hi - lo) / (SCALE_EVERY * STEP))))]


def scale_notes(k):
    """The k-th copy (0 is the first) of every stroke that has one: k n-ths of a turn of the click's wave after the stroke."""
    turn = BPM / 60 / WAVE_HZ                        # beats in one turn of the click's wave
    return [note(t + k * turn / n, NOTE, STEP, SCALE_VEL) for t, n in scale_strokes() if k < n]


def note(at, pitch, length, vel):
    return {"at": round(at, 5), "len": round(length, 4), "pitch": pitch, "vel": round(vel, 3)}


def part(name, steps):
    out = []
    for bar in range(BARS):
        if plays(name, bar):
            out += [note(bar * BEATS + s * STEP, p, n * STEP, v) for s, p, n, v in steps(bar)]
    return out


VEL = lambda s: 0.9 if s % LOOP == 0 else 0.76


def open_lane():
    """How bright both clicks are: the phase itself, as a share of the loop (0 together, 1 a whole loop ahead)."""
    pts, last = [], None
    for h in range(BARS * 2 + 1):
        v = round(phi(min(h * BAR / 2, BARS * BAR - 0.001), pend=False) / LOOP, 4)
        if v != last or h == BARS * 2:
            if last is not None and pts and pts[-1][0] != f"{(h - 1) * 2:g}b":
                pts.append([f"{(h - 1) * 2:g}b", last])
            pts.append([f"{h * 2:g}b", v])
        last = v
    return pts


def apart_lane():
    """Where the two clicks stand: 0 at their usual PAN, 1 an ear each (while the pendulum swings). They part and
    come back in the last sixteenth of a bar, which is one of the pattern's holes, with B exactly on A."""
    pts = [["0b", 0]]
    for name, b0, n, parts, phase in SECS:
        if phase[0] == "pend":
            lo, hi = (b0 + phase[1]) * BEATS, (b0 + phase[2]) * BEATS
            pts += ([[f"{lo - 0.125:g}b", 0]] if lo > 0 else []) + [[f"{lo:g}b", 1], [f"{hi - 0.125:g}b", 1], [f"{hi:g}b", 0]]
    return pts + [[f"{TOTAL:g}b", 0]]


def click_pan(side):
    return {"value": side * PAN, "mod": [{"src": "auto.apart", "amount": round(side * (PEND_APART - PAN), 4)}]} if PEND_ON else side * PAN


def click_fx():
    return {"fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.apart", "amount": PEND_GAIN}]}}]} if PEND_ON else {}


def click_auto():
    return {"open": {"points": open_lane()}, **({"apart": {"points": apart_lane()}} if PEND_ON else {})}


def shape_span():
    """The beats between which the two clicks have an ear each (B is exactly on A when it begins), or None."""
    sec = next((x for x in SECS if x[4][0] == "slips"), None) if SHAPE_ON else None
    return (sec[1] * BEATS, (sec[1] + min(SHAPE_ROWS * ROW, sec[2])) * BEATS) if sec and SHAPE_ROWS > 0 else None


def shape_gain():
    """dB a click is turned up when it is moved from PAN to SHAPE_APART, so that the two ears added are what they were: a part at p gives its far ear 1 - p."""
    return 20 * math.log10((2 - PAN) / (2 - SHAPE_APART))


def eared(notes, inside):
    """The notes of a click inside (or outside) the bars in which it has an ear to itself."""
    sp = shape_span()
    return [n for n in notes if (sp is not None and sp[0] <= n["at"] < sp[1]) == inside]


def a_notes():
    return [note(s * STEP, NOTE, 0.5 * STEP, VEL(s)) for s in range(BARS * BAR) if s % LOOP in PATTERN and plays("a", s // BAR)]


def c_notes():
    """The complement: C strikes the pattern's holes, on the grid."""
    return [note(s * STEP, "G5", 0.25 * STEP, 0.85 if s % LOOP == COMP[0] else 0.72) for s in range(BARS * BAR) if s % LOOP in COMP and plays("c", s // BAR)]


def doubles(k):
    """The sixteenths of the half-bar on which A and B strike together when B is k ahead."""
    return tuple(s for s in PATTERN if (s + k) % LOOP in PATTERN)


def tune_lock(bar):
    """The lock whose tune a bar plays (0 to LOOP), or None: B must be within TUNE_NEAR of it for the whole bar."""
    if not plays("tune", bar):
        return None
    p0, p1 = phi(bar * BAR), phi((bar + 1) * BAR - 0.001)
    k = round((p0 + p1) / 2)
    return k if abs(p0 - k) <= TUNE_NEAR and abs(p1 - k) <= TUNE_NEAR else None


def tune_notes():
    out = []
    for bar in range(BARS):
        k = tune_lock(bar)
        if k is not None:
            d = doubles(k)
            out += [note((bar * BAR + half + s) * STEP, TUNE[s], 1 * STEP, 0.85 if s == d[0] else 0.72) for half in (0, LOOP) for s in d]
    return out


def canon_phase(x):
    """Sixteenths the tune's second voice is ahead of the tune, x sixteenths after it sets off."""
    i, r = divmod(x, CANON_HOLD * BAR)
    u = min(1.0, r / (CANON_SLIDE * BAR))
    return i + u * u


def canon_notes():
    """The tune's own B: the same five notes on the same loop, each sounding when x + canon_phase(x) reaches it."""
    b0, n = next((sec[1] + CANON_FROM, sec[2] - CANON_FROM) for sec in SECS if sec[0] == "home")
    out = []
    for q in range(n * BAR + 2 * LOOP):
        if q % LOOP in TUNE:
            x = float(q)
            for _ in range(60):
                x = q - canon_phase(max(x, 0.0))
            if 0 <= x < n * BAR - 1e-6:
                p = TUNE[q % LOOP]
                out.append(note((b0 * BAR + x) * STEP, p[:-1] + str(int(p[-1]) + CANON_OCT), 1 * STEP, 0.85 if q % LOOP == 0 else 0.74))
    return out


def canon_lock(k):
    """What the two voices play on each sixteenth of the half-bar when the second is k ahead: (the tune's note or None, the second's or None)."""
    return [(TUNE.get(st), TUNE.get((st + k) % LOOP)) for st in range(LOOP)]


def b_notes():
    out = []
    for b in range(int(BARS * BAR + 9)):
        if b % LOOP in PATTERN:
            t = when(b)
            if 0 <= t < BARS * BAR and plays("b", int(t // BAR)):
                out.append(note(t * STEP, NOTE, 0.5 * STEP, VEL(b)))
    return out


KICK = lambda bar: [(s, "G1", 1, 0.95 if s == 0 else 0.9) for s in (0, 4, 8, 12)]
CLAP = lambda bar: [(4, "C4", 1, 0.8), (12, "C4", 1, 0.86)]
HAT = lambda bar: [(s, "A#4", 1, 0.8) for s in (2, 6, 10, 14)]
BASS = lambda bar: [(2, "G2", 15.6, 0.9)]      # struck on the off-beat, held for the bar: its two tones agree on the off-beats


def bass_lock(bar):
    """The lock the bass hears in a bar: the one B is in when the bass strikes (in "drifts", the one B is nearest)."""
    t = bar * BAR + 2
    p = phi(t, pend=False) if PEND_ON else phi(t)
    kind = next(ph[0] for name, b0, n, parts, ph in SECS if b0 <= bar < b0 + n)
    return int(round(p)) if kind == "drift" else int(math.floor(p + 1e-9))


def bass_note(bar):
    """The first stroke the two clicks share at that lock, two octaves under its note in the tune: G or B flat."""
    kind = next(ph[0] for name, b0, n, parts, ph in SECS if b0 <= bar < b0 + n)
    return TUNE[doubles(bass_lock(bar))[0]].replace("4", "2") if ROOT_ON and kind in ROOT_IN else "G2"


BASS_G = lambda bar: BASS(bar) if bass_note(bar) == "G2" else []
BASS_B = lambda bar: [(2, "Bb2", 15.6, 0.9)] if bass_note(bar) == "Bb2" else []

R = 1 + DELTA / F0             # the second tone of each pair, as a ratio of the note
PATCHES = {
    "os-click": {"about": "Out of Step's click (chirper-zero, 26 Nov): five cycles of a saw on G3 dying in 22 ms, lifted 9 dB round 9 kHz, started at the same point of its wave every time, through a low-pass that both clicks share (it opens with the phase): nothing in it is random, so two of them struck together are one click, and two struck a millisecond apart are a comb. (The machine's rim was tried first: two rims differ by 22 dB under one, and its note stood 16 to 25 dB over the album's envelope.)",
                 "play": {"vel_sens": 0.5},
                 "synth": {"layers": ["saw phase=0"], "filters": ["hp cutoff=500", "peak cutoff=9000 q=0.7 gain=9dB", {"kind": "lp", "cutoff": {"value": DULL, "mod": [{"src": "auto.open", "amount": OCTAVES}]}, "q": 0.7}], "amp": {"a": "0.1ms", "d": "22ms", "s": 0, "r": "10ms", "curve": 3}}},
    "os-comp": {"about": "Out of Step's third click (chirper-zero, 26 Nov, v2): the complement's. Two cycles of a saw on G5 dying in 12 ms, above 3 kHz, lifted 8 dB round 10 kHz: small and bright, so that it is heard as the holes being filled and not as a third pattern.",
                "play": {"vel_sens": 0.5},
                "synth": {"layers": ["saw phase=0"], "filters": ["hp cutoff=3000", "peak cutoff=10000 q=0.7 gain=8dB"], "amp": {"a": "0.1ms", "d": "12ms", "s": 0, "r": "8ms", "curve": 3}}},
    "os-tune": {"about": "Out of Step's pip (chirper-zero, 26 Nov, v3): a small glass tone (a sine with its twelfth, 140 ms), which plays only the sixteenths on which the two clicks strike together, a note for each stroke of the pattern.",
                "play": {"vel_sens": 0.6},
                "synth": {"layers": ["sine", "sine ratio=3 level=-14dB"], "amp": {"a": "0.3ms", "d": "140ms", "s": 0, "r": "40ms", "curve": 3}}},
    "os-kick": {"about": "Out of Step's bass drum (chirper-zero, 26 Nov): the engine's machine kick, short and dry, on G1.",
                "play": {"vel_sens": 0.3},
                "synth": {"layers": [{"type": "machine", "machine": {"part": "kick", "decay": "260ms", "click": 0.6, "drive": 0.35, "punch": 22, "punch_time": "32ms"}}],
                          "filters": ["hp cutoff=28"], "amp": {"a": "0.1ms", "d": "0s", "s": 1, "r": "1s"}}},
    "os-hat": {"about": "Out of Step's hat (chirper-zero, 26 Nov): the machine's hat, 45 ms, on the off-beats once the two clicks are home.",
               "play": {"vel_sens": 0.4},
               "synth": {"layers": [{"type": "machine", "machine": {"part": "hat", "decay": "45ms"}}], "filters": ["hp cutoff=6000"], "amp": {"a": "0.1ms", "d": "0s", "s": 1, "r": "150ms"}}},
    "os-clap": {"about": "Out of Step's clap (chirper-zero, 26 Nov): the machine's clap, three bursts, short, dry.",
                "play": {"vel_sens": 0.4},
                "synth": {"layers": [{"type": "machine", "machine": {"part": "clap", "bursts": 3, "decay": "140ms"}}], "amp": {"a": "0.1ms", "d": "0s", "s": 1, "r": "400ms"}}},
    "os-bass": {"about": f"Out of Step's bass (chirper-zero, 26 Nov): three pairs of sines, at G2 and its second and third harmonics, each pair {DELTA:g} Hz apart (one cycle a beat at {BPM}; ratio {R:.6f} for G2 ONLY: another note needs its own ratio). They start together, so struck on the off-beat they cancel on every beat: a pump with no compressor.",
                "play": {"mono": True, "vel_sens": 0.2},
                "synth": {"layers": [x for h, lv in ((1, -3), (2, -9), (3, -15)) for x in (f"sine phase=0 ratio={h} level={lv}dB", f"sine phase=0 ratio={h + DELTA / F0:.6f} level={lv - 1.5}dB")],
                          "amp": {"a": "4ms", "d": "0s", "s": 1, "r": "30ms"}}},
    "os-bass-b": {"about": f"Out of Step's second bass (chirper-zero, 26 Nov, v5): the same three pairs of sines built on B flat 2 ({F0B} Hz), each pair {DELTA:g} Hz apart (ratio {1 + DELTA / F0B:.6f} for B flat 2 only), so it pumps on the beat as the G does. It sounds at the locks whose first shared stroke is the pattern's second.",
                  "play": {"mono": True, "vel_sens": 0.2},
                  "synth": {"layers": [x for h, lv in ((1, -3), (2, -9), (3, -15)) for x in (f"sine phase=0 ratio={h} level={lv}dB", f"sine phase=0 ratio={h + DELTA / F0B:.6f} level={lv - 1.5}dB")],
                            "amp": {"a": "4ms", "d": "0s", "s": 1, "r": "30ms"}}},
}


def song():
    doc = {
        "about": "Chirpers - Escapement, track 7 by chirper-zero: OUT OF STEP. Two clicks, the same sound and the same half-bar pattern; one is on the grid, the other slips a sixteenth ahead every eight bars and catches there (eight locks, then home), and later drifts back without stopping. Where they part they make a comb; the bass is two sines one cycle a beat apart that cancel on every beat. Generated by compose/chirpers11/src/chirpers11-t7.py.",
        "tempo": BPM,
        "ceiling": "-1dB",
        "loudness": -11.0,
        "seed": 1,
        "tail": "2s",
        "length": f"{TOTAL}b",
        "event_stable": True,
        "patches": PATCHES,
        "buses": {"room": {"fx": ["reverb kind=room decay=0.5s mix=1", "hp cutoff=400"]}},
        "master": {"fx": [{"type": "eq", "bands": ["hp cutoff=30"]}, {"type": "compressor", "threshold": "-18dB", "ratio": 2, "attack": "20ms", "release": "160ms", "makeup": "0dB"}]},
        "tracks": [
            {"name": "kick", "patch": "os-kick", "gain": "-8dB", "pan": 0.0, "notes": part("kick", KICK)},
            {"name": "a", "patch": "os-click", "gain": "-2dB", "pan": click_pan(-1), "sends": {"room": "-16dB"}, **click_fx(), "auto": click_auto(), "notes": mid(eared(a_notes(), False), False)},
            {"name": "b", "patch": "os-click", "gain": "-2dB", "pan": click_pan(1), "sends": {"room": "-16dB"}, **click_fx(), "auto": click_auto(), "notes": mid(eared(b_notes(), False), False)},
            {"name": "bass", "patch": "os-bass", "gain": "-23dB", "pan": 0.0, "notes": part("bass", BASS_G if ROOT_ON else BASS)},
            {"name": "hat", "patch": "os-hat", "gain": "-1dB", "pan": 0.0, "sends": {"room": "-16dB"}, "notes": part("hat", HAT)},
            {"name": "clap", "patch": "os-clap", "gain": "-5dB", "pan": 0.0, "sends": {"room": "-10dB"}, "notes": part("clap", CLAP)},
        ],
    }
    if ROOT_ON:
        i = next(k for k, t in enumerate(doc["tracks"]) if t["name"] == "bass")
        doc["tracks"].insert(i + 1, {"name": "bassb", "patch": "os-bass-b", "gain": "-23dB", "pan": 0.0, "notes": part("bass", BASS_B)})
        doc["about"] = doc["about"].replace(" Generated by", " From v5, while B drifts home, the bass plays the first stroke the two clicks share at each lock B passes, G or B flat: it moves for the first time, and says where the locks are. Generated by")
    else:
        del PATCHES["os-bass-b"]
    if PEND_ON:
        doc["about"] = doc["about"].replace(" Generated by", f" From v4, while the two are one click (the opening and the ending) they are given an ear each and one swings {PEND_MS:g} ms ahead of the other and behind it: the click is heard to swing from ear to ear, with nothing panned. Generated by")
    if COMP_ON:
        doc["tracks"].append({"name": "c", "patch": "os-comp", "gain": "-6dB", "pan": 0.0, "sends": {"room": "-16dB"}, "notes": c_notes()})
        doc["about"] = doc["about"].replace(" Generated by", " From v2 a third click plays the pattern's three holes once the two are home: together they sound every sixteenth exactly once, and apart they collide. Generated by")
    else:
        del PATCHES["os-comp"]
    if TUNE_ON:
        doc["tracks"].append({"name": "tune", "patch": "os-tune", "gain": "-18dB", "pan": 0.0, "sends": {"room": "-10dB"}, "notes": tune_notes()})
        doc["about"] = doc["about"].replace(" Generated by", " From v3 a small pip plays the sixteenths on which the two clicks strike together, a note for each stroke of the pattern (G, B flat, D, F, A): every lock has its own tune, and home is the whole chord. Generated by")
    else:
        del PATCHES["os-tune"]
    if shape_span():
        for nm, side, notes in (("a-ear", -1, a_notes()), ("b-ear", 1, b_notes())):
            doc["tracks"].append({"name": nm, "patch": "os-click", "gain": f"{-2 + shape_gain():.2f}dB", "pan": round(side * SHAPE_APART, 3),
                                  "sends": {"room": "-16dB"}, "auto": {"open": {"points": open_lane()}}, "notes": eared(notes, True)})
        doc["about"] = doc["about"].replace(" Generated by", " From v7, for the first four rows of the slips, A has the left ear and B the right (0.85 of the way): the strokes they share are one click in the middle, each one's own are at its side, and as B slips the middle click leans, then splits (on one speaker the two clicks are as they were). Generated by")
        assert "From v7" in doc["about"]
    if wave_span():
        for nm, side, notes in (("a-mid", -1, a_notes()), ("b-mid", 1, b_notes())):
            doc["tracks"].append({"name": nm, "patch": "os-click", "gain": f"{-2 + wave_gain():.2f}dB", "pan": round(side * WAVE_PAN, 3),
                                  "sends": {"room": "-16dB"}, "auto": {"open": {"points": open_lane()}}, "notes": mid(notes, True)})
        doc["about"] = doc["about"].replace(" Generated by", " From v8, for the last eight bars of one click, the two clicks stand in one place and B goes half a turn of the click's own wave ahead (2.55 ms), then a whole turn, and back: at half a turn the odd harmonics cancel and the click is heard an octave up; at a whole turn it is itself again. Generated by")
        assert "From v8" in doc["about"]
    if scale_span():
        for k in range(max(SCALE_STEPS)):
            doc["tracks"].append({"name": f"wave-{k + 1}", "patch": "os-click", "gain": f"{SCALE_GAIN:g}dB", "pan": 0.0,
                                  "sends": {"room": "-16dB"}, "auto": {"open": {"points": open_lane()}}, "notes": scale_notes(k)})
        doc["about"] = doc["about"].replace(" Generated by", " From v9, in the second row of one again, one click plays its wave's own scale: struck n times, a n-th of a turn of its wave apart, it is the click on n times its note and no higher in peak (G3 G4 D5 G5 D6 F6 G6 A6 for n = 1 2 3 4 6 7 8 9), a click a beat, up and down twice. Generated by")
        assert "From v9" in doc["about"]
    if roll_spans():
        doc["tracks"].append({"name": "roll", "patch": "os-click", "gain": f"{ROLL_GAIN:g}dB", "pan": 0.0,
                              "sends": {"room": "-16dB"}, "auto": {"open": {"points": open_lane()}}, "notes": roll_notes()})
        doc["about"] = doc["about"].replace(" Generated by", " From v10 the click rolls: from sixteenths it quickens by the same ratio every beat until its strokes are one turn of its own wave apart, 196 a second, where every stroke is in step with the last one's tail and the row of clicks is one held note, G3: once, in the two bars of slips where the drum rests, landing on its return. Generated by")
        assert "From v10" in doc["about"]
    if comb_span():
        PATCHES["os-air"] = {"about": "Out of Step's small bright click (chirper-zero, 26 Nov, v12): a saw from phase nought with everything under 6.5 kHz taken off and a lift round 14 kHz, gone in 10 ms: no noise in it, so two of them are the same to the sample, and two of them n samples apart are a comb.",
                             "play": {"vel_sens": 0.5, "gate": 1},
                             "synth": {"layers": ["saw phase=0"], "filters": ["hp cutoff=6500", "hp cutoff=6500", "peak cutoff=14000 q=0.7 gain=6dB"], "amp": {"a": "0.1ms", "d": "10ms", "s": 0, "r": "5ms", "curve": 2}}}
        for nm, second in (("air-1", False), ("air-2", True)):
            doc["tracks"].append({"name": nm, "patch": "os-air", "gain": COMB_GAIN, "pan": 0.0, "notes": comb_notes(second)})      # dry, in the same place
        doc["about"] = doc["about"].replace(" Generated by", " From v12 a small bright click on the odd sixteenths, wherever the hat plays, is two clicks in one place: in slips and drifts the second goes up to twelve samples behind the first and back every four bars (too close to be heard as two, they are heard as a colour: a comb whose notches walk down the undertones of 24 kHz and up again), and in home they are in step to the sample. Generated by")
        assert "From v12" in doc["about"]
    if hemi_span():
        PATCHES["os-bass-d"] = {"about": f"Out of Step's second pump (chirper-zero, 26 Nov, v11): two pairs of sines, on D2 and its octave, each pair {HEMI_RATE * BPM / 60:g} Hz apart (a cycle and a half a beat at {BPM}), both tones of a pair as loud as each other. Struck on the off-beat it swells three times in two beats, where the bass swells twice: three against two. The pair's mean is as sharp as the bass's ({1200 * math.log2(1 + DELTA / 2 / F0):.1f} cents). For D2 ONLY: another note needs its own ratios.",
                                "play": {"mono": True, "vel_sens": 0.2},
                                "synth": {"layers": [x for lo, hi, lv in hemi_ratios() for x in (f"sine phase=0 ratio={lo:.6f} level={lv:g}dB", f"sine phase=0 ratio={hi:.6f} level={lv:g}dB")], "amp": {"a": "4ms", "d": "0s", "s": 1, "r": "30ms"}}}
        doc["tracks"].append({"name": "bassd", "patch": "os-bass-d", "gain": HEMI_GAIN, "pan": 0.0, "notes": hemi_notes()})      # dry and in the middle, as the bass is
        doc["about"] = doc["about"].replace(" Generated by", " From v11 the bass has a second pair of tones under it from the middle of drifts until it stops, on D2 and a cycle and a half a beat apart: it swells three times in two beats while the bass swells twice, and the two agree once every two beats: three against two, from four sines. Generated by")
        assert "From v11" in doc["about"]
    if FIVE:
        bars = sorted({int(n["at"] // BEATS) for t in doc["tracks"] if t["name"] in FIVE_WITH for n in t["notes"]})
        lo, hi = five_ratios()
        PATCHES["os-five"] = {"about": f"Out of Step's third pump (chirper-zero, 27 Nov, v14): two sines on C4, {FIVE_RATE * BPM / 60:g} Hz apart (two and a half cycles a beat at {BPM}), as loud as each other. Struck on the off-beat it swells five times in two beats, where the bass swells twice and the D pair three times; between swells there is nothing.",
                              "play": {"mono": True, "vel_sens": 0.2},
                              "synth": {"layers": [f"sine phase=0 ratio={lo:.6f} level=-3dB", f"sine phase=0 ratio={hi:.6f} level=-3dB"], "amp": {"a": "4ms", "d": "0s", "s": 1, "r": "30ms"}}}
        doc["tracks"].append({"name": "five", "patch": "os-five", "gain": FIVE_GAIN, "pan": 0.0, "notes": five_notes(bars)})      # dry and in the middle, as the bass is
        doc["about"] = doc["about"].replace(" Generated by", " From v14 a third pair of tones sounds wherever the bass does, on C4 and two and a half cycles a beat apart: it swells five times in two beats while the bass swells twice and the D pair three times, and all three agree once every two beats: two against three against five, from six tones that never change. Generated by")
        assert "From v14" in doc["about"]
    if CANON_ON:
        doc["tracks"].append({"name": "tune2", "patch": "os-tune", "gain": CANON_GAIN, "pan": PAN, "sends": {"room": "-10dB"}, "notes": canon_notes()})
        doc["about"] = doc["about"].replace(" Generated by", " From v6, in the second row of home, the tune has a B of its own: a second pip an octave lower plays the same five notes and slips a sixteenth ahead of the tune every two bars, so the tune is heard in canon with itself at four distances (Piano Phase's way, in the record's chord). Generated by")
        assert "From v6" in doc["about"]
    if lap_strokes():
        PATCHES["os-lap"] = {"about": "Out of Step's wooden click (chirper-zero, 26 Nov, v13): a sine and a saw from phase nought on C4 with the top taken off, gone in 30 ms: a small tock with a note, told from the two clicks (which have nothing under 500 Hz) by its body. It plays 17, 18, 19 and 20 strokes to the bar against the song's 16.",
                             "play": {"vel_sens": 0.5, "gate": 1},
                             "synth": {"layers": ["sine phase=0", "saw phase=0 level=-6dB"], "filters": ["hp cutoff=180", "lp cutoff=3000 q=0.7"], "amp": {"a": "0.1ms", "d": "30ms", "s": 0, "r": "10ms", "curve": 3}}}
        doc["tracks"].append({"name": "lap", "patch": "os-lap", "gain": LAP_GAIN, "pan": 0.0, "notes": lap_notes()})      # dry, in the middle
        doc["about"] = doc["about"].replace(" Generated by", " With C11T7_LAP=1, for the last eight bars before the bass drum stands back in drifts, a wooden click plays seventeen even strokes to the bar against the song's sixteen, then eighteen, nineteen and twenty: it laps the song once a bar, then twice, three and four times, which is once a beat, the rate at which the bass's two tones swell. Generated by")
        assert "With C11T7_LAP=1" in doc["about"]
    if jet_span():
        PATCHES["os-held"] = {"about": "Out of Step's click, held (chirper-zero, 26 Nov, v13): a saw from phase nought on the click's note with the click's own high-pass (nothing under 500 Hz) and the top rounded at 6 kHz. It is the note the roll arrives at, a click struck 196 times a second. Made to go through a phaser.",
                              "play": {"vel_sens": 0, "gate": 1},
                              "synth": {"layers": ["saw phase=0"], "filters": ["hp cutoff=500", "lp cutoff=6000 q=0.7"], "amp": {"a": "30ms", "d": "0s", "s": 1, "r": "80ms"}}}
        doc["tracks"].append({"name": "held", "patch": "os-held", "gain": JET_GAIN, "pan": 0.0,
                              "fx": [{"type": "phaser", "stages": JET_STAGES, "depth": JET_DEPTH, "feedback": JET_FEEDBACK, "mix": JET_MIX, "rate": JET_RATE}], "notes": jet_notes()})      # dry, in the middle
        doc["about"] = doc["about"].replace(" Generated by", " From v13, in the eight bars of drifts in which the bass drum stands back, the click's own note is held (the note the roll arrives at) and goes through a phaser: which of its harmonics are weakened sweeps there and back every two bars. Generated by")
        assert "through a phaser" in doc["about"]
    if VERN:
        doc["tracks"].append({"name": "vern", "patch": "os-air", "gain": VERN_GAIN, "pan": 0.0, "notes": vern_notes()})      # dry and in the middle, between the two clicks
        b0, b1 = vern_span()
        doc["about"] = doc["about"].replace(" Generated by", f" From v15 a vernier runs through bars {b0 + 1} to {b1}: {VERN_N} small high ticks in every bar against its sixteen sixteenths, so the ticks are with the click at the bar line and slip a whole sixteenth ahead of it by the bar's end, once every bar. Generated by")
        assert "From v15" in doc["about"]
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


def lock(k):
    """What they make when B is k sixteenths ahead: one half-bar, X A and B, a or b one of them, . neither; with C: c C alone, * B and C together."""
    b = {(p - k) % LOOP for p in PATTERN}
    def cell(s):
        if s in PATTERN:
            return "X" if s in b else "a"
        if COMP_ON:
            return "*" if s in b else "c"
        return "b" if s in b else "."
    return " ".join(cell(s) for s in range(LOOP))


if __name__ == "__main__":
    if os.environ.get("C11T7_SHOW"):
        sec = 60 / BPM * BEATS
        for name, b0, n, parts, phase in SECS:
            print(f"{name:10s} bars {b0:3d}-{b0 + n:3d}  {int(b0 * sec) // 60}:{b0 * sec % 60:04.1f}-{int((b0 + n) * sec) // 60}:{(b0 + n) * sec % 60:04.1f}  phase {phase}  " + ", ".join(p if w is None else p + " " + "+".join(f"{lo}-{hi}" for lo, hi in w) for p, w in parts.items()))
        for k in range(LOOP + 1):
            print(f"   B {k} ahead:  {lock(k)}" + (f"   the tune: {' '.join(TUNE[s] if s in doubles(k) else '.' for s in range(LOOP))}" if TUNE_ON else ""))
        if wave_span():
            lo, hi = wave_span()
            print(f"half a wave out of step, bars {lo // BEATS + 1:g}-{hi // BEATS:g} ({lo * 60 / BPM:.1f}-{hi * 60 / BPM:.1f} s): A and B at {-WAVE_PAN:+.2f} and {WAVE_PAN:+.2f}, both turned {wave_gain():+.2f} dB ; the click's wave is {1000 / WAVE_HZ:.3f} ms a turn ({WAVE_HZ:.1f} Hz) ; B's lead by bar, ms: "
                  + " ".join(f"{wave_ms((lo / STEP) + k * BAR + 3):.3f}" for k in range(int((hi - lo) // BEATS))) + " ; heard: " + " ".join(("low", "HIGH")[w % 2] for w in WAVE_STEPS[:int((hi - lo) // BEATS)]))
        if shape_span():
            lo, hi = shape_span()
            print(f"the locks' shape, bars {lo // BEATS:g}-{hi // BEATS:g}: A at {-SHAPE_APART:+.2f}, B at {SHAPE_APART:+.2f}, both turned up {shape_gain():.2f} dB ; B k ahead: sixteenths in the middle / on the left / on the right: " + " ; ".join(
                f"{k}: {','.join(map(str, doubles(k)))} / {','.join(str(q) for q in PATTERN if q not in doubles(k))} / {','.join(str(q) for q in sorted((p - k) % LOOP for p in PATTERN) if q not in doubles(k))}" for k in range(1, SHAPE_ROWS + 1)))
        if CANON_ON:
            b0 = next(sec[1] + CANON_FROM for sec in SECS if sec[0] == "home")
            for k in range(1, int((2 * ROW - CANON_FROM) / CANON_HOLD) + 1):
                print(f"   the tune's own B {k} ahead (bars {b0 + (k - 1) * CANON_HOLD + CANON_SLIDE:g}-{b0 + k * CANON_HOLD:g}): " + " ".join(("+".join(q[:-1] for q in (a, b_) if q) or ".") for a, b_ in canon_lock(k)))
        if TUNE_ON:
            runs, last = [], None
            for bar in range(BARS):
                k = tune_lock(bar)
                if k != last or not runs:
                    runs.append([bar, bar + 1, k])
                else:
                    runs[-1][1] = bar + 1
                last = k
            print("   the tune by bars: " + " ".join(f"{lo}-{hi}:{k}" for lo, hi, k in runs if k is not None))
        if ROOT_ON:
            runs = []
            for bar in range(BARS):
                if plays("bass", bar):
                    k, p = bass_lock(bar), bass_note(bar)
                    if runs and runs[-1][1] == bar and runs[-1][3] == p:
                        runs[-1][1] = bar + 1; runs[-1][2].append(k)
                    else:
                        runs.append([bar, bar + 1, [k], p])
            print("   the bass by bars (the locks it hears): " + " ".join(f"{lo}-{hi}:{p}({','.join(str(q) for q in sorted(set(ks), key=ks.index))})" for lo, hi, ks, p in runs))
        if PEND_ON:
            for name, b0, n, parts, phase in SECS:
                if phase[0] == "pend":
                    print(f"   the pendulum in \"{name}\" (bars {b0 + phase[1]}-{b0 + phase[2]}, {phase[3]}): B's lead at each quarter of a bar, ms (+ the right ear first): " + " ".join(f"{lead_ms((b0 + phase[1]) * BAR + q * 4):+.2f}" for q in range(0, (phase[2] - phase[1]) * 4 + 1)))
        ms = 60 / BPM / 4 * 1000
        print("   the first slip (bars 24-26): the gap between A's stroke and B's, ms: " + " ".join(f"{(n['at'] / STEP - round(n['at'] / STEP + phi(n['at'] / STEP)) + 0) * -ms:.1f}" for n in b_notes() if 24 * BEATS <= n["at"] < 25.5 * BEATS))
        if comb_span():
            bs = comb_span(); b0 = bs[0]; sec = BEATS * 60 / BPM; st = comb_strokes()
            runs = [b for b in bs if b - 1 not in bs]; ends = [b + 1 for b in bs if b + 1 not in bs]
            print(f"   two clicks less than a wave apart, bars " + ", ".join(f"{a + 1}-{b}" for a, b in zip(runs, ends)) + f" ({len(bs)} bars, where the hat plays; from {int(b0 * sec) // 60}:{b0 * sec % 60:04.1f}): {len(st)} strokes on sixteenths {' '.join(str(x) for x, v in COMB_STEPS)} ; apart in {' and '.join(COMB_APART)} (in step for {COMB_STILL} bars, then to {COMB_MAX} samples, {1000 * COMB_MAX / RATE:.2f} ms, and back every {COMB_TURN} bars) ; in step to the sample everywhere else")
            print("      samples apart at each bar's first stroke: " + " ".join(f"{b + 1}:{comb_apart(b + 1 / 16)}" for b in bs))
            for b in range(b0 + COMB_STILL, b0 + COMB_STILL + COMB_TURN):
                print(f"      bar {b + 1}: samples apart " + " ".join(str(n) for t, n, v in st if b * BEATS <= t < (b + 1) * BEATS) + " ; the lowest notch (Hz) " + " ".join(f"{RATE / 2 / n:.0f}" if n else "-" for t, n, v in st if b * BEATS <= t < (b + 1) * BEATS))
        if lap_strokes():
            sec = BEATS * 60 / BPM; st = lap_strokes(); ms = 60 / BPM / 4 * 1000
            print(f"   one more to the bar, bars {LAP_PLAN[0][0] + 1}-{LAP_PLAN[-1][0] + LAP_PLAN[-1][1]} ({int(LAP_PLAN[0][0] * sec) // 60}:{LAP_PLAN[0][0] * sec % 60:04.1f}-{int((LAP_PLAN[-1][0] + LAP_PLAN[-1][1]) * sec) // 60}:{(LAP_PLAN[-1][0] + LAP_PLAN[-1][1]) * sec % 60:04.1f}): {len(st)} strokes of a wooden click on {LAP_NOTE}, {LAP_GAIN} ; the song has {BAR} to the bar ({1000 * sec / BAR:.1f} ms apart)")
            for b0, n, per in LAP_PLAN:
                one = [off for t, p, off in st if b0 * BEATS <= t < (b0 + 1) * BEATS]
                print(f"      bars {b0 + 1}-{b0 + n}: {per} to the bar ({1000 * sec / per:.1f} ms apart, {per / sec:.2f} a second) ; it laps the song {per - BAR} time(s) a bar ; in step with the grid {sum(1 for o in one if abs(o) < 1e-9)} time(s) a bar, exactly between two sixteenths {sum(1 for o in one if abs(abs(o) - 0.5) < 1e-9)} ; each stroke's ms from the nearest sixteenth: " + " ".join(f"{o * ms:+.0f}" for o in one))
        if jet_span():
            sec = BEATS * 60 / BPM; lo, hi = jet_span()
            print(f"   the break through a phaser, bars {lo + 1}-{hi} ({int(lo * sec) // 60}:{lo * sec % 60:04.1f}-{int(hi * sec) // 60}:{hi * sec % 60:04.1f}): the click's note ({NOTE}, {WAVE_HZ:.1f} Hz) held, {JET_GAIN} ; {JET_STAGES} all-pass stages, depth {JET_DEPTH}, feedback {JET_FEEDBACK}, mix {JET_MIX} ; a sweep there and back every {JET_RATE} ({int(JET_RATE[:-1]) * 60 / BPM:.2f} s): {(hi - lo) * BEATS / int(JET_RATE[:-1]):g} sweeps")
        if VERN:
            b0, b1 = vern_span(); barms = BEATS * 60000 / BPM; six = barms / 16
            print(f"   the vernier, bars {b0 + 1}-{b1} ({int(b0 * barms / 1000) // 60}:{b0 * barms / 1000 % 60:04.1f}-{int(b1 * barms / 1000) // 60}:{b1 * barms / 1000 % 60:04.1f}): {VERN_N} ticks a bar against 16 sixteenths, {len(vern_notes())} ticks, {VERN_GAIN} ; a tick every {barms / VERN_N:.2f} ms (a sixteenth is {six:.2f}) ; tick k is k times {barms / 16 - barms / VERN_N:.3f} ms before sixteenth k ; early by, ms: " + " ".join(f"{k * (barms / 16 - barms / VERN_N):.0f}" for k in range(VERN_N)))
        if FIVE:
            trs = {t["name"]: t for t in song()["tracks"]}; ns = trs["five"]["notes"]; bars = sorted({int(n["at"] // BEATS) for n in ns}); lo, hi = five_ratios(); sec5 = BEATS * 60 / BPM
            runs = [b for b in bars if b - 1 not in bars]; ends = [b + 1 for b in bars if b + 1 not in bars]
            print(f"   two, three, five: bars " + ", ".join(f"{a + 1}-{b}" for a, b in zip(runs, ends)) + f" ({int(bars[0] * sec5) // 60}:{bars[0] * sec5 % 60:04.1f}-{int((bars[-1] + 1) * sec5) // 60}:{(bars[-1] + 1) * sec5 % 60:04.1f}), {len(ns)} notes on {FIVE_NOTE} at {FIVE_GAIN} ; the pair {FIVE_F0 * lo:.3f} and {FIVE_F0 * hi:.3f} Hz ({FIVE_F0 * (hi - lo):.3f} Hz apart: {FIVE_RATE:g} cycles a beat) ; it swells at beats " + " ".join(f"{x:g}" for x in five_swells()) + " of the bar ; the last note of each run held " + f"{ns[-1]['len']:g} beats")
        if hemi_span():
            sec = BEATS * 60 / BPM; d, g = hemi_swells()
            print(f"   three against two, bars " + " and ".join(f"{b0 + 1}-{b1} ({int(b0 * sec) // 60}:{b0 * sec % 60:04.1f}-{int(b1 * sec) // 60}:{b1 * sec % 60:04.1f})" for b0, b1 in hemi_span()) + f", {HEMI_GAIN}: the second pair on {HEMI_NOTE}: " + " and ".join(f"{lo * HEMI_F0:.2f} + {hi * HEMI_F0:.2f} Hz ({lv:g} dB each)" for lo, hi, lv in hemi_ratios()) + f" ; {HEMI_RATE * BPM / 60:g} Hz apart ({HEMI_RATE:g} cycles a beat) ; its note {1200 * math.log2((hemi_ratios()[0][0] + hemi_ratios()[0][1]) / 2):+.1f} cents from {HEMI_NOTE} (the bass's {1200 * math.log2(1 + DELTA / 2 / F0):+.1f} from G2)")
            print(f"      in every half bar it swells at beats {' '.join(f'{x:g}' for x in d)} ; the bass at {' '.join(f'{x:g}' for x in g)} ; together at {' '.join(f'{x:g}' for x in d if x in g)}")
        if roll_spans():
            st = roll_strokes(); beat = 60 / BPM; ng = sum(1 for t, r in st if r < WAVE_HZ - 1e-9)
            nt = lambda f: (lambda m: "C C# D Eb E F F# G Ab A Bb B".split()[int(round(m)) % 12] + str(int(round(m)) // 12 - 1) + f"{100 * (m - round(m)):+.0f}c")(69 + 12 * math.log2(f / 440))
            print(f"   the roll: {len(st)} strokes in {ROLL_GLIDE + ROLL_HOLD} beats: {ng} quickening from {st[0][1]:.2f} a second (sixteenths) by {math.exp(math.log(WAVE_HZ / st[0][1]) / ROLL_GLIDE):.3f} times a beat for {ROLL_GLIDE} beats, then {len(st) - ng} a turn of the wave apart ({1000 / WAVE_HZ:.3f} ms, {WAVE_HZ:.1f} a second: {nt(WAVE_HZ)}) ; the last stroke {1000 * (ROLL_GLIDE + ROLL_HOLD - st[-1][0]) * beat:.2f} ms before the bar line ; a stroke's velocity {ROLL_VEL:g} falling to {ROLL_VEL * (WAVE_HZ * STEP * beat) ** -ROLL_FALL:.3f} ({20 * math.log10((WAVE_HZ * STEP * beat) ** -ROLL_FALL):.1f} dB) ; fader {ROLL_GAIN:g} dB")
            print("      the rate at each beat: " + " ".join(f"{st[0][1] * (WAVE_HZ / st[0][1]) ** (b / ROLL_GLIDE):.1f}" for b in range(ROLL_GLIDE + 1)) + " ; in step with its own tail (strokes k turns apart) at: " + " ".join(f"k={k}: {WAVE_HZ / k:.1f} a second ({nt(WAVE_HZ / k)}), beat {ROLL_GLIDE * math.log(WAVE_HZ / k / st[0][1]) / math.log(WAVE_HZ / st[0][1]):.2f}" for k in (4, 3, 2, 1)))
            print("      " + " ; ".join(f"{way} from bar {int(t0 // BEATS) + 1} ({int(t0 * beat) // 60}:{t0 * beat % 60:04.1f}) to the line of bar {int(t0 // BEATS) + 3} ({int((t0 + 8) * beat) // 60}:{(t0 + 8) * beat % 60:04.1f})" for t0, way in roll_spans()))
        if scale_span():
            lo, hi = scale_span()
            names = {1: "G3", 2: "G4", 3: "D5", 4: "G5", 5: "B5", 6: "D6", 7: "F6-", 8: "G6", 9: "A6"}
            print(f"   the wave's own scale, bars {lo // BEATS + 1:g}-{hi // BEATS:g} ({lo * 60 / BPM:.1f}-{hi * 60 / BPM:.1f} s): the click's wave is {1000 / WAVE_HZ:.3f} ms a turn ; a stroke every {SCALE_EVERY} sixteenths, every copy at {SCALE_GAIN:g} dB in the middle ; n (copies, a n-th of a turn apart): its note, Hz, ms from copy to copy: " + " ; ".join(f"{n}: {names.get(n, '?')} {n * WAVE_HZ:.0f} {1000 / WAVE_HZ / n:.3f}" for n in SCALE_STEPS))
            print("      by beat: " + " ".join(f"{n}" for t, n in scale_strokes()) + f" ; {sum(n for t, n in scale_strokes())} clicks in {len(scale_strokes())} strokes")
        print(f"{BARS} bars, {TOTAL} beats, {BARS * sec:.1f} s; the bass: {F0} and {F0 * R:.4f} Hz")
    else:
        open(OUT, "w").write(dump(song()))
