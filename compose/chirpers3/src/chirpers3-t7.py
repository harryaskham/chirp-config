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
# Round 4 (v4): B = THE TAPE RUNS BACKWARDS: a shadow song (`songs: loopsrc`, never a track) renders 24 beats of t7's
# own bowed-vibes and tape-piano loops, and after the door closes a sampler plays it REVERSED, an octave down at
# half speed (beat 152 to the end: the loops swelling in backwards as the real ones leave). Two passes cut the
# piece into too many sections (16); one long pass keeps the drift whole.
R4 = set(filter(None, os.environ.get("T7_R4", "B").split(","))) - {"none"}
# Round 5 (v5): C = THE BACKWARDS TAPE, CHOPPED (wM's chop fx, pin a9e910d1): the reversed loops are cut every two
# bars into eight one-beat slices and replayed rearranged, `0 r1 2 . r4 5 _ r7` (a slice flipped forwards again here
# and there, the live tape let through once, one beat of silence): the backwards swell stutters and catches.
R5 = set(filter(None, os.environ.get("T7_R5", "C").split(","))) - {"none"}
# Round 6 (v6), on per-voice fx (pin 3eee6a72+): P = THE LOOPS WANDER IN SPACE: the bowed vibes and the whistle
# carry a per-voice pan read from each note's random value, so every pass of a loop lands somewhere new in the room;
# S = a calmer architecture: the tape piano and the pad enter together (beat 26) and leave together (beat 170),
# one door opening and one closing instead of four (the piece read as 15 sections).
R6 = set(filter(None, os.environ.get("T7_R6", "P,S").split(","))) - {"none"}
# Round 7 (v7), feedback routing (engine PR #35): D = A DUB ROOM: a bus with a lo-pass, a worn tape and a limiter
# whose output comes back into itself every 1.5 s (`returns`, -5 dB), so what is sent there circles and darkens:
# the whistle, t6's remembered sigh and the beat through the wall; C = the backwards tape's chop loses its beat of
# silence (`0 r1 2 . r4 5 6 r7`), so the tail drifts on instead of stopping. (Moving the whistle's entry to the door
# and the vibes' exit to the piano's only shifted the section boundaries and cost recurrence: tried, reverted.)
R7 = set(filter(None, os.environ.get("T7_R7", "D,C").split(","))) - {"none"}
# Round 8 (v8): L = THE PAD NEVER BREATHES OUT: the juno's two chords overlap and dissolve into each other (Fmaj7 for
# 14 beats, then Dm9 for the loop's other 15, its release crossing into the next), so the pad is one continuous swell instead of two
# entries with silences between (each re-entry read as a new section: seed 0 split at 41 and 51.5 s).
R8 = set(filter(None, os.environ.get("T7_R8", "L").split(","))) - {"none"}
# Round 9 (v9): Q = THE RAIN SINGS: while the door is open (beats 70-150) a second, denser rain falls through a comb
# filter tuned to F3 (the piece's root, q 12; engine PR #32), so the drops ring at F and its harmonics against the
# window; the plain rain goes on under it.
R9 = set(filter(None, os.environ.get("T7_R9", "Q").split(","))) - {"none"}
# Round 12 (v10), wM's shimmer and freeze on a bus of their own: K = THE RAIN'S RING GOES UP: the singing rain also
# feeds a "sky" bus, a long hall with an octave-up shimmer, so its ringing F climbs in octaves above the room; when
# the door begins to shut (beat 138, while the rain still rings) the sky freezes and holds that climbing chord until
# 158, then lets it go. (On the quiet
# whistle's own hall the same shimmer and freeze were inaudible: round 11, discarded.)
R12 = set(filter(None, os.environ.get("T7_R12", "K").split(","))) - {"none"}

# the loops: (track, loop length in beats, enter, leave, [(offset, length, notes)], velocity)
LOOPS = [
    ("vib", 17, 10, 186, [(0, 4, "A4"), (6, 5, "E5"), (12, 3, "D5")], 70),
    ("pno", 23, 22, 176, [(0, 3, "F3,C4"), (5, 2, "G4"), (9, 4, "B4"), (16, 3, "A4")], 66),
    ("pad", 29, 38, 166, [(0, 10, "F3,A3,C4,E4"), (14, 10, "D3,F3,A3,C4,E4")], 58),
    ("whi", 31, 62, 150, [(3, 2, "C6"), (8, 4, "A5"), (20, 3, "E6")], 50),
    ("drone", 37, 0, 204, [(0, 20, "F1"), (20, 15, "C2")], 72),
]
if "L" in R8:
    LOOPS[2] = ("pad", 29, LOOPS[2][2], LOOPS[2][3], [(0, 14, "F3,A3,C4,E4"), (14, 15, "D3,F3,A3,C4,E4")], LOOPS[2][5])
if "S" in R6:
    LOOPS[1] = ("pno", 23, 26, 170, LOOPS[1][4], LOOPS[1][5])
    LOOPS[2] = ("pad", 29, 26, 170, LOOPS[2][4], LOOPS[2][5])


def build():
    rng = random.Random(7)
    T = {k: Track(k) for k in ("vib", "pno", "pad", "whi", "drone", "rain", "crackle", "hiss", "pulse", "bass",
                               "sigh", "rev", "srain")}
    if "B" in R4:
        T["rev"].add(152.0, 52.0, "C3", 92)  # one long reversed pass, an octave down at half speed
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
    if "Q" in R9:  # the singing rain: its own dice, so the plain rain is untouched
        qrng = random.Random(99)
        for beat in range(DOOR[0], DOOR[1]):
            edge = min(1.0, (beat - DOOR[0]) / 16.0, (DOOR[1] - beat) / 16.0)
            for _ in range(qrng.randint(2, 5)):
                T["srain"].add(beat + qrng.uniform(0, 0.98), 0.05, "C5", int(qrng.randint(40, 90) * (0.3 + 0.7 * edge)))
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


def loopsrc_song():
    """A shadow source: 24 beats of the bowed-vibes and tape-piano loops (their own phrases), worn, never played."""
    def score(tr):
        _, L, _, _, phrase, vel = next(x for x in LOOPS if x[0] == tr)
        ev, toks, pos = [], [], 0.0
        for k in range(3):
            for o, ln, notes in phrase:
                if k * L + o < 24:
                    ev.append((k * L + o, min(ln, 24 - (k * L + o)), notes))
        for s, ln, notes in sorted(ev):
            if s > pos:
                toks.append(f"R/{s - pos:g}b")
            toks.append(f"{notes}/{ln:g}b@70")
            pos = s + ln
        return " ".join(toks)
    wow = {"type": "chorus", "rate": 0.27, "depth": 0.5, "voices": 1, "mix": 1.0}
    return {"tempo": BPM, "length": "24b", "tail": "1s", "patches": {"c2-bowed-vibes": patches()["c2-bowed-vibes"]},
            "tracks": [{"name": "vib", "patch": "c2-bowed-vibes", "fx": [wow, "reverb kind=hall decay=3s mix=0.3"],
                        "score": score("vib")},
                       {"name": "pno", "patch": "tape-piano", "gain": "-2dB",
                        "fx": [wow, "tape drive=0.35 warmth=0.7", "reverb kind=hall decay=3s mix=0.3"],
                        "score": score("pno")}]}


def patches():
    bowed = {"about": "Odd Hours t8's bowed vibraphone (chirper-two): bar partials 1 / 4 / 10, a slow swell, no motor.",
             "synth": {**({"fx": [{"type": "pan", "pan": {"value": 0, "mod": [{"src": "rand", "amount": 0.75}]}}]} if "P" in R6 else {}), "layers": [{"name": "bar", "type": "additive", "partials": [[1, 1], [4.0, 0.1], [10.0, 0.015]]}],
                       "filters": ["hp cutoff=150", "lp cutoff=6k"],
                       "amp": {"a": "350ms", "d": "1.5s", "s": 0.7, "r": "1.2s"}}, "play": {"vel_sens": 0.5}}
    whistle = {"about": "chirper-two's whistle: a sine with a breathy edge and a slow vibrato.",
               "synth": {**({"fx": [{"type": "pan", "pan": {"value": 0, "mod": [{"src": "rand", "amount": 0.75}]}}]} if "P" in R6 else {}), "pitch": {"value": 0, "mod": [{"src": "lfo.vib", "amount": 12}]},
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
        *([{"name": "loops-reversed", "patch": "c2-loops-rev", "pan": 0.15, "gain": "-3dB",
            "fx": ([{"type": "chop", "slices": 8, "length": "2/1", "pattern": "0 r1 2 . r4 5 6 r7" if "C" in R7 else "0 r1 2 . r4 5 _ r7"}] if "C" in R5 else [])
                  + ["lp cutoff=3800", {"type": "crush", "bits": 12, "rate": 14000, "mix": 0.25},
                     "reverb kind=hall decay=4s mix=0.35"], "score": T["rev"].score(TOTAL)}] if "B" in R4 else []),
        *([{"name": "singing-rain", "patch": "c2-rain", "pan": 0.1, "gain": "38dB",
            "fx": ["comb cutoff=174.61 q=12", "lp cutoff=3500", "width width=1.5",
                   "reverb kind=hall decay=3s mix=0.35"], "score": T["srain"].score(TOTAL)}] if "Q" in R9 else []),
        {"name": "crackle", "patch": "c2-crackle", "gain": "-30dB", "score": T["crackle"].score(TOTAL)},
        {"name": "hiss", "patch": "c2-hiss", "gain": "-36dB", "score": T["hiss"].score(TOTAL)},
    ]
    about = ("Chirpers - Tape Weather, track 7. Original composition by chirper-two, generated by "
             "compose/chirpers3/src/chirpers3-t7.py. Ambient tape loops: beatless drift. Five loops of unequal prime "
             "lengths (17, 23, 29, 31, 37 beats) on bowed vibes, tape piano, a juno pad, a whistling sine and a drone, "
             "in F lydian, sliding against each other and never lining up the same way twice; the rain from t6 still "
             "falling. Nominal 60 bpm.")
    if "D" in R7:
        for tr in tracks:
            if tr["name"] in ("whistle", "sigh", "pulse"):
                tr["sends"] = {"dubroom": {"whistle": "-4dB", "sigh": "-2dB", "pulse": "-6dB"}[tr["name"]]}
    if "K" in R12 and "Q" in R9:
        for tr in tracks:
            if tr["name"] == "singing-rain":
                tr["sends"] = {"sky": "0dB"}
    lines = [
        f"about: {json.dumps(about)}",
        "meta: " + json.dumps({"artist": "Chirpers", "album": "Tape Weather", "title": "After the Beat, Rain", "track": 7,
                               "year": 2026}),
        f"tempo: {BPM}",
        f'length: "{TOTAL:g}b"',
        'tail: "5s"',
        'ceiling: "-0.5dB"',
        'volume: "4dB"',
        "patches: " + json.dumps({**patches(), **({"c2-loops-rev": {
            "about": "chirper-two: t7's own loops, resampled from the shadow song `loopsrc` and played backwards.",
            "synth": {"layers": [{"type": "sample", "song": "loopsrc", "root": "C4", "reverse": True}],
                      "amp": {"a": "1.5s", "d": "0s", "s": 1, "r": "3s"}}}} if "B" in R4 else {})}),
        *(["songs: " + json.dumps({"loopsrc": loopsrc_song()})] if "B" in R4 else []),
        *(["buses: " + json.dumps({
            **({"dubroom": {
                "gain": "-4dB",
                "fx": ["lp cutoff=1800", {"type": "tape", "drive": 0.4, "warmth": 0.7, "wow": 6, "flutter": 1.5, "seed": 7},
                       "hp cutoff=120", "limiter ceiling=-6dB"],
                "returns": [{"from": "dubroom", "gain": "-5dB", "time": "3/8"}]}} if "D" in R7 else {}),
            **({"sky": {
                "gain": "0dB",
                "auto": {"frz": {"points": [["0b", 0.0], ["138b", 0.0], ["138.3b", 1.0], ["158b", 1.0], ["158.5b", 0.0]]}},
                "fx": ["hp cutoff=300",
                       {"type": "reverb", "kind": "hall", "decay": "7s", "mix": 1.0, "predelay": "60ms", "shimmer": 0.5,
                        "freeze": {"value": 0, "mod": [{"src": "auto.frz", "amount": 1}]}},
                       "lp cutoff=7000"]}} if "K" in R12 and "Q" in R9 else {})})]
          if "D" in R7 or ("K" in R12 and "Q" in R9) else []),
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
