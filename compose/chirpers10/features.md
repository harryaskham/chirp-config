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
| a late window that renders fast with a `rotary` on a bus: any rotary makes its bus and every track routed to it render from the top for a `--from POS --preroll` window (16 s of the full mix at 12:44: 108-129 s; 13 s with the rotary off the guitars' bus) | chirp-eco, 13 Nov | bd-e11da9: the rotors' angle follows from `speed` alone, so the engine could advance it without the audio. Until then: the rotary on a bus of its own fed only by the tracks that play through it, or render once and cut windows from the file |

Add a row when you need something the engine lacks: say exactly what and why, and tell chirp-eco.

## Who builds them (Harry, 13 Nov 09:27)

Asked "who should build the engine features the song has shown are missing?" (chirp-eco, wM, chirper-zero, or not
now), Harry chose: **"chirper-zero builds them"**. His words of 12 Nov still frame it: "add new ones if we need better
amp sim or DI features. All chirp-native of course."

How a feature gets from the composer to the groove (chirp-eco gates, lands and adopts; the composer never pushes to
tools main and never moves `tools/groove-pin`):

1. **A worktree of your own at tools main**, outside `/tmp` (it is aged at ten days):
   `git -C ~/tools fetch -q origin && git -C ~/tools worktree add -b chirp-zero-engine ~/.local/state/chirper-zero/engine origin/main`.
   Main's engine is the groove's pin, so you start from what is playing. Read the source there, never in an old checkout.
2. **One bead a feature, one feature a landing, small.** Opt-in, and its default exact: with the option unset every
   existing song renders bit for bit as before. Released albums are frozen; the gate checks all 109 of their songs.
3. **Build in a guarded unit** so the groove's guard can freeze it, with a target directory of your own:
   `systemd-run --user --collect --unit=guarded-zero-build-$(date +%H%M) -p CPUSchedulingPolicy=batch -p Nice=12 --setenv=PATH="$PATH" --setenv=HOME="$HOME" --working-directory=$HOME/.local/state/chirper-zero/engine/cli/chirp -- bash -c 'nix develop -c bash -c "CARGO_BUILD_JOBS=4 CARGO_TARGET_DIR=/tmp/lt/target-zero cargo build --release -p chirp-cli" > /tmp/lt/zero-build.log 2>&1; echo EXIT $? >> /tmp/lt/zero-build.log'`.
   The binary is `/tmp/lt/target-zero/release/chirp`; bench with it by path. CPU only.
4. **Before handing over**, in the same shell: `cargo test --workspace && cargo clippy --workspace --all-targets -- -D warnings`
   (the README's own line), a test for the feature beside the code, and a line for it in `cli/chirp/README.md`.
5. **Hand over by message to chirp-eco**: the commit hashes on your branch, the bead, what you measured, and a PROBE: a
   small song or patch string that uses the feature, which your build plans and the groove's pin refuses.
6. **chirp-eco then** builds it afresh, runs the probe both ways, runs the gate (109 released songs identical, and this
   record's song identical), lands it on tools main, puts the groove on the new pin at the song's wrap, and adds the row
   above. About an hour and a half from hand-over when nothing differs.
7. **The song may not use a new feature until chirp-eco says the groove is on the new pin**: the groove renders with
   `tools/groove-pin`, and a song the pin cannot plan stops the record playing. Bench it in a copy until then.

Candidates, in no order (which, whether and when are the composer's call; the song comes first): the physical palm mute's
low mids (bd-bc17f7), the AW diphthong (bd-3b52e9), a rotary that does not force a from-the-top render (bd-e11da9), and
whatever the amp or the DI next turns out to lack. Three README notes wait for the first landing: the `stutter` `chance`
rule, the `chaos` `amount` map and the curve of an `auto` lane's falls, all in the table below.

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
| `stutter` reads `chance` at the start of each 256-frame block (about 5 ms) and decides a slot at its first frame; a lane rises in a straight line between its points and falls on a curve (the row below) | raise the lane half a beat before the slot and bring it down half a beat before the next: one raised 5 ms early missed its slot and caught the next. `tapestop`'s `stop` is a threshold (0.5) and is not touchy | v21 |
| an `auto` lane is an envelope: between two points a RISE is a straight line, a FALL takes the envelope's `curve` (default 3, exponential; `plan.rs` `points_at`). A gain lane from 0 to -20 dB over eight beats reads -3.0 -8.8 -12.6 -15.3 -17.1 -18.3 -19.2 -19.8 at the beats' middles; with `"curve": 0` in the lane's dict, -1.2 -3.7 -6.2 ... -18.7, the line | every fade-out, duck-by-lane or sweep down drawn as two points is a quick drop and a plateau (half the fall in the first 21% of the time) unless the lane says `"curve": 0`; fade-ins are lines either way. `tools/lanes.py ID` lists every lane, what it drives and each fall that is not a line | v24 |
| `sympathetic` rings on after the playing stops (its `decay`), and ANY ring ahead of a saturated amp holds the amp at full level | no `sympathetic` on a high-gain rig that must stop (bd-42e146) | v19-v20 |
| a held note through a saturated amp has no decay: the string dies, the amp's output does not until the string is 30-40 dB down. An 8 s chord falls 1-2 dB through `ct-chug`, `ct-wall` or `m8`, 37 dB through the low-gain `ct-crunch`, 48 through `ct-clean` | a chord written to ring out sits flat and then cuts. A ring-out is a fader move after the amp (an `auto` lane on the bus), not a property of the note. `tools/holds.py ID` lists every long note that sits flat with a rest after it | v9, v23 |
| a `rotary` remembers its start (so do `radio`, `vinyl`, `cloud`, `crush`, `ring`, `vocoder`, `autolevel`, a `tape` with a deck, `lpc`, `waveset`, `pvoc`): a windowed render (`--from POS --preroll N`) renders that effect's bus and every track routed to it from the top, so the take is the same | one such effect on a big bus makes every late window cost most of a full render: a solo guitar track at 12:44 took 38 s with the rotary on the guitars' bus, 2-6 s without. Keep such an effect on a bus of its own | v15, found 13 Nov |
| a noise-burst pick (`soft` 0, the default) spreads a low string's attack over one period (23 ms on a low F); `soft` 1 is the triangle of a released string | on MUTED notes bind `soft` to `expr.pm`: riffpunch on Bleed 0-30 s goes 67.0 to 86.6 with nothing else changed (rise 19.5 to 16.2 ms, the record 14.2; tight 3.2 to 0.9, the record 1.2). On every note it is worse on open notes (The Faultless 69.1 to 43.5). A muted note's DI is then fundamental-heavy: the amp's `tight` 80 to 220 brings the spectrum back | 13 Nov (bench; in the song from v25) |
| a speech recogniser reads none of a harsh voice in a full mix, ours or a record's; `base.en` is no judge of a scream | judge words on the voice alone with `small.en` (`tools/wordread.py`), tone and level with `tools/voxref.py` | v17-v18 |
| the `chaos` layer (Roessler, x axis) has periodic windows the schema does not mention (held Ab4, share of the tone off the whole multiples): `amount` 0-0.3 clean; 0.34-0.58 period two (4-6%); 0.66-0.75 chaotic; 0.8-0.85 period THREE (17-18%); 0.9-0.95 chaotic; 1.0 period FIVE (19%) | the windows at 0.8-0.85 and 1.0 are the musical ones (a fifth below; a just minor third above and a major third below); a lane on `amount` walks between them | v22 |
| a pure tone has all its energy in one band | `tools/presence.py` can call it buried (-12 dB under the mix) while `tools/stembal.py` shows its band 4 dB over the records: run both on a sine-like part | v22 |
