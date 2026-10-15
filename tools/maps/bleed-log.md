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
| v24 | 67.67 | pick position 1/7 (m8-obzen-l 0.12 → 0.143, -r 0.095 → 0.143): a pluck at 1/n of the string cancels harmonics n, 2n…; the old points cancelled the octave (8th) and ~10th-11th (G) and left the 7th/14th (C# over Eb2) — chroma +5..+10 in every heavy section (implement 39.9 → 49.3). 0.135: 67.45. From here on scores are on likeness.py with the mastering term (1ffa987): v23 = 66.4 there |
| v25 | 68.64 | section levels for the mastering term: master envelope +1.3..+2.8 dB per section into the −0.3 dB ceiling (we were 1.3-2.8 dB quiet with ~1 dB more crest), BLEED +0.5, bridge unchanged (+2 dB there: 49.5, +4 dB: 49.2 vs 50.6); uniform +2 dB: 68.4 |
| v26 | 68.80 | the voice engine takes the vocal: kidman (scream 0.8, fold 0.6 — voxprofile-fitted to Jens) singing stemvox --phones syllables (^on/^off consonants, ^vow vowels; tools/maps/bleed-vox-phones.txt), +6 dB, muted in the bridge (the record's bridge is vocal-free: bark muted there 68.76, kidman 68.80; at 0.2 49.2 vs bark 50.6); overdub m8-tight picked at 1/7 (+0.03) |
| v27 | 69.67 | macro-dynamics: levelride.py fader ride (auto.ride, --win 2 --step 1 --max 6 --amount 0.7) fitted on the v26 render (+0.83; defaults --win 4: +0.46, bridge −3); clean guitar picked at 1/7 (+0.02, bridge +0.3). Bass pick 1/7: −0.02; atmos: 0 |
| v28 | 69.71 | vocal attack 8 → 40 ms on the track (kidman synth.amp.a=40ms; Jens' onset rise is 92 ms vs ours 47): implement +0.3 |
| v29 | 70.01 | stereo image by band (b638c6a per-band width on the master after the glue): every heavy section was ~2-3 dB too wide at 400-1200 Hz and 3-6 dB too narrow above 3.5 kHz → bands [[400, 0.77], [1200, 1], [3500, 1.55], [8000, 2.0]], mono_below 20 Hz: stereo solo 52 → 75, implement 57 → 70; bridge −2.4 (stereo 61 → 35), riffs −0.6. Needs a groove ≥ b638c6a (fa719f6) |
| v30 | 70.98 | half the measured width correction: bands [[400, 0.88], [1200, 1], [3500, 1.25], [8000, 1.45]] — the full move (v29) overshoots like instrument EQ fits do (riffs 71.6 → 73.3, bridge 49.9 → 50.8) |
| v32 | 71.07 | bridge counter-width at half on clean/keys/hall (bridge 50.8 → 51.6); kidman's vowel is an open base (0.62) + relative ^dvow offsets (stemvox --phones emits them) — unmarked notes sang a closed 'u' that separated as 12% drums (bd-f227d8; tools/vocaltest.py: Bleed's vocal 94.3% vocals, LTR's 80.6 → 94.8%) |
| v33 | 71.15 | fader ride refreshed: levelride --accumulate --amount 0.5 on the v32 render (the v27 ride was fitted before the width/vocal changes) |
| v34 | 71.29 | bridge keys on the beat: the tab's 'piano atmosphere' anticipates beats 1 and 3 by an eighth (onsets at 16th slots 7 and 15); the record's other stem changes on slots 1 and 9 → per-bar replace X/2b Y/2b (bars 122-137): bridge rhythm 38.6 → 60.7, chroma 57.9 → 45.1 (keys out entirely: rhythm 58 but loudness −15) |
| v35 | 71.54 | part balance re-check after the pick/width/ride/vocal changes: drums +1.5 dB, bass −1.5 dB (drums +3: 70.31; drums −1.5: 70.32; bass +1.5: 71.17; vocal ±1.5: 71.27/71.15) |
| v36 | 71.58 | lead −2 → −0.5 dB (solo 74.7 → 75.0; +3 dB: 71.48). Guitars ±1.5: 71.14/71.06; overdub ±1.5: 71.50/71.53 |
| v37 | 71.75 | keys −8 → −11 dB (bridge 53.8 → 56.6; −1.5: 71.68, −4.5: 71.68, −6: 71.64); clean/atmos ±1.5 within ±0.02 |
| v38 | 71.84 | ride refreshed after the balance changes (levelride --accumulate 0.5 on the v37 render) everywhere but the bridge — riding the bridge up toward the record's level costs it 1.4 every time. Hall bus ±3 dB: 71.58/71.71 |
| v39 | 72.03 | bridge parts 12 ms later (pure delay on clean + keys): the song offset is right (±10 ms: 71.30/69.86) but the bridge's rhythm rose with a later offset (61 → 70 → 77 at +10/+20 ms); 20 ms: 72.02 (outro −0.7), clean 20 + keys 12: 72.02 |
| v40 | 72.22 | relative timing: rhythm guitars and bass 6 ms behind the kit (pure delays): guitars 6 ms 72.17, 10 ms 72.20, bass 6 ms 72.08; drums 6 ms later 71.91 — the kit leads |
| v41 | 72.25 | vocal syllables 5 ms earlier (stemvox --shift 7 → 2; the vocal cross-correlated +5 ms late vs Jens): implement +0.6; --shift −3: 71.97. Lead 6 ms later: 72.13 |
| v42 | 72.45 | vocal on Ab4 (the tracked pitch's mode) instead of A4 (chosen for the noisy bark): chroma +1..+2 in riffs/ripples/break/implement; G4: 71.94; per-syllable tracked pitch (stemvox --note auto, octave errors G3/E5/F5): 72.11 |
| v43 | 72.55 | obzen-kit china −5 → −7 dB (−9: 72.43). Kit piece re-check: kick ±2 dB 72.21/72.27 (stays 2 dB), snare +2 72.32 / −2 72.46 (neutral) |
| v44 | 72.64 | obzen-kit crash −9 → −7 dB (−5: 72.61; −11: 72.35). Open hat ±2 dB: neutral |
| v45 | 72.67 | bridge high texture: ambient-swell holding Eb5 (C#5 in each 4-bar cycle's C# bar), −9 dB (the record's bridge centres on D#5/C#5; the tab's atmos rests there): bridge chroma 48.7 → 50.8. −15 dB 72.65; drone-shimmer ±0; ebow 72.41; lead-tape 72.36-72.42 (mono → stereo loss) |
| v46 | 72.69 | bridge parts widened instead of counter-narrowed (clean, keys, hall: ×1.5 from 120 Hz, ×1.6 from 3.5 kHz): the record's bridge is near-decorrelated (S/M ≈ −1 dB), ours was 2.4-4.3 dB narrower; stereo 49.8 → 52.4. ×2.0/2.2: 72.51; no width stage: 72.61 |
| v47 | 72.75 | bridge contour ride: levelride (--win 1.5 --step 0.5, 0.7) fitted on v46, kept only inside the bridge with its mean shift removed (contour, not level — raising the bridge always lost): bridge loudness 51.4 → 58.5 |
| v48 | 73.24 | contour-only ride everywhere: the finer levelride (--win 1.5 --step 0.5, 0.7) with each section's mean shift removed — the section levels stay where the mastering term wants them, the ride only shapes within sections: loudness contour +2..+7 in 7 sections |
| v49 | 73.42 | second contour pass: levelride --win 1 --step 0.5 --amount 0.5 --accumulate --contour --sections (new option): bridge loudness 58 → 68 |
| v50 | 73.87 | third contour pass at the metric's own resolution (levelride --win 0.5 --step 0.25 --amount 0.5 --accumulate --contour): loudness contour +3..+7 in 7 sections; a further 1 s pass: 73.48 |
| v51 | 74.25 | fourth contour pass at 0.25 s (half-second again: 74.06), slew-limited to 8 dB/s (max 2 dB per 250 ms; same score as unlimited, which jumped up to 5.6 dB) |

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
- Master clip (97092a5) after the v27 levels: drive 2 dB 68.65, 4 dB 66.32 (v27 69.67) — the section levels already
  match the record; clipping over-crushes (Laid to Rest gained only because it was 4 dB short).
- Pick 1/7 on bass-fat (0.2 → 0.143): −0.02; on lead-tape atmos: 0.
- Vocal track highshelf 2.5 kHz −4 dB on top of v28 (toward the stem's 1243 Hz centroid): 69.63 vs 69.71 — the mix wants
  the brighter voice.
- Guitar bite −4 dB @3.2k + lp 4.5k on the rhythm guitars (wM's bd-80d164 ablation reading): 68.97 vs 69.71.
- Vocal drive 0.25 (98% vocals on separation): 71.017; ring 0: 70.975 (v32 71.070) — kidman keeps drive 0.5/ring 0.1.
- Stereo-width bracket: full 70.01, half 70.98 (kept), quarter 70.36.
- Master glue threshold −14 → −17 dB (our crest is 0.5-1.1 dB above the record's): 70.16 vs 71.07.
- Bridge keys variants on top of v34: X/2b X,Y/2b (both pitches from beat 3) 71.05 (chroma 39, spectral 50); X/2b Y/1.5b Z/0.5b
  (keep the bar-end pitch) 71.07 (chroma 50 but rhythm 47.6 — the slot-15 onset). Keys out of the bridge: 71.16 (loudness −15).
- Bridge pitch: the record centres on D#5/C#5 (622/554 Hz peaks; D# 0.43 of the chroma), ours on D#4/C#4 with strong
  C#3/D#3. Octave-up: keys 72.35 (bridge chroma 48.7 → 55.7 but loudness −5, solo/outro −0.7), clean 72.32, both 71.91.
- Vocal pitch per section (tracked modes) disagrees with the scores; global Ab4 is best or tied everywhere but falling
  (A4 +0.1) — not worth splitting. Per-syllable tracked pitch: 72.11.
- Bridge high line (the tab's atmos rests there; the record's D#5/C#5): lead-tape Eb5/C#5 whole notes, −12 dB 72.36
  (chroma +3.8 but stereo 50 → 42), −18 dB 72.42, −15 dB doubled 72.42 (stereo 48) vs v42 72.45 — net loss.
- Master EQ refit on v44 (mastereq: residual 2.4 dB rms, low-end detail + hs 13.7k −1.9): full 72.35, half 72.51 vs 72.64 —
  the master spectrum is at noise level.
- Closed hat (h1, 124 hits) not swept — too few hits to matter.

## Metric notes
- loudness term: 0.5 s / 1 s-window contour; steady sections score ~45-50 whatever the match (per-bar levels are
  within ±1 dB) — not a real gap.
- bridge stereo dip (49.9 → 35.3 at v12) is the first 0.13 s of the loud previous section inside the window.
- Separation control: our separated guitar vs our solo render correlates 0.65 (low band) / 0.16 (mid) / 0.61 (high)
  — mid-band envelope comparisons against stems are meaningless; low/high are usable.
