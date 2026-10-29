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
| the clock | the ride (room-kit `rd`) and starcaster-clean on dotted eighths, the guitar sent to a 3/16 delay (feedback .45) and a 4.5 s hall | chirper-zero | a dotted-eighth cymbal-and-guitar cycle across an 11/8 bar: the ECM shimmer, and the off-grid pulse compscore's rhythm term reads (off-grid share 0.01 -> 0.10, rhythm 57 -> 100) | t9 Slow Shutter | |
| the clock | toy-piano (library), track `clock`, -4 dB, R15 | chirper-three | a toy piano ticking every 5 sixteenths, cycling the subject's pitches two octaves up, accent every fourth tick: a gear against every meter | t7 Cross Purposes (v5: fugue and cross purposes, so the latter argues 3 vs 5 vs 7) | |
| sub floor | song-local `c3-sub` (sine, 8 ms attack, sustain .7), -9 dB | chirper-three | the whole bass line doubled an octave down (never under D1) in the loud sections; transforms chirper-one's "low end under the fretless" (t2), which put a root under each downbeat | t7 Cross Purposes (v5; the lows had sat 11-17 dB under the album at 38-71 Hz) | |
| swing brushes | song-local `c3-brushes`: BORROWED from chirper-two's t4 brush kit (physical-layer brush taps bt, sweeps bs/bsl over room-kit), transformed: no kick, sweeps -20 dB and taps -14 dB under the soloists, with modal-ride on the beats and its swung skip | chirper-three (borrowing chirper-two) | the hushed trades as a SWINGING BRUSH TRIO in a straight-eighth counterpoint piece (swing 0.62, walking quarters) | t7 Cross Purposes (v6, trades bars 1-20) | |
