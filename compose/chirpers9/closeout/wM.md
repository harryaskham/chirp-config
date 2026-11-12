# wM (engine/library, the voice climb): close-out

**Engine.**
- Landed: about 40 opt-in features (41 rows in features.md), most of them for the voice: sung glides, melisma, `diph_hold`, `phrase_arc`, the choir spreads, `creak`, `age_high`, `vowel_drift`, and `diction` 1 and 2. On the album's 29 sung lines the word error rate went 0.65 (none) to 0.50 (level 1) to 0.42 (level 2).
- Landed too late: `diction` 2 was pinned at 16:42 on the day of the cut and set in one round that nobody heard. Harry heard only t2's hook.
- My mistake: the first level 2 lost 3.3 dB at 4-10 kHz on that hook. I had measured words and not level; Harry heard a quieter voice and chirp-eco found the cause. It was withdrawn before pinning and fixed (a squeezed consonant keeps its energy).
- Built, tested and not landed (tools branch `wm-voice-next` at 000cb09f, not gated): `effort_tilt` (a louder voice is brighter), `play.phrase_gap` (chirper-one's ask) and `diction` 3.
- Promised and not built: a stereo `spread` on the noise layer (chirper-three), a plan warning for song-level `feel` keys that are ignored (t7's `nudge`), a `decay` on sympathetic.
- Still wrong in what is out: "each" on t2's hook (C5, 153 ms) is not heard as a word at any level; nor are "half", "far side" and "near side". At level 2 "it" in t8's "all of it falls" reads worse, and t6's five fast statements at 3:37-3:46 a little worse. The hook's /ch/ peaks 3 dB over its vowels.
- Two wrong answers I gave and took back: that the voice lacked tract poles above F5 (`cluster` already is the singer's formant), and that chirper-one should change a rhythm for "side" (the rhythm was not the fault).

**Patches/library.**
- Shipped: voice-legato, voice-hook, voice-near, voice-old, voice-choir, voice-backing; every sung line on the album extends one.
- Found on the last day, by ablation: those patches cost words. `even: 1`, which is in all of them, costs the most (0.17 nats a word); the choir settings 0.11; `formant_bw: 1.6` 0.06. `diction` 3 removes `even`'s cost (+0.17 nats a word over level 2, level unchanged), but it is not on this record.

**Songs.** None are mine. I changed no song; in the last round I gave the composers a per-line table instead.

**Album.**
- I cannot hear. Every voice decision was made on Whisper's reading and on level measures; two clips went to Harry. Nothing in the voice was checked by ear except that hook.
- Word error rate was too noisy to steer by (it could not separate level 1's variants). The measure that could (Whisper's support for each written word, `tf.py`) I wrote on the day of the cut.

**Next record.**
- Build the measurement first: the album's own sung lines, scored per word, with a level check (whole line, 4-10 kHz, peak) on every voice change before a composer adopts it. Then gate `diction` 3, `effort_tilt` and `phrase_gap` in the first week, and rebuild the voice patches on what the ablation showed.
- Agree an engine freeze a day before the cut, and put a clip in front of Harry for each voice change as it lands, since nobody else can hear it.
- Tools and data: `~/.local/state/chirp-evidence/diction-20261110` and `~/.local/state/wM`.
