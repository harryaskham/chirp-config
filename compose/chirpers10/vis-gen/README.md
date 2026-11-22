# Common Time: the film

There are two films here. The **second** (`wild.py`, `wildgen.py`) is the current one; the
first (motion studies: `studies.py`, `ctgen.py`, described from "The idea" on) survives in it
as one family of pictures among many.

## The second film: many small machines (`wild.py`, `wildgen.py`)

The first film was one idea held for 78 minutes. This one never shows the same picture twice:
about 940 scenes on the album, every one different.

**What is drawn**

- **Idioms** (`wild.py`, the `@idiom` functions: 181 so far). Each is a small machine, place,
  game or diagram built from the notes themselves, and each keeps one rule: *what the music
  counts, the picture counts*. A note is a thing (a domino, a lantern, a lit window, a letter
  typed, a block dropped into a well); a riff's cell is a width or a number of things (bells
  in a ring of changes, oars on a galley, fingers on a hand, pictures on a reel); a turn of
  the riff is a turn of something. So the odd lengths are seen sliding against the bar
  without being announced.
- **Guises** (`@treat`, 55): an idiom is seen plain once, and after that through something it
  has not been seen through. Prints (halftone, newsprint, engraving, one-bit, type, a line
  drawing, a blueprint, relief, two-ink posters, solarised); cameras that hold time (a
  slit-scan with a strip a sixteenth, stop motion on the riff's notes, a sheet of as many
  frames as the riff is long); the picture moved (a kaleidoscope with as many mirrors as the
  riff has sixteenths, a wall of as many copies, wrapped round a circle, wound up, torn into
  sixteen bands on the riff's notes, a stone dropped into it on every note, inside itself
  without end, round a ball, on a folding screen with a leaf for each sixteenth); what the
  picture is made of (combed into streaks, blown, set in leaded glass, overgrown, smoking,
  running, woven of its own strips, seen as heat, a worn tape, its colours arriving one
  after another); made by hand (cut from sheets of coloured paper with the light going
  round, drawn as a range of ridges that the notes heave, knitted, cross-stitched, built of
  studded bricks, threaded as beads, a puzzle put together a piece a sixteenth and taken
  apart again).
- **Combinations** (`@combo`, 21; also a round window that circles, a nest of frames, an
  iris thrown open on the riff's turn, a card dealt over the picture; and three in which
  one picture works on the other: seen through it as through glass, shown only through its
  lights, or with its bodies cut out in black). Where three riffs run and the band is full,
  three pictures (`@trio`): a colour separation with one picture in each of red, green and
  blue, thirds, bands that change places, one inside another inside a third.
  Two pictures: two idioms share the frame, each reading its own part:
  double exposure, intercut on the riff's turns, a round window, a diptych, a triptych,
  difference, lighten, a corner that changes places half way, one sweeping the other off;
  and the frame cut into as many strips (or bands, squares, cake slices, rings) as the riff
  has sixteenths, the two pictures changing places each time the riff comes round. More of
  these where the music is fuller.
- **Chains**: a picture is joined by a second, then the second stands alone or is joined by
  a third, so through a full passage something always carries over the cut.
- **Titles** (`master`): each song's name comes on in its own way (through a slit, turning
  over like a departures board, a word at a time as big as the frame, spaced along the foot,
  down the edge, round a ring …).

**How it follows the music** (`wildgen.py`)

| What the music does | What the film does |
|---|---|
| A joint: who plays changes, or a riff's length changes | A cut (`cut`), to the sixteenth. Between joints a scene lasts whole rounds of its own riffs where they come round quickly enough, so cuts fall where riffs meet and not on the bar. |
| A full passage / a thin one | Scenes of four to eight seconds / six to eleven; loud idioms / calm ones (`mood`); more pictures two at a time. |
| A long round comes to its end | The scene ends there and the picture burns out into it. |
| The great round ends (every length of riff the song keeps to comes round at once, on a bar line, once in the song and past its middle: bar 385 of the first song) | A hand for each length comes up over the pictures of the bars before, each going round once in its own turn; they reach the top together only then. The picture burns out to white, and out of the white comes the song's first picture, exactly as it stood at the first bar. It is the one picture the film shows twice. |
| A riff is played differently for one turn among many alike | For that turn the picture is its negative. |
| The band is building, or thinning | The camera goes in (push, punch, a step closer each turn), or draws back; level passages get a move across, a lean, a rock with the riff. |
| Two riffs of the scene come round together | The picture catches the light for an instant. |
| The drums break into a fill (`fills`) | That bar goes by in flashes, a beat each (`flurries`), each a different picture: mostly ones the song has shown, in another guise. |
| The band comes in after a thin bar (`dynamics`) | A cut on it; the new picture is struck with light and comes forward. |
| The band stops for a bar | That bar stands alone, drained and dim. |
| A riff comes back | Its cast of colour comes back (each length of riff has a hue of its own in a song), and now and then the picture it had, changed. |
| The band gains a part, or loses one, and nothing else changes | The picture stays and gains or loses that part (`more`, `less`): a second wheel, a third row. The dealer looks a scene ahead for a picture that can. |
| A long round (two or three riffs running until they come round together) | The frame is ruled round its edge a sixteenth at a time for as long as the round lasts, across every cut and flash, with a mark wherever each riff begins a turn (`ruled`). The marks fall together only at the corner where the riffs meet. |
| Two parts play one riff, one of them ahead of the other (`slips`, `stereo`: a left and a right guitar; found from the notes, to a quarter of a sixteenth) | A canon: the picture is drawn once for each part and the two are joined (`JOINS`: down the middle, in strips, bands, rings, wedges, a board). In step that is one whole picture; out of step it breaks along the joins by exactly as much as the parts are apart, and further as they slip. A song's own canon is shown whole once while the parts are still together and comes back each time they are a sixteenth further apart (Odd Sympathy: at 1, 2, 3, 4, 5 and 8, where the halves fit; Take Up the Slack: as the slack is taken up). |
| Two parts answer one another (`talkers`: each plays where the other rests, and they change over) | A picture each, side by side, and the line between them is pushed across the frame by whichever is playing for as long as it plays (`tug`): the frame keeps the account of who has had how much of the time. |
| A part is given one more note to the beat, time after time (`dealing`: two to the beat, then three, then four) | The dice come back at each new number and show it: a die for each beat of the bar, a pip for each note, set out as on a real die. At seven there is no such face. |
| Few notes, or the song ringing out | Pictures made of notes (`FED`) are kept away. |
| The riff comes round part way through a scene | A treatment arrives or leaves there; the camera cuts in or out there; 3D scenes change camera there. |
| The song ends | On the picture it began with, changed. |

Each song has a house (`HOUSE`): the guises and ways of sharing the frame it leans to, so
the songs differ from one another as well as from bar to bar; and five featured idioms
(`FEATURE`). Where the music is full a picture may wear two guises at once (`STACK`: one
that moves it, one that changes what it is made of, one that works on it in time).

Some songs are printed on a stock of their own (`STOCK`: grainy and pale for In the Time
Of, out of register for Close Enough).

Nothing is dealt twice (`Deal`, album-wide): never the same idiom in the same guise, never
the same family twice running, never the same idiom within twelve scenes. Each song has its
own colours (`PALS`) and some idioms built on what it is about, taken sideways (`FEATURE`):
bells rung in changes for Plain Hunt, Huygens's two clocks for Odd Sympathy, a dish of
cells for Carrying Capacity, squares laid round one another and a wall whose bricks are the
waits between notes for Extreme and Mean, the oblong cut down to its common measure for
Common Measure, the walks of the first sixteen numbers down to one for So Far, striped
poles that climb for ever for False Summit, wheels seen only by the flash of another
riff's notes for Slow Enough to Count.

What a picture is like decides what may be done to it (sets at the end of `wild.py`,
several of them measured on a proof with `wlight.py`): thin pictures (`THIN`) do not take
guises that leave less of a picture than there was (`SHRINKS`); hair-line pictures (`BOLD`)
are thickened and take only guises that add (`FILLS`); pictures made of notes (`FED`) and
pictures that take time to form (`SLOW`) keep out of flashes; `cutout`, `stencil` and
`glass` need something to work on and something to work with (`FULL`, `BROAD`, `fits`);
flames, bricks and paintings keep their own colours (`TRUE`).

Commands (from this directory; `CHIRP` reads the cells and may be any recent binary):

    wildgen.py --plan --tally          what would be dealt, and the totals
    wildgen.py --out=/tmp/cv/ct/genw   write all seventeen programmes there
    wtry.py 1 190 194 OUT.jpg NAME…    draw idioms over bars 190-194 of song 1, a strip each
                                       (NAME/TREATMENT and A+B/COMBINATION work too)

Programmes are written as generated; do not edit them. They need the engine of the
`chirp-video` branch at 633f6e09 or later (`notes:` and `note.*`, `timeslice`, `step`,
`halftone`, `outline`, `bold`, `remap`, the warps, `droste`, `orb`, `sort`, `wind`, `glass`,
`grow`, `flow`, `weave`, `pleat`, `lag`, `papercut`, `terrain`, `stitch`, `pieces`, `pick:`,
`repeat:`, an actor's `cut:` and `as:`, the new transitions),
which is not yet in a pinned binary, so they are not in `vis/`.

## The first film: motion studies

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
| `studio`, `chase` (`daylight`) | None: the place itself | The old techniques. A daylight 3D track: a black wall ruled in threads, a chalked floor, plaster figures with sun shadows and the poses they have just left. The camera goes alongside at common time's pace, so a chalk line and a thread pass each beat while the feet come down at each riff's own length. Cut between three views (side on, the feet, from ahead and low) when the first riff comes round, not on the bar. `studio` is at a walk, `chase` at a run. |
| `knot` (`loops` with `tie`) | The same lamp, the shutter open for one whole round | Where the music runs a long cycle right round, the scene is that round exactly and the wire is all of the lamp's path since it began: the knot is tied before your eyes, a thread at first and a close weave by the end, and the last strand closes it as the round ends. Three riffs weave a block; two weave a sheet. |
| `discs` | Phenakistoscope: a ring flashed by its riff | A ring per riff with as many runners or horses round it as the riff has sixteenths, turning once per cell. Each note's flash finds every figure in the next one's place, so the ring stands still and they run on the spot. |
| `gears` | None: clockwork in real light | A steel gear per riff with a tooth for every sixteenth, all in mesh and all let go a tooth at a time, so a five turns faster than a seven. A jewel on each first tooth; they come to the top together only where the riffs do. |
| `loops` | A lamp on an open shutter, and the wire model made of its path (Gilbreth's chronocyclegraphs) | One lamp swung across by one riff, up and down by the next, in and out by a third (or by the bar): riffs of different lengths tie a knot, and it stands for as long as they repeat. The last five bars of the path are the wire; the box turns slowly. A resting riff's side of the box goes flat. Where the riffs begin together the lamp is at the centre. |
| `fence` | A picket-fence picture (the Ombro-Cinéma) | A lane per riff under its own fence. The plate holds as many pictures as the riff has sixteenths, in strips; the fence has a gap every that many and slides a strip a sixteenth. The horse of now shows bright in the gaps, and where it was at every other sixteenth of the turn shows faintly between the pales. |

Subjects are `walker`, `runner`, `horse` (gallop), `pacer` (a horse walking) and `bird`. The
horse is built in `studies.py` from bones and poses; it needs nothing new in the engine.

What every plate shares:

- **The ruler** along the foot: sixteen ticks a bar and a cursor. That is common time.
- **The border** (`border`): lit in the spot colour where all the plate's cycles come round
  together. The same sign in every study; nothing else announces a meeting.
- **The wait** (`waited`): if the cycles had been long apart, the plate is overexposed for a
  moment as well, the more the longer they had been apart. A meeting that comes every bar or
  two only lights the border. The look keeps the time itself; nothing is told it.
- **Exposure** (`finish`): halation that grows with the low end, so heavy passages burn and
  quiet ones are thin hard lines.
- **The cutting keeps the riff's time** (`shot_list`, `cutting`, `rostrum`): inside a scene
  the film cuts from the whole plate to its details and back, as a film is made from
  photographs on a rostrum: a wheel, a ring, a lane, the line of a photo-finish. A cut comes
  where the scene's first riff begins a turn, each time it has come round as often as takes
  about four and a half seconds (at 126 bpm a five every eight turns, an eleven every three),
  so the cuts fall across the bar lines as the riff does. The plate itself is not touched:
  the camera is a filter over the finished picture. The knot and the gears are real bodies
  and have real second cameras (the knot from its side and close; the gears where two wheels
  mesh), cut the same way, as the daylight track is.
  - The shots are worked out here, from the engine's reading of where the riff's turns
    begin (`Track.anchor`), and written into the look against the song's own clock: a scene
    is cut the same however it is drawn. `python3 ctgen.py --cuts [--plan] [N…]` prints them
    (view:seconds) with the shortest and the share of time away from the whole plate.
  - A scene opens on its whole plate (about three seconds, until the riff next begins a
    turn), goes through its details in order, comes back to the whole, and round; it closes
    on the whole plate, from the last cut that leaves two and a half seconds. No shot is
    shorter than that.
  - One thing is not known beforehand: a meeting of the plate's cycles that was long in
    coming (seven seconds apart or more). It brings the whole plate back, burning, until
    the next cut; meetings that come round every bar or two do not cut.
  - `CT_SHOW_CUTS=1 python3 ctgen.py --out=DIR` writes programmes whose black is lifted a
    step per view, so a tool can read every frame's view off a clip (never for a film).
  - The legend names what is on screen: `PL. 06  FIG. 2` in one corner, and `DET. A`, `B`,
    … in the other while a detail is (only where the shots are certain).
- **A photo-finish runner fits its strip:** as tall as its lane lets it be, and no longer
  than the strip gives it between one crossing and the next (a short riff's runners come
  nose to tail, not through one another). A lone lane is no taller than its runners need
  and lies across the middle. The details are centred on the runners.
- **A plate's subject is there from the start:** a part gets a body only if it plays within
  about the scene's first four seconds (three bars of a quick song, one of a slow one).
- **A camera already running** (`lead` on a scene; `LEAD` in `ctgen.py`): a plate, a strip, a
  sheet or a fence is started a bar or two before its cut and drawn unseen, so the cut lands
  on a picture already made. Only a song's first plate develops in view, under its title.
- **A body keeps its riff's length** (`HELD`): where the notes give no cell for a while (a
  rest, a bar that varies), the body keeps the scene's own and stands where it was. A plate
  is not emptied by a riff that pauses.
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
Run nothing else heavy beside it. `reel.py TAG BIN 3840x2160 60 N` (env `FROM`, `TO` in bars)
draws a sampler at delivery size.

## The generator (`ctgen.py`)

```
python3 ctgen.py            # every song: writes ../film/chirpers10-tN.yaml
python3 ctgen.py 3 7        # only those
python3 ctgen.py --plan 3   # what it found in the song and what it chose
python3 ctgen.py --reel=1:188:236 --out=DIR   # a sampler: bars 188 to 236 of song 1, a study every four bars
```

For each song it reads the notes (`tools/songmap.py`) and works out:

1. What each track is (riff, bass, drum, tune, voice), from its notes.
2. Each track's cell, bar by bar. It asks the engine (`chirp --json vis cells -f SONG`, from
   `$CHIRP` or the chirp-video build), which reads the notes as played; without such a
   binary it reads the written notes the same way, and `--plan` says so.
3. Where the music runs a long cycle right round (`find_cycles`): two or three parts keeping
   cells of different lengths together for as long as those lengths take to come round (their
   least common multiple), where that is a wait of nine seconds to a minute. Such a round is
   one scene, to the sixteenth: a plate lasts as long as its cycle. The longest are tied as
   knots (up to a fifth of the song, never two running); the rest get the other studies
   (`name*` in a plan). A scene can therefore begin a sixteenth off the bar line.
4. Where else the song changes: who plays, and which cells. Scenes change there, and at least
   every 26 seconds or so.
5. Which tracks carry a distinct cell in each stretch (riffs first, one wheel per cell), and
   which tune sings over them. A part counts only if it plays a note a bar and keeps its cell
   through about half the stretch.
6. Which study suits the stretch, taking the one used least so far in the song. A song opens
   on lines and bodies on black, not on daylight, steel or a strip that starts empty; a train
   of gears is dealt only to riffs within four times of each other's length.

`try.py STUDY OUT.yaml [key=value …] TRACK…` writes one study as a programme, to look at.

## What it needs

- The `chirp-video` branch of chirp (cells; the `expose` (with `each`), `slit`, `panels` and
  `fence` filters; `mask: none`; a scene's `lead`; long trails). No
  released binary draws these programmes yet, which is why they are written to `film/` and not
  to `vis/`. Move them when the branch lands.
- Check one with `chirp --json vis check ../compose/chirpers10/film/chirpers10-tN.yaml -f
  chirpers10-tN.yaml` from `songs/`.

## For the composers

The picture is clearest where a riff repeats exactly for several bars, and where two parts
with different cells play together. Nothing needs marking in the song.

Where parts of different lengths play together for one whole round (five, seven and eleven
for 385 sixteenths, say), the film gives that round one plate and ties its knot. A round cut
short by a bar, or a part that drops out near its end, loses that.
