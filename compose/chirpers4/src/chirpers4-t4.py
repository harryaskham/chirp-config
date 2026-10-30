#!/usr/bin/env python3
"""Chirpers - Phantom Downbeat (Chirpers IV), track 4: TWO FLOORS (chirper-three).

TRIBAL / PERCUSSIVE WAREHOUSE TECHNO with a METRIC MODULATION: the same bar holds two tempos.

The pivot is a 12-step grid (triplet eighths, a third of a beat): a shekere shuffle, congas, a rolling bass and an
agogo bell all live on it. Under a four-on-the-floor 909 kick (steps 0 3 6 9) those twelve steps are a tribal shuffle
at 128 bpm. Under a kick on every fourth step (0 4 8, three to the bar: the TRIBE'S floor, deep tuned toms) the same
twelve steps become straight sixteenths at 96 bpm. Nothing about the grid or the bar changes; only which floor the
ear stands on.

FORM (144 bars, 128 bpm, ~4:30):
  intro  1-16   the machine's floor: 909 kick + rumble; the shekere's shuffle enters
  groove 17-48  four on the floor: clap, open hats, congas, the rolling bass; the stab already hints at three
  both   49-64  TWO FLOORS: the toms' three-floor joins the 909's four (4 against 3): the ear can stand on either
  slow   65-80  the 909 leaves: the toms carry it, the hats and clap move to the three-floor: the floor slows to 96
  break  81-96  no kicks: the shekere's accents flip between 4 and 3 every two bars (the ear cannot tell which floor);
                a drone, the bell, a Shepard riser
  drop   97-128 the four-floor slams back (with a distorted 909 layer) and the toms stay: both floors at full weight
  outro  129-144 the machine's floor and the shuffle, thinning out
"""
import json
import os
import random

OUT = os.environ.get("C4T4_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers4-t4.yaml")
BPM = 128
BAR = 4.0                                   # beats per bar
STEP = 1 / 3                                # the pivot grid: twelve steps a bar
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

SECTIONS = [("intro", 1, 16), ("groove", 17, 48), ("both", 49, 64), ("slow", 65, 80), ("break", 81, 96),
            ("drop", 97, 128), ("outro", 129, 144)]
BARS = SECTIONS[-1][2]
TOTAL = BARS * BAR


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def b0(bar):
    return (bar - 1) * BAR


def st(bar, step):
    return b0(bar) + step * STEP


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
        merged = []
        for e in ev:
            if merged and abs(merged[-1][0] - e[0]) < 1e-6:
                continue
            merged.append(e)
        toks, pos = [], 0.0
        for i, (s, ln, head, vel) in enumerate(merged):
            nxt = merged[i + 1][0] if i + 1 < len(merged) else total
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


P = {k: Part() for k in ("four", "kh", "toms", "boom", "clap", "hats", "shek", "conga", "bell", "bass", "sub", "stab", "pad",
                         "riser")}

G = 7                                       # G minor
FOUR_ON = {"intro", "groove", "both", "drop", "outro"}
THREE_ON = {"both", "slow", "drop"}


def floors():
    """THE TWO FLOORS. The machine's: a 909 kick on every beat (steps 0 3 6 9). The tribe's: deep tuned toms on every
    fourth step (0 4 8), three to the bar, which alone make the bar feel like 96 bpm."""
    hand = random.Random(4)
    tom_pitch = [G + 26, G + 26, G + 21]                # D2 D2 A1 ... the tribe's floor sings a falling fourth
    for bar in range(1, BARS + 1):
        sec = sec_of(bar)
        if sec in FOUR_ON and not (sec == "outro" and bar > 142):
            for s in (0, 3, 6, 9):
                P["four"].add(st(bar, s), 0.5, "k", 116 if s == 0 else 110)
            if sec == "drop" and bar < 105:
                for s in (0, 3, 6, 9):
                    P["kh"].add(st(bar, s), 0.5, "kh", 96)          # the drop's distorted layer
        if sec in THREE_ON:
            for i, s in enumerate((0, 4, 8)):
                v = (104 if i == 0 else 94) + hand.randint(-4, 4)
                if sec == "both" and bar < 53:
                    v -= 24 - 6 * (bar - 49)                         # the tribe arrives over four bars
                P["toms"].add(st(bar, s), 1.2, nm(tom_pitch[i]), v)
                P["boom"].add(st(bar, s), 0.6, nm(tom_pitch[i]), v + 6)     # THE TRIBE'S CHEST-HIT: an 808 under each tom
            if bar % 4 == 0:                                         # a fill into the next phrase, falling
                for j, s in enumerate((9, 10, 11)):
                    P["toms"].add(st(bar, s) + 0.02, 0.3, nm(G + 33 - 4 * j), 80 + 6 * j)


def backbeat():
    """Clap and hats follow the floor the ear stands on: the four's clap on 2 and 4 and open hats on the straight
    off-beats; the three's clap on its third beat (step 8), a rim on its second, hats on its off-beats (2 6 10)."""
    hand = random.Random(9)
    for bar in range(1, BARS + 1):
        sec = sec_of(bar)
        four = sec in ("groove", "both", "drop") or (sec == "outro" and bar < 137)
        three = sec == "slow"
        if four:
            for b in (1, 3):
                P["clap"].add(b0(bar) + b + 0.012, 0.5, "cp", 100 + hand.randint(-5, 3))
        if (four or (sec == "intro" and bar > 8)):
            for b in range(4):
                P["hats"].add(b0(bar) + b + 0.5, 0.25, "oh", 84 if sec != "intro" else 66)
        if three:
            P["clap"].add(st(bar, 8) + 0.012, 0.5, "cp", 104 + hand.randint(-5, 3))
            P["clap"].add(st(bar, 4), 0.25, "rs", 70 + hand.randint(-6, 6))
            for s in (2, 6, 10):
                P["hats"].add(st(bar, s), 0.25, "oh", 86)


def shuffle():
    """THE PIVOT: the shekere on all twelve steps. Its accents say which floor: on 0 3 6 9 under the four, on 0 4 8
    under the three; in the break they flip every two bars, so the ear cannot settle (a Necker cube for tempo)."""
    hand = random.Random(12)
    for bar in range(5, BARS + 1):
        sec = sec_of(bar)
        if 81 <= bar <= 84:
            continue                                        # the break opens on the drone alone: both floors gone
        if sec == "slow":
            acc = (0, 4, 8)
        elif sec == "break":
            acc = (0, 3, 6, 9) if ((bar - 81) // 2) % 2 == 0 else (0, 4, 8)
        else:
            acc = (0, 3, 6, 9)
        for s in range(12):
            v = (92 if s in acc else 48 + (8 if s % 2 else 0)) + hand.randint(-6, 6)
            if sec == "break" and (s not in acc or bar == 96):
                continue                            # the break: only the accents, flipping; bar 96 is a blackout
            if sec == "intro":
                v -= 16
            P["shek"].add(st(bar, s), 0.3, "sk", v)


CONGA = {0: "lo", 2: "mu", 4: "sl", 5: "o", 7: "mu", 8: "sl", 10: "o", 11: "mu"}


def congas():
    """A tribal conga line on the pivot grid; its slaps (4 and 8) lean towards the three-floor before it exists, and
    every fourth bar one hit moves (the loop mutates)."""
    hand = random.Random(21)
    pat = dict(CONGA)
    for bar in range(17, 129):
        sec = sec_of(bar)
        if sec == "break" and (bar < 89 or bar == 96):
            continue
        if bar % 4 == 1 and bar > 17:
            src = hand.choice(sorted(pat))
            dst = (src + hand.choice([-1, 1])) % 12
            if dst not in pat:
                pat[dst] = pat.pop(src)
        for s, piece in pat.items():
            v = {"lo": 96, "sl": 90, "o": 80, "mu": 62}[piece] + hand.randint(-8, 6)
            P["conga"].add(st(bar, s), 0.3, piece, v)


BELL = (0, 2, 3, 5, 7, 8, 10)


def bell():
    """An agogo line in the break and the drop: seven of the twelve steps, low on the floor's beats."""
    for bar in list(range(85, 96)) + list(range(105, 129)):
        for s in BELL:
            P["bell"].add(st(bar, s), 0.3, "al" if s in (0, 8) else "ah", 74 if s in (0, 8) else 60)


def bass():
    """THE ROLLING BASS (G minor) between the kicks of whichever floor: under the four, steps 1 2 4 5 7 8 10 11 (a
    gallop); under the three, 2 3 6 7 10 11; and a sustained 808 sub under the bar."""
    hand = random.Random(31)
    for bar in range(9, BARS + 1):
        sec = sec_of(bar)
        if sec == "break":
            continue
        root = G + 31                                     # G2
        alt = {0: 0, 1: 0, 2: 3, 3: -2}[(bar // 2) % 4]   # G G Bb F: the line moves every two bars
        if sec in ("groove", "both", "drop", "outro") and bar >= 17 and bar < 141:
            steps = (1, 2, 4, 5, 7, 8, 10, 11)
        elif sec == "slow" and bar >= 69:                # the slow floor opens bare: toms, boom, shekere
            steps = (2, 3, 6, 7, 10, 11)
        else:
            steps = ()
        for s in steps:
            pch = root + (alt if s in (10, 11) else 0) + (12 if s == 11 and bar % 4 == 3 else 0)
            P["bass"].add(st(bar, s), STEP * 0.8, nm(pch), (94 if s in (2, 5, 8, 11, 3, 7) else 78) + hand.randint(-5, 5))
        if (sec != "outro" or bar < 137) and sec not in THREE_ON:     # under the three-floor the boom is the low end
            P["sub"].add(b0(bar), BAR - 0.05, nm(G + 19 + (alt if alt != 3 else 3)), 90)


def stab():
    """THE STAB, a Gm9 through a comb: on steps 2 6 10 (the three-floor's off-beats) from the groove on, so the
    tribe is hinted at before it plays; every eighth bar it answers a third higher."""
    for bar in range(25, 129):
        sec = sec_of(bar)
        if sec == "break":
            continue
        if bar % 2 == 0 and sec in ("groove",):
            continue
        hi = bar % 8 == 0
        chord = [G + 43, G + 46, G + 50, G + 53, G + 57] if not hi else [G + 46, G + 50, G + 53, G + 57, G + 60]
        for s in (2, 6, 10):
            P["stab"].add(st(bar, s), 0.22, ",".join(nm(m) for m in chord), 88 if s == 2 else 72)


def breakdown():
    """The break's drone (Gm add9, juno through a low-pass) and the Shepard riser in its last eight bars."""
    P["pad"].add(b0(81), 15 * BAR - 0.1, ",".join(nm(m) for m in (G + 43, G + 46, G + 50, G + 57)), 70)
    P["riser"].add(b0(89), 8 * BAR - 0.1, "C4", 90)


LEVEL = {"intro": -7, "groove": -1, "both": 0, "slow": -3, "break": -14, "drop": 0, "outro": -8}


def dyn_lane():
    """The set's dynamics: the break drops right down, the drop comes back at full weight."""
    sec = lambda beats: beats * 60 / BPM
    pts = []
    for name, a, z in SECTIONS:
        t0 = sec(b0(a))
        if pts:
            pts.append([f"{max(0.0, t0 - 0.25):.3f}s", pts[-1][1]])
        pts.append([f"{t0:.3f}s", float(LEVEL[name])])
    return pts


def main():
    floors()
    backbeat()
    shuffle()
    congas()
    bell()
    bass()
    stab()
    breakdown()
    beat_s = 60 / BPM
    tr = lambda name, patch, **kw: dict({"name": name, "patch": patch, "score": P[name].score()}, **kw)
    pump = lambda d: {"type": "pump", "on": "four", "depth": d, "attack": "3ms", "release": "300ms", "curve": 0.6}
    song = {
        "about": "Chirpers - Phantom Downbeat (Chirpers IV), track 4 by chirper-three: TWO FLOORS. Tribal / percussive "
                 "warehouse techno with a metric modulation: a 12-step pivot grid that is a shuffle at 128 under a 909 "
                 "four-on-the-floor and straight sixteenths at 96 under the toms' three-to-the-bar. Generated by "
                 "compose/chirpers4/src/chirpers4-t4.py; see compose/chirpers4/styles.md.",
        "tempo": BPM,
        "tail": "3s",
        "ceiling": "-0.3dB",
        "buses": {
            # the RUMBLE (after chirper-two's t10): the kicks' tails, a low hall, driven, ducking under each kick
            "rumble": {"fx": ["reverb kind=hall decay=2.4s mix=1", "lp cutoff=130",
                              {"type": "tape", "drive": 0.6, "mix": 1},
                              {"type": "pump", "on": "four", "depth": "-14dB", "release": "290ms", "curve": 0.8}]},
            "room": {"fx": ["reverb kind=room decay=1.1s mix=1 predelay=12ms", "hp cutoff=300"]},
        },
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=30", "peak cutoff=45 q=1.2 gain=-6dB",
                                                    "lowshelf cutoff=120 gain=-2dB", "peak cutoff=420 q=0.8 gain=3dB",
                                                    "peak cutoff=2500 q=0.7 gain=2dB", "highshelf cutoff=7000 gain=-1dB"]},
                          {"type": "gain", "gain": "+22dB"},
                          {"type": "compressor", "threshold": "-14dB", "ratio": 3, "attack": "12ms", "release": "140ms",
                           "makeup": "2dB"},
                          {"type": "drive", "drive": 0.4, "mix": 0.35},  # parallel saturation: the spikes rounded
                          {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                          # the set's dynamics AFTER the saturation, so the break's drop is not squashed back up
                          "limiter ceiling=-0.3dB"],
                   "auto": {"dyn": {"points": dyn_lane()}}},
        "tracks": [
            tr("four", "909", gain="0dB", sends={"rumble": "-14dB"}),                       # the machine's floor
            tr("kh", "909", gain="-8dB", fx=["lp cutoff=6000"]),
            tr("toms", "prog-tom", gain="-6dB", sends={"rumble": "-18dB", "room": "-14dB"},  # the tribe's floor
               fx=[{"type": "drive", "drive": 0.35, "mix": 0.5}]),
            tr("boom", "808", gain="-14dB", fx=[{"type": "drive", "drive": 0.3, "mix": 0.4}]),
            tr("clap", "909", gain="-2dB", sends={"room": "-8dB"}),
            tr("hats", "909", gain="-7dB", pan=0.1),
            tr("shek", "afro-perc", gain="-5dB", pan=-0.2, sends={"room": "-18dB"}),        # THE PIVOT
            tr("conga", "congas", gain="-4dB", pan=0.25, sends={"room": "-14dB"}),
            tr("bell", "afro-perc", gain="-10dB", pan=-0.35, sends={"room": "-12dB"}),
            tr("bass", "analog-bass", gain="-6dB", fx=["lp cutoff=1400", pump("-8dB")]),
            tr("sub", "808", gain="-24dB", fx=[pump("-10dB")]),
            tr("stab", "brass-stab", gain="-7dB", pan=-0.15, sends={"room": "-10dB"},
               fx=[{"type": "filter", "kind": "comb", "cutoff": 196, "q": 6},
                   {"type": "delay", "time": f"{2 * STEP * beat_s * 1000:.0f}ms", "feedback": 0.38, "mix": 0.3},
                   pump("-8dB")]),
            tr("pad", "juno-pad", gain="-12dB", fx=["lp cutoff=1400"], sends={"room": "-6dB"}),
            tr("riser", "fx-riser-shepard", gain="-12dB"),
        ],
    }
    with open(OUT, "w") as f:
        json.dump(song, f, indent=1)
        f.write("\n")
    print(f"wrote {OUT}: {BARS} bars, {TOTAL * beat_s:.0f} s")


if __name__ == "__main__":
    main()
