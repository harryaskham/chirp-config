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

**The riff assembles itself (v47).** The approach (11:06) was already things arriving one at a time: the ticks, the heartbeat, a guitar, a second guitar, the band. Now the riffs arrive a note at a time too. The seven wheel's guitar (right, 11:19) comes in as ONE muted note to each turn of its wheel, three times, alone over the ticks and the heartbeat, deep in a wet spring; then two notes a turn, three, four, the whole riff, and the spring dries as it fills in (the guitar comes nearer). The five wheel's guitar (left, 11:25) does the same, faster. The bass waits two bars. The spring's drip had nowhere to be heard (Harry: "I cannot hear it in the piece"): a spring answers a short note with nothing after it, and both of its places were riffs without a rest.

**Eleven arrives alone (v48).** When eleven's first chord lands (1:44) the five wheel's two guitars rest for five bars. The bass and the kick go on turning five; the wall guitars ring eleven's chords over them, the china with each chord. Ten seconds of the two wheels against each other and nothing else: five in the rhythm section, eleven in the guitars. The five wheel's guitars come back where five next meets a bar line (1:54), on a crash. Before, eleven came in under a riff that went straight on, and its arrival was a thickening (its chords sat 3 to 4 dB under the riff's guitars).

**The cymbal finds the bass's wheel (v49).** Riff B is seven against eleven: the guitars and the kick turn seven, the bass turns eleven under them, and for fourteen bars nothing said so (a ride bell counted quarters). Riff A's rule is that at every landing something joins; riff B's second landing (2:40) had nothing. Now, from there, the china strikes where the bass's eleven begins each turn, over the ride bell's quarters. Seven bars later the lead comes in with its tune, which is one note to each turn of eleven: the china's last stroke (2:52.9) and the tune's first note (2:54.2) are one turn apart. The cymbal marks the tune's clock before the tune arrives, and hands it over.

**The guitars speak (v50).** Harry's main word on the song: "the voice needs work is my main takesway, voice is weak". The weak voice was the talker at 6:42 ("Each one keeps its own count. None of them wrong."), and nothing I could measure made it stronger as a voice. So the lines are now said by the band: the two wall guitars hold the open chord through each line and the engine's cross-synthesis gives the chord the talker's moving spectrum. They sound only while he speaks; he stays under them, 9 dB lower than he was. The order of the song's voices is now: a whisper ("wait"), the machine itself (the guitars speaking), the bark (screaming the same lines at 9:01), the singers ("yes").

**Seven meets eleven, and the eleven has a body (v51).** Section 9 (bars 154-165) is the lead's run over the guitars and the kick on the seven wheel "while the bass turns eleven": the eleven wheel had one voice, the bass. Now the drummer's left hand turns it on the toms with the bass, strike for strike: the floor tom on the ground, the high tom where the bass jumps the octave, the snare where the backbeat falls. The right hand keeps four on the ride, the foot keeps seven with the guitars: three wheels in one kit. And the bass's eq now follows the ground on B flat, E flat, A flat and G flat (not on D flat).

**The tune comes back in harmony (v52).** Section round, 8:15-8:44 (windows 7:37-8:38). Where all three wheels turn together (bars 245-275) the lead plays the tune twice through. On its second pass (from bar 259.9) a second lead guitar plays it a third above, note for note on the eleven wheel: E flat over C and B, C over A flat, A flat over F, B flat over G flat, F over D flat, all notes of the piece's mode. The only place the tune is harmonised by another guitar.

**The landing has a floor (v53).** Whole-song round (the piece read stretch by stretch against the records; one finding acted on). Under the landing's four chords (bars 385-388, 12:13) each chord now has the sub drop the first one had, and the bass strikes with the kick's second stroke inside the bar where it held one note. No other note changed.

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

**The heartbeat, and the lock shaken (v18).** Two bars after the band lets go a pulse comes in under the two music boxes and stays to the landing: the bass in soft eighths on the ground as it steps down (F2, Eb2, Db2, C2), a closed hat on the quarters (eighths from bar 86), a soft kick on the bar line. It keeps the left box's time, so the right box slides against something. And one more slip, where the song had none: at bar 106, with the two guitars locked half a bar apart, the right one runs two sixteenths further ahead over two bars and falls back over the next two; the beat thins to a kick and a hat as in the other slips; the lock holds (a crash at bar 110, and the last barks).

**The voice in tune, and in the band (v19).** Harry: "yes but needs to be more realistic and in some kindof tune" and "On top, like a voice-over". In the first of its two passages (0:36-0:53, the clocks in step) the four lines are now SUNG: each syllable already fell on an attack of the riff, and now it takes that attack's note, two octaves over the guitars (F F F B A-flat F F C; a line that starts before the bar starts on the riff's last note, C). The words ARE the riff. A second singer sings the same line quietly on each side; the voice goes through the guitars' room; the guitars duck 2 dB under it, not 5; and it sits where the records' voices sit against the band, not over it. The second passage (2:13, the two voices a beat apart) is still spoken, on purpose, until Harry says which.

**The hold on B ends in plain agreement (v20).** The hold three sixteenths apart (1:51-2:04) is built on the five places a bar where the two guitars strike together (Harry: "The band agreeing; it builds"). It has a shape now: two bars as it was; then the china joins the snare on the two places where the guitars make a chord with each other; and in its last bar (2:02) the guitars too play only where they agree: five stabs from the whole band with rests between, a unison, a tritone, a minor third, a fifth, and a last one where the right guitar, being ahead, is already on the F the song goes to next. Then the right guitar starts to slide again.

**The clock that opens the song is a music box (v21).** The song opened on the left guitar and a "pendulum", the kit's ride bell on one and three. Harry turned that pendulum down twice where it was exposed (under the drift: "doesnt work at this tempo on this kit piece"; at the end: "Sounds like a click track") and kept the music boxes that replaced it. Now the opening's clock is the left music box too: tick on the bar line (F), tock on three (the C under it). One clock, on the left, with the left guitar: the instrument that takes the riff when the guitars let go (2:44) and that the song ends on. The ride bell still ticks under the hold on B, which he kept as it is.

**In every slip, the two clocks (v22).** In each of the four slips (0:53, 1:11, 1:46, 2:04) the hat that counted quarters is gone and two music boxes tick in its place: the left one on the song's clock (tick on one, tock on three), the right one written on the same beats but on the right guitar's clock (the track `warp`). As the right guitar slides, the right tick slides with it: in the first slip the two ticks start together and end a sixteenth apart; each later slip starts as far apart as the hold before it and widens by one more. The song's idea, stated by nothing but two clocks, each time the idea happens. The music box is now the song's clock everywhere: the opening, the slips, the drift, the end.

**The bass follows the key (v23).** A mix round, no notes changed (the fault found on Plain Hunt at its v11). The bass's eq was cut to the low F; in the holds on A flat and B its body was pushed down, and on C nearly all of it, which is very likely what Harry heard when he asked for "more bass" there. The eq now moves with the ground in the holds on A flat and B. The hold on C is left as Harry signed it off (3 dB more bass, "Enough"); whether it should have its tone back instead is on the Questions page.

**The clocks chime the echo (v24).** Section round, 1:38-1:46 (window 1:11-1:46). The hold an eighth apart was six bars of its beat, two bars naked (the echo heard), and four bars of the same beat again. Over the last four, two music boxes now play the riff's three hook notes, the left on the song's clock and the right on the right guitar's (`warp`): each note chimes on the right and is answered on the left an eighth later, four octaves over the guitars. The echo is implied, then exposed, then rung. It is the first time the boxes play the riff's notes (they have only ticked until here; at 2:44 they take the whole riff), and they go straight into the next slip's ticks.

**The guitars have a chest, and four guitars against (v25).** Whole-song round; no notes of the two guitars changed. (1) One eq band on each guitar (2 dB at 700 Hz): the voiceless holds were 2.6 to 3.4 dB under the records at 500 Hz-1 kHz. (2) Where the clocks lock against each other (bars 98-122, 3:38-4:31) each clock has a second guitar: `gl2` on the song's clock, `gr2` on the right clock (`warp`), the same riff, a second take through another amp, microphone and cone, inside the main pair. The right double waits for the bar line (the main right guitar's half-bar pickup into the landing is as it was). They leave with the band; the two guitars end the song alone.

**The two guitars trade a bar (v26).** Section round, 0:27-0:31 (window 0:00-0:35). In step, after four bars together, the left guitar plays the riff alone for bar 12 and the right alone for bar 13; then both again into the stop and the voice's first word. The bass and the kit go on underneath. Each guitar is heard by itself before the right one starts to slip (0:53).

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

**The tower (v2).** Where the bells ring alone (0:00, 2:17, the end) they ring over a chant: two low men's voices a fifth apart, F and C, the mouth moving slowly between "o" and "u", with a bowed horsehair drone on the low F as their floor. A gong is struck twice: when the first extent comes round (2:17) and on the last chord (4:52). The bowed bass and the synth pad the album's other two songs use have left this one.

**The second extent starts on the bass (v3).** For its first eight rows (bars 63-66, until the row and the bar line meet again) the guitars rest: the bass, the kick, the snare and the bell carry the row, and the four guitars come in on the crash. All through the second extent the bass is two basses: the one it had for the weight, and over it a bass through a folding fuzz for the teeth.

**The climb (v4).** Over the last third of the second extent (bars 93-108, on C) a lead guitar plays the row's own notes the other way and slowly: from the ground up, C5 Db5 Eb5 Gb5 G5 Bb5, two bars to a note, then the octave C6 held for the last three bars. The band's row falls sixteen notes a bar; the lead climbs once and reaches the top as the extent comes round and the band lands on F. The song's first lead. For the last four bars the snare is on every beat.

**The row becomes a riff (v5).** The bells have weights, and keep them wherever they stand in the row. The treble is LONG (open, ringing: two sixteenths in the first extent, three in the second); the tenor is REPEATED (two muted chugs, then three: a gallop); the four between are single muted sixteenths.

| extent | a row | rounds as played | against the bar |
|---|---|---|---|
| first (Plain Bob) | 8 sixteenths | Eb- C B Ab Gb F F | half a bar: every row starts on a beat, and the long note walks through the sixteenths between |
| second (Grandsire) | 10 sixteenths | Eb-- C B Ab Gb F F F | turns against it: the row and the bar line meet every fifth bar |

The ringers' rule is untouched: the same 240 rows in the same order. 120 bpm (it was 96), so a row takes about the time it took. The landing is rung as the band first rang rounds (the first extent's row, on F).

**The form since v5** (bars, 0-indexed; 2 s a bar; the table above is v1-v4's):

| bars | time | what |
|---|---|---|
| 0-4 | 0:00 | the bells alone ring rounds over the chant |
| 4-8 | 0:08 | the band's rounds, eight times |
| 8-68 | 0:16 | the first extent: on F, on Ab (0:56), on B (1:36) |
| 68-76 | 2:16 | it has come round: the chord, the gong, the bells over the chant |
| 76-151 | 2:32 | the second extent: the bass alone for five bars, the guitars at 2:42; on Ab (3:22), on C (4:12); the lead climbs from 4:18 |
| 151-159 | 5:02 | the landing: rounds on F, sixteen times, the bells over the band |
| 159-162 | 5:18 | one chord, the gong; the tenor tolls three times |

**The method is heard (v6).** A LEAD is ten rows, and in each one the treble walks out to the back of the row and home again; the last two rows of every lead have it leading, so the long note is first in the riff twice running. The band now plays that shape.

| what | where in a lead | what the band does | when |
|---|---|---|---|
| HOME (a plain lead end) | rows 9 and 10 | a crash on each of the two long notes; the kit no longer crashes by the bar count | first cycle: every five bars (0:24, 0:34, 0:44; 1:04 ...); second cycle: every six and a quarter, so each falls a beat later in the bar (2:42, 3:07, 3:32, 3:57, 4:22, 4:47) |
| THE CALL (a bob or a single) | rows 9 and 10 of a called lead | a unison break: every note open and loud, the kick with every note, and the kit stops its beat and rings the row (crash = treble, four toms high to low = the four bells between, snare = the tenor's chugs); then the band is back on a crash | first cycle: the last bar of each third (0:54, 1:34, 2:14); second cycle: the middle and the end of each third (2:54, 3:19, 3:44, 4:09, 4:34, 4:59 into the landing) |
| THE HUNT LAID BARE | the first lead on A flat, in both cycles | the guitars play only the long note and the low chugs; the bass keeps the four notes between | 0:56-1:06 and 3:22-3:34 |

The bare lead is in both cycles on purpose: with it in the first only, the scorer heard the second cycle as less of a return of the first (returns 0.224 of sections, under its floor of 0.25); in both, 0.354 on both seeds, and it cuts the second cycle's thirds where the first's are cut.

**The riff in harmony (v7).** The second cycle's stretch on A flat now has three states, a break between each: the riff laid bare (3:22), the whole riff (3:34), and from 3:47 the riff with a SECOND VOICE: two more guitars (a third amp, `mark`) play it an octave up and a third above, two steps up the riff's own six-note scale (F takes A flat, G flat takes B, A flat takes C, B takes E flat, C takes F, E flat takes G flat), in the riff's rhythm. At the break at 4:09 they join the unison an octave up; when the key moves to C (4:12) they stop, and the high register is the lead's. The first cycle has no harmony: it is the second's.

**The last stretch has its own rig (v8).** From where the key moves to C and the lead begins to climb (4:12) to the landing, the second pair of guitars is another rig: a `gojira` amp through the engine's 1x12 (the first pair stays on the 5150 and the modern 4x12, and keeps the weight). At the landing the four come back: the return is a return of the rig too. The new colour is where the music is new, on purpose: through the whole second cycle it made that cycle less of a return of the first (the scorer's returning share 0.34 -> 0.25).

**The snare hunts (v9).** The first cycle had no event of its own at its end (the second has the lead's climb). For its last two leads (1:56-2:14) the snare leaves the backbeat and follows the long note: one stroke to each riff, exactly where the treble is. Bar by bar through a lead it falls on sixteenths 1 and 10, 3 and 12, 4 and 11, 2 and 9, then 0 and 8: it slides out to the back of the riff and comes home on beats one and three, with the two crashes that mark home. The china's eighths and the kick keep the bar. The song's name, played on the snare.

**Harry's answers (v10).** He answered eight Plain Hunt cards (15 Nov, 02:35-02:40). KEPT: the bells ("Ominous: keep them"), the riff ("A riff now: go on"), the form ("Shape: keep all three"), the hunting snare ("Pulling against the beat: keep it"), the last stretch's rig ("Bite: keep it"). MENDED:
- the chant ("dont hear chamts"): it was two held notes, a pad. Now the two voices SING A LINE, a note to each row the bells ring, stepping round the low F (F, G flat, A flat), the upper voice a fifth over the lower throughout; and 4 dB louder. Under the last tolls each bell is answered two beats later.
- the bass alone at 2:32 ("Too long alone"): four rows, not eight (2.5 bars for 5); the guitars come in on a crash at 2:37.
- the harmony guitars at 3:47 ("Keep it, louder"): 3 dB up.

**The bass follows the key (v11).** A mix round, no notes changed. The bass's eq was cut to the low F; on A flat, B and C its fundamental climbed into the eq's lift and its body and growl were pushed down. The eq's three low bands now move with the ground, so the bass keeps on B and C the shape it has on F.

**The harmony, first heard (v12).** Section round, 1:26-1:36. The harmony guitars (a third and an octave over the riff), which Harry kept in the second cycle ("Keep it, louder"), now make a first short appearance in the first: the last lead of the stretch on A flat, four bars, and the break after it an octave up. It is where the second cycle has its long one (eleven bars, after its own break), so the second is the first grown, as the bare riff is in both. Tried first and dropped: the stretch assembled a pair of guitars at a time (ten thin bars after five bare ones; and through this cabinet the two amps differ by less than 1.5 dB in any band).

**The bell in the hunt (v13).** Section round, 2:40-3:12 (and on to 3:19). The second extent is Grandsire, where TWO bells hunt: the treble and one more, and a call puts a different bell into the hunt. From the second lead of the F stretch (row 10, 2:44) the bell in the hunt is heard: its note is left open on the guitars and struck on that bell's own tom (the toms the calls are rung on). Each row has two accents that walk through it against each other. After the call at 2:55 it is another note and another tom: the third bell (B, the second tom) for the second (C, the first tom).

**The climb is tremolo-picked (v14).** Palette round. The lead's climb over the last stretch (4:18-5:02) was seven notes held three bars each; it is now the same seven notes picked on every sixteenth, with the kick, on a drier lead (`lead-slap`), harder as it climbs.

**The treble is a treble, and in Grandsire two bells ring (v15).** Palette round. (1) In the band the bell that rings the treble's place in each row is its own instrument, `treble`: the church bell with its hum (the octave under its note) taken down; the tower's bells (opening, middle, landing) are untouched. (2) In the second cycle the bell in the hunt rings too, softer, a third to a fifth under the treble: two bells walk through each row against each other, and at every call the lower one changes its note (leads 0-1 the second bell, C over the ground; 2-3 the third, B; 4-5 the fourth, A flat; 6-7 the third; 8-9 the second; 10-11 the fourth). The first cycle has one hunting bell and one bell ringing; the second has two and two.

**The landing lands (v16).** Palette round. On the landing (bars 151-159, 5:02) all six guitars play rounds: the first cycle's doubles (gl2/gr2) and the second cycle's (jl/jr, the small cabinet) together for the first time. And the lead's climb has its last note: one stroke of the top C on the landing's first beat, let ring (the tremolo stopped a sixteenth short before).

**The harmony opens (v17).** Section round, 3:59-4:09 (window 3:44-4:16). The second cycle's harmony guitars play the first of their two leads in thirds (rows 60-69, as before) and the second in sixths (rows 70-77: four steps up the riff's six-note scale: F takes C, G flat takes E flat, A flat takes F, B takes G flat, C takes A flat, E flat takes B), then the call in unison an octave up, the key change, and the lead's climb.

## t4 Running Total (chirper-zero)

Opened by Harry on 15 Nov about 02:42 GMT: "we can do fourth track same climber". The album's fourth kind of long cycle: a SUM.

**The idea.** One riff, two bars of sixteenths (thirty-two places), never simply played but added up: its first place; its first two; its first three; each statement from the top and one place longer. The n-th statement begins after 1 + 2 + ... + (n-1) sixteenths (the triangular numbers), so against a kit that keeps four in a bar the riff's head lands somewhere new every time. The arithmetic closes: 1 + ... + 31 = 496 sixteenths = 31 bars exactly, and + 32 = 528 = 33 bars. So the first statement after the very first to begin on a bar line is the first WHOLE one.

**The riff** (o = the open low F, accented; c = a muted chug; a note name = a hook note; - = held; r = rest):

    o c c Ab - c B - c c r Gb c C - c | o c Eb - c c B Ab c r c Gb - c c C

**The form (v1, the skeleton).** 116 bpm, 131 bars, 4:31.

| bars | time | what |
|---|---|---|
| 0-33 | 0:00 | THE BUILD: statements 1 to 32 from the top. A marimba counts the first eight alone (an abacus); one guitar with bass and kick (0:05); the second guitar (0:18); the doubles (0:39); the first whole statement begins on the bar line at 1:04 |
| 33-49 | 1:08 | THE TOTAL: the whole riff eight times, on F then on A flat (1:25) |
| 49-82 | 1:41 | THE BACK-BUILD, on B: the same sum from the other end (the last place, the last two, ...). The marimba alone; the bass and kick join (1:59); the band (2:20) |
| 82-98 | 2:50 | THE TOTAL again: on C, then home on F (3:06) |
| 98-129 | 3:23 | THE MELT: the riff loses its first place each time; the band thins; the marimba counts the last eight down alone (4:22) |
| 129-131 | 4:27 | one chord |

**Its own colour.** A marimba (`modal-marimba`, a rosewood bar): wood, where Odd Sympathy has a music box and Plain Hunt has bells.

**The total has a tune (v2).** The riff has nine notes that are not the low string: A flat, B, G flat, C, then E flat, B, A flat, G flat, C: the album's hook. In the riff they pass in a sixteenth or two. When the first total moves up to A flat (1:25) a lead guitar plays only those nine, each held until the next, each starting exactly where the riff strikes it: the tune that was inside the riff, drawn out over the band. (The second total does not have it yet.)

**The second count is said quietly (v3).** The riff is added up twice, and both times the band came in a third of the way through and stayed. Now the second sum (from the riff's END, bars 49-82, on B) is the song's quiet middle, and it is staged like a sum: the marimba counts eight statements alone; a clean guitar says them with it from the ninth (`ct-glass`, left, an octave over the riff, its low notes short and its hook notes ringing); a second clean guitar from the seventeenth (`ct-clean`, right); the bass and kick come back at the twenty-fifth, on the accents and hook notes only; the band comes in for the last four statements (the 29th, 2:33, on a crash). The hat keeps time; no snare until the band. The low end is gone for forty seconds.

**The bass follows the key (v3).** The fault found on Plain Hunt at its v11: the bass's eq was cut to the low F. Its three bands fitted to the ground now follow it (A flat, B, C).

**The tune is added up too (v4).** Section round, the second total (2:50-3:23). The riff was a sum; now its tune is one. Over the second total the lead plays the riff's hook notes as the riff strikes them, but only the first two in the first statement (the second held); one more each statement. Eight statements and nine notes: the tune is whole exactly once, in the last statement, at home on F, as the melt begins. On C it is an octave under, so it rises as it comes home. The kit is in half time on C and takes the backbeat when the key comes home.

**The china counts (v5).** Wherever the riff is being added up or taken apart (the build from its seventeenth statement, the last statements of the second count, the melt) the china strikes where each statement STARTS, with the kick and the open string, and a hat keeps the time. The strokes come further apart as the statements grow and closer as they melt: the kit plays the sum. In the two totals the china rides the bar as before, so the cymbal alone says whether the riff is being counted or is whole.

**The riff whole has its own rig (v6).** Palette round. In the two totals, and on the last chord, the second pair of guitars is Common Time's wall rig (in its form whose rests are rests); wherever the riff is being counted it is the tight pair as before. So the guitars say what the china says: counted, the riff is tight; whole, it is a wall.

**The tune melts too (v7).** Section round, the melt's first half minute (3:18-3:51), and on to where the guitars thin. The riff was added up and so was its tune; the riff is taken apart and now so is the tune. Through the melt the lead goes on playing the riff's hook notes where the riff strikes them, and as the riff loses its front the tune loses its first note: nine notes for four statements, eight from 3:38, seven from 3:48, six from 4:00, five at 4:07. It stops where the second pair of guitars does (4:09), and the marimba, which comes in there, carries what is left down to the last note, C. The lead's fader sinks 5 dB through it.

**The knock (v8).** Palette round: the part the song lacked. A woodblock knocks once where every statement starts, in the passages where the china does not: the build's statements 1-16 (0:00-0:16), the back-build's 1-28 (1:41-2:30), the melt's last eight (4:22-4:27). In the back-build and the melt each statement starts on a different place of the riff, so until now nothing said "again". Because the statements are 1, 2, 3 ... sixteenths long the knocks are a figure of their own: close together and soft at the start of a count, slowing by arithmetic (a ball bouncing, backwards); and at the end of the song they close up again and run into the last chord.

**The count has mids, and the total on C is clearer (v9).** Whole-song round; no notes changed. The four tight guitars (the riff being counted: the build, the band's return in the back-build, the melt) get 2.5 dB at 700 Hz, where those stretches read hollow against the records. The wall pair's low-mid cut is 3 dB deeper while the total is on C (bars 82-90), the muddiest stretch.

**The total arrives (v10).** Whole-song round. The count is said by two guitars to its last statement, both times (the build, and the band's return in the back-build); the riff whole is the first time there are four. Before, the second pair of tight guitars joined eight statements before the end, and the total was no louder than the count before it. The tight doubles (`gl2`/`gr2`) now play only in the melt (bars 98-121).

**The snare counts too (v11).** Section round, 0:52-1:04 (window 0:33-1:06) and its mirror at 2:34-2:45. For the last three statements before the riff is whole (29, 30 and 31 places long) the snare leaves the backbeat and strikes the riff's hook notes with the guitars: kick on the chugs, snare on the hooks, china on the heads, the hat alone keeping the bar. The thirty-second statement begins on the bar line and the backbeat comes back with it; two bars later, the four guitars.

**The bass grows teeth (v12).** Palette round. From the build's statement 25 (bar 18.75, 0:39) to the total, and from the back-build's statement 29 (2:34) to the second total, a fuzz bass (`teeth`: `bass-fuzz`, the folding fuzz, high-passed at 500 Hz) doubles the bass's notes. It comes in where the second pair of guitars used to (v10 took them out so that the riff whole would arrive): the count grows at 0:39 again, without becoming four guitars.

**The band thins as the riff does (v13).** Section round, 3:48 (window 3:18-3:51). In the melt the second pair of guitars leaves at statement 24 (bar 110.25), where the kit goes to half time, not at statement 16: four guitars (3:23), two under the melting tune (3:48), the marimba and no tune (4:08), the marimba alone (4:22), the chord.

## t5 False Summit (chirper-zero)

Harry, 15 Nov about 12:38: "true djent, but that leverages audio illusions throughout mainly risers/shpehers but in djent style, really make it a clear illlusory song, all about the illusions". 100 bpm, F, 108 bars, 4:24.

A false summit is the top you can see from below that is not the top. The piece is built on the two illusions of endless motion, and THE BAND plays them (they are not a pad behind the band). Its long cycle is one that never completes.

**The stair (a Shepard scale on guitars).** A line climbs the album's six notes (F, G flat, A flat, B, C, E flat), six notes to the bar on the bar's 3 3 3 3 2 2, an octave every bar, for ever, and is never higher. Four guitars a side play it an octave apart (F1 to E5). Each climbs through all four octaves, and its fader is a bell over where it is: nothing at the bottom, full two octaves up (F3), nothing at the top, where it drops back to the bottom unheard. Three faders a third apart on such a bell always add to the same power, so every bar is the same bar and every bar starts higher than the last. Under it the low string chugs sixteenths (F, F, A flat, E flat, a bar each), open where the line's notes fall, the kick on those six.

**The turn (a Risset rhythm on guitars).** One bar of the low F (`occoccoc` in eighths: 3 3 2) at three speeds an octave of speed apart, all speeding up together, each doubling over four bars while the fastest fades out and the slowest fades in: faster and faster, never faster. The speed rises in a STRAIGHT LINE, not the usual curve, and that closes the arithmetic: in four bars the three play 3, 6 and 12 bars of the riff, so at every fourth bar line all three and the kit are together, and inside the cycle a chug falls on every bar line (the speeds there are 5:4, 3:2, 7:4 of the kit's). The three are always exactly 1 : 2 : 4, so they share one grid: it is one riff, not three. The snare, the china and the bass keep four in a bar.

**The descent.** The stair downwards and all of it: the whole riff, chugs and all, a step of the scale lower every bar on the four guitars a side (and two basses an octave apart on their own bell), under an endless falling rumble (the library's `shepard-fall`). A tuning that keeps dropping.

**The pole.** A breath: one chord through a filter that climbs for ever (`barberpole`), the line at half speed on the Shepard tone, and a bass that is only its second to sixth harmonics (`phantom-bass`): the ear supplies the note.

**Both.** Pitch and speed rise together, as a tape speeding up does: each guitar climbs an octave of the scale while it doubles its speed. An endless riser (`fx-riser-endless`) swells over the last eight bars and stops dead.

**The summit.** A bar of nothing, then the stair's first four bars exactly (the same notes on the same guitars at the same tempo), and one chord. After four minutes of climbing the band is where it started.

| bars | | |
|---|---|---|
| 0-8 | the foot | the stair alone on a Shepard tone (the plain form of the illusion first), then the guitars take it up |
| 8-32 | the stair | the band; half time, then the backbeat from bar 20 |
| 32-48 | the turn | four cycles |
| 48-72 | the descent | four octaves down |
| 72-84 | the pole | the riser comes in at bar 80 |
| 84-100 | both | four cycles; the riser from bar 92 |
| 100-108 | the summit | silence, the stair's first bars, one chord |

Form as arithmetic: every section's start is computed from its length (`FOOT`, `RISE`, `TIME`, `FALL`, `POLE`, `BOTH`, `STOP`, `HOME`, `END`), the cycle from `CYCLE`, the bells from `VOICES` and `ROLES`.

**The joins are risers (v2).** Harry asked for "mainly risers/shpehers but in djent style". Three sections now hand over on a RUN: the eight guitars pick a semitone to the sixteenth on the same bell, so the run climbs four thirds of an octave a bar and is never higher. Two bars each: out of the stair into the turn (bars 30-32, rising; it ends on C and the turn lands on F), out of the descent into the pole (70-72, falling), out of the pole into both (82-84, rising, under the riser that never arrives). Under the two rising ones the snare doubles its speed into the bar line.

**One cabinet a side (v2).** chirp-eco's `tools/endless.py` read v1: the stair held inside a bar but the eight guitars repeated every FOUR bars, not every bar (each had its own cone and pan, so which speaker held which octave came round), and the turn's last two cycles were 1.6 to 2 dB over its first two. The four on a side now share one cone and one place. The turn and both now read "it holds".

**The tick (v2).** In the pole the hat's quarters are a tick that speeds up for ever: the engine's own `risset` on a kit track (it works on a drum: no amp to flatten the copies' fades). The plain form of the turn, alone, as the foot is the plain form of the stair.

**The bass keeps the bar (v2).** Under the turn and under both the bass strikes every beat (it held one long note a bar, and a long note of this bass is all 120-250 Hz).

**The stair has a tune (v3).** The line was the scale straight up: the plain form, right for the first eight bars with the band, and not a tune. From bar 16 it is a FIGURE: up two steps of the scale, back one, up two, back one, each bar starting three steps above the last: F A-flat G-flat B A-flat C | B E-flat C F E-flat G-flat. Two bars, ending an octave above where it began and beginning again there: it climbs an octave every two bars and is never higher. Same eight guitars, same bell, same six places in the bar. The kit takes the backbeat where it comes in. The first bars again at the end are the scale, as at the start.

**The lead comes down (v4).** Section round, the stair's last six bars before the run (0:57-1:12). A lead guitar comes in over the tune and does the one thing nothing else in the song does: it really moves. Down the scale, a note to the half bar, two octaves (F5 to F3), landing on the low F exactly where the guitars' run begins. In those six bars the tune under it climbs three octaves and is no higher; the lead falls two and is two octaves lower. The one honest line shows the stair up for what it is.

**The fill that never lands (v5).** Palette round. A drummer's fill goes round the toms from the high one to the floor tom and stops, because the kit has no lower drum. This kit now has: a set of toms struck three at a time an octave apart under the guitars' bell, so a fill goes on down and the drum is never lower. Each octave of the descent ends on one (eight strokes into bar 54, twelve into 60, a whole bar into 66, down the scale onto the riff's F), and under the guitars' falling run (bars 70-72) the toms fall with it for two bars, a semitone a stroke. The fill into the descent (bar 47) is still the kit's four real toms, high to low to the snare: the one that lands.

**The riser is a guitar (v6).** Palette round. The last climb (both) swelled into the stop on a synth riser, the one thing in the song that was not played. Now the riser is the lead guitar, three of them an octave apart under the bell, playing the song's own stair steeper and steeper: four bars of the tune (an octave every two bars), two of the plain scale (an octave a bar), two of the run (a semitone a sixteenth), and the stop. Eight and a half octaves up in eight bars, and where it began. At 0:57 the lead was the one honest line; at the end it has caught the illusion too. The synth stays under it, 8 dB down.

**The turn, heard naked (v7).** Section round, the turn's second half (1:26-1:55). The turn now has a shape over its four cycles: two with the kit and the bass holding the bar under the chug; the THIRD (bars 40-44, 1:36-1:46) with the snare, the china and the bass gone on a crash, so the chug is alone with its kick, speeding up; the fourth with the kit back harder than it left (the snare on the backbeat, the china in eighths), into the fill and the descent.

**The stair in harmony (v8).** Section round, 0:28-0:57 (and on to the run at 1:12). From the tune's third statement (bar 20, 0:48) the right side's four guitars take it two steps of the scale higher: a third or a fourth over the left on every note (F with A flat, G flat with B, A flat with C, B with E flat, C with F, E flat with G flat). Both lines are stairs: each side is still four guitars an octave apart under its own bell. The stair now gathers every four bars: the tune (16), its harmony (20), the lead coming down through both (24), the run (30).

**The fall gets steeper (v9).** Section round, 2:24-2:52. The descent falls faster and faster and is still never lower: a step of the scale a bar to bar 60 (as it was), then two steps a bar (bars 60-66, an octave in three bars), three (66-68), and six (68-70): a step on every accent of the riff, an octave a bar, the first minute's stair upside down. Then the run, as before; the fall now reaches it on F, the run's first note. The steps change on the riff's accents. The first two changes of speed come out of the tom fills that never land.

**The seam in the fall, and the kit steepens (v10).** Whole-song round on the descent (1:55-2:52). (1) The bass's eq no longer follows the ground through the fall: it stands on F while the notes pass through it. It had leapt up ten semitones on the second step of every octave (E flat), which could be read as the fall coming round. (2) The kit changes gear where the fall does: half time to bar 60; the backbeat from 60 (two steps a bar); the china in eighths from 66 (three); the snare on every beat from 68 (six); then the toms' fall. A crash at each change.

**The band carries the stair alone (v11).** Whole-song round. The Shepard tone that states the illusion at the foot no longer stays on under the band: it sounds alone (bars 0-4), the guitars take the stair up (4-8), and when the band comes in (bar 8, 0:19) it is gone; the same at the summit (bars 101-105). It still sounds in the pole. Through the stair (bars 8-32) the illusion is the eight guitars' alone.

**The pole's line is on guitars (v12).** Palette round. In the quiet middle (bars 72-82, 2:53-3:17) the stair's line, at half an octave a bar, is on the three lead guitars an octave apart under the bell (`slow_leads()`), where it was on the Shepard tone. The tone now sounds only in the foot (bars 0-8).

## t6 Carrying Capacity (chirper-zero)

Harry, 16 Nov about 12:33: "make it unique". Source: `src/chirpers10-t6.py` (its first page is the full account).

**The idea: one rule and one dial; no riff was written.** Every half bar the rule `x <- r * x * (1 - x)` is applied once, and the number it gives (0 to 1) is the half bar:
- `floor(7x)` of its six places are struck, filling in the order 0, 3, 2, 5, 1, 4 (the two beats, their pick-ups, the rest);
- one of the struck places is the accent (which one: how far x is through its seventh); the rest are muted chugs on the open low E;
- the accent's pitch is rung `floor(16x)` of sixteen rungs: two octaves of the half-whole scale on E (E F G Ab Bb B Db D). From the octave up it is a fifth, not a single note.
- under 1/7 the half bar is empty.

**The form is the dial r** (bars are 0-indexed; a bar is two half bars, 1.74 s):

| bars | time | r | what the rule does |
|---|---|---|---|
| 0-8 | 0:00 | 1.5 rising to 2.8 | growth: nothing, single low notes, then the shuffle assembles |
| 8-16 | 0:14 | 2.8 to 2.98 | one: the same half bar every time (`0.0A.0`: a shuffle with its accent on the back beat) |
| 16-24 | 0:28 | 3.2, then 3.4 | two: two half bars alternate |
| 24-32 | 0:42 | 3.5 | four: a two-bar riff |
| 32-40 | 0:56 | 3.555 | eight: the two-bar riff, differently the second time |
| 40-50 | 1:10 | 3.6 rising to 3.7 | it stops repeating |
| 50-60 | 1:27 | 3.7402 | a window: it locks on FIVE half bars (two and a half bars), four times round |
| 60-68 | 1:44 | 3.8 | it lets go again |
| 68-77 | 1:58 | 3.8365 | a window: THREE half bars, after three half bars of finding it |
| 77-83 | 2:14 | 3.845 | the three doubles: six |
| 83-99 | 2:24 | 3.995 | the whole range: screams, holes of up to three half bars (the 808 boom falls through them), climbs |
| 99-111 | 2:52 | 3.5, 3.2, 2.8 | the dial comes down: four, two, one (each for four bars; the rule needs most of that to settle) |
| 111-113 | 3:13 | 1.0 | three single low notes, each lower, and none |

It is one orbit: x starts at 0.02 and is never reset. The two windows' settings are found by the generator (`lock`): the setting inside the window from which the orbit, arriving as it does, locks soonest.

**Who plays it.** Guitars, bass and the machine's kick play the half bar together. The machine's hat keeps the beat (four in a bar, opened before each new setting); its snare is on two and four where the riff repeats or runs wild, and on three only in the windows. The lead (`nes-pulse-lead`, a chip's pulse) has NO notes in the song: its track is the engine's own `gen: logistic`, one system for each dial setting, started from the orbit's own number there; it plays each half bar's rung, three octaves up. The generator was checked against the engine: 171 notes, none different.

**Unlike the other five** (what chirp-eco measured they share): triplets (twelve-eight written as four-four) at 138 where they are straight sixteenths at 100 to 126; on E in the half-whole scale where they sit on F and C; a drum machine where they have one kit and a stick; a part the engine composes.

**v1 is the skeleton**: the whole dial, played bare, on the record's guitars and bass.
