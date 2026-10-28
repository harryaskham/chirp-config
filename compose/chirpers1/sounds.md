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
| punch kit | metal-kit-punch | chirper-three | metal-kit-dry with a fat snare that holds its body, then drops | candidate; t7 Iron Stairs (v6) | chirper-one (t7) |
| sung lead | m8-lead-f0 (song-local: m8-lead + pitch bound to expr.f0) | chirper-one | the m8 lead played like a guitar: long notes scoop up a semitone into pitch, notes within a fourth slide from the previous held note (^f0 cents paths; generator helper `guitarize` in chirpers1-t7.py) | t7 Iron Stairs lead (v6) | |
| breath gate | juno-pad + a track LFO `{"gt": {"wave": "square", "rate": "5/16"}}` on its gain (+-6 dB) | chirper-zero | a pad chopped by a square gate whose period is the BREATH CELL (5 sixteenths): the chop drifts against the bar and realigns every 5 bars (generator flag T5_GATEF) | t5 Five Breaths, the exhale's return (F) | |
