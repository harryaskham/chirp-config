# chirpers11: what the songs did to the patches they share

Written by `tools/patchbank.py census` from each song's plan as committed; do not edit by hand.
A field is what a song set on top of the patch: an override (or its own patch's `extends`), or `+TYPE.PARAM`
for an effect a track adds after the patch. AGREED: one value on more than half of the patch's tracks, in three
songs or more: that is what `patchbank.py succeed` puts in the successor `NAME-2`. The rest each song chose.

## `sub-sine`: 5 songs, 5 tracks; as it comes in tracks 2, 5, 6

| field | tracks | songs | values (the songs) | |
|---|---|---|---|---|
| `+pump.depth` | 5 | 5 | `-5dB` in 1, 2, 3; `-4dB` in 5, 6 | AGREED |
| `+pump.on` | 5 | 5 | `kick` in 1, 2, 3, 5, 6 | AGREED |
| `+pump.attack` | 3 | 3 | `2ms` in 1, 3, 5 | AGREED |
| `+pump.curve` | 3 | 3 | `0.7` in 1, 3, 5 | AGREED |
| `+pump.release` | 3 | 3 | `170ms` in 2, 6; `160ms` in 5 |  |
| `params.grit` | 2 | 2 | `0.8` in 1, 3 |  |

