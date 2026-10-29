#!/usr/bin/env python3
"""chirpers3-t9 (Tape Weather, track 9) - generator for songs/chirpers3-t9.yaml (chirper-zero).

CASSETTE BOSSA: a bossa nova played (not sampled) on a cassette left in a warm car. An original tune and changes in D,
120 bpm in a gentle two: a song-local NYLON GUITAR (the pluck string model, two planes, soft fingers) with its thumb on
1 and 3 and the chords on the bossa clave's off-beats; a mellotron flute sings the tune; surdo, ganza and a rim click
dragged late; everything through wM's tape deck pushed hard, on vinyl; once, the cassette catches.

Form: intro (the guitar alone) / A A (the flute) / B (the bridge, down a whole step, a rhodes joins) / A (the rhodes
takes the tune) / THE CATCH (two bars of stretched tape) / A A (the flute) / outro (the guitar over the ganza, fading).

Motifs (compose/chirpers3/motifs.md):
  AFTERNOON  the A tune: F#5. E5 F#5 A5 | B5~~ . | A5 G5 F#5 E5 D5 | C#5. B4 Bb4~ | A4 C#5 E5. D5 | D#5~ G5~ | F#5 E5 D5 B4~ | E5~~~
  CHANGES    Dmaj9 D6/9 Em9 A13b9 | F#m7 B7b13 Em9 A7sus; bridge Cmaj9 Am9 Dm9 G13 | Em7 A7b13 Em9 A7sus.
  THE THUMB  root on 1, fifth on 3, an anticipation of the next root on the last 16th of every other bar; the chords on
             0 3 6 10 13 | 2 6 9 12 14 (16ths), short and plucked.
Run: python3 compose/chirpers3/src/chirpers3-t9.py  (writes songs/chirpers3-t9.yaml)
"""
import json
import os
import random

ROOT = os.path.expanduser("~/.config/chirp")
OUT = os.environ.get("T9_OUT") or os.path.join(ROOT, "songs", "chirpers3-t9.yaml")
BPM = 120
MG = float(os.environ.get("T9_MG", "11"))
V2 = os.environ.get("T9_V2", "1") == "1"
V3 = os.environ.get("T9_V3", "1") == "1"
CHOP = os.environ.get("T9_CHOP", "catch")  # wM's MPC chop: "catch" = the cassette chews the bar before THE CATCH (master); "both" = and the guitar chopped in the outro's last four bars  # the form made audible: a master dynamics lane by section and a STOP at every seam (the band stops mid-bar, the rim fills)  # the draft's fixes: an upright bass (borrowed from Odd Hours t1), the master off the flute's presence and onto the lows, the bridge without the percussion
S = 0.25

NOTE = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8,
        "A": 9, "A#": 10, "Bb": 10, "B": 11}
NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "Bb", "B"]


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


CH = {  # name: (thumb root midi, guitar voicing)
    "Dmaj9": (50, [54, 57, 61, 64]), "D6/9": (50, [57, 59, 64, 66]), "Em9": (40, [55, 59, 62, 66]),
    "A13b9": (45, [55, 58, 61, 66]), "F#m7": (42, [54, 57, 61, 64]), "B7b13": (47, [57, 63, 67]),
    "A7sus": (45, [55, 59, 62, 64]), "Cmaj9": (48, [52, 55, 59, 62]), "Am9": (45, [55, 59, 60, 64]),
    "Dm9": (50, [53, 57, 60, 64]), "G13": (43, [53, 59, 64]), "Em7": (40, [55, 59, 62]), "A7b13": (45, [55, 61, 65]),
}
A_CH = ["Dmaj9", "D6/9", "Em9", "A13b9", "F#m7", "B7b13", "Em9", "A7sus"]
B_CH = ["Cmaj9", "Am9", "Dm9", "G13", "Em7", "A7b13", "Em9", "A7sus"]
A_TUNE = [
    [("F#5", 1.5), ("E5", .5), ("F#5", 1), ("A5", 1)], [("B5", 3), ("R", 1)],
    [("A5", .5), ("G5", .5), ("F#5", 1), ("E5", 1), ("D5", 1)], [("C#5", 1.5), ("B4", .5), ("Bb4", 2)],
    [("A4", 1), ("C#5", 1), ("E5", 1.5), ("D5", .5)], [("D#5", 2), ("G5", 2)],
    [("F#5", 1), ("E5", .5), ("D5", .5), ("B4", 2)], [("E5", 4)],
]
A_END = [("D5", 4)]  # the second A's last bar comes home
B_TUNE = [
    [("E5", 1.5), ("D5", .5), ("E5", 1), ("G5", 1)], [("B5", 3), ("R", 1)],
    [("A5", .5), ("F5", .5), ("E5", 1), ("D5", 2)], [("E5", 2), ("D5", 1), ("B4", 1)],
    [("G5", 1.5), ("F#5", .5), ("E5", 2)], [("F5", 2), ("E5", 1), ("C#5", 1)],
    [("D5", 1), ("E5", 1), ("F#5", 1), ("G5", 1)], [("A5", 4)],
]

FORM = [("intro", 4), ("A", 16), ("B", 8), ("Ar", 8), ("catch", 2), ("A2", 16), ("outro", 8)]


def chords_for(sec, b):
    return (B_CH if sec == "B" else A_CH)[b % 8]


def guitar(c, b, vel=70):
    root, v = CH[c]
    ch = ",".join(nm(n) for n in v)
    hits = (0, 3, 6, 10, 13) if b % 2 == 0 else (2, 6, 9, 12, 14)
    ev = [(st, ch, 2, vel - (6 if st % 4 else 0)) for st in hits if st not in (0, 8)]
    return grid(ev)


def thumb(c, b, nxt):
    root, _ = CH[c]
    ev = [(0, nm(root), 6, 86), (8, nm(root + 7 if root + 7 <= 57 else root - 5), 6, 78)]
    if b % 2 == 1:
        ev.append((14, nm(CH[nxt][0]), 2, 70))
    return grid(ev)


def perc(b, rng):
    ev = []
    for st in range(16):
        p = []
        if st in (0, 8):
            p.append("sm")
        if st in (6, 14):
            p.append("sd")
        p.append("gz")
        ev.append((st, ",".join(p), 1, (88 if "sm" in p else 74 if "sd" in p else (56 if st % 4 == 2 else 40)) + rng.randint(-4, 4)))
    return grid(ev)


def rim(b):
    return grid([(st, "so", 1, 66) for st in ((0, 6, 12) if b % 2 == 0 else (4, 10))])


def tune(notes, vel=82, shift=0):
    return J(*[R(d) if n == "R" else f"{nm(12 * (int(n[-1]) + 1) + NOTE[n[:-1]] + shift)}/{d:g}b@{vel}" for n, d in notes])


def build():
    names = ("guitar", "thumb", "perc", "rim", "flute", "rhodes", "rpad", "bass")
    T = {n: [] for n in names}
    rng = random.Random(9)
    times, t = {}, 0.0
    for si, (sec, nb) in enumerate(FORM):
        times[sec] = t
        for b in range(nb):
            c = chords_for(sec, b)
            nxt = chords_for(sec, b + 1) if b + 1 < nb else (chords_for(FORM[si + 1][0], 0) if si + 1 < len(FORM) else c)
            bar = {n: R(4) for n in names}
            bar["guitar"] = guitar(c, b, vel=64 if sec in ("intro", "outro") else 70)
            bar["thumb"] = thumb(c, b, nxt)
            if V2 and sec not in ("intro",):
                root = CH[c][0]
                low = root - 12 if root - 12 >= 28 else root
                ev = [(0, nm(low), 6, 92), (8, nm(low + 7), 5, 84)]
                if b % 2 == 1:
                    ev.append((14, nm(CH[nxt][0] - 12 if CH[nxt][0] - 12 >= 28 else CH[nxt][0]), 2, 76))
                bar["bass"] = grid(ev) if sec != "catch" else R(4)
            if sec not in ("intro", "catch") and not (V2 and sec == "B"):
                bar["perc"] = perc(b, rng)
                if sec != "outro":
                    bar["rim"] = rim(b)
            if sec in ("A", "A2"):
                bar["flute"] = tune(A_END if b % 16 == 15 else A_TUNE[b % 8], vel=84 if sec == "A" else 88)
            elif sec == "B":
                bar["flute"] = tune(B_TUNE[b], vel=86)
                bar["rpad"] = f"{','.join(nm(n + 12) for n in CH[c][1])}/4b@50"
            elif sec == "Ar":
                bar["rhodes"] = tune(A_TUNE[b % 8], vel=78, shift=-12)
                bar["rpad"] = f"{','.join(nm(n + 12) for n in CH[c][1])}/4b@44"
            elif sec == "outro":
                bar["guitar"] = guitar(c, b, vel=62 - 3 * b)
                bar["thumb"] = thumb(c, b, nxt) if b < 6 else R(4)
            if V3 and b == nb - 1 and sec not in ("outro", "catch"):  # the stop: everyone out at the bar's middle, the rim fills
                for n in ("guitar", "thumb", "flute", "rhodes", "rpad", "bass", "perc"):
                    toks, pos, out = bar[n].split(), 0.0, []
                    for tk in toks:
                        head, rest = tk.split("/", 1)
                        d = float(rest.split("b", 1)[0])
                        if pos >= 2:
                            break
                        tail = rest[len(rest.split("b", 1)[0]) + 1:]
                        out.append(f"{head}/{min(d, 2 - pos):g}b{tail}")
                        pos += d
                    if pos < 2:
                        out.append(R(2 - pos))
                    out.append(R(2))
                    bar[n] = J(*out)
                bar["rim"] = grid([(st, "so", 1, 60 + 4 * k) for k, st in enumerate((8, 10, 11, 12, 14, 15))])
            for n in names:
                T[n].append(bar[n])
            t += 4 * 60 / BPM
    return T, times, t


NYLON = {
    "about": "Tape Weather t9: a nylon-string guitar on the pluck string model - soft fingers (pick .6), no buzz, a "
             "low stiffness, two planes beating (wM's string), a dark top and a warm body.",
    "synth": {"layers": [{"name": "string", "type": "pluck", "stiff": 0.05, "buzz": 0, "pick": 0.6, "planes": 0.3, "beat": 1.5,
                          "decay": {"value": "2.4s", "mod": [{"src": "vel", "amount": 0.3}]},
                          "bright": {"value": 0.32, "mod": [{"src": "vel", "amount": 0.2}, {"src": "rand", "amount": 0.04}]}}],
              "amp": {"a": "2ms", "s": 1, "r": "160ms"}},
    "play": {"humanize": {"time": "6ms", "vel": 0.08}, "vel_sens": 0.5},
    "fx": [{"type": "eq", "bands": ["peak cutoff=210 q=0.9 gain=3dB", "highshelf cutoff=4000 gain=-6dB"]}],
    "gain": "-8dB",
}


def dyn_lane(times, total):
    lv = {"intro": -6, "A": 0, "B": -4, "Ar": -2, "catch": -8, "A2": 1, "outro": -6}
    pts = [["0s", lv["intro"]]]
    for sec, _ in FORM[1:]:
        a = times[sec]
        pts += [[f"{a - 0.3:.2f}s", pts[-1][1]], [f"{a:.2f}s", lv[sec]]]
    pts.append([f"{total + 8:.2f}s", lv["outro"]])
    return pts


def song():
    T, times, total = build()
    sc = lambda n: " | ".join(T[n])  # noqa: E731
    deck = "tape drive=0.15 mix=1 wow=18 flutter=3 drift=1.5 tone=6000 sweep=0.7 seed=9"
    bar = 4 * 60 / BPM
    c0 = times["catch"]
    catch = [["0s", 0], [f"{c0:.3f}s", 0], [f"{c0 + bar * 0.6:.3f}s", -1.5], [f"{c0 + bar * 1.4:.3f}s", -0.7], [f"{c0 + 2 * bar:.3f}s", 0], [f"{total + 8:.2f}s", 0]]
    cm = [["0s", 0], [f"{c0 - 0.02:.3f}s", 0], [f"{c0:.3f}s", 1], [f"{c0 + 2 * bar - 0.02:.3f}s", 1], [f"{c0 + 2 * bar:.3f}s", 0], [f"{total + 8:.2f}s", 0]]
    upright = json.loads(open(os.path.join(ROOT, "songs", "chirpers2-t1.yaml")).read().split("patches: ", 1)[1].split("\n", 1)[0])["upright"] if V2 else None
    o0 = times["outro"] + 4 * bar
    gcp = [["0s", 0], [f"{o0 - 0.02:.3f}s", 0], [f"{o0:.3f}s", 1], [f"{total + 8:.2f}s", 1]]
    gchop = ([{"type": "chop", "slices": 8, "pattern": "0 . 2 . r4 . 6 _", "mix": {"value": 0, "mod": [{"src": "auto.gcp", "amount": 1}]}}]
             if CHOP == "both" else [])
    tracks = [
        {"name": "guitar", "patch": "nylon", "pan": -0.15, "fx": [deck] + gchop, **({"auto": {"gcp": {"points": gcp}}} if gchop else {}), "sends": {"room": "-12dB"}, "score": sc("guitar")},
        {"name": "thumb", "patch": "nylon", "gain": "2dB", "pan": -0.1, "fx": [deck], "score": sc("thumb")},
        {"name": "perc", "patch": "samba-kit", "gain": "-10dB", "pan": 0.2, "score": "swing16=0.56 " + sc("perc")},
        {"name": "rim", "patch": "room-kit play.humanize.nudge.so=45ms", "gain": "-12dB", "pan": 0.3, "score": sc("rim")},
        {"name": "flute", "patch": "mellotron-flute", "gain": "-6dB", "pan": 0.1, "fx": [deck], "sends": {"room": "-8dB"}, "score": sc("flute")},
        {"name": "rhodes", "patch": "rhodes", "gain": "-7dB", "pan": 0.2, "fx": [deck], "sends": {"room": "-10dB"}, "score": sc("rhodes")},
        {"name": "rpad", "patch": "rhodes", "gain": "-14dB", "pan": -0.25, "fx": [deck], "sends": {"room": "-8dB"}, "score": sc("rpad")},
    ]
    if V2:
        tracks.append({"name": "bass", "patch": "upright", "gain": "4dB", "score": sc("bass")})
    return {
        "about": ("Chirpers - Tape Weather, track 9 (original composition, chirper-zero; generator "
                  "compose/chirpers3/src/chirpers3-t9.py). Cassette bossa: an original bossa nova in D at 120 bpm, played on "
                  "a song-local nylon guitar, mellotron flute, rhodes, surdo and ganza, through a tape deck pushed hard "
                  "and on vinyl; once, the cassette catches."),
        "tempo": BPM, "ceiling": "-0.3dB", "tail": "4s", "feel": {"drift": "5ms", "drift_bars": 4},
        "patches": {"nylon": NYLON, **({"upright": upright} if V2 else {})},
        "buses": {"room": {"fx": ["reverb kind=room decay=1.4s size=0.6 mix=1 predelay=12ms"]}},
        "master": {"fx": [{"type": "eq", "bands": (["lowshelf cutoff=150 gain=6dB", "peak cutoff=1100 q=0.6 gain=-8dB", "highshelf cutoff=6000 gain=2dB"] if V2
                                                   else ["peak cutoff=300 q=0.8 gain=-3dB", "highshelf cutoff=6000 gain=2dB"])},
                          {"type": "pitch", "semitones": {"value": 0, "mod": [{"src": "auto.cat", "amount": 1}]},
                           "mix": {"value": 0, "mod": [{"src": "auto.cm", "amount": 1}]}},
                          "vinyl crackle=0.35 dust=0.3 noise=-62dB rumble=0.25 warp=5 wear=0.4 seed=9",
                          {"type": "compressor", "threshold": "-20dB", "ratio": 2, "attack": "15ms", "release": "200ms", "makeup": "0dB"},
                          {"type": "gain", "gain": f"+{MG:g}dB"}] + ([{"type": "chop", "slices": 8, "pattern": "0 r1 2 2 _ 5 r6 7",
                                                                       "mix": {"value": 0, "mod": [{"src": "auto.cp", "amount": 1}]}}] if CHOP else []) + ([{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}}] if V3 else []),
                   "auto": {"cat": {"points": catch}, "cm": {"points": cm}, **({"cp": {"points": cm}} if CHOP else {}), **({"dyn": {"points": dyn_lane(times, total)}} if V3 else {})}},
        "tracks": tracks,
    }


def dump(doc):
    lines = [f"{k}: {json.dumps(doc[k])}" for k in ("about", "tempo", "ceiling", "tail", "feel", "patches", "master")]
    lines.append("buses:")
    lines += [f"  {b}: {json.dumps(v)}" for b, v in doc["buses"].items()]
    lines.append("tracks:")
    lines += ["  - " + json.dumps(t) for t in doc["tracks"]]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    open(OUT, "w").write(dump(song()))
    print("wrote", OUT)
