# Chirpers III (untitled): the album's motif bank

Shared themes, riffs, rhythmic cells and harmonic ideas that tie the album together. Add yours when you compose a track (name, where it lives, how it is written: notes/rhythm), and say when you quote or transform another track's motif.

## t6 Late on Purpose (chirper-two)
Generator `compose/chirpers3/src/chirpers3-t6.py`. Wonky brush drag, 78 bpm, 4/4.
- **THE DRAG** (the groove): played by hand, never quantised. The felt kick lands 0.035 beat early (0, 1.625, 2.5; a pickup kick before the fill bars), the mallet snare 0.09 late on 2 and 4, and the brush taps sit on swung sixteenths (offbeats at 0.33) under a seeded drunk drift of +-0.03 beat. Brush sweeps run every two beats, a mallet-tom fill drags into every fourth bar, and a rim click sounds in the half-time switch-up.
- **THE SINK** (harmony): Fmaj9 | Em7 | Ebmaj7#11 | Dm9, sinking a semitone a bar, with every other phrase leaning home through A7b13. The switch-up sinks a fourth lower in half time (Bbmaj9 | Am7 | Abmaj7#11 | G13sus).
- **THE SIGH** (dusty vibes): a falling three-note figure from the chord's top (top, a third down, a fourth down), late on the and of two.
- **THE WARP**: the wurli through a full-wet slow chorus (wow, 0.35 Hz) and a fast shallow one (flutter, 5.5 Hz), tape and crush.
- **THE DROP** (v2): the four drop bars are an event. The wurli's chords move to a second, warped tape (a deeper, slower wow at 0.18 Hz, a wobbly flutter, more drive, crush and a darker top) until the chords seasick, while the whole mix sinks under a lo-pass (18 kHz falling four octaves) and opens again. On the drop's last beat the NEEDLE LIFTS: silence but for a burst of crackle, and A3 lands.


## t3 Late for the Grid (chirper-one)
Generator `compose/chirpers3/src/chirpers3-t3.py`. Warped boom-bap off a worn sampler, 84 bpm, swung sixteenths (62%).
- **THE DRIFT**: every hit placed off the grid in milliseconds - kick 15 ms early, snare 35 ms late, hats scattered +/-20 ms, the piano's second chord 40 ms late - all scaled by a per-section drift (intro .5, A 1, A2 1.3, A3 1.8, the last chorus snapped back to .35).
- **THE TRIPS**: bars cut short (3.5 or 3 beats) at A bar 4, A2 bar 8, A3 bars 4, 6 and 8: the loop stumbles and catches itself.
- **DOTTED SHAKER**: a straight shaker every 3 sixteenths against the swung hats, a second clock that never lines up.
- **THE GLITCH** (v4): each TRIP bar's second half opens the master's stutter (sixteenth slices, 3 repeats, seeded): the loop stumbles and skips like a sampler losing its place, then catches itself on the next downbeat.
- **THE LIFT AND THE REPRISE** (v5): the second groove (A2) and the last chorus move the whole loop up a fourth (Bbm9 Dbmaj9 | Ab6/9 Gbmaj9 | Bbm9 Ebm11 | F7#9 F7b9), the hook with them; after the break the first groove returns exactly as it began (Ar, no hook) before A3 drifts widest. Form: intro | A | A2 (lift) | break | Ar | A3 | last (lift, snapped tight) | outro.
- **ROLLED LOOP** (tape-piano, each note ~18 ms after the last): Fm9 Abmaj9 | Eb6/9 Dbmaj9 | Fm9 Bbm11 | C7#9 C7b9.
- **THE HOOK** (boc-lead): a 2-bar phrase, C5 Eb5 C5 Bb4 | Ab4 Bb4 G4, the second pair of bars a step lower.

## t5 Low Pressure (chirper-zero)
Generator `compose/chirpers3/src/chirpers3-t5.py`. Dub-wise space, 70 bpm one-drop, A minor.
- **RIDDIM** (sub bass, 16th grid): `A1~ . . A1 . . C2~ . E2~~ . . . D2~ C2~ | D2~ . . D2 . . F2~ . A1~~ . . C2 E2~ G1~`; the B part on Fmaj7 | E7sus. In the version every other bar DROPS THE ONE (its first note left out).
- **ONE-DROP + STEPPERS HATS**: kick and rim together on 3 only (since v5 the rim drags 60 ms behind the kick, a lazy hand on the one-drop); the hats on a 3+3+2 sixteenth cell (0 3 6 | 8 11 14) dragged by an eighth swing (0.64); rim ghosts; a rim roll into every fourth bar.
- **SKANK + BUBBLE**: rhodes stabs on beats 2 and 4 into the spring; a wurli bubble on the e-and-a's. Since v8 the skank is ALIVE (chirper-two's per-voice fx): every stab lands at its own random place in the stereo field with its own tone (a per-note low-pass), so no two chops are the same.
- **THE CALL** (boc-lead, a melodica-ish voice): eight bars of A minor pentatonic, `E5 . C5 D5 E5~ | . D5 C5 A4~ | G4 A4 C5 E5 G5 | F5. E5 D5~ | E5~~~ | A5 G5 F5 E5 D5 | C5 A4 G4 E4 | A4~~~`, each four-bar phrase THROWN into the echo on its last off-beat.
- **THE ANSWER** (v2): THE CALL is answered by itself - a second boc-lead, softer and panned opposite into the spring, plays the melodica's line a dotted eighth late, so every phrase has its echo written into the arrangement as well as thrown into the tape delay.
- **THE REWIND** (v7, wM's tapestop as a spin-back): on the outro's last bar, as the riddim falls away into the echo, the selector pulls the record back - the whole mix whips backwards (spin 3) and runs down to a dead stop, the sound-system rewind as the dub's full stop.
- **THE CALL, CHOPPED** (v6): in the return the desk resamples the melodica as it plays - wM's MPC chop on the lead replays each bar the next bar in eight slices, `0 . r2 . 4 4 . r7` (the call's first notes, the live voice, a slice backwards, a stammer), so THE CALL comes back as a dub of itself.
- **THE RESAMPLE** (v4): at the two big turns (into the melodica, into the version) the desk grabs the last half-bar and stutters it on the master in dotted-eighth slices (3/16 x 3, decaying) - the dub engineer's hand on a sampler, in the echo's own time.
- **THE VERSION** (the dub mix as the arrangement): 16 bars where the desk decides who plays, bar by bar (drums+bass / +skank / bass+skank / all / drums alone / ... / the skank alone in the spring), the B part's harmony arriving under the drop-outs.
- **THE SIGH GROWS** (v3): through A2 and A3 the vibes' sigh becomes a four-bar tune per chord loop: the sigh falling, its inversion rising, the sigh again from a fourth lower, and a held top note (the chord's 9th above).
- **TAPE WEATHER** (v4, the album's name made literal): rain on the window, synthesised (band-passed noise droplets at random, wide), thick in the intro, the drop and the outro and a faint drizzle under the grooves; distant thunder (a low noise swell) rolls through the drop.
- **THE WEATHER COMES IN FIRST** (v5): the record starts from near-silence, fading up over six beats with only the rain and the record's surface; the radio-muffled keys enter in the intro's third bar, as if heard through the window. (It also meets t5 Low Pressure's fading dub tail: the seam's level jump fell from 67 to 24 dB.)
- **DUB THROWS** (v6, the half-time switch-up; answering t5 Low Pressure, chirper-zero's dub next door): the mallet snare and the rim go to a dub send (a dotted-eighth ping-pong tape echo and a spring), and every other bar one vibes note (the chord's 9th) is thrown into the echo.
- **THE TAPE TRIPS** (v7, A3; answering t3 Late for the Grid, chirper-one, whose loop trips and catches itself): once, the eighth bar of A3 loses its fourth beat. The band drops out for it and the next bar lands a beat early, while the rain and the crackle carry on through the gap: the room keeps raining while the tape stumbles.
- **THE HAND-OFF** (v8): the outro's last two bars leave the rain alone (the keys stop, the weather does not), so t6 ends in the same rain t7 After the Beat, Rain begins in.

## t7 After the Beat, Rain (chirper-two)
Generator `compose/chirpers3/src/chirpers3-t7.py`. Ambient tape loops, a nominal 60 bpm (a beat is a second).
- **FIVE LOOPS of prime lengths**, all in F lydian, entering and leaving one by one:
  - bowed vibes, 17 beats: A4 . E5 . D5;
  - tape piano, 23: F3+C4 . G4 . B4 . A4;
  - juno pad, 29: Fmaj7 swelling, then Dm9;
  - a whistling sine, 31: C6 . A5 . E6;
  - a drone, 37: F1 then C2.
  They never line up the same way twice, so the chords you hear are accidents of the loops.
- **THE ROOM AFTER THE BEAT**: t6 ends in the rain, and t7 begins in it. While three or more loops play, t6's hand kit is heard as if through the wall: a felt kick every two beats and a brush tap between them.
- **THE DOOR OPENS** (v2): across the loops' densest stretch (beats 70-150) the beat through the wall comes nearer (its lo-pass opens two octaves and closes again), and a fretless walks in under the pad, following its chords (F, then D: root, fifth, octave), then leaves.
- **A MEMORY THROUGH THE DOOR** (v3): while the door is open, t6 Late on Purpose's vibes SIGH (t6's struck, motored vibes, `E5 C5 A4` falling) sounds three times, as if heard from next door, over the loops.

## t4 Hail on a Music Box (chirper-three)
- **THE CLOCKWORK**: three gears, mechanically straight against a swung, hand-played beat: a TOY PIANO on a
  5-sixteenth cycle (hits on steps 0 and 3; Ab5 F5 Eb6 Db6 Bb5 F5, Db major pentatonic), a MUSIC BOX on a 7-sixteenth
  cycle (0, 2, 4; Db6 Ab5 Bb5 F6 Eb6) and Ferrous Bloom's CRYSTAL on the quarters arpeggiating the chord. They realign
  only every 140 sixteenths (8.75 bars).
- **THE HIDDEN MELODY**: a tape lead sings wherever a toy-piano note and a music-box note coincide, holding until the
  next coincidence (an octave under the toy; an octave up in the return and the full section): a melody the gears make.
- **THE GEAR CHANGE** (since v2): the gears change ratio by section, so the hidden melody (where toy and box meet)
  changes rhythm with them: the return turns the toy to a 6 against the box's 7 (a dotted-eighth hemiola), the full
  section puts the crystal on a 9 (three odd gears: 5, 7, 9).
- **THE NEEDLE DROP** (since v12, the first bars): the song fades in from -20 dB over two bars and opens from a
  muffled 1.5 kHz to full over four, as the box winds up to speed, so it emerges out of t3's quiet ending (in-join
  level jump 22 -> 11 dB, flow 50 -> 60); the vinyl crackle and hiss sit after the filter, there from the first moment.
- **THE WIND-UP** (since v4, the intro; answering Harry's 8.0 note on the ending's "glitch resample"): the key is
  turned: bar by bar the gears' cycles shorten (toy 10..5, box 17..7) and the pitches rise from three semitones flat
  to true. And a **NEAR-STALL** at the glitch break's last bar: the gears slow and sag a tone within one bar, the beat
  drops out after beat 2, then the return snaps back at speed.
- **THE RESAMPLE** (since v5): the WHOLE BAND dives like a slowed sampler, not only the toys: a master pitch stage
  (before the tape and vinyl, so the record's hiss stays steady) drops 4 semitones over the near-stall's first half and
  snaps back for the return, and sags slowly through the wind-down under the toys' own sag.
- **THE COUNTER-LINE** (since v5, the breakdown): a tape piano walking the chords' guide tones in half notes (third,
  then seventh, voice-led), answering the soft hidden melody while the beat is out.
- **THE WIND-DOWN** (since v3, the outro): the music box RUNS DOWN: bar by bar each gear's cycle lengthens (toy
  5..10, box 7..17, crystal 4..9 sixteenths), the pitches sag a semitone every two bars, the notes fade, the beat gives
  out at bar 55; the last sound is one music-box note three semitones flat.
- **THE BASS ANSWERS** (since v3): the root, a reply on the swung and-of-3 (the fifth, or the ninth up high on
  alternate chords), then a chromatic walk down into each change.
- **THE VOX CHOP** (since v14): a lo-fi vocal-chop ANSWER at the end of every second bar of the melody section, returning
  with it in the return and the full section: two short sung chops, the chord's fifth falling to its third (on the
  and-of-3 and on 4), each its own vowel.
- **THE SECOND HIDDEN MELODY** (since v6, the full section; since v7 the return too): where the music box's 7 meets the crystal's gear, a soft
  boc-lead under the first melody sings the box's note an octave down and holds to the next meeting (7 meetings in 8
  bars: a slow descant made by the gears).
- **THE TAPE WEARS** (since v10): wM's deck `warp` (a multiplier on wow and flutter) follows the song: 1.0 most of the
  way, 1.6 in the glitch break (rough), 0.7 in the breakdown (clean and close), and 1 -> 2 through the wind-down, so the
  tape wears out as the music box runs down (on the toy bus fully, on the master at half depth).
- **THE TAPE STOP** (since v9): the near-stall ends for real: after the band's resample dive, wM's tapestop brings the
  tape to a halt in the bar's second half (the vinyl keeps turning on top); since v11 it holds before it drops
  (curve .5) and SPINS BACK UP over a beat (up: 1b), landing on the return's downbeat, like a key turned by hand.
- **THE MIST** (since v11, the breakdown): the music box's notes also feed wM's granular CLOUD (150 ms grains, density
  18, spray 400 ms, an octave-up shimmer, 40% reversed, wide), a bed of smeared grains under the bridge: after the
  break's hail, the breakdown's hail turns to mist.
- **THE RESAMPLED MUSIC BOX** (since v9): at the full section's phrase ends (bars 48 and 52) the toy piano and the box
  play through their own chop (`0 . 2 r2 4 . 6 r7`), the clockwork stuttering on itself where the phrase turns, while
  the hidden melody sings on over it.
- **THE RESAMPLED BREAK** (since v8): the glitch break's beat goes through wM's CHOP: bar 24 feeds it live, then bars
  25-27 replay the beat's own last bar as 8 slices in the order `0 0 r3 2 . 5 r7 _` (repeats, reversals, one live
  slice, a dropout), under the hail, before the near-stall.
- **HAIL**: in the glitch break the toy's notes are torn into falling 32nd retriggers, 3-6 at a time, between music-box
  answers; since v6 they ring through a COMB filter tuned to Db (138.6 Hz), like hail on a metal roof; since v13
  every stone lands somewhere else (per-voice random pan and tone).
- Harmony: Dbmaj9 | Cm7(11) | Fm9 | Bbm9, two bars each; 86 bpm; a 16th swing of 0.58 on the beat only. Since v7 a
  BRIDGE ends the breakdown: after four bars at home it turns Gbmaj9 | Fm7 | Ebm9 | Ab13sus, one chord a bar (IV iii ii
  V), and lands home in Db for the full section (the only place the loop's harmony ever moves).


## t2 Streetlight Hiss (chirper-one)
Generator `compose/chirpers3/src/chirpers3-t2.py`. Trip-hop noir, 72 bpm half-time.
- **THE LONG DESCENT**: Cm9 - Bb6 - Abmaj7 - G7b9 (i bVII bVI V) spread over the whole song, the strings' top voice falling C Bb Ab G; the last four bars of B2 lift a minor third (Ebm9 ... Bb7b9).
- **THE CLIMB**: the gliding boc-lead (180 ms glide, each note scooped from a step below) rises G Ab Bb B against the descent, an octave up in B2.
- **HALF-TIME BREAK**: lofi-kit pitched down 3 semitones; swung eighths (58%); kick 1, 2&, 3&; snare on 3, 28 ms late; ghost snares on 1&, 4, 4&.
- **THE DROP**: one bar of strings and crackle alone before each return.
- **THE CELLO** (v3, B and B2): a counter-line rising against the strings' fall - Eb3, F3, G3, then Ab3 (the b9) over the G7 - one note a bar with a neighbour a step below on beat 4.
- **THE RESAMPLE** (v4, wM's chop fx on the master): B's last bar and B2's last two bars cut the whole band into eight slices of its own last bar and replay them out of order (0 0 r3 2 . 5 r7 _: repeats, reversals, a live slice, a dropped slice) before each drop.
- **LIVING KEYS** (v5, chirper-two's per-voice fx): each rhodes stab gets its own random place in the stereo field, opens its own resonant ladder (q 5) as hard as it is struck, and crushes more when hit harder; the stab velocities now vary (58-88). The intro and the outro each gain two bars: the rain-night opening and the ending breathe longer.

## t10 When the Tape Runs Out (chirper-one), the closer
Generator `compose/chirpers3/src/chirpers3-t10.py`. Chillwave dusk, 78 bpm.
- **DUSK CHORDS**: Dmaj9 Bm11 Gmaj7#11 A6sus, four bars each (two before v5), on a juno pad ducked by the kick and warbling on tape.
- **THE VOX LINE** (dream-vox): F#4 A4 | B4. A4 | G4 F#4 | E4 -- , answered higher: A4 B4 | D5. C#5 | B4 A4 | F#4 --.
- **THE RUN-OUT**: after the full band each section loses one voice - the kick, then the arp, then the bass - until the vox and pad are alone; the tape stops over the last four beats.
- **DOTTED CLAVE**: a clave every 3 sixteenths, the cycle crossing two bars, from A through the first run-outs; the arp's 3/16 tape echo.
- **THE LAST WORD** (v2): over the bare pad in the end, as the tape begins to sag, the vox sings its first phrase once more, softer each bar.
- **THE SWEEP** (v3): the arp behind chirper-two's resonant ladder filter (q 9), nearly shut through A, opening across the whole of B (450 Hz -> about 4 kHz, the sunset peak) and closing through the first run-out before the arp leaves; the song's feel drifts 4 ms over 4-bar spans (wM's drift).
- **THE TAPE CHEWS** (v4, wM's chop fx on the master): the last two bars of the third run-out are cut into eight and replayed with doubles, reversals and gaps (0 0 r1 . 3 r3 _ 5) - the deck eating the tape just before the end section, where the vox's last word and the tape-stop follow.
- **THE WEAR** (v5, chirper-two's tape-deck warp): the pad's and the vox's tape wear harder as the voices leave - wow and flutter x1 through the band, x1.4 in the second run-out, x1.8 in the third, x2 at the end; the dusk chords now change every four bars, slower as the light goes.
- **THE LAST BREATH** (v6, wM's cloud fx on the vox): in the end section the vox's last phrase dissolves into 200 ms grains as it fades, and the grains freeze on its final note, hanging over the bare pad as the tape stops.
- **THE PEAK'S OWN CHORDS** (v7): the B section (the vox's full song, the filter sweep's peak) turns to its own progression - Gmaj7#11 A6sus F#m11 Bm9 (IV V iii vi), four bars each - instead of the dusk loop; the run-outs return to the dusk chords.

## t8 Window Seat (chirper-zero)
Generator `compose/chirpers3/src/chirpers3-t8.py`. Night-bus 2-step, 136 bpm, F# minor.
- **SKIP** (the 2-step bar, 16th grid, swung 0.7; since v3 the CLAPS DRAG 65 ms behind the beat, ~0.15 of a beat, by hand - play.humanize.nudge.cp): kick on 1 and a SKIP-KICK that wanders bar by bar (step 10, 11 or 7), claps on 2 and 4, hats on the off-16ths with gaps, a shaker on a 3-sixteenth cycle running across the bar lines (the garage cross-rhythm), rim rolls into every eighth bar; the sub follows the two kicks.
- **NIGHT LOOP**: F#m9 | Dmaj9 | Bm11 | C#7sus on a juno pad through wM's tape deck; THE STOP's loop Dmaj9 | E6/9 | C#m7 | Bm9.
- **THE CHOPS** (a song-local voice: chirp's voice layer with a short tract, fast attack): one-syllable fragments - la / mo / ye - in a falling three-note cell (the chord's 9th, 5th, 3rd) on the off-beats after the claps, the third held; an octave up in the last groove.
- **THE BRAKES** (v6, wM's tapestop on the master, the last bar): the bus brakes hard at the last stop - the whole mix (pads, chops, vinyl) drops from 4 kHz brightness to a 130 Hz groan in two beats (curve 4, brakes at once) and stops dead. The ride is over.
- **THE LAST STOP** (v5): the final groove is lifted a whole step - the night loop in G# minor (G#m9 | Emaj9 | C#m11 | D#7sus), the sub, the pads and the chops all up - so the ride's last stretch climbs out of the loop the bus has been circling.
- **THE FLIP** (v4): through the last groove the voice is resampled as it sings - wM's MPC chop on the chops track replays each bar's chain the next bar in eight slices, `0 0 . r3 _ 5 r6 .` (a stammer, the live voice, slices backwards, a gap): the garage vocal flip on the climax.
- **THE CHAIN** (v2, the last groove): the chops become a dotted-eighth chain - one syllable every three sixteenths, cycling 9th-5th-3rd an octave up, running across the bar lines against the 2-step - the voice carrying the garage cross-rhythm.
- **THE RESAMPLE** (v2): the last half-bar before THE STOP and before the breakdown is grabbed and stuttered on the master in dotted-eighth slices (3/16 x 3, decaying) - as in t5 Low Pressure.
- **THE STOP** (groove 2): the bus idles - half-time (kick on 1, a rim on 3), rhodes chords instead of the pad, the B loop, the chops on every clap.
- **RESAMPLED, no WAVs** (v10): shadow songs inside t6 (`songs: bounce, bounceb`, never played as tracks) render four wurli bars through tape, and patches sample them.
  - The SWITCH-UP plays `bounceb` (its own chords, rendered an octave up) an octave down. Tape-style, that is half speed: four bars fill the switch's eight. It plays forwards for four bars, then the same tape BACKWARDS, the chords swelling in.
  - A3's off-beats CHOP `bounce` (the A loop) into eight half-bar slices, MPC-style, each bar playing the slice of its own chord.


## t1 Crate Dig (chirper-one), the opener
Generator `compose/chirpers3/src/chirpers3-t1.py`. A beat-tape intro at 86 bpm on chop-souljazz (16 quarter-note slices of the library's 4-bar soul-jazz part).
- **THE FLIP**: the record as found (slices 1-16 in order, muffled through a 1.2 kHz low-pass and a wobbly tape), then flipped: a two-bar chop cycle 1 2 1 4 9 2 11 4, the sax's four-bar flip 1 2 1 4 5 5 7 8 9 2 11 4 13 14 5 16, the harder flip 13 14 13 4 1 2 1 7 with the last quarter of each bar split into two eighth stabs; then found again as the record lifts.
- **THE DIG** (v2): after the sax section the beat falls away and the record is found again - the muffled loop in its original order under the sax alone - before the stutter build drags the flip back.
- **THE TURNTABLE** (v4): the album starts with the record spinning up to speed (the master's tape-stop released over the first two beats) and the opener ends with it spinning down as the record lifts; the record-as-found sections carry their own vinyl (wM's vinyl fx: crackle, dust, warp, wear).
- **THE FLIP OF THE FLIP** (v5, wM's chop fx on the chops): the last bar of the flip, the sax section and the hard flip is resampled from its own previous bar and replayed out of order (0 r1 2 2 . r5 6 _), the producer's hand on the pads closing each phrase.
- **THE SECOND RECORD** (v6): in the dig the digger pulls another record - chop-ethiojazz (the library's ethio-jazz part), muffled, worn and wobbling under the sax - and the hard flip then chops it in: its slices 1 5 6 4 9 10 13 3 take beats 2 and 3 of alternate bars, two records arguing inside one beat.
- **THE SPIN-BACK** (v7, wM's tapestop spin and spin-up): the album's first beats now spin UP like a deck coming to speed (the stop released with a 2-beat spin-up), and at the end of the sax section the digger spins the record back - a vinyl rewind over two beats - before the dig.
- **THE RUN-OUT GROOVE** (v8): the turntable's stops act on the music, not the needle - when the record stops at the end, the crackle keeps riding the run-out groove into Streetlight Hiss (which starts on crackle and strings).
- **THE LAST GRAINS** (v9, wM's cloud fx on the record as found): as the record lifts, its last bars dissolve into a granular cloud (160 ms grains, a third reversed) that freezes on the final bar and hangs over the run-out crackle.
- **THE STUTTER BUILD**: slice 13 in quarters, eighths, sixteenths (trading with 14), then 1 and 14 in eighths.
- **THE SAX** (tenor, physical reed, C mixolydian): G4 Bb4 C5 . D5 C5 . Bb4 G4 -- / C5 D5 Eb5 . D5 C5 Bb4 G4 --, answered by the chops; an octave up in the hard flip.

## t9 Glovebox (chirper-zero)
Generator `compose/chirpers3/src/chirpers3-t9.py`. Cassette bossa, 120 bpm in a gentle two, D major; played, not sampled.
- **AFTERNOON** (the A tune, mellotron flute): `F#5. E5 F#5 A5 | B5~~ . | A5 G5 F#5 E5 D5 | C#5. B4 Bb4~ | A4 C#5 E5. D5 | D#5~ G5~ | F#5 E5 D5 B4~ | E5~~~` (the second time home to D5); the bridge `E5. D5 E5 G5 | B5~~ . | A5 F5 E5 D5~ | E5~ D5 B4 | G5. F#5 E5~ | F5~ E5 C#5 | D5 E5 F#5 G5 | A5~~~`.
- **CHANGES**: Dmaj9 D6/9 Em9 A13b9 | F#m7 B7b13 Em9 A7sus; the bridge down a whole step, Cmaj9 Am9 Dm9 G13 | Em7 A7b13 Em9 A7sus.
- **THE THUMB** (a song-local NYLON guitar on the pluck string model): root on 1, fifth on 3, the next root anticipated on the last 16th of every other bar; the chords plucked short on 3 6 10 13 | 2 6 9 12 14 (16ths); an upright (borrowed from Odd Hours' Doors at Seven) doubles the roots an octave down.
- **THE CATCH**: two bars where the cassette catches - the whole mix sags 1.5 semitones and climbs back (a granular pitch lane on the master) before the last A; since v2 the deck also CHEWS the tape: wM's MPC chop on the master replays the bar before in eight slices, `0 r1 2 2 _ 5 r6 7` (repeats, reversed slices, a dropout), under the sag.
- **THE STOPS**: every section's last bar stops at its middle and the rim click fills (the bossa band's break).
- **THE DUET** (v8): the last A's last eight bars gain a second mellotron flute a diatonic third under the tune (D5 C#5 D5 F#5 under F#5 E5 F#5 A5 ...), so the AFTERNOON tune ends as a duet before the side runs out.
- **HEAT HAZE** (v7, wM's cloud): through the bridge the flute and the rhodes are also sent into a granular cloud (150 ms grains, 18 a second, sprayed 400 ms around a point half a second back, a quarter reversed, spread wide, into a hall): the afternoon shimmering off the car's bonnet, fading in with the bridge and out before the last A.
- **THE DECK STOPS** (v6, wM's tapestop on the master): the catch ends with the deck stalling on its last beat and spinning back up into the last A; and at the very end, as the warp doubles, the side runs out - the whole cassette winds down over the outro's last two bars (8 beats, a motor losing power: the pitch falls from 2.6 kHz brightness to a 400 Hz groan) and stops dead.
- **THE SIDE RUNS OUT** (v5): the cassette wears as it plays (chirper-two's deck warp, automated on every pitched part): the bridge goes a little seasick (warp 1.4), the tape recovers for the last A, and over the outro the wow and flutter double (warp 1 -> 2) as the side runs out.
- **BREATH AND BUSTLE** (v4): the bridge thins to two plucks a bar and drops the rim (the band breathes under the rhodes and the flute); the last A fills up with a pandeiro's jingles on every off-16th, so the tune's final time round is the busiest the tape gets.
- **THE GUITAR ANSWERS** (v3, the last A): at every phrase end the nylon guitar answers the flute - a falling run down the chord's tones an octave up, four eighths in the bar's last two beats (F#5 C#5 Bb4 G4 over A13b9 ...).
- **THE NEW PALETTE** (v11): a LADDER BASS in the drop (a saw and a sine through chirp's Moog-style ladder at q 10, an envelope opening it on each note, growling under the seasick chords). COMBED BRUSHES in the switch-up (the sweeps through a comb tuned two octaves above each chord's root: they sing Bb A Ab G). A HUMMED VOCAL resampled and chopped: a shadow song has the voice engine hum the sigh ("mm-oo", tape-worn), and a sampler cuts it into eight one-beat slices that answer the vibes in the first A section.
- **THE TAPE WEARS OUT** (v12, the tape deck's new `warp`): the keys' tape (wow 8, flutter 2, drift) follows a wear lane across the song, near-new in the intro, loosening through A, the switch and A2, seasick at the drop's end, still worn after it. THE HUM, BACKWARDS: the hummed sigh plays once more at A3's end, and `chop` replays it in the outro as reversed slices (`r7 r6 . r4 _ r2 r1 r0`).
- **THE HUM SCATTERS** (v13, per-voice fx): every hummed chop carries its own effects: a pan from its random value (each slice somewhere new), a crush that bites harder the harder it is played, and a low-pass that opens with velocity. The chops become voices around the room instead of one line.
- **THE TAPE RUNS BACKWARDS** (t7 v4): a shadow song (`songs: loopsrc`) renders 24 beats of t7's own bowed-vibes and tape-piano loops. After the door closes, a sampler plays it reversed, an octave down at half speed, from beat 152 to the end: the loops swell in backwards as the real ones leave.
- **THE BACKWARDS TAPE, CHOPPED** (t7 v5; wM's `chop` fx): the reversed loops are cut every two bars into eight one-beat slices and replayed rearranged (`0 r1 2 . r4 5 _ r7`: some slices flipped forwards again, the live tape once, a beat of silence). The backwards swell stutters and catches.
- **THE LOOPS WANDER IN SPACE** (t7 v6; per-voice fx): the bowed vibes and the whistle carry a per-voice pan read from each note's random value, so every pass of a loop lands somewhere new in the room. The tape piano and the pad now enter together (beat 26) and leave together (beat 170).

