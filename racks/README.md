# racks — named, composable effect chains

A rack is `racks/NAME.yaml` (JSON is valid YAML): `about`, `fx` (a chain: effects, effect strings, or
`"rack:OTHER"` to nest), optional `macros` (`{name: {default, targets: [{path, amount}]}}`).
Reference them as `"rack:NAME"` anywhere an fx list is written — the engine expands them natively
(nested racks, overrides like `rack:NAME 0.mix=0.3`, macros like `rack:NAME space=0.8` or
`space=var.space`; see the chirp README "Effect racks"). Racks here shadow the built-in copies.
`tools/compose.py`'s expansion still works but is no longer needed.
Groups: rig-* (pedals → amp → cab → eq → gate), time (tape-echo, slapback, dub-throw, shimmer-hall,
plate-short, room-tight, spring-surf), modulation (stutter-16, phaser-slow, chorus-wide), dynamics
(glue-bus, pump, smash-ott, parallel-ny, opto-smooth, tape-warm, drum-bus-punch — compressors are
loudness-matched), lo-fi (bitcrush, radio, telephone), master (master-eq, master-default).
