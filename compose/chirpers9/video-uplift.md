# Accretion film: uplift review and plan

chirp-video, 10 Nov 2026, at Harry's request ("take a holistic look ... improve it dramatically").
Status: DIRECTED by Harry, 10 Nov 03:20 (below). Work started.

## Harry's direction, 10 Nov

- **The model:** the picture is co-built with the music, as a bar visualiser is, except that the
  scenes are real scenes driven by the real musical signal. Not a separate 3D system synced
  afterwards.
- **Two speeds, one programme:** realtime at low resolution while the music plays; the same
  programme read out at full 4K later, below realtime.
- **Style:** chirp-video's call (the disk's look included).
- **GPU:** no; it is doing ML work. Section F is dropped.
- **Song information:** all in the songs and their sources; work it out, do not ask the composers.
- **Guards:** mostly arbitrary; just work (units keep their `guarded-` names so eco's guard can
  still pause them; the 4-thread cap is not a rule).

### How Standby Amber did it (the model to return to)

- Each song had a programme named after it. The live panes (`chirp vis watch`, `v` in
  `chirp watch`) draw the programme named like the playing song, its scenes placed on the live
  timeline's bars; `chirp video --album` drew the same programmes for the film, the engine
  rendering each song's audio and drawing every frame from the same plan.
- 12 programmes, 77 scenes, every one placed in bars. 27 envelopes fired by named tracks, 17
  direct track readings, 11 layers drawing the notes themselves, and the composers' hidden states
  read through `song.wear`, `song.drift`, `song.height`, `song.agree`.
- Each look was the system inside its song (a melody sorting itself drawn sorting, an automaton,
  a swarm locking), in flat layers cheap enough to play live.

### Where Accretion stands against that (measured 10 Nov, 640x360)

| scene | frames a second, 4 threads | 12 threads |
|---|---|---|
| t1 | 31 | 31 |
| t2 dawn flight | 4.6 | 6.1 |
| t2 road | 11.6 | 15.1 |
| t3 street | 9.6 | 13.6 |
| t3 plaza | 7.0 | 11.1 |
| t4 act I | 5.6 | 7.7 |
| t4 act II | 14.3 | 14.6 |
| t5 | 8.5 | 7.8 |
| t6 act I | 7.7 | 13.5 |
| t6 act II | 10.7 | 14.6 |
| t7 | 28 | 36 |
| t8 act I | 31 | 39 |

- Only the three space scenes play live, even at 360p.
- The cost is in geometry, not pixels: 720p is about half the speed of 360p, not a quarter, and
  three times the threads gains little. Static land, trees and seas are rebuilt every frame, on
  one thread.
- Lanes (`lane.NAME`) reach offline video only; the live pane and the browser get tracks, notes,
  sections and song variables but no lanes.

### Revised order

1. **Play live:** every scene at 24 frames a second or more at 640x360. Keep unchanged geometry
   between frames, work vertices on all threads, and scale detail, counts and shadow maps with the
   output size.
2. **Rebuild each programme on the song,** Standby Amber's way: scenes in bars, bodies on tracks
   and notes, the story on lanes and song variables. t1 first.
3. **Engine sources for that:** lanes in the live pane and the browser; note-bound instances;
   pan; time to the next note; sung vowels.
4. **Image quality that costs little a pixel:** linear light and a grade; the disk's look; the
   album's colour arc.
5. **Dropped or parked:** the GPU path; baked simulations; many samples a pixel as a requirement
   (optional on the 4K read-out only).

The findings and the longer list below stand, read in that order.

## What the review found

Measured on the eight committed programmes (`vis/chirpers9-tN.yaml`) against snapshot 20261109-1701.

### 1. The picture follows the loudness, not the composition

| what the programmes read | uses, all 8 tracks |
|---|---|
| the clock in seconds (`time.t`) | 168 |
| overall loudness (`audio.level`, `audio.low`) | 39 |
| lifts and onsets of the whole mix (`audio.lift`, `audio.onset`) | 14 |
| tempo (`time.bpm`) | 10 |
| a bar trigger | 5 |
| any single track (`track.NAME.*`) | 0 |
| any note (pitch, velocity, length) | 0 |
| any composer automation lane (`lane.NAME`) | 0 |
| any section | 0 |
| any sung word | 0 |

What the songs carry, and the engine can already read (checked: `lane.sep`, `lane.lens`,
`track.tide.level` and hyphenated names such as `track.seed-d.hit` all resolve on the current pin):

- 27 to 119 named tracks a song, every note with pitch, velocity and length, known ahead of time.
- The composers' own story controls as automation lanes:
  - t1 `gather_ring`, `gather_turn`, `open`, `close`
  - t2 `grav`, `lens`, `lock`, `spin`, `glitch`
  - t3 `lock`, `sync`, `field`, `still`, `eyelift`, `fall`, `glitch`, `grit` (32 lanes)
  - t5 `heat`, `peri_near`, `peri_spin`, `tide`
  - t6 `sep` (the two sides parting), `stop` (the tape stop), `lens`, `shut`
  - t7 `coll`, `crest`, `plunge`, `whirl`, `float`, `gasp`, `hole`, `laps` (28 lanes)
- 29 to 489 sung notes a track, each with its phonemes and timing.
- Pans: t1's five seed notes are five tracks at pans -0.7, +0.55, -0.3, +0.75, +0.1, on cycles of
  9, 7, 8, 6 and 5 beats. That is the whole story of the track, and the picture shows none of it.

Example of the cost: t3's lock, the album's first resolution, is drawn as
`smooth(200, 232, time.t)`, a guess in seconds, while the song states it exactly in `lane.lock`
and `lane.sync`. This is also why the programmes were waiting for a freeze.

The album is built from eight elements (E1 to E8, `motifs.md`), each with its own cycle length
(5 beats, 7 sixteenths, 7 beats, 20 beats, 3 beats, 8 beats, 11 sixteenths), drifting out of phase
and locking at the crests. Nothing in the film shows an element, a cycle or a lock.

### 2. The film barely edits

- 17 scenes in 38 minutes: one new picture every 2 min 15 s on average. Only t1 cuts between
  cameras.
- The music is held to "no stretch of about 30 s where nothing changes; every 8 to 16 bars
  something moves" (Harry, 6 Nov). The picture is not held to it.
- Camera moves are slow sine drifts unrelated to phrases.

### 3. The image is single-sample, lit in display colour, flat-surfaced, in empty space

- **Colour:** colours go in as `hex / 255` and out as `value * 255`, with no transfer curve
  anywhere, so all lighting, blending and bloom are computed on display-encoded values. That
  gives harsh falloff, muddy blends and highlights that clip to flat colour: a large part of the
  "90s" read.
- **Samples:** one sample a pixel a frame (`aa` is a blur after the fact). Glints shimmer, thin
  shapes stair-step, shadows have one hardness, depth of field is a filter.
- **Surfaces:** one flat colour each. Detail exists only as vertex displacement.
- **Space:** flat black with dot stars. The disk, the album's central image, is rings of
  coloured dots; the art brief asks for "a thin, intensely bright ring of warm white-gold and
  orange light".
- **People:** read as mannequins when lit from the front at medium distance.
- **Palette:** each track chose its own; there is no colour arc across the album.

### 4. The renderer leaves the machine idle

- Rendering runs on 4 of 24 CPU threads at idle priority (the guard that protects the groove).
- pocket4 has a Radeon RX 7900 XTX (24 GB, 19 GB in use by something else, 1 % busy) and an idle
  integrated Radeon 890M. Vulkan is installed. The engine uses neither.

## What I would do, in order

### A. Bind the picture to the score

Largest gain, least new engine, and it removes the freeze dependency.

1. **Engine (small):**
   - Note-bound instances: a layer with `per: track.NAME` gets one instance a note, with
     `note.key`, `note.vel`, `note.len`, `note.age`, `note.until` (seconds before it sounds, for
     anticipation) and `note.i` (its place in the phrase).
   - `track.NAME.pan`, so a voice stands where it is heard.
   - `track.NAME.next`: time to the track's next note, so cameras cut on the downbeat and bodies
     wind up before a hit instead of reacting after it.
   - Sung syllables: `track.NAME.open` (how open the vowel is) for mouths, and the words for
     captions.
   - Harmony: the root and colour of the chord sounding, so the light changes with the key (t6's
     crest lifts a whole tone into E).
2. **Elements as recurring actors:** each of E1 to E8 gets one visual identity, a body, a colour
   temperature and a way of moving, that appears whenever that element sounds, in every track.
   Their cycles become orbits and gaits, so phase, polymeter and the locks are seen.
3. **Lanes drive the story:** replace every second-based guess with the lane or track that states
   it (`lane.lock`, `lane.sep`, `lane.heat`, `lane.grav`, `lane.stop` ...).
4. **Needs from composers (not yet asked):** `sections:` markers in each song, and a map of which
   tracks carry which element. I can draft the map from track names and `motifs.md` for them to
   correct.

### B. Edit it like a film

- A shot list a track: 15 to 25 shots, cut on bar lines, sizes varied (wide, medium, close,
  insert), moves tied to phrases and lanes.
- Apply the music's own rule: no 30 s without a change of picture.
- No engine work beyond A; `shot:` and bar-timed keys exist.

### C. The image pipeline

1. **Linear light**, opt-in per look: colours decoded on the way in, a filmic curve and a grade on
   the way out (lift, gamma, gain, split tone, halation).
2. **A colour script for the album:** cold blue dust in t1 to white-gold in t8, the disk heating as
   it falls in; element colours as accents.
3. **Accumulated samples:** `--shutter N` already renders N sub-frames a frame. Jitter the camera
   by a fraction of a pixel, the sun and the lens in each, and the same sub-frames give true
   anti-aliasing, motion blur, soft shadows and real depth of field together. Cost: N times.

### D. The disk and space

1. **A luminous disk:** gas marched through the hole's bent light paths, sheared by its own
   rotation, hot inside and beamed brighter on the approaching side, with the debris specks over
   it. One band an element, its brightness and turbulence from that element's tracks. Matches the
   art brief; changes a look I built earlier, so it needs Harry's eye on a prototype.
2. **A baked sky:** nebula, dust lanes and a galaxy band computed once a scene into a wrap-round
   picture, then nearly free a frame. The same picture lights and is reflected by every body.

### E. Surfaces and nature

- Per-pixel bump and colour variation from expressions (rock, sand ripples, bark, cloth).
- A real ocean: summed trochoidal waves with foam where they fold (fixes t6's facets and t4's
  broken glass).
- Baked simulations, run once from the scene start so stills, seeks and split renders still
  agree: reaction-diffusion for t1's crust (it is literally nucleation), smoke for t4's fire.
- People: silhouette, rim light and distance by direction; stylised, not photographic, as the art
  brief says. Mouths from the sung syllables in the few close shots.

### F. A GPU path (decision, not started)

- Highest ceiling: D and E become cheap, and 4K with many samples becomes hours, not days.
- Cost and risk: a new dependency and a second renderer for offline video only; unknown
  contention with whatever holds 19 GB on the 7900 XTX.
- Proposal: decide after the first slice shows how far the CPU gets; then at most a one-day spike
  on the idle integrated GPU.

## How I would run it

1. **One track first, end to end** (t1: its five seed voices, their cycles and the crest where
   they align), through A, B and C. Post before and after. Harry judges the bar.
2. Then roll A to C across t2 to t8, D for the seams, t7 and t8, and E where a track needs it.
3. Every engine change stays opt-in and goes through eco's gate as before.

## Decisions for Harry

| decision | options |
|---|---|
| the disk's look | keep the dot rings; or the luminous gas disk with specks (prototype first) |
| render budget (estimates from earlier timings) | 4K at one sample (about 12 h now); or 1080p/1440p at 4 samples (sharper motion, softer light, about 16 to 30 h on 4 threads) |
| threads for the final render | stay at 4 idle threads; or more while the groove is paused (eco's guard) |
| GPU | leave it; or a time-boxed spike after the t1 slice |
| composers' time | ask for section markers and the element map now; or after the t1 slice |
