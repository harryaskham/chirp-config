# chirpers11: the instruments banked in the library

Written by `tools/patchbank.py promote chirpers11 --md`; do not edit by hand. Each name is a file in `patches/`,
resolved and self-contained: `patch: NAME` on a track gives the instrument as the song plays it.

| name | from | what |
|---|---|---|
| `gt-clap` | Give or Take v1 (track clap) | Give or Take's clap (chirper-zero, 26 Nov): the machine's clap, three bursts, short; deck A. |
| `gt-hat` | Give or Take v1 (track hat) | Give or Take's sixteenth click (chirper-zero, 26 Nov): a 14 ms burst of white noise between 6 and 12.5 kHz; deck B. |
| `gt-kick` | Give or Take v1 (track kick) | Give or Take's bass drum (chirper-zero, 26 Nov): the engine's machine kick, short and dry, resting on the song's G; deck A. |
| `gt-knock` | Give or Take v2 (track knock) | Give or Take's second bass drum (chirper-zero, 26 Nov, v2): deck B's own, a little shorter and clickier than deck A's, through a high-pass on the lane `low` (32 Hz to 315 Hz: the low EQ of the incoming record, killed unt… |
| `gt-meet` | Give or Take v4 (track meet) | Give or Take's ping (chirper-zero, 26 Nov, v4): Least Common's `lc-ping` (chirper-one) rebuilt here under this song's name: a vibraphone bar with no motor, half a second long. It plays t2's meeting tune once the two deck… |
| `gt-roll` | Give or Take v5 (track roll) | Give or Take's loop (chirper-zero, 26 Nov, v5): deck B's bass drum as it is in "the nudge" (its bass out: a high-pass at 315 Hz), let go the instant its note ends, so that a note as long as the loop is the loop: the firs… |
| `gt-stab` | Give or Take v1 (track stab) | Give or Take's dub chord (chirper-zero, 26 Nov): three saws and a square through a short filter envelope, dry (the echo is a bus); its pitch follows deck B's speed (auto.spd, semitones), as a chord on a nudged record doe… |
| `gt-tick` | Give or Take v1 (track tick) | Give or Take's grid click (chirper-zero, 26 Nov): the machine's rim, one voice, high and dry; deck A's ruler marks. |
| `gt-tock` | Give or Take v1 (track tock) | Give or Take's tock (chirper-zero, 26 Nov): a wooden bar on the modal layer (after Common Measure's clave), whose pitch follows deck B's speed (auto.spd, semitones). |
| `ht-bass` | Hearing Things v1 (track bass) | Hearing Things' bass (chirper-zero, 26 Nov): the second to sixth harmonics of the note and nothing at the note itself (after the library's phantom-bass): the ear supplies the pitch. |
| `ht-chop` | Hearing Things v4 (track chop) | Hearing Things' chord (chirper-zero, 26 Nov, v4): a plain sine a note, switched on in a millisecond and off in three, so that a sixteenth of it is a sixteenth and its holes are holes. |
| `ht-clap` | Hearing Things v1 (track clap) | Hearing Things' clap (chirper-zero, 26 Nov): the machine's clap, three bursts, short, dry. |
| `ht-fence` | Hearing Things v4 (track fence) | Hearing Things' fence (chirper-zero, 26 Nov, v4): white noise between 170 and 560 Hz, switched as the chord is: it fills the chord's holes exactly, in the chord's band, louder than the chord. |
| `ht-hat` | Hearing Things v1 (track ris) | Hearing Things' hat (chirper-zero, 26 Nov): the machine's hat, 28 ms, above 5 kHz, whose loudness is all velocity: the Risset rhythm's layers are told apart by nothing else. |
| `ht-kick` | Hearing Things v1 (track kick) | Hearing Things' bass drum (chirper-zero, 26 Nov): the engine's machine kick, short and dry, on A1: the only thing on the record under 100 Hz but for eight bars. |
| `ht-pip` | Hearing Things v5 (track line) | Hearing Things' pip (chirper-zero, 26 Nov, v5): a plain tone with a little of its octave, 90 ms: plain enough that two of them are told apart by pitch and by nothing else. |
| `ht-shep` | Hearing Things v2 (tracks shep0, shep1, shep2, shep3) | Hearing Things' rising voice (chirper-zero, 26 Nov, v2): a small struck tone (a sine with two bar-like partials, 70 ms), whose loudness is all velocity and whose pitch rides the lane `rise` (semitones): one layer of the … |
| `ht-tick` | Hearing Things v1 (track tick) | Hearing Things' click (chirper-zero, 26 Nov): the machine's rim, 35 ms, on E5; on the off-beats from the first bar to the last. |
| `lc-chord` | Least Common v1 (track chord) | Least Common: what three clicks make when they meet. A short filtered chord for a delay to carry. |
| `lc-clap` | Least Common v1 (track clap) | Least Common: two and four. The drum machine's clap, short. |
| `lc-hat` | Least Common v1 (track hat) | Least Common: the off beat. The drum machine's hat, closed. |
| `lc-kick` | Least Common v1 (track kick) | Least Common: the four. The drum machine's bass drum resting on G, short enough to leave the sixteenth before the next beat empty. |
| `lc-ping` | Least Common v1 (track ping) | Least Common: what two clicks make when they meet. A vibraphone bar with no motor, half a second long. |
| `lc-root` | Least Common v2 (track bass) | Least Common: the bass once the meetings write its line (v2). A sine and its octave, so that a line on 73 to 117 Hz is also heard on 147 to 233. |
| `lc-seven` | Least Common v1 (track seven) | Least Common: the click that counts seven. The drum machine's rim, tuned to G: two short pings and a click, a knock. |
| `lc-three` | Least Common v1 (track three) | Least Common: the click that counts three. Ten milliseconds of noise above 5 kHz: a tick with no note. |
| `lc-tock` | Least Common v2 (track five) | Least Common: the click that counts five, once it has a tune (v2). The same wooden bar damped twice as fast, so that a note it keeps for twenty strokes is a colour and not a drone. |
| `lc-tone` | Least Common v1 (track tone) | Least Common: the meetings one size up. A plain held tone, a sine and a little of its octave, that takes a beat to arrive. |
| `os-bass` | Out of Step v1 (track bass) | Out of Step's bass (chirper-zero, 26 Nov): three pairs of sines, at G2 and its second and third harmonics, each pair 2.1 Hz apart (one cycle a beat at 126; ratio 1.021429 for G2 ONLY: another note needs its own ratio). T… |
| `os-bass-b` | Out of Step v5 (track bassb) | Out of Step's second bass (chirper-zero, 26 Nov, v5): the same three pairs of sines built on B flat 2 (116.5409 Hz), each pair 2.1 Hz apart (ratio 1.018019 for B flat 2 only), so it pumps on the beat as the G does. It so… |
| `os-clap` | Out of Step v1 (track clap) | Out of Step's clap (chirper-zero, 26 Nov): the machine's clap, three bursts, short, dry. |
| `os-click` | Out of Step v1 (tracks a, b) | Out of Step's click (chirper-zero, 26 Nov): five cycles of a saw on G3 dying in 22 ms, lifted 9 dB round 9 kHz, started at the same point of its wave every time, through a low-pass that both clicks share (it opens with t… |
| `os-comp` | Out of Step v2 (track c) | Out of Step's third click (chirper-zero, 26 Nov, v2): the complement's. Two cycles of a saw on G5 dying in 12 ms, above 3 kHz, lifted 8 dB round 10 kHz: small and bright, so that it is heard as the holes being filled and… |
| `os-hat` | Out of Step v1 (track hat) | Out of Step's hat (chirper-zero, 26 Nov): the machine's hat, 45 ms, on the off-beats once the two clicks are home. |
| `os-kick` | Out of Step v1 (track kick) | Out of Step's bass drum (chirper-zero, 26 Nov): the engine's machine kick, short and dry, on G1. |
| `os-tune` | Out of Step v3 (track tune) | Out of Step's pip (chirper-zero, 26 Nov, v3): a small glass tone (a sine with its twelfth, 140 ms), which plays only the sixteenths on which the two clicks strike together, a note for each stroke of the pattern. |
| `rt-air` | Ring True v1 (track air) | Ring True: the air. Three milliseconds of noise into a resonator tuned to the note (a band-pass); how long it sings comes from the stroke (expr.ring, on its q). |
| `rt-drum` | Ring True v3 (track weight) | Ring True: the weight whose thud gives way to its note (v3). rt-boom's two layers, a felt thud and a kettledrum head on the same note; the stroke's ring (expr.ring, seconds) sets the head's ring time and also takes the t… |
| `rt-metal` | Ring True v1 (track metal) | Ring True: the metal. A steel bar (1 : 2.76 : 5.40 : 8.93); its ring time from the stroke (expr.ring, seconds over 0.012). |
| `rt-plate` | Ring True v2 (tracks plate, plate-room) | Ring True: the plate, the thing that rings false. A small thin plate (dense inharmonic modes) struck near its edge; its ring time from the stroke (expr.ring, seconds over 0.010). Stopped, a bright tick; let go, a wash an… |
| `rt-skin` | Ring True v1 (track skin) | Ring True: the skin. A kettledrum head (the air in the kettle pulls its modes to 1 : 1.5 : 2 : 2.5, so it sings its note); its ring time from the stroke (expr.ring, seconds over 0.03). |
| `rt-string` | Ring True v1 (track string) | Ring True: the string. A plucked string whose ring time comes from the stroke (expr.ring, seconds over 0.03): a palm on it, lifted. |
| `rt-wood` | Ring True v1 (track wood) | Ring True: the wood. A small bar (1 : 4 : 10) struck near its middle; its ring time from the stroke (expr.ring, seconds over 0.015). |
| `sc-hat` | Small Change v2 (track hat) | Small Change: the hat that plays what can be paid. The machine's hat, 30 ms, above 6 kHz. |
| `sc-kick` | Small Change v1 (track kick) | Small Change: the drum. The machine's bass drum on G, short. |
| `sc-seed` | Small Change v1 (tracks seed-a, seed-b, seed-c) | Small Change: the seed. One vibraphone bar with no motor, short, with two milliseconds of noise on its front (a click that the coins carry too): the only struck note in the song. |
| `sr-chord` | Standing Room v1 (track chord) | Standing Room's dub chord (chirper-zero, 26 Nov): three saws and a square through a short filter envelope, dry; its space is the bus `dub`, a dotted-eighth echo whose feedback breathes. |
| `sr-clap` | Standing Room v1 (track clap) | Standing Room's clap (chirper-zero, 26 Nov): the machine's clap, three bursts, short, dry. |
| `sr-click` | Standing Room v5 (track click) | Standing Room's click (chirper-zero, 26 Nov): the machine's rim with a breath of white noise, 40 ms, above 500 Hz and lifted 6 dB round 11 kHz: bright enough that a wall can take its top away. |
| `sr-kick` | Standing Room v1 (track kick) | Standing Room's bass drum (chirper-zero, 26 Nov): the engine's machine kick, short and dry, on A1. It is not in any room. |
| `sr-tock` | Standing Room v1 (track tock) | Standing Room's tock (chirper-zero, 26 Nov): a wooden bar on the modal layer (after Common Measure's clave), an octave or so under the click. |
| `wd-chord` | Wind Down v1 (track chord) | Wind Down: what three cycles make when they meet: a short filtered chord. |
| `wd-comp` | Wind Down v2 (track comp) | Wind Down: the complement's click (after Out of Step v2): two cycles of a saw on G5 dying in 12 ms, above 3 kHz, lifted round 10 kHz. |
| `wd-ghost` | Wind Down v1 (track ghost) | Wind Down: a bass with no fundamental (after Hearing Things): harmonics two to six of the note and nothing at the note. |
| `wd-hat` | Wind Down v2 (track hat) | Wind Down: the hat (after Hearing Things): the machine's hat, 28 ms, above 5 kHz, whose loudness is all velocity. |
| `wd-held` | Wind Down v3 (track held) | Wind Down: the meetings' last chord, held (v3): wd-chord's two saws under a low-pass at 900 Hz that does not open, half a second coming and three seconds going. |
| `wd-kick` | Wind Down v1 (track kick) | Wind Down: the drum. The machine's bass drum on G, short. |
| `wd-ping` | Wind Down v1 (track ping) | Wind Down: what two cycles make when they meet (after Least Common): a vibraphone bar with no motor. |
| `wd-saw` | Wind Down v1 (track saw) | Wind Down: a click that is five cycles of a saw (after Out of Step): on G3 that is 51 ms. |
| `wd-seed` | Wind Down v1 (track seed) | Wind Down: the seed (after Small Change): a short vibraphone bar with 2 ms of noise on its front. |
| `wd-sink` | Wind Down v3 (track tick) | Wind Down: the click whose note can sink (v3): wd-wood with the whole voice's pitch on the stroke (expr.sink, semitones). |
| `wd-under` | Wind Down v3 (track under) | Wind Down: the fundamental the ghost bass never had (v3): a sine at the note. |
| `wd-wood` | Wind Down v1 (tracks tick, cell) | Wind Down: Ring True's wooden bar (1 : 4 : 10), its ring time given by each stroke (expr.ring, seconds over 0.015), with the stick's click on its front (2 ms of noise). It is the click and the cell. |
