#!/usr/bin/env python3
"""chirpers8-t9 (chirpers VIII, track 9). Composed by chirper-two: POLYTEMPO BRAINDANCE in BOHLEN-PIERCE.

"Period Doubling". A clock that learns to drift. One number drives everything: the LOGISTIC MAP, x <- r x (1 - x),
iterated once per sixteenth. As r climbs through the track the music walks the famous road into chaos:
- ONE (r 2.9): the map settles on a single value after a damped wobble - one note, sixteenths, a sequencer pulse.
- TWO (r 3.2, 7/8): the first doubling - two notes alternate.  FOUR (r 3.5): four, and a rest appears in the cycle.
- EIGHT (r 3.56, 5/4): eight.  CHAOS (r 3.7 -> 3.82, the tempo ramping 140 -> 150): no cycle at all.
- WINDOW (r 3.835, 4/4): inside chaos, order returns for a moment: PERIOD THREE - a cycle of three sixteenths that
  runs across the beat, a cross-rhythm made by arithmetic.
- STORM (r 4.0, 11/8 at 154): full chaos.  SETTLE (r 3.4 -> 2.9, slowing to 132): back down to one note.
- THE TUNING is BOHLEN-PIERCE: 13 equal steps to the TRITAVE (3:1) instead of the octave, in its Lambda mode
  (degrees 0 2 3 4 6 7 9 10 12); no octaves anywhere. Its natural voice is the clarinet (odd harmonics only), so the
  lead is chirp's PHYSICAL REED (a reed on a cylindrical bore); chords are BP's 3:5:7 triad on a glass pad.
- POLYTEMPO: the lead runs on sixteenths, glitch blips on a 5:4 grid (the map's twin, y) and the folded-sine bass on a
  3:4 grid, so three clocks run at once and only meet at bar lines.
- METER CHANGES (4/4, 7/8, 5/4, 11/8) and TEMPO RAMPS in the tempo map; drums whose accents, ratchets and stutters
  the map decides; a fold shaper on the bass, a stutter on the drum bus whose chance rises with chaos.
140 bpm base, Bohlen-Pierce on A. Form: one 20 / two 16 / four 20 / eight 20 / chaos 32 / window 18 / storm 24 /
settle 28 bars.

Emits songs/chirpers8-t9.yaml. Edit the music here.
"""
import json
import math
import os
import random

OUT = os.environ.get("T9_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers8-t9.yaml")
BP = 12 * math.log2(3) / 13              # one Bohlen-Pierce step in semitones (146.3 cents)
TRITAVE = 12 * math.log2(3)
LAMBDA = [0, 2, 3, 4, 6, 7, 9, 10, 12]   # the Lambda mode, 9 notes a tritave
# (name, bars, meter, r from, r to, bpm at start, ramp to next?)
SECS = [("one", 20, (4, 4), 2.9, 2.9), ("two", 16, (7, 8), 3.2, 3.2), ("four", 20, (4, 4), 3.5, 3.5),
        ("eight", 20, (5, 4), 3.56, 3.56), ("chaos", 32, (4, 4), 3.7, 3.82), ("window", 18, (4, 4), 3.835, 3.835),
        ("storm", 24, (11, 8), 3.95, 4.0), ("settle", 28, (4, 4), 3.4, 2.9)]
BPM = {"one": 140, "two": 140, "four": 140, "eight": 140, "chaos": 140, "window": 150, "storm": 154, "settle": 154}
# T9_R2 = drift (v2, wM's tunings, systems and morph). THE CLOCK DRIFTS OUT OF TUNE AND BACK: the song's `tuning` is
# 12-TET while the map holds one and two notes (the Bohlen-Pierce lines snap to their nearest semitones: a plain
# sequencer), ramps into exact Bohlen-Pierce across the period-four section, stays alien through eight, chaos, the
# window and the storm, and ramps back to 12-TET as it settles. In the chaos and the storm a second glass pad plays the
# 3:5:7 chords CROSS-SYNTHESISED with the drum bus (`morph` mode cross keyed by `drums`), so the chords breathe in the
# chaotic rhythm. A second logistic map, at r 3.95 as a song `var`, throws the reed around the stereo field.
# T9_R2=none reproduces v1.
R2 = os.environ.get("T9_R2", "drift")
# T9_R3 = sing (v3, wM's singing voice): in the period-three window a human voice SINGS "it comes back in threes"
# (`chirp tts --sing "A3/8 C4 E4" --repeat 3`, src/t9/sing.json): five syllables on a three-note tune, so the words
# land on different notes each time round while the map cycles in threes under them; its notes snap to the song's
# Bohlen-Pierce. Once more as the map settles, by then back in 12-TET: the same words, a different tuning.
# T9_R3=none reproduces v2.
R3 = os.environ.get("T9_R3", "sing")
# T9_R4 = break (v4, palette round). Out of the album's staples: the kit leaves machine-kit (on nine songs) for the
# BREAK-KIT, a squashed 1969 funk kit as a sampler hears it, and in chaos and storm the map CHOPS THE BREAK - each
# sixteenth's iterate picks a piece (ghost, edit snare, open hat) the way a jungle producer slices the Amen, on its
# own track into the drums bus (so the stutter and the glass pad's cross-synthesis hear it too). The blips leave the
# library `blip` (four songs) for c9-pulse, a one-bit loudspeaker voice: a very narrow pulse train, crushed - the
# sound of a machine driving its speaker directly, the oldest computer music there is, said sideways.
# T9_R4=none reproduces v3.
R4 = os.environ.get("T9_R4", "break")
KIT = "break-kit" if R4 == "break" else "machine-kit"
# T9_R5 = orbit (v5, section round on w5, 1:49-2:17, the period-eight section's second half: "static, little new" and
# the song's dynamic range only 5.3 dB). THE ATTRACTOR AS A CHORD: the drums fall away and a wordless choir (the
# library's classic formant choir, new to the album) holds all eight points of the period-eight orbit at once, each
# at its exact Bohlen-Pierce pitch (Hz, so no tuning snaps them): the orbit's four close pairs - the branches of the
# bifurcation diagram that have only just split - sit ~60 cents apart and BEAT against each other. You hear period
# doubling as pitches splitting. The drums come back through a ratcheted break fill. New tracks only (orbit, fill)
# and lanes local to the window. T9_R5=none reproduces v4.
R5 = os.environ.get("T9_R5", "orbit")
# T9_R6 = steel (v6, palette round). The song had no sustained, singing line: reed, blips and pulses are all
# staccato. Now, as the map SETTLES (r 3.4 -> 2.9), a PEDAL STEEL (new to the album) plays the period-two orbit
# itself: its two points as two long notes a bar, gliding one into the other (the steel's swell and slide), their
# interval narrowing bar by bar as r falls, until at r = 3 - the bifurcation point - they meet in one note, the
# fixed point 1 - 1/r, which it holds to the end. The bifurcation diagram heard backwards, as a tune that closes.
# Exact Bohlen-Pierce pitches (Hz, the map's own mapping), so no tuning snaps them. And the album-staple bell (three
# songs) that marks each section becomes a HANDPAN. T9_R6=none reproduces v5.
R6 = os.environ.get("T9_R6", "steel")
# T9_R7 = lpg (v7, palette round). AS KEPT: the bass's sub-sine body stays (replacing it outright, and the dizi below,
# both broke the sections' returns: recurrence 100 -> 56-85), and c9-lpg joins as the bass's VOICE, an octave over
# it (T9_R7_BASS=layer; =lpg swaps the bass whole; T9_R7_DIZI=1 adds the flute). The design: c9-lpg, a patch of my own
# after the West Coast: a triangle and its octave, folded, through a LOW-PASS GATE (one envelope opens the filter and
# the amp together, then lets both fall: the "bongo" pluck of the first voltage-controlled music), so the 3:4 bass
# speaks each note instead of humming under the floor. And in the early, static windows (w2 and w4: the two and four
# sections), a DIZI - the bamboo flute with the buzzing membrane, new to the album - doubles the reed's accents (its
# loudest iterates) an octave up, which in Bohlen-Pierce lands on the scale's nearest step to an octave: 1170 cents,
# a slightly closed octave, the song's tuning pulling the flute in. The flute comes back as the map settles, so the
# record's two calm ends share a colour. T9_R7=none reproduces v6.
R7 = os.environ.get("T9_R7", "lpg")
# T9_R8 = ostinato (v8, section round on w4, 1:22-1:49: "static, little new vs w3" - the end of period four and the
# start of period eight). THE ORBIT AS A TUNE: a STEEL PAN (new to the album) plays the attractor's own orbit as an
# ostinato in eighths - the four points of period four, round and round, growing louder - and at the bifurcation
# (bar 1 of the 5/4 section) the tune DOUBLES to the eight points of period eight, an eight-note figure turning
# against the ten eighths of each 5/4 bar, so it lands differently every bar. At 256b it stops, exactly where the
# choir freezes the same eight points into a chord. Exact Bohlen-Pierce Hz, the map's own mapping. New track only.
# T9_R8=none reproduces v7.
R8 = os.environ.get("T9_R8", "ostinato")


def logistic_orbit(r, p, n=4000):
    x = 0.5
    for _ in range(n):
        x = r * x * (1 - x)
    out = []
    for _ in range(p):
        x = r * x * (1 - x)
        out.append(x)
    return out


# T9_R9 = return (v9, section round on w2, 0:27-0:54: "static" - the end of `one` and most of `two`). IT COMES BACK:
# a KOTO (new to the album) knocks the map off its attractor and lets it return, one iterate per eighth. At the end
# of `one` (r = 2.9, where the fixed point is about to lose its footing: multiplier -0.9) the knocked value spirals
# home slowly, high-low-high, narrowing - the period-two alternation heard coming before it arrives. In `two` every
# other 7/8 bar is a knock and a return in seven eighths (seven iterates), each knock a different size and side, so
# the lick recurs but never repeats. Under it a TABLA (new to the album) plays a 3+2+2 cycle in the 7/8, a te-re fill
# every fourth bar. New tracks only. (T9_KNOCK=every, a knock in every bar: w2 motion 0.032 -> 0.038, still
# "static", s0 -0.04; opt-in.) T9_R9=none reproduces v8.
R9 = os.environ.get("T9_R9", "return")
KNOCKS = [0.22, -0.18, 0.3, -0.25, 0.12, -0.3, 0.26, -0.1]
TABLA = [["tin", "tin", "na", "dhin", "na", "dhin", "na"],
         ["dha", "tin", "na", "dhin", "na", "dhin", "na"],
         ["tin", "tin", "na", "dhin", "na", "ge", "na"],
         ["dha", "te", "re", "dhin", "na", "dhin", "dha"]]


def lmap(r, x, n):
    out = []
    for _ in range(n):
        x = r * x * (1 - x)
        out.append(x)
    return out


# T9_R10 = bpclar (v10, palette round). The lead leaves the library clarinet (three album songs) for c9-bpclar, this
# song's own BOHLEN-PIERCE CLARINET: Bohlen-Pierce is the clarinet's scale (a cylindrical bore sounds odd harmonics,
# and BP repeats at the 3:1 tritave, not the octave), so this reed is pushed harder and brighter, a little airier, and
# carries a quiet sine at exactly 3:1 - the third harmonic, the tritave, sung on top of every note. In the calm
# sections (the period-3 window, the settle) it plays SUBTONE: breathy, dark, close. Pushed bright (press 0.52, bright
# 0.5, lp 4.5k) it cost spectrum (s0 96.75); the darker reed (0.46/0.38/3.6k) sits at parity. T9_SUB=none|settle
# and the T9_BPC_* knobs stay. T9_R10=none reproduces v9.
R10 = os.environ.get("T9_R10", "bpclar")
# T9_R11 = d (v11, whole-song round). D FROM OUTSIDE. Both neighbours live on D - Kept in Mercury (t8) ends on a
# D-minor colour (292/342/468/547/877 Hz), Call and Return (t10) opens on a loud D4 - and this song, in
# Bohlen-Pierce on A, met neither (flow 59: in-seam 7.7 dB off, A4's handpan +25 dB at 468; out-seam 8.5 dB, -32 at
# 292). So D becomes the note from outside the system: the handpan that marks every bifurcation now strikes D4 in
# exact Hz, which BP has no step for - a neighbour's note heard through the wall at each doubling, ringing against
# the tritave scale - the song opens on t8's own D-minor chord (D F A D on the glass pad, still 12-EDO there)
# before the map takes it (with t8's A3 under it, louder), and at the end the floor (bass, its pluck) leaves six beats
# early, the last chords turn to D-F-G-D, a final D4 bell strikes and a choir holds D4+D5 into the tail for t10 to
# answer. Flow 59 -> 62/63.
# T9_R11=none reproduces v10.
R11 = os.environ.get("T9_R11", "d")
SUB_SECS = {"both": ("window", "settle"), "settle": ("settle",), "none": ()}[os.environ.get("T9_SUB", "both")]
C9_BPCLAR = {
    "about": "chirper-two: a Bohlen-Pierce clarinet - the reed on a cylindrical bore pushed harder and brighter, a little "
             "airier, with a quiet sine at exactly 3:1 (the tritave BP repeats at) on every note; ^sub subtone.",
    "synth": {
        "layers": [
            {"name": "reed", "type": "wind", "exciter": "reed",
             "pressure": {"value": float(os.environ.get("T9_BPC_PRESS", "0.46")), "mod": [{"src": "vel", "amount": 0.3}, {"src": "expr.sub", "amount": -0.3}]},
             "breath": {"value": 0.22, "mod": [{"src": "expr.sub", "amount": 0.55}]},
             "bright": {"value": float(os.environ.get("T9_BPC_BRIGHT", "0.38")), "mod": [{"src": "vel", "amount": 0.25}, {"src": "expr.sub", "amount": -0.35}]}},
            {"name": "tritave", "type": "osc", "wave": "sine", "ratio": 3,
             "level": {"value": os.environ.get("T9_TRITAVE", "-20dB"), "mod": [{"src": "expr.sub", "amount": -12}]}},
            {"name": "tongue", "type": "noise",
             "level": {"value": "-70dB", "mod": [{"src": "env.t", "amount": 40}, {"src": "vel", "amount": 8}]}}],
        "env": {"f": {"a": "30ms", "d": "350ms", "s": 0.75, "r": "150ms"}, "t": {"a": "2ms", "d": "30ms", "s": 0}},
        "pitch": {"value": 0, "mod": [{"src": "rand", "amount": 0.01}]},
        "filters": ["hp cutoff=90",
                    {"kind": "lp", "cutoff": {"value": os.environ.get("T9_BPC_LP", "3.6k"), "mod": [{"src": "vel", "amount": 0.8}, {"src": "expr.sub", "amount": -1}]}, "q": 0.7},
                    "peak cutoff=1.5k q=1.4 gain=2dB", "peak cutoff=3.2k q=2 gain=1dB"],
        "amp": {"a": "30ms", "s": 1, "r": "120ms", "curve": 3}},
    "play": {"gate": 0.97, "vel_sens": 0.5, "humanize": {"time": "6ms", "vel": 0.05}},
    "fx": ["reverb kind=room decay=1.4s mix=0.2"],
    "gain": "-3dB"}
R7BASS = os.environ.get("T9_R7_BASS", "layer") if R7 == "lpg" else "none"   # lpg | layer | sub
R7DIZI = os.environ.get("T9_R7_DIZI", "0") == "1" and R7 == "lpg"
C9_LPG = {"about": "chirper-two: a West Coast low-pass-gate bass - triangle plus its octave, folded, through one "
                   "envelope that opens the filter and the amp together and lets both fall (a struck, vocal pluck).",
          "synth": {"layers": [{"wave": "triangle"}, {"wave": "sine", "ratio": 2, "level": "-10dB"}],
                    "env": {"lpg": {"a": "1ms", "d": "320ms", "s": 0, "curve": 3}},
                    "filters": [{"kind": "lp", "q": 1.4,
                                 "cutoff": {"value": 140, "mod": [{"src": "env.lpg", "amount": 4.5}, {"src": "vel", "amount": 1.0}]}}],
                    "drive": {"value": 0.35, "mod": [{"src": "vel", "amount": 0.3}]},
                    "amp": {"a": "1ms", "d": "520ms", "s": 0, "r": "90ms", "curve": 3}},
          "play": {"vel_sens": 0.6}}
C9_PULSE = {"about": "chirper-two: a one-bit loudspeaker voice - a very narrow pulse (6%, wider with velocity), crushed, "
                     "nothing smoothing it: a machine driving its speaker directly.",
            "synth": {"layers": [{"wave": "pulse", "width": {"value": 0.06, "mod": [{"src": "vel", "amount": 0.12}]}}],
                      "filters": ["hp cutoff=180", "lp cutoff=7k"],
                      "amp": {"a": "0.5ms", "d": "80ms", "s": 0, "r": "20ms"}},
            "fx": ["crush bits=5 rate=16kHz"],
            "play": {"vel_sens": 0.7}}
SING = []


def sing(at, scale=1.0):
    src = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "t9", "sing.json")))["tracks"][0]
    for nt in src["notes"]:
        m = round(69 + 12 * math.log2(float(nt["pitch"].rstrip("hz")) / 440))
        d = {"at": round(at + nt["at"], 4), "len": nt["len"], "ph": nt["ph"], "pitch": f"m{m}",
             "vel": round(nt["vel"] * scale, 3)}
        if nt.get("expr_path"):
            d["expr_path"] = nt["expr_path"]
        SING.append(d)
    return src["patch"]
GROUPS = {(4, 4): [4, 4, 4, 4], (7, 8): [4, 4, 6], (5, 4): [6, 4, 6, 4], (6, 8): [6, 6], (11, 8): [6, 6, 6, 4]}  # 16ths


def bp(deg, base):
    o, d = divmod(deg, 9)
    return base + o * TRITAVE + LAMBDA[d] * BP


def mm(m):
    return f"m{m:.3f}"


class Track:
    def __init__(self, name):
        self.name, self.ev = name, []

    def add(self, at, ln, head, vel, art=""):
        self.ev.append((round(max(0.0, at), 4), max(0.03, round(ln, 4)), head, int(max(1, min(127, vel))), art))

    def score(self, total):
        ev = sorted(self.ev, key=lambda x: (x[0], -x[3]))
        merged = []
        for x in ev:
            if x[0] >= total - 1e-6:
                continue
            if merged and abs(merged[-1][0] - x[0]) < 1e-3:
                continue
            merged.append(x)
        toks, pos = [], 0.0
        for i, (s, ln, head, vel, art) in enumerate(merged):
            nxt = merged[i + 1][0] if i + 1 < len(merged) else total
            gap = nxt - s
            if s - pos > 1e-4:
                toks.append(f"R/{s - pos:.4g}b")
            if ln > gap + 1e-6:
                toks.append(f"{head}/{gap:.4g}b@{vel}^gate={min(4.0, ln / gap):.3g}{art}")
            else:
                toks.append(f"{head}/{ln:.4g}b@{vel}{art}")
                if gap - ln > 1e-4:
                    toks.append(f"R/{gap - ln:.4g}b")
            pos = nxt
        if total - pos > 1e-4:
            toks.append(f"R/{total - pos:.4g}b")
        return " ".join(toks)


def build():
    rng = random.Random(9)
    names = ("kick", "snare", "hats", "ride", "lead", "blip", "bass", "pad", "padx", "bell", "chop")
    T = {k: Track(k) for k in names}
    x, y = 0.2, 0.71
    pos = 0.0
    secs = []
    trace = []
    for name, nbars, meter, r0, r1 in SECS:
        secs.append((name, pos, nbars, meter))
        steps = int(round(meter[0] * 16 / meter[1]))  # sixteenths a bar
        groups = GROUPS[meter]
        for i in range(nbars):
            start = pos
            frac = i / max(1, nbars - 1)
            r = r0 + (r1 - r0) * frac
            xs = []
            for s in range(steps):
                x = r * x * (1 - x)
                xs.append(x)
            trace.append((name, i, [round(v, 3) for v in xs[:8]]))
            # ---- the lead: the map, one sixteenth per iterate (silent under 0.42) ----
            if not (name == "one" and i < 2):
                for s, v in enumerate(xs):
                    if v > 0.42:
                        deg = max(0, min(13, int((v - 0.3) * 16)))
                        T["lead"].add(start + s * 0.25, 0.24, mm(bp(deg, 57)), int(58 + 50 * v),
                                      "^sub=0.7" if R10 == "bpclar" and name in SUB_SECS else "")
            # ---- drums: grouped kicks, a snare on the last group, map-made accents and ratchets ----
            groove = name not in ("one",) or i >= 8
            if groove and name != "settle" or (name == "settle" and i < 20):
                g0 = 0
                for gi, g in enumerate(groups):
                    T["kick"].add(start + g0 * 0.25, 0.5, "k", 112 if gi == 0 else 100)
                    g0 += g
                T["snare"].add(start + (steps - groups[-1]) * 0.25, 0.4, "s", 98)
                for s, v in enumerate(xs):
                    if v > 0.93 and s % 2 == 1 and name in ("chaos", "storm", "window"):
                        T["kick"].add(start + s * 0.25, 0.25, "k", 90)
                    if 0.45 < v < 0.52 and name in ("chaos", "storm"):
                        T["snare"].add(start + s * 0.25, 0.25, "s", 80, "^r=3")
                    if s % 2 == 1 or name in ("chaos", "storm", "window"):
                        T["hats"].add(start + s * 0.25 + 0.01, 0.1, "h", int(40 + 40 * v), "?0.85")
                    if s % 4 == 2:
                        T["ride"].add(start + s * 0.25 + 0.01, 0.5, "rd", 60, "?0.9")
                    if R4 == "break" and name in ("chaos", "storm"):   # the map chops the break
                        piece = ("g" if 0.25 < v <= 0.45 else "s2" if 0.52 <= v < 0.62 else
                                 "oh" if 0.8 < v <= 0.93 and s % 2 == 0 else None)
                        if piece:
                            T["chop"].add(start + s * 0.25, 0.25, piece,
                                          {"g": 52, "s2": 74, "oh": 58}[piece] + int(20 * v))
            # ---- polytempo: blips on a 5:4 grid from the map's twin ----
            if name not in ("one", "two"):
                k, t = 0, 0.0
                bar_beats = steps / 4
                while t < bar_beats - 1e-6:
                    y = min(4.0, r + 0.02) * y * (1 - y)
                    if y > 0.62:
                        T["blip"].add(start + t, 0.15, mm(bp(int(y * 9) + 9, 57)), int(50 + 40 * y), "?0.8")
                    t += 0.2
                    k += 1
            # ---- the bass on a 3:4 grid, folded ----
            if name not in ("one",) or i >= 12:
                xb = xs[0]
                deg = int(xb * 5)
                t = 0.0
                bar_beats = steps / 4
                while t < bar_beats - 1e-6:
                    T["bass"].add(start + t, 1.1, mm(bp(deg, 33)), 96 if t == 0 else 82)
                    t += 4 / 3
            # ---- BP 3:5:7 chords on the glass pad, every two bars ----
            if i % 2 == 0 and name in ("one", "four", "window", "settle", "eight"):
                root = int(xs[0] * 5)
                base = bp(root, 57)
                T["pad"].add(start, steps / 4 * 2 - 0.1, ",".join(mm(base + st * BP) for st in (0, 6, 10)), 64)
            if R3 == "sing" and ((name == "window" and i in (2, 10)) or (name == "settle" and i == 22)):
                sing(start, 0.85 if name == "settle" else 1.0)
            if R2 == "drift" and i % 2 == 0 and name in ("chaos", "storm"):
                root = int(xs[0] * 5)
                base = bp(root, 57)
                T["padx"].add(start, steps / 4 * 2 - 0.1, ",".join(mm(base + st * BP) for st in (0, 6, 10, 13)), 80)
            if i == 0:
                T["bell"].add(start, 6.0, mm(bp(0, 69)), 70)
            pos += steps / 4
    total = pos
    return total, secs, T, trace


def tempo_map(secs, total):
    pts = []
    for name, s, n, meter in secs:
        p = {"at": f"{s:g}b", "bpm": BPM[name], "meter": f"{meter[0]}/{meter[1]}"}
        if name in ("window",):
            p["ramp"] = True       # chaos ramps 140 -> 150 into the window
        pts.append(p)
    pts.append({"at": f"{total:g}b", "bpm": 132, "ramp": True})  # settle slows to 132
    return pts


def j_even(k):
    return k % 2 == 0


def seconds(tm, total):
    pts = [(float(p["at"][:-1]), p["bpm"], p.get("ramp", False)) for p in tm]
    sec = 0.0
    for (a, b0, _), (b, b1, ramp) in zip(pts, pts[1:]):
        if ramp:
            sec += (b - a) * 60 * math.log(b1 / b0) / (b1 - b0) if b1 != b0 else (b - a) * 60 / b0
        else:
            sec += (b - a) * 60 / b0
    return sec


def main():
    total, secs, T, trace = build()
    st = {n: s for n, s, k, m in secs}
    if R11 == "d":
        T["bell"].ev = [(a, ln, "293.66hz", v, art) for a, ln, h, v, art in T["bell"].ev]
        T["bell"].add(total - 8.0, 8.0, "293.66hz", int(os.environ.get("T9_DBELL_VEL", "66")))
        dm_in = os.environ.get("T9_D_IN", "m57.000,m62.000,m65.000,m69.000,m74.000")
        dm_out = os.environ.get("T9_D_OUT", "m62.000,m65.000,m67.000,m74.000")
        for k in ("bass", "bpluck", "ksub"):   # the floor leaves before the last D, so it rings alone
            if k in T:
                T[k].ev = [e for e in T[k].ev if e[0] < total - 6.0]
        T["pad"].ev = [(a, ln, dm_in, 120, art) if a < 8.0 - 1e-6 else
                       ((a, ln, dm_out, 84, art) if a >= total - 16.0 - 1e-6 else (a, ln, h, v, art))
                       for a, ln, h, v, art in T["pad"].ev]
    orbit, fill = Track("orbit"), Track("fill")
    o0 = st["eight"] + 8 * 5                      # the eight section's ninth bar (256b): the window
    if R5 == "orbit":
        xs8 = next(xs for name, i, xs in trace if name == "eight" and i == 8)
        hz = sorted(220.0 * 3 ** ((v - 0.3) * 16 / 13) for v in xs8)
        orbit_notes = [{"at": o0, "len": 54.0, "pitch": f"{h:.2f}hz", "vel": 0.57 if k % 2 == 0 else 0.52}
                       for k, h in enumerate(hz)]
        for k, at in enumerate([o0 + 16 + 0.25 * j for j in range(16)]):   # the fill: 16th ratchets rising
            fill.add(at, 0.25, "s2" if j_even(k) else "g", 50 + 3 * k, "^r=2" if k >= 8 else "")
    dizi = Track("dizi")
    bpl = Track("bpluck")
    if R7BASS == "layer":   # the low-pass gate as the bass's voice, an octave over the sub body it leaves in place
        for a, ln, h, v, art in T["bass"].ev:
            bpl.add(a, min(ln, 0.9), f"m{float(h[1:]) + 12:.3f}", v, art)
    if R7DIZI:
        for a, ln, h, v, art in T["lead"].ev:
            if (st["two"] <= a < st["eight"] or a >= st["settle"]) and v >= 92:
                dizi.add(a, ln, f"m{float(h[1:]) + 12:.3f}", v - 14, art)
    ret, tab = Track("ret"), Track("tab")
    if R9 == "return":
        one, two = next(s for s in SECS if s[0] == "one"), next(s for s in SECS if s[0] == "two")
        hz = lambda v: f"{2 * 220.0 * 3 ** ((v - 0.3) * 16 / 13):.2f}hz"
        xs = 1 - 1 / one[3]
        for a, x0 in ((st["two"] - 16.0, xs - 0.2), (st["two"] - 8.0, xs + 0.18)):
            for i, v in enumerate([x0] + lmap(one[3], x0, 15)):
                ret.add(a + i * 0.5, 0.45, hz(v), max(40, 74 - 2 * i))
        orb = logistic_orbit(two[3], 2)
        bl = 3.5
        for b in range(two[1]):
            a = st["two"] + b * bl
            pat = TABLA[b % 4] if b % 4 != 3 else TABLA[3]
            for i, bol in enumerate(pat):
                if bol == "te":
                    tab.add(a + i * 0.5, 0.25, "te", 62)
                    tab.add(a + i * 0.5 + 0.25, 0.25, "re", 56)
                elif bol == "re":
                    continue
                else:
                    tab.add(a + i * 0.5, 0.5, bol, 78 if i in (0, 3, 5) else 60)
            if b % 2 == 1 or os.environ.get("T9_KNOCK", "half") == "every":
                d = KNOCKS[(b // 2) % len(KNOCKS)] * (1 if b % 2 else -0.7)
                x0 = min(0.95, max(0.05, orb[b % 2] + d))
                for i, v in enumerate([x0] + lmap(two[3], x0, 6)):
                    ret.add(a + i * 0.5, 0.45, hz(v), 76 if i == 0 else 60)
    osti = Track("osti")
    if R8 == "ostinato":
        sec4 = next(s for s in SECS if s[0] == "four")
        sec8 = next(s for s in SECS if s[0] == "eight")
        o4, o8 = logistic_orbit(sec4[3], 4), logistic_orbit(sec8[3], 8)
        a, end4, end8 = st["eight"] - 24.0, st["eight"], st["eight"] + 40.0
        k = 0
        while a < end8 - 1e-6:
            pts = o4 if a < end4 else o8
            v = pts[k % len(pts)]
            hz = 2 * 220.0 * 3 ** ((v - 0.3) * 16 / 13)
            if a < end4:
                vel = int(50 + 30 * (a - (end4 - 24.0)) / 24.0) + (8 if k % 4 == 0 else 0)
            else:
                vel = 82 + (10 if (k - 48) % 8 == 0 else 0)
            osti.add(a, 0.45, f"{hz:.2f}hz", vel)
            a += 0.5
            k += 1
            if abs(a - end4) < 1e-6:
                k = 48
    steel = Track("steel")
    if R6 == "steel":
        sname, sbars, smeter, sr0, sr1 = next(s for s in SECS if s[0] == "settle")
        for i in range(2, sbars):
            r = sr0 + (sr1 - sr0) * i / max(1, sbars - 1)
            a = st["settle"] + 4 * i
            if r > 3.0:
                d = math.sqrt((r + 1) * (r - 3))
                pts = [((r + 1) + d) / (2 * r), ((r + 1) - d) / (2 * r)]
            else:
                pts = [1 - 1 / r]
            for k, v in enumerate(pts):
                hz = 220.0 * 3 ** ((v - 0.3) * 16 / 13)
                ln = 4.0 / len(pts)
                steel.add(a + k * ln, ln, f"{hz:.2f}hz", 78 if k == 0 else 70, "^gate=1.15")
    ksub = Track("ksub")   # v4: the break kit's kick is a 1969 kick (A#1): a short sine an octave under each one
    for at, ln, head, vel, art in T["kick"].ev:
        ksub.add(at, 0.4, "E1", vel, art)
    tm = tempo_map(secs, total)
    chaos = [["0b", 0.0], [f"{st['chaos']}b", 0.05], [f"{st['window']}b", 0.25], [f"{st['window'] + 0.01}b", 0.05],
             [f"{st['storm']}b", 0.2], [f"{st['settle']}b", 0.4], [f"{st['settle'] + 0.01}b", 0.0], [f"{total}b", 0.0]]
    dyn = [["0b", -3.0], [f"{st['two']}b", -1.0], [f"{st['chaos']}b", 0.0], [f"{st['window']}b", -2.0],
           [f"{st['storm'] - 0.01}b", -2.0], [f"{st['storm']}b", 0.0], [f"{st['settle']}b", -1.0], [f"{total}b", -4.0]]
    if R5 == "orbit":   # the breakdown sits lower: the song's dynamic range opens
        o0 = st["eight"] + 8 * 5
        lv = lambda b: next(v0 + (v1 - v0) * (b - float(a0[:-1])) / (float(a1[:-1]) - float(a0[:-1]))   # noqa: E731
                            for (a0, v0), (a1, v1) in zip(dyn, dyn[1:]) if float(a0[:-1]) <= b <= float(a1[:-1]))
        dyn = sorted(dyn + [[f"{o0}b", lv(o0)], [f"{o0 + 4}b", lv(o0) - 3.0], [f"{o0 + 14}b", lv(o0) - 3.0],
                            [f"{o0 + 16}b", lv(o0 + 16)]], key=lambda p: float(p[0][:-1]))
    pump = {"type": "pump", "on": "kick.k", "depth": "-5dB", "attack": "3ms", "release": "200ms", "curve": 0.8}
    tracks = [
        {"name": "kick", "patch": KIT, "gain": "-5dB", "out": "drums",
         "fx": ["hp cutoff=28", "lowshelf cutoff=60 gain=5dB"] if R4 == "break" else ["hp cutoff=45"], "score": T["kick"].score(total)},
        {"name": "snare", "patch": KIT, "gain": "-4dB", "out": "drums", "score": T["snare"].score(total)},
        {"name": "hats", "patch": KIT, "gain": "-2dB", "pan": 0.2, "out": "drums",
         "fx": ["hp cutoff=800"] + (["lp cutoff=9k"] if R4 == "break" else []),
         "score": T["hats"].score(total)},
        {"name": "ride", "patch": KIT, "gain": "-5dB", "pan": -0.25, "out": "drums", "fx": ["hp cutoff=3000"],
         "score": T["ride"].score(total)},
        {"name": "lead", "patch": "c9-bpclar" if R10 == "bpclar" else "clarinet", "gain": "-10.5dB" if R10 == "bpclar" else "-8dB",
         "pan": ({"value": 0.0, "mod": [{"src": "var.wander", "amount": 1}]} if R2 == "drift" else -0.1),
         "fx": ["hp cutoff=220", "peak cutoff=1200 gain=4dB q=0.8", {"type": "delay", "time": "3/16", "feedback": 0.3, "mix": 0.2, "ping_pong": True, "tone": 4000},
                "reverb kind=room decay=0.9s mix=0.15"], "score": T["lead"].score(total)},
        {"name": "blip", "patch": "c9-pulse" if R4 == "break" else "blip",
         "gain": os.environ.get("T9_PULSE_GAIN", "-6dB") if R4 == "break" else "-7dB", "pan": 0.35,
         "fx": [{"type": "delay", "time": "1/8", "feedback": 0.35, "mix": 0.25, "ping_pong": True, "tone": 6000}],
         "score": T["blip"].score(total)},
        {"name": "bass", "patch": "c9-lpg" if R7BASS == "lpg" else "sub-sine",
         "gain": os.environ.get("T9_LPG_GAIN", "-15dB") if R7BASS == "lpg" else "-13dB",
         "fx": [{"type": "drive", "drive": 0.55, "shape": "fold", "mix": 0.5},
                "lp cutoff=1100" if R7BASS == "lpg" else "lp cutoff=600", "hp cutoff=38", pump],
         "score": T["bass"].score(total)},
        {"name": "pad", "patch": "pad-glass", "gain": "-19dB", "fx": [pump], "score": T["pad"].score(total)},
        *([{"name": "sing",
            "patch": json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "t9", "sing.json")))["tracks"][0]["patch"],
            "gain": os.environ.get("T9_SING_GAIN", "-10dB"), "pan": 0.0,
            "fx": ["hp cutoff=140", "compressor threshold=-20dB ratio=3 attack=5ms release=120ms",
                   {"type": "delay", "time": "3/16", "feedback": 0.35, "mix": 0.22, "ping_pong": True, "tone": 3500},
                   "reverb kind=room decay=1.2s mix=0.2"], "notes": SING}] if R3 == "sing" else []),
        *([{"name": "padx", "patch": "pad-glass", "gain": os.environ.get("T9_PADX_GAIN", "-14dB"),
            "fx": [{"type": "morph", "key": "drums", "mode": "cross", "amount": 0.8}, "hp cutoff=200"],
            "score": T["padx"].score(total)}] if R2 == "drift" else []),
        {"name": "bell", "patch": "handpan" if R6 == "steel" else "bell",
         "gain": os.environ.get("T9_PAN_GAIN", "-6dB") if R6 == "steel" else "-14dB", "fx": ["reverb kind=hall decay=3s mix=0.35"],
         "score": T["bell"].score(total)},
        *([{"name": "chop", "patch": "break-kit", "gain": os.environ.get("T9_CHOP_GAIN", "0dB"), "pan": -0.1,
            "out": "drums", "score": T["chop"].score(total)},
           *([{"name": "orbit", "patch": "choir-classic amp.a=3s amp.r=4s", "gain": os.environ.get("T9_ORBIT_GAIN", "-10dB"),
               "pan": 0.0, "fx": ["hp cutoff=180", "chorus mix=0.15", "reverb kind=hall decay=4s mix=0.35"],
               "notes": orbit_notes},
              {"name": "fill", "patch": "break-kit", "gain": "-3dB", "pan": 0.1, "out": "drums",
               "score": fill.score(total)}] if R5 == "orbit" else []),
           *([{"name": "ret", "patch": "koto", "gain": os.environ.get("T9_KOTO_GAIN", "1dB"), "pan": -0.28,
               "fx": ["hp cutoff=200", "reverb kind=room decay=0.9s mix=0.16"], "score": ret.score(total)},
              {"name": "tab", "patch": "tabla-kit", "gain": os.environ.get("T9_TABLA_GAIN", "-5dB"), "pan": 0.22,
               "fx": ["reverb kind=room decay=0.5s mix=0.12"], "score": tab.score(total)}]
             if R9 == "return" else []),
           *([{"name": "osti", "patch": "steel-pan", "gain": os.environ.get("T9_OSTI_GAIN", "-8dB"), "pan": 0.3,
               "fx": ["hp cutoff=250", "reverb kind=room decay=0.8s mix=0.18"], "score": osti.score(total)}]
             if R8 == "ostinato" else []),
           *([{"name": "steel", "patch": "pedal-steel", "gain": os.environ.get("T9_STEEL_GAIN", "-4dB"), "pan": -0.15,
               "sends": {}, "fx": ["hp cutoff=150", {"type": "delay", "time": "3/8", "feedback": 0.3, "mix": 0.2,
                                                     "ping_pong": True, "tone": 3500}],
               "score": steel.score(total)}] if R6 == "steel" else []),
           *([{"name": "dizi", "patch": "dizi", "gain": os.environ.get("T9_DIZI_GAIN", "-5dB"), "pan": 0.2,
               "fx": ["hp cutoff=400", {"type": "delay", "time": "3/16", "feedback": 0.25, "mix": 0.18, "ping_pong": True,
                                        "tone": 5000}, "reverb kind=room decay=0.9s mix=0.2"],
               "score": dizi.score(total)}] if R7DIZI else []),
           *([{"name": "bpluck", "patch": "c9-lpg", "gain": os.environ.get("T9_PLUCK_GAIN", "-16dB"), "pan": 0.08,
               "fx": ["hp cutoff=90", {"type": "drive", "drive": 0.45, "shape": "fold", "mix": 0.4}, "lp cutoff=2400", pump],
               "score": bpl.score(total)}] if R7BASS == "layer" else []),
           {"name": "ksub", "patch": "sub-sine amp.d=180ms amp.s=0 amp.r=40ms", "gain": os.environ.get("T9_KSUB_GAIN", "-4dB"),
            "fx": ["lp cutoff=120"], "score": ksub.score(total)}] if R4 == "break" else []),
    ]
    buses = {"drums": {"gain": "0dB",
                       "fx": [{"type": "stutter", "slice": "1/16", "repeats": 4, "decay": 0.15, "pitch": 1.5, "seed": 9,
                               "chance": {"value": 0, "mod": [{"src": "auto.chaos", "amount": 1}]}},
                              "glue threshold=-16dB ratio=3 attack=5ms release=100ms",
                              "reverb kind=room decay=0.5s mix=0.1"] +
                             ([{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.drop", "amount": 1}]}}]
                              if R5 == "orbit" else []),
                       "auto": {"chaos": {"points": chaos},
                                **({"drop": {"points": [["0b", 0.0], [f"{o0}b", 0.0], [f"{o0 + 4}b", -30.0],
                                                        [f"{o0 + 14}b", -30.0], [f"{o0 + 16}b", 0.0],
                                                        [f"{total}b", 0.0]]}} if R5 == "orbit" else {})}}}
    secline = "; ".join(f"{n} {m[0]}/{m[1]} from {s:g}b ({k} bars)" for n, s, k, m in secs)
    about = ("chirpers - A Light Left On, track 9. Original composition by chirper-two, generated by "
             "compose/chirpers8/src/chirpers8-t9.py. Polytempo braindance in Bohlen-Pierce tuning (13 steps to the 3:1 "
             "tritave): the logistic map, iterated each sixteenth, walks from one note through period doubling into "
             f"chaos, its period-three window and back, on a physical reed. Sections: {secline}.")
    if R11 == "d":   # the voices find D: a choir holds D4 and D5 through the last bars into the tail, for t10
        dh = Track("dhold")
        dh.add(total - 12.0, 12.0, "m62.000,m74.000", int(os.environ.get("T9_DHOLD_VEL", "90")))
        tracks.append({"name": "dhold", "patch": "choir-classic amp.a=2s amp.r=2.5s",
                       "gain": os.environ.get("T9_DHOLD_GAIN", "-8dB"), "pan": 0.0,
                       "fx": ["hp cutoff=180", "reverb kind=hall decay=2.5s mix=0.25"], "score": dh.score(total)})
    lines = [
        f"about: {json.dumps(about)}",
        "meta: " + json.dumps({"artist": "chirpers", "album": "A Light Left On", "title": "Period Doubling", "track": 9,
                               "year": 2026}),
        "tempo: " + json.dumps(tm),
        *(["tuning: " + json.dumps([{"edo": 12},
                                    {"at": f"{st['four']:g}b", "edo": 13, "period": "3/1", "root": "A3", "ramp": "20bar"},
                                    {"at": f"{st['settle'] + 32:g}b", "edo": 12, "ramp": "16bar"}]),
           "vars: " + json.dumps({"wander": {"system": {"type": "logistic", "r": 3.95, "n": 1600, "range": [-0.6, 0.6]},
                                             "every": "1/8"}})] if R2 == "drift" else []),
        f'length: "{total:g}b"',
        'tail: "2s"',
        'ceiling: "-1dB"',
        'volume: "0dB"',
        "loudness: -11",
        "true_peak: true",
        *(["patches: " + json.dumps({"c9-pulse": C9_PULSE, **({"c9-lpg": C9_LPG} if R7BASS in ("lpg", "layer") else {}),
                                     **({"c9-bpclar": C9_BPCLAR} if R10 == "bpclar" else {})})]
          if R4 == "break" else []),
        "buses: " + json.dumps(buses),
        "master: " + json.dumps({"fx": [{"type": "eq", "bands": (["hp cutoff=25", "peak cutoff=90 gain=-4dB q=0.9",
                                                               "peak cutoff=420 gain=-3dB q=0.8",
                                                               "highshelf cutoff=5000 gain=5dB"] if R4 != "break" else
                                                              ["hp cutoff=25", "peak cutoff=85 gain=-6dB q=0.9",
                                                               "peak cutoff=380 gain=-4.5dB q=0.8",
                                                               "peak cutoff=1150 gain=" + os.environ.get("T9_MID_GAIN", "0dB" if R7BASS == "lpg" or R7DIZI else "1.5dB" if R7BASS == "layer" else "3dB") + " q=0.6",
                                                               "highshelf cutoff=5000 gain=-5dB"])},
                                        "glue threshold=-20dB ratio=2 attack=10ms release=150ms makeup=1dB",
                                        {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                                        {"type": "limiter", "ceiling": "-1.2dB", "release": "80ms"}],
                                 "auto": {"dyn": {"points": dyn}}}),
        "tracks:",
    ]
    lines += ["  - " + json.dumps(t) for t in tracks]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write("\n".join(lines) + "\n")
    print(f"wrote {OUT}: {total:g} beats, {seconds(tm, total):.0f} s; {secline}")
    for name, i, xs in trace:
        if i in (4,) or (name == "window" and i in (1, 8, 15)):
            print(f"  {name:7s} bar {i}: x = {xs}")


if __name__ == "__main__":
    main()
