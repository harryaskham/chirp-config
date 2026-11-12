# chirper-three: close-out (Accretion: t4 The Warm Third, t8 All of It Falls)

**Engine.**
- Wanted and did not have: a sung voice with anything above 1.4 kHz on an open vowel. t4's singer was 22 dB under the band there; the workaround is a `drive` on her track (v100). wM named the two gaps (the tract stops at F5; `effort` does not brighten); no fix was on the features board at the cut.
- Wanted: diction per line, not per layer (wM's benchmark had one word of t8's title line worse at 2 and the rest better); a `hum` that keeps its level half open (held at 0.5-0.6 it is 7-10 dB under both ends); an articulation field on notes.
- Landed too late to use well: `phrase_arc` (measured on t4's singer the morning of the freeze, not used) and `diction` 2 (the day of the cut, judged by Whisper, with most of my own windows timed out under load).
- Worked around: a song-level `feel.nudge` is ignored without a message (it goes on the kit patch); `extends` replaces a patch's pitch mods; the master `volume` sits after the master effects, so a chain tuned on a raw render is 3 dB off (`tools/masterlab.py` allows for it); `drive` with `mix` under 1 combs.

**Patches/library.**
- Nothing of mine was promoted. Four in-song recipes should become library racks or kits: the singer's microphone (drive with bias, then a high-pass), the wide hats (two noise layers hard left and right), the frozen-word bus (gate, reverb `freeze`, fade) and the master's tape, shelf and glue.

**Songs.**
- t4 (v102, 110 rounds). Did not land: the hats, the glockenspiel and shaker in B2, the bowl and the piano are still masked; the +8 dB master shelf at 6 kHz is a band-aid over dull sources; the duet does not lift with her at the climax. With one more pass I would have the climax heard first: her E5 at 3:31 swings +/-50 cents. The recorded v101 round note names the wrong chords (they are Am11, G6/9, D9).
- t8 (v104, 109 rounds). Did not land: the early stretto (bars 17-64) is narrow above 2 kHz; the horizon is as loud as the jet for 35 s; only one of her six questions opens its mouth in time (v103); in the song's own choir Whisper heard 'all of it' at no diction level (one seed). Three rounds were shaped by keeping one weak boundary (2:08) over a threshold, and the opening's level lane was dropped for it.
- Never checked by ear: strictly all of it. I cannot hear, and Harry left no note on t4 or t8. The riskiest are the last fourteen rounds (t4 v96-v102, t8 v98-v104): the width, the drummer's ghosts and fills, the tape on both masters, the drive on her voice, the lift, the frozen halo, the pump, the diction.

**Album.**
- My joins: t3 -> t4 is the one term t4 loses (tone 3.1-3.2 dB against a free 3.0); the level step into t8 is 3.6-4.0 dB (1.9 before I compressed t8's master) and never got the lane that would restore it; t4's last low D is the loudest thing in the t4 -> t5 overlap and stands on measurement alone.
- Width is uneven: at the 10 Nov snapshot t8's top read -2.6 against -4.5 to -6.7 for the other seven. The album's mono top was found late and I fixed it only on my own tracks.
- The film had to read t8's frozen word from a gain lane (`fo`), not the bus that makes it: I named and placed lanes with no thought for the picture.

**Next record.**
- Start from what is heard, not the score. Ninety-odd versions of each track were steered mostly by compscore and flatness near their ceiling; the six deep passes per track after Harry said go deep, judged from stems, pictures and limiter work, changed more of the sound. Build the benches (share, masterlab, look, bounds) and the master chain in the first week.
- Test the singer and her words with Whisper before writing lines to notes, and put an A/B sheet in front of Harry every few days: 'far side' read as 'outside' for most of this album's life.
