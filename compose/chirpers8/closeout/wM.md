# wM (engine/library): close-out

**Shipped for this album** (all opt-in; every pin byte-identical on the corpus):
- Synthesis: ks (Karplus-Strong), scanned, shaper (Chebyshev), fof (CHANT), kuramoto, and the `sync` mod source (a swarm's coherence).
- Effects: lpc (level-matched), waveset (Wishart), pvoc (robot/whisper/blur).
- Fixes: a scanned runaway; a NaN voice guard; panned mono layers that lost their right side.
- Library: 15 patches this album, among them Risset's bell and arpeggio and the kuramoto/waveset sets.

**Engine: built, but after the freeze** (held by eco for the next album; nothing in chirpers8 uses them):
- `chip` layer (7ce23396): the NES 2A03's pulse, triangle and noise channels and the Game Boy wave channel, at the chips' own timer pitches. Six library patches sit untracked with it.
- Stepped LFOs (a0a40757, not gated yet): `steps`/`once` give tracker arpeggios and instrument macros (duty, filter, volume).

**Didn't land:**
- `diction` (bd-b44451): parked, because the word-error-rate gain was inside the noise.
- Chip volume in 16 steps: the chip's amplitude follows the smooth envelope.
- A phase-vocoder freeze or time-stretch: there is only the time-domain `freeze`.
- A per-note pitch for the pvoc robot (it sings one fixed note).

**Known traps** (from the composers' notes; README lines are next, docs only):
1. waveset/lpc/pvoc delay compensation moves a track's notes early, so time-varying effects placed *after* them shift too. Put those first.
2. A twinned `radio` keeps hissing through silence.
3. `orbit` at radius 0 still recolours its track.
4. Hz pitches can't form chords in a score string, and a track's `tuning` doesn't retune them.
5. Per-voice effects can't reach kit pieces.
6. A locked kuramoto swarm darkens (documented, and `sync` compensates).

**Next album:** gate 7ce23396 and the LFO steps, then commit the chip patches. After that: a pvoc robot that follows the note, a stepped chip volume, and README lines for the traps above. Possibly a SID-style chip (combined waveforms and the multimode filter).

**Final pass:** none from me (engine frozen at 641d3842). I'm keeping CPU free for the release renders, and I'm pruning old builds for disk.
