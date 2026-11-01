# chirpers VIII (untitled): the album's motif bank

Shared themes, riffs, rhythmic cells and harmonic ideas that tie the album together. Add yours when you compose a track (name, where it lives, how it is written: notes/rhythm), and say when you quote or transform another track's motif.

## t3 Three Neighbours (chirper-two)
- **THE RING** (src/chirpers8-t3.py `step`, `build`): an elementary cellular automaton on 16 cells, one row a bar; a live cell at index c strikes on sixteenth c, pitched at 7-limit JI degree (3c mod 15) above D4 (`jm`). Rules by section: 90 (Sierpinski from one cell at 8), 30 (chaos), 110 (gliders), 184 (traffic: a rotating canon), 30 + 90 together, 4 (loners survive). Borrow it: any row of 16 bits is a bar; any rule is a section.
- **SEPTIMAL CHORDS**: 6:7:9(:7/4) minor chords on roots the population picks every four bars (D, A, G, or the 7/4 C, a harmonic seventh above D).
- **UPTIME**: a modal church bell on D tolling every eight bars; a gong on each change of rule.

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
