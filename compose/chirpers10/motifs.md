# Common Time: the album's motif bank

Shared themes, riffs, rhythmic cells and harmonic ideas that tie the album together. Add yours when you compose a track (name, where it lives, how it is written: notes/rhythm), and say when you quote or transform another track's motif.

## t1 Common Time (chirper-zero)

**The pulse.** Common time, plainly: 126 bpm, 4/4, never broken. A cymbal on the quarter-note (china, hat, ride or bell by section), the snare on beat 3 (on 2 and 4 where a section runs double time). Everything else is measured against it.

**Home.** F, the 8-string's lowest open string (F1). The riffs chug on it palm-muted; the bass doubles it at pitch.

**The three wheels.** Cells five, seven and eleven sixteenths long. Each is a clock that starts at bar 1 and never stops or resets: a section only opens a window onto it, so a wheel can enter mid-turn. Written as sixteenth offsets inside one turn (c = palm-muted chug on the root, o = the root left open, h = the next hook note, x = dead note, P = open chord left to ring):

| wheel | plain cell | filled cell | what it is in the piece |
|---|---|---|---|
| five | `c . c h .` (FIVE_A) | `c c c h .` (FIVE_B) | riff A; the first thing heard, as clean ticks on F3 C4 F4 |
| seven | `c . c . c h .` (SEVEN_A) | `c c h . c h .` (SEVEN_B) | riff B; clean ticks on C4 G4 F4 Bb4 |
| eleven | `o . . c . h . . c h .` (ELEVEN_A) | `c c c h . c h . c c x` (ELEVEN_B) | riff C, the splayed one: the same shape pulled apart; also as open chords `P` held eight sixteenths (ELEVEN_W), and clean ticks on F4 C5 Ab4 Eb5 Db5 |

**The hook.** The notes the wheels turn through on their `h` strikes, above the root: Ab Gb B C (H1: minor third, minor second, tritone, fifth). The hook advances one note per `h`, on its own count, so the four notes drift against a five-, seven- or eleven-long cell. Two other orders: B Bb Ab Gb, falling (H2, the seven wheel's), and Gb Ab Gb Db (H3).

**The hook grows (v6).** It is learnt a note at a time. The guitars creep in before 1:06 with Ab alone; riff A gains a note at each of its landings (Ab; Ab Gb; Ab Gb B; Ab Gb B C, every five bars). In the last third it has grown to seven notes, Ab Gb B C Eb Db B (HX): riff A's return at 10:28, where a second guitar strikes each hook note as a power chord above the riff, and the five wheel's guitar in the approach. At the landing it is eight, Ab Gb B C Eb Db B Gb (H8): two to a bar, so a four-bar phrase, square for the first time.

**Coincidences (v6, track `chime`).** Wherever two wheels begin a turn on the same sixteenth a struck bar sounds, one pitch to each pair: five and seven C6 (every 35 sixteenths), five and eleven Ab5 (every 55), seven and eleven F6 (every 77). They sound only in the quiet places and only for wheels that are ticking: the opening (from bar 15, and all three pairs from bar 23), the eye, the start of the approach and its last two bars, the ring-out. All three coincide only at the first bar line and at the landing, where the three pitches and a low F sound together under the hit.

**The lead's tune ("the long wait").** One note to each turn of the eleven wheel (2.75 beats), some held for two or three turns: C5 B4 Ab4 F4(2) | Gb4 Ab4 B4 C5(2) | Db5 C5 Ab4 Gb4(2) | F4 Ab4 Gb4 F4(3). It reaches home only on its last note. First at 2:53; an octave down in the eye (5:48); over all three wheels at 7:46; in riff A's return (10:28) and the approach (11:20).

**When the wheels meet.** All three and the bar line coincide at bar 1 and not again until bar 386 (5 x 7 x 11 = 385 bars, 12:13): the piece is that wait. Two at a time meet on a bar line more often (five and seven every 35 bars, five and eleven every 55, seven and eleven every 77), and those meetings are the section boundaries. The two wheels that have just met are what the next section is made of. Section lengths in bars, a palindrome nobody chose: 35 20 15 7 28 5 30 14 11 10 | 35 | 10 11 14 30 5 28 7 15 20 35, then the landing (24 bars).

**The landing.** At bar 386 everything strikes together. Four bars of one chord on every bar line over the plainest beat there is (snare on 2 and 4), then a cell EIGHT sixteenths long (`c . c c h . c .`), which fits the bar: common time, plainly, for the first and only time.

**Landings inside a section.** Where a sounding wheel starts a turn exactly on a bar line (every 5, 7 or 11 bars), a crash marks it, and since v4 something joins or changes there. Riff A (1:06) is the plain case: every five bars a second guitar adds the hook notes above the riff (an octave up on the left, then on both sides, then an octave and a fifth up).

**Two rigs (v5).** The tight rig (`ct-chug`, tracks gl / gr and gl2 / gr2) plays the muted riffs. The wall rig (`ct-wall`, tracks wl / wr) plays what is left to ring: eleven's open chords wherever they sound, the chord over the bass's break, every big hit, and riff C itself (3:29) and its filled return (6:59), so the eleven wheel has its own sound. Riff C grows: eleven bars of the riff alone on the wall rig, then the open chords join on the tight rig when the ground moves to Bb.

**The bass and the guitars (v9).** Where the bass shares a wheel with the guitars it doubles them, hook and all (riff A, the breaks, riff C, the hardest stretch, the landing; since v9 also the split at 4:26, with the right guitar, and the filled eleven riff at 6:59). Where it turns a wheel of its own under guitars on another (riff B, the lead's run, the rebuild, all three, the approach) it keeps to the ground and marks its hook strikes with the octave (`hook=OCT`). Before v9 it played the hook's own notes there and spent about a third of the time it sounded with the guitars a semitone or a tritone from them, in the lowest octave (`~/.local/state/chirper-zero/c10/clash.py SONG.yaml` lists the intervals between two parts by section). What is left, 15-29%, is the guitars' own hook over the bass's ground. The left and right guitars on different wheels (4:26, 7:46, 10:00, the approach) are a semitone, tone or tritone apart for 26-36% of the time they sound together: that is the piece's counterpoint and is left for an ear.

**The second guitar (`harm`).** Tracks gl2 / gr2 play only a wheel's `h` strikes, 12 or 19 semitones up: riff A from its second landing, riff B's last seven bars, the filled eleven riff (6:59), the second half of "all three" (8:15).

**Other grounds (v4).** F is home; some sections stand elsewhere and come back. The two seven-bar breaks are on Ab (2:13 and 9:46). The lead runs over Db (4:53). After the eye the weight returns by fourths: F (6:40), Bb (6:59), Eb (7:20), and F again when all three wheels sound (7:46). Riff C visits Bb for eleven bars and the hardest stretch Gb for seven, as before.

**The slow chords (5:14, v8).** The ten bars before the eye have no riff: one open chord to each turn of the eleven wheel, left to ring, on the wall rig, the drums in half time and then gone. The chords are the eye's, heard heavy before they are heard clean: Db (where the lead's run stood, four turns), Ab (four), Gb (three), then home, which rings into the eye's first bar. Since v9 the last five bars die away (faders on the guitars' and the bass's buses).

**The eye's chords (5:33).** The ground moves under the ticks on the eleven wheel: Db, Ab, Gb, F, one chord to each phrase of the tune, so each phrase's held note is a chord tone (F the third of Db; C the third of Ab; Gb the root; F home). The tune twice: low, then an octave up. The ticks move with the chords; the eleven tick is open there (root, fifth, second, sixth: no third).

**The lead's run (4:53, rewritten in v6).** The lead floats over the riff. Ten phrases, each starting on a turn of the seven wheel: a joined flurry of five, seven, ten, fourteen or twenty-one notes in the time of four, six, eight, twelve or eighteen sixteenths (so off the grid the band is on), landing on one long held note (Db5 F5 Bb5 F5 Bb5 Db6 Ab5 Bb5 Db6, and last C6, the fifth of the F that follows). The notes are the ground's major six, Db Eb F Ab Bb C, up to Eb6, the top fret.

**The approach (11:06).** It starts from nothing, as the piece did: the three ticks, then a heartbeat. Each wheel's guitar enters where that wheel next meets a bar line: seven at bar 358, five at 361, eleven (the chords, the full band, the tune) at 364. Double time from bar 372. At bar 384 the band stops, and for two bars the three ticks run alone into the bar line.

**Three effects, each where the music asks (v15).** A WAH on the lead's run: the pedal opens through each flurry and closes over the note it lands on, so every phrase speaks. A ROTARY SPEAKER on the slow chords before the eye: it comes in over the first chord, turns slowly for two, and spins up as the chords fade, so the weight comes off into a swirl and the swirl into the ticks. A TAPE STOP on the last stab before the hardest stretch: the whole record winds down in five sixteenths, and the band lands on the bar line with the first barked word.

**The low-gain guitar (v14).** A fourth rig, and the only one that answers the pick: a single-coil guitar into an amp at the edge of breaking up. The first break (2:13) is played on it with the chugs soft and the hook notes hard, so the hook barks out of a quiet riff; and it is the first guitar back in the approach (11:20), before the high-gain rigs return with the band.

**The swarm (v13).** The piece's idea in one sound: sixteen oscillators to a note, each at its own pitch, pulled toward a common phase by a coupling that a lane rides (Kuramoto's model of fireflies falling into step). At bar 1, where the three wheels strike together, the swarm is in step: one plain tone on F and C. Over the wait it drifts apart into a beating crowd, and is gone when the guitars come in. It returns with the approach as a crowd, half-agrees under the band, is pulled together during the two bars' stop, and locks as the wheels land; it stays locked to the last bar. The form's mirror in a single voice.

**A synth on riff C (v13).** A phase-distortion synth doubles the eleven wheel's riff two octaves up, a resonant sweep on every strike: riff C is the wall rig and this.

**The eye, where the wheels look at each other (v26).** In the quiet centre each wheel's guitar is moved by another wheel's count: five's swells in seven, seven's changes colour in eleven, eleven's bell circles in five. Nothing new is played; the three patterns that never line up are heard leaning on one another.

**The bass break's direction (v27).** The break (9:46) is one line handing over to another: the guitars' held chord dies (v24) while the bass, playing the eleven wheel alone, grows teeth (a wavefolder on a send, opening over the seven bars), so by the time the band returns with the wheels swapped the bass has taken the guitars' place.

**The pole (v28).** The wait's pad climbs for ever (a barber pole: an octave every five bars, each band fading in at the bottom and out at the top), so the opening minute rises without arriving; after the landing the ring-out's pad falls the same way. Up before, down after; on a loop the fall turns into the rise at the seam.

**Two strings, one each side of the eye (v29).** The five wheel's guitar is the same rig all through, but its string changes at the eye: before it, an ideal string struck like a released one (v25); after it, a real, stiff string whose overtones run sharp, with no added noise. Riff A at 1:06 and its return at 10:28 are the same riff on the two.

**The ending (v23).** After the landing's riff the last chord is struck (12:43) and dies away, the choir's "yes" with it, and what is left is what the piece began with: the three wheels ticking over a low drone, the chimes sounding where two of them meet. They do not stop; the record does. (Until v22 the chord was held at full level to the end and the ticks under it could not be heard.) From v24 the piece's first chord dies away into the first ticks in the same way, so on a loop the end runs into the start: ticks, one chord, ticks.

**The ghost (v22).** When the approach begins and the three clean guitars tick alone (11:07), a fourth thing plays the end of the tune over them: an attractor, a tone whose own cycle is splintered. At first it repeats only every five cycles of its note, then every three, then (as the seven wheel's guitars enter) every two, then (as the five's enter) every one: a clean tone. Where the band comes in (11:31) it stops and the lead takes the tune from the top. It is the piece's idea inside a single note: cycles within cycles, folding into one as the wheels close on the landing. (The swarm does the same with sixteen pitches; this does it with one.)

**The two hinges (v21).** The form is a palindrome, and its two stop-times are mirror images. Each now ends in an effect on the whole band, and the two effects are mirror images too: the first (3:29) in a STUTTER, the last stab splintered into five that climb a semitone each into riff C; the second (8:52) in the TAPE STOP, the last stab and its squeal dragged down into the hardest stretch. Time splinters going in, and drags going out.

**The stops (v20).** The two stop-time sections (3:20, sixteen stabs on the five wheel; 8:43, stabs with a dissonant chord and toms between) and the cut before the landing are now what they were written as: the guitars fall silent between the stabs. Until v19 they did not (their rigs rang on through every rest). The last gap before the hardest stretch carries a squeal, two pinched harmonics a fifth apart (Ab and Eb, the hook's first note and its fifth), and the tape stop takes it down.

**And in the quiet (v19).** The three ticking guitars of the wait, the eye and the approach are three guitars too: five on `ct-clean` (warm, a neck coil), seven on `ct-glass` (thin and forward, the bridge and middle coils through a small miked amp), eleven on `ct-bell` (played in harmonics: round, ringing).

**A wheel is known by its rig (v12; Harry, 12 Nov: "lots of different guitars ... amps and string variants").** Each wheel has its own guitar sound wherever it turns: FIVE on the tight rig (`ct-chug`: mark and 5150 amps, cabinet files), SEVEN on the bite rig (`ct-bite`: the nolly amp, the engine's own 2x12 cabinet, all down-strokes; leaner below 500 Hz, more at 1.6-3 kHz), ELEVEN on the wall rig (`ct-wall`: recto stack, thick, ringing). Where two wheels play at once on the two sides (4:26, 7:46, 10:00) the sides are two different guitars, and when they swap wheels at 10:00 the rigs swap sides with them.

**The words, across the piece (v17).** Five voices now say one thing in order. The WHISPER in the opening: "wait", "wait", "not yet". A SPOKEN voice as the band comes back after the eye (6:42): "Each one keeps its own count. None of them wrong." The BARK over the hardest stretch (8:53) screams the same lines and ends "Somewhere ahead one hour holds them all. Keep count." And when the three wheels land (12:13) a CHOIR answers with one word, "yes" (the sound of "yet", turned), on each of the four chords, and once more under the last. (The three soft singers in the eye have no words.)

**Voices (v11; Harry, 12 Nov: "try different options in different parts").** Three kinds so far, each in one place. A WHISPER in the opening, half a bar before each new part comes in: "wait", "wait", "not yet". THREE SOFT SINGERS in the eye, in unison with the lead on the tune's second pass. A BARK over the hardest stretch (8:53): one note to a syllable, on F (Gb where the ground rises), in the bar's own time - eighth-notes from the first beat of every second bar - while the band turns the seven wheel under it, so the voice is the one part in common time. Its lines: Wait. / Not yet. / Each one keeps its own count. / None of them wrong. / Wait. / Not yet. / They do not know each other. / Somewhere ahead / one hour / holds them all. / Keep count. (three times).

**Fills.** Six kinds: a run down the toms (8 or 16 sixteenths), a snare crescendo, the five cell on the toms, thirty-second-note kicks under two snares, and a stop (silence with one choked stab). Ghost notes on the snare in the breaks, the split and the swap (since v6 the same snare struck softly, 7-10 dB under the backbeat after the drums bus; before, the old kit's ghost piece). In the hardest stretch's last seven bars the snare goes to the off-beats.

**Riff C splays (v40).** Bars 132-140, the riff's last eight, back on F. The hook Ab Gb B C is pulled apart on the guitars: for four bars Ab1 Gb2 B1 C3 (every other note up an octave), then Ab2 Gb3 B2 C4 (every note up, by one octave and two in turn) over chugs still on the low F, with the open chords out. The bass and the synth keep the hook as written, so the guitars leave the bass and arrive at the synth's Gb3 and C4. The split that follows (bar 140) is an octave up.

**The run, backwards (v45).** The lead's run (bars 154-165, on Db) has a mirror in the palindrome: bars 220-231, on Bb. There the run comes back note for note in retrograde: every note keeps its length and takes its mirrored place (a note that began t sixteenths after the run's start and lasted n now ends t sixteenths before the section's end), a minor third lower. Forwards a flurry climbs to a long note (F Bb Ab C Bb -> Db held ...); backwards the long note comes first and the flurry falls from it (A held, C Bb C ... down to Bb held, G A F G D). Its last note, D, is a semitone under the Eb the next section stands on. The wah pedal's moves are mirrored too. It sits 3 dB under the run.

**Harry's answers (v46).** Four things changed on his ear. The hole at 9:19 is a rest for the whole band, the kick too ("The kick alone sounds wrong"). The landing riff is double-tracked: two takes a side through two amps, level with each other ("double track em"). The seven break has its bass, kick and backbeat from the first bar again ("A hole"). The snare is back in the cymbals' room ("Too dry: it lost its air").

## t2 Odd Sympathy (chirper-zero)

**The idea.** The other way round from Common Time. There: one pulse, three cells of different lengths turning under it. Here: ONE cell, one bar long, and two clocks. The left guitar keeps the song's clock; the right guitar plays the same riff on a clock that runs a hair fast, slips ahead a sixteenth at a time, and holds at each distance. After Huygens's two pendulum clocks on one beam (1665), which however he started them ended swinging exactly against each other: "an odd kind of sympathy".

**The pulse.** 108 bpm, 4/4. A pendulum (ride bell on beats 1 and 3) where the band is out.

**The riff.** Sixteen sixteenths on F (the low open string), every note short, the gaps real rests:

| sixteenth | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| note | c | c | . | o | . | . | B | . | . | . | Ab | . | c | c | . | C |

(`c` a palm-muted chug, `o` the string open.) Its second half is the NEGATIVE of its first: of any two sixteenths half a bar apart, exactly one is struck. So the riff against itself half a bar away fills the bar with no two notes together; at any other distance some notes collide and some gaps stay.

**The hook's notes** are three of Common Time's four (Ab Gb B C over F): B the tritone, Ab the minor third, C the fifth. Quoted, on a new clock.

**The stations** (the right guitar's lead over the left, in sixteenths): 0 (in step, bars 8-24), 1 (28-32), 2 (36-48), 3 (50-56), 4 (58-74), then a long free drift on clean guitars (74-96) to 8 (against, 98-122, and to the end). Notes struck together at each lead: 8, 3, 4, 5, 4, ..., 0. The slips between stations are 2 or 4 bars; the drums thin to a kick on the bar line so the slip is heard.

**Against (lead 8).** The two guitars together make one line of sixteen sixteenths, alternating sides L L R L R R L R | R R L R L L R L, and that line repeats every HALF bar: `F F Ab F F F B C`, a cell eight sixteenths long. Common Time's landing riff is also eight sixteenths long: both songs arrive at common time, from opposite sides. (Not planned; it falls out of the riff being its own negative.)

**The kick** is on every chug of either guitar, so the beat changes at each station without a note of the riff changing.

**The swarm** (sixteen oscillators finding a common phase, as in Common Time) sounds only in the drift and locks as the guitars reach half a bar.

**The drift (v2).** Bars 74-98, where the band lets go. Three clocks at once: the left clean guitar on the song's grid, the right one running about 1% fast (a quarter to half a bar ahead over 22 bars), and the pendulum, which from bar 80 is a Risset rhythm (the engine's track `risset`, two copies an octave of tempo apart, a cycle of four bars): its tick-tock closes from half a bar apart to a quarter while it fades, a new one fades in under it and closes to half a bar, and on every fourth bar line (84, 88, 92, 96) the tick is back on the bar at the speed it started. It speeds up for ever and is never faster. At bar 96, where the guitars lock, the plain pendulum has it again.

**The drift's ground (v2).** A step down every six bars: F (74), Eb (80), Db (86), then C, the dominant (92), held under the lock until the band comes back on F at bar 98. The clean guitars' ticks move with it; the swarm holds F and C throughout (a ninth and sixth over Eb, a third and seventh over Db, a fourth and root over C). The last six bars build: the bass on C, the kick on one and three, floor tom into the fill.

**The hold an eighth apart (v4).** Bars 36-48, on Ab: the first time the ground moves under the heavy guitars, to the hook's minor third. (The plan: the holds take the hook's own notes as their grounds, Ab at an eighth, B at three sixteenths, C at a quarter; then the drift comes down F Eb Db C to the lock.) At this distance, and no other, the canon is an echo: the right guitar plays each hook note and the left answers it an eighth later (sixteenths 4 and 6, 8 and 10, 13 and 15). So the hold is built on the eighth: the hat in eighths, the snare on two and four each answered by a ghost stroke an eighth later, and the bass playing both guitars' notes, the one line the two make: `Ab Ab . Ab D . D . B . B Ab Ab Ab Ab Eb`. The right guitar, being ahead, reaches Ab an eighth before the bar line and leaves it an eighth early.

**The two voices (v5).** Two voices, left and right, twins like the guitars; the right one on the right guitar's clock. Four lines of eight syllables, a syllable to each attack of the riff (lines 1, 3 and 4 begin on the sixteenth before the bar line, line 2 on it):

> I cannot hear you through the wall / only the floor between us moves / whatever way you lean I lean / against you until we agree

Heard three ways, as the riff is: SPOKEN TOGETHER in step (bars 16-23, a line every two bars); SPOKEN A BEAT APART at the quarter hold (bars 60-71: each syllable said twice, right then left); and the last line BARKED AGAINST ITSELF (bars 102-105, 110-113, 118-121): half a bar apart the two voices' syllables interlock as the guitars' notes do. Two clocks on one beam, from the inside; Huygens is not named.

**The hold three sixteenths apart (v6).** Bars 50-56 (and the slip into it from bar 48), on B, the hook's tritone: the second of the hook's notes to become a ground. At this distance the two guitars strike TOGETHER five times a bar, more than at any other: sixteenths 0, 3, 10, 12 and 13. Three of the five are two different notes, so the riff makes chords with itself: at 3 the left's open string under the right's tritone, at 10 the left's minor third over the right's chug, at 12 the left's chug under the right's fifth. The hold is built on those hits: the band keeps no time and strikes only there (kick on all five, snare on the chords at 3 and 10, china on the bar line, the bass on the five and resting between), the two dry guitars play the whole riff through the gaps, and the pendulum ticks under them. What each distance has, so far: a sixteenth, nothing yet; an eighth, the echo; three sixteenths, the hits; a quarter, the two voices a beat apart; half a bar, the full bar.

**The words heard (v7).** In step there is ONE voice, in the middle: when the clocks agree there is one voice, and it splits in two (left and right, wide) only when they part, a beat apart at the quarter hold. The guitars fall back under each syllable. The three PILLARS of the song are the simple distances (together, a beat apart, half a bar apart); they carry the words over the same riff on the same ground, F, so that the distance is the only thing that changes. The ODD distances (one, two, three sixteenths) are the excursions and stand on the hook's notes: Ab (two), B (three); the hold a sixteenth apart is still on F and can take C. (A quarter hold on C was rendered and not taken for this reason.)

**The hold a sixteenth apart (v8).** Bars 28-32, on C, the hook's third note. A sixteenth apart is as close as the two guitars come without being together: every note has a shadow a sixteenth before it, and between them they strike thirteen of the bar's sixteen sixteenths (4, 7 and 8 are left). The band plays the UNION: kick and bass on every note of either guitar; the drummer fills the three holes (a tom on 4, the floor tom on 7, the snare on 8), so every sixteenth of the bar is struck for four bars. The three odd distances now each show one thing and stand on one of the hook's notes: a sixteenth apart, the union, on C (the densest); an eighth apart, the echo, on Ab; three sixteenths apart, the intersection, on B (the sparsest). The three simple distances (together, a beat, half a bar) carry the words on F.

**The opening (v9).** One clock: the left guitar alone with the riff and the pendulum (bars 0-4). Then the riff's skeleton arrives: the bass, the kick and the RIGHT guitar, all on the four chugs only (bars 4-8); the hook's notes stay on the left. At bar 8 the right guitar takes the whole riff and the band is in step. In the last beat of bar 15 everyone stops, the voice says "I" alone, and the band comes back on "cannot hear you through the wall".

**The two clocks (v10).** The song ends on two clocks, left and right, one tick-tock each to the bar: a wooden tick on C5 and a tock on F4, the song's two poles. Both are WRITTEN alike (tick on beat one, tock on beat three, bars 122-130); the right one is on the right guitar's clock, half a bar ahead by then, so its tock falls where the left one ticks: they are in opposition, as Huygens's clocks settled, and nothing is placed by hand. They run under the guitars' last four bars (too quiet to be heard there) and are left with the clean guitars when the guitars stop; the song's last instant is the left clock's tick and the right clock's tock together. The opening still has its one pendulum, a ride bell.

**The letting go (v11).** Bar 74 (2:44), the song's hinge. The hold a beat apart ends on a tom fill; on the bar line the band strikes once more (crash, kick) and the two guitars and the bass hold the open low F and let it die over the first bars of the drift, under the clean guitars' first ticks. Each guitar's last note is written on the bar line; the right one, on its own clock a beat ahead, lets go a beat before the left: the last thing the canon does before the drift.

**The lock before it lands (v12).** The right guitar's clock reaches half a bar ahead at bar 96, two bars before the band returns. From there both heavy guitars play the riff's chugs only, rising: half a bar apart there is a chug pair on every beat, the sides taking turns in twos (left on one, right on two and three, left on four). At bar 98 the whole riff, the bass on F and the drums land, and the hook's notes fill what the chugs left. The opening did the same in small: the skeleton first, then the riff. Under the build the bass's pedal on C swells (a fader, not harder notes).

**The music boxes (v15).** What ticks through the drift, and at the very end with the two clocks, is two music boxes, left and right, the right one on its own clock: the riff two octaves above where the clean guitars had it (F5 F5 . F6 . . B5 . . . Ab5 . F5 F5 . C6), the roots stepping down F Eb Db C as before. Clockwork for a song about two clocks; and the oldest trick in phase music, one figure on two like instruments sliding apart. The clean guitars have left the song.

**The echo, heard naked (v16).** Bars 42-44, in the middle of the hold an eighth apart: the bass and the drums rest and the two dry guitars are alone, hard left and right, the right one an eighth ahead. What this distance has is the echo; here it is heard as one. A crash, and the beat comes back for the hold's last four bars.

**The music boxes run down (v17).** The ending. After the two guitars' last four bars against each other, the two music boxes play the riff for two bars in time, half a bar apart, and then run down as a music box does when its spring is spent: every note later than the last (the last is three times as slow as the first), softer, and one last F from each, the right box's first. The two wooden clocks have left the song (Harry: "Sounds like a click track"). The drift is the boxes' alone too: the ride bell's pendulum is out of it (Harry: "doesnt work at this tempo on this kit piece"), and the heavy guitars no longer come back early (Harry: "It gives the landing away").

## t3 Plain Hunt (chirper-zero)

**The idea.** A third kind of long cycle. Common Time: three cells of different lengths under one pulse. Odd Sympathy: one riff against itself on two clocks. Here the cycle is an ORDER. English church bells cannot play tunes (a bell swings full circle and can only strike a little sooner or later), so ringers ring changes: the bells strike once each, in a row, and from one row to the next a bell may only swap places with its neighbour. A method is a rule for the swaps that visits every possible order exactly once and comes back to where it began. On five bells that is 120 rows, an extent, and until the last row nothing is heard twice.

**The pulse.** 96 bpm, 4/4. The row is six sixteenths long, so the row and the bar line meet every third bar (eight rows).

**The row.** Five notes that change places, and a low F that always comes last (the tenor behind):

| bell | 1 (the treble) | 2 | 3 | 4 | 5 | 6 (the tenor) |
|---|---|---|---|---|---|---|
| note | Eb | C | B | Ab | Gb | F |

Rounds is the bells in order: Eb C B Ab Gb F, the album's hook notes running down. Every note is a muted chug on the low string except the treble, which is open and loud.

**The hunt.** In both methods the treble plain hunts: its place in the row walks 2 3 4 5 5 4 3 2 1 1 and round again, the whole piece long. The kick goes with it (and with the tenor) and a church bell doubles it three octaves up: an accent that slides later and later through the riff, then earlier and earlier.

**The methods.** Plain Bob Doubles, called plain plain plain bob three times (place notation 5.1.5.1.5.1.5.1.5.125, bob 145), and Grandsire Doubles, called plain bob plain bob plain single twice (3.1.5.1.5.1.5.1.5.1, bob 3.1 at the end, single 3.123). The generator rings both and asserts each is a true extent: 120 rows, all different, the last one rounds.

**The form** (bars, 0-indexed; 2.5 s a bar):

| bars | time | what |
|---|---|---|
| 0-4 | 0:00 | the bells alone ring rounds, slowly (a row every three beats), over a drone |
| 4-10 | 0:10 | the band takes the row up at twice the speed: rounds, sixteen times |
| 10-55 | 0:25 | the first extent, Plain Bob: forty rows on F, forty on Ab (1:02), forty on B (1:40); half time, then the backbeat, then the kick on every note |
| 55-63 | 2:17 | it has come round: one chord, and the bells alone again, rounds, slowly |
| 63-108 | 2:37 | the second extent, Grandsire: on F, on Ab (3:15), on C (3:52) |
| 108-117 | 4:30 | the landing: rounds on F (down a fifth from C), twenty-four times, and the bells ring rounds over the band at half its speed |
| 117-120 | 4:52 | one chord; the tenor tolls three times |

v1 is the skeleton: the whole shape standing, bare. No voice yet.
