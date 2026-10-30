#!/usr/bin/env python3
"""Chirpers - Soft Concrete (Chirpers V), track 1, the opener: FIRST LIGHT (chirper-three).

2-STEP LIQUID drum & bass, 174 bpm, C minor / Eb major: the album's door, dawn into the dancefloor.

The groove is UK-garage 2-step at drum & bass tempo: a kick on the one and a skip on the and-of-3 (steps 0 and 10),
the snare on 2 and 4 (steps 4 and 12) with soft ghosts, and sixteenth hats SWUNG like garage (the off sixteenths
late); under the drops a quiet bed of wM's synthesised amen, re-sequenced from its ghost slices, rolls underneath.
Lush ninth chords (a juno pad held, an epiano comping in the 2-step's gaps with its damper), a warm sub on the
roots pumped by the kick, a short hook on a breathy low whistle (a vocal chop until v4), and only in the second drop a soft drifting reese. Patient entries (Harry: refine, don't
overcook): it opens half-time and drumless, chords and chops in tape hiss, and lets the drums in through a filter.

FORM (128 bars, 174 bpm, ~2:57):
  intro  1-16    pad and keys in hiss, sparse chops; filtered hats from 9
  build  17-32   half-time kick and snare (17), then the full 2-step through a low-pass opening over 8 bars (25)
  drop   33-64   the roller: 2-step drums, swung hats, the amen bed, the sub, comping keys, the chop hook
  break  65-80   drums out: the pad and the hook alone, then a riser
  drop2  81-112  everything back, and the soft reese
  outro  113-128 thinning to hats, pad and a last chop
"""
import json
import os
import random

OUT = os.environ.get("C5T1_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers5-t1.yaml")
BPM = 174
S = 16
BAR = 4.0
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
SECTIONS = [("intro", 1, 16), ("build", 17, 32), ("drop", 33, 64), ("break", 65, 80), ("drop2", 81, 112),
            ("outro", 113, 128)]
BARS = SECTIONS[-1][2]
TOTAL = BARS * BAR
SW = 0.085                                   # garage swing: the off sixteenths this many beats late (~29 ms, v6)


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def b0(bar):
    return (bar - 1) * BAR


def x16(bar, step):
    return b0(bar) + step / 4 + (SW if step % 2 else 0.0)


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
            base, _, mods = head.partition("^")
            toks.append(f"{base}/{ln:.5g}b@{vel}" + (f"^{mods}" if mods else ""))
            pos = s + ln
        if total - pos > 1e-5:
            toks.append(f"R/{total - pos:.5g}b")
        return " ".join(toks)


P = {}


def part(n):
    return P.setdefault(n, Part())


# two bars each: Abmaj9 | Gm9 | Cm9 | Bb13sus (euphoria and melancholy in the same four chords)
CHORDS = [(8, [56, 60, 63, 67, 70]), (7, [55, 58, 62, 65, 69]), (0, [55, 60, 63, 67, 74]), (10, [58, 63, 65, 68, 72])]


def chord_at(bar):
    return CHORDS[((bar - 1) // 2) % 4]


def drums():
    hand = random.Random(1)
    for bar in range(9, 125):
        sec = sec_of(bar)
        full = sec in ("drop", "drop2") or (sec == "build" and bar >= 25)
        half = sec == "build" and bar < 25
        if full or half:
            part("kick").add(x16(bar, 0), 0.5, "k", 112)
            if full:
                skip = SKIPS[bar % 4]                                     # THE SKIP WANDERS (v3): 10 11 10 7
                part("kick").add(x16(bar, skip), 0.5, "k", 100)
                if bar % 4 == 0:
                    part("kick").add(x16(bar, 10), 0.4, "k", 84)          # the fourth bar doubles it: 7 and 10
            if full:
                for s in (4, 12):
                    part("snare").add(x16(bar, s) + 0.01, 0.5, "s", 104 + hand.randint(-4, 4))
                if sec in ("drop", "drop2"):
                    for s in (7, 14):                                     # THE RIM (v6): a swung rimshot on the
                        part("rim").add(x16(bar, s), 0.25, "rs", 80 + hand.randint(-6, 4))   # off-sixteenths
                for s in (3, 9, 14):                                      # ghosts on the off-sixteenths (v3)
                    if hand.random() < 0.6:
                        part("snare").add(x16(bar, s), 0.25, "s", 40 + hand.randint(-6, 8))
            else:
                part("snare").add(x16(bar, 8) + 0.01, 0.5, "s", 100)       # half-time: the snare on 3
        hats = (sec == "intro" and bar >= 9) or sec in ("build", "drop", "drop2") or (sec == "outro" and bar < 125)
        if hats:
            for s in range(16):
                if sec == "intro" and s % 2 == 0:
                    continue
                v = (74 if s in (0, 3, 6, 8, 11, 14) else 48) + hand.randint(-6, 6)   # the 3-3-2 push (v3)
                if sec == "intro":
                    v -= 12
                part("hats").add(x16(bar, s), 0.2, "h", v)


AMEN = [2, 3, 6, 7, 9, 11, 13, 14, 15]
SKIPS = [7, 10, 11, 10]      # the 2-step's second kick, bar by bar (bar % 4): a drummer's skip, not a loop's       # the amen's ghost and ride slices (not its kicks and main snares)


def amen_bed():
    """A quiet re-sequenced amen under the drops: its ghost slices, rolling, one re-pitched or reversed now and then."""
    hand = random.Random(7)
    for bar in range(41, 65):     # v5: drop 1 waits 8 bars for the bed (v7: drop 2 has the ROLLER instead)
        for s in range(16):
            if s in (0, 4, 10, 12) or hand.random() < 0.35:
                continue
            sl = hand.choice(AMEN) + 16 * (bar % 2)
            mod = "^tune=2" if hand.random() < 0.08 else ("^rev=1" if hand.random() < 0.05 else "")
            part("amen").add(x16(bar, s), 0.25, nm(36 + sl) + mod, 60 + hand.randint(-10, 10))


ROLL = [0, 2, 3, 6, 4, 11, 13, 7]      # the roller's eighth-note slices (v7)


def roller():
    """THE AMEN COMES FORWARD (v7): in the second drop the bed becomes a ROLLER, eighth-note slices of wM's amen in
    their own order, the off-eighths laid back like a hand on the pads, every fourth bar's last hit pitched up three
    semitones into the next phrase: the opener ends in the album's rolling world."""
    hand = random.Random(9)
    for bar in range(81, 113):
        for k, sl in enumerate(ROLL):
            at = b0(bar) + k / 2         # v9: straight, on the hats' grid (the laid-back off-eighths fought the swing)
            mod = "^tune=3" if (bar % 4 == 0 and k == 7) else ""
            part("roll").add(at, 0.5, nm(36 + sl + 16 * (bar % 2 if k >= 4 else 0)) + mod,
                             (92 if k in (0, 4) else 74) + hand.randint(-6, 6))


def harmony():
    hand = random.Random(3)
    for bar in range(1, 125, 2):
        sec = sec_of(bar)
        root, voic = chord_at(bar)
        pk = "padb" if sec == "break" else "pad"                       # v9: the break's pad and keys on their own
        kk = "keysb" if sec == "break" else "keys"                     # tracks, through the band-pass sweep
        part(pk).add(b0(bar), 2 * BAR - 0.1, ",".join(nm(m) for m in voic), 66 if sec in ("intro", "break") else 58)
        if sec in ("drop", "drop2", "build"):
            # the keys comp in the 2-step's gaps: the and-of-1, the a-of-2, and the and-of-3 of the second bar
            for b, s in ((bar, 2), (bar, 7), (bar + 1, 2), (bar + 1, 11)):
                part("keys").add(x16(b, s), 0.6, ",".join(nm(m + 12 if m < 60 else m) for m in voic[1:]),
                                 70 + hand.randint(-6, 6))
        elif sec in ("intro", "break") or (sec == "outro" and bar < 121):
            part(kk).add(b0(bar), 1.5, ",".join(nm(m) for m in voic), 60)
        if sec in ("drop", "drop2", "build") and bar >= 25:
            r = 24 + root                                                  # the sub on the roots (C1..Bb1)
            part("sub").add(b0(bar), 2 * BAR - 0.1, nm(r if r >= 26 else r + 12), 96)
        if sec == "drop2":
            part("reese").add(b0(bar), 2 * BAR - 0.1, nm(36 + root if 36 + root <= 46 else 24 + root), 70)


HOOK = [(0, "G5"), (3, "Eb5"), (6, "F5"), (10, "G5"), (16, "Bb5"), (19, "G5"), (22, "F5"), (26, "Eb5")]   # 2 bars


def chops():
    """THE HOOK (since v4 on a low whistle, legato, an octave down; v1-v3 a vocal chop) over two bars, sparse in the intro, every other phrase in the drops,
    alone in the break."""
    hand = random.Random(5)
    for bar in range(5, 125, 2):
        sec = sec_of(bar)
        if sec == "intro" and bar % 4 != 1:
            continue
        if sec in ("drop", "drop2") and ((bar - 1) // 4) % 2 == 1 or 33 <= bar < 41:   # v5: drop 1 opens bare
            continue
        if sec == "build" or (sec == "outro" and bar > 117):
            continue
        for k, (s, n) in enumerate(HOOK):
            bb = bar + s // 16
            nxt = HOOK[k + 1][0] if k + 1 < len(HOOK) else 32
            m = NAMES.index(n[:-1]) + 12 * (int(n[-1]) + 1)   # at pitch (G5-Bb5): it fills the mix's 1 kHz hole; an
            # octave down it crowded 300-400 Hz (+8..+11 dB over the genre)
            part("hook").add(x16(bb, s % 16), (nxt - s) / 4 * 0.9, nm(m), 84 + hand.randint(-8, 6))   # legato


LEVEL = {"intro": -4, "build": -2, "drop": 0, "break": -5, "drop2": 0, "outro": -4}


def lanes():
    sec = lambda beats: beats * 60 / BPM
    dyn = []
    for name, a, z in SECTIONS:
        t0 = sec(b0(a))
        if dyn:
            dyn.append([f"{max(0.0, t0 - 0.2):.3f}s", dyn[-1][1]])
        dyn.append([f"{t0:.3f}s", float(LEVEL[name])])
    # the build's low-pass opening over bars 25-32 (and closed through the intro)
    lp = [["0s", 0.0], [f"{sec(b0(25)):.3f}s", 0.0], [f"{sec(b0(33)) - 0.05:.3f}s", 1.0], [f"{sec(b0(33)):.3f}s", 1.0]]
    return dyn, lp


# v9: THE BREAK SWEEPS - a band-pass on the pad and the keys, only in the break (its mix opens there), rising from
# 300 Hz to 3 kHz over the sixteen bars, so the breakdown travels instead of sitting
BP = {"type": "filter", "kind": "bp", "q": 1.6, "cutoff": {"value": 300, "mod": [{"src": "auto.bp", "amount": 1}]}}


def bp_lanes():
    sec = lambda beats: beats * 60 / BPM
    a, z = sec(b0(65)), sec(b0(81))
    bp = [["0s", 0.0], [f"{a:.3f}s", 0.0], [f"{z - 0.05:.3f}s", 2700.0], [f"{z:.3f}s", 2700.0]]   # 300 Hz + lane
    return {"bp": {"points": bp}}


def main():
    drums()
    amen_bed()
    roller()
    harmony()
    chops()
    part("riser").add(b0(77), 4 * BAR - 0.1, "C4", 80)
    dyn, lp = lanes()
    bp_auto = bp_lanes()
    pump = {"type": "pump", "on": "kick", "depth": "-8dB", "attack": "3ms", "release": "230ms", "curve": 0.6}
    tr = lambda n, patch, **kw: dict({"name": n, "patch": patch, "score": part(n).score()}, **kw)
    song = {
        "about": "Chirpers - Soft Concrete (Chirpers V), track 1 (opener) by chirper-three: FIRST LIGHT. 2-step "
                 "liquid drum & bass: a garage-swung 2-step at 174 under lush ninth chords, a warm sub, a vocal-chop "
                 "hook and a quiet amen bed. Generated by compose/chirpers5/src/chirpers5-t1.py.",
        "tempo": BPM,
        "tail": "3s",
        "ceiling": "-1.0dB",
        "true_peak": True,               # v5: wM's clipping fix: limiters oversample 4x with lookahead, never clamp
        "volume": "0dB",
        "buses": {"drums": {"fx": [{"type": "compressor", "threshold": "-16dB", "ratio": 4, "attack": "1ms",
                                     "release": "70ms", "makeup": "2dB"},
                                    "clip ceiling=-11dB knee=0.7 link=true"]},   # chirper-two's clean liquid recipe
                  "space": {"fx": ["reverb kind=hall decay=3.2s mix=1 predelay=25ms", "hp cutoff=300", "lp cutoff=8000"]},
                  "echo": {"fx": [{"type": "delay", "time": "3/16", "feedback": 0.4, "mix": 1}, "lp cutoff=3500",
                                  "hp cutoff=400"]}},
        # v2: chirper-two's clean liquid master (the album's agreed -12.5 LUFS, no flat runs): glue, +7 dB into a fast
        # smooth compressor, the limiter only a safety net (the engine's limiter pins samples whenever it engages)
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=26", "peak cutoff=450 q=0.8 gain=-3dB",
                                                    "peak cutoff=1050 q=1.0 gain=2dB", "peak cutoff=3000 q=1.0 gain=1dB",
                                                    "highshelf cutoff=7000 gain=-7dB"]},   # v9: darker, more night
                          {"type": "filter", "kind": "lp", "cutoff": {"value": 600, "mod": [{"src": "auto.lp", "amount": 19000}]}},
                          {"type": "tape", "drive": 0.2, "mix": 0.4, "hiss": "-66dB", "wow": 2, "flutter": 1, "seed": 3},
                          {"type": "compressor", "threshold": "-22dB", "ratio": 2.5, "attack": "15ms", "release": "150ms",
                           "makeup": "0dB"},
                          {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                          {"type": "gain", "gain": "+12.5dB"},   # (+7 in the recipe; this mix has more headroom)
                          {"type": "compressor", "threshold": "-5dB", "ratio": 10, "attack": "0.3ms", "release": "60ms",
                           "makeup": "0dB"},
                          "limiter ceiling=-1.2dB release=80ms"],   # v5: true-peak limiter (song true_peak), no clamping
                   "auto": {"dyn": {"points": dyn}, "lp": {"points": lp}}},
        "tracks": [
            tr("kick", "tight-kit", gain="-4dB", out="drums"),
            tr("snare", "tight-kit", gain="-6dB", out="drums", sends={"space": "-14dB"}),
            tr("hats", "tight-kit", gain="-13dB", pan=0.15, out="drums"),
            tr("rim", "tight-kit", gain="-9dB", pan=-0.2, out="drums", sends={"space": "-16dB"}),   # v6: the swing, heard
            tr("amen", "amen-chops", gain="-13dB", out="drums", fx=["hp cutoff=500", pump]),
            tr("roll", "amen-chops", gain="-10dB", out="drums", fx=["hp cutoff=150", pump]),   # v7: the roller
            tr("sub", "808", gain="-4dB", fx=[{"type": "drive", "drive": 0.2, "mix": 0.4},
                                              {"type": "phantom", "harmonics": "-4dB", "odd": 0.4, "remove": 0.0},
                                              pump]),   # v9: wM's phantom puts the sub's harmonics on small speakers
            tr("reese", "reese", gain="-12dB", fx=["lp cutoff=700", pump]),
            tr("pad", "juno-pad", gain="-8dB", sends={"space": "-6dB"}, lfo={"pf": {"wave": "sine", "rate": "20b"}},
               fx=[{"type": "filter", "kind": "lp", "cutoff": {"value": 1600, "mod": [{"src": "lfo.pf", "amount": 700}]}},
                   pump]),
            tr("padb", "juno-pad", gain="-6dB", sends={"space": "-4dB"}, fx=["lp cutoff=1600", BP], auto=bp_auto),
            tr("keys", "epiano-tine synth.tine.sense=0.2 play.release.patch=epiano-damper play.release.decay=2s",
               gain="-6dB", pan=-0.15, sends={"space": "-10dB", "echo": "-16dB"}),
            tr("keysb", "epiano-tine synth.tine.sense=0.2 play.release.patch=epiano-damper play.release.decay=2s",
               gain="-4dB", pan=-0.15, sends={"space": "-8dB", "echo": "-14dB"}, fx=[BP], auto=bp_auto),
            tr("hook", "low-whistle", gain="-7dB", pan=0.1, sends={"space": "-8dB", "echo": "-12dB"}),   # v4: the hook
            # on a breathy low whistle, not a vocal chop (the vocal side is chirper-one's Last Night Bus)
            tr("riser", "fx-riser-shepard", gain="-14dB"),
        ],
    }
    with open(OUT, "w") as f:
        json.dump(song, f, indent=1)
        f.write("\n")
    print(f"wrote {OUT}: {BARS} bars, {TOTAL * 60 / BPM:.0f} s")


if __name__ == "__main__":
    main()
