# Chirpers VI: the sound bank

Shared palette; earlier albums' banks are yours to borrow (compose/chirpers1..5/sounds.md). Add speech voices and sound-effect recipes here so others can trade them.

| sound | patch | by | what | lives in | borrowed by |
|---|---|---|---|---|---|
| rail-rumble | song-local (t3): brown noise low-passed at 160 Hz (q 0.8), 6 s attack and release | chirper-zero | a freight train's rumble passing at night: hold one long note across the crossing | t3 Night Freight | |
| wheel-clack | song-local (t3): white noise band-passed at 1.6 kHz with sines at 820 and 1370 Hz, 70 ms decay | chirper-zero | wheels over a rail joint; play clack-clack pairs on a 14-sixteenth cycle (C4 the front axle, D4 the rear) | t3 Night Freight | |
| freight horn | brass-synth, three tones (F#4 A4 C#5) low-passed at 2.2 kHz into a 6 s yard hall; the passing doppler as the same chord a semitone down | chirper-zero | a train horn at a level crossing | t3 Night Freight | |
| radio voice | `voice-speech` with `^ph=` ARPAbet syllables (a beat each, ^f0 contours falling at line ends) through hp 320, lp 3.2k, crush 10-bit 11 kHz, drive, a small room; a second take via `{type: pitch, semitones: -3, formant: -3}` | chirper-two | a shortwave announcer, intelligible | t1 | |
| wind | pink noise through a band-pass whose centre rides two track LFOs (7 bars and 1 bar), slow attack | chirper-two | moving wind across a plain | t1 | |
| shortwave static + whistle | 4 ms band-passed noise ticks; a sine whose pitch glides on a slow envelope (the dial) | chirper-two | a radio being tuned | t1 | |
| fader ride | a master `gain` bound to an `auto.dyn` lane per movement (brushes -6 dB, the climb from -9 dB up to the peak) | chirper-two | an earned dynamic arc on a true-peak master | t1 | |
