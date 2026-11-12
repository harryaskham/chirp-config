# Common Time (chirpers10): the sound bank

The first job on this record is the sound (album.json "brief"): a new family of guitars, amps, basses and kits, built on what is below with the engine as it is now. Add every new patch, rack, chain and recipe to the table at the bottom as you make it: name, what it is, what it was built from, where it lives. New names only; never edit a patch below (six released albums render through the library, and `tools/libguard.py` refuses a change that moves them).

## What exists: the djent family (inventory by chirp-eco, 12 Nov)

Made for the Meshuggah reproductions and *Ferrous Bloom* between 13 and 29 Oct; the engine has had 389 commits since the last of them changed.

| patch | what its `about` says | built from | last changed |
|---|---|---|---|
| `m8-bass-dist` |  | amp, cab, compressor, eq, gate; extends m8-bass | 13 Oct |
| `m8-bass` |  | amp, cab, gate, noise, pluck | 13 Oct |
| `m8-bkp-l` | Hot passive-pickup double (left): mid-peaked, more output, into a Gojira-voiced amp, cannibal-choir/impaler-jim. Pair with m8-bkp-r. | amp, compressor, eq, gate, ir, sympathetic; extends m8 | 29 Oct |
| `m8-bkp-r` | Hot passive-pickup double (right): other player, 5150, impaler-jim/cannibal-choir. | amp, compressor, eq, gate, ir, sympathetic; extends m8 | 29 Oct |
| `m8-chug-l` | Harder chug rig (left of a pair): compressor pedal into a Mark-voiced amp with a big screamer push and very tight lows, cookie-monster/kitten-slayer c... | amp, compressor, eq, gate, ir, sympathetic; extends m8 | 29 Oct |
| `m8-chug-r` | Harder chug rig (right of a pair): another player and rig - pick nearer the neck, stiffer string, compressor pedal into a 5150-voiced amp, darth-genoc... | amp, compressor, eq, gate, ir, sympathetic; extends m8 | 29 Oct |
| `m8-clean` |  | pluck | 13 Oct |
| `m8-emg-l` | Active-pickup double (left): flat, compressed EMG-style DI into a 5150, thick cab blend (kaiju-tamer/big-bubba). Pair with m8-emg-r. | amp, compressor, eq, gate, ir, sympathetic; extends m8 | 29 Oct |
| `m8-emg-r` | Active-pickup double (right): other player, Mark-voiced amp, october-32th/kaiju-tamer. | amp, compressor, eq, gate, ir, sympathetic; extends m8 | 29 Oct |
| `m8-fluence-l` | Airy, tight active double (left): Fluence-style DI into the modern amp, bright tight cab (devils-cunnilingus/cathode-ray-fleshburn). Pair with m8-flue... | amp, compressor, eq, gate, ir, sympathetic; extends m8 | 29 Oct |
| `m8-fluence-r` | Airy, tight active double (right): other player, 5150, cathode-ray-fleshburn/devils-cunnilingus. | amp, compressor, eq, gate, ir, sympathetic; extends m8 | 29 Oct |
| `m8-fuzz` | Fuzz rig for doom, sludge and slams: a folding fuzz pedal into a crunch amp, woolly and huge; cab blend, low-mid weight, fizz tamed, long plate. | amp, drive, eq, gate, ir, sympathetic; extends m8 | 29 Oct |
| `m8-gojira` |  | amp, eq, gate, ir; extends m8 | 29 Oct |
| `m8-mark` |  | amp, eq, gate, ir; extends m8 | 29 Oct |
| `m8-nolly` |  | amp, compressor, eq, gate, ir; extends m8 | 29 Oct |
| `m8-obzen-l` | obZen-era Meshuggah rhythm rig (left of a quad-trackable pair; pair with m8-obzen-r): the m8-chug-l player and chain, re-voiced against Bleed's palm-m... | amp, compressor, eq, gate, ir, sympathetic; extends m8 | 29 Oct |
| `m8-obzen-r` | obZen-era Meshuggah rhythm rig (right of a quad-trackable pair; pair with m8-obzen-l): the m8-chug-r player and chain, re-voiced against Bleed's palm-... | amp, compressor, eq, gate, ir, sympathetic; extends m8 | 29 Oct |
| `m8-phase` | Phaser pedal into a Gojira-voiced amp: slow six-stage sweep under heavy chugs and ringing chords - for space sections and as the odd side of a double. | amp, eq, gate, ir, phaser, sympathetic; extends m8 | 29 Oct |
| `m8-rhythm-l` | Left rhythm rig for double-tracked heavy riffs: the 8-string into a 5150-voiced amp with a screamer, cookie-monster/kitten-slayer cab blend, fizz dip ... | amp, eq, gate, ir, sympathetic; extends m8 | 29 Oct |
| `m8-rhythm-r` | Right rhythm rig for double-tracked heavy riffs: a different player and rig from m8-rhythm-l - pick nearer the neck, other pickup/coil and string stif... | amp, eq, gate, ir, sympathetic; extends m8 | 29 Oct |
| `m8-tight` | Smoother modern rhythm rig for polymetric/djent riffs: the 8-string into a lower-gain Gojira-voiced amp with a tighter low end, two-IR cab blend, 3 kH... | amp, eq, gate, ir, sympathetic; extends m8 | 29 Oct |
| `m8-twang-chorus` | Ringing 8-string through a chorus pedal into the twang amp: shimmering, wide open hits with ping-pong delay and hall. Leave gaps after each hit. | amp, chorus, eq, ir, sympathetic; extends m8 | 29 Oct |
| `m8-twang` | Big ringing 8-string for open hits that are left to play out: long sustain into a saturated amp, two-IR cab, dotted-16th ping-pong delay and a wide ha... | amp, eq, ir, sympathetic; extends m8 | 29 Oct |
| `m8-v2` |  | drive, eq, gate, noise, pluck | 13 Oct |
| `metal-kit-dry` | metal-kit with no bus effects: route its tracks to a shared drums bus (e.g. rack:drum-bus-punch) so the kit is glued and processed once per part inste... | ; extends metal-kit | 14 Oct |
| `metal-kit-phys` |  | drum; extends metal-kit-dry | 28 Oct |
| `metal-kit-punch` |  | noise; extends metal-kit-dry | 28 Oct |
| `metal-kit` | Fat modern metal kit (extends prog-kit) with articulations. Kick k (punchy, clicky, tight for double kick). Snare: s rimshot-thick main, sc centre, so... | additive, compressor, drive, eq, noise; extends prog-kit | 14 Oct |
| `bass-fat` | Fat modern metal bass DI: the picked bass string model with a long, heavy string (5 s decay, darker tone, a little more fret buzz) and a strong sine s... | amp, cab, compressor, eq, gate; extends m8-bass | 13 Oct |
| `kidman` | Harsh barked metal vocal on the voice engine (scream 0.8 and false-fold 0.6 put its harmonic-to-noise ratio and subharmonics inside Jens Kidman's meas... | compressor, voice | 15 Oct |
| `obzen-kit-dry` |  | compressor, drive, eq; extends obzen-kit | 26 Oct |
| `obzen-kit` |  | compressor, drive, eq; extends metal-kit | 15 Oct |


Built into the engine (no file in `patches/`; `chirp patch show NAME` prints them, and the library patches above extend them):

- `haake`: Haake-style metal kit, dynamic: every hit varies (pitch, tone, level) and velocity changes timbre (beater click, snare crack/wires
- `m8`: Meshuggah-style 8-string (F standard: F1 Bb1 Eb2 Ab2 Db3 Gb3 Bb3 Eb4): bridge-humbucker DI (pickup position, resonance) into a 3-s
- `m8-lead`: Fluid, saturated legato lead (Thordendal-ish) with delayed vibrato, ping-pong delay and a big room.
- `m8-lead-guitar`: Guitar take on the m8 lead (opt-in; m8-lead is the oscillator lead): the m8 string through a singing lead amp — legato notes are h
- `m8-lead-synth`: Synth take on a fluid, saturated legato lead (oscillators, the pre-2026 m8-lead) with delayed vibrato, ping-pong delay and a big r

Library parts: `songs/lib-meshuggah-brk.yaml`, `songs/lib-meshuggah-hook.yaml`, `songs/lib-meshuggah.yaml` (sections with both guitars, bass, sub and the kit; `tr=` transposes).

Racks they lean on: `rack:drum-bus-punch`, `rack:parallel-ny`, `rack:room-tight`. The first two carry their own dry signal: fine as an insert, but on a parallel send every hit is added twice (bd-e0185e). Build send-safe ones under new names if you want parallel drums.

Reference records for the genre envelope (`ref/ID.wav`, the reproductions' sources): broken-cog, dancers-to-a-discordant-system (9:36), in-death-is-death (13:22), they-move-below (9:35), bleed, the-faultless, ligature-marks, pravus. 35 Meshuggah reproductions are paused in the registry with their song files (`songs/ID.yaml`); they are measurements of those records, not material.

## The new family

| sound | patch / recipe | built from | what is new in it | lives in |
|---|---|---|---|---|
| rhythm guitars, a left/right pair | `ct-chug-l`, `ct-chug-r` | `m8-obzen-l` / `-r` (string, compressor, cab blend, EQ, gate, plate kept) | the amp is the engine's white-box one: triode preamp stages into a push-pull power amp inside a feedback loop (18 / 20 dB) driving a speaker's impedance; the low string settles from 0.8 semitones sharp over 110 ms; more scrape, twice the sympathetic ring, a palm mute that lasts twice as long. Against two records' guitar stems (tools/riffpunch.py, old pair -> this): Bleed 41.4 -> 67.0, The Faultless 37.8 -> 69.1 (separator floor 67-86). What each part gave on its own is in the patch's `about` and in ~/.local/state/chirper-zero/c10 (cands.py: 30 candidates) | `patches/ct-chug-l.yaml`, `patches/ct-chug-r.yaml`; t1 tracks gl, gr, gl2, gr2 |
| bass | `ct-bass` | `bass-fat` (the m8-bass string and sine sub, crunch amp, 4x10) | re-voiced against two records' bass stems, which live at 80-1300 Hz with little above 2.5 kHz: sub 6 dB lower, more string through a hotter amp (gain 0.7, mix 0.6), +6 / +8 dB at 110 / 220 Hz, +5 dB at 900 Hz, -10 dB above 1.5 kHz, 4 kHz low-pass. 1/3-octave envelope error against the stems (bbench.py, bass-fat -> this): Bleed 9.4 -> 4.7 dB, The Faultless 8.4 -> 3.8 dB. The white-box amp parts all measured worse on a bass; not used | `patches/ct-bass.yaml`; t1 track bass |
| kit (dry: no bus effects) | `ct-kit` | `metal-kit-dry`; `metal-kit-phys`'s snare; `modal-tom`, `modal-crash`, `modal-china`, `modal-ride` | SNARE: the physical `drum` layer (stick, two coupled heads, shell, wires) tightened to a 0.18 s head and a 140 ms envelope, +5 dB body at 200 Hz. tools/drumpunch.py against two records' drum stems (obzen-kit -> this snare, old cymbals): Bleed 44.1 -> 58.7, The Faultless 47.1 -> 56.8; the snare alone 26 -> 67 and 23 -> 40. TOMS: struck membranes on F3 C3 Ab2 F2 C2. CRASH, CHINA, RIDE: modal plates, high-passed at 1.2-1.5 kHz, at the old cymbals' level. Not settled: the bench reads the kit a little worse with the modal cymbals than with the old ones (56.4 and 55.5 against 58.7 and 56.8; the kick's reading, not the snare's); kept for an ear to judge. Kick: metal-kit's (a physical kick and an EQ'd one measured no better) | `patches/ct-kit.yaml`; t1 tracks kick, snare, cym, toms |
| drums bus (a recipe, in the song) | room 0.7 s at 10%, `glue` 2.5:1 at -24 dB, then `clip` with its ceiling at -13 dBFS | - | the kit's four tracks go to one bus (`out: drums`) and the bus is soft-clipped about 5 dB, as metal records do to kick and snare peaks: the whole mix then reaches -10 LUFS on a plain gain, with no limiter work, so what the groove plays (the raw mix) has the release's dynamics | t1 `buses.drums` |
| swell and drop (in the song) | `ct-swell`, `ct-drop` (song-local patches) | noise layer; sine | a breath in before a landing (band-passed noise that swells while the note is held, its band rising, cut on the bar line) and the floor dropping on it (a sine falling an octave in 0.35 s). Before 1:06, 3:29, 6:40, 6:59 and the landing | t1 `patches`, tracks rise, drop |
| hats and ride faders (a recipe) | the kit's hats and ride on their own tracks (`hat` +14 dB, `ride` +6 dB) | - | at the cymbals' fader a closed hat read 27-29 dB under the mix and the ride 23 under (tools/presence.py): parts nobody could hear. Now 16 and 12-15 under | t1 tracks hat, ride |
