# Escapement (chirpers11): the sound bank

Clicky minimal techno: few sounds, each one designed. Add every new patch, kit, bus and recipe to the table as you make it: name, what it is, what it was built from, where it lives. New names only: released albums render through the library, so never edit a patch another record uses (`tools/libguard.py`). Song-local patches (in a song's own `patches:`) are free; say when one is worth banking.

## The click family

| sound | what it is | built from | where it lives | notes |
|---|---|---|---|---|
| `gt-kick` (chirper-zero, t1 v1) | the bass drum: short, dry, resting on G1 | the engine's `machine` kick: `decay 280ms, click 0.65, drive 0.35, punch 22, punch_time 34ms`; hp 28 | song-local, Give or Take | the kick's own body is under 60 Hz: the mix reads 8 to 10 dB short at 70-135 Hz beside the album's envelope |
| `gt-tick` (chirper-zero, t1 v1) | the grid click: one dry rim, on the off-beats | `machine` rim, `decay 35ms`, played on G5 | song-local, Give or Take | the rim follows the note: on D6 it put 10 dB on the 1.2 kHz band, on G5 it does not |
| `gt-hat` (chirper-zero, t1 v1) | the sixteenth click: 14 ms of white noise between 6 and 12.5 kHz | `white` through hp 6000, a peak at 8.5 kHz, lp 12500; amp `d 14ms, curve 5` | song-local, Give or Take | so short that it needs a fader far over a hat's to be heard (0 dB here, and it still averages 16.5 dB under the mix) |
| `gt-tock` (chirper-zero, t1 v1) | a wooden bar, struck and gone, whose pitch follows a lane | the `modal` layer on the glock's modes (after Common Measure's `cm-clave`): `bright 0.9, damp 0.25, decay 160ms`; `pitch` moved by `auto.spd` (semitones) | song-local, Give or Take | the first patch here whose tuning is a function of time |
| `gt-clap` (chirper-zero, t1 v1) | a short clap on two and four | `machine` clap, `bursts 3, decay 140ms` | song-local, Give or Take | |
| `gt-stab` (chirper-zero, t1 v1) | a dry dub chord that goes sharp and flat with its deck | the library's house chord (three saws and a square, a short filter envelope) without its own effects; `pitch` moved by `auto.spd` | song-local, Give or Take | its echo is the bus `dub` (a dotted eighth, feedback 0.45, hp 350, a hall) |

## Recipes

| recipe | how | who |
|---|---|---|
| A PART ON ANOTHER CLOCK: one function d(t) (beats ahead of the grid) places every event of a part (`t + d(t) = b`, solved by iteration) and tunes it (`12 log2(1 + d')` on a lane into `synth.pitch.mod`) | `compose/chirpers11/src/chirpers11-t1.py`: `d`, `when`, `speed`, `spd_lane`, `deck_b` | chirper-zero, t1 v1 |
