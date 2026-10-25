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
