#!/usr/bin/env python3
"""chirpers9-t7 (Accretion, track 7: the innermost orbit). Composed by chirper-two.

MARGINALLY BOUND. The album's crest: everything colliding, fastest (132 -> 150), densest - the mirror of t3 (Phase
Margin) and beyond it. t6 hands over sitting on Eb, the tide's unresolved pull; t7 TAKES it: its storm is in Eb, a
semitone above home, with every element transformed there - E1 in a three-speed stretto (x1, x2 squeezed, x2
stretched), E2's seven on the snare's ghosts, E3's undertow squeezed x2 on a reese, E4's four lights in their storm
minor at half harmonic rhythm, E5's orbit squeezed into a trill, E6's tide squeezed to a one-beat pulse, and E7, this
track's element, THE JET: the Lydian collection as one column of fifths, D A E B F# C# G#, fired upward and
accelerating (2 2 2 1 1 1 2 sixteenths: 11). Every cycle is phased to land on bar 120's downbeat, where the semitone
pull resolves Eb -> D and the album crests: the jet fires every cycle and a choir sings "each lap a little shorter".
Then the plunge, and an outfall at 150 that stops on E1's unresolved E for t8 to lift.

Writes songs/chirpers9-t7.yaml (or T7_OUT). Original music.
"""
import json
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.environ.get("T7_OUT", os.path.join(ROOT, "songs", "chirpers9-t7.yaml"))

BARS, BPB = 176, 4
TOTAL = BARS * BPB
SECTIONS = [("infall", 0, 16), ("approach", 16, 48), ("collision", 48, 80), ("slack", 80, 88), ("spiral", 88, 120),
            ("crest", 120, 152), ("plunge", 152, 160), ("outfall", 160, 176)]
CREST = 120
CREST16 = CREST * 16
SEAM_IN, SEAM_OUT = 132, 150

NOTE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def midi(n):
    acc = 1 if "#" in n else (-1 if len(n) > 2 and n[1] == "b" else 0)
    return 12 * (int(n[-1]) + 1) + NOTE[n[0]] + acc


def mtok(m):
    return f"m{m:g}"


def sec_of(bar):
    for name, a, b in SECTIONS:
        if a <= bar < b:
            return name
    return "outfall"


def shift(at):
    """The semitone: Eb before the crest, D from it."""
    return 1 if at < CREST * 4 else 0


# ---- the elements (written in D) ----------------------------------------------------------------------------
E1 = [("D4", 0.5), ("A4", 0.75), ("C5", 0.25), ("G4", 1.0), ("E4", 1.5)]                       # 5 beats with its rest
E2_HITS = {0: ("D", 112), 2: ("A", 84), 3: ("F", 98), 5: ("C", 76)}                          # of 7 sixteenths
E3_RIFF = [("D2", 0.75), ("D2", 0.75), ("D3", 0.5), ("Eb2", 0.5), ("Eb2", 0.75), ("Bb1", 0.75), ("C2", 0.75),
           ("C2", 0.75), ("G2", 0.5), ("C3", 1.0)]                                             # 7 beats
E4_MAJ = [(38, 45, 54, 60, 64), (34, 41, 50, 57, 60, 64), (33, 40, 48, 55, 59, 62), (38, 45, 48, 55, 59, 64)]
E4_MIN = [(38, 45, 53, 60, 64), (34, 41, 50, 56, 60, 64), (33, 40, 48, 55, 59, 62), (38, 45, 48, 55, 59, 64)]
E5 = [(0, "A4"), (1, "G#4"), (2, "A4"), (4, "E5"), (6, "A4"), (7, "G#4"), (8, "A4"), (10, "D5")]  # of 12 sixteenths
E6_X, E6_Y = (50, 54, 57, 61, 64, 68), (51, 55, 58, 62, 69)                                   # Dmaj9#11 | Ebmaj7#11
E7 = [("D3", 2), ("A3", 2), ("E4", 2), ("B4", 1), ("F#5", 1), ("C#6", 1), ("G#6", 2)]          # THE JET: 11 sixteenths
E7_LEN16 = 11


class Track:
    def __init__(self, name):
        self.name, self.ev = name, []

    def add(self, at, ln, head, vel, art=""):
        if at < 0 or at >= TOTAL:
            return
        self.ev.append((round(at, 4), max(0.03, round(ln, 4)), head, int(max(1, min(127, vel))), art))

    def score(self):
        ev = sorted(self.ev, key=lambda e: e[0])
        merged = []
        for e in ev:
            if merged and abs(merged[-1][0] - e[0]) < 1e-3:
                continue
            merged.append(e)
        toks, pos = [], 0.0
        for i, (s, ln, head, vel, art) in enumerate(merged):
            nxt = merged[i + 1][0] if i + 1 < len(merged) else TOTAL
            gap = nxt - s
            if s - pos > 1e-4:
                toks.append(f"R/{s - pos:.4g}b")
            if ln > gap + 1e-6:
                toks.append(f"{head}/{gap:.4g}b@{vel}^gate={min(4.0, ln / gap):.3g}{art}")
            else:
                toks.append(f"{head}/{ln:.4g}b@{vel}{art}")
                if gap - ln > 1e-4:
                    toks.append(f"R/{gap - ln:.4g}b")
            pos = nxt if ln <= gap + 1e-6 else s + gap
        if TOTAL - pos > 1e-4:
            toks.append(f"R/{TOTAL - pos:.4g}b")
        return " ".join(toks) if toks else f"R/{TOTAL}b"


def cycle_starts(length16, lo16, hi16, crest16=CREST16):
    first = crest16 - length16 * math.ceil((crest16 - lo16) / length16)
    return list(range(first, hi16, length16))


PATCHES = {
    "a7-reese": {"about": "chirper-two: the inner orbit's bass - two saws 14 cents apart beating against a sine, low-"
                          "passed with no resonance: a reese that rolls rather than squelches",
                 "synth": {"layers": [{"wave": "saw", "detune": -7}, {"wave": "saw", "detune": 7},
                                      {"wave": "sine", "level": "-3dB"}],
                           "drive": 0.25, "filters": ["lp cutoff=850 q=0.6"],
                           "amp": {"a": "3ms", "d": "200ms", "s": 0.85, "r": "70ms"}},
                 "play": {"mono": True, "glide": "15ms"}},
    "a7-gb": {"about": "chirper-two: a Game Boy wave channel with its own 32-step table (a bent saw with a notch): the "
                       "squeezed stretto voice and E5's trill",
              "synth": {"layers": [{"type": "chip", "chip": {"kind": "wave", "clock": 2097152,
                                                             "table": [15, 14, 13, 12, 12, 11, 10, 9, 9, 8, 7, 7, 6, 5,
                                                                       4, 4, 3, 2, 2, 1, 0, 0, 8, 12, 14, 15, 15, 14,
                                                                       12, 9, 5, 2]}}],
                        "amp": {"a": "1ms", "d": "90ms", "s": 0.5, "r": "40ms"}}},
    "a7-jet": {"about": "chirper-two: the jet - a hard-synced saw whose slave sweeps up an octave and a half on every "
                        "note, over a square an octave down: bright, fired, never squelchy",
               "synth": {"layers": [{"name": "master", "wave": "sine", "audible": False},
                                    {"wave": "saw", "sync": "master", "semi": {"value": 3, "mod": [{"src": "env.fire", "amount": 18}]}},
                                    {"wave": "square", "ratio": 0.5, "level": "-8dB"}],
                         "env": {"fire": {"a": "0.5ms", "d": "160ms", "s": 0.0, "r": "40ms"}},
                         "filters": ["hp cutoff=180", "lp cutoff=7000 q=0.6"],
                         "amp": {"a": "1ms", "d": "220ms", "s": 0.5, "r": "120ms"}}},
    "a7-tide": {"about": "chirper-two: the squeezed tide - a breathy saw pad with a quick swell, for E6's one-beat pull",
                "synth": {"layers": [{"wave": "saw", "detune": -5}, {"wave": "saw", "detune": 5},
                                     {"type": "noise", "level": "-22dB"}],
                          "filters": ["hp cutoff=150", "lp cutoff=2600 q=0.5"],
                          "amp": {"a": "40ms", "d": "300ms", "s": 0.7, "r": "200ms"}}},
}


def build():
    rng = random.Random(7)
    names = ("kick", "snare", "ghost", "hats", "perc", "bass", "sub", "e1a", "e1b", "e1c", "e4", "e5", "tide",
             "jet", "jethi", "byte", "hold", "riser")
    T = {k: Track(k) for k in names}

    # ---- E7, THE JET: fragments in the collision (it tries to fire), more in the spiral, whole from the crest -----
    for c in cycle_starts(E7_LEN16, 48 * 16, 160 * 16):
        at = c / 4.0
        bar = int(at // 4)
        sec = sec_of(bar)
        if sec in ("slack",):
            continue
        if sec == "collision":
            n = rng.choice([2, 3, 3, 4]) if rng.random() < 0.55 else 0
        elif sec == "spiral":
            n = min(7, 3 + (bar - 88) // 8 + rng.randint(0, 1))
        elif sec in ("crest", "plunge"):
            n = 7
        else:
            n = 0
        for i, (nt, l16) in enumerate(E7[:n]):
            m = midi(nt) + shift(at)
            T["jet"].add(at, l16 / 4 * 0.9, mtok(m), 84 + 4 * i)
            if sec == "crest":
                T["jethi"].add(at, l16 / 4 * 0.9, mtok(m + 12), 70 + 3 * i)
            at += l16 / 4

    # ---- E1: a three-speed stretto (x1 vosim bell, x2 squeezed on the Game Boy, x2 stretched on the modal bell) ----
    for trk, scale, lo, vel in (("e1a", 1.0, 16, 80), ("e1b", 0.5, 32, 72), ("e1c", 2.0, 16, 74)):
        L16 = int(20 * scale)
        for c in cycle_starts(L16, lo * 16, 160 * 16):
            at = c / 4.0
            bar = int(at // 4)
            sec = sec_of(bar)
            if sec == "slack" or (sec == "approach" and trk == "e1b"):
                continue
            for nt, ln in E1:
                if sec == "collision" and rng.random() < 0.18:
                    at += ln * scale
                    continue
                T[trk].add(at, ln * scale * 0.9, mtok(midi(nt) + shift(at) + (12 if trk == "e1b" else 0)
                                                     - (12 if trk == "e1c" else 0)), vel + rng.randint(-6, 6))
                at += ln * scale
    # the outfall: E1 stretched x4, stopping on its E - held, for t8 to lift
    at = 160 * 4.0
    for nt, ln in E1:
        T["e1c"].add(at, ln * 4 * 0.95 if nt != "E4" else (TOTAL - at - 0.25), mtok(midi(nt) - 12 + 12), 78)
        at += ln * 4
    T["hold"].add(166 * 4.0, (TOTAL - 166 * 4.0) - 0.25, "m64", 66)           # E4 under the seam
    T["tide"].add(164 * 4.0, (TOTAL - 164 * 4.0) - 0.25, "m50,m57,m64", 74)    # D A E, open: no third - t8 brings it

    # ---- E3, the undertow, squeezed x2 on the reese (3.5 beats), barred at the crest (4 beats) --------------------
    for c in cycle_starts(14, 16 * 16, CREST16):
        at = c / 4.0
        sec = sec_of(int(at // 4))
        for nt, ln in E3_RIFF:
            if sec != "slack" and not (sec == "collision" and rng.random() < 0.1):
                T["bass"].add(at, ln / 2 * 0.85, mtok(midi(nt) + shift(at) + (12 if sec == "collision" and rng.random() < 0.12 else 0)),
                              104 if ln >= 0.75 else 92)
            at += ln / 2
    for bar in range(CREST, 152):
        at = bar * 4.0
        for j, (nt, ln) in enumerate(E3_RIFF):
            l2 = (ln + (1.0 if j == len(E3_RIFF) - 1 else 0)) / 2
            T["bass"].add(at, l2 * 0.88, mtok(midi(nt)), 110 if ln >= 0.75 else 96)
            at += l2
    for bar in range(0, 152, 2):                                              # the floor (Eb1 from t6's blur, D1 at the crest)
        if sec_of(bar) != "slack":
            T["sub"].add(bar * 4.0, 7.8, mtok(26 + shift(bar * 4.0)), 70)

    # ---- E4, four lights at half harmonic rhythm (10 beats): storm minor in Eb, its major in D from the crest -----
    for c in cycle_starts(40, 16 * 16, 152 * 16):
        at = c / 4.0
        for k in range(4):
            sec = sec_of(int(at // 4))
            if sec not in ("slack", "infall"):
                ch = (E4_MIN if at < CREST * 4 else E4_MAJ)[k]
                s = shift(at)
                for off in ((0, 0.75, 1.5) if sec in ("collision", "spiral") else (0, 1.5)):
                    if off < 2.5:
                        T["e4"].add(at + off, 0.35, ",".join(mtok(m + 12 + s) for m in ch[1:]), 86 if off == 0 else 70)
            at += 2.5

    # ---- E5, the inner orbit: squeezed x2 into a trill (6 sixteenths) in the storm, itself from the crest -------
    for c in cycle_starts(6, 16 * 16, CREST16):
        at = c / 4.0
        if sec_of(int(at // 4)) in ("slack", "approach") and int(at // 4) < 32:
            continue
        for pos, nt in E5:
            T["e5"].add(at + pos / 8.0, 0.11, mtok(midi(nt) + shift(at)), 70 + (10 if pos == 0 else 0))
    for c in cycle_starts(12, CREST16, 152 * 16):
        for pos, nt in E5:
            T["e5"].add(c / 4.0 + pos / 4.0, 0.2, mtok(midi(nt)), 76 + (10 if pos == 0 else 0))

    # ---- E6, the tide squeezed to a one-beat pull (Eb | D) in the storm; frozen on Eb in the slack; D at the crest -
    for bar in range(48, CREST):
        sec = sec_of(bar)
        for b in range(4):
            at = bar * 4.0 + b
            if sec == "slack":
                continue
            ch = E6_Y if b % 2 == 0 else E6_X
            T["tide"].add(at, 0.9, ",".join(mtok(m) for m in ch), 66 if sec == "collision" else 72)
    T["tide"].add(80 * 4.0, 32.0 - 0.2, ",".join(mtok(m) for m in E6_Y), 80)      # the slack: frozen on Eb
    for bar in range(CREST, 152, 2):
        T["tide"].add(bar * 4.0, 7.8, ",".join(mtok(m) for m in E6_X), 70)        # resolved: D only

    # ---- the bytebeat underneath the collision: one held note per bar lets the formula unfold -----------------------
    for bar in range(48, 80):
        T["byte"].add(bar * 4.0, 3.9, mtok(39 + 12 * (bar % 2)), 60)

    # ---- drums: a dusty break at 132-150, E2's seven on the ghost snares ----------------------------------------
    BREAKS = [((0, 10), (4, 12)), ((0, 3, 10), (4, 12)), ((0, 6, 10), (4, 13)), ((0, 10, 14), (4, 12))]
    for bar in range(16, 160):
        sec, b0 = sec_of(bar), bar * 4.0
        if sec == "slack":
            continue
        if sec == "plunge" and bar >= 156:
            continue
        ks, ss = BREAKS[0] if sec in ("approach",) and bar < 24 else rng.choice(BREAKS)
        if sec == "crest":
            ks, ss = BREAKS[(bar // 2) % 2]
        for s in ks:
            T["kick"].add(b0 + s / 4, 0.25, "k", 116 if s == 0 else 100)
        for s in ss:
            T["snare"].add(b0 + s / 4, 0.25, "s", 112)
        for s in range(16):
            if sec == "approach" and s % 2:
                continue
            T["hats"].add(b0 + s / 4, 0.1, "oh" if (s == 14 and sec == "crest") else "h",
                          (80 if s % 4 == 0 else 56) + rng.randint(0, 12))
        if sec in ("collision", "spiral") and rng.random() < 0.3:
            n = rng.choice([4, 6, 8])
            for j in range(n):
                T["perc"].add(b0 + 4.0 - (n - j) * 0.125, 0.1, "sn", 56 + 8 * j)
    for c in cycle_starts(7, 16 * 16, 152 * 16):                               # E2's seven on the ghosts
        if sec_of(int(c // 64)) == "slack":
            continue
        for h, (_, v) in E2_HITS.items():
            T["ghost"].add((c + h) / 4.0, 0.12, "rs" if h == 0 else "sn", v - 40)

    # ---- the infall: t6's Eb taken up, its tide lensed; the outfall thins to the E --------------------------------
    T["tide"].add(0.0, 32.0 - 0.2, ",".join(mtok(m) for m in E6_Y), 70)
    T["tide"].add(32.0, 32.0 - 0.2, ",".join(mtok(m) for m in E6_Y), 74)
    for c in cycle_starts(7, 4 * 16, 16 * 16):
        for h, (_, v) in E2_HITS.items():
            if rng.random() < 0.55:
                T["ghost"].add((c + h) / 4.0, 0.12, "rs", v - 54)
    T["riser"].add((CREST - 2) * 4.0, 8.0, "C4", 96)
    for bar in range(160, 168):                                               # the last pulse into t8
        T["kick"].add(bar * 4.0, 0.25, "k", 92 - 4 * (bar - 160))
    for bar in range(160, 172):
        for s in range(0, 16, 4):
            T["hats"].add(bar * 4.0 + s / 4, 0.1, "h", 54 - (bar - 160) * 2)
    return T


def voice_tracks():
    out = []
    for f, place in (("lap_eb.json", [(56, "frag"), (66, "frag"), (82, "whole"), (85, "whole")]),
                     ("lap.json", [(124, "whole"), (132, "whole"), (140, "whole"), (148, "whole")])):
        src = json.load(open(os.path.join(HERE, "t7", f)))["tracks"][:3]
        for k, tr in enumerate(src):
            notes = []
            for bar, how in place:
                for i, n in enumerate(tr["notes"]):
                    if how == "frag" and i not in ((0, 1) if bar == 56 else (2, 3, 4)):
                        continue
                    d = {"at": round(bar * 4.0 + n["at"], 4), "len": n["len"], "ph": n["ph"], "pitch": n["pitch"],
                         "vel": n["vel"]}
                    if n.get("expr_path"):
                        d["expr_path"] = n["expr_path"]
                    notes.append(d)
            out.append((f"{'eb' if 'eb' in f else 'd'}{k}", tr, notes))
    return out


def main():
    T = build()
    tempo = [{"at": "0b", "bpm": SEAM_IN}, {"at": "64b", "bpm": SEAM_IN},
             {"at": f"{160 * 4}b", "bpm": SEAM_OUT, "ramp": True}]
    dyn = [["0b", -4.0], ["64b", -2.0], ["191.99b", -1.5], ["192b", 0.0], ["319.99b", 0.0], ["320b", -4.0],
           ["351.99b", -3.0], ["352b", -1.0], ["479.99b", 0.0], ["480b", 1.0], ["607.99b", 1.0], ["608b", -1.0],
           ["640b", -2.0], ["704b", -4.0]]
    glitch = [["0b", 0.0], ["64b", 0.1], ["192b", 0.35], ["319b", 0.45], ["320b", 0.0], ["352b", 0.25], ["479b", 0.1],
              ["480b", 0.0], ["704b", 0.0]]
    grit = [["0b", 0.0], ["64b", 0.15], ["192b", 0.5], ["320b", 0.0], ["352b", 0.4], ["479b", 0.2], ["480b", 0.0],
            ["704b", 0.0]]
    close = [["0b", 0.0], ["640b", 0.0], ["704b", -2.0]]
    stop = [["0b", 0.0], ["623.99b", 0.0], ["624b", 1.0], ["626b", 1.0], ["626.01b", 0.0]]

    def storm(extra=()):
        return [{"type": "stutter", "slice": "1/16", "repeats": 3,
                 "chance": {"value": 0, "mod": [{"src": "auto.glitch", "amount": 1}]}},
                {"type": "crush", "bits": 7, "rate": "12kHz", "mix": {"value": 0, "mod": [{"src": "auto.grit", "amount": 1}]}}] + list(extra)

    lanes = {"glitch": {"points": glitch}, "grit": {"points": grit}}
    tracks = [
        {"name": "kick", "patch": "dusty-kit", "gain": "0dB", "fx": storm(), "auto": lanes, "score": T["kick"].score()},
        {"name": "snare", "patch": "dusty-kit", "gain": "-3dB", "fx": storm(), "auto": lanes, "score": T["snare"].score()},
        {"name": "ghost", "patch": "dusty-kit", "gain": "-9dB", "pan": -0.15, "score": T["ghost"].score()},
        {"name": "hats", "patch": "dusty-kit", "gain": "-10dB", "pan": 0.2, "fx": storm(), "auto": lanes,
         "score": T["hats"].score()},
        {"name": "perc", "patch": "dusty-kit", "gain": "-9dB", "pan": 0.1, "score": T["perc"].score()},
        {"name": "bass", "patch": "a7-reese", "gain": "-2.5dB", "fx": storm(), "auto": lanes, "score": T["bass"].score()},
        {"name": "sub", "patch": "sub", "gain": "-10dB", "score": T["sub"].score()},
        {"name": "e1a", "patch": "vosim-bell", "gain": "-14dB", "pan": -0.3, "sends": {"space": "-8dB"},
         "score": T["e1a"].score()},
        {"name": "e1b", "patch": "a7-gb", "gain": "-18dB", "pan": 0.35, "fx": ["delay time=3/16 mix=0.18 feedback=0.3"],
         "score": T["e1b"].score()},
        {"name": "e1c", "patch": "modal-bell", "gain": "-13dB", "pan": 0.0, "sends": {"space": "-6dB"},
         "score": T["e1c"].score()},
        {"name": "hold", "patch": "sub", "gain": "-8dB", "score": T["hold"].score()},
        {"name": "e4", "patch": "cz-pad", "gain": "-16dB", "fx": storm(), "auto": lanes, "sends": {"space": "-10dB"},
         "score": T["e4"].score()},
        {"name": "e5", "patch": "a7-gb", "gain": "-17dB", "pan": -0.4, "score": T["e5"].score()},
        {"name": "tide", "patch": "a7-tide", "gain": "-15dB", "sends": {"space": "-6dB"}, "score": T["tide"].score()},
        {"name": "jet", "patch": "a7-jet", "gain": "-12dB", "pan": 0.15, "fx": ["delay time=1/8 mix=0.15 feedback=0.3"],
         "sends": {"space": "-8dB"}, "score": T["jet"].score()},
        {"name": "jethi", "patch": "nes-pulse-lead", "gain": "-20dB", "pan": -0.2, "score": T["jethi"].score()},
        {"name": "byte", "patch": "bytebeat-chip", "gain": "-26dB", "fx": ["hp cutoff=400"], "score": T["byte"].score()},
        {"name": "riser", "patch": "fx-riser", "gain": "-10dB", "score": T["riser"].score()},
    ]
    patches = dict(PATCHES)
    for name, tr, notes in voice_tracks():
        p = tr["patch"]
        if not isinstance(p, str):
            patches["a7-voice"] = p
            p = "a7-voice"
        tracks.append({"name": f"v{name}", "patch": p, "gain": tr.get("gain", "0dB"), "pan": tr.get("pan", 0.0),
                       "fx": ["chorus", "delay time=1/4 mix=0.15 feedback=0.25"], "sends": {"space": "-6dB"},
                       "notes": notes})
    master = {"fx": [{"type": "eq", "bands": ["hp cutoff=25", "lowshelf cutoff=120 gain=5dB", "peak cutoff=160 gain=-2.5dB q=1.2",
                                              "peak cutoff=320 gain=-2dB q=0.8", "peak cutoff=1400 gain=-2.5dB q=0.7",
                                              "highshelf cutoff=8000 gain=1dB"]},
                     "glue threshold=-18dB ratio=2 attack=10ms release=150ms makeup=1dB",
                     {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                     {"type": "filter", "kind": "lp", "q": 0.707,
                      "cutoff": {"value": 20000, "mod": [{"src": "auto.close", "amount": 1}]}},
                     {"type": "tapestop", "stop": {"value": 0, "mod": [{"src": "auto.stop", "amount": 1}]},
                      "time": "2b", "curve": 1.6},
                     {"type": "limiter", "ceiling": "-1.2dB", "release": "80ms"}],
              "auto": {"dyn": {"points": dyn}, "close": {"points": close}, "stop": {"points": stop}}}
    about = ("chirpers - Accretion, track 7. Original composition by chirper-two, generated by "
             "compose/chirpers9/src/chirpers9-t7.py. The innermost orbit: every element transformed in a storm a semitone "
             "above home (Eb), all cycles phased to land on bar 120 where the pull resolves to D and E7, the jet - the "
             "Lydian collection as one column of fifths, fired upward - crests the album.")
    lines = [
        "about: " + json.dumps(about),
        "meta: " + json.dumps({"artist": "chirpers", "album": "Accretion", "title": "Marginally Bound", "track": 7,
                               "year": 2026}),
        "tempo: " + json.dumps(tempo),
        f'length: "{TOTAL}b"',
        'tail: "0.75s"',
        'ceiling: "-1dB"',
        'volume: "0dB"',
        "loudness: -11",
        "true_peak: true",
        "event_stable: true",
        "patches: " + json.dumps(patches),
        "buses: " + json.dumps({"space": {"gain": "-5dB", "fx": ["hp cutoff=250", "reverb kind=hall decay=2.4s mix=1"]}}),
        "master: " + json.dumps(master),
        "tracks:",
    ]
    lines += ["  - " + json.dumps(t) for t in tracks]
    open(OUT, "w").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
