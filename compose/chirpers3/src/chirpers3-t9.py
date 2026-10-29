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
CHOP = os.environ.get("T9_CHOP", "catch")
RIMLATE = os.environ.get("T9_RIMLATE", "45")  # the rim click's drag behind the beat (ms)
ANSWER = os.environ.get("T9_ANSWER", "1") == "1"
DENS = os.environ.get("T9_DENS", "1") == "1"
WEAR = os.environ.get("T9_WEAR", "1") == "1"
TSTOP = os.environ.get("T9_TSTOP", "both")
LIVEGTR = os.environ.get("T9_LIVEGTR", "0") in ("1", "pan")
LIVEKIND = os.environ.get("T9_LIVEGTR", "0")
HAZE = os.environ.get("T9_HAZE", "1") == "1"
PAND3 = os.environ.get("T9_PAND3", "0") == "1"
SURDRAG = os.environ.get("T9_SURDRAG", "")
GZSW = os.environ.get("T9_GZSW", "0.56")
GZ3 = os.environ.get("T9_GZ3", "64")  # the ganza accents a 16th-level 3+3+2 (0 3 6 | 8 11 14), the partido-alto lean: accent velocity, e.g. 64  # the ganza's 16th swing (and the pandeiro's, unless T9_PANDSW): 0.56 near-straight; ~0.6 leans into the samba swing
FHARM = os.environ.get("T9_FHARM", "1") == "1"
EPIANO = os.environ.get("T9_EPIANO", "tine")  # wM's physical pickup e-piano in place of the rhodes (the bridge pad and the instrumental A): "tine" / "reed"  # the last A's last eight bars: a second flute a diatonic third under the tune (D major / the chord's tones)  # the open surdo (the dotted pulse on 6 and 14) dragged late by hand (ms)  # the last A's pandeiro on a dotted-eighth cycle (every 3 sixteenths, across the bar lines) instead of every off-16th  # wM's cloud (granular) as heat haze: the bridge's flute and rhodes are sent into a shimmering grain cloud  # "1": pan + tone per pluck; "pan": a small place per pluck only  # per-voice fx on the nylon (pin 3eee6a72): every pluck its own small place and its own tone  # wM's tapestop on the master: "end" = the side runs out and the deck stops over the outro's last two bars; "both" = and the catch ends in a stop that spins back up into the last A  # the tape wears (chirper-two's deck warp, pin 220ef336): harder through the bridge (1.4), and the side running out over the outro (1 -> 2)  # density contrast: the bridge sparer (two plucks a bar, no rim), the last A busier (pandeiro jingles on the off-16ths)
IND_DB = os.environ.get("T9_INDDB", "-13")
INDICATOR = os.environ.get("T9_INDICATOR", "")  # the car's indicator ticking through the intro and the outro (tick-tock every 380 ms, out of time with the bossa); "" off, "io" intro+outro, "all" the whole way, quieter  # the last A: the guitar answers the flute at every phrase end (a falling fill on the 4th bar's last two beats)  # wM's MPC chop: "catch" = the cassette chews the bar before THE CATCH (master); "both" = and the guitar chopped in the outro's last four bars  # the form made audible: a master dynamics lane by section and a STOP at every seam (the band stops mid-bar, the rim fills)  # the draft's fixes: an upright bass (borrowed from Odd Hours t1), the master off the flute's presence and onto the lows, the bridge without the percussion
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


def guitar(c, b, vel=70, sparse=False):
    root, v = CH[c]
    ch = ",".join(nm(n) for n in v)
    hits = (0, 3, 6, 10, 13) if b % 2 == 0 else (2, 6, 9, 12, 14)
    if sparse:
        hits = (3, 10) if b % 2 == 0 else (6, 12)
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
        gzv = (int(GZ3) if st in (0, 3, 6, 8, 11, 14) else 38) if GZ3 else (56 if st % 4 == 2 else 40)
        ev.append((st, ",".join(p), 1, (88 if "sm" in p else 74 if "sd" in p else gzv) + rng.randint(-4, 4)))
    return grid(ev)


def rim(b):
    return grid([(st, "so", 1, 66) for st in ((0, 6, 12) if b % 2 == 0 else (4, 10))])


def tune(notes, vel=82, shift=0):
    return J(*[R(d) if n == "R" else f"{nm(12 * (int(n[-1]) + 1) + NOTE[n[:-1]] + shift)}/{d:g}b@{vel}" for n, d in notes])


def build():
    names = ("guitar", "thumb", "perc", "rim", "flute", "rhodes", "rpad", "bass") + (("gfill",) if ANSWER else ()) + (("pand",) if DENS else ()) + (("flute2",) if FHARM else ())
    T = {n: [] for n in names}
    rng = random.Random(9)
    times, t = {}, 0.0
    for si, (sec, nb) in enumerate(FORM):
        times[sec] = t
        for b in range(nb):
            c = chords_for(sec, b)
            nxt = chords_for(sec, b + 1) if b + 1 < nb else (chords_for(FORM[si + 1][0], 0) if si + 1 < len(FORM) else c)
            bar = {n: R(4) for n in names}
            bar["guitar"] = guitar(c, b, vel=64 if sec in ("intro", "outro") else 70, sparse=(DENS and sec == "B"))
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
                if sec != "outro" and not (DENS and sec == "B"):
                    bar["rim"] = rim(b)
                if DENS and sec == "A2":
                    bar["pand"] = grid([(st, "pd", 1, 52 if st % 4 == 3 else 40) for st in range(1, 16, 2)])
                    if PAND3:
                        off = (3 - (b * 16) % 3) % 3
                        bar["pand"] = grid([(st, "pd", 1, 60 if ((b * 16 + st) // 3) % 2 == 0 else 46) for st in range(off, 16, 3)])
            if sec in ("A", "A2"):
                bar["flute"] = tune(A_END if b % 16 == 15 else A_TUNE[b % 8], vel=84 if sec == "A" else 88)
                if FHARM and sec == "A2" and b >= 8:
                    notes = A_END if b % 16 == 15 else A_TUNE[b % 8]
                    scale = [2, 4, 6, 7, 9, 11, 1]  # D major pitch classes
                    def third_under(n):
                        m = 12 * (int(n[-1]) + 1) + NOTE[n[:-1]]
                        for k in (3, 4):
                            if (m - k) % 12 in scale:
                                return nm(m - k)
                        return nm(m - 3)
                    bar["flute2"] = J(*[R(d) if n == "R" else f"{third_under(n)}/{d:g}b@72" for n, d in notes])
                if ANSWER and sec == "A2" and b % 4 == 3:  # the guitar answers: a falling run down the chord's tones in the bar's last two beats
                    root, v = CH[c]
                    run = sorted(v, reverse=True) + [v[0] - 12 + 12]
                    fill = [(8 + 2 * k, nm(n + 12), 2, 74 - 3 * k) for k, n in enumerate(run[:4])]
                    bar["gfill"] = grid(fill)
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


LIVE_FX = [{"type": "pan", "pan": {"value": 0, "mod": [{"src": "rand", "amount": 0.3}]}},
           {"type": "filter", "kind": "lowpass", "cutoff": {"value": 3200, "mod": [{"src": "rand", "amount": 0.5}]}, "q": 0.9}]

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


def ts_lane(times, total, bar):
    """The stop lane: the outro's last two bars (8 beats) run the deck down; with "both", the catch's last beat too."""
    end0 = total - 2 * bar
    pts = [["0s", 0]]
    if TSTOP == "both":
        c1 = times["catch"] + 2 * bar - 60 / BPM  # the catch's last beat: a stop, released on the downbeat (it spins back up)
        pts += [[f"{c1 - 0.02:.3f}s", 0], [f"{c1:.3f}s", 1], [f"{c1 + 60 / BPM - 0.02:.3f}s", 1], [f"{c1 + 60 / BPM:.3f}s", 0]]
    pts += [[f"{end0 - 0.02:.3f}s", 0], [f"{end0:.3f}s", 1], [f"{total + 8:.2f}s", 1]]
    return pts


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
    wear_auto = {}
    if WEAR:
        b0, b1 = times["B"], times["B"] + 8 * 4 * 60 / BPM
        o0 = times["outro"]
        wr = [["0s", 1], [f"{b0 - 0.5:.2f}s", 1], [f"{b0 + 0.5:.2f}s", 1.4], [f"{b1 - 0.5:.2f}s", 1.4], [f"{b1 + 0.5:.2f}s", 1],
              [f"{o0:.2f}s", 1], [f"{total:.2f}s", 2], [f"{total + 8:.2f}s", 2]]
        deck = {"type": "tape", "drive": 0.15, "mix": 1, "wow": 18, "flutter": 3, "drift": 1.5, "tone": 6000, "sweep": 0.7, "seed": 9,
                "warp": {"value": 0, "mod": [{"src": "auto.wr", "amount": 1}]}}
        wear_auto = {"wr": {"points": wr}}
    bar = 4 * 60 / BPM
    c0 = times["catch"]
    catch = [["0s", 0], [f"{c0:.3f}s", 0], [f"{c0 + bar * 0.6:.3f}s", -1.5], [f"{c0 + bar * 1.4:.3f}s", -0.7], [f"{c0 + 2 * bar:.3f}s", 0], [f"{total + 8:.2f}s", 0]]
    cm = [["0s", 0], [f"{c0 - 0.02:.3f}s", 0], [f"{c0:.3f}s", 1], [f"{c0 + 2 * bar - 0.02:.3f}s", 1], [f"{c0 + 2 * bar:.3f}s", 0], [f"{total + 8:.2f}s", 0]]
    upright = json.loads(open(os.path.join(ROOT, "songs", "chirpers2-t1.yaml")).read().split("patches: ", 1)[1].split("\n", 1)[0])["upright"] if V2 else None
    o0 = times["outro"] + 4 * bar
    gcp = [["0s", 0], [f"{o0 - 0.02:.3f}s", 0], [f"{o0:.3f}s", 1], [f"{total + 8:.2f}s", 1]]
    gchop = ([{"type": "chop", "slices": 8, "pattern": "0 . 2 . r4 . 6 _", "mix": {"value": 0, "mod": [{"src": "auto.gcp", "amount": 1}]}}]
             if CHOP == "both" else [])
    ind = []
    if INDICATOR:
        spans = ([(0.0, times["A"] + 2), (times["outro"], total)] if INDICATOR == "io" else [(0.0, total)])
        pos = 0.0
        toks = []
        for a, b in spans:
            if a > pos:
                toks.append(f"R/{int(round((a - pos) * 1000))}ms")
                pos = a
            k = 0
            while pos + 0.38 <= b:
                toks.append(f"{'wb' if k % 2 == 0 else 'wbl'}/380ms@{58 if k % 2 == 0 else 50}")
                pos += 0.38
                k += 1
        ind = [{"name": "indicator", "patch": "room-kit", "gain": "-18dB" if INDICATOR == "all" else f"{IND_DB}dB", "pan": -0.6,
                "fx": [{"type": "eq", "bands": ["hp cutoff=900", "peak cutoff=2500 q=1 gain=3dB"]}, deck], "score": " ".join(toks)}]
    def wa(tr):
        if wear_auto and deck in tr.get("fx", []):
            tr = dict(tr)
            tr["auto"] = {**tr.get("auto", {}), **wear_auto}
        return tr
    tracks = ind + [
        {"name": "guitar", "patch": "nylon", "pan": -0.15, "fx": [deck] + gchop, **({"auto": {"gcp": {"points": gcp}}} if gchop else {}), "sends": {"room": "-12dB"}, "score": sc("guitar")},
        {"name": "thumb", "patch": "nylon", "gain": "2dB", "pan": -0.1, "fx": [deck], "score": sc("thumb")},
        {"name": "perc", "patch": "samba-kit" + (f" play.humanize.nudge.sd={SURDRAG}ms" if SURDRAG else ""), "gain": "-10dB", "pan": 0.2, "score": f"swing16={GZSW} " + sc("perc")},
        {"name": "rim", "patch": f"room-kit play.humanize.nudge.so={RIMLATE}ms", "gain": "-12dB", "pan": 0.3, "score": sc("rim")},
        {"name": "flute", "patch": "mellotron-flute", "gain": "-6dB", "pan": 0.1, "fx": [deck], "sends": {"room": "-8dB"}, "score": sc("flute")},
        {"name": "rhodes", "patch": f"epiano-{EPIANO}" if EPIANO else "rhodes", "gain": "-7dB", "pan": 0.2, "fx": [deck], "sends": {"room": "-10dB"}, "score": sc("rhodes")},
        {"name": "rpad", "patch": f"epiano-{EPIANO}" if EPIANO else "rhodes", "gain": "-14dB", "pan": -0.25, "fx": [deck], "sends": {"room": "-8dB"}, "score": sc("rpad")},
    ]
    if V2:
        tracks.append({"name": "bass", "patch": "upright", "gain": "4dB", "score": sc("bass")})
    tracks = [wa(t) for t in tracks]
    if HAZE:
        b0, b1 = times["B"], times["B"] + 8 * 4 * 60 / BPM
        hz = [["0s", 0], [f"{b0 - 0.5:.2f}s", 0], [f"{b0 + 1.0:.2f}s", 1], [f"{b1 - 1.0:.2f}s", 1], [f"{b1:.2f}s", 0], [f"{total + 8:.2f}s", 0]]
        for t in tracks:
            if t["name"] in ("flute", "rpad"):
                t["sends"] = {**t.get("sends", {}), "haze": {"value": "-60dB", "mod": [{"src": "auto.hz", "amount": float(os.environ.get("T9_HAZEDB", "56"))}]}}
                t["auto"] = {**t.get("auto", {}), "hz": {"points": hz}}
    if FHARM:
        tracks.append(wa({"name": "flute2", "patch": "mellotron-flute", "gain": "-10dB", "pan": -0.2, "fx": [deck], "sends": {"room": "-8dB"}, "score": sc("flute2")}))
    if DENS:
        tracks.append({"name": "pand", "patch": "samba-kit", "gain": "-12dB", "pan": 0.35, "score": f"swing16={os.environ.get('T9_PANDSW', GZSW)} " + sc("pand")})
    if ANSWER:
        tracks.append({"name": "gfill", "patch": "nylon", "gain": "-2dB", "pan": 0.25, "fx": [deck], "sends": {"room": "-10dB"}, "score": sc("gfill")})
    tracks = [wa(t) for t in tracks]
    return {
        "about": ("Chirpers - Tape Weather, track 9 (original composition, chirper-zero; generator "
                  "compose/chirpers3/src/chirpers3-t9.py). Cassette bossa: an original bossa nova in D at 120 bpm, played on "
                  "a song-local nylon guitar, mellotron flute, rhodes, surdo and ganza, through a tape deck pushed hard "
                  "and on vinyl; once, the cassette catches."),
        "tempo": BPM, "ceiling": "-0.3dB", "tail": "4s", "feel": {"drift": "5ms", "drift_bars": 4},
        "patches": {"nylon": ({**NYLON, "synth": {**NYLON["synth"], "fx": (LIVE_FX if LIVEKIND == "1" else
                                                                       [{"type": "pan", "pan": {"value": 0, "mod": [{"src": "rand", "amount": 0.25}]}}])}}
                              if LIVEGTR else NYLON), **({"upright": upright} if V2 else {})},
        "buses": {"room": {"fx": ["reverb kind=room decay=1.4s size=0.6 mix=1 predelay=12ms"]},
                  **({"haze": {"fx": [{"type": "cloud", "size": "150ms", "density": 18, "position": "500ms", "spray": "400ms",
                                         "spread": 0.8, "reverse": 0.25, "mix": 1},
                                        "reverb kind=hall decay=2.5s size=0.8 mix=0.5 predelay=20ms"]}} if HAZE else {})},
        "master": {"fx": [{"type": "eq", "bands": (["lowshelf cutoff=150 gain=6dB", "peak cutoff=1100 q=0.6 gain=-8dB", "highshelf cutoff=6000 gain=2dB"] if V2
                                                   else ["peak cutoff=300 q=0.8 gain=-3dB", "highshelf cutoff=6000 gain=2dB"])},
                          {"type": "pitch", "semitones": {"value": 0, "mod": [{"src": "auto.cat", "amount": 1}]},
                           "mix": {"value": 0, "mod": [{"src": "auto.cm", "amount": 1}]}},
                          "vinyl crackle=0.35 dust=0.3 noise=-62dB rumble=0.25 warp=5 wear=0.4 seed=9",
                          {"type": "compressor", "threshold": "-20dB", "ratio": 2, "attack": "15ms", "release": "200ms", "makeup": "0dB"},
                          {"type": "gain", "gain": f"+{MG:g}dB"}] + ([{"type": "tapestop", "time": "8b", "curve": 1.2, "up": "1b",
                                                                      "stop": {"value": 0, "mod": [{"src": "auto.ts", "amount": 1}]}}] if TSTOP else []) + ([{"type": "chop", "slices": 8, "pattern": "0 r1 2 2 _ 5 r6 7",
                                                                       "mix": {"value": 0, "mod": [{"src": "auto.cp", "amount": 1}]}}] if CHOP else []) + ([{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}}] if V3 else []),
                   "auto": {**({"ts": {"points": ts_lane(times, total, bar)}} if TSTOP else {}), "cat": {"points": catch}, "cm": {"points": cm}, **({"cp": {"points": cm}} if CHOP else {}), **({"dyn": {"points": dyn_lane(times, total)}} if V3 else {})}},
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
