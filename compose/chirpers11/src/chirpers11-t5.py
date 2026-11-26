#!/usr/bin/env python3
"""Escapement (Chirpers 11), track 5 (chirper-zero): HEARING THINGS. The slot's word is ILLUSIONS.

Three things that are not on the record, and one rule: THE EAR IS THE INSTRUMENT, so nothing here is hidden by a
trick of the mix. Each is plain arithmetic and all three work on one speaker.

1. THE BEAT THAT TURNS AROUND. The song opens with a click and a bass and no bass drum. They are on the OFF-beats
   (steps 2, 6, 10, 14), but with nothing to say so the ear takes them for the beat. When the bass drum comes in on
   the real beat, not one note of the click or the bass moves: the listener does. It is done twice.

2. THE BASS THAT IS NOT THERE. The bass plays only the second to sixth harmonics of each note (110, 165, 220, 275,
   330 Hz for the A at 55): it has no partial at the pitch you hear. In "not there" the bass drum stops too and the
   record has next to nothing under 95 Hz (22 dB under the rest); then the real fundamental is put under it for
   eight bars and taken away.

3. THE ACCELERANDO THAT NEVER ARRIVES (a Risset rhythm). A hat in LAYERS layers, each twice as fast as the one below.
   Over one row (CYCLE beats) every layer doubles its speed: its strokes fall where C * 2^(t / CYCLE) passes a whole
   number, so layer j ends the row exactly where layer j + 1 began it. Each layer's loudness follows its speed (a
   sine-squared window over the LAYERS octaves), so the fastest fades out as it becomes a blur and a new slowest
   fades in underneath: the row repeats note for note, and it has been speeding up all the way through. C is 23,
   which makes the layers start each row at 0.498, 0.996, 1.99 and 3.98 strokes a beat: on the grid, near enough.
   Then they pull ahead of it, and at the row's end they are on it again, one octave on. In "out" it runs backwards.

THE FORM IS ARITHMETIC: a row is ROW bars; SECTIONS lists each section's rows and its parts (a part may be given the
bars of the section it plays: (from, to)). Every note comes from those.

v1 is the SKELETON (26 Nov): the three illusions, each stated once and then together, with few sounds.
"""
import json
import math
import os

OUT = os.environ.get("C11T5_OUT", os.path.join(os.path.dirname(__file__), "..", "..", "..", "songs", "chirpers11-t5.yaml"))
BPM = 125
BEATS = 4
ROW = 8
STEP = 0.25

CYCLE = ROW * BEATS            # beats in which every layer of the hat doubles its speed
LAYERS = 4
C = 23                         # the slowest layer's count at the start of a row: its speed there is C * ln 2 / CYCLE strokes a beat
QUIET = 0.04                   # strokes softer than this are left out

ALL = None
# name, rows, {part: None (the whole section) or (from bar, to bar) of the section}
SECTIONS = [
    ("the wrong one",    2, {"tick": ALL, "bass": (8, 16)}),
    ("turned around",    3, {"tick": ALL, "bass": ALL, "kick": ALL, "clap": (8, 24)}),
    ("never arrives",    5, {"tick": ALL, "bass": ALL, "kick": ALL, "clap": ALL, "ris": ALL}),
    ("not there",        3, {"tick": ALL, "bass": ALL, "ris": ALL, "kick": (8, 24), "sub": (8, 16), "clap": (16, 24)}),
    ("the wrong one again", 1, {"tick": ALL, "bass": ALL, "ris": ALL, "clapx": ALL}),
    ("all three",        3, {"tick": ALL, "bass": ALL, "kick": ALL, "clap": ALL, "ris": ALL}),
    ("out",              3, {"tick": (0, 20), "bass": (0, 16), "kick": (0, 8), "sir": ALL}),
]


def starts():
    out, b = [], 0
    for name, rows, parts in SECTIONS:
        out.append((name, b, rows * ROW, parts)); b += rows * ROW
    return out, b


SECS, BARS = starts()
TOTAL = BARS * BEATS


def plays(part, bar):
    for name, b0, n, parts in SECS:
        if b0 <= bar < b0 + n:
            if part not in parts:
                return False
            w = parts[part]
            return w is None or w[0] <= bar - b0 < w[1]
    return False


def note(at, pitch, length, vel):
    return {"at": round(at, 4), "len": round(length, 4), "pitch": pitch, "vel": round(vel, 3)}


def part(name, steps):
    out = []
    for bar in range(BARS):
        if plays(name, bar):
            out += [note(bar * BEATS + s * STEP, p, n * STEP, v) for s, p, n, v in steps(bar)]
    return out


def risset(back=False):
    """One row of the hat: (beat in the row, velocity). Stroke n of the finest layer falls at CYCLE * log2(n / n0);
    it belongs to every layer whose count it divides into, and its loudness is the sum of their windows."""
    n0 = C * 2 ** (LAYERS - 1)
    out = []
    for n in range(n0, 2 * n0):
        t = CYCLE * math.log2(n / n0)
        amp = sum(math.sin(math.pi * (t / CYCLE + j) / LAYERS) ** 2 for j in range(LAYERS) if n % 2 ** (LAYERS - 1 - j) == 0)
        v = amp / (LAYERS / 2)
        if v >= QUIET:
            out.append(((CYCLE - t) % CYCLE if back else t, v))
    return sorted(out)


def ris_notes(name, back=False):
    row, out = risset(back), []
    for r in range(BARS // ROW):
        if plays(name, r * ROW):
            out += [note(r * CYCLE + t, "A5", 0.1, v) for t, v in row]
    return out


OFF = (2, 6, 10, 14)           # where the click and the bass are from the first bar to the last
TICK = lambda bar: [(s, "E5", 1, 0.9 if s in (2, 10) else 0.78) for s in OFF]
LINE = [("A1", "A1", "A1", "C2"), ("A1", "A1", "A1", "A1"), ("A1", "A1", "A1", "D2"), ("A1", "A1", "E2", "G1")]
BASS = lambda bar: [(s, p, 1.5, 0.9 if s in (2, 10) else 0.8) for s, p in zip(OFF, LINE[bar % 4])]
KICK = lambda bar: [(s, "A1", 1, 0.95 if s == 0 else 0.9) for s in (0, 4, 8, 12)]
CLAP = lambda bar: [(4, "C4", 1, 0.8), (12, "C4", 1, 0.86)]      # two and four
CLAPX = lambda bar: [(6, "C4", 1, 0.8), (14, "C4", 1, 0.86)]     # two and four of the wrong beat

PATCHES = {
    "ht-kick": {"about": "Hearing Things' bass drum (chirper-zero, 26 Nov): the engine's machine kick, short and dry, on A1: the only thing on the record under 100 Hz but for eight bars.",
                "play": {"vel_sens": 0.3},
                "synth": {"layers": [{"type": "machine", "machine": {"part": "kick", "decay": "260ms", "click": 0.6, "drive": 0.35, "punch": 22, "punch_time": "32ms"}}],
                          "filters": ["hp cutoff=28"], "amp": {"a": "0.1ms", "d": "0s", "s": 1, "r": "1s"}}},
    "ht-tick": {"about": "Hearing Things' click (chirper-zero, 26 Nov): the machine's rim, 35 ms, on E5; on the off-beats from the first bar to the last.",
                "play": {"vel_sens": 0.5},
                "synth": {"layers": [{"type": "machine", "machine": {"part": "rim", "decay": "35ms"}}], "filters": ["hp cutoff=400"], "amp": {"a": "0.1ms", "d": "0s", "s": 1, "r": "200ms"}}},
    "ht-hat": {"about": "Hearing Things' hat (chirper-zero, 26 Nov): the machine's hat, 28 ms, above 5 kHz, whose loudness is all velocity: the Risset rhythm's layers are told apart by nothing else.",
               "play": {"vel_sens": 1.0},
               "synth": {"layers": [{"type": "machine", "machine": {"part": "hat", "decay": "28ms"}}], "filters": ["hp cutoff=5000"], "amp": {"a": "0.1ms", "d": "0s", "s": 1, "r": "120ms"}}},
    "ht-clap": {"about": "Hearing Things' clap (chirper-zero, 26 Nov): the machine's clap, three bursts, short, dry.",
                "play": {"vel_sens": 0.4},
                "synth": {"layers": [{"type": "machine", "machine": {"part": "clap", "bursts": 3, "decay": "140ms"}}], "amp": {"a": "0.1ms", "d": "0s", "s": 1, "r": "400ms"}}},
    "ht-bass": {"about": "Hearing Things' bass (chirper-zero, 26 Nov): the second to sixth harmonics of the note and nothing at the note itself (after the library's phantom-bass): the ear supplies the pitch.",
                "play": {"mono": True, "gate": 0.85, "vel_sens": 0.5},
                "synth": {"layers": [{"type": "additive", "partials": [[2, 1.0], [3, 0.85], [4, 0.6], [5, 0.42], [6, 0.3]]}],
                          "env": {"f": {"a": "1ms", "d": "160ms", "s": 0}},
                          "filters": [{"kind": "lp", "cutoff": {"value": 1800, "mod": [{"src": "env.f", "amount": 1.2}]}, "q": 0.8}],
                          "amp": {"a": "2ms", "d": "320ms", "s": 0.55, "r": "60ms", "curve": 3}}},
}


def song():
    pump = {"type": "pump", "on": "kick", "depth": "-4dB", "attack": "2ms", "release": "160ms", "curve": 0.7}
    return {
        "about": "Chirpers - Escapement, track 5 by chirper-zero: HEARING THINGS. Three things that are not on the record: a beat that turns around (the click and the bass are on the off-beats from the first bar; the bass drum says so later), a bass with nothing at its own pitch (harmonics two to six), and a hat that speeds up through every row and starts the next where it started the last (a Risset rhythm in four layers). Generated by compose/chirpers11/src/chirpers11-t5.py.",
        "tempo": BPM,
        "ceiling": "-1dB",
        "loudness": -11.0,
        "seed": 1,
        "tail": "2s",
        "length": f"{TOTAL}b",
        "event_stable": True,
        "patches": PATCHES,
        "buses": {"room": {"fx": ["reverb kind=room decay=0.5s mix=1", "hp cutoff=400"]}},
        "master": {"fx": [{"type": "eq", "bands": ["hp cutoff=30"]}, {"type": "compressor", "threshold": "-18dB", "ratio": 2, "attack": "20ms", "release": "160ms", "makeup": "0dB"}]},
        "tracks": [
            {"name": "kick", "patch": "ht-kick", "gain": "-8dB", "pan": 0.0, "notes": part("kick", KICK)},
            {"name": "tick", "patch": "ht-tick", "gain": "-2dB", "pan": 0.0, "sends": {"room": "-14dB"}, "notes": part("tick", TICK)},
            {"name": "bass", "patch": "ht-bass", "gain": "-11dB", "pan": 0.0, "fx": [pump], "notes": part("bass", BASS)},
            {"name": "sub", "patch": "sub-sine", "gain": "-10dB", "pan": 0.0, "fx": [pump], "notes": part("sub", BASS)},
            {"name": "clap", "patch": "ht-clap", "gain": "-5dB", "pan": 0.0, "sends": {"room": "-10dB"}, "notes": sorted(part("clap", CLAP) + part("clapx", CLAPX), key=lambda n: n["at"])},
            {"name": "ris", "patch": "ht-hat", "gain": "6dB", "pan": 0.0, "sends": {"room": "-16dB"}, "notes": sorted(ris_notes("ris") + ris_notes("sir", back=True), key=lambda n: n["at"])},
        ],
    }


def dump(doc):
    lines = []
    for k, v in doc.items():
        if k == "tracks":
            lines.append("tracks:")
            lines += ["  - " + json.dumps(t) for t in v]
        else:
            lines.append(f"{k}: {json.dumps(v)}")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    if os.environ.get("C11T5_SHOW"):
        sec = 60 / BPM * BEATS
        for name, b0, n, parts in SECS:
            print(f"{name:20s} bars {b0:3d}-{b0 + n:3d}  {int(b0 * sec) // 60}:{b0 * sec % 60:04.1f}-{int((b0 + n) * sec) // 60}:{(b0 + n) * sec % 60:04.1f}  " + ", ".join(p if w is None else f"{p} {w[0]}-{w[1]}" for p, w in parts.items()))
        row = risset()
        print(f"the hat: {len(row)} strokes a row; layer speeds at the row's start " + ", ".join(f"{C * 2 ** j * math.log(2) / CYCLE:.3f}" for j in range(LAYERS)) + " strokes a beat, doubled at its end")
        for q in range(4):
            seg = [(t, v) for t, v in row if q * 8 <= t < (q + 1) * 8]
            mean = sum(v * v for t, v in seg) and math.exp(sum(v * v * math.log(C * 2 ** (LAYERS - 1) * math.log(2) / CYCLE * 2 ** (t / CYCLE)) for t, v in seg) / sum(v * v for t, v in seg))
            print(f"   bars {q * 2}-{q * 2 + 2} of the row: {len(seg):3d} strokes, the loud ones (vel > 0.7) at beats " + " ".join(f"{t:.2f}" for t, v in seg if v > 0.7)[:90])
        print(f"{BARS} bars, {TOTAL} beats, {BARS * sec:.1f} s")
    else:
        open(OUT, "w").write(dump(song()))
