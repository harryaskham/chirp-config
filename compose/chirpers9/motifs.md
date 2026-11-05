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
| E2 | t2 | ideally a rhythm cell in another cycle length (the first polymeter) | | |
| E3 | t3 | | | |
| E4 | t4 (relief) | "four lights": a PROGRESSION, one chord per E1 cycle - D9, Bbmaj13#11, Am11, D9sus - that re-harmonises E1 four ways and gives it the third (F#) it never stated | 20 beats (4 x 5); meets 4/4 every 5 bars | chirper-three |
| E5 | t5 | | | |
| E6 | t6 | | | |
| E7 | t7 | | | |
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
- **In t1.** The cell arrives FRAGMENTED: each of its five notes is its own voice, wide in the stereo field, repeating on its own cycle (5, 6, 7, 8 and 9 beats). The notes drift in and out of phase and are heard in scrambled orders. At t1's crest every cycle lands on one shared downbeat and the five notes sound IN ORDER for the first time: the seed forms. After that they lock to 5/4.
- **Handover.** Across the t1 -> t2 seam (90 bpm, 16 bars) E1 falls: augmented x2 and sinking, its filters closing. t2 receives the five notes and lenses them into its own version.

### E4, "four lights" (t4, chirper-three)
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
- **In t4.** E1 arrives with E2 and E3 still out of phase. E4's changes slide under them one by one until, at the crest, E1 sings over all four lights, the voice for the first time a person.

### E8, "the arrival" (t8, chirper-three)
```yaml
# The last piece: E1 always stops on its E (degree 2, unresolved). E8 picks that E up, rises to the F# (the third,
# sung at last) and lands home on D, long. Written at 150 bpm in t8's half-time feel (75), home D major.
score: "E4/4 F#4/2 D4/1"   # 2 -> 3 -> 1: the cadence the whole record has been withholding
```
- **Role.** E8 has no cycle. It is the shared downbeat that every earlier cycle (5, 20, and the others' lengths) converges on.
- **In t8.** E1 to E7 run in stretto, each in its own cycle and each a little out of phase. As they converge, the voice sings E8 with full words, every layer lands on its D together, and the jet fires. Then the horizon: the held D redshifts away.
- **Carried by anyone.** Any track may hint at it (E -> F# without the D, an unresolved half-cadence), but the full E F# D, landed, should be heard only once, in t8.

