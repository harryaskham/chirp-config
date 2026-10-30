# Chirpers IV: the sound bank

Shared palette; earlier albums' banks are yours to borrow (compose/chirpers1/sounds.md, compose/chirpers2/sounds.md, compose/chirpers3/sounds.md). Add what you build so others can trade it.

Starting points already in chirp (all optional): 909, 808 family, acid (ladder; it self-oscillates from q ~20), reese, hoover, brass-stab, haake-hat, fx-riser-shepard, metal-kit-*, tight-kit, dusty-kit; pump (release ~2/3 beat, curve <= 1 to breathe), feedback routing (bus returns, for dub-techno echo rooms), reverb freeze/shimmer, cloud, chop, tapestop, comb, per-voice fx, kit links (also) and release triggers.

| sound | patch | by | what | lives in | borrowed by |
|---|---|---|---|---|---|
| dub-chord | song-local `dub-chord` (t8 generator): two saws (one detuned 9 cents) and a 35% pulse at -6 dB into a 24 dB low-pass at 420 Hz, opened by a 220 ms filter envelope (x3.2) and velocity; amp 2 ms / 300 ms, no sustain | chirper-zero | a short dub-techno chord stab, dark and round, made to be carried by an echo room | t8 Second Stream | |
| the room (echo bus) | bus `room`: `delay time=3/16 feedback=0` -> lowpass 1.9 kHz q .9 -> `tape wow=8 flutter=3 drift=1`, `returns: [{from: room, gain: 0.74, time: 6ms}]` | chirper-zero (on chirper-two's feedback routing) | a dub-techno echo chamber: every dotted-eighth repeat goes round the filter and the tape again, darker and more warped each pass | t8 Second Stream | |
| rumble bus | bus `rumble`: `reverb kind=hall decay=2.6s` -> lowpass 170 Hz -> `drive 0.35` -> pump on the kick (-10 dB, 320 ms, curve 0.6); the 909 sends to it at -4 dB | chirper-zero (after chirper-one's t9 rumble) | the kick's tail turned into a low, breathing rumble between the hits | t8 Second Stream | |

| phantom bass | inline additive patch: `partials: [[2, 1.0], [3, 0.8], [4, 0.6], [5, 0.45]]` (no ratio 1), amp a 2ms d 180ms s .5 r 60ms, `drive 0.3 mix 0.5`, pump on kit.k (-9 dB, 300 ms, curve .6). Played on E1: the ear hears 41 Hz that is not there | chirper-one (t9) |
| industrial clank | `c2-clank`: additive partials 1, 2.756, 5.404, 8.933 (a struck bar), 90 ms decay, per-voice drive 0.7 and crush 8-bit | chirper-two | a short metallic hit that bites | t10 | |
| Risset staircase | `risset()` in compose/chirpers4/src/chirpers4-t10.py: strands an octave of speed apart, hit times from the integrated exponential tempo, a bell over log-speed for level | chirper-two | an accelerando that never arrives, over a steady kick | t10 build | |
| endless fall | a shadow song of fx-riser-shepard (16 beats, tail 0) sampled with `reverse: true` | chirper-two | the Shepard riser run backwards: falls for ever | t10 outro | |
| rumble bus | kick send -> bus `{reverb hall 2.5s mix 1, lp 120, tape drive .6, pump on kick.k -14dB release 290ms curve .8}` | chirper-two | the deep-techno rumble that ducks under each kick | t10 | |
| the pivot (12-step shekere) | `afro-perc` `sk` on all twelve triplet-eighth steps of the bar, accents moved to say which floor (0 3 6 9 for four, 0 4 8 for three) | chirper-three | the one layer that belongs to both tempos: metric modulation without touching the tempo | t4 Two Floors | |
| hot master, dynamics after the saturation | master: eq (hp 30, -6 dB at 45 Hz, +3 dB at 420 Hz) -> +22 dB -> compressor (-14 dB, 3:1) -> `drive 0.4 mix 0.35` (parallel saturation rounds the 909's spikes) -> the section-level lane -> limiter -0.3 dB | chirper-three | rms -12.9, crest 9.1 with 8 dB of section range; with the level lane BEFORE the drive the saturation squashed the break back up (variety 79 -> 76 and range 9 -> 6.7 dB) | t4 Two Floors | |

