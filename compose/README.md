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
   A song written by a generator (`compose/ALBUM/src/ALBUM-tN.py`): WRITE THE FORM AS ARITHMETIC from the first
   round. Every section's start, every lane's point and every landing computed from a few weights (how long a row
   is, how many rows a section has), never typed as bar numbers. Plain Hunt's v5 (14 Nov) changed tempo, the riff's
   length and the song's length in ONE flag because of it, and the flag off still gave v4 byte for byte.
   A NEW SONG'S FIRST ROUNDS: read its first full section AGAINST THE ALBUM'S REFERENCE RECORDS, and by part
   (`tools/stembal.py song … --refs … --windows … --voice --parts …`), as soon as it has one. The scorer's spectrum
   term will not say it (it reads the whole song against a wide envelope). Plain Hunt was first read at v8, seven
   versions in, and its last stretch stood +2.9 dB at 250-500 Hz and -2.6 at 120-250. (`--id ALBUM-tN` puts the
   read on record; `climb.py next` says when a song is unread or four versions stale.)
   And at v2 or v3, read WHAT JOINS over the whole song: `tools/entries.py ALBUM-tN`. Plain Hunt's first cycle
   gained nothing but crashes, the calls' toms and a hat for two minutes (0:16 to 2:14); the list says it in one
   glance, and it was first looked at at v9.
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

**The tools' tests** (14 Nov): `python3 tools/tests/run.py [WORD …]` runs every test file, each in its own process
(about two and a half minutes for all 132; `run.py stembal presence` for a few). Run it after changing a module
other tools import. Do not use `pytest tools/tests` in one process: a few test files set their own scratch root as
they are imported, and it reports thirty failures that are not there.

`tools/chirpers.py status ALBUM` shows the album; `chirpers.py refresh ALBUM` re-renders every composed song and
re-saves features (run it after several songs change).

### Round types (Harry, 2 Nov)

An album can set `params.rounds` in its `album.json`, e.g. `{"whole": 0.4, "section": 0.4, "palette": 0.2}`. Then
`climb.py next` draws each round's TYPE, from those weights, per song and round number (reproducible), and the brief
says which. `next --type T` overrides the draw when you have a reason; `climb.py type ID` prints one song's type, for
owners who rotate their own songs. Name the type in your round note. Without
`params.rounds`, every round is a whole-song round as before.
A SONG MAY CARRY ITS OWN WEIGHTS (15 Nov): `"rounds": {"whole": 0.4, "section": 0.6}` on its track in `album.json`
stands for that song in place of the album's. For a song whose palette is settled (every instrument kept by Harry's
ear or waiting on his answer), so the draw stops landing on a palette round with nothing honest to do: Odd Sympathy
drew three in one night. It is the composer's to set and to take off again; say so in the round note.

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
  Before the full render (14 Nov, each from a round that would have been shorter with it): under every staple the
  brief says what it DOES here, and `--roles` says it for every track (the bars where a part is the floor);
  `chirpers.py palette ALBUM-tN --bench TRACK FROM-TO PATCH[@DB] [--layer]` (`tools/swapbench.py`) puts the new
  patch on the same notes, alone through the track's routing: the bands a swap LOSES, whether a layer is THERE.
  When the part has rests in the window it also prints THE PART'S RESTS: how far each patch has fallen by the second
  half of a rest, against its notes (-10 is a stop, 0 a rig that plays through; FILLS THE RESTS when a patch is 3 dB
  or more nearer its notes than the present one). A riff with sixteenth rests on a rig that fills them is not the
  same riff (chirper-zero, Running Total v6: the plain wall +0.5, its stop form -10, the twin rig -24).
- **An effect inside a library patch can ride a lane, with no copy of the patch** (chirper-zero, Common Time v47):
  `patch: "ct-crunch-l fx.6.mix=auto.wet"` and `auto: {wet: {points: [["0b", 0.2], ["1440b", 0.7], …]}}` on the
  track. Any parameter a patch string can set takes `auto.NAME` the same way.
- **A new part in an empty band: bench it at -6 dB first.** A lone high tone needs far less gain than a part in a
  full band (K-weighting, and nothing to mask it): two music boxes set from the song's opening came out over the
  guitars and their bars 3 dB louder than the holds around them; 7 dB came off before the first full render.
- **Does the part keep its tone in every key?** `tools/keyshape.py SONG bass` (or `gl,gr`): the part alone on each
  ground it plays, each band against its own total, against its home key; and home's own bars played there, so a
  loss is told apart as THE RIG (an eq or compressor fitted to one ground) or the notes. Run it at a song's first
  key change. All four of Common Time's songs carried a bass bus fitted on F: off it the bass alone lost 4 to 10 dB
  from 250 Hz up, the mix read "+1 at 60-120, -2 at 120-250", and Harry's "more bass" on one such stretch was
  answered with a fader. When his ear asks for MORE of a part in one place, read the part alone there against
  itself elsewhere before reaching for level.
- **Does the endless thing hold?** `tools/endless.py SONG TRACK,TRACK FROM-TO --cycle 1bar` (a Shepard scale, a
  Risset rhythm, a barber pole, a riser that never arrives): the illusion's parts alone, one cycle against the
  next (level, bands, the centroid's drift in octaves a cycle: a real climb reads 1.00), a LONGER cycle under it
  (parts that take turns and are not alike), the song's notes cycle by cycle, and the inside of the cycle with
  the wrap (a SAW-TOOTH is a run undone at the wrap: the riser starting again). `chirpers.py illusion` says the
  part LEADS; this says the illusion HOLDS. Neither says an ear hears it climb. An illusion on a distorted
  guitar is written out a copy a track with fader lanes (the engine's `risset` fades ahead of the amp).
- **Where does a `risset` track sound?** `tools/risset.py SONG [TRACK] [--bars A-B]`: the song writes only the
  pattern; this lists every copy's strokes with their speed and level, bar by bar (the engine's arithmetic,
  checked against its audio). `endless.py` reads such a track through it. On a clean kit the engine's `risset`
  is the illusion as written; through an amp, write the copies out (above).
- **A pedal that changes every bar**: `keyshape.py SONG bass --min 1 --pool` reads each ground from as many of
  its bars as make eight.
- **An eq band's cutoff rides a lane too**: `{"kind": "peak", "cutoff": {"value": 44, "mod": [{"src": "auto.key",
  "amount": 0.08333}]}, "q": 1.5, "gain": "-7dB"}` on a bus with a lane `key` in semitones over the home ground (a
  frequency mod is in octaves, so 1/12 a semitone). The mend for a rig fitted to one key.
- **What joins, and where else does it play?** `tools/entries.py SONG --from A --to B` lists every part that
  enters over a stretch, in order, a kit's pieces apart (a missing step in "something joins at every landing" is a
  gap in the list). `tools/rests.py SONG TRACK:PIECE` says where one drum of a kit plays: when Harry turns a device
  down in one place, look for the same part elsewhere the same hour.
- **Can it be heard?** A spring, an echo or a ring is heard in the gaps between a part's notes. `tools/rests.py
  SONG TRACK …` lists them from the plan (and what else sounds in each); a part with none says so. Harry could not
  hear a dripping spring for nine versions because the guitars carrying it never rested.

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

**Reading recurrence** (14 Nov, chirper-zero, Plain Hunt v6): `tools/secsim.py ID WAV…` prints the scorer's own sections on each of the album's novelty cuts and, for each from the third on, the earlier non-adjacent section it best matches and how well. Look there BEFORE guessing a cure: a passage changed in one cycle and not in its twin makes the twin match less. `--text` adds an ON THE EDGE line when a cut's share sits within 0.02 of the band's end: there the term reads 100 and says nothing until the next change tips it.

**How loud is one stroke?** (16 Nov, chirper-zero, Running Total v8): `presence.py`'s `vs mix` is a part's power while it sounds, and a short stroke with a tail (a room, a ringing bar) sounds all the time, so `vs mix` follows how OFTEN the part strikes: a knock at one velocity read -11.2 dB striking every bar and -3.6 striking eight times in two bars. Under each table presence now prints SHORT STROKES: each stroke's own tenth of a second against the mix's same tenth (the median, low to high, how many), for parts whose strokes `vs mix` reads 3 dB or more low. Level a sparse part by that figure; a held or fast-repeating part has no strokes there and `vs mix` is its figure. A drum's strokes sit about -3 to -5 dB under a mix (Running Total's kick).

**Does an illusion that changes speed hold?** (16 Nov, chirper-zero, False Summit v9: a fall that steepens): `endless.py SONG TRACKS FROM-TO --cycles 2x6bars,2x3bars,2bars,2x1bar --steps 6 --seeds 0,11` reads the cycles in order whatever their length (a slice is the same step of the figure at every speed): cycle by cycle, speed by speed (a speed with ONE cycle is read against the joins either side), and each change of speed. Read it on TWO seeds: where a slice holds two or three notes the players' own variation moves its brightness by half an octave, so a mark is given only when every seed has it. The strongest line is THE CYCLE'S SHAPE: every cycle of every speed and seed together, slice by slice, with its standard error; A PLACE IN THE CYCLE is a slice that stands out in that mean: something the ear can find once a cycle.

**Whose band is it?** (16 Nov, chirper-zero, three times in one day): a held, pitched part can be most of one band of the mix while reading "buried" or ordinary by level: a synth riser was most of a climax's 500 Hz-1 kHz for five versions. `presence.py` now prints, under each of its tables and from the same renders, WHOSE BAND IS IT: for each of the nine bands, the tracks that ALONE are within 6 dB of the mix's own band there (0 = the track is the band, -3 about half). When `stembal.py` reads a band over the records in a passage, run presence on that passage and read the band's owner before mending; `stembal.py … --parts NAME=track,…` is the longer table for chosen parts. Tracks that are the left and the right of one part by name (gl/gr, el/er) are also read TOGETHER, their powers added, so a pair is listed even when neither side holds the band alone. A pure-toned part (a music box, a bell, a marimba) holds its fundamental's band at a level where a guitar would not: for such a part read this block, not `vs mix` (Odd Sympathy v24).

**Is a "static" window static in its notes?** (16 Nov, chirper-zero, False Summit v8 and Plain Hunt v13): the section map's flag hears tone, harmony's level and (in its own column) rhythm, half a second at a time; it cannot hear WHICH notes. A harmony written on one side of a stair, a key change at one level, an accent that moves place every row all leave a window "static". Under each static window the map now reads the plan, part by part (a pitched track, or one piece of a kit's track; a note is its place in the bar and its pitch class): how many parts LOOP (every 1, 2 or 4 bars), which CHANGE in the window and at which bar, and which NEVER SETTLE. A window whose parts change or never settle is static in its SOUND: listen before rewriting it, and do not read the flag as "nothing happens here".

**What is a part's loss worth in the mix?** (16 Nov, chirper-zero, Common Time v51): `keyshape.py` reads a part ALONE, and a 7 dB loss of the bass's upper bands on another ground was worth 1 dB of the mix at 120-250 Hz and nothing above: the guitars hold those bands there. Under each ground that LOSES it now prints IN THE MIX: the whole song over the same bars, how far the part alone sits against the mix in each lost band, and what the loss is WORTH (the dB the mix's band would rise were it mended), and COVERED when no band is worth 0.5 dB. A covered loss is not heard as level; it may still be the part's own tone where it is exposed. It costs about 40 s a losing ground on a full song: `--no-mix` while fitting a mend, the mix once at the end.

**How many cycles does a drift need?** (16 Nov, chirper-zero, False Summit v6): where a passage HOLDS over seven cycles (False Summit's stair: +0.009 octaves a cycle), neighbouring cycles still differ by up to 0.11 octaves. So `endless.py` marks DRIFT from two cycles only at 0.13 octaves a cycle, from three at 0.064, from four or more at 0.05, and says when a smaller figure is left unmarked. Give it three cycles or more where the song has them.

**A short section can carry a form term** (15 Nov, chirper-zero, Running Total v6): structure and variety count a section as one whatever its length, so a few seconds cut off as a section of their own (a last chord on a new rig; a dead stop) can move them as far as a new passage would: there, six points of the total from four seconds of 276, while the passage the round was about was a seam at no cut. `compscore.py ID WAV --text` now says so under the terms when it is so (`A SHORT SECTION CARRIES A FORM TERM: 267-271 s …: structure 98.0 (89.5 without); variety 72.7 (42.9 without)`): the score is unchanged, the line says which seconds the points sit on. Read it, and `secsim.py`, BEFORE writing what a gain means.

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

### Questions for Harry's ear (the review page, 14 Nov)

Harry, 14 Nov: "hard to answer qs in chat - if you put them on the review site as side by side comparisons with a way
to give feedback as an answer I can review in batch." So a question a measurement cannot settle goes ON THE PAGE, not
only in a message:

    python3 tools/listen.py ask ALBUM --track N --version v7 --key os-words --at 33 \
        --title "Can you make out the spoken words now?" --context "what changed, what to listen for" \
        --ab "v6|v7=/path/to/clip-ab.mp3" --clip "the voice alone=/path/to/clip.mp3" \
        --choice "Yes, clearly" --choice "Some of them" --choice "No, the band still covers them"

THE PAGE SHOWS ONE QUESTION AT A TIME (15 Nov). Harry, with 26 cards waiting: "questions are very busy and hard to
even parse or answer"; "make it easy to respond, like a flick thru view w autoplay, maybe with shorter more focused
examples for some things". Each card now plays by itself when it comes up, its takes in turn (A, B, A ...), opening
on the few seconds where they differ; an answer brings the next card. Your notes are folded away under it. He
answered eight cards in five minutes the night it changed. So write a card for a listener who is flicking through:

- THE TITLE IS THE QUESTION, AND ONLY THE QUESTION, short: "A drummer pulling against the beat, or lost?". The page
  sets a long title's last question large and what stands before it small, and lifts a bracketed "(you said: ...)"
  out; a title that is only the question reads better still. What changed goes FIRST in `--context`, one sentence:
  under a short title the page shows that sentence small over the question (and the next one too when the first
  is a few words), and folds the rest away. The takes carry their own labels, so "A is v1, B is v2" is not needed;
  the measurements go last.
- THE A/B IS SHORT AND ON THE CHANGE: 6 to 10 seconds, starting a bar before it. The page finds the seconds to open
  on by measurement (from a second and a half before the takes first part, 4 to 7 s; takes of 11 s or less play
  whole) and `ask` prints them; `--focus START-END` (seconds into the takes) sets them yourself, and
  `listen.py questions ALBUM --focus` lists every card's. ONE more clip at most, and only if the answer needs it.
  A card with no A/B (two clips of different passages) plays each once, in order.
- TWO TO FOUR CHOICES, a few words each. Five or six is a questionnaire.

- `--ab "A|B=FILE"`: the usual A-then-B clip (a silence between the takes) is cut into its sides and shown side by
  side; when the sides are the same length he can switch between them mid-phrase. It takes any number of takes, a
  label each ("1|2|3|4|5=FILE": five voices in one row). `--clip` is one player.
- `--choice` are buttons; he can always write instead, or as well. One question a card: ask two things as two cards
  unless one answer covers both.
- `--parts TRACK[:PIECE],…` NAMES THE PARTS the question is about (`--parts ride:rb,hat`). When it is answered, the
  message that brings you his words also says where else those parts play in the song as it then stands, the
  question's own place starred. An answer about one place is often an answer about a device: a ride-bell pendulum
  he turned down in two passages went on opening the song for seven hours (15 Nov). A new track of a version not
  yet in `songs/` reads "not in the song now" when you ask: the card stands (the line is read again when he
  answers), and asking after `climb.py done` shows the bars at once.
- When a change is being taken back or softened, ask THREE WAYS in one `--ab` ("as it first was|as I made it|a
  middle=FILE": three takes with a silence between). On 14 Nov the snare asked so got one clear answer ("Now: the
  air is back") where an A/B would have had to be asked twice.
- `--key`: a name for the PASSAGE. Ask again with the same key after a new version and the old card leaves the page,
  so he is never asked about a superseded clip. `listen.py retire ALBUM ID` takes one off by hand.
- The page keeps its own copy of each clip. His answers come back verbatim in ONE caco message two minutes after he
  stops (`listen.py questions ALBUM` shows them all). Keep the question in your round note as well.
- A card's clips are from the version it was asked on. At every snapshot the page measures, for each card, the same
  seconds of the song then and now (the mean difference of the band envelopes, in dB), and a card whose passage has
  moved says so: "the mix has moved a little since" (0.15 dB or more) or "this passage has changed since" (0.6 or
  more), with the song's current version. `listen.py questions ALBUM --moved` lists them, the furthest first: those
  are the ones worth asking again with the same `--key`. A card with no tag still sounds like the song.

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
