#!/usr/bin/env python3
"""chirpers3-t7 (Tape Weather, track 7). Composed by chirper-two: AMBIENT TAPE LOOPS.

Beatless drift: the room after t6's beat stops. Five tape loops of unequal (prime) lengths, each one short phrase on
a different worn instrument, slide against each other and never line up the same way twice, so the chords that
sound are accidents of the loops: bowed vibes (17 beats), tape piano (23), a juno pad swelling (29), a whistling
sine (31), a low drone (37), all in F lydian. They enter one by one out of the rain that t6 ended in, drift, and
leave one by one; slow wow, hiss and the weather outside throughout. Nominal 60 bpm (a beat is a second).

Emits songs/chirpers3-t7.yaml. Edit the music here.
"""
import json
import os
import random

OUT = os.environ.get("T7_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers3-t7.yaml")
BPM = 60
TOTAL = 204.0
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def midi(n):
    name, octv = n[:-1], int(n[-1])
    return 12 * (octv + 1) + NAMES.index(name)


class Track:
    def __init__(self, name):
        self.name, self.ev = name, []

    def add(self, at, ln, head, vel):
        self.ev.append((round(max(0.0, at), 4), max(0.05, round(ln, 4)), head, int(max(1, min(127, vel)))))

    def score(self, total):
        ev = sorted(self.ev, key=lambda e: (e[0], -e[3]))
        merged = []
        for e in ev:
            if e[0] >= total - 1e-6:
                continue
            if merged and abs(merged[-1][0] - e[0]) < 1e-3:
                continue
            merged.append(e)
        toks, pos = [], 0.0
        for i, (s, ln, head, vel) in enumerate(merged):
            nxt = merged[i + 1][0] if i + 1 < len(merged) else total
            ln = min(ln, nxt - s)
            if s - pos > 1e-4:
                toks.append(f"R/{s - pos:.4g}b")
            toks.append(f"{head}/{ln:.4g}b@{vel}")
            pos = s + ln
        if total - pos > 1e-4:
            toks.append(f"R/{total - pos:.4g}b")
        return " ".join(toks)


# Round 2 (v2): O = THE DOOR OPENS in the middle: across the loops' densest stretch (beats 70-150) the beat through the
# wall comes nearer (its lo-pass opens two octaves and closes again), and a fretless walks in under the pad,
# following its chords (F, then D), then leaves.
R2 = set(filter(None, os.environ.get("T7_R2", "O").split(","))) - {"none"}
DOOR = (70, 150)
# Round 3 (v3): M = A MEMORY through the open door: t6 Late on Purpose's vibes SIGH (the struck, motored vibes of t6,
# E5 C5 A4 falling, late) sounds three times while the door is open, as if heard from next door, over the loops.
R3 = set(filter(None, os.environ.get("T7_R3", "M").split(","))) - {"none"}

# the loops: (track, loop length in beats, enter, leave, [(offset, length, notes)], velocity)
LOOPS = [
    ("vib", 17, 10, 186, [(0, 4, "A4"), (6, 5, "E5"), (12, 3, "D5")], 70),
    ("pno", 23, 22, 176, [(0, 3, "F3,C4"), (5, 2, "G4"), (9, 4, "B4"), (16, 3, "A4")], 66),
    ("pad", 29, 38, 166, [(0, 10, "F3,A3,C4,E4"), (14, 10, "D3,F3,A3,C4,E4")], 58),
    ("whi", 31, 62, 150, [(3, 2, "C6"), (8, 4, "A5"), (20, 3, "E6")], 50),
    ("drone", 37, 0, 204, [(0, 20, "F1"), (20, 15, "C2")], 72),
]


def build():
    rng = random.Random(7)
    T = {k: Track(k) for k in ("vib", "pno", "pad", "whi", "drone", "rain", "crackle", "hiss", "pulse", "bass",
                               "sigh")}
    for tr, L, enter, leave, phrase, vel in LOOPS:
        k = 0
        while True:
            base = enter + k * L
            if base >= leave:
                break
            for o, ln, notes in phrase:
                at = base + o
                if at >= leave:
                    continue
                # the tape's own dynamics: each pass a little louder or softer, fading in and out at the ends
                edge = min(1.0, (at - enter) / 20.0, (leave - at) / 20.0)
                T[tr].add(at + rng.uniform(-0.03, 0.05), ln, notes, int(vel * (0.55 + 0.45 * edge) + rng.randint(-4, 4)))
            k += 1
    # the weather, from t6: rain thinning as the loops gather, thickening as they leave
    for beat in range(int(TOTAL)):
        busy = sum(1 for _, _, e, l, _, _ in LOOPS[:4] if e <= beat < l)
        for _ in range(rng.randint(1, 3) if busy >= 3 else rng.randint(3, 6)):
            T["rain"].add(beat + rng.uniform(0, 0.98), 0.05, "C5", rng.randint(18, 55))
        if rng.random() < 0.2:
            T["crackle"].add(beat + rng.uniform(0, 0.98), 0.06, "C5", rng.randint(25, 60))
    T["hiss"].add(0.0, TOTAL - 0.1, "C4", 60)
    # a heartbeat through the wall: a felt kick every four beats and a brush sweep, only while three loops play
    for beat in range(0, int(TOTAL), 2):
        busy = sum(1 for _, _, e, l, _, _ in LOOPS[:4] if e <= beat < l)
        if busy >= 3:
            T["pulse"].add(beat + 0.02, 0.6, "k", 62 + (6 if beat % 4 == 0 else 0) + rng.randint(-4, 4))
            T["pulse"].add(beat + 1.0 + rng.uniform(0.0, 0.05), 0.9, "bt", 46 + rng.randint(-4, 4))
    if "M" in R3:  # t6's sigh, remembered
        for b0 in (94, 110, 126):
            for k, (o, n) in enumerate(((0.5, "E5"), (1.0, "C5"), (1.75, "A4"))):
                T["sigh"].add(b0 + o, 0.9 if k == 2 else 0.4, n, 66 - 3 * k)
    if "O" in R2:  # the fretless follows the pad's 29-beat loop through the door's window
        k = 0
        while True:
            base = 38 + k * 29
            if base >= DOOR[1]:
                break
            for o, ln, root in ((0, 10, 41), (14, 10, 38)):
                at = base + o
                if DOOR[0] <= at < DOOR[1]:
                    T["bass"].add(at + 0.05, 3.5, nm(root), 64)
                    T["bass"].add(at + 4.05, 2.5, nm(root + 7), 54)
                    T["bass"].add(at + 7.05, 2.5, nm(root + 12), 50)
            k += 1
    return T


def patches():
    bowed = {"about": "Odd Hours t8's bowed vibraphone (chirper-two): bar partials 1 / 4 / 10, a slow swell, no motor.",
             "synth": {"layers": [{"name": "bar", "type": "additive", "partials": [[1, 1], [4.0, 0.1], [10.0, 0.015]]}],
                       "filters": ["hp cutoff=150", "lp cutoff=6k"],
                       "amp": {"a": "350ms", "d": "1.5s", "s": 0.7, "r": "1.2s"}}, "play": {"vel_sens": 0.5}}
    whistle = {"about": "chirper-two's whistle: a sine with a breathy edge and a slow vibrato.",
               "synth": {"pitch": {"value": 0, "mod": [{"src": "lfo.vib", "amount": 12}]},
                         "layers": [{"name": "tone", "wave": "sine"},
                                    {"name": "breath", "type": "noise", "level": "-34dB"}],
                         "lfo": {"vib": {"wave": "sine", "rate": "4.6hz"}},
                         "filters": ["hp cutoff=400", "lp cutoff=5k"],
                         "amp": {"a": "180ms", "d": "400ms", "s": 0.8, "r": "700ms"}}, "play": {"vel_sens": 0.6}}
    drone = {"about": "chirper-two's drone: two detuned sines, very slow.",
             "synth": {"layers": [{"name": "a", "wave": "sine"}, {"name": "b", "wave": "sine", "detune": 7, "level": "-6dB"}],
                       "amp": {"a": "3s", "d": "2s", "s": 0.85, "r": "4s"}}}
    rain = {"about": "chirper-two's rain (t6): a droplet of band-passed noise.",
            "synth": {"layers": [{"name": "drop", "type": "noise"}], "filters": ["hp cutoff=900", "lp cutoff=5500"],
                      "amp": {"a": "0.3ms", "d": "9ms", "s": 0, "r": "6ms", "curve": 2}}, "play": {"vel_sens": 1.0}}
    crackle = {"about": "chirper-two's vinyl crackle (t6).",
               "synth": {"layers": [{"name": "tick", "type": "noise"}], "filters": ["hp cutoff=1800", "lp cutoff=9k"],
                         "amp": {"a": "0.1ms", "d": "3ms", "s": 0, "r": "2ms"}}, "play": {"vel_sens": 1.0}}
    hiss = {"about": "chirper-two's tape hiss (t6).",
            "synth": {"layers": [{"name": "hiss", "type": "noise"}], "filters": ["hp cutoff=3000", "lp cutoff=10k"],
                      "amp": {"a": "3s", "d": "1s", "s": 1.0, "r": "4s"}}}
    brush = dict(type="drum", beater="brush", decay="0.3s", sharp=20, reso=1.4, cavity=0.3, reso_level=0.5, shell=0.3,
                 shell_hz=470, wires=0.45, gap=0.25, wire_tone="5k", strike=0.35, damp=0.35, slap=0.6, stereo=0.35)
    far = {"about": "t6's hand kit heard through the wall: a felt kick and a brush sweep (physical drum layer).",
           "extends": "room-kit",
           "kit": {"k": {"pitch": "D1", "gain": "0dB", "patch": {"synth": {"layers": [dict(type="drum", beater="felt",
                         decay="0.6s", sharp=35, reso=1.0, cavity=0.25, reso_level=0.6, air=0.45, strike=0.2, damp=0.35,
                         slap=0.2, stereo=0.15)], "filters": ["hp cutoff=28", "lp cutoff=900"],
                         "amp": {"a": "1ms", "d": "700ms", "s": 0, "r": "60ms", "curve": 2}}, "play": {"vel_sens": 0.7}}},
                   "bt": {"pitch": "E3", "gain": "-6dB", "patch": {"synth": {"layers": [brush],
                          "filters": ["hp cutoff=300", "lp cutoff=5k"],
                          "amp": {"a": "0.5ms", "d": "500ms", "s": 0, "r": "60ms", "curve": 2}}, "play": {"vel_sens": 0.7}}},
                   "bs": {"pitch": "E3", "gain": "-4dB", "patch": {"synth": {"layers": [dict(brush, sweep="1.2s")],
                          "filters": ["hp cutoff=200", "lp cutoff=4k"],
                          "amp": {"a": "40ms", "d": "1.4s", "s": 0, "r": "120ms", "curve": 1}}, "play": {"vel_sens": 0.7}}}}}
    struck = {"about": "Odd Hours t8's vibraphone (chirper-two), as t6 uses it: partials 1 / 4 / 10, a 5.2 Hz motor.",
              "synth": {"layers": [{"name": "bar", "type": "additive", "partials": [[1, 1], [4.0, 0.16], [10.0, 0.025]],
                                    "level": {"value": "0dB", "mod": [{"src": "lfo.motor", "amount": 3}]}}],
                        "lfo": {"motor": {"wave": "sine", "rate": "5.2hz"}},
                        "filters": ["hp cutoff=150", "lp cutoff=7k"],
                        "amp": {"a": "2ms", "d": "3.2s", "s": 0, "r": "500ms", "curve": 2}}, "play": {"vel_sens": 0.55}}
    return {**({"c2-vibes": struck} if "M" in R3 else {}), "c2-far-kit": far, "c2-bowed-vibes": bowed, "c2-whistle": whistle, "c2-drone": drone, "c2-rain": rain,
            "c2-crackle": crackle, "c2-hiss": hiss}


def main():
    T = build()
    wow = {"type": "chorus", "rate": 0.27, "depth": 0.5, "voices": 1, "mix": 1.0}
    hall = "reverb kind=hall decay=4.5s mix=0.38 predelay=30ms"
    tracks = [
        {"name": "bowed-vibes", "patch": "c2-bowed-vibes", "pan": -0.35, "gain": "0dB", "fx": [wow, hall],
         "score": T["vib"].score(TOTAL)},
        {"name": "tape-piano", "patch": "tape-piano", "pan": 0.3, "gain": "4dB",
         "fx": [dict(wow, rate=0.21), "tape drive=0.35 warmth=0.7", "lp cutoff=4200",
                {"type": "crush", "bits": 12, "rate": 16000, "mix": 0.25}, hall], "score": T["pno"].score(TOTAL)},
        {"name": "juno", "patch": "juno-pad", "pan": 0.0, "gain": "0dB", "fx": ["lp cutoff=3200", hall],
         "score": T["pad"].score(TOTAL)},
        {"name": "whistle", "patch": "c2-whistle", "pan": 0.5, "gain": "-14dB", "fx": [dict(wow, rate=0.33), hall],
         "score": T["whi"].score(TOTAL)},
        {"name": "drone", "patch": "c2-drone", "gain": "-30dB", "fx": ["lp cutoff=300"], "score": T["drone"].score(TOTAL)},
        {"name": "rain", "patch": "c2-rain", "pan": -0.15, "gain": "-30dB",
         "fx": ["reverb kind=room decay=0.6s mix=0.25", "width width=1.6"], "score": T["rain"].score(TOTAL)},
        {"name": "pulse", "patch": "c2-far-kit", "gain": "-6dB",
         "fx": ([{"type": "filter", "kind": "lp", "cutoff": {"value": 1200, "mod": [{"src": "auto.door", "amount": 2.2}]}}]
                if "O" in R2 else []) + ["reverb kind=room decay=1.2s mix=0.35"],
         "score": T["pulse"].score(TOTAL),
         **({"auto": {"door": {"points": [["0b", 0.0], [f"{DOOR[0]}b", 0.0], [f"{(DOOR[0] + DOOR[1]) // 2}b", 1.0],
                                          [f"{DOOR[1]}b", 0.0]]}}} if "O" in R2 else {})},
        *([{"name": "fretless", "patch": "fretless", "pan": -0.05, "gain": "-4dB",
            "fx": ["lp cutoff=700", "tape drive=0.2 warmth=0.5", "reverb kind=room decay=1.0s mix=0.2"],
            "score": T["bass"].score(TOTAL)}] if "O" in R2 else []),
        *([{"name": "sigh", "patch": "c2-vibes", "pan": 0.35, "gain": "-6dB",
            "fx": [dict(wow, rate=0.35), "lp cutoff=2600", "reverb kind=hall decay=3s mix=0.4"],
            "score": T["sigh"].score(TOTAL)}] if "M" in R3 else []),
        {"name": "crackle", "patch": "c2-crackle", "gain": "-30dB", "score": T["crackle"].score(TOTAL)},
        {"name": "hiss", "patch": "c2-hiss", "gain": "-36dB", "score": T["hiss"].score(TOTAL)},
    ]
    about = ("Chirpers - Tape Weather, track 7. Original composition by chirper-two, generated by "
             "compose/chirpers3/src/chirpers3-t7.py. Ambient tape loops: beatless drift. Five loops of unequal prime "
             "lengths (17, 23, 29, 31, 37 beats) on bowed vibes, tape piano, a juno pad, a whistling sine and a drone, "
             "in F lydian, sliding against each other and never lining up the same way twice; the rain from t6 still "
             "falling. Nominal 60 bpm.")
    lines = [
        f"about: {json.dumps(about)}",
        "meta: " + json.dumps({"artist": "Chirpers", "album": "Tape Weather", "title": "After the Beat, Rain", "track": 7,
                               "year": 2026}),
        f"tempo: {BPM}",
        f'length: "{TOTAL:g}b"',
        'tail: "5s"',
        'ceiling: "-0.5dB"',
        'volume: "4dB"',
        "patches: " + json.dumps(patches()),
        "master: " + json.dumps({"fx": [{"type": "eq", "bands": ["hp cutoff=28"]}, "tape drive=0.2 warmth=0.5",
                                        "glue threshold=-22dB ratio=1.5 attack=40ms release=400ms makeup=1dB"]}),
        "tracks:",
    ]
    lines += ["  - " + json.dumps(t) for t in tracks]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write("\n".join(lines) + "\n")
    print(f"wrote {OUT}: {TOTAL / BPM * 60:.1f} s")


if __name__ == "__main__":
    main()
