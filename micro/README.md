# Micro benchmark

Harry, 25 Oct 2026: reproduce short clips (1-10 s) of exposed instruments **from scratch**, to measure sonic accuracy
without the song-shape terms that let whole-song climbs hide bad local sound, and to grow the patch library and the
engine until chirp can synthesise them closely.

- Clips: `micro/clips.json` (`tools/microclips.py propose|add|list`). Each is a window of a record we have stems for,
  where one stem (or the crowd) is exposed. About a third of each family is **holdout**.
- Score: `tools/microscore.py --clip ID --song micro/songs/ID.yaml` (signal measures only: spectral, timbre, tone,
  transients, pitch, modulation, stereo; level-matched and aligned, so loudness and placement do not count).
- Masking report: `tools/microscore.py --mask` scores each clip's song's current best render over the same window.

## Rules

1. **Climb the library, not the clip.** A micro song (`micro/songs/<clip-id>.yaml`, the clip's notes from 0 s) is a
   test harness. A gain counts when its sound lives in `patches/` (a library patch), an engine feature (a bead for
   wM) or a shared tool, not in song-local tweaks.
2. **Holdouts.** Never tune on a holdout clip. A library change must also improve (or hold) its family's holdout
   clips, each built once from the library with its own notes.
3. **No global regressions.** A library patch change is crossclimbed across every album song that uses it
   (`tools/crossclimb.py --a-cfg OLD --b-cfg NEW`, chirp-eco runs it) and adopted only if no song loses beyond noise.
4. **Record every attempt:** `microscore.py --clip ID --song … --record "what changed"` appends to
   `micro/ledger.jsonl`; `--board` shows the best per clip.
5. **Ears decide.** Ask Harry to listen to a reference/ours pair (`chirp live queue FILE --id groove --label NAME`,
   never over the groove) before a family is called solved.
6. **Engine gaps.** When a family cannot get close (the profile shows which dimension), file a bead (project `tools`,
   labels `chirp,dsp`) with the clip ids and the profile as evidence.

Canary: chirper-three (from 25 Oct).

## In-context scoring (25 Oct)

Clips whose song exists are scored IN CONTEXT: `microscore.py --clip ID --context TRACKS [--set tracks.N.patch=P]`
renders the album song with the clip's instrument tracks soloed (its master, buses and lanes kept) over the clip window.
A library patch is then judged as it sounds on that record. masteraudit across 111 songs found no common master tilt
(median correction within +-2 dB, quartiles +-2-3 dB both ways): each master corrects toward its own record's colour,
so a standard harness master would not help, and bare harnesses over-reward dark colour patches (chirper-three).
Mind's Mirrors' guitars: bare harness 31.0, in context 49.2 on their album patches, 39.1 with clean-dry swapped in.
Standalone harnesses (`micro/songs/`) remain for clips without a song file, and for building parts from scratch.

## Findings

- **25 Oct, piano-recorded as the `piano` default: rejected.** chirper-three's piano-recorded (the built-in piano,
  -12 dB above 2.5 kHz, plate, width 2) beat the built-in on all four piano clips, holdouts included
  (clair-de-lune-piano-164 36.9 -> 46.2 on every seed). Crossclimbed as the default across the 25 album songs that
  use pianos: mean -0.96, 13 worse (saturnine -5.5, daydreaming -4.1, wuthering-heights -4.0, pyramid-song -3.7),
  1 better (clair-de-lune +3.4). With --refit (each side's master refitted first): mean -0.84, the same 13 worse, so
  stale masters were not the cause. The global metric prefers the brighter, narrower piano inside mixes that are
  closer to the records locally. That is the masking this benchmark is for: either the global terms reward brightness
  as fill (as with the S&M crowd bed) or a clip misses how the part sits in its mix. piano-recorded stays a named
  patch that songs opt into (Clair de Lune +3.4 / +4.65 refit).
- **25 Oct, les-paul low-mid body (+2.5 / +5 dB peak at 250 Hz) as the default: rejected.** masterbypatch found
  the 8 les-paul songs' masters boosting 141-356 Hz by ~+5 dB, across 4 albums (not an album confound). Refit
  crossclimb: half mean -0.02 (thin-thing -0.39), full mean -0.16 (thin-thing -0.58, electioneering -0.46). A
  patch-level TILT cannot beat refitted masters, since a master refit is itself a tilt. Library defaults can win
  only on what a master cannot fix: timbre, transients, modulation, stereo. Point library work there.
- **26 Oct, Immutable's 8-string with less pre-gain (m8-emg-l/r amp gain .8 -> .45/.40, ts .65-.7 -> .35/.30): micro yes, songs no.**
  On the riff clips the lower gain won monotonically (the-faultless-riff-206 +1.3, riff-276 +5.3; holdout
  ligature-marks-riff-122 +2.0, abysmal-eye-riff-213 flat), almost all of it transients (attack/envelope shape). The
  refit crossclimb over the 7 songs using m8-emg rejected both settings: .45/.35 mean -0.21, .40/.30 mean -0.26, 6 of 7
  worse, and the holdout SONGS the worst (-0.47, -0.52). By section the loss is broad, riff-heavy sections included
  (ligature-marks 102-117 s at .68 guitar+bass share: -1.47), and moves song-level terms (loudness contour, master,
  stereo), not timbre. The guitars' level is unchanged (-0.1 dB: the amp compensates). So micro (level-matched, local
  envelope) and the song metric disagree on how much distortion the record has. Harry's ear is the tiebreak; a
  section-local lane would only be worth it if the song metric agreed somewhere, and it didn't in any section.
- **26 Oct, tighter 8-string chugs (play.gate .88 -> .65, palm-mute decay ~0.35 -> ~0.1 s): micro yes, songs no, and why.**
  All four riff clips gained (training +1.4/+4.4, holdouts +0.4/+1.0), and the refit crossclimb rejected it like the
  gain change: mean -0.25, 5 of 7 songs worse. Scoring the same windows against the record's FULL MIX with the whole band
  playing shrinks the gain: the-faultless 206.5 +1.24 vs the stem -> +0.46 vs the mix; 276.5 +3.89 (transients 40 -> 67)
  -> -0.55 (transients 30 -> 29). A separator gates a dense mix's stem between chugs (the kick, bass and room that fill
  them are taken out), so stem-referenced ENVELOPE scores reward staccato that isn't in the record. Rule: stems are fine
  for spectral/timbre/tone, but an envelope or articulation candidate must also gain on the full-mix, full-band section
  score (`microscore --section SONG:A-B` without --stem or --context) before it goes to a crossclimb.
