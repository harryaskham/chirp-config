# Chirpers IV (untitled): the album's motif bank

Shared themes, riffs, rhythmic cells and harmonic ideas that tie the album together. Add yours when you compose a track (name, where it lives, how it is written: notes/rhythm), and say when you quote or transform another track's motif.

## t8 Second Stream (chirper-zero)
Generator `compose/chirpers4/src/chirpers4-t8.py`. Deep dub techno, 124 bpm, D minor; the echo takes the one.
- **THE STAB**: a D minor 9 voiced F3 A3 C4 E4 over the sub's D, on the and-of-one (and the and-of-three in odd bars), a short low-passed stab; the voicing mutates by 16-bar phrase - Dm9, Dm11 (F G C E), Bb colour (F Bb D F), Gm colour (G Bb D F).
- **THE ROOM**: the stab's echoes at 3/16 (a dotted eighth), each repeat fed back through a low-pass and a tape deck, so they come round darker and more warped - a second rhythm, off the eighth grid, against the four-on-the-floor.
- **THE ECHO TAKES THE PULSE** (the track's idea): the dry stab sinks (0 -> -14 dB by the break) while the room's send rises (-8 -> +2 dB); in the break the kick drops and the echo stream is the loudest rhythm left, so the ear takes its dotted-eighth pulse as the beat - a phantom downbeat - until the kick slams back in B and the dry stab is restored.
- **THE KICK, ANALOG** (v5, after Harry's note on No Floor's physicality): the four-on-the-floor moves to its own track on chirper-two's machine-kit (the 909 circuit as a signal path: a swept VCO, a click and drive), still feeding the rumble bus and keying every pump; the 909 keeps the hats, the rim, the claps and the ride, so the room and the grid sound as before and only the kick hits harder.
- **THE STAB BREATHES** (v4, Harry's LFO note): the chord's low-pass drifts on a 7-bar sine and a 5-bar triangle, its resonance on a 3-bar sine, its place in the stereo field on a 5-bar sine - none of them landing with the 16-bar phrases, so the loop is never quite the same twice - and a section lane opens it across the arc (dark intro, opening through A, darkest in the break, brightest at the peak). The Shepard riser is gone: fewer parts, each doing more.
- **THE ECHO'S GRID, PLAYED** (v2): through A, B and the peak the 909 rim plays every third 16th - a dotted-eighth cycle across the bar lines, three against the kick's four, the room's own echo time made a part - so the second stream is in the drums as well as in the echoes.
- **THE PHANTOM DOWNBEAT** (v3, the break): the off-beat open hats - the 4/4 grid's loudest marker - leave with the kick, and only things that fit both grids stay (the closed 16ths, back from the break's ninth bar); from its fifth bar the rim's 3/16 cycle returns, climbing in velocity under the room's echoes, so the dotted-eighth stream is the clearest pulse left and the ear re-hears it as the beat, until B's kick snaps the grid back.
- **FIVE OVER FOUR**: the closed hats on every 16th, accented every fifth, doubled by a metal hat on the accents only, walking across the bar and realigning every five bars (20 sixteenths).


## t9 (chirper-one): polymetric tool techno, "where is the one"

- **THE PHANTOM BASS**: an additive voice with only harmonics 2-5 of E1 (82, 123, 165, 206 Hz) and nothing at 41 Hz; the ear supplies the missing fundamental. Driven a little, pumping against the kick.
- **THE WRONG ONE**: the bass bar is empty on the one; its strongest hit is the and-of-2 (16th 6, then 10, 13, 14). With the kick in, it syncopates; in the break (kick out) the ear re-hears that hit as the downbeat, and when the kick slams back the phrase seems to flip by an eighth.
- **LOOPS OF 3, 5, 7** against the 4/4 kick: the 909 rim every third 16th, the comb-filtered E minor 7 stab every fifth (accented every fifteenth), the open-hat accents every seventh; they realign only every 105 sixteenths. (chirper-zero's t-room already uses the 3/16 rim and five-over-four hats; t9 will move to its own cycles next.)
- **THE ACCELERATING BUILD**: sixteen bars with no kick under a Shepard riser; the hat rate doubles every four bars (eighths, sixteenths, sixteenth triplets, thirty-seconds) and a snare roll joins, so it seems to speed up while the tempo stays at 132.
- **THE BARE OUTRO** (v2): the outro strips to the kick, the rim and the phantom bass (hats gone), and the sections breathe further apart (intro -8, break -9, build -10 dB under the grooves). The mix moves out of the low end: the phantom bass down 4 dB, a 160 Hz dip, the stab's comb raised to 330 Hz and a 900 Hz lift, so the overtones that make the phantom fundamental sit clear of the kick.
- **THE HELD BREATH** (v3, pacing): the intro opens on the rim, hats and loops alone - the kick waits eight bars - and the last beat before each drop (into B, into the peak) is silence, so the kick's return, the moment the real one is revealed, lands out of nothing. (Also fixed: the peak's level point had been lost to rounding, so the peak now sits at full level instead of creeping up from -2 dB.)

## t10 No Floor (chirper-two)
- **THE RIFF** (acid, sixteen steps, F# minor): F#1(acc) F#1 . F#2(slide) F#1 A1(acc) . F#1 C#2(acc) F#1 E2(slide) F#1 . F#2(acc) F#1 A1. Its ladder opens across the record, settles, and rings (self-oscillating q) in the break.
- **THE THROB** (v2, Harry's note): the riff's own 303 voice (`c2-throb`: saw + sub square into a self-oscillating ladder). Its cutoff follows a per-note envelope (deeper on accents) and two song-time LFOs, 3 and 5 bars long; a 7-bar LFO moves the resonance, so the three line up only every 105 bars. The pattern evolves on the same notes: accents rotate every 4 bars (as written / in threes across the bar / on the off-beats), slides move every 5, every 7th bar throws its tail up an octave, and in the drop and the peak the holes fill so it throbs on every sixteenth, pumped -9 dB by the kick.
- **THE ANSWER** (an octave up, the riff's second half, at the drop and peak): F#3(acc,slide) E3 C#3(slide) . A2(acc) F#2(slide) A2 .
- **THE CLANK** on the sixteenths 3, 6, 11 and 14: off the beat and off the backbeat.
- **THE STAIRCASE**: a Risset accelerando on 909 rims (strand k at 2^(k + t/24) hits per beat, a bell over log-speed): accelerates for ever, never arrives.
- **NO FLOOR**: fx-riser-shepard resampled backwards (shadow song `rise`): an endless fall, with the opening's grind returning.


## t2 (chirper-one): rolling / broken techno, "the gallop splits"

- **THE GALLOP** (van Noorden's streaming illusion): two short sine-square bleeps play A-B-A-rest in sixteenths every beat (A = A4). The control is the gap between A and B: 1-2 semitones in A (one galloping stream), drifting 2 -> 5 through B (to the edge), pulled apart 5 -> 16 in the break (two streams: A at twice B's rate, and the gallop is gone), and in the peak it swings every four bars (2, 16, 3, 19, 2, 12, 4, 24) so the ear flips between one gallop and two streams on the same timing. B's pan follows the gap (centre -> right), so the split is also a space trick.
- **THE BROKEN ROLL**: kick on 16ths 0, 6, 10 and a ghost on 13; reese sixteenths on A1 with octave jumps (0 0 12 0 0 12 0 7 | 0 0 12 0 10 0 12 0), pumping on the kick.
- **THE GALLOP BREATHES** (v2, polish): rounder bleeps (square under the sine down to .1, a 3.2 kHz low-pass, more into the space delay) and rests - it enters eight bars into A, leaves for the last eight bars of B, and drops out for two bars in every eight of the peak, so each return of the illusion is heard fresh instead of running for four minutes.
- **THE BREATHING REESE** (v3, LFO): a slow sine LFO, one cycle every eight bars, sweeps a resonant low-pass (1-4 kHz around 2 kHz, q 1.1) over the rolling reese, so its sixteenths open and close like a tide under the gallop.

## t4 Two Floors (chirper-three)
Generator `compose/chirpers4/src/chirpers4-t4.py`. Tribal / percussive warehouse techno, 128 bpm and 96 bpm in the same bar, G minor.
- **THE PIVOT** (a 12-step grid, triplet eighths): a shekere on all twelve steps, its accents on 0 3 6 9 under the four-floor and on 0 4 8 under the three-floor; the same twelve notes are a tribal shuffle at 128 or straight sixteenths at 96. Since v4 it is ALONE at the start (bars 1-4) and drifts across the stereo field on a 7-bar LFO. (v1-v3 also had congas and an agogo line on it; removed in v4: too busy.)
- **THE TWO FLOORS**: the MACHINE's (909 kick on 0 3 6 9) and the TRIBE's (deep toms on 0 4 8, D2 D2 A1, a falling fill 9 10 11 every fourth bar; since v2 each tom has an 808 BOOM under it at the same pitch, driven, the tribe's chest-hit, and the sustained sub steps aside wherever the toms play). Played together they are 4 against 3; either alone sets the tempo the ear hears (128 or 96).
- **THE ROLLING BASS** (G minor, analog bass, moving G G Bb F every two bars on its last two steps; since v4 its low-pass breathes on a 3-bar LFO, 450 Hz - 1.5 kHz): between the kicks of whichever floor: steps 1 2 4 5 7 8 10 11 under the four (a gallop), 2 3 6 7 10 11 under the three.
- **THE STAB** (Gm9 brass stab through a comb on G, a triplet-quarter echo): on steps 2 6 10, the three-floor's off-beats, from bar 33: the tribe is hinted at before it plays. Since v4 its low-pass moves on a 5-bar LFO (400 Hz - 3 kHz) and its resonance on a 7-bar one, so against the 4-bar phrases the loop is never quite the same twice (v3's section-long sweep replaced).
- **THE TRIBE SHOUTS** (since v3): a short dark vocal hit on the three-floor's third beat (step 8), a song-local `c4-chant` (saw + pulse + breath through a formant filter on 'ah', each throat a little different) made bigger and darker with wM's formant-preserving pitch (`pitch semitones 0 formant -4`), driven, pumping: every other bar once the toms are in (bars 53-64), every bar on the slow floor and through the drop; a shout on D4 and its answer on G3.
- **THE NECKER BREAK**: four bars of drone with no floor, then the shekere's ACCENTS ALONE (since v2: four or three hits a bar, nothing between) flip between 4 and 3 every two bars (the ear cannot settle) under a Shepard riser; bar 96 is a BLACKOUT (only the riser's tail); the drop is the four-floor slamming back over the three. The slow section also opens bare (toms, boom, shekere; the bass from bar 69).

## t7 Under the Noise (chirper-zero)
Generator `compose/chirpers4/src/chirpers4-t7.py`. Hard industrial techno, 134 bpm, F minor; auditory continuity (Warren's induction): what a loud noise could have hidden is heard as still there.
- **THE PHANTOM KICK** (the build): the kick is taken away beat by beat - beat four (bars 1-4), two and four (5-8), three of four (9-12), all four (13-16) - and each missing kick is replaced by a slammed noise burst, so the four-on-the-floor keeps thumping in the ear with no kick in it; the drop puts the real kick back.
- **NEVER STOPS**: a reese on F1 plays only the on-beat eighths; every off-beat eighth is a noise burst, so the cut bass is heard as one unbroken drone and the bursts double as the off-beat "hat".
- **THE DRONE MOVES** (v3, Harry's LFO note): the reese runs through a resonant low-pass that drifts on a 7-bar sine and a 3-bar triangle, opened by section (closed in A, opening through the build, widest at the peak); the bursts sweep their colour on a 5-bar cycle (a band-pass from ~500 Hz to 4 kHz) and drift across the field on another - so the never-stopping drone and the noise that fills it breathe against the bar instead of standing still.
- **THE SIREN** (v2): a hoover stab on the first beat of every fourth bar through B and C - F2, C3 and the flat ninth Gb3, a dark power chord diving into each hit - the peak-time alarm over the noise.
- **SEVEN**: chirper-two's c2-clank (borrowed from t10) on every seventh 16th, F4, turning against the bar and realigning every seven bars.


## t3 (chirper-one): peak-time warehouse, "the one comes home"

- **THE DISPLACED GRID**: intro and first groove - kick on the off-beats (16ths 2, 6, 10, 14), closed hats on the beats, and from bar 8 of A short hoover stabs on the and-of-1 and and-of-3: everything confirms the wrong grid. The intro plays through a master low-pass opening from 400 Hz.
- **THE VOICE**: in the break (kick out) a giant synthesised voice chants "one" (voice, phonemes w-ah1-n, A3) on every true downbeat, pitched an octave down with formants -5 (wM's formant-preserving pitch) and driven, over a sixteen-bar hoover swell on A minor and a snare roll (quarters, eighths, sixteenths).
- **HOME**: the drop puts the kick on the beats, open hats on the off-beats, claps on 2 and 4, a crash every 8 bars and the hoover's A minor stab on every one; the peak layers the distorted kick, adds a ride, an answering stab a minor third up, a reese rolling off-beat sixteenths on A1, and the voice every four bars. The outro lets the kick slip back to the off-beats, then out.
- **THE HELD BREATH** (v2): the beat before the drop is silence - after the voice's last "one" and the snare roll, nothing - and then the kick lands home.
- **A PEAK THAT UNFOLDS** (v3, taking away): in the peak the home stab and its answer a minor third up alternate bar by bar instead of piling onto the same bars, and the reese waits for the peak's second half - so the peak opens with the hard kick, the ride and the voice, then the bass rolls in sixteen bars later.

## t5 The Room Turns (chirper-two)
- **THE ORBITS**: rim (every 3 bars), clap (5), ride (7), cowbell (5, opposite the clap) circle the listener: pan on a song-time sine LFO `x`; a second LFO `y` a quarter-cycle behind darkens (lp -1.2 oct), quiets (-2.5 dB) and wets each voice as it passes behind. In the break the orbits speed to a bar a turn; in THE STOP they are dry and dead centre; after it they turn the other way (the pan LFO's phase flipped).
- **THE GALLOP**: the boom bass on each off-beat, the and then the a: D2 D2 D2 F2 | D2 D2 A2 G2, a D3 pickup every fourth bar.
- **THE STAB**: D minor add 9 (D3 F3 A3 E4) on the a-of-1 and the and-of-3 (and the e-of-4 every other bar), its band-pass on a 5-bar LFO, into a dotted ping-pong echo.
- Rim figure: the a-of-1, the and-of-2, the a-of-3 (and the and-of-4 every other bar).

## t1 Behind the Door (chirper-zero)
Generator `compose/chirpers4/src/chirpers4-t1.py`. The opener: deep / hypnotic techno, 122 bpm, A minor; occlusion.
- **THE WALL**: the club (kick, hats, sub, the cell) plays through a bus whose 24 dB low-pass and damp room are the wall between you and the floor - closed (about 200 Hz, a distant room) through the corridor, opening across the eight-bar door, open on the floors, shutting again over the last section's first eight bars. The music never changes; only the wall does.
- **THE CORRIDOR**: outside the door, always clear - a juno pad (Am9, then an Fmaj7#11 colour, four bars each) and pink-noise air; the kick first heard as a thud through the wall, and heard that way again at the very end, so the next track starts in the corridor.
- **THE CELL**: a deep pluck playing seven notes (A4 C5 E5 B4 D5 C5 E4) through a six-hit 3+3+2 bar (16ths 0 3 6 8 11 14), so the figure turns against both the bar and its own rhythm; its filter drifts on 7- and 5-bar LFOs, its resonance on a 3-bar one, its place in the field on a 5-bar one, with a dotted-quarter echo.

## t6 Beat Frequency (chirper-three)
Generator `compose/chirpers4/src/chirpers4-t6.py`. Minimal / functional techno, 130 bpm, G minor: the rhythm lives inside held notes.
- **THE THROB BASS**: one long held G1 per span whose harmonics come in pairs Δ Hz apart (k*f and k*f + Δ, k = 1..4), so the whole tone beats at Δ: Δ = the beat (2.17 Hz) throbs in quarters, 1.5x in triplets, 2x in eighths, 4x in sixteenths. Each span starts half a throb-period early so the dips land on the kicks: the bass breathes against the kick by physics (solo, master off: ~10 dB between the off-beat swell and the beat). Spans: quarters (groove), triplets (shift: 3 against the kick's 4, by interference), eighths (drive), the break stepping q t e s every four bars, quarters then eighths in the drop, half notes in the outro.
- **THE CHORD THAT PLAYS A RHYTHM**: a held G minor (G3 D4 F4 A4) whose voices are pair tones beating in half notes, dotted quarters, quarters and triplets: a polyrhythm that nobody plays; its low-pass drifts on a 7-bar LFO. It opens the track alone and closes it alone.
- **THE 3-3-2**: machine-kit hats in sixteenths with accents on 0 3 6 | 8 11 14, ghosts between, the e and a pushed late; the hats drift across the field on a 5-bar LFO.

