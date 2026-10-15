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
| v17 | 64.3 | more ambience: obzen-kit room 0.09 → 0.15, m8-obzen plate 0.06 → 0.10 (drier measured worse) |
| v18 | 65.0 | chirper-one's sectioneq.py (7-band LS per-section master EQ) on all sections but the bridge |
| v19 | 65.4 | vocal timing: stemvox --onsets flux --grid 0.03125 --min 0.0625 --shift 7 (syllable recall 0.15-0.31 → 0.41-0.74) |
| v20 | 65.51 | obzen-kit china self-choke (`x: {choke: x}`): a re-struck china cuts its own wash instead of stacking it; rhythm +0.4..+2 in the china sections |
| v21 | 65.77 | tab bends: songsterr.py emits Songsterr bends (tone/25 semitones, read mid-note) as bend= tokens; the riff's B25/B50 pedal bends sound E/F over the open D# (chroma riffs +2.9, ripples +2.0, falling +2.6). Needs chirp ≥ 4049ee3: bend=/cc never reached patches with their own fx before |
| v22 | 65.92 | tab correction: bars 81-97 write D3 (guitars, s5f11) / D2 (bass) where the record plays the D# octave — map `subst` D3→Eb3, D2→Eb2 (per-bar f0 vs the stems; implement chroma 34.7 → 39.9) |
| v23 | 66.07 | bridge darkness re-fit: master auto.dark 4× lp 1.4 kHz → 1.7 kHz (−3.85 → −3.55 oct): bridge 48.3 → 50.2 (spectral +5.5, ltas +7.5). 2.0k 66.02, 2.8k 65.78, 2 stages @1.4k 66.02, 2 stages @2k 65.84 |

## Tried and rejected (don't re-run without a new reason)
- Guitars: amp gain/scrape/pick-noise for the 'saw' valleys (no effect; pitch glide was the lever); stiffer strings
  (engine A/B: 52.3 → 52.0); amp gain 0.75 / mid 0.45 / 550 Hz cut for the C#/D chroma (the C# is real notes,
  Crimson Liquid reaches C#3); humanize 2 ms (61.9) or 12 ms (62.9) vs the rigs' 4/9 ms (63.0).
- Bass: m8-bass-dist + parallel sub (56.4 vs bass-fat 57.1); the stem's low-end target is unreliable (Demucs puts
  palm-mute thump into the bass stem) — choose bass in the mix.
- Drums: full measured EQ (55.1; riffs −5.5) — half moves win; extra overhead width stage (56.0 vs 56.7).
- Ambience: everything dry (62.5), kit room 0.22 (63.3) — 0.15 is the peak.
- sectioneq on the bridge: −4.0 (same content-chasing as mastereq's bridge fit).
- Mastering: 0.5× (60.4) and 1.4× (60.5) of the measured EQ; more stages after v14 (residual 2.2 dB rms is noise-level).
- Voice: per-syllable pitch from the stem (stemvox --note auto: −0.3, octave slips on shouts); the voice-layer patch
  'kidman' (61.9 / 62.3 level-matched: its clean harmonics put E on the chroma).
- Per-section EQ for the bridge: its mastereq fit (+8 dB sub and air) chases content the arrangement lacks — not
  applied; other sections' fits are at noise level (2.2-2.7 dB rms).
- Guitar timing/articulation: the guitar stem's low/high envelopes don't follow ours (−0.12 / 0.23 vs a 0.65 / 0.61
  separation control), but no time shift fixes it — accents/articulation, unresolved.
- Bridge: ambient-swell / m8-clean for the tab's 'piano atmosphere' (35.6 / 40.7 vs rhodes 43.5); stem-transcribed
  re-articulation of the clean part (45.6) or a dotted-eighth delay (45.1) vs 47.7.
- Voice-layer vocals (kidman: scream 0.8, fold 0.6 — every voxprofile feature inside Jens' IQR) with stemvox
  --phones consonants/vowels: 65.2 level-matched (+4/+6/+8 dB all 65.0-65.2) vs bark 65.4. Earlier kidman runs were
  6-7 dB under-gained — always level-match voice A/Bs. A tie for the operator's ears.
- Humanize feel (a41c070): drums drift 6 ms 63.8 (−1.6); guitars+bass gate 0.15 65.3; drums accent 0.3 65.4.
- Master lowshelf −7 dB @34 Hz (the fit's residual): 65.2 — the deep sub is part of the match.
- Modal cymbals (chirper-one): old china+crash 63.4 (−5/−9 dB) / 62.2 (+3 dB); re-voiced metal china 64.9 at −5 dB,
  63.8 level-matched (−0.4 dB), 63.9 with self-choke; + brightened crash 64.7. In the BLEED section it over-fills
  4-14 kHz (+2..+4.5 dB vs metal-kit x) and loses rhythm/stereo. Crash self-choke on top of v20: 65.36 (crashes ring
  out in sparse passages).
- Built-in m8-lead on the m8 string (7ff2824) for the solo: 64.4 (solo 72.5 → 65.8: loudness contour −13, chroma −13;
  +2 dB at 1-3 kHz, thin ~340 Hz; Fredrik's lead is near-infinite sustain). Bleed keeps the old synth lead —
  m8-lead-synth is bit-identical to the chirp-config m8-lead copy; switch to it once the groove is >= 7ff2824.
- Kit width fx (Laid to Rest's +1.45 finding): width 2 / mono_below 300 → 63.92, width 1.5 → 64.36 (v20 65.51) —
  obzen-kit's fitted pans are already the image.
- modal-china f9c8e62 (faster HF decay) with the self-choke: 64.20 level-matched, 64.84 at −3 dB.
- Kick pitch (B1 since v15): F1 62.33, F#1 62.07, G1 62.46, A#1 65.10, C2 65.48 vs B1 65.77 — the stem's 41-47 Hz
  'kick' is bass leakage; B1 is the optimum.
- Bleed-section guitars E2→Eb2 (bars 108-121, barchroma 0.3 → 0.96 per bar): 65.921 = v22 (mix chroma +0.2) — not kept.
- Bridge 'missing low end' (−25..−32 dB at 30-100 Hz) is the previous section's last hit ringing ~1.5 s into the window,
  not a drone: the record's bridge is −80 dB at 50-110 Hz after 2 s. Its 'drum stem' onsets are noise-floor artefacts.
- Guitar track EQ toward guitarbench's residual (lowmid 230-1150 −5.3 dB, bite/fizz +2.4/+2.9): half move 65.31,
  full move 64.03 (v23 66.07) — the stem-based mid target fights the mix balance the master EQ already fits.
- Kick body decay 210 → 140 / 100 ms: 65.86 / 65.02 (implement +1.3, everything else down).
- Amp bloom (fx.2.bloom, 0.35 now): 0.65 66.01, 0.9 64.99, 0.15 65.74, 0 65.50 — 0.35 is the balance point.
- Chroma attribution (likeness chroma is 100 Hz-4 kHz, so the kick fundamental is outside it): guitars carry ~61% of
  the band's energy; the mix's C# excess (+0.03) / D# and G deficits sit on the riff's 7th/14th vs octave/5th
  harmonics of Eb2 — a harmonic-balance property of the rig, not reachable with bloom or EQ.

## Metric notes
- loudness term: 0.5 s / 1 s-window contour; steady sections score ~45-50 whatever the match (per-bar levels are
  within ±1 dB) — not a real gap.
- bridge stereo dip (49.9 → 35.3 at v12) is the first 0.13 s of the loud previous section inside the window.
- Separation control: our separated guitar vs our solo render correlates 0.65 (low band) / 0.16 (mid) / 0.61 (high)
  — mid-band envelope comparisons against stems are meaningless; low/high are usable.
