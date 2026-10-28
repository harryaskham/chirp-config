#!/usr/bin/env python3
"""chirpers1-t3 "Moult" (Chirpers, Ferrous Bloom, track 3: the groove). Composed by chirper-two.

Identity: 96 BPM, swung sixteenths (swing16 .55), half-time 4/4 kit with the cymbal on the quarter. The hypnotic figure is NINEFOLD, a 9-sixteenth
chug cell that realigns with the bar every 9 bars (so the A sections are 9 bars long and the realignment is the
section boundary). It moults: one slot changes every few repeats (a chug becomes a ghost, a rest becomes a stab, a
stab doubles), so the loop never quite repeats. Harmony is the THIRDS WHEEL: roots step by major thirds
F -> A -> C# -> F (the augmented-triad axis), and every stab is root + octave + major 3rd + augmented 5th, so the
song's colour is the hexatonic F G# A C C# E rather than the usual phrygian/locrian.

Emits songs/chirpers1-t3.yaml. Edit the music here, not the YAML.
"""
import json
import os

OUT = os.environ.get("MOULT_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers1-t3.yaml")
# Round 2 (kept as v2): P quarter-note cymbal pulse in the heavy sections; L less sub, more 80-120 Hz in the bass;
# D dynamics inside the loud sections (Moult builds, Lock's second cycle hits harder under a pad swell); A the cell's
# first chug is its accent; swing16 .6 -> .55: at .6 the odd-length cell flips swing parity every repeat and smears
# its own 9-against-16 (the onset autocorrelation saw only eighths); at .55 the cycle is felt and the riff still swings.
# MOULT_R2 / MOULT_SWING override them for A/B (MOULT_R2=none for v1's arrangement with MOULT_SWING=0.6).
R2 = set(filter(None, os.environ.get("MOULT_R2", "P,L,D,A").split(","))) - {"none"}
SWING16 = float(os.environ.get("MOULT_SWING", "0.55"))
# Round 3 (kept as v3): J, a ride-edge wash swells under the closing roll so Moult's end opens toward t4's cymbals
# (the join's spectral jump 9.9 -> 7.1 dB). MOULT_R3=none for v2.
R3 = set(filter(None, os.environ.get("MOULT_R3", "J").split(","))) - {"none"}
# Round 6 (sound playground): W = the WHEEL KIT, physical coupled-head drums (chirp `type: drum`, bd-7d117e) whose
# air-spring split is a major third, so every drum sounds a THIRDS WHEEL dyad, played as tuned toms in the Wheel,
# the Hollow and the Lock (kept as v4 on judgment; MOULT_R6=none for v3).
R6 = set(filter(None, os.environ.get("MOULT_R6", "W").split(","))) - {"none"}  # kept as v4
# The wheel kit's toms by the root they voice: batter F2 sounds F2+A2, A2 sounds A2+C#3, C#3 sounds C#3+F3.
WHEEL_TOM = {29: "t3", 33: "t2", 37: "t1"}


def wheel_kit():
    """Moult's kit: metal-kit-dry's cymbals and hats; kick, snare, ghost and toms rebuilt on the physical drum layer.
    Matched heads and cavity 0.294 put the in-phase pair a major third (x1.26) above the batter's tuning: the kick's
    batter is F1 and its air-raised pair A1; each tom's two loudest partials are neighbouring wheel notes."""
    cav = 0.294

    def piece(pitch, layer, filters, amp, drive, vs, gain="0dB"):
        return {"pitch": pitch, "gain": gain, "patch": {"synth": {"layers": [dict(type="drum", **layer)],
                "filters": filters, "amp": amp, "drive": drive}, "play": {"vel_sens": vs}}}
    tom = dict(beater="stick", contact=1.6, decay="1.1s", sharp=45, reso=1.0, cavity=cav, reso_level=0.6, air=0.45,
               strike=0.3, shell=0.3, damp=0.25, slap=0.5)
    tamp = {"a": "0.2ms", "d": "1.3s", "s": 0, "r": "80ms", "curve": 3}
    snare = dict(beater="stick", decay="0.35s", sharp=30, reso=1.5, cavity=0.35, reso_level=0.5, shell=0.45,
                 shell_hz=480, wires=0.55, gap=0.25, wire_tone="4.5k", strike=0.3, damp=0.3, slap=0.8)
    sf = ["hp cutoff=100", "peak cutoff=220 q=1 gain=2dB"]
    samp = {"a": "0.2ms", "d": "450ms", "s": 0, "r": "30ms"}
    return {"wheel-kit": {
        "about": "Moult's wheel kit (chirper-two): metal-kit-dry with physical coupled-head drums whose cavity split "
                 "is a major third, so each drum sounds a THIRDS WHEEL dyad (kick F1+A1; toms C#2+F2, F2+A2, A2+C#3, "
                 "C#3+F3).",
        "extends": "metal-kit-dry",
        "kit": {
            "k": piece("F1", dict(beater="felt", decay="0.45s", sharp=60, reso=1.0, cavity=cav, reso_level=0.6,
                                  air=0.4, strike=0.15, damp=0.4, shell=0.15, slap=0.7),
                       ["hp cutoff=28", "lowshelf cutoff=70 gain=2dB"],
                       {"a": "0.2ms", "d": "600ms", "s": 0, "r": "30ms", "curve": 4}, 0.2, 0.45, gain="8dB"),
            "s": piece("G3", snare, sf, samp, 0.15, 0.6),
            "g": piece("G3", dict(snare, strike=0.15), sf, samp, 0.15, 0.6, gain="-16dB"),
            "ft": piece("C#2", tom, ["hp cutoff=40"], tamp, 0.1, 0.55, gain="2.5dB"),
            "t3": piece("F2", tom, ["hp cutoff=45"], tamp, 0.1, 0.55, gain="2.5dB"),
            "t2": piece("A2", tom, ["hp cutoff=50"], tamp, 0.1, 0.55, gain="2.5dB"),
            "t1": piece("C#3", tom, ["hp cutoff=55"], tamp, 0.1, 0.55, gain="2.5dB")}}}
BPM = 96
STEP = 0.25  # beats per sixteenth
BAR = 16
NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
F1, A1, CS2 = 29, 33, 37  # the wheel's three roots (8-string F standard: F1 is the low open string)


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


class Part:
    """Events on the sixteenth grid: (step, length in steps, head, velocity, mark)."""

    def __init__(self, name):
        self.name, self.ev = name, []

    def add(self, step, length, head, vel, mark=""):
        self.ev.append((step, length, head, vel, mark))

    def score(self, total, prefix=""):
        merged = {}
        for e in sorted(self.ev, key=lambda e: (e[0], -e[3])):
            merged.setdefault(e[0], e)  # one event per step: the loudest wins
        ev = sorted(merged.values())
        toks, pos = ([prefix] if prefix else []), 0
        for i, (s, ln, head, vel, mark) in enumerate(ev):
            assert s >= pos, (self.name, s, pos, head)
            nxt = ev[i + 1][0] if i + 1 < len(ev) else total
            ln = min(ln, nxt - s)
            if s > pos:
                toks.append(f"R/{(s - pos) * STEP:g}b")
            toks.append(f"{head}/{ln * STEP:g}b@{vel}" + (f"^{mark}" if mark else ""))
            pos = s + ln
        if total > pos:
            toks.append(f"R/{(total - pos) * STEP:g}b")
        return " ".join(toks)


# ---------------- motifs ----------------
# NINEFOLD: 9 slots. X palm-muted root chug, x ghost (dead) chug, O open root ring, S augmented stab, . rest.
# The moult: each variant changes one or two slots of the previous one.
NINEFOLD = [
    "X.XX.x.S.",  # 0  statement
    "X.XX.x.SX",  # 1  a chug grows on the tail
    "X.XXxx.SX",  # 2  a ghost fills the gap
    "XX.Xxx.SX",  # 3  the second chug slips one sixteenth earlier (displacement)
    "XX.Xx.SSX",  # 4  the stab doubles
    "XX.X.xSS.",  # 5  the tail sheds
    "O..X.xSS.",  # 6  the head opens up: space
    "O.xX.xS.x",  # 7  stab truncated, ghosts at the edges
]


def stab(root):
    """Root + octave + major third + augmented fifth, voiced on the upper strings."""
    return [root + 12, root + 16, root + 20]


def ninefold(gl, gr, bass, kick, start, bars, root_at, variant_at, phase_r=None, accent=110):
    """Lay the 9-cell from `start` for `bars` bars. root_at(step) and variant_at(k) pick the root and the
    moult for repeat k; phase_r(step) -> extra sixteenths of delay for the right guitar (phasing)."""
    end = start + bars * BAR
    k, s = 0, start
    while s < end:
        pat, root = NINEFOLD[variant_at(k)], root_at(s)
        for i, c in enumerate(pat):
            t = s + i
            if t >= end or c == ".":
                continue
            d = phase_r(t) if phase_r else 0
            acc = accent(t) if callable(accent) else accent
            head = "A" in R2 and i == 0  # A: the cell's first chug is its accent (kick and guitars), the rest sit back
            if c == "X":
                for g, dd in ((gl, 0), (gr, d)):
                    g.add(t + dd, 1, nm(root), min(127, acc + 10) if head else acc - 6 * (i % 2), "pm")
                bass.add(t, 1, nm(root), 116 if head else 104)
                kick.append((t, 124 if head else (92 if "A" in R2 else 104)))
            elif c == "x":
                for g, dd in ((gl, 0), (gr, d)):
                    g.add(t + dd, 1, nm(root), 64, "pm")
            elif c == "O":
                for g, dd in ((gl, 0), (gr, d)):
                    g.add(t + dd, 2, f"{nm(root)},{nm(root + 12)}", acc)
                bass.add(t, 2, nm(root), 110)
                kick.append((t, 124 if head else 112))
            elif c == "S":
                ch = ",".join(nm(n) for n in stab(root))
                for g, dd in ((gl, 0), (gr, d)):
                    g.add(t + dd, 2, ch, acc - 4)
                bass.add(t, 2, nm(root), 100)
        k += 1
        s += 9


def hexatonic(root):
    """F G# A C C# E on any root: alternating minor 3rd / minor 2nd (the augmented scale)."""
    return [root + x for x in (0, 3, 4, 7, 8, 11)]


# ---------------- the song ----------------
def build():
    gl, gr, bass = Part("gtr-l"), Part("gtr-r"), Part("bass")
    drums, lead, clean, pad = Part("drums"), Part("lead"), Part("clean"), Part("pad")
    kick = []          # (step, vel) kicks that lock to the guitar
    kit = {}           # step -> {piece: vel}

    def hit(step, piece, vel):
        kit.setdefault(step, {})[piece] = max(vel, kit.get(step, {}).get(piece, 0))

    def halftime(start, bars, hats="h", hat_vel=(78, 58), ghosts=True, snare=110, pulse=None):
        """Half-time kit. With `pulse` (round 2, P) the cymbal states the 96 BPM quarter and nothing between, so
        NINEFOLD's 9-against-16 is what moves: pulse(bar) names the cymbal for that bar."""
        for b in range(bars):
            s0 = start + b * BAR
            if pulse and "P" in R2:
                for i in range(0, BAR, 4):
                    hit(s0 + i, pulse(b), 100 if i == 0 else 90)
            else:
                for i in range(0, BAR, 2):
                    hit(s0 + i, hats, hat_vel[(i // 2) % 2])
            hit(s0 + 8, "s", snare)
            if ghosts and b % 2 == 1:
                hit(s0 + 14, "g", 44)
                hit(s0 + 5, "g", 36)

    sec = {}
    t = 0

    # 1. TIDE (4 bars): the cell alone on the left guitar and bass, kit hats only; the pulse arrives in bar 3.
    sec["tide"] = (t, 4)
    tl, tr, tb, tk = Part("x"), Part("x"), Part("x"), []
    ninefold(tl, tr, tb, tk, t, 4, lambda s: F1, lambda k: 0, accent=96)
    # the figure is first heard on the clean guitar: chugs become muted F3 plucks, the stab a soft augmented triad;
    # the bass joins in bar 3, the rhythm pair only at bar 5 (the clean figure becomes the chug riff)
    for st, ln, head, vel, mark in tl.ev:
        if "," in head:
            clean.add(st, ln, ",".join(nm(n + 12) for n in stab(F1)), 64)
        else:
            clean.add(st, 1, nm(F1 + 24), max(46, vel - 40))
    for ev in tb.ev:
        if ev[0] >= t + 2 * BAR:
            bass.add(*ev[:3], ev[3] - 16, ev[4])
    for b in range(4):
        for i in range(0, BAR, 2):
            hit(t + b * BAR + i, "h", 40 + 8 * b)
    for s, v in tk:
        if s >= t + 2 * BAR:
            hit(s, "k", v - 20)
    hit(t + 2 * BAR + 8, "s", 84)
    hit(t + 3 * BAR + 8, "s", 96)
    # Round 5 (28 Oct, compscore 14c8f947), NOT kept, all off: the Ingot -> Moult seam from Moult's side. v3
    # 95.217/95.241 (seam: level 0.9 dB, spectral 19.0, Moult -47 dB at 83 Hz). B 94.338/94.286 (spectral 10.5, level
    # 7.2), B2 94.007/93.925 (level 14.2), T 94.333/94.240: every low end under the Tide lifts its level and costs
    # variety ~7 (93.6 -> 87): the thin opening is Moult's contrast. The seam is left to Ingot's last bar.
    if "B" in R3:  # only the bass carries Ingot's low F under the first two bars
        bass.add(t, 2 * BAR, nm(F1), 80)
    if "B2" in R3:  # the same, an octave up and softer: F2 (87 Hz, its 2nd harmonic ~262 Hz) is what the seam lacks;
        # the riff's F1 then drops in at bar 3
        bass.add(t, 2 * BAR, nm(F1 + 12), 60)
    if "T" in R3:  # tried in round 4, NOT kept (off by default): take over t2 "Ingot"'s held F-B: the bass holds F1
        # from the downbeat, a pad holds F2 B2 for two bars, then the B falls a semitone to A (with C# above). The join
        # from Ingot fell 22.7 -> 13.9 dB but flow stayed ~54 (anything over ~5 dB scores ~0 there) and the thin
        # opening lost its contrast (variety 93.6 -> 86.9; total -0.36/-1.07). Moult opening thin out of Ingot's
        # held chord is the point: the groove drops in.
        bass.add(t, 2 * BAR, nm(F1), 84)
        pad.add(t, 2 * BAR, ",".join(nm(n) for n in (F1 + 12, F1 + 18)), 86)
        pad.add(t + 2 * BAR, 2 * BAR, ",".join(nm(n) for n in (F1 + 12, F1 + 16, F1 + 20)), 80)
    for i, p in enumerate(("t3", "t3", "ft", "ft")):
        hit(t + 3 * BAR + 12 + i, p, 90 + 6 * i)
    t += 4 * BAR

    # 2. NINEFOLD (9 bars): the full rig; the moult walks 0 -> 1 -> 2.
    sec["ninefold"] = (t, 9)
    ninefold(gl, gr, bass, kick, t, 9, lambda s: F1, lambda k: min(k // 6, 2))
    halftime(t, 9, pulse=lambda b: "h")
    hit(t, "c", 118)
    t += 9 * BAR

    # 3. MOULT (9 bars): variants 3 -> 5; the right guitar slips one sixteenth late in the last 4 bars (phasing),
    # china on the first stab of each realignment-half.
    sec["moult"] = (t, 9)
    s0 = t
    ramp = (lambda st: 100 + int(16 * (st - s0) / (9 * BAR))) if "D" in R2 else 110  # D: Moult builds
    ninefold(gl, gr, bass, kick, t, 9, lambda s: F1, lambda k: 3 + min(k // 6, 2),
             phase_r=lambda st: 1 if st >= s0 + 5 * BAR else 0, accent=ramp)
    halftime(t, 9, ghosts=True, pulse=lambda b: "rd" if b < 5 else "rb")
    hit(t, "c", 120)
    hit(t + 5 * BAR, "x", 112)
    for i, p in enumerate(("s", "s", "t2", "t3", "ft", "ft")):
        hit(t + 9 * BAR - 6 + i, p, 92 + 5 * i)
    t += 9 * BAR

    # 4. THIRDS WHEEL (12 bars): roots F -> A -> C#, 4 bars each. Riff 5+5+6: open roots on 0, 5, 10, an augmented
    # stab on 12, ghosts on 3 and 8. A clean guitar pings the augmented arpeggio with a dotted-eighth delay.
    sec["wheel"] = (t, 12)
    for b in range(12):
        root = (F1, A1, CS2)[b // 4]
        s = t + b * BAR
        for o in (0, 5, 10):
            for g in (gl, gr):
                g.add(s + o, 2, f"{nm(root)},{nm(root + 12)}", 108)
            bass.add(s + o, 3, nm(root), 108)
            hit(s + o, "k", 108)
            if "W" in R6 and o:  # the toms answer the open roots: this root's wheel dyad
                hit(s + o, WHEEL_TOM[root], 104 if o == 5 else 96)
        if "W" in R6:  # the stab turns the wheel early: the next root's tom
            hit(s + 12, WHEEL_TOM[(F1, A1, CS2)[min(b + 1, 11) // 4]], 108)
        for o in (3, 8):
            for g in (gl, gr):
                g.add(s + o, 1, nm(root), 62, "pm")
        ch = ",".join(nm(n) for n in stab(root))
        for g in (gl, gr):
            g.add(s + 12, 3, ch, 104)
        bass.add(s + 12, 3, nm(root), 100)
        for i in range(0, BAR, 2):
            hit(s + i, "h", 74 if i % 4 == 0 else 56)
        hit(s + 8, "s", 108)
        arp = [root + 24, root + 28, root + 32, root + 28]
        for j, o in enumerate((2, 7, 13)):
            clean.add(s + o, 3, nm(arp[(b + j) % 4]), 76)
        if b % 4 == 0:
            hit(s, "c", 112)
    t += 12 * BAR

    # 5. HOLLOW (8 bars): the rhythm pair drops out. Clean hexatonic arpeggio in eighths with space, bass holds,
    # the pad holds the augmented triad, sidestick on 3, kick on 1 and the 'and' of 3.
    sec["hollow"] = (t, 8)
    hx = hexatonic(53)  # F3 G#3 A3 C4 C#4 E4
    line = [0, 2, 4, 5, 3, 1, 2, 4, 0, 3, 5, 4, 2, 1, 3, 0]  # a fixed path through the six notes
    for b in range(8):
        s = t + b * BAR
        if b >= 4:  # the bass stays out for the first half of the breath
            bass.add(s, 14, nm(A1), 56)
            hit(s + 10, "ft" if "W" in R6 else "k", 58)
        hit(s, "ft" if "W" in R6 else "k", 70 if b < 4 else 76)  # W: a deep tom heartbeat (C#2+F2)
        hit(s + 8, "ss", 66)
        for i in range(0, BAR, 4):
            hit(s + i, "h", 38)
        for j, o in enumerate((0, 3, 6, 10, 12)):
            n = hx[line[(b * 5 + j) % len(line)]] + (12 if b >= 6 and j == 4 else 0)
            clean.add(s + o, 2 if o != 12 else 4, nm(n), 70 + 4 * (j % 2))
    pad.add(t, 4 * BAR, ",".join(nm(n) for n in (53, 57, 61)), 70)
    pad.add(t + 4 * BAR, 4 * BAR, ",".join(nm(n) for n in (57, 61, 65)), 74)
    for i, p in enumerate(("t1", "t1", "t2", "t2", "t3", "t3", "ft", "ft")):
        hit(t + 8 * BAR - 8 + i, p, 80 + 5 * i)
    t += 8 * BAR

    # 6. NINEFOLD IN A (9 bars): the cell returns a major third up, wearing variants 6, 7, 4, and a lead sings a
    # swinging hexatonic line over it.
    sec["ninefold_a"] = (t, 9)
    ninefold(gl, gr, bass, kick, t, 9, lambda s: A1, lambda k: (6, 7, 4)[min(k // 6, 2)])
    halftime(t, 9, pulse=lambda b: "h")
    hit(t, "c", 120)
    hl = [n + 12 for n in hexatonic(A1 + 24)]  # A4 C5 C#5 E5 F5 G#5 (the lead plays them an octave lower)
    phrase = [  # (bar, step, length in steps, index into hl)
        (0, 0, 8, 3), (0, 8, 4, 4), (0, 12, 4, 3), (1, 0, 16, 2),
        (2, 0, 8, 1), (2, 8, 4, 2), (2, 12, 4, 3), (3, 0, 16, 5),
        (4, 0, 6, 0), (4, 6, 2, 5), (4, 8, 8, 4), (5, 0, 8, 3), (5, 8, 8, 2),
        (6, 0, 4, 1), (6, 4, 4, 2), (6, 8, 8, 3), (7, 0, 16, 2), (8, 0, 12, 0),
    ]
    for b, st, ln, i in phrase:
        lead.add(t + b * BAR + st, ln, nm(hl[i] - 12), 92)
    t += 9 * BAR

    # 7. LOCK (18 bars): two realignment cycles. The guitars keep NINEFOLD (variants 2/5), the bass leaves them
    # for the album's LATTICE seven-cell, so 9 against 7 against 16. Second cycle: the root turns the thirds wheel every two
    # bars, and the china marks every stab.
    sec["lock"] = (t, 18)
    s0 = t
    def lat_root(s):
        if s < s0 + 9 * BAR:
            return F1
        return (F1, A1, CS2, F1, A1, CS2, F1, F1, F1)[min((s - s0 - 9 * BAR) // (2 * BAR), 8)]
    dummy_bass = Part("x")
    lock_acc = (lambda st: 106 if st < s0 + 9 * BAR else 120) if "D" in R2 else 114  # D: the 2nd cycle hits harder
    ninefold(gl, gr, dummy_bass, kick, t, 18, lat_root, lambda k: (2, 5)[(k // 4) % 2], accent=lock_acc)
    # the bass borrows the album's LATTICE (t1): its 3+2+2 seven-cell, walking LATTICE's F-Gb-B-E line one note per
    # cell (4 against 3 onsets), so NINEFOLD's augmented stabs grind against LATTICE's minor 2nd, tritone and
    # major 7th; in the second cycle the line rides the thirds wheel (root, +1, +6, +11 on each wheel root).
    seven, line4 = "X..X.X.", (0, 1, 6, 11)
    s, cell = t, 0
    while s < t + 18 * BAR:
        r = lat_root(s) + line4[cell % 4]
        for i, c in enumerate(seven):
            if s + i < t + 18 * BAR and c != ".":
                bass.add(s + i, 2 if i == 0 else 1, nm(r), 112 if i == 0 else 98)
        s, cell = s + 7, cell + 1
    if "D" in R2:
        halftime(t, 9, hats="oh", hat_vel=(64, 48), snare=100, pulse=lambda b: "rd")
        halftime(t + 9 * BAR, 9, hats="oh", hat_vel=(74, 56), snare=118, pulse=lambda b: "x")
        if "W" in R6:  # the second cycle turns the wheel: its root's tom lands with every backbeat
            for b in range(9, 18):
                hit(t + b * BAR + 8, WHEEL_TOM[lat_root(t + b * BAR)], 112)
        for b in list(range(0, 9, 3)) + list(range(9, 18)):
            hit(t + b * BAR, "c", 112 if b < 9 else 120)
        pad.add(t + 9 * BAR, 9 * BAR, ",".join(nm(n) for n in (65, 69, 73)), 76)  # F4 A4 C#5 swells over cycle 2
    else:
        halftime(t, 18, hats="oh", hat_vel=(70, 52), pulse=lambda b: "rd" if b < 9 else "x")
        for b in range(0, 18, 2):
            hit(t + b * BAR, "c", 116)
    for st, ln, head, vel, mark in gl.ev:
        if st >= t + 9 * BAR and len(head.split(",")) == 3:  # the augmented stabs of the second cycle
            hit(st, "x", 100)
    t += 18 * BAR

    # 8. SILT (6 bars): the cell sheds to its first chug, the stab rings over the pad, then a tom/snare roll into
    # track 4 (the onslaught).
    sec["silt"] = (t, 6)
    ninefold(gl, gr, bass, kick, t, 2, lambda s: F1, lambda k: (0, 6, 6, 7)[min(k, 3)], accent=104)
    for b in (2, 3):
        s = t + b * BAR
        for o in (0, 9):
            for g in (gl, gr):
                g.add(s + o, 1, nm(F1), 96 - 10 * (b - 2), "pm")
            bass.add(s + o, 1, nm(F1), 96)
            hit(s + o, "k", 96)
        hit(s + 8, "s", 96)
    ring = ",".join(nm(n) for n in (F1, F1 + 12) + tuple(stab(F1)))
    for g in (gl, gr):
        g.add(t + 4 * BAR, 2 * BAR - 4, ring, 104)
    bass.add(t + 4 * BAR, 2 * BAR - 4, nm(F1), 104)
    hit(t + 4 * BAR, "c", 118)
    hit(t + 4 * BAR, "k", 110)
    pad.add(t, 6 * BAR, ",".join(nm(n) for n in (53, 57, 61, 65)), 80)
    # the Hollow's clean line comes back over the ring-out, an octave up and slower: the breath before track 4
    for j, o in enumerate((0, 6, 12, 18, 24, 30)):
        if o + 2 * BAR < 6 * BAR - 12:
            clean.add(t + 2 * BAR + 4 + o, 5, nm(hx[line[j]] + 12), 62)
    for i in range(12):
        hit(t + 6 * BAR - 12 + i, ("s", "t2", "t3", "ft")[i % 4] if i < 8 else "s", 70 + 4 * i)
        if "J" in R3:  # round 3: a ride-edge wash swells under the roll, opening Moult's end toward t4's cymbals
            hit(t + 6 * BAR - 12 + i, "rde", 50 + 5 * i)
    t += 6 * BAR

    for s, v in kick:
        hit(s, "k", v)
    for s in sorted(kit):
        pieces = kit[s]
        head = ",".join(sorted(pieces))
        drums.add(s, 1, head, max(pieces.values()))
    return t, sec, dict(gl=gl, gr=gr, bass=bass, drums=drums, lead=lead, clean=clean, pad=pad)


def main():
    total, sec, P = build()
    sw = f"swing16={SWING16:g}"
    delay = {"type": "delay", "time": f"{60000 / BPM * 0.75:.1f}ms", "feedback": 0.32, "mix": 0.22}
    # Mix (v1): the first render sat -10 dB under the genre envelope at 77-122 Hz and +4..9 dB over it at 270-830 Hz,
    # with too much sub and too little 2.4-9.5 kHz: body into the bass, the box out of the guitars, air on the master.
    geq = {"type": "eq", "bands": ["peak cutoff=420 q=0.8 gain=-4dB", "highshelf cutoff=3000 gain=3dB"]}
    beq = {"type": "eq", "bands": ["lowshelf cutoff=45 gain=-4dB", "peak cutoff=100 q=0.9 gain=6dB"]}
    if "L" in R2:  # round 2: less sub, more 80-120 Hz body
        beq = {"type": "eq", "bands": ["lowshelf cutoff=55 gain=-7dB", "peak cutoff=105 q=0.8 gain=7dB"]}
    tracks = [
        {"name": "gtr-l", "patch": "m8-emg-l", "pan": -1, "gain": "-2dB", "fx": [geq], "score": P["gl"].score(total, sw)},
        {"name": "gtr-r", "patch": "m8-emg-r", "pan": 1, "gain": "-2dB", "fx": [geq], "score": P["gr"].score(total, sw)},
        {"name": "bass", "patch": "bass-fat", "gain": "-1dB", "fx": [beq], "score": P["bass"].score(total, sw)},
        {"name": "drums", "patch": "wheel-kit" if "W" in R6 else "metal-kit-dry", "out": "kit",
         "score": P["drums"].score(total, sw)},
        {"name": "lead", "patch": "m8-lead", "gain": "-5dB", "pan": 0.15, "fx": [delay, "reverb kind=plate decay=1.8s mix=0.18"],
         "score": P["lead"].score(total, sw)},
        {"name": "clean", "patch": "m8-twang-chorus", "gain": "-7dB", "pan": -0.25, "fx": [delay, "reverb kind=hall decay=2.4s mix=0.25"],
         "score": P["clean"].score(total, sw)},
        {"name": "pad", "patch": "juno-pad", "gain": "-14dB", "score": P["pad"].score(total)},
    ]
    secs = "; ".join(f"{k} {v[0] // BAR + 1}-{v[0] // BAR + v[1]}" for k, v in sec.items())
    about = ("Chirpers - Moult (Ferrous Bloom, track 3: the groove). Original composition by chirper-two, generated by "
             "compose/chirpers1/src/chirpers1-t3.py. 96 BPM swung half-time (swing16 .55), quarter-note cymbals; NINEFOLD, a 9-sixteenth chug cell that "
             "moults one slot at a time and realigns every 9 bars; the THIRDS WHEEL F-A-C# (augmented colour); the climax "
             "locks NINEFOLD against the album's LATTICE seven-cell on the bass. "
             f"Bars: {secs}.")
    lines = [
        f"about: {json.dumps(about)}",
        "meta: " + json.dumps({"artist": "Chirpers", "album": "Ferrous Bloom", "title": "Moult", "track": 3, "year": 2026}),
        f"tempo: {BPM}",
        f'length: "{total * STEP:g}b"',
        'ceiling: "-0.1dB"',
        'volume: "4dB"',
        "buses: " + json.dumps({"kit": {"fx": ["rack:drum-bus-punch", {"type": "eq", "bands": ["highshelf cutoff=8000 gain=2dB"]}]}}),
    ] + (["patches: " + json.dumps(wheel_kit())] if "W" in R6 else []) + [
        "master: " + json.dumps({"fx": [
            {"type": "eq", "bands": ["lowshelf cutoff=40 gain=-3dB", "peak cutoff=100 q=1 gain=3dB",
                                     "peak cutoff=500 q=0.7 gain=-2.5dB", "highshelf cutoff=3000 gain=3dB",
                                     "highshelf cutoff=12000 gain=-2dB"]},
            "glue threshold=-20dB ratio=2.5 attack=10ms release=160ms makeup=2dB",
            "clip drive=5dB ceiling=-0.5dB"]}),
        "tracks:",
    ]
    lines += ["  - " + json.dumps(t) for t in tracks]
    open(OUT, "w").write("\n".join(lines) + "\n")
    print(f"wrote {OUT}: {total // BAR} bars, {total * STEP / BPM * 60:.1f} s; {secs}")


if __name__ == "__main__":
    main()
