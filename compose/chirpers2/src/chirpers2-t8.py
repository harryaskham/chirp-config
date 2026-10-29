#!/usr/bin/env python3
"""chirpers2-t8 (Odd Hours, track 8). Composed by chirper-two: MALLET CHAMBER IN PHASE.

A kit-less vibes-and-marimba quartet: process music meets chamber jazz.
- CELL: one 12-eighth figure on two marimbas, written as scale degrees over the chord (in Eb lydian:
  Eb4 Bb4 F5 Bb4 G4 Bb4 | C5 Bb4 F4 Bb4 G4 D5). Marimba 2 plays the same cell, PHASED: it steps one eighth ahead
  every four bars, and the fourth bar of each step blurs half an eighth ahead (a sixteenth off the grid), so the two
  parts slide out of unison through every offset. After twelve steps the process comes back to unison.
- 12/8 AGAINST 4/4: the marimbas and the frame drum feel the bar in four dotted quarters; the bowed bass walks half
  notes in 4/4 (an 8-beat cycle against the 6-beat bar, realigning every four bars, where the chord changes).
- VIBES (motor tremolo): a long melody whose every four-bar phrase is a PALINDROME (pitches and durations read the
  same backwards: Palindrome for Brushes and Toms' idea, t4), sung over the phasing.
- HARMONY moves slowly, four bars a chord: Ebmaj7#11 | Cm9 | Abmaj9 | Bb13sus (one diatonic collection, the A of
  Eb lydian turning to Ab); the bridge goes up a minor third (Gbmaj7#11 | Ebm9 | Bmaj9 | Db13sus) and inverts the cell.
- FORM (seven sections): cell / phase / melody / bridge / peak / unison / coda.
The frame drum is chirp's physical membrane (`type: drum`, one head, felt and brush): dum, tek and sweeps.

Emits songs/chirpers2-t8.yaml. Edit the music here.
"""
import json
import os

OUT = os.environ.get("T8_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers2-t8.yaml")
BPM = 112
BAR = 6.0  # a 12/8 bar, in quarter beats

NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


SCALES = {"maj7#11": [0, 2, 4, 6, 7, 9, 11], "m9": [0, 2, 3, 5, 7, 9, 10], "maj9": [0, 2, 4, 5, 7, 9, 11],
          "13sus": [0, 2, 4, 5, 7, 9, 10]}
HOME = [(63, "maj7#11"), (60, "m9"), (68, "maj9"), (58, "13sus")]     # Eb4, C4, Ab4, Bb3
BRIDGE = [(66, "maj7#11"), (63, "m9"), (59, "maj9"), (61, "13sus")]   # Gb4, Eb4, B3, Db4


def deg(chord, d):
    root, kind = chord
    sc = SCALES[kind]
    return root + 12 * (d // 7) + sc[d % 7]


CELL = [0, 4, 8, 4, 2, 4, 5, 4, 1, 4, 2, 6]
CELL_INV = [8 - d for d in CELL]  # the bridge's cell: the same figure upside down

# Vibes half-phrases: (degree above the chord's root an octave up, eighths); each sums to 24 and is mirrored.
HALVES = [
    [(4, 6), (5, 3), (6, 3), (8, 4), (9, 2), (7, 6)],
    [(2, 4), (4, 2), (7, 6), (6, 3), (4, 3), (5, 6)],
    [(9, 6), (8, 2), (6, 4), (4, 3), (5, 3), (1, 6)],
    [(0, 3), (2, 3), (4, 6), (7, 4), (11, 2), (9, 6)],
]


def palindrome(half):
    """half + its retrograde; the centre note (end of half, start of the mirror) is one held note."""
    back = list(reversed(half))
    return half[:-1] + [(half[-1][0], half[-1][1] * 2)] + back[1:]


class Track:
    def __init__(self, name):
        self.name, self.ev = name, []

    def add(self, at, ln, head, vel):
        self.ev.append((round(at, 4), max(0.05, round(ln, 4)), head, int(max(1, min(127, vel)))))

    def score(self, total):
        ev = sorted(self.ev, key=lambda e: (e[0], -e[3]))
        merged = []
        for e in ev:
            if e[0] >= total - 1e-6:
                continue
            if merged and abs(merged[-1][0] - e[0]) < 1e-6:
                continue
            merged.append(e)
        toks, pos = [], 0.0
        for i, (s, ln, head, vel) in enumerate(merged):
            nxt = merged[i + 1][0] if i + 1 < len(merged) else total
            ln = min(ln, nxt - s)
            if s - pos > 1e-4:
                toks.append(f"R/{s - pos:.4g}b")
            toks.append(f"{head}/{ln:.4g}b@{vel}")
            pos = s + ln
        if total - pos > 1e-4:
            toks.append(f"R/{total - pos:.4g}b")
        return " ".join(toks)


FORM = [("cell", 4), ("phase", 16), ("melody", 16), ("bridge", 16), ("peak", 16), ("unison", 8), ("coda", 6)]
LEVEL = {"cell": 70, "phase": 76, "melody": 82, "bridge": 74, "peak": 96, "unison": 80, "coda": 60}


def build():
    T = {k: Track(k) for k in ("m1", "m2", "vib", "bass", "sub", "fd")}
    bars, b = [], 0
    for name, n in FORM:
        for i in range(n):
            bars.append((b * BAR, name, i, n))
            b += 1
    total = len(bars) * BAR
    step = 0  # marimba 2's phase offset in eighths; it climbs 0..11 over phase, melody and peak
    for bi, (start, sec, i, n) in enumerate(bars):
        v = LEVEL[sec]
        prog = BRIDGE if sec == "bridge" else HOME
        chord = prog[(i // 4) % 4] if sec not in ("cell", "coda") else HOME[0]
        if sec == "coda":
            chord = HOME[i // 2 % 2 * 0]  # the coda rests on the home chord
        cell = CELL_INV if sec == "bridge" else CELL
        # ---- the marimbas ----
        if sec != "coda":
            for e in range(12):
                acc = 10 if e % 3 == 0 else 0
                T["m1"].add(start + e / 2, 0.45, nm(deg(chord, cell[e]) - 12), v - 8 + acc)  # the low marimba
        if sec in ("phase", "melody", "peak"):
            k = {"phase": 0, "melody": 4, "peak": 8}[sec] + i // 4
            off = k + (0.5 if i % 4 == 3 else 0.0)  # the blur bar: half an eighth on toward the next step
            for e in range(12):
                at = start + ((e + off) % 12) / 2
                T["m2"].add(at, 0.45, nm(deg(chord, cell[e])), v - 12 + (8 if e % 3 == 0 else 0))
        elif sec == "unison" or (sec == "bridge" and i < 8):
            for e in range(12):
                T["m2"].add(start + e / 2, 0.45, nm(deg(chord, cell[e]) + (0 if sec == "unison" else 12)), v - 14)
        elif sec == "bridge":  # canon at half a bar, a third above
            for e in range(12):
                T["m2"].add(start + ((e + 6) % 12) / 2, 0.45, nm(deg(chord, cell[e] + 2)), v - 12)
        # ---- the vibes ----
        if sec in ("melody", "peak", "unison") and i % 4 == 0:
            half = HALVES[(i // 4 + (2 if sec == "peak" else 0)) % 4]
            phrase = palindrome(half)
            at, mid = start, len(phrase) // 2
            for j, (d, ln) in enumerate(phrase):
                swell = 12 - 4 * abs(j - mid)  # dynamics mirror too: up to the centre, back down
                T["vib"].add(at, ln / 2 * 0.98, nm(deg(chord, d) + 12), v - 4 + swell)
                at += ln / 2
        elif sec == "bridge" and i % 4 == 0:
            for j, d in enumerate([4, 6, 9, 8, 8, 9, 6, 4]):
                T["vib"].add(start + j * 3, 2.9, nm(deg(chord, d) + 12), v - 10 + (6 if j in (3, 4) else 0))
        elif sec == "coda" and i == 0:  # one mirror, slowed by a quarter: five bars of the six
            phrase = palindrome(HALVES[0][:3] + [(9, 6)])  # a short mirror, slowing
            at = start
            for d, ln in phrase:
                T["vib"].add(at, ln / 2 * 1.2, nm(deg(HOME[0], d) + 12), v)
                at += ln / 2 * 1.25
        # ---- the bowed bass: half notes in 4/4 against the 12/8 ----
        if sec in ("phase", "melody", "peak", "unison") and not (sec == "phase" and i < 4):
            for h in range(3):
                beat = start + 2 * h
                cyc = int(round(beat / 2)) % 4  # position in the 8-beat (4/4 bar) cycle
                d = [0, 4, 1, 2][cyc] if (i % 4) < 3 else [0, 6, 5, 4][cyc]
                note = deg((chord[0] - 24 if chord[0] - 24 >= 28 else chord[0] - 12, chord[1]), d)
                acc = 10 if cyc == 0 else 0
                head = nm(note) + ("," + nm(note + 12) if sec == "peak" and cyc == 0 else "")
                T["bass"].add(beat, 1.95, head, v - 10 + acc)
                if cyc in (0, 2):  # the sub: the 4/4 bar's strong beats an octave under the bow
                    T["sub"].add(beat, 1.9, nm(note - 12 if note - 12 >= 24 else note), v - 8 + acc)
        elif sec == "bridge":
            root = chord[0] - 24 if chord[0] - 24 >= 28 else chord[0] - 12
            bn = root if i % 2 == 0 else deg((root, chord[1]), 4)
            T["bass"].add(start, BAR * 0.98, nm(bn), v - 6)
            T["sub"].add(start, BAR * 0.95, nm(bn - 12 if bn - 12 >= 24 else bn), v - 10)
        elif sec == "coda" and i < 4:
            T["bass"].add(start, BAR * 0.98, nm(HOME[0][0] - 24), v - 14)
        # ---- the frame drum ----
        fd = T["fd"]
        if sec == "cell" and i >= 2:
            fd.add(start, 1, "dum", v - 14)
        elif sec in ("phase", "melody", "unison"):
            fd.add(start, 1, "dum", v - 6)
            fd.add(start + 3, 1, "dum", v - 12)
            fd.add(start + 1.5, 0.5, "tek", v - 12)
            fd.add(start + 4.5, 0.5, "tek", v - 10)
            if sec == "melody":
                for e in (2, 5, 8, 11):
                    fd.add(start + e / 2, 0.3, "gh", v - 30)
        elif sec == "bridge":
            fd.add(start, 3, "sw", v - 10)
            fd.add(start + 3, 3, "sw", v - 16)
        elif sec == "peak":
            fd.add(start, 1, "dum", v - 2)
            fd.add(start + 3, 1, "dum", v - 8)
            for e in (3, 9):
                fd.add(start + e / 2, 0.5, "tek", v - 6)
            for e in (2, 5, 8, 11):
                fd.add(start + e / 2, 0.25, "gh", v - 26)
            fd.add(start + 4.75, 0.25, "tek", v - 16)  # a sixteenth grace into the third dotted quarter
            if i % 4 == 3:
                fd.add(start + 5, 1, "sw", v - 12)
        elif sec == "coda" and i == 0:
            fd.add(start, 6, "sw", v - 18)
    sec = []
    for name, n in FORM:
        first = next(bb for bb in bars if bb[1] == name)
        sec.append((name, first[0], n))
    return total, bars, sec, T


def patches():
    marimba = {"about": "Cross Purposes' marimba (chirper-three, Odd Hours t7), borrowed: additive wooden-bar "
                        "partials 1 / 3.93 / 9.2 with a mallet click.",
               "synth": {"layers": [{"name": "bar", "type": "additive", "partials": [[1, 1], [3.93, 0.32], [9.2, 0.07]]},
                                    {"name": "click", "type": "noise", "level": {"value": "-70dB", "mod": [{"src": "env.ck", "amount": 40}]}}],
                         "env": {"ck": {"a": "0.2ms", "d": "5ms", "s": 0}}, "filters": ["hp cutoff=120"],
                         "amp": {"a": "1ms", "d": "650ms", "s": 0, "r": "80ms", "curve": 3}},
               "play": {"vel_sens": 0.6}}
    vibes = {"about": "chirper-two's vibraphone for Odd Hours t8: aluminium-bar partials 1 / 4 / 10 (tuned bars), a "
                      "soft yarn-mallet tick, a long ring, and the MOTOR: a 5.2 Hz tremolo on the bar.",
             "synth": {"layers": [{"name": "bar", "type": "additive", "partials": [[1, 1], [4.0, 0.16], [10.0, 0.025]],
                                   "level": {"value": "0dB", "mod": [{"src": "lfo.motor", "amount": 3}]}},
                                  {"name": "tick", "type": "noise", "level": {"value": "-72dB", "mod": [{"src": "env.tk", "amount": 36}]}}],
                       "env": {"tk": {"a": "0.3ms", "d": "4ms", "s": 0}},
                       "lfo": {"motor": {"wave": "sine", "rate": "5.2hz"}},
                       "filters": ["hp cutoff=150", "lp cutoff=7k"],
                       "amp": {"a": "2ms", "d": "3.2s", "s": 0, "r": "500ms", "curve": 2}},
             "play": {"vel_sens": 0.55}}
    head = dict(type="drum", beater="felt", decay="0.7s", sharp=25, strike=0.2, damp=0.25, slap=0.4, air=0.3,
                stereo=0.3)

    def piece(pitch, layer, amp, gain="0dB"):
        return {"pitch": pitch, "gain": gain, "patch": {"synth": {"layers": [layer], "filters": ["hp cutoff=55"],
                                                                    "amp": amp}, "play": {"vel_sens": 0.7}}}
    frame = {"about": "chirper-two's frame drum for Odd Hours t8: one physical membrane (bd-7d117e), low: a felt "
                      "'dum' in the centre, a 'tek' near the rim, finger ghosts and brush sweeps.",
             "extends": "room-kit",
             "kit": {"dum": piece("E2", dict(head, decay="0.9s"), {"a": "0.5ms", "d": "1.1s", "s": 0, "r": "80ms", "curve": 2}, "8dB"),
                     "tek": piece("A2", dict(head, strike=0.85, sharp=40, contact=0.6, damp=0.45),
                                  {"a": "0.3ms", "d": "300ms", "s": 0, "r": "40ms"}),
                     "gh": piece("A2", dict(head, strike=0.7, damp=0.6, contact=0.5),
                                 {"a": "0.3ms", "d": "150ms", "s": 0, "r": "30ms"}, "-4dB"),
                     "sw": piece("A2", dict(head, beater="brush", sweep="1.4s", strike=0.5),
                                 {"a": "60ms", "d": "1.8s", "s": 0, "r": "200ms", "curve": 1}, "-2dB")}}
    sub = {"about": "chirper-two's sub for Odd Hours t8: a soft sine an octave under the bowed bass (after chirper-three's "
                    "c3-sub in Cross Purposes).",
           "synth": {"layers": [{"name": "sub", "wave": "sine"}], "amp": {"a": "30ms", "d": "400ms", "s": 0.75, "r": "150ms"}}}
    return {"c3-marimba": marimba, "c2-vibes": vibes, "c2-frame": frame, "c2-sub": sub}


def main():
    total, bars, sec, T = build()
    hall = "reverb kind=hall decay=2.4s mix=0.22 predelay=20ms"
    tracks = [
        {"name": "marimba-1", "patch": "c3-marimba", "pan": -0.5, "gain": "-3dB", "fx": [hall], "score": T["m1"].score(total)},
        {"name": "marimba-2", "patch": "c3-marimba", "pan": 0.5, "gain": "-4dB", "fx": [hall], "score": T["m2"].score(total)},
        {"name": "vibes", "patch": "c2-vibes", "pan": 0.05, "gain": "0dB", "fx": [hall], "score": T["vib"].score(total)},
        {"name": "bass", "patch": "tagelharpa-bass-bowed", "pan": -0.05, "gain": "1dB", "score": T["bass"].score(total)},
        {"name": "sub", "patch": "c2-sub", "gain": "-8dB", "score": T["sub"].score(total)},
        {"name": "frame", "patch": "c2-frame", "pan": 0.15, "gain": "0dB",
         "fx": ["reverb kind=room decay=1.0s mix=0.15"], "score": T["fd"].score(total)},
    ]
    secs = "; ".join(f"{n} from {s:.0f}b ({k} bars)" for n, s, k in sec)
    about = ("Chirpers - Odd Hours, track 8. Original composition by chirper-two, generated by "
             "compose/chirpers2/src/chirpers2-t8.py. Mallet chamber in phase: two marimbas phase one 12-eighth cell "
             "through all twelve offsets and back to unison; vibes sing palindromic phrases; a bowed bass walks 4/4 "
             f"against the 12/8; a physical frame drum. 112 bpm. Sections: {secs}.")
    lines = [
        f"about: {json.dumps(about)}",
        "meta: " + json.dumps({"artist": "Chirpers", "album": "Odd Hours", "title": "Mallet Chamber in Phase",
                               "track": 8, "year": 2026}),
        f"tempo: {BPM}",
        'meter: "12/8"',
        f'length: "{total:g}b"',
        'tail: "3s"',
        'ceiling: "-0.3dB"',
        'volume: "4dB"',
        "patches: " + json.dumps(patches()),
        "master: " + json.dumps({"fx": [{"type": "eq", "bands": ["hp cutoff=35", "highshelf cutoff=6000 gain=-1.5dB"]},
                                        "glue threshold=-20dB ratio=1.4 attack=20ms release=250ms makeup=1dB"]}),
        "tracks:",
    ]
    lines += ["  - " + json.dumps(t) for t in tracks]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write("\n".join(lines) + "\n")
    print(f"wrote {OUT}: {len(bars)} bars, {total / BPM * 60:.1f} s; {secs}")


if __name__ == "__main__":
    main()
