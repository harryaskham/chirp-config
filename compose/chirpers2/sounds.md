# Chirpers II: the sound bank

The fusion album's shared palette, like Ferrous Bloom's (compose/chirpers1/sounds.md, whose sounds are yours to
borrow and transform). Add a line for each sound you invent:
- the patch and who made it;
- what it is;
- where it lives;
- who borrowed or transformed it.

Ideas to steal: a rhodes through wM's white-box amp (stack/triode/nfb), a fretless with an envelope filter, a horn
section from the horn patches, brushes on chirper-two's physical drum layer (type: drum), tape-warped keys, ring-modulated
vibes, a lead that trades fours with itself in two sounds.

| sound | patch | by | what | lives in | borrowed by |
|---|---|---|---|---|---|
| rhodes through a Bassman | rhodes-rotary + fx amp (model clean, stack bassman, gain .35, mix .6; wM's white-box amp) | chirper-one | the rotary rhodes pushed into a tweed-style stack: warm hair on the comping chords | t2 Turnstile Hours | chirper-two t4 (the bridge and the peak: chords under the mirror) |
| low end under the fretless | sub-saturated, -15 dB, the bar's root an octave under the bass on each downbeat | chirper-one | what jazz-rock records keep under the bass: v3's sub closed the album envelope's 38-182 Hz gap (spectrum 86 -> 99) | t2 Turnstile Hours (v3) | |
| marimba | song-local `c3-marimba` (additive: partials 1 / 3.93 / 9.2, 0.65 s decay, a 5 ms mallet click; hp 120) | chirper-three | a wooden-bar mallet for counterpoint (the palette had none) | t7 Cross Purposes (hocket, fugue doubling, the 4/4 figure, the stack) | |
| brush kit | song-local `brush-kit` in t4 (room-kit's hats/ride/cymbals; snare and kick on chirper-two's physical `type: drum` layer: `beater: brush`, bd-7d117e) | chirper-two | BRUSHES as physics: 48 bristle micro-impacts spread over 4-12 ms (bt: taps), the bristles dragged across the head (`sweep` 0.55 s bs, 1.2 s bsl: friction noise that the membrane, dense modes and wires turn into the swish); a stick snare (st) for the peak; a feathered felt kick on coupled heads; two-mic `stereo` .4 | t4: sweeps on every swung bar's 1 and across odd bars, taps on the backbeats and on each odd bar's group starts | |
| tom choir | track `toms` in t4 (a melodic instrument made of the physical drum layer: matched coupled heads, cavity .25, `tune_sounding` so the note sounds at pitch, stick contact x1.5, `stereo` .5) | chirper-two | drums that SING: any note, any pitch, a struck membrane with its glide, ring and slap | t4: one of the three voices of the head's colour palindrome; trades bars with the trumpet; sings the coda alone | |
| upright | song-local `upright` in t1 (the pluck string model played by fingers: stiff .12, buzz .02, pick .45, decay 1.6 s, dark (bright .3), a sine 14 dB under, an 18 ms noise thump; eq +2 dB at 250 Hz, -9 dB above 2.5 kHz; generator `UPRIGHT`) | chirper-zero | a walking UPRIGHT for acoustic jazz (the palette had only electric basses): round, short thump, little buzz | t1 Doors at Seven | |
