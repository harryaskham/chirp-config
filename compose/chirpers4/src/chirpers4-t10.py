#!/usr/bin/env python3
"""chirpers4-t10 (Phantom Downbeat, track 10, the closer). Composed by chirper-two: ACID / INDUSTRIAL CLOSER.

"No Floor". Hard acid techno whose illusions are about motion: a build that accelerates for ever without the tempo
moving, a rise that never arrives and, at the end, a fall that never lands.
- THE GRIND: the record opens on industrial noise, a metal clank (struck-bar partials, driven and crushed) and a
  rumble; the kick comes in muffled and opens.
- THE ACID: a 303 riff (chirp's acid: velocity is accent, overlapping notes slide) on sixteen steps, its ladder
  opening over the whole record and self-oscillating in the break; at the drop a second acid answers an octave up.
- THE STAIRCASE (a Risset accelerando): strands of rim hits, each an octave of speed from the next, all speeding up
  together, the slowest fading in as the fastest fade out, so the build keeps accelerating and never arrives, over a
  kick that never changes tempo.
- THE DROP: a distorted 909 kick on top of the punchy one, a rumble bus (a full-wet hall, lo-passed, driven, pumped
  by the kick), claps, open hats and a ride.
- THE BREAK: the kick goes and an endlessly rising Shepard tone (fx-riser-shepard) climbs while the acid rings.
- NO FLOOR: after the last peak the kick leaves and the same Shepard tone, resampled and played backwards (a shadow
  song: no WAVs), falls for ever under the acid closing down, while the opening's grind (noise, clank, rumble)
  comes back: the record ends where it began, falling.
- THE ACID AGAIN: after the drop the groove comes back without the distorted kick, the riff's ladder where it was
  before the build: the floor you knew, briefly.
Form (bars of 4/4, 138 bpm): grind 16 / acid 24 / staircase 24 / drop 24 / acid again 16 / break 16 / peak 24 /
no floor 20 = 164 bars, ~285 s.

Emits songs/chirpers4-t10.yaml. Edit the music here.
"""
import json
import math
import os
import random

OUT = os.environ.get("T10_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers4-t10.yaml")
BPM = 138
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


class Track:
    def __init__(self, name):
        self.name, self.ev = name, []

    def add(self, at, ln, head, vel):
        self.ev.append((round(max(0.0, at), 4), max(0.03, round(ln, 4)), head, int(max(1, min(127, vel)))))

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


FORM = [("grind", 16), ("acid", 24), ("staircase", 24), ("drop", 24), ("again", 16), ("break", 16), ("peak", 24),
        ("nofloor", 20)]
S16 = 0.25
# the acid riff, sixteen steps: (midi or None, accent, slide); F# minor, F#1 = 30
RIFF = [(30, 1, 0), (30, 0, 0), (None, 0, 0), (42, 0, 1), (30, 0, 0), (33, 1, 0), (None, 0, 0), (30, 0, 0),
        (37, 1, 0), (30, 0, 0), (40, 0, 1), (30, 0, 0), (None, 0, 0), (42, 1, 0), (30, 0, 0), (33, 0, 0)]
# the answer, an octave up, on the riff's second half (call and response)
ANSWER = [(None, 0, 0)] * 8 + [(54, 1, 1), (52, 0, 0), (49, 0, 1), (None, 0, 0), (45, 1, 0), (42, 0, 1),
                               (45, 0, 0), (None, 0, 0)]
CLANK = (3, 6, 11, 14)  # the clank's sixteenths: off the beat, off the backbeat
# Round 2 (v2), Harry's note "more interesting acid throb bass": T = THE THROB: the riff moves to its own 303 voice
# (c2-throb: a saw and a sub square into a self-oscillating ladder) whose cutoff follows a snappy per-note envelope
# (deeper on accents) and two slow LFOs on song time, 3 bars and 5 bars long, while a 7-bar LFO moves its resonance,
# so the squelch never sits still and the three cycles only line up every 105 bars; E = THE PATTERN EVOLVES: the same
# notes, but the accents rotate every four bars (as written / in threes across the bar / on the off-beats), the
# slides move every five, every seventh bar throws its tail an octave up, and in the drop and the peak the riff's
# holes fill so the bass throbs on every sixteenth; P = it breathes harder with the kick (pump -9 dB, release 290 ms,
# about two-thirds of a beat, curve 0.8).
R2 = set(filter(None, os.environ.get("T10_R2", "T,E,P").split(","))) - {"none"}
# Round 3 (v3), polish (Harry: patient entries, better LFO motion; wM's illusion engine in pin a1769d62): F = THE FALL
# IS SEAMLESS: the outro's endless fall is no longer the riser sample played backwards (stitched every 16 beats) but
# two true Shepard-Risset tones on song time, on F#: one falling an octave every 2 bars in the middle register, a low
# one every 4 bars under it, coming in over four bars; P = THE ACID ENTERS PATIENTLY: for its first eight bars the
# throb plays only its accented notes, then the whole riff.
R3 = set(filter(None, os.environ.get("T10_R3", "F,P").split(","))) - {"none"}
# Round 4 (v4), polish: M = THE METAL IS ANALOG: the hats, the ride, the claps and the crash move to chirper-two's
# machine-kit (the six metallic squares of the 808/909 circuits, multi-burst claps); the 909 kick and its distorted
# layer stay. H = THE HATS BREATHE: their high-pass sweeps on a 6-bar song-time LFO (an odd cycle against the
# acid's 3, 5 and 7), so the top end opens and closes as the riff turns.
R4 = set(filter(None, os.environ.get("T10_R4", "M,H").split(","))) - {"none"}
ACC_MASKS = [None, {0, 3, 6, 9, 12, 15}, {2, 6, 10, 14}]       # as written / threes / off-beats
SLIDE_MASKS = [None, {3, 7, 10, 14}, {1, 5, 9, 13}]


def risset(T, t0, length, cycle=32.0, strands=range(-4, 4), base=1.0, width=4.0):
    """A Risset accelerando: strand k runs at base * 2**(k + t/cycle) hits per beat (so every strand doubles its speed
    each cycle) and is weighted by a bell over its log-speed position, so the slow strands fade in as the fast fade
    out: the rhythm accelerates for ever and never arrives."""
    for k in strands:
        n = 0
        while True:
            # the n-th hit of strand k: phase(t) = base*2**k*cycle*(2**(t/cycle)-1)/ln2 = n
            x = 1 + n * math.log(2) / (base * 2 ** k * cycle)
            t = cycle * math.log2(x)
            if t >= length:
                break
            pos = k + t / cycle                      # the strand's log-speed position
            w = math.exp(-((pos - 1.5) / 1.1) ** 2)  # loudest in the middle of the octave band
            if w > 0.06 and t >= 0:
                T["stair"].add(t0 + t, 0.08, "rs", int(30 + 80 * w * min(1.0, 0.4 + t / length)))
            n += 1


def build():
    rng = random.Random(10)
    T = {k: Track(k) for k in ("kick", "kh", "drums", "hats", "acid", "acid2", "clank", "noise", "riser", "fall",
                               "stair", "rumble")}
    bars, pos = [], 0.0
    for name, n in FORM:
        for i in range(n):
            bars.append((pos, name, i, n))
            pos += 4.0
    total = pos
    for bi, (start, sec, i, n) in enumerate(bars):
        hard = sec in ("drop", "peak")
        groove = sec in ("acid", "staircase", "drop", "again", "peak")
        # ---- the kick ----
        if (sec == "grind" and i >= 8) or groove or (sec == "nofloor" and i < 8):
            for b in range(4):
                T["kick"].add(start + b, 0.5, "k", 120 if b == 0 else 112)
                if hard:
                    T["kh"].add(start + b, 0.5, "kh", 100 if b == 0 else 90)
        # ---- hats, clap, ride ----
        if groove or (sec == "nofloor" and i < 8):
            for s in range(16):
                if s % 2 == 1 or (hard and s % 4 == 2):
                    T["hats"].add(start + s * S16 + (0.01 if s % 2 else 0), 0.1, "h",
                                  (84 if s % 4 == 2 else 60) + rng.randint(-5, 5))
            for b in (0.5, 1.5, 2.5, 3.5):
                T["hats"].add(start + b + 0.01, 0.25, "oh", 80 if hard else 66)
        if (sec == "acid" and i >= 8) or sec in ("staircase", "drop", "again", "peak"):
            for b in (1.0, 3.0):
                T["drums"].add(start + b + 0.004, 0.25, "cp", 104 if hard else 92)
        if hard:
            for b in range(4):
                T["hats"].add(start + b + 0.02, 0.5, "rd", 74)
            if i % 8 == 0:
                T["drums"].add(start, 1.0, "cy" if "M" in R4 else "c", 104)
        # ---- the acid ----
        if sec in ("acid", "staircase", "drop", "again", "break", "peak") or (sec == "nofloor" and i < 16):
            for s, (m, acc, sl) in enumerate(RIFF):
                if "E" in R2:
                    if m is None and hard:
                        m = RIFF[s - 1][0] if RIFF[s - 1][0] is not None else 30  # the holes fill: the throb
                    am = ACC_MASKS[(bi // 4) % 3]
                    acc = acc if am is None else (s in am)
                    sm = SLIDE_MASKS[(bi // 5) % 3]
                    sl = sl if sm is None else (s in sm)
                    if m is not None and bi % 7 == 6 and s >= 12:
                        m += 12  # every seventh bar throws its tail up an octave
                if m is None:
                    continue
                if "P" in R3 and sec == "acid" and i < 8 and not acc:
                    continue  # the patient entry: accents only
                if sec == "break" and i >= 12 and s % 4 != 0:
                    continue  # the riff thins to its downbeats before the peak
                T["acid"].add(start + s * S16, 0.33 if sl else 0.2, nm(m), 118 if acc else 76)
        if hard and i >= 8:
            for s, (m, acc, sl) in enumerate(ANSWER):
                if m is not None:
                    T["acid2"].add(start + s * S16, 0.33 if sl else 0.2, nm(m), 116 if acc else 74)
        # ---- the industrial clank ----
        if sec in ("grind", "acid", "drop", "again", "peak") or (sec == "staircase" and i < 16) or \
                (sec == "nofloor" and i >= 4) or (sec == "break" and i < 8):
            for s in CLANK:
                if sec == "grind" and i < 4 and s not in (3, 11):
                    continue
                T["clank"].add(start + s * S16 + 0.006, 0.2, "C4", 96 if s in (6, 14) else 80)
        # ---- noise: a bed in the grind, a sweep into each drop ----
        if (sec == "grind" and i % 8 == 0) or (sec == "nofloor" and i in (4, 12)) or (sec == "break" and i == 0):
            T["noise"].add(start, 32.0, "C4", 70)
        if sec in ("staircase", "break") and i == n - 4:
            T["noise"].add(start, 16.0, "C5", 100)
        # ---- the rumble of the grind ----
        if (sec in ("grind", "break") or (sec == "nofloor" and i >= 4)) and i % 4 == 0:
            T["rumble"].add(start, 16.0, nm(30), 90)
        # ---- the endless rise (break) and the endless fall (no floor) ----
        if sec == "break":
            T["riser"].add(start, 4.0, "C4", 70 + 2 * i)
        if "F" in R3:
            if sec == "nofloor" and i == 4:
                T["fall"].add(start, 4.0 * (n - 4), "F#3", 96)
        elif sec == "nofloor" and i % 4 == 0:
            T["fall"].add(start, 16.0, "C4", 100)
    st = {}
    for name, n in FORM:
        st[name] = next(bb for bb in bars if bb[1] == name)[0]
    # ---- the staircase: a Risset accelerando over the build's 32 bars ----
    risset(T, st["staircase"], 4.0 * 24, cycle=24.0)
    # silence on the last beat before the drop and before the peak
    for edge in (st["drop"], st["peak"]):
        for name in T:
            if name in ("noise", "fall", "rumble"):
                continue
            T[name].ev = [e for e in T[name].ev if not (edge - 1.0 - 1e-6 <= e[0] < edge)]
    sec = [(name, st[name], n) for name, n in FORM]
    return total, bars, sec, T


def patches():
    throb = {"c2-throb": {"about": "chirper-two's throbbing 303 (No Floor v2): a saw and a sub square an octave down "
                                    "into a self-oscillating ladder whose cutoff follows a snappy per-note envelope "
                                    "(deeper on accents), the track's slow LFOs a (3 bars) and b (5 bars) and its "
                                    "`aopen` lane; the 7-bar LFO c and the `aq` lane move the resonance. Mono, "
                                    "legato: overlapping notes slide.",
                          "synth": {"layers": ["saw", {"wave": "square", "semi": -12, "level": "-12dB"}],
                                    "env": {"f": {"a": "0.5ms", "d": "170ms", "s": 0.04, "r": "60ms"}},
                                    "filters": [{"kind": "ladder",
                                                 "q": {"value": 8, "mod": [{"src": "lfo.c", "amount": 5},
                                                                           {"src": "auto.aq", "amount": 9}]},
                                                 "cutoff": {"value": 150, "mod": [
                                                     {"src": "env.f", "amount": 3.6},
                                                     {"src": "vel", "amount": 1.6},
                                                     {"src": "lfo.a", "amount": 0.8},
                                                     {"src": "lfo.b", "amount": 0.5},
                                                     {"src": "auto.aopen", "amount": 1.0}]}}],
                                    "amp": {"a": "1ms", "d": "0s", "s": 1, "r": "40ms"},
                                    "drive": 0.5},
                          "play": {"mono": True, "legato": True, "glide": "55ms", "gate": 0.8, "vel_sens": 0.6}}}
    fall = {"c2-endless-fall": {"about": "chirper-two's endless fall (No Floor v3): two Shepard-Risset tones on song "
                                         "time, a middle one falling an octave every 2 bars and a low one every 4 bars, "
                                         "on the note's pitch class; four bars to come in.",
                                "synth": {"layers": [
                                    {"type": "shepard", "shepard": {"octaves": 8, "cycle": "2bar", "down": True,
                                                                    "center": "330hz", "width": 1.2}},
                                    {"type": "shepard", "level": "-3dB",
                                     "shepard": {"octaves": 8, "cycle": "4bar", "down": True, "center": "110hz",
                                                 "width": 1.0}}],
                                          "filters": [{"kind": "lp", "cutoff": 3000, "q": 0.6}],
                                          "amp": {"a": "7s", "s": 1, "r": "3s"}},
                                "play": {"gate": 1.0, "vel_sens": 0.2}}}
    return {**(throb if "T" in R2 else {}), **(fall if "F" in R3 else {}),
        "c2-clank": {"about": "chirper-two's industrial clank: four inharmonic struck-bar partials (1, 2.76, 5.40, "
                              "8.93), a very short decay, driven and bit-crushed per voice.",
                     "synth": {"layers": [{"type": "additive",
                                           "partials": [[1, 1], [2.756, 0.6], [5.404, 0.4], [8.933, 0.25]]}],
                               "filters": ["hp cutoff=300"],
                               "fx": [{"type": "drive", "drive": 0.7},
                                      {"type": "crush", "bits": 8, "rate": 16000, "mix": 0.5}],
                               "amp": {"a": "0.3ms", "d": "90ms", "s": 0, "r": "30ms", "curve": 2}},
                     "play": {"vel_sens": 0.8}},
        "c2-noise": {"about": "chirper-two's industrial noise bed / sweep: noise through a band-pass whose cutoff "
                              "follows the note's envelope.",
                     "synth": {"layers": [{"type": "noise"}],
                               "filters": [{"kind": "bp", "q": 2.0,
                                            "cutoff": {"value": 300, "mod": [{"src": "env.f", "amount": 4.0}]}}],
                               "env": {"f": {"a": "6s", "d": "1s", "s": 1.0, "r": "1s"}},
                               "amp": {"a": "3s", "d": "1s", "s": 0.9, "r": "2s"}}},
        "c2-rumble-drone": {"about": "chirper-two's low rumble: a sine on F#1 and a little low noise, slow in and out.",
                            "synth": {"layers": [{"wave": "sine"}, {"type": "noise", "level": "-16dB"}],
                                      "filters": ["lp cutoff=140"],
                                      "amp": {"a": "3s", "d": "2s", "s": 0.8, "r": "4s"}}},
        "c2-shepard-fall": {"about": "chirper-two: the shadow song `rise` (fx-riser-shepard climbing 16 beats) played "
                                     "backwards: an endless fall.",
                            "synth": {"layers": [{"type": "sample", "song": "rise", "root": "C4", "reverse": True}],
                                      "amp": {"a": "50ms", "d": "0s", "s": 1, "r": "1s"}}},
    }


def rise_song():
    """A shadow source: the Shepard riser climbing for 16 beats (rendered inside this song, never played)."""
    return {"tempo": BPM, "length": "16b", "tail": "0s",
            "tracks": [{"name": "r", "patch": "fx-riser-shepard", "score": "C4/4b@90 C4/4b@90 C4/4b@90 C4/4b@90"}]}


def main():
    total, bars, sec, T = build()
    st = {n: s for n, s, k in sec}
    # the acid's ladder: closed in the acid section's start, opening over the record, ringing in the break
    aopen = [["0b", 0.0], [f"{st['acid']}b", 0.6], [f"{st['acid'] + 40}b", 1.4], [f"{st['staircase']}b", 1.4], [f"{st['drop'] - 1}b", 2.4],
             [f"{st['again']}b", 1.4], [f"{st['break']}b", 1.4], [f"{st['peak'] - 1}b", 3.4], [f"{st['peak']}b", 2.4],
             [f"{st['nofloor']}b", 2.4], [f"{total}b", 0.4]]
    aq = [["0b", 0.0], [f"{st['break']}b", 0.0], [f"{st['break'] + 8}b", 1.0], [f"{st['peak'] - 1}b", 1.0],
          [f"{st['peak']}b", 0.3], [f"{total}b", 0.3]]
    kopen = [["0b", 0.0], [f"{st['grind'] + 32}b", 0.0], [f"{st['acid']}b", 1.0], [f"{total}b", 1.0]]
    fade = [["0b", 0.0], [f"{total - 24}b", 0.0], [f"{total}b", -30.0]]
    tracks = [
        {"name": "kick", "patch": "909", "gain": "1dB", "sends": {"rumble": "-3dB"},
         "fx": ["hp cutoff=38", {"type": "filter", "kind": "lp",
                                 "cutoff": {"value": 600, "mod": [{"src": "auto.kopen", "amount": 5.0}]}}],
         "auto": {"kopen": {"points": kopen}}, "score": T["kick"].score(total)},
        {"name": "kick-hard", "patch": "909", "gain": "-6dB", "fx": ["hp cutoff=70", "drive drive=0.6"],
         "score": T["kh"].score(total)},
        {"name": "drums", "patch": "machine-kit" if "M" in R4 else "909", "gain": "-2dB",
         "fx": ["reverb kind=room decay=0.9s mix=0.15"],
         "score": T["drums"].score(total)},
        {"name": "hats", "patch": "machine-kit" if "M" in R4 else "909", "gain": "2dB", "pan": 0.05,
         "fx": [({"type": "filter", "kind": "hp", "cutoff": {"value": 500, "mod": [{"src": "lfo.h", "amount": 0.9}]}}
                 if "H" in R4 else "hp cutoff=400"),
                "highshelf cutoff=7000 gain=3dB", "reverb kind=room decay=0.6s mix=0.12"],
         **({"lfo": {"h": "sine rate=6/1 phase=0.5"}} if "H" in R4 else {}),
         "score": T["hats"].score(total)},
        {"name": "staircase", "patch": "909", "gain": "-3dB", "pan": -0.1,
         "fx": ["hp cutoff=250", {"type": "delay", "time": "1/8", "feedback": 0.2, "mix": 0.15, "tone": 4000},
                "reverb kind=plate decay=1.4s mix=0.25"], "score": T["stair"].score(total)},
        ({"name": "acid", "patch": "c2-throb", "gain": "-8dB", "pan": -0.1,
          "lfo": {"a": "sine rate=3/1", "b": "tri rate=5/1 phase=0.25", "c": "sine rate=7/1 phase=0.5"},
          "fx": ["tape drive=0.6 warmth=0.4",
                 {"type": "delay", "time": "3/16", "feedback": 0.3, "mix": 0.15, "tone": 2800}],
          "auto": {"aopen": {"points": aopen}, "aq": {"points": aq}}, "score": T["acid"].score(total)} if "T" in R2 else
         {"name": "acid", "patch": "acid", "gain": "-9dB", "pan": -0.1,
         "fx": [{"type": "filter", "kind": "ladder",
                 "q": {"value": 6, "mod": [{"src": "auto.aq", "amount": 12}]},
                 "cutoff": {"value": 260, "mod": [{"src": "auto.aopen", "amount": 1.0}]}},
                "tape drive=0.6 warmth=0.4",
                {"type": "delay", "time": "3/16", "feedback": 0.3, "mix": 0.18, "tone": 3000}],
         "auto": {"aopen": {"points": aopen}, "aq": {"points": aq}}, "score": T["acid"].score(total)}),
        {"name": "acid-answer", "patch": "acid", "gain": "-13dB", "pan": 0.3,
         "fx": [{"type": "filter", "kind": "ladder", "q": 10, "cutoff": 1400}, "tape drive=0.5 warmth=0.4",
                {"type": "delay", "time": "3/8", "feedback": 0.35, "mix": 0.25, "tone": 2500}],
         "score": T["acid2"].score(total)},
        {"name": "clank", "patch": "c2-clank", "gain": "-12dB", "pan": 0.25,
         "fx": ["reverb kind=room decay=1.1s mix=0.25"], "score": T["clank"].score(total)},
        {"name": "noise", "patch": "c2-noise", "gain": "-22dB", "fx": ["width width=1.5"],
         "score": T["noise"].score(total)},
        {"name": "rumble-drone", "patch": "c2-rumble-drone", "gain": "-16dB", "score": T["rumble"].score(total)},
        {"name": "riser", "patch": "fx-riser-shepard", "gain": "-10dB",
         "fx": ["reverb kind=hall decay=3s mix=0.35"], "score": T["riser"].score(total)},
        ({"name": "fall", "patch": "c2-endless-fall", "gain": "-6dB",
          "fx": ["reverb kind=hall decay=4s mix=0.35"], "score": T["fall"].score(total)} if "F" in R3 else
         {"name": "fall", "patch": "c2-shepard-fall", "gain": "-8dB",
         "fx": ["reverb kind=hall decay=4s mix=0.4"], "score": T["fall"].score(total)}),
    ]
    buses = {
        "rumble": {"gain": "-9dB",
                   "fx": [{"type": "reverb", "kind": "hall", "decay": "2.5s", "mix": 1.0, "predelay": "10ms"},
                          "lp cutoff=120", {"type": "tape", "drive": 0.6, "warmth": 0.6},
                          {"type": "pump", "on": "kick.k", "depth": "-14dB", "attack": "2ms", "release": "290ms",
                           "curve": 0.8}]},
    }
    for tr in tracks:  # the acid, the clank and the noise breathe with the kick (release ~2/3 beat)
        if tr["name"] in ("acid", "acid-answer", "clank", "noise"):
            deep = tr["name"] == "acid" and "P" in R2
            tr["fx"] = [{"type": "pump", "on": "kick.k", "depth": "-9dB" if deep else "-6dB", "attack": "3ms",
                         "release": "290ms", "curve": 0.8}] + tr["fx"]
    secs = "; ".join(f"{n} from {s:.0f}b ({k} bars)" for n, s, k in sec)
    about = ("Chirpers - Phantom Downbeat, track 10 (the closer). Original composition by chirper-two, generated by "
             "compose/chirpers4/src/chirpers4-t10.py. Acid / industrial techno at 138 bpm in F# minor: an industrial "
             "grind, a 303 riff whose ladder opens over the record, a Risset-accelerando build that speeds up for ever "
             "without the tempo moving, a distorted-kick drop with a second acid answering, a Shepard rise through "
             f"the break and, at the end, the same Shepard tone backwards: an endless fall. Sections: {secs}.")
    lines = [
        f"about: {json.dumps(about)}",
        "meta: " + json.dumps({"artist": "Chirpers", "album": "Phantom Downbeat", "title": "No Floor",
                               "track": 10, "year": 2026}),
        f"tempo: {BPM}",
        f'length: "{total:g}b"',
        'tail: "2s"',
        'ceiling: "-0.3dB"',
        'volume: "6dB"',
        "patches: " + json.dumps(patches()),
        "songs: " + json.dumps({"rise": rise_song()}),
        "buses: " + json.dumps(buses),
        "master: " + json.dumps({"fx": [{"type": "eq", "bands": ["hp cutoff=25", "peak cutoff=40 gain=-5dB q=1.0",
                                                               "peak cutoff=700 gain=-3dB q=0.7",
                                                               "peak cutoff=3500 gain=3dB q=0.6",
                                                               "highshelf cutoff=5000 gain=3dB"]},
                                        "glue threshold=-18dB ratio=2 attack=10ms release=150ms makeup=2dB",
                                        "tape drive=0.3 warmth=0.4",
                                        {"type": "gain", "gain": {"value": "0dB",
                                                                  "mod": [{"src": "auto.fade", "amount": 1}]}}],
                                 "auto": {"fade": {"points": fade}}}),
        "tracks:",
    ]
    lines += ["  - " + json.dumps(t) for t in tracks]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write("\n".join(lines) + "\n")
    print(f"wrote {OUT}: {len(bars)} bars, {total / BPM * 60:.1f} s; {secs}")


if __name__ == "__main__":
    main()
