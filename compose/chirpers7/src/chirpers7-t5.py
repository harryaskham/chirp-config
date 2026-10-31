#!/usr/bin/env python3
"""Chirpers - The Endless Stair (Chirpers VII), track 5: SAY IT AGAIN (chirper-three).

DEEP SOULFUL HOUSE, B minor (10A), 119.5 -> 120 bpm inside the track (the tape's tempo path). Featured illusion:
SPEECH-TO-SONG. A spoken phrase, "Just one more step, and we're home", loops over a bare groove. It is speech (the
voice engine speaking, each syllable with a speaking glide), but its speaking pitches sit secretly on the tape's
STAIR (degrees 1 2 3 5: B C# D F#): C#3 C#3 D3 F#3 | D3 C#3 B2. Repeated, the ear begins to hear it sing; then the
Rhodes starts doubling the very pitches the voice has been speaking, the chords harmonise it, and in the drop a soft
lead sings it two octaves up. In the break the phrase returns alone and still sounds sung - and it repeats every
seven beats instead of eight, sliding against the bar.

FORM (176 bars, ~5:52):
  intro  1-16    the seam in: a minimal kick, hats, the sub on B (under t4's tail)
  speech 17-48   the phrase spoken every two bars over the groove alone; nothing pitched but the sub
  song   49-80   the Rhodes doubles the voice's pitches (quietly, then fully); the chords and the bass arrive
  break  81-96   no drums: the phrase alone over a pad, every SEVEN beats (it drifts against the bar)
  drop   97-144  everything, a soft lead singing the phrase two octaves up; the stair rising on celesta
  outro  145-176 the seam out: stripping back, the bass settling on F# (t6's F# minor)
"""
import json
import os
import random

OUT = os.environ.get("C7T5_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers7-t5.yaml")
BAR = 4.0
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
SECTIONS = [("intro", 1, 16), ("speech", 17, 48), ("song", 49, 80), ("break", 81, 96), ("drop", 97, 144),
            ("outro", 145, 176)]
BARS = SECTIONS[-1][2]
TOTAL = BARS * BAR


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


# THE PHRASE: (beat, length, phonemes, speaking pitch (MIDI), f0 glide)
PHRASE = [(0.0, 0.45, "jh-ah1-s-t", 49, "0>15>0"), (0.5, 0.45, "w-ah1-n", 49, "0>-10"),
          (1.0, 0.45, "m-ao1-r", 50, "0>-10"), (1.5, 0.8, "s-t-eh1-p", 54, "0>20>-30"),
          (2.6, 0.35, "ae1-n-d", 50, "0>-10"), (3.0, 0.4, "w-ih1-r", 49, "0>-10"),
          (3.45, 1.2, "hh-ow1-m", 47, "0>-30>-90")]
# chords, two bars each: Bm9 | Gmaj7 | Em9 | F#7sus
CHORDS = [(35, [57, 61, 62, 66]), (31, [54, 59, 62, 66]), (28, [55, 59, 62, 66]), (30, [52, 54, 59, 61])]


def chord_at(bar):
    return CHORDS[((bar - 1) // 2) % 4]


def phrase_at(at, voice=True, rhodes=0, lead=0, vel=84):
    for beat, ln, ph, m, f0 in PHRASE:
        if voice:
            part("voice").add(at + beat, ln, f"{nm(m)}^ph={ph}^f0={f0}", vel - (6 if ph.endswith("0") else 0))
        if rhodes:
            part("rhodes").add(at + beat, ln * 0.95, nm(m + 12), rhodes)
        if lead:
            part("lead").add(at + beat, ln * 0.95, nm(m + 24), lead)


def voice_line():
    for bar in range(17, 145, 2):
        sec = sec_of(bar)
        if sec == "break":
            continue
        g = bar - 49
        rh = 0 if sec == "speech" else (40 + min(g, 16) * 2 if sec == "song" else 70)
        ld = 74 if sec == "drop" else 0
        phrase_at(b0(bar), rhodes=rh, lead=ld)
    x = b0(81)                                                       # the break: every SEVEN beats
    while x < b0(97) - 4:
        phrase_at(x, rhodes=56)
        x += 7
    for bar in (145, 149, 153, 157):                                 # the outro: the phrase thinning out
        phrase_at(b0(bar), rhodes=50 if bar < 153 else 0)


def drums():
    hand = random.Random(5)
    for bar in range(1, BARS + 1):
        sec = sec_of(bar)
        if sec == "break" or bar > 172:
            continue
        for b in range(4):
            part("kick").add(b0(bar) + b, 0.5, "kr" if sec != "drop" else "k", 112 if b == 0 else 106)
            if bar >= 5:
                part("hats").add(b0(bar) + b + 0.5, 0.25, "oh", 72 + hand.randint(-6, 6))
        if bar >= 33 and sec != "outro" or (sec == "outro" and bar < 161):
            for b in (1, 3):
                part("clap").add(b0(bar) + b + 0.015, 0.5, "cp", 96 + hand.randint(-4, 4))
        if sec in ("song", "drop"):
            for s in range(16):
                if s % 2 == 0 and hand.random() < 0.35:
                    continue
                part("shaker").add(b0(bar) + s / 4 + (0.03 if s % 2 else 0), 0.2, "h", (58 if s % 4 == 2 else 40) + hand.randint(-6, 6))


def harmony():
    for bar in range(1, BARS + 1, 2):
        sec = sec_of(bar)
        root, v = chord_at(bar)
        if sec in ("song", "drop", "break") and not (sec == "song" and bar < 57):
            part("pad").add(b0(bar), 2 * BAR - 0.1, ",".join(nm(m) for m in v), 60 if sec != "break" else 66)
        # the bass: the sub on B through intro and speech; from the song, the chord roots with the phrase's walk
        if sec in ("intro", "speech"):
            for k in range(2):
                part("sub").add(b0(bar + k), BAR - 0.1, "B1", 92)
        elif sec in ("song", "drop"):
            for k in range(2):
                b = b0(bar + k)
                part("sub").add(b, 1.5, nm(root), 96)
                part("sub").add(b + 1.5, 0.5, nm(root), 80)
                part("sub").add(b + 2.5, 1.4, nm(root + (7 if k else 0)), 88)
        elif sec == "outro":
            for k in range(2):
                part("sub").add(b0(bar + k), BAR - 0.1, "B1" if bar < 161 else "F#1", 90)


def stair():
    """THE THREAD: the tape's stair (B C# D F#) rising on celesta, once every eight bars of the drop."""
    for bar in range(100, 145, 8):
        for k, m in enumerate((71, 73, 74, 78)):
            part("stair").add(b0(bar) + 2 + k * 0.5, 0.45, nm(m), 76 + 4 * k)


LEVEL = {"intro": -5, "speech": -3, "song": -1, "break": -6, "drop": 0, "outro": -4}


def lanes():
    dyn = []
    for name, a, z in SECTIONS:
        if dyn:
            dyn.append([f"{b0(a) - 0.25:.2f}b", dyn[-1][1]])
        dyn.append([f"{b0(a):.2f}b", float(LEVEL[name])])
    return dyn


def main():
    voice_line()
    drums()
    harmony()
    stair()
    tempo = [{"at": "0b", "bpm": 119.5}, {"at": f"{b0(145):.0f}b", "bpm": 120, "ramp": True}]
    pump = {"type": "pump", "on": "kick", "depth": "-7dB", "attack": "3ms", "release": "330ms", "curve": 0.7}
    tr = lambda n, patch, **kw: dict({"name": n, "patch": patch, "score": part(n).score()}, **kw)
    song = {
        "about": "Chirpers - The Endless Stair (Chirpers VII), track 5 by chirper-three: SAY IT AGAIN. Deep soulful house "
                 "in B minor; the speech-to-song illusion: a spoken phrase whose speaking pitches sit on the tape's stair, "
                 "repeated until it sings, then doubled by the Rhodes, harmonised, and sung by a lead. Generated by "
                 "compose/chirpers7/src/chirpers7-t5.py.",
        "tempo": tempo,
        "tail": "1.2s",
        "loudness": -11,                       # the tape's agreed loudness (proposed), through the engine's true-peak limiter
        "buses": {"room": {"fx": ["reverb kind=room decay=1.4s mix=1 predelay=15ms", "hp cutoff=250"]},
                  "hall": {"fx": ["reverb kind=hall decay=3.2s mix=1 predelay=30ms", "hp cutoff=250"]}},
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=30", "peak cutoff=350 q=0.8 gain=-2dB",
                                                    "highshelf cutoff=7000 gain=-2dB"]},
                          {"type": "compressor", "threshold": "-20dB", "ratio": 2.5, "attack": "15ms", "release": "150ms",
                           "makeup": "0dB"},
                          {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                          {"type": "gain", "gain": "+8dB"},
                          {"type": "compressor", "threshold": "-10dB", "ratio": 8, "attack": "1ms", "release": "60ms",
                           "makeup": "0dB"}],    # catch the kick's peaks; the song's loudness masters (true-peak limited)
                   "auto": {"dyn": {"points": lanes()}}},
        "tracks": [
            tr("kick", "machine-kit", gain="-4dB"),
            tr("hats", "machine-kit", gain="-10dB", pan=0.1),
            tr("clap", "machine-kit", gain="-6dB", sends={"room": "-10dB"}),
            tr("shaker", "machine-kit", gain="-14dB", pan=-0.2),
            tr("sub", "808", gain="-8dB", fx=[{"type": "phantom", "harmonics": "-6dB", "odd": 0.4, "remove": 0.0}, pump]),
            tr("voice", "voice-speech", gain="-3dB", sends={"room": "-12dB"},
               fx=[{"type": "filter", "kind": "hp", "cutoff": 120}]),
            tr("rhodes", "epiano-tine synth.tine.sense=0.3 play.release.patch=epiano-damper play.release.decay=2s",
               gain="-6dB", pan=-0.15, sends={"hall": "-10dB"}),
            tr("pad", "juno-pad", gain="-12dB", sends={"hall": "-6dB"}, lfo={"pf": {"wave": "sine", "rate": "28b"}},
               fx=[{"type": "filter", "kind": "lp", "cutoff": {"value": 1800, "mod": [{"src": "lfo.pf", "amount": 0.6}]}}, pump]),
            tr("lead", "boc-lead", gain="-10dB", pan=0.15, sends={"hall": "-8dB"}),
            tr("stair", "celesta", gain="-10dB", pan=0.25, sends={"hall": "-6dB"}),
        ],
    }
    with open(OUT, "w") as f:
        json.dump(song, f, indent=1)
        f.write("\n")
    print(f"wrote {OUT}: {BARS} bars")


if __name__ == "__main__":
    main()
