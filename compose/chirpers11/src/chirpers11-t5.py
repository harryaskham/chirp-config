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

v2 (26 Nov): THE HAT ALSO RISES (C11T5_SHEP=0 takes it out: v1). From the third row of "never arrives" each layer
of the Risset rhythm has a voice of its own, a small struck tone, on the same strokes; the four are an octave
apart (A3, A4, A5, A6) and every one of them climbs an octave through the row (one lane, `rise`, 0 to 12
semitones). So a layer ends the row at the speed AND the pitch at which the next began it, the same windows fade
the top out and the bottom in, and the row repeats note for note: it is a Shepard scale and a Risset rhythm at
once, getting faster and higher for ever and going nowhere. In "out" it runs backwards: slower and lower, for ever.

v3 (26 Nov): THE DRUM GOES ROUND THE CLICK (C11T5_ROUND=0 takes the section out: v2). The click stands on step 2
of every beat's four sixteenths, and the first illusion used two of the four places a drum can stand against it:
nowhere (the click is the beat) and two sixteenths before it (the click is the "and"). A new section, "round the
click", after "the wrong one again", uses the other three, a row each, the drum one sixteenth later every row:
  1. THE DRUM JUST BEFORE THE CLICK (kick on steps 1, 5, 9, 13): DUM-ta. The click is the drum's echo, the "e".
  2. THE DRUM ON THE CLICK (2, 6, 10, 14): the wrong beat, and now the drum says so too. The click is the beat.
  3. THE DRUM JUST AFTER THE CLICK (3, 7, 11, 15): ta-DUM. The click is a pickup, the "a", and the bar gallops.
Then "all three" puts the drum a sixteenth later again, which is the true beat (0, 4, 8, 12), and the click is the
"and". So in four rows the same click has been every sixteenth of the beat, and not one note of it or of the bass
has moved since the first bar: only the drum has, and with it where the listener stands. The drum rests for the
last bar of each row (the step is a silence, not a stumble); a clap on its two and four joins it half-way through.
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

SHEP = os.environ.get("C11T5_SHEP", "1") != "0"      # v2: the layers' own voices, rising
SHEP_ROOT = ("A3", "A4", "A5", "A6")                  # the note each layer starts every row on
RISE = 12                                             # semitones every layer climbs in a row
ROUND = os.environ.get("C11T5_ROUND", "1") != "0"    # v3: the drum goes round the click
ROUND_AT = (1, 2, 3)                                  # the sixteenth of the beat the drum stands on, a row each ("all three" is 0)
ROUND_REST = 1                                        # bars at the end of each of those rows with no drum
ALL = None
# name, rows, {part: None (the whole section) or (from bar, to bar) of the section}
SECTIONS = [
    ("the wrong one",    2, {"tick": ALL, "bass": (8, 16)}),
    ("turned around",    3, {"tick": ALL, "bass": ALL, "kick": ALL, "clap": (8, 24)}),
    ("never arrives",    5, {"tick": ALL, "bass": ALL, "kick": ALL, "clap": ALL, "ris": ALL, "shep": (16, 40)}),
    ("not there",        3, {"tick": ALL, "bass": ALL, "ris": ALL, "kick": (8, 24), "sub": (8, 16), "clap": (16, 24)}),
    ("the wrong one again", 1, {"tick": ALL, "bass": ALL, "ris": ALL, "clapx": ALL}),
] + ([("round the click", len(ROUND_AT), {"tick": ALL, "bass": ALL,
                                          **{f"k{k}": (i * ROW, (i + 1) * ROW - ROUND_REST) for i, k in enumerate(ROUND_AT)},
                                          **{f"c{k}": (i * ROW + ROW // 2, (i + 1) * ROW - ROUND_REST) for i, k in enumerate(ROUND_AT)}})] if ROUND else []) + [
    ("all three",        3, {"tick": ALL, "bass": ALL, "kick": ALL, "clap": ALL, "ris": ALL, "shep": ALL}),
    ("out",              3, {"tick": (0, 20), "bass": (0, 16), "kick": (0, 8), "sir": ALL, "pehs": ALL}),
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


def layer(j, back=False):
    """One row of layer j alone: (beat in the row, velocity). Its own strokes and its own window, nothing summed."""
    n0, out = C * 2 ** j, []
    for n in range(n0, 2 * n0):
        t = CYCLE * math.log2(n / n0)
        v = math.sin(math.pi * (t / CYCLE + j) / LAYERS) ** 2
        if v >= QUIET:
            out.append(((CYCLE - t) % CYCLE if back else t, v))
    return sorted(out)


def shep_notes(j):
    out = []
    for name, back in (("shep", False), ("pehs", True)):
        row = layer(j, back)
        for r in range(BARS // ROW):
            if plays(name, r * ROW):
                out += [note(r * CYCLE + t, SHEP_ROOT[j], 0.2, v) for t, v in row]
    return sorted(out, key=lambda n: n["at"])


def rise_lane():
    """Semitones every layer's voice is above its root: 0 to RISE through each row it plays (RISE to 0 backwards)."""
    pts = [["0b", 0]]
    for r in range(BARS // ROW):
        for name, lo, hi in (("shep", 0, RISE), ("pehs", RISE, 0)):
            if plays(name, r * ROW):
                pts += [[f"{r * CYCLE:g}b", lo], [f"{(r + 1) * CYCLE - 0.01:g}b", hi]]
    pts.append([f"{TOTAL:g}b", 0])
    return pts


OFF = (2, 6, 10, 14)           # where the click and the bass are from the first bar to the last
TICK = lambda bar: [(s, "E5", 1, 0.9 if s in (2, 10) else 0.78) for s in OFF]
LINE = [("A1", "A1", "A1", "C2"), ("A1", "A1", "A1", "A1"), ("A1", "A1", "A1", "D2"), ("A1", "A1", "E2", "G1")]
BASS = lambda bar: [(s, p, 1.5, 0.9 if s in (2, 10) else 0.8) for s, p in zip(OFF, LINE[bar % 4])]
KICK = lambda bar: [(s, "A1", 1, 0.95 if s == 0 else 0.9) for s in (0, 4, 8, 12)]
CLAP = lambda bar: [(4, "C4", 1, 0.8), (12, "C4", 1, 0.86)]      # two and four
CLAPX = lambda bar: [(6, "C4", 1, 0.8), (14, "C4", 1, 0.86)]     # two and four of the wrong beat


def kick_on(k):
    """The bass drum on sixteenth k of every beat (0 is KICK)."""
    return lambda bar: [(s, "A1", 1, 0.95 if s == k else 0.9) for s in (k, k + 4, k + 8, k + 12)]


def clap_on(k):
    """Two and four of the beat that drum makes."""
    return lambda bar: [(k + 4, "C4", 1, 0.8), (k + 12, "C4", 1, 0.86)]


def moved(name, on):
    """The strokes of the rows in which the drum stands somewhere else, in time order with the part's own."""
    return sum((part(f"{name}{k}", on(k)) for k in ROUND_AT), []) if ROUND else []

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
    "ht-shep": {"about": "Hearing Things' rising voice (chirper-zero, 26 Nov, v2): a small struck tone (a sine with two bar-like partials, 70 ms), whose loudness is all velocity and whose pitch rides the lane `rise` (semitones): one layer of the Shepard-Risset hat.",
                "play": {"vel_sens": 1.0},
                "synth": {"layers": ["sine", "sine ratio=2.76 level=-10dB", "sine ratio=5.4 level=-18dB"], "pitch": {"value": 0, "mod": [{"src": "auto.rise", "amount": 1}]},
                          "amp": {"a": "0.3ms", "d": "70ms", "s": 0, "r": "20ms", "curve": 3}}},
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
    doc = {
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
            {"name": "kick", "patch": "ht-kick", "gain": "-8dB", "pan": 0.0, "notes": sorted(part("kick", KICK) + moved("k", kick_on), key=lambda n: n["at"]) if ROUND else part("kick", KICK)},
            {"name": "tick", "patch": "ht-tick", "gain": "-2dB", "pan": 0.0, "sends": {"room": "-14dB"}, "notes": part("tick", TICK)},
            {"name": "bass", "patch": "ht-bass", "gain": "-11dB", "pan": 0.0, "fx": [pump], "notes": part("bass", BASS)},
            {"name": "sub", "patch": "sub-sine", "gain": "-10dB", "pan": 0.0, "fx": [pump], "notes": part("sub", BASS)},
            {"name": "clap", "patch": "ht-clap", "gain": "-5dB", "pan": 0.0, "sends": {"room": "-10dB"}, "notes": sorted(part("clap", CLAP) + part("clapx", CLAPX) + moved("c", clap_on), key=lambda n: n["at"])},
            {"name": "ris", "patch": "ht-hat", "gain": "6dB", "pan": 0.0, "sends": {"room": "-16dB"}, "notes": sorted(ris_notes("ris") + ris_notes("sir", back=True), key=lambda n: n["at"])},
        ],
    }
    if SHEP:
        lane = rise_lane()
        doc["tracks"] += [{"name": f"shep{j}", "patch": "ht-shep", "gain": "-13dB", "pan": 0.15, "sends": {"room": "-14dB"}, "auto": {"rise": {"points": lane}}, "notes": shep_notes(j)} for j in range(LAYERS)]
        doc["about"] = doc["about"].replace(" Generated by", " From v2 each layer of the hat has a small tone of its own that climbs an octave a row, so it is faster and higher for ever. Generated by")
    else:
        del PATCHES["ht-shep"]
    if ROUND:
        doc["about"] = doc["about"].replace(" Generated by", " From v3 the drum goes round the click a sixteenth a row (just before it, on it, just after it, then the true beat), so the same click is heard as every sixteenth of the beat and never moves. Generated by")
    return doc


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
        if ROUND:
            names = {0: 'the "and"', 1: 'the "e" (DUM-ta)', 2: "the beat", 3: 'the "a" (ta-DUM)'}
            print("the click is on sixteenth 2 of every beat; with the drum on sixteenth k it is heard as: " + " ; ".join(f"k = {k}: {names[k]}" for k in ROUND_AT + (0,)))
        print(f"{BARS} bars, {TOTAL} beats, {BARS * sec:.1f} s")
    else:
        open(OUT, "w").write(dump(song()))
