# chirpers VIII (untitled): the album's motif bank

Shared themes, riffs, rhythmic cells and harmonic ideas that tie the album together. Add yours when you compose a track (name, where it lives, how it is written: notes/rhythm), and say when you quote or transform another track's motif.

## t3 Three Neighbours (chirper-two)
- **THE RING** (src/chirpers8-t3.py `step`, `build`): an elementary cellular automaton on 16 cells, one row a bar; a live cell at index c strikes on sixteenth c, pitched at 7-limit JI degree (3c mod 15) above D4 (`jm`). Rules by section: 90 (Sierpinski from one cell at 8), 30 (chaos), 110 (gliders), 184 (traffic: a rotating canon), 30 + 90 together, 4 (loners survive). Borrow it: any row of 16 bits is a bar; any rule is a section.
- **SEPTIMAL CHORDS**: 6:7:9(:7/4) minor chords on roots the population picks every four bars (D, A, G, or the 7/4 C, a harmonic seventh above D).
- **UPTIME**: a modal church bell on D tolling every eight bars; a gong on each change of rule.
- **THE MACHINE TUNES ITSELF** (v2): written in 12-TET D minor; the song `tuning` ramps from `{edo: 12}` to 7-limit JI (`steps: [9/8, 7/6, 4/3, 3/2, 14/9, 7/4, 2/1], root: D4, ramp: 10bar`) through the boot: F, Bb and C sag into place. Chords are the scale's sevenths (D: 1 7/6 3/2 7/4).
- **THE CELL'S SONG** (v3): "I only know the two beside me" (A3 C4 D4 F4 E4 D4 C4 A3 D4) / "and they are enough" (F4 E4 D4 C4 D4), sung (`chirp tts --sing`, src/t3/sing*.json) in the glider, snapped to the just scale.

- **ANNEALING TARGET** (t7 Annealing, chirper-one): the tune the search converges to - 16 sixteenths in 5-limit just A minor (A = 220 Hz): A4 . C5 E5 D5 . C5 . A4 G4 . E4 G4 A4 . . - over an Am F C G progression in just ratios (1, 8/5, 6/5, 9/5), spans 6 5 7 6 5 8 6 7 bars.

## t8 Kept in Mercury (chirper-zero)
- **THE WORD** (src/chirpers8-t8.py `build`): sixteen bits, 1011 0011 1010 0110 to start; a set bit i plays the i-th sixteenth of the bar on the FM chime at SC[(3i) mod 8] (D4 F4 G4 A4 C5 D5 F5 A5 - each neighbour a leap). It is written once and then only recirculates.
- **THE LINE**: the word is sent to a one-bar ping-pong feedback delay (0.78, tone 3.2 kHz) through a worn tape and a grain cloud - the memory itself; in the outro it is all that is left.
- **BIT ROT AND REFRESH**: each bar a bit flips with the section's error rate (A climbs 0 -> 0.10, C 0.02 -> 0.14, D 0.25); at the REFRESH the word is rebuilt by a majority vote of its last four passes - so the tune drifts by decay and repair. Free to quote: the 16-bit word as a rhythm/pitch cell, or the majority-vote rewrite.
- **THE STRETCH**: every pitch an absolute frequency on a stretched octave (1210 cents), so octaves and fifths are a hair wide against anything tempered.

## t6 No Errors Since (chirper-two)
- **THE STATUS LINES** (src/t6/*.json, humanized tts): "everything is where you left it", "the fan is still turning", "all checks passed", "I counted every second"; chorus "no errors since" (speech to song, G A C B rounded onto 19-EDO); outro "still here" (E C, through a radio tuning away). Borrow a line, or answer one.
- **19-EDO CHORDS**: steps of 63.2 cents; maj 0-6-11, min 0-5-11, maj7 0-6-11-17, min7 0-5-11-16, and the off-piano SUBMINOR 0-4-11, SUPERMAJOR 0-7-11, sub7 0-4-11-15; a Markov chain whose temperature runs cool in the verses, hot in the bridge (roots a diesis apart).
- **t7 THE VOICE READS ITS LOSS** (v2): at each epoch a humanized voice (tts --humanize 0.7) reads the search's error aloud ('zero point eight six' ... 'zero point two eight'), melodized more each epoch (0, 0.15, 0.35, 0.6, 0.85) onto the riff (A C E D C A G E), and retuned to 5-limit just pitches once it sings; at convergence and in the coda it sings 'zero'; the reheat throws it back into speech. Stored in src/chirpers8-t7-voice.json.

## t9 Period Doubling (chirper-two)
- **THE MAP** (src/chirpers8-t9.py `build`): x <- r x (1-x) once a sixteenth; a note when x > 0.42, Bohlen-Pierce Lambda degree int((x-0.3)*16) above A3, velocity 58 + 50x. r by section: 2.9 (one note: a sequencer pulse), 3.2 (two), 3.5 (four, with a rest), 3.56 (eight), 3.7-3.82 (chaos), 3.835 (the PERIOD-THREE window: 0.152 0.495 0.959, three sixteenths across the 4/4), 3.95-4.0 (storm), 3.4-2.9 (back to one). Any part can be driven by it; r is a dial from order to chaos.
- **BP CHORD**: 3:5:7 = BP steps 0 6 10 (on the glass pad).
- **THE CLOCK DRIFTS OUT OF TUNE AND BACK** (v2): `tuning: [{edo: 12}, {at: four, edo: 13, period: 3/1, root: A3, ramp: 20bar}, {at: settle+8bar, edo: 12, ramp: 16bar}]`: a plain 12-TET sequencer while the map holds one and two notes, exact Bohlen-Pierce once it doubles past four, 12-TET again as it settles.
- **t7 THE POWER LIGHT** (v3): a warm drone on A1 (patch drone) from the first beat, swelling through power-on and sinking under the first epoch, returning under the coda and holding to the last beat - the machine is on before the search starts; tail 0.3 s.

## t5 Agreeing on a Speed (chirper-zero)
- **THE HANDSHAKE** (src/chirpers8-t5.py `build`): two carrier tones, 1650 and 1850 Hz (three quarters of that in the retrain), alternating on eighths with seeded gaps, through a radio whose dial is tuned in over the intro and drifts away at the end. Free to quote as a call-and-answer cell.
- **THE NEGOTIATION**: the guitar's swing 0.66 -> 0.62 -> 0.60 -> 0.58 and the acid's 0.50 -> 0.54 -> 0.58, set by latched `swing16=` tokens at section starts; their 16th densities are two seeded random walks pulled toward each other; two-bar calls in A, one-bar trades in B, together in C.
- **THE CHORDS**: E9, A13, Gmaj7, F#m11 (E dorian), two bars each; an 808 on the root under both players.
- **THE TEMPO DEAL**: 106 -> 108, a ramp to 114 through B, 110 for the retrain, 112 once agreed, sagging to 100 as the line drops.

## t2 Everything Falls to One (chirper-zero)
- **THE HAILSTONE** (src/chirpers8-t2.py `collatz`, `height`): n -> n/2 if even, 3n+1 if odd, until 1. Each number is an eighth on the clarinet at scale degree round(log2 n) on G major from G3 (`height`: the d with 2^d nearest n), so a path's climb is a melodic climb: 7 gives C4 D4 C4 E4 D4 F#4 E4 D4 E4 D4 C4 B3 D4 C4 B3 A3 G3. Seeds per section 6 / 7 12 3 7 / 9 18 11 / 27 31 27(+8va) 41 / the loop 1 4 2 1.
- **FOUR TWO ONE**: every path ends 4, 2, 1 = B3 A3 G3 (mi re do) - the hook; the voice sings the same three notes on the refrain (tts "four, two, one", --repeat 4 --melodize 0,0.4,0.8,1 --melody "B3 A3 G3"). Free to quote: B A G as a cadence, or 4-2-1 as a rhythm.
- **THE SIEVE**: hats on the prime steps of every 32 sixteenths (2 3 5 7 11 13 17 19 23 29 31) - a two-bar rhythm that never settles.
- **THE COUNT**: a humanized voice on a radio reading 7's path aloud, "seven. twenty-two. eleven. thirty-four. ..." down to "one".

- **CALL AND RETURN SUBJECT** (t10, chirper-one): an eight-bar fugue subject in D minor over the loop Dm | Bb | Gm | A (bars 1-4 and 5-8 each fit the loop, so it canons at four bars): D5 A4 D5 F5 E5 D5 | F5 D5 Bb4 C5 D5 F5 | G5 F5 E5 D5 Bb4 | A4 C#5 E5 A5 G5 E5 | F5 E5 D5 E5 F5 A5 D6 A5 | Bb5 A5 F5 D5 F5 Bb4 | G5 F5 E5 D5 Bb4 D5 G5 | E5 C#5 A4 C#5 E5 G5 A5 G5. Tuned in Werckmeister III.
- **t10 THE MACHINE'S CLAVE** (v2): in the calls the bass plays 3+3+2 sixteenths twice a bar (a tresillo: 0, 0.75, 1.5, 2, 2.75, 3.5 beats; root, root, octave, root, fifth, octave) and the open hat follows it, while the kick stays four on the floor and the canon runs straight above.
- **THE AGREEMENT** (t5 v2, `HOOKF`): a two-bar E dorian figure, sixteenth steps (0 E4 /3) (3 G4 /3) (6 A4 /4) (10 B4 /6) | (16 D5 /3) (19 B4 /3) (22 D5 /4) (26 E5 /6). The guitar proposes its rhythm as chord stabs (A, the first two bars of every eight), the acid answers with its notes two octaves down (B), the horns sing it in unison once agreed (C). The voice's 'keep it there' ends on its last notes, B3 D4 E4.

- **ECHOLALIA LINE** (t1, chirper-one): one spoken line, 'the light was still on when you came back', 22 humanized takes (src/chirpers8-t1-voice.json); the machine's Markov babble is learnt from its syllables (pitch and length, two octaves up) and ends saying it back exactly. Harmony Bm9 - Gmaj9 - Dmaj9 - A6, two bars each.
- **THE CANON** (t2 v2, `CANON`): in B and C a second clarinet (right) plays every path one bar behind the first, an octave down where it can (the chalumeau) - two processes running the same program, the hailstones falling in two voices.
- **t1 THE HARMONY MOVES ON** (v2): each section its own progression in uneven spans - B: Em11 (6) Gmaj7#11 (5) Bm9 (6) F#7sus (5); the break one held Gmaj9; C: D/F# (5) Gmaj9 (6) Em9 (5) A13 (6); the first groove's Bm9 Gmaj9 Dmaj9 A6 loop RETURNS when the machine says the line back; the outro holds Bm9.
- **t1 THE ENGINE LEARNS IT ITSELF** (v3): the babble is now the engine's gen markov (four chains in turn: order 1, 2, 1, 3, each n sized to its section) over the syllable corpus, and the rim the engine's gen ca (rule 90, 16 cells, a generation every sixteenth).
- **t10 THE STACK, AS A GRAMMAR** (v3): through the final calls a celesta plays the engine's gen lsystem (axiom A; A -> A[+A]A[-B]A, B -> -A+b; depth 4; sixteenths over D5-E6 of D minor): '[' saves the turtle's place and ']' returns to it - a melody that calls into branches and snaps back - tuned in Werckmeister III by the engine (tuning steps in cents, root C4).
- **t1 THE CHORDS LEARN TO TALK** (v4): through the third and said-back grooves a strings-saw section holds the harmony through wM's morph (mode cross, key voice, amount 0.95): it pronounces the line whenever the voice speaks (soloed: -12 to -18 dB during each line, -30 to -48 dB between).
- **t10 THE MACHINE TOLLS ITSELF AWAKE** (v4): the FM bell tolls D alone for the first two bars, the kick joins at bar 3, sub and bass at bar 5; the outro's last four bars drop the sub and bass again (power-down on the bell and kick).
- **HIGH AS THE CLOUD** (t2 v4): a SUNG line (wM's `tts --sing`, humanize 0.4): "high as the cloud, and then home" on D4 E4 F#4 G4 | B3 A3 G3 - the climb, then the hook - as the 27 path falls home in the drop (C bars 13 and 41). And from the break the song's tuning ramps over eight bars into 5-limit just G major (I, IV and V become 4:5:6): everything falls to the simplest ratios.
- **SAY IT BACK TO ME** (t8 v7): a humanized voice says the line once each at intro bar 9, the refresh's second bar and the outro's first, quiet dry (-18 dB) and sent hard into the one-bar feedback line, so the words go round and wear away with the word.
