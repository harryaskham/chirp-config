#!/usr/bin/env python3
"""chirpers3-t4 (Tape Weather, track 4): "Hail on a Music Box". Composed by chirper-three.

GLITCHY IDM-LITE, a broken music box in a lo-fi beat.
- THE CLOCKWORK (mechanical, dead straight): a toy piano on a 5-sixteenth cycle (hits on steps 0 and 3), a music box on
  a 7-sixteenth cycle (0, 2, 4), and Ferrous Bloom's crystal on the quarters arpeggiating the chord. They realign only
  every 140 sixteenths (8.75 bars), so the texture never repeats bar to bar.
- THE HIDDEN MELODY: wherever a toy-piano note and a music-box note coincide, a tape lead sings and holds until the next
  coincidence: a melody nobody plays on purpose, made by the gears.
- THE BEAT (human, swung): a tight kit, 16ths swung at 0.58, kick patterns that shift bar by bar, ghost snares and
  dropped hats, crushed and low-passed, with the drum bus stuttering now and then.
- GLITCHES: probabilistic stutter on the toy and drum buses, composed HAIL (a toy note retriggered as 32nds) in
  the break, and since v8 the break's BEAT RESAMPLED through wM's chop (its own last bar cut into 8 slices and
  replayed as 0 0 r3 2 . 5 r7 _: repeats, reversals, a live slice, a dropout).
- HARMONY: Dbmaj9 | Cm7(11) | Fm9 | Bbm9, two bars each, with a BRIDGE in the breakdown (Gbmaj9 | Fm7 | Ebm9 |
  Ab13sus, turning home); wM's tape deck (wow, flutter, hiss) on the toys, the pad
  and the master, his vinyl (crackle, dust, warp) on the master; the kit's wonk from play.humanize (late snare,
  early kick, swing drift).
- THE GEAR CHANGE: the return turns the toy to a 6 against the box's 7 (a dotted-eighth hemiola); the full section
  puts the crystal on a 9, three odd gears; so the hidden melody's rhythm changes section by section.
- FORM (58 bars, 86 bpm): the WIND-UP (the key turned: gears speed up and rise to pitch), beat, melody, glitch
  break ending in a NEAR-STALL (the box almost runs down mid-song, then snaps back), return, breakdown, full, and
  the WIND-DOWN (the music box runs down: gears lengthen, pitches sag, the beat gives out). Harry liked the ending's
  'glitch resample' (v3, 8.0), so it now frames the song.
- THE BASS ANSWERS: the root, a reply on the swung and-of-3 (fifth or ninth), a chromatic walk into each change.

Emits songs/chirpers3-t4.yaml. Edit the music here.
"""
import json
import os
import random

OUT = os.environ.get("T4_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers3-t4.yaml")
BPM = 86
S = 16                                  # sixteenths per bar
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
SW = 0.58                               # 16th swing for the hand-played parts

CHORDS = [(1, [0, 4, 7, 11, 14]), (0, [0, 3, 7, 10, 17]), (5, [0, 3, 7, 10, 14]), (10, [0, 3, 7, 10, 14])]
TOY_SEQ = [80, 77, 87, 85, 82, 77]      # Ab5 F5 Eb6 Db6 Bb5 F5 (Db major pentatonic)
BOX_SEQ = [85, 80, 82, 89, 87]          # Db6 Ab5 Bb5 F6 Eb6

SECTIONS = [("intro", 1, 8), ("beat", 9, 16), ("melody", 17, 24), ("glitch", 25, 28), ("return", 29, 36),
            ("breakdown", 37, 44), ("full", 45, 52), ("outro", 53, 58)]
BARS = SECTIONS[-1][2]
TOTAL = BARS * S


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def b0(bar):
    return (bar - 1) * S


def sec_of(bar):
    for name, a, z in SECTIONS:
        if a <= bar <= z:
            return name
    return "outro"


def swing(x):
    pair = 2.0 * int(x // 2)
    f = x - pair
    return pair + (f * 2 * SW if f <= 1 else 2 * SW + (f - 1) * (2 - 2 * SW))


class Part:
    def __init__(self):
        self.ev = []

    def add(self, st, ln, head, vel):
        self.ev.append((st, ln, head, int(max(1, min(127, vel)))))

    def score(self, total=TOTAL):
        ev = sorted(self.ev, key=lambda e: (e[0], -e[3]))
        merged = []
        for e in ev:
            if merged and abs(merged[-1][0] - e[0]) < 1e-6:
                continue
            merged.append(e)
        toks, pos = [], 0.0
        for i, (s, ln, head, vel) in enumerate(merged):
            nxt = merged[i + 1][0] if i + 1 < len(merged) else total
            ln = min(ln, nxt - s)
            if ln <= 1e-6:
                continue
            if s - pos > 1e-4:
                toks.append(f"R/{(s - pos) / 4:.4g}b")
            toks.append(f"{head}/{ln / 4:.4g}b@{vel}")
            pos = s + ln
        if total - pos > 1e-4:
            toks.append(f"R/{(total - pos) / 4:.4g}b")
        return " ".join(toks)


P = {k: Part() for k in ("toy", "box", "xtal", "lead", "pad", "bass", "sub", "kick", "snare", "hat", "perc", "cpiano", "hail", "desc", "sq",
                         "ckick", "csnare", "chat", "ctoy", "cbox", "mist", "vox", "boxsong", "throw", "rlead")}
rng = random.Random(4)


BRIDGE = [(6, [0, 4, 7, 11, 14]), (5, [0, 3, 7, 10, 14]), (3, [0, 3, 7, 10, 14]), (8, [0, 5, 7, 10, 21])]
# the breakdown's BRIDGE (its last 4 bars, one chord a bar): Gbmaj9 | Fm7 | Ebm9 | Ab13sus (IV iii ii V), turning
# home to Db for the full section


def chord_at(bar):
    if 41 <= bar <= 44:                                   # the breakdown settles at home for 4 bars, then turns
        return BRIDGE[bar - 41]
    return CHORDS[((bar - 1) // 2) % 4]


def wind_up(a, z):
    """THE WIND-UP (the intro, answering the wind-down Harry liked): the key is turned and the box comes up to speed:
    bar by bar the gears' cycles shorten (toy 10..5, box 17..7, crystal 8..4 sixteenths) and the pitches rise from
    three semitones flat to true, the notes swelling."""
    k = j = 0
    span = z - a
    for bar in range(a, z + 1):
        n = z - bar                                             # 3, 2, 1, 0: how far from speed
        lo, hi = b0(bar), b0(bar + 1)
        sag, fade = -((n * 3 + 2) // 3), 6 * n
        if bar >= 2:
            for x in range(lo, hi, 5 + n + (n > 1)):
                P["toy"].add(x, 1.6 + n * 0.4, nm(TOY_SEQ[k % len(TOY_SEQ)] + sag), 62 - fade)
                k += 1
        for x in range(lo, hi, 7 + 3 * n):
            P["box"].add(x, 1.8 + n * 0.5, nm(BOX_SEQ[j % len(BOX_SEQ)] + sag), 58 - fade)
            j += 1


def stall(bar):
    """THE NEAR-STALL (the glitch break's last bar, a hint of the ending mid-song): the hail stops, the gears slow and
    sag fast within the bar (gaps widening, pitch falling a tone), and the beat drops out after beat 2; then the return
    snaps back at speed, as if the key got another turn."""
    x, gap, i = b0(bar), 2.0, 0
    while x < b0(bar) + 13:
        P["toy"].add(x, gap * 0.8, nm(TOY_SEQ[i % len(TOY_SEQ)] - (i // 2)), 70 - 5 * i)
        P["box"].add(x + gap / 2, gap * 0.8, nm(BOX_SEQ[i % len(BOX_SEQ)] - (i // 2) - 1), 62 - 5 * i)
        x += gap
        gap *= 1.35
        i += 1


def wind_down(a, z, toy_on, box_on, k, j):
    """THE WIND-DOWN: the music box runs down. Bar by bar each gear's cycle lengthens (toy 5..10, box 7..17, crystal
    4..9 sixteenths), the pitches sag a semitone every two bars as the mechanism slows, and the notes fade; the last
    sound is one sagging music-box note."""
    for bar in range(a, z + 1):
        n = bar - a
        lo, hi = b0(bar), b0(bar + 1)
        sag, fade = -(n // 2), 6 * n
        for x in range(lo, hi, 5 + n):
            pch = TOY_SEQ[k % len(TOY_SEQ)] + sag
            P["toy"].add(x, 1.6 + n * 0.4, nm(pch), 64 - fade)
            toy_on[x] = pch
            k += 1
        for x in range(lo, hi, 7 + 2 * n):
            pch = BOX_SEQ[j % len(BOX_SEQ)] + sag
            P["box"].add(x, 1.8 + n * 0.5, nm(pch), 60 - fade)
            box_on[x] = pch
            j += 1
        if bar < z:
            root, iv = chord_at(bar)
            for q, x in enumerate(range(lo, hi, 4 + n)):
                P["xtal"].add(x, 3, nm(68 + ((root + iv[q % len(iv)] - 8) % 12) + sag), 54 - fade)
    P["box"].add(b0(z) + 6, 10, nm(BOX_SEQ[0] - 3), 40)                  # the last, sagging note
    return k, j


GEARS = {"return": (6, 7, 4), "full": (5, 7, 9)}   # (toy, box, crystal) cycles by section; else (5, 7, 4)


def gear(sec):
    return GEARS.get(sec, (5, 7, 4))


def clockwork():
    """The three gears, mechanically straight; each section decides which gears turn and at what ratio (the GEAR
    CHANGE: the return turns the toy to a 6, a dotted-eighth hemiola against the box's 7; the full section puts the
    crystal on a 9, three odd gears). Returns the onsets for the hidden melody (toy and box coinciding)."""
    toy_on, box_on, xtal_full = {}, {}, {}
    k = j = 0
    for name, a, z in SECTIONS:
        lo, hi = b0(a), b0(z + 1)
        tl, bl, xl = gear(name)
        if name == "outro":
            k, j = wind_down(a, z, toy_on, box_on, k, j)
            continue
        if name == "intro":
            wind_up(1, 4)
            lo = b0(5)                                          # the gears run at speed from bar 5
        for x in range(lo, hi, tl):
            for o in ((0, 3) if tl == 5 else (0, 3) if tl == 6 else (0,)):
                st = x + o
                if st >= hi:
                    continue
                bar = st // S + 1
                if (name == "intro" and bar < 5) or (name == "outro" and bar >= 54) or name == "glitch":
                    k += 1
                    continue
                pch = TOY_SEQ[k % len(TOY_SEQ)]
                v = (58 if name in ("intro", "breakdown") else 66) + (8 if o == 0 else 0)
                P["toy"].add(st, 1.6, nm(pch), v)
                toy_on[st] = pch
                k += 1
        for x in range(lo, hi, bl):
            for o in (0, 2, 4):
                st = x + o
                if st >= hi:
                    continue
                bar = st // S + 1
                if (name == "intro" and bar < 3) or (name == "outro" and bar >= 56) or name == "glitch":
                    j += 1
                    continue
                pch = BOX_SEQ[j % len(BOX_SEQ)]
                P["box"].add(st, 1.8, nm(pch), (54 if name in ("intro", "breakdown") else 62) + (6 if o == 0 else 0))
                box_on[st] = pch
                j += 1
        q = 0
        for x in range(lo, hi, xl):                             # the crystal: chord tones on its own gear
            bar = x // S + 1
            if bar == BARS:
                continue
            root, iv = chord_at(bar)
            m = 68 + ((root + iv[q % len(iv)] - 8) % 12)
            P["xtal"].add(x, 3, nm(m), 52 if name in ("intro", "breakdown") else 58)
            if name in ("full", "return"):
                xtal_full[x] = m
            q += 1
    return sorted(set(toy_on) & set(box_on)), toy_on, box_on, xtal_full


def descant(box_on, xtal_full):
    """THE SECOND HIDDEN MELODY (the return and the full section): where the music box's 7 meets the crystal's gear, a soft voice under
    the first melody sings the box's note an octave down and holds to the next meeting: two tunes made by the gears."""
    meet = sorted(set(box_on) & set(xtal_full))
    for i, st in enumerate(meet):
        nxt = meet[i + 1] if i + 1 < len(meet) else st + 12
        P["desc"].add(st, min(nxt - st, 16) * 0.95, nm(box_on[st] - 12), 60)
    return len(meet)


def melody(coinc, toy_on):
    """THE HIDDEN MELODY: a tape lead on every toy/box coincidence, held to the next, an octave under the toy."""
    for i, st in enumerate(coinc):
        sec = sec_of(st // S + 1)
        if sec not in ("melody", "return", "full", "breakdown"):
            continue
        nxt = coinc[i + 1] if i + 1 < len(coinc) else st + 8
        up = 12 if sec in ("return", "full") else 0
        # the hidden melody CHANGES VOICE by section: the tape lead, but in the return a barking Rhodes (epiano-tine)
        dest = "rlead" if sec == "return" else "lead"
        vel = 70 if sec != "breakdown" else 56
        P[dest].add(st, min(nxt - st, 12) * 0.95, nm(toy_on[st] - 12 + up - (12 if dest == "rlead" else 0)),
                    vel + (16 if dest == "rlead" else 0))
        if b0(49) <= st < b0(53):
            # THE BOX SINGS: the last four bars before the wind-down, the music box itself plays the tune its gears
            # have been making all along, an octave above the lead, clear in its own voice; then it runs down
            P["boxsong"].add(st, min(nxt - st, 12) * 0.95, nm(toy_on[st] + 12), 76)


KICKS = [[0, 10], [0, 7, 10], [0, 3, 10], [0, 9, 11], [0, 10, 14], [0, 6, 10]]


def beat():
    for bar in range(1, BARS + 1):
        sec = sec_of(bar)
        if sec in ("intro", "breakdown") or bar > 54:
            continue
        a = b0(bar)
        soft = sec == "beat"
        if bar == 28:                                           # the stall: two beats, then nothing
            P["kick"].add(a, 1, "k", 96)
            P["throw"].add(a + 4, 1, "s", 96)                   # the last snare before the stop: a DUB THROW
            P["hat"].add(a + swing(2), 0.5, "h", 52)
            continue
        # THE RESAMPLED BREAK: bars 24-27 play through the CHOP tracks (wM's MPC-style chop): bar 24 feeds it live,
        # then the break's beat is cut from its own last bar, slices repeated, reversed and dropped
        K, SN, H = ("ckick", "csnare", "chat") if 24 <= bar <= 27 else ("kick", "snare", "hat")
        for k in KICKS[(bar * 5) % len(KICKS)]:
            P[K].add(a + swing(k), 1, "k", (84 if soft else 100) - (10 if k else 0))
        if not soft:
            for s in (4, 12):
                P[SN].add(a + s, 1, "s", 92 + rng.randint(-6, 4))                # dragged late by the kit's nudge
            if rng.random() < 0.6:
                P[SN].add(a + swing(rng.choice([7, 11, 15])), 0.5, "rs", 44 + rng.randint(0, 12))
        for e in range(0, 16, 1 if sec in ("full", "return") else 2):
            if rng.random() < 0.12:
                continue                                                         # a dropped hat
            P[H].add(a + swing(e), 0.5, "h", (64 if e % 4 == 0 else 46) + rng.randint(-6, 6))
        if sec == "glitch":                                                      # HAIL: rolls and retriggers
            for j in range(8):
                P[SN].add(a + 12 + j * 0.5, 0.5, "s", 50 + 8 * j)
        if sec == "full" and bar % 2 == 0:
            for e in range(0, 16, 2):
                P["perc"].add(a + swing(e + 1), 0.5, "sh", 44 + rng.randint(0, 10))


def glitch_hail():
    """The break: the toys are torn into hail: single notes retriggered as 32nds, falling."""
    a, z = b0(25), b0(28)                                      # bar 28 is the near-stall
    stall(28)
    x = a
    i = 0
    while x < z:
        p = TOY_SEQ[i % len(TOY_SEQ)] + (12 if i % 3 == 0 else 0)
        n = rng.choice([3, 4, 6])
        for j in range(n):
            P["hail"].add(x + j * 0.5, 0.45, nm(p - j), 70 - 4 * j)      # HAIL ON METAL: through a comb on Db
        P["box"].add(x + n * 0.5 + 1, 1.5, nm(BOX_SEQ[i % len(BOX_SEQ)]), 58)
        x += rng.choice([5, 7, 4])
        i += 1


TOY_CHOP = {"type": "chop", "slices": 8, "pattern": "0 . 2 r2 4 . 6 r7", "length": "1/1", "mix": 1}


def chop_toys():
    """The full section's phrase ends (bars 48 and 52) RESAMPLE THE MUSIC BOX: the toy piano and the box play bars
    47-48 and 51-52 through their own chop, the first bar feeding it live, the second cut from it (live slices,
    repeats, reversals), so the clockwork stutters on itself where the phrases turn."""
    spans = [(b0(47), b0(49)), (b0(51), b0(53))]
    for src in ("toy", "box"):
        keep, moved = [], []
        for e in P[src].ev:
            (moved if any(a <= e[0] < z for a, z in spans) else keep).append(e)
        P[src].ev = keep
        P["c" + src].ev.extend(moved)


def vox_chops():
    """THE VOX CHOP (the melody section, returning with it in the return and the full section): a lo-fi vocal-chop
    answer at the end of every second bar: two
    short sung chops, the chord's fifth falling to its third, on the and-of-3 and on 4, each its own vowel."""
    for bar in list(range(18, 25, 2)) + list(range(30, 37, 2)) + list(range(46, 53, 2)):   # born with the melody
        root, iv = chord_at(bar)
        fifth = 68 + ((root + iv[2] - 8) % 12)
        third = 68 + ((root + iv[1] - 8) % 12)
        third = third if third < fifth else third - 12
        P["vox"].add(b0(bar) + swing(10), 1.6, nm(fifth), 74)
        P["vox"].add(b0(bar) + 12, 2.6, nm(third), 70)


def mist():
    """THE MIST (the breakdown): the music box's notes also feed a granular CLOUD (wM's), smeared into a shimmering bed
    under the bridge and the counter-line: after the break's hail, the breakdown's hail turns to mist."""
    for e in P["box"].ev:
        if b0(37) <= e[0] < b0(45):
            P["mist"].add(e[0], 6, e[2], e[3])


def squelch():
    """The full section's SQUELCH: the bass line doubled through chirper-two's ladder filter, resonant, its cutoff swept
    by a slow LFO, for the last big section only."""
    for st, ln, head, vel in list(P["bass"].ev):
        if b0(45) <= st < b0(53):
            P["sq"].add(st, ln, head, vel - 6)


def counter_line():
    """The breakdown's COUNTER-MELODY: an electric piano (wM's tine pickup: clean soft, barking when pressed through the
    bridge) walking the chords' guide tones in half notes (the third, then the
    seventh), voice-led to the nearest, answering the soft hidden melody while the beat is out."""
    prev = 65
    for bar in range(37, 45):
        root, iv = chord_at(bar)
        for h, deg in enumerate((iv[1], iv[3])):
            pc = (root + deg) % 12
            cands = [m for m in range(58, 76) if m % 12 == pc]
            m = min(cands, key=lambda c: abs(c - prev))
            lean = 20 if bar >= 41 else 0                     # leaning in through the bridge: the tine starts to bark
            P["cpiano"].add(b0(bar) + 8 * h, 7.5, nm(m), 62 + (4 if h == 0 else 0) + lean)
            prev = m


def chord_spans():
    """(bar, bars) per chord: two bars each, one bar each through the bridge (bars 41-44)."""
    out, bar = [], 1
    while bar <= BARS:
        n = 1 if 41 <= bar <= 44 else 2
        out.append((bar, n))
        bar += n
    return out


def harmony():
    for bar, n in chord_spans():
        root, iv = chord_at(bar)
        sec = sec_of(bar)
        if bar >= 5:
            voic = sorted({56 + ((root + x - 8) % 12) for x in iv})
            P["pad"].add(b0(bar), n * S - 0.5, ",".join(nm(m) for m in voic), 56 if sec in ("intro", "breakdown") else 62)
        if sec not in ("intro", "glitch") and bar < 57:
            r = 37 + ((root - 1) % 12)
            nxt = 37 + ((chord_at(bar + n)[0] - 1) % 12)
            ans = r + (7 if (bar // 2) % 2 == 0 else 14)            # the fifth, or the ninth up high
            last = b0(bar) + (n - 1) * S                              # the chord's last bar
            P["bass"].add(b0(bar), 10, nm(r), 86)                    # the root...
            P["bass"].add(b0(bar) + swing(11), 3 if n == 2 else 1.5, nm(ans), 72)   # ...answered on the swung and-of-3...
            if n == 2:
                P["bass"].add(last, 12, nm(r), 80)
            P["bass"].add(last + swing(13), 1.2, nm(nxt + 2), 66)    # ...then a walk down into the next chord
            P["bass"].add(last + swing(15), 1.0, nm(nxt + 1), 70)
            P["sub"].add(b0(bar), n * S - 1, nm(r - 12), 90)          # the warm floor an octave under the bass


def wear_lane():
    """THE TAPE WEARS (wM's deck warp, 0..2, a multiplier on wow and flutter): normal through most of the song, rough in
    the glitch break, clean and close in the breakdown, and wearing out (1 -> 2) as the music box runs down."""
    sec = lambda e: e / 4 * 60 / BPM
    pts = [(0, 1.0), (b0(25) - 2, 1.0), (b0(25), 1.6), (b0(29) - 2, 1.6), (b0(29), 1.0), (b0(37) - 2, 1.0),
           (b0(37), 0.7), (b0(45) - 2, 0.7), (b0(45), 1.0), (b0(53), 1.0), (TOTAL, 2.0)]
    return [[f"{sec(e):.3f}s", v] for e, v in pts]


def tapestop_lane():
    """The tape stops in the near-stall's second half (after the resample dive) and spins back up into the return."""
    sec = lambda e: e / 4 * 60 / BPM
    pts = [(0, 0.0), (b0(28) + 7, 0.0), (b0(28) + 7.1, 1.0), (b0(28) + 11.9, 1.0), (b0(28) + 12, 0.0), (TOTAL, 0.0)]
    # stop just before beat 2-and-a-half, release on beat 4: the 1-beat spin-up lands on the return's downbeat
    # (a final stop at the very end was tried: it silenced the join into t5, flow 50 -> 27; the wind-down ends it)
    return [[f"{sec(e):.3f}s", v] for e, v in pts]


def resample_lane():
    """The whole band dives like a slowed sampler: 4 semitones over the near-stall's first half, snapping back at the
    return; and a slow sag through the wind-down. Before the tape and vinyl, so the record's hiss stays steady."""
    sec = lambda e: e / 4 * 60 / BPM
    pts = [(0, 0.0), (b0(28) - 0.5, 0.0), (b0(28) + 8, 1.0), (b0(29) - 0.6, 1.0), (b0(29), 0.0),
           (b0(53), 0.0), (TOTAL, 1.0)]
    return [[f"{sec(e):.3f}s", v] for e, v in pts]


def voiced(base, spread, lp, lp_var):
    """A per-voice variant (chirper-two's synth.fx): every note pans to its own random place and gets its own tone."""
    return {"extends": base, "synth": {"fx": [
        {"type": "pan", "pan": {"value": 0, "mod": [{"src": "rand", "amount": spread}]}},
        {"type": "filter", "kind": "lp", "cutoff": {"value": lp, "mod": [{"src": "rand", "amount": lp_var}]}}]}}


# LIVING TINES (the gears: no two notes quite alike) and SCATTERED HAIL (every stone lands somewhere else)
VOICED = {"c4-toy": voiced("toy-piano", 0.45, 7000, 3000), "c4-box": voiced("music-box", 0.45, 7000, 3000),
          "c4-hail": voiced("toy-piano", 1.0, 5000, 3500),
          # the VOX CHOP: a tape lead sung through a per-voice formant, each chop its own vowel around 'ah'
          "c4-vox": {"extends": "lead-tape", "synth": {"fx": [
              {"type": "formant", "vowel": {"value": 0.5, "mod": [{"src": "rand", "amount": 0.35}]}, "q": 8, "mix": 1}]}}}

BREATHE = {"type": "pump", "on": "kick", "depth": "-9dB", "attack": "5ms", "release": "450ms", "curve": 0.5}
# THE BREATH: wM's pump keyed on every kick, released over ~65% of a beat with a gentle curve (chirp-eco's recipe:
# the default swell recovers so fast it averages to ~-0.7 dB; v15-v20's quarter grid barely breathed)

CHOP = {"type": "chop", "slices": 8, "pattern": "0 0 r3 2 . 5 r7 _", "length": "1/1", "mix": 1}   # wM's resampler

# wM's lo-fi toolkit (bd-9ef6a7): Dilla-ish wonk on the kit, a late snare and an early kick, each bar its own swing
KIT = ("lofi-kit play.humanize.nudge.s=22ms play.humanize.nudge.k=-8ms play.humanize.swing_drift=0.04 "
       "play.humanize.drunk=4ms play.humanize.drift=5ms")       # drift works now (wM): the kit wanders over bars


def main():
    coinc, toy_on, box_on, xtal_full = clockwork()
    melody(coinc, toy_on)
    n_desc = descant(box_on, xtal_full)
    beat()
    glitch_hail()
    harmony()
    counter_line()
    squelch()
    mist()
    vox_chops()
    chop_toys()
    sec = lambda e: e / 4 * 60 / BPM
    tr = lambda name, patch, **kw: dict({"name": name, "patch": patch, "score": P[name].score()}, **kw)
    tracks = [
        tr("toy", "c4-toy", pan="L35", gain="-6dB", out="toys"),
        tr("box", "c4-box", pan="R35", gain="-6dB", out="toys"),
        tr("ctoy", "c4-toy", pan="L35", gain="-6dB", out="toys", fx=[TOY_CHOP]),      # the resampled music box
        tr("cbox", "c4-box", pan="R35", gain="-6dB", out="toys", fx=[TOY_CHOP]),
        tr("xtal", "fb-crystal", pan="R10", gain="-24dB", out="toys"),
        tr("lead", "lead-tape", pan="L10", gain="-9dB", sends={"space": "-10dB"}),
        tr("rlead", "epiano-tine synth.tine.sense=0.5 synth.tine.key=-0.25", pan="L10", gain="-4dB", sends={"space": "-9dB", "echo": "-14dB"},   # the return's
           fx=["tape wow=10 flutter=2 seed=17"]),                                        # hidden melody, on a barking Rhodes
        tr("boxsong", "c4-box", pan="R15", gain="2dB", sends={"space": "-9dB"}),          # THE BOX SINGS (bars 49-52)
        tr("hail", "c4-hail", pan="C", gain="4dB", out="toys", fx=["comb cutoff=138.6 q=6"]),   # hail on a metal roof
        tr("desc", "boc-lead", pan="R20", gain="-4dB", sends={"space": "-9dB"}),     # the second hidden melody
        tr("vox", "c4-vox", pan="L15", gain="-4dB", sends={"space": "-7dB", "echo": "-4dB"},
           fx=[{"type": "tape", "wow": 10, "flutter": 2, "seed": 9}]),                  # the VOX CHOP answers
        tr("mist", "music-box", gain="-6dB", sends={"space": "-6dB"},                   # the MIST: hail into grains
           fx=[{"type": "cloud", "size": "150ms", "density": 18, "position": "500ms", "spray": "400ms", "pitch": 12,
                "scatter": 0.2, "reverse": 0.4, "spread": 0.9, "mix": 0.85, "seed": 3}]),
        tr("cpiano", "epiano-tine synth.tine.sense=0.5 synth.tine.key=-0.25", pan="L30", gain="-6dB", sends={"space": "-9dB"},     # the breakdown's counter-line,
           fx=["tape wow=8 flutter=2 seed=13"]),                                         # on wM's tine pickup
        tr("pad", "juno-pad", gain="-14dB", fx=["lp cutoff=2200", "tape wow=9 flutter=2 seed=11", BREATHE],
           sends={"space": "-8dB"}),                                                    # the pad BREATHES with the kick
        tr("bass", "analog-bass", gain="0dB"),
        tr("sub", "sub", gain="-4dB", fx=[BREATHE]),
        tr("sq", "analog-bass", gain="-10dB", pan="R15", lfo={"sw": {"wave": "sine", "rate": "1/2"}},     # the SQUELCH
           fx=[{"type": "filter", "kind": "ladder", "cutoff": {"value": 700, "mod": [{"src": "lfo.sw", "amount": 500}]}, "q": 12}]),
        tr("kick", KIT, out="drums", gain="4dB"),
        tr("snare", KIT, out="drums"),
        tr("hat", KIT, out="drums", gain="-6dB"),
        tr("perc", KIT, out="drums", gain="-8dB"),
        tr("throw", KIT, out="drums", gain="2dB", sends={"echo": "0dB"}),   # the stall's snare, thrown into the dub echo,
        # whose repeats are then caught by the master's tape stop: they slow, sag and die with the tape
        *[tr(n, KIT, out="drums", gain=g, fx=[CHOP]) for n, g in (("ckick", "4dB"), ("csnare", "0dB"), ("chat", "-6dB"))],
    ]
    head = [
        'about: "Chirpers - Tape Weather, track 4: Hail on a Music Box (chirper-three). Glitchy IDM-lite: a broken music box in a lo-fi beat; toy cycles of 5, 7 and 4 sixteenths, a melody made where the gears coincide, a hand-played swung beat that stutters. Generated by compose/chirpers3/src/chirpers3-t4.py."',
        f"tempo: {BPM}",
        'tail: "2.5s"',
        'ceiling: "-0.5dB"',
        "patches: " + json.dumps(VOICED),
        "buses:",
        '  toys: {fx: [' + ", ".join(json.dumps(f) for f in [
            {"type": "tape", "wow": 14, "flutter": 3, "drift": 1, "tone": "8kHz", "sweep": 0.6, "squash": 0.3,
             "hiss": "-62dB", "seed": 4, "warp": {"value": 0, "mod": [{"src": "auto.wear", "amount": 1}]}},  # the wow, worn
            {"type": "crush", "bits": 10, "rate": 22000, "mix": 0.3},
            {"type": "stutter", "slice": "1/32", "repeats": 4, "chance": 0.07, "seed": 41},
            "lp cutoff=10k", "reverb kind=room decay=1.4s mix=0.18 predelay=10ms"]) + '], auto: '
        + json.dumps({"wear": {"points": wear_lane()}}) + '}',
        '  drums: {fx: [' + ", ".join(json.dumps(f) for f in [
            {"type": "stutter", "slice": "1/16", "repeats": 3, "chance": 0.08, "seed": 7},
            "lp cutoff=10k", {"type": "tape", "drive": 0.35, "warmth": 0.5, "mix": 1},
            {"type": "compressor", "threshold": "-18dB", "ratio": 3, "attack": "8ms", "release": "120ms", "makeup": "3dB"}]) + ']}',
        '  space: {fx: ["reverb kind=hall decay=3.2s mix=1 predelay=30ms mono_below=200hz shimmer=0.25"]}',   # a halo
        # THE DUB ECHO (chirper-two's feedback routing): the bus hears itself a dotted eighth ago through a band-pass and a
        # tape deck, so every repeat comes back darker and more worn (gain .55: it dies away)
        '  echo: ' + json.dumps({"fx": ["hp cutoff=350", "lp cutoff=2600",
                                         {"type": "tape", "wow": 12, "flutter": 3, "drive": 0.3, "seed": 6}],
                                  "returns": [{"from": "echo", "gain": 0.55, "time": f"{3 * 60 / BPM / 4 * 1000:.0f}ms"}]}),
        'master: ' + json.dumps({"fx": [{"type": "pitch", "semitones": {"value": 0, "mod": [{"src": "auto.rs", "amount": -4}]},
                                        "mix": 1},       # the RESAMPLE: the whole band slows like a sampler (Harry's note)
                                       {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.fi", "amount": 1}]}},
                                       # THE NEEDLE DROPS: the song fades in out of t3's quiet ending (in-join was 22 dB)
                                       {"type": "filter", "kind": "lp",
                                        "cutoff": {"value": 18000, "mod": [{"src": "auto.op", "amount": -16500}]}},
                                       # ...muffled at first (1.5 kHz), opening as the box comes up to speed (bars 1-4)
                                       {"type": "tapestop", "stop": {"value": 0, "mod": [{"src": "auto.ts", "amount": 1}]},
                                        "time": "1b", "up": "1b", "curve": 0.5, "mix": 1},   # the tape STOPS (holding,
                                       # then dropping), and SPINS BACK UP into the return (the record keeps turning)
                                       {"type": "tape", "drive": 0.25, "mix": 0.5, "squash": 0.4, "hiss": "-56dB", "wow": 4,
                                        "flutter": 1, "seed": 7,
                                        "warp": {"value": 0.5, "mod": [{"src": "auto.wear", "amount": 0.5}]}},
                                       "vinyl crackle=0.4 dust=0.35 noise=-62dB rumble=0.3 warp=5 wear=0.4 seed=5",
                                       {"type": "eq", "bands": [{"kind": "peak", "cutoff": 600, "gain": "-3dB", "q": 0.8}]},
                                       "glue threshold=-24dB ratio=3 attack=15ms release=200ms makeup=3dB",
                                       {"type": "gain", "gain": "11dB"}],
                                "auto": {"rs": {"points": resample_lane()}, "ts": {"points": tapestop_lane()},
                                         "fi": {"points": [["0s", -20.0], [f"{2 * S / 4 * 60 / BPM:.3f}s", 0.0]]},
                                         "op": {"points": [["0s", 1.0], [f"{1 * S / 4 * 60 / BPM:.3f}s", 0.85],
                                                           [f"{4 * S / 4 * 60 / BPM:.3f}s", 0.0]]},
                                         "wear": {"points": wear_lane()}}}),
        "tracks:",
    ]
    with open(OUT, "w") as f:
        f.write("\n".join(head) + "\n")
        for d in tracks:
            f.write("  - " + json.dumps(d) + "\n")
    print(f"wrote {OUT}: {BARS} bars, {sec(TOTAL):.0f} s; {len(coinc)} gear coincidences, {n_desc} for the descant")


if __name__ == "__main__":
    main()
