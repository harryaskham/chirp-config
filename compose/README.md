# Composition mode: Chirpers albums

Harry, 28 Oct: alongside reproducing records, chirp climbs ORIGINAL music. An album by **Chirpers** starts as empty
tracks. Climbers claim them like any climb, compose each song from scratch with the library's patches, fx and mix
tools, then keep climbing it. There is no record to match, so the score is `tools/compscore.py` (intrinsic measures
plus Harry's ratings), and Harry's ear decides.

## The pieces

| what | where |
|---|---|
| album spec: genre, brief, palette, track slots (role, length, brief), weights | `compose/ALBUM/album.json` |
| the album's motif bank: shared riffs, cells, harmonies, who uses them | `compose/ALBUM/motifs.md` |
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
6. **Keep climbing**: each round, make the one musical change you believe improves it most, A/B on paired seeds
   (`compscore` on seeds 0/11), and keep it only if it wins AND stays itself.

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

Calibration (28 Oct): real records score 68-88 on these terms (before length), a looped bar 33. The measures are
guidance, not taste. **Variety over convergence**: never trade a song's identity for a few points; a change that
makes the songs sound alike is a loss, whatever compscore says. Invent better measures: drop a file in
`compose/measures/` with `measure(ctx) -> (score or None, detail)` and propose a weight in `album.json`.

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
