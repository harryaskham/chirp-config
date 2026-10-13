# racks — named, composable effect chains

A rack is `racks/NAME.yaml` (JSON is valid YAML): `about`, `fx` (a chain: effects, effect strings, or
`"rack:OTHER"` to nest), optional `macros` (`{name: {default, targets: [{path, amount}]}}`).
Reference them as `"rack:NAME"` anywhere an fx list is written; `tools/compose.py` expands them
(`compose.rack(name)`, `compose.expand(fx_list)`) until the engine resolves racks natively (bead filed).
Groups: rig-* (pedals → amp → cab → eq → gate), time (tape-echo, slapback, dub-throw, shimmer-hall,
plate-short, room-tight, spring-surf), modulation (stutter-16, phaser-slow, chorus-wide), dynamics
(glue-bus, pump, smash-ott, parallel-ny, opto-smooth, tape-warm, drum-bus-punch — compressors are
loudness-matched), lo-fi (bitcrush, radio, telephone), master (master-eq, master-default).
