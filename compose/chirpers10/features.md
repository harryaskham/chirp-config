# Common Time (chirpers10): the engine board

What the engine has that Accretion's pin did not, and what this record asks of it. The full list of what chirp can do,
feature by feature with its pin, is Accretion's board (`compose/chirpers9/features.md`); `python3 tools/chirpers.py palette
chirpers10-t1` shows what the song uses beside what it has not tried. Every row is opt-in: its default is exact, and each
pin is gated identical over the 109 released songs and this one before the groove adopts it.

The groove's pin is in `tools/groove-pin`; render with that binary (`$(cat tools/groove-pin)`), never the Nix chirp.

## Landed since Accretion's pin (97a13ae6)

| feature | what it does | on main | groove pin | used by |
|---|---|---|---|---|
| voice layer `effort_tilt: 0..1` (wM, bd-7d9b6e) | a louder voice is brighter: a shelf on the voiced source centred on 1.7 kHz, 24 dB per unit of `effort` around 0.5 at 1; default 0, exact | 52a91bfd | 45a33b89 (12 Nov 06:09) | |
| `play.phrase_gap` (wM, bd-c26c45) | the longest rest inside one `phrase_arc` phrase (a time, 0..5 s; unset = 0.3 s as before): shorter gives each short phrase its own arc, longer runs one arc across a line's breaths | fc5b0ca9 | 45a33b89 | |
| voice layer `diction: 3` (wM, bd-db3c56) | `even` holds the vowels level and leaves the consonants; on Accretion's 29 sung lines the word error rate went 0.425 (level 2) to 0.356; levels 0-2 unchanged | 45a33b89 | 45a33b89 | |

## Asked for, not built

| ask | by | state |
|---|---|---|
| `chirp plan` reports an ignored song-level `feel` key (a `feel.nudge` there is silent) | Accretion's close-out | bd-d0e254, wM's for his next turn |
| send-safe drum racks (`rack:drum-bus-punch` and `rack:parallel-ny` add the dry twice on a parallel send) | Accretion's close-out | bd-e0185e, library; new names only |
| master effects that see the normalised level (opt-in) | Accretion's close-out | bd-43e0bd |
| live playback at the file's level: the groove ignores `loudness` and plays the raw mix (v1 sat 19 dB under its file) | found 12 Nov | no bead yet: the song carries its own level for now |
| the physical palm mute (pluck `mute`) keeps a muted low string's low mids: it takes about 13 dB too much out at 400 Hz-1 kHz after the amp (riffpunch on Bleed 34 against the older muting's 67) | chirper-zero, v12 | bd-bc17f7; the song uses the older muting (decay, brightness and a filter riding `expr.pm`) |
| the diphthong AW ends apart from OW: a sung "now" is heard as "no" (AW ends 420/900, OW 380/800) | chirper-zero, v17-v18 | bd-3b52e9; respell N AA1 UH0, or choose another word |
| high-gain rigs whose rests are silent: the library's rigs with `sympathetic` ahead of a saturated amp hold full level through a rest (28 patches, 81 songs) | chirper-zero, v19-v20 | bd-42e146, library; in a song: `PATCH fx.0.mix=0` on the track. No engine change needed: a smaller ring is no fix, and the riffs do not miss it. Library names since v22: `ct-chug-stop-l/r`, `ct-bite-stop-l/r`, `ct-wall-stop-l/r` (17-19 dB down a sixteenth after a stab at 120 BPM; the wall 15). The older `m8-*` rigs are as they were |

Add a row when you need something the engine lacks: say exactly what and why, and tell chirp-eco, who takes it to Harry
(wM works when Harry gives him a turn).

## Learned in use (how the engine behaves; none of these is a fault)

Each cost a round to find. They go into the engine's README with the next landing; until then they are here.

| what | the rule | found |
|---|---|---|
| live playback ignores a song's `loudness` | set the level in the song (a master `gain`, or `autolevel`); a file render's level says nothing about the groove's | v1-v3 |
| the plan drops values equal to the engine's default | `chirp plan` and `tools/showcase.py` show a reverb with no `kind` (it is a hall) and an amp with no `model` (it is `modern`) | 12 Nov |
| an amp is saturated from `gain` 0.3 up (soft and hard strokes 5.8 dB apart at 0.05, 0.5 dB at 0.3, 0 at 0.5) | a different string, pick or pickup is only a different guitar near `gain` 0.13; above it they move the spectrum about 2 dB at most | v14 |
| a compressed bass (or a clipped drums bus) ignores velocity and track gain | ride it AFTER the compressor: an `auto` lane on the bus gain | v8, v21 |
| a reverb inside a bus chain at a high `mix` turns the dry down with it (it cross-fades) | put the room on a send beside the bus, not in its chain | v10 |
| the `rotary` costs 2.7 dB of level at `mix` 1 | make it up on the fader | v15 |
| a track's name seeds its `humanize` | a null test across two track names is invalid; keep the name and change the patch | v15 |
| `stutter` reads `chance` at the start of each 256-frame block (about 5 ms) and decides a slot at its first frame; a lane moves in a straight line between its points | raise the lane half a beat before the slot and bring it down half a beat before the next: one raised 5 ms early missed its slot and caught the next. `tapestop`'s `stop` is a threshold (0.5) and is not touchy | v21 |
| `sympathetic` rings on after the playing stops (its `decay`), and ANY ring ahead of a saturated amp holds the amp at full level | no `sympathetic` on a high-gain rig that must stop (bd-42e146) | v19-v20 |
| a speech recogniser reads none of a harsh voice in a full mix, ours or a record's; `base.en` is no judge of a scream | judge words on the voice alone with `small.en` (`tools/wordread.py`), tone and level with `tools/voxref.py` | v17-v18 |
| the `chaos` layer (Roessler, x axis) has periodic windows the schema does not mention (held Ab4, share of the tone off the whole multiples): `amount` 0-0.3 clean; 0.34-0.58 period two (4-6%); 0.66-0.75 chaotic; 0.8-0.85 period THREE (17-18%); 0.9-0.95 chaotic; 1.0 period FIVE (19%) | the windows at 0.8-0.85 and 1.0 are the musical ones (a fifth below; a just minor third above and a major third below); a lane on `amount` walks between them | v22 |
| a pure tone has all its energy in one band | `tools/presence.py` can call it buried (-12 dB under the mix) while `tools/stembal.py` shows its band 4 dB over the records: run both on a sine-like part | v22 |
