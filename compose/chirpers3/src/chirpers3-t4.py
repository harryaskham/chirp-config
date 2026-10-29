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
- GLITCHES: probabilistic stutter on the toy and drum buses, plus composed HAIL (a toy note retriggered as 32nds)
  in the break.
- HARMONY: Dbmaj9 | Cm7(11) | Fm9 | Bbm9, two bars each; wM's tape deck (wow, flutter, hiss) on the toys, the pad
  and the master, his vinyl (crackle, dust, warp) on the master; the kit's wonk from play.humanize (late snare,
  early kick, swing drift).
- THE GEAR CHANGE: the return turns the toy to a 6 against the box's 7 (a dotted-eighth hemiola); the full section
  puts the crystal on a 9, three odd gears; so the hidden melody's rhythm changes section by section.
- FORM (58 bars, 86 bpm): intro (toys enter one by one), beat, melody, glitch break, return, breakdown, full, and
  the WIND-DOWN (the music box runs down: gears lengthen, pitches sag, the beat gives out).
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


P = {k: Part() for k in ("toy", "box", "xtal", "lead", "pad", "bass", "sub", "kick", "snare", "hat", "perc")}
rng = random.Random(4)


def chord_at(bar):
    return CHORDS[((bar - 1) // 2) % 4]


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
    toy_on, box_on = {}, {}
    k = j = 0
    for name, a, z in SECTIONS:
        lo, hi = b0(a), b0(z + 1)
        tl, bl, xl = gear(name)
        if name == "outro":
            windup = wind_down(a, z, toy_on, box_on, k, j)
            k, j = windup
            continue
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
            q += 1
    return sorted(set(toy_on) & set(box_on)), toy_on


def melody(coinc, toy_on):
    """THE HIDDEN MELODY: a tape lead on every toy/box coincidence, held to the next, an octave under the toy."""
    for i, st in enumerate(coinc):
        sec = sec_of(st // S + 1)
        if sec not in ("melody", "return", "full", "breakdown"):
            continue
        nxt = coinc[i + 1] if i + 1 < len(coinc) else st + 8
        up = 12 if sec in ("return", "full") else 0
        P["lead"].add(st, min(nxt - st, 12) * 0.95, nm(toy_on[st] - 12 + up), 70 if sec != "breakdown" else 56)


KICKS = [[0, 10], [0, 7, 10], [0, 3, 10], [0, 9, 11], [0, 10, 14], [0, 6, 10]]


def beat():
    for bar in range(1, BARS + 1):
        sec = sec_of(bar)
        if sec in ("intro", "breakdown") or bar > 54:
            continue
        a = b0(bar)
        soft = sec == "beat"
        for k in KICKS[(bar * 5) % len(KICKS)]:
            P["kick"].add(a + swing(k), 1, "k", (84 if soft else 100) - (10 if k else 0))
        if not soft:
            for s in (4, 12):
                P["snare"].add(a + s, 1, "s", 92 + rng.randint(-6, 4))            # dragged late by the kit's nudge
            if rng.random() < 0.6:
                P["snare"].add(a + swing(rng.choice([7, 11, 15])), 0.5, "rs", 44 + rng.randint(0, 12))
        for e in range(0, 16, 1 if sec in ("full", "return") else 2):
            if rng.random() < 0.12:
                continue                                                         # a dropped hat
            P["hat"].add(a + swing(e), 0.5, "h", (64 if e % 4 == 0 else 46) + rng.randint(-6, 6))
        if sec == "glitch":                                                      # HAIL: rolls and retriggers
            for j in range(8):
                P["snare"].add(a + 12 + j * 0.5, 0.5, "s", 50 + 8 * j)
        if sec == "full" and bar % 2 == 0:
            for e in range(0, 16, 2):
                P["perc"].add(a + swing(e + 1), 0.5, "sh", 44 + rng.randint(0, 10))


def glitch_hail():
    """The break: the toys are torn into hail: single notes retriggered as 32nds, falling."""
    a, z = b0(25), b0(29)
    x = a
    i = 0
    while x < z:
        p = TOY_SEQ[i % len(TOY_SEQ)] + (12 if i % 3 == 0 else 0)
        n = rng.choice([3, 4, 6])
        for j in range(n):
            P["toy"].add(x + j * 0.5, 0.45, nm(p - j), 70 - 4 * j)
        P["box"].add(x + n * 0.5 + 1, 1.5, nm(BOX_SEQ[i % len(BOX_SEQ)]), 58)
        x += rng.choice([5, 7, 4])
        i += 1


def harmony():
    for bar in range(1, BARS + 1, 2):
        root, iv = chord_at(bar)
        sec = sec_of(bar)
        if bar >= 5:
            voic = sorted({56 + ((root + x - 8) % 12) for x in iv})
            P["pad"].add(b0(bar), 2 * S - 0.5, ",".join(nm(m) for m in voic), 56 if sec in ("intro", "breakdown") else 62)
        if sec not in ("intro", "glitch") and bar < 57:
            r = 37 + ((root - 1) % 12)
            nxt = 37 + ((chord_at(bar + 2)[0] - 1) % 12)
            ans = r + (7 if (bar // 2) % 2 == 0 else 14)            # the fifth, or the ninth up high
            P["bass"].add(b0(bar), 10, nm(r), 86)                    # the root...
            P["bass"].add(b0(bar) + swing(11), 3, nm(ans), 72)        # ...answered on the swung and-of-3...
            P["bass"].add(b0(bar) + S, 12, nm(r), 80)
            P["bass"].add(b0(bar) + S + swing(13), 1.2, nm(nxt + 2), 66)   # ...then a walk down into the next chord
            P["bass"].add(b0(bar) + S + swing(15), 1.0, nm(nxt + 1), 70)
            P["sub"].add(b0(bar), 2 * S - 1, nm(r - 12), 90)          # the warm floor an octave under the bass


# wM's lo-fi toolkit (bd-9ef6a7): Dilla-ish wonk on the kit, a late snare and an early kick, each bar its own swing
KIT = ("lofi-kit play.humanize.nudge.s=22ms play.humanize.nudge.k=-8ms play.humanize.swing_drift=0.04 "
       "play.humanize.drunk=4ms")


def main():
    coinc, toy_on = clockwork()
    melody(coinc, toy_on)
    beat()
    glitch_hail()
    harmony()
    sec = lambda e: e / 4 * 60 / BPM
    tr = lambda name, patch, **kw: dict({"name": name, "patch": patch, "score": P[name].score()}, **kw)
    tracks = [
        tr("toy", "toy-piano", pan="L35", gain="-6dB", out="toys"),
        tr("box", "music-box", pan="R35", gain="-6dB", out="toys"),
        tr("xtal", "fb-crystal", pan="R10", gain="-24dB", out="toys"),
        tr("lead", "lead-tape", pan="L10", gain="-9dB", sends={"space": "-10dB"}),
        tr("pad", "juno-pad", gain="-14dB", fx=["lp cutoff=2200", "tape wow=9 flutter=2 seed=11"], sends={"space": "-8dB"}),
        tr("bass", "analog-bass", gain="0dB"),
        tr("sub", "sub", gain="-4dB"),
        tr("kick", KIT, out="drums", gain="4dB"),
        tr("snare", KIT, out="drums"),
        tr("hat", KIT, out="drums", gain="-6dB"),
        tr("perc", KIT, out="drums", gain="-8dB"),
    ]
    head = [
        'about: "Chirpers - Tape Weather, track 4: Hail on a Music Box (chirper-three). Glitchy IDM-lite: a broken music box in a lo-fi beat; toy cycles of 5, 7 and 4 sixteenths, a melody made where the gears coincide, a hand-played swung beat that stutters. Generated by compose/chirpers3/src/chirpers3-t4.py."',
        f"tempo: {BPM}",
        'tail: "2.5s"',
        'ceiling: "-0.5dB"',
        "buses:",
        '  toys: {fx: [' + ", ".join(json.dumps(f) for f in [
            "tape wow=14 flutter=3 drift=1 tone=8kHz sweep=0.6 squash=0.3 hiss=-62dB seed=4",   # the wow (wM's deck)
            {"type": "crush", "bits": 10, "rate": 22000, "mix": 0.3},
            {"type": "stutter", "slice": "1/32", "repeats": 4, "chance": 0.07, "seed": 41},
            "lp cutoff=10k", "reverb kind=room decay=1.4s mix=0.18 predelay=10ms"]) + ']}',
        '  drums: {fx: [' + ", ".join(json.dumps(f) for f in [
            {"type": "stutter", "slice": "1/16", "repeats": 3, "chance": 0.08, "seed": 7},
            "lp cutoff=10k", {"type": "tape", "drive": 0.35, "warmth": 0.5, "mix": 1},
            {"type": "compressor", "threshold": "-18dB", "ratio": 3, "attack": "8ms", "release": "120ms", "makeup": "3dB"}]) + ']}',
        '  space: {fx: ["reverb kind=hall decay=3.2s mix=1 predelay=30ms mono_below=200hz"]}',
        'master: ' + json.dumps({"fx": ["tape drive=0.25 mix=0.5 squash=0.4 hiss=-56dB wow=4 flutter=1 seed=7",
                                       "vinyl crackle=0.4 dust=0.35 noise=-62dB rumble=0.3 warp=5 wear=0.4 seed=5",
                                       {"type": "eq", "bands": [{"kind": "peak", "cutoff": 600, "gain": "-3dB", "q": 0.8}]},
                                       "glue threshold=-24dB ratio=3 attack=15ms release=200ms makeup=3dB",
                                       {"type": "gain", "gain": "11dB"}]}),
        "tracks:",
    ]
    with open(OUT, "w") as f:
        f.write("\n".join(head) + "\n")
        for d in tracks:
            f.write("  - " + json.dumps(d) + "\n")
    print(f"wrote {OUT}: {BARS} bars, {sec(TOTAL):.0f} s; {len(coinc)} gear coincidences")


if __name__ == "__main__":
    main()
