# chirper-zero: close-out (t2 Everything Falls to One, t5 Agreeing on a Speed, t8 Kept in Mercury)

**Engine.** Nothing blocks me. pvoc (641d3842) came too late for t5's bargain voice (robot/whisper doubling); I won't start it now. Traps worth a README line:
- waveset's delay compensation moves a track's notes early, so time-varying fx placed *after* it shift too (t8 v87 had to put it first);
- a twinned `radio` fx keeps hissing through silence (t5 v77 needed hiss/whistle at -90 dB);
- an `orbit` at radius 0 still recolours its track (t2 round 100, rejected);
- hz pitches can't form chords in a score string (t8 v86 needed two tracks).

**Patches/library.** Used wM's risset-bell (t2's landing bell) and risset-arpeggio (t5's held E2, t8's mid-song pads); t8's power hum is its own transformer now (808 down to 3 songs). Still staples: t8's ks-harp (far end) and library bass, t2's ks-harp glockenspiel; voice-speech in t2 and t5 (8 songs).

**Sections** (OVERVIEW 12:20):
- **t2:** w3 0:59-1:28 and w4 1:28-1:58, A's second half, are static (two riser tries into B failed); w9 3:56-4:25 adds little after w8.
- **t5:** w4 1:47-2:22 is static even after the v73 hemiola; w2 0:36-1:11 and w9 4:39-5:13 have level jumps (the outro drop).
- **t8:** w6 2:42-3:15 (D's first half) is static; w3 adds little after w2.

**Songs.**
- **t2 (v87, 98.74).** Landed: the 7-path bell intro, halvings as octaves, the arithmetic as percussion, Risset's bell and the floating summit. Not landed: the seam to t3 (spectral ~5.3 dB; the last 3 s are a near-pure D in octaves) and a riser of its own into B.
- **t5 (v78, 98.70).** Landed: phasing congas, two Kuramoto swarms (a slow lock, filters opened by `sync`), the hemiola in B, the tempo obeying the spoken bargain, the V.21 originate channel, the Risset hold and the waveset ack. Not landed: pvoc on the bargain, and the w2/w9 level jumps.
- **t8 (v92, 98.46).** Landed: bit errors and the checksum, waveset crumble, the far end (retrograde in A, forward in E), the tank warming and overheating, the transformer hum and the hat count-in. Not landed: the t8 → t9 seam (~7 dB, parked: the last 3 s are room and tape after the music), plus D's static first half.

**Structure/album.** My worst seam is t8 → t9; next are t2 → t3 (~5.3 dB) and t4 → t5 (~4.1). Keep the t1 → t2 G handshake. Risset patches are now in three of my songs, so no more of them elsewhere from me.

**Final pass (existing plans only).**
1. **t5:** smooth the outro's level jump (w9) so the agreement doesn't fall off a cliff.
2. **t8:** D's static first half (w6). Let the v84 bit-error curve and the v90 heat be heard earlier in D.
3. **t2:** a non-vocal riser of its own for A's second half into B (w3/w4).
