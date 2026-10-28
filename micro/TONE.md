# Tone push: DI, amps, cabs and drums (from 28 Oct)

Harry, 28 Oct: "focus on getting the DI and amps/cabs/IR sounding really sick, and much punchier realistic drums:
different articulations, string DI sim strategies, amp modelling techniques; go super deep, better sounds on existing
songs."

**What it is for (Harry, 28 Oct, 16:5x):** the tone push serves **the chirpers' own album, Ferrous Bloom**. Better
guitar and drum sound means better original songs. Composition climbing stays ON, and each composer brings the new
sounds into their own tracks.

- **The records** (and their stems) are a realism yardstick only: drumpunch/riffpunch/microscore say whether a
  snare or amp sounds like a real one.
- **Old reproduction albums** are checked only when a shared library default changes (chirp-eco's crossclimb),
  so the new sounds cannot quietly break them.
- **New sounds go in as named patches** (e.g. metal-kit-punch) that Ferrous Bloom tracks adopt by A/B: compscore on
  seeds 0/11, plus Harry's ears.
- **Ferrous Bloom is the sound playground** (Harry): invent mad new guitar sounds and compose against them. Trade
  sounds back and forth, give parts different rhythmic patterns, try fun combinations. Realism is one option, not the
  goal. The album's shared palette is `compose/chirpers1/sounds.md`.

## Constraints (Harry)

- **Synthesis only.** Samples and record stems are for comparison and measurement, never in a patch.
- **Neural/NAM-style modelling only if it compiles into the engine** (weights in the patch, CPU-cheap). We have no
  paired DI/amp captures, so learned parts are fitted offline against record stems (bd-95f4e2, exploratory).
- chirp stays CPU-only. Offline fitting tools may use the GPU.

## Where we start

- **Guitar chain**:
  - pluck string: pick position, stiffness, vary, click/scrape/thump/squeak, contact grain;
  - pickup position and coil resonance; sympathetic strings; compressor;
  - `amp`: n tanh stages with coupling HP and Miller LP, 4x oversampling + ADAA, a 3-filter tone approximation, one
    tanh power stage with sag/bloom, presence/resonance as fixed shelves;
  - `ir`: the Jester IR blends, speaker breakup, room; then EQ, gate, plate.
- **Drums**: drum-machine style synthesis (patches/metal-kit: a sine body with a pitch envelope, noise click/wires,
  additive partials), with a kit bus (compressor, drive, EQ, room).

## Streams

| stream | who | what |
|---|---|---|
| amp, white-box | wM | bd-b1f325: TMB tone stack (Yeh), triode stages, NFB power amp into a speaker load |
| guitar DI | wM, after the amp | bd-dfbe0c: two-polarisation string, pick contact/slip, palm-mute point, pickup nonlinearity |
| drums, physical model | chirper-two | bd-7d117e: membrane modes, stick contact, coupled heads, wire buzz |
| drum sound design | chirper-three | the micro drums family with today's engine (layers, kit bus: parallel compression, transient shaping, room), then canary for bd-7d117e |
| guitar rig sound design | chirper-zero | the riff family with today's engine (pickup/coil, amp voicing, IR blends, breakup, doubles), then the new amp/DI |
| articulations | chirper-one | bd-90c9d2: bends, vibrato, slides, legato, harmonics, chokes, dead notes; tab2song mapping; obZen/Immutable songs |
| measurement, gates, listening | chirp-eco | drumpunch.py (per-hit punch vs stems), tonefit.py (parameter fitting), byte-identity + crossclimb gates, A/B sets for Harry |

## Measuring

- **Micro clips** (`micro/clips.json`; `tools/microscore.py --clip ID --context all --set …`): the riff family
  (stem-referenced metal guitar), drums, guitar and bass. About a third are holdouts: never tune on them.
- **Drum punch** (`tools/drumpunch.py`, chirp-eco): per-hit attack, peak-to-body and spectral balance of kick, snare
  and toms against the record's drum stem.
- **Full songs**: library changes are crossclimbed across every song that uses them (chirp-eco).
- **Ears decide**: before calling a stream better, queue a reference/before/after set for Harry
  (`chirp live queue FILE --id groove --label NAME`, never over the groove).

## Findings

**28 Oct, drumpunch baseline (chirp-eco).** `tools/drumpunch.py --song ID --from A --to B` measures clean kick and
snare hits from our own score, paired with the same moments on the record's drum stem.

The separator noise floor (BS-Roformer against htdemucs on one song) scores **79-91** (kicks 94-98, snares 64-87).
Our kits score **42-57**, so the gap is real. The same diagnosis holds on three songs:

| piece | ours | record |
|---|---|---|
| snare decay to -20 dB (Bleed / Pineal) | 140 / 141 ms | 22 / 65 ms |
| snare body (150-300 Hz) vs crack (1.5-5 kHz) | about -14 dB | about -3 dB |
| snare rise | 11.5-12.5 ms | 4-5 ms |
| kick rise (Pineal) | 11.5 ms | 4.5 ms |

- **The snare** rings far too long (it rings out where the record's is tight), is thin (lacks body against its
  crack) and attacks too softly.
- **The kick attack** is soft on Pineal.

That is the drum-machine sound: a real snare is fat, fast and tight.

**28 Oct, riffpunch baseline (chirp-eco).** `tools/riffpunch.py --song ID --from A --to B` measures our clean
guitar onsets against the record's guitar stem. Over 30 s each of Bleed, The Faultless and Pineal, ours scores
41-46, against a separator floor of 67-86.

- **Grain** (spectral flatness of 1-4 kHz in the sustain) is the robust, large gap: ours **0.13-0.22**, the records
  **0.34-0.41**. The two separators agree within 0.02. Our distorted guitars lack the noise between their harmonics,
  the synth-guitar tell. Levers: contact grain and pick scrape, string/pickup nonlinearity (bd-dfbe0c), and amp-stage
  intermodulation (bd-b1f325).
- **Mid scoop** (400 Hz-1 kHz vs 1-4 kHz) is not deep enough: ours -2 to -5.5 dB, the records -6 to -12 dB; the
  separators agree within ~1 dB. This is the tone stack's job (bd-b1f325's TMB stack).
- **Fizz** (6-10 kHz vs 1-4 kHz) is rig-specific: The Faultless and Pineal rigs have **+13 dB** too much, Bleed
  -6 dB too little. Judge fizz against bs_roformer refs only: htdemucs loses 3-11 dB up there.
- ~~Timing scatter explains the riff transients~~ **RETRACTED** (chirper-one): per-note attack peaks are not
  resolvable in a sustained-distortion stem. A random pick in the +-30 ms window gives IQR 30 ms and 67% off by
  >10 ms, which is exactly what we read, and the global lag search wandered to -100 ms on aligned songs (now capped
  at +-20 ms). The tone findings above hold after the fix (re-measured at shared moments). The riff family's low
  microscore transients remain unexplained: an onset-correlation is fragile on dense distortion too.

**28 Oct, metal-kit-punch r2 as metal-kit-dry's default: NOT adopted (chirp-eco crossclimb, --refit-width).**
Over 18 songs (Pravus failed on the full disk): mean -0.03, sum -0.51.
- **obZen gains**: Combustion +0.60, Pineal +0.63, obZen +0.21, Snake +0.16, Electric Red +0.14, Dancers +0.04.
- **Immutable loses**: -0.10..-0.45 on all ten with a change, apart from Kaleidoscope (+0.17).

The fat, gated snare suits obZen's production and not Immutable's. It stays a named kit:
- Ferrous Bloom uses it by A/B (Ingot, Iron Stairs, The Long Unwinding);
- obZen owners may adopt it per song when obZen resumes.

## Rules

Everything in micro/README.md's rules applies:
- climb the library, not the clip;
- holdouts;
- no global regressions;
- record every attempt;
- ears decide;
- engine gaps become beads.

Engine work is opt-in and default-identical: chirp-eco checks byte-identical renders before adopting a pin.

Composition mode is ON. The point is a better-sounding Ferrous Bloom: put the new kits, rigs and articulations
into your album tracks, and A/B them there.

**28 Oct, articulations, first pass (chirper-one, bd-90c9d2).**

- **What the engine already gives.** The m8 family's built-in pitch takes `env.bite`, `rand` and a delayed `lfo.vib`. Held notes grow vibrato after 380 ms at 0.2 depth, tab or no tab. With wM's expression paths (bd-8d7ab2), binding `expr.f0` (amount 0.01) adds per-note pitch curves in cents. A chord bends as one: its widest curve.
- **Mapping in `tools/songsterr.py`.**
  - New opt-in bend mode, `--bends path` (tab2song part key `"bends": "path"`, f29115d6). A bent note's curve becomes a per-note `^f0=a>b>…` in cents. Slides do too: in, from -2 semitones over 1/8 beat; out, -2 then -5 over the last 1/4.
  - This replaces the track-wide `bend=` events, which moved every sounding note in the track. That is why the obZen maps strip them.
  - Default output (peak/curve/mean) is byte-identical on Lethargica's and Pravus's tabs.
  - The m8 patches need the binding: a song-local `extends` with pitch.mod = bite .15, rand .05, lfo.vib .2, expr.f0 .01 (the built-in list plus one).
  - Palm mutes (`^pm`), dead notes (`^dead`), pinch harmonics (`^ph`), natural harmonics (`^nh=N`) and hammer-ons (`^h`, opt-in "articulations": ["hp"]) were already carried.
- **A/B, Lethargica v12** (slides only; its tab has no lead bends). Bends and slides as paths on the rhythm pair: 69.27/68.95 vs 69.27/68.98. With the bass too: 69.21/68.98. Rhythm-pair vibrato off: 69.25/68.99; at 0.1: 69.24/68.95. All flat.
- **How few bends obZen has.** Path notes per tab track: Pravus 4; Pineal 18/18 on the rhythm pair, 4 on the lead, 10 on the bass; Snake 10/10, bass 27; Dancers 19/32, solo 6, bass 19. Whole-song scores cannot see them. The riff clips (microscore/riffpunch) and ears must judge.
- **Timing scatter** (riffpunch, Pineal 60-90 s). The record vs ours has an IQR of 38 ms (74% off by >10 ms). With the rhythm pair's strum and humanise at 0 it is 36.5 ms (71%). So the scatter is not our humanise. It is the record's own timing against the tab grid: drift or feel, wM's warp territory.
- **28 Oct (chirper-one): riffpunch timing is unmeasurable on sustained distortion.** On Pineal 60-90 s the global lag reads -100 ms, though the song is map-aligned and should read ~0. With shift 0: offset median -13 ms, IQR 30.8 ms, 64% off by >10 ms. A peak picked at random in the +-30 ms search window gives IQR 30 ms and 67%. Read riffpunch's timing against that random baseline; the attack peaks of a distorted guitar stem aren't resolvable per note. Dancers' bend paths (the riff's A2 bend, bars 3-36 and 166-242) are flat whole-song (65.73 path / 65.71 bend= vs 65.75 unbent) and on microscore over bars 3-9 vs the SW guitar stem (42.98 / 43.38 vs 43.28).
