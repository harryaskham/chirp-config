#!/usr/bin/env python3
"""chirpers7-t4 (The Endless Stair, track 4). Composed by chirper-two: AFRO-TINGED MINIMAL HOUSE.

"The Tritone Question". A rolling, percussive minimal groove whose hook is the TRITONE PARADOX: two Shepard tones a
tritone apart (B then F), so the interval has no up or down; half the room hears it rise, half hears it fall, and the
same listener can flip. The track keeps asking which.
- THE QUESTION: the pair B-F (Shepard tones: octave-spaced partials under a fixed bell) on the off-beats; then the stair's
  notes each with its tritone (B-F, C#-G, D-G#, F#-C), so the stair climbs while every step is ambiguous.
- THE VOICE asks it aloud once the seam has passed: "up... or down?" (t3 handed over "one more step up").
- THE GROOVE (afro-tinged): the rumble kick four to the floor, a 12/8 bell pattern on the cowbell over it, toms in
  triplet figures, triplet shaker hats, a clap late on the four; the cross-rhythm of three against four is the motion.
- THE BASS: chirper-two's machine boom played as a bass line on B (tuned per note), pumped.
- THE CHORD: a sparse Bm9 dub stab into a feedback echo room.
- THE SEAMS: in, t3's last 16 bars (kick, hats, claps, the phrase "one more step up" spoken, E minor) play over t4's
  first 16 bars of the plain kick, triplet shakers and open hats (v2: the mixer hands the lows over at the overlap's
  midpoint, mixplan swap 'mid'; v1's composed swap, a high-passed kick, sagged the low end under the linear crossfade); out, t4's last 16 bars at 119.5 are kick, hats and a held B (the boom)
  for t5's 808 on B1.
Tempo 119 -> 119.5 (a ramp inside the track). B minor (10A).
Form (bars of 4/4): in 16 / A1 24 (sparse: kick, shakers, toms, the boom, the question) / drop 4 / A2 16 (+ the bell,
the clap, the chord) / break 12 (no kick: toms, the voice, the question slowed) / B1 8 / drop 4 / B2 24 (the peak:
sixteenth shakers, the toms rolling every other bar) / out 16 = 124 bars.

Emits songs/chirpers7-t4.yaml. Edit the music here.
"""
import json
import os
import random

# rounds: T4_R2 = unswap (v2: no composed bass swap; the kick-in plays full and the mixer hands the lows over at the
# overlap midpoint, mixplan swap column 'mid': a composed swap under a linear crossfade sags the low end into a hole).
# T4_R2=none reproduces v1.
R2 = os.environ.get("T4_R2", "unswap")

OUT = os.environ.get("T4_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers7-t4.yaml")
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


class Track:
    def __init__(self, name):
        self.name, self.ev = name, []

    def add(self, at, ln, head, vel, art=""):
        self.ev.append((round(max(0.0, at), 4), max(0.03, round(ln, 4)), head, int(max(1, min(127, vel))), art))

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
        for i, (s, ln, head, vel, art) in enumerate(merged):
            nxt = merged[i + 1][0] if i + 1 < len(merged) else total
            ln = min(ln, nxt - s)
            if s - pos > 1e-4:
                toks.append(f"R/{s - pos:.4g}b")
            toks.append(f"{head}/{ln:.4g}b@{vel}{art}")
            pos = s + ln
        if total - pos > 1e-4:
            toks.append(f"R/{total - pos:.4g}b")
        return " ".join(toks)


FORM = [("in", 16), ("A1", 24), ("drop1", 4), ("A2", 16), ("break", 12), ("B1", 8), ("drop2", 4), ("B2", 24),
        ("out", 16)]
STAIR = [71, 73, 74, 78]                         # B C# D F#: the stair in B minor
CHORD = [59, 62, 66, 69, 73]                     # Bm9: B3 D4 F#4 A4 C#5
BELL = [0, 2, 4, 5, 7, 9, 11]                    # the 12/8 bell, in triplet eighths (12 to the bar)
BASS = [(0.0, 35, 0.6), (1.5, 35, 0.3), (2.0, 42, 0.4), (2.75, 35, 0.3), (3.5, 38, 0.4)]  # B1 B1 F#2 B1 D2
SPEECH = [["ah1-p", "ao1-r", "d-aw1-n"]]         # "up ... or down?"


def build():
    rng = random.Random(4)
    T = {k: Track(k) for k in ("kickin", "kick", "hats", "clap", "bell", "toms", "bass", "pair", "stab", "voice", "rise")}
    bars, pos = [], 0.0
    for name, n in FORM:
        for i in range(n):
            bars.append((pos, name, i, n))
            pos += 4.0
    total = pos
    step = 0
    for bi, (start, sec, i, n) in enumerate(bars):
        core = sec in ("A1", "A2", "B1", "B2")
        full = sec in ("A2", "B1", "B2")
        if core or sec in ("in", "out"):
            for b in range(4):  # under t3's tail the plain kick, softer; the rumble kick once the seam has passed
                (T["kickin"] if sec == "in" else T["kick"]).add(start + b, 1.0, "k" if sec == "in" else "kr",
                                                               (96 if sec == "in" else 112) - (0 if b == 0 else 8))
        # ---- triplet shaker hats (12 to the bar), accents on each beat's last triplet ----
        if sec == "B2":  # the peak: sixteenth shakers
            for s in range(16):
                T["hats"].add(start + s * 0.25 + 0.01, 0.1, "h", (60 if s % 4 == 3 else 46) + rng.randint(-5, 5))
        elif core or sec == "in":
            for k in range(12):
                if sec == "A1" and k % 3 != 2:
                    continue  # A1: the accented triplets only (sparse); A2 and B1 fill in the rest
                v = (58 if k % 3 == 2 else 42) + rng.randint(-5, 5)
                T["hats"].add(start + k / 3 + 0.01, 0.12, "h", v)
        if sec in ("out", "in"):
            for b in (0.5, 1.5, 2.5, 3.5):
                T["hats"].add(start + b + 0.01, 0.35, "oh", 62)
        # ---- the 12/8 bell over the four ----
        if full:
            for k in BELL:
                T["bell"].add(start + k / 3, 0.2, "cb", 74 if k in (0, 7) else 60)
        # ---- toms in triplet figures: low on the one, a three-note pickup into each bar's four ----
        if core:
            T["toms"].add(start + 0.0, 0.5, "lt", 70)
            for k, piece in enumerate(("mt", "mt", "ht")):
                T["toms"].add(start + 3.0 + k / 3, 0.3, piece, 62 + 4 * k)
            if i % 4 == 3 or (sec == "B2" and i % 2 == 1):
                for k, piece in enumerate(("ht", "mt", "lt", "ht", "mt", "lt")):
                    T["toms"].add(start + 2.0 + k / 3, 0.3, piece, 66 + 2 * k)
        if full:
            T["clap"].add(start + 3.0 + 1 / 3, 0.5, "cp", 88)  # late on the four
        # ---- the boom bass ----
        if sec == "break":  # toms alone, slow, under the question
            for k, piece in enumerate(("lt", "mt", "lt")):
                T["toms"].add(start + k * 4 / 3, 0.5, piece, 60)
        if core or sec in ("drop1", "drop2"):
            for b, m, ln in BASS:
                T["bass"].add(start + b, ln, nm(m), 104 if b == 0 else 90)
        if sec == "out" and i % 4 == 0:
            T["bass"].add(start, 15.8, nm(35), 96)  # the held B for t5
        # ---- THE QUESTION: Shepard pairs a tritone apart on the off-beats ----
        if sec not in ("in", "out"):  # nothing pitched under t3's phrase in the seam
            pairs = 1 if sec in ("in", "A1") else (2 if sec != "break" else 1)
            for p in range(pairs):
                root = STAIR[step % 4] if sec not in ("in", "A1") else 71
                step += 1 if sec not in ("in", "A1") else 0
                t0 = start + (0.5 if p == 0 else 2.5)
                ln = 0.45 if sec != "break" else 1.4
                T["pair"].add(t0, ln, nm(root), 80)
                T["pair"].add(t0 + (0.5 if sec != "break" else 1.5), ln, nm(root + 6), 80)
        # ---- the chord, sparse ----
        if full and i % 2 == 0:
            T["stab"].add(start + 1.75, 0.3, ",".join(nm(x) for x in CHORD), 80)
        if sec == "break" and i % 4 == 0:
            T["stab"].add(start, 0.4, ",".join(nm(x) for x in CHORD), 76)
        # ---- the voice: once the seam has passed, and again in the break ----
        if (sec == "A1" and i == 0) or (sec == "break" and i == 8):
            t = start + 1.0
            for k, syl in enumerate(SPEECH[0]):
                f0 = "0>40>90" if k == 0 else ("0>-20" if k == 1 else "40>-30>-120")
                T["voice"].add(t, 0.9, "A2", 82, f"^ph={syl}^f0={f0}")
                t += 1.5 if k == 0 else 1.0
        if sec in ("drop1", "drop2") and i == 0:
            T["rise"].add(start, 16.0, "C4", 92)
    sec = []
    for name, n in FORM:
        first = next(bb for bb in bars if bb[1] == name)
        sec.append((name, first[0], n))
    return total, bars, sec, T


def patches():
    return {
        "c2-tritone": {"about": "chirper-two: the tritone paradox's voice, a Shepard tone (octave-spaced partials under "
                                "a fixed bell centred near 500 Hz, wide): a pair a tritone apart has no up or down.",
                       "synth": {"layers": [{"type": "shepard", "shepard": {"octaves": 9, "center": "500hz", "width": 1.4}}],
                                 "amp": {"a": "6ms", "d": "500ms", "s": 0.3, "r": "300ms", "curve": 2}},
                       "play": {"vel_sens": 0.5}},
        "c2-boom-bass": {"about": "chirper-two: the machine layer's 808 boom as a bass line, short and driven.",
                         "synth": {"layers": [{"type": "machine", "machine": {"part": "boom", "decay": "420ms",
                                                                               "punch": 3, "drive": 0.35, "click": 0.1}}],
                                   "amp": {"a": "0.1ms", "d": "0s", "s": 1, "r": "120ms"}},
                         "play": {"mono": True, "vel_sens": 0.5}},
        "c2-dub-stab": {"about": "chirper-two's dub chord stab (see t1).",
                        "synth": {"layers": [{"wave": "saw", "detune": -7}, {"wave": "saw", "detune": 7},
                                             {"wave": "square", "level": "-8dB"}],
                                  "filters": [{"kind": "lp", "q": 1.4,
                                               "cutoff": {"value": 500, "mod": [{"src": "env.f", "amount": 2.2}]}}],
                                  "env": {"f": {"a": "1ms", "d": "160ms", "s": 0.0}},
                                  "amp": {"a": "2ms", "d": "280ms", "s": 0.0, "r": "90ms"}},
                        "play": {"vel_sens": 0.6}},
        "c2-rise": {"about": "chirper-two: a noise rise.",
                    "synth": {"layers": [{"type": "noise"}],
                              "filters": [{"kind": "bp", "q": 1.5,
                                           "cutoff": {"value": 300, "mod": [{"src": "env.up", "amount": 5.0}]}}],
                              "env": {"up": {"a": "8s", "d": "1s", "s": 1.0}},
                              "amp": {"a": "6s", "d": "1s", "s": 1.0, "r": "300ms"}}},
    }


def main():
    total, bars, sec, T = build()
    st = {n: s for n, s, k in sec}
    tempo = [{"at": "0b", "bpm": 119}, {"at": f"{st['A1']}b", "bpm": 119},
             {"at": f"{st['out']}b", "bpm": 119.5, "ramp": True}]
    dyn = [["0b", 0.0], [f"{st['drop1']}b", -3.0], [f"{st['A2'] - 0.01}b", -3.0], [f"{st['A2']}b", 0.0],
           [f"{st['break']}b", -7.0], [f"{st['B1'] - 0.01}b", -7.0], [f"{st['B1']}b", 0.0], [f"{st['drop2']}b", -3.0],
           [f"{st['B2'] - 0.01}b", -3.0], [f"{st['B2']}b", 0.0], [f"{total}b", 0.0]]
    pump = {"type": "pump", "on": "kick.kr", "depth": "-7dB", "attack": "3ms", "release": "340ms", "curve": 0.8}
    tracks = [
        {"name": "kick", "patch": "machine-kit", "gain": "0dB", "score": T["kick"].score(total)},
        {"name": "kick-in", "patch": "machine-kit", "gain": "-2dB", "fx": ([] if R2 == "unswap" else ["hp cutoff=110"]),  # the bass swap: t3 keeps
         "score": T["kickin"].score(total)},                                                  # the low end in the seam
        {"name": "hats", "patch": "machine-kit", "gain": "-3dB", "pan": 0.12,
         "fx": ["hp cutoff=600", "reverb kind=room decay=0.5s mix=0.12"], "score": T["hats"].score(total)},
        {"name": "bell", "patch": "machine-kit", "gain": "-10dB", "pan": -0.2,
         "fx": ["reverb kind=room decay=0.8s mix=0.2"], "score": T["bell"].score(total)},
        {"name": "toms", "patch": "machine-kit", "gain": "-5dB", "pan": 0.1,
         "fx": ["reverb kind=room decay=0.9s mix=0.18"], "score": T["toms"].score(total)},
        {"name": "clap", "patch": "machine-kit", "gain": "-5dB", "fx": ["reverb kind=plate decay=1.1s mix=0.2"],
         "score": T["clap"].score(total)},
        {"name": "bass", "patch": "c2-boom-bass", "gain": "-7dB", "fx": [pump, "hp cutoff=45"],
         "score": T["bass"].score(total)},
        {"name": "pair", "patch": "c2-tritone", "gain": "-8dB",
         "fx": [{"type": "delay", "time": "3/8", "feedback": 0.3, "mix": 0.22, "ping_pong": True, "tone": 3000},
                "reverb kind=hall decay=2.5s mix=0.3"], "score": T["pair"].score(total)},
        {"name": "stab", "patch": "c2-dub-stab", "gain": "-12dB", "sends": {"room": "-3dB"}, "fx": [pump, "hp cutoff=200"],
         "score": T["stab"].score(total)},
        {"name": "voice", "patch": "voice-speech", "gain": "-8dB", "pan": -0.15,
         "fx": ["hp cutoff=250", {"type": "delay", "time": "3/8", "feedback": 0.35, "mix": 0.3, "tone": 2500},
                "reverb kind=hall decay=3s mix=0.35"], "score": T["voice"].score(total)},
        {"name": "rise", "patch": "c2-rise", "gain": "-20dB", "fx": ["width width=1.5"], "score": T["rise"].score(total)},
    ]
    buses = {"room": {"gain": "-5dB",
                      "fx": ["hp cutoff=250", "lp cutoff=2400",
                             {"type": "tape", "drive": 0.35, "warmth": 0.6, "wow": 3, "flutter": 1, "seed": 4},
                             "limiter ceiling=-6dB"],
                      "returns": [{"from": "room", "gain": "-4dB", "time": "3/16"}]}}
    secs = "; ".join(f"{n} from {s:.0f}b ({k} bars)" for n, s, k in sec)
    about = ("Chirpers - The Endless Stair, track 4. Original composition by chirper-two, generated by "
             "compose/chirpers7/src/chirpers7-t4.py. Afro-tinged minimal house, 119 -> 119.5 bpm, B minor: the TRITONE "
             "PARADOX as the hook (Shepard-tone pairs a tritone apart, B-F, then each stair step with its tritone: no up "
             f"or down), a 12/8 bell and triplet toms over the four, a boom bass, a voice asking 'up or down?'. Sections: {secs}.")
    lines = [
        f"about: {json.dumps(about)}",
        "meta: " + json.dumps({"artist": "Chirpers", "album": "The Endless Stair", "title": "The Tritone Question",
                               "track": 4, "year": 2026}),
        "tempo: " + json.dumps(tempo),
        f'length: "{total:g}b"',
        'tail: "1s"',
        'ceiling: "-1dB"',
        'volume: "0dB"',
        "loudness: -11",
        "true_peak: true",
        "patches: " + json.dumps(patches()),
        "buses: " + json.dumps(buses),
        "master: " + json.dumps({"fx": [{"type": "eq", "bands": ["hp cutoff=28", "lowshelf cutoff=80 gain=-5dB",
                                                               "peak cutoff=160 gain=-3dB q=0.8",
                                                               "peak cutoff=3500 gain=2dB q=0.7",
                                                               "highshelf cutoff=6000 gain=3dB"]},
                                        "glue threshold=-20dB ratio=2 attack=10ms release=150ms makeup=1dB",
                                        {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                                        {"type": "limiter", "ceiling": "-1.2dB", "release": "80ms"}],
                                 "auto": {"dyn": {"points": dyn}}}),
        "tracks:",
    ]
    lines += ["  - " + json.dumps(t) for t in tracks]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write("\n".join(lines) + "\n")
    print(f"wrote {OUT}: {len(bars)} bars; {secs}")


if __name__ == "__main__":
    main()
