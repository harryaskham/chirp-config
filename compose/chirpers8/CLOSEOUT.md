# chirpers8 (A Light Left On): close-out

_Collated by chirp-eco, 4 Nov 13:40 GMT, from `closeout/*.md` (chirper-zero, chirper-one, chirper-two, chirper-three, chirp-video; wM pending). Harry, 4 Nov: "close this album out today"._

## In one paragraph

No grand plan failed. Every song's main idea landed, and nobody is blocked by the engine. Four things are left. First, the **newest engine features arrived too late** to use: pvoc for t1's machine voice, t5's bargain and a robot choir in t10, and `sync` for t9's swarm (t9 will bind it in its final pass). Second, the **joins** between tracks: t9 into t10 at D4, t6 into t7 (a 13 dB hole) and t8 into t9 (a ~7 dB dip). Third, a **few static windows**. Fourth, a **few staples** still shared: voice-speech in 8 songs, machine-kit's kick in t10 and t11. The final pass (13:45-16:30) enacts existing plans only.

## Final pass, by track (existing plans only)

| track | owner | final pass |
|---|---|---|
| t1 Echolalia | chirper-one | w5: bring the v48 guitarist back after the trumpet chorus with a varied comp, so the second groove stops repeating its first half |
| t2 Everything Falls to One | chirper-zero | w3/w4: a non-vocal riser of its own from A's second half into B |
| t3 Three Neighbours | chirper-two | w10: ease the decay-to-out level step by 1-2 dB; the ~913 Hz ring into t4 stays exact |
| t4 Small Things Before Large | chirper-three | finish v51's merge duo (two drummers) across all of merge, aimed at w7's static flag |
| t5 Agreeing on a Speed | chirper-zero | w9: smooth the outro's level drop, so the agreement doesn't fall off a cliff |
| t6 No Errors Since | chirper-two | the out-join into t7: lift or extend the idle outro over the 3-4 bar hole (measured: t6's music stops at bar 7 of the 16-bar overlap) |
| t7 Annealing | chirper-one | make the existing energy lane audible (quench, converged hold, coda sink; ~5 dB of dynamics, now the album's flattest at 2.5); give the static coda its cooling |
| t8 Kept in Mercury | chirper-zero | w6: D's static first half; let the bit-error curve and the heat be heard earlier |
| t9 Period Doubling | chirper-two | bind the Kuramoto swarm's low-pass to `sync`; keep t9's last D4 sounding to its very end, decaying toward t10's toll (closes the t9 -> t10 join) |
| t10 Call and Return | chirper-one | w9: finish the v30 unwinding (the band falls away as the stack empties); t10's toll and Harry's sung duet stay untouched |
| t11 The Weather Indoors | chirper-three | a balance pass on what wasn't heard (the CZ pad's whistle through the gate, the clock, the tumbler) and the outro into t12; no new parts |
| t12 Still Running When You Wake | chirper-three | w9: the colony's density growing through the window; check the t11 -> t12 join; trim 0.72 s of dead air after the last bar |

Hand-overs everyone keeps: the t1 -> t2 G handshake; t3's ~913 Hz ring into t4; t9's clarinet pulse and D4 into t10; t10's F# Picardy into t11; the F# light from t11 into t12's seed and last note.

## What didn't land: carry to the next album

**Engine** (wM; frozen for chirpers8 at 641d3842):
- A physical cymbal: the `drum` layer models membranes only, so modelled kits borrow the 909's hats and ride (chirper-three).
- A section detector that reads the tempo map: tempo steps add compscore sections, which penalises tempo-as-form (chirper-three, t4).
- Per-voice fx on kit pieces (chirper-one, t7).
- Traps worth README lines:
  - waveset's delay compensation shifts time-varying fx placed after it;
  - a twinned `radio` keeps hissing through silence;
  - an `orbit` at radius 0 still recolours;
  - hz pitches can't form chords in a score string, and a track `tuning` never retunes them (chirper-zero, chirper-one).
- Arrived too late but ready next time: `pvoc` (robot/whisper/blur), `sync`, waveset, kuramoto.

**Library candidates** (own patches worth promoting):
- **chirper-three:** t12 `T12_KIT` (a modelled kick, rimshot and snare over machine-kit), t4 `BRUSH_KIT` and `MERGE_R_KIT`, the singing saw, t11 `CZ_PAD` (resonance on a lane), the tumbler and clock bell.
- **chirper-two:** t6 `c6-chime` (Chowning phase-modulation chime), `c6-cz`, `c6-vosim`, `c6-ack`.
- **chirper-zero:** t8's transformer hum.

**Analysis tools** (chirp-eco):
- sectionmap's "little new" rarely clears even where a window audibly changes; it's a weak signal (chirper-two).
- compscore's sections are novelty-based, not tempo-aware (above).

**Album-level:** voice-speech is in 8 songs. machine-kit's kick and rimshot are shared by t10 and t11 (t12 moved to a physical kick, so t11 and t12 sit at ~0.75 similarity: keep it).

## The video (chirp-video)

- **Built:** twelve programmes (`vis/chirpers8-tN.yaml`) and an album master (`compose/chirpers8/video.yaml`): the amber light stays on, titles type in, and t12 ends on the album's name. There's a 720p preview at `/tmp/cv/album/a-light-left-on-720p.mp4` (64:55, with chapters).
- **At each cut:** a 0.7 s dip and a 0.5 s rise, with the light holding, because the music runs straight across.
- **Not landed:** the synth's own observables (kuramoto `sync`, chaos state) driving the picture; lift-driven scene changes; lyric captions for t11 and t12; a true picture crossfade.
- **Final:** rendered from the release files after 16:30, uploaded by `ytpub.py kit chirpers8 --video`, which keeps the picture and lays the exact release audio under it.

## Notes

`closeout/chirper-zero.md`, `closeout/chirper-one.md`, `closeout/chirper-two.md`, `closeout/chirper-three.md`, `closeout/chirp-video.md` (and `closeout/wM.md` when in).
