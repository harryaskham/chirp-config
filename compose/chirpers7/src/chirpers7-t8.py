#!/usr/bin/env python3
"""chirpers7-t8 (The Endless Stair, track 8). Composed by chirper-two: SOULFUL VOCAL HOUSE.

"Through the Static". A warm, gospel-tinged deep house where the voice is the CONTINUITY ILLUSION: a sung line (chirp's
voice engine) whose long notes are cut out again and again, each gap filled by a louder burst of radio static; the ear
hears the voice go on singing through the static, though nothing sings there. Through the track the dropouts thin, and
at the peak the static clears and the voice really does sing on, whole.
- THE VOICE sings THE STAIR (C# D# E G#) in long gospel notes over drawbar-organ chords (C#m9 | Amaj7 | E6 | G#m7, eight bars each: t7's
  progression, carried on). The gaps are a gain lane on the voice track (so the voice itself never stops: same phase,
  same breath either side) with a static burst exactly in each gap, every beat in A1, every other beat in A2, on a
  3-3-2 in the break, none at the peak.
- THE GROOVE: the rumble kick, claps on two and four, open hats, sixteenth shakers, a rim; a rolling bass, pumped.
- THE SEAMS: in, t7's last 16 bars (kick, clicks, claps, the octave-illusion tones on G#/C# fading) play over t8's first
  16 bars of the plain kick (v2: the mixer swaps the lows at the overlap's midpoint, mixplan swap 'mid'), hats and the
  organ holding C# and G#; out, t8's last 16 bars at
  121.5: the rumble kick, hats and a held C# minor organ chord (C# E G#), G# on top for t9's G#.
Tempo 121 -> 121.5 (a ramp inside the track). C# minor (12A).
Form (bars of 4/4): in 16 / A1 16 / A2 20 (A1 grows into it) / break 16 / B1 8 / drop 4 / B2 26 / out 16 = 122 bars.

Emits songs/chirpers7-t8.yaml. Edit the music here.
"""
import json
import os
import random

# rounds: T8_R2 = unswap (v2: no composed bass swap; the kick-in plays full and the mixer hands the lows over at the
# overlap midpoint, mixplan swap column 'mid': a composed swap under a linear crossfade sags the low end into a hole).
# T8_R2=none reproduces v1.
R2 = os.environ.get("T8_R2", "unswap")

OUT = os.environ.get("T8_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers7-t8.yaml")
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


FORM = [("in", 16), ("A1", 16), ("A2", 20), ("break", 16), ("B1", 8), ("drop2", 4), ("B2", 26),
        ("out", 16)]
PROG = [(37, [56, 61, 64, 68, 75]),   # C#m9: G#3 C#4 E4 G#4 D#5
        (33, [56, 61, 64, 68]),       # Amaj7: G#3 C#4 E4 G#4 (over A)
        (40, [56, 61, 64, 68]),       # E6: G#3 C#4 E4 G#4 (over E)
        (32, [54, 59, 63, 66])]       # G#m7: F#3 B3 D#4 F#4
# the sung line, four bars per chord: the stair (C# D# E G#) and its answer, long notes
VOICE = [[(73, 8.0, "^o"), (80, 8.0, "")],     # C# ... G#: the stair's first and last steps, held long
         [(80, 8.0, ""), (76, 8.0, "^o")],     # G# ... E
         [(76, 8.0, ""), (83, 8.0, "^o")],     # E ... B (the answer reaching up)
         [(78, 8.0, "^e"), (73, 8.0, "^o")]]   # F# ... C#: home
BASS = [(0.0, 0.4), (0.75, 0.2), (1.5, 0.25), (2.5, 0.4), (3.25, 0.25)]


def build():
    rng = random.Random(8)
    T = {k: Track(k) for k in ("kickin", "kick", "hats", "clap", "rim", "bass", "organ", "voice", "static", "rise")}
    gaps = []  # (start beat, length beats): where the voice is cut and the static bursts
    bars, pos = [], 0.0
    for name, n in FORM:
        for i in range(n):
            bars.append((pos, name, i, n))
            pos += 4.0
    total = pos
    for bi, (start, sec, i, n) in enumerate(bars):
        core = sec in ("A1", "A2", "B1", "B2")
        full = sec in ("A2", "B1", "B2")
        root, chord = PROG[(i // 8) % 4]  # eight bars a chord: long gospel spans
        # ---- kicks: thin under t7's tail (a bass swap), then the rumble kick ----
        if core or sec in ("in", "out"):
            for b in range(4):
                (T["kickin"] if sec == "in" else T["kick"]).add(start + b, 1.0, "k" if sec == "in" else "kr",
                                                               (96 if sec == "in" else 112) - (0 if b == 0 else 8))
        if core or sec in ("in", "out"):
            for b in (0.5, 1.5, 2.5, 3.5):
                T["hats"].add(start + b + 0.01, 0.35, "oh", 64)
        if full:
            for s in range(16):
                if s % 2:
                    T["hats"].add(start + s * 0.25 + 0.015, 0.1, "h", 48 + rng.randint(-5, 5))
            T["clap"].add(start + 1.0, 0.5, "cp", 98)
            T["clap"].add(start + 3.0, 0.5, "cpw" if i % 4 == 3 else "cp", 98)
            for o in (0.0, 0.75, 1.5):
                T["rim"].add(start + 2.0 + o + 0.02, 0.2, "rs", 60)
        if core or sec in ("drop1", "drop2"):
            for b, ln in BASS:
                T["bass"].add(start + b, ln, nm(root - 12 if root >= 36 else root), 100 if b == 0 else 86)
        # ---- the organ: chords (half-bar pulses in the grooves, held in the break), C#/G# in the seams ----
        if sec == "in" and i % 4 == 0:
            T["organ"].add(start, 15.8, "C#3,G#3,C#4", 60 + 2 * i)
        elif sec == "out" and i % 4 == 0:
            T["organ"].add(start, 15.8, "C#3,E3,G#3,C#4,G#4", 70)
        elif sec in ("break",) and i % 4 == 0:
            T["organ"].add(start, 15.8, ",".join(nm(x) for x in chord), 72)
        elif core or sec in ("drop1", "drop2"):
            for b in (0.0, 2.5):
                T["organ"].add(start + b + 0.02, 1.4 if b == 0 else 1.3, ",".join(nm(x) for x in chord), 76)
        # ---- the voice: a phrase per four bars; the gaps by section ----
        if (core or sec == "break") and i % 8 == 0:
            t = start
            for m, d, vow in VOICE[(i // 8) % 4]:  # each phrase at half speed: eight bars, longer notes to sing through
                T["voice"].add(t, d * 2 * 0.98, nm(m), 86, vow)
                t += d * 2
        if sec == "A1":
            beats = [b for b in range(4)]                    # every beat
        elif sec == "A2":
            beats = [b for b in (1, 3)]                      # every other beat
        elif sec == "break":
            beats = [0.75, 1.5, 3.0]                         # a 3-3-2 of dropouts
        else:
            beats = []                                       # the static clears
        for b in beats:
            g0 = start + b + 0.5 if sec != "break" else start + b
            gaps.append((g0, 0.25))
            T["static"].add(g0, 0.25, "C5", 96 + rng.randint(-6, 6))
        if sec in ("drop1", "drop2") and i == 0:
            T["rise"].add(start, 16.0, "C4", 92)
    sec = []
    for name, n in FORM:
        first = next(bb for bb in bars if bb[1] == name)
        sec.append((name, first[0], n))
    return total, bars, sec, T, gaps


def patches():
    return {
        "c2-static-burst": {"about": "chirper-two: a burst of radio static (broadband noise band-limited 300 Hz-7 kHz, "
                                     "flat while held): loud enough that a voice cut under it is heard to go on.",
                            "synth": {"layers": [{"type": "noise"}], "filters": ["hp cutoff=300", "lp cutoff=7000"],
                                      "amp": {"a": "2ms", "d": "0s", "s": 1.0, "r": "6ms"}},
                            "play": {"vel_sens": 0.6}},
        "c2-rollbass": {"about": "chirper-two: a rolling deep-house bass (see t2).",
                        "synth": {"layers": [{"wave": "sine"}, {"wave": "saw", "level": "-10dB"}],
                                  "filters": [{"kind": "lp", "q": 1.0,
                                               "cutoff": {"value": 260, "mod": [{"src": "env.f", "amount": 1.6}]}}],
                                  "env": {"f": {"a": "1ms", "d": "120ms", "s": 0.0}},
                                  "amp": {"a": "2ms", "d": "220ms", "s": 0.4, "r": "60ms"}},
                        "play": {"vel_sens": 0.6, "mono": True}},
        "c2-rise": {"about": "chirper-two: a noise rise.",
                    "synth": {"layers": [{"type": "noise"}],
                              "filters": [{"kind": "bp", "q": 1.5,
                                           "cutoff": {"value": 300, "mod": [{"src": "env.up", "amount": 5.0}]}}],
                              "env": {"up": {"a": "8s", "d": "1s", "s": 1.0}},
                              "amp": {"a": "6s", "d": "1s", "s": 1.0, "r": "300ms"}}},
    }


def main():
    total, bars, sec, T, gaps = build()
    st = {n: s for n, s, k in sec}
    tempo = [{"at": "0b", "bpm": 121}, {"at": f"{st['A1']}b", "bpm": 121},
             {"at": f"{st['out']}b", "bpm": 121.5, "ramp": True}]
    gate = [["0b", 0.0]]
    for g0, gl in gaps:  # the voice drops out exactly under each burst (6 ms edges)
        gate += [[f"{g0 - 0.012:.4f}b", 0.0], [f"{g0:.4f}b", 1.0], [f"{g0 + gl - 0.012:.4f}b", 1.0], [f"{g0 + gl:.4f}b", 0.0]]
    gate.append([f"{total}b", 0.0])
    dyn = [["0b", 0.0], [f"{st['break']}b", -5.0], [f"{st['B1'] - 0.01}b", -5.0], [f"{st['B1']}b", 0.0], [f"{st['drop2']}b", -3.0],
           [f"{st['B2'] - 0.01}b", -3.0], [f"{st['B2']}b", 0.0], [f"{total}b", 0.0]]
    pump = {"type": "pump", "on": "kick.kr", "depth": "-6dB", "attack": "3ms", "release": "330ms", "curve": 0.8}
    tracks = [
        {"name": "kick", "patch": "machine-kit", "gain": "0dB", "score": T["kick"].score(total)},
        {"name": "kick-in", "patch": "machine-kit", "gain": "-2dB", "fx": ([] if R2 == "unswap" else ["hp cutoff=110"]), "score": T["kickin"].score(total)},
        {"name": "hats", "patch": "machine-kit", "gain": "-3dB", "pan": 0.1,
         "fx": ["hp cutoff=500", "reverb kind=room decay=0.5s mix=0.1"], "score": T["hats"].score(total)},
        {"name": "clap", "patch": "machine-kit", "gain": "-4dB", "fx": ["reverb kind=plate decay=1.3s mix=0.25"],
         "score": T["clap"].score(total)},
        {"name": "rim", "patch": "machine-kit", "gain": "-9dB", "pan": -0.25, "score": T["rim"].score(total)},
        {"name": "bass", "patch": "c2-rollbass", "gain": "-2dB", "fx": [pump], "score": T["bass"].score(total)},
        {"name": "organ", "patch": "organ", "gain": "-12dB", "pan": -0.1,
         "fx": [pump, "hp cutoff=300", "reverb kind=hall decay=2.2s mix=0.25"], "score": T["organ"].score(total)},
        {"name": "voice", "patch": "voice", "gain": "-6dB", "pan": 0.05,
         "fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.gap", "amount": -60}]}},
                "hp cutoff=200", "reverb kind=hall decay=2.4s mix=0.25"],
         "auto": {"gap": {"points": gate}}, "score": T["voice"].score(total)},
        {"name": "static", "patch": "c2-static-burst", "gain": "-8dB", "pan": 0.05,
         "fx": [{"type": "crush", "bits": 9, "rate": 14000, "mix": 0.4}], "score": T["static"].score(total)},
        {"name": "rise", "patch": "c2-rise", "gain": "-20dB", "fx": ["width width=1.5"], "score": T["rise"].score(total)},
    ]
    secs = "; ".join(f"{n} from {s:.0f}b ({k} bars)" for n, s, k in sec)
    about = ("Chirpers - The Endless Stair, track 8. Original composition by chirper-two, generated by "
             "compose/chirpers7/src/chirpers7-t8.py. Soulful vocal house, 121 -> 121.5 bpm, C# minor: a sung voice as "
             "the CONTINUITY ILLUSION (its long notes cut out under bursts of radio static, heard to sing on through "
             f"them), the static clearing at the peak; organ chords C#m9 Amaj7 E6 G#m7. Sections: {secs}.")
    lines = [
        f"about: {json.dumps(about)}",
        "meta: " + json.dumps({"artist": "Chirpers", "album": "The Endless Stair", "title": "Through the Static",
                               "track": 8, "year": 2026}),
        "tempo: " + json.dumps(tempo),
        f'length: "{total:g}b"',
        'tail: "1s"',
        'ceiling: "-1dB"',
        'volume: "0dB"',
        "loudness: -11",
        "true_peak: true",
        "patches: " + json.dumps(patches()),
        "master: " + json.dumps({"fx": [{"type": "eq", "bands": ["hp cutoff=28", "peak cutoff=320 gain=-6dB q=0.8",
                                                               "peak cutoff=3500 gain=2dB q=0.7",
                                                               "highshelf cutoff=6000 gain=2dB"]},
                                        "glue threshold=-20dB ratio=2 attack=10ms release=150ms makeup=1dB",
                                        {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                                        {"type": "limiter", "ceiling": "-1.2dB", "release": "80ms"}],
                                 "auto": {"dyn": {"points": dyn}}}),
        "tracks:",
    ]
    lines += ["  - " + json.dumps(t) for t in tracks]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write("\n".join(lines) + "\n")
    print(f"wrote {OUT}: {len(bars)} bars, {len(gaps)} gaps; {secs}")


if __name__ == "__main__":
    main()
