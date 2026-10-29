#!/usr/bin/env python3
"""chirpers3-t6 (Tape Weather, track 6). Composed by chirper-two: WONKY BRUSH DRAG.

Bedroom-jazz lo-fi played by hand on a physical kit: no samples and no quantise.
- THE DRUMMER DRAGS: chirp's physical drum layer (bd-7d117e) with soft mallets and brushes. A felt kick pushed a
  little early, a mallet snare dragged late, brush taps drifting off the swung sixteenths (a seeded drunk walk, the
  same every render), brush sweeps under it all, mallet-tom fills at phrase ends.
- THE TAPE WARPS: the wurli goes through a slow chorus at full wet (wow), a fast shallow one (flutter), tape
  saturation, a worn top and a little bit-crush. The drop deepens the wow until the chords seasick.
- THE CHORDS SINK: Fmaj9 | Em7 | Ebmaj7#11 | Dm9, a semitone a bar; the switch-up sinks a fourth lower (Bbmaj9 |
  Am7 | Abmaj7#11 | G13sus) in half time.
- DUSTY VIBES: Odd Hours t8's vibraphone (borrowed) behind a lo-pass, a falling three-note sigh, late.
- Vinyl crackle (synthesised: sparse noise ticks) and hiss throughout.
Form: intro (radio-muffled keys) / A / switch-up (half time) / A2 / drop (the warp) / A3 / outro.

Emits songs/chirpers3-t6.yaml. Edit the music here.
"""
import json
import os
import random

OUT = os.environ.get("T6_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers3-t6.yaml")
BPM = 78
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


class Track:
    def __init__(self, name):
        self.name, self.ev = name, []

    def add(self, at, ln, head, vel):
        self.ev.append((round(max(0.0, at), 4), max(0.05, round(ln, 4)), head, int(max(1, min(127, vel)))))

    def score(self, total):
        ev = sorted(self.ev, key=lambda e: (e[0], -e[3]))
        merged = []
        for e in ev:
            if e[0] >= total - 1e-6:
                continue
            if merged and abs(merged[-1][0] - e[0]) < 1e-3:
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


# chords: (bass root midi, voicing midis)
A_LOOP = [(41, [57, 60, 64, 67]),   # Fmaj9: F2 | A3 C4 E4 G4
          (40, [55, 59, 62, 66]),   # Em7(9): E2 | G3 B3 D4 F#4
          (39, [55, 58, 62, 69]),   # Ebmaj7#11: Eb2 | G3 Bb3 D4 A4
          (38, [53, 57, 60, 64])]   # Dm9: D2 | F3 A3 C4 E4
A_TURN = (45, [55, 61, 65, 68])     # A7b13 (the fourth bar of every other phrase leans home)
B_LOOP = [(34, [50, 53, 57, 60]),   # Bbmaj9: Bb1 | D3 F3 A3 C4
          (33, [48, 52, 55, 59]),   # Am7(9)
          (32, [48, 51, 55, 62]),   # Abmaj7#11
          (31, [53, 57, 60, 64])]   # G13sus: G1 | F3 A3 C4 E4

FORM = [("intro", 4), ("A", 16), ("switch", 8), ("A2", 16), ("drop", 4), ("A3", 12), ("outro", 4)]
LEVEL = {"intro": 58, "A": 72, "switch": 66, "A2": 78, "drop": 56, "A3": 80, "outro": 56}
DRUMS = {"A", "switch", "A2", "A3"}


def build():
    rng = random.Random(6)
    T = {k: Track(k) for k in ("keys", "bass", "sub", "vibes", "drums", "crackle", "hiss")}
    bars, b = [], 0
    for name, n in FORM:
        for i in range(n):
            bars.append((b * 4.0, name, i, n))
            b += 1
    total = len(bars) * 4.0
    drift = 0.0
    for start, sec, i, n in bars:
        v = LEVEL[sec]
        if sec == "switch":
            root, voic = B_LOOP[(i // 2) % 4]  # half time: a chord every two bars
        else:
            root, voic = A_LOOP[i % 4]
            if i % 8 == 7 and sec in ("A", "A2", "A3"):
                root, voic = A_TURN
        # ---- keys: the chord a hair late, strummed; a soft re-hit on the and of three ----
        drag = 0.05 if sec != "intro" else 0.0
        T["keys"].add(start + drag, 2.4 if sec != "switch" else 3.8, ",".join(nm(x) for x in voic), v - 6)
        if sec in ("A", "A2", "A3") and i % 2 == 1:
            T["keys"].add(start + 2.5 + drag, 1.3, ",".join(nm(x) for x in voic[1:]), v - 18)
        if sec in ("intro", "drop", "outro"):
            T["keys"].add(start + 2.0 + drag, 1.9, ",".join(nm(x) for x in voic[:3]), v - 14)
        # ---- bass: behind the beat ----
        if sec in DRUMS:
            late = 0.04
            T["sub"].add(start + late, 3.6 if sec == "switch" and i % 2 == 0 else 1.6, nm(root - 12), v - 4)
            if sec == "switch":
                if i % 2 == 0:
                    T["bass"].add(start + late, 3.6, nm(root), v - 2)
                else:
                    T["bass"].add(start + 2.5 + late, 1.2, nm(root + 7), v - 10)
            else:
                T["bass"].add(start + late, 1.4, nm(root), v - 2)
                T["bass"].add(start + 1.75 + late, 0.6, nm(root + 12 if i % 2 else root + 7), v - 12)
                T["bass"].add(start + 2.5 + late, 1.2, nm(root + 7), v - 8)
                if i % 4 == 3:
                    T["bass"].add(start + 3.5 + late, 0.45, nm(root + 1 if i % 8 == 7 else root - 1), v - 10)
        # ---- dusty vibes: a falling three-note sigh, late, every other bar of the A sections ----
        if sec in ("A2", "A3") and i % 2 == 0 or (sec == "A" and i % 4 == 2):
            top = sorted(voic)[-1] + 12
            sigh = [top, top - 3 if (top - 3) % 12 in {x % 12 for x in voic} else top - 4, top - 5]
            for k, (o, nn) in enumerate(zip((1.55, 1.95, 2.75), sigh)):
                T["vibes"].add(start + o + rng.uniform(-0.02, 0.04), 0.9 if k == 2 else 0.4, nm(nn), v - 10 - 3 * k)
        # ---- the drummer ----
        d = T["drums"]
        if sec in DRUMS:
            drift = max(-0.03, min(0.03, drift + rng.uniform(-0.012, 0.012)))
            half = sec == "switch"
            kicks = [0.0, 2.5] if half else ([0.0, 1.625, 2.5] if i % 4 != 3 else [0.0, 1.625, 2.375, 2.75])
            for kb in kicks:
                d.add(start + kb - 0.035, 0.5, "k", v + (4 if kb == 0 else -6))
            for sb in ([2.0] if half else [1.0, 3.0]):
                d.add(start + sb + 0.09 + drift, 0.5, "ms", v - 2)
            for s16 in range(16 if not half else 0):  # brush taps on the swung sixteenths, drifting
                pos16 = s16 // 2 * 0.5 + (0.33 if s16 % 2 else 0.0)
                if s16 % 2 and rng.random() < (0.1 if sec == "A3" else 0.45):
                    continue
                vel = v - (14 if s16 % 4 == 0 else 22 if s16 % 2 == 0 else 30)
                d.add(start + pos16 + drift + rng.uniform(-0.02, 0.02), 0.2, "bt", vel)
            d.add(start, 1.9, "bs", v - 22)
            d.add(start + 2.0, 1.9, "bs", v - 24)
            if i % 4 == 3 and not half:  # a mallet-tom fill dragging into the next bar
                for k, (o, piece) in enumerate(((3.25, "mt1"), (3.5, "mt1"), (3.75, "mt2"))):
                    d.add(start + o + 0.03 * k, 0.3, piece, v - 6 - 2 * k)
            if half and i % 2 == 1:
                d.add(start + 3.5 + 0.05, 0.3, "rc", v - 10)
        elif sec == "drop":
            d.add(start, 3.8, "bs", v - 18)
        # ---- vinyl crackle and hiss ----
        for _ in range(rng.randint(5, 11)):
            T["crackle"].add(start + rng.uniform(0, 3.95), 0.06, "C5", rng.randint(30, 80))
    T["hiss"].add(0.0, total - 0.1, "C4", 60)
    sec = []
    for name, n in FORM:
        first = next(bb for bb in bars if bb[1] == name)
        sec.append((name, first[0], n))
    return total, bars, sec, T


def patches():
    def drum(pitch, layer, amp, gain="0dB", filters=("hp cutoff=40",)):
        return {"pitch": pitch, "gain": gain, "patch": {"synth": {"layers": [layer], "filters": list(filters),
                                                                    "amp": amp}, "play": {"vel_sens": 0.7}}}
    brush = dict(type="drum", beater="brush", decay="0.3s", sharp=20, reso=1.4, cavity=0.3, reso_level=0.5,
                 shell=0.3, shell_hz=470, wires=0.45, gap=0.25, wire_tone="5k", strike=0.35, damp=0.35, slap=0.6,
                 stereo=0.35)
    kit = {"about": "chirper-two's lo-fi hand kit for Tape Weather t6: chirp's physical drum layer with soft mallets "
                    "and brushes (no samples): a felt kick, a mallet snare, brush taps and sweeps, mallet toms, a rim.",
           "extends": "room-kit",
           "kit": {
               "k": drum("D1", dict(type="drum", beater="felt", decay="0.55s", sharp=35, reso=1.0, cavity=0.25,
                                    reso_level=0.6, air=0.45, strike=0.2, damp=0.35, slap=0.25, stereo=0.15),
                         {"a": "0.5ms", "d": "650ms", "s": 0, "r": "50ms", "curve": 2}, "10dB", ("hp cutoff=28",)),
               "ms": drum("D3", dict(brush, beater="felt", contact=1.4, wires=0.5, decay="0.28s", slap=0.5),
                          {"a": "0.5ms", "d": "500ms", "s": 0, "r": "60ms", "curve": 2}, "-2dB", ("hp cutoff=90",)),
               "bt": drum("E3", brush, {"a": "0.5ms", "d": "600ms", "s": 0, "r": "60ms", "curve": 2}, "-2dB",
                          ("hp cutoff=120",)),
               "bs": drum("E3", dict(brush, sweep="0.9s"), {"a": "30ms", "d": "1.2s", "s": 0, "r": "100ms", "curve": 1},
                          "-5dB", ("hp cutoff=150",)),
               "mt1": drum("A2", dict(type="drum", beater="felt", decay="0.6s", sharp=30, reso=1.0, cavity=0.2,
                                      tune_sounding=True, reso_level=0.5, air=0.4, strike=0.3, damp=0.3, slap=0.3,
                                      stereo=0.4), {"a": "0.5ms", "d": "800ms", "s": 0, "r": "80ms", "curve": 2}),
               "mt2": drum("E2", dict(type="drum", beater="felt", decay="0.7s", sharp=30, reso=1.0, cavity=0.2,
                                      tune_sounding=True, reso_level=0.5, air=0.4, strike=0.3, damp=0.3, slap=0.3,
                                      stereo=0.4), {"a": "0.5ms", "d": "900ms", "s": 0, "r": "80ms", "curve": 2}),
               "rc": drum("E3", dict(brush, beater="stick", strike=0.95, damp=0.8, wires=0.2, slap=1.0),
                          {"a": "0.2ms", "d": "120ms", "s": 0, "r": "30ms"}, "-4dB", ("hp cutoff=300",)),
           }}
    vibes = {"about": "Odd Hours t8's vibraphone (chirper-two), borrowed: partials 1 / 4 / 10, a 5.2 Hz motor.",
             "synth": {"layers": [{"name": "bar", "type": "additive", "partials": [[1, 1], [4.0, 0.16], [10.0, 0.025]],
                                   "level": {"value": "0dB", "mod": [{"src": "lfo.motor", "amount": 3}]}}],
                       "lfo": {"motor": {"wave": "sine", "rate": "5.2hz"}},
                       "filters": ["hp cutoff=150", "lp cutoff=7k"],
                       "amp": {"a": "2ms", "d": "3.2s", "s": 0, "r": "500ms", "curve": 2}},
             "play": {"vel_sens": 0.55}}
    crackle = {"about": "chirper-two's vinyl crackle: a 3 ms noise tick, high-passed.",
               "synth": {"layers": [{"name": "tick", "type": "noise"}], "filters": ["hp cutoff=1800", "lp cutoff=9k"],
                         "amp": {"a": "0.1ms", "d": "3ms", "s": 0, "r": "2ms"}}, "play": {"vel_sens": 1.0}}
    hiss = {"about": "chirper-two's tape hiss: a quiet band of noise.",
            "synth": {"layers": [{"name": "hiss", "type": "noise"}], "filters": ["hp cutoff=3000", "lp cutoff=10k"],
                      "amp": {"a": "2s", "d": "1s", "s": 1.0, "r": "3s"}}}
    sub = {"about": "chirper-two's sub: a sine an octave under the fretless's long notes.",
           "synth": {"layers": [{"name": "sub", "wave": "sine"}], "amp": {"a": "140ms", "d": "500ms", "s": 0.8, "r": "200ms"}}}
    return {"c2-lofi-kit": kit, "c2-vibes": vibes, "c2-crackle": crackle, "c2-hiss": hiss, "c2-sub": sub}


def main():
    total, bars, sec, T = build()
    wow = {"type": "chorus", "rate": 0.35, "depth": 0.55, "voices": 1, "mix": 1.0}
    flutter = {"type": "chorus", "rate": 5.5, "depth": 0.08, "voices": 1, "mix": 0.5}
    tracks = [
        {"name": "keys", "patch": "wurli", "pan": -0.1, "gain": "-6dB",
         "fx": [wow, flutter, "tape drive=0.3 warmth=0.65", "lp cutoff=5000",
                {"type": "crush", "bits": 12, "rate": 16000, "mix": 0.3},
                "reverb kind=room decay=1.2s mix=0.18"], "score": T["keys"].score(total)},
        {"name": "bass", "patch": "fretless", "gain": "1dB", "fx": ["lp cutoff=900", "tape drive=0.2 warmth=0.5"],
         "score": T["bass"].score(total)},
        {"name": "sub", "patch": "c2-sub", "gain": "-5dB", "score": T["sub"].score(total)},
        {"name": "vibes", "patch": "c2-vibes", "pan": 0.3, "gain": "-6dB",
         "fx": [wow, "lp cutoff=2600", "reverb kind=hall decay=2.2s mix=0.3"], "score": T["vibes"].score(total)},
        {"name": "drums", "patch": "c2-lofi-kit", "gain": "0dB",
         "fx": ["tape drive=0.35 warmth=0.6", "lp cutoff=11000",
                {"type": "crush", "bits": 12, "rate": 18000, "mix": 0.25},
                "reverb kind=room decay=0.7s mix=0.12"], "score": T["drums"].score(total)},
        {"name": "crackle", "patch": "c2-crackle", "pan": 0.05, "gain": "-20dB", "score": T["crackle"].score(total)},
        {"name": "hiss", "patch": "c2-hiss", "gain": "-36dB", "score": T["hiss"].score(total)},
    ]
    secs = "; ".join(f"{n} from {s:.0f}b ({k} bars)" for n, s, k in sec)
    about = ("Chirpers - Tape Weather, track 6. Original composition by chirper-two, generated by "
             "compose/chirpers3/src/chirpers3-t6.py. Wonky brush drag: bedroom-jazz lo-fi on a physical soft-mallet "
             "and brush kit, unquantised (kick early, snare late, brushes drifting), tape-warped wurli chords sinking "
             f"a semitone a bar, a lazy fretless, dusty vibes, crackle and hiss. 78 bpm. Sections: {secs}.")
    lines = [
        f"about: {json.dumps(about)}",
        "meta: " + json.dumps({"artist": "Chirpers", "album": "Tape Weather", "title": "Late on Purpose", "track": 6,
                               "year": 2026}),
        f"tempo: {BPM}",
        f'length: "{total:g}b"',
        'tail: "3s"',
        'ceiling: "-0.5dB"',
        'volume: "3dB"',
        "patches: " + json.dumps(patches()),
        "master: " + json.dumps({"fx": [{"type": "eq", "bands": ["hp cutoff=30", "highshelf cutoff=8000 gain=0dB"]},
                                        "tape drive=0.2 warmth=0.5",
                                        "glue threshold=-20dB ratio=1.6 attack=20ms release=250ms makeup=1dB"]}),
        "tracks:",
    ]
    lines += ["  - " + json.dumps(t) for t in tracks]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write("\n".join(lines) + "\n")
    print(f"wrote {OUT}: {len(bars)} bars, {total / BPM * 60:.1f} s; {secs}")


if __name__ == "__main__":
    main()
