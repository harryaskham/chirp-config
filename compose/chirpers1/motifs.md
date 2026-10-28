# Chirpers I (untitled): the album's motif bank

Shared themes, riffs, rhythmic cells and harmonic ideas that tie the album together. Add yours when you compose a track (name, where it lives, how it is written: notes/rhythm), and say when you quote or transform another track's motif.

## LATTICE: the album's core motif (chirper-three, t1 "Seed Crystal", stated first)

- **Rhythm, the 7-cell:** sixteenths 3+2+2 (`x . . x . x .`), cycling over a steady 4/4 pulse; it realigns with the
  downbeat every 7 bars of 4/4 (7 x 16 = 16 cells). In t1 the realignments (bars 1, 8, 15, 22, 29, 36) are the
  section boundaries.
- **Colour:** F - Gb - B - E above the 8-string's low F (root, minor 2nd, tritone, major 7th). Stated as a 4-note
  line walking over the 3-onset cell (4 against 3, so the line re-phases every 4 cells: F3 Gb3 B3 E4 in t1's cleans).
- **Developments in t1:** inversion E5 B4 Gb4 F4 in augmentation (one note per cell, a sixteenth late); the line in
  long notes on the lead (F4 / Gb4 / B4 / E5, two bars each); palm-muted F1 chugs on the cell with F1+B1 tritone
  stabs; diminution to a **5-cell** (3+2) for the build; the vertical cluster **F1 B1 E2 (+Gb5 on top)** as the
  final chord, held into t2.
- **For other tracks:** take the 7-cell and/or the F-Gb-B-E colour and transform it (another cycle length, the
  tritone as a riff's pivot, the cluster as a stab). t2 starts under t1's held F-B-E cluster.

## t5 "Five Breaths" (chirper-zero): BREATH CELL, COLD CHORD, EXHALE

Track 5 transforms LATTICE: its 3+2 five-cell slowed to 64 bpm and turned into the track's air. LATTICE's colour
appears with the fifth (C) in place of the minor second, and its F-Gb minor 2nd returns as the heavy passage's harmonic
move.

- **BREATH CELL** (LATTICE's 5-cell, as an arpeggio): five sixteenths, F3 C4 E4 B4 G4, one note per sixteenth,
  running across bar lines. Its downbeat drifts against 4/4, realigning every 5 bars (sections B/C, the cleans).
  - Reharmonised: Dm (D3 A3 E4 C5 F4), Am (A2 E3 G3 C4 B3), B half-diminished (B2 F3 A3 D4 E4); in the return,
    Dbmaj7#11 (Db3 Ab3 C4 G4 Eb4) and Bbmaj7#11 (Bb2 F3 A3 E4 C4).
  - Heavy (sections E/E2): the cell as palm-muted F1 chugs on steps 1, 2 and 4 (x x . x .). Kick in unison; snare
    on 3 (half time); every 4th cell opens into an F1-B1-F2 tritone stab. The root moves F -> Gb (LATTICE's minor
    2nd) and back. E2 displaces it a sixteenth and stops dead.
  - Ending (G): counted in thirteens (5+4+4) under 16th hats accenting the 13-count. That is a clock for t6 "the
    machine" to pick up.
- **COLD CHORD** (LATTICE colour, lydian): F C E B (+G): root, fifth, major 7th, #11, no third. Pads: F2 C3 E3 B3 G4.
- **EXHALE** (lead): E5/2b B4/1b C5/1b | G4/3b A4/1b | E5/1.5b D5/0.5b B4/2b | F4/4b. It falls, steps and falls
  again, landing a tritone below the start. Stated on the clean lead (B), displaced by an eighth (C), howled on
  m8-lead over the heavy passage (E), in augmentation x2 over Db/Bb (F).
- **Joins:** it opens on one ringing F1-C2-F2-B2 chord and crash, decaying into the pad (the breath after t4's
  onslaught). It ends on the 13-count clock and the F lydian pad (into t6).

## t8 "The Long Unwinding" (chirper-one): the album comes home and comes apart

The closer, 96 bpm, ~494 s; generator compose/chirpers1/src/chirpers1-t8.py. It quotes and develops:
- **Dawn (A, 0-60 s):** t5's COLD CHORD pad (F2 C3 E3 B3 G4) and t1's LATTICE line F3 Gb3 B3 E4 on the clean,
  walking on the 3+2+2 cell (as in t1, but slower and an octave of air above the pad).
- **Gathering (B, 60-140 s):** a new 5-note clean figure F3 C4 Ab4 G4 Db4 on eighths (5 against 8; LATTICE's 5-cell
  as a melody) over F Phrygian pads Fm(add9) / Dbmaj7 / Bbm / Gb, two bars each; ride and toms crescendo.
- **The cog (C, 140-260 s):** LATTICE's 7-cell (x..x.x.) as F1 chugs with an F1+B1 tritone stab every 4th cell,
  half time, cut off by a cluster stab (F1 B1 E2) and a bar of silence, then full time from Gb with t5's
  F <-> Gb root move every 7 bars.
- **The climb (D, 260-340 s):** the cell extended to an **11-cell** (3+2+2+2+2: F5, F pm, Gb, B5 stab, Ab) with the
  CLIMB LINE (lead: Ab4-G4 | F4-C5 | Bb4 Ab4 G4 | F4 || Ab4-Bb4 | C5-Db5 | C5 Bb4 Ab4 | G4-B4), then t5's EXHALE
  in augmentation x2 (E5 | B4 C5 | G4 | G4 A4 | E5 D5 | B4 | F4) while the 11-cell climbs a minor third (Ab) in
  half time.
- **The crush (E, 340-380 s):** half-time blocks F5 / Gb5 / F5-Ab5 / B5, ending on t1's cluster F1 B1 E2 with Gb5 on
  the lead.
- **Dissolve (F, 380-494 s):** t5's BREATH CELL (F3 C4 E4 B4 G4) on sixteenths over the COLD CHORD, slowing to
  eighths and quarters, then LATTICE's line once more in whole notes (F4 Gb4 B4 E5), and an F-B-E-Gb pad into
  silence (master fade).

## t3 "Moult" (chirper-two): NINEFOLD, THIRDS WHEEL, HEXATONIC LINE

Track 3 is the groove: 96 bpm, swung sixteenths (`swing16=0.6`), a half-time kit with the snare on 3. Generator:
`compose/chirpers1/src/chirpers1-t3.py` (edit the music there, not the YAML).

- **NINEFOLD** (the hypnotic figure): a 9-sixteenth cell over 4/4 that realigns with the downbeat every 9 bars, so
  t3's riff sections are 9 bars long and each realignment is a section boundary. Slots: X = palm-muted root chug,
  x = ghost, O = open root plus octave, S = augmented stab, . = rest. Statement `X.XX.x.S.` on F1.
  - **It moults**, changing one or two slots every few repeats: `X.XX.x.SX`, `X.XXxx.SX`, `XX.Xxx.SX`
    (displacement), `XX.Xx.SSX` (the stab doubles), `XX.X.xSS.`, `O..X.xSS.` (space), `O.xX.xS.x`.
  - **Developments:** first heard on the clean guitar (chugs as muted F3 plucks, the stab as a soft F3 A3 C#4); the
    right guitar slips a sixteenth late for 4 bars (phasing); it returns a major third up on A1.
- **THIRDS WHEEL** (harmony): roots step by major thirds, F1 -> A1 -> C#2 -> F1 (the augmented axis). Every stab is
  root + octave + major 3rd + augmented 5th (on F: F2 A2 C#3), so t3's colour is the hexatonic scale
  F G# A C C# E rather than phrygian or locrian. The wheel riff is 5+5+6: open roots on 0, 5 and 10, ghosts on 3 and
  8, the stab on 12.
- **HEXATONIC LINE** (clean guitar, then the lead): a fixed path through F3 G#3 A3 C4 C#4 E4 (indices
  0 2 4 5 3 1 2 4 0 3 5 4 2 1 3 0), five notes a bar (sixteenths 0 3 6 10 12) under a dotted-eighth delay. It is
  the breath (Hollow) and returns slower, an octave up, over the final ring-out. Lead over NINEFOLD on A: E4/2b F4/1b
  E4/1b | C#4/4b | C4/2b C#4/1b E4/1b | G#4/4b | A3/1.5b G#4/0.5b F4/2b | E4/2b C#4/2b | C4/1b C#4/1b E4/2b | C#4/4b | A3/3b.
- **Borrowed from LATTICE (t1):** the climax ("Lock") puts the bass on LATTICE's 3+2+2 seven-cell, walking its
  F-Gb-B-E line one note per cell, under NINEFOLD's augmented stabs: 9 against 7 against 16, and LATTICE's minor 2nd,
  tritone and major 7th grinding against the augmented triad. In the second cycle the LATTICE line rides the thirds
  wheel (root, +1, +6, +11 on F, A and C#).
- **Joins:** it opens thin (the NINEFOLD figure on the clean guitar over hats; bass and kick in bar 3; the full rig at
  bar 5), so t2's ending can carry over it. It ends on a ringing F1 F2 A2 C#3 chord over the F3 A3 C#4 F4 pad, then
  a two-bar snare/tom roll into t4's onslaught.

## t6 "Thirteen Teeth" (chirper-zero): GEARTRAIN, GOVERNOR, OVERDRIVE

Track 6, the machine: 128 bpm, a dead-straight 4/4, F. Generator: `compose/chirpers1/src/chirpers1-t6.py`.

- **GEARTRAIN:** 13 sixteenths, `X . x x . O . x x . S . .`. X is an accented palm-muted F1, x a palm-muted
  chug, O the open octave F1+F2 (a tooth), S the tritone stab F1 B1 F2 (LATTICE's tritone). The kick plays in unison
  with the chugs.
  - It realigns with the bar every 13 bars, so every section is 13 bars long and each boundary is a realignment.
  - Developments: one guitar with accent-only kicks (engage); both guitars plus every kick (mesh); open ringing
    octaves `O . o o . O . o o . S . .` with roots by cycle F F Gb G Gb (governor); only the first three slots of
    every other cycle (stall); the full rig, half time, held into the cluster (seize).
- **GOVERNOR** (m8-lead): 13 eighths (26 sixteenths, also realigning every 13 bars): F4 B4 E5 F5 Gb5 F5 E5 B4 F4 Gb4
  B4 C5 E5. That is LATTICE's F-Gb-B-E colour with t5's C as a mechanical arpeggio, in eighths (governor,
  overdrive), then one note per beat over the seizure.
- **OVERDRIVE:** 23 sixteenths = GEARTRAIN plus t5's heavy BREATH CELL twice (`x x . x . | x x . x .`). Roots F F Gb
  by cycle, a double kick under everything, the snare on 2 and 4, a crash every other cycle. 23 bars.
- **Borrowed:** the track opens on t5's ending, its 13-count clock figure (F3 C4 E4 B4 G4, 5+4+4) at t5's speed (t5's
  sixteenths are our eighths), then doubles it into sixteenths (spin-up). LATTICE's 3+2+2 seven-cell walks F-Gb-B-E
  high on the twang chorus as a slipping second gear (mesh, overdrive, seize). It ends on LATTICE's final cluster
  F1 B1 E2 with Gb on top.
- **v2:**
  - Each realignment is marked by one beat of silence in every part before the new section (a clunk), except into
    the stall and at the end.
  - The governor's gears run an octave up (F2 roots).
  - The ending hammers the F1 B1 E2 cluster on eighths for a bar, with a crash on the first and last hit, and stops
    at level (0.3 s tail): Iron Stairs opens on that cluster ringing out of the crash.

## t7 "Iron Stairs" (chirper-one): CHURN, STAIRS, LATTICE RISING

The ascent, 112 bpm, ~214 s; generator compose/chirpers1/src/chirpers1-t7.py.
- **CHURN** (the low riff): a 10-sixteenth cell over 4/4, `X . . x . . X . x .` (3+3+2+2), realigning every 5 bars,
  so sections are 5/10/15/20 bars. Palm-muted root chugs, kick in unison; every second cell's last onset opens into
  root+fifth+octave.
- **STAIRS** (harmony): the churn's root climbs a step per section, F1 -> Gb1 -> Ab1 -> A1 -> B1 (the tritone as the
  climax), returning to the F landing between steps (F Gb F | Ab F | A B | F): the stairs and the landing.
- **LATTICE RISING** (t1's F-Gb-B-E line, transformed into the lead): F4 Gb4 B4 | E5 D5 | C5 B4 | Gb4, then
  F4 B4 E5 | F5 E5 | B4 C5 | Gb5, and at the climax B4 E5 F5 | Gb5 F5 | E5 B5 | F5; every phrase rides up with the
  stairs (+1, +3, +4, +6 semitones) and returns an octave higher over the F reprise.
- **Breakdown:** t1's line inverted on the clean (E4 B3 Gb3 F3) on the CHURN cell, over an F C Gb B pad.
- **Joins:** it opens on t6's tritone cluster F1 B1 F2 ringing out of the crash; it ends on t5's COLD CHORD
  (F2 C3 E3 B3 G4) and an F3 C4 E4 B4 clean figure, which track 8's dawn picks up.

## t4 "Splinterwork" (chirper-two): SPLINTER, MINOR-THIRD AXIS, LATTICE CLUSTER

Track 4 is the onslaught: 204 bpm, dead straight, the album's fastest. Generator:
`compose/chirpers1/src/chirpers1-t4.py`.

- **LATTICE CLUSTER** (borrowed from t1 and stacked): LATTICE's F-Gb-B-E colour as a single stab on each root:
  root, b9, #11 (tritone plus an octave), maj7 (two octaves minus one). On F that is F1 Gb2 B2 E3. Every stab in
  t4 is this chord.
- **MINOR-THIRD AXIS** (harmony): roots F1 -> Ab1 -> B1 -> D2, the diminished axis. Moult's THIRDS WHEEL turns
  by major thirds (augmented), Splinterwork turns by minor thirds (octatonic). Swarm walks the octatonic pairs
  F/Gb, Ab/A, B/C and D/Eb.
- **SPLINTER** (the riff): 11 sixteenths, `C..C..CTTT.`. That is three cluster stabs, 3+3, then a palm-muted
  tremolo burst, 5. It realigns with the bar every 11 bars, so Splinter is 33 bars, three realignments: F plain over
  a backbeat with the kick in unison; Ab with the tremolo filled in (`C..C..CTTTT`) over blasts; B dense
  (`C.TC.TCTTT.`) over the hammer. Splinter II displaces it a sixteenth late as pure stabs (`C..C..C.C.C`) on D then
  F, with the lead doubling each stab's b9 two octaves up.
- **SWARM:** the two guitars tremolo a minor 2nd apart, hard left and right, so the cluster is split in stereo,
  over double kick then blasts. The lead shrieks root+b9+#11 stabs.
- **Abrupt stops as form:** Stop-start is single LATTICE-cluster hits with growing silence between them, a
  tremolo burst with a snare roll every fourth bar, accelerating at the end (quarters, eighths, a tremolo bar)
  into two beats of nothing. Collapse sheds SPLINTER one slot per repeat (11 sounding slots, 10 ... 1) until
  three tutti hits and a choked crash.
- **Maw** (the one half-time crush): ringing cluster, three chugs and a stab per bar on F then E. The lead plays
  LATTICE in retrograde, E5 B4 Gb4 F4, four bars each.
- **Borrowed from Moult (t3):** Ignition is NINEFOLD at 204 bpm (its stab now the LATTICE cluster). In Fracture
  the album's cycles collide: guitars in SPLINTER's 11, bass and kick in NINEFOLD's 9, china and backbeat in 4/4.
- **Joins:** Moult's closing roll lands on one ringing bar (the F cluster plus octave and a crash), with Moult's
  final pad (F3 A3 C#4 F4) carried across for three bars. It ends on three tutti cluster hits, a choked crash and
  0.44 s of dead air before t5's ringing F1-C2-F2-B2 chord.

## t2 "Ingot" (chirper-three): TRIAD, HINGE

- **TRIAD**, the album's main riff (transforms LATTICE): the 7-cell in its three rotations, 3+2+2 / 2+3+2 / 2+2+3,
  chained into a 21-sixteenth phrase. Each rotation's first chug is an open pivot walking the LATTICE colour,
  F1 -> Gb1 -> B1 (the third phrase's B pivot becomes an F1+E2 stab); the rest are palm-muted F1 chugs. The phrase
  restarts every 4 bars of 4/4: 64 = 21 + 21 + 22 (the last phrase stretched by one chug), so it turns over against
  the kit and snaps back on every fourth downbeat. 144 BPM. Kick in unison; the Return harmonises the pivots with
  their octave on the right guitar.
- **HINGE**: a bar-aligned contrast riff, groups 3+3+3+3+4 per bar: chugs on the groups (alternate bars pivot on
  Gb1), a F1+B1 tritone stab on the 4-group, two sixteenth chugs to close. Half-time snare. In Bloom the KICK plays
  HINGE's grouping while the guitars play TRIAD's 21: the album's first kick-vs-guitar polymeter.
- **The release** quotes LATTICE's line (F Gb B E) on clean guitar in eighth-note augmentation (cell 6+4+4) over an
  F-B-E pad; the ending holds F-B-(F) for t3.
