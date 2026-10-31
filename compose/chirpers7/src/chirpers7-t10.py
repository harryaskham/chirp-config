#!/usr/bin/env python3
"""Chirpers - The Endless Stair (Chirpers VII), track 10: THE NOTE IN THE SILENCE (chirper-three).

DEEP HYPNOTIC HOUSE, D# minor (2A), 122 -> 122.5 bpm inside the track (the tape's tempo path). Featured illusion:
THE ZWICKER TONE. After a few seconds of loud noise with a notch cut out of it, a faint tone is heard in the silence that
follows, at a pitch inside the notch - and nothing plays it. Each of the four breaks is a swell of notched noise and
then a whole bar of SILENCE in which the ear hears the missing note; the music comes back with a glockenspiel playing
EXACTLY that note, so the phantom turns real. The four notches are THE STAIR (D# F F# A#): the tape's thread heard as
after-tones in four silences, and after the last one the bell plays the whole stair.
The groove: a reese bass, a Rhodes on the sixteenth 'a's (3 and 11), a rim on a dotted-eighth cycle that runs across
the bar lines, kick and hats; the Rhodes chord moves on as each break adds a step.

FORM (176 bars, ~5:46):
  intro  1-16    the seam in: kick, hats, the sub holding D#1 (from t9's outro)
  A      17-40   the groove
  Z1     41-44   noise with a notch at D# swelling (41-43); bar 44 silence; the bell answers D# at 45
  B      45-72   the groove with the bell's D#
  Z2     73-76   the notch at F; silence; the bell answers F
  C      77-104  a new bass figure; the bell D# F
  Z3     105-108 the notch at F#; silence; the bell answers F#
  D      109-136 the full drop; the bell D# F F#
  Z4     137-140 the notch at A#; silence; the bell plays the whole stair
  E      141-152 the peak: the stair complete
  outro  153-176 the seam out: kick, hats, the sub on D# (Eb: t11's E-flat minor, the same key)
"""
import json
import os
import random

OUT = os.environ.get("C7T10_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers7-t10.yaml")
BAR = 4.0
NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
SECTIONS = [("intro", 1, 16), ("A", 17, 40), ("Z1", 41, 44), ("B", 45, 72), ("Z2", 73, 76), ("C", 77, 104),
            ("Z3", 105, 108), ("D", 109, 136), ("Z4", 137, 140), ("E", 141, 152), ("outro", 153, 176)]
BARS = SECTIONS[-1][2]
TOTAL = BARS * BAR
DS1 = 27                                     # D#1
STAIR = [75, 77, 78, 82]                     # D#5 F5 F#5 A#5: the notches and the bell's answers
BREAKS = {"Z1": 0, "Z2": 1, "Z3": 2, "Z4": 3}
ZSTART = {0: 41, 1: 73, 2: 105, 3: 137}


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


# the chord walk, two bars each, growing as the stair grows: D#m9 | Bmaj7 | G#m9 | A#7sus
CHORDS = [(DS1 + 24, [54, 58, 61, 65]), (DS1 + 20, [51, 54, 58, 61]), (DS1 + 17, [51, 54, 56, 59]),
          (DS1 + 19, [53, 56, 58, 61])]
BASS_A = [(0, 0.45, 0), (0.75, 0.2, 0), (1.5, 0.45, 7), (2.5, 0.2, 0), (2.75, 0.45, 10), (3.5, 0.3, 12)]
BASS_C = [(0, 0.7, 0), (1.25, 0.2, 12), (1.75, 0.45, 7), (3.0, 0.45, 3), (3.75, 0.2, 5)]


def zwicker():
    """The breaks: notched noise swelling for three bars, then a bar of silence (nothing at all plays), then the bell."""
    for k, z in ZSTART.items():
        for i in range(3):
            part(f"nz{k}").add(b0(z + i), BAR, "C4", [72, 92, 112][i])
        # each break its own colour under the noise, clear of the notch: a reese drone, the Rhodes held, the bell's steps
        if k == 1:
            part("bass").add(b0(z), 3 * BAR - 0.1, nm(DS1 + 12), 90)
        elif k == 2:
            part("rhodes").add(b0(z), 3 * BAR - 0.1, ",".join(nm(m) for m in CHORDS[0][1]), 70)
        elif k == 3:
            for j, m in enumerate(STAIR[:3]):
                part("bell").add(b0(z) + 2 * j * BAR / 2, 2.5, nm(m), 60)
        nxt = z + 4
        if k < 3:
            part("bell").add(b0(nxt), 3.0, nm(STAIR[k]), 100)
        else:
            for j, m in enumerate(STAIR):                                     # the whole stair, at last
                part("bell").add(b0(nxt) + j, 1.5, nm(m), 96 + 4 * j)


def is_break(bar):
    return sec_of(bar) in BREAKS


def drums():
    hand = random.Random(10)
    cyc = 0                                                                  # the dotted-eighth rim, across bar lines
    for bar in range(1, BARS + 1):
        sec = sec_of(bar)
        if is_break(bar):
            continue
        for b in range(4):
            part("kick").add(b0(bar) + b, 0.5, "k", 114 if b == 0 else 106)
            part("hats").add(b0(bar) + b + 0.5, 0.25, "oh", 68 + hand.randint(-6, 6))
            if sec not in ("intro",):
                for s in (1, 3):
                    if hand.random() < 0.7:
                        part("hats").add(b0(bar) + b + s / 4, 0.1, "h", 50 + hand.randint(-8, 8))
        if sec not in ("intro",) and not (sec == "outro" and bar >= 161):
            for s in range(16):
                if (cyc + s) % 3 == 0:
                    part("rim").add(b0(bar) + s / 4, 0.2, "rs", 64 + hand.randint(-8, 8))
            cyc = (cyc + 16) % 3
        if sec not in ("intro", "A") or (sec == "A" and bar >= 25):
            if not (sec == "outro" and bar >= 161):
                for b in (1, 3):
                    part("clap").add(b0(bar) + b + 0.012, 0.5, "cp", 92 + hand.randint(-4, 4))


def harmony():
    for bar in range(1, BARS + 1):
        sec = sec_of(bar)
        if is_break(bar):
            continue
        root, v = CHORDS[((bar - 1) // 2) % 4]
        if sec in ("intro", "outro"):
            part("sub").add(b0(bar), BAR - 0.1, nm(DS1), 72 if sec == "intro" else 92)   # the head meets t9's tail
            continue
        fig = BASS_C if sec in ("C", "D", "E") else BASS_A
        for at, ln, iv in fig:
            part("bass").add(b0(bar) + at, ln, nm(root - 24 + 12 + iv), 100 if at == 0 else 84)
        sr = root - 24 if root - 24 >= DS1 else root - 12                    # never below D#1
        part("sub").add(b0(bar), 1.8, nm(sr), 96)
        part("sub").add(b0(bar) + 2, 1.8, nm(sr), 90)
        # the Rhodes on the sixteenth 'a's (3 and 11), and from C a third hit on 14
        hits = (0.75, 2.75) + ((3.5,) if sec in ("C", "D", "E") else ())
        up = 12 if (sec == "B" and bar >= 61) else 0               # v3: B's second half lifts an octave
        rh = "rhodesdub" if sec in ("D", "E") else "rhodes"           # v3: the dub chords arrive with the full drop
        for h in hits:
            part(rh).add(b0(bar) + h, 0.6, ",".join(nm(m + up) for m in v), 90)
        # the bell keeps the steps it has been given, on the off-beat of one
        k = {"B": 1, "C": 2, "D": 3, "E": 4}.get(sec, 0)
        if k and bar % 2 == 1 and not bar == ZSTART.get(k - 1, 0) + 4:
            for j in range(k):
                part("bell").add(b0(bar) + 0.5 + j * 0.75, 0.6, nm(STAIR[j]), 72 + 4 * j)


LEVEL = {"intro": -8, "A": -4, "B": -3, "C": -2, "D": 0, "E": 0, "outro": -5, "Z1": -2, "Z2": -2, "Z3": -2, "Z4": -1}


def lanes():
    dyn = []
    for name, a, z in SECTIONS:
        if dyn:
            dyn.append([f"{b0(a) - 0.25:.2f}b", dyn[-1][1]])
        dyn.append([f"{b0(a):.2f}b", float(LEVEL[name])])
    return dyn


def main():
    zwicker()
    drums()
    harmony()
    tempo = [{"at": "0b", "bpm": 122}, {"at": f"{b0(17):.0f}b", "bpm": 122},
             {"at": f"{b0(153):.0f}b", "bpm": 122.5, "ramp": True}]
    pump = {"type": "pump", "on": "kick", "depth": "-7dB", "attack": "3ms", "release": "320ms", "curve": 0.7}
    tr = lambda n, patch, **kw: dict({"name": n, "patch": patch, "score": part(n).score()}, **kw)
    noise = {"synth": {"layers": ["noise"], "amp": {"a": "40ms", "d": 0, "s": 1, "r": "8ms"}}}
    nz = []
    for k, m in enumerate(STAIR):
        f = 440 * 2 ** ((m - 69) / 12) * 1.08              # centred a little above the note: the after-tone sits low
        nz.append(tr(f"nz{k}", noise, gain="-8dB",
                     fx=[{"type": "filter", "kind": "notch", "cutoff": round(f * r, 1), "q": 1.5} for r in (0.9, 1.0, 1.1)]
                        + [{"type": "filter", "kind": "lp", "cutoff": [9000, 6000, 12000, 4000][k]},
                           {"type": "filter", "kind": "hp", "cutoff": 120}]))
    song = {
        "about": "Chirpers - The Endless Stair (Chirpers VII), track 10 by chirper-three: THE NOTE IN THE SILENCE. Deep "
                 "hypnotic house in D# minor; the Zwicker-tone illusion: notched noise, then silence, and a faint tone "
                 "heard where nothing plays - answered by a bell on that very note; the four notches are the tape's "
                 "stair. Generated by compose/chirpers7/src/chirpers7-t10.py.",
        "tempo": tempo,
        "tail": "0.1s",                          # end on the last bar: the DJ mixes out of it (chirper-one's finding)
        "loudness": -11,
        "volume": "0dB",
        "buses": {"room": {"fx": ["reverb kind=room decay=1.0s mix=1 predelay=10ms", "hp cutoff=250"]},
                  "hall": {"fx": ["reverb kind=hall decay=2.6s mix=1 predelay=25ms", "hp cutoff=300"]},
                  "dub": {"fx": ["delay time=3/16 mix=1 feedback=0.5", "hp cutoff=450", "lp cutoff=3200",
                                 "reverb kind=hall decay=2.2s mix=0.25"]}},
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=28", "lowshelf cutoff=200 gain=-3dB",
                                                    "highshelf cutoff=5000 gain=3dB"]},
                          {"type": "compressor", "threshold": "-20dB", "ratio": 2.5, "attack": "15ms", "release": "150ms",
                           "makeup": "0dB"},
                          {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                          {"type": "gain", "gain": "+8dB"},
                          {"type": "compressor", "threshold": "-12dB", "ratio": 8, "attack": "0.3ms", "release": "60ms",
                           "makeup": "0dB"}],
                   "auto": {"dyn": {"points": lanes()}}},
        "tracks": [
            tr("kick", "machine-kit", gain="-11dB"),
            tr("hats", "machine-kit", gain="0dB", pan=0.1, lfo={"hh": {"wave": "sine", "rate": "20b"}},
               fx=[{"type": "filter", "kind": "hp", "cutoff": {"value": 3000, "mod": [{"src": "lfo.hh", "amount": 0.6}]}}]),
            tr("rim", "machine-kit", gain="-3dB", pan=-0.3, sends={"room": "-10dB"}),
            tr("clap", "machine-kit", gain="0dB", sends={"room": "-8dB"}),
            tr("bass", "reese", gain="-8dB", lfo={"rb": {"wave": "sine", "rate": "28b"}},
               fx=[{"type": "filter", "kind": "lp", "q": 0.9,
                    "cutoff": {"value": 600, "mod": [{"src": "lfo.rb", "amount": 0.8}]}}, pump]),
            tr("sub", "sub-sine", gain="-13dB", fx=[pump]),
            tr("rhodes", "epiano-tine synth.tine.sense=0.3", gain="-5dB", pan=-0.15, sends={"hall": "-10dB"},
               lfo={"rl": {"wave": "sine", "rate": "36b"}},
               fx=[{"type": "filter", "kind": "lp", "cutoff": {"value": 4000, "mod": [{"src": "lfo.rl", "amount": 0.7}]}},
                   pump]),
            tr("rhodesdub", "epiano-tine synth.tine.sense=0.3", gain="-5dB", pan=-0.15,
               sends={"hall": "-10dB", "dub": "-5dB"},   # v3: DUB CHORDS in D and E: each stab trails dotted-eighth echoes
               fx=[{"type": "filter", "kind": "lp", "cutoff": 4000}, pump]),
            tr("bell", "glock", gain="-8dB", pan=0.2, sends={"hall": "-6dB"}),
        ] + nz,
    }
    with open(OUT, "w") as f:
        json.dump(song, f, indent=1)
        f.write("\n")
    print(f"wrote {OUT}: {BARS} bars")


if __name__ == "__main__":
    main()
