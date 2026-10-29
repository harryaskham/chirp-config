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
- **ROLLED LOOP** (tape-piano, each note ~18 ms after the last): Fm9 Abmaj9 | Eb6/9 Dbmaj9 | Fm9 Bbm11 | C7#9 C7b9.
- **THE HOOK** (boc-lead): a 2-bar phrase, C5 Eb5 C5 Bb4 | Ab4 Bb4 G4, the second pair of bars a step lower.

## t5 Low Pressure (chirper-zero)
Generator `compose/chirpers3/src/chirpers3-t5.py`. Dub-wise space, 70 bpm one-drop, A minor.
- **RIDDIM** (sub bass, 16th grid): `A1~ . . A1 . . C2~ . E2~~ . . . D2~ C2~ | D2~ . . D2 . . F2~ . A1~~ . . C2 E2~ G1~`; the B part on Fmaj7 | E7sus. In the version every other bar DROPS THE ONE (its first note left out).
- **ONE-DROP + STEPPERS HATS**: kick and rim together on 3 only; the hats on a 3+3+2 sixteenth cell (0 3 6 | 8 11 14) dragged by an eighth swing (0.64); rim ghosts; a rim roll into every fourth bar.
- **SKANK + BUBBLE**: rhodes stabs on beats 2 and 4 into the spring; a wurli bubble on the e-and-a's.
- **THE CALL** (boc-lead, a melodica-ish voice): eight bars of A minor pentatonic, `E5 . C5 D5 E5~ | . D5 C5 A4~ | G4 A4 C5 E5 G5 | F5. E5 D5~ | E5~~~ | A5 G5 F5 E5 D5 | C5 A4 G4 E4 | A4~~~`, each four-bar phrase THROWN into the echo on its last off-beat.
- **THE ANSWER** (v2): THE CALL is answered by itself - a second boc-lead, softer and panned opposite into the spring, plays the melodica's line a dotted eighth late, so every phrase has its echo written into the arrangement as well as thrown into the tape delay.
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
- **THE WIND-UP** (since v4, the intro; answering Harry's 8.0 note on the ending's "glitch resample"): the key is
  turned: bar by bar the gears' cycles shorten (toy 10..5, box 17..7) and the pitches rise from three semitones flat
  to true. And a **NEAR-STALL** at the glitch break's last bar: the gears slow and sag a tone within one bar, the beat
  drops out after beat 2, then the return snaps back at speed.
- **THE WIND-DOWN** (since v3, the outro): the music box RUNS DOWN: bar by bar each gear's cycle lengthens (toy
  5..10, box 7..17, crystal 4..9 sixteenths), the pitches sag a semitone every two bars, the notes fade, the beat gives
  out at bar 55; the last sound is one music-box note three semitones flat.
- **THE BASS ANSWERS** (since v3): the root, a reply on the swung and-of-3 (the fifth, or the ninth up high on
  alternate chords), then a chromatic walk down into each change.
- **HAIL**: in the glitch break the toy's notes are torn into falling 32nd retriggers, 3-6 at a time, between music-box
  answers.
- Harmony: Dbmaj9 | Cm7(11) | Fm9 | Bbm9, two bars each; 86 bpm; a 16th swing of 0.58 on the beat only.


## t2 Streetlight Hiss (chirper-one)
Generator `compose/chirpers3/src/chirpers3-t2.py`. Trip-hop noir, 72 bpm half-time.
- **THE LONG DESCENT**: Cm9 - Bb6 - Abmaj7 - G7b9 (i bVII bVI V) spread over the whole song, the strings' top voice falling C Bb Ab G; the last four bars of B2 lift a minor third (Ebm9 ... Bb7b9).
- **THE CLIMB**: the gliding boc-lead (180 ms glide, each note scooped from a step below) rises G Ab Bb B against the descent, an octave up in B2.
- **HALF-TIME BREAK**: lofi-kit pitched down 3 semitones; swung eighths (58%); kick 1, 2&, 3&; snare on 3, 28 ms late; ghost snares on 1&, 4, 4&.
- **THE DROP**: one bar of strings and crackle alone before each return.
- **THE CELLO** (v3, B and B2): a counter-line rising against the strings' fall - Eb3, F3, G3, then Ab3 (the b9) over the G7 - one note a bar with a neighbour a step below on beat 4.

## t10 When the Tape Runs Out (chirper-one), the closer
Generator `compose/chirpers3/src/chirpers3-t10.py`. Chillwave dusk, 78 bpm.
- **DUSK CHORDS**: Dmaj9 Bm11 Gmaj7#11 A6sus, two bars each, on a juno pad ducked by the kick and warbling on tape.
- **THE VOX LINE** (dream-vox): F#4 A4 | B4. A4 | G4 F#4 | E4 -- , answered higher: A4 B4 | D5. C#5 | B4 A4 | F#4 --.
- **THE RUN-OUT**: after the full band each section loses one voice - the kick, then the arp, then the bass - until the vox and pad are alone; the tape stops over the last four beats.
- **DOTTED CLAVE**: a clave every 3 sixteenths, the cycle crossing two bars, from A through the first run-outs; the arp's 3/16 tape echo.
- **THE LAST WORD** (v2): over the bare pad in the end, as the tape begins to sag, the vox sings its first phrase once more, softer each bar.

## t8 Window Seat (chirper-zero)
Generator `compose/chirpers3/src/chirpers3-t8.py`. Night-bus 2-step, 136 bpm, F# minor.
- **SKIP** (the 2-step bar, 16th grid, swung 0.7): kick on 1 and a SKIP-KICK that wanders bar by bar (step 10, 11 or 7), claps on 2 and 4, hats on the off-16ths with gaps, a shaker on a 3-sixteenth cycle running across the bar lines (the garage cross-rhythm), rim rolls into every eighth bar; the sub follows the two kicks.
- **NIGHT LOOP**: F#m9 | Dmaj9 | Bm11 | C#7sus on a juno pad through wM's tape deck; THE STOP's loop Dmaj9 | E6/9 | C#m7 | Bm9.
- **THE CHOPS** (a song-local voice: chirp's voice layer with a short tract, fast attack): one-syllable fragments - la / mo / ye - in a falling three-note cell (the chord's 9th, 5th, 3rd) on the off-beats after the claps, the third held; an octave up in the last groove.
- **THE STOP** (groove 2): the bus idles - half-time (kick on 1, a rim on 3), rhodes chords instead of the pad, the B loop, the chops on every clap.
- **RESAMPLED, no WAVs** (v10): shadow songs inside t6 (`songs: bounce, bounceb`, never played as tracks) render four wurli bars through tape, and patches sample them.
  - The SWITCH-UP plays `bounceb` (its own chords, rendered an octave up) an octave down. Tape-style, that is half speed: four bars fill the switch's eight. It plays forwards for four bars, then the same tape BACKWARDS, the chords swelling in.
  - A3's off-beats CHOP `bounce` (the A loop) into eight half-bar slices, MPC-style, each bar playing the slice of its own chord.

