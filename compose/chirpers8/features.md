# chirpers VIII: the engine coverage board

Harry asked for a showcase of ALL the different combinations of chirp's engine features. Across the 12 tracks, every feature below should be SHOWCASED somewhere (prominent, audible, used well), and the best tracks combine features nobody has combined yet. Claim a cluster when you take a track (put your track in "showcased by"), keep clusters distinct, and add anything new you or wM build at the bottom. chirp-eco keeps a measured coverage table (which features each song actually uses) in the "measured" section.

## Synthesis
| feature | showcased by |
|---|---|
| osc waves: sine, triangle, saw, square, pulse (PWM) | t7 (chirper-one) |
| additive | t7 (chirper-one) |
| FM / phase modulation between layers, hard sync | t10 (chirper-one) |
| motif transforms (@motifs: inversion, retrograde, augmentation, diminution), harmony $N, scale degrees %N | t10 (chirper-one) |
| tables (wavetable-style) | t11 (chirper-three), t10 (chirper-one) |
| shepard (endless glides, scales, chords) | t12 (chirper-three) |
| sample | t11 (chirper-three) |
| drum machines and kits (machine-kit, dusty, physical drums) | t7 (chirper-one) |
| physical: modal | t3 (chirper-two) |
| physical: bowed | t12 (chirper-three) |
| physical: pluck | t12 (chirper-three) |
| physical: membrane | t5 (chirper-zero) |
| physical: reed | t2 (chirper-zero, clarinet) |
| physical: lips (brass) | t12 (chirper-three) |
| physical: bar, bell, glock, gong | t3 (chirper-two) |
| guitar with amps and cabs | t5 (chirper-zero) |
| shapers: fold, tanh, clip, crush | t7 (chirper-one) |
## Processing (fx)
| feature | showcased by |
|---|---|
| filter family: lp / hp / bp / notch / peak / shelves / allpass / comb / ladder | t5 (chirper-zero) |
| ring, formant, vocoder | t6 (chirper-two) |
| cloud (grains), freeze | t8 (chirper-zero) |
| chop, stutter, tapestop, tape, vinyl | t8 (chirper-zero) |
| delay, reverb (room / plate / hall / chamber / spring), ir | t8 (chirper-zero) |
| chorus, phaser, wah, tremolo, width, pan | t5 (chirper-zero); t4 (chirper-three, pan as array index) |
| barberpole, phantom, sympathetic | t12 (chirper-three) |
| radio, follow-noise | t5 (chirper-zero) |
| pitch | t11 (chirper-three) |
| crush, drive, clip, amp, cab | t5 (chirper-zero) |
| dynamics: compressor, glue, ott, transient, gate, duck, pump, limiter, autolevel | t11 (chirper-three) |

## Time
| feature | showcased by |
|---|---|
| tempo maps and ramps | t9 (chirper-two) |
| risset (accelerando / decelerando) | t12 (chirper-three) |
| warp | t12 (chirper-three) |
| meter changes | t9 (chirper-two) |
| polymeter by step length | t9 (chirper-two) |
| swing, swing drift, humanize | t5 (chirper-zero) |

## Pitch and tuning
| feature | showcased by |
|---|---|
| tuning: cents, ratios (just intonation) | t3 (chirper-two); t8 (chirper-zero, a stretched octave); t11 (chirper-three, the harmonic series 8-16) |
| tuning: EDO / non-octave scales | t9 (chirper-two); t12 (chirper-three, 31-EDO); t4 (chirper-three, Carlos alpha, non-octave) |
| bend, glide, strum | t12 (chirper-three) |
| expression paths (^NAME=a>b) | t12 (chirper-three) |

## Generators and systems
| feature | showcased by |
|---|---|
| vars and expr | t12 (chirper-three) |
| lfo and auto lanes | t7 (chirper-one) |
| chance (?p) and choices (a\|b) | t6 (chirper-two) |
| Euclidean patterns | t3 (chirper-two) |
| every / vary / seeds | t8 (chirper-zero), t10 (chirper-one) |
| complex systems (chaotic maps, cellular automata, L-systems, Markov): ask wM | t3 (chirper-two); t12 (chirper-three, an L-system); t11 (chirper-three, the Lorenz attractor); t4 (chirper-three, sorting algorithms) |

## Voice
| feature | showcased by |
|---|---|
| chirp tts, humanized (realistic) | t6 (chirper-two) |
| speech-to-song (repeat / melodize / melody) | t6 (chirper-two) |
| vocoder / formant / radio on voice | t6 (chirper-two) |

## New this album (built by wM or you)
| feature | commit | built by | showcased by |
|---|---|---|---|
| microtonal `tuning` (song or track): `{edo: 19}`, `{edo: 13, period: 3/1}` (Bohlen-Pierce), `{steps: [9/8, 5/4, …, 2/1]}` (scala ratios/cents), `root`, `map: nearest` (written notes snap) or `keys` (keys count steps); a list retunes over time with `ramp`; score `~N` plays step N exactly (README "Microtonal tunings") | a657923e | wM | t1 (chirper-one: a tuning list with ramps, 5 -> 12 -> 24 -> 96 EDO, speech pitches snapping to a sharpening grid) |
| complex systems: track `gen` (notes after the score from a `notes` pool) and var `system` (steps): `logistic` (r), `lorenz` (attractor, axis), `ca` (rule 0-255, width, poly; on kit pieces a drum machine), `lsystem` (axiom, rules, depth; turtle +/- [ ]), `markov` (order, learnt from score tokens in `from`); seeded (README "Complex systems") | d082b8f5; t4 (chirper-three, sorting algorithms) | wM | |

## Measured (chirp-eco)
Not measured yet: coverage appears here once songs exist.
