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

Add a row when you need something the engine lacks: say exactly what and why, and tell chirp-eco, who takes it to Harry
(wM works when Harry gives him a turn).
