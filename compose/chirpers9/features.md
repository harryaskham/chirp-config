# Accretion (chirpers9): the engine board

What each track leans on. Not a coverage checklist this time: Accretion is about depth, and about elements that
carry and transform from track to track. Claim what your track features (`tN (you)`) so neighbours can choose
contrasting colours, and add a row when a new engine feature lands (opt-in, gated byte-identical against the
released albums first). Ask wM for features; the voice has no ceiling.

## Synthesis
| feature | featured by |
|---|---|
| osc waves: sine, triangle, saw, square, pulse (PWM) | |
| additive | t2 (chirper-one: risset-bell lens) |
| FM / phase modulation between layers, hard sync | |
| motif transforms (@motifs: inversion, retrograde, augmentation, diminution), harmony $N, scale degrees %N | t2 (chirper-one: E1 inverted, retrograde canon, augmented; E2 augmented) |
| tables (wavetable-style) | |
| shepard (endless glides, scales, chords) | |
| sample | |
| drum machines and kits (machine-kit, dusty, physical drums) | t2 (chirper-one: 909); t4 (chirper-three): brush-kit, half time |
| physical: modal | |
| physical: bowed | t4 (chirper-three): cellos carry E4 |
| physical: pluck | t4 (chirper-three): upright bass |
| physical: membrane | |
| physical: reed | |
| physical: lips (brass) | |
| physical: bar, bell, glock, gong | |
| guitar with amps and cabs | |
| shapers: fold, tanh, clip, crush | |
## Processing (fx)
| feature | featured by |
|---|---|
| filter family: lp / hp / bp / notch / peak / shelves / allpass / comb / ladder | |
| ring, formant, vocoder | |
| cloud (grains), freeze | |
| chop, stutter, tapestop, tape, vinyl | t2 (chirper-one) |
| delay, reverb (room / plate / hall / chamber / spring), ir | |
| chorus, phaser, wah, tremolo, width, pan | |
| barberpole, phantom, sympathetic | |
| radio, follow-noise | |
| pitch | |
| crush, drive, clip, amp, cab | |
| dynamics: compressor, glue, ott, transient, gate, duck, pump, limiter, autolevel | |

## Time
| feature | featured by |
|---|---|
| tempo maps and ramps | t2 (chirper-one: 90 -> 98 ramp between flat seams); t4 (chirper-three): 108 -> 112 ramp, flat across both seams |
| risset (accelerando / decelerando) | |
| warp | |
| meter changes | |
| polymeter by step length | t2 (chirper-one: 7 / 3 / 5 / 4 converging at the crest) |
| swing, swing drift, humanize | |

## Pitch and tuning
| feature | featured by |
|---|---|
| tuning: cents, ratios (just intonation) | |
| tuning: EDO / non-octave scales | |
| bend, glide, strum | |
| expression paths (^NAME=a>b) | |

## Generators and systems
| feature | featured by |
|---|---|
| vars and expr | |
| lfo and auto lanes | |
| chance (?p) and choices (a\| |
| Euclidean patterns | |
| every / vary / seeds | |
| complex systems (chaotic maps, cellular automata, L-systems, Markov): ask wM | |

## Voice
| feature | featured by |
|---|---|
| chirp tts, humanized (realistic) | t4 (chirper-three): sung voice layer, humanize 0.5, warm close tract (formant_bw 1.6, ph_soft, breath) |
| speech-to-song (repeat / melodize / melody) | |
| vocoder / formant / radio on voice | t2 (chirper-one: tts whisper) |

## Built for Standby Amber (all available)
| feature | commit | built by | showcased by |
|---|---|---|---|
| microtonal `tuning` (song or track): `{edo: 19}`, `{edo: 13, period: 3/1}` (Bohlen-Pierce), `{steps: [9/8, 5/4, …, 2/1]}` (scala ratios/cents), `root`, `map: nearest` (written notes snap) or `keys` (keys count steps); a list retunes over time with `ramp`; score `~N` plays step N exactly (README "Microtonal tunings") | |
| complex systems: track `gen` (notes after the score from a `notes` pool) and var `system` (steps): `logistic` (r), `lorenz` (attractor, axis), `ca` (rule 0-255, width, poly; on kit pieces a drum machine), `lsystem` (axiom, rules, depth; turtle +/- [ ]), `markov` (order, learnt from score tokens in `from`); seeded (README "Complex systems") | |
| `morph` fx with `key: TRACK` (pre-fader; mute the key): `mode: morph` blends two spectra (`amount` 0 = this track, 1 = the key; automate it to turn a pad into a drum loop), `mode: cross` gives this track the key's spectral envelope (strings that speak a tts line) (README "morph") | |
| `chirp tts --sing "D4/8 F4 A4/4 … ./4"`: the words sung on a written melody, one syllable per note (lengths latch, `.` rests, `_` holds); level legato notes, a scoop into each phrase, a fall off its end, vibrato on long notes; `--humanize` loosens intonation; `--mode choir` harmonises (README "Speech") | |
| `type: bytebeat` layer (one-line computer music of a counter `t`): `bytebeat: {formula: "t*(t>>9| |
| more systems for `gen` and vars: `life` (Conway's Game of Life on a `width` × `height` torus as a sequencer: a playhead reads a column per step, live cells sound up to `poly`, rows pick the pool bottom-low, each pass is a generation; `life: B3/S23` or any B/S rule; `init: center` = R-pentomino, `glider`, `random`, rows `010/001/111`), `henon` (`a` 1.4, `b` 0.3, `axis` x/y), `walk` (random walk over `width` positions, up to `step`, bouncing) | |
| `type: gendyn` layer: Xenakis's dynamic stochastic synthesis (GENDY3). A cycle of `points` breakpoints whose levels (`amp` step) and segment lengths (`time` step, within `spread` of the period) random-walk every cycle and bounce off walls; `dist: cauchy\| |
| `type: vosim` layer: Kaegi/Tempelaars VOSIM (1978). Each period starts with `pulses` sin² pulses `1/formant` long, each `decay` × the last, then silence; `formant` (Hz, mods in octaves) places the formant, so sweeping it talks and two layers make a vowel; 1 pulse low = round bass, many pulses high = bell | |
| `type: terrain` layer: wave terrain synthesis (1978). An orbit (`rx`, `ry` radii, `cx`, `cy` centre) circles a surface (`sines` = sin(kπx)·cos(kπy), or `ripple` = sin(kπr)) once a period; centred = odd harmonics, off-centre = even too, wider/higher `k` = brighter; `ratio` ≠ 1 drifts (1.007 slow morph); radii/centre/k modulatable (LFO on `cx` = timbre drift, env on `k` = filterless opening) | |
| `type: pd` layer: Casio CZ phase distortion (1984). `pd: {shape, amount}`: `saw`/`square`/`pulse` bend a sine (amount 0) into those shapes (1); `reso_saw`/`reso_tri`/`reso_trap` put a resonance 1 + 15·amount × the note under a window, so sweeping amount (env/LFO) = the CZ's resonant-filter sweep with no filter; anti-alias knee limit; mean removed | |
| `orbit` fx: moving sound sources (Chowning 1971). A path around the listener (`path=circle` around a centre `distance` ahead, `figure8`, or `line` = a fly-by from `radius` m left to right, `distance` ahead); per-ear distance delays give ITD and true Doppler (`doppler` 0..1), loudness falls from the closest approach, head shadow, darker behind and far; `rate` laps/s or `1/1`; `phase`, `mix`. Headphones | |
| `type: chaos` layer: audio-rate chaotic oscillators, a strange attractor looping at the note's pitch. `chaos: {system: rossler\| |
| `lpc` fx: LPC-10 linear predictive coding, the talking toys' / first speech chips' voice. Resample to `rate` (8 kHz), per `frame` (22.5 ms) an `order`-pole filter (10) + gain + voiced/unvoiced pitch, rebuilt from pulses or noise through the filter, held like an unsmoothed DAC. `pitch: auto` tracks, `pitch=C3` = monotone; `bits=5` = crunchy coefficients; `noise` breath. Speech stays intelligible (Whisper reads it); `lpc pitch=C3 bits=5` on voice-speech = the speaking toy On the grid from ee46ab71: its latency is compensated (onsets within ~5 ms; was 36-46 ms late), so no hand nudges; its level still depends on the source patch (voice-tts ~+14 dB), so solo-match. | |
| `ks` layer: Karplus-Strong (1983) as published. Noise in a one-period loop with a two-point average = plucked string. `ks: {blend}` < 1 = the paper's drum (0.5 snare high / toms low; 0 = hollow harp an octave down), `stretch` S rings S× longer, `tune: false` = the original's flat high notes. `decay` = T60, `bright` = burst colour (bind vel for dynamics) | |
| orbit `level` (metres): the distance that plays at full level, so far paths are faint (1/distance) and distance lanes fade on their own; unset = full level at each path's closest approach (far paths even, not faint; chirper-three's finding) | |
| `scanned` layer: scanned synthesis (Verplank, Mathews & Shaw 2000), Max Mathews' late work. A ring of 128 masses+springs ripples at hand speed and is read round at the pitch as a wavetable, so the timbre IS the moving shape. `scanned: {speed}` laps/s (0.2 drifts, 2 shimmers; >4 rough), `width` strike (narrow bright), `smooth`, `centre`; `decay` = T60 of the motion; `push` (mods) = a hand holding the ring: an LFO/lane plays the timbre and keeps notes alive | |
| `shaper` layer: Chebyshev waveshaping (Le Brun & Arfib 1979). A sine through a polynomial that writes `harmonics: [1, 0.5, …]` exactly at full drive; `index` (mods) thins it toward a sine, so an envelope/vel on index = a filter sweep with no filter (Risset's brass: louder = brighter). Odd-only lists = clarinet-hollow. No aliasing (harmonics past Nyquist dropped per note) | |
| `fof` layer: FOF synthesis, Rodet's CHANT (IRCAM 1979-84). Each pitch period launches one decaying grain per formant; the grains add up to a sung vowel, no filters. `fof: {voice: soprano/alto/tenor/bass, vowel: a/e/i/o/u}` (Csound's tables); `vowel: u>a` + `morph` (mods) sings the vowel change on a lane; `attack` 3 ms (short buzzy, long round). Add 5.5 Hz vibrato via synth pitch mods for the classic CHANT soprano | |
| scanned + lpc fixes: a fast push LFO can't pump the scanned ring (the hand follows push over ~150 ms; a sixteenth-note LFO silenced c8t2); `push` is a brightness control across 0..1 (0.1 round, 0.5 middle ripples, 1 the whole strike); scanned notes start at about -9 dB RMS (to keep t5/t8 mixes: t5 scanc push 1.0 gain -11dB, t8 wordscan push 0.74 gain -18dB); `lpc` is level-neutral whatever the source; a broken (NaN) layer goes quiet instead of silencing the song | |
| Library patches for the new engines: `ks-nylon`, `ks-harp`, `ks-drum` (Karplus-Strong), `scanned-breath`, `scanned-mallet` (scanned; need 502b6b8d), `shaper-brass`, `shaper-reed` (Chebyshev), `fof-soprano`, `fof-chant` (CHANT). Reel: ~/.local/state/chirp-evidence/library2-20261104/reel.mp3 | |
| `chirp vis` / `chirp video` (visuals, not sound; every render unchanged): looks (layers: plasma, noise, rings/tunnel, grid, spectrum, scope, lines, notes roll/clock/stars, particles, shape, segment text; filters: feedback, bloom, kaleido, mirror, warp, chroma, scanlines, …) driven by expressions of `audio.*`, `track.NAME.hit/level/key`, `time.beat`, `section.progress`, the look's own `lfo`/`env`/`var`; programmes switch looks at `32bar` / `section:NAME` with crossfades. `chirp video -f SONG --look kraft -o x.mp4` (soundtrack byte-identical to `chirp render`), `--still`, `--sheet N`; `v` in `chirp watch`, `chirp vis watch`, the web app's visual pane. Flash guard on. For album videos. | |
| `kuramoto` layer: Kuramoto's coupled oscillators (1975), the maths of synchrony (fireflies, pacemakers, applause). A swarm (`count` 8, `wave` saw, `spread` 25 cents) pulled toward its mean phase by `coupling` (modulatable; 1 = critical): below 1 a beating chorus, above 1 a core locks onto the note (R 0.3 → 0.65 at 1.5 → 0.91 at 3). Notes start from random phases and find their pitch; a lane on coupling makes order emerge and dissolve | t2 (chirper-one: the pad locks at the crest) |
| Fix: layer `pan` on fof/shaper/scanned/ks/chaos/pd/terrain/vosim/gendyn/bytebeat no longer silences their right side | |
| `waveset` fx: Wishart's waveset distortion (CDP). The sound cut at upward zero crossings into wavesets (≤ `max` 20 ms), each (or each group of `n`) transformed whole: `reverse`, `transpose` (n harmonics up), `sine`/`square` substitution (any sound becomes a pitch-following buzz), `omit` (1 in n), `repeat` (hold the first of n), `shuffle` (seeded). Length kept; late by max (×n for group modes), compensated on tracks like lpc | |
| `sync` mod source: a kuramoto layer's coherence (0 a crowd … 1 locked; ~0.3 for a crowd of 8), readable by any synth param (filter, pitch, drive). A locked swarm grows purer and darker (centroid 390 → 170 Hz on saws at A2), so `sync` on a filter can make the agreement bloom open | |
| Library patches: `risset-bell` (Risset's 1969 additive bell), `risset-arpeggio` (held notes arpeggiate their overtones, Mutations), `kuramoto-choir`, `kuramoto-flies` (swarms; need b8f9d6b1), `crumble-pad`, `waveset-buzz` (waveset; need b8f9d6b1). Reel: ~/.local/state/chirp-evidence/library3-20261104/reel.mp3 | t2 (chirper-one) |
| `pvoc` fx: a phase vocoder's classic transforms (Moorer 1978, Dolson 1986; AudioSculpt) on 1024-sample windows: `robot` (`pitch=D3`; phases zeroed, any voice a monotone machine on that note; several on a chord = a machine choir), `whisper` (random phases: vowels kept, pitch gone), `blur` (`amount` 0..0.99: each sound's colour hangs on). Level-matched (robot/whisper); 21 ms delay compensated on tracks like lpc | |
| `chip` layer: the 8-bit sound chips' channels (NES 2A03, Game Boy wave): `kind: pulse` (`duty` snaps to 1/8, 1/4, 1/2, 3/4; modulatable), `triangle` (32-step staircase, the NES bass), `wave` (`table` of 4-bit levels), `noise` (15-bit LFSR at the 2A03's 16 rates; `short` = 93-step metallic loop). Pitches from 11-bit timers (`clock` 1789773; C7 = 2110.6 Hz, as on the console; 0 = exact). Band-limited | t2 (chirper-one: chip-metal E2, triangle bass, pulse E1) |
| Library patches (chip; need 7ce23396): `nes-pulse-lead`, `nes-triangle-bass`, `nes-noise-hat`, `nes-noise-snare`, `chip-metal` (93-step short noise), `gb-wave-pad`. Reel: ~/.local/state/chirp-evidence/library4-20261104/reel.mp3 | t2 (chirper-one); t4 (chirper-three: nes-noise-hat, a 7-in-16 euclid of air) |

## New for Accretion (engine c3c8958a, adopted 5 Nov)
| feature | featured by |
|---|---|
| stepped LFOs: an `lfo` with `steps: [...]` plays them in turn, one every 1/rate (`once` holds the last). Retriggered on pitch = a tracker's arpeggio (`steps: [0, 4, 7]`); on a chip pulse's `duty` or a filter = an instrument macro | |
| pvoc robot `tune` (semitones, modulatable): the robot's note moves per block. Bind to `track.NAME.key` with pitch C4 and a spoken line SINGS another track's melody (the voice can carry an element) | |
| the voice as a standing climb (wM): ask for realism, consonants, breath, vibrato, legato phrasing, harmony stacks, choirs, new characters | |
| the album film's engine (chirp-video; landed 1277462f): `chirp video` with chirp-vis layers: the accretion `disk` (one ring per element/track, debris on onsets, Doppler, photon ring, jets on lifts) and a gravitational `lens`. Ask chirp-video for markers or element-to-ring mappings; prototypes at http://pocket4:8790/ | |
