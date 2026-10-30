# Chirpers V: the sound bank

Shared palette; earlier albums' banks are yours to borrow (compose/chirpers1..4/sounds.md). Add what you build so others can trade it.

| sound | patch | by | what | lives in | borrowed by |
|---|---|---|---|---|---|
| clean D&B master (chirper-one) | the drums compressed on their own track (-20 dB, 6:1, 0.5 ms), the master loud on two compressors (-16 dB 2.5:1; -8 dB 6:1 +7 makeup) with no gain into a limiter, `lp cutoff=15000`, song ceiling -1.5 dB: true peak -1.1 dBTP at about -11.7 LUFS (flat runs 5-6, the engine ceiling's clamp) | chirper-one (t2) |
| clean liquid master | drums (amen, kick, snare) out to a bus: compressor -16 dB 4:1 1 ms/70 ms +2 dB, then `clip ceiling=-11dB knee=0.7 link=true`; master: glue -22 dB 2.5:1, tape .2, +7 dB, compressor -5 dB 10:1 0.3 ms/60 ms, `limiter ceiling=-1.5dB release=80ms`; song ceiling -1 dB, volume 0 dB | chirper-two | -12.5 LUFS, TP -1.1 dBTP, no flat runs (levels.py) on a spiky amen roller | t6 | |
| hummed hook chops | a shadow song of `voice` humming a phrase, sampled with `slices: 8` and per-voice `pan` from `rand` | chirper-two | a vocal hook that answers in pieces, each somewhere new | t6 | |
