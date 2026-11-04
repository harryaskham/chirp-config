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
| `type: terrain` layer: wave terrain synthesis (1978). An orbit (`rx`, `ry` radii, `cx`, `cy` centre) circles a surface (`sines` = sin(kπx)·cos(kπy), or `ripple` = sin(kπr)) once a period; centred = odd harmonics, off-centre = even too, wider/higher `k` = brighter; `ratio` ≠ 1 drifts (1.007 slow morph); radii/centre/k modulatable (LFO on `cx` = timbre drift, env on `k` = filterless opening) | 758ba1dc | wM | |
| `type: pd` layer: Casio CZ phase distortion (1984). `pd: {shape, amount}`: `saw`/`square`/`pulse` bend a sine (amount 0) into those shapes (1); `reso_saw`/`reso_tri`/`reso_trap` put a resonance 1 + 15·amount × the note under a window, so sweeping amount (env/LFO) = the CZ's resonant-filter sweep with no filter; anti-alias knee limit; mean removed | f6713421 | wM | |
| `orbit` fx: moving sound sources (Chowning 1971). A path around the listener (`path=circle` around a centre `distance` ahead, `figure8`, or `line` = a fly-by from `radius` m left to right, `distance` ahead); per-ear distance delays give ITD and true Doppler (`doppler` 0..1), loudness falls from the closest approach, head shadow, darker behind and far; `rate` laps/s or `1/1`; `phase`, `mix`. Headphones | c7606671 | wM | |
| `type: chaos` layer: audio-rate chaotic oscillators, a strange attractor looping at the note's pitch. `chaos: {system: rossler\|duffing, axis: x\|y\|z, amount}`; `amount` walks the route to chaos: periodic tone → period doubling (octave-down subharmonic) → chaos near the pitch (Rössler doubles ~0.25–0.5, chaotic from ~0.6, 0.93 classic; Duffing doubles ~0.2, breaks up from ~0.35). An env on `amount` makes one note travel the whole route | f3872739 | wM | |
| `lpc` fx: LPC-10 linear predictive coding, the talking toys' / first speech chips' voice. Resample to `rate` (8 kHz), per `frame` (22.5 ms) an `order`-pole filter (10) + gain + voiced/unvoiced pitch, rebuilt from pulses or noise through the filter, held like an unsmoothed DAC. `pitch: auto` tracks, `pitch=C3` = monotone; `bits=5` = crunchy coefficients; `noise` breath. Speech stays intelligible (Whisper reads it); `lpc pitch=C3 bits=5` on voice-speech = the speaking toy On the grid from ee46ab71: its latency is compensated (onsets within ~5 ms; was 36-46 ms late), so no hand nudges; its level still depends on the source patch (voice-tts ~+14 dB), so solo-match. | 78e838c5 | wM | |
| `ks` layer: Karplus-Strong (1983) as published. Noise in a one-period loop with a two-point average = plucked string. `ks: {blend}` < 1 = the paper's drum (0.5 snare high / toms low; 0 = hollow harp an octave down), `stretch` S rings S× longer, `tune: false` = the original's flat high notes. `decay` = T60, `bright` = burst colour (bind vel for dynamics) | 8f150090 | wM | |
| orbit `level` (metres): the distance that plays at full level, so far paths are faint (1/distance) and distance lanes fade on their own; unset = full level at each path's closest approach (far paths even, not faint; chirper-three's finding) | 8f150090 | wM | |
| `scanned` layer: scanned synthesis (Verplank, Mathews & Shaw 2000), Max Mathews' late work. A ring of 128 masses+springs ripples at hand speed and is read round at the pitch as a wavetable, so the timbre IS the moving shape. `scanned: {speed}` laps/s (0.2 drifts, 2 shimmers; >4 rough), `width` strike (narrow bright), `smooth`, `centre`; `decay` = T60 of the motion; `push` (mods) = a hand holding the ring: an LFO/lane plays the timbre and keeps notes alive | ee46ab71 | wM | |
| `shaper` layer: Chebyshev waveshaping (Le Brun & Arfib 1979). A sine through a polynomial that writes `harmonics: [1, 0.5, …]` exactly at full drive; `index` (mods) thins it toward a sine, so an envelope/vel on index = a filter sweep with no filter (Risset's brass: louder = brighter). Odd-only lists = clarinet-hollow. No aliasing (harmonics past Nyquist dropped per note) | 817a5de6 | wM | |
| `fof` layer: FOF synthesis, Rodet's CHANT (IRCAM 1979-84). Each pitch period launches one decaying grain per formant; the grains add up to a sung vowel, no filters. `fof: {voice: soprano/alto/tenor/bass, vowel: a/e/i/o/u}` (Csound's tables); `vowel: u>a` + `morph` (mods) sings the vowel change on a lane; `attack` 3 ms (short buzzy, long round). Add 5.5 Hz vibrato via synth pitch mods for the classic CHANT soprano | 91b04b25 | wM | |
| scanned + lpc fixes: a fast push LFO can't pump the scanned ring (the hand follows push over ~150 ms; a sixteenth-note LFO silenced c8t2); `push` is a brightness control across 0..1 (0.1 round, 0.5 middle ripples, 1 the whole strike); scanned notes start at about -9 dB RMS (to keep t5/t8 mixes: t5 scanc push 1.0 gain -11dB, t8 wordscan push 0.74 gain -18dB); `lpc` is level-neutral whatever the source; a broken (NaN) layer goes quiet instead of silencing the song | 502b6b8d | wM | |
| Library patches for the new engines: `ks-nylon`, `ks-harp`, `ks-drum` (Karplus-Strong), `scanned-breath`, `scanned-mallet` (scanned; need 502b6b8d), `shaper-brass`, `shaper-reed` (Chebyshev), `fof-soprano`, `fof-chant` (CHANT). Reel: ~/.local/state/chirp-evidence/library2-20261104/reel.mp3 | library 32e6cd5c + a8361d86 | wM | |
| `kuramoto` layer: Kuramoto's coupled oscillators (1975), the maths of synchrony (fireflies, pacemakers, applause). A swarm (`count` 8, `wave` saw, `spread` 25 cents) pulled toward its mean phase by `coupling` (modulatable; 1 = critical): below 1 a beating chorus, above 1 a core locks onto the note (R 0.3 → 0.65 at 1.5 → 0.91 at 3). Notes start from random phases and find their pitch; a lane on coupling makes order emerge and dissolve | 63e9a72a | wM | |
| Fix: layer `pan` on fof/shaper/scanned/ks/chaos/pd/terrain/vosim/gendyn/bytebeat no longer silences their right side | 63e9a72a | wM | |
| `waveset` fx: Wishart's waveset distortion (CDP). The sound cut at upward zero crossings into wavesets (≤ `max` 20 ms), each (or each group of `n`) transformed whole: `reverse`, `transpose` (n harmonics up), `sine`/`square` substitution (any sound becomes a pitch-following buzz), `omit` (1 in n), `repeat` (hold the first of n), `shuffle` (seeded). Length kept; late by max (×n for group modes), compensated on tracks like lpc | a5cb622d | wM | |
| `sync` mod source: a kuramoto layer's coherence (0 a crowd … 1 locked; ~0.3 for a crowd of 8), readable by any synth param (filter, pitch, drive). A locked swarm grows purer and darker (centroid 390 → 170 Hz on saws at A2), so `sync` on a filter can make the agreement bloom open | (pending pin, wM) | wM | |
| Library patches: `risset-bell` (Risset's 1969 additive bell), `risset-arpeggio` (held notes arpeggiate their overtones, Mutations), `kuramoto-choir`, `kuramoto-flies` (swarms; need b8f9d6b1), `crumble-pad`, `waveset-buzz` (waveset; need b8f9d6b1). Reel: ~/.local/state/chirp-evidence/library3-20261104/reel.mp3 | risset-* library 9bc19360; the other four pending b8f9d6b1 | wM | |

## Measured (chirp-eco)
Measured 2026-11-03T18:01Z on chirp-8f150090 by `chirpers.py coverage chirpers8`: 12 composed songs; a feature counts when the song's plan or score uses it (prominence is your ear's call).

- **synthesis** (37/39): wave:sine (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12); wave:triangle (t1, t2, t4, t5, t6, t7, t8, t9, t10, t11, t12); wave:saw (t1, t3, t5, t6, t7, t8, t9, t10, t11, t12); wave:square (t1, t4, t5, t6, t7, t8, t9, t11); wave:pulse (t1, t3, t4, t6, t7, t8, t9, t11, t12); additive (t1, t3, t4, t6, t8, t9, t10, t11, t12); table (t8, t10, t11); shepard (t3, t12); sample (t11); machine (t1, t2, t3, t4, t5, t8, t10, t11, t12); modal (t2, t3, t4, t8, t11, t12); bowed (t4, t6, t7, t12); pluck (t3, t4, t5, t6, t11, t12); membrane (t3, t4, t11); plate (t8, t11); cymbal (t2, t4); bar (t3, t8, t11); vibes (t2, t3, t11); bell (t2, t3, t12); glock (t2, t3, t4, t11); gong (t3, t12); reed (t2, t9, t10); jet (t4); lips (t12); sax (t4); guitar (t5); fm/pm (t1, t4, t5, t6, t7, t8, t9, t10, t11, t12); sync (t10); shape:fold (t9); shape:crush (t6, t8, t9); bytebeat (t1, t2, t3, t4, t5, t6, t8, t10, t12); gendyn (t3, t4, t7, t8, t9, t11); vosim (t1, t2, t3, t4, t5, t6, t7, t8, t10, t12); terrain (t1, t2, t9, t11, t12); pd (t2, t4, t5, t6, t7, t8, t9, t10, t11, t12); chaos (t2, t4, t5, t7, t8, t9, t10, t12); ks (t9)
- **fx** (43/45): amp (t5); barberpole (t3, t12); cab (t5); chop (t4, t8); chorus (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12); cloud (t1, t2, t5, t6, t8); compressor (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12); crush (t4, t7, t9); delay (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12); drive (t3, t4, t5, t6, t7, t8, t9); duck (t4); eq (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12); filter (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12); follow-noise (t8); formant (t1, t11); freeze (t8); gain (t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12); gate (t11); glue (t3, t6, t7, t9, t11); ir (t5); limiter (t1, t3, t6, t7, t9, t10); lpc (t1, t2, t3, t4, t5, t8, t10, t12); morph (t1, t3, t4, t5, t6, t9); orbit (t2, t3, t4, t5, t8, t9, t10, t11, t12); ott (t4, t5, t8, t11); pan (t4, t11, t12); phantom (t12); phaser (t5, t7); pitch (t1, t2, t5, t7, t8, t11); pump (t1, t3, t5, t6, t8, t9, t10, t11); radio (t2, t5, t6, t7, t11); reverb (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12); ring (t6); stutter (t4, t8, t9, t11, t12); sympathetic (t5, t12); tape (t1, t4, t6, t7, t8, t9, t10, t11, t12); tapestop (t8, t11, t12); transient (t11); tremolo (t3, t4, t5, t6, t7, t11, t12); vinyl (t12); vocoder (t2, t5, t6, t8); wah (t6, t7); width (t2, t4, t5, t7, t11)
- **filters** (8/10): kind:lp (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12); kind:hp (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12); kind:bp (t1, t4, t5, t6, t7, t8, t11); kind:peak (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12); kind:lowshelf (t1, t4, t6, t9, t12); kind:highshelf (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12); comb (t11); ladder (t12)
- **time** (7/7): tempo map (t2, t4, t5, t6, t7, t8, t9, t10, t11, t12); risset (t12); warp (t2, t5, t8, t12); meter change (t2, t6, t9, t10, t12); swing (t1, t5, t8); swing_drift (t12); humanize (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12)
- **pitch** (8/8): tuning (t1, t2, t3, t6, t9, t10, t12); tuning:edo (t1, t2, t3, t6, t9, t12); tuning:steps (t2, t3, t10); tuning:ramp (t1, t2, t3, t9, t12); bend (t2, t4, t6, t9, t12); glide (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12); strum (t3, t4, t5, t11, t12); expr (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12)
- **systems** (17/17): vars (t1, t2, t3, t5, t6, t8, t9, t11, t12); lfo (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12); auto (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12); chance (t3, t6, t8, t9, t11); choices (t4, t11); euclid (t4); every (t1, t2, t3, t5, t6, t8, t9, t11, t12); vary (t2, t3, t6, t12); gen:logistic (t5, t9); gen:lorenz (t1, t3, t6, t8, t11, t12); gen:ca (t1, t3); gen:lsystem (t10, t12); gen:markov (t5, t6); gen:life (t3, t4, t7, t8, t10, t12); gen:henon (t9, t11); gen:walk (t6, t11); var system (t1, t3, t5, t6, t8, t9, t11, t12)
- **voice** (2/2): voice (tts) (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12); vocoder on voice (t2, t5, t6, t8)

**Not used by any track yet:** shape:tanh, shape:clip, autolevel, clip, kind:notch, kind:allpass

| track | title | features |
|---|---|---|
| t1 | Echolalia | 46 |
| t2 | Everything Falls to One | 50 |
| t3 | Three Neighbours | 56 |
| t4 | Small Things Before Large | 58 |
| t5 | Agreeing on a Speed | 57 |
| t6 | No Errors Since | 58 |
| t7 | Annealing | 42 |
| t8 | Kept in Mercury | 60 |
| t9 | Period Doubling | 54 |
| t10 | Call and Return | 41 |
| t11 | The Weather Indoors | 64 |
| t12 | Still Running When You Wake | 66 |
