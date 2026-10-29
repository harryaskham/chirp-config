#!/usr/bin/env python3
"""chirpers3-t8 (Tape Weather, track 8) - generator for songs/chirpers3-t8.yaml (chirper-zero).

NIGHT-BUS 2-STEP: lo-fi UK garage at 2 a.m. A shuffled, skippy 2-step beat at 136 bpm under a worn minor-ninth loop
(F#m9 | Dmaj9 | Bm11 | C#7sus) and wordless chopped voices; the city going past the window. Original; a style, not a
version of any track.

Form: intro (pad, vinyl, the first chops) / groove (the 2-step: kick on 1 and a wandering skip-kick, claps on 2 and 4,
swung 16th hats, the sub following the kick) / groove 2 (the chops answering every clap) / breakdown (the beat gone:
pad and voices) / groove 3 (the beat back, the chops an octave up) / outro (thinning to the pad and the vinyl).

Motifs (compose/chirpers3/motifs.md):
  SKIP      the 2-step bar on the 16th grid: kick 0 and a skip-kick at 10, 11 or 7 (it wanders by bar), claps 4 and 12,
            hats 0 2 3 6 8 10 11 14 (swung 0.62), a shaker on the off-16ths.
  THE CHOPS one-syllable voice fragments (a vowel and a soft consonant each) on the off-beats after the claps, pitched to
            the chord's 9th, 5th and 3rd in a falling three-note cell, the third chop held.
  NIGHT LOOP F#m9 | Dmaj9 | Bm11 | C#7sus, one chord a bar, voiced close on a juno pad through tape.
Run: python3 compose/chirpers3/src/chirpers3-t8.py  (writes songs/chirpers3-t8.yaml)
"""
import json
import os
import random

ROOT = os.path.expanduser("~/.config/chirp")
OUT = os.environ.get("T8_OUT") or os.path.join(ROOT, "songs", "chirpers3-t8.yaml")
BPM = 136
MG = float(os.environ.get("T8_MG", "10"))
V2 = os.environ.get("T8_V2", "1") == "1"
BUS = os.environ.get("T8_BUS", "1") == "1"
SH3 = os.environ.get("T8_SH3", "1") == "1"
H3 = os.environ.get("T8_H3", "0") == "1"
CH3 = os.environ.get("T8_CH3", "1") == "1"  # the last groove's chops as a dotted-eighth chain (every 3 sixteenths, across the bar lines), the voice carrying the cross-rhythm
RESAMPLE = os.environ.get("T8_RESAMPLE", "1") == "1"
LATE = os.environ.get("T8_LATE", "65")
VCHOP = os.environ.get("T8_VCHOP", "climax")
WEAR = os.environ.get("T8_WEAR", "0") == "1"
LIFT = int(os.environ.get("T8_LIFT", "2"))
BRAKE = os.environ.get("T8_BRAKE", "hard")
PUMP = os.environ.get("T8_PUMP", "-8")
SPACE = os.environ.get("T8_SPACE", "")
FOG = os.environ.get("T8_FOG", "1") == "1"  # the window fogs: the hall FREEZES through the breakdown's bars 2-7 (wM's reverb freeze), the pads and chops held as a wash  # the chops' echo as a tape loop (feedback routing): one dotted-eighth delay, its own output fed back through a low-pass and a tape deck  # wM's pump: the pads and the rhodes breathe on the kick (keyed from drums.k), depth in dB, e.g. -8  # the bus brakes at the last stop (wM's tapestop on the master, the last bar): "hard" = curve 4 over 2 beats; "soft" = curve 1.6 over 4  # the last groove lifted (semitones): the night loop up a step for the final run  # the tape wears (deck warp lanes): the beatless breakdown drifts seasick (1.6), the outro wears out (1 -> 2)  # wM's MPC chop on the voice: "stop" = through THE STOP; "climax" = through the last groove (the chain resampled)  # the claps (and optionally the hats) dragged late by hand: "45" or "45,25" (ms; play.humanize.nudge)  # master stutter bursts (3/16 slices) on the last half-bar before groove 2 and before the breakdown  # the HATS on the 3-sixteenth cycle instead (the loud voice carries the cross-rhythm; the shaker off)  # the shaker on a 3-sixteenth cycle (dotted eighths) running across the bar: the garage cross-rhythm  # groove 2 becomes THE STOP: half-time (kick 1, rim 3, no hats), rhodes chords for the pad, the B loop  # the v1 rework: a B loop for groove 2, a heavier shuffle with more off-16th hats, the sub up, the mud out
S = 0.25

NOTE = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8,
        "A": 9, "A#": 10, "Bb": 10, "B": 11}
NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


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


# chord: (root midi for the sub, pad voicing, chop tones (9th, 5th, 3rd) high)
LOOP = [("F#m9", 30, [57, 61, 64, 68], [68, 61, 57]), ("Dmaj9", 26, [57, 61, 64, 66], [64, 57, 54]),
        ("Bm11", 35, [54, 57, 61, 64], [61, 54, 50]), ("C#7sus", 37, [54, 59, 61, 66], [63, 56, 54])]

LOOP_B = [("Dmaj9", 26, [57, 61, 64, 66], [64, 57, 54]), ("E6/9", 28, [56, 59, 61, 66], [66, 59, 56]),
          ("C#m7", 37, [56, 59, 61, 64], [63, 56, 52]), ("Bm9", 35, [54, 57, 61, 62], [61, 54, 50])]

FORM = [("intro", 8), ("groove", 16), ("groove2", 16), ("breakdown", 8), ("groove3", 16), ("outro", 16)]
SKIPS = [10, 11, 7, 10, 11, 10, 7, 11]  # where the skip-kick lands, bar by bar


def drums(b, rng, sec):
    """SKIP: the 2-step bar."""
    ev = [(0, "k", 1, 110), (SKIPS[b % len(SKIPS)], "k", 1, 92), (4, "cp", 1, 100), (12, "cp", 1, 104)]
    for st in (() if H3 else (0, 2, 3, 5, 6, 9, 11, 13, 14) if V2 else (0, 2, 3, 6, 8, 10, 11, 14)):
        if st not in (0, 10, 11) or st == 0 or V2:
            ev.append((st, "h", 1, 72 if st % 4 == 0 else 58))
    if BUS and sec == "groove2":  # THE STOP: the bus idles - half-time, kick on 1, a rim on 3, a ghost before it
        ev = [(0, "k", 1, 104), (8, "rs", 1, 96), (7, "rs", 1, 46), (14, "k", 1, 70) if b % 2 else (15, "rs", 1, 40)]
        return grid(ev)
    for st in (1, 5, 9, 13):
        if rng.random() < 0.7 and not SH3 and not H3:
            ev.append((st, "sh", 1, 66 if BUS else 44))
    if H3:
        off = (3 - (b * 16) % 3) % 3
        ev += [(st, "h", 1, 80 if (b * 16 + st) % 6 == 0 else 60) for st in range(off, 16, 3)]
    if SH3 and not H3:
        off = (3 - (b * 16) % 3) % 3
        ev += [(st, "sh", 1, 74 if (b * 16 + st) % 6 == 0 else 58) for st in range(off, 16, 3)]
    if b % 8 == 7:
        ev += [(13, "rs", 1, 70), (14, "rs", 1, 76), (15, "rs", 1, 84)]
    # merge simultaneous hits into chords of pieces
    m = {}
    for st, p, ln, v in ev:
        if st in m:
            m[st] = (st, m[st][1] + "," + p, 1, max(m[st][3], v))
        else:
            m[st] = (st, p, ln, v)
    return grid(list(m.values()))


def chord(b, sec=""):
    c = (LOOP_B if V2 and sec == "groove2" else LOOP)[b % 4]
    if LIFT and sec == "groove3":
        name, r, v, tones = c
        return (name, r + LIFT, [n + LIFT for n in v], [n + LIFT for n in tones])
    return c


def sub(b, sec=""):
    _, r, _, _ = chord(b, sec)
    sk = SKIPS[b % len(SKIPS)]
    return grid([(0, nm(r), sk, 100), (sk, nm(r + 12 if sk == 7 else r), 16 - sk, 90)])


def pad(b, vel=58, sec=""):
    _, _, v, _ = chord(b, sec)
    return f"{','.join(nm(n) for n in v)}/4b@{vel}"


VOWELS = [(0.5, 19), (0.25, 16), (0.75, 22)]  # a (l-), o (m-), e (y-)


def chops(b, rng, up=0, dense=False, sec=""):
    """THE CHOPS: the falling three-note cell after the claps (steps 6, 7, 14 - or 5, 7, 14), the last held."""
    _, _, _, tones = chord(b, sec)
    starts = (6, 7, 14) if b % 2 == 0 else (5, 7, 14)
    ev = []
    for k, (st, n) in enumerate(zip(starts, tones)):
        if not dense and k == 1 and b % 4 == 3:
            continue
        vow, on = VOWELS[(b + k) % 3]
        ln = 1 if k < 2 else 2
        ev.append((st, f"{nm(n + up)}", ln, 74 - 4 * k, vow, on))
    out, pos = [], 0
    for st, head, ln, vel, vow, on in ev:
        out.append(R((st - pos) * S))
        out.append(f"{head}/{ln * S:g}b@{vel}^vow={vow}^on={on}")
        pos = st + ln
    out.append(R((16 - pos) * S))
    return J(*out)


def chop_chain(b, up=12, sec=""):
    """The chops in a dotted-eighth chain: one syllable every 3 sixteenths, cycling 9th-5th-3rd of the chord."""
    _, _, _, tones = chord(b, sec)
    off = (3 - (b * 16) % 3) % 3
    out, pos = [], 0
    for k, st in enumerate(range(off, 16, 3)):
        n = tones[((b * 16 + st) // 3) % 3]
        vow, on = VOWELS[((b * 16 + st) // 3) % 3]
        out.append(R((st - pos) * S))
        out.append(f"{nm(n + up)}/{S:g}b@{70 if k % 2 == 0 else 58}^vow={vow}^on={on}")
        pos = st + 1
    out.append(R((16 - pos) * S))
    return J(*out)


def build():
    names = ("drums", "sub", "pad", "glass", "chops", "rhodes")
    T = {n: [] for n in names}
    rng = random.Random(8)
    gb = 0
    for sec, nb in FORM:
        for b in range(nb):
            bar = {n: R(4) for n in names}
            if sec == "intro":
                bar["pad"] = pad(gb, 44 + 2 * b)
                if b >= 4:
                    bar["chops"] = chops(gb, rng)
                if b >= 6:
                    bar["drums"] = grid([(st, "h", 1, 50) for st in (2, 6, 10, 14)])
            elif sec in ("groove", "groove2", "groove3"):
                bar["drums"] = drums(gb, rng, sec)
                bar["sub"] = sub(gb, sec)
                bar["pad"] = pad(gb, sec=sec)
                if BUS and sec == "groove2":
                    bar["rhodes"] = J(pad(gb, 74, sec=sec).replace("/4b", "/1.5b"), R(0.5), pad(gb, 60, sec=sec).replace("/4b", "/1b"), R(1))
                    bar["pad"] = R(4)
                if sec != "groove" or b >= 8:
                    bar["chops"] = chops(gb, rng, up=12 if sec == "groove3" else 0, dense=(sec != "groove"), sec=sec)
                if sec == "groove3":
                    bar["glass"] = pad(gb, 50, sec=sec)
                    if CH3:
                        bar["chops"] = chop_chain(gb, sec=sec)
            elif sec == "breakdown":
                bar["pad"] = pad(gb, 62)
                bar["glass"] = pad(gb, 54)
                bar["chops"] = chops(gb, rng, dense=True)
            elif sec == "outro":
                if b < 8:
                    bar["drums"] = drums(gb, rng, sec) if b < 4 else grid([(st, "h", 1, 46) for st in (2, 6, 10, 14)])
                    bar["sub"] = sub(gb) if b < 6 else R(4)
                bar["pad"] = pad(gb, 58 - 2 * b)
                if b < 12:
                    bar["chops"] = chops(gb, rng)
            for n in names:
                T[n].append(bar[n])
            gb += 1
    return T


def vchop_track(track):
    """Resample the voice: the chop replays the previous bar of the chops in eight slices, a garage vocal flip."""
    if not VCHOP:
        return track
    st, total = section_starts()
    secs = {"stop": ["groove2"], "climax": ["groove3"], "both": ["groove2", "groove3"]}[VCHOP]
    lane = [["0s", 0]]
    for sec in secs:
        a = st[sec]
        b = a + dict(FORM)[sec] * 4 * 60 / BPM
        lane += [[f"{a - 0.02:.3f}s", 0], [f"{a:.3f}s", 1], [f"{b - 0.02:.3f}s", 1], [f"{b:.3f}s", 0]]
    lane.append([f"{total + 8:.2f}s", 0])
    track = dict(track)
    track["fx"] = list(track["fx"]) + [{"type": "chop", "slices": 8, "pattern": "0 0 . r3 _ 5 r6 .",
                                        "mix": {"value": 0, "mod": [{"src": "auto.vc", "amount": 1}]}}]
    track["auto"] = {"vc": {"points": lane}}
    return track


def section_starts():
    t, out = 0.0, {}
    for sec, nb in FORM:
        out[sec] = t
        t += nb * 4 * 60 / BPM
    return out, t


def song():
    T = build()
    sc = lambda n, pre="": (pre + " " if pre else "") + " | ".join(T[n])  # noqa: E731
    deck = "tape drive=0.12 mix=1 wow=12 flutter=2 drift=1 tone=6500 sweep=0.6 seed=8"
    wear_auto = {}
    if WEAR:
        st, total = section_starts()
        bd0, bd1 = st["breakdown"], st["groove3"]
        o0 = st["outro"]
        wr = [["0s", 1], [f"{bd0 - 0.3:.2f}s", 1], [f"{bd0 + 0.5:.2f}s", 1.6], [f"{bd1 - 0.5:.2f}s", 1.6], [f"{bd1:.2f}s", 1],
              [f"{o0:.2f}s", 1], [f"{total:.2f}s", 2], [f"{total + 8:.2f}s", 2]]
        deck = {"type": "tape", "drive": 0.12, "mix": 1, "wow": 12, "flutter": 2, "drift": 1, "tone": 6500, "sweep": 0.6, "seed": 8,
                "warp": {"value": 0, "mod": [{"src": "auto.wr", "amount": 1}]}}
        wear_auto = {"wr": {"points": wr}}
    chop = {"about": "Tape Weather t8: the chop voice - chirp's voice layer with a short tract (a higher, younger voice), "
                     "a fast attack and a short release, the vowel and onset consonant written per note.",
            "synth": {"layers": [{"type": "voice", "tract": 0.82, "breath": 0.4,
                                  "vowel": {"value": 0.5, "mod": [{"src": "expr.vow", "amount": 1}]}, "onset": "expr.on"}],
                      "amp": {"a": "6ms", "d": "0s", "s": 1, "r": "70ms"}},
            "play": {"mono": True}}
    tracks = [
        {"name": "drums", "patch": ("lofi-kit" if not LATE else "lofi-kit play.humanize.nudge.cp={}ms".format(LATE.split(",")[0])
                                     + (" play.humanize.nudge.h={}ms".format(LATE.split(",")[1]) if "," in LATE else "")), "gain": "-4dB", "score": sc("drums", "swing16=0.7" if V2 else "swing16=0.62")},
        {"name": "sub", "patch": "analog-bass", "gain": "2dB" if V2 else "-2dB", "fx": [{"type": "filter", "kind": "lowpass", "cutoff": 180}],
         "score": sc("sub")},
        {"name": "pad", "patch": "juno-pad", "gain": "-13dB", "fx": [deck], "sends": {"hall": "-10dB"}, "score": sc("pad")},
        {"name": "glass", "patch": "pad-glass", "gain": "-15dB", "pan": 0.3, "fx": [deck], "sends": {"hall": "-8dB"}, "score": sc("glass")},
        {"name": "rhodes", "patch": "rhodes", "gain": "-9dB", "pan": 0.2, "fx": [deck], "sends": {"hall": "-12dB", "echo": "-14dB"}, "score": sc("rhodes")},
        *([] if not VCHOP else []),
        {"name": "chops", "patch": "chop-vox", "gain": "-6dB", "pan": -0.15, "fx": [deck],
         "sends": {"hall": "-6dB", "echo": "-12dB"}, "score": sc("chops", "swing16=0.62")},
    ]
    if PUMP:
        for t in tracks:
            if t["name"] in ("pad", "glass", "rhodes"):
                t["fx"] = list(t["fx"]) + [{"type": "pump", "on": "drums.k", "depth": f"{PUMP}dB", "attack": "4ms", "release": "200ms", "curve": 2}]
    tracks = [vchop_track(t) if t["name"] == "chops" else t for t in tracks]
    if wear_auto:
        tracks = [({**t, "auto": {**t.get("auto", {}), **wear_auto}} if deck in t.get("fx", []) else t) for t in tracks]
    doc = {
        "about": ("Chirpers - Tape Weather, track 8 (original composition, chirper-zero; generator "
                  "compose/chirpers3/src/chirpers3-t8.py). Night-bus 2-step: lo-fi UK garage at 136 bpm - a shuffled, "
                  "skippy 2-step under a worn F#m9 | Dmaj9 | Bm11 | C#7sus loop and wordless chopped voices."),
        "tempo": BPM, "ceiling": "-0.3dB", "tail": "5s", "patches": {"chop-vox": chop},
        "buses": {"hall": ({"fx": ["reverb kind=hall decay=3.2s size=0.9 mix=1 predelay=24ms"]} if not FOG else
                           {"fx": [{"type": "reverb", "kind": "hall", "decay": "3.2s", "size": 0.9, "mix": 1, "predelay": "24ms",
                                    "freeze": {"value": 0, "mod": [{"src": "auto.fog", "amount": 1}]}}],
                            "auto": {"fog": {"points": fog_lane()}}}),
                  "echo": ({"fx": ["delay time=3/16 feedback=0.45 mix=1 tone=2200"]} if not SPACE else
                           {"fx": ["delay time=3/16 feedback=0 mix=1 tone=2800", {"type": "filter", "kind": "lowpass", "cutoff": 2200, "q": 0.8},
                                   "tape drive=0.2 mix=1 wow=12 flutter=3 drift=1 tone=5500 sweep=0.6 seed=8"],
                            "returns": [{"from": "echo", "gain": float(SPACE), "time": "6ms"}]})},
        "master": {"fx": [{"type": "eq", "bands": (["peak cutoff=280 q=0.8 gain=-5dB", "peak cutoff=640 q=0.8 gain=-3dB", "highshelf cutoff=6000 gain=4dB"] if V2
                                                   else ["peak cutoff=640 q=0.8 gain=-4dB", "highshelf cutoff=6000 gain=2dB"])},
                          "vinyl crackle=0.3 dust=0.25 noise=-62dB rumble=0.2 warp=3 wear=0.3 seed=8",
                          {"type": "compressor", "threshold": "-20dB", "ratio": 2, "attack": "15ms", "release": "200ms", "makeup": "0dB"},
                          {"type": "gain", "gain": f"+{MG + (2 if V2 else 0):g}dB"}] + resample_fx()},
        "tracks": tracks,
    }
    if RESAMPLE:
        doc["master"]["auto"] = resample_auto()
    if BRAKE:
        st, total = section_starts()
        t0 = total - 4 * 60 / BPM
        doc["master"]["fx"].append({"type": "tapestop", "time": "2b" if BRAKE == "hard" else "4b", "curve": 4 if BRAKE == "hard" else 1.6,
                                    "stop": {"value": 0, "mod": [{"src": "auto.brk", "amount": 1}]}})
        doc["master"].setdefault("auto", {})["brk"] = {"points": [["0s", 0], [f"{t0 - 0.02:.3f}s", 0], [f"{t0:.3f}s", 1], [f"{total + 8:.2f}s", 1]]}
    return doc


def fog_lane():
    st, total = section_starts()
    bar = 4 * 60 / BPM
    a, b = st["breakdown"] + 1.5 * bar, st["breakdown"] + 7.5 * bar
    return [["0s", 0], [f"{a - 0.02:.3f}s", 0], [f"{a:.3f}s", 1], [f"{b - 0.02:.3f}s", 1], [f"{b:.3f}s", 0], [f"{total + 8:.2f}s", 0]]


def resample_fx():
    if not RESAMPLE:
        return []
    st, total = section_starts()
    half = 2 * 60 / BPM
    gl = [["0s", 0]]
    for a in (st["groove2"] - half, st["breakdown"] - half):
        gl += [[f"{a - 0.02:.3f}s", 0], [f"{a:.3f}s", 1], [f"{a + half - 0.03:.3f}s", 1], [f"{a + half:.3f}s", 0]]
    gl.append([f"{total + 8:.2f}s", 0])
    return [{"type": "stutter", "slice": "3/16", "repeats": 3, "chance": 1, "decay": 0.15, "seed": 8,
             "mix": {"value": 0, "mod": [{"src": "auto.gl", "amount": 1}]}}]


def resample_auto():
    if not RESAMPLE:
        return {}
    st, total = section_starts()
    half = 2 * 60 / BPM
    gl = [["0s", 0]]
    for a in (st["groove2"] - half, st["breakdown"] - half):
        gl += [[f"{a - 0.02:.3f}s", 0], [f"{a:.3f}s", 1], [f"{a + half - 0.03:.3f}s", 1], [f"{a + half:.3f}s", 0]]
    gl.append([f"{total + 8:.2f}s", 0])
    return {"gl": {"points": gl}}


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
