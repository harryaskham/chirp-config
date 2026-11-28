#!/usr/bin/env python3
"""Wind Down (Escapement, track 8, the closer). Clicky minimal techno, 124 BPM running down to 50, G minor, 200 bars.

THE RULE. Nothing here is new. One thing is taken from each of the other seven songs, gathered a section at a time
on one grid in one key, held together, and then let go one at a time, last in, first out, until the first thing on
the record (a click off the beat) is alone again. Then the spring runs down: over the last eight bars the tempo
falls from 124 to 50, each tick is let ring a little longer than the last, and the final stroke, let go altogether
and an octave down, lands ON the one, where that click has never been.

  from 1 Give or Take      the grid: a bass drum on the four and one click on the off-beats (sixteenths 2 6 10 14)
  from 7 Out of Step       the half-bar pattern x x . x . x x . on a short saw click
  from 5 Hearing Things    the bass with no fundamental (harmonics two to six), its line a tone down, off the beat
  from 4 Ring True         the cell's tune on the wooden bar, stopped; let go once everything is gathered
  from 2 Least Common      the meeting tune: a ping where two of the cycles 3, 5 and 7 meet, a chord where all three do
  from 3 Standing Room     standing room: two walls 3 and 5 sixteenths away, round the click
  from 6 Small Change      one seed every two bars and a pair of coins, 3 and 5, a fifth up and a fourth down
The click itself is Ring True's wooden bar playing Give or Take's grid: a note stopped too soon, until the end.

v2 (26 Nov): WHAT THE SONGS LEARNT SINCE. The seven grew after v1 quoted them, and chirper-zero offered three of
his (06:04): the closer takes one more thing from four of them, and one from the album's name. Six switches, each
`--without-…` (all six off is v1 byte for byte):
  CATCH   the escapement itself. In the last bar before each thing comes the wheel is caught: everything stops but
          the click (in its room, once it has one), and on the one it is let go with the new thing in it. Seven
          catches, the last before all are gathered. Nothing is caught on the way out: that is the winding down.
  COMP    from 7 Out of Step v2: the complement . . x . x . . x, a small bright click in the pattern's three holes.
          It fits only when everything is home, so it plays through the hold and no longer: for those 32 bars every
          sixteenth of the bar is struck.
  HAT     from 5 Hearing Things: its hat, backwards. From the bar the first thing leaves to the bar the drum goes, a
          hat that slows down through every eight bars and starts the next where it started the last: the song has
          been winding down for a minute and a half before the tempo moves.
  LEARNT  from 3 Standing Room v3: when the room goes, what is left of it is in the bass. For the eight bars after
          its door shuts the bass plays the room's three-three-two (D F C D F C on sixteenths 2 5 7 10 13 15).
  STOP    from 1 Give or Take v3: the stop. The spring does not run down in a straight line against the beat (v1): it
          loses speed in a straight line against the clock, as a platter does when the motor goes off: slowly, then
          all at once. Speed sqrt(1 - 2x / W) after x beats, W chosen so that a fifth of it is left on the one
          (v1 kept two fifths): the last ticks are nearly two seconds apart.
  TUCK    the click 3 dB lower while anything else plays (it stood 14 dB over the envelope at its own note), and as
          it was while it is alone.

v3 (26 Nov): EACH LEAVES AS ITSELF. In v2 a thing went by being absent from the next bar, and the scorer heard
bars 114 to 172 as one section. Six switches, each `--without-…` (all six off is v2 byte for byte); five are the
leaving thing's own song's idea, in its last bars, and the sixth is the end:
  SPENT   6 Small Change: the change spends what it has left. In its last four bars a seed every bar, not every
          two, and in the last of them on beats one and three; the coins run on over the bar line after it.
  HELD    2 Least Common: the meetings' last word is a chord that is not let go: on the bar they leave, the chord
          held for a bar and two bars dying. The only held sound in the song.
  TAKEN   4 Ring True: the cell is taken back into the hand. Over its last eight bars its ring goes from let go
          to stopped, so it leaves as the click it came as.
  REAL    5 Hearing Things: the bass with no fundamental is given it. For its last four bars a sine plays the
          notes the ear had been supplying; then both go.
  SLIP    7 Out of Step: the pattern slips. In its last eight bars it starts a sixteenth later each bar: eight
          steps, eight bars, so it has gone all the way round and is in step again in the bar it leaves.
  SINK    1 Give or Take's stop, its other half (chirper-zero's A RECORD SWITCHED OFF): as the spring runs down
          each tick's NOTE sinks with the speed, as a record's does when the motor goes off. A clock's tick does
          not sink, but by then each tick is being let ring into a note. A quarter of the speed is left on the
          one (v2: a fifth), so the note has sunk exactly two octaves: the last stroke is G4, reached, not jumped to.

v4 (26 Nov): THE BODY OF THE SOUND. v3 read 10 and 11 dB over the album's envelope from 1.4 to 1.6 kHz and 11
under at 71 Hz: a song with a waist and no hips. Read by parts, the middle is the click's note and the saw's
eighth harmonic (between them half to nine tenths of 1 to 2 kHz once the cell has gone), and nothing at all lives
between the drum (47 Hz) and the bass's second harmonics (98 up). Three switches (`--without-mid`, `-body`,
`-open`; all three off is v3 byte for byte):
  MID    the click is turned from its note towards its click: 6 dB off round G6 (1568 Hz) and 3 dB on round
         11 kHz, after its clip. While it is alone it is 4.5 dB up, so the lone click stands where it stood.
         As the spring runs down and the note sinks it leaves the cut behind, so the note comes out as it falls
         (and the 4.5 dB is taken off again by the last stroke). The saw's click loses 5 dB round 1.6 kHz.
  BODY   the drum is given the body between its note and the bass: 5 dB round 72 Hz.
  OPEN   the last chord opens as it dies. It was held under a low-pass that never moved; now the filter is shut
         while the chord is held (600 Hz) and opens two octaves in the first two and a half seconds of its
         going, which now takes six, not three (with both at three seconds the chord was 17 dB under the mix
         before the filter had moved a third of the way): the meetings' last word gets brighter as it gets
         quieter, a door opening on something leaving.

v28 (28 Nov): EVERYONE IS COUNTED IN, AND THE ELEVEN IS COUNTED BEFORE IT COMES. Three switches (`--without-entered`,
`-counts`, `-laid`; all three off is v27 byte for byte).
  ENTERED  the notched stick counts the seven out as they leave (v25: bars 145 to 192, a row a bar). It was not
           there when they came. Now each is counted IN: one row in the bar it comes (bars 17, 33, 49, 65, 81, 97;
           not the grid, which is the click itself), a notch for each one here: 2 3 4 5 6 7. And these rows CLIMB
           to their click (the notches before it, rising, as in Ring True), where the rows that count them out
           are drawn back and fall away after it: counted in, counted out.
  COUNTS   the eleven's big brother is told twice before the eleven comes (v27: bars 91 and 102). In Least Common
           (v28) it counts its own eleven softly before the small one comes; here too: between its first told
           stroke and home its bar again every 11 beats, softer (not on its own strokes, not in a caught bar): bar
           93 beat 4, bar 99 beat 2, bar 104 beat 4, bar 107 beat 3, bar 110 beat 2: 8 elevens from bar 91 to
           home, bar 113, where the small one takes the count up on that very beat.
  LAID     when only the click is left the stick was put down (its last row is in bar 192). Now that is heard:
           one tap of its lowest notch in bar 193, where the next row would have been.

v27 (28 Nov): THE BIG BROTHER COMES HOME TOO, AND HERE THE TWO AGREE. Three switches on (`--without-elder`,
`-told`, `-apart`; all three off is v26 byte for byte) and one written and off (`--with-aired`).
  ELDER   in Least Common (v27) the eleven has a big brother: its wooden bar let ring, 269.5 Hz, on the bar line
          every eleven BARS; and there the small eleven, counted from another place, is one beat behind it.
          Here the small one's knock is already at that pitch, and short: 20 dB down in 70 ms: a knock more
          than a note, so its slow rise to the twelfth harmonic could hardly be heard as a rise. Now the big
          brother comes home with it (`wd-eleven-big`: the same bar let ring, at the eleven's own pitch, a
          stroke higher each time): on the bar line every eleven bars from where all are gathered. From there
          to the last stroke is 88 bars: 8 elevens of bars and 0 over, as it is 32 elevens of beats and 0
          over: nine strokes, bars 113 124 135 146 157 168 179 190 and the last stroke, each one together
          with every fourth knock of the small eleven. Away from home the two counts were a beat apart. At
          home they agree, and the last stroke of both is the album's last stroke, on D over the hour bell.
  TOLD    the big brother is heard before the eleven comes, as the caught bars say who is coming: two and
          one elevens of bars early, on the bar lines of bars 91 and 102 (not in a caught bar), 3 dB softer.
  APART   and there the two are as they were in Least Common: the small eleven's knock one beat behind the
          big bar, on beat 2 of bars 91 and 102. Twice a beat apart; then, from bar 113, together.
  AIRED   (off) the big bar sent to the hall (-12 dB). Built and measured: over its first half second it
          keeps its pitch there (within 8 cents), but then the hall answers at its own: 277 Hz after the
          strokes written 269.5 to 278.7, and 297 to 298 Hz after those written 287.9 to 294.0 (the last
          stroke's answer 25 cents sharp, under the bell); and the stroke written nearest the hall's own
          note (bar 135, 275.6 Hz) rings on for a second, 6 to 18 dB over the others' answers: one stroke
          in nine has a tail. It cost 0.006 of score too. It is dry, as the small one is.

v26 (28 Nov): THE ELEVEN COMES HOME. Three switches (`--without-eleven`, `-lands`, `-creeps`; all three off is
v25 byte for byte).
  ELEVEN  in Least Common (v26) a fourth voice counts eleven beats, the next prime after that song's three,
          and misses its home by one beat: 210 is nineteen elevens and one over. This song's home is the
          album's: the last stroke. From the bar everything is gathered (bar 113) to the last stroke is 88
          bars, 352 beats: thirty-two elevens and nothing over. So the eleven begins when all are gathered
          (`wd-eleven`: Least Common's low wooden bar under this song's name), is struck every eleven beats
          with its echo every eleven sixteenths between, as there, through the hold, the leaving and the
          spring's running down, and its thirty-third stroke is the last stroke of the record: it comes home.
  LANDS   there its note is the eleventh harmonic of the drum's G (539 Hz), a note no scale here has. Here
          it is an octave lower, 269.5 Hz (this song is already 5.8 dB over the album in the band at 547 Hz:
          read with compscore --bands after the first build), and on the last stroke it is the TWELFTH:
          294 Hz, the fifth, the D over the hour bell's B flat: in tune. It is dry: in the hall a note this
          short is answered at the hall's own nearest pitch (up to 43 cents off, read), and that is not home.
  CREEPS  and it gets there as the song runs down: each stroke is a thirty-second of a harmonic nearer
          (harmonic 11, 11 1/32, 11 2/32 ... 12 of 24.5 Hz: 0.77 Hz a stroke, 4 to 5 cents): the one thing
          in this song that rises while everything else leaves or slows.

v25 (28 Nov): SOMEBODY KEEPS THE SCORE AS THEY LEAVE. Three switches (`--without-tally`, `-back`, `-full`; all
three off is v24 byte for byte).
  TALLY  in Ring True (v25) a ninth thing counts the others: a notched stick, a notch for every thing that
         rings. Here it counts who is still in the room. From the bar the change goes (bar 145) to the bar
         before the drum goes (bar 192) a row of dry clicks a sixty-fourth apart (`wd-rasp`: Ring True's notch
         under this song's name) begins on beat 3 of every bar, a notch for each of the seven that is still
         here: six, then five when the room goes, four, three, two, one: the row is a notch shorter each
         time somebody leaves, every eight bars, and when only the click is left there is nothing to count
         and the stick is put down. It is the same row every time, cut a notch shorter.
  BACK   in Ring True the row is drawn towards its last click and climbs to it. Here it is drawn BACK: its
         first click is on the beat (D7) and the notches fall away after it, a step of the five notes
         and softer each: a thing running down, as everything in this song does.
  FULL   the score is read once while all seven are here: one row of seven notches in bar 144, the bar
         before the first one leaves (the song's own way: what is coming is told once before).

v24 (28 Nov): THE TICK COMES APART AS THE SPRING RUNS DOWN, AND THE RECORD IS OFF ITS CENTRE. Four switches
(`--without-rundown`, `-limp`, `-wow`, `-waver`; all four off is v23 byte for byte).
  RUNDOWN  v23's teeth are heard where the drum plays and not after. Now they come back under the last ticks
           (bars 193 to 200, when the drum has gone and the spring runs down), and they tell how far down it
           is. A watchmaker's timing machine reads a balance's swing from the time between a tick's first
           sound and its last (the lift time): the weaker the swing, the longer the tooth takes to fall. So
           each of the 32 last clicks has its tooth again, and the tooth falls after the click by a time that
           grows as the spring's speed falls (RUNDOWN['lift'] seconds times one over the speed, less one):
           nothing at bar 193, 16 ms at bar 197, 35 ms at bar 199, 83 ms at the last click but one: the tick
           thickens, then comes apart into two sounds. On the last stroke no tooth falls: the wheel has
           stopped. (The teeth are placed by the tempo map as written, turned round: second_at.)
  LIMP     the second pallet's tooth has twice as far to fall (2 to 208 ms): tick is still one sound when tock
           is two.
  WOW      everything here is ON a record, and the record is pressed off its centre (WOW['off'] mm): once a
           turn the groove runs fast and slow under the needle, and what rings long enough to show it wavers
           in pitch: the clock's bells. The same hole and a smaller circle: the nearer the label, the deeper
           the wow, so each quarter's chime wavers more than the last (the radius falls evenly, as v21's
           hiss does), and the hour bell most. It turns with the record: it is at its top where the groove
           joins itself, at every joint of the run-out. New patches, the old bells with the wow:
           `wd-chime-wow-1` to `-4` and `wd-hour-wow`. Ring True's strings, which are tuned to the hour bell,
           now hear it go out of tune and back once a turn: benched alone with them, its ring is 1.8 dB
           lower in its third second than the steady bell's (without them the two are the same to 0.1 dB).
  WAVER    the meetings' last chord (bar 161: held a bar, then six seconds dying as it opens) is the one other
           sound on the record long enough for a turn to be heard in it: it wavers too, four turns and more
           (`wd-open-wow`). Nothing else is given the wow: a liberty; the rest is too short to show it.

v23 (28 Nov): THE ESCAPEMENT IS HEARD: TICK, TOCK; AND THE TURNTABLE RUMBLES IN THE RUN-OUT. Three switches
(`--without-pallet`, `-exit`, `-rumble`; all three off is v22 byte for byte).
  PALLET   the song is a clock, and the click is its grid, on the half beats. When the drum comes (bar 9) the
           click is tucked under it, and from there to the hat (bar 145) the song had next to nothing above
           10 kHz: the top octave stood 44 to 50 dB under the whole for three and a half minutes, where the
           click alone in bars 1 to 8 has it 22 dB under. A clock's tick is the escape wheel's tooth on the
           pallet: a few ms of metal, all of it at the top. Now each click that falls in a bar where the drum
           plays has that tooth with it (`wd-pallet`: 6 ms of noise above 10 kHz, a track of its own), from
           bar 9 to bar 144. Not in the caught bars (the click is bare there and the master brings its own top
           up), not in bars 1 to 8 (chirper-zero's seam), and not once the hat is in.
  EXIT     an escapement has two pallets and a clock says two things. The tooth on the second pallet (the
           clicks on sixteenths 6 and 14) is lower: a band from 8 to 11 kHz, with less of the first one's
           top (`wd-pallet-exit`): tick, tock, tick, tock. (A first try, the same tooth with the octave under
           it from 5 kHz, was on no meter: the click's own wood is 15 dB over it there. A second, 8.5 to
           12.5 kHz with gentler sides, read the same as the tick from 9 to 12.5 kHz and 6 dB under it above.)
  RUMBLE   the record has had a surface, a run-out groove, a pre-echo and a lifted needle; a turntable also has
           a bearing, heard under a quiet groove as a low rumble that comes round with the platter. In the
           run-out, from its first joint to the needle's lift: noise from 25 to 90 Hz (`wd-rumble`), the same
           samples at every turn (one note a turn, begun on the joint: the engine's clockless chip noise). It
           stops with the surface when the needle is lifted. (Under the last ticks as well, from bar 193, it
           cost the scorer a section at two levels: it is in the run-out only.)

v22 (27 Nov): THE NEXT BAR IS HEARD BEFORE IT COMES. Two switches (`--without-preecho`, `-nearer`; both off is
v21 byte for byte). v20 and v21 made the end a record (a run-out groove, its surface, the needle lifted) and v21's
surface was faint. A record has one sign that needs no quiet room: PRE-ECHO. A loud groove is cut beside a silent
one and presses through its wall: in the silence before a loud entry the entry is heard faintly, one turn early.
  PREECHO  this song has such silences: the caught bars, where everything stops but the click, and the bar after,
           where everything comes back with one thing more. In caught bars 16, 32, 48 and 112 the first turn of
           the bar after (1.8 s at 33 1/3: 3.72 beats) is heard a turn early, 30 dB down: every stroke of
           everything but the click and the clocks, on tracks of their own (`pre-...`: the same patches, places
           and sends, no fader rides). A turn is not a bar: 1.8 s against 1.935 s: the ghost's beats fall 135 ms
           after the caught bar's own: a beat of another time, as a real one is. The catch already says who is
           coming, by a note or two of the new thing; the record says ALL that is coming, and says it too soon.
           NOT in caught bars 64, 80 and 96: the first build had all seven, and the scorer's cuts at those three
           (0.20, 0.18, 0.20: the catch's own beginning) fell to 0.16, 0.16, 0.17: structure 100 to 95.3, the
           total 1.08 down; at 38 dB down there it was still 0.16 down. A silence the scorer leans on is left.
  NEARER   v21's surface under the last ticks stood 3 dB over the floor. It comes back 9 dB nearer, and the
           locked groove's hiss 6: the step up at the first joint, 5 dB in v21, is 2.

v21 (27 Nov): THE RECORD COMES UP AS THE SPRING RUNS DOWN. Three switches on (`--without-leadin`, `-reveal`,
`-inner`; all off is v20 byte for byte) and one written and off (`--with-spiral`). v20 made the end a record: a
run-out groove, its surface, the needle lifted. But that surface began from nothing at the first joint, 1.1 s after
the last stroke: a record with no surface until it had finished playing.
  LEADIN  the record's surface comes in under the click over bars 1 to SPIRAL['in'] (no stroke: it fades in; Out of
          Step's last eight bars lie over these, and chirper-zero allowed it on three conditions: nothing over
          10 kHz, in over the bars and not at a stroke, 25 dB or more under his last eight bars), and goes under
          the drum over bars 9 to 12. It is NOT the run-out's hiss: in the playing groove the needle is on new
          vinyl at every turn, so this surface never comes round (one held white hiss, new patch wd-spiral);
          only the locked groove repeats (wd-surface, v20).
  REVEAL  and it comes up again as the spring runs down (over bars 193 to 196) and stays to the first joint of
          the run-out, where the locked groove's takes over: the machine stops and what it was written on is
          heard under it. The run-out's hiss no longer starts from nothing.
  INNER   the needle has gone in. A groove's dust passes it more slowly the nearer the label: the hiss's whole
          band slides down with the radius, r(t) / r(0): an LP's first groove is at 146 mm and its last at 60 mm,
          and the needle crosses that at an even rate (a spiral of even pitch): 700 to 6000 Hz in bar 1 is 290
          to 2487 Hz at the last stroke; in the locked groove (53 mm) 255 to 2186 Hz (its patch is then
          wd-inner: another band, another name). The same roughness in a narrower band: its level is held by
          -10 log10 of the same ratio (3.8 dB at the label).
  SPIRAL  (off) the hiss under the WHOLE record. Built first, on two seeds: the scorer reads it in every quiet
          frame (99.676 for 99.854: sections more alike, recurrence 0.47 to 0.51), and measured it is under the
          song's own tails nearly everywhere (6 dB over the floor in a caught bar, 1 dB in bars 5 to 8): it
          takes the black out of the silences for a hiss nobody hears under the music. Written, and off.
          Two engine facts cost a build each: a lane on a filter's cutoff (`cutoff=700+auto.slide*-411`) is
          not in Hz: the depth is in OCTAVES (cutoff = 700 x 2^(depth x lane)), and in Hz the track was silent
          with no word from `chirp plan`; and a held note is let go at 95% of its written length unless its
          patch says `gate: 1` (800 beats of one note lost its last 19 s).

v20 (27 Nov): THE RECORD IS STILL TURNING. Three switches (`--without-groove`, `-surface`, `-lift`; all off is
v19 byte for byte). The rule's first lines call the click 'the first thing on the record'; Give or Take now begins with
a record being started (chirper-zero's v24). The closer ended when its clock had struck: the spring run down,
the wall clock's four last ticks, the bell dying. But all of that is ON a record, and a record does not stop
when its music does.
  GROOVE   after the last stroke the needle is in the run-out groove, which is a circle: a click where the
           groove joins itself, once a turn (1.8 s: 33 1/3 turns a minute), and the same three specks of
           dust every time round, 3, 3+5 and 3+5+7 sixteenths of a turn after the joint (the three cycles
           this record counts in, and one sixteenth over to the joint). GROOVE['turns'] turns and the joint
           once more. The first two turns are under the bell and the wall clock's last ticks (the turn's
           phase is set so that nothing of it falls within 170 ms of a tick); then the clock has stopped
           and the record has not: the loop is heard twice alone. Every speck is the same sound at every
           turn (the engine's chip noise with no clock: the same samples at each note-on: chirper-zero's
           finding): that sameness is what a locked groove is; a clock's ticks are never the same twice.
           New patch wd-groove. The song is GROOVE['turns'] turns less the old four beats longer.
  SURFACE  the record's surface, what the needle rides on: a faint hiss from the first joint on (new patch
           wd-surface). The first build held one white hiss, and in the finished song the third and fourth
           turns were then no more alike than chance (correlation 0.52): but a locked groove's surface is
           the same groove wall every time round. So the surface is a note a turn, begun at each joint, of
           the same chip noise at a step rate slow enough not to come round inside a turn (D3: 13.7 thousand
           steps a second, 2.4 s to a round): the hiss itself repeats with the record.
  LIFT     and then somebody lifts the needle: half a second after the last joint a soft low thump and one
           speck (new patch wd-lift), the surface gone at once, a second of nothing. Give or Take begins
           with a record being started on the other deck.

v19 (27 Nov): THE CLOCK STRIKES ONE. Three switches (`--without-hammer`, `-one`, `-sympathy`; all off is v18 byte
for byte).
  HAMMER   v18's bell was six partials that begin together in half a millisecond: a tone with no stroke (its
           own note said it might be a test tone). A clock's bell is struck: the hammer is a grain of noise
           HAMMER['ms'] ms long on the front of every chime note (new patch wd-chime-struck; wd-chime stands).
           Its level is an envelope on a noise layer, and what is written is not what comes out: benched, the
           grain's 6 ms above 3 kHz read -69 dBFS at 68 (written as 12 dB under the bell: it was 34 under),
           and 8.3 dB more for every 10: HAMMER['amount'] is the benched number, about 12 dB under the bell's
           own first 6 ms.
  ONE      v18 said the song's last stroke was the hour's one o'clock, on paper only. Now the clock strikes
           it: after the four changes (372 to 390 s) it waits 6.4 s and strikes its hour bell once, on the
           song's last stroke: B flat 2, an octave under the bell its quarters end on (Westminster's hour
           bell is the tonic under the quarters), struck harder and let ring ONE['ring'] (new patch wd-hour:
           the same bell, longer). The four ticks after the last stroke are heard under its ring: the clock
           has struck and is still going when the record ends. The first build had it at the chime's level:
           in the finished song its note stood 15 dB under the last stroke: ONE['db'] dB more.
  SYMPATHY Ring True's strings nobody plays are let go beside the last click (v6). Two of them are the hour
           bell's own notes: the B flat 2 string is its prime and the F2 string has its fifth and twelfth. They
           hear the bell (ONE['strings']) and ring with it, to its left and right.

v18 (27 Nov): THE CLOCK CHIMES THE SONG'S QUARTERS, AND AT THE END THE HOUR. Two switches (`--without-quarters`,
`-hour`; both off is v17 byte for byte). The record's clock (chirper-zero's, in Give or Take) chimes the Westminster
quarters of every minute and never the hour; Hearing Things quotes its half. This song is the record's last, and its
form is an hour by its own arithmetic: four quarters of forty-eight bars (the cell comes at bar 49, the change at 97,
home at 145, the spring runs down from 193). So the clock on the wall (v14: it does not run down) now says so:
  QUARTERS the clock chimes at the song's three quarters: one change at bar 49, two at bar 97, three at bar 145: the
           changes taken in order, round and round, as a clock takes them. A note at every whole second (the clock's
           time: 31 beats to 15 seconds, so each note is 32 ms later against the beat than the one before), beginning
           at the first whole second of the quarter: the two ticks heard in the caught bar before it are the two
           seconds before the first note.
  HOUR     as the spring runs down the clock rings the hour's four changes (the only time on the record), a note a
           second from the second the drum goes: the song's own tick slows from two a second to one in a second and
           a half while the chime keeps the seconds. It ends on B flat six seconds before the last stroke, which is
           its one o'clock.
The tune is zero's QUART_CHANGES (five changes on four bells, by degree of B flat: 3 2 1 5, 1 3 2 5, 1 2 3 1, 3 1 2 5,
5 2 3 1): D C B flat F: all four are in this song's G minor. The bells are this song's own (patch wd-chime: six
partials with no third: the first build used the engine's church bell, whose minor third put A flat over the saw's
G and D flat beside D, and at -15 dB it took 0.4 to 0.5 off the score: the low hums tilted the whole master), TWO
OCTAVES under Give or Take's (D4 C4 Bb3 F3 for D6 C6 Bb5 F5): the pitch
those bells would have on a platter at the quarter speed this song stops at (124 to 31), and the band where this
song is thin (250 to 350 Hz), under the cell (which plays the same four notes an octave up) and over the bass.

v17 (27 Nov): THE DRUM GOES TO THE FIFTH TOO, AND HOME IS WHOLE. Two switches (`--without-tuned`, `-resolve`; both
off is v16 byte for byte). Read first: v16 took the bass down to the fifth for sixteen bars (129 to 144) and gave it
its fundamental there, and its own note said what was weak: the return home (bar 145) is a cadence on paper: the
floor (the sine at 36.7 Hz) is simply taken away on the one, the bass goes UP a fourth as three things leave, and the
scorer's curve shows nothing. A cadence wants its arrival voiced where its tension was.
  TUNED    the drum goes to the fifth as well, the other way: UP a fifth, to D2 (73.4 Hz), for the same sixteen
           bars: the bass's D1 under it, the bass's own lowest sound (D2) on it. A tuned drum is an arrival of
           depth, not a bass line (Least Common v17, measured): on D2 it does not go down to 50 Hz; on the one of
           bar 145 it falls a fifth onto G1 and all its depth is back on that stroke. This song's drum has moved
           before (v11: the beater held against it, B flat 1 then C2, as it stops). BENCH (the drum alone,
           raw): this drum is mostly its sweep down to the note: from 66 to 82 Hz the drum on G1 has 3.5 dB
           MORE than the drum on D2 (so the chest, v9's bell at 71 Hz, served the old drum better), and tuned
           up it is 0.7 dB smaller with its highest sample 1.7 dB lower. So for those sixteen bars the drum is
           smaller and higher, the master delivers everything round it half a dB louder, and at home the big
           drum is back: the fifth is lighter, home is heavy.
  RESOLVE  home is whole for its first bar: the bass's fundamental stays under it for bar 145 (G1 G1 G1 B flat 1:
           49 Hz), and is taken away on the one of bar 146. The voice that made the fifth a turn now says where
           it was going: D1 to G1, a fourth up, in the same sine.

v16 (27 Nov): THE BASS GOES DOWN TO THE FIFTH. Two switches (`--without-fifth`, `-stand`; both off is v15 byte
for byte).
  FIFTH   Read first: from 'all gathered' (bar 113) to where the cell goes (bar 169) the scorer's novelty curve
          has no peak over 0.13: nearly two minutes, the song's summit and the first three things to leave,
          are one section to it; and the song has never left G: the drum on G1, the bass on G1, the pattern
          on G3, for six and a half minutes. The catches have always been led by a D (the bass's held D2
          before each new thing), and nothing has ever stood on it. Now, for the second half of 'all
          gathered' (bars 129 to 144, where the cell is let go), the bass's whole line goes down a fourth:
          D1 D1 D1 F1 | D1 D1 D1 D1 | D1 D1 D1 G1 | D1 D1 A1 C2: the fifth of the key, UNDER the drum. The
          pattern stays on G3 and the triad is G minor: over a D that is a chord waiting (D, G, A: the
          fifth with its fourth held), and it is let go on the one of bar 145, where the bass is home on G
          and the first things go: the song turns for home on a cadence, not only on a subtraction.
          The bass has no fundamental (harmonics two to six), so on D1 its lowest sound is D2, 73.4 Hz:
          the one band where this song has always been short (71 Hz: 8.1 dB under the album), because
          nothing was ever there: the drum is on 49 and 98, the bass on 98 and up.
  STAND   The first build had FIFTH alone, and the curve did not see it: the bass is a quiet off-beat pulse
          (its D2 12 dB under the drum in that band) and a fourth down moved the mix by 1 dB. Every other
          time this song holds a D the bass is WHOLE: before each new thing its own voice plays the D
          under its harmonics (v12), and in its last bars it is given its fundamental (v9, 'the bass is
          given its fundamental'). So on the fifth it is whole too: the same voice (wd-under, at the fader
          it has at the end) plays every note of the line with it: D1 is 36.7 Hz. The summit's second half
          has a floor under it, and it is taken away on the one of bar 145, where the bass is home.

v15 (27 Nov): THE OTHER CLOCK FALLS BEHIND. Two switches (`--without-clocks`, `-linger`; both off is v14 byte
for byte):
  CLOCKS  v14's wall clock is heard only at the end, when the spring has run down. But it was there all along,
          and this song's beat is not a second: 124 to the minute is 2.067 beats a second, so that 31
          beats take exactly 15 seconds, and against the wall clock the beat gains 32 ms every second
          beat. Seven times the escapement is caught and the click is alone for a bar (CATCH), on the
          half beats. Now the wall clock is heard in each of those bars as well, at the whole seconds of
          the song that fall in it (one or two). In the first catch (second 30) its tick is exactly on
          the beat, half way between two clicks, where the drum will come in a bar later: it sounds
          like the song's own. In the second (60, 61) it is on the beat and 32 ms after it; then 32 and
          65; 65 and 97; 97 and 129; 129 and 161; and in the last (215, 216), before all are gathered,
          161 and 194 ms after the beat: 81 and 49 ms before the next click. Catch by catch the other
          clock falls behind the beat it began on: the song is running fast. At the end the click
          slows, the clock catches it up near 388 s and goes on alone (v14). Same sound, same fader,
          same side as at the end; tick and tock keep the turns they would have had from second 0.
  LINGER  Ring True v15: what the master does not own is the time between strokes. v13's goodbyes are
          single strokes: the pattern's three (bar 185) and the drum's last (bar 193). They also go to
          the hall now, so each leaves a tail: the pattern's last three strokes hang for a bar and a
          half over the groove that goes on, and the drum's last stroke rings on as the spring begins
          to run down and the clock is first left alone with the click. The bass's goodbye (G1) is under
          the hall's 350 Hz and is not sent: a hall carries nothing under its own high-pass.

v14 (27 Nov): THE CLOCK ON THE WALL DOES NOT RUN DOWN. Two switches (`--without-wall`, `-cede`; both off is v13 byte
for byte):
  WALL   the album is called Escapement, and its first song has a clock on the wall (chirper-zero, Give or
         Take v16: one tick at every whole second of the song, through the section where nothing else keeps
         time). The last song is a spring running down. From the bar the drum goes (193) the same clock
         ticks here: at every whole second of THIS song (372, 373 ...), tick and tock by turns, on the right,
         taking no notice. The song's own click slows from a gap of 491 ms to 1.6 s; somewhere in bar 199
         its gap passes one second and for a moment the two keep the same time; then the click falls
         behind, the last stroke lands (396.4 s), and the clock ticks four times more (397 to 400) and the
         record ends. His sound, under this song's names (wd-clock-tick, wd-clock-tock): three 9 ms grains
         of noise a tick (unlock, impulse, drop: 14, 8 and 0 ms before the second) through a narrow band
         at 3.6 or 3 kHz. The seconds are found on this song's own tempo map (a ramp a beat).
  CEDE   v13's bass and pattern said goodbye under a groove that went on (the beat moved 0.3 and 0.0 dB).
         Not louder: room (Ring True v14). The drum gives the one of the bar after to whoever has just
         left: no bass drum on beat 1 of bars 177 and 185, as it already gives a beat to the answer in
         bars 147, 151 and 154.

v13 (27 Nov): THE BAR AFTER SAYS WHO HAS LEFT. Two switches (`--without-left`, `-ajar`; both off is v12 byte for
byte):
  LEFT   v12's rule the other way round. A catch says who is coming; now the bar after a thing has gone says
         who has left: the leaver plays whatever of its OWN figure falls in that bar's first beat, 3 dB under
         its stroke, and nothing after. Four of the seven leave with a gesture of their own and keep it (the
         change is paid and shut, the walls sing, the meetings hold their last chord, the cell is dropped).
         The three that only stopped now have one:
           bar 177  the bass: one more note, on the and of one (G1, with the fundamental it was given)
           bar 185  the pattern: its first three strokes (sixteenths 0, 1 and 3)
           bar 193  the drum: one stroke on the one, on G: after two bars with the beater held against it
                    (B flat, then C) the last stroke is let go and is the note the drum always had. Then
                    the spring runs down.
  AJAR   the one catch that told nothing was the room's (bar 80): its door opened slowly through two bars
         (-60 dB to 0), so in the caught bar it was half shut and not heard. Now the door is open for the
         whole caught bar and shut before it: the click alone is heard IN the room for one bar, and then
         the room comes. First built the other way (the door opening in the last beat only): on the bench
         the bar read the same to 0.2 dB with it and without: the walls answer a click three and five
         sixteenths late, and a door that opens with the last click lets nothing through before the bar
         line.

v12 (27 Nov): THE CATCH SAYS WHO IS COMING. Two switches (`--without-tell`, `-whole`; both off is v11 byte for
byte):
  TELL   seven times the escapement catches: a bar with only the click, and after it something new. Until now
         all seven were the same bar. Now each says who is coming: the newcomer plays whatever of its OWN
         figure falls in the caught bar's last beat, as if it had come a beat early (3 dB under its stroke):
           bar 16   the pattern: its last two strokes (sixteenths 13 and 14)
           bar 32   the bass with no fundamental: its last note of four bars, F2
           bar 48   the cell: the last stroke of its two-bar tune, C5, before it begins on D5
           bar 64   the meetings: three and five meet on beat 4 of this bar, a D5, and are heard to part
                    over the bar line
           bar 80   the room: nothing new (its door is already opening through this bar)
           bar 96   the change: one seed, three sixteenths before the one, so that its first coin (three
                    sixteenths on) falls ON the one with the first seed proper
           bar 112  the complement: the pattern's holes that fall in the beat (sixteenths 12 and 15)
  WHOLE  v11's lead (the bass's D2 through the last beat of five catches) is a bare sine: the bass's
         fundamental with none of its harmonics, where the bass itself is harmonics with no fundamental. On
         small speakers it is not there at all. Now, ONCE, the bass's own voice plays the same D2 with it,
         under it: the first time the bass comes back before the drum (bar 48) it is whole for that beat, so
         that the four bare fundamentals after it are known for the bass; then it has no fundamental again
         until bar 173 (Ring True v11's SHOW: shown once before). First built in all five catches the lead plays in:
         the scorer's boundary after each fell by 0.03 to 0.06 (one of them, where nothing else was new, from
         0.17 to 0.14) and its sections at the highest cut from 9 to 5: a catch whose last beat has the bass's
         voice in it is three quarters of a catch (v11's finding with two beats of the lead, again).

v11 (27 Nov): WHAT THE SONGS LEARNT AFTER MIDNIGHT. Ring True (v11) and Least Common (v11) each learnt something
in the last hour; the closer takes two things from the one and one from the other, and nothing of its own. Three
switches (`--without-grip`, `-choke`, `-lead`; all three off is v10 byte for byte):
  GRIP   4 Ring True v11: the wood has a hand. There, as the wood closes, the hand comes down on the bar's
         middle: its note goes and its second mode, two octaves up, is what is left. Here the cell IS that bar,
         and the hand takes it back over bars 161 to 168: so bar by bar the cell's tune goes up two octaves as
         it is stopped (the note 12 dB down by the last bar, the second mode at the note's old level). And on
         the cell's last stroke the hand lets go of the stick and of the bar (v8): that one stroke has its
         note again, whole, and bounces on it. A new patch name, wd-grip. Ring True's crossfade was linear in
         dB and dipped 6 dB in the middle; here each layer has its own level on the stroke (expr.note,
         expr.mode) and the two are an equal-power pair: a change of colour, not of level.
  CHOKE  4 Ring True v11: the weight's head tightens under the beater as it is stopped. Here the drum goes at
         bar 193: in its last two bars the beater is held against it and its note rises, B flat then C for G.
         The drum does not just stop: it is stopped.
  LEAD   2 Least Common v11: the bass comes back before the drum. In each caught bar where the bass is already
         in (bars 48, 64, 80, 96, 112) the bass's own fundamental (the sine it is given at the end, v3) holds
         D, the fifth below, through the bar's last beat into the one the drum comes back on. Not the whole
         bar: Least Common found that a break with the bass's band filled is no longer a break. FIRST BUILT
         WITH THE LAST TWO BEATS HELD, and this song found the same thing at half the size: rendered in full,
         the scorer's sections fell from 10 to 8 at its highest cut, and came back with the lead out.

v10 (26 Nov): WHAT THE SONGS LEARNT TONIGHT. Small Change (v9) and Least Common (v10) each learnt something after
the closer last quoted them; it takes one thing from each and nothing of its own. Three switches (`--without-
exchange`, `-rate`, `-given`; all three off is v9 byte for byte):
  EXCHANGE  6 Small Change v9: the same change in another currency. While the change spends what is left (bars
            141 to 144, a seed a bar) the seeds are also paid by a second pair of coins, 3 and 5, of a unit two
            thirds of a sixteenth (three of its units for two sixteenths): the same fifths up on the left and
            fourths down on the right, one and a half times as fast, three against two with the first pair. A
            hand opens it for those four bars and lets it down over the two after, as the first pair's run on.
  RATE      6 Small Change v9: through the hold the complement has filled the pattern's holes, so that every
            sixteenth of the bar is struck. In its last four bars the complement's click also counts what the
            other currency can pay where that falls BETWEEN the sixteenths: 5, 8, 10 and 11 of its units after
            each seed, softer the more coins. The full grid is given its triplet just before it empties.
  GIVEN     2 Least Common v10: the drum rests where the three and the five meet on it, and the beat is given
            to the answer (the knock, which has sounded there since v6). From the bar the first thing leaves to
            the bar the meetings leave (145 to 160) that is three beats, fifteen beats apart (bar 147 beat two,
            151 beat one, 154 beat four), and the fourth fifteen is where all three meet on the drum (bar 158:
            the chord, the triad turning over), with the drum under it: three rests count in the last meeting.

v9 (26 Nov): WITH INTEREST. Three switches (`--without-answer`, `-interest`, `-chest`; all three off is v8 byte for
byte):
  ANSWER    the hand drops the stick on the cell's last stroke (v8), and the strings nobody plays were shut in
            that same half beat: the one stroke of the cell's that is let go altogether was the one they did not
            hear. Now they hear it and its bounces, and are held open through the bar after the cell has gone
            (bar 169), then let down over the next: the cell's last note is answered by the strings that have
            its note in them (C3's fourth partial and F2's sixth are C5), and the answer is what is left of the
            cell when it is not there.
  INTEREST  Small Change's lesson of v7 (a purse that gives back more than it is given, with a hand on its fader,
            builds; shut, it is empty at once). The change's last seed (bar 144, beat 3) went to the smallest
            purse and was a held B flat that ran out. Now the purse pays interest: the note swells for the two
            beats that are left and is shut on the one of bar 145, where the change goes. A clip inside the loop
            is the purse's size: it cannot hold more than that, so the swell comes up to a level and stays.
  CHEST     nothing in this song sounds between 60 and 85 Hz: the drum is on G1 (49 Hz) with its 47 Hz taken
            down, and the bass has no fundamental (that is its illusion). Beside the album the song stood 9.6 dB
            short at 71 Hz, the one band the scorer charged it for, and aimed at as such: a bell of 4 dB at 71 Hz
            on the drum, narrow (its stroke sweeps through there; it has no note there to give the bass).

v8 (26 Nov): WHAT IS LEFT BOUNCING. Two of the seven grew once more after v7, and the closer takes the new thing
from each. Two switches (`--without-drop`, `-part`; both off is v7 byte for byte):
  DROP  4 Ring True v8. There the stick is let go too: a thing's stroke is dropped and bounces, each bounce sooner
        and softer than the last by the same share. Here the hand has taken the cell back (bars 161 to 168); on
        the cell's last stroke it lets go of the stick, and of the bar: the stroke rings as nothing of the cell's
        has for eight bars. The cell goes at bar 169 and its stick is still bouncing on a bar still ringing:
        eight bounces, each gap three quarters of the one before, and the ninth would fall on beat two of the
        bar the cell is not in. Something coming to rest by itself, which is the song.
  PART  2 Least Common v8. There the second half remembers the first: each click's echo keeps its old cycle. Here
        nobody plays the cycles at all; only their meetings are heard, as pings. Now each meeting is heard to
        part: after a ping the two cycles that met go on their way, the three's click 3 sixteenths later on the
        left, the five's 5 later on the right, the seven's 7 later in the middle (where Least Common stands
        them). They are the ping's own echoes with the note taken out (what is left of a vibraphone bar over
        1.2 kHz is its second mode, two octaves up, and its click), so Least Common's cycles are heard in the
        closer for one step each, 342 times, and nobody plays them.

v7 (26 Nov): RING TRUE. Two of the seven grew again after v6, and the closer takes the new things from each. Three
switches (`--without-true`, `-turn`, `-tame`; all off is v6 byte for byte):
  TAME  2 Least Common v7 again: the pings' commonest note, D5, 3 dB down by an EQ on their track. The strings
        sing on the cell's notes, 500 Hz to 1 kHz, where this song already stood 6.4 dB over the album's
        envelope at 547 Hz; with them it stood 6.6.
  TRUE  4 Ring True v7. There the strings nobody plays are let go while the wood closes, and go quiet by themselves
        as it is shut. Here the cell is Ring True's wooden bar; so when the room goes (bar 153) the strings are
        let go beside the cell and are what is left round it: a string answers a note only if it is one of its
        own. Then the hand takes the cell (bar 161) and drags it late, and a thing dragged late is flat: the
        strings stop answering at once, bars before the hand has shut the cell. They ring while it rings true.
        They are stopped when the cell goes, and wait for the last stroke as before.
  TURN  2 Least Common v7. There the drum's low triad turns over a page at a time. Here the drum answers the
        meetings that land on it, two notes at a time; now each time all three meet on the drum (every 105
        beats) the triad turns over: G2 B flat 2 D3, then B flat 2 D3 G3, then D3 G3 B flat 3, and round.

v6 (26 Nov): WHAT THEY LEARNT THIS AFTERNOON. Three of the seven grew again after v5 quoted them, and the closer
takes the new thing from each. Three switches on (`--without-strings`, `-paid`, `-knock`; all off is v5 byte for byte) and one off:
  KNOCK   2 Least Common v6, the drum answers. There the drum answers each click that lands on it. Here nobody
          plays the cycles, only their meetings sound; so the drum answers each MEETING that lands on it, with
          the notes of the two cycles that met (G2 for the three, B flat 2 for the five, D3 for the seven):
          two low notes every 15, 21 and 35 beats, and all three every 105.
  STRINGS 4 Ring True v6, the strings nobody plays. The click is Ring True's wooden bar, and beside it lie that
          song's five open strings (F2, G2, B flat 2, C3, D3: each a loop one period long that returns itself
          and hears only the click). They are stopped for the whole record. The last stroke, on the one, is
          G4, the fourth harmonic of the G string: as it is struck the strings are let go, and when the stroke
          has stopped the string goes on at that note by itself. The last sound on the record is a string
          nobody played.
  EARLY   (OFF, `--with-early`) the strings let go from the top of the run-down instead, answering each tick as
          it slows and sinks. By solo they stood 10 to 15 dB under the lone click there, and the scorer took
          0.4 (99.05 for 99.45): with a new sound through the last 25 seconds its boundary at bar 9, where
          nothing changed, reads 0.16 for 0.18. Off until an ear asks for it.
  PAID    6 Small Change v5, the smallest change. The change's very last seed (bar 144, beat three) is paid in
          coins of 3 and 5 of a unit that is a pitch (B flat 3's period): its change is its own note, held,
          as the change leaves.

v5 (26 Nov): TWO MORE LEAVINGS. In v3 five of the seven left as themselves; the room only had its door shut, and
the cell was damped and nothing else. Three switches (`--without-sing`, `-nudge`, `-ease`; all three off is v4
byte for byte):
  SING   3 Standing Room v6: the walls sing. In the room's last four bars two more walls come in, so near that
         they cannot be counted: a second pair of buses, each returning the click and itself, one after 10.2 ms
         and one after 6.8. An echo every 10.2 ms is not an echo, it is 98 Hz: the room, as it goes, is two
         strings that the click plucks, G on the left and the D above it on the right (the far walls are 3 and
         5 sixteenths away; the near ones 3 and 2 of something a hundred times smaller). They rise through three
         bars, stand for one, and the door shuts on them with the room's.
  NUDGE  1 Give or Take's hand: as the cell is taken back into the hand (TAKEN) the hand is felt. Over its last
         eight bars the cell is dragged late by up to a sixteenth and let catch up, d(x) = reach sin^2(pi x / T),
         and its notes go with its speed, flat while it is dragged and sharp while it catches up
         (-12 log2(1 + d') semitones on each stroke): it is in step again in the bar it leaves.
  EASE   the cell let go is 2 dB lower (7 dB off at ring 1, not 5): let go it carried 91 to 98% of 500 Hz to
         1 kHz, and 547 Hz stood 6.7 dB over the album's envelope.

Form as arithmetic: GATHER lists the things in the order they come; each comes STEP bars after the last, all are
held for HOLD bars, they go in reverse order LEAVE bars apart, and the last WIND bars are the spring running down.
"""
import argparse
import json
from math import exp, log, log10, log2, pi, sin, sqrt
from pathlib import Path

BPM, SLOW = 124, 50
S16 = 60000 / BPM / 4                       # a sixteenth, ms
BAR = 16
STEP, HOLD, LEAVE, WIND = 16, 32, 8, 8      # bars
GATHER = ['grid', 'pattern', 'ghost', 'cell', 'meetings', 'room', 'change']
COMES = {k: i * STEP for i, k in enumerate(GATHER)}
ALL = len(GATHER) * STEP                    # the bar at which everything is in
GOES = {k: ALL + HOLD + (len(GATHER) - 1 - i) * LEAVE for i, k in enumerate(GATHER)}   # last in, first out
GOES['grid'] = GOES['pattern'] + LEAVE      # the drum goes here; the click stays to the end
RUNS_DOWN = GOES['grid']
BARS = RUNS_DOWN + WIND
DRUM_IN = 8                                 # the bass drum comes eight bars after the click (and turns the listener round)
LET_GO = (ALL + HOLD // 2, ALL + HOLD)      # the cell's ring goes from STOPPED to 1 across these bars
STOPPED = 0.15                              # the cell's ring while it is gathered
ALONE = 6                                   # dB the click's fader comes up while it is alone (before the drum; as the spring runs down)
SHUT = -0.25                                # the click's: stopped sooner than Ring True stops anything (5 ms), so it is a tick and not a note
TICK, LAST = 'G6', 'G5'                     # the click's note (an octave over Give or Take's, clear of the cell and the pings); the last stroke's
CYCLES = (3, 5, 7)
PING = {(3, 5): 'D5', (3, 7): 'Bb4', (5, 7): 'F4'}
CHORD = ('G3', 'Bb3', 'D4', 'F4', 'A4')
CELL = [(3, 'D5', .8), (7, 'F5', .7), (11, 'G5', .85), (14, 'F5', .65), (19, 'D5', .8), (23, 'C5', .7), (27, 'Bb4', .85), (29, 'C5', .6)]
PATTERN = (0, 1, 3, 5, 6)                   # of eight sixteenths
GHOST = (('G1', 'G1', 'G1', 'Bb1'), ('G1', 'G1', 'G1', 'G1'), ('G1', 'G1', 'G1', 'C2'), ('G1', 'G1', 'D2', 'F2'))
WALLS = (3, 5)                              # sixteenths there and back
COINS, UP, DOWN, GIVE = (3, 5), 7, -5, 0.62
LAG = {UP: 19.7, DOWN: 23.8}                # ms the pitch effect is late (Small Change's bench)
WOOD = (0.015, 1.0)                         # the bar's ring time, seconds: stopped, let go
OUT = Path(__file__).resolve().parents[3] / 'songs/chirpers11-t8.yaml'

# ---- v2: the switches and their numbers. Nothing above is changed by them.
ON = {'catch': True, 'comp': True, 'hat': True, 'learnt': True, 'stop': True, 'tuck': True,
      'spent': True, 'held': True, 'taken': True, 'real': True, 'slip': True, 'sink': True,
      'mid': True, 'body': True, 'open': True, 'sing': True, 'nudge': True, 'ease': True, 'strings': True, 'paid': True, 'knock': True, 'early': False, 'true': True, 'turn': True, 'tame': True, 'drop': True, 'part': True, 'answer': True, 'interest': True, 'chest': True, 'exchange': True, 'rate': True, 'given': True, 'grip': True, 'choke': True, 'lead': True, 'tell': True, 'whole': True, 'left': True, 'ajar': True, 'wall': True, 'cede': True, 'clocks': True, 'linger': True, 'fifth': True, 'stand': True, 'tuned': True, 'resolve': True, 'quarters': True, 'hour': True, 'hammer': True, 'one': True, 'sympathy': True, 'groove': True, 'surface': True, 'lift': True, 'leadin': True, 'reveal': True, 'inner': True, 'spiral': False, 'preecho': True, 'nearer': True, 'pallet': True, 'exit': True, 'rumble': True, 'rundown': True, 'limp': True, 'wow': True, 'waver': True, 'tally': True, 'back': True, 'full': True, 'eleven': True, 'lands': True, 'creeps': True, 'elder': True, 'told': True, 'apart': True, 'aired': False, 'entered': True, 'counts': True, 'laid': True}
ENTERED = {'db': 0, 'trim': {}}   # v28: the rows that count the seven in: dB on a row; dB by the bar (from 1)
COUNTS = {'db': -7, 'trim': {393: 3, 415: 3}}   # v28: the big brother's own count before home: dB on a stroke (its told strokes are at -3, its strokes from home at 0); dB by beat (bar 99 beat 2 and bar 104 beat 4: at one level those two were 2.1 and 1.7 dB over the music in their band, where the other three were 4.5 to 4.8: the music has its D4 and C4 there)
LAID = {'pitch': 'Bb5', 'vel': 0.8, 'db': 0}   # v28: the stick laid down: the note of its lowest notch, touch, dB
GROOVE = {'patch': 'wd-groove', 'turn': 1.8, 'after': 1.1, 'turns': 4, 'dust': ((0, 'G2', 1.0, 0), (3, 'D4', .7, -9), (8, 'A3', .6, -14), (15, 'F4', .8, -6)),   # v20: the run-out groove: seconds a turn (33 1/3 a minute); seconds from the last stroke to the first joint; turns; what is in a turn: (sixteenths of a turn after the joint, the chip noise's note: its step rate, how hard, dB)
          'gain': '-28dB', 'pan': 0, 'ms': 4, 'hp': 180, 'lp': 2600, 'rest': 1.5}   # its fader (bench: at -24 dB the joint's highest sample stood 2 to 6 dB over the wall clock's ticks: 4 dB off) and place; a speck's length, ms; its band; seconds of the song after the last joint (the surface goes in them)
SPIRAL = {'patch': 'wd-spiral', 'gain': '-51dB', 'hp': 700, 'lp': 6000, 'in': 4, 'to': 8, 'out': 4, 'radius': (146.05, 60.3, 53.2), 'lock': 'wd-inner', 'every': 8, 'walls': 2, 'up': 4, 'down': 70}   # v21: the playing groove's surface: its patch, fader (bench, alone: at the run-out's -58 dB the white hiss stood 10 dB under the locked groove's chip noise: -78 dBFS for -68: so 7 dB up, to meet it at the first joint with INNER's 3.8) and band at the first groove (the run-out's, v20); bars over which it comes in; the bar to which it is held, and bars over which it goes, where it does not stay; an LP's first, last and locked groove, mm from the centre; the run-out surface's name when its band has slid; bars between the points of the slide's line; low-pass filters in a row at the band's top (Out of Step's last bars lie over the first eight: nothing over 10 kHz); REVEAL: bars over which it comes up again from the bar the spring runs down; dB it is down in between
RUMBLE = {'patch': 'wd-rumble', 'gain': '-32dB', 'hp': 25, 'lp': 90, 'pitch': 'C3', 'vel': 0.8, 'in': (-6,), 'from': 'joint'}   # v23: the bearing's rumble: its patch, fader (the second build's -20 dB stood 10 dB OVER the surface in the run-out: this master lifted it 13.6 dB), band, the chip noise's note (its step rate), touch, and the dB on its first turns as it comes in
PALLET = {'patch': 'wd-pallet', 'gain': '-20dB', 'hp': 10000, 'ms': 6, 'bars': (8, 144), 'vel': 0.8, 'exit': {'patch': 'wd-pallet-exit', 'gain': '-10dB', 'band': (8000, 11000), 'steep': 3, 'on': (6, 14)}}   # v23: the tooth on the pallet: its patch, fader (bench), where it begins (Hz), how long it is, the bars (from 0, to but not with) in which it is struck with the click where the drum plays, and its touch (the click's own shape is not copied: one touch)
NEARER = {'up': 9, 'lock': 6}   # v22: dB on the playing groove's surface where it comes back as the spring runs down (the lead-in in bars 1 to 8 is as it was: chirper-zero's seam), and on the locked groove's hiss
ELEVEN = {'patch': 'wd-eleven', 'gain': '-12dB', 'pan': -0.3, 'hall': None, 'from': ALL, 'beats': 11, 'of': 24.4997, 'harmonic': (11, 12), 'vel': 0.9, 'len': 1.0, 'last': 4.0,
          'echo': (-4, -7, -10), 'echo_vel': 0.6, 'echo_len': 0.5, 'bare': -9.5,
          'trim': {0: 1.5, 1: 0.8, 2: -1.3, 3: 0.8, 4: -1.2, 5: 1.0, 6: -3.0, 7: 1.9, 8: -0.3, 9: 1.5, 10: -2.1, 11: 1.2, 12: 0.3, 13: -0.1, 14: 0.6, 15: 2.7, 16: 1.0, 17: 2.6, 18: -0.3, 19: 3.5, 20: -1.6, 21: -1.7, 22: -2.1, 23: -1.7, 24: -1.6, 25: 0.2, 26: -1.9, 27: -1.2, 28: -1.4, 29: 0.9, 30: -8.6, 31: -8.6}}   # v26: the eleven: its patch, fader, place, hall (NONE: it is dry: the note is 20 dB down in 80 ms and the hall then answers at its OWN nearest pitch: sent there at -14 dB, the strokes read over 0.3 s gathered at 277, 282, 288 and 299 Hz, up to 43 cents from what was written, and the last, written 294.0, read 299.6: not home); the bar it begins in (from 0); its cycle (beats; its echo's is that many sixteenths); the G an octave under the drum's G1 (Hz) and the harmonics of it the voice begins on and comes home on (269.5 to 294 Hz: an octave under Least Common's: this song is already 5.8 dB over the album's envelope in the band at 547 Hz, and the eleven there, 6 dB under its fader here, put it 0.9 dB past the tolerance; from 250 to 292 Hz the song is 0.5 dB under); touch and length (beats) of a stroke, and of the last; dB, touch and length of its three echoes; dB on an echo that falls in the bare last bars when its stroke did not (the last full bar's stroke has its echoes after the grid has gone: at their written level they came out up to 2.1 dB OVER the two strokes that follow them); dB on a stroke by its number (from 0), and on its echoes, SET FROM A FINISHED BUILD, every stroke read (200 to 350 Hz): at one written level the first 30 came out 6.5 dB apart (-14.1 to -20.6 dBFS with the fader at -16), level with or under what else is in that band; each is written to come out level, the two in the bare last bars (the spring running down) 3 dB under, the last as it falls
ELDER = {'track': 'eleven-big', 'patch': 'wd-eleven-big', 'gain': '-10dB', 'pan': -0.3, 'hall': '-12dB', 'bars': 11, 'decay': '900ms', 'vel': 0.9, 'len': 1.5, 'told': (2, 1), 'told_db': -3, 'behind': 1, 'knock': {91: -1.9, 102: 3.5}, 'trim': {}}   # v27: the eleven's big brother: its track, patch, fader, place; AIRED: what the hall is sent (the chime's); its cycle, bars; its bar's ring; touch and length (beats); TOLD: how many of its cycles before the eleven comes it is heard, and dB on those; APART: the beats behind it at which the small eleven knocks there, and dB on that knock by its bar (from 1), SET FROM A FINISHED BUILD (200 to 350 Hz, the top of its first 60 ms): at one written level the two came out -13.1 and -18.1 dBFS: each is written to come out at -15 (the eleven's strokes at home are -12.8 to -13.8); dB on a stroke of the big bar by its bar (from 1): NONE: at one written level its eight strokes at home came out within 0.9 dB of each other over their first half second (-21.7 to -22.6 dBFS from 200 to 400 Hz; the tops of their first 60 ms are 3.0 dB apart by what each falls with) and the two told ones 1.6 and 2.7 dB under them for 3 written
ELEVEN_PATCH = {'about': "Wind Down: the eleven (v26): Least Common's fourth voice (lc-eleven) under this song's name: a low wooden bar, short (benched alone: 20 dB down in 70 ms, 40 in 140), its next mode two octaves up and 13 to 18 dB under. Its notes are written in Hz: harmonics 11 to 12 of the G an octave under the drum's; dry, each reads within 4 cents of what is written.",
                'synth': {'layers': [{'type': 'modal', 'modes': 'bar', 'decay': '260ms', 'bright': 0.35, 'strike': 0.5}], 'amp': {'a': '0.3ms', 'd': '450ms', 's': 0, 'r': '120ms'}},
                'play': {'event_stable': True, 'vel_sens': 0.5}}
TALLY = {'patch': 'wd-rasp', 'gain': '-12dB', 'notch': -2, 'first': 3, 'fall': -1.5, 'more': 0, 'pan': -0.45, 'bars': (ALL + HOLD, RUNS_DOWN), 'at': 8, 'gap': 1 / 16, 'ladder': ('D7', 'C7', 'Bb6', 'G6', 'F6', 'D6', 'C6', 'Bb5'), 'vel': (0.05, 0.85), 'len': 0.04}   # v25: the tally: its patch, fader, dB on every notch but the row's click on the beat, dB more on the notch next to the click (this master dips whatever falls in the 30 ms after the drum: at one level that notch read 3 to 5 dB under the next), dB more on each notch than on the one before it (at one level the notches did not fall away: the farther from the drum the more this master lifts them), dB more on the whole row for each notch in it (Ring True's is 1: there the more things ring the louder the song; here the song thins as they leave, and with 1 the click on the beat read -7.4 to -9.1 dBFS while six to four were here, 7 to 10 dB over what else is on that beat: with none it is the same click in every bar), place; the bars it plays in (from 0, to but not with); the sixteenth of the bar its click is on; the gap between notches (beats: a sixty-fourth); the notes from the click outwards (a step of the five notes each); touch (how much less each notch has than the one before it; the click): the same row whoever is here, cut a notch shorter each time somebody leaves; a click's length (beats)
TALLY_PATCH = {'about': "Wind Down: the tally (v25): Ring True's ninth thing (rt-rasp) under this song's name: one notch of a notched stick: a very small dry bar (six milliseconds) with two milliseconds of grit on it. Nothing in it rings.",
               'synth': {'layers': [{'type': 'modal', 'modes': 'bar', 'decay': '6ms', 'bright': 0.9, 'strike': 0.8},
                                    {'type': 'noise', 'color': 'white', 'level': {'value': '-70dB', 'mod': [{'src': 'env.burst', 'amount': 52}]}}],
                         'env': {'burst': {'a': '0.1ms', 'd': '2ms', 's': 0, 'r': '2ms'}},
                         'amp': {'a': '0.1ms', 'd': '0s', 's': 1, 'r': '20ms'}},
               'play': {'event_stable': True, 'vel_sens': 0.6}}
RUNDOWN = {'lift': 0.04, 'limp': 2, 'gain': '-20dB', 'exit': '-10dB'}   # v24: seconds of lift time where the spring's speed has halved (it is this times one over the speed, less one); how many times as far the second pallet's tooth falls (LIMP); the two teeth's faders under the last ticks (v23's own, read in the row)
WOW = {'off': 0.4, 'top': 0.25, 'chime': 'wd-chime-wow', 'hour': 'wd-hour-wow', 'held': 'wd-open-wow'}   # v24: mm the record's hole is off its centre; where in its turn the wow is at the joint (0.25: its top); the wowed bells' names
PREECHO = {'at': {15: -30, 31: -30, 47: -30, 111: -30}, 'not': ('pallet-down', 'pallet-exit-down', 'chime-q1', 'chime-q2', 'chime-q3', 'chime-q4', 'rumble', 'pallet', 'pallet-exit', 'tick', 'clock-tick', 'clock-tock', 'chime', 'hour', 'groove', 'surface', 'lift', 'spiral')}   # v22: the caught bars (from 0) whose next bar is heard a turn early, and the dB under itself at which it is (the first build had all seven at -30: the scorer's cuts at bars 64, 80 and 96, the catches' own beginnings, read 0.20 0.18 0.20 before and 0.16 0.16 0.17 with it: two sections lost at its two highest settings, structure 100 to 95.3, the total 1.08 down); the tracks that do not print through (the click and the clocks keep their own time; the run-out is not music)
SURFACE = {'patch': 'wd-surface', 'gain': '-58dB', 'hp': 700, 'lp': 6000, 'pitch': 'D3', 'vel': 0.8}   # v20: the record's surface: its fader (benched), its band, the chip noise's note (its step rate: slow enough not to come round inside a turn)
LIFT = {'patch': 'wd-lift', 'after': 0.5, 'rest': 1.0, 'pitch': 'D2', 'gain': '-22dB', 'vel': 0.8, 'ms': 90, 'speck': ('C2', 1.0, 3)}   # v20: the needle is lifted: seconds after the last joint; seconds of nothing after it; the thump's note, fader, touch and decay; the speck with it (the groove's patch: note, touch, dB)
HAMMER = {'patch': 'wd-chime-struck', 'amount': 96, 'ms': 3}   # v19: the struck bell's name; the hammer's grain of noise: its envelope's amount over -80 dB (benched: see the docstring), and how long
ONE = {'patch': 'wd-hour', 'bell': 'Bb2', 'db': 6, 'vel': 0.9, 'ring': '5s', 'strings': '-40dB'}   # v19: the hour bell's name and note; dB on its one stroke (the chime's fader is CHIME['gain']); the stroke; its ring; what Ring True's strings take of it (SYMPATHY)
CHIME = {'patch': 'wd-chime', 'gain': '-19dB', 'hall': '-12dB', 'bells': {3: 'D4', 2: 'C4', 1: 'Bb3', 5: 'F3'},   # v18: the clock's chime: its fader and what the hall is sent; its four bells by degree of B flat (Give or Take's, two octaves down)
         'changes': ((3, 2, 1, 5), (1, 3, 2, 5), (1, 2, 3, 1), (3, 1, 2, 5), (5, 2, 3, 1)), 'order': {1: (0,), 2: (1, 2), 3: (3, 4, 0), 4: (1, 2, 3, 4)},   # the Westminster quarters (chirper-zero's QUART_CHANGES); the changes rung at each quarter and at the hour
         'apart': 1, 'change': 5, 'vel': 0.7, 'ring': '2.4s', 'trim': {4: -8},   # seconds from note to note and from change to change; the stroke; the bell's ring; dB by quarter (1 to 4), read in the finished song
         'partials': [[0.5, 0.35], [1, 1.0], [1.5, 0.3], [2, 0.4], [3, 0.15], [4, 0.08]]}   # the bell's partials, ratio and level: hum, prime, fifth, octave, twelfth, double octave: no third (a church bell's minor third puts A flat on F and D flat on B flat)
TUNED = {'semis': 7}                      # v17: how far the drum's note moves while the bass is on the fifth (a fifth up: D2)
RESOLVE = {'bars': 1, 'db': 0}            # v17: how many bars of home the bass's fundamental stays under; dB on those notes
FIFTH = {'semis': -5}                     # v16: how far the bass's line moves for the second half of 'all gathered' (a fourth down: the fifth of the key, under the drum)
LINGER = {'db': {'saw': 6, 'kick': 6}}  # v15: the things whose goodbye (LEFT's strokes) also goes to the hall, and dB on those strokes there beside the dry ones
WALL = {'gain': '-20dB', 'pan': 0.5, 'hz': (3600, 3000), 'parts': ((0.014, 0.35), (0.008, 0.5), (0.0, 1.0)), 'after': 4}   # v14: the clock's fader and side (Give or Take's: -20 dB, 0.5); its two pallets, Hz; a tick's three sounds (seconds before the second, velocity); whole seconds it ticks on after the last stroke
GONE = {'to': 4, 'db': -3}              # v13: the sixteenth of the bar after a thing has gone up to which its own figure is played once more; dB on those strokes
AJAR = {'beats': 4, 'over': 0.25}       # v13: beats before the room comes at which its door is open; beats it takes to open (it was shut to open over eight)
TELL = {'from': 12, 'db': -3}           # v12: the sixteenth of a caught bar from which the newcomer's own figure is played; dB on those strokes
WHOLE = {'gain': '-6dB', 'bars': (COMES['cell'] - 1,)}   # v12: dB on the bass's own voice (harmonics two to six) under the lead's fundamental; the caught bars (from 0) it is in (first: all five; see the docstring)
GRIP = {'note': -12, 'semis': 24, 'from': '-40dB', 'patch': 'wd-grip'}   # v11: dB on the cell's note with the hand all the way down; its second mode's place above the note; that layer's level with no hand; the patch
CHOKE = {'notes': ('Bb1', 'C2')}        # v11: the drum's note in each of its last bars
LEAD = {'beats': 1, 'pitch': 'D2', 'gain': '-27dB', 'vel': .8}   # v11: beats before the one that the bass's fundamental holds; its note; its fader.
# Bench (g.sh, gread.py, raw, bar 48 by beat): at the fundamental's own fader (-21 dB) the note alone read -31.3 dBFS where the caught bar's click reads -43.2 and the groove either side -22.3: the bar's second half 12 dB over its first.
# 6 dB less: over the click and 15 under the groove (Least Common's stands 2 dB over its break; a sine at 73 Hz wants more than a click does to be heard at all).
# RENDERED IN FULL WITH TWO BEATS HELD: the scorer's sections fell from 10 to 8 at its highest cut on both seeds (structure 99.33 for 100), and with the lead out they were 10 again (first/: nl11, ng11): half a caught bar with the bass's
# band in it is half a catch. One beat: a pickup into the one, and the catch is a catch for three beats of its four
EXCHANGE = {'per': 1.5, 'back': 0.72, 'feed': '3dB', 'pan': 0.3, 'down': 8}   # v10: Small Change's exchange: how many of its units make a sixteenth; what each loop gives back a pass (the first pair's is 0.62 and its passes are half as often again); what it takes of the seed (the first pair takes 0 dB; see the bench below); how far to each side (the first pair is at 0.5); beats over which it is let down.
# Bench (xc.sh, xcread.py: the song less v9, raw, by unit from the seed of bar 141): taking -2 dB its coins read -33 and -38 on 3 and 5 units where the first pair's read -34 and -32 on 3 and 5 sixteenths, and by bar it stood 1 to 5 dB under the first pair and 18 to 22 under the mix. Taking 0 dB (rendered in full): 3 under to 2 over the first pair, still 16 to 20 under the mix, and in the finished song 0.2 to 0.5 dB on 400 Hz to 3 kHz: these are the fullest bars of the song and the change is a small thing in them. 3 dB more: for four bars the other currency is the one that is heard.
RATE = {'upto': 12, 'gain': '-9dB', 'pan': -0.2}   # v10: the largest amount the click counts (twelve units is two beats); its fader and side (the complement's are -6 dB and 0.2). Bench: at -6 dB its highest sample was -10.4 dBFS beside the complement's -11.0: a second complement, not a count behind it. 3 dB less
GIVEN = {'meet': (3, 5), 'bars': 2 * LEAVE}   # v10: the two cycles whose meeting on the drum the drum rests for; the bars before the meetings go in which it does
ANSWER = {'feed': '-29dB', 'open': 4, 'down': 4}   # v9: what the strings take of the dropped stroke and of its bounces; beats after the cell goes that they are held open; beats over which they are let down.
# Bench (int.sh, intread.py: the song less the song without the answer, raw, by half beat): at -27 dB the answer read -27 -24 -28 -29 -32 -36 -39 from the stroke through bar 169, 7.6 dB under the mix over that bar, and level with
# or over what is between the drum's beats there (-26 to -30) for two beats: 2 dB less
INTEREST = {'back': 0.737, 'feed': '-27dB', 'size': -24}   # v9: what each loop of the smallest purse gives back (0.71 ran out); what it takes of the seed (it was -13: it starts lower and comes up); the clip in the loop, dBFS.
# Bench (the seed and its purse alone by quarter beat): taking -19 dB and clipped at -22 it read -27 -30 -28 -27 -26 -26 -26 -26: up 4 dB in half a beat and then flat at its size, 1.6 dB under the whole mix: a held note, louder; not a swell.
# It comes up 2 dB a quarter beat until it is full: so 8 dB less of the seed, to be full only at the one, and a purse 2 dB smaller
CHEST = 'peak cutoff=71 q=3 gain=4dB'    # v9: on the drum.
# Bench (bars 143 to 146, raw): with q 1.5 the bell reached the drum's own note and its octave: the drum's beats read 3 dB more (-16 for -19 by quarter beat), the whole mix 1.8 dB more, and 60 to 85 Hz 3.7: a louder drum, not a chest. So q 3
DROP = {'share': 0.75, 'bounces': 8, 'rest': 7, 'ring': 1.0, 'db': 3}   # v8: each bounce's gap and level as a share of the one before; how many are heard; sixteenths from the stroke to where the next would fall; the dropped stroke's ring (let go) and dB on it.
# Bench (part.sh, partread.py: the stroke and its bounces alone by 60 ms; the mix with and without). Stopped as the hand had left it (a 28 ms tap) and 6 dB up, the stroke's highest sample was -8.5 dBFS and its bounces moved the mix 1 or 2 dB in two
# sixths of a second: a loud tap and nothing after it. Let go (it rings a second), the same bounces have a note to ring on
PART = {'side': {3: -0.45, 5: 0.45, 7: 0.0}, 'hp': {3: 1200, 5: 1200, 7: 1200}, 'gain': '4dB'}   # v8: where each cycle's click stands (Least Common's places), the high-pass that takes the ping's note out of it, the buses' fader.
# Bench: with the three's high-pass at 5 kHz, the five's at 2 kHz and the seven's at 1.2 kHz and the fader at 0 dB the clicks stood 12.4 dB under the pings and 13 to 16 under the mix from 1 to 5 kHz, and the three's was nearly nothing
# (25 under the mix from 5 to 10 kHz: a vibraphone bar has little up there). So one high-pass for all three, and 4 dB more
TAME = 'peak cutoff=587 q=3 gain=-3dB'  # v7: on the pings (Least Common's)
TRUE = {'feed': '-33dB'}                # v7: what the strings take of the cell.
# Bench, by difference (the song with them less the song without, raw): at Ring True's -30 dB they stood 9 to 11 dB under the mix in bars 153 to 160 and 6 to 7 above 300 Hz, and put 3.6 dB on the song from 500 Hz to 1 kHz there (547 Hz is 6.4 over the album's envelope already): 3 dB less
TURNED = ({3: 'G2', 5: 'Bb2', 7: 'D3'}, {3: 'Bb2', 5: 'D3', 7: 'G3'}, {3: 'D3', 5: 'G3', 7: 'Bb3'})   # v7: the triad's three positions (Least Common's)
TURN_DB = (0, -1, -2)                   # and dB on each (the same head higher stands further forward: Least Common's bench)
PAGE = 105                              # beats between two meetings of all three on the drum
KNOCK = {'notes': {3: 'G2', 5: 'Bb2', 7: 'D3'}, 'gain': '-5dB', 'hold': -10}   # v6: Least Common's knock: each cycle's note; its fader and the clip before it.
# Bench, bars 113 to 128, the 600 ms after each knock: at Least Common's -2 dB two notes at once stood 2.6 dB under this mix from 90 to 123 Hz and level with it from 123 to 200 (this song is thinner there): 3 dB less
WD_KNOCK = {'about': "Wind Down: the drum's answer when a meeting lands on it (v6, after Least Common's lc-knock): a small kettledrum head let ring 800 ms.",
            'synth': {'layers': [{'type': 'modal', 'modes': 'kettle', 'decay': '800ms', 'bright': 0.3, 'strike': 0.3}], 'amp': {'a': '0.5ms', 'd': '0s', 's': 1, 'r': '600ms'}},
            'play': {'event_stable': True, 'vel_sens': 0.4}}
STRINGS = {'strings': (('F2', 87.307, 0.3), ('G2', 97.999, 0.0), ('Bb2', 116.541, -0.3), ('C3', 130.813, 0.15), ('D3', 146.832, -0.15)),   # v6: Ring True's: note, Hz, side
           'feed': '-30dB', 'back': 0.985, 'lp': 5000, 'from': -12}   # what they take of the click; what each gives back a period; the low-pass in the loop; the dB their hand starts from
PAID = {'hz': 233.08, 'coins': (3, 5), 'back': 0.71, 'feed': '-13dB', 'pan': 0.6}   # v6: Small Change's note purse: its unit (B flat 3), its coins, what each loop gives back of itself and the other, what it takes of the seed.
# Giving back 0.70 as it does in Small Change (where it is alone) the note was 9 dB under this mix for half a bar and 22 under by the next: gone before it was heard as held. Giving back 0.71 and taking 6 dB more it is 5, 11 and 18 under by half bar and still 21 to 26 under two bars on
SING = {'walls': (('sing-l', 10.2, '-0.8dB', -0.7), ('sing-r', 6.8, '-0.5dB', 0.7)), 'bars': 4, 'from': -6, 'feed': '18dB', 'fx': ['lp cutoff=4500', 'hp cutoff=200']}   # v5: the near walls: (name, ms away: 1 / 98 Hz and 1 / 147 Hz, what each gives back of itself, side); the room's last bars; the dB their door starts at; what they take of the click.
# The feed is set by solo: a stopped click is so little that at -6 dB the walls stood 33 dB under the mix above 300 Hz in their standing bar; at 14, 10.7; at 18 (and the door from -6, not -12, so that all four bars are heard) see the round's note.
# First try, the two returning EACH OTHER as the far walls do: it did not sing (33 dB gone in 50 ms): a wall on the left hears a wall on the right through its own pan, 6.4 dB lost a pass. So each returns itself
NUDGE = {'reach': 0.25, 'bars': LEAVE}                        # v5: the hand on the cell: beats late at its latest; over its last bars
EASE = -7                                                     # v5: dB on the cell at ring 1 (it was -5)
MID = {'tick': ['peak cutoff=1568 q=1 gain=-6dB', 'peak cutoff=11000 q=0.7 gain=3dB'], 'saw': ['peak cutoff=1600 q=0.8 gain=-5dB']}   # v4
MID_ALONE = 4.5                                               # v4: dB more on the click while it is alone (with its note cut the lone click read 4.6 dB lower: -32.4 for -27.8)
BODY = 'peak cutoff=72 q=1.4 gain=5dB'                        # v4: on the drum
OPEN = {'about': "Wind Down: the meetings' last chord, opening as it dies (v4): wd-held with its low-pass at 600 Hz while the chord is held and opening two octaves over the first two and a half seconds of a six-second release.",
        'synth': {'layers': [{'wave': 'saw', 'detune': -7}, {'wave': 'saw', 'detune': 7}],
                  'filters': [{'kind': 'lp', 'cutoff': {'value': 2400, 'mod': [{'src': 'env.shut', 'amount': -2}]}, 'q': 0.8}],
                  'env': {'shut': {'a': '1ms', 'd': '0s', 's': 1, 'r': '2.5s'}},
                  'amp': {'a': '500ms', 'd': '0s', 's': 1, 'r': '6s'}}, 'play': {'event_stable': True, 'vel_sens': 0.3}}
OPEN_DB = 2                                                   # on its fader: shut at 600 Hz it stood 2 dB lower while held than wd-held did at 900
SUNK = 0.25                                                   # v3 SINK: the share of its speed left on the one: two octaves
SPENT = LEAVE // 2                                            # v3: bars before the change goes in which it spends
HELD = {'len': 4, 'gain': '-28dB', 'vel': .8}                # the last chord: beats held, its fader (at -16 it was the loudest thing in the mix, 1.5 dB under the whole)
REAL = {'bars': LEAVE // 2, 'gain': '-21dB'}                 # the bass's own fundamental: its last bars, its fader (at -13 it was 84% of everything under 60 Hz and the bars 3 dB up)
V3 = {
    'wd-held': {'about': "Wind Down: the meetings' last chord, held (v3): wd-chord's two saws under a low-pass at 900 Hz that does not open, half a second coming and three seconds going.",
                'synth': {'layers': [{'wave': 'saw', 'detune': -7}, {'wave': 'saw', 'detune': 7}], 'filters': [{'kind': 'lp', 'cutoff': 900, 'q': 0.8}],
                          'amp': {'a': '500ms', 'd': '0s', 's': 1, 'r': '3s'}}, 'play': {'event_stable': True, 'vel_sens': 0.3}},
    'wd-under': {'about': "Wind Down: the fundamental the ghost bass never had (v3): a sine at the note.",
                 'synth': {'layers': [{'wave': 'sine'}], 'amp': {'a': '6ms', 'd': '0s', 's': 1, 'r': '50ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.3}},
}
CATCHES = sorted({COMES[k] - 1 for k in GATHER[1:]} | {ALL - 1})   # the bar before each coming, and before all are gathered
LEFT = 0.2                                                    # the share of its speed the spring has left on the one, with STOP
COMP = tuple(s for s in range(8) if s not in PATTERN)        # the pattern's holes: 2, 4, 7
COMP_BARS = (ALL, ALL + HOLD)                                 # home: the hold
HAT_BARS = (ALL + HOLD, RUNS_DOWN)                            # from the first leaving to the drum's
ROW, LAYERS, COUNT, QUIET = 8, 4, 23, 0.04                    # Hearing Things' numbers: bars in a row, layers, the slowest layer's count, the softest stroke kept
LEARNT = ((2, 'D2'), (5, 'F2'), (7, 'C2'), (10, 'D2'), (13, 'F2'), (15, 'C2'))   # Standing Room's bass once it has learnt the room
LEARNT_BARS = (GOES['room'], GOES['room'] + LEAVE)
W_STOP = 2 * WIND * 4 / (1 - LEFT ** 2)                       # beats a platter would take to stop if LEFT of its speed is left after WIND bars
TUCK = 3                                                      # dB
NEW = {
    'wd-comp': {'about': "Wind Down: the complement's click (after Out of Step v2): two cycles of a saw on G5 dying in 12 ms, above 3 kHz, lifted round 10 kHz.",
                'synth': {'layers': ['saw phase=0'], 'filters': ['hp cutoff=3000', 'peak cutoff=10000 q=0.7 gain=8dB'], 'amp': {'a': '0.1ms', 'd': '12ms', 's': 0, 'r': '8ms', 'curve': 3}},
                'play': {'event_stable': True, 'vel_sens': 0.5}},
    'wd-hat': {'about': "Wind Down: the hat (after Hearing Things): the machine's hat, 28 ms, above 5 kHz, whose loudness is all velocity.",
               'synth': {'layers': [{'type': 'machine', 'machine': {'part': 'hat', 'decay': '28ms'}}], 'filters': ['hp cutoff=5000'], 'amp': {'a': '0.1ms', 'd': '0s', 's': 1, 'r': '120ms'}},
               'play': {'event_stable': True, 'vel_sens': 1.0}},
}


def slowing():
    """One row of the hat that slows down for ever (Hearing Things' risset, backwards): (beat in the row, velocity).
    Stroke n of the finest layer falls CYCLE * log2(n / n0) beats before the row's end; it belongs to every layer whose
    count it divides into, and its loudness is the sum of their windows."""
    cycle, n0, out = ROW * 4, COUNT * 2 ** (LAYERS - 1), []
    for n in range(n0, 2 * n0):
        t = cycle * log2(n / n0)
        v = sum(sin(pi * (t / cycle + j) / LAYERS) ** 2 for j in range(LAYERS) if n % 2 ** (LAYERS - 1 - j) == 0) / (LAYERS / 2)
        if v >= QUIET:
            out.append(((cycle - t) % cycle, v))
    return sorted(out)


def w_stop():
    """W_STOP, or with SINK the same for SUNK of its speed left."""
    return 2 * WIND * 4 / (1 - SUNK ** 2) if ON['sink'] else W_STOP


def speed(x):
    """The spring's speed x beats into the wind-down, as a share of full speed."""
    return sqrt(1 - 2 * x / w_stop()) if ON['stop'] else 1 + (SLOW / BPM - 1) * x / (WIND * 4)

open_amp = {'a': '0.2ms', 'd': '0s', 's': 1, 'r': '2.5s', 'curve': 1}
PATCHES = {
    'wd-wood': {'about': "Wind Down: Ring True's wooden bar (1 : 4 : 10), its ring time given by each stroke (expr.ring, seconds over 0.015), with the stick's click on its front (2 ms of noise). It is the click and the cell.",
                'synth': {'layers': [{'type': 'modal', 'modes': 'bar', 'decay': {'value': WOOD[0], 'mod': [{'src': 'expr.ring', 'amount': 1}]}, 'bright': 0.75, 'strike': 0.35},
                                     {'type': 'noise', 'color': 'white', 'level': {'value': '-80dB', 'mod': [{'src': 'env.stick', 'amount': 70}]}}],
                          'env': {'stick': {'a': '0.1ms', 'd': '2ms', 's': 0, 'r': '2ms'}}, 'amp': open_amp},
                'play': {'event_stable': True, 'vel_sens': 0.6}},
    'wd-kick': {'about': "Wind Down: the drum. The machine's bass drum on G, short.",
                'synth': {'layers': [{'type': 'machine', 'machine': {'part': 'kick', 'decay': '240ms', 'click': 0.5, 'drive': 0.2, 'punch': 20}}],
                          'amp': {'a': '0.1ms', 'd': '0s', 's': 1, 'r': '400ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.3}},
    'wd-saw': {'about': 'Wind Down: a click that is five cycles of a saw (after Out of Step): on G3 that is 51 ms.',
               'synth': {'layers': [{'wave': 'saw'}], 'filters': ['lp cutoff=9000'], 'amp': {'a': '0.1ms', 'd': '45ms', 's': 0, 'r': '6ms', 'curve': 0}},
               'play': {'event_stable': True, 'vel_sens': 0.5}},
    'wd-ghost': {'about': 'Wind Down: a bass with no fundamental (after Hearing Things): harmonics two to six of the note and nothing at the note.',
                 'synth': {'layers': [{'type': 'additive', 'partials': [[2, 1], [3, 0.85], [4, 0.6], [5, 0.42], [6, 0.3]]}],
                           'amp': {'a': '4ms', 'd': '0s', 's': 1, 'r': '40ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.3}},
    'wd-ping': {'about': 'Wind Down: what two cycles make when they meet (after Least Common): a vibraphone bar with no motor.',
                'synth': {'layers': [{'type': 'modal', 'modes': 'vibes', 'decay': '650ms', 'bright': 0.55, 'strike': 0.3}],
                          'amp': {'a': '0.3ms', 'd': '900ms', 's': 0, 'r': '200ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.5}},
    'wd-chord': {'about': 'Wind Down: what three cycles make when they meet: a short filtered chord.',
                 'synth': {'layers': [{'wave': 'saw', 'detune': -7}, {'wave': 'saw', 'detune': 7}, {'wave': 'pulse', 'level': '-8dB'}],
                           'filters': [{'kind': 'lp', 'cutoff': {'value': 500, 'mod': [{'src': 'env.f', 'amount': 2.6}]}, 'q': 1.4}],
                           'env': {'f': {'a': '1ms', 'd': '140ms', 's': 0, 'r': '80ms'}},
                           'amp': {'a': '1ms', 'd': '220ms', 's': 0, 'r': '90ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.4}},
    'wd-seed': {'about': 'Wind Down: the seed (after Small Change): a short vibraphone bar with 2 ms of noise on its front.',
                'synth': {'layers': [{'type': 'modal', 'modes': 'vibes', 'decay': '180ms', 'bright': 0.6, 'strike': 0.3},
                                     {'type': 'noise', 'color': 'white', 'level': {'value': '-80dB', 'mod': [{'src': 'env.tick', 'amount': 70}]}}],
                          'env': {'tick': {'a': '0.1ms', 'd': '2ms', 's': 0, 'r': '2ms'}},
                          'amp': {'a': '0.3ms', 'd': '250ms', 's': 0, 'r': '80ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.4}},
}


def ring_s(r):
    return WOOD[0] * (WOOD[1] / WOOD[0]) ** r


def wood(at, pitch, vel, r, ease=-5):
    """One stroke on the bar at ring r (0 stopped .. 1 let go): its ring time, and 5 dB off at ring 1 so that letting go is a swell."""
    return {'at': round(at, 4), 'len': 0.25, 'pitch': pitch, 'vel': vel, 'expr': {'ring': round(ring_s(r) - WOOD[0], 5)}, 'gain': f'{round(ease * max(r, 0), 2)}dB'}


def hand(x):
    """v5 NUDGE: x beats into the cell's last bars, how late the hand has made it (beats) and how fast that is changing (beats a beat)."""
    span = NUDGE['bars'] * 4
    return NUDGE['reach'] * sin(pi * x / span) ** 2, NUDGE['reach'] * pi / span * sin(2 * pi * x / span)


def coins_for(amount, p, q):
    """v10: the fewest coins of p and q that make an amount, or None if it cannot be paid."""
    ways = [i + (amount - i * p) // q for i in range(amount // p + 1) if (amount - i * p) % q == 0]
    return min(ways) if ways else None


def given(beat):
    """v10 GIVEN: whether the drum gives this beat (counted from the top of the song) to the answer."""
    return ON['given'] and ON['knock'] and GOES['meetings'] - GIVEN['bars'] <= beat // 4 < GOES['meetings'] and tuple(c for c in CYCLES if beat * 4 % c == 0) == GIVEN['meet']


def caught(bar):
    return ON['catch'] and bar in CATCHES


def told(bar):
    """v12: what the thing that comes after this caught bar plays of its own figure in the bar's last beat: (track, note) pairs, in time order."""
    b, nxt, last = bar * 4, bar + 1, range(TELL['from'], BAR)
    if nxt == COMES['pattern']:
        return [('saw', {'at': b + (8 + s) / 4, 'len': 0.2, 'pitch': 'G3', 'vel': .62}) for s in PATTERN if 8 + s in last]
    if nxt == COMES['ghost']:
        return [('ghost', {'at': b + s / 4, 'len': 0.45, 'pitch': GHOST[bar % 4][i], 'vel': .85}) for i, s in enumerate((2, 6, 10, 14)) if s in last]
    if nxt == COMES['cell']:
        return [('cell', wood(b + (s % BAR) / 4, pitch, vel, STOPPED, **({'ease': EASE} if ON['ease'] else {}))) for s, pitch, vel in CELL if s // BAR == bar % 2 and s % BAR in last]
    if nxt == COMES['meetings']:
        return [('ping', {'at': s / 4, 'len': 1, 'pitch': PING[m], 'vel': .75}) for s in range(bar * BAR + TELL['from'], (bar + 1) * BAR) for m in [tuple(c for c in CYCLES if s % c == 0)] if len(m) == 2]
    if nxt == COMES['change']:
        return [('seed', {'at': b + 4 - COINS[0] / 4, 'len': 0.25, 'pitch': 'Bb4', 'vel': .9})]
    if nxt == ALL and ON['comp']:
        return [('comp', {'at': b + (8 + s) / 4, 'len': 0.1, 'pitch': 'G5', 'vel': .75}) for s in COMP if 8 + s in last]
    return []


def beat_at(sec):
    """v14: the beat (from 0) at which the song is sec seconds old, on the tempo map as written: steady to RUNS_DOWN, then a straight ramp a beat (bpm against beats) through the wind-down, then the last tempo held."""
    t, b = RUNS_DOWN * 4 * 60 / BPM, RUNS_DOWN * 4
    if sec <= t or not ON['stop']:
        return sec * BPM / 60
    for x in range(WIND * 4):
        v0, v1 = BPM * speed(x), BPM * speed(x + 1)
        k = v1 - v0                                             # bpm a beat
        dt = 60 * log(v1 / v0) / k
        if sec <= t + dt:
            return b + x + v0 / k * (exp(k * (sec - t) / 60) - 1)
        t += dt
    return b + WIND * 4 + (sec - t) * BPM * speed(WIND * 4) / 60


def groove():
    """v20 GROOVE: the run-out groove's notes: in each turn the joint and its dust, the same every turn; and the joint once more."""
    t0 = clock(BARS) + GROOVE['after']
    out = []
    for k in range(GROOVE['turns'] + 1):
        for u, pitch, vel, db in GROOVE['dust'][:None if k < GROOVE['turns'] else 1]:
            t = t0 + (k + u / 16) * GROOVE['turn']
            out.append({'at': round(beat_at(t), 5), 'len': round(beat_at(t + GROOVE['ms'] / 1000) - beat_at(t), 5), 'pitch': pitch, 'vel': vel, **({'gain': f'{db}dB'} if db else {})})
    return out


def lifted():
    """v20 LIFT: the second at which the needle is lifted (None: it is not)."""
    return clock(BARS) + GROOVE['after'] + GROOVE['turns'] * GROOVE['turn'] + LIFT['after'] if ON['lift'] and ON['groove'] and ON['stop'] else None


def inner(sec=None):
    """v21 INNER: the needle's radius over the first groove's at second sec of the record (None: in the locked groove): what the surface's band is multiplied by. The spiral has an even pitch: the radius falls evenly from the first bar to the run-out's first joint."""
    r0, r1, lock = SPIRAL['radius']
    if not ON['inner']:
        return 1.0
    return lock / r0 if sec is None else (r0 + (r1 - r0) * min(max(sec / (clock(BARS) + GROOVE['after']), 0), 1)) / r0


def second_at(beat):
    """v24: the second at which the song reaches a beat, on the tempo map as written: beat_at turned round, by halving (clock() is the platter's own curve, which the map follows a beat at a time: the two are 10 ms apart at the last click)."""
    lo, hi = 0.0, clock(BARS) + 60
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if beat_at(mid) < beat else (lo, mid)
    return (lo + hi) / 2


def lift_time(at, second=False):
    """v24 RUNDOWN: seconds from a click of the wind-down (at beat `at`) to its tooth: the lift time, which grows as the spring's speed falls; LIMP: twice that on the second pallet."""
    return RUNDOWN['lift'] * (1 / speed(at - RUNS_DOWN * 4) - 1) * (RUNDOWN['limp'] if second and ON['limp'] else 1)


def wow_cents(sec):
    """v24 WOW: how far each way, in cents, the pitch wavers at second sec of the record: the hole's offset over the needle's radius (which falls evenly to the run-out's first joint)."""
    r0, r1, _ = SPIRAL['radius']
    return 1200 * log2(1 + WOW['off'] / (r0 + (r1 - r0) * min(max(sec / (clock(BARS) + GROOVE['after']), 0), 1)))


def wow_patch(patch, sec, text):
    """v24 WOW: a bell with the record's wow at second sec: its pitch on an oscillator that runs on song time, once a turn, at its top at every joint of the run-out."""
    joint = clock(BARS) + GROOVE['after']
    return {**patch, 'about': patch['about'] + text,
            'synth': {**patch['synth'], 'pitch': {'value': 0, 'mod': [{'src': 'lfo.wow', 'amount': round(wow_cents(sec) / 100, 4)}]},
                      'lfo': {**patch['synth'].get('lfo', {}), 'wow': {'wave': 'sine', 'rate': round(1 / GROOVE['turn'], 5), 'phase': round((WOW['top'] - joint / GROOVE['turn']) % 1, 4)}}}}


def run_out():
    """v20: the second at which the song ends: LIFT['rest'] after the needle is lifted, or GROOVE['rest'] after the groove's last joint; without the groove, where it ended (four beats after the last stroke)."""
    if lifted():
        return lifted() + LIFT['rest']
    return clock(BARS) + GROOVE['after'] + GROOVE['turns'] * GROOVE['turn'] + GROOVE['rest'] if ON['groove'] and ON['stop'] else None


def wall():
    """v14: the wall clock's notes, (tick's, tock's): three a tick, at every whole second from the bar the drum goes to WALL['after'] seconds past the last stroke."""
    first, last = int(clock(RUNS_DOWN)) + 1, int(clock(BARS)) + WALL['after']
    secs = (caught_seconds() if ON['clocks'] else []) + list(range(first, last + 1))
    return tuple([{'at': round(beat_at(sec - early), 5), 'len': 0.05, 'pitch': 'C6', 'vel': vel} for sec in secs if (sec - first) % 2 == pallet for early, vel in WALL['parts']] for pallet in (0, 1))


def caught_seconds():
    """v15: the whole seconds of the song that fall in a caught bar (the tempo is whole and steady there: second s is in bar b when 240 b <= s BPM < 240 (b + 1))."""
    return [s for b in (CATCHES if ON['catch'] else []) for s in range(240 * b // BPM, 240 * (b + 1) // BPM + 1) if 240 * b <= s * BPM < 240 * (b + 1)]


def moved(pitch, semis):
    """v16: a note name moved by semitones (flats for the black keys, as the song writes them)."""
    names = ('C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B')
    n = names.index(pitch[:-1]) + 12 * int(pitch[-1]) + semis
    return f'{names[n % 12]}{n // 12}'


def on_the_fifth(bar):
    """v16 FIFTH: is the bass on the fifth in this bar? The second half of 'all gathered': from half way between everything being in and the first thing going, to the first thing going."""
    return ON['fifth'] and (ALL + GOES['change']) // 2 <= bar < GOES['change']


def chimes():
    """v18: the clock's chime, as (quarter, second, degree): quarter q of the song begins at bar q * RUNS_DOWN / 4 (the fourth is the hour, where the spring runs down); its first note is on the first whole second after that bar line, then one every CHIME['apart'] seconds, a change every CHIME['change']."""
    return [(q, int(clock(q * RUNS_DOWN // 4)) + 1 + i * CHIME['change'] + j * CHIME['apart'], deg)
            for q in (1, 2, 3, 4) if ON['hour' if q == 4 else 'quarters'] for i, c in enumerate(CHIME['order'][q]) for j, deg in enumerate(CHIME['changes'][c])]


def chime_patch(ring=None, about=None):
    """v18: the clock's bell. v19: with a hammer on its front (HAMMER); `ring` and `about` make the hour bell of it (ONE)."""
    text = "Wind Down: the chime of the clock on the wall (v18). A bell with no third: six partials (hum, prime, fifth, octave, twelfth, double octave), so every partial of every bell is a note of the song's scale; the higher ones die sooner. Four of them ring Give or Take's quarters (chirper-zero's tune) two octaves under that clock's bars: the pitch they would have at the quarter speed this song stops at."
    synth = {'layers': [{'type': 'additive', 'partials': CHIME['partials'], 'tilt': 0, 'damp': 0.5}], 'amp': {'a': '0.5ms', 'd': ring or CHIME['ring'], 's': 0, 'r': ring or CHIME['ring']}}
    if ON['hammer']:
        synth = {'layers': synth['layers'] + [{'type': 'noise', 'color': 'white', 'level': {'value': '-80dB', 'mod': [{'src': 'env.hammer', 'amount': HAMMER['amount']}]}}],
                 'env': {'hammer': {'a': '0.1ms', 'd': f"{HAMMER['ms']}ms", 's': 0, 'r': f"{HAMMER['ms']}ms"}}, 'amp': synth['amp']}
        text += f" v19: it is struck: a hammer, {HAMMER['ms']} ms of noise on its front."
    return {'about': about or text, 'synth': synth, 'play': {'event_stable': True, 'vel_sens': 0.4}}


def left(bar):
    """v13: what a thing that went with the bar line before this bar plays of its own figure in this bar's first beat: (track, note) pairs, in time order."""
    b, first, out = bar * 4, range(GONE['to']), []
    if bar == GOES['ghost']:
        out += [(tr, {'at': b + s / 4, 'len': 0.45, 'pitch': GHOST[bar % 4][i], 'vel': .85}) for i, s in enumerate((2, 6, 10, 14)) if s in first for tr in (('ghost', 'under') if ON['real'] else ('ghost',))]
    if bar == GOES['pattern']:
        out += [('saw', {'at': b + s / 4, 'len': 0.2, 'pitch': 'G3', 'vel': .8 if s == 0 else .62}) for s in PATTERN if s in first]
    if bar == RUNS_DOWN:
        out += [('kick', {'at': b, 'len': 0.5, 'pitch': 'G1', 'vel': .95})]
    return out


def here(thing, bar):
    return COMES[thing] <= bar < GOES[thing] and not caught(bar)


def eleven_hz(k, n):
    """v26: the eleven's k-th stroke of n + 1 (from 0), Hz: LANDS: the last on the twelfth harmonic; CREEPS: each a step nearer."""
    lo, hi = ELEVEN['harmonic']
    h = lo + (hi - lo) * k / n if ON['creeps'] and ON['lands'] else hi if ON['lands'] and k == n else lo
    return ELEVEN['of'] * h


def elder_notes():
    """v27 ELDER: the eleven's big brother: on the bar line every ELDER['bars'] bars from the bar all are gathered to the last stroke: every fourth stroke of the eleven, at that stroke's pitch. TOLD: and on the bar lines that many of its cycles before, at the first stroke's pitch (never in a caught bar)."""
    first, strokes = ELEVEN['from'], (BARS - ELEVEN['from']) * 4 // ELEVEN['beats']
    out = []
    for k in sorted([-x for x in ELDER['told']] if ON['told'] else []) + list(range((BARS - first) // ELDER['bars'] + 1)):
        bar = first + k * ELDER['bars']
        if bar < 0 or bar > BARS or (k < 0 and caught(bar)):
            continue
        db = ELDER['trim'].get(bar + 1, 0) + (ELDER['told_db'] if k < 0 else 0)
        out.append({'at': bar * 4, 'len': ELEVEN['last'] if bar == BARS else ELDER['len'], 'pitch': f"{eleven_hz(max(0, k) * ELDER['bars'] * 4 // ELEVEN['beats'], strokes):.2f}hz", 'vel': ELDER['vel'], **({'gain': f'{db:g}dB'} if db else {})})
    return out


def elder_patch():
    """v27 ELDER: the eleven's bar let ring: Least Common's lc-eleven-big under this song's name, its notes written in Hz."""
    return {'about': "Wind Down: the eleven's big brother (v27): Least Common's lc-eleven-big under this song's name: the eleven's low wooden bar let ring. Its notes are written in Hz, the eleven's own: harmonics 11 to 12 of the G an octave under the drum's: 269.5 Hz, the pitch it has in Least Common, to 294.0 on the last stroke.",
            'synth': {'layers': [{'type': 'modal', 'modes': 'bar', 'decay': ELDER['decay'], 'bright': 0.35, 'strike': 0.5}], 'amp': {'a': '0.3ms', 'd': '0s', 's': 1, 'r': '300ms'}},
            'play': {'event_stable': True, 'vel_sens': 0.5}}


def eleven_notes():
    """v26 ELEVEN: a stroke every ELEVEN['beats'] beats from the bar all are gathered to the last stroke, three echoes after each (none after the last)."""
    first, n = ELEVEN['from'] * 4, (BARS - ELEVEN['from']) * 4 // ELEVEN['beats']
    out = []
    if ON['apart'] and ON['told'] and ON['elder']:              # v27 APART: where the big brother is told, the small one is a beat behind it, as in Least Common
        for q in elder_notes():
            if q['at'] < first:
                db = ELDER['knock'].get(round(q['at'] / 4) + 1, 0)
                out.append({'at': q['at'] + ELDER['behind'], 'len': ELEVEN['len'], 'pitch': q['pitch'], 'vel': ELEVEN['vel'], **({'gain': f'{db:g}dB'} if db else {})})
    for k in range(n + 1):
        at, pitch = first + k * ELEVEN['beats'], f'{eleven_hz(k, n):.2f}hz'
        if at > BARS * 4:
            break
        trim = ELEVEN['trim'].get(k, 0)
        out.append({'at': at, 'len': ELEVEN['last'] if at == BARS * 4 else ELEVEN['len'], 'pitch': pitch, 'vel': ELEVEN['vel'], **({'gain': f'{trim:g}dB'} if trim else {})})
        for j, db in enumerate(ELEVEN['echo'], 1):
            if at + j * ELEVEN['beats'] / 4 < BARS * 4:
                bare = ELEVEN['bare'] if at < RUNS_DOWN * 4 <= at + j * ELEVEN['beats'] / 4 else 0
                out.append({'at': at + j * ELEVEN['beats'] / 4, 'len': ELEVEN['echo_len'], 'pitch': pitch, 'vel': ELEVEN['echo_vel'], 'gain': f'{db + trim + bare:g}dB'})
    return out


def elder_count():
    """v28 COUNTS: between its first told stroke and home the big brother counts its own eleven softly: its bar again every ELEVEN['beats'] beats (not on its own strokes, not in a caught bar), at the first stroke's pitch."""
    if not (ON['counts'] and ON['told'] and ON['elder']):
        return []
    own, home = {q['at'] for q in elder_notes()}, ELEVEN['from'] * 4
    out = []
    for at in range(min(own) + ELEVEN['beats'], home, ELEVEN['beats']):
        if at in own or caught(at // 4):
            continue
        db = COUNTS['db'] + COUNTS['trim'].get(at, 0)
        out.append({'at': at, 'len': ELDER['len'], 'pitch': f"{eleven_hz(0, (BARS - ELEVEN['from']) * 4 // ELEVEN['beats']):.2f}hz", 'vel': ELDER['vel'], **({'gain': f'{db:g}dB'} if db else {})})
    return out


def entered_notes():
    """v28 ENTERED: each of the seven is counted in as it comes: a row in the bar it comes (not the first: the grid is the click itself), a notch for each one here; the row CLIMBS to its click (the notches before it). LAID: one tap of the lowest notch in the bar after the last row."""
    out = []
    for k in GATHER if ON['entered'] else []:
        bar = COMES[k]
        if bar == 0 or caught(bar):
            continue
        n = tally_count(bar)
        for j in range(n + 1):
            db = (TALLY['notch'] + TALLY['fall'] * (j - 1) + (TALLY['first'] if j == 1 else 0) if j else 0) + ENTERED['db'] + ENTERED['trim'].get(bar + 1, 0)
            out.append({'at': round(bar * 4 + TALLY['at'] / 4 - j * TALLY['gap'], 4), 'len': TALLY['len'], 'pitch': TALLY['ladder'][j], 'vel': round(TALLY['vel'][1] - TALLY['vel'][0] * j, 3), **({'gain': f'{db:g}dB'} if db else {})})
    if ON['laid']:
        out.append({'at': TALLY['bars'][1] * 4 + TALLY['at'] / 4, 'len': TALLY['len'], 'pitch': LAID['pitch'], 'vel': LAID['vel'], **({'gain': f"{LAID['db']:g}dB"} if LAID['db'] else {})})
    return out


def tally_count(bar):
    """v25 TALLY: how many of the seven are still here in a bar."""
    return sum(1 for k in GATHER if COMES[k] <= bar < GOES[k])


def tally_notes():
    """v25 TALLY: a row a bar: its click on TALLY['at'], and a notch for each one still here; BACK: the notches after the click, falling (without it before the click, climbing to it, as in Ring True)."""
    out = []
    for bar in range(TALLY['bars'][0] - (1 if ON['full'] else 0), TALLY['bars'][1]):   # v25 FULL: and once in the bar before the first one leaves
        if caught(bar):
            continue
        n = tally_count(bar)
        for j in range(n + 1):
            db = (TALLY['notch'] + TALLY['fall'] * (j - 1) + (TALLY['first'] if j == 1 else 0) if j else 0) + TALLY['more'] * n
            out.append({'at': round(bar * 4 + TALLY['at'] / 4 + (j if ON['back'] else -j) * TALLY['gap'], 4), 'len': TALLY['len'], 'pitch': TALLY['ladder'][j],
                        'vel': round(TALLY['vel'][1] - TALLY['vel'][0] * j, 3), **({'gain': f'{db:g}dB'} if db else {})})
    return sorted(out, key=lambda x: x['at'])


def build():
    T = {k: [] for k in ('kick', 'tick', 'saw', 'ghost', 'cell', 'ping', 'chord', 'seed', 'comp', 'hat', 'held', 'under')}
    if ON['paid']:
        T['paid'] = []
    if ON['knock']:
        T['knock'] = []
    if ON['rate'] and ON['exchange'] and ON['spent'] and ON['comp']:
        T['rate'] = []
    if ON['lead'] and ON['catch']:
        T['lead'] = []
    for bar in range(BARS):
        b = bar * 4
        down = bar >= RUNS_DOWN
        # from 1: the grid. The click is there from the first bar to the last; in the last WIND bars it is let ring more each bar.
        r = SHUT + (1 - SHUT) * (bar - RUNS_DOWN + 1) / (WIND + 1) if down else SHUT
        for s in (2, 6, 10, 14):
            T['tick'].append(wood(b + s / 4, TICK, .8 if s in (2, 10) else .7, r))
            if ON['sink'] and ON['stop'] and down:            # the note sinks with the speed
                T['tick'][-1]['expr']['sink'] = round(12 * log2(speed((bar - RUNS_DOWN) * 4 + s / 4)), 2)
        if DRUM_IN <= bar < RUNS_DOWN and not caught(bar):
            for beat in range(4):
                if given(b + beat):                             # v10: the beat is the answer's
                    continue
                if ON['cede'] and ON['left'] and beat == 0 and any(tr != 'kick' for tr, _ in left(bar)):   # v14 CEDE: the one is the leaver's
                    continue
                T['kick'].append({'at': b + beat, 'len': 0.5, 'pitch': CHOKE['notes'][bar - (RUNS_DOWN - len(CHOKE['notes']))] if ON['choke'] and bar >= RUNS_DOWN - len(CHOKE['notes']) else moved('G1', TUNED['semis']) if ON['tuned'] and on_the_fifth(bar) else 'G1', 'vel': .95 if beat == 0 else .88})
        if 'lead' in T and caught(bar) and bar > COMES['ghost']:   # v11 LEAD: the bass comes back before the drum
            T['lead'].append({'at': b + 4 - LEAD['beats'], 'len': LEAD['beats'], 'pitch': LEAD['pitch'], 'vel': LEAD['vel']})
            if ON['whole'] and bar in WHOLE['bars']:            # v12 WHOLE: the bass's own voice with it: whole for a beat
                T['ghost'].append({'at': b + 4 - LEAD['beats'], 'len': LEAD['beats'], 'pitch': LEAD['pitch'], 'vel': LEAD['vel'], 'gain': WHOLE['gain']})
        for tr, n in (told(bar) if ON['tell'] and caught(bar) else []):   # v12 TELL: the catch says who is coming
            T[tr].append({**n, 'gain': f"{round(float(n.get('gain', '0dB')[:-2]) + TELL['db'], 2)}dB"})
        for tr, n in (left(bar) if ON['left'] else []):          # v13 LEFT: the bar after says who has left
            T[tr].append({**n, 'gain': f"{round(float(n.get('gain', '0dB')[:-2]) + GONE['db'], 2)}dB"})
            if ON['linger'] and tr in LINGER['db']:              # v15 LINGER: and the hall keeps it
                T.setdefault(tr + '-gone', []).append({**n, 'gain': f"{round(float(n.get('gain', '0dB')[:-2]) + GONE['db'] + LINGER['db'][tr], 2)}dB"})
        if here('pattern', bar):
            slip = (bar - (GOES['pattern'] - LEAVE) + 1) % 8 if ON['slip'] and bar >= GOES['pattern'] - LEAVE else 0
            for half in (0, 8):
                for s in PATTERN:
                    T['saw'].append({'at': b + (half + (s + slip) % 8) / 4, 'len': 0.2, 'pitch': 'G3', 'vel': .8 if s == 0 else .62})
        if here('ghost', bar) and ON['learnt'] and LEARNT_BARS[0] <= bar < LEARNT_BARS[1]:
            for s, pitch in LEARNT:                          # the room has gone: the bass plays what it learnt of it
                T['ghost'].append({'at': b + s / 4, 'len': 0.45, 'pitch': pitch, 'vel': .88 if s == 2 else .8})
        elif here('ghost', bar):
            for i, s in enumerate((2, 6, 10, 14)):
                T['ghost'].append({'at': b + s / 4, 'len': 0.45, 'pitch': moved(GHOST[bar % 4][i], FIFTH['semis']) if on_the_fifth(bar) else GHOST[bar % 4][i], 'vel': .85})
                if ON['stand'] and ON['real'] and on_the_fifth(bar):     # v16 STAND: on the fifth the bass is whole
                    T['under'].append(dict(T['ghost'][-1]))
                if ON['resolve'] and ON['stand'] and ON['real'] and ON['fifth'] and GOES['change'] <= bar < GOES['change'] + RESOLVE['bars']:   # v17 RESOLVE: and for its first bar home
                    T['under'].append({**T['ghost'][-1], **({'gain': f"{RESOLVE['db']}dB"} if RESOLVE['db'] else {})})
                if ON['real'] and bar >= GOES['ghost'] - REAL['bars']:
                    T['under'].append({'at': b + s / 4, 'len': 0.45, 'pitch': GHOST[bar % 4][i], 'vel': .85})
        if ON['comp'] and COMP_BARS[0] <= bar < COMP_BARS[1]:
            for half in (0, 8):
                for s in COMP:
                    T['comp'].append({'at': b + (half + s) / 4, 'len': 0.1, 'pitch': 'G5', 'vel': .75})
        if ON['hat'] and HAT_BARS[0] <= bar < HAT_BARS[1] and (bar - HAT_BARS[0]) % ROW == 0 and bar + ROW <= HAT_BARS[1]:
            T['hat'] += [{'at': round(b + t, 4), 'len': 0.1, 'pitch': 'A5', 'vel': round(v, 3)} for t, v in slowing()]
        if here('cell', bar):
            lo, hi = LET_GO
            r = STOPPED if bar < lo else 1 if bar >= hi else STOPPED + (1 - STOPPED) * (bar - lo) / (hi - lo)
            if ON['taken'] and bar >= GOES['cell'] - LEAVE:    # taken back into the hand: stopped again by its last bar
                r = 1 - (1 - STOPPED) * (bar - (GOES['cell'] - LEAVE) + 1) / LEAVE
            for s, pitch, vel in CELL:
                if s // BAR == bar % 2:
                    T['cell'].append(wood(b + (s % BAR) / 4, pitch, vel, r, **({'ease': EASE} if ON['ease'] else {})))
                    if ON['grip'] and ON['taken'] and bar >= GOES['cell'] - LEAVE:   # v11 GRIP: the hand on the bar's middle: an equal-power pair
                        x = (bar - (GOES['cell'] - LEAVE) + 1) / LEAVE
                        T['cell'][-1]['expr'].update(note=round(10 * log10(1 - (1 - 10 ** (GRIP['note'] / 10)) * x), 2), mode=round(-float(GRIP['from'][:-2]) + 10 * log10(x), 2))
                    if ON['nudge'] and bar >= GOES['cell'] - NUDGE['bars']:   # the hand: late, and its note with its speed
                        late, rate = hand((bar - (GOES['cell'] - NUDGE['bars'])) * 4 + (s % BAR) / 4)
                        T['cell'][-1]['at'] = round(T['cell'][-1]['at'] + late, 4)
                        T['cell'][-1]['expr']['sink'] = round(-12 * log2(1 + rate), 2)
            if ON['drop'] and bar == GOES['cell'] - 1:         # v8 DROP: the cell's last stroke goes by a track of its own, so that only it bounces
                n = T['cell'].pop()
                let = wood(n['at'], n['pitch'], n['vel'], DROP['ring'], **({'ease': EASE} if ON['ease'] else {}))   # let go, where the hand had it stopped
                T['cell-drop'] = [{**let, 'expr': {**{k: v for k, v in n['expr'].items() if k not in ('note', 'mode')}, 'ring': let['expr']['ring']}, 'gain': f"{round(float(let['gain'][:-2]) + DROP['db'], 2)}dB"}]
        if here('meetings', bar):
            for s in range(bar * BAR, (bar + 1) * BAR):          # the cycles are counted from the top of the song; nobody plays them
                meet = tuple(c for c in CYCLES if s % c == 0)
                if len(meet) == 2:
                    T['ping'].append({'at': s / 4, 'len': 1, 'pitch': PING[meet], 'vel': .75})
                elif len(meet) == 3:
                    T['chord'].append({'at': s / 4, 'len': 0.5, 'pitch': ','.join(CHORD), 'vel': .8})
                if ON['knock'] and len(meet) >= 2 and s % 4 == 0:   # v6 KNOCK: a meeting on the drum
                    pos = (s // 4 // PAGE - COMES['meetings'] * 4 // PAGE) % len(TURNED) if ON['turn'] else 0   # v7 TURN: how many times all three have met on the drum since the meetings came
                    T['knock'].append({'at': s / 4, 'len': 0.5, 'pitch': ','.join((TURNED[pos] if ON['turn'] else KNOCK['notes'])[c] for c in meet), 'vel': .8,
                                       **({'gain': f'{TURN_DB[pos]}dB'} if ON['turn'] and TURN_DB[pos] else {})})
        spending = ON['spent'] and here('change', bar) and bar >= GOES['change'] - SPENT
        if here('change', bar) and ((bar - COMES['change']) % 2 == 0 or spending):
            T['seed'].append({'at': b, 'len': 0.25, 'pitch': 'Bb4', 'vel': .9})
            if spending and 'rate' in T:                        # v10 RATE: what the other currency can pay of this seed, between the sixteenths
                T['rate'] += [{'at': round(b + a / (4 * EXCHANGE['per']), 4), 'len': 0.1, 'pitch': 'G5', 'vel': round(.8 - .13 * (coins_for(a, *COINS) - 1), 2)}
                              for a in range(1, RATE['upto'] + 1) if coins_for(a, *COINS) and (a / EXCHANGE['per']) % 1]
            if spending and bar == GOES['change'] - 1:
                T['paid' if ON['paid'] else 'seed'].append({'at': b + 2, 'len': 0.25, 'pitch': 'Bb4', 'vel': .9})   # v6 PAID: the very last seed goes to the smallest purse
        if ON['held'] and bar == GOES['meetings']:
            T['held'].append({'at': b, 'len': HELD['len'], 'pitch': ','.join(CHORD), 'vel': HELD['vel']})
    # the final stroke: the click, let go altogether, on the one
    T['tick'].append(wood(BARS * 4, LAST, .9, 1))
    T['tick'][-1]['gain'] = '0dB'
    if ON['sink'] and ON['stop']:                             # the last stroke is where the sinking has got to
        T['tick'][-1].update(pitch=TICK)
        T['tick'][-1]['expr']['sink'] = round(12 * log2(SUNK), 2)
    return T


def door(thing):
    """A bus fader that is shut (-60 dB) until its thing comes, open while it is here, and shut again over two bars as it goes."""
    a, z = COMES[thing] * 4, GOES[thing] * 4
    if ON['ajar'] and thing == 'room':                         # v13 AJAR: the door opens in the last beat before the room comes
        return {'points': [['0b', -60], [f"{a - AJAR['beats'] - AJAR['over']}b", -60], [f"{a - AJAR['beats']}b", 0], [f'{z}b', 0], [f'{z + 8}b', -60], [f'{BARS * 4}b', -60]], 'curve': 0}
    return {'points': [['0b', -60]] + ([[f'{a - 8}b', -60]] if a >= 8 else []) + [[f'{a}b', 0], [f'{z}b', 0], [f'{z + 8}b', -60], [f'{BARS * 4}b', -60]], 'curve': 0}


def near():
    """v5 SING: the near walls' door: shut until the room's last bars, up from SING['from'] dB to 0 by its last bar, and shut with the room's."""
    a, z = (GOES['room'] - SING['bars']) * 4, GOES['room'] * 4
    return {'points': [['0b', -60], [f'{a - 1}b', -60], [f'{a}b', SING['from']], [f'{z - 4}b', 0], [f'{z}b', 0], [f'{z + 8}b', -60], [f'{BARS * 4}b', -60]], 'curve': 0}


def alone():
    """The click's fader ride: ALONE dB before the drum comes, 0 while anything else plays, back up over the first bar of the wind-down."""
    a, z = DRUM_IN * 4, RUNS_DOWN * 4
    low = ALONE + (TUCK if ON['tuck'] else 0)
    up = low + (MID_ALONE if ON['mid'] else 0)                # v4: the lone click stands where it stood before its note was cut
    pts = [['0b', up], [f'{a - 0.5}b', up], [f'{a}b', 0]]
    for bar in (CATCHES if ON['catch'] else []):              # the click is alone in a caught bar too
        pts += [[f'{bar * 4 - 0.25}b', 0], [f'{bar * 4}b', up], [f'{bar * 4 + 3.5}b', up], [f'{bar * 4 + 4}b', 0]]
    # as the spring runs down the note sinks out of the cut, so what was added for it is taken off again by the last stroke
    return {'points': pts + [[f'{z}b', 0], [f'{z + 4}b', up]] + ([[f'{BARS * 4}b', low]] if up != low else []) + [[f'{BARS * 4 + 4}b', low]], 'curve': 0}


def song():
    T = build()
    db = lambda x: f'{20 * log10(x):.2f}dB'
    under = {'type': 'pump', 'on': 'kick', 'depth': '-4dB', 'release': '170ms'}
    hold = lambda d: f'clip drive=0dB ceiling={d}dB'
    buses = {'hall': {'fx': ['reverb kind=hall decay=3.2s mix=1 predelay=25ms', 'hp cutoff=350', 'lp cutoff=6000']}}
    for me, you, n, side in (('wall-l', 'wall-r', WALLS[0], -0.7), ('wall-r', 'wall-l', WALLS[1], 0.7)):
        buses[me] = {'pan': side, 'gain': {'value': '0dB', 'mod': [{'src': 'auto.door', 'amount': 1}]}, 'auto': {'door': door('room')},
                     'fx': ['lp cutoff=4500', 'hp cutoff=300'],
                     'returns': [{'from': 'tick', 'gain': '-4dB', 'time': f'{n}/16'}, {'from': you, 'gain': '-3dB', 'time': f'{n}/16'}]}
    for me, you, n, semi, side in (('coin-up', 'coin-down', COINS[0], UP, -0.5), ('coin-down', 'coin-up', COINS[1], DOWN, 0.5)):
        t = f'{n * S16 - LAG[semi]:.2f}ms'
        buses[me] = {'pan': side, 'fx': [{'type': 'pitch', 'semitones': semi, 'mix': 1}, 'lp cutoff=10000', 'hp cutoff=150'],
                     'returns': [{'from': 'seed', 'gain': '0dB', 'time': t}, {'from': me, 'gain': db(GIVE), 'time': t}, {'from': you, 'gain': db(GIVE), 'time': t}]}
    if ON['exchange'] and ON['spent']:                         # v10: the same seeds in another currency, for the bars the change spends in
        a, z, u = (GOES['change'] - SPENT) * 4, GOES['change'] * 4, S16 / EXCHANGE['per']
        hand = {'points': [['0b', -60], [f'{a - 0.05}b', -60], [f'{a}b', 0], [f'{z}b', 0], [f"{z + EXCHANGE['down']}b", -60], [f'{BARS * 4}b', -60]], 'curve': 0}
        for me, you, n, semi, side in (('xcoin-up', 'xcoin-down', COINS[0], UP, -EXCHANGE['pan']), ('xcoin-down', 'xcoin-up', COINS[1], DOWN, EXCHANGE['pan'])):
            t = f'{n * u - LAG[semi]:.2f}ms'
            buses[me] = {'pan': side, 'gain': {'value': '0dB', 'mod': [{'src': 'auto.hand', 'amount': 1}]}, 'auto': {'hand': hand},
                         'fx': [{'type': 'pitch', 'semitones': semi, 'mix': 1}, 'lp cutoff=10000', 'hp cutoff=150'],
                         'returns': [{'from': 'seed', 'gain': EXCHANGE['feed'], 'time': t}, {'from': me, 'gain': db(EXCHANGE['back']), 'time': t}, {'from': you, 'gain': db(EXCHANGE['back']), 'time': t}]}
    end = BARS * 4
    doc = {
        'about': "Chirpers, Escapement, track 8: Wind Down, by chirper-one. Generated by compose/chirpers11/src/chirpers11-t8.py (its docstring is the rule). The closer: one thing from each of the other seven songs, gathered a section at a time on one grid in G minor, held, and let go one at a time until the click that opened the record is alone; then the tempo runs down from 124 to 50 and the last stroke, let ring, lands on the one.",
        'meta': {'artist': 'chirpers', 'album': 'Escapement', 'title': 'Wind Down', 'track': 8, 'year': 2026},
        'tempo': [{'at': '0b', 'bpm': BPM}, {'at': f'{RUNS_DOWN * 4}b', 'bpm': BPM}] +
                 ([{'at': f'{RUNS_DOWN * 4 + x}b', 'bpm': round(BPM * speed(x), 3), 'ramp': True} for x in range(1, WIND * 4 + 1)] if ON['stop'] else
                  [{'at': f'{end}b', 'bpm': SLOW, 'ramp': True}]),
        'seed': 1, 'event_stable': True, 'length': f'{end + 4}b', 'tail': '4s', 'ceiling': '-1dB', 'true_peak': True, 'loudness': -12,
        'patches': PATCHES, 'buses': buses,
        'master': {'fx': [{'type': 'eq', 'bands': ['hp cutoff=28']}]},
        'tracks': [
            {'name': 'kick', 'patch': 'wd-kick', 'gain': '-9dB', 'notes': T['kick'], 'fx': [{'type': 'eq', 'bands': ['peak cutoff=47 q=1.2 gain=-3dB', 'peak cutoff=130 q=0.9 gain=3dB'] + ([CHEST] if ON['chest'] else [])}]},
            {'name': 'ghost', 'patch': 'wd-ghost', 'gain': '-20dB', 'notes': T['ghost'], 'fx': ['lp cutoff=900', under]},
            {'name': 'tick', 'patch': 'wd-wood', 'gain': {'value': '-7dB', 'mod': [{'src': 'auto.alone', 'amount': 1}]}, 'auto': {'alone': alone()}, 'pan': 0, 'notes': T['tick'], 'fx': [hold(-12)], 'sends': {'hall': '-16dB'}},
            {'name': 'saw', 'patch': 'wd-saw', 'gain': '-12dB', 'pan': -0.25, 'notes': T['saw']},
            {'name': 'cell', 'patch': 'wd-wood', 'gain': '-1dB', 'pan': 0.3, 'notes': T['cell'], 'sends': {'hall': '-12dB'}},
            {'name': 'ping', 'patch': 'wd-ping', 'gain': '-12dB', 'pan': -0.15, 'notes': T['ping'], 'sends': {'hall': '-10dB'}},
            {'name': 'chord', 'patch': 'wd-chord', 'gain': '-8dB', 'pan': 0.1, 'notes': T['chord'], 'fx': [hold(-8), under], 'sends': {'hall': '-8dB'}},
            {'name': 'seed', 'patch': 'wd-seed', 'gain': '-6dB', 'notes': T['seed'], 'fx': [hold(-12)]},
        ],
    }
    by_name = {t['name']: t for t in doc['tracks']}
    if ON['tame']:
        by_name['ping']['fx'] = [{'type': 'eq', 'bands': [TAME]}] + by_name['ping'].get('fx', [])
    if ON['mid']:
        by_name['tick']['fx'] = by_name['tick']['fx'] + [{'type': 'eq', 'bands': MID['tick']}]
        by_name['saw']['fx'] = [{'type': 'eq', 'bands': MID['saw']}]
    if ON['body']:
        by_name['kick']['fx'] = [{'type': 'eq', 'bands': by_name['kick']['fx'][0]['bands'] + [BODY]}]
    if ON['tuck']:
        by_name['tick']['gain']['value'] = f"{float(by_name['tick']['gain']['value'][:-2]) - TUCK:g}dB"
    if ON['comp']:
        doc['patches'] = {**doc['patches'], 'wd-comp': NEW['wd-comp']}
        doc['tracks'].append({'name': 'comp', 'patch': 'wd-comp', 'gain': '-6dB', 'pan': 0.2, 'notes': T['comp']})
        if T.get('rate'):                                      # v10 RATE: the same click on the other side
            doc['tracks'].append({'name': 'rate', 'patch': 'wd-comp', 'gain': RATE['gain'], 'pan': RATE['pan'], 'notes': T['rate']})
    if ON['sink'] and ON['stop']:
        sunk = json.loads(json.dumps(PATCHES['wd-wood']))
        sunk['about'] = "Wind Down: the click whose note can sink (v3): wd-wood with the whole voice's pitch on the stroke (expr.sink, semitones)."
        sunk['synth']['pitch'] = {'value': 0, 'mod': [{'src': 'expr.sink', 'amount': 1}]}
        doc['patches'] = {**doc['patches'], 'wd-sink': sunk}
        by_name['tick']['patch'] = 'wd-sink'
    if ON['nudge']:                                           # the cell's notes move with the hand: the same patch as the sinking click
        if 'wd-sink' not in doc['patches']:
            sunk = json.loads(json.dumps(PATCHES['wd-wood']))
            sunk['about'] = "Wind Down: the bar whose note can move (v3): wd-wood with the whole voice's pitch on the stroke (expr.sink, semitones)."
            sunk['synth']['pitch'] = {'value': 0, 'mod': [{'src': 'expr.sink', 'amount': 1}]}
            doc['patches'] = {**doc['patches'], 'wd-sink': sunk}
        by_name['cell']['patch'] = 'wd-sink'
    if ON['grip'] and ON['taken']:                            # v11: the cell's bar twice, the second two octaves up, each with its own level on the stroke
        held = json.loads(json.dumps(doc['patches'][by_name['cell']['patch']]))
        bar_layer = held['synth']['layers'][0]
        held['about'] = "Wind Down: the bar with a hand on its middle (v11, after Ring True's rt-held): the cell's patch, and its bar a second time two octaves up (a wooden bar's second mode). Each has its level on the stroke: expr.note (dB on the note, 0 with no hand) and expr.mode (dB over -40 on the second mode)."
        held['synth']['layers'] = [{**bar_layer, 'level': {'value': '0dB', 'mod': [{'src': 'expr.note', 'amount': 1}]}}] + held['synth']['layers'][1:] + [{**bar_layer, 'semi': GRIP['semis'], 'level': {'value': GRIP['from'], 'mod': [{'src': 'expr.mode', 'amount': 1}]}}]
        doc['patches'] = {**doc['patches'], GRIP['patch']: held}
        by_name['cell']['patch'] = GRIP['patch']
    if ON['sing']:
        for me, ms, back, side in SING['walls']:
            doc['buses'][me] = {'pan': side, 'gain': {'value': '0dB', 'mod': [{'src': 'auto.near', 'amount': 1}]}, 'auto': {'near': near()}, 'fx': SING['fx'],
                                'returns': [{'from': 'tick', 'gain': SING['feed'], 'time': f'{ms}ms'}, {'from': me, 'gain': back, 'time': f'{ms}ms'}]}
    if ON['strings']:
        hand = {'points': ([['0b', -60], [f'{RUNS_DOWN * 4 - 1}b', -60], [f'{RUNS_DOWN * 4}b', STRINGS['from']], [f'{RUNS_DOWN * 4 + 8}b', 0], [f'{BARS * 4 + 16}b', 0]] if ON['early'] else
                           [['0b', -60], [f'{BARS * 4 - 0.5}b', -60], [f'{BARS * 4}b', 0], [f'{BARS * 4 + 16}b', 0]]), 'curve': 0}
        if ON['true']:                                         # v7: let go beside the cell from where the room goes to where the cell goes
            hand['points'] = hand['points'][:1] + [[f"{GOES['room'] * 4 - 1}b", -60], [f"{GOES['room'] * 4}b", 0], [f"{GOES['cell'] * 4 - 0.5}b", 0], [f"{GOES['cell'] * 4}b", -60]] + hand['points'][1:]
            if ON['answer'] and T.get('cell-drop'):            # v9: held open through the bar after the cell, then let down
                hand['points'][3:5] = [[f"{GOES['cell'] * 4 + ANSWER['open']}b", 0], [f"{GOES['cell'] * 4 + ANSWER['open'] + ANSWER['down']}b", -60]]
        for name, hz, side in STRINGS['strings']:
            me = 'str-' + name.lower()
            t = f"{1000 / hz - 225.1 / STRINGS['lp']:.3f}ms"         # a period, less the low-pass's own delay, so the loop is in tune
            doc['buses'][me] = {'pan': side, 'gain': {'value': '0dB', 'mod': [{'src': 'auto.hand', 'amount': 1}]}, 'auto': {'hand': hand}, 'fx': [f"lp cutoff={STRINGS['lp']}"],
                                'returns': [{'from': 'tick', 'gain': STRINGS['feed'], 'time': t}] + ([{'from': 'cell', 'gain': TRUE['feed'], 'time': t}] if ON['true'] else []) +
                                           ([{'from': x, 'gain': ANSWER['feed'], 'time': t} for x in ('cell-drop', 'cell-bounce')] if ON['true'] and ON['answer'] and T.get('cell-drop') else []) + [{'from': me, 'gain': db(STRINGS['back']), 'time': t}]}
    if T.get('cell-drop'):                                     # v8 DROP: the same track again for the one stroke, and its bounces: echoes of it, each sooner and softer by the same share
        doc['tracks'].append({**{x: y for x, y in by_name['cell'].items() if x != 'notes'}, 'name': 'cell-drop', 'notes': T['cell-drop']})
        gap = DROP['rest'] * 60000 / BPM / 4 * (1 - DROP['share']) / (1 - DROP['share'] ** (DROP['bounces'] + 1))
        doc['buses']['cell-bounce'] = {'pan': by_name['cell']['pan'], 'returns': [{'from': 'cell-drop', 'gain': f"{20 * log10(DROP['share']) * j:.2f}dB", 'time': f"{gap * (1 - DROP['share'] ** j) / (1 - DROP['share']):.1f}ms"} for j in range(1, DROP['bounces'] + 1)]}
    if ON['part'] and T['ping']:                               # v8 PART: the pings by pair, a track each (the same track three times), so that each cycle's bus hears only its own meetings
        base = {x: y for x, y in by_name['ping'].items() if x != 'notes'}
        doc['tracks'] = [t for t in doc['tracks'] if t['name'] != 'ping'] + [{**base, 'name': f'ping-{a}{b}', 'notes': [n for n in T['ping'] if n['pitch'] == PING[(a, b)]]} for a, b in PING]
        for c in CYCLES:
            doc['buses'][f'part-{c}'] = {'pan': PART['side'][c], 'gain': PART['gain'], 'fx': [f"hp cutoff={PART['hp'][c]}"],
                                         'returns': [{'from': f'ping-{a}{b}', 'gain': '0dB', 'time': f'{c * 60000 / BPM / 4:.2f}ms'} for a, b in PING if c in (a, b)]}
    if ON['knock'] and T['knock']:
        doc['patches'] = {**doc['patches'], 'wd-knock': WD_KNOCK}
        doc['tracks'].append({'name': 'knock', 'patch': 'wd-knock', 'gain': KNOCK['gain'], 'notes': T['knock'], 'fx': [hold(KNOCK['hold'])]})
    if ON['paid'] and T['paid']:
        doc['tracks'].append({'name': 'paid', 'patch': 'wd-seed', 'gain': by_name['seed']['gain'], 'notes': T['paid'], 'fx': [hold(-12)]})
        u, (p, q) = 1000 / PAID['hz'], PAID['coins']
        for coin, other, side in ((p, q, -1), (q, p, 1)):
            me, t = f'paid{coin}', f'{coin * u:.3f}ms'
            doc['buses'][me] = {'pan': side * PAID['pan'], 'gain': '0dB', 'fx': ['lp cutoff=6000', 'hp cutoff=40'],
                                'returns': [{'from': 'paid', 'gain': PAID['feed'], 'time': t}, {'from': me, 'gain': db(PAID['back']), 'time': t}, {'from': f'paid{other}', 'gain': db(PAID['back']), 'time': t}]}
            if ON['interest']:                                 # v9: the purse gives back more than it is given, cannot hold more than its size, and is shut on the one
                one = GOES['change'] * 4
                doc['buses'][me] = {'pan': side * PAID['pan'], 'gain': {'value': '0dB', 'mod': [{'src': 'auto.shut', 'amount': 1}]}, 'auto': {'shut': {'points': [['0b', 0], [f'{one - 0.03}b', 0], [f'{one}b', -60], [f'{BARS * 4 + 16}b', -60]], 'curve': 0}},
                                    'fx': ['lp cutoff=6000', 'hp cutoff=40', hold(INTEREST['size'])],
                                    'returns': [{'from': 'paid', 'gain': INTEREST['feed'], 'time': t}, {'from': me, 'gain': db(INTEREST['back']), 'time': t}, {'from': f'paid{other}', 'gain': db(INTEREST['back']), 'time': t}]}
    if ON['held']:
        waver = ON['waver'] and ON['wow'] and ON['open']        # v24 WAVER: the meetings' last chord is on the record too
        held_sec = second_at(min(n['at'] for n in T['held'])) if waver else 0
        doc['patches'] = {**doc['patches'], **({WOW['held']: wow_patch(OPEN, held_sec, f" v24: on a record pressed {WOW['off']:g} mm off its centre: its pitch wavers {wow_cents(held_sec):.1f} cents each way once a turn ({GROOVE['turn']} s).")} if waver else {'wd-open': OPEN} if ON['open'] else {'wd-held': V3['wd-held']})}
        doc['tracks'].append({'name': 'held', 'patch': WOW['held'] if waver else 'wd-open' if ON['open'] else 'wd-held', 'gain': f"{float(HELD['gain'][:-2]) + OPEN_DB:g}dB" if ON['open'] else HELD['gain'], 'pan': -0.1, 'notes': T['held'], 'fx': [under], 'sends': {'hall': '-6dB'}})
    if ON['real']:
        doc['patches'] = {**doc['patches'], 'wd-under': V3['wd-under']}
        doc['tracks'].append({'name': 'under', 'patch': 'wd-under', 'gain': REAL['gain'], 'notes': T['under'], 'fx': [under]})
    if T.get('lead'):
        doc['patches'] = {**doc['patches'], 'wd-under': V3['wd-under']}
        doc['tracks'].append({'name': 'lead', 'patch': 'wd-under', 'gain': LEAD['gain'], 'notes': T['lead']})
    if ON['hat']:
        doc['patches'] = {**doc['patches'], 'wd-hat': NEW['wd-hat']}
        doc['tracks'].append({'name': 'hat', 'patch': 'wd-hat', 'gain': '6dB', 'pan': -0.2, 'notes': T['hat'], 'sends': {'hall': '-18dB'}})
    for tr in LINGER['db']:                                     # v15 LINGER: a goodbye's strokes again, into the hall alone
        if T.get(tr + '-gone'):
            doc['tracks'].append({**{k: v for k, v in by_name[tr].items() if k not in ('notes', 'sends', 'auto')}, 'name': tr + '-gone', 'notes': T[tr + '-gone'], 'out': 'hall'})
    if ON['wall'] and ON['stop']:                               # v14 WALL: the clock on the wall does not run down
        for nm, hz, notes in zip(('tick', 'tock'), WALL['hz'], wall()):
            doc['patches'] = {**doc['patches'], f'wd-clock-{nm}': {
                'about': f"Wind Down: the clock on the wall, the {nm} (v14). Give or Take's (chirper-zero's gt-clock-{nm}, v16), under this song's name: a 9 ms grain of noise through a narrow band at {hz} Hz, one pallet of an escapement. Three of them make a tick (unlock, impulse, drop).",
                'play': {'vel_sens': 0.7}, 'synth': {'layers': ['white'], 'filters': [{'kind': 'bp', 'cutoff': hz, 'q': 5}, 'hp cutoff=1200'], 'amp': {'a': '0.1ms', 'd': '9ms', 's': 0, 'r': '5ms', 'curve': 3}}}}
            doc['tracks'].append({'name': f'clock-{nm}', 'patch': f'wd-clock-{nm}', 'gain': WALL['gain'], 'pan': WALL['pan'], 'notes': notes})
    if ON['quarters'] or ON['hour']:                            # v18: the clock on the wall chimes the song's quarters, and the hour
        bell = HAMMER['patch'] if ON['hammer'] else CHIME['patch']   # v19 HAMMER: another sound, another name
        if ON['wow']:                                           # v24 WOW: each quarter's chime has its own depth: a track and a patch a quarter
            for quarter in sorted({q for q, _, _ in chimes()}):
                first = min(sec for q, sec, _ in chimes() if q == quarter)
                doc['patches'] = {**doc['patches'], f"{WOW['chime']}-{quarter}": wow_patch(chime_patch(), first, f" v24: on a record pressed {WOW['off']:g} mm off its centre: its pitch wavers {wow_cents(first):.1f} cents each way once a turn ({GROOVE['turn']} s), as deep as the needle's radius at quarter {quarter} makes it.")}
                doc['tracks'].append({'name': f'chime-q{quarter}', 'patch': f"{WOW['chime']}-{quarter}", 'gain': CHIME['gain'], 'pan': WALL['pan'], 'sends': {'hall': CHIME['hall']},
                                      'notes': [{'at': round(beat_at(sec), 5), 'len': 1.0, 'pitch': CHIME['bells'][deg], 'vel': CHIME['vel'], **({'gain': f"{CHIME['trim'][q]:g}dB"} if q in CHIME['trim'] else {})} for q, sec, deg in chimes() if q == quarter]})
        else:
            doc['patches'] = {**doc['patches'], bell: chime_patch()}
            doc['tracks'].append({'name': 'chime', 'patch': bell, 'gain': CHIME['gain'], 'pan': WALL['pan'], 'sends': {'hall': CHIME['hall']},
                                  'notes': [{'at': round(beat_at(sec), 5), 'len': 1.0, 'pitch': CHIME['bells'][deg], 'vel': CHIME['vel'], **({'gain': f"{CHIME['trim'][q]:g}dB"} if q in CHIME['trim'] else {})} for q, sec, deg in chimes()]})
    if ON['one'] and ON['hour']:                                # v19 ONE: the clock strikes one, on the song's last stroke
        one_bell = chime_patch(ONE['ring'], f"Wind Down: the hour bell of the clock on the wall (v19). The chime's bell (six partials, no third{', struck by a hammer' if ON['hammer'] else ''}) an octave under the note its quarters end on, let ring {ONE['ring']}. It is struck once, on the song's last stroke: one o'clock.")
        one_name = WOW['hour'] if ON['wow'] else ONE['patch']    # v24 WOW: the hour bell on the record: another sound, another name
        doc['patches'] = {**doc['patches'], one_name: wow_patch(one_bell, clock(BARS), f" v24: on a record pressed {WOW['off']:g} mm off its centre: its pitch wavers {wow_cents(clock(BARS)):.1f} cents each way once a turn ({GROOVE['turn']} s).") if ON['wow'] else one_bell}
        doc['tracks'].append({'name': 'hour', 'patch': one_name, 'gain': CHIME['gain'], 'pan': WALL['pan'], 'sends': {'hall': CHIME['hall']},
                              'notes': [{'at': BARS * 4, 'len': 1.0, 'pitch': ONE['bell'], 'vel': ONE['vel'], 'gain': f"{ONE['db']:g}dB"}]})
        if ON['sympathy'] and ON['strings']:                    # v19 SYMPATHY: Ring True's strings hear the hour bell
            for name, bus in doc['buses'].items():
                if name.startswith('str-'):
                    bus['returns'] = bus['returns'] + [{'from': 'hour', 'gain': ONE['strings'], 'time': next(r['time'] for r in bus['returns'] if r['from'] == 'tick')}]
    if ON['groove'] and ON['stop']:                             # v20 GROOVE: the needle is in the run-out groove
        doc['patches'] = {**doc['patches'], GROOVE['patch']: {
            'about': f"Wind Down: the record's run-out groove (v20): a speck in the groove, the same at every turn: the engine's chip noise with no chip's clock (the same samples at each note-on; chirper-zero's finding, Give or Take v24), {GROOVE['ms']} ms, {GROOVE['hp']} to {GROOVE['lp']} Hz. The note sets the step rate: the joint is the lowest and dullest.",
            'play': {'vel_sens': 0.5, 'gate': 1}, 'synth': {'layers': [{'type': 'chip', 'chip': {'kind': 'noise', 'clock': 0}}], 'filters': [f"hp cutoff={GROOVE['hp']}", f"lp cutoff={GROOVE['lp']}"], 'amp': {'a': '0.3ms', 'd': '0s', 's': 1, 'r': '3ms'}}}}
        doc['tracks'].append({'name': 'groove', 'patch': GROOVE['patch'], 'gain': GROOVE['gain'], 'pan': GROOVE['pan'], 'notes': groove()})
        doc['length'] = f'{round(beat_at(run_out()), 3)}b'
    if ON['surface'] and ON['stop']:                            # v20 SURFACE: what the needle rides on: the same hiss every turn
        slid = inner() if ON['leadin'] and (ON['spiral'] or ON['reveal']) else 1.0   # v21 INNER: in the locked groove the band has slid with the radius, and the level is held
        lock_up = NEARER['lock'] if ON['nearer'] and ON['leadin'] and ON['reveal'] and not ON['spiral'] else 0   # v22 NEARER
        sf = SURFACE if slid == 1.0 else {**SURFACE, 'patch': SPIRAL['lock'], 'hp': round(SURFACE['hp'] * slid), 'lp': round(SURFACE['lp'] * slid), 'gain': f"{float(SURFACE['gain'][:-2]) - 10 * log10(slid) + lock_up:.1f}dB"}
        doc['patches'] = {**doc['patches'], sf['patch']: {
            'about': f"Wind Down: the record's surface in its run-out groove (v20): the engine's chip noise with no chip's clock on {sf['pitch']} (the same samples at each note-on, and too slow a step rate to come round inside a turn), {sf['hp']} to {sf['lp']} Hz, one note a turn: the hiss repeats with the record.",
            'play': {'vel_sens': 0.5, 'gate': 1}, 'synth': {'layers': [{'type': 'chip', 'chip': {'kind': 'noise', 'clock': 0}}], 'filters': [f"hp cutoff={sf['hp']}", f"lp cutoff={sf['lp']}"], 'amp': {'a': '5ms', 'd': '0s', 's': 1, 'r': '30ms'}}}}
        t0, stop = clock(BARS) + GROOVE['after'], (lifted() or (run_out() - 0.3 if run_out() else clock(BARS) + 6))
        starts = [t0 + k * GROOVE['turn'] for k in range(GROOVE['turns'] + 2) if t0 + k * GROOVE['turn'] < stop - 0.05]
        doc['tracks'].append({'name': 'surface', 'patch': sf['patch'], 'gain': sf['gain'], 'pan': 0,
                              'notes': [{'at': round(beat_at(a), 5), 'len': round(beat_at(min(a + GROOVE['turn'], stop)) - beat_at(a), 5), 'pitch': sf['pitch'], 'vel': sf['vel']} for a in starts]})
    if lifted():                                                # v20 LIFT: somebody lifts the needle
        doc['patches'] = {**doc['patches'], LIFT['patch']: {
            'about': f"Wind Down: the needle lifted out of the groove (v20): a soft low thump, a sine and its octave, {LIFT['ms']} ms.",
            'play': {'vel_sens': 0.3}, 'synth': {'layers': [{'wave': 'sine'}, {'wave': 'sine', 'semi': 12, 'level': '-6dB'}], 'amp': {'a': '2ms', 'd': f"{LIFT['ms']}ms", 's': 0, 'r': '30ms'}}}}
        doc['tracks'].append({'name': 'lift', 'patch': LIFT['patch'], 'gain': LIFT['gain'], 'pan': 0,
                              'notes': [{'at': round(beat_at(lifted()), 5), 'len': round(beat_at(lifted() + LIFT['ms'] / 1000) - beat_at(lifted()), 5), 'pitch': LIFT['pitch'], 'vel': LIFT['vel']}]})
        for tr in doc['tracks']:
            if tr['name'] == 'groove':
                pitch, vel, db = LIFT['speck']
                tr['notes'] = tr['notes'] + [{'at': round(beat_at(lifted()), 5), 'len': tr['notes'][0]['len'], 'pitch': pitch, 'vel': vel, 'gain': f'{db}dB'}]
    if ON['leadin']:                                            # v21 LEADIN: the playing groove's surface, in over the first bars; SPIRAL: under the whole record; INNER: its band slides down with the radius
        whole = ON['spiral'] and ON['stop']
        stays = whole or (ON['reveal'] and ON['stop'])
        end = (clock(BARS) + GROOVE['after'] if ON['groove'] and ON['surface'] else clock(BARS)) if stays else clock(SPIRAL['to'] + SPIRAL['out'])
        secs = lambda bars: f"{bars * 240 / BPM:.2f}s"
        doc['patches'] = {**doc['patches'], SPIRAL['patch']: {
            'about': "Wind Down: the record's surface in the playing groove (v21): one held white hiss (new vinyl at every turn: it never comes round, as the run-out's does), coming in over the first bars; its band and its comings and goings are the track's.",
            'play': {'gate': 1}, 'synth': {'layers': ['white'], 'amp': {'a': secs(SPIRAL['in']), 'd': '0s', 's': 1, 'r': '30ms'}}}}
        sliding = ON['inner'] and stays
        under, back = SPIRAL['to'] + SPIRAL['out'], RUNS_DOWN + SPIRAL['up']
        comes_up = NEARER['up'] if ON['nearer'] and stays and not whole else 0   # v22 NEARER: the surface comes back higher than it came in
        there = lambda b: comes_up if comes_up and b >= back else 0 if whole or b <= SPIRAL['to'] or (stays and b >= back) else -SPIRAL['down'] if b >= under and (not stays or b <= RUNS_DOWN) else None   # dB: bars 1-8, down under the drum, up again with the spring
        bars = sorted(set(range(0, BARS, SPIRAL['every'])) | {SPIRAL['to'], under} | ({RUNS_DOWN, back} if stays else set()))
        pts = [[f'{b * 4}b', clock(b), there(b)] for b in bars if clock(b) < end and there(b) is not None] + [[f'{round(beat_at(end), 3)}b', end, comes_up if stays else -SPIRAL['down']]]
        doc['tracks'].append({'name': 'spiral', 'patch': SPIRAL['patch'], 'pan': 0, 'notes': [{'at': 0, 'len': round(beat_at(end), 5), 'pitch': 'C5', 'vel': 0.8}],
                              'gain': {'value': SPIRAL['gain'], 'mod': [{'src': 'auto.held', 'amount': 1}]},
                              'fx': ([f"hp cutoff={SPIRAL['hp']}+auto.slide*{round(log2(inner(end)), 4)}"] + [f"lp cutoff={SPIRAL['lp']}+auto.slide*{round(log2(inner(end)), 4)}"] * SPIRAL['walls']   # the depth of a lane on a cutoff is in OCTAVES (bench: written in Hz the track was silent)
                                     if sliding else [f"hp cutoff={SPIRAL['hp']}"] + [f"lp cutoff={SPIRAL['lp']}"] * SPIRAL['walls']),
                              'auto': {'held': {'points': [[b, round(db + (-10 * log10(inner(t)) if sliding else 0), 3)] for b, t, db in pts], 'curve': 0},
                                       **({'slide': {'points': [[b, round(log2(inner(t)) / log2(inner(end)), 4)] for b, t, _ in pts], 'curve': 0}} if sliding else {})}})
    if ON['rumble'] and ON['groove'] and ON['surface'] and ON['stop'] and lifted():   # v23 RUMBLE: the platter's bearing, under the last ticks and the run-out, to the lift
        joint, turn, stop = clock(BARS) + GROOVE['after'], GROOVE['turn'], lifted()
        first = joint if RUMBLE['from'] == 'joint' else joint - turn * int((joint - clock(RUNS_DOWN)) / turn)      # from the run-out's first joint (the third build's, from the bar the drum goes, cost a section), in step with the joints
        starts = [first + k * turn for k in range(int((stop - first) / turn) + 1) if first + k * turn < stop - 0.05]
        doc['patches'] = {**doc['patches'], RUMBLE['patch']: {
            'about': f"Wind Down: the turntable's rumble (v23): the bearing under the platter: the engine's chip noise with no chip's clock (the same samples at each note-on), {RUMBLE['hp']} to {RUMBLE['lp']} Hz, one note a turn: it comes round with the record.",
            'play': {'vel_sens': 0.5, 'gate': 1}, 'synth': {'layers': [{'type': 'chip', 'chip': {'kind': 'noise', 'clock': 0}}], 'filters': [f"hp cutoff={RUMBLE['hp']}"] + [f"lp cutoff={RUMBLE['lp']}"] * 2, 'amp': {'a': '20ms', 'd': '0s', 's': 1, 'r': '20ms'}}}}
        doc['tracks'].append({'name': 'rumble', 'patch': RUMBLE['patch'], 'gain': RUMBLE['gain'], 'pan': 0,
                              'notes': [{'at': round(beat_at(a), 5), 'len': round(beat_at(min(a + turn, stop)) - beat_at(a), 5), 'pitch': RUMBLE['pitch'], 'vel': RUMBLE['vel'],
                                         **({'gain': f"{RUMBLE['in'][k]}dB"} if k < len(RUMBLE['in']) else {})} for k, a in enumerate(starts)]})
    if ON['pallet']:                                            # v23 PALLET: the click's tooth, where the drum plays
        drum = {int(n['at'] // 4) for t in doc['tracks'] if t['name'] == 'kick' for n in t['notes']}
        click = next(t for t in doc['tracks'] if t['name'] == 'tick')
        teeth = [{'at': n['at'], 'len': 0.05, 'pitch': 'C6', 'vel': PALLET['vel']} for n in click['notes'] if PALLET['bars'][0] <= n['at'] // 4 < PALLET['bars'][1] and int(n['at'] // 4) in drum]
        doc['patches'] = {**doc['patches'], PALLET['patch']: {
            'about': f"Wind Down: the escape wheel's tooth on the pallet (v23): {PALLET['ms']} ms of white noise above {PALLET['hp'] / 1000:g} kHz, struck with the click where the drum plays: the click's top, which the drum's level takes from it.",
            'play': {'vel_sens': 0.5}, 'synth': {'layers': [{'type': 'noise', 'color': 'white'}], 'filters': [f"hp cutoff={PALLET['hp']}"] * 2, 'amp': {'a': '0.1ms', 'd': f"{PALLET['ms']}ms", 's': 0, 'r': '4ms'}}}}
        tock = [n for n in teeth if ON['exit'] and round(n['at'] % 4 * 4) in PALLET['exit']['on']]   # v23 EXIT: the second pallet
        doc['tracks'].append({'name': 'pallet', 'patch': PALLET['patch'], 'gain': PALLET['gain'], 'pan': click.get('pan', 0), 'notes': [n for n in teeth if n not in tock]})
        if tock:
            doc['patches'] = {**doc['patches'], PALLET['exit']['patch']: {
                'about': f"Wind Down: the tooth on the exit pallet, the tock (v23): wd-pallet's {PALLET['ms']} ms of noise, through a band from {PALLET['exit']['band'][0] / 1000:g} to {PALLET['exit']['band'][1] / 1000:g} kHz: lower than the tick's tooth, with less of its top.",
                'play': {'vel_sens': 0.5}, 'synth': {'layers': [{'type': 'noise', 'color': 'white'}], 'filters': [f"hp cutoff={PALLET['exit']['band'][0]}"] * 2 + [f"lp cutoff={PALLET['exit']['band'][1]}"] * PALLET['exit']['steep'], 'amp': {'a': '0.1ms', 'd': f"{PALLET['ms']}ms", 's': 0, 'r': '4ms'}}}}
            doc['tracks'].append({'name': 'pallet-exit', 'patch': PALLET['exit']['patch'], 'gain': PALLET['exit']['gain'], 'pan': click.get('pan', 0), 'notes': tock})
    if ON['rundown'] and ON['pallet'] and ON['stop']:           # v24 RUNDOWN: the teeth come back under the last ticks, each a lift time after its click; LIMP: the second pallet's twice as late
        click = next(t for t in doc['tracks'] if t['name'] == 'tick')
        down = {False: [], True: []}
        for n in click['notes']:
            if RUNS_DOWN * 4 <= n['at'] < BARS * 4:             # the last clicks, not the last stroke: the wheel has stopped
                second = bool(ON['exit']) and round(n['at'] % 4 * 4) in PALLET['exit']['on']
                down[second].append({'at': round(beat_at(second_at(n['at']) + lift_time(n['at'], second)), 5), 'len': 0.05, 'pitch': 'C6', 'vel': PALLET['vel']})
        doc['tracks'].append({'name': 'pallet-down', 'patch': PALLET['patch'], 'gain': RUNDOWN['gain'], 'pan': click.get('pan', 0), 'notes': down[False]})
        if down[True]:
            doc['tracks'].append({'name': 'pallet-exit-down', 'patch': PALLET['exit']['patch'], 'gain': RUNDOWN['exit'], 'pan': click.get('pan', 0), 'notes': down[True]})
    if ON['tally']:                                            # v25 TALLY: Ring True's notched stick counts who is still here
        doc['patches'] = {**doc['patches'], TALLY['patch']: TALLY_PATCH}
        doc['tracks'].append({'name': 'tally', 'patch': TALLY['patch'], 'gain': TALLY['gain'], 'pan': TALLY['pan'], 'notes': sorted(tally_notes() + entered_notes(), key=lambda q: q['at'])})
    if ON['eleven']:                                           # v26 ELEVEN: Least Common's eleven, from all gathered to the last stroke
        doc['patches'] = {**doc['patches'], ELEVEN['patch']: ELEVEN_PATCH}
        doc['tracks'].append({'name': 'eleven', 'patch': ELEVEN['patch'], 'gain': ELEVEN['gain'], 'pan': ELEVEN['pan'], **({'sends': {'hall': ELEVEN['hall']}} if ELEVEN['hall'] and 'hall' in doc.get('buses', {}) else {}), 'notes': eleven_notes()})
    if ON['elder'] and ON['eleven']:                            # v27 ELDER: the eleven's big brother, every eleven bars from all gathered to the last stroke
        doc['patches'] = {**doc['patches'], ELDER['patch']: elder_patch()}
        doc['tracks'].append({'name': ELDER['track'], 'patch': ELDER['patch'], 'gain': ELDER['gain'], 'pan': ELDER['pan'], **({'sends': {'hall': ELDER['hall']}} if ON['aired'] and 'hall' in doc.get('buses', {}) else {}), 'notes': sorted(elder_notes() + elder_count(), key=lambda q: q['at'])})
    if ON['preecho'] and ON['catch']:                           # v22 PREECHO: in each caught bar the first turn of the bar after it, a turn early
        turn = GROOVE['turn'] * BPM / 60                        # beats in one turn of the record (the tempo is steady at every catch)
        for t in list(doc['tracks']):
            if t['name'] in PREECHO['not'] or t['name'].startswith('pre-'):
                continue
            early = sorted(({**n, 'at': round(n['at'] - turn, 5), 'gain': f"{float(n.get('gain', '0dB')[:-2]) + PREECHO['at'][c]:g}dB"}
                            for c in CATCHES if c in PREECHO['at'] for n in t['notes'] if 4 * (c + 1) <= n['at'] < 4 * (c + 1) + turn), key=lambda n: n['at'])
            if early:
                fader = t.get('gain', '0dB')
                doc['tracks'].append({**{k: v for k, v in t.items() if k != 'notes'}, 'name': 'pre-' + t['name'], 'gain': fader['value'] if isinstance(fader, dict) else fader, 'notes': early})
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


def clock(bar):
    """Seconds at the top of a bar: steady to RUNS_DOWN, then a tempo falling in a straight line (against beats) to SLOW."""
    t = min(bar, RUNS_DOWN) * 4 * 60 / BPM
    if bar > RUNS_DOWN:
        n, x = WIND * 4, (bar - RUNS_DOWN) * 4
        if ON['stop']:                                        # a platter's: x beats take W - sqrt(W^2 - 2 W x) beats of full speed
            return t + 60 / BPM * (w_stop() - sqrt(w_stop() ** 2 - 2 * w_stop() * x))
        k = (SLOW - BPM) / n
        t += 60 / k * log((BPM + k * x) / BPM)
    return t


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--out', type=Path, default=OUT)
    ap.add_argument('--form', action='store_true', help='print the form and stop')
    for k in [k for k, on in ON.items() if not on]:
        ap.add_argument(f'--with-{k}', action='store_true', help=f'put in {k} (written, and off)')
    for k in [k for k, on in ON.items() if on]:
        ap.add_argument(f'--without-{k}', action='store_true', help=f'leave out {k} (the last three off is v27, the last six v26, the last nine v25, the last twelve v24, the last sixteen v23, the last nineteen v22, the last twenty-one v21, the last twenty-four v20, the last twenty-seven v19, the last thirty v18, the last thirty-two v17, the last thirty-four v16, the last thirty-six v15, the last thirty-eight v14, the last forty v13, the last forty-two v12, the last forty-four v11, the last forty-seven v10, the last fifty v9, the last fifty-three v8, the last fifty-five v7, the last fifty-eight v6, the last sixty-one v5, the last sixty-four v4, the last sixty-seven v3, the last seventy-three v2, all seventy-nine v1)')
    a = ap.parse_args()
    for k in ON:
        ON[k] = getattr(a, f'with_{k}') if not ON[k] else not getattr(a, f'without_{k}')
    if a.form:
        marks = sorted([(COMES[k], f'{k} comes') for k in GATHER] + [(DRUM_IN, 'the drum comes'), (ALL, 'all gathered'), (LET_GO[0], 'the cell is let go')] +
                       [(GOES[k], f'{k} goes' if k != 'grid' else 'the drum goes; the spring runs down') for k in GATHER] + [(BARS, 'the last stroke, on the one')] +
                       ([(b, 'caught') for b in CATCHES] if ON['catch'] else []) +
                       ([(COMP_BARS[0], 'the complement fills the holes'), (COMP_BARS[1], 'the complement goes')] if ON['comp'] else []) +
                       ([(HAT_BARS[0], 'the hat that slows for ever')] if ON['hat'] else []) +
                       ([(LEARNT_BARS[0], "the bass plays the room's figure"), (LEARNT_BARS[1], 'the bass is itself again')] if ON['learnt'] else []) +
                       ([(GOES['change'] - SPENT, 'the change spends what is left')] if ON['spent'] else []) +
                       ([(GOES['change'] - SPENT, 'the change is also paid in another currency: coins of 3 and 5 of a unit two thirds of a sixteenth (three for two)')] if ON['exchange'] and ON['spent'] else []) +
                       ([(GOES['change'] - SPENT, "the complement's click counts what the other currency can pay, between the sixteenths: " + ' '.join(str(a) for a in range(1, RATE['upto'] + 1) if coins_for(a, *COINS) and (a / EXCHANGE['per']) % 1) + ' units after each seed')] if ON['rate'] and ON['exchange'] and ON['spent'] and ON['comp'] else []) +
                       ([(beat // 4, f'the drum gives beat {beat % 4 + 1} to the answer: the three and the five meet on it') for beat in range(BARS * 4) if given(beat)]) +
                       ([(GOES['meetings'], 'the last chord, held')] if ON['held'] else []) +
                       ([(GOES['cell'] - LEAVE, 'the cell is taken back into the hand')] if ON['taken'] else []) +
                       ([(GOES['cell'] - LEAVE, "the hand is on the bar's middle: bar by bar the cell's note goes and its second mode, two octaves up, is what is left; its dropped stroke has the note again")] if ON['grip'] and ON['taken'] else []) +
                       ([(RUNS_DOWN - len(CHOKE['notes']), 'the beater is held against the drum: its note rises, ' + ' then '.join(CHOKE['notes']))] if ON['choke'] else []) +
                       ([(b, f"the bass comes back before the drum: its fundamental holds {LEAD['pitch']} through the last {'beat' if LEAD['beats'] == 1 else str(LEAD['beats']) + ' beats'}") for b in CATCHES if b > COMES['ghost']] if ON['lead'] and ON['catch'] else []) +
                       ([(b, 'the catch says who is coming: ' + ', '.join(f"{tr} {n['pitch']} on sixteenth {round((n['at'] - b * 4) * 4)}" for tr, n in told(b))) for b in CATCHES if told(b)] if ON['tell'] and ON['catch'] else []) +
                       ([(b, f"for that beat the bass is whole: its own voice plays the {LEAD['pitch']} under its fundamental") for b in CATCHES if b > COMES['ghost'] and b in WHOLE['bars']] if ON['whole'] and ON['lead'] and ON['catch'] else []) +
                       ([(b, 'the bar after says who has left: ' + ', '.join(f"{tr} {n['pitch']} on sixteenth {round((n['at'] - b * 4) * 4)}" for tr, n in left(b))) for b in range(BARS) if left(b)] if ON['left'] else []) +
                       ([(COMES['room'] - 1, "the room's door is open through the caught bar: the click alone is heard in the room")] if ON['ajar'] and ON['catch'] else []) +
                       ([(RUNS_DOWN, f"the surface comes back nearer than it came in: {NEARER['up']} dB up under the last ticks, and the locked groove's hiss {NEARER['lock']} dB up: the step at the first joint is {5 + NEARER['lock'] - NEARER['up']} dB (5)")] if ON['nearer'] and ON['leadin'] and ON['reveal'] and ON['stop'] and not ON['spiral'] else []) +
                       ([(RUNS_DOWN, f"the turntable rumbles: its bearing is heard {'in the run-out' if RUMBLE['from'] == 'joint' else 'under the last ticks and the run-out'}, {RUMBLE['hp']} to {RUMBLE['lp']} Hz, the same at every turn, from {'its first joint' if RUMBLE['from'] == 'joint' else f'bar {RUNS_DOWN + 1}'} to the needle's lift")] if ON['rumble'] and ON['groove'] and ON['surface'] and ON['stop'] and lifted() else []) +
                       ([(PALLET['bars'][0], f"the escapement has two pallets: the tooth on the first (the click on sixteenths 2 and 10: tick) is all above {PALLET['hp'] / 1000:g} kHz; on the second (sixteenths {' and '.join(str(x) for x in PALLET['exit']['on'])}: tock) it is lower, {PALLET['exit']['band'][0] / 1000:g} to {PALLET['exit']['band'][1] / 1000:g} kHz, with less of the first one's top")] if ON['pallet'] and ON['exit'] else []) +
                       ([(PALLET['bars'][0], f"the click shows its tooth where the drum plays, bars {PALLET['bars'][0] + 1} to {PALLET['bars'][1]}: {PALLET['ms']} ms of noise above {PALLET['hp'] / 1000:g} kHz with every click (the escape wheel's tooth on the pallet); not in the caught bars, where the click is bare")] if ON['pallet'] else []) +
                       ([(ELEVEN['from'], f"the eleven comes home: Least Common's fourth voice ({ELEVEN['patch']}) is struck every {ELEVEN['beats']} beats from here, its echo every {ELEVEN['beats']} sixteenths between: from here to the last stroke is {(BARS - ELEVEN['from']) * 4} beats, {(BARS - ELEVEN['from']) * 4 // ELEVEN['beats']} elevens and {(BARS - ELEVEN['from']) * 4 % ELEVEN['beats']} over (in Least Common 210: 19 and 1 over): {(BARS - ELEVEN['from']) * 4 // ELEVEN['beats'] + 1} strokes" +
                         (f"; its note: harmonic {ELEVEN['harmonic'][0]} of the G an octave under the drum's ({eleven_hz(0, 32):.1f} Hz, an octave under Least Common's)" + (f", each stroke a thirty-second of a harmonic nearer the next ({eleven_hz(1, 32) - eleven_hz(0, 32):.2f} Hz a stroke): {' '.join(f'{eleven_hz(k, 32):.1f}' for k in (0, 8, 16, 24, 31))} Hz at strokes 1 9 17 25 32" if ON['creeps'] and ON['lands'] else ''))),
                         (BARS, f"the eleven's last stroke is the last stroke: " + (f"harmonic {ELEVEN['harmonic'][1]}, {eleven_hz(32, 32):.1f} Hz: the fifth, D4, over the hour bell's {ONE['bell']}: in tune" if ON['lands'] else f"still harmonic {ELEVEN['harmonic'][0]}, {eleven_hz(32, 32):.1f} Hz"))] if ON['eleven'] else []) +
                       ([(ELEVEN['from'], f"the eleven's big brother comes home too ({ELDER['patch']}: Least Common's: the eleven's bar let ring, at the eleven's own pitch): on the bar line every {ELDER['bars']} bars from here: to the last stroke is {BARS - ELEVEN['from']} bars, {(BARS - ELEVEN['from']) // ELDER['bars']} elevens of bars and {(BARS - ELEVEN['from']) % ELDER['bars']} over: bars {' '.join(str(round(q['at'] / 4) + 1) for q in elder_notes() if q['at'] >= ELEVEN['from'] * 4 and q['at'] < BARS * 4)} and the last stroke: with every fourth knock of the eleven: in Least Common the two were a beat apart: here they agree" + (f"; it is heard in the hall ({ELDER['hall']}): it rings long enough to keep its pitch there" if ON['aired'] else ''))] +
                        ([(round(elder_notes()[0]['at'] / 4), f"the big brother is heard before the eleven comes: on the bar line of bar{'s' if len(ELDER['told']) > 1 else ''} {' and '.join(str(round(q['at'] / 4) + 1) for q in elder_notes() if q['at'] < ELEVEN['from'] * 4)}, {' and '.join(str(x) for x in sorted(ELDER['told'], reverse=True))} elevens of bars early, {-ELDER['told_db']} dB softer" + (f"; and there the two are as they were in Least Common: the eleven's knock {ELDER['behind']} beat behind it, on beat {ELDER['behind'] + 1}" if ON['apart'] else ''))] if ON['told'] and elder_notes()[0]['at'] < ELEVEN['from'] * 4 else []) if ON['elder'] and ON['eleven'] else []) +
                       ([(TALLY['bars'][0], f"somebody keeps the score as they leave: Ring True's notched stick ({TALLY['patch']}): a row of dry clicks a sixty-fourth apart ({60000 / BPM * TALLY['gap']:.0f} ms) on beat {TALLY['at'] // 4 + 1} of every bar, bars {TALLY['bars'][0] + 1} to {TALLY['bars'][1]}, a notch for each of the seven still here: " +
                         ', '.join(f"bars {b + 1}-{b + LEAVE}: {tally_count(b)}" for b in range(TALLY['bars'][0], TALLY['bars'][1], LEAVE)) + '; when only the click is left the stick is put down' +
                         ('; the full house is read once before, in bar ' + str(TALLY['bars'][0]) + ': seven' if ON['full'] else '') +
                         (f"; the row is drawn back: its click on the beat ({TALLY['ladder'][0]}), the notches falling away after it: {' '.join(TALLY['ladder'][1:tally_count(TALLY['bars'][0]) + 1])}" if ON['back'] else '; the row climbs to its click, as in Ring True'))] if ON['tally'] else []) +
                       ([(RUNS_DOWN, "the tick comes apart as the spring runs down: the teeth come back under the last 32 clicks, each a lift time after its click (ms, by bar, first pallet" + (" then second, which has twice as far to fall" if ON['limp'] and ON['exit'] else '') + "): " +
                         '; '.join(f"bar {RUNS_DOWN + k + 1}: {1000 * lift_time((RUNS_DOWN + k) * 4 + 0.5):.0f}" + (f" {1000 * lift_time((RUNS_DOWN + k) * 4 + 1.5, True):.0f}" if ON['exit'] else '') for k in range(WIND)) +
                         f"; the last click {1000 * lift_time(BARS * 4 - 0.5, True):.0f}; on the last stroke no tooth falls: the wheel has stopped")] if ON['rundown'] and ON['pallet'] and ON['stop'] else []) +
                       ([(0, f"the record is pressed {WOW['off']:g} mm off its centre: once a turn ({GROOVE['turn']} s) what rings on it wavers in pitch, more the nearer the label: the clock's chimes " +
                         ', '.join(f"{wow_cents(min(sec for q, sec, _ in chimes() if q == quarter)):.1f}" for quarter in sorted({q for q, _, _ in chimes()})) + f" cents each way by quarter, the hour bell {wow_cents(clock(BARS)):.1f}; at its top at every joint of the run-out")] if ON['wow'] and (ON['quarters'] or ON['hour']) else []) +
                       ([(GOES['meetings'], f"the last chord is on the record too: it wavers {wow_cents(clock(GOES['meetings'])):.1f} cents each way once a turn as it dies")] if ON['waver'] and ON['wow'] and ON['open'] else []) +
                       ([(CATCHES[0], f"the record's pre-echo: in caught bars {', '.join(str(c + 1) for c in sorted(PREECHO['at']))} the first turn of the bar after ({GROOVE['turn']} s: {GROOVE['turn'] * BPM / 60:.2f} beats) is heard a turn early, {' '.join(str(-PREECHO['at'][c]) for c in sorted(PREECHO['at']))} dB down: all but the click and the clocks; its beats fall {round(1000 * (240 / BPM - GROOVE['turn']))} ms after the caught bar's own")] if ON['preecho'] and ON['catch'] else []) +
                       ([(CATCHES[0], 'the other clock is heard in each caught bar, falling behind the beat it began on (the click is on the half beats): ms after the beat, by catch: ' + '; '.join(' '.join(f'{(s * BPM % 60) * 1000 / BPM:.0f}' for s in caught_seconds() if 240 * b <= s * BPM < 240 * (b + 1)) for b in CATCHES))] if ON['clocks'] and ON['wall'] and ON['stop'] and ON['catch'] else []) +
                       ([(b, 'the hall keeps the goodbye: ' + ', '.join(sorted({tr for tr, _ in left(b) if tr in LINGER['db']}))) for b in range(BARS) if any(tr in LINGER['db'] for tr, _ in left(b))] if ON['linger'] and ON['left'] else []) +
                       ([((ALL + GOES['change']) // 2, 'the bass goes down to the fifth, under the drum: ' + ' | '.join(' '.join(moved(x, FIFTH['semis']) for x in row) for row in GHOST)), (GOES['change'], 'the bass is home on G')] if ON['fifth'] else []) +
                       ([((ALL + GOES['change']) // 2, f"the drum goes to the fifth too, the other way: it is tuned up to {moved('G1', TUNED['semis'])} while the bass is down there"), (GOES['change'], 'the drum falls a fifth onto its own note, G1, on the one')] if ON['tuned'] and ON['fifth'] else []) +
                       ([(GOES['change'], 'home is whole for its first bar: the bass keeps its fundamental under it (' + ' '.join(GHOST[GOES['change'] % 4]) + '), and it is taken away on the next one')] if ON['resolve'] and ON['stand'] and ON['real'] and ON['fifth'] else []) +
                       ([((ALL + GOES['change']) // 2, 'on the fifth the bass is whole: its fundamental under every note (D1 is 36.7 Hz), to the one of the bar it comes home')] if ON['stand'] and ON['real'] and ON['fifth'] else []) +
                       ([(q * RUNS_DOWN // 4, f"the clock chimes the {('quarter', 'half', 'three quarters')[q - 1]}: {('one change', 'two changes', 'three changes')[q - 1]}, a note a second from {min(x for k, x, _ in chimes() if k == q)} s (" + ' | '.join(' '.join(CHIME['bells'][d] for d in CHIME['changes'][c]) for c in CHIME['order'][q]) + f"), {round((beat_at(min(x for k, x, _ in chimes() if k == q)) % 1) * 60000 / BPM)} ms after a beat and 32 ms later with each note") for q in (1, 2, 3)] if ON['quarters'] else []) +
                       ([(RUNS_DOWN, f"the clock chimes the hour, the only time on the record: four changes, a note a second from {min(x for k, x, _ in chimes() if k == 4)} s to {max(x for k, x, _ in chimes() if k == 4)} s (" + ' | '.join(' '.join(CHIME['bells'][d] for d in CHIME['changes'][c]) for c in CHIME['order'][4]) + f"); the last stroke, {clock(BARS) - max(x for k, x, _ in chimes() if k == 4):.1f} s on, is its one o'clock")] if ON['hour'] else []) +
                       ([(BARS, f"the clock strikes one, on the last stroke: its hour bell ({ONE['bell']}), an octave under the bell its quarters end on, let ring {ONE['ring']}; the {WALL['after']} ticks after it are under its ring")] if ON['one'] and ON['hour'] else []) +
                       ([(BARS, f"the record is still turning: the needle is in the run-out groove: a click where the groove joins itself, once a turn ({GROOVE['turn']} s: 33 1/3 turns a minute), and the same three specks of dust each time round, " + ', '.join('+'.join(str(c) for c in CYCLES[:i + 1]) for i in range(3)) + f" sixteenths of a turn on: {GROOVE['turns']} turns from {clock(BARS) + GROOVE['after']:.1f} s and the joint once more at {clock(BARS) + GROOVE['after'] + GROOVE['turns'] * GROOVE['turn']:.1f} s; the wall clock's last tick is at {int(clock(BARS)) + WALL['after']} s: the loop is heard twice alone")] if ON['groove'] and ON['stop'] else []) +
                       ([(0, f"the needle is down: the record's surface comes in under the click over bars 1 to {SPIRAL['in']} (no stroke), {SPIRAL['hp']} to {SPIRAL['lp']} Hz" + (": one hiss that never comes round, under the whole record to the run-out's first joint, where the locked groove's takes over" if ON['spiral'] and ON['stop'] else f", and goes under the drum over bars {SPIRAL['to'] + 1} to {SPIRAL['to'] + SPIRAL['out']}"))] if ON['leadin'] else []) +
                       ([(RUNS_DOWN, f"the record comes up as the spring runs down: its surface again, over bars {RUNS_DOWN + 1} to {RUNS_DOWN + SPIRAL['up']}, and under the last ticks to the run-out's first joint, where the locked groove's takes over")] if ON['leadin'] and ON['reveal'] and ON['stop'] and not ON['spiral'] else []) +
                       ([(RUNS_DOWN if not ON['spiral'] else 0, f"the needle has gone in: the hiss's band has slid down with the radius ({SPIRAL['radius'][0]:g} mm to {SPIRAL['radius'][1]:g} mm, evenly): {SPIRAL['hp']} to {SPIRAL['lp']} Hz in bar 1, {round(SPIRAL['hp'] * inner(clock(BARS)))} to {round(SPIRAL['lp'] * inner(clock(BARS)))} Hz at the last stroke, {round(SURFACE['hp'] * inner())} to {round(SURFACE['lp'] * inner())} Hz in the locked groove ({SPIRAL['radius'][2]:g} mm); its level held: {-10 * log10(inner(clock(BARS))):.1f} dB more at the last stroke")] if ON['inner'] and ON['leadin'] and (ON['spiral'] or ON['reveal']) and ON['stop'] else []) +
                       ([(BARS, f"the record's surface is heard from the first joint on, the same hiss every turn" + (f", to {lifted():.1f} s" if lifted() else ''))] if ON['surface'] and ON['stop'] else []) +
                       ([(BARS, f"the needle is lifted at {lifted():.1f} s: a soft thump, and the surface is gone at once; {LIFT['rest']:g} s of nothing (Give or Take begins with a record being started)")] if lifted() else []) +
                       ([(BARS, "Ring True's strings hear the hour bell: the B flat 2 string is its note and the F2 string has its fifth: they ring with it")] if ON['sympathy'] and ON['one'] and ON['hour'] and ON['strings'] else []) +
                       ([(RUNS_DOWN // 4, f"the clock's bells are struck: a hammer, {HAMMER['ms']} ms of noise on the front of every chime note")] if ON['hammer'] and (ON['quarters'] or ON['hour']) else []) +
                       ([(RUNS_DOWN, f"the clock on the wall: a tick at every whole second from {int(clock(RUNS_DOWN)) + 1} s to {int(clock(BARS)) + WALL['after']} s, {WALL['after']} of them after the last stroke")] if ON['wall'] and ON['stop'] else []) +
                       ([(b, 'the drum gives the one to whoever has just left') for b in range(BARS) if ON['left'] and any(tr != 'kick' for tr, _ in left(b))] if ON['cede'] else []) +
                       ([(GOES['cell'] - 1, "the hand lets go of the stick: the cell's last stroke bounces")] if ON['drop'] else []) +
                       ([(COMES['meetings'], 'each meeting is heard to part: the two cycles that met click once more, 3, 5 or 7 sixteenths on')] if ON['part'] else []) +
                       ([(GOES['ghost'] - REAL['bars'], 'the bass is given its fundamental')] if ON['real'] else []) +
                       ([(GOES['pattern'] - LEAVE, 'the pattern slips a sixteenth a bar')] if ON['slip'] else []) +
                       ([(GOES['room'] - SING['bars'], 'the walls come in until they sing')] if ON['sing'] else []) +
                       ([(RUNS_DOWN if ON['early'] else BARS, "Ring True's strings are let go beside the click")] if ON['strings'] else []) +
                       ([(COMES['meetings'], 'the drum answers each meeting that lands on it')] if ON['knock'] else []) +
                       ([(GOES['room'], "the strings are let go beside the cell, and ring while it rings true")] if ON['true'] and ON['strings'] else []) +
                       ([(b // 4, f"all three meet on the drum: the triad turns over ({' '.join(TURNED[(b // PAGE - COMES['meetings'] * 4 // PAGE) % len(TURNED)][c] for c in CYCLES)})") for b in range(0, GOES['meetings'] * 4, PAGE) if b >= COMES['meetings'] * 4] if ON['turn'] and ON['knock'] else []) +
                       ([(GOES['change'] - 1, "the change's last seed is paid in the smallest coins: a held B flat")] if ON['paid'] else []) +
                       ([(GOES['cell'], "the strings answer the dropped stroke: held open through the bar after the cell, then let down")] if ON['answer'] and ON['true'] and ON['strings'] and ON['drop'] else []) +
                       ([(GOES['change'] - 1, "the last seed is paid with interest: the held B flat swells and is shut on the one")] if ON['interest'] and ON['paid'] else []) +
                       ([(DRUM_IN, 'the drum has a chest: a bell of 4 dB at 71 Hz')] if ON['chest'] else []) +
                       ([(GOES['cell'] - NUDGE['bars'], 'the hand drags the cell a sixteenth late and lets it catch up')] if ON['nudge'] else []) +
                       ([(min(COMES[k] for k in GATHER if COMES[k]), "each of the seven is counted in as it comes: the notched stick's row in the bar it comes, a notch for each one here, climbing to its click on beat 3 (the rows that count them out fall away after theirs): " + ', '.join(f"bar {COMES[k] + 1}: {tally_count(COMES[k])}" for k in GATHER if COMES[k] and not caught(COMES[k])))] if ON['entered'] and ON['tally'] else []) +
                       ([(TALLY['bars'][1], f"the stick is laid down: one tap of its lowest notch ({LAID['pitch']}) on beat 3, where the next row would have been")] if ON['laid'] and ON['tally'] else []) +
                       ([(elder_count()[0]['at'] // 4, f"the big brother counts its own eleven before the small one comes, as in Least Common: its bar again every {ELEVEN['beats']} beats, {-COUNTS['db']} dB under its strokes from home (not on its own strokes, not in a caught bar): " + ', '.join(f"bar {q['at'] // 4 + 1} beat {q['at'] % 4 + 1}" for q in elder_count()))] if elder_count() else []))
        for bar, what in marks:
            t = clock(bar)
            print(f'bar {bar + 1:3d}  {int(t) // 60}:{t % 60:05.2f}  {what}')
        T = build()
        print(f'{BARS} bars, {clock(BARS):.1f} s to the last stroke; strokes: ' + ', '.join(f'{k} {len(v)}' for k, v in T.items() if v or k not in ('held', 'under')))
        ticks = [clock(RUNS_DOWN + (bar * 16 + s) / 16) for bar in range(WIND) for s in (2, 6, 10, 14)] + [clock(BARS)]
        print('the spring: the gap between ticks goes ' + ' '.join(f'{(b - a) * 1000:.0f}' for a, b in zip(ticks, ticks[1:]))[:60] + ' ... ' +
              ' '.join(f'{(b - a) * 1000:.0f}' for a, b in zip(ticks[-5:], ticks[-4:])) + ' ms (the last is the half beat to the one)')
    else:
        a.out.write_text(dump(song()))
