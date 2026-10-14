# chirp tools (user)

Keep a live `groove` session evolving as real songs.

- `evolve.py` — every loop pass the groove plays a generated song (`songs/form-1|2.yaml`) with a
  form that suits its style (rock / edm / classical / breakdown): intro, verses, pre, choruses,
  breakdown, solo, a lifted final section, outro; transitions (risers, impacts, reverse cymbals).
  Drums come from the `beat-*` parts; melodic material is freshly composed per song by
  `compose.py` (a key, mode and four-chord progression; an idiomatic main riff; a hook motif that
  is stated, sequenced and resolved; chords, arpeggio, held layer → `songs/gen-form-*`).
  A song lasts 2–3 passes, mutating one element per pass.
  Styles: 26 heavy (`compose.HEAVY_STYLES`) and 43 chill (`compose.CHILL_STYLES`) — see below.
- `compose.py STYLE` — compose a test set (`songs/gen-test-*`).
- `restart-groove.sh [SONG] [ARRANGEMENT]` — restart `groove` on a pinned copy of chirp and resume the evolver.

## Steering (applies to the playing song at the next bar, and to the queued one)

    echo "COMMAND" >> ~/.config/chirp/tools/steer.txt

| Command | Effect |
| --- | --- |
| `compose` / `melody` / `rekey` | new key + melody / new motifs, same key / new key, mode and progression |
| `key +2`, `tempo -4` | transpose / tempo |
| `swap ROLE [PART]` | re-pick a role (`mid high low half brk riff hook pad soft arp hold`) |
| `xf ROLE ^rev^rot=0.25^thin=0.2^aug=2^inv` | lasting motif transform on a role |
| `style NAME` | switch style now (same key) |
| `next NAME` | replace only the queued song with a fresh one in NAME |
| `journey on\|off`, `journey h=0.5 rate=0.05` | gradual heaviness climb (lofi … djent) |
| `mutate` | one random change |

`state.json` shows what is playing and queued; `journey.json` the heaviness climb (full djent mode:
mostly djent, sometimes breakdown, clean or another genre). Watch with `chirp watch`.

## Rigs (reusable sound choices)

`compose.py` keeps every instrument choice in `RIGS` (with fallbacks for builds that lack a patch)
and builds guitars through `rhythm_tracks(score)`, so other composition scripts get the same sound:

```python
import os, sys; sys.path.insert(0, os.path.expanduser("~/.config/chirp/tools")); import compose
tracks = compose.rhythm_tracks("expr.pm=1 F1/16@110 F1@98 …") + [compose.track("bass", compose.rig("bass"), "F1/16@110 …")]
```

| Role | Patches (first available) |
| --- | --- |
| rhythm | `m8-rhythm-l` + `m8-rhythm-r` — a real double: two rigs (5150 / Gojira voicings, different IRs, pick, pickup, stiffness), two players (seeds 7 / 13, looser right hand) |
| bass | `bass-fat` (heavy string DI + strong sub, light amp blend) → `bass-di` → `m8-bass` |
| sub / twang / lead / drums | `sub-sine` → `sub` · `m8-twang` · `lead-monster` · `prog-kit` |

In hand-written YAML, double a rhythm part the same way:

```yaml
- {name: gtr-l, patch: m8-rhythm-l, pan: L90, seed: 7, score: "…"}
- {name: gtr-r, patch: m8-rhythm-r, pan: R90, seed: 13, score: "…"}
```

Riff building blocks in `compose.py`: `gen_meshuggah` (odd cycles over a 4/4 pulse with locked
drums; power chords, clusters, choked stops, muted scratches; `mode` riff / toms / shuffle / break),
`gen_space` (ringing twangs with gaps), `gen_djent`, `gen_hook` (motif → sequence → cadence),
`gen_clusters`, `gen_hold`, `soften` (velocity-scaled variant). Modes include the evil ones
(double-harmonic, hungarian, neapolitan, phrygian-dominant, locrian, diminished).

## Staying current

`tools/sync.sh` (run it regularly, e.g. every few minutes): pulls `chirp-config`, restarts the
evolver if `evolve.py`/`compose.py` changed upstream, and when `tools` origin/main has new chirp
commits rebuilds in a detached worktree and restarts the groove on the new build (resuming the
queued song). `favorites.json` lists saved parts (`songs/fav-*`) that forms recall — breakdowns
re-use a favourite ~⅓ of the time, transposed into the song's key.

## Favourites

`tools/fav.py 23:40 [ROLE]` (or `fav.py now`) saves what was playing at that time — evolve.py archives
every chapter to `~/.cache/chirp/played` — as `songs/fav-ROLE-KEY-HHMM.yaml` parts plus the song identity
in `favorites.json`. Forms recall saved parts for the matching role ~⅓ of the time (transposed into the
song's key; kits don't transpose) and saved songs return now and then with a new tempo and key.

## Kit and guitar detail

`metal-kit` (default kit): punchy triggered-style kick, rimshot-thick snare, compressed/saturated bus.
Generated parts add ghosts and flams; guitars get pinch squeals, tremolo-picked stabs, machine-gun
double chugs, whammy dives and natural harmonics on twangs, and per-section inserts (phaser/chorus in
space sections, a 1/16 stutter gate in some breakdowns).

## Time-varying effects

Every generated part goes through `compose.enhance(role, tracks, beats)`:
sidechain (`duck` by the part's kick: sub −8 dB, reese −6, bass −3), builds (`riffSoft`/`riffUp`: an
`auto` envelope opens a low-pass across the part and swells the level), dub delay throws at the end of
breakdowns/space sections (an `auto` spike on a feedback delay's mix) and an LFO auto-pan on twangs.
The engine also offers `track.NAME.vel/key` follow sources, song `vars` (lfo/auto/steps), `cc.N`, and
modulatable amp gain, drive, delay/reverb/chorus/phaser mix, glue mix, OTT depth, tape drive, width, gain,
pan and sends — all usable from these helpers.

## Racks and grooves

- `racks/NAME.yaml` — named, composable effect chains (see `racks/README.md`); `compose.rack(name)` /
  `compose.expand(fx)` resolve `"rack:NAME"` (nested) until the engine supports racks natively.
- `songs/groove-*.yaml` — the groove library (drum-only, tempo-inheriting parts), rebuilt by
  `tools/grooves.py`: djent cells and breakdowns, Meshuggah cycles / tom grooves / shuffle, Garstka
  breakdowns, blasts (trad/hammer/bomb/d-beat), thrash (gallop/chromatic/skank/half), Tool-style
  5–31/8 grooves by grouping (heavy/tribal/clean). Drop in with `@groove-mesh-11-8`.

## Keeping it running

`tools/watchdog.sh` (run in the background): every 15 s, if the `groove` session is gone and the
Pulse server answers (e.g. after an sgu24 Pulse restart), it restarts the groove on the latest build,
resuming the queued song. Log: /tmp/chirp-watchdog.log.

## Song-level variety (per song / per chapter)

- **Form variants** (`fv`): base, extended, short, breakheavy, shuffle.
- **Guest sections**: two sections from other styles' generators composed in the song's key
  (`riffGuest1/2`: jazz, breakcore, blast, tribal, whammy, taiko, kotekan, tabla, space, beatdown,
  D&B, brostep, gallop, chaos); ~60% of songs slot one or two into the form.
- **Modulation**: half of chapters shift key (±1, 2, ±3, 5, ±6 semitones) at a section; chapter
  boundaries may shift key or change scale (same motifs, new mode).
- **Metric modulation**: ~a third of chapters change tempo 3:2 / 2:3 / 4:3 / 3:4 at a section
  (half return later) via the form's tempo map.
- Rig sets, compression styles and flavours vary per song; the energy and filter lanes and the
  vocoder choir (agent TTS re-sung in the song's key) follow each chapter.

## Journeys (`tools/journey.json`)

- `mode`: `metalambient` (heavy ↔ ambient interludes), `chill` (the night set) or anything else (the
  heaviness-driven heavy rotation; `h` climbs by `rate` per pass). `until` (epoch) + `then` schedule a
  switch: e.g. chill until 10:50, then `metal` — the handover warms up from h 0.4 back to 1.0 (~7 passes).
- **Night arc** (`night_arc`, chill mode): 05:00–07:30 favours sparse, drumless `DEEP_NIGHT` styles
  (×2.5, busy styles ×0.4); 07:30–11:00 favours brighter `MORNING` grooves (×2.2). Choices use
  normalised `random.choices` over `CHILL_MIX`.
- Favourites only return within the journey's world (chill favourites in chill mode, heavy otherwise).

## The chill set (43 styles)

Jazz & soul: ukjazz gogo ballad doomjazz souljazz ethiojazz neosoul manouche bossa citypop.
Electronic: lofihop downtempo house-melodic triphop dub vaporwave chillwave cyberscape berlin hauntology
beattape lofihouse amapiano liquid fusion. Classical & ambient: chamber neoclassical satie tiersen
minimal lid ambient kankyo backrooms dawnchorus handpan. World: mali guofeng celtic dawnraga balearic.
Band: smile slowcore. Steady styles (`STEADY`) hold key, tempo and mode for the whole song.

Per song / chapter, all deterministic from the song's seed:
- **Textures** (`texture`/`generic_texture`): 2–3 modulators per chapter — breathing filter, wow swell,
  wearing grit, reverb tide, delay swell, phaser, tremolo, tape-skip creep, section high-pass sweep,
  pitch drift for warped styles.
- **Scapes**: wind, shortwave, rain, waterphone layered under ~40% of riff parts (`SCAPE_STYLES`).
- **Feel** (`feel_track`): tight / laid / drunk — 16th-grid kit tracks re-timed with 1/128 sub-step
  offsets (`drunk()`): kick on the grid, backbeats late, hats drifting. Neo-soul is always drunk.
- **Transitions** (`write_form`): in-key wind-chime cascades, swells, soft downlifters, and one-beat
  drum fills on each style's own kit (`STYLE_KIT`, `SOFT_FILLS`).
- **Instrument swaps** (`FAMILIES`): each family (keys, mallets, winds, reeds/brass, pads, pianos,
  guitars, basses) swaps to a sibling with p=0.35 per song.
- **Melodic development**: the hook gains an octave double in chapter 2 (mallet above) and later
  (cellos/horn below or flute above). `gen_hook` writes classic, call-and-response or sparse forms
  with breathing rests and phrase-arc dynamics.
- **Guests / fusion**: same-key sections from other chill styles (`CHILL_GUESTS`); `fusion` splices one
  style's harmony over another's rhythm section (`RHYTHM_SRC`).
- **Resampling**: `beattape` and `lofihouse` chop library parts (`chop-*` patches: `type: sample`,
  `song: lib-X`, `slices: 16`) and re-sequence them MPC-style (`chop_phrase`).
- **Stock layers**: the engine's `@vox-chops` / `@orch-hit` in B sections of some styles, transposed
  to the song's (relative) minor.

## Loudness

- `qa.py STYLE…` renders a chapter through the master and reports rms, peak, limited samples, xRT,
  dynamics and band levels (QA rms is per-channel; LUFS reads ~3 dB higher).
- Static trims: `STYLE_TRIM`, `COMP_TRIM`, per-style air shelf.
- **Adaptive** (`loud_sample`): each pass's short-term LUFS (`live status` → `lufs_s`) nudges a learned
  per-style trim (step 0.5) and a slow shared `_chill` / `_heavy` trim (0.1) — `tools/loudness.json`.
  Targets: −18 LUFS chill (night), −11.5 heavy (the level the metal always played at).
- **Autolevel** on the master (`autolevel`, 0.5 dB/s, ±6 dB) rides within passes, after the trims.

## Voice (agent TTS → `voxchoir`)

17 chains — choir (vocoder), shimmer, harmony, radio, robot, demon, glitch, dub, ghost, phaser80,
talkbox, formant wah, chop, octaves, megaphone, underwater, whisper — chosen per chapter from chill /
heavy pools with style affinities (`VOX_STYLE`), parameters re-rolled per chapter and varied mid-pass,
timings tempo-synced, level-matched (`VOX_GAIN`). The pass log shows `vox=NAME`.

## Between songs

- **Tape stops**: the master carries `tapestop stop=var.stop`; ~30% of song changes in tape-friendly
  styles (`TAPESTOP`) wind down over the last beat and snap back on the downbeat (`tape stop` in the log).

## Library

- `libparts.py [STYLE…|heavy]` — export `songs/lib-STYLE.yaml` (section), `-hook` (melody), `-brk`
  (heavy breakdowns): composed in C, tempo-inheriting, `tr=` transposable; index `songs/LIB.md`.
- `grooves.py` — rebuild the drum-only `groove-*` library (metal and chill grooves).

## Operations

- `restart-groove.sh` takes `chirp-restart-v2.lock` (spawned processes don't inherit it); the watchdog
  skips while it is held. `sync.sh` rebuilds origin/main when the engine changed and restarts the
  groove at a pass boundary (≤ 2.5 s left).
- Runtime state (ignored): `state.json`, `steer.txt`, `journey.json`, `loudness.json`, `form-*`, `gen-*`.
