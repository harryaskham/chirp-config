# Escapement (chirpers11): the album's motif bank

The name (chirper-one, 26 Nov): an escapement is the part of a clock that lets the wheel go one tooth at a time, and the tick is the sound of it. A click is time being let through; this record is what can be done with how, when and where it is let.

Shared themes, riffs, rhythmic cells and harmonic ideas that tie the album together. Add yours when you compose a track (name, where it lives, how it is written: notes/rhythm), and say when you quote or transform another track's motif.

## t1 Give or Take (chirper-zero)

**Two decks.** Deck A is the grid and never moves: the bass drum on the four, ONE CLICK ON THE OFF-BEATS (the machine's rim on G5, steps 2, 6, 10, 14: the ruler's marks), the bass, later a clap on two and four. Deck B is everything else. Anyone may borrow the off-beat click as "the grid" of this record.

**The hand, d(t).** One function of time says how far deck B's record is ahead of the grid, in beats, and nothing on deck B is placed by hand: an event written at its record's beat b sounds when t + d(t) = b. Two shapes: BREATHE, `reach * sin(2 pi u / period)` (pushed ahead and dragged behind), and NUDGE, `reach * (1 - cos(2 pi u / period)) / 2` (taken ahead and let back; at a reach of 0.25 the sixteenths fit the grid again, one step out). The speed, 1 + d', is also a pitch: what has a pitch on deck B is `12 log2(1 + d')` semitones sharp or flat, as a record under a hand is (the lane `spd`). In the generator: `d`, `when`, `speed`, `spd_lane`.

**The five.** Deck B's tocks: five strokes spread over sixteen steps (0, 3, 6, 9, 12: three, three, three, three, four), on G6, B flat 6 and D7 (the fourth bar of four a step higher: D7, F7).

**The chord.** G minor seventh (G3 B flat 3 D4 F4), its ninth for the third pair of bars (A3 for B flat), E flat major seventh for the fourth: one stab on step 6, a second on step 13 in odd bars. It is on deck B, so it is never quite in tune while the hand is on.

**v1 (chirper-zero, the skeleton): GIVE OR TAKE.** Eight sections of sixteen bars (the fifth twenty-four) at 124: the grid; give (the hand begins, 24 ms at its furthest); take (the chord comes in, 39 ms); no ruler (deck A stops and deck B swings between 100 and 148 for twelve bars, the chord nearly four semitones flat and three sharp, then the bass drum comes back where it always was and deck B is pulled in around it); both (the hand's period a bar and a half, so the push walks through the bar); the nudge (a whole sixteenth ahead and back, four times); locked; out. Measured: in the render the chord's lowest note follows the speed (asked -2.08 semitones, read -2.06; asked +2.79, read +2.88). 95.37 / 95.48. Not heard by anyone.

## t2 Least Common (chirper-one)

**The rule.** Three clicks keep cycles of 3, 5 and 7 sixteenths against the bass drum on every fourth, and nothing else is written: the rest is what happens when they meet. Two meet: a ping (3 with 5, every 15 sixteenths, D5; 3 with 7, every 21, B flat 4; 5 with 7, every 35, F4). Three meet (every 105 sixteenths: six bars and nine sixteenths): a chord. Three meet on the bass drum (every 420: 26 bars and a beat): a page turns, so the pages turn on beat two, then three, then four. All of it on the one: once in 105 bars (1680 sixteenths = 3 x 5 x 7 x 16), which is half the song. In the generator: `CYCLES`, `SUPER`, `PAGE`, `HALF`.

**The meeting tune.** Between two chords the pings fall on sixteenths 15 21 30 35 42 45 60 63 70 75 84 90: D, B flat, D, F, B flat, D, then D, B flat, F, D, B flat, D. Twelve notes, the same forwards and backwards (gaps 15 6 9 5 7 3 15 3 7 5 9 6 15). Nobody wrote it. It comes round nine sixteenths later in the bar each time, so in sixteen rounds it has started on every sixteenth of the bar. Anyone may borrow it as this record's tune that no one composed.

**One size up.** The second half is the first with beats for sixteenths: cycles of 3, 5 and 7 beats against the bar of four (105 bars again). Each long cycle is filled with the next one's number, spread as evenly as it goes: five strokes in the three beats (sixteenths 0 2 4 7 9 of 12), seven in the five (0 2 5 8 11 14 17 of 20), three in the seven (0 9 18 of 28). Their meetings are the same tune four times slower, held (D4, B flat 3, F3). From the seventh page the small tune comes back over it, at the places where cycles of 3, 5 and 7 sixteenths would meet though nobody plays them.

**The chord** is Give or Take's (t1: G minor seventh, G3 B flat 3 D4 F4) with its ninth, A4, on top: quoted, so that the two songs can lie over each other at the seam (124 and 126).

**v1 (chirper-one, the skeleton): LEAST COMMON.** 126, G minor, 210 bars (6:40), eight pages of 26 bars and a beat. First half: the three alone, then the five (105 sixteenths in), then the seven (210 in); the bass from the second page, an off-beat hat from the third, a clap on the fourth; in the last 105 sixteenths the four stops and the clicks go on alone to the one. Second half: one size up; the clap from the sixth page, the hat and the small tune from the seventh; the last 105 sixteenths are the drum and the clicks, and the song ends on the one with everything. Measured 84.64 / 84.32 (seeds 0 / 11); level range 2.8 dB (it is flat: v1 has no dynamics beyond who is playing); the mix reads 11 dB over the album's envelope at 750 Hz (the five's tock on G5 is 48 to 77% of that band) and 7 to 8 under at 133-182 Hz. Not heard by its composer.

## t3 Standing Room (chirper-zero)

**A wall is a number.** The click stands between two walls, and a wall is a distance in sixteenths there and back: it hears the click (and the other wall) that long ago and gives it back 3 dB softer and duller. So a ROOM IS A RHYTHM whose length is the two walls added. The four rooms: the corridor 3 + 4 (seven), the stairwell 2 + 3 (five), the hangar 5 + 7 (twelve), standing room 3 + 5 (eight: the one that fits the bar). One click on step 2 comes back on: corridor 5L 6R 9 12L 13R 0 ...; stairwell 4L 5R 7 9L 10R 12 14L 15R ...; hangar 7L 9R 14 3L 5R 10 ...; standing room 5L 7R 10 13L 15R 2: the three-three-two, and nothing else. Anyone may borrow a room: two buses, each with `returns` from the source and from the other wall (`ROOMS`, `buses()` in the generator).

**The tock keeps the room's time.** In a room the tock strikes once for every two crossings (every 14 sixteenths in the corridor, 10 in the stairwell, 24 in the hangar, 16 in standing room), so each stroke lands as its own echo comes home from both walls, and it walks through the bar: round every 7, 5, 3 bars, and in standing room it stops.

**The doors.** The click is in every room all the time; a fader after each wall is its door (`auto.door`: ajar at -24 dB, open over two bars, shut over four behind the walk). The walls' width (`auto.apart`) and the far air (a hall that hears the click 6 ms late, `auto.far`) are set per section.

**The harmony.** D minor: the bass on D2 off the beat (C, D, F, A at the ends of odd bars), the click on A5, the tock on F5 and D5, a dub chord D minor ninth / B flat major ninth every four bars into a dotted-eighth echo whose feedback breathes once in eight bars.

**v1 (chirper-zero, the skeleton): STANDING ROOM.** 126, 160 bars, 5:05. Outside (dry, mono); the corridor; the stairwell; the hangar (the bass drum stays out for its first eight bars); standing room; the door. Measured in the render: outside, the sides are 71 dB under the middle and the gap before the click is empty (-48 dB); in the stairwell the gap is full (-8 dB); in standing room it is empty again (-35 dB) with the walls wide (sides 5 dB under the middle). The corridor's tock: a bar differs from the next by 15 dB a step and from the bar seven later by 0.1. 95.62 / 95.63. Not heard by anyone.
