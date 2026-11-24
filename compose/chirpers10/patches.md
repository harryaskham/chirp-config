# chirpers10: what the songs did to the patches they share

Written by `tools/patchbank.py census` from each song's plan as committed; do not edit by hand.
A field is what a song set on top of the patch: an override (or its own patch's `extends`), or `+TYPE.PARAM`
for an effect a track adds after the patch. AGREED: one value on more than half of the patch's tracks, in three
songs or more: that is what `patchbank.py succeed` puts in the successor `NAME-2`. The rest each song chose.

## `ct-bass`: 17 songs, 22 tracks; as it comes in tracks 3, 4, 5, 6, 8, 11, 14

| field | tracks | songs | values (the songs) | |
|---|---|---|---|---|
| `synth.layers.1.level` | 10 | 10 | `-12dB` in 5, 11; `-20dB` in 8, 15; `-18dB` in 1; `-24dB` in 2; `-14dB` in 9; `-17dB` in 12; `-13dB` in 13; `{value:-60dB,mod:[{src:env.under,amount:51}]}` in 16 |  |
| `fx.2.bands.3.cutoff` | 9 | 9 | `1150` in 2, 5, 8, 9, 10, 11, 12, 13, 15 |  |
| `fx.2.bands.3.q` | 9 | 9 | `1.2` in 2, 5, 8, 9, 11, 12, 15; `1.6` in 10, 13 |  |
| `fx.2.bands.3.gain` | 9 | 9 | `9dB` in 2, 5, 8, 11; `6dB` in 9, 15; `8dB` in 10; `10dB` in 12; `11dB` in 13 |  |
| `fx.2.bands.1.gain` | 8 | 8 | `6dB` in 2, 5, 8, 9, 12, 15; `4dB` in 7; `11dB` in 11 |  |
| `fx.2.bands.0.gain` | 7 | 7 | `12dB` in 2, 5, 8, 9, 12, 15; `9dB` in 11 |  |
| `fx.2.bands.2.cutoff` | 7 | 7 | `540` in 2, 5, 8, 9, 12, 15; `600` in 10 |  |
| `fx.2.bands.2.q` | 7 | 7 | `0.7` in 2, 5, 8, 9, 12, 15; `1` in 10 |  |
| `fx.2.bands.2.gain` | 7 | 7 | `-6dB` in 2, 5, 9, 10, 12, 15; `-3dB` in 8 |  |
| `+compressor.attack` | 2 | 2 | `12ms` in 13, 17 |  |
| `+compressor.makeup` | 2 | 2 | `2.5dB` in 13, 17 |  |
| `+compressor.ratio` | 2 | 2 | `8.0` in 13, 17 |  |
| `+compressor.threshold` | 2 | 2 | `-26dB` in 13, 17 |  |
| `synth.pitch.mod.1.amount` | 2 | 2 | `0` in 16, 17 |  |
| `synth.pitch.mod.2.src` | 1 | 1 | `expr.bend` in 7 |  |
| `synth.pitch.mod.2.amount` | 1 | 1 | `1` in 7 |  |
| `fx.2.bands.5.cutoff` | 1 | 1 | `6000` in 12 |  |
| `synth.env.under.a` | 1 | 1 | `45ms` in 16 |  |
| `synth.env.under.s` | 1 | 1 | `1` in 16 |  |

## `ct-kit`: 17 songs, 111 tracks; as it comes in tracks 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16

| field | tracks | songs | values (the songs) | |
|---|---|---|---|---|
| `kit.s.patch.synth.filters.1.gain` | 17 | 12 | `-2dB` in 11; `-3dB` in 9, 13, 17; `2dB` in 2, 15; `-2.5dB` in 1; `3.5dB` in 3; `0.5dB` in 7; `-1.5dB` in 8; `-5dB` in 10; and 1 more values |  |
| `kit.s.patch.synth.layers.0.slap` | 13 | 8 | `1.6` in 11, 12; `0.5` in 1, 8; `0.6` in 2, 15; `0.8` in 9, 13 |  |
| `kit.s.patch.synth.layers.0.contact` | 13 | 8 | `0.35` in 11, 12; `0.45` in 1, 7, 8, 9; `0.9` in 10, 17 |  |
| `kit.s.patch.synth.layers.0.wires` | 13 | 8 | `0.95` in 11, 12, 13; `1.1` in 3; `0.9` in 7; `1.0` in 15; `1` in 16; `0.7` in 17 |  |
| `kit.t1.patch.synth.layers.0.decay` | 11 | 5 | `0.6s` in 16; `0.55s` in 14, 15, 17; `0.35s` in 8 |  |
| `kit.t1.patch.synth.amp.d` | 11 | 5 | `0.8s` in 16; `0.7s` in 14, 15, 17; `0.4s` in 8 |  |
| `kit.t2.patch.synth.layers.0.decay` | 11 | 5 | `0.6s` in 16; `0.55s` in 14, 15, 17; `0.35s` in 8 |  |
| `kit.t2.patch.synth.amp.d` | 11 | 5 | `0.8s` in 16; `0.7s` in 14, 15, 17; `0.4s` in 8 |  |
| `kit.s.patch.synth.layers.0.wire_tone` | 10 | 5 | `5000` in 10, 11, 12, 16, 17 |  |
| `kit.s.pitch` | 9 | 9 | `G3` in 1, 2, 8, 9, 15; `Ab3` in 7, 13; `m51.85` in 16; `m56.863` in 17 |  |
| `kit.s.patch.synth.layers.0.mode_count` | 7 | 7 | `10` in 1, 2, 8, 9, 13, 15, 16 |  |
| `kit.s.patch.synth.layers.0.damp` | 7 | 7 | `0.9` in 1, 7, 8, 9; `0.6` in 2, 15; `0.15` in 13 |  |
| `kit.s.patch.synth.amp.d` | 7 | 7 | `110ms` in 7, 8, 9, 15; `125ms` in 1; `200ms` in 10; `260ms` in 13 |  |
| `kit.ft.patch.synth.layers.0.decay` | 7 | 2 | `0.6s` in 16; `0.35s` in 8 |  |
| `kit.ft.patch.synth.amp.d` | 7 | 2 | `0.8s` in 16; `0.4s` in 8 |  |
| `kit.t1.patch.synth.layers.0.tilt` | 6 | 5 | `-6` in 1, 8, 14, 15, 17 |  |
| `kit.t1.patch.synth.filters.1.gain` | 6 | 5 | `8dB` in 1, 8, 15, 17; `5dB` in 14 |  |
| `kit.t2.patch.synth.layers.0.tilt` | 6 | 5 | `-6` in 1, 8, 14, 15, 17 |  |
| `kit.t2.patch.synth.filters.1.gain` | 6 | 5 | `8dB` in 1, 8, 15, 17; `5dB` in 14 |  |
| `kit.k.patch.synth.amp.d` | 6 | 5 | `170ms` in 8, 12, 17; `160ms` in 15; `80ms` in 16 |  |
| `kit.t3.patch.synth.layers.0.tilt` | 5 | 4 | `-6` in 1, 8, 14, 17 |  |
| `kit.t3.patch.synth.filters.1.gain` | 5 | 4 | `8dB` in 1, 8, 17; `5dB` in 14 |  |
| `kit.k.pitch` | 5 | 4 | `F1` in 5, 16; `Ab1` in 8; `C2` in 12 |  |
| `kit.x.patch.synth.layers.0.bright` | 5 | 5 | `0.6` in 10, 11, 12; `0.72` in 15; `0.65` in 17 |  |
| `kit.x.patch.synth.filters.2.cutoff` | 5 | 5 | `5000` in 10, 12, 15, 17; `5k` in 11 |  |
| `kit.s.patch.synth.layers.0.decay` | 4 | 4 | `0.15s` in 1, 8; `0.24s` in 10; `0.38s` in 13 |  |
| `kit.ft.patch.synth.layers.0.tilt` | 4 | 4 | `-6` in 1, 8, 15, 17 |  |
| `kit.ft.patch.synth.layers.1.level.mod.0.amount` | 4 | 4 | `76` in 1, 8, 15, 17 |  |
| `kit.ft.patch.synth.env.att.d` | 4 | 4 | `12ms` in 1, 8, 15, 17 |  |
| `kit.ft.patch.synth.filters.1.gain` | 4 | 4 | `8dB` in 1, 8, 15, 17 |  |
| `kit.t1.patch.synth.layers.1.level.mod.0.amount` | 4 | 4 | `76` in 1, 8, 15, 17 |  |
| `kit.t1.patch.synth.env.att.d` | 4 | 4 | `12ms` in 1, 8, 15, 17 |  |
| `kit.t2.patch.synth.layers.1.level.mod.0.amount` | 4 | 4 | `76` in 1, 8, 15, 17 |  |
| `kit.t2.patch.synth.env.att.d` | 4 | 4 | `12ms` in 1, 8, 15, 17 |  |
| `kit.s.patch.synth.pitch.mod.1.amount` | 4 | 4 | `0` in 7, 13, 16, 17 |  |
| `kit.t3.patch.synth.layers.0.decay` | 4 | 3 | `0.55s` in 14, 17; `0.35s` in 8 |  |
| `kit.t3.patch.synth.amp.d` | 4 | 3 | `0.7s` in 14, 17; `0.4s` in 8 |  |
| `kit.t3.patch.synth.layers.1.level.mod.0.amount` | 3 | 3 | `76` in 1, 8, 17 |  |
| `kit.t3.patch.synth.env.att.d` | 3 | 3 | `12ms` in 1, 8, 17 |  |
| `kit.k.patch.synth.pitch.mod.1.amount` | 3 | 2 | `0` in 5, 16 |  |
| `kit.s.patch.synth.layers.0.tune_sounding` | 3 | 3 | `true` in 7, 13, 17 |  |
| `kit.s.patch.synth.layers.0.tune_exact` | 3 | 3 | `true` in 7, 13, 17 |  |
| `kit.t1.patch.synth.layers.0.damp` | 3 | 3 | `0.8` in 8, 15, 17 |  |
| `kit.t2.patch.synth.layers.0.damp` | 3 | 3 | `0.8` in 8, 15, 17 |  |
| `kit.x.gain` | 3 | 3 | `-7dB` in 10; `-3.5dB` in 11; `-8.5dB` in 17 |  |
| `kit.x.patch.synth.filters.1.gain` | 3 | 3 | `0dB` in 11, 17; `-3dB` in 15 |  |
| `kit.t3.patch.synth.layers.0.damp` | 2 | 2 | `0.8` in 8, 17 |  |
| `kit.k.patch.synth.layers.2.level.value` | 2 | 2 | `-40dB` in 11; `-54dB` in 16 |  |
| `kit.x.patch.synth.filters.2.gain` | 2 | 2 | `6dB` in 11; `3.5dB` in 17 |  |
| `kit.x.patch.synth.layers.0.tilt` | 2 | 2 | `0` in 11; `1` in 17 |  |
| `kit.t1.patch.synth.layers.1.level.value` | 2 | 1 | `-50dB` in 14 |  |
| `kit.t2.patch.synth.layers.1.level.value` | 2 | 1 | `-50dB` in 14 |  |
| `kit.t3.patch.synth.layers.1.level.value` | 2 | 1 | `-50dB` in 14 |  |
| `kit.s.patch.synth.filters.2.kind` | 2 | 2 | `peak` in 16, 17 |  |
| `kit.s.patch.synth.filters.2.cutoff` | 2 | 2 | `900` in 16; `650` in 17 |  |
| `kit.s.patch.synth.filters.2.q` | 2 | 2 | `1` in 16; `0.8` in 17 |  |
| `kit.s.patch.synth.filters.2.gain` | 2 | 2 | `-6dB` in 16; `-8dB` in 17 |  |
| `kit.ft2.patch.synth.layers.0.tilt` | 1 | 1 | `-6` in 1 |  |
| `kit.ft2.patch.synth.layers.1.level.mod.0.amount` | 1 | 1 | `76` in 1 |  |
| `kit.ft2.patch.synth.env.att.d` | 1 | 1 | `12ms` in 1 |  |
| `kit.ft2.patch.synth.filters.1.gain` | 1 | 1 | `8dB` in 1 |  |
| `kit.k.patch.synth.pitch.mod.0.amount` | 1 | 1 | `35` in 5 |  |
| `kit.ft.patch.synth.layers.0.damp` | 1 | 1 | `0.8` in 8 |  |
| `+filter.cutoff` | 1 | 1 | `9000` in 10 |  |
| `kit.h.gain` | 1 | 1 | `0dB` in 10 |  |
| `kit.hs.gain` | 1 | 1 | `-1dB` in 10 |  |
| `kit.h1.gain` | 1 | 1 | `-1.5dB` in 10 |  |
| `kit.h2.gain` | 1 | 1 | `-5.5dB` in 10 |  |
| `kit.h3.gain` | 1 | 1 | `-7dB` in 10 |  |
| `kit.oh.gain` | 1 | 1 | `-5dB` in 10 |  |
| `kit.hp.gain` | 1 | 1 | `-4dB` in 10 |  |
| `kit.x.patch.synth.filters.0.cutoff` | 1 | 1 | `3000` in 11 |  |
| `kit.rde.gain` | 1 | 1 | `0dB` in 11 |  |
| `kit.ss.gain` | 1 | 1 | `7dB` in 13 |  |
| `kit.g.gain` | 1 | 1 | `-5dB` in 13 |  |
| `kit.s.patch.synth.layers.0.gap` | 1 | 1 | `0.05` in 13 |  |
| `kit.s.patch.synth.layers.0.cavity` | 1 | 1 | `0.162` in 16 |  |
| `kit.s.patch.synth.filters.1.cutoff` | 1 | 1 | `175` in 16 |  |
| `kit.s.patch.synth.pitch.mod.0.amount` | 1 | 1 | `0` in 16 |  |
| `kit.s.patch.synth.filters.0.cutoff` | 1 | 1 | `110` in 16 |  |
| `kit.k.patch.synth.layers.3.level.value` | 1 | 1 | `-54dB` in 16 |  |
| `kit.ft.pitch` | 1 | 1 | `m41` in 17 |  |
| `kit.t1.pitch` | 1 | 1 | `m60.02` in 17 |  |
| `kit.t2.pitch` | 1 | 1 | `m53` in 17 |  |
| `kit.t3.pitch` | 1 | 1 | `m48.02` in 17 |  |

## `ct-twin`: 16 songs, 76 tracks; as it comes in tracks 3

| field | tracks | songs | values (the songs) | |
|---|---|---|---|---|
| `fx.2.cone` | 71 | 16 | `32` in 5, 6; `33` in 5, 6; `41` in 5, 12, 16; `140` in 14; `141` in 14; `142` in 14; `143` in 14; `4` in 2; and 35 more values |  |
| `fx.2.mic` | 67 | 14 | `0.5` in 2, 3, 4, 5, 6, 8, 9, 14, 16; `0.45` in 5, 10, 17; `0.35` in 3, 4, 7, 8, 14; `0.6` in 2, 6; `0.47` in 6, 9; `0.55` in 14; `0.4` in 14; `0.25` in 12; and 1 more values |  |
| `fx.1.model` | 63 | 15 | `gojira` in 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17; `modern` in 2, 4, 6, 8, 9, 14; `mark` in 5, 6; `5150` in 3, 5; `nolly` in 3 |  |
| `synth.filters.0.cutoff.mod.0.amount` | 57 | 15 | `-2` in 2, 3, 5, 6, 7, 8, 10, 11, 13, 14, 15, 16, 17; `-3` in 9; `-2.7` in 9; `-3.4` in 12 | AGREED |
| `synth.layers.0.soft` | 33 | 10 | `expr.pm*0.5` in 2, 3, 5, 8, 10, 14, 15; `expr.pm*0.4` in 9, 11; `expr.pm*0.3` in 13 |  |
| `fx.1.tight` | 30 | 8 | `150` in 3, 5, 8, 9, 13, 15, 17; `180` in 14 |  |
| `synth.layers.0.mute` | 27 | 6 | `expr.pm*0.6` in 9, 10, 17; `expr.hand*0.8` in 5; `expr.pm*0.56` in 12, 16; `expr.pm*0.8` in 5 |  |
| `synth.layers.0.mute_width` | 27 | 6 | `0.1` in 5, 9, 10, 17; `0.10` in 12, 16 |  |
| `synth.layers.0.thump.mod.0.amount` | 24 | 5 | `0` in 3, 5, 9, 13, 17 |  |
| `+transient.attack` | 14 | 5 | `3.0` in 8, 12; `2.0` in 9; `8.0` in 7; `5.0` in 8; `4.0` in 16 |  |
| `fx.0.attack` | 10 | 4 | `15ms` in 7, 8, 12, 16 |  |
| `synth.pitch.mod.1.amount` | 10 | 3 | `0` in 14, 16, 17 |  |
| `synth.layers.0.soft.mod.1.src` | 8 | 1 | `expr.hand` in 5 |  |
| `synth.layers.0.soft.mod.1.amount` | 8 | 1 | `-0.5` in 5 |  |
| `fx.0.release` | 8 | 3 | `200ms` in 8, 12, 16 |  |
| `+transient.sustain` | 8 | 3 | `-1.0` in 8, 12, 16 |  |
| `synth.pitch.mod.2.amount` | 6 | 2 | `0` in 14, 17 |  |
| `synth.layers.0.tune_sounding` | 6 | 2 | `true` in 16, 17 |  |
| `synth.layers.0.thump` | 4 | 1 | `expr.pm*0.2` in 8; `0` in 8 |  |
| `synth.pitch.value` | 4 | 1 | `-0.027` in 14; `-0.037` in 14 |  |
| `synth.layers.0.decay.mod.0.amount` | 2 | 1 | `-2.6` in 3 |  |
| `fx.2.model` | 2 | 1 | `1x12` in 3 |  |
| `synth.amp.r` | 2 | 1 | `20ms` in 7 |  |
| `synth.pitch.mod.3.src` | 2 | 1 | `expr.bend` in 7 |  |
| `synth.pitch.mod.3.amount` | 2 | 1 | `1` in 7 |  |
| `synth.layers.0.choke` | 2 | 1 | `120ms` in 8 |  |
| `fx.1.sag` | 2 | 1 | `0.5` in 12 |  |
| `+filter.q` | 1 | 1 | `0.7` in 2 |  |

## `808`: 11 songs, 19 tracks; as it comes in tracks 5, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17

| field | tracks | songs | values (the songs) | |
|---|---|---|---|---|
| `synth.amp.r` | 1 | 1 | `20ms` in 7 |  |

## `ct-wall-stop-l`: 9 songs, 10 tracks; as it comes in tracks 4, 10

| field | tracks | songs | values (the songs) | |
|---|---|---|---|---|
| `+cab.cone` | 9 | 8 | `144` in 14; `52` in 7; `64` in 8; `74` in 9; `87` in 10; `14` in 11; `94` in 15; `101` in 17 |  |
| `+cab.mic` | 9 | 8 | `0.4` in 9, 11, 14, 17; `0.5` in 7, 8, 15; `0.55` in 10 |  |
| `+cab.model` | 9 | 8 | `4x12-modern` in 7, 8, 9, 10, 11, 14, 15, 17 | AGREED |
| `fx.3.mix` | 6 | 5 | `0` in 7, 9, 14, 15, 17 | AGREED |
| `fx.4.bands.0.gain` | 6 | 5 | `0dB` in 7, 9, 14, 15, 17 | AGREED |
| `fx.4.bands.1.gain` | 6 | 5 | `0dB` in 7, 9, 14, 15, 17 | AGREED |
| `fx.4.bands.2.gain` | 6 | 5 | `0dB` in 7, 9, 14, 15, 17 | AGREED |
| `fx.4.bands.3.gain` | 6 | 5 | `0dB` in 7, 9, 14, 15, 17 | AGREED |
| `synth.layers.0.thump.mod.0.amount` | 4 | 4 | `0.2` in 7, 11, 15; `0` in 8 |  |
| `synth.filters.0.cutoff.mod.0.amount` | 3 | 3 | `-2` in 8, 11, 15 |  |
| `synth.pitch.mod.2.amount` | 3 | 2 | `0` in 14, 17 |  |
| `synth.pitch.mod.1.amount` | 3 | 2 | `0` in 14, 17 |  |
| `synth.pitch.value` | 2 | 1 | `-0.041` in 14 |  |
| `synth.amp.r` | 1 | 1 | `20ms` in 7 |  |
| `synth.pitch.mod.3.src` | 1 | 1 | `expr.bend` in 7 |  |
| `synth.pitch.mod.3.amount` | 1 | 1 | `1` in 7 |  |
| `synth.layers.0.choke` | 1 | 1 | `120ms` in 8 |  |
| `+transient.attack` | 1 | 1 | `4.0` in 8 |  |
| `+transient.sustain` | 1 | 1 | `-1.0` in 8 |  |
| `+filter.cutoff` | 1 | 1 | `130` in 10 |  |
| `+filter.kind` | 1 | 1 | `hp` in 10 |  |
| `synth.layers.0.tune_sounding` | 1 | 1 | `true` in 17 |  |

## `ct-clean`: 8 songs, 13 tracks; as it comes in tracks 4, 9, 12, 13

| field | tracks | songs | values (the songs) | |
|---|---|---|---|---|
| `+reverb.decay` | 5 | 3 | `1.6s` in 9, 14; `0.85s` in 12 |  |
| `+reverb.mix` | 5 | 3 | `0.12` in 9, 12; `0.1` in 14 |  |
| `+reverb.predelay` | 5 | 3 | `20ms` in 9, 14; `12ms` in 12 |  |
| `+phaser.depth` | 5 | 3 | `0.55` in 9, 10, 14 |  |
| `+phaser.mix` | 5 | 3 | `0.35` in 10, 14; `0.38` in 9 |  |
| `+phaser.rate` | 5 | 3 | `0.18` in 9, 14; `0.16` in 9, 10; `0.11` in 14 |  |
| `synth.layers.0.inharm` | 4 | 2 | `0.00008` in 1, 10 |  |
| `fx.3.mix` | 3 | 2 | `0` in 6, 14 |  |
| `synth.layers.0.node` | 2 | 2 | `expr.node` in 6; `4` in 13 |  |
| `synth.layers.0.pinch` | 2 | 2 | `expr.contact` in 6; `1` in 13 |  |
| `+phaser.feedback` | 2 | 1 | `0.32` in 9 |  |
| `synth.pitch.mod.0.amount` | 2 | 1 | `0` in 14 |  |
| `synth.pitch.mod.1.amount` | 2 | 1 | `0` in 14 |  |
| `synth.layers.0.tune_sounding` | 2 | 1 | `true` in 14 |  |
| `strum` | 2 | 1 | `20ms` in 14 |  |
| `+tremolo.depth` | 1 | 1 | `0.85` in 1 |  |
| `+tremolo.rate` | 1 | 1 | `1.75b` in 1 |  |
| `synth.layers.0.pickup` | 1 | 1 | `0.075` in 6 |  |
| `synth.layers.0.soft` | 1 | 1 | `1` in 6 |  |
| `synth.layers.0.choke` | 1 | 1 | `55ms` in 6 |  |
| `synth.amp.r` | 1 | 1 | `45ms` in 6 |  |
| `play.gate` | 1 | 1 | `1` in 6 |  |
| `+reverb.kind` | 1 | 1 | `chamber` in 12 |  |
| `fx.0.threshold` | 1 | 1 | `0dB` in 13 |  |

## `ct-wall-stop-r`: 8 songs, 9 tracks; as it comes in tracks 4

| field | tracks | songs | values (the songs) | |
|---|---|---|---|---|
| `+cab.cone` | 8 | 7 | `145` in 14; `53` in 7; `65` in 8; `75` in 9; `15` in 11; `95` in 15; `102` in 17 |  |
| `+cab.mic` | 8 | 7 | `0.4` in 9, 11, 14, 17; `0.5` in 7, 8, 15 | AGREED |
| `+cab.model` | 8 | 7 | `4x12-modern` in 7, 8, 9, 11, 14, 15, 17 | AGREED |
| `fx.3.mix` | 6 | 5 | `0` in 7, 9, 14, 15, 17 | AGREED |
| `fx.4.bands.0.gain` | 6 | 5 | `0dB` in 7, 9, 14, 15, 17 | AGREED |
| `fx.4.bands.1.gain` | 6 | 5 | `0dB` in 7, 9, 14, 15, 17 | AGREED |
| `fx.4.bands.2.gain` | 6 | 5 | `0dB` in 7, 9, 14, 15, 17 | AGREED |
| `fx.4.bands.3.gain` | 6 | 5 | `0dB` in 7, 9, 14, 15, 17 | AGREED |
| `synth.layers.0.thump.mod.0.amount` | 4 | 4 | `0.2` in 7, 11, 15; `0` in 8 |  |
| `synth.filters.0.cutoff.mod.0.amount` | 3 | 3 | `-2` in 8, 11, 15 |  |
| `synth.pitch.mod.2.amount` | 3 | 2 | `0` in 14, 17 |  |
| `synth.pitch.mod.1.amount` | 3 | 2 | `0` in 14, 17 |  |
| `synth.pitch.value` | 2 | 1 | `-0.041` in 14 |  |
| `synth.amp.r` | 1 | 1 | `20ms` in 7 |  |
| `synth.pitch.mod.3.src` | 1 | 1 | `expr.bend` in 7 |  |
| `synth.pitch.mod.3.amount` | 1 | 1 | `1` in 7 |  |
| `synth.layers.0.choke` | 1 | 1 | `120ms` in 8 |  |
| `+transient.attack` | 1 | 1 | `4.0` in 8 |  |
| `+transient.sustain` | 1 | 1 | `-1.0` in 8 |  |
| `synth.layers.0.tune_sounding` | 1 | 1 | `true` in 17 |  |

## `voice-hook`: 5 songs, 11 tracks; as it comes in tracks 2

| field | tracks | songs | values (the songs) | |
|---|---|---|---|---|
| `synth.layers.0.diction` | 9 | 4 | `3` in 8, 14, 15, 17 | AGREED |
| `+reverb.decay` | 8 | 2 | `2.2s` in 14; `0.35s` in 2 |  |
| `+reverb.mix` | 8 | 2 | `0.14` in 14; `0.15` in 2 |  |
| `+reverb.predelay` | 8 | 2 | `30ms` in 14; `6ms` in 2 |  |
| `synth.layers.0.effort_tilt` | 8 | 3 | `1` in 8, 14, 15 | AGREED |
| `synth.layers.0.tract` | 3 | 1 | `0.86` in 14 |  |
| `synth.pitch.value` | 3 | 1 | `0.12` in 14; `0.08` in 14 |  |
| `+reverb.kind` | 2 | 1 | `room` in 2 |  |
| `play.phrase_arc` | 2 | 2 | `0.5` in 8, 15 |  |
| `synth.layers.0.consonant_level` | 2 | 1 | `6dB` in 14 |  |
| `synth.layers.0.aspirate` | 1 | 1 | `1` in 15 |  |
| `synth.layers.0.effort.value` | 1 | 1 | `0.8` in 17 |  |
| `synth.layers.0.speech` | 1 | 1 | `0.6` in 17 |  |

## `ct-glass`: 4 songs, 7 tracks; as it comes in tracks 4, 7, 9

| field | tracks | songs | values (the songs) | |
|---|---|---|---|---|
| `+phaser.feedback` | 4 | 3 | `0.32` in 9; `0.6` in 1; `0.35` in 7 |  |
| `+phaser.rate` | 4 | 3 | `2.75b` in 1; `0.14` in 7; `0.11` in 9; `0.1` in 9 |  |
| `synth.layers.0.inharm` | 3 | 1 | `0.00008` in 1 |  |
| `+phaser.depth` | 3 | 2 | `0.55` in 9; `0.62` in 7 |  |
| `+phaser.mix` | 3 | 2 | `0.38` in 9; `0.48` in 7 |  |
| `+reverb.decay` | 2 | 1 | `1.6s` in 9 |  |
| `+reverb.mix` | 2 | 1 | `0.12` in 9 |  |
| `+reverb.predelay` | 2 | 1 | `20ms` in 9 |  |

## `voice-choir`: 4 songs, 10 tracks; never as it comes

| field | tracks | songs | values (the songs) | |
|---|---|---|---|---|
| `synth.layers.0.tract` | 9 | 3 | `1.12` in 15; `0.95` in 1; `1.18` in 3; `1.1` in 3 |  |
| `synth.layers.0.effort_tilt` | 7 | 2 | `1` in 3, 15 |  |
| `synth.layers.0.diction` | 7 | 2 | `3` in 15, 17 |  |
| `fx.0.mix` | 7 | 2 | `0.14` in 15; `0.05` in 17 |  |
| `synth.layers.0.singers` | 4 | 1 | `1` in 15; `2` in 15; `3` in 15; `4` in 15 |  |
| `synth.layers.0.harmony` | 3 | 2 | `[7]` in 3; `[-5,7]` in 1 |  |
| `synth.layers.0.part_size` | 2 | 1 | `1` in 3 |  |
| `synth.layers.0.vib_spread` | 2 | 1 | `1` in 3 |  |
| `synth.layers.0.consonant_level` | 2 | 1 | `-3dB` in 3 |  |
| `synth.layers.0.effort.value` | 2 | 2 | `0.4` in 3; `0.8` in 17 |  |
| `synth.layers.0.speech` | 1 | 1 | `0.6` in 17 |  |

## `voice-legato`: 4 songs, 7 tracks; never as it comes

| field | tracks | songs | values (the songs) | |
|---|---|---|---|---|
| `fx.0.mix` | 7 | 4 | `0` in 1, 7, 10, 13 | AGREED |
| `synth.layers.0.diction` | 6 | 3 | `3` in 7, 10, 13 | AGREED |
| `synth.layers.0.ring` | 6 | 3 | `1.0` in 7, 10, 13 | AGREED |
| `synth.layers.0.effort.value` | 6 | 3 | `0.9` in 7, 10, 13; `0.8` in 7, 10 | AGREED |
| `synth.layers.0.inhale` | 4 | 2 | `0` in 1, 10 |  |
| `synth.layers.0.tract` | 3 | 2 | `0.86` in 7, 10; `1.1` in 7 |  |
| `+clip.ceiling` | 2 | 1 | `-12dB` in 7 |  |
| `synth.layers.0.hum` | 1 | 1 | `0.8` in 1 |  |

## `kidman`: 3 songs, 5 tracks; never as it comes

| field | tracks | songs | values (the songs) | |
|---|---|---|---|---|
| `synth.layers.0.diction` | 5 | 3 | `2` in 1, 2, 15 | AGREED |
| `synth.layers.0.speech` | 5 | 3 | `1` in 1, 2, 15 | AGREED |
| `synth.layers.0.tract` | 2 | 1 | `1.06` in 15; `0.96` in 15 |  |

## `voice-speech`: 3 songs, 3 tracks; as it comes in tracks 1

| field | tracks | songs | values (the songs) | |
|---|---|---|---|---|
| `synth.layers.0.join` | 2 | 2 | `true` in 3, 5 |  |
| `synth.layers.0.effort.value` | 2 | 2 | `0.7` in 3; `0.75` in 5 |  |
| `synth.layers.0.ring` | 2 | 2 | `0.6` in 3; `0.8` in 5 |  |
| `synth.layers.0.effort_tilt` | 1 | 1 | `1` in 3 |  |
| `synth.layers.0.diction` | 1 | 1 | `2` in 5 |  |

## `bass-fuzz`: 2 songs, 2 tracks; never as it comes

| field | tracks | songs | values (the songs) | |
|---|---|---|---|---|
| `fx.0.shape` | 2 | 2 | `wavefold` in 3, 4 |  |

## `ct-bell`: 2 songs, 4 tracks; as it comes in tracks 11

| field | tracks | songs | values (the songs) | |
|---|---|---|---|---|
| `synth.layers.0.inharm` | 2 | 1 | `0.00008` in 1 |  |
| `+orbit.radius` | 1 | 1 | `2` in 1 |  |
| `+orbit.rate` | 1 | 1 | `2.5b` in 1 |  |

## `ct-crunch-l`: 2 songs, 2 tracks; as it comes in tracks 9

| field | tracks | songs | values (the songs) | |
|---|---|---|---|---|
| `synth.layers.0.mute` | 1 | 1 | `expr.pm*0.6` in 1 |  |
| `synth.layers.0.mute_width` | 1 | 1 | `0.1` in 1 |  |
| `synth.layers.0.decay.mod.0.amount` | 1 | 1 | `0` in 1 |  |
| `synth.filters.0.cutoff.mod.0.amount` | 1 | 1 | `0` in 1 |  |
| `synth.layers.0.bright.mod.0.amount` | 1 | 1 | `0` in 1 |  |
| `fx.6.kind` | 1 | 1 | `spring` in 1 |  |
| `fx.6.mix` | 1 | 1 | `auto.wet` in 1 |  |
| `fx.6.decay` | 1 | 1 | `1.6s` in 1 |  |
| `fx.6.drip` | 1 | 1 | `1` in 1 |  |

## `ct-crunch-r`: 2 songs, 2 tracks; as it comes in tracks 9

| field | tracks | songs | values (the songs) | |
|---|---|---|---|---|
| `synth.layers.0.mute` | 1 | 1 | `expr.pm*0.6` in 1 |  |
| `synth.layers.0.mute_width` | 1 | 1 | `0.1` in 1 |  |
| `synth.layers.0.decay.mod.0.amount` | 1 | 1 | `0` in 1 |  |
| `synth.filters.0.cutoff.mod.0.amount` | 1 | 1 | `0` in 1 |  |
| `synth.layers.0.bright.mod.0.amount` | 1 | 1 | `0` in 1 |  |
| `fx.6.kind` | 1 | 1 | `spring` in 1 |  |
| `fx.6.mix` | 1 | 1 | `auto.wet` in 1 |  |
| `fx.6.decay` | 1 | 1 | `1.6s` in 1 |  |
| `fx.6.drip` | 1 | 1 | `1` in 1 |  |

## `harmonium`: 2 songs, 4 tracks; as it comes in tracks 11

| field | tracks | songs | values (the songs) | |
|---|---|---|---|---|
| `fx.0.depth` | 3 | 1 | `0` in 16 |  |
| `synth.layers.1.cents` | 3 | 1 | `0` in 16 |  |
| `fx.1.mix` | 2 | 1 | `0.06` in 16 |  |
| `synth.layers.4.wave` | 2 | 1 | `sine` in 16 |  |
| `synth.layers.4.ratio` | 2 | 1 | `3` in 16 |  |
| `synth.layers.4.level` | 2 | 1 | `-10.5dB` in 16 |  |
| `+pump.attack` | 1 | 1 | `12ms` in 11 |  |
| `+pump.curve` | 1 | 1 | `0.65` in 11 |  |
| `+pump.depth` | 1 | 1 | `-13dB` in 11 |  |
| `+pump.every` | 1 | 1 | `3/8` in 11 |  |
| `+pump.hold` | 1 | 1 | `28ms` in 11 |  |
| `+pump.release` | 1 | 1 | `395ms` in 11 |  |
| `+rotary.depth` | 1 | 1 | `0.65` in 11 |  |
| `+rotary.doppler` | 1 | 1 | `0.6` in 11 |  |
| `+rotary.speed` | 1 | 1 | `0.22` in 11 |  |
| `+rotary.spread` | 1 | 1 | `0.9` in 11 |  |

## `juno-pad`: 2 songs, 2 tracks; as it comes in tracks 1, 2

| field | tracks | songs | values (the songs) | |
|---|---|---|---|---|
| `+barberpole.bands` | 1 | 1 | `5` in 1 |  |
| `+barberpole.cycle` | 1 | 1 | `20b` in 1 |  |
| `+barberpole.low` | 1 | 1 | `100` in 1 |  |
| `+barberpole.q` | 1 | 1 | `8.0` in 1 |  |
| `+barberpole.spread` | 1 | 1 | `0.3` in 1 |  |
| `+phaser.depth` | 1 | 1 | `0.55` in 2 |  |
| `+phaser.mix` | 1 | 1 | `0.3` in 2 |  |
| `+phaser.rate` | 1 | 1 | `0.13` in 2 |  |

## `lead-monster`: 2 songs, 3 tracks; as it comes in tracks 4, 8

| field | tracks | songs | values (the songs) | |
|---|---|---|---|---|
| `synth.layers.2.wave` | 1 | 1 | `sine` in 8 |  |
| `synth.layers.2.ratio` | 1 | 1 | `1` in 8 |  |
| `synth.layers.2.level.value` | 1 | 1 | `-400dB` in 8 |  |
| `synth.layers.2.level.mod.0.src` | 1 | 1 | `auto.sing` in 8 |  |
| `synth.layers.2.level.mod.0.amount` | 1 | 1 | `1` in 8 |  |
| `synth.layers.3.wave` | 1 | 1 | `sine` in 8 |  |
| `synth.layers.3.ratio` | 1 | 1 | `2` in 8 |  |
| `synth.layers.3.level.value` | 1 | 1 | `-397dB` in 8 |  |
| `synth.layers.3.level.mod.0.src` | 1 | 1 | `auto.sing` in 8 |  |
| `synth.layers.3.level.mod.0.amount` | 1 | 1 | `1` in 8 |  |

## `m8-lead-guitar`: 2 songs, 6 tracks; as it comes in tracks 1

| field | tracks | songs | values (the songs) | |
|---|---|---|---|---|
| `fx.4.mix` | 3 | 1 | `0.18` in 14 |  |
| `fx.5.mix` | 3 | 1 | `0.15` in 14 |  |
| `synth.pitch.mod.2.amount` | 3 | 1 | `1` in 14; `0` in 14 |  |
| `synth.layers.0.tune_sounding` | 2 | 1 | `true` in 14 |  |
| `synth.pitch.mod.2.src` | 2 | 1 | `auto.shake` in 14 |  |
| `fx.4.time` | 2 | 1 | `343.615ms` in 14 |  |
| `synth.pitch.mod.1.amount` | 1 | 1 | `0` in 14 |  |
| `synth.pitch.value` | 1 | 1 | `-0.054` in 14 |  |

## `modal-gong`: 2 songs, 2 tracks; as it comes in tracks 3

| field | tracks | songs | values (the songs) | |
|---|---|---|---|---|
| `play.gate` | 1 | 1 | `1` in 5 |  |
| `synth.amp.r` | 1 | 1 | `65ms` in 5 |  |
| `synth.layers.0.damp` | 1 | 1 | `0.1` in 5 |  |
| `synth.layers.0.strike` | 1 | 1 | `expr.edge` in 5 |  |
| `+filter.cutoff` | 1 | 1 | `150` in 5 |  |
| `+filter.kind` | 1 | 1 | `hp` in 5 |  |

## `ondes`: 2 songs, 2 tracks; never as it comes

| field | tracks | songs | values (the songs) | |
|---|---|---|---|---|
| `fx.0.mix` | 2 | 2 | `{value:0,mod:[{src:auto.palme,amount:0.15}]}` in 12; `0.15` in 17 |  |
| `synth.amp.r` | 1 | 1 | `90ms` in 12 |  |
| `fx.0.notes` | 1 | 1 | `F4,Gb4,Ab4,C5` in 12 |  |
| `fx.0.decay` | 1 | 1 | `4s` in 12 |  |
| `fx.0.tune_sounding` | 1 | 1 | `true` in 12 |  |
| `fx.1.mix` | 1 | 1 | `0.04` in 12 |  |
| `fx.1.decay` | 1 | 1 | `0.8s` in 12 |  |
| `synth.pitch.mod.0.amount` | 1 | 1 | `0.05` in 17 |  |
| `+sympathetic.decay` | 1 | 1 | `8s` in 17 |  |
| `+sympathetic.notes` | 1 | 1 | `43.675hz` in 17 |  |

## `organ-pipe`: 2 songs, 3 tracks; never as it comes

| field | tracks | songs | values (the songs) | |
|---|---|---|---|---|
| `fx.0.mix` | 3 | 2 | `0` in 3; `0.22` in 9 |  |
| `synth.layers.0.level.value` | 2 | 1 | `-70dB` in 3 |  |
| `synth.layers.1.level.value` | 2 | 1 | `-6dB` in 3 |  |
| `synth.layers.2.level.value` | 2 | 1 | `-70dB` in 3 |  |
| `synth.layers.3.level.value` | 2 | 1 | `0dB` in 3 |  |
| `synth.layers.4.level.value` | 2 | 1 | `-8dB` in 3 |  |
| `fx.0.decay` | 1 | 1 | `1.6s` in 9 |  |
| `+rotary.mix` | 1 | 1 | `0.55` in 9 |  |
| `+rotary.speed` | 1 | 1 | `0.35` in 9 |  |

## `tabla-kit`: 2 songs, 5 tracks; as it comes in tracks 14

| field | tracks | songs | values (the songs) | |
|---|---|---|---|---|
| `kit.na.choke` | 3 | 1 | `dayan` in 9 |  |
| `kit.tin.choke` | 3 | 1 | `dayan` in 9 |  |
| `kit.te.choke` | 3 | 1 | `dayan` in 9 |  |
| `kit.re.choke` | 3 | 1 | `dayan` in 9 |  |
| `kit.ge.choke` | 3 | 1 | `bayan` in 9 |  |
| `kit.gem.choke` | 3 | 1 | `bayan` in 9 |  |
| `kit.na.patch.synth.amp.d` | 3 | 1 | `250ms` in 9 |  |
| `kit.tin.patch.synth.amp.d` | 3 | 1 | `300ms` in 9 |  |
| `kit.na.patch.synth.layers.1.level.value` | 3 | 1 | `-116dB` in 9 |  |
| `kit.tin.patch.synth.layers.1.level.value` | 3 | 1 | `-118dB` in 9 |  |
| `kit.na.patch.synth.env.c.d` | 3 | 1 | `120ms` in 9 |  |
| `kit.tin.patch.synth.env.c.d` | 3 | 1 | `120ms` in 9 |  |
| `kit.na.patch.synth.layers.0.partials` | 3 | 1 | `[[2,1],[3,0.8],[4,0.65],[5,0.45],[1,0.12]]` in 9 |  |
| `kit.tin.patch.synth.layers.0.partials` | 3 | 1 | `[[1,0.75],[2,1],[3,0.65],[4,0.45],[5,0.25]]` in 9 |  |
| `kit.ge.gain` | 3 | 1 | `-4.5dB` in 9 |  |
| `kit.gem.gain` | 3 | 1 | `-4.5dB` in 9 |  |
| `kit.na.patch.synth.filters.1.cutoff.value` | 3 | 1 | `2.5k` in 9 |  |
| `kit.tin.patch.synth.filters.1.cutoff.value` | 3 | 1 | `2.5k` in 9 |  |

## `tagelharpa-bass`: 2 songs, 3 tracks; as it comes in tracks 3

| field | tracks | songs | values (the songs) | |
|---|---|---|---|---|
| `play.mono` | 2 | 1 | `true` in 15 |  |
| `play.legato` | 2 | 1 | `true` in 15 |  |
| `play.glide` | 2 | 1 | `350ms` in 15 |  |
| `play.glide_smooth` | 2 | 1 | `true` in 15 |  |
| `synth.pitch.mod.0.amount` | 2 | 1 | `0` in 15 |  |
| `synth.pitch.mod.1.amount` | 2 | 1 | `0.05` in 15 |  |

## `voice-near`: 2 songs, 5 tracks; never as it comes

| field | tracks | songs | values (the songs) | |
|---|---|---|---|---|
| `synth.layers.0.diction` | 5 | 2 | `3` in 6, 13 |  |
| `synth.layers.0.tract` | 4 | 1 | `1.04` in 6; `0.98` in 6 |  |
| `synth.layers.0.breath.value` | 4 | 1 | `0.13` in 6 |  |
| `synth.layers.0.effort.value` | 4 | 1 | `0.55` in 6 |  |
| `synth.layers.0.inhale` | 4 | 1 | `0.1` in 6 |  |
| `play.glide` | 4 | 1 | `35ms` in 6 |  |
| `synth.layers.0.ring` | 4 | 1 | `0.5` in 6 |  |

## `voice-talk`: 2 songs, 7 tracks; as it comes in tracks 1, 2

| field | tracks | songs | values (the songs) | |
|---|---|---|---|---|
| `+reverb.decay` | 3 | 1 | `0.35s` in 2 |  |
| `+reverb.kind` | 3 | 1 | `room` in 2 |  |
| `+reverb.mix` | 3 | 1 | `0.15` in 2 |  |
| `+reverb.predelay` | 3 | 1 | `6ms` in 2 |  |

