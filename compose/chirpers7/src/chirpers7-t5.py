#!/usr/bin/env python3
"""Chirpers - The Endless Stair (Chirpers VII), track 5: ONE LINE, TWO (chirper-three).

MINIMAL DEEP ACID, B minor (10A), 119.5 -> 120 bpm inside the track (the tape's tempo path). Featured illusion:
AUDITORY STREAMING (van Noorden's gallop). ONE acid line plays low-high-low-rest in sixteenths (A B A -). While its two
notes are a tone apart (B and C#) it is heard as one galloping line. The high note then climbs the tape's STAIR
(C# D F# B, and on up), widening the gap; past half an octave the ear cannot hold it as one line any more: it SPLITS
into two players, a steady eighth-note bass and a syncopated line on the 'e' of every beat, and the GALLOP VANISHES -
though no note's timing has changed. The break pulls the two apart in space, then closes the gap until they fuse back
into one; in the drop the high note climbs the stair every eight bars, so the line fuses, wavers and splits again and
again over a moving root: an endless stair of fission.

FORM (176 bars, ~5:52):
  intro  1-16    the seam in: kick, hats, the 808 holding B (under t4's tail)
  one    17-48   the gallop on B/C# (one line), the filter slowly opening; D from bar 33 (still one, just)
  split  49-80   the high note climbs: F# (49, the ear wavers), B (57), D (65), F# (73): two lines; claps, dub stabs
  break  81-96   no drums: the two streams pan apart, then the gap closes bar by bar until they are one again
  drop   97-144  everything; every eight bars the high note climbs the stair (C# D F# B: one -> two) over B G E F#
  outro  145-176 the seam out: one line again, the filter closing; from 161 kick, hats and the 808 on F# (t6's F#m)
"""
import json
import os
import random

OUT = os.environ.get("C7T5_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers7-t5.yaml")
BAR = 4.0
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
SECTIONS = [("intro", 1, 16), ("one", 17, 48), ("split", 49, 80), ("break", 81, 96), ("drop", 97, 144),
            ("outro", 145, 176)]
BARS = SECTIONS[-1][2]
TOTAL = BARS * BAR
B2 = 47


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def b0(bar):
    return (bar - 1) * BAR


def sec_of(bar):
    for name, a, z in SECTIONS:
        if a <= bar <= z:
            return name
    return "outro"


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
        return " ".join(toks)


P = {}


def part(n):
    return P.setdefault(n, Part())


# the gap (semitones above the low note) of the high note, bar by bar
STAIR = [2, 3, 7, 12]                       # C# D F# B above B: the tape's stair, one line -> two


def gap_at(bar):
    sec = sec_of(bar)
    if sec == "one":
        return 2 if bar < 33 else 3
    if sec == "split":
        return {0: 7, 1: 12, 2: 15, 3: 19}[(bar - 49) // 8]
    if sec == "break":                      # 81-88 wide (19), panned apart; 89-92 the octave at HALF RATE (fused);
        return 19 if bar < 89 else [12, 12, 12, 12, 7, 5, 3, 2][bar - 89]          # 93-96 closing, still slow
    if sec == "drop":
        return STAIR[((bar - 97) % 8) // 2]
    if sec == "outro":
        return 2
    return None


def root_at(bar):
    """The low note: B through the first half; in the drop it walks B G E F# (eight bars each)."""
    if sec_of(bar) == "drop":
        return [B2, B2 - 4, B2 - 7, B2 - 5][((bar - 97) // 8) % 4]
    return B2


def acid():
    """The one line: A B A - in sixteenths; A and B on separate tracks only so the break can pull them apart in
    space (same patch, same level, same place everywhere else: one player)."""
    acc = 0
    for bar in range(17, 161):
        g = gap_at(bar)
        if g is None:
            continue
        lo = root_at(bar)
        if 89 <= bar <= 96:
            # v4: THE RATE: the same gallop in EIGHTHS (A B A -, two cells a bar): slower, the wide gap fuses again
            for cell in range(2):
                t = b0(bar) + cell * 2
                part("acidA").add(t, 0.4, nm(lo), 104 if cell == 0 else 90)
                part("acidB").add(t + 0.5, 0.4, nm(lo + g), 96)
                part("acidA").add(t + 1.0, 0.4, nm(lo), 82)
            continue
        for beat in range(4):
            t = b0(bar) + beat
            part("acidA").add(t, 0.2, nm(lo), 104 if beat == 0 else 84)
            part("acidA").add(t + 0.5, 0.2, nm(lo), 80)
            acc += 1
            part("acidB").add(t + 0.25, 0.2, nm(lo + g), 112 if acc % 3 == 0 else 86)   # a three-step accent


def drums():
    hand = random.Random(5)
    for bar in range(1, BARS + 1):
        sec = sec_of(bar)
        if sec == "break":
            continue
        for b in range(4):
            part("kick").add(b0(bar) + b, 0.5, "k", 112 if b == 0 else 106)
            if bar >= 5:
                part("hats").add(b0(bar) + b + 0.5, 0.25, "oh", 70 + hand.randint(-6, 6))
            if sec in ("split", "drop") or (sec == "one" and bar >= 33):
                for s in (1, 3):
                    if hand.random() < 0.75:
                        part("hats").add(b0(bar) + b + s / 4, 0.1, "h", 56 + hand.randint(-8, 8))
        if sec in ("split", "drop") or (sec == "outro" and bar < 161):
            for b in (1, 3):
                part("clap").add(b0(bar) + b + 0.012, 0.5, "cp", 94 + hand.randint(-4, 4))
        if sec == "drop" and bar % 8 == 0:
            part("clap").add(b0(bar) + 3.75, 0.25, "rs", 80)


def harmony():
    for bar in range(1, BARS + 1):
        sec = sec_of(bar)
        lo = root_at(bar) - 12
        if sec in ("intro", "one") or (sec == "outro" and bar < 161):
            part("sub").add(b0(bar), BAR - 0.1, nm(B2 - 12), 92)
        elif sec in ("split", "drop"):
            part("sub").add(b0(bar), 1.4, nm(lo), 98)
            part("sub").add(b0(bar) + 1.5, 0.4, nm(lo), 78)
            part("sub").add(b0(bar) + 2.5, 1.3, nm(lo), 90)
        elif sec == "break":
            if bar in (81, 89):
                part("sub").add(b0(bar), 8 * BAR - 0.2, nm(B2 - 12), 70)
        elif sec == "outro":
            part("sub").add(b0(bar), BAR - 0.1, nm(B2 - 17), 92)          # F#1: the fifth, t6's tonic
        # THE DUB STABS: a minor-ninth chord on the root, on the 'and' of two and four, into a delay
        if (sec == "split" and bar >= 57) or sec == "drop":
            r = root_at(bar) + 12
            minor = r in (B2 + 12, B2 + 5)                               # Bm, Em minor; G major; F# a sus
            v = [r, r + (3 if minor else 4), r + 7, r + 10 if minor else r + 11, r + 14]
            if r == B2 + 7:                                              # F#: a sus4 with the seventh
                v = [r, r + 5, r + 7, r + 10]
            for b in (1.5, 3.5):
                part("stab").add(b0(bar) + b, 0.22, ",".join(nm(m) for m in v), 82)


LEVEL = {"intro": -8, "one": -5, "split": -2, "break": -9, "drop": 0, "outro": -6}


def lanes():
    dyn = []
    for name, a, z in SECTIONS:
        if dyn:
            dyn.append([f"{b0(a) - 0.25:.2f}b", dyn[-1][1]])
        dyn.append([f"{b0(a):.2f}b", float(LEVEL[name])])
    # the acid's filter opening (octaves above its base): slow through 'one', open for the split, breathing in the drop
    op = [["0b", 0.0], [f"{b0(17)}b", 0.0], [f"{b0(49)}b", 1.2], [f"{b0(81)}b", 1.4], [f"{b0(89)}b", 0.6],
          [f"{b0(97)}b", 1.0], [f"{b0(145)}b", 1.4], [f"{b0(161)}b", 0.0], [f"{TOTAL}b", 0.0]]
    # the break's spatial split: A to the left, B to the right, and back together as the gap closes
    pan = [["0b", 0.0], [f"{b0(81)}b", 0.0], [f"{b0(86)}b", 0.7], [f"{b0(88)}b", 0.7], [f"{b0(91)}b", 0.0],
           [f"{TOTAL}b", 0.0]]
    return dyn, op, pan


def main():
    acid()
    drums()
    harmony()
    dyn, op, pan = lanes()
    tempo = [{"at": "0b", "bpm": 119.5}, {"at": f"{b0(145):.0f}b", "bpm": 120, "ramp": True}]
    pump = {"type": "pump", "on": "kick", "depth": "-7dB", "attack": "3ms", "release": "330ms", "curve": 0.7}
    acid_fx = lambda: [{"type": "filter", "kind": "lp", "q": 0.9,
                        "cutoff": {"value": 900, "mod": [{"src": "auto.op", "amount": 1.0},
                                                         {"src": "lfo.res", "amount": 0.5}]}}]
    tr = lambda n, patch, **kw: dict({"name": n, "patch": patch, "score": part(n).score()}, **kw)
    acid_tr = lambda n, side: tr(n, "acid", gain="-2dB", sends={"room": "-14dB"},
                                 lfo={"res": {"wave": "sine", "rate": "28b"}},          # seven bars: never on the four
                                 auto={"op": {"points": op}, "pan": {"points": pan}},
                                 pan={"value": 0, "mod": [{"src": "auto.pan", "amount": side}]}, fx=acid_fx())
    song = {
        "about": "Chirpers - The Endless Stair (Chirpers VII), track 5 by chirper-three: ONE LINE, TWO. Minimal deep acid "
                 "in B minor; the auditory-streaming illusion: one acid line galloping between two notes splits into two "
                 "lines as its high note climbs the tape's stair, and fuses again. Generated by "
                 "compose/chirpers7/src/chirpers7-t5.py.",
        "tempo": tempo,
        "tail": "0.1s",                          # end on the last bar: the DJ mixes out of it (chirper-one's finding)
        "loudness": -11,
        "buses": {"room": {"fx": ["reverb kind=room decay=1.2s mix=1 predelay=12ms", "hp cutoff=250"]},
                  "dub": {"fx": ["delay time=3/16 mix=1 feedback=0.55", "hp cutoff=400", "lp cutoff=3000",
                                 "reverb kind=hall decay=2.5s mix=0.3"]}},
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=30", "peak cutoff=350 q=0.8 gain=-2dB",
                                                    "highshelf cutoff=7000 gain=4dB"]},
                          {"type": "compressor", "threshold": "-20dB", "ratio": 2.5, "attack": "15ms", "release": "150ms",
                           "makeup": "0dB"},
                          {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                          {"type": "gain", "gain": "+8dB"},
                          {"type": "compressor", "threshold": "-10dB", "ratio": 8, "attack": "1ms", "release": "60ms",
                           "makeup": "0dB"}],    # catch the kick's peaks; the song's loudness masters (true-peak limited)
                   "auto": {"dyn": {"points": dyn}}},
        "tracks": [
            tr("kick", "machine-kit", gain="-12dB"),
            tr("hats", "machine-kit", gain="-5dB", pan=0.1, lfo={"hh": {"wave": "sine", "rate": "20b"}},
               fx=[{"type": "filter", "kind": "hp", "cutoff": {"value": 2500, "mod": [{"src": "lfo.hh", "amount": 0.7}]}}]),
            tr("clap", "machine-kit", gain="-7dB", sends={"room": "-8dB"}),
            tr("sub", "808", gain="-12dB", fx=[{"type": "phantom", "harmonics": "-6dB", "odd": 0.4, "remove": 0.0}, pump]),
            acid_tr("acidA", -1.0),
            acid_tr("acidB", 1.0),
            tr("stab", "juno-pad", gain="-13dB", sends={"dub": "-4dB"}, lfo={"sl": {"wave": "sine", "rate": "36b"}},
               fx=[{"type": "filter", "kind": "bp", "q": 0.7,
                    "cutoff": {"value": 900, "mod": [{"src": "lfo.sl", "amount": 0.8}]}}, pump]),
        ],
    }
    with open(OUT, "w") as f:
        json.dump(song, f, indent=1)
        f.write("\n")
    print(f"wrote {OUT}: {BARS} bars")


if __name__ == "__main__":
    main()
