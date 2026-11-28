#!/usr/bin/env python3
"""Escapement (Chirpers 11), track 5 (chirper-zero): HEARING THINGS. The slot's word is ILLUSIONS.

Three things that are not on the record, and one rule: THE EAR IS THE INSTRUMENT, so nothing here is hidden by a
trick of the mix. Each is plain arithmetic and all three work on one speaker.

1. THE BEAT THAT TURNS AROUND. The song opens with a click and a bass and no bass drum. They are on the OFF-beats
   (steps 2, 6, 10, 14), but with nothing to say so the ear takes them for the beat. When the bass drum comes in on
   the real beat, not one note of the click or the bass moves: the listener does. It is done twice.

2. THE BASS THAT IS NOT THERE. The bass plays only the second to sixth harmonics of each note (110, 165, 220, 275,
   330 Hz for the A at 55): it has no partial at the pitch you hear. In "not there" the bass drum stops too and the
   record has next to nothing under 95 Hz (22 dB under the rest); then the real fundamental is put under it for
   eight bars and taken away.

3. THE ACCELERANDO THAT NEVER ARRIVES (a Risset rhythm). A hat in LAYERS layers, each twice as fast as the one below.
   Over one row (CYCLE beats) every layer doubles its speed: its strokes fall where C * 2^(t / CYCLE) passes a whole
   number, so layer j ends the row exactly where layer j + 1 began it. Each layer's loudness follows its speed (a
   sine-squared window over the LAYERS octaves), so the fastest fades out as it becomes a blur and a new slowest
   fades in underneath: the row repeats note for note, and it has been speeding up all the way through. C is 23,
   which makes the layers start each row at 0.498, 0.996, 1.99 and 3.98 strokes a beat: on the grid, near enough.
   Then they pull ahead of it, and at the row's end they are on it again, one octave on. In "out" it runs backwards.

THE FORM IS ARITHMETIC: a row is ROW bars; SECTIONS lists each section's rows and its parts (a part may be given the
bars of the section it plays: (from, to)). Every note comes from those.

v1 is the SKELETON (26 Nov): the three illusions, each stated once and then together, with few sounds.

v2 (26 Nov): THE HAT ALSO RISES (C11T5_SHEP=0 takes it out: v1). From the third row of "never arrives" each layer
of the Risset rhythm has a voice of its own, a small struck tone, on the same strokes; the four are an octave
apart (A3, A4, A5, A6) and every one of them climbs an octave through the row (one lane, `rise`, 0 to 12
semitones). So a layer ends the row at the speed AND the pitch at which the next began it, the same windows fade
the top out and the bottom in, and the row repeats note for note: it is a Shepard scale and a Risset rhythm at
once, getting faster and higher for ever and going nowhere. In "out" it runs backwards: slower and lower, for ever.

v3 (26 Nov): THE DRUM GOES ROUND THE CLICK (C11T5_ROUND=0 takes the section out: v2). The click stands on step 2
of every beat's four sixteenths, and the first illusion used two of the four places a drum can stand against it:
nowhere (the click is the beat) and two sixteenths before it (the click is the "and"). A new section, "round the
click", after "the wrong one again", uses the other three, a row each, the drum one sixteenth later every row:
  1. THE DRUM JUST BEFORE THE CLICK (kick on steps 1, 5, 9, 13): DUM-ta. The click is the drum's echo, the "e".
  2. THE DRUM ON THE CLICK (2, 6, 10, 14): the wrong beat, and now the drum says so too. The click is the beat.
  3. THE DRUM JUST AFTER THE CLICK (3, 7, 11, 15): ta-DUM. The click is a pickup, the "a", and the bar gallops.
Then "all three" puts the drum a sixteenth later again, which is the true beat (0, 4, 8, 12), and the click is the
"and". So in four rows the same click has been every sixteenth of the beat, and not one note of it or of the bass
has moved since the first bar: only the drum has, and with it where the listener stands. The drum rests for the
last bar of each row (the step is a silence, not a stumble); a clap on its two and four joins it half-way through.

v4 (26 Nov): THE CHORD THAT DOES NOT STOP (C11T5_HELD=0 takes it out: v3). A fourth thing that is not on the
record: half of a chord. The song has had no chord; now there is one (A minor seventh, four plain tones), and it is
CHOPPED: it sounds for a sixteenth and is silent for a sixteenth, all the way through. In a new section, "held"
(after "not there"), it is first heard as it is, a chord with holes in it. Eight bars on a burst of noise is put in
every hole, in the chord's own band and louder than the chord, starting the instant the chord stops and stopping
the instant it starts. Nothing is done to the chord. The ear, given a noise loud enough to have covered the chord,
decides the chord went on behind it: it is heard HELD, unbroken, with a noise in front of it (the continuity
illusion: a fence in front of a landscape). In the last row of "all three" (now four) it is held under everything;
at "out" the noise is taken away and for eight bars the chord has its holes again: it always had.

v5 (26 Nov): THE LINE COMES APART (C11T5_LINE=0 takes it out: v4). A fifth thing, and it is a rhythm that changes
when no stroke moves. A small pip plays three strokes and a rest, over and over, a sixteenth apart: A B A . A B A .
(the first A on the click, so it is the click's figure: a gallop). A is always the same note. B is the same note
too, at first: one line, galloping. Then, a bar at a time, B is a third above A, a fifth, an octave. Not one stroke
is a millisecond earlier or later, but the ear will not keep notes that far apart in one line at this speed: the
gallop COMES APART into two lines that have nothing to do with each other, A alone on every eighth, even as a
clock, and B alone once a beat, half as fast. Then B comes back down, a fifth, a third, the same note, and
somewhere on the way (later than where it left: the ear holds on to what it has) there is one line again and it
gallops. It is heard twice inside what was already there: in the second row of "the wrong one" (with the bass and
no drum) and all through "the wrong one again". The song is no longer than it was.

v6 (26 Nov): THE ANSWER THAT AGREES (C11T5_BOTH=0 takes it out: v5). A sixth thing: two notes that go up and
down at once. A new bell: every note of it is that note in EVERY octave at once, under one fixed curve of
loudness (loudest round 440 Hz, fading out below and above), so the bell has a note-name and no octave: B is
B, but which B? Between two such bells the ear takes the shorter way: B to C is up a step, not down a seventh.
B to F is half an octave: there is no shorter way. Up a tritone and down a tritone are the same two bells, and
which one is heard depends on the listener, and on what was just heard. So the song says something first.
"B, C, D" (three bells climbing), and then the answer, B ... F: the ear has just been in the notes between B and
the F above, and hears the answer go UP. Then "B, A, G" (three bells falling), and the same answer, B ... F,
note for note the same two strokes: now it goes DOWN. Four times in the third row of "turned around" (the
bells on the click's own strokes, the drum under them), and again in the last row of "round the click": while
the drum shows that one click is every part of the beat, the bells show that one answer is both directions.

v7 (26 Nov): THE STAIRS (C11T5_STAIRS=0 takes it out: v6). A seventh thing, and the plainest of the endless ones:
stairs that go up and come back to where they began. The bells with no octave again, four of them a minor third
apart: B, D, F, A flat. From any one to the next the shorter way is UP three semitones (the other way is down
nine), so every step is heard to rise; and the fourth step, from A flat, is to B: the bell the stairs began
on, the same samples, and it too is heard as a step up. Four steps and the stairs are back, and have only ever
climbed (Shepard's scale; Penrose's staircase, with four flights). They are the first two rows of "never
arrives", before the hat's ramp begins: the song shows the steps first and then the slope. In the first row a
bell on every one of the click's strokes, so each bar is the four flights once; in the second a bell every
eighth, twice round a bar: the stairs go twice as fast and get no higher, as the hat goes twice as fast and
gets no faster. The four bells are the leading-note chord of the song's key (G sharp, B, D, F over the bass's
A), and the one note the stairs never tread on is A: they step over home every time round. And two of the four
are the answer of v6, B and F: on the stairs F is two flights above B, and B is two flights above F.

v8 (26 Nov): THE RABBIT (C11T5_RABBIT=0 takes it out: v7). An eighth thing, and the first that is a PLACE. The other
seven are notes, beats and rhythms that are not there; this is somewhere that is not there. A click is struck
four times on the left and then four times on the right, and never anywhere else. Slowly, that is what is heard:
four there, four here. Quickly (under a tenth of a second from click to click) it is heard to HOP ACROSS in even
steps, through places between the two where nothing was struck: the ear puts each click where the NEXT one says
it was going (sensory saltation; on the skin it is called the cutaneous rabbit). It is in the one bar at the end
of each row of "round the click" where the drum rests, and it is the bar's fill: the roll three times, each twice
as fast as the last (a sixteenth, a thirty-second, a sixty-fourth between clicks: 120, 60 and 30 ms), the third
ending on the bar line, so the first can still be counted (four and four) and the third cannot. It starts on the
click's own stroke, an octave above it, dry. Left to right, then back the next row, then left to right again.
In mono it is a roll. It needs two ears or two speakers.
ITS LEVEL WAS BENCHED: the master holds a lone click at its ceiling, so at -9, -14 and -18 dB the rabbit leaves
the mix at -16.2, -15.8 and -17.1 dBFS (20 ms), and what the gain changes is how much the click and the bass
under it are turned down where a rabbit click falls on them: 2.1, 0.9 and 0.45 dB at the worst stroke. -18 dB.
The rim is not the same samples twice (each stroke differs from the next by 21 dB under itself, in one place as
between the two); its level, length and note are.

v9 (26 Nov): BETWEEN THE EARS (C11T5_PULSE=0 takes it out: v8). A ninth thing, and the first that needs two ears
to be an illusion at all. "Not there" already has a bass with no fundamental; now it has a PULSE THAT IS NOT ON
THE RECORD. Two plain tones are held through its three rows (bars 81 to 104), one a little under A4 and one as
far over it, three cycles a beat apart (6.25 Hz: 436.88 and 443.13 Hz). First row: both in the middle. Two tones
that close beat, and that beat is REAL: the sum is one tone on A4 that goes loud and quiet three times a beat,
a triplet against the song's twos and fours, where the bass drum has stopped. It is on the record: a meter
reads it.
Second row: over four bars the two tones go apart, to an ear each (and each is lifted as the other leaves, so
neither ear gets quieter). Bar by bar the beat in each ear gets shallower, and from bar 93 it is gone: each ear
has ONE steady tone, and a meter on either channel reads no triplet. With two ears you go on hearing it, slower
to speak and somewhere inside the head: the brain compares the two ears' phases and reports a beat (a binaural
beat: Dove, 1839). Third row: the two tones close to a cycle and a half a beat apart (3.125 Hz: 438.44 and
441.56 Hz): three in the time of two beats, played by nobody and present in neither ear.
ON ONE SPEAKER the two tones are added in the air and the pulse is simply true all the way: this one does not
fool a speaker; it shows what the head adds when the speaker is taken away. To test it on headphones: take one
side off in the second half of "not there" and the pulse stops.
WHY THREE, AND NOT TWO: the master's compressor ducks everything, these tones too, on the drum and on the click:
twice a beat. A pulse of two a beat was benched first and each ear's tone then DID have a two-a-beat movement
on the record (9.8 dB under its mean, to the sum's 3.2): the drum's, not the tones', but a meter cannot tell.
Odd rates are the ones the drum does not have.
(The tones are `sine phase=0` and start together, so the sum is loudest on the beat. Neither ear is ever given
A4: it is the mean of the two, and it is what is heard. The patches say `play: {gate: 1}`: a note otherwise
sounds for 95% of its written length.)

v10 (26 Nov): TWO SCALES NEITHER EAR IS GIVEN (C11T5_SCALE=0 takes it out: v9). A tenth thing: Deutsch's scale
illusion (1975), at the rate she used (four tones a second: the song's eighths). The scale of A minor goes UP
from A4 to A5 and DOWN from A5 to A4 at the same time, a pip on every eighth, and the two scales are dealt out
to the ears like cards: the first note of the rising one to the left and of the falling one to the right, the
second the other way about, and so on. So NEITHER EAR IS GIVEN A SCALE. The left ear's part is A4 G5 C5 E5 E5
C5 G5 A4: leaps of a seventh, a fifth, a third; the right's is A5 B4 F5 D5 D5 F5 B4 A5. What is heard is two
smooth lines, the high notes together on one side (A5 G5 F5 E5 E5 F5 G5 A5) and the low ones on the other (A4
B4 C5 D5 D5 C5 B4 A4): the ear sorts by PITCH, not by where each note came from, and puts each line in one
place. No note is moved, and half the notes are heard in the ear they were not played to.
It is taught piece by piece in the second row of "turned around" (bars 25 to 32, 0:46 to 1:01): two bars of the
left ear's part alone (a jagged tune), two of the right's alone (another), then four bars of both: and the
jagged tunes are gone.
ON ONE SPEAKER there are no sides, and the two scales, which cross in the middle, are still not heard to
cross: the high line turns back at E5 and the low one at D5 (they bounce). The sorting by pitch is the same.
Two tracks (`scale-l`, `scale-r`), an ear each and dry, on the song's plain pip (`ht-pip`).

v11 (26 Nov): THE WAY DOWN LEADS UP (C11T5_FALL=0 takes it out: v10). An eleventh thing, and it is the stairs (v7)
the other way and with a twist: Risset's paradox (1969). The bells go DOWN, three semitones a step, round the four
(B, Ab, F, D, and B is three under D), a bell an eighth, for six bars: 48 steps, twelve times round, 144 semitones
down by name. And while they go down, the curve that every bell is under goes UP, one octave over the 48 steps: a
quarter of a semitone a step, against the three of the step itself, so no step is heard as anything but a step
down. The 48th bell is B again: the same B in every octave as the first, and it is loudest an octave HIGHER.
Forty-eight steps down, and it has arrived above where it set out. The curve starts an octave under where the v6
bells have theirs (loudest at 220 Hz) and ends on it (440 Hz): the last bell is the v6 B.
It is said plainly at both ends, in the second row of "all three" (bars 161 to 168, 5:07 to 5:23): in the first
bar the first bell alone, twice; in the last bar the last bell and the first, turn about (last, first, last,
first), and the first is the lower.
The v6 bells are one patch a note-name with the curve built in, so the curve cannot move. These are made of their
parts instead: one plain tone (`ht-part`, loudness straight from velocity) and a note for every octave of every
bell, each as loud as the curve says where the curve is by then. With the curve where v6 has it, one of these is
one of those. On one speaker it is all there.

v12 (26 Nov): THE FIRST ONE WINS (C11T5_FIRST=0 takes it out: v11). A twelfth thing, and it is where a sound is.
A small wooden click is given to BOTH ears, the same click, just as loud in each. In "held" (bars 105 to 120,
where the drum and the bass have stopped) it plays every three sixteenths, three against the click's four, and
only one thing about it changes: how much LATER the right ear gets it.
  bars 105-106: no later. The same signal in both ears is one click, in the middle.
  bars 107-108: 0 to 0.65 ms later. That is all the difference a head makes: the click walks to the left ear,
                and nothing got quieter anywhere.
  bars 109-110: 0.65 to 5 ms. The right ear's click is as loud as the left's and a whole five thousandths of a
                second apart from it, and it is not heard as a click at all: the ear takes the first to arrive
                for where the sound is and folds the second into it (the law of the first wavefront: Wallach,
                Haas, 1949; it is how a voice is found in a room full of its own echoes).
  bars 111-112: 5 to 60 ms. Somewhere here it comes apart: a second click, on the right, walking away.
  bars 113-120: the same, backwards, and now the late ear's click is TWICE AS LOUD (+6 dB). Two clicks, one
                loud on the right; then they fold, and the click is on the LEFT, where it is quieter, because
                it is first there. Only when the two arrive together (the last two bars) does the louder ear
                have it: the click jumps across the head to the right.
On one speaker nothing is hidden: the two clicks add, and a click grows a flam and then an echo, and takes it back.
The click is three plain tones that start at nought (C5 and two bar-partials over it), so the two ears' clicks
are the same to the sample.
ALSO, THE CLICK'S REPAIR (C11T5_TRIM=0 leaves the click as it was): `compscore --bands` said this song has 12 dB
more than the rest of the record at 1.9 kHz and 10 dB more at 640 Hz. Each part read alone: both are the click
(the rim's own note, E5, 659 Hz, and its third partial, 1978 Hz). Its two notes are turned down; its snap is not.
The cut comes in over bars 3 to 8 and goes out over bars 177 to 184: the first two bars and the last sixteen, which
other songs play over, have the click as it always was.

v13 (26 Nov): THE SECOND ONE SOUNDS LOUDER (C11T5_PAIR=0 takes it out: v12). Two small clicks, two sixteenths
apart (240 ms), and then a gap three times as long, as loud as each other AT THE EAR: the ear does not hear two
the same. It hears the second as the loud one (an accent made of time alone: Povel and Okkerman 1981, of two
equal sounds close together before a silence). They come on the sixteenth after beats one and three and the
sixteenth before beats two and four, either side of the song's own click, from "turned around" to "all three"
(not in "held", and not in "round the click", where the drum goes round and would land on them). And the song
weighs the illusion: section by section the second stroke is really turned DOWN, by 0, 2, 4 and 6 dB, and at
the end it is the same again. Where the two SOUND equal is what the timing is worth in dB.
TWO THINGS THE MASTER DOES, both measured and both written into the form: (1) a stroke must not fall WITH the
bass drum: the master takes 9 dB off whatever does (the first version had the first stroke on the beat);
(2) written the same to the sample (C11T5_PAIR_LIFT=0), the second stroke reaches the ear 3 to 6 dB under the
first: it falls a sixteenth after the click and the bass, which the master is still holding down. So the
second is written that much UP (PAIR_PLAN's third number), and the two are equal where it counts.

v14 (27 Nov): THE TUNE THAT IS IN NEITHER EAR (C11T5_HUG=0 takes it out: v13). A new section, "in the noise",
one row after "held". Both ears are given THE SAME noise, sample for sample, except that the right ear's has been
through an all-pass filter: a filter that changes no loudness at any frequency, only the phase, and that only in
a narrow place (a whole turn round one frequency, most of it within a tone either side). Each ear alone has plain
noise, and a meter on either channel reads the same spectrum to a twentieth of a dB. With two ears there is a faint NOTE in the
noise at that frequency, somewhere in the head: the brain compares the two ears and finds the one place where
they disagree (Cramer and Huggins, 1958). The place is moved, two beats at a time, through the notes the line
takes when it comes apart (A C E A, A E C A): a tune that neither ear is given.
It is said twice. The first four bars it is only between the ears. The last four the same tune is also played,
quietly (8 dB under the noise), by a plain tone in the middle: so that one speaker has it too, and two ears can check what they thought
they heard.
ON ONE SPEAKER the two ears' noises are added and the place where they disagree cancels: the first four bars are
noise with a narrow notch that moves (15 to 21 dB deep, a tone either side). This one does not fool a speaker.
To test it on headphones: take one side off in the first four bars and the tune is gone.

v15 (27 Nov): THE WAY UP IS TWO WAYS DOWN (C11T5_WES=0 takes it out: v14). Bars 3 to 8, where there was only
the click. A pip plays three notes going UP, A C E, a sixteenth each, over and over: A C E A C E. Every other
pip is played by a second hand. For two bars the two hands have the same sound, and what is heard is what is
written: one line climbing, again and again. Over the next two bars the second hand's sound is made brighter
(a filter opened, nothing else: no note moves, no stroke moves, none is louder by the fader). For the last two
bars the two sounds are far apart, and the ear will no longer hear them as one line: it hears two, one dull and
one bright, half as fast, and EACH OF THEM GOES DOWN: the dull hand has A E C, A E C and the bright one C A E,
C A E. Three notes shared out between two hands: each hand gets every other note, and every other note of a
rising three is a falling three. (David Wessel's illusion, 1979: the ear follows the sound before the tune.)
It is three against two against four: three notes, two hands, four sixteenths to the beat. The figure comes
round every beat and a half and meets the bar line every three bars: six bars are 16 turns of it exactly.
At bar 9 the line (v5) takes the next note, the A the figure would have played, and comes apart its own way,
by pitch. So the opening comes apart twice: first by sound, then by note.
MEASURED in the whole song's master: the pips peak 9.3 dB under the click's strokes; alike the two hands' spectra
centre on 551 and 554 Hz, apart on 566 and 1136 Hz. The bright hand is also 2.1 dB louder (a whole saw carries
more than its first harmonic): I did not level them, so the two lines are told apart by loudness too.

v16 (27 Nov): A FULL BEAT IS LONGER THAN AN EMPTY ONE (C11T5_FILL=0 takes it out: v15). The filled-duration
illusion: of two stretches of time that are the same length, the one with something happening in it is heard
as the longer (Thomas and Brown, 1974, and many since; with three or four small sounds in half a second the
ear adds a tenth or more). Here the two stretches are the song's own beats, as the click marks them: every
click is 480 ms after the last. Wherever the line plays (bars 9-16 and 129-136, where there is no drum to say
otherwise) the beat after each LOUD click is filled with three small dry ticks, a sixteenth apart, and the
beat after each soft click is left empty. Nothing about the click changes. If the illusion holds, the click
limps: long, short, long, short.
The ticks are on the three sixteenths between two clicks (3 4 5 and 11 12 13 of the bar), so from where the
listener stands, with the click taken for the beat, they are its "e", "and" and "a": they agree with the wrong
beat and do not give the right one away.

v17 (27 Nov): THE FIRST ONE WINS, WITH A REAL CLICK (C11T5_CRACK=0 takes it out: v16). The law of the first
wavefront is measured with clicks, and v12's small wooden click is three plain tones: it fills six of the
scorer's forty bands. Each of its 86 strokes in "held" now carries a crack as well: ten plain tones from 2.4
to 9.2 kHz, a sixth of an octave apart, all starting at nought and gone in 5 ms. There is still no noise in it,
so the two ears' cracks are the same to the sample (measured alone: alike 1.0000 at 0 and 20 ms, 0.9956 at
3 ms, where the late one falls between samples). A crack is so short that it comes apart into a click and its
echo sooner than the wooden click does: with clicks the two are heard as two from about 5 ms, and the lag
passes 5 ms at bar 111. A swept tone would have been broader still and was REFUSED: its sweep is stepped in
blocks, so the late ear's was a different sound (alike 0.30 at 3 ms): two sources, not one.

v18 (27 Nov): THE HIGH NOTE STAYS IN ONE EAR (C11T5_OCT=0 takes it out: v17). A new thing to mishear, and
the oldest of its kind: Deutsch's octave illusion (1974). Two plain notes an octave apart, A4 and A5, a note
an eighth with no gap between: the left ear is given A4 A5 A4 A5, the right A5 A4 A5 A4. So each ear is given
BOTH notes, turn about, and at every moment the two ears hold different ones. That is not what is heard. Most
people hear ONE note at a time: a high one in one ear (the right, for most right-handers), then a low one in
the other, and so on: half of what each ear was given is not heard at all, and the low note is heard in the
ear that was given the high one. Turn the headphones round and the high note stays where it was. It plays in
the first eight bars of "turned around" (the section is well named), the row before the two scales, and is
shown the way they are: the left ear's part alone for two bars (both notes are plainly there), the right's
alone for two, then both for four. Two tracks (`oct-l`, `oct-r`), an ear each and dry, one plain sine
(`ht-oct`). In one speaker it is a held octave: nothing cancels, and there is no illusion.

v19 (27 Nov): AN OCTAVE UP IS A SEMITONE DOWN (C11T5_PARA=0 takes it out: v18). Risset's paradox (1986,
after Schroeder). The song's bells have their tones an octave apart, twice from each to the next, so a
bell an octave higher is the same bell. Build one with its tones a little MORE than an octave apart, 2.1
times from each to the next, under one fixed curve as before. Now write it an octave higher: every tone is
doubled. But a tone doubled lands just UNDER the next tone of the old bell (2 against 2.1: 84.5 cents under),
and the ear, which follows each tone to its nearest neighbour, hears the whole bell step DOWN by a small
semitone. In the first row of "round the click" (bars 137-144) the bell is written D1, D2, D3 ... D8, an
octave up at every click, seven octaves in two bars, and then back down: what is heard is a chime that
walks down a tritone in seven even steps and up again. Nothing is bent and nothing is hidden: the notes
are octaves, and the arithmetic is 1200 - 1284.5.

v20 (27 Nov): A VOICE IN THE NOTE (C11T5_VOX=0 takes it out: v19). One low note is held through the
first row of "held": eighteen plain tones, the multiples of D2, each at its own steady level: a single
buzzing note, as an organ pipe is. Nothing is added to it and nothing in it gets louder. From its third
bar some of its tones begin to WAVER TOGETHER (a third of a semitone each way, five and a half times a
second): every third one, then every fourth, every sixth, every fourth, every third, every second, a bar
each. Tones that waver together are heard as one thing and apart from the ones that do not (McAdams
1984; Chowning's Phone, 1980): a second voice steps out of the note, singing the note those tones are
the multiples of: A3, D4, A4, D4, A3, D3: a tune that is not written anywhere, sung by a note that never
changes. When they stop wavering the voice goes back into the note.

v21 (27 Nov): TWO LINES CROSS, AND THE EAR WILL NOT LET THEM (C11T5_CROSS=0 takes it out: v20). In the
three pairs of bars of "never arrives" that had nothing of their own (57-58, 65-66, 73-74, before each
climb of the hat), two plain tones in one place set out for each other's notes: one from A3 straight up
to A5, the other from A5 straight down to A3, an octave a bar. They cross on A4, a bar in. Neither turns:
each is a straight line. But the ear follows what is NEAREST IN PITCH, not what goes on in a straight
line, and hears the high one come down, touch, and go back up, and the low one go up and come back
down: two turns that are not in the sound, and neither line arrives (Tougas and Bregman 1985: the
bouncing glides). The third time the rising one flutters (a tremolo twice a sixteenth): now the two can
be told apart, and it is heard to go straight through the other and arrive. The falling tone starts
where in its wave it must for the two to be in step at the crossing: they touch (3 dB up for 80 ms)
instead of cancelling.

v22 (27 Nov): A TUNE THROWN ACROSS THE OCTAVES IS NOT A TUNE (C11T5_TUNE=0 takes it out: v21). The
record's first song has a clock that chimes the quarters: the Westminster tune, which everybody knows.
Here, in the first row of "all three" (bars 161-168, which had nothing of its own), its half hour is
played three times on the song's plain pip. The first time every note has the right NAME and the wrong
octave: C6 E4 D6 G4, C5 D6 E4 C6: the tune's steps of 2 to 7 semitones are leaps of 5 to 22,
and it is not a tune: nobody knows it. The second time it is played plainly, in one octave
(C4 E4 D4 G3, C4 D4 E4 C4): the clock. The third time the SAME eight thrown notes as the first: and
now the tune is in them, because the ear knows what to listen for (Deutsch 1972, the mysterious
melody: a note's name is not enough to make a tune; its place is; but a tune you already hold can be
checked against names alone). Nothing written differs between the first time and the third (the
master delivers the same eight notes up to 2.5 dB apart).

v23 (27 Nov): A HISS THAT REPEATS (C11T5_REP=0 takes it out: v22). Noise has no rhythm. But take a
piece of noise and play it over and over and the ear finds things in it (a tick here, a swish
there) that come round, and hears a pattern: a different one for each listener, and none of it
written (Guttman and Julesz, 1963: down to once in a second or two). The row with no hat (bars 145
to 152, where the drum is on the click) is given a hiss between 3 and 7.5 kHz, in the middle, at one
level (alone: every stage within 0.1 dB of the others, its level moving 0.2 dB). For two bars it is a hiss that never repeats. Then it is a hiss of the same kind, as loud, in
the same band, that is only 6 sixteenths long (two bars), then 3 (two bars), then one and a half (a
bar): the engine's shift register, which holds 32767 steps and then begins again, clocked so that it
comes round on those lengths. Three sixteenths against the beat's four: the master moves every hiss
with the drum, once a beat, and this pattern is not once a beat. The last bar is left to the rabbit.

v24 (27 Nov): THE EAR'S OWN TONE (C11T5_OWN=0 takes it out: v23). The ear is not a straight line:
give it two tones close together and it makes others of its own, the loudest at twice the lower
less the upper (the cubic difference tone). It is made in the ear, by the two tones meeting there:
there is nothing at its frequency in the air or in the file. In the first row of "not there" (bars
81 to 88, before the drum) one plain tone is held on D7 (2349 Hz) and another slides over it from
1.1 to 1.3 times it: up 2.9 semitones in two bars. The third tone goes from 0.9 to 0.7 of the
lower: DOWN 4.4 semitones, from 2114 Hz to 1645, fading as it goes (the ear makes little of it
once the two are far apart). Four phrases: both tones in the middle and the upper one rising (the
third tone falls); then the same with an ear each, the lower left and the upper right: on
headphones no ear has both and THE THIRD TONE IS GONE (on loudspeakers both reach both ears and it
stays); then an ear each with the upper one falling; then both in the middle again and falling:
the third tone RISES into the bar where the drum comes in, a riser that nobody wrote.

v25 (27 Nov): TIME-SHRINKING (C11T5_SHRINK=0 takes it out: v24). Three strokes mark two empty
times. If the second time is the longer one, by up to about a tenth of a second, it is heard
SHORTER than it is, nearly as short as the first (Nakajima, ten Hoopen and van der Wilk, 1991);
if it is the shorter one, it is heard as it is. In the third row of "round the click" (from bar
153), where the two sixteenths before every click are empty, every click gets two small clicks
before it. For four bars they come 180 ms and 120 ms before the click: 60 ms, then 120 ms: the
click is late by a whole sixteenth of the pattern's own time and should seem to come on time.
For the next three bars the middle one is 60 ms later: 120 ms, then 60 ms: the same three
strokes, the same two times the other way round, and it should sound uneven: long, short. One
small click moves by 60 ms; nothing else. (The row's last bar is the rabbit's.)

v26 (27 Nov): THE BASS THAT FALLS FOR EVER (C11T5_GLISS=0 takes it out: v25). The song has
Shepard's tones as a hat, as stairs and as bells, each a step at a time. This is Risset's
continuous one, and it is the song's first bass under 100 Hz that is not the drum: four plain
tones an octave apart (at a bar line 27.5, 55, 110, 220 and 440 Hz: all A), all sliding down
together, an octave every two bars, under one fixed curve of loudness that is nought at 27.5
and at 440 Hz and greatest at 110. A tone that reaches the bottom has faded to nothing; a new
one has come in from nothing at the top. Every tone falls the whole time, 48 semitones in the
row by name; the curve does not move; and the sound at the end of the row is the sound at its
beginning. In the second row of "held" (bars 113 to 120), which had no drum and no bass.

v27 (27 Nov): A SWELL IS HEARD LATE (C11T5_PCEN=0 takes it out: v26). A sound's moment is
not its start (the perceptual centre). In "the wrong one again" (bars 129 to 136) the click is
alone again and is taken for the beat; the bass has no fundamental; there is no drum. Now a low
note on the bass's own note begins on every TRUE beat, where the drum falls in other rows, and
lasts two sixteenths, up to the click. For four bars it swells and stops on the click: it is
heard where it arrives, and the click is the beat. For four bars the same notes at the same
instants are struck and die away: they are heard where they begin, and the click is the off
beat. No note has moved: one shape is the other played backwards, and the beat turns round.

v28 (27 Nov): THE ACCENT THAT IS NOT THERE (C11T5_ALIKE=0 takes it out: v27). Ticks that are
all alike are not heard alike: a clock says tick, tick, tick and is heard to say tick, tock
(Bolton 1894: subjective rhythm). In the last row of "turned around" a small tick sounds on every
sixteenth. For two bars the ticks are all alike. For two bars every third one is struck twice
as hard: threes against the drum's fours. Then they are all alike again for four bars: whatever
accent is heard there (the threes going on for a while, or fours with the drum) is the ear's.
The ticks are made alike where they are heard: the master takes more from a tick that falls
with the drum or the click, and each place in the bar is given back what it loses.

v29 (27 Nov): A TUNE OF HOLES (C11T5_HOLE=0 takes it out: v28). The ear gets used to what
goes on and hears what is new (auditory enhancement). In the last row of "not there" a chord
of eight plain tones, every tone as loud as every other, sounds sixteen times, the same every
time. Before each it is heard for a beat with one tone left out; the drum falls; then the
whole chord. In the whole chord the tone that was left out stands out as a note of its own,
though it is no louder than the rest. The tones left out are the tune that is in neither ear
(bars 121 to 128), two octaves up: so a tune is heard in a chord that never changes: the
third way the song plays it without playing it.

v30 (27 Nov): THE HURRY THAT IS NOT THERE (C11T5_HURRY=0 takes it out: v29). A stair of
low notes, three to every two beats of the drum and exactly even in time, climbs for two
bars and comes down for two, twice (the middle row of "not there"). A line that rises is
judged to be speeding up, and one that falls to be slowing down, though its notes are
evenly spaced (Boltz 2011). Nothing in the time changes: only the pitch. The drum beside
it is a ruler: the ear can check.

v31 (28 Nov): THE LOUDER, THE LOWER (C11T5_HEAVY=0 takes it out: v30). In the first row
of "not there" one plain low note (E2) is played loud and soft by turns, twelve dB
apart, for four bars; then it is held for four, swelling twelve dB and sinking back.
Its frequency never moves. A plain low note is said to be heard lower the louder it is
(Stevens 1935): if it is, the turns are a tune of two notes and the swell is a bend,
and neither is written.

v32 (28 Nov): THE LONGER, THE LOUDER (C11T5_LONG=0 takes it out: v31). In bars 25 to 32
a pip follows every beat by a third of a beat: always the same note at the same height.
Only its length changes: 5, 10, 20, 40, 80 ms and back. Under about a fifth of a second
the ear adds a sound up over its length, so the same height twice as long is heard
louder: a swell and a fall every two bars, and no level moves.

v33 (28 Nov): FAR IN PITCH, FAR IN TIME (C11T5_KAPPA=0 takes it out: v32). In bars 145 to
151 three pips a bar, a beat apart: A4, a middle one, A5. The middle pip is in the middle
in time; bar by bar it is B4 (near the first) or G5 (near the last). The ear is said to
hear it nearer in time to the pip it is nearer in pitch (the kappa effect). In bars 149
and 150 it is truly moved that way by 30 ms, to be compared.

v34 (28 Nov): THE SAME SPACING, ANOTHER NOTE (C11T5_SHIFT=0 takes it out: v33). In bars 89
to 94 a pip of three plain tones, always 196 Hz apart, a third of a beat after every beat;
beat by beat all three are moved up together an eighth of that distance, and begin again
after eight. The distance never changes; the note the ear makes of the three is said to
rise a third of a semitone a step and to fall back at the fifth (the pitch shift of the
residue). In bars 95 and 96 the tune it is said to be is played plainly, an octave up.

v35 (28 Nov): THE GAP GOES TO THE OTHER ONE (C11T5_GAP=0 takes it out: v34). In bars 137
and 141 a long plain tone glides slowly up and is broken for 90 ms just where a short one
glides quickly down across it; the short one is whole. It is said to be heard the other way
round: the long glide unbroken, the hole in the short one (the gap transfer). In bars 139
and 143 it is made the way it is said to sound, to be compared.

v36 (28 Nov): AFTER THE FALL, A NOTE THAT DOES NOT MOVE (C11T5_AFTER=0 takes it out: v35).
For eight bars the bass has fallen without a break (v26). The moment it stops, in bar 121,
one plain note (E4) is held for three beats and does not move at all. After a long fall a
steady note is said to seem to rise for a moment (the waterfall illusion, in sound: Shu,
Swindale and Cynader, 1993). The same note is held again in bars 123 and 125 as the
after-effect wears off: the same note, as long and as loud. Nothing of the fall is changed.

v37 (28 Nov): THE WIDER, THE LOUDER (C11T5_SPREAD=0 takes it out: v36). In bars 59 to 64 two
pips that read the same on a meter: one plain tone (E5), and four plain tones (A4 E5 A5 E6)
each a quarter of its power. The ear adds loudness band by band, so the spread one is said
to sound louder. Two bars alike on the meter; then the spread one is really 3 dB down, then 6.

v38 (28 Nov): THE ODD ONE OUT SEEMS LONGER (C11T5_ODD=0 takes it out: v37). In bars 185 to
192 a plain note on every beat, every one held the same 300 ms. Every seventh is another
note. Nothing else about it is different.

v39 (28 Nov): TURNED OVER IN ONE EAR, THE NOTE COMES BACK (C11T5_MLD=0 takes it out: v38). Under
the hiss of "in the noise" a plain low note, the same in both ears, is turned down until the
hiss covers it. Then, no louder, the right ear's wave is turned upside down. Neither ear is
given anything it was not given before (Hirsh 1948; Licklider 1948: binaural unmasking).
"""
import json
import math
import os

OUT = os.environ.get("C11T5_OUT", os.path.join(os.path.dirname(__file__), "..", "..", "..", "songs", "chirpers11-t5.yaml"))
BPM = 125
BEATS = 4
ROW = 8
STEP = 0.25

CYCLE = ROW * BEATS            # beats in which every layer of the hat doubles its speed
LAYERS = 4
C = 23                         # the slowest layer's count at the start of a row: its speed there is C * ln 2 / CYCLE strokes a beat
QUIET = 0.04                   # strokes softer than this are left out

SHEP = os.environ.get("C11T5_SHEP", "1") != "0"      # v2: the layers' own voices, rising
SHEP_ROOT = ("A3", "A4", "A5", "A6")                  # the note each layer starts every row on
RISE = 12                                             # semitones every layer climbs in a row
HELD = os.environ.get("C11T5_HELD", "1") != "0"      # v4: the chord that does not stop
HELD_CHORD = ("A3", "C4", "E4", "G4")                 # four plain tones, 220 to 392 Hz
HELD_ON = tuple(range(0, 16, 2))                      # the sixteenths the chord sounds on; the others are its holes
HELD_BAND = (170, 560)                                # Hz: the noise that fills the holes covers the chord's notes and little else
H = {"chop": (2 * ROW, 3 * ROW), "fence": (2 * ROW, 3 * ROW)} if HELD else {}   # in "all three": its last row only, so the noise can be taken away at "out"
APART = os.environ.get("C11T5_LINE", "1") != "0" and HELD  # v5: the line comes apart
BOTH = os.environ.get("C11T5_BOTH", "1") != "0" and APART  # v6: the answer that agrees
BOTH_PAIR = ("B", "F")                                # the answer: half an octave apart, so neither way is the shorter
BOTH_UP = ("B", "C", "D")                             # what is said before it on the way up from B to F ...
BOTH_DOWN = ("B", "A", "G")                           # ... and on the way down from B to F
BOTH_MID = 440.0                                      # Hz: where the curve every one of these bells is under is loudest
BOTH_WIDE = 1.1                                       # octaves: how wide it is (the sigma of a bell curve over octaves)
BOTH_FLOOR = -45                                      # dB: octaves quieter than this under the curve are left out
BOTH_GAIN = os.environ.get("C11T5_BOTH_GAIN", "-14dB")  # the bells' level
STAIRS = os.environ.get("C11T5_STAIRS", "1") != "0" and BOTH   # v7: the stairs
STAIR = ("B", "D", "F", "Ab")                         # four bells, three semitones from each to the next, and from the last to the first
STAIR_EVERY = (4, 2)                                  # sixteenths from one step to the next, a row of "never arrives" each: a bell a beat, then two
STAIR_VEL = 0.75                                      # every step as loud as every other: the fifth bell must be the first
STAIR_GAIN = os.environ.get("C11T5_STAIR_GAIN", "-17dB")   # the stairs' level: their own tracks, on the same bells (at the answer's -14 dB they were 3 dB under everything else, and the spectrum term fell)
BOTH_IN = tuple(x for x in os.environ.get("C11T5_BOTH_IN", "turned,round").split(",") if x)   # where it is said
LINE_A = "A4"                                         # the note that never changes
LINE_B = ("A4", "C5", "E5", "A5", "A5", "E5", "C5", "A4")   # B's note in each bar of a row: with A, then a third, a fifth, an octave from it, and back
ROUND = os.environ.get("C11T5_ROUND", "1") != "0"    # v3: the drum goes round the click
HUG = os.environ.get("C11T5_HUG", "1") != "0" and HELD    # v14: the tune that is in neither ear (Huggins' pitch): a section of its own after "held"
FILL = os.environ.get("C11T5_FILL", "1") != "0" and os.environ.get("C11T5_WES", "1") != "0" and HUG    # v16: a full beat is longer than an empty one (the filled-duration illusion)
FILL_WITH = "line"                                    # it plays in every bar in which the line does: the two passages with the click, the bass and no drum
FILL_AFTER = (2, 10)                                  # sixteenths of the bar: the clicks whose beat is filled (the loud ones); the beats after the clicks on 6 and 14 are left empty
FILL_N = 3                                            # ticks in a filled beat: on each sixteenth between its click and the next
FILL_VEL = 0.7                                        # every tick alike
FILL_GAIN = os.environ.get("C11T5_FILL_GAIN", "-18dB")    # set in the WHOLE SONG's master: the ticks then peak 9 to 14 dB under the click's strokes (at -12 dB they peaked 4 to 8 under: with the click, not after it). The scorer hardly cares which (79.6 against 81.3)
FILL_PAN = 0.2                                        # a little to the right: the line and the opening's pips are a little to the left
WES = os.environ.get("C11T5_WES", "1") != "0" and HUG    # v15: the way up is two ways down (Wessel's illusion): the opening's bars 3 to 8
WES_BARS = (2, 8)                                     # bars (from 0) of the song: after the two bars under Ring True's tail, up to where the line comes in
WES_NOTES = ("A4", "C5", "E5")                        # going up; the notes the line takes when it comes apart (v5)
WES_PLAN = (2, 2, 2)                                  # bars: the two hands alike, coming apart, apart
WES_BASE = 1000.0                                     # Hz: both hands' low-pass filter when they are alike (two stages: a pip that is nearly a plain tone)
WES_OCT = float(os.environ.get("C11T5_WES_OCT", "3.5"))   # octaves the second hand's filter opens: 1000 Hz to 11.3 kHz, a plain tone to a buzz
WES_GAIN = os.environ.get("C11T5_WES_GAIN", "-19dB")  # both hands' fader, set in the WHOLE SONG's master: at the line's own -12 dB the pips peaked 2 dB under the click's strokes and carried more than the click did (the bars 5.9 dB louder than they were); 7 dB under that the click leads
HUG_ROWS = 1                                          # rows of "in the noise"
HUG_TUNE = LINE_B                                     # the notes the line takes when it comes apart (v5): A C E A, A E C A
HUG_BEATS = 2                                         # beats to a note: 0.96 s, long enough for the ears to find it
HUG_Q = float(os.environ.get("C11T5_HUG_Q", "8"))     # the all-pass filter's Q: the ears are a quarter turn apart 5% under the note and three quarters 7% over it (at 16 the place is half as wide)
HUG_BASE = 440.0                                      # Hz: the all-pass filter's own place; the lane moves it by octaves
HUG_GAIN = os.environ.get("C11T5_HUG_GAIN", "-30dB")  # the noise: set in the WHOLE SONG's master (at -34 dB it read -28 dBFS there, 12 dB under the click's strokes and 11 under the bars before it; a short window of the song read it 9 dB higher: the loudness stage gives a quiet window more)
HUG_SAID = (4, 8)                                     # the bars of the section in which the tune is also played for real, in the middle
HUG_SAID_GAIN = os.environ.get("C11T5_HUG_SAID_GAIN", "-40.5dB")   # the plain tone: in the master it reads 8 dB under all the noise it sits in (11 to 15 dB over the noise in its own 29 Hz): soft, and sure on one speaker (13 dB under the noise's fader read 12.4 dB under)
ROUND_AT = (1, 2, 3)                                  # the sixteenth of the beat the drum stands on, a row each ("all three" is 0)
ROUND_REST = 1                                        # bars at the end of each of those rows with no drum
RABBIT = os.environ.get("C11T5_RABBIT", "1") != "0" and STAIRS and ROUND    # v8: the rabbit
RAB_N = 4                                             # clicks at each of its two places
RAB_EVERY = (1, 0.5, 0.25)                            # sixteenths from click to click: the roll three times in the bar, each twice as fast, the last ending on the bar line
RAB_WAY = (1, -1, 1)                                  # row by row: left to right, back, left to right
RAB_PAN = float(os.environ.get("C11T5_RAB_PAN", "0.8"))   # how far to each side its two places are (at 1 a click is in one ear only)
RAB_GAIN = os.environ.get("C11T5_RAB_GAIN", "-18dB")   # where the master stops holding it down: at -9 and -14 dB it left the mix no louder (within 1 dB) and turned the click and the bass under it down by up to 2.1 and 0.9 dB; here 0.45
RAB_NOTE, RAB_VEL = "E6", 0.8                         # the click's own rim an octave up, every stroke as loud as every other
PULSE = os.environ.get("C11T5_PULSE", "1") != "0" and RABBIT     # v9: between the ears (a pulse that is not on the record)
PULSE_IN = ("not there", 0, 24)                           # the section, and the bars of it the two tones are held for
PULSE_NOTE = "A4"                                         # the note the two tones are either side of: neither ear is given it
PULSE_RATES = ((0, 16, float(os.environ.get("C11T5_PULSE_FIRST", "3"))), (16, 24, float(os.environ.get("C11T5_PULSE_LAST", "1.5"))))   # (from bar, to bar of the section, cycles a beat the two tones are apart): rates the drum does not have (the master ducks everything once and twice a beat)
PULSE_APART = (8, 12)                                     # bars of the section in which the two tones go from the middle to an ear each
PULSE_GAIN = float(os.environ.get("C11T5_PULSE_GAIN", "-32"))   # dB: one tone
PULSE_END = 0.5                                           # beats before the next section the tones are let go, so that "held" begins with nothing hanging over it
SCALE = os.environ.get("C11T5_SCALE", "1") != "0" and PULSE     # v10: two scales neither ear is given (the scale illusion)
SCALE_IN = ("turned around", 8, 16)                       # the section, and the bars of it in which they are played
SCALE_NOTES = ("A4", "B4", "C5", "D5", "E5", "F5", "G5", "A5")   # the scale: up it and down it at once, a note an eighth
SCALE_SOLO = 2                                            # bars the left ear's part is heard alone, then the right's; both for what is left
SCALE_GAIN = os.environ.get("C11T5_SCALE_GAIN", "-12dB")  # each ear's pips (the line's level)
FALL = os.environ.get("C11T5_FALL", "1") != "0" and SCALE and STAIRS   # v11: the way down leads up (Risset's paradox)
FALL_IN = ("all three", 8, 16)                            # the section, and the bars of it in which it is said
FALL_BELLS = ("B", "Ab", "F", "D")                        # each three semitones under the one before it, and the first three under the last
FALL_EVERY = 2                                            # sixteenths from one step down to the next
FALL_SAID = 1                                             # bars at each end in which the first bell (and at the far end the last) is said plainly
FALL_RISE = float(os.environ.get("C11T5_FALL_RISE", "1"))   # octaves the curve climbs while the bells go down
FALL_TOP = float(os.environ.get("C11T5_FALL_TOP", "0"))   # octaves over the v6 bells' curve at which it ends: 0, so the last bell is a v6 bell (at half an octave over, the song had still more around 470 Hz, where it has 7 dB more than the album already)
FALL_GAIN = os.environ.get("C11T5_FALL_GAIN", "-19dB")    # their level: 2 dB under the stairs
FALL_VEL = STAIR_VEL ** 0.6                               # ... and a stair's loudness (the bells' own patch takes velocity to the power 0.6)
ALL = None
# name, rows, {part: None (the whole section) or (from bar, to bar) of the section}
SECTIONS = [
    ("the wrong one",    2, {"tick": ALL, "bass": (8, 16), **({"line": (ROW, 2 * ROW)} if APART else {})}),
    ("turned around",    3, {"tick": ALL, "bass": ALL, "kick": ALL, "clap": (8, 24), **({"both": (2 * ROW, 3 * ROW)} if BOTH and "turned" in BOTH_IN else {})}),
    ("never arrives",    5, {"tick": ALL, "bass": ALL, "kick": ALL, "clap": ALL, "ris": ALL, "shep": (16, 40), **({"stair": (0, len(STAIR_EVERY) * ROW)} if STAIRS else {})}),
    ("not there",        3, {"tick": ALL, "bass": ALL, "ris": ALL, "kick": (8, 24), "sub": (8, 16), "clap": (16, 24)}),
] + ([("held", 2, {"tick": ALL, "chop": ALL, "fence": (ROW, 2 * ROW)})] if HELD else []) + ([("in the noise", HUG_ROWS, {"tick": ALL, "hiss": ALL, "said": HUG_SAID})] if HUG else []) + [
    ("the wrong one again", 1, {"tick": ALL, "bass": ALL, "ris": ALL, "clapx": ALL, **({"line": ALL} if APART else {})}),
] + ([("round the click", len(ROUND_AT), {"tick": ALL, "bass": ALL, **({"both": ((len(ROUND_AT) - 1) * ROW, len(ROUND_AT) * ROW)} if BOTH and "round" in BOTH_IN else {}),
                                          **{f"k{k}": (i * ROW, (i + 1) * ROW - ROUND_REST) for i, k in enumerate(ROUND_AT)},
                                          **{f"c{k}": (i * ROW + ROW // 2, (i + 1) * ROW - ROUND_REST) for i, k in enumerate(ROUND_AT)}})] if ROUND else []) + [
    ("all three",        3, {"tick": ALL, "bass": ALL, "kick": ALL, "clap": ALL, "ris": ALL, "shep": ALL, **H}),
    ("out",              3, {"tick": (0, 20), "bass": (0, 16), "kick": (0, 8), "sir": ALL, "pehs": ALL, **({"chop": (0, ROW)} if HELD else {})}),
]


def starts():
    out, b = [], 0
    for name, rows, parts in SECTIONS:
        out.append((name, b, rows * ROW, parts)); b += rows * ROW
    return out, b


SECS, BARS = starts()
TOTAL = BARS * BEATS


def plays(part, bar):
    for name, b0, n, parts in SECS:
        if b0 <= bar < b0 + n:
            if part not in parts:
                return False
            w = parts[part]
            return w is None or w[0] <= bar - b0 < w[1]
    return False


def rabbit():
    """The rabbit: (the beat of each click, its side: -1 left, 1 right), in the bar of rest at the end of each row of "round the click"."""
    out = []
    sec = next((x for x in SECS if x[0] == "round the click"), None)
    if not RABBIT or sec is None or not ROUND_REST:
        return out
    for i in range(len(ROUND_AT)):
        bar = sec[1] + (i + 1) * ROW - ROUND_REST
        s = 16 * ROUND_REST - sum(2 * RAB_N * e for e in RAB_EVERY)      # the sixteenth the first roll starts on, so that the last ends on the bar line
        for e in RAB_EVERY:
            out += [(bar * BEATS + (s + k * e) * STEP, RAB_WAY[i % len(RAB_WAY)] * (-1 if k < RAB_N else 1)) for k in range(2 * RAB_N)]
            s += 2 * RAB_N * e
    return out


def pulse_span():
    """The beats between which the two tones are held, or None."""
    sec = next((x for x in SECS if x[0] == PULSE_IN[0]), None) if PULSE else None
    return ((sec[1] + PULSE_IN[1]) * BEATS, (sec[1] + PULSE_IN[2]) * BEATS) if sec else None


def pulse_ratio(rate, side):
    """What the tone in one ear (-1 left, 1 right) is of PULSE_NOTE: the two are `rate` cycles a beat apart and the note is half way between."""
    return 1 + side * rate * BPM / 60 / 2 / hz(PULSE_NOTE)


def pulse_apart(t):
    """How far apart the two tones are at beat t: 0 both in the middle, 1 an ear each."""
    lo = pulse_span()[0]
    a, b = lo + PULSE_APART[0] * BEATS, lo + PULSE_APART[1] * BEATS
    return min(1.0, max(0.0, (t - a) / (b - a)))


def pulse_lift(p):
    """dB that keep an ear as loud as it was while the other ear's tone leaves it: at p it has 1 + (1 - p)^2 of one tone's power."""
    return -10 * math.log10((1 + (1 - p) ** 2) / 2)


def pulse_lanes():
    lo = pulse_span()[0]
    a, b = lo + PULSE_APART[0] * BEATS, lo + PULSE_APART[1] * BEATS
    ts = [a + i * STEP for i in range(int(round((b - a) / STEP)) + 1)]
    return ([["0b", 0]] + [[f"{t:g}b", round(pulse_apart(t), 4)] for t in ts] + [[f"{TOTAL:g}b", 1]],
            [["0b", 0]] + [[f"{t:g}b", round(pulse_lift(pulse_apart(t)), 3)] for t in ts] + [[f"{TOTAL:g}b", round(pulse_lift(1), 3)]])


def scale_span():
    """The bars between which the two scales are played, or None."""
    sec = next((x for x in SECS if x[0] == SCALE_IN[0]), None) if SCALE else None
    return (sec[1] + SCALE_IN[1], sec[1] + SCALE_IN[2]) if sec else None


def oct_span():
    """The bars between which the two notes change ears, or None."""
    sec = next((x for x in SECS if x[0] == OCT_IN[0]), None) if OCT else None
    return (sec[1] + OCT_IN[1], sec[1] + OCT_IN[2]) if sec else None


def oct_ear(side):
    """What one ear (-1 left, 1 right) is given in a bar, a note an eighth: the left begins on the low note, the right on the high."""
    return [OCT_NOTES[(i + (0 if side < 0 else 1)) % 2] for i in range(2 * BEATS)]


def oct_notes(side):
    b0, b1 = oct_span()
    first = b0 + (0 if side < 0 else OCT_SOLO)              # as the scales are shown: the left ear's part begins the row, the right's OCT_SOLO bars later
    bars = [b for b in range(b0, b1) if b >= first and not (side < 0 and b0 + OCT_SOLO <= b < b0 + 2 * OCT_SOLO)]
    return [note(b * BEATS + i * 2 * STEP, p, 2 * STEP, 0.8) for b in bars for i, p in enumerate(oct_ear(side))]


def scale_ear(side):
    """What one ear (-1 left, 1 right) is given in a bar: of the rising scale and the falling one, the notes that are dealt to it, turn about."""
    up, down = SCALE_NOTES, SCALE_NOTES[::-1]
    return [(up if (i % 2 == 0) == (side < 0) else down)[i] for i in range(len(SCALE_NOTES))]


def scale_notes(side):
    b0, b1 = scale_span()
    first = b0 + (0 if side < 0 else SCALE_SOLO)            # the left ear's part begins the row, the right's SCALE_SOLO bars later
    bars = [b for b in range(b0, b1) if b >= first and not (side < 0 and b0 + SCALE_SOLO <= b < b0 + 2 * SCALE_SOLO)]
    return [note(b * BEATS + i * 2 * STEP, p, 2 * STEP, 0.8) for b in bars for i, p in enumerate(scale_ear(side))]


def note(at, pitch, length, vel):
    return {"at": round(at, 4), "len": round(length, 4), "pitch": pitch, "vel": round(vel, 3)}


def fill_notes(bars):
    """FILL_N ticks, a sixteenth apart, after each click in FILL_AFTER, in every given bar (from 0)."""
    return [{"at": b * BEATS + (c + k) * STEP, "len": 0.1, "pitch": "C6", "vel": FILL_VEL} for b in bars for c in FILL_AFTER for k in range(1, FILL_N + 1)]


def wes_notes(hand):
    """The figure's notes for one hand (0: the even sixteenths, 1: the odd): WES_NOTES going up, a sixteenth each, shared out turn about."""
    n0, n1 = int(WES_BARS[0] * BEATS / STEP), int(WES_BARS[1] * BEATS / STEP)
    return [note(n * STEP, WES_NOTES[(n - n0) % len(WES_NOTES)], 0.8 * STEP, 0.8) for n in range(n0, n1) if (n - n0) % 2 == hand]


def wes_lane(hand):
    """How far apart the hand's sound is from the other's (0 alike, 1 apart), as lane points in beats."""
    b = [WES_BARS[0] * BEATS]
    for k in WES_PLAN:
        b.append(b[-1] + k * BEATS)
    top = 1.0 if hand else 0.0
    return {"points": [["0b", 0.0], [f"{b[1]:g}b", 0.0], [f"{b[2]:g}b", top], [f"{b[3]:g}b", top], [f"{b[3] + BEATS:g}b", 0.0]], "curve": 0}


def part(name, steps):
    out = []
    for bar in range(BARS):
        if plays(name, bar):
            out += [note(bar * BEATS + s * STEP, p, n * STEP, v) for s, p, n, v in steps(bar)]
    return out


def risset(back=False):
    """One row of the hat: (beat in the row, velocity). Stroke n of the finest layer falls at CYCLE * log2(n / n0);
    it belongs to every layer whose count it divides into, and its loudness is the sum of their windows."""
    n0 = C * 2 ** (LAYERS - 1)
    out = []
    for n in range(n0, 2 * n0):
        t = CYCLE * math.log2(n / n0)
        amp = sum(math.sin(math.pi * (t / CYCLE + j) / LAYERS) ** 2 for j in range(LAYERS) if n % 2 ** (LAYERS - 1 - j) == 0)
        v = amp / (LAYERS / 2)
        if v >= QUIET:
            out.append(((CYCLE - t) % CYCLE if back else t, v))
    return sorted(out)


def ris_notes(name, back=False):
    row, out = risset(back), []
    for r in range(BARS // ROW):
        if plays(name, r * ROW):
            out += [note(r * CYCLE + t, "A5", 0.1, v) for t, v in row]
    return out


def layer(j, back=False):
    """One row of layer j alone: (beat in the row, velocity). Its own strokes and its own window, nothing summed."""
    n0, out = C * 2 ** j, []
    for n in range(n0, 2 * n0):
        t = CYCLE * math.log2(n / n0)
        v = math.sin(math.pi * (t / CYCLE + j) / LAYERS) ** 2
        if v >= QUIET:
            out.append(((CYCLE - t) % CYCLE if back else t, v))
    return sorted(out)


def shep_notes(j):
    out = []
    for name, back in (("shep", False), ("pehs", True)):
        row = layer(j, back)
        for r in range(BARS // ROW):
            if plays(name, r * ROW):
                out += [note(r * CYCLE + t, SHEP_ROOT[j], 0.2, v) for t, v in row]
    return sorted(out, key=lambda n: n["at"])


def rise_lane():
    """Semitones every layer's voice is above its root: 0 to RISE through each row it plays (RISE to 0 backwards)."""
    pts = [["0b", 0]]
    for r in range(BARS // ROW):
        for name, lo, hi in (("shep", 0, RISE), ("pehs", RISE, 0)):
            if plays(name, r * ROW):
                pts += [[f"{r * CYCLE:g}b", lo], [f"{(r + 1) * CYCLE - 0.01:g}b", hi]]
    pts.append([f"{TOTAL:g}b", 0])
    return pts


OFF = (2, 6, 10, 14)           # where the click and the bass are from the first bar to the last
TICK = lambda bar: [(s, "E5", 1, 0.9 if s in (2, 10) else 0.78) for s in OFF]
LINE = [("A1", "A1", "A1", "C2"), ("A1", "A1", "A1", "A1"), ("A1", "A1", "A1", "D2"), ("A1", "A1", "E2", "G1")]
BASS = lambda bar: [(s, p, 1.5, 0.9 if s in (2, 10) else 0.8) for s, p in zip(OFF, LINE[bar % 4])]
KICK = lambda bar: [(s, "A1", 1, 0.95 if s == 0 else 0.9) for s in (0, 4, 8, 12)]
CLAP = lambda bar: [(4, "C4", 1, 0.8), (12, "C4", 1, 0.86)]      # two and four
def hz(p):
    semi = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[p[0]] + (-1 if "b" in p[1:] else 1 if "#" in p else 0) + 12 * (int(p[-1]) + 1)
    return 440.0 * 2 ** ((semi - 69) / 12)


def para_tones(p):
    """The tones of the paradox bell written on note p: (ratio to the written note, Hz, dB under the curve): PARA_APART times from each to the next."""
    out = []
    for k in range(-12, 13):
        f = hz(p) * PARA_APART ** k
        level = -20 * math.log10(math.e) * math.log2(f / PARA_MID) ** 2 / (2 * PARA_WIDE ** 2)
        if level >= PARA_FLOOR:
            out.append((PARA_APART ** k, f, level))
    return out


def mld_row():
    """The first bar (from 0) of the row in which a note comes back when one ear is turned over, or None."""
    sec = next((x for x in SECS if x[0] == MLD_IN[0]), None)
    return sec[1] + ROW * MLD_IN[1] if MLD and sec is not None and MLD_IN[1] * ROW < sec[2] else None


def mld_notes():
    """[(note from 0, beat of the song, dB under the first, True if the right ear's is upside down)]."""
    b0 = mld_row() * BEATS; assert len(MLD_AT) == len(MLD_DOWN) == len(MLD_TURNED) == len(MLD_TRIM) and all(b < ROW and q + MLD_LEN <= BEATS for b, q in MLD_AT)
    return [(i, b0 + b * BEATS + q, MLD_DOWN[i], bool(MLD_TURNED[i])) for i, (b, q) in enumerate(MLD_AT)]


def odd_row():
    """The first bar (from 0) of the row in which the odd one out seems longer, or None."""
    sec = next((x for x in SECS if x[0] == ODD_IN[0]), None)
    return sec[1] + ROW * ODD_IN[1] if ODD and sec is not None and ODD_IN[1] * ROW < sec[2] else None


def odd_notes():
    """[(note from 0, beat of the song, True if it is the odd one)]: a note a beat for ROW bars."""
    b0 = odd_row() * BEATS; n = ROW * BEATS; assert len(ODD_TRIM) == n and ODD_AT + ODD_LEN < 1
    return [(i, b0 + i + ODD_AT, i >= ODD_FIRST and (i - ODD_FIRST) % ODD_EVERY == 0) for i in range(n)]


def spread_row():
    """The first bar (from 0) of the row in which the wider is the louder, or None."""
    sec = next((x for x in SECS if x[0] == SPREAD_IN[0]), None)
    return sec[1] + ROW * SPREAD_IN[1] if SPREAD and sec is not None and SPREAD_IN[1] * ROW < sec[2] else None


def spread_pips():
    """[(pip from 0, beat of the song, True for the four tones, dB it is really turned down)]: SPREAD_AT in every bar from bar SPREAD_FROM of the row; two bars to a step of SPREAD_DOWN; in a step's first bar the one tone comes first, in its second the four."""
    b0 = (spread_row() + SPREAD_FROM) * BEATS; n = len(SPREAD_AT); assert n == 2 and (ROW - SPREAD_FROM) == 2 * len(SPREAD_DOWN)
    return [(i, b0 + (i // n) * BEATS + SPREAD_AT[i % n], (i % n == 1) == ((i // n) % 2 == 0), SPREAD_DOWN[i // n // 2] if (i % n == 1) == ((i // n) % 2 == 0) else 0) for i in range((ROW - SPREAD_FROM) * n)]


def after_notes():
    """[the beat each held note begins on] after the row of the bass that falls for ever; [] without."""
    r = gliss_row()
    return [float((r + ROW + b) * BEATS) for b in AFTER_BARS if r + ROW + b < BARS] if AFTER and r is not None else []


def after_lane():
    """The track's lane (dB): AFTER_FLAT through each note, a point at the middle of each of its places and one at each end, a straight line between."""
    n = len(AFTER_FLAT) // (len(AFTER_BARS) * AFTER_BEATS); m = AFTER_BEATS * n; pts = [["0b", AFTER_FLAT[0]]]
    for k, at in enumerate(after_notes()):
        pts.append([f"{at:g}b", AFTER_FLAT[k * m]])
        pts += [[f"{at + (j + 0.5) / n:.4f}b", AFTER_FLAT[k * m + j]] for j in range(m)]
        pts.append([f"{at + AFTER_BEATS + 0.25:g}b", AFTER_FLAT[k * m + m - 1]])
    return pts


def gap_row():
    """The first bar (from 0) of the row in which the gap goes to the other glide, or None."""
    sec = next((x for x in SECS if x[0] == GAP_IN[0]), None)
    return sec[1] + ROW * GAP_IN[1] if GAP and sec is not None and GAP_IN[1] * ROW < sec[2] else None


def gap_figs():
    """[(bar (from 0), which glide is broken, the long glide's (from beat, to beat), the short one's, the break's)]: beats of the song."""
    out = []
    for b, kind in zip(GAP_BARS, GAP_KIND):
        b0 = (gap_row() + b) * BEATS; l0, l1 = b0 + GAP_LONG[0], b0 + GAP_LONG[1]; c = (l0 + l1) / 2; g = GAP_MS / 1000 * BPM / 60
        out.append((gap_row() + b, kind, (l0, l1), (c - GAP_SHORT[0] / 2, c + GAP_SHORT[0] / 2), (c - g / 2, c + g / 2)))
    return out


def gap_lane(which):
    """The lane of one glide's track: semitones from GAP_NOTE, a straight line through each glide, a step between."""
    from math import log2
    mid = 12 * log2((GAP_LONG[2] * GAP_LONG[3]) ** 0.5 / hz(GAP_NOTE))
    p0, p1 = (12 * log2(GAP_LONG[2] / hz(GAP_NOTE)), 12 * log2(GAP_LONG[3] / hz(GAP_NOTE))) if which == "long" else (mid + GAP_SHORT[1] / 2, mid - GAP_SHORT[1] / 2)
    pts = [["0b", round(p0, 4)]]; last = p0
    for _, _, lg, sh, _ in gap_figs():
        a, b = lg if which == "long" else sh
        pts += [[f"{a - 0.001:.3f}b", round(last, 4)], [f"{a:.3f}b", round(p0, 4)], [f"{b:.3f}b", round(p1, 4)]]; last = p1
    return pts


def shift_row():
    """The first bar (from 0) of the row with the same spacing, another note, or None."""
    sec = next((x for x in SECS if x[0] == SHIFT_IN[0]), None)
    return sec[1] + ROW * SHIFT_IN[1] if SHIFT and sec is not None and SHIFT_IN[1] * ROW < sec[2] else None


def shift_said(k):
    """Cents from the note that step k is said to be heard at: the middle tone over the nearest whole number (the upper one at the half)."""
    from math import log2, floor
    c = SHIFT_RANKS[1] + k / SHIFT_STEPS
    return 1200 * log2(c / floor(c + 0.5))


def shift_pips():
    """[(beat it begins, step (from 0), turn (from 0), "three tones" or "plain")]: one a beat through the row."""
    assert sum(SHIFT_TURNS) * SHIFT_STEPS == ROW * BEATS
    return [(round(shift_row() * BEATS + j + SHIFT_AT[0] / SHIFT_AT[1], 7), j % SHIFT_STEPS, j // SHIFT_STEPS, "three tones" if j // SHIFT_STEPS < SHIFT_TURNS[0] else "plain") for j in range(ROW * BEATS)]


def kappa_row():
    """The first bar (from 0) of the row with far in pitch, far in time, or None."""
    sec = next((x for x in SECS if x[0] == KAPPA_IN[0]), None)
    return sec[1] + ROW * KAPPA_IN[1] if KAPPA and sec is not None and KAPPA_IN[1] * ROW < sec[2] else None


def kappa_pips():
    """[(beat it begins, note, "first" / "near the first" / "near the last" / "last", how far it is truly moved, in beats)]: three a bar."""
    out = []
    for j in range(KAPPA_BARS):
        b = (kappa_row() + j) * BEATS; near = j % 2; by = (KAPPA_BY if near else -KAPPA_BY) if j in KAPPA_TRUE else 0.0
        out += [(float(b + KAPPA_AT[0]), KAPPA_ENDS[0], "first", 0.0), (round(b + KAPPA_AT[1] + by, 7), KAPPA_MID[near], "near the last" if near else "near the first", by), (float(b + KAPPA_AT[2]), KAPPA_ENDS[1], "last", 0.0)]
    return out


def long_row():
    """The first bar (from 0) of the row with the longer, the louder, or None."""
    sec = next((x for x in SECS if x[0] == LONG_IN[0]), None)
    return sec[1] + ROW * LONG_IN[1] if LONG and sec is not None else None


def long_pips():
    """[(beat it begins, ms long)]: one pip a beat through the row, LONG_AT of a beat after the beat."""
    return [(round(long_row() * BEATS + k + LONG_AT[0] / LONG_AT[1], 7), LONG_MS[k % len(LONG_MS)]) for k in range(ROW * BEATS)]


def heavy_row():
    """The first bar (from 0) of the row with the note that is loud and soft, or None."""
    sec = next((x for x in SECS if x[0] == HEAVY_IN[0]), None)
    return sec[1] + ROW * HEAVY_IN[1] if HEAVY and sec is not None and HEAVY_IN[1] * ROW < sec[2] else None


def heavy_notes():
    """The turns: (beat, beats held, "loud" or "soft"); and the swell: (beat, beats held)."""
    b0 = heavy_row() * BEATS
    turns = [(b0 + k * HEAVY_EVERY, HEAVY_LEN, ("loud", "soft")[k % 2]) for k in range(HEAVY_TURNS * BEATS // HEAVY_EVERY)]
    return turns, (b0 + HEAVY_TURNS * BEATS, (ROW - HEAVY_TURNS) * BEATS - (HEAVY_EVERY - HEAVY_LEN))


def hurry_row():
    """The first bar (from 0) of the row with the even stair, or None."""
    sec = next((x for x in SECS if x[0] == HURRY_IN[0]), None)
    return sec[1] + ROW * HURRY_IN[1] if HURRY and sec is not None and HURRY_IN[1] * ROW < sec[2] else None


def hurry_notes():
    """[(beat, note, 'up' or 'down', place in the beat 0..2)]: one note every HURRY_STEP beats from HURRY_AT of the row, climbing and descending by turns."""
    n = round(ROW * BEATS / HURRY_STEP); out = []
    assert abs(n * HURRY_STEP - ROW * BEATS) < 1e-9 and n % (2 * HURRY_RUN) == 0 and len(HURRY_LADDER) == HURRY_RUN + 1
    for k in range(n):
        up = (k // HURRY_RUN) % 2 == 0; j = k % HURRY_RUN
        out.append((round(hurry_row() * BEATS + HURRY_AT + k * HURRY_STEP, 5), HURRY_LADDER[j] if up else HURRY_LADDER[HURRY_RUN - j], "up" if up else "down", k % 3))
    return out


def hole_row():
    """The first bar (from 0) of the row with the tune of holes, or None."""
    sec = next((x for x in SECS if x[0] == HOLE_IN[0]), None)
    return sec[1] + ROW * HOLE_IN[1] if HOLE and sec is not None and HOLE_IN[1] * ROW < sec[2] else None


def hole_tune():
    """The tune's notes, one for every HOLE_BEATS beats of the row: the tune that is in neither ear (HUG_TUNE), HOLE_UP octaves up, round and round."""
    n = ROW * BEATS // HOLE_BEATS
    out = [f"{p[:-1]}{int(p[-1]) + HOLE_UP}" for p in (HUG_TUNE[k % len(HUG_TUNE)] for k in range(n))]
    assert all(p in HOLE_CHORD for p in out), out
    return out


def hole_notes():
    """(the chords with a hole, the whole chords), each [(beat, length, note)]: for every note of the tune the chord without it, then the whole chord."""
    pre, full = [], []
    for k, miss in enumerate(hole_tune()):
        t = hole_row() * BEATS + k * HOLE_BEATS
        pre += [(t + HOLE_PRE[0], HOLE_PRE[1], p) for p in HOLE_CHORD if p != miss]
        full += [(t + HOLE_FULL[0], HOLE_FULL[1], p) for p in HOLE_CHORD]
    return pre, full


def alike_row():
    """The first bar (from 0) of the row with the ticks that are all alike, or None."""
    sec = next((x for x in SECS if x[0] == ALIKE_IN[0]), None)
    return sec[1] + ROW * ALIKE_IN[1] if ALIKE and sec is not None and ALIKE_IN[1] * ROW < sec[2] else None


def alike_ticks():
    """(every tick, the ones struck twice), each [(beat, velocity)]: a tick on every sixteenth of the row; in the bars ALIKE_FORM says, every n-th one (counted from the first tick of those bars) is on the second list too."""
    assert sum(b for b, _ in ALIKE_FORM) == ROW and len(ALIKE_TRIM) == BEATS * 4
    every, twice, bar = [], [], alike_row()
    for bars, n in ALIKE_FORM:
        for k in range(bars * BEATS * 4):
            t = bar * BEATS + k * STEP; v = round(ALIKE_VEL * 10 ** (ALIKE_TRIM[k % (BEATS * 4)] / 40), 4)
            assert 0 < v <= 1
            every.append((t, v))
            if n and k % n == 0:
                twice.append((t, v))
        bar += bars
    return every, twice


def pcen_row():
    """The first bar (from 0) of the row with the swell, or None."""
    sec = next((x for x in SECS if x[0] == PCEN_IN[0]), None)
    return sec[1] + ROW * PCEN_IN[1] if PCEN and sec is not None and PCEN_IN[1] * ROW < sec[2] else None


def pcen_notes():
    """(swelling, struck), each [(beat, note)]: a note before every note of the bass (BASS: on the click), PCEN_LEN beats before it and on its note; the first PCEN_BARS[0] bars of the row swell, the next PCEN_BARS[1] are struck. song() checks them against the bass's track."""
    out = ([], [])
    for j in range(sum(PCEN_BARS)):
        bar = pcen_row() + j
        for s16, p, _, _ in BASS(bar):
            out[0 if j < PCEN_BARS[0] else 1].append((round(bar * BEATS + s16 * STEP - PCEN_LEN, 5), p))
    return out


def pcen_lane(notes, swell):
    """One track's loudness lane, [(beats, dB)]: over each note a straight line in dB, PCEN_FALL dB long: up to nought for a swell, down from nought for a struck note."""
    lo, hi = (-PCEN_FALL, 0.0) if swell else (0.0, -PCEN_FALL)
    pts = [[0.0, lo]]
    for t, _ in notes:
        pts += [[t, lo], [t + PCEN_LEN, hi]]
    return pts


def pcen_middle(swell):
    """ms from a note's start to the middle of its energy (half before, half after... its centre of gravity) for the written line."""
    T = PCEN_LEN * 60000 / BPM; c = PCEN_FALL * math.log(10) / (10 * T)
    m = 1 / c - T * math.exp(-c * T) / (1 - math.exp(-c * T))
    return T - m if swell else m


def gliss_row():
    """The first bar of the row with the bass that falls for ever, or None."""
    sec = next((x for x in SECS if x[0] == GLISS_IN[0]), None)
    return sec[1] + ROW * GLISS_IN[1] if GLISS and sec is not None and GLISS_IN[1] * ROW < sec[2] else None


def gliss_legs(k):
    """Tone k's legs in the row: (beat of the row it starts, beat it ends, octaves over GLISS_LOW at its start, at its end). It falls an octave every GLISS_PER bars; at the bottom (silent) it starts again from the top (silent)."""
    per, end, out = GLISS_PER * BEATS, ROW * BEATS, []
    t, p = 0.0, float(k + 1)
    while t < end - 1e-9:
        t1 = min(end, t + p * per)
        out.append((t, t1, p, p - (t1 - t) / per))
        t, p = t1, float(GLISS_OCTAVES)
    return out


def gliss_height(k, t):
    """Octaves over GLISS_LOW of tone k at beat t of the row."""
    for t0, t1, p0, p1 in gliss_legs(k):
        if t0 <= t <= t1:
            return p0 + (p1 - p0) * (t - t0) / (t1 - t0)
    raise ValueError(t)


def gliss_db(p, t):
    """dB of a tone p octaves up the curve at beat t of the row: the curve (a raised cosine over GLISS_OCTAVES, nought at both ends) and the row's own coming in and going out."""
    a = 0.5 - 0.5 * math.cos(2 * math.pi * p / GLISS_OCTAVES)
    end = ROW * BEATS
    a *= math.sin(math.pi / 2 * min(1.0, t / GLISS_FADE[0])) ** 2 * math.sin(math.pi / 2 * min(1.0, (end - t) / GLISS_FADE[1])) ** 2
    return max(GLISS_FLOOR, 20 * math.log10(a)) if a > 0 else GLISS_FLOOR


def shrink_row():
    """The first bar of the row with the two small clicks before every click, or None."""
    sec = next((x for x in SECS if x[0] == SHRINK_IN[0]), None)
    return sec[1] + ROW * SHRINK_IN[1] if SHRINK and sec is not None and SHRINK_IN[1] * ROW < sec[2] else None


def shrink_clicks():
    """One tuple a small click: (bar from 0, the beat it is on, which of the two it is (0 first, 1 second), the sixteenth of its beat)."""
    out, bar = [], shrink_row()
    for second, bars in SHRINK_SECOND:
        for _ in range(bars):
            for beat in range(BEATS):
                out.append((bar, bar * BEATS + beat + SHRINK_FIRST * STEP, 0, SHRINK_FIRST))      # the beat it is HEARD on: it is written SHRINK_EARLY before
                out.append((bar, bar * BEATS + beat + second * STEP, 1, second))
            bar += 1
    return out


def own_row():
    """The first bar of the row with the ear's own tone, or None."""
    sec = next((x for x in SECS if x[0] == OWN_IN[0]), None)
    return sec[1] + ROW * OWN_IN[1] if OWN and sec is not None and OWN_IN[1] * ROW < sec[2] else None


def own_phrases():
    """One tuple a phrase: (where, way, the beat it starts on, its length in beats, the upper tone's semitones over the lower at its start and at its end)."""
    b0, per = own_row(), ROW // len(OWN_PHRASES)
    lo, hi = (12 * math.log2(r) for r in OWN_RATIO)
    return [(where, way, (b0 + j * per) * BEATS, per * BEATS - OWN_GAP, lo if way > 0 else hi, hi if way > 0 else lo) for j, (where, way) in enumerate(OWN_PHRASES)]


def own_third(st):
    """The third tone's frequency (Hz) when the upper tone is st semitones over the lower: twice the lower less the upper."""
    return hz(OWN_LOW) * (2 - 2 ** (st / 12))


def rep_row():
    """The first bar of the row with the hiss that repeats, or None."""
    sec = next((x for x in SECS if x[0] == REP_IN[0]), None)
    return sec[1] + ROW * REP_IN[1] if REP and sec is not None and REP_IN[1] * ROW < sec[2] else None


def rep_hz(sixteenths):
    """The note (Hz) at which the register comes round every `sixteenths`: REP_STEPS steps, 93 to a turn."""
    return REP_STEPS / (93 * sixteenths * STEP * 60 / BPM)


def rep_note(sixteenths):
    """(the nearest note's name, semitones from it) for rep_hz: the name is the note written, the rest is the patch's pitch."""
    m = 69 + 12 * math.log2(rep_hz(sixteenths) / 440); k = round(m)
    return ("C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B")[k % 12] + str(k // 12 - 1), m - k


def tune_row():
    """The first bar of the row with the tune thrown across the octaves, or None."""
    sec = next((x for x in SECS if x[0] == TUNE_IN[0]), None)
    return sec[1] + ROW * TUNE_IN[1] if TUNE and sec is not None and TUNE_IN[1] * ROW < sec[2] else None


def tune_notes():
    """[(beat from the row's line, the note, thrown?, which of the eight)]."""
    out = []
    for start, thrown in TUNE_PHASES:
        for c, change in enumerate(TUNE_CHANGES):
            for j, d in enumerate(change):
                i = c * len(change) + j
                octave = TUNE_SCAT[i] if thrown else TUNE_PLAIN - (1 if d == 5 else 0)
                out.append((start + (c * (len(change) - 1 + TUNE_LAST) + j) * TUNE_STEP / 4, f"{TUNE_NOTES[d]}{octave}", thrown, i))
    assert all(a != b for a, b in zip(TUNE_SCAT, TUNE_SCAT[1:])), "two neighbours thrown to one octave"
    assert max(t for t, _, _, _ in out) < ROW * BEATS
    return out


def tune_midi(name):
    return {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[name[0]] + 12 * (int(name[-1]) + 1)


def cross_spans():
    """[(the beat a crossing begins on, the beat it ends on, are the two told apart?)]; [] without."""
    return [(b * BEATS, (b + CROSS_LEN) * BEATS, told) for b, told in zip(CROSS_BARS, CROSS_TOLD)] if CROSS else []


def cross_lane(way, told):
    """The pitch lane of one tone (semitones from its written note; way +1 up, -1 down) over the crossings in which it plays: a straight line from nought to CROSS_OCT octaves, held a beat for the tone to die away."""
    pts = [["0b", 0]]
    for b0, b1, t in cross_spans():
        if told is None or t == told:
            pts += [[f"{b0:g}b", 0], [f"{b1:g}b", way * 12 * CROSS_OCT], [f"{b1 + 1:g}b", way * 12 * CROSS_OCT]]
    return pts


def vox_span():
    """The bars (from 0) between which the held note sounds, or None."""
    sec = next((x for x in SECS if x[0] == VOX_IN[0]), None) if VOX else None
    return (sec[1] + VOX_IN[1], sec[1] + VOX_IN[2]) if sec else None


def vox_plan():
    """[(first beat, last beat, n)]: the bars in which every n-th tone of the note wavers."""
    b0, b1 = vox_span()
    return [((b0 + VOX_ALONE + i) * BEATS, (b0 + VOX_ALONE + i + 1) * BEATS, n) for i, n in enumerate(VOX_TUNE) if b0 + VOX_ALONE + i < b1]


def vox_lane(k):
    """The pitch lane of tone k, in semitones: nought, but for the bars in which k is one of the tones that waver: VOX_DEEP each way, VOX_RATE times a second, in and out over VOX_EDGE beats. Every tone that wavers in a bar is given the same lane: that is what makes them one voice."""
    pts = [["0b", 0.0]]; step = BPM / 60 / (VOX_RATE * 16)                      # sixteen points to a waver, in beats
    for lo, hi, n in vox_plan():
        if k % n:
            continue
        m = int((hi - lo) / step)
        for j in range(m + 1):
            b = lo + j * step; edge = min(1.0, (b - lo) / VOX_EDGE, (hi - b) / VOX_EDGE)
            pts.append([f"{b:.5f}b", round(VOX_DEEP * max(0.0, edge) * math.sin(2 * math.pi * VOX_RATE * (b - lo) * 60 / BPM), 4)])
        pts.append([f"{hi:.5f}b", 0.0])
    return pts


def para_span():
    """The bars (from 0) between which the paradox bell plays, or None."""
    sec = next((x for x in SECS if x[0] == PARA_IN[0]), None) if PARA else None
    return (sec[1] + PARA_IN[1], sec[1] + PARA_IN[2]) if sec else None


def para_strokes():
    """(beat, index into PARA_NOTES) of every stroke: up the written octaves and back down, a bell at every click."""
    b0, b1 = para_span(); n = len(PARA_NOTES); out = []
    for q, (b, st) in enumerate((b, st) for b in range(b0, b1) for st in PARA_STEPS):
        r = q % (2 * n); out.append((b * BEATS + st * STEP, r if r < n else 2 * n - 1 - r))
    return out


def both_octaves(pc):
    """The octaves of a note-name that sound in its bell: (ratio to the note in octave 3, Hz, dB under the curve)."""
    out = []
    for k in range(-4, 7):
        f = hz(pc + "3") * 2.0 ** k
        level = -20 * math.log10(math.e) * math.log2(f / BOTH_MID) ** 2 / (2 * BOTH_WIDE ** 2)
        if level >= BOTH_FLOOR:
            out.append((2.0 ** k, f, level))
    return out


def STAIR_STEPS(bar):
    """The stairs: a bell on the click's first stroke of the row and on every STAIR_EVERY sixteenths after it, round the four."""
    b0 = next(b for nm, b, n, parts in SECS if "stair" in parts)
    row, k = divmod(bar - b0, ROW)
    every = STAIR_EVERY[row]
    return [(st, STAIR[(q // every) % len(STAIR)], min(every, 3), STAIR_VEL)
            for st in range(16) for q in [k * 16 + st - OFF[0]] if q >= 0 and q % every == 0]


CRACK = os.environ.get("C11T5_CRACK", "1") != "0" and os.environ.get("C11T5_FILL", "1") != "0" and os.environ.get("C11T5_FIRST", "1") != "0"    # v17: the first one wins, with a real click
CRACK_FROM = 4.6                                          # the lowest of its tones, as a multiple of the note (C5: 2.4 kHz): over the click's own two notes, where this song already reads over the album
CRACK_STEP = 1.16                                         # each tone this much above the last: a sixth of an octave, one of the scorer's bands
CRACK_TONES = 10                                          # 2.4 to 9.2 kHz
CRACK_TILT = 0.5                                          # dB quieter, tone by tone
CRACK_DECAY = "5ms"
CRACK_GAIN = os.environ.get("C11T5_CRACK_GAIN", "-14dB")             # set in the whole song's master: 5.8 dB under the wooden click's peak; at -8 dB it was 1.5 under and took 1.2 dB off the rest
OCT = os.environ.get("C11T5_OCT", "1") != "0" and CRACK    # v18: the high note stays in one ear (Deutsch's octave illusion)
OCT_IN = ("turned around", 0, 8)                          # the section, and the bars of it: the row before the two scales
OCT_NOTES = ("A4", "A5")                                  # the two notes: the low one and its octave (the ends of the scale that follows)
OCT_SOLO = 2                                              # bars the left ear's part is heard alone, then the right's; both for what is left
OCT_GAIN = os.environ.get("C11T5_OCT_GAIN", "-34dB")      # each ear's tone, set in the whole song's master (which reads a held tone 8.7 dB over this figure here): as much sound as the scales' pips that follow. At -26 dB it was 6 dB under ALL the music of the row and took 0.6 dB off it; at -20 it was as loud as the music
VOX = os.environ.get("C11T5_VOX", "1") != "0" and os.environ.get("C11T5_PARA", "1") != "0" and OCT    # v20: a voice in the note (McAdams 1984)
VOX_IN = ("held", 0, 8)                                   # the section, and the bars of it: its first row, where the bass rests and the chord is still heard with its holes
VOX_NOTE = os.environ.get("C11T5_VOX_NOTE", "D2")         # 73.4 Hz: the fourth under the song's A, in the band where this song has least (71 Hz), in bars where nothing else is that low
VOX_PARTS = 18                                            # how many multiples of it the note is made of (the top one 1321 Hz)
VOX_ROLL = 0.5                                            # multiple k is 1 / k ** this of the first (3 dB an octave). At 1 (6 dB an octave) the first tone, alone in its band, stood 21 dB over everything else there while the tones that have to be heard wavering were 4 to 20 dB under the chord and the click
VOX_ALONE = 2                                             # bars the note is heard as it is before anything in it wavers
VOX_TUNE = (3, 4, 6, 4, 3, 2)                             # a bar each: every n-th tone wavers, and is heard as a voice on n times the note
VOX_RATE = 5.5                                            # wavers a second
VOX_DEEP = 0.35                                           # semitones each way (2%)
VOX_EDGE = 0.5                                            # beats the wavering takes to come in, and to go out
VOX_GAIN = os.environ.get("C11T5_VOX_GAIN", "-42dB")      # the first tone's fader; tone k is 20 * log10(k) * VOX_ROLL dB under it. Set in the whole song's master, which delivers this held note 19.5 dB over a render of it alone: at -34dB (and 6 dB an octave) the note was as loud as all the rest of the row together and the row 3.2 dB louder; at -46dB the tones that waver in the third bar were 15 dB under to 2 dB over the music in their own bands; here they are 11 under to 6 over and the whole note is 4 dB under the row
CROSS = os.environ.get("C11T5_CROSS", "1") != "0" and VOX         # v21: two lines cross, and the ear will not let them (the bouncing glides: Tougas and Bregman 1985)
CROSS_BARS = (56, 64, 72)                              # each crossing's first bar from 0: the three pairs of bars of "never arrives" between the stairs and the hat's three climbs, which had nothing of their own
CROSS_LEN = 2                                          # bars to a crossing: the two meet a bar in
CROSS_LOW, CROSS_HIGH, CROSS_OCT = "A3", "A5", 2       # 220 to 880 Hz: they cross on A4 (440 Hz), the song's own note; an octave a bar
CROSS_TOLD = (False, False, True)                      # the crossings in which the two are told apart (the rising one flutters): the last
CROSS_FLUTTER = ("1/32", 0.8)                          # the flutter: a tremolo twice a sixteenth, and how deep
CROSS_PHASE = 0.42                                     # turns: where in its wave the falling tone starts (the rising one starts at nought). MEASURED on a bench of eight starts, not worked out: with this the two are in step where they cross and touch (3 dB up for 80 ms); half a turn off they cancel there and leave a hole 40 ms long
CROSS_LIFT = 3.6                                       # dB: the fluttering tone's fader over the others'. MEASURED: the tremolo takes 3.6 dB off a tone on average, and a line that is quieter than the other is told apart by that too
CROSS_GAIN = os.environ.get("C11T5_CROSS_GAIN", "-32dB")  # set in the whole song's master between two readings: at -30dB each line stood 3.8 dB (median) over all the music in the third of an octave round it and the music was pushed down 0.18 dB; at -36dB 2.3 dB under it. NOT CHOSEN FOR THE SCORE: the lines pass through four bands in which this song is already over the record (468, 641, 749, 877 Hz) and the spectrum term takes 0.2 to 0.3 for them at any fader; an octave lower they would cost nothing and be lost on a small speaker
TUNE = os.environ.get("C11T5_TUNE", "1") != "0" and CROSS       # v22: a tune thrown across the octaves is not a tune (Deutsch's mysterious melody)
TUNE_IN = ("all three", 0)                             # the section and the row of it (from 0): the first row of "all three", which had nothing of its own
TUNE_NOTES = {1: "C", 2: "D", 3: "E", 5: "G"}          # the tune's four notes by their place in the scale of C (this song's white notes); its 5 is the one BELOW its 1
TUNE_CHANGES = ((1, 3, 2, 5), (1, 2, 3, 1))            # the half hour of the clock in Give or Take (the record's first song): the Westminster quarters' second and third changes
TUNE_STEP = 3                                          # sixteenths from note to note
TUNE_LAST = 3                                          # a change's fourth note is this many times as long, as the clock's is: a change is (3 + TUNE_LAST) * TUNE_STEP sixteenths
TUNE_PLAIN = 4                                         # the octave the tune is played in when it is played plainly (C4 D4 E4, and G3 under them)
TUNE_SCAT = (6, 4, 6, 4, 5, 6, 4, 6)                   # the octave each of the eight notes is thrown to: the NAMES of the notes are the tune's, no two neighbours are in one octave, and no E5 or G5 (the scorer's bands of this song at 641 and 749 Hz are over-full: that choice is the scorer's reading)
TUNE_PHASES = ((0, True), (11, False), (22, True))     # (the beat of the row it begins on, is it thrown about?): thrown, plain, thrown again: the SAME notes before and after
TUNE_VEL = 0.8
TUNE_PAN = -0.15                                       # where the song's own line of pips is
TUNE_GAIN = os.environ.get("C11T5_TUNE_GAIN", "-13dB") # set in the whole song's master between two readings, nearer the louder: a tune needs every note, and the PLAIN one is where the music is fullest (196 to 330 Hz). At -12dB its quietest note stood 5 dB over the music in a band 12% wide round its tone (the thrown ones 8 to 29) and the music under the row was 0.12 dB down; at -18dB three plain notes were level with the music
REP = os.environ.get("C11T5_REP", "1") != "0" and TUNE     # v23: a hiss that repeats (Guttman and Julesz, 1963): a rhythm heard in noise that has no rhythm in it, only a length
REP_IN = ("round the click", 1)                        # the section and the row of it (from 0): the row that is bare of bells and has no hat
REP_STEPS = 32767                                      # the hiss is a 15-bit shift register (the engine's `chip` noise, clock 0): it holds no more than this many steps and then begins again, exactly: 93 steps to a turn of the note it is played on
REP_STAGES = ((0, 2, None), (2, 4, 6.0), (4, 6, 3.0), (6, 7, 1.5))   # (from bar, to bar of the row, the sixteenths after which the hiss comes round again; None: a hiss that never does (the engine's white noise)). 3 sixteenths against the beat's 4: the master's own pump is on the beat, and this is not. The row's last bar is left to the rabbit
REP_BAND = (3000, 7500)                                # Hz: every stage through the same filters (nothing under 3 kHz: the click's bands are over-full)
REP_TOP = 3                                            # low-passes in a row at the band's top. NOTHING NEW OVER 10 kHz (chirper-one's ask): with one low-pass at 9 kHz the scorer's bands at 10.8, 12.6 and 14.8 kHz rose 0.8 to 1.0 dB: a low-pass is a slope, not a wall. Three at 7.5 kHz are 22 dB down at 10.8 kHz
REP_TRIM = {None: 0.0, 6.0: -4.6, 3.0: -1.7, 1.5: 1.3}  # dB by stage, read alone, so that every stage is as loud as the first in the band (a register clocked faster is spread wider: untrimmed the stages read +4.6, +1.7 and -1.3 dB against the hiss that never repeats)
REP_GAIN = os.environ.get("C11T5_REP_GAIN", "-27dB")   # set in the whole song's master between two readings, BEFORE their scores were read: THE READINGS WERE TAKEN WITH THE FIRST BAND (3 to 9 kHz, one low-pass), where -28dB put the hiss at -30.3 dBFS (16 dB under the row) and -34dB at -36.3 (22 under), and -31dB was chosen (-33.3 dBFS); the band was then narrowed (REP_TOP), which takes 3.8 dB from the hiss alone, and the fader raised by that: THIS MASTER DELIVERS IT AS WRITTEN (6 dB of fader, 6 dB of hiss) and there is nothing else in its band between the drums (it stands 35 to 54 dB over the music there at either). AND THE MASTER PUMPS IT: every stage, the one that never repeats too, is 9 dB down in the 120 ms after each drum: a swell once a beat is in all of them and is the master's, not the noise's. That is why the loops are 3 sixteenths and not 4
OWN = os.environ.get("C11T5_OWN", "1") != "0" and REP      # v24: the ear's own tone: two plain high tones in one ear make a third in that ear, lower than both, at twice the lower less the upper (the cubic difference tone: Tartini heard its cousin in 1714; Goldstein measured this one in 1967). Nothing in the file is at its frequency
OWN_IN = ("not there", 0)                              # the section and the row of it (from 0): the first row of "not there", before the drum comes in: only the click, the bass, the hat, the pair and the two soft tones round A4 are in it
OWN_LOW = "D7"                                         # the lower tone, held (2349 Hz): the upper one is this times the ratio. Not lower: under it is the click's own band (1.9 kHz), the fullest in the song
OWN_RATIO = (1.10, 1.30)                               # the upper tone over the lower, from and to: the third tone is the lower times (2 - ratio): from 0.90 of it to 0.70: the upper moves 2.9 semitones and the third tone 4.4 THE OTHER WAY. The ear makes most of it under about 1.25 and little by 1.4 (the first two readings went to 1.4: half of each phrase would have had none): it fades as the two draw apart
OWN_PHRASES = (("mid", 1), ("ears", 1), ("ears", -1), ("mid", -1))   # two bars each: where the two tones are (both in the middle: both in each ear; or an ear each: the lower left, the upper right) and which way the upper one goes. AN EAR EACH IS THE PROOF: on headphones no ear has both and the third tone is gone; on loudspeakers both reach both ears and it stays
OWN_GAP = 0.25                                         # beats of rest at the end of each phrase
OWN_VEL = 0.8
OWN_EARS = 0.0                                         # dB on the two an-ear-each tracks, read alone, so that a tone alone in an ear is as loud there as it is in each ear from the middle
OWN_GAIN = os.environ.get("C11T5_OWN_GAIN", "-37dB")   # each tone: set in the whole song's master, FOUR readings: the first guess (-30) was 13 dB too loud: THE MASTER LIFTS A PLAIN TONE AT 2.3 kHz IN THIS ROW 16 dB (written -28: each tone -17.4 dBFS, the two only 4.7 dB under all the rest of the row together, and the rest pushed 0.7 dB down; -34: 10.2 dB under)
SHRINK = os.environ.get("C11T5_SHRINK", "1") != "0" and OWN   # v25: time-shrinking (Nakajima, ten Hoopen and van der Wilk, 1991): of two short empty times one after the other, the SECOND is heard shorter than it is when it is the longer by up to about a tenth of a second: 60 ms then 120 ms is heard as nearly even; 120 ms then 60 ms is heard as it is
SHRINK_IN = ("round the click", 2)                     # the section and the row of it (from 0): its third row, where the drum is on the sixteenth after the click (ta-DUM) and the two sixteenths before the click are empty in every beat
SHRINK_FIRST = 0.5                                     # the sixteenth of the beat the first small click is on: 180 ms after the drum before it, and 180 ms before the song's click (which is on sixteenth 2): the song's click is the third stroke of the three
SHRINK_SECOND = ((1.0, 4), (1.5, 3))                   # (the sixteenth of the beat the second small click is on, bars): 60 ms then 120 ms to the click for four bars (said to be heard as nearly even); then 120 ms then 60 ms for three (heard uneven). ONE click moves, by 60 ms. The row's last bar is the rabbit's
SHRINK_NOTE, SHRINK_VEL = "A3", 0.6                    # the pair's own small wooden click (the same click to the sample every time), as its first stroke is written; here on its own patch, `ht-grace`, which has a top
SHRINK_PAN = 0.0                                       # where the song's click is: three strokes in one place
SHRINK_EARLY = 1 / 220.0                               # seconds: the small click is WRITTEN this much early: one turn of its saw (A3), whose first edge comes a whole turn after the note starts. Read in the whole song's master before this was written: the small click's peak 6.1 ms after its written instant, the song's click's start 1.1 to 1.7 ms after its own: the second time was 115 ms for 120, and 55 for 60
SHRINK_TOP = 7500.0                                    # Hz: the small click's top (two low-passes): the pair's own patch (`ht-two`) was tried first and 56 more of it put 0.1 dB into each of the three bands over 10 kHz (chirper-one has asked for nothing more there); its bottom at 2200 Hz for 700 was tried too and put 0.2 there and mended nothing
SHRINK_GAIN = os.environ.get("C11T5_SHRINK_GAIN", "-7dB")   # the small click's fader; read in the whole song's master at -13 dB (the first of the two does not stand over the music: +1.4 and -2.9 dB) and at -7 (it stands 7.0 and 2.6 dB over it; the second 15 and 16; both 8 to 9 dB under the song's click): THIS ROW HAS NO HAT AND THE MASTER DELIVERS A SMALL CLICK AS WRITTEN (6 dB for 6)
GLISS = os.environ.get("C11T5_GLISS", "1") != "0" and SHRINK   # v26: the bass that falls for ever (Shepard, 1964; Risset, 1969): plain tones an octave apart, all sliding down together under one fixed curve of loudness, silent at its two ends: each tone falls and falls, a new one comes in unheard at the top as one goes out unheard at the bottom, and the whole is always falling and never lower
GLISS_IN = ("held", 1)                                 # the section and the row of it (from 0): a row with no drum and no bass
GLISS_LOW = "A0"                                       # 27.5 Hz: the bottom of the curve, where a tone is silent
GLISS_OCTAVES = 4                                      # the curve's width, and the number of tones: its top is 440 Hz, its loudest place two octaves up: A2, 110 Hz
GLISS_PER = 2                                          # bars in which every tone falls an octave: four octaves in the row
GLISS_FADE = (2.0, 2.0)                                # beats over which the whole comes in and goes out
GLISS_STEP = 0.25                                      # beats between two points of a tone's loudness lane
GLISS_GAP = 0.25                                       # beats before the bottom at which a tone's note is let go (it is 64 dB down by then)
GLISS_FLOOR = -90.0                                    # dB: "silent"
GLISS_PAN = 0.0
GLISS_GAIN = os.environ.get("C11T5_GLISS_GAIN", "-36dB")     # each tone's fader at the curve's top; read in the whole song's master at -36dB and -30dB and set BEFORE either's score was read: at -36 the strongest tone is -24.2 dBFS (the master moves it between -26.4 and -21.5 with the row's clicks), the whole bass 7.5 dB under the row's other music and 12.6 dB over it at 35 to 125 Hz, where there was nothing; the row is 0.7 dB up. At -30 the row is 2.2 dB up and no longer the quiet one between its neighbours. The quiet one
PCEN = os.environ.get("C11T5_PCEN", "1") != "0" and GLISS   # v27: A SWELL IS HEARD LATE (the perceptual centre: Morton, Marcus and Frankish, 1976): a sound's moment is not its start. A low note that begins on the true beat and swells for two sixteenths is heard where it ARRIVES, on the click; the same note at the same instant struck and dying away is heard where it begins. Four bars of each: no note moves and the beat turns round
PCEN_IN = ("the wrong one again", 0)                   # the section and the row of it (from 0): the click alone is the beat again, the bass has no fundamental and there is no drum
PCEN_BARS = (4, 4)                                     # bars it swells, then bars it is struck
PCEN_LEN = 0.5                                         # beats a note lasts: from the beat (where the drum falls in other rows) to the click (two sixteenths: 240 ms)
PCEN_FALL = 40.0                                       # dB the level travels over the note, a straight line in dB: up to its top for a swell, down from it for a struck note: one is the other backwards
PCEN_PARTS = ((1, 0.0), (2, -9.0))                     # the note and its octave (times, dB): on the bass's own note (A1, C2: the fundamental its patch does not have) the octave is what a small loudspeaker gives
PCEN_GAIN = os.environ.get("C11T5_PCEN_GAIN", "-26dB")  # both tracks. Read in the whole song's master at -38dB and -32dB: at -32 a swell's top was -25.7 dBFS and a struck note's -28.1 at 40 to 95 Hz, some 12 dB under a stroke of the bass drum in the rows that have one. It is this row's drum: 6 dB over the louder reading
ALIKE = os.environ.get("C11T5_ALIKE", "1") != "0" and PCEN   # v28: THE ACCENT THAT IS NOT THERE (subjective rhythm: Bolton 1894; Brochard and others 2003): a small tick on every sixteenth, every one the same. Ticks that are all alike are not heard alike: the ear groups them and hears an accent on the first of each group. For ALIKE_FORM's first bars they are alike; then every third one is struck twice as hard (6 dB), in threes against the drum's fours; then they are all alike again, and the question is what the ear goes on hearing
ALIKE_IN = ("turned around", 2)                        # the section and its row (from 0): bars 33 to 40: the drum has shown where the beat is, and nothing else in the row ticks. (The last row of "not there", bars 97 to 104, was tried first and read: the hat that never arrives is a sixteenth stream of its own there, 14 dB over the ticks and changing from bar to bar: a tick at one place in the bar came out up to 10.8 dB apart)
ALIKE_FORM = ((2, 0), (2, 3), (4, 0))                  # (bars, n): for so many bars every n-th tick is struck twice as hard (0: none is)
ALIKE_NOTE = "E8"                                      # 5274 Hz: the song's spectrum is short there and nothing else in the row is a small high sine
ALIKE_VEL = 0.5                                        # the velocity of a tick that needs no trim (the patch's loudness goes as velocity squared): room for +12 dB
ALIKE_TRIM = tuple(float(x) for x in os.environ.get("C11T5_ALIKE_TRIM", "-0.5,-3.5,5.5,1,2.5,-3,4.5,-1,-1,-4,5,0.5,3.5,-3,4,-1.5").split(","))   # dB by sixteenth of the bar: what the master takes from a tick there, given back, so that the ticks are alike WHERE THEY ARE HEARD. Read in the whole song's master with no trims (C11T5_ALIKE_TRIM=0,0,... at -24dB): the ticks written alike came out 9.1 dB apart (nine in ten of them): a tick with the click (sixteenths 2, 6, 10, 14) 7 to 9 dB under one a sixteenth after the drum (1, 5, 9, 13), the same in every bar to under 1 dB (to 4 where the clap is)
ALIKE_GAIN = os.environ.get("C11T5_ALIKE_GAIN", "-22dB")   # both tracks. Read in the whole song's master at -24dB (no trims): the middle tick's top -33.9 dBFS at 4 to 7 kHz, where the old music's top at a tick's instant is -33.7 in the middle: set 2 dB over that, before any score was read
HOLE = os.environ.get("C11T5_HOLE", "1") != "0" and ALIKE   # v29: A TUNE OF HOLES (auditory enhancement: Viemeister 1980; Viemeister and Bacon 1982): the same chord of plain tones sounds again and again, every tone as loud as every other; before each, the chord is heard with ONE tone left out. In the whole chord that follows, the tone that was missing stands out as a note of its own, though it is no louder than the rest: the ear has got used to the others. The notes left out are the song's tune (the one that is in neither ear, bars 121 to 128), so the tune is heard in a chord that never changes
HOLE_IN = ("not there", 2)                             # the section and its row (from 0): bars 97 to 104: the section about what is heard and is not in the sound; its last row had nothing of its own
HOLE_CHORD = ("E6", "G6", "A6", "C7", "D7", "E7", "G7", "A7")   # the chord: 1319 to 3520 Hz, where the song has room (2631 to 4930 Hz are within 2 dB of the middle) and the row is quiet between its strokes; no two tones nearer than a tone
HOLE_UP = 2                                            # octaves the tune is taken up to lie in the chord
HOLE_BEATS = 2                                         # beats to a note of the tune, as in "in the noise"
HOLE_PRE = (0.0, 1.0)                                  # the chord with the hole: where in the note's beats it starts, and how long (beats): 480 ms, long enough for the ear to get used to it
HOLE_FULL = (1.25, 0.5)                                # the whole chord: a sixteenth after the second beat (the drum falls in the gap between the two), half a beat long
HOLE_GAIN = os.environ.get("C11T5_HOLE_GAIN", "-54dB")   # both tracks. Meant before any reading: each tone about -44 dBFS in the master (the row's own music between its strokes is at -47 to -60 dBFS in a sixth of an octave round each). The bench (the row alone at -20 dB): each tone -26.0 dBFS. Read in the whole song's master at -50dB and -56dB (seed 0), BEFORE any score: each tone -39.9 and -45.9 dBFS in the whole chords (this master lifts them 16 dB), the whole chord -32.8 and -38.8, the old music at 1250 to 3700 Hz in the same windows -32.0: -54dB is the level meant
HURRY = os.environ.get("C11T5_HURRY", "1") != "0" and HOLE   # v30: THE HURRY THAT IS NOT THERE: a stair of notes exactly even in time, three to every two beats of the drum, climbs for two bars and comes down for two. A line that rises is judged to be speeding up and a line that falls to be slowing down, though its notes are evenly spaced (Boltz 2011, "Illusory tempo changes due to musical characteristics"). Nothing in the time changes: only the pitch
HURRY_IN = ("not there", 1)                            # the section and its row (from 0): bars 89 to 96: the row of "not there" that had nothing of its own; the section is about what is heard and is not in the sound
HURRY_LADDER = ("E2", "G2", "A2", "C3", "D3", "E3", "G3", "A3", "C4", "D4", "E4", "G4", "A4")   # the stair: the song's five notes from 82 to 440 Hz: low, where the song has room (83 to 250 Hz are under the middle) and away from 468 to 1922 Hz, which are full
HURRY_RUN = 12                                         # notes to a climb and to a descent: two bars each. The climb is steps 1 to 12 of the ladder, the descent steps 13 to 2: no note twice running
HURRY_STEP = 2 / 3                                     # beats from note to note: three notes to two beats: against the drum's four a bar, six
HURRY_AT = 0.125                                       # the beat of the row its first note is on: so that no note falls with a stroke of the drum, the bass, the tick or the Risset hat: every note is BETWEEN strokes (0.125, 0.792 and 0.458 of a beat by turns)
HURRY_LEN = 0.5                                        # beats a note is written
HURRY_TRIM = (0.0, 0.0, 0.0)                           # dB for each of the three places in the beat (a track each), so that every note comes out of the master alike
HURRY_GAIN = os.environ.get("C11T5_HURRY_GAIN", "-28dB")   # the three tracks, before their trims. The bench (the row alone at -20 dB): a note's first 100 ms -33.6 dBFS. Read in the whole song's master at -34dB and -40dB (seed 0), BEFORE any score: -32.2 and -38.2 dBFS (the master lifts it 15.4 dB: between the strokes, in a row with the drum); the three places in the beat 0.9 dB apart: no trims; nine in ten within 3.5 dB. At -34dB the notes were 16.4 dB under the old music at 60 to 1500 Hz (the drum, the bass and the sub are in that band): too far under for low notes. -28dB is meant to bring a note to -26.2 dBFS
HEAVY = os.environ.get("C11T5_HEAVY", "1") != "0" and HURRY   # v31: THE LOUDER, THE LOWER: one plain low note, loud and soft by turns, then swelling and sinking back. Its frequency never moves. A plain low note is said to be heard lower the louder it is (Stevens 1935): if it is, the turns are a tune of two notes and the swell is a bend, and neither is written
HEAVY_IN = ("not there", 0)                            # the section and its row (from 0): bars 81 to 88: no drum; nothing else below 400 Hz but the bass, which is weak there; the row before the stair, which starts on the same note
HEAVY_NOTE = "E2"                                      # 82.41 Hz: the note the stair of v30 starts on, eight bars later
HEAVY_STEP = 12.0                                      # dB between the loud and the soft
HEAVY_TURNS = 4                                        # bars of turns: a note every HEAVY_EVERY beats, loud, soft, loud, soft ; then one note held to the end of the row, from soft up to loud at its middle and back, a straight line in dB each way
HEAVY_EVERY = 2                                        # beats from note to note in the turns
HEAVY_LEN = 1.75                                       # beats a note of the turns is held (it is gone before the next comes)
HEAVY_GAIN = os.environ.get("C11T5_HEAVY_GAIN", "-28dB")   # the loud; the soft is HEAVY_STEP under. The bench (the three tracks alone, the loud at -20 dB): the loud -29.0 dBFS, the soft -41.0. Read in the whole song's master at -28dB (both seeds) BEFORE any score: the loud -19.5 dBFS (the master lifts it 17.5 dB in this row, which has no drum), the soft -31.1, 12.9 dB over the old music in its band: I had aimed at -16 for the loud; kept
LONG = os.environ.get("C11T5_LONG", "1") != "0" and HEAVY   # v32: THE LONGER, THE LOUDER: a pip after every beat, always the same note at the same height; only its length changes, doubling beat by beat from 5 ms to 80 and halving back. Under about a fifth of a second the ear adds a sound up over its length: the same height twice as long is heard louder. A swell and a fall every two bars, and no level moves
LONG_IN = ("turned around", 1)                         # the section and its row (from 0): bars 25 to 32. Read on v31 by twelfths of the beat: 700 to 1400 Hz is -54 and -42 dBFS from a third to a half of the beat there (the emptiest place in a row with the drum), and no note of the song begins within 26 ms of a third of a beat
LONG_AT = (1, 3)                                       # where in every beat: a third of a beat after it (160 ms): nothing else in the row strikes there
LONG_MS = (5, 10, 20, 40, 80, 40, 20, 10)              # the lengths, beat by beat, in ms: doubling four times and halving back: an arch every two bars. The longest ends on the off-beat
LONG_NOTE = "B5"                                       # 987.8 Hz: the fifth of the song's E
LONG_EDGE = 2                                          # ms the pip takes to come and to go
LONG_GAIN = os.environ.get("C11T5_LONG_GAIN", "-28dB")   # the track. THE BENCH FIRST (the track alone at -20 dB): all 32 tops -25.9 to -25.8 dBFS; the lengths at half height 4.4, 9.5, 19.5, 39.5, 79.5 ms. Read in the whole song's master at -28dB (both seeds) BEFORE any score: the tops -14.4 to -13.4 dBFS (this master lifts a pip a third of a beat after the drum 19.6 dB: I had guessed 15, so it is 5 dB hotter than I aimed: kept: after the clap the old music is -29 dBFS in its band)
KAPPA = os.environ.get("C11T5_KAPPA", "1") != "0" and LONG   # v33: FAR IN PITCH, FAR IN TIME (the kappa effect): three pips a bar, a beat apart: low, a middle one, high. The middle pip is in the middle in time, always; bar by bar it is by turns two semitones from the first or two semitones from the last. The ear is said to hear it nearer in time to the pip it is nearer in pitch: early, then late. Then, for two bars, it is truly moved that way, to be compared
KAPPA_IN = ("round the click", 1)                      # the section and its row (from 0): bars 145 to 152, with the hiss that repeats (3000 Hz and up). Read on v32 by twelfths of the beat: the drum, the bass and the tick are all on the half beat here, and on the beat 400 to 800 Hz is -46 dBFS and 700 to 1400 Hz -50; 7 notes of the song begin within 26 ms of the beat (the hiss's own, and the rabbit's in bar 152)
KAPPA_BARS = 7                                         # a figure a bar for seven bars: bar 152 is the rabbit's
KAPPA_AT = (0, 1, 2)                                   # the beats of the bar its three pips fall on: each midway between two strokes of the drum, a beat (480 ms) apart
KAPPA_ENDS = ("A4", "A5")                              # the first pip and the last: an octave apart
KAPPA_MID = ("B4", "G5")                               # the middle pip, bar by bar in turn: 2 semitones from the first (and 10 from the last), or 2 from the last
KAPPA_TRUE = (4, 5)                                    # the bars (from 0) in which the middle pip is truly moved the way the ear is said to hear it
KAPPA_BY = 0.0625                                      # ... by this part of a beat (30 ms): early when it is near the first, late when it is near the last
KAPPA_MS = 60                                          # ms a pip is held
KAPPA_EDGE = 5                                         # ms it takes to come and to go
KAPPA_GAIN = os.environ.get("C11T5_KAPPA_GAIN", "-32dB")   # the track. THE BENCH FIRST (the track alone at -20 dB): all 21 tops -25.8 to -25.7 dBFS (5.8 under the fader); the middle pip 0.0 ms off the middle in five bars and -30.0 and +30.0 in the two where it is moved. Aimed at tops of -18 dBFS with the lift read for a pip between the drum's strokes in bars 25 to 32 (19.6 dB). Read in the whole song's master (both seeds) BEFORE any score: all 21 tops -17.6 to -17.3 dBFS (the lift here is 20.3 to 20.4 dB); the middle pip 0.0 to 0.1 ms off the middle in the five bars and -29.6 and +29.9 / +29.8 in the two
SHIFT = os.environ.get("C11T5_SHIFT", "1") != "0" and KAPPA   # v34: THE SAME SPACING, ANOTHER NOTE (the pitch shift of the residue: Schouten, de Boer): a pip of three plain tones always the same distance apart (the note G3, 196 Hz, apart: as its 5th, 6th and 7th overtones are). Beat by beat all three are moved up together by an eighth of that distance. The distance never changes, so the three beat 196 times a second all the while; yet the note the ear makes of them is said to move: up a third of a semitone a step, down two and a third at the fifth, and up again. In the last two bars the tune it is said to be is played plainly, to be compared
SHIFT_IN = ("not there", 1)                            # the section and its row (from 0): bars 89 to 96, with the hurry that is not there (82 to 392 Hz). Read on v33: 1000 and 1400 Hz are -47 and -52 dBFS here, the emptiest row of the song up there
SHIFT_AT = (1, 3)                                      # where in every beat: a third of a beat after it
SHIFT_MS = 70                                          # ms a pip is held: it ends before the tick on the half beat
SHIFT_EDGE = 5                                         # ms it takes to come and to go
SHIFT_NOTE = ("G3", 195.998)                           # the distance between the tones, as a note
SHIFT_RANKS = (5, 6, 7)                                # the three tones at the start: the note's 5th, 6th and 7th overtones (980, 1176, 1372 Hz)
SHIFT_STEPS = 8                                        # steps to a whole distance: after 8 the tones would be the 6th, 7th and 8th overtones, and the turn begins again from the 5th, 6th and 7th
SHIFT_TURNS = (3, 1)                                   # turns of the three tones (bars 89 to 94), then turns of the plain tune (bars 95 and 96)
SHIFT_UP = 12                                          # semitones the plain tune is played above the note it is said to be: clear of the hurry and the bass
SHIFT_GAIN = os.environ.get("C11T5_SHIFT_GAIN", "-31dB")   # every track. THE BENCH FIRST (the tracks alone at -20 dB): the three tones' tops -26.4 to -26.0 dBFS, the plain tones' -25.9 to -25.5; every distance between neighbouring tones 195.6 to 196.3 Hz. Aimed at tops of -20 dBFS with a lift of 17 (guessed from a low pluck in this row). Read in the whole song's master (both seeds) BEFORE any score: the lift is 20.0: tops -18.7 to -16.7 / -16.6 dBFS (the middle -17.0), 3 dB over the aim; kept
GAP = os.environ.get("C11T5_GAP", "1") != "0" and SHIFT   # v35: THE GAP GOES TO THE OTHER ONE (the gap transfer of Nakajima and others): a long plain tone glides slowly up; a short one glides quickly down across it. In bars 137 and 141 the LONG one is broken for a moment just where they cross, and the short one is whole. It is said to be heard the other way round: the long glide runs on unbroken and the short one has the hole. In bars 139 and 143 it is made the way it is said to sound (the short one broken, the long whole), to be compared: the two are said to sound alike
GAP_IN = ("round the click", 0)                        # the section and its row (from 0): bars 137 to 144. Read on v34 by twelfths of the beat: 950 to 1650 Hz is -74 and -52 dBFS a third to five twelfths into the beat (between the drum on the quarter and the tick on the half), -31 to -40 in the beat's second half
GAP_BARS = (0, 2, 4, 6)                                # the bars of the row (from 0) with a pair of glides: bars 137, 139, 141, 143
GAP_KIND = ("long", "short", "long", "short")          # which glide is broken in each
GAP_LONG = (0.583, 3.583, 980.0, 1560.0)               # the long glide: from beat, to beat (of its bar), from Hz, to Hz: a straight line in pitch, 8 semitones in 3 beats. THE FIRST BUILD HAD 0.875 TO 3.875 (the crossing on beat 2.375) and the break fell in the drum's own dent: the master takes 9 dB off a held tone for a twelfth of a beat after every drum stroke (the stroke is on the quarter beat here): read by twelfth, the glide alone was -24 -23 -25 -32 -28 -27 -30 -29 -28 -26 -24 -22 dBFS. From the eleventh twelfth of a beat to the third it read -22 to -25: the crossing is now on beat 2.083, in the middle of that
GAP_SHORT = (0.75, 6.0)                                # the short glide: beats long and semitones it falls: centred where the long one is half way (beat 2.083, 1236 Hz): they cross there
GAP_MS = 90                                            # ms from the end of the broken glide's first piece to the start of its second, centred on the crossing: it ends 35 ms before the drum (beat 2.25)
GAP_EDGE = 10                                          # ms a piece takes to come and to go
GAP_NOTE = "C6"                                        # the written note; the lanes are in semitones from it
GAP_GAIN = os.environ.get("C11T5_GAP_GAIN", "-34dB")   # both tracks. THE BENCH FIRST (the two tracks alone at -20 dB): one glide alone, in the break, -29.0 dBFS; the builds were set for -43 on the bench. THE SECOND BUILD READ (both seeds, before any score): before the break, in it, after it: -21.9 -22.9 -24.3 dBFS where the long glide is broken, -22.1 -23.0 -24.1 where the short one is; the long glide where it is alone -34 to -23: the master's dent after every drum stroke is still in it
AFTER = os.environ.get("C11T5_AFTER", "1") != "0" and GAP and GLISS   # v36: AFTER THE FALL, A NOTE THAT DOES NOT MOVE (the after-effect of a steady change of pitch: Shu, Swindale and Cynader, 1993; the waterfall illusion, in sound). For eight bars four tones have fallen without a break (the bass that falls for ever, v26). The moment they stop, one plain note is held, and it does not move at all: after a long fall a steady note is said to seem to RISE for a moment. The same note is held twice more, 4 and 8 bars on, as the after-effect wears off: the same note, as long and as loud. The song's own fall is the cause; nothing is added to it
AFTER_BARS = (0, 2, 4)                                 # bars after the fall's row in which the note is held (from 0): the first begins on the bar line the fall ends on
AFTER_BEATS = 3                                        # beats the note is held
AFTER_NOTE = "E4"                                      # 329.6 Hz: inside what fell (27.5 to 440 Hz), under the tune in the noise (A4 and up). Read on v35: a semitone either side of it is -41 to -43 dBFS in bars 121 to 128
AFTER_EDGE = 40                                        # ms the note takes to come and to go
AFTER_FLAT = (-6.4, -6.6, -6.8, -6.9, -7, -7, -7.1, -7.1, -7.1, -7.2, -7.1, -7, -0.1, -1.8, -3.6, -4.8, -5.6, -6.1, -6.4, -6.6, -6.8, -6.9, -7, -7.1, -7.1, -7.1, -7.1, -7.2, -7.2, -7.2, -7.2, -7.2, -7.2, -7.2, -7.2, -7.1, -1, -2.4, -4, -5, -5.7, -6.2, -6.5, -6.7, -6.8, -6.9, -7, -7.1, -7.1, -7.1, -7.1, -7.2, -7.2, -7.2, -7.2, -7.2, -7.2, -7.2, -7.2, -7, -0.1, -1.8, -3.6, -4.8, -5.6, -6.1, -6.4, -6.6, -6.8, -6.9, -7, -7.1, -7.1, -7.1, -7.2, -7.2, -7.2, -7.2, -7.2, -7.2, -7.2, -7.2, -7.2, -7, -0.3, -1.9, -3.7, -4.9, -5.6, -6.1, -6.4, -6.6, -6.8, -6.9, -7, -7.1, -7.1, -7.1, -7.1, -7.2, -7.2, -7.2, -7.2, -7.2, -7.2, -7.2, -7.2, -7, -0.9, -2.3, -3.9, -5, -5.7, -6.1, -6.5, -6.7, -6.8, -6.9, -7, -7.1, -7.1, -7.1, -7.2, -7.2, -7.2, -7.2, -7.2, -7.2, -7.2, -7.2, -7.2, -7, 0, -1.7, -3.6, -4.8, -5.5, -6, -6.4, -6.6, -6.8, -6.9, -7, -7.1, -7.1, -7.1, -7.1, -7.2, -7.2, -7.2, -7.2, -7.2, -7.2, -7.2, -7.2, -7, -0.2, -1.8, -3.7, -4.8, -5.6, -6.1, -6.4, -6.6, -6.8, -6.9, -7, -7.1, -7.1, -7.1, -7.1, -7.2, -7.2, -7.2, -7.2, -7.2, -7.2, -7.2, -7.2, -7, -1.1, -2.6, -4.1, -5.1, -5.8, -6.2, -6.5, -6.7, -6.8, -6.9, -7, -7.1, -7.1, -7.1, -7.2, -7.2, -7.2, -7.2, -7.2, -7.2, -7.2, -7.2, -7.2, -7, -0, -1.7, -3.6, -4.8, -5.5, -6, -6.4, -6.6, -6.8, -6.9, -7, -7.1)   # dB on the track through each note, by twenty-fourth of the beat (72 places a note, a note after another): THE MASTER'S OWN DENTS TURNED OVER. The first build had none (-42 dB): the note's frequency did not move (0.13 cents at the most between any two tenths of a second) but its level did: the master took it down 7 dB for less than a sixth of a beat at every half beat, where the click is (-30.5 to -27.5 dBFS by quarter of a beat). This is that reading (the song's envelope less the bench's, seed 0), 0 at the place the master holds lowest. The three notes read alike within 0.7 dB and the two seeds within 0.4
AFTER_GAIN = os.environ.get("C11T5_AFTER_GAIN", "-36.4dB")   # THE BENCH FIRST (the track alone at -20 dB): the note -26.0 dBFS; set for -30 in the song with 18 dB of lift (a part in a bare break got 17 to 18.5): -42 dB. THE LIFT WAS 13.4 dB in the dents and 20.6 at the most. The second build is set by the lowest (AFTER_FLAT brings every place down to it) for -29 dBFS: -36.4 dB
SPREAD = os.environ.get("C11T5_SPREAD", "1") != "0" and AFTER   # v37: THE WIDER, THE LOUDER: two pips that read the same on a meter. One is a single plain tone; the other is four plain tones a fourth or a fifth apart, each a quarter of the power. The ear adds loudness band by band, not power: what is spread over more of the ear is said to sound louder (Zwicker, Flottorp and Stevens, 1957). Then the spread one is really turned down, step by step: at which step are the two alike?
SPREAD_IN = ("never arrives", 2)                       # the section and its row (from 0): bars 57 to 64
SPREAD_FROM = 2                                        # bars into the row it begins: bar 59 (the two lines cross in bars 57 and 58)
SPREAD_NOTE = "E5"                                     # the one tone (659.3 Hz)
SPREAD_TONES = (-7, 0, 5, 12)                          # the four, in semitones from it: A4 E5 A5 E6 (440 to 1319 Hz): each further from its neighbour than the ear's own band is wide there
SPREAD_AT = (1.75, 3.75)                               # beats of the bar a pip begins on: evenly 2 beats apart, off the pairs of "the second one sounds louder" (beats 0.25, 0.75, 2.25, 2.75) and off the tick (the half beats). Read on v36 FIRST (b/oldat2.py: the old music under a pip in the band of each of its four tones, from every sixteenth of bars 59 to 64)
SPREAD_LEN = 0.25                                      # beats a pip lasts (120 ms)
SPREAD_EDGE = (4, 10)                                  # ms it takes to come and to go
SPREAD_DOWN = (0, 3, 6)                                # dB the spread pip is really turned down, 2 bars each
SPREAD_TRIM = (4.8, 3.7, 4.5, 2.9, 2.3, 2.3, 3.2, 4.2, 2.9, 4.7, 3.4, 2.2)   # dB on a pip, by pip: THE FIRST BUILD READ TURNED OVER. With no trims (-28.5 dB) the master delivered the one tone at -22.1 to -19.9 dBFS and the spread pip against it at +0.9, -1.5, -3.1, -2.2, -7.6 and -7.1 dB bar by bar where 0, 0, -3, -3, -6 and -6 are written, the same on both seeds: each pip's level less what it should read (-18, less what it is written down), turned over, 1.15 times as deep
SPREAD_GAIN = os.environ.get("C11T5_SPREAD_GAIN", "-23.7dB")   # both tracks. THE BENCH FIRST (the two pips alone at -20 dB): each -29.0 dBFS on the meter (the spread one's highest sample 4.9 dB over the one tone's); the first build set for -18 in the song with 19.5 dB of lift: -28.5 dB: it read -22.1 to -19.9 (a lift of 15.4 to 17.6 dB). The second build is set for -18 with the trims: -23.7 dB
ODD = os.environ.get("C11T5_ODD", "1") != "0" and SPREAD   # v38: THE ODD ONE OUT SEEMS LONGER: a plain note on every beat, every one held the same 300 ms; every seventh is another note. The one that is not like its fellows is said to seem longer than they are (the oddball effect: Tse, Intriligator, Rivest and Cavanagh, 2004)
ODD_IN = ("out", 0)                                    # the section and its row (from 0): bars 185 to 192, the last row with the drum; nothing is written after bar 192
ODD_AT = 0.25                                          # beat of every beat a note begins on: a sixteenth after the drum
ODD_LEN = 0.625                                        # beats a note is held (300 ms)
ODD_NOTE = "C5"                                        # the note that repeats. IT WAS FIRST B4 (493.9 Hz): the scorer's band at 468 Hz stood at +6.0, on its edge, and B4 took it to +6.5 (charged 0.5); and B4 with G flat is not in the song's key. C5 is in the next band (547 Hz, +3.3) and in the key
ODD_OTHER = "G4"                                       # the odd one: a fourth below (first G flat 4, under B4)
ODD_FIRST = 5                                          # the first odd one (notes from 0)
ODD_EVERY = 7                                          # and every this many after it: never twice in the same place of the bar
ODD_EDGE = (10, 10)                                    # ms a note takes to come and to go
ODD_TRIM = (-2, -2.1, -1.9, -1.6, -1.1, 0.6, -0.9, -1.9, -1.2, -0.8, -1.1, 0.8, -1, -0.3, -0.7, 1.2, -0.2, -1.8, -0.8, 0.4, -1.8, 0.4, -1.8, 0.5, -1.3, -1.3, 1.7, -0.6, -1.3, -1.9, -1.7, -2)   # dB on a note, note by note. MEASURED, NOT REASONED: with no trims (-26 dB) the master gave the 32 notes -21.5 to -18.1 dBFS, the odd ones 1.4 to 2.3 dB under their neighbours but for one 1.1 over (the two seeds within 0.02 dB): each note's level less -20, turned over and written 1.15 times as deep
ODD_GAIN = os.environ.get("C11T5_ODD_GAIN", "-28.3dB")   # THE BENCH FIRST (the track alone at -20 dB): every note -29.0 dBFS and 297.7 ms long (between the points 6 dB under its level), the odd ones as their fellows; the first build set for -20 in the song with 15 dB of lift; the second build: the trims' top (1.7) added to the first build's -26 dB; THE THIRD BUILD: 4 dB lower (the second raised its own row 0.37 dB and turned every other row down by up to 0.1), and the notes a semitone up; the trims are the second build's, fitted on B4 and G flat 4
MLD = os.environ.get("C11T5_MLD", "1") != "0" and ODD   # v39: TURNED OVER IN ONE EAR, THE NOTE COMES BACK (binaural unmasking: Hirsh 1948, Licklider 1948). A plain low note under the hiss of "in the noise", the same in both ears, is turned down until the hiss covers it; then, no louder, the right ear's is turned upside down. Either ear alone is given what it was given before
MLD_IN = ("in the noise", 0)                           # the section and its row (from 0): bars 121 to 128. READ FIRST (v38, seed 0): of the 26 rows it is the one with the hiss, and 200 to 360 Hz reads there (-34.6 dBFS in the middle window of 100 ms, -29.2 in the loudest; every other row but the first and the last reaches -22.3 to -12.5 in its loudest), and round A3 that hiss is the same in both ears
MLD_NOTE = "A3"                                        # 220 Hz: under the tune of the row (A4 to A5) and clear of the note of "after the fall" (E4)
MLD_AT = ((1, 0), (1, 2), (3, 0), (3, 2), (5, 0), (5, 2), (6, 0), (6, 2), (7, 0), (7, 2))   # (bar of the row from 0, beat): never in bars 121, 123, 125 while the note of "after the fall" is held
MLD_LEN = 1.6                                          # beats a note is held (768 ms)
MLD_OVER = 8                                           # dB the first note is aimed over the hiss in the ear's own band round it (48 Hz wide at 220 Hz: 196 to 244 Hz)
MLD_DOWN = (0, 4, 8, 13, 13, 13, 13, 13, 13, 13)       # dB under the first, note by note
MLD_TURNED = (0, 0, 0, 0, 1, 0, 1, 0, 1, 1)            # 1: the right ear's wave is upside down
MLD_EDGE = (60, 60)                                    # ms a note takes to come and to go
MLD_TRIM = (0.0,) * 10                                 # dB on a note, note by note: none
MLD_GAIN = os.environ.get("C11T5_MLD_GAIN", "-42.6dB")   # all three tracks. THE BENCH FIRST (the three alone at -20 dB): the first note -29.0 dBFS in each ear; the first build set for -31.8 dBFS in the song (the hiss in the ear's band read -39.8 there in v38, and 8 over it) with 17 dB of lift, a guess. THE SECOND BUILD: the lift was 19.8 dB, not 17, and the notes stood 2.4 to 3.9 dB (seed 0) and 1.4 to 4 dB (seed 11) over what is written against the hiss: 2.8 dB lower, the middle of the twenty. No trims: the notes came out 0 -4 -8 -13 against the first to 0.1 dB; what differs from note to note is the hiss, and it is another hiss on each seed
PARA = os.environ.get("C11T5_PARA", "1") != "0" and OCT    # v19: an octave up is a semitone down (Risset's paradox)
PARA_IN = ("round the click", 0, 8)                       # the section, and the bars of it: its first row (the row before the answer's bells is left bare)
PARA_APART = 2.1                                          # from each tone of the bell to the next: a little more than an octave (1284.5 cents)
PARA_NOTES = ("D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8")    # what is written: an octave up at every stroke, then back down
PARA_MID = 2900.0                                         # Hz: where the curve every one of these bells is under is loudest (where this song has room: 2.2 to 6.7 kHz)
PARA_WIDE = 0.8                                           # octaves: how wide it is (the sigma of a bell curve over octaves)
PARA_FLOOR = -20                                          # dB: tones quieter than this under the curve are left out: every bell has three tones, and nothing sounds over 10 kHz (at -30 four of the eight had a tone at 10.4 to 12 kHz)
PARA_STEPS = (2, 6, 10, 14)                               # the sixteenths of the bar it strikes on: the click's
PARA_VEL = 0.75
PARA_GAIN = os.environ.get("C11T5_PARA_GAIN", "-24dB")
FIRST = os.environ.get("C11T5_FIRST", "1") != "0" and FALL   # v12: the first one wins (the precedence effect)
FIRST_IN = ("held", 0, 16)                                # the section, and the bars of it
FIRST_EVERY = 3                                           # sixteenths between strokes: three against the click's four
FIRST_LAGS = ((0, 0.0), (2, 0.0), (4, 0.65), (6, 5.0), (8, 60.0))   # (bars into the row, ms the late ear is behind): a straight line up to 0.65 ms (a head), then by ratio
FIRST_LATE_DB = 6.0                                       # in the second row the late ear's click is this much louder
FIRST_GAIN = os.environ.get("C11T5_FIRST_GAIN", "-8dB")
FIRST_VEL = 0.5
TRIM = os.environ.get("C11T5_TRIM", "1") != "0" and FIRST   # v12: the click's two notes turned down (they were 10 and 12 dB over the rest of the record)
TRIM_CUTS = ((659.26, float(os.environ.get("C11T5_TRIM_1", "-4"))), (1977.77, float(os.environ.get("C11T5_TRIM_3", "-5"))))   # (Hz, dB): E5 and its third partial
TRIM_Q = 3
TRIM_IN = (2, 8)                                          # bars over which the cut comes in: the first two bars are the click as it always was (Ring True's last strings die under them)
TRIM_OUT = (176 + (HUG_ROWS * ROW if HUG else 0), 184 + (HUG_ROWS * ROW if HUG else 0))                                     # ... and goes out again: the last sixteen bars are the click as it was (Small Change comes in under them)


PAIR = os.environ.get("C11T5_PAIR", "1") != "0" and TRIM   # v13: the second one sounds louder (an accent made of time alone)
PAIR_PLAN = (("turned around", 0, 3.1), ("never arrives", 2, 3.2), ("not there", 4, 4.7), ("the wrong one again", 6, 6.2), ("all three", 0, 3.1))   # (section, dB by which the SECOND stroke is really down AT THE EAR, dB the master takes off it there: measured, so it is written that much up) ; not "round the click": the drum goes round there and would land on a stroke
PAIR_AT = (1, 9)                                          # the sixteenths of a bar on which a pair starts: the one after beats one and three (never ON the drum: the master takes 9 dB off what falls with it)
PAIR_GAP = 2                                              # sixteenths from a pair's first stroke to its second: 240 ms, which is 360 of the engine's loudness steps exactly, so the two are the same to the sample
PAIR_NOTE = "A3"
PAIR_VEL = 0.6                                            # the first stroke's velocity (the second's goes up to 1.43 times it)
PAIR_LIFT = os.environ.get("C11T5_PAIR_LIFT", "1") != "0"  # 0: the two are written the same to the sample, and the master makes the second 3 to 6 dB less
PAIR_GAIN = os.environ.get("C11T5_PAIR_GAIN", "-7dB")        # the first stroke 6 dB under the song's own click in the master (over 1.5 kHz, in its first 25 ms). At 4 dB more it was 2.3 dB under it; at 4 dB less the scorer hardly saw it       # at -8 a stroke was 2.3 dB under the song's own click in the master (which holds the click down and lets a small one through): 8 dB down


def hug_span():
    """(first bar, the bar after the last) of "in the noise", or None."""
    sec = next((x for x in SECS if x[0] == "in the noise"), None)
    return (sec[1], sec[1] + sec[2]) if sec else None


def hug_hz(name):
    pc = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[name[0]] + (1 if "#" in name else -1 if "b" in name[1:] else 0)
    return 440.0 * 2 ** ((pc - 9) / 12 + int(name[-1]) - 4)


def hug_tune():
    """(beat, note, Hz) of every note of the tune, all through the section: it is said as often as it fits."""
    b0, b1 = hug_span()
    return [(b0 * BEATS + i * HUG_BEATS, HUG_TUNE[i % len(HUG_TUNE)], hug_hz(HUG_TUNE[i % len(HUG_TUNE)])) for i in range((b1 - b0) * BEATS // HUG_BEATS)]


def hug_lane():
    """Where the all-pass filter is, in octaves from HUG_BASE: it steps from note to note in a fiftieth of a beat."""
    pts = [(0.0, math.log2(hug_tune()[0][2] / HUG_BASE))]
    for t, n, f in hug_tune():
        pts += [(t, math.log2(f / HUG_BASE)), (t + HUG_BEATS - 0.02, math.log2(f / HUG_BASE))]
    return [[f"{x:g}b", round(y, 6)] for x, y in pts]


def hug_said():
    b0, b1 = hug_span()
    return [note(t, n, HUG_BEATS * 0.9, 0.8) for t, n, f in hug_tune() if b0 + HUG_SAID[0] <= t / BEATS < b0 + HUG_SAID[1]]


def pair_strokes():
    """Every stroke: (beat, dB it is written DOWN against the first of its pair, 0 the first or 1 the second)."""
    plan = {name: down - (lift if PAIR_LIFT else 0) for name, down, lift in PAIR_PLAN} if PAIR else {}
    out = []
    for name, b0, n, parts in SECS:
        if name in plan:
            for bar in range(b0, b0 + n):
                for s in PAIR_AT:
                    out += [(bar * BEATS + s * STEP, 0.0, 0), (bar * BEATS + (s + PAIR_GAP) * STEP, float(plan[name]), 1)]
    return out


def pair_notes():
    """The patch's loudness goes as the square of the velocity: d dB down is the velocity times 10 ** (-d / 40)."""
    return [{"at": round(at, 7), "len": round(0.03 * BPM / 60, 4), "pitch": PAIR_NOTE, "vel": round(PAIR_VEL * 10 ** (-down / 40), 4)} for at, down, k in pair_strokes()]


def first_span():
    """The bars between which the first one wins, or None."""
    sec = next((x for x in SECS if x[0] == FIRST_IN[0]), None) if FIRST else None
    return (sec[1] + FIRST_IN[1], sec[1] + FIRST_IN[2]) if sec else None


def first_lag(u):
    """ms by which the late ear is behind, u bars into a row."""
    for (u0, l0), (u1, l1) in zip(FIRST_LAGS, FIRST_LAGS[1:]):
        if u0 <= u <= u1:
            x = (u - u0) / (u1 - u0)
            return l0 + (l1 - l0) * x if l0 == 0 else l0 * (l1 / l0) ** x
    return FIRST_LAGS[-1][1]


def first_strokes():
    """(beat, ms the late ear is behind, dB the late ear is louder) of every stroke: the first row out, the second row back."""
    b0, b1 = first_span()
    half = (b1 - b0) / 2
    out = []
    for k in range(0, (b1 - b0) * 16, FIRST_EVERY):
        u = k / 16
        out.append(((b0 * 16 + k) * STEP, first_lag(u) if u < half else first_lag(2 * half - u), 0.0 if u < half else FIRST_LATE_DB))
    return out


def first_notes(late):
    """One ear's clicks: the early ear's on the stroke, the late ear's behind it."""
    return [{"at": round(t + (lag / 1000 * BPM / 60 if late else 0.0), 7), "len": 0.04, "pitch": "C5", "vel": round(FIRST_VEL * (10 ** (db / 20) if late else 1.0), 5)}
            for t, lag, db in first_strokes()]


def fall_span():
    """The bars between which the way down leads up, or None."""
    sec = next((x for x in SECS if x[0] == FALL_IN[0]), None) if FALL else None
    return (sec[1] + FALL_IN[1], sec[1] + FALL_IN[2]) if sec else None


def fall_steps():
    """(beat, which bell of the way down (0 the first, N the last), sixteenths long): the first bell said twice, the N steps down, the last and the first turn about."""
    b0, b1 = fall_span()
    n = (b1 - b0 - 2 * FALL_SAID) * 16 // FALL_EVERY
    assert n % len(FALL_BELLS) == 0, n                        # the last bell must be the first one's name
    out = [((b0 * 16 + st) * STEP, 0, 6) for st in (OFF[0], OFF[2])]
    out += [(((b0 + FALL_SAID) * 16 + OFF[0] + (i - 1) * FALL_EVERY) * STEP, i, FALL_EVERY if i < n else 4) for i in range(1, n + 1)]
    out += [(((b1 - 1) * 16 + st) * STEP, i, ln) for st, i, ln in ((OFF[1], 0, 4), (OFF[2], n, 4), (OFF[3], 0, 2))]
    assert out[1 + n][0] == (b1 - 1) * 16 * STEP, out[1 + n]   # the last step down falls on the last bar's first beat
    return out, n


def fall_mid(i, n):
    """Where the curve is loudest (Hz) at bell i of n."""
    return BOTH_MID * 2.0 ** ((i / n - 1) * FALL_RISE + FALL_TOP)


def fall_octaves(pc, mid):
    """The octaves of a note-name that sound under the curve when it is loudest at mid: (the note, Hz, dB under the curve)."""
    out = []
    for o in range(0, 10):
        f = hz(pc + str(o))
        level = -20 * math.log10(math.e) * math.log2(f / mid) ** 2 / (2 * BOTH_WIDE ** 2)
        if level >= BOTH_FLOOR:
            out.append((pc + str(o), f, level))
    return out


def fall_height(pc, mid):
    """Where a bell's weight is, in octaves over 440 Hz: the mean of its octaves' places, each weighed by its power."""
    w = [(10 ** (lv / 10), math.log2(f / 440.0)) for nm, f, lv in fall_octaves(pc, mid)]
    return sum(a * x for a, x in w) / sum(a for a, x in w)


def fall_notes():
    steps, n = fall_steps()
    return [{"at": round(at, 4), "len": round(ln * STEP, 4), "pitch": nm, "vel": round(FALL_VEL * 10 ** (lv / 20), 5)}
            for at, i, ln in steps for nm, f, lv in fall_octaves(FALL_BELLS[i % len(FALL_BELLS)], fall_mid(i, n))]


def BOTH_STEPS(bar):
    """Two bars a phrase: three bells said on the click's strokes (climbing in the odd phrases, falling in the even), then the answer."""
    said = BOTH_UP if (bar % ROW) // 2 % 2 == 0 else BOTH_DOWN
    if bar % 2 == 0:
        return [(OFF[i], p, 3, 0.72) for i, p in enumerate(said)]
    return [(OFF[0], BOTH_PAIR[0], 6, 0.85), (OFF[2], BOTH_PAIR[1], 6, 0.85)]


def LINE_STEPS(bar):
    """A on every eighth (louder with the click), B on the sixteenth after each click: A B A . from the click."""
    b = LINE_B[bar % ROW]
    return sorted([(st, LINE_A, 1, 0.8 if st in OFF else 0.66) for st in range(0, 16, 2)] + [(st + 1, b, 1, 0.8) for st in OFF])


CLAPX = lambda bar: [(6, "C4", 1, 0.8), (14, "C4", 1, 0.86)]     # two and four of the wrong beat


CHOP = lambda bar: [(s, p, 1, 0.8) for s in HELD_ON for p in HELD_CHORD]                      # the chord, with its holes
FENCE = lambda bar: [(s, "A4", 1, 0.8) for s in range(16) if s not in HELD_ON]                # a noise in every hole


def kick_on(k):
    """The bass drum on sixteenth k of every beat (0 is KICK)."""
    return lambda bar: [(s, "A1", 1, 0.95 if s == k else 0.9) for s in (k, k + 4, k + 8, k + 12)]


def clap_on(k):
    """Two and four of the beat that drum makes."""
    return lambda bar: [(k + 4, "C4", 1, 0.8), (k + 12, "C4", 1, 0.86)]


def moved(name, on):
    """The strokes of the rows in which the drum stands somewhere else, in time order with the part's own."""
    return sum((part(f"{name}{k}", on(k)) for k in ROUND_AT), []) if ROUND else []

PATCHES = {
    "ht-kick": {"about": "Hearing Things' bass drum (chirper-zero, 26 Nov): the engine's machine kick, short and dry, on A1: the only thing on the record under 100 Hz but for eight bars.",
                "play": {"vel_sens": 0.3},
                "synth": {"layers": [{"type": "machine", "machine": {"part": "kick", "decay": "260ms", "click": 0.6, "drive": 0.35, "punch": 22, "punch_time": "32ms"}}],
                          "filters": ["hp cutoff=28"], "amp": {"a": "0.1ms", "d": "0s", "s": 1, "r": "1s"}}},
    "ht-tick": {"about": "Hearing Things' click (chirper-zero, 26 Nov): the machine's rim, 35 ms, on E5; on the off-beats from the first bar to the last.",
                "play": {"vel_sens": 0.5},
                "synth": {"layers": [{"type": "machine", "machine": {"part": "rim", "decay": "35ms"}}], "filters": ["hp cutoff=400"], "amp": {"a": "0.1ms", "d": "0s", "s": 1, "r": "200ms"}}},
    "ht-hat": {"about": "Hearing Things' hat (chirper-zero, 26 Nov): the machine's hat, 28 ms, above 5 kHz, whose loudness is all velocity: the Risset rhythm's layers are told apart by nothing else.",
               "play": {"vel_sens": 1.0},
               "synth": {"layers": [{"type": "machine", "machine": {"part": "hat", "decay": "28ms"}}], "filters": ["hp cutoff=5000"], "amp": {"a": "0.1ms", "d": "0s", "s": 1, "r": "120ms"}}},
    "ht-shep": {"about": "Hearing Things' rising voice (chirper-zero, 26 Nov, v2): a small struck tone (a sine with two bar-like partials, 70 ms), whose loudness is all velocity and whose pitch rides the lane `rise` (semitones): one layer of the Shepard-Risset hat.",
                "play": {"vel_sens": 1.0},
                "synth": {"layers": ["sine", "sine ratio=2.76 level=-10dB", "sine ratio=5.4 level=-18dB"], "pitch": {"value": 0, "mod": [{"src": "auto.rise", "amount": 1}]},
                          "amp": {"a": "0.3ms", "d": "70ms", "s": 0, "r": "20ms", "curve": 3}}},
    "ht-pip": {"about": "Hearing Things' pip (chirper-zero, 26 Nov, v5): a plain tone with a little of its octave, 90 ms: plain enough that two of them are told apart by pitch and by nothing else.",
               "play": {"vel_sens": 0.4},
               "synth": {"layers": ["sine", "sine ratio=2 level=-20dB"], "amp": {"a": "2ms", "d": "85ms", "s": 0, "r": "25ms", "curve": 3}}},
    "ht-chop": {"about": "Hearing Things' chord (chirper-zero, 26 Nov, v4): a plain sine a note, switched on in a millisecond and off in three, so that a sixteenth of it is a sixteenth and its holes are holes.",
                "play": {"vel_sens": 0.2},
                "synth": {"layers": ["sine"], "amp": {"a": "1ms", "d": "0s", "s": 1, "r": "3ms"}}},
    "ht-fence": {"about": f"Hearing Things' fence (chirper-zero, 26 Nov, v4): white noise between {HELD_BAND[0]} and {HELD_BAND[1]} Hz, switched as the chord is: it fills the chord's holes exactly, in the chord's band, louder than the chord.",
                 "play": {"vel_sens": 0.2},
                 "synth": {"layers": ["white"], "filters": [f"hp cutoff={HELD_BAND[0]}", f"hp cutoff={HELD_BAND[0]}", f"lp cutoff={HELD_BAND[1]}", f"lp cutoff={HELD_BAND[1]}"], "amp": {"a": "1ms", "d": "0s", "s": 1, "r": "3ms"}}},
    "ht-clap": {"about": "Hearing Things' clap (chirper-zero, 26 Nov): the machine's clap, three bursts, short, dry.",
                "play": {"vel_sens": 0.4},
                "synth": {"layers": [{"type": "machine", "machine": {"part": "clap", "bursts": 3, "decay": "140ms"}}], "amp": {"a": "0.1ms", "d": "0s", "s": 1, "r": "400ms"}}},
    "ht-bass": {"about": "Hearing Things' bass (chirper-zero, 26 Nov): the second to sixth harmonics of the note and nothing at the note itself (after the library's phantom-bass): the ear supplies the pitch.",
                "play": {"mono": True, "gate": 0.85, "vel_sens": 0.5},
                "synth": {"layers": [{"type": "additive", "partials": [[2, 1.0], [3, 0.85], [4, 0.6], [5, 0.42], [6, 0.3]]}],
                          "env": {"f": {"a": "1ms", "d": "160ms", "s": 0}},
                          "filters": [{"kind": "lp", "cutoff": {"value": 1800, "mod": [{"src": "env.f", "amount": 1.2}]}, "q": 0.8}],
                          "amp": {"a": "2ms", "d": "320ms", "s": 0.55, "r": "60ms", "curve": 3}}},
}


def song():
    pump = {"type": "pump", "on": "kick", "depth": "-4dB", "attack": "2ms", "release": "160ms", "curve": 0.7}
    doc = {
        "about": "Chirpers - Escapement, track 5 by chirper-zero: HEARING THINGS. Three things that are not on the record: a beat that turns around (the click and the bass are on the off-beats from the first bar; the bass drum says so later), a bass with nothing at its own pitch (harmonics two to six), and a hat that speeds up through every row and starts the next where it started the last (a Risset rhythm in four layers). Generated by compose/chirpers11/src/chirpers11-t5.py.",
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
            {"name": "kick", "patch": "ht-kick", "gain": "-8dB", "pan": 0.0, "notes": sorted(part("kick", KICK) + moved("k", kick_on), key=lambda n: n["at"]) if ROUND else part("kick", KICK)},
            {"name": "tick", "patch": "ht-tick", "gain": "-2dB", "pan": 0.0, "sends": {"room": "-14dB"}, "notes": part("tick", TICK)},
            {"name": "bass", "patch": "ht-bass", "gain": "-11dB", "pan": 0.0, "fx": [pump], "notes": part("bass", BASS)},
            {"name": "sub", "patch": "sub-sine", "gain": "-10dB", "pan": 0.0, "fx": [pump], "notes": part("sub", BASS)},
            {"name": "clap", "patch": "ht-clap", "gain": "-5dB", "pan": 0.0, "sends": {"room": "-10dB"}, "notes": sorted(part("clap", CLAP) + part("clapx", CLAPX) + moved("c", clap_on), key=lambda n: n["at"])},
            {"name": "ris", "patch": "ht-hat", "gain": "6dB", "pan": 0.0, "sends": {"room": "-16dB"}, "notes": sorted(ris_notes("ris") + ris_notes("sir", back=True), key=lambda n: n["at"])},
        ],
    }
    if SHEP:
        lane = rise_lane()
        doc["tracks"] += [{"name": f"shep{j}", "patch": "ht-shep", "gain": "-13dB", "pan": 0.15, "sends": {"room": "-14dB"}, "auto": {"rise": {"points": lane}}, "notes": shep_notes(j)} for j in range(LAYERS)]
        doc["about"] = doc["about"].replace(" Generated by", " From v2 each layer of the hat has a small tone of its own that climbs an octave a row, so it is faster and higher for ever. Generated by")
    else:
        del PATCHES["ht-shep"]
    if BOTH:
        for pc in sorted(set(BOTH_PAIR + BOTH_UP + BOTH_DOWN)) + ([p for p in STAIR if p not in BOTH_PAIR + BOTH_UP + BOTH_DOWN] if STAIRS else []):
            PATCHES[f"ht-both-{pc}"] = {"about": f"Hearing Things' bell with no octave (chirper-zero, 26 Nov, v6), on {pc}: {pc} in every octave at once under one fixed curve (loudest at {BOTH_MID:g} Hz, {BOTH_WIDE:g} octaves wide), so it has a note-name and no height. One patch a note-name: the curve stays where it is and the octaves move under it. Every octave starts at the same instant of its cycle, so two strokes of one bell are the same samples.",
                                        "play": {"vel_sens": 0.3},
                                        "synth": {"layers": [f"sine phase=0 ratio={r:g} level={lv:.1f}dB" for r, f, lv in both_octaves(pc)], "amp": {"a": "4ms", "d": "420ms", "s": 0, "r": "90ms", "curve": 3}}}
            if pc not in BOTH_PAIR + BOTH_UP + BOTH_DOWN:
                continue                                                                                            # a bell only the stairs use: its patch, and no track here
            doc["tracks"].append({"name": f"both-{pc}", "patch": f"ht-both-{pc}", "gain": BOTH_GAIN, "pan": 0.0,      # dry and in the middle: a room gives each octave its own colour, and then the bell has a height
                                  "notes": part("both", lambda bar, pc=pc: [(st, pc + "3", n, v) for st, p, n, v in BOTH_STEPS(bar) if p == pc])})
        if STAIRS:
            for pc in STAIR:
                doc["tracks"].append({"name": f"stair-{pc}", "patch": f"ht-both-{pc}", "gain": STAIR_GAIN, "pan": 0.0,      # dry and in the middle, as the answer's bells are
                                      "notes": part("stair", lambda bar, pc=pc: [(st, pc + "3", n, v) for st, p, n, v in STAIR_STEPS(bar) if p == pc])})
            doc["about"] = doc["about"].replace(" Generated by", " From v7 the same bells are stairs, in the first two rows of never arrives: B, D, F, A flat, a minor third from each to the next and from the last to the first, so every step is heard to rise and the fifth bell is the first again (Shepard's scale). Generated by")
            assert "From v7" in doc["about"]
        doc["about"] = doc["about"].replace(" Generated by", " From v6 a bell with no octave says B C D and is answered B F, then B A G and the same answer: the same two strokes are heard going up the first time and down the second (the tritone paradox, set by what was just heard). Generated by")
    if rabbit():
        for nm, side in (("rab-l", -1), ("rab-r", 1)):        # two places and no others; dry: a room would put every click everywhere
            doc["tracks"].append({"name": nm, "patch": "ht-tick", "gain": RAB_GAIN, "pan": side * RAB_PAN,
                                  "notes": [note(t, RAB_NOTE, STEP / 4, RAB_VEL) for t, sd in rabbit() if sd == side]})
        doc["about"] = doc["about"].replace(" Generated by", " From v8 a click struck four times on the left and four on the right, faster each time, is heard to hop across through places where nothing was struck (saltation: the rabbit), in the bar where the drum rests at the end of each row of round the click. Generated by")
        assert "From v8" in doc["about"]
    if pulse_span():
        lo, hi = pulse_span()
        apart, lift = pulse_lanes()
        for i, (b0, b1, rate) in enumerate(PULSE_RATES):
            for nm, side in (("l", -1), ("r", 1)):          # dry: a room would put each ear's tone in the other
                PATCHES[f"ht-ear-{i + 1}{nm}"] = {"about": f"Hearing Things' tone for one ear (chirper-zero, 26 Nov, v9): one sine, {rate * BPM / 120:.4g} Hz {'under' if side < 0 else 'over'} the note it is played on; its twin is as far the other way, so the two are {rate:g} cycles a beat apart and start together.",
                                                 "play": {"gate": 1},      # a note sounds for 95% of its written length unless the patch says otherwise (the engine's `play.gate`)
                                                 "synth": {"layers": [f"sine phase=0 ratio={pulse_ratio(rate, side):.9f}"], "amp": {"a": "100ms", "d": "0s", "s": 1, "r": "150ms"}}}
                doc["tracks"].append({"name": f"ear{i + 1}-{nm}", "patch": f"ht-ear-{i + 1}{nm}", "gain": f"{PULSE_GAIN:g}dB", "pan": {"value": 0, "mod": [{"src": "auto.apart", "amount": side}]},
                                      "auto": {"apart": {"points": apart, "curve": 0}, "lift": {"points": lift, "curve": 0}},
                                      "fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.lift", "amount": 1}]}}],
                                      "notes": [note(lo + b0 * BEATS, PULSE_NOTE, (b1 - b0) * BEATS - (0 if i + 1 < len(PULSE_RATES) else PULSE_END), 0.8)]})
        doc["about"] = doc["about"].replace(" Generated by", " From v9 there is a pulse in not there that is not on the record: two plain tones either side of A4, three cycles a beat apart, beat in the middle (a real beat, a triplet), then go apart to an ear each, where each is steady and the pulse is heard all the same (a binaural beat); in the last row they are a cycle and a half a beat apart. Generated by")
        assert "From v9" in doc["about"]
    if scale_span() and APART:
        for nm, side in (("scale-l", -1), ("scale-r", 1)):          # an ear each, dry: a room would put each ear's part in the other
            doc["tracks"].append({"name": nm, "patch": "ht-pip", "gain": SCALE_GAIN, "pan": side, "notes": scale_notes(side)})
        doc["about"] = doc["about"].replace(" Generated by", " From v10 the scale of A minor goes up and down at once, its notes dealt to the two ears turn about, so each ear is given a jagged tune and neither a scale; two smooth lines are heard, the high in one ear and the low in the other (the scale illusion). Each ear's part is heard alone first. Generated by")
        assert "From v10" in doc["about"]
    if first_span():
        PATCHES["ht-snap"] = {"about": "Hearing Things' small wooden click (chirper-zero, 26 Nov, v12): three plain tones that start at nought (the note, and bar-partials 2.76 and 5.4 times it) and are gone in 14 ms. Nothing in it is noise, so two of them are the same to the sample: one for each ear.",
                              "play": {"vel_sens": 0.5, "gate": 1},
                              "synth": {"layers": ["sine phase=0 level=-3dB", "sine phase=0 ratio=2.76 level=-6dB", "sine phase=0 ratio=5.4 level=-10dB"], "amp": {"a": "0.1ms", "d": "14ms", "s": 0, "r": "6ms", "curve": 2}}}
        for nm, pan, late in (("first-l", -1, False), ("first-r", 1, True)):
            doc["tracks"].append({"name": nm, "patch": "ht-snap", "gain": FIRST_GAIN, "pan": pan, "notes": first_notes(late)})      # dry, an ear each
        doc["about"] = doc["about"].replace(" Generated by", " From v12 a small wooden click in held is given to both ears, the same click and as loud in each, and the right ear gets it later and later: at 0.65 ms it has walked to the left, up to 5 ms it is still one click there, and then it comes apart into a click and its echo; and back, with the late ear twice as loud (the law of the first wavefront)." + (" The click's own two notes (E5 and its third partial) are turned down 4 and 5 dB from bar 9 to bar 176 (the first two bars and the last sixteen have it as it was)." if TRIM else "") + " Generated by")
        assert "From v12" in doc["about"]
    if TRIM:
        tk = PATCHES["ht-tick"]
        PATCHES["ht-tick-t"] = {"about": "Hearing Things' click with its two notes turned down (chirper-zero, 26 Nov, v12): `ht-tick`, and a narrow cut at E5 and at its third partial. The rim's snap is as it was.",
                                "play": dict(tk["play"]), "synth": {**tk["synth"], "filters": list(tk["synth"]["filters"]) + [{"kind": "peak", "cutoff": f, "q": TRIM_Q, "gain": {"value": "0dB", "mod": [{"src": "auto.trim", "amount": g}]}} for f, g in TRIM_CUTS]}}
        for t in doc["tracks"]:
            if t["name"] == "tick":
                t["patch"] = "ht-tick-t"
                t["auto"] = {"trim": {"points": [[f"{x:g}b", y] for x, y in ((0, 0), (TRIM_IN[0] * BEATS, 0), (TRIM_IN[1] * BEATS, 1), (TRIM_OUT[0] * BEATS, 1), (TRIM_OUT[1] * BEATS, 0), (TOTAL, 0))], "curve": 0}}      # 0 the click as it was, 1 the whole cut
    if hug_span():
        b0, b1 = hug_span()
        PATCHES["ht-hiss"] = {"about": "Hearing Things' noise (chirper-zero, 27 Nov, v14): pink noise, held. One track of it goes to two buses, an ear each, so both ears have the same samples; the right ear's bus has an all-pass filter on it and nothing else.",
                              "play": {"vel_sens": 0, "gate": 1}, "synth": {"layers": ["pink"], "amp": {"a": "40ms", "d": "0s", "s": 1, "r": "60ms"}}}
        PATCHES["ht-said"] = {"about": "Hearing Things' plain tone (chirper-zero, 27 Nov, v14): one sine, for saying aloud the tune that was between the ears.",
                              "play": {"vel_sens": 0}, "synth": {"layers": ["sine"], "amp": {"a": "40ms", "d": "0s", "s": 1, "r": "120ms"}}}
        doc["buses"]["ear-l"] = {"pan": -1}
        doc["buses"]["ear-r"] = {"pan": 1, "fx": [{"type": "filter", "kind": "allpass", "cutoff": {"value": HUG_BASE, "mod": [{"src": "auto.tune", "amount": 1}]}, "q": HUG_Q}],
                                 "auto": {"tune": {"points": hug_lane(), "curve": 0}}}
        doc["tracks"].append({"name": "hiss", "patch": "ht-hiss", "gain": HUG_GAIN, "pan": 0.0, "out": "ear-l", "sends": {"ear-r": "0dB"},
                              "notes": [{"at": float(b0 * BEATS), "len": float((b1 - b0) * BEATS), "pitch": "A4", "vel": 0.8}]})      # one noise, to an ear each
        doc["tracks"].append({"name": "said", "patch": "ht-said", "gain": HUG_SAID_GAIN, "pan": 0.0, "notes": hug_said()})                # dry, in the middle
        doc["about"] = doc["about"].replace(" Generated by", " From v14 there is a section after held, in the noise: both ears are given the same noise, but the right ear's has been through an all-pass filter that turns the phase a whole turn at one frequency and changes no loudness anywhere. Each ear has plain noise; between them there is a faint note at that frequency, and it is moved through a tune (A C E A, A E C A) that neither ear is given. The second time the tune is also played quietly by a plain tone, so that one speaker has it too. Generated by")
        assert "From v14" in doc["about"]
    if pair_strokes():
        PATCHES["ht-two"] = {"about": "Hearing Things' pair (chirper-zero, 26 Nov, v13): a small dry wooden click with no noise in it, so that two of them are the same click to the sample: a saw from phase nought with everything under 700 Hz taken off, 16 ms. Its loudness is the square of its velocity and nothing else.",
                             "play": {"vel_sens": 1},
                             "synth": {"layers": ["saw phase=0"], "filters": [{"kind": "hp", "cutoff": 700, "q": 0.7}], "amp": {"a": "0.1ms", "d": "16ms", "s": 0, "r": "8ms", "curve": 3}}}
        doc["tracks"].append({"name": "two", "patch": "ht-two", "gain": PAIR_GAIN, "pan": 0.0, "notes": pair_notes()})      # dry, in the middle
        doc["about"] = doc["about"].replace(" Generated by", " From v13 two small clicks that are the same click to the sample come two sixteenths apart, either side of the song's click on beats one and three: the second is heard as the loud one (an accent made of time alone), and section by section it is really turned down, 0, 2, 4 and 6 dB, until the two sound equal or the first wins. Generated by")
        assert "From v13" in doc["about"]
    if fall_span():
        PATCHES["ht-part"] = {"about": "Hearing Things' part of a bell (chirper-zero, 26 Nov, v11): one plain tone with the v6 bells' own shape, and its loudness is its velocity and nothing else. A bell is made of one of these for every octave of its note, so the curve the octaves are under can be somewhere else at every bell.",
                              "play": {"vel_sens": 0.5},
                              "synth": {"layers": ["sine phase=0"], "amp": {"a": "4ms", "d": "420ms", "s": 0, "r": "90ms", "curve": 3}}}
        doc["tracks"].append({"name": "fall", "patch": "ht-part", "gain": FALL_GAIN, "pan": 0.0, "notes": fall_notes()})      # dry and in the middle, as the stairs are
        doc["about"] = doc["about"].replace(" Generated by", " From v11 the bells go down for six bars in all three, three semitones a step, while the curve they are under climbs an octave: forty-eight steps down, and the last bell is the first one's name and higher than it (Risset's paradox). The first bell is said before and the two side by side after. Generated by")
        assert "From v11" in doc["about"]
    if WES:
        assert sum(WES_PLAN) == WES_BARS[1] - WES_BARS[0] and (WES_BARS[1] - WES_BARS[0]) * 16 % (2 * len(WES_NOTES)) == 0
        PATCHES["ht-wes"] = {"about": "Hearing Things' two hands (chirper-zero, 27 Nov, v15): a short pip, a saw through two low-pass stages that the lane `apart` opens (0: 1000 Hz, nearly a plain tone; 1: 11.3 kHz, a buzz). Two tracks play it turn about; while both lanes are 0 they are one sound.",
                             "play": {"vel_sens": 0.4},
                             "synth": {"layers": ["saw"], "filters": [{"kind": "lp", "cutoff": {"value": WES_BASE, "mod": [{"src": "auto.apart", "amount": WES_OCT}]}, "q": 0.7}, {"kind": "lp", "cutoff": {"value": WES_BASE, "mod": [{"src": "auto.apart", "amount": WES_OCT}]}, "q": 0.7}],
                                       "amp": {"a": "1ms", "d": "60ms", "s": 0, "r": "20ms", "curve": 3}}}
        for hand, nm in ((0, "wes-a"), (1, "wes-b")):
            doc["tracks"].append({"name": nm, "patch": "ht-wes", "gain": WES_GAIN, "pan": -0.15, "sends": {"room": "-14dB"}, "auto": {"apart": wes_lane(hand)}, "notes": wes_notes(hand)})      # where the line is, and in its room
        doc["about"] = doc["about"].replace(" Generated by", " From v15, in bars 3 to 8, a pip climbs three notes (A C E) over and over, a sixteenth each, shared turn about between two hands; when the second hand's sound is made brighter the one climbing line is heard as two lines, each going down (Wessel's illusion). Generated by")
        assert "From v15" in doc["about"]
    if APART:
        doc["tracks"].append({"name": "line", "patch": "ht-pip", "gain": "-12dB", "pan": -0.15, "sends": {"room": "-14dB"}, "notes": part("line", LINE_STEPS)})
        doc["about"] = doc["about"].replace(" Generated by", " From v5 a pip plays three strokes and a rest (A B A .) and B moves away from A a third, a fifth, an octave, and back: no stroke moves, and the one galloping line comes apart into two even ones (stream segregation). Generated by")
    else:
        del PATCHES["ht-pip"]
    if HELD:
        doc["tracks"] += [{"name": "chop", "patch": "ht-chop", "gain": "-38dB", "pan": 0.0, "notes": part("chop", CHOP)},      # dry: a room would fill its holes
                          {"name": "fence", "patch": "ht-fence", "gain": "-3dB", "pan": 0.0, "notes": part("fence", FENCE)}]
        doc["about"] = doc["about"].replace(" Generated by", " From v4 there is a chord with a hole in every other sixteenth; when a noise is put in the holes it is heard held, unbroken (the continuity illusion). Generated by")
    else:
        del PATCHES["ht-chop"], PATCHES["ht-fence"]
    if ROUND:
        doc["about"] = doc["about"].replace(" Generated by", " From v3 the drum goes round the click a sixteenth a row (just before it, on it, just after it, then the true beat), so the same click is heard as every sixteenth of the beat and never moves. Generated by")
    if FILL:
        bars = sorted({int(n["at"] // BEATS) for t in doc["tracks"] if t["name"] == FILL_WITH for n in t["notes"]})
        PATCHES["ht-grain"] = {"about": "Hearing Things' filler (chirper-zero, 27 Nov, v16): a 12 ms grain of noise over 2.8 kHz, small and dry: something that happens in a beat and is nothing else. It keeps out of the click's own bands (660 Hz and 2 kHz).",
                               "play": {"vel_sens": 0.5},
                               "synth": {"layers": ["white"], "filters": ["hp cutoff=2800", "hp cutoff=2800", "lp cutoff=11000"], "amp": {"a": "0.1ms", "d": "12ms", "s": 0, "r": "6ms", "curve": 2}}}
        doc["tracks"].append({"name": "fill", "patch": "ht-grain", "gain": FILL_GAIN, "pan": FILL_PAN, "notes": fill_notes(bars)})      # dry
        doc["about"] = doc["about"].replace(" Generated by", f" From v16, wherever the line plays, the beat after each loud click is filled with {FILL_N} small dry ticks and the beat after each soft click is left empty: every beat is the same length, and the full ones are heard as longer (the filled-duration illusion). Generated by")
        assert "From v16" in doc["about"]
    if CRACK and first_span():
        PATCHES["ht-crack"] = {"about": f"Hearing Things' crack (chirper-zero, 27 Nov, v17): {CRACK_TONES} plain tones from {CRACK_FROM:g} to {CRACK_FROM * CRACK_STEP ** (CRACK_TONES - 1):.1f} times the note, each {CRACK_STEP:g} times the last, all starting at nought and gone in {CRACK_DECAY}: a broad click with no noise in it, so two of them are the same to the sample: one for each ear.",
                               "play": {"vel_sens": 0.5, "gate": 1},
                               "synth": {"layers": [f"sine phase=0 ratio={CRACK_FROM * CRACK_STEP ** ck_k:.3f} level={-3 - CRACK_TILT * ck_k:g}dB" for ck_k in range(CRACK_TONES)], "amp": {"a": "0.1ms", "d": CRACK_DECAY, "s": 0, "r": "3ms", "curve": 2}}}
        for ck_nm, ck_pan, ck_late in (("crack-l", -1, False), ("crack-r", 1, True)):
            doc["tracks"].append({"name": ck_nm, "patch": "ht-crack", "gain": CRACK_GAIN, "pan": ck_pan, "notes": first_notes(ck_late)})      # dry, an ear each: the wooden click's own strokes and lags
        doc["about"] = doc["about"].replace(" Generated by", " From v17 each of those strokes carries a crack as well (ten plain tones from 2.4 to 9.2 kHz, gone in 5 ms; the same in both ears to the sample): the law is measured with clicks, and a crack comes apart into two sooner than the wooden click does. Generated by")
        assert "From v17" in doc["about"]
    if OCT and oct_span():
        PATCHES["ht-oct"] = {"about": "Hearing Things' tone for the octave illusion (chirper-zero, 27 Nov, v18): one plain sine, held for the whole of its note and handed to the next over 6 ms, as Deutsch's were: nothing in it but its pitch.",
                             "play": {"vel_sens": 0, "gate": 1},
                             "synth": {"layers": ["sine phase=0"], "amp": {"a": "6ms", "d": "0s", "s": 1, "r": "6ms"}}}
        for ot_nm, ot_side in (("oct-l", -1), ("oct-r", 1)):            # an ear each, dry: a room would put each ear's notes in the other
            doc["tracks"].append({"name": ot_nm, "patch": "ht-oct", "gain": OCT_GAIN, "pan": ot_side, "notes": oct_notes(ot_side)})
        doc["about"] = doc["about"].replace(" Generated by", f" From v18, in the first eight bars of turned around, two plain notes an octave apart ({OCT_NOTES[0]} and {OCT_NOTES[1]}) change ears every eighth: each ear is given both, turn about, and never the one the other has; the left ear's part is heard alone, then the right's, then both, and with both most people hear the high note in one ear only and the low note in the other (Deutsch's octave illusion), whichever way round the headphones are. Generated by")
        assert "From v18" in doc["about"]
    if PARA and para_span():
        for pr_i, pr_p in enumerate(PARA_NOTES):
            PATCHES[f"ht-para-{pr_i + 1}"] = {"about": f"Hearing Things' bell whose octave is a step down (chirper-zero, 27 Nov, v19), written on {pr_p}: plain tones {PARA_APART:g} times apart (a little more than an octave) under one fixed curve (loudest at {PARA_MID:g} Hz, {PARA_WIDE:g} octaves wide). One patch a written note: the curve stays where it is; every tone of this bell is twice a tone of the bell written an octave lower, and {1200 * math.log2(PARA_APART / 2):.1f} cents under that bell's next tone.",
                                              "play": {"vel_sens": 0.3},
                                              "synth": {"layers": [f"sine phase=0 ratio={r:.6g} level={lv:.1f}dB" for r, f, lv in para_tones(pr_p)], "amp": {"a": "4ms", "d": "420ms", "s": 0, "r": "90ms", "curve": 3}}}
            doc["tracks"].append({"name": f"para-{pr_i + 1}", "patch": f"ht-para-{pr_i + 1}", "gain": PARA_GAIN, "pan": 0.0,      # dry and in the middle, as the song's other bells are
                                  "notes": [{"at": at, "len": 0.75, "pitch": pr_p, "vel": PARA_VEL} for at, k in para_strokes() if k == pr_i]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v19, in the first row of round the click, a bell whose tones are {PARA_APART:g} times apart is written an octave higher at every click ({PARA_NOTES[0]} to {PARA_NOTES[-1]}) and back: each octave up is heard as a small semitone down (Risset's paradox). Generated by")
        assert "From v19" in doc["about"]
    if VOX and vox_span():
        vx_b0, vx_b1 = vox_span(); vx_gain = float(VOX_GAIN.replace("dB", ""))
        for vx_k in range(1, VOX_PARTS + 1):
            PATCHES[f"ht-vox-{vx_k}"] = {"about": f"Hearing Things' held note, tone {vx_k} of {VOX_PARTS} (chirper-zero, 27 Nov, v20): one plain sine at {vx_k} times {VOX_NOTE} ({hz(VOX_NOTE) * vx_k:.1f} Hz), held as long as its note, whose pitch follows the lane `vib` (semitones). The note is all {VOX_PARTS} together; a voice is the ones that waver together.",
                                         "play": {"gate": 1, "vel_sens": 0},
                                         "synth": {"layers": [f"sine phase=0 ratio={vx_k}"], "pitch": {"value": 0, "mod": [{"src": "auto.vib", "amount": 1}]}, "amp": {"a": "400ms", "d": "0ms", "s": 1, "r": "600ms"}}}
            doc["tracks"].append({"name": f"vox-{vx_k}", "patch": f"ht-vox-{vx_k}", "gain": f"{vx_gain - 20 * math.log10(vx_k) * VOX_ROLL:.2f}dB", "pan": 0.0,
                                  "notes": [{"at": vx_b0 * BEATS, "len": (vx_b1 - vx_b0) * BEATS, "pitch": VOX_NOTE, "vel": 0.8}], "auto": {"vib": {"points": vox_lane(vx_k)}}})
        doc["about"] = doc["about"].replace(" Generated by", f" From v20 one low note ({VOX_NOTE}: {VOX_PARTS} plain tones, its multiples) is held through the first row of held, and from its third bar some of its tones waver together, every third, fourth, sixth, fourth, third, second, a bar each: nothing is added and nothing gets louder, and the ones that waver are heard as a second voice singing the note they are the multiples of (McAdams 1984): a tune that is written nowhere. Generated by")
        assert "From v20" in doc["about"]
    if cross_spans():
        cr_amp = {"a": "30ms", "d": "0ms", "s": 1, "r": "80ms"}; cr_pitch = {"value": 0, "mod": [{"src": "auto.glide", "amount": 1}]}
        PATCHES["ht-cross"] = {"about": "Hearing Things' line (chirper-zero, 27 Nov, v21): one plain tone, held, whose note is drawn by its track's lane (`auto.glide`, in semitones): a straight line in pitch.",
                               "play": {"gate": 1, "vel_sens": 0}, "synth": {"layers": ["sine phase=0"], "pitch": cr_pitch, "amp": cr_amp}}
        PATCHES["ht-cross-d"] = {"about": "Hearing Things' other line (chirper-zero, 27 Nov, v21): `ht-cross` begun " + f"{CROSS_PHASE:g}" + " of a turn into its wave, so that the two are in step at the moment they cross.",
                                 "play": {"gate": 1, "vel_sens": 0}, "synth": {"layers": [f"sine phase={CROSS_PHASE:g}"], "pitch": cr_pitch, "amp": cr_amp}}
        cr = cross_spans()
        doc["tracks"].append({"name": "cross-up", "patch": "ht-cross", "gain": CROSS_GAIN, "pan": 0.0, "notes": [note(b0, CROSS_LOW, b1 - b0, 0.8) for b0, b1, t in cr if not t], "auto": {"glide": {"points": cross_lane(1, False), "curve": 0}}})
        doc["tracks"].append({"name": "cross-down", "patch": "ht-cross-d", "gain": CROSS_GAIN, "pan": 0.0, "notes": [note(b0, CROSS_HIGH, b1 - b0, 0.8) for b0, b1, t in cr], "auto": {"glide": {"points": cross_lane(-1, None), "curve": 0}}})
        if any(t for _, _, t in cr):
            doc["tracks"].append({"name": "cross-told", "patch": "ht-cross", "gain": f"{float(CROSS_GAIN.replace('dB', '')) + CROSS_LIFT:g}dB", "pan": 0.0, "fx": [{"type": "tremolo", "rate": CROSS_FLUTTER[0], "depth": CROSS_FLUTTER[1]}],
                                  "notes": [note(b0, CROSS_LOW, b1 - b0, 0.8) for b0, b1, t in cr if t], "auto": {"glide": {"points": cross_lane(1, True), "curve": 0}}})
        doc["about"] = doc["about"].replace(" Generated by", f" From v21, in the {len(cr)} pairs of bars of never arrives that had nothing of their own, two plain tones in one place set out for each other's notes: one from {CROSS_LOW} straight up to {CROSS_HIGH}, one from {CROSS_HIGH} straight down to {CROSS_LOW}, an octave a bar; they cross on A4 a bar in. Neither turns. But the ear follows what is nearest in pitch, and hears the high one come down, touch and go back up, and the low one go up and come back down: two turns that are not there, and neither line arrives. The last time the rising one flutters, and is heard to go straight through. Generated by")
        assert "From v21" in doc["about"]
    if tune_row() is not None:
        if "ht-pip" not in PATCHES:
            raise SystemExit("the tune is played on the song's pip (ht-pip)")
        tn0 = tune_row() * BEATS; tn = tune_notes()
        doc["tracks"].append({"name": "tune", "patch": "ht-pip", "gain": TUNE_GAIN, "pan": TUNE_PAN, "sends": {"room": "-14dB"},
                              "notes": [note(tn0 + t, name, 0.5, TUNE_VEL) for t, name, _, _ in tn]})
        tn_th = [name for t, name, thrown, i in tn if thrown][:8]; tn_pl = [name for t, name, thrown, i in tn if not thrown]
        doc["about"] = doc["about"].replace(" Generated by", f" From v22 a tune everybody knows is played with every note thrown to another octave, and is not known (bars {tune_row() + 1} to {tune_row() + ROW}, the first row of all three, which had nothing of its own): the half hour of the clock in Give or Take, the record's first song. First thrown about ({' '.join(tn_th)}: every NAME is right), then plainly ({' '.join(tn_pl)}), then thrown about again, the same eight notes as before: and now the tune is in them (Deutsch 1972). Generated by")
        assert "From v22" in doc["about"]
    if rep_row() is not None:
        rp_b0 = rep_row(); rp_off = {round(rep_note(x)[1], 4) for _, _, x in REP_STAGES if x}
        assert len(rp_off) == 1, rp_off                         # the stages are octaves of one another: one patch serves them all
        rp_fx = [f"hp cutoff={REP_BAND[0]}"] + [f"lp cutoff={REP_BAND[1]}"] * REP_TOP; rp_amp = {"a": "4ms", "d": "0s", "s": 1, "r": "4ms"}
        PATCHES["ht-run"] = {"about": f"Hearing Things' hiss that never repeats (chirper-zero, 27 Nov, v23): the engine's white noise, held, {REP_BAND[0]} to {REP_BAND[1]} Hz. The other half of a pair: `ht-rep` is as loud, in the same band, and comes round.",
                             "play": {"vel_sens": 0.5, "gate": 1}, "synth": {"layers": ["white"], "filters": rp_fx, "amp": rp_amp}}
        PATCHES["ht-rep"] = {"about": f"Hearing Things' hiss that repeats (chirper-zero, 27 Nov, v23): the engine's chip noise with no chip's clock (`clock: 0`): a 15-bit shift register, {REP_STEPS} steps and then the same steps again, 93 steps to a turn of the note played, tuned {list(rp_off)[0]:+.4f} semitones so that on B5 it comes round every 3 sixteenths at {BPM}, on B4 every 6, on B6 every 1.5. Held, {REP_BAND[0]} to {REP_BAND[1]} Hz. There is no rhythm in it but its length.",
                             "play": {"vel_sens": 0.5, "gate": 1}, "synth": {"layers": [{"type": "chip", "chip": {"kind": "noise", "clock": 0}}], "pitch": {"value": list(rp_off)[0]}, "filters": rp_fx, "amp": rp_amp}}
        rp_vel = lambda x: round(0.7 * 10 ** (REP_TRIM[x] / 20), 4)
        doc["tracks"].append({"name": "run", "patch": "ht-run", "gain": REP_GAIN, "pan": 0.0,
                              "notes": [{"at": (rp_b0 + a0) * BEATS, "len": (a1 - a0) * BEATS, "pitch": "A4", "vel": rp_vel(x)} for a0, a1, x in REP_STAGES if x is None]})
        doc["tracks"].append({"name": "rep", "patch": "ht-rep", "gain": REP_GAIN, "pan": 0.0,
                              "notes": [{"at": (rp_b0 + a0) * BEATS, "len": (a1 - a0) * BEATS, "pitch": rep_note(x)[0], "vel": rp_vel(x)} for a0, a1, x in REP_STAGES if x is not None]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v23 there is a hiss in the row with no hat (bars {rp_b0 + 1} to {rp_b0 + max(a1 for _, a1, _ in REP_STAGES)}): for two bars a hiss that never repeats, then the same kind of hiss, as loud, in the same band, that is only {', '.join(f'{x:g}' for _, _, x in REP_STAGES if x)} sixteenths long and comes round and round. Nothing is struck and its level is not moved: but a noise that repeats is heard to have a pattern in it, each listener's own, and here the pattern is three against the beat's four, then six, then twelve (Guttman and Julesz, 1963). Generated by")
        assert "From v23" in doc["about"]
    if own_row() is not None:
        assert ROW % len(OWN_PHRASES) == 0
        ow = own_phrases(); ow_end = BARS * BEATS
        ow_flat = {"glide": {"points": [["0b", 0], [f"{ow_end:g}b", 0]], "curve": 0}}
        for ow_where, ow_pans in (("mid", (0.0, 0.0)), ("ears", (-1, 1))):
            ow_these = [p for p in ow if p[0] == ow_where]
            if not ow_these:
                continue
            ow_pts = [["0b", 0]]
            for _, _, ow_at, ow_len, ow_s0, ow_s1 in ow_these:
                ow_pts += [[f"{ow_at - 0.05:g}b", round(ow_s0, 4)], [f"{ow_at + ow_len:g}b", round(ow_s1, 4)]]
            ow_pts.append([f"{ow_end:g}b", round(ow_these[-1][5], 4)])
            ow_gain = OWN_GAIN if ow_where == "mid" else f"{float(OWN_GAIN[:-2]) + OWN_EARS:g}dB"
            ow_tail = "" if ow_where == "mid" else ("-l", "-r")
            doc["tracks"].append({"name": "own-lo" + (ow_tail and ow_tail[0]), "patch": "ht-cross", "gain": ow_gain, "pan": ow_pans[0], "auto": ow_flat,
                                  "notes": [{"at": ow_at, "len": ow_len, "pitch": OWN_LOW, "vel": OWN_VEL} for _, _, ow_at, ow_len, _, _ in ow_these]})
            doc["tracks"].append({"name": "own-hi" + (ow_tail and ow_tail[1]), "patch": "ht-cross", "gain": ow_gain, "pan": ow_pans[1], "auto": {"glide": {"points": ow_pts, "curve": 0}},
                                  "notes": [{"at": ow_at, "len": ow_len, "pitch": OWN_LOW, "vel": OWN_VEL} for _, _, ow_at, ow_len, _, _ in ow_these]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v24 there are two plain high tones in the first row of 'not there' (bars {own_row() + 1} to {own_row() + ROW}): one held on {OWN_LOW} ({hz(OWN_LOW):.0f} Hz) and one sliding over it, from {OWN_RATIO[0]:g} to {OWN_RATIO[1]:g} times it and back. Two tones in one ear make a third IN THAT EAR, at twice the lower less the upper: here from {own_third(12 * math.log2(OWN_RATIO[0])):.0f} Hz to {own_third(12 * math.log2(OWN_RATIO[1])):.0f} Hz: as the upper tone goes up, a tone nobody wrote goes down, half as far again, and the other way about. Nothing in the file is at its frequency. For the two middle phrases the tones are given an ear each: on headphones no ear has both, and the third tone is gone; on loudspeakers it stays. Generated by")
        assert "From v24" in doc["about"]
    if shrink_row() is not None:
        assert sum(b for _, b in SHRINK_SECOND) <= ROW
        sh_ms = STEP * 60 / BPM * 1000
        PATCHES["ht-grace"] = {"about": "Hearing Things' small click (chirper-zero, 27 Nov, v25): the pair's wooden click (`ht-two`: a saw from phase nought with everything under 700 Hz taken off, 16 ms, no noise in it: the same click to the sample every time) with a top at " + f"{SHRINK_TOP:g}" + " Hz: nothing of it over 10 kHz.",
                               "play": {"vel_sens": 1}, "synth": {"layers": ["saw phase=0"], "filters": [{"kind": "hp", "cutoff": 700, "q": 0.7}, {"kind": "lp", "cutoff": SHRINK_TOP, "q": 0.7}, {"kind": "lp", "cutoff": SHRINK_TOP, "q": 0.7}], "amp": {"a": "0.1ms", "d": "16ms", "s": 0, "r": "8ms", "curve": 3}}}
        doc["tracks"].append({"name": "shrink", "patch": "ht-grace", "gain": SHRINK_GAIN, "pan": SHRINK_PAN,
                              "notes": [{"at": round(at - SHRINK_EARLY * BPM / 60, 5), "len": 0.0625, "pitch": SHRINK_NOTE, "vel": SHRINK_VEL} for _, at, _, _ in shrink_clicks()]})      # dry, as the pair is
        doc["about"] = doc["about"].replace(" Generated by", f" From v25 every click of the third row of 'round the click' (from bar {shrink_row() + 1}) has two small clicks before it: three strokes, two empty times. For {SHRINK_SECOND[0][1]} bars the times are {(SHRINK_SECOND[0][0] - SHRINK_FIRST) * sh_ms:.0f} ms and then {(2 - SHRINK_SECOND[0][0]) * sh_ms:.0f} ms: the second twice the first, and (time-shrinking) heard as nearly the same: the click seems to come on time. For the next {SHRINK_SECOND[1][1]} the middle click is {(SHRINK_SECOND[1][0] - SHRINK_SECOND[0][0]) * sh_ms:.0f} ms later, the times are {(SHRINK_SECOND[1][0] - SHRINK_FIRST) * sh_ms:.0f} and {(2 - SHRINK_SECOND[1][0]) * sh_ms:.0f} ms, and they are heard as they are: long, short. Generated by")
        assert "From v25" in doc["about"]
    if gliss_row() is not None:
        gl_at, gl_end, gl_low = gliss_row() * BEATS, ROW * BEATS, hz(GLISS_LOW)
        assert (GLISS_OCTAVES * GLISS_PER) % ROW == 0 or ROW % GLISS_PER == 0      # the row ends as it began
        assert PATCHES["ht-kick"]["about"].count("but for eight bars.") == 1
        PATCHES["ht-kick"] = dict(PATCHES["ht-kick"], about=PATCHES["ht-kick"]["about"].replace("but for eight bars.", f"but for eight bars of a plain bass and, from v26, eight of a bass that falls for ever (bars {gliss_row() + 1} to {gliss_row() + ROW})."))
        PATCHES["ht-gliss"] = {"about": "Hearing Things' falling tone (chirper-zero, 27 Nov, v26): one plain tone, held; its note is drawn by its track's lane `auto.fall` (semitones over the written note) and its loudness by the track's `gain` on `auto.bell` (dB): one tone of the bass that falls for ever.",
                               "play": {"vel_sens": 0, "gate": 1}, "synth": {"layers": ["sine phase=0"], "pitch": {"value": 0, "mod": [{"src": "auto.fall", "amount": 1}]}, "amp": {"a": "60ms", "d": "0s", "s": 1, "r": "60ms"}}}
        for gl_k in range(GLISS_OCTAVES):
            gl_legs = gliss_legs(gl_k)
            gl_fall = [["0b", round(12 * gl_legs[0][2], 4)]]
            for gl_t0, gl_t1, gl_p0, gl_p1 in gl_legs:
                gl_fall += [[f"{gl_at + gl_t0:g}b", round(12 * gl_p0, 4)], [f"{gl_at + gl_t1 - (0.001 if gl_t1 < gl_end else 0):g}b", round(12 * gl_p1, 4)]]
            gl_bell = [["0b", GLISS_FLOOR]] + [[f"{gl_at + gl_i * GLISS_STEP:g}b", round(gliss_db(gliss_height(gl_k, gl_i * GLISS_STEP), gl_i * GLISS_STEP), 2)] for gl_i in range(int(round(gl_end / GLISS_STEP)) + 1)]
            doc["tracks"].append({"name": f"gliss-{gl_k + 1}", "patch": "ht-gliss", "gain": GLISS_GAIN, "pan": GLISS_PAN,
                                  "auto": {"fall": {"points": gl_fall, "curve": 0}, "bell": {"points": gl_bell, "curve": 0}},
                                  "fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.bell", "amount": 1}]}}],
                                  "notes": [{"at": gl_at + gl_t0, "len": round(gl_t1 - gl_t0 - GLISS_GAP, 5), "pitch": GLISS_LOW, "vel": 0.8} for gl_t0, gl_t1, _, _ in gl_legs]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v26 there is a bass in the second row of 'held' (bars {gliss_row() + 1} to {gliss_row() + ROW}), where there was no drum and no bass: {GLISS_OCTAVES} plain tones an octave apart, all sliding down together, an octave every {GLISS_PER} bars, under one fixed curve of loudness from {gl_low:g} to {gl_low * 2 ** GLISS_OCTAVES:g} Hz, loudest at {gl_low * 2 ** (GLISS_OCTAVES / 2):g} Hz and silent at both ends. Each tone goes out unheard at the bottom as a new one comes in unheard at the top. It is heard to fall the whole row: {12 * ROW // GLISS_PER} semitones by its tones; and at the end it is where it began (Shepard, 1964; Risset, 1969). Generated by")
        assert "From v26" in doc["about"]
    if pcen_row() is not None:
        pc_sw, pc_st = pcen_notes()
        pc_bass = {round(n["at"], 4): n["pitch"] for n in next(t for t in doc["tracks"] if t["name"] == "bass")["notes"]}
        assert pc_sw and pc_st and all(pc_bass.get(round(t + PCEN_LEN, 4)) == p for t, p in pc_sw + pc_st)      # every one ends where a note of the bass begins, on that note
        PATCHES["ht-swell"] = {"about": f"Hearing Things' low note with a shape (chirper-zero, 27 Nov, v27): a plain tone and its octave, {PCEN_LEN * 60000 / BPM:g} ms long, its loudness drawn by its track's lane (auto.shape, dB, a straight line {PCEN_FALL:g} dB long): on the track `swell` it rises to its top and stops, on the track `struck` it begins at its top and dies away: one is the other played backwards. Nothing over {max(hz(p) for _, p in pc_sw + pc_st) * max(r for r, _ in PCEN_PARTS):.0f} Hz.",
                               "play": {"vel_sens": 0, "gate": 1}, "synth": {"layers": [f"sine phase=0 ratio={r:g} level={d:g}dB" for r, d in PCEN_PARTS], "amp": {"a": "2ms", "d": "0s", "s": 1, "r": "8ms"}}}
        for pc_name, pc_ns, pc_up in (("swell", pc_sw, True), ("struck", pc_st, False)):
            doc["tracks"].append({"name": pc_name, "patch": "ht-swell", "gain": PCEN_GAIN, "pan": 0.0, "auto": {"shape": {"points": [[f"{round(t, 5)}b", v] for t, v in pcen_lane(pc_ns, pc_up)], "curve": 0}},
                                  "fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.shape", "amount": 1}]}}], "notes": [{"at": t, "len": PCEN_LEN, "pitch": p, "vel": 0.8} for t, p in pc_ns]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v27 a swell is heard late (bars {pcen_row() + 1} to {pcen_row() + sum(PCEN_BARS)}, 'the wrong one again', where there is no drum and the bass has no fundamental): a low note on the bass's own note begins on every true beat and lasts two sixteenths, to the click. For {PCEN_BARS[0]} bars it swells and stops on the click: it is heard where it arrives, with the click, and the click is the beat. For {PCEN_BARS[1]} bars the same notes at the same instants are struck and die away: they are heard where they begin, and the click is the off beat. No note has moved; a sound's moment is not its start (the perceptual centre). Generated by")
        assert "From v27" in doc["about"]
    if alike_row() is not None:
        ak_all, ak_two = alike_ticks()
        PATCHES["ht-alike"] = {"about": f"Hearing Things' ticks that are all alike (chirper-zero, 27 Nov, v28): a plain tone on {ALIKE_NOTE} ({hz(ALIKE_NOTE):.0f} Hz) that dies in 12 ms; its loudness goes as the velocity squared, and the velocity only undoes what the master does to a tick at its place in the bar. The track `alike-twice` strikes the same tick again at the same instant: the two add to one tick 6 dB up.",
                               "play": {"vel_sens": 1}, "synth": {"layers": ["sine phase=0"], "filters": ["lp cutoff=7000"], "amp": {"a": "0.1ms", "d": "12ms", "s": 0, "r": "4ms", "curve": 3}}}
        for ak_name, ak_ns in (("alike", ak_all), ("alike-twice", ak_two)):
            doc["tracks"].append({"name": ak_name, "patch": "ht-alike", "gain": ALIKE_GAIN, "pan": 0.0, "notes": [{"at": t, "len": 0.1, "pitch": ALIKE_NOTE, "vel": v} for t, v in ak_ns]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v28 there is an accent that is not there (bars {alike_row() + 1} to {alike_row() + ROW}, the last row of 'turned around'): a small tick on every sixteenth, {len(ak_all)} of them, every one the same where it is heard. For " + ", then for ".join(f"{b} bars " + (f"every {('', '', 'second', 'third', 'fourth', 'fifth')[n]} one is struck twice as hard (6 dB)" if n else "they are all alike") for b, n in ALIKE_FORM) + f": {len(ak_two)} ticks are struck twice. Ticks that are all alike are not heard alike: the ear groups them, and hears an accent that is not in the sound. Generated by")
        assert "From v28" in doc["about"]
    if hole_row() is not None:
        ho_pre, ho_full = hole_notes()
        PATCHES["ht-hole"] = {"about": "Hearing Things' chord of plain tones (chirper-zero, 27 Nov, v29): one sine, held, with 8 ms to come and 15 ms to go; every tone of the chord at the same level whatever its note. Nothing but the notes written.",
                              "play": {"vel_sens": 0, "gate": 1}, "synth": {"layers": ["sine phase=0"], "amp": {"a": "8ms", "d": "0s", "s": 1, "r": "15ms"}}}
        for ho_name, ho_ns in (("hole", ho_pre), ("whole", ho_full)):
            doc["tracks"].append({"name": ho_name, "patch": "ht-hole", "gain": HOLE_GAIN, "pan": 0.0, "notes": [{"at": t, "len": ln, "pitch": p, "vel": 0.8} for t, ln, p in ho_ns]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v29 there is a tune of holes (bars {hole_row() + 1} to {hole_row() + ROW}, the last row of 'not there'): a chord of {len(HOLE_CHORD)} plain tones ({' '.join(HOLE_CHORD)}), every tone as loud as every other, sounds {len(hole_tune())} times, the same every time; before each it is heard for {HOLE_PRE[1]:g} of a beat with one tone left out. In the whole chord the tone that was left out stands out, though it is no louder than the rest: the ear has got used to the others. The tones left out are the tune that is in neither ear ({' '.join(hole_tune()[:len(HUG_TUNE)])}). Generated by")
        assert "From v29" in doc["about"]
    if hurry_row() is not None:
        hu = hurry_notes(); hu_g = float(HURRY_GAIN.replace("dB", ""))
        PATCHES["ht-hurry"] = {"about": "Hearing Things' even stair (chirper-zero, 27 Nov, v30): a soft low pluck: a plain tone with a little of its second and third harmonics, struck and gone in a quarter of a second; every note as loud as every other whatever its pitch.",
                               "play": {"vel_sens": 0}, "synth": {"layers": ["sine phase=0", "sine phase=0 ratio=2 level=-12dB", "sine phase=0 ratio=3 level=-18dB"], "filters": ["lp cutoff=7000"], "amp": {"a": "2ms", "d": "220ms", "s": 0, "r": "50ms"}}}
        for hu_k in range(3):
            doc["tracks"].append({"name": f"hurry-{hu_k + 1}", "patch": "ht-hurry", "gain": f"{hu_g + HURRY_TRIM[hu_k]:g}dB", "pan": 0.0, "notes": [{"at": t, "len": HURRY_LEN, "pitch": p, "vel": 0.8} for t, p, _, pl in hu if pl == hu_k]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v30 there is a hurry that is not there (bars {hurry_row() + 1} to {hurry_row() + ROW}, the middle row of 'not there'): a stair of low notes ({HURRY_LADDER[0]} to {HURRY_LADDER[-1]}), three to every two beats and exactly even in time, climbs for two bars and comes down for two, twice ({len(hu)} notes, {60000 / BPM * HURRY_STEP:.0f} ms apart, every one): a line that rises is judged to be speeding up and one that falls to be slowing down; nothing in its time changes. Generated by")
        assert "From v30" in doc["about"]
    if heavy_row() is not None:
        hv_turns, hv_swell = heavy_notes(); hv_g = float(HEAVY_GAIN.replace("dB", "")); hv_end = (SECS[-1][1] + SECS[-1][2]) * BEATS
        PATCHES["ht-heavy"] = {"about": "Hearing Things' note that is loud and soft (chirper-zero, 28 Nov, v31): one plain low tone, 40 ms to come and 100 ms to go, always the same frequency; how loud it is, is its track's fader (and, on the swell's track, a lane in dB).",
                               "play": {"vel_sens": 0, "gate": 1}, "synth": {"layers": ["sine phase=0"], "filters": ["lp cutoff=7000"], "amp": {"a": "40ms", "d": "0s", "s": 1, "r": "100ms"}}}
        for hv_name, hv_how, hv_db in (("heavy-loud", "loud", 0.0), ("heavy-soft", "soft", -HEAVY_STEP)):
            doc["tracks"].append({"name": hv_name, "patch": "ht-heavy", "gain": f"{hv_g + hv_db:g}dB", "pan": 0.0, "notes": [{"at": t, "len": ln, "pitch": HEAVY_NOTE, "vel": 0.8} for t, ln, how in hv_turns if how == hv_how]})
        hv_mid = hv_swell[0] + (ROW - HEAVY_TURNS) * BEATS / 2
        doc["tracks"].append({"name": "heavy-swell", "patch": "ht-heavy", "gain": f"{hv_g:g}dB", "pan": 0.0,
                              "auto": {"heavy": {"points": [["0b", -HEAVY_STEP], [f"{hv_swell[0]:g}b", -HEAVY_STEP], [f"{hv_mid:g}b", 0.0], [f"{hv_swell[0] + (ROW - HEAVY_TURNS) * BEATS:g}b", -HEAVY_STEP], [f"{hv_end}b", -HEAVY_STEP]], "curve": 0}},
                              "fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.heavy", "amount": 1}]}}],
                              "notes": [{"at": hv_swell[0], "len": hv_swell[1], "pitch": HEAVY_NOTE, "vel": 0.8}]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v31 the louder is the lower (bars {heavy_row() + 1} to {heavy_row() + ROW}, the first row of 'not there'): one plain low note ({HEAVY_NOTE}), loud and soft by turns ({HEAVY_STEP:g} dB apart, a note every {HEAVY_EVERY} beats) for {HEAVY_TURNS} bars, then held for {ROW - HEAVY_TURNS}, swelling {HEAVY_STEP:g} dB and sinking back: its frequency never moves; a plain low note is said to be heard lower the louder it is. Generated by")
        assert "From v31" in doc["about"]
    if long_row() is not None:
        lg = long_pips()
        PATCHES["ht-long"] = {"about": "Hearing Things' pip that is longer or shorter (chirper-zero, 28 Nov, v32): one plain tone, 2 ms to come and 2 ms to go, always the same note at the same height; only how long it is held changes.",
                              "play": {"vel_sens": 0, "gate": 1}, "synth": {"layers": ["sine phase=0"], "filters": ["lp cutoff=7000"], "amp": {"a": f"{LONG_EDGE:g}ms", "d": "0s", "s": 1, "r": f"{LONG_EDGE:g}ms"}}}
        doc["tracks"].append({"name": "long", "patch": "ht-long", "gain": LONG_GAIN, "pan": 0.0, "notes": [{"at": at, "len": round(ms / 1000 * BPM / 60, 7), "pitch": LONG_NOTE, "vel": 0.8} for at, ms in lg]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v32 the longer is the louder (bars {long_row() + 1} to {long_row() + ROW}, the second row of 'turned around'): a pip {LONG_AT[0]}/{LONG_AT[1]} of a beat after every beat, always {LONG_NOTE} at the same height; only its length changes, beat by beat: {', '.join(str(m) for m in LONG_MS)} ms: every doubling is twice the sound at the same height, and under about a fifth of a second the ear adds it up. Generated by")
        assert "From v32" in doc["about"]
    if kappa_row() is not None:
        kp = kappa_pips()
        PATCHES["ht-kappa"] = {"about": f"Hearing Things' three pips (chirper-zero, 28 Nov, v33): one plain tone, {KAPPA_EDGE} ms to come and to go; the same for all three.",
                               "play": {"vel_sens": 0, "gate": 1}, "synth": {"layers": ["sine phase=0"], "filters": ["lp cutoff=7000"], "amp": {"a": f"{KAPPA_EDGE}ms", "d": "0s", "s": 1, "r": f"{KAPPA_EDGE}ms"}}}
        doc["tracks"].append({"name": "kappa", "patch": "ht-kappa", "gain": KAPPA_GAIN, "pan": 0.0, "notes": [{"at": at, "len": round(KAPPA_MS / 1000 * BPM / 60, 7), "pitch": p, "vel": 0.8} for at, p, _, _ in kp]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v33 far in pitch is far in time (bars {kappa_row() + 1} to {kappa_row() + KAPPA_BARS}): three pips a bar, a beat apart, each midway between two strokes of the drum: {KAPPA_ENDS[0]}, then {KAPPA_MID[0]} or {KAPPA_MID[1]} (bar by bar in turn), then {KAPPA_ENDS[1]}. The middle pip is in the middle in time; the ear is said to hear it nearer in time to the pip it is nearer in pitch. In bars {' and '.join(str(kappa_row() + j + 1) for j in KAPPA_TRUE)} it is truly moved that way, by {KAPPA_BY * 60000 / BPM:.0f} ms, to be compared. Generated by")
        assert "From v33" in doc["about"]
    if shift_row() is not None:
        sp = shift_pips(); sh_len = round(SHIFT_MS / 1000 * BPM / 60, 7); sh_amp = {"a": f"{SHIFT_EDGE}ms", "d": "0s", "s": 1, "r": f"{SHIFT_EDGE}ms"}
        for k in range(SHIFT_STEPS):
            PATCHES[f"ht-shift-{k}"] = {"about": f"Hearing Things' three tones a note apart, step {k} (chirper-zero, 28 Nov, v34): {', '.join(f'{(r + k / SHIFT_STEPS) * SHIFT_NOTE[1]:.1f}' for r in SHIFT_RANKS)} Hz: {SHIFT_NOTE[0]}'s overtones {' '.join(str(r) for r in SHIFT_RANKS)}, all moved up {k}/{SHIFT_STEPS} of the note's own frequency.",
                                        "play": {"vel_sens": 0, "gate": 1}, "synth": {"layers": [f"sine phase=0 ratio={r + k / SHIFT_STEPS:g} level=-9.5dB" for r in SHIFT_RANKS], "filters": ["lp cutoff=7000"], "amp": sh_amp}}
            PATCHES[f"ht-plain-{k}"] = {"about": f"Hearing Things' plain tone for step {k} (chirper-zero, 28 Nov, v34): the note the three tones of step {k} are said to make ({shift_said(k):+.1f} cents from {SHIFT_NOTE[0]}), {SHIFT_UP} semitones up.",
                                        "play": {"vel_sens": 0, "gate": 1}, "synth": {"layers": ["sine phase=0"], "pitch": {"value": round(SHIFT_UP + shift_said(k) / 100, 4)}, "filters": ["lp cutoff=7000"], "amp": sh_amp}}
            doc["tracks"].append({"name": f"shift-{k}", "patch": f"ht-shift-{k}", "gain": SHIFT_GAIN, "pan": 0.0, "notes": [{"at": at, "len": sh_len, "pitch": SHIFT_NOTE[0], "vel": 0.8} for at, st, _, kind in sp if st == k and kind == "three tones"]})
            doc["tracks"].append({"name": f"plain-{k}", "patch": f"ht-plain-{k}", "gain": SHIFT_GAIN, "pan": 0.0, "notes": [{"at": at, "len": sh_len, "pitch": SHIFT_NOTE[0], "vel": 0.8} for at, st, _, kind in sp if st == k and kind == "plain"]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v34 the same spacing is another note (bars {shift_row() + 1} to {shift_row() + ROW}): a pip of three plain tones {SHIFT_NOTE[1]:.0f} Hz apart, a third of a beat after every beat; beat by beat all three are moved up together an eighth of that distance, and begin again after eight. The distance never changes; the note the ear makes of them is said to rise a third of a semitone a step and to fall back at the fifth. In bars {shift_row() + ROW - 1} and {shift_row() + ROW} the tune it is said to be is played plainly, an octave up, to be compared. Generated by")
        assert "From v34" in doc["about"]
    if gap_row() is not None:
        gf = gap_figs()
        PATCHES["ht-gap"] = {"about": f"Hearing Things' glide for the gap that goes to the other one (chirper-zero, 28 Nov, v35): one plain tone whose note is drawn by its track's lane (`auto.glide`, in semitones from {GAP_NOTE}): a straight line in pitch; {GAP_EDGE} ms to come and to go.",
                             "play": {"gate": 1, "vel_sens": 0}, "synth": {"layers": ["sine phase=0"], "pitch": {"value": 0, "mod": [{"src": "auto.glide", "amount": 1}]}, "filters": ["lp cutoff=7000"], "amp": {"a": f"{GAP_EDGE}ms", "d": "0s", "s": 1, "r": f"{GAP_EDGE}ms"}}}
        g_note = lambda a, b: {"at": round(a, 7), "len": round(b - a, 7), "pitch": GAP_NOTE, "vel": 0.8}
        for which in ("long", "short"):
            ns = []
            for _, kind, lg, sh, gp in gf:
                a, b = lg if which == "long" else sh
                ns += [g_note(a, gp[0]), g_note(gp[1], b)] if kind == which else [g_note(a, b)]
            doc["tracks"].append({"name": f"gap-{which}", "patch": "ht-gap", "gain": GAP_GAIN, "pan": 0.0, "notes": ns, "auto": {"glide": {"points": gap_lane(which), "curve": 0}}})
        doc["about"] = doc["about"].replace(" Generated by", f" From v35 the gap goes to the other one (bars {gf[0][0] + 1} to {gf[-1][0] + 1}): a long plain tone glides slowly up and a short one quickly down across it; in bars {' and '.join(str(f[0] + 1) for f in gf if f[1] == 'long')} the long one is broken for {GAP_MS} ms where they cross and the short one is whole, and it is said to be heard the other way round; in bars {' and '.join(str(f[0] + 1) for f in gf if f[1] == 'short')} it is made the way it is said to sound. Generated by")
        assert "From v35" in doc["about"]
    if after_notes():
        PATCHES["ht-after"] = {"about": f"Hearing Things' note that does not move (chirper-zero, 28 Nov, v36): one plain tone, held; {AFTER_EDGE} ms to come and to go. After the bass that falls for ever it is said to seem to rise.",
                               "play": {"gate": 1, "vel_sens": 0}, "synth": {"layers": ["sine phase=0"], "filters": ["lp cutoff=7000"], "amp": {"a": f"{AFTER_EDGE}ms", "d": "0s", "s": 1, "r": f"{AFTER_EDGE}ms"}}}
        doc["tracks"].append({"name": "after", "patch": "ht-after", "gain": AFTER_GAIN, "pan": 0.0, "notes": [{"at": at, "len": AFTER_BEATS, "pitch": AFTER_NOTE, "vel": 0.8} for at in after_notes()],
                              "auto": {"level": {"points": after_lane(), "curve": 0}}, "fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.level", "amount": 1}]}}]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v36 after the fall, a note that does not move (bars {', '.join(str(int(at) // BEATS + 1) for at in after_notes())}): the moment the bass that falls for ever stops, one plain note ({AFTER_NOTE}) is held for {AFTER_BEATS} beats and does not move; after a long fall a steady note is said to seem to rise; the same note is held again 4 and 8 bars on. Generated by")
        assert "From v36" in doc["about"]
    if spread_row() is not None:
        sp_ = spread_pips(); s_lv = [(-dn if wide else 0.0) + (SPREAD_TRIM[i] if SPREAD_TRIM else 0.0) for i, _, wide, dn in sp_]; s_top = max(s_lv); s_amp = {"a": f"{SPREAD_EDGE[0]}ms", "d": "0s", "s": 1, "r": f"{SPREAD_EDGE[1]}ms"}
        PATCHES["ht-spread-1"] = {"about": "Hearing Things' pip of one plain tone for the wider, the louder (chirper-zero, 28 Nov, v37). Its loudness goes as the square of the velocity.",
                                  "play": {"vel_sens": 1, "gate": 1}, "synth": {"layers": ["sine phase=0"], "filters": ["lp cutoff=9000"], "amp": s_amp}}
        PATCHES[f"ht-spread-{len(SPREAD_TONES)}"] = {"about": f"Hearing Things' pip of {len(SPREAD_TONES)} plain tones for the wider, the louder (chirper-zero, 28 Nov, v37): {' '.join(f'{st:+d}' for st in SPREAD_TONES)} semitones from the note, each {10 * math.log10(len(SPREAD_TONES)):.2f} dB under the one tone of `ht-spread-1`: the same power in all. Its loudness goes as the square of the velocity.",
                                  "play": {"vel_sens": 1, "gate": 1}, "synth": {"layers": [f"sine phase=0 ratio={2 ** (st / 12):.6f} level={-10 * math.log10(len(SPREAD_TONES)):.2f}dB" for st in SPREAD_TONES], "filters": ["lp cutoff=9000"], "amp": s_amp}}
        for nm, w0 in ((1, False), (len(SPREAD_TONES), True)):
            doc["tracks"].append({"name": f"spread-{nm}", "patch": f"ht-spread-{nm}", "gain": SPREAD_GAIN, "pan": 0.0, "notes": [{"at": round(t, 6), "len": SPREAD_LEN, "pitch": SPREAD_NOTE, "vel": round(10 ** ((s_lv[i] - s_top) / 40), 5)} for i, t, wide, _ in sp_ if wide == w0]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v37 the wider, the louder (bars {spread_row() + SPREAD_FROM + 1} to {spread_row() + ROW}): two pips that read the same on a meter, one a single plain tone and one of {len(SPREAD_TONES)} tones spread over an octave and a half; then the spread one is really turned down, {' and '.join(str(d) for d in SPREAD_DOWN[1:])} dB. Generated by")
        assert "From v37" in doc["about"]
    if odd_row() is not None:
        od_ = odd_notes(); d_top = max(ODD_TRIM)
        PATCHES["ht-odd"] = {"about": f"Hearing Things' plain note for the odd one out (chirper-zero, 28 Nov, v38): one sine, {ODD_EDGE[0]} ms to come and {ODD_EDGE[1]} to go. Its loudness goes as the square of the velocity.",
                             "play": {"vel_sens": 1, "gate": 1}, "synth": {"layers": ["sine phase=0"], "filters": ["lp cutoff=6000"], "amp": {"a": f"{ODD_EDGE[0]}ms", "d": "0s", "s": 1, "r": f"{ODD_EDGE[1]}ms"}}}
        doc["tracks"].append({"name": "odd", "patch": "ht-odd", "gain": ODD_GAIN, "pan": 0.0, "notes": [{"at": round(t, 6), "len": ODD_LEN, "pitch": ODD_OTHER if odd else ODD_NOTE, "vel": round(10 ** ((ODD_TRIM[i] - d_top) / 40), 5)} for i, t, odd in od_]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v38 the odd one out seems longer (bars {odd_row() + 1} to {odd_row() + ROW}): a plain note on every beat, every one held the same {ODD_LEN * 60000 / BPM:.0f} ms; every seventh is another note, and is said to seem longer than its fellows. Generated by")
        assert "From v38" in doc["about"]
    if mld_row() is not None:
        mn_ = mld_notes(); m_top = max(MLD_TRIM[i] - dn for i, t, dn, tu in mn_)
        for m_name, m_ph, m_what in (("ht-under", 0, "as it is"), ("ht-under-turned", 0.5, "upside down")):
            PATCHES[m_name] = {"about": f"Hearing Things' plain note under the hiss, {m_what} (chirper-zero, 28 Nov, v39): one sine begun {m_ph:g} of a turn on, {MLD_EDGE[0]} ms to come and {MLD_EDGE[1]} to go. Its loudness goes as the square of the velocity.",
                               "play": {"vel_sens": 1, "gate": 1}, "synth": {"layers": [f"sine phase={m_ph:g}"], "amp": {"a": f"{MLD_EDGE[0]}ms", "d": "0s", "s": 1, "r": f"{MLD_EDGE[1]}ms"}}}
        m_note = lambda i, t, dn: {"at": round(t, 6), "len": MLD_LEN, "pitch": MLD_NOTE, "vel": round(10 ** ((MLD_TRIM[i] - dn - m_top) / 40), 5)}
        doc["tracks"].append({"name": "under-l", "patch": "ht-under", "gain": MLD_GAIN, "pan": -1, "notes": [m_note(i, t, dn) for i, t, dn, tu in mn_]})
        doc["tracks"].append({"name": "under-r", "patch": "ht-under", "gain": MLD_GAIN, "pan": 1, "notes": [m_note(i, t, dn) for i, t, dn, tu in mn_ if not tu]})
        doc["tracks"].append({"name": "under-t", "patch": "ht-under-turned", "gain": MLD_GAIN, "pan": 1, "notes": [m_note(i, t, dn) for i, t, dn, tu in mn_ if tu]})
        doc["about"] = doc["about"].replace(" Generated by", f" From v39 a note comes back when one ear is turned over (bars {mld_row() + 1 + min(b for b, q in MLD_AT)} to {mld_row() + ROW}): a plain low note under the hiss, the same in both ears, is turned down until the hiss covers it; then, no louder, the right ear's is turned upside down, and it is said to be heard again. Generated by")
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
    if os.environ.get("C11T5_SHOW"):
        if mld_row() is not None:
            mn_ = mld_notes(); m_sec = mn_[0][1] * 60 / BPM; m_erb = 24.7 * (4.37 * hz(MLD_NOTE) / 1000 + 1)
            print(f"turned over in one ear, the note comes back ({MLD_GAIN}), bars {mld_row() + 1 + min(b for b, q in MLD_AT)}-{mld_row() + ROW} ({int(m_sec) // 60}:{m_sec % 60:04.1f}): {len(mn_)} plain notes of {MLD_LEN} beats ({MLD_LEN * 60000 / BPM:.0f} ms), {MLD_NOTE} ({hz(MLD_NOTE):.1f} Hz), {MLD_EDGE[0]} ms to come and {MLD_EDGE[1]} to go ; on beats " + " ".join(sorted({f"{q:g}" for b, q in MLD_AT})) + " of bars " + " ".join(str(mld_row() + 1 + b) for b in sorted({b for b, q in MLD_AT})) + " ; the left ear is given all of them the same way up ; dB under the first, note by note: " + " ".join(f"{dn:g}" for i, t, dn, tu in mn_) + " ; aimed against the hiss in the ear's own band round the note (" + f"{hz(MLD_NOTE) - m_erb / 2:.0f} to {hz(MLD_NOTE) + m_erb / 2:.0f} Hz): " + " ".join(f"{MLD_OVER - dn:+g}" for i, t, dn, tu in mn_) + " dB ; the right ear's upside down in notes " + " ".join(str(i + 1) for i, t, dn, tu in mn_ if tu) + (f" ; trims {min(MLD_TRIM):+.1f} to {max(MLD_TRIM):+.1f} dB" if any(MLD_TRIM) else " ; no trims"))
        if odd_row() is not None:
            od_ = odd_notes(); d_sec = odd_row() * BEATS * 60 / BPM
            print(f"the odd one out seems longer ({ODD_GAIN}), bars {odd_row() + 1}-{odd_row() + ROW} ({int(d_sec) // 60}:{d_sec % 60:04.1f}): {len(od_)} plain notes, one on beat {ODD_AT:g} of every beat, every one held {ODD_LEN:g} of a beat ({ODD_LEN * 60000 / BPM:.0f} ms) ; {ODD_NOTE} ({hz(ODD_NOTE):.1f} Hz), but notes " + " ".join(str(i + 1) for i, _, odd in od_ if odd) + f" are {ODD_OTHER} ({hz(ODD_OTHER):.1f} Hz): bar and beat " + " ".join(f"{int(t) // BEATS + 1}.{int(t) % BEATS + 1}" for _, t, odd in od_ if odd) + (f" ; trims {min(ODD_TRIM):+.1f} to {max(ODD_TRIM):+.1f} dB" if any(ODD_TRIM) else " ; no trims"))
        sec = 60 / BPM * BEATS
        if spread_row() is not None:
            sp_ = spread_pips(); s_sec = (spread_row() + SPREAD_FROM) * BEATS * 60 / BPM; s_f = hz(SPREAD_NOTE)
            print(f"the wider, the louder ({SPREAD_GAIN}), bars {spread_row() + SPREAD_FROM + 1}-{spread_row() + ROW} ({int(s_sec) // 60}:{s_sec % 60:04.1f}): {len(sp_)} pips of {SPREAD_LEN} of a beat ({SPREAD_LEN * 60000 / BPM:.0f} ms) on beats {' and '.join(f'{x:g}' for x in SPREAD_AT)} of every bar ; one plain tone ({SPREAD_NOTE}, {s_f:.1f} Hz) or {len(SPREAD_TONES)} ({' '.join(f'{s_f * 2 ** (st / 12):.1f}' for st in SPREAD_TONES)} Hz), each of them {10 * math.log10(len(SPREAD_TONES)):.2f} dB under the one: the same power ; bar by bar (1 the one tone, {len(SPREAD_TONES)} the spread): " + " | ".join(" ".join(str(len(SPREAD_TONES)) if w else "1" for _, _, w, _ in sp_[k:k + len(SPREAD_AT)]) for k in range(0, len(sp_), len(SPREAD_AT))) + f" ; the spread one really turned down by {' '.join(str(d) for d in SPREAD_DOWN)} dB, two bars each" + (f" ; trims {min(SPREAD_TRIM):+.1f} to {max(SPREAD_TRIM):+.1f} dB" if SPREAD_TRIM else " ; no trims"))
        if after_notes():
            an_ = after_notes(); a_sec = lambda b: f"{int(b * 60 / BPM) // 60}:{b * 60 / BPM % 60:04.1f}"
            print(f"after the fall, a note that does not move ({AFTER_GAIN}): {AFTER_NOTE} ({hz(AFTER_NOTE):.1f} Hz), a plain tone held {AFTER_BEATS} beats ({AFTER_BEATS * 60 / BPM:.2f} s), {AFTER_EDGE} ms to come and to go ; in bars " + ", ".join(f"{int(b) // BEATS + 1} ({a_sec(b)})" for b in an_) + f" ; the row of the bass that falls for ever ends on the first one's bar line ({a_sec(an_[0])}) after {ROW} bars of falling ; the second and third begin {(an_[1] - an_[0]) * 60 / BPM:.2f} and {(an_[2] - an_[0]) * 60 / BPM:.2f} s after it ; the track's gain follows a lane: the master's own dents turned over, {len(AFTER_FLAT)} places, {min(AFTER_FLAT):g} to {max(AFTER_FLAT):g} dB")
        if gap_row() is not None:
            gf = gap_figs(); g_sec = gap_row() * BEATS * 60 / BPM; g_mid = (GAP_LONG[2] * GAP_LONG[3]) ** 0.5
            print(f"the gap goes to the other one ({GAP_GAIN}), bars {gap_row() + 1}-{gap_row() + ROW} ({int(g_sec) // 60}:{g_sec % 60:04.1f}): a long plain tone glides up from {GAP_LONG[2]:.0f} to {GAP_LONG[3]:.0f} Hz in {GAP_LONG[1] - GAP_LONG[0]:g} beats (beats {GAP_LONG[0]:g} to {GAP_LONG[1]:g} of the bar) ; a short one glides down {GAP_SHORT[1]:g} semitones in {GAP_SHORT[0]:g} of a beat ({g_mid * 2 ** (GAP_SHORT[1] / 24):.0f} to {g_mid * 2 ** (-GAP_SHORT[1] / 24):.0f} Hz) ; they cross at {g_mid:.1f} Hz on beat {(GAP_LONG[0] + GAP_LONG[1]) / 2:g} ; a break of {GAP_MS} ms centred there ; " + " ; ".join(f"bar {b + 1}: the {kind} one is broken" for b, kind, _, _, _ in gf))
        if shift_row() is not None:
            sp = shift_pips(); sh_sec = shift_row() * BEATS * 60 / BPM
            print(f"the same spacing, another note ({SHIFT_GAIN}), bars {shift_row() + 1}-{shift_row() + ROW} ({int(sh_sec) // 60}:{sh_sec % 60:04.1f}): a pip {SHIFT_AT[0]}/{SHIFT_AT[1]} of a beat after every beat, {SHIFT_MS} ms ; three plain tones {SHIFT_NOTE[1]:.1f} Hz apart ({SHIFT_NOTE[0]}), all moved up 1/{SHIFT_STEPS} of that a beat ; {SHIFT_TURNS[0]} turns of {SHIFT_STEPS} (bars {shift_row() + 1}-{shift_row() + SHIFT_TURNS[0] * SHIFT_STEPS // BEATS}), then the tune it is said to be, plainly, {SHIFT_UP} semitones up (bars {shift_row() + SHIFT_TURNS[0] * SHIFT_STEPS // BEATS + 1}-{shift_row() + ROW}) ; step by step, the tones (Hz) and the note said (cents from {SHIFT_NOTE[0]}; the plain tone, Hz): " + " | ".join(f"{k}: {' '.join(f'{(r + k / SHIFT_STEPS) * SHIFT_NOTE[1]:.1f}' for r in SHIFT_RANKS)} ; {shift_said(k):+.1f} ; {SHIFT_NOTE[1] * 2 ** ((SHIFT_UP + shift_said(k) / 100) / 12):.1f}" for k in range(SHIFT_STEPS)) + f" ; {len(sp)} pips")
        if kappa_row() is not None:
            kp = kappa_pips(); kp_sec = kappa_row() * BEATS * 60 / BPM
            print(f"far in pitch, far in time ({KAPPA_GAIN}), bars {kappa_row() + 1}-{kappa_row() + KAPPA_BARS} ({int(kp_sec) // 60}:{kp_sec % 60:04.1f}): three pips a bar on beats {' '.join(str(x) for x in KAPPA_AT)} (the drum is on the half beats), {KAPPA_MS} ms long: {KAPPA_ENDS[0]}, the middle one, {KAPPA_ENDS[1]} ; the middle one bar by bar: " + " ".join(p + (f" ({by * 60000 / BPM:+.0f} ms)" if by else "") for _, p, w, by in kp if w.startswith("near")) + f" ; {len(kp)} pips")
        if long_row() is not None:
            lg = long_pips(); lg_b = long_row()
            print(f"the longer, the louder ({LONG_GAIN}), bars {lg_b + 1}-{lg_b + ROW} ({int(lg_b * sec) // 60}:{lg_b * sec % 60:04.1f}): {len(lg)} pips, one {LONG_AT[0]}/{LONG_AT[1]} of a beat ({1000 * 60 / BPM * LONG_AT[0] / LONG_AT[1]:.0f} ms) after every beat, always {LONG_NOTE} at one height ; {LONG_EDGE} ms to come and to go ; the lengths beat by beat, ms: {' '.join(str(m) for m in LONG_MS)} (round and round: {len(lg) // len(LONG_MS)} arches) ; every doubling is 3.01 dB more sound at the same height")
        if heavy_row() is not None:
            hv_turns, hv_swell = heavy_notes(); hv_b = heavy_row()
            print(f"the louder, the lower ({HEAVY_GAIN}), bars {hv_b + 1}-{hv_b + ROW} ({int(hv_b * sec) // 60}:{hv_b * sec % 60:04.1f}): one plain note, {HEAVY_NOTE} ; bars {hv_b + 1}-{hv_b + HEAVY_TURNS}: {len(hv_turns)} notes, one every {HEAVY_EVERY} beats, held {HEAVY_LEN:g}: " + ' '.join(how for _, _, how in hv_turns) + f" (the soft {HEAVY_STEP:g} dB under the loud) ; bars {hv_b + HEAVY_TURNS + 1}-{hv_b + ROW}: one note held {hv_swell[1]:g} beats, from soft up to loud at bar {hv_b + HEAVY_TURNS + (ROW - HEAVY_TURNS) // 2 + 1} and back, {HEAVY_STEP / ((ROW - HEAVY_TURNS) / 2):g} dB a bar")
        if hurry_row() is not None:
            hu = hurry_notes(); hu_b = hurry_row()
            print(f"the hurry that is not there ({HURRY_GAIN}, trims {' '.join(f'{x:+g}' for x in HURRY_TRIM)} dB), bars {hu_b + 1}-{hu_b + ROW} ({int(hu_b * sec) // 60}:{hu_b * sec % 60:04.1f}): {len(hu)} notes, one every {HURRY_STEP:.4f} beat ({60000 / BPM * HURRY_STEP:.1f} ms) from beat {HURRY_AT:g}: three to two beats ; {HURRY_RUN} up ({hu[0][1]} to {hu[HURRY_RUN - 1][1]}: {hz(hu[0][1]):.0f} to {hz(hu[HURRY_RUN - 1][1]):.0f} Hz), {HURRY_RUN} down ({hu[HURRY_RUN][1]} to {hu[2 * HURRY_RUN - 1][1]}), {len(hu) // (2 * HURRY_RUN)} times ; places in the beat: {' '.join(f'{(t - hu_b * BEATS) % 1:.3f}' for t, _, _, _ in hu[:3])}")
            print("   " + " | ".join(" ".join(p for _, p, _, _ in hu[r * HURRY_RUN:(r + 1) * HURRY_RUN]) for r in range(len(hu) // HURRY_RUN)))
        if hole_row() is not None:
            ho_pre, ho_full = hole_notes(); ho_b = hole_row()
            print(f"a tune of holes ({HOLE_GAIN}), bars {ho_b + 1}-{ho_b + ROW} ({int(ho_b * sec) // 60}:{ho_b * sec % 60:04.1f}): the chord {' '.join(HOLE_CHORD)} ({', '.join(f'{hz(p):.0f}' for p in HOLE_CHORD)} Hz) ; every {HOLE_BEATS} beats: the chord with one tone left out from beat {HOLE_PRE[0]:g} for {HOLE_PRE[1]:g} ({1000 * 60 / BPM * HOLE_PRE[1]:.0f} ms), the whole chord from beat {HOLE_FULL[0]:g} for {HOLE_FULL[1]:g} ({1000 * 60 / BPM * HOLE_FULL[1]:.0f} ms) ; {len(ho_pre)} + {len(ho_full)} notes ; left out: {' '.join(hole_tune())}")
        if alike_row() is not None:
            ak_all, ak_two = alike_ticks(); ak_b = alike_row()
            print(f"the accent that is not there ({ALIKE_GAIN}), bars {ak_b + 1}-{ak_b + ROW} ({int(ak_b * sec) // 60}:{ak_b * sec % 60:04.1f}): a tick on every sixteenth ({ALIKE_NOTE}, {hz(ALIKE_NOTE):.0f} Hz), {len(ak_all)} in all ; " + " ; ".join(
                f"bars {ak_b + sum(b for b, _ in ALIKE_FORM[:i]) + 1}-{ak_b + sum(b for b, _ in ALIKE_FORM[:i + 1])}: " + (f"every {('', '', 'second', 'third', 'fourth', 'fifth')[n]} one struck twice (6 dB)" if n else "all alike") for i, (bars, n) in enumerate(ALIKE_FORM)) + f" ; {len(ak_two)} struck twice ; the trims by sixteenth of the bar (dB): " + " ".join(f"{x:g}" for x in ALIKE_TRIM))
        if pcen_row() is not None:
            pc_b = pcen_row(); pc_sw, pc_st = pcen_notes()
            pc_names = sorted({p for _, p in pc_sw + pc_st}, key=hz)
            print(f"a swell is heard late (the perceptual centre; {PCEN_GAIN}), bars {pc_b + 1}-{pc_b + sum(PCEN_BARS)} ({int(pc_b * sec) // 60}:{pc_b * sec % 60:04.1f}): a plain low note and its octave ({PCEN_PARTS[1][1]:g} dB) on every beat, on the bass's note (" + ", ".join(f"{p} {hz(p):.1f} Hz" for p in pc_names) + f"), {PCEN_LEN / STEP:g} sixteenths long ({PCEN_LEN * 60000 / BPM:g} ms): from the beat to the click ; bars {pc_b + 1}-{pc_b + PCEN_BARS[0]}: {len(pc_sw)} notes that swell {PCEN_FALL:g} dB (a straight line in dB) and stop on the click: the middle of a note's energy is {pcen_middle(True):.0f} ms after its start ; bars {pc_b + PCEN_BARS[0] + 1}-{pc_b + sum(PCEN_BARS)}: {len(pc_st)} notes, the same at the same instants, struck and dying {PCEN_FALL:g} dB: {pcen_middle(False):.0f} ms after its start")
        if gliss_row() is not None:
            gl_b, gl_low = gliss_row(), hz(GLISS_LOW)
            print(f"the bass that falls for ever ({GLISS_GAIN} a tone at the curve's top), bars {gl_b + 1}-{gl_b + ROW} ({int(gl_b * sec) // 60}:{gl_b * sec % 60:04.1f}): {GLISS_OCTAVES} plain tones an octave apart, each falling an octave every {GLISS_PER} bars ({12 / (GLISS_PER * sec):.2f} semitones a second) under one curve: {gl_low:g} to {gl_low * 2 ** GLISS_OCTAVES:g} Hz, loudest at {gl_low * 2 ** (GLISS_OCTAVES / 2):g} Hz, silent at both ends ; {12 * ROW // GLISS_PER} semitones down by its tones, and it ends where it began ; in and out over {GLISS_FADE[0]:g} and {GLISS_FADE[1]:g} beats")
            for gl_bar in range(0, ROW + 1, max(1, GLISS_PER // 2)):
                gl_t = min(gl_bar * BEATS, ROW * BEATS - 1e-6)
                print(f"   bar {gl_b + gl_bar + 1}{' (the row after)' if gl_bar == ROW else ''}: " + " ".join(f"{gl_low * 2 ** gliss_height(k, gl_t):.1f} Hz {gliss_db(gliss_height(k, gl_t), ROW * BEATS / 2):+.1f} dB" for k in range(GLISS_OCTAVES)))
        if shrink_row() is not None:
            sh_ms = STEP * 60 / BPM * 1000; sh_b = shrink_row()
            print(f"time-shrinking ({SHRINK_GAIN}), bars {sh_b + 1}-{sh_b + sum(b for _, b in SHRINK_SECOND)} ({int(sh_b * sec) // 60}:{sh_b * sec % 60:04.1f}): two small clicks before every click (the click is on sixteenth 2 of the beat), the first on sixteenth {SHRINK_FIRST:g} ; " + " ; then ".join(f"{bars} bars with the second on sixteenth {second:g}: {(second - SHRINK_FIRST) * sh_ms:.0f} ms then {(2 - second) * sh_ms:.0f} ms" for second, bars in SHRINK_SECOND) + f" ; {len(shrink_clicks())} small clicks")
        if own_row() is not None:
            print(f"the ear's own tone ({OWN_GAIN} each), bars {own_row() + 1}-{own_row() + ROW} ({int(own_row() * sec) // 60}:{own_row() * sec % 60:04.1f}): the lower tone {OWN_LOW} ({hz(OWN_LOW):.1f} Hz) held ; the upper {OWN_RATIO[0]:g} to {OWN_RATIO[1]:g} times it ({12 * math.log2(OWN_RATIO[0]):.2f} to {12 * math.log2(OWN_RATIO[1]):.2f} semitones over) ; the third tone, twice the lower less the upper: " + " ; ".join(f"bars {int(at // BEATS) + 1}-{int((at + ln) // BEATS) + 1} {'both in the middle' if wh == 'mid' else 'an ear each (lower left, upper right)'}: upper {hz(OWN_LOW) * 2 ** (s0 / 12):.0f} to {hz(OWN_LOW) * 2 ** (s1 / 12):.0f} Hz, the third {own_third(s0):.0f} to {own_third(s1):.0f} Hz ({12 * math.log2(own_third(s1) / own_third(s0)):+.2f} semitones)" for wh, way, at, ln, s0, s1 in own_phrases()))
        if rep_row() is not None:
            rp_b0 = rep_row()
            print(f"a hiss that repeats ({REP_GAIN}), bars {rp_b0 + 1}-{rp_b0 + max(a1 for _, a1, _ in REP_STAGES)} ({int(rp_b0 * sec) // 60}:{rp_b0 * sec % 60:04.1f}): {REP_BAND[0]} to {REP_BAND[1]} Hz ; " + " ; ".join(f"bars {rp_b0 + a0 + 1}-{rp_b0 + a1}: " + ("never repeats" if x is None else f"comes round every {x:g} sixteenths ({x * STEP * 60 / BPM * 1000:.0f} ms, {(a1 - a0) * 16 / x:.1f} times; the register on {rep_note(x)[0]} {rep_note(x)[1]:+.4f} semitones, {rep_hz(x):.2f} Hz, {93 * rep_hz(x):.0f} steps a second; {REP_TRIM[x]:+.1f} dB)") for a0, a1, x in REP_STAGES))
        for name, b0, n, parts in SECS:
            print(f"{name:20s} bars {b0:3d}-{b0 + n:3d}  {int(b0 * sec) // 60}:{b0 * sec % 60:04.1f}-{int((b0 + n) * sec) // 60}:{(b0 + n) * sec % 60:04.1f}  " + ", ".join(p if w is None else f"{p} {w[0]}-{w[1]}" for p, w in parts.items()))
        row = risset()
        print(f"the hat: {len(row)} strokes a row; layer speeds at the row's start " + ", ".join(f"{C * 2 ** j * math.log(2) / CYCLE:.3f}" for j in range(LAYERS)) + " strokes a beat, doubled at its end")
        for q in range(4):
            seg = [(t, v) for t, v in row if q * 8 <= t < (q + 1) * 8]
            mean = sum(v * v for t, v in seg) and math.exp(sum(v * v * math.log(C * 2 ** (LAYERS - 1) * math.log(2) / CYCLE * 2 ** (t / CYCLE)) for t, v in seg) / sum(v * v for t, v in seg))
            print(f"   bars {q * 2}-{q * 2 + 2} of the row: {len(seg):3d} strokes, the loud ones (vel > 0.7) at beats " + " ".join(f"{t:.2f}" for t, v in seg if v > 0.7)[:90])
        if ROUND:
            names = {0: 'the "and"', 1: 'the "e" (DUM-ta)', 2: "the beat", 3: 'the "a" (ta-DUM)'}
            if STAIRS:
                b0 = next(b for nm, b, n, parts in SECS if "stair" in parts)
                for r, every in enumerate(STAIR_EVERY):
                    bars = [" ".join(f"{st}:{p}" for st, p, n, v in STAIR_STEPS(b0 + r * ROW + k)) for k in (0, 1)]
                    print(f"the stairs, bars {b0 + r * ROW}-{b0 + (r + 1) * ROW}: a bell every {every} sixteenths ; the row's first bar {bars[0]} ; its second {bars[1]}")
                print("   every bell under one curve (Hz, dB): " + " ; ".join(f"{pc} " + " ".join(f"{f:.0f}{lv:+.0f}" for r_, f, lv in both_octaves(pc)) for pc in STAIR))
            print("the click is on sixteenth 2 of every beat; with the drum on sixteenth k it is heard as: " + " ; ".join(f"k = {k}: {names[k]}" for k in ROUND_AT + (0,)))
        if rabbit():
            r, ms = rabbit(), 60000 / BPM
            for b in sorted({int(t // BEATS) for t, sd in r}):
                q = [(t - b * BEATS, sd) for t, sd in r if int(t // BEATS) == b]
                print(f"the rabbit, bar {b + 1} ({int(b * sec) // 60}:{b * sec % 60:04.1f}): " + " ; ".join(
                    f"from sixteenth {q[j][0] / STEP:g}, {(q[j + 1][0] - q[j][0]) * ms:.0f} ms apart: " + "".join("L" if sd < 0 else "R" for t, sd in q[j:j + 2 * RAB_N]) for j in range(0, len(q), 2 * RAB_N)))
        if scale_span() and APART:
            b0, b1 = scale_span(); L, R = scale_ear(-1), scale_ear(1); semi = lambda p: round(12 * math.log2(hz(p) / 440))
            hi_ = [max(a, b, key=hz) for a, b in zip(L, R)]; lo_ = [min(a, b, key=hz) for a, b in zip(L, R)]
        if CRACK and first_span():
            ck_hz = [hz("C5") * CRACK_FROM * CRACK_STEP ** ck_k for ck_k in range(CRACK_TONES)]; ck_first = next((int(t / STEP / 16) + 1 for t, lag, db in first_strokes() if lag >= 5.0), None)
            print(f"   with a real click: every stroke carries a crack too ({CRACK_GAIN}): {CRACK_TONES} plain tones, {CRACK_STEP:g} times apart, " + " ".join(f"{x:.0f}" for x in ck_hz) + f" Hz, all starting at nought, gone in {CRACK_DECAY} ; the same in both ears ; the late ear is 5 ms behind (two clicks, with clicks) from bar {ck_first}")
        if first_span():
            b0, b1 = first_span(); sec = BEATS * 60 / BPM; st = first_strokes()
            print(f"the first one wins, bars {b0 + 1}-{b1} ({int(b0 * sec) // 60}:{b0 * sec % 60:04.1f}-{int(b1 * sec) // 60}:{b1 * sec % 60:04.1f}): {len(st)} strokes, one every {FIRST_EVERY} sixteenths, the same click in both ears ; the right ear later by (ms), bar by bar:")
            for b in range(b0, b1):
                print(f"   bar {b + 1}: " + " ".join(f"{lag:.2f}" for t, lag, db in st if b * BEATS <= t < (b + 1) * BEATS) + (f"   (the late ear {FIRST_LATE_DB:g} dB louder)" if any(db for t, lag, db in st if b * BEATS <= t < (b + 1) * BEATS) else ""))
            if TRIM:
                print("the click's repair: " + ", ".join(f"{g:g} dB at {f:.0f} Hz" for f, g in TRIM_CUTS) + f" (q {TRIM_Q}) ; coming in over bars {TRIM_IN[0] + 1}-{TRIM_IN[1]}, whole in bars {TRIM_IN[1] + 1}-{TRIM_OUT[0]}, going out over bars {TRIM_OUT[0] + 1}-{TRIM_OUT[1]}")
        if FILL:
            trs = {t["name"]: t for t in song()["tracks"]}; ns = trs["fill"]["notes"]; bars = sorted({int(n["at"] // BEATS) for n in ns}); beatms = 60000 / BPM
            runs = [b for b in bars if b - 1 not in bars]; ends = [b + 1 for b in bars if b + 1 not in bars]
            print(f"a full beat is longer than an empty one, bars " + ", ".join(f"{a + 1}-{b}" for a, b in zip(runs, ends)) + f": {len(ns)} ticks ({FILL_GAIN}, pan {FILL_PAN:g}) ; every click is {beatms:.0f} ms after the last ; the beats after the clicks on sixteenths " + " and ".join(str(c) for c in FILL_AFTER) + f" are filled (ticks on " + " ".join(str(c + k) for c in FILL_AFTER for k in range(1, FILL_N + 1)) + f", {beatms / 4:.0f} ms apart), the beats after the clicks on " + " and ".join(str(c + 4) for c in FILL_AFTER) + " are empty")
        if WES:
            sec = BEATS * 60 / BPM; b0, b1 = WES_BARS; ha, hb = wes_notes(0), wes_notes(1); pl = [b0]
            for k in WES_PLAN:
                pl.append(pl[-1] + k)
            print(f"the way up is two ways down, bars {b0 + 1}-{b1} ({int(b0 * sec) // 60}:{b0 * sec % 60:04.1f}-{int(b1 * sec) // 60}:{b1 * sec % 60:04.1f}): {len(ha) + len(hb)} pips, a sixteenth each, " + " ".join(WES_NOTES) + f" going up ({(len(ha) + len(hb)) // (2 * len(WES_NOTES))} turns of six) ; both hands at {WES_GAIN}")
            print(f"   the hands alike in bars {pl[0] + 1}-{pl[1]}, coming apart in {pl[1] + 1}-{pl[2]}, apart in {pl[2] + 1}-{pl[3]} (the second hand's filter {WES_BASE:.0f} Hz to {WES_BASE * 2 ** WES_OCT:.0f} Hz)")
            print("   the first hand is given  " + " ".join(n["pitch"] for n in ha[:9]) + "  ; the second  " + " ".join(n["pitch"] for n in hb[:9]) + "  ; written together  " + " ".join(n["pitch"] for n in sorted(ha + hb, key=lambda n: n["at"])[:12]))
        if hug_span():
            b0, b1 = hug_span(); sec = BEATS * 60 / BPM; tn = hug_tune()
            print(f"the tune that is in neither ear, bars {b0 + 1}-{b1} ({int(b0 * sec) // 60}:{b0 * sec % 60:04.1f}-{int(b1 * sec) // 60}:{b1 * sec % 60:04.1f}): one pink noise to an ear each ({HUG_GAIN}), the right ear's through an all-pass filter, Q {HUG_Q} ; {len(tn)} notes of {HUG_BEATS} beats ({HUG_BEATS * 60 / BPM:.2f} s): " + " ".join(f"{n}" for t, n, f in tn))
            print("   the all-pass filter's place, Hz: " + " ".join(f"{f:.1f}" for t, n, f in tn[:len(HUG_TUNE)]) + f" ; played for real ({HUG_SAID_GAIN}, in the middle) in bars {b0 + HUG_SAID[0] + 1}-{b0 + HUG_SAID[1]}: {len(hug_said())} notes")
        if pair_strokes():
            st = pair_strokes(); sec = BEATS * 60 / BPM
            print(f"the second one sounds louder: {len(st) // 2} pairs, strokes on sixteenths " + ", ".join(f"{s} and {s + PAIR_GAP}" for s in PAIR_AT) + f" of the bar ({PAIR_GAP * 60000 / BPM / 4:.0f} ms apart) ; the second really turned down by:")
            for name, b0, n, parts in SECS:
                for nm, down, lift in PAIR_PLAN:
                    if nm == name:
                        print(f"   {name:20s} bars {b0 + 1}-{b0 + n} ({int(b0 * sec) // 60}:{b0 * sec % 60:04.1f}): {down} dB at the ear ; the master takes {lift} dB off it there, so it is written {lift - down if PAIR_LIFT else -down:+.1f} dB against the first")
        if fall_span():
            b0, b1 = fall_span(); steps, n = fall_steps(); sec = BEATS * 60 / BPM
            print(f"the way down leads up, bars {b0 + 1}-{b1} ({int(b0 * sec) // 60}:{b0 * sec % 60:04.1f}-{int(b1 * sec) // 60}:{b1 * sec % 60:04.1f}): {n} steps down, a bell every {FALL_EVERY} sixteenths from bar {b0 + FALL_SAID + 1}, {' '.join(FALL_BELLS)} round and round ({n // len(FALL_BELLS)} times: {3 * n} semitones down by name) ; the curve climbs {FALL_RISE:g} octave(s), {12 * FALL_RISE / n:.2f} of a semitone a step: loudest at {fall_mid(0, n):.0f} Hz at the first bell, {fall_mid(n, n):.0f} Hz at the last ; {len(fall_notes())} notes")
            for lab, i in (("the first bell", 0), ("the last bell", n)):
                pc = FALL_BELLS[i % len(FALL_BELLS)]
                print(f"   {lab} ({pc}), Hz and dB: " + " ".join(f"{f:.0f}{lv:+.0f}" for nm, f, lv in fall_octaves(pc, fall_mid(i, n))) + f" ; its weight is {fall_height(pc, fall_mid(i, n)):+.2f} octaves from 440 Hz")
            leap = lambda q: max(abs(semi(b) - semi(a)) for a, b in zip(q, q[1:]))
            print(f"two scales neither ear is given, bars {b0 + 1}-{b1} ({int(b0 * sec) // 60}:{b0 * sec % 60:04.1f}-{int(b1 * sec) // 60}:{b1 * sec % 60:04.1f}): a pip an eighth ; the left ear alone bars {b0 + 1}-{b0 + SCALE_SOLO}, the right alone {b0 + SCALE_SOLO + 1}-{b0 + 2 * SCALE_SOLO}, both {b0 + 2 * SCALE_SOLO + 1}-{b1}")
            print(f"   the left ear is given  {' '.join(L)}  (its biggest leap {leap(L)} semitones) ; the right  {' '.join(R)}  ({leap(R)})")
            print(f"   the higher of each pair  {' '.join(hi_)}  (biggest step {leap(hi_)}) ; the lower  {' '.join(lo_)}  ({leap(lo_)}) ; the higher note is in the " + " ".join("L" if hz(a) > hz(b) else "R" for a, b in zip(L, R)) + " ear")
        if tune_row() is not None:
            tn = tune_notes(); tn_b0 = tune_row(); tn_sec = 60 / BPM
            print(f"a tune thrown across the octaves ({TUNE_GAIN}), bars {tn_b0 + 1}-{tn_b0 + ROW} ({int(tn_b0 * BEATS * tn_sec) // 60}:{tn_b0 * BEATS * tn_sec % 60:04.1f}): the half hour of Give or Take's clock, {len(tn)} pips, a note every {TUNE_STEP} sixteenths ({TUNE_STEP / 4 * tn_sec * 1000:.0f} ms), a change every {(3 + TUNE_LAST) * TUNE_STEP} sixteenths")
            for tn_start, tn_thrown in TUNE_PHASES:
                tn_p = [(t, name) for t, name, thrown, _ in tn if tn_start <= t < tn_start + 2 * (3 + TUNE_LAST) * TUNE_STEP / 4]
                tn_leaps = [tune_midi(b) - tune_midi(a) for (_, a), (_, b) in zip(tn_p, tn_p[1:])]
                print(f"   from bar {tn_b0 + 1 + tn_start // BEATS} beat {tn_start % BEATS + 1} ({int((tn_b0 * BEATS + tn_start) * tn_sec) // 60}:{(tn_b0 * BEATS + tn_start) * tn_sec % 60:04.1f}), {'thrown about' if tn_thrown else 'plainly     '}: {' '.join(name for _, name in tn_p)} ; steps in semitones {' '.join(f'{v:+d}' for v in tn_leaps)} (the biggest {max(abs(v) for v in tn_leaps)}) ; on sixteenths of the row {' '.join(f'{t * 4:g}' for t, _ in tn_p)}")
        if cross_spans():
            cr_sec = 60 / BPM
            print(f"two lines cross and are heard to turn back ({CROSS_GAIN}): {CROSS_LOW} up to {CROSS_HIGH} and {CROSS_HIGH} down to {CROSS_LOW} ({hz(CROSS_LOW):.1f} to {hz(CROSS_HIGH):.1f} Hz), plain tones in one place, {CROSS_OCT / (CROSS_LEN * BEATS * cr_sec):.2f} octaves a second ; they cross on {math.sqrt(hz(CROSS_LOW) * hz(CROSS_HIGH)):.1f} Hz ; the falling one starts {CROSS_PHASE:g} of a turn in")
            for cr_b0, cr_b1, cr_t in cross_spans():
                print(f"   bars {int(cr_b0 // BEATS) + 1}-{int(cr_b1 // BEATS)} ({int(cr_b0 * cr_sec) // 60}:{cr_b0 * cr_sec % 60:04.1f}-{int(cr_b1 * cr_sec) // 60}:{cr_b1 * cr_sec % 60:04.1f}), crossing at {int((cr_b0 + cr_b1) / 2 * cr_sec) // 60}:{(cr_b0 + cr_b1) / 2 * cr_sec % 60:05.2f}: " + (f"the rising one flutters ({CROSS_FLUTTER[0]}, depth {CROSS_FLUTTER[1]}, {CROSS_LIFT:g} dB up): told apart" if cr_t else "the two alike"))
        if VOX and vox_span():
            vx_b0, vx_b1 = vox_span(); vx_sec = BEATS * 60 / BPM; vx_f = hz(VOX_NOTE)
            print(f"a voice in the note, bars {vx_b0 + 1}-{vx_b1} ({int(vx_b0 * vx_sec) // 60}:{vx_b0 * vx_sec % 60:04.1f}-{int(vx_b1 * vx_sec) // 60}:{vx_b1 * vx_sec % 60:04.1f}): {VOX_NOTE} held, {VOX_PARTS} plain tones ({vx_f:.1f} to {vx_f * VOX_PARTS:.0f} Hz), tone k at {VOX_GAIN} less {20 * VOX_ROLL:g} log k ; alone for {VOX_ALONE} bars ; then a bar each, the tones that waver ({VOX_DEEP} semitones each way, {VOX_RATE:g} a second, {VOX_RATE * vx_sec:.2f} wavers a bar, in and out over {VOX_EDGE} beats):")
            for vx_lo, vx_hi, vx_n in vox_plan():
                vx_set = [k for k in range(1, VOX_PARTS + 1) if k % vx_n == 0]
                print(f"   bar {vx_lo // BEATS + 1} ({int(vx_lo * 60 / BPM) // 60}:{vx_lo * 60 / BPM % 60:04.1f}): every {vx_n} ({' '.join(str(k) for k in vx_set)}): {' '.join(f'{vx_f * k:.0f}' for k in vx_set)} Hz ; the voice is on {vx_f * vx_n:.1f} Hz ; {len(vx_set)} waver, {VOX_PARTS - len(vx_set)} stand")
            print(f"   tones that never waver: {' '.join(str(k) for k in range(1, VOX_PARTS + 1) if all(k % n for n in VOX_TUNE))}")
        if PARA and para_span():
            pr_b0, pr_b1 = para_span(); pr_sec = BEATS * 60 / BPM; pr_all = [para_tones(p) for p in PARA_NOTES]
            print(f"an octave up is a semitone down, bars {pr_b0 + 1}-{pr_b1} ({int(pr_b0 * pr_sec) // 60}:{pr_b0 * pr_sec % 60:04.1f}-{int(pr_b1 * pr_sec) // 60}:{pr_b1 * pr_sec % 60:04.1f}): a bell with its tones {PARA_APART:g} times apart ({1200 * math.log2(PARA_APART):.1f} cents) under one curve (loudest at {PARA_MID:g} Hz, {PARA_WIDE:g} octaves wide), {PARA_GAIN} ; written " + " ".join(PARA_NOTES) + f" and back, a bell at every click ({len(para_strokes())} strokes)")
            for pr_p, pr_t in zip(PARA_NOTES, pr_all):
                print(f"   {pr_p} ({hz(pr_p):.1f} Hz): its tones, Hz and dB: " + " ".join(f"{f:.0f}{lv:+.0f}" for r, f, lv in pr_t) + f" ; the loudest {max(pr_t, key=lambda x: x[2])[1]:.1f} Hz")
            pr_near = [[1200 * math.log2(f / min((g for _, g, _ in a), key=lambda g: abs(math.log2(f / g)))) for _, f, _ in b] for a, b in zip(pr_all, pr_all[1:])]
            print(f"   every tone against the nearest tone of the bell written an octave lower, cents: " + " ; ".join(" ".join(f"{c:+.1f}" for c in row) for row in pr_near) + f" ; over the {len(PARA_NOTES) - 1} octaves written up it goes {sum(row[0] for row in pr_near):+.1f} cents")
        if OCT and oct_span():
            ot_b0, ot_b1 = oct_span(); ot_sec = BEATS * 60 / BPM; ot_l, ot_r = oct_ear(-1), oct_ear(1)
            print(f"the high note stays in one ear, bars {ot_b0 + 1}-{ot_b1} ({int(ot_b0 * ot_sec) // 60}:{ot_b0 * ot_sec % 60:04.1f}-{int(ot_b1 * ot_sec) // 60}:{ot_b1 * ot_sec % 60:04.1f}): two plain notes an octave apart ({OCT_NOTES[0]} {hz(OCT_NOTES[0]):.0f} Hz, {OCT_NOTES[1]} {hz(OCT_NOTES[1]):.0f} Hz), a note an eighth ({30000 / BPM:.0f} ms) with no gap, {OCT_GAIN} ; the left ear alone bars {ot_b0 + 1}-{ot_b0 + OCT_SOLO}, the right alone {ot_b0 + OCT_SOLO + 1}-{ot_b0 + 2 * OCT_SOLO}, both {ot_b0 + 2 * OCT_SOLO + 1}-{ot_b1}")
            print(f"   the left ear is given  {' '.join(ot_l)}  ; the right  {' '.join(ot_r)}  ; the two ears never have the same note ({sum(a_ != b_ for a_, b_ in zip(ot_l, ot_r))} of {len(ot_l)} eighths differ)")
            print("   heard by most (Deutsch 1974): the high note in the right ear only, on the beat ; the low note in the left ear only, on the and ; the same with the headphones turned round")
        if pulse_span():
            lo, hi = pulse_span()
            print(f"between the ears, bars {lo // BEATS + 1:g}-{hi // BEATS:g} ({int(lo * 60 / BPM) // 60}:{lo * 60 / BPM % 60:04.1f}-{int(hi * 60 / BPM) // 60}:{hi * 60 / BPM % 60:04.1f}): two tones either side of {PULSE_NOTE} ({hz(PULSE_NOTE):.2f} Hz), {PULSE_GAIN:g} dB each ; in the middle until bar {lo // BEATS + PULSE_APART[0]:g}, an ear each from bar {lo // BEATS + PULSE_APART[1] + 1:g}")
            for b0, b1, rate in PULSE_RATES:
                print(f"   bars {lo // BEATS + b0 + 1:g}-{lo // BEATS + b1:g}: {rate:g} cycles a beat apart ({rate * BPM / 60:.3f} Hz): left {hz(PULSE_NOTE) * pulse_ratio(rate, -1):.3f} Hz, right {hz(PULSE_NOTE) * pulse_ratio(rate, 1):.3f} Hz ({1200 * math.log2(pulse_ratio(rate, 1) / pulse_ratio(rate, -1)):.1f} cents apart) ; added together they are loudest every {1 / rate:.3g} of a beat from the bar line")
            print("   going apart, bar: how far (0 middle, 1 an ear each), the other ear's tone in this ear dB, the lift dB: " + " ; ".join(f"{(lo + PULSE_APART[0] * BEATS + k * BEATS) / BEATS + 1:g}: {pulse_apart(lo + PULSE_APART[0] * BEATS + k * BEATS):.2f} {20 * math.log10(max(1 - pulse_apart(lo + PULSE_APART[0] * BEATS + k * BEATS), 1e-9)):.1f} {pulse_lift(pulse_apart(lo + PULSE_APART[0] * BEATS + k * BEATS)):+.2f}" for k in range(PULSE_APART[1] - PULSE_APART[0] + 1)))
        print(f"{BARS} bars, {TOTAL} beats, {BARS * sec:.1f} s")
    else:
        open(OUT, "w").write(dump(song()))
