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


def root_at(bar):
    for name, a, z in SECTIONS:
        if a <= bar <= z:
            prog, span = PROGS[name]
            return prog[((bar - a) // span) % len(prog)]
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
            else:
                head = pitch(RIFF[v] + root_at(bar))
            part("lead").add(b0(bar) + k / 4, 0.22, head + f"^ix={ix}", vel)   # v7: the riff,
            # transposed with the progression like a sequencer under a keyboard
        # THE WORK, AUDIBLE: a tick per comparison, a hit per swap; a crash when a pass changes nothing / it is done
        for j in cmp:
            part("tick").add(b0(bar) + j / 4, 0.1, "h", 52 + hand.randint(-6, 6))
        for j in sw:
            # v15: THE SWAPS PLAY THE TOMS - each swap strikes a tuned membrane (modal layer) at the pitch of the
            # element being moved, in the riff's notes an octave down: the work becomes a talking-drum line
            part("swap").add(b0(bar) + j / 4 + 0.125, 0.3, pitch(RIFF[arr[j]] + root_at(bar), BASE - 12),
                             84 + hand.randint(-6, 6))
        if (sec == "sorted" and chopped(bar) and not chopped(bar - 1)):
            part("crash").add(b0(bar), 2.0, "cy", 84)                # v4: a crash where the sound gets sorted
        if (sw == [] and sec not in ("intro", "sorted", "outro")) or done:
            part("crash").add(b0(bar), 2.0, "cy", 80)
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
            for b in range(4):
                part("kick").add(b0(bar) + b, 0.5, "k", 116 if b == 0 else 108)
            if sec not in ("intro",) or bar > 8:
                for b in (1, 3):
                    part("clap").add(b0(bar) + b, 0.5, "cp", 92)
                for b in range(4):
                    part("hats").add(b0(bar) + b + 0.5, 0.25, "oh", 62)


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
SPOKEN_AT = [b for b in range(17, 124, 8) if not 89 <= b <= 100]
SUNG_AT = (125, 133, 141, 149)


def voice_tracks():
    spoken, sung = [], []
    for bar in SPOKEN_AT:
        for at, ln, ph, p, v, f0 in SPOKEN:
            n = {"at": round(b0(bar) + at, 4), "len": ln, "ph": ph, "pitch": p, "vel": v}
            if f0:
                n["expr_path"] = {"f0": f0}
            spoken.append(n)
    for bar in SUNG_AT:
        for i, (at, ln, ph, p, v, f0) in enumerate(SUNG):
            n = {"at": round(b0(bar) + at, 4), "len": ln, "ph": ph, "vel": v,
                 "pitch": pitch(RIFF[i % 16] + root_at(bar + int(at // 4)))}
            if f0:
                n["expr_path"] = {"f0": f0}
            sung.append(n)
    return [{"name": "speaker", "patch": SPOKEN_PATCH, "gain": "-9dB", "pan": -0.05,
             "sends": {"room": "-12dB", "dly": "-16dB"}, "fx": [{"type": "filter", "kind": "hp", "cutoff": 140}],
             "notes": spoken},
            {"name": "singer", "patch": SUNG_PATCH, "gain": "-10dB", "pan": 0.05,
             "sends": {"room": "-10dB", "dly": "-12dB"}, "fx": [{"type": "filter", "kind": "hp", "cutoff": 160}],
             "notes": sung}]


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


def main():
    write()
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
            tr("bass", "808", gain="-9dB", fx=["duck by=kick depth=-4dB"]),                  # v6: round, no squelch
            tr("tune", "rhodes", gain="-10dB", pan=-0.1, sends={"dly": "-10dB"},
               fx=[{"type": "filter", "kind": "hp", "cutoff": 250}]),                      # v6: the tune that emerges
            *voice_tracks(),                                                                 # v10: speech to song
            tr("chimes", "chimes", gain="-14dB", pan=0.3, sends={"room": "-8dB"}),          # v14: the seam's air
            tr("ring", "vibes", gain="-2dB", pan=0.1, sends={"room": "-8dB", "dly": "-14dB"}),   # v9: t3's ring caught
            tr("ride", "machine-kit", gain="-9dB", pan=-0.3, sends={"room": "-12dB"}),      # v6: the top end
            tr("tune_mar", "marimba", gain="-8dB", pan=-0.1, sends={"dly": "-10dB"}),      # v6: each algorithm its voice
            tr("tune_flu", "flute", gain="-11dB", pan=-0.1, sends={"dly": "-10dB"}),
            tr("tune_kal", "kalimba", gain="-8dB", pan=-0.1, sends={"dly": "-10dB"}),
            {"name": "progress", "patch": "machine-kit", "gain": "-13dB", "pan": 0.3, "sends": {"room": "-12dB"},
             "score": progress_score()},                     # v5: the work's progress as a Euclidean rhythm
            tr("pad", "juno-pad", gain="-11dB", sends={"dly": "-14dB"},
               fx=[{"type": "morph", "key": "speaker", "mode": "cross",
                    "amount": {"value": 0, "mod": [{"src": "auto.pm", "amount": 1}]}},           # v13: the pad speaks
                   "duck by=kick depth=-6dB", {"type": "filter", "kind": "hp", "cutoff": 200}],
               auto={"pm": {"points": pad_morph_lane()}}),   # (its own name: morph_lane is v3's lead lane)                                           # v2; v4: ducked by the kick
            tr("carrier", "partial", gain="-24dB", sends={"room": "-10dB"}),                # v8: the handshake
            tr("hum", "808", gain="-4dB"),                     # v2: into t5's E2 (v8: 6 dB up - it sat at -36 dB alone)
            tr("tick", "909", gain="-17dB", pan=0.2, fx=[{"type": "filter", "kind": "hp", "cutoff": 3000}]),
            tr("swap", "modal-tom", gain="-15dB", pan=-0.2, sends={"room": "-10dB"}),     # v15: tuned membranes
            tr("crash", "909", gain="-12dB", sends={"room": "-8dB"}),
            tr("kick", "909", gain="-10dB"),
            tr("clap", "909", gain="-6dB", sends={"room": "-8dB"}),
            tr("hats", "909", gain="-6dB", pan=0.1),
        ],
        "buses": {"room": {"fx": ["reverb kind=room decay=0.9s mix=1 predelay=8ms", "hp cutoff=250"]},
                  "dly": {"fx": ["delay time=3/16 mix=1 feedback=0.35", "hp cutoff=400", "lp cutoff=5000"]}},
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=28", "peak cutoff=300 q=0.8 gain=-5dB",
                                                    "highshelf cutoff=5000 gain=4dB"]},     # v6: the envelope again
                          {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                          {"type": "compressor", "threshold": "-12dB", "ratio": 8, "attack": "0.3ms",
                           "release": "60ms", "makeup": "0dB"}],
                   "auto": {"dyn": {"points": lanes()}}},
    }
    with open(OUT, "w") as f:
        json.dump(song, f, indent=1)
    print("wrote", OUT, "bars", BARS)


if __name__ == "__main__":
    main()
