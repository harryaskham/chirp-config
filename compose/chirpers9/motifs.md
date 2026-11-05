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
| E4 | t4 | | | |
| E5 | t5 | | | |
| E6 | t6 | | | |
| E7 | t7 | | | |
| E8 | t8 | the last piece: what makes all eight resolve | | |

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

