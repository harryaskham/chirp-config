# Saturnine (GoGo Penguin) — climb log

Reference: official upload https://www.youtube.com/watch?v=WW6JY2WcEUI (293.3 s, full band, RMS -12.5 dBFS,
crest 12.5 dB). Stems: ref/stems/htdemucs_6s/saturnine/ (piano, bass, drums carry the body; "other" carries a
tonal low-mid ostinato from 0 s — most likely the hand-muted piano, C4/Bb3/Ab3/C5, ~3.5 onsets/s; the piano
stem is silent for the first 20 s). No Songsterr tab exists.

Timing: click-steady 112.01 bpm (pulse-train fit over 10-280 s; windows within ±30 ms, the ±0.25 s ones are
half-beat syncopation), first beat 0.302 s, 4/4 assumed. Sections: tools/saturnine-sections.txt (intro to 22 s,
then ~30 s blocks).

Build (no tab, so no map; regenerate with):
  stemsong.py OUT.yaml --stems ref/stems/htdemucs_6s/saturnine --bpm 112.01 --offset 0.302 --bpb 4 --grid 4 \
      --parts piano:piano:chords:-2 other:piano:chords:-4 bass:upright-bass:line:-4
  drumtrans.py --template-song tight-kit PIECES OUT (pieces k s g rs ss h hs oh hp t1 t2 ft rd rde c sp), render
  drumtrans.py drums.wav SONG TPL.wav PIECES drums.json --vel-gamma 1.5  (tight-kit's bus compressor floors the
      fitted velocity exponent at 0.3 and every hit came out @1 without it) → tracks drums-{kick,snare,toms,cymbals}
  master: glue, +3 dB, clip drive 2 dB.
drumtrans labels are rough: snare family mostly sidestick (ss 193, g 58), toms mostly floor tom (435), ride edge
220, hats 2 — likely hats read as ride and snare body as floor tom.

| version | change | score | kept |
|---|---|---|---|
| v1a | stemsong (piano/other chords on piano, bass line on upright-bass) + drumtrans drums on tight-kit | 50.5 | |
| v1b | master +5 dB, clip 4 dB (RMS -10.3, crest 6.8: over-squashed) | 51.2 | |
| v1 | master +3 dB, clip 2 dB (RMS -13.8, crest 10.3) | 52.1 | yes |
