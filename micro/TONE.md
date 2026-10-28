# Tone push: DI, amps, cabs and drums (from 28 Oct)

Harry, 28 Oct: "focus on getting the DI and amps/cabs/IR sounding really sick, and much punchier realistic drums:
different articulations, string DI sim strategies, amp modelling techniques; go super deep, better sounds on existing
songs."

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

## Rules

Everything in micro/README.md's rules applies:
- climb the library, not the clip;
- holdouts;
- no global regressions;
- record every attempt;
- ears decide;
- engine gaps become beads.

Engine work is opt-in and default-identical: chirp-eco checks byte-identical renders before adopting a pin.

Composition mode is paused for this push. Ferrous Bloom keeps playing in the groove as a listening test bed, and
library gains reach it through the shared patches.
