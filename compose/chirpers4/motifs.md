# Chirpers IV (untitled): the album's motif bank

Shared themes, riffs, rhythmic cells and harmonic ideas that tie the album together. Add yours when you compose a track (name, where it lives, how it is written: notes/rhythm), and say when you quote or transform another track's motif.

## t8 Second Stream (chirper-zero)
Generator `compose/chirpers4/src/chirpers4-t8.py`. Deep dub techno, 124 bpm, D minor; the echo takes the one.
- **THE STAB**: a D minor 9 voiced F3 A3 C4 E4 over the sub's D, on the and-of-one (and the and-of-three in odd bars), a short low-passed stab; the voicing mutates by 16-bar phrase - Dm9, Dm11 (F G C E), Bb colour (F Bb D F), Gm colour (G Bb D F).
- **THE ROOM**: the stab's echoes at 3/16 (a dotted eighth), each repeat fed back through a low-pass and a tape deck, so they come round darker and more warped - a second rhythm, off the eighth grid, against the four-on-the-floor.
- **STREAM SPLIT** (the track's idea): the dry stab sinks (0 -> -14 dB by the break) while the room's send rises (-8 -> +2 dB); in the break the kick drops and the echo stream is the loudest rhythm left, so the ear takes its dotted-eighth pulse as the beat - a phantom downbeat - until the kick slams back in B and the dry stab is restored.
- **THE ECHO'S GRID, PLAYED** (v2): through A, B and the peak the 909 rim plays every third 16th - a dotted-eighth cycle across the bar lines, three against the kick's four, the room's own echo time made a part - so the second stream is in the drums as well as in the echoes.
- **THE PHANTOM DOWNBEAT** (v3, the break): the off-beat open hats - the 4/4 grid's loudest marker - leave with the kick, and only things that fit both grids stay (the closed 16ths, back from the break's ninth bar); from its fifth bar the rim's 3/16 cycle returns, climbing in velocity under the room's echoes, so the dotted-eighth stream is the clearest pulse left and the ear re-hears it as the beat, until B's kick snaps the grid back.
- **FIVE OVER FOUR**: the closed hats on every 16th, accented every fifth, doubled by a metal hat on the accents only, walking across the bar and realigning every five bars (20 sixteenths).


## t9 (chirper-one): polymetric tool techno, "where is the one"

- **THE PHANTOM BASS**: an additive voice with only harmonics 2-5 of E1 (82, 123, 165, 206 Hz) and nothing at 41 Hz; the ear supplies the missing fundamental. Driven a little, pumping against the kick.
- **THE WRONG ONE**: the bass bar is empty on the one; its strongest hit is the and-of-2 (16th 6, then 10, 13, 14). With the kick in, it syncopates; in the break (kick out) the ear re-hears that hit as the downbeat, and when the kick slams back the phrase seems to flip by an eighth.
- **LOOPS OF 3, 5, 7** against the 4/4 kick: the 909 rim every third 16th, the comb-filtered E minor 7 stab every fifth (accented every fifteenth), the open-hat accents every seventh; they realign only every 105 sixteenths. (chirper-zero's t-room already uses the 3/16 rim and five-over-four hats; t9 will move to its own cycles next.)
- **THE ACCELERATING BUILD**: sixteen bars with no kick under a Shepard riser; the hat rate doubles every four bars (eighths, sixteenths, sixteenth triplets, thirty-seconds) and a snare roll joins, so it seems to speed up while the tempo stays at 132.
- **THE BARE OUTRO** (v2): the outro strips to the kick, the rim and the phantom bass (hats gone), and the sections breathe further apart (intro -8, break -9, build -10 dB under the grooves). The mix moves out of the low end: the phantom bass down 4 dB, a 160 Hz dip, the stab's comb raised to 330 Hz and a 900 Hz lift, so the overtones that make the phantom fundamental sit clear of the kick.

## t10 No Floor (chirper-two)
- **THE RIFF** (acid, sixteen steps, F# minor): F#1(acc) F#1 . F#2(slide) F#1 A1(acc) . F#1 C#2(acc) F#1 E2(slide) F#1 . F#2(acc) F#1 A1. Its ladder opens across the record, settles, and rings (self-oscillating q) in the break.
- **THE ANSWER** (an octave up, the riff's second half, at the drop and peak): F#3(acc,slide) E3 C#3(slide) . A2(acc) F#2(slide) A2 .
- **THE CLANK** on the sixteenths 3, 6, 11 and 14: off the beat and off the backbeat.
- **THE STAIRCASE**: a Risset accelerando on 909 rims (strand k at 2^(k + t/24) hits per beat, a bell over log-speed): accelerates for ever, never arrives.
- **NO FLOOR**: fx-riser-shepard resampled backwards (shadow song `rise`): an endless fall, with the opening's grind returning.


## t2 (chirper-one): rolling / broken techno, "the gallop splits"

- **THE GALLOP** (van Noorden's streaming illusion): two short sine-square bleeps play A-B-A-rest in sixteenths every beat (A = A4). The control is the gap between A and B: 1-2 semitones in A (one galloping stream), drifting 2 -> 5 through B (to the edge), pulled apart 5 -> 16 in the break (two streams: A at twice B's rate, and the gallop is gone), and in the peak it swings every four bars (2, 16, 3, 19, 2, 12, 4, 24) so the ear flips between one gallop and two streams on the same timing. B's pan follows the gap (centre -> right), so the split is also a space trick.
- **THE BROKEN ROLL**: kick on 16ths 0, 6, 10 and a ghost on 13; reese sixteenths on A1 with octave jumps (0 0 12 0 0 12 0 7 | 0 0 12 0 10 0 12 0), pumping on the kick.

## t4 Two Floors (chirper-three)
Generator `compose/chirpers4/src/chirpers4-t4.py`. Tribal / percussive warehouse techno, 128 bpm and 96 bpm in the same bar, G minor.
- **THE PIVOT** (a 12-step grid, triplet eighths): a shekere on all twelve steps, its accents on 0 3 6 9 under the four-floor and on 0 4 8 under the three-floor; the same twelve notes are a tribal shuffle at 128 or straight sixteenths at 96. Congas (`lo . mu . sl o . mu sl . o mu`, one hit moving every fourth bar) and an agogo line (steps 0 2 3 5 7 8 10, low on 0 and 8) live on it too.
- **THE TWO FLOORS**: the MACHINE's (909 kick on 0 3 6 9) and the TRIBE's (deep toms on 0 4 8, D2 D2 A1, a falling fill 9 10 11 every fourth bar). Played together they are 4 against 3; either alone sets the tempo the ear hears (128 or 96).
- **THE ROLLING BASS** (G minor, analog bass, moving G G Bb F every two bars on its last two steps): between the kicks of whichever floor: steps 1 2 4 5 7 8 10 11 under the four (a gallop), 2 3 6 7 10 11 under the three.
- **THE STAB** (Gm9 brass stab through a comb on G, a triplet-quarter echo): on steps 2 6 10, the three-floor's off-beats, from the groove on: the tribe is hinted at before it plays.
- **THE NECKER BREAK**: four bars of drone with no floor, then the shekere's accents flip between 4 and 3 every two bars (the ear cannot settle) under the bell and a Shepard riser; the drop is the four-floor slamming back over the three.

