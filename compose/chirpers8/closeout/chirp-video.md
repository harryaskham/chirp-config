# chirp-video: close-out (A Light Left On, the video)

**Engine (chirp vis, branch `chirp-video`, not merged).**
- Missing: the synth's observables (kuramoto `sync`, the chaos systems' state) don't reach the pictures. t5's swarm runs its own Kuramoto model on the song's `agree` instead.
- Missing: the web pane only knows built-in looks, not album programmes. Lift-driven scene changes weren't built; scenes are timed.
- Known limits: sync is weak by design on the calm tracks (t6 0.41, t7 0.42, t10 0.49). Caption typing follows each phrase's length, not each word.

**Patches/library.** n/a (visual looks only). Twelve programmes live in `vis/chirpers8-tN.yaml`, and `compose/chirpers8/video.yaml` holds the album master: the amber light, title cards and fades.

**Sections.** Per-scene scoring (`--score 0`) swept t1-t4 and t9. It found two near-black stretches, both fixed: t9's storm (luma 0.002) and t1's score scenes (0.02). t5-t8 and t10-t12 aren't swept yet.

**Songs.**
- Lyric captions exist where phrase files exist: t1, t2, t3, t5, t6, t7, t8, t9, t10. t11 and t12 have none.
- t8 is meant to be colourless; its silver costs it on the score.
- t10's printed final is a light section in a dark album, kept on purpose.

**Structure/album.**
- Each track fades in from black and out to it, while the amber light stays on.
- Titles type in at the start of each track, and t12 ends on the album's name. Chapters and a description are written beside the video.
- The music bleeds between tracks but the picture dips to black. That reads as a chapter break, but the music doesn't pause; a crossfade between programmes would match the bleed better (not built).
- Most-alike pair: t8 and t12 (0.064).

**Final pass (existing plans only).**
1. Finish the per-scene sweep (t5-t8, t10-t12) and fix any dark or still scene.
2. Render the final video from the release files: each track's `audio:` set to release.json's files, back to back with no gaps. Check its length against the release program (±2 s, ytpub's limit), and check the chapters.
3. Render the parts in parallel so 1080p fits the release window, then score and look at the whole album once more.

**Final pass, done (14:10).**
- Scene sweep: all 12 swept. Lifted the dark scenes: t9's storm, t1's score, t10's deep stack, t12's opening and t6's intro and verses.
- Seams: the dip at each cut is now under a second (0.7 s down, 0.5 s up), with the amber light holding through it.
- Final render dry-run on stand-in MP3s passed: length equal to the release program (0.00 s difference) and 12 chapters. Ready for release.json.

**Release (4 Nov, evening).**
- Standby Amber, rendered at 4K: 3840x2160, HEVC on the GPU, drawn in 6 parallel parts under release.json's files.
- 13 unique transitions, approved by Harry: a boot into t1, then one per join, then a power-down to the amber standby light. Each ends on the next song's first frame.
- Sync: every frame sits on the album's own timeline, measured with tools/vissync.py (0 ±1 frame wherever the picture clearly follows the sound).
- Fixed on the way: captions cut short at the placeholder's length; lower case for the band ("chirpers").
- Still missing (for next time): a true picture crossfade across songs, synth observables (`sync` and the systems' state) as vis sources, and album programmes in the web pane.
