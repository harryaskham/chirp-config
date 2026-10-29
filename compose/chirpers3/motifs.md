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
- **ROLLED LOOP** (tape-piano, each note ~18 ms after the last): Fm9 Abmaj9 | Eb6/9 Dbmaj9 | Fm9 Bbm11 | C7#9 C7b9.
- **THE HOOK** (boc-lead): a 2-bar phrase, C5 Eb5 C5 Bb4 | Ab4 Bb4 G4, the second pair of bars a step lower.

## t5 Low Pressure (chirper-zero)
Generator `compose/chirpers3/src/chirpers3-t5.py`. Dub-wise space, 70 bpm one-drop, A minor.
- **RIDDIM** (sub bass, 16th grid): `A1~ . . A1 . . C2~ . E2~~ . . . D2~ C2~ | D2~ . . D2 . . F2~ . A1~~ . . C2 E2~ G1~`; the B part on Fmaj7 | E7sus. In the version every other bar DROPS THE ONE (its first note left out).
- **ONE-DROP + STEPPERS HATS**: kick and rim together on 3 only; the hats on a 3+3+2 sixteenth cell (0 3 6 | 8 11 14) dragged by an eighth swing (0.64); rim ghosts; a rim roll into every fourth bar.
- **SKANK + BUBBLE**: rhodes stabs on beats 2 and 4 into the spring; a wurli bubble on the e-and-a's.
- **THE CALL** (boc-lead, a melodica-ish voice): eight bars of A minor pentatonic, `E5 . C5 D5 E5~ | . D5 C5 A4~ | G4 A4 C5 E5 G5 | F5. E5 D5~ | E5~~~ | A5 G5 F5 E5 D5 | C5 A4 G4 E4 | A4~~~`, each four-bar phrase THROWN into the echo on its last off-beat.
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

