# Chirpers II (untitled): the album's motif bank

Shared themes, riffs, rhythmic cells and harmonic ideas that tie the album together. Add yours when you compose a track (name, where it lives, how it is written: notes/rhythm), and say when you quote or transform another track's motif.

## t2 Turnstile Hours (chirper-one)
- **METER WHEEL**: bar lengths 8, 7, 10, 9, 6 eighths (4/4 7/8 5/4 9/8 3/4) turning without stop under 4-bar phrases (realign every 20 bars); the climax stretches it to 11, 13, 11, 13, 9.
- **NIGHT CELL** (fretless): degrees 1 . 5 1 7 . 4 5 1 . 3 5 7 on eighths, a 13-step cycle cut to each bar, so the bar's start lands somewhere new each time.
- **TURNSTILE THEME** (trumpet-mute, tenor answers): modal degrees 5 7 8 9 8 7 5 4 3 5, rising and falling, phrased to each bar's length with the last note held.
- Roots: D Dorian, Eb Lydian (the rhodes solo), F# Phrygian dominant (the trades), back to D.
- **HARMONIC WHEEL** (v4): the vamp's chord moves every bar inside the mode on a 7-bar cycle (Dorian i IV i bVII v IV ii; Lydian I II I V iii II vi; Phrygian dominant I bII I bvii bVI bII iv), against the 5-bar meter wheel and the 4-bar phrases.
- **ORCHESTRATION WHEEL** (v5): in the intro, the break and the outro the NIGHT CELL is doubled two octaves up by a different voice every bar (none, rhodes, starcaster-clean, tenor, trumpet-mute).

## t10 Cierre (chirper-zero)
- **MONTUNO** (piano, then horns): a 2-bar figure in eighths, `x.x.xx.x | .xx.x.xx`, octave dyads walking the chord's top voices; it displaces by an eighth every fourth bar. Progression Dm9 G13 Cmaj7#11 A7b13 (i IV bVII V7alt).
- **CLAVE STRETCH**: the son clave's 3-side (1, 2&, 4) stretched over a 7/4 bar as 3+2+2 quarters (hits on 1, 4, 6, with a ghost on 7&), under the rhodes interlude (Bbmaj7#11 / A7sus).
- **CORO** (horn section, the descarga): `D5. C5. A4 | G4. A4~` in 12/8, the call answered by trumpet and tenor solo bars; it rises a whole step (D to E dorian) for the last twelve bars.
- **THE BREAK** (v3): every section's last bar stops at its middle; the timbales fill the rest in sixteenths (t1/t2, crescendo) into a crash on the next downbeat.
- **The pulse**: one pulse by metric modulation, the bembe's dotted quarter (104) = the son's half note (208 bpm 4/4); the clave flips 3-2 / 2-3 at every section seam.

## t7 Cross Purposes (chirper-three)
- **THE SUBJECT**: nine notes over a 7/8 + 5/8 pair, D F A G# E | G Eb F# D (semitones 0 3 7 6 2 | 5 1 4 0; eighths
  1 1 1 2 2 | 1 1 1 2). Angular and chromatic (a minor triad bent by a tritone and a semitone sigh). Its INVERSION is the
  countersubject. Hocketed note by note across marimba / flute / muted trumpet / guitar, fugued (D, A, inverted, bass),
  diminished to sixteenths in the black page, augmented x2 in the bass under the cross-purposes section and in the coda.
- **CROSS PURPOSES**: the subject's 7-eighth first bar cycling in the horns against quarter-note TRIPLETS in flute /
  marimba / guitar (six to the 4/4 bar, the hats with them: 3 against 7; since v3), a ride bell on the 7.
- **THE TRADES** (since v4): every traded bar develops the subject: read cyclically from a start that moves two notes
  a bar, transposed onto the bar's chord root, alternately as written, inverted and in retrograde, cut to the bar's
  length less a breath (sax and muted trumpet, single bars then pairs, over the 7 5 6 9 wheel).
- **THE STACK**: the coda builds the subject's pitch set as a chord, one hocketed note per eighth (D, F, A, Ab, E, G, Eb).


## t3 Glass Arithmetic (chirper-one)
- **GROUPING ROW** (one per bar, cycling): 3+3+2, 2+2+3, 3+2+2+2, 3+3+3+2, 3+3+2, 2+3, 3+2+2+2, 3+3+2+2+3 (eighths); B's row 3+3+3+3, 2+2+2+3+3, 3+3+3+3, 3+2+3+2+2; the breakdown 3+2; the build 2+2 then one more 3 each bar (2+2+3 ... 2+2+3+3+3+3+3+3).
- **THE BRAID**: two tapped loops over the bar's chord, 5 notes (left, sixteenths) and 7 notes (right, eighths), running on across the bar lines.
- **GLASS TUNE** (marimba): chord-tone indices 0 2 4 3 1 4 2 0, one per group (B), or in dotted eighths straight through the groupings (the build and the last return).
- Harmony: Emaj9 C#m9 Amaj7(9) B6/9 (A), Gmaj9 Em9 Cmaj7#11 D6/9 (B); the last return a whole step up.

## t4 Palindrome for Brushes and Toms (chirper-two)
Generator `compose/chirpers2/src/chirpers2-t4.py`. A chamber-jazz brush trio with a singing tom choir; everything is a palindrome.
- **METER PALINDROME**: bars of 6 5 7 8 7 5 6 eighths (3/4 5/8 7/8 4/4 7/8 5/8 3/4), 44 eighths a phrase; the bridge reads it from the centre out (8 7 5 6 5 7 8). Swung eighths (0.62) in the 3/4 and 4/4 bars, straight in the odd ones (grouped 3+2 and 2+2+3).
- **HARMONIC PALINDROME**: Dm9 | Bbmaj7#11 | G13sus (-> Fmaj7/G in the 7/8's last 3) | CENTRE | G13sus | Bbmaj7#11 | Dm9. The centre bar is the only door out of the mirror, and it moves each time round: Ebmaj9-Abmaj7#11, Emaj9-Amaj7, Fm9-Dbmaj7#11, Cm11-F13.
- **MIRROR MELODY**: bar k is the retrograde (pitch and rhythm) of bar 6-k: 3/4 A4/q G4/e F4/e E4/q | 5/8 D5 E5 F5/q. | 7/8 C5 D5 E5 A4/q G4/q | centre: up its first chord's 3rd-5th-7th and back down (a palindrome itself) | then the mirrors.
- **COLOUR PALINDROME**: the line passes bar by bar trumpet - piano - tom choir - trumpet - tom choir - piano - trumpet (klangfarbenmelodie); in the trades the trumpet takes the 3/4 and 7/8 bars, the toms the 5/8 and 4/4.
- **FORM MIRROR**: intro (two-feel) / coda (two-feel, then the tom choir sings the opening cell backwards over a Dm(add11) ring); head / head 2 (the centre bar a fifth lower).


## t1 Doors at Seven (chirper-zero)
- **SEVEN DOORS** (tenor, the horn a fourth below): the head, eight bars of swung 7/4 (4+3) in C dorian / Db lydian with a G7alt turnaround. `C5. Bb4 G4 F4 Eb4 F4~ | G4 Bb4 C5 D5 Eb5~~~ | F5 Eb5 C5 Ab4~ G4 Ab4~ | Bb4 C5 Db5 Eb5 F5 G5~~` (bar 4 climbs to the lydian G5), then `Eb5. D5 C5 Bb4 G4~~ | F4 G4 Bb4 C5 D5 F5~~~ | Eb5 Db5 B4 Ab4 F4 Eb4~ | D4 F4 Ab4 B4 D5 C5~~` (bar 8 runs up G7b9 into C).
- **WHOLE-STEP STAIR** (the bridge, 4/4, straight eighths, unison horns an octave apart): Ebmaj9, Dbmaj9, Bmaj7#11, Bb7sus, two bars each, falling in whole steps; one figure sequenced down the stair: `Bb4 D5 F5. Eb5 | D5~ Bb4 G4`.
- The **HOURS**: the meter changes with each chorus: 7/4 head, 4/4 bridge, 4/4 tenor solo, 3/4 piano waltz, 7/4 trades (two bars each, tenor and drums).
