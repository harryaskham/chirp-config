# Chirpers V (untitled): the album's motif bank

Shared themes, riffs, rhythmic cells and harmonic ideas that tie the album together. Add yours when you compose a track (name, where it lives, how it is written: notes/rhythm), and say when you quote or transform another track's motif.

## t2 (chirper-one): 2-step liquid, "Last Night Bus"

- **THE CHORDS**: Gm9 - Ebmaj9 - Bbmaj7 - F6/9, two bars each, on a physical Rhodes (epiano-tine with the epiano-damper release): struck on the one, re-struck without the root on the and-of-2 of the second bar.
- **THE SHUFFLE**: amen-chops slices on the eighth grid, two alternating bars [0 3 4 6 10 9 7 14] / [0 3 4 11 13 9 15 22], off-eighths 0.04 beat late, plus garage skips: slice 2 (ghost) on the e-of-2 and slice 1 (kick) on the e-of-4.
- **THE HOOK**: a wordless voice (^o, formant +2) on the chord's top tones - top, next, a held third, back - every other chord in the drops, every chord in the break, into a 3/16 echo.
- **THE GARAGE CHOPS**: a second voice up a fifth (formants kept), ^e, sixteenth stabs on the off-beats (0.5, 1.25, 2.5, 3.25) of every chord's second bar in the drops.
- **THE WORDS** (v4): the garage chops sing the title in fragments - 'night' (n-ay1-t), 'bus' (b-ah1-s), 'night', 'home' (hh-ow1-m, held a little longer) - on the same off-beat stabs: the vocal sample a garage producer would have chopped, synthesised.
- **THE GLITCH**: the amen track's stutter (1/16, 4 repeats, roll 0.5 to 1/64) opens on the last beat of every eighth bar of the second drop.
- **CLEAN LOUDNESS** (v2, chirper-two's recipe): the master's last compressor is now +12 dB into a fast 10:1 (-5 dB, 0.3 ms, 60 ms, +2.5 makeup) instead of 6:1 at 1 ms with +7 makeup, so the amen's transients are caught softly before the -1.5 dB ceiling: -12.2 LUFS, true peak -1.1 dBTP, longest pinned run 6 -> 4.
- **NO PINS** (v3): the master ends on a 13.5 kHz low-pass, -4 dB and a low-knee soft clip (-2.3 dB, knee 0.55) under a -1 dB ceiling, song volume 0 dB (chirper-zero's find): true peak -1.3..-1.6 dBTP, longest pinned run 4 -> 1, -12.8 LUFS - levels 100.

## t6 Overpass Rain (chirper-two)
- **THE CHORDS**: Fm9 (Ab3 C4 Eb4 G4) | Dbmaj9 (F3 Ab3 C4 Eb4) | Bbm9 (Ab3 C4 Db4 F4) | C7sus(b9) (Bb3 Db4 F4 G4), two bars each, Rhodes comped 2-step: beats 0, 1.75, 3.5, 5, 6.5 of each two bars.
- **THE HOOK** (hummed, voice engine): C5 Ab4 G4 . Eb4 F4 (oo oo oh oh ah), eight beats, falling; chopped answers: slices 1, 2, 3, 5 on the and-of-1, the e-of-2, 3 and 4.
- **THE ROLLER** (amen-chops, eighth-note slices per bar): 0 3 2 7 | 4 5 2 6, every fourth bar 0 3 2 7 | 4(^tune=2) 5 2 15 6(^tune=5); break-kit kick on 1 and the and-of-3, snare on 2 and 4.
- **THE END HOLDS** (v2): the outro's last chords are held over the rain with the pad, a 0.5 s tail, so it hands Concrete Hum a room, not a silence; the Rhodes drifts across the stereo field on a 3-bar song-time LFO.
- **FINAL ROUND** (v3, Harry's notes): the sub gains a mid layer (wM's phantom: its 2nd-6th harmonics) so the line reads on small speakers; the first drop ends on a one-beat TAPE STOP into the break; the build climbs through a resonant low-pass from 400 Hz to open; the top comes down 1.5 dB above 6 kHz; true-peak master.

## t1 First Light (chirper-three), the opener
Generator `compose/chirpers5/src/chirpers5-t1.py`. 2-step liquid, 174 bpm, C minor / Eb major.
- **THE 2-STEP**: kick on 0 and THE SKIP, which since v3 wanders bar by bar like a drummer's (steps 10, 11, 10, then 7 and 10 together on every fourth bar), snare on 4 and 12 with soft ghosts on the off-sixteenths (3, 9, 14), sixteenth hats swung like garage (the off sixteenths 0.085 of a beat late, ~29 ms, since v6) with their accents in a 3-3-2 (0 3 6 | 8 11 14), and since v6 a dry RIMSHOT on the swung off-sixteenths 7 and 14 in the drops, so the swing is heard, not just felt (chirper-one's note).
- **THE CHORDS** (two bars each): Abmaj9 | Gm9 | Cm9 | Bb13sus, a juno pad held under an epiano comping in the 2-step's gaps (the and-of-1, the a-of-2, the and-of-3 of the second bar), its damper on each release.
- **THE HOOK** (two bars): `G5 . . Eb5 . . F5 . . . G5 . . . . . | Bb5 . . G5 . . F5 . . . Eb5`, since v4 on a breathy LOW WHISTLE, legato (each note held to the next), at pitch where it fills the mix's 1 kHz hole (an octave down it crowded 300-400 Hz); sparse in the intro, every other phrase in the drops, alone in the break. (v1-v3: a vocal chop; the vocal side of 2-step is chirper-one's Last Night Bus.)
- **THE AMEN BED**: wM's amen-chops re-sequenced from its ghost and ride slices only (never its kicks or main snares), quietly, high-passed, one hit re-pitched (+2) or reversed now and then. Since v5 the first drop OPENS BARE: eight bars of the 2-step, the sub and the keys alone, then the amen bed and the whistle hook join at bar 41.
- **THE ROLLER** (since v7, the second drop only): the bed comes forward as a roller, eighth-note amen slices `0 2 3 6 | 4 11 13 7` (the second half from the break's other bar on odd bars), off-eighths laid back 0.04 of a beat, the fourth bar's last hit `^tune=3`: the opener ends in the album's rolling world.

## t4 Hairline (chirper-zero)
Generator `compose/chirpers5/src/chirpers5-t4.py`. Liquid glitchstep, 174 bpm, G minor.
- **THE CHANGES**: Gm9 | Ebmaj9 | Cm11 | D7sus4 (b9 colour), a chord a bar; the physical-tine Rhodes (with the damper) on 1 and the and-of-2, a juno pad under it, a reese and a sub on the root (1 and the and-of-3, with the kick).
- **THE VOICE**: wordless chops from the voice engine on the chord's 9th, 5th and 3rd, falling after the snare (16ths 5, 7, 14), the vowels turning ah - oo - eh bar by bar; in the half-time middle they fall after its snare on 3.
- **THE HAND-OVER** (v7): the outro's Rhodes no longer stops four bars early - each of the last four bars rings one soft whole-bar chord, the last the D7sus(b9), and the render tail is 1 s - so the dominant hands straight into Underpass's Gm9 (t5 opens in Hairline's key).
- **THE WOBBLE** (v6): in the half-time middle the reese gets its own voice an octave up, through a resonant low-pass (q 4) swept by a triplet-quarter LFO - three wobbles to every two beats, pulling against the half-time snare - so the roller falls through the crack into glitchstep proper before it climbs back out.
- **ACROSS THE LINE** (v5, chirper-one's note): the phrase-end cracks no longer stop at the bar line - the stutter runs on through the next phrase's downbeat (the half-bar plus the first beat), so the one itself arrives fractured and the crack pulls the beat into the new phrase instead of decorating the old one.
- **THE HAIRLINE**: the last half-bar of every 8-bar phrase cracks - a buffer stutter on the drum bus whose repeats rise in pitch and accelerate toward 1/64 - so the seams lift instead of breaking; in the climax every other bar cracks, in the half-time middle every fourth.
- **THE KIT, LEANED ON** (v3): the 2-step kick and snare driven (0.5) and squeezed by a fast compressor on their own track, so the backbeat snaps and the kick has a front edge - the roller pushes now instead of sitting square under the chords.
- **THE WALK** (v4): in the second drop and the climax the reese leaves the root and walks - root (3 sixteenths), octave (3), fifth (4), root (4), flat seventh (2), gliding between them - while the sub keeps the root underneath, so the return develops instead of repeating.
- **THE ROLL**: wM's amen-chops under the clean 2-step kick and snare as a ghost roll (high-passed at 350 Hz), the break re-sequenced 16th by 16th, its fourth bar turning to the break's tail.


## t3 (chirper-one): reese-led, dark to light, "Ring Road Sunrise" (v4 re-style)

- **THE DARK**: G minor (Gm - Ebmaj7 - Cm - D roots, two bars each). A reese lead plays an eight-bar line, brooding and gliding: G3 Bb3 A3 G3 | Eb3 F3 G3 | C4 Bb3 A3 G3 | F#3 A3 G3 (overlapping notes), its low-pass (1.4 kHz) breathing on an eight-bar LFO; a low juno pad and the sub under it; no piano, no voice.
- **THE LIGHT**: the drops turn to Bb major - Ebmaj9 - Bbmaj7 - Fadd9 - Gm9 - and a concert grand arrives for the first time, house stabs (one, and-of-2, four) with a left-hand root; the reese drops to bass (root + 12, three hits a bar).
- **THE MEETING**: the break holds the light chords on the piano while the reese plays the dark line over them (its F# becomes F in the light).
- **THE DAWN BREAKS** (v5): the master's last beat before each drop is caught and replayed rising - wM's stutter with a pitch ramp (1/16 slices, 4 repeats, +3 semitones a repeat) - so the dark verse winds itself up into the light; the drop lands on the clean one.
- **THE HANDOVER**: the last four bars hold Ebmaj9 over a low G (pad and piano) into Hairline's Gm9; the render tail is 1.2 s.
- (v2's semitone lift is withdrawn: it is Streetlights Off's.)

## t10 Streetlights Off (chirper-zero)
Generator `compose/chirpers5/src/chirpers5-t10.py`. The closer: euphoric liquid D&B, 172 bpm, Db major (the last drop in D).
- **THE CHANGES**: Dbmaj9 | Ab/C | Bbm9 | Gbmaj9 - a lifting I-V-vi-IV that keeps falling back to its minor sixth; the piano comps it in 2-step stabs (1, the and-of-2, the and-of-3), the strings hold it.
- **THE HOOK**: the voice engine, wordless: Ab4 . F4 Ab4 Bb4 | Ab4 . Eb4 . | F4 Eb4 Db4 Eb4 | F4 . . . (vowels turning); in the half-time interlude a second voice sings it a diatonic third above.
- **THE INTERLUDE**: the drops' breakdown is half-time (kick on one, snare on three), the strings an octave up - a held breath before the second drop.
- **THE LIFT**: the last drop a semitone up (D major), the piano rolling the chord in 16ths an octave up, the ride on the off-beats, a one-bar pull-out and a riser before it - the album's biggest lift.
- **THE DESCANT** (v4): in the second drop the strings add the chord's top tones an octave up, falling in half notes above the hook - the drop develops instead of repeating the first.
- **THE THIRD COMES BACK** (v4): the interlude's second voice (the hook a third above) is held back through the second drop and returns only in the lift, transposed with it - the last reveal is the harmony you heard once, now a semitone higher.
- **THE DISSOLVE**: the drums leave, then the bass; the piano picks the hook out alone an octave up, the voice hums the last phrases, and the city's air comes up as the streetlights go off.


## t8 (chirper-one): jungle-tinged liquid, "Wet Brick"

- **THE BREAK, WHOLE**: amen-chops in its own order - bar n of every four plays slices 8n .. 8n+7 on the eighth grid: the original amen at 170.
- **THE EDIT**: the fourth bar of every phrase (and, in the second drop, the second bar of each phrase's second half): odd slices reversed (^rev=1), the snares on slots 2 and 6 re-pitched (^tune=+3, +5 in the second drop), the last eighth replaced by the snare at +7 then +12 in sixteenths; in the second drop that beat also stutters into a roll (1/16 -> 1/64).
- **THE BOOM**: 808 sub on the root for three bars, then overlapping notes slide up the octave and down to the fifth into the next root.
- **THE BED**: juno pad Fm9 - Dbmaj7 - Ebsus2 - Cm7, four bars each; a Rhodes answers each chord on the and-of-2 (upper three notes, an octave up) into a 3/8 echo.
- **BARE JUNGLE** (v2, taking away): the second drop's first sixteen bars have no pad - just the edited break, the boom's glides and the Rhodes answers - and the bed returns for its second half, so the second drop is a different place from the first rather than a repeat.

## t7 Concrete Hum (chirper-two)
- **THE REESE RIFF** (two bars over each chord root, in 3+3+2 sixteenths): root root m3 | root b7 root || root 5 4 m3 2. Glides (gate 1.15), the filter breathing on 3- and 5-bar LFOs, a notch on a 7-bar one.
- **THE CHORDS**, four bars each: Gm9 (Bb3 D4 F4 A4) | Ebmaj9 (G3 Bb3 D4 G4) | Cm9 (Bb3 D4 Eb4 G4) | D7(b9) (C4 Eb4 F#4 A4); Rhodes stabs on the a-of-1 and the a-of-3 every other bar.
- **THE COUNTER-REESE** (second drop, an octave up): 8ve b7 5 | m3+8ve 8ve.
- **THE ROLLER**: amen slices 0 1 2 3 | 9 13(a-of-3) 2 7; the kick on 1 and the a-of-3, snares on 2 and 4; half-time break: kick 1, snare 3.
- **THE END HUMS** (v2): the outro carries the pad and the held reese hum (the intro's mirror) to the last bar, a 0.5 s tail: no more four bars of silence before Wet Brick.

## t9 Late Shift (chirper-three)
Generator `compose/chirpers5/src/chirpers5-t9.py`. Liquid funk, 174 bpm, A dorian.
- **THE CHANGES** (a bar each, eight-bar cycle): Am9 Am9 | D9 D9 | Gmaj9 Gmaj9 | F#m7b5 B7#9; Rhodes on the one and re-struck rootless on the and-of-2.
- **THE FUNK LINE** (finger bass, sixteenths from the root): A `0~~ 8va . b7~ 5~ 0 b3~ . 4 5`, B `0~ 0 8va~ . b7 5~~ . 4 b3~ 2 0` alternating bars, ghosts at low velocity; an 808 sub doubles the roots.
- **THE CHOPS** (cutting guitar): off-eighths 2 6 10 14 with sixteenth pushes on 7 and 15, the chord's upper voices an octave up.
- **THE STABS** (horn section): `da-da-DAAT` on sixteenths 10 12 14 at the end of every fourth bar (every second in drop 2).
- **THE SOLO** (lead-wah, the break, twice): `E5 . G5 A5~ | G5 E5 D5~ B4~ | C5 D5 E5 F#5~~ | E5 D5 B4~~ | A4 C5 E5 G5 B5~~ | A5 G5~ E5~ | F#5~ A5 C6~ | B5~ A5 F#5~~`.


## t5 (chirper-one): ambient / half-time interlude, "Underpass"

- **THE TUNNEL**: piano-wash holds Gm9 - Ebmaj7 - Cm9 - Dbmaj7 (four bars each, rolled) and moves the album from Hairline's G minor to Overpass Rain's F minor, ending on a held Fm9.
- **THE HALF-TIME**: amen slices at (beat, slice) 0/0 kick, 1.5/3 ghost, 2/4 snare, 3.25/10, 3.5/6 - the one and the three - with the sub on the root every two bars; only in the two half-time sections.
- **THE WALLS**: a second amen-chops track plays the whole amen in order at -40 dB, sent +22 dB into a bus of granular cloud (60 ms grains, density 14, spray .6, scatter .4, 35% reversed) then a 5 s hall, low-passed at 3 kHz: the next room's drum & bass smeared into concrete - only in the intro's second half and the drift, where the beat is not.
- **THE GLASS**: in the second half-time a pad-glass bell on the chord's top notes (an octave and two up), every other bar.
- **A CLEARER TUNNEL** (v2, mix): the master EQ moves the weight out of the mud and into the floor - 45 Hz -4 (the sub's boom), 110 Hz +4 (the half-time kick's body), 220 Hz -3 and 450 Hz -6 (where the washed piano and the voice pad piled up), air above 13 kHz +3 (the glass and the walls' grains).
- **THE SHIFT ENDS** (since v2, after chirper-zero's seam note): the outro's D9 slides down a half step into a held DBMAJ9 for the last four bars (Rhodes Db2 + Ab3 C4 Eb4 F4 Ab4, a soft horn swell C5 F5 Ab5, bass and sub on Db), a 1.2 s tail: the band hands its last chord to Streetlights Off, which opens on Dbmaj9.
