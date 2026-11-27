#!/usr/bin/env python3
"""Least Common (chirpers11, track 2). Clicky minimal techno, 126 BPM, G minor, 210 bars (6:40).

THE RULE. Three clicks keep cycles of 3, 5 and 7 sixteenths against a bass drum on every fourth. They are never
told what to do after that: everything else in the song is what happens when they MEET.
  two meet   -> a ping. 3 with 5 (every 15 sixteenths) rings D, 3 with 7 (every 21) B flat, 5 with 7 (every 35) F.
  three meet -> a chord (every 105 sixteenths: six bars and nine sixteenths).
  three meet ON THE BASS DRUM -> the song turns a page (every 420 sixteenths: 26 bars and a beat. So the pages turn
                on beat two, then beat three, then beat four).
  all meet ON THE ONE -> once in 105 bars (1680 sixteenths = 3 x 5 x 7 x 16). That is a HALF of the song.
Between two chords the pings fall on sixteenths 15 21 30 35 42 45 60 63 70 75 84 90: twelve notes, the same forwards
and backwards (gaps 15 6 9 5 7 3 15 3 7 5 9 6 15). Nobody wrote that tune. It comes round every 105 sixteenths, nine
sixteenths later in the bar each time, so it visits every sixteenth of the bar once before it is home.

THE SECOND HALF IS THE FIRST, ONE SIZE UP: cycles of 3, 5 and 7 BEATS against the bar of four. 3 x 5 x 7 x 4 beats is
105 bars again. Each long cycle is filled with the NEXT one's number, spread as evenly as it goes (Euclid): five
strokes in the three beats, seven in the five, three in the seven. Their meetings are the same tune four times
slower, so it is held, not struck: a tone that changes when two cycles begin together. From the seventh page the small
tune comes back over it (pings where cycles of 3, 5 and 7 sixteenths WOULD meet, though nobody is playing them): the
same tune at two sizes at once.

The four's own parts (bass, off-beat hat, clap) come in a page at a time and are the only things placed by page. The
chord is Give or Take's (track 1: G minor seventh) with its ninth on top, so the two songs can be laid over each other.

v2 (26 Nov): WHAT A MEETING DOES. In v1 a meeting was only a note. Six switches, each `--without-…` (all six off
is v1 byte for byte); every one is driven by the same count, how far it is to the next time all three meet:
  PLACE   the three and the five walk apart from the centre and back between two meetings of all three (the three
          to the left, the five to the right, the seven stays), so a chord is also three sounds arriving at one
          place. One size up in the second half: the walk takes a page.
  NEAR    the clicks are loudest where the three meet and NEAR dB quieter half way between.
  DOOR    a far room behind the clicks. Its door is shut when a page turns and opens a step each time the three
          meet (four steps to a page); the page turn shuts it again. In the last stretch of the first half, where the
          four stops, it is wide open: the clicks walk to the one alone in a hall. One size up in the second half:
          a step a page, wide open on the last.
  MEMORY  a click keeps the note of the last meeting it was in. The five's tock is on G after a chord, D after it
          meets the three, F after the seven; the seven's knock on G, B flat (the three), F (the five). Two tunes
          nobody wrote, in place of one note struck 400 times. Both are an octave under the pings.
  ROOTS   the bass keeps its rhythm and takes its note from the last meeting of any two (G2 after a chord, D2,
          B flat 2, F2): a bass line that the cycles write.
  BREAK   what the half does, one size down. Before each page of the first half turns, from the last time the five
          and the seven meet (35 sixteenths: two bars and three), the four stops, and the clicks walk to the page
          turn alone, the far room wide open. The page turns on the drum and the door shuts.

v3 (26 Nov): THE SPRING. The two halves were joined by a stop. Eight switches (`--without-rundown`, `-windup`,
`-through`, `-seven`, `-swing`, `-line`, `-rest`, `-wide`; all eight off is v2 byte for byte):
  RUNDOWN  the clock runs down by halves. In the last stretch of the first half (105 sixteenths, the four already
           stopped) each click loses every other stroke, and then every other one again: cycles of 3, 5 and 7
           sixteenths, then eighths, then beats. It is 3 against 5 against 7 at every size, and the size it
           reaches is the second half's, so the one arrives at the tempo the clicks have already come down to. A
           ping is as loud as the quieter of the two that meet, so the tune thins out with them.
  WINDUP   and is wound up at the end. In the last stretch of the second half the big cycles lose their fillings
           and the small cycles come back the same way backwards: every fourth stroke is already there (it is
           the head of the big cycle), then every second, then every one. The song reaches home at the size it
           began at, 3 against 5 against 7 sixteenths, so that it could begin again.
  THROUGH  the tune goes through the door as well. The pings, the chord and the held tone are sent to the far room
           (the clicks alone moved it 0.6 dB), so what a meeting makes is heard further off as the door opens.
  SEVEN    the seven was the quietest thing in the song (15 to 19 dB under the mix): 1.5 dB up.
  LINE     the bass keeps its line. In the second half it took its note from the big cycles' meetings and so held
           one note for five to nine bars: twenty slow changes that the scorer heard as twenty small sections,
           most of them alike. Now it goes on following the small cycles' meetings, as in the first half (nobody
           is playing them, but the drum's sixteenths still count them): the first half's tune stays in the bass
           under the second half's held tones, the same tune at two sizes from the one on.
  REST     the second half gets the breaks the first has, one size up: before each of its pages turns, from the
           last time the three and the five BEATS meet (60 sixteenths: three bars and three), the four stops
           and the clicks walk to the page turn alone.
  WIDE     the far room 6 dB up, so that the door is heard, and thinner (nothing under 900 Hz comes back from it).
  SWING    the door swings. It stepped open when the three met; now it opens all the way through each stretch,
           to the next step's place, so the tune moves off steadily and the page turn brings it back at once.

v4 (26 Nov): THE CLICKS GO THROUGH THE DOOR. In three rounds the door never moved the song more than 0.7 dB:
it was a room getting louder behind clicks that stayed where they were. Five switches (`--without-away`,
`-home`, `-slow`, `-push`, `-low`; all five off is v3 byte for byte):
  AWAY   the clicks walk off. As the door opens their own sound falls (AWAY dB by the last step) while what the
         far room gives back of them stays as it was: they have their own far room (`gone`), whose fader makes up
         exactly what their faders lose. The same strokes are further off each time the three meet, furthest in
         the break before the page turns, and the page turn puts them back in front of you at once. One size
         up in the second half: a step further a page. While the clock runs down they stand in front (they come
         back on the chord that begins it), so that the slowing is heard at full size.
  HOME   and they come home. Over the last stretch of the song, as the small cycles are wound back up, the clicks
         walk back from the far room to where they began, and the pings swell with them. The big cycles' fillings
         no longer fade as the small strokes come in: they stay whole to the half-way point, where the eighths
         have taken their place (v3's wind-up was 2 to 4 dB thinner above 5 kHz than what it replaced).
  SLOW   the clock runs down over two stretches, not one. In the first the four is still playing, so the clicks
         are heard to go from sixteenths to eighths AGAINST the drum; then the four stops and they go to beats
         alone. Twenty-five seconds in place of twelve.
  PUSH   on the last page of each half the off-beat hat is a sixteenth late: on the sixteenth the bass drum was
         cut short to leave empty, pushing into every beat.
  LOW    the bass 2 dB up (114 Hz stood 9.3 dB under the album's envelope).

v6 (26 Nov): THE DRUM ANSWERS. The second half's cycles of 3, 5 and 7 beats were never new: a click on a cycle of
3 sixteenths lands on the bass drum every 12 sixteenths, which is every 3 beats; the five every 5 beats; the seven
every 7. Those meetings, a click with the drum, were the only ones in the song that did nothing. One switch
(`--without-knock`; off is v5 byte for byte):
  KNOCK  from the first half's last page on, when a click lands on the drum the drum answers with a low knock (a
         small kettledrum head, new patch `lc-knock`): G for the three, B flat for the five, D for the seven. So
         under the last page of sixteenths a slow G minor triad is already turning in 3, 5 and 7 beats, two of its
         notes together every 15, 21 and 35 beats and all three exactly where the page turns; through the run-down
         it is what is left with the drum; and on the one the clicks take up those same three cycles, and the
         knock is now the head of each. It stops four bars before the end (the low end of a seam is the next
         song's). Its notes are 98 to 370 Hz, where this song stood 7 to 11 dB under the album's envelope.

v18 (27 Nov): THE LAST TURN IS HEARD. Two switches on (`--without-recap`, `-pause`; both off is v17 byte for byte)
and one built, rendered and left off (`--with-bars`). Read first: four tries had left the last turn (into page 8,
5:50) at 0.12 on the scorer's curve: a barer break (v16 BREATH: 0.16), the drum's note (v17), the hat waiting a page
(v17). This round read where the other turns' peaks ARE: page 7's (0.36) is thirteen sixteenths BEFORE its turn: on
the bass's held note coming into a bare break. It is not the pings: with the pings gone from page 7 it still reads
0.36. A turn is heard where a held, pitched thing comes into an empty band; the last turn's break was never empty,
because the bass walked through it.
  RECAP  the pings (the first half's tune, at the small cycles' own places, over the second half's held tones) come
         back on the LAST page, not on the seventh: the second half reads: page 5 the slow tune alone; page 6 the
         triad turns and the drum goes up; page 7 the hat, the clap that counts, the drum on D; page 8 home: the
         triad in its first position, the drum down a fifth onto its own note, and over them the tune the song
         began with. Page 7 loses its 48 pings; no stroke is added anywhere. Alone it does nothing for the turn
         (0.13) and is here for the form.
  PAUSE  v16's BREATH, a meeting longer: in the last break the walk is one step (D2, to the first meeting of the
         three and the five), then the bass, the held tone and the knocks rest for 7.5 beats (the clock and the
         clicks go on), then the bass leads the turn on D2 as it led the others. With RECAP the curve reads 0.23
         at the turn (0.18 and 0.19 with the short breath): a section at every cut, for the first time.
  BARS   (off) the same tune a third size up: cycles of 3, 5 and 7 BARS take exactly the half to meet (105 bars):
         their meetings held an octave under the held tones (D3, B flat 2, F2), resting in the breaks. Three builds
         (the whole half at -28 dB; the last page only at -24, with and without RECAP): each 0.8 to 1.1 under v17:
         a held tone under half the song makes its pages more alike in timbre (spread 4.8 dB for 5.3) and takes
         the recurrence share under its band (0.21 to 0.24 for 0.29), and it did not make a turn heard. Left off.
WHAT IT COSTS: 0.25 of the score on both seeds, and it is kept under v17: structure is whole (100 for 99.18) and the
variety term falls two points: the new last section is too like the page before it in timbre. That is the next job.

v17 (27 Nov): THE TRIAD TURNS OVER ON THE DRUM. Two switches: `--without-ground` (on; off is v16 byte for byte) and
`--with-last` (OFF: built, rendered on both seeds, and not shipped). Read
first: v7 turned the triad over a page at a time in the second half (the drum's answer: G2 B flat 2 D3, then B flat
2 D3 G3, then D3 G3 B flat 3, then home), 'under a song that never changed chord'. It never did: a chord is turned
over when its LOWEST note changes, and the lowest note of this song is the drum, which has rested on G1 for six
minutes and forty seconds, 843 strokes. And the last turn (into page 8, 5:50) is the least heard of the seven
(0.16 on the scorer's curve, the others 0.23 to 0.36), its peak 54 sixteenths late: page 8 did not sound different
from page 7 from its first beat.
  GROUND  in the second half the drum rests an octave under the triad's lowest note: G1 on page 5, B flat 1 on page
          6, D2 on page 7, and G1 again on the last page and at home. The inversions are real now (G minor, then
          over its third, then over its fifth: the chord that waits), and the last turn is a fall of a fifth onto
          the drum's own note, on the first stroke of the page: the bass has held D2 into every turn since v12, and
          this is the first time the drum answers it. No stroke is added, taken away or moved: only the drum's
          note on two pages. The machine's drum follows its note (bench: 49.8, 59.0 and 74.3 Hz; highest sample
          within 0.7 dB; 0.8 and 1.5 dB more body on the two higher notes).
  LAST    (off) the first build had GROUND alone and the scorer's curve did not move at the last turn (0.12, its
          peak still 54 sixteenths late): it does not hear a drum's note. What the other turns have and this one has
          not is somebody COMING IN: the bass and the clap on page 6, the hat and the pings on page 7; on page 8
          nobody: everything was in already. 'The four's own parts come in a page at a time' (the rule): so the
          hat waits a page. Page 7 has the pings, the counting clap and the drum on D, and no hat (88 strokes
          fewer); the hat comes in on the last page, on its first off-beat (the stroke it always played
          there), with its ring, as the drum falls to G. Nothing is added: the pickup that told of the hat before page 7 goes too; the one before page 8
          (the hat that rings) was there.
          RENDERED: the turn still reads 0.12 and the song 0.12 and 0.10 less (variety: a section fewer at one
          cut): above 5 kHz page 7 is 2.7 dB darker without its hat and the step into page 8 is 4 dB for 1.5,
          but the clicks own that band, not the hat: the hat's coming is not the event the pings' was. So it
          ships off, as BREATH did: the idea did not do what it was built for. `--with-last` is that build.

v16 (27 Nov): THE CLOCK IS STRUCK AS HARD AS THE CLICKS; AND THE LAST TURN, READ. Two switches: `--without-struck`
(on; off is v15 byte for byte) and `--with-breath` (OFF: built twice, rendered, and not shipped). Read first: of the seven page turns the scorer's novelty curve gives the last (into page 8,
5:50) 0.12, where the other six read 0.23 to 0.36: the turn the whole song walks to is the one that is least heard.
  BREATH  v12 gave the last break the bass's whole walk, and the break is full: the walk, the held tone, the
          drum's answers (rendered without the walk the turn reads 0.25, and the song 0.14 less: the scorer
          likes the low band filled). Small Change v15 and chirper-zero's rule: whoever is in a band takes
          the arrival from what enters it next. Every other turn the bass plays into is led by ONE note: the
          fifth, D, held fifteen sixteenths from the last meeting of the three and the five to the turn
          (pages 6 and 7 read 0.29 and 0.36). So the last turn is led the same way, and before the leading
          note the walk stops for breath: between the last two meetings of the three and the five (bar 183
          beat 2.5 to bar 184 beat 1.25) the walk's fifth and sixth notes are not played, the held tone is
          let go and the drum's three answers rest. The walk is D, D, B flat, F; a bar bare but for the
          clicks, their pings and one tick of the clock; then the D that leads every turn; then the page.
          THE FIRST BUILD left the last bar bare instead (the leading D with it): the turn read 0.16 and the
          song 0.2 less; and it took away the dominant the page is turned on. THIS BUILD read 0.16 as well,
          and 0.19 less (variety: the scorer then cuts pages 7 and 8 apart and finds them alike; spectrum:
          a bar with nothing at 114 Hz, the song's worst band). And the curve's peak is not at the turn
          but 54 sixteenths after it: a barer break is not the cure; the last page does not sound different
          from the seventh soon enough. So BREATH IS OFF: it is here for an ear to try (`--with-breath`).
  STRUCK  v15: the clock at -26 dB stands 9 to 15 dB over its band in the first half's stops and 2 dB in the
          last one. From the second half on the clicks are struck 4 dB harder (FORE) and their echoes fill
          the clock's band: so the clock is struck as much harder there as they are (its three later stops
          and nowhere else).

v15 (27 Nov): WHEN THE FOUR STOPS YOU CAN HEAR THE CLOCK. Two switches (`--without-wall`, `-leave`; both off is
v14 byte for byte):
  WALL   a page of this song is 105 beats at 126 to the minute: fifty seconds exactly, and the song is eight
         of them. So a clock that ticks once a second ticks fifty times a page, and every page turns on a
         tick. The album has such a clock (chirper-zero's, Give or Take v16 and v17: it ticks through that
         song's last four bars, which are this song's first four). Here it goes on, and is heard whenever
         the four stops: four ticks in each break before a turn of the first half (46 to 49 s, and so
         on), seven in each of the second half's (243 to 249 s ...), and twelve where this song's own
         clock runs down (188 to 199 s): 45 in all, tick and tock by turns, on the right. Against the
         sixteenths a second is 8.4 of them: the ticks fall on no grid of the song's, ten to every
         twenty-one beats. It is the album's clock and not a copy: its seconds are Give or Take's, which
         fall 32 ms after this song's (WALL['phase']), and its tick and tock are the ones that song would
         have reached. His sound under this song's names (lc-clock-tick, lc-clock-tock).
  LEAVE  v14 gave each part that comes in the last stroke before its turn. The other half (Wind Down v13:
         the bar after says who has left), by this song's own rule, that things happen where cycles meet:
         where the bass, the hat and the clap leave the drum alone (2:55 and 6:27.5) the hat and the clap
         each come back once, on the first stroke of its own part that falls where two of the clicks
         meet (where a ping sounds), 3 dB under. The hat on the 21st sixteenth after and the clap on the
         30th (2:57.5, 2:58.6); at the end the clap (6:30.0) and then the hat (6:34.6). Four strokes, each
         on its own place in the bar, each with a ping. NOT THE BASS: built first with its return as well
         (on the 60th sixteenth, the meeting's note): the song then lost two of the scorer's sections,
         the ones made by the bass's leaving (bars 96 and 209), and 2.3 points. A bass that comes back
         has not left. LEAVE['who'] has it for an ear to try.

v14 (27 Nov), THE LAST STROKE BEFORE A TURN IS THE NEWCOMER'S. One switch (`--without-tell`; off is v13 byte
for byte). The bass has said it is coming since v12 (its first note held to the turn). The four's other parts
came in on the turn with no word. Now each part that comes in on the next page plays, in the break before it,
the one last stroke it would have played before the turn had it been there, 3 dB under:
  into page 3   the hat: the last off-beat (two sixteenths before the turn)
  into page 4   the clap: the last two-or-four (two beats before)
  into page 6   the clap again (the second half's first page has none)
  into page 7   the hat (two sixteenths before) and the clap that counts with the three (two beats before, on
                the side its count would have had)
  into page 8   the hat that rings for the five: let ring two sixteenths and stopped on the turn
Six strokes in 402 s. Wind Down's rule (v12: the catch says who is coming), agreed with chirper-zero for the
onsets it adds (about 0.015 a second against Standing Room's 6.58).

v13 (27 Nov): THE FIVE'S HAT RINGS. Two switches (`--without-ring`, `-once`; both off is v12 byte for byte):
  RING   since v9 the hat counts with the five on page 8: the first hat after each of its knocks is 'let ring'
         (lc-open: the machine's hat with a decay of 450 ms, held half a beat). Small Change v12 found what
         that decay is: the time to fall 60 dB. At 450 ms the hat falls 16 dB by the next sixteenth and is
         gone under the clicks: a longer stroke, not an open hat, and the count was never heard as one. A new
         patch name, lc-rung: the same hat with a decay of 1.2 s (6 dB a sixteenth at 126), held three
         sixteenths (it was two) and then stopped, a sixteenth before the next shut hat. Sixteen strokes,
         every five beats: now the five has a hat that rings.
  ONCE   and it is heard before it counts (Ring True v11: shown once before). On page 4 the drum gives three
         beats to its answer (v11 LEND: bars 83, 87, 91). The first hat after each of those beats now rings
         too: where the drum is not, the hat is let go. Three strokes; no stroke is added (each was a shut
         hat). Needs RING (with it off, ONCE does nothing).

v12 (27 Nov): THE LAST TURN. Two switches (`--without-led`, `-walk`; both off is v11 byte for byte):
  LED    since v11 the bass comes back a bar early before four page turns, on D, held into the G the drum
         returns on. The two turns it did not lead were the two where the bass COMES IN (into page 2, its
         first note of the song; into page 6, its first of the second half). Now those are led too: the
         bass's first note is the fifth, held fifteen sixteenths into the one. Every turn the bass plays
         after is led by it.
  WALK   v11 first held every meeting of every break and found a break with the bass's band filled is no
         longer a break (the scorer's sections 10 to 7, 1.1 off), so only the last note was kept. The whole
         line is given ONE break: the last turn of the song (into page 8, bars 181 to 184). There the bass
         takes each meeting's note as the clicks make it and holds it to the next: D, D, B flat, F, D, B
         flat, D. The one break that is not one is the one before the last page.

v11 (26 Nov): THE BASS WALKS TO THE PAGE TURN. Two switches (`--without-hold`, `-lend`; both off is v10 byte
for byte):
  HOLD   before a page turns the four stops and the clicks walk to the turn alone, meeting two at a time as they
         go. Since v2 the bass has played the note of the last meeting; in the break it stopped with the others.
         Now it comes back EARLY: at the break's last meeting of two (the three and the five, fifteen sixteenths
         before the turn) it takes that meeting's note, D, and holds it to the turn, with no drum over it, 10 dB
         under where it plays in the groove; and the turn's own note, G, is the one the drum comes back on. A
         fifth below the one, held into it: the page turn is led into. Only where the bass is already in (the
         turns into pages 3, 4, 7 and 8), and not in the run-down (the card on it is not answered).
         FIRST BUILT WITH EVERY MEETING HELD (F, D, B flat, D; and D, D, B flat, F, D, B flat, D): a slow line
         under the whole break. Rendered in full it scored 1.1 LOWER (97.03 and 96.88 for 98.16 and 98.09): the
         scorer's sections fell from 10 and 9 to 7 and 6 at its two highest cuts, because a break with the
         bass's band filled is less of a break and the page turns stopped reading as boundaries. That is a
         musical fact too, not only the scorer's. `HOLD['last'] = 0` is that build.
  LEND   page 6's turn (v10: the drum rests where the three and the five meet on it, and the knock has the
         beat) is given to the first half as well, one size down: on page 4, where the three and the five
         SIXTEENTHS meet on the drum, fifteen beats apart, the drum rests three times before the clock begins to
         run down, and the knock (which comes in on that page) has the beat. The two halves rhyme.

v10 (26 Nov): EACH OF THE FOUR TAKES A TURN. Since v9 the clap counts with the three on page 7 and the hat with
the five on page 8; the drum and the bass had not left the four. Three switches (`--without-skip`, `-leap`, `-back`;
all three off is v9 byte for byte):
  SKIP   on page 6 (bars 132 to 154) the drum rests on the beat where the three and the five meet: every fifteen
         beats after the turn (15, 30, 45, 60, 75). Its answer still sounds there (the knock, two notes): the
         beat is given to the answer. The sixth time (90 beats) is where the four stops for the page turn, as it
         always did: five single beats missing, and then the drum stays away for fifteen. The break is counted
         in, in fifteens.
  LEAP   on page 8 (bars 185 to 204) the bass counts with the seven: the bass note after each of the seven's
         knocks is played an octave up, twelve times, seven beats apart. So on the last two pages the clap has
         the three, the hat the five and the bass the seven, and before them the drum has the three and five
         together.
  BACK   since v8 the clicks are struck 4 dB harder through the second half and nothing else was: in the
         finished song its pages read 2 dB more above 1 kHz than the first half's and 0.6 to 0.8 dB less from
         60 to 130 Hz, where the song already stands 5 to 8 dB under the album. The bass is given 2 dB back
         from the second half on (the leaping notes with it: they are struck as hard as the notes round them).

v9 (26 Nov): THE CLAP CHANGES SIDES. Everything that counted three, five and seven was a click, a ping or a
knock; the four's own parts (the drum, the bass, the hat, the clap) never left the four. Three switches
(`--without-count`, `-sway`, `-open`; all three off is v8 byte for byte):
  COUNT  on page 7 (bars 158 to 180, until the four stops for the page turn) the clap leaves the four and
         counts with the three. The three's cycle is three beats there and the drum answers its first beat with
         a knock (v6); the clap now falls on its second: knock, clap, nothing, thirty times, a slow three over
         the drum's four. Two and four are not played for 45 seconds. On page 8 the clap is back on two and
         four, and the hat is late (v4): the four's parts take their turns at not being where they were.
  SWAY   while it counts three the clap stands to one side and then the other, turn about (0.5 each way): a
         cycle of six beats from left to left, over bars of four.
  OPEN   on page 8 (bars 185 to 204, where the hat is a sixteenth late and the clap is back on two and four) the
         hat counts with the five: the first hat after each of the five's knocks is let ring (`lc-open`, a new
         sound: the same hat with ten times the ring, held half a beat) in place of the shut one. Knock, and the hat opens: once
         every five beats, sixteen times. So the last two pages hand the four's parts to the cycles one at a
         time, the clap to the three and then the hat to the five, before the clock runs down.

v8 (26 Nov): THE SECOND HALF REMEMBERS THE FIRST. On page 6 the three clicks stood 20 to 22 dB under the mix: the
second half was a low-end piece with the clicks far behind it, on an album of clicks. Two switches
(`--without-ghost`, `-fore`; both off is v7 byte for byte):
  GHOST  in the first half the clicks count 3, 5 and 7 sixteenths; in the second, 3, 5 and 7 beats. Now in the
         second half each click has an echo, and the echo keeps its old cycle: the three's comes back every 3
         sixteenths, the five's every 5, the seven's every 7, each time half as loud, from the other side of
         the room. Nobody plays the small cycles there, and they are heard all the same, under the big ones:
         both sizes of the same three numbers at once. In the last stretch, as the small cycles are wound back
         up and played again, the echoes go.
  FORE   and the clicks are struck FORE dB harder through the second half, until that last stretch.

v7 (26 Nov): THE TRIAD TURNS OVER. The drum's answer (v6) was the same three notes in the same three cycles for
four minutes: every page of 105 beats the same low tune. Three switches (`--without-turn`, `-carry`, `-tame`; all
three off is v6 byte for byte):
  TURN   one size up again. The three notes turn in 3, 5 and 7 beats; now the triad itself turns over once in the
         second half, an inversion a page. On the one it is as it was (G2 B flat 2 D3: the three's note lowest and
         commonest); when the page turns the lowest note goes to the top (B flat 2, D3, G3), and again (D3, G3,
         B flat 3), and on the last page it is home (G2, B flat 2, D3). The note heard every three beats is
         G, then B flat, then D, then G: the song's chord, a page a note, under a song that never changed chord.
  CARRY  in the second half the four stops for fifteen beats before each page turns, and the drum's answer
         stopped with it. Now the answer goes on without the question: the knocks keep their beats through the
         break, CARRY_DB down, with the slow clicks and the held tone, and the page turns on the whole triad.
  TAME   the pings' commonest note, D5 (587 Hz), 3 dB down by an EQ on their track: 547 and 641 Hz have stood
         about 7 dB over the album's envelope since v2, and by solo the pings are half of what the song has from
         250 Hz to 1 kHz on the first half's pages.

v5 (26 Nov): ONLY THE DRUM. Read by solo, v4's slow run-down was a change of rhythm 14 to 19 dB under the four,
and the second half's four pages all stood at one level. Three switches (`--without-bare`, `-small`, `-rise`;
all three off is v4 byte for byte):
  BARE   as the clock begins to run down only the drum is left of the four (as it is in the last stretch of the
         song): the bass, the hat and the clap stop a stretch before the drum does, and the clicks stand at full
         height through the run-down (no ride down between meetings). So the first half of the run-down is three
         clicks going from sixteenths to eighths against a drum and nothing else.
  SMALL  the second half begins as the first did. The first half's first page has no bass (three clicks and a
         drum); one size up, the second half's first page has none either: three slow clicks, the held tones
         and the drum. The bass comes back with the page turn, and the clap with it.
  RISE   the wind-up's sixteenths come in from 12 dB down, not 24 (its third quarter stood 3.6 dB under the page
         before it above 5 kHz).
A fourth was tried and dropped: the drum's body moved from 130 Hz to 110 (114 Hz stands 8.7 dB under the album's
envelope). Read on a page where nothing else had changed it moved 105 to 123 Hz by 0.2 dB: the drum has nothing there.

Form as arithmetic: everything below is computed from CYCLES, BAR and BEAT. Nothing is typed as a bar number.
"""
import argparse
import json
from math import lcm, log10
from pathlib import Path

BPM = 126
BEAT, BAR = 4, 16                       # sixteenths
CYCLES = (3, 5, 7)                      # the three clicks, sixteenths (first half) or beats (second half)
VOICES = ('three', 'five', 'seven')
SUPER = lcm(*CYCLES)                    # 105: the three meet
PAGE = lcm(SUPER, BEAT)                 # 420: the three meet on the bass drum
HALF = lcm(SUPER, BAR)                  # 1680: all meet on the one (105 bars)
TOTAL = 2 * HALF
assert (SUPER, PAGE, HALF) == (105, 420, 1680) and HALF % BAR == 0 and PAGE // BEAT % 4 == 1
KEY = 'G'
PING = {(3, 5): 'D5', (3, 7): 'Bb4', (5, 7): 'F4'}          # the commonest meeting gets the plainest note
TONE = {(3, 5): 'D4', (3, 7): 'Bb3', (5, 7): 'F3'}           # the same three notes an octave down, held
CHORD = ('G3', 'Bb3', 'D4', 'F4', 'A4')
OUT = Path(__file__).resolve().parents[3] / 'songs/chirpers11-t2.yaml'

# ---- v2: the switches and their numbers. Nothing above is changed by them.
ON = {'place': True, 'near': True, 'door': True, 'memory': True, 'roots': True, 'break': True,
      'rundown': True, 'windup': True, 'through': True, 'seven': True, 'swing': True, 'line': True, 'rest': True, 'wide': True,
      'away': True, 'home': True, 'slow': True, 'push': True, 'low': True,
      'bare': True, 'small': True, 'rise': True, 'knock': True, 'turn': True, 'carry': True, 'tame': True, 'ghost': True, 'fore': True, 'count': True, 'sway': True, 'open': True, 'skip': True, 'leap': True, 'back': True, 'hold': True, 'lend': True, 'led': True, 'walk': True, 'ring': True, 'once': True, 'tell': True, 'wall': True, 'leave': True, 'breath': False, 'struck': True, 'ground': True, 'last': False, 'recap': True, 'pause': True, 'bars': False}
PAUSE = {'page': 7, 'meet': (3, 5), 'who': ('bass', 'tone', 'knock'), 'from': 3}   # v18: v16's BREATH, a meeting longer: the page before whose turn the low band is left bare; the two cycles; the tracks that rest; how many of their meetings before the turn the rest begins (it ends at the last, where the bass leads)
THIRD = {'notes': {(3, 5): 'D3', (3, 7): 'Bb2', (5, 7): 'F2'}, 'db': -24, 'vel': .7, 'from': 75}   # v18 BARS: the meetings of cycles of 3, 5 and 7 BARS: the tones' three notes an octave down again; the track's fader (the tones' own); velocity
RECAP = {'page': 7}                     # v18: the page (from 0) on which the pings come back in the second half (they came back on page 6)
GROUND = {'octaves': 1}                 # v17: how far under the triad's lowest note the drum rests in the second half
BREATH = {'page': 7, 'meet': (3, 5), 'who': ('bass', 'tone', 'knock')}   # v16: the page (from 0) before whose turn the low band is left bare; the two cycles between whose last two meetings before the turn it is; the tracks that rest there
WALL = {'gain': '-26dB', 'pan': 0.5, 'room': '-10dB', 'hz': (3600, 3000), 'parts': ((0.014, 0.35), (0.008, 0.5), (0.0, 1.0)), 'phase': 0.032}   # v15: the clock's fader (Give or Take's and Wind Down's is -20 dB: here that put its ticks 15 to 20 dB over their band and as high as -13 dBFS; at -32 it was lost in the later breaks), side and send (Give or Take's: 0.5, -10 dB); its two pallets, Hz; a tick's three sounds (seconds before the second, velocity); seconds the album's whole seconds fall after this song's
LEAVE = {'db': -3, 'who': ('hat', 'clap')}  # v15: dB on the one stroke a part plays after it has left; the parts that do (with 'bass' as well the scorer lost two sections, at bars 96 and 209: its return undoes the leaving)
TELL = {'db': -3, 'hat': (2, 3, 6, 7), 'clap': (3, 5, 6, 7), 'ring': 2}   # v14: dB on a pickup; the pages (from 0) the hat and the clap play on (as build() has them); sixteenths the rung pickup is held (to the turn)
RING = {'patch': 'lc-rung', 'decay': '1200ms', 'release': '100ms', 'len': 3}   # v13: the hat that rings for the five: its patch; the time it takes to fall 60 dB; how fast it is stopped; sixteenths it is held (it was 2)
LED = (1, 5)                            # v12: the pages (from 0) on which the bass comes in: the turn into each is led as well
WALK = 7                                # v12: the page (from 0) whose turn the bass walks into, holding every meeting's note
HOLD = {'db': -13, 'vel': .8, 'pages': (2, 3, 6, 7), 'last': 1}   # v11: dB and touch on the held notes (the bass is not ducked there: no drum); the pages (from 0) whose turn the bass walks into; how many of the break's last meetings it holds (0: all of them).
# Bench (hold.sh, holdread.py, raw, by beat): at -3 dB the held bass alone read -24.5 dBFS through the first half's break, where everything else reads -36.8 and the groove before it -21.8: the break was 12 dB up and no longer a break (10 dB up and level with the groove in the second half's). 10 dB less: under the clicks, not over them
LEND = {'page': 3, 'meet': (3, 5)}     # v11: the first half's page (from 0) on which the drum rests where two of the small cycles meet on it; the two
BACK = 2                                # v10: dB on the bass through the second half
SKIP = {'page': 5, 'meet': (3, 5)}     # v10: the page (from 0) on which the drum rests where two cycles meet; the two
LEAP = {'page': 7, 'cycle': 7, 'within': 6, 'db': -2}   # v10: the page on which the bass counts with a cycle; the cycle, beats; sixteenths after its knock within which the bass's next note is looked for; dB on that note, an octave up
COUNT = {'page': 6, 'cycle': 3, 'beat': 1}   # v9: the page (from 0) on which the clap counts with a cycle; the cycle, beats; the beat of it the clap falls on (from 0: the one after the knock)
SWAY = {'pan': 0.5, 'db': 2.5}          # v9: how far to each side the clap stands while it counts; dB on it there.
# Bench (count.sh, countread.py: page 7's first nine bars by beat): at the clap's own fader the claps to the sides read -43 to -45 a beat where the clap in the middle read -41 (what a side costs): so 2.5 dB
OPEN = {'page': 7, 'cycle': 5, 'gain': '0dB'}   # v9: the page on which the hat counts with a cycle; the cycle, beats; the open hat's fader (the shut hat's is 6 dB).
# Bench (open.sh, openread.py: page 8's first ten bars): first with the machine's decay at 150 ms and the fader at 2 dB: by 30 ms -30 -40 -51 -61 -69 -75 where the shut hat reads -32 -52 -60 -66 -74 -80: a hat a
# little less shut, gone in 90 ms; not an open one. So 450 ms, held half a beat (the next shut hat stops it), 2 dB lower
LC_OPEN = {'about': "Least Common: the hat let ring, once every five beats: the first hat after the five's knock (v9). The drum machine's hat with ten times the shut one's ring, held half a beat.",
           'synth': {'layers': [{'type': 'machine', 'machine': {'part': 'hat', 'decay': '450ms'}}],
                     'amp': {'a': '0.1ms', 'd': '0s', 's': 1, 'r': '60ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.6}}
GHOST = {'feed': '-4dB', 'back': 0.5, 'hp': 300, 'side': {'three': 0.5, 'five': -0.5, 'seven': 0.0}}   # v8: what each click's echo takes of it, what it gives back of itself each pass, its high-pass, where it stands (the three walks left and the five right)
FORE = 4                                # v8: dB on the three clicks through the second half
# Bench, page 6's first sixteen bars, each click alone, by sixteenth (ghost.sh, ghostread.py). The three (struck on sixteenths 1 3 5 8 10 of twelve) read -36 -58 -38 -59 -36 -57 -65 -40 -63 -40 -61 -72 in v7; with its echo
# taking -6 dB of it: -36 -53 -38 -44 -36 -46 -52 -39 -53 -40 -47 -61: new strokes on 4, 6 and 11, 8 to 10 dB under the played ones, and a second echo on 7. The five's stood 10 under, the seven's 7 (it is in the middle: a bus
# to one side loses more). So -4 dB. With the clicks 3 dB harder they stood 20.9, 18.7 and 21.2 dB under the mix (v7 24.4, 22.1, 24.8) and 7.8, 7.3 and 8.8 above 300 Hz (10.1, 9.5, 11.1): so 4
TURNED = ({3: 'G2', 5: 'Bb2', 7: 'D3'}, {3: 'Bb2', 5: 'D3', 7: 'G3'}, {3: 'D3', 5: 'G3', 7: 'Bb3'})   # v7: the triad's three positions, by how many pages of the second half have turned (the fourth is the first again)
TURN_DB = (0, -1, -2)                   # v7: on the knock in each position. Bench, by solo: at one level the second inversion stood 2.7 dB under the mix from 200 to 400 Hz (v6's root position 7.5) and the first 4.6 (7.8): the head is the same size and its notes are higher
CARRY_DB = -6                           # v7: on a knock where the four has stopped. Bench, the break before page 6: with them the break reads -32.1 dB raw for -35.4 (under 250 Hz -34.5 for -43.0) and the groove before it -24.3: still a break, 8 dB down, with a low tune in it
TAME = 'peak cutoff=587 q=3 gain=-3dB'  # v7: on the pings. At q 1.4 it took 2.1 to 3.0 dB off everything from 400 Hz to 1 kHz (2.3 dB off the pings as a whole): a fader, not a note
KNOCK = {3: 'G2', 5: 'Bb2', 7: 'D3'}    # v6: the drum's answer to each click that lands on it
KNOCK_FROM = HALF - PAGE                # from the first half's last page
KNOCK_SEAM = 4 * BAR                    # and not in the last four bars
KNOCK_DB, KNOCK_HOLD = '-2dB', -10     # its fader, and the clip before it. Bench, alone on page 4: at 180 ms the head was a spike (-9.6 dBFS highest sample, 21 dB gone in 50 ms) carrying 13 dB less from 90 to 400 Hz than the bass or the drum. So it rings longer, the spike is clipped off, and the fader brings up what is left: at -4 dB it read 7 to 9 dB under the mix from 90 to 400 Hz and 4.4 under the bass; at -2 see the round's note
LC_KNOCK = {'about': "Least Common: the drum's answer when a click lands on it (v6). A small kettledrum head (modes 1 : 1.5 : 2 : 2.5, so on G2, B flat 2 and D3 everything it has is between 98 and 370 Hz), let ring 800 ms.",
            'synth': {'layers': [{'type': 'modal', 'modes': 'kettle', 'decay': '800ms', 'bright': 0.3, 'strike': 0.3}], 'amp': {'a': '0.5ms', 'd': '0s', 's': 1, 'r': '600ms'}},
            'play': {'event_stable': True, 'vel_sens': 0.4}}
RISE = -12                              # v5: dB the wind-up's strokes come in at
AWAY = 9                                # v4: dB the clicks' own sound has fallen when the door is wide open (their far room makes it up)
SWELL = 3                               # v4 HOME: dB the pings have risen by the end of the last stretch
LOW_DB = 2                              # v4 LOW: on the bass's fader
FLOOR = -24                             # dB a stroke has fallen to when it goes (RUNDOWN), or comes in at (WINDUP)
THROUGH = '-6dB'                        # the tune's send to the far room
THROUGH_DRY = -1.5                      # dB on the pings' own fader with it (547 Hz was 7.8 dB over the envelope already)
SEVEN_DB = 1.5                          # (2.5 put 641 Hz 9 dB over the envelope)
ALL = tuple(CYCLES)
WIDE = 0.8                              # how far from the centre a click stands when it is furthest from a meeting of all three
NEAR = 5                                # dB quieter there
LIFT = 2                                # dB on the clicks' faders with NEAR on (the ride takes 2.5 dB off on average)
DOOR = (-60, -12, -6, 0)                # the far room's fader, by how many times the three have met since the page turned
FAR = '-3dB'                            # each click's send to the far room
# The notes are the pings' own (D, B flat, F; G for the chord), each click an octave under the pings (the tock on the
# pings' own octave stacked with them, 13 dB over the envelope at 547 Hz; an octave over them, 12 over at 1.2 kHz).
MEMORY = {'five': {(3, 5): 'D4', (5, 7): 'F4', ALL: 'G4'}, 'seven': {(3, 7): 'Bb3', (5, 7): 'F3', ALL: 'G3'}}
ROOT = {(3, 5): 'D2', (3, 7): 'Bb2', (5, 7): 'F2', ALL: 'G2'}
ROOTS_DB = -3                           # the bass's fader with ROOTS on, beside v1's (this patch is 14 dB louder than the sine it replaces)
LC_ROOT = {'about': 'Least Common: the bass once the meetings write its line (v2). A sine and its octave, so that a line on 73 to 117 Hz is also heard on 147 to 233.',
           'synth': {'layers': [{'wave': 'sine'}, {'wave': 'sine', 'semi': 12, 'level': '-6dB'}], 'amp': {'a': '4ms', 'd': '0s', 's': 1, 'r': '60ms'}},
           'play': {'event_stable': True, 'vel_sens': 0.3}}
BREAK = lcm(*CYCLES[1:])                # 35: the last meeting of the five and the seven before a page turns
TURNS = [p * PAGE for p in range(1, HALF // PAGE)]   # the page turns of the first half (the half itself has its own, v1's)
REST = lcm(*CYCLES[:2]) * BEAT          # 60: v3, the second half's break. The last meeting of the three and the five BEATS before a page turns (3 bars and 3)
TURNS2 = [HALF + t for t in TURNS]      # the page turns of the second half
WIDE_DB = 6                             # v3: the far room's own fader (at 0 dB it added 0.6 dB to the clicks alone)
WIDE_HP = 900                           # and its high-pass with it (at 500 the wider room put 547 and 641 Hz 9 dB over the envelope and the low end 2 dB down beside them)


def broken(s):
    """Is sixteenth s in a break (the four stopped before a page turn)?"""
    return (ON['break'] and any(t - BREAK <= s < t for t in TURNS)) or (ON['rest'] and any(t - REST <= s < t for t in TURNS2))

TOCK = {'about': 'Least Common: the click that counts five, once it has a tune (v2). The same wooden bar damped twice as fast, so that a note it keeps for twenty strokes is a colour and not a drone.',
        'synth': {'layers': [{'type': 'modal', 'modes': 'bar', 'decay': '28ms', 'bright': 0.8, 'damp': 0.4, 'strike': 0.4}],
                  'amp': {'a': '0.2ms', 'd': '45ms', 's': 0, 'r': '20ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.7}}
TOCK_DB = 0                            # the five's fader with MEMORY on, beside v1's


def order(c, s):
    """2 where the cycle of c beats begins, 1 where the cycle of c eighths does, 0 on its other sixteenth strokes."""
    return 2 if s % (4 * c) == 0 else 1 if s % (2 * c) == 0 else 0


def rundown(c, s):
    """dB on the stroke of cycle c at sixteenth s in the last stretch of the first half (None: not played). The
    strokes of order 0 fall to FLOOR over the first half of the stretch and go; those of order 1 over the second."""
    w = SUPER * (2 if ON['slow'] else 1)                     # v4 SLOW: over two stretches, the first with the four still in
    if not ON['rundown'] or not HALF - w <= s < HALF or order(c, s) == 2:
        return 0
    x = (s - (HALF - w)) / w * 2 - (order(c, s) == 1)
    return None if x >= 1 else round(FLOOR * max(x, 0), 1)


def windup(c, s):
    """The same backwards in the last stretch of the second half: dB on a small-cycle stroke that the big cycle
    does not already play (None: not played). Order 1 comes up over the first half of the stretch, order 0 over the second."""
    if not ON['windup'] or not TOTAL - SUPER <= s < TOTAL or s % c:
        return None
    x = (s - (TOTAL - SUPER)) / SUPER * 2 - (order(c, s) == 0)
    return None if x < 0 else round((RISE if ON['rise'] else FLOOR) * (1 - min(x, 1)), 1)


def stretches():
    """(start, length, which step of four) in sixteenths, for every stretch between two meetings of all three: sixteen
    of 105 sixteenths in the first half (four to a page), four of 105 beats (a page each) in the second."""
    return ([(s, SUPER, s % PAGE // SUPER) for s in range(0, HALF, SUPER)] +
            [(s, PAGE, (s - HALF) // PAGE) for s in range(HALF, TOTAL, PAGE)])


def beats(s16):
    return ('%.4f' % (s16 / BEAT)).rstrip('0').rstrip('.') + 'b'


def running_down(s):
    """Is sixteenth s in the run-down (the last stretch of the first half; with SLOW the last two)?"""
    return ON['rundown'] and HALF - SUPER * (2 if ON['slow'] else 1) <= s < HALF


def bare(s):
    """v5: do the bass, the hat and the clap rest at sixteenth s? From where the clock begins to run down to the one
    (the drum goes on for the first of the two stretches; v1 let the bar that straddles its stopping play out)."""
    return ON['bare'] and ON['slow'] and running_down(s)


def walk(far, stand=False):
    """A lane that is 0 where the three meet and `far` half way to the next meeting, straight lines between. With
    `stand` (v5 BARE, the clicks' level) it stays at 0 through the run-down."""
    pts = []
    for s, n, _ in stretches():
        pts += [[beats(s), 0], [beats(s + n / 2), 0 if stand and ON['bare'] and running_down(s) else far]]
    return {'points': pts + [[beats(TOTAL), 0]], 'curve': 0}


def door():
    """The far room's fader: DOOR[k] through the k-th stretch since the page turned, stepping within a sixteenth."""
    pts = []
    for s, n, k in stretches():
        pts += [[beats(s), DOOR[k]], [beats(s + n - 1), DOOR[min(k + 1, len(DOOR) - 1) if ON['swing'] else k]]]
    return {'points': pts + [[beats(TOTAL), DOOR[-1]], [beats(TOTAL + BAR), DOOR[-1]]], 'curve': 0}

def away():
    """v4: dB on the clicks' own sound. 0 when a page turns and -AWAY when the door is wide open, moving as the door
    moves. With HOME it comes back to 0 over the last stretch of the song."""
    top, pts = len(DOOR) - 1, []
    w = SUPER * (2 if ON['slow'] else 1) * ON['rundown']     # while the clock runs down they stand in front
    for s, n, k in stretches():
        here = HALF - w <= s < HALF
        pts += [[beats(s), 0 if here else -AWAY * k / top], [beats(s + n - 1), 0 if here else -AWAY * (min(k + 1, top) if ON['swing'] else k) / top]]
    end = -AWAY
    if ON['home']:
        pts, end = [q for q in pts if float(q[0][:-1]) * BEAT < TOTAL - SUPER] + [[beats(TOTAL - SUPER), -AWAY]], 0
    return {'points': pts + [[beats(TOTAL), end], [beats(TOTAL + BAR), end]], 'curve': 0}


def at(lane, b):
    """A lane's value at beat b (straight lines between its points)."""
    pts = [(float(q[0][:-1]), q[1]) for q in lane['points']]
    for (b0, v0), (b1, v1) in zip(pts, pts[1:]):
        if b0 <= b <= b1:
            return v0 if b1 == b0 else v0 + (v1 - v0) * (b - b0) / (b1 - b0)
    return pts[-1][1] if b > pts[-1][0] else pts[0][1]


def gone():
    """v4: the fader of the clicks' own far room: the door's, plus what the clicks' faders have lost, at every point of either lane."""
    d, a = door(), away()
    bs = sorted({float(q[0][:-1]) for q in d['points'] + a['points']})
    return {'points': [[('%.4f' % b).rstrip('0').rstrip('.') + 'b', round(at(d, b) - at(a, b), 3)] for b in bs], 'curve': 0}


PATCHES = {
    'lc-kick': {'about': "Least Common: the four. The drum machine's bass drum resting on G, short enough to leave the sixteenth before the next beat empty.",
                'synth': {'layers': [{'type': 'machine', 'machine': {'part': 'kick', 'decay': '240ms', 'click': 0.55, 'drive': 0.2, 'punch': 20}}],
                          'amp': {'a': '0.1ms', 'd': '0s', 's': 1, 'r': '400ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.3}},
    'lc-three': {'about': 'Least Common: the click that counts three. Ten milliseconds of noise above 5 kHz: a tick with no note.',
                 'synth': {'layers': [{'type': 'noise', 'color': 'white'}], 'filters': ['hp cutoff=5000', 'peak cutoff=8500 q=2 gain=8dB'],
                           'amp': {'a': '0.1ms', 'd': '10ms', 's': 0, 'r': '8ms', 'curve': 3}}, 'play': {'event_stable': True, 'vel_sens': 0.7}},
    'lc-five': {'about': 'Least Common: the click that counts five. A small wooden bar (1 : 4 : 10) struck hard and damped at once: a tock on G.',
                'synth': {'layers': [{'type': 'modal', 'modes': 'bar', 'decay': '55ms', 'bright': 0.8, 'damp': 0.4, 'strike': 0.4}],
                          'amp': {'a': '0.2ms', 'd': '80ms', 's': 0, 'r': '30ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.7}},
    'lc-seven': {'about': "Least Common: the click that counts seven. The drum machine's rim, tuned to G: two short pings and a click, a knock.",
                 'synth': {'layers': [{'type': 'machine', 'machine': {'part': 'rim', 'decay': '45ms'}}],
                           'amp': {'a': '0.1ms', 'd': '0s', 's': 1, 'r': '120ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.7}},
    'lc-ping': {'about': 'Least Common: what two clicks make when they meet. A vibraphone bar with no motor, half a second long.',
                'synth': {'layers': [{'type': 'modal', 'modes': 'vibes', 'decay': '650ms', 'bright': 0.55, 'strike': 0.3}],
                          'amp': {'a': '0.3ms', 'd': '900ms', 's': 0, 'r': '200ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.5}},
    'lc-chord': {'about': 'Least Common: what three clicks make when they meet. A short filtered chord for a delay to carry.',
                 'synth': {'layers': [{'wave': 'saw', 'detune': -7}, {'wave': 'saw', 'detune': 7}, {'wave': 'pulse', 'level': '-8dB'}],
                           'filters': [{'kind': 'lp', 'cutoff': {'value': 500, 'mod': [{'src': 'env.f', 'amount': 2.6}]}, 'q': 1.4}],
                           'env': {'f': {'a': '1ms', 'd': '140ms', 's': 0, 'r': '80ms'}},
                           'amp': {'a': '1ms', 'd': '220ms', 's': 0, 'r': '90ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.4}},
    'lc-tone': {'about': 'Least Common: the meetings one size up. A plain held tone, a sine and a little of its octave, that takes a beat to arrive.',
                'synth': {'layers': [{'wave': 'sine'}, {'wave': 'triangle', 'semi': 12, 'level': '-16dB'}],
                          'amp': {'a': '240ms', 'd': '0s', 's': 1, 'r': '900ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.2}},
    'lc-hat': {'about': "Least Common: the off beat. The drum machine's hat, closed.",
               'synth': {'layers': [{'type': 'machine', 'machine': {'part': 'hat', 'decay': '45ms'}}],
                         'amp': {'a': '0.1ms', 'd': '0s', 's': 1, 'r': '120ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.6}},
    'lc-clap': {'about': "Least Common: two and four. The drum machine's clap, short.",
                'synth': {'layers': [{'type': 'machine', 'machine': {'part': 'clap', 'decay': '140ms', 'bursts': 3}}],
                          'amp': {'a': '0.1ms', 'd': '0s', 's': 1, 'r': '300ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.5}},
}


def euclid(k, n):
    """k strokes spread over n steps as evenly as they go, the first on the first step."""
    return [i * n // k for i in range(k)]


def touch(pos):
    """How hard a click lands: hardest where it catches the bass drum, lighter on the off beat, lightest between."""
    return .92 if pos % BEAT == 0 else .74 if pos % BEAT == 2 else .58


def told(t):
    """v14: (track, sixteenth, length) of the one last stroke each of the four's parts that comes in on the page after turn t would have played before t. On the grid of the page it is leaving."""
    page, out = t // PAGE, []
    if page in hat_pages() and page - 1 not in hat_pages() and not (ON['last'] and ON['open'] and ON['ring'] and page == OPEN['page']):   # v17 LAST: where the hat that rings already tells, it tells once
        out.append(('hat', max(x for x in range(t - BAR, t) if x % BAR in (2, 6, 10, 14)), 1))
    if page in TELL['clap'] and page - 1 not in TELL['clap']:
        out.append(('clap', max(x for x in range(t - BAR, t) if x % BAR in (4, 12)), 1))
    if ON['count'] and page == COUNT['page']:
        x = max(x for x in range(t - COUNT['cycle'] * BEAT, t) if (x - HALF) % (COUNT['cycle'] * BEAT) == COUNT['beat'] * BEAT)
        out.append(('clap-' + 'lr'[(x - HALF) // (COUNT['cycle'] * BEAT) % 2] if ON['sway'] else 'clap', x, 1))
    if ON['open'] and ON['ring'] and page == OPEN['page']:
        out.append(('open', max(x for x in range(t - BAR, t) if x % BAR in (2, 6, 10, 14)), TELL['ring']))
    return sorted(out, key=lambda o: o[1])


def stopped(s):
    """v15: has the four stopped at sixteenth s (a break before a page turn, or the first half's last stretch)?"""
    return broken(s) or HALF - SUPER <= s < HALF


def wall():
    """v15: the wall clock's notes, (tick's, tock's): three sounds a tick, at every whole second of the album's clock that falls where the four has stopped. This song's even seconds are Give or Take's odd ones: ticks."""
    out = ([], [])
    for sec in range(1, TOTAL * 60 // (BPM * BEAT) + 1):
        t = sec + WALL['phase']
        if stopped(int(t * BPM * BEAT / 60)):
            out[sec % 2].extend({'at': round((t - early) * BPM / 60, 5), 'len': 0.05, 'pitch': 'C6', 'vel': vel, **({'gain': f'{FORE}dB'} if ON['struck'] and ON['fore'] and t * BPM * BEAT / 60 >= HALF else {})} for early, vel in WALL['parts'])
    return out


def leaves(lo, hi):
    """v15: (track, sixteenth, length) for each of the four's parts that plays on the page of sixteenth lo and has left the drum alone from lo to hi: the first stroke its own part would have played there that falls where exactly two of the clicks meet (where a ping sounds). In the second half the bar that straddles lo is played out, so the search begins at the next bar line."""
    page, out = lo // PAGE, []
    late = 1 if ON['push'] and page % (HALF // PAGE) == HALF // PAGE - 1 else 0
    for tr, lens, here in (('bass', {2: 1.5, 7: 1, 10: 1, 14: 1.5}, page >= 1), ('hat', {o + late: 1 for o in (2, 6, 10, 14)}, page in hat_pages()), ('clap', {4: 1, 12: 1}, page in (3, 5, 6, 7))):
        own = [(s0 + o, ln) for s0 in range(lo // BAR * BAR, hi, BAR) for o, ln in sorted(lens.items()) if lo <= s0 + o < hi and (s0 >= lo or lo < HALF)]
        hit = [(x, ln) for x, ln in own if len([c for c in CYCLES if x % c == 0]) == 2]
        if here and hit and tr in LEAVE['who']:
            out.append((tr, *hit[0]))
    return sorted(out, key=lambda o: o[1])


def hat_pages():
    """v17 LAST: the pages (from 0) the hat plays on: v14's TELL['hat'], and with LAST not the second half's third page: it waits for the last."""
    return tuple(p for p in TELL['hat'] if not (ON['last'] and p == HALF // PAGE + 2))


def ground(s):
    """v17 GROUND: the drum's note at sixteenth s: in the second half, GROUND['octaves'] under the lowest note of the page's triad (v7's TURNED); G1 before it and at home."""
    if not (ON['ground'] and ON['turn'] and ON['knock']) or not HALF <= s < TOTAL:
        return 'G1'
    low = TURNED[(s - HALF) // PAGE % len(TURNED)][CYCLES[0]]
    return f"{low[:-1]}{int(low[-1]) - GROUND['octaves']}"


def build():
    T = {n: [] for n in ('kick', 'three', 'five', 'seven', 'ping', 'chord', 'tone', 'bass', 'hat', 'clap')}
    marks = []

    def add(tr, s16, len16, pitch, vel, **more):
        T[tr].append({'at': round(s16 / BEAT, 4), 'len': round(len16 / BEAT, 4), 'pitch': pitch, 'vel': round(vel, 3), **more})

    if ON['knock']:
        T['knock'] = []
    if ON['count'] and ON['sway']:
        T['clap-l'], T['clap-r'] = [], []
    if ON['open']:
        T['open'] = []

    def knock(s, db=0):
        """v6: the drum's answer at sixteenth s, a note for each click whose cycle lands on it (every 3, 5 and 7 beats)."""
        if ON['knock'] and KNOCK_FROM <= s < TOTAL - KNOCK_SEAM:
            notes = TURNED[(s - HALF) // PAGE % len(TURNED)] if ON['turn'] and s >= HALF else KNOCK
            for c in CYCLES:
                if s % (c * BEAT) == 0:
                    g = db + (TURN_DB[(s - HALF) // PAGE % len(TURNED)] if ON['turn'] and s >= HALF else 0)
                    add('knock', s, 2, notes[c], .85, **({'gain': f'{g}dB'} if g else {}))

    pitch = {'three': 'C6', 'five': 'G5', 'seven': 'G4'}
    mem = dict(pitch)
    roots = []                                                # the note of the last meeting of any two, at every sixteenth
    # ---- the first half: cycles of 3, 5 and 7 sixteenths. Who is in, by supercycle (the three meet at each one's head).
    supers = HALF // SUPER                                    # 16
    pages = HALF // PAGE                                      # 4
    per_page = PAGE // SUPER                                  # 4
    enters = {'three': 0, 'five': 1, 'seven': 2}              # one more click each time the three would have met
    last = supers - 1                                         # the last supercycle of the half: the four stops, to come back on the one
    for s in range(0, HALF):
        n = s // SUPER
        here = [c for c, v in zip(CYCLES, VOICES) if s % c == 0 and (n >= enters[v] or s == 0)]
        if ON['memory'] and len(here) >= 2:                   # a click keeps the note of the last meeting it was in
            for c, v in zip(CYCLES, VOICES):
                if c in here and v in MEMORY:
                    mem[v] = MEMORY[v][tuple(here)]
        loud = {c: rundown(c, s) for c in here}               # v3: 0 dB everywhere but in the last stretch
        for c, v in zip(CYCLES, VOICES):
            if c in here and loud[c] is not None:
                add(v, s, 1, mem[v], touch(s), **({'gain': f'{loud[c]}dB'} if loud[c] else {}))
        met = tuple(c for c in CYCLES if s % c == 0)
        roots.append(ROOT[met] if len(met) >= 2 else roots[-1])
        if len(here) == 2 and None not in loud.values():     # a meeting is as loud as the quieter of the two
            add('ping', s, 4, PING[tuple(here)], .8, **({'gain': f'{min(loud.values())}dB'} if min(loud.values()) else {}))
        if len(here) == 3:
            add('chord', s, 2, ','.join(CHORD), .85 if s % BEAT == 0 else .7)
        if s % BEAT == 0 and n != last and not broken(s):
            if not (ON['lend'] and ON['knock'] and s // PAGE == LEND['page'] and not running_down(s) and met == LEND['meet']):   # v11 LEND: the beat is the answer's
                add('kick', s, 2, ground(s), .95 if s % BAR == 0 else .88)
            knock(s)
    marks += [('first half: three, five and seven sixteenths', 0)] + [(f'page {p + 1} (the three meet on beat {p * PAGE // BEAT % 4 + 1})', p * PAGE) for p in range(1, pages)]
    marks += [('the clock begins to run down, ' + ('only the drum left of the four' if ON['bare'] else 'the four still playing'), (last - 1) * SUPER)] * (ON['slow'] and ON['rundown']) + [('the four stops', last * SUPER)]
    # ---- the second half: one size up. Cycles of 3, 5 and 7 beats, each filled with the next one's number.
    fill = {c: euclid(CYCLES[(i + 1) % 3], c * BEAT) for i, c in enumerate(CYCLES)}
    assert [len(fill[c]) for c in CYCLES] == [5, 7, 3]
    held = []                                                  # (sixteenth, the cycles that begin together)
    for s in range(HALF, TOTAL):
        r = s - HALF
        heads = [c for c in CYCLES if r % (c * BEAT) == 0]
        small = tuple(c for c in CYCLES if r % c == 0)       # v3 LINE: the bass keeps the small cycles' meetings
        roots.append((ROOT[small] if len(small) >= 2 else roots[-1]) if ON['line'] else ROOT[tuple(heads)] if len(heads) >= 2 else roots[-1])
        if ON['memory'] and len(heads) >= 2:
            for c, v in zip(CYCLES, VOICES):
                if c in heads and v in MEMORY:
                    mem[v] = MEMORY[v][tuple(heads)]
        for c, v in zip(CYCLES, VOICES):
            filled = r % (c * BEAT) in fill[c]
            if ON['windup'] and s >= TOTAL - SUPER and r % (c * BEAT):       # v3: the fillings go, the small cycles come back
                going = (s - (TOTAL - SUPER)) / SUPER * 2
                both = [g for g in ((0.0 if ON['home'] else round(FLOOR * going, 1)) if filled and going < 1 else None, windup(c, s)) if g is not None]
                if both:
                    add(v, s, 1, mem[v], touch(s), **({'gain': f'{max(both)}dB'} if max(both) else {}))
            elif filled:
                add(v, s, 1, mem[v], touch(s) if r % (c * BEAT) else .95)
        if len(heads) >= 2:
            held.append((s, tuple(heads)))
        if s % BEAT == 0 and not broken(s):
            if not (ON['skip'] and r // PAGE == SKIP['page'] - pages and tuple(heads) == SKIP['meet']):   # v10 SKIP: the beat is given to the answer
                add('kick', s, 2, ground(s), .95 if s % BAR == 0 else .88)
            knock(s)
        elif s % BEAT == 0 and ON['carry']:                  # v7: the answer goes on through the break
            knock(s, CARRY_DB)
    held.append((TOTAL, tuple(CYCLES)))
    def lent(s):
        """v13: is sixteenth s a beat the drum gives to its answer on the first half's LEND page?"""
        return ON['lend'] and ON['knock'] and s % BEAT == 0 and s // PAGE == LEND['page'] and not running_down(s) and not broken(s) and tuple(c for c in CYCLES if s % c == 0) == LEND['meet']

    for (s, heads), (nxt, _) in zip(held, held[1:]):
        if len(heads) == 3:
            add('chord', s, 2, ','.join(CHORD), .85)
            continue                                           # after a chord the tone rests until the next two meet
        add('tone', s, nxt - s - 2, TONE[heads], .7)
    if ON['bars']:                                             # v18 BARS: the same tune a third size up: cycles of 3, 5 and 7 bars, their meetings held
        T['bars'] = []
        big = [(HALF + r, tuple(c for c in CYCLES if r % (c * BAR) == 0)) for r in range(BAR, HALF + 1, BAR)]
        big = [(s, h) for s, h in big if len(h) >= 2 and s >= HALF + THIRD['from'] * BAR]   # the three meet 105 bars on: at home
        for (s, h), (nxt, _) in zip(big, big[1:]):
            x = s
            while x < nxt:                                     # it lets go where the four stops for a page turn, and comes back on the turn
                if broken(x):
                    x += 1
                    continue
                y = x
                while y < nxt and not broken(y):
                    y += 1
                add('bars', x, y - x - 2, THIRD['notes'][h], THIRD['vel'])
                x = y
        marks += [("the same tune a third size up: three, five and seven BARS, which take the whole half to meet: " + (f"their last {len(big) - 1} meetings" if THIRD['from'] > 15 else "their meetings") + " held an octave under the held tones, from here to home, where the three meet: " + ' '.join(THIRD['notes'][h] for _, h in big[:-1]) + ("; it lets go for each page turn's break and comes back on the turn" if THIRD['from'] <= 15 else ''), round(T['bars'][0]['at'] * BEAT))]
    # the same tune at both sizes: from the seventh page the pings come back over the held tones, at the small
    # cycles' own places (three, five and seven sixteenths counted from the top of the half, nobody playing them)
    for s in range(RECAP['page'] * PAGE if ON['recap'] else HALF + 2 * PAGE, TOTAL):
        small = tuple(c for c in CYCLES if (s - HALF) % c == 0)
        if len(small) == 2:
            up = round(SWELL * (s - (TOTAL - SUPER)) / SUPER, 1) if ON['home'] and s >= TOTAL - SUPER else 0
            add('ping', s, 4, PING[small], .62, **({'gain': f'{up}dB'} if up else {}))
    # home: everything meets on the one, and that is the end
    add('chord', TOTAL, 8, ','.join(CHORD), .9)
    add('kick', TOTAL, 2, 'G1', .95)
    for v in VOICES:
        add(v, TOTAL, 1, MEMORY[v][ALL] if ON['memory'] and v in MEMORY else pitch[v], .95)
    marks += [('the drum answers each click that lands on it: a knock every 3, 5 and 7 beats', KNOCK_FROM)] * ON['knock']
    marks += [('second half: three, five and seven beats', HALF)] + [(f'page {p + 5} (the three meet on beat {p * PAGE // BEAT % 4 + 1})', HALF + p * PAGE) for p in range(1, pages)]
    marks += [(f"the triad turns over: {' '.join(TURNED[p % len(TURNED)][c] for c in CYCLES)}", HALF + p * PAGE) for p in range(1, pages)] * (ON['turn'] and ON['knock'])
    marks += [("the hat waits a page: this one has the pings, the counting clap and the drum on its new note, and no hat", HALF + 2 * PAGE), ("the hat comes in on the last page", HALF + 3 * PAGE)] * ON['last']
    marks += [(f"the drum goes with it: it rests on {ground(HALF + p * PAGE)}, an octave under the triad's lowest note" + (': a fifth down, onto its own note' if ground(HALF + p * PAGE) == 'G1' else ''), HALF + p * PAGE) for p in range(1, pages)] * (ON['ground'] and ON['turn'] and ON['knock'])
    marks += [("each click's echo keeps its old cycle: 3, 5 and 7 sixteenths under 3, 5 and 7 beats", HALF)] * ON['ghost'] + [(f'the clicks are struck {FORE} dB harder', HALF)] * ON['fore']
    marks += [(f"the clap counts with the three: every third beat, the beat after the knock" + (', from side to side' if ON['sway'] else ''), COUNT['page'] * PAGE)] * ON['count']
    marks += [("the tune comes back: the pings of the first half, at the small cycles' own places, over the held tones: they waited for home", RECAP['page'] * PAGE)] * ON['recap']
    marks += [("the hat counts with the five: the first hat after each of its knocks is let ring", OPEN['page'] * PAGE)] * ON['open']
    marks += [(f'the drum gives beat {s // BEAT % 4 + 1} to the answer: the three and the five sixteenths meet on it', s) for s in range(LEND['page'] * PAGE, (LEND['page'] + 1) * PAGE, BEAT)
              if ON['lend'] and ON['knock'] and not running_down(s) and not broken(s) and tuple(c for c in CYCLES if s % c == 0) == LEND['meet']]
    marks += [(f'the bass is struck {BACK} dB harder', HALF)] * ON['back']
    marks += [(f'the clock on the wall is struck {FORE} dB harder too, in its three later stops', HALF)] * (ON['struck'] and ON['fore'] and ON['wall'])
    marks += [("the drum rests where the three and the five meet: every fifteen beats, five times; the sixth is the break", HALF + (SKIP['page'] - pages) * PAGE)] * ON['skip']
    marks += [("the bass counts with the seven: the note after each of its knocks is an octave up", HALF + (LEAP['page'] - pages) * PAGE)] * ON['leap']
    marks += [('the hat after the beat the drum gave away is let ring', s + 3) for s in range(LEND['page'] * PAGE, (LEND['page'] + 1) * PAGE, BEAT) if lent(s)] * (ON['once'] and ON['ring'] and ON['open'])
    marks += [('only the drum is left of the four', HALF + last * SUPER), ('home', TOTAL)]
    if ON['break']:
        marks = sorted(marks + [('the four stops for the page turn', t - BREAK) for t in TURNS], key=lambda m: m[1])
    if ON['rest']:
        marks = sorted(marks + [('the four stops for the page turn', t - REST) for t in TURNS2], key=lambda m: m[1])
    # ---- the four's own parts: a bass that never plays with the drum, an off-beat hat, a clap on two and four.
    # Pages (from 0): the bass from page 1; the hat on pages 2, 3 and 6, 7; the clap on page 3 and pages 5, 6, 7.
    # In the last supercycle of the first half the four stops (the drum too) and comes back on the one; in the last
    # supercycle of the second half only the four is left of its parts (the drum), under the clicks, to the end.
    cell = ((2, 1.5, 'G2'), (7, 1, 'G2'), (10, 1, 'Bb2'), (14, 1.5, 'G2'))
    if ON['hold'] and ON['roots']:                            # v11 HOLD: through a break the bass holds each meeting's note to the next
        for t in [x for x in TURNS * ON['break'] + TURNS2 * ON['rest'] if x // PAGE in HOLD['pages'] + (LED if ON['led'] else ())]:
            lo = t - (BREAK if t < HALF else REST)
            meets = [s for s in range(lo, t) if len([c for c in CYCLES if (s - (HALF if t > HALF and ON['line'] else 0)) % c == 0]) >= 2]
            every = ON['walk'] and t // PAGE == WALK                      # v12 WALK: this one turn has the whole line
            meets = meets[-HOLD['last']:] if HOLD['last'] and not every else meets
            for s, nxt in zip(meets, meets[1:] + [t]):
                add('bass', s, nxt - s, roots[s], HOLD['vel'], gain=f"{HOLD['db'] + (BACK if ON['back'] and s >= HALF else 0)}dB")
            marks.append((("the bass walks to the last turn, holding each meeting's note to the next: " if every and HOLD['last'] else ("the bass comes in early: its first note is held to the turn: " if t // PAGE in LED else "the bass comes back early and holds the last meeting's note to the turn: ") if HOLD['last'] else "the bass holds each meeting's note to the next: ") + ' '.join(roots[s] for s in meets), meets[0]))
        marks.sort(key=lambda m: m[1])
    for s0 in range(0, TOTAL, BAR):
        page = s0 // PAGE
        if last * SUPER <= s0 < HALF or s0 >= HALF + last * SUPER:
            continue
        if page >= 1 and not (ON['small'] and page == pages):   # v5 SMALL: the second half's first page has no bass, as the first half's has none
            for off, ln, p in cell:
                if not broken(s0 + off) and not bare(s0 + off):
                    add('bass', s0 + off, ln, roots[s0 + off] if ON['roots'] else p, .85, **({'gain': f'{BACK}dB'} if ON['back'] and s0 + off >= HALF else {}))
        if page in TELL['hat']:
            late = 1 if ON['push'] and page % pages == pages - 1 else 0       # v4: the last page of a half, a sixteenth late
            for off in (2, 6, 10, 14):
                if page not in hat_pages() and s0 + off + late < (page + 1) * PAGE:   # v17 LAST: the page the hat waits through; in the bar that straddles the turn it plays from the turn on, as it did
                    continue
                if not broken(s0 + off + late) and not bare(s0 + off + late):
                    if ON['open'] and page == OPEN['page'] and (s0 + off - HALF) % (OPEN['cycle'] * BEAT) == 2:   # v9: the first hat after the five's knock is let ring
                        add('open', s0 + off + late, RING['len'] if ON['ring'] else 2, 'A#4', .7)
                    elif ON['once'] and ON['ring'] and ON['open'] and any(lent(x) for x in range(s0 + off + late - 3, s0 + off + late)):   # v13 ONCE: the first hat after a beat the drum gave away
                        add('open', s0 + off + late, RING['len'], 'A#4', .7)
                    else:
                        add('hat', s0 + off + late, 1, 'A#4', .7)
        if ON['count'] and page == COUNT['page']:                # v9: the clap counts with the three
            for s in range(s0, s0 + BAR):
                if s >= (COUNT['page'] + 1) * PAGE:               # the bar that straddles the next page turn: from the turn on, two and four again
                    if (s - s0) in (4, 12) and not broken(s) and not bare(s):
                        add('clap', s, 1, 'C4', .7)
                elif (s - HALF) % (COUNT['cycle'] * BEAT) == COUNT['beat'] * BEAT and not broken(s) and not bare(s):
                    add('clap-' + 'lr'[(s - HALF) // (COUNT['cycle'] * BEAT) % 2] if ON['sway'] else 'clap', s, 1, 'C4', .7)
        elif page in (3, 5, 6, 7):
            for off in (4, 12):
                if not broken(s0 + off) and not bare(s0 + off):
                    add('clap', s0 + off, 1, 'C4', .7)
    if ON['tell']:                                             # v14 TELL: the last stroke before a turn is the newcomer's
        names = {'hat': 'hat', 'clap': 'clap', 'clap-l': 'clap that counts', 'clap-r': 'clap that counts', 'open': 'hat that rings'}
        for t in TURNS * ON['break'] + TURNS2 * ON['rest']:
            for tr, x, ln in told(t):
                add(tr, x, ln, 'A#4' if tr in ('hat', 'open') else 'C4', .7, gain=f"{TELL['db']}dB")
                marks.append((f"the {names[tr]} says it is coming: the last stroke it would have played before the turn", x))
        for tr in ('hat', 'clap'):
            T[tr].sort(key=lambda n: n['at'])
        marks.sort(key=lambda m: m[1])
    if ON['leap']:                                             # v10 LEAP: the bass note after each of the seven's knocks, an octave up
        for s7 in range(HALF + (LEAP['page'] - pages) * PAGE, HALF + (LEAP['page'] - pages + 1) * PAGE, LEAP['cycle'] * BEAT):
            after = [n for n in T['bass'] if s7 < n['at'] * 4 <= s7 + LEAP['within']]
            if after:
                n = min(after, key=lambda n: n['at'])
                n['pitch'] = n['pitch'][:-1] + str(int(n['pitch'][-1]) + 1)
                if float(n.get('gain', '0dB')[:-2]) + LEAP['db']:
                    n['gain'] = f"{float(n.get('gain', '0dB')[:-2]) + LEAP['db']:g}dB"
                else:
                    n.pop('gain', None)
    if ON['leave']:                                            # v15 LEAVE: each of the three that left comes back once, where two clicks meet
        for lo, hi in ([((last - 1) * SUPER, last * SUPER)] if bare((last - 1) * SUPER) else []) + [(HALF + last * SUPER, TOTAL)]:
            for tr, x, ln in leaves(lo, hi):
                add(tr, x, ln, (roots[x] if ON['roots'] else 'G2') if tr == 'bass' else 'A#4' if tr == 'hat' else 'C4', .85 if tr == 'bass' else .7, gain=f"{LEAVE['db'] + (BACK if tr == 'bass' and ON['back'] and x >= HALF else 0)}dB")
                marks.append((f"the {tr} comes back once: the first stroke of its part that falls where two clicks meet", x))
        marks.sort(key=lambda m: m[1])
    if ON['breath'] and ON['rest']:                            # v16 BREATH: the bar before the last page, the band is left bare
        t = BREATH['page'] * PAGE
        lo, hi = t - BREATH.get('from', 2) * lcm(*BREATH['meet']), t - lcm(*BREATH['meet'])
        for tr in BREATH['who']:
            if tr in T:
                T[tr] = [{**n, 'len': round(lo / BEAT - n['at'], 4)} if n['at'] < lo / BEAT < n['at'] + n['len'] else n for n in T[tr] if not lo / BEAT <= n['at'] < hi / BEAT]
        marks = sorted(marks + [("the walk stops for breath: the low band is bare to the last meeting of the three and the five, where the bass leads the turn as it led the others", lo)], key=lambda m: m[1])
    if ON['pause'] and ON['rest']:                             # v18 PAUSE: the same, a meeting longer: the walk is one step, a rest, and the lead
        t = PAUSE['page'] * PAGE
        lo, hi = t - PAUSE['from'] * lcm(*PAUSE['meet']), t - lcm(*PAUSE['meet'])
        for tr in PAUSE['who']:
            if tr in T:
                T[tr] = [{**n, 'len': round(lo / BEAT - n['at'], 4)} if n['at'] < lo / BEAT < n['at'] + n['len'] else n for n in T[tr] if not lo / BEAT <= n['at'] < hi / BEAT]
        marks = sorted(marks + [(f"the walk stops after its first step: the low band is bare for {(hi - lo) / BEAT:g} beats, to the last meeting of the three and the five, where the bass leads the turn as it led the others", lo)], key=lambda m: m[1])
    return T, marks


def song():
    T, marks = build()
    def track(name, patch, gain, pan=0, **more):
        return {'name': name, 'patch': patch, 'gain': gain, 'pan': pan, 'notes': sorted(T[name], key=lambda n: n['at']), **more}
    echo = lambda n, mix, fb: {'type': 'delay', 'time': f'{n}/16', 'mix': mix, 'feedback': fb, 'tone': 2600}
    under = {'type': 'pump', 'on': 'kick', 'depth': '-5dB', 'release': '170ms'}
    hold = lambda db: f'clip drive=0dB ceiling={db}dB'          # a click's level is its own, not the limiter's
    doc = {
        'about': "Chirpers, album eleven, track 2: Least Common, by chirper-one. Generated by compose/chirpers11/src/chirpers11-t2.py (its docstring is the rule). Three clicks on cycles of 3, 5 and 7 sixteenths against a bass drum on every fourth; a ping where two meet, a chord where three meet, a new page where three meet on the drum, and all of it on the one once in 105 bars. The second half is the first, one size up.",
        'meta': {'artist': 'chirpers', 'album': 'Escapement', 'title': 'Least Common', 'track': 2, 'year': 2026},
        'tempo': BPM, 'seed': 1, 'event_stable': True, 'length': f'{(TOTAL + BAR) // BEAT}b', 'tail': '3s', 'ceiling': '-1dB', 'true_peak': True, 'loudness': -13,
        'patches': PATCHES,
        'buses': {'room': {'fx': ['reverb kind=room decay=0.5s mix=1 predelay=8ms', 'hp cutoff=400']},
                  'hall': {'fx': ['reverb kind=hall decay=3.2s mix=1 predelay=25ms', 'hp cutoff=350', 'lp cutoff=6000']}},
        'master': {'fx': [{'type': 'eq', 'bands': ['hp cutoff=28']}]},
        'tracks': [
            track('kick', 'lc-kick', '-6dB', fx=[{'type': 'eq', 'bands': ['peak cutoff=47 q=1.2 gain=-3dB', 'peak cutoff=130 q=0.9 gain=3dB']}]),
            track('bass', 'sub-sine', '-11dB', fx=[under]),
            track('three', 'lc-three', '-3dB', pan=-0.45, fx=[hold(-12)], sends={'room': '-14dB'}),
            track('five', 'lc-five', '0dB', pan=0.45, fx=[hold(-14)], sends={'room': '-12dB'}),
            track('seven', 'lc-seven', '-1dB', pan=0.0, fx=[hold(-14)], sends={'room': '-12dB'}),
            track('ping', 'lc-ping', '-10.5dB', pan=0.15, fx=[echo(3, 0.3, 0.45)], sends={'hall': '-10dB'}),
            track('chord', 'lc-chord', '-6dB', pan=-0.1, fx=[hold(-6), echo(3, 0.45, 0.6), under], sends={'hall': '-8dB'}),
            track('tone', 'lc-tone', '-28dB', pan=0.1, fx=[under], sends={'hall': '-6dB'}),
            track('hat', 'lc-hat', '6dB', pan=0.2, sends={'room': '-16dB'}),
            track('clap', 'lc-clap', '-6dB', pan=-0.05, sends={'room': '-10dB'}),
        ]}
    by_name = {t['name']: t for t in doc['tracks']}
    side = {'three': -1, 'five': 1, 'seven': 0}
    if ON['roots']:
        doc['patches'] = {**doc['patches'], 'lc-root': LC_ROOT}
        by_name['bass'].update(patch='lc-root', gain=f"{float(by_name['bass']['gain'][:-2]) + ROOTS_DB:g}dB")
    if ON['low']:
        by_name['bass']['gain'] = f"{float(by_name['bass']['gain'][:-2]) + LOW_DB:g}dB"
    if ON['memory']:
        doc['patches'] = {**doc['patches'], 'lc-tock': TOCK}
        by_name['five'].update(patch='lc-tock', gain=f"{float(by_name['five']['gain'][:-2]) + TOCK_DB:g}dB")
    if ON['seven']:
        by_name['seven']['gain'] = f"{float(by_name['seven']['gain'][:-2]) + SEVEN_DB:g}dB"
    if ON['through'] and ON['door']:
        for name in ('ping', 'chord', 'tone'):
            by_name[name]['sends'] = {**by_name[name]['sends'], 'far': THROUGH}
        by_name['ping']['gain'] = f"{float(by_name['ping']['gain'][:-2]) + THROUGH_DRY:g}dB"
    for v in VOICES:
        t = by_name[v]
        if ON['place'] and side[v]:
            t['pan'] = {'value': 0, 'mod': [{'src': 'auto.place', 'amount': 1}]}
            t.setdefault('auto', {})['place'] = walk(side[v] * WIDE)
        if ON['near']:
            t['gain'] = {'value': f"{float(t['gain'][:-2]) + LIFT:g}dB", 'mod': [{'src': 'auto.near', 'amount': 1}]}
            t.setdefault('auto', {})['near'] = walk(-NEAR, stand=True)
        if ON['door']:
            t['sends'] = {**t['sends'], 'gone' if ON['away'] else 'far': FAR}
        if ON['door'] and ON['away']:
            g = t['gain'] if isinstance(t['gain'], dict) else {'value': t['gain'], 'mod': []}
            t['gain'] = {'value': g['value'], 'mod': g['mod'] + [{'src': 'auto.away', 'amount': 1}]}
            t.setdefault('auto', {})['away'] = away()
    if ON['door']:
        doc['buses'] = {**doc['buses'], 'far': {'fx': ['reverb kind=hall decay=2.6s mix=1 predelay=30ms', f"hp cutoff={WIDE_HP if ON['wide'] else 500}", 'lp cutoff=8000'],
                                                'gain': {'value': f"{WIDE_DB if ON['wide'] else 0}dB", 'mod': [{'src': 'auto.door', 'amount': 1}]}, 'auto': {'door': door()}}}
        if ON['away']:                                        # the clicks' own far room: the same room, its fader making up what theirs lose
            doc['buses']['gone'] = {**doc['buses']['far'], 'auto': {'door': gone()}}
    if ON['tame']:
        by_name['ping']['fx'] = [{'type': 'eq', 'bands': [TAME]}] + by_name['ping']['fx']
    span = lambda v: {'points': [['0b', v[0]], [beats(HALF - 1), v[0]], [beats(HALF), v[1]], [beats(TOTAL - SUPER), v[1]], [beats(TOTAL), v[0]], [beats(TOTAL + BAR), v[0]]], 'curve': 0}   # a lane for the second half, going back over its last stretch
    if ON['fore']:                                            # v8: struck harder through the second half
        for v in VOICES:
            g = by_name[v]['gain'] if isinstance(by_name[v]['gain'], dict) else {'value': by_name[v]['gain'], 'mod': []}
            by_name[v]['gain'] = {'value': g['value'], 'mod': g['mod'] + [{'src': 'auto.fore', 'amount': 1}]}
            by_name[v].setdefault('auto', {})['fore'] = span((0, FORE))
    if ON['ghost']:                                           # v8: each click's echo keeps its first-half cycle
        for c, v in zip(CYCLES, VOICES):
            t = f'{c * 60000 / BPM / BEAT:.2f}ms'
            doc['buses'] = {**doc['buses'], f'ghost-{v}': {'pan': GHOST['side'][v], 'gain': {'value': '0dB', 'mod': [{'src': 'auto.ghost', 'amount': 1}]}, 'auto': {'ghost': span((-60, 0))}, 'fx': [f"hp cutoff={GHOST['hp']}"],
                                                           'returns': [{'from': v, 'gain': GHOST['feed'], 'time': t}, {'from': f'ghost-{v}', 'gain': f"{20 * log10(GHOST['back']):.2f}dB", 'time': t}]}}
    for name, side in (('clap-l', -1), ('clap-r', 1)):         # v9 SWAY: the clap again, to each side
        if T.get(name):
            doc['tracks'].append({**{x: y for x, y in by_name['clap'].items() if x != 'notes'}, 'name': name, 'gain': f"{float(by_name['clap']['gain'][:-2]) + SWAY['db']:g}dB", 'pan': side * SWAY['pan'], 'notes': sorted(T[name], key=lambda n: n['at'])})
    if T.get('open'):                                           # v9 OPEN: the hat let ring, where the shut one stands
        doc['patches'] = {**doc['patches'], 'lc-open': LC_OPEN}
        doc['tracks'].append({**{x: y for x, y in by_name['hat'].items() if x != 'notes'}, 'name': 'open', 'patch': 'lc-open', 'gain': OPEN['gain'], 'notes': sorted(T['open'], key=lambda n: n['at'])})
        if ON['ring']:                                          # v13 RING: the same hat with a decay it can be heard by
            rung = json.loads(json.dumps(LC_OPEN))
            rung['about'] = "Least Common: the hat that rings for the five (v13). lc-open's hat with a decay of 1.2 s (6 dB a sixteenth), held three sixteenths and stopped."
            rung['synth']['layers'][0]['machine']['decay'] = RING['decay']
            rung['synth']['amp']['r'] = RING['release']
            doc['patches'] = {**{k: v for k, v in doc['patches'].items() if k != 'lc-open'}, RING['patch']: rung}
            doc['tracks'][-1]['patch'] = RING['patch']
    if ON['knock']:
        doc['patches'] = {**doc['patches'], 'lc-knock': LC_KNOCK}
        doc['tracks'].append(track('knock', 'lc-knock', KNOCK_DB, fx=[hold(KNOCK_HOLD)]))
    if ON['wall']:                                              # v15 WALL: when the four stops you can hear the clock
        for nm, hz, notes in zip(('tick', 'tock'), WALL['hz'], wall()):
            if notes:
                doc['patches'] = {**doc['patches'], f'lc-clock-{nm}': {
                    'about': f"Least Common: the clock on the wall, the {nm} (v15). Give or Take's (chirper-zero's gt-clock-{nm}, v16), under this song's name: a 9 ms grain of noise through a narrow band at {hz} Hz, one pallet of an escapement. Three of them make a tick (unlock, impulse, drop).",
                    'play': {'vel_sens': 0.7}, 'synth': {'layers': ['white'], 'filters': [{'kind': 'bp', 'cutoff': hz, 'q': 5}, 'hp cutoff=1200'], 'amp': {'a': '0.1ms', 'd': '9ms', 's': 0, 'r': '5ms', 'curve': 3}}}}
                doc['tracks'].append({'name': f'clock-{nm}', 'patch': f'lc-clock-{nm}', 'gain': WALL['gain'], 'pan': WALL['pan'], 'sends': {'room': WALL['room']}, 'notes': notes})
        secs = sorted(round(n['at'] * 60 / BPM) for t in doc['tracks'] if t['name'].startswith('clock-') for n in t['notes'][2::3])
        runs = []
        for x in secs:
            if runs and x == runs[-1][-1] + 1:
                runs[-1].append(x)
            else:
                runs.append([x])
        marks = sorted(marks + [(f"the clock on the wall is heard: {len(r)} ticks, at {r[0]} to {r[-1]} s of the song", int((r[0] + WALL['phase']) * BPM * BEAT / 60)) for r in runs], key=lambda m: m[1])
    if ON['bars'] and T.get('bars'):                           # v18 BARS: the tones' patch an octave down, dry (the hall has nothing under 350 Hz), under the drum as the tones are
        doc['tracks'].append(track('bars', 'lc-tone', f"{THIRD['db']}dB", fx=[under]))
    return doc, marks


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
    for k in ON:
        ap.add_argument(f"--{'without' if ON[k] else 'with'}-{k}", action='store_true', help=f"{'leave out' if ON[k] else 'put in'} {k} (of those that are on: the last two off is v17, the last three v16, the last four v15, the last six v14, the last seven v13, the last nine v12, the last eleven v11, the last thirteen v10, the last sixteen v9, the last nineteen v8, the last twenty-one v7, the last twenty-four v6, the last twenty-five v5, the last twenty-eight v4, the last thirty-three v3, the last forty-one v2, all forty-seven v1)")
    a = ap.parse_args()
    for k in ON:
        ON[k] = not getattr(a, f'without_{k}') if ON[k] else getattr(a, f'with_{k}')
    doc, marks = song()
    if a.form:
        sec = 60 / BPM / BEAT
        for name, s in marks:
            print(f'{s:5d}  bar {s // BAR + 1:3d} beat {s % BAR / BEAT + 1:4.2f}  {int(s * sec) // 60}:{s * sec % 60:05.2f}  {name}')
        for t in doc['tracks']:
            print(f"   {t['name']:6s} {len(t['notes']):5d} notes")
    else:
        a.out.write_text(dump(doc))
