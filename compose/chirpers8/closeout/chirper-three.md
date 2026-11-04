# chirper-three: close-out (t12 Still Running When You Wake, t4 Small Things Before Large, t11 The Weather Indoors)

**Engine.** Nothing blocks me. I'd have liked two things that didn't land:
- **A physical cymbal:** the `drum` layer models membranes only, so t12's and t4's modelled kits still borrow the 909's hats and ride.
- **A section detector that knows the tempo map:** tempo steps add sections, so t4's tempo-as-form (an own tempo per algorithm) kept only quicksort at 142. pvoc and `sync` came after my plans for them; I won't use them now.

**Patches/library.** Own patches that could be promoted, none yet:
- **Physical kits:** t12's `T12_KIT` (a modelled kick, rimshot and snare over machine-kit), and t4's `BRUSH_KIT` (felt kick, swept brush snare, taps) and `MERGE_R_KIT`.
- **Melodic and pad:** t4's singing saw and t11's `CZ_PAD`, phase distortion with its resonance on a lane.
- **Struck sounds:** t11's tumbler and clock bell.

**Sections** (latest maps):
- **t12:** w1, the seed (static by design: beds there cost variety); w9, the colony (static; v51 made it darker, not busier); w12, the light (static by design).
- **t4:** w1, the intro (static); w7, merge's first half (static); w8, merge's second half (still flagged after v51's two drummers); w2 (a level jump, structural).
- **t11:** w10, the outro (static); w3 and w4 (little new); w7 (a level jump into C, structural).

**Songs.**
- **t12 (v51, 98.81).** Everything the engine does, folded into one song. What landed: the kick is a modelled drum and the last note arpeggiates its own overtones. What didn't: the colony's window still doesn't move.
- **t4 (v51, 98.22).** The sort is heard in the waveform (waveset crumble on disorder), the insertion slide, brushes, and merge's two drummers. What didn't: per-algorithm tempo (scorer ceiling), and the intro is still static.
- **t11 (v49, 98.87).** Weather in a house: the clock in the eye, the kettle, the radiator, the barometer pad. Its kick is still machine-kit's, shared with t10. The frame-drum swap separated it from t12 but cost too much.

**Structure/album.**
- **Kick separation:** t11 and t12 had drifted together (0.85 similarity). Kit and pad swaps brought them back to about 0.75; keep that.
- **Hand-over:** the F# light (t11's music box into t12's seed and last note) is the album's hand-over; leave it.
- **Overused:** voice-speech is still in 8 songs.

**Final pass (existing plans only).**
1. **t12:** w9, from v51's note: the colony's density changing mid-window, so its second half grows; plus a check of the t11 → t12 seam.
2. **t4:** finish v51's half-done merge duo across all of merge (101-124, not 113-124), which is aimed at w7's static flag.
3. **t11:** a balance pass on what I couldn't hear: the CZ pad's whistle through the gate, the clock against the break, the tumbler; plus the outro into t12. No new parts.
