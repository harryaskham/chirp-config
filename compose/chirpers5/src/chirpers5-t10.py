#!/usr/bin/env python3
"""chirpers5-t10 (Soft Concrete, track 10, the closer) - generator for songs/chirpers5-t10.yaml (chirper-zero).

EUPHORIC LIQUID CLOSER / "streetlights off". 172 bpm in Db major; the last drop lifts to D. The album ends at dawn: a
big, lifting liquid anthem - piano and strings, a sung wordless hook - whose last drop rises a semitone, then the beat
dissolves and only the piano, the voice and the city's air are left as the streetlights go off. Original; a style, not
a version of any track.

Form (bars): intro 16 (piano and voice, the strings in at 9) / build 8 (the drums under a roll) / A 32 (the anthem) /
breakdown 16 (no drums: piano, strings, the hook) / B 32 (the reese joins) / lift 16 (the last drop, a semitone up) /
dissolve 24 (the drums leave, then the bass; piano, voice, the city's air).

Motifs (compose/chirpers5/motifs.md):
  THE CHANGES  Dbmaj9 | Ab/C | Bbm9 | Gbm(maj9) - a lifting I-V-vi that keeps falling back to its minor sixth, and (v6) a
               borrowed minor iv: the dawn stays bittersweet.
  THE HOOK     the voice: Ab4 . F4 Ab4 Bb4 | Ab4 . Eb4 . | F4 Eb4 Db4 Eb4 | F4 . . . (vowels turning ah, oo, eh, ah).
  THE LIFT     the last drop a semitone up (D major), the album's biggest lift; the dissolve after it its exhale.
Run: python3 compose/chirpers5/src/chirpers5-t10.py  (writes songs/chirpers5-t10.yaml)
"""
import json
import os

ROOT = os.path.expanduser("~/.config/chirp")
OUT = os.environ.get("C5T10_OUT") or os.path.join(ROOT, "songs", "chirpers5-t10.yaml")
BPM = 172
SPB = 60 / BPM
BAR = 4 * SPB
S = 0.25
RECIPE = float(os.environ.get("C5T10_RECIPE", "3"))
RCLIP = os.environ.get("C5T10_RCLIP", "-2.0")
TPLIM = os.environ.get("C5T10_TPLIM", "")  # wM's true-peak limiter (true_peak: true, 4x oversampled, 5 ms lookahead, never clamps) as the master's last stage at this ceiling (dB), instead of the clip and the 16 kHz low-pass
LOWLIFT = os.environ.get("C5T10_LOWLIFT", "7")  # the master's 100 Hz lifted (dB): the liquid bass's body
MIDEQ = os.environ.get("C5T10_MIDEQ", "-3,-4")  # "low,mid": the 300 Hz cut eased to this (dB) and 1 kHz taken down by this
HARMIN = os.environ.get("C5T10_HARMIN", "lift")  # where else the hook's third-above voice sings, besides the interlude: "B" (the second drop and the lift) or "lift" (the lift only)
DESC = os.environ.get("C5T10_DESC", "1") == "1"  # the strings gain a descant in the second drop: the chord's top tones an octave up, falling in half notes
DAWN = int(os.environ.get("C5T10_DAWN", "0"))  # the opening piano heard through the window: a low-pass from about 620 Hz opening to 14 kHz over this many bars

# Harry's Soft Concrete notes (30 Oct, 15:45): swing vs stutter, bass weight, use the toolbox deliberately, a touch darker
SWAG = os.environ.get("C5T10_SWAG", "1") == "1"  # the amen roll swings with the kit (16ths at 0.55): its chops agree with the groove instead of running straight under a swung kit
PHANT = os.environ.get("C5T10_PHANT", "-3")  # the sub's phantom harmonics (dB): its 2nd-6th harmonics mixed in, so the bassline reads on small speakers
REESEMOVE = os.environ.get("C5T10_REESEMOVE", "1") == "1"  # the reese driven (mid harmonics) and its low-pass breathing on a 3-bar LFO, resonance up
BSWEEP = os.environ.get("C5T10_BSWEEP", "1") == "1"  # the build's drums through a high-pass falling from about 1.3 kHz to nothing over its last four bars: the drop opens the floor
KEYMOVE = os.environ.get("C5T10_KEYMOVE", "1") == "1"  # the strings move: a notch swept on a 5-bar LFO and the pan on a 7-bar one
TAPE = os.environ.get("C5T10_TAPE", "1") == "1"  # the pull-out before the lift: piano, strings and voices wind down to a halt over its last two beats (a tape stop), then the lift snaps them back a semitone up
DARK = os.environ.get("C5T10_DARK", "0")  # the master's 6 kHz shelf at this (dB, was +3): more night than dusk
MINORIV = os.environ.get("C5T10_MINORIV", "1") == "1"  # the fourth chord borrowed from the minor: Gbm(maj9) for Gbmaj9 - the iv that keeps the dawn bittersweet
TPON = os.environ.get("C5T10_TPON", "1") == "1"
BLINE = os.environ.get("C5T10_BLINE", "1") == "1"  # a bassline instead of a drone: root, root, the octave on the 2-step kick, the fifth as a pickup - sub and reese together; the reese doubles it from the first drop (darker there)  # true_peak: true (the album's levels rule)

NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
FORM = [("intro", 16), ("build", 8), ("A", 32), ("breakdown", 16), ("B", 32), ("lift", 16), ("dissolve", 24)]
# (bass root, piano/strings voicing) in Db major
CH = [(25, [53, 56, 60, 63, 65]),   # Dbmaj9: F3 Ab3 C4 Eb4 F4 over Db
      (24, [51, 56, 60, 63, 68]),   # Ab/C: Eb3 Ab3 C4 Eb4 Ab4 over C
      (22, [49, 53, 56, 60, 61]),   # Bbm9: Db3 F3 Ab3 C4 Db4 over Bb
      (30, [53, 57, 61, 65, 68] if MINORIV else [53, 58, 61, 65, 68])]   # Gbmaj9: F3 Bb3 Db4 F4 Ab4 over Gb (MINORIV: Gbm(maj9), A3 for Bb3)
HOOK = [[("Ab4", 4), ("F4", 2), ("Ab4", 2), ("Bb4", 4), ("R", 4)],
        [("Ab4", 6), ("Eb4", 6), ("R", 4)],
        [("F4", 3), ("Eb4", 3), ("Db4", 2), ("Eb4", 4), ("R", 4)],
        [("F4", 12), ("R", 4)]]
VOWELS = ["", "^u", "^e", ""]
NOTE = {"C": 0, "Db": 1, "D": 2, "Eb": 3, "E": 4, "F": 5, "Gb": 6, "G": 7, "Ab": 8, "A": 9, "Bb": 10, "B": 11}


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


def up(sec):
    return 1 if sec in ("lift",) or (sec == "dissolve") else 0


DRUMS = ("A", "B", "lift")


def kit(sec, b):
    ev = {}

    def add(st, piece, vel):
        ev.setdefault(st, []).append((piece, vel))

    if sec in DRUMS or (sec == "build" and b >= 4) or (sec == "dissolve" and b < 8):
        add(0, "k", 118)
        add(10, "k", 102)
        add(4, "s", 112)
        add(12, "s", 116)
        for st in range(16):
            add(st, "h", 68 if st % 4 == 2 else (50 if st % 2 else 38))
        if sec == "lift":
            for st in (2, 6, 10, 14):
                add(st, "rd", 80)
            if b % 4 == 3:
                add(14, "s", 90)
                add(15, "s", 100)
    if sec == "breakdown":  # the half-time interlude: kick on one, snare on three, soft
        return grid([(0, "k", 1, 100), (8, "s", 1, 96)] + [(st, "h", 1, 44) for st in (4, 12)])
    if sec == "B" and b == 31:  # the pull-out before the lift: the kit stops after beat two, the riser takes the bar
        return grid([(0, "k", 1, 118), (4, "s", 1, 112)])
    out = [(st, ",".join(p for p, _ in v), 1, max(vv for _, vv in v)) for st, v in ev.items()]
    return grid(out) if out else R(4)


AMEN = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]] * 3 + [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 28, 29, 30, 31, 30, 31]]


def amen(sec, b):
    if not (sec in DRUMS or (sec == "dissolve" and b < 4)):
        return R(4)
    return grid([(st, nm(36 + n), 1, 90 if st % 4 == 0 else 72) for st, n in enumerate(AMEN[b % 4])])


def bass(sec, b, gb):
    root = CH[gb % 4][0] + up(sec)
    if BLINE and sec in DRUMS:
        return grid([(0, nm(root), 6, 104), (6, nm(root), 4, 90), (10, nm(root + 12), 4, 100), (14, nm(root + 7), 2, 92)])
    if sec in DRUMS or (sec == "build" and b >= 6) or (sec == "dissolve" and b < 12):
        return grid([(0, nm(root), 10, 100), (10, nm(root), 6, 90)])
    return R(4)


def reese(sec, b, gb):
    root = CH[gb % 4][0] + up(sec)
    if BLINE and sec in DRUMS:
        v = 96 if sec != "A" else 78
        return grid([(0, nm(root + 12), 6, v), (6, nm(root + 12), 4, v - 8), (10, nm(root + 24), 4, v), (14, nm(root + 19), 2, v - 6)])
    if sec in ("B", "lift"):
        return grid([(0, nm(root + 12), 16, 96)])
    return R(4)


def piano(sec, b, gb):
    v = [n + up(sec) for n in CH[gb % 4][1]]
    ch = ",".join(nm(n) for n in v)
    if sec == "lift":  # the lift rolls: the chord's tones in 16ths up and down, the piano running
        seq = v + v[-2:0:-1]
        return grid([(st, nm(seq[st % len(seq)] + 12), 1, 80 if st % 4 == 0 else 66) for st in range(16)])
    if sec == "dissolve":  # the epilogue: the piano picks out the hook, an octave up, alone
        cell = HOOK[gb % 4]
        toks, st = [], 0
        for n, d in cell:
            if n != "R":
                toks.append((st, nm(12 * (int(n[-1]) + 2) + NOTE[n[:-1]] + up(sec)), d, 64))
            st += d
        return grid(toks)
    if sec in ("intro", "breakdown"):  # broken: the chord rolled up across the bar
        return grid([(st, nm(n), 3, 70 - 2 * k) for k, (st, n) in enumerate(zip((0, 3, 6, 8, 11), v))])
    return grid([(0, ch, 5, 84), (6, ch, 4, 72), (10, ch, 6, 76)])


def strings(sec, b, gb):
    if (sec == "intro" and b < 8) or (sec == "dissolve" and b >= 8):
        return R(4)
    v = [n + up(sec) + (12 if sec in ("lift", "breakdown") else 0) for n in CH[gb % 4][1]]
    vel = {"intro": 46, "build": 52, "A": 56, "breakdown": 64, "B": 58, "lift": 66, "dissolve": 50}[sec]
    if DESC and sec == "B":
        top = sorted(v)[-2:]
        a, c = top[1] + 12, top[0] + 12
        return J(f"{','.join(nm(n) for n in v[1:])},{nm(a)}/2b@{vel}", f"{','.join(nm(n) for n in v[1:])},{nm(c)}/2b@{vel}")
    return f"{','.join(nm(n) for n in v[1:])}/4b@{vel}"


def voice(sec, b, gb):
    if sec == "build" or (sec == "intro" and b < 4) or (sec == "dissolve" and b >= 16):
        return R(4)
    cell = HOOK[gb % 4]
    toks, st = [], 0
    for k, (n, d) in enumerate(cell):
        if n != "R":
            m = 12 * (int(n[-1]) + 1) + NOTE[n[:-1]] + up(sec)
            toks.append((st, nm(m) + VOWELS[(gb + k) % 4], d, 88 if sec in ("lift", "breakdown") else 80))
        st += d
    return grid(toks)


def harmony(sec, b, gb):
    """In the interlude the hook gains a second voice a diatonic third above (Db major)."""
    secs = {"": ("breakdown",), "B": ("breakdown", "B", "lift"), "lift": ("breakdown", "lift")}[HARMIN]
    if sec not in secs:
        return R(4)
    scale = [1, 3, 5, 6, 8, 10, 0]
    cell = HOOK[gb % 4]
    toks, st = [], 0
    for k, (n, d) in enumerate(cell):
        if n != "R":
            m = 12 * (int(n[-1]) + 1) + NOTE[n[:-1]]
            pc = m % 12
            i = scale.index(pc) if pc in scale else 0
            m2 = m + ((scale[(i + 2) % 7] - pc) % 12)
            toks.append((st, nm(m2 + up(sec)) + VOWELS[(gb + k + 1) % 4], d, 72))
        st += d
    return grid(toks)


def air(sec, b):
    return "C4/4b@60" if sec == "dissolve" else R(4)


def riser(sec, b, nb):
    return "C4/4b@84" if ((sec in ("build", "breakdown") and b >= nb - 2) or (sec == "B" and b == nb - 1)) else R(4)


def build():
    names = ("kit", "amen", "bass", "reese", "piano", "strings", "voice", "harmony", "air", "riser")
    T = {n: [] for n in names}
    gb = 0
    for sec, nb in FORM:
        for b in range(nb):
            T["kit"].append(kit(sec, b))
            T["amen"].append(amen(sec, b))
            T["bass"].append(bass(sec, b, gb))
            T["reese"].append(reese(sec, b, gb))
            T["piano"].append(piano(sec, b, gb))
            T["strings"].append(strings(sec, b, gb))
            T["voice"].append(voice(sec, b, gb))
            T["harmony"].append(harmony(sec, b, gb))
            T["air"].append(air(sec, b))
            T["riser"].append(riser(sec, b, nb))
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


def song():
    T = build()
    st, total = starts()
    sc = lambda n, pre="": (pre + " " if pre else "") + " | ".join(T[n])  # noqa: E731
    d1 = st["dissolve"]
    dyn = [(0, -5), (st["build"], -3), (st["A"], 0), (st["breakdown"], -4), (st["B"], 0), (st["lift"], 1), (d1, -2), (d1 + 24, -9)]
    pump = lambda d: {"type": "pump", "on": "kit.k", "depth": f"{d}dB", "attack": "1ms", "release": "230ms", "curve": 0.6}  # noqa: E731
    doc = {
        "about": "Chirpers - Soft Concrete (Chirpers V), track 10 by chirper-zero: EUPHORIC LIQUID CLOSER, streetlights off. Generated "
                 "by compose/chirpers5/src/chirpers5-t10.py; see its docstring and compose/chirpers5/styles.md.",
        "tempo": BPM, "ceiling": "-1dB", "volume": "0dB", **({"true_peak": True} if (TPLIM or TPON) else {}), "tail": "3s",
        "patches": {"city-air": {"about": "Soft Concrete t10: the city at dawn - pink noise, band-passed low, steady.",
                                 "synth": {"layers": [{"type": "noise", "color": "pink"}], "filters": ["bp cutoff=500 q=0.4"],
                                           "amp": {"a": "2s", "s": 1, "r": "2s"}}}},
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=26", "peak cutoff=80 q=0.8 gain=2dB", *([f"peak cutoff=100 q=0.8 gain={LOWLIFT}dB"] if LOWLIFT else []),
                                                   f"peak cutoff=300 q=0.8 gain={MIDEQ.split(',')[0] if MIDEQ else -6}dB",
                                                   *([f"peak cutoff=1000 q=0.8 gain={MIDEQ.split(',')[1]}dB"] if MIDEQ else []), f"highshelf cutoff=6000 gain={DARK or 3}dB"]},
                          {"type": "compressor", "threshold": "-16dB", "ratio": 2, "attack": "10ms", "release": "150ms", "makeup": "0dB"},
                          {"type": "gain", "gain": f"+{RECIPE:g}dB"},
                          {"type": "compressor", "threshold": "-5dB", "ratio": 10, "attack": "0.3ms", "release": "60ms", "makeup": "0dB"},
                          {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                          *([f"limiter ceiling={TPLIM}dB release=80ms"] if TPLIM else
                            [{"type": "clip", "ceiling": f"{RCLIP}dB", "knee": 0.8, "link": True},
                             {"type": "filter", "kind": "lowpass", "cutoff": 16000, "q": 0.5}])],
                   "auto": {"dyn": lane(dyn, {d1 + 24})}},
        "buses": {
            "drums": {"fx": ([{"type": "filter", "kind": "hp", "cutoff": {"value": 20, "mod": [{"src": "auto.bs", "amount": 6}]}, "q": 0.7}] if BSWEEP else []) +
                            [{"type": "compressor", "threshold": "-16dB", "ratio": 4, "attack": "1ms", "release": "80ms", "makeup": "0dB"},
                             {"type": "clip", "ceiling": "-11dB", "knee": 0.7, "link": True}],
                      **({"auto": {"bs": lane([(0, 0), (st["build"] + 4, 1), (st["A"], 0)], {st["A"]})}} if BSWEEP else {})},
            **({"keys": {"fx": [{"type": "tapestop", "stop": {"value": 0, "mod": [{"src": "auto.ts", "amount": 1}]}, "time": "2b", "curve": 1.6}],
                         "auto": {"ts": lane([(0, 0), (st["lift"] - 0.5, 1), (st["lift"], 0)])}}} if TAPE else {}),
            "hall": {"fx": ["reverb kind=hall decay=3.2s size=0.9 mix=1 predelay=24ms"]},
            "echo": {"fx": ["delay time=3/8 feedback=0.35 mix=1 tone=3500"]},
        },
        "tracks": [
            {"name": "kit", "patch": "machine-kit", "gain": "-2dB", "out": "drums",
             "fx": [{"type": "drive", "drive": 0.5, "mix": 1}, {"type": "compressor", "threshold": "-14dB", "ratio": 6, "attack": "0.3ms", "release": "60ms", "makeup": "3dB"}],
             "score": sc("kit", "swing16=0.55")},
            {"name": "amen", "patch": "amen-chops", "gain": "-13dB", "out": "drums", "fx": [{"type": "filter", "kind": "highpass", "cutoff": 400, "q": 0.7}],
             "score": sc("amen", "swing16=0.55" if SWAG else "")},
            {"name": "sub", "patch": "sub-sine", "gain": "1dB", "fx": [pump(-6)] + ([{"type": "phantom", "cutoff": 100, "harmonics": f"{PHANT}dB"}] if PHANT else []), "score": sc("bass")},
            {"name": "reese", "patch": "reese", "gain": "-8dB",
             "fx": [pump(-6)] + ([{"type": "drive", "drive": 0.35, "mix": 0.6}, {"type": "filter", "kind": "lowpass", "cutoff": {"value": 1100, "mod": [{"src": "lfo.r", "amount": 0.7}]}, "q": 2}]
                                 if REESEMOVE else [{"type": "filter", "kind": "lowpass", "cutoff": 1200, "q": 1}]),
             **({"lfo": {"r": "sine rate=3/1"}} if REESEMOVE else {}), "score": sc("reese")},
            {"name": "piano", "patch": "piano-recorded", "gain": "-6dB", "pan": -0.1,
             "fx": [pump(-4)] + ([{"type": "filter", "kind": "lowpass", "cutoff": {"value": 14000, "mod": [{"src": "auto.pf", "amount": -4.5}]}, "q": 0.7}] if DAWN else []),
             **({"auto": {"pf": lane([(0, 1), (DAWN, 0)], {DAWN})}} if DAWN else {}),
             "sends": {"hall": "-12dB"}, "score": sc("piano")},
            {"name": "strings", "patch": "strings-synth", "gain": "-12dB", "pan": 0.1,
             "fx": [pump(-5)] + ([{"type": "filter", "kind": "notch", "cutoff": {"value": 1000, "mod": [{"src": "lfo.n", "amount": 1.2}]}, "q": 1.2},
                                  {"type": "pan", "pan": {"value": 0.1, "mod": [{"src": "lfo.p", "amount": 0.35}]}}] if KEYMOVE else []),
             **({"lfo": {"n": "sine rate=5/1", "p": "sine rate=7/1"}} if KEYMOVE else {}), "sends": {"hall": "-8dB"}, "score": sc("strings")},
            {"name": "voice", "patch": "voice", "gain": "-7dB", "pan": 0.05, "sends": {"hall": "-6dB", "echo": "-14dB"}, "score": sc("voice")},
            {"name": "harmony", "patch": "voice", "gain": "-11dB", "pan": -0.25, "sends": {"hall": "-4dB"}, "score": sc("harmony")},
            {"name": "air", "patch": "city-air", "gain": "-26dB", "sends": {"hall": "-10dB"}, "score": sc("air")},
            {"name": "riser", "patch": "fx-riser-noise", "gain": "-16dB", "sends": {"hall": "-10dB"}, "score": sc("riser")},
        ],
    }
    if TAPE:
        for t in doc["tracks"]:
            if t["name"] in ("piano", "strings", "voice", "harmony"):
                t["out"] = "keys"
    return doc


def dump(doc):
    lines = [f"{k}: {json.dumps(doc[k])}" for k in ("about", "tempo", "ceiling", "volume", "true_peak", "tail", "patches", "master") if k in doc]
    lines.append("buses:")
    lines += [f"  {b}: {json.dumps(v)}" for b, v in doc["buses"].items()]
    lines.append("tracks:")
    lines += ["  - " + json.dumps(t) for t in doc["tracks"]]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    open(OUT, "w").write(dump(song()))
    print("wrote", OUT)
