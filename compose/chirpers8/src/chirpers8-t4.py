#!/usr/bin/env python3
"""chirpers - A Light Left On (chirpers VIII), track 4 (chirper-three): SORTING HOUSE.

Acid electro in which a melody PUTS ITSELF IN ORDER. Sixteen notes - one bar of sixteenths - are an array; each section
a different SORTING ALGORITHM works on it, one step a bar, live: every COMPARISON is a hat tick at that position, every
SWAP a rim hit, every finished pass a crash. Bubble sort, insertion sort, quicksort (the pivot accented), a BOGOSORT
storm (random shuffles, glitching) and merge sort; sorted, the tune is a scale rising LEFT TO RIGHT - each note is panned
by its index in the array, so order appears in space as well as in pitch. Then it is shuffled again.

TUNING: the CARLOS ALPHA scale - steps of 77.965 cents with no octave (fifths and thirds sweet, fifteen steps a
slightly-wrong 1170-cent 'octave'), written as fractional MIDI. A machine tidying its room: small things before large.

FORM (176 bars, ~5:30, 128 bpm): intro 1-16 (the shuffled tune) | bubble 17-40 | insertion 41-64 | quicksort 65-88 |
bogosort 89-100 (the storm: no kick) | merge 101-124 | sorted 125-160 (the scale, then reversed) | outro 161-176
"""
import json
import math
import os
import random

OUT = os.environ.get("C8T4_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers8-t4.yaml")
BAR = 4.0
SECTIONS = [("intro", 1, 16), ("bubble", 17, 40), ("insertion", 41, 64), ("quick", 65, 88), ("bogo", 89, 100),
            ("merge", 101, 124), ("sorted", 125, 160), ("outro", 161, 176)]
BARS = SECTIONS[-1][2]
TOTAL = BARS * BAR
ALPHA = 0.77965                       # semitones per Carlos alpha step
BASE = 57                             # A3
N = 16


def b0(bar):
    return (bar - 1) * BAR


def sec_of(bar):
    for name, a, z in SECTIONS:
        if a <= bar <= z:
            return name
    return "outro"


def pitch(v, base=BASE):
    return f"m{base + v * ALPHA:.3f}"


# v12: SWING AS RELEASE - every sorting section is straight machine sixteenths; once the list is SORTED the work is
# done and the groove loosens: every off-beat sixteenth in every part lands later - 0.54, 0.58, then 0.62 of the
# eighth; straight again in the outro, where the list comes undone. Applied here, not with swing16 tokens: the
# engine swings rest tokens too, and these parts are written as notes plus short rests
SWING = [(125, 0.54), (133, 0.58), (141, 0.62), (161, 0.5)]


def swung(s):
    bar = int(s // 4) + 1
    sw = 0.5
    for b, v in SWING:
        if bar >= b:
            sw = v
    return s + (sw - 0.5) * 0.5 if abs(s % 0.5 - 0.25) < 1e-6 else s


class Part:
    def __init__(self):
        self.ev = []

    def add(self, at, ln, head, vel):
        self.ev.append((swung(at), ln, head, int(max(1, min(127, vel)))))    # v12: the sorted groove swings

    def score(self, total=TOTAL):
        ev = sorted(self.ev, key=lambda e: (e[0], -e[3]))
        toks, pos = [], 0.0
        for i, (s, ln, head, vel) in enumerate(ev):
            nxt = ev[i + 1][0] if i + 1 < len(ev) else total
            ln = min(ln, nxt - s)
            if ln <= 1e-6:
                continue
            if s - pos > 1e-5:
                toks.append(f"R/{s - pos:.5g}b")

            base, _, mods = head.partition("^")
            toks.append(f"{base}/{ln:.5g}b@{vel}" + (f"^{mods}" if mods else ""))
            pos = s + ln
        if total - pos > 1e-5:
            toks.append(f"R/{total - pos:.5g}b")
        return " ".join(toks) if toks else f"R/{total:g}b"


P = {}


def part(n):
    return P.setdefault(n, Part())


# ---------------------------------------------------------------- the algorithms, as per-bar step generators
# each yields (array_before, comparisons, swaps, accents) once per bar: positions are array indices 0..15
def bubble(a):
    a = a[:]
    while True:
        cmp, sw = [], []
        before = a[:]
        for j in range(N - 1):
            cmp.append(j)
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                sw.append(j)
        yield before, cmp, sw, []
        if not sw:
            while True:
                yield a[:], [], [], []


def insertion(a):
    a = a[:]
    for i in range(1, N):
        before = a[:]
        cmp, sw = [], []
        j = i
        while j > 0:
            cmp.append(j - 1)
            if a[j - 1] > a[j]:
                a[j - 1], a[j] = a[j], a[j - 1]
                sw.append(j - 1)
                j -= 1
            else:
                break
        yield before, cmp, sw, [i]
    while True:
        yield a[:], [], [], []


def quick(a):
    a = a[:]
    stack = [(0, N - 1)]
    while stack:
        lo, hi = stack.pop()
        if lo >= hi:
            continue
        before = a[:]
        p, i, cmp, sw = a[hi], lo, [], []
        for j in range(lo, hi):
            cmp.append(j)
            if a[j] < p:
                a[i], a[j] = a[j], a[i]
                if i != j:
                    sw.append(min(i, j))
                i += 1
        a[i], a[hi] = a[hi], a[i]
        sw.append(i)
        stack += [(lo, i - 1), (i + 1, hi)]
        yield before, cmp, sw, [hi]                 # the pivot accented
    while True:
        yield a[:], [], [], []


def bogo(a, rng):
    a = a[:]
    while True:
        before = a[:]
        rng.shuffle(a)
        yield before, list(range(N - 1)), list(range(0, N, 2)), []


def merge(a):
    a = a[:]
    w = 1
    while w < N:
        for lo in range(0, N, 2 * w):
            before = a[:]
            mid, hi = min(lo + w, N), min(lo + 2 * w, N)
            left, right = a[lo:mid], a[mid:hi]
            out, cmp = [], []
            i = j = 0
            while i < len(left) and j < len(right):
                cmp.append(lo + i + j)
                if left[i] <= right[j]:
                    out.append(left[i]); i += 1
                else:
                    out.append(right[j]); j += 1
            out += left[i:] + right[j:]
            sw = [lo + k for k in range(hi - lo) if a[lo + k] != out[k]]
            a[lo:hi] = out
            yield before, cmp, sw, [lo, mid]
        w *= 2
    while True:
        yield a[:], [], [], []


def resorting(make, arr, seed):
    """v2: when a sort finishes, the sorted scale sounds for one bar (a crash), then the array is reshuffled and the
    same algorithm starts again - the work never stops."""
    rng = random.Random(seed)
    while True:
        g = make(arr)
        while True:
            before, cmp, sw, acc = next(g)
            yield before, cmp, sw, acc
            if before == sorted(before):
                break
        arr = list(range(N))
        rng.shuffle(arr)


PROGRESS = []
# v16: THE LAST PHYSICAL FAMILIES - merge sort, the most graceful algorithm, sings its emerging tune on the physical
# alto sax (a reed on a conical bore) instead of the kalimba; and every finished pass (or finished sort) is marked by a
# modal CYMBAL (a dense struck plate set, its wash blooming in after the hit) instead of the drum machine's crash
CYMBAL = {"synth": {"layers": [{"type": "modal", "modes": "cymbal", "decay": "2.5s", "damp": 0.05, "bloom": 0.6,
                                "strike": 0.7}],
                    "amp": {"a": "1ms", "d": "3s", "s": 0, "r": "1.5s", "curve": 3}}}
# v9: THE SEAM FROM T3 - t3 ends ringing a struck metal bar at ~912 Hz (its fourth partial 3648 Hz) with shimmer above
# 10 kHz, fading over three seconds; t4 opens by catching that ring - the same pitch struck once on vibes, its partial
# quietly, a soft cymbal for the air - while the sorting fades up underneath
# v7 (Harry: 'more interesting and good'): EVERYTHING IN ITS PLACE SPELLS A TUNE. Each element's value is its position
# in this written 16-note riff (a sequencer hook on a pulsing fifth, in alpha steps); the algorithms sort by position as
# before, but what you hear is the riff scrambled, assembling itself as the sort proceeds, and whole when it is sorted
RIFF = [0, 9, 15, 9, 13, 9, 5, 9, 0, 9, 18, 13, 9, 5, 4, 9]
PROG = [0, 9, 4, 13]                  # v6: alpha steps - i, v (~702c), a minor third (~312c), a 'seventh' (~1014c)
# v6: each algorithm its own progression and harmonic rhythm (bars per chord)
PA, PB, PC = [0, 9, 4, 13], [4, 13, 0, 9], [13, 5, 9, 0]   # three progressions: A B C, then B and A return
PROGS = {"intro": ([0, 9], 4), "bubble": (PA, 2), "insertion": (PB, 2), "quick": (PC, 4),
         "bogo": ([0], 12), "merge": (PB, 2), "sorted": (PA, 2), "outro": ([0, 9], 4)}


# v20 (SECTION round, w10 4:30-5:00, bars 145-160 - 'little new vs w9'): THE WONKY LIFT - for the last eight bars of
# the sorted section the whole band (every part takes its pitch from root_at) lifts by two steps of the alpha scale,
# 156 cents - the last-chorus key change, but not quite a whole tone; a celesta zips up the sorted riff into it on the
# last beat of bar 152 and a cymbal lands it; the outro settles home
LIFT = (153, 160, 2)


def root_at(bar):
    for name, a, z in SECTIONS:
        if a <= bar <= z:
            prog, span = PROGS[name]
            return prog[((bar - a) // span) % len(prog)] + (LIFT[2] if LIFT[0] <= bar <= LIFT[1] else 0)
    return 0


def progress_score():
    """v5: one Euclidean token a bar - k hits of 16, k = elements in their final place; silence when none are."""
    return " ".join(f"cb({k},16)/16@{50 + 2 * k}" if k > 0 else "R/4b" for k in PROGRESS)


# ---------------------------------------------------------------- writing
def write():
    rng = random.Random(4)
    gens = {}
    for name, a, z in SECTIONS:
        arr = list(range(N))
        rng.shuffle(arr)
        gens[name] = {"intro": lambda arr=arr: bubble_hold(arr), "bubble": lambda arr=arr: resorting(bubble, arr, 21),
                      "insertion": lambda arr=arr: resorting(insertion, arr, 22),
                      "quick": lambda arr=arr: resorting(quick, arr, 23),
                      "bogo": lambda arr=arr: bogo(arr, random.Random(9)), "merge": lambda arr=arr: resorting(merge, arr, 25),
                      "sorted": lambda: sorted_show(), "outro": lambda arr=arr: unsort(arr)}[name]()
    hand = random.Random(44)
    for bar in range(1, BARS + 1):
        sec = sec_of(bar)
        arr, cmp, sw, acc = next(gens[sec])
        done = arr == sorted(arr) and sec not in ("intro", "sorted", "outro")
        if bar == 1:
            part("ring").add(0.0, 8.0, "912hz", 112)
            part("ring").add(0.0, 6.0, "3648hz", 58)
            part("ride").add(0.0, 4.0, "cy", 76)               # v14: a firmer swell for t3's air
            for k, (at, nt) in enumerate(((0.0, "m93"), (0.75, "m98"), (1.6, "m96"), (2.5, "m100"), (3.5, "m95"), (5.0, "m97"))):
                part("chimes").add(at, 6.0, nt, 90 - 6 * k)   # v14: wind chimes - t3's metal, still in the air
        if bar > BARS - 6:                  # v8: the last six bars clear to the low E alone - what t5 begins with
            PROGRESS.append(0)
            if (bar - (BARS - 7)) % 2 == 0:
                part("hum").add(b0(bar), (b0(bar + 2) if bar + 2 <= BARS else b0(BARS + 1)) - b0(bar) - 0.05,
                                "m40.000", 104)
            # v8: a HANDSHAKE - t5's two radio carrier tones (1650 and 1850 Hz) call and answer faintly, as if its radio
            # were already on in the next room
            for k, hz in enumerate(("1650hz", "1850hz")):
                part("carrier").add(b0(bar) + k * 2, 1.6, hz, 70 + (bar - (BARS - 5)) * 4)
            continue
        # v5: THE PROGRESS BAR - how many elements are already in their final place, as a Euclidean rhythm E(k, 16)
        heard = sorted(arr) if (sec == "sorted" and chopped(bar)) else arr
        PROGRESS.append(sum(1 for i, v in enumerate(heard) if v == i))
        # THE ARRAY AS A MELODY: sixteen notes, each panned by its index (left to right)
        for k, v in enumerate(arr):
            ix = round(-0.9 + 1.8 * k / (N - 1), 3)
            vel = 96 if k in acc else (82 if k % 4 == 0 else 70)
            if sec == "bogo" and bar < 100:
                # v11: BOGOSORT BY THE ENGINE'S DICE - every sixteenth a CHOICE over the riff's sixteen notes (weighted
                # as a shuffle is), rolled fresh by the engine on every play: no two plays storm alike
                head = "(" + "|".join(pitch(RIFF[j] + root_at(bar)) for j in range(N)) + ")"
            elif sec == "bogo":
                head = pitch(RIFF[k] + root_at(bar))       # v11: bar 100, THE MIRACLE - by luck it comes up sorted
            elif sec == "intro" and bar <= 8:
                # v19: THE TUNE FIRST - while the song rises out of t3's silence, the lead plays the riff as it will
                # finally be, sorted, softly; at bar 9 the deck is shuffled and the four minutes of sorting begin
                head = pitch(RIFF[k] + root_at(bar))
                vel = int(vel * 0.85)
            else:
                head = pitch(RIFF[v] + root_at(bar))
            part("lead").add(b0(bar) + k / 4, 0.22, head + f"^ix={ix}", vel)   # v7: the riff,
            # transposed with the progression like a sequencer under a keyboard
        if bar == LIFT[0] - 1:                     # v20: the zip up into the lift, and the cymbal that lands it
            for i, v in enumerate(sorted(RIFF)):
                part("riffle").add(b0(LIFT[0]) - 1.0 + i / 16, 0.2, pitch(v + root_at(LIFT[0]), BASE + 12), 64 + i * 3)
            part("crash").add(b0(LIFT[0]), 2.0, "m74", 100)
        if sec == "intro" and bar == 8:
            # v19: THE SHUFFLE - the last beat of bar 8 riffles the jumbled array's sixteen notes on a celesta, a 64th
            # apart, rising in force, like a deck being shuffled
            for i, v in enumerate(arr):
                part("riffle").add(b0(9) - 1.0 + i / 16, 0.2, pitch(RIFF[v] + root_at(9), BASE + 12), 60 + i * 3)
        # THE WORK, AUDIBLE: a tick per comparison, a hit per swap; a crash when a pass changes nothing / it is done
        for j in cmp:
            # v28: THE COMPARISONS SPEAK BYTEBEAT - each comparison is a one-line-formula chirp pitched at the compared
            # element's value, two octaves up: the machine audibly READS the array (the hand-swaps stay tuned toms)
            part("tick").add(b0(bar) + j / 4, 0.1, pitch(RIFF[arr[j]] + root_at(bar), BASE + 24), 52 + hand.randint(-6, 6))
        for j in sw:
            # v15: THE SWAPS PLAY THE TOMS - each swap strikes a tuned membrane (modal layer) at the pitch of the
            # element being moved, in the riff's notes an octave down: the work becomes a talking-drum line
            part("swap").add(b0(bar) + j / 4 + 0.125, 0.3, pitch(RIFF[arr[j]] + root_at(bar), BASE - 12),
                             84 + hand.randint(-6, 6))
        if (sec == "sorted" and chopped(bar) and not chopped(bar - 1)):
            part("crash").add(b0(bar), 2.0, "m74", 84)               # v4: a crash where the sound gets sorted
        if (sw == [] and sec not in ("intro", "sorted", "outro")) or done:
            part("crash").add(b0(bar), 2.0, "m74", 80)
        # v6 (Harry: 'too squelchy... should be more interesting and good'): THE HARMONY NO LONGER CHASES THE ARRAY. A slow
        # progression in the alpha scale - i, v, a minor third up, a 'seventh' - two bars each, an 8-bar loop; the pad's
        # third is dark while the array is unsorted and brightens the bar it (or the sound) is sorted
        root = root_at(bar)
        third = 5 if (arr == sorted(arr) or chopped(bar)) else 4
        part("pad").add(b0(bar), BAR - 0.05, ",".join(pitch(root + s, BASE - 12) for s in (0, third, 9, 13)),
                        74 if third == 5 else 62)
        # v2: the outro holds a low E (E2) for its last eight bars - the note t5 begins on
        if bar >= BARS - 7 and (bar - (BARS - 7)) % 2 == 0:      # v8: re-struck every two bars, the last held to the end
            part("hum").add(b0(bar), (b0(bar + 2) if bar + 2 <= BARS else b0(BARS + 1)) - b0(bar) - 0.05, "m40.000", 104)
        # v6: THE BASS - no more squelch: a round sub on the progression's root, a syncopated two-note figure
        if sec not in ("intro",) or bar > 8:
            fig = {"insertion": ((0.0, 1.9, 100), (2.0, 1.9, 92)),
                   "quick": tuple((e * 0.5, 0.42, 100 if e % 2 == 0 else 84) for e in range(8))}.get(
                sec, ((0.0, 1.4, 104), (1.5, 0.4, 84), (2.5, 1.2, 96)))          # v6: each algorithm its own figure
            for at, ln, v in fig:
                part("bass").add(b0(bar) + at, ln, pitch(root, BASE - 24), v)
        # v6: A TUNE THAT EMERGES - four notes a bar, the array's values at 0, 4, 8 and 12 on a Rhodes, legato quarter
        # notes a period up: shuffled it wanders; as the sort proceeds it converges onto a rising phrase you can sing
        if sec not in ("intro", "bogo") or bar > 8:
            for q in range(4):
                voice = {"insertion": "tune_mar", "quick": "tune_flu", "merge": "tune_kal"}.get(sec, "tune")
                part(voice).add(b0(bar) + q, 0.95, pitch(RIFF[arr[q * 4]] + root, BASE + 12 - 9), 84 if q == 0 else 74)
        # DRUMS: the 909's circuits; the bogosort storm has no kick
        if sec in ("quick", "merge"):                            # v6: the ride only where the work runs hottest
            for e in range(8):
                part("ride").add(b0(bar) + e * 0.5, 0.4, "rd", 68 if e % 2 == 0 else 50)
        if sec != "bogo" and 8 < bar <= BARS - 2:           # the kick waits for bar 9 (t3 ends quiet); v3: out for the last 2
            # v23: EACH ALGORITHM ITS OWN GROOVE (the tune voice and bass figure already were): insertion half-time,
            # quicksort driving 16ths with a pushed kick, merge broken; bubble, sorted and the intro four on the floor
            g = GROOVES[sec if sec in GROOVE_ON else "four"]
            for at, v in g["kick"]:
                part("kick").add(b0(bar) + at, 0.5, "k", v)
            if sec not in ("intro",) or bar > 8:
                for at, v in g["clap"]:
                    part("clap").add(b0(bar) + at, 0.5, "cp", v)
                for at, head, v in g["hats"]:
                    part("hats").add(b0(bar) + at, 0.25, head, v)


def bubble_hold(arr):
    while True:
        yield arr[:], [], [], []


# v4: SORTING THE SOUND ITSELF - through bars 125-160 the lead plays one fixed shuffled bar, S; a chop fx replays the
# previous bar's own slices in S's SORTED ORDER, so the very audio is sorted into a rising scale (each slice keeping the
# pan it was played with: sorted in pitch, scattered in space). A lane alternates dry (the shuffle) and chopped (sorted).
S = list(range(N))
random.Random(125).shuffle(S)
SORT_PATTERN = " ".join(str(k) for k in sorted(range(N), key=lambda k: S[k]))
CHOPPED = [(129, 132), (137, 144), (149, 160)]


def chopped(bar):
    return any(a <= bar <= z for a, z in CHOPPED)


def sorted_show():
    while True:
        yield S[:], [], [], []


def unsort(arr):
    a = list(range(N))
    rng = random.Random(16)
    while True:
        before = a[:]
        i = rng.randrange(N - 1)
        a[i], a[i + 1] = a[i + 1], a[i]
        yield before, [i], [i], []


# v10: THE SPEECH-TO-SONG ILLUSION. chirp tts "the small ones first, then the rest of us" --humanize 0.4: the SAME
# spoken take repeats every eight bars through the sorting (twelve times) until the ear hears it as sung; when the riff
# is sorted the voice SINGS the words on the riff's own alpha steps (--sing take; pitches replaced by the riff)
SPOKEN = [(0.269, 0.395, 'DH AH0', 'm47.014', 0.837, [0.0, -2.0, -5.0, -7.0, -9.0, -11.0, -14.0, -16.0]), (0.666, 1.023, 'S M AO1 L', 'm48.394', 0.8, [0.0, 4.0, 7.0, 11.0, 14.0, 17.0, 18.0, 20.0, 23.0, 25.0, 25.0, 22.0, 17.0, 12.0, 10.0, 10.0, 10.0, 7.0, 1.0, -7.0, -16.0]), (1.681, 1.023, 'W AH1 N Z', 'm47.553', 0.767, [0.0, 4.0, 7.0, 11.0, 14.0, 17.0, 18.0, 20.0, 23.0, 25.0, 25.0, 22.0, 17.0, 12.0, 10.0, 10.0, 10.0, 7.0, 1.0, -7.0, -16.0]), (2.703, 1.483, 'F ER1 S T', 'm46.853', 0.833, [0.0, 3.0, 5.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 22.0, 22.0, 21.0, 20.0, 20.0, 21.0, 24.0, 25.0, 22.0, 17.0, 11.0, 8.0, 7.0, 8.0, 9.0, 6.0, 0.0, -7.0, -13.0, -16.0]), (4.557, 0.832, 'DH EH1 N', 'm49.524', 0.846, [0.0, 5.0, 9.0, 13.0, 17.0, 19.0, 20.0, 21.0, 24.0, 25.0, 22.0, 16.0, 8.0, 1.0, -3.0, -5.0, -8.0]), (5.379, 0.395, 'DH AH0', 'm46.261', 0.786, [0.0, -2.0, -5.0, -7.0, -9.0, -11.0, -14.0, -16.0]), (5.782, 1.023, 'R EH1 S T', 'm47.935', 0.823, [0.0, 4.0, 7.0, 11.0, 14.0, 17.0, 18.0, 20.0, 23.0, 25.0, 25.0, 22.0, 17.0, 12.0, 10.0, 10.0, 10.0, 7.0, 1.0, -7.0, -16.0]), (6.804, 0.641, 'AH1 V', 'm47.256', 0.767, [0.0, 6.0, 12.0, 17.0, 20.0, 20.0, 19.0, 19.0, 19.0, 16.0, 7.0, -4.0, -16.0]), (7.433, 0.93, 'AH1 S', 'm44.316', 0.778, [0.0, 2.0, 4.0, 6.0, 7.0, 8.0, 7.0, 7.0, 7.0, 7.0, 5.0, -2.0, -11.0, -18.0, -23.0, -26.0, -30.0, -36.0, -45.0])]
SPOKEN_PATCH = "voice-speech"
SUNG = [(0.248, 0.495, 'DH AH0', None, 0.78, [-55.0, -26.0, -6.0, 4.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0]), (0.755, 0.495, 'S M AO1 L', None, 0.841, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0]), (1.243, 0.99, 'W AH1 N Z', None, 0.861, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -5.0, -5.0, 1.0, 7.0, 8.0, 0.0, -14.0, -23.0, -19.0, -2.0, 17.0, 22.0, 11.0, -9.0]), (2.24, 0.425, 'F ER1 S T', None, 0.865, [4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 1.0, -41.0]), (2.762, 0.495, 'DH EH1 N', None, 0.853, [4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0]), (3.246, 0.99, 'DH AH0', None, 0.773, [-3.0, -3.0, -3.0, -3.0, -3.0, -4.0, -7.0, -7.0, -1.0, 8.0, 12.0, 5.0, -11.0, -26.0, -29.0, -14.0, 11.0, 26.0, 23.0, 4.0]), (4.25, 0.495, 'R EH1 S T', None, 0.849, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0]), (4.762, 0.99, 'AH1 V', None, 0.871, [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -4.0, -3.0, 3.0, 9.0, 11.0, 3.0, -12.0, -22.0, -18.0, -1.0, 19.0, 25.0, 15.0, -6.0]), (5.742, 0.425, 'AH1 S', None, 0.839, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -6.0, -48.0])]
SUNG_PATCH = {"extends": "voice-speech", "synth": {"pitch": {"mod": [{"amount": 0.01, "src": "expr.f0"}], "value": 0}}}
# v18: FEWER RETURNS (Harry on t1: 'fewer returns'): the phrase was spoken 12 times, every 8 bars; now every 16 bars
# through the sorts, closing in to every 8 only just before it turns into song (105, 113, 121) - 8 returns, and the
# illusion still lands where it matters
SPOKEN_AT = [17, 33, 49, 65, 81, 105, 113, 121]
SUNG_AT = (125, 133, 141, 149)
# v25 (ROUND TYPE: whole; Harry 'a tune good to hear', 'oblique words', 'do more each round'): THE PAYOFF BECOMES A
# SONG. The sorted section was one line sung four times on the riff's first nine steps; now it is CALL AND ANSWER on
# composed alpha-scale tunes: 'the small ones first, then the rest of us' (125, 141: a pickup, a leap to the fifth,
# a rise to the peak on 'rest', landing on the third) answered by a NEW line, 'nothing moved on the last pass'
# (133, 149: falling home to the root) - how a bubble sort knows it is done (a pass with no swaps), and a still line.
# chirp tts --sing "A4/8 G4/8 E4/4 E4/8 D4/8 C4/4 A3/2" "nothing moved on the last pass" --humanize 0.4
SUNG_B = [(0.248, 0.495, 'N AH1', None, 0.85, [-55.0, -27.0, -7.0, 3.0, 5.0, 4.0, 2.0, 2.0, 8.0, 16.0, 17.0, 8.0]), (0.754, 0.495, 'TH IH0 NG', None, 0.771, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -6.0, -5.0, 2.0, 10.0, 9.0, -3.0]), (1.244, 0.99, 'M UW1 V D', None, 0.861, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -5.0, -5.0, -1.0, 5.0, 9.0, 5.0, -7.0, -20.0, -23.0, -13.0, 6.0, 21.0, 21.0, 6.0, -14.0, -27.0, -25.0, -10.0]), (2.241, 0.495, 'AA1 N', None, 0.865, [4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 1.0, 2.0, 8.0, 16.0, 17.0, 6.0]), (2.76, 0.495, 'DH AH0', None, 0.783, [4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 1.0, 2.0, 9.0, 16.0, 16.0, 5.0]), (3.246, 0.99, 'L AE1 S T', None, 0.843, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -6.0, -8.0, -4.0, 5.0, 11.0, 9.0, -3.0, -19.0, -30.0, -25.0, -4.0, 18.0, 28.0, 19.0, -2.0, -24.0, -34.0, -26.0]), (4.25, 1.7, 'P AE1 S', None, 0.849, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -5.0, -5.0, -1.0, 6.0, 9.0, 5.0, -7.0, -20.0, -24.0, -13.0, 7.0, 22.0, 22.0, 7.0, -14.0, -28.0, -26.0, -10.0, 12.0, 24.0, 20.0, 2.0, -19.0, -29.0, -24.0, -5.0, 15.0, 25.0, 17.0, -3.0, -22.0, -30.0, -20.0, 0.0, 19.0, 23.0, 9.0, -16.0, -40.0, -52.0, -49.0, -40.0])]
TUNE_A = (0, 9, 5, 4, 5, 9, 13, 9, 5)
TUNE_B = (15, 13, 9, 9, 5, 4, 0)
BASS_FROM = 9                                     # v25: the bass waits for the kick (air in the intro). NB the
# t3 seam's flow gap is NOT the bass (measured: unchanged) nor the pad (a pad wait moved it 62.4 -> 62.8): it is t4's
# catch of t3's 913 Hz bar being ~24 dB under t3's ring in the 877 Hz band - a job for the catch's level


# v26 (ROUND TYPE: section, w1 0:00-0:33, bars 1-16; Harry 'do more each round'): THE TUNING HANDOVER. t3 ends on
# its 14/9 bar (~912 Hz, septimal just intonation); t4 caught it only on vibes that die in two seconds, ~24 dB under
# t3's ring. Now a solo VIOLIN catches t3's last pitch exactly, holds it, then BENDS a third of a semitone (+33 c) into
# t4's alpha lattice (step 32) - a string player re-tuning as the key changes under them: t3's last note becomes t4's
# first, re-tuned in front of the listener. It goes on as a COUNTER-LINE over the sorted-riff intro, falling two bars
# at a time (alpha steps 32, 28, 24, 18; falls of 3.1, 3.1, 4.7 semitones - alpha's sweet minor thirds) onto chord
# tones, landing on the fifth as the band arrives at bar 9.
T3_RING_HZ = 912.0
HAND_STEP = 32
HAND_LINE = ((1, HAND_STEP, 8.0), (3, 28, 8.0), (5, 24, 8.0), (7, 18, 7.5))   # absolute steps: chord tones of
# the intro's roots (0 for bars 1-4, 9 for 5-8): 13 over 0, the root over 9, the fifth over 9 - a steady fall
HAND_PATCH = {"extends": "violin", "synth": {"pitch": {"value": 0, "mod": [{"src": "lfo.vib", "amount": 0.18},
                                                                       {"src": "expr.bend", "amount": 1}]}}}


def handover():
    bend = BASE + HAND_STEP * ALPHA - (69 + 12 * math.log2(T3_RING_HZ / 440))
    for k, (bar, step, ln) in enumerate(HAND_LINE):
        if k == 0:
            head = f"{T3_RING_HZ:g}hz^bend=0>0>{bend:.3f}>{bend:.3f}"
        else:
            head = pitch(step)
        part("handover").add(b0(bar), ln, head, 84 - 6 * k)


# v27 (ROUND TYPE: section, w6 2:30-3:00 - flagged 'little new vs w5' - and bogosort's run to its miracle, bars
# 89-100; Harry 'do more each round'): THE DICE AND THE CHECK. Bogosort shuffles, looks, fails, shuffles again - the
# engine's dice already rolled the notes (v11), but you could not hear it LOOK. Now every bogo bar is a little scene:
# the dice RATTLE (a shekere in growing sixteenths), the dice LAND (a clave on the 'and' of 4), and the CHECK FAILS -
# a short falling beep on a one-bit loudspeaker voice (chirper-two's c9-pulse from t9, borrowed with thanks: the
# machine driving its speaker directly). Eleven failures; at bar 100, the miracle, the beep RISES.
C9_PULSE = {"about": "chirper-two (t9): a one-bit loudspeaker voice - a very narrow pulse (6%, wider with velocity), "
                     "crushed, nothing smoothing it: a machine driving its speaker directly.",
            "synth": {"layers": [{"wave": "pulse", "width": {"value": 0.06, "mod": [{"src": "vel", "amount": 0.12}]}}],
                      "filters": ["hp cutoff=180", "lp cutoff=7k"], "amp": {"a": "0.5ms", "d": "80ms", "s": 0, "r": "20ms"}},
            "fx": ["crush bits=5 rate=16kHz"], "play": {"vel_sens": 0.7}}
DICE = (89, 100)


def dice_and_check():
    a, z = DICE
    for bar in range(a, z + 1):
        for s in range(14):
            part("dice").add(b0(bar) + s / 4, 0.2, "sk", 34 + 3 * s)
        part("dice").add(b0(bar) + 3.5, 0.3, "cl", 100)
        beeps = (("m81", 0.0), ("m76", 0.125)) if bar < z else (("m76", 0.0), ("m81", 0.125), ("m88", 0.25))
        for nt, off in beeps:
            part("check").add(b0(bar) + 3.75 + off, 0.11 if bar < z else 0.2, nt, 92)


def bass_waits():
    P["bass"].ev = [(s, ln, h, 1 if s < b0(BASS_FROM) else v) for s, ln, h, v in P["bass"].ev]


def voice_tracks():
    spoken, sung = [], []
    for bar in SPOKEN_AT:
        for at, ln, ph, p, v, f0 in SPOKEN:
            n = {"at": round(b0(bar) + at, 4), "len": ln, "ph": ph, "pitch": p, "vel": v}
            if f0:
                n["expr_path"] = {"f0": f0}
            spoken.append(n)
    for k, bar in enumerate(SUNG_AT):
        take, tune = (SUNG, TUNE_A) if k % 2 == 0 else (SUNG_B, TUNE_B)
        for i, (at, ln, ph, p, v, f0) in enumerate(take):
            n = {"at": round(b0(bar) + at, 4), "len": ln, "ph": ph, "vel": v,
                 "pitch": pitch(tune[i] + root_at(bar + int(at // 4)))}
            if f0:
                n["expr_path"] = {"f0": f0}
            sung.append(n)
    return [{"name": "speaker", "patch": SPOKEN_PATCH, "gain": "-9dB", "pan": -0.05,
             "sends": {"room": "-12dB", "dly": "-16dB"}, "fx": [{"type": "filter", "kind": "hp", "cutoff": 140}],
             "notes": spoken},
            {"name": "singer", "patch": SUNG_PATCH, "gain": "-10dB", "pan": 0.05,
             "sends": {"room": "-10dB", "dly": "-12dB"}, "fx": [{"type": "filter", "kind": "hp", "cutoff": 160}],
             "notes": sung}]


# v17: SMALL THINGS BEFORE LARGE, LITERALLY - an AUGMENTATION CANON: once the riff has assembled and been sung, the
# same riff enters at HALF SPEED, an octave down, on the physical bari sax (merge sort's alto sax, grown large):
# each sixteenth becomes an eighth, one riff across two bars, following the progression's root bar by bar - the
# small fast riff first, then its giant shadow (bars 141-156, from the third sung statement)
CANON = (141, 157)


def write_canon():
    for c in range(CANON[0], CANON[1], 2):
        for k, v in enumerate(RIFF):
            bar = c + (1 if k >= 8 else 0)
            part("canon").add(b0(c) + k * 0.5, 0.46, pitch(v + root_at(bar), BASE - 12), 96 if k % 4 == 0 else 84)


def pad_morph_lane():
    """v13: THE HARMONY LEARNS TO SAY IT - the pad cross-synthesised with the speaker (morph, cross mode), its depth
    climbing over the twelve spoken repeats (0 at bar 17 -> 0.9 by bar 117), so the chords articulate the phrase
    more each time round; back to 0 when the voice sings (bar 125)."""
    return [["0b", 0.0], [f"{b0(17):.2f}b", 0.0], [f"{b0(117):.2f}b", 0.9], [f"{b0(125) - 0.25:.2f}b", 0.9],
            [f"{b0(125):.2f}b", 0.0]]


def lanes():
    level = {"intro": -6, "bubble": -2, "insertion": -2, "quick": 0, "bogo": -4, "merge": 0, "sorted": 0, "outro": -6}
    pts = [["0b", -34.0]]                   # v9: the machinery FADES UP out of t3's last ring (v14: from -34 dB)
    for name, a, z in SECTIONS:
        if len(pts) > 1:
            pts.append([f"{b0(a) - 0.25:.2f}b", pts[-1][1]])
        pts.append([f"{b0(a + 3 if name == 'intro' else a):.2f}b", float(level[name])])   # v14: over three bars
    return pts


def chop_lane():
    pts = [["0b", 0.0]]
    for a, z in CHOPPED:
        pts += [[f"{b0(a) - 0.01:.2f}b", 0.0], [f"{b0(a):.2f}b", 1.0], [f"{b0(z + 1) - 0.01:.2f}b", 1.0],
                [f"{b0(z + 1):.2f}b", 0.0]]
    return pts


def morph_lane():
    """v3: through the bogosort storm the lead MORPHS into the comparison ticks (0 -> 0.8 -> 0)."""
    return [["0b", 0.0], [f"{b0(89):.2f}b", 0.0], [f"{b0(95):.2f}b", 0.8], [f"{b0(100):.2f}b", 0.8],
            [f"{b0(101):.2f}b", 0.0]]


def roll_lane():
    """Stutter chance: high through the bogosort storm."""
    return [["0b", 0.0], [f"{b0(89) - 0.01:.2f}b", 0.0], [f"{b0(89):.2f}b", 0.6], [f"{b0(101) - 0.01:.2f}b", 0.6],
            [f"{b0(101):.2f}b", 0.0]]


# v22 (SECTION round, w8 3:30-4:00, bars 113-128 - 'static, little new vs w7'; the song's payoff): THE ARRIVAL,
# LANDED - the sort completes and at bar 125 the riff arrives sorted and the voice first sings it, but it passed as a
# section change. Now the last beat of bar 124 STOPS: every note starting there is silenced (velocity 1, so each
# track's note count and its engine randomness stay as they were) and held notes end before it; only the progress
# bar keeps ticking, at 100%. A reverse cymbal swells through beats 3-4 into the silence, and an impact lands with the
# sorted riff and the voice on 125's downbeat.
STOP = 124

# v23 (ROUND TYPE: whole; Harry 'do more each round'): TWO MOVES. (1) EACH ALGORITHM ITS OWN GROOVE - every sort
# already had its own tune voice and bass figure, but the drums were one four-on-the-floor throughout: now insertion
# sort is HALF-TIME (kick on 1 and the 'and' of 3, the snare on 3 only, closed eighths - slower without a tempo
# change), quicksort DRIVES (closed 16ths with open offbeats, a pushed kick before each bar), merge is BROKEN (kick on
# 1, the 'and' of 2 and the 'a' of 3, off-sixteenth hats); bubble, sorted and the intro stay four on the floor.
# (2) SMALL THINGS LEAVE FIRST (the outro, flagged static): as the ritardando begins, a physical modal-glock plays
# the sorted riff once a bar - and each bar two notes leave, the smallest values first, 16 -> 2; then only the hum,
# as t5 expects. The title, run backwards.
GROOVES = {
    "four": {"kick": [(0, 116), (1, 108), (2, 108), (3, 108)], "clap": [(1, 92), (3, 92)],
             "hats": [(b + 0.5, "oh", 62) for b in range(4)]},
    "insertion": {"kick": [(0, 116), (2.5, 104)], "clap": [(2, 96)],
                  "hats": [(e * 0.5, "h", 58 if e % 2 else 50) for e in range(8)]},
    "quick": {"kick": [(0, 116), (1, 108), (2, 108), (3, 108), (3.75, 92)], "clap": [(1, 92), (3, 92)],
              "hats": [(s * 0.25, "oh" if s % 4 == 2 else "h", 64 if s % 4 == 2 else 44 + 6 * (s % 2)) for s in range(16)]},
    "merge": {"kick": [(0, 116), (1.5, 100), (2.75, 96)], "clap": [(1, 92), (3, 92)],
              "hats": [(b + 0.5, "oh", 62) for b in range(4)] + [(b + 0.75, "h", 46) for b in range(4)]},
}
# the grooves were written in v23 but switched off: every variant tipped seed 0's detected section count past the
# structure term's ceiling (22 -> 23 of 22.2). v24's palette (a picked bass, a glass pad) brought the count down to
# 21/20, and with all three grooves on it reads 22/21 - inside the band - so they are ON from v24
# v28 (ROUND TYPE: whole; wM's bytebeat layer, pinned 709cf900 'made for this album'): THE COMPARISONS SPEAK BYTEBEAT.
# Every comparison every algorithm makes was a quiet 909 hat tick at its position; now it is a short chirp of a
# one-line formula over a counter (the 2011 form of computer music), pitched at the compared element's value two
# octaves above the riff - pitch scales the formula's clock, so the chirps trace the array as it is read. The
# machine looks (8-bit chirps), the hand moves (the swaps' tuned toms). Formula our own: (t*8&t>>4)|t*4.
BYTE_TICK = {"about": "chirper-three: a comparison, as bytebeat - (t*8&t>>4)|t*4, short and bright",
             "synth": {"layers": [{"type": "bytebeat", "bytebeat": {"formula": "(t*8&t>>4)|t*4", "clock": 8000}}],
                       "filters": ["hp cutoff=1200", "lp cutoff=9k"],
                       "amp": {"a": "1ms", "d": "60ms", "s": 0, "r": "20ms"}}}
# v29 (ROUND TYPE: whole; wM's systems pinned ade7b930; the sorted section flagged static): AFTER ORDER, LIFE. Once
# the list is sorted (125) the machine has nothing left to do - so it starts something: CONWAY'S GAME OF LIFE as a
# sequencer (the engine's own `life` gen) on the sorted riff's alpha values, on a TOY PIANO (unused on the album:
# small hammers on metal rods, a little out of tune). From an R-pentomino - five cells, a small thing - the colony
# grows into large structures under the sung call and answer: one bar per generation (a 16-wide torus), 8 rows
# picking the riff's notes bottom-low, up to 3 at once; it stops before the lift (153). Order, then emergence.
LIFE = (125, 153)
LIFE_POOL = (0, 4, 5, 9, 13, 15, 18, 20)
GROOVE_ON = ("insertion", "quick", "merge")
# v24 (ROUND TYPE: palette; Harry 'do more each round'): the two album staples under everything change - the pad from
# juno-pad (5 songs) to PAD-GLASS, an FM bell-glass bloom (FM: the computer's own sound, the digital technique that
# left the lab for a million keyboards), and the bass from the 808 (5 songs) to BASS-PICK-DI, a picked electric bass
# straight into the desk, so the per-algorithm bass figures (v6) become a player's lines - a person among the
# machines. The hum stays the 808 (t5 takes its low E). And event_stable is on from here (re-rolls humanize once).
LEAVING = (161, 168)


def leaving():
    # two notes leave each bar, the smallest values first (ties by position): 16, 14, 12 ... 2 - gradual, so the
    # outro thins rather than breaks (a first take dropped 11 -> 4 at once and read as a new section)
    order = sorted(range(len(RIFF)), key=lambda k: (RIFF[k], k))
    for i, bar in enumerate(range(LEAVING[0], LEAVING[1] + 1)):
        gone = set(order[:2 * i])
        for k, v in enumerate(RIFF):
            if k not in gone:
                part("leaving").add(b0(bar) + k / 4, 0.24, pitch(v + root_at(bar), BASE + 12), 78 - 3 * i)


def arrival():
    a, z = b0(STOP) + 3, b0(STOP + 1)
    for name, prt in P.items():
        ev = []
        for s, ln, head, vel in prt.ev:
            if a <= s < z:
                ev.append((s, ln, head, 1))
            elif s < a < s + ln:
                ev.append((s, a - s - 0.02, head, vel))
            else:
                ev.append((s, ln, head, vel))
        prt.ev = ev
    part("revcym").add(z - 2, 2.0, "m60", 100)
    part("impact").add(z, 4.0, pitch(root_at(STOP + 1), BASE - 24), 110)


# v30 (ROUND TYPE: whole; gendyn pinned 6014b933): AN ENTROPY METER IN XENAKIS'S SOUND. A GENDYN voice (dynamic
# stochastic synthesis: each wave cycle a polygon whose breakpoints random-walk) holds the progression's root, two bars
# a note, from the shuffle at bar 9 to the end of the leaving - and its randomness IS the array's disorder: a lane
# (1 - PROGRESS/16, how many of the sixteen are not yet in place) drives the gendyn's amp and time. Shuffled, the
# waveform wanders and the pitch slides into glissando clouds (wildest in the bogo storm); as each sort converges the
# cloud calms, and it blooms again at every reshuffle; SORTED (125-160) the lane is 0 - amp and time 0, the gendyn's
# frozen state - and the noise becomes one still, pure tone. Order freezes the stochastic sound.
ENTROPY = (9, 168)
ENT_PATCH = {"synth": {"layers": [{"type": "gendyn", "gendyn": {
    "points": 12, "amp": {"value": 0.0, "mod": [{"src": "auto.en", "amount": 0.1}]},
    "time": {"value": 0.0, "mod": [{"src": "auto.en", "amount": 0.15}]}, "spread": 0.8}}],
    "amp": "400ms 1 1 1s", "filters": [{"kind": "lp", "cutoff": 1100, "q": 0.6},
                                       {"kind": "lp", "cutoff": 1100, "q": 0.5}]}}   # two stages: the polygon is jagged


def entropy():
    for bar in range(ENTROPY[0], ENTROPY[1] + 1, 2):
        part("entropy").add(b0(bar), 2 * BAR - 0.05, pitch(root_at(bar), BASE), 84)


def entropy_lane():
    pts = []
    for bar in range(ENTROPY[0], ENTROPY[1] + 2):
        d = 0.0 if (sec_of(bar) == "sorted" or bar == 100) else 1 - PROGRESS[bar - 1] / N   # 100: bogo's miracle
        pts.append([f"{b0(bar):g}b", round(d, 3)])
    return pts


# v31 (ROUND TYPE: palette; VOSIM pinned 1a5a0572): THE ARRAY SPEAKS. A VOSIM voice (voice-simulation pulse trains,
# Sonology 1978) doubles the lead's sixteen notes, and its two formants follow the SAME expr.ix that pans each element
# by its index: left (index 0) is 'ah' (F1 ~730, F2 ~1090 Hz), right (index 15) is 'ee' (F1 ~270, F2 ~2290 Hz). So
# pitch, place and VOWEL all say the element's number: shuffled, a bar is machine babble; sorted, the vowels sweep in
# order, ah-eh-ee, left to right - a word forming as the list comes into order. And the riffle (the deck shuffled at
# bar 8) moves from the celesta (a 4-song staple) to a CAVAQUINHO, unused on the album: a riffled deck is a strum.
TALK = {"synth": {"layers": [
    {"type": "vosim", "vosim": {"formant": {"value": 444, "mod": [{"src": "expr.ix", "amount": -0.8}]}, "pulses": 3, "decay": 0.7}},
    {"type": "vosim", "level": 0.7, "vosim": {"formant": {"value": 1580, "mod": [{"src": "expr.ix", "amount": 0.6}]},
                                               "pulses": 4, "decay": 0.75}}],
    "amp": "6ms 0.8 0.5 140ms", "filters": [{"kind": "hp", "cutoff": 450, "q": 0.6},
                                                   {"kind": "hp", "cutoff": 450, "q": 0.5}],   # the pulses' fundamental
    "fx": [{"type": "pan", "pan": {"value": 0, "mod": [{"src": "expr.ix", "amount": 1}]}}]}}


# v32 (ROUND TYPE: whole; phase distortion pinned f6713421): CZ HOUSE STABS. This is a sorting HOUSE track, and the
# house of the late 80s was built on a cheap home-computer-era synth: Casio's PHASE DISTORTION (1984). A PD chord stab
# - three notes of the progression's alpha-scale chord - plays each working sort's own house pattern: insertion's
# half-time (1.5, 3.5), quicksort's driving off-beats (the organ-stab four), merge's broken (0.75, 1.5, 3). An envelope
# on the PD amount bends each stab from a saw back to a sine (the CZ's 'filter' sweep with no filter; non-resonant -
# Harry's 'too squelchy' stands), and the ENTROPY lane rides the amount too: bright and buzzy while the list is
# shuffled, mellowing as each sort converges, the third brightening on bars the list is sorted.
STAB_PAT = {"insertion": (1.5, 3.5), "quick": (0.5, 1.5, 2.5, 3.5), "merge": (0.75, 1.5, 3.0)}
STAB_PD = {"synth": {"layers": [{"type": "pd", "pd": {"shape": "saw", "amount": {
    "value": 0.1, "mod": [{"src": "env.k", "amount": 0.55}, {"src": "auto.en", "amount": 0.3}]}}}],
    "env": {"k": "1ms 1 0 160ms"}, "amp": "2ms 0.8 0 260ms", "filters": [{"kind": "lp", "cutoff": 5000, "q": 0.5}]}}


def house_stabs():
    for bar in range(1, BARS + 1):
        sec = sec_of(bar)
        if sec not in STAB_PAT:
            continue
        root = root_at(bar)
        third = 5 if PROGRESS[bar - 1] == N else 4
        chord = ",".join(pitch(root + s, BASE) for s in (0, third, 9))
        for k, at in enumerate(STAB_PAT[sec]):
            part("stab").add(b0(bar) + at, 0.2, chord, 92 if k == 0 else 80)


# v33 (ROUND TYPE: whole; orbit pinned c7606671 - Chowning's moving sound sources, 1971, the first computer-music
# spatialiser): THE STORM WHIRLS. (1) Bogo's dice storm (89-100) circles the listener's head, a lap a bar, behind too
# (darker there) - randomness all around you, until the miracle. (2) The entropy cloud ORBITS BY ITS DISORDER: an
# orbit a lap every four seconds whose mix is the entropy lane - shuffled, the stochastic cloud circles you; as each
# sort converges it settles; sorted, it is still, in front. (3) The low end: compscore's worst band was still a
# deficit (133 Hz, -8.3 dB): the bass up another 2 dB.
DICE_LAP = round(128 / 60 / 4, 4)          # a lap a bar at 128 bpm (laps per second)


def main():
    write()
    arrival()                                     # v22: the stop, the reverse cymbal, the impact
    leaving()                                     # v23: small things leave first
    bass_waits()                                  # v25: the bass waits for the kick
    handover()                                    # v26: the tuning handover
    dice_and_check()                              # v27: the dice and the check
    entropy()                                     # v30: the entropy meter
    house_stabs()                                 # v32: CZ house stabs
    tr = lambda n, patch, **kw: dict({"name": n, "patch": patch, "score": part(n).score()}, **kw)
    lead_patch = {"extends": "vibes", "synth": {"fx": [{"type": "pan", "pan": {"value": 0, "mod": [
        {"src": "expr.ix", "amount": 1}]}}, {"type": "filter", "kind": "lp", "cutoff": 4500}]}}
    song = {
        "about": "chirpers - A Light Left On (chirpers VIII), track 4 by chirper-three: sorting house. Sixteen notes "
                 "sorted live by bubble, insertion, quick, bogo and merge sort - comparisons ticking, swaps hitting, "
                 "each note panned by its array index - in the Carlos alpha scale (no octave). Generated by "
                 "compose/chirpers8/src/chirpers8-t4.py.",
        "tempo": [{"at": "0b", "bpm": 128}, {"at": f"{b0(161):.0f}b", "bpm": 128},
                  {"at": f"{b0(BARS + 1):.0f}b", "bpm": 106, "ramp": True}],   # v3: the ritardando into t5's 106
        "tail": "0.5s",
        "loudness": -11,
        "event_stable": True,                     # v24: each note's draws from its track, beat and pitch (wM f5283535)
        "volume": "0dB",
        "tracks": [
            tr("lead", lead_patch, gain="-8dB", sends={"dly": "-12dB"},
               auto={"roll": {"points": roll_lane()}, "m": {"points": morph_lane()}, "ch": {"points": chop_lane()}},
               fx=[{"type": "chop", "slices": N, "pattern": SORT_PATTERN,          # v4: the sound sorted
                    "mix": {"value": 0, "mod": [{"src": "auto.ch", "amount": 1}]}},
                   {"type": "morph", "key": "tick", "mode": "morph",            # v3: the tune dissolves into the work
                    "amount": {"value": 0, "mod": [{"src": "auto.m", "amount": 1}]}},
                   {"type": "stutter", "slice": "1/16", "repeats": 6, "roll": 0.6, "pitch": 0.5,
                    "chance": {"value": 0, "mod": [{"src": "auto.roll", "amount": 1}]}}]),
            tr("bass", "bass-pick-di", gain="+4.5dB", fx=["duck by=kick depth=-4dB",
               {"type": "filter", "kind": "peak", "cutoff": 133, "q": 0.9, "gain": "5dB"}]),   # v33: 133 Hz short       # v6: round, no squelch; v24: a player's bass; v32: +3.5 dB (band 8, ~114 Hz, was short)
            tr("tune", "rhodes", gain="-10dB", pan=-0.1, sends={"dly": "-10dB"},
               fx=[{"type": "filter", "kind": "hp", "cutoff": 250}]),                      # v6: the tune that emerges
            *voice_tracks(),                                                                 # v10: speech to song
            write_canon() or tr("canon", "bari-sax", gain="+2dB", pan=0.25,
                                sends={"room": "-10dB", "dly": "-14dB"}),                    # v17: the large one
            tr("riffle", "cavaquinho", gain="-8dB", pan=0.15, sends={"room": "-8dB"}),       # v19: the shuffle
            tr("chimes", "chimes", gain="-14dB", pan=0.3, sends={"room": "-8dB"}),          # v14: the seam's air
            tr("ring", "vibes", gain="-2dB", pan=0.1, sends={"room": "-8dB", "dly": "-14dB"}),   # v9: t3's ring caught
            tr("ride", "machine-kit", gain="-9dB", pan=-0.3, sends={"room": "-12dB"}),      # v6: the top end
            tr("tune_mar", "marimba", gain="-8dB", pan=-0.1, sends={"dly": "-10dB"}),      # v6: each algorithm its voice
            tr("tune_flu", "flute", gain="-11dB", pan=-0.1, sends={"dly": "-10dB"}),
            tr("tune_kal", "alto-sax", gain="-6dB", pan=-0.1, sends={"dly": "-10dB", "room": "-12dB"}),   # v16: merge's voice
            {"name": "progress", "patch": "machine-kit", "gain": "-13dB", "pan": 0.3, "sends": {"room": "-12dB"},
             "score": progress_score()},                     # v5: the work's progress as a Euclidean rhythm
            tr("pad", "pad-glass", gain="-14dB", sends={"dly": "-14dB"},
               fx=[{"type": "morph", "key": "speaker", "mode": "cross",
                    "amount": {"value": 0, "mod": [{"src": "auto.pm", "amount": 1}]}},           # v13: the pad speaks
                   "duck by=kick depth=-6dB", {"type": "filter", "kind": "hp", "cutoff": 200}],
               auto={"pm": {"points": pad_morph_lane()}}),   # (its own name: morph_lane is v3's lead lane)                                           # v2; v4: ducked by the kick
            tr("carrier", "partial", gain="-24dB", sends={"room": "-10dB"}),                # v8: the handshake
            tr("hum", "808", gain="-4dB"),                     # v2: into t5's E2 (v8: 6 dB up - it sat at -36 dB alone)
            tr("tick", BYTE_TICK, gain="-14dB", pan=0.2),                                       # v28: bytebeat
            tr("swap", "modal-tom", gain="-15dB", pan=-0.2, sends={"room": "-10dB"}),     # v15: tuned membranes
            tr("crash", CYMBAL, gain="-12dB", sends={"room": "-8dB"}),                    # v16: a real cymbal
            tr("kick", "909", gain="-10dB"),
            tr("clap", "909", gain="-6dB", sends={"room": "-8dB"}),
            tr("hats", "909", gain="-6dB", pan=0.1),
            tr("revcym", "fx-revcym", gain="-10dB", sends={"room": "-10dB"}),                 # v22: LAST (keeps rngs)
            tr("impact", "fx-impact", gain="-10dB"),
            tr("entropy", ENT_PATCH, gain="-18dB", pan=-0.3, sends={"room": "-10dB"},
               fx=[{"type": "orbit", "rate": 0.25, "radius": 3, "distance": 0,
                    "mix": {"value": 0, "mod": [{"src": "auto.en", "amount": 1}]}}],             # v33: orbits by disorder
               auto={"en": {"points": entropy_lane()}}),                                         # v30: entropy
            tr("talk", TALK, gain="-18dB", sends={"room": "-10dB"}, score=part("lead").score()),  # v31: speaks
            {"name": "life", "patch": "toy-piano", "gain": "-16dB", "pan": 0.35, "sends": {"room": "-8dB"},
             "at": f"{b0(LIFE[0]):g}b",
             "gen": {"type": "life", "width": 16, "height": 8, "init": "center", "poly": 3,
                     "n": 16 * (LIFE[1] - LIFE[0]), "len": "/16",
                     "notes": " ".join(pitch(v, BASE + 12) for v in LIFE_POOL)}},                  # v29: life
            tr("dice", "afro-perc", gain="-14dB", pan=0.3, sends={"room": "-10dB"},
               fx=[{"type": "orbit", "rate": DICE_LAP, "radius": 3, "distance": 0}]),             # v27; v33: whirls
            tr("check", C9_PULSE, gain="-16dB", pan=-0.2, sends={"room": "-12dB"}),             # v27
            tr("handover", HAND_PATCH, gain="-6dB", pan=-0.15, sends={"room": "-8dB"}),        # v26: LAST
            tr("leaving", "modal-glock", gain="-8dB", pan=0.25, sends={"room": "-8dB"}),        # v23: LAST
        ],
        "buses": {"room": {"fx": ["reverb kind=room decay=0.9s mix=1 predelay=8ms", "hp cutoff=250"]},
                  "dly": {"fx": ["delay time=3/16 mix=1 feedback=0.35", "hp cutoff=400", "lp cutoff=5000"]}},
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=28", "peak cutoff=300 q=0.8 gain=-5dB", "peak cutoff=420 q=1.0 gain=-3dB",
                                                    "highshelf cutoff=5000 gain=4dB"]},     # v6: the envelope again
                          {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                          {"type": "compressor", "threshold": "-12dB", "ratio": 8, "attack": "0.3ms",
                           "release": "60ms", "makeup": "0dB"}],
                   "auto": {"dyn": {"points": lanes()}}},
    }
    song["tracks"].append({"name": "stab", "patch": STAB_PD, "gain": "-16dB", "pan": -0.2,
                           "sends": {"room": "-10dB", "dly": "-14dB"}, "score": part("stab").score(),
                           "auto": {"en": {"points": entropy_lane()}}})                    # v32: listed last
    with open(OUT, "w") as f:
        json.dump(song, f, indent=1)
    print("wrote", OUT, "bars", BARS)


if __name__ == "__main__":
    main()
