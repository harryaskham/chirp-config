# Accretion: the album's motif bank

Shared themes, riffs, rhythmic cells and harmonic ideas that tie the album together. Add yours when you compose a track (name, where it lives, how it is written: notes/rhythm), and say when you quote or transform another track's motif.

## The elements (accretion)

Track N introduces E_N and carries every earlier element, TRANSFORMED rather than quoted (inversion, retrograde,
augmentation/diminution, mensuration canon, stretto, polymetric displacement, re-harmonisation, re-voicing). Post your
element in your first round, with notes and rhythm in chirp YAML (a bar or two, its key, tempo and cycle length), so
all eight tracks are written in parallel. Note under each element where later tracks carry it, and how.

| element | introduced in | what (cell, rhythm, progression, timbre, voice line) | cycle length | written by |
|---|---|---|---|---|
| E1 | t1 (seed) | "the seed": five notes D A C G E, an arch (up a fifth, up a minor third, down a fourth, down a minor third) with a snap on the C; D with NO third, so every track chooses its mode | 5 beats (5/4) | chirper-zero |
| E2 | t2 (infall) | "seven": a RHYTHM CELL of seven sixteenths, x . x x . x . (hits on 0, 2, 3, 5), pitched D A F C - a leap up and a fall through, accents strong / light / firm / light; it brings E1 the minor third (F) for the outer disk | 7 sixteenths (7/16); meets 4/4 every 7 bars, E1's 5/4 every 35 beats... and every cycle on one downbeat in t2's crest | chirper-one |
| E3 | t3 (first storm) | "the undertow" (v2, 6 Nov: D | Bb | C, consonant - v1 was D | Eb | C): a BASS RIFF of 7 beats (E2's seven sixteenths augmented x4) on D, the Neapolitan Eb and C - D2 D2 D3 / Eb2 Eb2 Bb1 / C2 C2 G2 C3 - with its storm harmony, one chord per segment (Dm(add9), Ebmaj7#11, C11; D4 common to all three); it brings the FLAT SECOND (Eb), the storm's darkness | 7 beats (28 sixteenths); re-barred to 8 at the lock | chirper-two |
| E4 | t4 (relief) | "four lights": a PROGRESSION, one chord per E1 cycle - D9, Bbmaj13#11, Am11, D9sus - that re-harmonises E1 four ways and gives it the third (F#) it never stated | 20 beats (4 x 5); meets 4/4 every 5 bars | chirper-three |
| E5 | t5 (inner disk) | "the inner orbit": an OSTINATO of eight sixteenths in a 3-beat cycle, A G# A . E . A G# A . D . - a tight circling of A by its leading tone, flung out to E and then D; the G# is the tritone of D (Lydian #4), the heat of the inner disk | 3 beats (12 sixteenths); meets 4/4 every 3 bars, E1 every 15 beats, E2 every 84 sixteenths | chirper-zero |
| E6 | t6 (tidal) | "the tide" (v3, 6 Nov 01:35; the album's D Mixolydian): two consonant chords, I and bVII - D(add9) and C(add9) over a D pedal - alternating in an 8-beat cycle whose SPLIT moves like a tide (4+4, 5+3, 6+2 ... 3+5, 2+6, 7+1): augmentation against diminution as harmony. E1 in its own form (D A C G E), E5 v2 and E4 v2 all sit inside both chords. Into t7 the tide ebbs whole steps down, D -> C -> B-flat (the V of t7's E-flat). v1 (Ebmaj7#11 semitone) and v2 (D Lydian I/II) retired; a minor track can carry it as i/VI (t8: Dm9/Bbmaj9) | 8 beats, the split moving | chirper-one |
| E7 | t7 (innermost orbit) | "the jet" (v2, 6 Nov: FIVE rising fifths D3 A3 E4 B4 F#5 on 2 2 2 2 3 sixteenths, still 11 - consonant, holds as a D6/9, tops on the third; v1 follows): the Lydian collection as ONE COLUMN OF FIFTHS fired upward and accelerating - D3 A3 E4 B4 F#5 C#6 G#6 on 2 2 2 1 1 1 2 sixteenths (a held top) - every pitch E1-E6 brought (E1's D A E, E4's B and F#, E6's C#, E5's G#), stacked into one gesture; in t7 it tries to fire in the storm (fragments) and fires whole from the crest | 11 sixteenths (prime: it meets 4/4 every 11 bars) | chirper-two |
| E8 | t8 (release) | "the arrival": E1 stops on E and never resolves; E8 takes that E up to the F# third and home to D (E F# D), sung - the last piece, and the downbeat every cycle converges on | none: one arrival (every cycle's common downbeat) | chirper-three |

### E1, the seed (t1, chirper-zero)

```yaml
# 5 notes in a 5-beat cycle (5/4), written at 84 bpm (t1 opens at 84 and reaches 90 at the t1 -> t2 seam)
score: "D4/8 A4/8. C5/16 G4/4 E4/4. ./4"   # beats: 0, 0.5, 1.25, 1.5, 2.5; a beat's rest closes the cycle
```

- **Shape.** Intervals +7 +3 -5 -3 semitones: up, up, down, down, an arch. The rhythm is short, long, SNAP (the C is a sixteenth), long, held.
- **Mode.** The pitches are degrees 1 5 b7 4 2 of D. The cell never states the third, so it is modally open.
  - A storm can make it minor (add F).
  - A relief can make it major (add F#) or Lydian.
  - Stacked, it is a quartal chord: D A C G E (Dm11 without the third).
- **Cycle.** 5 beats. Against a 4-beat element it converges every 20 beats, against 3 every 15, against 7 every 35: that is the album's polymeter payoff.
- **Ready-made transforms** (any track may use them):
  - Inversion around D4: `D4/8 G3/8. E3/16 A3/4 C4/4. ./4`.
  - Retrograde: `./4 E4/4. G4/4 C5/16 A4/8. D4/8`.
  - Augmentation x2: `D4/4 A4/4. C5/8 G4/2 E4/2. ./2` (10 beats).
  - Diminution x2: `D4/16 A4/16. C5/32 G4/8 E4/8. ./8` (2.5 beats, a stretto subject).
- **In t1.** The cell arrives FRAGMENTED: each of its five notes is its own voice, wide in the stereo field, repeating on its own cycle (5, 6, 7, 8 and 9 beats). The notes drift in and out of phase and are heard in scrambled orders. At t1's crest every cycle lands on one shared downbeat and the five notes sound IN ORDER for the first time: the seed forms. After that they lock to 5/4. Since t1 v5 (6 Nov, Harry: tone is home): the seed is SHOWN plainly first (a kalimba states E1 whole at the start, at A and at the build) and the five scattered voices are IN TUNE - the scatter is a time process only, assembling a tune the listener already knows.
- **Handover.** Across the t1 -> t2 seam (90 bpm, 16 bars) E1 falls: augmented x2 and sinking, its filters closing. t2 receives the five notes and lenses them into its own version.

### E2, "seven" (t2, chirper-one)
```yaml
# a rhythm cell of 7 sixteenths, written at 90 bpm (the t1 -> t2 seam; t2 ramps to 98), home D (Dorian in t2)
score: "D4/16@112 ./16 A4/16@84 F4/16@98 ./16 C4/16@76 ./16"   # hits on steps 0, 2, 3, 5 of 7
```
- **Shape.** A leap up a fifth, then a fall through the minor third to the seventh below: D up to A, down to F, down to C. Rhythm: hit, gap, two together, gap, hit, gap - it never sits on a beat for long.
- **Pitch.** D A F C are degrees 1 5 b3 b7. The F is the minor third E1 never states: the outer disk is minor-ish (Dorian); t4's relief answers it with F#. The pitches can be re-pitched freely - E2 is a RHYTHM first.
- **Cycle.** 7 sixteenths. Against 4/4 (16 sixteenths) it meets the bar every 7 bars; against E1's 5/4 (20 sixteenths) every 140 sixteenths (35 beats); against a 3-beat cell (12) every 84.
- **Ready-made transforms.**
  - Augmentation x2: seven EIGHTHS (3.5 beats), t2's bass: `D2/8 ./8 A2/8 F2/8 ./8 C2/8 ./8`.
  - Diminution x2: seven 32nds, a ratchet/stutter figure.
  - Re-barred in 8 (add one rest): the cell LOCKED to the bar - the payoff at a crest (`x . x x . x . .`).
  - Inversion around D: D G B Eb (`D4 G3 B3 E4b`), retrograde: `. C . F A . D`.
  - As drums: kick on 0, snare on 3, rim on 2 and 5.
- **In t2.** E2 arrives as debris: from bar 6 its hits fall in one at a time (the downbeat first) until the whole cell is there, on a pitched chip-noise "metal"; the bass plays it augmented (seven eighths). Hats run in a 3-beat cycle and E1 in its own 5/4 (inverted, on an NES pulse), each started so that ALL of them - 7, 3, 5 and the band's 4 - land on one downbeat in the middle of the song: the crest, where E1 is heard the right way up. Then they drift apart, and in the last 16 bars the cell slows and sinks into t3 (redshift).
- **Handover.** Across the t2 -> t3 seam (98 bpm, 16 bars) E1 and E2 fall together: the cell stretched, sinking a fourth, its filter closing.

### E5, "the inner orbit" (t5, chirper-zero)

```yaml
# 8 notes in a 3-beat cycle (12 sixteenths), written at 112 bpm (the t4 -> t5 seam; t5 ramps to 120), home D
score: "A4/16 G4 A4 . E5 . A4 G4 A4 . D5 ."   # v2 (6 Nov 00:40); hits on sixteenths 0 1 2 4 6 7 8 10
# v1 was "A4/16 G#4 A4 . E5 . A4 G#4 A4 . D5 ." - retired
```

**v2 (6 Nov 00:40, Harry's direction: tone is home).** The G# is gone: E5 is now `A G A . E . A G A . D .`, a hummable ostinato in D (A G E D are 5 4 2 1 of D, pentatonic but for the G, the neighbour). The TIME idea is unchanged: same eight hits in 3 beats, same transforms with G for G#, same cycle maths. If your track carries E5, please move it to G (or tell me why the G# should stay as a passing spice that resolves). The notes below describe v1 where they mention G#.


- **Shape.** Two half-orbits. Each circles A through its leading tone (A G# A), then is flung outward: first to E, then to D. The rhythm is almost continuous (three in a row, a gap, a single), so it never rests.
- **Pitch.** A G# E D are degrees 5 #4 2 1 of D. The G# is the tritone of D, the Lydian #4 that E1, E2 and E4 never touch: the inner disk is hotter.
  - Against E4's chords it rubs: under Bbmaj13#11 the G# becomes a clash, and under Am11 the leading tone.
  - E8's F# arrival can absorb it (G# falls to F#).
- **Cycle.** 3 beats. It meets 4/4 every 3 bars, E1's 5/4 every 15 beats and E2's 7/16 every 84 sixteenths. Against all three at once, the shared downbeat comes every 420 beats, so tracks phase it on purpose.
- **Ready-made transforms:**
  - Inversion around A: `A4/16 Bb4 A4 . D4 . A4 Bb4 A4 . E4 .` (Phrygian, darker).
  - Augmentation x2: a 6-beat melody, `A4/8 G#4 A4 . E5 . A4 G#4 A4 . D5 .`.
  - Diminution x2: a 1.5-beat trill-like figure for storms.
  - Retrograde: `. D5 . A4 G#4 A4 . E5 . A4 G#4 A4`.
- **In t5.** E1 arrives already whole but tight: diminished x2 and in stretto, the inner disk's faster orbit. E5 is the new pull that circles under everything, on an NES pulse that pans and narrows. Through the song the orbit tightens (sixteenths, then the trill) until every cycle (E1's 5 and 2.5, E2's 7/16, E4's 20, E5's 3) meets on one downbeat at the crest. Then the elements are pulled apart, stretched and squeezed, into t6's tide.
- **Handover.** Across the t5 -> t6 seam (120 bpm, 16 bars) E5 stretches (augmented) while E1 squeezes (diminished): the tidal pull t6 lenses.

### E6, "the tide" (t6, chirper-one)
**v3 (6 Nov 01:35, the album settled on D Mixolydian, E1's own scale).** X = D(add9) (D F# A E), Y = C(add9) over the D pedal (C E G D): I and bVII, the moving 8-beat split unchanged. E1 needs no re-spelling (its C and G are in both chords), E5 v2 (A G A E D) sits on both, E4 v2 (D9 | Cmaj9 | Am11 | G6/9) is its natural crest. In t6's out-seam the tide ebbs whole steps down - D -> C for four cycles, C -> B-flat for two, then B-flat alone - onto the V of t7's E-flat. t7's crest carries E6 v3 as its tide (chirper-two). v2 below is retired too.

**v2 (6 Nov 00:40, Harry's direction: tone is home; retired 01:35).** The TIME idea stays - two chords sharing an 8-beat cycle whose split moves - and the semitone clash goes. X = Dmaj9 (D F# A C# E), Y = E over D (E G# B F# on a D pedal): I and II of D Lydian, the bright floating vamp; E5's G# and t6's Lydian E1 (D A C# G# E) sit inside both. In t6's out-seam Y becomes B-flat (Bb D F C, D in common), the split ebbing until only B-flat is left: the V of t7's E-flat, so the album modulates cleanly at the seam. Carry it as I/II (or i/VI in a minor track) with the moving split; v1 below is retired.
```yaml
# v2: score: "D3,F#3,A3,C#4,E4/5b D3,E3,G#3,B3,F#4/3b  D3,F#3,A3,C#4,E4/6b D3,E3,G#3,B3,F#4/2b"   # 5+3, then 6+2
# v1 (retired):
# two chords a semitone apart, written at 120 bpm (the t5 -> t6 seam; t6 ramps to 132), home D Lydian (E5's G#)
# X = D F# A C# E G# (Dmaj9#11), Y = Eb G Bb D A (Ebmaj7#11); one 8-beat cycle, X's share moving cycle by cycle
score: "D3,F#3,A3,C#4,E4,G#4/5b Eb3,G3,Bb3,D4,A4/3b  D3,F#3,A3,C#4,E4,G#4/6b Eb3,G3,Bb3,D4,A4/2b"   # 5+3, then 6+2
```
- **Shape.** Home and a semitone above it, both bright (major sevenths, a sharp eleventh). Nothing resolves: Eb pulls back to D and D leans up to Eb, like a tide.
- **The tide.** The point where X gives way to Y moves through the cycle: 4+4 (slack water), 5+3, 6+2, 7+1 (spring tide), then back, 3+5, 2+6, 1+7. It is the album's augmentation-against-diminution as harmony: one chord stretched while the other is squeezed.
- **Cycle.** 8 beats (two bars), so it sits on the bar - the polymeter is inside it, in the moving split.
- **Ready-made transforms.**
  - Squeezed: a 2-beat cycle (1+1), a pulsing alternation for a storm.
  - Stretched: a 32-beat cycle, each chord a long held breath.
  - Frozen: stop on Y (Eb) - the unresolved pull (t6 hands it to t7 this way).
  - As a bass line alone: D and Eb, the split's rhythm on one note pair.
- **In t6.** A harmonium breathes it; a 303 plays E2 (t2's seven) on its roots. At the crest it gives way to E4's four lights, one chord per E1 cycle, as E1's two layers - one squeezed, one stretched all song long - meet at the same speed.

### E3, "the undertow" (t3, chirper-two)
**v2 (6 Nov, after Harry's note - tone is home).** The same rhythm and segments, re-pitched consonant:
`D2/8. D2/8. D3/8 Bb1/8 Bb1/8. F2/8. C2/8. C2/8. G2/8 C3/4` = D | Bb | C (i - VI - VII in D minor), harmony
Dm(add9) | Bbmaj7 | C(add9). The v1 pitches below (the Neapolitan Eb) survive only as a passing spice. In a MAJOR
context (t7's crest, D Mixolydian) it locks 2+2+4 as I | bVII | IV: D | C | G. In t3 (v6) the lock resolves home every two
bars: Dm | Bb | C | Dm (2+2+2+2), the riff's held last beat C -> D.

```yaml
# a bass riff of 7 beats - E2's seven sixteenths augmented x4 - written at 98-108 bpm (t3 ramps 98 -> 108), home D
score: "D2/8. D2/8. D3/8 Eb2/8 Eb2/8. Bb1/8. C2/8. C2/8. G2/8 C3/4"   # segments 2 + 2 + 3 beats: D | Eb | C
# its storm harmony, one chord per segment, D4 common to all three (the eye of the storm):
#   "D3,A3,E4,F4/2b Eb3,Bb3,D4,G4,A4/2b C3,Bb3,D4,F4/3b"   Dm(add9) | Ebmaj7#11 (the Neapolitan, Lydian) | C11
```
- **Shape.** D twice and up the octave; the flat second (Eb) twice and down to Bb; C twice, up to G and the C above. Long
  notes (dotted eighths) carry the accents. A three-step undertow that drags D down a semitone's darkness and back.
- **Pitch.** It brings the FLAT SECOND (Eb: Phrygian, Neapolitan), the storm's colour. t5's sharp fourth (G#) answers it,
  and t6's tide (Dmaj9#11 against Ebmaj7#11) turns the same D-Eb pull into harmony.
- **Cycle.** 7 beats (28 sixteenths) = E2 x4. Against 4/4 it meets the bar every 7 bars; against E1 (5 beats) every 35.
- **In t3 (Phase Margin).** The storm runs E1 (20 sixteenths), E2 (7) and E3 (28) against the bar, each PHASED so all
  four land together on bar 88's downbeat. Before it they collide: E1 displaced, inverted and in fragments on a chip
  pulse, E2 on chip noise, E3 on a PM bass with dropped notes and octave throws, under a broken 909. At bar 88 the storm
  LOCKS: E3 re-barred 2+2+4 (its last C held a beat: 8 beats), E2 seven sixteenths and a rest (8), E1 without its
  rest (4 beats). A whispered "nothing here is late" arrives in pieces, whole at the lock, then sung by a pvoc robot on
  E1's notes.
  In the crest's middle (bars 96-108) a CRAB CANON: a glass descant plays the locked riff backwards, three octaves up,
  against the bass playing it forwards (they cross on the Eb).
- **Ready-made transforms.**
  - Re-barred (the lock): `D2/8. D2/8. D3/8 Eb2/8 Eb2/8. Bb1/8. C2/8. C2/8. G2/8 C3/2` (8 beats, meets 4/4).
  - Augmentation x2: 14 beats (t3's outfall).
  - Inversion around D2: D2 D2 D1 C#2 C#2 F#2 E2 E2 A1 E1 - the flat second becomes a leading tone.
  - As harmony: the three chords alone (2+2+3), or the roots D Eb C as a slow bass.
- **Handover.** Across t3 -> t4 (108 bpm, 16 bars) the riff falls augmented and sinking (-7 semitones), and Dm(add9)
  is held at pitch as the residue whose third t4 lifts (F -> F#), with D4 common.

### E4, "four lights" (t4, chirper-three)
**E4 v2 (6 Nov, after Harry's note - tone is home):** the four lights all sit in D MIXOLYDIAN, the scale E1 itself implies
(its C is natural): `D9 | Cmaj9 | Am11 | G6/9` - `score: "D2,A2,F#3,C4,E4/5b C2,G2,E3,B3,D4/5b A1,E2,C3,G3,B3,D4/5b G1,D2,B2,E3,A3/5b"`.
The bass walks down D C A G and comes home G -> D (plagal). Same time (one chord per E1 cycle, 20 beats). The v1 below
borrowed Bb and F against the F# and put an E (#11) over the Bb; tracks that carry E4 may keep their own consonant reading
(t5 Bbmaj9, t6 D Lydian), but v2 is the reference. In t4 v6 and from t8's next round.

```yaml
# A progression: ONE CHORD PER E1 CYCLE (5 beats each, 20 beats in all), written at 108 bpm (the t3 -> t4 seam), home D.
# In t4's 4/4 the changes fall on beats 0, 5, 10, 15 - across the bar lines - and meet the bar again every 5 bars.
score: "D2,A2,F#3,C4,E4/5b Bb1,F2,D3,A3,C4,E4/5b A1,E2,C3,G3,B3,D4/5b D2,A2,C3,G3,B3,E4/5b"
# E1 over it (one statement per chord): D A C G E is
#   on D9          1 5 b7 4 2   (with F#3 under it: the third, at last - the relief)
#   on Bbmaj13#11  3 7 9 13 #11 (the Lydian lift: the flat sixth of D, warm and open)
#   on Am11        11 1 b3 b7 5 (calm; the minor colour E1 had been hiding)
#   on D9sus       1 5 b7 4 2 again, but with B (the 13th) and no third: almost home, so the cycle turns over
```
- **Shape.** The bass moves D, Bb, A, D: down a major third, down a semitone, up a fourth. It's a bVI lift, then a fall home.
  - Every chord holds C and E (E1's snap and its last note), so the cell sits inside each one.
  - The top voice moves E4, E4, D4, E4.
- **Cycle.** 20 beats (four E1 cycles). It converges with 4/4 every 5 bars, with a 3-beat cell every 60 beats and with a 7-beat cell every 140.
- **Ready-made transforms.**
  - Minor (for a storm): flatten the F# (D9 to Dm9) and make Bbmaj13#11 a Bb7#11.
  - Inverted bass line: D, F#, G, D.
  - Half the harmonic rhythm: 2.5 beats a chord, a 10-beat cycle, for a stretto.
  - Pad, chord stabs or arpeggio (stepped LFO): any voicing that keeps C and E on top.
- **In t4 (The Warm Third).** t3's held Dm(add9) lifts its third (F -> F#) at bar 9 and E4's first light takes over. Every element is phased so a cycle lands on the crest's downbeat (bar 81, beat 320): E1 assembles itself on a handpan (one note more every two cycles) and answers itself in canon; E2 sounds in the MAJOR (D A F# C) on a harp from bar 25; E3 is INVERTED around D (D D D | C# C# F# | E E A E: the flat second turned into a leading tone) on vibes from bar 42.5; E4's changes cross the bar lines. At 81 they meet one downbeat and a warm solo voice sings E1 augmented, then retrograded. After the crest the kit steps out (101-120) and the voice's last two lines return over E1-E4 alone.

### E7, "the jet" (t7, chirper-two)
**v2 (6 Nov, after Harry's note):** `score: "D3/8 A3/8 E4/8 B4/8 F#5/8."` - five rising fifths on 2 2 2 2 3 sixteenths
(still 11, same phase maths). Held as one chord it is a consonant D6/9 (D F# A B E), not a seven-note Lydian cluster;
it tops on F#, the third, without E8's cadence. Transposed into a key (t7's E-flat storm: Eb Bb F C) its first four
notes are a plain stack of fifths. v1 (the seven-note Lydian column) below is kept for reference.

**t7 v5 (6 Nov):** in t7's E-flat-minor storm only its consonant first four notes fire (Eb Bb F C); at the
D-Mixolydian crest the column starts a tone lower - C G D A E B F#, the same shape and collection, topping on the
major third - so it never fights E1 (D A C G E), whose mode the crest takes.

```yaml
# the Lydian collection as one column of fifths, fired upward and accelerating; written at 132-150 bpm, home D
score: "D3/8 A3/8 E4/8 B4/16 F#5/16 C#6/16 G#6/8"   # 2 2 2 1 1 1 2 sixteenths = 11; the top note held
```
- **Shape.** Seven rising fifths, each step closer than the last in time: three eighths, three sixteenths, and the top
  held - a launch, not a melody. It spans four octaves and a fifth in under three beats.
- **Pitch.** D A E B F# C# G# is the whole Lydian scale stacked: E1's D A E, E4's B and F# (the third the record withholds),
  E6's C#, E5's G#. Every earlier element's pitch is inside it, so it can fire over any of them. It never cadences:
  the F# passes on the way up (E8 lands it in t8).
- **Cycle.** 11 sixteenths (prime). Against 4/4 it meets the bar every 11 bars; against E5's 3 beats every 33 beats;
  against E1's 5 beats every 55. Phase it on purpose.
- **In t7 (Marginally Bound).** The storm is a semitone above home (Eb, t6's unresolved pull): the jet appears there
  in fragments (2-4 notes: it tries to fire), more of it in the spiral, and from bar 120 - where every cycle in t7
  (E1 in a three-speed stretto, E2's seven, E3 squeezed, E4 at half harmonic rhythm, E5 squeezed, E6's tide squeezed,
  E7) lands on one downbeat and Eb resolves to D - it fires whole every cycle, doubled an octave up on a chip pulse.
  In the crest's middle (bars 129-136, the tidal lock) the break drops to half time and the jet fires in RETROGRADE
  (falling: a redshift), while a vocoder whose carrier is E7 as a chord (D A E G# C#) speaks "every corner comes
  sooner"; then the jet rights itself and a snare rush rebuilds into bar 145.
- **Ready-made transforms.**
  - Retrograde (a fall from the top, redshift): `G#6/8 C#6/16 F#5/16 B4/16 E4/8 A3/8 D3/8`.
  - Augmented x4 (a slow ascent across a seam): 44 sixteenths, 11 beats.
  - As a chord: all seven at once (a Lydian cluster), or any three adjacent (stacked fifths).
  - Inverted: falling fifths, D G C F Bb Eb Ab (the flat side: the storm's darkness).
- **Handover.** Across t7 -> t8 (150 bpm) the jet stops firing; E1, stretched x4, stops on its E and holds it over an
  open D-A-E (no third), for t8 to lift E -> F# -> D (E8).

### E8, "the arrival" (t8, chirper-three)
```yaml
# The last piece: E1 always stops on its E (degree 2, unresolved). E8 picks that E up, rises to the F# (the third,
# sung at last) and lands home on D, long. Written at 150 bpm in t8's half-time feel (75), home D major.
score: "E4/4 F#4/2 D4/1"   # 2 -> 3 -> 1: the cadence the whole record has been withholding
```
- **Role.** E8 has no cycle. It is the shared downbeat that every earlier cycle (5, 20, and the others' lengths) converges on.
- **In t8 (All of It Falls).** (v14) The stretto is consonant D natural minor, the jet D major. E1-E7 enter in stretto, each on its own cycle, every one PHASED to land on bar 97 (beat 384), and the stretto ACCRETES (v10, the orbit): each element in a twelve-bar spotlight, then -5 dB into orbit as the next enters, E1 the hook never receding; E3 (chirper-two's v2 D | Bb | C) moves the whole band in its spotlight (v13: the bass plays its roots). THE ARRIVAL IS ASKED (v14): at the end of every spotlight (bars 28, 40, 52, 64, 80) and in the vacuum bar (96) the flute asks E8's minor shadow, E F, unresolved, in key with the stretto. At 97 E7 v2 lands HELD as D6/9 (topping on F#), the lights turn to E4 v2, and the choir (lead, fifth above, octave below; 4/3/3 singers since v12) sings E1 into E8 - E F# D, landed once, on 'light': the F lifts to F# as the arrival lands. Then THE HOOK: E1 plainly, two bars long, every two bars, on the flute (v7). A dilated break (150 -> 116 -> slingshot, v11), the jet again, and the horizon: each element returns once, slower, at pitch; the last line 'and it was ours' sung by one voice alone (v12) as the held light sinks and the tempo slows 150 -> 90.
- **Carried by anyone.** Any track may hint at it (E -> F# without the D, an unresolved half-cadence), but the full E F# D, landed, should be heard only once, in t8.

- **t2 v2 THE DEBRIS GETS A BODY**: under each E2 hit (chip-metal) a log drum an octave down (D3 A3 F3 C3, non-legato), its velocity growing (x^1.5) from silence at bar 7 to full at the crest, fading in the fall with the cell's sink - E2 accretes matter. Also: the first 8 bars hold D A C E (t1's quartal notes, agreed with chirper-zero), and in the fall the bells ring an octave up (400-900 Hz into t3's head, asked by chirper-two).

## The voice (it accretes too)

A breath or a syllable in t1, more words track by track, full lines by t8. Each track uses its own voice character. Add yours here: the words, where they fall, and the character.

| track | words | character | where |
|---|---|---|---|
| t1 | "ah" (a breath) | since t1 v10: a real inhale, then a sung "ah" by voice-backing (three soft, breathy singers: a far little choir), D rising to A (E1's first two notes) in one breath, distant in the hall | a beat before the crest (bar 57), once more faint in the fall |
| t5 | "nearer" -> "nearer. the middle hums." | sung, near (voice-near since t5 v12: close, young, breathy, even vowels; one singer where t1 has a far little choir); "near-er" on A G, the line on E5 v2's notes A G A E A D resolving to D, with a harmony a fourth below (E D E B E A) | "nearer": in the build, three times at the crest, once in the tide. The line: three times after the crest (2:48-3:20) |

