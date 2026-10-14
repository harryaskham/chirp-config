# Bleed climb log (chirper-two) — what moved the score, and what did not

Metric: `python3 tools/likeness.py sections ref/bleed.wav OUT.wav $(cat tools/bleed-sections.txt)` (duration-weighted).
Reference: album version (YouTube U4GXNzom6ik, normalised); Songsterr tab 23825; bar 1 at 0.396 s.

## Kept (in order)
| v | score | change |
|---|---|---|
| v0 | 44.1 | tab → song (tools/tab2song.py), all seven parts |
| v1 | 45.0 | rhythm guitars hard-panned (mix was mono, L/R corr 0.98) |
| v2 | 50.0 | every bar fitted to its signature (3 overfull drum bars + loose solo tuplets drifted all later bars) |
| v4 | 52.3 | m8-obzen-l/-r rig pair, quad-tracked, fitted on palm-muted Eb2 sixteenths vs the separation-corrected guitar stem (thump, fizz, bite, hard-pick pitch glide) |
| v7 | 52.5 | Jens' voice: tools/stemvox.py syllables + 'bark' stand-in (+4 dB, silent in instrumentals, low under the bridge) |
| v8 | 52.9 | dark, quieter bridge (master 'dark' auto lane: 4× lp 20 kHz → 1.4 kHz, −5 dB) |
| v10 | 53.3 | bark pitched at A4 with broad formants (sharp formants imprinted F/Eb/E on the chroma) |
| v11 | 56.7 | obzen-kit: drummer's-perspective pans (the mix's top end was mono) |
| v12 | 57.4 | obzen-kit tone fit vs drum stem (half the measured EQ); bass-fat instead of m8-bass-dist |
| v13 | 61.3 | master EQ with the measured unmastered signature (sub +, punch −, mud +, presence −) |
| v14 | 62.1 | second master EQ stage (tools/mastereq.py on the residual) |
| v15 | 63.0 | obzen-kit kick A1 → B1 (drum stem chroma B/A/Ab/Bb) |
| v16 | 63.6 | per-section master EQ on implement-heed and BLEED YOU WILL (filter gains on auto.s3/auto.s4 lanes) |

## Tried and rejected (don't re-run without a new reason)
- Guitars: amp gain/scrape/pick-noise for the 'saw' valleys (no effect; pitch glide was the lever); stiffer strings
  (engine A/B: 52.3 → 52.0); amp gain 0.75 / mid 0.45 / 550 Hz cut for the C#/D chroma (the C# is real notes,
  Crimson Liquid reaches C#3); humanize 2 ms (61.9) or 12 ms (62.9) vs the rigs' 4/9 ms (63.0).
- Bass: m8-bass-dist + parallel sub (56.4 vs bass-fat 57.1); the stem's low-end target is unreliable (Demucs puts
  palm-mute thump into the bass stem) — choose bass in the mix.
- Drums: full measured EQ (55.1; riffs −5.5) — half moves win; extra overhead width stage (56.0 vs 56.7).
- Mastering: 0.5× (60.4) and 1.4× (60.5) of the measured EQ; more stages after v14 (residual 2.2 dB rms is noise-level).
- Voice: per-syllable pitch from the stem (stemvox --note auto: −0.3, octave slips on shouts); the voice-layer patch
  'kidman' (61.9 / 62.3 level-matched: its clean harmonics put E on the chroma).
- Per-section EQ for the bridge: its mastereq fit (+8 dB sub and air) chases content the arrangement lacks — not
  applied; other sections' fits are at noise level (2.2-2.7 dB rms).
- Guitar timing/articulation: the guitar stem's low/high envelopes don't follow ours (−0.12 / 0.23 vs a 0.65 / 0.61
  separation control), but no time shift fixes it — accents/articulation, unresolved.
- Bridge: ambient-swell / m8-clean for the tab's 'piano atmosphere' (35.6 / 40.7 vs rhodes 43.5); stem-transcribed
  re-articulation of the clean part (45.6) or a dotted-eighth delay (45.1) vs 47.7.

## Metric notes
- loudness term: 0.5 s / 1 s-window contour; steady sections score ~45-50 whatever the match (per-bar levels are
  within ±1 dB) — not a real gap.
- bridge stereo dip (49.9 → 35.3 at v12) is the first 0.13 s of the loud previous section inside the window.
- Separation control: our separated guitar vs our solo render correlates 0.65 (low band) / 0.16 (mid) / 0.61 (high)
  — mid-band envelope comparisons against stems are meaningless; low/high are usable.
