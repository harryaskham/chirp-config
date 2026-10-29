#!/usr/bin/env python3
"""chirpers2-t4 (Odd Hours, track 4). Composed by chirper-two: a CHAMBER JAZZ BRUSH TRIO with a singing tom choir.

Everything is a palindrome:
- METERS, bar by bar: 3/4 5/8 7/8 4/4 7/8 5/8 3/4 (44 eighths a phrase). The bridge reads it from the centre out
  (4/4 7/8 5/8 3/4 5/8 7/8 4/4). Swung eighths in the 3/4 and 4/4 bars, straight in the odd ones.
- HARMONY: Dm9 | Bbmaj7#11 | G13sus | CENTRE | G13sus | Bbmaj7#11 | Dm9. The centre bar's chords move each time the
  phrase comes round (the only door out of the mirror). Harmonic rhythm breathes with the meter: one chord in 3/4
  and 5/8 bars, two in 7/8 (4+3) and in 4/4.
- MELODY: each bar's line is the retrograde (pitch and rhythm) of its mirror bar's, so the whole head reads the same
  backwards, and the centre bar is a palindrome itself.
- ORCHESTRATION: the melody passes bar by bar (klangfarbenmelodie) trumpet -> piano -> tom choir -> trumpet ->
  tom choir -> piano -> trumpet, a palindrome of colours.
The TOM CHOIR is a melodic instrument made of physical membrane toms (chirp `type: drum`, bd-7d117e: tuned with
`tune_sounding`, two-mic `stereo`); the kit plays BRUSHES (`beater: brush`, taps and `sweep`s).

Emits songs/chirpers2-t4.yaml. Edit the music here.
"""
import json
import os

OUT = os.environ.get("T4_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers2-t4.yaml")
BPM = 132
SWING = float(os.environ.get("T4_SWING", "0.62"))  # where a swung off-beat eighth lands (0.667 = triplet: tried, rhythm flat, recurrence lost)
TRIP = "T" in os.environ.get("T4_OPTS", "")  # triplet brush ghosts before the backbeats (off: no gain)
NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
PC = {n: i for i, n in enumerate(NAMES)}
PC.update({"Db": 1, "D#": 3, "Gb": 6, "G#": 8, "A#": 10})


def midi(n):
    """'D4' -> 62."""
    name, octv = (n[:-1], int(n[-1])) if n[-2] not in "-" else (n[:-2], int(n[-2:]))
    return 12 * (octv + 1) + PC[name]


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


# ---------------- the palindrome ----------------
METERS = [6, 5, 7, 8, 7, 5, 6]          # eighths per bar
BRIDGE = [8, 7, 5, 6, 5, 7, 8]          # read from the centre out
SWUNG = {6: True, 8: True, 5: False, 7: False}
GROUP = {5: (3, 2), 7: (2, 2, 3), 6: (2, 2, 2), 8: (2, 2, 2, 2)}

# chords: (root midi in octave 2-3, voicing intervals above the root for the piano, scale for lines)
CH = {
    "Dm9": (50, [3, 7, 10, 14], [0, 2, 3, 5, 7, 9, 10]),
    "Bbmaj7#11": (46, [4, 7, 11, 18], [0, 2, 4, 6, 7, 9, 11]),
    "G13sus": (43, [5, 10, 14, 21], [0, 2, 5, 7, 9, 10]),
    "Fmaj7/G": (43, [10, 14, 17, 21], [0, 2, 4, 5, 7, 9, 10]),
    "Ebmaj9": (51, [4, 7, 11, 14], [0, 2, 4, 7, 9, 11]),
    "Abmaj7#11": (44, [4, 7, 11, 18], [0, 2, 4, 6, 7, 9, 11]),
    "Emaj9": (52, [4, 7, 11, 14], [0, 2, 4, 7, 9, 11]),
    "Amaj7": (45, [4, 7, 11, 16], [0, 2, 4, 7, 9, 11]),
    "Fm9": (53, [3, 7, 10, 14], [0, 2, 3, 5, 7, 8, 10]),
    "Dbmaj7#11": (49, [4, 7, 11, 18], [0, 2, 4, 6, 7, 9, 11]),
    "Cm11": (48, [3, 10, 14, 17], [0, 2, 3, 5, 7, 9, 10]),
    "F13": (41, [4, 10, 14, 21], [0, 2, 4, 7, 9, 10]),
    "Dm(maj9)": (50, [3, 7, 11, 14], [0, 2, 3, 5, 7, 9, 11]),
}
# the centre bar's door, phrase by phrase
CENTRES = [("Ebmaj9", "Abmaj7#11"), ("Emaj9", "Amaj7"), ("Fm9", "Dbmaj7#11"), ("Cm11", "F13")]


def low(root):
    """A chord root in the bass's register, E1..D#2 (an upright's bottom octave)."""
    r = root % 12
    return 28 + (r - 4) % 12


def bar_chords(meter, centre, mirror_pos):
    """The chords of a bar (a list of (start eighth, chord name)) at palindrome position 0..6."""
    side = ["Dm9", "Bbmaj7#11", "G13sus", None, "G13sus", "Bbmaj7#11", "Dm9"][mirror_pos]
    if side is None:
        return [(0, centre[0]), (4, centre[1])]
    if meter == 7:  # 4 + 3: the sus resolves sideways
        return [(0, side), (4, "Fmaj7/G")] if side == "G13sus" else [(0, side), (4, side)]
    return [(0, side)]


# ---------------- the head melody: bar k is the retrograde of bar 6-k ----------------
# (eighth offset, length in eighths, note); bars 0..3 are written, 4..6 are their mirrors.
HEAD = [
    [(0, 2, "A4"), (2, 1, "G4"), (3, 1, "F4"), (4, 2, "E4")],                     # 3/4  Dm9
    [(0, 1, "D5"), (1, 1, "E5"), (2, 3, "F5")],                                    # 5/8  Bbmaj7#11
    [(0, 1, "C5"), (1, 1, "D5"), (2, 1, "E5"), (3, 2, "A4"), (5, 2, "G4")],        # 7/8  G13sus | Fmaj7/G
    None,                                                                          # 4/4  the centre (per chord)
]


def centre_line(centre):
    """The centre bar's own palindrome on its two chords: up the first chord, mirrored down the second."""
    r0, v0, _ = CH[centre[0]]
    a = [r0 + 24 + v0[1], r0 + 24 + v0[2], r0 + 24 + v0[3]]
    return [(0, 1, nm(a[0])), (1, 1, nm(a[1])), (2, 2, nm(a[2])), (4, 2, nm(a[2])), (6, 1, nm(a[1])), (7, 1, nm(a[0]))]


def retro(line, meter):
    return sorted((meter - (o + ln), ln, n) for o, ln, n in line)


def head_bar(pos, meter, centre):
    if pos == 3:
        return centre_line(centre)
    if pos < 3:
        return HEAD[pos]
    return retro(HEAD[6 - pos], meter)


VOICE = ["tpt", "pno", "tom", "tpt", "tom", "pno", "tpt"]  # the colour palindrome


class Track:
    def __init__(self, name):
        self.name, self.ev = name, []

    def add(self, at, ln, head, vel, mark=""):
        self.ev.append((round(at, 4), max(0.05, round(ln, 4)), head, int(max(1, min(127, vel))), mark))

    def score(self, total):
        ev = sorted(self.ev, key=lambda e: (e[0], -e[3]))
        merged = []
        for e in ev:
            if merged and abs(merged[-1][0] - e[0]) < 1e-6:
                continue  # one event per onset (chords are written as one head)
            merged.append(e)
        toks, pos = [], 0.0
        for i, (s, ln, head, vel, mark) in enumerate(merged):
            nxt = merged[i + 1][0] if i + 1 < len(merged) else total
            ln = min(ln, nxt - s)
            if s - pos > 1e-4:
                toks.append(f"R/{s - pos:.4g}b")
            toks.append(f"{head}/{ln:.4g}b@{vel}" + (f"^{mark}" if mark else ""))
            pos = s + ln
        if total - pos > 1e-4:
            toks.append(f"R/{total - pos:.4g}b")
        return " ".join(toks)


def swing_at(bar_start, e8, swung):
    """Beat position of eighth e8 within a bar starting at bar_start (beats)."""
    b = bar_start + e8 / 2
    if swung and e8 % 2 == 1:
        b = bar_start + (e8 - 1) / 2 + SWING
    return b


def build():
    T = {k: Track(k) for k in ("tpt", "pno", "tom", "bass", "drums", "rhodes", "pno_lh")}
    bars = []   # (start beat, meter, pos, section, phrase index, centre)
    sec = []

    def add_phrase(section, meters, centre, pidx):
        start = bars[-1][0] + bars[-1][1] / 2 if bars else 0.0
        for pos, m in enumerate(meters):
            bars.append((start, m, pos, section, pidx, centre))
            start += m / 2

    form = [("intro", METERS, 2), ("head", METERS, 2), ("bridge", BRIDGE, 2), ("trade", METERS, 4),
            ("piano", BRIDGE, 2), ("peak", METERS, 2), ("head2", METERS, 2), ("coda", METERS, 2)]  # the form mirrors too
    p = 0
    for name, meters, n in form:
        first = len(bars)
        for k in range(n):
            add_phrase(name, meters, CENTRES[p % len(CENTRES)], p)
            p += 1
        sec.append((name, bars[first][0], len(bars) - first))
    total = bars[-1][0] + bars[-1][1] / 2 + 4.0  # a ring-out

    # dynamics: each phrase swells to its centre bar; sections set the level
    LEVEL = {"intro": 50, "head": 68, "bridge": 74, "trade": 84, "piano": 70, "peak": 104, "head2": 64, "coda": 48}
    # the bass's role per section: a two-feel under the heads, a pedal under the bridge, walking under the solos
    BASS = {"intro": "two", "head": "two", "bridge": "pedal", "trade": "walk", "piano": "walk", "peak": "walk",
            "head2": "two", "coda": "two"}

    def dyn(i):
        start, m, pos, section, pidx, centre = bars[i]
        return LEVEL[section] + 10 - 3 * abs(pos - 3)

    for i, (start, m, pos, section, pidx, centre) in enumerate(bars):
        swung = SWUNG[m]
        v = dyn(i)
        chords = bar_chords(m, centre, pos) if m in (5, 6, 7, 8) else [(0, "Dm9")]
        if section == "bridge":  # the bridge's meters are read from the centre: harmony follows its own mirror
            chords = bar_chords(m, centre, [3, 2, 1, 0, 1, 2, 3][pos] if pos != 3 else 0)
            if pos == 0 or pos == 6:
                chords = [(0, centre[0]), (4, centre[1])]
        name0 = chords[0][1]

        # ---- bass (fretless): its role changes by section; walking quarters in swung bars, grouped in odd ones ----
        role = BASS[section]
        if role == "pedal":
            T["bass"].add(start, m / 2 * 0.95, "D2", v - 6)
        elif role == "two":
            for ci, (c8, cn) in enumerate(chords):
                T["bass"].add(start + c8 / 2, ((chords[ci + 1][0] if ci + 1 < len(chords) else m) - c8) / 2 * 0.9,
                              nm(low(CH[cn][0])), v - 4)
        for ci, (c8, cn) in enumerate(chords if role == "walk" else []):
            root, voic, scale = CH[cn]
            end8 = chords[ci + 1][0] if ci + 1 < len(chords) else m
            if swung:
                for q8 in range(c8, end8, 2):
                    k = (q8 - c8) // 2
                    step = [0, scale[2] if len(scale) > 2 else 4, 7, 10 if 10 in scale else 9][k % 4]
                    note = low(root) + step
                    if q8 + 2 >= end8 and ci + 1 < len(chords):  # chromatic approach into the next chord
                        note = low(CH[chords[ci + 1][1]][0]) - 1
                    T["bass"].add(start + q8 / 2, 0.95, nm(note), v - 6)
            else:
                g8 = c8
                for gi, g in enumerate(GROUP[m]):
                    if g8 >= end8:
                        break
                    note = low(root) + (0 if gi == 0 else 7 if gi == 1 else 12)
                    T["bass"].add(start + g8 / 2, g / 2 * 0.9, nm(note), v - 4 + (4 if gi == 0 else 0))
                    g8 += g

        # ---- the melody (head sections), with the colour palindrome ----
        if section in ("head", "head2", "peak"):
            line = head_bar(pos, m, centre)
            if section == "head2" and pos == 3:   # the return: the centre bar a fifth lower, half time
                line = [(o, ln, nm(midi(n) - 7)) for o, ln, n in line]
            voice = VOICE[pos] if section != "peak" else ("tpt" if pos % 2 == 0 else "tom")
            for o, ln, n in line:
                at = swing_at(start, o, swung)
                T[voice].add(at, ln / 2 * 0.95, n if voice != "tom" else nm(midi(n) - 12), v + 4)
                if section == "peak" and voice == "tpt":  # unison in the piano an octave down at the peak
                    T["pno"].add(at, ln / 2 * 0.9, nm(midi(n) - 12), v)
        # ---- trading: trumpet takes the 3/4 and 7/8 bars, the tom choir the 5/8 and 4/4 ----
        if section == "trade":
            voice = "tpt" if m in (6, 7) else "tom"
            root, voic, scale = CH[name0]
            # a line built from the head's own cells, transposed onto this chord and varied per phrase
            cell = HEAD[[0, 1, 2, 2][min(pos, 3)]] if pos != 3 else centre_line(centre)
            shift = [0, 2, -3, 5][pidx % 4]
            for j, (o, ln, n) in enumerate(cell):
                if o >= m:
                    continue
                deg = scale[(j * 2 + pidx) % len(scale)]
                note = root + 24 + deg + shift if voice == "tpt" else root + 12 + deg
                at = swing_at(start, o, swung)
                T[voice].add(at, min(ln, m - o) / 2 * 0.9, nm(note), v + (6 if j == 0 else 0))
        # ---- piano: comping (rootless voicings), or the melody when VOICE says so ----
        comp = []
        for c8, cn in chords:
            root, voic, scale = CH[cn]
            vo = ",".join(nm(root + 12 + x) for x in voic) if root < 48 else ",".join(nm(root + x) for x in voic)
            comp.append((c8, vo))
        if section == "piano":  # piano solo: right hand lines over left-hand shells
            for c8, vo in comp:
                T["pno_lh"].add(start + c8 / 2, 1.0, vo, v - 10)
            root, voic, scale = CH[name0]
            for e8 in range(m):
                if (e8 + pidx) % 3 == 2:
                    continue  # breath: a rest every third eighth
                deg = scale[(e8 * 3 + pos + pidx) % len(scale)]
                note = root + 24 + deg + (12 if (e8 + pos) % 5 == 0 else 0)
                T["pno"].add(swing_at(start, e8, swung), 0.45, nm(note), v - 2 + (8 if e8 == 0 else 0))
        else:
            pattern = {6: [(1, 1), (4, 2)], 8: [(1, 1), (3, 1), (6, 2)], 5: [(0, 3)], 7: [(0, 2), (4, 3)]}[m]
            if pidx % 2:  # every other phrase: anticipations instead
                pattern = {6: [(0, 2), (5, 1)], 8: [(0, 2), (4, 1), (7, 1)], 5: [(3, 2)], 7: [(2, 2), (6, 1)]}[m]
            if not (section in ("head", "head2") and VOICE[pos] == "pno"):
                for o, ln in pattern:
                    cn_vo = [vo for c8, vo in comp if c8 <= o][-1]
                    T["pno_lh"].add(swing_at(start, o, swung), ln / 2 * 0.9, cn_vo, v - 16)
            else:
                T["pno_lh"].add(start, m / 2 * 0.9, comp[0][1], v - 16)
        # ---- rhodes through a Bassman stack: pads in the bridge, chords in the peak ----
        if section in ("bridge", "peak"):
            for c8, vo in comp:
                T["rhodes"].add(start + c8 / 2, (m - c8) / 2 * 0.95, vo, v - 8)

        # ---- drums: brushes (sticks at the peak) ----
        d = T["drums"]
        peak = section == "peak"
        if swung:
            beats = m // 2
            if not peak:
                d.add(start, beats * 0.95, "bsl" if section in ("intro", "coda") else "bs", v - 18)  # the sweep
            for bt in range(beats):
                if bt % 2 == 1 or (beats == 3 and bt == 2):
                    d.add(start + bt, 0.5, "st" if peak else "bt", v - 4)
                    d.add(start + bt, 0.5, "hf", v - 20)
                    if TRIP and bt >= 1 and not peak:  # the brush's triplet: two ghosts leading into the backbeat
                        d.add(start + bt - 2 / 3, 0.3, "bt", v - 24)
                        d.add(start + bt - 1 / 3, 0.3, "bt", v - 18)
                d.add(start + bt, 0.5, "rd", v - 14)                          # ride on the beat
                if bt % 2 == 1:
                    d.add(start + bt + SWING, 0.3, "rd", v - 22)               # and the skip
            d.add(start, 0.5, "k", v - 26 if not peak else v - 6)            # feathered
        else:
            g8 = 0
            for gi, g in enumerate(GROUP[m]):
                d.add(start + g8 / 2, g / 2 * 0.9, ("st" if peak else "bt") if gi else "k", v - (6 if gi else 18))
                if not peak and gi == 0:
                    d.add(start + g8 / 2, m / 2 * 0.9, "bs", v - 20)
                d.add(start + g8 / 2, 0.4, "rd", v - 16)
                g8 += g
        if peak and pos == 3:
            d.add(start, 0.5, "c", 110)
        if section == "coda" and pos == 6:
            d.add(start + 2, 2.0, "bsl", 60)

    # coda: the tom choir sings the head's opening cell backwards alone, the piano's last chord rings
    last = bars[-1][0] + bars[-1][1] / 2
    for k, (o, ln, n) in enumerate(reversed(HEAD[0])):
        T["tom"].add(last + o / 2, ln / 2, nm(midi(n) - 12), 70 - 3 * k)
    T["pno_lh"].add(last + 2.0, 2.0, "D3,A3,C4,E4,F4,G4", 62)
    T["bass"].add(last + 2.0, 2.0, "D2", 60)
    return total, bars, sec, T


def kit():
    snare = dict(type="drum", beater="brush", decay="0.32s", sharp=20, reso=1.45, cavity=0.3, reso_level=0.5,
                 shell=0.3, shell_hz=480, wires=0.5, gap=0.25, wire_tone="5.5k", strike=0.35, damp=0.3, slap=0.7,
                 stereo=0.4)

    def piece(pitch, layer, amp, gain="0dB", filters=("hp cutoff=90",)):
        return {"pitch": pitch, "gain": gain, "patch": {"synth": {"layers": [layer], "filters": list(filters),
                                                                    "amp": amp}, "play": {"vel_sens": 0.7}}}
    samp = {"a": "0.5ms", "d": "700ms", "s": 0, "r": "60ms", "curve": 2}
    return {"brush-kit": {
        "about": "chirper-two's brush kit for Odd Hours t4: room-kit's hats, ride and cymbals; snare and kick on the "
                 "physical drum layer (bd-7d117e): brush taps (bt), sweeps (bs, bsl), a stick snare for the peak (st), "
                 "a feathered felt kick.",
        "extends": "room-kit",
        "kit": {
            "bt": piece("E3", snare, samp),
            "bs": piece("E3", dict(snare, sweep="0.55s"), {"a": "20ms", "d": "900ms", "s": 0, "r": "80ms", "curve": 1}, "-3dB"),
            "bsl": piece("E3", dict(snare, sweep="1.2s"), {"a": "40ms", "d": "1.6s", "s": 0, "r": "120ms", "curve": 1}, "-3dB"),
            "st": piece("E3", dict(snare, beater="stick", slap=1.0), {"a": "0.2ms", "d": "450ms", "s": 0, "r": "40ms"}),
            "k": piece("G1", dict(type="drum", beater="felt", decay="0.5s", sharp=40, reso=1.0, cavity=0.25,
                                  reso_level=0.6, air=0.4, strike=0.25, damp=0.3, slap=0.3, stereo=0.2),
                       {"a": "0.5ms", "d": "600ms", "s": 0, "r": "40ms", "curve": 2}, "6dB", ("hp cutoff=45",)),
        }}}


def main():
    total, bars, sec, T = build()
    tom = {"synth": {"layers": [{"type": "drum", "beater": "stick", "contact": 1.5, "decay": "1.1s", "sharp": 35,
                                 "reso": 1.0, "cavity": 0.25, "tune_sounding": True, "reso_level": 0.5, "air": 0.45,
                                 "strike": 0.3, "shell": 0.25, "slap": 0.5, "stereo": 0.5}],
                     "filters": ["hp cutoff=60"], "amp": {"a": "0.3ms", "d": "1.4s", "s": 0, "r": "120ms", "curve": 3}},
           "play": {"vel_sens": 0.6}}
    tracks = [
        {"name": "trumpet", "patch": "trumpet-mute", "pan": 0.2, "gain": "-1dB",
         "fx": ["reverb kind=hall decay=1.8s mix=0.18"], "score": T["tpt"].score(total)},
        {"name": "piano", "patch": "piano-recorded", "pan": -0.15, "gain": "-2dB", "score": T["pno"].score(total)},
        {"name": "piano-lh", "patch": "piano-recorded", "pan": -0.25, "gain": "-6dB", "score": T["pno_lh"].score(total)},
        {"name": "toms", "patch": tom, "pan": -0.05, "gain": "3dB",
         "fx": ["reverb kind=room decay=0.9s mix=0.15"], "score": T["tom"].score(total)},
        {"name": "bass", "patch": "fretless", "gain": "-1dB", "score": T["bass"].score(total)},
        {"name": "drums", "patch": "brush-kit", "gain": "0dB", "fx": ["reverb kind=room decay=0.8s mix=0.12"],
         "score": T["drums"].score(total)},
        {"name": "rhodes", "patch": "rhodes-rotary", "pan": 0.3, "gain": "-11dB",
         "fx": [{"type": "amp", "model": "clean", "stack": "bassman", "gain": 0.35, "mix": 0.6}],
         "score": T["rhodes"].score(total)},
    ]
    secs = "; ".join(f"{n} from {s:.0f}b ({k} bars)" for n, s, k in sec)
    about = ("Chirpers - Odd Hours, track 4. Original composition by chirper-two, generated by "
             "compose/chirpers2/src/chirpers2-t4.py. A chamber-jazz brush trio with a singing tom choir; everything is "
             "a palindrome: meters 3/4 5/8 7/8 4/4 7/8 5/8 3/4, the harmony, the melody (each bar the retrograde of its "
             f"mirror) and the orchestration. 132 bpm. Sections: {secs}.")
    lines = [
        f"about: {json.dumps(about)}",
        "meta: " + json.dumps({"artist": "Chirpers", "album": "Odd Hours", "title": "Palindrome for Brushes and Toms",
                               "track": 4, "year": 2026}),
        f"tempo: {BPM}",
        f'length: "{total:g}b"',
        'ceiling: "-0.3dB"',
        'volume: "5dB"',
        "patches: " + json.dumps(kit()),
        "master: " + json.dumps({"fx": [{"type": "eq", "bands": ["hp cutoff=32", "peak cutoff=800 q=0.7 gain=-3dB",
                                                                   "highshelf cutoff=5000 gain=2dB"]},
                                        "glue threshold=-20dB ratio=1.3 attack=25ms release=250ms makeup=1dB"]}),
        "tracks:",
    ]
    lines += ["  - " + json.dumps(t) for t in tracks]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write("\n".join(lines) + "\n")
    print(f"wrote {OUT}: {len(bars)} bars, {total / BPM * 60:.1f} s; {secs}")


if __name__ == "__main__":
    main()
