# Chirpers VI: the sound bank

Shared palette; earlier albums' banks are yours to borrow (compose/chirpers1..5/sounds.md). Add speech voices and sound-effect recipes here so others can trade them.

| sound | patch | by | what | lives in | borrowed by |
|---|---|---|---|---|---|
| rail-rumble | song-local (t3): brown noise low-passed at 160 Hz (q 0.8), 6 s attack and release | chirper-zero | a freight train's rumble passing at night: hold one long note across the crossing | t3 Night Freight v1 (v2 moved to the port) | |
| wheel-clack | song-local (t3): white noise band-passed at 1.6 kHz with sines at 820 and 1370 Hz, 70 ms decay | chirper-zero | wheels over a rail joint; play clack-clack pairs on a 14-sixteenth cycle (C4 the front axle, D4 the rear) | t3 Night Freight v1 (v2 moved to the port) | |
| freight horn | brass-synth, three tones (F#4 A4 C#5) low-passed at 2.2 kHz into a 6 s yard hall; the passing doppler as the same chord a semitone down | chirper-zero | a train horn at a level crossing | t3 Night Freight v1 (v2 moved to the port) | |
| radio voice | `voice-speech` with `^ph=` ARPAbet syllables (a beat each, ^f0 contours falling at line ends) through hp 320, lp 3.2k, crush 10-bit 11 kHz, drive, a small room; a second take via `{type: pitch, semitones: -3, formant: -3}` | chirper-two | a shortwave announcer, intelligible | t1 | |
| wind | pink noise through a band-pass whose centre rides two track LFOs (7 bars and 1 bar), slow attack | chirper-two | moving wind across a plain | t1 | |
| shortwave static + whistle | 4 ms band-passed noise ticks; a sine whose pitch glides on a slow envelope (the dial) | chirper-two | a radio being tuned | t1 | |
| fader ride | a master `gain` bound to an `auto.dyn` lane per movement (brushes -6 dB, the climb from -9 dB up to the peak) | chirper-two | an earned dynamic arc on a true-peak master | t1 | |
| crane-chain | song-local (t3 v2): white noise band-passed at 1.2 kHz with sines at 560 and 1040 Hz, 90 ms decay | chirper-zero | a gantry crane's chain link over its sheave; clank-clank pairs on a 14-sixteenth cycle | t3 Night Freight | |
| ship-engine | song-local (t3 v2): brown noise low-passed at 130 Hz plus a 46 Hz sine, 6 s attack/release, tremolo 2.7 Hz depth 0.45 on the track | chirper-zero | a ship's diesel throbbing at the quay | t3 Night Freight | |
| buoy bell | bell (FM) at B4 / A#4, struck at irregular gaps (9, 7, 11, 6, 10, 8, 12 sixteenths) into a 6 s hall | chirper-zero | a buoy rocking on the swell | t3 Night Freight | |
| foghorn | brass-synth B1+F#2 held three 7/8 bars, low-passed at 900 Hz, into a 6 s hall | chirper-zero | a ship's horn in the harbour | t3 Night Freight | |
| air-hiss / reverse-beep | song-local (t3 v2): white noise band-passed at 4 kHz, 0.9 s decay / a 1160 Hz sine gated in quarter notes, far down in a 6 s hall | chirper-zero | air brakes releasing; a straddle carrier reversing across the yard | t3 Night Freight | |
| walkie-talkie voice | voice-speech (ARPAbet syllables, an eighth each, the last falling ^f0=0>-60) through hp 400 Hz, lp 3.2 kHz and drive 0.45 | chirper-zero | a crane operator on a handheld intercom - a close, small voice, not a broadcast radio | t3 Night Freight | |
| dawn birds | `c2-bird`: a sine (and its octave) whose pitch flicks up 7 st over 15 ms then falls (env), a 28 Hz vibrato LFO, 90 ms; random notes D6-B6, scattered | chirper-two | synthesised birdsong | t8 | |
| dawn kit (physical) | `c2-dawn-kit`: chirp's drum layer with brush taps/sweeps, felt mallet snare and toms, a stick snare with wires, rimshots, a felt kick and a plastic-beater kick: one kit's whole arc | chirper-two | brushes to full kit without changing kits | t8 | |
| radio switch-off | `c2-click`: a 25 ms noise click and a 90 Hz thump | chirper-two | the end of the broadcast | t8 | |
