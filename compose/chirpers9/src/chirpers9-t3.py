#!/usr/bin/env python3
"""chirpers9-t3 (Accretion, track 3: the first storm). Composed by chirper-two.

THE FIRST STORM. Three cycles of different lengths run against the bar: E1 (t1's cell, 12 sixteenths), E2 (t2's
rhythm cell, 5 sixteenths) and E3, this track's element - a progression on a 2+2+3-beat harmonic rhythm (28
sixteenths) - each started at the phase that makes all of them, and the bar, land together on bar 88's downbeat. Before
it they collide (polymeter, a broken 909 and a chip-noise kit, stutters and crush that the storm's own lanes deepen);
from bar 72 the parts assemble bar by bar; at bar 88 every cycle meets one downbeat and the storm LOCKS into one
groove (E3 re-barred 2+2+4, E2 and E1 re-barred into 4/4). A whispered voice ("nothing here is late") arrives in
pieces through the storm and whole at the lock, where a robot (pvoc) sings it on E1's notes. The last 16 bars fall
into t4: redshift (pitch lanes sinking, the master closing) at the seam's 108 bpm.

E1 and E2 are PROVISIONAL until t1/t2 post theirs in compose/chirpers9/motifs.md; the phase maths takes any cycle.
Writes songs/chirpers9-t3.yaml (or T3_OUT). Original music.
"""
import json
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.environ.get("T3_OUT", os.path.join(ROOT, "songs", "chirpers9-t3.yaml"))

BARS, BPB = 128, 4
TOTAL = BARS * BPB
SECTIONS = [("infall", 0, 16), ("front", 16, 40), ("eyewall", 40, 72), ("lock", 72, 88), ("crest", 88, 112),
            ("outfall", 112, 128)]
# round 2 (section, w9 = bars 96-108, the crest's middle): T3_R2=crab (default) - a crab canon: a glass descant plays
# the locked undertow BACKWARDS three octaves up while the bass plays it forwards; a 909 ride opens the hats; a snare
# fill and an eighth's silence before bar 104, a crash on it. T3_R2=none reproduces v1.
R2 = os.environ.get("T3_R2", "crab") != "none"
# round 3 (palette): T3_R3=ring (default) - two swaps. E1's lead: the album's staple nes-pulse-lead (5 songs) -> a3-ring,
# a saw RING-MODULATED by an inharmonic sine (layer ringmod, which no preset uses), the ring mix 0.85 through the storm
# and 0.1 from the lock (the storm resolves in the timbre too). The storm's snare: the 909 (3 songs) -> ks-drum, a
# Karplus-Strong skin tuned to the key (D4, ghosts on A4), until the lock, where the 909 takes over. =none reproduces v2.
R3 = os.environ.get("T3_R3", "ring") != "none"
# round 4 (section, w7 = bars 72-84, the lock assembling, flagged static): T3_R4=align (default) - the arithmetic made
# audible. Glass ticks count the bar's downbeats upward through D Phrygian (D5 Eb5 F5 G5 A5 Bb5 C6, two bars a step, to
# the break), and every downbeat where a cycle ALREADY lines up with the bar - E1 at bars 73, 78, 83; E2 and E3 together
# at 74 and 81 - lands an alignment hit (crash, kick, a shard chord), the double ones after an eighth of held breath.
# Bar 88 is where all of them line up at once. T3_R4=none reproduces v3.
R4 = os.environ.get("T3_R4", "align") != "none"
CLEAR = []      # R4: the bar-82 statement, spoken clearly (the voice clears as the arithmetic does)
CREST = 88                      # the bar every cycle lands on
CREST16 = CREST * 16            # ... in sixteenths
EYE = (62, 66)                  # the eye of the storm: four bars of stillness inside it
BREAK = (86, CREST)             # the held breath before the lock
SEAM_IN, SEAM_OUT = 98, 108     # mixplan: t2>t3 98, t3>t4 108, flat across each 16-bar overlap

# ---- the elements -------------------------------------------------------------------------------------------
# E1, the seed (t1, chirper-zero): D A C G E, short long SNAP long held, and a beat's rest: 5 beats = 20 sixteenths.
E1 = [("D4", 0.5), ("A4", 0.75), ("C5", 0.25), ("G4", 1.0), ("E4", 1.5)]
E1_LEN16 = 20
# E2, "seven" (t2, chirper-one): hits on 0 2 3 5 of 7 sixteenths, pitched D A F C.
E2_LEN, E2_HITS = 7, (0, 2, 3, 5)
E2_PITCH = {0: ("D5", 112), 2: ("A5", 84), 3: ("F5", 98), 5: ("C5", 76)}
# E3, "the undertow" (THIS TRACK'S ELEMENT): a bass riff of 7 beats - E2's seven sixteenths augmented x4 - on D, the
# Neapolitan Eb (the storm's flat second, the darkness the inner disk's sharp fourth will answer) and C: (note, beats).
E3_RIFF = [("D2", 0.75), ("D2", 0.75), ("D3", 0.5), ("Eb2", 0.5), ("Eb2", 0.75), ("Bb1", 0.75), ("C2", 0.75),
           ("C2", 0.75), ("G2", 0.5), ("C3", 1.0)]
E3_LEN16 = 28
# ... and the storm's harmony over it, one chord per riff segment (2 + 2 + 3 beats), D4 common to all three.
E3 = [((50, 57, 64, 65), 2.0),            # Dm(add9):      D3 A3 E4 F4
      ((51, 58, 62, 67, 69), 2.0),        # Ebmaj7(#11):   Eb3 Bb3 D4 G4 A4   (the Neapolitan, lydian)
      ((48, 58, 62, 65), 3.0)]            # C11 (Bb/C):    C3 Bb3 D4 F4
E3_LOCKED = [2.0, 2.0, 4.0]               # re-barred at the lock: 2+2+4 = two bars (the riff's last C held a beat)
NOTE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def midi(n):
    return 12 * (int(n[-1]) + 1) + NOTE[n[0]] + (1 if "#" in n else -1 if "b" in n[1:] else 0)


def mtok(m):
    return f"m{m:g}"


def sec_of(bar):
    for name, a, b in SECTIONS:
        if a <= bar < b:
            return name
    return "outfall"


class Track:
    def __init__(self, name):
        self.name, self.ev = name, []

    def add(self, at, ln, head, vel, art=""):
        if at < 0 or at >= TOTAL:
            return
        self.ev.append((round(at, 4), max(0.03, round(ln, 4)), head, int(max(1, min(127, vel))), art))

    def score(self):
        ev = sorted(self.ev, key=lambda e: e[0])
        merged = []
        for e in ev:
            if merged and abs(merged[-1][0] - e[0]) < 1e-3:
                continue
            merged.append(e)
        toks, pos = [], 0.0
        for i, (s, ln, head, vel, art) in enumerate(merged):
            nxt = merged[i + 1][0] if i + 1 < len(merged) else TOTAL
            gap = nxt - s
            if s - pos > 1e-4:
                toks.append(f"R/{s - pos:.4g}b")
            if ln > gap + 1e-6:
                toks.append(f"{head}/{gap:.4g}b@{vel}^gate={min(4.0, ln / gap):.3g}{art}")
            else:
                toks.append(f"{head}/{ln:.4g}b@{vel}{art}")
                if gap - ln > 1e-4:
                    toks.append(f"R/{gap - ln:.4g}b")
            pos = nxt if ln <= gap + 1e-6 else s + gap
        if TOTAL - pos > 1e-4:
            toks.append(f"R/{TOTAL - pos:.4g}b")
        return " ".join(toks) if toks else f"R/{TOTAL}b"


def euclid(k, n, rot=0):
    pat = [((i * k) % n) < k for i in range(n)]
    return [pat[(i + rot) % n] for i in range(n)]


def cycle_starts(length16, lo16, hi16):
    """Cycle starts (in sixteenths) of a LENGTH16 cycle phased to land on the crest, within [lo16, hi16)."""
    first = CREST16 - length16 * math.ceil((CREST16 - lo16) / length16)
    return list(range(first, hi16, length16))


# ---- patches (inline, this track's own; 'a3-' = Accretion t3) -------------------------------------------------
PATCHES = {
    "a3-grit": {"about": "chirper-two: the storm's bass - a sine phase-modulated by itself an octave up, the index "
                         "thrown on each attack, through drive and a low-pass: a hard, grainy low end, not a squelch",
                "synth": {"layers": [{"name": "m", "ratio": 2, "audible": False},
                                     {"wave": "sine", "pm": [{"from": "m", "depth": {"value": 0.15, "mod": [
                                         {"src": "env.bite", "amount": 0.9}]}}]},
                                     {"wave": "sine", "ratio": 0.5, "level": "-9dB"}],
                          "env": {"bite": {"a": "0.5ms", "d": "70ms", "s": 0.1, "r": "40ms"}},
                          "drive": 0.35,
                          "filters": ["lp cutoff=1400 q=0.8"],
                          "amp": {"a": "2ms", "d": "300ms", "s": 0.7, "r": "60ms"}},
                "play": {"mono": True, "glide": "12ms"}},
    "a3-shard": {"about": "chirper-two: crushed chord shards - two detuned saws and a 1:3.01 PM edge, a fast filter "
                          "snap; the storm's stabs and, held, the lock's chords",
                 "synth": {"layers": [{"wave": "saw", "detune": -9}, {"wave": "saw", "detune": 9},
                                      {"name": "e", "ratio": 3.01, "audible": False},
                                      {"wave": "sine", "level": "-6dB",
                                       "pm": [{"from": "e", "depth": {"value": 0.05, "mod": [
                                           {"src": "env.snap", "amount": 0.6}]}}]}],
                           "env": {"snap": {"a": "0.5ms", "d": "90ms", "s": 0.0, "r": "30ms"}},
                           "filters": [{"kind": "lp", "q": 1.2, "cutoff": {"value": 900, "mod": [
                               {"src": "env.snap", "amount": 3.2}]}}],
                           "amp": {"a": "1ms", "d": "180ms", "s": 0.45, "r": "90ms"}}},
    "a3-dust": {"about": "chirper-two: the infall's dust - a dark saw pad, slow in and out, for the cloud to shred",
                "synth": {"layers": [{"wave": "saw", "detune": -6}, {"wave": "saw", "detune": 6},
                                     {"wave": "triangle", "ratio": 2, "level": "-10dB"}],
                          "filters": ["hp cutoff=110", "lp cutoff=2200 q=0.5"],
                          "amp": {"a": "900ms", "d": "1s", "s": 0.8, "r": "1.6s"}}},
    "a3-tracker": {"about": "chirper-two: the tracker arp - an NES pulse whose stepped LFO walks the chord's own "
                            "intervals every 32nd, retriggered per note (a 1990s module's arpeggio command)",
                   "synth": {"layers": [{"type": "chip", "chip": {"kind": "pulse", "duty": 0.25}}],
                             "amp": {"a": "1ms", "d": "120ms", "s": 0.55, "r": "40ms"}}},
}
ARP_STEPS = {0: [0, 7, 14, 15, 19], 1: [0, 7, 11, 16, 18], 2: [0, 10, 14, 17, 22]}   # chord intervals over each root


def arp_patch(steps):
    p = json.loads(json.dumps(PATCHES["a3-tracker"]))
    p["synth"]["lfo"] = {"arp": {"steps": steps, "rate": "1/32", "retrig": True}}
    p["synth"]["pitch"] = {"value": 0, "mod": [{"src": "lfo.arp", "amount": 1}]}
    return p


for _i, _st in ARP_STEPS.items():
    PATCHES[f"a3-arp{_i}"] = arp_patch(_st)


def build():
    rng = random.Random(9)
    T = {k: Track(k) for k in ("kick", "snare", "hats", "perc", "chipsn", "chiphat", "bass", "shard", "arp0",
                               "arp1", "arp2", "e1", "e1hi", "e2", "dust", "sub", "hold", "riser", "whisper", "robot", "floor",
                               "glass", "tick")}

    # ---- E3: the progression -------------------------------------------------------------------------------
    # infall: augmented x2 on the dust pad (14-beat cycle), phased to the crest as well
    for c in cycle_starts(56, 0, 16 * 16):
        at = c / 4.0
        for (ch, beats) in E3:
            if 0 <= at < 64:
                T["dust"].add(at, beats * 2 - 0.1, ",".join(mtok(m) for m in ch), 62)
            at += beats * 2
    # the storm: 2+2+3, shards struck on displaced sixteenths, the bass on the roots, tracker arps above
    for c in cycle_starts(28, 16 * 16, CREST16):
        at = c / 4.0
        for k, (ch, beats) in enumerate(E3):
            bar = int(at // 4)
            sec = sec_of(bar)
            if at >= 64:
                hits = 0 if (sec == "front" and bar < 28) else 2 if sec == "front" else 3
                for h in range(hits):
                    off = rng.choice([0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]) if h else rng.choice([0, 0.25, 0.5])
                    if off < beats:
                        T["shard"].add(at + off, 0.2, ",".join(mtok(m) for m in ch), 88 + rng.randint(-10, 14))
                if sec in ("eyewall", "lock"):
                    T[f"arp{k}"].add(at, beats - 0.05, mtok(ch[0] + 12), 70 + (8 if sec == "eyewall" else 0))
            at += beats
    # E3 itself, the undertow, in the storm: the riff on its 7-beat cycle, glitched (dropped notes, octave throws)
    for c in cycle_starts(E3_LEN16, 16 * 16, CREST16):
        at = c / 4.0
        for n, ln in E3_RIFF:
            sec = sec_of(int(at // 4))
            if at >= 64:
                if not (sec == "eyewall" and rng.random() < 0.12):
                    up = 12 if (sec == "eyewall" and rng.random() < 0.15) else 0
                    T["bass"].add(at, ln * 0.85, mtok(midi(n) + up), (108 if ln >= 0.75 else 94) + rng.randint(-8, 8))
            at += ln
    # the floor under it: a sine an octave below the riff's long notes, the storm's and the crest's 30-80 Hz
    for c in cycle_starts(E3_LEN16, 16 * 16, 112 * 16):
        at = c / 4.0
        for n, ln in (E3_RIFF if at < CREST * 4 else E3_RIFF[:-1] + [(E3_RIFF[-1][0], E3_RIFF[-1][1] + 1.0)]):
            if ln >= 0.75 and 64 <= at < 112 * 4 and not (EYE[0] * 4 <= at < EYE[1] * 4 or BREAK[0] * 4 <= at < BREAK[1] * 4):
                T["floor"].add(at, ln * 0.9, mtok(midi(n) - 12 if midi(n) >= 36 else midi(n)), 90)
            at += ln
    # the lock and after: re-barred 2+2+4, steady
    for bar in range(CREST, 112, 2):
        at = bar * 4.0
        for k, ((ch, _), beats) in enumerate(zip(E3, E3_LOCKED)):
            T["shard"].add(at, 0.22, ",".join(mtok(m) for m in ch), 96)
            T["shard"].add(at + 0.75, 0.22, ",".join(mtok(m) for m in ch), 78)
            if beats > 2:
                T["shard"].add(at + 2.5, 0.22, ",".join(mtok(m) for m in ch), 84)
            T[f"arp{k}"].add(at, beats - 0.05, mtok(ch[0] + 12), 78)
            T["hold"].add(at, beats - 0.1, ",".join(mtok(m + 12) for m in ch[1:]), 70)
            T["sub"].add(at, beats - 0.1, mtok(ch[0] - 24), 70)
            at += beats
        at = bar * 4.0
        for j, (n, ln) in enumerate(E3_RIFF):                  # the riff, re-barred: its last C held a beat more
            ln2 = ln + (1.0 if j == len(E3_RIFF) - 1 else 0)
            T["bass"].add(at, ln2 * 0.88, mtok(midi(n)), 112 if ln >= 0.75 else 98)
            at += ln2
    # the outfall: E3 augmented again, falling into t4; the D4 common tone held over the seam
    for i, bar in enumerate(range(112, 120, 4)):                 # the riff augmented x2, falling
        at = bar * 4.0
        for n, ln in E3_RIFF[:6] if i == 0 else E3_RIFF[6:]:
            T["bass"].add(at, ln * 1.8, mtok(midi(n)), 96 - 8 * i)
            at += ln * 2
        ch = E3[i % 3][0]
        T["dust"].add(bar * 4.0, 15.8, ",".join(mtok(m) for m in ch), 70)
    T["dust"].add(120 * 4.0, 31.8, ",".join(mtok(m) for m in E3[0][0]), 74)   # Dm(add9) held: t4 lifts its third
    T["sub"].add(112 * 4.0, 16 * 4.0 - 0.2, "m62", 60)              # the D4, held into the next track

    # ---- E1: the cell (12 sixteenths), displaced and inverted in the storm, upright at the lock -----------------
    e1m = [midi(n) for n, _ in E1]
    for c in cycle_starts(E1_LEN16, 8 * 16, CREST16):
        at, bar = c / 4.0, int(c // 16)
        sec = sec_of(bar)
        inv = sec in ("front", "eyewall") and rng.random() < 0.5
        if sec == "infall" and rng.random() < 0.5:
            continue
        shift = rng.choice([0, 0.25, 0.5]) if sec in ("front", "eyewall") else 0
        for (n, ln), m in zip(E1, e1m):
            mm = 2 * e1m[0] - m if inv else m
            if sec == "eyewall" and rng.random() < 0.25:
                continue                                         # fragments
            T["e1"].add(at + shift, ln * 0.9, mtok(mm + 12), 74 + rng.randint(-8, 8))
            at += ln
    for bar in range(CREST, 112):
        at = bar * 4.0
        for (n, ln), m in zip(E1, e1m):
            T["e1"].add(at, ln * 0.92, mtok(m + 12), 84)
            if bar >= CREST + 8:
                T["e1hi"].add(at, ln * 0.92, mtok(m + 24), 70)
            at += ln

    # ---- E2: the rhythm cell (5 sixteenths) on the chip-metal channel, then barred at the lock -----------------
    for c in cycle_starts(E2_LEN, 0, CREST16):
        if c < 16 * 16 and rng.random() < 0.6:              # the infall: t2's cell arriving in pieces
            continue
        for h in E2_HITS:
            n, v = E2_PITCH[h]
            T["e2"].add((c + h) / 4.0, 0.12, n, v - (14 if c < 16 * 16 else 0))
    for bar in range(CREST, 112):
        for half in (0, 8):                                     # re-barred: seven sixteenths and a rest = half a bar
            for h in E2_HITS:
                n, v = E2_PITCH[h]
                T["e2"].add(bar * 4.0 + (half + h) / 4.0, 0.12, n, v)

    # ---- drums: the storm's broken machine, assembling into the groove -----------------------------------------
    LOCK_K, LOCK_S, LOCK_GHOST = (0, 3, 10), (4, 12), (7, 14, 15)
    for bar in range(16, 112):
        sec, b0 = sec_of(bar), bar * 4.0
        p_lock = 0.0 if bar < 72 else 1.0 if bar >= CREST else (bar - 72) / 16.0
        locked = rng.random() < p_lock
        if locked:
            for s in LOCK_K:
                T["kick"].add(b0 + s / 4, 0.25, "k", 118 if s == 0 else 104)
            for s in LOCK_S:
                T["snare"].add(b0 + s / 4, 0.25, "s", 112)
                T["perc"].add(b0 + s / 4, 0.25, "cp", 70)
            for s in LOCK_GHOST:
                T["snare"].add(b0 + s / 4, 0.25, "rs", 48 + rng.randint(0, 14))
            for s in range(16):
                T["hats"].add(b0 + s / 4, 0.12, "oh" if s == 14 else "h", 86 if s % 4 == 2 else 58 + rng.randint(0, 10))
            continue
        heavy = sec == "eyewall"
        for s, on in enumerate(euclid(5 if not heavy else 7, 16, rng.randrange(16))):
            if on:
                T["kick"].add(b0 + s / 4, 0.25, "kh" if heavy and rng.random() < 0.3 else "k", 100 + rng.randint(0, 22))
        for s, on in enumerate(euclid(3, 16, rng.randrange(16))):
            if on:
                T["snare"].add(b0 + s / 4, 0.25, "s", 96 + rng.randint(0, 24))
        for s, on in enumerate(euclid(11 if heavy else 9, 16, rng.randrange(16))):
            if on:
                T["hats"].add(b0 + s / 4, 0.1, "h", 50 + rng.randint(0, 34))
        if heavy or bar % 4 == 3:                       # chip-noise rolls at phrase ends, everywhere in the eyewall
            n = rng.choice([4, 6, 8])
            st = 4.0 - n * 0.125
            for j in range(n):
                T["chipsn"].add(b0 + st + j * 0.125, 0.1, "G4", 60 + j * 7)
        if heavy:
            for s in range(16):
                if rng.random() < 0.35:
                    T["chiphat"].add(b0 + s / 4 + (0.125 if rng.random() < 0.3 else 0), 0.06, "C7", 44 + rng.randint(0, 30))
    # the outfall: the groove thins out across the seam (kick and hats last)
    for bar in range(112, 124):
        b0 = bar * 4.0
        if bar < 120:
            T["kick"].add(b0, 0.25, "k", 104 - (bar - 112) * 4)
            T["kick"].add(b0 + 2.5, 0.25, "k", 90 - (bar - 112) * 4)
        for s in range(0, 16, 2):
            T["hats"].add(b0 + s / 4, 0.1, "h", 60 - (bar - 112) * 3)

    # ---- the infall: sparse chip clicks under t2's handover --------------------------------------------------------
    for bar in range(4, 16):
        for s in range(16):
            if rng.random() < 0.06 + 0.012 * bar:
                T["chiphat"].add(bar * 4.0 + s / 4, 0.05, "C7", 30 + rng.randint(0, 24))

    # ---- the eye and the break: everything driven stops; the eye keeps E3's D (dust + sub), the break a riser ----
    stops = ("kick", "snare", "hats", "perc", "chipsn", "chiphat", "bass", "shard", "arp0", "arp1", "arp2", "e1", "e2")
    for k in stops:
        T[k].ev = [e for e in T[k].ev if not (EYE[0] * 4 <= e[0] < EYE[1] * 4 or BREAK[0] * 4 <= e[0] < BREAK[1] * 4)]
    T["dust"].add(EYE[0] * 4.0, (EYE[1] - EYE[0]) * 4.0 - 0.2, ",".join(mtok(m) for m in E3[0][0]), 84)
    T["sub"].add(EYE[0] * 4.0, (EYE[1] - EYE[0]) * 4.0 - 0.2, "m38", 66)
    T["kick"].add(EYE[1] * 4.0, 0.25, "kh", 124)                    # the wall comes back
    T["riser"].add(BREAK[0] * 4.0, (BREAK[1] - BREAK[0]) * 4.0, "C4", 96)
    T["dust"].add(BREAK[0] * 4.0, 7.8, ",".join(mtok(m) for m in E3[2][0]), 80)

    # ---- round 2: the crest's middle (w9, bars 96-108) - a crab canon, a ride, a fill and a held breath -----------
    if R2:
        r2 = random.Random(31)
        lock = E3_RIFF[:-1] + [(E3_RIFF[-1][0], E3_RIFF[-1][1] + 1.0)]          # 2+2+4, 8 beats
        crab = list(reversed(lock))
        for cyc, bar in enumerate(range(96, 108, 2)):
            at = bar * 4.0
            for n, ln in crab:
                T["glass"].add(at, ln * 0.95, mtok(midi(n) + 36 - (12 if cyc % 2 and midi(n) + 36 > 84 else 0)),
                               80 if ln >= 0.75 else 68)
                at += ln
        for bar in range(96, 108):
            for b in range(4):
                T["perc"].add(bar * 4.0 + b, 0.25, "rd", 66 if b % 2 else 78)
        b0 = 103 * 4.0
        for j in range(6):                                                       # the fill: 16ths, rising
            T["snare"].add(b0 + 2.0 + j * 0.25, 0.25, "s", 78 + 7 * j)
        gap = (b0 + 3.5, b0 + 4.0)                                               # an eighth of held breath
        for k in T:
            T[k].ev = [e for e in T[k].ev if not (gap[0] <= e[0] < gap[1])]
        T["perc"].add(104 * 4.0, 1.0, "c", 100 + r2.randint(0, 10))
    # ---- the voice: whispered in pieces through the storm, whole at the lock, then sung by the robot -------------
    late = json.load(open(os.path.join(HERE, "t3", "late.json")))["tracks"][0]["notes"]
    whisper, robot = [], []

    def put(dst, at, keep=None, scale=1.0):
        for i, n in enumerate(late):
            if keep is not None and i not in keep:
                continue
            d = {"at": round(at + n["at"] * scale, 4), "len": round(n["len"] * scale, 4), "ph": n["ph"],
                 "pitch": n["pitch"], "vel": n["vel"]}
            if n.get("expr_path"):
                d["expr_path"] = n["expr_path"]
            dst.append(d)

    for bar, keep in ((30, {0}), (36, {2}), (44, {4}), (50, {0, 1}), (58, {2, 3}), (63, {0, 4}), (76, {0, 1, 2}),
                      (82, {0, 1, 2, 3})):
        put(whisper, bar * 4.0 + 0.5, keep)
    put(whisper, (CREST - 2) * 4.0, None)                 # whole, two bars before the lock
    if R4:
        CLEAR.extend(n for n in whisper if 82 * 4.0 <= n["at"] < 84 * 4.0)
        whisper[:] = [n for n in whisper if not (82 * 4.0 <= n["at"] < 84 * 4.0)]
    for bar in (92, 100, 108):
        put(robot, bar * 4.0, None)
    if R4:
        hits = {}
        for name, ln in (("E1", E1_LEN16), ("E2", E2_LEN), ("E3", E3_LEN16)):
            for c in cycle_starts(ln, 72 * 16, 86 * 16):
                if c % 16 == 0 and 72 * 16 <= c < 86 * 16:
                    hits.setdefault(c // 16, []).append(name)
        drums = ("kick", "snare", "hats", "perc", "chipsn", "chiphat")
        for bar, who in sorted(hits.items()):
            b0 = bar * 4.0
            if len(who) > 1:
                for k in drums:
                    T[k].ev = [e for e in T[k].ev if not (b0 - 0.5 <= e[0] < b0)]
            T["perc"].add(b0, 1.0, "c", 96 if len(who) == 1 else 116)
            T["kick"].add(b0, 0.25, "k", 112 if len(who) == 1 else 124)
            T["shard"].add(b0, 0.5, ",".join(mtok(m + 12) for m in E3[0][0]), 92 if len(who) == 1 else 112)
        steps = ["D5", "Eb5", "F5", "G5", "A5", "Bb5", "C6"]
        for bar in range(72, 86):
            T["tick"].add(bar * 4.0, 0.9, mtok(midi(steps[(bar - 72) // 2])), 84 + 2 * (bar - 72) + (12 if bar in hits else 0))
    return T, whisper, robot


def main():
    T, whisper, robot = build()
    tempo = [{"at": "0b", "bpm": SEAM_IN}, {"at": "64b", "bpm": SEAM_IN},
             {"at": "448b", "bpm": SEAM_OUT, "ramp": True}]
    dyn = [["0b", -5.0], ["64b", -2.5], ["159.99b", -2.0], ["160b", -0.5], ["247.99b", 0.0], ["248b", -3.0],
           ["263.99b", -3.0], ["264b", 0.0], ["343.99b", -1.0], ["344b", -2.0], ["351.99b", -2.0], ["352b", 1.0],
           ["448b", 0.5], ["512b", -3.0]]
    stut = [["0b", 0.0], ["64b", 0.12], ["160b", 0.3], ["280b", 0.42], ["288b", 0.3], ["352b", 0.0], ["512b", 0.0]]
    grit = [["0b", 0.0], ["64b", 0.2], ["160b", 0.55], ["288b", 0.6], ["352b", 0.0], ["512b", 0.0]]
    fall = [["0b", 0.0], ["448b", 0.0], ["512b", -7.0]]
    close = [["0b", 0.0], ["448b", 0.0], ["512b", -2.0]]
    stop = [["0b", 0.0], ["223.99b", 0.0], ["224b", 1.0], ["225b", 1.0], ["225.01b", 0.0]]

    def storm_fx(extra=()):
        return [{"type": "stutter", "slice": "1/16", "repeats": 3,
                 "chance": {"value": 0, "mod": [{"src": "auto.glitch", "amount": 1}]}},
                {"type": "crush", "bits": 6, "rate": "9kHz",
                 "mix": {"value": 0, "mod": [{"src": "auto.grit", "amount": 1}]}}] + list(extra)

    def lanes(**kw):
        d = {"glitch": {"points": stut}, "grit": {"points": grit}}
        d.update(kw)
        return d

    falling = [{"type": "pitch", "semitones": {"value": 0, "mod": [{"src": "auto.fall", "amount": 1}]}}]
    tracks = [
        {"name": "kick", "patch": "909", "gain": "-1dB", "fx": storm_fx(), "auto": lanes(), "score": T["kick"].score()},
        {"name": "snare", "patch": "909", "gain": "-4dB", "fx": storm_fx(), "auto": lanes(), "score": T["snare"].score()},
        {"name": "hats", "patch": "909", "gain": "-9dB", "pan": 0.15, "fx": storm_fx(), "auto": lanes(),
         "score": T["hats"].score()},
        {"name": "perc", "patch": "909", "gain": "-10dB", "pan": -0.1, "score": T["perc"].score()},
        {"name": "chipsn", "patch": "nes-noise-snare", "gain": "-8dB", "pan": -0.25, "score": T["chipsn"].score()},
        {"name": "chiphat", "patch": "nes-noise-hat", "gain": "-14dB", "pan": 0.35, "score": T["chiphat"].score()},
        {"name": "bass", "patch": "a3-grit", "gain": "-2.5dB", "fx": storm_fx(falling), "auto": lanes(fall={"points": fall}),
         "score": T["bass"].score()},
        {"name": "sub", "patch": "sub", "gain": "-12dB", "score": T["sub"].score()},
        {"name": "floor", "patch": "sub", "gain": "-10dB", "score": T["floor"].score()},
        {"name": "hold", "patch": "a3-shard", "gain": "-16dB", "pan": 0.1, "fx": ["lp cutoff=3500 q=0.6"],
         "sends": {"space": "-6dB"}, "score": T["hold"].score()},
        {"name": "riser", "patch": "fx-riser", "gain": "-10dB", "score": T["riser"].score()},
        {"name": "shard", "patch": "a3-shard", "gain": "-10dB", "pan": -0.1,
         "fx": storm_fx(falling) + ["delay time=3/16 mix=0.12 feedback=0.25"], "auto": lanes(fall={"points": fall}),
         "sends": {"space": "-12dB"}, "score": T["shard"].score()},
        *({"name": f"arp{k}", "patch": f"a3-arp{k}", "gain": "-17dB", "pan": (-0.3, 0.3, 0.0)[k], "fx": falling,
           "auto": {"fall": {"points": fall}}, "sends": {"space": "-10dB"}, "score": T[f"arp{k}"].score()}
          for k in range(3)),
        {"name": "e1", "patch": "nes-pulse-lead", "gain": "-13dB", "pan": 0.2,
         "fx": falling + ["delay time=1/8 mix=0.2 feedback=0.3"], "auto": {"fall": {"points": fall}},
         "sends": {"space": "-8dB"}, "score": T["e1"].score()},
        {"name": "e1hi", "patch": "nes-pulse-lead", "gain": "-19dB", "pan": -0.3,
         "fx": ["delay time=3/16 mix=0.25 feedback=0.3"], "sends": {"space": "-6dB"}, "score": T["e1hi"].score()},
        {"name": "e2", "patch": "chip-metal", "gain": "-15dB", "pan": -0.35, "score": T["e2"].score()},
        {"name": "dust", "patch": "a3-dust", "gain": "-15dB",
         "fx": [{"type": "cloud", "size": "120ms", "density": 14, "position": "400ms", "spray": "300ms",
                 "scatter": 0.4, "reverse": 0.3, "spread": 0.9, "mix": 0.6}],
         "sends": {"space": "-6dB"}, "score": T["dust"].score()},     # the residue t4 receives stays at pitch
        {"name": "whisper", "patch": "voice-speech", "gain": "-3dB", "pan": -0.1,
         "fx": ["pvoc mode=whisper seed=3", "delay time=3/8 mix=0.18 feedback=0.35"], "sends": {"space": "-6dB"},
         "notes": whisper},
        {"name": "robot", "patch": "voice-speech", "gain": "-4dB", "pan": 0.1,
         "fx": [{"type": "pvoc", "mode": "robot", "pitch": "C4",
                 "tune": {"value": 0, "mod": [{"src": "track.e1.key", "amount": 12}]}}],
         "sends": {"space": "-9dB"}, "notes": robot},
    ]
    patches = dict(PATCHES)
    if R3:
        patches["a3-ring"] = {"about": "chirper-two: the storm's lead - a saw ring-modulated by a sine at 1.414:1 (layer ringmod), "
                                       "an inharmonic, metallic edge whose ring mix rides an auto lane (`ring`: 0 = storm, "
                                       "1 = clean), over a quiet square an octave down",
                              "synth": {"layers": [{"name": "m", "wave": "sine", "ratio": 1.414, "audible": False},
                                                   {"wave": "saw", "ringmod": {"from": "m", "mix": {"value": 0.85, "mod": [
                                                       {"src": "auto.ring", "amount": -0.75}]}}},
                                                   {"wave": "square", "ratio": 0.5, "level": "-16dB"}],
                                        "filters": ["hp cutoff=200", "lp cutoff=4500 q=0.7"],
                                        "amp": {"a": "3ms", "d": "180ms", "s": 0.6, "r": "90ms"}}}
        ring = {"points": [["0b", 0.0], [f"{CREST * 4 - 0.01}b", 0.0], [f"{CREST * 4}b", 1.0], ["512b", 1.0]]}
        for tr in tracks:
            if tr["name"] in ("e1", "e1hi"):
                tr["patch"] = "a3-ring"
                tr["gain"] = {"e1": "-15dB", "e1hi": "-21dB"}[tr["name"]]
                tr.setdefault("auto", {})["ring"] = ring
        storm = Track("skin")
        lock = [e for e in T["snare"].ev if e[0] >= CREST * 4]
        storm.ev = [(e[0], e[1], "D4" if e[2] == "s" else "A4", e[3], e[4]) for e in T["snare"].ev if e[0] < CREST * 4]
        T["snare"].ev = lock
        for tr in tracks:
            if tr["name"] == "snare":
                tr["score"] = T["snare"].score()
        tracks.append({"name": "skin", "patch": "ks-drum", "gain": "-5dB", "pan": -0.05, "fx": storm_fx(), "auto": lanes(),
                       "score": storm.score()})
    if R2 or R4:
        patches["a3-glass"] = {"about": "chirper-two: the crest's glass - a sine phase-modulated at 3.5:1, the index pinged "
                                        "on each attack and settling to a faint shimmer; an octave partial; no low end",
                               "synth": {"layers": [{"name": "g", "ratio": 3.5, "audible": False},
                                                    {"wave": "sine", "pm": [{"from": "g", "depth": {"value": 0.06, "mod": [
                                                        {"src": "env.ping", "amount": 0.45}]}}]},
                                                    {"wave": "sine", "ratio": 2, "level": "-14dB"}],
                                         "env": {"ping": {"a": "0.5ms", "d": "250ms", "s": 0.05, "r": "100ms"}},
                                         "filters": ["hp cutoff=300", "lp cutoff=8000 q=0.6"],
                                         "amp": {"a": "2ms", "d": "600ms", "s": 0.45, "r": "400ms"}}}
    if R2:
        tracks.append({"name": "glass", "patch": "a3-glass", "gain": "-8dB", "pan": 0.25,
                       "fx": ["delay time=3/8 mix=0.2 feedback=0.35"], "sends": {"space": "-6dB"},
                       "score": T["glass"].score()})
    if R4:
        tracks.append({"name": "speak", "patch": "voice-speech", "gain": "3dB", "pan": 0.0,
                       "fx": ["delay time=3/8 mix=0.12 feedback=0.25"], "sends": {"space": "-10dB"}, "notes": CLEAR})
        tracks.append({"name": "tick", "patch": "a3-glass", "gain": "-10dB", "pan": -0.2,
                       "fx": ["delay time=1/4 mix=0.2 feedback=0.4"], "sends": {"space": "-6dB"},
                       "score": T["tick"].score()})
    master = {"fx": [{"type": "eq", "bands": ["hp cutoff=25", "peak cutoff=100 gain=3dB q=1.0",
                                              "peak cutoff=320 gain=-2dB q=0.8",
                                              "highshelf cutoff=8000 gain=2dB"]},
                     "glue threshold=-18dB ratio=2 attack=10ms release=150ms makeup=1dB",
                     {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                     {"type": "filter", "kind": "lp", "q": 0.707,
                      "cutoff": {"value": 20000, "mod": [{"src": "auto.close", "amount": 1}]}},
                     {"type": "tapestop", "stop": {"value": 0, "mod": [{"src": "auto.stop", "amount": 1}]},
                      "time": "1b", "curve": 1.6},
                     {"type": "limiter", "ceiling": "-1.2dB", "release": "80ms"}],
              "auto": {"dyn": {"points": dyn}, "close": {"points": close}, "stop": {"points": stop}}}
    about = ("chirpers - Accretion, track 3. Original composition by chirper-two, generated by "
             "compose/chirpers9/src/chirpers9-t3.py. The first storm: E1, E2 and E3 (a 2+2+3 progression) on cycles of "
             "12, 5 and 28 sixteenths, phased to meet the bar on one downbeat (bar 88), where the storm locks into a "
             "groove; a whispered line in pieces, whole at the lock, sung by a pvoc robot on E1's notes.")
    lines = [
        "about: " + json.dumps(about),
        "meta: " + json.dumps({"artist": "chirpers", "album": "Accretion", "title": "Phase Margin", "track": 3,
                               "year": 2026}),
        "tempo: " + json.dumps(tempo),
        f'length: "{TOTAL}b"',
        'tail: "0.75s"',
        'ceiling: "-1dB"',
        'volume: "0dB"',
        "loudness: -11",
        "true_peak: true",
        "event_stable: true",
        "patches: " + json.dumps(patches),
        "buses: " + json.dumps({"space": {"gain": "-5dB", "fx": ["hp cutoff=250", "reverb kind=plate decay=2.2s mix=1"]}}),
        "master: " + json.dumps(master),
        "tracks:",
    ]
    lines += ["  - " + json.dumps(t) for t in tracks]
    open(OUT, "w").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
