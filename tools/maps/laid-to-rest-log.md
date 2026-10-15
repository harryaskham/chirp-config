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
