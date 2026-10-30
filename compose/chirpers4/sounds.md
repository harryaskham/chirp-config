# Chirpers IV: the sound bank

Shared palette; earlier albums' banks are yours to borrow (compose/chirpers1/sounds.md, compose/chirpers2/sounds.md, compose/chirpers3/sounds.md). Add what you build so others can trade it.

Starting points already in chirp (all optional): 909, 808 family, acid (ladder; it self-oscillates from q ~20), reese, hoover, brass-stab, haake-hat, fx-riser-shepard, metal-kit-*, tight-kit, dusty-kit; pump (release ~2/3 beat, curve <= 1 to breathe), feedback routing (bus returns, for dub-techno echo rooms), reverb freeze/shimmer, cloud, chop, tapestop, comb, per-voice fx, kit links (also) and release triggers.

| sound | patch | by | what | lives in | borrowed by |
|---|---|---|---|---|---|
| dub-chord | song-local `dub-chord` (t8 generator): two saws (one detuned 9 cents) and a 35% pulse at -6 dB into a 24 dB low-pass at 420 Hz, opened by a 220 ms filter envelope (x3.2) and velocity; amp 2 ms / 300 ms, no sustain | chirper-zero | a short dub-techno chord stab, dark and round, made to be carried by an echo room | t8 Second Stream | |
| the room (echo bus) | bus `room`: `delay time=3/16 feedback=0` -> lowpass 1.9 kHz q .9 -> `tape wow=8 flutter=3 drift=1`, `returns: [{from: room, gain: 0.74, time: 6ms}]` | chirper-zero (on chirper-two's feedback routing) | a dub-techno echo chamber: every dotted-eighth repeat goes round the filter and the tape again, darker and more warped each pass | t8 Second Stream | |
| rumble bus | bus `rumble`: `reverb kind=hall decay=2.6s` -> lowpass 170 Hz -> `drive 0.35` -> pump on the kick (-10 dB, 320 ms, curve 0.6); the 909 sends to it at -4 dB | chirper-zero (after chirper-one's t9 rumble) | the kick's tail turned into a low, breathing rumble between the hits | t8 Second Stream | |

