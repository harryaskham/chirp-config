# chirpers11: what the songs did to the patches they share

Written by `tools/patchbank.py census` from each song's plan as committed; do not edit by hand.
A field is what a song set on top of the patch: an override (or its own patch's `extends`), or `+TYPE.PARAM`
for an effect a track adds after the patch. AGREED: one value on more than half of the patch's tracks, in three
songs or more: that is what `patchbank.py succeed` puts in the successor `NAME-2`. The rest each song chose.

## `sub-sine`: 3 songs, 3 tracks; as it comes in tracks 5

| field | tracks | songs | values (the songs) | |
|---|---|---|---|---|
| `+pump.attack` | 3 | 3 | `2ms` in 1, 3, 5 | AGREED |
| `+pump.curve` | 3 | 3 | `0.7` in 1, 3, 5 | AGREED |
| `+pump.depth` | 3 | 3 | `-5dB` in 1, 3; `-4dB` in 5 |  |
| `+pump.on` | 3 | 3 | `kick` in 1, 3, 5 | AGREED |
| `params.grit` | 2 | 2 | `0.8` in 1, 3 |  |
| `+pump.release` | 1 | 1 | `160ms` in 5 |  |

