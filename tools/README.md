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
