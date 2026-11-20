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
says which. `next --type T` overrides the draw when you have a reason; `climb.py type ID` prints one song's type.
Name the type in your round note. Without
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

**Reading recurrence** (14 Nov, chirper-zero, Plain Hunt v6): `tools/secsim.py ID WAV…` prints the scorer's own sections on each of the album's novelty cuts and, for each from the third on, the earlier non-adjacent section it best matches and how well. Look there BEFORE guessing a cure: a passage changed in one cycle and not in its twin makes the twin match less. `--text` adds an ON THE EDGE line when a cut's share sits within 0.02 of the band's end: there the term reads 100 and says nothing until the next change tips it. Give it the kept version's render and then the candidate's and it ends with WHAT CHANGED: under each render THE TERM (the mean of the cuts' scores, naming the cuts under 100), then for each cut whose score moved the seams that are GONE (two sections now one: it counts once where it counted twice), NEW or MOVED, and the sections whose return counts more or less. A term of 96.4 is usually six cuts at 100 and one outside the band: on Plain Hunt v15 every match that fell stayed inside the band and the 3.6 points were one cut where the seam at 206 s was no longer found (16 Nov).

**How loud is one stroke?** (16 Nov, chirper-zero, Running Total v8): `presence.py`'s `vs mix` is a part's power while it sounds, and a short stroke with a tail (a room, a ringing bar) sounds all the time, so `vs mix` follows how OFTEN the part strikes: a knock at one velocity read -11.2 dB striking every bar and -3.6 striking eight times in two bars. Under each table presence now prints SHORT STROKES: each stroke's own tenth of a second against the mix's same tenth (the median, low to high, how many), for parts whose strokes `vs mix` reads 3 dB or more low. Level a sparse part by that figure; a held or fast-repeating part has no strokes there and `vs mix` is its figure. A drum's strokes sit about -3 to -5 dB under a mix (Running Total's kick).

**Does an illusion that changes speed hold?** (16 Nov, chirper-zero, False Summit v9: a fall that steepens): `endless.py SONG TRACKS FROM-TO --cycles 2x6bars,2x3bars,2bars,2x1bar --steps 6 --seeds 0,11` reads the cycles in order whatever their length (a slice is the same step of the figure at every speed): cycle by cycle, speed by speed (a speed with ONE cycle is read against the joins either side), and each change of speed. Read it on TWO seeds: where a slice holds two or three notes the players' own variation moves its brightness by half an octave, so a mark is given only when every seed has it. The strongest line is THE CYCLE'S SHAPE: every cycle of every speed and seed together, slice by slice, with its standard error; A PLACE IN THE CYCLE is a slice that stands out in that mean: something the ear can find once a cycle.

**Whose band is it?** (16 Nov, chirper-zero, three times in one day): a held, pitched part can be most of one band of the mix while reading "buried" or ordinary by level: a synth riser was most of a climax's 500 Hz-1 kHz for five versions. `presence.py` now prints, under each of its tables and from the same renders, WHOSE BAND IS IT: for each of the nine bands, the tracks that ALONE are within 6 dB of the mix's own band there (0 = the track is the band, -3 about half). When `stembal.py` reads a band over the records in a passage, run presence on that passage and read the band's owner before mending; `stembal.py … --parts NAME=track,…` is the longer table for chosen parts. Tracks that are the left and the right of one part by name (gl/gr, el/er) are also read TOGETHER, their powers added, so a pair is listed even when neither side holds the band alone. A pure-toned part (a music box, a bell, a marimba) holds its fundamental's band at a level where a guitar would not: for such a part read this block, not `vs mix` (Odd Sympathy v24).

**Does the song step where it should?** (16 Nov, chirper-zero, Running Total v10): band readings against the records cannot see a form fault: sections that should step and do not. `tools/seams.py ID --wav FINISHED.wav` reads the plan for its seams (every place a part enters or leaves) and the finished file for each stretch's loudness: bars, time, LUFS, the step into it, who came and went; then where the song steps up 1 dB or more and its loudest stretch. Read whether the arrivals you wrote are in that list. ENTERS, NO STEP marks a seam where parts come in, none leave and the level hardly moves: a question for an ear. An arrival made by the same players is not a seam: give it as `--windows 21-33:count 33-41:whole 41-49:total`. Run it on a skeleton: Running Total's flat arrival was there from v1 and found at v9. `--bands` adds each stretch's nine bands against the stretch before it; `--bands first` against the first stretch given: the like-for-like read of a passage the records cannot judge (held chords against busy records prove little): `--windows 378-386:riff 386-387 387-388 388-389 389-390 --bands first` showed three of Common Time's four landing chords 4 to 5 dB short under 60 Hz against the riff before them (v53).

**Before an EQ, ask what share of the band the part has** (16 Nov, chirper-zero, Plain Hunt): `tools/presence.py` ends its WHOSE BAND IS IT lines with WHAT AN EQ ON IT WOULD MOVE: for each part (or left and right pair) that holds a band, its share of the band's power and how far the mix's own band moves when that part alone is turned up 2 dB there (`gl2+gr2 28% +0.6`). A part at -5 is a third of its band: 2 dB on it is 0.7 on the mix, and a peak gives less than its gain across a whole band. When the holders are all minorities, the band wants a part, not an EQ.

**A cut outlives its reason** (16 Nov, chirper-zero, False Summit v13: "an EQ set against a pile outlives the pile"): `python3 tools/eqcuts.py ID` lists every EQ band that cuts 1.5 dB or more (on a track, a bus, a patch, the master), the version it dates from (it plans the song's whole history, cached), and WHO HAS LEFT SINCE: a part that sounded on a quarter of the cut's beats when it was made and on half that or less now, whether its notes went or a gain lane turned it down. Run it in the round where a part leaves: `--song CANDIDATE.yaml`, or `--versions v10=OLD.yaml cand=NEW.yaml`. It reads notes and lanes, not sound: a mark is "re-read this cut", and the reading is the band with and without it (`stembal.py`, `seams.py --bands`). `--from 300 --to 1500` keeps to a range; cuts the song began with may be the family's own.

**A part that a rule writes** (16 Nov, chirper-zero, Carrying Capacity): a track may have no notes and only `gen` (one complex system or a list played one after another: logistic, lorenz, ca, lsystem, markov, life, henon, walk). The plan turns it into notes, so every tool that reads the plan (entries, rests, sectionmap, seams, presence, notechk …) sees them as written notes: check them against your own arithmetic with `chirp --json plan -f SONG` (his 171 lead notes: 0 differ; the first value emitted is f(x0), the pool index is floor(x * len), `rest` is a threshold). `tools/showcase.py` reads a track's `gen` and `score` from the song's FILE for the same reason, so the checklist's "generative systems" line counts them.

**A page of your own on the review site** (16 Nov, chirper-zero's digest "what changed while you were away"): put the page where the review server serves files as they are (`~/.local/state/chirp-eco/review/clips/`, http://pocket4:8790/clips/) and list it in `compose/ALBUM/links.json` as `[{"title": "While you were away", "url": "http://pocket4:8790/clips/NAME.html", "by": "you"}]`: the review page shows it in its bar beside Listen, Questions, Feedback, Worklog and History (http(s) links only, titles to 60 characters, six at most). Link a question as `http://pocket4:8791/#a=ALBUM&v=questions&q=ID`. Give the page `<meta name="viewport" content="width=device-width,initial-scale=1">`: Harry reads on a phone.

**Does the picture lean?** (16 Nov, chirper-zero, Odd Sympathy v26): `tools/levels.py WAV…` lists THE PICTURE under its table: right minus left over each whole file, the correlation of the two channels and the DC offset, flagging LEAN (half a dB or more over a song), ANTI (the channels correlate negatively: it thins in mono) and DC. `tools/seams.py` ends with the same figure for the file and the stretches that lean 1 dB or more: a side that enters first, a pair whose cones are not level. Common Time's five songs read -0.4 to +0.1 dB over the song.

**Where in a window did the round land?** (16 Nov, chirper-zero, False Summit v11): `sectionmap.py --against OLD.wav` gives one residual a window, and a window is half a minute: a fader moved in its last five seconds reads as the whole window's. Under the table it now says so: "w7's change sits in 3:16-3:21 (5 s of its 29): the rest of the window reads -50.1 dB, untouched". Read that line before taking a far window's residual for a side effect; the engine's renders do not depend on what was silent earlier (a node is skipped only on exact silence past its effects' tails, and effects take their phases from song time). And the scorer's spectrum guard is not `stembal.py`: it is the WHOLE song, every frame alike in dB, against the album's genre records, so a song with a minute of marimba and no bass reads short of bass there (Running Total: -7.6 dB at 97 Hz over the song, -5.0 in its louder half) while every heavy section is on the records.

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
- **`tools/modlint.py [ID|FILE ...]`** (default: the focus album): frequency mod amounts are in OCTAVES (`cutoff=800+lfo.a*2` sweeps two octaves); an amount written in Hz (-2600) shuts or opens the filter the moment the source moves (t8's horizon light was buried at -42.6 dB that way). Flags any beyond the engine's whole 14.9-octave range. Seconds per song. It also reads every KEY LANE (a lane that moves an eq's bands a semitone a unit, as the bass bus's `key` does) against the lowest note of the part it serves and says where the lane went THE LONG WAY ROUND (+10 while the notes went -2: False Summit's fall carried that from its skeleton to v9) or DOES NOT FOLLOW; those lines are questions and do not fail the lint. Run it after writing or changing a key lane.
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

## Every song is everyone's (Harry, 18 Nov)

NO SONG HAS AN OWNER. Harry, 18 Nov, verbatim: "climbing should not have owenrs, owners should be able to take the lock on
any song"; "a new round should release for anyuone to improve"; "tha tis hos we maintain variaety".

- `climb.py next` draws among every queued song of the record, whoever worked on it last. Starting a round takes that
  song's LOCK: for 90 minutes, or until you record the round, the draw leaves it out for everyone else and
  `next --take ID` refuses it to them (`--force` overrides; use it only when the holder has plainly gone).
- `climb.py done` records the round and releases the song. The next composer to draw it may change anything in it.
- DO NOT PASS, AND DO NOT WAIT FOR AN EAR (Harry, 19 Nov, verbatim: "can we stop passing on songs. ill add card replies
  but please we have so much we could do re: improving our instruments, better guitars, etc and just general
  improvements"; and: "try not to raise so many cards, just be creative"). On 18 Nov every song had been passed on as
  "full until heard". Versions he has not heard and cards still waiting are no reason to hold a round back. When a
  song's notes are settled, there are its INSTRUMENTS: the draw has a round type for it (`next --type instrument`): make
  one instrument sound better, heard alone and in the mix against the album's records; a gain in a library patch goes
  under a new name (`tools/libguard.py`); where the engine falls short, a bead with numbers. `climb.py pass` refuses
  now; `pass ID 'why' --anyway` is only for a song that cannot be touched (its files mid-change under someone else).
- AN INSTRUMENT ROUND'S YARDSTICKS (found on 19 Nov, by the composers named; the round's brief carries the short form):
  - the part ALONE against a record's lone part: guitars with `tools/cabspec.py`; a snare at its own hits with
    `tools/drumpunch.py`'s measures against the records' drum stems (body 150-300 Hz and wires 5-12 kHz against crack
    1.5-5 kHz: the album kit's snare read +5.0 dB body-to-crack, the records' median -3.2; chirper-zero's bench is
    `~/.local/state/chirper-zero/c10/t11-snare/sn.py`); a part's share of its OWN power by band says what it is before
    any record is consulted (a lead with 1% at 4-8 kHz has no pick: chirper-alpha).
  - a guitar's STROKE against the records' own strokes: `tools/riffpunch.py --strokes --song-file songs/ID.yaml
    --tracks gl,gr --from S --to S` (seconds; the rig you are judging) prints rise, punch, tight, fizz, scoop and
    grain beside six records' guitar stems read at their own chugs. Through a stroke the records' guitars carry
    11.3 dB more at 1-4 kHz than at 400 Hz-1 kHz (scoop -11.3; -12.7 to -6.5); the album's `ct-twin` chug read
    -4.4 on Extreme and Mean and -5.1 on In the Time Of: EVERY song's muted strokes are written at a full palm
    (pm 1.0), which closes the string's filter to 1 kHz before the amp, and the 700 Hz lifts on the twins date
    from the yardstick with voices in it (chirper-zero, Extreme and Mean v23: -7.7 after). Take Up the Slack v12: -4.6 to
    -11.5 with the same cure; Common Measure v24: -5.0 to -10.0 on six guitars. THREE songs agree on what a
    `ct-twin` successor wants: the palm two octaves not 3.4, and no 700 Hz lift. The microphone and the 800 Hz
    cut are NOT part of it: they are the mix choosing the amount (a song with no voice kept the microphone at
    0.5; the cut was 0, -3 and -4 dB on three rigs). Do NOT cut a guitar's top on `fizz_db` or a by-part
    8-16 kHz figure: the separator takes the guitar's top (the records' guitars ALONE read -22.5 to -25.4, their
    stems -33 to -36 under a band; the tool prints it); for the top trust `cabspec.py`. The records give NO
    figure for how empty the rest after a stroke should be: a stroke "followed by a rest" in our transcriptions
    is not followed by one on their guitar stems (-4 to 0 dB under the stroke).
  - a BASS alone against the records' basses: `tools/bassspec.py NAME=SOLO.wav[:FROM:TO] …` (a raw solo render;
    thirds of an octave, as shapes; chirper-zero). The records have their weight at the OCTAVE (the 80 Hz band
    26 dB over 40 Hz); the album's `ct-bass` was a sub and a box (+16 to +18 dB at 40 Hz, -8 at 80, +5 to +11
    at 400-800 Hz). Two things about it: its sine sub DRIVES the bass's two compressors (moved an octave up at
    -12 dB it left nothing else: the string's twelfth fell 21 dB); and THE SUB BELONGS TO THE KICK on the records
    (their basses sit 16 dB under their drums below 60 Hz; ours are level): with the sine off the bass is
    nearest the records alone and by part, but the MIX falls 0.7 to 3.1 dB under 60 Hz, so the round it asks
    for is the kick's sub FIRST, then the sine off (In the Time Of v24 kept a partial move).
    The full move, on a song whose kick could take it (Take Up the Slack v15): the bass's sine 11 dB down, the
    kick's decay 210 -> 160 ms with +6 dB at 55 Hz: the mix's 60-120 Hz mean distance 1.19 -> 0.36. For the
    families: `kit.k.patch.synth.amp.d` IS the drum's tail (any lift of the kick's fundamental with the decay
    untouched rings 70 ms to -20 dB; the records 44); the kit bus's clip gives back 2.4 of 6 dB lifted on the
    kick; a band on the drums' bus reaches every piece on it; and where the bass plays with NO kick it must
    keep its sine (off, that stretch fell 10.4 dB under 60 Hz): the sine's level is the per-song field.
    WHERE THE MOVE IS WRONG (chirper-one, Still Owing, built and not kept, 19 Nov): when the song's ROOT is under
    about 45 Hz the sine IS the note (there E flat 1, 38.9 Hz, under any kick): sine off and the kick lifted
    scored 97.0 against 99.9, the mix moving AWAY from the records under 120 Hz. Read the bass's lowest notes
    before handing the sub over; and a kick whose weight sits at 60 Hz cannot take it (every lift went into
    60-120 Hz as much as under 60). The numbers are in that song's history; nobody need repeat it.
  - a CYMBAL, hat or china alone against the top of the records' drums: `tools/cymspec.py NAME=SOLO.wav[:FROM:TO]`
    (thirds of an octave from 1 kHz, as shapes; each stroke's fall a quarter of a second on; chirper-zero). The
    records' metal has its weight at 4-6 kHz and is 9 dB down by 12.5 kHz. The yardstick does not hang on the
    separator: the records THEMSELVES carry 5.7 to 7.4 dB more at 4-8 kHz than at 8-16 (median 6.1). But a
    record's stems together hold only 60 to 81% of its 8-16 kHz power: trust a stem's SHAPE, never set a level
    against it. On the modal plate BRIGHT fills the top octave, not TILT; the kit's DRIVE on the china is its
    ring (drive 0 is a splash: 21 dB down in a quarter of a second).
  - a SNARE alone against the records' snares: `tools/snarespec.py NAME=SOLO.wav[:FROM:TO] … [--each]` (thirds of
    an octave, as a shape, with body and wires against crack and the stroke's fall; chirper-zero). What it shows
    that the two ratios did not: the album kit's snare has its NOTE in the 250 Hz band where the records have
    theirs at 200, and humps at 1-1.25 kHz and 2-2.5 kHz where theirs dip. `kit.s.pitch=G3` moves the note;
    `shell`, `shell_hz` and `reso_level` move nothing; `damp` 0.9 takes 2.5 dB off 1 kHz. NOT YET BENCHED (his
    correction): the head's `mode_count` (default 24; the 1-1.25 kHz hump is its upper explicit modes) and
    `slap` (the kit has 1.2; probably the 2-2.5 kHz hump): bench `kit.s.patch.synth.layers.0.mode_count=10..16`
    and `slap=0.4..0.8` against the tool BEFORE reaching for eq. Two cautions: the drums' bus glue and clip make a snare's measures depend on its
    FADER; and a snare's box can be standing in for guitars that are short at 250 Hz-4 kHz: let the MIX say
    how much of the cure to keep (Extreme and Mean v26 kept half).
  - a MUTED STROKE's low end (`riffpunch.py --strokes`, the LOW END column): on all six records the 100-250 Hz of
    a chug HOLDS OR GROWS through the stroke (the first 20 ms against 40-80 ms: -1.1 dB; -2.2 to +0.3); ours
    died (+2.3 to +3.5). The string's mute, its decay and the amp's tight filter move that a decibel at most;
    THE PALM'S WEIGHT moves it three, and every muted stroke on this album was written at a FULL palm. At 0.55
    all five of the yardstick's measures stand inside the records' range (chirper-alpha, So Far v15).
  - BY PART (`stembal.py song … --voice`, the group rows): read the two `groups:` lines first; until 08:18 on 19 Nov
    the default groups left guitars out on sixteen of seventeen songs. A figure is a share of the whole mix.
    `OUTSIDE THE GROUPS` under a window's table names a band where half or more of the mix is in NO group's tracks
    (Plain Hunt: one church bell held 54% of the first cycle's 500 Hz-1 kHz, more than the four rhythm guitars
    together; chirper-zero): there a group's figure is not the band. Read whose it is (`--parts TRACK,TRACK`,
    or `tools/presence.py`'s "whose band is it") before moving a grouped part on it.
  - THE MIX on the NO-VOICE rows for a window where nobody sings. A change is kept when the mix agrees: the records'
    stems do not sum to their mixes, and a rig fitted to a record's lone guitar can be wrong in the mix (chirper-zero).
  - THE BARS YOU DID NOT TOUCH SHOULD NULL against the last version: a tone change moves the master's gain, so the
    practice is to re-fit the song's loudness target until an untouched passage nulls. The master's gain is NOT
    continuous in the target on a song with quiet stretches (bd-dab22a, The Other Hand v18: targets -10.3075 and
    -10.305 gave an untouched passage 0.113 dB under and 0.098 dB over, with nothing between): when two targets
    0.0025 apart straddle zero, take the nearer and say so in the note (chirper-zero).
  - A WRITTEN BEAT BETWEEN TWO NOTES WANTS OSCILLATORS, NOT STRINGS: two plucked strings a hair apart do not hold
    the beat you wrote (`lead-tape`, also with `tune_sounding`, `vary=0` and `planes=0`: the lows fell at 0.50,
    0.88, 0.54, 0.82 of the half pulse, and two strings on ONE note swung 18-23 dB); an oscillator does (0.49 to
    0.53; 0.2 dB) (chirper-zero, Close Enough v10).
  - A SLIDE WRITTEN `expr` > `expr_end` ENDS AT THE GATE, not at the note's end: at the default gate the ramp is
    done at 95% of the note, and a 22 s slide read 0.5 cent flat at 20 s; `play.gate=1` on that part puts it
    within 0.02 cent (chirper-zero, Close Enough v10).
  - A PART THAT PLAYS THE VOICE'S OWN NOTES ON THE VOICE'S OWN ONSETS TAKES THE WORDS, even 4 to 9 dB under it:
    sung over a fretless bass playing the same notes at the same moments, `tools/wordread.py` read 3 of 10
    words from the mix and never more than 4 with the voice 6 dB hotter, brighter, an octave up or sung early
    (voice alone 9 of 10); with the bass resting 9, 9, 9 on three seeds; a floor tom or a held pad under the
    voice cost nothing. Read the words on the finished file with the song's OWN seed (chirper-alpha, Where It
    Was v22).
  - A PART WRITTEN ON ANOTHER PART'S PARTIAL MUST BE READ SUMMED, not each alone: an oscillator and the harmonium
    both start their cycle on the note's first sample, so two parts on one frequency stay phase-locked. A lead on
    the reeds' second harmonic stood 158 to 173 degrees from it: the shared line read 7.7 to 11.1 dB UNDER the
    reeds alone, and a power sum of the separate solos hid it (every by-part and `--parts` figure is a power
    sum). `saw phase=0.5` on the lead turned it over: +3.2 to +4.7 dB. His reader:
    `~/.local/state/chirper-zero/c10/t16-alone/phase.py PAIR.wav LEAD.wav` (chirper-zero, Close Enough v11, a
    defect in his own v10 found and mended).
  - YOUR SCRATCH (`/tmp/lt`): the janitor keeps at most 10 GB of audio there and deletes what is idle. `touch
    DIR/.tmpclean-keep` on a round's directory WHILE THE ROUND IS OPEN; at its end delete the audio and the marker.
    Marked audio may hold at most half the cap: beyond it the least recently used marked audio goes first. What
    you must read again belongs in `ref/` or your state directory. Reading a file does not refresh its "last
    used" on this /tmp: `touch` a base render you depend on (`tools/tmpclean.py -h`).
  - a MASTERED render before `done`: the master limiter turns down bowed and sawtooth-like parts, and sparse passages
    come up; a new voice's HARMONICS before its loudness (chirper-zero).
  - the recogniser ALONE, not under render load (`asr.py` exits 3 when a window did not finish), on the FINISHED
    file, with a window long enough to hold the whole line (30 s): on a short window of a mix (under 20 s, one or
    two words in it) it returned one number repeated, "40 40 40…", for settings it read right on the finished file
    (chirper-zero, So Far v9).
  - a KICK alone against the records' kicks, hit by hit (chirper-alpha's `~/.local/state/wM/common-time/t15-v11/
    kickref.py`; `refkicks.txt` beside it has the eleven): the album kit's kick has nothing at 90-120 Hz (-28.8 dB
    as a share of its own 35-250 Hz; the records' median -13.6, the leanest -19.4) and rings 84 ms to 20 dB down
    where theirs take 37 to 49. What worked on Take Up the Slack: a bare sine an octave over the drum on its OWN
    track. What did not: the same as a layer inside the kick's patch (its drive is one ceiling), more fader (the
    kit bus clips: 0.2 dB per dB), a shorter tail (it wants a bass that holds the sub first).
  - what you learn about a LIBRARY patch as it comes (tonight: `lead-tape`'s drive after its cabinet; the eight-string
    family's vibrato on held chords; `m8-lead-guitar` without a pick; the album kit's snare and kick; a tabla that is
    one held note when played fast; `ct-twin`'s full palm and raised mids; `ct-bass`'s twelfth louder than its
    fundamental on the low notes, and its sub; the kit's metal (`haake-hat` and the china: hiss above 8 kHz with
    nothing struck under it, where every record's drums carry about 6 dB more at 4-8 kHz than at 8-16); the plucked string's pitch, now `tune_sounding`) is worth a successor under a NEW name for every song: yours to write, `libguard.py`
    and chirp-eco to gate.
- THE LAST WORD ON A SONG IS NOT YOURS TWICE (18 Nov, at chirper-two's asking, who was drawn Common Measure five times
  in a day). The draw leaves out of YOUR draw the song whose last round is your own, while any other free song is
  queued: after your round it is for someone else. `next --take ID` brings you back to a song on purpose; `next
  --peek` looks without taking a lock. (If every free song is one you had the last word on, `next` says NOTHING NEW
  FOR YOU and starts nothing; `next --again` draws among them anyway, and with Harry's words of 19 Nov that is what to
  do: there is always an instrument to improve.)
- THE FILES EVERYONE WRITES (`motifs.md`, `sounds.md`, `features.md`) CAN HOLD SOMEONE ELSE'S OPEN LINES: a composer
  writes their paragraph before their round is recorded, and `commit` and `done --with` take a file whole. Look first
  (`git diff compose/ALBUM/motifs.md`). `done --with` REFUSES such a file, before anything is recorded, when one of its
  open hunks names neither your song (its id, title or tN) nor you (`--whole` takes it as it stands, when the lines are
  yours after all). When lines that are not yours are open in one, leave it out of `done --with` and commit your lines
  of it with
  `python3 tools/climb.py commit -m MSG --pick 'REGEX' compose/ALBUM/motifs.md compose/ALBUM/sounds.md`: only the hunks
  whose changed lines match REGEX (your song's title, your version) are committed; it prints what it left open, and
  every other line stays in the tree, uncommitted, as its writer left it. Lines that touch are one hunk and go in
  together: it says so when that happens. (chirper-zero, 19 Nov, who did this by hand.)
- Harry's notes and answers travel with the song, not to a person ("they will get notes hwen they next see the track"):
  the brief prints HARRY ON THIS TRACK, his open notes, his answers to the track's cards and the cards still waiting on
  him. When you act on a note, answer it: `listen.py reply ALBUM ID 'what you did' --done`.
- An empty slot is stood up by whoever draws it first (a title, a skeleton); from its first kept version it is in the
  draw for all.
- FEWER CARDS, AND A WAITING CARD FREEZES NOTHING (Harry, 19 Nov: "try not to raise so many cards, just be creative").
  A card is for what only his ear can settle; most rounds need none. From 18 Nov to 19 Nov this guide said to leave a
  passage with a card waiting alone; that rule was chirp-eco's and is withdrawn. If your round changes a carded
  passage: ask the card again on its key with clips from the new version if its question still stands (that replaces
  the card and adds none; a before/after's "before" rendered in the new mix too), or retire it
  (`listen.py retire ALBUM ID`) if your round answered or removed what it asked. `listen.py questions ALBUM --moved`
  lists the cards whose passage has changed since their clips were cut.
- The `owner` field older climbs carry, and "its name and its shape are X's" in an older track's role, say who composed
  the song first. They gate nothing.
- Album-wide alignment (a motif reprised, the album's palette) still goes in `motifs.md` first, and a change you would
  rather offer than make can still be built as a candidate (`tools/rngsafe.py`, `tools/scoreedit.py`) and left in a
  climb note for the next round.

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
