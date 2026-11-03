# chirpers VIII: the engine coverage board

Harry asked for a showcase of ALL the different combinations of chirp's engine features. Across the 12 tracks, every feature below should be SHOWCASED somewhere (prominent, audible, used well), and the best tracks combine features nobody has combined yet. Claim a cluster when you take a track (put your track in "showcased by"), keep clusters distinct, and add anything new you or wM build at the bottom. chirp-eco keeps a measured coverage table (which features each song actually uses) in the "measured" section.

## Synthesis
| feature | showcased by |
|---|---|
| osc waves: sine, triangle, saw, square, pulse (PWM) | t7 (chirper-one) |
| additive | t7 (chirper-one) |
| FM / phase modulation between layers, hard sync | t10 (chirper-one) |
| motif transforms (@motifs: inversion, retrograde, augmentation, diminution), harmony $N, scale degrees %N | t10 (chirper-one) |
| tables (wavetable-style) | t11 (chirper-three), t10 (chirper-one); also t8 (chirper-zero: a wavetable whose frames are the stored word's bits, v19) |
| shepard (endless glides, scales, chords) | t12 (chirper-three) |
| sample | t11 (chirper-three) |
| drum machines and kits (machine-kit, dusty, physical drums) | t7 (chirper-one); the `machine` layer (circuit-modelled drum-machine voices): t2's whole kit, a tuned tom on the backbeat (v29) and a G1 kick and closed/open hats (v30), plus a cowbell in t5 v27 (chirper-zero) |
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
| chorus, phaser, wah, tremolo, width, pan | t5 (chirper-zero); t4 (chirper-three, pan as array index); t6 (chirper-two, `wah` envelope-swept on a clavinet, v4) |
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
| meter changes | t9 (chirper-two); also t2 (chirper-zero: the break in 3/4, the 4-2-1 loop counted as a waltz, v21) |
| polymeter by step length | t9 (chirper-two) |
| swing, swing drift, humanize | t5 (chirper-zero) |

## Pitch and tuning
| feature | showcased by |
|---|---|
| tuning: cents, ratios (just intonation) | t3 (chirper-two); t8 (chirper-zero, a stretched octave); t11 (chirper-three, the harmonic series 8-16); t2 (chirper-zero, a ramp into 5-limit just G from the break) |
| tuning: EDO / non-octave scales | t9 (chirper-two); t12 (chirper-three, 31-EDO); t4 (chirper-three, Carlos alpha, non-octave) |
| bend, glide, strum | t12 (chirper-three); t2 (chirper-zero, bend: every 3n+1 note of the hailstone scooped up from a semitone below - `bend=-1 X/32 bend=-0.5 _/32 bend= _/16` - the halvings plain) |
| expression paths (^NAME=a>b) | t12 (chirper-three) |

## Generators and systems
| feature | showcased by |
|---|---|
| vars and expr | t12 (chirper-three); t8 (chirper-zero, a Lorenz var on the line tape's warp); t5 (chirper-zero, a logistic var at r 2.95 that settles after a damped two-cycle, stepping every two bars on the acid's resonance - agreement as a fixed point) |
| lfo and auto lanes | t7 (chirper-one) |
| chance (?p) and choices (a\|b) | t6 (chirper-two) |
| Euclidean patterns | t3 (chirper-two) |
| every / vary / seeds | t8 (chirper-zero), t10 (chirper-one) |
| complex systems (chaotic maps, cellular automata, L-systems, Markov): ask wM | t3 (chirper-two); t12 (chirper-three, an L-system); t11 (chirper-three, the Lorenz attractor); t4 (chirper-three, sorting algorithms); t5 (chirper-zero, an engine Markov chain over the hook as the lead) |

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
| complex systems: track `gen` (notes after the score from a `notes` pool) and var `system` (steps): `logistic` (r), `lorenz` (attractor, axis), `ca` (rule 0-255, width, poly; on kit pieces a drum machine), `lsystem` (axiom, rules, depth; turtle +/- [ ]), `markov` (order, learnt from score tokens in `from`); seeded (README "Complex systems") | d082b8f5; t4 (chirper-three, sorting algorithms) | wM | t1 (chirper-one: gen markov orders 1/2/3 learnt from a voice, gen ca rule 90 rim), t10 (chirper-one: gen lsystem - [ ] as call and return - on a Werckmeister III steps tuning); t1 also a var system (lorenz) steering a formant vowel |
| `morph` fx with `key: TRACK` (pre-fader; mute the key): `mode: morph` blends two spectra (`amount` 0 = this track, 1 = the key; automate it to turn a pad into a drum loop), `mode: cross` gives this track the key's spectral envelope (strings that speak a tts line) (README "morph") | 8ef47431 | wM | t1 (chirper-one: strings cross-synthesised by a humanized voice speak the line); t5 (chirper-zero, the guitar morphing into the acid once they agree) |
| `chirp tts --sing "D4/8 F4 A4/4 … ./4"`: the words sung on a written melody, one syllable per note (lengths latch, `.` rests, `_` holds); level legato notes, a scoop into each phrase, a fall off its end, vibrato on long notes; `--humanize` loosens intonation; `--mode choir` harmonises (README "Speech") | b4151423 | wM |; t2 (chirper-zero, "odd goes up, even comes down", v23; was "high as the cloud, and then home"); t8 (chirper-zero, "it only travels" (v22; was "say it back to me") at the outro's ninth bar, its m-notes moved by hand onto a 1210-cent stretched octave in Hz, so a song with no `tuning:` block still sings in its own tuning) |
| `type: bytebeat` layer (one-line computer music of a counter `t`): `bytebeat: {formula: "t*(t>>9|t>>13)&t>>6", clock: 8000}`, C operators on 32-bit unsigned ints (`* / % + - << >> < > == != & ^ \| && \|\| ?:`, unary `- ~ !`), the low byte the sample, held between counts (raw 8-bit steps with their aliasing). Each note restarts `t`; middle C counts at `clock`, an octave up twice as fast. `t*8` at C2 is about 62 Hz, so bass works; `&64` styles at low clocks fall below 30 Hz, so watch the floor | 709cf900 | wM | |
| more systems for `gen` and vars: `life` (Conway's Game of Life on a `width` × `height` torus as a sequencer: a playhead reads a column per step, live cells sound up to `poly`, rows pick the pool bottom-low, each pass is a generation; `life: B3/S23` or any B/S rule; `init: center` = R-pentomino, `glider`, `random`, rows `010/001/111`), `henon` (`a` 1.4, `b` 0.3, `axis` x/y), `walk` (random walk over `width` positions, up to `step`, bouncing) | ade7b930 | wM | |
| `type: gendyn` layer: Xenakis's dynamic stochastic synthesis (GENDY3). A cycle of `points` breakpoints whose levels (`amp` step) and segment lengths (`time` step, within `spread` of the period) random-walk every cycle and bounce off walls; `dist: cauchy\|uniform`; amp/time/spread modulatable. Small `amp` = living grainy tone at pitch; `time: 0.25, spread: 1.2` = glissandi | 6014b933 | wM | |
| `type: vosim` layer: Kaegi/Tempelaars VOSIM (1978). Each period starts with `pulses` sin² pulses `1/formant` long, each `decay` × the last, then silence; `formant` (Hz, mods in octaves) places the formant, so sweeping it talks and two layers make a vowel; 1 pulse low = round bass, many pulses high = bell | 1a5a0572 | wM | |
| `type: terrain` layer: wave terrain synthesis (1978). An orbit (`rx`, `ry` radii, `cx`, `cy` centre) circles a surface (`sines` = sin(kπx)·cos(kπy), or `ripple` = sin(kπr)) once a period; centred = odd harmonics, off-centre = even too, wider/higher `k` = brighter; `ratio` ≠ 1 drifts (1.007 slow morph); radii/centre/k modulatable (LFO on `cx` = timbre drift, env on `k` = filterless opening) | (pending pin, wM) | wM | |

## Measured (chirp-eco)
Measured 2026-11-03T04:02Z on chirp-ade7b930 by `chirpers.py coverage chirpers8`: 12 composed songs; a feature counts when the song's plan or score uses it (prominence is your ear's call).

- **synthesis** (31/33): wave:sine (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12); wave:triangle (t1, t4, t5, t6, t7, t8, t9, t10, t11, t12); wave:saw (t1, t2, t3, t5, t6, t7, t8, t9, t10, t11, t12); wave:square (t1, t4, t5, t6, t7, t8, t9, t11); wave:pulse (t1, t2, t3, t4, t5, t6, t7, t8, t9, t11, t12); additive (t1, t3, t4, t6, t8, t9, t10, t11, t12); table (t8, t10, t11); shepard (t3, t12); sample (t11); machine (t1, t2, t3, t4, t5, t8, t10, t11, t12); modal (t2, t3, t4, t8, t11, t12); bowed (t4, t6, t12); pluck (t3, t4, t5, t6, t9, t11, t12); membrane (t3, t4, t11); plate (t8, t11); cymbal (t2, t4); bar (t3, t8, t11); vibes (t2, t3, t11); bell (t2, t3, t12); glock (t2, t3, t4, t11); gong (t3, t12); reed (t2, t9, t10); jet (t4); lips (t12); sax (t4); guitar (t5); fm/pm (t1, t4, t5, t6, t7, t8, t9, t10, t11, t12); sync (t10); shape:fold (t9); shape:crush (t6, t8, t9); bytebeat (t1, t2, t3, t4, t5, t6, t8, t10, t12)
- **fx** (41/43): amp (t5); barberpole (t3, t12); cab (t5); chop (t4, t8); chorus (t1, t2, t3, t4, t5, t6, t7, t8, t9, t11, t12); cloud (t1, t2, t5, t6, t8); compressor (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12); crush (t4, t7, t9); delay (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12); drive (t3, t4, t5, t6, t7, t8, t9); duck (t4); eq (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12); filter (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12); follow-noise (t8); formant (t1, t11); freeze (t8); gain (t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12); gate (t11); glue (t3, t6, t7, t9, t11); ir (t5); limiter (t1, t3, t6, t7, t9, t10); morph (t1, t3, t4, t5, t6, t9); ott (t4, t5, t8, t11); pan (t4, t11, t12); phantom (t12); phaser (t5, t7); pitch (t1, t2, t5, t7, t8, t11); pump (t1, t3, t5, t6, t8, t9, t10, t11); radio (t2, t5, t6, t7, t11); reverb (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12); ring (t6); stutter (t4, t8, t9, t11, t12); sympathetic (t5, t12); tape (t1, t4, t6, t7, t8, t9, t10, t11, t12); tapestop (t8, t12); transient (t11); tremolo (t3, t4, t5, t6, t7, t11, t12); vinyl (t12); vocoder (t6); wah (t6, t7); width (t4, t7, t11)
- **filters** (8/10): kind:lp (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12); kind:hp (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12); kind:bp (t1, t4, t5, t6, t7, t8, t11); kind:peak (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12); kind:lowshelf (t1, t4, t6, t9, t12); kind:highshelf (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12); comb (t11); ladder (t12)
- **time** (7/7): tempo map (t2, t4, t5, t6, t9, t10, t11, t12); risset (t12); warp (t8, t12); meter change (t2, t6, t9, t10, t12); swing (t5, t8); swing_drift (t12); humanize (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12)
- **pitch** (8/8): tuning (t1, t2, t3, t6, t9, t10, t12); tuning:edo (t1, t2, t3, t6, t9, t12); tuning:steps (t2, t3, t10); tuning:ramp (t1, t2, t3, t9, t12); bend (t2, t4); glide (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12); strum (t3, t5, t9, t11, t12); expr (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12)
- **systems** (15/17): vars (t1, t2, t3, t5, t6, t8, t9, t11, t12); lfo (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12); auto (t1, t2, t3, t4, t5, t6, t7, t8, t10, t11, t12); chance (t3, t6, t8, t9, t11); choices (t4, t11); euclid (t4); every (t1, t2, t3, t5, t6, t8, t9, t11, t12); vary (t2, t3, t6, t12); gen:logistic (t5, t9); gen:lorenz (t1, t3, t6, t8, t11, t12); gen:ca (t1, t3); gen:lsystem (t10, t12); gen:markov (t5, t6); gen:life (t4); var system (t1, t3, t5, t6, t8, t9, t11, t12)
- **voice** (2/2): voice (tts) (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12); vocoder on voice (t6)

**Not used by any track yet:** shape:tanh, shape:clip, autolevel, clip, kind:notch, kind:allpass, gen:henon, gen:walk

| track | title | features |
|---|---|---|
| t1 | Echolalia | 42 |
| t2 | Everything Falls to One | 41 |
| t3 | Three Neighbours | 51 |
| t4 | Small Things Before Large | 51 |
| t5 | Agreeing on a Speed | 49 |
| t6 | No Errors Since | 54 |
| t7 | Annealing | 35 |
| t8 | Kept in Mercury | 50 |
| t9 | Period Doubling | 47 |
| t10 | Call and Return | 34 |
| t11 | The Weather Indoors | 57 |
| t12 | Still Running When You Wake | 58 |
