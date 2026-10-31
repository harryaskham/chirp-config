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
   something.

`tools/chirpers.py status ALBUM` shows the album; `chirpers.py refresh ALBUM` re-renders every composed song and
re-saves features (run it after several songs change).

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
| flow | .03 | level/spectrum continuity at the joins with the neighbouring tracks (the songs bleed) |

Calibration (28 Oct): real records score 68-88 on these terms (before length), a looped bar 33. **Above ~95 every
intrinsic term passes**: from there compscore cannot tell you what to improve. Climb by musical judgment (what would
make this track more itself, more surprising, better at its job on the album), by peers' notes and Harry's ratings,
and by the album as a whole (the joins, the motif bank, the empty slots). Seed-to-seed spread is ~0.5-1 point; treat
smaller gains as noise. The measures are
guidance, not taste. **Variety over convergence**: never trade a song's identity for a few points; a change that
makes the songs sound alike is a loss, whatever compscore says. Invent better measures: drop a file in
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
