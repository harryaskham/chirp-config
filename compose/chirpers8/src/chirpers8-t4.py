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


class Part:
    def __init__(self):
        self.ev = []

    def add(self, at, ln, head, vel):
        self.ev.append((at, ln, head, int(max(1, min(127, vel)))))

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
        # THE ARRAY AS A MELODY: sixteen notes, each panned by its index (left to right)
        for k, v in enumerate(arr):
            ix = round(-0.9 + 1.8 * k / (N - 1), 3)
            vel = 96 if k in acc else (82 if k % 4 == 0 else 70)
            part("lead").add(b0(bar) + k / 4, 0.22, pitch(v) + f"^ix={ix}", vel)
        # THE WORK, AUDIBLE: a tick per comparison, a hit per swap; a crash when a pass changes nothing / it is done
        for j in cmp:
            part("tick").add(b0(bar) + j / 4, 0.1, "h", 52 + hand.randint(-6, 6))
        for j in sw:
            part("swap").add(b0(bar) + j / 4 + 0.125, 0.15, "rs", 84 + hand.randint(-6, 6))
        if (sw == [] and sec not in ("intro", "sorted", "outro")) or done:
            part("crash").add(b0(bar), 2.0, "cy", 80)
        # v2: THE HARMONY RESPONDS TO ORDER - a triad on the array's first value: a dark 312-cent third while it is
        # unsorted, the 390-cent major third the moment it is sorted
        third = 5 if arr == sorted(arr) else 4
        part("pad").add(b0(bar), BAR - 0.05, ",".join(pitch(arr[0] + s, BASE - 12) for s in (0, third, 9)),
                        78 if arr == sorted(arr) else 64)
        # v2: the outro holds a low E (E2) for its last eight bars - the note t5 begins on
        if bar == BARS - 7:
            part("hum").add(b0(bar), b0(BARS + 1) - b0(bar) - 0.05, "m40.000", 96)
        # THE BASS: the array's first value, two octaves down, an acid line on eighths
        if sec not in ("intro",) or bar > 8:
            for e in range(8):
                v = arr[(e * 2) % N] if e % 2 else arr[0]
                part("bass").add(b0(bar) + e * 0.5, 0.42, pitch(v, BASE - 24), 104 if e % 2 == 0 else 86)
        # DRUMS: the 909's circuits; the bogosort storm has no kick
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


def sorted_show():
    up, down = list(range(N)), list(range(N))[::-1]
    k = 0
    while True:
        yield (up if (k // 8) % 2 == 0 else down)[:], [], [], [0]
        k += 1


def unsort(arr):
    a = list(range(N))
    rng = random.Random(16)
    while True:
        before = a[:]
        i = rng.randrange(N - 1)
        a[i], a[i + 1] = a[i + 1], a[i]
        yield before, [i], [i], []


def lanes():
    level = {"intro": -6, "bubble": -2, "insertion": -2, "quick": 0, "bogo": -4, "merge": 0, "sorted": 0, "outro": -6}
    pts = []
    for name, a, z in SECTIONS:
        if pts:
            pts.append([f"{b0(a) - 0.25:.2f}b", pts[-1][1]])
        pts.append([f"{b0(a):.2f}b", float(level[name])])
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
    lead_patch = {"extends": "arp-pluck", "synth": {"fx": [{"type": "pan", "pan": {"value": 0, "mod": [
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
               auto={"roll": {"points": roll_lane()}, "m": {"points": morph_lane()}},
               fx=[{"type": "morph", "key": "tick", "mode": "morph",            # v3: the tune dissolves into the work
                    "amount": {"value": 0, "mod": [{"src": "auto.m", "amount": 1}]}},
                   {"type": "stutter", "slice": "1/16", "repeats": 6, "roll": 0.6, "pitch": 0.5,
                    "chance": {"value": 0, "mod": [{"src": "auto.roll", "amount": 1}]}}]),
            tr("bass", "acid", gain="-7dB"),
            tr("pad", "juno-pad", gain="-9dB", sends={"dly": "-14dB"}),                    # v2
            tr("hum", "808", gain="-10dB"),                                                # v2: into t5's E2
            tr("tick", "909", gain="-11dB", pan=0.2),
            tr("swap", "909", gain="-6dB", pan=-0.2, sends={"room": "-10dB"}),
            tr("crash", "909", gain="-12dB", sends={"room": "-8dB"}),
            tr("kick", "909", gain="-10dB"),
            tr("clap", "909", gain="-6dB", sends={"room": "-8dB"}),
            tr("hats", "909", gain="-6dB", pan=0.1),
        ],
        "buses": {"room": {"fx": ["reverb kind=room decay=0.9s mix=1 predelay=8ms", "hp cutoff=250"]},
                  "dly": {"fx": ["delay time=3/16 mix=1 feedback=0.35", "hp cutoff=400", "lp cutoff=5000"]}},
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=28", "highshelf cutoff=5000 gain=-3dB"]},
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
