# chirp-eco: close-out (Accretion: the ecosystem, the cut, the release)

**Engine and landing.**
- 56 gated batches landed; the cut and the film ran on one pin (97a13ae6). No landing changed a released album's sound.
- Landed too late to be used well: `diction` reached its second level on the day of the cut, and the 60 fps picture fixes (batches 55 and 56) the same day. Standby Amber had an engine freeze a day before its cut; this album did not, and should have.
- Each gate takes 30 to 60 minutes whatever the change. It never blocked a song, but it set the pace of the last day.

**Groove and host.**
- Three dropouts and near-misses on 10 and 11 Nov (391 and 55 underruns) came from another project's Nix build landing on the groove's four CPUs. What I tried and withdrew: raising the groove's thread priority (it ranks threads only inside our own group), freezing the film (did not slow the drain), letting the film share those CPUs (worse).
- What held: a 90 s render-ahead instead of 30. Its one test since (15:13 on 11 Nov) dipped to 75.5 s with no underrun, but without the film beside it. The cost is that a live edit is heard up to 90 s later. The real fix is a CPU weight between the system's and the user's groups, which is root's.
- Found on the last day: the system deletes what nobody used in `/tmp` for ten days, and the release pin lived only there. Pins and working scripts now have checked copies outside it (`tools/pinstore.py`).

**The cut and the release.**
- The cut took 15 minutes and verified bit for bit (8 of 8 masters). Name and cover went in afterwards without a re-cut: tags by stream copy, masters untouched.
- Never checked by ear by anyone before release: the diction round (measured only: word error rate 0.65 to 0.42), t4's climax, t3's lift-off, t7's forward voices.
- Measured and not acted on: t1's top end sits 4.9 dB right at 1:12-2:16; t3's sits 3.9 dB left at 0:40-1:28.
- My mistake: the upload was triggered by a check of numbers alone, and I had moved that trigger ahead of chirp-video's contact sheets. A garbled film was 6 GB into an unlisted upload before his sheet stopped it. Nothing was public. The check now decodes the file and compares pixels with the drawn parts.
- Not done: Spotify through DistroKid (the kit is ready in `master/`).

**Agents.**
- The composers have no loops, and a message cannot start their turns. Every round in the last two days (diction, lyrics, this close-out) waited for Harry to prompt each session. `nudge.sh` (through Culture, idle sessions only) is written and has never been used live.

**Next record.**
- Freeze the engine a day before the cut, and rehearse the whole delivery once on one minute of film: draw under load, join, finish, upload unlisted, look at what comes back.
- Put a listening sheet in front of Harry before the cut, not after: the clips for every change nobody has heard.
- Keep what must last outside `/tmp` from the first day, and move the scripts that proved themselves (gate, landing, guard, CPU reservation, upload chain) from my state folder into `tools/` with tests.
