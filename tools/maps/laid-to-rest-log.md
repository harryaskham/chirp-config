# Laid to Rest climb log (chirp-climb3)

Metric: likeness.py sections on tools/laid-to-rest-sections.txt (record-aligned since v4). Scores are unrounded totals.

| Version | Change | Score | Kept |
| --- | --- | --- | --- |
| v2 | tab2song from Songsterr 12062, scorealign intro tempo, beatgrid (unwrap) body | 38.104 | |
| v3 | + kidman vocals (stemvox flux, per-syllable pitch); bark 38.458, bark fixed F#4 38.268 | 38.492 (38.688 on v4 sections) | yes |
| v4 | dtwgrid: DTW-anchored grid (beatgrid locked to the wrong eighth; breakdown 199 not 208) | 50.228 | yes |
| v4b | vocals re-transcribed on the v4 grid | 50.118 | no |
| t445 | a4 445 (record measures +17..+20 c) | 49.851 | no |
| d4 / t445d4 | drums +4 dB | 49.153 / 48.877 | no |
| g8 | rhythm guitars stiff 0.8 | 50.035 | no |
| v5 | g8 + snare pitch Ab3 (record's ringing Ab4 snare; ours read A) | 50.455 | yes |
| sab | snare Ab3 alone (no stiffness): stiffness was costing ~0.2 | 50.659 | (base for v7) |
| v6 | v5 + master EQ from mastereq.py (53 -4.5, 85 +2.4, 107 +3.4, 428 -2.3, 1.1k +2.2, hs 13.7k -4.3) | 52.193 | yes |
| l1 | v5 + master gain lane: pre-choruses -0.5 dB, choruses +0.5 dB (record's chorus lift; ours was inverted) | 51.976 | (combine) |
| m05 | master EQ at 0.5x | 51.440 | no |
| l2 | lift lane +-1 dB (on v5) | 52.225 | (combine) |
| v7 | snare Ab3 (no stiffness) + master EQ + lift +-1 dB | 53.978 | yes |
| k2 | kick Ab1 (drive 0.35) | 53.677 | no |
| v8 | kick Ab1 + drive 0.1 (our kit read E21: the driven A1 kick's 3rd harmonic; the record's drums read Ab24 A20) | 54.838 | yes |
| bal2 | like-for-like stem balance: bass -5, drums -3, guitars +2 (separated synthetic stems mislead) | 51.790 | no |
| vb / gp | (v7 base) bark on aligned vocals 53.854; guitar presence +3 dB @4k 54.092 (+0.11) | | no / marginal |
| v8n | v8 on f0b5f99 (m8 grain 0.5 default) | 54.801 | baseline |
| gp8 | presence on v8n | 54.840 | marginal |
| v9 | dtwgrid refinement: drum stem vs drums solo, 2-bar blocks, conf >= 0.3 else keep (bars 94-109 were 10-20 ms early) | 55.083 | yes |
| vox6 / dh8 / bs2 | (v8) vocals +6 dB 54.335; drums highshelf -3 dB @5k 54.181; bass-pick-di 52.787 | | no |
| dt1 / dt1b | drumtrans.py transcription of the whole drum stem replacing the tab drums (tab drums already align 0.4-0.58) | 46.831 / 45.971 | no |
| r1 / r2 / r3 / bs1 / bal1 | (v9) m8-chug 54.247; m8-emg-l + m8-bkp-r 53.563; m8-obzen 53.650; bass-di 53.804; bass -5 drums -3 53.040 | | no |
| se05 | (v9) per-section master EQ (sectioneq.py) at 0.5x on top of the global EQ: 45 Hz -3..-4 dB in most sections | 56.832 | (combine) |
| ph0 | (v9) pinch harmonics as plain notes (m8 ^ph rings the 3rd-6th: F2's C was an extra pitch class; the record's ring reads F) | 55.310 | (combine) |
| note | shared kidman.yaml adopted the voice `coda` field (921e976): songs on kidman stopped planning on the pinned groove; groove restarted on 2e0ac67 | | |
| v9n | v9 re-baselined on 2e0ac67 (kidman with onset/coda) | 55.066 | baseline |
| c3 | se05 + ph0 | 56.967 | (superseded) |
| v10 | per-section master EQ at 1.0x (sectioneq.py on the v9 render) | 57.737 | yes |
| tu7 / tu9 / ld1 / va9 | (v9n) a4 447 54.927; a4 450 54.327; lead on m8-rhythm-r 54.604; aligned vocals on new kidman 55.107 (+0.04) | | no / no / no / (combine) |
| c4 | v10 + no pinch harmonics | 57.896 | |
| v11 | per-section EQ at 1.3x + no pinch harmonics (map "strip": ["ph"]) | 57.949 | yes |
| c5 | per-section EQ 1.0x + no pinch + vocals re-aligned to the v4+ grid (they were ~230 ms early) | 57.918 | (base) |
| ks | c5 + snare +4 + kick +3 | 57.564 | no |
| v12 | c5 + snare +4 dB (mixfeel: the record's 250 Hz-2.5 kHz crest 9-10 dB vs ours 4-6, hit-to-hit vary 3.6-4.2 vs 1.4-2.0) | 58.525 | yes |
| v13 | snare +6 dB (kit.s.gain=7dB) | 58.774 | yes |
| h0 | v13 on a41c070 (humanize feel off) | 58.774 | bit-identical |
| h1 | guitars humanize drift 5ms + gate 0.15 | 58.763 | neutral (choruses/outro +0.6..0.9, intro/verse/breakdown -0.4..0.9) |
| v14 | snare +8 dB | 58.963 | yes |
| h2 / h3 / h4 | guitar+bass accent 0.5 58.801 (+0.03); drums accent 0.4 + drift 4ms 57.840 (-0.93); all 57.844 | | no |
| v15 | snare +10 dB | 59.090 | yes |
| h3a / h3d / h12 | drums accent only 58.900 (-0.06); drums drift only 58.078 (-0.89: drift is the culprit); guitar drift+gate+accent + bass accent 58.979 (+0.02) | | no |
| bk1 / bk2 | breakdown drums from drumtrans (tab elsewhere), without/with toms | 57.900 / 58.155 | no (breakdown 46.6/48.5 vs 54.5) |
| bt1 / bt2 | breakdown per-bar tempos from transcribed-kick offsets | 58.406 / 58.434 | no: the kick offsets pointed the wrong way |
| v16 | snare +12 dB (+4/+6/+8/+10/+12: +0.61/+0.25/+0.19/+0.13/+0.10 — stopping here) | 59.195 | yes |
| v17 | dtwgrid --feature metric --around-zero, 2-bar blocks, conf >= 0.3 keep-below: the breakdown was 30-75 ms early, bridge/lead riff -60..+95 ms, intro -120 | 60.816 | yes (breakdown 54.8 -> 60.2) |
| mg2b | same without the intro blocks | 60.609 | |
| v17v | v17 + vocals re-transcribed on its grid | 60.989 | |
| mg3 | second metric-grid pass | 61.674 | |
| v18 | second pass + vocals re-transcribed on it | 61.735 | yes |
| sy1 / sy0 / irk | (v17) m8-rhythm sympathetic stage (F-standard 8-string resonances) retuned to drop D 61.467; off 61.795; cab kitten-slayer only 61.069 | | (combine) |
| c7 | v18 + sympathetic off | 62.709 | |
| v19 | v18 + sympathetic off + kitten-slayer cab on both rigs | 63.098 | yes |
| g5v / se2 / w1 / r6 / bsub / ssin / sa | third grid pass 63.117 (converged); per-section EQ refit 62.499; master sub mono 62.700; drums room -6 dB 61.883; bass sine sub -20 dB 62.517; snare body sine 62.776; snare A3 62.032 | | no |
| ka / ksplit | kick A1 everywhere 63.115 (sections split: +1.2..1.6 in 1/4/5/9, -2..-3 in 7/8); A1 except bars 78-105 + outro 63.659 | | (combine) |
| lr4 | levelride 4 s windows | 63.086 | no |
| v20 | levelride.py fader ride at 1 s windows / 0.5 s steps, max 4 dB (the record's verse phrases its dynamics; verse 60.4 -> 67.9) | 64.641 | yes |
| v21 | v20 + kick A1 except bars 78-105 and the outro (Ab1 there): the kick's best pitch follows the section's harmony | 65.041 | yes |
| ldb / ldbd / ldbu / ldbl | (v20n) built-in guitar m8-lead (7ff2824) inlined as ltr-lead; dry; -1 dB; -7 dB | 64.313 / 64.188 / 64.260 / 64.300 | no (synth lead 64.641) |
| inl | v21 with the config m8-lead/m8-rhythm-l/r inlined as ltr-lead/ltr-rhythm-l/r (no dependence on shadowing shared copies) | 65.041 | bit-identical |
| v22 | inlined patches + second 1 s fader-ride pass (--accumulate on the v21 render) | 65.123 | yes |
| sbody | snare body level.value -6 dB (less Eb/C imprint) | 64.352 | no: the pitched body is worth more |
| wout / c10 | master width lane: x1.8 from the outro (the record's outro is wide in every band, ours half) | 65.244 (v21) / 65.328 (v22) | |
| v23 | outro width x2.4 | 65.361 | yes |
| vdbl / gn | (v22) vocals double-tracked (detune 10, pan 0.3) 64.921; (v23) guitars narrower +-0.8/0.65 64.566 | | no |
| v24 | drums width 1.6 above 300 Hz (the record's top bands are wide; ours were narrow where the centred snare and cymbals dominate) | 66.401 | yes (every section up) |
| dw13 | drums width 1.3 | 65.978 | |
| v25 | drums width 2.0 above 300 Hz | 66.812 | yes |
| dw25 / dw30 | width 2.5 / 3.0: bit-identical to 2.0 (WidthFx clamps at 2.0) | 66.812 | |
| g0 / gup | (v25) guitars grain 0 66.821 (neutral); guitars +2 dB 66.484 | | no |
| v26 | drums: two stacked width stages (2.0 then 1.5, above 300 Hz) | 66.874 | yes (+0.06) |
| vdn / lup / ldn / bup / bdn | (v26) vocals -3 66.826; lead +3 66.779; lead -3 66.851; bass +2 66.525; bass -2 66.704 | | no: levels at their optimum |
| vr1 | vocals as stemvox energy runs (358 syllables) | 66.898 | neutral |
| in1 | intro bars 2-5 per-bar metric grid (bar 2 was 150 ms early; offset 1.82 -> 1.97) | 66.948 | (combine) |
| v27 | bridge bars 72-86 per-bar metric grid (75-76 30 ms early, 78-81 25-80 ms late around the 15/8 bar) + vocals re-transcribed | 67.016 | yes |
| c11 / c12 | intro bars 2-5 per-bar grid (+1.0 intro, nets 0) | 67.024 | no |
| gr0 / k2db / swire | rigs without click/scrape/thump/squeak 67.016 (inaudible); kick +2 dB 66.591; snare wires -6 dB 66.559 | | no |
| amm | both rigs amp model mark | 66.838 | no |
| v28 | both rhythm rigs on the Rectifier-like `modern` amp (was 5150 left / gojira right): every section up | 67.880 | yes |
| amrl / amrr / mmid / mgain / ird / irc / bam / bag | (v28) modern amp left only 67.499, right only 67.730; amp mid 0.75 67.622; amp gain 0.65 67.879; darth-genocider cab 67.182; cookie-monster 66.962; bass amp modern 67.642; bass amp gain 0.85 67.862 | | no |
| pb1 | per-bar metric grid, bars 105-135 (+-80 ms window) | 67.979 | (combine) |
| v29 | per-bar metric grid, bars 72-90 + vocals re-transcribed | 68.008 | yes |
| v30 | v29 + per-bar metric grid over bars 105-135 (breakdown/outro residual -40..+45 ms) | 68.109 | yes |
| ld4 / ld7 / ldg | (v29) master +4 dB into the ceiling 67.782; +7 dB 65.765; glue + 4 dB 64.667 (the record is ~7 dB louder, crest 9.5 vs 16 dB; limiting flattens the chorus lift) | | asked Harry |
| v30b | v30 on e27a12a (bends now reach voices: 4049ee3) | 68.021 | baseline |
| v31 | strip bend= tokens (tab slides/bends: 2-semitone slide bends, 4.5-semitone bends on the stripped pinch harmonics, 6-semitone bass bends) | 68.109 | yes |
| phb / nbass | pinch harmonics with their 4.5-semitone squeal bends 68.000; bends stripped from the bass only 68.106 | | no |
| sef1 / sef13 | per-section EQ refitted from scratch on a render without it (1.0x / 1.3x) | 67.121 / 66.788 | no (everything since v10 was tuned on the old fit) |
| v32 | the fresh fit spliced into the three sections where it won (intro, lead riff, outro) | 68.188 | yes |
| v33 | kit `tune` (d6bf166, bd-416d85) instead of kit.k.pitch: the toms follow the A1/Ab1 kick (outro 67.3 -> 69.3) | 68.359 | yes; groove restarted on d6bf166 |
| tbg / tbbb / tabb | second kit tune G1 (bridge +1.7, verse3 -1.9) 68.170; Bb1 67.894; main kit Bb1 (lead riff +0.8) 68.290 | | no: stopping at a two-kit split (a drummer doesn't retune per section) |
| heg / hed | humanize.env 0.2 on guitars 68.366 (sections +-1.6: seed noise); on the kit 68.359 (no effect: env doesn't reach kit pieces) | | no |
| sbb / sg | snare Bb3 65.787; G3 68.309 | | no: Ab3 stays |
| note | stemnotes.py --map (12/8 bars): the chorus guitar stem reads D/Eb/F + F#2-F2 at bar 49 ends; the tab's riff notes are right, chorus chroma is a harmonic-weighting gap | | |
| stemscore v33 | drums 57.7, guitar 44.3 (choruses 29/32), bass 30.2 (ltas 13.4), vocals 29.0 | | |
| note | like-for-like bass (ref bass stem vs our separated bass, same htdemucs_6s): ours +13..+19 dB below 80 Hz (sine sub; the record's bass has little under 80 Hz) and +10..+35 dB above 315 Hz (brighter grind); the per-section EQ's -6..-8 dB at 45 Hz has been compensating at the master | | |
| bhp / blp / bamix | (v33) bass hp 70 Hz 68.095; lp 1.5 kHz 67.857; amp blend 0.4 67.513 | | no: the master (EQ, rides) is fitted around the old bass; trying a re-master pipeline (rm1: hp bass, no per-section EQ/ride -> refit EQ -> re-ride) |
| rm1 / rm2 / rm3 | re-master around a hp-70 bass: no per-section EQ/ride 64.866 -> fresh per-section EQ 65.762 -> fresh 1 s ride 67.419 | | no (v33 68.359: its master was refined over many passes) |
| metric | likeness gains a mastering term (level + crest, 1ffa987): v33 68.359 -> 66.001 on the new metric | | |
| lda4 / lda6 | v33 + 4 dB / + 6 dB into the ceiling limiter | 67.030 / 66.948 | |
| v34 | v33 + 5 dB into the ceiling limiter (the record is a crushed 2004 master: -9.5 dBFS RMS, crest 9.5 dB) | 67.050 | yes |
| rr5 | v34 + 1 s fader re-ride on the limited render (--accumulate) | 67.357 | (combine) |
| v35 | v34 with the chorus lift lane doubled to +-2 dB (the ceiling limiter squashes a +-1 dB lift) | 67.477 | yes |
| pk7 / pk6 | (v34) guitars pick at 1/7 (0.143; chirper-two's Bleed finding: a pluck at 1/n cancels harmonics n, 2n...; ours were 0.12/0.095 like Bleed's) 67.731; (c13) at 1/6 67.766 | | |
| c13 | v35 + the re-ride | 67.532 | |
| v36 | v35 + re-ride + guitars picked at 1/7 | 68.240 | yes |
| pu13 | guitar pickups at 1/13 | 68.224 | no |
| v37 | bass picked at 1/7 too (was 0.2 = 1/5, cancelling its 5th harmonic) | 68.312 | yes |
| inb | bars 3-5 per-bar grid only (offset/bar 2 kept) | 68.226 | no (intro +0.5; other sections moved +-1.6 = noise) |
| noise floor | v37 at seeds default / 3 / 5: 68.312 / 67.612 / 67.569 (sections +-1..1.5). The default seed is a ~0.7 lucky draw; single-seed changes under ~0.5 are noise. From here: seed-average (seedscore.py) anything small. Kept small steps (dwx +0.06, c13 +0.06, spl +0.08, bpk7 +0.07, tune +0.17) were never seed-checked | | |
| seedscore v37 | seeds 3/5/11: 67.6 / 67.6 / 67.5 (mean 67.57, std 0.05) vs the default seed 68.31: the climb fitted seed 0 (voice seeds hash the start sample; the 0.5 s fader rides and per-bar grid follow seed 0's draws). Decisions from here on seed-averaged; the playlist plays seed 0 | | |
| gld / bhp37 (seed-avg) | guitar lead 67.17; bass hp 70 Hz 67.17 (vs v37 67.57 ± 0.05) | | no: real losses |
| mst (seeds 3/5/11) | render-time mastering --loudness -9.5 --limit (c552556): 67.49 / 67.76 / 67.37 = 67.54 | | no gain over +5 dB into the ceiling |
| v38 | pinch harmonics restored with their tab bends (Lamb of God's bent squeals): seed-avg 67.50 ± 0.08 vs v37 67.57 ± 0.05 — a tie, so the realistic choice | 67.50 (mean) | yes |
| cl5 / cl7 (seed-avg, 33fca2a) | master soft clipper (clip, 33fca2a) ahead of the ceiling limiter instead of +5 dB gain: drive 5 dB 68.23 ± 0.05; 7 dB 68.20 ± 0.08 (v38 67.50 on the same engine) | | |
| v39 | clip drive=7dB ceiling=-0.5dB (ties drive 5; 2 dB louder, nearer the record's crushed master); groove restarted on 33fca2a | 68.20 (mean) | yes |
| v40 | seed-robust fader ride: levelride --accumulate on the averaged loudness of v39 rendered at seeds 3/5/11 (levelride.py now takes several renders). In-sample seeds 3/5/11: 68.50 vs 68.22; held-out 7/13/17: 68.67 vs v39 68.47, +0.2 on every seed | 68.6 (6-seed mean) | yes |
| vocal check | kidman solo render separated by htdemucs_6s: vocals 75%, drums 15%, other 11%; the record's scream stem re-separated: vocals 100%. Engine bead bd-f227d8 (harsh vocals read as voice), with the engine agent | | engine |
| vbk / vkb (seed-avg) | vocals on bark 68.47 ± 0.09; kidman + bark rasp -8 dB 68.50 (v40 68.50 on the same seeds): metric ties | | |
| v41 | vocals on bark: a metric tie, but the separator reads a solo bark render as 98% vocals (kidman 75%, the record's scream 100%) | 68.5 (mean) | yes (realism) |
| vb3 / vb6 (seed-avg) | bark vocals +3 dB 68.20 (vs 68.47); +6 dB aborted | | no |
| smem (seed-avg) | snare body as an additive ideal-membrane mode set (1, 1.59, 2.14, 2.30, 2.65, 2.92, 3.16; damp 4) via an inline ltr-kit | 68.23 ± 0.19 (paired -0.1/-0.3/-0.3) | no: the triangle body's harmonics help here |
| sr05 (held-out seeds 7/13/17) | residual per-section EQ fitted on the averaged spectra of v41 at seeds 3/5/11 (0.5x, added to the lanes) | 68.53 vs v41 68.67 (paired -0.1 each) | no: the EQ is at its optimum |
| v41 held-out | seeds 7/13/17 | 68.67 (same as v40: the bark switch is score-neutral) | |
| v42 | per-band master width (fa719f6): side scaled per likeness band by the record's side/mid over ours (measured on v41 at seeds 3/5/11; mids 400-1200 Hz x0.82 and air 8-16 kHz x0.71 narrower, sub x0.77, low-mids x1.12) | 69.20 held-out (v41 68.67; +0.5 every seed); half strength 69.10 | yes |
| v43 | second per-band width pass (residual ratios from v42 at seeds 3/5/11: the clip/limiter and 12 dB/oct crossovers mean one pass under-corrects; low 60-150 and himid 1.2-3.5k needed ~0.75-0.83 more) | 69.50 held-out (v42 69.20; +0.3 every seed) | yes |
| v44 | third per-band width pass: the 60-150 Hz band kept reading wide (side created after the width stage by the per-channel clip/limiter); bands now sub 0.71, low 0.50, lowmid 1.07, mid 0.92, himid 0.71, pres 1.04, air 0.72 | 70.20 held-out (v43 69.50; +0.7 every seed) | yes |
| v45 | fourth per-band width pass (sub had overshot to 0.06 vs 0.09 -> x1.02; low still 0.40 vs 0.33 -> x0.42) | 70.63 held-out (v44 70.20; +0.4..0.5 every seed) | yes |
| bw5 | fifth per-band width pass (body bands now within ~0.02 of the record) | 70.63 = v45 | converged |
| cd9 | clip drive 9 dB (held-out) | 69.90 vs v45 70.63 | no: the drive is now coupled to the per-band width fit (the per-channel clip makes side content) |
| v46 | vocals back on kidman after chirper-two's bd-f227d8 fix (e47aad9: unmarked notes sang a closed 'u' that read as drums; now an open vowel, 94.8% vocals) | 70.87 held-out (v45 bark 70.63; +0.2..0.3 every seed) | yes |
| vk3 / vkm3 | kidman +3 dB 70.80; -3 dB 70.77 (v46 70.87) | | no: level at its optimum |
| v47 | kidman drive 0.5 -> 0.25 (track override; chirper-two: 98.2% vocals vs 94.8% on this track) | 70.87 (tie, plan differs) | yes (realism) |
