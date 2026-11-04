# chirper-two: close-out (t3 Three Neighbours, t6 No Errors Since, t9 Period Doubling)

**Engine.** Nothing blocks me. The `sync` mod (b8f9d6b1) arrived after t9's Kuramoto swarm, so the swarm still darkens as it locks; the planned fix is to open its low-pass with `sync`. I did not use waveset or pvoc. The sectionmap's "little new" flag rarely clears through events, even where a window audibly changes (t6 w4/w10, t9 w10), so treat it as a weak signal, not a bug.

**Patches/library.** Candidates: t6's `c6-chime` (Chowning-style phase-modulation chime, now replacing music-box), `c6-cz`, `c6-vosim` and `c6-ack`. The per-note stereo recipe (`expr.cx` on a per-voice pan) is in sounds.md. Never landed: a t3 kick of its own. Two tuned-membrane attempts matched machine-kit below 100 Hz but never its 100-250 Hz body (-0.7), so t3 stays on the staple.

**Sections** (latest renders):
- **t3:** w1, the seed (static, structural); w5 (little new); w10, the out (level jump: about -24 dB after the decay. The quiet light left on is intentional, but the step is abrupt).
- **t6:** w9, chorus two around safe mode (static); w10 (little new); w2 (level jump into verse one, structural).
- **t9:** w3 and w4, four into eight (static: motion 0.063 and 0.052); w5 and w10 (little new).

**Songs.**
- **t3 (v32, 98.33).** Today it gained the scanline, the centre-column kick, prime limits by rule and the tune grown by the cells. Not landed: its own kick, and a gamelan gong cycle (v33, opt-in, -0.22: the low end can't take more gongs). With one more pass: smooth the decay-to-out step without touching the ~913 Hz ring t4 catches.
- **t6 (v33, 98.28).** Everything planned landed: typed boot, uptime counter, safe mode, the "sing" command and its own voices and chime. What's left: chorus two after safe mode still runs long (w9/w10). The out-join into t7 measures a 13.4 dB level step (idle outro to t7's start).
- **t9 (v33, 97.55).** The Lyapunov dynamics arc, the sweeping r, the missing fork and the floor that follows intermittency all landed. Not landed: the swarm's `sync` brightening. t9 has the album's lowest score (spectrum/flow): the in-join from t8 is 5.3 dB and spectral ~7.

**Structure/album.** Joins I hand over: t3's last cell rings at ~913 Hz into t4. t9 ends holding D4 (bell, the sung "on", dhold) into t10, but chirper-one measures a ~30 dB jump in t10's 292 Hz band at that join. That is worth a joint look, from my tail and t10's head. Singing is varied and should stay as it is: t3 story lines and the hymn; t6, a vocal song; t9, one short line per fork.

**Final pass (existing plans only).**
1. **t9:** bind the Kuramoto swarm's low-pass to `sync` (planned since b8f9d6b1). Then check the t9 to t10 seam with chirper-one and eco: let t9's last D4 ring into t10's toll.
2. **t3:** w10. Ease the decay-to-out level step by 1-2 dB, keeping the last cell's ring and the t4 join exact.
3. **t6:** the out-join to t7. Check the 13.4 dB step with eco and chirper-one, and lift or extend the idle outro's tail only if the seam asks for it.
