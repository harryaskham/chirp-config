#!/usr/bin/env python3
"""Ring True (Escapement, track 4). Clicky minimal techno, 125 BPM, B flat (five notes: B flat C D F G), 184 bars (5:53).

THE RULE. Six struck things, every one a physical model or noise, play ONE two-bar cell from the first bar to the
last. Not a stroke is added, moved or taken away once a thing has come in. What changes is how long each thing is
allowed to RING, and nothing else: a number from 0 (damped at once: a click) to 1 (let go: a note).
  the weight   a bass drum: a felt beater on a skin (the `drum` layer)             B flat 1
  the wood     a small bar (the `modal` layer, the marimba's modes)                the tune
  the metal    a steel bar (`modal`, the glockenspiel's modes), the off-beats      the tune's top
  the skin     a kettledrum head (`modal`, the kettle's modes)                     three low notes
  the string   a plucked string under a palm (`pluck`)                             the bass
  the air      a burst of noise in a resonator tuned to the note                   two and four
Every click is a note that was stopped too soon to be heard as one. The form lets them go one at a time, so the tune
that was in the clicks from bar 1 is heard, and then stops them again; the last sixteen bars are the first cell
once more, and the question for the ear is whether the tune can still be heard in it. In the very last bar
everything is let go at once (LAST): the answer, ringing into the silence.
A thing is LET GO slowly (over a section, bar by bar) and STOPPED quickly (over QUICK bars: a hand laid on it).

v2 (26 Nov), five switches, each `--without-…` (all five off is v1 byte for byte):
  PLATE  a seventh thing, and the one that RINGS FALSE: a small plate (`modal`, the plate's dense inharmonic modes) on
         the second sixteenth of every beat, so that with the weight on the beat, the metal on the off-beat and the
         wood on the fourth sixteenth the cell runs in sixteenths across four materials. Stopped it is the bright
         tick this family lacked; it comes in with the air, last of the family. It is the last to be let go
         (through the section with no weight), and let go it is a wash, never a note; it is choked in two bars
         with the string and the weight.
  BOOM   the weight becomes a thing that can ring true: the felt thud as it was, and under it a kettle's head on
         the same B flat whose ring time the stroke gives. Stopped: a thud. Let go: a drum that holds its note.
  ROOM   a stopped thing is dry; a thing let go is heard in a hall, in proportion to its ring (a second copy of
         each ringing stroke sent to the hall only, 20 log10(ring) dB under ROOM_DEPTH).
  TOLL   in the last bar before each new thing is let go, the weight itself is let go for that one bar: four
         strokes that hold their note, then a thud again. Nothing is added: it is the same four strokes.
  HUSH   in the last bar before the weight is lifted, a hand is laid on everything else: one bar of the whole
         family stopped dead under the weight's toll, and on the next one they are all let go.

v28 (28 Nov), THE ELEVENTH THING IS SHAKEN. Four switches (`--without-shaken`, `-doubles`, `-swirls`, `-walks`;
all four off is v27 byte for byte). By band against the album this song was 3.7 to 6.3 dB short from 5.7 to
9.2 kHz: ten things, and none of them a hiss.
  SHAKEN   seven things are struck, one is sung, one scraped, one plucked. The eleventh is shaken: a gourd of
           dry seeds (`rt-seeds`: noise from 4.5 to 11 kHz; the seeds do not arrive together, so its front is
           3 ms and not a click's). A shake is two sounds: the seeds thrown against the far wall, and falling
           back against the near one, softer. Where there is no weight (bars 97-112) it keeps the time the
           weight left: a shake a beat, thrown on the beat, back on the off-beat. Like the rasp it rests where
           a thing is listened to alone (bars 113-116, the weight), and it is put down on bar 129, where the
           first hands go on.
  DOUBLES  when the weight is let go the hand is free to shake twice as fast: from bar 117 a shake an eighth:
           thrown on every eighth, back on the sixteenths between.
  SWIRLS   it is let go as the others are: the more the family rings, the longer a few seeds run on round
           the shell after the throw (the note is held; the patch's sustain is 14 dB under its front).
  WALKS    the comb's tongue to follow (the wood's, v27) walks across the stereo as it walks through the bar:
           in the first place it is on the left, in the last on the right, a place a bar, and back.

v27 (28 Nov), THE COMB RINGS THE CHANGES. Four switches (`--without-changes`, `-courses`, `-treble`, `-clear`;
all four off is v26 byte for byte).
  CHANGES  for fourteen bars at the peak the comb played its seven tongues in one order, the order the things
           are let go: the same bar fourteen times. Seven things that ring in a fixed order are what bell
           ringers call ROUNDS, and what they do next is ring the changes. The plainest way is the plain
           hunt: every bar each tongue changes places with a neighbour, by turns the pairs counted from the
           first place and the pairs counted from the second: 1234567 2143657 2416375 4261735 ... 7654321
           (the tune backwards, bar 124) ... 1325476, and rounds again. On seven that is fourteen rows, and
           the comb has its seven tongues for fourteen bars (117 to 130): it comes round on bar 131, where
           the first hands go on and the five tongues that are left ring rounds. The rhythm does not change:
           the places are SPREAD's; only which tongue is plucked in each place.
  COURSES  wherever the comb has grown by a tongue it rings the changes on those it has, timed to be back
           in rounds on the run's last bar (the comb rests after each): on two, bars 53 to 64 (four rows a
           course: rounds for four bars, then two courses); on three, bars 69 to 80 (six rows: rounds for
           six bars, then one course); on five, bars 85 to 95 (ten rows: one course, and rounds on bar 95);
           on six, bars 97 to 112 (twelve rows: rounds for four bars, then one course). After the peak, as
           the things are stopped, it is rounds to the end.
  TREBLE   the wood's tongue, the first of rounds, is the one to follow: in a hunt it goes from the first
           place to the last, a place a bar, lies there for two bars and comes back. It is plucked 3 dB
           harder wherever it is not first.
  CLEAR    read in the finished song place by place, the comb's notes in five of its 24 places were under
           the music without it both at the stroke (the top of its first 60 ms, 150 to 550 Hz) and in the
           ring (80 to 300 ms after it): the second of three, the fourth of five, the third and the last of
           six, the third of seven. Each is written up by the lesser of the two shortfalls, 4 dB at most.
The comb's own words are mended too: its second mode is a tick on the note's front, 20 dB down in 60 ms, not
a tenth of a second.

v26 (28 Nov), THE TENTH THING IS PLUCKED: LETTING GO IS HOW IT IS PLAYED. Three switches (`--without-comb`,
`-spread`, `-follows`; all three off is v25 byte for byte).
  COMB     seven things are struck, one is sung and one is scraped. The tenth is plucked: a comb of steel
           tongues clamped at one end, as in a thumb piano or a music box (`rt-tine`: a plain tone, the
           clamped bar's second mode 6.27 times over it for an instant, and the nail). It is the one thing
           here that cannot be struck or stopped: a tongue is bent and LET GO, which is what this song is
           about. It has a tongue for each thing, in the order they are let go: the wood B flat 3, the metal
           F4, the string D4, the skin C4, the air G4, the plate B flat 4, the weight F3; and in every bar
           it plays the tongues of the things that ring (the ninth thing's count, sung): one note a bar from
           bar 37, two from 53, three from 69, five from 85, six with no weight, all seven at the peak: the
           weight's low F last, leading to the next bar's B flat. Then they are stopped one by one and the
           tune loses its notes: five, two, one, and the wood's alone as the wood closes. It rests where a
           thing is listened to alone, in the hush, and while everything is tapped. It is the song's tune:
           233 to 466 Hz, where nothing else is while the things ring.
  SPREAD   the bar's notes are spread as evenly as that many can be over sixteen sixteenths (the i-th of n
           16 i / n sixteenths after the first, rounded down): 0 | 0 8 | 0 5 10 | 0 3 6 9 12 | 0 2 5 8 10 13 |
           0 2 4 6 9 11 13: the rhythm is made again each time a thing is let go or stopped. The first is
           on sixteenth 6, the emptiest place in the bar where the comb sounds (read in the finished v25),
           so a long phrase ends over the bar line: the weight's low F is on sixteenth 3 of the next bar. (Without: each
           tongue keeps the place it has when all seven play.)
  FOLLOWS  a tongue is plucked as hard as its thing rings: 9 dB down for a thing that is stopped dead, none
           for one that rings whole: a new tongue comes in softly and grows, and the wood's goes out with
           the wood.

v25 (28 Nov), THE NINTH THING IS SCRAPED, AND IT COUNTS THE OTHERS. Three switches (`--without-rasp`, `-tally`,
`-zip`; all three off is v24 byte for byte).
  RASP   seven things are struck and one is sung. The ninth is scraped: a notched stick (`rt-rasp`: a notch is
         a very small dry bar, six milliseconds, with grit on it; nothing in it rings, so it can be neither
         let go nor stopped). A stroke on it is a ROW of clicks, a sixty-fourth apart (30 ms: the only thing in the
         song that is not on a sixteenth), drawn so that the last falls on beat 3 of the bar, where nothing
         but the weight is. It plays from the family's first bar to the bar before the hands come off, and
         rests wherever a thing is listened to alone.
  TALLY  the row has a notch for every thing that is ringing in that bar (a ring of a quarter or more): none
         among the taps (the stick's own tap is all there is), one when the wood is let go, two with the
         metal, three with the string, five with the skin and the air, six with the plate while there is no
         weight, seven at the peak: and back, five, two, one, none, as they are stopped. The more things ring
         the harder it is scraped: a dB a notch on the whole row. In the bar before
         each new thing the weight tolls, and the row is already one longer. Where everything rings and no
         click is left, the row of dry clicks is at its longest: it is the one thing the hall cannot blur.
  ZIP    the row climbs to its last click: each notch a step of the five notes under the next (the stick is
         scraped towards its thin end), so a long row is heard as longer and as rising: seven notches begin
         on Bb5 and end on D7.

v24 (28 Nov), THE EIGHTH THING IS NOT STRUCK. Three switches (`--without-glass`, `-rub`, `-four`; all three
off is v23 byte for byte).
  GLASS  seven things are struck, ring when a hand lets them go and stop when it holds them. The eighth is the
         other way round: a glass, sung by a finger going round its rim: it sounds only while the hand is ON it
         and stops when it is let go (`rt-glass`: a sine and a twin 4 cents over, as a glass's two near modes
         beat, and its second partial 2.32 times up; half a second to speak, a second to stop). So it sings
         where the others are stopped: one held note a section through the wind-down, a step of the home chord
         up each time a hand goes on something else (B flat 3 from bar 129, D4 from 137, F4 from 145, B flat 4
         while the wood closes, D5 over the taps, when every hand is on: bars 169 to 176), and on bar 177,
         where the hands begin to come off one a bar and each thing rings, the finger comes off first and the
         glass stops. It is the first sound in the song that does not die away: it lasts as long as the finger
         is on it.
  RUB    the finger takes a beat and a half to come round, and the glass's level rocks 6 dB with it: two turns
         to three beats, so the swell falls on a beat, then between two, and meets the bar line every third
         bar. (Once a beat and 3 dB, the first build's, could not be told from what this master does to a held
         note at every drum stroke: a 6 dB dip.)
  FOUR   v23 read the plate's traded strokes (bars 117 to 128) as 8.0 dB over the rest on beat 2 and 4.3 on
         beat 4: the strokes on beat 4 are 3 dB up.

v23 (27 Nov), THE PAIR SLOWS AS THE OTHERS ARE STOPPED, AND THE PIPE ENDS AS A PIPE DOES. Two switches
(`--without-slows`, `-fall`; both off is v22 byte for byte).
  SLOWS  v21's second metal bar came nearer in three steps (one wave a beat, an eighth, a sixteenth) and then
         stayed a sixteenth apart for 32 bars, to the bar the hand goes on. Now it goes back the way it came
         while the others are stopped: bars 137 to 140 one wave an eighth, bars 141 to 144 one wave a beat, and
         on bar 145 the hand is on the metal and there is one bar. The flutter is the peak's and leaves with it.
  FALL   v22 gave the pipe the plate's cell: seven even strokes on one note, twelve bars long: 42 F5s and no
         other note. The plate got the pipe's fall (F7 F7 F7 D7); the pipe had none. Now the pipe ends the
         plate's cell as a pipe ends its own: the seventh stroke falls a third (D5). A trade of rhythm in which
         each keeps the end of its own tune; and in the telling (bars 79 and 80) too.

v22 (27 Nov), ALL SIX TRADE, AND THE HALL HEARS BOTH BARS. Three switches (`--without-third`, `-foretold`,
`-hallpair`; all off is v21 byte for byte).
  THIRD     v20 had two pairs trade cells at the peak (the wood and the metal from bar 121, the string and the
            skin from bar 125); the air and the plate, the family's two that are neither struck bars nor
            stretched things, kept their own. Now they trade first, from bar 117: the pipe plays the plate's
            cell (seven even strokes on one note, two octaves down: F5) and the plate plays the pipe's (four
            strokes, the last a third lower: F7 F7 F7 D7). So the peak is the whole family changing hands, a
            pair every four bars, and on bar 129 each has its own again. The plate's four are 4 dB up: two of
            them fall on the bass drum, and with seven strokes become four the first build's peak was 2 to 3 dB
            poorer above 6 kHz.
  FORETOLD  and it is told once before, stopped, as the other two are (bars 31-32, 63-64): in bars 79 and 80
            the pipe taps the plate's cell and the plate the pipe's; on bar 81 the air is let go and has its own.
  HALLPAIR  v21's second metal bar was struck in the room only. The hall's copy of the metal (its own track:
            each ringing stroke 20 log10(ring) dB under) was still ONE bar, and in the finished song only the
            first dip of the pair's breath could be read: the hall filled the rest. Now the hall is sent both
            bars, each 6 dB under the one it had: the hall breathes with the pair.

v21 (27 Nov), THE METAL IS A PAIR, TUNED APART. Three switches (`--without-twin`, `-quicken`, `-told`; all off is
v20 byte for byte). The song is called Ring True and nothing in it has ever rung false. Bronze is not played that
way where it is played most: the metal bars of a gamelan come in pairs, one tuned a few waves a second over the
other on purpose, so that struck together their ring breathes. The tuner sets the breath's rate. Here it is the
song's own: the gap between the two bars, in waves a second, is the tempo's.
  TWIN     wherever the metal is let go (a ring of TWIN['ring'] s or more) a second bar is struck with it, tuned
           125 x 4 / 60 = 8.33 Hz OVER it: the two are in step at the stroke, against each other a thirty-second
           later (the ring is gone: not turned down: cancelled), in step again on the next sixteenth: the ring
           ticks sixteenths, by tuning alone: no gate, no motor. 8.33 Hz is a tenth of a semitone at these notes
           (F6: 10 cents): one note that shimmers, not two. Each bar is struck 6 dB under the old one, so the
           stroke's first instant is the old stroke's. Same place (a pair apart in space would beat only in
           the room, and not at all on headphones). The disc under the bars (v17) turns over both.
           THE BARS MUST RING TRUE FOR IT. The first build struck the second bar with the song's own metal and
           the breath came out anywhere from 5 to 12 a second: this engine's struck bar sounds 2 cents under to
           5 over its written note, differently at every stroke (its `vary`: one bar on F6 read 1395.4 to
           1400.6 Hz over eight strokes), and two layers in one patch are drawn apart as well. With `vary: 0`
           the same eight read 1397.5 +- 0.3. So with the pair the metal's patch is TWIN['patch'] (rt-true:
           rt-motor with no wander): every stroke of the metal is on its note, and its hall's copy with it.
  QUICKEN  the pair is not that far apart from the start: when the metal is first let go (bars 49-64) the gap
           is a quarter of that, one wave a BEAT (2.08 Hz: the ring goes out on the beat after the stroke and
           is back on the next off-beat: what the disc does, done by the second bar); with no weight (bars
           97-112) one wave an EIGHTH (4.17 Hz); from the peak on (bars 113-144) a SIXTEENTH. The breath
           doubles twice. Left out, the gap is a sixteenth everywhere.
  TOLD     v20's --next: the second trade (the string and the skin, bars 125-128) is told once before as
           well, stopped, in the last cell before the string is let go (bars 63-64), as the first was before
           the wood was (bars 31-32).

v20 (27 Nov), THE THINGS TRADE CELLS, AND THE HEAD GOES SLACK. Three switches (`--without-trade`, `-slack`,
`-hint`; all off is v19 byte for byte). Line 309 says of the cell "It never changes", and for 5:53 it had not: nineteen rounds
were all about how the things ring. What a thing IS, its notes or its sound, had never been put to the ear.
  TRADE  in the second half of the peak (bars 121-128, everything let go) the things play each other's cells,
         one pair at a time: from bar 121 the wood plays the metal's (its off-beats, an octave down) and the
         metal the wood's tune (an octave up); from bar 125 the string plays the skin's five strokes and the
         skin the string's eight. The same notes at the same instants: the sounds have moved. At bar 129,
         where the stopping begins, each has its own again. (The first build traded both pairs at bar 121.)
         The metal's disc is not moved: it was struck where the disc is open; on the wood's instants it is
         struck a sixteenth later, as the disc shuts.
  HINT   the trade is told once, small, two minutes before: in the family's last cell (bars 31-32, everything
         still stopped) the metal taps the wood's tune and the wood the metal's off-beats; on bar 33 the wood
         is let go and rings the tune itself, alone: a call on the wrong thing, then the answer on the right one.
  SLACK  the weight has been let go since bar 113; in the peak's last three bars its head goes slack: a step
         down the five notes each bar (G1, F1, D1), and home to B flat 1 on bar 129's one. Alone, the slack
         drum read 0.7, 0.4 and 1.8 dB under the tight one (the kettle's modes are weaker lower down): it is
         given 0.5, 0.5 and 2 dB. The hand on the
         weight (bars 137-138) tightens the head a step and two; this is the same head the other way. 38 Hz
         was the song's shortest band and nothing was written there: D1 is 36.7 Hz.

v19 (27 Nov), THE PIPE IS FLUTTER-TONGUED, AND THE DRUM HAS ITS WEIGHT BACK. Two switches (`--without-tongue`,
`-heft`; both off is v18 byte for byte).
  TONGUE   v18 tried to flutter the air's breath in its patch and found that an LFO does not turn a noise layer's
           level. This is the player's way: the tongue rolls (flutter-tonguing, frullato), about 25 times a second:
           a tremolo on the pipe's own track, a third of a sixteenth long (so every stroke, all of them on a beat,
           meets it at the same place in its turn), TONGUE['depth'] deep, for the sixteen bars with no weight (97 to
           112), where everything is let go and the pipe is most heard. Those strokes move to a track of their
           own (air-tongue) with the pipe's patch, place and room; the strings nobody plays still hear them.
           The breath is then quieter on average, so it has TONGUE['db'] dB. The first build (0.7 deep, 2 dB) read
           3.7 dB up and down alone and 2.0 in the finished song, where it read 1.1 with no tongue at all: too
           little. This is 0.85 deep and 4 dB (5.0 alone).
  HEFT     v18's disc under the weight cost the low band what the ring lost: 1.2 to 2.4 dB under 120 Hz where the
           drum rings longest, 0.3 to 0.8 dB under 100 Hz against the album. The head's level under the disc is
           HEFT['db'] dB up: open (on the beat) it is that much over the old drum's head, shut (off the beat)
           12 dB under that: the turn-taking is kept and the ring's energy is about the old drum's.

v18 (27 Nov), THE RINGS TAKE TURNS. One switch on (`--without-disc`; off is v17 byte for byte) and one built,
benched and left off (`--with-flutter`). v17 gave the metal a vibraphone's motor: its ring shuts on the beat and
opens on the off-beat it is struck on. Nothing is added here either: one more ring is turned.
  DISC     the same disc is under the weight. The weight is struck ON the beat, so its head's ring (up to three
           seconds, let go) is open on the beat and DISC['db'] * 2 dB down on the off-beat: where the metal is struck
           and its ring is open. The two rings take turns: the drum's boom on the beat, the bar's ring between; each
           is out of the other's stroke's way. The felt thud is not turned (only the head's layer), and a stopped
           stroke is as it was. Patch rt-drum-disc. Bench, one stroke let go, alone: 11 to 12 dB under the old ring
           240 and 720 ms after the stroke, level with it at 480 and 960 ms; the same highest sample. It costs the
           low band what the metal's motor cost the metal: the ring is quieter on average.
  FLUTTER  (off) the air's breath fluttered three to the beat, as a flute player's tongue does it (patch rt-flutter:
           an LFO a third of a beat long on the level of the breath's two noise layers). It does not flutter: on
           the bench the breath came out 0.9 dB LOUDER and moved 0.5 dB at 6.25 Hz where 3 was written (at 20
           written: 9 dB louder, 2 dB moved). The same LFO on the metal's modal layer does exactly what is written.
           Left off until a breath can be turned some other way.

v17 (27 Nov), THE METAL HAS A MOTOR. One more switch (`--without-motor`; off is v16 byte for byte).
  MOTOR  the steel bar is a vibraphone's now: under it a disc turns in its resonator, once a beat, shut ON the beat
         and open on the off-beat, where the metal is struck. So a stroke is as loud as it was, its ring is MOTOR
         ['db'] * 2 dB down half a beat later (on the beat, under the weight), back up on the next off-beat, and
         down again: the ring keeps the four by itself, and gets out of the big drum's way. A stopped stroke is as
         it was (in its 12 ms the disc has turned a fortieth of the way: 0.1 dB); only what RINGS is turned, which
         is this song's rule: nothing is added, the ring says more as it is let go. In the section with no weight
         (bars 97 to 112) the four is still heard, in the metal. The patch is rt-motor: rt-metal with a level that
         a sine a beat long moves (it starts again with each stroke, at its top). Two rounds on the bench (v16's
         notes) looked for this in a doublet (a twin bar a beat apart in Hz): the engine gives every modal voice
         its own few cents, so a pair warbles at 0 to 2.8 Hz, never the same twice; a motor is exact.

v16 (27 Nov), THE HALL HAS A FLOOR. One more switch (`--without-floor`; off is v15 byte for byte).
  FLOOR  v15 sent each thing to the hall in the bar its hand goes on, and three of the seven got nothing from
         it: the string and the skin, whose notes are under the hall's 300 Hz high-pass (0.4 dB each), and the
         big drum, which has no hall at all. There is a second room now, under the first: `floor`, a hall of
         1.6 s that keeps what the other throws away (90 Hz to 1.5 kHz). In the bar its hand goes on (bar 173
         the big drum, 174 the string, 176 the skin) each of the three is heard in it as well, and nowhere
         else: so all seven hands are heard going on by a room, the high things above and the low ones below.

v15 (27 Nov), THE HALL HEARS THE HAND GO ON. One more switch (`--without-heard`; off is v14 byte for byte).
  HEARD  v14 brought each thing forward for the bar its hand goes on, by level, and the master took two
         of the lifts back (the plate's and the pipe's: a lift on a small stroke just after a loud one is
         not delivered). Level was the wrong tool: a click is its highest sample, and the master owns
         those. What the master does not own is the time BETWEEN strokes. Since v5 a stopped thing is
         still heard in its hall (the -kept tracks: 'the hall remembers'). Now the hall hears each hand
         go on: in the bar a thing's hand goes on, its strokes are sent to its remembered hall as well
         (bar 171 the metal, 172 the plate, 174 the string, 175 the pipe, 176 the skin; the wood and the
         weight have no such hall and need none). The last section is all taps, dry: for one bar each,
         one thing has a hall round it with the hand's own sound in it, and its tail (2.4 s) runs under
         the next thing's bar. So the mirror is heard as five halls, one after another, each a colour,
         before the hands come off. The plate's 4 dB of v14 is taken back with it (it did nothing but
         make the master work).

v14 (27 Nov), EACH STEPS FORWARD FOR ITS BAR. Two more switches (`--without-turn`, `-aside`; both off is v13
byte for byte).
  TURN   v13's mirror was seven bars a side on paper and three by ear: measured in the finished song, only
         the wood, the metal and the weight moved their own band as their hand went on (5.3, 2.4, 1.3 dB);
         the plate, the pipe, the string and the skin moved it 0.4 dB or less. They are 11 to 23 dB under
         the mix in the last section, where everything is stopped: a change of note in a thing that is not
         heard is not heard. Now each thing steps forward for the bar its hand goes on (TURN's dB on that
         bar's strokes, set on the bench so that its own band reads over the bar before), and steps back:
         the metal 6 dB, the plate 4, the pipe 6. The wood and the weight need none. THE PLATE'S LIFT IS
         NOT DELIVERED: at 9 dB its band read 4.3 dB up raw and 0.1 in the finished song; at 4 dB, under
         the bar's own peaks, 0.0. Its taps fall a sixteenth after the beat, where the master is still
         holding the beat down. It is left at 4 for the raw mix; its cure is room or another sixteenth,
         not level. The string and the
         skin cannot: the touched string's stroke is already the highest sample of its bar (6 dB more put
         it at -1.4 dBFS raw), and the skin already rides its own ceiling (6 dB more gave 1.9).
  ASIDE  so the skin gets room and not level: the big drum stands aside for the bar the hand goes on the
         small one (bar 176, the last bar before the hands come off): the skin's step up is in the band the
         big drum fills. One bar with no bass drum, and then the call.

v13 (27 Nov), HANDS ON, HANDS OFF. Two more switches (`--without-laid`, `-edge`; both off is v12 byte for byte):
  LAID   v12 let each hand come off on one stroke, a bar each, before the last bar. The last section began with
         every hand already down and nothing to say when. Now the hands are heard going ON first, the same
         way round a mirror: in the bars before the call each thing's taps have its hand's sound for one bar,
         in the reverse order (the wood's second mode, the metal's, the drum's head a step tight, the string's
         octave, the pipe an octave down, the skin a step up), and then they come off in the order they went
         on. The bar line between is the mirror: the skin is laid on last and let go first.
  EDGE   the plate was the one thing with no hand. A plate held at its edge is a smaller plate: its strokes
         are an octave up under the hand (the same plate, F8 for F7): in its two stopped bars (137, 138), in
         the bar that shows the hands, and in the mirror, where it takes its place between the weight and the
         metal (it was stopped with the string and the weight). With it the mirror is seven bars a side
         (170 to 176 on, 177 to 183 off); without it six (172 to 177, 178 to 183).

v12 (27 Nov), THE HANDS COME OFF ONE AT A TIME. Two more switches (`--without-equal`, `-call`; both off is v11
byte for byte):
  EQUAL  v11's hand on the wood was one figure on the stroke with two amounts in dB, and a crossfade that is
         linear in dB dips in the middle: through its closing the wood alone stood 1.6, 4.5, 6.3 and 2.5 dB
         under v10's by four bars. Wind Down v11 mended that on the same bar: each of the two layers has its
         own level on the stroke (`expr.note`, `expr.mode`) and the pair is equal-power, so the hand changes
         the bar's colour and not its level, and the second mode is heard from the first bar (12 dB under the
         note) and not only from the middle. Brought home: a new patch name, rt-grip.
  CALL   the song ends with sixteen bars of taps (every hand down) and one bar in which everything is let go.
         Since v10 each hand has a sound of its own, heard while it comes down. Now each is heard once more as
         it comes OFF, a bar each, in the order they were laid on: in bars 178 to 183 the skin, the air, the
         string, the weight, the metal and the wood each let their last stroke of the bar ring (not all the
         way) with the hand's sound still in it: the skin a step up, the pipe an octave down, the string's
         octave, the drum's head a step tight, the metal's and the wood's second modes. Then bar 184: all of
         them, true.

v11 (26 Nov), EVERY THING HAS A HAND, AND THE HANDS ARE SHOWN ONCE BEFORE. v10 gave a hand to four of the seven
things; the weight and the wood were still stopped the old way, and the hands were first heard at bar 129. Four more
switches (`--without-choke`, `-grip`, `-show`, `-fade`; all four off is v10 byte for byte):
  CHOKE  the weight, bars 137-138 (it is stopped over them, with the string): the beater is held against the head,
         which tightens: a step up the five notes, then two (C2, D2 for B flat 1), as the skin did eight bars
         before. The big drum does what the small drum did.
  GRIP   the wood closes over sixteen bars (153-168). It is the last thing let go, and it had no hand: now as it
         closes the hand comes down on the bar's middle, where its first mode moves most and its second not at
         all: bar by bar its note goes (12 dB by the end) and its second mode, two octaves up, is what is left
         (a new patch name, rt-held: the wood and a second bar two octaves up, their levels on the stroke,
         `expr.hand`), until the taps come back on the note.
         FIRST BUILT AS THE STICK WALKING TO THE BAR'S END (the modal layer's `strike`, 0.35 to 1, on the stroke):
         benched, the bar's note did not move at all and its second mode by 1 dB: nothing to hear. Not kept.
  SHOW   the hush (bar 96: everything but the weight stopped dead for one bar, since v2) shows the hands: for
         that one bar the string is touched (its octave), the pipe shut (an octave down), the skin pressed (a step
         up), the metal pinched (its second mode) and the wood gripped (its second mode). Thirty-three bars later each
         comes back for two bars of its own.
  FADE   v10's weak point, measured: the shut pipe's last stroke (bar 130, D4) stood 12 dB over v9's in the same
         place, where the pipe is all but stopped. 6 dB off that stroke.

v10 (26 Nov), A HAND ON EACH. Until now a thing was stopped the same way whatever it was: its ring taken to
nothing over two bars. But a hand laid on a string, a pipe, a drum head and a steel bar does four different things, and
each of them is heard before the thing is quiet. Four more switches (`--without-touch`, `-cap`, `-press`,
`-pinch`; with them off it is v9 byte for byte). No stroke is added, moved or taken away; the hand changes what the stroke finds.
  TOUCH  the string (stopped in bars 137 and 138). A finger laid on the middle of a ringing string stops
         every partial but those with a node there: what is left is its octave, the harmonic. The string's eight
         strokes of those two bars sound an octave up, softer: the bass leaves upward, through its own harmonic.
  CAP    the air (bars 129 and 130). A pipe that is STOPPED is a pipe with its end shut, and it sounds an octave
         LOWER than the open pipe (a quarter wave where there was a half). The air's four strokes of those bars
         are an octave down: F4, F4, F4, D4. The string is stopped upward and the pipe downward.
  PRESS  the skin (bars 129 and 130, with the air). A hand pressed on a drum head tightens it and the note goes
         UP, as a player bends a kettledrum with the heel of the hand. Each stroke finds the head tighter: a step
         up the five notes in the first bar (B flat to C, F to G), two in the second (B flat to D, D to G, F to B
         flat), while its ring goes. Two of the strings nobody plays are C3 and D3, and they hear the skin.
  PINCH  the metal (bars 145 and 146). A steel bar held at its middle loses its first mode, which moves most
         there, and keeps its second, which does not move there at all: 2.76 times the note, an octave and a
         sharp fourth, in nobody's scale. For its last two bars the thing that rang true rings FALSE, as the plate
         always did: eight strokes at 2.76 times their notes (given in Hz), 6 dB down.
Bench (hand.sh, handread.py, raw, each thing alone): the pipe reads 350 Hz for 700 and the string 233 for 116;
the skin 130, 98, 146, 196, 117 Hz for 117, 87, 117, 145, 87. And v9's question, where LONG's extra 450 to 900 Hz
came from: raw, where everything is let go, there is none (the mix +0.01 dB with the second breath, the air
alone -0.05, the strings nobody plays -0.19); the raw mix's highest sample is 0.7 dB lower with it (the air's
fader is 1.4 dB down), so it was the loudness stage giving the whole song more, not the air or the strings.

v9 (26 Nov), THE HAND IS EMPTY. Three more switches (`--without-empty`, `-blow`, `-long`; with them off it is v8
byte for byte):
  EMPTY  since v8 each struck thing drops its stick on the last stroke of its listening, and the stick bounces to
         the one. But the hand went on playing: the thing's later strokes of that bar were struck through its own
         bounces (the wood's sixteenth 14, the metal's 15, the string's 15, the skin's 14 and 16), by a stick that
         was on the floor. They are left out now: once dropped, nothing more of that thing in the bar, and the
         bounces are heard to the one alone.
  BLOW   the air could not be dropped (v8: it is blown, not struck). Its own way of being let go too much: on the
         last stroke of its listening (bar 84, D5) the breath is not taken off and the pipe overblows up its own
         harmonics, a sixteenth each, to the one: D5, then D6, A6, D7 (the second, third and fourth), each a
         little softer. In the same bar the skin's stick is bouncing: the two things let go in that section fall
         and rise into the one together.
  LONG   everything else rings a second or more when it is let go; the air's breath was 0.4 s at any ring. A
         second, slower breath behind the first (it comes up with the ring as the first does, and is nothing
         while the air is stopped) makes a let-go stroke of the air a breath that trails off over most of a
         second (new patch `rt-sigh`: `rt-flue` and the second breath). Longer, not louder: 1.4 dB off its fader.

v8 (26 Nov), two more switches (`--without-drop`, `-skin`; with them off it is v7 byte for byte):
  DROP   until now a thing was stopped or let go. Now the stick is let go too. In the last bar of its listening
         (the four bars each thing is heard alone at the top of its turn) a thing's last stroke that is at least a
         beat before the one is dropped: it bounces. Each bounce comes sooner than the last by the same share
         (three quarters) and is that much softer, as a dropped stick's do, and the last of them would fall on the
         one, where the others come back and play it. The cell does not change: the stroke is the one that was
         always there, and nobody plays the bounces. Five drops: the wood (bar 36), the metal (52), the string
         (68), the skin (84), and the weight (116), a drum bouncing into the bar where everything is let go.
         Not the air: it is blown, and a breath has no stick to drop.
  SKIN   of the five strings nobody plays (v6), C3 and D3 never sounded: the string plays each of those notes
         once a cell, cut short (v7: 26 and 30 dB under the B flat). The skin is a drum tuned to the strings'
         notes (B flat 2, F2, D3); now the two top strings hear the skin as well, and only they do: the three low
         ones are as they were.

v7 (26 Nov), three more switches (`--without-own`, `-close`, `-soft`; with them off it is v6 byte for byte):
  OWN    the strings nobody plays are tuned to the five notes the STRING plays (F2, G2, B flat 2, C3, D3), and
         they could not hear it: they heard only the wood and the air, two and three octaves over them, and so
         sang the wood's notes and nothing under 500 Hz. Now they hear the string as well. When it is let go
         beside them each one sounds its own note, the note that was just plucked, and holds it after the pluck
         has gone: the string has a sustain pedal.
  CLOSE  the wood's closing (bars 153 to 168) was the one stopping with no mark. The strings are let go again for
         it. Nobody stops them: the wood closes, they hear less and less of it, and they go quiet by themselves.
  SOFT   1.4 kHz has stood 7 dB over the album's envelope since v3: the metal let go is 2 dB lower and its
         remembered hall 3 dB lower.

v6 (26 Nov), one more switch that is on (`--without-sympathy`; with it off it is v5 byte for byte) and one that is
off (`--with-wash`):
  SYMPATHY the strings nobody plays. Beside the seven things lie five open strings, tuned to the five notes two
           and three octaves under the wood's (F2, G2, B flat 2, C3, D3). Nothing strikes them, so the rule stands: not a
           stroke is added. They sound only because something near them is ringing at one of their own notes
           (each is a loop one period long that returns itself, and it is fed the wood and the air). They are
           things like the others, with a hand on them: let go across the section with no weight, open while the
           weight is let go, stopped in two bars with the skin and the air, and let go again in the last bar.
           When the weight is listened to alone (bars 113 to 116) what is heard round it is the strings dying.
  WASH     (OFF) the weight's listening was the only one nobody answered. The plate, the thing that rings false,
           answers it in its last two bars: a wash behind the toll. It does what it says (by solo the plate is
           all there is above 2 kHz in bars 115 and 116, 18 dB under the weight). Off because with it the scorer
           no longer hears the weight's four bars as something that returns (2 sections of 8 return for 3, under
           its band) and takes 2.2 points, for a sound that faint.

v5 (26 Nov), three more switches (`--without-flue`, `-remember`, `-lift`; with them off it is v4 byte for byte):
  FLUE     the air is blown, not struck. It was three milliseconds of noise in a resonator: let go, the resonator
           sang, which is a struck thing again and the least like its name of the seven. Now there is breath
           behind the puff (new patch `rt-flue`): a second noise that lasts nearly half a second and comes up
           only as the thing is let go, into a resonator a third as sharp. Stopped it is the same puff; let go
           it is a pipe that is blown: the note lasts as long as the breath does, not as long as the pipe rings.
  REMEMBER the room remembers. When a thing is stopped by the hand (the skin and the air, then the string and
           the plate, then the metal) it is a click again, but for the rest of that section the hall it rang in
           is still open round it: the stopped strokes go on being sent there (tracks `-kept`, each at a level
           set by solo, since a click is too short to fill a hall at a note's send). At the next stopping it is dry.
  LIFT     the metal's aftertaste, its one ringing stroke four bars after it is stopped, stood 9.4 dB under the
           mix: 4 dB up.

v4 (26 Nov), three more switches (`--without-answer`, `-even`, `-after`; with them off it is v3 byte for byte):
  ANSWER the listenings were all alike: four bars, a thing alone. Now the things already let go ANSWER the new one
         in the last two of its four bars, let go altogether as it is and 7 dB behind it: the wood is alone (nobody is before it); the metal is answered by the
         wood; the string by the metal and the wood; the skin and the air by all three. Each break is fuller than
         the last, and the fifth is the whole family without the weight (bars 97 to 112), which they have been
         gathering towards. The weight is not answered: it is what the others stand on.
  AFTER  an aftertaste, the foretaste's mirror. Four bars after it has been stopped, each thing gives ONE more
         stroke let go altogether (the last of its bar): the ring remembered, among clicks.
  EVEN   each thing alone at its own level. One number (3 dB down) left the wood alone 1.1 dB OVER the groove
         that came back after it and the others 1.1 to 2.2 under: the wood is now 5.5 down.

v3 (26 Nov), four more switches (`--without-listen`, `-off`, `-fore`, `-note`; with v2's five also off it is v1 byte for byte):
  LISTEN the others stop to listen. For the first four bars of its turn a thing is heard ALONE and let go altogether:
         the wood at bar 33, the metal at 49, the string at 65, the skin and the air together at 81, and at 113,
         after sixteen bars without it, the weight by itself, ringing B flat. Then everything comes back in, and the
         thing goes on being let go among the others. Until now a thing's turn was a slow change under six others.
         Alone it is 3 dB down, so that the others coming back is a step up.
  OFF    the hand comes off. A thing's turn no longer begins stopped and creeps: on the one of its section it is
         let go half way at once (ring 0.5: the wood goes from a 15 ms click to a 120 ms note in one bar), and the
         rest of the way over the sixteen bars. Every section now begins with something heard to change.
  FORE   a foretaste. Eight bars before its turn, each thing gives ONE stroke let go altogether (the last of its
         bar), in the middle of a section where it is otherwise stopped: one ring of a second among clicks, on a count.
  NOTE   the weight's note. In v2 the kettle under the thud rang for 1.2 s at most, so it was 17 dB gone by the
         next beat and 25 dB under its own thud. Let go, it now rings three seconds, the thud gives way (6 dB)
         and the head comes up (6 dB): each stroke lands on the last one's note, and the drum holds B flat.

Form as arithmetic: the sections are a list of lengths (LENGTHS, bars); each thing has a list of (section, ring)
points, a point `(n, r)` meaning ring r at the top of section n and `(n, r, QUICK)` ring r QUICK bars into it; its
ring at any bar is the straight line between them (`ring_at`). A ring r is a ring time `t0 * (t1 / t0) ** r` seconds
(equal steps of r are equal ratios of time), handed to the stroke as `expr.ring`.
"""
import argparse
import json
from math import cos, log10, log2, pi, sin
from pathlib import Path

BPM = 125
BAR, CELL = 16, 32                          # sixteenths in a bar and in the cell
SEC, QUICK, LAST = 16, 2, 1                 # bars: a section in which something is let go; how fast a thing is stopped; let go at the end
LENGTHS = [SEC] * 8 + [SEC // 2] * 3 + [SEC] * 2   # sections 1-8 let go, 9-11 stop (half as long: nothing in them is turning), 12-13
TOP = [sum(LENGTHS[:i]) for i in range(len(LENGTHS) + 1)]   # the bar each section starts on (and the end)
SECTIONS = len(LENGTHS)
BARS = TOP[-1]
OUT = Path(__file__).resolve().parents[3] / 'songs/chirpers11-t4.yaml'

# The cell: (sixteenth of 32, pitch, how hard). It never changes.
STROKES = {
    'weight': [(s, 'Bb1', .95 if s % BAR == 0 else .88) for s in range(0, CELL, 4)],
    'wood':   [(3, 'D5', .8), (7, 'F5', .7), (11, 'G5', .85), (14, 'F5', .65), (19, 'D5', .8), (23, 'C5', .7), (27, 'Bb4', .85), (29, 'C5', .6)],
    'metal':  [(2, 'F6', .7), (6, 'F6', .55), (10, 'G6', .7), (14, 'F6', .55), (18, 'D6', .7), (22, 'F6', .55), (26, 'G6', .7), (30, 'Bb6', .6)],
    'skin':   [(10, 'Bb2', .8), (15, 'F2', .65), (26, 'Bb2', .8), (29, 'D3', .6), (31, 'F2', .7)],
    'string': [(2, 'Bb2', .85), (7, 'Bb2', .7), (11, 'F2', .8), (14, 'G2', .7), (18, 'Bb2', .85), (23, 'Bb2', .7), (27, 'D3', .8), (30, 'C3', .7)],
    'air':    [(4, 'F5', .8), (12, 'F5', .75), (20, 'F5', .8), (28, 'D5', .75)],
}
# Ring time, seconds: (shut, let go).
RING = {'weight': (0.25, 1.10), 'wood': (0.015, 1.00), 'metal': (0.012, 1.20), 'skin': (0.030, 1.20), 'string': (0.030, 1.00), 'air': (0.004, 0.60)}
# Who is in from which bar, and each one's ring at section boundaries (a point per boundary named; straight lines between).
ENTERS = {'weight': 0, 'wood': 0, 'metal': 8, 'string': TOP[1], 'skin': TOP[1], 'air': TOP[1] + 8}
OUT_OF = {'weight': (TOP[6], TOP[7])}       # the seventh section: the weight is lifted
Q = QUICK
SHAPE = {                                    # (section counted from 0, ring[, bars into it])
    'wood':   [(2, 0), (3, 1), (3, .45, Q), (6, .45), (6, 1, Q), (11, 1), (12, 0)],
    'metal':  [(3, 0), (4, 1), (4, .5, Q), (6, .5), (6, 1, Q), (10, 1), (10, 0, Q)],
    'string': [(4, 0), (5, 1), (5, .7, Q), (6, .7), (6, 1, Q), (9, 1), (9, 0, Q)],
    'skin':   [(5, 0), (6, 1), (8, 1), (8, 0, Q)],
    'air':    [(5, 0), (6, .6), (6, 1, Q), (8, 1), (8, 0, Q)],
    'weight': [(7, 0), (8, 1), (9, 1), (9, 0, Q)],
}
NAMES = ['taps', 'the family', 'the wood is let go', 'the metal is let go', 'the string is let go', 'the skin and the air are let go', 'no weight: all let go',
         'the weight is let go', 'the skin and the air are stopped', 'the string and the weight are stopped', 'the metal is stopped', 'the wood closes', 'taps again']
assert len(NAMES) == SECTIONS

long_ring = {'a': '0.2ms', 'd': '0s', 's': 1, 'r': '2.5s', 'curve': 1}
ring = lambda t0: {'value': t0, 'mod': [{'src': 'expr.ring', 'amount': 1}]}
PATCHES = {
    'rt-weight': {'about': 'Ring True: the weight. A bass drum as a thing: a felt beater on a skin, its ring time from the stroke (expr.ring, seconds over 0.25).',
                  'synth': {'layers': [{'type': 'drum', 'beater': 'felt', 'decay': ring(0.25), 'strike': 0.15, 'slap': 0.4, 'sharp': 60}], 'amp': long_ring},
                  'play': {'event_stable': True, 'vel_sens': 0.3}},
    'rt-wood': {'about': 'Ring True: the wood. A small bar (1 : 4 : 10) struck near its middle; its ring time from the stroke (expr.ring, seconds over 0.015).',
                'synth': {'layers': [{'type': 'modal', 'modes': 'bar', 'decay': ring(0.015), 'bright': 0.75, 'strike': 0.35}], 'amp': long_ring},
                'play': {'event_stable': True, 'vel_sens': 0.6}},
    'rt-metal': {'about': 'Ring True: the metal. A steel bar (1 : 2.76 : 5.40 : 8.93); its ring time from the stroke (expr.ring, seconds over 0.012).',
                 'synth': {'layers': [{'type': 'modal', 'modes': 'glock', 'decay': ring(0.012), 'bright': 1.0, 'strike': 0.6}], 'amp': long_ring},
                 'play': {'event_stable': True, 'vel_sens': 0.6}},
    'rt-skin': {'about': 'Ring True: the skin. A kettledrum head (the air in the kettle pulls its modes to 1 : 1.5 : 2 : 2.5, so it sings its note); its ring time from the stroke (expr.ring, seconds over 0.03).',
                'synth': {'layers': [{'type': 'modal', 'modes': 'kettle', 'decay': ring(0.03), 'bright': 0.6, 'strike': 0.4}], 'amp': long_ring},
                'play': {'event_stable': True, 'vel_sens': 0.6}},
    'rt-string': {'about': 'Ring True: the string. A plucked string whose ring time comes from the stroke (expr.ring, seconds over 0.03): a palm on it, lifted.',
                  'synth': {'layers': [{'type': 'pluck', 'decay': ring(0.03), 'bright': 0.5, 'pick': 0.18, 'soft': 0.3}], 'amp': long_ring},
                  'play': {'event_stable': True, 'vel_sens': 0.5}},
    'rt-air': {'gain': '24dB', 'about': 'Ring True: the air. Three milliseconds of noise into a resonator tuned to the note (a band-pass); how long it sings comes from the stroke (expr.ring, on its q).',
               'synth': {'layers': [{'type': 'noise', 'color': 'white', 'level': {'value': '-70dB', 'mod': [{'src': 'env.burst', 'amount': 70}]}}],
                         'env': {'burst': {'a': '0.1ms', 'd': '3ms', 's': 0, 'r': '3ms'}},
                         'filters': [{'kind': 'bp', 'cutoff': 261.63, 'keytrack': 1, 'q': {'value': 0.7, 'mod': [{'src': 'expr.ring', 'amount': 1}]}}],
                         'amp': long_ring},
               'play': {'event_stable': True, 'vel_sens': 0.5}},
}
PATCH = {k: 'rt-' + k for k in STROKES}

# ---- v2: the switches, and what each adds. Nothing above is changed by them.
ON = {'plate': True, 'boom': True, 'room': True, 'toll': True, 'hush': True, 'listen': True, 'off': True, 'fore': True, 'note': True,
      'answer': True, 'even': True, 'after': True, 'flue': True, 'remember': True, 'lift': True, 'sympathy': True, 'wash': False, 'own': True, 'close': True, 'soft': True, 'drop': True, 'skin': True, 'empty': True, 'blow': True, 'long': True, 'touch': True, 'cap': True, 'press': True, 'pinch': True, 'choke': True, 'grip': True, 'show': True, 'fade': True, 'equal': True, 'call': True, 'laid': True, 'edge': True, 'turn': True, 'aside': True, 'heard': True, 'floor': True, 'motor': True, 'disc': True, 'flutter': False, 'tongue': True, 'heft': True, 'trade': True, 'slack': True, 'hint': True, 'twin': True, 'quicken': True, 'told': True, 'third': True, 'foretold': True, 'hallpair': True, 'slows': True, 'fall': True, 'glass': True, 'rub': True, 'four': True, 'rasp': True, 'tally': True, 'zip': True, 'comb': True, 'spread': True, 'follows': True, 'changes': True, 'courses': True, 'treble': True, 'clear': True, 'shaken': True, 'doubles': True, 'swirls': True, 'walks': True}
GOURD = {'patch': 'rt-seeds', 'gain': '-16dB', 'pan': 0.35, 'room': '-14dB', 'bars': (TOP[6], TOP[8]), 'fast': TOP[7], 'pitch': 'C5', 'vel': (0.9, 0.8), 'back': -2, 'len': 0.06, 'swirl': 0.3, 'hard': 5, 'trim': {4: 4, 8: 2, 12: 4}}   # v28: the gourd: patch, fader, place, send; the bars it plays (where there is no weight, and the peak); DOUBLES: the bar from which a shake is an eighth; touch of the throw and of the fall back, and the fall back's dB; a stroke's length (beats); SWIRLS: beats more at full ring; DOUBLES: dB harder at the peak (at one level its throw was 12.2 dB over what was on the bare beats and 3.6 over the peak); dB on a throw by its sixteenth where a shake is a beat (the master left beats 2 and 4 seven dB under beat 1)
GOURD_PATCH = {'about': "Ring True: the gourd (v28), the eleventh thing, the only one that is shaken: dry seeds in a shell. They do not arrive together (a front of 3 ms), rattle on the wall for 30 ms, and a few run on round it for as long as the note is held, 14 dB under. Nothing in it has a note: noise from 4.5 to 11 kHz, most of it near 6.8 kHz.",
               'synth': {'layers': [{'type': 'noise', 'color': 'white'}], 'filters': ['hp cutoff=4500', 'lp cutoff=11000', 'peak cutoff=6800 q=1.2 gain=6dB'], 'amp': {'a': '3ms', 'd': '30ms', 's': 0.2, 'r': '25ms', 'curve': 2}},
               'play': {'event_stable': True, 'vel_sens': 0.6, 'gate': 1}}
WALK = {'pan': 0.6, 'room': '-15.5dB', 'ends': 1.5}   # v28 WALKS: the two tracks the comb's tongue to follow is shared between (pan, left and right), equal power; their send to the room; dB more at the two ends of the walk, none in the middle (at equal power the two sides together, as one speaker hears them, were 2.6 to 3.0 dB under v27 at the ends: half of that is given back)
TRADE = {'to': 128, 'pairs': (('wood', 'metal', 12, 120), ('string', 'skin', 0, 124))}   # v20: the bar (from 0) at which each has its own cell again; the pairs that play each other's: how many semitones the second is over the first, and the bar (from 0) they trade at
TWIN = {'patch': 'rt-true', 'ring': 0.3, 'db': -6, 'gap': 1, 'bars': ((48, 64, 4), (96, 112, 2), (112, 144, 1))}   # v21: the metal's patch while it is a pair (the motor's, with the engine's stroke-to-stroke wander off: another sound, another name); the least ring, s, at which the second bar is struck; dB on each of the two (in step at the stroke they add to the old stroke); sixteenths to one wave of the gap between them where QUICKEN is off; the bars (from 0, to but not with) in which the metal is a pair, and the sixteenths to a wave there with QUICKEN
THIRD = {'pair': ('air', 'plate', 24), 'at': 116, 'told': (78, 80), 'lift': 4}   # v22: (the last: dB on the plate's strokes while it plays the pipe's cell: two of its four fall on the bass drum, and the first build's peak read 2 to 3 dB poorer above 6 kHz, bars 117 to 128) v22: the third pair that trades (how many semitones the second is over the first), the bar (from 0) it trades at, and the bars (from 0, to but not with) in which it is told once before, stopped
GLASS = {'patch': 'rt-glass', 'gain': '-28dB', 'pan': 0.2, 'room': '-14dB', 'notes': ((128, 136, 'Bb3', 0), (136, 144, 'D4', 0), (144, 152, 'F4', 0), (152, 168, 'Bb4', -3), (168, 176, 'D5', -6)), 'early': 0.5, 'vel': 0.7,
         'cents': 4, 'twin': -8, 'partial': (14.57, -20), 'rub': 3, 'rate': '3/8', 'turn': 1.5, 'speak': '500ms', 'stop': '1s'}   # v24: the glass: its patch, fader (bench, raw, 200 to 520 Hz: at -20 dB it stood 1 to 3 dB OVER the whole song in its band and 5 to 8 over the song's middle 100 ms: a lead; at -28 it is under the strokes and over the gaps), place and room; its notes (bars from 0, to but not with; and dB: the fewer the things that ring, the more this master lifts a held note); beats before the next note that the finger moves; touch; the twin's cents and dB; the second partial (semitones, dB); half the rock of the finger's turn (dB), the turn, and the turn in beats (a beat and a half: two turns to three beats. Once a beat and 3 dB, the first build's, was 1.9 dB as delivered UNDER a 6 dB dip this master makes in a held note at every drum stroke: not to be told from it); how long it takes to speak and to stop
COMB = {'patch': 'rt-tine', 'gain': '-14dB', 'pan': 0.0, 'room': '-14dB', 'at': 6, 'tines': {'wood': 'Bb3', 'metal': 'F4', 'string': 'D4', 'skin': 'C4', 'air': 'G4', 'plate': 'Bb4', 'weight': 'F3'},
        'ringing': 0.25, 'vel': 0.85, 'len': 1.0, 'soft': -9,
        'trim': {(1, 0): -6.6, (2, 0): -7.7, (2, 1): -2.3, (3, 0): -7.8, (3, 1): -1.3, (3, 2): 0.5, (5, 0): -6.8, (5, 1): -2.7, (5, 2): 2.4, (5, 3): -2.4, (5, 4): -1.3, (6, 0): -2.8, (6, 1): -4.0, (6, 2): 0.9, (6, 3): -0.6, (6, 4): -8.2, (6, 5): -2.8, (7, 0): -0.9, (7, 1): 0.9, (7, 2): 1.2, (7, 3): 6.1, (7, 4): -0.8, (7, 5): -1.2, (7, 6): -1.0}}   # v26: the comb: its patch, fader, place, room; the sixteenth of the bar its phrase begins on (the emptiest place in the bar from 150 to 550 Hz, read in the finished v25 by sixteenth: -28 to -34 dBFS on sixteenth 6 while the first things ring, -5 to -7 on the weight's four beats: begun on the one, the comb's first note of the bar came out 8 to 11 dB under the weight); a tongue for each thing, in the order they are let go; the ring from which a thing's tongue is plucked; touch and length (beats); FOLLOWS: dB on the tongue of a thing that does not ring at all; dB on a note by (how many in the bar, which of them), SET FROM A FINISHED BUILD, every note read: with none the comb came out -4.9 to -19.9 dBFS from 150 to 550 Hz (12 dB between the means of its 24 places; raw and alone every note is within 2 dB): this master lifts a half-second note most where the bar is emptiest; each place is written to come out at -12 (a cut of more than 4 dB is written 1.3 times as deep: in the build before, such cuts came out a third short)
HUNT = {'treble': 'wood', 'db': 3, 'clear': {(3, 1): 4.0, (5, 3): 3.8, (6, 2): 3.3, (6, 5): 3.7, (7, 2): 1.5}, 'about': "Ring True: the comb (v26; these words v27), the tenth thing, the only one that is plucked: a steel tongue clamped at one end, bent and let go: a plain tone that rings half a second, the clamped bar's second mode (6.27 times the note) as a tick on its front (20 dB down in 60 ms), and the nail's click. It cannot be stopped: it is not played until it is let go."}   # v27: the changes: the tongue to follow and the dB on it wherever it is not first in its bar; CLEAR: dB on a note by (how many in the bar, which place), FROM THE FINISHED BUILD WITH THE CHANGES IN: the places whose notes read under the music without the comb both at the top of their first 60 ms and over 80 to 300 ms after (150 to 550 Hz, the mean over every bar they play in): by the lesser shortfall, 4 dB at most, none under 1.5; the comb's patch's own words, mended (v26 wrote a tenth of a second for the second mode: a level on a layer falls in dB, as a straight line: 68 dB in 200 ms)
COMB_PATCH = {'about': "Ring True: the comb (v26), the tenth thing, the only one that is plucked: a steel tongue clamped at one end, bent and let go: a plain tone, the clamped bar's second mode (6.27 times the note) for a tenth of a second, and the nail's click on its front. It cannot be stopped: it is not played until it is let go.",
              'synth': {'layers': [{'type': 'osc', 'wave': 'sine'},
                                   {'type': 'osc', 'wave': 'sine', 'ratio': 6.27, 'level': {'value': '-80dB', 'mod': [{'src': 'env.ting', 'amount': 68}]}},
                                   {'type': 'noise', 'color': 'white', 'level': {'value': '-80dB', 'mod': [{'src': 'env.nail', 'amount': 62}]}}],
                        'env': {'ting': {'a': '0.1ms', 'd': '200ms', 's': 0, 'r': '30ms'}, 'nail': {'a': '0.1ms', 'd': '1.5ms', 's': 0, 'r': '1.5ms'}},
                        'amp': {'a': '0.5ms', 'd': '450ms', 's': 0, 'r': '90ms'}},
              'play': {'event_stable': True, 'vel_sens': 0.5}}
RASP = {'patch': 'rt-rasp', 'gain': '-12dB', 'notch': -8, 'bare': -6, 'more': 1, 'pan': -0.45, 'room': '-14dB', 'bars': (TOP[1], TOP[12] + 8), 'at': 8, 'gap': 1 / 16, 'ringing': 0.25, 'pitch': 'D7', 'climb': 1, 'vel': (0.5, 0.85), 'len': 0.04, 'plain': 0}   # v25: the rasp: its patch, fader, dB on every notch before the last click, and dB on a last click that has no weight under it (all three from the finished song: at -6 dB and no trims the last click read -10 dBFS with the weight and -3.5 without it, and the notches, between the strokes, -3 to -7: this master lifts a click that falls between the drum's strokes 15.5 dB where one thing rings (9 to 12 at the peak) and one that falls with the drum 8 to 10), dB more on the whole row for each notch in it (TALLY: the more things ring the harder it is scraped: with none, the third build's, the peak's seven notches were 10 to 20 dB under what rings in their band and its last click 4 under), place and room; the bars it plays in (from 0, to but not with); the sixteenth of the bar its row ends on; the gap between notches (beats: a sixty-fourth); the ring at which a thing counts as ringing; the last click's note; steps of the five notes each notch is under the next (ZIP); touch (the first notch, the last click); a click's length (beats); the notches without TALLY
RASP_PATCH = {'about': "Ring True: the rasp (v25): the ninth thing, scraped and not struck: one notch of a notched stick: a very small dry bar (six milliseconds) with two milliseconds of grit on it. Nothing in it rings.",
              'synth': {'layers': [{'type': 'modal', 'modes': 'bar', 'decay': '6ms', 'bright': 0.9, 'strike': 0.8},
                                   {'type': 'noise', 'color': 'white', 'level': {'value': '-70dB', 'mod': [{'src': 'env.burst', 'amount': 52}]}}],
                        'env': {'burst': {'a': '0.1ms', 'd': '2ms', 's': 0, 'r': '2ms'}},
                        'amp': {'a': '0.1ms', 'd': '0s', 's': 1, 'r': '20ms'}},
              'play': {'event_stable': True, 'vel_sens': 0.6}}   # (the first build's notch was noise alone through a narrow band: two milliseconds of it are two or three chances, and the same click read -11 to -23 dBFS from bar to bar: some notches were not there)
FOUR = {'at': 12, 'db': 3}   # v24: the sixteenth of the bar (beat 4) on which the plate's traded strokes are lifted again, and by how much
SLOWS = {'bars': ((136, 140, 2), (140, 144, 4))}   # v23: the bars (from 0, to but not with) in which the metal's pair goes back the way it came, and sixteenths to one wave of the gap there (they stand before TWIN's own spans)
TOLD = {'pair': ('string', 'skin', 0), 'bars': (62, 64)}   # v21: the second pair's trade told once before, stopped: the last cell before the string is let go
HINT = {'pair': ('wood', 'metal', 12), 'bars': (30, 32)}   # v20: the pair that trades once before, stopped; the bars (from 0, to but not with): the last cell before the wood is let go
SLACK = {'from': 125, 'steps': (-1, -2, -3), 'db': (0.5, 0.5, 2)}   # v20: the bar (from 0) at which the weight's head goes slack; steps of the five notes on each bar from there; dB on its strokes there (bench: alone, the slack drum read 0.7, 0.4 and 1.8 dB under the tight one, bar by bar)
TONGUE = {'section': 6, 'rate': '1/48', 'depth': 0.85, 'db': 4}   # v19: the section (from 0) in which the pipe is flutter-tongued; a roll of the tongue (a third of a sixteenth: 25 a second at 125); how deep (0.85: the level falls to 0.15: 16 dB); dB on those strokes (the first build was 0.7 and 2: too little in the finished song)
HEFT = {'db': 3, 'patch': 'rt-drum-heft'}   # v19: dB on the weight's head under its disc; the patch's name with it (another sound, another name)
DISC = {'patch': 'rt-drum-disc', 'db': 6, 'rate': '1/4', 'phase': 0.25}   # v18: the weight's patch with the disc under its head; half the dip, dB; a turn (a beat); where in its turn a stroke begins (0.25: open)
FLUTTER = {'patch': 'rt-flutter', 'db': 3, 'rate': '1/12', 'phase': 0.25}   # v18: the air's patch with a fluttered breath; dB up and down; a flutter (a third of a beat); where it begins (0.25: at its top)
MOTOR = {'patch': 'rt-motor', 'db': 6, 'rate': '1/4', 'phase': 0.25}   # v17: the metal's patch with its motor; half the dip, dB (the ring is twice this down on the beat); a turn of the disc; where in its turn a stroke begins (0.25: open). Bench, one stroke let go, alone: 12 dB down 240 and 720 ms after the stroke, level with the old ring at 0 and 480 ms, the same highest sample; at 9 (18 dB dips) the ring between strokes is 9 dB less on average
FLOOR = {'who': ('weight', 'string', 'skin'), 'reverb': 'reverb kind=hall decay=1.6s mix=1 predelay=20ms', 'hp': 90, 'lp': 1500, 'db': {'weight': -8, 'string': 0, 'skin': 2}}   # v16: the things the low room hears in the bar their hand goes on; the room; what it keeps, Hz; dB beside each one's dry fader into it. Bench, raw: at 0, 6 and 7 the rooms alone stood 3.8, 9.0 and 9.0 dB OVER the dry things from 90 to 300 Hz over their bars and the big drum's bar came up 3.6 dB whole: a boom
HEARD = {'who': ('metal', 'plate', 'string', 'air', 'skin'), 'not': ('plate',), 'db': {'string': -6}}   # v15: the things the hall hears while their hand goes on (those with a remembered hall: KEPT's); those whose TURN lift is taken back with it; dB on a thing's strokes into the hall there (the touched string is an octave up, so more of it is over the hall's 300 Hz: at KEPT's level its hall stood 7.7 dB over the bar between strokes and filled the pipe's band the bar before the pipe's)
ASIDE = {'for': 'skin', 'who': 'weight'}   # v14: the thing whose bar (its hand going on) another rests through; the one that rests
TURN = {'db': {'metal': 6, 'plate': 4, 'air': 6}}   # v14: dB on a thing's strokes in the bar its hand goes on (the mirror's first half): set on the bench, see the note
EDGE = {'switch': 'edge', 'semis': 12, 'db': 0, 'after': 'weight', 'call': 6}   # v13: the plate's hand (as HAND's); the thing it follows in the call; dB on its one stroke there
EQUAL = {'patch': 'rt-grip'}            # v12: the wood's patch with each layer's level on the stroke (expr.note, expr.mode), written as an equal-power pair
CALL = {'order': ('skin', 'air', 'string', 'weight', 'metal', 'wood'), 'ring': 0.6, 'db': {'air': 3, 'string': 6, 'metal': 9}}   # v12: the things whose hands come off, a bar each, before the last bar; how far that one stroke is let go; dB on it.
# Bench (hand3.sh, hand3read.py: each thing alone on that stroke, raw): with nothing added the six read -33.6 (skin) -36.3 (air) -39.9 (string) -30.8 (weight) -46.4 (metal) -35.8 (wood) dBFS over their beat, where the mix reads -28:
# the string 12 and the metal 18 under it (the hand's own -3 and -6 are for bars where the thing plays eight strokes with it, not one). Each brought to within 9 of the mix
# v10: what the hand does to each thing in the bars it is stopped: semitones on every stroke of them, or steps up the five notes bar by bar; dB on those strokes.
HAND = {'string': {'switch': 'touch', 'semis': 12, 'db': -3}, 'air': {'switch': 'cap', 'semis': -12, 'db': 0}, 'skin': {'switch': 'press', 'steps': (1, 2), 'db': 0}, 'metal': {'switch': 'pinch', 'ratio': 2.76, 'db': -6}}
HAND['weight'] = {'switch': 'choke', 'steps': (1, 2), 'db': 0}   # v11: the big drum's head tightens under the beater as the skin's did under the hand
GRIP = {'note': -12, 'mode': 40, 'from': '-40dB', 'semis': 24, 'patch': 'rt-held'}   # v11: dB on the wood's own layer with the hand all the way down; dB on its second mode's layer; that layer's level with no hand; its place above the note; the patch.
# Bench (hand2.sh, hand2read.py: the wood alone, D5, hand 0 to 1 by fifths): at -18 and +34 the stroke read -22.8 -26.4 -29.9 -32.8 -33.2 -28.3 dBFS: 10 dB down in the middle and 5.5 down held, and through its closing the wood alone stood
# 2.4, 6.7, 10.1 and 8.0 dB under v10's by four bars: the hand was a fader. The note taken less far and the second mode brought to the note's own level: a change of colour
SHOW = {'string': -3}                   # v11: dB on a thing's strokes in the bar that shows the hands (bench: the touched string's highest sample stood 3.3 dB over the stopped string's there, and the bar's 1.8 dB over)
FADE = {'air': -6}                      # v11: dB on a stopped thing's last stroke of its stopped bars
SCALE = ('Bb', 'C', 'D', 'F', 'G')
BLOW = {'harmonics': (2, 3, 4), 'db': -4}   # v9: the harmonics of its pipe the air overblows through, a sixteenth each, after the last stroke of its listening; dB on each beside the one before.
# Bench (blow.sh, blowread.py: the air alone from that stroke by sixteenth): at -2 dB a step the four read -18 -19 -18 -20 (the resonator gives a higher note more: its band is wider) and the bar's last beat stood 2 to 3 dB
# OVER the one it runs into (-21): a rise that tops what it leads to. So -4 a step
LONG = {'env': {'a': '120ms', 'd': '2s', 's': 0, 'r': '3s'}, 'db': -6, 'fader': -1.4}   # v9: the second breath: it is still coming up when the stroke ends (a sixteenth is 120 ms) and trails off after it; dB beside the first breath; dB on the air's fader.
# Longer, not louder: with the second breath the air alone read 1.4 dB more where everything is let go (bars 121 to 124: -24.0 for -25.4) and put 0.9 dB on the mix from 450 to 900 Hz, where the air is all but the mix (2 dB under it) and
# the song is already 5 dB over the album. So 1.4 dB off its fader.
# Bench, one let-go stroke alone by 120 ms: with 900 ms to let go it read -15 -27 -45 -55 where v8 reads -15 -37 -57 -59: a quarter of a second, not a second (the level hangs from the envelope by 70 dB, so its first tenth is 7 dB). So 3 s
DROP = {'share': 0.75, 'bounces': 8, 'room': 4, 'not': ('air',)}   # v8: each bounce's gap, and its level, as a share of the one before; how many are heard (the next would be the one); sixteenths before the one that the dropped stroke must leave; what is not struck.
# Bench (drop.sh, dropread.py: the stroke alone with its bounces, by 60 ms to the one): the wood -27 -32 -34 -36 -37 -36 -40 -36 -34 -35; the weight -22 -29 -26 -31 -29 -32 -33 -34: each bounce is softer and they come faster: the wood's buzzes back up towards the one and the others' run out (v8's note said the level holds; it does not).
# The air was dropped too at first, and its stroke by a track of its own read 5 dB under the same stroke on its own track (-23 for -18: the flue's pipe is still sounding from the stroke before, and a second track's pipe is cold): so not the air
SKIN = {'feeds': ('skin',), 'feed': '-28dB', 'strings': ('C3', 'D3')}   # v8: what else two of the strings hear, and how much of it.
# Bench (own.sh, ownread.py: the song with it less the song without, bars 117 and 118): with all five hearing the skin at -32 dB it woke B flat 2 most, then F2 (3 dB under), G2 (4), C3 (8), D3 (20): mostly more of the three that
# sounded already, 15 and 16 dB under the mix from 60 to 250 Hz on top of the 12 and 13 the string wakes. So only the two that did not sound, and 4 dB more of it
OWN = {'feeds': ('string',), 'feed': '-29dB'}   # v7: what else the strings hear, and how much of it.
# Bench (the song with it less the song without, bars 117 and 118): at -36 dB what the string wakes stood 18.1 and 19.8 dB under the mix from 60 to 120 and 120 to 250 Hz (B flat 2 strongest, then G2, F2): there, and nothing. 7 dB more
SOFT = {'ease': {'metal': -2}, 'kept': {'metal': -3}}   # v7: dB on the metal let go, and on its remembered hall
SYMPATHY = {'strings': (('F2', 87.307, 0.3), ('G2', 97.999, 0.0), ('Bb2', 116.541, -0.3), ('C3', 130.813, 0.15), ('D3', 146.832, -0.15)),   # v6: each string's note, Hz and side (a return cannot be shorter than 6 ms, so F and G are an octave under the others)
            'feeds': ('wood', 'air'), 'feed': '-30dB', 'back': 0.985, 'lp': 5000, 'let': -24}   # what they hear and how much of it; what each gives back of itself a period; the low-pass in the loop; the dB their hand starts from.
# Bench (the song with them less the song without): hearing the wood and the air at -20 dB they stood 3.7 and 2.5 dB under the whole mix once the wood was let go beside them (a string that gives back 0.985 answers a held note at its own pitch 36 dB up): 10 dB less
FLUE = {'q': 40, 'breath': {'a': '30ms', 'd': '450ms', 's': 0, 'r': '300ms'}, 'top': -24, 'ease': 0}   # v5: the resonator's q let go (it was 120); the breath; the breath's level let go, dB beside the puff's; dB on the stroke at ring 1
# The breath's level is set under the track's clip. Bench, the stroke let go, level over two seconds and its third harmonic beside its note: top 0 -25.8 (and 10 dB off the stroke took only 1.9 off: it was all clip);
# -12 -28.2, -26.0; -24 -33.1, -32.4; -36 -41.6, -31.9. At -24 it is clean and climbs with the ring: -51.5 -53.6 -43.3 -43.7 -37.6 -33.1 at rings 0, 0.2 … 1 (rt-air: -47.8 -54.8 -40.8 -42.0 -33.7 -44.1).
CAL_FLUE = [0, 0, 0, 0, 0, 0]                # v5: nothing is given back: the flue's highest sample is the clip's at every ring
KEPT = {'air': 7, 'string': 2.5, 'metal': 4, 'skin': 7, 'plate': 11}   # v5: dB over its dry fader at which a stopped thing is still sent to the hall (a track of its own, `-kept`). Set by solo: sent as a let-go stroke is (10 dB under the dry), the halls stood 23 to 38 dB under the mix above 300 Hz, which is nothing; a click is too short to fill a hall.
# At these each hall stands 2.5 to 4 dB over the click it remembers and 11 to 17 dB under the mix (K-weighted, by parts). At 10 and 17 the skin's and the plate's stood 7 and 10 dB over their own clicks: a hall with a tick in it, not a tick with a hall round it
LIFT = {'metal': 4}                          # v5: dB on a thing's aftertaste
ANSWER = 2                                   # v4: the last bars of a listening in which the things already let go answer
ANSWER_DB = -10                              # dB on the answering things: behind the thing they answer (at -6 the answered bars stood 0.6 to 1.4 dB OVER the groove that came back; at -10 level with it, so the weight's return is still the step)
AFTER = SEC // 4                             # v4: bars after it is stopped that a thing gives one more stroke let go
ALONE_OF = {'wood': -5.5}                    # v4 EVEN: dB on a thing alone where ALONE's one number left it over the return
LISTEN = 4                                   # bars at the top of its turn that a thing is heard alone, let go altogether
ALONE = -3                                   # dB on its strokes while it is alone (unhushed the wood alone read 2.4 dB OVER the groove it broke off, and the others' return was a step down)
OFF = 0.5                                    # the share of its ring a thing is given at once, on the one of its turn
FORE = SEC // 2                              # bars before its turn that a thing gives one stroke let go
NOTE = {'ring': (0.04, 3.0), 'thud': -2, 'note': 2, 'from': '-6dB', 'ease': -3.5}   # the head's ring time, seconds (v2: to 1.2: 17 dB gone by the next beat); dB a second of ring on the felt layer and on the head; the head's level stopped; dB at ring 1
PLATE = {'strokes': [(1, 'F7', .6), (5, 'F7', .5), (9, 'F7', .6), (13, 'F7', .5), (17, 'F7', .6), (21, 'F7', .5), (25, 'F7', .6)],
         'ring': (0.010, 1.5), 'enters': ENTERS['air'], 'shape': [(6, 0), (7, 1), (9, 1), (9, 0, Q)], 'ease': -8, 'gain': '-9dB', 'pan': -0.5}
BOOM = {'ring': (0.04, 1.2), 'gain': '-3dB'}
ROOM_DEPTH = -16                             # dB under its dry fader that a thing let go altogether is sent to the hall
TOLLS = [TOP[i] - 1 for i in range(2, 7)]    # the bar before each of sections 3 to 7: the weight is let go for it
HUSH = TOP[6] - 1                            # the bar before the weight is lifted: everything else is stopped for it
ROOM_FROM = 0.05                             # strokes with less ring than this are not sent at all
ROOM_THINGS = ('wood', 'metal', 'skin', 'string', 'air', 'plate')
NEW = {
    'rt-plate': {'about': 'Ring True: the plate, the thing that rings false. A small thin plate (dense inharmonic modes) struck near its edge; its ring time from the stroke (expr.ring, seconds over 0.010). Stopped, a bright tick; let go, a wash and never a note.',
                 'synth': {'layers': [{'type': 'modal', 'modes': 'plate', 'decay': ring(0.010), 'bright': 1.0, 'strike': 0.7}], 'amp': long_ring},
                 'play': {'event_stable': True, 'vel_sens': 0.6}},
    'rt-boom': {'about': "Ring True: the weight as a thing that can ring true. The felt beater's thud on a skin (fixed), and under it a kettledrum head on the same note whose ring time comes from the stroke (expr.ring, seconds over 0.04).",
                'synth': {'layers': [{'type': 'drum', 'beater': 'felt', 'decay': 0.35, 'strike': 0.15, 'slap': 0.4, 'sharp': 60},
                                     {'type': 'modal', 'modes': 'kettle', 'decay': ring(0.04), 'bright': 0.4, 'strike': 0.2, 'level': '-3dB'}], 'amp': long_ring},
                'play': {'event_stable': True, 'vel_sens': 0.3}},
}


def things():
    """The cell's things in order, with the plate when it is on."""
    return list(STROKES) + (['plate'] if ON['plate'] else [])


def drum_patch():
    """rt-boom with the stroke's ring on the two layers' levels as well: the thud gives way to the note."""
    felt, kettle = (dict(x) for x in NEW['rt-boom']['synth']['layers'])
    felt['level'] = {'value': '0dB', 'mod': [{'src': 'expr.ring', 'amount': NOTE['thud']}]}
    kettle['level'] = {'value': NOTE['from'], 'mod': [{'src': 'expr.ring', 'amount': NOTE['note']}]}
    return {'about': "Ring True: the weight whose thud gives way to its note (v3). rt-boom's two layers, a felt thud and a kettledrum head on the same note; the stroke's ring (expr.ring, seconds) sets the head's ring time and also takes the thud down and brings the head up.",
            'synth': {'layers': [felt, kettle], 'amp': NEW['rt-boom']['synth']['amp']}, 'play': NEW['rt-boom']['play']}


def strokes_of(thing):
    return PLATE['strokes'] if thing == 'plate' else STROKES[thing]


def ring_range(thing):
    return PLATE['ring'] if thing == 'plate' else (NOTE['ring'] if ON['note'] else BOOM['ring']) if thing == 'weight' and ON['boom'] else RING[thing]


def enters(thing):
    return PLATE['enters'] if thing == 'plate' else ENTERS[thing]


def up(pitch, semis):
    """A note name some semitones higher."""
    names = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
    n = names.index(pitch[:-1]) + 12 * int(pitch[-1]) + semis
    return f'{names[n % 12]}{n // 12}'


def step(pitch, k):
    """v10: a note name k steps up the five notes."""
    names = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
    scale = sorted(names.index(x) + 12 * o for x in SCALE for o in range(9))
    n = scale[scale.index(names.index(pitch[:-1]) + 12 * int(pitch[-1])) + k]
    return f'{names[n % 12]}{n // 12}'


def hz(pitch):
    """v10: a note name's frequency."""
    names = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
    return 440 * 2 ** ((names.index(pitch[:-1]) + 12 * (int(pitch[-1]) + 1) - 69) / 12)


def hand_of(thing):
    """v13: the thing's hand (HAND's entry; the plate's is EDGE), or None."""
    return EDGE if thing == 'plate' and ON['plate'] else HAND.get(thing)


def order():
    """v13: the things whose hands come off, in order: CALL's, with the plate after the weight when it has a hand."""
    o = list(CALL['order'])
    return o[:o.index(EDGE['after']) + 1] + ['plate'] + o[o.index(EDGE['after']) + 1:] if ON['edge'] and ON['plate'] else o


def laid(thing, bar):
    """v13: is this the bar in which the thing's hand is heard going on (all its taps have the hand's sound)? The call's bars in a mirror at the bar line before it."""
    if not (ON['laid'] and ON['call']) or thing not in order() or (thing != 'wood' and not ON[hand_of(thing)['switch']]) or (thing == 'wood' and not ON['grip']):
        return False
    return bar == BARS - LAST - len(order()) - 1 - order().index(thing)


def stopping(thing):
    """v10: the bars in which a hand stops the thing: from a point where it rings to a point QUICK bars on, in the same section, where it does not."""
    pts = PLATE['shape'] if thing == 'plate' and ON['edge'] else SHAPE.get(thing, [])
    return [TOP[b[0]] + j for a, b in zip(pts, pts[1:]) if len(b) > 2 and b[1] == 0 and a[1] > 0 and a[0] == b[0] for j in range(b[2])]


def hand_on(thing, bar):
    """v10: what the hand does to the thing's strokes in this bar, or None."""
    h = hand_of(thing) if ON['edge'] else HAND.get(thing)
    return h if h and ON[h['switch']] and (bar in stopping(thing) or (shown(bar) and thing != 'weight') or laid(thing, bar)) else None


def shown(bar):
    """v11: is this the bar that shows the hands (the hush)?"""
    return ON['show'] and ON['hush'] and bar == HUSH


def grip(bar):
    """v11: how far the hand is down on the wood's middle (0..1): bar by bar across its closing, and all the way in the bar that shows the hands."""
    if not ON['grip']:
        return 0
    if shown(bar):
        return 1
    return round((bar - TOP[11] + 1) / (TOP[12] - TOP[11]), 4) if TOP[11] <= bar < TOP[12] else 0


def called(thing, bar):
    """v12: is this the bar in which the thing's hand comes off (its last stroke rings with the hand's sound in it)?"""
    if not ON['call'] or thing not in order() or (thing != 'wood' and not ON[hand_of(thing)['switch']]) or (thing == 'wood' and not ON['grip']):
        return False
    return bar == BARS - LAST - len(order()) + order().index(thing)


def blown():
    """v9: (bar, sixteenth of the bar) of the stroke after which the air overblows: its last stroke in the last bar of its listening. None if it has none."""
    pts = SHAPE['air']
    if not (ON['blow'] and ON['listen'] and pts[0][1] == 0):
        return None
    bar = TOP[pts[0][0]] + LISTEN - 1
    mine = [s % BAR for s, _, _ in strokes_of('air') if s // BAR == bar % 2 and s % BAR + len(BLOW['harmonics']) < BAR]
    return (bar, mine[-1]) if mine else None


def flue_patch():
    """rt-air with breath behind the puff: a second noise, half a second long, whose level the stroke's ring brings up."""
    air = PATCHES['rt-air']
    breath = {'type': 'noise', 'color': 'white', 'level': {'value': f"{-130 + FLUE['top']}dB", 'mod': [{'src': 'env.breath', 'amount': 70}, {'src': 'expr.ring', 'amount': round(60 / (FLUE['q'] - 0.7), 3)}]}}
    if ON['long']:                                               # v9: the same breath again, slower: it trails off after the stroke
        sigh = {'type': 'noise', 'color': 'white', 'level': {'value': f"{-130 + FLUE['top'] + LONG['db']}dB", 'mod': [{'src': 'env.sigh', 'amount': 70}, {'src': 'expr.ring', 'amount': round(60 / (FLUE['q'] - 0.7), 3)}]}}
        return {'gain': air['gain'], 'about': "Ring True: the air, blown (v5), and its breath trailing off (v9). rt-air's puff of noise in a resonator tuned to the note; behind it a breath nearly half a second long, and behind that a slower one that goes on for a second after the stroke. The stroke's ring brings both up (60 dB from stopped to let go). The resonator's q goes to 40, not 120, so let go it is breath with a note in it and not a ping.",
                'synth': {**air['synth'], 'layers': air['synth']['layers'] + [breath, sigh], 'env': {**air['synth']['env'], 'breath': FLUE['breath'], 'sigh': LONG['env']}}, 'play': air['play']}
    return {'gain': air['gain'], 'about': "Ring True: the air, blown (v5). rt-air's puff of noise in a resonator tuned to the note, and behind it a breath: a second noise nearly half a second long whose level the stroke's ring brings up (60 dB from stopped to let go). The resonator's q goes to 40, not 120, so let go it is breath with a note in it and not a ping.",
            'synth': {**air['synth'], 'layers': air['synth']['layers'] + [breath], 'env': {**air['synth']['env'], 'breath': FLUE['breath']}}, 'play': air['play']}


def remembered(thing, bar):
    """v5: is the thing, stopped by the hand, still heard in its hall? From the bar it is stopped to the end of that section."""
    last = (PLATE['shape'] if thing == 'plate' else SHAPE[thing])[-1]
    return ON['remember'] and len(last) > 2 and last[1] == 0 and TOP[last[0]] + last[2] <= bar < TOP[last[0] + 1]


def motor_patch(bar):
    """v17 MOTOR: the metal's patch (bar) with a disc turning under it: its one layer's level is MOTOR['db'] under, moved MOTOR['db'] up and down by a sine MOTOR['rate'] long that starts again with every stroke at its top."""
    layer = {**bar['synth']['layers'][0], 'level': {'value': f"-{MOTOR['db']}dB", 'mod': [{'src': 'lfo.motor', 'amount': MOTOR['db']}]}}
    return {**bar, 'about': "Ring True: the metal with its motor (v17). The steel bar of rt-metal over a resonator whose disc turns once a beat: open when the bar is struck (the off-beat), shut on the beat: the ring is " + f"{2 * MOTOR['db']}" + " dB down on every beat and back between. A stopped stroke is as rt-metal's.",
            'synth': {**bar['synth'], 'layers': [layer] + bar['synth']['layers'][1:], 'lfo': {'motor': {'wave': 'sine', 'rate': MOTOR['rate'], 'phase': MOTOR['phase'], 'retrig': True}}}}


def disc_patch(drum):
    """v18 DISC: the weight's patch (drum) with the metal's disc under its head: the head's layer (the second) is DISC['db'] under and moved DISC['db'] up and down by a sine DISC['rate'] long that starts again with every stroke at its top. The thud (the first layer) is not turned."""
    thud, head = drum['synth']['layers'][:2]
    lvl = head['level']
    head = {**head, 'level': {'value': f"{float(lvl['value'][:-2]) - DISC['db'] + (HEFT['db'] if ON['heft'] else 0):g}dB", 'mod': lvl['mod'] + [{'src': 'lfo.motor', 'amount': DISC['db']}]}}
    return {**drum, 'about': "Ring True: the weight with a disc under its head (v18)" + (f", and the head {HEFT['db']} dB up under it (v19): the ring's energy is about rt-drum's" if ON['heft'] else '') + ". rt-drum, and the head's ring is turned once a beat: open on the beat the drum is struck on, " + f"{2 * DISC['db']}" + " dB down on the off-beat. The felt thud is not turned; a stopped stroke is as rt-drum's.",
            'synth': {**drum['synth'], 'layers': [thud, head] + drum['synth']['layers'][2:], 'lfo': {'motor': {'wave': 'sine', 'rate': DISC['rate'], 'phase': DISC['phase'], 'retrig': True}}}}


def flutter_patch(air):
    """v18 FLUTTER: the air's patch (air) with its two breaths (the second and third layers) moved FLUTTER['db'] up and down by a sine FLUTTER['rate'] long that starts again with every stroke. The puff (the first layer) is not fluttered."""
    layers = air['synth']['layers']
    breaths = [{**b, 'level': {**b['level'], 'mod': b['level']['mod'] + [{'src': 'lfo.flutter', 'amount': FLUTTER['db']}]}} for b in layers[1:3]]
    return {**air, 'about': "Ring True: the air with a fluttered breath (v18). rt-sigh, and its two breaths go " + f"{FLUTTER['db']}" + " dB up and down three times a beat, as a flute player's tongue does it. The puff is not fluttered; a stopped stroke has no breath and is as rt-sigh's.",
            'synth': {**air['synth'], 'layers': [layers[0]] + breaths + layers[3:], 'lfo': {'flutter': {'wave': 'sine', 'rate': FLUTTER['rate'], 'phase': FLUTTER['phase'], 'retrig': True}}}}


def cell_of(thing, bar):
    """v20 TRADE: the strokes a thing plays in a bar: its own cell, or in the trading bars its partner's, moved to its own octave."""
    spans = [(*x, TRADE['to']) for x in TRADE['pairs']] * ON['trade'] + [(*HINT['pair'], *HINT['bars'])] * ON['hint'] + [(*TOLD['pair'], *TOLD['bars'])] * ON['told'] + [(*THIRD['pair'], THIRD['at'], TRADE['to'])] * (ON['third'] and ON['trade']) + [(*THIRD['pair'], *THIRD['told'])] * ON['foretold']   # v22 THIRD, FORETOLD: the air and the plate too. v20 HINT: once before, small (v21 TOLD: the second pair too)
    if spans:
        for a, b, semis, at, to in spans:
            if thing in (a, b) and at <= bar < to:
                cell = [(s, up(pitch, semis if thing == b else -semis), vel) for s, pitch, vel in strokes_of(a if thing == b else b)]
                if ON['fall'] and (a, b, semis) == THIRD['pair'] and thing == a:   # v23 FALL: the pipe ends the plate's cell as it ends its own
                    cell[-1] = (cell[-1][0], strokes_of(a)[-1][1], cell[-1][2])
                return cell
    return strokes_of(thing)


def slack(bar, what='steps'):
    """v20 SLACK: how many steps of the five notes the weight's head is from its own note in a bar (0: none); or, what='db', the dB on its strokes there."""
    return SLACK[what][bar - SLACK['from']] if ON['slack'] and 0 <= bar - SLACK['from'] < len(SLACK['steps']) else 0


def patch_of(thing):
    if thing == 'metal' and ON['motor']:
        return TWIN['patch'] if ON['twin'] else MOTOR['patch']   # v21 TWIN: the bars of a pair ring true
    if thing == 'weight' and ON['disc'] and ON['boom'] and ON['note']:
        return HEFT['patch'] if ON['heft'] else DISC['patch']
    if thing == 'air' and ON['flutter'] and ON['flue'] and ON['long']:
        return FLUTTER['patch']
    if thing == 'air' and ON['flue']:
        return 'rt-sigh' if ON['long'] else 'rt-flue'            # v9: with its second breath it is another sound, under another name
    if thing == 'wood' and ON['grip']:
        return EQUAL['patch'] if ON['equal'] else GRIP['patch']
    return 'rt-plate' if thing == 'plate' else ('rt-drum' if ON['note'] else 'rt-boom') if thing == 'weight' and ON['boom'] else PATCH[thing]


def ring_at(thing, bar):
    """The thing's ring (0..1) at a bar: the straight line between its points; flat before the first and after the last."""
    if bar >= BARS - LAST:
        return 1.0
    if thing == 'weight' and ON['toll'] and bar in TOLLS:
        return 1.0
    if thing != 'weight' and ON['hush'] and bar == HUSH:
        return 0.0
    pts = [(TOP[p[0]] + (p[2] if len(p) > 2 else 0), p[1]) for p in (PLATE['shape'] if thing == 'plate' else SHAPE[thing])]
    if ON['off'] and pts[0][1] == 0 and pts[0][0] <= bar < pts[1][0]:      # its turn: half at once, the rest across the section
        (b0, _), (b1, r1) = pts[0], pts[1]
        return r1 * (OFF + (1 - OFF) * (bar - b0) / (b1 - b0))
    if bar <= pts[0][0]:
        return pts[0][1]
    for (b0, r0), (b1, r1) in zip(pts, pts[1:]):
        if b0 <= bar < b1:
            return r0 + (r1 - r0) * (bar - b0) / (b1 - b0)
    return pts[-1][1]


def dropped(thing):
    """v8: (bar, sixteenth of the bar) of the stroke a thing drops: in the last bar of its listening, its last stroke that leaves DROP['room'] sixteenths before the one. None if it has no listening."""
    pts = SHAPE.get(thing)
    if not (ON['drop'] and ON['listen'] and pts and pts[0][1] == 0) or thing in DROP['not']:
        return None
    bar = TOP[pts[0][0]] + LISTEN - 1
    late = [s % BAR for s, _, _ in strokes_of(thing) if s // BAR == bar % 2 and s % BAR <= BAR - DROP['room']]
    return (bar, late[-1]) if late else None


def listened(bar):
    """The things whose turn began within the last LISTEN bars (they are heard alone); empty when nothing is listened to."""
    if not ON['listen']:
        return set()
    return {k for k, pts in SHAPE.items() if pts[0][1] == 0 and TOP[pts[0][0]] <= bar < TOP[pts[0][0]] + LISTEN}


def answering(bar):
    """v4: the things that answer in this bar: in the last ANSWER bars of a listening (never the weight's), every
    thing whose own turn began before it. Empty when nobody answers."""
    out = set()
    if ON['answer']:
        for k in listened(bar):
            top = TOP[SHAPE[k][0][0]]
            if k == 'weight' and ON['wash'] and ON['plate'] and bar >= top + LISTEN - ANSWER:
                out |= {'plate'}                                # v6: the plate answers the toll
            if k != 'weight' and bar >= top + LISTEN - ANSWER:
                out |= {j for j, pts in SHAPE.items() if j != 'weight' and pts[0][1] == 0 and TOP[pts[0][0]] < top}
    return out


def aftertaste(thing):
    """v4: the bar in which a thing, stopped, gives one more let-go stroke (None for the weight, and for a thing that is never stopped)."""
    if thing == 'weight' or not ON['after']:
        return None
    last = (PLATE['shape'] if thing == 'plate' else SHAPE[thing])[-1]
    return TOP[last[0]] + (last[2] if len(last) > 2 else 0) + AFTER if last[1] == 0 else None


def foretaste(thing):
    """The bar in which a thing gives its one let-go stroke before its turn (None for the weight: it has its tolls)."""
    if thing == 'weight':
        return None
    first = (PLATE['shape'] if thing == 'plate' else SHAPE[thing])[0]
    return TOP[first[0]] - FORE


def seconds(thing, r):
    t0, t1 = ring_range(thing)
    return t0 * (t1 / t0) ** r


def air_q(r):
    """The air's resonator: a band-pass's q from a ring, 0.7 (a puff) to 120 (it sings); with FLUE to 40 (the breath sings, not the pipe)."""
    return 0.7 * ((FLUE['q'] if ON['flue'] else 120) / 0.7) ** r


# What the bench reads (--bench, then bread.py): a thing's highest sample at rings 0, 0.2 … 1. A shut string or a
# singing resonator is far quieter than the same stroke let go, so each stroke is given back the difference.
CAL = {'string': [-26.8, -17.3, -13.8, -11.4, -10.0, -10.3], 'air': [-41.2, -34.1, -37.3, -34.5, -36.8, -35.9]}
# And the other way: a bar that rings for a second carries far more than the same bar stopped, at the same highest
# sample. dB taken from a stroke at ring 1 (in proportion below it), so that letting go is a swell and not a flood.
EASE = {'wood': -5, 'metal': -5, 'skin': -3}


def level(thing, r):
    """dB to add to a stroke at ring r so that the thing's highest sample is the same at every ring."""
    db = (PLATE['ease'] if thing == 'plate' else NOTE['ease'] if thing == 'weight' and ON['boom'] and ON['note'] and NOTE['ease'] else FLUE['ease'] if thing == 'air' and ON['flue'] else EASE.get(thing, 0) + (SOFT['ease'].get(thing, 0) if ON['soft'] else 0)) * r
    if thing in CAL:
        cal = CAL_FLUE if thing == 'air' and ON['flue'] else CAL[thing]
        c = [cal[-1] - v for v in cal]
        x = min(r * 5, 4.999)
        i = int(x)
        db += c[i] + (c[i + 1] - c[i]) * (x - i)
    return round(db, 2) if thing in CAL or thing in EASE or thing == 'plate' or (thing == 'weight' and ON['boom'] and ON['note'] and NOTE['ease']) else None


def expr(thing, r):
    return {'ring': round(air_q(r) - 0.7, 4)} if thing == 'air' else {'ring': round(seconds(thing, r) - ring_range(thing)[0], 5)}


def stroke(thing, at, pitch, vel, r):
    n = {'at': at, 'len': 0.25, 'pitch': pitch, 'vel': vel, 'expr': expr(thing, r)}
    if level(thing, r) is not None:
        n['gain'] = f'{level(thing, r)}dB'
    return n


def rasp_count(bar):
    """v25 TALLY: the rasp's notches in a bar: the struck things that are in and ring RASP['ringing'] or more."""
    return sum(1 for k in things() if bar >= enters(k) and not any(a <= bar < b for a, b in [OUT_OF.get(k, (0, 0))]) and ring_at(k, bar) >= RASP['ringing'])


def rasp_bare(bar):
    """v25 RASP: is the row's last click alone on its beat: no weight in the bar (lifted, or standing aside)?"""
    return any(a <= bar < b for a, b in [OUT_OF.get('weight', (0, 0))]) or bool(ON['aside'] and laid(ASIDE['for'], bar))


def rasp_notes():
    """v25 RASP: a row a bar, its last click on RASP['at']; it rests where a thing is listened to alone."""
    out = []
    for bar in range(*RASP['bars']):
        if listened(bar):
            continue
        n = rasp_count(bar) if ON['tally'] else RASP['plain']
        land = bar * 4 + RASP['at'] / 4
        for j in range(n, -1, -1):
            out.append({'at': round(land - j * RASP['gap'], 4), 'len': RASP['len'], 'pitch': step(RASP['pitch'], -RASP['climb'] * j) if ON['zip'] else RASP['pitch'],
                        'vel': round(RASP['vel'][1] - (RASP['vel'][1] - RASP['vel'][0]) * j / max(n, 1), 3),
                        **({'gain': f"{db:g}dB"} if (db := (RASP['notch'] if j else RASP['bare'] if rasp_bare(bar) else 0) + (RASP['more'] * n if ON['tally'] else 0)) else {})})
    return out


def comb_rings(bar):
    """v26 COMB: the things whose tongues are plucked in a bar, in the order they are let go: those that are in and ring (not the weight's toll, not the last bar); none where a thing is listened to alone."""
    if listened(bar) or bar >= BARS - LAST:
        return []
    return [k for k in COMB['tines'] if k in things() and bar >= enters(k) and not any(a <= bar < b for a, b in [OUT_OF.get(k, (0, 0))])
            and not (k == 'weight' and ON['toll'] and bar in TOLLS) and ring_at(k, bar) >= COMB['ringing']]


def comb_runs():
    """v27: the comb's runs: [first bar, the bar after the last, who] for each stretch of bars with the same tongues and no rest between."""
    runs = []
    for bar in range(BARS):
        who = comb_rings(bar)
        if who and runs and runs[-1][2] == who and runs[-1][1] == bar:
            runs[-1][1] = bar + 1
        elif who:
            runs.append([bar, bar + 1, who])
    return runs


def hunt_row(n, r):
    """v27 CHANGES: row r of the plain hunt on n: which of the n (from 0, in rounds' order) is in each place. Row 0 is rounds; at each row every pair changes places, by turns the pairs from the first place and the pairs from the second; rounds again after 2n rows."""
    row = list(range(n))
    for step in range(r):
        for place in range(step % 2, n - 1, 2):
            row[place], row[place + 1] = row[place + 1], row[place]
    return row


def comb_row(bar, runs):
    """v27 CHANGES, COURSES: (a bar's tongues in the order they are plucked, the row's number or None where the comb does not hunt). It hunts in a run that has more tongues than the run before (CHANGES: all of them; COURSES: fewer), from the bar that brings it back to rounds on the run's last bar if the comb rests after it, or on the next run's first bar if it does not."""
    who = comb_rings(bar)
    at = next((x for x, (a, b, _) in enumerate(runs) if a <= bar < b), None)
    if at is None or len(who) < 2 or (at and len(who) <= len(runs[at - 1][2])) or not ON['changes' if len(who) == len(COMB['tines']) else 'courses']:
        return who, None
    a, b, _ = runs[at]
    rests = at + 1 == len(runs) or runs[at + 1][0] != b
    r = max(0, bar - a - (b - a - rests) % (2 * len(who)))
    return [who[x] for x in hunt_row(len(who), r)], r


def comb_patch():
    """v27: the comb's patch, its own words mended where any of v27 is on."""
    return {**COMB_PATCH, 'about': HUNT['about']} if ON['changes'] or ON['courses'] or ON['treble'] or ON['clear'] else COMB_PATCH


def gourd_notes():
    """v28 SHAKEN: a shake a beat (thrown on the beat, back on the off-beat) where there is no weight; it rests where a thing is listened to alone; DOUBLES: a shake an eighth from GOURD['fast']; SWIRLS: the throw held longer the more the family rings."""
    out = []
    for bar in range(*GOURD['bars']):
        if listened(bar):
            continue
        per = 2 if ON['doubles'] and bar >= GOURD['fast'] else 4      # sixteenths in a shake
        run = GOURD['swirl'] * sum(ring_at(k, bar) for k in things()) / len(things()) if ON['swirls'] else 0
        hard = GOURD['hard'] if per == 2 else 0
        for s16 in range(0, BAR, per):
            db = hard + (GOURD['trim'].get(s16, 0) if per == 4 else 0)
            out.append({'at': bar * 4 + s16 / 4, 'len': round(min(GOURD['len'] + run, per / 8 - 0.02), 3), 'pitch': GOURD['pitch'], 'vel': GOURD['vel'][0], **({'gain': f'{db:g}dB'} if db else {})})
            out.append({'at': bar * 4 + (s16 + per // 2) / 4, 'len': GOURD['len'], 'pitch': GOURD['pitch'], 'vel': GOURD['vel'][1], 'gain': f"{GOURD['back'] + hard:g}dB"})
    return out


def comb_notes():
    """v26 COMB: a bar's notes: a tongue for each thing that rings; SPREAD: as evenly as that many can be over the bar; FOLLOWS: as hard as its thing rings. v27 CHANGES, COURSES: which tongue is in which place; TREBLE: the one to follow."""
    out, whole, runs = [], len(COMB['tines']), comb_runs()
    for bar in range(BARS):
        who = comb_rings(bar)
        order, row = comb_row(bar, runs)
        for i, k in enumerate(order):
            s16 = COMB['at'] + (16 * i // len(who) if ON['spread'] else 16 * list(COMB['tines']).index(who[i]) // whole)
            if s16 >= 16 and not comb_rings(bar + 1):            # the phrase's end crosses the bar line: not into a bar where the comb rests
                continue
            db = (round(COMB['soft'] * (1 - ring_at(k, bar)), 1) if ON['follows'] else 0) + COMB['trim'].get((len(who), i), 0) + (HUNT['db'] if ON['treble'] and row is not None and i and k == HUNT['treble'] else 0) + (HUNT['clear'].get((len(who), i), 0) if ON['clear'] else 0)
            out.append({'at': bar * 4 + s16 / 4, 'len': COMB['len'], 'pitch': COMB['tines'][k], 'vel': COMB['vel'], **({'gain': f'{db:g}dB'} if db else {}),
                        **({'_walk': i / (len(order) - 1)} if ON['walks'] and ON['treble'] and row is not None and k == HUNT['treble'] and len(order) > 1 else {})})   # v28 WALKS: where the tongue to follow is in its bar, 0 (first) to 1 (last)
    return out


def comb_walk(notes):
    """v28 WALKS: (the comb's notes that stay in the middle, the left track's, the right track's): a walking note is shared between the two by equal power, by its place in the bar."""
    mid, left, right = [], [], []
    for n in notes:
        if '_walk' not in n:
            mid.append(n)
            continue
        w, base = n['_walk'], float(n.get('gain', '0dB')[:-2]) + WALK['ends'] * abs(2 * n['_walk'] - 1)
        for side, g in ((left, cos(w * pi / 2)), (right, sin(w * pi / 2))):
            if g > 0.01:
                side.append({**{x: y for x, y in n.items() if x not in ('_walk', 'gain')}, 'gain': f'{round(base + 20 * log10(g), 1):g}dB'})
    return mid, left, right


def build():
    T = {k: [] for k in things()}
    if ON['room']:
        T.update({k + '-room': [] for k in ROOM_THINGS if k in T})
        if ON['remember']:
            T.update({k + '-kept': [] for k in ROOM_THINGS if k in T and k in KEPT})
    T.update({k + '-drop': [] for k in things() if dropped(k)})
    for bar in range(BARS):
        for thing in things():
            if bar < enters(thing) or any(a <= bar < b for a, b in [OUT_OF.get(thing, (0, 0))]):
                continue
            alone = listened(bar)
            if alone and thing not in alone and thing not in answering(bar):
                continue
            r_bar = 1.0 if alone else ring_at(thing, bar)        # whatever sounds in a listening is let go altogether
            mine = [x for x in cell_of(thing, bar) if x[0] // BAR == bar % 2]
            if ON['aside'] and thing == ASIDE['who'] and laid(ASIDE['for'], bar):   # v14 ASIDE: the big drum stands aside for the skin's bar
                continue
            for s, pitch, vel in cell_of(thing, bar):
                if thing == 'weight' and slack(bar):             # v20 SLACK: the head is slack: its note is lower
                    pitch = step(pitch, slack(bar))
                if ON['empty'] and dropped(thing) and bar == dropped(thing)[0] and s // BAR == bar % 2 and s % BAR > dropped(thing)[1]:
                    continue                                    # v9 EMPTY: its stick is on the floor
                if s // BAR == bar % 2:
                    r = 1.0 if ((ON['fore'] and bar == foretaste(thing)) or bar == aftertaste(thing)) and s == mine[-1][0] else r_bar
                    off = called(thing, bar) and s == mine[-1][0]   # v12 CALL: the hand comes off on this stroke
                    if off:
                        r = CALL['ring']
                    n = stroke(thing, bar * 4 + (s % BAR) / 4, pitch, vel, r)
                    if thing == 'weight' and slack(bar, 'db'):   # v20 SLACK: the slack head is as loud as the tight one was
                        n['gain'] = f"{round(float(n.get('gain', '0dB')[:-2]) + slack(bar, 'db'), 2)}dB"
                    if hand_on(thing, bar) or (off and hand_of(thing)):   # v10: the hand changes what the stroke finds
                        h = hand_on(thing, bar) or hand_of(thing)
                        n['pitch'] = step(pitch, h['steps'][stopping(thing).index(bar) if bar in stopping(thing) else 0]) if 'steps' in h else f"{hz(pitch) * h['ratio']:.1f}hz" if 'ratio' in h else up(pitch, h['semis'])
                        if h['db']:
                            n['gain'] = f"{round(float(n.get('gain', '0dB')[:-2]) + h['db'], 2)}dB"
                        if ON['fade'] and thing in FADE and bar == stopping(thing)[-1] and s == mine[-1][0]:   # v11: its last stroke under the hand
                            n['gain'] = f"{round(float(n.get('gain', '0dB')[:-2]) + FADE[thing], 2)}dB"
                        if shown(bar) and thing in SHOW:
                            n['gain'] = f"{round(float(n.get('gain', '0dB')[:-2]) + SHOW[thing], 2)}dB"
                        if ON['turn'] and laid(thing, bar) and thing in TURN['db'] and not (ON['heard'] and thing in HEARD['not']):   # v14 TURN: it steps forward for its bar (v15: the plate's lift was never delivered)
                            n['gain'] = f"{round(float(n.get('gain', '0dB')[:-2]) + TURN['db'][thing], 2)}dB"
                        if off and (thing in CALL['db'] or thing == 'plate'):
                            n['gain'] = f"{round(float(n.get('gain', '0dB')[:-2]) + (EDGE['call'] if thing == 'plate' else CALL['db'][thing]), 2)}dB"
                    if thing == 'wood' and (grip(bar) or off or laid(thing, bar)):   # v11: the hand on the bar's middle
                        x = 1 if off or laid(thing, bar) else grip(bar)
                        n['expr'] = {**n['expr'], **({'note': round(10 * log10(1 - (1 - 10 ** (GRIP['note'] / 10)) * x), 2), 'mode': round(-float(GRIP['from'][:-2]) + 10 * log10(x), 2)} if ON['equal'] else {'hand': x})}
                    if alone and ALONE:
                        down = ANSWER_DB if thing not in alone else ALONE_OF.get(thing, ALONE) if ON['even'] else ALONE
                        n['gain'] = f"{round(float(n.get('gain', '0dB')[:-2]) + down, 2)}dB"
                    if ON['lift'] and thing in LIFT and bar == aftertaste(thing) and r == 1.0 and not alone:
                        n['gain'] = f"{round(float(n.get('gain', '0dB')[:-2]) + LIFT[thing], 2)}dB"
                    if ON['floor'] and ON['room'] and thing in FLOOR['who'] and laid(thing, bar):   # v16 FLOOR: the low room hears it in the bar its hand goes on
                        T.setdefault(thing + '-floor', []).append(dict(n))
                    T[thing + '-drop' if dropped(thing) == (bar, s % BAR) else thing].append(n)   # v8: the dropped stroke goes by a track of its own, so that only it bounces
                    if thing + '-room' in T and r >= ROOM_FROM:      # the room hears a thing as far as it is let go
                        own = float(n.get('gain', '0dB')[:-2])
                        T[thing + '-room'].append({**n, 'gain': f'{round(own + 20 * log10(r), 2)}dB'})
                    elif thing + '-kept' in T and (remembered(thing, bar) or (ON['heard'] and thing in HEARD['who'] and laid(thing, bar))):   # v5: stopped, and its hall still open (v15 HEARD: and in the bar its hand goes on)
                        T[thing + '-kept'].append({**n, 'gain': f"{round(float(n.get('gain', '0dB')[:-2]) + HEARD['db'][thing], 2)}dB"} if ON['heard'] and laid(thing, bar) and thing in HEARD['db'] and not remembered(thing, bar) else dict(n))
                    if thing == 'air' and blown() == (bar, s % BAR):        # v9 BLOW: the breath is not taken off: up the pipe's harmonics to the one
                        for j, h in enumerate(BLOW['harmonics'], 1):
                            m = {**n, 'at': n['at'] + j / 4, 'pitch': up(pitch, round(12 * log2(h))), 'gain': f"{round(float(n.get('gain', '0dB')[:-2]) + BLOW['db'] * j, 2)}dB"}
                            T[thing].append(m)
                            if thing + '-room' in T:
                                T[thing + '-room'].append(dict(m))
    if ON['third'] and ON['trade'] and THIRD['lift']:             # v22 THIRD: the plate's strokes while it plays the pipe's cell, lifted (dry and to the hall)
        for k in ('plate', 'plate-room'):
            if T.get(k):
                T[k] = [{**n, 'gain': f"{round(float(n.get('gain', '0dB')[:-2]) + THIRD['lift'], 2)}dB"} if THIRD['at'] <= n['at'] // 4 < TRADE['to'] else n for n in T[k]]
        if ON['four']:                                            # v24 FOUR: of those, the ones on beat 4, 3 dB more
            for k in ('plate', 'plate-room'):
                if T.get(k):
                    T[k] = [{**n, 'gain': f"{round(float(n.get('gain', '0dB')[:-2]) + FOUR['db'], 2)}dB"} if THIRD['at'] <= n['at'] // 4 < TRADE['to'] and round(n['at'] % 4 * 4) == FOUR['at'] else n for n in T[k]]
    if ON['glass']:                                               # v24 GLASS: the eighth thing, sung and not struck: one held note a section while the others are stopped
        T['glass'] = [{'at': a * 4, 'len': (b - a) * 4 - GLASS['early'], 'pitch': pitch, 'vel': GLASS['vel'], **({'gain': f'{db}dB'} if db else {})} for a, b, pitch, db in GLASS['notes']]
    if ON['rasp']:                                                # v25 RASP: the ninth thing, scraped: a row of clicks a bar
        T['rasp'] = rasp_notes()
    if ON['shaken']:                                              # v28 SHAKEN: the eleventh thing, shaken
        T['gourd'] = gourd_notes()
    if ON['twin'] and ON['motor'] and T.get('metal'):             # v21 TWIN: the metal is a pair; QUICKEN: the gap between them doubles twice
        both, second = [], []
        for n in T['metal']:
            span = next((x for x in (SLOWS['bars'] if ON['slows'] and ON['quicken'] else ()) + TWIN['bars'] if x[0] <= n['at'] // 4 < x[1]), None)   # v23 SLOWS: the pair goes back the way it came
            if span and n.get('expr', {}).get('ring', 0) >= TWIN['ring'] and not n['pitch'].endswith('hz'):
                db = f"{round(float(n.get('gain', '0dB')[:-2]) + TWIN['db'], 2)}dB"
                both.append({**n, 'gain': db})
                second.append({**n, 'gain': db, 'pitch': f"{hz(n['pitch']) + BPM * 4 / 60 / (span[2] if ON['quicken'] else TWIN['gap']):.2f}hz"})
            else:
                both.append(n)
        if second:
            T['metal'], T['metal-twin'] = both, second
            if ON['hallpair'] and T.get('metal-room'):           # v22 HALLPAIR: the hall is sent both bars
                twin_of = {m['at']: m['pitch'] for m in second}
                assert len(twin_of) == len(second)
                room, room2 = [], []
                for n in T['metal-room']:
                    if n['at'] in twin_of and not n['pitch'].endswith('hz'):
                        db = f"{round(float(n.get('gain', '0dB')[:-2]) + TWIN['db'], 2)}dB"
                        room.append({**n, 'gain': db}); room2.append({**n, 'gain': db, 'pitch': twin_of[n['at']]})
                    else:
                        room.append(n)
                if room2:
                    T['metal-room'], T['metal-twin-room'] = room, room2
    return T


def song(T, bars=BARS):
    track = lambda name, gain, pan=0, **more: {'name': name, 'patch': patch_of(name), 'gain': gain, 'pan': pan, 'notes': T[name], **more}
    hold = lambda db: f'clip drive=0dB ceiling={db}dB'          # a stroke's highest sample is its own, not the limiter's
    doc = {
        'about': "Chirpers, Escapement, track 4: Ring True, by chirper-one. Generated by compose/chirpers11/src/chirpers11-t4.py (its docstring is the rule). " + ('Seven' if ON['plate'] else 'Six') + " struck things, each a physical model or noise, play one two-bar cell from the first bar to the last; the only thing that changes is how long each is allowed to ring. Every click is a note stopped too soon to be heard as one: the form lets them go one at a time, then shuts them again.",
        'meta': {'artist': 'chirpers', 'album': 'Escapement', 'title': 'Ring True', 'track': 4, 'year': 2026},
        'tempo': BPM, 'seed': 1, 'event_stable': True, 'length': f'{bars * 4}b', 'tail': '4s', 'ceiling': '-1dB', 'true_peak': True, 'loudness': -12,
        'patches': PATCHES,
        'buses': {'room': {'fx': ['reverb kind=room decay=0.4s mix=1 predelay=6ms', 'hp cutoff=300']}},
        'master': {'fx': [{'type': 'eq', 'bands': ['hp cutoff=28']}]},
        'tracks': [track('weight', '-3dB'), track('wood', '-3dB', pan=-0.3, sends={'room': '-14dB'}), track('metal', '-5dB', pan=0.35, sends={'room': '-14dB'}),
                   track('skin', '0dB', pan=0.15, fx=[hold(-10)], sends={'room': '-14dB'}), track('string', '-3dB', pan=-0.1), track('air', f"{2 + LONG['fader']:g}dB" if ON['long'] and ON['flue'] else '2dB', pan=0.05, fx=[hold(-9)], sends={'room': '-12dB'})],
    }
    by_name = {t['name']: t for t in doc['tracks']}
    if ON['grip']:
        wood = PATCHES['rt-wood']
        bar = wood['synth']['layers'][0]
        doc['patches'] = {**doc['patches'], GRIP['patch']: {**wood, 'about': "Ring True: the wood with a hand on its middle (v11). rt-wood, and a second bar two octaves up (the wood's second mode, 4 times its note); the stroke's expr.hand (0 no hand, 1 held) takes the first down and brings the second up, so that held, the second mode is what is left.",
                                                            'synth': {**wood['synth'], 'layers': [{**bar, 'level': {'value': '0dB', 'mod': [{'src': 'expr.hand', 'amount': GRIP['note']}]}},
                                                                                                  {**bar, 'semi': GRIP['semis'], 'level': {'value': GRIP['from'], 'mod': [{'src': 'expr.hand', 'amount': GRIP['mode']}]}}]}}}
        if ON['equal']:                                        # v12: the same two bars, each with its own level on the stroke
            del doc['patches'][GRIP['patch']]
            doc['patches'] = {**doc['patches'], EQUAL['patch']: {**wood, 'about': "Ring True: the wood with a hand on its middle, as an equal-power pair (v12, after Wind Down's wd-grip). rt-wood, and a second bar two octaves up (the wood's second mode); each has its level on the stroke: expr.note (dB on the note, 0 with no hand) and expr.mode (dB over -40 on the second mode).",
                                                               'synth': {**wood['synth'], 'layers': [{**bar, 'level': {'value': '0dB', 'mod': [{'src': 'expr.note', 'amount': 1}]}},
                                                                                                     {**bar, 'semi': GRIP['semis'], 'level': {'value': GRIP['from'], 'mod': [{'src': 'expr.mode', 'amount': 1}]}}]}}}
    if ON['boom'] and ON['note']:
        doc['patches'] = {**doc['patches'], 'rt-drum': drum_patch()}
        if ON['disc']:                                           # v18 DISC: the weight's patch with the disc under its head
            doc['patches'] = {**doc['patches'], patch_of('weight'): disc_patch(drum_patch())}
    elif ON['boom']:
        doc['patches'] = {**doc['patches'], 'rt-boom': NEW['rt-boom']}
        by_name['weight']['gain'] = BOOM['gain']
    if ON['flue']:
        doc['patches'] = {**doc['patches'], patch_of('air'): flutter_patch(flue_patch()) if patch_of('air') == FLUTTER['patch'] else flue_patch()}   # v18 FLUTTER
    if ON['motor']:                                              # v17 MOTOR: the metal's patch with its disc
        doc['patches'] = {**doc['patches'], MOTOR['patch']: motor_patch(doc['patches'][PATCH['metal']])}
        if ON['twin']:                                           # v21 TWIN: the same bar and disc with no wander from stroke to stroke
            true = motor_patch(doc['patches'][PATCH['metal']])
            doc['patches'] = {**doc['patches'], TWIN['patch']: {**true, 'about': "Ring True: the metal that rings true (v21). rt-motor's bar and disc with the engine's stroke-to-stroke wander off (`vary: 0`): every stroke sounds its written note (rt-motor's are 2 cents under to 5 over it, a new draw each time), so that two of them tuned a set number of waves a second apart breathe at that rate and no other.",
                                                                 'synth': {**true['synth'], 'layers': [{**true['synth']['layers'][0], 'vary': 0}] + true['synth']['layers'][1:]}}}
    if ON['plate'] and 'plate' in T:
        doc['patches'] = {**doc['patches'], 'rt-plate': NEW['rt-plate']}
        doc['tracks'].append(track('plate', PLATE['gain'], pan=PLATE['pan'], sends={'room': '-16dB'}))
        by_name['plate'] = doc['tracks'][-1]
    if ON['room']:
        doc['buses'] = {**doc['buses'], 'hall': {'fx': ['reverb kind=hall decay=2.4s mix=1 predelay=20ms', 'hp cutoff=300', 'lp cutoff=7000']}}
        for k in ROOM_THINGS:
            if k + '-room' in T:
                dry = by_name[k]
                doc['tracks'].append({'name': k + '-room', 'patch': dry['patch'], 'gain': f"{float(dry['gain'][:-2]) + ROOM_DEPTH}dB", 'pan': dry['pan'],
                                      'notes': T[k + '-room'], 'out': 'hall', **({'fx': dry['fx']} if 'fx' in dry else {})})
        for k in ROOM_THINGS:
            if T.get(k + '-kept'):
                dry = by_name[k]
                doc['tracks'].append({'name': k + '-kept', 'patch': dry['patch'], 'gain': f"{float(dry['gain'][:-2]) + KEPT[k] + (SOFT['kept'].get(k, 0) if ON['soft'] else 0)}dB", 'pan': dry['pan'],
                                      'notes': T[k + '-kept'], 'out': 'hall', **({'fx': dry['fx']} if 'fx' in dry else {})})
    if ON['floor'] and ON['room'] and any(T.get(k + '-floor') for k in FLOOR['who']):   # v16 FLOOR: a second room under the first
        doc['buses'] = {**doc['buses'], 'floor': {'fx': [FLOOR['reverb'], f"hp cutoff={FLOOR['hp']}", f"lp cutoff={FLOOR['lp']}"]}}
        for k in FLOOR['who']:
            if T.get(k + '-floor'):
                dry = by_name[k]
                doc['tracks'].append({'name': k + '-floor', 'patch': dry['patch'], 'gain': f"{float(dry['gain'][:-2]) + FLOOR['db'][k]}dB", 'pan': dry['pan'], 'notes': T[k + '-floor'], 'out': 'floor'})
    for k in [k for k in by_name if T.get(k + '-drop')]:        # v8 DROP: the same track again for the one stroke, and its bounces: echoes of it, each sooner and softer by the same share
        doc['tracks'].append({**{x: y for x, y in by_name[k].items() if x != 'notes'}, 'name': k + '-drop', 'notes': T[k + '-drop']})
        rest = (BAR - dropped(k)[1]) * 60000 / BPM / 4            # ms from the stroke to the one
        gap = rest * (1 - DROP['share']) / (1 - DROP['share'] ** (DROP['bounces'] + 1))
        doc['buses'][k + '-bounce'] = {'pan': by_name[k]['pan'], 'returns': [{'from': k + '-drop', 'gain': f"{20 * log10(DROP['share']) * j:.2f}dB", 'time': f"{gap * (1 - DROP['share'] ** j) / (1 - DROP['share']):.1f}ms"} for j in range(1, DROP['bounces'] + 1)]}
    if ON['sympathy'] and bars == BARS:
        hand = {'points': [['0b', -60], [f'{TOP[6] * 4 - 1}b', -60], [f'{TOP[6] * 4}b', SYMPATHY['let']], [f'{TOP[7] * 4}b', 0], [f'{TOP[8] * 4}b', 0], [f'{(TOP[8] + QUICK) * 4}b', -60]] +
                          ([[f'{TOP[11] * 4 - 1}b', -60], [f'{TOP[11] * 4}b', 0], [f'{TOP[12] * 4 - 1}b', 0], [f'{TOP[12] * 4}b', -60]] if ON['close'] else []) +   # v7: let go while the wood closes; shut again for the taps
                          [[f'{(BARS - LAST) * 4 - 0.5}b', -60], [f'{(BARS - LAST) * 4}b', 0], [f'{BARS * 4 + 16}b', 0]], 'curve': 0}
        for name, hz, side in SYMPATHY['strings']:
            me = 'sym-' + name.lower()
            t = f"{1000 / hz - 225.1 / SYMPATHY['lp']:.3f}ms"         # a period, less the low-pass's own delay (0.2251 / its cutoff), so the loop is in tune
            doc['buses'][me] = {'pan': side, 'gain': {'value': '0dB', 'mod': [{'src': 'auto.hand', 'amount': 1}]}, 'auto': {'hand': hand}, 'fx': [f"lp cutoff={SYMPATHY['lp']}"],
                                'returns': [{'from': k, 'gain': SYMPATHY['feed'], 'time': t} for k in SYMPATHY['feeds']] + ([{'from': k, 'gain': OWN['feed'], 'time': t} for k in OWN['feeds']] if ON['own'] else []) + ([{'from': k, 'gain': SKIN['feed'], 'time': t} for k in SKIN['feeds']] if ON['skin'] and name in SKIN['strings'] else []) + [{'from': me, 'gain': f"{20 * log10(SYMPATHY['back']):.2f}dB", 'time': t}]}
    if ON['tongue'] and bars == BARS:                          # v19 TONGUE: the pipe's let-go strokes of one section on a track of their own, with a rolled tongue
        air = next(t for t in doc['tracks'] if t['name'] == 'air')
        a, z = TOP[TONGUE['section']] * 4, TOP[TONGUE['section'] + 1] * 4
        rolled = [n for n in air['notes'] if a <= n['at'] < z and n['expr']['ring'] > 0]
        if rolled:
            air['notes'] = [n for n in air['notes'] if not (a <= n['at'] < z and n['expr']['ring'] > 0)]
            doc['tracks'].append({**air, 'name': 'air-tongue', 'notes': rolled, 'gain': f"{float(air['gain'][:-2]) + TONGUE['db']:g}dB",
                                  'fx': list(air.get('fx') or []) + [{'type': 'tremolo', 'depth': TONGUE['depth'], 'rate': TONGUE['rate']}]})
            for b in doc['buses'].values():                      # whoever hears the pipe hears these strokes too
                if any(r.get('from') == 'air' for r in b.get('returns', [])):
                    b['returns'] = b['returns'] + [{**r, 'from': 'air-tongue'} for r in b['returns'] if r.get('from') == 'air']
    if T.get('metal-twin'):                                       # v21 TWIN: the second bar, beside the first: its fader, its place, its room
        doc['tracks'].append({**{x: y for x, y in by_name['metal'].items() if x != 'notes'}, 'name': 'metal-twin', 'notes': T['metal-twin']})
        for b in doc['buses'].values():                          # whoever hears the metal hears both bars
            if any(r.get('from') == 'metal' for r in b.get('returns', [])):
                b['returns'] = b['returns'] + [{**r, 'from': 'metal-twin'} for r in b['returns'] if r.get('from') == 'metal']
    if T.get('glass'):                                            # v24 GLASS: its patch and its track; RUB: the finger's turn
        doc['patches'] = {**doc['patches'], GLASS['patch']: {
            'about': "Ring True: the glass (v24): the eighth thing, the only one that is not struck: a finger goes round its rim, and it sings only while the hand is on it. A sine and a twin a few cents over (a glass's two near modes beat), its second partial 2.32 times up; the level rocks as the finger comes round, two turns to three beats; half a second to speak, a second to stop.",
            'synth': {'layers': [{'wave': 'sine', **({'level': {'value': f"-{GLASS['rub']}dB", 'mod': [{'src': 'lfo.rub', 'amount': GLASS['rub']}]}} if ON['rub'] else {})},
                                 {'wave': 'sine', 'detune': GLASS['cents'], 'level': {'value': f"{GLASS['twin'] - GLASS['rub']}dB", 'mod': [{'src': 'lfo.rub', 'amount': GLASS['rub']}]} if ON['rub'] else f"{GLASS['twin']}dB"},
                                 {'wave': 'sine', 'semi': GLASS['partial'][0], 'level': f"{GLASS['partial'][1]}dB"}],
                      **({'lfo': {'rub': {'wave': 'sine', 'rate': GLASS['rate'], 'phase': 0, 'retrig': True}}} if ON['rub'] else {}),
                      'amp': {'a': GLASS['speak'], 'd': '0s', 's': 1, 'r': GLASS['stop']}},
            'play': {'vel_sens': 0.3, 'gate': 1}}}
        doc['tracks'].append({'name': 'glass', 'patch': GLASS['patch'], 'gain': GLASS['gain'], 'pan': GLASS['pan'], **({'sends': {'room': GLASS['room']}} if 'room' in doc.get('buses', {}) else {}), 'notes': T['glass']})
    if T.get('rasp'):                                             # v25 RASP: its patch and its track
        doc['patches'] = {**doc['patches'], RASP['patch']: RASP_PATCH}
        doc['tracks'].append({'name': 'rasp', 'patch': RASP['patch'], 'gain': RASP['gain'], 'pan': RASP['pan'], **({'sends': {'room': RASP['room']}} if 'room' in doc.get('buses', {}) else {}), 'notes': T['rasp']})
    if T.get('metal-twin-room'):                                  # v22 HALLPAIR: the second bar's own way to the hall, as the first's
        first = next(t for t in doc['tracks'] if t['name'] == 'metal-room')
        doc['tracks'].append({**{x: y for x, y in first.items() if x != 'notes'}, 'name': 'metal-twin-room', 'notes': T['metal-twin-room']})
    if T.get('gourd'):                                            # v28 SHAKEN: its patch and its track
        doc['patches'] = {**doc['patches'], GOURD['patch']: GOURD_PATCH}
        doc['tracks'].append({'name': 'gourd', 'patch': GOURD['patch'], 'gain': GOURD['gain'], 'pan': GOURD['pan'], **({'sends': {'room': GOURD['room']}} if 'room' in doc.get('buses', {}) else {}), 'notes': T['gourd']})
    if ON['comb'] and bars == BARS:                               # v26 COMB: the tenth thing, plucked
        doc['patches'] = {**doc['patches'], COMB['patch']: comb_patch()}
        doc['tracks'].append({'name': 'comb', 'patch': COMB['patch'], 'gain': COMB['gain'], 'pan': COMB['pan'], **({'sends': {'room': COMB['room']}} if 'room' in doc.get('buses', {}) else {}), 'notes': (c_mid := comb_walk(comb_notes()))[0]})
        for c_name, c_pan, c_notes in (('comb-left', -WALK['pan'], c_mid[1]), ('comb-right', WALK['pan'], c_mid[2])):   # v28 WALKS: the tongue to follow, between two tracks
            if c_notes:
                doc['tracks'].append({'name': c_name, 'patch': COMB['patch'], 'gain': COMB['gain'], 'pan': c_pan, **({'sends': {'room': WALK['room']}} if 'room' in doc.get('buses', {}) else {}), 'notes': c_notes})
    return doc


def bench():
    """Each thing alone, one stroke every two seconds at rings 0, 0.2 … 1 (60 BPM, a stroke every two beats)."""
    was = ON['room']
    ON['room'] = False                                           # the bench reads the things dry
    T = {k: [stroke(k, 2 * i, strokes_of(k)[0][1], .8, i / 5) for i in range(6)] for k in things()}
    doc = song(T, bars=3)
    ON['room'] = was
    doc.update(tempo=60, length='12b', tail='2s', loudness=None)
    for t in doc['tracks']:
        t.update(gain='0dB', pan=0, sends={})
    return doc


def dump(doc):
    lines = []
    for k, v in doc.items():
        if k == 'tracks':
            lines.append('tracks:')
            lines += ['  - ' + json.dumps(t) for t in v]
        else:
            lines.append(f'{k}: {json.dumps(v)}')
    return '\n'.join(lines) + '\n'


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--out', type=Path, default=OUT)
    ap.add_argument('--form', action='store_true', help='print the form and stop')
    ap.add_argument('--bench', action='store_true', help='write the bench song (each thing at six rings) instead')
    for k, on in ON.items():
        ap.add_argument(f"--{'without' if on else 'with'}-{k}", action='store_true', help=f"{'leave out' if on else 'put in'} {k} (of the seventy-two that are on: all off is v1; the last sixty-seven off is v2; the last sixty-three off is v3; the last sixty off is v4; the last fifty-seven off is v5; the last fifty-six off is v6; the last fifty-three off is v7; the last fifty-one off is v8; the last forty-eight off is v9; the last forty-four off is v10; the last forty off is v11; the last thirty-eight off is v12; the last thirty-six off is v13; the last thirty-four off is v14; the last thirty-three off is v15; the last thirty-two off is v16; the last thirty-one off is v17; the last thirty off is v18; the last twenty-eight off is v19; the last twenty-five off is v20; the last twenty-two off is v21; the last nineteen off is v22; the last seventeen off is v23; the last fourteen off is v24; the last eleven off is v25; the last eight off is v26; the last four off is v27)")
    a = ap.parse_args()
    for k, on in list(ON.items()):
        ON[k] = on != getattr(a, f"{'without' if on else 'with'}_{k}")
    if a.form:
        sec = 60 / BPM * 4
        for i, name in enumerate(NAMES):
            b, e = TOP[i], TOP[i + 1]
            print(f'{i + 1:2d}  bars {b + 1:3d}-{e:3d}  {int(b * sec) // 60}:{b * sec % 60:05.2f}  {name:38s} ' +
                  ' '.join(f'{k} {ring_at(k, b):.2f}>{ring_at(k, e - 1):.2f}' for k in list(SHAPE) + (['plate'] if ON['plate'] else []) if e > enters(k) and not any(x <= b < y for x, y in [OUT_OF.get(k, (0, 0))])))
        if ON['sympathy']:
            print(f"    the strings nobody plays ({' '.join(n for n, _, _ in SYMPATHY['strings'])}): let go across bars {TOP[6] + 1}-{TOP[7]}, open to bar {TOP[8]}, stopped by bar {TOP[8] + QUICK}, let go in bar {BARS}" + (f"; let go again while the wood closes, bars {TOP[11] + 1}-{TOP[12]}" if ON['close'] else '') + ('; they hear the string as well as the wood and the air' if ON['own'] else '') + (f"; {' and '.join(SKIN['strings'])} hear the skin too" if ON['skin'] else ''))
        if ON['drop']:
            print('    the stick is let go too: ' + ', '.join(f'the {k} in bar {dropped(k)[0] + 1} on sixteenth {dropped(k)[1] + 1} ({(BAR - dropped(k)[1]) * 60000 / BPM / 4:.0f} ms to the one)' for k in things() if dropped(k)) + f"; {DROP['bounces']} bounces, each {DROP['share']} of the one before")
        if ON['empty'] and ON['drop']:
            print('    the hand is empty: once its stick is dropped a thing plays nothing more in that bar')
        if blown():
            print(f"    the air overblows: after its stroke in bar {blown()[0] + 1} on sixteenth {blown()[1] + 1}, harmonics {' '.join(str(h) for h in BLOW['harmonics'])} of its pipe, a sixteenth each, to the one")
        if ON['long'] and ON['flue']:
            print("    the air's breath trails off: a second, slower breath behind the first")
        for k, h in HAND.items():
            if ON[h['switch']] and stopping(k):
                print(f"    a hand on the {k}, bars {stopping(k)[0] + 1}-{stopping(k)[-1] + 1}: " + {'touch': 'touched at its middle, its octave is what is left', 'cap': 'the pipe is shut at its end: an octave lower', 'press': 'the head is pressed and tightens: a step up the five notes, then two', 'pinch': 'held at its middle, its second mode is what is left (2.76 times the note)', 'choke': 'the beater is held against the head, which tightens: a step up the five notes, then two'}[h['switch']] + ': ' + ' '.join(n['pitch'] for n in build()[k] if n['at'] // 4 in stopping(k)))
        if ON['grip']:
            print(f"    a hand on the wood as it closes, bars {TOP[11] + 1}-{TOP[12]}: on its middle, bar by bar: its note {GRIP['note'] * grip(TOP[11]):.1f} to {GRIP['note'] * grip(TOP[12] - 1):.0f} dB, its second mode (two octaves up) {float(GRIP['from'][:-2]) + GRIP['mode'] * grip(TOP[11]):.1f} to {float(GRIP['from'][:-2]) + GRIP['mode'] * grip(TOP[12] - 1):.0f} dB")
        if ON['show'] and ON['hush']:
            print(f"    the hush shows the hands, bar {HUSH + 1}: " + ', '.join(f"the {k} {' '.join(n['pitch'] for n in build()[k] if n['at'] // 4 == HUSH)}" for k in HAND if hand_on(k, HUSH)) + ("; the wood gripped: its second mode" if grip(HUSH) else ''))
        if ON['equal'] and ON['grip']:
            print("    the wood's hand is an equal-power pair: its note and its second mode each have their level on the stroke")
        if ON['call']:
            print('    the hands come off one at a time, the last stroke of a bar each: ' + ', '.join(f"bar {BARS - LAST - len(order()) + j + 1} the {k} ({[n['pitch'] for n in build()[k] if n['at'] // 4 == BARS - LAST - len(order()) + j][-1]})" for j, k in enumerate(order()) if called(k, BARS - LAST - len(order()) + j)))
        if ON['laid'] and ON['call']:
            print('    and are heard going on first, a bar each, the other way round: ' + ', '.join(f"bar {BARS - LAST - len(order()) - j} the {k} ({[n['pitch'] for n in build()[k] if n['at'] // 4 == BARS - LAST - len(order()) - 1 - j][-1]})" for j, k in enumerate(order()) if laid(k, BARS - LAST - len(order()) - 1 - j)))
        if ON['turn'] and ON['laid'] and ON['call']:
            print('    each steps forward for the bar its hand goes on: ' + ', '.join(f'the {k} {v:+d} dB' for k, v in TURN['db'].items() if k in order() and not (ON['heard'] and k in HEARD['not'])))
        if ON['heard'] and ON['laid'] and ON['call'] and ON['room'] and ON['remember']:
            print('    the hall hears each hand go on: ' + ', '.join(f'bar {b + 1} the {k}' for b in range(BARS) for k in HEARD['who'] if laid(k, b)))
        if ON['floor'] and ON['room']:
            print('    and the low room under it hears the low ones: ' + ', '.join(f'bar {b + 1} the {k}' for b in range(BARS) for k in FLOOR['who'] if laid(k, b)))
        if ON['aside'] and ON['laid'] and ON['call']:
            print(f"    the {ASIDE['who']} stands aside for the bar the hand goes on the {ASIDE['for']}: bar " + ' '.join(str(b + 1) for b in range(BARS) if laid(ASIDE['for'], b)))
        if ON['edge'] and ON['plate']:
            print(f"    the plate has a hand: held at its edge its strokes are an octave up (bars {' '.join(str(b + 1) for b in stopping('plate'))}, the bar that shows the hands, and the mirror)")
        if ON['fade'] and ON['cap']:
            print(f"    the shut pipe's last stroke (bar {stopping('air')[-1] + 1}): {FADE['air']} dB")
        if ON['motor']:
            print(f"    the metal has a motor: a disc under the bar turns once a beat, open on the off-beat it is struck on and shut on the beat: its ring is {2 * MOTOR['db']} dB down on every beat and back between; a stopped stroke is as it was")
        if ON['disc'] and ON['boom'] and ON['note']:
            print(f"    the same disc is under the weight: struck on the beat, its head's ring is open on the beat and {2 * DISC['db']} dB down on the off-beat, where the metal's is open: the two rings take turns; the thud is not turned")
        if ON['flutter'] and ON['flue'] and ON['long']:
            print(f"    the air's breath is fluttered: three to the beat, {FLUTTER['db']} dB up and down: three in the breath against four in the hands; its puff is not")
        if ON['tongue']:
            print(f"    the pipe is flutter-tongued while there is no weight (bars {TOP[TONGUE['section']] + 1}-{TOP[TONGUE['section'] + 1]}): the tongue rolls three times a sixteenth ({BPM / 60 * 12:g} a second), the breath falling {-20 * log10(1 - TONGUE['depth']):.0f} dB at each roll; every stroke meets it at the same place in its turn")
        if ON['heft'] and ON['disc'] and ON['boom'] and ON['note']:
            print(f"    the weight's head is {HEFT['db']} dB up under its disc: open it is over the old drum's head, shut {2 * DISC['db'] - HEFT['db']} dB under it")
        if ON['trade']:
            print(f"    the things trade cells, one pair at a time, to bar {TRADE['to']}: " + '; '.join(f"from bar {at + 1} the {x} plays the {y}'s" + (f" (an octave {'down' if semis > 0 else 'up'})" if semis else '') + f" and the {y} the {x}'s" + (f" (an octave {'up' if semis > 0 else 'down'})" if semis else '') for x, y, semis, at in TRADE['pairs']) + f"; from bar {TRADE['to'] + 1} each has its own again")
        if ON['rasp']:
            runs = []
            for b in range(*RASP['bars']):
                c = None if listened(b) else rasp_count(b) if ON['tally'] else RASP['plain']
                if runs and runs[-1][2] == c:
                    runs[-1][1] = b
                else:
                    runs.append([b, b, c])
            print(f"    the ninth thing is scraped: a notched stick: a row of clicks a sixty-fourth apart ({60000 / BPM * RASP['gap']:.0f} ms), the last on beat {RASP['at'] // 4 + 1} of the bar, bars {RASP['bars'][0] + 1}-{RASP['bars'][1]}; it rests where a thing is listened to alone" +
                  (': a notch for every thing that rings: ' + ', '.join((f"bar {a + 1}" if a == b else f"bars {a + 1}-{b + 1}") + f": {c}" for a, b, c in runs if c is not None) + f"; and {RASP['more']:g} dB more on the row for each notch in it" if ON['tally'] else '') +
                  (f"; the row climbs to its last click ({RASP['pitch']}), each notch a step of the five notes under the next: {' '.join(step(RASP['pitch'], -RASP['climb'] * j) for j in range(7, -1, -1))}" if ON['zip'] else ''))
        if ON['glass']:
            print("    the eighth thing is not struck: a glass, sung by a finger going round its rim: it sounds only while the hand is on it, so it sings where the others are stopped: " + ', '.join(f"{pt} bars {a + 1}-{b}" for a, b, pt, _ in GLASS['notes']) + f"; on bar {GLASS['notes'][-1][1] + 1} the hands begin to come off and the finger does first: as the others are let go and ring, the glass stops" + (f"; the finger takes {GLASS['turn']:g} beats to come round: its level rocks {2 * GLASS['rub']:g} dB, two turns to three beats: the swell falls on a beat, then between two, and meets the bar line every third bar" if ON['rub'] else ''))
        if ON['four'] and ON['third'] and ON['trade'] and THIRD['lift']:
            print(f"    the plate's traded strokes on beat 4 are {FOUR['db']} dB up again (bars {THIRD['at'] + 1}-{TRADE['to']})")
        if ON['slows'] and ON['quicken'] and ON['twin'] and ON['motor']:
            print('    the pair goes back the way it came while the others are stopped: ' + '; '.join(f"bars {a + 1}-{b}: {BPM * 4 / 60 / g:.2f} Hz (one wave {'a beat' if g == 4 else 'an eighth'})" for a, b, g in SLOWS['bars']) + f"; on bar {SLOWS['bars'][-1][1] + 1} the hand is on the metal and there is one bar")
        if ON['fall'] and (ON['foretold'] or (ON['third'] and ON['trade'])):
            print(f"    the {THIRD['pair'][0]} ends the {THIRD['pair'][1]}'s cell as it ends its own: the last of the seven strokes falls to {strokes_of(THIRD['pair'][0])[-1][1]}: " + ' '.join(pt for _, pt, _ in cell_of(THIRD['pair'][0], THIRD['told'][0] if ON['foretold'] else THIRD['at'])))
        if ON['third'] and ON['trade']:
            x, y, semis = THIRD['pair']
            print(f"    a third pair trades first: from bar {THIRD['at'] + 1} the {x} plays the {y}'s cell ({semis // 12} octaves down: " + ' '.join(up(pt, -semis) for _, pt, _ in strokes_of(y)) + f") and the {y} the {x}'s ({semis // 12} octaves up: " + ' '.join(up(pt, semis) for _, pt, _ in strokes_of(x)) + '): all six have changed hands by the peak\'s end')
        if ON['foretold']:
            x, y, semis = THIRD['pair']
            print(f"    the third trade is told once before too, stopped, bars {THIRD['told'][0] + 1}-{THIRD['told'][1]}: the {y} taps the {x}'s cell and the {x} the {y}'s; on bar {THIRD['told'][1] + 1} the {x} is let go and has its own")
        if ON['hallpair'] and ON['twin'] and ON['motor'] and ON['room']:
            print("    the hall hears both bars of the metal's pair: its copy of each paired stroke is two, tuned apart as in the room")
        if ON['hint']:
            print(f"    the trade is told once before, stopped, bars {HINT['bars'][0] + 1}-{HINT['bars'][1]}: the {HINT['pair'][1]} taps the {HINT['pair'][0]}'s cell (an octave up) and the {HINT['pair'][0]} the {HINT['pair'][1]}'s (an octave down); on bar {HINT['bars'][1] + 1} the {HINT['pair'][0]} is let go and has its own")
        if ON['told']:
            print(f"    the second trade is told once before too, stopped, bars {TOLD['bars'][0] + 1}-{TOLD['bars'][1]}: the {TOLD['pair'][1]} taps the {TOLD['pair'][0]}'s cell and the {TOLD['pair'][0]} the {TOLD['pair'][1]}'s; on bar {TOLD['bars'][1] + 1} the {TOLD['pair'][0]} is let go and has its own")
        if ON['twin']:
            print("    the metal is a pair wherever it is let go: a second bar struck with the first, tuned over it by the tempo: " + '; '.join(f"bars {a + 1}-{b}: {BPM * 4 / 60 / (g if ON['quicken'] else TWIN['gap']):.2f} Hz (one wave {'a beat' if (g if ON['quicken'] else TWIN['gap']) == 4 else 'an eighth' if (g if ON['quicken'] else TWIN['gap']) == 2 else 'a sixteenth'})" for a, b, g in TWIN['bars']) + f": in step at the stroke, against each other half a wave later; each {-TWIN['db']} dB under the old stroke")
        if ON['slack']:
            print(f"    the weight's head goes slack, bars {SLACK['from'] + 1}-{SLACK['from'] + len(SLACK['steps'])}: a step down the five notes each bar: " + ' '.join(step(STROKES['weight'][0][1], k) for k in SLACK['steps']) + f", and {STROKES['weight'][0][1]} again on bar {SLACK['from'] + len(SLACK['steps']) + 1}")
        if ON['comb']:
            runs = []
            for bar in range(BARS):
                who = comb_rings(bar)
                if who and runs and runs[-1][2] == who and runs[-1][1] == bar:
                    runs[-1][1] = bar + 1
                elif who:
                    runs.append([bar, bar + 1, who])
            print(f"    the tenth thing is plucked: a comb of steel tongues ({COMB['patch']}), one for each thing in the order they are let go: " + ', '.join(f'the {k} {v}' for k, v in COMB['tines'].items()) +
                  ": in every bar the tongues of the things that ring" + (', spread as evenly as that many can be over the bar' if ON['spread'] else ', each in its own place') + (', each as hard as its thing rings' if ON['follows'] else '') + ': ' +
                  '; '.join(f"bars {a + 1}-{b}: {' '.join(COMB['tines'][k] for k in who)}" + (f" on {' '.join(str(COMB['at'] + 16 * i // len(who)) for i in range(len(who)))}" if ON['spread'] else '') for a, b, who in runs) + f" (sixteenths of the bar; 16 is the next bar's one); {len(comb_notes())} notes")
        if ON['comb'] and (ON['changes'] or ON['courses']):
            c_runs = comb_runs()
            for c_a, c_b, c_who in c_runs:
                c_rows = [comb_row(c_bar, c_runs) for c_bar in range(c_a, c_b)]
                if c_rows[0][1] is None:
                    continue
                digits = lambda order: ''.join(str(c_who.index(k) + 1) for k in order)
                c_first = next(x for x, (_, r) in enumerate(c_rows) if r)
                print(f"    the comb rings the changes on {len(c_who)}, bars {c_a + 1}-{c_b}: a plain hunt: every bar each tongue changes places with a neighbour ({2 * len(c_who)} rows to a course)" +
                      (f": rounds for {c_first} bar{'s' if c_first > 1 else ''}, then" if c_first > 1 else ':') + ' ' + ' '.join(digits(order) for order, _ in c_rows[c_first if c_first > 1 else 0:]) +
                      (f": back in rounds on the run's last bar" if c_rows[-1][0] == c_who else f": it comes round on bar {c_b + 1}, where the comb goes on with the tongues that are left") +
                      f" (1 is {COMB['tines'][c_who[0]]}, the {c_who[0]}'s; {len(c_who)} is {COMB['tines'][c_who[-1]]}, the {c_who[-1]}'s)")
            if ON['treble']:
                print(f"    the {HUNT['treble']}'s tongue is the one to follow: {HUNT['db']} dB harder wherever it is not first in its bar: it goes from the first place to the last, a place a bar, and back")
        if ON['comb'] and ON['clear']:
            print("    the comb's weakest places are written up: " + ', '.join(f"note {c_i + 1} of {c_n} {c_db:+g} dB" for (c_n, c_i), c_db in HUNT['clear'].items()))
        if ON['shaken']:
            g_bars = [g_b + 1 for g_b in range(*GOURD['bars']) if not listened(g_b)]
            print(f"    the eleventh thing is shaken: a gourd of seeds ({GOURD['patch']}): a shake is two sounds, the throw and the fall back ({-GOURD['back']} dB under, and a softer touch): bars {g_bars[0]}-{g_bars[-1]}, where there is no weight and through the peak: a shake a beat, thrown on the beat" +
                  (f"; from bar {max(GOURD['fast'], min(g_b for g_b in range(GOURD['fast'], GOURD['bars'][1]) if not listened(g_b))) + 1} a shake an eighth, {GOURD['hard']} dB harder" if ON['doubles'] else '') + f"; it rests where a thing is listened to alone (bars {' '.join(str(g_b + 1) for g_b in range(*GOURD['bars']) if listened(g_b))}) and is put down on bar {GOURD['bars'][1] + 1}" +
                  (f"; the throw is held longer the more the family rings: {' '.join(f'{1000 * 60 / BPM * g_l:.0f}' for g_l in sorted({g_n['len'] for g_n in gourd_notes() if g_n['vel'] == GOURD['vel'][0]}))} ms" if ON['swirls'] else ''))
        if ON['walks'] and ON['treble'] and ON['comb']:
            print(f"    the comb's tongue to follow walks across the stereo as it walks through the bar: the first place on the left, the last on the right (two tracks at {WALK['pan']} either side, equal power): {sum(1 for w_n in comb_notes() if '_walk' in w_n)} strokes")
        print(f'{BARS} bars, {BARS * sec:.1f} s; strokes: ' + ', '.join(f'{k} {len(v)}' for k, v in build().items()))
    else:
        a.out.write_text(dump(bench() if a.bench else song(build())))
