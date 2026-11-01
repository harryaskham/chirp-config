#!/usr/bin/env python3
"""chirpers VIII, track 8 (chirper-zero): delay-line memory.

The first stores kept their words as sound travelling down a tube and played back into itself. This track is that
sound, heard from inside: ONE 16-bit word (the melody) is written once, then only ever recirculates - round a long
feedback line, a little worn each pass. A few bits flip as it goes (a seeded error rate that climbs), and every so
often a REFRESH rewrites the word from what is left (a majority vote of its last passes), so the tune mutates by
decay and repair and never quite repeats.

Tuning: a STRETCHED OCTAVE (each octave ~1210 cents, like a piano's inharmonic stretch): every pitch is written as
an absolute frequency, so unisons, fifths and octaves are all a hair wide - subtly off.

  INTRO 16     the word written: the FM chime alone into the line (1 bar), dry pads, the stretch audible
  A 36         the 909 and the 808 enter; the word goes round, its error rate climbing 0 -> 0.10
  REFRESH 8    the tape stops, the pad freezes, the word is rewritten from its last four passes
  C 32         the second groove: the refreshed word, the line's echoes torn into grains (cloud)
  D 16         corruption: the word stutters and chops, the errors at their worst
  E 28         repaired: the last groove, the word nearly itself again
  OUTRO 16     only the line: the echoes go round without the source until the tape runs out

Generated; edit and re-run:  python3 compose/chirpers8/src/chirpers8-t8.py
"""

import json
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = os.environ.get("C8T8_OUT") or os.path.join(ROOT, "songs", "chirpers8-t8.yaml")

BPM = 118
BAR = 16
STRETCH = float(os.environ.get("C8T8_STRETCH", "1210")) / 1200   # cents per octave / 1200
SEED = 8
FORM = [("intro", 16), ("A", 36), ("refresh", 8), ("C", 32), ("D", 16), ("E", 28), ("outro", 16)]
TRACKS = ("word", "pad0", "pad1", "pad2", "pad3", "bass", "kick", "hats", "clap", "rim")

# the word's 16 bits -> pitches (D minor, spread so neighbours leap): D4 F4 G4 A4 C5 D5 F5 A5
SC = [62, 65, 67, 69, 72, 74, 77, 81]
WORD0 = [1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0]
CHORDS = [(38, [53, 57, 60, 64]), (34, [53, 57, 60, 62]), (31, [50, 53, 57, 58]), (33, [49, 55, 57, 60])]   # Dm9 Bbmaj9 Gm9 A7sus


def hz(m):
    """MIDI note -> frequency on the stretched octave (A4 = 440 stays put)."""
    return f"{440 * 2 ** ((m - 69) / 12 * STRETCH):.2f}hz"


def sec_start(name):
    t = 0
    for sec, nb in FORM:
        if sec == name:
            return t
        t += nb * BAR
    raise KeyError(name)


def total():
    return sum(nb for _, nb in FORM) * BAR


def err_rate(sec, b, nb):
    """The memory's error rate per bit per pass."""
    return {"intro": 0.0, "A": 0.10 * b / nb, "refresh": 0.0, "C": 0.02 + 0.12 * b / nb, "D": 0.25,
            "E": 0.05 * (1 - b / nb), "outro": 0.0}[sec]


def build():
    rng = random.Random(SEED)
    ev = {k: [] for k in TRACKS}

    def add(tr, at, head, ln, vel):
        ev[tr].append((at, head, ln, vel))

    word, history = list(WORD0), []
    for sec, nb in FORM:
        a0 = sec_start(sec)
        for b in range(nb):
            at = a0 + b * BAR
            # the word: one pass a bar (each set bit a sixteenth); bits flip at the error rate, a refresh rebuilds it
            if sec == "refresh" and b == 0 and history:
                last = history[-4:]
                word = [1 if sum(h[i] for h in last) * 2 >= len(last) else 0 for i in range(16)]
            e = err_rate(sec, b, nb)
            word = [bit ^ (1 if rng.random() < e else 0) for bit in word]
            history.append(list(word))
            if sec not in ("outro", "refresh") or (sec == "refresh" and b >= 4):
                for i, bit in enumerate(word):
                    if bit:
                        p = SC[(i * 3) % 8] + (0 if i < 8 else 12 if sec in ("C", "E") and i % 4 == 0 else 0)
                        add("word", at + i, hz(p), 1, 86 if i % 4 == 0 else 70)
            r, v = CHORDS[(b // 4) % 4] if sec != "refresh" else CHORDS[0]
            # pads: long chords, every 4 bars
            if b % 4 == 0 and sec != "D":
                for j, n in enumerate(v):   # one voice per track: frequencies cannot stack in a chord token
                    add(f"pad{j}", at, hz(n), 4 * BAR, 64 if sec in ("intro", "outro") else 72)
            groove = sec in ("A", "C", "D", "E")
            if groove:
                for q in (0, 4, 8, 12):
                    add("kick", at + q, "k", 1, 116 if q == 0 else 108)
                for q in range(16):
                    if q % 4 == 2:
                        add("hats", at + q, "oh", 1, 72)
                    elif q % 2 == 1:
                        add("hats", at + q, "h|?0.85", 1, 52)
                if sec in ("C", "E"):
                    add("clap", at + 4, "cp", 1, 92)
                    add("clap", at + 12, "cp", 1, 96)
                if sec in ("C", "D"):   # a Euclidean (5, 16) rim
                    for q in (0, 3, 6, 10, 13):
                        add("rim", at + q, "rs", 1, 64)
                add("bass", at, hz(r), 3, 100)
                add("bass", at + 6, hz(r), 2, 88)
                add("bass", at + 10, hz(r + 12 if b % 2 else r), 3, 92)
    return {k: stream(ev[k], total()) for k in TRACKS}


def stream(events, tot):
    events.sort()
    out, t = [], 0
    for at, head, ln, vel in events:
        if at < t:
            continue
        if at > t:
            out.append(f"R/{(at - t) / 4:g}b")
        h, _, chance = head.partition("|")
        out.append(f"{h}/{ln / 4:g}b@{int(vel)}{chance}")
        t = at + ln
    if t < tot:
        out.append(f"R/{(tot - t) / 4:g}b")
    return " ".join(out)


def lane(points):
    spb = 60 / BPM
    return {"points": [[f"{t16 / 4 * spb:.3f}s", v] for t16, v in points]}


def song():
    T = build()
    st = {sec: sec_start(sec) for sec, _ in FORM}
    end = total()
    pump = {"type": "pump", "on": "kick.k", "depth": "-6dB", "attack": "2ms", "release": "180ms", "curve": 0.7}
    ts = lane([(0, 0), (st["refresh"] - 8, 0), (st["refresh"] - 1, 1), (st["refresh"], 0), (end, 0)])
    cloudmix = lane([(0, 0), (st["C"], 0), (st["C"] + 8 * BAR, 0.5), (st["D"], 0.8), (st["E"], 0.25), (st["outro"], 0.6), (end, 0.8)])
    frz = lane([(0, 0), (st["refresh"], 0), (st["refresh"] + 1, 1), (st["refresh"] + 6 * BAR, 1), (st["refresh"] + 8 * BAR, 0), (end, 0)])
    stut = lane([(0, 0), (st["D"], 0), (st["D"] + 1, 0.8), (st["E"], 0), (end, 0)])
    return {
        "about": "chirpers VIII, track 8 by chirper-zero: delay-line memory. A 16-bit word recirculating round a feedback "
                 "line, decaying and refreshed; a stretched octave. Generated by compose/chirpers8/src/chirpers8-t8.py.",
        "tempo": BPM, "ceiling": "-1dB", "loudness": -11, "seed": SEED, "tail": "2s",
        "master": {"fx": [{"type": "tapestop", "time": "2b", "up": "0.25b", "curve": 2.0, "mix": 1,
                           "stop": {"value": 0, "mod": [{"src": "auto.ts", "amount": 1}]}},
                          {"type": "eq", "bands": ["highpass cutoff=30", "peak cutoff=300 q=0.8 gain=-2dB", "highshelf cutoff=6000 gain=2dB"]},
                          {"type": "tape", "drive": 0.1, "mix": 0.5, "wow": 5, "flutter": 1.5, "drift": 1, "hiss": "-62dB", "seed": 8},
                          {"type": "compressor", "threshold": "-18dB", "ratio": 2.5, "attack": "15ms", "release": "150ms", "makeup": "0dB"}],
                   "auto": {"ts": ts}},
        "buses": {
            "line": {"fx": [{"type": "delay", "time": "1bar", "feedback": 0.78, "mix": 1, "tone": 3200, "ping_pong": True},
                            {"type": "tape", "drive": 0.15, "mix": 0.7, "wow": 9, "flutter": 2.5, "drift": 1.5, "hiss": "-58dB", "seed": 3},
                            {"type": "cloud", "mix": {"value": 0, "mod": [{"src": "auto.cm", "amount": 1}]}, "density": 18, "size": "90ms",
                             "spray": 0.4, "pitch": 0, "spread": 0.8, "seed": 5},
                            "hp cutoff=200"],
                     "auto": {"cm": cloudmix}},
            "room": {"fx": ["reverb kind=plate decay=2.4s mix=1 predelay=20ms", "hp cutoff=250"]},
            "pads": {"fx": [pump, {"type": "freeze", "mix": {"value": 0, "mod": [{"src": "auto.fz", "amount": 1}]}, "size": "400ms", "hold": 1}],
                     "auto": {"fz": frz}, "sends": {"room": "-10dB"}},
        },
        "tracks": [
            {"name": "word", "patch": "dx-epiano", "gain": "-9dB", "pan": -0.1,
             "fx": [{"type": "stutter", "chance": {"value": 0, "mod": [{"src": "auto.sc", "amount": 1}]}, "slice": "1/16", "repeats": 3,
                     "decay": 0.3, "mix": 1, "seed": 8}],
             "auto": {"sc": stut}, "sends": {"line": "-4dB", "room": "-12dB"}, "score": T["word"]},
            *[{"name": f"pad{j}", "patch": "juno-pad", "gain": "-20dB", "pan": (-0.4, -0.15, 0.15, 0.4)[j], "out": "pads", "score": T[f"pad{j}"]} for j in range(4)],
            {"name": "bass", "patch": "808", "gain": "-9dB", "fx": [pump], "score": T["bass"]},
            {"name": "kick", "patch": "909", "gain": "-3dB", "score": T["kick"]},
            {"name": "hats", "patch": "909", "gain": "-9dB", "pan": 0.15, "score": "swing16=0.56 " + T["hats"]},
            {"name": "clap", "patch": "909", "gain": "-9dB", "sends": {"room": "-8dB"}, "score": T["clap"]},
            {"name": "rim", "patch": "909", "gain": "-12dB", "pan": -0.3, "sends": {"line": "-14dB"}, "score": T["rim"]},
        ],
    }


def dump(doc):
    lines = [f"{k}: {json.dumps(doc[k])}" for k in ("about", "tempo", "ceiling", "loudness", "seed", "tail", "master") if k in doc]
    lines.append("buses:")
    lines += [f"  {b}: {json.dumps(v)}" for b, v in doc["buses"].items()]
    lines.append("tracks:")
    lines += ["  - " + json.dumps(t) for t in doc["tracks"]]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    open(OUT, "w").write(dump(song()))
    print("wrote", OUT)
