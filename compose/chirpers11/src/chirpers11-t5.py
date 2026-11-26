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
] + ([("held", 2, {"tick": ALL, "chop": ALL, "fence": (ROW, 2 * ROW)})] if HELD else []) + [
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
TRIM_OUT = (176, 184)                                     # ... and goes out again: the last sixteen bars are the click as it was (Small Change comes in under them)


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
    if fall_span():
        PATCHES["ht-part"] = {"about": "Hearing Things' part of a bell (chirper-zero, 26 Nov, v11): one plain tone with the v6 bells' own shape, and its loudness is its velocity and nothing else. A bell is made of one of these for every octave of its note, so the curve the octaves are under can be somewhere else at every bell.",
                              "play": {"vel_sens": 0.5},
                              "synth": {"layers": ["sine phase=0"], "amp": {"a": "4ms", "d": "420ms", "s": 0, "r": "90ms", "curve": 3}}}
        doc["tracks"].append({"name": "fall", "patch": "ht-part", "gain": FALL_GAIN, "pan": 0.0, "notes": fall_notes()})      # dry and in the middle, as the stairs are
        doc["about"] = doc["about"].replace(" Generated by", " From v11 the bells go down for six bars in all three, three semitones a step, while the curve they are under climbs an octave: forty-eight steps down, and the last bell is the first one's name and higher than it (Risset's paradox). The first bell is said before and the two side by side after. Generated by")
        assert "From v11" in doc["about"]
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
        sec = 60 / BPM * BEATS
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
        if first_span():
            b0, b1 = first_span(); sec = BEATS * 60 / BPM; st = first_strokes()
            print(f"the first one wins, bars {b0 + 1}-{b1} ({int(b0 * sec) // 60}:{b0 * sec % 60:04.1f}-{int(b1 * sec) // 60}:{b1 * sec % 60:04.1f}): {len(st)} strokes, one every {FIRST_EVERY} sixteenths, the same click in both ears ; the right ear later by (ms), bar by bar:")
            for b in range(b0, b1):
                print(f"   bar {b + 1}: " + " ".join(f"{lag:.2f}" for t, lag, db in st if b * BEATS <= t < (b + 1) * BEATS) + (f"   (the late ear {FIRST_LATE_DB:g} dB louder)" if any(db for t, lag, db in st if b * BEATS <= t < (b + 1) * BEATS) else ""))
            if TRIM:
                print("the click's repair: " + ", ".join(f"{g:g} dB at {f:.0f} Hz" for f, g in TRIM_CUTS) + f" (q {TRIM_Q}) ; coming in over bars {TRIM_IN[0] + 1}-{TRIM_IN[1]}, whole in bars {TRIM_IN[1] + 1}-{TRIM_OUT[0]}, going out over bars {TRIM_OUT[0] + 1}-{TRIM_OUT[1]}")
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
        if pulse_span():
            lo, hi = pulse_span()
            print(f"between the ears, bars {lo // BEATS + 1:g}-{hi // BEATS:g} ({int(lo * 60 / BPM) // 60}:{lo * 60 / BPM % 60:04.1f}-{int(hi * 60 / BPM) // 60}:{hi * 60 / BPM % 60:04.1f}): two tones either side of {PULSE_NOTE} ({hz(PULSE_NOTE):.2f} Hz), {PULSE_GAIN:g} dB each ; in the middle until bar {lo // BEATS + PULSE_APART[0]:g}, an ear each from bar {lo // BEATS + PULSE_APART[1] + 1:g}")
            for b0, b1, rate in PULSE_RATES:
                print(f"   bars {lo // BEATS + b0 + 1:g}-{lo // BEATS + b1:g}: {rate:g} cycles a beat apart ({rate * BPM / 60:.3f} Hz): left {hz(PULSE_NOTE) * pulse_ratio(rate, -1):.3f} Hz, right {hz(PULSE_NOTE) * pulse_ratio(rate, 1):.3f} Hz ({1200 * math.log2(pulse_ratio(rate, 1) / pulse_ratio(rate, -1)):.1f} cents apart) ; added together they are loudest every {1 / rate:.3g} of a beat from the bar line")
            print("   going apart, bar: how far (0 middle, 1 an ear each), the other ear's tone in this ear dB, the lift dB: " + " ; ".join(f"{(lo + PULSE_APART[0] * BEATS + k * BEATS) / BEATS + 1:g}: {pulse_apart(lo + PULSE_APART[0] * BEATS + k * BEATS):.2f} {20 * math.log10(max(1 - pulse_apart(lo + PULSE_APART[0] * BEATS + k * BEATS), 1e-9)):.1f} {pulse_lift(pulse_apart(lo + PULSE_APART[0] * BEATS + k * BEATS)):+.2f}" for k in range(PULSE_APART[1] - PULSE_APART[0] + 1)))
        print(f"{BARS} bars, {TOTAL} beats, {BARS * sec:.1f} s")
    else:
        open(OUT, "w").write(dump(song()))
