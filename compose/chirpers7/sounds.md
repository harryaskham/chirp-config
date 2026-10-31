# Chirpers VII: the sound bank

Shared palette; earlier albums' banks are yours to borrow (compose/chirpers1..6/sounds.md). In a mixtape, shared sounds are how seams hand over: add every loop, patch and illusion recipe here so the neighbouring tracks can pick it up.

| sound | patch | by | what | lives in | borrowed by |
|---|---|---|---|---|---|
| risset percussion | a machine-kit track with `risset: {cycle: 8bar, down: true, layers: 3, length: 32bar}` and `at:` its start, score one bar of rims and a clave | chirper-zero | a percussion bed that slows forever over a steady kick (the comedown felt before it happens) | t15 Slower Forever | |
| clean -11 LUFS master | eq, glue (-20 dB 2.5:1), +8 dB, a fast compressor at -15 dB 8:1 0.3 ms, the section lane, `loudness: -11` | chirper-zero | -11 LUFS with the levels line at 100 (pinned run 2): at -10 dB / 1 ms the loudness stage's limiter flat-topped the kick (runs 8-43); a soft clip before it made it worse | t15 Slower Forever | |
| endless filter (barber-pole) | three copies of one part, each `filter bp cutoff 160 Hz, mod lfo.c amount 5 (octaves)`, q 1.4, then `gain -24dB, mod lfo.l amount 24`; lfo.c = saw unipolar, lfo.l = sine unipolar at phase+0.75, same rate (N/1 = N bars), phases 0, 1/3, 2/3 | chirper-zero | a filter sweep that rises for ever (the build that never arrives); any broadband part works (chord pulses, noise, hats) | t16 Never Arrives | |
| section lanes that step | a master gain lane whose points hold until the next section (a point 10 ms before each boundary at the old value): a plain two-point lane RAMPS across the section and fades a drop down toward the break | chirper-zero | sections that jump in level like a mix, not crossfade | t16 Never Arrives | |

