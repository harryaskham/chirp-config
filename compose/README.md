# Songwriting climbs: Chirpers albums

**We are writing albums together, in real time** (Harry, 29 Oct). The chirpers write, rewrite and arrange original
songs round by round. Harry listens on the groove as they change, rates and leaves notes (the player's `:rate`/`:note`,
or tools/rate.py), and the chirpers answer his notes and each other's ideas. They trade motifs and sounds between
tracks. Every round is a songwriting iteration: a richer, better song than the round before, never a metric tweak.
compscore is a guardrail; the songs and Harry's ears are the point.


Harry, 28 Oct: alongside reproducing records, chirp climbs ORIGINAL music. An album by **Chirpers** starts as empty
tracks. Climbers claim them like any climb, compose each song from scratch with the library's patches, fx and mix
tools, then keep climbing it. There is no record to match, so the score is `tools/compscore.py` (intrinsic measures
plus Harry's ratings), and Harry's ear decides.

## The pieces

| what | where |
|---|---|
| album spec: genre, brief, palette, track slots (role, length, brief), weights | `compose/ALBUM/album.json` |
| the album's motif bank: shared riffs, cells, harmonies, who uses them | `compose/ALBUM/motifs.md` |
| the album's sound bank: rigs and kits invented for it, who made and borrowed them | `compose/ALBUM/sounds.md` |
| ratings and notes (Harry's, and agents' peer ratings) | `compose/ALBUM/ratings.jsonl` (via `tools/rate.py`) |
| agents' own measures (plugins) | `compose/measures/NAME.py` |
| saved per-song features for album terms; the genre envelope | `ref/compose/ALBUM/` (local) |
| track climbs | `climbs.json`: `ALBUM-tN`, `mode: compose`, `songs/ALBUM-tN.yaml` |

## Workflow

1. `climb.py next` (or `--take ALBUM-tN`) draws an empty track like any requested climb. Its brief shows the slot,
   the album brief, the neighbouring tracks and the latest ratings.
2. **Name the album** if nobody has: `tools/chirpers.py name ALBUM "Name"` (once, first agent wins), then
   `tools/chirpers.py art ALBUM` (cover via the `tti` CLI, pixelated for the player).
3. **Compose** `songs/ALBUM-tN.yaml` from scratch: tempo, form, motifs, parts, arrangement, mix and master (with a
   top-level `ceiling`). Title it: `tools/chirpers.py title ALBUM-tN "Title"`. Add its motifs to `motifs.md`.
4. **Render, listen, score**: `python3 tools/compscore.py ALBUM-tN OUT.wav --text [--song CANDIDATE.yaml]` shows the
   terms and where it is weak (pass `--song` when the render came from a candidate file: its `tempo` sets the rhythm grid).
5. **Record**: `climb.py done ALBUM-tN --version v1 --score S --note … --next … --with songs/ALBUM-tN.yaml
   compose/ALBUM/motifs.md`, then `compscore.py ALBUM-tN KEPT.wav --save`, which saves the kept render's features
   for the album terms. The song joins the playlist.
6. **Keep climbing, richly** (Harry, 29 Oct): every round makes a RICH, audible improvement. Every pass can change
   anything: a new or rewritten section, deeper motif development, a new sound or instrument, a solo or counter-line,
   reharmonisation, rhythm and meter, arrangement, builds, the mix, the transitions; several at once is fine. Never
   record a no-change round. A/B on paired seeds (`compscore` on seeds 0/11). compscore is a guardrail, not a gate:
   near its ceiling, keep what sounds better on judgment (`climb.py done … --keep`) unless it clearly breaks
   something. A SECTION-COUNT FLIP IS NOT A REGRESSION (ruled 10 Nov, Accretion's final push): when a change's only
   cost is one section more or fewer at one novelty cut on one seed (`tools/bounds.py` shows the peak and its margin;
   the curve is normalised over the whole song, so a level change anywhere can tip a weak peak), and every other term
   is level or better on the seeds you scored, keep it on judgment and put the seed table and the peak in the note.
   Do not spend rounds steering a peak across a cut. A trial you refuse by ear: `climb.py done … --refused` (logged, never the best however it scored). A
   higher score recorded without the song in `--with` stops and asks which you meant (chirper-three's t4 v60, 8 Nov).
   So does the mirror: a score that does NOT beat the best with the changed song in `--with` and no `--keep` (at a
   score's ceiling every round ties: Common Time v7, 12 Nov). The song file is always the registry's best.

`tools/chirpers.py status ALBUM` shows the album; `chirpers.py refresh ALBUM` re-renders every composed song and
re-saves features (run it after several songs change).

### Round types (Harry, 2 Nov)

An album can set `params.rounds` in its `album.json`, e.g. `{"whole": 0.4, "section": 0.4, "palette": 0.2}`. Then
`climb.py next` draws each round's TYPE, from those weights, per song and round number (reproducible), and the brief
says which. `next --type T` overrides the draw when you have a reason; `climb.py type ID` prints one song's type, for
owners who rotate their own songs. Name the type in your round note. Without
`params.rounds`, every round is a whole-song round as before.

- **whole**: the usual round, the bold change that moves the whole song most.
- **section**: one ~30 s window, worked closely in its context. The aim is the small changes a whole-song pass misses,
  the ones that make a song feel handcrafted and unique: make that window stand out, or blend, and keep the variety
  moving. `chirpers.py sections ALBUM-tN --wav BEST.wav` maps the song in windows of whole 4-bar phrases, about 30 s,
  on its own tempo map. For each window it shows level, brightness, density, internal motion, the change from the
  window before, and the earlier window it is most like. Its likeness hears the notes as well as the sound: a
  semitone sequence with register, twice a beat, so a melody moved, reordered or leapt an octave counts. The **groove** column hears feel: where in the beat the attacks fall (a 24-bin onset-phase histogram on the tempo map), so straight 8ths turning into a triplet shuffle reads ~0.15 where a steady groove reads under ~0.06; at 0.08 or more the window is marked (new groove) and is never called little new (chirper-three, t4 v36, 3 Nov). It flags near-repeats, static windows, little-new windows
  and level jumps, then names the windows to focus on next: flagged, least recently focused first. It also prints the
  `chirp render --from/--to` commands for each window, alone and in context. After the change,
  `sections … --wav NEW.wav --against OLD.wav` shows per-window deltas: the residual (the energy of new - old,
  about -60 dB untouched, -20 clearly changed), the note-sequence change and the feature deltas, so you can confirm
  the change stayed in its window and see how it moved against its neighbours. The full-length score must not regress beyond noise, or keep it
  on judgment. Record the round with `sections … --mark N --note '…' --as NAME`, which writes the song's ledger
  `compose/ALBUM/sections/ALBUM-tN.jsonl` and commits it, so focus rotates through the song. The flags are a
  flashlight, not a quota: a static window can be the point.
  Keep a section round local (chirper-one, t7 v16): a track's per-note randomness (humanize velocity, timing,
  gate) is one stream drawn note by note, so notes added to an EXISTING track shift every later note's draws and
  the change leaks into later windows (-6 to -9 dB residual there). Put the window's new material on its own new
  track, listed last (tracks seed by name, so other tracks are untouched). When a generator skips parts in some
  bars, write them as usual and filter the events out afterwards, so its own random sequence does not shift.
  `--against` shows any leak. Since engine f5283535 (2 Nov, wM, bd-89f091) a song can say `event_stable: true` at
  its top level instead: every note's humanize and DSP draws then come from its track, beat and pitch, so an edit to
  one window leaves the rest as it was, on any track. Switching it on re-rolls the humanized notes once, so do it in a
  round that changes the music anyway, and measure after it.
- **palette**: `chirpers.py palette ALBUM-tN` lists the song's instruments (track, patch, what it is made of), the
  album's staples (library patches three or more songs share), the library patches no song on the album uses, the
  song's own patches (library candidates), and the engine features the album has not used. Change one or two
  instruments: swap a staple for something no other track has, design a new patch, or add the part the song lacks.
  Measure on full-length renders.

## The score (`tools/compscore.py`)

The total is a weighted mean of the terms that apply; weights are in `album.json` (`weights`).

| term | weight | what it rewards |
|---|---|---|
| human | .30 | Harry's latest rating x10 (an older version's counts half) |
| peer | .05 | other agents' ratings (never the composer's own) |
| structure | .12 | a section count suited to the length, unequal section lengths |
| variety | .12 | contrast across sections: loudness range, timbre spread, density change |
| recurrence | .10 | motifs that return, in a middle band (none = no development; all = one idea looped) |
| rhythm | .08 | onset periodicities off the eighth-note grid of the song's declared `tempo` (polymeter cells, displacement) at a sane density: the cell has to drive accents/kick to show |
| spectrum | .07 | no departure beyond 6 dB from the genre's spectrum envelope: a broken-mix check, never a target (clean tracks are meant to differ) |
| master | .06 | level, peak and crest in the album's ranges |
| length | .04 | within the slot's length |
| cohesion | .03 | timbre close enough to the rest of the album |
| distinct | .02 | not a near-copy of another track |
| flow | .03 | level/spectrum continuity at the joins with the neighbouring tracks (the songs bleed); not scored for an album whose album.json says `"bleed": false` |

**Reading spectrum's detail** (3 Nov): `worst_band_hz` / `worst_band_db` say where and which way, + = louder than the envelope. The worst band can be a DEFICIT: a new mid layer makes loudness normalisation pull the whole mix down and leave the bass short. Before trimming a new layer that cost spectrum, check whether the worst band sits below it (chirper-three, t4 v32: +3.5 dB of bass took spectrum 89.2 -> 91.3 with the stabs kept). A level-change residual of about -30 dB in every other window of `sectionmap --against` is the normaliser trimming the master (~0.3 dB), not a musical change. For the whole picture from one render, `compscore.py ID WAV --bands` lists every band: signed dB vs the envelope, dB beyond tolerance, and the spectrum/total points fixing that band alone would give. A run of neighbouring short bands wants a peaking EQ on the track that owns them, not broadband gain (chirper-three, t4 v33: +2 dB of bass moved 133 Hz by 0.3 dB; a 133 Hz peak, q 0.9, +5 dB fixed it). Fix a deficit only as far as the band needs: on t12 v35 a sub at +5 dB gave the same spectrum as +3 dB but cost 'distinct' (84-93), since a heavier low end everywhere makes the sections share more (chirper-three). --bands so far: t3 97.60 -> 98.07, t4 97.15 -> 97.78, t6 +0.6, t9 +0.85, t12 97.71 -> 98.66.

Calibration (28 Oct): real records score 68-88 on these terms (before length), a looped bar 33. **Above ~95 every
intrinsic term passes**: from there compscore cannot tell you what to improve. Climb by musical judgment (what would
make this track more itself, more surprising, better at its job on the album), by peers' notes and Harry's ratings,
and by the album as a whole (the joins, the motif bank, the empty slots). Seed-to-seed spread is ~0.5-1 point; treat
smaller gains as noise. The measures are
guidance, not taste. **Variety over convergence**: never trade a song's identity for a few points; a change that
makes the songs sound alike is a loss, whatever compscore says. **Praise is local** (Harry, 3 Nov: "i need to be able to say 'i like this bit' without the whole album turning into that! keep things varied. not all singing. but not NO singing either! nuance is key"): a moment Harry likes is good in its song, not a template. Within an hour of his t10 note, 8 of 12 songs had taken up the new FOF layer and at least 4 had the same four-voice choir; that is the failure mode. Ask what this song wants; if another song already has the move, find this song's own version or another idea. Invent better measures: drop a file in
`compose/measures/` with `measure(ctx) -> (score or None, detail)` and propose a weight in `album.json`.

**The metric is yours (Harry, 30 Oct: "climbers choose their own metrics, whatever makes the best song").** From
Chirpers IV on, the composers choose an album's weights and measures. Set `weights` in `compose/ALBUM/album.json`
(a plugin such as `polymeter` counts only once it has a weight there) and add measures in `compose/measures/`. Agree
on caco before changing a weight, so every track on the album is scored by the same rules. After any change, rebaseline
the album (`tools/chirpers.py rebaseline ALBUM --apply`) so bests compare like for like.

## The groove and the queue

The groove plays the album's playlist. Each entry re-reads its song file when its turn comes, so **Harry hears your
latest version automatically: never `chirp live queue` a round just to publish it.** Queue only a deliberate
before/after pair for a big change, and at most one pair of yours at a time. It plays ahead of the album, so a
queue that grows faster than it plays (29 Oct: 10 versions, about 45 minutes) starves the album. Better: render
short excerpts as mp3 and `audio_share` them, so Harry can play them whenever he likes.

## Illusions that have to work on Harry's speakers

Lessons from The Endless Stair (31 Oct), from Harry's ears and the chirpers' measurements. **Harry listens on both headphones and speakers** (his answer, 1 Nov), so every track has to work both ways:
- **The same signal in both ears means ONE source.** Precedence/Haas, Huggins pitch, binaural beats on noise and other phase tricks need identical signals in the two ears: one track routed to two buses (with the delay, filter or pan on a bus). Two tracks playing the same score with a noise or randomised patch produce two *different* noises, and the illusion silently disappears (chirper-zero, t17). Keep such pairs dry: a shared reverb leaks each side into the far ear and blurs the separation.
- **Dichotic tricks vanish on speakers.** Octave, scale and Huggins illusions, and anything that needs one ear each, should come with a version that also works in mono.
- **The presence meter (`chirpers.py illusion`) is a flashlight, not a target.** Holes or parts added only to raise its percentage read as glitches ("something out of track", Harry on t10). Close gaps with things that are musical and unmistakable: a riser or barber pole into the moment, the illusion's own figure brought forward, or teach the ear the obvious version before the subtle one.

## Mixtapes (a DJ-mixed album)

An album with `compose/ALBUM/mixplan.md` plays as a DJ mix. The seam table (`| seam | ... | overlap (bars) | ... |`, one
`| tN -> tM |` row per seam) drives three things:
- **The groove**: when the next playlist entry is the album neighbour (tN, then tN+1), it starts on the outgoing
  track's bar line OVERLAP bars before that track's musical end, beat-aligned, crossfaded linearly; there is no
  tempo sync. Gaps in the album, and the loop back to the opener, play back to back.
- **`chirpers.py seams ALBUM`**: an audit of every seam: how far the two tracks' beats drift apart across the overlap
  (a tempo ramp inside the last OVERLAP bars flams the kicks; hold the seam tempo flat there), plus dead air after a
  track's last bar line (end `length` on the last bar and set a short `tail`). Run it after any tempo or length change.
- **`chirpers.py seam ALBUM N`**: one seam (tN -> tN+1) as the live mix plays it: both songs rendered, the overlap laid
  on the outgoing bar line, sub (< 120 Hz) and full-band level per bar for the linear crossfade and the mixer swap,
  and mp3s with 8 bars either side in /tmp/chirp-seams (to listen to, or `audio_share`). About a minute.
- **`tools/modlint.py [ID|FILE ...]`** (default: the focus album): frequency mod amounts are in OCTAVES (`cutoff=800+lfo.a*2` sweeps two octaves); an amount written in Hz (-2600) shuts or opens the filter the moment the source moves (t8's horizon light was buried at -42.6 dB that way). Flags any beyond the engine's whole 14.9-octave range. Seconds per song.
- **`tools/libguard.py [PATH ...] [--me NAME]`** (10 Nov): the library (`patches/ racks/ styles/ irs/`) is LIVE for every album, so editing a patch other songs use changes them at once. It plans every registered song against the committed library and against the library with your change, and names each song whose canonical plan differs. `climb.py commit` and `done --with` run it for library files: REFUSED when a song outside the album in progress would change (a released album must keep rendering as released), HELD until `--library-ok` when another composer's song would (tell them first). A file under a NEW name is free; so is a change kept in your song (`extends: NAME` plus overrides, which `tools/extendslint.py` checks for dropped mod routes). About a minute.
- **The picture reads your song** (10 Nov): each track's programme (`vis/ID.yaml`) is built on its bars, track names and lanes. `climb.py commit` and `done --with` check it against the version you commit and print a NOTE (never blocking) when that version gives it a warning the committed one did not: keep the name, or tell chirp-video. `tools/visdrift.py` shows where every programme stands against its song.
- **`tools/presence.py ID [--from POS --to POS] [-j 3]`** (any song): how audible EVERY track is inside its own mix. Renders the mix and each top-level track solo over the window (unmastered, K-weighted like LUFS), and lists each track's level against the mix while it sounds, how often it is within 10 dB of it, and how much of the window it plays; BURIED flags parts more than 25 dB under (inaudible: raise, cut or let them go). A 32-bar window of a 21-track song takes about a minute.
- **`chirpers.py illusion ALBUM N TRACK[,TRACK...]`** (any album): how present a track's illusion parts are in its
  mix: soloed against the full render (both unnormalised), their level against the mix, the share of the track
  where they sit within 10 LU of it, the longest stretch without, and a 30 s timeline. About 30 s.
- **`chirpers.py release ALBUM --mix [--swap [BAR]]`**: the continuous mixtape file, with a tracklist and CUE.
  `--swap` adds a DJ bass swap at 120 Hz in every overlap: the highs crossfade, and the lows stay the outgoing track's
  until the midpoint (or BAR bars in), then hand over within a beat. An optional `swap` column in the seam table
  (a bar, `mid` or `no`) sets it per seam. The groove gets the same swap once the engine has it.

## Ratings and notes

Harry: `tools/rate.py ID 7.5 --note "the bridge drags"`, or `tools/rate.py now 8` for whatever the groove plays, or
`tools/rate.py note ID "text"`. Agents can rate other agents' songs (`--who` defaults to your climb name in an agent
session); those feed `peer`. `climb.py next` shows a song's latest ratings and notes, so read them first.

## Working on each other's songs

Each track has an owner once composed. To improve someone else's song, or to align a motif or style across tracks,
build the change as a candidate (`tools/rngsafe.py`, `tools/scoreedit.py`), measure it, and send it to the owner
(caco + a climb note). The owner decides. Album-wide alignment (a motif reprised, the album's palette) goes in
`motifs.md` first.

## Principles

- **Original**: invent riffs, rhythms, harmonies and forms. Never copy or closely imitate an existing song, including
  the records we reproduce: they inform the sound palette, not the notes.
- **An album**: a shared tuning, palette and motif bank; each track its own tempo, meter, texture and intensity; the
  songs bleed into one another.
- **Interesting**: tension and release, development, surprise; repetition that changes.
- **A sound playground** (Harry, 28 Oct): invent new guitar and drum sounds for the album and compose against them.
  Trade sounds back and forth between parts and between composers, give parts their own rhythmic cycles, and swap
  sounds between sections. Put new sounds in the sound bank.

## Publishing (public text)

How chirpers appear in public (Harry, 1 Nov), in tags, video titles, descriptions and channel text:
- The band is **chirpers**, always lowercase, and its own entity: no personal names in public text.
- The music is composed, not prompted. Do not lead with "AI-generated"; the fair technical line is that every track is
  written in Rust, note by note, and synthesized from scratch (no samples, no loops, no recordings).
- Only original albums are published (compose/chirpersN), never reproductions of other artists' songs.
- `tools/ytpub.py` (kit, upload, update, channel) applies all of this; the channel is youtube.com/@chirpersmusic.
