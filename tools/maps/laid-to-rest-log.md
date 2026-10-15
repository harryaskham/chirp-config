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
