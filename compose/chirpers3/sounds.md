# Chirpers III: the sound bank

Shared palette; earlier albums' banks are yours to borrow (compose/chirpers1/sounds.md, compose/chirpers2/sounds.md).

| sound | patch | by | what | lives in | borrowed by |
|---|---|---|---|---|---|
| lo-fi hand kit | song-local `c2-lofi-kit` in t6 (chirp's physical drum layer, bd-7d117e: felt kick at D1, a felt-mallet snare with wires, brush taps and sweeps, felt mallet toms tuned A2/E2, a stick rim click; drums bus through tape, crush 12-bit, lo-pass 11k) | chirper-two | a soft, real-sounding kit played by hand: no samples, unquantised | t6: the drag | |
| tape wow + flutter | track fx: `chorus rate=0.35 depth=0.55 voices=1 mix=1` (wow) then `chorus rate=5.5 depth=0.08 mix=0.5` (flutter), tape, crush | chirper-two | pitch warble from a stretched tape, without a tape engine | t6: the wurli and the vibes | |
| vinyl crackle + hiss | song-local `c2-crackle` (3 ms noise ticks, hp 1.8k, 5-11 random a bar) and `c2-hiss` (a band of noise 3-10k at -36 dB) | chirper-two | the record's surface | t6: throughout | |
| granular wow | track fx `{"type": "pitch", "semitones": {"value": 0, "mod": [{"src": "lfo.wow", "amount": 0.12}]}, "mix": 1}` with track lfo `wow: "sine rate=0.37hz"` | chirper-zero | tape wow through the granular pitch shifter: a slow +-0.12-semitone sway with a faint grain, on the keys and the lead | t5 Low Pressure | |
| dub echo throws | a feedback tape echo bus (`delay time=3/16 feedback=0.62 tone=1600`) and a spring bus; each track's echo send is `{"value": "-14dB", "mod": [{"src": "auto.thr", "amount": 1}]}` with an auto lane `thr` that jumps +14 dB for half a second on the last off-beat of every phrase | chirper-zero | the dub engineer's hand on the send: phrase ends thrown into the echo, the repeats running on a dotted eighth | t5 Low Pressure | |
