#!/usr/bin/env python3
"""chirpers4-t1 (Phantom Downbeat, track 1) - generator for songs/chirpers4-t1.yaml (chirper-zero).

DEEP / HYPNOTIC OPENER / "behind the door". 122 bpm 4/4 in A minor. The album's door into the club: an OCCLUSION
illusion - the same music heard first through a wall (a low-pass and a damp, distant room on the club bus), then the
door opens and you are in the room, and at the end it closes behind you. Original; a style, not a version of any track.

Outside the door (always clear): a deep juno pad (Am9, Fmaj7#11) and the corridor's air. Inside (on the CLUB bus, behind
the wall): the 909 kick and hats, the sub, and THE CELL - a song-local deep pluck playing a 7-step figure against the
bar, its filter and resonance drifting on 7-, 5- and 3-bar LFOs.

Form (bars): corridor 16 (the pad, the air; the kick a muffled thud through the wall from bar 5) / door 8 (the wall
opens) / floor A 32 / deep 16 (no kick: the pad, the cell, the hats) / floor B 32 (the kick back, the ride) / door
closes 16 (the wall shuts over eight bars, then the corridor again: the thud through the wall to the end).

Run: python3 compose/chirpers4/src/chirpers4-t1.py  (writes songs/chirpers4-t1.yaml)
"""
import json
import os

ROOT = os.path.expanduser("~/.config/chirp")
OUT = os.environ.get("C4T1_OUT") or os.path.join(ROOT, "songs", "chirpers4-t1.yaml")
BPM = 122
SPB = 60 / BPM
BAR = 4 * SPB
S = 0.25
MG = float(os.environ.get("C4T1_MG", "18"))
CLOSE8 = os.environ.get("C4T1_CLOSE8", "1") == "1"  # the door closes over eight bars, then the corridor again: only the kick's thud through the wall to the end (a mirror of the opening)
SWING = os.environ.get("C4T1_SWING", "")
TRES = os.environ.get("C4T1_TRES", "1") == "1"  # the cell on a 3+3+2 16th grid (0 3 6 8 11 14), the 7 notes cycling through it - syncopated against the kick  # a light 16th swing on the kit and the cell, e.g. 0.58

NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
FORM = [("corridor", 16), ("door", 8), ("A", 32), ("deep", 16), ("B", 32), ("close", 16)]
PADS = [[45, 57, 60, 64, 67, 71], [41, 57, 60, 64, 67, 71]]  # Am9 (A2 A3 C4 E4 G4 B4), Fmaj7#11 colour over F2
CELL = [69, 72, 76, 71, 74, 72, 64]  # THE CELL: A4 C5 E5 B4 D5 C5 E4, seven notes cycling through a 6-hit 3+3+2 bar


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def R(d):
    return f"R/{d:g}b" if d > 1e-9 else ""


def J(*xs):
    return " ".join(x for x in xs if x)


def grid(events, steps=16):
    ev = sorted(events)
    out, pos = [], 0
    for i, (st, head, ln, vel) in enumerate(ev):
        if st < pos:
            continue
        nxt = ev[i + 1][0] if i + 1 < len(ev) else steps
        ln = max(1, min(ln, nxt - st, steps - st))
        out.append(R((st - pos) * S))
        out.append(f"{head}/{ln * S:g}b@{int(vel)}")
        pos = st + ln
    out.append(R((steps - pos) * S))
    return J(*out)


def starts():
    t, out = 0, {}
    for sec, nb in FORM:
        out[sec] = t
        t += nb
    return out, t


def kit(sec, b):
    ev = {}

    def add(st, piece, vel):
        ev.setdefault(st, []).append((piece, vel))

    kick = (sec == "corridor" and b >= 4) or sec in ("door", "A", "B") or (sec == "close" and (b < 12 or CLOSE8))
    if kick:
        for st in (0, 4, 8, 12):
            add(st, "k", 116 if st == 0 else 108)
    if sec in ("A", "B", "deep") or (sec == "door" and b >= 4) or (sec == "close" and b < 8):
        for st in (2, 6, 10, 14):
            add(st, "oh" if sec != "deep" else "h", 70 if sec != "deep" else 56)
    if sec in ("A", "B") and b >= 8:
        for st in range(16):
            if st % 4 != 2:
                add(st, "h", 70 if st % 2 == 1 else 44)
    if sec == "B":
        for st in (0, 4, 8, 12):
            add(st, "rd", 70)
    out = [(st, ",".join(p for p, _ in v), 1, max(vv for _, vv in v)) for st, v in ev.items()]
    return grid(out) if out else R(4)


def sub(sec, b):
    if sec in ("A", "B") or (sec == "door" and b >= 4) or (sec == "close" and b < 8):
        return grid([(st, "A1", 2, 92) for st in (2, 6, 10, 14)])
    return R(4)


def cell(sec, b, gb):
    """THE CELL: 7 notes on the 16th grid, cycling across the bar lines; it enters in the door and thins in the close."""
    if sec == "corridor" or (sec == "close" and b >= 10):
        return R(4)
    ev = []
    if TRES:
        for k, st in enumerate((0, 3, 6, 8, 11, 14)):
            n = gb * 6 + k
            ev.append((st, nm(CELL[n % 7]), 2 if st in (6, 14) else 1, 96 if n % 7 == 0 else 74))
        return grid(ev)
    for st in range(0, 16, 2):  # 8ths: the 7-note cycle walks across the bar (realigns every 7 bars... 8 eighths per bar)
        n = gb * 8 + st // 2
        ev.append((st, nm(CELL[n % 7]), 1, 96 if n % 7 == 0 else 74))
    return grid(ev)


def pad(sec, b, gb):
    v = PADS[(gb // 4) % 2]
    vel = {"corridor": 60, "door": 56, "A": 44, "deep": 62, "B": 42, "close": 58}[sec]
    return f"{','.join(nm(n) for n in v)}/4b@{vel}"


def air(sec, b):
    return "C4/4b@60" if sec in ("corridor", "door", "deep", "close") else R(4)


def build():
    names = ("kit", "sub", "cell", "pad", "air")
    T = {n: [] for n in names}
    gb = 0
    for sec, nb in FORM:
        for b in range(nb):
            T["kit"].append(kit(sec, b))
            T["sub"].append(sub(sec, b))
            T["cell"].append(cell(sec, b, gb))
            T["pad"].append(pad(sec, b, gb))
            T["air"].append(air(sec, b))
            gb += 1
    return T


def lane(points, ramp=None):
    """Steps at section bars; `ramp` = set of bars where the value glides from the previous point instead of stepping."""
    st, total = starts()
    pts = [["0s", points[0][1]]]
    for bar, val in points:
        t = bar * BAR
        if t <= 0:
            continue
        if ramp and bar in ramp:
            pts.append([f"{t:.3f}s", val])
        else:
            pts += [[f"{max(0.0, t - 0.05):.3f}s", pts[-1][1]], [f"{t:.3f}s", val]]
    pts.append([f"{total * BAR + 8:.2f}s", pts[-1][1]])
    return {"points": pts}


def song():
    T = build()
    st, total = starts()
    sc = lambda n: (f"swing16={SWING} " if SWING and n in ("kit", "cell") else "") + " | ".join(T[n])  # noqa: E731
    # THE WALL: the club bus's low-pass (octaves below fully open) - closed through the corridor, opening across the door,
    # open on the floors and the deep section, closing again at the end
    d0, d1, c0, c1 = st["door"], st["A"], st["close"], st["close"] + (8 if CLOSE8 else 16)
    wall = [(0, -6.5), (d0, -6.5), (d1, 0), (c0, 0), (c1, -6.5)] + ([(total, -6.5)] if CLOSE8 else [])
    wall_ramp = {d1, c1}
    room = [(0, 0), (d0, 0), (d1, -1), (c0, -1), (c1, 0)]  # the damp room's send: present behind the wall, gone inside
    dyn = [(0, -6), (st["door"], -3), (st["A"], 0), (st["deep"], -5), (st["B"], 1), (st["close"], -4)]
    pump = lambda d: {"type": "pump", "on": "kit.k", "depth": f"{d}dB", "attack": "4ms", "release": "330ms", "curve": 0.6}  # noqa: E731
    patches = {
        "deep-pluck": {"about": "Phantom Downbeat t1: the deep pluck - a saw and a square an octave down into a resonant 24 dB "
                                "low-pass that snaps open and settles dark; the track's 7-, 5- and 3-bar LFOs move it.",
                       "play": {"vel_sens": 0.5},
                       "synth": {"layers": ["saw", {"wave": "square", "semi": -12, "level": "-8dB"}],
                                 "env": {"f": {"a": "1ms", "d": "160ms", "s": 0.1, "r": "80ms"}},
                                 "filters": [{"kind": "lp", "slope": 24,
                                              "cutoff": {"value": 520, "mod": [{"src": "env.f", "amount": 2.6}, {"src": "vel", "amount": 0.8},
                                                                               {"src": "lfo.a", "amount": 0.9}, {"src": "lfo.b", "amount": 0.5}]},
                                              "q": {"value": 4, "mod": [{"src": "lfo.c", "amount": 2.5}]}}],
                                 "amp": {"a": "1ms", "d": "240ms", "s": 0.1, "r": "90ms"}}},
        "air": {"about": "Phantom Downbeat t1: the corridor's air - pink noise, low-passed, steady.",
                "synth": {"layers": [{"type": "noise", "color": "pink"}], "filters": ["bp cutoff=900 q=0.4"],
                          "amp": {"a": "60ms", "s": 1, "r": "200ms"}}},
    }
    doc = {
        "about": "Chirpers - Phantom Downbeat (Chirpers IV), track 1 by chirper-zero: DEEP / HYPNOTIC OPENER, behind the door. "
                 "Generated by compose/chirpers4/src/chirpers4-t1.py; see its docstring and compose/chirpers4/styles.md.",
        "tempo": BPM, "ceiling": "-0.3dB", "tail": "4s", "patches": patches,
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=24", "peak cutoff=45 q=1 gain=-4dB", "peak cutoff=320 q=0.8 gain=-3dB",
                                                   "highshelf cutoff=2500 gain=8dB"]},
                          {"type": "gain", "gain": f"+{MG:g}dB"},
                          {"type": "drive", "drive": 0.25, "mix": 0.6},
                          {"type": "compressor", "threshold": "-16dB", "ratio": 3, "attack": "10ms", "release": "120ms", "makeup": "2dB"},
                          {"type": "compressor", "threshold": "-6dB", "ratio": 10, "attack": "0.5ms", "release": "40ms", "makeup": "1dB"},
                          {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}}],
                   "auto": {"dyn": lane(dyn)}},
        "buses": {
            "club": {"fx": [{"type": "filter", "kind": "lowpass", "slope": 24, "cutoff": {"value": 18000, "mod": [{"src": "auto.wall", "amount": 1}]}, "q": 0.7}],
                     "sends": {"damp": {"value": "-60dB", "mod": [{"src": "auto.room", "amount": 54}]}},
                     "auto": {"wall": lane(wall, wall_ramp), "room": lane(room, wall_ramp)}},
            "damp": {"fx": ["reverb kind=room decay=1.2s size=0.6 mix=1 predelay=18ms", {"type": "filter", "kind": "lowpass", "cutoff": 900}]},
            "rumble": {"fx": ["reverb kind=hall decay=2.4s size=0.85 mix=1", {"type": "filter", "kind": "lowpass", "cutoff": 160, "q": 0.7},
                              "drive drive=0.35 mix=1", pump(-10)]},
            "hall": {"fx": ["reverb kind=hall decay=4s size=0.9 mix=1 predelay=20ms"]},
        },
        "tracks": [
            {"name": "kit", "patch": "909", "gain": "0dB", "out": "club", "sends": {"rumble": "-5dB"}, "score": sc("kit")},
            {"name": "sub", "patch": "sub-sine", "gain": "-8dB", "out": "club", "fx": [pump(-8)], "score": sc("sub")},
            {"name": "cell", "patch": "deep-pluck", "gain": "-12dB", "out": "club",
             "lfo": {"a": "sine rate=7/1", "b": "tri rate=5/1 phase=0.25", "c": "sine rate=3/1 phase=0.5", "p": "sine rate=5/1 phase=0.75"},
             "pan": {"value": 0.1, "mod": [{"src": "lfo.p", "amount": 0.4}]},
             "fx": [pump(-6), {"type": "delay", "time": "3/8", "feedback": 0.35, "mix": 0.25, "tone": 2500}], "sends": {"hall": "-14dB"}, "score": sc("cell")},
            {"name": "pad", "patch": "juno-pad", "gain": "-14dB", "lfo": {"w": "sine rate=5/1"},
             "pan": {"value": 0, "mod": [{"src": "lfo.w", "amount": 0.3}]}, "fx": [pump(-4)], "sends": {"hall": "-8dB"}, "score": sc("pad")},
            {"name": "air", "patch": "air", "gain": "-30dB", "sends": {"hall": "-10dB"}, "score": sc("air")},
        ],
    }
    return doc


def dump(doc):
    lines = [f"{k}: {json.dumps(doc[k])}" for k in ("about", "tempo", "ceiling", "tail", "patches", "master")]
    lines.append("buses:")
    lines += [f"  {b}: {json.dumps(v)}" for b, v in doc["buses"].items()]
    lines.append("tracks:")
    lines += ["  - " + json.dumps(t) for t in doc["tracks"]]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    open(OUT, "w").write(dump(song()))
    print("wrote", OUT)
