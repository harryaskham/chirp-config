# Archangel (Burial) — build log

Reference: Hyperdub's official upload (YouTube 8k_f2QK77ew, 238.2 s, full band to ~17 kHz, RMS -12.3 dB, 932 clipped
samples: the record as released). Stems: htdemucs_6s — drums -4.6 dB rel. the mix (throughout), bass -4.0 (from
~30 s), vocals -11.6 (throughout), other -14.7 (from ~30 s), guitar -22.6, piano silent.

Timing: 135.18 bpm, click-steady (pulse-train fit; 20 s windows within ±15 ms), first beat 0.005 s, 4/4.
Sections (4-bar blocks of 7.1 s, joins where the stems' arrangement changes): drums alone 0-7.1, vocals enter
7.1-28.4, pad/bass build 28.4-49.7, full 49.7-78.1, the second vocal phrase 78.1-99.4, the breakdown (drums -15 dB,
no bass) 99.4-113.6, full 113.6-163.3, a thinner variation 163.3-191.7, full 191.7-234.4, tail.

Build (no map; regenerate with):
  stemsong.py OUT.yaml --stems ref/stems/htdemucs_6s/archangel --bpm 135.18 --offset 0.005 --bpb 4 --grid 4 \
      --parts vocals:dream-vox:voice:-4 other:juno-pad:pad:-6 bass:sub:line:-2 guitar:pad-glass:chords:-12
  drumtrans.py --template-song tight-kit PIECES tpl.yaml (k s rs ss h hs oh shk c t1 ft), render → tpl.wav
  drumtrans.py drums.wav SONG tpl.wav PIECES drums.json --vel-gamma 1.5 → drums-{kick,snare,hats,toms,cymbals}
      (1599 onsets: kick 309, snare 744, hats 2, toms 17, cymbals 38 — hats mislabelled as in Saturnine)
  + vinyl (patch vinyl, one held note, -18 dB); master glue, gain +8 dB, clip drive 4 dB; ceiling -0.3 dB.
  stemhats.py --patch tight-kit --gain 0dB --to 234.4 --name drums-shuffle (620 uncovered 6-12 kHz hits)
  stemretime.py drums-{kick,snare,toms,cymbals} vs the drum stem --window 0.045 --grid 48

| version | change | score |
|---|---|---|
| a1 | stemsong + drumtrans + vinyl, gentle master (RMS -18.3) | 40.55 |
| a2 | master +8 dB / clip 4 dB, ceiling -0.3 dB (RMS -12.1) | 43.98 |
| a3 | + drums-shuffle (stemhats, 620 hats) | 47.40 |
| v1 | + drum hits retimed to the stem (±45 ms) | 49.01 |

Engine: the vocal chops (Burial's pitched, chopped R&B fragments) can be built from existing fx (Pitch, Formant,
Stutter, Tape, Crush) and resampling (chop-lofihop's method) — no engine gap filed yet.
| v2 | widthfit.py 2 passes (per-section master band lanes wb0-wb6; the record far narrower below 400 Hz: ratios 0.2-0.5, wider above 3.5 kHz: 1.2-1.5) | 52.62 (held-out 52.66/52.60 vs 49.02/49.03) |
| v4 | the vocal: stemvel on vocals-voice vs the vocal stem (658 notes); patch tests lost: maynard tract 0.8 -3.1, voice -11.5, +6 dB -6.9 (held-out, on v2) | 54.095 (held-out 54.10/54.03 vs v3 53.86/53.83) |
