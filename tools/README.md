# chirp tools (user)

Keep a live `groove` session evolving as real songs.

- `evolve.py` — every loop pass the groove plays a generated song (`songs/form-1|2.yaml`) with a
  form that suits its style (rock / edm / classical / breakdown): intro, verses, pre, choruses,
  breakdown, solo, a lifted final section, outro; transitions (risers, impacts, reverse cymbals).
  Drums come from the `beat-*` parts; melodic material is freshly composed per song by
  `compose.py` (a key, mode and four-chord progression; an idiomatic main riff; a hook motif that
  is stated, sequenced and resolved; chords, arpeggio, held layer → `songs/gen-form-*`).
  A song lasts 2–3 passes, mutating one element per pass.
  Styles: djent djent-breakdown prog-clean poly house garage hardcore acid idm lofi classical doom-ambient.
- `compose.py STYLE` — compose a test set (`songs/gen-test-*`).
- `restart-groove.sh [SONG] [ARRANGEMENT]` — restart `groove` on a pinned copy of chirp and resume the evolver.

## Steering (applies to the playing song at the next bar, and to the queued one)

    echo "COMMAND" >> ~/.config/chirp/tools/steer.txt

| Command | Effect |
| --- | --- |
| `compose` / `melody` / `rekey` | new key + melody / new motifs, same key / new key, mode and progression |
| `key +2`, `tempo -4` | transpose / tempo |
| `swap ROLE [PART]` | re-pick a role (`mid high low half brk riff hook pad soft arp hold`) |
| `xf ROLE ^rev^rot=0.25^thin=0.2^aug=2^inv` | lasting motif transform on a role |
| `style NAME` | switch style now (same key) |
| `next NAME` | replace only the queued song with a fresh one in NAME |
| `journey on\|off`, `journey h=0.5 rate=0.05` | gradual heaviness climb (lofi … djent) |
| `mutate` | one random change |

`state.json` shows what is playing and queued; `journey.json` the heaviness climb (full djent mode:
mostly djent, sometimes breakdown, clean or another genre). Watch with `chirp watch`.

## Rigs (reusable sound choices)

`compose.py` keeps every instrument choice in `RIGS` (with fallbacks for builds that lack a patch)
and builds guitars through `rhythm_tracks(score)`, so other composition scripts get the same sound:

```python
import os, sys; sys.path.insert(0, os.path.expanduser("~/.config/chirp/tools")); import compose
tracks = compose.rhythm_tracks("expr.pm=1 F1/16@110 F1@98 …") + [compose.track("bass", compose.rig("bass"), "F1/16@110 …")]
```

| Role | Patches (first available) |
| --- | --- |
| rhythm | `m8-rhythm-l` + `m8-rhythm-r` — a real double: two rigs (5150 / Gojira voicings, different IRs, pick, pickup, stiffness), two players (seeds 7 / 13, looser right hand) |
| bass | `bass-fat` (heavy string DI + strong sub, light amp blend) → `bass-di` → `m8-bass` |
| sub / twang / lead / drums | `sub-sine` → `sub` · `m8-twang` · `lead-monster` · `prog-kit` |

In hand-written YAML, double a rhythm part the same way:

```yaml
- {name: gtr-l, patch: m8-rhythm-l, pan: L90, seed: 7, score: "…"}
- {name: gtr-r, patch: m8-rhythm-r, pan: R90, seed: 13, score: "…"}
```

Riff building blocks in `compose.py`: `gen_meshuggah` (odd cycles over a 4/4 pulse with locked
drums; power chords, clusters, choked stops, muted scratches; `mode` riff / toms / shuffle / break),
`gen_space` (ringing twangs with gaps), `gen_djent`, `gen_hook` (motif → sequence → cadence),
`gen_clusters`, `gen_hold`, `soften` (velocity-scaled variant). Modes include the evil ones
(double-harmonic, hungarian, neapolitan, phrygian-dominant, locrian, diminished).
