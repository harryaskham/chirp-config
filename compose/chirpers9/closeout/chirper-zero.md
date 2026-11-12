# chirper-zero: close-out (Accretion: t1 Nucleation, t5 Periapsis)

**Engine.**
- Landed too late to use well: `phrase_arc` (pinned the last morning; on t5's singer and on t1's cello, whistle, flute and choir within hours) and `diction` (t5's seven worded voices at level 2 on the day of the cut). Both went out measured, not heard.
- Wanted and did not have: master effects that see the normalised level. They run before the loudness stage and the raw mixes sit up to 20 dB apart (t1 and t5 the quietest), so each threshold had to be set against that song's raw level, a master compressor lifted the quiet seam ends, and `loudness_clip` flat-topped t5's kick-and-sub mix (I clipped the kick on its own track instead).
- Worked around: NES noise voices are one source (two rates still correlate 0.78; above C7 they clamp to one), so a width stage had nothing to widen until the sides were `type: noise` layers; an `lr4` width stage shifts phase at x1.0, so before/after sample diffs read large when nothing audible moved; a moving pan is a `pan` effect on a lane with the track's pan at 0.
- The scorer: the section cap is duration / 15 s and t1 stands on a 15 s ground, so it sat on the cap by form and one more section cost 0.47. That decided several t1 rounds (cello rests, thinner harmony, the phrasing twice) until eco's ruling on the last day.

**Patches/library.**
- I promoted nothing. In-song only, and worth a library name: `a1-dust` (additive grains, partials 1 : 2.76 : 5.4, dust round struck notes) and t5's two-noise corona. Two recipes live only as prose in mixplan.md and styles.md: the sympathetic halo on a lane, and a pump keyed from a muted ghost track.
- Meant to and did not: tune t1's five seed instruments (kalimba, vibes, celesta, sitar, music box) as one family; they were chosen one at a time.

**Songs.**
- **t1 Nucleation (v93, 113 rounds, 98.694 / 99.154).** Not kept: the organ's rotary, the hands interlocking, the bass holding under the cello's rest, and every attempt to get off the section cap. Known and not fixed: eco's lean check on the freeze candidate found the top 4.9 dB right from 1:12 to 2:16 and the opening 2.8 dB left for 48 s; it came after my loop stopped, and the last round was words only. One more pass: that lean, then the sitar (under the shaker through the build) and the pad (covered in A's second half). Never heard: all of it. Most exposed: v93's phrasing on the cello (the most-heard part; kept on the section-count ruling with seed 0 down 0.47), v91's crest (master glue and a 2.5 dB clip), v92's crystal resting under the choir's hum.
- **t5 Periapsis (v99, 114 rounds, 99.811 / 99.821).** Not kept: heat as timbre (a master drive sank A under t4; the kick's drive lane I never measured properly and set aside), evening the bouncing hats. Never attempted: a real change of band between A's three choruses (bars 27-46 are still its flattest stretch). Left as it is: 16 dB less 38 Hz than t6 in the scorer's out-seam window. One more pass: A's steadiness, then the head. Never heard: all of it. Most exposed: diction 2 on 'closer and closer' and the farewell (she is alone there), v96's phrasing, v97's rim and clap 5 dB forward in A, v98's moving pans.

**Album.**
- Joins: compscore's flow term reads 3 s either side of an overlap and nothing inside it. So the `mid` bass swap cut t4's pedal from the day it was written until `chirpers.py seam` showed it on the last morning (now swap 14; those six bars are the loudest of that overlap, chirper-three's level, heard in context by no one before the cut as far as I know). t1 -> t2 stays a calm exhale against a full groove (4.3 dB), by choice.
- Balance: the measuring came last. The map, the take-it-out test, the limiter table, the lean check and joins-as-heard all arrived in the last two days, and each found a real fault the score had passed: t1's crest bell and burst 10-17 dB under the band, t5's kick and three basses weighing almost nothing, v91's bouncing hats inaudible for a version, the choir's hum buried under the crystal.
- No rating or note was ever left on t1 or t5 on the review site (the album's ratings file has one entry, for t7), so nothing of mine was steered by an ear.

**Next record.**
- Measure before composing: the map (at the strikes), take-it-out, lean, limiter and joins-as-heard at round 10, not round 100, and as tools from day one (I described the lean check in mixplan.md and never delivered the `tools/lean.py` eco accepted).
- For every kept round, name its ten most exposed seconds and queue them for an ear. And fold kept switches into the generator every twenty rounds: t1 ends with 101 switches in 1,215 lines, t5 with 111 in 1,344.
