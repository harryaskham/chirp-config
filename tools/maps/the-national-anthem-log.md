# The National Anthem (Radiohead) — climb log

Reference: official upload https://www.youtube.com/watch?v=NfQD1QiQ9o4 (351.7 s, full band, RMS -11.5 dBFS, crest 11.5 dB).
Stems: ref/stems/htdemucs_6s/the-national-anthem/. Tab: Songsterr 51268 (studio transcription, 9 tracks:
vocals, bass, brass section, keyboard, 3 ondes Martenot, baritone sax, drums), cached in ref/songsterr-51268.
Map: tools/maps/the-national-anthem.json. Sections: tools/the-national-anthem-sections.txt (bars 1,5,17,29,37,49,61,76,92,105,119 + end).

Timing: the record is click-tracked at 91.48 bpm (pulse-train fit over 13-315 s, every 25 s window within
±10 ms of one grid), not the tab's 90; bar 1 (the bass entry) at 2.105 s. The tab is 131 bars of 4/4 but every
track is silent after bar 122 — the record's last ~30 s (the brass/noise tail to 351 s) is not transcribed.

| version | change | score | kept |
|---|---|---|---|
| v1a | tab at 90 bpm, offset 2.12 s: bass-fuzz, rock-kit (h1->h, drop m92), maynard vox, horn-section brass, tenor-sax bari, juno-pad keys, 3x theremin ondes | 34.9 (rhythm ~0) | |
| v1b | all bars at the measured 91.48 bpm, offset 2.105 s | 45.9 (rhythm 30-57) | |
| v1 | + master +2.6 dB before the clip (body RMS was 2.6 dB low) | 47.1 | yes |
| wb1 | per-section master band-width lanes (wb0-wb6, record/ours side-mid per likeness band, clip 0.2-2.5): the record is mono-ish below 150 Hz, very wide at 400-1.2k (~1.0: ondes/brass) and 0.6 in the air; ours the reverse | 48.4 | |
| wb2 | second band pass | 48.7 | |
| bw3 / bw15 | bass_width 0.3 / 0.15 (below the stage's 120 Hz corner bands do not apply; mono_below 0 needs a newer groove than f4b9563) | 49.2 / 48.9 | |
| v2 | third band pass on bw3 | 49.7 | yes |
| t0 / t6 | ending tail: stempad of the guitar stem (the record's ending lives there: drums/bass gone from 316 s, 'guitar' -17..-22 dB = the brass/sax squall) over bars 119-131 on brass, 0 / -6 dB | 49.9 / 49.7 (v3 50.3; ending 32.2 -> 29.3 / 26.9: ltas +9 but chroma -14) | no |
| t7 | the tail only from bar 126 (where v3 is already silent) | 48.9 (ending 20.3, loudness term 0.1) | no |
