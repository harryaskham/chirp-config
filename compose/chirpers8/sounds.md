# chirpers VIII: the sound bank

Shared palette for the engine showcase; earlier albums' banks are yours to borrow (compose/chirpers1..7/sounds.md). Add every new patch, fx chain, generator recipe, tuning and voice treatment here, so the next track can push it further instead of rediscovering it.

| sound | patch / recipe | by | what | lives in | borrowed by |
|---|---|---|---|---|---|
| c8-bar / c8-vibes / c8-glock / c8-bell / c8-tom (t3) | inline patches in src/chirpers8-t3.py `patches()`: one `type: modal` layer each, `modes: bar / vibes / glock / bell / membrane`, `bright` 0.3-0.7 + vel 0.35, `strike` 0.15-0.4 + rand 0.08, `vary` 0.4, amp d 2-9 s | chirper-two | a physical mallet orchestra (marimba, vibraphone, glockenspiel, church bell, tuned tom) that plays microtonal pitches exactly | chirpers8-t3 | |
| 7-limit JI as fractional MIDI (t3) | `m{50 + 12*log2(ratio):.3f}` for 1 9/8 7/6 4/3 3/2 14/9 7/4 (and comma chords of them); `^gate` caps at 4, so let struck notes ring through their release | chirper-two | any tuning written straight into the score | chirpers8-t3 | |
| cellular-automaton rhythm (t3) | `step(row, rule)`: new[i] = (rule >> (row[i-1]<<2 \| row[i]<<1 \| row[i+1])) & 1 on a ring; births/deaths drive other parts; population rotates Euclidean hats and bass | chirper-two | a pattern that is rule-bound but never repeats | chirpers8-t3 | |
