# chirpers9 (Accretion): close-out

_Collated by chirp-eco, 12 Nov 00:45 GMT, from `closeout/*.md` (chirper-zero, chirper-one, chirper-two, chirper-three, wM, chirp-video, chirp-eco). Public since 11 Nov 13:55: https://youtu.be/beZKZ14nOIs . Every figure below is the author's own; the notes have the detail._

## In one paragraph

The album is out, the songs are whole, and nobody says a main idea failed. What all seven notes say, each in its own words, is this: **almost nothing on the record was checked by an ear.** Harry heard t2's crest and its hook; the review site holds one rating, for t7. Everything else went out on measurement. The second thing they agree on: **the score stopped steering long before the end** (it sat at its ceiling; the last 20 to 80 rounds of each song moved it by hundredths), and the faults that mattered were found in the last two days by instruments that did not exist in the first week. The third: **the newest features landed on the last day** (`phrase_arc`, `diction` 2, the 60 fps picture fixes) and were set once, unheard.

## By track: what did not land, and what is most exposed

| track | owner | did not land | one more pass would be | unheard and most exposed |
|---|---|---|---|---|
| t1 Nucleation v93 | chirper-zero | the organ's rotary, the hands interlocking, getting off the section cap; five seed instruments never tuned as a family | the lean (top 4.9 dB right at 1:12-2:16), then the sitar and the pad | the cello's phrasing (v93), the crest's master glue and clip (v91) |
| t2 The Long Way In v111 | chirper-one | the head (0:00-0:32) never had a round; the join from t1 (t2 is 9-21 dB brighter at 8-16 kHz) | the crest: now the narrowest place in the song, limiter over 2 dB | "each" on the hook is not heard as a word; distance buses and the widened top (v103-v106) |
| t3 Phase Margin v106 | chirper-two | the join into t4 (promised, not closed); top leans 3.7 dB left at 0:40-1:28; first storm 13.9 dB of low end over its tunes | a line for the first storm, the lean, the join | v105 (storms' low end, the sweep at 3:17), landed after the candidate |
| t4 The Warm Third v102 | chirper-three | hats, glockenspiel, shaker, bowl and piano still masked; a +8 dB master shelf over dull sources; the duet does not lift with her | the climax heard first (her E5 at 3:31 swings 50 cents either way) | the last seven rounds: width, tape, the drive on her voice, the lift |
| t5 Periapsis v99 | chirper-zero | heat as timbre; a real change of band between A's three choruses (bars 27-46) | A's steadiness, then the head | diction 2 on "closer and closer" and the farewell, where she is alone |
| t6 Spring Tide v116 | chirper-one | the floor never moves; 600-1400 Hz crowded and hidden by master cuts; flattest track on the map (31%) | the head and the torn section (3:37-4:06) | glue and clipper on the crest (v109); the five fast statements read slightly worse at diction 2 |
| t7 Marginally Bound v105 | chirper-two | E1 at three speeds is written and not heard (koto in a hundredth of its frames); low end 9.9 dB over the tunes; the verse singer has almost nothing above 2.8 kHz | the low end, as done on t3 | the groove change of v104, the first to sound since v76 |
| t8 All of It Falls v104 | chirper-three | the early stretto is narrow above 2 kHz; the horizon as loud as the jet for 35 s; one of her six questions opens its mouth in time | the level step in from t7 (3.6-4.0 dB) | the frozen halo, the pump, "all of it" in the choir (Whisper heard it at no level) |

## Engine and library: open at the close

- **Built and tested during the album, landed after it** (12 Nov 04:40, by wM at Harry's word, on tools main: 52a91bfd `effort_tilt`, fc5b0ca9 `play.phrase_gap`, 45a33b89 `diction` 3; opt-in, gated identical over the 109 released songs; not on this record). wM's ablation on the last day: the shipped voice patches cost words (`even: 1` the most), and `diction` 3 removes that cost.
- **Silent failures.** A song-level `feel.nudge` is ignored without a message: t7's groove, written at v76, first sounded at v104. The plan warning was promised and not built (bd-d0e254). `tools/look.py --song` cannot read our song files. `features.md` says t6 uses a Duffing layer; it does not.
- **Master chain.** Master effects run before the loudness stage, and the master `volume` sits after them, so thresholds are set against raw levels up to 20 dB apart and a chain tuned on a raw render is 3 dB off (three composers; bd-43e0bd).
- **Racks that will bite the next song.** `rack:drum-bus-punch` and `rack:parallel-ny` on a parallel send add each stick a second time (t3's snare reached +13 dBFS before the master). The songs clip their own buses; the racks are unchanged (bd-e0185e; the metal kit uses them).
- **Voice.** `diction` is per track, and two composers wanted it per line. Little above 1.4-2.8 kHz on open vowels (t4, t7). "each", "half", "far side" and "near side" are not heard as words at any level.
- **Smaller.** An `lr4` width stage shifts phase at width 1; `terrain` has a DC mean; `extends` replaces a patch's pitch mods; `drive` with `mix` under 1 combs; removing a track's early notes re-rolls the rest of its randomness; `orbit` is binaural only; NES noise voices are one source.
- **Picture** (chirp-video): light is display-encoded, one sample a pixel; one process uses about five CPUs; the flash guard counts by frame.
- **Nothing was promoted to the library.** Named as worth it: `a1-dust`, t5's two-noise corona, t6's hand cymbals, t2's wave-terrain keys, the two distance buses as a rack, `a3-flock`, `a7-plume`, `a3-grit` with `a3-deep`, the nudged kit forks, the singer's microphone, the wide hats, the frozen-word bus, the master's tape-shelf-glue.

## The scorer and the measuring

- The join term reads 3 s either side of an overlap and nothing inside it. The bass hand-overs were first measured on 10 Nov; t2 to t3, t6 to t7 and t7 to t8 were re-set that day.
- The section cap is duration / 15 s; t1 sat on it by form, and it decided several rounds. The spectrum term reads the opposite of `bandprof.py` on t3 and t7.
- What found real faults: the arrangement map, take-it-out, flatness, the limiter table, lean, joins as heard, Whisper per written word. All arrived in the last two days. `lean` and the per-word measure are still outside `tools/`.
- Density: t3 and t7 ended at 107 and 128 tracks with 30 to 47 sounding at once; t1 and t5 carry 101 and 111 switches in their generators. The map showed parts described for days that nobody could hear.

## Next record: what they would do differently (their words, grouped)

1. **Put an ear in the loop.** A clip of every exposed change in front of Harry the day it lands (all four composers and wM); name each kept round's ten most exposed seconds.
2. **Measure what is heard from round 10, not round 100.** Have the map, share, lean, limiter, joins-as-heard and the master bench in the first week. Stop climbing the score at its ceiling.
3. **Freeze the engine a day before the cut,** and rehearse the whole delivery once on one minute of film: draw under load, join, finish, upload unlisted, look.
4. **Voice first.** Per-word scoring and a level check before a composer adopts a voice change; test the singer and her words before writing lines to notes; each sung line on its own track.
5. **Co-build the film** from the first day, with a small whole-film draft every few days.
6. **Housekeeping.** Commit the round, then investigate; fold kept switches into the generator every twenty rounds; keep what must last outside `/tmp`.

## What we have

- **Six albums public on YouTube; none on Spotify.** All six store kits are complete in `~/Music/Chirpers/<album>/master/`. The film's master and everything a re-render needs are kept (`RERENDER.md` beside it); the drawn parts are deleted.
- **Engine:** main's chirp is the release pin 97a13ae6; about 40 opt-in features landed for this album. All six release engines have checked copies outside `/tmp` (`tools/pinstore.py`).
- **Fleet:** all six agents closed out on 12 Nov 00:10-00:15; no loops, nothing running, nothing uncommitted. Each kept its working files under `~/.local/state/<name>/`.
- **The groove** plays Accretion on a 90 s buffer.
