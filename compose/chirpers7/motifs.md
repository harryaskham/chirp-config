# Chirpers VII (untitled): the album's motif bank

Shared themes, riffs, rhythmic cells and harmonic ideas that tie the album together. Add yours when you compose a track (name, where it lives, how it is written: notes/rhythm), and say when you quote or transform another track's motif.

## t3 (chirper-one): soulful deep house, "One More Step"

- **THE PHRASE**: "one more step up" (w-ah1-n | m-ao1-r | s-t-eh1-p | ah1-p) on wM's speech voice, every two bars, syllables at beats 0, 0.5, 1, 1.75. As speech: all on E3 with falling glides (+150 > -60, +90 > -40, +40 > -160, -60 > -320 cents). As song: E3 F#3 G3 B3 - THE STAIR - with flat pitch. Through B the blend moves 0 -> 1 (pitches step onto the stair, glides shrink); C is all song; the outro returns the plain speech.
- **THE SUNG DOUBLE**: the same syllables on the sung voice an octave up (formants kept), from B's bar 12, alone in the break.
- **THE CHORDS**: Em9 - Cmaj9 - Am9 - Bm7, two bars each, a Rhodes stab on the one and a rootless answer on the and-of-2; the Rhodes quotes THE STAIR two octaves up in C, answering the phrase.
- **TEMPO**: 118.5 -> 119 bpm, ramped across the whole track (song tempo map), for the tape's tempo path.

## t15 Slower Forever (chirper-zero)
Generator `compose/chirpers7/src/chirpers7-t15.py`. Dub house, 124 -> 123 bpm (the ramp in the last 32 bars), C minor (5A). 6:14. Featured illusion: the RISSET DECELERANDO.
- **THE SINKING**: one bar of rims (0 3 6 | 8 11 14) with a clave on 11, played as a Risset rhythm slowing forever - three tempo octaves, each halving over eight bars while the slowest fades out and the fastest fades in. Alone under a glass pad in the break, sinking under the full groove in B, and in R2 cycling twice as fast (four bars) before the bpm really drops in the outro.
- **THE CHANGES**: Cm9 | Abmaj7 | Gsus(b9) | Fm9, a bar each, as off-beat house-chord stabs thrown into a dub delay (3/16) whose feedback climbs through the break; their low-pass breathes on a 7-bar LFO.
- **THE STAIR**: falling (G Eb D C) as the stabs' top line throughout and on the glass in B's second half; rising (C D Eb G) in the outro, handing t16 its G.
- **THE GROOVES DEVELOP**: A's second half answers its stabs (2, 7, 10, 15) with rims on the off-16ths; B's second half hardens the kick and brings the falling stair on top.
- **SEAMS**: bars 1-16 kick (rumble), hats and a held C2 (t14's F minor fifth); bars 177-192 kick, hats and the sub on G1 (t16's tonic), the tempo easing 124 -> 123 across the last 32 bars.


## t7 (chirper-one): micro-house, "Which Ear"

- **THE OCTAVE ILLUSION**: two pure sines, hard left and hard right, every eighth note in antiphase - left: high, low, high, low; right: low, high, low, high - an octave apart. The low tone steps THE STAIR (C#4 D#4 E4 G#4) every eight bars. Quiet in A (from bar 8), forward in B and C, alone in the break, fading in the outro.
- **THE HANDSHAKE** (v2): the intro's 16 bars now carry the octave tones on C# from the start, at the quietest and growing, under t6's phantom C# (chirper-three's 'Nobody Plays the Bass') - the missing fundamental handing to the wrong-ear octave.
- **THE DART** (v3): in the break's second half the octave tones hop in sixteenths instead of eighths - the single tone the ear invents seems to dart between the ears; the clicks come forward 3 dB and the master gains a broad 3 kHz lift for the rims and hats, so the micro-house top end is as crisp as the illusion.
- **THE CLICKS**: machine-kit rims and tiny hats in two alternating skippy sixteenth patterns, odd sixteenths 0.03 beat late; a stutter on the clicks over the last beat of every eighth bar of B and C, on the same swing (swing 0.56).
- **THE CHORDS**: C#m9 - Amaj7 - E6 - G#m7, a dub stab on the and-of-1 and a rootless answer on the and-of-3, every other bar in B and C; a sub (with phantom harmonics) on the root.

## t16 Never Arrives (chirper-zero)
Generator `compose/chirpers7/src/chirpers7-t16.py`. Rolling hypnotic minimal house, 123 -> 122 bpm (the ramp in the last 32 bars), G minor (6A). 5:46. Featured illusion: THE ENDLESS FILTER (barber-pole).
- **THE ENDLESS FILTER**: a 16th chord pulse (house-chord) through three parallel band-passes; each cutoff climbs five octaves on a saw (160 Hz -> 5 kHz) a third of a cycle apart, while each copy's level swells in at the bottom and fades at the top on a sine - a Shepard tone made of a filter sweep, a house build that rises for ever and never arrives. Its cycle is 16 bars in the build and the break (where it plays alone), 8 in A, 4 in A2 and B; in B2 it stops for eight bars and resumes.
- **THE ROLL**: the sub on the 16ths around the beat (2 3 6 10 11 14), its notes the chord's stair (1 2 3 5); in B the octave jumps; in B2 it drops out for four bars and comes back climbing.
- **THE CHANGES**: Gm9 | Ebmaj7 | Cm9 | D7sus(b9), a bar each.
- **THE STAIR**: falling (D Bb A G) as stabs over B2; rising (G A Bb D) in the outro, handing t17 its D.
- **SEAMS**: bars 1-16 rumble kick, hats and the sub holding G1 (t15's outro, at 123); bars 161-176 rumble kick, hats and a held D2 (t17's tonic), 123 -> 122.


## t11 (chirper-one): modern minimal, "Both Ways"

- **THE PAIRS**: Shepard tones (8 octave-spaced partials under a Gaussian envelope, width 1.1 octaves) - each bar a step of THE STAIR (Eb, F, Gb, Bb; a step every eight bars) on the one for a dotted quarter, answered by its tritone (A, B, C, E) on the and-of-2; in B and C every other bar adds the pair reversed on the four.
- **THE TURN**: two copies of the pairs - envelope centred at 250 Hz and at 1 kHz - cross-faded by gain lanes: low alone in A, low -> high through B, high alone in the break (where the Shepard position glides up an octave), both at once in C, low in the outro.
- **THE BASS**: a rolling sixteenth line (root, octave, fifth, minor seventh) through a ladder breathing on 5- and 7-bar LFOs, pumped by the kick; a sub on the root.

## t1 The First Step (chirper-two)
- **THE STAIR** (the tape's thread): degrees 1 2 3 5 rising, here A B C E, as SHEPARD TONES (`c2-stair`: a shepard layer, octaves 8, centre 600 Hz, width 1.1, no glide) so the scale climbs for ever and never gets higher. Quarter notes in the intro and the outro, eighths in the grooves, half notes in the break, sixteenths at the peak; it never restarts, it only counts on.
- **THE BASS** (phantom-bass, off the beat): A1 . E2 A1 C2 on the and-of-1, the a-of-2, the and-of-3, the e-of-4 and the and-of-4; at the peak under F G Am.
- **THE CHORD**: Am9 (A3 C4 E4 G4 B4) on the a-of-1 and the and-of-3, into a feedback echo room; Fmaj9 and G6/9 at the peak.
- **THE WHISPER**: "up" (voice-speech, a rising f0) in the break and before the peak.

## t17 The Room Turns (chirper-zero)
Generator `compose/chirpers7/src/chirpers7-t17.py`. Lo-fi deep house, 122 -> 120 bpm (the ramp in the last 32 bars), D minor (7A). 5:17. Featured illusion: THE ROOM THAT TURNS (precedence / Haas), with a BINAURAL BEAT under the break.
- **THE TURNING LOOP**: rims and shaker on the 16ths (0 3 6 7 10 11 13 15), swung, played by four dusty-kit tracks - a left-leading pair (left on time, right 18 ms late) and a right-leading pair (the reverse) - crossfaded by complementary 6-bar sine LFOs. The ear follows the leading side, so the loop circles the head while its level never changes.
- **TURNING AGAINST THE BAR** (v2): the turning loop is now a dotted-eighth cycle (a rim or shaker on every third 16th, running across the bar lines), so it turns in space and against the four-on-the-floor at once; the lazy Rhodes sits on the "a" of 1 and 3 (16ths 3 and 11) and the sub answers on 9 and 11. A2 opens every off-beat hat and adds a third stab; the clap arrives with A; B2 breathes four bars without the kick.
- **THE BINAURAL BEAT**: under the break, D3 (146.83 Hz) in the left ear and 151.83 Hz in the right (with their octaves): a 5 Hz beat that exists only inside the head.
- **THE CHANGES**: Dm9 | Bbmaj7 | Gm9 | A7sus(b9), lazy Rhodes on the and-of-1 and the 3 through a 5-bar low-pass LFO, held in the dust in the break.
- **THE STAIR**: D E F A as the Rhodes' top notes and as a line on top in A2 and the outro, handing t18 its D.
- **SEAMS**: bars 1-16 kick, hats and a held D2 (t16's outro at 122); bars 145-160 kick, hats and a held D2 into t18 at 120.


## t13 (chirper-one): heavy deep house, peak time, "Faster Forever"

- **THE RUSH**: a machine-kit bar (rims, shaker, clave, hats in sixteenths) on Risset tracks - `risset: {cycle: 8bar, down: false, layers: 3}` - from A's bar 8, through B, alone in the break and through the peak: three tempo octaves, each doubling over eight bars while the fastest fades out and the slowest fades in; the kick never changes.
- **THE PLATEAU**: Fm9 - Dbmaj7 - Bbm9 - C7sus, four bars a chord; a driven sixteenth bass and a sub, pumped; stabs on the and-of-1 of every other bar; THE STAIR (F G Ab C) on the off-beats of the alternate bars in B (doubled in octaves in C); the hard kick (kd) in the peak.
- **THE PEDAL** (v2): the driven sixteenth bass now holds F under every chord instead of following the roots - the plateau's floor doesn't move while the harmony turns above it (and compscore stops hearing a new section at every chord change: 23 sections -> 7).

## t18 The Stair Comes Down (chirper-zero)
Generator `compose/chirpers7/src/chirpers7-t18.py`. The closer: ambient deep house, 120 bpm with a decelerando to 112 over the last 32 bars, D minor (7A) rising a fifth to A minor (8A) - home, where t1 began. 5:59. Featured illusion: THE STAIR COMES DOWN.
- **THE STAIR, FALLING FOR EVER**: the tape's four notes (degrees 5 3 2 1) on Shepard tones (chirper-two's c2-stair recipe, its centre at 1.2 kHz), counted downward without restarting - A F E D A F ... in D minor, E C B A E ... at home. Every step is smaller than a tritone (-4 -1 -2 -5), so each is heard falling, and the stair descends for six minutes without getting lower. A step a beat in the grooves, a step a half-bar in the break and at the very end.
- **THE FALLING CHORDS**: under the break, the chord's notes on a Shepard pad gliding down an octave every eight seconds, for ever.
- **HOME**: the last third moves a fifth up to A minor (Am9 - Fmaj7 - Dm9 - E7sus), the tape's first key; the hats open, the pads brighten.
- **THE END** (v2): the outro is the falling floor - the kick leaves at its first bar, the falling Shepard chords return in A minor under the decelerando (120 -> 112), and the stair falls on alone at half speed into a held A minor.
- **B2** (v2): the stair shimmers an octave up with itself (a second Shepard voice into the echo), the hats open, the clap rests.
- **THE KIT'S STAIR** (v2): a soft rim on every third 16th through the grooves, a dotted-eighth cycle across the bar lines, echoing the stair's 3/16 delay.
- **SEAM**: bars 1-16 kick, hats and a held D2 (t17's outro at 120).


## t12 (chirper-one): dub house, "The Ghost Note"

- **THE WASH**: two bars of pink noise (6 s attack, cut dead) before each sixteen-bar phrase end, through two stacked notch filters an octave-wide around a step of THE STAIR (Bb6 1865 Hz, then C, Db, F), then one beat where the whole master drops to -45 dB: the Zwicker after-tone hangs in that silence, near the notch's lower edge. Two more washes come alone in the break.
- **THE GHOST MADE REAL**: in the last groove, on the downbeat after each silence, the Rhodes plays the ghost's note (Bb6 C7 Db7 F7) out loud into the echo.
- **THE HARMONY OPENS**: over a sub pedal on Bb, A holds Bbm9 alone, B swings Bbm9 <-> Gbmaj7 eight bars each, C walks Bbm9 - Gbmaj7 - Ebm9 - Fm7; a dub stab on the and-of-1 into a 3/8 tape echo.
