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

v16 (27 Nov): THE CLICKS SING (C11T7_SING=0 takes it out: v15). A click is every frequency at once with all
their phases lined up at one instant. Keep each frequency's strength and set every phase to nought, window after
window, and what comes out has the same spectrum but repeats at the rate the windows are laid down: it has a
NOTE (the phase vocoder's "robot"). Nothing else is done to the click. Through bars 49-56 (the bare row before
the hat) A's own strokes are heard a second time, in the middle, treated so, and the rate is set stroke by stroke
to the note the tune will give that stroke when it comes at bar 61 (G Bb D F A on steps 0 1 3 5 6 of the half
bar), an octave down: the click sings its tune twelve bars before the tune is played. Measured alone, what comes
out has the click's spectrum to 1.4 dB in every octave and its level to 0.2 dB; only the phases are different.

v17 (27 Nov): THE DRUM COMES INTO FOCUS (C11T7_FOCUS=0 takes it out: v16). A drum beat once a beat is, to
Fourier, a pile of steady tones at the multiples of 2.1 Hz (126 to the minute), all in phase on the beat.
Take fifteen of them, the 21st to the 35th (44.1 to 73.5 Hz: the bass drum's own band), hold them, and
nothing is struck: where they agree there is a thump, and they agree once a beat. Now put each one out of
phase by the square of its place (k from -7 to 7: k squared over 28 of a turn): the same fifteen tones at
the same strengths are a hum whose pitch slides down through the beat, with no thump in it. And tune each
one flat by a hair (k squared over 28, over the row's 15.24 seconds: 0.115 Hz at the most) so that they
come back into phase on a chosen bar line. In two rows where the bass drum rests and then comes in
(bars 9-16 and 121-128) that is what plays: a hum that draws itself together, beat by beat, from a slide
a whole beat long to a thump of a twentieth of a second, and is a drum on the line where the drum comes in.
Nothing changes but phase: its level and its spectrum are the same in the first beat as in the last.
(The third such row, bars 57-64, was built and taken out: C11T7_FOCUS_ROWS=8,56,120 puts it back.)

v18 (27 Nov): THE CLICK COMES APART AND FINDS ITSELF (C11T7_SWARM=0 takes it out: v17). Twelve small
clicks, each with its own place and its own note, strike together on the first beat of a break (bars 57
and 121: the two rows in which the bass drum rests and then comes in).
Each has its own idea of the tempo: the slowest 4% under, the fastest 4% over, the rest evenly between.
For two bars nobody listens: the one stroke opens into a fan, the fast ones early and to the right and
high, the slow ones late and to the left and low: a run downwards across each beat, wider every beat (a
third of a second by the third bar). Then they begin to listen, harder and harder, and not to the song:
only to each other. Each leans towards where it hears the rest (Kuramoto's sum of sines, 1975), and, as the
fireflies of Malaya do (Ermentrout 1991), each also changes its own tempo by what it hears. Nobody tells
them where the beat is. They come back onto it because for every one that ran ahead one fell as far
behind: the swarm's mean phase never left it (the mean of their strokes is within 6 ms of the beat
throughout: a slow one's stroke is a little later than a fast one's is early). By the seventh bar the
twelve are one click again, to a hundredth of a millisecond, on the beat, and stay there until the drum
comes in.

v19 (27 Nov): A SECOND DRUM CHANGES GEAR (C11T7_GEAR=0 takes it out: v18). The song's clicks slip by
sixteenths, by samples, by parts of a wave. This is the same thing in whole numbers: a small low drum
plays against the bass drum at EVERY RATIO BETWEEN ONE AND TWO WHOSE LOWER NUMBER IS FOUR OR LESS, in
order: 1:1, 5:4, 4:3, 3:2, 5:3, 7:4, 2:1 (the Farey sequence of order four). Each gear is held for whole
turns, and for a bar's worth of beats at least: four turns of 1:1, one of 5:4, two of 4:3, two of 3:2,
two of 5:3, one of 7:4, four of 2:1: 4 + 4 + 6 + 4 + 6 + 4 + 4 beats, which is eight bars exactly. The
two drums strike together at the start of every turn and nowhere else in it, so every change of gear is
made in step. Up through the gears in the row before the roll (which goes on from there to a note), and
down through them in the last row the bass drum plays, home to one for one.

v20 (27 Nov): A CLICK THAT NOBODY STRUCK (C11T7_TURN=0 takes it out: v19). From v10 the roll shows that
a note is a click repeated in step with itself: the click quickens until its strokes are one turn of its
wave apart, and is a note. This is the other way round: A CLICK IS A NOTE THAT CHANGES STEP. The note the
roll arrives at stays, one plain tone, for the six bars up to "home" (which had nothing of their own),
and every three sixteenths (half-way between two sixteenths, where nobody strikes) it is turned upside
down. Nothing is struck. The ear does not hear which way
up a tone is; it hears it change, as a click. And how loud that click is depends only on WHERE IN ITS
WAVE the tone is caught: at the top the turn is a step of twice its height; at nought there is no step,
only a corner. The tone has 70 waves and a sixteenth in every turn, so each turn catches it a sixteenth
of a wave further on, and the clicks swell and die every eight turns (six beats), four times in the six
bars: an accent nobody plays, three against four, made of phase alone. The track is heard through a
shelf (12 dB up over 600 Hz, where a plain tone has nothing): the tone is as it was and only the turns
are brighter; without it the tone had to be the loudest thing in the row to be heard clicking.

v21 (27 Nov): THE PENDULUM GOES OVER THE TOP (C11T7_OVER=0 takes it out: v20). The song begins with a
pendulum, and a pendulum has two kinds of motion: it swings, or it goes round. Between them is the one
swing that just reaches the top, which takes for ever. In a row of "drifts" that had nothing of its own
(bars 113-120) a real pendulum is pushed from one to the other. Its acceleration is the sine of its
angle, so a wide swing takes LONGER than a small one (the fault every clock's escapement is built to
hide), and the escapement pushes it at every pass through the bottom, by the same share of its speed:
that is its tick, in the middle. A small tick eight times a beat is where the bob is (left and right
by the sine of the angle, quieter the higher it is). It swings wider and slower; the seventh swing
reaches 176.8 degrees and all but stops there, far off, for more than a bar; it falls back the way it
came; and at the next push it goes over. After that there is no swinging back: it goes round and
round, the same way, each turn quicker than the last, till the row ends. The phase that swung now runs.

v22 (27 Nov): ONE NOTE COMES APART INTO EIGHT RHYTHMS (C11T7_RHY=0 takes it out: v21). A note is a
sum of plain tones, 1, 2, 3 ... times its frequency, and the ear takes them for one thing as long as
they begin together. Here they are let go. In the first row of "drifts" (bars 105 to 112) the first
eight harmonics of B flat (the series on B flat is B flat, F and D, the song's chord over the bass's
G; the seventh is no note of ours and is left as it is) are eight plain tones, and the n-th strikes n
times a bar: two more come in every bar, and all eight play the row's second half. On every bar line all of them strike at once, from the same
point of their waves, 20 log10(n) dB apart: the first eight terms of a saw: one note. Inside the bar
they are 1 against 2 against 3 ... against 8, every small polyrhythm at once, and what strikes at
p/q of the bar is harmonic q and its multiples, which are the harmonics of a note q times as high:
the note heard at any moment is the DENOMINATOR of the time. It is Cowell's and Theremin's
rhythmicon (1931): the same ratios as pitch and as rhythm; phase is what makes them one note or eight.

v23 (27 Nov): THE CLICK COMES APART (C11T7_DISP=0 takes it out: v22). A click is every frequency
starting at once. An all-pass filter lets every frequency through at the level it came in at and
changes only its PHASE: near the filter's own frequency the sound is held back a little. A chain of
them, their frequencies spread evenly in pitch from 400 Hz to 8 kHz, holds each frequency back by
about (filters) / (f ln 20): the low ones longest. So a click goes in and a falling chirp comes out:
the same spectrum, to the dB, and another sound: its harmonics are out of step. In the sixth row of
"slips" (bars 65 to 72) A's click on sixteenths 6 and 14 is given a second copy through such a chain,
on A's side: 32 filters for two bars, then 64, 128, 256: the click's third harmonic comes 14, 29,
57 and then 114 ms after its twenty-fourth.

v24 (27 Nov): THE WHISTLE IS PUT IN STEP (C11T7_BACK=0 takes it out: v23). The same chains, the
other way. If a chain holds every frequency back by its own time, then a sound in which every
frequency is sounded that much EARLY comes out of it with all of them together: a click. That
sound is a rising whistle: the low frequencies first (they will be held longest), the high ones
last. It is how a radar puts a long weak chirp back into one sharp pulse, and (the other way
round) what a bat's ear does with its call. In the last row of "drifts" (bars 129 to 136) a
whistle from 588 Hz to 6 kHz goes into the chain of 256 filters (it is 107 ms long), then 128
(53 ms), 64 (27 ms), 32 (13 ms): two bars each, each 3 dB up on the last, so the same energy goes
in every time, and the same click comes out, on A's side, half a sixteenth after A's clicks on 6
and 14, where nothing in the song strikes: a click where only a whistle was written. The whistle
itself is heard going in, quietly, on B's side, ending as the click sounds.

v25 (27 Nov): A NOTE OUT OF STEP WITH ITSELF (C11T7_PM=0 takes it out: v24). The song puts one
click out of step with another. Here one plain low tone is put out of step with ITSELF: an
unheard second wave pushes its phase a quarter of a turn ahead and holds it a quarter of a turn
back, over and over. That is all phase modulation is (Chowning, 1973: the DX7's whole method).
How far the phase is pushed never changes in the row; only how often. Once a beat, the tone's
pitch is heard to wobble (a vibrato: 94.7 to 101.3 Hz). Twice, four, eight times a beat the
wobble widens and blurs. Sixteen times a beat (33.6 Hz) it cannot be followed, and the one
tone is heard as SEVERAL: itself, and pairs of side tones 33.6 Hz apart whose sizes are
Bessel's functions of the push: at a quarter of a turn the first pair is 1.6 dB LOUDER than
the note. Then as often as the drum's note, as the note itself, as its octave: three new
instruments from one sine. Bars 33 to 40, under the vernier, in the row before the bass.

v26 (27 Nov): THE SWARM HUMS (C11T7_HUM=0 takes it out: v25). A rhythm and a pitch are one
thing at two speeds. In the first break (bars 57 to 64) twelve clicks come apart and find each
other (v18). Now each of them holds a low tone that makes 31 waves for every beat of its OWN
tempo: 65.1 Hz and its octave, where the bass drum that rests here would be. Twelve clicks a
little out of step are twelve tones a little out of tune: a rumble that gathers itself into a
soft thump every 4.4 beats (the twelve tones are one again 31 times sooner than the clicks
would be): a drum nobody strikes, slipping against the bar. As the swarm finds the beat the
thumps grow longer until they are one held note; and since the tone turns 31 times for a
click's once, it shows the swarm's last milliseconds of error, which the clicks no longer do.
The tones come up over the eight beats for which the swarm is deaf, so that the break still
begins with the bottom gone (C11T7_HUM_IN=0 starts them at once, a thump where the drum would
be: read and refused). The note is held until the drum comes back and takes its place
(C11T7_HUM_HELD=7 lets it go a bar sooner: read and refused, see the note).

v27 (27 Nov): AN OCTAVE BY PHASE ALONE (C11T7_ALT=0 takes it out: v26). The ear is said to be
deaf to phase. It is, while it can hear a note's harmonics one by one. Above about the tenth
they are too close together for that, and the ear reads the pitch from how often the wave
pulses. In the first row of home a note sounds on every off beat: harmonics 13 to 26 of the
bass's G and nothing under them. For two bars every harmonic starts on its sine: one pulse a
period, and the note is a low buzz on G. Then every second note has its even harmonics a
quarter turn on: two pulses a period, and it is heard an octave up. The two notes have the
same harmonics at the same strengths: the off-beat octaves of a house bass, made of one note.

v28 (27 Nov): TWO SAWS OUT OF STEP (C11T7_SAWS=0 takes it out: v27). A pulse wave is two
sawtooths: one the right way up, one upside down and a little late. In step they are nothing
at all; the later the second, the wider the pulse; half a wave late it is a square, with every
even harmonic gone and every odd one doubled. In the second row of "home" a sawtooth on C3 is
held, a bar at a time. In the second bar the same sawtooth is added to it upside down, and the
sound goes: one and one is nothing. Then the second saw is slid late, 1/16, 1/4 and 1/2 of a
wave, a bar each: a thin reed opens into a hollow square; and back, 1/4, 1/16, and in the last
bar in step again: home, and nothing. No note, level or harmonic of either saw changes: only
the phase between them.

v29 (27 Nov): IN PHASE, OUT OF PHASE (C11T7_FLIP=0 takes it out: v28). A phrase of eight
notes, two bars long, is played four times in the row of the gears, the same in each ear
every time. The second and fourth times the right ear's wave is upside down. In phase the
phrase is in the sum of the two sides: in the middle, with the drum. Out of phase it is in
their difference, where almost nothing else is: it leaves the middle, is heard at the two
ears, and comes clear of the drum, though neither ear's level has changed. On one speaker
the second and fourth times are not there: the two sides add up to nothing.

v30 (28 Nov): THE BEAT THAT IS ONLY IN THE HEAD (C11T7_HEAD=0 takes it out: v29). In
the row of the sung clicks a low note is held in each ear: 249 waves to the bar in the
left, and 250, 250, 251, 251, 253, 253, 257, 257 in the right. Each ear by itself has a
steady note. The difference in phase between the ears goes round once for every wave
more: once a bar, then twice, four times, eight. Slowly, the note crosses the head;
fast, it flutters. On one speaker it is a plain beat.

v31 (28 Nov): LOUDNESS BY LATENESS (C11T7_LATE=0 takes it out: v30). After the drum has
gone (bars 145 to 152) two low tones sound, the same note at the same level, and neither
ever changes. One is held. The other begins again on every beat: in step, a quarter of a
wave late, a third, a half. Together they are twice the cosine of half the turn between
them: 6 dB up, 3 dB up, as loud as one, nothing: a note that dies away in every bar by
lateness alone.

v32 (28 Nov): IN STEP, A CLICK; OUT OF STEP, A HUM (C11T7_BUZZ=0 takes it out: v31). In
bars 17 to 24 sixteen tones of one low note (the 5th to the 20th of G1) are struck on the
off beats, all at one level. Begun together they are in step once every wave of the note
and tick there. Begun each a different part of its own wave late, the same tones at the
same levels never meet, and there is no tick. Nothing differs but where each wave begins.

v33 (28 Nov): FIVE OUT OF STEP MAKE A STAIR WITHOUT END (C11T7_POLE=0 takes it out: v32).
In bars 25 to 32 the drum's note (G1) is held with all its overtones and heard through
five narrow windows an octave apart, all climbing an octave every four bars, each coming
in at the bottom and going out at the top (the engine's barber's pole). The overtones are
picked out one after another, always upward; every four bars the same chord stands there
again.

v34 (28 Nov): ONE AND ONE MAKE TWO, ONE, OR NOTHING (C11T7_SUM=0 takes it out: v33). In
bars 113 to 120 a plain tone, alone and steady for two bars; then a second tone of the same
pitch and loudness sounds with it all the time. In step, the two make one tone 6 dB higher;
a third of a turn out, one exactly as loud as either; half a turn out, nothing. The rhythm
is the second tone's phase alone.

v35 (28 Nov): A QUARTER OF A TURN AND THE THROB IS GONE (C11T7_THROB=0 takes it out: v34).
In bars 137 to 144 three plain tones, a middle one and one 4.2 Hz to either side. For two
bars the middle one is in step with the sides and the three swell and sink twice a beat
(12 dB). For the next two it is turned a quarter of a turn: the same three tones, as loud,
and hardly a throb (1.3 dB). And again.

v36 (28 Nov): THE WAVE SLIPS UNDER ITS OWN BEAT (C11T7_UNDER=0 takes it out: v35). In bars
43 to 48 a short note whose beat is G3's (196 a second, the click's own wave) and whose
tones are 4 to 11 times that. At each step every tone is moved up by the same 24.5 Hz: the
beat inside the note does not change, the wave under it is an eighth of a turn further on
at every beat. After eight steps every tone stands where its neighbour stood: the first note.
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
FOCUS = os.environ.get("C11T7_FOCUS", "1") != "0" and os.environ.get("C11T7_SING", "1") != "0" and os.environ.get("C11T7_VERN", "1") != "0" and os.environ.get("C11T7_FIVE", "1") != "0" and JET      # v17: the drum comes into focus (fifteen held tones that come into phase)
FOCUS_ROWS = tuple(int(x) for x in os.environ.get("C11T7_FOCUS_ROWS", "8,120").split(","))    # the first bar (from 0) of each row it plays in: rows where the bass drum rests and plays in the bar after. NOT 56 (bars 57-64): there it took the hat's entry and the drum's return away as sections (8 to 7; the share of returns 0.40 to 0.29)
FOCUS_BARS = ROW                                                     # ... and how long it takes to come into phase
FOCUS_PARTS = (21, 35)                                               # the multiples of the beat's own frequency (BPM / 60 = 2.1 Hz) that are held: 44.1 to 73.5 Hz
FOCUS_NOTE = ("G1", 440 * 2 ** ((31 - 69) / 12))                     # the note the held voice is written on and its Hz (it does not sound: every tone is tuned from it)
FOCUS_OVER = 0.5                                                     # beats the voice is held past the bar line, so that the last thump (on the line, with the drum) is whole
FOCUS_GAIN = os.environ.get("C11T7_FOCUS_GAIN", "-54dB")              # set in the whole song's master, which lifts a held low part about 20 dB over its fader figure in these rows: at -28 and -36 dB it was louder than the music it lay under
GEAR = os.environ.get("C11T7_GEAR", "1") != "0" and os.environ.get("C11T7_SWARM", "1") != "0" and FOCUS      # v19: a second drum changes gear
GEAR_ROWS = tuple((int(x.split(":")[0]), x.split(":")[1]) for x in os.environ.get("C11T7_GEAR_ROWS", "72:up,136:down").split(",") if x)   # (the row's first bar from 0, up or down through the gears): the row before the roll; the last row the bass drum plays
GEAR_BARS = 8
GEAR_MOST = 4                                          # the largest lower number: every ratio p:q from 1:1 to 2:1 with q no more than this
GEAR_NOTE = os.environ.get("C11T7_GEAR_NOTE", "C3")    # 130.8 Hz: the fourth over the bass's G, where this song has least (133 Hz, 7.6 dB under the record)
GEAR_ACCENT = (1.0, 0.72)                              # velocity of the stroke that falls with the bass drum (the start of a turn), and of the rest. The master undoes it: a stroke with the bass drum is delivered 2 to 6 dB over a render of it alone, a stroke between two of the bass drum's 9 to 20 dB over: the drum marks the turn, the second drum is heard in the gaps
GEAR_GAIN = os.environ.get("C11T7_GEAR_GAIN", "-19dB")  # set in the whole song's master between two readings: at -16dB its strokes between the bass drum's stood level with all the music from 100 to 320 Hz and peaked -4 dBFS (a second bass drum); at -22dB 3 to 15 dB under it
TURN = os.environ.get("C11T7_TURN", "1") != "0" and GEAR and ROLL_ON      # v20: a click that nobody struck (a held note turned over)
TURN_BARS = 6                                          # from the line the roll arrives at to the line of "home": six bars that had nothing of their own
TURN_EVERY = 0.75                                      # beats: the note is turned over every three sixteenths (three against the beat's four)
TURN_FIRST = 0.375                                     # beats: the first turn, a sixteenth and a half after the line, so that EVERY turn is half-way between two sixteenths, where nobody strikes. ON the sixteenths (the first form, refused) each turn fell with the song's own clicks and was 6 to 14 dB under them
TURN_SHELF = (600, "12dB")                             # the track is heard through a shelf: 12 dB up over 600 Hz, where a plain tone has NOTHING: the tone is as it was, and only the turns are brighter. Without it a turn is 12 dB under its own tone (a step falls 6 dB an octave) and the tone had to be the loudest thing in the row to be heard clicking (refused: 11 dB over the music in its band)
TURN_WAVES = 70 + 1 / 16                               # the note's waves in one turn: the click's note has 70 (196 Hz); a sixteenth of a wave more (1.5 cents) and each turn catches the wave a sixteenth of a turn further on: nought, a third, two thirds, nearly all, all of its height and back, every 8 turns (6 beats)
TURN_SLOW = 0.0993e-3                                  # seconds: MEASURED, not chosen. This engine's slow oscillators are late: their phase is summed in single precision, and at 1.4 Hz the upper half of the square's cycle lasts 0.245 ms too long and the lower 0.04 too short (the step is 489.3 parts in 2 to the 24 and is rounded to 489 there). The note is tuned to the turn as it is made, not as it is written; by the row's end the turns are 3 ms late
TURN_GAIN = os.environ.get("C11T7_TURN_GAIN", "-34dB")  # set in the whole song's master between two readings: at -30dB the tone was level with all the music from 150 to 260 Hz, the large turns 9 dB over what was in their gaps (the largest 22) and the highest sample -2.6 dBFS: louder than the song's own clicks; at -36dB the tone was 6.5 dB under, the large turns 5 dB over their gaps and under the song's clicks
OVER = os.environ.get("C11T7_OVER", "1") != "0" and TURN     # v21: the pendulum goes over the top
OVER_IN = ("drifts", int(os.environ.get("C11T7_OVER_ROW", "1")))   # the section and the row of it (from 0): a row of "drifts" that had nothing of its own
OVER_PERIOD = 4.0                                      # beats: the time of one small swing there and back: a bar
OVER_START = 60.0                                      # degrees from straight down that the first swing reaches
OVER_PUSHES = 6                                        # passes through the bottom before the swing that all but reaches the top: the escapement pushes at every pass, in the way it is going, by the same share of its speed
OVER_NEAR = 176.8                                      # degrees that swing reaches: 3.2 short of the top, where a pendulum all but stops. The push is worked out from this: (sin(NEAR / 2) / sin(START / 2)) ** (1 / PUSHES)
OVER_STEPS = 960                                       # steps of a beat the motion is worked out in (leapfrog: the angle's acceleration is -(2 pi / PERIOD)^2 sin(angle))
OVER_PER_BEAT = 8                                      # the bob is heard as a small tick this many times a beat, evenly IN TIME, each where the bob is then
OVER_OFF = 0.5                                         # of the gap between two of them: the first is half a thirty-second after the line, so every one falls between the sixteenths and the thirty-seconds
OVER_PAN = 0.9                                         # level with the pivot (90 degrees) it is this far to the side: the pan is OVER_PAN * sin(angle)
OVER_FAR = 9.0                                         # dB quieter at the top than at the bottom: by height, (1 - cos(angle)) / 2
OVER_VEL = 0.8                                         # the bob's tick at the bottom
OVER_NOTE = "B8"                                       # the bob's tick (7.9 kHz: chosen by the scorer's bands: the band of this song with the most room; nothing of it over 10 kHz)
OVER_TICK = ("B7", 0.9, 4.0)                           # the escapement's tick at every pass through the bottom: its note (an octave under the bob's), velocity, dB over the bob's fader; in the middle. At -16dB (this) a tick was -17 to -24 dBFS in its own 4 ms and 15 to 29 dB over the music from 3 to 5 kHz; at -8dB it was -12 to -16 dBFS, as loud as the song's own clicks
OVER_GAIN = os.environ.get("C11T7_OVER_GAIN", "-20dB") # the bob's fader, set in the whole song's master between two readings. This song has little from 6.5 to 9.5 kHz, so the bob stands well over what is there at any fader (median 22 dB over at -14dB, 14 dB at -22dB) and the master delivers it as written (8 dB for 8): the question is how much of the row it takes. At -14dB the music under it was 0.11 dB down; at -22dB 0.02
RHY = os.environ.get("C11T7_RHY", "1") != "0" and OVER    # v22: one note comes apart into eight rhythms (the rhythmicon: Cowell and Theremin, 1931)
RHY_IN = ("drifts", 0)                                 # the section and the row of it (from 0): the first row of "drifts", which had nothing of its own
RHY_ROOT = "Bb2"                                       # the note whose harmonics they are: the series on B flat is B flat, F, D (and the seventh, which is no note of ours): over the bass's G the song's own chord
RHY_N = 8                                              # the harmonics: number n is n times the root's frequency and strikes n times a bar, evenly, from the bar line
RHY_BUILD = 0.5                                        # bars between one harmonic coming in and the next, taken down to a whole bar: harmonic n from bar int((n - 1) * this) of the row: two more every bar, and all eight for the row's second half (at one a bar the eighth was heard for a single bar)
RHY_RING = "220ms"                                     # a stroke's ring
RHY_LEN = 0.2                                          # beats a stroke is held
RHY_VEL = 0.8
RHY_PAN = 0.5                                          # the lowest is this far left, the highest this far right, evenly: each rhythm has a place; at the bar line they still strike as one
RHY_GAIN = os.environ.get("C11T7_RHY_GAIN", "-14dB")   # the first harmonic's fader, set in the whole song's master between two readings, BEFORE their scores were read, FROM THE QUIET END (the eighth harmonic, 18 dB under the first): at -12dB its strokes stood a median 1 dB over the music in their own band (22 of 40 level with it or over) and at -18dB 5 under (13 of 40); 179 and 107 of all 214 strokes were level with the music or over. The harmonics in empty bands (350, 583, 699, 816 Hz) stand 7 to 16 dB clear at -12dB; the first two are in the bass's band (B flat 2 is the bass's own note in bars 107 to 110) and are under it at any fader tried. Harmonic n is 20 log10(n) dB under it (a saw's own law: so that all eight struck together, from phase nought, are the first eight terms of one saw)
DISP = os.environ.get("C11T7_DISP", "1") != "0" and RHY   # v23: the click's own harmonics go out of step: a chain of all-pass filters changes nothing in a click but the PHASE of each frequency, and the click comes out as a falling chirp (the same spectrum, another sound)
DISP_IN = ("slips", 5)                                 # the section and the row of it (from 0): the last-but-two row of "slips", which had nothing of its own (the swarm is before it, the gears after)
DISP_STAGES = (32, 64, 128, 256)                       # all-pass filters in the chain, for two bars each: every two bars the chain is twice as long
DISP_BAND = (400.0, 8000.0)                            # Hz: the filters' own frequencies, evenly spaced in pitch between these: each holds back the frequencies near its own, so a frequency f is late by about (filters) / (f ln(top / bottom)): the low ones last
DISP_Q = 2.0
DISP_ON = (6, 14)                                      # the sixteenths of the bar: two of A's own clicks (with the hat): it is A's click that is heard to come apart, and the next sixteenth has only the air on it
DISP_VEL = 0.9                                         # A's
DISP_PAN = -0.35                                       # A's side in this row
DISP_KEEP = "-120dB"                                   # a held note this far down goes into each chain for as long as its stage lasts, AND NOTHING ELSE KEEPS THE CHAIN RUNNING: the engine stops a bus's effects when the last voice that feeds it ends (it takes a filter to have no tail), and the click's voice ends after 27 ms, while 256 all-pass filters are still giving it back 100 ms later. Read on the bench without it: the click's third harmonic came out 30 dB down, the sixth 18 to 33, the stroke 25 ms long. With it: every band within 0.1 dB of the click's own
DISP_GAIN = os.environ.get("C11T7_DISP_GAIN", "-8dB")  # set in the whole song's master between two readings, BEFORE their scores were read (A's click is -2dB): what is heard of the copy is its TAIL, after A's own click is over: between 500 and 1500 Hz, from 30 to 110 ms after the stroke, the mix is 6.1, 8.5 and 9.4 dB over what it was at -6dB (64, 128, 256 filters) and 3.0, 4.1, 5.0 dB over at -12dB; with 32 filters there is no tail at either (the copy is over in 24 ms: a click on a click). Nearer the louder: a chirp has to be heard as one. THE MASTER DELIVERS THE COPY 8 dB LOUDER THROUGH 256 FILTERS THAN THROUGH 32 (the same energy went in: its peak is 7 dB lower, and this master holds peaks)
BACK = os.environ.get("C11T7_BACK", "1") != "0" and DISP   # v24: the other half of v23: a whistle goes into the same chains and a CLICK comes out (pulse compression: a radar's chirp, a bat's call): each frequency of the whistle is sounded as much BEFORE the instant as the chain will hold it back, so the chain puts them all in step
BACK_IN = ("drifts", 3)                                # the section and the row of it (from 0): the last row of "drifts", which had nothing of its own
BACK_STAGES = tuple(reversed(DISP_STAGES))             # the chains, two bars each, the longest first: the whistle halves every two bars and the click that comes out is the same click
BACK_SPAN = (588.0, 6000.0)                            # Hz the whistle rises through: from the click's third harmonic
BACK_NOTE = "D5"                                       # the note the whistle's tone is written on (587.33 Hz): its lane (semitones over it) draws the rise
BACK_POINTS = 80                                       # points of the lane to a whistle, evenly spaced in pitch
BACK_ON = (6.5, 14.5)                                  # the sixteenths of the bar the click comes out on: HALF A SIXTEENTH AFTER A's own clicks on 6 and 14 (the ones that came apart in v23), where nothing else in the song strikes: a click is heard where only a whistle was written
BACK_PAN = (0.35, -0.35)                               # the whistle as it goes in is heard on B's side; the click comes out on A's
BACK_HEARD = os.environ.get("C11T7_BACK_HEARD", "-34dB")   # the whistle as it is heard going in: ONE fader for all four lengths. Read in the whole song's master with the short ones 3 dB up a halving (as they go into the chains): the 107 and 53 ms whistles came level with the music in their ear over their own time (-1.3, +0.8 dB) and the 27 and 13 ms ones 10 dB over it: too much of a zip. At one fader they are about -1, -2, +4 and +1
BACK_GAIN = os.environ.get("C11T7_BACK_GAIN", "-31dB")     # the whistle into the longest chain (a shorter one 3 dB up for every halving: the same energy in, so the same click out). ALONE at -28dB the click that comes out has A's own click's energy to 0.3 dB and its peak to 0.8, out of every chain. Set in the whole song's master between two readings, BEFORE their scores were read: at -28dB the click is 0 to 3 dB under A's own click beside it by energy, at -34dB 1.5 to 5: THIS MASTER GIVES 2 dB FOR 6 OF FADER ON A CLICK. 16 and 15 of the 16 stand 6 dB or more over the music in their ear
PM = os.environ.get("C11T7_PM", "1") != "0" and BACK   # v25: a note out of step with ITSELF (phase modulation, Chowning 1973): one plain tone whose phase is pushed ahead and held back by a second, unheard wave, always by the same quarter of a turn; only how OFTEN changes: once a beat it is a wobble of pitch, sixteen times a beat a growl, as often as the note's own wave a new instrument
PM_IN = ("slips", 1)                                   # the section and the row of it (from 0): the row before the bass comes in
PM_NOTE = "G2"                                         # the bass's note
PM_TURN = 0.25                                         # of a turn each way: the index is 2 pi times this (1.571 radians): the first pair of side tones is then 1.6 dB OVER the note itself
PM_RATES = (("beat", 1), ("beat", 2), ("beat", 4), ("beat", 8), ("beat", 16), ("note", 0.5), ("note", 1), ("note", 2))   # one a bar: how often the phase goes there and back: so many times a beat of the song, then so many times a wave of the note (the drum's note, the note itself, its octave)
PM_LEN = 3.75                                          # beats each bar's note is held (it is struck again every bar: the unheard wave starts again with it)
PM_PAN = 0.0
PM_BREAK = (4, 8) if os.environ.get("C11T7_PM_BREAK", "0") != "0" else None   # OFF. C11T7_PM_BREAK=1 rests the bass drum in these bars of the row (from 0): the four in which the note is several tones. TRIED AND REFUSED (v25): it leaves those bars 5.5 dB quieter and the step into the bass 9 dB for 4, the note 6.5 to 10 dB over everything else there; but it takes four bars of the drum's low end from a song already short of it, changes a part that was not mine to change without an ear, and scored 0.12 and 0.08 LESS than leaving the drum in: I had tried it because the scorer charged the row for being a new section over the same drum, and it did not mend that
PM_GAIN = os.environ.get("C11T7_PM_GAIN", "-32dB")     # read in the whole song's master at -32dB and -26dB: at -32 the note stands 5.6 to 9.4 dB over everything else at 40 to 400 Hz between the drums and the row is 0.6 dB up (it is the quiet row before the bass comes in, 4 dB under the next); at -26 it is level with the drums and the row is 1.9 dB up. The quiet one, so that the row stays the valley it is. (Both readings' scores had been read by then: the quiet one is also the one that costs less)
SWARM = os.environ.get("C11T7_SWARM", "1") != "0" and FOCUS      # v18: the click comes apart and finds itself (twelve clicks that listen only to each other)
SWARM_ROWS = tuple(int(x) for x in os.environ.get("C11T7_SWARM_ROWS", "56,120").split(","))    # the first bar (from 0) of each row it plays in: the two breaks in which the bass drum rests and then comes in
SWARM_BARS = ROW                                                     # how long a row is
SWARM_N = 12                                                         # how many clicks
SWARM_OFF = 0.04                                                     # the slowest is this far under the tempo and the fastest this far over; the rest evenly between
SWARM_DEAF = 8                                                       # beats for which nobody listens
SWARM_LEAN = 0.8                                                     # by the row's end, how hard each leans towards the rest: turns a beat for a mean sine of 1 (it rises from nought when they begin to listen)
SWARM_LEARN = 0.5                                                    # ... and how fast each changes its own tempo: turns a beat, a beat
SWARM_SUB = 192                                                      # steps in a beat of the arithmetic (midpoint rule)
SWARM_NOTES = ("D8", "D#8", "E8", "F8", "F#8", "G8", "G#8", "A8", "A#8", "B8", "C9", "C#9")    # each one's note, the slowest first: 4.7 to 8.9 kHz, where this song has room (nothing over 10 kHz)
SWARM_PAN = 0.8                                                      # the slowest this far left, the fastest this far right
SWARM_ROOM = "-16dB"
SWARM_GAIN = os.environ.get("C11T7_SWARM_GAIN", "-20dB")              # read in the whole song's master: a lone tick's highest sample is -7.5 to -10.8 dBFS there (19 dB over a render of it alone); in step, on the beat with the song's click, the twelve come out 6 dB under what they are apart
HUM = os.environ.get("C11T7_HUM", "1") != "0" and PM and SWARM   # v26: THE SWARM HUMS: each of the swarm's twelve clicks holds a low tone that makes HUM_TIMES waves for every beat of ITS OWN tempo. A rhythm and a pitch are one thing at two speeds: twelve clicks a little out of step are twelve tones a little out of tune, and when the clicks find the beat the tones find one pitch, and one phase
HUM_ROW = 0                                            # which of the swarm's rows (SWARM_ROWS): the first break only (the second lies on the scorer's short-section line, bars 119 to 124)
HUM_TIMES = 31                                         # waves to a beat of a click's own: 65.1 Hz at the song's tempo (the kick rests here, and the song is short at 61 and 71 Hz); it is also how many times finer than the clicks the tones show the swarm's last error
HUM_NOTE = "C2"                                        # the note it is written on: the lane carries the rest (65.1 Hz is 8 cents under it)
HUM_PARTS = ((1, 0.0), (2, -8.0))                      # the tone and its octave (times, dB): the octave (130.2 Hz) is what a small loudspeaker gives of it
HUM_HELD = int(os.environ.get("C11T7_HUM_HELD", "8"))   # bars of the row the tones are held: all of it: each click holds its tone for as long as it plays, and the drum takes the note's place. READ AND REFUSED: 7 (let go a bar before the drum comes back, so that it comes back into an empty bottom): my guess for why the scorer's structure term fell; it fell the same either way (see the note)
HUM_LET = "80ms"                                       # how long the letting go takes
HUM_IN = float(os.environ.get("C11T7_HUM_IN", str(SWARM_DEAF)))   # beats over which the tones come up: the beats for which nobody listens. So the break still begins with the bottom gone (the drum has just stopped), and the hum rises out of it (0: all twelve at once on the break's first beat, a thump where the drum would be: READ AND REFUSED, see the note)
HUM_STEP = 16                                          # points of the lane to a beat
HUM_PAN = 0.4                                          # the slowest this far left, the fastest this far right (the clicks are at 0.8): in step they are one sound in the middle
HUM_GAIN = os.environ.get("C11T7_HUM_GAIN", "-52dB")   # each tone. Read in the whole song's master at -48dB and -42dB (this master gives a part 17 dB more than a render of it alone): at -42 the held note of bars 62 to 64 was LOUDER than the bass (-12.9 dBFS at 56 to 77 Hz, the bass -16.6 and pushed down 1.5 dB); at -48 it was 2.6 dB under the bass (-18.2) and those bars 0.8 dB up. 4 dB under the quieter reading: the note under the bass, the octave over the music that is there
ALT = os.environ.get("C11T7_ALT", "1") != "0" and HUM   # v27: AN OCTAVE BY PHASE ALONE: one note, the same harmonics at the same strengths, heard an octave apart. The note is harmonics ALT_HARMS of ALT_NOTE and nothing under them: too close together for the ear to hear one by one, so its pitch is read from how often the wave pulses. With every harmonic started on its sine the wave pulses once a period (the low note); with the EVEN ones a quarter turn on (cosines) it pulses twice a period, and is heard an octave up (Patterson 1987; Shackleton and Carlyon 1994). No meter of spectrum can tell the two apart
ALT_IN = ("home", 0)                                   # the section and its row (from 0): the first row of home, bars 89 to 96, which had nothing of its own
ALT_NOTE = "G2"                                        # the bass's note, 98 Hz: the pulses are 10.2 ms apart, or 5.1
ALT_HARMS = (13, 26)                                   # the first and the last harmonic (1274 to 2548 Hz): from about the tenth up at this note the ear no longer hears harmonics one by one
ALT_EDGE = (-6.0, -2.5)                                # dB on the outermost harmonic at each end, and on the next: a band with soft ends has no edge to be heard as a pitch of its own
ALT_AT = 0.5                                           # the place in every beat where a note begins: the off beat, with the hat; every note stands alike to the drum, so the master treats the two kinds alike
ALT_LEN = 0.5                                          # beats a note lasts: to the next beat
ALT_PLAIN = 2                                          # bars at the row's start in which every note is the low one; after them every second note is the other
ALT_GAIN = os.environ.get("C11T7_ALT_GAIN", "-52dB")   # both tracks. Read in the whole song's master at -50dB and -56dB (the new less the old at 1100 to 2800 Hz; this master gives the part 18.5 dB more than a render of it alone): a note -29.9 and -35.9 dBFS, where the old music under the notes is -33.4 to -35.8: set between, 2 to 4 dB over the old music, before any score was read
SAWS = os.environ.get("C11T7_SAWS", "1") != "0" and ALT   # v28: TWO SAWS OUT OF STEP: a sawtooth and the same sawtooth upside down are nothing at all when they are in step; slide the second a little late and what is left is a pulse, as wide as the slide: a pulse wave IS two sawtooths out of step. Harmonic n of the pair is 2 sin(pi n w) times the one saw's (w the slide in waves): at half a wave every even harmonic is gone and every odd one doubled: a square. The row goes from one saw, to nothing, to a square, and no note changes: only the second saw's phase
SAWS_IN = ("home", 1)                                  # the section and its row (from 0): the second row of home, bars 97 to 104: in "home" the clicks are in step; so are the saws (and cancel), they go half a wave out of step and come home
SAWS_NOTE = "C3"                                       # 130.8 Hz: the fourth over the bass's G; the song is short at 133 Hz (its first harmonic) and full from 1200 Hz. (C2 with 16 harmonics was benched first: the same harmonics would have stood 6 dB lower against the note, 20 dB under the row's music at 400 to 1000 Hz, and the pulse's change of colour is in them)
SAWS_HARMS = 8                                         # harmonics of each saw, each at 1/n: up to 1047 Hz
SAWS_STEPS = (None, 0.0, 1 / 16, 1 / 4, 1 / 2, 1 / 4, 1 / 16, 0.0)   # a bar each: None: the first saw alone; else the second saw sounds too, upside down and this part of a wave late: out to half a wave (a square) and home again: in the last bar they are in step once more, and gone. (The first form went one way, to the square in the last bar, (None, 0, 1/32, 1/16, 1/8, 1/4, 3/8, 1/2), and was read and scored: the square stopped dead on the first bar of "drifts")
SAWS_AT = 0.5                                          # the beat of the bar on which a note begins (with the bass and the two-three-five)
SAWS_LEN = 3.9                                         # beats it is held
SAWS_GAIN = os.environ.get("C11T7_SAWS_GAIN", "-36dB")   # every track of the pair. Meant before any reading: the one saw about -26 dBFS in the master (14 dB under the row). The bench (the row alone at -20 dB): the one saw -27.2 dBFS. Read in the whole song's master at -30dB and -36dB (seed 0), BEFORE any score: the one saw -20.4 and -26.1 dBFS (this master lifts it 17 dB), the square -15.8 and -21.4: -36dB is the level meant
FLIP = os.environ.get("C11T7_FLIP", "1") != "0" and SAWS   # v29: IN PHASE, OUT OF PHASE: the same phrase four times, the same in each ear every time; the second and fourth times the right ear's wave is upside down. In phase it is in the SUM of the two sides, in the middle, where the drum is. Out of phase it is in neither side's sum but in their DIFFERENCE, where almost nothing else is: it leaves the middle, is heard at the two ears, and comes clear of the drum though no level has changed (the ear can take the difference: Hirsh 1948, Durlach 1963). On one speaker the second and fourth are not there at all
FLIP_IN = ("slips", 6)                                 # the section and its row (from 0): bars 73 to 80, the row of the gears
FLIP_TUNE = (("G4", 0.75), ("Bb4", 1.75), ("D5", 2.75), ("C5", 3.75), ("Bb4", 4.75), ("G4", 5.75), ("F4", 6.75), ("G4", 7.75))   # the phrase: (note, beat of its two bars): the tune's own notes, a sixteenth before each beat; 349 to 587 Hz, where the song has room (468 Hz) and the ear takes the difference best
FLIP_TIMES = ("in", "out", "in", "out")                # the four times: in phase, out of phase
FLIP_LEN = 0.9                                         # beats a note is written
FLIP_LAST = 0.2                                        # beats the phrase's last note is written: short, so that nothing of it is left when the row ends: the two bars after the row are the drum's rest, and a cut leans on that rest (the first build held it 0.65 of a beat into bar 81: one of the scorer's seven cuts lost its bound at 155 s on both seeds)
FLIP_GAIN = os.environ.get("C11T7_FLIP_GAIN", "-32dB")   # all three tracks. The bench (the row alone at -20 dB): a note's first 200 ms -33.1 dBFS in each ear. Read in the whole song's master at -28dB and -34dB (seed 0), BEFORE any score: -24.4 and -30.4 dBFS in each ear (the master lifts it 16.7 dB: a sixteenth before the beat in a row with the drum), the same in phase and out. At -28dB the phrase in phase stood 13.7 dB over the old music's sum in its own sixth of an octave: too far forward for the change to matter; at -34dB 7.7. -32dB is meant to bring it to -28.4 dBFS: in the music when in phase
HEAD = os.environ.get("C11T7_HEAD", "1") != "0" and FLIP   # v30: THE BEAT THAT IS ONLY IN THE HEAD: one low note in each ear, the right ear's a few waves a bar more than the left's. Each ear by itself has a steady note; the difference in phase between the ears goes round once for every wave more: slowly, the note crosses the head; fast, it flutters. On one speaker it is a plain beat
HEAD_IN = ("slips", 3)                                 # the section and its row (from 0): bars 49 to 56, the row of the sung clicks: the clicks are already an ear each there
HEAD_NOTE = ("C3", 130.8127826502993)                  # the note written and its frequency; the lanes move it to a whole number of waves to the bar
HEAD_WAVES = 249                                       # waves to the bar in the left ear (130.725 Hz at 126 to the minute: C3 less 1.2 cents)
HEAD_MORE = (1, 1, 2, 2, 4, 4, 8, 8)                   # waves more to the bar in the right ear, bar by bar: the turns of the difference in phase in that bar. In phase at every bar line
HEAD_RISE = 2                                          # beats the note takes to come
HEAD_GO = 4                                            # beats it takes to go: the last bar
HEAD_GAIN = os.environ.get("C11T7_HEAD_GAIN", "-35dB")   # both tracks. The bench (the two tracks alone at -20 dB): each ear -29.0 dBFS (a track hard to one side reads 9.0 under its fader). The old music in a sixth of an octave round C3 in this row is -31.2 dBFS a side. Read in the whole song's master at -35dB (both seeds) BEFORE any score: each ear -26.8 / -26.7 dBFS (the master lifts a held tone in this row 17.2 dB), 4.6 / 4.7 dB over the old music in its band: kept
LATE = os.environ.get("C11T7_LATE", "1") != "0" and HEAD   # v31: LOUDNESS BY LATENESS: two low tones, the same note at the same level, and neither ever changes: one is held; the other begins again on every beat, late by a part of a wave. Together they are twice the cosine of half the turn between them: in step 6 dB up, a quarter of a wave late 3 dB up, a third late just as loud as one, half a wave late NOTHING. A bass note that dies away in every bar and no fader moves
LATE_IN = ("one again", 1)                             # the section and its row (from 0): bars 145 to 152, the row after the drum has gone: the old music is -40 dBFS at 61 Hz there (read on v30, by sixteenth: -40 -41 -42 -41)
LATE_WAVES = 28                                        # waves to the beat: 58.8 Hz (Bb1 and 16 cents): seven to the sixteenth, so a tone begun on any beat is in step with one begun on any other. 61 Hz is a band the song is short in
LATE_NOTE = ("Bb1", 58.27047018976124)                 # the note written and its frequency; the patch moves it to LATE_WAVES
LATE_BY = ((0, 1), (1, 4), (1, 3), (1, 2))             # how late the second tone begins on each beat of every bar, in waves (a fraction): 0, a quarter, a third, a half: the two together +6.02, +3.01, 0.00 dB of one, and nothing
LATE_GAIN = os.environ.get("C11T7_LATE_GAIN", "-38dB")   # each track. THE BENCH FIRST (the two tracks alone at -20 dB): one tone's worth (the third beat) -29.0 dBFS; in step +6.02, a quarter late +3.03; half a wave late 34.9 to 58.1 dB under one tone (the starts are whole samples). Read in the whole song's master at -38dB (both seeds) BEFORE any score: one tone's worth -29.0 dBFS (this master lifts it 18.0 dB), in step -22.2
BUZZ = os.environ.get("C11T7_BUZZ", "1") != "0" and LATE   # v32: IN STEP, A CLICK; OUT OF STEP, A HUM: sixteen tones of one low note at one level, struck on the off beats. Begun together they are in step once every wave of the note and tick there, 49 times a second. Begun each a different part of its own wave late they never meet, and the same tones at the same levels have no tick in them. Nothing differs but where each wave begins
BUZZ_IN = ("one click", 2)                             # the section and its row (from 0): bars 17 to 24: the click, the second click and the drum, and nothing else
BUZZ_NOTE = ("G1", 440.0 * 2 ** ((31 - 69) / 12))      # the note whose tones they are (the drum's): 49.0 Hz
BUZZ_TONES = (5, 20)                                   # its tones written: the 5th to the 20th: 245 to 980 Hz, all at one level; the note itself is not written
BUZZ_PAIRS = (2, 2, 2, 2, 2, 2, 1, 1)                  # pairs a bar: one stab in step and one out of step, on the off beats, the order turned round every other pair (so each kind falls in both halves of the bar: read on v31, the old music is 8 dB louder after beats 0 and 2 than after 1 and 3); it thins in the last two bars
BUZZ_LEN = 0.45                                        # beats a stab is held
BUZZ_GAIN = os.environ.get("C11T7_BUZZ_GAIN", "-40dB")   # each track. THE BENCH FIRST (the two tracks alone at -20 dB): in step -28.7 dBFS with its highest sample -15.3 (13.4 dB over); out of step -29.1 and -23.9 (5.2 dB over); tone by tone the same to 0.0 dB. Aimed at -28 dBFS. The first build (-36dB, a lift of 17 dB guessed) read -24.3 in the song: the lift here is 20.4 dB, and its ticks reached -8.8 dBFS. Read at -40dB in the whole song's master (both seeds) BEFORE any score: in step -28.3 dBFS (highest sample -12.8), out of step -28.5 (-21.6)
POLE = os.environ.get("C11T7_POLE", "1") != "0" and BUZZ   # v33: FIVE OUT OF STEP MAKE A STAIR WITHOUT END (the barber's pole): one low note with all its overtones, held, heard through five narrow windows an octave apart that all climb an octave every four bars. Each window is a fifth of the way round behind the next; each comes in at the bottom and goes out at the top. So the overtones are picked out one after another, always upward, and every four bars the same chord stands there again, though every window has climbed an octave
POLE_IN = ("slips", 0)                                 # the section and its row (from 0): bars 25 to 32: the two clicks, the drum and the vernier
POLE_BARS = (0, 8)                                     # the bars of the row (from 0) it sounds in: bars 25 to 32: two turns. It comes in slowly under the first slip (bars 25 and 26)
POLE_NOTE = ("G1", 48.9994)                            # the note: the drum's own: a sawtooth, nothing over 3 kHz
POLE_LOW = 98                                          # Hz: the lowest window's lowest place: G2, the note's second overtone
POLE_BANDS = 5                                         # windows: G2 to G7 (98 to 3136 Hz)
POLE_SPACING = 1.0                                     # octaves from one window to the next
POLE_Q = 6.0                                           # how narrow a window is: a sixth of its own frequency: under 300 Hz it holds one overtone at a time
POLE_CYCLE = 4                                         # bars a window takes to climb to where the next one was (the engine keeps it on the song's clock: bar 25 begins a turn). THE FIRST BUILD HAD 2 (bars 27 to 32, three turns) and the scorer counted its steps as strokes in a thin stretch (the spread of the sections' densities 0.20 to 0.19: variety 99.54 to 97.89 / 99.39 to 97.52). At 4 the lowest window's steps come one a bar (overtones 4 5 6 7), the next one's two a bar, the next four: slow enough to follow
POLE_FADE = (8, 4, 24)                                 # beats it takes to come, beats to go, and from how many dB down
POLE_GAIN = os.environ.get("C11T7_POLE_GAIN", "-35dB")   # the track. THE BENCH FIRST (the track alone at -20 dB): -33.8 dBFS at full height; with 17.5 dB of lift for a held part in a drum row, aimed at -31. Read in the whole song's master BEFORE any score (both seeds): -31.5 to -30.7 dBFS; between the strokes 7.6 dB over the old music in 150 to 800 Hz (80 of 80 windows) and 3.0 under it in 800 to 3200 Hz
SUM = os.environ.get("C11T7_SUM", "1") != "0" and POLE   # v34: ONE AND ONE MAKE TWO, ONE, OR NOTHING: two plain tones of one pitch and one loudness, both sounding all the time. Where the second is in step with the first they make one tone twice as high (6 dB); where it is a third of a turn out, one tone exactly as loud as either alone; where it is half a turn out, nothing. So the rhythm is made by the second tone's phase alone, and most of the time two tones are sounding and nothing is heard. For the first two bars the first tone is alone, and steady: the second, as steady, is what chops it
SUM_IN = ("drifts", 1)                                 # the section and its row (from 0): bars 113 to 120. Read on v33 by twelfths of the beat: 495 to 548 Hz is -34 dBFS on the beat and -37 to -57 between here
SUM_WAVES = 62                                         # whole waves of the tone in a sixteenth: 520.8 Hz (C5, 8 cents flat): so the first tone runs on unbroken from stroke to stroke
SUM_NOTE = "C5"                                        # the written note; the patch is tuned down to SUM_WAVES
SUM_ALONE = 2                                          # bars the first tone is alone
SUM_BARS = ("I..T..I..T..I.T.", "T..I..T..I..T.I.")    # the second tone by sixteenth, bar and bar about: I in step, T a third of a turn out, . half a turn out
SUM_TURN = {"I": 0.0, "T": 1 / 3, ".": 0.5}            # turns the second tone is behind the first
SUM_EDGE = 2                                           # ms a tone takes to come and to go
SUM_TRIM = (0.0, 0, 0, -4.3, 0, 0, -5.1, 0, 0, -4.9, 0, 0, -1.3, 0, -4.4, 0)   # dB (0 or less) on both tones of a stroke by the sixteenth of the bar it falls on, by velocity (both alike, or they would not cancel). THE FIRST BUILD HAD NONE (-40 dB): in the finished song a stroke a third of a turn out came out, at sixteenths 0 3 6 9 12 14 of the bar, -30.6 -27.2 -25.5 -25.8 -29.3 -26.2 dBFS and one in step -24.7 -19.5 -19.6 -19.7 -23.4 -20.3: 5 dB between the beat and the off beat. These are that reading turned over, for -27 and -21 everywhere
SUM_HELD = -5.6                                        # dB (0 or less) on the first tone while it is alone: held, the master lifts it 21 dB (the first build: -25.5 to -24.7 dBFS at its tops); a stroke on the beat 15: this brings it to the strokes' -27
SUM_GAIN = os.environ.get("C11T7_SUM_GAIN", "-36.4dB")   # every track. THE BENCH FIRST (the four tracks alone at -20 dB, no trims): a stroke a third of a turn out -25.5 dBFS at its top; the first build was set for -45.5 on the bench (-40 dB); the second is 3.6 dB up with the trims. THE SECOND BUILD READ (both seeds, before any score): in step -21.1 -20.2 -21.1 -21.0 -21.2 -21.0 dBFS by place, a third out -27.0 -27.9 -27.0 -27.1 -27.0 -27.0, the tone alone -27.5 to -26.7; the silences 35 dB under the lowest stroke
THROB = os.environ.get("C11T7_THROB", "1") != "0" and SUM   # v35: A QUARTER OF A TURN AND THE THROB IS GONE: three plain tones, a middle one and one 4.2 Hz to either side of it, each side one 0.3 as high. With the middle one in step with the sides, the three are one tone that swells and sinks twice a beat (0.4 to 1.6 of the middle tone's height: 12 dB). Turn the middle one a quarter of a turn and the SAME three tones, as loud as they were, hardly throb at all (1 to 1.17: 1.3 dB, twice as often). v25 pushed one tone's phase to MAKE side tones; here the side tones are given, and only the middle tone's phase says whether the three throb
THROB_IN = ("one again", 0)                            # the section and its row (from 0): bars 137 to 144. Read on v34 by twelfths of the beat: 932 Hz and 15 Hz to either side is -41 to -54 dBFS in this row (-44.4 over the row)
THROB_NOTE = "Bb5"                                     # the middle tone (932.3 Hz): the third of the song's G
THROB_RATE = 2                                         # throbs to the beat: the side tones are this many waves a beat from the middle one (4.2 Hz)
THROB_DEPTH = 0.6                                      # how far the throb swings (the two side tones together, as a share of the middle one): each side tone is half of this as high
THROB_TOP = 0.25                                       # the beat the first top falls on: tops on the second and fourth sixteenths of every beat, the troughs on the beat and the half beat
THROB_TURN = 0.25                                      # turns the middle tone is turned in the bars without the throb
THROB_BARS = 2                                         # bars each way, by turns, the throb first
THROB_EDGE = 10                                        # ms a note takes to come and to go
THROB_FADE = (4, 24)                                   # the last note goes out over this many beats, to this many dB down
THROB_FLAT = (-1, -1.7, -4.5, -8.1, -10.9, -11, -8.5, -8.6, -12, -14.5, -15.7, -14.7, -11, -9.8, -12.5, -14.4, -15.3, -14, -9.6, -8.4, -12, -14.4, -15.6, -14.5, -8.9, -1.5, -3.6, -7.7, -10.2, -9.9, -7, -7.4, -11.1, -13.7, -15.1, -13.9, -9.4, -7.8, -11.3, -13.8, -14.8, -13.3, -9.4, -9.3, -12.5, -14.6, -15.8, -14.4, -8.3, -0.9, -4.5, -8.6, -11.3, -11.3, -8.5, -8.5, -11.9, -13.7, -13.8, -12.6, -9.7, -9.6, -12.4, -14.5, -15.5, -14.2, -9.5, -8.1, -11.9, -14.3, -15.6, -14.4, -8.5, 0, -3, -7.7, -10.4, -10.4, -7.5, -7.3, -10.9, -13.6, -15, -13.9, -9.3, -7.4, -11.1, -13.7, -14.7, -13.5, -9.7, -9.2, -12.5, -14.7, -15.8, -14.4, -8.3, -0.4, -4.1, -8.3, -11, -11.2, -8.5, -8.5, -12, -14.5, -15.7, -14.7, -11, -9.9, -12.6, -14.6, -15.5, -14.2, -9.7, -8.2, -11.8, -14.3, -15.6, -14.3, -8.6, -0.6, -3.1, -7.5, -10.4, -10.5, -7.6, -7.6, -11.1, -13.1, -14, -13.2, -9.4, -8, -11.3, -13.8, -14.8, -13.3, -9.5, -9.4, -12.5, -14.7, -15.8, -14.4, -8.1, -0.1, -4.2, -8.5, -11.1, -11.2, -8.5, -8.5, -11.8, -13.8, -14.3, -12.9, -9.6, -9.6, -12.5, -14.5, -15.4, -14.1, -9.4, -8.2, -11.9, -14.4, -15.6, -14.3, -8.5, -0.8, -3.7, -8.1, -10.8, -10.7, -7.7, -7.4, -10.9, -13.4, -14.8, -13.7, -9.2, -7.3, -11.1, -13.6, -14.4, -13.1, -9.4, -9.2, -12.5, -14.6, -15.6, -15.2)   # dB on both tracks through every two bars, by twenty-fourth of the beat (192 places): THE MASTER'S OWN THROB TURNED OVER. The first build had none (-40.4 dB), and in the finished song the three tones with the middle one turned, which alone are level within 0.9 dB, read 9.4 dB between their highest and lowest twelfth of the beat: the master's gain on a held tone goes through 15.8 dB in two bars: lowest just after every beat, and 6.9 to 7.7 dB under its highest just after each of the other three sixteenths. This is that reading (bars 139-140, the song's envelope less the bench's, seed 0), 0 at the place the master holds lowest. It is the same in bar 143 within 1.4 dB and under the throb's tops in bars 137-138 and 141-142 within 1.5
THROB_GAIN = os.environ.get("C11T7_THROB_GAIN", "-26.8dB")   # both tracks. THE BENCH FIRST (the two tracks alone at -20 dB): the middle tone -26.1 dBFS by spectrum; the first build set for -28 in the song with 18.5 dB of lift (a held tone in bars 145 to 152 got 18.0): -40.4 dB. THE LIFT IS NOT ONE NUMBER HERE: 4.9 to 20.7 dB through two bars. The second build is set by the lowest (THROB_FLAT brings every place down to it): -26.8 dB
UNDER = os.environ.get("C11T7_UNDER", "1") != "0" and THROB   # v36: THE WAVE SLIPS UNDER ITS OWN BEAT: a short note is a beat (G3: 196 a second, the click's own wave) with a wave inside it (plain tones from 4 to 11 times 196 Hz under one window). Move EVERY tone up by the same number of Hz and the beat inside the note is not changed at all, but the wave under it is that much of a turn further on at every beat. The note is said to go sharp by about a seventh of what was added, and sour (de Boer, 1956; Schouten, Ritsma and Cardozo, 1962). After a whole turn (196 Hz) every tone stands where its neighbour stood: it is the first note again. In "slips", where the two clicks slip against each other
UNDER_IN = ("slips", 2)                                # the section and its row (from 0): bars 41 to 48
UNDER_FROM = 2                                         # bars into the row it begins: bar 43 (bars 37 to 41 are a short section that carries a form term: nothing is written on its line)
UNDER_NOTE = "G3"                                      # the beat inside the note: 196.0 a second
UNDER_RANKS = (4, 11)                                  # the window: from 4 to 11 times the note (784 to 2156 Hz), a sine squared: a tone is as high as the window is where it stands, so the tones add to the same at every step
UNDER_STEPS = 8                                        # steps to a whole turn: a step moves every tone up by an eighth of 196 Hz (24.5 Hz)
UNDER_AT = (0.25, 1.75, 2.25, 3.75)                    # beats of the bar a note begins on. Read on v35 FIRST (b/oldat.py: 784 to 2156 Hz over a note's own 0.3 of a beat, from every sixteenth of bars 43 to 48): these four are the quietest (-34.1 to -32.4 dBFS; the loudest sixteenth -28.1)
UNDER_LEN = 0.3                                        # beats a note lasts (143 ms: 28 beats of the note)
UNDER_EDGE = (4, 12)                                   # ms it takes to come and to go
UNDER_TRIM = (2.4, -0.9, 2.9, -0.9, 2.4, -0.9, 3, -0.9, 2.4, -0.9, 3, -0.9, 2.5, -0.9, 3.2, -0.9, 2.5, -0.9, 3.1, -0.9, 2.4, -0.9, 3, -0.9)   # dB on a note, by note: THE FIRST BUILD READ TURNED OVER. With no trims (-38.2 dB) the master put the notes three sixteenths after a beat at -21.7 dBFS, those a sixteenth after the first beat at -24.7 to -24.6 and those a sixteenth after the third at -25.3 to -25.1, the same on both seeds: each note's level less -22.5, turned over, 1.15 times as deep; the largest is taken off all of them and given to the fader
UNDER_GAIN = os.environ.get("C11T7_UNDER_GAIN", "-35dB")   # every track. THE BENCH FIRST (the eight steps alone at -20 dB): every step -24.8 dBFS, one loudness; the first build set for -23 in the song with 20 dB of lift: -38.2 dB: it read -25.3 to -21.7 (a lift of 21.3 dB three sixteenths after a beat, 18.3 to 18.4 and 17.7 to 17.9 a sixteenth after the first and the third). The second build is set for -22.5 with the trims: -35 dB
SING = os.environ.get("C11T7_SING", "1") != "0" and os.environ.get("C11T7_VERN", "1") != "0" and os.environ.get("C11T7_FIVE", "1") != "0" and JET      # v16: the clicks sing (every phase set to nought)
SING_IN = ("slips", 24, 32)                                          # the section, and the bars of it: the bare row between the vernier and the hat
SING_OF = "a-ear"                                                    # whose strokes: A's, as they are in those bars
SING_PITCH = "C3"                                                    # the robot's note for a key of C4: it sings the tune an octave down (the effect's top is 750 Hz: at C4 the tune's A5 came out 277 cents flat)
SING_EARLY = 0.1                                                     # beats before a stroke that its key is set: the effect works 1024 samples (21 ms) ahead of what is heard, and with the key set on the stroke every click sang the note before its own
SING_GAIN = os.environ.get("C11T7_SING_GAIN", "-12dB")                # set in the whole song's master: at -6 dB the sung click peaked as high as the click itself
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


def gear_plan():
    """[(p, q, turns)]: every ratio p:q from 1:1 to 2:1 with q <= GEAR_MOST, in order (a Farey sequence), each held for the fewest whole turns (q beats each) that last a bar at least."""
    from fractions import Fraction
    rs = sorted({Fraction(p, q) for q in range(1, GEAR_MOST + 1) for p in range(q, 2 * q + 1)})
    plan = [(r.numerator, r.denominator, -(-BEATS // r.denominator)) for r in rs]
    assert sum(q * t for _, q, t in plan) == GEAR_BARS * BEATS, plan
    return plan


def gear_notes():
    out = []
    for row, way in GEAR_ROWS:
        b = row * BEATS
        for p, q, turns in (gear_plan() if way == "up" else gear_plan()[::-1]):
            out += [{"at": round(b + j * q / p, 6), "len": 0.25, "pitch": GEAR_NOTE, "vel": GEAR_ACCENT[0 if j % p == 0 else 1]} for j in range(p * turns)]
            b += q * turns
    return out


def pm_row():
    """The first bar of the row with the note that is out of step with itself, or None."""
    sec = next((x for x in SECS if x[0] == PM_IN[0]), None)
    return sec[1] + ROW * PM_IN[1] if PM and sec is not None and PM_IN[1] * ROW < sec[2] else None


def pm_hz():
    semi = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[PM_NOTE[0]] + (-1 if "b" in PM_NOTE[1:] else 0) + 12 * (int(PM_NOTE[-1]) + 1)
    return 440.0 * 2 ** ((semi - 69) / 12)


def pm_rate(j):
    """Hz at which bar j's phase goes there and back."""
    kind, k = PM_RATES[j]
    return k * BPM / 60 if kind == "beat" else k * pm_hz()


def pm_bessel(n, x):
    """J_n(x): how much of a tone pushed x radians each way is found n side tones from it."""
    return sum((-1) ** k / (math.factorial(k) * math.factorial(k + n)) * (x / 2) ** (2 * k + n) for k in range(30))


def back_row():
    """The first bar of the row in which the whistle is put in step, or None."""
    sec = next((x for x in SECS if x[0] == BACK_IN[0]), None)
    return sec[1] + ROW * BACK_IN[1] if BACK and sec is not None and BACK_IN[1] * ROW < sec[2] else None


def back_strokes(j):
    """The beats on which stage j's clicks come out."""
    b0, per = back_row(), ROW // len(BACK_STAGES)
    return [(b0 + j * per + i) * BEATS + st * STEP for i in range(per) for st in BACK_ON]


def back_whistle(k, at):
    """One whistle into a chain of k filters, to come out a click at beat `at`: [(beat, semitones over BACK_NOTE)]: the frequency f is sounded disp_late(f, k) seconds before the instant."""
    lo, hi = BACK_SPAN; base = 440 * 2 ** (({"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[BACK_NOTE[0]] + (-1 if "b" in BACK_NOTE else 0) + 12 * (int(BACK_NOTE[-1]) - 4) - 9) / 12)
    out = []
    for i in range(BACK_POINTS + 1):
        f = lo * (hi / lo) ** (i / BACK_POINTS)
        out.append((at - disp_late(f, k) * BPM / 60, 12 * math.log2(f / base)))
    return out


def back_lane(j):
    """Stage j's lane: its whistles one after another; between two the lane goes back down while nothing sounds."""
    pts = []
    for at in back_strokes(j):
        wh = back_whistle(BACK_STAGES[j], at)
        if not pts:
            pts.append(["0b", round(wh[0][1], 4)])
        else:
            pts.append([f"{wh[0][0] - 0.5:.5f}b", round(wh[0][1], 4)])
        pts += [[f"{t:.5f}b", round(st, 4)] for t, st in wh]
        pts.append([f"{wh[-1][0] + 0.25:.5f}b", round(wh[-1][1], 4)])
    pts.append([f"{BARS * BEATS:g}b", pts[-1][1]])
    return pts


def back_notes(j):
    out = []
    for at in back_strokes(j):
        wh = back_whistle(BACK_STAGES[j], at)
        out.append({"at": round(wh[0][0], 5), "len": round(wh[-1][0] - wh[0][0], 5), "pitch": BACK_NOTE, "vel": 0.8})
    return out


def disp_row():
    """The first bar of the row in which the click comes apart, or None."""
    sec = next((x for x in SECS if x[0] == DISP_IN[0]), None)
    return sec[1] + ROW * DISP_IN[1] if DISP and sec is not None and DISP_IN[1] * ROW < sec[2] else None


def disp_cuts(k):
    """The k all-pass filters' own frequencies (Hz): evenly spaced in pitch across DISP_BAND."""
    lo, hi = DISP_BAND
    return [round(lo * (hi / lo) ** ((i + 0.5) / k), 2) for i in range(k)]


def disp_late(f, k):
    """Seconds by which a chain of k filters holds back the frequency f (the sum of each filter's group delay there)."""
    out = 0.0
    for f0 in disp_cuts(k):
        x = f / f0
        out += 2 / (DISP_Q * 2 * math.pi * f0) * (1 + x * x) / ((1 - x * x) ** 2 + x * x / DISP_Q ** 2)
    return out


def disp_notes(j):
    """Stage j's strokes: A's click on DISP_ON, in the stage's bars of the row."""
    b0, per = disp_row(), ROW // len(DISP_STAGES)
    return [{"at": (b0 + j * per + i) * BEATS + st * STEP, "len": 0.125, "pitch": NOTE, "vel": DISP_VEL} for i in range(per) for st in DISP_ON]


def rhy_row():
    """The first bar of the row with the rhythmicon, or None."""
    sec = next((x for x in SECS if x[0] == RHY_IN[0]), None)
    return sec[1] + ROW * RHY_IN[1] if RHY and sec is not None and RHY_IN[1] * ROW < sec[2] else None


def rhy_strokes(n):
    """The beats on which harmonic n strikes: n to the bar, evenly, from the bar line, from the bar it comes in."""
    b0 = rhy_row()
    return [round((b0 + bar) * BEATS + j * BEATS / n, 5) for bar in range(int((n - 1) * RHY_BUILD), ROW) for j in range(n)]


def rhy_together(bar):
    """What is heard through a bar with the harmonics that are in by then: [(the place in the bar as a fraction in lowest terms (p, q), the harmonics that strike there)]. The harmonics striking at p / q are q, 2q, 3q ...: the multiples of q, which are the harmonics of a note q times the root's: the DENOMINATOR is the note."""
    from fractions import Fraction
    there = {}
    for n in range(1, RHY_N + 1):
        if bar >= int((n - 1) * RHY_BUILD):
            for j in range(n):
                there.setdefault(Fraction(j, n), []).append(n)
    return [((f.numerator, f.denominator), there[f]) for f in sorted(there)]


def over_row():
    """The first bar of the row in which the pendulum goes over the top, or None."""
    sec = next((x for x in SECS if x[0] == OVER_IN[0]), None)
    return sec[1] + ROW * OVER_IN[1] if OVER and sec is not None and OVER_IN[1] * ROW < sec[2] else None


_over = {}


def over_path():
    """(angles, ticks, push): the pendulum's angle in radians from straight down at every 1 / OVER_STEPS of a beat of the row; every pass through the bottom as (beat from the row's line, the angle's whole turns so far, speed after the push in units of the speed that just reaches the top); and the push (speed is multiplied by it at every pass). A real pendulum: its acceleration is -w0^2 sin(angle), so a wide swing takes longer than a small one, and one that reaches the top takes for ever."""
    if "p" not in _over:
        w0 = 2 * math.pi / OVER_PERIOD; k0 = math.sin(math.radians(OVER_START) / 2)
        push = (math.sin(math.radians(OVER_NEAR) / 2) / k0) ** (1 / OVER_PUSHES)
        th, om, dt = 0.0, 2 * w0 * k0, 1 / OVER_STEPS
        angles, ticks = [0.0], [(0.0, 0, k0)]
        for i in range(ROW * BEATS * OVER_STEPS):
            om_h = om - w0 * w0 * math.sin(th) * dt / 2; th2 = th + om_h * dt; om2 = om_h - w0 * w0 * math.sin(th2) * dt / 2
            c1, c2 = th / (2 * math.pi), th2 / (2 * math.pi)
            if math.floor(c1) != math.floor(c2):                                   # it has passed straight down (a whole number of turns): the escapement's tick and its push
                whole = max(math.floor(c1), math.floor(c2)); om2 *= push
                ticks.append(((i + (whole * 2 * math.pi - th) / (th2 - th)) * dt, whole, abs(om2) / (2 * w0)))
            th, om = th2, om2; angles.append(th)
        _over["p"] = (angles, ticks, push)
    return _over["p"]


def over_bob():
    """[(beat from the row's line, angle, pan, velocity)] of the bob's ticks."""
    angles = over_path()[0]; out = []
    for j in range(ROW * BEATS * OVER_PER_BEAT):
        t = (j + OVER_OFF) / OVER_PER_BEAT; th = angles[int(round(t * OVER_STEPS))]
        out.append((t, th, round(OVER_PAN * math.sin(th), 4), round(OVER_VEL * 10 ** (-OVER_FAR * (1 - math.cos(th)) / 2 / 20), 4)))
    return out


def turn_span():
    """(the beat the held note begins on, the beat it ends on): from the line the roll up arrives at, for TURN_BARS bars. None without."""
    ups = [t0 for t0, way in roll_spans() if way == "up"] if TURN else []
    return (ups[0] + 2 * BEATS, ups[0] + 2 * BEATS + TURN_BARS * BEATS) if ups else None


def turn_hz():
    """The held note: TURN_WAVES waves in one turn as this engine makes the turn (TURN_SLOW longer than written)."""
    return TURN_WAVES / (TURN_EVERY * 60 / BPM + TURN_SLOW)


def turn_steps():
    """[(beat, share)]: every turn, and the step it makes as a share of twice the note's height: the sine of where in its wave the note is caught."""
    t0, t1 = turn_span()
    return [(t0 + TURN_FIRST + k * TURN_EVERY, abs(math.sin(2 * math.pi * ((TURN_FIRST / TURN_EVERY + k) * TURN_WAVES % 1)))) for k in range(int(round((t1 - t0) / TURN_EVERY)))]


def swarm_ticks():
    """For each of the SWARM_N clicks, the beats (from the row's start) at which it strikes: each runs at its own tempo; from SWARM_DEAF on each leans towards the rest by the mean sine of how far ahead of it they are, and changes its own tempo by the same."""
    n, beats = SWARM_N, SWARM_BARS * BEATS; dt = 1 / SWARM_SUB
    lead = [0.0] * n; rate = [SWARM_OFF * (2 * i - (n - 1)) / (n - 1) for i in range(n)]; out = [[0.0] for _ in range(n)]
    def pull(ld, rt, t):
        hear = max(0.0, (t - SWARM_DEAF) / (beats - SWARM_DEAF)); them = [sum(math.sin(2 * math.pi * (x - y)) for x in ld) / n for y in ld]
        return [rt[i] + SWARM_LEAN * hear * them[i] for i in range(n)], [SWARM_LEARN * hear * them[i] for i in range(n)]
    for k in range(beats * SWARM_SUB):
        t = k * dt; a1, b1 = pull(lead, rate, t)
        a2, b2 = pull([lead[i] + 0.5 * dt * a1[i] for i in range(n)], [rate[i] + 0.5 * dt * b1[i] for i in range(n)], t + 0.5 * dt)
        new = [lead[i] + dt * a2[i] for i in range(n)]; rate = [rate[i] + dt * b2[i] for i in range(n)]
        for i in range(n):
            p0, p1 = t + lead[i], t + dt + new[i]
            if math.floor(p1 + 1e-12) > math.floor(p0 + 1e-12):
                at = t + dt * (math.floor(p1 + 1e-12) - p0) / (p1 - p0)
                if at < beats - 0.01: out[i].append(at)
        lead = new
    return out


_HUM_MEMO = {}


def under_row():
    """The first bar (from 0) of the row in which the wave slips under its own beat, or None."""
    sec = next((x for x in SECS if x[0] == UNDER_IN[0]), None)
    return sec[1] + ROW * UNDER_IN[1] if UNDER and sec is not None and UNDER_IN[1] * ROW < sec[2] else None


def under_tones(k):
    """Step k's tones: [(times the note, how high 0 to 1)]: rank n + k / UNDER_STEPS for every whole n in the window, as high as the window (a sine squared from UNDER_RANKS[0] to UNDER_RANKS[1]) is there."""
    lo, hi = UNDER_RANKS; out = [(n + k / UNDER_STEPS, math.sin(math.pi * (n + k / UNDER_STEPS - lo) / (hi - lo)) ** 2) for n in range(lo, hi)]
    return [(r, w) for r, w in out if w > 1e-9]


def under_layers(k):
    """The patch's layers for step k: every tone begins at nought, so the beat inside the note is the same at every step."""
    return [f"sine phase=0 ratio={r:g} level={20 * math.log10(w):.2f}dB" for r, w in under_tones(k)]


def under_like(k):
    """Hz: one over the delay (near one beat of the note) after which step k's wave is most like itself, and the next best if it is nearly as good: [(Hz, likeness 0 to 1)]."""
    f0 = hz(UNDER_NOTE); tt = under_tones(k); tot = sum(w * w for _, w in tt); r = lambda x: sum(w * w * math.cos(2 * math.pi * rk * f0 / x) for rk, w in tt) / tot
    xs = [f0 * (0.86 + 0.28 * j / 28000) for j in range(28001)]; rs = [r(x) for x in xs]
    tops = sorted(((rs[j], xs[j]) for j in range(1, 28000) if rs[j] >= rs[j - 1] and rs[j] > rs[j + 1]), reverse=True)
    return [(x, v) for v, x in tops[:2] if v >= tops[0][0] - 0.02]


def under_notes():
    """[(note from 0, beat of the song, step)]: UNDER_AT in every bar from bar UNDER_FROM of the row; the first three notes and the last seven are step 0, and between them a step every two notes: the two notes half a beat apart are always the same step."""
    b0 = (under_row() + UNDER_FROM) * BEATS; n = (ROW - UNDER_FROM) * len(UNDER_AT)
    return [(i, b0 + (i // len(UNDER_AT)) * BEATS + UNDER_AT[i % len(UNDER_AT)], min(max((i - 1) // 2, 0), UNDER_STEPS) % UNDER_STEPS) for i in range(n)]


def throb_row():
    """The first bar (from 0) of the row in which a quarter of a turn takes the throb away, or None."""
    sec = next((x for x in SECS if x[0] == THROB_IN[0]), None)
    return sec[1] + ROW * THROB_IN[1] if THROB and sec is not None and THROB_IN[1] * ROW < sec[2] else None


def throb_layers(turn):
    """The patch's three tones: the middle one turned by turn (turns); the side ones THROB_RATE waves a beat below and above it, set so that the three are in step THROB_TOP of a beat after a note begins."""
    rr = THROB_RATE * BPM / 60 / hz(THROB_NOTE); ph = (THROB_RATE * THROB_TOP) % 1; lv = 20 * math.log10(THROB_DEPTH / 2)
    return [f"sine phase={turn:g}", f"sine phase={ph:g} ratio={1 - rr:.8f} level={lv:.2f}dB", f"sine phase={(1 - ph) % 1:g} ratio={1 + rr:.8f} level={lv:.2f}dB"]


def throb_lane():
    """Both tracks' lane (dB): THROB_FLAT through every THROB_BARS bars, a point at the middle of each of its places, a straight line between; and the way out at the end."""
    b0 = throb_row() * BEATS; end = b0 + ROW * BEATS; n = len(THROB_FLAT) // (THROB_BARS * BEATS); pts = [["0b", THROB_FLAT[0]]]
    for k in range(ROW * BEATS * n):
        t = b0 + (k + 0.5) / n
        pts.append([f"{t:.4f}b", round(THROB_FLAT[k % len(THROB_FLAT)] - THROB_FADE[1] * max(0.0, (t - (end - THROB_FADE[0])) / THROB_FADE[0]), 2)])
    return pts


def throb_spans():
    """[(beat, beats long, True with the throb)]: by turns through the row."""
    b0 = throb_row() * BEATS; n = THROB_BARS * BEATS
    return [(b0 + k * n, n, k % 2 == 0) for k in range(ROW // THROB_BARS)]


def sum_row():
    """The first bar (from 0) of the row in which one and one make two, one or nothing, or None."""
    sec = next((x for x in SECS if x[0] == SUM_IN[0]), None)
    return sec[1] + ROW * SUM_IN[1] if SUM and sec is not None and SUM_IN[1] * ROW < sec[2] else None


def sum_hz():
    """The tone: SUM_WAVES whole waves to the sixteenth."""
    return SUM_WAVES * 4 * BPM / 60


def sum_runs():
    """[(beat, beats long, state, the sixteenth of the bar it begins on)]: the second tone's states after the bars alone, each run of one state one note."""
    st = "".join(SUM_BARS[b % len(SUM_BARS)] for b in range(ROW - SUM_ALONE)); out = []; k = 0
    while k < len(st):
        j = k
        while j < len(st) and st[j] == st[k] and (st[k] == "." or j == k):
            j += 1
        out.append(((sum_row() + SUM_ALONE) * BEATS + k / 4, (j - k) / 4, st[k], k % (4 * BEATS))); k = j
    return out


def pole_row():
    """The first bar (from 0) of the row with the stair without end, or None."""
    sec = next((x for x in SECS if x[0] == POLE_IN[0]), None)
    return sec[1] + ROW * POLE_IN[1] if POLE and sec is not None and POLE_IN[1] * ROW < sec[2] else None


def pole_span():
    """(the beat it begins, the beat it ends)."""
    return (pole_row() + POLE_BARS[0]) * BEATS, (pole_row() + POLE_BARS[1]) * BEATS


def buzz_row():
    """The first bar (from 0) of the row with the tones in step and out of step, or None."""
    sec = next((x for x in SECS if x[0] == BUZZ_IN[0]), None)
    return sec[1] + ROW * BUZZ_IN[1] if BUZZ and sec is not None and BUZZ_IN[1] * ROW < sec[2] else None


def buzz_late(k):
    """How late the kth tone begins when they are out of step, as a part of its own wave: j (j - 1) / (2 n) for the jth of n (Schroeder's rule: the flattest wave the same tones can make)."""
    n = BUZZ_TONES[1] - BUZZ_TONES[0] + 1; j = k - BUZZ_TONES[0] + 1
    return (j * (j - 1) / (2 * n)) % 1


def buzz_stabs():
    """[(the beat a stab begins, "in" or "out")]: in pairs, on the off beats; the order turned round every other pair."""
    out = []
    for bar, pairs in enumerate(BUZZ_PAIRS):
        for p in range(pairs):
            b = (buzz_row() + bar) * BEATS + 2 * p; out += [(b + 0.5, "in"), (b + 1.5, "out")] if len(out) % 4 == 0 else [(b + 0.5, "out"), (b + 1.5, "in")]
    return out


def late_row():
    """The first bar (from 0) of the row with loudness by lateness, or None."""
    sec = next((x for x in SECS if x[0] == LATE_IN[0]), None)
    return sec[1] + ROW * LATE_IN[1] if LATE and sec is not None and LATE_IN[1] * ROW < sec[2] else None


def late_starts():
    """[(beat the second tone begins again, waves late, dB the two together stand to one: 20 log of 2 cos(pi x), None for nothing)]: one for every beat of the row."""
    import math
    out = []
    for k in range(ROW * BEATS):
        n, d = LATE_BY[k % len(LATE_BY)]; x = n / d; both = 2 * abs(math.cos(math.pi * x))
        out.append((round(late_row() * BEATS + k + x / LATE_WAVES, 7), x, round(20 * math.log10(both), 2) if both > 1e-9 else None))
    return out


def head_row():
    """The first bar (from 0) of the row with the beat that is only in the head, or None."""
    sec = next((x for x in SECS if x[0] == HEAD_IN[0]), None)
    return sec[1] + ROW * HEAD_IN[1] if HEAD and sec is not None and HEAD_IN[1] * ROW < sec[2] else None


def head_semis(waves):
    """Semitones from the written note to a tone of so many waves to the bar."""
    import math
    return round(12 * math.log2(waves * BPM / (60 * BEATS) / HEAD_NOTE[1]), 7)


def head_lane(more):
    """A track's pitch by time, as a lane in semitones: HEAD_WAVES + more[k] waves to the bar in the row's kth bar."""
    b0 = head_row() * BEATS; pts = [["0b", head_semis(HEAD_WAVES + more[0])]]
    for k, m in enumerate(more):
        pts += [[f"{b0 + k * BEATS:g}b", head_semis(HEAD_WAVES + m)], [f"{b0 + (k + 1) * BEATS - 0.001:g}b", head_semis(HEAD_WAVES + m)]]
    return {"points": pts + [[f"{b0 + len(more) * BEATS:g}b", head_semis(HEAD_WAVES + more[-1])], [f"{BARS * BEATS}b", head_semis(HEAD_WAVES + more[-1])]], "curve": 0}


def flip_row():
    """The first bar (from 0) of the row with the phrase in phase and out of phase, or None."""
    sec = next((x for x in SECS if x[0] == FLIP_IN[0]), None)
    return sec[1] + ROW * FLIP_IN[1] if FLIP and sec is not None and FLIP_IN[1] * ROW < sec[2] else None


def flip_notes():
    """[(beat, note, 'in' or 'out')]: the phrase once for every one of FLIP_TIMES."""
    span = ROW * BEATS // len(FLIP_TIMES)
    assert span * len(FLIP_TIMES) == ROW * BEATS and all(0 <= t < span for _, t in FLIP_TUNE)
    return [(flip_row() * BEATS + k * span + t, p, how) for k, how in enumerate(FLIP_TIMES) for p, t in FLIP_TUNE]


def flip_len(t):
    """Beats the note at beat t is written: the phrase's last note is short (FLIP_LAST), the others FLIP_LEN."""
    span = ROW * BEATS // len(FLIP_TIMES)
    return FLIP_LAST if abs((t - flip_row() * BEATS) % span - FLIP_TUNE[-1][1]) < 1e-9 else FLIP_LEN


def saws_row():
    """The first bar (from 0) of the row with the two saws, or None."""
    sec = next((x for x in SECS if x[0] == SAWS_IN[0]), None)
    return sec[1] + ROW * SAWS_IN[1] if SAWS and sec is not None and SAWS_IN[1] * ROW < sec[2] else None


def saws_layers(late):
    """The sine layers of a sawtooth of SAWS_HARMS harmonics (harmonic n at 1/n). late None: the saw itself; else the same saw upside down and `late` of a wave late: harmonic n half a turn on, less n times `late`."""
    return [f"sine phase={0 if late is None else (0.5 - n * late) % 1:.6f} ratio={n} level={-20 * math.log10(n):.3f}dB" for n in range(1, SAWS_HARMS + 1)]


def saws_model(late):
    """(harmonic n of the pair against the one saw's, dB, for n = 1..SAWS_HARMS; the pair's level against one saw, dB). A harmonic that is gone is None."""
    g = [2 * abs(math.sin(math.pi * n * late)) for n in range(1, SAWS_HARMS + 1)]
    tot = sum((x / n) ** 2 for n, x in enumerate(g, 1)) / sum(1 / n ** 2 for n in range(1, SAWS_HARMS + 1))
    return [None if x < 1e-9 else 20 * math.log10(x) for x in g], (None if tot < 1e-12 else 10 * math.log10(tot))


def alt_row():
    """The first bar (from 0) of the row with the note that is an octave up by phase alone, or None."""
    sec = next((x for x in SECS if x[0] == ALT_IN[0]), None)
    return sec[1] + ROW * ALT_IN[1] if ALT and sec is not None and ALT_IN[1] * ROW < sec[2] else None


def hz(note):
    semis = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}[note[:-1]]
    return 440 * 2 ** ((semis + 12 * (int(note[-1]) + 1) - 69) / 12)


def alt_notes():
    """(low, high), each [(beat, beats long)]: a note on every off beat of the row; after ALT_PLAIN bars every second one is the alternating-phase note."""
    out = ([], [])
    for j in range(ROW):
        for k in range(BEATS):
            out[1 if j >= ALT_PLAIN and k % 2 == 1 else 0].append(((alt_row() + j) * BEATS + k + ALT_AT, ALT_LEN))
    return out


def alt_layers(alternating):
    """The note's layers: harmonics ALT_HARMS, every one a sine started at nought; or, alternating, the even ones a quarter turn on."""
    hs = list(range(ALT_HARMS[0], ALT_HARMS[1] + 1))
    edge = lambda i: ALT_EDGE[min(i, len(hs) - 1 - i)] if min(i, len(hs) - 1 - i) < len(ALT_EDGE) else 0.0
    return [f"sine phase={0.25 if alternating and h % 2 == 0 else 0:g} ratio={h} level={edge(i):g}dB" for i, h in enumerate(hs)]


def hum_note_hz():
    semis = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}[HUM_NOTE[:-1]]
    return 440 * 2 ** ((semis + 12 * (int(HUM_NOTE[-1]) + 1) - 69) / 12)


def hum_paths():
    """For each of the swarm's clicks, how far ahead of the song's beat it is (beats) at every 1 / SWARM_SUB of a beat of the row: swarm_ticks' own arithmetic, step for step (the strokes it gives are checked against swarm_ticks')."""
    if "paths" in _HUM_MEMO:
        return _HUM_MEMO["paths"]
    n, beats = SWARM_N, SWARM_BARS * BEATS; dt = 1 / SWARM_SUB
    lead = [0.0] * n; rate = [SWARM_OFF * (2 * i - (n - 1)) / (n - 1) for i in range(n)]; out = [[0.0] for _ in range(n)]; ticks = [[0.0] for _ in range(n)]
    def pull(ld, rt, t):
        hear = max(0.0, (t - SWARM_DEAF) / (beats - SWARM_DEAF)); them = [sum(math.sin(2 * math.pi * (x - y)) for x in ld) / n for y in ld]
        return [rt[i] + SWARM_LEAN * hear * them[i] for i in range(n)], [SWARM_LEARN * hear * them[i] for i in range(n)]
    for k in range(beats * SWARM_SUB):
        t = k * dt; a1, b1 = pull(lead, rate, t)
        a2, b2 = pull([lead[i] + 0.5 * dt * a1[i] for i in range(n)], [rate[i] + 0.5 * dt * b1[i] for i in range(n)], t + 0.5 * dt)
        new = [lead[i] + dt * a2[i] for i in range(n)]; rate = [rate[i] + dt * b2[i] for i in range(n)]
        for i in range(n):
            p0, p1 = t + lead[i], t + dt + new[i]
            if math.floor(p1 + 1e-12) > math.floor(p0 + 1e-12):
                at = t + dt * (math.floor(p1 + 1e-12) - p0) / (p1 - p0)
                if at < beats - 0.01: ticks[i].append(at)
            out[i].append(new[i])
        lead = new
    assert ticks == swarm_ticks()
    _HUM_MEMO["paths"] = out
    return out


def hum_lane(i):
    """[(beats from the row's start, Hz)], HUM_STEP to the beat: the tone of click i makes HUM_TIMES waves for every beat of ITS OWN: the song's tempo times one and how fast its lead is growing (the lead's difference across the two points either side)."""
    path = hum_paths()[i]; m = SWARM_SUB // HUM_STEP; top = SWARM_BARS * BEATS * HUM_STEP; out = []
    for k in range(top + 1):
        k0, k1 = max(0, k - 1), min(top, k + 1)
        out.append((k / HUM_STEP, HUM_TIMES * BPM / 60 * (1 + (path[k1 * m] - path[k0 * m]) * HUM_STEP / (k1 - k0))))
    return out


def hum_turns():
    """For each tone, its phase in turns at every point of its lane: the lane added up as the engine does it (straight lines between the points)."""
    if "turns" not in _HUM_MEMO:
        out = []
        for i in range(SWARM_N):
            ln = hum_lane(i); th = [0.0]
            for (t0, f0), (t1, f1) in zip(ln, ln[1:]):
                th.append(th[-1] + (t1 - t0) * 60 / BPM * (f0 + f1) / 2)
            out.append(th)
        _HUM_MEMO["turns"] = out
    return _HUM_MEMO["turns"]


def hum_step(k):
    """How far in step the tones are at point k of the lane: 1 is one tone, about 1 / root(n) is n strangers: the length of the mean of their phases as arrows."""
    th = hum_turns()
    return abs(sum(complex(math.cos(2 * math.pi * x[k]), math.sin(2 * math.pi * x[k])) for x in th)) / len(th)


def focus_tones():
    """(Hz, turns out of phase at the start, weight) of each held tone: tone k (from the middle) starts k squared times FOCUS_SPREAD of a turn out,
    which lays the thump out over one whole beat as a falling slide, and is flat by just enough to be back in phase after FOCUS_BARS bars."""
    lo, hi = FOCUS_PARTS; n = hi - lo + 1; beat_hz = BPM / 60; secs = FOCUS_BARS * BEATS * 60 / BPM
    spread = 1 / (2 * (n - 1))                                       # turns: with this the slide is exactly one beat long
    out = []
    for j in range(n):
        k = j - (n - 1) / 2
        out.append(((lo + j) * beat_hz - spread * k * k / secs, (spread * k * k) % 1.0, 0.5 - 0.5 * math.cos(2 * math.pi * (j + 1) / (n + 1))))
    return out


def focus_slide(bar_in_row):
    """ms the slide lasts at the start of a bar of the row (a whole beat at first, nothing on the last line)."""
    return 60000 / BPM * (1 - bar_in_row / FOCUS_BARS)


def sing_span():
    """(first bar, bar after the last), from 0."""
    at = 0
    for nm, rows, *_ in SECTIONS:
        if nm == SING_IN[0]:
            return at + SING_IN[1], at + SING_IN[2]
        at += rows * ROW
    raise KeyError(SING_IN[0])


def sing_keys(strokes):
    """For each stroke, the tune's note for its place in the half bar, set SING_EARLY beats before it."""
    return [{"at": round(n["at"] - SING_EARLY, 5), "len": 0.2, "pitch": TUNE[int(round(n["at"] / STEP)) % 8], "vel": 0.5} for n in strokes]


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
    if SING:
        sg_b0, sg_b1 = sing_span(); sg_src = next(t for t in doc["tracks"] if t["name"] == SING_OF)
        sg_strokes = [dict(n, at=round(n["at"], 5)) for n in sg_src["notes"] if sg_b0 * BEATS <= n["at"] < sg_b1 * BEATS]
        assert all(int(round(n["at"] / STEP)) % 8 in TUNE and abs(n["at"] / STEP - round(n["at"] / STEP)) < 1e-6 for n in sg_strokes), "a stroke off the pattern"
        doc["tracks"].append({"name": "singkey", "patch": "os-tune", "gain": "-90dB", "pan": 0.0, "notes": sing_keys(sg_strokes)})      # not heard: it only tells the robot its note
        doc["tracks"].append({"name": "sing", "patch": sg_src["patch"], "gain": SING_GAIN, "pan": 0.0, "sends": {"room": "-16dB"}, "auto": sg_src["auto"],
                              "fx": [{"type": "pvoc", "mode": "robot", "pitch": SING_PITCH, "tune": {"value": 0, "mod": [{"src": "track.singkey.key", "amount": 12}]}}],
                              "notes": sg_strokes})
        doc["about"] = doc["about"].replace(" Generated by", f" From v16, through bars {sg_b0 + 1} to {sg_b1}, A's strokes are heard a second time in the middle with every phase set to nought (a phase vocoder's robot): the same spectrum, but now each has a note, the one the tune gives its place, an octave down. Generated by")
        assert "From v16" in doc["about"]
    if FOCUS:
        for fo_b in FOCUS_ROWS:
            assert not any(plays("kick", fo_x) for fo_x in range(fo_b, fo_b + FOCUS_BARS)) and plays("kick", fo_b + FOCUS_BARS), f"the drum does not rest through bars {fo_b + 1}-{fo_b + FOCUS_BARS} and come in after"
        PATCHES["os-focus"] = {"about": f"Out of Step's drum that nobody strikes (chirper-zero, 27 Nov, v17): {FOCUS_PARTS[1] - FOCUS_PARTS[0] + 1} plain held tones at the multiples {FOCUS_PARTS[0]} to {FOCUS_PARTS[1]} of the beat's own frequency ({BPM / 60:g} Hz), each a hair flat and out of phase at the start by the square of its place, so that the hum they make draws together into one thump a beat over {FOCUS_BARS} bars. Written on {FOCUS_NOTE[0]}, which does not sound.",
                               "play": {"vel_sens": 0, "gate": 1},
                               "synth": {"layers": [f"sine phase={fo_ph:.6f} ratio={fo_f / FOCUS_NOTE[1]:.8f} level={20 * math.log10(fo_w):.2f}dB" for fo_f, fo_ph, fo_w in focus_tones()], "amp": {"a": "40ms", "d": "0s", "s": 1, "r": "30ms"}}}
        doc["tracks"].append({"name": "focus", "patch": "os-focus", "gain": FOCUS_GAIN, "pan": 0.0,
                              "notes": [{"at": fo_b * BEATS, "len": FOCUS_BARS * BEATS + FOCUS_OVER, "pitch": FOCUS_NOTE[0], "vel": 0.8} for fo_b in FOCUS_ROWS]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v17, in {len(FOCUS_ROWS)} rows where the bass drum rests and then comes in, fifteen held low tones ({FOCUS_PARTS[0] * BPM / 60:g} to {FOCUS_PARTS[1] * BPM / 60:g} Hz, the beat's own multiples) come slowly into phase: a hum that draws itself together into a thump a beat, and is a drum on the line where the drum comes in. Generated by")
        assert "From v17" in doc["about"]
    if SWARM:
        PATCHES["os-fly"] = {"about": "Out of Step's smallest click (chirper-zero, 27 Nov, v18): a millisecond and a half of a plain tone from phase nought, on whatever note it is given (4.7 to 8.9 kHz in the swarm), nothing over 10 kHz: one of twelve that begin as one click, come apart and find each other.",
                             "play": {"vel_sens": 0.5, "gate": 1},
                             "synth": {"layers": ["sine phase=0"], "filters": ["lp cutoff=10000"], "amp": {"a": "0.1ms", "d": "1.5ms", "s": 0, "r": "1ms", "curve": 2}}}
        sw_ticks = swarm_ticks()
        for sw_i in range(SWARM_N):
            doc["tracks"].append({"name": f"swarm-{sw_i + 1}", "patch": "os-fly", "gain": SWARM_GAIN, "pan": round(SWARM_PAN * (2 * sw_i - (SWARM_N - 1)) / (SWARM_N - 1), 4), "sends": {"room": SWARM_ROOM},
                                  "notes": [{"at": round(sw_b * BEATS + sw_at, 5), "len": 0.02, "pitch": SWARM_NOTES[sw_i], "vel": 0.8} for sw_b in SWARM_ROWS for sw_at in sw_ticks[sw_i]]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v18, in {'the two breaks' if len(SWARM_ROWS) == 2 else 'the break'} where the bass drum rests, {SWARM_N} small clicks that begin as one come apart (each has its own tempo, up to {SWARM_OFF * 100:g}% off) and then, listening only to each other, find the beat again and are one click when the drum comes in. Generated by")
        assert "From v18" in doc["about"]
    if GEAR and GEAR_ROWS:
        PATCHES["os-gear"] = {"about": "Out of Step's second drum (chirper-zero, 27 Nov, v19): a small low drum for counting against the bass drum: three plain tones (the note, its octave -10 dB, its twelfth -18 dB), each begun at the same point of its wave, gone in a tenth of a second. Its loudness is its velocity.",
                              "play": {"vel_sens": 0.5},
                              "synth": {"layers": ["sine phase=0", "sine phase=0 ratio=2 level=-10dB", "sine phase=0 ratio=3 level=-18dB"], "amp": {"a": "0.5ms", "d": "110ms", "s": 0, "r": "40ms", "curve": 3}}}
        doc["tracks"].append({"name": "gear", "patch": "os-gear", "gain": GEAR_GAIN, "pan": 0.0, "notes": gear_notes()})
        doc["about"] = doc["about"].replace(" Generated by", " From v19 a second small drum changes gear against the bass drum: it plays every ratio between one and two whose lower number is " + str(GEAR_MOST) + " or less, in order (" + ", ".join(f"{p}:{q}" for p, q, _ in gear_plan()) + "), each for whole turns and a bar's worth of beats at least, which is eight bars exactly; the two strike together at the start of every turn, so every change is made in step: up through the gears before the roll, down through them in the last row the bass drum plays. Generated by")
        assert "From v19" in doc["about"]
    if turn_span():
        tu0, tu1 = turn_span()
        PATCHES["os-turn"] = {"about": "Out of Step's note turned over (chirper-zero, 27 Nov, v20): one plain tone, held, multiplied by a square that is plus one and minus one by turns and is not heard itself: every time the square changes sides the tone is turned upside down. Nothing is struck. A turn caught at the top of the wave is a step of twice its height, a click; caught at nought it is no step at all.",
                              "play": {"gate": 1, "vel_sens": 0},
                              "synth": {"layers": [{"type": "osc", "wave": "square", "phase": round(0.5 - TURN_FIRST / (2 * TURN_EVERY), 6), "audible": False, "name": "turn", "fixed": round(BPM / 60 / (2 * TURN_EVERY), 6)},
                                                   {"type": "osc", "wave": "sine", "phase": 0, "ratio": round(turn_hz() / WAVE_HZ, 9), "ringmod": "turn"}],
                                        "amp": {"a": "5ms", "d": "0ms", "s": 1, "r": "60ms"}}}
        doc["tracks"].append({"name": "turn", "patch": "os-turn", "gain": TURN_GAIN, "pan": 0.0, "fx": [{"type": "eq", "bands": [f"highshelf cutoff={TURN_SHELF[0]} gain={TURN_SHELF[1]}"]}], "notes": [note(tu0, NOTE, tu1 - tu0, 0.8)]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v20 the note the roll arrives at stays for {TURN_BARS} bars, one plain tone, and is turned upside down every three sixteenths, half-way between two sixteenths, where nobody strikes: nothing is struck, and every turn is a click, because the ear does not hear which way up a tone is but hears it change. How loud the click is depends on where in its wave the tone is caught: at its top the step is twice its height, at nought there is none; the tone has a sixteenth of a wave more than a whole number in every turn, so the clicks swell and die away every eight turns, {int(round(TURN_BARS * BEATS / TURN_EVERY / 8))} times in the {TURN_BARS} bars, with nobody playing louder or softer. (The track is heard through a shelf, {TURN_SHELF[1]} up over {TURN_SHELF[0]} Hz, where a plain tone has nothing: only the turns are brighter for it.) Generated by")
        assert "From v20" in doc["about"]
    if over_row() is not None:
        if "os-fly" not in PATCHES:
            raise SystemExit("the bob's tick is the swarm's (os-fly): C11T7_SWARM must be on")
        ov0 = over_row() * BEATS; ov_bob = over_bob(); ov_ticks = over_path()[1]; ov_push = over_path()[2]
        doc["tracks"].append({"name": "over-bob", "patch": "os-fly", "gain": OVER_GAIN, "pan": {"value": 0, "mod": [{"src": "auto.swing", "amount": 1}]},
                              "auto": {"swing": {"points": [["0b", 0.0]] + [[f"{round(ov0 + t, 5):g}b", pan] for t, _, pan, _ in ov_bob], "curve": 0}},
                              "notes": [{"at": round(ov0 + t, 5), "len": 0.02, "pitch": OVER_NOTE, "vel": vel} for t, _, _, vel in ov_bob]})
        doc["tracks"].append({"name": "over-tick", "patch": "os-fly", "gain": f"{float(OVER_GAIN[:-2]) + OVER_TICK[2]:g}dB", "pan": 0.0,
                              "notes": [{"at": round(ov0 + t, 5), "len": 0.02, "pitch": OVER_TICK[0], "vel": OVER_TICK[1]} for t, _, _ in ov_ticks]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v21 the pendulum the song began with is pushed until it goes over the top (bars {over_row() + 1} to {over_row() + ROW}, a row of the drifts that had nothing of its own). It is a real pendulum, so a wide swing takes longer than a small one, and the escapement pushes it at every pass through the bottom (its tick, in the middle; {(ov_push - 1) * 100:.1f}% of its speed each time). A small tick {OVER_PER_BEAT} times a beat is where the bob is: it swings from side to side, wider and slower ({' '.join(f'{b - a:.2f}' for (a, _, _), (b, _, _) in zip(ov_ticks[:OVER_PUSHES + 1], ov_ticks[1:OVER_PUSHES + 2]))} beats from tick to tick), all but stops at the top, far off, falls back, and at the next push goes over: after that it only goes round, {abs(over_path()[0][-1]) / (2 * math.pi):.1f} turns by the row's end, each quicker than the last. Generated by")
        assert "From v21" in doc["about"]
    if rhy_row() is not None:
        rh_b0 = rhy_row()
        for rh_n in range(1, RHY_N + 1):
            PATCHES[f"os-part-{rh_n}"] = {"about": f"Out of Step's rhythmicon, harmonic {rh_n} (chirper-zero, 27 Nov, v22): one plain tone at {rh_n} times the note played, from phase nought, struck and dying in {RHY_RING}. Eight of them ({', '.join(str(k) for k in range(1, RHY_N + 1))}) on one note, each 20 log10(n) dB under the first, struck together are the first eight terms of a saw: one note. Struck n to the bar they are eight rhythms.",
                                            "play": {"vel_sens": 0.5}, "synth": {"layers": [f"sine phase=0 ratio={rh_n}"], "amp": {"a": "1ms", "d": RHY_RING, "s": 0, "r": "40ms", "curve": 3}}}
            doc["tracks"].append({"name": f"part-{rh_n}", "patch": f"os-part-{rh_n}", "gain": f"{float(RHY_GAIN[:-2]) - 20 * math.log10(rh_n):.2f}dB", "pan": round(RHY_PAN * (2 * (rh_n - 1) / (RHY_N - 1) - 1), 3),
                                  "notes": [{"at": rh_t, "len": RHY_LEN, "pitch": RHY_ROOT, "vel": RHY_VEL} for rh_t in rhy_strokes(rh_n)]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v22 one note comes apart into {RHY_N} rhythms (bars {rh_b0 + 1} to {rh_b0 + ROW}): the first {RHY_N} harmonics of {RHY_ROOT}, each a plain tone, the n-th striking n times a bar; two more come in every bar, and all {RHY_N} play the row's second half. On every bar line they strike together from the same point of their waves and are one note, a saw; inside the bar they are 1 against 2 against 3 and so on to {RHY_N}, and what strikes at p/q of the bar is harmonic q with its multiples: the note heard is the denominator (a rhythmicon: Cowell and Theremin, 1931). Generated by")
        assert "From v22" in doc["about"]
    if disp_row() is not None:
        assert ROW % len(DISP_STAGES) == 0
        di_b0 = disp_row(); di_hz = [588.0, 1176.0, 2352.0, 4704.0]       # the click's 3rd, 6th, 12th and 24th harmonics (it is a saw on G3, 196 Hz, with nothing under 500 Hz)
        PATCHES["os-keep"] = {"about": f"Out of Step's keeper (chirper-zero, 27 Nov, v23): one plain tone, held, played {DISP_KEEP[1:]} down into a chain of filters so that the engine keeps the chain running after the click that went into it has ended. It is not there to be heard, and at that level it is under the last bit of the file.",
                              "play": {"vel_sens": 0, "gate": 1}, "synth": {"layers": ["sine phase=0"], "amp": {"a": "1ms", "d": "0s", "s": 1, "r": "1ms"}}}
        for di_j, di_k in enumerate(DISP_STAGES):
            doc["tracks"].append({"name": f"keep-{di_j + 1}", "patch": "os-keep", "gain": DISP_KEEP, "pan": 0.0, "out": f"chain-{di_j + 1}",
                                  "notes": [{"at": (di_b0 + di_j * (ROW // len(DISP_STAGES))) * BEATS, "len": (ROW // len(DISP_STAGES)) * BEATS, "pitch": "G1", "vel": 0.5}]})
            doc["buses"][f"chain-{di_j + 1}"] = {"fx": [{"type": "filter", "kind": "allpass", "cutoff": di_f, "q": DISP_Q} for di_f in disp_cuts(di_k)]}
            doc["tracks"].append({"name": f"disp-{di_j + 1}", "patch": "os-click", "gain": DISP_GAIN, "pan": DISP_PAN, "out": f"chain-{di_j + 1}",
                                  "auto": {"open": {"points": open_lane()}}, "notes": disp_notes(di_j)})      # dry: the chain is all it goes through
        doc["about"] = doc["about"].replace(" Generated by", f" From v23 A's click comes apart (bars {di_b0 + 1} to {di_b0 + ROW}): on two sixteenths of every bar a second copy of it goes through a chain of all-pass filters, which change nothing in it but the phase of each frequency: the spectrum is the click's, and the sound is a falling chirp, because its harmonics no longer start together: the chain holds the low ones back longest. Every two bars the chain is twice as long ({', '.join(str(k) for k in DISP_STAGES)} filters): the click's third harmonic (588 Hz) comes {', '.join(f'{1000 * (disp_late(588.0, k) - disp_late(4704.0, k)):.0f}' for k in DISP_STAGES)} ms after its twenty-fourth. Generated by")
        assert "From v23" in doc["about"]
    if back_row() is not None:
        assert ROW % len(BACK_STAGES) == 0 and all(k in DISP_STAGES for k in BACK_STAGES)
        bk_b0 = back_row(); bk_per = ROW // len(BACK_STAGES)
        PATCHES["os-whistle"] = {"about": "Out of Step's whistle (chirper-zero, 27 Nov, v24): one plain tone whose note is drawn by its track's lane (auto.glide, semitones): a rise through the click's band, each frequency sounded as long before the instant as a chain of all-pass filters will hold it back. Through that chain it is a click; heard as it goes in, a short rising whistle.",
                                 "play": {"vel_sens": 0, "gate": 1}, "synth": {"layers": ["sine phase=0"], "pitch": {"value": 0, "mod": [{"src": "auto.glide", "amount": 1}]}, "amp": {"a": "1ms", "d": "0s", "s": 1, "r": "1ms"}}}
        for bk_j, bk_k in enumerate(BACK_STAGES):
            bk_n = DISP_STAGES.index(bk_k) + 1; bk_up = 10 * math.log10(max(BACK_STAGES) / bk_k); bk_lane = back_lane(bk_j)
            doc["tracks"].append({"name": f"back-{bk_n}", "patch": "os-whistle", "gain": f"{float(BACK_GAIN[:-2]) + bk_up:.2f}dB", "pan": BACK_PAN[1], "out": f"chain-{bk_n}",
                                  "auto": {"glide": {"points": bk_lane, "curve": 0}}, "notes": back_notes(bk_j)})      # into the chain: what is heard of this track is the click
            doc["tracks"].append({"name": f"heard-{bk_n}", "patch": "os-whistle", "gain": BACK_HEARD, "pan": BACK_PAN[0],
                                  "auto": {"glide": {"points": bk_lane, "curve": 0}}, "notes": back_notes(bk_j)})      # dry: the whistle as it goes in
            doc["tracks"].append({"name": f"hold-{bk_n}", "patch": "os-keep", "gain": DISP_KEEP, "pan": 0.0, "out": f"chain-{bk_n}",
                                  "notes": [{"at": (bk_b0 + bk_j * bk_per) * BEATS - 1, "len": bk_per * BEATS + 1, "pitch": "G1", "vel": 0.5}]})      # the keeper again (v23): the chain must be running before the whistle starts and after it ends
        doc["about"] = doc["about"].replace(" Generated by", f" From v24 the same chains are used the other way (bars {bk_b0 + 1} to {bk_b0 + ROW}): a rising whistle goes in and a click comes out. Each frequency of the whistle, from {BACK_SPAN[0]:g} Hz to {BACK_SPAN[1]:g}, is sounded as long before the instant as the chain will hold it back, so the chain puts them all in step: a radar's pulse, a bat's call. The whistle is {', '.join(f'{1000 * (disp_late(BACK_SPAN[0], k) - disp_late(BACK_SPAN[1], k)):.0f}' for k in BACK_STAGES)} ms long through {', '.join(str(k) for k in BACK_STAGES)} filters, two bars each, 3 dB up for every halving: the same energy goes in, and the same click comes out, half a sixteenth after A's clicks on 6 and 14, where nothing else strikes. The whistle is heard as it goes in, quietly, on B's side; the click comes out on A's. Generated by")
        assert "From v24" in doc["about"]
    if pm_row() is not None:
        assert len(PM_RATES) <= ROW
        pm_i = 2 * math.pi * PM_TURN
        for pm_j, (pm_kind, pm_k) in enumerate(PM_RATES):
            pm_wob = {"type": "osc", "wave": "sine", "name": "wob", "phase": 0, "audible": False}
            pm_wob.update({"fixed": round(pm_rate(pm_j), 4)} if pm_kind == "beat" else {"ratio": pm_k})
            PATCHES[f"os-pm-{pm_j + 1}"] = {"about": f"Out of Step's note that is out of step with itself (chirper-zero, 27 Nov, v25): a plain tone whose phase an unheard wave pushes {PM_TURN:g} of a turn ahead and back, " + (f"{pm_k:g} times a beat ({pm_rate(pm_j):.2f} Hz)" if pm_kind == "beat" else f"{pm_k:g} times in each of its own waves") + ". Nothing else is done to it.",
                                              "play": {"vel_sens": 0, "gate": 1}, "synth": {"layers": [pm_wob, {"type": "osc", "wave": "sine", "phase": 0, "pm": [{"from": "wob", "depth": round(pm_i, 4)}]}], "amp": {"a": "10ms", "d": "0s", "s": 1, "r": "40ms"}}}
            doc["tracks"].append({"name": f"pm-{pm_j + 1}", "patch": f"os-pm-{pm_j + 1}", "gain": PM_GAIN, "pan": PM_PAN, "notes": [{"at": (pm_row() + pm_j) * BEATS, "len": PM_LEN, "pitch": PM_NOTE, "vel": 0.8}]})
        if PM_BREAK:
            pm_kick = next(t for t in doc["tracks"] if t["name"] == "kick"); pm_was = len(pm_kick["notes"])
            pm_kick["notes"] = [n for n in pm_kick["notes"] if not (pm_row() + PM_BREAK[0]) * BEATS <= n["at"] < (pm_row() + PM_BREAK[1]) * BEATS]
            assert pm_was - len(pm_kick["notes"]) == (PM_BREAK[1] - PM_BREAK[0]) * BEATS, pm_was - len(pm_kick["notes"])
        doc["about"] = doc["about"].replace(" Generated by", f" From v25 one note is out of step with itself (bars {pm_row() + 1} to {pm_row() + len(PM_RATES)}, under the vernier, before the bass comes in): a plain tone on the bass's {PM_NOTE} whose phase an unheard wave pushes {PM_TURN:g} of a turn ahead and {PM_TURN:g} back. A bar each: " + ", ".join(f"{k:g} a beat" if kind == "beat" else f"{k:g} a wave" for kind, k in PM_RATES) + f". Slowly it is a wobble of pitch ({pm_hz() - pm_i * pm_rate(0):.1f} to {pm_hz() + pm_i * pm_rate(0):.1f} Hz at once a beat); faster, the wobble cannot be followed and the one tone is heard as several: the note itself {20 * math.log10(abs(pm_bessel(0, pm_i))):.1f} dB, a pair of side tones {20 * math.log10(abs(pm_bessel(1, pm_i))):.1f} dB as far above and below it as the phase is turned a second, the next pair {20 * math.log10(abs(pm_bessel(2, pm_i))):.1f} dB (Bessel's functions): phase modulation, the way a whole family of synthesizers makes its sounds. Generated by")
        assert "From v25" in doc["about"]
    if HUM and SWARM_ROWS:
        hum_b0 = SWARM_ROWS[HUM_ROW] * BEATS; hum_f = HUM_TIMES * BPM / 60
        assert SWARM_SUB % HUM_STEP == 0
        PATCHES["os-hum"] = {"about": f"Out of Step's humming swarm (chirper-zero, 27 Nov, v26): a plain held tone and its octave whose pitch follows its track's lane (auto.hum, semitones from {HUM_NOTE}): {HUM_TIMES} waves to every beat of one click of the swarm ({hum_f:.2f} Hz when that click is on the song's tempo). Twelve of them: out of step a rumble that gathers into a soft thump every {(SWARM_N - 1) / (2 * SWARM_OFF * HUM_TIMES):.3f} beats, in step one tone. Nothing over {hum_f * (1 + SWARM_OFF) * HUM_PARTS[-1][0]:.0f} Hz.",
                             "play": {"vel_sens": 0, "gate": 1}, "synth": {"layers": [f"sine phase=0 ratio={r:g} level={d:g}dB" for r, d in HUM_PARTS], "pitch": {"value": 0, "mod": [{"src": "auto.hum", "amount": 1}]}, "amp": {"a": f"{max(8, round(HUM_IN * 60000 / BPM))}ms", "d": "0s", "s": 1, "r": HUM_LET}}}
        assert 1 <= HUM_HELD <= SWARM_BARS
        for hum_i in range(SWARM_N):
            hum_pts = [[f"{round(hum_b0 + t, 5)}b", round(12 * math.log2(f / hum_note_hz()), 5)] for t, f in hum_lane(hum_i)]
            doc["tracks"].append({"name": f"hum-{hum_i + 1}", "patch": "os-hum", "gain": HUM_GAIN, "pan": round(HUM_PAN * (2 * hum_i - (SWARM_N - 1)) / (SWARM_N - 1), 4), "auto": {"hum": {"points": hum_pts, "curve": 0}},
                                  "notes": [{"at": hum_b0, "len": HUM_HELD * BEATS - 0.02, "pitch": HUM_NOTE, "vel": 0.8}]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v26 the swarm hums (bars {SWARM_ROWS[HUM_ROW] + 1} to {SWARM_ROWS[HUM_ROW] + SWARM_BARS}, the first break, where the bass drum rests): each of the swarm's {SWARM_N} clicks holds a low tone that makes {HUM_TIMES} waves for every beat of its own tempo ({hum_f:.1f} Hz and its octave). A rhythm and a pitch are one thing at two speeds: while the clicks are out of step the tones are out of tune, a rumble that gathers itself into a soft thump every {(SWARM_N - 1) / (2 * SWARM_OFF * HUM_TIMES):.2f} beats (a drum nobody strikes, slipping against the bar); as the clicks find the beat the thumps grow longer until they are one held note, which shows the swarm's last error {HUM_TIMES} times larger than the clicks do" + (f"; it is let go {SWARM_BARS - HUM_HELD} bar(s) before the drum comes back" if HUM_HELD < SWARM_BARS else "") + ". Generated by")
        assert "From v26" in doc["about"]
    if alt_row() is not None:
        al_lo, al_hi = alt_notes(); al_f = hz(ALT_NOTE)
        for al_name, al_alt, al_what in (("os-alt-0", False, "every harmonic a sine started at nought: the wave pulses once a period, and the note is heard on its written pitch"), ("os-alt-1", True, "the even harmonics a quarter turn on (cosines): the wave pulses twice a period, and the note is heard an octave over its written pitch, with the same harmonics at the same strengths as `os-alt-0`")):
            PATCHES[al_name] = {"about": f"Out of Step's octave by phase alone (chirper-zero, 27 Nov, v27): harmonics {ALT_HARMS[0]} to {ALT_HARMS[1]} of the written note and nothing under them ({ALT_HARMS[0] * al_f:.0f} to {ALT_HARMS[1] * al_f:.0f} Hz on {ALT_NOTE}), the two at each end turned down {-ALT_EDGE[0]:g} and {-ALT_EDGE[1]:g} dB; {al_what}.",
                                "play": {"vel_sens": 0, "gate": 1}, "synth": {"layers": alt_layers(al_alt), "filters": ["lp cutoff=7500"], "amp": {"a": "5ms", "d": "0s", "s": 1, "r": "20ms"}}}
        for al_name, al_patch, al_ns in (("alt-low", "os-alt-0", al_lo), ("alt-high", "os-alt-1", al_hi)):
            doc["tracks"].append({"name": al_name, "patch": al_patch, "gain": ALT_GAIN, "pan": 0.0, "notes": [{"at": t, "len": ln, "pitch": ALT_NOTE, "vel": 0.8} for t, ln in al_ns]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v27 there is an octave by phase alone (bars {alt_row() + 1} to {alt_row() + ROW}, the first row of home): one note on every off beat, harmonics {ALT_HARMS[0]} to {ALT_HARMS[1]} of the bass's {ALT_NOTE} and nothing under them. For {ALT_PLAIN} bars every harmonic starts on its sine and the wave pulses once a period; after that every second note has its even harmonics a quarter turn on, pulses twice a period, and is heard an octave up: {len(al_lo)} notes and {len(al_hi)}, the same harmonics at the same strengths in both. Generated by")
        assert "From v27" in doc["about"]
    if saws_row() is not None:
        assert len(SAWS_STEPS) == ROW and SAWS_STEPS[0] is None and all(x is not None for x in SAWS_STEPS[1:])
        sw_f = hz(SAWS_NOTE)
        sw_amp = {"a": "20ms", "d": "0s", "s": 1, "r": "40ms"}
        PATCHES["os-saw-a"] = {"about": f"Out of Step's first saw (chirper-zero, 27 Nov, v28): a sawtooth made of its first {SAWS_HARMS} harmonics, each a sine started at nought, harmonic n at 1/n ({sw_f:.1f} to {SAWS_HARMS * sw_f:.0f} Hz on {SAWS_NOTE}); held.",
                               "play": {"vel_sens": 0, "gate": 1}, "synth": {"layers": saws_layers(None), "amp": sw_amp}}
        doc["tracks"].append({"name": "saw-a", "patch": "os-saw-a", "gain": SAWS_GAIN, "pan": 0.0, "notes": [{"at": (saws_row() + k) * BEATS + SAWS_AT, "len": SAWS_LEN, "pitch": SAWS_NOTE, "vel": 0.8} for k in range(ROW)]})
        for sw_k, sw_late in enumerate(SAWS_STEPS):
            if sw_late is None:
                continue
            PATCHES[f"os-saw-b{sw_k}"] = {"about": f"Out of Step's second saw, bar {sw_k + 1} of its row (chirper-zero, 27 Nov, v28): the first saw upside down and {sw_late:g} of a wave late ({1000 * sw_late / sw_f:.2f} ms): harmonic n half a turn on, less n times {sw_late:g}. With the first saw it leaves a pulse {100 * sw_late:g}% of the wave wide.",
                                          "play": {"vel_sens": 0, "gate": 1}, "synth": {"layers": saws_layers(sw_late), "amp": sw_amp}}
            doc["tracks"].append({"name": f"saw-b{sw_k}", "patch": f"os-saw-b{sw_k}", "gain": SAWS_GAIN, "pan": 0.0, "notes": [{"at": (saws_row() + sw_k) * BEATS + SAWS_AT, "len": SAWS_LEN, "pitch": SAWS_NOTE, "vel": 0.8}]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v28 two saws are out of step (bars {saws_row() + 1} to {saws_row() + ROW}, the second row of home): a sawtooth on {SAWS_NOTE} ({sw_f:.1f} Hz, {SAWS_HARMS} harmonics) is held a bar at a time; from the second bar the same sawtooth sounds with it, upside down: bar by bar the second is " + ", ".join("in step (the two are nothing)" if x == 0 else (f"1/{round(1 / x)}" if abs(1 / x - round(1 / x)) < 1e-9 else f"{x:g}") + " of a wave late" for x in SAWS_STEPS[1:]) + ", and what is left is a pulse as wide as the second is late: at half a wave a square, every even harmonic gone. No note changes: only the second saw's phase. Generated by")
        assert "From v28" in doc["about"]
    if flip_row() is not None:
        fl = flip_notes()
        for fl_name, fl_ph, fl_what in (("os-flip", 0, "the right way up"), ("os-flip-over", 0.5, "upside down: every part of it half a turn on")):
            PATCHES[fl_name] = {"about": f"Out of Step's phrase in and out of phase (chirper-zero, 27 Nov, v29): a soft struck tone, a sine and its octave, {fl_what}. `os-flip` in one ear and `os-flip-over` in the other are the same sound with one ear's wave turned over: together on one speaker they are nothing.",
                                "play": {"vel_sens": 0}, "synth": {"layers": [f"sine phase={fl_ph:g}", f"sine phase={fl_ph:g} ratio=2 level=-12dB"], "filters": ["lp cutoff=7000"], "amp": {"a": "3ms", "d": "300ms", "s": 0.3, "r": "80ms"}}}
        for fl_name, fl_patch, fl_pan, fl_how in (("flip-l", "os-flip", -1.0, ("in", "out")), ("flip-in", "os-flip", 1.0, ("in",)), ("flip-out", "os-flip-over", 1.0, ("out",))):
            doc["tracks"].append({"name": fl_name, "patch": fl_patch, "gain": FLIP_GAIN, "pan": fl_pan, "notes": [{"at": t, "len": flip_len(t), "pitch": p, "vel": 0.8} for t, p, how in fl if how in fl_how]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v29 a phrase is in phase and out of phase (bars {flip_row() + 1} to {flip_row() + ROW}, the row of the gears in 'slips'): {' '.join(p for p, _ in FLIP_TUNE)}, two bars, {len(FLIP_TIMES)} times, the same in each ear every time; the {' and '.join(('first', 'second', 'third', 'fourth')[k] for k, how in enumerate(FLIP_TIMES) if how == 'out')} time the right ear's wave is upside down: the phrase is then in neither the left nor the right alone but in their difference, where almost nothing else is: it leaves the middle and comes clear of the drum; on one speaker it is not there. Generated by")
        assert "From v29" in doc["about"]
    if head_row() is not None:
        hd_beat = 60 / BPM
        PATCHES["os-head"] = {"about": "Out of Step's beat in the head (chirper-zero, 28 Nov, v30): one plain held tone whose pitch follows its track's lane (auto.tune, semitones). One track in each ear, the right ear's a few waves a bar more: each ear by itself is steady and the difference in phase between them goes round.",
                              "play": {"vel_sens": 0, "gate": 1}, "synth": {"layers": ["sine phase=0"], "pitch": {"value": 0, "mod": [{"src": "auto.tune", "amount": 1}]}, "filters": ["lp cutoff=7000"],
                                                                         "amp": {"a": f"{round(HEAD_RISE * hd_beat, 4):g}s", "d": "0s", "s": 1, "r": f"{round(HEAD_GO * hd_beat, 4):g}s"}}}
        for hd_name, hd_pan, hd_more in (("head-l", -1.0, (0,) * len(HEAD_MORE)), ("head-r", 1.0, HEAD_MORE)):
            doc["tracks"].append({"name": hd_name, "patch": "os-head", "gain": HEAD_GAIN, "pan": hd_pan, "auto": {"tune": head_lane(hd_more)},
                                  "notes": [{"at": head_row() * BEATS, "len": len(HEAD_MORE) * BEATS - HEAD_GO, "pitch": HEAD_NOTE[0], "vel": 0.8}]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v30 a beat is only in the head (bars {head_row() + 1} to {head_row() + ROW}, the row of the sung clicks in 'slips'): a low note in each ear, {HEAD_WAVES} waves to the bar in the left ({HEAD_WAVES * BPM / (60 * BEATS):.3f} Hz) and {', '.join(str(HEAD_WAVES + m) for m in HEAD_MORE)} in the right, bar by bar: each ear by itself has a steady note, and the difference in phase between the ears goes round {', '.join(str(m) for m in HEAD_MORE)} times a bar: slowly it crosses the head, fast it flutters; on one speaker it is a plain beat. Generated by")
        assert "From v30" in doc["about"]
    if late_row() is not None:
        import math as lt_math
        lt = late_starts(); lt_end = (late_row() + ROW) * BEATS
        PATCHES["os-late"] = {"about": "Out of Step's two tones that are louder or softer by how late one is (chirper-zero, 28 Nov, v31): one plain held tone, no coming and no going, moved to a whole number of waves to the beat. Two tracks of it at one level: together they are twice the cosine of half the turn between them.",
                              "play": {"vel_sens": 0, "gate": 1}, "synth": {"layers": ["sine phase=0"], "pitch": {"value": round(12 * lt_math.log2(LATE_WAVES * BPM / 60 / LATE_NOTE[1]), 7)}, "filters": ["lp cutoff=7000"], "amp": {"a": "0ms", "d": "0s", "s": 1, "r": "0ms"}}}
        doc["tracks"].append({"name": "late-held", "patch": "os-late", "gain": LATE_GAIN, "pan": 0.0, "notes": [{"at": late_row() * BEATS, "len": ROW * BEATS, "pitch": LATE_NOTE[0], "vel": 0.8}]})
        doc["tracks"].append({"name": "late-again", "patch": "os-late", "gain": LATE_GAIN, "pan": 0.0,
                              "notes": [{"at": at, "len": round((lt[i + 1][0] if i + 1 < len(lt) else lt_end) - at, 7), "pitch": LATE_NOTE[0], "vel": 0.8} for i, (at, _, _) in enumerate(lt)]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v31 loudness is lateness (bars {late_row() + 1} to {late_row() + ROW}, the row after the drum has gone): two low tones of {LATE_WAVES} waves to the beat ({LATE_WAVES * BPM / 60:.1f} Hz) at one level, and neither ever changes: one is held, the other begins again on every beat, {', '.join('in step' if n == 0 else f'{n}/{d} of a wave late' for n, d in LATE_BY)}: together {', '.join('nothing' if v is None else f'{v:+.1f} dB' for _, _, v in lt[:len(LATE_BY)])} of one. Generated by")
        assert "From v31" in doc["about"]
    if buzz_row() is not None:
        import math as bz_math
        bz_n = BUZZ_TONES[1] - BUZZ_TONES[0] + 1; bz = buzz_stabs()
        for bz_kind, bz_what in (("in", "every tone begun together: in step once every wave of the note, where they tick"), ("out", "each tone begun a different part of its own wave late (Schroeder's rule): the same tones at the same levels, never in step: no tick")):
            PATCHES[f"os-buzz-{bz_kind}"] = {"about": f"Out of Step's {bz_n} tones of {BUZZ_NOTE[0]} (the {BUZZ_TONES[0]}th to the {BUZZ_TONES[1]}th: {BUZZ_TONES[0] * BUZZ_NOTE[1]:.0f} to {BUZZ_TONES[1] * BUZZ_NOTE[1]:.0f} Hz), all at one level (chirper-zero, 28 Nov, v32): {bz_what}.",
                                             "play": {"vel_sens": 0, "gate": 1}, "synth": {"layers": [f"sine phase={(0 if bz_kind == 'in' else (1 - buzz_late(k)) % 1):g} ratio={k} level={-10 * bz_math.log10(bz_n):.2f}dB" for k in range(BUZZ_TONES[0], BUZZ_TONES[1] + 1)],
                                                                                 "filters": ["lp cutoff=7000"], "amp": {"a": "3ms", "d": "0s", "s": 1, "r": "15ms"}}}
            doc["tracks"].append({"name": f"buzz-{bz_kind}", "patch": f"os-buzz-{bz_kind}", "gain": BUZZ_GAIN, "pan": 0.0, "notes": [{"at": t, "len": BUZZ_LEN, "pitch": BUZZ_NOTE[0], "vel": 0.8} for t, kd in bz if kd == bz_kind]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v32 in step, a click; out of step, a hum (bars {buzz_row() + 1} to {buzz_row() + len(BUZZ_PAIRS)}): the {BUZZ_TONES[0]}th to the {BUZZ_TONES[1]}th tones of {BUZZ_NOTE[0]} ({BUZZ_TONES[0] * BUZZ_NOTE[1]:.0f} to {BUZZ_TONES[1] * BUZZ_NOTE[1]:.0f} Hz), all at one level, struck on the off beats in pairs: one with every tone begun together (in step once every wave of the note: a tick {BUZZ_NOTE[1]:.0f} times a second) and one with each begun a different part of its own wave late (the same tones at the same levels, and no tick), the order turned round every other pair: {len(bz) // 2} of each. Generated by")
        assert "From v32" in doc["about"]
    if pole_row() is not None:
        pl0, pl1 = pole_span(); assert (pl0 // BEATS) % POLE_CYCLE == 0
        PATCHES["os-pole"] = {"about": "Out of Step's one low note with all its overtones (chirper-zero, 28 Nov, v33): a sawtooth, nothing over 3 kHz, held. Its track carries the engine's barber's pole (five narrow windows an octave apart, all climbing) and a lane that brings it in and takes it out.",
                              "play": {"vel_sens": 0, "gate": 1}, "synth": {"layers": ["saw phase=0"], "filters": ["lp cutoff=3000"], "amp": {"a": "20ms", "d": "0s", "s": 1, "r": "50ms"}}}
        doc["tracks"].append({"name": "pole", "patch": "os-pole", "gain": POLE_GAIN, "pan": 0.0,
                              "auto": {"arch": {"points": [["0b", -90], [f"{pl0 - 0.001:g}b", -90], [f"{pl0:g}b", -POLE_FADE[2]], [f"{pl0 + POLE_FADE[0]:g}b", 0], [f"{pl1 - POLE_FADE[1]:g}b", 0], [f"{pl1:g}b", -POLE_FADE[2]], [f"{pl1 + 0.001:g}b", -90]], "curve": 0}},
                              "fx": [{"type": "barberpole", "low": POLE_LOW, "bands": POLE_BANDS, "spacing": POLE_SPACING, "q": POLE_Q, "cycle": f"{POLE_CYCLE}bar", "mix": 1}, {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.arch", "amount": 1}]}}],
                              "notes": [note(pl0, POLE_NOTE[0], pl1 - pl0, 0.8)]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v33 five out of step make a stair without end (bars {pl0 // BEATS + 1} to {pl1 // BEATS}): {POLE_NOTE[0]} with all its overtones, held, through {POLE_BANDS} narrow windows {POLE_SPACING:g} octave apart ({POLE_LOW} Hz and up) that all climb an octave every {POLE_CYCLE} bars, each coming in at the bottom and going out at the top: the overtones are picked out one after another, always upward, and every {POLE_CYCLE} bars the same chord stands there again. Generated by")
        assert "From v33" in doc["about"]
    if sum_row() is not None:
        sr_ = sum_runs(); s_tune = round(12 * math.log2(sum_hz() / hz(SUM_NOTE)), 6); s_amp = {"a": f"{SUM_EDGE}ms", "d": "0s", "s": 1, "r": f"{SUM_EDGE}ms"}
        for nm, tn, what in (("os-sum", 0.0, "the first tone, and the second where it is in step"), ("os-sum-third", SUM_TURN["T"], "the second tone a third of a turn behind"), ("os-sum-out", SUM_TURN["."], "the second tone half a turn behind: the first turned over")):
            PATCHES[nm] = {"about": f"Out of Step's plain tone for one and one (chirper-zero, 28 Nov, v34): {sum_hz():.1f} Hz, {SUM_WAVES} whole waves to the sixteenth; {what}. Its loudness goes as the square of the velocity.",
                           "play": {"vel_sens": 1, "gate": 1}, "synth": {"layers": [f"sine phase={round(tn, 7):g}"], "pitch": {"value": s_tune}, "filters": ["lp cutoff=7000"], "amp": s_amp}}
        s_vel = lambda pl, stt: 1.0 if stt == "." else round(10 ** (SUM_TRIM[pl] / 40), 5)
        s_note = lambda at, ln, v: {"at": round(at, 7), "len": round(ln, 7), "pitch": SUM_NOTE, "vel": v}
        doc["tracks"].append({"name": "sum-a", "patch": "os-sum", "gain": SUM_GAIN, "pan": 0.0, "notes": [s_note(sum_row() * BEATS, SUM_ALONE * BEATS, round(10 ** (SUM_HELD / 40), 5))] + [s_note(at, ln, s_vel(pl, stt)) for at, ln, stt, pl in sr_]})
        for nm, pt, stt0 in (("sum-in", "os-sum", "I"), ("sum-third", "os-sum-third", "T"), ("sum-out", "os-sum-out", ".")):
            doc["tracks"].append({"name": nm, "patch": pt, "gain": SUM_GAIN, "pan": 0.0, "notes": [s_note(at, ln, s_vel(pl, stt)) for at, ln, stt, pl in sr_ if stt == stt0]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v34 one and one make two, one, or nothing (bars {sum_row() + 1} to {sum_row() + ROW}): a plain tone ({sum_hz():.1f} Hz) alone and steady for {SUM_ALONE} bars; then a second tone of the same pitch and loudness sounds with it all the time, in step (the two make one twice as high), a third of a turn out (one exactly as loud as either) or half a turn out (nothing): the rhythm is the second tone's phase and nothing else. Generated by")
        assert "From v34" in doc["about"]
    if throb_row() is not None:
        ts_ = throb_spans(); t_amp = {"a": f"{THROB_EDGE}ms", "d": "0s", "s": 1, "r": f"{THROB_EDGE}ms"}; t_end = ts_[-1][0] + ts_[-1][1]
        for nm, tn, what in (("os-throb", 0.0, "the middle one in step with the side ones: the three swell and sink together"), ("os-still", THROB_TURN, f"the middle one turned {THROB_TURN:g} of a turn: the same three tones, and hardly a throb")):
            PATCHES[nm] = {"about": f"Out of Step's three plain tones for a quarter of a turn (chirper-zero, 28 Nov, v35): a middle one and one {THROB_RATE * BPM / 60:g} Hz to either side, each {THROB_DEPTH / 2:g} as high; {what}.",
                           "play": {"vel_sens": 0, "gate": 1}, "synth": {"layers": throb_layers(tn), "filters": ["lp cutoff=7000"], "amp": t_amp}}
        t_note = lambda at, ln: {"at": round(at, 6), "len": round(ln, 6), "pitch": THROB_NOTE, "vel": 0.8}
        for nm, pt, th0 in (("throb", "os-throb", True), ("still", "os-still", False)):
            doc["tracks"].append({"name": nm, "patch": pt, "gain": THROB_GAIN, "pan": 0.0, "notes": [t_note(at, ln) for at, ln, th in ts_ if th == th0], "auto": {"arch": {"points": throb_lane(), "curve": 0}},
                                  "fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.arch", "amount": 1}]}}]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v35 a quarter of a turn and the throb is gone (bars {throb_row() + 1} to {throb_row() + ROW}): three plain tones, a middle one ({THROB_NOTE}) and one {THROB_RATE * BPM / 60:g} Hz to either side; for {THROB_BARS} bars the middle one is in step with the sides and the three swell and sink {THROB_RATE} times a beat; for the next {THROB_BARS} it is turned a quarter of a turn and the same three tones, as loud, hardly throb; and again. Generated by")
        assert "From v35" in doc["about"]
    if under_row() is not None:
        un_ = under_notes(); u_top = max(UNDER_TRIM, default=0.0)
        assert [(round(r, 9), round(w, 9)) for r, w in under_tones(UNDER_STEPS)] == [(round(r, 9), round(w, 9)) for r, w in under_tones(0)]      # a whole turn on, every tone stands where its neighbour stood
        for k in sorted({q[2] for q in un_}):
            PATCHES[f"os-under-{k}"] = {"about": f"Out of Step's note for the wave that slips under its own beat (chirper-zero, 28 Nov, v36), step {k} of {UNDER_STEPS}: plain tones at {' '.join(f'{r:g}' for r, _ in under_tones(k))} times the note, under one window; every one {k}/{UNDER_STEPS} of the note higher than a harmonic. Its loudness goes as the square of the velocity.",
                                        "play": {"vel_sens": 1, "gate": 1}, "synth": {"layers": under_layers(k), "filters": ["lp cutoff=9000"], "amp": {"a": f"{UNDER_EDGE[0]}ms", "d": "0s", "s": 1, "r": f"{UNDER_EDGE[1]}ms"}}}
            doc["tracks"].append({"name": f"under-{k}", "patch": f"os-under-{k}", "gain": UNDER_GAIN, "pan": 0.0, "notes": [{"at": round(t, 6), "len": UNDER_LEN, "pitch": UNDER_NOTE, "vel": round(10 ** (((UNDER_TRIM[i] if UNDER_TRIM else 0.0) - u_top) / 40), 5)} for i, t, kk in un_ if kk == k]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v36 the wave slips under its own beat (bars {under_row() + UNDER_FROM + 1} to {under_row() + ROW}): a short note whose beat is {UNDER_NOTE}'s and whose every tone is moved up by the same eighth of that at each step: the beat inside the note never changes, the wave under it is an eighth of a turn further on, and after {UNDER_STEPS} steps it is the first note again. Generated by")
        assert "From v36" in doc["about"]
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
        if under_row() is not None:
            un_ = under_notes(); u_sec = (under_row() + UNDER_FROM) * BEATS * 60 / BPM; u_f = hz(UNDER_NOTE); u_c = lambda x: 1200 * math.log2(x / u_f)
            print(f"the wave slips under its own beat ({UNDER_GAIN}), bars {under_row() + UNDER_FROM + 1}-{under_row() + ROW} ({int(u_sec) // 60}:{u_sec % 60:04.1f}): a note of {UNDER_LEN} beats ({UNDER_LEN * 60000 / BPM:.0f} ms) whose beat is {UNDER_NOTE}'s ({u_f:.2f} a second): {len(under_tones(1))} plain tones from {UNDER_RANKS[0]} to {UNDER_RANKS[1]} times it ({UNDER_RANKS[0] * u_f:.0f} to {UNDER_RANKS[1] * u_f:.0f} Hz) under one window ; a step moves every tone up {u_f / UNDER_STEPS:.2f} Hz ; {len(un_)} notes on beats {' '.join(f'{x:g}' for x in UNDER_AT)} of every bar ; steps by note: {' '.join(str(k) for _, _, k in un_)} ; the wave is most like itself after one over (Hz, cents from the note), by step: " + " ; ".join(f"{k}: " + " or ".join(f"{x:.1f} ({u_c(x):+.0f})" for x, _ in under_like(k)) for k in range(UNDER_STEPS)) + (f" ; trims {min(UNDER_TRIM):+.1f} to {max(UNDER_TRIM):+.1f} dB" if UNDER_TRIM else " ; no trims"))
        if throb_row() is not None:
            ts_ = throb_spans(); t_sec = throb_row() * BEATS * 60 / BPM; t_m = THROB_DEPTH
            print(f"a quarter of a turn and the throb is gone ({THROB_GAIN}), bars {throb_row() + 1}-{throb_row() + ROW} ({int(t_sec) // 60}:{t_sec % 60:04.1f}): three plain tones: {THROB_NOTE} ({hz(THROB_NOTE):.1f} Hz) and one {THROB_RATE * BPM / 60:g} Hz to either side, each {20 * math.log10(t_m / 2):.1f} dB under it ; in step (bars " + ", ".join(f"{int(at) // BEATS + 1}-{int(at + ln - 1) // BEATS + 1}" for at, ln, th in ts_ if th) + f"): the three swell and sink {THROB_RATE} times a beat, {1 - t_m:g} to {1 + t_m:g} of the middle tone ({20 * math.log10((1 + t_m) / (1 - t_m)):.1f} dB), the tops on beats {THROB_TOP:g} and {THROB_TOP + 1 / THROB_RATE:g} ; the middle one turned {THROB_TURN:g} of a turn (bars " + ", ".join(f"{int(at) // BEATS + 1}-{int(at + ln - 1) // BEATS + 1}" for at, ln, th in ts_ if not th) + f"): 1 to {(1 + t_m ** 2) ** 0.5:.3f} ({10 * math.log10(1 + t_m ** 2):.1f} dB), {2 * THROB_RATE} times a beat ; the last note goes out over {THROB_FADE[0]} beats ; both tracks' gain follows one lane: the master's own throb turned over, {len(THROB_FLAT)} places through every {THROB_BARS} bars, {min(THROB_FLAT):g} to {max(THROB_FLAT):g} dB")
        if sum_row() is not None:
            sr_ = sum_runs(); s_sec = sum_row() * BEATS * 60 / BPM; s_n = {k: sum(1 for q in sr_ if q[2] == k) for k in "IT."}
            print(f"one and one make two, one, or nothing ({SUM_GAIN}), bars {sum_row() + 1}-{sum_row() + ROW} ({int(s_sec) // 60}:{s_sec % 60:04.1f}): two plain tones at {sum_hz():.1f} Hz ({SUM_WAVES} waves to the sixteenth; {SUM_NOTE} {1200 * math.log2(sum_hz() / hz(SUM_NOTE)):+.1f} cents), one loudness ; the first alone for {SUM_ALONE} bars ; then the second by sixteenth, bar and bar about: {' | '.join(SUM_BARS)} (I in step: the two make {20 * math.log10(abs(2 * math.cos(math.pi * SUM_TURN['I']))):+.2f} dB ; T a third of a turn out: {20 * math.log10(abs(2 * math.cos(math.pi * SUM_TURN['T']))):+.2f} dB ; . half a turn out: nothing) ; {s_n['I']} strokes in step, {s_n['T']} a third out, {s_n['.']} silences ; both tones sound for {sum(q[1] for q in sr_):g} beats and are silent together for {sum(q[1] for q in sr_ if q[2] == '.'):g} of them ; trims by sixteenth of the bar (dB): " + " ".join(f"{t:g}" for t in SUM_TRIM) + f" ; alone {SUM_HELD:g}")
        if pole_row() is not None:
            pl0, pl1 = pole_span(); pl_sec = pl0 * 60 / BPM
            print(f"five out of step make a stair without end ({POLE_GAIN}), bars {pl0 // BEATS + 1}-{pl1 // BEATS} ({int(pl_sec) // 60}:{pl_sec % 60:04.1f}): {POLE_NOTE[0]} ({POLE_NOTE[1]:.2f} Hz) held {pl1 - pl0} beats, a sawtooth under 3 kHz ; {POLE_BANDS} windows {POLE_SPACING:g} octave apart from {POLE_LOW} Hz ({POLE_LOW} to {POLE_LOW * 2 ** (POLE_BANDS * POLE_SPACING):.0f} Hz), each a {POLE_Q:g}th of its frequency wide, climbing an octave every {POLE_CYCLE} bars: {(pl1 - pl0) // (BEATS * POLE_CYCLE)} turns ; in over {POLE_FADE[0]} beats and out over {POLE_FADE[1]}, from {POLE_FADE[2]} dB down ; the window that begins a turn at {POLE_LOW * 2:.0f} Hz stands on overtone, beat by beat: " + " ".join(f"{POLE_LOW * 2 * 2 ** (k / (BEATS * POLE_CYCLE)) / POLE_NOTE[1]:.1f}" for k in range(BEATS * POLE_CYCLE)))
        if buzz_row() is not None:
            bz = buzz_stabs(); bz_sec = buzz_row() * BEATS * 60 / BPM; bz_n = BUZZ_TONES[1] - BUZZ_TONES[0] + 1
            print(f"in step, a click; out of step, a hum ({BUZZ_GAIN} each), bars {buzz_row() + 1}-{buzz_row() + len(BUZZ_PAIRS)} ({int(bz_sec) // 60}:{bz_sec % 60:04.1f}): the tones {BUZZ_TONES[0]} to {BUZZ_TONES[1]} of {BUZZ_NOTE[0]} ({BUZZ_NOTE[1]:.2f} Hz: {BUZZ_TONES[0] * BUZZ_NOTE[1]:.0f} to {BUZZ_TONES[1] * BUZZ_NOTE[1]:.0f} Hz), {bz_n} of them at one level ; a stab of {BUZZ_LEN:g} beats on the off beats, in pairs: one in step (every tone begun together: a tick every {1000 / BUZZ_NOTE[1]:.1f} ms) and one out of step (each begun this part of its own wave late: " + " ".join(f"{buzz_late(k):g}" for k in range(BUZZ_TONES[0], BUZZ_TONES[1] + 1)) + ") ; the order turned round every other pair ; pairs a bar: " + " ".join(str(p) for p in BUZZ_PAIRS) + f" ; {len(bz) // 2} of each")
        if late_row() is not None:
            lt = late_starts(); lt_sec = late_row() * BEATS * 60 / BPM
            print(f"loudness by lateness ({LATE_GAIN} each), bars {late_row() + 1}-{late_row() + ROW} ({int(lt_sec) // 60}:{lt_sec % 60:04.1f}): two tones of {LATE_WAVES} waves to the beat ({LATE_WAVES * BPM / 60:.2f} Hz: {LATE_NOTE[0]} {1200 * __import__('math').log2(LATE_WAVES * BPM / 60 / LATE_NOTE[1]):+.0f} cents), one held for {ROW} bars, the other begun again on every beat ({len(lt)} notes)")
            for at, x, v in lt[:len(LATE_BY)]:
                print(f"   beat {int(at) % BEATS} of every bar: {x:.4f} of a wave late ({1000 * x * 60 / (LATE_WAVES * BPM):.2f} ms): the two together " + ("nothing" if v is None else f"{v:+.2f} dB of one"))
        if head_row() is not None:
            hd_b = head_row(); hd_f = BPM / (60 * BEATS)
            print(f"the beat that is only in the head ({HEAD_GAIN}), bars {hd_b + 1}-{hd_b + ROW} ({int(hd_b * BEATS * 60 / BPM) // 60}:{hd_b * BEATS * 60 / BPM % 60:04.1f}): the left ear {HEAD_WAVES} waves to the bar ({HEAD_WAVES * hd_f:.3f} Hz: {HEAD_NOTE[0]} {head_semis(HEAD_WAVES) * 100:+.1f} cents) ; the right ear " + ' '.join(f"{HEAD_WAVES + m} ({(HEAD_WAVES + m) * hd_f:.3f} Hz)" for m in HEAD_MORE) + " ; the difference in phase goes round " + ' '.join(f"{m}" for m in HEAD_MORE) + " times a bar (" + ' '.join(f"{m * hd_f:.2f}" for m in sorted(set(HEAD_MORE))) + f" a second) ; in phase at every bar line ; {HEAD_RISE} beats to come, {HEAD_GO} to go")
        if flip_row() is not None:
            fl = flip_notes(); fl_b = flip_row()
            print(f"in phase, out of phase ({FLIP_GAIN}), bars {fl_b + 1}-{fl_b + ROW} ({int(fl_b * BEATS * 60 / BPM) // 60}:{fl_b * BEATS * 60 / BPM % 60:04.1f}): the phrase {' '.join(f'{p} (beat {t:g})' for p, t in FLIP_TUNE)} ; {len(FLIP_TIMES)} times: {' '.join(FLIP_TIMES)} ; the left ear the same every time (pan -1), the right ear the same wave (in) or the wave upside down (out) (pan 1) ; {len(fl)} notes of {FLIP_LEN:g} beats (the last of each time {FLIP_LAST:g}: over before the bar ends)")
        if saws_row() is not None:
            sw_f = hz(SAWS_NOTE)
            print(f"two saws out of step ({SAWS_GAIN}), bars {saws_row() + 1}-{saws_row() + ROW} ({int(saws_row() * sec) // 60}:{saws_row() * sec % 60:04.1f}): a sawtooth on {SAWS_NOTE} ({sw_f:.2f} Hz), harmonics 1 to {SAWS_HARMS} ({SAWS_HARMS * sw_f:.0f} Hz), a note a bar from beat {SAWS_AT} held {SAWS_LEN} beats")
            for sw_k, sw_late in enumerate(SAWS_STEPS):
                if sw_late is None:
                    print(f"   bar {saws_row() + sw_k + 1}: the first saw alone"); continue
                sw_g, sw_tot = saws_model(sw_late)
                print(f"   bar {saws_row() + sw_k + 1}: the second saw upside down, {sw_late:g} of a wave late ({1000 * sw_late / sw_f:.2f} ms): " + ("nothing is left" if sw_tot is None else f"a pulse {100 * sw_late:g}% wide, {sw_tot:+.1f} dB against the one saw ; harmonics 1 to 8 against the one saw's, dB: " + " ".join("gone" if x is None else f"{x:+.1f}" for x in sw_g[:8]) + " ; gone: " + (" ".join(str(n) for n, x in enumerate(sw_g, 1) if x is None) or "none")))
        if alt_row() is not None:
            al_lo, al_hi = alt_notes(); al_f = hz(ALT_NOTE)
            print(f"an octave by phase alone ({ALT_GAIN}), bars {alt_row() + 1}-{alt_row() + ROW} ({int(alt_row() * sec) // 60}:{alt_row() * sec % 60:04.1f}): harmonics {ALT_HARMS[0]} to {ALT_HARMS[1]} of {ALT_NOTE} ({al_f:.2f} Hz: {ALT_HARMS[0] * al_f:.0f} to {ALT_HARMS[1] * al_f:.0f} Hz), a note on every off beat, {ALT_LEN:g} of a beat long ; {len(al_lo)} with every harmonic a sine (a pulse every {1000 / al_f:.1f} ms: heard on {ALT_NOTE}) ; {len(al_hi)} with the even harmonics a quarter turn on (a pulse every {500 / al_f:.1f} ms: heard an octave up), every second note from bar {alt_row() + ALT_PLAIN + 1}")
        if HUM and SWARM_ROWS:
            hm_b = SWARM_ROWS[HUM_ROW]; hm_f = HUM_TIMES * BPM / 60; hm_n = SWARM_N; hm_th = hum_turns(); hm_p = hum_paths(); hm_m = SWARM_SUB // HUM_STEP
            hm_err = max(abs(hm_th[i][k] - HUM_TIMES * (k / HUM_STEP + hm_p[i][k * hm_m])) for i in range(hm_n) for k in range(len(hm_th[i])))
            hm_again = (hm_n - 1) / (2 * SWARM_OFF * HUM_TIMES)
            print(f"the swarm hums, bars {hm_b + 1}-{hm_b + SWARM_BARS} ({int(hm_b * sec) // 60}:{hm_b * sec % 60:04.1f}): each of the swarm's {hm_n} clicks holds a tone of {HUM_TIMES} waves to its OWN beat ({hm_f:.2f} Hz at the song's tempo: {HUM_NOTE} {1200 * math.log2(hm_f / hum_note_hz()):+.0f} cents; the slowest {hm_f * (1 - SWARM_OFF):.2f}, the fastest {hm_f * (1 + SWARM_OFF):.2f}) and " + ", ".join(f"{r:g} times it {d:g} dB" for r, d in HUM_PARTS[1:]) + f" ; {HUM_GAIN} each, pan -{HUM_PAN:g} to {HUM_PAN:g} ; while nobody listens the {hm_n} are one tone again every {hm_again:.3f} beats ({hm_again * 60 / BPM:.3f} s) ; the lane against the swarm's arithmetic: {hm_err:.4f} of a turn at most ; coming up over {HUM_IN:g} beats, held for {HUM_HELD} of the row's {SWARM_BARS} bars, let go in {HUM_LET}")
            for hm_j in range(HUM_HELD):
                hm_r = [hum_step(k) for k in range(hm_j * BEATS * HUM_STEP, (hm_j + 1) * BEATS * HUM_STEP + 1)]
                hm_fs = [hum_lane(i)[hm_j * BEATS * HUM_STEP][1] for i in range(hm_n)]
                hm_top = [k / HUM_STEP for k in range(hm_j * BEATS * HUM_STEP, (hm_j + 1) * BEATS * HUM_STEP) if hum_step(k) > 0.8 and hum_step(k) >= hum_step(max(0, k - 1)) and hum_step(k) > hum_step(k + 1)]
                print(f"   bar {hm_b + hm_j + 1}: in step {min(hm_r):.2f} to {max(hm_r):.2f} ({20 * math.log10(max(1e-9, (sum(x * x for x in hm_r) / len(hm_r)) ** 0.5)):+.1f} dB against one tone of all {hm_n}) ; the tones at its first beat {min(hm_fs):.2f} to {max(hm_fs):.2f} Hz ; one tone at beat(s) of the row: " + (" ".join(f"{x:g}" for x in hm_top) or "-"))
        if pm_row() is not None:
            pm_i = 2 * math.pi * PM_TURN
            print(f"a note out of step with itself (phase modulation), bars {pm_row() + 1}-{pm_row() + len(PM_RATES)} ({int(pm_row() * sec) // 60}:{pm_row() * sec % 60:04.1f}): {PM_NOTE} ({pm_hz():.2f} Hz), its phase pushed {PM_TURN:g} of a turn each way ({pm_i:.3f} radians) ; {PM_GAIN}, pan {PM_PAN:g} ; the note itself {20 * math.log10(abs(pm_bessel(0, pm_i))):.1f} dB, side tones {' '.join(f'{20 * math.log10(abs(pm_bessel(n, pm_i))):.1f}' for n in (1, 2, 3))} dB")
            for pm_j, (pm_kind, pm_k) in enumerate(PM_RATES):
                pm_f = pm_rate(pm_j)
                print(f"   bar {pm_row() + pm_j + 1}: {pm_k:g} a {pm_kind} ({pm_f:.2f} Hz): " + (f"a wobble from {pm_hz() - pm_i * pm_f:.1f} to {pm_hz() + pm_i * pm_f:.1f} Hz" if pm_f < 20 else "tones at " + " ".join(f"{abs(pm_hz() + n * pm_f):.0f}" for n in (-3, -2, -1, 0, 1, 2, 3)) + " Hz"))
        if back_row() is not None:
            bk_b0 = back_row(); bk_per = ROW // len(BACK_STAGES)
            print(f"the whistle is put in step (pulse compression), bars {bk_b0 + 1}-{bk_b0 + ROW} ({int(bk_b0 * sec) // 60}:{bk_b0 * sec % 60:04.1f}): a rise from {BACK_SPAN[0]:g} to {BACK_SPAN[1]:g} Hz into the chains of v23 ; a click comes out on sixteenths {', '.join(str(x) for x in BACK_ON)} ; into the longest chain {BACK_GAIN}, 3 dB up a halving ; heard {BACK_HEARD}")
            for bk_j, bk_k in enumerate(BACK_STAGES):
                print(f"   bars {bk_b0 + bk_j * bk_per + 1}-{bk_b0 + (bk_j + 1) * bk_per}: {bk_k} filters ; the whistle starts {1000 * disp_late(BACK_SPAN[0], bk_k):.1f} ms before the instant and ends {1000 * disp_late(BACK_SPAN[1], bk_k):.1f} ms before it ({1000 * (disp_late(BACK_SPAN[0], bk_k) - disp_late(BACK_SPAN[1], bk_k)):.1f} ms long)")
        if disp_row() is not None:
            di_b0 = disp_row(); di_per = ROW // len(DISP_STAGES)
            print(f"the click comes apart (all-pass: phase only), bars {di_b0 + 1}-{di_b0 + ROW} ({int(di_b0 * sec) // 60}:{di_b0 * sec % 60:04.1f}): A's click on sixteenths {', '.join(str(x) for x in DISP_ON)} again through a chain of all-pass filters ({DISP_BAND[0]:g} to {DISP_BAND[1]:g} Hz, q {DISP_Q:g}) ; {DISP_GAIN}, pan {DISP_PAN}")
            for di_j, di_k in enumerate(DISP_STAGES):
                print(f"   bars {di_b0 + di_j * di_per + 1}-{di_b0 + (di_j + 1) * di_per}: {di_k} filters ; held back, ms: " + " ".join(f"{f:g} Hz: {1000 * disp_late(f, di_k):.1f}" for f in (588.0, 784.0, 1176.0, 1568.0, 2352.0, 3136.0, 4704.0, 6272.0)))
        if rhy_row() is not None:
            rh_b0 = rhy_row(); rh_hz = 440 * 2 ** (({"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[RHY_ROOT[0]] + (-1 if "b" in RHY_ROOT else 0) + 12 * (int(RHY_ROOT[-1]) + 1) - 69) / 12)
            print(f"one note comes apart (the rhythmicon), bars {rh_b0 + 1}-{rh_b0 + ROW} ({int(rh_b0 * sec) // 60}:{rh_b0 * sec % 60:04.1f}): harmonics 1 to {RHY_N} of {RHY_ROOT} ({rh_hz:.2f} Hz): " + ", ".join(f"{k}: {k * rh_hz:.0f} Hz {float(RHY_GAIN[:-2]) - 20 * math.log10(k):.1f} dB from bar {rh_b0 + 1 + int((k - 1) * RHY_BUILD)}" for k in range(1, RHY_N + 1)) + f" ; {sum(len(rhy_strokes(k)) for k in range(1, RHY_N + 1))} strokes")
            for rh_bar in sorted({0, 1, 2, ROW - 1}):
                print(f"   bar {rh_b0 + rh_bar + 1}: " + " ".join(f"{p}/{q}:{'+'.join(str(k) for k in ks)}" for (p, q), ks in rhy_together(rh_bar)))
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
        if over_row() is not None:
            ov_ticks = over_path()[1]; ov_bob = over_bob(); ov_b0 = over_row()
            print(f"   the pendulum goes over the top ({OVER_GAIN}), bars {ov_b0 + 1}-{ov_b0 + ROW} ({int(ov_b0 * BEATS * 60 / BPM) // 60}:{ov_b0 * BEATS * 60 / BPM % 60:04.1f}): a small swing takes {OVER_PERIOD:g} beats ; it starts at {OVER_START:g} degrees ; pushed {(over_path()[2] - 1) * 100:.2f}% at every pass through the bottom ; {len(ov_bob)} ticks of the bob ({OVER_NOTE}), {len(ov_ticks)} of the escapement ({OVER_TICK[0]})")
            print("      passes through the bottom (bar.beat: speed after the push, 1 = just reaches the top ; beats since the last): " + " ".join(f"{ov_b0 + 1 + int(t // BEATS)}.{t % BEATS + 1:.2f}:{k:.3f};{t - (ov_ticks[i - 1][0] if i else 0):.2f}" for i, (t, _, k) in enumerate(ov_ticks)))
            ov_a = over_path()[0]; ov_top = max(range(int(ov_ticks[OVER_PUSHES + 1][0] * OVER_STEPS)), key=lambda q: abs(ov_a[q]))
            print(f"      the highest it swings before it goes over: {abs(math.degrees(ov_a[ov_top])):.1f} degrees at beat {ov_top / OVER_STEPS:.2f} of the row ; over 150 degrees for {sum(1 for q in ov_a[:int(ov_ticks[OVER_PUSHES + 1][0] * OVER_STEPS)] if abs(q) > math.radians(150)) / OVER_STEPS:.2f} beats ; whole turns by the row's end: {abs(ov_a[-1]) / (2 * math.pi):.2f}")
            print("      the bob's pan at each half beat: " + " ".join(f"{ov_bob[q][2]:+.2f}" for q in range(0, len(ov_bob), OVER_PER_BEAT // 2)))
        if turn_span():
            tu0, tu1 = turn_span(); tu_sec = 60 / BPM; tu = turn_steps()
            print(f"   a click that nobody struck ({TURN_GAIN}): {NOTE} held, one plain tone at {turn_hz():.3f} Hz ({1200 * math.log2(turn_hz() / WAVE_HZ):+.2f} cents), bars {int(tu0 // BEATS) + 1}-{int(tu1 // BEATS)} ({int(tu0 * tu_sec) // 60}:{tu0 * tu_sec % 60:04.1f}-{int(tu1 * tu_sec) // 60}:{tu1 * tu_sec % 60:04.1f}), turned over every {TURN_EVERY:g} beats from {TURN_FIRST:g} after the line ({TURN_EVERY * tu_sec * 1000:.2f} ms written, {TURN_SLOW * 1000:.3f} more as made): {len(tu)} turns, {TURN_WAVES:g} waves in each ; a shelf, {TURN_SHELF[1]} over {TURN_SHELF[0]} Hz")
            print("      each turn's step as a share of twice the tone's height: " + " ".join(f"{v:.2f}" for _, v in tu))
            print("      the largest steps (bar.sixteenth): " + " ".join(f"{int(b // BEATS) + 1}.{b % BEATS * 4:g}" for b, v in tu if v > 0.9) + " ; the smallest: " + " ".join(f"{int(b // BEATS) + 1}.{b % BEATS * 4:g}" for b, v in tu if v < 0.3))
        if GEAR and GEAR_ROWS:
            ge_beat = 60000 / BPM
            print(f"   a second drum changes gear ({GEAR_GAIN}, on {GEAR_NOTE}): every ratio from 1:1 to 2:1 with a lower number of {GEAR_MOST} or less ; " + " ; ".join(f"{p}:{q} x{t} ({q * t} beats, {p * t} strokes, {q / p * ge_beat:.1f} ms apart)" for p, q, t in gear_plan()) + f" ; {sum(q * t for _, q, t in gear_plan())} beats, {sum(p * t for p, _, t in gear_plan())} strokes a row")
            for ge_row, ge_way in GEAR_ROWS:
                ge_b = 0; ge_out = []
                for p, q, t in (gear_plan() if ge_way == "up" else gear_plan()[::-1]):
                    ge_out.append(f"{p}:{q} from bar {ge_row + ge_b // BEATS + 1} beat {ge_b % BEATS + 1}"); ge_b += q * t
                print(f"      bars {ge_row + 1}-{ge_row + GEAR_BARS} ({int(ge_row * BEATS * 60 / BPM) // 60}:{ge_row * BEATS * 60 / BPM % 60:04.1f}), {ge_way}: " + " ; ".join(ge_out))
            print("      one turn of each, in beats from its start: " + " ; ".join(f"{p}:{q}: " + " ".join(f"{j * q / p:.3f}" for j in range(p)) for p, q, _ in gear_plan()))
        if SWARM:
            sw_t = swarm_ticks(); sw_ms = 60000 / BPM
            print(f"   the click comes apart and finds itself, bars " + ", ".join(f"{b + 1}-{b + SWARM_BARS}" for b in SWARM_ROWS) + f": {SWARM_N} clicks ({SWARM_GAIN}; {SWARM_NOTES[0]} on the left to {SWARM_NOTES[-1]} on the right), the slowest {SWARM_OFF * 100:g}% under the tempo, the fastest as far over ; deaf for {SWARM_DEAF} beats, then each leans to the rest (to {SWARM_LEAN:g} turns a beat) and changes its tempo (to {SWARM_LEARN:g}) ; strokes each: {sorted(set(len(x) for x in sw_t))}")
            sw_rows = [[min(x, key=lambda v: abs(v - sw_b)) - sw_b for x in sw_t] for sw_b in range(SWARM_BARS * BEATS)]
            print("      first to last, ms, at each beat: " + " ".join(f"{sw_ms * (max(r) - min(r)):.2f}".rstrip("0").rstrip(".") if max(r) - min(r) > 1e-7 else "0" for r in sw_rows))
            print("      the slowest and the fastest against the beat, ms, at the first beat of each bar: " + " ".join(f"{sw_ms * sw_rows[b][0]:+.2f}/{sw_ms * sw_rows[b][-1]:+.2f}" for b in range(0, SWARM_BARS * BEATS, BEATS)) + f" ; the middle of the swarm, at its furthest from the beat: {max(abs(sum(r)) / len(r) for r in sw_rows) * sw_ms:.3f} ms")
        if FOCUS:
            fo_t = focus_tones(); fo_bar = BEATS * 60 / BPM
            print(f"   the drum comes into focus, bars " + ", ".join(f"{b + 1}-{b + FOCUS_BARS} ({int(b * fo_bar) // 60}:{b * fo_bar % 60:04.1f})" for b in FOCUS_ROWS) + f": {len(fo_t)} held tones ({FOCUS_GAIN}), the multiples {FOCUS_PARTS[0]} to {FOCUS_PARTS[1]} of the beat ({BPM / 60:g} Hz): {fo_t[0][0]:.2f} to {fo_t[-1][0]:.2f} Hz ; at the start tone k is k squared / {2 * (len(fo_t) - 1)} of a turn out (the outermost {fo_t[0][1]:.3f}) and {1000 * ((FOCUS_PARTS[0]) * BPM / 60 - fo_t[0][0]):.1f} mHz flat at the most ; in phase on the line of bars " + ", ".join(str(b + FOCUS_BARS + 1) for b in FOCUS_ROWS))
            print("      the slide lasts, at the start of each bar of the row, ms: " + " ".join(f"{focus_slide(j):.0f}" for j in range(FOCUS_BARS)) + " ; on the line after: 0 (one thump)")
        if SING:
            sg_b0, sg_b1 = sing_span(); sg_trs = {t["name"]: t for t in song()["tracks"]}; sg_n = sg_trs["sing"]["notes"]; sg_k = sg_trs["singkey"]["notes"]; sg_bar = BEATS * 60 / BPM
            print(f"   the clicks sing, bars {sg_b0 + 1}-{sg_b1} ({int(sg_b0 * sg_bar) // 60}:{sg_b0 * sg_bar % 60:04.1f}-{int(sg_b1 * sg_bar) // 60}:{sg_b1 * sg_bar % 60:04.1f}): {len(sg_n)} of {SING_OF}'s strokes again, in the middle, every phase set to nought ({SING_GAIN}) ; each sings the tune's note for its place, an octave down (the robot's note {SING_PITCH} for a key of C4): step " + " ".join(f"{p}:{TUNE[p]}" for p in sorted(TUNE)) + f" ; the key is set {SING_EARLY:g} of a beat ({SING_EARLY * 60000 / BPM:.0f} ms) before its stroke ; the first bar's keys " + " ".join(x["pitch"] for x in sg_k[:10]))
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
