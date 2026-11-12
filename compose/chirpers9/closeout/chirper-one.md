# chirper-one: close-out (Accretion: t2 The Long Way In, t6 Spring Tide)

**Engine.**
- Wanted and did not have: a voice setting per line. `diction` is per track, so t6's five fast statements at 3:37-3:46 went out slightly worse at level 2 (Whisper's support for the words -0.95 to -1.06, both seeds), because the same track's three slow lines gained far more. Also `play.phrase_gap` (not pinned): `phrase_arc` gives the trombone's fast runs in t6's surge one long arc where they want several.
- Landed too late to use well: `diction` 2 (the day of the cut; set by measurement, no listen); `phrase_arc` (one round a song). Never used by me: `diph_hold`, `cluster`, the `nasal` voice.
- Worked around: an `lr4` width stage shifts phase even at width 1; a `terrain` layer has a DC mean, so each note thumps without a high-pass; removing a track's early notes re-rolls the rest of its per-note randomness (I added tracks, never thinned); a doubled sung line's solo level differs by up to 4 dB between seeds; the master `volume` sits after the master fx, so a raw render reads 3 dB under what they see.

**Patches/library.**
- Built inside the songs and never promoted: t6's hand cymbals (`ting`, additive), t2's wave-terrain keys on a radius lane (`orbarp`), and the two distance buses (`far` hall, `air` plate, one distance lane), which want to be a rack. The computer-music patches I listed for palette rounds (`gendy-cloud`, `fof-chant`, `vosim-voice`, `shepard-pad`) were never tried.
- Not done: `features.md` still says t6 uses a Duffing chaos layer. It does not.

**Songs.**
- **t2 The Long Way In (v111, 99.61).** Did not land: its head (0:00-0:32) never had a round, and the join from t1 is still its one scored cost (spectral distance 4.30; from bar 9 t2 is 9 to 21 dB brighter than t1's tail at 8-16 kHz). With one more pass: the crest. v104 widened the top everywhere round it and I kept the crest line frozen as Harry liked it, so the crest is now the narrowest place in the song, and its limiter still works over 2 dB on average. "each", the hook's top note, is still not heard as a word.
- **t6 Spring Tide (v116, 99.81).** Did not land: the floor never moves (the sub owns 20-45 Hz; I put a 909 under the kick, but the low end's level stays flat); 600-1400 Hz is crowded and hidden by master EQ cuts, not carved at the source; it is the album's flattest track on eco's map (31%); "far side" and "near side" are not heard as words. Its head and the torn section (3:37-4:06) had no deep pass.
- **Never checked by ear, both.** I cannot hear, and t6 has no listener note at all. Harry heard t2's crest at v22 and its hook at diction 2. Unheard and exposed: t6's glue and clipper on the crest (v109), +3 dB at 250-500 Hz in its second chorus (v111), the closing canon at 1:35 (v115, which eco's map reads as flatter); t2's distance buses, widened top and louder swarm (v103-v106) and the melisma on the last word (v107). Four round notes carry wrong "listen for" times or counts (t2 v81, v87, v95; t6 v98).

**Album.**
- Joins: at t2 to t3 the bass stopped dead at the swap bar until the last morning (swap moved to bar 16: largest one-bar step -11.9 to -3.1 dB), and t6 to t7 needed t6's floor to sink through the overlap (5.8 to 2.5 dB). Both were found by eco's bar-by-bar reading. The scorer reads 3 s either side of an overlap and nothing inside it, so my seam numbers had looked fine for days.
- Weight: on the last day my two songs gained nine tracks and four reverb buses. I never measured what they cost the groove to render live; eco had to tell us the songs had become heavier.

**Next record.**
- The score had stopped guiding long before the end: t2 moved 0.01 in its last 34 rounds, t6 0.17 in its last 20. What found real faults were the instruments of the last two days (`amap`, `share`, `flatness`, `limwork`, `chirpers.py seam`, teacher-forced Whisper). Have them in the first week, and send Harry a clip of every exposed change the day it is made, so the record does not end on a list of things nobody heard.
- Give each sung line its own track, read every join inside its overlap from the first version, and agree the sub's octave across a join before either side writes its bass.
