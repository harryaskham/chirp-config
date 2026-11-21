# Common Time: the film

Draft stage. The songs are still changing, so the film is **generated from the songs**: nothing
is placed by hand on a bar. Run the generator again when a song changes and its programme
follows.

## The idea

**Motion studies.** Every scene is one way a camera can hold time in a single still picture, in
the manner of Marey, Muybridge and Edgerton, and it is pointed at things that count.

- **Common time is the ruling:** a ruled wall, sixteen ticks to the bar along the foot of the
  plate, a hairline on each bar.
- **The odd riffs are what moves against it.** The engine finds each track's cell (the length
  of its repeating riff in sixteenths) from the notes, as `track.NAME.cell`, and turns a wheel
  once per cell, as `track.NAME.turn`. A riff of five is a wheel of five; with one of seven
  beside it they come round together every thirty-five sixteenths, and the picture shows it
  without saying so.
- **One spot colour a song**, silver on black. Seven of the seventeen songs are printed as
  negatives: black figures on a pale ruled wall, the spot colour an ink.

## The studies (`studies.py`)

Each is a function of track names, so it fits any song and any version of it.

| Study | The camera | What it shows |
|---|---|---|
| `wheels` | A plate flashed by each riff's notes | A wheel per riff, as big as the riff is long, with a tooth per sixteenth. The pointer prints where the notes fall, so the riff draws its own necklace. A thread lights between two wheels that come round together. |
| `finish_line` | A photo-finish slit | A lane per riff and a runner (or horse) who crosses the line once per cell. The strip holds them as far apart as the riff is long, with the notes ticked along the top of the lane. Where cycles meet they cross level and the line is drawn in the spot colour. |
| `balls` | A strobe on an open plate | A ball per riff, bouncing once per cell (a longer riff goes higher). The arcs are faint; the notes are beads on them. The floor lights when they land together. |
| `pendulums` | A plate flashed by the notes | A pendulum per riff, as long as its cell. The beam lights when all swing through the middle at once. |
| `walkers` | Marey's fixed plate | A lane per riff. Common time carries the figure across; its cell works its legs; each note is a flash. |
| `sheet` | Muybridge's row of cameras | As many panels as the riff has sixteenths, one taken each sixteenth, so the sheet stands still while the riff repeats. |
| `flight` | A plate flashed by the notes | A bird per tune, flying at the height of the note. |
| `studio` | None: the place itself | The old techniques. A daylight 3D track with a ruled black wall, PBR figures with sun shadows, their earlier poses standing behind them, a slow camera. |
| `discs` | Phenakistoscope: a ring flashed by its riff | A ring per riff with as many runners or horses round it as the riff has sixteenths, turning once per cell. Each note's flash finds every figure in the next one's place, so the ring stands still and they run on the spot. |
| `gears` | None: clockwork in real light | A steel gear per riff with a tooth for every sixteenth, all in mesh and all let go a tooth at a time, so a five turns faster than a seven. A jewel on each first tooth; they come to the top together only where the riffs do. |
| `loops` | A lamp on an open shutter, and the wire model made of its path (Gilbreth's chronocyclegraphs) | One lamp swung across by one riff, up and down by the next, in and out by a third (or by the bar): riffs of different lengths tie a knot, and it stands for as long as they repeat. The last five bars of the path are the wire; the box turns slowly. A resting riff's side of the box goes flat. Where the riffs begin together the lamp is at the centre. |
| `fence` | A picket-fence picture (the Ombro-Cinéma) | A lane per riff under its own fence. The plate holds as many pictures as the riff has sixteenths, in strips; the fence has a gap every that many and slides a strip a sixteenth. The horse of now shows bright in the gaps, and where it was at every other sixteenth of the turn shows faintly between the pales. |
| `chase` | None: the camera runs alongside | The studio with the wall streaming past. Horses or runners hold their places, each one's legs at its own cell, each surging and falling back once a turn. |

Subjects are `walker`, `runner`, `horse` (gallop), `pacer` (a horse walking) and `bird`. The
horse is built in `studies.py` from bones and poses; it needs nothing new in the engine.

What every plate shares:

- **The ruler** along the foot: sixteen ticks a bar and a cursor. That is common time.
- **The border** (`border`): lit in the spot colour where all the plate's cycles come round
  together. The same sign in every study; nothing else announces a meeting.
- **Exposure** (`finish`): halation that grows with the low end, so heavy passages burn and
  quiet ones are thin hard lines.
- **What a plate keeps:** its last twenty notes or so, by count and not by the clock (`each`
  on the `expose` filter). A slow riff fills its plate as a fast one does, and a riff that
  rests leaves its plate standing rather than empty.
- **The print** (`master`): the plate's number and title for the first bars while the first
  plate develops under it, a small `PL. NN  FIG. N` legend, grain, dark corners. Seven songs
  are printed as negatives (`WHITE` in `ctgen.py`); those come up from black and go back to
  it by a veil in the master, because a programme's own fade is taken before the print is
  turned over.

## Drawing a draft

`~/.local/state/chirp-video/cv/draft.py TAG BIN 1280x720 30` (run it in a guarded unit) draws
every song over its WAV, long songs in parts cut at scene starts, and joins the album;
`draft_and_post.sh TAG BIN` also puts the result on the review page. About an hour at 720p.
Do not regenerate `film/` while a draft is drawing: parts read the programme when they start.

## The generator (`ctgen.py`)

```
python3 ctgen.py            # every song: writes ../film/chirpers10-tN.yaml
python3 ctgen.py 3 7        # only those
python3 ctgen.py --plan 3   # what it found in the song and what it chose
```

For each song it reads the notes (`tools/songmap.py`) and works out:

1. What each track is (riff, bass, drum, tune, voice), from its notes.
2. Each track's cell, bar by bar (the same reading as the engine's).
3. Where the song changes: who plays, and which cells. Scenes change there, and at least every
   26 seconds or so.
4. Which tracks carry a distinct cell in each stretch (riffs first, one wheel per cell), and
   which tune sings over them.
5. Which study suits the stretch, taking the one used least so far in the song.

`try.py STUDY OUT.yaml [key=value …] TRACK…` writes one study as a programme, to look at.

## What it needs

- The `chirp-video` branch of chirp (cells; the `expose` (with `each`), `slit`, `panels` and
  `fence` filters; `mask: none`). No
  released binary draws these programmes yet, which is why they are written to `film/` and not
  to `vis/`. Move them when the branch lands.
- Check one with `chirp --json vis check ../compose/chirpers10/film/chirpers10-tN.yaml -f
  chirpers10-tN.yaml` from `songs/`.

## For the composers

The picture is clearest where a riff repeats exactly for several bars, and where two parts
with different cells play together. Nothing needs marking in the song.
