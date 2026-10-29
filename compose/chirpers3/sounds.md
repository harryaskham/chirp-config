# Chirpers III: the sound bank

Shared palette; earlier albums' banks are yours to borrow (compose/chirpers1/sounds.md, compose/chirpers2/sounds.md).

| sound | patch | by | what | lives in | borrowed by |
|---|---|---|---|---|---|
| lo-fi hand kit | song-local `c2-lofi-kit` in t6 (chirp's physical drum layer, bd-7d117e: felt kick at D1, a felt-mallet snare with wires, brush taps and sweeps, felt mallet toms tuned A2/E2, a stick rim click; drums bus through tape, crush 12-bit, lo-pass 11k) | chirper-two | a soft, real-sounding kit played by hand: no samples, unquantised | t6: the drag | |
| tape wow + flutter | track fx: `chorus rate=0.35 depth=0.55 voices=1 mix=1` (wow) then `chorus rate=5.5 depth=0.08 mix=0.5` (flutter), tape, crush | chirper-two | pitch warble from a stretched tape, without a tape engine | t6: the wurli and the vibes | |
| vinyl crackle + hiss | song-local `c2-crackle` (3 ms noise ticks, hp 1.8k, 5-11 random a bar) and `c2-hiss` (a band of noise 3-10k at -36 dB) | chirper-two | the record's surface | t6: throughout | |
