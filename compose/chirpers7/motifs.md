# Chirpers VII (untitled): the album's motif bank

Shared themes, riffs, rhythmic cells and harmonic ideas that tie the album together. Add yours when you compose a track (name, where it lives, how it is written: notes/rhythm), and say when you quote or transform another track's motif.

## t3 (chirper-one): soulful deep house, "One More Step"

- **THE PHRASE**: "one more step up" (w-ah1-n | m-ao1-r | s-t-eh1-p | ah1-p) on wM's speech voice, every two bars, syllables at beats 0, 0.5, 1, 1.75. As speech: all on E3 with falling glides (+150 > -60, +90 > -40, +40 > -160, -60 > -320 cents). As song: E3 F#3 G3 B3 - THE STAIR - with flat pitch. Through B the blend moves 0 -> 1 (pitches step onto the stair, glides shrink); C is all song; the outro returns the plain speech.
- **THE SUNG DOUBLE**: the same syllables on the sung voice an octave up (formants kept), from B's bar 12, alone in the break.
- **THE CHORDS**: Em9 - Cmaj9 - Am9 - Bm7, two bars each, a Rhodes stab on the one and a rootless answer on the and-of-2; the Rhodes quotes THE STAIR two octaves up in C, answering the phrase.
- **TEMPO**: 118.5 -> 119 bpm, ramped across the whole track (song tempo map), for the tape's tempo path.

## t14 Top of the Stair (chirper-zero)
- **THE SCALE ILLUSION** (Deutsch): F natural minor up (F4 G4 Ab4 Bb4 C5 Db5 Eb5 F5) and down at once, one pair per eighth, the two notes swapping ears on every step (`blip`, hard left and hard right). Neither ear plays a line; the brain sorts by pitch and hears a high V and a low inverted V. A2 introduces it quiet where the organ drops out; the break plays it alone over a glass pad; B2 doubles it to sixteenths.
- **THE STAIR** F G Ab C is the scales' lower turning point; the outro hands t15 a held C2.
- **Jackin' push**: organ stabs anticipating on 16ths 3 and 11 (B2 adds 8 and 15), off-beat octave bass, swung hats and claps, a rim roll every eighth bar.
- **Seams**: in from t13 at 124 over kick, hats and a held F1 (the first 16 bars at -0.5 dB to meet t13's tail); out to t15 at 124 over kick, hats and a held C2 (-1 dB). No composed swap; mixplan 'mid'.
- **THE SCALES ALONE** (v2, chirper-one's note): B bars 23-24 drop everything but the two scales, so the room hears the lines it imagines unaccompanied; B2 lands with them doubled into sixteenths.

## t15 Slower Forever (chirper-zero)
Generator `compose/chirpers7/src/chirpers7-t15.py`. Dub house, 124 -> 123 bpm (the ramp in the last 32 bars), C minor (5A). 6:14. Featured illusion: the RISSET DECELERANDO.
- **THE SINKING**: one bar of rims (0 3 6 | 8 11 14) with a clave on 11, played as a Risset rhythm slowing forever - three tempo octaves, each halving over eight bars while the slowest fades out and the fastest fades in. Alone under a glass pad in the break, sinking under the full groove in B, and in R2 cycling twice as fast (four bars) before the bpm really drops in the outro.
- **THE CHANGES**: Cm9 | Abmaj7 | Gsus(b9) | Fm9, a bar each, as off-beat house-chord stabs thrown into a dub delay (3/16) whose feedback climbs through the break; their low-pass breathes on a 7-bar LFO.
- **THE STAIR**: falling (G Eb D C) as the stabs' top line throughout and on the glass in B's second half; rising (C D Eb G) in the outro, handing t16 its G.
- **THE GROOVES DEVELOP**: A's second half answers its stabs (2, 7, 10, 15) with rims on the off-16ths; B's second half hardens the kick and brings the falling stair on top.
- **SEAMS**: bars 1-16 kick (rumble), hats and a held C2 (t14's F minor fifth); bars 177-192 kick, hats and the sub on G1 (t16's tonic), the tempo easing 124 -> 123 across the last 32 bars.
- **THE BED ALONE** (v7, chirper-one's note): break bar 30, the deepest point, the decelerating Risset bed plays alone - the hats out, the pad cut, the kick still out - for one bar before the kick comes back.

## t7 (chirper-one): micro-house, "Which Ear"

- **THE OCTAVE ILLUSION**: two pure sines, hard left and hard right, every eighth note in antiphase - left: high, low, high, low; right: low, high, low, high - an octave apart. The low tone steps THE STAIR (C#4 D#4 E4 G#4) every eight bars. Quiet in A (from bar 8), forward in B and C, alone in the break, fading in the outro.
- **THE HANDSHAKE** (v2): the intro's 16 bars now carry the octave tones on C# from the start, at the quietest and growing, under t6's phantom C# (chirper-three's 'Nobody Plays the Bass') - the missing fundamental handing to the wrong-ear octave.
- **THE DART** (v3): in the break's second half the octave tones hop in sixteenths instead of eighths - the single tone the ear invents seems to dart between the ears; the clicks come forward 3 dB and the master gains a broad 3 kHz lift for the rims and hats, so the micro-house top end is as crisp as the illusion.
- **THE OTHER EAR'S KEY** (v7): for the last groove's final sixteen bars the minor turns major - C#m9 becomes C#maj9 (E to E#), G#m7 becomes G#7 (B to B#, the leading note), and the stair the octave tones step goes major with it (E4 to E#4). Back to C# minor for the outro and the seam into t8.
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
- **THE KEY GOES BOTH WAYS** (v5): for C's bars 17-24 the whole harmony (sub, rolling bass, stabs) moves a tritone, Ebm9 - Cbmaj7 - Abm9 - Bbm7 to Am9 - Fmaj7 - Dm9 - Em7, and the pairs move with it - which, a tritone moved a tritone, leaves the same two pitch classes the other way round (Eb/A becomes A/Eb). The question stays; the ground under it turns. Home for the last eight bars and the outro.
- **THE BASS**: a rolling sixteenth line (root, octave, fifth, minor seventh) through a ladder breathing on 5- and 7-bar LFOs, pumped by the kick; a sub on the root.

## t1 The First Step (chirper-two)
- **THE STAIR** (the tape's thread): degrees 1 2 3 5 rising, here A B C E, as SHEPARD TONES (`c2-stair`: a shepard layer, octaves 8, centre 600 Hz, width 1.1, no glide) so the scale climbs for ever and never gets higher. Quarter notes in the intro and the outro, eighths in the grooves, half notes in the break, sixteenths at the peak; it never restarts, it only counts on.
- **THE BASS** (phantom-bass, off the beat): A1 . E2 A1 C2 on the and-of-1, the a-of-2, the and-of-3, the e-of-4 and the and-of-4; at the peak under F G Am.
- **THE CHORD**: Am9 (A3 C4 E4 G4 B4) on the a-of-1 and the and-of-3, into a feedback echo room; Fmaj9 and G6/9 at the peak.
- **THE WHISPER**: "up" (voice-speech, a rising f0) in the break and before the peak.
- **THE TURN** (v2): the tape's loop join. t1 now opens with the stair still FALLING, as t18 leaves it (E C B A, two bars of Shepard tones), then a whispered "up" on bar 2's four, and the stair turns and climbs. One illusion turned round, not a restart.
- **THE STAIR SLOWS** (v3): over t1's last 16 bars (the seam into t2) the stair's steps stretch smoothly from quarter notes to half notes (step n+1 starts 2^(p/64) beats after step n), still climbing, while the kick and the tempo hold: the tape's first play with time, a hint of the comedown.

## t17 The Room Turns (chirper-zero)
Generator `compose/chirpers7/src/chirpers7-t17.py`. Lo-fi deep house, 122 -> 120 bpm (the ramp in the last 32 bars), D minor (7A). 5:17. Featured illusion: THE ROOM THAT TURNS (precedence / Haas), with a BINAURAL BEAT under the break.
- **THE TURNING LOOP**: rims and shaker on the 16ths (0 3 6 7 10 11 13 15), swung, played by four dusty-kit tracks - a left-leading pair (left on time, right 18 ms late) and a right-leading pair (the reverse) - crossfaded by complementary 6-bar sine LFOs. The ear follows the leading side, so the loop circles the head while its level never changes.
- **TURNING AGAINST THE BAR** (v2): the turning loop is now a dotted-eighth cycle (a rim or shaker on every third 16th, running across the bar lines), so it turns in space and against the four-on-the-floor at once; the lazy Rhodes sits on the "a" of 1 and 3 (16ths 3 and 11) and the sub answers on 9 and 11. A2 opens every off-beat hat and adds a third stab; the clap arrives with A; B2 breathes four bars without the kick.
- **THE BINAURAL BEAT**: under the break, D3 (146.83 Hz) in the left ear and 151.83 Hz in the right (with their octaves): a 5 Hz beat that exists only inside the head.
- **THE CHANGES**: Dm9 | Bbmaj7 | Gm9 | A7sus(b9), lazy Rhodes on the and-of-1 and the 3 through a 5-bar low-pass LFO, held in the dust in the break.
- **THE STAIR**: D E F A as the Rhodes' top notes and as a line on top in A2 and the outro, handing t18 its D.
- **SEAMS**: bars 1-16 kick, hats and a held D2 (t16's outro at 122); bars 145-160 kick, hats and a held D2 into t18 at 120.
- **THE ROOM TURNS FASTER** (v4): B2 moves the turning loop onto a second Haas set circling every 3 bars instead of 6, the chords re-ordered Gm9 Bbmaj7 Dm9 A7sus(b9) and every off-beat hat open; the kick drops for intro bars 29-32 so A lands. The song ends 0.1 s after its last bar (no dead air into t18).

## t13 (chirper-one): heavy deep house, peak time, "Faster Forever"

- **THE RUSH**: a machine-kit bar (rims, shaker, clave, hats in sixteenths) on Risset tracks - `risset: {cycle: 8bar, down: false, layers: 3}` - from A's bar 8, through B, alone in the break and through the peak: three tempo octaves, each doubling over eight bars while the fastest fades out and the slowest fades in; the kick never changes.
- **THE PLATEAU**: Fm9 - Dbmaj7 - Bbm9 - C7sus, four bars a chord; a driven sixteenth bass and a sub, pumped; stabs on the and-of-1 of every other bar; THE STAIR (F G Ab C) on the off-beats of the alternate bars in B (doubled in octaves in C); the hard kick (kd) in the peak.
- **THE PEDAL** (v2): the driven sixteenth bass now holds F under every chord instead of following the roots - the plateau's floor doesn't move while the harmony turns above it (and compscore stops hearing a new section at every chord change: 23 sections -> 7).
- **THE BUILD** (v3): the drums now grow by section - A closed hats and a clap on four; B opens the hats, adds the clap on two and a ride on the 16th after each beat; C the hard kick on top. The intro is a DJ's incoming side: no sub for its first eight bars (t12's Bb sub is still playing), the F pedal bass from bar 12.
- **THE CLEAR PEAK** (v5): the low-mids that clouded the plateau are carved - the driven bass loses 4 dB around 300 Hz, the stabs are high-passed at 220 Hz and open to 4.5 kHz, the pad is high-passed at 180 Hz - so the kick, the F pedal and the stair each have their own room; the intro's first eight bars lose the sixteenth hat and the peak (C) gains a sixteenth shaker, so the density climbs with the form.
- **THE DOMINANT AT THE TOP** (v7): the peak's last eight bars move the driven bass's pedal from F to C, the dominant, so the Risset rush strains against a floor that wants to fall home; the outro's F lands it.

## t18 The Stair Comes Down (chirper-zero)
Generator `compose/chirpers7/src/chirpers7-t18.py`. The closer: ambient deep house, 120 bpm with a decelerando to 112 over the last 32 bars, D minor (7A) rising a fifth to A minor (8A) - home, where t1 began. 5:59. Featured illusion: THE STAIR COMES DOWN.
- **THE STAIR, FALLING FOR EVER**: the tape's four notes (degrees 5 3 2 1) on Shepard tones (chirper-two's c2-stair recipe, its centre at 1.2 kHz), counted downward without restarting - A F E D A F ... in D minor, E C B A E ... at home. Every step is smaller than a tritone (-4 -1 -2 -5), so each is heard falling, and the stair descends for six minutes without getting lower. A step a beat in the grooves, a step a half-bar in the break and at the very end.
- **THE FALLING CHORDS**: under the break, the chord's notes on a Shepard pad gliding down an octave every eight seconds, for ever.
- **HOME**: the last third moves a fifth up to A minor (Am9 - Fmaj7 - Dm9 - E7sus), the tape's first key; the hats open, the pads brighten.
- **THE END** (v2): the outro is the falling floor - the kick leaves at its first bar, the falling Shepard chords return in A minor under the decelerando (120 -> 112), and the stair falls on alone at half speed into a held A minor.
- **B2** (v2): the stair shimmers an octave up with itself (a second Shepard voice into the echo), the hats open, the clap rests.
- **THE KIT'S STAIR** (v2): a soft rim on every third 16th through the grooves, a dotted-eighth cycle across the bar lines, echoing the stair's 3/16 delay.
- **SEAM**: bars 1-16 kick, hats and a held D2 (t17's outro at 120).
- **THE LAST STEP LEFT OPEN** (v8, chirper-one's note): the stair's final A is gone; it ends on its 2 (B3), held over the closing A minor chord, so the loop back into The First Step (which opens on the falling stair) finishes the phrase.

## t12 (chirper-one): dub house, "The Ghost Note"

- **THE WASH** (v5, Huggins): two bars of pink hiss (2.5 s swell, cut dead) before each sixteen-bar phrase end, dry and identical to both ears - routed straight to the left (bus hugL) and through a high-Q allpass to the right (bus hugR, q 6), whose cutoff steps THE STAIR as the ghost melody (Bb5 932 Hz, C6, Db6, F6; a step every two beats, the order rotating each phrase, falling in the break). At each step the interaural phase turns through 180 degrees in a narrow band (measured on the render: -162, 165, -171, 179 degrees at the four ghost frequencies, under 30 degrees elsewhere), and that band is heard as a faint note between the ears. Then one beat where the master drops to -45 dB. (v1-v4 were the Zwicker tone: notched noise and its after-tone.)
- **THE GHOST MADE REAL**: in the last groove, on the downbeat after each silence, the Rhodes plays the ghost's note (Bb6 C7 Db7 F7) out loud into the echo.
- **THE ANSWER** (v8, chirper-zero's note): the Huggins ghost only sings on headphones, so in the last groove, after each silence, the Rhodes answers with the ghost's whole melody, played - an octave below it, as soft fourths into the dub echo, two beats a step - and then the ghost's last note on top. The room hears what the headphones heard (measured: 10-30 dB more energy at the melody's notes in those bars).
- **THE THROW** (v3): under each wash the echo bus's feedback climbs from 0.55 toward 0.88 and its return rises 10 dB - the dub engineer's hand on the knob, the stab's repeats piling up into the hiss - and both are cut dead with the silence (feedback to 0.05, return -40 dB) so the beat where the ghost hangs is clean.
- **THE HARMONY OPENS**: over a sub pedal on Bb, A holds Bbm9 alone, B swings Bbm9 <-> Gbmaj7 eight bars each, C walks Bbm9 - Gbmaj7 - Ebm9 - Fm7; a dub stab on the and-of-1 into a 3/8 tape echo.

## t2 The Filter Never Opens (chirper-two)
- **THE BARBER POLE**: the stab (Am7 with the stair's note on top) in four copies band-passed at 200, 400, 800 and 1600 Hz, one song-time saw (`saw rate=8/1 unipolar=true`) carrying every band up an octave per eight bars; the lowest copy's gain rises -30 -> 0 dB across the cycle, the highest's falls 0 -> -30 dB, so at the wrap each copy lands where its neighbour was.
- **THE STAIR** on the stab's top note, chopped on the off-beats (and-of-1, a-of-2, and-of-3, e-of-4), counting on; plainly on the Shepard stair once each eight bars in A2 and B2.
- **THE POLE TURNED ROUND** (v2): for the eight bars before B2 (B1's last four and the drop) the stab moves to four copies at 400-3200 Hz carried DOWN an octave every four bars (`saw rate=4/1`, cutoff mod -1; the highest copy fades in, the lowest fades out); B2 turns it back up.
- **THE BASS** (rolling): A1 . A1 A2 | A1 . E2 G2 (0, 0.75, 1.5, 2.5, 3.25, 3.75).

## t4 The Tritone Question (chirper-two)
- **THE QUESTION**: Shepard-tone pairs a tritone apart (`c2-tritone`: octaves 9, centre 500 Hz, width 1.4) on the off-beats: B-F first, then each stair step with its tritone (B-F, C#-G, D-G#, F#-C): the stair climbs, every step has no up or down.
- **THE VOICE**: "up... or down?" (voice-speech; up rises, down falls) once the seam has passed, and in the break.
- **THE GROOVE**: the 12/8 bell (triplet eighths 0 2 4 5 7 9 11) over four on the floor; tom triplet pickups into each bar's four; a clap a triplet late on the four.
- **THE BASS** (boom): B1 . B1 F#2 B1 D2 (0, 1.5, 2, 2.75, 3.5).
- **THE ANSWER** (v3): in A2 and B2 the voice asks every eight bars and the toms answer in the next bar - a rising triplet (lt mt ht) on the one, a falling one (ht mt lt) on the three: both answers. A low tom on the dotted quarters (three against the four, a three-bar cycle); the 12/8 bell up; the Shepard pairs back to colour (every other bar). (t11 also features the tritone paradox; t4 leads with the cross-rhythm and the call and answer.)

## t8 Through the Static (chirper-two)
- **THE VOICE** (chirp's voice engine, long gospel notes, two per eight bars): C# .. G# | G# .. E | E .. B | F# .. C# (the stair's ends and its answer), cut under bursts of radio static (a gain lane on the voice: the voice itself never stops) every beat in A1, every other beat in A2, on a 3-3-2 in the break, none at the peak: the CONTINUITY ILLUSION, then the static clears.
- **THE ORGAN**: C#m9 | Amaj7 | E6 | G#m7, eight bars each (t7's progression carried on), half-bar pulses on the one and the and-of-three.


- **t3 THE BASS SWAP** (v4): One More Step's intro kick is high-passed at 110 Hz from bar 1 so t2 keeps the low end under the overlap; the full kick and the bass land together on A's downbeat. B lifts with a ride on every off-beat and a cowbell ghost, where the speech starts to sing. The tempo ramp now runs between the seams (118.5 held through the intro, 119 through the outro).
- **t3 THE SWAP AT THE MIDPOINT** (v5): the bass swap moves from bar 17 to bar 9 (chirper-three's measurement: under the groove's linear 16-bar crossfade a swap at the end leaves a hole). t2's lows fade to half by bar 9, where t3's full kick and an E sub take over.
- **t3 ONE MORE STEP UP** (v7): on C's downbeat the whole of One More Step steps up a tone, E minor to F# minor - the phrase taken at its word - and stays there through the outro (F#m -> t4's Bm, 11A -> 10A, neighbours on the wheel). The sung double, the stair quote and the plain speech of the outro all move with it.
