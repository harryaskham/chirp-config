#!/usr/bin/env python3
"""chirpers6-t4 (All the Lights Left On, track 4) - generator for songs/chirpers6-t4.yaml (chirper-zero).

SLOWCORE WALTZ INTO A SHOEGAZE WALL / "sodium". 3/4 at 72 bpm, E minor (the last movement in its relative G major).
The orange sodium streetlights left on all night: their hum and flicker are the found sound. A slow, bare waltz under a
lamp blooms into a wall of chorus-and-fuzz guitars with the melody buried inside it; the wall fails as the lamps flicker
(gated, stuttered, tape-stopped), and the waltz comes back in the major as the lamps go off one by one. The only words
(v4): someone counting the lamps out, eight down to one. Original; a style, not a version of any track.

Form (3/4 bars): I HUM 16 (the mains hum and a buzzing ballast, a failing lamp's relay clicking, one guitar note
swelling) / II WALTZ 32 (a clean guitar and a fretless in 3/4, brushes, THE WALTZ) / III BLOOM 32 (reverse swells into
each phrase, a second guitar gliding in octaves, the brushes to sticks, an ebow answering the theme a third above) /
IV WALL 48 (the shoegaze wall: chorused crunch guitars strumming eighths left and right, a fuzz rig holding the chords,
a supersaw pad, the theme buried in a wordless choir, heavy 6/8 drums, sub) / V FLICKER 16 (the wall cut by the
failing lamp: gated on irregular sixteenths, stuttered, then a tape stop) / VI LIGHTS OUT 32 (the waltz in G major on a
drowned piano and the clean guitar; the lamps switching off one by one, the hum stepping down until it is gone).

Motifs (compose/chirpers6/motifs.md):
  THE CHANGES  Em9 | Cmaj9 | Am9 | B7sus4 - B7, two bars each; in LIGHTS OUT Gmaj9 | Cmaj9 | Em9 | D6/9 - G.
  THE WALTZ    B4 | A4 G4 F#4 | G4 . E4 | D4 | E4 F#4 G4 | A4 . B4 | F#4 | D#4 .  (eight bars, quarters and dotted halves).
  THE LAMP     the 100 Hz hum (and its 200/300 Hz), a ballast buzz, a relay's clicks, the switch-off thunk.
Run: python3 compose/chirpers6/src/chirpers6-t4.py  (writes songs/chirpers6-t4.yaml)
"""
import json
import os
import random

ROOT = os.path.expanduser("~/.config/chirp")
OUT = os.environ.get("C6T4_OUT") or os.path.join(ROOT, "songs", "chirpers6-t4.yaml")
BPM = 72
S = 0.25  # beats per sixteenth
BAR = 12  # sixteenths in a 3/4 bar
MGAIN = float(os.environ.get("C6T4_MGAIN", "6.5"))
WARMUP = os.environ.get("C6T4_WARMUP", "1") == "1"  # the lamp warms up: the buzz and the relay first, the hum entering after a bar (sodium lamps start dim and rise)
WALLSTAGES = os.environ.get("C6T4_WALLSTAGES", "1") == "1"  # the wall's stages made distinct: bare strums and fuzz; then the pad and the choir; then the major glimpse with the strums tremolo-picked in 16ths (shimmer)
LOSTAGES = os.environ.get("C6T4_LOSTAGES", "1") == "1"  # lights out in four stages: the piano alone; the clean guitar and brushes join; the ebow's last line over them; the piano and the hum alone
EQ = os.environ.get("C6T4_EQ", "1") == "1"
LATEOFF = os.environ.get("C6T4_LATEOFF", "1") == "1"
SUBMODE = os.environ.get("C6T4_SUBMODE", "")  # "c": the sub's C and A roots an octave up (C1 and A1 were piling up at 32 and 51 Hz); "none": no sub
HPF = os.environ.get("C6T4_HPF", "28")  # the master's high-pass (Hz)
TOP = os.environ.get("C6T4_TOP", "3")
WPUMP = os.environ.get("C6T4_WPUMP", "1") == "1"  # the wall breathes with the kick: the wall bus pumps (sidechain) from the rock kit's kick, -4 dB
GLIDE = os.environ.get("C6T4_GLIDE", "1") == "1"
COUNT = os.environ.get("C6T4_COUNT", "1") == "1"  # someone counts the lamps out: a close, dry voice says the number of each lamp as it goes off in LIGHTS OUT, eight down to one
BUZZIN = os.environ.get("C6T4_BUZZIN", "1") == "1"  # the ballast buzz enters a bar in, after the first relay clicks  # glide guitar: half the wall through a pitch shifter wobbling +-0.35 semitone on a 1.5-bar LFO (the tremolo arm held while strumming)  # the master's 8 kHz shelf (dB) with the EQ on  # the last lamp goes off in the last bar but one (not three bars early), and the render tail is 1 s: the hand-over into Leave the Lights On has no dead air  # the crunch guitars' 2.4 kHz down 4 dB on the wall bus, the master's top up 3 dB from 8 kHz

NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
NOTE = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9,
        "A#": 10, "Bb": 10, "B": 11}
FORM = [("hum", 16), ("waltz", 32), ("bloom", 32), ("wall", 48), ("flicker", 16), ("lightsout", 32)]
# (root, voicing) - E minor, then G major for the last movement
CH = [(28, [52, 55, 59, 62, 66]),   # Em9: E3 G3 B3 D4 F#4
      (24, [48, 52, 55, 59, 62]),   # Cmaj9: C3 E3 G3 B3 D4
      (33, [45, 52, 55, 59, 60]),   # Am9: A2 E3 G3 B3 C4
      (35, [47, 52, 54, 57, 59])]   # B7sus4: B2 E3 F#3 A3 B3 (the 4th falls to D#)
CHG = [(31, [43, 50, 54, 57, 59]),  # Gmaj9: G2 D3 F#3 A3 B3
       (24, [48, 52, 55, 59, 62]),  # Cmaj9
       (28, [52, 55, 59, 62, 66]),  # Em9
       (26, [50, 54, 57, 59, 64])]  # D6/9: D3 F#3 A3 B3 E4
WALTZ = [[("B4", 12)], [("A4", 4), ("G4", 4), ("F#4", 4)], [("G4", 8), ("E4", 4)], [("D4", 12)],
         [("E4", 4), ("F#4", 4), ("G4", 4)], [("A4", 8), ("B4", 4)], [("F#4", 12)], [("D#4", 8), ("R", 4)]]
WALTZG = [[("D5", 12)], [("C5", 4), ("B4", 4), ("A4", 4)], [("B4", 8), ("G4", 4)], [("F#4", 12)],
          [("G4", 4), ("A4", 4), ("B4", 4)], [("C5", 8), ("D5", 4)], [("A4", 12)], [("B4", 8), ("R", 4)]]
TRACKS = ("hum", "buzz", "click", "thunk", "clean", "glide", "fretless", "kit", "brush", "ebow", "swell", "strumL", "strumR",
          "fuzz", "pad", "choir", "sub", "piano", "count")


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def midi(n):
    return 12 * (int(n[-1]) + 1) + NOTE[n[:-1]]


def R(d):
    return f"R/{d:g}b" if d > 1e-9 else ""


def J(*xs):
    return " ".join(x for x in xs if x)


def sec_start(name):
    t = 0
    for sec, nb in FORM:
        if sec == name:
            return t
        t += nb * BAR
    raise KeyError(name)


def total_steps():
    return sum(nb for _, nb in FORM) * BAR


def chord(sec, b):
    tab = CHG if (sec == "lightsout" or (sec == "wall" and 24 <= b < 36)) else CH
    return tab[(b // 2) % 4]


def build():
    ev = {k: [] for k in TRACKS}
    rnd = random.Random(7)

    def add(tr, at, head, ln, vel):
        ev[tr].append((at, head, ln, vel))

    total = total_steps()
    # THE LAMP: the hum held through the hum, low under the waltz, gone in the wall, back in the flicker, stepping down at the end
    add("hum", BAR if WARMUP else 0, "C4", sec_start("bloom") - (BAR if WARMUP else 0), 92)
    add("buzz", BAR if BUZZIN else 0, "C4", sec_start("waltz") + 8 * BAR - (BAR if BUZZIN else 0), 80)
    add("hum", sec_start("flicker"), "C4", 16 * BAR, 96)
    lo = sec_start("lightsout")
    offs = [0, 6, 11, 15, 19, 22, 25, 28, 31] if LATEOFF else [0, 6, 11, 15, 19, 22, 25, 27, 29]  # the lamps going off, bar by bar
    for k in range(len(offs) - 1):
        add("hum", lo + offs[k] * BAR, "C4", (offs[k + 1] - offs[k]) * BAR, 96 - 10 * k)
        add("thunk", lo + offs[k + 1] * BAR, "C2", 2, 100 - 4 * k)
        add("click", lo + offs[k + 1] * BAR + 1, "C5", 1, 90)
        if COUNT:  # the count, a beat after each lamp goes: eight ... one
            words = [["ey1-t"], ["s-eh1", "v-ah0-n"], ["s-ih1-k-s"], ["f-ay1-v"], ["f-ao1-r"], ["th-r-iy1"], ["t-uw1"], ["w-ah1-n"]][k]
            for j, syl in enumerate(words):
                last = j == len(words) - 1
                add("count", lo + offs[k + 1] * BAR + 4 + 2 * j, "G2^ph=" + syl + ("^f0=0>-50" if last else ""), 3 if last else 2, 70 - 2 * k)
    # the failing lamp's relay: irregular clicks in the hum and the flicker
    for sec, dens in (("hum", 0.18), ("flicker", 0.35)):
        a = sec_start(sec)
        nb = dict(FORM)[sec]
        for t in range(a, a + nb * BAR):
            if rnd.random() < dens:
                add("click", t, "C5", 1, 60 + rnd.randint(0, 40))

    for sec, nb in FORM:
        a0 = sec_start(sec)
        for b in range(nb):
            at = a0 + b * BAR
            r, v = chord(sec, b)
            theme = WALTZG if (sec == "lightsout" or (sec == "wall" and 24 <= b < 36)) else WALTZ
            ws = b // 12 if sec == "wall" else -1  # the wall's stage: entry, the buried theme, the major glimpse, the drop and return
            cell = theme[b % 8]

            # --- one guitar note swelling in the hum
            if sec == "hum" and b in (4, 10):
                add("ebow", at, "B3", 5 * BAR, 70)

            # --- the clean waltz guitar: bass note then the chord in eighths (r, 5, 9, 3, 5, 9)
            lo_stage = b // 8 if (LOSTAGES and sec == "lightsout") else -1
            if (sec in ("waltz", "bloom") or (sec == "lightsout" and lo_stage in (-1, 1, 2)) or (sec == "hum" and b >= 12)):
                idx = [0, 2, 4, 1, 2, 3]
                vel0 = 70 if sec != "hum" else 54
                for k, i in enumerate(idx):
                    add("clean", at + 2 * k, nm(v[i]), 2, vel0 + (10 if k == 0 else 0))
            # --- the gliding octave guitar in the bloom: the theme an octave down, legato
            if sec == "bloom" and b >= 8:
                st = 0
                for n, l in cell:
                    if n != "R":
                        add("glide", at + st, nm(midi(n) - 12) + "^gate=1.1", l, 72)
                    st += l
            # --- the theme: the clean guitar's top line in the waltz, the ebow a third above answering in the bloom,
            #     the choir buried in the wall, the piano in the major
            if sec == "waltz" and b >= 8:
                st = 0
                for n, l in cell:
                    if n != "R":
                        add("ebow", at + st, n, l, 78)
                    st += l
            if sec == "bloom" and (b // 4) % 2 == 1:
                st = 0
                for n, l in cell:
                    if n != "R":
                        add("ebow", at + st, nm(midi(n) + (3 if n[0] in "EAB" else 4)), l, 84)
                    st += l
            if sec == "wall" and (ws in (1, 2) or (ws == 3 and b >= 40)):
                st = 0
                for n, l in cell:
                    if n != "R":
                        add("choir", at + st, n, l, 92 if ws != 2 else 98)
                    st += l
            if sec == "lightsout":
                st = 0
                for n, l in cell:
                    if n != "R":
                        add("piano", at + st, f"{n},{nm(v[1] + 12)}" if l >= 8 else n, l, 70 - (b // 8) * 6)
                    st += l
                if b % 2 == 0:
                    add("piano", at, nm(r + 12), 4, 62)

            # --- bass
            if LOSTAGES and sec == "lightsout" and lo_stage == 2 and b % 8 == 0:
                st_ = 0
                for n, l in [("B4", 24), ("A4", 12), ("G4", 36), ("F#4", 12), ("G4", 12)]:  # the ebow's last line
                    add("ebow", at + st_, n, l, 80)
                    st_ += l
            if sec in ("waltz", "bloom") or (sec == "lightsout" and lo_stage in (-1, 1, 2)):
                add("fretless", at, nm(r + 12), 8, 86)
                add("fretless", at + 8, nm(r + 19), 4, 70)
            if sec in ("wall",) and SUBMODE != "none":
                add("sub", at, nm(r + 12 if (SUBMODE == "c" and r in (24, 33)) else r), BAR, 96)
                add("fretless", at, nm(r + 12), 6, 96)
                add("fretless", at + 6, nm(r + 12), 6, 88)

            # --- reverse swells into each four-bar phrase of the bloom, and into the wall
            if (sec == "bloom" and b % 4 == 3) or (sec == "bloom" and b == nb - 1):
                add("swell", at + 4, nm(v[0] + 12), 8, 84)

            # --- the wall: chorused crunch guitars strumming eighths L/R, the fuzz rig holding, the saw pad
            if sec in ("wall", "flicker") and not (ws == 3 and b < 40):
                ch = ",".join(nm(n) for n in v[:4])
                if WALLSTAGES and ws == 2:  # the major glimpse: the strums tremolo-picked in 16ths, a shimmer
                    for k in range(3):
                        add("strumL", at + 4 * k, ch + "^r=4", 4, 96)
                        add("strumR", at + 4 * k, ch + "^r=4", 4, 92)
                else:
                    for k in range(6):
                        add("strumL", at + 2 * k, ch, 2, 100 if k % 3 == 0 else 86)
                        add("strumR", at + 2 * k + 1 if k < 5 else at + 2 * k, ch, 1 if k < 5 else 2, 96 if k % 3 == 0 else 82)
            if sec in ("wall", "flicker") and b % 2 == 0:
                add("fuzz", at, f"{nm(r + 12)},{nm(r + 19)},{nm(r + 24)}", 2 * BAR, 110)
                if not (ws == 3 and b < 40) and not (WALLSTAGES and ws == 0):
                    add("pad", at, ",".join(nm(n + 12) for n in v[1:4]), 2 * BAR, 90)

            # --- drums
            kit = []
            if sec == "waltz":
                kit += [(0, "k", 80), (4, "s", 54), (8, "s", 58)]
                if b % 2 == 0:
                    kit += [(0, "sw", 50)]
            elif sec == "bloom":
                if b < 16:
                    kit += [(0, "k", 88), (4, "ss", 70), (8, "ss", 74), (0, "rd", 60), (6, "rd", 54)]
                else:
                    kit += [(0, "k", 100), (4, "s", 86), (8, "s", 90)] + [(st, "rd", 66) for st in (0, 4, 8)]
                if b == nb - 1:
                    kit += [(st, "s", 70 + 5 * st) for st in range(6, 12)]
            elif sec == "wall":
                kit += [(0, "k", 118), (6, "s", 120), (3, "k", 96), (9, "k", 100)]
                if ws == 2:  # the major glimpse: the ride doubles
                    kit += [(st, "rd", 94 if st % 6 == 0 else 80) for st in range(12)]
                elif ws == 3 and b < 40:  # the drop: kick and floor tom under the fuzz
                    kit = [(0, "k", 120), (6, "ft", 112), (9, "ft", 100)]
                else:
                    kit += [(st, "rd", 92 if st % 6 == 0 else 78) for st in range(0, 12, 2)]
                if b % 4 == 0 or (ws == 3 and b >= 40 and b % 2 == 0):
                    kit += [(0, "c", 122)]
                if b % 8 == 7:
                    kit = [k for k in kit if k[0] < 6] + [(6 + i, t, 96 + 4 * i) for i, t in enumerate(["t1", "t2", "t2", "t3", "ft", "ft"])]
            elif sec == "flicker":
                kit += [(0, "k", 112), (6, "s", 112)]
            elif sec == "lightsout" and (lo_stage in (1, 2) if LOSTAGES else 8 <= b < 24):
                kit += [(0, "k", 70), (4, "ss", 56), (8, "ss", 58)]
            sticks = (sec == "bloom" and b >= 16) or sec in ("wall", "flicker")
            for st, piece, vel in kit:
                add("kit" if sticks else "brush", at + st, piece, 1, vel)
    return {k: stream(ev[k], total) for k in TRACKS}


def stream(events, total):
    by = {}
    for st, head, ln, vel in events:
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


def lane(points, step=True):
    """points: (sixteenth, value). step=True holds each value until the next point (gates); False ramps."""
    spb = 60 / BPM
    pts = [["0s", points[0][1]]]
    prev = points[0][1]
    for t16, val in points[1:]:
        t = t16 * S * spb
        if step:
            pts.append([f"{max(0.0, t - 0.004):.3f}s", prev])
        pts.append([f"{t:.3f}s", val])
        prev = val
    pts.append([f"{total_steps() * S * spb + 10:.2f}s", prev])
    return {"points": pts}


def flicker_gate():
    """The failing lamp: the wall bus cut to -40 dB on irregular sixteenths through the flicker (seeded)."""
    rnd = random.Random(31)
    a = sec_start("flicker")
    pts = [(0, 0)]
    on = True
    for t in range(a, a + 16 * BAR):
        p_off = 0.12 + 0.5 * (t - a) / (16 * BAR)  # failing more and more
        want = rnd.random() > p_off
        if want != on:
            pts.append((t, 0 if want else -40))
            on = want
    pts.append((a + 16 * BAR, -60))  # out
    return lane(pts)


def song():
    T = build()
    sc = lambda n: T[n]  # noqa: E731
    st = {sec: sec_start(sec) for sec, _ in FORM}
    dyn = lane([(0, -8), (st["waltz"], -6), (st["bloom"], -4), (st["bloom"] + 16 * BAR, -2), (st["wall"], 0),
                (st["flicker"], -1), (st["lightsout"], -7)])
    fl = st["flicker"]
    doc = {
        "about": "Chirpers - All the Lights Left On (Chirpers VI), track 4 by chirper-zero: SLOWCORE WALTZ INTO A SHOEGAZE WALL, sodium. "
                 "Generated by compose/chirpers6/src/chirpers6-t4.py; see its docstring and compose/chirpers6/styles.md.",
        "tempo": BPM, "ceiling": "-1.2dB", "volume": "0dB", "true_peak": True, "tail": "1s" if LATEOFF else "2s",
        "patches": {
            "mains-hum": {"about": "sodium: the streetlights' mains hum - 100 Hz with its 200 and 300 Hz, steady",
                          "synth": {"layers": ["sine fixed=100", "sine fixed=200 level=-9dB", "sine fixed=300 level=-16dB"],
                                    "amp": {"a": "2s", "s": 1, "r": "1.5s"}}},
            "ballast-buzz": {"about": "sodium: a lamp's ballast buzzing - pink noise band-passed at 2.4 kHz, thin",
                             "synth": {"layers": [{"type": "noise", "color": "pink"}], "filters": ["bp cutoff=2400 q=2"],
                                       "amp": {"a": "3s", "s": 1, "r": "2s"}}},
            "relay-click": {"about": "sodium: a failing lamp's relay - a 2 ms tick",
                            "synth": {"layers": [{"type": "noise", "color": "white"}, "sine fixed=2600 level=-6dB"], "filters": ["hp cutoff=1800"],
                                      "amp": {"a": "0.2ms", "d": "8ms", "s": 0, "r": "5ms"}}},
            "switch-thunk": {"about": "sodium: a streetlight switching off - a low thunk",
                             "synth": {"layers": ["sine fixed=62", {"type": "noise", "color": "brown"}], "filters": ["lp cutoff=400"],
                                       "amp": {"a": "1ms", "d": "220ms", "s": 0, "r": "120ms"}}},
        },
        "master": {"fx": [{"type": "eq", "bands": [f"highpass cutoff={HPF}", "peak cutoff=300 q=0.8 gain=-2dB", "highshelf cutoff=7000 gain=0dB", *([f"highshelf cutoff=8000 gain={TOP}dB"] if EQ else [])]},
                          {"type": "compressor", "threshold": "-18dB", "ratio": 2, "attack": "20ms", "release": "250ms", "makeup": "0dB"},
                          {"type": "gain", "gain": f"+{MGAIN:g}dB"},
                          {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}}],
                   "auto": {"dyn": dyn}},
        "buses": {
            "drums": {"fx": [{"type": "compressor", "threshold": "-14dB", "ratio": 3, "attack": "6ms", "release": "100ms", "makeup": "1dB"}]},
            "wall": {"fx": ([{"type": "eq", "bands": ["peak cutoff=2400 q=0.9 gain=-4dB"]}] if EQ else [])
                           + ([{"type": "pitch", "semitones": {"value": 0, "mod": [{"src": "lfo.g", "amount": 0.35}]}, "mix": 0.5, "grain": "60ms"}] if GLIDE else [])
                           + ([{"type": "pump", "on": "kit.k", "depth": "-4dB", "attack": "2ms", "release": "300ms", "curve": 0.8}] if WPUMP else [])
                           + [{"type": "chorus", "depth": 0.6, "rate": 0.7, "mix": 0.5},
                            {"type": "stutter", "slice": "1/16", "repeats": 3, "chance": 0.35, "roll": 1, "seed": 3,
                             "mix": {"value": 0, "mod": [{"src": "auto.stu", "amount": 1}]}},
                            {"type": "tapestop", "stop": {"value": 0, "mod": [{"src": "auto.ts", "amount": 1}]}, "time": "3b", "curve": 1.4},
                            {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.fl", "amount": 1}]}}],
                     "sends": {"hall": "-4dB"}, **({"lfo": {"g": "sine rate=3/2"}} if GLIDE else {}),
                     "auto": {"fl": flicker_gate(), "stu": lane([(0, 0), (fl, 1), (fl + 16 * BAR, 0)]),
                              "ts": lane([(0, 0), (fl + 15 * BAR, 1), (fl + 16 * BAR, 0)])}},
            "hall": {"fx": ["reverb kind=hall decay=4.5s size=1 mix=1 predelay=40ms", "lp cutoff=9000"]},
        },
        "tracks": [
            {"name": "hum", "patch": "mains-hum", "gain": "-24dB", "score": sc("hum")},
            {"name": "buzz", "patch": "ballast-buzz", "gain": "-36dB", "pan": 0.2, "score": sc("buzz")},
            {"name": "click", "patch": "relay-click", "gain": "-26dB", "pan": 0.25, "score": sc("click")},
            {"name": "thunk", "patch": "switch-thunk", "gain": "-14dB", "sends": {"hall": "-10dB"}, "score": sc("thunk")},
            {"name": "clean", "patch": "starcaster-clean", "gain": "-9dB", "pan": -0.2, "sends": {"hall": "-10dB"}, "score": sc("clean")},
            {"name": "glide", "patch": "starcaster-clean", "gain": "-12dB", "pan": 0.35, "sends": {"hall": "-6dB"}, "score": sc("glide")},
            {"name": "fretless", "patch": "fretless-bass", "gain": "-7dB", "score": sc("fretless")},
            {"name": "brush", "patch": "brush-kit", "gain": "-4dB", "out": "drums", "score": sc("brush")},
            {"name": "kit", "patch": "rock-kit-dark", "gain": "-4dB", "out": "drums", "score": sc("kit")},
            {"name": "ebow", "patch": "ebow", "gain": "-12dB", "pan": 0.15, "sends": {"hall": "-6dB"}, "score": sc("ebow")},
            {"name": "swell", "patch": "rev-swell", "gain": "-12dB", "sends": {"hall": "-8dB"}, "score": sc("swell")},
            {"name": "strumL", "patch": "strat-crunch", "gain": "-14dB", "pan": -0.75, "out": "wall", "score": sc("strumL")},
            {"name": "strumR", "patch": "strat-crunch", "gain": "-14dB", "pan": 0.75, "out": "wall", "score": sc("strumR")},
            {"name": "fuzz", "patch": "m8-fuzz", "gain": "-16dB", "out": "wall", "score": sc("fuzz")},
            {"name": "pad", "patch": "saw-pad", "gain": "-16dB", "out": "wall", "score": sc("pad")},
            {"name": "choir", "patch": "dream-vox", "gain": "-12dB", "out": "wall", "score": sc("choir")},
            {"name": "sub", "patch": "sub-sine", "gain": "-16dB", "score": sc("sub")},
            *([{"name": "count", "patch": "voice-speech", "gain": "-10dB", "pan": 0.1,
                "fx": [{"type": "filter", "kind": "hp", "cutoff": 120, "q": 0.7}, "reverb kind=room decay=0.6s mix=0.15"], "score": sc("count")}] if COUNT else []),
            {"name": "piano", "patch": "piano-wash", "gain": "-6dB", "pan": -0.1, "score": sc("piano")},
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
