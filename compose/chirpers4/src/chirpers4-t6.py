#!/usr/bin/env python3
"""Chirpers - Phantom Downbeat (Chirpers IV), track 6: BEAT FREQUENCY (chirper-three).

MINIMAL / FUNCTIONAL TECHNO where the rhythm lives inside held notes: INTERFERENCE BEATING.

Two tones a few hertz apart beat: their sum swells and fades Δ times a second. Tuned so Δ is the tempo's own pulse,
a single held note THROBS IN TIME, a rhythm that nobody plays. Every bass "note" here is one long tone made of
harmonic pairs (k*f and k*f + Δ, k = 1..4), so all its harmonics beat together; its dips are timed onto the kick, so
the bass breathes against the kick by physics, not by a sidechain. Change Δ and the same held note throbs in
triplets (3 against the kick's 4), eighths, sixteenths.

And THE CHORD THAT PLAYS A RHYTHM: a held G minor chord whose four voices each beat at their own rate (G3 in half
notes, D4 in dotted quarters, F4 in quarters, A4 in triplets): a polyrhythm made of interference inside a sustain.

Few parts, each doing a lot (Harry, 30 Oct: closer to No Floor's drive and focus, patient entries, better LFOs, not
acid): the machine kit's rumble kick, a clap, hats, the throb bass and the beating chord.

FORM (144 bars, 130 bpm, ~4:26):
  intro  1-16   the chord alone (its own polyrhythm), the hats (5), the kick (9)
  groove 17-48  the throb bass in quarters, breathing against the kick; the clap (25), open hats (33)
  shift  49-64  the same held bass throbs in TRIPLETS: three against the kick's four, by interference
  drift  65-80  (since v4) THE DRIFT: the throb's rate is 17/16 of the tempo, so the pulse slides against the kick and
                comes round again every four bars (chirper-one's idea: the beating going off the grid)
  break  81-96  no kick: the throb steps up every four bars, quarters, triplets, eighths, sixteenths: an acceleration
                made of interference, under the chord
  drop   97-128 the kick back, the throb in quarters, then eighths for the peak
  outro  129-144 a slow half-note throb, then the chord alone
"""
import json
import math
import os
import random

OUT = os.environ.get("C4T6_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers4-t6.yaml")
BPM = 130
BEAT_HZ = BPM / 60.0
BAR = 4.0
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

SECTIONS = [("intro", 1, 16), ("groove", 17, 48), ("shift", 49, 64), ("drift", 65, 80), ("break", 81, 96),
            ("drop", 97, 128), ("outro", 129, 144)]
BARS = SECTIONS[-1][2]
TOTAL = BARS * BAR


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def b0(bar):
    return (bar - 1) * BAR


def sec_of(bar):
    for name, a, z in SECTIONS:
        if a <= bar <= z:
            return name
    return "outro"


class Part:
    def __init__(self):
        self.ev = []

    def add(self, at, ln, head, vel):
        self.ev.append((at, ln, head, int(max(1, min(127, vel)))))

    def score(self, total=TOTAL):
        ev = sorted(self.ev, key=lambda e: (e[0], -e[3]))
        toks, pos = [], 0.0
        for i, (s, ln, head, vel) in enumerate(ev):
            nxt = ev[i + 1][0] if i + 1 < len(ev) else total
            ln = min(ln, nxt - s)
            if ln <= 1e-6:
                continue
            if s - pos > 1e-5:
                toks.append(f"R/{s - pos:.5g}b")
            toks.append(f"{head}/{ln:.5g}b@{vel}")
            pos = s + ln
        if total - pos > 1e-5:
            toks.append(f"R/{total - pos:.5g}b")
        return " ".join(toks)


# throb rates as multiples of the beat: half notes, dotted quarters, quarters, triplets, eighths, sixteenths
RATES = {"h": 0.5, "dq": 2 / 3, "q": 1.0, "t": 1.5, "e": 2.0, "s": 4.0, "d": 17 / 16}
# "d", THE DRIFT (v4, after chirper-one's note): a beat rate that is NOT the tempo's: the pulse slides off the off-beat,
# through the kick and back once every sixteen beats - the locked illusion unlocking, then snapping back
BASS = 31                                    # G1


def pair_patch(m, rate, harmonics=4, tilt=1.0, a="30ms", r="120ms", fund=1.0, cluster=2):
    """A tone whose harmonics each come as a CLUSTER of tones Δ Hz apart (Δ = rate x the beat), so the held note
    beats in time. Two per harmonic (a pair) swell and fade smoothly; three (since v3, the throb) make a sharper
    envelope - a narrow peak once a period with near silence either side and a small bump between - a PULSE."""
    d = rate * BEAT_HZ / hz(m)
    parts = []
    for k in range(1, harmonics + 1):
        amp = round((fund if k == 1 else 1.0) / k ** tilt / cluster * 2, 3)
        parts += [[round(k + j * d, 6), amp] for j in range(cluster)]
    return {"synth": {"layers": [{"type": "additive", "partials": parts}],
                      "amp": {"a": a, "d": "0s", "s": 1, "r": r}}}

P = {}


def part(name):
    return P.setdefault(name, Part())


def throb_plan():
    """(start bar, end bar, rate) for the throb bass."""
    plan = [(17, 49, "q"), (49, 65, "t"), (65, 81, "d"),
            (81, 85, "q"), (85, 89, "t"), (89, 93, "e"), (93, 97, "s"),
            (97, 113, "q"), (113, 129, "e"), (129, 137, "h")]
    return plan


def throb():
    """Each span is one long held G1; it starts a little early so the beating's dips land on the kicks (the trough
    of |cos(pi Δ t)| comes half a period after the note starts)."""
    for a, z, rate in throb_plan():
        early = 1 / (2 * RATES[rate])                         # in beats
        name = "throb_" + rate
        start = b0(a) - early
        end = b0(z) - early
        part(name).add(start, end - start, nm(BASS), 100)


CHORD = [(55, "h"), (62, "dq"), (65, "q"), (69, "t")]       # G3 D4 F4 A4: half, dotted quarter, quarter, triplet


def chord():
    """THE CHORD THAT PLAYS A RHYTHM: held, its four voices beating at four rates. Where it plays."""
    spans = [(1, 17, 84), (17, 49, 52), (49, 65, 52), (129, 145, 84)]   # it hands over to the bass
    for i, (m, rate) in enumerate(CHORD):
        for a, z, v in spans:
            part(f"ch{i}").add(b0(a), b0(z) - b0(a), nm(m), v)
        # THE WORLD ACCELERATES (v5): in the break the same chord beats at TWICE its rates, its polyrhythm
        # speeding up with the bass's steps (half notes -> quarters, dotted quarters -> three a bar, ...)
        part(f"cb{i}").add(b0(81), b0(97) - b0(81), nm(m), 70)


def drums():
    hand = random.Random(6)
    for bar in range(1, BARS + 1):
        sec = sec_of(bar)
        kick = bar >= 9 and sec != "break" and bar <= 140
        if kick:
            for b in range(4):
                part("kick").add(b0(bar) + b, 0.5, "k", 112 if b == 0 else 106)   # the punchy kick: the throb is the rumble
        if bar >= 25 and sec not in ("break", "intro") and bar <= 136:
            for b in (1, 3):
                part("clap").add(b0(bar) + b + 0.032, 0.5, "cp", 98 + hand.randint(-4, 4))   # dragged ~15 ms
        if bar >= 5 and (sec != "break" or bar >= 93) and bar <= 140:
            if sec == "intro":                                   # the intro: off-beats only
                for b in range(4):
                    part("hats").add(b0(bar) + b + 0.515, 0.2, "h", 56 + hand.randint(-6, 6))
            else:
                # THE 3-3-2: sixteenths with accents on 0 3 6 | 8 11 14 (dotted eighths against the four), the
                # rest ghosts, a hand on them (the e and a pushed late)
                for i in range(16):
                    acc = i in (0, 3, 6, 8, 11, 14)
                    v = (78 if acc else 40) + hand.randint(-6, 6) + (6 if sec in ("drift", "drop") else 0)
                    late = 0.03 if i % 2 else 0.0
                    part("hats").add(b0(bar) + i / 4 + late, 0.2, "h", v)
        if bar >= 41 and sec in ("groove", "shift", "drift", "drop"):       # THE RIM on the 3-3-2's off accents
            for i in (3, 6, 11, 14):
                part("rim").add(b0(bar) + i / 4 + 0.02, 0.2, "rs", 72 + hand.randint(-6, 6))
        if bar >= 33 and sec in ("groove", "shift", "drift", "drop"):
            for b in range(4):
                part("ohat").add(b0(bar) + b + 0.5, 0.4, "oh", 74 + hand.randint(-4, 4))


LEVEL = {"intro": -3, "groove": -1, "shift": -1, "drift": 0, "break": -9, "drop": 0, "outro": -6}


def dyn_lane():
    sec = lambda beats: beats * 60 / BPM
    pts = []
    for name, a, z in SECTIONS:
        t0 = sec(b0(a))
        if pts:
            pts.append([f"{max(0.0, t0 - 0.25):.3f}s", pts[-1][1]])
        pts.append([f"{t0:.3f}s", float(LEVEL[name])])
    return pts


def main():
    throb()
    chord()
    drums()
    beat_s = 60 / BPM
    patches = {f"c6-throb-{r}": pair_patch(BASS, RATES[r], harmonics=6, tilt=0.8, fund=0.5, cluster=3)  # a PULSE
               for r in ("h", "q", "t", "e", "s", "d")}                 # so the throb sounds above the kick's band
    for i, (m, rate) in enumerate(CHORD):
        patches[f"c6-chord-{i}"] = pair_patch(m, RATES[rate], harmonics=3, tilt=1.4, a="400ms", r="2.5s")
        patches[f"c6-chordx2-{i}"] = pair_patch(m, 2 * RATES[rate], harmonics=3, tilt=1.4, a="400ms", r="2.5s")
    pump = {"type": "pump", "on": "kick", "depth": "-6dB", "attack": "3ms", "release": "300ms", "curve": 0.6}
    tracks = [
        {"name": "kick", "patch": "machine-kit", "gain": "-1.5dB", "score": part("kick").score()},
        {"name": "rim", "patch": "machine-kit", "gain": "-10dB", "pan": 0.25, "sends": {"room": "-12dB"},
         "score": part("rim").score()},
        {"name": "clap", "patch": "machine-kit", "gain": "-5dB", "sends": {"room": "-9dB"}, "score": part("clap").score()},
        {"name": "hats", "patch": "machine-kit", "gain": "-5dB", "lfo": {"hp": {"wave": "sine", "rate": "20b"}},
         "fx": [{"type": "pan", "pan": {"value": 0.05, "mod": [{"src": "lfo.hp", "amount": 0.35}]}}],     # 5 bars
         "score": part("hats").score()},
        {"name": "ohat", "patch": "machine-kit", "gain": "-8dB", "pan": -0.1, "score": part("ohat").score()},
    ]
    for r in ("h", "q", "t", "e", "s", "d"):
        name = "throb_" + r
        if name in P:
            tracks.append({"name": name, "patch": f"c6-throb-{r}", "gain": "-5dB",
                           "lfo": {"bl": {"wave": "sine", "rate": "12b"}},                  # the buzz breathes (3 bars)
                           "fx": [{"type": "filter", "kind": "lp", "q": 1.2,
                                   "cutoff": {"value": 1800 if r == "d" else 900,      # the drift is brighter
                                              "mod": [{"src": "lfo.bl", "amount": 300}]}}],
                           # (no drive: saturation filled the troughs where the pairs cancel)
                           "score": part(name).score()})
    for i, (m, rate) in enumerate(CHORD):
        tracks.append({"name": f"ch{i}", "patch": f"c6-chord-{i}", "gain": "-9dB", "pan": [-0.3, 0.3, -0.15, 0.15][i],
                       "lfo": {"cf": {"wave": "sine", "rate": "28b"}},                         # 7 bars
                       "fx": [{"type": "filter", "kind": "lp",
                               "cutoff": {"value": 2200, "mod": [{"src": "lfo.cf", "amount": 1200}]}}],
                       "sends": {"room": "-8dB"}, "score": part(f"ch{i}").score()})
    for i, (m, rate) in enumerate(CHORD):
        tracks.append({"name": f"cb{i}", "patch": f"c6-chordx2-{i}", "gain": "-9dB", "pan": [-0.3, 0.3, -0.15, 0.15][i],
                       "lfo": {"cf": {"wave": "sine", "rate": "28b"}},                         # 7 bars
                       "fx": [{"type": "filter", "kind": "lp",
                               "cutoff": {"value": 2200, "mod": [{"src": "lfo.cf", "amount": 1200}]}}],
                       "sends": {"room": "-8dB"}, "score": part(f"cb{i}").score()})
    song = {
        "about": "Chirpers - Phantom Downbeat (Chirpers IV), track 6 by chirper-three: BEAT FREQUENCY. Minimal / "
                 "functional techno where the rhythm lives inside held notes (interference beating: harmonic pairs "
                 "a beat-rate apart). Generated by compose/chirpers4/src/chirpers4-t6.py; see compose/chirpers4/styles.md.",
        "tempo": BPM,
        "tail": "3s",
        "ceiling": "-0.3dB",
        "patches": patches,
        "buses": {"room": {"fx": ["reverb kind=hall decay=2.8s mix=1 predelay=20ms", "hp cutoff=250", "lp cutoff=7000"]}},
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=28", "peak cutoff=50 q=1.2 gain=-5dB",
                                                    "peak cutoff=320 q=0.8 gain=-2dB", "peak cutoff=2500 q=0.7 gain=2dB",
                                                    "highshelf cutoff=5000 gain=5dB"]},
                          {"type": "gain", "gain": "+18dB"},
                          {"type": "compressor", "threshold": "-11dB", "ratio": 3, "attack": "25ms", "release": "140ms",
                           "makeup": "2dB"},
                          {"type": "drive", "drive": 0.4, "mix": 0.35},
                          {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                          "limiter ceiling=-0.3dB"],
                   "auto": {"dyn": {"points": dyn_lane()}}},
        "tracks": tracks,
    }
    with open(OUT, "w") as f:
        json.dump(song, f, indent=1)
        f.write("\n")
    print(f"wrote {OUT}: {BARS} bars, {TOTAL * beat_s:.0f} s")


if __name__ == "__main__":
    main()
