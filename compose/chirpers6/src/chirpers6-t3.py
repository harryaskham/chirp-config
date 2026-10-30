#!/usr/bin/env python3
"""chirpers6-t3 (All the Lights Left On, track 3) - generator for songs/chirpers6-t3.yaml (chirper-zero).

INSTRUMENTAL POST-METAL / "night freight". 132 bpm, B minor in drop-tuned guitars (the heaviest movement down in A).
A freight train crosses the album at night, and the wheels' clack over the rail joints becomes the riff's odd meter:
7/8 (the wheels) against 4/4 (the crescendo). Riff-led, heavy/light, no singer. Original; a style, not a version of
any track.

Form (bars, meter): I CROSSING 32 x 7/8 (a level-crossing bell, the freight approaching: rumble, wheel clacks in 7, a
three-tone horn that drops as it passes) / II JOINTS 40 x 7/8 (a clean 8-string arpeggio riff on the clack rhythm,
fretless bass, rims and toms) / III CHUG 64 x 7/8 (the riff drop-tuned on doubled rigs, fuzz bass, a room kit; a
tremolo-picked lead on top in the second half) / IV YARD 32 x 4/4 (the train gone: wind, distant metal, a cello drone,
an ebow sings the line augmented) / V CLIMB 48 x 4/4 (toms to full kit, the clean riff stretched to 4/4, then tremolo
walls; the bass walks the riff inverted) / VI DERAILED 40 x 4/4 (half-time doom in A: china, sub, and the wheels' 7
returning against the 4 - the train comes back) / VII LAST CAR 32 x 7/8 (the clean riff alone with the bell, the train
receding, wind).

Motifs (compose/chirpers6/motifs.md):
  THE JOINTS   the wheels' clack - clack-clack ... clack-clack on a 14-sixteenth cycle - and the 2+2+3 riff built on it.
  THE CHANGES  Bm(add9) | Gmaj7 | D(add9) | A(add9), two 7/8 bars (or one 4/4 bar pair) each.
  THE LINE     F#4 | D4 E4 | A4 | C#5 B4 - tremolo-picked in the chug, augmented on the ebow in the yard.
Run: python3 compose/chirpers6/src/chirpers6-t3.py  (writes songs/chirpers6-t3.yaml)
"""
import json
import os

ROOT = os.path.expanduser("~/.config/chirp")
OUT = os.environ.get("C6T3_OUT") or os.path.join(ROOT, "songs", "chirpers6-t3.yaml")
BPM = 132
S = 0.25  # beats per sixteenth
MGAIN = float(os.environ.get("C6T3_MGAIN", "5"))

NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
SEVEN, FOUR = 14, 16
FORM = [("crossing", 32, SEVEN), ("joints", 40, SEVEN), ("chug", 64, SEVEN), ("yard", 32, FOUR),
        ("climb", 48, FOUR), ("derailed", 40, FOUR), ("lastcar", 32, SEVEN)]
# (heavy root, clean voicing): B minor
CH = [(35, [47, 54, 61, 62, 66, 71]),   # Bm(add9): B2 F#3 C#4 D4 F#4 B4
      (31, [43, 50, 54, 57, 59, 62]),   # Gmaj7(9): G2 D3 F#3 A3 B3 D4
      (38, [50, 57, 62, 64, 66, 69]),   # D(add9): D3 A3 D4 E4 F#4 A4
      (33, [45, 52, 57, 59, 61, 64])]   # A(add9): A2 E3 A3 B3 C#4 E4
LINE = [[("F#4", 28)], [("D4", 14), ("E4", 14)], [("A4", 28)], [("C#5", 14), ("B4", 14)]]
NOTE = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9,
        "A#": 10, "Bb": 10, "B": 11}
TRACKS = ("bell", "rumble", "clack", "horn", "wind", "clean", "fretless", "chugl", "chugr", "fuzz", "sub", "kit", "lead",
          "cello", "ebow", "yardmetal")


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def midi(n):
    return 12 * (int(n[-1]) + 1) + NOTE[n[:-1]]


def R(d):
    return f"R/{d:g}b" if d > 1e-9 else ""


def J(*xs):
    return " ".join(x for x in xs if x)


def grid(events, steps):
    ev = sorted(events)
    out, pos = [], 0
    for i, (st, head, ln, vel) in enumerate(ev):
        if st < pos or st >= steps:
            continue
        nxt = ev[i + 1][0] if i + 1 < len(ev) else steps
        ln = max(1, min(ln, nxt - st, steps - st))
        out.append(R((st - pos) * S))
        note, _, art = head.partition("^")
        out.append(f"{note}/{ln * S:g}b@{int(vel)}" + (f"^{art}" if art else ""))
        pos = st + ln
    out.append(R((steps - pos) * S))
    return J(*out)


def layout():
    """[(section, bar-in-section, bar steps, absolute start step)] for every bar."""
    bars, t = [], 0
    for sec, nb, steps in FORM:
        for b in range(nb):
            bars.append((sec, b, steps, t))
            t += steps
    return bars, t


def sec_start(name):
    t = 0
    for sec, nb, steps in FORM:
        if sec == name:
            return t
        t += nb * steps
    raise KeyError(name)


def chord_of(sec, b, steps):
    """One chord per two bars."""
    return CH[(b // 2) % 4]


def build():
    bars, total = layout()
    ev = {k: [] for k in TRACKS}  # absolute (step, head, len, vel)

    def add(tr, at, head, ln, vel):
        ev[tr].append((at, head, ln, vel))

    # THE JOINTS: the wheels' clacks on a 14-step cycle, wherever the train is (independent of the bars)
    def clacks(a, b, v0, v1):
        n = b - a
        for t in range(a, b):
            ph = (t - a) % 14
            if ph in (0, 2, 8, 10):
                v = v0 + (v1 - v0) * (t - a) / max(1, n)
                add("clack", t, "C4" if ph in (0, 8) else "D4", 1, v * (1.0 if ph in (0, 8) else 0.8))

    s1 = sec_start("crossing")
    clacks(s1 + 12 * 14, sec_start("joints") + 16 * 14, 40, 112)  # approaching, passing, still rattling past
    s6 = sec_start("derailed")
    clacks(s6 + 16 * 16, sec_start("lastcar"), 70, 118)  # the train comes back: 7 against the 4
    s7 = sec_start("lastcar")
    clacks(s7, s7 + 16 * 14, 70, 20)  # the last car receding

    for sec, b, steps, at in bars:
        r, v = chord_of(sec, b, steps)
        ln = steps * S

        def put(tr, head, vel, st=0, l=None):
            add(tr, at + st, head, steps - st if l is None else l, vel)

        # --- field sounds
        if (sec == "crossing" and b < 24) or (sec == "lastcar" and 4 <= b < 20):
            for q in range(0, steps, 4):
                add("bell", at + q, "E5", 2, 72 if sec == "crossing" else 50)
        if sec == "crossing" and b == 8:
            add("rumble", at, "C3", 24 * 14, 100)  # the freight's rumble, held across the crossing
        if sec == "lastcar" and b == 0:
            add("rumble", at, "C3", 20 * 14, 70)
        if sec == "crossing" and b in (18, 20):
            put("horn", "F#4,A4,C#5", 96, 0, 14 + 7)  # the horn, three tones
        if sec == "crossing" and b == 22:
            put("horn", "F4,G#4,C5", 84, 0, 14 + 10)  # passing: the doppler drop
        if sec == "lastcar" and b == 6:
            put("horn", "E4,G4,B4", 54, 0, 21)  # far away now
        if (sec == "crossing" and b == 0) or (sec == "yard" and b == 0) or (sec == "lastcar" and b == 12):
            nb = {"crossing": 32, "yard": 32, "lastcar": 20}[sec]
            add("wind", at, "C4", nb * steps, 70 if sec != "crossing" else 50)

        # --- the clean riff (THE JOINTS): 7 eighths, 2+2+3
        if sec in ("joints", "lastcar") or (sec == "crossing" and b >= 24) or (sec == "chug" and b < 8):
            idx = [0, 2, 3, 1, 4, 2, 5] if b % 2 == 0 else [0, 2, 3, 1, 4, 3, 2]
            for k, i in enumerate(idx):
                acc = k in (0, 2, 4)
                vel = (82 if acc else 66) - (20 if sec == "crossing" else 0) - (14 if (sec == "lastcar" and b >= 24) else 0)
                add("clean", at + 2 * k, nm(v[i]), 2, vel)
        if sec == "climb" and b < 16:  # stretched to 4/4: eight eighths
            idx = [0, 2, 3, 1, 4, 2, 5, 3]
            for k, i in enumerate(idx):
                add("clean", at + 2 * k, nm(v[i]), 2, 80 if k % 2 == 0 else 64)

        # --- bass
        if sec == "joints" or (sec == "lastcar" and 8 <= b < 24):
            for st, l in ((0, 4), (4, 4), (8, 6)):
                add("fretless", at + st, nm(r + 12), l, 88 if st == 0 else 74)
        if sec == "yard":
            if b % 2 == 0:
                put("cello", f"{nm(r + 12)},{nm(r + 19)}", 70, 0, 32)
        if sec == "chug" or (sec == "climb" and b >= 16):
            if steps == SEVEN:
                for st, l in ((0, 2), (2, 2), (4, 2), (6, 2), (8, 6)):
                    add("fuzz", at + st, nm(r + 12), l, 100 if st in (0, 8) else 82)
            else:  # the climb: the riff inverted - the bass walks down where the clean riff went up
                walk = [r + 12, r + 10, r + 7, r + 5]
                for k, n in enumerate(walk):
                    add("fuzz", at + 4 * k, nm(n), 4, 98 if k == 0 else 84)
        if sec in ("chug",) or (sec == "climb" and b >= 32):
            put("sub", nm(r), 90)
        if sec == "derailed":
            put("sub", nm(DOOM[b % 4][0]), 96)

        # --- the heavy rigs
        if sec == "chug":
            pc = lambda n: f"{nm(n)},{nm(n + 7)},{nm(n + 12)}"  # noqa: E731
            for st in (0, 1, 2, 4, 5, 6):
                add("chugl", at + st, nm(r) + "^pm", 1, 104 if st in (0, 4) else 92)
                add("chugr", at + st, nm(r) + "^pm", 1, 102 if st in (0, 4) else 90)
            add("chugl", at + 8, pc(r), 6, 118)
            add("chugr", at + 8, pc(r), 6, 116)
        if sec == "climb" and b >= 16:  # tremolo walls: power chords picked in 16ths
            pc = f"{nm(r)},{nm(r + 7)},{nm(r + 12)}"
            vel = 80 + (b - 16)
            add("chugl", at, pc + "^r=8", 8, vel)
            add("chugl", at + 8, pc + "^r=8", 8, vel)
            add("chugr", at, pc + "^r=8", 8, vel - 2)
            add("chugr", at + 8, pc + "^r=8", 8, vel - 2)
        if sec == "derailed":
            d = DOOM[b % 4]
            for st, n, l in d[1]:
                add("chugl", at + st, f"{nm(n)},{nm(n + 7)},{nm(n + 12)}", l, 120)
                add("chugr", at + st, f"{nm(n)},{nm(n + 7)},{nm(n + 12)}", l, 118)

        # --- THE LINE
        if sec == "chug" and b >= 32 and b % 2 == 0:
            cell = LINE[(b // 2) % 4]
            st = 0
            for n, l in cell:
                add("lead", at + st, f"{n}^r={l // 2}", l, 92)
                st += l
        if sec == "yard" and b >= 4 and b % 4 == 0:
            cell = LINE[(b // 4) % 4]
            st = 0
            for n, l in cell:
                add("ebow", at + st, n, l * 64 // 28, 84)
                st += l * 64 // 28
        if sec == "climb" and b >= 24 and b % 2 == 0:
            cell = LINE[(b // 2) % 4]
            st = 0
            for n, l in cell:
                add("ebow", at + st, nm(midi(n) + 12), l * 32 // 28, 96)
                st += l * 32 // 28

        # --- distant metal in the yard (every 5 bars: the odd length keeps it from settling)
        if sec == "yard" and b % 5 == 2:
            add("yardmetal", at + 6, "cbl", 2, 70)
            add("yardmetal", at + 9, "t3", 2, 50)

        # --- drums
        kit = []
        if sec == "joints":
            kit += [(st, "rc", 70 if st in (0, 8) else 54) for st in (0, 2, 8, 10)]
            if b >= 16:
                kit += [(0, "ft", 84), (4, "t3", 72), (8, "ft", 90)]
            if b >= 32:
                kit += [(st, "hf", 50) for st in range(0, 14, 2)]
        elif sec == "chug":
            kit += [(0, "k", 118), (2, "k", 104), (8, "k", 114), (4, "s", 112), (11, "s", 116)]
            kit += [(st, "rd", 76 if st % 4 == 0 else 62) for st in range(0, 14, 2)]
            if b % 8 == 0:
                kit += [(0, "c", 118)]
        elif sec == "climb":
            if b < 16:
                kit += [(0, "ft", 70 + b), (8, "t3", 60 + b)]
            elif b < 32:
                kit += [(0, "k", 112), (8, "s", 112)] + [(st, "rd", 70) for st in range(0, 16, 2)]
                if b % 4 == 0:
                    kit += [(0, "c", 112)]
            else:
                kit += [(st, "k", 112) for st in range(0, 16, 2)] + [(4, "s", 118), (12, "s", 118)]
                kit += [(st, "rde", 90) for st in range(0, 16, 4)]
                if b % 2 == 0:
                    kit += [(0, "c", 122)]
        elif sec == "derailed":
            kit += [(0, "k", 120), (6, "k", 108), (8, "s", 122), (4, "x", 100), (12, "x", 106)]
            if b % 4 == 0:
                kit += [(0, "c", 124)]
        for st, piece, vel in kit:
            add("kit", at + st, piece, 1, vel)

    # absolute events -> one continuous score per track (long holds simply run on)
    return {k: stream(ev[k], total) for k in TRACKS}


def stream(events, total):
    by = {}
    for st, head, ln, vel in events:  # simultaneous hits on one track (kit pieces) become one chord
        if st in by:
            h0, l0, v0 = by[st]
            n0, _, a0 = h0.partition("^")
            n1 = head.partition("^")[0]
            by[st] = (f"{n0},{n1}" + (f"^{a0}" if a0 else ""), min(l0, ln), max(v0, vel))
        else:
            by[st] = (head, ln, vel)
    ev = sorted((st, h, l, v) for st, (h, l, v) in by.items())
    out, pos = [], 0
    for i, (st, head, ln, vel) in enumerate(ev):
        if st < pos:
            continue
        nxt = ev[i + 1][0] if i + 1 < len(ev) else total
        hold = max(1, min(ln, max(nxt, st + 1) - st, total - st))
        out.append(R((st - pos) * S))
        note, _, art = head.partition("^")
        out.append(f"{note}/{hold * S:g}b@{int(vel)}" + (f"^{art}" if art else ""))
        pos = st + hold
    out.append(R((total - pos) * S))
    return J(*out)


DOOM = [(33, [(0, 33, 8), (8, 36, 4), (12, 34, 4)]),     # A, C, Bb
        (33, [(0, 33, 12), (12, 31, 4)]),                # A, G
        (36, [(0, 36, 8), (8, 34, 8)]),                  # C, Bb
        (31, [(0, 31, 6), (6, 33, 10)])]                 # G, A


def lane(points):
    _, total = layout()
    pts = [["0s", points[0][1]]]
    spb = 60 / BPM
    for step, val in points[1:]:
        t = step * S * spb
        pts.append([f"{t:.3f}s", val])
    pts.append([f"{total * S * spb + 10:.2f}s", pts[-1][1]])
    return {"points": pts}


def song():
    T = build()
    sc = lambda n: T[n]  # noqa: E731
    st = {sec: sec_start(sec) for sec, _, _ in FORM}
    # the arc in dB on the master: quiet passages stay quiet
    dyn = lane([(0, -6), (st["joints"], -4), (st["chug"], 0), (st["yard"], -6), (st["climb"], -4),
                (st["climb"] + 32 * 16, 0), (st["derailed"], 1), (st["lastcar"], -5)])
    doc = {
        "about": "Chirpers - All the Lights Left On (Chirpers VI), track 3 by chirper-zero: INSTRUMENTAL POST-METAL, night freight. "
                 "Generated by compose/chirpers6/src/chirpers6-t3.py; see its docstring and compose/chirpers6/styles.md.",
        "tempo": BPM, "ceiling": "-1.2dB", "volume": "0dB", "true_peak": True, "tail": "2s",
        "patches": {
            "rail-rumble": {"about": "night freight: the train's rumble - brown noise low-passed, swelling in and out over seconds",
                            "synth": {"layers": [{"type": "noise", "color": "brown"}], "filters": ["lp cutoff=160 q=0.8"],
                                      "amp": {"a": "6s", "s": 1, "r": "6s"}}},
            "wheel-clack": {"about": "night freight: a wheel over a rail joint - a noise crack and two metal partials, short",
                            "synth": {"layers": [{"type": "noise", "color": "white"}, "sine fixed=820 level=-6dB", "sine fixed=1370 level=-10dB"],
                                      "filters": ["bp cutoff=1600 q=0.7"], "amp": {"a": "0.5ms", "d": "70ms", "s": 0, "r": "40ms"}}},
        },
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=28", "peak cutoff=300 q=0.8 gain=-2dB", "highshelf cutoff=7000 gain=-1dB"]},
                          {"type": "compressor", "threshold": "-18dB", "ratio": 2, "attack": "15ms", "release": "200ms", "makeup": "0dB"},
                          {"type": "gain", "gain": f"+{MGAIN:g}dB"},
                          {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}}],
                   "auto": {"dyn": dyn}},
        "buses": {
            "drums": {"fx": [{"type": "compressor", "threshold": "-14dB", "ratio": 3, "attack": "5ms", "release": "90ms", "makeup": "1dB"}]},
            "hall": {"fx": ["reverb kind=hall decay=3.5s size=0.9 mix=1 predelay=30ms"]},
            "yard": {"fx": ["reverb kind=hall decay=6s size=1 mix=1 predelay=60ms", "lp cutoff=2500"]},
        },
        "tracks": [
            {"name": "bell", "patch": "bell", "gain": "-20dB", "pan": 0.35, "sends": {"yard": "-6dB"}, "score": sc("bell")},
            {"name": "rumble", "patch": "rail-rumble", "gain": "-12dB", "score": sc("rumble")},
            {"name": "clack", "patch": "wheel-clack", "gain": "-14dB", "pan": -0.2, "sends": {"yard": "-14dB"}, "score": sc("clack")},
            {"name": "horn", "patch": "brass-synth", "gain": "-16dB", "fx": [{"type": "filter", "kind": "lp", "cutoff": 2200, "q": 0.7}],
             "sends": {"yard": "-4dB"}, "score": sc("horn")},
            {"name": "wind", "patch": "fx-wind", "gain": "-18dB", "score": sc("wind")},
            {"name": "clean", "patch": "clean-chorus", "gain": "-8dB", "pan": -0.15, "sends": {"hall": "-10dB"}, "score": sc("clean")},
            {"name": "fretless", "patch": "fretless-bass", "gain": "-6dB", "score": sc("fretless")},
            {"name": "chugl", "patch": "m8-rhythm-l", "gain": "-10dB", "pan": -0.7, "score": sc("chugl")},
            {"name": "chugr", "patch": "m8-rhythm-r", "gain": "-10dB", "pan": 0.7, "score": sc("chugr")},
            {"name": "fuzz", "patch": "bass-fuzz", "gain": "-8dB", "score": sc("fuzz")},
            {"name": "sub", "patch": "sub-sine", "gain": "-10dB", "score": sc("sub")},
            {"name": "kit", "patch": "room-kit", "gain": "-2dB", "out": "drums", "score": sc("kit")},
            {"name": "lead", "patch": "m8-lead-guitar", "gain": "-14dB", "pan": 0.2, "sends": {"hall": "-8dB"}, "score": sc("lead")},
            {"name": "cello", "patch": "cellos", "gain": "-8dB", "sends": {"hall": "-6dB"}, "score": sc("cello")},
            {"name": "ebow", "patch": "ebow", "gain": "-10dB", "pan": 0.1, "sends": {"hall": "-8dB"}, "score": sc("ebow")},
            {"name": "yardmetal", "patch": "metal-kit", "gain": "-14dB", "pan": 0.5, "sends": {"yard": "0dB"}, "score": sc("yardmetal")},
        ],
    }
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
