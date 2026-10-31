#!/usr/bin/env python3
"""Chirpers - The Endless Stair (Chirpers VII), track 9: WHERE'S THE ONE (chirper-three).

DEEP MINIMAL TECH-HOUSE, G# minor (1A), 121.5 -> 122 bpm inside the track (the tape's tempo path). Featured illusion:
THE BEAT FLIP (a phantom downbeat). A groove whose stabs and bass accents sit on the off-beats; take the kick away and
the ear re-anchors on them; bring the kick back an eighth LATE, on those off-beats, and the whole groove runs displaced
while sounding perfectly normal; then stop it, leave two bars of doubt, and bring the kick back on the TRUE beat -
which for a few bars sounds like it's on the off-beat, until the claps pull the ear home. In the break a hemiola (the
riff grouped in threes over the four) and a voice saying "one" where the ear thinks the one is: never on the real one.
THE STAIR (G# A# B D#) is a pluck figure that starts on the off-beat, the flip in miniature.

FORM (176 bars, ~5:47):
  intro  1-16    the seam in: kick, hats, the 808 holding G# (t8's C# minor hands a fifth up)
  A      17-40   the groove: kick on the beat, stabs and riff accents on the off-beats, claps 2 and 4
  turn   41-56   41-44 the kick and hats gone (the off-beats become the beat); 45-56 the kick returns DISPLACED, on
                 the off-beats, with the claps on the displaced backbeat: the flipped groove, heard as normal
  back   57-72   57-58 nothing but the stab (doubt); the kick returns on the TRUE beat (heard as the off-beat), the
                 claps on 2 and 4 from 61 pull it home
  break  73-88   no kick: the riff in threes against the four (a hemiola), a pad, the voice counting "one" on the
                 hemiola's accent
  drop   89-136  everything; at 105-112 a quick flip (four bars displaced) and back; the stair on the off-beat
  outro  137-176 the seam out: back on the true beat, thinning; from 161 kick, hats and the 808 on D# (t10's D#m)
"""
import json
import os
import random

OUT = os.environ.get("C7T9_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers7-t9.yaml")
BAR = 4.0
NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
SECTIONS = [("intro", 1, 16), ("A", 17, 40), ("turn", 41, 56), ("back", 57, 72), ("break", 73, 88), ("drop", 89, 136),
            ("outro", 137, 176)]
BARS = SECTIONS[-1][2]
TOTAL = BARS * BAR
GS1 = 32                                     # G#1
FLIP_DISPLACED = [(45, 56), (107, 112), (131, 131)]   # the kick (and claps) an eighth late; v6: bar 131, once, no
# warning - the doubt comes back late and short, and the listener who has learned the trick is caught again (chirper-zero)
KEY_UP = (81, 88)                            # v6: the counted hemiola a fourth up, C# minor: time and key move together
KICKLESS = [(41, 44), (57, 58), (73, 88), (105, 106)]
# v4: THE PHANTOM DOWNBEAT itself: every eighth bar of the groove and the drop, beat one is a hole - no kick, bass, sub,
# stab or hat on the one - and the ear supplies the downbeat that isn't played
GHOST_ONE = {24, 32, 40, 96, 104, 120, 128, 136}


def hole(bar, at):
    return bar in GHOST_ONE and at - b0(bar) < 1.0


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def b0(bar):
    return (bar - 1) * BAR


def sec_of(bar):
    for name, a, z in SECTIONS:
        if a <= bar <= z:
            return name
    return "outro"


def within(bar, spans):
    return any(a <= bar <= z for a, z in spans)


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


# the riff on the sixteenth grid: (position, semitones over the root); its accents fall on the off-beats (2 6 10 14)
RIFF = [(0, 0), (2, 0), (3, 7), (6, 0), (8, -2), (10, 0), (11, 3), (14, 5)]
ROOTS = [GS1, GS1, GS1 - 4, GS1 - 2]          # G#m | G#m | E | F# (a bar each)
ROOTS_DROP = [GS1, GS1 - 4, GS1 + 3, GS1 - 2]  # the drop walks somewhere new: G#m | E | B | F#


def root_of(bar):
    return (ROOTS_DROP if sec_of(bar) == "drop" else ROOTS)[(bar - 1) % 4]


def minor_at(bar):
    return root_of(bar) == GS1


def riff():
    for bar in range(17, 161):
        sec = sec_of(bar)
        root = root_of(bar)
        if sec == "break":
            # THE HEMIOLA: the riff's cell (three eighths: root, fifth, root an octave up) over and over against the four
            k0 = (bar - 73) * 8
            for e in range(8):
                k = k0 + e
                note = [0, 7, 12][k % 3] + (5 if KEY_UP[0] <= bar <= KEY_UP[1] else 0)
                part("bass").add(b0(bar) + e * 0.5, 0.4, nm(GS1 + note), 88 if k % 3 == 0 else 58)   # v5: hushed
            continue
        up = 12 if sec == "back" else 0                       # the return comes back changed: an octave up, lighter
        for pos, iv in RIFF:
            acc = pos in (2, 6, 10, 14)
            if sec == "outro" and not acc:                       # the outro thins to the accents
                continue
            if hole(bar, b0(bar) + pos / 4):
                continue
            part("bass").add(b0(bar) + pos / 4, 0.22, nm(root + iv + up), 104 if acc else 80)


def drums():
    hand = random.Random(9)
    for bar in range(1, BARS + 1):
        sec = sec_of(bar)
        disp = within(bar, FLIP_DISPLACED)
        off = 0.5 if disp else 0.0
        if not within(bar, KICKLESS):                            # v2: to the last bar (the seam into t10)
            for b in range(4):
                if hole(bar, b0(bar) + b + off):
                    continue
                part("kick").add(b0(bar) + b + off, 0.5, "k", 114 if b == 0 else 106)
        if sec == "break" or within(bar, [(41, 44), (57, 60), (105, 106)]):
            continue
        for b in range(4):
            if bar >= 5 and not hole(bar, b0(bar) + b + 0.5 - off):
                part("hats").add(b0(bar) + b + 0.5 - off, 0.25, "oh", 68 + hand.randint(-6, 6))   # always opposite the kick
            if sec in ("A", "drop") or (sec == "back" and bar >= 65):
                for s in (1, 3):
                    if hand.random() < 0.7:
                        if not hole(bar, b0(bar) + b + s / 4):
                            part("hats").add(b0(bar) + b + s / 4, 0.1, "h", 52 + hand.randint(-8, 8))
        if (sec in ("A", "turn", "drop") and bar >= 25) or (sec == "back" and bar >= 61) or (sec == "outro" and bar < 161):
            for b in (1, 3):
                part("clap").add(b0(bar) + b + off + 0.012, 0.5, "cp", 94 + hand.randint(-4, 4))
        if sec == "drop" and bar % 4 == 0:
            part("clap").add(b0(bar) + 3.75, 0.25, "rs", 82)


def stabs():
    """G#m9 on the off-beats: the anchor the ear moves to when the kick goes."""
    for bar in range(17, 145):
        sec = sec_of(bar)
        if sec == "break":
            continue
        r = root_of(bar) + 24
        minor = minor_at(bar)
        v = [r + (3 if minor else 4), r + 7, r + (10 if minor else 11), r + 14]
        hits = (0.75, 1.5, 2.75, 3.5) if (sec == "drop" and bar >= 121) else (0.5, 1.5, 2.5, 3.5)   # the anchor shifts
        for b in hits:
            if hole(bar, b0(bar) + b):
                continue
            part("stab").add(b0(bar) + b, 0.18, ",".join(nm(m) for m in v), 84 if b in (0.5, 0.75, 2.5, 2.75) else 72)


def sub_and_pad():
    for bar in range(1, BARS + 1):
        sec = sec_of(bar)
        root = root_of(bar)                            # the 808 on the riff's root
        if sec == "intro" or (sec == "outro" and bar < 161):
            part("sub").add(b0(bar), BAR - 0.1, nm(GS1), 92)
        elif sec == "outro":
            part("sub").add(b0(bar), BAR - 0.1, nm(GS1 - 5), 120)           # D#1: the fifth, t10's D# minor (full: the seam)
        elif sec == "break":
            if bar == 73:
                part("pad").add(b0(bar), 8 * BAR - 0.1, ",".join(nm(m) for m in (56, 59, 63, 66, 70)), 70)
            elif bar == 81:                                  # v6: C#m9 for the counted bars (chirper-one's fourth)
                part("pad").add(b0(bar), 8 * BAR - 0.1, ",".join(nm(m) for m in (61, 64, 68, 71, 75)), 72)
        elif not within(bar, [(41, 44), (57, 58)]):
            if bar in GHOST_ONE:
                part("sub").add(b0(bar) + 1.0, 0.6, nm(root), 100)        # the one left empty
            else:
                part("sub").add(b0(bar), 1.6, nm(root), 100)
            part("sub").add(b0(bar) + 2, 1.6, nm(root), 92)


def stair_and_voice():
    # THE STAIR on a pluck, starting on the off-beat (the flip in miniature)
    for bar in list(range(33, 41, 2)) + list(range(121, 137, 4)):
        for k, iv in enumerate((0, 2, 3, 7)):
            part("stair").add(b0(bar) + 0.5 + k * 0.75, 0.6, nm(GS1 + 36 + iv), 78 + 5 * k)
    # the voice counting "one" where the hemiola puts its accent (every three eighths): never on the true one
    # v2: from bar 81 the voice COUNTS the hemiola aloud - one, two, three on its dotted-quarter pulse, against the
    # bar's four - talking the ear into the wrong meter; then "one" on the TRUE downbeat as the drop lands (bar 89)
    words = [("w-ah1-n", "0>-20", 0), ("t-uw1", "0>-10", -2), ("th-r-iy1", "0>-30", -4)]
    for k in range(int((b0(89) - b0(81)) * 2 // 3)):             # every three eighths from bar 81
        at = b0(81) + k * 1.5
        if at >= b0(89) - 0.5:
            break
        ph, f0, dv = words[k % 3]
        part("voice").add(at, 0.5, f"C#4^ph={ph}^f0={f0}", 82 + dv)          # v6: counting in C#
    for bar in range(77, 81, 2):                                  # before the count: a lone "one" in the wrong place
        part("voice").add(b0(bar) + 1.5, 0.45, "G#3^ph=w-ah1-n^f0=0>-20", 78)
    part("voice").add(b0(89), 0.6, "B3^ph=w-ah1-n^f0=0>-60", 100)    # home


LEVEL = {"intro": -8, "A": -4, "turn": -3, "back": -3, "break": -8, "drop": 0, "outro": -5}


def lanes():
    dyn = []
    for name, a, z in SECTIONS:
        if dyn:
            dyn.append([f"{b0(a) - 0.25:.2f}b", dyn[-1][1]])
        dyn.append([f"{b0(a):.2f}b", float(LEVEL[name])])
    return dyn


def main():
    riff()
    drums()
    stabs()
    sub_and_pad()
    stair_and_voice()
    tempo = [{"at": "0b", "bpm": 121.5}, {"at": f"{b0(17):.0f}b", "bpm": 121.5},
             {"at": f"{b0(137):.0f}b", "bpm": 122, "ramp": True}]
    pump = {"type": "pump", "on": "kick", "depth": "-7dB", "attack": "3ms", "release": "320ms", "curve": 0.7}
    tr = lambda n, patch, **kw: dict({"name": n, "patch": patch, "score": part(n).score()}, **kw)
    song = {
        "about": "Chirpers - The Endless Stair (Chirpers VII), track 9 by chirper-three: WHERE'S THE ONE. Deep minimal "
                 "tech-house in G# minor; the beat-flip illusion (a phantom downbeat): the kick leaves, the ear re-anchors "
                 "on the off-beats, the kick returns an eighth late and sounds normal, then returns on the true beat and "
                 "sounds wrong; a hemiola break with a voice counting 'one' in the wrong place. Generated by "
                 "compose/chirpers7/src/chirpers7-t9.py.",
        "tempo": tempo,
        "tail": "0.1s",                          # end on the last bar: the DJ mixes out of it (chirper-one's finding)
        "loudness": -11,
        "volume": "0dB",
        "buses": {"room": {"fx": ["reverb kind=room decay=1.1s mix=1 predelay=10ms", "hp cutoff=250"]},
                  "dub": {"fx": ["delay time=3/16 mix=1 feedback=0.45", "hp cutoff=500", "lp cutoff=3500",
                                 "reverb kind=hall decay=2.2s mix=0.3"]}},
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=28", "lowshelf cutoff=200 gain=-3dB",
                                                    "highshelf cutoff=5000 gain=4dB"]},
                          {"type": "compressor", "threshold": "-20dB", "ratio": 2.5, "attack": "15ms", "release": "150ms",
                           "makeup": "0dB"},
                          {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                          {"type": "gain", "gain": "+8dB"},
                          {"type": "compressor", "threshold": "-12dB", "ratio": 8, "attack": "0.3ms", "release": "60ms",
                           "makeup": "0dB"}],
                   "auto": {"dyn": {"points": lanes()}}},
        "tracks": [
            tr("kick", "machine-kit", gain="-14dB"),
            tr("hats", "machine-kit", gain="3dB", pan=0.1, lfo={"hh": {"wave": "sine", "rate": "20b"}},
               fx=[{"type": "filter", "kind": "hp", "cutoff": {"value": 3000, "mod": [{"src": "lfo.hh", "amount": 0.6}]}}]),
            tr("clap", "machine-kit", gain="-3dB", sends={"room": "-8dB"}),
            tr("bass", "acid", gain="-6dB", lfo={"bc": {"wave": "sine", "rate": "36b"}},
               auto={"dk": {"points": [["0b", 0.0], [f"{b0(73)}b", 0.0], [f"{b0(76)}b", -1.5], [f"{b0(87)}b", -1.5],
                                       [f"{b0(89)}b", 0.0], [f"{TOTAL}b", 0.0]]}},     # v5: the break goes dark
               fx=[{"type": "filter", "kind": "lp", "q": 0.8,
                    "cutoff": {"value": 700, "mod": [{"src": "lfo.bc", "amount": 0.9},
                                                     {"src": "auto.dk", "amount": 1.0}]}}, pump]),
            tr("sub", "808", gain="-21dB", fx=[{"type": "filter", "kind": "lp", "cutoff": 100}, pump]),
            tr("stab", "juno-pad", gain="-4dB", pan=-0.15, sends={"dub": "-6dB"}, lfo={"sl": {"wave": "sine", "rate": "28b"}},
               fx=[{"type": "filter", "kind": "bp", "q": 0.8,
                    "cutoff": {"value": 1400, "mod": [{"src": "lfo.sl", "amount": 0.8}]}}, pump]),
            tr("pad", "juno-pad", gain="-8dB", sends={"dub": "-10dB"},
               fx=[{"type": "filter", "kind": "lp", "cutoff": 2200}]),
            tr("stair", "celesta", gain="-8dB", pan=0.3, sends={"dub": "-4dB"}),
            tr("voice", "voice-speech", gain="-6dB", pan=-0.2, sends={"dub": "-8dB"},
               fx=[{"type": "filter", "kind": "hp", "cutoff": 150}]),
        ],
    }
    with open(OUT, "w") as f:
        json.dump(song, f, indent=1)
        f.write("\n")
    print(f"wrote {OUT}: {BARS} bars")


if __name__ == "__main__":
    main()
