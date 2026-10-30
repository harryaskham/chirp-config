#!/usr/bin/env python3
"""chirpers4-t8 (Phantom Downbeat, track 8) - generator for songs/chirpers4-t8.yaml (chirper-zero).

DEEP DUB TECHNO / "the echo takes the one". 124 bpm 4/4 in D minor. A dub-techno chord stab, thrown into an ECHO ROOM
(chirper-two's feedback routing: every dotted-eighth repeat goes round a low-pass and a tape deck again, darker each
pass) over a four-on-the-floor kick whose tail feeds a pumped RUMBLE bus. Original; a style, not a version of any track.

STREAM SPLIT: through the record the dry stab sinks and its echoes rise, so the dotted-eighth stream becomes the louder
rhythm. In the break the kick drops out and the ear re-hears the echoes as the pulse - a phantom downbeat 3/16 off the
real one - and the kick's return snaps the grid back.

Form (bars): intro 16 (kick, rumble, the sub) / build 16 (the stab enters, hats) / A 32 (the long hypnotic middle) /
break 16 (no kick: the echo stream alone, the hall frozen) / B 32 (the kick slams back) / peak 16 (claps, the ride) /
outro 16.

Motifs (compose/chirpers4/motifs.md):
  THE STAB        a D minor 9 (F3 A3 C4 E4 over D) on the and-of-one, a second on the and-of-three in alternate bars;
                  the voicing mutates by phrase (Dm9 -> Dm11 -> Bbmaj7/D -> Gm9/D).
  FIVE OVER FOUR  the closed hats on every 16th, accented every fifth: the accent walks across the bar and realigns every
                  five bars.
  THE ROOM        the echo bus: delay 3/16 -> low-pass 1.9 kHz -> tape, fed back into itself at 0.74.
Run: python3 compose/chirpers4/src/chirpers4-t8.py  (writes songs/chirpers4-t8.yaml)
"""
import json
import os

ROOT = os.path.expanduser("~/.config/chirp")
OUT = os.environ.get("C4T8_OUT") or os.path.join(ROOT, "songs", "chirpers4-t8.yaml")
BPM = 124
SPB = 60 / BPM
BAR = 4 * SPB
S = 0.25
MG = float(os.environ.get("C4T8_MG", "18"))
ROOMFB = float(os.environ.get("C4T8_ROOMFB", "0.74"))

NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
FORM = [("intro", 16), ("build", 16), ("A", 32), ("break", 16), ("B", 32), ("peak", 16), ("outro", 16)]
VOICINGS = [  # the stab's voicing by 16-bar phrase (over a D in the sub)
    [53, 57, 60, 64],        # Dm9:  F3 A3 C4 E4
    [53, 55, 60, 64],        # Dm11: F3 G3 C4 E4
    [53, 58, 62, 65],        # Bbmaj7/D colour: F3 Bb3 D4 F4
    [55, 58, 62, 65],        # Gm9/D colour: G3 Bb3 D4 F4
]


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


def kit(sec, b, gb):
    """909: the kick on every beat (not in the break), the open hat on every off-beat, closed 16ths accented every fifth."""
    ev = {}

    def add(st, piece, vel):
        ev.setdefault(st, []).append((piece, vel))

    kick = sec not in ("break",) and not (sec == "outro" and b >= 12)
    if kick:
        for st in (0, 4, 8, 12):
            add(st, "k", 118 if st == 0 else 110)
    if sec not in ("intro",) or b >= 8:
        for st in (2, 6, 10, 14):
            add(st, "oh", 74 if sec in ("A", "B", "peak") else 60)
    if sec in ("A", "B", "peak") or (sec == "build" and b >= 8) or (sec == "break" and b >= 8):
        for st in range(16):
            if st in (2, 6, 10, 14):
                continue
            n = gb * 16 + st
            add(st, "h", 96 if n % 5 == 0 else 50)
    if sec in ("A", "B", "peak") and b % 2 == 1:
        add(11, "rs", 70)
    if sec == "peak":
        for st in (4, 12):
            add(st, "cp", 96)
    if sec in ("B", "peak"):
        for st in (2, 6, 10, 14):
            add(st, "rd", 84)
    out = [(st, ",".join(p for p, _ in v), 1, max(vv for _, vv in v)) for st, v in ev.items()]
    return grid(out)


def accents(sec, b, gb):
    """FIVE OVER FOUR made a voice: a metal hat only on every fifth 16th, walking across the bar (realigns every 5 bars)."""
    if not (sec in ("A", "B", "peak") or (sec == "build" and b >= 8)):
        return R(4)
    return grid([(st, "C5", 1, 100 if (gb * 16 + st) % 20 == 0 else 84) for st in range(16) if (gb * 16 + st) % 5 == 0])


def sub(sec, b):
    """The sub on the off-beats (D1), breathing on the kick's pump; out in the break's first half."""
    if sec == "break" and b < 8:
        return R(4)
    if sec == "intro" and b < 4:
        return R(4)
    return grid([(st, "D1", 2, 96 if st == 2 else 84) for st in (2, 6, 10, 14)])


def stab(sec, b, phrase):
    """THE STAB on the and-of-one (and the and-of-three in odd bars)."""
    if sec == "intro" or (sec == "outro" and b >= 12):
        return R(4)
    v = VOICINGS[phrase % len(VOICINGS)]
    ch = ",".join(nm(n) for n in v)
    ev = [(2, ch, 1, 100)]
    if b % 2 == 1:
        ev.append((10, ch, 1, 88))
    return grid(ev)


def build():
    names = ("kit", "sub", "stab", "riser", "acc")
    T = {n: [] for n in names}
    gb = 0
    for sec, nb in FORM:
        for b in range(nb):
            phrase = gb // 16
            T["kit"].append(kit(sec, b, gb))
            T["sub"].append(sub(sec, b))
            T["acc"].append(accents(sec, b, gb))
            T["stab"].append(stab(sec, b, phrase))
            T["riser"].append("C4/4b@84" if (sec in ("build", "break") and b >= nb - 4) else R(4))
            gb += 1
    return T


def lane(points):
    st, total = starts()
    pts = [["0s", points[0][1]]]
    for bar, val in points:
        t = bar * BAR
        if t > 0:
            pts += [[f"{max(0.0, t - 0.05):.3f}s", pts[-1][1]], [f"{t:.3f}s", val]]
    pts.append([f"{total * BAR + 8:.2f}s", pts[-1][1]])
    return {"points": pts}


def song():
    T = build()
    st, total = starts()
    sc = lambda n: " | ".join(T[n])  # noqa: E731
    # STREAM SPLIT: the dry stab sinks and the room's send rises; the break is all room; B restores the dry stab
    dry = [(0, 0), (st["A"], -2), (st["A"] + 16, -5), (st["break"], -14), (st["B"], -2), (st["peak"], -4), (st["outro"], -6)]
    wet = [(0, -8), (st["A"], -6), (st["A"] + 16, -3), (st["break"], 2), (st["B"], -6), (st["peak"], -2), (st["outro"], 0)]
    dyn = [(0, -6), (st["build"], -3), (st["A"], 0), (st["break"], -7), (st["B"], 0), (st["peak"], 1), (st["outro"], -5)]
    frz = [(0, 0), (st["break"] + 2, 1), (st["break"] + 12, 0)]
    pump = lambda d: {"type": "pump", "on": "kit.k", "depth": f"{d}dB", "attack": "4ms", "release": "320ms", "curve": 0.6}  # noqa: E731
    patches = {
        "dub-chord": {"about": "Phantom Downbeat t8: the dub-techno chord - two detuned saws and a pulse through a low-pass that snaps "
                               "open and closes fast, a short stab for the echo room to carry.",
                      "play": {"vel_sens": 0.5},
                      "synth": {"layers": ["saw", "saw detune=9", "pulse width=0.35 level=-6dB"],
                                "env": {"f": {"a": "1ms", "d": "220ms", "s": 0.05, "r": "80ms"}},
                                "filters": [{"kind": "lp", "cutoff": {"value": 420, "mod": [{"src": "env.f", "amount": 3.2}, {"src": "vel", "amount": 1.2}]}, "q": 2.2}],
                                "amp": {"a": "2ms", "d": "300ms", "s": 0, "r": "120ms"}}},
    }
    doc = {
        "about": "Chirpers - Phantom Downbeat (Chirpers IV), track 8 by chirper-zero: DEEP DUB TECHNO, the echo takes the one. "
                 "Generated by compose/chirpers4/src/chirpers4-t8.py; see its docstring and compose/chirpers4/styles.md.",
        "tempo": BPM, "ceiling": "-0.3dB", "tail": "4s", "patches": patches,
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=24", "peak cutoff=40 q=1 gain=-6dB", "peak cutoff=320 q=0.8 gain=-3dB", "peak cutoff=700 q=0.7 gain=-3dB", "highshelf cutoff=2500 gain=11dB"]},
                          {"type": "gain", "gain": f"+{MG:g}dB"},
                          {"type": "drive", "drive": 0.25, "mix": 0.6},
                          {"type": "compressor", "threshold": "-16dB", "ratio": 3, "attack": "10ms", "release": "120ms", "makeup": "2dB"},
                          {"type": "compressor", "threshold": "-6dB", "ratio": 10, "attack": "0.5ms", "release": "40ms", "makeup": "1dB"},
                          {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}}],
                   "auto": {"dyn": lane(dyn)}},
        "buses": {
            "rumble": {"fx": ["reverb kind=hall decay=2.6s size=0.9 mix=1", {"type": "filter", "kind": "lowpass", "cutoff": 170, "q": 0.7},
                              "drive drive=0.35 mix=1", pump(-10)]},
            "room": {"fx": ["delay time=3/16 feedback=0 mix=1 tone=3000", {"type": "filter", "kind": "lowpass", "cutoff": 1900, "q": 0.9},
                            "tape drive=0.2 mix=1 wow=8 flutter=3 drift=1 tone=6000 sweep=0.6 seed=4"],
                     "returns": [{"from": "room", "gain": ROOMFB, "time": "6ms"}]},
            "wash": {"fx": [{"type": "reverb", "kind": "hall", "decay": "5s", "size": 0.95, "mix": 1,
                             "freeze": {"value": 0, "mod": [{"src": "auto.frz", "amount": 1}]}}],
                     "auto": {"frz": lane(frz)}},
        },
        "tracks": [
            {"name": "kit", "patch": "909", "gain": "0dB", "sends": {"rumble": "-4dB"}, "score": sc("kit")},
            {"name": "sub", "patch": "sub-sine", "gain": "-9dB", "fx": [pump(-8)], "score": sc("sub")},
            {"name": "stab", "patch": "dub-chord", "gain": {"value": "-10dB", "mod": [{"src": "auto.dry", "amount": 1}]}, "pan": -0.1,
             "fx": [pump(-6)], "sends": {"room": {"value": "0dB", "mod": [{"src": "auto.wet", "amount": 1}]}, "wash": "-12dB"},
             "auto": {"dry": lane(dry), "wet": lane(wet)}, "score": sc("stab")},
            {"name": "acc", "patch": "haake-hat", "gain": "-2dB", "pan": 0.3, "sends": {"room": "-14dB"}, "score": sc("acc")},
            {"name": "riser", "patch": "fx-riser-shepard", "gain": "-16dB", "sends": {"wash": "-10dB"}, "score": sc("riser")},
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
