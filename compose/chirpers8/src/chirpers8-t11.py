#!/usr/bin/env python3
"""chirpers - A Light Left On (chirpers VIII), track 11 (chirper-three): BUTTERFLY HOUSE.

Deep, breathing electronic house whose every dial is steered by a STRANGE ATTRACTOR. The Lorenz system
(sigma 10, rho 28, beta 8/3) is integrated once per sixteenth from one fixed seed; its three coordinates drive the song:
  x  which LOBE the orbit is in -> which harmonic world (C# or F#), and the wavetable lead's POSITION;
  y  which partial the lead plays, and how often the TRANCE GATE opens on the pads;
  z  the vocal CHOPS (sampled, sliced) fire near the top of the attractor.
The orbit flips lobes at moments nobody can predict - the song changes key when the weather does. (The smallest change
in the seed and it is a different song: a butterfly in the machine.)

TUNING: the HARMONIC SERIES. Every pitch is a partial (8..16) of the lobe's fundamental - C#1 or F#1 - written as
fractional MIDI: the 7th, 11th and 13th partials are alien to twelve notes, and pure.

DYNAMICS SHOWCASE: a bass that PUMPS on the kick, pads TRANCE-GATED by a ghost track the attractor writes, OTT on the
drums, a TRANSIENT shaper on the kick, GLUE on the master; a wavetable lead with a PITCH harmonizer a pure fifth above.

FORM (168 bars, ~5:40; 120 bpm, a ritardando to 112 over the last 16 bars to hand the closer its tempo):
  intro 1-16  kick, gated pads   |  A 17-48 the lead   |  B 49-80 + chops, full   |  break 81-96 the attractor alone
  C 97-136 the peak  |  outro 137-168 thinning; the orbit is held in the F# lobe for the last 16 bars, into the closer
"""
import json
import math
import os
import random

OUT = os.environ.get("C8T11_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers8-t11.yaml")
BAR = 4.0
SECTIONS = [("intro", 1, 16), ("A", 17, 48), ("B", 49, 80), ("break", 81, 96), ("C", 97, 136), ("outro", 137, 168)]
BARS = SECTIONS[-1][2]
TOTAL = BARS * BAR
FUND = {+1: 25, -1: 30}                     # C#1 (lobe x > 0), F#1 (lobe x < 0)
PARTIALS = [8, 9, 10, 11, 12, 13, 14, 15, 16]


def b0(bar):
    return (bar - 1) * BAR


def sec_of(bar):
    for name, a, z in SECTIONS:
        if a <= bar <= z:
            return name
    return "outro"


def partial(n, lobe, octave=0):
    """The n-th partial of the lobe's fundamental, as fractional MIDI."""
    return FUND[lobe] + 12 * math.log2(n) + 12 * octave


def mm(p):
    return f"m{p:.3f}"


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


# ---------------------------------------------------------------- the attractor
def lorenz(n, seed=(1.0, 1.0, 1.05), dt=0.0045, sub=4):
    x, y, z = seed
    out = []
    for _ in range(n):
        for _ in range(sub):                         # RK2 (midpoint), small steps
            dx, dy, dz = 10 * (y - x), x * (28 - z) - y, x * y - (8 / 3) * z
            xm, ym, zm = x + dx * dt / 2, y + dy * dt / 2, z + dz * dt / 2
            dx, dy, dz = 10 * (ym - xm), xm * (28 - zm) - ym, xm * ym - (8 / 3) * zm
            x, y, z = x + dx * dt, y + dy * dt, z + dz * dt
        out.append((x, y, z))
    return out


ORBIT = lorenz(BARS * 16)


def state(bar, s16=0):
    return ORBIT[(bar - 1) * 16 + s16]


def lobe_at(bar, s16=0):
    if bar >= BARS - 15:
        return -1                                   # the outro is held in the F# lobe: into the closer
    return 1 if state(bar, s16)[0] > 0 else -1


# ---------------------------------------------------------------- writing
def write_music():
    hand = random.Random(11)
    for bar in range(1, BARS + 1):
        sec = sec_of(bar)
        lb = lobe_at(bar)
        # PADS: a harmonic-seventh chord of the lobe (partials 8 10 12 14), held; gated by the ghost track below
        if sec != "break" or bar >= 89:
            part("pad").add(b0(bar), BAR - 0.05, ",".join(mm(partial(n, lb, -1)) for n in (8, 10, 12, 14)),
                            62 if sec in ("intro", "outro") else 72)
        # THE TRANCE GATE: a muted ghost track, a sixteenth wherever the attractor's |y| is high enough
        for s in range(16):
            x, y, z = state(bar, s)
            if abs(y) > 6 + (6 if sec in ("intro", "outro") else 0) or s % 4 == 0:
                part("gtrig").add(b0(bar) + s / 4, 0.2, "rs", 110)
        # BASS: partial 2 (an octave above the fundamental), pumping eighths; the 3rd partial on the off-beat 'and'
        if sec not in ("intro", "break") and not (sec == "outro" and bar > 160):
            for e in range(8):
                n = 2 if e % 4 != 3 else 3
                part("bass").add(b0(bar) + e * 0.5, 0.45, mm(partial(n, lb, 0)), 100 if e % 2 == 0 else 84)
        # THE LEAD: a wavetable, a partial chosen by y each eighth, when the orbit moves fast enough
        if sec in ("A", "B", "break", "C") or (sec == "outro" and bar < 153):
            for e in range(8):
                x, y, z = state(bar, e * 2)
                x2, y2, z2 = state(bar, min(15, e * 2 + 1))
                if abs(y2 - y) > (1.2 if sec != "break" else 0.6):
                    k = int(round((y + 25) / 50 * (len(PARTIALS) - 1)))
                    n = PARTIALS[max(0, min(len(PARTIALS) - 1, k))]
                    part("lead").add(b0(bar) + e * 0.5, 0.42, mm(partial(n, lb, 0)), 76 + int(min(30, abs(y2 - y) * 4)))
        # CHOPS: the sampled voice, sliced, fires near the top of the attractor (z high)
        if sec in ("B", "C"):
            for s in range(0, 16, 2):
                x, y, z = state(bar, s)
                if z > 36:
                    part("chops").add(b0(bar) + s / 4, 0.25, f"m{60 + int(abs(x)) % 16}", 90)
        # DRUMS
        if sec != "break":
            for b in range(4):
                if not (sec == "outro" and bar > 164):
                    part("kick").add(b0(bar) + b, 0.5, "k", 114 if b == 0 else 106)
                if sec != "intro" or bar > 8:
                    part("hats").add(b0(bar) + b + 0.5, 0.25, "oh", 66 + hand.randint(-6, 6))
                    for s in (1, 3):
                        if hand.random() < 0.7:
                            part("hats").add(b0(bar) + b + s / 4, 0.1, "h", 48 + hand.randint(-8, 8))
            if sec in ("A", "B", "C"):
                for b in (1, 3):
                    part("clap").add(b0(bar) + b + 0.02, 0.5, "cp", 90 + hand.randint(-4, 4))


def wt_lane():
    """The wavetable position from x, once a bar: 0 (lobe F#, x -20) to 1 (lobe C#, x +20)."""
    return [[f"{b0(bar):.2f}b", round(max(0.0, min(1.0, (state(bar)[0] + 20) / 40)), 3)] for bar in range(1, BARS + 1)]


def tempo_map():
    return [{"at": "0b", "bpm": 120}, {"at": f"{b0(BARS - 15):.0f}b", "bpm": 120},
            {"at": f"{b0(BARS + 1):.0f}b", "bpm": 112, "ramp": True}]


def lanes():
    level = {"intro": -6, "A": -3, "B": -1, "break": -5, "C": 0, "outro": -6}
    pts = []
    for name, a, z in SECTIONS:
        if pts:
            pts.append([f"{b0(a) - 0.25:.2f}b", pts[-1][1]])
        pts.append([f"{b0(a):.2f}b", float(level[name])])
    return pts


def main():
    write_music()
    tr = lambda n, patch, **kw: dict({"name": n, "patch": patch, "score": part(n).score()}, **kw)
    lead_patch = {"extends": "juno-pad", "synth": {"layers": [
        {"type": "wavetable", "table": "resonant", "position": {"value": 0, "mod": [{"src": "auto.wt", "amount": 1}]}}],
        "amp": {"a": "4ms", "d": "180ms", "s": 0.55, "r": "120ms"}}}
    flips = sum(1 for i in range(1, len(ORBIT)) if (ORBIT[i][0] > 0) != (ORBIT[i - 1][0] > 0))
    song = {
        "about": "chirpers - A Light Left On (chirpers VIII), track 11 by chirper-three: butterfly house. The Lorenz "
                 "attractor steers every dial - the key (its two lobes), a wavetable lead, a trance gate, sampled chops - "
                 "in the harmonic series over C# and F#; a dynamics showcase (pump, gate, ott, transient, glue). "
                 "Generated by compose/chirpers8/src/chirpers8-t11.py.",
        "tempo": tempo_map(),
        "tail": "0.5s",
        "loudness": -11,
        "volume": "0dB",
        "tracks": [
            tr("lead", lead_patch, gain="-10dB", pan=0.15, sends={"hall": "-10dB", "dly": "-12dB"},
               auto={"wt": {"points": wt_lane()}},
               fx=[{"type": "pitch", "semitones": 7.02, "mix": 0.3}, {"type": "filter", "kind": "lp", "cutoff": 6000}]),
            tr("pad", "juno-pad", gain="-11dB", pan=-0.15, sends={"hall": "-8dB"},
               fx=["gate key=gtrig threshold=-40dB attack=1ms release=40ms", "ott depth=0.3"]),
            tr("gtrig", "machine-kit", gain="-80dB"),
            tr("bass", "808", gain="-8dB", fx=[{"type": "pump", "on": "kick", "depth": "-9dB", "release": "1/6",
                                                "curve": 0.6}]),
            tr("chops", "chopper", gain="-12dB", pan=-0.3, sends={"dly": "-8dB"}),
            tr("kick", "machine-kit", gain="-11dB", fx=["transient attack=6 sustain=-4"]),
            tr("hats", "machine-kit play.humanize.drunk=4ms", gain="-3dB", pan=0.2, fx=["ott depth=0.35"]),
            tr("clap", "machine-kit play.humanize.nudge.cp=8ms", gain="-5dB", sends={"room": "-8dB"}),
        ],
        "buses": {"room": {"fx": ["reverb kind=room decay=1.0s mix=1 predelay=10ms", "hp cutoff=250"]},
                  "hall": {"fx": ["reverb kind=hall decay=2.8s mix=1 predelay=25ms", "hp cutoff=250"]},
                  "dly": {"fx": ["delay time=3/16 mix=1 feedback=0.4", "hp cutoff=400", "lp cutoff=4000"]}},
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=28", "highshelf cutoff=6000 gain=3dB"]},
                          {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                          "glue makeup=2dB",
                          {"type": "compressor", "threshold": "-12dB", "ratio": 8, "attack": "0.3ms",
                           "release": "60ms", "makeup": "0dB"}],
                   "auto": {"dyn": {"points": lanes()}}},
    }
    with open(OUT, "w") as f:
        json.dump(song, f, indent=1)
    print("wrote", OUT, "bars", BARS, "lobe flips", flips,
          "lobes by section", {n: sum(lobe_at(b) for b in range(a, z + 1)) for n, a, z in SECTIONS})


if __name__ == "__main__":
    main()
