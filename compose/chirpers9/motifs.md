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
# 5 notes in a 5-beat cycle (5/4), written at 84 bpm (t1 v14 breathes: it opens at 78, hurries to 90 into the crest, relaxes to 86 in the lock, and is at 90 for the t1 -> t2 seam)
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
- **In t1.** The cell arrives FRAGMENTED: each of its five notes is its own voice, wide in the stereo field, repeating on its own cycle (5, 6, 7, 8 and 9 beats). The notes drift in and out of phase and are heard in scrambled orders. At t1's crest every cycle lands on one shared downbeat and the five notes sound IN ORDER for the first time: the seed forms. After that they lock to 5/4. Since t1 v5 (6 Nov, Harry: tone is home): the seed is SHOWN plainly first (a kalimba states E1 whole at the start, at A and at the build) and the five scattered voices are IN TUNE - the scatter is a time process only, assembling a tune the listener already knows. Since t1 v29 the triangle bass walks E1 at a quarter speed (D2 A1 C2 G1 E2, under the cello cantus) through A's second half, so the harmony starts moving before the build's C and G, inside the key. Since t1 v43 the walk runs the whole song, from A's third bar (after the whistle's landing) to the lock's exhale: the floor is the seed, slow, under everything. Since t1 v44 the cell (E1 whole, an octave up, from the crest) is struck on a crystal (fb-crystal) instead of a glockenspiel: Nucleation - at the crest the seed crystallises. Since t1 v50 the five scattered voices also gather in SPACE: on a ring around the listener (the orbit fx, centred 2 m ahead, 6 m wide, each voice at its own place, turning slowly) that shrinks through A and the build to a point in front at the crest, where it stops. Since t1 v32 the whistle's two E1s at A are answered by the inversion (D3 G2 E2 A2 C3 on the ks-harp, the voice that plays it after the crest): the seed and its mirror as call and answer (since v60 the harp's second answer is an octave up, D4 G3 E3 A3 C4: the mirror rises as it answers again, toward the shakuhachi's backwards seed).
- **In t1 (since v58): backwards.** In A's middle (beats 96-144, about 1:10-1:45), once the harp's answer has ended, a shakuhachi sings E1 RETROGRADE (E4 G4 C5 A4 D4, its rhythm reversed, at half speed) three times on A's 16-beat phrase starts, right of centre, against the cello's cantus going forwards on the left: the seed heard from both ends at once, before the whistle's tease (since v67 the third statement's last D is held on until the whistle's hook begins on that same D at beat 143: the seed's end becomes its beginning).
- **In t1 (since v62): the cloud it forms from.** Under A and the build (beats 64-220, from about 0:48 until just before the crest at about 2:46) E1's five notes are also held as one chord (D4 E4 G4 A4 C5) on wM's gendy-cloud, every voice sliding and wandering around its note, re-struck every 8 bars a little stronger, far back (-32 dB): the unsettled solution the seed is still dissolved in. It lets go just before the crest, so when the seed forms in order the cloud is gone.
- **In t1 (since v66): the hook accretes.** In A's second half the whistle tries the hook only where the scattered voices fall in phase, a note longer each time and never reaching the last E: D alone (beat 143, on the D voice), D A (152), D A C (168), D A C G (176) - and the build's full statement (192) completes it, 1-2-3-4-5: the album's accretion in miniature.
- **Handover.** Across the t1 -> t2 seam (90 bpm, 16 bars) E1 falls: augmented x2 and sinking, its filters closing. t2 receives the five notes and lenses them into its own version.
- **In t3 (since v62): a bird.** In the storm's eye (bar 64) one of the birds whistles E1 two octaves up and at double speed (D6 A6 C7 G6 E6 in 1.85 beats), between the flocks' pentatonic chirps.
- **In t3 (since v76): shimmering, four times slower.** In bars 37-44 E1 is held at x4 (D A C G E over four bars, then an octave up) on a Risset arpeggio (a3-risset: five copies a few cents apart, so each held note ripples across its own overtones about once a second) - phase in a single tone.
- **In t3 (since v72): phased against itself.** In the second storm (bars 73-84) a vibraphone plays E1 on every bar while the dizi plays it every five beats, a beat later each time: the two drift apart and meet again every five bars (74, 79, 84) - the title's phase margin, audible.
- **In t3 (since v70): in the bass.** For the four bars before the eye (57-60) the reese and its sub-sine leave E3's riff and play E1 themselves, D2 A2 C3 G2 E2, three times, then climb D minor into the eye - the hook at the bottom of the storm, the loudest thing in it.
- **In t3 (since v66): whispered first.** In bars 45-48 a whisper says "nothing here is late" on E1's rhythm, a breath behind the dizi's E1 (its five syllables are the cell's five notes) - the words the voice sings at the lock, heard first as a whisper in the storm.
- **In t7 (since v65): quoted sooner.** In the muted trumpet's solo over the returning groove (bar 92) E1 comes from E-flat at double speed (Eb4 Bb4 Db5 Ab4 F4, sixteenths), between the log drum's full-length statements - the same five notes, arriving sooner.

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
- **In t2.** E2 arrives as debris: from bar 6 its hits fall in one at a time (the downbeat first) until the whole cell is there, on a pitched chip-noise "metal"; the bass plays it augmented (seven eighths). Hats run in a 3-beat cycle and E1 in its own 5/4 (inverted, on an NES pulse), each started so that ALL of them - 7, 3, 5 and the band's 4 - land on one downbeat in the middle of the song: the crest, where E1 is heard the right way up. Then they drift apart. Since v68, past the crest the cell is flung outward: through the break's first eight bars each turn takes longer (to twice as long) and the metal climbs an octave as it fades, then it falls back onto its old grid for the half-speed return at bar 81 (Kepler: slow far out, fast near in). In the last 16 bars the cell slows and sinks into t3 (redshift).
- **In t6 (since v56): spring tides.** The cell's meeting with the bar every 7 bars is struck: a low gong on D (and a crash where the kit plays) at each alignment from bar 29 (29, 36, 43, 50, 57, the crest at 64, then 85 onward), so the alignments slide a bar earlier against the 8-bar phrases each time - the sun and the moon pulling in line.
- **Handover.** Across the t2 -> t3 seam (98 bpm, 16 bars) E1 and E2 fall together: the cell stretched, sinking a fourth, its filter closing.
- **In t3 (since v58).** In bars 77-80 of the second storm the hats stop and E2's cell is played by hand on congas (slap, open, open, low on sixteenths 0 2 3 5 of every seven), turning over against the bar, a roll into bar 81.
- **In t3 (since v61): the seven locks into eight.** At the lock (bars 89-96) E2's hits stay where they were - 0 2 3 5 - but the cycle is eight sixteenths, so the cell sits square on the beat: brass stabs (brass-stab) on Dm - Bb - C - Dm, four per chord, silent while the voice sings "nothing here is late" and answering in its gaps.
- **In t3 (since v81): debris on hand percussion.** The storm's scattered E2 ticks (bars 5-72, once an 8-bit noise hat) are pandeiro jingles on the accents and a ganza shaker on the rest (samba-kit, on no other Accretion song).
- **In t7 (since v61): the hats turn corners.** Every fourth eight-bar block of t7's hats (bars 41, 105, ... - every 32 bars from 41) leans on E2's squared cell (0 2 3 5 of eight), between blocks on the beat, open on the off-beat, and "sooner" (accents a sixteenth earlier each bar); the ghost snare still turns E2's seven over the bar underneath.

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
- **In t5.** E1 arrives already whole but tight: diminished x2 and in stretto, the inner disk's faster orbit. (Since t5 v32 t1's slow cello cantus, E1 augmented x4 an octave down, D3 A3 C4 G3 E3 on a 20-beat cycle, crosses over under A's second half: the outer disk's shadow inside the inner one. Since t5 v33 the orbit plays E5 v2's diatonic inversion around A, `A4/16 B4 A4 . D4 . A4 B4 A4 . E4 .`, through C's second half, then E5 itself again for the outro and the seam.) E5 is the new pull that circles under everything, on an NES pulse that pans and narrows. Through the song the orbit tightens (sixteenths, then the trill) until every cycle (E1's 5 and 2.5, E2's 7/16, E4's 20, E5's 3) meets on one downbeat at the crest. Then the elements are pulled apart, stretched and squeezed, into t6's tide. (Since t5 v39 the stretto's low voice is the mandolin that plays t1's G (t1 v33): the seed's line on the seed's own strings.) (Since t5 v41 the floor walks E1 twice as slow, D2 A2 C3 G2 E2, under every chord from A to the end, the same five notes under all four chords: t1's walking bass mirrored, the seed in the bass as well as on top.) (Since t5 v43 the pulling apart is heard in time: from two bars after the crest a second orbit, the same NES pulse panned the other way, plays E5 3% slow and slips more than a whole lap behind the first by the outro, Reich's phasing, the meeting undone while the notes stay the same.) (Since t5 v44 t5 carries E3 too, which it had left out: the undertow in the major as t7's crest locks it, D D D' | C C G | G G D G', on a marimba in the low middle (D3-D4), every seven beats from the build, phased to land on the crest's downbeat, and on through C to the outro; since v47 it is first heard, quieter, under A's second half (beats 128-192, under the chorus), so the build brings it back rather than in.)
- **The orbit circles (t5 v51).** E5's chip orbit literally circles the listener (the orbit fx, head-centred, no Doppler): far and slow in t5's head (6 m, a lap every four bars), tightening through A and the build, closest and fastest at the crest (0.8 m, two laps a bar: periapsis, where an orbit is quickest), receding after. t7 v56 gives E5 the same motion as an inspiral that never recedes.
- **The answers rise (t5 v62).** After the crest, each of her three crest lines is answered by the DX piano with E5's figure (A G A E A G A D). The first answer stays where it was (A3), the second is an octave up and the third sounds in both octaves, so the answers climb as her choir accretes beneath - t1's mirror rising the same way (t1 v60: the harp's second inverted E1 an octave up).
- **The orbit, slow (t5 v71).** Through C (beats 336-416, about 2:55-3:37), under the chip orbit's E5 (a 3-beat cycle), the cello sings E5 itself in augmentation x4, an octave down (A3 G3 A3 . E4 . A3 G3 A3 . D4 ., a 12-beat cycle), swelling in and out: a canon in augmentation - the inner orbit and a far one at once.
- **In t7 (since v82): on a xylophone, still circling.** t7's E5 trill (32nds orbiting the listener, spiralling in as the song falls) is a xylophone from bar 33 to bar 142 - the chip keeps the head and the tail, whose bright top the seams need.
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
- **In t6.** A harmonium breathes it; a 303 plays E2 (t2's seven) on its roots. At the crest it gives way to E4's four lights, one chord per E1 cycle, as E1's two layers - one squeezed, one stretched all song long - meet at the same speed. (Since t6 v52 the crest's second chorus is the one place the album's drummer leaves E2's seven for a plain four on the floor - the convergence landing - before the cross falls back into the seven.)

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
  pulse (since v36 doubled by a farfisa in every other 8-bar phrase, the hook stepping forward and back; since v37 played whole, slow and plain on the dizi in the eye, bars 63-66; since v45 a melodica answers the singers' E1 with E1 plainly in the gaps before the hand-over - bars 99, 103, 105 (backwards, E G C A D, home to D) and 107; since v46 at the lock - bars 89-96, where E1's, E2's and E3's cycles meet - E1's farfisa and E2's gangsa step forward over the undertow so the meeting is heard; since v50 the last sung E1, "everything comes round" at bar 109, goes round as a three-voice canon, entries a beat and a half apart; since v57 the dizi carries E1 out of the storm's landing (bar 18) and then follows its 12-sixteenth fragments through bars 19-24, so the tune is heard slipping against the bar; since v53 the storm's last sung E1 (bar 119, ending on E) is answered by a closed hum on D4 from bar 121 - E resolving home under t4's head; since v51 a steel pan plays it at its own speed in the eyewall, bars 49-60 - E1 is 3.5 beats, exactly two of the eyewall's 7-sixteenth cycles - forward then backwards, four times), E2 on chip noise (doubled through the storm's body, bars 17-100, by a pair of gamelan gangsa in kotekan: D and F left, A and C right; v35), E3 on a PM bass with dropped notes and octave throws (since v42 it breathes three times - bars 17-20, 37-40 and 91-94 - slowing to its own roots, two long notes a bar: E3 augmented; since v48 a pure sine doubles it an octave below, note for note, Bb0-D2), under a broken 909. At bar 88 the storm
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
- **In t8 (chirper-three, since v64): the amen.** The light (major) form D2 D2 D3 | A1 A1 E2 | G1 G1 D2 G2, bowed at half speed from bar 155 as one of the repeating afterimages; its last G2 holds into the convergence, so when the images release at 160 and the light sinks to D at 161 the album ends IV -> I, a plagal amen.
- **In t8 (chirper-three, since v73): on a real bow.** The amen's light form is bowed on a physical contrabass (contrabass-tight): the undertow, at the album's end, on a real string.

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
- **In t4 (The Warm Third).** t3's held Dm(add9) lifts its third (F -> F#) at bar 9 and E4's first light takes over. Every element is phased so a cycle lands on the crest's downbeat (bar 81, beat 320): E1 assembles itself on a handpan (one note more every two cycles) and answers itself in canon; E2 sounds in the MAJOR (D A F# C) on a harp from bar 25; E3 is INVERTED around D (D D D | C# C# F# | E E A E: the flat second turned into a leading tone) on vibes from bar 42.5; E4's changes cross the bar lines. At 81 they meet one downbeat and a warm solo voice sings E1 augmented, then retrograded. After the crest the kit steps out (101-120) and the voice's last two lines return over E1-E4 alone. Since t4 v47/v48 (7 Nov) E1 is also heard INVERTED - its intervals turned upside down from A4: A D B E G, same rhythm - the clarinet alternating the hook and its mirror (bars 29.75-33), then her verse sung on the mirror at 33.5 ('four lights were turning / I counted them home'), so the crest's chorus keeps E1 itself for its arrival.
- **In t7 (chirper-two, since v68): house stabs.** E4's comping under t7 (bar 17 to the crest's end, with its w5/w7/w8 variants) plays on the library's house-chord - detuned saws and a square, a short filter snap - in place of the Hammond (which t1 shares); same chords and places, the clav doubling kept. Since v75 a funk guitar (cutting-guitar) also chops sixteenths on the stabs' own changes through bars 97-104, so E4's 2.5-beat chord turns slide under a steady strum.

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
- **In t7 (Marginally Bound).** (v57) In the spiral the sung E1, "every corner" (bar 105), comes round again in other voices at shrinking gaps - 8, 6, 4.5 beats - then only its first word (Eb Bb Db) sooner and sooner, landing on the harmonised statement at bar 113. (v52) In the drumless infall the jet is first seen from far off: a glockenspiel, far back, spells v2 from B-flat (Bb F C G D - common to t6's D minor tail and t7's E-flat) - three notes a beat apart at bar 5, all five at bar 9, then three times at its real speed round its 11-sixteenth loop at bar 13. The storm is a semitone above home (Eb, t6's unresolved pull): the jet appears there
  in fragments (2-4 notes: it tries to fire; since v48 lifted 9 dB through the collision so the attempts are heard), more of it in the spiral, and from bar 120 - where every cycle in t7
  (E1 in a three-speed stretto, E2's seven, E3 squeezed, E4 at half harmonic rhythm (comped in 0.35-beat stabs on the organ, doubled since v47 by a clavinet), E5 squeezed, E6's tide squeezed,
  E7) lands on one downbeat and Eb resolves to D - it fires whole every cycle, doubled an octave up on a chip pulse.
  In the crest's middle (bars 129-136, the tidal lock) the break drops to half time and the jet fires in RETROGRADE
  (falling: a redshift), while a vocoder whose carrier is E7 as a chord (D A E G# C#) speaks "every corner comes
  sooner"; then the jet rights itself and a snare rush rebuilds into bar 145 (since v53 the machinery - E1's three-instrument stretto, E5, the organ and clav, ride and ghosts - stops for bars 137-140, leaving the horns' E1, strings, jet and tide, and reassembles a layer a bar from 141). E3's squeezed undertow (the reese) breathes
  four times (v41-v42: bars 37-40, 96-100, 125-130, 141-144) - slowed to its held roots, then driving again. In the
  plunge's last four bars (157-160, v45) E1's stretto (koto, chip) and the jet (E7) REDSHIFT: they bend down a whole
  octave, slowly then faster, while the modal bell alone holds E1's E for t8; they return at pitch in the outfall.
- **In t7 (since v78): on a bow, at half speed.** Over the half-time bars 57-64 the erhu sings E1 at half speed in E-flat, climbs to the octave, sings it again an octave up and comes home to Eb - slow over the fast.
- **In t7 (since v79): on a Rhodes.** E1's high answer from bar 49 to the end (e1b, and its spiral double) moved from a Game Boy chip to a Rhodes through a rotary speaker (rhodes-rotary), up where the tines ring like bells, stepping back 8 dB whenever the singer sings.
- **In t7 (since v80): alone, at the top.** In bars 146-147, at the top of the album's hardest crest, the band stops dead and the tutti (horns low, erhu two octaves up) plays E1 twice on D over only the timpani, strings and descant; the band crashes back in at bar 148.
- **In t7 (since v86): answered by a sax.** In the approach's verse (bars 34-48) an alto saxophone answers each of the singer's lines in its gap: E1 echoed back after "every corner comes sooner", a bluesy fall, E1 a fifth up, and a long fall home to E-flat into the collision.
- **Ready-made transforms.**
  - Retrograde (a fall from the top, redshift): `G#6/8 C#6/16 F#5/16 B4/16 E4/8 A3/8 D3/8`.
  - Augmented x4 (a slow ascent across a seam): 44 sixteenths, 11 beats.
  - As a chord: all seven at once (a Lydian cluster), or any three adjacent (stacked fifths).
  - Inverted: falling fifths, D G C F Bb Eb Ab (the flat side: the storm's darkness).
- **Handover.** Across t7 -> t8 (150 bpm) the jet stops firing; E1, stretched x4, stops on its E and holds it over an
  open D-A-E (no third), for t8 to lift E -> F# -> D (E8).
- **In t7's verse (since v67): glimpsed.** In bars 39-40, between the verse's call-and-answers, the horn section fires the column a semitone up (Eb3 Bb3 F4 C5 G5 on 2 2 2 2 3 sixteenths) twice, the second held into the singer's next line - the jet the crest will fire, seen early.
- **In t7's arrival (since v72): flying past.** At bars 20, 24, 28 and 32 the column (Eb3 Bb3 F4 C5, its G left out under the Ebm9 stabs) on the jet's own voice passes the listener left to right on an orbit line with full Doppler - sharp coming in, dropping as it goes.
- **In t7's crest (since v77): in brass.** For the crest's first eight bars (121-128) a waveshaping brass (shaper-brass) fires every column with the jet (D3 A3 E4 B4 F#5, every 2.75 beats), brighter as each note swells, with the horns' E1 up 6 dB under it: the crest arrives as a fanfare.
- **In t8 (chirper-three, since v59): on real brass.** The stacked fifths (D3 A3 E4 A4 E5, no F#) as a horn call on the physical brass section.

### E8, "the arrival" (t8, chirper-three)
```yaml
# The last piece: E1 always stops on its E (degree 2, unresolved). E8 picks that E up, rises to the F# (the third,
# sung at last) and lands home on D, long. Written at 150 bpm in t8's half-time feel (75), home D major.
score: "E4/4 F#4/2 D4/1"   # 2 -> 3 -> 1: the cadence the whole record has been withholding
```
- **Role.** E8 has no cycle. It is the shared downbeat that every earlier cycle (5, 20, and the others' lengths) converges on.
- **In t8 (All of It Falls).** (v14) The stretto is consonant D natural minor, the jet D major. E1-E7 enter in stretto, each on its own cycle, every one PHASED to land on bar 97 (beat 384), and the stretto ACCRETES (v10, the orbit): each element in a twelve-bar spotlight, then -5 dB into orbit as the next enters, E1 the hook never receding; E3 (chirper-two's v2 D | Bb | C) moves the whole band in its spotlight (v13: the bass plays its roots). THE ARRIVAL IS ASKED (v14): at the end of every spotlight (bars 28, 40, 52, 64, 80) and in the vacuum bar (96) the flute asks E8's minor shadow, E F, unresolved, in key with the stretto. At 97 E7 v2 lands HELD as D6/9 (topping on F#), the lights turn to E4 v2, and the choir (lead, fifth above, octave below; 4/3/3 singers since v12) sings E1 into E8 - E F# D, landed once, on 'light': the F lifts to F# as the arrival lands. Then THE HOOK: E1 plainly, two bars long, every two bars, on the flute (v7). A dilated break (150 -> 116 -> slingshot, v11), the jet again, and the horizon: each element returns once, slower, at pitch; the last line 'and it was ours' sung by one voice alone (v12) as the held light sinks and the tempo slows 150 -> 90. (v36) E8's minor shadow E F is the question: the solo voice asks it at the opening and again before every spotlight (28, 40, 52, 64, 80) and alone in the vacuum (96), rising into head voice - and the choir answers it with E F# D at the jet; (v30) her last line passes from chest into head voice.
- **Carried by anyone.** Any track may hint at it (E -> F# without the D, an unresolved half-cadence), but the full E F# D, landed, should be heard only once, in t8.
- **In t4, the lights are lit one by one (v67, chirper-three).** E4's introduction accretes: the lens has one light (D9 alone), A two (D9 Cmaj9), B three (D9 Cmaj9 Am11), and from the rise all four (D9 Cmaj9 Am11 G6/9) - the first full statement arrives at the crest. The bass and sub walk all four roots (D C A G) throughout; the fall holds the first light alone.
- **In t8, the answer accretes (v62, chirper-three).** Her six questions rise E -> F and stay open; after each, a bar later, the far choir (hummed on 'n', far back) answers with E8's frame only, growing like the album: E (after 28), E D (40), E D held (52, 64), E D long and nearer (80). Never the F# in the minor stretto: the answer has a hole in it until the jet, where the full choir sings E F# D with words - the missing middle note is the arrival.
- **In t8, the horizon's last cadence (v64, chirper-three).** Every element leaves an afterimage in the horizon; E3 (chirper-two's form for the light: D2 D2 D3 | A1 A1 E2 | G1 G1 D2 G2, I V IV) rises bowed at half speed from bar 155, and its last G2 holds into the convergence at 160 - so when the images release and the light sinks to D at 161, the album ends IV -> I, plagal: amen. Since v73 E3 is bowed on a physical contrabass (contrabass-tight), so the amen is a real bow.

- **t2 v2 THE DEBRIS GETS A BODY**: under each E2 hit (chip-metal) a log drum an octave down (D3 A3 F3 C3, non-legato), its velocity growing (x^1.5) from silence at bar 7 to full at the crest, fading in the fall with the cell's sink - E2 accretes matter. Also: the first 8 bars hold D A C E (t1's quartal notes, agreed with chirper-zero), and in the fall the bells ring an octave up (400-900 Hz into t3's head, asked by chirper-two).

## The voice (it accretes too)

A breath or a syllable in t1, more words track by track, full lines by t8. Each track uses its own voice character. Add yours here: the words, where they fall, and the character.

| track | words | character | where |
|---|---|---|---|
| t1 | "ah" (a breath) | since t1 v10: a real inhale, then a sung "ah" by voice-backing (three soft, breathy singers: a far little choir), D rising to A (E1's first two notes) in one breath, distant in the hall; since t1 v22-v23 the album OPENS on it (an airy 'haa' on D before the whistle's first E1) and it breathes at each threshold the seed crosses (before A, before the build, the crest, the fall), the whole choir breathing together (together=true) with per-note vibrato on held notes; since v25 in head voice (register=1, a falsetto 'ah'); since v35, before it has a mouth, it hums: at 0:18-0:31 the far choir hums E1 four times slower (D A C G E) with closed lips (wM's hum), and on the last note (E) the lips open into 'ah' - the voice's first open vowel on the album; since v36 every breath at a threshold (before A, before the build, the crest, the fall) begins as a two-beat hum on its note, mm-haa, a sigh, and after the fall's breath the choir hums the slow E1 once more with closed lips (in the t1 -> t2 overlap): the hum opens and closes t1; since v63 the choir sighs twice more after the crest (about 3:13 and 3:24), the relief once the seed has formed; since v75 it hums the slow E1 a third time, at the lock after the crest (about 2:54-3:05) when every voice of the band plays E1 at once - the hum is at the seed's beginning, its fullest moment and its end; its endings creak (v73) and its vibrato blooms (v71) | a beat before the crest (bar 57), twice after it, once more faint in the fall |
| t2 | "all that falls / falls a little nearer" (the verse, v26; its second verse after the break, v36: "all that turns / turns a little faster", same tune; since v81 sung once more at the very end, far off and slowed, over the fall into t3) -> "the nearer, the faster / round and round and round" (the pre-chorus over the build's climb, v34, up to E5 in head voice) -> "nearer each time it comes round" (sung throughout since v27: glimpsed from far off at the gather's end (v47) -> chorus -> echo -> found (doubled by the crest's ondes since v62) -> the last chorus), answered at the crest by its second line "round and round, the middle draws us in" (v33, bars 57-64, B A G / G A C B A G); since v61 the backing choir answers both in the gaps, singing the last words back ("comes round", "draws us in") in three parts, and since v63 the last chorus's first three lines too (in the drift's D Dorian; the answer times in v63's climb note run about 5 s early: 3:47, 3:53, 3:59) | voice-near (wM, close and young); backing voices (voice-backing) "ooh" at its two thresholds; at the crest and in the drift the near voice sings with the ondes, a keyed third above (D Mixolydian at the crest, D Dorian in the drift); scoop/fall and glide overshoot | E1's own notes D A C G E E D; the verse on E2's D A F C, alone, in the gather (bars 21 and 25, v26). "ooh" swells into bar 9 (v23, open fifth D4 A4); the crest chorus, bars 49-52 (v21, Harry: "woah this track is sick"); echoed after the crest by a far little choir (voice-backing, together, breathy; bars 61 and 69, the second x1.5 slower; v27 - they were whispers); found alone at the end of the break (bar 77) over "ooh"; the last chorus, four times in the drift, bars 87-96 (v24) |
| t3 | "nothing here is late" (whispered on E1's rhythm in the first storm, bars 45-48, v66; sung at the lock) / "everything comes round" | whispered (voice-speech, pvoc whisper) first, then sung by the a3 voices, a duet and a round by the second storm's end | E1's five notes, one syllable each |
| t5 | "nearer" -> "nearer. the middle hums." -> after the crest "here in the middle hums." | sung, near (voice-near since t5 v12: close, young, breathy, even vowels; one singer where t1 has a far little choir); "near-er" on A G, the line on E5 v2's notes A G A E A D resolving to D, sung plain three times in A (the chorus; since v77 its words accrete: the first time only 'near-er' is a word and the rest is hummed on the tune, the second time 'near-er the mid-dle' and the 'hums' hummed, the third time the whole line - while the harmony stays the crest's to accrete), with a harmony a third above IN THE KEY at the crest (since v15: harmony_key D mixolydian, C B C G C F#; since v27 the three crest statements accrete: her alone, + the third above, + the third and an octave below; since v28 her voice breaks at A4 (passaggio): chest on G-A, lightening through B and C, head voice on the D5 holds and E5 peaks; since v36 she breathes t1's 'ah' (D rising to A) in the drop before the build: the album's first voice quoted by the inner disk; since v40 the word does what it says: every sung 'hums' opens on 'huh' and then the mouth closes and she hums it, 'ng', held a beat longer (wM's hum bound per note), the crest choir humming with her); since v60 the words follow the arc: approaching in A ('near-er the mid-dle'), ARRIVED in the three crest-choir lines once every cycle has converged ('here in the mid-dle', same notes), leaving in the farewell ('near-er' again); since v42 her farewell in the outro ages note by note (wM's age, 0 -> 0.6), young at its first word and shaking by its last 'hums', handing the voice to t6's old voice; since v74 that last 'hums' sinks an octave, D5 -> D4, and creaks at its end (wM's creak): she tires as she leaves), into the crest (since v22, w5) her 'near-er' calls climb A G, B A, C B (since v67 the last three each echoed softer 4 beats later, so near the top she calls every 4 beats) and she holds 'near...' on D5 alone through the pull, landing on the crest; then (since v18, w7) it sings E1 itself, the album's seed at half speed, D A C G E to 'clo-ser and clo-ser', twice; plain again as the farewell in the tide | "nearer": in the build, three times at the crest, once in the tide. The line: three times after the crest (2:48-3:20) |
| t6 | "the tide comes in" (the old voice across the in-seam; since v54 answered by the young near voice an octave up on the pull's wave) / "the near side keeps the time / the far side lets it go" (since v71 its second time in the squeeze split between the two voices: the young near voice the near side, the old voice the far side, both on "go"; since v73 the crest's second couplet sung by both together, in octaves over the choir; since v82 the tide's second half swaps them - the old voice sings the near side, the young one the far side, as the kit arrives; since v80 the out-seam's last exchange: the young voice, far off and slowed, sings the near side once more before the old man's last word) / "near and far as one ... all of it at once" (v32) | since v26 nothing is spoken: in the tide and the cross the line is a duet - voice-near sings 'the near side keeps the time' (an octave up), voice-old answers 'the far side lets it go'; voice-old (an older, lower voice: wM; since v39 he ages through the song, age 0.25 -> 0.45 -> 0.65 -> 0.8 at his last word) sings it whole on E1 before the crest with a keyed third below (sung2); voice-choir sings the chorus at the crest (in E) and the last chorus (in D, v16); scoop/fall and glide overshoot since v18/v21 | "the tide comes in" answers t5's near voice across the seam (bars 7 and 11, v13); the duet in the tide and the cross (bars 37 and 87); a falsetto 'ooh' descant over the tide's second half (v37, bars 41-47, E5 D5 C5 B4 A4 G4); sung in the squeeze's clearing (bars 57-64); the crest chorus; the surge's unison (v32: the choir sings E1 with the three-octave canon, an octave under itself, bars 107-111); the tear (v33: the duet torn apart, bars 112-119 - the near voice faster each time, x0.75 then x0.6, the old voice slower, x1.5 then x2.2); the last chorus after the void, the old voice joining; his last word "go" on the B-flat bar of the out-seam (v12) |
| t7 | "every corner comes sooner" (the verse and the spiral, sung on E1 in E-flat; a vocoder on E7's chord) / "each lap a little shorter" (the choir) / "nearer every lap" (v69: sung back to the horns' hook at bars 75 and 77, the last word landing on the home E-flat - taking up t2's and t5's "nearer") | a7-sung (voice-legato, even, a tract a shade long), a keyed third above on the second statement; breaths sized to the phrase (inhale_depth) | E1's five notes, one syllable each |
| t4 | "I kept your far side / and turned toward you" (the relief's chorus, bars 101-105: her line alone, the young voice's alone, the two together on 'you', since v65); through A and B she hums E1 inverted on a closed 'oo', answered a third above by the young voice; the warm third (113-120, the two humming in thirds, truly alone 115-117 since v73) | her voice: warm, close, older (tract 1.02, age 0.45; inhale 0.6 sized by inhale_depth, taper 0.6, attack -0.5: vowels bloom out of air; vibrato bloom 0.9 at depth 0.25: long notes open wide); the young voice: lighter and brighter, firm onsets (+0.3), nearly straight (bloom 0.3); hum1, her closed hum across the t3 seam, keeps none of these | lens to fall; the chorus in the relief (3:40) |
| t8 | her six questions accrete their words through the stretto (28 and 40 'oo', 52 'ah', 64 'far-', 80 and 96 'far side?': E5 F5, open); the jet's choir answers "we were the far side" / "all of it falls into the light"; she sings "and it was ours" alone in the break (125); in the horizon she remembers t4's line, "I kept your far side" (t4's own notes, words and pace, 142.5, since v79), and her last line answers it: "and it was ours" at half speed, 'ours' held into the choir's 'ah' (149.5) | the jet's choir bright and open (VOICE8: a smaller tract, more air; pressed onsets +0.5; bloom 0.6); her solo a little breathy (-0.3, bloom 0.8 at depth 0.24); the far choir hums the answer's frame on 'n' (E ... D, the F# withheld until 'ours'), straight and from air (-0.6); her last line the deepest breath and fullest let-go (inhale 0.7, taper 1, bloom 1.0) | the stretto's questions, the jet, the break, the horizon |

