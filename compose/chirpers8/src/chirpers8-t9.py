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
    names = ("kick", "snare", "hats", "ride", "lead", "blip", "bass", "pad", "padx", "bell")
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
                        T["lead"].add(start + s * 0.25, 0.24, mm(bp(deg, 57)), int(58 + 50 * v))
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
    tm = tempo_map(secs, total)
    chaos = [["0b", 0.0], [f"{st['chaos']}b", 0.05], [f"{st['window']}b", 0.25], [f"{st['window'] + 0.01}b", 0.05],
             [f"{st['storm']}b", 0.2], [f"{st['settle']}b", 0.4], [f"{st['settle'] + 0.01}b", 0.0], [f"{total}b", 0.0]]
    dyn = [["0b", -3.0], [f"{st['two']}b", -1.0], [f"{st['chaos']}b", 0.0], [f"{st['window']}b", -2.0],
           [f"{st['storm'] - 0.01}b", -2.0], [f"{st['storm']}b", 0.0], [f"{st['settle']}b", -1.0], [f"{total}b", -4.0]]
    pump = {"type": "pump", "on": "kick.k", "depth": "-5dB", "attack": "3ms", "release": "200ms", "curve": 0.8}
    tracks = [
        {"name": "kick", "patch": "machine-kit", "gain": "-5dB", "out": "drums", "fx": ["hp cutoff=45"], "score": T["kick"].score(total)},
        {"name": "snare", "patch": "machine-kit", "gain": "-4dB", "out": "drums", "score": T["snare"].score(total)},
        {"name": "hats", "patch": "machine-kit", "gain": "-2dB", "pan": 0.2, "out": "drums", "fx": ["hp cutoff=800"],
         "score": T["hats"].score(total)},
        {"name": "ride", "patch": "machine-kit", "gain": "-5dB", "pan": -0.25, "out": "drums", "fx": ["hp cutoff=3000"],
         "score": T["ride"].score(total)},
        {"name": "lead", "patch": "clarinet", "gain": "-8dB",
         "pan": ({"value": 0.0, "mod": [{"src": "var.wander", "amount": 1}]} if R2 == "drift" else -0.1),
         "fx": ["hp cutoff=220", "peak cutoff=1200 gain=4dB q=0.8", {"type": "delay", "time": "3/16", "feedback": 0.3, "mix": 0.2, "ping_pong": True, "tone": 4000},
                "reverb kind=room decay=0.9s mix=0.15"], "score": T["lead"].score(total)},
        {"name": "blip", "patch": "blip", "gain": "-7dB", "pan": 0.35,
         "fx": [{"type": "delay", "time": "1/8", "feedback": 0.35, "mix": 0.25, "ping_pong": True, "tone": 6000}],
         "score": T["blip"].score(total)},
        {"name": "bass", "patch": "sub-sine", "gain": "-13dB",
         "fx": [{"type": "drive", "drive": 0.55, "shape": "fold", "mix": 0.5}, "lp cutoff=600", "hp cutoff=38", pump],
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
        {"name": "bell", "patch": "bell", "gain": "-14dB", "fx": ["reverb kind=hall decay=3s mix=0.35"],
         "score": T["bell"].score(total)},
    ]
    buses = {"drums": {"gain": "0dB",
                       "fx": [{"type": "stutter", "slice": "1/16", "repeats": 4, "decay": 0.15, "pitch": 1.5, "seed": 9,
                               "chance": {"value": 0, "mod": [{"src": "auto.chaos", "amount": 1}]}},
                              "glue threshold=-16dB ratio=3 attack=5ms release=100ms",
                              "reverb kind=room decay=0.5s mix=0.1"],
                       "auto": {"chaos": {"points": chaos}}}}
    secline = "; ".join(f"{n} {m[0]}/{m[1]} from {s:g}b ({k} bars)" for n, s, k, m in secs)
    about = ("chirpers - A Light Left On, track 9. Original composition by chirper-two, generated by "
             "compose/chirpers8/src/chirpers8-t9.py. Polytempo braindance in Bohlen-Pierce tuning (13 steps to the 3:1 "
             "tritave): the logistic map, iterated each sixteenth, walks from one note through period doubling into "
             f"chaos, its period-three window and back, on a physical reed. Sections: {secline}.")
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
        "buses: " + json.dumps(buses),
        "master: " + json.dumps({"fx": [{"type": "eq", "bands": ["hp cutoff=25", "peak cutoff=90 gain=-4dB q=0.9",
                                                               "peak cutoff=420 gain=-3dB q=0.8",
                                                               "highshelf cutoff=5000 gain=5dB"]},
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
