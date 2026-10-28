# Ferrous Bloom: the sound bank

Harry, 28 Oct: Ferrous Bloom is where the chirpers try out mad new guitar (and drum) sounds. Go crazy composing
against fun combinations:
- trade sounds back and forth;
- give different parts different rhythmic patterns.

This file is the album's shared palette, like the motif bank.

**How to add a sound**: make it a patch (song-local while you experiment; `patches/fb-NAME.yaml` once it is good
enough for others), then add a line here.
- the name and the patch;
- who made it and what it is (the chain, the trick);
- where it lives (track and section);
- who borrowed or transformed it.

Borrow freely, and say so here when you transform someone else's sound.

**Ideas to steal** (not rules):
- **Rigs**:
  - extreme amp voicings and gain staging, fuzz, octave-up/down, ring modulation;
  - wavetable or FM layers on the pluck, filter sweeps and LFOs;
  - rhythmic gating, stutter and glitch, pitch-shifted doubles and harmonies;
  - feedback or e-bow-like sustain, baritone or detuned doubles, clean/fuzz hybrids.
- **Trading**:
  - call and response between two contrasting rigs (left/right, or section by section);
  - hocketing: one riff's notes split across two sounds;
  - a sound swap mid-riff;
  - one track's sound answering another track's motif.
- **Rhythm**:
  - each part in its own cycle (guitar 7, bass 9, kit 4/4);
  - a gate or LFO pattern in a different cycle from the notes it chops;
  - the same riff in two sounds offset by a sixteenth.
- **Drums**: kits with character, not only realism: chirper-three's metal-kit-punch (a fat snare that holds its
  body, then drops), and chirper-two's physical-model drums as they land.

The realism yardstick (drumpunch/riffpunch/microscore against the records) is there when you want a sound to be real.
Here, invention counts as much as realism.

## Sounds

| sound | patch | by | what | lives in | borrowed by |
|---|---|---|---|---|---|
| m8 rig | m8-emg-l / m8-emg-r | library | active-pickup 8-string into a 5150, Jester cab blend | every track | everyone |
| punch kit | metal-kit-punch | chirper-three | metal-kit-dry with a fat snare that holds its body, then drops | t2 Ingot (v6), t7 Iron Stairs (v6), t8 The Long Unwinding (v9). Realism vs the records' drum stems (drumpunch): the-abysmal-eye 62.6 -> 81.4 (untuned), the-faultless 61.7 -> 73.7 | chirper-one (t7, t8) |
| sung lead | m8-lead-f0 (song-local: m8-lead + pitch bound to expr.f0) | chirper-one | the m8 lead played like a guitar: long notes scoop up a semitone into pitch, notes within a fourth slide from the previous held note (^f0 cents paths; generator helper `guitarize` in chirpers1-t7.py) | t7 Iron Stairs lead (v6); t8 The Long Unwinding's climb/crush leads (v9) | |
| breath gate | juno-pad + a track LFO `{"gt": {"wave": "square", "rate": "5/16"}}` on its gain (+-6 dB) | chirper-zero | a pad chopped by a square gate whose period is the BREATH CELL (5 sixteenths): the chop drifts against the bar and realigns every 5 bars (generator flag T5_GATEF) | t5 Five Breaths, the exhale's return (F) | chirper-one (t8 The Long Unwinding v11: the dissolve's pad, where t5's BREATH CELL returns) |
| shard | m8-emg-r + track fx `{"type": "crush", "bits": 6, "rate": 5000, "mix": 0.6}` (song-local) | chirper-three | the m8 chain, bit-crushed and centred: HINGE's hocket partner. Each 3+3+3+3+4 bar alternates wide m8 pair -> centred shard -> wide -> shard -> wide, then the tritone stab (generator: `hinge()` tags groups 2 and 4 "shard") | t2 Ingot HINGE (v7, bars 37-52) |chirper-zero: t6 Thirteen Teeth v6, the GEAR HOCKET (GEARTRAIN split: m8 accents/stabs left, the chugs as SHARD hard right) in mesh and governor; chirper-one (t7 Iron Stairs v8: the CHURN's light chugs hocketed onto it in the A and B steps) |
| sub-crush | track `fuzz` (m8-emg-r + fx pitch -12 mix .6, crush 8-bit mix .25) | chirper-one | the m8 rig an octave down and bit-crushed: a sub-floor under the half-time blocks | t8 crush, second half (bars 145-152); t7 Iron Stairs' F landings and reprise | chirper-one (t7) |
| ring stab | track `ring` (m8-emg-l + fx ring 233 Hz mix .6) | chirper-one | only the 11-cell's tritone stabs, ring-modulated and panned right: hocketed against the pair's chugs | t8 climb (bars 105-136) | |
| halo | track `halo` (m8-clean + fx freeze hold 1 size .8 mix .5, pitch +12 mix .25) | chirper-one | e-bow-like frozen sustain with an octave shimmer: LATTICE's line in long notes over the breath cell | t8 dissolve (bars 153-172) | |
| fifth-up harmony | track `harm` (m8-lead-f0, the lead's line +7 semitones) | chirper-one | the sung lead doubled a fifth above at the climax and the reprise, panned against the lead | t7 Iron Stairs (bars 71-90) | |
| 5-gate pad | juno-pad + fx tremolo depth .6 at 1.49 Hz | chirper-one | the pad chopped every 5 sixteenths at 112 bpm (half the CHURN's 10), a gate cycle against the riff | t7 Iron Stairs (intro, breakdown, outro) | |
| felt toms | song-local kit `seed-toms` (metal-kit-dry with `ft`/`t3` rebuilt on the physical `type: drum` layer, bd-7d117e; generator helper `felt_tom`) | chirper-three | felt-mallet membrane toms TUNED to LATTICE's poles: floor tom F2, high tom B2 (the tritone). Light head/cavity coupling (reso_level .1, cavity .1) so the drum sounds at its note (at .5/.4 the strongest partial sits 1.33x above it); +12 dB piece gain (felt is soft) | t1 Seed Crystal (v6), the distant percussion of B, C and the seed's return | |
| ring glass | pad-glass + track fx `{"type": "ring", "freq": 233, "mix": 0.6}` | chirper-zero (the ring setting borrowed from chirper-one's t8) | the glass pad's held B3-E4-B4 chord ring-modulated at 233 Hz: a metallic, unstable breath before the weight lands | t5 Five Breaths, the held breath (D) | |
| machine tools | m8-chug-l/r, m8-fluence-l/r, m8-fuzz (library rigs, swapped per section) | chirper-zero | the same GEARTRAIN riff handed to a different rig in each 13-bar section: the hard chug rig (engage), airy Fluence for the governor's open octaves (beside SHARD), woolly fuzz for the 23-cycle overdrive; m8-emg returns for mesh and the seizure | t6 Thirteen Teeth v7 | |
| sub swell | song-local `seed-sub` (sine F1 + a -14 dB octave, amp attack 2.6 s, full sustain) | chirper-three | a riser made of the NEXT song's floor: a pure F1 fades in across Seed Crystal's held cluster and peaks as Ingot's first kick and F1 bass land. Filled the join's 38 Hz hole (was -24 dB): spectral 8.6 -> 7.6 dB | t1 Seed Crystal (v7, the HOLD bar 42) | |
