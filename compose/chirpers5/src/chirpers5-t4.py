#!/usr/bin/env python3
"""chirpers5-t4 (Soft Concrete, track 4) - generator for songs/chirpers5-t4.yaml (chirper-zero).

LIQUID GLITCHSTEP / "hairline". 174 bpm in G minor. A soulful liquid roller that keeps cracking: glitchstep fractures
(buffer stutters whose repeats ramp up in pitch, drum rolls accelerating to 1/64) at its seams, and a half-time
glitchstep middle where the roller falls through the crack and climbs back out. Original; a style, not a version of
any track.

Form (bars): intro 16 (the pad, the Rhodes, the voice; the amen filtered far away) / build 8 (the drums arrive under a
roll) / A 32 (the roller: 2-step kick and snare over the amen ghost roll, reese and sub) / half 16 (half-time
glitchstep: the snare on 3, the stutters in charge) / B 32 (the roller back, the voice answering) / climax 16 (every
other bar cracks) / outro 16.

Motifs (compose/chirpers5/motifs.md):
  THE CHANGES   Gm9 | Ebmaj9 | Cm11 | D7sus4 (b9 colour), one chord a bar, Rhodes stabs on 1 and the and-of-2.
  THE VOICE     wordless chops on chord tones (9th, 5th, 3rd), vowels turning ah-oo-eh, falling after the snare.
  THE HAIRLINE  each 8-bar phrase cracks on its last half-bar: a buffer stutter whose repeats rise in pitch.
Run: python3 compose/chirpers5/src/chirpers5-t4.py  (writes songs/chirpers5-t4.yaml)
"""
import json
import os

ROOT = os.path.expanduser("~/.config/chirp")
OUT = os.environ.get("C5T4_OUT") or os.path.join(ROOT, "songs", "chirpers5-t4.yaml")
BPM = 174
SPB = 60 / BPM
BAR = 4 * SPB
S = 0.25
MG = float(os.environ.get("C5T4_MG", "20"))
LIMG = os.environ.get("C5T4_LIMG", "")
DBUS = os.environ.get("C5T4_DBUS", "0") == "1"
LUSH = os.environ.get("C5T4_LUSH", "1") == "1"
MCOMP = os.environ.get("C5T4_MCOMP", "")
CEIL = os.environ.get("C5T4_CEIL", "-1dB")
KITCOMP = os.environ.get("C5T4_KITCOMP", "1") == "1"
BASSOUT = os.environ.get("C5T4_BASSOUT", "1") == "1"
KITDRIVE = os.environ.get("C5T4_KITDRIVE", "0.5")
TRIM = os.environ.get("C5T4_TRIM", "")
SOFTCLIP = os.environ.get("C5T4_SOFTCLIP", "")
KIT = os.environ.get("C5T4_KIT", "machine-kit")
KITCLIP = os.environ.get("C5T4_KITCLIP", "")
MCLIP = os.environ.get("C5T4_MCLIP", "0")
RECIPE = os.environ.get("C5T4_RECIPE", "8")
VOL0 = os.environ.get("C5T4_VOL0", "1") == "1"
RLIM = os.environ.get("C5T4_RLIM", "-1.5")
RREL = os.environ.get("C5T4_RREL", "80ms")
RCLIP = os.environ.get("C5T4_RCLIP", "-2.8")
TOPLP = os.environ.get("C5T4_TOPLP", "16000")  # a gentle low-pass after the final clip (Hz): the clip's sharp corners are what overshoot between samples  # the recipe's last stage as a soft-knee clip (ceiling dB) instead of the limiter: rounded, never pinned  # the safety limiter's release  # the recipe's safety limiter ceiling (dB): low enough that the inter-sample peaks stay under -1 dBTP  # the song's volume at 0 dB (the default leaves ~3 dB of headroom below the ceiling unused)  # chirper-two's Overpass Rain levels recipe (the album's -12.5 LUFS target): the drums bus compressed (-16 dB, 4:1, 1 ms) then soft-clipped at -11 dB; the master a glue, then this many dB into a fast compressor (-5 dB, 10:1, 0.3 ms), then a -1.5 dB limiter as a net  # a soft-knee clip at the end of the master (ceiling dB) that rounds the compressors' transient overshoots below the song ceiling, so the engine's hard clamp never acts  # "ceiling,makeup": the kit's clicks rounded by a soft-knee clip on its own track (stereo-linked), then made up - the transient that set the master's peak is gone, the body stays  # the 2-step kit (machine-kit's clicks spike ~6 dB over the mix; 909 is rounder)  # a soft clip (drive, full mix) at the end of the master: spikes the compressors are too slow for are rounded, not clamped  # a final trim (dB) so the master never meets the engine's hard ceiling (no clamp, no inter-sample overs) until the limiter fix lands  # the kick's click rounded by a soft drive on the kit (amount), before its compressor  # the bass out of the kick's way: the sub back at -8 dB and the pumps duck in 1 ms (the kick and the bass onsets were summing into the ceiling)  # the kit's click tamed at the source: a fast compressor on the kick and snare (0.3 ms attack), so the master never meets its ceiling  # the song ceiling (-2 dB leaves room for inter-sample peaks: true peak <= -1 dBTP)  # the master's body raised: a slow glue (-24 dB, 3:1, 30 ms) then the fast peak stage with this much makeup (dB)  # the sustained parts up (pad +5, reese and sub +4, Rhodes +3, voice +2): the liquid fullness carries the loudness, the drums keep their transients  # the drums glued and rounded on their bus (a soft drive and a firmer compressor) so the master is loud without a limiter pinning the kick

NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
FORM = [("intro", 16), ("build", 8), ("A", 32), ("half", 16), ("B", 32), ("climax", 16), ("outro", 16)]
# (root for the bass, Rhodes voicing, voice tones (9th, 5th, 3rd) an octave up)
CH = [(31, [50, 53, 57, 58, 62], [69, 62, 58]),      # Gm9: D3 F3 A3 Bb3 D4 over G
      (27, [51, 55, 58, 62, 65], [65, 58, 55]),      # Ebmaj9: Eb3 G3 Bb3 D4 F4
      (24, [51, 55, 58, 62, 65], [62, 55, 51]),      # Cm11: Eb3 G3 Bb3 D4 F4 over C
      (26, [50, 55, 57, 60, 63], [64, 57, 54])]      # D7sus4 b9: D3 G3 A3 C4 Eb4


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
        note, _, art = head.partition("^")
        out.append(f"{note}/{ln * S:g}b@{int(vel)}" + (f"^{art}" if art else ""))
        pos = st + ln
    out.append(R((steps - pos) * S))
    return J(*out)


def starts():
    t, out = 0, {}
    for sec, nb in FORM:
        out[sec] = t
        t += nb
    return out, t


ROLLER = ("A", "B", "climax")


def kit(sec, b):
    ev = {}

    def add(st, piece, vel):
        ev.setdefault(st, []).append((piece, vel))

    if sec in ROLLER or (sec == "build" and b >= 4) or (sec == "outro" and b < 8):
        add(0, "k", 118)
        add(10, "k", 104)
        add(4, "s", 112)
        add(12, "s", 116)
        for st in range(16):
            add(st, "h", 70 if st % 4 == 2 else (52 if st % 2 else 40))
    elif sec == "half":
        add(0, "k", 116)
        add(8, "s", 118)
        if b % 2 == 1:
            add(11, "k", 96)
        for st in range(0, 16, 2):
            add(st, "h", 60 if st % 4 == 2 else 42)
    out = [(st, ",".join(p for p, _ in v), 1, max(vv for _, vv in v)) for st, v in ev.items()]
    return grid(out) if out else R(4)


AMEN = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 26, 27, 28, 29, 30, 31]]


def amen(sec, b):
    """The amen ghost roll: re-sequenced 16ths (the fourth bar of each four turns to the break's tail)."""
    if sec in ("intro", "half") or (sec == "outro" and b >= 12) or (sec == "build" and b < 2):
        if sec == "intro" and b >= 8:
            pass
        else:
            return R(4)
    seq = AMEN[b % 4]
    return grid([(st, nm(36 + n), 1, 92 if st % 4 == 0 else 76) for st, n in enumerate(seq)])


def bass(sec, b, gb):
    root = CH[gb % 4][0]
    if sec in ROLLER or (sec == "build" and b >= 6):
        return grid([(0, nm(root), 10, 100), (10, nm(root), 6, 92)])
    if sec == "half":
        return grid([(0, nm(root), 16, 96)])
    return R(4)


def rhodes(sec, b, gb):
    v = CH[gb % 4][1]
    ch = ",".join(nm(n) for n in v)
    if sec == "outro" and b >= 12:
        return R(4)
    if sec in ("intro", "half"):
        return grid([(0, ch, 12, 70)])
    return grid([(0, ch, 5, 86), (6, ch, 6, 74)])


def pad(sec, b, gb):
    v = CH[gb % 4][1]
    vel = {"intro": 56, "build": 52, "A": 44, "half": 60, "B": 44, "climax": 48, "outro": 54}[sec]
    return f"{','.join(nm(n) for n in v)}/4b@{vel}"


VOWELS = ["", "^u", "^e"]


def voice(sec, b, gb):
    """THE VOICE: the falling cell after each snare (the 9th, 5th, 3rd), vowels turning."""
    if sec in ("build",) or (sec == "intro" and b < 8) or (sec == "outro" and b >= 8):
        return R(4)
    tones = CH[gb % 4][2]
    starts_ = (5, 7, 14) if sec != "half" else (9, 11, 14)
    return grid([(st, nm(t) + VOWELS[(gb + k) % 3], 2 if k == 2 else 1, 84 - 6 * k) for k, (st, t) in enumerate(zip(starts_, tones))])


def build():
    names = ("kit", "amen", "bass", "rhodes", "pad", "voice", "riser")
    T = {n: [] for n in names}
    gb = 0
    for sec, nb in FORM:
        for b in range(nb):
            T["kit"].append(kit(sec, b))
            T["amen"].append(amen(sec, b))
            T["bass"].append(bass(sec, b, gb))
            T["rhodes"].append(rhodes(sec, b, gb))
            T["pad"].append(pad(sec, b, gb))
            T["voice"].append(voice(sec, b, gb))
            T["riser"].append("C4/4b@84" if (sec in ("build", "half") and b >= nb - 2) else R(4))
            gb += 1
    return T


def lane(points, ramp=None):
    st, total = starts()
    pts = [["0s", points[0][1]]]
    for bar, val in points:
        t = bar * BAR
        if t <= 0:
            continue
        if ramp and bar in ramp:
            pts.append([f"{t:.3f}s", val])
        else:
            pts += [[f"{max(0.0, t - 0.03):.3f}s", pts[-1][1]], [f"{t:.3f}s", val]]
    pts.append([f"{total * BAR + 8:.2f}s", pts[-1][1]])
    return {"points": pts}


def cracks():
    """THE HAIRLINE: the stutter's mix lane - on for the last half-bar of every 8-bar phrase in the roller sections and the
    build; in the climax every other bar; the half-time middle cracks every 4 bars."""
    st, total = starts()
    on = []
    for sec, nb in FORM:
        a = st[sec]
        if sec in ("A", "B", "build"):
            on += [a + p + 7.5 for p in range(0, nb, 8)]
        elif sec == "climax":
            on += [a + p + 0.5 for p in range(1, nb, 2)]
        elif sec == "half":
            on += [a + p + 3.5 for p in range(0, nb, 4)]
    pts = []
    for x in sorted(on):
        pts += [(x, 1), (x + 0.5, 0)]
    return lane([(0, 0)] + pts)


def song():
    T = build()
    st, total = starts()
    sc = lambda n, pre="": (pre + " " if pre else "") + " | ".join(T[n])  # noqa: E731
    dyn = [(0, -5), (st["build"], -3), (st["A"], 0), (st["half"], -3), (st["B"], 0), (st["climax"], 1), (st["outro"], -4)]
    pump = lambda d: {"type": "pump", "on": "kit.k", "depth": f"{d}dB", "attack": "1ms" if BASSOUT else "4ms", "release": "230ms", "curve": 0.6}  # noqa: E731
    stutter = {"type": "stutter", "slice": "1/16", "repeats": 7, "chance": 1, "roll": 0.7, "floor": "1/64", "pitch": 1.5,
               "decay": 0.05, "seed": 4, "mix": {"value": 0, "mod": [{"src": "auto.crk", "amount": 1}]}}
    doc = {
        "about": "Chirpers - Soft Concrete (Chirpers V), track 4 by chirper-zero: LIQUID GLITCHSTEP, hairline. Generated by "
                 "compose/chirpers5/src/chirpers5-t4.py; see its docstring and compose/chirpers5/styles.md.",
        "tempo": BPM, "ceiling": CEIL, **({"volume": "0dB"} if VOL0 else {}), "tail": "2s",
        "patches": {"rhodes-damped": {"about": "Soft Concrete t4: the physical tine Rhodes with the damper's key-off (release triggers).",
                                      "extends": "epiano-tine", "play": {"release": {"patch": "epiano-damper", "decay": "2s", "gain": "3dB"}}}},
        "master": ({"fx": [{"type": "eq", "bands": ["highpass cutoff=26", "peak cutoff=45 q=1 gain=-3dB", "peak cutoff=300 q=0.8 gain=-3dB", "highshelf cutoff=6000 gain=3dB"]},
                           {"type": "compressor", "threshold": "-16dB", "ratio": 2, "attack": "10ms", "release": "150ms", "makeup": "0dB"},
                           {"type": "gain", "gain": f"+{float(RECIPE):g}dB"},
                           {"type": "compressor", "threshold": "-5dB", "ratio": 10, "attack": "0.3ms", "release": "60ms", "makeup": "0dB"},
                           {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                           ({"type": "clip", "ceiling": f"{RCLIP}dB", "knee": 0.8, "link": True} if RCLIP else f"limiter ceiling={RLIM}dB release={RREL}"),
                           *([{"type": "filter", "kind": "lowpass", "cutoff": float(TOPLP), "q": 0.5}] if TOPLP else [])],
                    "auto": {"dyn": lane(dyn)}} if RECIPE else
                   {"fx": [{"type": "eq", "bands": ["highpass cutoff=26", "peak cutoff=45 q=1 gain=-3dB", "peak cutoff=300 q=0.8 gain=-3dB", "highshelf cutoff=6000 gain=3dB"]},
                          {"type": "gain", "gain": f"+{MG:g}dB"},
                          ({"type": "compressor", "threshold": "-24dB", "ratio": 3, "attack": "30ms", "release": "200ms", "makeup": "4dB"} if MCOMP else
                           {"type": "compressor", "threshold": "-16dB", "ratio": 3, "attack": "10ms", "release": "120ms", "makeup": "2dB"}),
                          ({"type": "compressor", "threshold": "-10dB", "ratio": 8, "attack": "0.5ms", "release": "50ms", "makeup": "1dB"} if DBUS else
                           {"type": "compressor", "threshold": "-8dB", "ratio": 6, "attack": "1ms", "release": "60ms", "makeup": f"{MCOMP or 1}dB"}),
                          {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                          *([{"type": "gain", "gain": f"{float(LIMG):+g}dB"}, "limiter ceiling=-1.5dB release=80ms"] if LIMG else []),
                          *([{"type": "drive", "drive": float(SOFTCLIP), "mix": 1}] if SOFTCLIP else []),
                          *([{"type": "clip", "ceiling": f"{MCLIP}dB", "knee": 0.6, "link": True}] if MCLIP else []),
                          *([{"type": "gain", "gain": f"{float(TRIM):+g}dB"}] if TRIM else [])],
                   "auto": {"dyn": lane(dyn)}}),
        "buses": {
            "drums": {"fx": [stutter] + ([{"type": "compressor", "threshold": "-16dB", "ratio": 4, "attack": "1ms", "release": "80ms", "makeup": "0dB"},
                                          {"type": "clip", "ceiling": "-11dB", "knee": 0.7, "link": True}] if RECIPE else []) + ([] if RECIPE else ([{"type": "drive", "drive": 0.3, "mix": 0.5},
                                          {"type": "compressor", "threshold": "-20dB", "ratio": 4, "attack": "3ms", "release": "80ms", "makeup": "4dB"}] if DBUS else
                                         [{"type": "compressor", "threshold": "-14dB", "ratio": 3, "attack": "5ms", "release": "90ms", "makeup": "2dB"}])),
                      "auto": {"crk": cracks()}},
            "hall": {"fx": ["reverb kind=hall decay=2.8s size=0.85 mix=1 predelay=20ms"]},
            "echo": {"fx": ["delay time=3/16 feedback=0.4 mix=1 tone=3000"]},
        },
        "tracks": [
            {"name": "kit", "patch": KIT, "gain": "-2dB", "out": "drums",
             **({"fx": [{"type": "clip", "ceiling": f"{KITCLIP.split(',')[0]}dB", "knee": 0.6, "link": True},
                        {"type": "gain", "gain": f"+{KITCLIP.split(',')[1]}dB"}]} if KITCLIP else {}),
             **({"fx": ([{"type": "drive", "drive": float(KITDRIVE), "mix": 1}] if KITDRIVE else [])
                        + [{"type": "compressor", "threshold": "-14dB", "ratio": 6, "attack": "0.3ms", "release": "60ms", "makeup": "3dB"}]} if KITCOMP else {}),
             "score": sc("kit", "swing16=0.56")},
            {"name": "amen", "patch": "amen-chops", "gain": "-12dB", "out": "drums", "fx": [{"type": "filter", "kind": "highpass", "cutoff": 350, "q": 0.7}],
             "score": sc("amen")},
            {"name": "bass", "patch": "reese", "gain": "-5dB" if LUSH else "-9dB", "fx": [pump(-6), {"type": "filter", "kind": "lowpass", "cutoff": 900, "q": 1.2}], "score": sc("bass")},
            {"name": "sub", "patch": "sub-sine", "gain": "-4dB" if (LUSH and not BASSOUT) else "-8dB", "fx": [pump(-6)], "score": sc("bass")},
            {"name": "rhodes", "patch": "rhodes-damped", "gain": "-5dB" if LUSH else "-8dB", "pan": -0.15, "fx": [pump(-4)], "sends": {"hall": "-12dB"}, "score": sc("rhodes")},
            {"name": "pad", "patch": "juno-pad", "gain": "-11dB" if LUSH else "-16dB", "fx": [pump(-6)], "sends": {"hall": "-8dB"}, "score": sc("pad")},
            {"name": "voice", "patch": "voice", "gain": "-8dB" if LUSH else "-10dB", "pan": 0.2, "sends": {"hall": "-6dB", "echo": "-12dB"}, "score": sc("voice")},
            {"name": "riser", "patch": "fx-riser-noise", "gain": "-16dB", "sends": {"hall": "-10dB"}, "score": sc("riser")},
        ],
    }
    return doc


def dump(doc):
    lines = [f"{k}: {json.dumps(doc[k])}" for k in ("about", "tempo", "ceiling", "volume", "tail", "patches", "master") if k in doc]
    lines.append("buses:")
    lines += [f"  {b}: {json.dumps(v)}" for b, v in doc["buses"].items()]
    lines.append("tracks:")
    lines += ["  - " + json.dumps(t) for t in doc["tracks"]]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    open(OUT, "w").write(dump(song()))
    print("wrote", OUT)
