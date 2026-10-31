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
Form (bars of 4/4), v3: in 16 / A1 16 / A2 28 (A1 grows into it) / break 16 / drop 4 / B2 30 / out 16 = 126 bars
(v2: A2 20, a B1 of 8 after the break, B2 26).

Emits songs/chirpers7-t8.yaml. Edit the music here.
"""
import json
import os
import random

# rounds: T8_R2 = unswap (v2: no composed bass swap; the kick-in plays full and the mixer hands the lows over at the
# overlap midpoint, mixplan swap column 'mid': a composed swap under a linear crossfade sags the low end into a hole).
# T8_R2=none reproduces v1.
R2 = os.environ.get("T8_R2", "unswap")
# T8_R3 = longer (v3: A2, the voice through the thinning static, runs eight bars longer - 20 -> 28 - before the break,
# so the illusion has longer to work before the static clears (chirper-three's note); B1 goes, the break runs straight
# into the drop and the cleared peak (B2 26 -> 30); 250 s). T8_R3=none reproduces v2.
R3 = os.environ.get("T8_R3", "longer")
# T8_R4 = between (v4: the static lands BETWEEN the organ's chords, not on them - the organ's pulses shortened (1.2 and
# 0.85 beats) to leave room; A1 four dropouts between them (beats 1.3, 1.75, 2.2, 3.5), A2 two (1.5, 3.5), the break's
# 3-3-2 kept under its held chords - and the dropouts fade like a radio
# losing the signal: the voice dips over ~20 ms instead of 6, and each burst of static swells in just before the gap
# and out just after, so the noise covers both edges and the brain fills the voice in; chirper-one's note).
# T8_R4=none reproduces v3.
R4 = os.environ.get("T8_R4", "between")
# T8_R5 = tamb (v5: a gospel tambourine - the samba kit's pandeiro jingles - on the 'a' of one and of three in the full
# grooves (A2, B2), level with the off-beat hats: the shuffle of a church band's tambourine against the four, and air
# above 9 kHz). T8_R5=none reproduces v4.
R5 = os.environ.get("T8_R5", "tamb")
# T8_R6 = dark (v6, Harry's 31 Oct steers: darker and wonkier, illusions in front all the way, more time-play).
# - Darker chords, eight bars each: C#m11 | Amaj7#11 (a D#-E rub inside) | F#m9 | G#7b9 (an altered dominant
#   leaning back into C# minor, never quite resolving), in place of C#m9 | Amaj7 | E6 | G#m7.
# - The continuity illusion in the seams too: the seam organ (C#/G# in, the C#m chord out) drops out under static once
#   a bar (in: from bar 9, as t7's tones fade; out: bars 1-12, the last four clean for t9).
# - A Shepard riser (shepard-pad) through the end of the break and the drop.
# - THE RADIO DIES: a tape-stop on the whole mix over the last two beats of the break; the drop starts from silence
#   and the static has cleared. T8_R6=none reproduces v5.
R6 = os.environ.get("T8_R6", "dark")
# T8_R7 = seasick (v7, wM's time-play part 1; Harry's "slight wow on ONE element"): once the static has cleared, the
# organ comes loose from the beat - through B2 it slides a sixteenth behind the kick and back, then a sixteenth ahead
# and back (warp, smooth re-locks), its pulses ducking against a pump that stays on the kick: gospel that sways.
# Locked again before the out seam; the seam organ and the voice keep the song's clock. T8_R7=none reproduces v6.
R7 = os.environ.get("T8_R7", "seasick")

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


FORM = ([("in", 16), ("A1", 16), ("A2", 28), ("break", 16), ("drop2", 4), ("B2", 30), ("out", 16)] if R3 == "longer"
        else [("in", 16), ("A1", 16), ("A2", 20), ("break", 16), ("B1", 8), ("drop2", 4), ("B2", 26), ("out", 16)])
PROG = [(37, [56, 61, 64, 68, 75]),   # C#m9: G#3 C#4 E4 G#4 D#5
        (33, [56, 61, 64, 68]),       # Amaj7: G#3 C#4 E4 G#4 (over A)
        (40, [56, 61, 64, 68]),       # E6: G#3 C#4 E4 G#4 (over E)
        (32, [54, 59, 63, 66])]       # G#m7: F#3 B3 D#4 F#4
if R6 == "dark":
    PROG = [(37, [56, 59, 64, 66, 75]),   # C#m11: G#3 B3 E4 F#4 D#5
            (33, [56, 61, 63, 64]),       # Amaj7#11: G#3 C#4 D#4 E4 (over A: the D#-E rub)
            (42, [57, 61, 64, 68]),       # F#m9: A3 C#4 E4 G#4 (over F#)
            (32, [54, 60, 63, 69])]       # G#7b9: F#3 B#3 D#4 A4 (over G#)
# the sung line, four bars per chord: the stair (C# D# E G#) and its answer, long notes
VOICE = [[(73, 8.0, "^o"), (80, 8.0, "")],     # C# ... G#: the stair's first and last steps, held long
         [(80, 8.0, ""), (76, 8.0, "^o")],     # G# ... E
         [(76, 8.0, ""), (83, 8.0, "^o")],     # E ... B (the answer reaching up)
         [(78, 8.0, "^e"), (73, 8.0, "^o")]]   # F# ... C#: home
BASS = [(0.0, 0.4), (0.75, 0.2), (1.5, 0.25), (2.5, 0.4), (3.25, 0.25)]


def build():
    rng = random.Random(8)
    T = {k: Track(k) for k in ("kickin", "kick", "hats", "clap", "rim", "bass", "organ", "voice", "static", "rise", "tamb",
                               "organseam", "riser")}
    seamgaps = []  # v6: where the seam organ drops out under static
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
            if R5 == "tamb":  # the tambourine on the a's (16ths 3 and 11), the second a little harder
                T["tamb"].add(start + 0.75 + 0.01, 0.3, "pd", 84 + rng.randint(-4, 4))
                T["tamb"].add(start + 2.75 + 0.01, 0.3, "pd", 92 + rng.randint(-4, 4))
        if core or sec in ("drop1", "drop2"):
            for b, ln in BASS:
                T["bass"].add(start + b, ln, nm(root - 12 if root >= 36 else root), 100 if b == 0 else 86)
        # ---- the organ: chords (half-bar pulses in the grooves, held in the break), C#/G# in the seams ----
        so = T["organseam"] if R6 == "dark" else T["organ"]
        if sec == "in" and i % 4 == 0:
            so.add(start, 15.8, "C#3,G#3,C#4", 60 + 2 * i)
        elif sec == "out" and i % 4 == 0:
            so.add(start, 15.8, "C#3,E3,G#3,C#4,G#4", 70)
        elif sec in ("break",) and i % 4 == 0:
            T["organ"].add(start, 15.8, ",".join(nm(x) for x in chord), 72)
        elif core or sec in ("drop1", "drop2"):
            for b in (0.0, 2.5):  # (v4: shorter, so the static has room between the chords)
                ln = (1.2 if b == 0 else 0.85) if R4 == "between" else (1.4 if b == 0 else 1.3)
                T["organ"].add(start + b + 0.02, ln, ",".join(nm(x) for x in chord), 76)
        if R6 == "dark" and ((sec == "in" and i >= 8) or (sec == "out" and i < 12)):
            seamgaps.append((start + 1.5, 0.25))
            T["static"].add(start + 1.46, 0.33, "C5", 90 + rng.randint(-6, 6))
        if R6 == "dark" and ((sec == "break" and i == 8) or (sec == "drop2" and i == 0)):
            T["riser"].add(start, 31.8 if sec == "break" else 15.8, "C#4,G#4", 84)
        # ---- the voice: a phrase per four bars; the gaps by section ----
        if (core or sec == "break") and i % 8 == 0:
            t = start
            for m, d, vow in VOICE[(i // 8) % 4]:  # each phrase at half speed: eight bars, longer notes to sing through
                T["voice"].add(t, d * 2 * 0.98, nm(m), 86, vow)
                t += d * 2
        if sec == "A1":
            beats = ([1.3, 1.75, 2.2, 3.5] if R4 == "between" else [b for b in range(4)])  # every beat (v4: between chords)
        elif sec == "A2":
            beats = ([1.5, 3.5] if R4 == "between" else [b for b in (1, 3)])  # every other beat (v4: between chords)
        elif sec == "break":
            beats = [0.75, 1.5, 3.0]                         # a 3-3-2 of dropouts
        else:
            beats = []                                       # the static clears
        for b in beats:
            if R4 == "between":
                g0 = start + b
                gaps.append((g0, 0.25))
                T["static"].add(g0 - 0.04, 0.33, "C5", 96 + rng.randint(-6, 6))  # covers both edges
            else:
                g0 = start + b + 0.5 if sec != "break" else start + b
                gaps.append((g0, 0.25))
                T["static"].add(g0, 0.25, "C5", 96 + rng.randint(-6, 6))
        if sec in ("drop1", "drop2") and i == 0:
            T["rise"].add(start, 16.0, "C4", 92)
    sec = []
    for name, n in FORM:
        first = next(bb for bb in bars if bb[1] == name)
        sec.append((name, first[0], n))
    return total, bars, sec, T, gaps, seamgaps


def patches():
    return {
        "c2-static-burst": {"about": "chirper-two: a burst of radio static (broadband noise band-limited 300 Hz-7 kHz, "
                                     "flat while held): loud enough that a voice cut under it is heard to go on.",
                            "synth": {"layers": [{"type": "noise"}], "filters": ["hp cutoff=300", "lp cutoff=7000"],
                                      "amp": ({"a": "18ms", "d": "0s", "s": 1.0, "r": "22ms"} if R4 == "between"
                                              else {"a": "2ms", "d": "0s", "s": 1.0, "r": "6ms"})},
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
    total, bars, sec, T, gaps, seamgaps = build()
    st = {n: s for n, s, k in sec}
    tempo = [{"at": "0b", "bpm": 121}, {"at": f"{st['A1']}b", "bpm": 121},
             {"at": f"{st['out']}b", "bpm": 121.5, "ramp": True}]
    gate = [["0b", 0.0]]
    for g0, gl in gaps:  # the voice drops out exactly under each burst (6 ms edges)
        e = 0.04 if R4 == "between" else 0.012  # the voice's dip: ~20 ms like a fading radio (v4), 6 ms before
        gate += [[f"{g0 - e:.4f}b", 0.0], [f"{g0:.4f}b", 1.0], [f"{g0 + gl - e:.4f}b", 1.0], [f"{g0 + gl:.4f}b", 0.0]]
    gate.append([f"{total}b", 0.0])
    sgate = [["0b", 0.0]]
    for g0, gl in seamgaps:
        sgate += [[f"{g0 - 0.04:.4f}b", 0.0], [f"{g0:.4f}b", 1.0], [f"{g0 + gl - 0.04:.4f}b", 1.0], [f"{g0 + gl:.4f}b", 0.0]]
    sgate.append([f"{total}b", 0.0])
    ts0 = st["drop2"] - 2.0  # the radio dies over the break's last two beats
    tstop = [["0b", 0.0], [f"{ts0 - 0.01}b", 0.0], [f"{ts0}b", 1.0], [f"{st['drop2'] - 0.01}b", 1.0],
             [f"{st['drop2']}b", 0.0], [f"{total}b", 0.0]]
    if "B1" in st:
        dyn = [["0b", 0.0], [f"{st['break']}b", -5.0], [f"{st['B1'] - 0.01}b", -5.0], [f"{st['B1']}b", 0.0],
               [f"{st['drop2']}b", -3.0], [f"{st['B2'] - 0.01}b", -3.0], [f"{st['B2']}b", 0.0], [f"{total}b", 0.0]]
    else:  # v3: the break runs straight into the drop
        dyn = [["0b", 0.0], [f"{st['break']}b", -5.0], [f"{st['drop2'] - 0.01}b", -5.0], [f"{st['drop2']}b", -3.0],
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
         **({"warp": [{"over": f"{st['B2'] / 4:g}bar", "to": 0}, {"over": "8bar", "to": 0.25, "curve": "in"},
                      {"over": "8bar", "to": 0, "curve": "smooth"}, {"over": f"{(st['out'] - st['B2']) / 4 - 24:g}bar", "to": 0},
                      {"over": "4bar", "to": -0.25, "curve": "in"}, {"over": "4bar", "to": 0, "curve": "smooth"}]}
            if R7 == "seasick" else {}),
         "fx": [pump, "hp cutoff=300", "reverb kind=hall decay=2.2s mix=0.25"], "score": T["organ"].score(total)},
        *([{"name": "organ-seam", "patch": "organ", "gain": "-12dB", "pan": -0.1,
            "fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.sgap", "amount": -60}]}},
                   "hp cutoff=300", "reverb kind=hall decay=2.2s mix=0.25"],
            "auto": {"sgap": {"points": sgate}}, "score": T["organseam"].score(total)},
           {"name": "riser", "patch": "shepard-pad", "gain": "-13dB", "fx": ["hp cutoff=250", "width width=1.4"],
            "score": T["riser"].score(total)}] if R6 == "dark" else []),
        {"name": "voice", "patch": "voice", "gain": "-6dB", "pan": 0.05,
         "fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.gap", "amount": -60}]}},
                "hp cutoff=200", "reverb kind=hall decay=2.4s mix=0.25"],
         "auto": {"gap": {"points": gate}}, "score": T["voice"].score(total)},
        {"name": "static", "patch": "c2-static-burst", "gain": "-8dB", "pan": 0.05,
         "fx": [{"type": "crush", "bits": 9, "rate": 14000, "mix": 0.4}], "score": T["static"].score(total)},
        {"name": "rise", "patch": "c2-rise", "gain": "-20dB", "fx": ["width width=1.5"], "score": T["rise"].score(total)},
    ] + ([{"name": "tamb", "patch": "samba-kit", "gain": "-3dB", "pan": 0.3,
           "fx": ["hp cutoff=1800", "reverb kind=room decay=0.6s mix=0.18"], "score": T["tamb"].score(total)}]
         if R5 == "tamb" else [])
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
        "master: " + json.dumps({"fx": ([{"type": "tapestop", "time": "2b", "up": "0.25b", "curve": 2.0, "mix": 1,
                                          "stop": {"value": 0, "mod": [{"src": "auto.ts", "amount": 1}]}}]
                                        if R6 == "dark" else []) + [
                                        {"type": "eq", "bands": ["hp cutoff=28", "peak cutoff=320 gain=-6dB q=0.8",
                                                               "peak cutoff=3500 gain=2dB q=0.7",
                                                               "highshelf cutoff=6000 gain=2dB"]},
                                        "glue threshold=-20dB ratio=2 attack=10ms release=150ms makeup=1dB",
                                        {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                                        {"type": "limiter", "ceiling": "-1.2dB", "release": "80ms"}],
                                 "auto": {"dyn": {"points": dyn}, **({"ts": {"points": tstop}} if R6 == "dark" else {})}}),
        "tracks:",
    ]
    lines += ["  - " + json.dumps(t) for t in tracks]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write("\n".join(lines) + "\n")
    print(f"wrote {OUT}: {len(bars)} bars, {len(gaps)} gaps; {secs}")


if __name__ == "__main__":
    main()
